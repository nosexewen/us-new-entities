"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

from decimal import Decimal

from ...models import (
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
    qualification_citation="MCA § 35-8-1001",
    threshold=QualificationThreshold(
        citation="MCA § 35-8-1001(2)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("70"),
    forms=(
        StateForm(
            "Application for certificate of authority", "Foreign LLC", "https://biz.sosmt.gov/"
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "MCA § 35-8-1002(4)",
        "$5 for each day of unauthorized business, capped at $1,000 for each year. "
        "Covered days and yearly cap allocation require manual assessment; public "
        "contracts may be voidable.",
    ),
    annual_obligations=(
        annual(
            "Annual report",
            "January 1 through April 15, beginning the calendar year after authorization.",
            "0",
            "MCA § 35-8-208; Montana SOS fee schedule",
            "Current timely-filing fee is waived; after April 15 the schedule charges "
            "$35. Confirm the waiver for the filing year.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application states compliance with home-jurisdiction organizational laws and "
        "existence there; § 35-8-1003 does not require a certificate attachment or "
        "numeric freshness limit. Series require operating-agreement copies."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="MCA §§ 35-14-1502, 35-14-1503",
    threshold=QualificationThreshold(
        citation="MCA § 35-14-1505",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("70"),
    forms=(
        StateForm(
            "Foreign registration statement",
            "Foreign for-profit corporation",
            "https://biz.sosmt.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "MCA § 35-14-1502",
        "Proceedings cannot be maintained until registration; state/public contracts "
        "can be voidable. This section does not specify a daily monetary penalty; do "
        "not import the LLC $5-per-day penalty or repealed corporate law.",
    ),
    annual_obligations=(
        annual(
            "Annual report",
            "January 1 through April 15, beginning the calendar year after registration.",
            "0",
            "MCA § 35-14-1621; Montana SOS fee schedule",
            "Current timely-filing fee is waived; after April 15 the schedule charges "
            "$35. Confirm the waiver for the filing year.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Registration states compliance with home-jurisdiction organizational laws "
        "and existence there; § 35-14-1503 does not require a certificate attachment "
        "or numeric freshness limit."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Montana SOS foreign LP fee schedule; MCA Chapter 35-12",
    threshold=QualificationThreshold(
        citation="MCA Chapter 35-12",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset(),
    ),
    filing_fee=Decimal("10"),
    forms=(StateForm("Certificate of authority", "Foreign LP", "https://biz.sosmt.gov/"),),
    qualification_penalty=unresolved_penalty(
        "MCA Chapter 35-12", "LP sanctions require separate review."
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
    state="MT",
    name="Montana",
    registered_agent=RegisteredAgentRequirement(
        citation="MCA §§ 35-7-102, 35-7-105; 35-14-1503(4)",
        notes=(
            "Maintain a consenting eligible agent and an actual in-state registered "
            "office for LLC/corporate filings; a PO box alone is insufficient. LP "
            "exceptions require separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "MCA § 35-8-1001 LLC authority and exemptions",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0080/part_0100/section_0010/0350-0080-0100-0010.html",
        ),
        source(
            "MCA § 35-8-1002 LLC sanctions",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0080/part_0100/section_0020/0350-0080-0100-0020.html",
        ),
        source(
            "MCA § 35-8-1003 LLC application",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0080/part_0100/section_0030/0350-0080-0100-0030.html",
        ),
        source(
            "MCA § 35-8-208 LLC annual report",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0080/part_0020/section_0080/0350-0080-0020-0080.html",
        ),
        source(
            "MCA § 35-14-1502 corporate registration and consequences",
            "https://mca.legmt.gov/bills/mca/title_0350/chapter_0140/part_0150/section_0020/0350-0140-0150-0020.html",
        ),
        source(
            "MCA § 35-14-1503 corporate registration statement",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0140/part_0150/section_0030/0350-0140-0150-0030.html",
        ),
        source(
            "MCA § 35-14-1505 corporate exemptions",
            "https://mca.legmt.gov/bills/mca/title_0350/chapter_0140/part_0150/section_0050/0350-0140-0150-0050.html",
        ),
        source(
            "MCA § 35-14-1621 corporate annual report",
            "https://leg.mt.gov/bills/mca/title_0350/chapter_0140/part_0160/section_0210/0350-0140-0160-0210.html",
        ),
        source(
            "Business Services Filing Fees - Official Montana Secretary of State Website "
            "- Christi Jacobsen",
            "https://sosmt.gov/business/fees",
        ),
        source(
            "MCA § 35-7-105 agent appointment and consent",
            "https://mca.legmt.gov/bills/mca/title_0350/chapter_0070/part_0010/section_0050/0350-0070-0010-0050.html",
        ),
        source(
            "MCA § 35-7-102 registered agent definitions",
            "https://mca.legmt.gov/bills/mca/title_0350/chapter_0070/part_0010/section_0020/0350-0070-0010-0020.html",
        ),
    ),
    version="2026-10-11-batch5",
    notes=(
        "LLC authority and for-profit foreign corporate registration each cost $70. "
        "LLCs add $50 for each named series. The current SOS schedule waives timely "
        "LLC/corporate annual-report fees and charges $35 after April 15; confirm the "
        "waiver for the filing year. State/public contracts have additional "
        "qualification rules and can be voidable if registration is missing.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "The current corporate law uses foreign registration statements under Chapter "
        "35-14; do not apply repealed Chapter 35-1 authority penalties to "
        "corporations.",
    ),
)
