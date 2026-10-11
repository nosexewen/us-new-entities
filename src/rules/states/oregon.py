"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

from decimal import Decimal

from ...models import (
    AnnualObligation,
    EntityRequirement,
    EntityType,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)
from ._shared import source, unresolved_penalty

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="ORS §§ 63.701, 63.707",
    threshold=QualificationThreshold(
        citation="ORS § 63.701(2)",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("275"),
    forms=(
        StateForm(
            "Application for authority to transact business",
            "Form 110",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/fllc-authority.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "ORS § 63.704",
        "Cannot maintain proceedings until authorized; liable for fees that would "
        "have applied during each year or part of unauthorized business, including "
        "report fees. Contracts and defenses remain valid; no fixed daily fine is "
        "supplied.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report / renewal",
            cycle="annual",
            due_rule="By the anniversary of authority each year.",
            fee=Decimal("275"),
            citation="ORS § 63.787; Oregon SOS Business Registry Fee Schedule",
            notes="Foreign renewal is $275; domestic LLC renewal is $100.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Certificate of existence current within 60 days, unless a web-verifiable "
        "home registry number provides the qualifying status information under § "
        "63.707(2) and SOS Form 110."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="ORS §§ 60.701, 60.707",
    threshold=QualificationThreshold(
        citation="ORS § 60.701(2)",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("275"),
    forms=(
        StateForm(
            "Application for authority to transact business",
            "Foreign business corporation",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/fbc-authority.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "ORS § 60.704",
        "Cannot maintain proceedings until authorized; liable for fees that would "
        "have applied during each year or part of unauthorized business, including "
        "report fees. Contracts and defenses remain valid; no fixed daily fine is "
        "supplied.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report / renewal",
            cycle="annual",
            due_rule="By the anniversary of authority each year.",
            fee=Decimal("275"),
            citation="ORS § 60.787; Oregon SOS Business Registry Fee Schedule",
            notes="Foreign renewal is $275; domestic corporate renewal is $100.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Certificate of existence current within 60 days, unless a web-verifiable "
        "home registry number provides the qualifying status information under § "
        "60.707(2) and the SOS corporate application."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Oregon SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="Oregon SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("275"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/br-fee-schedule.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Oregon SOS foreign LP fee schedule", "LP sanctions require separate review."
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence="Review LP evidence requirements independently.",
    initial_report=None,
)
REQUIREMENT = StateRequirement(
    state="OR",
    name="Oregon",
    registered_agent=RegisteredAgentRequirement(
        citation="ORS §§ 63.721, 60.721",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Oregon Revised Statutes",
            "https://www.oregonlegislature.gov/bills_laws/ors/ors063.html",
        ),
        source(
            "Oregon Revised Statutes",
            "https://www.oregonlegislature.gov/bills_laws/ors/ors060.html",
        ),
        source(
            "Application for Authority to Transact—Foreign Limited Liability Company",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/fllc-authority.pdf",
        ),
        source(
            "Application for Authority to Transact Business—Business/Professional",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/fbc-authority.pdf",
        ),
        source(
            "Business Registry Fee Schedule",
            "https://sos.oregon.gov/business/Documents/business-registry-forms/br-fee-schedule.pdf",
        ),
        source(
            "Business Registration Forms | <br>\tOregon Secretary of State | State of Oregon<br>",
            "https://sos.oregon.gov/business/register/pages/business-registration-forms.aspx",
        ),
        source(
            "Annual Report or Renewal | <br>\tOregon Secretary of State | State of Oregon<br>",
            "https://sos.oregon.gov/business/pages/obr-annual-report-renewal.aspx",
        ),
    ),
    version="2026-10-11-batch7",
    notes=(
        "Foreign LLC authority and foreign for-profit corporate authority each cost "
        "$275. Their annual renewal also costs $275; do not use the $100 domestic "
        "renewal fee. The SOS forms allow a web-verifiable home registry number "
        "instead of a certificate where qualifying status information is accessible.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
