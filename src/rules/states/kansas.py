"""Kansas foreign qualification rules from official statutory and filing sources."""

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
    qualification_citation="K.S.A. 17-7931",
    threshold=QualificationThreshold(
        citation="K.S.A. 17-7932",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate."
        ),
    ),
    filing_fee=Decimal("115"),
    forms=(
        StateForm(
            "Application for registration",
            "FA",
            "https://sos.ks.gov/forms/business_services/FA.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "K.S.A. 17-76,126",
        (
            "An unregistered LLC cannot maintain proceedings until registered and "
            "historical fees and penalties are paid. For corporations, historical "
            "taxes, fees and penalties must also be paid. The reviewed provisions do "
            "not specify a fixed qualification penalty; assess arrears manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Information report",
            cycle="biennial",
            due_rule=(
                "By April 15 in years matching the odd/even parity of the Kansas foreign "
                "registration application year; confirm the initial report year in the SOS "
                "record."
            ),
            fee=Decimal("90"),
            citation="K.S.A. 17-76,139(d)",
            notes=(
                "$90 online or $110 paper per the SOS information report form. Historical "
                "reports may be required with a delayed foreign application."
            ),
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
        "Provide the statement under penalty of perjury that the entity exists in "
        "good standing in its home jurisdiction, required by current K.S.A. "
        "17-7931(d). Do not require the repealed 90-day home-state certificate "
        "attachment."
    ),
)

_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="K.S.A. 17-7931",
    threshold=QualificationThreshold(
        citation="K.S.A. 17-7932",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate."
        ),
    ),
    filing_fee=Decimal("115"),
    forms=(
        StateForm(
            "Application for registration",
            "FA",
            "https://sos.ks.gov/forms/business_services/FA.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "K.S.A. 17-7307",
        (
            "An unregistered LLC cannot maintain proceedings until registered and "
            "historical fees and penalties are paid. For corporations, historical "
            "taxes, fees and penalties must also be paid. The reviewed provisions do "
            "not specify a fixed qualification penalty; assess arrears manually."
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Information report",
            cycle="biennial",
            due_rule=(
                "By April 15 in years matching the odd/even parity of the Kansas foreign "
                "registration application year; confirm the initial report year in the SOS "
                "record."
            ),
            fee=Decimal("90"),
            citation="K.S.A. 17-7505",
            notes=(
                "$90 online or $110 paper per the SOS information report form. Historical "
                "reports may be required with a delayed foreign application."
            ),
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
        "Provide the statement under penalty of perjury that the entity exists in "
        "good standing in its home jurisdiction, required by current K.S.A. "
        "17-7931(d). Do not require the repealed 90-day home-state certificate "
        "attachment."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="K.S.A. 17-7931",
    threshold=QualificationThreshold(
        citation="K.S.A. 17-7932",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be in a "
            "course of repeated like transactions. Orders must require acceptance "
            "outside the state; tax and regulatory nexus are separate."
        ),
    ),
    filing_fee=Decimal("115"),
    forms=(
        StateForm(
            "Application for registration",
            "FA",
            "https://sos.ks.gov/forms/business_services/FA.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "K.S.A. 17-7931; LP sanctions require manual review",
        (
            "LP sanctions and reporting require separate entity-specific review; do not "
            "apply LLC or corporate penalties automatically."
        ),
    ),
    consequences=(
        ("Authority, court-access remedies and other consequences require separate LP review."),
    ),
    good_standing_evidence=(
        "Provide the statement under penalty of perjury that the entity exists in "
        "good standing in its home jurisdiction, required by current K.S.A. "
        "17-7931(d). Do not require the repealed 90-day home-state certificate "
        "attachment."
    ),
)

REQUIREMENT = StateRequirement(
    state="KS",
    name="Kansas",
    registered_agent=RegisteredAgentRequirement(
        citation="K.S.A. 17-7925, 17-7931(f); SOS FA registered-office instructions",
        notes=(
            "Maintain a resident agent and Kansas registered street address where the "
            "agent may regularly be present. The agent may be an individual, a "
            "Kansas-registered business, or the business itself as allowed by the FA "
            "instructions. A PO box does not suffice."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "K.S.A. 17-7937 Attorney General injunction",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_079_0037.html",
        ),
        source(
            "Kansas SOS foreign corporation information report IFP",
            "https://sos.ks.gov/forms/business_services/IFP.pdf",
        ),
        source(
            "K.S.A. 17-7925 resident agent",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_079_0025.html",
        ),
        source(
            "K.S.A. 17-7931 foreign covered entity registration",
            "https://www.ksrevisor.gov/statutes/chapters/ch17/017_079_0031.html",
        ),
        source(
            "K.S.A. 17-7932 activity exclusions",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_079_0032.html",
        ),
        source(
            "K.S.A. 17-76,126 unregistered LLC proceedings",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_076_0126.html",
        ),
        source(
            "K.S.A. 17-7307 unregistered corporation proceedings",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_073_0007.html",
        ),
        source(
            "K.S.A. 17-76,139 LLC biennial reports",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_076_0139.html",
        ),
        source(
            "K.S.A. 17-7505 foreign corporation biennial reports",
            "https://ksrevisor.gov/statutes/chapters/ch17/017_075_0005.html",
        ),
        source(
            "Kansas Register regulations effective February 27, 2026",
            "https://sos.ks.gov/publications/register/Volume-45/Issues/Issue-07/02-12-26-53865.html",
        ),
        source("SOS foreign application FA", "https://sos.ks.gov/forms/business_services/FA.pdf"),
        source(
            "SOS LLC information report ILC", "https://sos.ks.gov/forms/business_services/ILC.pdf"
        ),
    ),
    version="2026-10-11-batch4",
    notes=(
        "The Attorney General may seek an injunction against unregistered foreign covered "
        "entities under K.S.A. 17-7937.",
        (
            "SOS form FA lists $115 for all foreign businesses. Information reports "
            "are biennial, not annual; modeled $90 is the online price, while paper "
            "costs $110. Kansas agricultural ownership and special business rules "
            "require separate review."
        ),
    ),
    review_disclosures=(
        (
            "Noted discrepancy, resolved by disclosure: the February 27, 2026 "
            "regulations list a $100 foreign entity application base in K.A.R. "
            "7-17-1, plus $10 information/services and $5 technology for paper "
            "filing, consistent with FA total $115. K.A.R. 7-50-1 separately lists "
            "a $75 foreign LLC application/recording fee. The guide uses the "
            "current FA $115 charge and preserves the $75 regulatory figure for "
            "confirmation with SOS, rather than silently treating them as "
            "identical."
        ),
        (
            "LP qualification and activity screening use the reviewed "
            "covered-entity statute. LP sanctions and report applicability remain "
            "outside this LLC/C-Corp review."
        ),
    ),
)
