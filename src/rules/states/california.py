"""California foreign-entity rules, separated by legal entity type.

Official agency guidance, fees, forms and service options were reviewed live.
Legislative text reviewed October 11, 2026; see docs/verification/review-2026-10-11.md.
"""

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


def _statute(code: str, section: str) -> str:
    return (
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
        f"?lawCode={code}&sectionNum={section}."
    )


_FORMS = "https://www.sos.ca.gov/business-programs/business-entities/forms"
_CORP_FORMS = f"{_FORMS}/corporations-foreign-out-state-or-out-country"
_LLC_FORMS = f"{_FORMS}/limited-liability-companies-foreign-out-state-or-out-country"
_LP_FORMS = f"{_FORMS}/limited-partnership-foreign-out-state-or-out-country"
_SOS = "https://www.sos.ca.gov/business-programs/business-entities"
_REVIEWED = date(2026, 10, 10)
_LAW_REVIEWED = date(2026, 10, 11)

_STATEMENT_PENALTY = PenaltyPolicy(
    citation="Cal. Rev. & Tax. Code § 19141; Corp. Code §§ 2204–2206, 17713.09",
    description=(
        "$250 upon SOS certification after an uncured 60-day delinquency notice; "
        "reasonable-cause relief and statutory exceptions apply. Start the "
        "estimation interval at notice, not the original report due date."
    ),
    amount_min=Decimal("250"),
    amount_max=Decimal("250"),
    grace_days=60,
    assessment="after_notice_and_sos_certification",
)


def _tax_obligation(entity_type: EntityType) -> AnnualObligation:
    citations = {
        EntityType.C_CORP: "Cal. Rev. & Tax. Code §§ 23151, 23153",
        EntityType.LLC: "Cal. Rev. & Tax. Code §§ 17941–17942",
        EntityType.LP: "Cal. Rev. & Tax. Code § 17935",
    }
    return AnnualObligation(
        name="Franchise/annual tax and applicable income-based tax or LLC fee",
        cycle="annual_tax_year",
        due_rule=(
            "Tax-year, tax-classification and return-specific payment deadlines; "
            "LLC annual tax generally due 15th day of fourth taxable-year month."
        ),
        fee=None,
        citation=citations[entity_type],
        notes=(
            "Separate from SOS reporting and qualification penalties. Determine "
            "tax classification, tax year, exemptions, income and applicable "
            "first-year rules before computing liability; qualification tax "
            "nexus and economic tax nexus are different tests."
        ),
    )


_CORPORATION = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Cal. Corp. Code § 2105",
    threshold=QualificationThreshold(
        citation="Cal. Corp. Code § 191",
        isolated_transaction_max_days=180,
        notes=(
            "Repeated and successive California transactions other than interstate "
            "or foreign commerce. Orders accepted outside California, internal "
            "affairs, bank accounts and a nonrepeated isolated transaction "
            "completed within 180 days are statutory safe harbors."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Statement and Designation by Foreign Corporation - Stock", "S&DC-S/N", _CORP_FORMS
        ),
    ),
    qualification_penalty=PenaltyPolicy(
        citation="Cal. Corp. Code § 2203(a)–(c)",
        description=(
            "Court may assess $20 per day of willful unauthorized intrastate "
            "business, considering corporate size and willfulness. No statutory "
            "daily-interest compounding or stated aggregate cap. The interval "
            "must represent actual willful business days for the upper estimate."
        ),
        amount_min=Decimal("0"),
        amount_max=Decimal("20"),
        period=PenaltyPeriod.DAY,
        assessment="court_assessed_willful_business_days",
        unquantified_components=(
            "Any $250 litigation-cure penalty under § 2203(c) requires a pending "
            "prequalification intrastate-business action.",
            "Historical filing fees and applicable franchise or other taxes are separate.",
            "R&TC § 19135 may impose $2,000 per taxable year only after failure to "
            "file a demanded tax return within 60 days, subject to reasonable cause.",
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Statement of Information",
            cycle="annual",
            due_rule="During registration anniversary month or the preceding five months.",
            fee=Decimal("25"),
            citation="Cal. Corp. Code § 2117; Gov. Code § 12186(h)",
            late_penalty=_STATEMENT_PENALTY,
            notes="$20 filing fee plus $5 disclosure fee under Corp. Code § 2117(d).",
        ),
        _tax_obligation(EntityType.C_CORP),
    ),
    initial_report="Statement of Information (SI-550) within 90 days of qualification; $25.",
    consequences=(
        "Maintaining an action on prequalification intrastate business is restricted "
        "until qualification, required payments and court receipts under § 2203(c).",
        "Report delinquency can lead to California forfeiture after statutory "
        "notice/certification conditions under §§ 2204–2206. SOS guidance requires "
        "filing within 60 days of a pending suspension/forfeiture notice to avoid "
        "forfeiture; this is separate from the penalty delinquency notice and home-state status.",
    ),
    good_standing_evidence=(
        "Domestic-state certificate showing an existing corporation in good standing "
        "under § 2105(b); restore domestic authority before signing qualification statements."
    ),
)

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="Cal. Corp. Code § 17708.02",
    threshold=QualificationThreshold(
        citation="Cal. Corp. Code § 17708.03",
        isolated_transaction_max_days=180,
        notes="Repeated and successive intrastate transactions; tax nexus is a separate test.",
    ),
    filing_fee=Decimal("70"),
    forms=(
        StateForm(
            "Application to Register a Foreign Limited Liability Company", "LLC-5", _LLC_FORMS
        ),
    ),
    qualification_penalty=PenaltyPolicy(
        citation="Cal. Corp. Code §§ 17708.07, 17708.09; Rev. & Tax. Code § 19135",
        description=(
            "Registration sanctions include inability to maintain proceedings and "
            "Attorney General injunction. The cited LLC provisions do not impose "
            "the corporate $20-per-day penalty."
        ),
        assessment="fact_dependent_tax_and_enforcement_review",
        unquantified_components=(
            "Outstanding taxes and fees depend on tax classification and filing history.",
            "R&TC § 19135 $2,000 per taxable-year sanction requires failure to file "
            "a tax return within 60 days after FTB demand and has reasonable-cause "
            "relief; determine applicability from the LLC's tax classification.",
        ),
    ),
    annual_obligations=(
        AnnualObligation(
            name="Statement of Information",
            cycle="biennial",
            due_rule=(
                "Registration anniversary month or preceding five months "
                "in the applicable biennial year."
            ),
            fee=Decimal("20"),
            citation="Cal. Corp. Code § 17702.09; Gov. Code § 12190(k)",
            late_penalty=_STATEMENT_PENALTY,
        ),
        _tax_obligation(EntityType.LLC),
    ),
    initial_report="Statement of Information (LLC-12) within 90 days of registration; $20.",
    consequences=(
        "Cannot maintain a California action until registered; may defend proceedings.",
        "Attorney General may enjoin unauthorized business under § 17708.09.",
        "Report or tax defaults can suspend/forfeit California powers after statutory "
        "conditions. SOS guidance requires filing within 60 days of a pending "
        "suspension/forfeiture notice; reinstatement and domestic-state restoration "
        "are separate remedies.",
    ),
    good_standing_evidence=(
        "Existence/status/good-standing certificate or similar record issued within "
        "six months under § 17708.02(b), plus truthful domestic-authority statement."
    ),
)

_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Cal. Corp. Code § 15909.02",
    threshold=QualificationThreshold(
        citation="Cal. Corp. Code §§ 15901.02(ai), 15909.03",
        trigger_activities=frozenset(
            {
                Activity.OFFICE,
                Activity.LOCAL_SERVICES,
                Activity.RETAIL,
                Activity.INTRASTATE_BUSINESS,
                Activity.INCOME_PRODUCING_PROPERTY,
            }
        ),
        isolated_transaction_max_days=180,
        notes=(
            "Repeated and successive intrastate transactions. Ownership of "
            "income-producing California real or tangible personal property "
            "expressly constitutes transacting business under § 15909.03(b); "
            "unspecified property activity needs factual review."
        ),
    ),
    filing_fee=Decimal("70"),
    forms=(
        StateForm("Application for Registration of Foreign Limited Partnership", "LP-5", _LP_FORMS),
    ),
    qualification_penalty=PenaltyPolicy(
        citation="Cal. Corp. Code § 15909.07(c)",
        description=(
            "$20 per unauthorized intrastate-business day, capped at $10,000; "
            "recoverable in an action under § 2258. Daily accrual is not compounding. "
            "The interval assumes unauthorized business on each counted day."
        ),
        amount_min=Decimal("20"),
        amount_max=Decimal("20"),
        period=PenaltyPeriod.DAY,
        cap=Decimal("10000"),
        assessment="recoverable_statutory_daily_penalty",
    ),
    annual_obligations=(_tax_obligation(EntityType.LP),),
    consequences=(
        "Cannot maintain California proceedings until registered; "
        "contracts and defense remain valid.",
        "Attorney General may restrain unauthorized business under § 15909.08.",
        "No routine SOS annual Statement of Information; annual tax duties remain separate.",
    ),
    good_standing_evidence=(
        "Domestic-state certificate of existence or similar record issued within "
        "six months under § 15909.02(b), plus truthful domestic-authority statement."
    ),
)

REQUIREMENT = StateRequirement(
    state="CA",
    name="California",
    registered_agent=RegisteredAgentRequirement(
        citation="Cal. Corp. Code §§ 1505, 2117(b), 17701.13, 15901.16(d)",
        notes=(
            "Resident individual with California street address or registered "
            "corporate agent under § 1505. When a corporate agent is designated, "
            "its address is not entered on the entity form; agent registration "
            "supplies the service address."
        ),
    ),
    entity_rules={EntityType.C_CORP: _CORPORATION, EntityType.LLC: _LLC, EntityType.LP: _LP},
    sources=(
        LegalSource("Cal. Corp. Code § 191", _statute("CORP", "191"), _LAW_REVIEWED),
        LegalSource("Cal. Corp. Code § 17708.03", _statute("CORP", "17708.03"), _LAW_REVIEWED),
        LegalSource("Cal. Corp. Code § 15901.02(ai)", _statute("CORP", "15901.02"), _LAW_REVIEWED),
        LegalSource("Cal. Corp. Code § 15909.03", _statute("CORP", "15909.03"), _LAW_REVIEWED),
        LegalSource("Cal. Corp. Code § 2105", _statute("CORP", "2105"), _LAW_REVIEWED),
        LegalSource("Cal. Corp. Code § 2203", _statute("CORP", "2203"), _LAW_REVIEWED),
        LegalSource(
            "Cal. Corp. Code §§ 17708.02–17708.09", _statute("CORP", "17708.07"), _LAW_REVIEWED
        ),
        LegalSource(
            "Cal. Corp. Code §§ 15909.02–15909.08", _statute("CORP", "15909.07"), _LAW_REVIEWED
        ),
        LegalSource("Cal. Gov. Code § 12186", _statute("GOV", "12186"), _LAW_REVIEWED),
        LegalSource("Cal. Gov. Code § 12188", _statute("GOV", "12188"), _LAW_REVIEWED),
        LegalSource("Cal. Gov. Code § 12190", _statute("GOV", "12190"), _LAW_REVIEWED),
        LegalSource("Cal. Rev. & Tax. Code § 19141", _statute("RTC", "19141"), _LAW_REVIEWED),
        LegalSource("Cal. Rev. & Tax. Code § 19135", _statute("RTC", "19135"), _LAW_REVIEWED),
        LegalSource("California SOS foreign corporation forms and fees", _CORP_FORMS, _REVIEWED),
        LegalSource("California SOS foreign LLC forms and fees", _LLC_FORMS, _REVIEWED),
        LegalSource("California SOS foreign LP forms and fees", _LP_FORMS, _REVIEWED),
        LegalSource(
            "California SOS qualification, agent and forfeiture guidance", f"{_SOS}/faqs", _REVIEWED
        ),
        LegalSource(
            "California SOS Statement of Information filing window", f"{_SOS}/statements", _REVIEWED
        ),
        LegalSource("California SOS service options", f"{_SOS}/service-options", _REVIEWED),
        LegalSource(
            "California SOS current processing dates", f"{_SOS}/processing-dates/", _REVIEWED
        ),
        LegalSource(
            "California FTB penalty reference chart",
            "https://www.ftb.ca.gov/forms/misc/1024.html",
            _REVIEWED,
        ),
        LegalSource(
            "California FTB common penalties",
            "https://www.ftb.ca.gov/pay/penalties-and-interest/index.html",
            _REVIEWED,
        ),
        LegalSource(
            "California FTB suspension and revival",
            "https://www.ftb.ca.gov/help/business/my-business-is-suspended.html",
            _REVIEWED,
        ),
        LegalSource(
            "California FTB LLC tax guidance",
            "https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html",
            _REVIEWED,
        ),
        LegalSource(
            "California FTB tax doing-business test",
            "https://www.ftb.ca.gov/file/business/doing-business-in-california.html",
            _REVIEWED,
        ),
    ),
    version="2026-10-11-official-law-review",
    notes=(
        "Official SOS/FTB guidance, fees, forms and service options were fetched and "
        "reviewed October 10, 2026. Legislative text was retrieved and reviewed October "
        "11, resolving the earlier HTTP 403 gap. Evidence: docs/verification/review-2026-10-11.md.",
        "No penalty changes an entity's domestic-state standing automatically.",
        "Annual tax amounts depend on classification, tax year and exemptions; "
        "do not treat a fixed annual-tax amount as universal.",
        "Optional SOS services are additional to base filing fees: 24-hour expedite "
        "$350 excluding weekends/holidays; same-day $750 if received by 9:30 a.m. "
        "for a response by 4 p.m. California local time. Four-hour $500 is Sacramento "
        "drop-off only and requires prior approved preclearance; 24-hour preclearance "
        "is separately $500. A filing response can be rejection rather than approval.",
        "Sacramento drop-off adds a nonrefundable $15 handling fee per filing, "
        "except Statements of Information; it does not apply online or by mail. "
        "Fees and eligibility can change; consult current SOS service options.",
        "The processing-dates page updated October 9, 2026 listed corporation, "
        "LLC and LP formation/registration arrivals being reviewed: online October 7, "
        "in person October 6, mail October 5. These are queue-date observations, "
        "not promised turnaround times; recheck the live page before scheduling.",
    ),
)
