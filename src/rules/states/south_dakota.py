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
    qualification_citation="SDCL § 47-34A-1002",
    threshold=QualificationThreshold(
        citation="SDCL § 47-34A-1003",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Income-producing real or tangible personal "
            "property is business except statutory excluded holdings. The $750 fee is for "
            "ordinary LLCs online, not foreign series authority."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("750"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LLC",
            "https://sdsos.gov/docs/business/foreignllccertificateofauthority20180215.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "SDCL §§ 47-34A-1008, 47-34A-1009",
        "Cannot maintain proceedings until authorized; contracts, defenses and "
        "member/manager liability protections remain valid. Secretary of State is "
        "service agent for unregistered activity; Attorney General may restrain "
        "unauthorized business. These provisions supply no fixed daily qualification "
        "fine.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Under current SDCL § 59-11-25, before February 1 (January 31), beginning the "
                "calendar year after authorization. Confirm the entity’s assigned filing date "
                "with SOS."
            ),
            fee=Decimal("55"),
            citation="SDCL §§ 47-34A-211, 47-34A-212, 59-11-24, 59-11-25",
            notes=(
                "Online $55; paper $70 including $15 paper fee; delinquent reports add $55. "
                "Effective January 1, 2027, § 59-11-25 permits election of the "
                "formation-anniversary month or January 31 of the following year; follow the "
                "recorded election and any change-of-filing-date form. Agricultural-land "
                "disclosures and restricted ownership need separate review. The older SOS "
                "portal instruction still says $50 for late reports; current statutes, the "
                "fee schedule and July 2025 forms all specify $55, which governs this guide."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Original one-page home-jurisdiction certificate of existence or similar "
        "authenticated record is required by § 47-34A-1002(c) and the SOS form; the "
        "reviewed materials prescribe no numeric freshness limit."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="SDCL §§ 47-1A-1501, 47-1A-1503",
    threshold=QualificationThreshold(
        citation="SDCL § 47-1A-1501",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Mere property ownership is exempt; LLC "
            "income-producing-property wording is not copied to corporations."
        ),
    ),
    filing_fee=Decimal("750"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign business corporation",
            "https://sdsos.gov/docs/business/corporation-foreign-certificateofauthority.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "SDCL §§ 47-1A-1502, 47-1A-1502.2",
        "Civil penalty $100 for each day of unauthorized business, capped at $1,000 "
        "per year. Court access is restricted until authorized; contracts and "
        "defenses remain valid. Days, year boundaries and other sanctions require "
        "manual review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Under current SDCL § 59-11-25, before February 1 (January 31), beginning the "
                "calendar year after authorization. Confirm the entity’s assigned filing date "
                "with SOS."
            ),
            fee=Decimal("55"),
            citation="SDCL §§ 47-1A-122, 59-11-24, 59-11-25",
            notes=(
                "Online $55; paper $70 including $15 paper fee; delinquent reports add $55. "
                "Effective January 1, 2027, § 59-11-25 permits election of the "
                "formation-anniversary month or January 31 of the following year; follow the "
                "recorded election and any change-of-filing-date form. Agricultural-land "
                "disclosures and restricted ownership need separate review. The older SOS "
                "portal instruction still says $50 for late reports; current statutes, the "
                "fee schedule and July 2025 forms all specify $55, which governs this guide."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Original one-page home-jurisdiction certificate of existence or similar "
        "authenticated record under § 47-1A-1503 and the SOS form; no numeric "
        "freshness limit is supplied."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="South Dakota SOS foreign LP registration fee",
    threshold=QualificationThreshold(
        citation="South Dakota SOS foreign LP registration fee",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("125"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://sdsos.gov/general-information/filing-fees.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "South Dakota SOS foreign LP registration fee", "LP sanctions require separate review."
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
    state="SD",
    name="South Dakota",
    registered_agent=RegisteredAgentRequirement(
        citation="SDCL §§ 59-11-6, 59-11-7",
        notes=(
            "Appoint a consenting commercial or noncommercial registered agent; § 59-11-6 "
            "also permits an officeholder designation. Paper authority forms request an "
            "actual South Dakota street/business office address; PO box alone is "
            "insufficient. No separate outside vendor is required. LP exceptions require "
            "independent review."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Codified Law 47-34A | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-34A",
        ),
        source(
            "Codified Law 47-1A-1501 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-1A-1501",
        ),
        source(
            "Codified Law 47-1A-1503 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-1A-1503",
        ),
        source(
            "Codified Law 47-1A-1502 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-1A-1502",
        ),
        source(
            "Codified Law 47-1A-1502.2 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-1A-1502.2",
        ),
        source(
            "Codified Law 47-1A-122 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/47-1A-122",
        ),
        source(
            "Codified Law 59-11-6 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/59-11-6",
        ),
        source(
            "Codified Law 59-11-7 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/59-11-7",
        ),
        source(
            "Codified Law 59-11-24 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/59-11-24",
        ),
        source(
            "Codified Law 59-11-25 | South Dakota Legislature",
            "https://sdlegislature.gov/Statutes/59-11-25",
        ),
        source(
            "General Information: South Dakota Secretary of State",
            "https://sdsos.gov/general-information/filing-fees.aspx",
        ),
        source(
            "Corporations: South Dakota Secretary of State",
            "https://sdsos.gov/business-services/corporations/corporate-forms/limited-liability-companies.aspx",
        ),
        source(
            "Corporations: South Dakota Secretary of State",
            "https://sdsos.gov/business-services/corporations/corporate-forms/business-corporations.aspx",
        ),
        source(
            "Foreign LLC - Certificate of Authority",
            "https://sdsos.gov/docs/business/foreignllccertificateofauthority20180215.pdf",
        ),
        source(
            "Foreign Business Corp - Certificate of Authority",
            "https://sdsos.gov/docs/business/corporation-foreign-certificateofauthority.pdf",
        ),
        source("RETURN TO", "https://sdsos.gov/docs/business/foreignllcannualreport20250701.pdf"),
        source("RETURN TO", "https://sdsos.gov/docs/business/corpforeignannualreport20250701.pdf"),
        source(
            "South Dakota Secretary of State Monae L. Johnson - Business",
            "https://sosenterprise.sd.gov/BusinessServices/Business/AnnualReportInstr.aspx",
        ),
    ),
    version="2026-10-11-batch8",
    notes=(
        "Ordinary foreign LLC and corporate authority each cost $750 online or $765 "
        "on paper. Annual reports cost $55 online or $70 on paper; delinquent reports "
        "add $55. Foreign series LLC authority is $800 before applicable paper "
        "charges and is outside the ordinary-LLC fee shown. Agricultural land, "
        "farming and foreign beneficial ownership have additional rules. The current "
        "statute and its January 1, 2027 deadline amendment are distinguished in the "
        "annual-report notes.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "SDCL § 59-11-25 currently requires the first report before February 1 in the "
        "calendar year after authorization and the same date thereafter. Text marked "
        "effective January 1, 2027 permits the formation-anniversary-month or January "
        "31 election; it is disclosed as future law, not substituted for current law. "
        "Confirm the entity’s assigned filing date with SOS.",
    ),
)
