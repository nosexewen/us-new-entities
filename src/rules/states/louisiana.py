"""Louisiana foreign qualification rules from official statutory and filing sources."""

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
    qualification_citation="La. R.S. 12:1342, 12:1345",
    threshold=QualificationThreshold(
        citation="La. R.S. 12:1343",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate. "
            "Acquisition/disposition of property outside regular business is "
            "listed; operations and industry-specific financial exemptions require "
            "separate review."
        ),
    ),
    filing_fee=Decimal("185"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "972",
            "https://www.sos.la.gov/media/ablp3yv5/972-application-of-foreign-limited-liability-company.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "La. R.S. 12:1354(C)",
        (
            "Historical fees and taxes for years or parts of years without authority, "
            "plus applicable nonpayment penalties. The Attorney General recovers "
            "amounts due; neither reviewed section gives a fixed civil-penalty maximum. "
            "Assess historical rates and actual liabilities manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "On or before the qualification anniversary date each year; corporation "
                "first report is due the anniversary in the following calendar year."
            ),
            fee=Decimal("35"),
            citation="La. R.S. 12:1350.1",
            notes=(
                "Current SOS schedule effective October 1, 2026 sets $35, superseding older "
                "$30 forms. Credit-card payments add a $5 statutory convenience charge."
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
        "Attach an original home-jurisdiction certificate of existence or good "
        "standing dated within 90 days of submission; articles alone do not replace "
        "it. See SOS form 972 and R.S. 12:304(E) for the respective entity types."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="La. R.S. 12:301, 12:304",
    threshold=QualificationThreshold(
        citation="La. R.S. 12:302",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate. "
            "Acquisition/disposition of property outside regular business is "
            "listed; operations and industry-specific financial exemptions require "
            "separate review."
        ),
    ),
    filing_fee=Decimal("155"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "326",
            "https://www.sos.la.gov/media/idoafmga/326-application-of-foreign-corporation-for-certificate-of-authority.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "La. R.S. 12:314(C)",
        (
            "Historical fees and taxes for years or parts of years without authority, "
            "plus applicable nonpayment penalties. The Attorney General recovers "
            "amounts due; neither reviewed section gives a fixed civil-penalty maximum. "
            "Assess historical rates and actual liabilities manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "On or before the qualification anniversary date each year; corporation "
                "first report is due the anniversary in the following calendar year."
            ),
            fee=Decimal("35"),
            citation="La. R.S. 12:309",
            notes=(
                "Current SOS schedule effective October 1, 2026 sets $35, superseding older "
                "$30 forms. Credit-card payments add a $5 statutory convenience charge."
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
        "Attach an original home-jurisdiction certificate of existence or good "
        "standing dated within 90 days of submission; articles alone do not replace "
        "it. See SOS form 972 and R.S. 12:304(E) for the respective entity types."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Louisiana SOS foreign partnership filing schedule",
    threshold=QualificationThreshold(
        citation="LP statutory activity exemptions require separate manual review",
        exempt_activities=frozenset(),
        notes=(
            "Only official LP filing information is populated in this LLC/C-Corp "
            "batch; no automatic safe harbors are encoded."
        ),
    ),
    filing_fee=Decimal("185"),
    forms=(
        StateForm(
            "Foreign partnership registration",
            "344",
            "https://www.sos.la.gov/business-services/forms-fee-schedule",
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
    state="LA",
    name="Louisiana",
    registered_agent=RegisteredAgentRequirement(
        citation="La. R.S. 12:1350; 12:308",
        notes=(
            "Maintain a Louisiana registered office and eligible resident individual or "
            "qualifying entity agent with an in-state address for service. Obtain the "
            "agent acceptance required by the entity-specific application; keep current "
            "office and business-establishment information."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Louisiana SOS foreign corporation application 326",
            "https://www.sos.la.gov/media/idoafmga/326-application-of-foreign-corporation-for-certificate-of-authority.pdf",
        ),
        source("R.S. 12:1342 foreign LLC authority", "https://legis.la.gov/Legis/Law.aspx?d=76297"),
        source(
            "R.S. 12:1343 LLC activity exclusions", "https://legis.la.gov/Legis/Law.aspx?d=76298"
        ),
        source(
            "R.S. 12:1345 foreign LLC application", "https://legis.la.gov/Legis/Law.aspx?d=76300"
        ),
        source(
            "R.S. 12:1354 unregistered LLC consequences",
            "https://legis.la.gov/Legis/Law.aspx?d=76311",
        ),
        source(
            "R.S. 12:1350 foreign LLC agent requirements",
            "https://legis.la.gov/Legis/Law.aspx?d=76306",
        ),
        source(
            "R.S. 12:1350.1 foreign LLC annual report",
            "https://legis.la.gov/Legis/Law.aspx?d=76307",
        ),
        source(
            "R.S. 12:301 foreign corporation authority",
            "https://legis.la.gov/Legis/Law.aspx?d=76472",
        ),
        source(
            "R.S. 12:302 corporate activity exclusions",
            "https://legis.la.gov/Legis/Law.aspx?d=76473",
        ),
        source(
            "R.S. 12:304 foreign corporation application",
            "https://legis.la.gov/Legis/Law.aspx?d=76475",
        ),
        source(
            "R.S. 12:314 unregistered corporation consequences",
            "https://legis.la.gov/Legis/Law.aspx?d=76488",
        ),
        source(
            "R.S. 12:308 foreign corporation agent requirements",
            "https://legis.la.gov/Legis/Law.aspx?d=76480",
        ),
        source(
            "R.S. 12:309 foreign corporation annual report",
            "https://legis.la.gov/Legis/Law.aspx?d=76481",
        ),
        source(
            "SOS foreign LLC application 972",
            "https://www.sos.la.gov/media/ablp3yv5/972-application-of-foreign-limited-liability-company.pdf",
        ),
        source(
            "Louisiana SOS business forms and fees",
            "https://www.sos.la.gov/business-services/forms-fee-schedule",
        ),
        source(
            "Louisiana SOS fee schedule effective October 1, 2026",
            "https://static.sos.la.gov/shared/fee_changes_2026.pdf",
        ),
        source(
            "Louisiana SOS filing and payment guidance",
            "https://www.sos.la.gov/business-services/file-business-documents",
        ),
    ),
    version="2026-10-11-batch4",
    notes=(
        (
            "Effective October 1, 2026, SOS fees are $185 for foreign LLC "
            "authority, $155 for foreign corporation authority and $35 for annual "
            "reports. Credit-card payments add $5; expedited handling adds $35 (24 "
            "hours) or $60 (priority). Taxes and licensing are separate."
        ),
    ),
    review_disclosures=(
        (
            "Noted discrepancy, resolved by disclosure: older foreign LLC form 972 "
            "quotes $150; current corporation form 326 agrees with the $155 schedule. "
            "Older report instructions quote $30. The dated SOS October 1, 2026 "
            "schedule controls the modeled $185/$155 qualification and $35 report "
            "charges; use older forms for application content, not current pricing."
        ),
        (
            "LP entries contain official foreign partnership fees and filing "
            "guidance only; LP statutory sanctions, exemptions and reports require "
            "separate review."
        ),
    ),
)
