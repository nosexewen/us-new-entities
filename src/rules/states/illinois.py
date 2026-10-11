"""Illinois entity-specific qualification fees, thresholds, and annual reports."""

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

_SOS = "https://www.ilsos.gov/"
_PDF = _SOS + "content/dam/publications/pdf_publications/"
_ILGA = "https://ilga.gov/documents/legislation/ilcs/documents/"
_LLC_ACT = "https://www.ilga.gov/legislation/ILCS/details?ActID=2290&ActName=Limited+Liability+Company+Act.&ChapAct=805+ILCS+180%2F"


def _entity(entity: EntityType) -> EntityRequirement:
    citation, form, identifier, days, report_fee, penalty = {
        EntityType.LLC: (
            "805 ILCS 180/45-5, 45-45, 45-47",
            "llc455.pdf",
            "LLC 45.5",
            120,
            "75",
            "After failing to obtain admission within 60 days of beginning business, "
            "$2,000 plus $100 for each month or fraction of continued unauthorized business, "
            "plus historical fees and penalties. Accrual and arrears require manual assessment.",
        ),
        EntityType.C_CORP: (
            "805 ILCS 5/13.05, 13.15, 13.70, 13.75",
            "bca1315.pdf",
            "BCA 13.15",
            120,
            "75",
            "After failure to apply within 60 days, the greater of 10% of filing/license "
            "fees and franchise taxes or $200 plus $5 per month or fraction, plus historical "
            "fees, applicable taxes, and penalties. Franchise-tax exemptions and allocation "
            "inputs must be reviewed; do not apply the LLC sanction to a corporation.",
        ),
        EntityType.LP: (
            "805 ILCS 215/902, 903, 907",
            "lp902.pdf",
            "LP 902",
            30,
            "100",
            "No fixed dollar sanction is inferred from § 907. Historical fees, "
            "applicable penalties, and any enforcement assessment require manual review.",
        ),
    }[entity]
    exemptions = {Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS, Activity.SOLICITATION}
    if entity == EntityType.LP:
        exemptions.add(Activity.INTERSTATE_COMMERCE)
    triggers = {
        Activity.OFFICE,
        Activity.LOCAL_SERVICES,
        Activity.RETAIL,
        Activity.INTRASTATE_BUSINESS,
    }
    if entity == EntityType.LP:
        triggers.add(Activity.INCOME_PRODUCING_PROPERTY)
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation=citation,
            trigger_activities=frozenset(triggers),
            exempt_activities=frozenset(exemptions),
            isolated_transaction_max_days=days,
            notes=f"Local operations trigger screening. An isolated transaction must finish "
            f"within {days} days and not be part of repeated transactions. LP ownership "
            "of income-producing real or tangible property is a trigger unless a statutory "
            "exclusion applies. Do not assume the same property rule for corporations/LLCs.",
        ),
        filing_fee=Decimal("150"),
        forms=(
            StateForm(
                "Application for Authority/Admission to Transact Business", identifier, _PDF + form
            ),
        ),
        qualification_penalty=unresolved_penalty(citation, penalty),
        annual_obligations=(
            annual(
                "Annual report",
                "Before the first day of the anniversary month; LP reports are delivered "
                "within the preceding 60 days. Check any approved extended corporate filing month.",
                report_fee,
                "805 ILCS 180/50-1, 50-10; 805 ILCS 5/14.05; 805 ILCS 215/210, 1302",
                "Late penalties and administrative revocation are separate from the "
                "base report fee; corporate tax/exemption inputs need separate review.",
            ),
        ),
        consequences=(
            "Cannot maintain an Illinois proceeding without authority/admission; "
            "contract validity and the ability to defend proceedings are preserved.",
            "The $150 application amount is a base filing fee, not a guaranteed corporate "
            "all-in total; additional fees, applicable franchise tax, "
            "or sanctions may be assessed.",
        ),
        good_standing_evidence=(
            "Attach home-jurisdiction certified articles as amended, authenticated within "
            "90 days, for a foreign corporation."
            if entity == EntityType.C_CORP
            else "Confirm home-jurisdiction certification requirements in the current "
            "entity-specific application; restore domestic existence before foreign filing."
        ),
    )


REQUIREMENT = StateRequirement(
    state="IL",
    name="Illinois",
    registered_agent=RegisteredAgentRequirement(
        citation="805 ILCS 5/5.05; 805 ILCS 180/1-35; 805 ILCS 215/114",
        notes="Maintain an eligible agent and Illinois street-address registered office. "
        "A PO box alone is not an acceptable registered office.",
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source("Illinois SOS LLC forms and fees", _SOS + "publications/business-services/llc.html"),
        source(
            "Illinois SOS corporation forms and fees",
            _SOS + "publications/business-services/dfc.html",
        ),
        source("Illinois SOS LP forms and fees", _SOS + "publications/business-services/lp.html"),
        source("Illinois foreign corporation authority application", _PDF + "bca1315.pdf"),
        source("Illinois foreign LLC admission application", _PDF + "llc455.pdf"),
        source("Illinois LLC Act", _LLC_ACT),
        source(
            "Illinois corporation unauthorized-business sanctions", _ILGA + "080500050K13.70.htm"
        ),
        source("Illinois corporation safe harbors", _ILGA + "080500050K13.75.htm"),
        source("Illinois LP safe harbors", _ILGA + "080502150K903.htm"),
        source("Illinois LP annual report", _ILGA + "080502150K210.htm"),
        source(
            "Illinois SOS corporate annual-report instructions",
            _SOS + "departments/business-services/annual-reports/corp-instructions.html",
        ),
        source("Illinois LP unauthorized-business consequences", _ILGA + "080502150K907.htm"),
    ),
    version="2026-10-11-official-source-review",
    verification_issues=(
        "Corporate franchise-tax exemptions, historical allocation, late-payment "
        "calculations, and LLC/LP certificate freshness must be confirmed from the "
        "current filing instructions; sanctions remain unquantified in the calculator.",
    ),
)
