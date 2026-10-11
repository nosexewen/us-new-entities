"""North Carolina foreign-entity rules reviewed against the General Statutes."""

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

_ROOT = "https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/ByChapter/"
_SOS = "https://www.sosnc.gov/webfiles/documents/forms/Business_Registration/"
_APPLICATIONS = {
    EntityType.LLC: (
        "L-09",
        "limited_liability_companies/application_for_certificate_of_authority.pdf",
    ),
    EntityType.C_CORP: (
        "B-09",
        "business_Corporations/application_of_certificate_of_authority.pdf",
    ),
    EntityType.LP: (
        "LP-04",
        "limited_partnerships/Application_for_Registration_as_a_foreign_limited_partnership.pdf",
    ),
}


def _entity(entity: EntityType) -> EntityRequirement:
    identifier, application = _APPLICATIONS[entity]
    citation = {
        EntityType.LLC: "N.C. Gen. Stat. §§ 57D-7-01–57D-7-03",
        EntityType.C_CORP: "N.C. Gen. Stat. §§ 55-15-01–55-15-03",
        EntityType.LP: "N.C. Gen. Stat. §§ 59-902, 59-907",
    }[entity]
    reports = (
        (
            annual(
                "Annual report",
                "April 15, first due in the calendar year following authorization.",
                "200",
                "N.C. Gen. Stat. §§ 57D-2-24, 57D-1-22",
                "Professional LLC exceptions and online processing charges are separate.",
            ),
        )
        if entity == EntityType.LLC
        else (
            annual(
                "Annual report",
                "15th day of the fourth month following the close of the fiscal year.",
                None,
                "N.C. Gen. Stat. §§ 55-16-22, 55-1-22",
                "$25 paper or $18 statutory electronic fee; online processing charges "
                "are separate. Professional-corporation exceptions apply.",
            ),
        )
        if entity == EntityType.C_CORP
        else ()
    )
    penalty = (
        "$500 plus costs, historical fees/taxes, interest, and other applicable penalties."
        if entity == EntityType.LP
        else "$10 per day, capped at $1,000 for each year or partial year, plus historical "
        "fees/taxes, interest, and other penalties. The annual cap resets by applicable "
        "year; a single lifetime cap would understate exposure."
    )
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation=citation,
            notes="Local operations trigger screening. Interstate commerce, bank accounts, "
            "internal affairs, and orders accepted outside the state are listed safe harbors. "
            "An isolated transaction must be completed within six calendar months and not "
            "be repeated; calendar-month eligibility requires manual review, not a 180-day proxy.",
        ),
        filing_fee=Decimal("50" if entity == EntityType.LP else "250"),
        forms=(
            StateForm(
                "Application for registration as foreign limited partnership"
                if entity == EntityType.LP
                else "Application for Certificate of Authority",
                identifier,
                _SOS + application,
            ),
        ),
        qualification_penalty=unresolved_penalty(citation, penalty),
        annual_obligations=reports,
        consequences=(
            "Cannot maintain a state-court proceeding unless authority is obtained before trial.",
            "Failure to qualify does not invalidate contracts or prevent defending proceedings.",
            "LLP/LLLP annual reporting must not be imposed on an ordinary LP; "
            "separate tax obligations and entity-specific revocation rules still apply.",
        ),
        good_standing_evidence=(
            "Attach an original authenticated home-jurisdiction Certificate of Existence "
            "or similar document less than six months old; a photocopy is not accepted "
            "(B-09 item 10; L-09 item 8)."
            if entity != EntityType.LP
            else "LP-04 does not request an attached home-jurisdiction existence certificate. "
            "Supply the formation, general-partner and limited-partner-record information "
            "required by the form and § 59-902; registration fee is $50."
        ),
    )


REQUIREMENT = StateRequirement(
    state="NC",
    name="North Carolina",
    registered_agent=RegisteredAgentRequirement(
        citation="N.C. Gen. Stat. §§ 55-15-07, 57D-7-06, 59-902; Chapter 55D Article 4",
        notes="Maintain an eligible agent and registered office with a North Carolina "
        "street address; a separate mailing address can accompany the street address.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=tuple(
        source(
            f"North Carolina General Statutes Chapter {chapter}", _ROOT + f"Chapter_{chapter}.html"
        )
        for chapter in ("55", "55D", "57D", "59")
    )
    + tuple(
        source(f"North Carolina SOS application {identifier}", _SOS + path)
        for identifier, path in _APPLICATIONS.values()
    )
    + (
        source(
            "North Carolina SOS forms and fees",
            "https://www.sosnc.gov/forms/by_title/_Business_Registration",
        ),
    ),
    version="2026-10-11-official-forms-review",
    notes=(
        "Quoted filing fees are standard paper application fees confirmed by current "
        "SOS downloads. Optional electronic payment and expedited-service charges are "
        "excluded, not treated as zero. No queue duration is promised. Six-calendar-month "
        "isolated transactions remain manual because the model accepts days, not months.",
    ),
)
