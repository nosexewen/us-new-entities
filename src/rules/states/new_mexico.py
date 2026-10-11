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
    qualification_citation="NMSA 1978 § 53-19-48",
    threshold=QualificationThreshold(
        citation="NMSA 1978 § 53-19-54",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Under NMSA 1978 Chapter 53, Article 19, "
            "New Mexico LLCs have no periodic or annual report requirement and the "
            "periodic-report fee is $0. Domestic LLC formation is a one-time $50 "
            "filing under § 53-19-63(A); foreign LLC registration remains $100 under "
            "§ 53-19-63(K). Separate tax and licensing obligations may apply."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(StateForm("Foreign LLC registration", "Foreign LLC", "https://enterprise.sos.nm.gov/"),),
    qualification_penalty=unresolved_penalty(
        "NMSA 1978 § 53-19-53",
        "Fees and penalties for the unauthorized period plus a civil penalty up to "
        "$200 for each year or part, with interest and costs as applicable; "
        "attorney-general injunctions are possible. Do not assume the maximum is "
        "automatically assessed.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of good standing/compliance current within 30 "
        "days and not expired when received under § 53-19-48; submit the registered "
        "agent's signed acceptance."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="NMSA 1978 § 53-17-1",
    threshold=QualificationThreshold(
        citation="NMSA 1978 § 53-17-1",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("200"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign corporation",
            "https://enterprise.sos.nm.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NMSA 1978 § 53-17-20",
        "Civil penalty of $200 for each offense, plus fees, franchise taxes and "
        "penalties for the unauthorized period. Determine offenses and arrears "
        "manually; do not apply the LLC annual penalty formula.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Biennial corporate report",
            cycle="biennial",
            due_rule=(
                "Fifteenth day of the fourth month after the end of the tax year, in the "
                "applicable biennial reporting year."
            ),
            fee=Decimal("25"),
            citation="NMSA 1978 §§ 53-5-2, 53-2-1(A)(16)",
            notes=(
                "Tax-year-based reporting; do not substitute an annual "
                "registration-anniversary deadline."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing certificate current within 30 days and not "
        "expired when received; written acceptance by the registered agent under § "
        "53-17-6."
    ),
    initial_report=(
        "File the initial corporate report within 30 days after the certificate of "
        "authority is issued under NMSA 1978 § 53-5-2."
    ),
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="NMSA 1978 § 54-2A-210(A)(2)",
    threshold=QualificationThreshold(
        citation="NMSA 1978 § 54-2A-210(A)(2)",
        isolated_transaction_max_days=None,
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
            "Application for certificate of authority",
            "Foreign LP",
            "https://law.justia.com/codes/new-mexico/chapter-54/article-2a/article-2/section-54-2a-210/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "NMSA 1978 § 54-2A-210(A)(2)", "LP sanctions require separate review."
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
    state="NM",
    name="New Mexico",
    registered_agent=RegisteredAgentRequirement(
        citation="NMSA 1978 §§ 53-19-5, 53-19-48, 53-17-6",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "New Mexico Statutes Section 53-19-48 (2025) - Registration. :: 2025 New "
            "Mexico Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-19/section-53-19-48",
        ),
        source(
            "New Mexico Statutes Section 53-19-54 (2025) - Transactions not constituting "
            "transacting business. :: 2025 New Mexico Statutes :: U.S. Codes and Statutes "
            ":: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-19/section-53-19-54",
        ),
        source(
            "New Mexico Statutes Section 53-19-53 (2025) - Transaction of business "
            "without registration. :: 2025 New Mexico Statutes :: U.S. Codes and Statutes "
            ":: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-19/section-53-19-53",
        ),
        source(
            "New Mexico Statutes Section 53-19-63 (2025) - Filing, service and copying "
            "fees. :: 2025 New Mexico Statutes :: U.S. Codes and Statutes :: U.S. Law :: "
            "Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-19/section-53-19-63",
        ),
        source(
            "New Mexico Statutes Section 53-19-5 (2025) - Registered office and "
            "registered agent; change of principal place of business. :: 2025 New Mexico "
            "Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-19/section-53-19-5",
        ),
        source(
            "New Mexico Statutes Section 53-17-1 (2025) - Admission of foreign "
            "corporation. :: 2025 New Mexico Statutes :: U.S. Codes and Statutes :: U.S. "
            "Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-17/section-53-17-1",
        ),
        source(
            "New Mexico Statutes Section 53-17-20 (2025) - Transacting business without "
            "certificate of authority. :: 2025 New Mexico Statutes :: U.S. Codes and "
            "Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-17/section-53-17-20",
        ),
        source(
            "New Mexico Statutes Section 53-2-1 (2025) - Fees of secretary of state. :: "
            "2025 New Mexico Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-2/section-53-2-1/",
        ),
        source(
            "New Mexico Statutes Section 53-5-2 (2025) - Corporate and supplemental "
            "reports. :: 2025 New Mexico Statutes :: U.S. Codes and Statutes :: U.S. Law "
            ":: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-5/section-53-5-2",
        ),
        source(
            "New Mexico Statutes Section 53-17-6 (2025) - Filing of application for "
            "certificate of authority. :: 2025 New Mexico Statutes :: U.S. Codes and "
            "Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-53/article-17/section-53-17-6",
        ),
        source(
            "New Mexico Statutes Section 54-2A-210 (2025) - Secretary of state fees. :: "
            "2025 New Mexico Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/new-mexico/chapter-54/article-2a/article-2/section-54-2a-210/",
        ),
        source(
            "Business Services | Maggie Toulouse Oliver - New Mexico Secretary of State",
            "https://www.sos.nm.gov/business-services/",
        ),
    ),
    version="2026-10-11-batch6",
    notes=(
        "LLC foreign registration has a $100 statutory base fee. Corporate "
        "qualification is $1 per 1,000 authorized shares represented in New Mexico, "
        "at least $200 and at most $1,000; $200 is a minimum, not a flat fee. Confirm "
        "the actual portal total and processing charges. SOS states that business "
        "filings are now online.",
    ),
    verification_issues=(
        "Current payable portal totals and any payment-processing fees remain "
        "unverified; published amounts are statutory base fees.",
    ),
    review_disclosures=(
        "At the user's direction on 2026-10-11, the cited Justia statutory "
        "reproductions are accepted as sufficient verification for New Mexico. "
        "The primary review flag is satisfied by that acceptance; Justia remains "
        "a secondary publisher, and NM OneSource was not independently retrieved.",
        "LLCs have no periodic or annual report requirement under NMSA 1978 "
        "Chapter 53, Article 19 ($0 periodic-report fee). The one-time domestic "
        "formation filing is $50 under § 53-19-63(A); foreign registration is "
        "$100 under § 53-19-63(K). The corporate biennial report does not apply "
        "to LLCs. The reporting limitation is resolved at the user's direction.",
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
