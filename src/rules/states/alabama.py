"""Alabama foreign registration under Title 10A and current SOS guidance."""

from decimal import Decimal

from ...models import (
    EntityRequirement,
    EntityType,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)
from ._shared import source, unresolved_penalty

_CODE = "https://alison.legislature.state.al.us/code-of-alabama?section="
_FEES = "https://sos.alabama.gov/sites/default/files/form-files/FeeSchedule.pdf"
_NOTICE = (
    "https://www.sos.alabama.gov/newsroom/"
    "secretary-state-wes-allen-applauds-final-passage-legislation-cutting-red-tape-alabama"
)


def _entity(entity: EntityType) -> EntityRequirement:
    citation = "Ala. Code §§ 10A-1-7.01–10A-1-7.04"
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation=citation,
            exempt_activities=frozenset(),
            notes="Apply the current Title 10A registration provisions and other applicable "
            "law. No generic activity safe harbors or isolated-transaction day limit are "
            "assumed from repealed corporate provisions; exemptions require manual review.",
        ),
        filing_fee=Decimal("150"),
        forms=(
            StateForm(
                "Application for Registration",
                "Foreign entity application under § 10A-1-7.04",
                "https://www.sos.alabama.gov/sites/default/files/"
                + (
                    "2022-09/ForeignLLCRegistration.pdf"
                    if entity == EntityType.LLC
                    else "2022-09/ForeignCorporationRegistration.pdf"
                    if entity == EntityType.C_CORP
                    else "2022-11/ForeignLPStatementAuthority.pdf"
                ),
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "Ala. Code § 10A-1-7.23",
            "After more than 90 days transacting business without registration, the SOS "
            "may collect a late filing fee equal to the registration fee ($150) for each "
            "year of delinquency and condition registration on payment. Assessment and "
            "the applicable delinquency years require manual review; this is not a daily fine.",
        ),
        annual_obligations=(),
        consequences=(
            "An unregistered foreign entity generally cannot maintain a state-court action "
            "until registered (§ 10A-1-7.21); federal-law entities have a statutory exception.",
            "Failure to register does not invalidate contracts or prevent defending an action.",
            "Business privilege tax and business licenses are separate obligations; the "
            "absence of an SOS annual report does not mean no tax filings are required.",
        ),
        good_standing_evidence="The application must state valid existence in the formation "
        "jurisdiction (§ 10A-1-7.04(b)(5)). Attach the Alabama name reservation certificate "
        "required by § 10A-1-7.01(e); check the current entity-specific application attachments.",
    )


REQUIREMENT = StateRequirement(
    state="AL",
    name="Alabama",
    registered_agent=RegisteredAgentRequirement(
        citation="Ala. Code § 10A-1-5.31",
        notes="Maintain a resident individual or eligible domestic/registered foreign entity "
        "at an Alabama street address for personal service. The agent's business office "
        "must match the registered office; virtual-only, mail-forwarding-only, mailbox-only "
        "and telephone-answering-only offices do not qualify.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=tuple(
        source(f"Ala. Code § {section}", _CODE + section)
        for section in (
            "10A-1-7.01",
            "10A-1-7.02",
            "10A-1-7.04",
            "10A-1-7.21",
            "10A-1-7.23",
            "10A-1-5.31",
        )
    )
    + (
        source(
            "Alabama SOS current forms and attachments",
            "https://www.sos.alabama.gov/business-entities/business-downloads",
        ),
        source(
            "Alabama SOS foreign LLC application",
            "https://www.sos.alabama.gov/sites/default/files/2022-09/ForeignLLCRegistration.pdf",
        ),
        source(
            "Alabama SOS foreign corporation application",
            "https://www.sos.alabama.gov/sites/default/files/2022-09/ForeignCorporationRegistration.pdf",
        ),
        source("Alabama SOS fee schedule (August 23, 2023 revision)", _FEES),
        source("Alabama SOS: annual report repeal effective October 1, 2024", _NOTICE),
    ),
    version="2026-10-11-batch2",
    review_disclosures=(
        "The 2023 fee schedule's $10 corporate annual report row is superseded by "
        "HB 230, signed May 7, 2024 and effective October 1, 2024, as confirmed by "
        "the SOS. No SOS annual report is imposed here on LLCs or business corporations.",
    ),
    notes=(
        "The $150 registration fee excludes the required $25 name reservation, "
        "online processing charges and optional expedited service. Reserve the name "
        "and attach the certificate before filing; no processing duration is promised.",
    ),
)
