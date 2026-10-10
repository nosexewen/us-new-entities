from dataclasses import FrozenInstanceError
from datetime import date, datetime
from decimal import Decimal

import pytest
from us_new_entities.models import (
    Activity,
    AnnualObligation,
    BusinessPresence,
    Entity,
    EntityStatus,
    EntityType,
    LegalSource,
    QualificationThreshold,
    RegisteredAgent,
    normalize_state,
)


def make_entity(**changes):
    values = {
        "legal_name": "  Acme LLC  ",
        "entity_type": "LLC",
        "domestic_state": " delaware ",
        "formation_date": date(2024, 2, 29),
        "sos_entity_id": "  001234  ",
        "status": "Good Standing",
    }
    return Entity(**(values | changes))


def test_entity_normalizes_identity_without_losing_leading_zeroes():
    entity = make_entity()
    assert entity.legal_name == "Acme LLC"
    assert entity.domestic_state == "DE"
    assert entity.sos_entity_id == "001234"
    assert entity.entity_type is EntityType.LLC
    assert entity.status is EntityStatus.GOOD_STANDING
    assert entity.formation_date == date(2024, 2, 29)
    with pytest.raises(FrozenInstanceError):
        entity.legal_name = "Renamed LLC"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("legal_name", " "),
        ("legal_name", None),
        ("entity_type", "S-Corp"),
        ("domestic_state", "Atlantis"),
        ("formation_date", "2024-02-29"),
        ("formation_date", datetime(2024, 2, 29)),
        ("sos_entity_id", " "),
        ("sos_entity_id", 1234),
        ("status", "Active"),
    ],
)
def test_entity_rejects_invalid_identity_fields(field, value):
    with pytest.raises(ValueError):
        make_entity(**{field: value})


def test_entity_can_have_unknown_registry_identifier():
    assert make_entity(sos_entity_id=None).sos_entity_id is None


@pytest.mark.parametrize(
    ("supplied", "expected"),
    [
        ("California", "CA"),
        ("  tX ", "TX"),
        ("new york", "NY"),
        ("District of Columbia", "DC"),
        ("Wyoming", "WY"),
    ],
)
def test_normalize_us_jurisdictions(supplied, expected):
    assert normalize_state(supplied) == expected


@pytest.mark.parametrize("value", ["ZZ", "Puerto Rico", "", None, 12])
def test_normalize_rejects_unsupported_or_malformed_jurisdictions(value):
    with pytest.raises(ValueError):
        normalize_state(value)


def test_business_presence_is_immutable_and_coerces_known_activity_values():
    supplied = {"operating_office"}
    presence = BusinessPresence(supplied)
    supplied.add("bank_account_only")
    assert presence.activities == frozenset({Activity.OFFICE})


@pytest.mark.parametrize("days", [0, -1, 1.5, True])
def test_isolated_duration_requires_positive_integer(days):
    with pytest.raises(ValueError):
        BusinessPresence({Activity.ISOLATED_TRANSACTION}, isolated_transaction_days=days)


def test_business_presence_rejects_unknown_activities_and_nonboolean_repetition():
    with pytest.raises(ValueError):
        BusinessPresence({"mysterious_activity"})
    with pytest.raises(ValueError):
        BusinessPresence({Activity.ISOLATED_TRANSACTION}, repeated_transactions="false")


def test_threshold_rejects_conflicting_exemptions():
    with pytest.raises(ValueError, match="both a trigger and an exemption"):
        QualificationThreshold(
            citation="test",
            trigger_activities={Activity.OFFICE},
            exempt_activities={Activity.OFFICE},
        )


def test_threshold_normalizes_declared_activities_and_rejects_unknown_values():
    threshold = QualificationThreshold(
        citation="test",
        trigger_activities={"operating_office"},
        exempt_activities={"interstate_commerce_only"},
    )
    assert next(iter(threshold.trigger_activities)) is Activity.OFFICE
    assert next(iter(threshold.exempt_activities)) is Activity.INTERSTATE_COMMERCE
    with pytest.raises(ValueError):
        QualificationThreshold(citation="test", trigger_activities={"unknown"})
    with pytest.raises(ValueError):
        QualificationThreshold(citation="test", exempt_activities={"unknown"})


@pytest.mark.parametrize("limit", [0, -1, True, 2.5])
def test_threshold_rejects_invalid_isolated_transaction_limits(limit):
    with pytest.raises(ValueError):
        QualificationThreshold(citation="test", isolated_transaction_max_days=limit)


def test_isolated_transaction_without_day_limit_is_boolean_and_cannot_also_have_a_limit():
    with pytest.raises(ValueError):
        QualificationThreshold(citation="test", isolated_transaction_without_day_limit="false")
    with pytest.raises(ValueError):
        QualificationThreshold(
            citation="test",
            isolated_transaction_max_days=30,
            isolated_transaction_without_day_limit=True,
        )


@pytest.mark.parametrize("address", ["PO Box 123", "P.O. Box 45", "Post Office Box 99"])
def test_registered_agent_identifies_post_office_boxes(address):
    agent = RegisteredAgent("Agent", "ca", address)
    assert agent.is_po_box
    assert agent.state == "CA"


def test_registered_agent_street_address_is_not_a_po_box():
    assert not RegisteredAgent("Agent", "TX", "100 Boxwood Street").is_po_box


@pytest.mark.parametrize("field", ["name", "street_address"])
def test_registered_agent_requires_nonempty_identity_and_address(field):
    values = {"name": "Agent", "state": "CA", "street_address": "1 Main Street"}
    values[field] = " "
    with pytest.raises(ValueError):
        RegisteredAgent(**values)


@pytest.mark.parametrize("fee", [Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 25.0])
def test_annual_obligation_rejects_invalid_money(fee):
    with pytest.raises(ValueError):
        AnnualObligation("Report", "annual", "May 1", fee, "test")


def test_source_provenance_requires_https_and_real_citation():
    with pytest.raises(ValueError):
        LegalSource("test", "http://example.org")
    with pytest.raises(ValueError):
        LegalSource(" ", "https://example.org")
    assert LegalSource("test", "https://example.org").verified_on is None
