"""Arkansas foreign entity rules with SOS fees and identified statutory reproductions."""

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

_SOS = "https://www.sos.arkansas.gov/"
_FORMS = _SOS + "business-commercial-services-bcs/forms-fees/"
_LLC = _FORMS + "llc/foreign-llc"
_CORP = _FORMS + "corporations/foreign-corporations"
_LP = _FORMS + "partnerships/lp-llp-lllp-foreign"
_JUSTIA = "https://law.justia.com/codes/arkansas/title-4/subtitle-3/"


def _entity(entity: EntityType) -> EntityRequirement:
    llc = entity == EntityType.LLC
    lp = entity == EntityType.LP
    citation = (
        "Ark. Code §§ 4-38-902, 4-38-905, 4-38-913"
        if llc
        else ("Ark. Code § 4-47-902; SOS form LPF-01" if lp else "Ark. Code §§ 4-27-1501–4-27-1503")
    )
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation="Ark. Code § 4-38-905" if llc else citation,
            **(
                {"exempt_activities": frozenset()}
                if lp
                else {"isolated_transaction_without_day_limit": True}
                if llc
                else {"isolated_transaction_max_days": 30}
            ),
            notes="LLC isolated transactions not in the course of similar transactions "
            "have no fixed day limit under current Chapter 38. Corporate isolated "
            "transactions must finish within 30 days and not be repeated. Both list bank "
            "accounts, internal affairs, interstate commerce and orders accepted outside "
            "Arkansas. LP exemptions require separate review.",
        ),
        filing_fee=Decimal("300"),
        forms=(
            StateForm(
                "Application for Certificate of Registration"
                if llc
                else "Application for Certificate of Authority",
                "FL-01" if llc else "LPF-01" if lp else "F-01",
                _SOS
                + "uploads/bcs/"
                + (
                    "FL-01_1_1.pdf"
                    if llc
                    else "Foreign_Partnership_LFP-01V2.pdf"
                    if lp
                    else "F-01_2.pdf"
                ),
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "Ark. Code § 4-38-913(d)–(f)"
            if llc
            else "Ark. Code § 4-27-1502(d)"
            if not lp
            else citation,
            "LLC: historical fees and penalties plus a civil penalty up to $5,000 for "
            "each twelve-month period or part, measured from first doing business until "
            "registration (§ 4-38-913). Corporation: historical fees and penalties plus "
            "up to $5,000 for each year or partial year (§ 4-27-1502). Entity-specific "
            "periods, court assessments, interest and costs remain manual."
            if not lp
            else "Review LP sanctions separately under Chapter 47; LLC and "
            "corporation $5,000 schedules are not automatically applied to LPs.",
        ),
        annual_obligations=(
            annual(
                "Annual limited partnership report" if lp else "Annual franchise tax report",
                "Annually; confirm the deadline on the current LP-AR form."
                if lp
                else "May 1 annually; confirm the first filing year against registration "
                "and tax records.",
                "0" if lp else "150" if llc else None,
                "SOS foreign-partnership report schedule"
                if lp
                else "Ark. Code §§ 26-54-104, 26-54-105; SOS franchise-tax forms",
                "LP annual reports are listed without a filing fee; ordinary LPs are not "
                "assigned the LLC franchise tax."
                if lp
                else "LLC annual franchise tax is $150. Corporation tax is capital-based (0.3% "
                "of the applicable Arkansas base), minimum $150 for stock corporations; "
                "corporations without authorized stock pay $300. Late penalties and interest "
                "are separate, not included in qualification sanctions.",
            ),
        ),
        consequences=(
            "An unregistered LLC or corporation cannot maintain state-court proceedings "
            "until qualified; contracts remain valid and defending proceedings is permitted.",
            "State enforcement can include civil penalties and injunctions. Keep franchise "
            "taxes current, including final reports when withdrawing or cancelling.",
        ),
        good_standing_evidence="Attach the home-jurisdiction certificate of existence/good "
        "standing dated within 30 days of filing under the SOS application and guide. "
        "LPs also follow the certified formation-document requirements in the SOS guide.",
    )


REQUIREMENT = StateRequirement(
    state="AR",
    name="Arkansas",
    registered_agent=RegisteredAgentRequirement(
        citation="Arkansas SOS forms FL-01, F-01 and Doing Business in Arkansas 2025; Chapter 4-20",
        notes="Maintain an eligible registered agent at a physical Arkansas street address "
        "for service. A PO box alone is not a registered office.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=tuple(
        source(citation, url)
        for citation, url in (
            ("SOS foreign LLC forms and fees", _LLC),
            ("SOS foreign corporation forms and fees", _CORP),
            ("SOS foreign partnership forms and fees", _LP),
            (
                "SOS Doing Business in Arkansas 2025",
                _SOS + "uploads/bcs/DoingBusinessInArkansas2025.pdf",
            ),
            ("SOS foreign LLC application FL-01", _SOS + "uploads/bcs/FL-01_1_1.pdf"),
            ("SOS foreign corporation application F-01", _SOS + "uploads/bcs/F-01_2.pdf"),
            ("SOS 2026 corporation franchise tax report", _SOS + "uploads/bcs/Corp1_FT_2026.pdf"),
            (
                "Ark. Code § 4-38-905 (Justia reproduction)",
                _JUSTIA + "chapter-38/subchapter-9/section-4-38-905/?",
            ),
            (
                "Ark. Code § 4-38-913 (Justia reproduction)",
                _JUSTIA + "chapter-38/subchapter-9/section-4-38-913/",
            ),
            (
                "Ark. Code § 4-27-1501 (Justia reproduction)",
                _JUSTIA + "chapter-27/subchapter-15/part-a/section-4-27-1501/",
            ),
            (
                "Ark. Code § 4-27-1502 (Justia reproduction)",
                _JUSTIA + "chapter-27/subchapter-15/part-a/section-4-27-1502/",
            ),
        )
    ),
    version="2026-10-11-accepted-statutory-review",
    verification_issues=(),
    review_disclosures=(
        "Review acceptance: at the user's direction, the reviewed Justia statutory "
        "citations are sufficient verification for Arkansas statutory rules and "
        "franchise tax requirements. The primary review flag is satisfied. Justia "
        "remains identified as a third-party statutory reproduction; the failed "
        "official Act 1041 retrieval is retained in the verification log. Franchise "
        "tax figures also rely on the reviewed SOS fee schedules and 2026 tax form. "
        "Older Chapter 32 references do not override current Chapter 38 rules.",
    ),
    notes=(
        "The $300 qualification fee is the paper fee. LLCs and corporations may file "
        "online for $270; foreign LPs are listed as paper-only $300. Tax, publication "
        "and optional services are separate. LP statutory exemptions and sanctions "
        "are outside this LLC/C-Corp review and remain manual.",
    ),
)
