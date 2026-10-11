import json
from datetime import date, datetime
from pathlib import Path

import pytest
from us_new_entities.models import (
    Activity,
    BusinessPresence,
    ComplianceAudit,
    Entity,
    EntityStatus,
    EntityType,
    QualificationDecision,
    RegisteredAgent,
)
from us_new_entities.rules.registry import DEFAULT_REGISTRY, UnsupportedJurisdictionError

STATES = ("CA", "DE", "TX", "FL", "WY")
AS_OF = date(2026, 10, 10)


def entity_for(target, entity_type=EntityType.LLC, **changes):
    values = {
        "legal_name": "Example Entity",
        "entity_type": entity_type,
        "domestic_state": "DE" if target != "DE" else "WY",
        "formation_date": date(2020, 1, 1),
        "sos_entity_id": "000001",
        "status": EntityStatus.GOOD_STANDING,
    }
    return Entity(**(values | changes))


def audit(target, activities, entity_type=EntityType.LLC, **options):
    return ComplianceAudit(
        entity_for(target, entity_type),
        target,
        BusinessPresence(activities),
        as_of=AS_OF,
        **options,
    ).evaluate()


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
@pytest.mark.parametrize(
    "activity",
    [Activity.OFFICE, Activity.LOCAL_SERVICES, Activity.RETAIL, Activity.INTRASTATE_BUSINESS],
)
def test_regular_foreign_local_operations_require_filing_and_agent(target, entity_type, activity):
    result = audit(target, {activity}, entity_type)
    assert result.decision is QualificationDecision.REQUIRED
    assert result.qualification_required is True
    assert result.foreign_filing_required is True
    assert result.registered_agent_required is True
    assert result.registered_agent_appointment_required is True
    assert result.domestic_reinstatement_required is False
    assert not result.filing_blockers
    assert result.sources
    assert result.entity_requirement.entity_type is entity_type
    assert result.entity_requirement.forms[0].name in " ".join(result.remedies)


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_domestic_operations_do_not_need_foreign_qualification(target, entity_type):
    entity = entity_for(target, entity_type, domestic_state=target)
    result = ComplianceAudit(
        entity,
        target,
        BusinessPresence({Activity.OFFICE}),
        as_of=AS_OF,
    ).evaluate()
    assert result.decision is QualificationDecision.NOT_REQUIRED
    assert result.qualification_required is False
    assert result.foreign_filing_required is False
    assert result.registered_agent_required is True
    assert result.registered_agent_appointment_required is True


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_domestic_agent_requirement_is_satisfied_by_a_valid_in_state_agent(target, entity_type):
    result = ComplianceAudit(
        entity_for(target, entity_type, domestic_state=target),
        target,
        BusinessPresence({Activity.OFFICE}),
        registered_agent=RegisteredAgent("Domestic Service Agent", target, "123 Main Street"),
        as_of=AS_OF,
    ).evaluate()
    assert result.qualification_required is False
    assert result.foreign_filing_required is False
    assert result.registered_agent_required is True
    assert result.registered_agent_appointment_required is False


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_safe_harbor_activities_do_not_require_foreign_filing(target, entity_type):
    result = audit(target, {Activity.INTERSTATE_COMMERCE}, entity_type)
    assert result.decision is QualificationDecision.NOT_REQUIRED
    assert result.qualification_required is False
    assert result.foreign_filing_required is False
    assert result.registered_agent_appointment_required is False


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_bank_accounts_use_the_state_and_entity_specific_safe_harbor(target, entity_type):
    result = audit(target, {Activity.BANK_ACCOUNT}, entity_type)
    if (target, entity_type) in {("DE", EntityType.C_CORP), ("WY", EntityType.LP)}:
        assert result.decision is QualificationDecision.REVIEW_REQUIRED
        assert result.foreign_filing_required is None
    else:
        assert result.decision is QualificationDecision.NOT_REQUIRED
        assert result.foreign_filing_required is False


@pytest.mark.parametrize("target", STATES)
def test_interstate_safe_harbor_does_not_hide_local_office(target):
    result = audit(target, {Activity.INTERSTATE_COMMERCE, Activity.OFFICE})
    assert result.decision is QualificationDecision.REQUIRED
    assert result.foreign_filing_required is True


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_texas_out_of_state_order_acceptance_alone_requires_review(entity_type):
    result = audit("TX", {Activity.SOLICITATION}, entity_type)
    assert result.decision is QualificationDecision.REVIEW_REQUIRED
    assert result.foreign_filing_required is None


def test_delaware_corporate_office_used_only_for_protected_solicitation_is_exempt():
    result = audit("DE", {Activity.SOLICITATION_OFFICE}, EntityType.C_CORP)
    assert result.decision is QualificationDecision.NOT_REQUIRED
    assert result.foreign_filing_required is False
    assert result.registered_agent_required is False


def test_delaware_corporate_operating_office_is_not_exempt_by_out_of_state_order_acceptance():
    result = audit("DE", {Activity.OFFICE, Activity.SOLICITATION}, EntityType.C_CORP)
    assert result.decision is QualificationDecision.REQUIRED
    assert result.foreign_filing_required is True
    assert result.registered_agent_required is True


@pytest.mark.parametrize(
    ("target", "entity_type"),
    [
        (target, entity_type)
        for target in STATES
        for entity_type in EntityType
        if (target, entity_type) != ("DE", EntityType.C_CORP)
    ],
)
def test_other_entity_rules_do_not_inherit_delaware_corporate_solicitation_office_exemption(
    target,
    entity_type,
):
    result = audit(target, {Activity.SOLICITATION_OFFICE}, entity_type)
    assert result.decision is QualificationDecision.REVIEW_REQUIRED
    assert result.foreign_filing_required is None


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize(
    "activity", [Activity.EMPLOYEES, Activity.ONLINE_SALES, Activity.REAL_PROPERTY]
)
def test_unspecified_business_facts_require_review(target, activity):
    result = audit(target, {Activity.INTERSTATE_COMMERCE, activity})
    assert result.decision is QualificationDecision.REVIEW_REQUIRED
    assert result.qualification_required is None
    assert result.foreign_filing_required is None
    assert result.registered_agent_required is None
    assert result.registered_agent_appointment_required is None


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_income_producing_property_uses_the_explicit_entity_specific_statute(target, entity_type):
    result = audit(target, {Activity.INCOME_PRODUCING_PROPERTY}, entity_type)
    if (target, entity_type) in {
        ("CA", EntityType.LP),
        ("FL", EntityType.LLC),
        ("FL", EntityType.LP),
    }:
        assert result.decision is QualificationDecision.REQUIRED
        assert result.foreign_filing_required is True
    else:
        assert result.decision is QualificationDecision.REVIEW_REQUIRED
        assert result.foreign_filing_required is None


@pytest.mark.parametrize("target", STATES)
def test_missing_activity_facts_are_not_a_safe_harbor(target):
    assert audit(target, set()).decision is QualificationDecision.REVIEW_REQUIRED


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_isolated_transactions_need_known_duration_and_nonrepetition(target, entity_type):
    rule = DEFAULT_REGISTRY.get(target).for_entity(entity_type)
    limit = rule.threshold.isolated_transaction_max_days
    entity = entity_for(target, entity_type)
    unknown = ComplianceAudit(
        entity,
        target,
        BusinessPresence({Activity.ISOLATED_TRANSACTION}),
        as_of=AS_OF,
    ).evaluate()
    unlimited = rule.threshold.isolated_transaction_without_day_limit
    expected = (
        QualificationDecision.NOT_REQUIRED if unlimited else QualificationDecision.REVIEW_REQUIRED
    )
    assert unknown.decision is expected
    repeated = ComplianceAudit(
        entity,
        target,
        BusinessPresence({Activity.ISOLATED_TRANSACTION}, repeated_transactions=True),
        as_of=AS_OF,
    ).evaluate()
    assert repeated.decision is QualificationDecision.REVIEW_REQUIRED
    if unlimited:
        long_transaction = ComplianceAudit(
            entity,
            target,
            BusinessPresence({Activity.ISOLATED_TRANSACTION}, isolated_transaction_days=3650),
            as_of=AS_OF,
        ).evaluate()
        assert long_transaction.decision is QualificationDecision.NOT_REQUIRED
    if limit is None:
        return
    exempt = ComplianceAudit(
        entity,
        target,
        BusinessPresence({Activity.ISOLATED_TRANSACTION}, isolated_transaction_days=limit),
        as_of=AS_OF,
    ).evaluate()
    assert exempt.decision is QualificationDecision.NOT_REQUIRED
    for presence in (
        BusinessPresence({Activity.ISOLATED_TRANSACTION}, isolated_transaction_days=limit + 1),
        BusinessPresence(
            {Activity.ISOLATED_TRANSACTION},
            isolated_transaction_days=1,
            repeated_transactions=True,
        ),
    ):
        assert (
            ComplianceAudit(
                entity,
                target,
                presence,
                as_of=AS_OF,
            )
            .evaluate()
            .decision
            is QualificationDecision.REVIEW_REQUIRED
        )


@pytest.mark.parametrize("status", [EntityStatus.FORFEITED, EntityStatus.REVOKED])
@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_domestic_bad_status_blocks_filing_without_erasing_needed_remedies(
    status,
    target,
    entity_type,
):
    result = ComplianceAudit(
        entity_for(target, entity_type, status=status),
        target,
        BusinessPresence({Activity.OFFICE}),
        as_of=AS_OF,
    ).evaluate()
    assert result.qualification_required is True
    assert result.foreign_filing_required is True
    assert result.registered_agent_appointment_required is True
    assert result.domestic_reinstatement_required is True
    assert result.filing_blockers
    assert "domestic" in result.filing_blockers[0].lower()
    assert any("Resolve" in remedy for remedy in result.remedies)


@pytest.mark.parametrize("target", STATES)
def test_existing_foreign_registration_needs_continuing_agent_without_new_filing(target):
    result = audit(target, {Activity.INTERSTATE_COMMERCE}, is_qualified=True)
    assert result.foreign_filing_required is False
    assert result.registered_agent_required is True
    assert result.registered_agent_appointment_required is True
    valid_agent = RegisteredAgent("Service Agent", target, "123 Main Street")
    result = audit(target, {Activity.OFFICE}, is_qualified=True, registered_agent=valid_agent)
    assert result.foreign_filing_required is False
    assert result.registered_agent_required is True
    assert result.registered_agent_appointment_required is False


@pytest.mark.parametrize("target", STATES)
@pytest.mark.parametrize("failure", ["wrong_state", "po_box", "not_physical"])
def test_registered_agent_address_must_be_physical_and_in_target_state(target, failure):
    agent = RegisteredAgent(
        "Service Agent",
        ("DE" if target != "DE" else "WY") if failure == "wrong_state" else target,
        "P.O. Box 100" if failure == "po_box" else "123 Main Street",
        is_physical_address=failure != "not_physical",
    )
    assert (
        audit(
            target,
            {Activity.OFFICE},
            registered_agent=agent,
        ).registered_agent_appointment_required
        is True
    )


def test_unimplemented_jurisdiction_fails_closed():
    with pytest.raises(UnsupportedJurisdictionError, match="OH"):
        audit("OH", {Activity.BANK_ACCOUNT})


@pytest.mark.parametrize("invalid_date", [datetime(2026, 1, 1), "2026-01-01"])
def test_audit_rejects_nondate_as_of(invalid_date):
    with pytest.raises(ValueError):
        ComplianceAudit(
            entity_for("CA"), "CA", BusinessPresence({Activity.OFFICE}), as_of=invalid_date
        )


def test_audit_cannot_precede_formation():
    with pytest.raises(ValueError, match="precedes formation"):
        ComplianceAudit(
            entity_for("CA"), "CA", BusinessPresence({Activity.OFFICE}), as_of=date(2019, 12, 31)
        )


def test_fixture_cross_border_expansions():
    cases = json.loads((Path(__file__).parent / "fixtures" / "expansions.json").read_text())
    for case in cases:
        entity = Entity(
            legal_name=case["legal_name"],
            entity_type=case["entity_type"],
            domestic_state=case["domestic_state"],
            formation_date=date.fromisoformat(case["formation_date"]),
            sos_entity_id=case["sos_entity_id"],
            status=case["status"],
        )
        result = ComplianceAudit(
            entity,
            case["target_state"],
            BusinessPresence(case["activities"]),
            is_qualified=case.get("is_qualified", False),
            as_of=AS_OF,
        ).evaluate()
        assert result.decision.value == case["decision"], case["legal_name"]
        assert result.foreign_filing_required == case["foreign_filing_required"]
        assert result.domestic_reinstatement_required == case["reinstatement_required"]
        assert bool(result.filing_blockers) == case["filing_blocked"]


def test_audit_preserves_unverified_source_warnings_in_a_custom_registry():
    from dataclasses import replace

    from us_new_entities.rules.registry import RulesRegistry

    original = DEFAULT_REGISTRY.get("CA")
    unverified = replace(
        original,
        sources=tuple(replace(source, verified_on=None) for source in original.sources),
        verification_issues=("The current filing fee still requires review.",),
    )
    result = ComplianceAudit(
        entity_for("CA"),
        "CA",
        BusinessPresence({Activity.OFFICE}),
        as_of=AS_OF,
    ).evaluate(RulesRegistry([unverified]))
    assert any("not been live verified" in warning for warning in result.warnings)
    assert "The current filing fee still requires review." in result.warnings


def test_verified_sources_with_an_unresolved_conflict_still_warn_in_the_audit():
    from dataclasses import replace

    from us_new_entities.rules.registry import RulesRegistry

    original = DEFAULT_REGISTRY.get("CA")
    conflicted = replace(
        original,
        sources=tuple(replace(source, verified_on=AS_OF) for source in original.sources),
        verification_issues=("Two reviewed official sources disagree about a late fee.",),
    )
    result = ComplianceAudit(
        entity_for("CA"),
        "CA",
        BusinessPresence({Activity.OFFICE}),
        as_of=AS_OF,
    ).evaluate(RulesRegistry([conflicted]))
    assert conflicted.sources_verified
    assert not conflicted.rules_verified
    assert "Two reviewed official sources disagree about a late fee." in result.warnings
