"""New York foreign authority, publication, and biennial reporting requirements."""

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

_DOS = "https://dos.ny.gov/"
_FORMS = {
    EntityType.LLC: _DOS + "application-authority-foreign-limited-liability-companies",
    EntityType.C_CORP: _DOS + "application-authority-foreign-business-corporation",
    EntityType.LP: _DOS + "application-authority-foreign-limited-partnerships-0",
}
_SENATE = "https://www.nysenate.gov/legislation/laws/"
_BIENNIAL = _DOS + "biennial-statements-business-corporations-and-limited-liability-companies"


def _entity(entity: EntityType) -> EntityRequirement:
    citation = {
        EntityType.LLC: "N.Y. LLC Law §§ 802, 803, 808",
        EntityType.C_CORP: "N.Y. Business Corporation Law §§ 1301, 1304, 1312",
        EntityType.LP: "N.Y. Partnership Law §§ 121-902, 121-907",
    }[entity]
    publication = (
        "Within 120 days of filing authority, publish once a week for six successive "
        "weeks in two county-clerk-designated newspapers, one daily and one weekly. "
        "File the Certificate of Publication and affidavits with a separate $50 fee. "
        "Newspaper charges vary and are additional to the authority and certificate fees. "
        "Failure to complete publication can suspend business authority."
        if entity != EntityType.C_CORP
        else None
    )
    return EntityRequirement(
        entity_type=entity,
        qualification_citation=citation,
        threshold=QualificationThreshold(
            citation=citation,
            exempt_activities=(
                frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS})
                if entity != EntityType.LP
                else frozenset()
            ),
            notes="Regular local operations trigger screening. Corporation/LLC statutes "
            "expressly exclude maintaining bank accounts and internal meetings; do not "
            "import other states' interstate-commerce, solicitation, or isolated-transaction "
            "safe harbors automatically. LP safe-harbor questions require manual review.",
        ),
        filing_fee=Decimal(
            {EntityType.LLC: "250", EntityType.C_CORP: "225", EntityType.LP: "200"}[entity]
        ),
        forms=(StateForm("Application for Authority", citation, _FORMS[entity]),),
        qualification_penalty=unresolved_penalty(
            citation,
            "An unauthorized foreign entity cannot maintain a New York action until "
            "authorized; contracts and the ability to defend actions are preserved. "
            "No universal dollar sanction or unpaid-tax estimate is assumed.",
        ),
        annual_obligations=(
            (
                AnnualObligation(
                    name="Biennial Statement",
                    cycle="biennial",
                    due_rule="Every two years during the calendar month of the original "
                    "Application for Authority filing.",
                    fee=Decimal("9"),
                    citation="N.Y. Business Corporation Law § 408; LLC Law § 301(e); DOS guidance",
                    notes="A missed statement appears as past due on the status record. "
                    "This is not an annual fee and does not apply to an ordinary LP.",
                ),
            )
            if entity != EntityType.LP
            else ()
        ),
        initial_report=publication,
        consequences=(
            "Designate the Secretary of State as statutory process agent and provide "
            "a reliable forwarding address; a private registered agent is optional.",
            "A foreign corporation already conducting New York business must obtain "
            "State Tax Commission consent for its authority application.",
            "Separate New York tax filings and beneficial-ownership reporting must be "
            "reviewed independently of qualification and biennial statements.",
        ),
        good_standing_evidence="Attach a home-jurisdiction Certificate of Existence "
        "dated within one year; obtain any required agency consent for regulated activities.",
    )


REQUIREMENT = StateRequirement(
    state="NY",
    name="New York",
    registered_agent=RegisteredAgentRequirement(
        citation="N.Y. LLC Law §§ 301–302; Business Corporation Law §§ 304–305; "
        "Partnership Law § 121-104",
        notes="The Secretary of State is the statutory service-of-process agent. A private "
        "registered agent may be designated but is not mandatory. Maintain the required "
        "process-forwarding address; optional agents must satisfy entity-specific eligibility.",
        private_appointment_required=False,
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        *(
            source(f"New York DOS foreign {entity.value} application instructions", url)
            for entity, url in _FORMS.items()
        ),
        source("New York DOS biennial statements", _BIENNIAL),
        source(
            "New York DOS foreign LLC publication",
            _DOS + "certificate-publication-foreign-limited-liability-company-0",
        ),
        source("New York LLC safe harbors", _SENATE + "LLC/803"),
        source("New York optional LLC registered agent", _SENATE + "LLC/302"),
        source("New York optional corporate registered agent", _SENATE + "BSC/305"),
        source("New York LP statutory process agent", _SENATE + "PTR/121-104"),
        source("New York foreign LP authority and publication", _SENATE + "PTR/121-902"),
        source("New York foreign LLC unauthorized-business consequences", _SENATE + "LLC/808"),
        source(
            "New York foreign corporate unauthorized-business consequences", _SENATE + "BSC/1312"
        ),
        source("New York corporation qualification", _SENATE + "BSC/1301"),
        source("New York foreign LP unauthorized-business consequences", _SENATE + "PTR/121-907"),
    ),
    version="2026-10-11-official-source-review",
    verification_issues=(
        "Qualification screening does not decide tax nexus. Newspaper costs, tax "
        "consents, and current LLC transparency/reporting obligations require separate "
        "review; they are not included in the authority application fee.",
    ),
)
