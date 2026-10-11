"""Entity-specific regression checks for the seventh state batch."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("ND", "OH", "OK", "OR", "PA")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp,lp",
    [
        ("ND", "135", "145", "110"),
        ("OH", "99", "99", "99"),
        ("OK", "300", "300", "300"),
        ("OR", "275", "275", "275"),
        ("PA", "250", "250", "250"),
    ],
)
def test_batch7_foreign_fees_are_not_domestic_fees(state, llc, corp, lp):
    r = DEFAULT_REGISTRY.get(state)
    assert r.for_entity(EntityType.LLC).filing_fee == Decimal(llc)
    assert r.for_entity(EntityType.C_CORP).filing_fee == Decimal(corp)
    assert r.for_entity(EntityType.LP).filing_fee == Decimal(lp)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch7_guides_replace_placeholders_with_reviewed_rules(state, entity):
    r = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for text in (page.html, page.markdown):
        assert "Guide coming soon." not in text
        assert r.for_entity(entity).qualification_citation in text
    assert 'content="noindex, follow"' not in page.html
    assert r.rules_verified and not r.verification_issues
    assert all(s.verified_on == date(2026, 10, 11) for s in r.sources)


@pytest.mark.parametrize(
    "state,entity",
    [
        ("ND", EntityType.LLC),
        ("ND", EntityType.C_CORP),
        ("OK", EntityType.LLC),
        ("OR", EntityType.LLC),
        ("OR", EntityType.C_CORP),
    ],
)
def test_batch7_thirty_day_isolated_transactions_stop_at_day_31(state, entity):
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.NOT_REQUIRED
    )
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


@pytest.mark.parametrize(
    "state,entity",
    [
        ("OH", EntityType.LLC),
        ("PA", EntityType.LLC),
        ("PA", EntityType.C_CORP),
    ],
)
def test_unlimited_isolated_transaction_statutes_do_not_invent_a_day_cap(state, entity):
    rule = DEFAULT_REGISTRY.get(state).for_entity(entity)
    assert rule.threshold.isolated_transaction_without_day_limit
    assert rule.threshold.isolated_transaction_max_days is None
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 60).decision
        is QualificationDecision.NOT_REQUIRED
    )


@pytest.mark.parametrize("state", ["OH", "OK"])
def test_corporations_do_not_inherit_llc_safe_harbors(state):
    for activity in (Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.SOLICITATION):
        assert (
            screen(state, EntityType.C_CORP, activity).decision
            is QualificationDecision.REVIEW_REQUIRED
        )
        assert (
            screen(state, EntityType.LLC, activity).decision is QualificationDecision.NOT_REQUIRED
        )
    assert (
        screen(state, EntityType.C_CORP, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen(state, EntityType.C_CORP, Activity.INTERSTATE_COMMERCE).decision
        is QualificationDecision.NOT_REQUIRED
    )


@pytest.mark.parametrize("entity", TYPES)
def test_north_dakota_income_property_triggers_and_interstate_review(entity):
    assert screen("ND", entity, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert (
        screen("ND", entity, Activity.INTERSTATE_COMMERCE).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_north_dakota_solicitation_differs_by_entity():
    assert (
        screen("ND", EntityType.LLC, Activity.SOLICITATION).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen("ND", EntityType.C_CORP, Activity.SOLICITATION).decision
        is QualificationDecision.NOT_REQUIRED
    )


def test_north_dakota_foreign_corporate_deadline_is_may_not_august():
    r = DEFAULT_REGISTRY.get("ND")
    llc = r.for_entity(EntityType.LLC).annual_obligations[0]
    corp = r.for_entity(EntityType.C_CORP).annual_obligations[0]
    assert "November 15" in llc.due_rule and llc.fee == Decimal("50")
    assert "May 15" in corp.due_rule and corp.fee == Decimal("25")
    assert "August 1" in corp.notes
    assert "year after" in llc.due_rule and "year after" in corp.due_rule
    for entity in TYPES:
        description = r.for_entity(entity).qualification_penalty.description
        assert "$5,000" in description and "$1,000" in description


@pytest.mark.parametrize("entity", TYPES)
def test_ohio_has_no_ordinary_annual_report(entity):
    r = DEFAULT_REGISTRY.get("OH")
    assert not r.for_entity(entity).annual_obligations
    assert "no regular SOS annual report" in r.notes[0]
    if entity is EntityType.C_CORP:
        assert "90 days" in r.for_entity(entity).good_standing_evidence
        assert "$250–$10,000" in r.for_entity(entity).qualification_penalty.description
    else:
        assert (
            "no home-jurisdiction certificate attachment"
            in r.for_entity(entity).good_standing_evidence
        )


def test_oklahoma_conditional_agent_fees_and_capital_certificate_are_distinct():
    r = DEFAULT_REGISTRY.get("OK")
    assert not r.registered_agent.private_appointment_required
    llc = r.for_entity(EntityType.LLC)
    corp = r.for_entity(EntityType.C_CORP)
    assert llc.annual_obligations[0].fee == Decimal("25")
    assert llc.annual_obligations[1].fee == Decimal("40")
    assert "only when" in llc.annual_obligations[1].due_rule
    assert corp.annual_obligations[0].fee == Decimal("100")
    assert "Tax Commission" in corp.annual_obligations[0].due_rule
    assert corp.annual_obligations[1].fee is None
    assert "authorized capitalization" in corp.annual_obligations[1].due_rule
    assert "0.1%" in corp.annual_obligations[1].notes
    assert "$300 minimum" in r.notes[0]
    assert "after tax year 2023" in r.notes[0]
    assert "60 days" in llc.good_standing_evidence
    assert "six months" in corp.good_standing_evidence
    assert "$200–$500" in corp.qualification_penalty.description


def test_oklahoma_sources_use_the_current_annual_text_before_november_amendment():
    r = DEFAULT_REGISTRY.get("OK")
    urls = {s.url for s in r.sources}
    assert any("CiteID=552969" in url for url in urls)
    assert not any("CiteID=365007" in url for url in urls)
    assert any("November 1, 2026" in text for text in r.review_disclosures)
    assert screen("OK", EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required


@pytest.mark.parametrize("entity", TYPES)
def test_oregon_foreign_renewal_and_conditional_certificate_evidence(entity):
    rule = DEFAULT_REGISTRY.get("OR").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.fee == Decimal("275") and "anniversary" in report.due_rule
    assert "$100" in report.notes
    assert "60 days" in rule.good_standing_evidence
    assert "web-verifiable" in rule.good_standing_evidence
    assert "fixed daily fine" in rule.qualification_penalty.description


def test_pennsylvania_reports_and_publication_are_entity_specific():
    r = DEFAULT_REGISTRY.get("PA")
    llc, corp = (r.for_entity(e) for e in TYPES)
    assert not r.registered_agent.private_appointment_required
    assert "CROP" in r.registered_agent.notes
    assert "September 30" in llc.annual_obligations[0].due_rule
    assert "June 30" in corp.annual_obligations[0].due_rule
    for rule in (llc, corp):
        assert rule.annual_obligations[0].fee == Decimal("7")
        assert "2025" in rule.annual_obligations[0].notes
        assert "2027" in rule.annual_obligations[0].notes
        assert "six months" in rule.annual_obligations[0].notes
    assert llc.initial_report is None
    assert "two newspapers" in corp.initial_report
    assert "legal journal" in corp.initial_report
    assert "Publication charges vary" in corp.initial_report
    assert "no home-jurisdiction good-standing certificate" in corp.good_standing_evidence


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch7_penalties_do_not_claim_exact_totals(state, entity):
    result = (
        DEFAULT_REGISTRY.get(state)
        .for_entity(entity)
        .qualification_penalty.estimate(date(2024, 1, 1), date(2026, 1, 1))
    )
    assert result.exact_amount is None and result.unresolved


@pytest.mark.parametrize("state", BATCH)
def test_batch7_unreviewed_lp_scope_does_not_inherit_safe_harbors(state):
    assert (
        screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen(state, EntityType.LP, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
