"""Optional charges verified in official sources; base fees stay in the rules registry.

No private service prices are assumed. A range remains a range when official
instructions distinguish document classes without a reviewed exact class quote.
"""

from datetime import date
from decimal import Decimal
from types import MappingProxyType

from ..models import EntityType, LegalSource
from .types import ExpeditedOption, FilingOptions

_REVIEWED = date(2026, 10, 10)
_TX_EXPRESS = LegalSource(
    "Texas SOS Express filing service", "https://www.sos.state.tx.us/express.shtml", _REVIEWED
)
_DE_EXPRESS = LegalSource(
    "Delaware SOS expedited services", "https://corp.delaware.gov/expserv/", _REVIEWED
)
_DE_FEES = LegalSource(
    "Delaware August 2026 fee schedule (foreign qualification rows)",
    "https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf",
    _REVIEWED,
)

_TX_OPTIONS = FilingOptions(
    expedited=(
        ExpeditedOption(
            "Standard expedited service",
            Decimal("50"),
            "Typically 2–3 business days; state review and filing eligibility still apply.",
            _TX_EXPRESS,
        ),
        ExpeditedOption(
            "Next-business-day expedited service",
            Decimal("500"),
            (
                "Qualifying filings received by noon Central; "
                "processed by close of the next business day."
            ),
            _TX_EXPRESS,
        ),
        ExpeditedOption(
            "Same-day expedited service",
            Decimal("750"),
            "Qualifying filings received by noon Central; processed by close of that business day.",
            _TX_EXPRESS,
        ),
    ),
    notes=(
        (
            "Expedited charges are additional; they do not guarantee "
            "acceptance of incomplete or ineligible filings."
        ),
    ),
)
_DE_OPTIONS = FilingOptions(
    expedited=(
        ExpeditedOption(
            "One-hour expedited service",
            Decimal("1000"),
            "Subject to eligibility, workload, and 9 p.m. Eastern cutoff.",
            _DE_EXPRESS,
        ),
        ExpeditedOption(
            "Two-hour expedited service",
            Decimal("500"),
            "Subject to eligibility, workload, and 7 p.m. Eastern cutoff.",
            _DE_EXPRESS,
        ),
        ExpeditedOption(
            "Same-day expedited service",
            Decimal("100"),
            (
                "Foreign qualification surcharge per file number; "
                "2 p.m. Eastern cutoff. Filing eligibility and workload apply."
            ),
            _DE_FEES,
        ),
        ExpeditedOption(
            "Next-business-day expedited service",
            Decimal("50"),
            (
                "Foreign qualification surcharge per file number; "
                "7 p.m. Eastern cutoff. Filing eligibility and workload apply."
            ),
            _DE_FEES,
        ),
    ),
    notes=(
        (
            "Mail transit is outside the expedited state review period. Same-day and "
            "next-business-day fees are per file number; one-hour and two-hour fees "
            "are per document/request. An optional certified copy adds $50. "
            "Cutoffs come from the official expedited-services guide: "
            "https://corp.delaware.gov/expserv/."
        ),
    ),
)

_DEFAULTS = {
    (state, entity): options
    for state, options in (("TX", _TX_OPTIONS), ("DE", _DE_OPTIONS))
    for entity in EntityType
}
_CA_SERVICE = LegalSource(
    "California SOS optional filing service fees",
    "https://www.sos.ca.gov/business-programs/business-entities/service-options",
    _REVIEWED,
)
_CA_QUEUE = LegalSource(
    "California SOS processing-date snapshot",
    "https://www.sos.ca.gov/business-programs/business-entities/processing-dates/",
    _REVIEWED,
)
_CA_OPTIONS = FilingOptions(
    expedited=(
        ExpeditedOption(
            "24-hour filing response",
            Decimal("350"),
            "Online or Sacramento drop-off; excludes weekends and holidays. "
            "A response can be a rejection rather than acceptance.",
            _CA_SERVICE,
        ),
        ExpeditedOption(
            "Same-day filing response",
            Decimal("750"),
            "Received by 9:30 a.m. California local time for a response by 4 p.m.; "
            "eligibility applies and rejection remains possible.",
            _CA_SERVICE,
        ),
        ExpeditedOption(
            "Four-hour filing response",
            Decimal("500"),
            "Sacramento drop-off only with approved preclearance. "
            "Preclearance is separate; 24-hour preclearance costs another $500.",
            _CA_SERVICE,
        ),
    ),
    standard_processing=(
        "Dated queue snapshot updated October 9, 2026: formations/registrations "
        "received online October 7, in person October 6, by mail October 5 "
        "were under review. Recheck the live queue; this is not a turnaround guarantee."
    ),
    processing_source=_CA_QUEUE,
    notes=(
        "Sacramento drop-off may add a $15 nonrefundable handling fee; "
        "online/mail filings are excluded. Optional services are additional to filing fees.",
    ),
)
for entity in EntityType:
    _DEFAULTS[("CA", entity)] = _CA_OPTIONS
for entity, document in (
    (EntityType.LLC, "FLLC/FLLC-CertificateAuthority.pdf"),
    (EntityType.C_CORP, "FPROF/FP-CertificateAuthority.pdf"),
    (EntityType.LP, "FLP/FLP-CertificateRegistration.pdf"),
):
    _DEFAULTS[("WY", entity)] = FilingOptions(
        standard_processing=(
            "The official application states up to 15 business days following "
            "receipt; no expedited filing service is offered."
        ),
        processing_source=LegalSource(
            "Wyoming foreign application processing instructions",
            "https://sos.wyo.gov/Forms/Business/" + document,
            _REVIEWED,
        ),
        notes=("Online appointment does not shorten Wyoming's state review period.",),
    )
# These administrative designation charges are included in, not added to, the foreign filing total.
for entity, fee, chapter in (
    (EntityType.LLC, "25", "0605"),
    (EntityType.C_CORP, "35", "0607"),
    (EntityType.LP, "35", "0620"),
):
    _DEFAULTS[("FL", entity)] = FilingOptions(
        agent_designation_fee=Decimal(fee),
        agent_designation_source=LegalSource(
            f"Fla. Stat. chapter {chapter} agent-designation fee",
            f"https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/{chapter}/{chapter}.html",
            _REVIEWED,
        ),
    )
DEFAULT_FILING_OPTIONS = MappingProxyType(_DEFAULTS)
