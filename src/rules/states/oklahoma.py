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
    qualification_citation="18 O.S. § 2043",
    threshold=QualificationThreshold(
        citation="18 O.S. § 2049",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Income-producing real or tangible personal property constitutes business "
            "except the enumerated exclusions. Isolated transactions must finish within "
            "30 days and not be repeated like transactions. Qualification exemptions do "
            "not determine tax, licensing, or service-of-process nexus."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("300"),
    forms=(
        StateForm(
            "Registration of foreign limited liability company",
            "SOS Form 0083",
            "https://www.sos.ok.gov/forms/Fm0083.PDF",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "18 O.S. § 2048",
        "Cannot maintain proceedings until registered; contracts and defenses remain "
        "valid. This section specifies no fixed monetary qualification fine; do not "
        "import corporate penalties.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual certificate",
            cycle="annual",
            due_rule="Anniversary of foreign registration each year.",
            fee=Decimal("25"),
            citation="18 O.S. § 2055.2",
            notes=(
                "Failure to file and pay within 60 days after the due date causes loss of "
                "good standing/registration."
            ),
        ),
        AnnualObligation(
            name="Secretary of State agent fee (conditional)",
            cycle="annual",
            due_rule="July 1, only when the Secretary of State acts as the LLC’s agent.",
            fee=Decimal("40"),
            citation="18 O.S. § 2055(13); SOS Form 0083",
            notes="No $40 fee is due if an additional eligible private agent is appointed.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction organization/good-standing certificate dated within the "
        "last 60 days, per SOS Form 0083."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="18 O.S. § 1130",
    threshold=QualificationThreshold(
        citation="18 O.S. § 1132",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "The corporate exceptions differ from the LLC list. Solicitation requires "
            "outside approval and shipment of goods with the specified stock/sample "
            "restrictions; ordinary solicitation, bank accounts, internal affairs and "
            "isolated transactions require review. Purely interstate operations are "
            "excepted; separate tax and process rules still apply."
        ),
        exempt_activities=frozenset({Activity.INTERSTATE_COMMERCE}),
    ),
    filing_fee=Decimal("300"),
    forms=(
        StateForm(
            "Certificate of qualification",
            "SOS Form 0012",
            "https://www.sos.ok.gov/forms/Fm0012.PDF",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "18 O.S. §§ 1134, 1137",
        "Corporate fines of $200–$500 per offense; agents may separately face "
        "$100–$500 per offense. Specified certificate/fee failures after notice can "
        "add $25 per day capped at $500 per offense. Court access requires authority "
        "and payment of applicable arrears; assess notice, offenses, tax periods and "
        "fees manually.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Secretary of State registered-agent fee",
            cycle="annual",
            due_rule="July 1 each year; collected by the Oklahoma Tax Commission.",
            fee=Decimal("100"),
            citation="18 O.S. § 1142(A)(18); OTC Form 200-R guidance",
            notes=(
                "Continues after franchise-tax repeal; the statutory delinquency/suspension "
                "provision applies after September 1."
            ),
        ),
        AnnualObligation(
            name="Invested-capital certificate (conditional)",
            cycle="annual",
            due_rule=(
                "Anniversary of qualification, until the filing fee has been paid on total "
                "authorized capitalization."
            ),
            fee=None,
            citation="18 O.S. § 1142(A)(17)",
            notes=(
                "Report maximum Oklahoma invested capital and capital previously paid upon. "
                "Additional fees are 0.1% of excess invested capital, subject to the "
                "authorized-capital limit; this is not a flat $25 LLC annual certificate."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate evidencing existence dated no earlier than six "
        "months before filing; assets/liabilities statement must also be no earlier "
        "than six months, under § 1130."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Oklahoma SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="Oklahoma SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("300"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.sos.ok.gov/business/forms.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Oklahoma SOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="OK",
    name="Oklahoma",
    registered_agent=RegisteredAgentRequirement(
        citation="18 O.S. §§ 2043, 1130; SOS foreign LLC/corporate instructions",
        notes=(
            "Foreign corporations maintain the Secretary of State as agent and may "
            "appoint an additional private agent. Foreign LLCs may appoint an eligible "
            "private agent or use the Secretary of State. Any private agent must maintain "
            "an actual Oklahoma business office open during regular hours; a PO box alone "
            "is insufficient. LP rules require separate review."
        ),
        private_appointment_required=False,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Foreign Limited Liability Company - Registration",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=552968",
        ),
        source(
            "Registration Required to Transact Business in State-Foreign Limited Liability Company",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67218",
        ),
        source(
            "Foreign Limited Liability Company - Acts Not Constituting Transacting "
            "Business In State",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67219",
        ),
        source("Fees", "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67225"),
        source(
            "Annual Certificate for Domestic Limited Liability Company and Registered "
            "Series and Foreign Limited Liability Company",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=552969",
        ),
        source(
            "OSCN Found Document:Foreign Corporations; Definition; Qualification to do "
            "Business in State; Procedure",
            "https://www.oscn.net/applications/OCISWeb/DeliverDocument.asp?CiteID=67139",
        ),
        source(
            "Exceptions to Requirements",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67141",
        ),
        source(
            "Violations and Penalties",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67143",
        ),
        source(
            "Actions By and Against Unqualified Foreign Corporations",
            "https://www.oscn.net/applications/oscn/DeliverDocument.asp?CiteID=67146",
        ),
        source(
            "OSCN Found Document:Filing and Other Service Fees",
            "https://www.oscn.net/applications/OCISWeb/DeliverDocument.asp?CiteID=67153",
        ),
        source(
            "Oklahoma Secretary of State - Business Forms",
            "https://www.sos.ok.gov/business/forms.aspx",
        ),
        source(
            "APPLICATION FOR REGISTRATION of a Foreign Limited Liability Company",
            "https://www.sos.ok.gov/forms/Fm0083.PDF",
        ),
        source(
            "CERTIFICATE OF QUALIFICATION Foreign Corporation",
            "https://www.sos.ok.gov/forms/Fm0012.PDF",
        ),
        source("Other Taxes", "https://oklahoma.gov/tax/businesses/other-taxes.html"),
    ),
    version="2026-10-11-batch7",
    notes=(
        "Foreign LLC registration costs $300. Corporate qualification costs 0.1% of "
        "maximum capital invested in Oklahoma during the fiscal year, with a $300 "
        "minimum and no fee base above authorized capital (18 O.S. § 1142(A)(13)). "
        "LLC annual certificates cost $25. The Secretary of State agent fee is $40 "
        "annually for LLCs using that agent and $100 annually for foreign "
        "corporations, payable to the Tax Commission for corporations. Franchise-tax "
        "filing ended after tax year 2023; agent fees continue.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "Rules reflect law reviewed on October 11, 2026. OSCN labels the cited § 2043 "
        "and § 2055.2 texts as being superseded November 1, 2026; the separate § "
        "2055.2 text that will go into effect then is not used as current law. "
        "Recheck the enacted amendment for filings on or after November 1.",
    ),
)
