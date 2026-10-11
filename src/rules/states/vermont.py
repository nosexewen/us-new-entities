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
    qualification_citation="11 V.S.A. §§ 4112–4113",
    threshold=QualificationThreshold(
        citation="11 V.S.A. § 4113",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("155"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LLC",
            "https://sos.vermont.gov/business-services/business-filings/foreign-registration",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "11 V.S.A. §§ 4119–4120",
        "Cannot maintain affirmative proceedings, counterclaims, crossclaims or "
        "affirmative defenses until qualified; ordinary defense and contracts remain "
        "valid. Civil penalty $50 per day, capped at $10,000 per year, plus "
        "fees and other applicable sanctions; Attorney General injunction possible. "
        "Fact-specific periods require manual calculation.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Within three months after fiscal year end; March 31 for a calendar fiscal year."
            ),
            fee=Decimal("170"),
            citation="11 V.S.A. §§ 4033, 4012",
            notes="Foreign LLC fee $170; domestic $45 fee does not apply.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence issued within 90 days before "
        "filing, under § 4112 and SOS instructions."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="11A V.S.A. §§ 15.01, 15.03",
    threshold=QualificationThreshold(
        citation="11A V.S.A. § 15.01",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("155"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign profit corporation",
            "https://sos.vermont.gov/business-services/business-filings/foreign-registration",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "11A V.S.A. § 15.02",
        "Cannot maintain affirmative proceedings, counterclaims, crossclaims or "
        "affirmative defenses until qualified; ordinary defense and contracts remain "
        "valid. Civil penalty $50 per day, capped at $10,000 per year, plus "
        "fees and other sanctions; injunction possible. Fact-specific periods require "
        "manual calculation.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Within two and one-half months after fiscal year end; March 15 for a "
                "calendar fiscal year."
            ),
            fee=Decimal("250"),
            citation="11A V.S.A. §§ 16.22, 1.22",
            notes="Foreign profit corporation fee $250; domestic $60 fee does not apply.",
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence dated within 30 days before "
        "filing, per SOS foreign registration instructions."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Vermont SOS fee schedule: foreign limited partnership registration",
    threshold=QualificationThreshold(
        citation="Vermont SOS fee schedule: foreign limited partnership registration",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("155"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://sos.vermont.gov/business-services/fees-statutes/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Vermont SOS fee schedule: foreign limited partnership registration",
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
    state="VT",
    name="Vermont",
    registered_agent=RegisteredAgentRequirement(
        citation="11 V.S.A. §§ 4007, 1655; 11A V.S.A. § 15.07",
        notes=(
            "Maintain a consenting individual Vermont resident or an authorized business "
            "organization with a place of business in Vermont; provide current name, "
            "email and address information under § 1655. An outside commercial provider "
            "is not mandatory. The LLC designated notification office may be outside "
            "Vermont, distinct from the in-state service agent."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source("Vermont Laws", "https://legislature.vermont.gov/statutes/fullchapter/11/025"),
        source("Vermont Laws", "https://legislature.vermont.gov/statutes/fullchapter/11A/015"),
        source("Vermont Laws", "https://legislature.vermont.gov/statutes/fullchapter/11a/001"),
        source("Vermont Laws", "https://legislature.vermont.gov/statutes/fullchapter/11a/016"),
        source(
            "11 V.S.A. § 1655. Designation of agent for service of process; change; resignation",
            "https://legislature.vermont.gov/statutes/section/11/015/01655",
        ),
        source(
            "Foreign Registration | Secretary of State",
            "https://sos.vermont.gov/business-services/business-filings/foreign-registration",
        ),
        source(
            "Annual/Biennial Reports | Secretary of State",
            "https://sos.vermont.gov/business-services/business-filings/annualbiennial-reports",
        ),
        source(
            "Fees | Secretary of State", "https://sos.vermont.gov/business-services/fees-statutes/"
        ),
    ),
    version="2026-10-11-batch9",
    notes=(
        "Foreign LLC and profit corporation registration each costs $155. Foreign LLC "
        "annual reports cost $170; foreign profit corporation reports cost $250. "
        "Domestic $45 LLC and $60 corporation report fees do not apply to these "
        "foreign guides.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
