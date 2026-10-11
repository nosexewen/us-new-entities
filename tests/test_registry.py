from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest
from us_new_entities.models import EntityType, StateRequirement
from us_new_entities.rules.registry import (
    DEFAULT_REGISTRY,
    RulesRegistry,
    UnsupportedJurisdictionError,
)

STATES = DEFAULT_REGISTRY.states


def test_registry_covers_exactly_twenty_populated_states():
    assert DEFAULT_REGISTRY.states == (
        "AK",
        "AL",
        "AR",
        "AZ",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "IA",
        "ID",
        "IL",
        "IN",
        "NC",
        "NY",
        "TX",
        "WA",
        "WY",
    )


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_each_state_type_has_a_complete_rule_and_source_provenance(state, entity_type):
    requirement = DEFAULT_REGISTRY.get(state)
    rule = requirement.for_entity(entity_type)
    assert rule.entity_type is entity_type
    assert rule.qualification_citation
    assert rule.threshold.citation
    assert rule.qualification_penalty.citation
    assert rule.qualification_penalty.description
    assert isinstance(rule.filing_fee, Decimal)
    assert rule.filing_fee > 0
    assert rule.forms
    for form in rule.forms:
        assert form.name
        assert form.identifier
        assert form.url.startswith("https://")
    assert rule.consequences
    assert requirement.sources
    for source in requirement.sources:
        assert source.citation
        assert source.url.startswith("https://")
    assert requirement.registered_agent.physical_in_state_address is True
    assert requirement.registered_agent.po_boxes_allowed is False
    assert requirement.registered_agent.citation


@pytest.mark.parametrize(
    ("name", "state"),
    [
        (" california ", "CA"),
        ("Delaware", "DE"),
        ("texas", "TX"),
        ("Florida", "FL"),
        ("wyoming", "WY"),
    ],
)
def test_registry_lookup_accepts_full_names(name, state):
    assert DEFAULT_REGISTRY.get(name) is DEFAULT_REGISTRY.get(state)


def test_registry_does_not_default_to_another_states_rules():
    with pytest.raises(UnsupportedJurisdictionError, match="NJ"):
        DEFAULT_REGISTRY.get("New Jersey")
    with pytest.raises(ValueError):
        DEFAULT_REGISTRY.get("ZZ")
    with pytest.raises(UnsupportedJurisdictionError):
        RulesRegistry([]).get("CA")


def test_duplicate_state_rules_cannot_silently_replace_existing_rules():
    california = DEFAULT_REGISTRY.get("CA")
    with pytest.raises(ValueError, match="Duplicate"):
        RulesRegistry([california, california])


def test_state_requirement_copies_mapping_and_prevents_mutation():
    original = DEFAULT_REGISTRY.get("CA")
    supplied = dict(original.entity_rules)
    snapshot = replace(original, entity_rules=supplied)
    supplied.clear()
    assert set(snapshot.entity_rules) == set(EntityType)
    with pytest.raises(TypeError):
        snapshot.entity_rules[EntityType.LLC] = original.for_entity(EntityType.LP)


def test_state_requirement_requires_all_types_and_matching_keys():
    original = DEFAULT_REGISTRY.get("CA")
    missing = dict(original.entity_rules)
    del missing[EntityType.LP]
    with pytest.raises(ValueError, match="cover"):
        replace(original, entity_rules=missing)
    mismatch = dict(original.entity_rules)
    mismatch[EntityType.LLC] = original.for_entity(EntityType.LP)
    with pytest.raises(ValueError, match="does not match"):
        replace(original, entity_rules=mismatch)


def test_state_requirement_cannot_drop_sources():
    with pytest.raises(ValueError, match="provenance"):
        replace(DEFAULT_REGISTRY.get("CA"), sources=())


def test_source_verification_status_tracks_every_source():
    original = DEFAULT_REGISTRY.get("CA")
    verified = tuple(replace(source, verified_on=date(2026, 10, 10)) for source in original.sources)
    assert replace(original, sources=verified).sources_verified
    assert not replace(original, sources=(replace(verified[0], verified_on=None),)).sources_verified


def test_state_requirement_is_the_exported_model():
    assert all(isinstance(DEFAULT_REGISTRY.get(state), StateRequirement) for state in STATES)


@pytest.mark.parametrize(
    ("state", "llc_fee", "corporation_fee", "lp_fee"),
    [
        ("CA", "70", "100", "70"),
        ("DE", "200", "245", "200"),
        ("FL", "125", "70", "1000"),
        ("TX", "750", "750", "750"),
        ("WY", "150", "150", "150"),
    ],
)
def test_initial_filing_fees_are_type_specific(state, llc_fee, corporation_fee, lp_fee):
    requirement = DEFAULT_REGISTRY.get(state)
    assert requirement.for_entity(EntityType.LLC).filing_fee == Decimal(llc_fee)
    assert requirement.for_entity(EntityType.C_CORP).filing_fee == Decimal(corporation_fee)
    assert requirement.for_entity(EntityType.LP).filing_fee == Decimal(lp_fee)


def test_california_reporting_cycles_do_not_impose_corporate_rules_on_llcs_or_lps():
    requirement = DEFAULT_REGISTRY.get("CA")
    corporate_reports = [
        item
        for item in requirement.for_entity(EntityType.C_CORP).annual_obligations
        if item.name == "Statement of Information"
    ]
    llc_reports = [
        item
        for item in requirement.for_entity(EntityType.LLC).annual_obligations
        if item.name == "Statement of Information"
    ]
    lp_reports = [
        item
        for item in requirement.for_entity(EntityType.LP).annual_obligations
        if item.name == "Statement of Information"
    ]
    assert len(corporate_reports) == 1
    assert corporate_reports[0].cycle == "annual"
    assert corporate_reports[0].fee == Decimal("25")
    assert len(llc_reports) == 1
    assert llc_reports[0].cycle == "biennial"
    assert llc_reports[0].fee == Decimal("20")
    assert not lp_reports


def test_delaware_foreign_corporation_report_is_distinct_from_alternative_entity_tax():
    requirement = DEFAULT_REGISTRY.get("DE")
    corporation = requirement.for_entity(EntityType.C_CORP).annual_obligations
    assert len(corporation) == 1
    assert corporation[0].fee == Decimal("250")
    assert "June 30" in corporation[0].due_rule
    for entity_type in (EntityType.LLC, EntityType.LP):
        obligations = requirement.for_entity(entity_type).annual_obligations
        assert len(obligations) == 1
        assert obligations[0].fee == Decimal("400")
        assert "June 1" in obligations[0].due_rule


def test_verified_sources_and_resolved_rules_are_separate_findings():
    original = DEFAULT_REGISTRY.get("CA")
    reviewed = replace(
        original,
        sources=tuple(
            replace(source, verified_on=date(2026, 10, 10)) for source in original.sources
        ),
        verification_issues=(),
    )
    assert reviewed.sources_verified
    assert reviewed.rules_verified
    conflict = replace(
        reviewed, verification_issues=("An official fee conflict remains unresolved.",)
    )
    assert conflict.sources_verified
    assert not conflict.rules_verified
    unverified = replace(reviewed, sources=(replace(reviewed.sources[0], verified_on=None),))
    assert not unverified.sources_verified
    assert not unverified.rules_verified


@pytest.mark.parametrize("entity_type", list(EntityType))
def test_texas_uses_public_information_report_for_all_three_entity_types(entity_type):
    obligations = DEFAULT_REGISTRY.get("TX").for_entity(entity_type).annual_obligations
    assert any("Public Information Report" in item.name for item in obligations)
    assert not any("Ownership Information Report" in item.name for item in obligations)
