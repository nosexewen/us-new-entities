"""Entity-specific regressions for the eighth source-backed state batch."""

from datetime import date
from decimal import Decimal

import pytest
from test_state_batch import screen
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.models import Activity, EntityType, QualificationDecision
from us_new_entities.rules import DEFAULT_REGISTRY

BATCH = ("RI", "SC", "SD", "TN", "UT")
TYPES = (EntityType.LLC, EntityType.C_CORP)


@pytest.mark.parametrize(
    "state,llc,corp,lp",
    [
        ("RI", "150", "310", "100"),
        ("SC", "110", "135", "10"),
        ("SD", "750", "750", "125"),
        ("TN", "300", "600", "600"),
        ("UT", "59", "59", "70"),
    ],
)
def test_foreign_fees_and_documented_minimums(state, llc, corp, lp):
    r = DEFAULT_REGISTRY.get(state)
    assert tuple(r.for_entity(e).filing_fee for e in EntityType) == tuple(
        Decimal(fee) for fee in (llc, corp, lp)
    )


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_ten_active_guides_have_citations_and_carry_review_status(state, entity):
    r = DEFAULT_REGISTRY.get(state)
    page = LandingPageGenerator(base_url="https://us-new-entities.pages.dev").generate(
        state, entity
    )
    for content in (page.html, page.markdown):
        assert "Guide coming soon." not in content
        assert r.for_entity(entity).qualification_citation in content
        if state == "TN":
            assert "user accepted" in content
            assert "Primary statutory review remains open" not in content
    assert 'content="noindex, follow"' not in page.html
    assert r.rules_verified and not r.verification_issues
    assert r.sources_verified
    assert all(s.verified_on == date(2026, 10, 11) for s in r.sources)


@pytest.mark.parametrize("state", ["RI", "SC", "SD"])
@pytest.mark.parametrize("entity", TYPES)
def test_thirty_day_safe_harbors_have_a_real_boundary(state, entity):
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 30).decision is (
        QualificationDecision.NOT_REQUIRED
    )
    assert screen(state, entity, Activity.ISOLATED_TRANSACTION, 31).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


@pytest.mark.parametrize("state", ["TN", "UT"])
@pytest.mark.parametrize("entity", TYPES)
def test_calendar_month_and_ordinary_course_conditions_are_not_day_counts(state, entity):
    rule = DEFAULT_REGISTRY.get(state).for_entity(entity)
    assert rule.threshold.isolated_transaction_max_days is None
    assert not rule.threshold.isolated_transaction_without_day_limit
    for duration in (1, 30, 31, 60):
        assert screen(state, entity, Activity.ISOLATED_TRANSACTION, duration).decision is (
            QualificationDecision.REVIEW_REQUIRED
        )
    assert ("one calendar month" if state == "TN" else "ordinary course") in rule.threshold.notes


@pytest.mark.parametrize("state", ["SC", "SD"])
def test_income_property_trigger_is_not_copied_from_llcs_to_corporations(state):
    assert screen(state, EntityType.LLC, Activity.INCOME_PRODUCING_PROPERTY).qualification_required
    assert screen(state, EntityType.C_CORP, Activity.INCOME_PRODUCING_PROPERTY).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


def test_rhode_island_share_license_minimum_reports_and_tax_are_distinct():
    r = DEFAULT_REGISTRY.get("RI")
    assert "$150 filing plus $160 license" in r.notes[0]
    assert "one-fifth cent" in r.notes[0]
    for entity in TYPES:
        rule = r.for_entity(entity)
        report, tax = rule.annual_obligations
        assert "February 1 through May 1" in report.due_rule
        assert "calendar year after" in report.due_rule
        assert report.fee == Decimal("50")
        assert "$25" in report.notes and "June 1" in report.notes
        assert tax.fee is None and "$400" in tax.notes
        assert "60 days" in rule.good_standing_evidence


def test_south_carolina_corporate_dor_report_and_initial_license_are_separate():
    r = DEFAULT_REGISTRY.get("SC")
    assert not r.for_entity(EntityType.LLC).annual_obligations
    corp = r.for_entity(EntityType.C_CORP)
    report = corp.annual_obligations[0]
    assert "DOR" in report.name and "April 15" in report.due_rule
    assert report.fee is None and "minimum $25" in report.notes
    assert "CL-1" in corp.initial_report and "$135" in corp.initial_report
    assert "$10" in corp.qualification_penalty.description
    assert "$1,000" in corp.qualification_penalty.description


@pytest.mark.parametrize("entity", TYPES)
def test_south_dakota_current_fees_and_future_deadline_are_explicit(entity):
    r = DEFAULT_REGISTRY.get("SD")
    report = r.for_entity(entity).annual_obligations[0]
    assert report.fee == Decimal("55")
    assert "February 1 (January 31)" in report.due_rule
    assert "calendar year after authorization" in report.due_rule
    assert "paper $70" in report.notes and "$55" in report.notes
    assert "January 1, 2027" in report.notes
    assert "formation-anniversary month or January 31" in report.notes
    assert "$765" in r.notes[0] and "$800" in r.notes[0]
    assert "Original one-page" in r.for_entity(entity).good_standing_evidence
    assert "no numeric freshness" in r.for_entity(entity).good_standing_evidence or (
        "no numeric freshness" in r.for_entity(entity).good_standing_evidence.lower()
    )
    if entity == EntityType.C_CORP:
        assert "$100" in r.for_entity(entity).qualification_penalty.description
        assert "$1,000" in r.for_entity(entity).qualification_penalty.description


def test_tennessee_member_fees_penalty_formulas_and_month_freshness_differ():
    r = DEFAULT_REGISTRY.get("TN")
    llc, corp = (r.for_entity(e) for e in TYPES)
    assert llc.annual_obligations[0].fee is None
    assert "$50 per member" in llc.annual_obligations[0].notes
    assert "$3,000" in llc.annual_obligations[0].notes
    assert corp.annual_obligations[0].fee == Decimal("20")
    assert "three times" in llc.qualification_penalty.description
    assert "treble fees, penalties and taxes" in corp.qualification_penalty.description
    for rule in (llc, corp):
        assert "two calendar months" in rule.good_standing_evidence
        assert "April 1" in rule.annual_obligations[0].due_rule
    assert r.rules_verified and not r.verification_issues
    assert any("user accepted" in text and "Justia" in text for text in r.review_disclosures)


@pytest.mark.parametrize("entity", TYPES)
def test_utah_october_recodification_certificate_deadline_and_portal_fee(entity):
    r = DEFAULT_REGISTRY.get("UT")
    rule = r.for_entity(entity)
    assert "16-1a-503" in rule.qualification_citation
    assert "16-1a-506" in rule.threshold.citation
    assert "90 days" in rule.good_standing_evidence
    assert "October 1, 2026" in rule.good_standing_evidence
    report = rule.annual_obligations[0]
    assert "Last day of the anniversary month" in report.due_rule
    assert "60 days earlier" in report.due_rule
    assert report.fee == Decimal("18")
    assert "includes the $5" in report.notes
    assert any("16-1a-S504" in s.url for s in r.sources)
    assert not any("48-3a-S902" in s.url for s in r.sources)


@pytest.mark.parametrize("state", BATCH)
@pytest.mark.parametrize("entity", TYPES)
def test_penalties_remain_manual_when_required_facts_are_missing(state, entity):
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
    assert screen(state, EntityType.LP, Activity.BANK_ACCOUNT).decision is (
        QualificationDecision.REVIEW_REQUIRED
    )


def test_cited_sources_have_substantive_retrieval_records_and_secondary_labels():
    import json
    from pathlib import Path

    manifest = json.loads(
        (
            Path(__file__).parents[1] / "docs/verification/batch8-2026-10-11-retrievals.json"
        ).read_text()
    )
    accepted = {r["requested_url"]: r for r in manifest["retrievals"] if r["accepted"]}
    for state in BATCH:
        for source in DEFAULT_REGISTRY.get(state).sources:
            row = accepted[source.url]
            assert row["status_code"] == 200 and row["content_characters"] > 500
            assert len(row["content_sha256"]) == 64
            assert row["reviewed_on"] == "2026-10-11"
            if "law.justia.com" in source.url:
                assert state == "TN" and row["source_kind"] == "secondary_statute"
    assert manifest["primary_review_open"] == []
    assert manifest["user_accepted_secondary_review"] == ["TN"]
