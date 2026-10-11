"""Regression cases for entity-specific rules in the fifth state batch."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("MI", "MN", "MS", "MO", "MT")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp",
    [
        ("MI", "50", "60"),
        ("MN", "185", "200"),
        ("MS", "250", "500"),
        ("MO", "105", "155"),
        ("MT", "70", "70"),
    ],
)
def test_batch5_initial_fees_include_correct_entity_and_filing_method(state, llc, corp):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.for_entity(EntityType.LLC).filing_fee == Decimal(llc)
    assert requirement.for_entity(EntityType.C_CORP).filing_fee == Decimal(corp)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch5_guides_replace_placeholders_and_keep_review_provenance(state, entity):
    requirement = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for text in (page.html, page.markdown):
        assert "Guide coming soon." not in text
        assert requirement.for_entity(entity).qualification_citation in text
        if state == "MS":
            assert "The primary review flag is satisfied" in text
            assert "third-party statutory reproduction" in text
            assert "Primary-publisher verification remains outstanding" not in text
    assert 'content="noindex, follow"' not in page.html
    assert requirement.rules_verified
    assert not requirement.verification_issues
    assert all(s.verified_on == date(2026, 10, 11) for s in requirement.sources)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch5_isolated_transaction_exemptions_stop_after_thirty_days(state, entity):
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.NOT_REQUIRED
    )
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


@pytest.mark.parametrize("entity", TYPES)
def test_minnesota_does_not_inherit_other_states_solicitation_exemptions(entity):
    assert (
        screen("MN", entity, Activity.SOLICITATION).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen("MN", entity, Activity.BANK_ACCOUNT).decision is QualificationDecision.NOT_REQUIRED
    )


def test_minnesota_income_producing_property_has_a_specific_llc_trigger():
    assert screen("MN", EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert (
        screen("MN", EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_minnesota_free_llc_and_paid_corporate_renewals_are_separate():
    requirement = DEFAULT_REGISTRY.get("MN")
    assert requirement.for_entity(EntityType.LLC).annual_obligations[0].fee == Decimal("0")
    corporate = requirement.for_entity(EntityType.C_CORP).annual_obligations[0]
    assert corporate.fee == Decimal("115")
    assert "$135" in corporate.notes
    assert "December 31" in corporate.due_rule


@pytest.mark.parametrize("entity", TYPES)
def test_michigan_current_report_fee_does_not_use_future_reduced_fee(entity):
    report = DEFAULT_REGISTRY.get("MI").for_entity(entity).annual_obligations[0]
    assert report.fee == Decimal("25")
    assert "2027" in report.notes


def test_michigan_llc_and_corporate_first_report_exceptions_differ():
    requirement = DEFAULT_REGISTRY.get("MI")
    assert "September 30" in requirement.for_entity(EntityType.LLC).annual_obligations[0].due_rule
    assert (
        "January 1 through May 15"
        in requirement.for_entity(EntityType.C_CORP).annual_obligations[0].due_rule
    )


@pytest.mark.parametrize("entity", TYPES)
def test_mississippi_foreign_reports_are_not_domestic_free_reports(entity):
    report = DEFAULT_REGISTRY.get("MS").for_entity(entity).annual_obligations[0]
    assert report.fee == Decimal("250" if entity is EntityType.LLC else "25")
    assert "April 15" in report.due_rule


@pytest.mark.parametrize("entity", TYPES)
def test_missouri_certificate_freshness_and_solicitation_review(entity):
    rule = DEFAULT_REGISTRY.get("MO").for_entity(entity)
    assert "60" in rule.good_standing_evidence
    assert (
        screen("MO", entity, Activity.SOLICITATION).decision
        is QualificationDecision.REVIEW_REQUIRED
    )


def test_missouri_initial_report_and_optional_biennial_election_are_visible():
    rule = DEFAULT_REGISTRY.get("MO").for_entity(EntityType.C_CORP)
    assert "30 days" in rule.initial_report
    report = rule.annual_obligations[0]
    assert report.fee == Decimal("20")
    assert "$40 online or $90 paper" in report.notes
    assert "parity" in report.notes
    assert not DEFAULT_REGISTRY.get("MO").for_entity(EntityType.LLC).annual_obligations


@pytest.mark.parametrize("entity", TYPES)
def test_montana_current_waiver_is_not_a_permanent_fee_promise(entity):
    report = DEFAULT_REGISTRY.get("MT").for_entity(entity).annual_obligations[0]
    assert report.fee == Decimal("0")
    assert "$35" in report.notes
    assert "Confirm the waiver" in report.notes
    assert "April 15" in report.due_rule


def test_montana_current_corporate_sanctions_do_not_import_llc_daily_fee():
    requirement = DEFAULT_REGISTRY.get("MT")
    assert (
        "$5 for each day"
        in requirement.for_entity(EntityType.LLC).qualification_penalty.description
    )
    corporate = requirement.for_entity(EntityType.C_CORP)
    assert corporate.qualification_citation == "MCA §§ 35-14-1502, 35-14-1503"
    assert (
        "does not specify a daily monetary penalty" in corporate.qualification_penalty.description
    )


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_batch5_penalties_do_not_claim_an_exact_total_without_assessment(state, entity):
    estimate = (
        DEFAULT_REGISTRY.get(state)
        .for_entity(entity)
        .qualification_penalty.estimate(date(2024, 1, 1), date(2026, 1, 1))
    )
    assert estimate.exact_amount is None
    assert estimate.unresolved


@pytest.mark.parametrize("state", BATCH)
def test_unreviewed_lp_safe_harbors_do_not_inherit_llc_rules(state):
    assert (
        screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        screen(state, EntityType.LP, Activity.ISOLATED_TRANSACTION, 30).decision
        is QualificationDecision.REVIEW_REQUIRED
    )
