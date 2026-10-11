"""Colorado foreign entity rules reviewed against the official 2026 Title 7."""

from decimal import Decimal

from ...models import (
    EntityRequirement,
    EntityType,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)
from ._shared import annual, source, unresolved_penalty

_CODE = "https://olls.info/crs/crs2026-title-07.htm"
_SOS = "https://www.coloradosos.gov/"
_FEES = "https://www.sos.state.co.us/pubs/info_center/fees/business.html"


def _entity(entity: EntityType) -> EntityRequirement:
    citation = "C.R.S. §§ 7-90-801–7-90-803"
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation="C.R.S. § 7-90-801(2)",
            isolated_transaction_max_days=30,
            notes="Bank accounts, internal affairs, interstate commerce and orders accepted "
            "outside Colorado are safe harbors. Isolated transactions must complete within "
            "30 days and not be part of repeated like transactions. Owning property without "
            "more is listed, but property operations require their own facts.",
        ),
        filing_fee=Decimal("100"),
        forms=(
            StateForm(
                "Statement of Foreign Entity Authority",
                "SOFEA",
                _SOS + "pubs/business/FAQs/foreigns.html",
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "C.R.S. § 7-90-802(2)–(4)",
            "A prescribed fee of no more than $100 for each calendar year or partial year "
            "without authority, plus a civil penalty of no more than $5,000. The $5,000 "
            "civil penalty is not multiplied by years. Assessment, interest and court costs "
            "remain manual; authority cannot be filed until applicable amounts are paid.",
        ),
        annual_obligations=(
            annual(
                "Periodic report",
                "Annually; default deadline is the last day of the second "
                "calendar month after the anniversary reporting month. Confirm the assigned "
                "month in the SOS record; filing opens two months before that month.",
                None if entity == EntityType.LP else "25",
                "C.R.S. § 7-90-501; SOS periodic-report FAQ and fee schedule",
                "$50 late filing penalty; continuing failure leads to delinquent status. "
                "For LPs, confirm reporting-entity status under § 7-90-102(58.5), including "
                "formation date and any election; older nonreporting LPs are not assumed to "
                "owe a periodic report. Reporting LPs pay the same $25 fee. "
                "Beginning July 1, 2027, employer EEO-1 reporting "
                "requirements in § 7-90-501(1)(f) also require review.",
            ),
        ),
        consequences=(
            "Without authority, the foreign entity cannot maintain a Colorado debt-collection "
            "court proceeding; the court may stay proceedings pending qualification.",
            "Lack of authority does not invalidate acts or prevent defending proceedings. "
            "The attorney general may seek civil penalties and an injunction.",
        ),
        good_standing_evidence="Provide the formation jurisdiction and true entity name "
        "on the electronic SOFEA; follow current filing instructions for any attachments. "
        "No unsupported home-state certificate freshness deadline is imposed.",
    )


REQUIREMENT = StateRequirement(
    state="CO",
    name="Colorado",
    registered_agent=RegisteredAgentRequirement(
        citation="C.R.S. § 7-90-701; SOS registered-agent requirements effective July 1, 2025",
        notes="Agent must consent. An individual must be at least 18 with Colorado residence "
        "or usual place of business and verified eligibility using Colorado ID or the "
        "alternative mailed-passcode process. An entity agent must be registered and in "
        "good standing with a usual Colorado place of business. Maintain a physical "
        "street address for in-person service during normal business hours, not a PO box.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source("Official Colorado Revised Statutes 2026 Title 7 (OLLS download)", _CODE),
        source("Colorado SOS business fee schedule, revised July 1, 2024", _FEES),
        source(
            "Colorado SOS periodic-report FAQ",
            "https://sos.state.co.us/pubs/business/FAQs/reports.html",
        ),
        source("Colorado SOS foreign-entity filing FAQ", _SOS + "pubs/business/FAQs/foreigns.html"),
        source(
            "Colorado SOS agent requirements from July 1, 2025",
            _SOS + "pubs/business/RAchanges.html",
        ),
    ),
    version="2026-10-11-batch2",
    notes=(
        "Foreign authority is a $100 online filing; the current periodic-report fee is "
        "$25, not the former $10. Taxes, licensing and optional services are separate. "
        "LP reporting status requires manual confirmation before charging a report fee.",
    ),
)
