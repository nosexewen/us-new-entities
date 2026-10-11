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
    qualification_citation="Minn. Stat. § 322C.0802",
    threshold=QualificationThreshold(
        citation="Minn. Stat. § 322C.0803",
        isolated_transaction_max_days=30,
        notes=(
            "Income-producing real or tangible personal property constitutes transacting "
            "business except the specified fiduciary holdings. Solicitation and "
            "interstate-commerce claims require individual review; they are not "
            "enumerated in § 322C.0803. Isolated transactions must finish within 30 days "
            "and not be repeated like transactions. Qualification exemptions do not "
            "determine tax, licensing, or service-of-process nexus."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
        trigger_activities=frozenset(
            {
                Activity.OFFICE,
                Activity.LOCAL_SERVICES,
                Activity.RETAIL,
                Activity.INTRASTATE_BUSINESS,
                Activity.INCOME_PRODUCING_PROPERTY,
            }
        ),
    ),
    filing_fee=Decimal("185"),
    forms=(
        StateForm(
            "Certificate of authority",
            "Foreign LLC",
            "https://www.sos.mn.gov/business-liens/business-forms-fees/foreign-limited-liability-company-forms/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Minn. Stat. §§ 322C.0808–322C.0809",
        "Maintaining proceedings is barred until authority is obtained; "
        "attorney-general injunctive relief is authorized. These sections do not "
        "supply a numeric late-qualification fee; review monetary exposure "
        "separately.",
    ),
    annual_obligations=(
        annual(
            "Annual renewal",
            "December 31, beginning the calendar year after registration.",
            "0",
            "Minn. Stat. § 322C.0208",
            "",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application attests compliance with home-jurisdiction organizational law; § "
        "322C.0802 does not prescribe a certificate attachment or numeric freshness "
        "limit."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Minn. Stat. §§ 303.03, 303.06",
    threshold=QualificationThreshold(
        citation="Minn. Stat. § 303.03",
        isolated_transaction_max_days=30,
        notes=(
            "Solicitation and interstate-commerce claims require individual review; they "
            "are not enumerated in § 303.03. Isolated transactions must finish within 30 "
            "days and not be repeated like transactions. Qualification exemptions do not "
            "determine tax, licensing, or service-of-process nexus."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
    ),
    filing_fee=Decimal("200"),
    forms=(
        StateForm(
            "Certificate of authority",
            "Foreign corporation",
            "https://www.sos.mn.gov/business-liens/business-forms-fees/foreign-corporation-nonprofit-or-cooperative-forms/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Minn. Stat. § 303.20",
        "Court-recoverable penalty up to $1,000 plus up to $100 for each month or "
        "fraction of continued unauthorized business. Assessment is discretionary; do "
        "not assume the maximum or zero.",
    ),
    annual_obligations=(
        annual(
            "Annual renewal",
            "December 31, beginning the calendar year after authority is received.",
            "115",
            "Minn. Stat. §§ 303.14, 5.34; SOS fee schedule",
            "$135 online/in person.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Application attests compliance with home-jurisdiction organizational law; § "
        "303.06 does not prescribe a certificate attachment or numeric freshness "
        "limit."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Minn. Stat. Chapter 321; SOS foreign LP schedule",
    threshold=QualificationThreshold(
        citation="Minn. Stat. Chapter 321",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset(),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Certificate of authority",
            "Foreign LP",
            "https://www.sos.mn.gov/business-liens/business-filing-and-certification-fee-schedule/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Minn. Stat. Chapter 321", "LP sanctions require separate review."
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
    state="MN",
    name="Minnesota",
    registered_agent=RegisteredAgentRequirement(
        citation="Minn. Stat. §§ 322C.0802(5), 303.06(1)(3), 303.02(5)",
        notes=(
            "Maintain a consenting eligible agent and an actual in-state registered "
            "office for LLC/corporate filings; a PO box alone is insufficient. LP "
            "exceptions require separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source("Ch. 322C MN Statutes", "https://www.revisor.mn.gov/statutes/cite/322C/full"),
        source("Ch. 303 MN Statutes", "https://www.revisor.mn.gov/statutes/cite/303/full"),
        source(
            "Office of the State Of Minnesota Secretary of State",
            "https://www.sos.mn.gov/business-liens/business-filing-and-certification-fee-schedule/",
        ),
        source(
            "Office of the State Of Minnesota Secretary of State",
            "https://www.sos.mn.gov/business-liens/business-forms-fees/foreign-limited-liability-company-forms/",
        ),
        source(
            "Office of the State Of Minnesota Secretary of State",
            "https://www.sos.mn.gov/business-liens/business-forms-fees/foreign-corporation-nonprofit-or-cooperative-forms/",
        ),
        source("Sec. 5.34 MN Statutes", "https://www.revisor.mn.gov/statutes/cite/5.34"),
    ),
    version="2026-10-11-batch5",
    notes=(
        "Base fees shown are mail filings. LLC authority is $185 by mail or $205 "
        "online/in person; corporate authority is $200 by mail or $220 online/in "
        "person. Foreign corporate renewals cost $115 by mail or $135 online/in "
        "person; LLC renewals are free.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
