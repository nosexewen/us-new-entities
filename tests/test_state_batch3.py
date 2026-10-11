"""Regression cases for the third batch's statutory and administrative distinctions."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("CT", "HI", "ID", "IN", "IA")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp",
    [
        ("CT", "120", "385"),
        ("HI", "51", "51"),
        ("ID", "100", "100"),
        ("IN", "125", "125"),
        ("IA", "100", "100"),
    ],
)
def test_qualification_fees_include_mandatory_components_and_identify_filing_method(
    state, llc, corp
):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.for_entity(EntityType.LLC).filing_fee == Decimal(llc)
    assert requirement.for_entity(EntityType.C_CORP).filing_fee == Decimal(corp)
    notes = " ".join(requirement.notes)
    if state == "CT":
        assert "$285" in notes and "$435" in notes
    elif state == "HI":
        assert "$1 State Archives" in notes
    elif state == "ID":
        assert "$120" in notes and "$20" in notes
    elif state == "IN":
        assert "$75" in notes and "paper" in notes


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_requested_guides_are_populated_with_dated_official_sources(state, entity):
    requirement = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for text in (page.html, page.markdown):
        assert "Guide coming soon." not in text
        assert requirement.for_entity(entity).qualification_citation in text
    assert 'content="noindex, follow"' not in page.html
    assert all(s.verified_on == date(2026, 10, 11) for s in requirement.sources)
    assert not any("justia.com" in s.url for s in requirement.sources)


@pytest.mark.parametrize(
    "state,entity",
    [
        ("CT", EntityType.LLC),
        ("ID", EntityType.LLC),
        ("ID", EntityType.C_CORP),
        ("IA", EntityType.LLC),
        ("IA", EntityType.C_CORP),
    ],
)
def test_current_statutes_without_an_isolated_transaction_day_limit(state, entity):
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision is (
        QualificationDecision.NOT_REQUIRED
    )


@pytest.mark.parametrize(
    "state,entity",
    [
        ("CT", EntityType.C_CORP),
        ("HI", EntityType.LLC),
        ("HI", EntityType.C_CORP),
        ("IN", EntityType.LLC),
        ("IN", EntityType.C_CORP),
    ],
)
def test_thirty_day_statutory_boundaries_are_preserved(state, entity):
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision is (
        QualificationDecision.NOT_REQUIRED
    )
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


def test_hawaii_income_producing_property_trigger_is_llc_specific():
    assert screen("HI", EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert screen("HI", EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


def test_iowa_biennial_report_parity_fees_and_current_section_numbers():
    state = DEFAULT_REGISTRY.get("IA")
    llc = state.for_entity(EntityType.LLC).annual_obligations[0]
    corp = state.for_entity(EntityType.C_CORP).annual_obligations[0]
    assert llc.cycle == corp.cycle == "biennial"
    assert "odd-numbered" in llc.due_rule and "even-numbered" in corp.due_rule
    assert llc.fee == Decimal("30") and "$45" in llc.notes
    assert corp.fee == Decimal("60")
    assert "489.212" in llc.citation and "490.1621" in corp.citation


@pytest.mark.parametrize("entity", TYPES)
def test_indiana_reports_disclose_both_statutory_and_published_online_prices(entity):
    rule = DEFAULT_REGISTRY.get("IN").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.cycle == "biennial" and report.fee == Decimal("50")
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate("IN", entity)
    for text in (page.html, page.markdown):
        assert "$20" in text and "$32" in text and "resolved by disclosure" in text
    policy = rule.qualification_penalty
    assert "$10,000" in policy.description
    assert policy.estimate(date(2024, 1, 1), date(2026, 1, 1)).exact_amount is None


@pytest.mark.parametrize("entity", TYPES)
def test_connecticut_monthly_penalty_exemption_and_type_specific_report_deadlines(entity):
    rule = DEFAULT_REGISTRY.get("CT").for_entity(entity)
    assert "$300" in rule.qualification_penalty.description
    assert "90 days" in rule.qualification_penalty.description
    report = rule.annual_obligations[0]
    if entity == EntityType.LLC:
        assert report.fee == Decimal("80") and "March 31" in report.due_rule
    else:
        assert report.fee == Decimal("435") and "$285" in report.notes
        assert "first annual report" in report.due_rule


@pytest.mark.parametrize("state,age", [("HI", "60 days"), ("IN", "60 days"), ("IA", "90 days")])
@pytest.mark.parametrize("entity", TYPES)
def test_certificate_freshness_comes_from_the_entity_specific_instructions(state, age, entity):
    assert age in DEFAULT_REGISTRY.get(state).for_entity(entity).good_standing_evidence


@pytest.mark.parametrize("state", ("CT", "HI", "IA"))
def test_unreviewed_lp_safe_harbors_are_not_inherited_from_llc_or_corporation(state):
    assert screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )
    assert "LP" in " ".join(DEFAULT_REGISTRY.get(state).review_disclosures)


def test_unconfirmed_idaho_report_fee_is_not_reported_as_zero():
    for entity in TYPES:
        report = DEFAULT_REGISTRY.get("ID").for_entity(entity).annual_obligations[0]
        assert report.fee is None
        assert "final day" in report.due_rule and "one year" in report.due_rule
