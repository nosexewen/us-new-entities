"""Delaware foreign entity rules, with tax/report sanctions kept separate."""

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

_DGCL = "https://delcode.delaware.gov/title8/c001/sc16/index.html"
_LLC = "https://delcode.delaware.gov/title6/c018/sc09/index.html"
_LP = "https://delcode.delaware.gov/title6/c017/sc09/index.html"
_FEES = "https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf"
_FORMS = "https://corp.delaware.gov/corpforms/"
_VERIFIED = date(2026, 10, 10)


def _alternative_entity_tax(citation: str) -> AnnualObligation:
    return AnnualObligation(
        name="Annual alternative entity tax",
        cycle="annual",
        due_rule="June 1 for the preceding calendar year; no annual report is required.",
        fee=Decimal("400.00"),
        citation=citation,
        late_penalty=PenaltyPolicy(
            citation=citation,
            description=(
                "$200 late tax penalty, plus simple 1.5% interest per month or part "
                "on unpaid tax and penalty; compute each missed tax year separately."
            ),
            amount_min=Decimal("200.00"),
            amount_max=Decimal("200.00"),
            interest_monthly_rate=Decimal("0.015"),
            interest_on_penalty=True,
        ),
        notes=(
            "Applies to domestic and registered foreign LLCs/LPs. Tax is not prorated. "
            "The estimate excludes the unpaid $400 principal. A foreign LLC/LP ceases "
            "to be registered when tax is not paid when due; paying taxes, penalties, "
            "and interest restores registration. The separate three-year cancellation "
            "rule concerns domestic certificates, not a grace period for foreign entities."
        ),
    )


def _qualification_penalty(citation: str) -> PenaltyPolicy:
    return PenaltyPolicy(
        citation=citation,
        description=(
            "$200 for each year or part of business without registration. Annual "
            "periods use anniversaries in this estimate; the collecting authority "
            "must confirm the assessment basis. Filing fees and tax arrears are separate."
        ),
        amount_min=Decimal("200.00"),
        amount_max=Decimal("200.00"),
        period=PenaltyPeriod.STARTED_YEAR,
        unquantified_components=(
            "Registration fees and penalties for the unregistered period require assessment",
        ),
    )


REQUIREMENT = StateRequirement(
    state="DE",
    name="Delaware",
    registered_agent=RegisteredAgentRequirement(
        citation="8 Del. C. §§ 132, 371(b)(2); 6 Del. C. §§ 18-104, 17-104",
        notes=(
            "Maintain an eligible registered agent and Delaware registered office with "
            "a physical street address; a post office box alone does not suffice."
        ),
    ),
    entity_rules={
        EntityType.C_CORP: EntityRequirement(
            entity_type=EntityType.C_CORP,
            qualification_citation="8 Del. C. § 371",
            threshold=QualificationThreshold(
                citation="8 Del. C. §§ 371(b), 373(a)",
                exempt_activities=frozenset(
                    {
                        Activity.INTERSTATE_COMMERCE,
                        Activity.SOLICITATION,
                        Activity.SOLICITATION_OFFICE,
                    }
                ),
                notes=(
                    "Local branch offices, agents, or representatives are screening "
                    "signals. Section 373 protects wholly interstate operations and "
                    "specified solicitation with acceptance and fulfillment outside "
                    "Delaware. An office used only for protected solicitation is not "
                    "automatically a trigger: use SOLICITATION_OFFICE for that exclusive "
                    "purpose, not the regular local OFFICE activity. "
                    "No general 30-day isolated-transaction "
                    "exemption is assumed for corporations."
                ),
            ),
            filing_fee=Decimal("245.00"),
            forms=(
                StateForm(
                    "Qualification Certificate of a Foreign Corporation",
                    "foreign-corporation",
                    "https://corpfiles.delaware.gov/Foreign_Corp/Foreign%20Corporation.pdf",
                ),
            ),
            qualification_penalty=PenaltyPolicy(
                citation="8 Del. C. §§ 378, 383",
                description=(
                    "$200–$500 fine per offense; this interval estimate represents "
                    "one assessed offense, not a daily/monthly compounded charge."
                ),
                amount_min=Decimal("200.00"),
                amount_max=Decimal("500.00"),
                assessment="per_offense_if_assessed",
                unquantified_components=(
                    "Number of offenses and any past fees/taxes require separate assessment",
                ),
            ),
            annual_obligations=(
                AnnualObligation(
                    name="Foreign corporation annual report",
                    cycle="annual",
                    due_rule=(
                        "June 30, first in the year following the calendar year in which "
                        "qualification becomes effective, then annually on a calendar year basis."
                    ),
                    fee=Decimal("250.00"),
                    citation="8 Del. C. §§ 374, 391(a)(8)",
                    late_penalty=PenaltyPolicy(
                        citation="8 Del. C. § 391(a)(8)",
                        description=(
                            "$200 statutory late penalty for a report not filed by June 30. "
                            "Current SOS payment instructions instead say $250; obtain "
                            "a confirmed assessment before relying on an exact amount."
                        ),
                        amount_min=Decimal("200.00"),
                        amount_max=Decimal("200.00"),
                        unquantified_components=(
                            "Official source conflict: § 391(a)(8) says $200 late penalty; "
                            "SOS paytaxes instructions say $250",
                        ),
                    ),
                    notes=(
                        "Foreign corporations do not owe the domestic corporation franchise "
                        "tax merely by qualification. Section 375 terminates the right to do "
                        "business after failure to file a report within a two-year period."
                    ),
                ),
            ),
            good_standing_evidence=(
                "Domestic-jurisdiction certificate of corporate existence issued no "
                "earlier than six months before filing; qualification statement must "
                "also say the corporation is authorized to conduct the proposed business "
                "in its incorporation jurisdiction (8 Del. C. § 371(b))."
            ),
            consequences=(
                "Cannot maintain a Delaware action until qualified and arrears are paid (§ 383).",
                "Failure to qualify does not invalidate contracts or prevent defending an action.",
                "Agents may face a separate $100–$500 per-offense sanction (§ 378).",
            ),
        ),
        EntityType.LLC: EntityRequirement(
            entity_type=EntityType.LLC,
            qualification_citation="6 Del. C. § 18-902",
            threshold=QualificationThreshold(
                citation="6 Del. C. §§ 18-902, 18-912",
                isolated_transaction_without_day_limit=True,
                notes=(
                    "The statutory safe harbors include internal affairs, bank accounts, "
                    "orders accepted outside Delaware, and interstate commerce. An isolated "
                    "transaction not in a course of similar transactions has no fixed day "
                    "limit. Property and debt-collection activities need their specific facts."
                ),
            ),
            filing_fee=Decimal("200.00"),
            forms=(
                StateForm(
                    "Certificate of Registration of Foreign Limited Liability Company",
                    "foreign-llc-registration",
                    "https://corpfiles.delaware.gov/LLC_Forms/Foreign%20LLC.pdf",
                ),
            ),
            qualification_penalty=_qualification_penalty("6 Del. C. § 18-907(d)"),
            annual_obligations=(_alternative_entity_tax("6 Del. C. § 18-1107"),),
            good_standing_evidence=(
                "Attach an official domestic-jurisdiction certificate of existence "
                "issued no earlier than six months before filing (§ 18-902(2)); an "
                "authorized person must also state that the LLC validly exists as of "
                "filing (§ 18-902(1)(b)). Resolve adverse domestic status before filing."
            ),
            consequences=(
                "Cannot maintain a Delaware action until registration and required payments "
                "(§ 18-907).",
                "Failure to register does not invalidate contracts or prevent defending an action.",
            ),
        ),
        EntityType.LP: EntityRequirement(
            entity_type=EntityType.LP,
            qualification_citation="6 Del. C. § 17-902",
            threshold=QualificationThreshold(
                citation="6 Del. C. §§ 17-902, 17-912",
                isolated_transaction_without_day_limit=True,
                notes=(
                    "Apply the LP-specific transacting-business safe harbors. Ordinary "
                    "local operations are screening signals; ownership, financing, and "
                    "partner activities need fact-specific review. An isolated transaction "
                    "outside a course of similar transactions has no fixed day limit."
                ),
            ),
            filing_fee=Decimal("200.00"),
            forms=(
                StateForm(
                    "Certificate of Registration of Foreign Limited Partnership",
                    "foreign-lp-registration",
                    "https://corpfiles.delaware.gov/LP_Forms/Foreign%20LP.pdf",
                ),
            ),
            qualification_penalty=_qualification_penalty("6 Del. C. § 17-907(d)"),
            annual_obligations=(_alternative_entity_tax("6 Del. C. § 17-1109"),),
            good_standing_evidence=(
                "Attach an official domestic-jurisdiction certificate of existence "
                "issued no earlier than six months before filing (§ 17-902(2)); an "
                "authorized person must also state that the LP validly exists as of "
                "filing (§ 17-902(1)(b)). Resolve adverse domestic status before filing."
            ),
            consequences=(
                "Cannot maintain a Delaware action until registration and required payments "
                "(§ 17-907).",
                "Failure to register does not invalidate contracts or prevent defending an action.",
            ),
        ),
    },
    sources=(
        LegalSource("8 Del. C. §§ 371–383", _DGCL, _VERIFIED),
        LegalSource(
            "8 Del. C. § 391(a)(8)",
            "https://delcode.delaware.gov/title8/c001/sc18/index.html",
            _VERIFIED,
        ),
        LegalSource("6 Del. C. §§ 18-902, 18-907, 18-912", _LLC, _VERIFIED),
        LegalSource("6 Del. C. §§ 17-902, 17-907, 17-912", _LP, _VERIFIED),
        LegalSource(
            "6 Del. C. §§ 18-1105, 18-1107",
            "https://delcode.delaware.gov/title6/c018/sc11/index.html",
            _VERIFIED,
        ),
        LegalSource(
            "6 Del. C. §§ 17-1107, 17-1109",
            "https://delcode.delaware.gov/title6/c017/sc11/index.html",
            _VERIFIED,
        ),
        LegalSource("Delaware Division of Corporations August 2026 fee schedule", _FEES, _VERIFIED),
        LegalSource(
            "Qualification Certificate of a Foreign Corporation instructions, rev. 8/2026",
            "https://corpfiles.delaware.gov/Foreign_Corp/Foreign%20Corporation.pdf",
            _VERIFIED,
        ),
        LegalSource(
            "Foreign LLC Registration Certificate instructions, rev. 8/2026",
            "https://corpfiles.delaware.gov/LLC_Forms/Foreign%20LLC.pdf",
            _VERIFIED,
        ),
        LegalSource(
            "Foreign LP Registration Certificate instructions, rev. 8/2026",
            "https://corpfiles.delaware.gov/LP_Forms/Foreign%20LP.pdf",
            _VERIFIED,
        ),
        LegalSource(
            "Delaware Division of Corporations official forms directory", _FORMS, _VERIFIED
        ),
        LegalSource(
            "8 Del. C. §§ 131–132 registered office/agent",
            "https://delcode.delaware.gov/title8/title8.pdf",
            _VERIFIED,
        ),
        LegalSource(
            "6 Del. C. §§ 17-104, 18-104 registered office/agent",
            "https://delcode.delaware.gov/title6/title6.pdf",
            _VERIFIED,
        ),
        LegalSource(
            "Delaware SOS annual alternative entity tax instructions",
            "https://corp.delaware.gov/alt-entitytaxinstructions/",
            _VERIFIED,
        ),
        LegalSource(
            "Delaware SOS foreign corporation annual report payment instructions",
            "https://corp.delaware.gov/paytaxes/",
            _VERIFIED,
        ),
        LegalSource(
            "Delaware SOS expedited service fees and cutoff times",
            "https://corp.delaware.gov/expserv/",
            _VERIFIED,
        ),
    ),
    version="2026-10-10-live",
    verification_issues=(
        "Foreign corporation annual late penalty conflicts: current § 391(a)(8) says "
        "$200, while current SOS annual report instructions say $250; obtain confirmation.",
    ),
    notes=(
        "Official statutes and listed SOS instructions were retrieved and reviewed on "
        "2026-10-10; evidence and unresolved conflicts are in docs/verification/delaware.md.",
        "The initial historical DGCL mirror at https://github.com/companymachine/dgcl/tree/"
        "93882ddd6fb85c17e171de214dd79db846c8516e is provenance only; current rules use "
        "reviewed official statutory sources.",
        "Qualification sanctions are distinct from annual tax/report delinquency; no automatic "
        "monthly compounding of qualification penalties is assumed.",
        "Filing fees exclude registered agent service fees, certificates, and expedited fees.",
        "The August 2026 schedule sets initial foreign qualification/registration surcharges "
        "for all three types at same day $100 (14:00 Eastern cutoff), next business day $50 "
        "(19:00), one hour $1,000 (21:00), or two hours $500 (19:00), in addition to base fees. "
        "Same-day/24-hour fees apply per file number; one/two-hour fees per document/request. "
        "Busy periods, filing errors, and delivery can affect total elapsed time.",
        "The current foreign form instructions confirm base government filing fees of "
        "corporation $245 and LLC/LP $200, with an optional certified copy $50 additional. "
        "Registered-agent designation is part of the application; no separate initial "
        "agent designation government fee is listed for these foreign filings. Private "
        "registered-agent service pricing remains separate.",
    ),
)
