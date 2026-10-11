"""Hawaii rules reviewed against official statutes and filing guidance."""

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
    qualification_citation="HRS §§ 428-1002, 428-1008",
    threshold=QualificationThreshold(
        citation="HRS § 428-1003",
        trigger_activities=frozenset(
            {
                Activity.OFFICE,
                Activity.LOCAL_SERVICES,
                Activity.RETAIL,
                Activity.INTRASTATE_BUSINESS,
                Activity.INCOME_PRODUCING_PROPERTY,
            }
        ),
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be similar "
            "recurring transactions. Under § 428-1003(b), ownership of income-producing "
            "real or tangible personal property, other than excluded property, "
            "constitutes transacting business."
        ),
    ),
    filing_fee=Decimal("51"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "FLLC-1",
            "https://files.hawaii.gov/dcca/breg/registration/forms/fllc-1.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "HRS § 428-1008(e)",
        (
            "Historical fees and penalties that would have applied if authority and required "
            "reports had been filed. No fixed dollar civil-penalty maximum is stated in this "
            "provision; do not treat unknown charges as zero."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Due March 31, June 30, September 30 or December 31 according to the quarter of "
                "registration, starting the following year."
            ),
            fee=Decimal("12.50"),
            citation="HRS § 428-210; DCCA 2026 annual-report notice",
            notes=(
                "$12.50 online. DCCA states a $10 late fee per delinquent year; confirm paper "
                "pricing before filing."
            ),
        ),
    ),
    consequences=(
        (
            "Failure to qualify does not invalidate contracts or prevent defending "
            "proceedings; maintaining an action requires qualification."
        ),
    ),
    good_standing_evidence=(
        "Attach an authenticated home-jurisdiction certificate of existence or similar "
        "record dated no more than 60 days before filing. Provide a sworn translation if "
        "needed."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="HRS §§ 414-431, 414-432",
    threshold=QualificationThreshold(
        citation="HRS § 414-431(b)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Owning property without more is listed; operations require "
            "separate screening."
        ),
    ),
    filing_fee=Decimal("51"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "FC-1",
            "https://cca.hawaii.gov/breg/registration/fpc/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "HRS § 414-432(d)",
        (
            "Historical fees and associated nonpayment penalties for the years or parts of "
            "years without authority. The Attorney General recovers amounts due; calculation "
            "remains manual."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Due March 31, June 30, September 30 or December 31 according to the quarter of "
                "registration, starting the following year."
            ),
            fee=Decimal("12.50"),
            citation="HRS § 414-472; DCCA 2026 annual-report notice",
            notes=(
                "$12.50 online. DCCA states a $10 late fee per delinquent year; confirm paper "
                "pricing before filing."
            ),
        ),
    ),
    consequences=(
        (
            "Failure to qualify does not invalidate contracts or prevent defending "
            "proceedings; maintaining an action requires qualification."
        ),
    ),
    good_standing_evidence=(
        "Attach an authenticated home-jurisdiction good-standing certificate dated no "
        "more than 60 days before filing. Provide a sworn translation if needed."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Hawaii DCCA foreign LP registration instructions",
    threshold=QualificationThreshold(
        citation="Foreign LP statutory exemptions require manual review",
        exempt_activities=frozenset(),
        notes=(
            "Official LP application and $50 filing plus $1 archives fee are populated; "
            "LLC and corporate exemptions are not applied to LPs."
        ),
    ),
    filing_fee=Decimal("51"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "FLP-1",
            "https://cca.hawaii.gov/breg/registration/flp/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Foreign LP sanctions require manual review",
        (
            "LP sanctions and reporting applicability are outside this LLC/C-Corp statutory "
            "review; obtain an entity-specific assessment."
        ),
    ),
    consequences=(
        ("LP remedies and litigation consequences require an entity-specific statutory review."),
    ),
    good_standing_evidence=(
        "Confirm the home-jurisdiction evidence required by the current entity-specific "
        "filing instructions."
    ),
)

REQUIREMENT = StateRequirement(
    state="HI",
    name="Hawaii",
    registered_agent=RegisteredAgentRequirement(
        citation="Hawaii DCCA FLLC-1 and FC-1 agent instructions",
        notes=(
            "Appoint an eligible consenting agent with a physical Hawaii street address for "
            "service, as required by the entity-specific application; a post office box alone "
            "is insufficient."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "HRS § 428-1002 foreign LLC application and certificate",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0428/HRS_0428-1002.htm",
        ),
        source(
            "HRS § 428-1003 activity exclusions",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0428/HRS_0428-1003.htm",
        ),
        source(
            "HRS § 414-431 authority and exclusions",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0414/HRS_0414-0431.htm",
        ),
        source(
            "HRS § 428-1008 failure to qualify",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0428/HRS_0428-1008.htm",
        ),
        source(
            "HRS § 414-432 failure to qualify",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0414/HRS_0414-0432.htm",
        ),
        source(
            "HRS § 428-210 annual reports",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0428/HRS_0428-0210.htm",
        ),
        source(
            "HRS § 414-472 annual reports",
            "https://www.capitol.hawaii.gov/hrscurrent/Vol08_Ch0401-0429/HRS0414/HRS_0414-0472.htm",
        ),
        source(
            "DCCA foreign LLC fees and instructions",
            "https://cca.hawaii.gov/breg/registration/fllc/",
        ),
        source(
            "DCCA foreign corporation fees and instructions",
            "https://cca.hawaii.gov/breg/registration/fpc/",
        ),
        source(
            "DCCA FLLC-1 application",
            "https://files.hawaii.gov/dcca/breg/registration/forms/fllc-1.pdf",
        ),
        source("DCCA business registration FAQs", "https://cca.hawaii.gov/breg/faqs/"),
        source(
            "DCCA foreign LP filing instructions", "https://cca.hawaii.gov/breg/registration/flp/"
        ),
        source(
            "DCCA July 1, 2026 annual-report notice",
            "https://cca.hawaii.gov/breg/third-quarter-hawaii-annual-business-reports-due-2026/",
        ),
    ),
    version="2026-10-11-batch3",
    notes=(
        (
            "The qualification total is $51: $50 filing fee plus mandatory $1 State "
            "Archives fee. Expedited service adds $25. Annual reports follow the "
            "registration quarter; taxes and optional services are separate."
        ),
    ),
    review_disclosures=(
        (
            "This batch verifies LLC and C-Corp statutory rules. LP entries contain "
            "official filing fees and forms only; LP exemptions, sanctions and reporting "
            "require a separate statutory review and are screened manually."
        ),
    ),
)
