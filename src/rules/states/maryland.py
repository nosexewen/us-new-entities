"""Source-backed foreign qualification rules; reviewed 2026-10-11."""

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

_LLC = EntityRequirement(
    entity_type=EntityType.LLC,
    qualification_citation="Md. Code, Corps. & Ass’ns § 4A-1002",
    threshold=QualificationThreshold(
        citation="Md. Code, Corps. & Ass’ns § 4A-1009",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "Maryland distinguishes intrastate qualification from "
            "interstate/foreign-business registration. Sections 4A-1002 and 7-202 require "
            "registration for business in Maryland even when commerce is interstate only; "
            "§ 7-203 governs corporate intrastate qualification. The screening decision "
            "covers filing duties, not only intrastate qualification. Isolated "
            "transactions outside a course of similar transactions have no fixed day cap. "
            "Solicitation is not treated as an automatically reviewed exemption. Tax, "
            "licensing and service-of-process obligations remain distinct. Section "
            "4A-1009(b) treats income-producing real or tangible personal property as "
            "doing business, except the foreclosure/default-acquired property exclusions "
            "in subsection (a); those exclusions require manual factual review."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INTERSTATE_COMMERCE}
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign limited liability company registration",
            "SDAT foreign LLC registration",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/Charter%20-%20Foreign%20Businesses/Foreign%20Limited%20Liability%20Company%20Registration_0326-A.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Md. Code, Corps. & Ass’ns § 4A-1007",
        "Unregistered Maryland business carries a $200 Department penalty, reducible "
        "or abatable under Tax–Property § 14-704; SDAT registration form requires it "
        "with filing if prior unregistered business is disclosed. Each member and "
        "each transacting agent may, on misdemeanor conviction, face a separate fine "
        "up to $1,000. Cannot maintain suit until the penalty is paid and "
        "registration requirements are satisfied, or company and successors have "
        "ceased Maryland business as the statute permits. Contracts and defense "
        "remain valid; SDAT becomes service agent. This is not a $200 per-day/year or "
        "universal annual-report late fee; exact overall sanctions require review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Form 1 annual report / conditional business personal-property return",
            cycle="annual",
            due_rule=(
                "On or before April 15 each year, subject to an approved SDAT extension and "
                "applicable report year."
            ),
            fee=Decimal("300"),
            citation="Md. Code, Corps. & Ass’ns § 1-203(b)(3)(ii); Tax–Property § 11-101",
            notes=(
                "Under Corps. & Ass’ns § 1-203(b)(3)(ii) and Tax–Property § 11-101, "
                "the ordinary LLC/stock-corporation Form 1 annual-report filing fee is $300, "
                "separate from any business personal-property assessment or tax. Follow the "
                "applicable tax-year Form 1 questions and instructions to determine whether a "
                "personal-property return is also required; no-property status does not "
                "itself waive the annual report. SDAT permits an online-requested 60-day "
                "extension; for 2026 the extended deadline is June 15. MarylandSaves/employer "
                "savings-plan waivers and certified-family-farm exceptions require documented "
                "eligibility. The current Form 1 lists a $0 fee for a foreign interstate "
                "corporation; do not apply the ordinary $300 qualified-stock-corporation "
                "amount to that distinct registration category. Report delinquency/forfeiture "
                "and property-return penalties require separate fact-specific review; the "
                "$200 nonregistration penalty is not a universal annual-report late fee."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-state written proof of existence equivalent to a certificate of good "
        "standing, issued within the last 60 days at filing, per current SDAT foreign "
        "LLC form and § 4A-1002(b)(7). This is certificate freshness, not a renewal "
        "period."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Md. Code, Corps. & Ass’ns §§ 7-202–7-203",
    threshold=QualificationThreshold(
        citation="Md. Code, Corps. & Ass’ns § 7-103; § 7-202",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=True,
        notes=(
            "Maryland distinguishes intrastate qualification from "
            "interstate/foreign-business registration. Sections 4A-1002 and 7-202 require "
            "registration for business in Maryland even when commerce is interstate only; "
            "§ 7-203 governs corporate intrastate qualification. The screening decision "
            "covers filing duties, not only intrastate qualification. Isolated "
            "transactions outside a course of similar transactions have no fixed day cap. "
            "Solicitation is not treated as an automatically reviewed exemption. Tax, "
            "licensing and service-of-process obligations remain distinct. Section 7-103 "
            "excludes interstate-only commerce from intrastate qualification, but § 7-202 "
            "still requires registration. No LLC income-property trigger is copied into "
            "corporate screening."
        ),
        exempt_activities=frozenset({Activity.BANK_ACCOUNT, Activity.INTERNAL_AFFAIRS}),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INTERSTATE_COMMERCE},
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign corporation qualification",
            "SDAT foreign corporation qualification",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/Charter%20-%20Foreign%20Businesses/Foreign%20Corporation%20Qualification_0326-A.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Md. Code, Corps. & Ass’ns §§ 7-301–7-302",
        "Unqualified/unregistered Maryland business carries a $200 Department "
        "penalty, reducible or abatable under Tax–Property § 14-704; SDAT "
        "qualification form requires payment if prior business is disclosed. Each "
        "officer and each transacting agent may, on misdemeanor conviction, face a "
        "separate fine up to $1,000. Cannot maintain suit until the penalty is paid "
        "and requirements are met, or corporation and successors have ceased Maryland "
        "business as § 7-301 permits. This is not a $200 per-day/year or universal "
        "annual-report late fee; exact overall sanctions require review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Form 1 annual report / conditional business personal-property return",
            cycle="annual",
            due_rule=(
                "On or before April 15 each year, subject to an approved SDAT extension and "
                "applicable report year."
            ),
            fee=Decimal("300"),
            citation="Md. Code, Corps. & Ass’ns § 1-203(b)(3)(ii); Tax–Property § 11-101",
            notes=(
                "Under Corps. & Ass’ns § 1-203(b)(3)(ii) and Tax–Property § 11-101, "
                "the ordinary LLC/stock-corporation Form 1 annual-report filing fee is $300, "
                "separate from any business personal-property assessment or tax. Follow the "
                "applicable tax-year Form 1 questions and instructions to determine whether a "
                "personal-property return is also required; no-property status does not "
                "itself waive the annual report. SDAT permits an online-requested 60-day "
                "extension; for 2026 the extended deadline is June 15. MarylandSaves/employer "
                "savings-plan waivers and certified-family-farm exceptions require documented "
                "eligibility. The current Form 1 lists a $0 fee for a foreign interstate "
                "corporation; do not apply the ordinary $300 qualified-stock-corporation "
                "amount to that distinct registration category. Report delinquency/forfeiture "
                "and property-return penalties require separate fact-specific review; the "
                "$200 nonregistration penalty is not a universal annual-report late fee."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-state written proof of existence equivalent to a certificate of good "
        "standing no more than 60 days old at filing, per current SDAT corporation "
        "qualification form and §§ 7-202(b)(2), 7-203(b)(2)."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Md. Code, Corps. & Ass’ns § 1-203(b)(3)(i); SDAT fee schedule",
    threshold=QualificationThreshold(
        citation="Md. Code, Corps. & Ass’ns § 1-203(b)(3)(i); SDAT fee schedule",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://dat.maryland.gov/businesses/Documents/FEES.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Md. Code, Corps. & Ass’ns § 1-203(b)(3)(i); SDAT fee schedule",
        "LP sanctions require separate review.",
    ),
    annual_obligations=(),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence="Review LP evidence requirements independently.",
    initial_report=None,
)
REQUIREMENT = StateRequirement(
    state="MD",
    name="Maryland",
    registered_agent=RegisteredAgentRequirement(
        citation="Md. Code, Corps. & Ass’ns §§ 1-101(x), 4A-1002(b)(4)–(5), 7-202(b), 7-203(b)",
        notes=(
            "A consenting private resident agent may be an individual residing in "
            "Maryland or a Maryland corporation, LLC or LP, with an actual Maryland "
            "address; no P.O. boxes. Private appointment is not compulsory: the foreign "
            "filing forms appoint SDAT when no private agent is named, or the agent "
            "cannot be found or served, for no additional fee. Corporations may expressly "
            "appoint the Department under §§ 7-202/7-203; LLC § 4A-1002 requires the "
            "fallback statement. Government service is distinct from an optional paid "
            "commercial provider. Do not apply the domestic LLC principal-office "
            "requirement automatically to foreign LLCs."
        ),
        private_appointment_required=False,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Md. Code, Corps. & Ass’ns § 1-203",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=1-203&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 1-101",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=1-101&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 4A-1002",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=4a-1002&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 4A-1007",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=4a-1007&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 4A-1009",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=4a-1009&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 7-202",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=7-202&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 7-203",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=7-203&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 7-301",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=7-301&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 7-302",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=7-302&enactments=false",
        ),
        source(
            "Md. Code, Corps. & Ass’ns § 7-103",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gca&section=7-103&enactments=false",
        ),
        source(
            "Md. Code, Tax–Property § 11-101",
            "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gtp&section=11-101&enactments=false",
        ),
        source(
            "Limited Liability Company Registration",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/Charter%20-%20Foreign%20Businesses/Foreign%20Limited%20Liability%20Company%20Registration_0326-A.pdf",
        ),
        source(
            "FOREIGN CORPORATION QUALIFICATION",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/Charter%20-%20Foreign%20Businesses/Foreign%20Corporation%20Qualification_0326-A.pdf",
        ),
        source(
            "Departmental Forms & Applications", "https://dat.maryland.gov/pages/sdatforms.aspx"
        ),
        source(
            "2026 Filings - Form 1 Business Entity Annual Report",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/BPP%20-%20Annual%20Reports%20and%20Returns/2026%20Filings%20-%20Form%201%20Business%20Entity%20Annual%20Report_0426-A.pdf",
        ),
        source(
            "2026 Form 1 Instructions",
            "https://dat.maryland.gov/Documents/Accessible%20Documents/BPP%20-%20Annual%20Reports%20and%20Returns/2026%20Form%201%20Instructions%20%20FINAL_0416-A.pdf",
        ),
        source(
            "2024.05 SDAT Corporate Charter Fee Schedule",
            "https://dat.maryland.gov/businesses/Documents/FEES.pdf",
        ),
    ),
    version="2026-10-11-batch10",
    notes=(
        "Foreign LLC registration and foreign corporate intrastate qualification each "
        "have a $100 base filing fee under Corps. & Ass’ns § 1-203(b)(3)(i), "
        "corroborated by current SDAT forms. Domestic formation also has a $100 base "
        "processing fee under § 1-203, but domestic corporate "
        "organization/capitalization charges are separate. These guides concern "
        "foreign filings, not a universal domestic formation total. Optional "
        "expedited service and applicable portal/payment charges are separate; "
        "confirm the chosen filing channel.",
        "Form 1 annual reports for ordinary foreign LLCs and qualified stock "
        "corporations are due April 15 with a $300 fee under Corps. & Ass’ns § "
        "1-203(b)(3)(ii) and Tax–Property § 11-101. Eligibility-based waivers and the "
        "distinct foreign-interstate-corporation $0 Form 1 category are disclosed; "
        "personal-property tax is separate.",
    ),
    verification_issues=(),
    review_disclosures=(
        "Foreign LLC registration/corporate intrastate qualification has a $100 base "
        "fee under Corps. & Ass’ns § 1-203(b)(3)(i). Domestic formation also has a "
        "$100 base processing fee, with separate corporate organization/capitalization "
        "charges; these guides concern foreign filings. Optional expedite and applicable "
        "portal/payment charges are separate; confirm the selected channel.",
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
