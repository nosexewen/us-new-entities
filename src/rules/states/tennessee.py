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
    qualification_citation="Tenn. Code Ann. § 48-249-904",
    threshold=QualificationThreshold(
        citation="Tenn. Code Ann. § 48-249-902",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "The statute uses one calendar month, not 30 days, for nonrepeated isolated "
            "transactions. The day-count screening model leaves this exemption for manual "
            "review. Solicitation requires out-of-state acceptance. Qualification "
            "exemptions do not determine tax, licensing or service-of-process nexus. "
            "Initial registration $50 per member, minimum $300 and maximum $3,000."
        ),
    ),
    filing_fee=Decimal("300"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "SS-4233",
            "https://sos-prod.tnsosgovfiles.com/s3fs-public/document/SS-4233%20COA%20LLC_0.pdf?VersionId=Yf5Pmfnf25fLEne_HGVwXUhIaVXBp5Rk",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Tenn. Code Ann. § 48-249-913",
        "Fine is three times the otherwise required filing fee for each year or part "
        "of a year without authority; amounts must be paid before the application is "
        "filed. Member count and elapsed years require manual calculation. Court "
        "access is restricted; contracts, defenses and limited liability remain "
        "valid.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "First day of the fourth month after fiscal-year end (April 1 for a calendar "
                "year), or a date set by SOS rule."
            ),
            fee=None,
            citation="Tenn. Code Ann. § 48-249-1017; Tennessee SOS annual report FAQ",
            notes=(
                "Member-based fee: $50 per member, minimum $300 and maximum $3,000. $300 is "
                "not a universal fee; registered-agent/office changes add $20."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated certificate of existence/good standing from the home filing "
        "office dated no more than two calendar months before filing, per SS-4233; do "
        "not convert months to a fixed 60-day limit. SS-4233 also requires a "
        "Tennessee Department of Revenue Letter of Good Standing if the disclosed "
        "start date precedes application approval by more than one year."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Tenn. Code Ann. § 48-25-101",
    threshold=QualificationThreshold(
        citation="Tenn. Code Ann. § 48-25-101(b)",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "The statute uses one calendar month, not 30 days, for nonrepeated isolated "
            "transactions. The day-count screening model leaves this exemption for manual "
            "review. Solicitation requires out-of-state acceptance. Qualification "
            "exemptions do not determine tax, licensing or service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("600"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "SS-4431",
            "https://sos-prod.tnsosgovfiles.com/s3fs-public/document/SS-4431%20COA%20For-Profit%20Corp_1.pdf?VersionId=50ixhNNBGfPZ8WuH.wOllqvpUYt0SniC",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Tenn. Code Ann. § 48-25-102",
        "Liability equals treble fees, penalties and taxes plus interest for years or "
        "parts of years of unauthorized business; payment is required before filing "
        "authority. Court access is restricted; corporate acts and defenses remain "
        "valid. Do not reduce this formula to three times the $600 filing fee.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "First day of the fourth month after fiscal-year end (April 1 for a calendar "
                "year), or a date set by SOS rule."
            ),
            fee=Decimal("20"),
            citation="Tenn. Code Ann. § 48-26-203; Tennessee SOS annual report FAQ",
            notes="Registered-agent/office changes add $20; franchise/excise taxes are separate.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated home-jurisdiction certificate of existence/good standing dated "
        "no more than two calendar months before filing, per SS-4431. The form also "
        "requires a Tennessee Department of Revenue Letter of Good Standing when the "
        "disclosed start date precedes approval by more than one year."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Tennessee SOS foreign LP registration fee",
    threshold=QualificationThreshold(
        citation="Tennessee SOS foreign LP registration fee",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("600"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://sos.tn.gov/businesses/services/business-forms-fees",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Tennessee SOS foreign LP registration fee", "LP sanctions require separate review."
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
    state="TN",
    name="Tennessee",
    registered_agent=RegisteredAgentRequirement(
        citation="Tenn. Code Ann. §§ 48-249-109, 48-25-107",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Tennessee Code § 48-249-904 (2025) - Application for certificate of "
            "authority :: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. Law :: "
            "Justia",
            "https://law.justia.com/codes/tennessee/title-48/limited-liability-companies/chapter-249/part-9/section-48-249-904/",
        ),
        source(
            "Tennessee Code § 48-249-902 (2025) - Transactions not constituting "
            "transacting business :: 2025 Tennessee Code :: U.S. Codes and Statutes :: "
            "U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/limited-liability-companies/chapter-249/part-9/section-48-249-902/",
        ),
        source(
            "Tennessee Code § 48-249-913 (2025) - Transaction of business without "
            "certificate of authority :: 2025 Tennessee Code :: U.S. Codes and Statutes "
            ":: U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/limited-liability-companies/chapter-249/part-9/section-48-249-913/",
        ),
        source(
            "Tennessee Code § 48-25-101 (2025) - Authority to transact business required "
            ":: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/for-profit-business-corporations/chapter-25/part-1/section-48-25-101/",
        ),
        source(
            "Tennessee Code § 48-25-102 (2025) - Consequences of transacting business "
            "without authority :: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. "
            "Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/for-profit-business-corporations/chapter-25/part-1/section-48-25-102/",
        ),
        source(
            "Tennessee Code § 48-249-1017 (2025) - Annual report for secretary of state "
            ":: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/limited-liability-companies/chapter-249/part-10/section-48-249-1017/",
        ),
        source(
            "Tennessee Code § 48-26-203 (2025) - Filing annual report with secretary of "
            "state :: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. Law :: "
            "Justia",
            "https://law.justia.com/codes/tennessee/title-48/for-profit-business-corporations/chapter-26/part-2/section-48-26-203/",
        ),
        source(
            "Tennessee Code § 48-249-109 (2025) - Registered office and registered agent "
            ":: 2025 Tennessee Code :: U.S. Codes and Statutes :: U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/limited-liability-companies/chapter-249/part-1/section-48-249-109/",
        ),
        source(
            "Tennessee Code § 48-25-107 (2025) - Registered office and registered agent "
            "of foreign corporation :: 2025 Tennessee Code :: U.S. Codes and Statutes :: "
            "U.S. Law :: Justia",
            "https://law.justia.com/codes/tennessee/title-48/for-profit-business-corporations/chapter-25/part-1/section-48-25-107/",
        ),
        source(
            "Business Forms & Fees | Tennessee Secretary of State",
            "https://sos.tn.gov/businesses/services/business-forms-fees",
        ),
        source(
            "All Frequently Asked Questions for Businesses | Tennessee Secretary of State",
            "https://sos.tn.gov/businesses/faqs",
        ),
        source(
            "Tennessee statutory/filing guidance",
            "https://sos-prod.tnsosgovfiles.com/s3fs-public/document/SS-4233%20COA%20LLC_0.pdf?VersionId=Yf5Pmfnf25fLEne_HGVwXUhIaVXBp5Rk",
        ),
        source(
            "Tennessee statutory/filing guidance",
            "https://sos-prod.tnsosgovfiles.com/s3fs-public/document/SS-4431%20COA%20For-Profit%20Corp_1.pdf?VersionId=50ixhNNBGfPZ8WuH.wOllqvpUYt0SniC",
        ),
        source(
            "Create an Account in TNCaB to File an Annual Report | Tennessee Secretary of State",
            "https://sos.tn.gov/businesses/pages/create-an-account-in-tncab-to-file-an-annual-report",
        ),
    ),
    version="2026-10-11-batch8",
    notes=(
        "Foreign LLC registration is $50 per member existing at filing, minimum $300 "
        "and maximum $3,000. Annual LLC reports use the member-based $300–$3,000 "
        "schedule. Foreign for-profit corporate authority is $600 and annual reports "
        "$20; registered-agent/office changes add $20. Calendar-year reports are "
        "ordinarily due April 1. Franchise/excise taxes, exemptions, professional "
        "entities and obligated-member elections require separate tax review. These "
        "LLC rules cover the Revised LLC Act; legacy entities governed by the older "
        "Act require entity-specific review.",
    ),
    verification_issues=(
        "Primary statutory review remains open: Tennessee Code text was reviewed "
        "through the 2025 Justia compilation, with current SOS forms and fees as "
        "official operational evidence. Independent mirror citations have not been "
        "accepted as primary verification for Tennessee.",
    ),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "Both LLC and corporate isolated-transaction exemptions use one calendar "
        "month, not a fixed 30-day limit. The day-only model conservatively requires "
        "manual review for this activity rather than invent a conversion.",
    ),
)
