"""Strict example adapter for canonicalized SOS bulk CSV exports.

Required columns: legal_name, entity_type, domestic_state, formation_date, status.
Optional columns: sos_entity_id, source_jurisdiction, status_jurisdiction. All other
columns are ignored. status is standing in the domestic formation jurisdiction.
status_jurisdiction defaults to the source jurisdiction when known, else domestic.
A foreign registry export must therefore supply affirmative domestic-status
provenance with status_jurisdiction=domestic_state; source-local foreign registration
status cannot establish domestic standing or imply a domestic reinstatement remedy.
The domestic_state column means formation jurisdiction, never registration location.
Only ISO YYYY-MM-DD and explicit US MM/DD/YYYY dates are accepted. Unknown values,
including registry 'Active' without affirmative standing evidence, are rejected.

Suspended, FTB/SOS suspended and FTB/SOS forfeited statuses are collapsed into the
model's adverse Forfeited category to require remediation. The original status and
a warning remain available; this mapping does not equate their legal consequences.
Business facts are supplied through target_state/presence arguments only.
"""

import csv
import re
from collections.abc import Mapping
from datetime import date, datetime
from typing import TYPE_CHECKING, TextIO

from ..models import (
    BusinessPresence,
    ComplianceAudit,
    Entity,
    EntityStatus,
    EntityType,
    QualificationDecision,
    RegisteredAgent,
    normalize_state,
)
from .base import (
    BaseRegistryAdapter,
    BatchNormalizationResult,
    ComplianceFlag,
    NormalizedRecord,
    RecordValidationError,
    ValidationIssue,
)

if TYPE_CHECKING:
    from ..rules.registry import RulesRegistry


_TYPE_ALIASES = {
    "llc": EntityType.LLC,
    "limited liability company": EntityType.LLC,
    "c corp": EntityType.C_CORP,
    "c corporation": EntityType.C_CORP,
    "corporation": EntityType.C_CORP,
    "business corporation": EntityType.C_CORP,
    "stock corporation": EntityType.C_CORP,
    "lp": EntityType.LP,
    "limited partnership": EntityType.LP,
}
_STATUS_ALIASES = {
    "good standing": EntityStatus.GOOD_STANDING,
    "in good standing": EntityStatus.GOOD_STANDING,
    "forfeited": EntityStatus.FORFEITED,
    "ftb forfeited": EntityStatus.FORFEITED,
    "sos forfeited": EntityStatus.FORFEITED,
    "sos ftb forfeited": EntityStatus.FORFEITED,
    "ftb sos forfeited": EntityStatus.FORFEITED,
    "suspended": EntityStatus.FORFEITED,
    "ftb suspended": EntityStatus.FORFEITED,
    "sos suspended": EntityStatus.FORFEITED,
    "sos ftb suspended": EntityStatus.FORFEITED,
    "ftb sos suspended": EntityStatus.FORFEITED,
    "revoked": EntityStatus.REVOKED,
}
_REQUIRED_COLUMNS = frozenset(
    {
        "legal_name",
        "entity_type",
        "domestic_state",
        "formation_date",
        "status",
    }
)


def _alias_key(value: str) -> str:
    return re.sub(r"[\s\-_/]+", " ", value.strip().casefold()).strip()


def _parse_date(value: object) -> date:
    if type(value) is date:
        return value
    if not isinstance(value, str):
        raise ValueError("Use a date, YYYY-MM-DD, or US MM/DD/YYYY")
    value = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", value):
        return datetime.strptime(value, "%m/%d/%Y").date()
    raise ValueError("Use YYYY-MM-DD or explicit US MM/DD/YYYY; no inferred date formats")


class CSVRegistryAdapter(BaseRegistryAdapter):
    """Normalize a user-supplied export without fetching any public registry.

    ``source_jurisdiction`` describes the exporting registry. For example, a CA
    export can contain a DE domestic entity: these jurisdictions stay distinct.
    Corporation aliases refer to legal entity form, not C/S tax-election evidence.
    """

    def __init__(self, *, source_jurisdiction: str | None = None):
        self.source_jurisdiction = (
            normalize_state(source_jurisdiction) if source_jurisdiction is not None else None
        )

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
        issues: list[ValidationIssue] = []
        if not isinstance(record, Mapping):
            raise RecordValidationError(
                (ValidationIssue("record", "invalid_type", "Record must be a mapping"),),
                row_number=row_number,
            )
        if None in record:
            issues.append(ValidationIssue("csv_row", "extra_cells", "More cells than CSV headers"))

        def required_text(field: str) -> str | None:
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(ValidationIssue(field, "required", "Supply a nonempty string"))
                return None
            return value.strip()

        legal_name = required_text("legal_name")
        type_value = required_text("entity_type")
        status_value = required_text("status")
        domestic_value = required_text("domestic_state")
        entity_type = _TYPE_ALIASES.get(_alias_key(type_value)) if type_value else None
        if type_value and entity_type is None:
            issues.append(
                ValidationIssue("entity_type", "unsupported", "Expected LLC, C-Corp or LP")
            )
        status = _STATUS_ALIASES.get(_alias_key(status_value)) if status_value else None
        if status_value and status is None:
            issues.append(
                ValidationIssue(
                    "status",
                    "unknown_status",
                    "Explicit standing, forfeiture or revocation is required; "
                    "Active alone does not prove Good Standing",
                )
            )
        domestic_state = None
        if domestic_value:
            try:
                domestic_state = normalize_state(domestic_value)
            except ValueError as exc:
                issues.append(ValidationIssue("domestic_state", "invalid_state", str(exc)))
        formation_date = None
        try:
            formation_date = _parse_date(record.get("formation_date"))
        except ValueError as exc:
            issues.append(ValidationIssue("formation_date", "invalid_date", str(exc)))
        identifier = record.get("sos_entity_id")
        if isinstance(identifier, str):
            identifier = identifier.strip() or None
        elif identifier is not None:
            issues.append(
                ValidationIssue(
                    "sos_entity_id",
                    "invalid_type",
                    "Supply an identifier string to preserve leading zeros",
                )
            )
        source = self.source_jurisdiction
        source_value = record.get("source_jurisdiction")
        if source_value not in (None, ""):
            try:
                normalized_source = normalize_state(source_value)
                if source is not None and source != normalized_source:
                    issues.append(
                        ValidationIssue(
                            "source_jurisdiction",
                            "conflict",
                            "Row and adapter source jurisdictions differ",
                        )
                    )
                else:
                    source = normalized_source
            except ValueError as exc:
                issues.append(ValidationIssue("source_jurisdiction", "invalid_state", str(exc)))
        status_jurisdiction = source or domestic_state
        status_source_value = record.get("status_jurisdiction")
        if status_source_value not in (None, ""):
            try:
                status_jurisdiction = normalize_state(status_source_value)
            except ValueError as exc:
                issues.append(ValidationIssue("status_jurisdiction", "invalid_state", str(exc)))
        if domestic_state is not None and status_jurisdiction != domestic_state:
            issues.append(
                ValidationIssue(
                    "status_jurisdiction",
                    "non_domestic_status",
                    "Status must have affirmative domestic-jurisdiction provenance; foreign "
                    "registry standing does not establish domestic standing or reinstatement needs",
                )
            )
        if issues:
            raise RecordValidationError(issues, row_number=row_number)
        entity = Entity(legal_name, entity_type, domestic_state, formation_date, identifier, status)
        flags: list[ComplianceFlag] = []
        warnings: list[str] = []
        if status != EntityStatus.GOOD_STANDING:
            flags.append(ComplianceFlag.DOMESTIC_REINSTATEMENT)
        if "suspended" in _alias_key(status_value):
            flags.append(ComplianceFlag.ADVERSE_STATUS_MAPPING)
            warnings.append(
                "Suspension is mapped to the adverse Forfeited category for screening; "
                "verify the source jurisdiction's specific reinstatement procedure."
            )
        audit = None
        if target_state is not None:
            try:
                audit = ComplianceAudit(
                    entity,
                    target_state,
                    presence if presence is not None else BusinessPresence(frozenset()),
                    is_qualified=is_qualified,
                    registered_agent=registered_agent,
                    as_of=as_of,
                ).evaluate(registry)
            except ValueError as exc:
                raise RecordValidationError(
                    (ValidationIssue("audit", "invalid_audit_context", str(exc)),),
                    row_number=row_number,
                ) from exc
            if audit.foreign_filing_required:
                flags.append(ComplianceFlag.FOREIGN_FILING)
            if audit.registered_agent_appointment_required:
                flags.append(ComplianceFlag.REGISTERED_AGENT_APPOINTMENT)
            if audit.decision == QualificationDecision.REVIEW_REQUIRED:
                flags.append(ComplianceFlag.QUALIFICATION_REVIEW)
        else:
            flags.append(ComplianceFlag.QUALIFICATION_REVIEW)
            warnings.append(
                "No target-state audit was requested; registry records alone do not "
                "establish local business activity or qualification requirements."
            )
        return NormalizedRecord(
            entity=entity,
            source_jurisdiction=source,
            status_jurisdiction=status_jurisdiction,
            raw_status=status_value,
            row_number=row_number,
            flags=tuple(flags),
            audit_result=audit,
            warnings=tuple(warnings),
        )

    def ingest_csv(
        self,
        source: TextIO,
        *,
        target_state: str | None = None,
        presence: BusinessPresence | None = None,
        is_qualified: bool = False,
        registered_agent: RegisteredAgent | None = None,
        as_of: date | None = None,
        registry: "RulesRegistry | None" = None,
    ) -> BatchNormalizationResult:
        """Read a CSV text stream (open UTF-8 exports with ``encoding='utf-8-sig'``).

        Row numbers are CSV physical line numbers. Invalid field values do not stop
        subsequent rows. A CSV syntax error stops parsing because row boundaries
        cannot be trusted, and is retained as a structured rejection.
        """
        reader = csv.DictReader(source, strict=True)
        accepted: list[NormalizedRecord] = []
        rejected: list[RecordValidationError] = []
        try:
            headers = reader.fieldnames
        except csv.Error as exc:
            return BatchNormalizationResult(
                (),
                (
                    RecordValidationError(
                        (ValidationIssue("csv_header", "invalid_csv", str(exc)),),
                        row_number=1,
                    ),
                ),
            )
        if not headers or len(set(headers)) != len(headers) or any(not h for h in headers):
            return BatchNormalizationResult(
                (),
                (
                    RecordValidationError(
                        (
                            ValidationIssue(
                                "csv_header", "invalid_header", "CSV needs nonempty unique headers"
                            ),
                        ),
                        row_number=1,
                    ),
                ),
            )
        missing_columns = sorted(_REQUIRED_COLUMNS - set(headers))
        if missing_columns:
            return BatchNormalizationResult(
                (),
                (
                    RecordValidationError(
                        (
                            ValidationIssue(
                                "csv_header",
                                "missing_columns",
                                "Missing required CSV columns: " + ", ".join(missing_columns),
                            ),
                        ),
                        row_number=1,
                    ),
                ),
            )
        while True:
            try:
                record = next(reader)
            except StopIteration:
                break
            except csv.Error as exc:
                rejected.append(
                    RecordValidationError(
                        (ValidationIssue("csv_row", "invalid_csv", str(exc)),),
                        row_number=reader.line_num,
                    )
                )
                break
            try:
                accepted.append(
                    self.normalize(
                        record,
                        row_number=reader.line_num,
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
