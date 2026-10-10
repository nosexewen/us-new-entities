from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest
from us_new_entities.models import EntityType, PenaltyPeriod, PenaltyPolicy, period_count
from us_new_entities.rules.registry import DEFAULT_REGISTRY


def policy(**changes):
    values = {
        "citation": "Example statute",
        "description": "Test calculation policy",
        "amount_min": Decimal("20"),
        "amount_max": Decimal("20"),
        "period": PenaltyPeriod.DAY,
    }
    return PenaltyPolicy(**(values | changes))


@pytest.mark.parametrize(
    ("start", "end", "period", "expected"),
    [
        (date(2025, 12, 31), date(2026, 1, 1), PenaltyPeriod.DAY, 1),
        (date(2025, 12, 31), date(2026, 1, 1), PenaltyPeriod.CALENDAR_YEAR, 1),
        (date(2025, 12, 31), date(2026, 1, 2), PenaltyPeriod.CALENDAR_YEAR, 2),
        (date(2025, 1, 1), date(2026, 1, 1), PenaltyPeriod.CALENDAR_YEAR, 1),
        (date(2024, 2, 29), date(2025, 2, 27), PenaltyPeriod.STARTED_YEAR, 1),
        (date(2024, 2, 29), date(2025, 2, 28), PenaltyPeriod.STARTED_YEAR, 1),
        (date(2024, 2, 29), date(2025, 3, 1), PenaltyPeriod.STARTED_YEAR, 2),
        (date(2025, 12, 31), date(2026, 1, 2), PenaltyPeriod.STARTED_YEAR, 1),
        (date(2024, 1, 31), date(2024, 2, 28), PenaltyPeriod.FULL_MONTH, 0),
        (date(2024, 1, 31), date(2024, 2, 29), PenaltyPeriod.FULL_MONTH, 1),
        (date(2025, 1, 31), date(2025, 2, 28), PenaltyPeriod.FULL_MONTH, 1),
        (date(2025, 1, 31), date(2025, 2, 28), PenaltyPeriod.STARTED_MONTH, 1),
        (date(2025, 1, 31), date(2025, 3, 1), PenaltyPeriod.STARTED_MONTH, 2),
        (date(2025, 1, 1), date(2025, 1, 2), PenaltyPeriod.ONCE, 1),
    ],
)
def test_calendar_and_anniversary_period_boundaries(start, end, period, expected):
    assert period_count(start, end, period) == expected


@pytest.mark.parametrize("period", list(PenaltyPeriod))
def test_same_day_cure_has_zero_elapsed_periods(period):
    assert period_count(date(2025, 1, 1), date(2025, 1, 1), period) == 0


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (date(2025, 1, 2), date(2025, 1, 1)),
        ("2025-01-01", date(2025, 1, 2)),
        (date(2025, 1, 1), datetime(2025, 1, 2)),
    ],
)
def test_invalid_penalty_date_intervals_are_rejected(start, end):
    with pytest.raises(ValueError):
        policy().estimate(start, end)


def test_daily_penalty_excludes_cure_date_and_caps_accumulation():
    start = date(2025, 1, 1)
    penalty = policy(cap=Decimal("100"))
    assert penalty.estimate(start, start + timedelta(days=2)).exact_amount == Decimal("40.00")
    assert penalty.estimate(start, start + timedelta(days=5)).exact_amount == Decimal("100.00")
    assert penalty.estimate(start, start + timedelta(days=500)).exact_amount == Decimal("100.00")


def test_cap_applies_to_both_bounds_of_a_statutory_range():
    estimate = policy(amount_max=Decimal("50"), cap=Decimal("100")).estimate(
        date(2025, 1, 1),
        date(2025, 1, 4),
    )
    assert (estimate.minimum, estimate.maximum) == (Decimal("60.00"), Decimal("100.00"))
    assert estimate.exact_amount is None


def test_unquantified_sanctions_are_not_zero_dollar_safe_results():
    estimate = policy(amount_min=None, amount_max=None).estimate(
        date(2025, 1, 1),
        date(2025, 2, 1),
    )
    assert estimate.minimum is None
    assert estimate.maximum is None
    assert estimate.exact_amount is None
    assert estimate.interest is None
    assert estimate.unresolved


def test_known_base_with_unquantified_taxes_is_not_an_exact_total():
    estimate = policy(unquantified_components=("Unpaid taxes",)).estimate(
        date(2025, 1, 1),
        date(2025, 1, 2),
    )
    assert estimate.minimum == estimate.maximum == Decimal("20.00")
    assert estimate.exact_amount is None
    assert estimate.unresolved == ("Unpaid taxes",)


def test_simple_interest_uses_tax_plus_penalty_without_interest_on_interest():
    estimate = policy(
        amount_min=Decimal("200"),
        amount_max=Decimal("200"),
        period=PenaltyPeriod.ONCE,
        interest_monthly_rate=Decimal("0.015"),
        interest_on_penalty=True,
    ).estimate(date(2025, 1, 1), date(2025, 4, 1), unpaid_tax=Decimal("300"))
    assert estimate.interest == Decimal("22.50")
    assert estimate.minimum == estimate.maximum == Decimal("222.50")
    assert estimate.exact_amount == Decimal("222.50")


def test_missing_interest_principal_keeps_estimate_unresolved():
    estimate = policy(interest_monthly_rate=Decimal("0.015")).estimate(
        date(2025, 1, 1),
        date(2025, 2, 1),
    )
    assert estimate.interest is None
    assert estimate.exact_amount is None
    assert any("unpaid_tax" in item for item in estimate.unresolved)


def test_currency_rounding_is_decimal_half_up():
    estimate = policy(amount_min=Decimal("0.005"), amount_max=Decimal("0.005")).estimate(
        date(2025, 1, 1),
        date(2025, 1, 2),
    )
    assert estimate.exact_amount == Decimal("0.01")


@pytest.mark.parametrize(
    "changes",
    [
        {"amount_min": Decimal("-1")},
        {"amount_max": Decimal("NaN")},
        {"amount_min": Decimal("Infinity")},
        {"amount_min": 20.0},
        {"amount_max": None},
        {"amount_min": Decimal("21")},
        {"cap": Decimal("-1")},
        {"interest_monthly_rate": Decimal("-0.01")},
        {"interest_monthly_rate": Decimal("NaN")},
        {"interest_monthly_rate": None},
        {"compound_interest": "false"},
        {"interest_on_penalty": "false"},
        {"grace_days": -1},
        {"grace_days": True},
        {"grace_days": 1.5},
        {"period": "weekly"},
        {"interest_period": PenaltyPeriod.DAY},
    ],
)
def test_invalid_penalty_declarations_are_rejected(changes):
    with pytest.raises(ValueError):
        policy(**changes)


@pytest.mark.parametrize("tax", [Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 300.0])
def test_invalid_tax_principal_is_rejected(tax):
    with pytest.raises(ValueError):
        policy().estimate(date(2025, 1, 1), date(2025, 2, 1), unpaid_tax=tax)


def test_california_corporation_willful_daily_sanction_and_lp_cap():
    state = DEFAULT_REGISTRY.get("CA")
    start = date(2025, 1, 1)
    corp = state.for_entity(EntityType.C_CORP).qualification_penalty
    lp = state.for_entity(EntityType.LP).qualification_penalty
    assert corp.period is PenaltyPeriod.DAY
    assert (corp.amount_min, corp.amount_max) == (Decimal("0"), Decimal("20"))
    assert "willful" in (corp.description + corp.assessment).lower()
    corp_estimate = corp.estimate(start, start + timedelta(days=10))
    assert corp_estimate.minimum == Decimal("0.00")
    assert corp_estimate.maximum == Decimal("200.00")
    assert corp_estimate.exact_amount is None
    assert lp.cap == Decimal("10000")
    assert lp.estimate(start, start + timedelta(days=600)).maximum == Decimal("10000.00")
    llc = state.for_entity(EntityType.LLC).qualification_penalty.estimate(
        start,
        start + timedelta(days=10),
    )
    assert llc.exact_amount is None
    assert llc.unresolved


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_texas_90_day_grace_and_calendar_year_parts(entity_type):
    penalty = DEFAULT_REGISTRY.get("TX").for_entity(entity_type).qualification_penalty
    start = date(2025, 10, 1)
    assert penalty.grace_days == 90
    assert penalty.period is PenaltyPeriod.CALENDAR_YEAR
    grace_estimate = penalty.estimate(start, start + timedelta(days=90))
    assert grace_estimate.minimum == grace_estimate.maximum == Decimal("0.00")
    if penalty.unquantified_components:
        assert grace_estimate.exact_amount is None
        assert grace_estimate.unresolved
    # Once the grace is exceeded, the whole unregistered interval controls;
    # qualification on Jan 1 does not count a new calendar year of business.
    assert penalty.estimate(start, date(2025, 12, 31)).minimum == Decimal("750.00")
    assert penalty.estimate(start, date(2026, 1, 1)).minimum == Decimal("750.00")
    assert penalty.estimate(start, date(2026, 1, 2)).minimum == Decimal("1500.00")


def test_delaware_corporate_fine_is_per_offense_not_per_year():
    penalty = DEFAULT_REGISTRY.get("DE").for_entity(EntityType.C_CORP).qualification_penalty
    assert penalty.period is PenaltyPeriod.ONCE
    estimate = penalty.estimate(date(2020, 1, 1), date(2026, 1, 1))
    assert (estimate.minimum, estimate.maximum) == (Decimal("200.00"), Decimal("500.00"))
    assert estimate.periods == 1
    assert estimate.exact_amount is None


@pytest.mark.parametrize("entity_type", [EntityType.LLC, EntityType.LP])
def test_delaware_annual_tax_late_penalty_has_simple_monthly_interest(entity_type):
    obligations = DEFAULT_REGISTRY.get("DE").for_entity(entity_type).annual_obligations
    penalties = [item.late_penalty for item in obligations if item.late_penalty is not None]
    assert len(penalties) == 1
    penalty = penalties[0]
    assert penalty.amount_min == penalty.amount_max == Decimal("200")
    assert penalty.interest_monthly_rate == Decimal("0.015")
    assert penalty.interest_on_penalty is True
    assert penalty.compound_interest is False
    estimate = penalty.estimate(date(2025, 6, 2), date(2025, 9, 2), unpaid_tax=Decimal("400"))
    assert estimate.interest == Decimal("27.00")
    assert estimate.minimum == estimate.maximum == Decimal("227.00")


@pytest.mark.parametrize("entity_type", [EntityType.LLC, EntityType.LP])
def test_delaware_unregistered_alternative_entities_have_a_sourced_annual_penalty(entity_type):
    penalty = DEFAULT_REGISTRY.get("DE").for_entity(entity_type).qualification_penalty
    assert penalty.period is PenaltyPeriod.STARTED_YEAR
    assert penalty.amount_min == penalty.amount_max == Decimal("200")
    first_year = penalty.estimate(date(2024, 2, 29), date(2025, 2, 28))
    next_year = penalty.estimate(date(2024, 2, 29), date(2025, 3, 1))
    assert first_year.minimum == first_year.maximum == Decimal("200.00")
    assert next_year.minimum == next_year.maximum == Decimal("400.00")
    assert first_year.exact_amount is None


def test_delaware_conflicting_official_annual_report_late_fee_is_not_an_exact_total():
    obligation = DEFAULT_REGISTRY.get("DE").for_entity(EntityType.C_CORP).annual_obligations[0]
    estimate = obligation.late_penalty.estimate(date(2026, 7, 1), date(2026, 7, 2))
    assert estimate.minimum == estimate.maximum == Decimal("200.00")
    assert estimate.exact_amount is None
    assert any("conflict" in issue.lower() for issue in estimate.unresolved)


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_florida_annual_late_fee_is_flat_not_a_daily_or_yearly_multiplier(entity_type):
    obligations = DEFAULT_REGISTRY.get("FL").for_entity(entity_type).annual_obligations
    penalties = [item.late_penalty for item in obligations if item.late_penalty is not None]
    assert len(penalties) == 1
    estimate = penalties[0].estimate(date(2025, 5, 2), date(2026, 9, 1))
    assert estimate.minimum == estimate.maximum == Decimal("400.00")
    assert estimate.periods == 1


def test_florida_lp_qualification_penalty_is_unknown_not_invented():
    penalty = DEFAULT_REGISTRY.get("FL").for_entity(EntityType.LP).qualification_penalty
    assert penalty.estimate(date(2025, 1, 1), date(2025, 2, 1)).exact_amount is None
    assert penalty.amount_min is None


@pytest.mark.parametrize("entity_type", [EntityType.LLC, EntityType.C_CORP])
def test_florida_qualification_range_counts_anniversary_year_parts(entity_type):
    penalty = DEFAULT_REGISTRY.get("FL").for_entity(entity_type).qualification_penalty
    one_period = penalty.estimate(date(2024, 2, 29), date(2025, 2, 28))
    two_periods = penalty.estimate(date(2024, 2, 29), date(2025, 3, 1))
    assert (one_period.minimum, one_period.maximum) == (Decimal("500.00"), Decimal("1000.00"))
    assert (two_periods.minimum, two_periods.maximum) == (Decimal("1000.00"), Decimal("2000.00"))
    assert one_period.exact_amount is None
    if entity_type is EntityType.C_CORP:
        assert penalty.assessment == "court_ordered_only"


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_wyoming_additional_arrears_prevent_exact_total(entity_type):
    penalty = DEFAULT_REGISTRY.get("WY").for_entity(entity_type).qualification_penalty
    estimate = penalty.estimate(date(2025, 1, 1), date(2025, 2, 1))
    assert estimate.minimum == estimate.maximum == Decimal("5000.00")
    assert estimate.unresolved
    assert estimate.exact_amount is None
