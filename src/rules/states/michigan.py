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
    qualification_citation="MCL 450.5002",
    threshold=QualificationThreshold(
        citation="MCL 450.5008",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("50"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "CSCL/CD-760",
            "https://www.michigan.gov/lara/-/media/Project/Websites/lara/cscl/NonImages_new/Corps/forms/llc/760-0725.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "MCL 450.5007(5)-(7)",
        "$100–$1,000 for each calendar month of unauthorized business within a "
        "five-year lookback, with a $10,000 company cap; managers, members or "
        "authorized persons can separately face up to $10,000. Recoverable fees, "
        "interest and court costs require manual assessment.",
    ),
    annual_obligations=(
        annual(
            "Annual statement",
            "February 15; authorization after September 30 skips the immediately "
            "following February 15.",
            "25",
            "MCL 450.4207(3), 450.5101(1)(g)",
            "$25 through September 30, 2027; the statute specifies $15 afterward.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing certificate dated no earlier than 30 days "
        "before receipt, per form CSCL/CD-760."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="MCL 450.2011",
    threshold=QualificationThreshold(
        citation="MCL 450.2012",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("60"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "CSCL/CD-560",
            "https://www.michigan.gov/lara/-/media/Project/Websites/lara/cscl/NonImages_new/Corps/forms/corporation/560-0725.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "MCL 450.2051, 450.2055",
        "$100–$1,000 for each calendar month of unauthorized business within a "
        "five-year lookback, capped at $10,000; attorney-general recovery includes "
        "costs and other legal liabilities.",
    ),
    annual_obligations=(
        annual(
            "Annual report",
            "May 15; corporations formed or authorized January 1 through May 15 need not "
            "file for that calendar year.",
            "25",
            "MCL 450.1911; 450.2060(1)(u)",
            "$25 before October 1, 2027; the statute specifies $15 afterward.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing certificate dated no earlier than 30 days "
        "before receipt, per form CSCL/CD-560."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="MCL 449.1902, 449.2107",
    threshold=QualificationThreshold(
        citation="MCL 449.1902",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset(),
    ),
    filing_fee=Decimal("10"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.michigan.gov/lara/bureau-list/cscl/corps/limited-part/types/foreign-limited-partnership",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "MCL 449.1907",
        "Court-access restrictions and other sanctions require LP-specific assessment.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Review the LP application requirements separately; do not inherit LLC or "
        "corporate certificate requirements."
    ),
)

REQUIREMENT = StateRequirement(
    state="MI",
    name="Michigan",
    registered_agent=RegisteredAgentRequirement(
        citation="MCL 450.4207; 450.1241",
        notes=(
            "Maintain a consenting eligible agent and an actual in-state registered "
            "office for LLC/corporate filings; a PO box alone is insufficient. LP "
            "exceptions require separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Act 23 of 1993",
            "https://www.legislature.mi.gov/documents/mcl/pdf/mcl-act-23-of-1993.pdf",
        ),
        source(
            "760 CSCL-CD Rev 7-25 Application for Certificate of Authority to Transact "
            "Business in Michigan (FLLC)",
            "https://www.michigan.gov/lara/-/media/Project/Websites/lara/cscl/NonImages_new/Corps/forms/llc/760-0725.pdf",
        ),
        source(
            "MCL - Section 450.2012 - Michigan Legislature",
            "https://legislature.mi.gov/Laws/MCL?objectName=mcl-450-2012",
        ),
        source(
            "MCL - Section 450.2011 - Michigan Legislature",
            "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-450-2011",
        ),
        source(
            "MCL - Section 450.2051 - Michigan Legislature",
            "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-450-2051",
        ),
        source(
            "MCL - Section 450.2055 - Michigan Legislature",
            "https://legislature.mi.gov/Laws/MCL?objectName=mcl-450-2055",
        ),
        source(
            "560 CSCL-CD Rev 7-25 Application for Certificate of Authority to Transact "
            "Business or Conduct Affairs in Michigan (Foreign Corporations)",
            "https://www.michigan.gov/lara/-/media/Project/Websites/lara/cscl/NonImages_new/Corps/forms/corporation/560-0725.pdf",
        ),
        source(
            "MCL - Section 450.1911 - Michigan Legislature",
            "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-450-1911",
        ),
        source(
            "MCL - Section 450.2062 - Michigan Legislature",
            "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-450-2062",
        ),
        source(
            "MCL - Section 450.2060 - Michigan Legislature",
            "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-450-2060",
        ),
        source(
            "MCL - Section 450.1241 - Michigan Legislature",
            "https://legislature.mi.gov/Laws/MCL?objectName=mcl-450-1241",
        ),
        source(
            "Act 213 of 1982",
            "https://legislature.mi.gov/documents/mcl/pdf/MCL-ACT-213-OF-1982.pdf",
        ),
        source(
            "Foreign Limited Partnership",
            "https://www.michigan.gov/lara/bureau-list/cscl/corps/limited-part/types/foreign-limited-partnership",
        ),
    ),
    version="2026-10-11-batch5",
    notes=(
        "Initial corporate admission is $60: $10 filing plus $50 initial admission "
        "fee. Later increases in shares attributable to Michigan can require "
        "additional fees under MCL 450.2062. LLC filing is $50. Optional expedited "
        "services are separate.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations. Michigan LPs may "
        "elect a private agent under MCL 449.1902; the shared agent summary describes "
        "LLCs and corporations.",
    ),
)
