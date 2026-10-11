"""Entity-specific regression checks for the sixth state batch."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("NE", "NV", "NH", "NJ", "NM")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp",
    [
        ("NE", "120", "110"),
        ("NV", "75", "75"),
        ("NH", "100", "100"),
        ("NJ", "100", "100"),
        ("NM", "100", "200"),
    ],
)
def test_batch6_base_fees_remain_entity_specific(state, llc, corp):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.for_entity(EntityType.LLC).filing_fee == Decimal(llc)
    assert requirement.for_entity(EntityType.C_CORP).filing_fee == Decimal(corp)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch6_active_guides_preserve_provenance_and_open_review_flags(state, entity):
    requirement = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for text in (page.html, page.markdown):
        assert "Guide coming soon." not in text
        assert requirement.for_entity(entity).qualification_citation in text
        for issue in requirement.verification_issues:
            assert issue in text
    assert 'content="noindex, follow"' not in page.html
    assert requirement.rules_verified is (state != "NM")
    assert all(s.verified_on == date(2026, 10, 11) for s in requirement.sources)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch6_isolated_transaction_limits_do_not_extend_to_day_31(state, entity):
    exempt = state != "NJ" or entity is EntityType.LLC
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision is (
        QualificationDecision.NOT_REQUIRED if exempt else QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


@pytest.mark.parametrize("entity", TYPES)
def test_nevada_narrow_solicitation_conditions_require_review(entity):
    assert (
        screen("NV", entity, Activity.SOLICITATION).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen("NV", entity, Activity.BANK_ACCOUNT).decision is QualificationDecision.NOT_REQUIRED
    )
    assert "shipment" in DEFAULT_REGISTRY.get("NV").for_entity(EntityType.LLC).threshold.notes


@pytest.mark.parametrize("activity", [Activity.SOLICITATION, Activity.INTERSTATE_COMMERCE])
def test_new_jersey_corporate_exemptions_do_not_inherit_llc_rules(activity):
    assert (
        screen("NJ", EntityType.C_CORP, activity).decision is QualificationDecision.REVIEW_REQUIRED
    )
    assert screen("NJ", EntityType.LLC, activity).decision is QualificationDecision.NOT_REQUIRED


@pytest.mark.parametrize("state", ["NE", "NJ"])
def test_income_producing_property_is_an_llc_trigger(state):
    assert screen(state, EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert (
        screen(state, EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_nebraska_biennial_cycles_and_variable_occupation_tax():
    r = DEFAULT_REGISTRY.get("NE")
    llc = r.for_entity(EntityType.LLC).annual_obligations[0]
    corp = r.for_entity(EntityType.C_CORP).annual_obligations[0]
    assert llc.cycle == corp.cycle == "biennial"
    assert "odd-numbered" in llc.due_rule and "April 1" in llc.due_rule
    assert llc.fee == Decimal("30") and "$25" in llc.notes
    assert "even-numbered" in corp.due_rule and "March 1" in corp.due_rule
    assert corp.fee is None and "$30,000" in corp.notes
    assert "$10 certificate" in r.notes[0]
    assert "60 days" in r.for_entity(EntityType.C_CORP).good_standing_evidence


@pytest.mark.parametrize(
    "entity,license_fee", [(EntityType.LLC, "200"), (EntityType.C_CORP, "500")]
)
def test_nevada_license_is_separate_from_annual_list(entity, license_fee):
    rule = DEFAULT_REGISTRY.get("NV").for_entity(entity)
    reports = rule.annual_obligations
    assert reports[0].fee == Decimal("150")
    assert reports[1].fee == Decimal(license_fee)
    assert "exemption" in reports[1].due_rule
    assert "$150" in rule.initial_report
    assert (
        "not a general"
        in DEFAULT_REGISTRY.get("NV").for_entity(EntityType.LLC).qualification_penalty.description
    )
    if entity is EntityType.C_CORP:
        assert "minimum" in reports[0].notes
        assert "at most $35,000" in DEFAULT_REGISTRY.get("NV").notes[0]


@pytest.mark.parametrize("entity", TYPES)
def test_new_hampshire_report_exception_and_affirmation(entity):
    rule = DEFAULT_REGISTRY.get("NH").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.fee == Decimal("100")
    assert "December 1" in report.due_rule and "April 1" in report.due_rule
    assert "$50" in report.notes and "$2" in report.notes
    assert "affirms" in rule.good_standing_evidence


def test_new_jersey_current_fees_and_corporate_certificate_requirement():
    r = DEFAULT_REGISTRY.get("NJ")
    for entity in TYPES:
        assert r.for_entity(entity).annual_obligations[0].fee == Decimal("75")
    assert "July 1, 2026" in r.notes[0]
    assert "30 days" in r.for_entity(EntityType.C_CORP).good_standing_evidence
    assert "does not prescribe" in r.for_entity(EntityType.LLC).good_standing_evidence
    assert "NJ-REG" in r.notes[0]


def test_new_mexico_reporting_and_penalties_do_not_cross_entity_types():
    r = DEFAULT_REGISTRY.get("NM")
    llc, corp = (r.for_entity(e) for e in TYPES)
    report = corp.annual_obligations[0]
    assert report.cycle == "biennial" and report.fee == Decimal("25")
    assert "fourth month" in report.due_rule
    assert "30 days" in corp.initial_report
    assert not llc.annual_obligations
    assert "no periodic or annual report requirement" in llc.threshold.notes
    assert "periodic-report fee is $0" in llc.threshold.notes
    assert "one-time $50" in llc.threshold.notes
    assert "up to $200" in llc.qualification_penalty.description
    assert "$200 for each offense" in corp.qualification_penalty.description
    for rule in (llc, corp):
        assert "30 days" in rule.good_standing_evidence
        assert "acceptance" in rule.good_standing_evidence
    assert "minimum" in r.notes[0]
    assert any("portal totals" in issue for issue in r.verification_issues)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch6_penalties_require_manual_assessment(state, entity):
    estimate = (
        DEFAULT_REGISTRY.get(state)
        .for_entity(entity)
        .qualification_penalty.estimate(date(2024, 1, 1), date(2026, 1, 1))
    )
    assert estimate.exact_amount is None and estimate.unresolved


@pytest.mark.parametrize("state", BATCH)
def test_batch6_lp_scope_does_not_inherit_reviewed_llc_exemptions(state):
    assert (
        screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen(state, EntityType.LP, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_nevada_corporate_publication_is_separate_from_lists_and_licenses():
    requirement = DEFAULT_REGISTRY.get("NV")
    corporate = requirement.for_entity(EntityType.C_CORP).annual_obligations
    publication = corporate[2]
    assert publication.citation == "NRS § 80.190"
    assert publication.fee is None
    assert "end of March" in publication.due_rule
    assert "third month" in publication.due_rule
    assert "two issues" in publication.notes and "$100" in publication.notes
    assert len(requirement.for_entity(EntityType.LLC).annual_obligations) == 2
    assert "$11,125" in corporate[0].notes


@pytest.mark.parametrize("state", ["NJ", "NM"])
def test_accepted_justia_review_is_disclosed_without_changing_publisher_provenance(state):
    requirement = DEFAULT_REGISTRY.get(state)
    assert not any("primary" in issue.lower() for issue in requirement.verification_issues)
    for entity in TYPES:
        page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
            state, entity
        )
        for text in (page.html, page.markdown):
            assert "The primary review flag is satisfied" in text
            assert "secondary publisher" in text
    assert any("law.justia.com" in source.url for source in requirement.sources)


def test_new_mexico_llc_reporting_resolution_keeps_foreign_fee_and_corporate_report():
    requirement = DEFAULT_REGISTRY.get("NM")
    llc = requirement.for_entity(EntityType.LLC)
    assert llc.filing_fee == Decimal("100")
    assert not llc.annual_obligations
    assert llc.initial_report is None
    assert not any("report" in issue.lower() for issue in requirement.verification_issues)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        "NM", EntityType.LLC
    )
    for text in (page.html, page.markdown):
        assert "$0 periodic-report fee" in text
        assert "formation filing is $50" in text
        assert "foreign registration is $100" in text
    assert requirement.for_entity(EntityType.C_CORP).annual_obligations[0].fee == Decimal("25")
