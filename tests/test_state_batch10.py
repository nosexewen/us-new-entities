"""Maryland statutory distinctions and completion of the fifty-state directory."""

import json
from datetime import date
from decimal import Decimal
from html import unescape
from pathlib import Path

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.models.entity import STATE_NAMES
from us_new_entities.rules import DEFAULT_REGISTRY

TYPES = (EntityType.LLC, EntityType.C_CORP)


def test_registry_populates_exactly_all_fifty_states_without_dc():
    assert set(DEFAULT_REGISTRY.states) == set(STATE_NAMES) - {"DC"}
    assert len(DEFAULT_REGISTRY.states) == 50


@pytest.mark.parametrize("entity", TYPES)
def test_maryland_guides_replace_last_placeholders_with_reviewed_statutory_content(entity):
    r = DEFAULT_REGISTRY.get("Maryland")
    assert r.rules_verified and r.sources_verified and not r.verification_issues
    assert all(s.verified_on == date(2026, 10, 11) for s in r.sources)
    page = LandingPageGenerator().generate("MD", entity)
    for content in (page.html, page.markdown):
        assert "Guide coming soon." not in content
        assert r.for_entity(entity).qualification_citation in unescape(content)
        assert "1-203(b)(3)(ii)" in content and "11-101" in content
        assert "April 15" in content and "$300" in content
        assert "60 days" in content and "$200" in content
    assert "GovernmentService" in page.html and "noindex, follow" not in page.html
    graph = page.json_ld["@graph"]
    service = next(node for node in graph if node["@type"] == "GovernmentService")
    assert service["provider"]["name"] == "Maryland Department of Assessments and Taxation"
    assert service["provider"]["url"] == "https://dat.maryland.gov/"
    faq = next(node for node in graph if node["@type"] == "FAQPage")
    assert "SDAT" in json.dumps(faq) and "New York" not in json.dumps(faq)


@pytest.mark.parametrize("entity", list(EntityType))
def test_base_foreign_filing_fee_is_one_hundred_dollars(entity):
    assert DEFAULT_REGISTRY.get("MD").for_entity(entity).filing_fee == Decimal("100")


@pytest.mark.parametrize("entity", TYPES)
def test_annual_report_fee_is_separate_from_property_tax_and_nonregistration_penalty(entity):
    obligation = DEFAULT_REGISTRY.get("MD").for_entity(entity).annual_obligations[0]
    assert obligation.name.startswith("Form 1") and obligation.cycle == "annual"
    assert obligation.fee == Decimal("300")
    assert "April 15" in obligation.due_rule
    for term in (
        "property assessment or tax",
        "60-day extension",
        "June 15",
        "MarylandSaves",
        "$0 fee for a foreign interstate corporation",
        "not a universal annual-report late fee",
    ):
        assert term in obligation.notes
    assert "1-203(b)(3)(ii)" in obligation.citation and "11-101" in obligation.citation


@pytest.mark.parametrize("entity", TYPES)
def test_interstate_business_still_requires_registration(entity):
    result = screen("MD", entity, Activity.INTERSTATE_COMMERCE)
    assert result.decision == QualificationDecision.REQUIRED
    assert result.foreign_filing_required
    notes = DEFAULT_REGISTRY.get("MD").for_entity(entity).threshold.notes
    assert "interstate/foreign-business registration" in notes
    if entity == EntityType.C_CORP:
        assert "7-103 excludes interstate-only" in notes and "7-202 still requires" in notes


@pytest.mark.parametrize("entity", TYPES)
def test_isolated_transaction_has_no_invented_thirty_day_limit(entity):
    threshold = DEFAULT_REGISTRY.get("MD").for_entity(entity).threshold
    assert threshold.isolated_transaction_without_day_limit
    assert threshold.isolated_transaction_max_days is None
    for duration in (30, 31, 365):
        assert (
            screen("MD", entity, Activity.ISOLATED_TRANSACTION, duration).decision
            == QualificationDecision.NOT_REQUIRED
        )


@pytest.mark.parametrize("entity", TYPES)
@pytest.mark.parametrize("activity", (Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS))
def test_reviewed_statutory_exemptions_remain_exempt(entity, activity):
    assert screen("MD", entity, activity).decision == QualificationDecision.NOT_REQUIRED


@pytest.mark.parametrize("entity", TYPES)
def test_solicitation_is_not_inherited_as_an_unreviewed_exemption(entity):
    assert (
        screen("MD", entity, Activity.SOLICITATION).decision
        == QualificationDecision.REVIEW_REQUIRED
    )


def test_llc_income_property_trigger_is_not_copied_into_corporate_rules():
    assert screen("MD", EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert (
        screen("MD", EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY).decision
        == QualificationDecision.REVIEW_REQUIRED
    )
    assert (
        "foreclosure/default-acquired"
        in DEFAULT_REGISTRY.get("MD").for_entity(EntityType.LLC).threshold.notes
    )


@pytest.mark.parametrize("entity", TYPES)
def test_private_agent_is_optional_but_statutory_service_remains(entity):
    r = DEFAULT_REGISTRY.get("MD")
    assert not r.registered_agent.private_appointment_required
    assert r.registered_agent.physical_in_state_address and not r.registered_agent.po_boxes_allowed
    assert "no additional fee" in r.registered_agent.notes
    result = screen("MD", entity, Activity.OFFICE)
    assert not result.registered_agent_required
    assert any("Department" in reason or "SDAT" in reason for reason in result.reasons)
    assert not result.registered_agent_appointment_required


@pytest.mark.parametrize("entity", TYPES)
def test_certificate_freshness_is_sixty_days_for_each_current_foreign_form(entity):
    assert "60 days" in DEFAULT_REGISTRY.get("MD").for_entity(entity).good_standing_evidence


@pytest.mark.parametrize("entity", TYPES)
def test_nonregistration_penalty_is_distinct_from_individual_criminal_fines(entity):
    penalty = DEFAULT_REGISTRY.get("MD").for_entity(entity).qualification_penalty
    for term in (
        "$200",
        "$1,000",
        "misdemeanor conviction",
        "reducible or abatable",
        "not a $200 per-day/year",
        "annual-report late fee",
        "ceased Maryland business",
    ):
        assert term in penalty.description
    assert ("member" if entity == EntityType.LLC else "officer") in penalty.description
    estimate = penalty.estimate(date(2024, 1, 1), date(2026, 10, 11))
    assert estimate.exact_amount is None and estimate.unresolved
    if entity == EntityType.LLC:
        assert "4A-1007" in penalty.citation
        assert "Contracts and defense remain valid" in penalty.description
    else:
        assert "7-301" in penalty.citation and "7-302" in penalty.citation


def test_lp_filing_stub_does_not_claim_full_llc_statutory_review():
    lp = DEFAULT_REGISTRY.get("MD").for_entity(EntityType.LP)
    assert "1-203(b)(3)(i)" in lp.qualification_citation
    assert not lp.annual_obligations
    assert "separate entity-specific review" in lp.threshold.notes
    assert (
        screen("MD", EntityType.LP, Activity.BANK_ACCOUNT).decision
        == QualificationDecision.REVIEW_REQUIRED
    )


def test_every_cited_source_has_substantive_official_retrieval_provenance():
    manifest = json.loads(
        (
            Path(__file__).parents[1] / "docs/verification/batch10-2026-10-11-retrievals.json"
        ).read_text()
    )
    assert manifest["remaining_coming_soon"] == [] and manifest["primary_review_open"] == []
    assert manifest["populated_states"] == 50
    accepted = {r["requested_url"]: r for r in manifest["retrievals"] if r["accepted"]}
    for source in DEFAULT_REGISTRY.get("MD").sources:
        row = accepted[source.url]
        assert row["status_code"] == 200 and row["content_characters"] > 1000
        assert row["source_kind"] in {"primary_statute", "official_agency"}
        assert len(row["content_sha256"]) == 64
        assert row["reviewed_on"] == "2026-10-11"
    assert not next(r for r in manifest["retrievals"] if r["key"] == "4a-210")["accepted"]
    assert not next(r for r in manifest["retrievals"] if r["key"] == "7-303")["accepted"]
