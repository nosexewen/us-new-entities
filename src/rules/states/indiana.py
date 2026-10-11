"""Indiana rules reviewed against official statutes and filing guidance."""

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
        qualification_citation="IC 23-0.5-5-2–23-0.5-5-3",
        threshold=QualificationThreshold(
            citation="IC 23-0.5-5-5",
            isolated_transaction_max_days=30,
            notes=(
                "Isolated transactions must be completed within 30 days and not be repeated "
                "like transactions; the current uniform code expressly retains this day "
                "limit."
            ),
        ),
        filing_fee=Decimal("125"),
        forms=(
            StateForm(
                "Foreign registration statement",
                "State Form 49459",
                "https://forms.in.gov/Download.aspx?id=17073",
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "IC 23-0.5-5-2(f)",
            (
                "Civil penalty of not more than $10,000 for unregistered business, collectible by "
                "the Attorney General. The statute does not multiply this maximum by years. "
                "Assessment and any other liabilities remain manual."
            ),
        ),
        annual_obligations=(
            AnnualObligation(
                name="Biennial report",
                cycle="biennial",
                due_rule=(
                    "Every two years on the SOS assigned schedule; INBiz states the registration "
                    "anniversary date with through-month-end filing before past due. Confirm the "
                    "assigned year in the business record."
                ),
                fee=Decimal("50"),
                citation="IC 23-0.5-2-13; IC 23-0.5-9-34; INBiz report guidance",
                notes=(
                    "$50 paper. Statutory electronic fee $20; published INBiz price $32; see noted "
                    "discrepancy."
                ),
            ),
        ),
        consequences=(
            (
                "Failure to qualify does not invalidate contracts or prevent defending "
                "proceedings; maintaining an action requires qualification."
            ),
        ),
        good_standing_evidence=(
            "Attach a certificate of existence issued by the proper home-jurisdiction "
            "authority within the last 60 days, as required by State Form 49459."
        ),
    )


REQUIREMENT = StateRequirement(
    state="IN",
    name="Indiana",
    registered_agent=RegisteredAgentRequirement(
        citation="IC 23-0.5-4-3; State Form 49459",
        notes=(
            "Designate a consenting commercial agent or an eligible noncommercial individual, "
            "general partnership, domestic filing entity or registered foreign entity. The "
            "form requires an Indiana street address for noncommercial agents, not a PO box. "
            "Provide and maintain a communications contact."
        ),
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source("Indiana Code 2026 Title 23", "https://iga.in.gov/laws/2026/ic/titles/23"),
        source(
            "INBiz business entity report guidance",
            "https://inbiz.in.gov/business-filings/business-entityreport",
        ),
        source(
            "SOS Foreign Registration, State Form 49459",
            "https://forms.in.gov/Download.aspx?id=17073",
        ),
    ),
    version="2026-10-11-batch3",
    notes=(
        (
            "The modeled $125 qualification fee is the paper fee. IC 23-0.5-9-26(a) "
            "states $75 for electronic foreign registration; confirm the actual INBiz "
            "checkout and any service charges. Special foreign master-series LLC charges "
            "are outside the ordinary LLC guide."
        ),
    ),
    review_disclosures=(
        (
            "Noted discrepancy, resolved by disclosure: IC 23-0.5-9-34(a)(1) states a $20 "
            "electronic biennial-report fee for for-profit entities; INBiz publishes $32 "
            "online. Both list $50 paper, which is the modeled report fee. The guide does "
            "not assume the difference is entirely a processing fee."
        ),
    ),
)
