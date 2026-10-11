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
from ._shared import source, unresolved_penalty

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="Ohio Rev. Code § 1706.511",
    threshold=QualificationThreshold(
        citation="Ohio Rev. Code § 1706.512",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "The isolated-transaction exemption requires a transaction outside a course "
            "of repeated similar transactions; the statute imposes no fixed day limit. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("99"),
    forms=(
        StateForm(
            "Registration of a foreign limited liability company",
            "Form 617",
            "https://www.ohiosos.gov/assets/617.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Ohio Rev. Code § 1706.515",
        "Debt-collection proceedings are restricted until effective registration. "
        "Liability includes the fee prescribed by the Secretary of State, with "
        "possible injunctions, interest and court costs; this section supplies no "
        "fixed daily penalty.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Section 1706.511 and Form 617 require registration details and the statutory "
        "agent’s written acceptance; no home-jurisdiction certificate attachment or "
        "numeric freshness limit is prescribed."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Ohio Rev. Code §§ 1703.03, 1703.04",
    threshold=QualificationThreshold(
        citation="Ohio Rev. Code § 1703.02",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Corporations solely engaged in interstate commerce are excepted, with "
            "specified machinery installation/demonstration/repair coverage. The "
            "corporate statute does not enumerate the LLC bank-account, internal-affairs, "
            "ordinary solicitation or isolated-transaction safe harbors; those facts "
            "require separate review."
        ),
        exempt_activities=frozenset({Activity.INTERSTATE_COMMERCE}),
    ),
    filing_fee=Decimal("99"),
    forms=(
        StateForm(
            "Foreign for-profit corporation application for license",
            "Form 530A",
            "https://www.ohiosos.gov/assets/530a.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Ohio Rev. Code §§ 1703.28, 1703.29",
        "Forfeiture of $250–$10,000 under § 1703.28 can be remitted; fees, statutory tax "
        "arrears and interest require review. Section 1703.29 adds a $250 "
        "court-access forfeiture and specified cure filings/percentage forfeitures. "
        "Do not combine these into an automatic exact total; current Form 530A "
        "distinguishes business conducted before and after October 15, 2009.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction good-standing or subsistence certificate dated no earlier "
        "than 90 days before application, under § 1703.04 and Form 530A."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Ohio SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="Ohio SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("99"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.ohiosos.gov/business/business-filing-forms",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Ohio SOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="OH",
    name="Ohio",
    registered_agent=RegisteredAgentRequirement(
        citation="Ohio Rev. Code §§ 1706.09, 1703.041",
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
            "Chapter 1706 - Ohio Revised Code | Ohio Laws",
            "https://codes.ohio.gov/ohio-revised-code/chapter-1706",
        ),
        source(
            "Chapter 1703 - Ohio Revised Code | Ohio Laws",
            "https://codes.ohio.gov/ohio-revised-code/chapter-1703",
        ),
        source(
            "Business Filing Forms & Fee Schedule | Ohio Secretary of State",
            "https://www.ohiosos.gov/business/business-filing-forms",
        ),
        source("Ohio statutory/filing guidance", "https://www.ohiosos.gov/assets/617.pdf"),
        source("Ohio statutory/filing guidance", "https://www.ohiosos.gov/assets/530a.pdf"),
        source(
            "Maintain Active Business Status in Ohio | Filing Requirements & Renewal Deadlines",
            "https://www.ohiosos.gov/business/ohio-business-roadmap/keeping-your-business-up-to-date",
        ),
        source(
            "Ohio Business FAQ | Secretary of State Filings, Names, Agents & Complaints",
            "https://www.ohiosos.gov/business/ohio-business-roadmap/frequently-asked-questions",
        ),
    ),
    version="2026-10-11-batch7",
    notes=(
        "Foreign LLC registration and foreign for-profit corporate licensing each "
        "cost $99. Ordinary LLCs and for-profit corporations have no regular SOS "
        "annual report requirement; taxes, agent changes and trade/fictitious-name "
        "renewals are separate. Professional associations, nonprofits and LLPs have "
        "different reporting requirements. Ohio permits the specified rural-route/box "
        "address combination, but a PO box alone or a commercial mail receiving "
        "agency is insufficient.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
