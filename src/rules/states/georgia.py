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
_LLC_PENALTY = (
    "https://law.justia.com/codes/georgia/title-14/chapter-11/article-7/section-14-11-711/"
)
_LLC_FEES = (
    "https://law.justia.com/codes/georgia/title-14/chapter-11/article-11/section-14-11-1101/"
)
_FEES = "https://sos.ga.gov/sites/default/files/forms/Reference%20-%20Filing%20Fees_0.pdf"


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
                "in this batch and require manual review.",
            ),
        ),
        filing_fee=Decimal("235"),
        forms=(StateForm("Application for Certificate of Authority", identifier, _GUIDE),),
        qualification_penalty=unresolved_penalty(
            (
                "O.C.G.A. § 14-11-711(c)(1)–(2); § 14-11-1101(b)"
                if entity == EntityType.LLC
                else "Georgia SOS foreign-registration FAQ; " + citation
            ),
            "SOS guidance imposes a $500 late-qualification penalty after more than 30 days "
            "of business without registration. LLCs and LPs also owe the fees that would "
            "have been imposed if registered. The fee schedule's recurring LLC row "
            "conflicts with the FAQ/administrative rule; neither a one-time LLC total "
            "nor annual repetition is calculated without applicant filing history and "
            "entity-specific assessment. For LLCs, O.C.G.A. § 14-11-711(c)(2) states "
            "$500 after 30 days with no annual multiplier; subsection (c)(1) adds "
            "historical fees, and § 14-11-1101(b) directs penalty collection. "
            "Confirm entity-specific assessment and arrears before calculating.",
        ),
        annual_obligations=(
            annual(
                "Annual registration",
                "January 1–April 1, starting in the year following foreign qualification.",
                "60",
                (
                    "O.C.G.A. § 14-11-1101(a)(14)–(15); Georgia SOS annual-registration guide"
                    if entity == EntityType.LLC
                    else "Georgia SOS annual-registration guide"
                ),
                "$50 filing fee plus $10 service charge for both online and paper, "
                "under the schedule effective September 6, 2025; $25 late-registration "
                "penalty. Failure to file can lead to revocation.",
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
        source(
            "O.C.G.A. § 14-11-711(c)(1)–(2), Justia (accepted for statutory verification)",
            _LLC_PENALTY,
        ),
        source(
            "O.C.G.A. § 14-11-1101(a)(15), Justia (accepted for statutory verification)",
            _LLC_FEES,
        ),
        source("Georgia SOS foreign entity registration guide", _GUIDE),
        source("Georgia SOS business division FAQ", _FAQ),
        source("Georgia SOS annual-registration guide", _ANNUAL),
        source("Georgia SOS fee schedule effective September 6, 2025", _FEES),
        source("Georgia LLC foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-21"),
        source("Georgia corporation foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-3"),
        source("Georgia LP foreign filing rules", "https://rules.sos.ga.gov/gac/590-7-12"),
    ),
    version="2026-10-11-accepted-statutory-review",
    review_disclosures=(
        "Noted discrepancy — foreign LLC late-qualification penalty: "
        "O.C.G.A. § 14-11-711(c) is reproduced as $500 after 30 days plus historical "
        "fees, without an annual multiplier; this is also the assessment described "
        "by SOS Rule 590-7-21-.07 and the FAQ. The September 6, 2025 administrative "
        "fee schedule additionally labels an LLC row $500 per year or part-year. "
        "Both formulations are disclosed; this fee conflict is resolved by disclosure, "
        "not by claiming the sources agree. The Justia reproductions of O.C.G.A. "
        "§ 14-11-711(c)(2) and § 14-11-1101(a)(15) are accepted for statutory "
        "verification at the user's direction. Applicant-specific historical fees "
        "and the disclosed assessment discrepancy remain unquantified.",
        "Filing-fee distinction: the statutory base figures are qualification $225 "
        "and annual registration $50. The administrative schedule adds a $10 service "
        "charge to each: $235 and $60, respectively, for both online and paper filing.",
    ),
    verification_issues=(),
    notes=(
        "Review acceptance: statutory and safe-harbor audit flags are satisfied at "
        "the user's direction. Justia is a third-party statutory reproduction, not "
        "the official Lexis publication. Penalty provisions do not establish "
        "transacting-business exemptions; safe harbors remain manually assessed "
        "and no automatic exemption has been added.",
        "The fee schedule effective September 6, 2025 resolves the filing-channel "
        "fee discrepancy: qualification $225+$10=$235, annual registration "
        "$50+$10=$60, amended annual registration $20+$10=$30 for both channels. "
        "Its service-charge note expressly includes the charge in the grid totals. "
        "Older base-only portal/FAQ quotes are not current all-in prices.",
        "Official administrative rules independently confirm the $500 LLC/corporate "
        "late-qualification assessment after 30 days, additional charges and "
        "LLC/LP certificate exceptions; numeric historical totals still need applicant facts.",
    ),
)
