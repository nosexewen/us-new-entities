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
    qualification_citation="Utah Code §§ 16-1a-503, 16-1a-504",
    threshold=QualificationThreshold(
        citation="Utah Code § 16-1a-506",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Effective October 1, 2026, § 16-1a-506 exempts an isolated transaction "
            "outside the entity’s ordinary course of business without a fixed day cap. "
            "Ordinary-course facts are not represented in the screening model, so "
            "isolated transactions require manual review; do not infer an automatic "
            "30-day or unlimited exemption. Solicitation requires out-of-state "
            "acceptance. Qualification exemptions do not determine tax or regulatory "
            "nexus."
        ),
    ),
    filing_fee=Decimal("59"),
    forms=(
        StateForm(
            "Foreign registration statement",
            "Foreign LLC",
            "https://businessregistration.utah.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Utah Code § 16-1a-503",
        "Cannot maintain proceedings until registered; contracts, defenses and "
        "limited-liability protections remain valid. This provision supplies no fixed "
        "monetary qualification fine; other sanctions require separate review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report / renewal",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month (month Utah authority takes effect), "
                "unless the division specifies another period by rule; filing may begin 60 "
                "days earlier."
            ),
            fee=Decimal("18"),
            citation="Utah Code § 16-1a-212; Utah Division fee schedule",
            notes=(
                "The $18 agency fee includes the $5 portal surcharge; do not add it twice. "
                "Late renewal fee is $10."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence or similar authorized document "
        "dated within 90 days before delivery of the registration statement, required "
        "by § 16-1a-504(3), effective October 1, 2026."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Utah Code §§ 16-1a-503, 16-1a-504",
    threshold=QualificationThreshold(
        citation="Utah Code § 16-1a-506",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Effective October 1, 2026, § 16-1a-506 exempts an isolated transaction "
            "outside the entity’s ordinary course of business without a fixed day cap. "
            "Ordinary-course facts are not represented in the screening model, so "
            "isolated transactions require manual review; do not infer an automatic "
            "30-day or unlimited exemption. Solicitation requires out-of-state "
            "acceptance. Qualification exemptions do not determine tax or regulatory "
            "nexus."
        ),
    ),
    filing_fee=Decimal("59"),
    forms=(
        StateForm(
            "Foreign registration statement",
            "Foreign business corporation",
            "https://businessregistration.utah.gov/",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Utah Code § 16-1a-503",
        "Cannot maintain proceedings until registered; contracts and defenses remain "
        "valid, with the limited-liability protections specified in subsection (4). "
        "This provision supplies no fixed monetary qualification fine; other "
        "sanctions require separate review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report / renewal",
            cycle="annual",
            due_rule=(
                "Last day of the anniversary month (month Utah authority takes effect), "
                "unless the division specifies another period by rule; filing may begin 60 "
                "days earlier."
            ),
            fee=Decimal("18"),
            citation="Utah Code § 16-1a-212; Utah Division fee schedule",
            notes=(
                "The $18 agency fee includes the $5 portal surcharge; do not add it twice. "
                "Late renewal fee is $10."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence or similar authorized document "
        "dated within 90 days before delivery of the registration statement under § "
        "16-1a-504(3), effective October 1, 2026."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Utah Division foreign LP fee schedule; Utah Code § 16-1a-504",
    threshold=QualificationThreshold(
        citation="Utah Division foreign LP fee schedule; Utah Code § 16-1a-504",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("70"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://commerce.utah.gov/wp-content/uploads/2023/04/currentfees.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Utah Division foreign LP fee schedule; Utah Code § 16-1a-504",
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
    state="UT",
    name="Utah",
    registered_agent=RegisteredAgentRequirement(
        citation="Utah Code §§ 16-1a-403, 16-1a-404",
        notes=(
            "Effective October 1, 2026, the shared chapter permits a consenting "
            "commercial/noncommercial agent or an office/position designation under § "
            "16-1a-404. In-state street and separate mailing addresses are governed by § "
            "16-1a-403; a PO box alone is insufficient. An outside vendor is not "
            "mandatory. LP scope below remains limited."
        ),
        private_appointment_required=True,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Utah Code Section 16-1a-503",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S503.html",
        ),
        source(
            "Utah Code Section 16-1a-504",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S504.html",
        ),
        source(
            "Utah Code Section 16-1a-506",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S506.html",
        ),
        source(
            "Utah Code Section 16-1a-212",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S212.html",
        ),
        source(
            "Utah Code Section 16-1a-403",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S403.html",
        ),
        source(
            "Utah Code Section 16-1a-404",
            "https://le.utah.gov/xcode/Title16/Chapter1A/16-1a-S404.html",
        ),
        source(
            "Updated Fee Schedule July 1, 2025 - Google Docs",
            "https://commerce.utah.gov/wp-content/uploads/2023/04/currentfees.pdf",
        ),
        source(
            "CORP Foreign Limited Liability Company - commerce.utah.gov",
            "https://commerce.utah.gov/corporations/business-entities/foreign-limited-liability-company/",
        ),
        source(
            "CORP Foreign Profit Corporation - commerce.utah.gov",
            "https://commerce.utah.gov/corporations/business-entities/foreign-profit-corporation/",
        ),
        source(
            "Utah statutory/filing guidance",
            "https://le.utah.gov/lrgc/Recodification/2026/Title48RecodificationCrosswalk.pdf",
        ),
    ),
    version="2026-10-11-batch8",
    notes=(
        "Effective October 1, 2026, Title 16 Chapter 1a supplies shared foreign "
        "registration, exemptions, certificate evidence, agent and annual-report "
        "provisions for LLCs and corporations. Former § 48-3a-902 is repealed; older "
        "no-certificate LLC guidance is not used. Registration is $59 and annual "
        "renewal/report $18 for both requested types under the current agency "
        "schedule; the starred $18 fee already includes a $5 Utah single-sign-on "
        "surcharge. Late renewal fee is $10. Fees, rather than a user-invented total, "
        "follow the cited agency schedule.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
        "The official provisions retrieved are expressly effective October 1, 2026. § "
        "16-1a-504 requires a home certificate dated within 90 days for both entity "
        "types. § 16-1a-506(l) imposes an outside-ordinary-course "
        "isolated-transaction condition and no day cap; the model leaves that "
        "fact-sensitive exemption for manual review.",
    ),
)
