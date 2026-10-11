"""Washington foreign registration under the Uniform Business Organizations Code."""

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
from ._shared import annual, source, unresolved_penalty

_CODE = "https://app.leg.wa.gov/RCW/default.aspx?cite=23.95&full=true"
_FORMS = "https://www.sos.wa.gov/corporations-charities/business-entities/filings-forms-information"
_ONLINE = (
    "https://www.sos.wa.gov/corporations-charities/business-entities/online-filing-instructions/"
)
_ANNUAL = _ONLINE + "file-annual-report-multiple-entity-types-online"
_LLC = _ONLINE + "register-foreign-non-wa-limited-liability-company-llc-online"
_LP = (
    _ONLINE + "register-foreign-non-wa-limited-partnership-lp-or-"
    "limited-liability-limited-partnership-lllp-online"
)


def _entity(entity: EntityType) -> EntityRequirement:
    return EntityRequirement(
        entity_type=entity,
        qualification_citation="RCW 23.95.505, 23.95.510",
        threshold=QualificationThreshold(
            citation="RCW 23.95.520",
            isolated_transaction_max_days=30,
            exempt_activities=frozenset(
                {
                    Activity.INTERSTATE_COMMERCE,
                    Activity.BANK_ACCOUNT,
                    Activity.INTERNAL_AFFAIRS,
                }
            ),
            notes="Local operating activities trigger screening. Listed safe harbors include "
            "interstate commerce, internal affairs, bank accounts, and isolated transactions "
            "completed within 30 days without repetition. Out-of-state order acceptance "
            "also requires no local performance except delivery/installation. Remote-worker "
            "employment alone is a listed safe harbor; unspecified employee duties require review.",
        ),
        filing_fee=Decimal("180"),
        forms=(StateForm("Foreign Registration Statement", "RCW 23.95.510", _FORMS),),
        qualification_penalty=unresolved_penalty(
            "RCW 23.95.505(5)",
            "Historical registration/report fees and penalties that would have been due "
            "must be assessed from filing history. No fixed or daily sanction is assumed.",
        ),
        annual_obligations=(
            annual(
                "Annual report",
                "Use the SOS-record annual expiration date; a report may be filed "
                "within 180 days before expiration.",
                "70",
                "RCW 23.95.255; Washington SOS annual-report instructions",
                "$25 delinquency fee when status is Delinquent. The annual-report "
                "instructions say the listed online report fee includes online processing; "
                "confirm the channel quote. Missing reports/agent can terminate registration.",
            ),
        ),
        consequences=(
            "Cannot maintain a Washington proceeding until registered and historical "
            "fees/penalties are paid.",
            "Failure to register does not impair contracts or the ability to defend a proceeding.",
        ),
        good_standing_evidence="Attach a home-jurisdiction certificate of existence/good standing "
        "or similar document issued no more than 60 days before submission.",
    )


REQUIREMENT = StateRequirement(
    state="WA",
    name="Washington",
    registered_agent=RegisteredAgentRequirement(
        citation="RCW 23.95.405, 23.95.415",
        notes="Designate a consenting eligible commercial or noncommercial agent with a "
        "Washington street address; confirm the required agent email and office contact fields.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source("Washington Uniform Business Organizations Code", _CODE),
        source("Washington SOS business filing forms and fees", _FORMS),
        source("Washington SOS foreign LLC registration instructions", _LLC),
        source("Washington SOS foreign LP registration instructions", _LP),
        source("Washington SOS annual-report instructions", _ANNUAL),
    ),
    version="2026-10-11-official-source-review",
    verification_issues=(
        "The $180 foreign registration fee excludes online processing charges. The "
        "annual-report instructions list $70 including online processing. Confirm "
        "the current channel total and annual expiration "
        "date in the SOS record; processing time is not guaranteed.",
    ),
)
