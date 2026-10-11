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
    qualification_citation="NRS § 86.544",
    threshold=QualificationThreshold(
        citation="NRS § 86.5483",
        isolated_transaction_max_days=30,
        notes=(
            "Solicitation exemption requires solicitation and receipt outside Nevada, "
            "out-of-state acceptance and shipment of goods into Nevada; ordinary "
            "solicitation with only out-of-state acceptance requires review. Isolated "
            "transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
        exempt_activities=frozenset(
            {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.INTERSTATE_COMMERCE}
        ),
    ),
    filing_fee=Decimal("75"),
    forms=(StateForm("Foreign LLC registration", "Foreign LLC", "https://www.nvsilverflume.gov/"),),
    qualification_penalty=unresolved_penalty(
        "NRS § 86.548",
        "Willful unauthorized business carries a fine of $1,000–$10,000. The 45-day "
        "cure provision concerns extraordinary remedies in litigation and is not a "
        "general qualification grace period.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual list",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month of registration, unless a valid "
                "alternative filing date applies."
            ),
            fee=Decimal("150"),
            citation="NRS § 86.5461",
            notes="",
        ),
        AnnualObligation(
            name="State business license renewal",
            cycle="annual",
            due_rule="With the annual list, unless a statutory exemption applies.",
            fee=Decimal("200"),
            citation="NRS §§ 76.100, 76.130",
            notes=(
                "Review Chapter 76 exemptions; late license renewal can add $100 per year "
                "under § 76.110."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application declares existence and good standing in the home jurisdiction; § "
        "86.544 does not prescribe a certificate attachment or numeric freshness "
        "limit."
    ),
    initial_report=(
        "File the $150 initial list at registration and obtain the $200 state "
        "business license unless exempt; review any valid alternative filing date "
        "under NRS § 86.5461."
    ),
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="NRS § 80.010",
    threshold=QualificationThreshold(
        citation="NRS § 80.015",
        isolated_transaction_max_days=30,
        notes=(
            "The solicitation exemption has outside-Nevada solicitation, receipt, "
            "acceptance and goods-shipment conditions; ordinary solicitation requires "
            "review. Isolated transactions must finish within 30 days and not be repeated "
            "like transactions. Qualification exemptions do not determine tax, licensing, "
            "or service-of-process nexus."
        ),
        exempt_activities=frozenset(
            {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.INTERSTATE_COMMERCE}
        ),
    ),
    filing_fee=Decimal("75"),
    forms=(
        StateForm(
            "Foreign corporation qualification",
            "Foreign corporation",
            "https://www.nvsilverflume.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NRS § 80.055",
        "Willful unauthorized business carries a fine of $1,000–$10,000. The 45-day "
        "extraordinary-remedy cure exception is limited to the statutory litigation "
        "setting.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual list",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month of qualification, unless a valid "
                "alternative filing date applies."
            ),
            fee=Decimal("150"),
            citation="NRS § 80.110",
            notes=(
                "$150 is the minimum; authorized stock can increase the annual list fee, "
                "capped at $11,125."
            ),
        ),
        AnnualObligation(
            name="State business license renewal",
            cycle="annual",
            due_rule="With the annual list, unless a statutory exemption applies.",
            fee=Decimal("500"),
            citation="NRS §§ 76.100, 76.130",
            notes="Late license renewal can add $100 per year under § 76.110.",
        ),
        AnnualObligation(
            name="Annual statement publication",
            cycle="annual",
            due_rule=(
                "By the end of March for calendar-year records, or the end of the third month "
                "after a different fiscal year closes."
            ),
            fee=None,
            citation="NRS § 80.190",
            notes=(
                "Publish in two issues of a Nevada newspaper with at least 1,000 weekly "
                "circulation. Publication charges vary; failure adds a $100 penalty for each "
                "month unpublished."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Declare home-jurisdiction existence and good standing and file the "
        "authorized-stock record required by § 80.010; no numeric certificate "
        "freshness limit is prescribed there."
    ),
    initial_report=(
        "File the $150 initial list at qualification and obtain the $500 state "
        "business license unless exempt. The $75 qualification amount is a minimum "
        "under NRS §§ 80.050, 78.760, not a flat fee."
    ),
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="NRS §§ 87A.540, 87A.315",
    threshold=QualificationThreshold(
        citation="NRS §§ 87A.540, 87A.315",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("75"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LP",
            "https://www.leg.state.nv.us/NRS/NRS-087A.html",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NRS §§ 87A.540, 87A.315", "LP sanctions require separate review."
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
    state="NV",
    name="Nevada",
    registered_agent=RegisteredAgentRequirement(
        citation="NRS §§ 77.300, 77.310",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "NRS: CHAPTER 86 - LIMITED-LIABILITY COMPANIES",
            "https://www.leg.state.nv.us/NRS/NRS-086.html",
        ),
        source(
            "NRS: CHAPTER 80 - FOREIGN CORPORATIONS", "https://www.leg.state.nv.us/NRS/NRS-080.html"
        ),
        source(
            "NRS: CHAPTER 78 - PRIVATE CORPORATIONS", "https://www.leg.state.nv.us/NRS/NRS-078.html"
        ),
        source(
            "NRS: CHAPTER 76 - STATE BUSINESS LICENSES",
            "https://www.leg.state.nv.us/NRS/NRS-076.html",
        ),
        source(
            "NRS: CHAPTER 77 - MODEL REGISTERED AGENTS ACT",
            "https://www.leg.state.nv.us/NRS/NRS-077.html",
        ),
        source(
            "NRS: CHAPTER 87A - UNIFORM LIMITED PARTNERSHIP ACT (2001)",
            "https://www.leg.state.nv.us/NRS/NRS-087A.html",
        ),
    ),
    version="2026-10-11-batch6",
    notes=(
        "LLC qualification is $75, with a $150 initial list and a $200 state business "
        "license unless exempt: $425 base total. Corporate qualification is a "
        "stock-based fee of at least $75 and at most $35,000, plus a $150 initial "
        "list and $500 license unless exempt: at least $725. Annual corporate lists "
        "are also stock-based; $150 is their minimum.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
