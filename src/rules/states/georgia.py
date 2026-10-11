"""Georgia foreign-entity filing rules from the SOS registration guide and FAQ."""

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

_GUIDE = "https://sos.ga.gov/how-to-guide/how-to-guide-register-foreign-entity"
_FAQ = "https://sos.ga.gov/page/business-division-faq"
_ANNUAL = "https://sos.ga.gov/how-to-guide/how-file-annual-registration"


def _entity(entity: EntityType, citation: str, identifier: str) -> EntityRequirement:
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation=citation,
            exempt_activities=frozenset(),
            notes=(
                "Local operations are screening signals. Apply the entity-specific Georgia "
                "transacting-business statute; statutory safe harbors have not been encoded "
                "in this batch and require manual review."
            ),
        ),
        filing_fee=Decimal("235"),
        forms=(StateForm("Application for Certificate of Authority", identifier, _GUIDE),),
        qualification_penalty=unresolved_penalty(
            "Georgia SOS foreign-registration FAQ; " + citation,
            "SOS guidance imposes a $500 late-qualification penalty after more than 30 days "
            "of business without registration. LLCs and LPs also owe the fees that would "
            "have been imposed if registered. Do not repeat $500 annually as for LLPs; "
            "confirm entity-specific statutory assessment and arrears before calculating.",
        ),
        annual_obligations=(
            annual(
                "Annual registration",
                "January 1–April 1, starting in the year following foreign qualification.",
                "60",
                "Georgia SOS annual-registration guide",
                "$50 filing fee plus $10 service charge under the current guide; "
                "$25 late-registration penalty. Older SOS fee tables show different totals; "
                "confirm the current portal quote. Failure to file can lead to revocation.",
            ),
        ),
        consequences=(
            "Registration is required before transacting business; review litigation "
            "restrictions and sanctions in the applicable entity statute.",
            "Foreign authority revoked for missing annual registrations requires a new "
            "application and qualification fee; domestic reinstatement is a different remedy.",
        ),
        good_standing_evidence=(
            "Foreign corporations must attach an original certificate of existence/good "
            "standing from the home jurisdiction dated no more than 90 days before filing."
            if entity == EntityType.C_CORP
            else "No certified home-state existence certificate is required under "
            "Georgia Rule 590-7-21-.07(1)(a) (LLC) or 590-7-12-.08(1)(a) (LP). "
            "Maintain home-state qualification and current filings."
        ),
    )


REQUIREMENT = StateRequirement(
    state="GA",
    name="Georgia",
    registered_agent=RegisteredAgentRequirement(
        citation="Georgia SOS registration and annual-registration guides",
        notes="Maintain an eligible agent at a physical Georgia street address where "
        "an individual can be located in person; no PO-box-only registered office.",
    ),
    entity_rules={
        EntityType.LLC: _entity(EntityType.LLC, "O.C.G.A. §§ 14-11-702, 14-11-703", "CD 241"),
        EntityType.C_CORP: _entity(EntityType.C_CORP, "O.C.G.A. §§ 14-2-1501–14-2-1503", "CD 236"),
        EntityType.LP: _entity(EntityType.LP, "O.C.G.A. § 14-9-902", "CD 251"),
    },
    sources=(
        source("Georgia SOS foreign entity registration guide", _GUIDE),
        source("Georgia SOS business division FAQ", _FAQ),
        source("Georgia SOS annual-registration guide", _ANNUAL),
        source("Georgia LLC foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-21"),
        source("Georgia corporation foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-3"),
        source("Georgia LP foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-12"),
    ),
    version="2026-10-11-official-guidance-review",
    verification_issues=(
        "The current registration guide quotes $235 including $10 service charge. "
        "Annual-registration guidance quotes $60 while older SOS fee schedules/FAQ "
        "show lower online amounts; verify the filing channel's current total.",
        "Primary statutory safe-harbor review remains incomplete: the official Lexis "
        "portal supplied only a contents page. SOS-linked Fastcase LLC § 14-11-702 "
        "text was retrieved, but is a third-party reproduction, not primary-law "
        "verification. Exempt activities and isolated transactions remain manual.",
    ),
    notes=(
        "October 11 live annual-guide table explicitly lists $60 for both online and "
        "paper filing. The portal landing page supplies no fee quote without choosing "
        "an entity; its $20 amendment notice also conflicts with the guide's $30. "
        "These inconsistencies remain disclosed rather than assumed superseded.",
        "Official administrative rules independently confirm the $500 LLC/corporate "
        "late-qualification assessment after 30 days, additional charges and "
        "LLC/LP certificate exceptions; numeric historical totals still need applicant facts.",
    ),
)
