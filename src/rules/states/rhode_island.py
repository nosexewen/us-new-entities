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
    qualification_citation="R.I. Gen. Laws § 7-16-49",
    threshold=QualificationThreshold(
        citation="R.I. Gen. Laws § 7-16-54(e)",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("150"),
    forms=(
        StateForm(
            "Application for registration",
            "Form 450",
            "https://docs.sos.ri.gov/documents/BusinessServices/450-application-for-registration.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "R.I. Gen. Laws § 7-16-54",
        "Cannot maintain proceedings until registered; contracts, defenses and member "
        "liability protections remain valid. SOS becomes service agent for "
        "unregistered business. Other sanctions require separate review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="February 1 through May 1, beginning the calendar year after registration.",
            fee=Decimal("50"),
            citation="R.I. Gen. Laws §§ 7-16-65(13), 7-16-66",
            notes=(
                "Late penalty $25 per year after the statutory 30-day grace period; SOS "
                "applies it June 1. Online access fees are separate."
            ),
        ),
        AnnualObligation(
            name="Annual minimum business tax / tax return",
            cycle="annual",
            due_rule=(
                "Follow the Division of Taxation deadline for the entity’s tax classification."
            ),
            fee=None,
            citation="Rhode Island DOS foreign registration and costs guidance",
            notes=(
                "Agency guidance states at least $400 annually for registered for-profit "
                "entities, even without profit or activity; tax is not prorated. Income-based "
                "taxes may exceed the minimum. This tax is separate from the $50 SOS annual "
                "report."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of good standing/legal existence dated within "
        "60 days of filing, required by SOS Form 450 and registration guidance."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="R.I. Gen. Laws §§ 7-1.2-1401, 7-1.2-1405",
    threshold=QualificationThreshold(
        citation="R.I. Gen. Laws § 7-1.2-1401(b)",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Corporate authority fee is a minimum of $310; the "
            "represented-share license fee can increase the total under § 7-1.2-1602(d)."
        ),
    ),
    filing_fee=Decimal("310"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Form 150",
            "https://docs.sos.ri.gov/documents/BusinessServices/150-certificate-of-authority.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "R.I. Gen. Laws § 7-1.2-1418",
        "Cannot maintain proceedings until authorized; unpaid fees, franchise taxes "
        "and applicable penalties for years or parts of years of unauthorized "
        "activity are recoverable. Contracts and defenses remain valid; injunctions "
        "require manual review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "February 1 through May 1, beginning the calendar year after authority is issued."
            ),
            fee=Decimal("50"),
            citation="R.I. Gen. Laws §§ 7-1.2-1501, 7-1.2-1602(a)(19)",
            notes=(
                "Late penalty $25 per year after the statutory 30-day grace period; SOS "
                "applies it June 1. Online access fees are separate."
            ),
        ),
        AnnualObligation(
            name="Annual minimum business tax / tax return",
            cycle="annual",
            due_rule=(
                "Follow the Division of Taxation deadline for the entity’s tax classification."
            ),
            fee=None,
            citation="Rhode Island DOS foreign registration and costs guidance",
            notes=(
                "Agency guidance states at least $400 annually for registered for-profit "
                "entities, even without profit or activity; tax is not prorated. Income-based "
                "taxes may exceed the minimum. This tax is separate from the $50 SOS annual "
                "report."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of good standing/legal existence dated within "
        "60 days of filing, per SOS registration guidance."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Rhode Island DOS foreign LP registration fee",
    threshold=QualificationThreshold(
        citation="Rhode Island DOS foreign LP registration fee",
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
            "https://www.sos.ri.gov/divisions/business-services/foreign-business/register-your-business-in-ri",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Rhode Island DOS foreign LP registration fee", "LP sanctions require separate review."
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
    state="RI",
    name="Rhode Island",
    registered_agent=RegisteredAgentRequirement(
        citation="R.I. Gen. Laws §§ 7-16-11, 7-1.2-501",
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
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-16/7-16-49.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-16/7-16-54.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/statutes/title7/7-16/7-16-65.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-16/7-16-66.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-1.2/7-14/7-1.2-1401.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/statutes/title7/7-1.2/7-14/7-1.2-1405.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-1.2/7-14/7-1.2-1418.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-1.2/7-15/7-1.2-1501.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/statutes/title7/7-1.2/7-16/7-1.2-1602.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/Statutes/TITLE7/7-16/7-16-11.htm",
        ),
        source(
            "Rhode Island statutory/filing guidance",
            "https://webserver.rilegislature.gov/statutes/title7/7-1.2/7-5/7-1.2-501.htm",
        ),
        source(
            "Register Business In RI - Rhode Island - Gregg M. Amore",
            "https://www.sos.ri.gov/divisions/business-services/foreign-business/register-your-business-in-ri",
        ),
        source(
            "Form 450 Application for Registration for a Foreign Limited Liability Company",
            "https://docs.sos.ri.gov/documents/BusinessServices/450-application-for-registration.pdf",
        ),
        source(
            "150 Certificate of Authority",
            "https://docs.sos.ri.gov/documents/BusinessServices/150-certificate-of-authority.pdf",
        ),
        source(
            "Costs And Fees - Rhode Island - Gregg M. Amore",
            "https://www.sos.ri.gov/divisions/business-services/foreign-business/business-basics/costs-and-fees",
        ),
        source(
            "File Your Annual Business Report - Rhode Island - Gregg M. Amore",
            "https://www.sos.ri.gov/divisions/business-services/ri-business/file-your-annual-report",
        ),
    ),
    version="2026-10-11-batch8",
    notes=(
        "Foreign LLC registration is $150. Corporate authority is ordinarily at least "
        "$310: $150 filing plus $160 license fee for fewer than 75 million authorized "
        "shares represented in Rhode Island. At 75 million or more represented shares "
        "the license fee is one-fifth cent per share; $310 is not a universal total. "
        "Annual reports are $50, February 1–May 1 beginning the next calendar year, "
        "plus the separate minimum annual tax described below. Online annual reports "
        "add a $2.50 access fee; reports late as of June 1 add a $25 penalty, with $3 "
        "online access fee for late filing.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
