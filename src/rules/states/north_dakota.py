"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

from decimal import Decimal

from ...models import (
    Activity,
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
    qualification_citation="NDCC §§ 10-32.1-74, 10-32.1-75",
    threshold=QualificationThreshold(
        citation="NDCC § 10-32.1-82",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Income-producing real or tangible personal property constitutes business "
            "except the specified excluded holdings. Interstate commerce and solicitation "
            "are not enumerated here and require separate review. Isolated transactions "
            "must finish within 30 days and not be repeated like transactions. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("135"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LLC",
            "https://firststop.sos.nd.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NDCC § 10-32.1-84",
        "Company civil penalty up to $5,000; participating governors, members or "
        "agents can separately face up to $1,000. Court access is restricted; "
        "injunctions, interest and costs require manual assessment.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "November 15, beginning the calendar year after the certificate of authority "
                "is issued."
            ),
            fee=Decimal("50"),
            citation="NDCC §§ 10-32.1-89, 10-32.1-92",
            notes="Ordinary LLC schedule; farming/ranching and authorized livestock rules differ.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of status from its filing office is required "
        "under § 10-32.1-75; the reviewed provision does not prescribe a numeric "
        "freshness limit."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="NDCC §§ 10-19.1-134, 10-19.1-135",
    threshold=QualificationThreshold(
        citation="NDCC § 10-19.1-143",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Income-producing real or tangible personal property constitutes business "
            "except statutory exclusions. Solicitation requires out-of-state acceptance; "
            "interstate commerce is not enumerated in § 10-19.1-143 and requires review. "
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
        exempt_activities=frozenset(
            {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.SOLICITATION}
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("145"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign corporation",
            "https://firststop.sos.nd.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NDCC § 10-19.1-142",
        "Corporate civil penalty up to $5,000 plus unpaid fees and penalties; "
        "participating directors, officers or agents can separately face up to "
        "$1,000. Injunctions, interest and costs require manual assessment.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="May 15, beginning the calendar year after authority is issued.",
            fee=Decimal("25"),
            citation="NDCC §§ 10-19.1-146, 10-19.1-147",
            notes="August 1 applies to domestic corporations, not ordinary foreign corporations.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated home-jurisdiction certificate of good standing or existence "
        "under § 10-19.1-135; no numeric freshness limit is prescribed in that "
        "provision."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="North Dakota SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="North Dakota SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("110"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.sos.nd.gov/business/business-services/business-structures/partnership",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "North Dakota SOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="ND",
    name="North Dakota",
    registered_agent=RegisteredAgentRequirement(
        citation="NDCC §§ 10-32.1-78, 10-19.1-138; Chapter 10-01.1",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source("North Dakota Century Code t10c32.1", "https://ndlegis.gov/cencode/t10c32-1.pdf"),
        source("North Dakota Century Code t10c19.1", "https://ndlegis.gov/cencode/t10c19-1.pdf"),
        source(
            "Limited Liability Company (LLC) | Secretary of State | North Dakota",
            "https://www.sos.nd.gov/business/business-services/business-structures/limited-liability-company-llc",
        ),
        source(
            "Corporation | Secretary of State | North Dakota",
            "https://www.sos.nd.gov/business/business-services/business-structures/corporation",
        ),
        source(
            "Maintain Registration | Secretary of State | North Dakota",
            "https://www.sos.nd.gov/business/business-services/maintain-registration",
        ),
        source("North Dakota Century Code t10c01.1", "https://ndlegis.gov/cencode/t10c01-1.pdf"),
        source(
            "Partnership | Secretary of State | North Dakota",
            "https://www.sos.nd.gov/business/business-services/business-structures/partnership",
        ),
    ),
    version="2026-10-11-batch7",
    notes=(
        "Ordinary foreign LLC registration costs $135; foreign corporate authority "
        "costs $145. Annual reports cost $50 for LLCs and $25 for corporations. "
        "Foreign corporate reports are due May 15, not the August 1 domestic "
        "deadline. Farming, ranching and authorized livestock entities have "
        "additional restrictions and different report deadlines requiring separate "
        "review.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
