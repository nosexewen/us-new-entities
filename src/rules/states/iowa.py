"""Iowa rules reviewed against official statutes and filing guidance."""

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

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="Iowa Code §§ 489.902–489.903",
    threshold=QualificationThreshold(
        citation="Iowa Code § 489.905",
        isolated_transaction_without_day_limit=True,
        notes=(
            "Isolated transactions must not be in the course of similar transactions; "
            "current § 489.905 has no fixed day limit. Owning, protecting and maintaining "
            "property is listed; operating activities require their own facts."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign registration statement",
            "635_0010",
            "https://sos.iowa.gov/business/pdf/635_0010.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Iowa Code §§ 489.902, 489.912",
        (
            "Section 489.902 bars maintaining proceedings until registered but states no "
            "fixed monetary penalty. Section 489.912 permits an Attorney General action to "
            "enjoin unregistered business. Other fees, taxes and sanctions require manual "
            "assessment."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Biennial report",
            cycle="biennial",
            due_rule=(
                "January 1 through April 1 of each odd-numbered year, starting the first "
                "odd-numbered year after the registration calendar year."
            ),
            fee=Decimal("30"),
            citation="Iowa Code § 489.212; SOS forms and fees",
            notes="$30 online or $45 paper. Separate taxes are not included.",
        ),
    ),
    consequences=(
        (
            "Failure to qualify does not invalidate contracts or prevent defending "
            "proceedings; maintaining an action requires qualification."
        ),
    ),
    good_standing_evidence=(
        "Attach an authenticated certificate of existence or similar document dated no "
        "earlier than 90 days before filing."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Iowa Code §§ 490.1502–490.1503",
    threshold=QualificationThreshold(
        citation="Iowa Code § 490.1505",
        isolated_transaction_without_day_limit=True,
        notes=(
            "Current § 490.1505 lists isolated transactions outside the course of similar "
            "transactions, without a fixed day limit. Do not apply the former 30-day "
            "test."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign registration statement",
            "635_0110a",
            "https://sos.iowa.gov/business/pdf/635_0110a.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Iowa Code § 490.1502",
        (
            "Registration is required to maintain an Iowa court proceeding. This section "
            "states no fixed monetary penalty; assess any other applicable fees, taxes or "
            "sanctions manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Biennial report",
            cycle="biennial",
            due_rule=(
                "January 1 through April 1 of each even-numbered year, starting the first "
                "even-numbered year after the registration calendar year."
            ),
            fee=Decimal("60"),
            citation="Iowa Code § 490.1621; SOS forms and fees",
            notes=(
                "$60 for-profit corporation report fee; the LLC $30 online/$45 paper prices do "
                "not apply."
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
        "Attach an authenticated certificate of existence or similar document issued "
        "within 90 days before filing."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Iowa SOS foreign LP application and fee schedule",
    threshold=QualificationThreshold(
        citation="Iowa Chapter 488 exemptions require manual statutory review",
        exempt_activities=frozenset(),
        notes=(
            "Only official LP application and $100 registration fee are populated; LLC "
            "and corporation exemptions and report cycles are not applied to LPs."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "635_0902",
            "https://sos.iowa.gov/business/pdf/635_0902.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Iowa Chapter 488 sanctions require manual review",
        (
            "LP sanctions and reporting applicability are outside this LLC/C-Corp statutory "
            "review; obtain an entity-specific assessment."
        ),
    ),
    consequences=(
        ("LP remedies and litigation consequences require an entity-specific statutory review."),
    ),
    good_standing_evidence=(
        "Confirm the home-jurisdiction evidence required by the current entity-specific "
        "filing instructions."
    ),
)

REQUIREMENT = StateRequirement(
    state="IA",
    name="Iowa",
    registered_agent=RegisteredAgentRequirement(
        citation="Iowa Code §§ 489.115, 490.501; foreign registration forms",
        notes=(
            "Maintain an Iowa registered agent and street address for service. LLC "
            "designation affirms consent and requires an Iowa place of business. A "
            "corporation must maintain its registered office and an eligible agent as "
            "specified in § 490.501."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Iowa Code § 490.1503 corporate registration and certificate",
            "https://www.legis.iowa.gov/docs/code/490.1503.pdf",
        ),
        source("Iowa Code 2026 Chapter 489", "https://www.legis.iowa.gov/docs/code/489.pdf"),
        source(
            "Iowa Code § 490.1502 registration", "https://www.legis.iowa.gov/docs/code/490.1502.pdf"
        ),
        source(
            "Iowa Code § 490.1505 activity exclusions",
            "https://www.legis.iowa.gov/docs/code/490.1505.pdf",
        ),
        source(
            "Iowa Code § 490.1621 biennial reports",
            "https://www.legis.iowa.gov/docs/code/490.1621.pdf",
        ),
        source(
            "SOS LLC foreign registration form 635_0010",
            "https://sos.iowa.gov/business/pdf/635_0010.pdf",
        ),
        source(
            "SOS corporate foreign registration form 635_0110a",
            "https://sos.iowa.gov/business/pdf/635_0110a.pdf",
        ),
        source(
            "SOS business entity forms and fees",
            "https://sos.iowa.gov/businesses/business-entity-forms-and-fees",
        ),
        source(
            "SOS biennial report filing instructions",
            "https://help.sos.iowa.gov/how-do-i-file-biennial-report",
        ),
        source(
            "Iowa Code § 490.501 agent requirement",
            "https://www.legis.iowa.gov/docs/code/490.501.pdf",
        ),
    ),
    version="2026-10-11-batch3",
    notes=(
        (
            "Qualification costs $100 for each requested entity type. LLC reports are due "
            "in odd-numbered years; corporation reports in even-numbered years. Current "
            "LLC reporting section is § 489.212, and corporation reporting section is § "
            "490.1621; obsolete numbering and 30-day corporate isolated-transaction "
            "limits are not used."
        ),
    ),
    review_disclosures=(
        (
            "This batch verifies LLC and C-Corp statutory rules. LP entries contain "
            "official filing fees and forms only; LP exemptions, sanctions and reporting "
            "require a separate statutory review and are screened manually."
        ),
    ),
)
