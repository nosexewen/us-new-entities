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
    qualification_citation="S.C. Code §§ 33-44-1002, 33-44-1004",
    threshold=QualificationThreshold(
        citation="S.C. Code § 33-44-1003",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Ownership of income-producing real or tangible "
            "personal property triggers qualification except specified excluded holdings. "
            "No routine SOS annual report; tax-classification-specific DOR obligations "
            "require review."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("110"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LLC",
            "https://businessfilings.sc.gov/BusinessFiling",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "S.C. Code §§ 33-44-1008, 33-44-1009",
        "Cannot maintain proceedings until authorized; contracts, defenses and "
        "limited liability remain valid. Secretary of State is service agent for "
        "unregistered business; Attorney General may seek an injunction. These "
        "sections supply no fixed daily qualification fine.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated home-jurisdiction certificate of existence or similar record "
        "under § 33-44-1002(b), dated no more than 30 days before filing per SOS "
        "rejection guidance."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="S.C. Code §§ 33-15-101, 33-15-103",
    threshold=QualificationThreshold(
        citation="S.C. Code § 33-15-101(b)",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Owning property without more is exempt; LLC "
            "income-producing-property language is not copied to corporations."
        ),
    ),
    filing_fee=Decimal("135"),
    forms=(
        StateForm(
            "Application for certificate of authority with initial annual report",
            "Foreign corporation / CL-1",
            "https://businessfilings.sc.gov/BusinessFiling",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "S.C. Code § 33-15-102",
        "Civil penalty $10 for each day of unauthorized business, capped at $1,000 "
        "per year. Court access is restricted until authorized; contracts and "
        "defenses remain valid. Applicable days and years require manual calculation.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="DOR annual report and corporate license fee",
            cycle="annual",
            due_rule=(
                "15th day of the fourth month after taxable-year end (April 15 for a "
                "calendar-year C corporation), unless a statutory exception applies."
            ),
            fee=None,
            citation="S.C. Code §§ 33-16-220, 12-20-20, 12-20-50",
            notes=(
                "Ordinary license fee is $15 plus $1 per $1,000 or fraction of capital stock "
                "and paid-in/capital surplus, minimum $25, with applicable apportionment and "
                "special-industry rules. DOR report accompanies the corporate tax filing; "
                "extensions do not extend license-fee payment."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated home-jurisdiction certificate of existence under § "
        "33-15-103(b), dated no more than 30 days before filing per SOS guidance."
    ),
    initial_report=(
        "File initial annual report CL-1 and the $25 minimum license fee with the "
        "authority application under § 12-20-40. The disclosed $135 registration "
        "total includes this ordinary initial minimum."
    ),
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="S.C. Code §§ 33-42-1620, 33-42-2040",
    threshold=QualificationThreshold(
        citation="S.C. Code §§ 33-42-1620, 33-42-2040",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("10"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.scstatehouse.gov/code/t33c042.php",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "S.C. Code §§ 33-42-1620, 33-42-2040", "LP sanctions require separate review."
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
    state="SC",
    name="South Carolina",
    registered_agent=RegisteredAgentRequirement(
        citation="S.C. Code §§ 33-44-108, 33-15-107",
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
            "Code of Laws - Title 33 - Chapter 44- - CORPORATIONS, PARTNERSHIPS AND ASSOCIATIONS",
            "https://www.scstatehouse.gov/code/t33c044.php",
        ),
        source(
            "Code of Laws - Title 33 - Chapter 15- - CORPORATIONS, PARTNERSHIPS AND ASSOCIATIONS",
            "https://www.scstatehouse.gov/code/t33c015.php",
        ),
        source(
            "Code of Laws - Title 33 - Chapter 1- - CORPORATIONS, PARTNERSHIPS AND ASSOCIATIONS",
            "https://www.scstatehouse.gov/code/t33c001.php",
        ),
        source(
            "Code of Laws - Title 33 - Chapter 16- - CORPORATIONS, PARTNERSHIPS AND ASSOCIATIONS",
            "https://www.scstatehouse.gov/code/t33c016.php",
        ),
        source(
            "Code of Laws - Title 12 - Chapter 20- - TAXATION",
            "https://www.scstatehouse.gov/code/t12c020.php",
        ),
        source(
            "FAQs About Business Entities | SC Secretary of State",
            "https://sos.sc.gov/faqs-about-business-entities",
        ),
        source(
            "Code of Laws - Title 33 - Chapter 42- - CORPORATIONS, PARTNERSHIPS AND ASSOCIATIONS",
            "https://www.scstatehouse.gov/code/t33c042.php",
        ),
    ),
    version="2026-10-11-batch8",
    notes=(
        "Foreign LLC authority is $110. Foreign corporate authority ordinarily totals "
        "$135: $10 filing, $100 statutory charge and $25 initial minimum license fee. "
        "Corporate initial report CL-1 accompanies the authority application. "
        "Corporations file annual reports with the Department of Revenue, not an "
        "ordinary SOS annual renewal. Ordinary LLCs have no routine SOS annual report "
        "under Chapter 44; taxation and licensing remain separate and LLCs taxed as "
        "corporations may have DOR filing duties.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
