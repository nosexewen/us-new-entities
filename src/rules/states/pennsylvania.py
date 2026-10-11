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
    qualification_citation="15 Pa.C.S. §§ 411, 412",
    threshold=QualificationThreshold(
        citation="15 Pa.C.S. § 403",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Foreign registration statement and docketing statement",
            "DSCB:15-412",
            "https://file.dos.pa.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "15 Pa.C.S. § 411(b)-(d)",
        "Cannot maintain proceedings until registered; contracts, defenses and "
        "liability limitations remain valid. Section 411 supplies no fixed monetary "
        "qualification fine; review other sanctions separately.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "January 1 through September 30, beginning the calendar year following "
                "registration."
            ),
            fee=Decimal("7"),
            citation="15 Pa.C.S. § 146; Pennsylvania DOS annual report guidance",
            notes=(
                "Annual reporting began in 2025. Administrative termination for missed "
                "reports begins with reports due in 2027, six months after the deadline."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "The registration and docketing statements do not require a home-jurisdiction "
        "good-standing certificate or articles attachment under § 412 and DOS "
        "guidance."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="15 Pa.C.S. §§ 411, 412",
    threshold=QualificationThreshold(
        citation="15 Pa.C.S. § 403",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Foreign registration statement and docketing statement",
            "DSCB:15-412",
            "https://file.dos.pa.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "15 Pa.C.S. § 411(b)-(d)",
        "Cannot maintain proceedings until registered; contracts, defenses and "
        "liability limitations remain valid. Section 411 supplies no fixed monetary "
        "qualification fine; review other sanctions separately.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "January 1 through June 30, beginning the calendar year following registration."
            ),
            fee=Decimal("7"),
            citation="15 Pa.C.S. § 146; Pennsylvania DOS annual report guidance",
            notes=(
                "Annual reporting began in 2025. Administrative termination for missed "
                "reports begins with reports due in 2027, six months after the deadline."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "DOS confirms no home-jurisdiction good-standing certificate or articles "
        "attachment is required with the registration and docketing statements."
    ),
    initial_report=(
        "Publish notice of intention to register or completed registration in two "
        "newspapers of general circulation, one a legal journal if possible, under 15 "
        "Pa.C.S. § 4124 and DOS guidance. Notice may precede or follow filing; retain "
        "proofs with corporate minutes rather than submit them to DOS. Publication "
        "charges vary."
    ),
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Pennsylvania DOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="Pennsylvania DOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.pa.gov/agencies/dos/programs/business/fees-and-payments",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Pennsylvania DOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="PA",
    name="Pennsylvania",
    registered_agent=RegisteredAgentRequirement(
        citation="15 Pa.C.S. §§ 109, 411(f), 412(a)(5)",
        notes=(
            "Maintain a Pennsylvania registered office with a physical street address or "
            "use the statutory commercial registered office provider (CROP) alternative. "
            "Pennsylvania does not require a separate private registered-agent "
            "appointment; a PO box alone is insufficient. Provider services are optional."
        ),
        private_appointment_required=False,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Chapter 4. - Title 15 - CORPORATIONS AND UNINCORPORATED ASSOCIATIONS",
            "https://www.legis.state.pa.us/WU01/LI/LI/CT/HTM/15/00.004..HTM",
        ),
        source(
            "Chapter 1. - Title 15 - CORPORATIONS AND UNINCORPORATED ASSOCIATIONS",
            "https://www.legis.state.pa.us/WU01/LI/LI/CT/HTM/15/00.001..HTM",
        ),
        source(
            "Chapter 41. - Title 15 - CORPORATIONS AND UNINCORPORATED ASSOCIATIONS",
            "https://www.legis.state.pa.us/WU01/LI/LI/CT/HTM/15/00.041..HTM",
        ),
        source(
            "Fees and Payments | Department of State | Commonwealth of Pennsylvania",
            "https://www.pa.gov/agencies/dos/programs/business/fees-and-payments",
        ),
        source(
            "Annual Reports | Department of State | Commonwealth of Pennsylvania",
            "https://www.pa.gov/agencies/dos/programs/business/types-of-filings-and-registrations/annual-reports",
        ),
        source(
            "Foreign Associations (corporations, partnerships and limited liability "
            "companies) | Department of State | Commonwealth of Pennsylvania",
            "https://www.pa.gov/agencies/dos/programs/business/types-of-filings-and-registrations/foreign-associations",
        ),
        source(
            "Frequently Asked Questions | Department of State | Commonwealth of Pennsylvania",
            "https://www.pa.gov/agencies/dos/resources/business-resources/frequently-asked-questions",
        ),
    ),
    version="2026-10-11-batch7",
    notes=(
        "Foreign LLC and for-profit corporate registration statements cost $250. "
        "Ordinary for-profit annual reports cost $7, beginning in 2025; reports start "
        "the calendar year following initial registration. LLC deadline is September "
        "30 and corporate deadline is June 30. Administrative termination for missing "
        "reports begins with reports due in 2027, six months after their deadline; "
        "terminated foreign registrations must reregister rather than retroactively "
        "reinstate.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
