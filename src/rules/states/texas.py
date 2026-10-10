"""Texas qualification rules and separate franchise reporting obligations."""

from datetime import date
from decimal import Decimal

from ...models import (
    Activity,
    AnnualObligation,
    EntityRequirement,
    EntityType,
    LegalSource,
    PenaltyPeriod,
    PenaltyPolicy,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)

_STATUTES = "https://tcss.legis.texas.gov/resources"
_BOC = f"{_STATUTES}/BO/htm/BO.9.htm"
_FEE = "https://www.sos.state.tx.us/corp/forms/806_boc.pdf"
_TAX = "https://comptroller.texas.gov/taxes/franchise/"
_REVIEWED = date(2026, 10, 10)

_REGISTRATION_PENALTY = PenaltyPolicy(
    citation="Tex. Bus. Orgs. Code § 9.054; Texas SOS foreign-entity registration instructions",
    description=(
        "$750 per calendar year or part of a calendar year of unregistered Texas "
        "business. Registration on or before the 90th day after beginning business "
        "is exempt. Once that exemption is lost, count the whole unauthorized "
        "interval, not only days after day 90. The SOS may collect the fee and "
        "condition registration on payment. No interest compounding is specified."
    ),
    amount_min=Decimal("750"),
    amount_max=Decimal("750"),
    period=PenaltyPeriod.CALENDAR_YEAR,
    grace_days=90,
    assessment="statutory_late_registration_fee",
    unquantified_components=(
        "Separate civil exposure under BOC § 9.052 equals fees and taxes that "
        "would have been imposed if registered when first required, plus penalties "
        "and interest for failure to pay those fees and taxes; historical "
        "filing and tax-account facts are needed. The 90-day exemption only "
        "waives this policy's late filing fee.",
    ),
)

_LP_PERIODIC = AnnualObligation(
    name="SOS limited-partnership periodic report, when requested",
    cycle="on_notice_not_more_than_once_every_four_years",
    due_rule="Within 30 days of the SOS first notification when a periodic report is required.",
    fee=Decimal("50"),
    citation="Tex. Bus. Orgs. Code §§ 153.301–153.312; Texas SOS Form 804 instructions",
    late_penalty=PenaltyPolicy(
        citation="Texas SOS Form 804 instructions and Form 806 fee schedule",
        description=(
            "$25 per month or part, capped at $100, after forfeiture for failure "
            "to file within 30 days of first notification. Start the interval at "
            "forfeiture, not the first report notice. This excludes the $50 "
            "report fee and any additional reinstatement fee."
        ),
        amount_min=Decimal("25"),
        amount_max=Decimal("25"),
        period=PenaltyPeriod.STARTED_MONTH,
        cap=Decimal("100"),
        assessment="sos_periodic_report_after_forfeiture",
    ),
    notes=(
        "Applies when an LP is not required to file a PIR under Tax Code § 171.203 "
        "and the SOS requires a report. Failure to file by the 30th day after "
        "the first notice is mailed forfeits Texas business rights; a separate "
        "forfeiture notice follows. Revocation may follow failure to revive "
        "within 120 days after the forfeiture notice is mailed. Reinstatement "
        "filing totals $225: $50 report, "
        "$100 late fee and $75 reinstatement, plus tax clearance and any applicable taxes."
    ),
)


def _entity(entity_type: EntityType, form_number: str, form_name: str) -> EntityRequirement:
    return EntityRequirement(
        entity_type=entity_type,
        qualification_citation="Tex. Bus. Orgs. Code § 9.001",
        threshold=QualificationThreshold(
            citation="Tex. Bus. Orgs. Code §§ 9.001, 9.251",
            exempt_activities=frozenset(
                {Activity.INTERSTATE_COMMERCE, Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}
            ),
            isolated_transaction_max_days=30,
            notes=(
                "Regular Texas operational business is screened for registration. "
                "Interstate-only commerce, bank accounts, internal affairs, "
                "and a nonrepeated isolated transaction completed within 30 days "
                "are safe harbors. Out-of-state order acceptance alone is not "
                "an enumerated § 9.251 exemption and requires review. The "
                "statutory list is nonexclusive under § 9.252. These registration "
                "exemptions do not decide franchise tax nexus."
            ),
        ),
        filing_fee=Decimal("750"),
        forms=(
            StateForm(
                form_name,
                form_number,
                f"https://www.sos.state.tx.us/corp/forms/{form_number}_boc.pdf",
            ),
        ),
        qualification_penalty=_REGISTRATION_PENALTY,
        annual_obligations=(
            AnnualObligation(
                name="Franchise tax filings and Public Information Report",
                cycle="annual",
                due_rule="Generally May 15, subject to tax-account requirements and extensions.",
                fee=None,
                citation="Tex. Tax Code §§ 171.202–171.203, 171.251–171.362",
                late_penalty=PenaltyPolicy(
                    citation="Tex. Tax Code §§ 171.362, 111.060, 171.251–171.301",
                    description=(
                        "$50 for each missed required report, regardless of tax "
                        "due or later filing; late payment or reporting incurs "
                        "5% of tax due, plus another 5% after 30 days, with interest "
                        "beginning on day 61 under Comptroller guidance. "
                        "The tax-percentage penalty has a statutory $1 minimum; "
                        "tax-account balances, due dates "
                        "and relief determine the additional amounts."
                    ),
                    amount_min=Decimal("50"),
                    amount_max=Decimal("50"),
                    assessment="tax_account_specific",
                    unquantified_components=(
                        "Unpaid-tax penalties, interest and applicable relief "
                        "require tax-account facts; the modeled $50 is only "
                        "the late-report component.",
                    ),
                ),
                notes=(
                    "No general SOS annual report for these entity types; some "
                    "LPs must file an SOS periodic report when notified. "
                    "No-tax-due thresholds and return exemptions do not automatically "
                    "eliminate PIR reporting. Tax-exempt, qualifying passive and "
                    "new veteran-owned entities may have reporting exemptions. Tax forfeiture "
                    "for report/tax/penalty defaults follows a 45-day notice and "
                    "cure period under §§ 171.251, 171.2515 and 171.256; restore "
                    "tax rights and SOS authority through the applicable processes."
                ),
            ),
        )
        + ((_LP_PERIODIC,) if entity_type == EntityType.LP else ()),
        consequences=(
            "Unregistered foreign entities may be restricted from maintaining Texas "
            "actions and may face enforcement under BOC §§ 9.051–9.053; contractual "
            "validity and the right to defend are preserved as provided by law.",
            "Texas tax forfeiture is distinct from missing foreign registration and "
            "does not automatically determine domestic-state standing.",
            "For an existing registration, the SOS may revoke under BOC § 9.101 "
            "if report, fee/penalty, agent/office or amendment defaults remain "
            "uncorrected before the 91st day after mailed notice; unpaid or "
            "dishonored registration fees use the 16th day. These notice periods "
            "do not give unregistered entities authority to conduct business.",
            "BOC §§ 9.103–9.104 reinstatement requires curing applicable defaults "
            "and filing by the third anniversary of revocation, with Comptroller "
            "tax clearance for taxable entities. Tax-Code forfeitures and court "
            "terminations use separate procedures.",
        ),
        good_standing_evidence=(
            "Confirm continued legal existence and domestic authority before "
            "executing the registration application. Standard Texas applications "
            "do not ordinarily require attaching a home-state status certificate; "
            "regulated entity types may need additional evidence."
        ),
    )


REQUIREMENT = StateRequirement(
    state="TX",
    name="Texas",
    registered_agent=RegisteredAgentRequirement(
        citation="Tex. Bus. Orgs. Code §§ 5.201–5.206",
        notes=(
            "Eligible consenting individual Texas resident or eligible organization, "
            "with a Texas street address where process can be personally served "
            "during normal business hours; the registered office is a business office, "
            "not solely a mailbox/answering service. Entity cannot be its own agent. "
            "Retain the agent's consent; filing the consent separately is optional."
        ),
    ),
    entity_rules={
        EntityType.C_CORP: _entity(
            EntityType.C_CORP,
            "301",
            "Application for Registration of a Foreign For-Profit Corporation",
        ),
        EntityType.LLC: _entity(
            EntityType.LLC,
            "304",
            "Application for Registration of a Foreign Limited Liability Company",
        ),
        EntityType.LP: _entity(
            EntityType.LP, "306", "Application for Registration of a Foreign Limited Partnership"
        ),
    },
    sources=(
        LegalSource("Tex. Bus. Orgs. Code Chapter 9", _BOC, _REVIEWED),
        LegalSource(
            "Tex. Bus. Orgs. Code Chapter 5",
            f"{_STATUTES}/BO/htm/BO.5.htm",
            _REVIEWED,
        ),
        LegalSource(
            "Tex. Bus. Orgs. Code Chapter 153",
            f"{_STATUTES}/BO/htm/BO.153.htm",
            _REVIEWED,
        ),
        LegalSource("Texas SOS business filing fee schedule", _FEE, _REVIEWED),
        LegalSource(
            "Texas SOS Form 301", "https://www.sos.state.tx.us/corp/forms/301_boc.pdf", _REVIEWED
        ),
        LegalSource(
            "Texas SOS Form 304", "https://www.sos.state.tx.us/corp/forms/304_boc.pdf", _REVIEWED
        ),
        LegalSource(
            "Texas SOS Form 306", "https://www.sos.state.tx.us/corp/forms/306_boc.pdf", _REVIEWED
        ),
        LegalSource(
            "Texas SOS Form 304 instructions",
            "https://www.sos.state.tx.us/corp/instructions/304.shtml",
            _REVIEWED,
        ),
        LegalSource(
            "Texas SOS foreign entity FAQ",
            "https://www.sos.state.tx.us/corp/foreignfaqs.shtml",
            _REVIEWED,
        ),
        LegalSource(
            "Texas SOS registered agent FAQ",
            "https://www.sos.state.tx.us/corp/registeredagentfaqs.shtml",
            _REVIEWED,
        ),
        LegalSource(
            "Texas SOS Form 804 periodic LP report instructions",
            "https://www.sos.state.tx.us/corp/instructions/804.shtml",
            _REVIEWED,
        ),
        LegalSource("Tex. Tax Code Chapter 171", f"{_STATUTES}/TX/htm/TX.171.htm", _REVIEWED),
        LegalSource("Tex. Tax Code Chapter 111", f"{_STATUTES}/TX/htm/TX.111.htm", _REVIEWED),
        LegalSource("Texas Comptroller franchise tax guidance", _TAX, _REVIEWED),
        LegalSource(
            "Texas Comptroller PIR/OIR requirements",
            "https://comptroller.texas.gov/taxes/franchise/pir-oir-filing-req.php",
            _REVIEWED,
        ),
        LegalSource(
            "Texas Comptroller franchise reporting requirements",
            "https://comptroller.texas.gov/taxes/franchise/filing-requirements.php",
            _REVIEWED,
        ),
        LegalSource(
            "Texas Express processing options",
            "https://www.sos.state.tx.us/express.shtml",
            _REVIEWED,
        ),
        LegalSource(
            "Texas SOS filing/payment options",
            "https://www.sos.state.tx.us/corp/options.shtml",
            _REVIEWED,
        ),
    ),
    version="2026-10-10-official-source-review",
    notes=(
        "Official BOC Chapters 5, 9 and 153, Tax Code Chapters 111 and 171, and "
        "SOS/Comptroller guidance reviewed on October 10, 2026 support the encoded "
        "qualification, fee, reporting, penalty, agent and processing rules. Formal "
        "statute URLs use the legislature's document backend; legacy URLs returned "
        "a JavaScript homepage rather than statute text.",
        "Texas Express optional additional fee per document: standard expedited $50, "
        "typically 2–3 business days; next-day $500 or same-day $750 for requests "
        "received by noon Central, completed by close of the next/same business day. "
        "Same/next-day service is requested in SOSPortal or in person; standard "
        "expedite also permits mail. Ordinary processing has no fixed window on "
        "the reviewed guidance. Preclearance is an optional $50 per document.",
        "Initial agent designation is part of registration; optional separate "
        "filing of agent consent costs $15. Private agent-service charges are "
        "separate. SOSPortal credit-card convenience fee is $0.25 per transaction "
        "plus 2.25% of total fees; ACH and mailed check/money-order options exist.",
        "Qualification penalties, periodic-report sanctions and tax forfeiture "
        "are separate. Estimator amounts represent specified monetary components, "
        "not complete historical tax/civil liability.",
    ),
)
