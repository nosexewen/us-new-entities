"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

from decimal import Decimal

from ...models import (
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
    qualification_citation="Va. Code § 13.1-1052",
    threshold=QualificationThreshold(
        citation="Va. Code § 13.1-1059",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Motion-picture production lasting less than 90 "
            "consecutive days, with out-of-state processing/marketing/distribution, has a "
            "separate conditional exemption requiring manual review."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for registration",
            "LLC1052",
            "https://www.scc.virginia.gov/businesses/forms-and-fees/foreign-limited-liability-companies/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Va. Code §§ 13.1-1057–1058",
        "Cannot maintain an action until registered; contracts and defense remain "
        "valid. Members, managers or employees who knowingly transact unauthorized "
        "business may face $500–$5,000 each; this is not an automatic flat entity "
        "fine. Attorney General restraint and fact-specific recovery require review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual registration fee (no LLC annual report)",
            cycle="annual",
            due_rule=(
                "Last day of the Virginia registration anniversary month, beginning the "
                "following year; follow any SCC-assigned date."
            ),
            fee=Decimal("50"),
            citation="Va. Code §§ 13.1-1062, 13.1-1064",
            notes=(
                "Late payment adds $25. No LLC annual report is required; this is a separate "
                "registration-fee payment."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated/certified copies of articles and all applicable amendments, "
        "corrections, mergers, conversions or domestications; certification no more "
        "than 12 months old per SCC checklist. A certificate merely showing good "
        "standing is not a substitute."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Va. Code §§ 13.1-757, 13.1-759",
    threshold=QualificationThreshold(
        citation="Va. Code § 13.1-757",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Separate conditional motion-picture exemption "
            "requires manual review."
        ),
    ),
    filing_fee=Decimal("75"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "SCC759",
            "https://www.scc.virginia.gov/media/sccvirginiagov-home/business-home/business-faqs/foreign-business-entities/scc759.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Va. Code § 13.1-758",
        "Cannot maintain a proceeding until authorized; contracts and defense remain "
        "valid. Directors, officers or employees who knowingly transact unauthorized "
        "business may face $500–$5,000 each; do not apply that range automatically to "
        "the entity. Other cure requirements require manual review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Last day of Virginia authorization anniversary month, beginning the "
                "following year; follow the SCC assessment."
            ),
            fee=Decimal("0"),
            citation="Va. Code § 13.1-775",
            notes=(
                "Annual report filing is free; the separate annual registration fee remains "
                "payable."
            ),
        ),
        AnnualObligation(
            name="Annual registration fee (share-based)",
            cycle="annual",
            due_rule="Last day of Virginia authorization anniversary month, as assessed by SCC.",
            fee=None,
            citation="Va. Code § 13.1-775.1; SCC February 2026 annual schedule",
            notes=(
                "Virginia annual corporate fee discrepancy: Code § 13.1-775.1, including the "
                "separately retrieved section, states $50 for up to 5,000 authorized shares "
                "plus $15 per additional 5,000 or fraction, capped at $850. The SCC February "
                "2026 annual assessment schedule instead states $100 plus $30 per additional "
                "5,000, capped at $1,700. Both figures are disclosed; confirm the actual CIS "
                "assessment with SCC before payment. No single flat corporate annual fee is "
                "modeled. Late payment adds the greater of $10 or 10% of the annual fee."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated/certified articles and applicable amendments/corrections and "
        "transaction documents, certified within 12 months per SCC checklist; a "
        "good-standing certificate alone is insufficient."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Va. Code §§ 50-73.54, 50-73.17(B)(2)",
    threshold=QualificationThreshold(
        citation="Va. Code §§ 50-73.54, 50-73.17(B)(2)",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://law.lis.virginia.gov/vacode/title50/chapter2.1/section50-73.17/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Va. Code §§ 50-73.54, 50-73.17(B)(2)", "LP sanctions require separate review."
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
    state="VA",
    name="Virginia",
    registered_agent=RegisteredAgentRequirement(
        citation="Va. Code §§ 13.1-1015, 13.1-1052, 13.1-763",
        notes=(
            "Continuously maintain a Virginia registered office and eligible agent. An "
            "individual Virginia resident must satisfy the applicable LLC "
            "member/manager/related-management eligibility or corporate officer/director "
            "eligibility, or be a Virginia State Bar member. Eligible authorized business "
            "entities may also serve. Residency alone is insufficient; an outside "
            "commercial vendor is not compulsory."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Code of Virginia Code - Chapter 12. Virginia Limited Liability Company Act",
            "https://law.lis.virginia.gov/vacodefull/title13.1/chapter12/",
        ),
        source(
            "Code of Virginia Code - Chapter 9. Virginia Stock Corporation Act",
            "https://law.lis.virginia.gov/vacodefull/title13.1/chapter9/",
        ),
        source(
            "§ 13.1-775.1. Annual registration fees to be paid by domestic and foreign "
            "corporations; penalty for failure to pay timely",
            "https://law.lis.virginia.gov/vacode/title13.1/chapter9/section13.1-775.1/",
        ),
        source(
            "§ 13.1-615.1. Charter and entrance fees for corporations",
            "https://law.lis.virginia.gov/vacode/title13.1/chapter9/section13.1-615.1/",
        ),
        source(
            "§ 13.1-616. Fees for filing documents or issuing certificates",
            "https://law.lis.virginia.gov/vacode/title13.1/chapter9/section13.1-616/",
        ),
        source(
            "Virginia SCC - Annual Registration Fees",
            "https://www.scc.virginia.gov/businesses/business-faqs/annual-registration-fees/",
        ),
        source(
            "Virginia SCC - Annual Reports",
            "https://www.scc.virginia.gov/businesses/business-faqs/clerks-annual-reports/",
        ),
        source(
            "Virginia SCC - Foreign Limited Liability Companies",
            "https://www.scc.virginia.gov/businesses/forms-and-fees/foreign-limited-liability-companies/",
        ),
        source(
            "Virginia SCC - Foreign Corporations",
            "https://www.scc.virginia.gov/businesses/forms-and-fees/foreign-corporations/",
        ),
        source(
            "Instructions to Form SCC759/921 - Application for Certificate of Authority "
            "to Transact Business in Virginia",
            "https://www.scc.virginia.gov/media/sccvirginiagov-home/business-home/business-faqs/foreign-business-entities/scc759.pdf",
        ),
        source(
            "Microsoft Word - an_fee",
            "https://www.scc.virginia.gov/media/sccvirginiagov-home/business-home/business-faqs/annual-registration-fees/an_fee.pdf",
        ),
        source(
            "Virginia SCC - Foreign Registration Checklist",
            "https://www.scc.virginia.gov/businesses/cis-help/foreign-registration-checklist/",
        ),
        source(
            "§ 50-73.17. Filing; fees; effective time and date",
            "https://law.lis.virginia.gov/vacode/title50/chapter2.1/section50-73.17/",
        ),
    ),
    version="2026-10-11-batch9",
    notes=(
        "Foreign LLC registration $100 and annual registration fee $50; no LLC annual "
        "report. Foreign stock corporation registration minimum $75: $25 filing plus "
        "$50 entrance fee per 25,000 authorized shares or fraction up to one million "
        "shares; above one million, entrance fee $2,500. The corporation filing fee "
        "is separate from its annual registration assessment.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "Virginia annual corporate fee discrepancy: Code § 13.1-775.1, including the "
        "separately retrieved section, states $50 for up to 5,000 authorized shares "
        "plus $15 per additional 5,000 or fraction, capped at $850. The SCC February "
        "2026 annual assessment schedule instead states $100 plus $30 per additional "
        "5,000, capped at $1,700. Both figures are disclosed; confirm the actual CIS "
        "assessment with SCC before payment. No single flat corporate annual fee is "
        "modeled.",
    ),
)
