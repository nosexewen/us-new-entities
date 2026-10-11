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
    qualification_citation="N.J.S.A. 42:2C-58",
    threshold=QualificationThreshold(
        citation="N.J.S.A. 42:2C-59",
        isolated_transaction_max_days=30,
        notes=(
            "Income-producing real or tangible personal property constitutes business "
            "except the specified security-interest holdings. Isolated transactions must "
            "finish within 30 days and not be repeated like transactions. Qualification "
            "exemptions do not determine tax, licensing, or service-of-process nexus."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Certificate of authority",
            "Foreign LLC",
            "https://www.njportal.com/DOR/BusinessFormation/Home/Welcome",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "N.J.S.A. 42:2C-65",
        "Cannot maintain proceedings until authorized; contracts and defenses remain "
        "valid. This section supplies no fixed monetary qualification fine; do not "
        "import corporate sanctions.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month shown in the New Jersey registry; agency "
                "guidance describes the business formation month. Confirm the assigned month "
                "for a foreign registration."
            ),
            fee=Decimal("75"),
            citation="N.J.S.A. 42:2C-26; NJ annual filing guidance",
            notes="",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Section 42:2C-58 requires application details and an initial agent but does "
        "not prescribe a home-jurisdiction certificate attachment or numeric "
        "freshness limit."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="N.J.S.A. 14A:13-3, 14A:13-4",
    threshold=QualificationThreshold(
        citation="N.J.S.A. 14A:13-3(2)",
        isolated_transaction_max_days=None,
        notes=(
            "The corporate statute lists narrower exemptions than the LLC statute. It "
            "does not enumerate a 30-day isolated-transaction, ordinary solicitation or "
            "interstate-commerce exemption; those activities require review. Tax and "
            "CBA-1 Notice of Business Activities obligations require separate analysis."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Certificate of authority",
            "Foreign for-profit corporation",
            "https://www.njportal.com/DOR/BusinessFormation/Home/Welcome",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "N.J.S.A. 14A:13-11",
        "$200–$1,000 for each calendar year of unauthorized business within a "
        "five-year lookback, plus costs. The applicable amount requires manual "
        "assessment.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month shown in the New Jersey registry; confirm "
                "the assigned month for a foreign registration."
            ),
            fee=Decimal("75"),
            citation="NJ annual filing guidance",
            notes="",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing certificate dated no earlier than 30 days "
        "before filing; foreign-language certificates require a translation under § "
        "14A:13-4."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="New Jersey Revenue foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="New Jersey Revenue foreign LP fee schedule",
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
            "https://www.nj.gov/treasury/revenue/fees.shtml",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "New Jersey Revenue foreign LP fee schedule", "LP sanctions require separate review."
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
    state="NJ",
    name="New Jersey",
    registered_agent=RegisteredAgentRequirement(
        citation="N.J.S.A. 42:2C-58; 14A:13-4; NJ registration instructions",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "State of NJ - NJ Treasury - DORES", "https://www.nj.gov/treasury/revenue/fees.shtml"
        ),
        source(
            "State of NJ - Department of the Treasury - Division of Revenue Getting Registered",
            "https://www.nj.gov/treasury/revenue/gettingregistered.shtml",
        ),
        source(
            "Taxes and Annual Report | Business.NJ.gov",
            "https://business.nj.gov/pages/filings-and-accounting/",
        ),
        source(
            "New Jersey Revised Statutes Section 42:2C-58 (2025) - Application for "
            "certificate of authority; amendments to certificate of authority. :: 2025 "
            "New Jersey Revised Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-42/section-42-2c-58/",
        ),
        source(
            "New Jersey Revised Statutes Section 42:2C-59 (2025) - Activities not "
            "constituting transacting business. :: 2025 New Jersey Revised Statutes :: "
            "U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-42/section-42-2c-59",
        ),
        source(
            "New Jersey Revised Statutes Section 42:2C-65 (2025) - Effect of failure to "
            "have certificate of authority. :: 2025 New Jersey Revised Statutes :: U.S. "
            "Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-42/section-42-2c-65",
        ),
        source(
            "New Jersey Revised Statutes Section 42:2C-26 (2025) - Annual report for "
            "filing office. :: 2025 New Jersey Revised Statutes :: U.S. Codes and "
            "Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-42/section-42-2c-26",
        ),
        source(
            "New Jersey Revised Statutes Section 14A:13-3 (2025) - Admission of foreign "
            "corporation :: 2025 New Jersey Revised Statutes :: U.S. Codes and Statutes "
            ":: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-14a/section-14a-13-3/",
        ),
        source(
            "New Jersey Revised Statutes Section 14A:13-11 (2025) - Transacting business "
            "without certificate of authority :: 2025 New Jersey Revised Statutes :: U.S. "
            "Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-14a/section-14a-13-11",
        ),
        source(
            "New Jersey Revised Statutes Section 14A:13-4 (2025) - Application for "
            "certificate of authority :: 2025 New Jersey Revised Statutes :: U.S. Codes "
            "and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-jersey/title-14a/section-14a-13-4",
        ),
        source(
            "Legacy Business Registration Form and Information",
            "https://www.nj.gov/treasury/revenue/pdf/Legacy-Reg-Form-0825.pdf",
        ),
        source(
            "Notice of Business Activities Report by a Foreign Corporation, Form CBA-1",
            "https://www.nj.gov/treasury/taxation/pdf/current/cbt/cba1.pdf",
        ),
    ),
    version="2026-10-11-batch6",
    notes=(
        "The current Revenue fee schedule and registration page state $100 for "
        "foreign LLC/corporate qualification (registration page updated July 1, "
        "2026). Older $125 registration instructions do not control the current fee. "
        "Annual reports cost $75. Complete NJ-REG tax/employer registration "
        "separately after business registration; qualification does not settle tax "
        "nexus.",
    ),
    verification_issues=(),
    review_disclosures=(
        "At the user's direction on 2026-10-11, the cited Justia statutory "
        "reproductions are accepted as sufficient verification for New Jersey. "
        "The primary review flag is satisfied by that acceptance; Justia remains "
        "a secondary publisher. Legislative gateway navigation and a bill reprint "
        "were not accepted as enacted current statutory text.",
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
