"""Foreign-entity regressions for the ninth source-backed batch."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("VT", "VA", "WV", "WI")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp,lp",
    [
        ("VT", "155", "155", "155"),
        ("VA", "100", "75", "100"),
        ("WV", "150", "100", "150"),
        ("WI", "100", "100", "75"),
    ],
)
def test_foreign_registration_fees_and_variable_minimums(state, llc, corp, lp):
    r = DEFAULT_REGISTRY.get(state)
    assert tuple(r.for_entity(e).filing_fee for e in EntityType) == tuple(
        Decimal(v) for v in (llc, corp, lp)
    )


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_active_guides_include_reviewed_sources_and_entity_specific_rules(state, entity):
    r = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for content in (page.html, page.markdown):
        assert "Guide coming soon." not in content
        assert r.for_entity(entity).qualification_citation in content
    assert 'content="noindex, follow"' not in page.html
    assert r.rules_verified and r.sources_verified and not r.verification_issues
    assert all(s.verified_on == date(2026, 10, 11) for s in r.sources)


@pytest.mark.parametrize("state,entity", [("VT", e) for e in TYPES] + [("WI", EntityType.LLC)])
def test_unlimited_isolated_transactions_do_not_inherit_thirty_day_caps(state, entity):
    rule = DEFAULT_REGISTRY.get(state).for_entity(entity)
    assert rule.threshold.isolated_transaction_without_day_limit
    assert rule.threshold.isolated_transaction_max_days is None
    for days in (30, 31, 365):
        assert (
            screen(state, entity, Activity.ISOLATED_TRANSACTION, days).decision
            == QualificationDecision.NOT_REQUIRED
        )


@pytest.mark.parametrize(
    "state,entity", [(st, e) for st in ("VA", "WV") for e in TYPES] + [("WI", EntityType.C_CORP)]
)
def test_thirty_day_safe_harbors_keep_their_boundary(state, entity):
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision
        == QualificationDecision.NOT_REQUIRED
    )
    assert (
        screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision
        == QualificationDecision.REVIEW_REQUIRED
    )


def test_vermont_foreign_report_fees_deadlines_and_certificate_ages_differ():
    r = DEFAULT_REGISTRY.get("VT")
    llc, corp = (r.for_entity(e) for e in TYPES)
    assert llc.annual_obligations[0].fee == Decimal("170")
    assert corp.annual_obligations[0].fee == Decimal("250")
    assert "March 31" in llc.annual_obligations[0].due_rule
    assert "March 15" in corp.annual_obligations[0].due_rule
    assert "90 days" in llc.good_standing_evidence
    assert "30 days" in corp.good_standing_evidence
    for rule in (llc, corp):
        assert "$50" in rule.qualification_penalty.description
        assert "$10,000" in rule.qualification_penalty.description
        assert "affirmative defenses" in rule.qualification_penalty.description
    assert "1655" in r.registered_agent.citation
    assert any("/11/015/01655" in s.url for s in r.sources)


def test_virginia_reports_fees_discrepancy_and_individual_penalties_are_separate():
    r = DEFAULT_REGISTRY.get("VA")
    llc, corp = (r.for_entity(e) for e in TYPES)
    assert len(llc.annual_obligations) == 1
    assert "no LLC annual report" in llc.annual_obligations[0].name
    assert llc.annual_obligations[0].fee == Decimal("50")
    report, assessment = corp.annual_obligations
    assert report.fee == Decimal("0") and assessment.fee is None
    for text in (assessment.notes, *r.review_disclosures):
        if "discrepancy" in text:
            assert "$50" in text and "$850" in text
            assert "$100" in text and "$1,700" in text
            assert "confirm" in text.lower()
    assert any("discrepancy" in text for text in r.review_disclosures)
    assert "$25 filing" in r.notes[0] and "$2,500" in r.notes[0]
    assert "Residency alone is insufficient" in r.registered_agent.notes
    for rule in (llc, corp):
        assert "$500–$5,000 each" in rule.qualification_penalty.description
        assert "12 months" in rule.good_standing_evidence
        assert (
            "good-standing" in rule.good_standing_evidence
            or "good standing" in rule.good_standing_evidence
        )
    assert "employees" in corp.qualification_penalty.description
    for entity in TYPES:
        page = LandingPageGenerator().generate("VA", entity)
        assert "annual corporate fee discrepancy" in page.html


@pytest.mark.parametrize("entity", TYPES)
def test_west_virginia_default_annual_reporting_and_conditional_biennial_election(entity):
    r = DEFAULT_REGISTRY.get("WV")
    obligation = r.for_entity(entity).annual_obligations[0]
    assert obligation.cycle == "annual" and obligation.fee == Decimal("25")
    assert "June 30" in obligation.due_rule and "following" not in obligation.due_rule
    for term in (
        "July 1, 2026",
        "five consecutive",
        "good standing",
        "$50",
        "$100",
        "2027",
        "second calendar year",
        "revoked",
    ):
        assert term in obligation.notes
    assert not r.registered_agent.private_appointment_required
    assert "MAY" in r.registered_agent.notes and "Secretary of State" in r.registered_agent.notes
    assert "60 days" not in r.for_entity(entity).good_standing_evidence


def test_west_virginia_income_property_and_corporate_fact_triggers_are_distinct():
    llc, corp = (DEFAULT_REGISTRY.get("WV").for_entity(e) for e in TYPES)
    assert Activity.INCOME_PRODUCING_PROPERTY in llc.threshold.trigger_activities
    assert Activity.INCOME_PRODUCING_PROPERTY not in corp.threshold.trigger_activities
    assert "torts" in corp.threshold.notes and "contract performance" in corp.threshold.notes


def test_wisconsin_foreign_quarter_paper_surcharge_and_capital_fees():
    r = DEFAULT_REGISTRY.get("WI")
    llc, corp = (r.for_entity(e) for e in TYPES)
    assert llc.annual_obligations[0].fee == Decimal("65")
    assert "$80" in llc.annual_obligations[0].notes
    assert "$15" in llc.annual_obligations[0].notes
    assert corp.annual_obligations[0].fee is None
    for rule in (llc, corp):
        assert "March 31" in rule.annual_obligations[0].due_rule
        assert "calendar year after" in rule.annual_obligations[0].due_rule
        assert "$5,000" in rule.qualification_penalty.description
    assert "$60,000" in corp.annual_obligations[0].notes
    assert "180.0122(1m)(u)" in corp.annual_obligations[0].notes
    assert "$97.50" in llc.qualification_penalty.description
    assert "do not require" in llc.good_standing_evidence
    assert "60 days" in corp.good_standing_evidence


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_unknown_penalty_inputs_do_not_produce_exact_estimates(state, entity):
    estimate = (
        DEFAULT_REGISTRY.get(state)
        .for_entity(entity)
        .qualification_penalty.estimate(date(2024, 1, 1), date(2026, 10, 11))
    )
    assert estimate.exact_amount is None and estimate.unresolved


@pytest.mark.parametrize("state", BATCH)
def test_lp_stubs_do_not_inherit_verified_llc_exemptions_or_reports(state):
    rule = DEFAULT_REGISTRY.get(state).for_entity(EntityType.LP)
    assert not rule.annual_obligations
    assert "separate entity-specific review" in rule.threshold.notes
    assert (
        screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision
        == QualificationDecision.REVIEW_REQUIRED
    )


def test_cited_sources_have_substantive_official_retrieval_evidence():
    manifest = json.loads(
        (
            Path(__file__).parents[1] / "docs/verification/batch9-2026-10-11-retrievals.json"
        ).read_text()
    )
    accepted = {r["requested_url"]: r for r in manifest["retrievals"] if r["accepted"]}
    for state in BATCH:
        for source in DEFAULT_REGISTRY.get(state).sources:
            row = accepted[source.url]
            assert row["status_code"] == 200 and row["content_characters"] > 1000
            assert row["source_kind"] in {"primary_statute", "official_agency"}
            assert len(row["content_sha256"]) == 64
            assert row["reviewed_on"] == "2026-10-11"
    assert manifest["primary_review_open"] == []
    assert manifest["remaining_coming_soon"] == ["MD"]
