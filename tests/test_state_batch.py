"""Regression cases for the October 11 state batch's entity-specific distinctions."""

from datetime import date
from decimal import Decimal

import pytest
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import (
    Activity,
    BusinessPresence,
    ComplianceAudit,
    Entity,
    EntityStatus,
    EntityType,
    QualificationDecision,
)
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("GA", "IL", "NY", "NC", "WA")


def screen(state, entity_type=EntityType.LLC, activity=Activity.OFFICE, days=None):
    return ComplianceAudit(
        Entity(
            legal_name="Batch Example",
            entity_type=entity_type,
            domestic_state="DE",
            formation_date=date(2020, 1, 1),
            sos_entity_id="batch-001",
            status=EntityStatus.GOOD_STANDING,
        ),
        state,
        BusinessPresence({activity}, isolated_transaction_days=days),
        as_of=date(2026, 10, 11),
    ).evaluate()


@pytest.mark.parametrize(
    "state,fees",
    [
        ("GA", ("235", "235", "235")),
        ("IL", ("150", "150", "150")),
        ("NY", ("250", "225", "200")),
        ("NC", ("250", "250", "50")),
        ("WA", ("180", "180", "180")),
    ],
)
def test_batch_base_fees_are_distinct_from_taxes_service_and_publication_charges(state, fees):
    requirement = DEFAULT_REGISTRY.get(state)
    for entity_type, amount in zip(
        (EntityType.LLC, EntityType.C_CORP, EntityType.LP), fees, strict=True
    ):
        assert requirement.for_entity(entity_type).filing_fee == Decimal(amount)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_populated_batch_pages_replace_placeholders_with_source_backed_rules(state, entity_type):
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity_type
    )
    assert "GovernmentService" in page.html
    assert "Guide coming soon." not in page.html
    assert 'content="noindex, follow"' not in page.html
    assert "2026-10-11" in page.html
    assert DEFAULT_REGISTRY.get(state).rules_verified == (state != "GA")


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_new_york_authority_does_not_require_a_private_agent(entity_type):
    result = screen("NY", entity_type)
    assert result.qualification_required
    assert result.foreign_filing_required
    assert result.registered_agent_required is False
    assert result.registered_agent_appointment_required is False
    assert not any("Appoint an eligible registered agent" in r for r in result.remedies)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        "NY", entity_type
    )
    assert "a separate private registered agent is optional" in page.html


def test_new_york_publication_and_biennial_reporting_are_type_specific():
    state = DEFAULT_REGISTRY.get("NY")
    for entity_type in (EntityType.LLC, EntityType.LP):
        notice = state.for_entity(entity_type).initial_report
        assert "120 days" in notice and "$50" in notice and "six successive weeks" in notice
    assert state.for_entity(EntityType.C_CORP).initial_report is None
    assert not state.for_entity(EntityType.LP).annual_obligations
    for entity_type in (EntityType.LLC, EntityType.C_CORP):
        report = state.for_entity(entity_type).annual_obligations[0]
        assert report.cycle == "biennial" and report.fee == Decimal("9")


@pytest.mark.parametrize(
    "entity_type,limit", [(EntityType.LLC, 120), (EntityType.C_CORP, 120), (EntityType.LP, 30)]
)
def test_illinois_isolated_transaction_boundaries_are_entity_specific(entity_type, limit):
    assert (
        screen("IL", entity_type, Activity.ISOLATED_TRANSACTION, limit).decision
        is QualificationDecision.NOT_REQUIRED
    )
    assert (
        screen("IL", entity_type, Activity.ISOLATED_TRANSACTION, limit + 1).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_illinois_income_producing_property_rule_is_lp_specific():
    assert screen("IL", EntityType.LP, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert (
        screen("IL", EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_north_carolina_calendar_month_safe_harbor_is_not_approximated_as_days():
    assert (
        screen("NC", activity=Activity.ISOLATED_TRANSACTION, days=180).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    state = DEFAULT_REGISTRY.get("NC")
    assert not state.for_entity(EntityType.LP).annual_obligations
    assert state.for_entity(EntityType.LLC).annual_obligations[0].fee == Decimal("200")
    assert "$500" in state.for_entity(EntityType.LP).qualification_penalty.description
    for entity_type in (EntityType.LLC, EntityType.C_CORP):
        policy = state.for_entity(entity_type).qualification_penalty
        assert "$10 per day" in policy.description and "$1,000" in policy.description
        assert policy.estimate(date(2024, 1, 1), date(2026, 1, 1)).exact_amount is None


def test_georgia_unreviewed_exemptions_require_manual_review():
    assert (
        screen("GA", activity=Activity.BANK_ACCOUNT).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_washington_30_day_safe_harbor_and_annual_report_fee():
    assert (
        screen("WA", activity=Activity.ISOLATED_TRANSACTION, days=30).decision
        is QualificationDecision.NOT_REQUIRED
    )
    assert (
        screen("WA", activity=Activity.ISOLATED_TRANSACTION, days=31).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    for entity_type in EntityType:
        report = DEFAULT_REGISTRY.get("WA").for_entity(entity_type).annual_obligations[0]
        assert report.fee == Decimal("70")
        assert "includes online processing" in report.notes


@pytest.mark.parametrize("state", ("CA", "DE", "FL", "IL", "NY", "NC", "WA"))
def test_resolved_reviews_have_dated_sources_and_no_open_evidence_flags(state):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.rules_verified
    assert not requirement.verification_issues
    assert all(source.verified_on is not None for source in requirement.sources)


def test_georgia_disclosure_does_not_resolve_separate_primary_law_gap():
    requirement = DEFAULT_REGISTRY.get("GA")
    assert not requirement.rules_verified
    assert len(requirement.verification_issues) == 1
    assert "safe-harbor" in requirement.verification_issues[0]
    assert requirement.review_disclosures


@pytest.mark.parametrize("state", ("DE", "GA"))
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_resolved_fee_disclosures_remain_visible_in_html_and_markdown(state, entity_type):
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity_type
    )
    for text in (page.html, page.markdown):
        assert "Noted discrepancy" in text
        assert "resolved by disclosure" in text
        if state == "DE":
            assert "$200" in text and "$250" in text
        else:
            assert "$500 per year or part-year" in text
            assert "$235 and $60" in text
    assert DEFAULT_REGISTRY.get(state).review_disclosures


def test_reviewed_certificate_freshness_is_entity_specific():
    il = DEFAULT_REGISTRY.get("IL")
    assert "60 days" in il.for_entity(EntityType.LLC).good_standing_evidence
    assert "90 days" in il.for_entity(EntityType.C_CORP).good_standing_evidence
    lp = il.for_entity(EntityType.LP).good_standing_evidence
    assert "no numeric age limit" in lp and "general partner" in lp and "30 days" in lp
    nc = DEFAULT_REGISTRY.get("NC")
    for entity_type in (EntityType.LLC, EntityType.C_CORP):
        assert "less than six months" in nc.for_entity(entity_type).good_standing_evidence
        assert ".pdf" in nc.for_entity(entity_type).forms[0].url
    assert "does not request" in nc.for_entity(EntityType.LP).good_standing_evidence
    ga = DEFAULT_REGISTRY.get("GA")
    for entity_type in (EntityType.LLC, EntityType.LP):
        assert "No certified home-state" in ga.for_entity(entity_type).good_standing_evidence


def test_illinois_franchise_tax_and_new_york_disclosure_scope_are_documented():
    assert "$10,000" in " ".join(DEFAULT_REGISTRY.get("IL").notes)
    assert "2% per month" in " ".join(DEFAULT_REGISTRY.get("IL").notes)
    ny = DEFAULT_REGISTRY.get("NY").for_entity(EntityType.LLC)
    assert "foreign-country law" in " ".join(ny.consequences)
    assert "another US state" in " ".join(ny.consequences)
