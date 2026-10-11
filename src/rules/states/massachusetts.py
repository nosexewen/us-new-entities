"""Massachusetts foreign qualification rules from official statutory and filing sources."""

from decimal import Decimal

from ...models import (
    Activity,
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
    qualification_citation="M.G.L. c. 156C, § 48",
    threshold=QualificationThreshold(
        citation="M.G.L. c. 156C, § 48: doing-business analysis",
        exempt_activities=frozenset(),
        notes=(
            "Registration is due within ten days after commencing business. No "
            "automatic LLC activity exemptions or isolated-transaction day limits "
            "are encoded from the separate corporate act; determine whether the LLC "
            "is doing business on its own facts."
        ),
    ),
    filing_fee=Decimal("500"),
    forms=(
        StateForm(
            "Foreign LLC application for registration",
            "c156cs48fllcregistration",
            "https://www.sec.state.ma.us/divisions/corporations/download/c156cs48fllcregistration.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "M.G.L. c. 156C, § 54(a)",
        (
            "Fine of not more than $500 for each year the failure to register "
            "continues. Court access is barred during the failure, while contracts and "
            "defense rights remain valid. Determine the annual periods and assessment "
            "manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule="On or before the anniversary date of the foreign LLC registration filing.",
            fee=Decimal("500"),
            citation="M.G.L. c. 156C, § 48; Corporations Division LLC report guidance",
            notes=(
                "$500 base/paper fee; electronic or fax filings at this fee level add the "
                "published $20 expedited charge, totaling $520."
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
        "Attach a home-jurisdiction certificate of legal existence or good standing "
        "issued by the authorized official. The reviewed registration statute and "
        "guide do not specify a numeric age limit for the initial attachment; do "
        "not borrow the 90-day amendment/reinstatement requirement."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="M.G.L. c. 156D, §§ 15.01, 15.03",
    threshold=QualificationThreshold(
        citation="M.G.L. c. 156D, § 15.01(c)",
        isolated_transaction_without_day_limit=True,
        trigger_activities=frozenset(
            {
                Activity.OFFICE,
                Activity.LOCAL_SERVICES,
                Activity.RETAIL,
                Activity.INTRASTATE_BUSINESS,
                Activity.INCOME_PRODUCING_PROPERTY,
            }
        ),
        notes=(
            "File the registration certificate within ten days after starting "
            "business. Owning or leasing Massachusetts real estate and activities "
            "requiring labor are statutory triggers. Isolated transactions outside "
            "repeated like transactions have no fixed day limit. Corporate "
            "exemptions are not applied to LLCs."
        ),
    ),
    filing_fee=Decimal("400"),
    forms=(
        StateForm(
            "Foreign corporation certificate of registration",
            "c156ds1503950c11348",
            "https://www.sec.state.ma.us/divisions/corporations/filing-by-subject/corporations/corporations-domestic-foreign.htm",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "M.G.L. c. 156D, § 15.02(d)",
        (
            "Historical late fees, interest and penalties plus a monthly or part-month "
            "amount determined by the Secretary subject to the applicable regulatory "
            "ceiling. A corporation that delivers the certificate is exempt from that "
            "monthly penalty for the first 10 days. The reviewed statute does not set a "
            "fixed dollar ceiling; assessment remains manual."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report",
            cycle="annual",
            due_rule=(
                "Within two and one-half months after the close of the corporation fiscal year."
            ),
            fee=Decimal("125"),
            citation="M.G.L. c. 156D, § 16.22; Corporations Division report guidance",
            notes=(
                "$125 timely paper, $150 late paper. Electronic timely base fee $100 plus "
                "published $10 expedited fee; confirm filing method and late pricing."
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
        "Attach a home-jurisdiction certificate of legal existence or good "
        "standing. The initial registration guide supplies no numeric age limit; "
        "the separate 90-day reinstatement rule is not imposed on initial "
        "registration."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Massachusetts Corporations Division foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="LP statutory activity exemptions require separate manual review",
        exempt_activities=frozenset(),
        notes=(
            "Only official LP filing information is populated in this LLC/C-Corp "
            "batch; no automatic safe harbors are encoded."
        ),
    ),
    filing_fee=Decimal("200"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://www.sec.state.ma.us/divisions/corporations/general-information/corporations-filing-fees.htm",
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
    state="MA",
    name="Massachusetts",
    registered_agent=RegisteredAgentRequirement(
        citation="M.G.L. c. 156C, § 48(7); c. 156D, § 15.07",
        notes=(
            "Maintain a consenting resident/registered agent and Massachusetts business "
            "address for service. LLC agent consent must appear on the registration or "
            "be attached. Follow the corporation registered-office requirements and "
            "eligible-agent instructions for the selected entity."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "M.G.L. c. 156D, § 15.07 corporation agent and registered office",
            "https://malegislature.gov/laws/generallaws/parti/titlexxii/chapter156d/section15.07",
        ),
        source(
            "M.G.L. c. 156C, § 48 foreign LLC registration and reports",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXXII/Chapter156C/Section48",
        ),
        source(
            "M.G.L. c. 156C, § 54 failure to register",
            "https://malegislature.gov/laws/generallaws/parti/titlexxii/chapter156c/section54",
        ),
        source(
            "M.G.L. c. 156D, § 15.01 authority and activity exclusions",
            "https://malegislature.gov/laws/generallaws/parti/titlexxii/chapter156d/section15.01",
        ),
        source(
            "M.G.L. c. 156D, § 15.02 failure to register",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXXII/Chapter156D/Section15.02",
        ),
        source(
            "Massachusetts Corporations Division foreign LLC guidance",
            "https://www.sec.state.ma.us/divisions/corporations/filing-by-subject/limited-liability/corporations-foreign-limited-liability-company.htm",
        ),
        source(
            "Massachusetts Corporations Division foreign corporation guidance",
            "https://www.sec.state.ma.us/divisions/corporations/filing-by-subject/corporations/corporations-domestic-foreign.htm",
        ),
        source(
            "Massachusetts Corporations Division filing and expedited fees",
            "https://www.sec.state.ma.us/divisions/corporations/general-information/corporations-filing-fees.htm",
        ),
    ),
    version="2026-10-11-batch4",
    notes=(
        (
            "The modeled qualification charges are $500 LLC and $400 corporation "
            "paper fees. The corporation schedule also lists $375 fax registration, "
            "plus a $15 expedited charge at that fee level. LLC electronic/fax $500 "
            "filings add $20. Corporate and LLC annual report deadlines and fees "
            "differ; taxes, licensing and special professional-entity approvals are "
            "separate."
        ),
    ),
    review_disclosures=(
        (
            "LLC statutory activity exemptions are not inferred from the "
            "corporation act; generic bank-account, interstate-commerce and "
            "isolated-transaction screening remains manual for LLCs."
        ),
        (
            "LP entries contain official qualification-fee information only; LP "
            "reporting, sanctions and activity exemptions require separate "
            "statutory review."
        ),
    ),
)
