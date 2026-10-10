"""Wyoming foreign qualification and asset-based annual reporting rules."""

from datetime import date
from decimal import Decimal

from ...models import (
    Activity,
    AnnualObligation,
    EntityRequirement,
    EntityType,
    LegalSource,
    PenaltyPolicy,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)

_STATUTES = "https://wyoleg.gov/statutes/compress/title17.pdf"
_FEE = "https://sos.wyo.gov/Business/docs/BusinessFees.pdf"
_FAQ = "https://sos.wyo.gov/faqs.aspx?root=BUS"
_REVIEWED = date(2026, 10, 10)
_FORMS = {
    EntityType.C_CORP: "https://sos.wyo.gov/Forms/Business/FPROF/FP-CertificateAuthority.pdf",
    EntityType.LLC: "https://sos.wyo.gov/Forms/Business/FLLC/FLLC-CertificateAuthority.pdf",
    EntityType.LP: "https://sos.wyo.gov/Forms/Business/FLP/FLP-CertificateRegistration.pdf",
}

_PENALTY = PenaltyPolicy(
    citation="Wyo. Stat. § 17-16-1502(d); §§ 17-29-114, 17-29-211, 17-14-1007(e)",
    description=(
        "$5,000 fixed qualification penalty, plus historical fees/license taxes, "
        "18% statutory interest, reasonable audit expenses and attorney fees. "
        "No annual $5,000 repetition or compound-interest assumption."
    ),
    amount_min=Decimal("5000"),
    amount_max=Decimal("5000"),
    assessment="statutory_fixed_component_plus_unresolved_arrears",
    unquantified_components=(
        "Historical registration/report fees and asset-based license taxes "
        "need filing history and asset values.",
        "Statutory 18% interest requires historical balances and applicable accrual basis.",
        "Reasonable audit expenses and attorney fees require assessed amounts.",
    ),
)


def _entity(
    entity_type: EntityType,
    qualification_citation: str,
    annual_citation: str,
    form_name: str,
    fee: str,
) -> EntityRequirement:
    return EntityRequirement(
        entity_type=entity_type,
        qualification_citation=qualification_citation,
        threshold=QualificationThreshold(
            citation=(
                "Wyo. Stat. § 17-16-1501"
                if entity_type == EntityType.C_CORP
                else "Wyo. Stat. §§ 17-29-114, 17-16-1501"
                if entity_type == EntityType.LLC
                else "Wyo. Stat. § 17-14-1002; entity-specific transaction facts"
            ),
            isolated_transaction_max_days=30 if entity_type != EntityType.LP else None,
            exempt_activities=(
                frozenset({Activity.INTERSTATE_COMMERCE})
                if entity_type == EntityType.LP
                else frozenset(
                    {
                        Activity.INTERSTATE_COMMERCE,
                        Activity.BANK_ACCOUNT,
                        Activity.INTERNAL_AFFAIRS,
                        Activity.SOLICITATION,
                    }
                )
            ),
            notes=(
                "Regular Wyoming operational business is a screening trigger. "
                "Corporate § 17-16-1501 safe harbors apply to LLCs through "
                "§ 17-29-114, including a nonrepeated transaction completed within "
                "30 days. Do not assume the corporate isolated-transaction safe "
                "harbor applies to LPs without reviewing applicable law."
            ),
        ),
        filing_fee=Decimal(fee),
        forms=(StateForm(form_name, "SOS foreign-entity application", _FORMS[entity_type]),),
        qualification_penalty=_PENALTY,
        annual_obligations=(
            AnnualObligation(
                name="Annual report and license tax",
                cycle="annual",
                due_rule=(
                    "First day of the Wyoming registration/qualification anniversary "
                    "month shown on the SOS record; reports may be filed up to "
                    "120 days before that due date."
                ),
                fee=None,
                citation=annual_citation,
                late_penalty=PenaltyPolicy(
                    citation=(
                        "Wyo. Stat. §§ 17-16-1530–17-16-1535; applicable entity cross-references"
                    ),
                    description=(
                        "SOS guidance warns of administrative dissolution/revocation "
                        "after 60 days without the required report. Foreign-corporate "
                        "revocation under § 17-16-1531 requires notice and 60 days "
                        "after perfected service to cure. Reinstatement and unpaid "
                        "tax/report costs are separately determined."
                    ),
                    assessment="administrative_notice_and_cure",
                    unquantified_components=(
                        "Reinstatement costs and unpaid asset-based license taxes "
                        "depend on filing history.",
                    ),
                ),
                notes=(
                    "License-tax formula: greater of $60 or 0.0002 of "
                    "Wyoming assets, subject to statutory valuation and exclusions. "
                    "Asset inputs are required; $60 is a floor, not a universal annual cost. "
                    "Online filing adds a payment-processor convenience fee. "
                    "Use the actual SOS-record due date for scheduling."
                ),
            ),
        ),
        consequences=(
            "Cannot maintain Wyoming proceedings until authorized/registered; "
            "contract validity and the ability to defend proceedings are preserved.",
            "SOS may withhold authority until qualification sanctions, arrears and costs are paid.",
            "Administrative revocation follows notice and applicable statutory cure "
            "procedures; it is not a change to the entity's home-state standing.",
        ),
        good_standing_evidence=(
            "Original domestic-state certificate of existence/good standing, "
            "issued no more than 60 days before Wyoming filing, and written "
            "registered-agent consent for each requested entity type. "
            "Restore domestic existence/authority first."
        ),
    )


REQUIREMENT = StateRequirement(
    state="WY",
    name="Wyoming",
    registered_agent=RegisteredAgentRequirement(
        citation="Wyo. Stat. §§ 17-28-101–17-28-111",
        notes=(
            "Eligible consenting agent with a physical Wyoming registered office "
            "available for service with the agent or an authorized natural person "
            "physically present. Individual agents must be at least 18 and resident "
            "in Wyoming. A drop box is not acceptable; a PO box can supplement "
            "the required physical address for mailing."
        ),
    ),
    entity_rules={
        EntityType.C_CORP: _entity(
            EntityType.C_CORP,
            "Wyo. Stat. §§ 17-16-1501, 17-16-1503",
            "Wyo. Stat. § 17-16-1630",
            "Foreign Profit Corporation Application for Certificate of Authority",
            "150",
        ),
        EntityType.LLC: _entity(
            EntityType.LLC,
            "Wyo. Stat. §§ 17-29-114, 17-16-1501–17-16-1503",
            "Wyo. Stat. § 17-29-209",
            "Foreign Limited Liability Company Application for Certificate of Authority",
            "150",
        ),
        EntityType.LP: _entity(
            EntityType.LP,
            "Wyo. Stat. § 17-14-1002",
            "Wyo. Stat. §§ 17-14-209(b), 17-16-1630",
            "Foreign Limited Partnership Application for Registration",
            "150",
        ),
    },
    sources=(
        LegalSource("Wyoming Statutes Title 17", _STATUTES, _REVIEWED),
        LegalSource("Wyoming SOS business filing fees effective July 1, 2026", _FEE, _REVIEWED),
        LegalSource(
            "Wyoming SOS foreign corporation authority form", _FORMS[EntityType.C_CORP], _REVIEWED
        ),
        LegalSource("Wyoming SOS foreign LLC authority form", _FORMS[EntityType.LLC], _REVIEWED),
        LegalSource("Wyoming SOS foreign LP registration form", _FORMS[EntityType.LP], _REVIEWED),
        LegalSource(
            "Wyoming SOS business and annual-report FAQ",
            _FAQ,
            _REVIEWED,
        ),
        LegalSource(
            "Wyoming SOS registered agent FAQ",
            "https://sos.wyo.gov/faqs.aspx?root=RAO",
            _REVIEWED,
        ),
    ),
    version="2026-10-10-official-source-review",
    notes=(
        "Official Wyoming statutes, current SOS fee schedule and application "
        "instructions reviewed October 10, 2026. All three foreign registration "
        "fees are $150; § 17-14-209(a)(v) supersedes the older LP $100 fee. "
        "Annual license tax has a $60 floor, not the historical $50 amount.",
        "Foreign-entity filings are mailed and processed in receipt order, "
        "with a maximum processing time of 15 business days after receipt. "
        "Wyoming does not offer expedited filing under the reviewed instructions.",
        "Initial agent designation/consent is included in the qualification "
        "form; a separate later Appointment of New Registered Agent/Office costs "
        "$5. Private agent fees are separate. A commercial agent's own $50 "
        "annual registration is not an entity qualification charge.",
        "The formal sources are the reviewed official publications. Historical "
        "mirror corroboration was superseded by live verification; see "
        "docs/verification/wyoming.md for evidence and remaining fact-dependent calculations.",
    ),
)
