"""Public registry adapter contracts; adapters never infer local business activity."""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

from ..models import AuditResult, BusinessPresence, Entity, RegisteredAgent

if TYPE_CHECKING:
    from ..rules.registry import RulesRegistry


class ComplianceFlag(StrEnum):
    DOMESTIC_REINSTATEMENT = "domestic_reinstatement_required"
    FOREIGN_FILING = "foreign_filing_required"
    REGISTERED_AGENT_APPOINTMENT = "registered_agent_appointment_required"
    QUALIFICATION_REVIEW = "qualification_review_required"
    ADVERSE_STATUS_MAPPING = "adverse_registry_status_mapped"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A machine-readable issue, without an unfiltered copy of the source row."""

    field: str
    code: str
    message: str


class RecordValidationError(ValueError):
    """A rejected row. Batch processing retains this error and continues."""

    def __init__(self, issues: Iterable[ValidationIssue], *, row_number: int | None = None):
        self.issues = tuple(issues)
        if not self.issues:
            raise ValueError("RecordValidationError needs at least one issue")
        self.row_number = row_number
        prefix = f"Row {row_number}: " if row_number is not None else ""
        super().__init__(prefix + "; ".join(f"{i.field}: {i.message}" for i in self.issues))


@dataclass(frozen=True, slots=True)
class NormalizedRecord:
    entity: Entity
    source_jurisdiction: str | None
    status_jurisdiction: str
    raw_status: str
    row_number: int | None
    flags: tuple[ComplianceFlag, ...]
    audit_result: AuditResult | None = None
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BatchNormalizationResult:
    accepted: tuple[NormalizedRecord, ...]
    rejected: tuple[RecordValidationError, ...]


class BaseRegistryAdapter(ABC):
    """Implement ``normalize`` for a jurisdiction's public records or bulk export.

    Fetching, rate limits and public-data terms belong to each future SOS adapter.
    This interface performs no network access and stores no authentication data.
    ``presence`` contains separately established business facts, not registry status.
    """

    @abstractmethod
    def normalize(
        self,
        record: Mapping[str, object],
        *,
        row_number: int | None = None,
        target_state: str | None = None,
        presence: BusinessPresence | None = None,
        is_qualified: bool = False,
        registered_agent: RegisteredAgent | None = None,
        as_of: date | None = None,
        registry: "RulesRegistry | None" = None,
    ) -> NormalizedRecord:
        """Normalize one record, or raise a structured ``RecordValidationError``."""

    def normalize_many(
        self,
        records: Iterable[Mapping[str, object]],
        *,
        start_row: int = 1,
        target_state: str | None = None,
        presence: BusinessPresence | None = None,
        is_qualified: bool = False,
        registered_agent: RegisteredAgent | None = None,
        as_of: date | None = None,
        registry: "RulesRegistry | None" = None,
    ) -> BatchNormalizationResult:
        """Process independent rows, keeping valid rows even when another row fails."""
        if type(start_row) is not int or start_row < 1:
            raise ValueError("start_row must be a positive integer")
        accepted: list[NormalizedRecord] = []
        rejected: list[RecordValidationError] = []
        for row_number, record in enumerate(records, start=start_row):
            try:
                accepted.append(
                    self.normalize(
                        record,
                        row_number=row_number,
                        target_state=target_state,
                        presence=presence,
                        is_qualified=is_qualified,
                        registered_agent=registered_agent,
                        as_of=as_of,
                        registry=registry,
                    )
                )
            except RecordValidationError as exc:
                rejected.append(exc)
        return BatchNormalizationResult(tuple(accepted), tuple(rejected))
