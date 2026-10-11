"""Idaho rules reviewed against official statutes and filing guidance."""

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
        qualification_citation="Idaho Code § 30-21-502",
        threshold=QualificationThreshold(
            citation="Idaho Code § 30-21-505",
            isolated_transaction_without_day_limit=True,
            notes=(
                "Isolated transactions must not be in the course of similar transactions; no "
                "fixed day limit. Orders must be accepted outside Idaho. Owning property "
                "without more is listed."
            ),
        ),
        filing_fee=Decimal("100"),
        forms=(
            StateForm(
                "Foreign registration statement",
                "Foreign Registration",
                "https://archive.sos.idaho.gov/CORP/forms/FOREIGN/Foreign%20Reg%20Statement.pdf",
            ),
        ),
        qualification_penalty=unresolved_penalty(
            "Idaho Code § 30-21-502",
            (
                "The entity cannot maintain an Idaho action until registered. This provision "
                "states no fixed dollar penalty; any additional fees, taxes or sanctions require "
                "a separate assessment."
            ),
        ),
        annual_obligations=(
            AnnualObligation(
                name="Annual report",
                cycle="annual",
                due_rule=(
                    "By close of business on the final day of the registration anniversary month, "
                    "beginning one year after registration."
                ),
                fee=None,
                citation="Idaho Code § 30-21-213",
                notes=(
                    "Confirm the current report charge; an unverified amount is not represented as "
                    "zero."
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
            "The current SOS foreign registration FAQ requests a home-state certificate of "
            "existence/good standing dated within 90 days of filing. Confirm the attachment "
            "requirements for the entity type in the filing workflow."
        ),
    )


REQUIREMENT = StateRequirement(
    state="ID",
    name="Idaho",
    registered_agent=RegisteredAgentRequirement(
        citation="Idaho Code §§ 30-21-402, 30-21-404",
        notes=(
            "Maintain a consenting commercial or noncommercial registered agent in Idaho. "
            "Supply the commercial agent name or the noncommercial agent name and Idaho "
            "street and mailing addresses. Confirm eligibility under § 30-21-404."
        ),
    ),
    entity_rules={entity: _entity(entity) for entity in EntityType},
    sources=(
        source(
            "Idaho Code § 30-21-502 registration",
            "https://legislature.idaho.gov/statutesrules/idstat/title30/t30ch21/sect30-21-502/",
        ),
        source(
            "Idaho Code § 30-21-505 activity exclusions",
            "https://legislature.idaho.gov/statutesrules/idstat/title30/t30ch21/sect30-21-505/",
        ),
        source(
            "Idaho Code § 30-21-213 annual reports",
            "https://legislature.idaho.gov/statutesrules/idstat/Title30/T30CH21/SECT30-21-213/",
        ),
        source(
            "Idaho Code § 30-21-402 agent requirement",
            "https://legislature.idaho.gov/statutesrules/idstat/Title30/T30CH21/SECT30-21-402/",
        ),
        source(
            "Idaho Code § 30-21-404 agent designation",
            "https://legislature.idaho.gov/statutesrules/idstat/title30/t30ch21/sect30-21-404/",
        ),
        source("SOS business forms and fees", "https://sos.idaho.gov/business-forms/"),
        source(
            "SOS foreign registration FAQ", "https://sos.idaho.gov/business-resources/business-faq/"
        ),
    ),
    version="2026-10-11-batch3",
    notes=(
        (
            "The base foreign registration fee is $100. Paper/manual filing adds $20, "
            "totaling $120; optional expedited and payment charges are separate. Annual "
            "report fee is left unquantified pending explicit current fee confirmation."
        ),
    ),
)
