"""Declarative rules and deterministic monetary estimates, without implied legal findings."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum
from types import MappingProxyType

from .entity import EntityType, normalize_state

CENT = Decimal("0.01")


class Activity(StrEnum):
    OFFICE = "operating_office"
    LOCAL_SERVICES = "regular_local_services"
    RETAIL = "local_retail"
    INTRASTATE_BUSINESS = "regular_intrastate_business"
    EMPLOYEES = "employees_duties_unspecified"
    REAL_PROPERTY = "real_property_activity_unspecified"
    INCOME_PRODUCING_PROPERTY = "income_producing_real_or_tangible_property"
    ONLINE_SALES = "online_sales_facts_unspecified"
    INTERSTATE_COMMERCE = "interstate_commerce_only"
    BANK_ACCOUNT = "bank_account_only"
    INTERNAL_AFFAIRS = "internal_affairs_only"
    SOLICITATION = "orders_accepted_outside_state"
    SOLICITATION_OFFICE = "office_only_for_out_of_state_order_solicitation"
    ISOLATED_TRANSACTION = "isolated_transaction"


@dataclass(frozen=True, slots=True)
class BusinessPresence:
    activities: frozenset[Activity]
    isolated_transaction_days: int | None = None
    repeated_transactions: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "activities", frozenset(Activity(a) for a in self.activities))
        if self.isolated_transaction_days is not None and (
            type(self.isolated_transaction_days) is not int or self.isolated_transaction_days < 1
        ):
            raise ValueError("isolated_transaction_days must be a positive integer")
        if type(self.repeated_transactions) is not bool:
            raise ValueError("repeated_transactions must be boolean")


@dataclass(frozen=True, slots=True)
class LegalSource:
    citation: str
    url: str
    # Never imply a live review when source access was unavailable.
    verified_on: date | None = None

    def __post_init__(self) -> None:
        if not self.citation.strip() or not self.url.startswith("https://"):
            raise ValueError("Legal sources require a citation and HTTPS source URL")


@dataclass(frozen=True, slots=True)
class QualificationThreshold:
    citation: str
    trigger_activities: frozenset[Activity] = frozenset(
        {Activity.OFFICE, Activity.LOCAL_SERVICES, Activity.RETAIL, Activity.INTRASTATE_BUSINESS}
    )
    exempt_activities: frozenset[Activity] = frozenset(
        {
            Activity.INTERSTATE_COMMERCE,
            Activity.BANK_ACCOUNT,
            Activity.INTERNAL_AFFAIRS,
            Activity.SOLICITATION,
        }
    )
    isolated_transaction_max_days: int | None = None
    isolated_transaction_without_day_limit: bool = False
    notes: str = "Regular local operations are screening signals; statutory facts control."

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "trigger_activities", frozenset(Activity(a) for a in self.trigger_activities)
        )
        object.__setattr__(
            self, "exempt_activities", frozenset(Activity(a) for a in self.exempt_activities)
        )
        if self.trigger_activities & self.exempt_activities:
            raise ValueError("An activity cannot be both a trigger and an exemption")
        if type(self.isolated_transaction_without_day_limit) is not bool:
            raise ValueError("isolated_transaction_without_day_limit must be boolean")
        if (
            self.isolated_transaction_without_day_limit
            and self.isolated_transaction_max_days is not None
        ):
            raise ValueError(
                "An isolated transaction cannot have both an unlimited and finite limit"
            )
        if self.isolated_transaction_max_days is not None and (
            type(self.isolated_transaction_max_days) is not int
            or self.isolated_transaction_max_days < 1
        ):
            raise ValueError("Isolated transaction limit must be a positive integer")


class PenaltyPeriod(StrEnum):
    ONCE = "once"
    DAY = "day"
    CALENDAR_YEAR = "calendar_year_or_part"
    STARTED_YEAR = "anniversary_year_or_part"
    STARTED_MONTH = "month_or_part"
    FULL_MONTH = "completed_month"


def period_count(start: date, end: date, period: PenaltyPeriod) -> int:
    """Count [start, end): start is liable; end is the cure date, and is excluded.

    Month/year periods use anniversaries, clamped to month end for leap days.
    Statutory calendar-year schedules count each calendar year touched instead.
    """
    import calendar

    if type(start) is not date or type(end) is not date or end < start:
        raise ValueError("Penalty interval requires dates with end >= start")
    if start == end:
        return 0
    if period == PenaltyPeriod.ONCE:
        return 1
    if period == PenaltyPeriod.DAY:
        return (end - start).days
    if period == PenaltyPeriod.CALENDAR_YEAR:
        from datetime import timedelta

        return (end - timedelta(days=1)).year - start.year + 1
    if period == PenaltyPeriod.STARTED_YEAR:
        years = end.year - start.year
        anniversary = date(
            end.year, start.month, min(start.day, calendar.monthrange(end.year, start.month)[1])
        )
        return years + (end > anniversary)
    months = (end.year - start.year) * 12 + end.month - start.month
    anniversary = date(
        end.year, end.month, min(start.day, calendar.monthrange(end.year, end.month)[1])
    )
    if period == PenaltyPeriod.FULL_MONTH:
        return max(0, months - (end < anniversary))
    if period == PenaltyPeriod.STARTED_MONTH:
        return months + (end > anniversary)
    raise ValueError(f"Unsupported penalty period: {period}")


@dataclass(frozen=True, slots=True)
class PenaltyEstimate:
    minimum: Decimal | None
    maximum: Decimal | None
    periods: int
    interest: Decimal | None
    assessment: str
    citation: str
    unresolved: tuple[str, ...] = ()

    @property
    def exact_amount(self) -> Decimal | None:
        if self.unresolved or self.minimum is None or self.minimum != self.maximum:
            return None
        return self.minimum


@dataclass(frozen=True, slots=True)
class PenaltyPolicy:
    """A range if assessed; taxes and arrears are separate from qualification sanctions.

    None amounts mean unquantified, never zero. Interest is simple unless the
    statute specifically authorizes interest on accrued interest.
    """

    citation: str
    description: str
    amount_min: Decimal | None = None
    amount_max: Decimal | None = None
    period: PenaltyPeriod = PenaltyPeriod.ONCE
    grace_days: int = 0
    cap: Decimal | None = None
    assessment: str = "statutory_if_assessed"
    interest_monthly_rate: Decimal = Decimal("0")
    interest_period: PenaltyPeriod = PenaltyPeriod.STARTED_MONTH
    interest_on_penalty: bool = False
    compound_interest: bool = False
    unquantified_components: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "period", PenaltyPeriod(self.period))
        object.__setattr__(self, "interest_period", PenaltyPeriod(self.interest_period))
        if self.interest_monthly_rate is None:
            raise ValueError("interest_monthly_rate must be a nonnegative finite Decimal")
        for name in ("interest_on_penalty", "compound_interest"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be boolean")
        for name in ("amount_min", "amount_max", "interest_monthly_rate", "cap"):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, Decimal) or not value.is_finite() or value < 0
            ):
                raise ValueError(f"{name} must be a nonnegative finite Decimal")
        if (self.amount_min is None) != (self.amount_max is None):
            raise ValueError("Supply both monetary bounds, or leave both unquantified")
        if self.amount_min is not None and self.amount_min > self.amount_max:
            raise ValueError("Penalty minimum exceeds maximum")
        if type(self.grace_days) is not int or self.grace_days < 0:
            raise ValueError("grace_days must be a nonnegative integer")
        if self.interest_period not in {PenaltyPeriod.STARTED_MONTH, PenaltyPeriod.FULL_MONTH}:
            raise ValueError("Monthly interest requires a monthly counting period")
        object.__setattr__(self, "unquantified_components", tuple(self.unquantified_components))

    def estimate(
        self, start: date, end: date, *, unpaid_tax: Decimal | None = None
    ) -> PenaltyEstimate:
        count = period_count(start, end, self.period)
        if unpaid_tax is not None and (
            not isinstance(unpaid_tax, Decimal) or not unpaid_tax.is_finite() or unpaid_tax < 0
        ):
            raise ValueError("unpaid_tax must be a nonnegative finite Decimal")
        if (end - start).days <= self.grace_days:
            return PenaltyEstimate(
                Decimal("0.00"),
                Decimal("0.00"),
                0,
                Decimal("0.00"),
                self.assessment,
                self.citation,
                self.unquantified_components if start != end else (),
            )
        unresolved = list(self.unquantified_components)
        if self.amount_min is None:
            unresolved.append("Monetary sanction requires manual statutory assessment")
            return PenaltyEstimate(
                None, None, count, None, self.assessment, self.citation, tuple(unresolved)
            )
        low = self.amount_min * count
        high = self.amount_max * count
        if self.cap is not None:
            low = min(low, self.cap)
            high = min(high, self.cap)
        interest = Decimal("0")
        if self.interest_monthly_rate:
            if unpaid_tax is None:
                unresolved.append("unpaid_tax is required to estimate interest")
                interest = None
            else:
                months = period_count(start, end, self.interest_period)
                principal_low = unpaid_tax + (low if self.interest_on_penalty else 0)
                principal_high = unpaid_tax + (high if self.interest_on_penalty else 0)
                factor = (
                    (1 + self.interest_monthly_rate) ** months - 1
                    if self.compound_interest
                    else self.interest_monthly_rate * months
                )
                interest = principal_low * factor
                low += interest
                high += principal_high * factor
        return PenaltyEstimate(
            low.quantize(CENT, rounding=ROUND_HALF_UP),
            high.quantize(CENT, rounding=ROUND_HALF_UP),
            count,
            None if interest is None else interest.quantize(CENT, rounding=ROUND_HALF_UP),
            self.assessment,
            self.citation,
            tuple(unresolved),
        )


@dataclass(frozen=True, slots=True)
class StateForm:
    name: str
    identifier: str
    url: str


@dataclass(frozen=True, slots=True)
class AnnualObligation:
    name: str
    cycle: str
    due_rule: str
    fee: Decimal | None
    citation: str
    late_penalty: PenaltyPolicy | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if self.fee is not None and (
            not isinstance(self.fee, Decimal) or not self.fee.is_finite() or self.fee < 0
        ):
            raise ValueError("Annual fee must be a nonnegative finite Decimal or None")


@dataclass(frozen=True, slots=True)
class RegisteredAgentRequirement:
    citation: str
    physical_in_state_address: bool = True
    po_boxes_allowed: bool = False
    notes: str = "An eligible individual or authorized agent must maintain the registered office."


@dataclass(frozen=True, slots=True)
class EntityRequirement:
    entity_type: EntityType
    qualification_citation: str
    threshold: QualificationThreshold
    filing_fee: Decimal
    forms: tuple[StateForm, ...]
    qualification_penalty: PenaltyPolicy
    annual_obligations: tuple[AnnualObligation, ...] = ()
    initial_report: str | None = None
    consequences: tuple[str, ...] = ()
    good_standing_evidence: str = "Obtain evidence of existence/status from the domestic state."

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_type", EntityType(self.entity_type))
        if (
            not isinstance(self.filing_fee, Decimal)
            or not self.filing_fee.is_finite()
            or self.filing_fee < 0
        ):
            raise ValueError("filing_fee must be a nonnegative finite Decimal")
        for name in ("forms", "annual_obligations", "consequences"):
            object.__setattr__(self, name, tuple(getattr(self, name)))


@dataclass(frozen=True, slots=True)
class StateRequirement:
    state: str
    name: str
    registered_agent: RegisteredAgentRequirement
    entity_rules: Mapping[EntityType, EntityRequirement]
    sources: tuple[LegalSource, ...]
    version: str = "2026-10-reference"
    notes: tuple[str, ...] = field(default_factory=tuple)
    verification_issues: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", normalize_state(self.state))
        copied = {EntityType(k): v for k, v in self.entity_rules.items()}
        if set(copied) != set(EntityType):
            raise ValueError("State rules must cover LLC, C-Corp, and LP")
        if any(k != v.entity_type for k, v in copied.items()):
            raise ValueError("Entity requirement does not match registry key")
        object.__setattr__(self, "entity_rules", MappingProxyType(copied))
        object.__setattr__(self, "sources", tuple(self.sources))
        object.__setattr__(self, "notes", tuple(self.notes))
        object.__setattr__(self, "verification_issues", tuple(self.verification_issues))
        if not self.sources:
            raise ValueError("State rules need source provenance")

    def for_entity(self, entity_type: EntityType) -> EntityRequirement:
        return self.entity_rules[EntityType(entity_type)]

    @property
    def sources_verified(self) -> bool:
        return all(source.verified_on is not None for source in self.sources)

    @property
    def rules_verified(self) -> bool:
        return self.sources_verified and not self.verification_issues
