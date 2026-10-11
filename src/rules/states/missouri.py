"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

from decimal import Decimal

from ...models import (
    Activity,
    EntityRequirement,
    EntityType,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)
from ._shared import annual, source, unresolved_penalty

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="RSMo § 347.153",
    threshold=QualificationThreshold(
        citation="RSMo § 347.163(5)",
        isolated_transaction_max_days=30,
        notes=(
            "Orders accepted outside Missouri are not an enumerated exemption in § "
            "347.163(5); review them individually. LLC annual reporting was not "
            "established by the reviewed corporate report provisions; confirm "
            "entity-specific obligations. Isolated transactions must finish within 30 "
            "days and not be repeated like transactions. Qualification exemptions do not "
            "determine tax, licensing, or service-of-process nexus."
        ),
        exempt_activities=frozenset(
            {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.INTERSTATE_COMMERCE}
        ),
    ),
    filing_fee=Decimal("105"),
    forms=(
        StateForm(
            "Application for registration",
            "LLC-4",
            "https://www.sos.mo.gov/CMSImages/Business/llc4.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "RSMo § 347.163(1)",
        "Fine of not less than $1,000, recovered by the prosecuting attorney. This "
        "provision gives no numeric maximum; do not model the minimum as an exact "
        "total.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing/existence certificate dated within 60 "
        "calendar days of filing, under § 347.153(1)(8) and LLC-4."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="RSMo §§ 351.572, 351.576",
    threshold=QualificationThreshold(
        citation="RSMo § 351.572(2)",
        isolated_transaction_max_days=30,
        notes=(
            "Orders accepted outside Missouri are not an enumerated exemption in § "
            "351.572(2); review them individually. Isolated transactions must finish "
            "within 30 days and not be repeated like transactions. Qualification "
            "exemptions do not determine tax, licensing, or service-of-process nexus."
        ),
        exempt_activities=frozenset(
            {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.INTERSTATE_COMMERCE}
        ),
    ),
    filing_fee=Decimal("155"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Corp-42",
            "https://www.sos.mo.gov/CMSImages/Business/corp42.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "RSMo § 351.574(4)",
        "Fine of not less than $1,000, recovered by the prosecuting attorney. This "
        "provision gives no numeric maximum; do not model the minimum as an exact "
        "total.",
    ),
    annual_obligations=(
        annual(
            "Corporate registration report",
            "Annually in the qualification month (or validly changed filing month), by month end.",
            "20",
            "RSMo §§ 351.120, 351.122; SOS fee schedule",
            "$45 paper. Eligible corporations may elect biennial filing in years matching "
            "formation/qualification parity: $40 online or $90 paper, replacing the "
            "annual cycle. Late reports add $15 per 30-day period per SOS guidance.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Current original home-jurisdiction certificate of good standing/existence "
        "not more than 60 days old, per Corp-42."
    ),
    initial_report=(
        "File the initial corporate registration report within 30 days of "
        "qualification under RSMo § 351.120(3)."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Missouri SOS foreign LP schedule; RSMo Chapter 359",
    threshold=QualificationThreshold(
        citation="RSMo Chapter 359",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset(),
    ),
    filing_fee=Decimal("105"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.sos.mo.gov/CMSImages/Business/fees.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "RSMo Chapter 359", "LP sanctions require separate review."
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence="Review LP evidence requirements independently.",
)

REQUIREMENT = StateRequirement(
    state="MO",
    name="Missouri",
    registered_agent=RegisteredAgentRequirement(
        citation="RSMo §§ 347.153(1)(4), 351.576(1)(5)",
        notes=(
            "Maintain a consenting eligible agent and an actual in-state registered "
            "office for LLC/corporate filings; a PO box alone is insufficient. LP "
            "exceptions require separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 347.163",
            "https://revisor.mo.gov/main/OneSection.aspx?section=347.163",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 347.153",
            "https://revisor.mo.gov/main/OneSection.aspx?section=347.153",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 351.572",
            "https://revisor.mo.gov/main/OneSection.aspx?section=351.572",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 351.574",
            "https://revisor.mo.gov/main/OneSection.aspx?section=351.574",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 351.120",
            "https://revisor.mo.gov/main/OneSection.aspx?section=351.120",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 351.122",
            "https://revisor.mo.gov/main/OneSection.aspx?section=351.122",
        ),
        source(
            "Missouri Revisor of Statutes - Revised Statutes of Missouri,  RSMo Section 351.576",
            "https://revisor.mo.gov/main/OneSection.aspx?section=351.576",
        ),
        source(
            "Schedule of Fees and Charges", "https://www.sos.mo.gov/CMSImages/Business/fees.pdf"
        ),
        source(
            "General Services & Filings - Missouri Secretary of State",
            "https://www.sos.mo.gov/business/corporations/generalinfo",
        ),
        source(
            "LLC 4 - Application for Registration of a Foreign Limited Liability Company",
            "https://www.sos.mo.gov/CMSImages/Business/llc4.pdf",
        ),
        source(
            "Corp 42 - Application for Certificate of Authority for a Foreign For-Profit "
            "Corporation",
            "https://www.sos.mo.gov/CMSImages/Business/corp42.pdf",
        ),
    ),
    version="2026-10-11-batch5",
    notes=(
        "SOS charges include the $5 technology surcharge: LLC authority $105 and "
        "corporate authority $155. Corporate reports cost $20 online or $45 paper "
        "annually; an eligible biennial election costs $40 online or $90 paper "
        "instead of annual reporting.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "The SOS schedule is dated June 30, 2015 and remains published. January 2025 "
        "LLC-4 and the current corporate application corroborate filing fees. "
        "Corporate annual/biennial prices are documented with the statutory surcharge "
        "and current SOS filing guidance.",
    ),
)
