"""Alaska foreign-entity rules from current legislative text and Commerce forms."""

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

_ROOT = "https://www.commerce.alaska.gov/web/"
_FEES = _ROOT + "cbpl/Corporations/CorporationFormsFees.aspx"
_REPORTS = _ROOT + "cbpl/Corporations/BiennialReportsFAQs"
_CODE = "https://www.akleg.gov/basis/statutes.asp?media=print&secStart="


def _entity(entity: EntityType) -> EntityRequirement:
    llc = entity == EntityType.LLC
    lp = entity == EntityType.LP
    citation = (
        "AS 32.11.410; Commerce foreign LP registration form 08-517"
        if lp
        else "AS 10.50.600–10.50.720"
        if llc
        else "AS 10.06.705–10.06.718"
    )
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation="AS 10.50.720" if llc else "AS 10.06.718" if not lp else citation,
            **(
                {"exempt_activities": frozenset()}
                if lp
                else {
                    "isolated_transaction_max_days": 30,
                    "exempt_activities": frozenset(
                        {
                            Activity.INTERSTATE_COMMERCE,
                            Activity.BANK_ACCOUNT,
                            Activity.SOLICITATION,
                        }
                    )
                    if llc
                    else QualificationThreshold(citation=citation).exempt_activities,
                }
            ),
            notes="LLC and corporate safe harbors include bank accounts, internal meetings, "
            "interstate commerce and orders accepted outside Alaska. Isolated transactions "
            "must finish within 30 days and not be repeated. LP exemptions are not encoded "
            "and require entity-specific review.",
        ),
        filing_fee=Decimal("150" if lp else "350"),
        forms=(
            StateForm(
                "Certificate of Registration" if llc or lp else "Certificate of Authority",
                "08-517" if lp else "08-0497" if llc else "08-414",
                _ROOT
                + "Portals/5/pub/"
                + ("08-517.pdf" if lp else "corp0497.pdf" if llc else "08-414.pdf"),
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "AS 10.50.690–10.50.710" if llc else "AS 10.06.710, 10.06.713" if not lp else citation,
            "LLC: up to $10,000 for each calendar year or partial year under AS 10.50.700, "
            "plus historical fees and penalties under AS 10.50.690. Corporation: up to "
            "$10,000 per calendar year or portion under AS 10.06.710, plus historical fees, "
            "corporation taxes and penalties. Court-assessed amounts and arrears are manual."
            if not lp
            else "LP sanctions require separate AS 32.11 review; no LLC or "
            "corporation penalty is automatically applied to an LP.",
        ),
        annual_obligations=()
        if lp
        else (
            AnnualObligation(
                name="Biennial report",
                cycle="biennial",
                due_rule="Before January 2 in even or odd years matching the Alaska "
                "registration year; confirm the next report date in the entity record.",
                fee=Decimal("200"),
                citation="AS 10.50.750, 10.50.760; Commerce biennial-report FAQ"
                if llc
                else "AS 10.06.811; Commerce biennial-report FAQ",
                notes="Foreign fee is $200, not the domestic $100. Commerce lists $247.50 "
                "with late charges on or after February 2. Statutory delinquency language "
                "refers to February 1 and mailing compliance; use the January deadline. "
                "The FAQ says foreign entities do not file an Initial Report; the statute's "
                "six-month provision applies upon receipt of a form from the department.",
            ),
        ),
        consequences=(
            "LLCs and corporations cannot maintain Alaska court actions until qualified; "
            "lack of qualification does not invalidate contracts or bar defending proceedings.",
            "Alaska business licenses and professional licenses are separate from entity "
            "registration. LPs do not file Commerce biennial reports under its current FAQ.",
        ),
        good_standing_evidence=(
            "Attach a home-jurisdiction certificate of good standing or equivalent "
            "under form 08-0497 and AS 10.50.615(b); no fixed age cutoff is stated."
            if llc
            else "Current form 08-414 requires an attestation of active home-jurisdiction "
            "good standing and does not list an attached certificate of good standing."
            if not lp
            else "Follow Commerce form 08-517 for LP proof and attachments; do not impose "
            "the LLC certificate requirement automatically."
        ),
    )


REQUIREMENT = StateRequirement(
    state="AK",
    name="Alaska",
    registered_agent=RegisteredAgentRequirement(
        citation="AS 10.06.150, 10.50.055, 32.11.830; Commerce registered-agent FAQ",
        notes="Agent must be an Alaska-resident individual or an authorized domestic or "
        "foreign corporation, not an LLC, LLP or LP. Maintain a real Alaska location "
        "where the agent is physically available; virtual and forwarding-only offices fail.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source(
            "Alaska Statutes Chapter 10.06 (legislative print view)",
            _CODE + "10.06&secEnd=10.06.995",
        ),
        source(
            "Alaska Statutes Chapter 10.50 (legislative print view)",
            _CODE + "10.50&secEnd=10.50.995",
        ),
        source("Commerce entity-specific forms and fees", _FEES),
        source("Commerce biennial-report FAQ", _REPORTS),
        source("Commerce registered-agent FAQ", _ROOT + "cbpl/Corporations/RegisteredAgentsFAQs"),
        source(
            "Commerce foreign corporation application 08-414", _ROOT + "Portals/5/pub/08-414.pdf"
        ),
        source("Commerce foreign LLC application 08-0497", _ROOT + "Portals/5/pub/corp0497.pdf"),
    ),
    version="2026-10-11-batch2",
    notes=(
        "This batch reviews LLC and C-Corp guides. LP filing fees and absence of biennial "
        "reports are sourced to Commerce; LP statutory exemptions and sanctions remain manual.",
    ),
)
