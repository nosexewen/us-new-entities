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
    qualification_citation="Neb. Rev. Stat. § 21-156",
    threshold=QualificationThreshold(
        citation="Neb. Rev. Stat. § 21-157",
        isolated_transaction_max_days=30,
        notes=(
            "Income-producing real or tangible personal property constitutes business, "
            "subject to the specified security-interest exception. Isolated transactions "
            "must finish within 30 days and not be repeated like transactions. "
            "Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
        trigger_activities=QualificationThreshold(citation="").trigger_activities
        | {Activity.INCOME_PRODUCING_PROPERTY},
    ),
    filing_fee=Decimal("120"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LLC",
            "https://sos.nebraska.gov/sites/default/files/doc/business-services/Corporations/Forms/ApplicationForCertificateofAuthorityLLC.pdf",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Neb. Rev. Stat. § 21-162",
        "Cannot maintain an action until authorized; contracts remain valid and "
        "defenses are preserved. This section does not supply a fixed monetary fine; "
        "review other liabilities separately.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Biennial report",
            cycle="biennial",
            due_rule=(
                "January 1 through April 1 in odd-numbered years, first due in the "
                "odd-numbered year following the calendar year of registration."
            ),
            fee=Decimal("30"),
            citation="Neb. Rev. Stat. §§ 21-125, 21-192",
            notes=(
                "$25 statutory electronic fee; additional portal processing may apply. SOS "
                "treats the report as delinquent June 16."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Home-jurisdiction certificate of existence authenticated by the issuing "
        "official; no numeric freshness limit is prescribed in the reviewed LLC "
        "section or form."
    ),
    initial_report=None,
)
_C_CORP = EntityRequirement(
    entity_type=EntityType.C_CORP,
    qualification_citation="Neb. Rev. Stat. § 21-2,203",
    threshold=QualificationThreshold(
        citation="Neb. Rev. Stat. § 21-2,203(b)",
        isolated_transaction_max_days=30,
        notes=(
            "Isolated transactions must finish within 30 days and not be repeated like "
            "transactions. Qualification exemptions do not determine tax, licensing, or "
            "service-of-process nexus."
        ),
    ),
    filing_fee=Decimal("110"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign corporation",
            "https://sos.nebraska.gov/sites/default/files/doc/business-services/Corporations/Forms/ApplicationForCertificateofAuthorityFC.pdf?download=1",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Neb. Rev. Stat. § 21-2,204",
        "$500 per day of unauthorized business, capped at $10,000 for each year. "
        "Allocate covered days and yearly caps manually; court access is restricted "
        "until authorization.",
    ),
    annual_obligations=(
        AnnualObligation(
            name="Biennial report and occupation tax",
            cycle="biennial",
            due_rule="March 1 in even-numbered years; delinquent April 15.",
            fee=None,
            citation="Neb. Rev. Stat. §§ 21-2,228, 21-306, 21-303",
            notes=(
                "Foreign corporate occupation tax is twice the § 21-303 schedule based on "
                "Nebraska property value, capped at $30,000; this is not a flat report fee."
            ),
        ),
    ),
    consequences=(
        "Failure to qualify can restrict maintaining court proceedings; "
        "entity-specific sanctions and exceptions control. Review contracts, defenses "
        "and cure requirements under the cited law.",
    ),
    good_standing_evidence=(
        "Authenticated home-jurisdiction certificate of existence no more than 60 "
        "days old, per SOS corporate application."
    ),
    initial_report=None,
)
_LP = EntityRequirement(
    entity_type=EntityType.LP,
    qualification_citation="Nebraska SOS foreign LP fee schedule",
    threshold=QualificationThreshold(
        citation="Nebraska SOS foreign LP fee schedule",
        isolated_transaction_max_days=None,
        notes=(
            "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
            "reporting, agent exceptions and sanctions require separate entity-specific "
            "review; an empty report list does not mean no obligations."
        ),
        exempt_activities=frozenset({}),
    ),
    filing_fee=Decimal("120"),
    forms=(
        StateForm(
            "Application for certificate of authority",
            "Foreign LP",
            "https://sos.nebraska.gov/business-services/forms-and-fee-information",
        ),
    ),
    qualification_penalty=unresolved_penalty(
        "Nebraska SOS foreign LP fee schedule", "LP sanctions require separate review."
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
    state="NE",
    name="Nebraska",
    registered_agent=RegisteredAgentRequirement(
        citation="Neb. Rev. Stat. §§ 21-113, 21-2,210",
        notes=(
            "Maintain an eligible agent and an actual in-state registered office for "
            "LLC/corporate filings; a PO box alone is insufficient. LP exceptions require "
            "separate review."
        ),
    ),
    entity_rules={EntityType.LLC: _LLC, EntityType.C_CORP: _C_CORP, EntityType.LP: _LP},
    sources=(
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-156",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-157",
        ),
        source(
            "Nebraska Legislature",
            "https://www.nebraskalegislature.gov/laws/statutes.php?statute=21-162",
        ),
        source(
            "Nebraska Legislature",
            "https://www.nebraskalegislature.gov/laws/statutes.php?statute=21-113",
        ),
        source(
            "Nebraska Legislature",
            "https://www.nebraskalegislature.gov/laws/statutes.php?statute=21-192",
        ),
        source(
            "Nebraska Legislature",
            "https://www.nebraskalegislature.gov/laws/statutes.php?statute=21-125",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-2,203",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-2,204",
        ),
        source(
            "Nebraska Legislature",
            "https://www.nebraskalegislature.gov/laws/statutes.php?statute=21-2,205",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-2,210",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-2,228",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-306",
        ),
        source(
            "Nebraska Legislature",
            "https://nebraskalegislature.gov/laws/statutes.php?statute=21-303",
        ),
        source(
            "Forms and Fee Information | Nebraska Secretary of State",
            "https://sos.nebraska.gov/business-services/forms-and-fee-information",
        ),
        source(
            "Annual/Biennial Reporting | Nebraska Secretary of State",
            "https://sos.nebraska.gov/business-services/annualbiennial-reporting",
        ),
        source(
            "Microsoft Word - Form Cert of Authority Foreign LLC.doc",
            "https://sos.nebraska.gov/sites/default/files/doc/business-services/Corporations/Forms/ApplicationForCertificateofAuthorityLLC.pdf",
        ),
        source(
            "Microsoft Word - NMBCA Cert of Authority to Transact Business 1.1.17 CHANGES "
            "top one under foreign 222.doc",
            "https://sos.nebraska.gov/sites/default/files/doc/business-services/Corporations/Forms/ApplicationForCertificateofAuthorityFC.pdf?download=1",
        ),
    ),
    version="2026-10-11-batch6",
    notes=(
        "LLC paper qualification is $120 ($110 filing plus $10 certificate); "
        "electronic qualification is $110 ($100 plus $10). Corporate qualification is "
        "$110 paper or $100 electronic. Optional services and payment processing are "
        "separate.",
    ),
    verification_issues=(),
    review_disclosures=(
        "LP coverage is limited to the cited filing requirement and fee. Exemptions, "
        "reporting, agent exceptions and sanctions require separate entity-specific "
        "review; an empty report list does not mean no obligations.",
    ),
)
