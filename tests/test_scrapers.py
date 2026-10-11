"""Normalization must preserve evidence and continue after invalid source rows."""

from datetime import date, datetime
from io import StringIO
from pathlib import Path

import pytest
from us_new_entities.models import (
    Activity,
    BusinessPresence,
    EntityStatus,
    EntityType,
    QualificationDecision,
    RegisteredAgent,
)
from us_new_entities.scrapers import (
    BaseRegistryAdapter,
    ComplianceFlag,
    CSVRegistryAdapter,
    RecordValidationError,
)


def record(**overrides):
    result = {
        "legal_name": "  Sample LLC  ",
        "entity_type": "limited liability company",
        "domestic_state": "Delaware",
        "formation_date": "2024-02-29",
        "sos_entity_id": "00000123",
        "status": "In Good Standing",
        "status_jurisdiction": "DE",
    }
    result.update(overrides)
    return result


def test_adapter_interface_is_abstract():
    with pytest.raises(TypeError):
        BaseRegistryAdapter()


def test_normalization_keeps_formation_and_registry_jurisdictions_distinct():
    normalized = CSVRegistryAdapter(source_jurisdiction="California").normalize(record())
    assert normalized.entity.legal_name == "Sample LLC"
    assert normalized.entity.entity_type == EntityType.LLC
    assert normalized.entity.domestic_state == "DE"
    assert normalized.entity.formation_date == date(2024, 2, 29)
    assert normalized.entity.sos_entity_id == "00000123"
    assert normalized.entity.status == EntityStatus.GOOD_STANDING
    assert normalized.source_jurisdiction == "CA"
    assert normalized.status_jurisdiction == "DE"
    assert normalized.audit_result is None
    assert normalized.flags == (ComplianceFlag.QUALIFICATION_REVIEW,)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("03/01/2024", date(2024, 3, 1)),
        ("2024-02-29", date(2024, 2, 29)),
        (date(2020, 1, 1), date(2020, 1, 1)),
    ],
)
def test_supported_date_formats(value, expected):
    assert (
        CSVRegistryAdapter().normalize(record(formation_date=value)).entity.formation_date
        == expected
    )


@pytest.mark.parametrize(
    "value",
    [
        "2023-02-29",
        "31/01/2024",
        "1/2/2024",
        "01-02-24",
        "2024-02-29T00:00:00Z",
        "29 Feb 2024",
        "",
        None,
        datetime(2024, 2, 29),
    ],
)
def test_ambiguous_invalid_or_timestamp_dates_are_rejected(value):
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(record(formation_date=value))
    assert any(issue.field == "formation_date" for issue in captured.value.issues)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("LLC", EntityType.LLC),
        ("C-Corp", EntityType.C_CORP),
        ("Corporation", EntityType.C_CORP),
        ("Limited Partnership", EntityType.LP),
    ],
)
def test_entity_form_aliases(value, expected):
    assert CSVRegistryAdapter().normalize(record(entity_type=value)).entity.entity_type == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("good-standing", EntityStatus.GOOD_STANDING),
        ("ftb forfeited", EntityStatus.FORFEITED),
        ("SOS Forfeited", EntityStatus.FORFEITED),
        ("Suspended", EntityStatus.FORFEITED),
        ("FTB Suspended", EntityStatus.FORFEITED),
        ("Revoked", EntityStatus.REVOKED),
    ],
)
def test_explicit_status_aliases_preserve_original_status(value, expected):
    normalized = CSVRegistryAdapter().normalize(record(status=value))
    assert normalized.entity.status == expected
    assert normalized.raw_status == value
    if "suspended" in value.casefold():
        assert ComplianceFlag.ADVERSE_STATUS_MAPPING in normalized.flags
        assert normalized.warnings


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "Active"),
        ("status", "Inactive"),
        ("status", "Dissolved"),
        ("domestic_state", "XX"),
        ("domestic_state", "Ontario"),
        ("entity_type", "Nonprofit Corporation"),
        ("sos_entity_id", 123),
        ("legal_name", " "),
    ],
)
def test_invalid_values_report_the_affected_field(field, value):
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(record(**{field: value}), row_number=7)
    assert captured.value.row_number == 7
    assert any(issue.field == field for issue in captured.value.issues)


def test_multiple_errors_are_reported_together():
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(
            record(status="Active", domestic_state="XX", formation_date="2023-02-29")
        )
    assert {issue.field for issue in captured.value.issues} == {
        "status",
        "domestic_state",
        "formation_date",
    }


def test_registered_state_does_not_fill_missing_domestic_state():
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter(source_jurisdiction="CA").normalize(
            record(domestic_state="", registration_state="CA")
        )
    assert any(issue.field == "domestic_state" for issue in captured.value.issues)


def test_conflicting_export_provenance_is_rejected():
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter(source_jurisdiction="CA").normalize(record(source_jurisdiction="TX"))
    assert captured.value.issues[0].code == "conflict"


@pytest.mark.parametrize("status", ["Revoked", "Good Standing", "Forfeited"])
def test_foreign_registry_status_does_not_establish_domestic_standing(status):
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter(source_jurisdiction="CA").normalize(
            record(status=status, status_jurisdiction="")
        )
    assert any(
        issue.field == "status_jurisdiction" and issue.code == "non_domestic_status"
        for issue in captured.value.issues
    )


def test_explicit_foreign_status_provenance_is_rejected():
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(record(status="Revoked", status_jurisdiction="CA"))
    assert captured.value.issues[0].code == "non_domestic_status"


def test_same_jurisdiction_registry_can_supply_domestic_status_without_extra_provenance():
    normalized = CSVRegistryAdapter(source_jurisdiction="DE").normalize(
        record(status_jurisdiction="", status="Revoked")
    )
    assert normalized.status_jurisdiction == "DE"
    assert ComplianceFlag.DOMESTIC_REINSTATEMENT in normalized.flags


def test_invalid_status_provenance_is_rejected():
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(record(status_jurisdiction="XX"))
    assert any(
        issue.field == "status_jurisdiction" and issue.code == "invalid_state"
        for issue in captured.value.issues
    )


def test_foreign_expansion_flags_forfeited_entity_and_agent_remedies():
    normalized = CSVRegistryAdapter(source_jurisdiction="CA").normalize(
        record(status="Forfeited"),
        target_state="Texas",
        presence=BusinessPresence(frozenset({Activity.LOCAL_SERVICES})),
        as_of=date(2025, 1, 1),
    )
    assert normalized.audit_result.decision == QualificationDecision.REQUIRED
    assert normalized.audit_result.filing_blockers
    assert set(normalized.flags) == {
        ComplianceFlag.DOMESTIC_REINSTATEMENT,
        ComplianceFlag.FOREIGN_FILING,
        ComplianceFlag.REGISTERED_AGENT_APPOINTMENT,
    }


def test_target_without_business_evidence_requests_review():
    normalized = CSVRegistryAdapter().normalize(record(), target_state="TX")
    assert normalized.audit_result.qualification_required is None
    assert normalized.flags == (ComplianceFlag.QUALIFICATION_REVIEW,)


def test_explicit_qualification_and_agent_facts_avoid_duplicate_remedies():
    normalized = CSVRegistryAdapter().normalize(
        record(),
        target_state="TX",
        presence=BusinessPresence(frozenset({Activity.OFFICE})),
        is_qualified=True,
        registered_agent=RegisteredAgent("Agent", "TX", "100 Main Street"),
    )
    assert ComplianceFlag.FOREIGN_FILING not in normalized.flags
    assert ComplianceFlag.REGISTERED_AGENT_APPOINTMENT not in normalized.flags


@pytest.mark.parametrize("target", ["XX", "Vermont"])
def test_unknown_or_unimplemented_target_is_rejected(target):
    with pytest.raises(RecordValidationError) as captured:
        CSVRegistryAdapter().normalize(
            record(), target_state=target, presence=BusinessPresence(frozenset({Activity.OFFICE}))
        )
    assert captured.value.issues[0].code == "invalid_audit_context"


def test_bulk_fixture_retains_valid_rows_and_structured_rejections():
    path = Path(__file__).parent / "fixtures" / "registry_records.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        result = CSVRegistryAdapter(source_jurisdiction="CA").ingest_csv(
            source,
            target_state="CA",
            presence=BusinessPresence(frozenset({Activity.OFFICE})),
            as_of=date(2025, 1, 1),
        )
    assert len(result.accepted) == 4
    assert len(result.rejected) == 4
    assert [row.row_number for row in result.accepted] == [2, 3, 4, 9]
    assert [error.row_number for error in result.rejected] == [5, 6, 7, 8]
    assert result.accepted[0].entity.sos_entity_id == "00001234"
    assert ComplianceFlag.DOMESTIC_REINSTATEMENT in result.accepted[1].flags
    assert result.accepted[-1].entity.status == EntityStatus.REVOKED


def test_mapping_batch_continues_after_bad_rows():
    result = CSVRegistryAdapter().normalize_many([record(), record(status="Active"), record()])
    assert [row.row_number for row in result.accepted] == [1, 3]
    assert result.rejected[0].row_number == 2


@pytest.mark.parametrize("csv_text", ["", "legal_name,legal_name\nA,B\n", ",status\nA,B\n"])
def test_empty_or_duplicate_csv_headers_are_rejected(csv_text):
    result = CSVRegistryAdapter().ingest_csv(StringIO(csv_text))
    assert not result.accepted
    assert result.rejected[0].issues[0].field == "csv_header"


def test_extra_csv_cells_are_not_silently_discarded():
    source = StringIO(
        "legal_name,entity_type,domestic_state,formation_date,status\n"
        "Sample,LLC,DE,2024-01-01,Good Standing,extra\n"
    )
    result = CSVRegistryAdapter().ingest_csv(source)
    assert not result.accepted
    assert result.rejected[0].issues[0].code == "extra_cells"


def test_csv_syntax_error_is_retained_as_a_rejection():
    source = StringIO(
        "legal_name,entity_type,domestic_state,formation_date,status\n"
        '"unterminated,LLC,DE,2024-01-01,Good Standing\n'
    )
    result = CSVRegistryAdapter().ingest_csv(source)
    assert not result.accepted
    assert result.rejected[0].issues[0].code == "invalid_csv"


@pytest.mark.parametrize(
    "csv_text",
    [
        "foo\n",
        "legal_name,entity_type,domestic_state,status\nSample,LLC,DE,Good Standing\n",
    ],
)
def test_missing_required_csv_headers_are_rejected_before_row_iteration(csv_text):
    result = CSVRegistryAdapter().ingest_csv(StringIO(csv_text))
    assert not result.accepted
    assert len(result.rejected) == 1
    assert result.rejected[0].row_number == 1
    assert result.rejected[0].issues[0].field == "csv_header"
    assert result.rejected[0].issues[0].code == "missing_columns"
    assert "formation_date" in result.rejected[0].issues[0].message


def test_correct_header_without_data_is_an_empty_successful_export():
    source = StringIO("legal_name,entity_type,domestic_state,formation_date,status\n")
    result = CSVRegistryAdapter().ingest_csv(source)
    assert result.accepted == ()
    assert result.rejected == ()
