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
    qualification_citation="W. Va. Code §§ 31B-10-1002, 31B-10-1004",
    threshold=QualificationThreshold(
        citation="W. Va. Code § 31B-10-1003",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("150"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "LLF-1",
            "https://sos.wv.gov/media/289/download?inline",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "W. Va. Code §§ 31B-10-1008–1009",
        "Cannot maintain an action until authorized; contracts, defense and "
        "limited-liability protections remain valid. Unregistered business appoints "
        "SOS for service and may face Attorney General restraint; no unsupported flat "
        "fine is modeled.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report (conditional biennial election)",
            cycle="annual",
            due_rule=(
                "January 1 through June 30 at 11:59 PM, beginning the calendar year after "
                "registration."
            ),
            fee=Decimal("25"),
            citation="W. Va. Code §§ 31B-2-211, 59-1-2a",
            notes=(
                "Annual reporting is the default. Effective July 1, 2026, businesses with "
                "five consecutive timely annual reports and good standing may elect biennial "
                "reporting for $50 instead of annual $25. Elect with the fifth timely report; "
                "businesses already eligible at effectiveness may elect January 1–July 1, "
                "2027. Skip the following calendar year; first biennial report is the second "
                "calendar year after election, then every two years. File by June 30 at 11:59 "
                "PM under § 59-1-2a(e); subsection (d) describes a January 1–July 1 window. "
                "Annual late fee $50; biennial late fee $100, separate from base fees. "
                "Election may be revoked after delinquency or loss of good standing; five new "
                "timely annual years are required to regain eligibility. Eligible "
                "veteran/active-duty businesses may have their first four annual report fees "
                "waived, but deadlines remain."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence under § 31B-10-1002(b) and LLF-1. "
        "Reviewed sources do not prescribe a numerical certificate-age limit; the "
        "form’s 90-day limit concerns delayed effectiveness, not certificate "
        "freshness."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="W. Va. Code §§ 31D-15-1501, 31D-15-1503",
    threshold=QualificationThreshold(
        citation="W. Va. Code § 31D-15-1501",
        isolated_transaction_max_days=30,
        isolated_transaction_without_day_limit=False,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus. Section 1501(d) also deems in-state contract "
            "performance, torts and injury from defective products to be transacting "
            "business; these fact-specific legal triggers require manual review."
        ),
    ),
    filing_fee=Decimal("100"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "CF-1",
            "https://sos.wv.gov/media/252/download?inline",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "W. Va. Code § 31D-15-1502",
        "Cannot maintain a circuit-court proceeding until authorized; contracts and "
        "defense remain valid. Liable for fees and taxes for each unauthorized year "
        "or part, plus applicable penalties; amounts require entity/history-specific "
        "review.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Annual report (conditional biennial election)",
            cycle="annual",
            due_rule=(
                "January 1 through June 30 at 11:59 PM, beginning the calendar year after "
                "authorization."
            ),
            fee=Decimal("25"),
            citation="W. Va. Code §§ 31D-16-1622, 59-1-2a",
            notes=(
                "Annual reporting is the default. Effective July 1, 2026, businesses with "
                "five consecutive timely annual reports and good standing may elect biennial "
                "reporting for $50 instead of annual $25. Elect with the fifth timely report; "
                "businesses already eligible at effectiveness may elect January 1–July 1, "
                "2027. Skip the following calendar year; first biennial report is the second "
                "calendar year after election, then every two years. File by June 30 at 11:59 "
                "PM under § 59-1-2a(e); subsection (d) describes a January 1–July 1 window. "
                "Annual late fee $50; biennial late fee $100, separate from base fees. "
                "Election may be revoked after delinquency or loss of good standing; five new "
                "timely annual years are required to regain eligibility. Eligible "
                "veteran/active-duty businesses may have their first four annual report fees "
                "waived, but deadlines remain."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence under § 31D-15-1503 and CF-1. No "
        "numerical freshness limit is inferred from the reviewed sources."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="West Virginia SOS foreign-business registration guidance",
    threshold=QualificationThreshold(
        citation="West Virginia SOS foreign-business registration guidance",
        isolated_transaction_max_days=None,
        isolated_transaction_without_day_limit=False,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("150"),
    forms=(
        StateForm(
            "Foreign limited partnership registration",
            "Foreign LP",
            "https://sos.wv.gov/business/registration-and-waivers/register-out-state-foreign-business",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "West Virginia SOS foreign-business registration guidance",
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
    state="WV",
    name="West Virginia",
    registered_agent=RegisteredAgentRequirement(
        citation="W. Va. Code §§ 31B-1-108, 31B-1-111, 31D-15-1507, 31D-15-1510",
        notes=(
            "Foreign LLCs and corporations MAY maintain a private agent and registered "
            "office; a private appointment is not mandatory. If appointed, use an "
            "eligible resident or authorized business and an actual in-state office. "
            "Secretary of State statutory service applies under §§ 31B-1-111 and "
            "31D-15-1510, including forwarding to the last supplied individual address "
            "when no private agent is listed; keep that contact current. Government "
            "service is distinct from an optional paid agent."
        ),
        private_appointment_required=False,
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source("§31B-10", "https://code.wvlegislature.gov/pdf/31B-10/"),
        source("§31D-15", "https://code.wvlegislature.gov/pdf/31D-15/"),
        source("§31B-1", "https://code.wvlegislature.gov/pdf/31B-1/"),
        source("§31B-2", "https://code.wvlegislature.gov/pdf/31B-2/"),
        source("§31D-16", "https://code.wvlegislature.gov/pdf/31D-16/"),
        source("West Virginia Code | §59-1-2A", "https://code.wvlegislature.gov/59-1-2A/"),
        source(
            "Register an Out-of-State (Foreign) Business | WV Secretary of State",
            "https://sos.wv.gov/business/registration-and-waivers/register-out-state-foreign-business",
        ),
        source(
            "West Virginia statutory/filing guidance",
            "https://sos.wv.gov/media/289/download?inline",
        ),
        source(
            "West Virginia statutory/filing guidance",
            "https://sos.wv.gov/media/252/download?inline",
        ),
        source(
            "West Virginia statutory/filing guidance",
            "https://sos.wv.gov/sites/default/files/2026-07/Annualreportcorp_0.pdf",
        ),
    ),
    version="2026-10-11-batch9",
    notes=(
        "Foreign LLC certificate of authority $150; foreign profit corporation "
        "authority $100. Default annual report fee $25, with conditional $50 biennial "
        "election effective July 1, 2026. Separate tax/business-registration "
        "requirements and eligibility-based waivers require review.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
