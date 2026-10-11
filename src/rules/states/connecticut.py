"""Connecticut rules reviewed against official statutes and filing guidance."""

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
    qualification_citation="Conn. Gen. Stat. §§ 34-275a–34-275b",
    threshold=QualificationThreshold(
        citation="Conn. Gen. Stat. § 34-275d",
        isolated_transaction_without_day_limit=True,
        notes=(
            "Isolated transactions must not be in the course of similar transactions; no "
            "fixed day limit. Orders must be accepted outside Connecticut. Separate tax "
            "and regulatory nexus tests apply."
        ),
    ),
    filing_fee=Decimal("120"),
    forms=(
        StateForm(
            "Foreign registration certificate",
            "Foreign LLC",
            "https://business.ct.gov/knowledge-base/articles/foreign-limited-liability-companies-forms-and-fees",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Conn. Gen. Stat. § 34-275a(g)–(h)",
        (
            "$300 for each month or part-month without authority, plus historical fees, "
            "taxes, interest and penalties. The monthly penalty does not apply if "
            "registration is obtained within 90 days after commencing business. The exemption "
            "does not excuse registration or historical charges. The Attorney General may "
            "recover assessed amounts and seek an injunction; assessment remains manual."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="January 1 through March 31, starting the year after registration.",
            fee=Decimal("80"),
            citation="Conn. Gen. Stat. §§ 34-247k, 34-243u(a)(15)",
            notes="",
        ),
    ),
    consequences=(
        (
            "Failure to qualify does not invalidate contracts or prevent defending "
            "proceedings; maintaining an action requires qualification."
        ),
    ),
    good_standing_evidence=(
        "Attach a duly authenticated certificate of existence or similar "
        "home-jurisdiction document. The reviewed statutes impose no numeric certificate "
        "age limit; confirm current filing instructions."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Conn. Gen. Stat. §§ 33-920, 33-922",
    threshold=QualificationThreshold(
        citation="Conn. Gen. Stat. § 33-920(b)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions."
        ),
    ),
    filing_fee=Decimal("385"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign stock corporation",
            "https://business.ct.gov/knowledge-base/articles/foreign-stock-corporations-forms-and-fees",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Conn. Gen. Stat. § 33-921(d)",
        (
            "$300 for each month or part-month without authority, plus historical fees, "
            "taxes, interest and penalties. The monthly penalty does not apply if "
            "registration is obtained within 90 days after commencing business. The exemption "
            "does not excuse registration or historical charges. The Attorney General may "
            "recover assessed amounts and seek an injunction; assessment remains manual."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Annual reports recur on the anniversary of the first annual report; confirm the "
                "assigned due date in the state record. The separate $285 license fee is due by "
                "the last day of the authority anniversary month."
            ),
            fee=Decimal("435"),
            citation="Conn. Gen. Stat. §§ 33-953, 33-617(a)(12), (d)",
            notes=(
                "$150 annual report plus $285 annual license fee. These components can have "
                "different deadlines."
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
        "Attach a duly authenticated certificate of existence or similar "
        "home-jurisdiction document. The reviewed statutes impose no numeric certificate "
        "age limit; confirm current filing instructions."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Connecticut SOS fee schedule, foreign LP registration (Chapter 610)",
    threshold=QualificationThreshold(
        citation="Chapter 610 activity screening requires manual statutory review",
        exempt_activities=frozenset(),
        notes=(
            "Only the official $120 LP registration fee is populated; no LLC or corporate "
            "safe harbor is applied to LPs."
        ),
    ),
    filing_fee=Decimal("120"),
    forms=(
        StateForm(
            "Certificate of registration of a foreign limited partnership",
            "Foreign LP",
            "https://business.ct.gov/-/media/businessonestop/fee-schedule-revised-712020.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Chapter 610 sanctions require manual review",
        (
            "LP penalties, exemptions and reporting applicability are outside this LLC/C-Corp "
            "statutory review; obtain an entity-specific assessment."
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
    state="CT",
    name="Connecticut",
    registered_agent=RegisteredAgentRequirement(
        citation="Conn. Gen. Stat. §§ 34-243n, 33-926",
        notes=(
            "Designate a consenting eligible Connecticut agent and address for service. A "
            "foreign LLC may designate the Secretary of the State under § 34-243n(c)(1); a "
            "private agent is not mandatory when that option is used. Corporate agents must "
            "satisfy § 33-926."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source("Uniform LLC Act, Chapter 613a", "https://www.cga.ct.gov/current/pub/chap_613a.htm"),
        source(
            "Business Corporation Act, Chapter 601",
            "https://www.cga.ct.gov/current/pub/chap_601.htm",
        ),
        source(
            "SOS business fee schedule",
            "https://business.ct.gov/-/media/businessonestop/fee-schedule-revised-712020.pdf",
        ),
        source(
            "SOS foreign annual reports and fees",
            "https://business.ct.gov/knowledge-base/articles/foreign-annual-report-forms-and-fees",
        ),
        source(
            "SOS foreign stock corporation forms and fees",
            "https://business.ct.gov/knowledge-base/articles/foreign-stock-corporations-forms-and-fees",
        ),
        source(
            "SOS foreign LLC forms and fees",
            "https://business.ct.gov/knowledge-base/articles/foreign-limited-liability-companies-forms-and-fees",
        ),
    ),
    version="2026-10-11-batch3",
    notes=(
        (
            "Corporate qualification is $100 filing plus $285 license fee, totaling $385. "
            "The recurring foreign corporation charge is $150 report plus $285 license "
            "fee, totaling $435; license renewal is due by the last day of the "
            "authorization anniversary month. LLC reports are $80. Optional expedite, "
            "certificate, agent-service fees and taxes are separate."
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
