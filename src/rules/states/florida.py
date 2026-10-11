"""Florida entity-type rules, including statutory annual report revocation dates."""

from datetime import date
from decimal import Decimal

from ...models import (
    Activity,
    AnnualObligation,
    EntityRequirement,
    EntityType,
    LegalSource,
    PenaltyPeriod,
    PenaltyPolicy,
    QualificationThreshold,
    RegisteredAgentRequirement,
    StateForm,
    StateRequirement,
)

_STATUTES = "https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL="
_LLC = _STATUTES + "0600-0699/0605/0605.html"
_CORP = _STATUTES + "0600-0699/0607/0607.html"
_LP = _STATUTES + "0600-0699/0620/0620.html"
_FORMS = "https://dos.fl.gov/sunbiz/forms/"
_REPORTS = "https://dos.fl.gov/sunbiz/manage-business/efile/annual-report/"
_VERIFIED = date(2026, 10, 10)
_GUIDANCE_REVIEWED = date(2026, 10, 11)
_PROPERTY_TRIGGERS = frozenset(
    {
        Activity.OFFICE,
        Activity.LOCAL_SERVICES,
        Activity.RETAIL,
        Activity.INTRASTATE_BUSINESS,
        Activity.INCOME_PRODUCING_PROPERTY,
    }
)


def _annual_report(fee: str, citation: str, revocation_citation: str) -> AnnualObligation:
    return AnnualObligation(
        name="Annual report and supplemental corporate fee",
        cycle="annual",
        due_rule=(
            "January 1–May 1, first due in the calendar year after foreign authorization, "
            "then each calendar year."
        ),
        fee=Decimal(fee),
        citation=citation + "; Fla. Stat. § 607.193",
        late_penalty=PenaltyPolicy(
            citation="Fla. Stat. § 607.193(2)(b)",
            description=(
                "$400 once per annual report when the supplemental corporate fee is "
                "remitted after May 1. The statutory reinstatement exception must be "
                "checked separately; this calculator models an ordinary late filing."
            ),
            amount_min=Decimal("400.00"),
            amount_max=Decimal("400.00"),
        ),
        notes=(
            "Includes the $88.75 supplemental corporate fee. Revocation and reinstatement "
            f"are governed separately by {revocation_citation}; missed report fees are "
            "not interest compounded with qualification sanctions."
        ),
    )


def _qualification_penalty(citation: str, *, court_ordered: bool) -> PenaltyPolicy:
    return PenaltyPolicy(
        citation=citation,
        description=(
            "$500–$1,000 for each year or part of unqualified business, plus fees and "
            "penalties that would have been due. Annual periods in this estimate use "
            "anniversaries; the collecting authority must confirm the assessment basis."
        ),
        amount_min=Decimal("500.00"),
        amount_max=Decimal("1000.00"),
        period=PenaltyPeriod.STARTED_YEAR,
        assessment="court_ordered_only" if court_ordered else "statutory_department_collected",
        unquantified_components=(
            "Past filing/report fees and penalties must be assessed separately",
        ),
    )


_EXISTENCE = (
    "Attach a certificate of existence or similar official domestic-jurisdiction "
    "record authenticated no more than 90 days before delivery. Resolve forfeiture "
    "or revocation and obtain acceptable current existence evidence before filing."
)
_REVOCATION = (
    "An annual report not delivered by 5 p.m. Eastern on the third Friday in September "
    "is a revocation ground; foreign authority is revoked on the fourth Friday in September."
)

REQUIREMENT = StateRequirement(
    state="FL",
    name="Florida",
    registered_agent=RegisteredAgentRequirement(
        citation="Fla. Stat. §§ 605.0113, 607.1507, 620.1114",
        notes=(
            "A Florida street address and eligible resident individual or authorized entity "
            "are required. The agent's address must equal the registered office address. "
            "Initial agent written acceptance is part of the foreign application."
        ),
    ),
    entity_rules={
        EntityType.LLC: EntityRequirement(
            entity_type=EntityType.LLC,
            qualification_citation="Fla. Stat. § 605.0902",
            threshold=QualificationThreshold(
                citation="Fla. Stat. §§ 605.0902, 605.0905",
                trigger_activities=_PROPERTY_TRIGGERS,
                isolated_transaction_max_days=30,
                notes=(
                    "An isolated transaction must finish within 30 days and not be part "
                    "of repeated like transactions. Bare ownership is exempt, but "
                    "income-producing real or tangible personal property constitutes "
                    "transacting business under § 605.0905(3), subject to the listed "
                    "subsection (1) exemptions. Unspecified property activity needs review."
                ),
            ),
            filing_fee=Decimal("125.00"),
            forms=(
                StateForm(
                    "Application by Foreign Limited Liability Company for Authorization "
                    "to Transact Business in Florida",
                    "foreign-llc-authorization",
                    _FORMS + "limited-liability-company/",
                ),
            ),
            qualification_penalty=_qualification_penalty(
                "Fla. Stat. § 605.0904(7)",
                court_ordered=False,
            ),
            annual_obligations=(
                _annual_report(
                    "138.75",
                    "Fla. Stat. §§ 605.0212, 605.0213",
                    "Fla. Stat. § 605.0908",
                ),
            ),
            good_standing_evidence=_EXISTENCE + " See § 605.0902(2).",
            consequences=(
                "Cannot maintain an action until authority is obtained (§ 605.0904).",
                "Failure to qualify does not invalidate contracts or prevent defending an action.",
                _REVOCATION + " See § 605.0908(1)(a), (2).",
                "Domestic dissolution or inactivity can support foreign revocation "
                "(§ 605.0908(1)(f)).",
                "Missing registered agent has a separate court-ordered $5/day, $500 cap "
                "(§ 605.0113(5)).",
            ),
        ),
        EntityType.C_CORP: EntityRequirement(
            entity_type=EntityType.C_CORP,
            qualification_citation="Fla. Stat. §§ 607.1501, 607.1503",
            threshold=QualificationThreshold(
                citation="Fla. Stat. § 607.1501",
                isolated_transaction_max_days=30,
                notes=(
                    "An isolated transaction must finish within 30 days and not be part "
                    "of repeated like transactions. Maintaining bank accounts, internal "
                    "affairs, interstate commerce, and orders accepted outside Florida "
                    "are safe harbors; owning/protecting property without more is exempt."
                ),
            ),
            filing_fee=Decimal("70.00"),
            forms=(
                StateForm(
                    "Application by Foreign Corporation for Authorization to Transact "
                    "Business in Florida",
                    "foreign-profit-corporation-authorization",
                    _FORMS + "corporations/",
                ),
            ),
            qualification_penalty=_qualification_penalty(
                "Fla. Stat. § 607.1502(4)",
                court_ordered=True,
            ),
            annual_obligations=(
                _annual_report(
                    "150.00",
                    "Fla. Stat. §§ 607.1622, 607.0122",
                    "Fla. Stat. § 607.1530",
                ),
            ),
            good_standing_evidence=_EXISTENCE + " See § 607.1503(2).",
            consequences=(
                "Cannot prosecute or maintain an action until authority is obtained (§ 607.1502).",
                "Failure to qualify does not invalidate contracts or prevent defending an action.",
                _REVOCATION + " See § 607.1530(1)(a), (2).",
                "Domestic dissolution or inactivity can support foreign revocation "
                "(§ 607.1530(1)(h)).",
                "Missing registered agent has a separate court-ordered $5/day, $500 cap "
                "(§ 607.1507(6)).",
            ),
        ),
        EntityType.LP: EntityRequirement(
            entity_type=EntityType.LP,
            qualification_citation="Fla. Stat. § 620.1902",
            threshold=QualificationThreshold(
                citation="Fla. Stat. §§ 620.1902, 620.1903",
                trigger_activities=_PROPERTY_TRIGGERS,
                isolated_transaction_max_days=30,
                notes=(
                    "An isolated transaction must finish within 30 days and not be part "
                    "of similar transactions. Bare property ownership is exempt; "
                    "income-producing real or tangible personal property constitutes "
                    "transacting business under § 620.1903(3), subject to the listed "
                    "subsection (1) exemptions. Unspecified property activity needs review."
                ),
            ),
            filing_fee=Decimal("1000.00"),
            forms=(
                StateForm(
                    "Application by Foreign Limited Partnership for Authorization to "
                    "Transact Business in Florida",
                    "foreign-lp-authorization",
                    _FORMS + "partnerships/",
                ),
            ),
            qualification_penalty=PenaltyPolicy(
                citation="Fla. Stat. §§ 620.1907, 620.1908",
                description=(
                    "Litigation bar and possible Attorney General restraint apply. "
                    "Do not import the LLC/corporation $500–$1,000 annual civil penalty "
                    "into the LP statute, which does not state that schedule."
                ),
                unquantified_components=("Any monetary remedies require LP-specific assessment",),
            ),
            annual_obligations=(
                _annual_report(
                    "500.00",
                    "Fla. Stat. §§ 620.1210, 620.1109",
                    "Fla. Stat. § 620.1906",
                ),
            ),
            good_standing_evidence=(
                _EXISTENCE + " See § 620.1902(2). Nonindividual general partners must "
                "also be organized/registered as required and active (§ 620.1902(1)(e))."
            ),
            consequences=(
                "Cannot maintain an action until authority is obtained (§ 620.1907).",
                "Failure to qualify does not invalidate contracts or prevent defending an action.",
                "The Attorney General may restrain unqualified business (§ 620.1908).",
                "Failure to maintain reports or agent can result in administrative "
                "revocation (§ 620.1906).",
                _REVOCATION + " See § 620.1906(1)(b), (2).",
                "Reinstatement fee is $500 per calendar year or part revoked (§ 620.1109(6)).",
            ),
        ),
    },
    sources=(
        LegalSource(
            "Fla. Stat. §§ 605.0113, 605.0212–605.0213, 605.0902–605.0908", _LLC, _VERIFIED
        ),
        LegalSource(
            "Fla. Stat. §§ 607.0122, 607.1501–607.1530, 607.1622, 607.193", _CORP, _VERIFIED
        ),
        LegalSource(
            "Fla. Stat. §§ 620.1109, 620.1114, 620.1210, 620.1902–620.1909", _LP, _VERIFIED
        ),
        LegalSource(
            "Florida Division of Corporations foreign entity forms", _FORMS, _GUIDANCE_REVIEWED
        ),
        LegalSource(
            "Florida foreign LLC application CR2E027",
            "https://files.floridados.gov/media/702554/cr2e027.pdf",
            _GUIDANCE_REVIEWED,
        ),
        LegalSource(
            "Florida foreign profit corporation application CR2E007",
            "https://form.sunbiz.org/pdf/cr2e007.pdf",
            _GUIDANCE_REVIEWED,
        ),
        LegalSource(
            "Florida foreign LP application CR2E056",
            "https://form.sunbiz.org/pdf/cr2e056.pdf",
            _GUIDANCE_REVIEWED,
        ),
        LegalSource(
            "Florida document processing dates",
            "https://dos.fl.gov/sunbiz/document-processing-dates/",
            _GUIDANCE_REVIEWED,
        ),
        LegalSource(
            "Florida Division of Corporations annual reports", _REPORTS, _GUIDANCE_REVIEWED
        ),
    ),
    version="2026-10-11-official-forms-review",
    notes=(
        "SOS forms pages process filings in receipt order. No paid expedited turnaround "
        "is quoted by this guide. The queue updated October 9, 2026 listed foreign "
        "registrations and LP filings received September 29; this is an observation, "
        "not a guaranteed processing duration. Use current form cover-letter courier "
        "addresses; the older LP instruction page names a superseded building.",
        "The official 2026 Florida statutes were retrieved and reviewed on 2026-10-10; "
        "SOS forms and instructions were reviewed October 11, 2026. Evidence: "
        "docs/verification/review-2026-10-11.md.",
        "The initial 2025 PDF mirror at https://github.com/caavme/US-Florida-Statutes-2025/tree/"
        "819709012f33e42b6c381915c0191e4c0daceb72 is historical provenance only.",
        "Initial fees include registered-agent designation filing fees, but not the "
        "agent's private service fee or optional certified copies.",
        "Foreign authorization base/agent-designation government fees are LLC $100+$25, "
        "corporation $35+$35, and LP $965+$35. An agent's private service price is additional "
        "and is not fixed by these filing fee statutes.",
        "Qualification does not determine tax nexus, service-of-process jurisdiction, "
        "or industry licensing; statutory safe harbors are not exemptions from those regimes.",
    ),
)
