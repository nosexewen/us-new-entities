"""Maine foreign qualification rules from official statutory and filing sources."""

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
    qualification_citation="31 M.R.S. § 1622",
    threshold=QualificationThreshold(
        citation="31 M.R.S. § 1623",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate. Owning "
            "property without more is listed; operations require their own facts."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Statement of foreign qualification",
            "MLLC-12",
            "https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/mllc12.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "31 M.R.S. § 1629",
        (
            "$500 for each year or portion of a year conducting business without "
            "authority. Attorney General collection and any interest or court costs "
            "require manual assessment; do not present an estimated total as a court "
            "determination."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="January 1 through June 1, beginning the calendar year after qualification.",
            fee=Decimal("150"),
            citation="31 M.R.S. §§ 1665, 1680(7), (10)",
            notes=(
                "$150 foreign entity report fee, not the domestic $85 rate. Late filing "
                "adds $50 and continuing defaults may cause revocation."
            ),
        ),
    ),
    consequences=(
        (
            "The LLC cannot maintain a Maine proceeding to collect its debts without an "
            "effective qualification statement. Contracts and defense rights remain "
            "valid; the Attorney General may seek an injunction."
        ),
    ),
    good_standing_evidence=(
        "Attach an authenticated certificate of existence or suitable similar "
        "home-jurisdiction document issued not more than 90 days before delivery of "
        "the application."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="13-C M.R.S. §§ 1501, 1503",
    threshold=QualificationThreshold(
        citation="13-C M.R.S. § 1501(2)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate. Owning "
            "property without more is listed; operations require their own facts."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Application for authority",
            "MBCA-12",
            "https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/mbca12.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "13-C M.R.S. § 1502(4)",
        (
            "$500 for each year or portion of a year conducting business without "
            "authority. Attorney General collection and any interest or court costs "
            "require manual assessment; do not present an estimated total as a court "
            "determination."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="January 1 through June 1, beginning the calendar year after qualification.",
            fee=Decimal("150"),
            citation="13-C M.R.S. §§ 1621, 123(1)(DD-1), (EE)",
            notes=(
                "$150 foreign entity report fee, not the domestic $85 rate. Late filing "
                "adds $50 and continuing defaults may cause revocation."
            ),
        ),
    ),
    consequences=(
        (
            "Failure to qualify does not invalidate contracts or prevent defending "
            "proceedings; maintaining proceedings requires qualification under the "
            "entity-specific statute."
        ),
    ),
    good_standing_evidence=(
        "Attach an authenticated certificate of existence or suitable similar "
        "home-jurisdiction document issued not more than 90 days before delivery of "
        "the application."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Maine SOS foreign LP application and fee schedule",
    threshold=QualificationThreshold(
        citation="LP statutory activity exemptions require separate manual review",
        exempt_activities=frozenset(),
        notes=(
            "Only official LP filing information is populated in this LLC/C-Corp "
            "batch; no automatic safe harbors are encoded."
        ),
    ),
    filing_fee=Decimal("250"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "MLPA-12",
            "https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/mlpa12.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "LP sanctions require separate statutory review",
        (
            "No LLC or corporate penalty is applied automatically. LP penalties, "
            "reporting and litigation consequences require an entity-specific review."
        ),
    ),
    consequences=(
        ("Authority, court-access remedies and other consequences require separate LP review."),
    ),
    good_standing_evidence=(
        "Confirm the home-jurisdiction evidence required by the current "
        "entity-specific application."
    ),
)

REQUIREMENT = StateRequirement(
    state="ME",
    name="Maine",
    registered_agent=RegisteredAgentRequirement(
        citation="5 M.R.S. § 105; MLLC-12 and MBCA-12",
        notes=(
            "Designate a commercial registered agent by its listed name, or identify a "
            "noncommercial agent and Maine physical street address. Designation affirms "
            "consent; a PO box alone is not sufficient. The applications distinguish "
            "commercial and noncommercial agents."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Maine Revised Statutes Title 31 Chapter 21 LLC Act",
            "https://legislature.maine.gov/statutes/31/title31ch21.pdf",
        ),
        source(
            "31 M.R.S. § 1680 fees and penalties",
            "https://legislature.maine.gov/statutes/31/title31sec1680.html",
        ),
        source(
            "31 M.R.S. § 1665 annual reports",
            "https://legislature.maine.gov/statutes/31/title31sec1665.html",
        ),
        source(
            "13-C M.R.S. § 1501 authority and safe harbors",
            "https://legislature.maine.gov/statutes/13-C/title13-Csec1501.html",
        ),
        source(
            "13-C M.R.S. § 1502 unregistered corporation consequences",
            "https://legislature.maine.gov/statutes/13-C/title13-Csec1502.html",
        ),
        source(
            "13-C M.R.S. § 1621 annual reports",
            "https://legislature.maine.gov/statutes/13-C/title13-Csec1621.html",
        ),
        source(
            "13-C M.R.S. § 123 filing fees",
            "https://legislature.maine.gov/statutes/13-C/title13-Csec123.html",
        ),
        source(
            "5 M.R.S. § 105 agent designation and consent",
            "https://legislature.maine.gov/statutes/5/title5sec105.html",
        ),
        source(
            "Maine SOS foreign entity applications and fees",
            "https://www.maine.gov/sos/corporations-commissions/information-about-entities/entity-types/foreign-entites",
        ),
        source(
            "Maine SOS foreign LLC form MLLC-12",
            "https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/mllc12.pdf",
        ),
        source(
            "Maine SOS foreign corporation form MBCA-12",
            "https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/mbca12.pdf",
        ),
        source(
            "Maine SOS report reminders and fees",
            "https://www.maine.gov/sos/corporations-commissions/incorporating-resources/corporations-commissions/filing-requirement-reminders",
        ),
    ),
    version="2026-10-11-batch4",
    notes=(
        (
            "Both requested foreign entity types pay $250 qualification and $150 "
            "annual reporting, with a $50 late report charge. Reports start the "
            "year after qualification and are due by June 1. Taxes and optional "
            "services are separate."
        ),
    ),
    review_disclosures=(
        (
            "LP entries contain official application and qualification-fee "
            "information only; statutory sanctions, activity exemptions and "
            "reporting require separate LP review."
        ),
    ),
)
