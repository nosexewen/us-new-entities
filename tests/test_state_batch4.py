"""Regression cases for current fees, safe harbors and report cycles in batch four."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("KS", "KY", "LA", "ME", "MA")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp",
    [
        ("KS", "115", "115"),
        ("KY", "90", "90"),
        ("LA", "185", "155"),
        ("ME", "250", "250"),
        ("MA", "500", "400"),
    ],
)
def test_current_qualification_prices_are_entity_specific(state, llc, corp):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.for_entity(EntityType.LLC).filing_fee == Decimal(llc)
    assert requirement.for_entity(EntityType.C_CORP).filing_fee == Decimal(corp)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_requested_guides_replace_placeholders_with_official_dated_rules(state, entity):
    requirement = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for text in (page.html, page.markdown):
        assert "Guide coming soon." not in text
        assert requirement.for_entity(entity).qualification_citation in text
    assert 'content="noindex, follow"' not in page.html
    assert requirement.rules_verified
    assert all(s.verified_on == date(2026, 10, 11) for s in requirement.sources)
    assert not any("justia.com" in s.url for s in requirement.sources)


@pytest.mark.parametrize("state", ("KS", "KY", "LA", "ME"))
@pytest.mark.parametrize("entity", TYPES)
def test_thirty_day_isolated_transaction_limits_are_not_removed(state, entity):
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision is (
        QualificationDecision.NOT_REQUIRED
    )
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


def test_massachusetts_corporate_isolated_transactions_have_no_day_limit():
    assert screen("MA", EntityType.C_CORP, Activity.ISOLATED_TRANSACTION, 31).decision is (
        QualificationDecision.NOT_REQUIRED
    )
    assert screen(
        "MA", EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY
    ).qualification_required


@pytest.mark.parametrize(
    "activity", (Activity.BANK_ACCOUNT, Activity.INTERSTATE_COMMERCE, Activity.ISOLATED_TRANSACTION)
)
def test_massachusetts_llc_exemptions_are_not_inherited_from_the_corporation_act(activity):
    assert screen("MA", EntityType.LLC, activity, 30).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


@pytest.mark.parametrize("entity", TYPES)
def test_kansas_biennial_reporting_and_replacement_of_certificate_requirement(entity):
    rule = DEFAULT_REGISTRY.get("KS").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.cycle == "biennial" and report.fee == Decimal("90")
    assert "April 15" in report.due_rule and "parity" in report.due_rule
    assert "$110 paper" in report.notes
    assert "penalty of perjury" in rule.good_standing_evidence
    assert "repealed 90-day" in rule.good_standing_evidence
    assert "17-7931" in rule.qualification_citation


@pytest.mark.parametrize("entity", TYPES)
def test_kentucky_report_calendar_and_daily_qualification_penalty(entity):
    rule = DEFAULT_REGISTRY.get("KY").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.cycle == "annual" and report.fee == Decimal("15")
    assert "June 30" in report.due_rule and "year after" in report.due_rule
    assert "$2 for each day" in rule.qualification_penalty.description
    assert "do not mandate a home-state certificate" in rule.good_standing_evidence


@pytest.mark.parametrize("entity", TYPES)
def test_louisiana_october_2026_prices_supersede_old_forms(entity):
    rule = DEFAULT_REGISTRY.get("LA").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.fee == Decimal("35")
    assert "anniversary" in report.due_rule
    assert "October 1, 2026" in report.notes and "$5" in report.notes
    assert "90 days" in rule.good_standing_evidence
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate("LA", entity)
    for text in (page.html, page.markdown):
        assert "$185/$155" in text and "$150" in text and "$155" in text
        assert "resolved by disclosure" in text


@pytest.mark.parametrize("entity", TYPES)
def test_maine_foreign_report_fees_and_penalties_are_not_domestic_prices(entity):
    rule = DEFAULT_REGISTRY.get("ME").for_entity(entity)
    report = rule.annual_obligations[0]
    assert report.fee == Decimal("150") and "June 1" in report.due_rule
    assert "$50" in report.notes
    assert "$500 for each year or portion" in rule.qualification_penalty.description
    assert "90 days" in rule.good_standing_evidence
    if entity == EntityType.LLC:
        assert "collection" not in rule.qualification_citation
        assert "collect its debts" in rule.consequences[0]


def test_massachusetts_llc_and_corporate_report_deadlines_and_filing_methods_differ():
    state = DEFAULT_REGISTRY.get("MA")
    llc = state.for_entity(EntityType.LLC)
    corp = state.for_entity(EntityType.C_CORP)
    assert llc.annual_obligations[0].fee == Decimal("500")
    assert "anniversary" in llc.annual_obligations[0].due_rule
    assert "$520" in llc.annual_obligations[0].notes
    assert corp.annual_obligations[0].fee == Decimal("125")
    assert "two and one-half months" in corp.annual_obligations[0].due_rule
    assert "$100" in corp.annual_obligations[0].notes
    assert "not more than $500" in llc.qualification_penalty.description
    assert "monthly" in corp.qualification_penalty.description
    assert "first 10 days" in corp.qualification_penalty.description


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_historical_penalties_require_assessment_instead_of_an_invented_exact_total(state, entity):
    policy = DEFAULT_REGISTRY.get(state).for_entity(entity).qualification_penalty
    estimate = policy.estimate(date(2024, 1, 1), date(2026, 1, 1))
    assert estimate.exact_amount is None and estimate.unresolved


@pytest.mark.parametrize("entity", TYPES)
def test_kansas_fee_discrepancy_preserves_both_official_figures(entity):
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate("KS", entity)
    for text in (page.html, page.markdown):
        assert "7-50-1" in text and "$75" in text and "$115" in text
        assert "resolved by disclosure" in text


@pytest.mark.parametrize("state", ("LA", "ME", "MA"))
def test_partial_lp_entries_require_manual_activity_review(state):
    assert screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )
    assert not DEFAULT_REGISTRY.get(state).for_entity(EntityType.LP).annual_obligations
