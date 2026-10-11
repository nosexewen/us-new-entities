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
    qualification_citation="Miss. Code § 79-29-1003",
    threshold=QualificationThreshold(
        citation="Miss. Code § 79-29-1015",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Application for registration",
            "F0200",
            "https://corp.sos.ms.gov/corp/portal/c/portal.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Miss. Code § 79-29-1203(1)(g)",
        "$10 for each day of unauthorized business, capped at $1,000 for each year, "
        "in addition to the $250 registration fee. Allocate covered days and yearly "
        "caps manually; reporting arrears are separate.",
    ),
    annual_obligations=(
        annual(
            "Annual report",
            "January 1 through April 15 each year.",
            "250",
            "Miss. Code § 79-29-1203; Mississippi SOS annual reports",
            "",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated certificate of existence or similar document from the "
        "home-jurisdiction official is required by § 79-29-1003(2); no numeric "
        "freshness limit is supplied in that section."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Miss. Code § 79-4-15.01",
    threshold=QualificationThreshold(
        citation="Miss. Code § 79-4-15.01(b)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("500"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "F0002",
            "https://corp.sos.ms.gov/corp/portal/c/portal.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Miss. Code § 79-4-15.02(d)",
        "$10 for each day of unauthorized business, capped at $1,000 for each year. "
        "Attorney-general collection and fact-specific yearly allocation require "
        "manual assessment.",
    ),
    annual_obligations=(
        annual(
            "Annual report",
            "January 1 through April 15 each year.",
            "25",
            "Miss. Code § 79-4-1.22; Mississippi SOS annual reports",
            "",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated certificate of existence or similar document from the "
        "home-jurisdiction official is required by § 79-4-15.03(b); no numeric "
        "freshness limit is supplied in that section."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Mississippi SOS foreign LP filing schedule",
    threshold=QualificationThreshold(
        citation="Mississippi SOS foreign LP filing schedule",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset(),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Application for registration",
            "F0300",
            "https://corp.sos.ms.gov/corp/portal/c/portal.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Mississippi foreign LP law", "LP sanctions require separate review."
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
    state="MS",
    name="Mississippi",
    registered_agent=RegisteredAgentRequirement(
        citation="Miss. Code §§ 79-29-1003(1)(c), 79-4-15.03(a)(5); §§ 79-35-4, 79-35-5",
        notes=(
            "Maintain a consenting eligible agent and an actual in-state registered "
            "office for LLC/corporate filings; a PO box alone is insufficient. LP "
            "exceptions require separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Miss. Code § 79-35-4 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-35/section-79-35-4",
        ),
        source(
            "Miss. Code § 79-35-5 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-35/section-79-35-5",
        ),
        source(
            "Miss. Code § 79-29-1013 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-29/article-10/section-79-29-1013",
        ),
        source(
            "Miss. Code § 79-35-13 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-35/section-79-35-13",
        ),
        source(
            "Mississippi SOS business filing fee schedule",
            "https://www.sos.ms.gov/content/documents/Business/FeeSchedule.pdf",
        ),
        source(
            "Annual Reports | MS SOS", "https://www.sos.ms.gov/business-services/annual-reports"
        ),
        source(
            "Miss. Code § 79-4-15.01 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-4/article-15/subarticle-a/section-79-4-15-01",
        ),
        source(
            "Miss. Code § 79-4-15.02 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-4/article-15/subarticle-a/section-79-4-15-02",
        ),
        source(
            "Miss. Code § 79-29-1015 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-29/article-10/section-79-29-1015",
        ),
        source(
            "Miss. Code § 79-29-1003 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-29/article-10/section-79-29-1003",
        ),
        source(
            "Miss. Code § 79-29-1203 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-29/article-12/section-79-29-1203",
        ),
        source(
            "Miss. Code § 79-4-15.03 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-4/article-15/subarticle-a/section-79-4-15-03",
        ),
        source(
            "Miss. Code § 79-4-1.22 (Justia 2025)",
            "https://law.justia.com/codes/mississippi/title-79/chapter-4/article-1/subarticle-b/section-79-4-1-22",
        ),
    ),
    version="2026-10-11-accepted-statutory-review",
    notes=(
        "Foreign LLC registration and annual reports each cost $250; foreign "
        "for-profit corporate authority costs $500 and annual reports cost $25. "
        "Annual reports must be filed online through the SOS portal. Taxes and "
        "business licenses are separate.",
    ),
    verification_issues=(),
    review_disclosures=(
        "Review acceptance: at the user's direction, the reviewed Justia 2025 "
        "statutory citations are sufficient verification for Mississippi statutory "
        "rules. The primary review flag is satisfied. Justia remains identified as "
        "a third-party statutory reproduction; official SOS guidance corroborates "
        "filing fees and annual reporting. The historical 2010 SOS LLC PDF remains "
        "excluded as current authority.",
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
