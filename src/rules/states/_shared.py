"""Small constructors for source-backed rules; unknown sanctions remain unquantified."""

from datetime import date
from decimal import Decimal

from ...models import AnnualObligation, LegalSource, PenaltyPolicy

REVIEWED = date(2026, 10, 11)


def source(citation: str, url: str) -> LegalSource:
    return LegalSource(citation, url, REVIEWED)


def unresolved_penalty(citation: str, description: str) -> PenaltyPolicy:
    return PenaltyPolicy(
        citation=citation,
        description=description,
        assessment="manual_statutory_assessment",
        unquantified_components=(description,),
    )


def annual(
    name: str, due: str, fee: str | None, citation: str, notes: str = ""
) -> AnnualObligation:
    return AnnualObligation(
        name=name,
        cycle="annual",
        due_rule=due,
        fee=Decimal(fee) if fee is not None else None,
        citation=citation,
        notes=notes,
    )
