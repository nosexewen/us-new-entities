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
    qualification_citation="RSA 304-C:175",
    threshold=QualificationThreshold(
        citation="RSA 304-C:174",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for registration",
            "FLLC-1",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/limited-liability-companies",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "RSA 304-C:180",
        "Cannot maintain proceedings until registered and fees for the unauthorized "
        "period are paid; liable for fees and penalties for each year or part. No "
        "fixed daily qualification fine is specified.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "January 1 through April 1, beginning the following year; registration from "
                "December 1 of the preceding year through April 1 of the current year skips "
                "the current-year report."
            ),
            fee=Decimal("100"),
            citation="RSA 304-C:194, 304-C:191",
            notes="$50 late fee after April 1; $2 electronic handling charge is separate.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application affirms home-jurisdiction good standing; the reviewed statute "
        "does not require a certificate attachment or numeric freshness limit."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="RSA 293-A:15.01, 15.03",
    threshold=QualificationThreshold(
        citation="RSA 293-A:15.01(b)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Form 40",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/domestic-and-foreign-corporation",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "RSA 293-A:15.02",
        "Cannot maintain proceedings until authorized; liable for fees and penalties "
        "for each year or part of unauthorized business. Contracts and defenses "
        "remain valid; no fixed daily qualification fine is specified.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "January 1 through April 1, beginning the following year; authorization from "
                "December 1 of the preceding year through April 1 of the current year skips "
                "the current-year report."
            ),
            fee=Decimal("100"),
            citation="RSA 293-A:16.21, 1.22",
            notes="$50 late fee after April 1; $2 electronic handling charge is separate.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application affirms home-jurisdiction good standing under the current § "
        "15.03; do not impose an obsolete certificate attachment requirement."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="New Hampshire SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="New Hampshire SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LP",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/limited-partnerships",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "New Hampshire SOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="NH",
    name="New Hampshire",
    registered_agent=RegisteredAgentRequirement(
        citation="RSA 304-C:177; 293-A:5.01, 15.03",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Chapter 304-C LIMITED LIABILITY COMPANIES",
            "https://gc.nh.gov/rsa/html/XXVIII/304-C/304-C-mrg.htm",
        ),
        source(
            "Chapter 293-A NEW HAMPSHIRE BUSINESS CORPORATION ACT",
            "https://gc.nh.gov/rsa/html/xxvii/293-a/293-a-mrg.htm",
        ),
        source(
            "Limited Liability Companies | New Hampshire Secretary of State",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/limited-liability-companies",
        ),
        source(
            "Domestic and Foreign Corporation | New Hampshire Secretary of State",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/domestic-and-foreign-corporation",
        ),
        source(
            "Limited Partnerships | New Hampshire Secretary of State",
            "https://www.sos.nh.gov/corporations-0/forms-and-fees/limited-partnerships",
        ),
    ),
    version="2026-10-11-batch6",
    notes=(
        "LLC and for-profit corporate foreign registration each cost $100. Annual "
        "reports cost $100; reports received after April 1 add a $50 late fee. SOS "
        "online filings add a $2 electronic handling charge.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
