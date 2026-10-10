"""Sourced optional filing fees and separately priced commercial agent services."""

from dataclasses import dataclass
from decimal import Decimal

from ..models import LegalSource
from .redirect import Provider


def validate_money(value: Decimal | None, name: str) -> None:
    if value is not None and (not isinstance(value, Decimal) or not value.is_finite() or value < 0):
        raise ValueError(f"{name} must be a nonnegative finite Decimal or None")


@dataclass(frozen=True, slots=True)
class ExpeditedOption:
    name: str
    surcharge: Decimal
    timing: str
    source: LegalSource
    surcharge_max: Decimal | None = None

    def __post_init__(self) -> None:
        validate_money(self.surcharge, "surcharge")
        validate_money(self.surcharge_max, "surcharge_max")
        if self.surcharge_max is not None and self.surcharge_max < self.surcharge:
            raise ValueError("Expedited fee upper bound is below the lower bound")
        if self.surcharge is None or not self.name.strip() or not self.timing.strip():
            raise ValueError("Expedited option needs a name, amount, and sourced timing")
        if not isinstance(self.source, LegalSource):
            raise ValueError("Expedited option source must be a LegalSource")


@dataclass(frozen=True, slots=True)
class FilingOptions:
    expedited: tuple[ExpeditedOption, ...] = ()
    agent_designation_fee: Decimal | None = None
    agent_designation_source: LegalSource | None = None
    standard_processing: str | None = None
    processing_source: LegalSource | None = None
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        validate_money(self.agent_designation_fee, "agent_designation_fee")
        if self.agent_designation_fee is not None and self.agent_designation_source is None:
            raise ValueError("Agent designation fee needs a government source")
        if self.standard_processing is not None and self.processing_source is None:
            raise ValueError("Processing estimates need an official source")
        for source in (self.agent_designation_source, self.processing_source):
            if source is not None and not isinstance(source, LegalSource):
                raise ValueError("Filing option sources must be LegalSource objects")
        if self.standard_processing is not None and not self.standard_processing.strip():
            raise ValueError("Standard processing description must be nonempty")
        if any(not isinstance(option, ExpeditedOption) for option in self.expedited):
            raise ValueError("expedited must contain ExpeditedOption objects")
        object.__setattr__(self, "expedited", tuple(self.expedited))
        object.__setattr__(self, "notes", tuple(self.notes))


@dataclass(frozen=True, slots=True)
class ProviderQuote:
    provider: Provider
    annual_price: Decimal | None = None
    price_source: LegalSource | None = None
    appointment_timing: str | None = None
    filing_timing: str | None = None
    timing_source: LegalSource | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider", Provider(self.provider))
        validate_money(self.annual_price, "annual_price")
        if self.annual_price is not None and self.price_source is None:
            raise ValueError("Commercial pricing needs a provider source")
        if (self.appointment_timing or self.filing_timing) and self.timing_source is None:
            raise ValueError("Provider timing claims need a source")
        for source in (self.price_source, self.timing_source):
            if source is not None and not isinstance(source, LegalSource):
                raise ValueError("Provider sources must be LegalSource objects")
        for timing in (self.appointment_timing, self.filing_timing):
            if timing is not None and (not isinstance(timing, str) or not timing.strip()):
                raise ValueError("Provider timing descriptions must be nonempty strings")
