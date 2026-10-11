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
    qualification_citation="Wis. Stat. §§ 183.0902–183.0903",
    threshold=QualificationThreshold(
        citation="Wis. Stat. § 183.0905",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign limited liability company registration",
            "Form 521",
            "https://dfi.wi.gov/Documents/BusinessServices/BusinessEntities/Forms/CORP521.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Wis. Stat. § 183.0902(6)",
        "For each unauthorized year or part, fees/charges that would have applied "
        "plus 50% of that amount or $5,000, whichever is less; payment required "
        "before registration. Form 521 worksheet uses $97.50 per prior report "
        "calendar year ($65 plus 50%), in addition to $100 registration. Court access "
        "restricted; contracts, defense, property title and limited-liability "
        "protection remain valid. Fact-specific calculations require review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="January 1 through March 31, beginning the calendar year after registration.",
            fee=Decimal("65"),
            citation="Wis. Stat. §§ 183.0212, 183.0122",
            notes=(
                "Online $65; paper $80 including $15 surcharge. Domestic anniversary-quarter "
                "timing does not apply to foreign LLCs."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Section 183.0903 and current Form 521 do not require attachment of a "
        "home-jurisdiction good-standing certificate. Do not import the corporate "
        "certificate requirement."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Wis. Stat. §§ 180.1501, 180.1503",
    threshold=QualificationThreshold(
        citation="Wis. Stat. § 180.1501",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Form 21",
            "https://dfi.wi.gov/Documents/BusinessServices/BusinessEntities/Forms/CORP21.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Wis. Stat. § 180.1502(5)",
        "For each unauthorized year or part, all fees/charges that would have applied "
        "plus 50% of that amount or $5,000, whichever is less; pay before authority "
        "issues. Cannot maintain proceedings until authorized; acts, property title "
        "and defense remain valid. Capital and historical fees require manual "
        "calculation.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report (capital-dependent)",
            cycle="annual",
            due_rule="January 1 through March 31, beginning the calendar year after authorization.",
            fee=None,
            citation="Wis. Stat. §§ 180.1622, 180.0122",
            notes=(
                "Corporate filing minimum $100 plus $3 for each $1,000 or fraction of "
                "Wisconsin-represented capital above $60,000, under § 180.0122(1m)(u); capital "
                "is calculated using Form 21 and § 180.1503, with "
                "qualified-new-business-venture exceptions. Annual reports cost at least $65 "
                "online or $80 paper, plus capital-increase charges. Do not treat $100 "
                "registration or $65 annual filing as universal totals."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of status/existence authenticated and dated no "
        "earlier than 60 days before delivery, under § 180.1503(2) and Form 21; "
        "certified articles are not a substitute."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Wisconsin DFI fee schedule: foreign limited partnership registration",
    threshold=QualificationThreshold(
        citation="Wisconsin DFI fee schedule: foreign limited partnership registration",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("75"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://dfi.wi.gov/Pages/BusinessServices/BusinessEntities/Fees.aspx",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Wisconsin DFI fee schedule: foreign limited partnership registration",
        "LP sanctions require separate review.",
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
    state="WI",
    name="Wisconsin",
    registered_agent=RegisteredAgentRequirement(
        citation="Wis. Stat. §§ 183.0115, 180.1507",
        notes=(
            "Maintain an eligible Wisconsin resident or authorized business entity as "
            "registered agent and an actual Wisconsin street-address registered office. A "
            "PO box, mailbox service or answering service alone is not an office. An "
            "outside commercial provider is not mandatory."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Wisconsin statutory/filing guidance",
            "https://docs.legis.wisconsin.gov/statutes/statutes/183.pdf",
        ),
        source(
            "Wisconsin statutory/filing guidance",
            "https://docs.legis.wisconsin.gov/statutes/statutes/180.pdf",
        ),
        source(
            "DFI\n            \n            \n            Corporation Fees",
            "https://dfi.wi.gov/Pages/BusinessServices/BusinessEntities/Fees.aspx",
        ),
        source(
            "Foreign Registration Statement",
            "https://dfi.wi.gov/Documents/BusinessServices/BusinessEntities/Forms/CORP521.pdf",
        ),
        source(
            "Certificate of Authority Application",
            "https://dfi.wi.gov/Documents/BusinessServices/BusinessEntities/Forms/CORP21.pdf",
        ),
    ),
    version="2026-10-11-batch9",
    notes=(
        "Foreign LLC registration $100; annual report $65 online or $80 paper "
        "including the $15 surcharge. Foreign reports for both entity types are due "
        "in the first calendar quarter, not the domestic anniversary quarter.",
        "Corporate filing minimum $100 plus $3 for each $1,000 or fraction of "
        "Wisconsin-represented capital above $60,000, under § 180.0122(1m)(u); capital "
        "is calculated using Form 21 and § 180.1503, with "
        "qualified-new-business-venture exceptions. Annual reports cost at least $65 "
        "online or $80 paper, plus capital-increase charges. Do not treat $100 "
        "registration or $65 annual filing as universal totals.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
