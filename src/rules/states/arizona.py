"""Arizona LLC and corporation rules, with distinct isolated-transaction standards."""

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

_ACC = "https://azcc.gov/"
_LP_FORM = (
    "https://azsos.gov/sites/default/files/docs/bsd_20220107_Foreign_LP_Fontes_rev20240603.pdf"
)


def _entity(entity: EntityType) -> EntityRequirement:
    llc = entity == EntityType.LLC
    lp = entity == EntityType.LP
    citation = (
        "A.R.S. §§ 29-3902–29-3905"
        if llc
        else (
            "A.R.S. § 29-349; SOS foreign LP registration form"
            if lp
            else "A.R.S. §§ 10-1501–10-1503"
        )
    )
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation="A.R.S. § 29-3905" if llc else citation,
            **(
                {"exempt_activities": frozenset()}
                if lp
                else {"isolated_transaction_without_day_limit": True}
                if llc
                else {"isolated_transaction_max_days": 30}
            ),
            notes="LLCs: isolated transactions not in the course of similar transactions "
            "have no fixed day limit (§ 29-3905(A)(9)). Corporations: completion within "
            "30 days and no repeated like transactions (§ 10-1501(B)(10)). Both list bank "
            "accounts, internal affairs, interstate commerce and out-of-state acceptance "
            "of orders. LP safe harbors require separate review.",
        ),
        filing_fee=Decimal("20" if lp else "150" if llc else "175"),
        forms=(
            StateForm(
                "Foreign Registration Statement"
                if llc
                else "Foreign Limited Partnership Registration"
                if lp
                else "Application for Authority",
                "L025" if llc else "SOS foreign LP form" if lp else "C018",
                _LP_FORM
                if lp
                else _ACC + "corporations/forms/" + ("llc-forms" if llc else "corporation-forms"),
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "A.R.S. § 29-3902; ACC foreign-entity FAQ"
            if llc
            else "A.R.S. § 29-349; SOS foreign LP form"
            if lp
            else "A.R.S. § 10-1502(D), (F)",
            "Corporations owe historical fees and applicable penalties plus a civil "
            "penalty up to $1,000; injunction litigation can add costs and attorney fees. "
            "The $1,000 is not an annual multiplier. Applicant-specific amounts remain manual."
            if not llc and not lp
            else "LLC/LP sanctions require entity-specific review. Do not import the corporate "
            "$1,000 penalty into another entity type or infer a zero monetary exposure.",
        ),
        annual_obligations=()
        if llc or lp
        else (
            annual(
                "Annual report",
                "Each year on the ACC-assigned date in the anniversary month.",
                "45",
                "A.R.S. § 10-1622(C), (F); ACC fee schedule",
                "Late fee is 20% of the fee due per month or fraction ($9 on a $45 report) "
                "until paid or foreign authority revoked. A requested extension of up to six "
                "months does not extend the fee payment deadline.",
            ),
        ),
        consequences=(
            "An unqualified LLC or corporation cannot maintain Arizona court proceedings; "
            "contracts remain valid and defending proceedings is permitted.",
            "LLCs have no ACC annual report. Tax and licensing obligations remain separate. "
            "Corporations must maintain reports and statutory-agent information "
            "to avoid revocation.",
        ),
        good_standing_evidence="ACC foreign LLC/corporation applications require certified "
        "formation documents and amendments, plus a home-jurisdiction certificate of "
        "existence dated within 60 days of the application. LPs use the separate SOS form "
        "and its attachments; ACC certificate requirements are not automatically imposed on LPs.",
    )


REQUIREMENT = StateRequirement(
    state="AZ",
    name="Arizona",
    registered_agent=RegisteredAgentRequirement(
        citation="ACC statutory-agent FAQ; SOS foreign LP form",
        notes="Maintain a consenting statutory agent at an Arizona physical address. "
        "Use an eligible Arizona-resident individual or authorized entity; LLC/corporation "
        "filings go to the ACC, while LP filings go to the Secretary of State.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=tuple(
        source(citation, url)
        for citation, url in (
            ("A.R.S. § 29-3905", "https://www.azleg.gov/ars/29/03905.htm"),
            ("A.R.S. § 10-1501", "https://www.azleg.gov/ars/10/01501.htm"),
            ("A.R.S. § 10-1502", "https://www.azleg.gov/ars/10/01502.htm"),
            ("A.R.S. § 10-1622", "https://www.azleg.gov/ars/10/01622.htm"),
            (
                "ACC LLC fees",
                _ACC + "docs/default-source/corps-files/fee-schedules/fee-schedule-llcs.pdf",
            ),
            (
                "ACC corporation fees",
                _ACC
                + "docs/default-source/corps-files/fee-schedules/fee-schedule-corporations.pdf",
            ),
            ("ACC business-services FAQ", _ACC + "faqs"),
            ("ACC LLC forms", _ACC + "corporations/forms/llc-forms"),
            ("ACC corporation forms", _ACC + "corporations/forms/corporation-forms"),
            ("Arizona SOS foreign LP registration", _LP_FORM),
        )
    ),
    version="2026-10-11-batch2",
    notes=(
        "Standard ACC filing fees exclude optional expedited service and any applicable "
        "publication costs. The LP $20 base is $10 filing plus $10 authority; the SOS "
        "form also charges $3 per page, so $20 is not an all-in LP price. LP statutory "
        "sanctions and exemptions are outside this LLC/C-Corp batch and remain manual.",
    ),
)
