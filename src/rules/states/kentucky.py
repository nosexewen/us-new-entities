"""Kentucky foreign qualification rules from official statutory and filing sources."""

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


def _entity(entity: EntityType) -> EntityRequirement:
    return EntityRequirement(
        entity_type=entity,
        qualification_citation="KRS 14A.9-010, 14A.9-030",
        threshold=QualificationThreshold(
            citation="KRS 14A.9-010(2)",
            isolated_transaction_max_days=30,
            notes=(
                "Isolated transactions must finish within 30 days and not be in a "
                "course of repeated like transactions. Orders must require acceptance "
                "outside the state; tax and regulatory nexus are separate."
            ),
        ),
        filing_fee=Decimal("90"),
        forms=(
            StateForm(
                "Certificate of authority",
                "FBE",
                "https://web.sos.ky.gov/forms/corp/FBE-Certificate%20of%20Authorization_Foreign%20Business%20Entity.pdf",
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "KRS 14A.9-020(4)",
            (
                "$2 for each day transacting business without authority, collectible by the "
                "Secretary of State. Determine the days of covered business and any "
                "additional charges manually; no unsupported maximum is imposed."
            ),
        ),
        annual_obligations=(
            AnnualObligation(
                name="Annual report",
                cycle="annual",
                due_rule="January 1 through June 30, beginning the year after authorization.",
                fee=Decimal("15"),
                citation="KRS 14A.6-010; Kentucky SOS filing fees",
                notes="",
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
            "Execution of the application represents that the entity validly exists in "
            "its home jurisdiction under KRS 14A.9-030(2). The reviewed application "
            "requirements do not mandate a home-state certificate attachment or numeric "
            "freshness limit; the agent must sign or supply written consent."
        ),
    )


REQUIREMENT = StateRequirement(
    state="KY",
    name="Kentucky",
    registered_agent=RegisteredAgentRequirement(
        citation="KRS 14A.4-010, 14A.9-030(3)",
        notes=(
            "The applicant cannot act as its own registered agent under FBE instructions. "
            "Maintain a Kentucky registered office and consenting resident individual "
            "or eligible domestic/qualified foreign entity at the same business "
            "address. The agent must sign the filing or deliver written acceptance. "
            "Keep the agent communications contact current. Legacy LP agent exceptions "
            "in § 14A.4-010 require entity-specific review."
        ),
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source(
            "Kentucky SOS foreign entity application FBE",
            "https://web.sos.ky.gov/forms/corp/FBE-Certificate%20of%20Authorization_Foreign%20Business%20Entity.pdf",
        ),
        source(
            "KRS 14A.9-010 qualification and safe harbors",
            "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=44318",
        ),
        source(
            "KRS 14A.9-020 qualification sanctions",
            "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=36569",
        ),
        source(
            "KRS 14A.9-030 foreign application",
            "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=40424",
        ),
        source(
            "KRS 14A.6-010 annual reports",
            "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=47075",
        ),
        source(
            "KRS 14A.4-010 registered agent and consent",
            "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=36549",
        ),
        source(
            "Kentucky SOS business filing fees",
            "https://www.sos.ky.gov/bus/business-filings/Pages/Fees.aspx",
        ),
    ),
    version="2026-10-11-batch4",
    notes=(
        (
            "Qualification costs $90 and annual reports cost $15 under the SOS "
            "schedule. Foreign entities seeking state contracts must satisfy KRS "
            "14A.9-010(6), even where ordinary activity exemptions may otherwise "
            "apply. Optional services, licensing and taxes are separate."
        ),
    ),
)
