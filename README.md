# US new entities

A dependency-free Python library for US business entity compliance screening and
source-backed static jurisdiction guides. It models
LLCs, C-Corporations, and limited partnerships, with modular rules for California,
Delaware, Texas, Florida, and Wyoming. Installable imports use `us_new_entities`;
the implementation lives in `src/models/`, `src/rules/states/`, and `src/scrapers/`.

## Install and test

Requires Python 3.11 or later. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/ruff check src tests
.venv/bin/ruff format --check src tests
```

For library-only installations, use `pip install .`. There are no runtime services,
API keys, or third-party runtime dependencies. No SOS network requests occur when
running audits or parsing CSVs.

## Screen a cross-border expansion

```python
from datetime import date
from us_new_entities.models import (
    Activity, BusinessPresence, ComplianceAudit, Entity, EntityStatus, EntityType,
)

entity = Entity(
    legal_name="Example Ventures LLC",
    entity_type=EntityType.LLC,
    domestic_state="Delaware",  # State names and postal abbreviations are accepted.
    formation_date=date(2024, 1, 15),
    sos_entity_id="0012345",    # IDs are strings; leading zeros survive normalization.
    status=EntityStatus.GOOD_STANDING,
)
result = ComplianceAudit(
    entity=entity,
    target_state="CA",
    presence=BusinessPresence(frozenset({Activity.LOCAL_SERVICES})),
    as_of=date(2026, 10, 10),
).evaluate()

assert result.qualification_required is True
assert result.foreign_filing_required is True
assert result.registered_agent_appointment_required is True
print(result.entity_requirement.filing_fee)  # Decimal('70')
print(result.remedies)
print(result.warnings)
```

`ComplianceAudit` separates the activity-based qualification requirement from the
need to file now. Pass `is_qualified=True` for an existing foreign registration;
registered-agent compliance still applies. A domestic-state audit requires no foreign
filing but still screens the domestic registered-agent duty. Pass a `RegisteredAgent(name, state,
street_address, is_physical_address=True)` to screen its supplied address facts.
PO boxes, an out-of-state office, and a declared nonphysical address fail the agent
check. Agent eligibility and actual availability for service require independent
verification.

A forfeited or revoked entity keeps its expansion flags, receives a domestic
reinstatement remedy, and has a filing blocker. Domestic formation status is distinct
from foreign registration status; `is_qualified` must come from independent records.
The audit does not assert that a filing will be accepted or that a status certificate
has already been obtained.

Regular local offices, services, retail, and intrastate operations are qualification
screening signals. Encoded exemptions include specified interstate-only activities,
bank accounts, internal affairs, and qualifying isolated transactions. Safe harbors
are entity-specific. A regular local activity alongside an exempt activity still
triggers screening. Merely losing an exemption does not prove qualification is
required: insufficient facts, unspecified employee duties, online sales, property
activity, and repeated/long isolated transactions return `review_required`, with
`None` requirement flags. For Delaware corporations, `Activity.SOLICITATION_OFFICE` describes an office used
exclusively for protected out-of-state-order solicitation; `Activity.OFFICE` describes
a regular local operating office. Revenue alone is not a universal statutory threshold.
Sales-tax nexus, employment duties, licensing, and federal rules are outside this
qualification audit.

## Inspect rules and estimate penalties

```python
from datetime import date
from us_new_entities.models import EntityType
from us_new_entities.rules import DEFAULT_REGISTRY

rule = DEFAULT_REGISTRY.get("TX").for_entity(EntityType.LLC)
estimate = rule.qualification_penalty.estimate(
    date(2025, 11, 1), date(2026, 3, 1)
)
print(estimate.minimum, estimate.maximum)  # 1500.00 1500.00
print(estimate.assessment, estimate.unresolved)
print(rule.forms, rule.annual_obligations, rule.consequences)
```

All money uses `Decimal`. Penalty intervals are **[first liable day, cure date)**:
the cure date is excluded, and a same-day interval is zero. Specify the actual
liability start; the library does not infer a missed filing deadline from a formation
date. Calendar-year schedules count each touched calendar year. Anniversary months
and years clamp to month end, including leap days. Texas's 90-day grace is tested
against the full operating interval; once exceeded, its late registration fee counts
the whole interval, including each calendar year or part.

`PenaltyEstimate.minimum` and `maximum` describe the **modeled sanction component if
assessed**, not a bill or a complete tax/remediation total. `assessment` describes
conditions such as willful conduct or court discretion. `unresolved` lists omitted
amounts or missing inputs. `exact_amount` is `None` when bounds differ or any
component remains unresolved. Unknown monetary sanctions use `None`, never zero.

Annual-report/tax penalties live on each `AnnualObligation.late_penalty`, separately
from unauthorized-business penalties. Interest policies require `unpaid_tax=Decimal(...)`;
without it the fixed component remains visible and the missing interest input is
flagged. Delaware's LLC/LP policy uses simple monthly interest on unpaid tax plus
the late penalty; it does not compound interest on interest. Statutory caps and
period counts are applied explicitly. Filing fees exclude optional expedited
service and third-party registered-agent charges; annual obligations identify
variable tax amounts rather than inventing a universal tax bill.

## Rule sources and scope

Each state module has per-type statutory citations, required forms, registration
fees, agent rules, initial/recurring filing instructions, and enforcement/forfeiture
consequences. Consequences that depend on notice, agency action, or a court order
are descriptive conditions, not automatic transitions of `Entity.status`.

Official source content was reviewed on **2026-10-10**, with these remaining limits:

| Jurisdiction | Current source review |
| --- | --- |
| [Wyoming](docs/verification/wyoming.md) | Official statutes, forms, fees, and agency instructions reviewed; no recorded verification issues. |
| [Texas](docs/verification/texas.md) | Official statutes, SOS guidance, and Comptroller instructions reviewed; no recorded verification issues. |
| [Delaware](docs/verification/delaware.md) | All listed official sources reviewed, including August 2026 forms/fees. Foreign corporate annual-report late penalty remains disputed: statute $200, SOS guidance $250. |
| [California](docs/verification/california.md) | Official SOS/FTB guidance reviewed; legislative source pages returned HTTP 403, leaving statutory coverage incomplete. |
| [Florida](docs/verification/florida.md) | Official 2026 statutes reviewed; DOS form/report pages returned origin challenges, leaving operational forms, processing, and expedited availability unverified. |

`LegalSource.verified_on` records actual content review, not URL reachability.
`StateRequirement.sources_verified` requires all listed sources to have review dates;
`rules_verified` also requires no recorded `verification_issues`. Audits and generated
pages expose remaining gaps and conflicts. Detailed citations and retrieval evidence
are indexed in [docs/verification/README.md](docs/verification/README.md).

These are reference snapshots. The rule version is an implementation snapshot, not
a certified legal effective date; tests verify encoded behavior, not current legal
validity. Recheck rates, deadlines, eligibility, and recent law changes against the
official instructions before an actual filing. Independently hosted historical
mirrors retained in notes do not establish current law.

To add a jurisdiction, create another `StateRequirement` module with all three
entity types and sources, then construct `RulesRegistry([...])`. The registry rejects
duplicate states, its rule mapping is immutable, and unsupported jurisdictions raise
`UnsupportedJurisdictionError`; they never silently become exempt.

## Generate jurisdiction guides

The generator produces matching HTML and Markdown guides with `GovernmentService`,
`FAQPage`, and `Offer` JSON-LD. Each page includes statutory duties, forms, fees,
conditional processing information, source dates, and outstanding verification
issues. Government filing charges are separated from commercial registered-agent
offers. `llms.txt` lists canonical guide URLs; `robots.txt` allows GPTBot,
OAI-SearchBot, PerplexityBot, and other crawlers. Generating files does not deploy
a site or perform a browser redirect.

The default layout covers all three entity types in all five states, creating 15
guides and 32 files, including the two crawler files:

```sh
.venv/bin/python -m us_new_entities.geo.generator site
```

For example, the default nested output includes `site/states/ca/llc/index.html`
and `index.md`. To build the ten LLC/C-Corp guides as flat files in `dist/`:

```sh
.venv/bin/python -m us_new_entities.geo.generator dist \
  --layout flat --entity-type LLC --entity-type C-Corp --overwrite
```

This writes ten HTML files such as `dist/ca-llc-foreign-qualification.html`, ten
matching Markdown files, `llms.txt`, and `robots.txt` (22 files total). Omit
`--overwrite` to refuse replacement of existing outputs. `--base-url` accepts an
explicit HTTPS site origin and overrides the configured public URL for that run.

### Site and referral configuration

The built-in default templates, also provided in [.env.example](.env.example), are:

```dotenv
PUBLIC_SITE_URL=https://compliance-hub.example.com
NORTHWEST_AFFILIATE_URL=https://www.northwestregisteredagent.com/?ref=EXAMPLE_AFFILIATE_ID
HARBOR_AFFILIATE_URL=https://www.shareasale.com/r.cfm?b=99010&u=EXAMPLE_USER_ID&m=99010
```

Use `cp .env.example .env` and replace the example origin and tracking IDs with
your approved values. `.env` is ignored by Git. These example IDs establish no
affiliate relationship, and provider support for forwarded campaign fields is not
guaranteed.

Configuration precedence is **built-in defaults → optional `.env` in the current
working directory → OS environment**. Helpers read configuration when called,
not at import time. `load_geo_config(env_file="path/to/.env")` selects an explicit
file; a missing explicit file raises `FileNotFoundError`. Only the three keys above
are read. The parser accepts literal assignments, optional `export`, comments,
and quoted values; it never executes shell code, expands variables, or evaluates
escapes. Duplicate or malformed assignments for recognized keys are rejected even
when an environment override exists. Do not source the file to use this parser.

`PUBLIC_SITE_URL` must be an HTTPS origin without credentials, a path, query, or
fragment. Referral destinations must use HTTPS on the approved Northwest, Harbor,
or ShareASale hosts; the ShareASale endpoint must be `/r.cfm`. Owner-configured
tracking parameters survive unchanged and incoming query fields cannot replace
them.

```python
from us_new_entities.geo import Provider, build_affiliate_url, load_geo_config

config = load_geo_config()
url = build_affiliate_url(
    Provider.NORTHWEST,
    "?state=CA&entity=AcmeCorp&source=chatgpt",
)
print(config.public_site_url)
print(url)
```

Only `state`, `entity`, `source`, `utm_source`, `utm_medium`, `utm_campaign`,
`utm_content`, and `utm_term` are forwarded. States accept full names or postal
abbreviations for the 50 states. Recognized `entity` values **`LLC`, `C-Corp`, and
`LP`** are preserved; any other supplied string, including a company name or an
empty value, falls back to `LLC`. An absent `entity` remains absent. Company names
are not sent to partners. This fallback is a referral label, not a determination
of the company's legal entity type, and does not change audit or page-generation
validation.

The sample `?state=CA&entity=AcmeCorp&source=chatgpt` now forwards
`state=CA&entity=LLC&source=chatgpt`. Both `source` and `utm_source` retain their
original keys and values when supplied together; owner-configured parameters take
precedence for each key. Repeated state/entity fields remain rejected. Other
unknown fields, including email, arbitrary redirect URLs, and incoming affiliate
IDs, are dropped. Inputs are bounded and malformed encodings or control characters
are rejected; campaign values should not contain personal data.

### Pricing and processing limits

Base government filing fees come from the rules registry. Source-backed optional
expedited charges and processing statements come from `DEFAULT_FILING_OPTIONS`;
missing information remains unquoted. A registered-agent designation government
fee shown as an included component is already part of the base filing fee and must
not be added again. These charges do not set a private agent's annual service price.

Commercial prices are unknown by default. Supply `ProviderQuote` records with
supporting `LegalSource` values to publish a known price or timing claim; unknown
prices remain quote-required and have no invented JSON-LD `price`. Provider links
include a referral disclosure and `rel="sponsored nofollow"`. Agent appointment,
document submission, and state approval are distinct steps. Any quoted expedited
window is subject to the source's cutoffs, eligibility, workload, and possible
rejection; it does not promise instant foreign qualification.

## Deploy to Cloudflare Pages

[.github/workflows/deploy.yml](.github/workflows/deploy.yml) runs on pushes to
`main` and manual runs on `main`. It installs the project, runs the full pytest
suite and Ruff checks, builds the ten LLC/C-Corp guides, validates the 22-file
artifact, then deploys that artifact with Wrangler. Failed build checks prevent
deployment; post-deployment checks verify the published files and HTTP content types.

Configure the repository before running the workflow:

1. Create a Cloudflare Pages **Direct Upload** project with production branch
   `main`, named `us-new-entities`. The workflow explicitly deploys to this project
   and uploads `dist/`.
2. Add GitHub Actions repository secrets `CLOUDFLARE_API_TOKEN` (with Cloudflare
   Pages Edit permission for the account) and `CLOUDFLARE_ACCOUNT_ID`.
3. Optionally set repository variable `PUBLIC_SITE_URL` to a custom HTTPS origin
   already connected to that Pages project. When unset, the workflow derives
   `https://us-new-entities.pages.dev`. Publishing rejects reserved example domains.
4. Optionally set `NORTHWEST_AFFILIATE_URL` and `HARBOR_AFFILIATE_URL` repository
   variables to approved partner URLs. Unlike the library's local example-ID
   templates, the workflow uses direct provider service links when these are unset.

The deployed artifact has `llms.txt`, `robots.txt`, and all state HTML/Markdown
files directly at its root. Cloudflare Pages
[redirects `.html` requests to extensionless routes](https://developers.cloudflare.com/pages/configuration/serving-pages/).
The workflow uses `--extensionless-urls` so HTML canonical
URLs, JSON-LD identifiers, and `llms.txt` point directly to routes such as
`https://us-new-entities.pages.dev/ca-llc-foreign-qualification`. Physical output
filenames remain `ca-llc-foreign-qualification.html` and `.md`; the crawler files
remain available at `/llms.txt` and `/robots.txt`.

Reproduce the deployment export locally, using your actual publishing origin:

```sh
.venv/bin/python -m us_new_entities.geo.generator dist \
  --base-url https://us-new-entities.pages.dev --layout flat --extensionless-urls \
  --entity-type LLC --entity-type C-Corp --overwrite
```

`--extensionless-urls` requires the flat layout. Omit it for hosts that serve the
`.html` URLs directly. Publishing configuration comes from GitHub Actions
variables and secrets; the workflow does not copy a local `.env` file.

Verify the generated deployment before publishing:

```sh
.venv/bin/python -m us_new_entities.geo.verify dist \
  --base-url https://us-new-entities.pages.dev
```

The checker requires exactly 22 flat files, validates HTML head metadata and
JSON-LD graphs, resolves local links and extensionless routes to existing files,
and checks discovery links and crawler rules. It exits unsuccessfully on errors.
Add `--check-live` after deployment to also fetch the published assets, check HTTP
status and content types, and compare response contents to the generated files.
The workflow retries this live check briefly to allow deployment propagation.
To deploy manually, choose **Actions → Deploy static guides → Run workflow** on `main`.

## Public registry adapter

`BaseRegistryAdapter` defines the interface for public records and bulk exports.
`CSVRegistryAdapter` is a sample local extractor/normalizer; it does not scrape a
live SOS site or bypass access controls. Provider adapters should retain source
jurisdiction and raw status, document status aliases, and supply domestic formation
state separately from the state where a foreign registration was found.

The canonical schema requires `legal_name`, `entity_type`, `domestic_state`,
`formation_date`, and `status`. Optional columns are `sos_entity_id`,
`source_jurisdiction`, and `status_jurisdiction`. Dates accept ISO `YYYY-MM-DD` or
explicit US `MM/DD/YYYY`; other formats and impossible dates are rejected. Unknown
states/types/statuses are rejected. “Active” alone does not establish good standing.
Suspended statuses map to the adverse Forfeited screening category while preserving
the raw status and a warning; their legal consequences remain provider-specific.

**`status` must describe standing in the domestic jurisdiction.** The status
jurisdiction defaults to the source registry if supplied, otherwise the domestic
state. A cross-state export enriched with domestic standing evidence must explicitly
supply `status_jurisdiction=domestic_state`. A foreign registration's revocation
cannot be reused as home-state status: conflicting provenance is rejected.

```python
from datetime import date
from us_new_entities.models import Activity, BusinessPresence
from us_new_entities.scrapers import CSVRegistryAdapter

adapter = CSVRegistryAdapter(source_jurisdiction="CA")
with open("tests/fixtures/registry_records.csv", encoding="utf-8-sig", newline="") as source:
    batch = adapter.ingest_csv(
        source,
        target_state="TX",
        presence=BusinessPresence(frozenset({Activity.LOCAL_SERVICES})),
        as_of=date(2026, 10, 10),
    )
print(len(batch.accepted), len(batch.rejected))  # 4 accepted, 4 rejected
for record in batch.accepted:
    print(record.entity.sos_entity_id, record.flags, record.audit_result.filing_blockers)
for error in batch.rejected:
    print(error.row_number, [(issue.field, issue.code) for issue in error.issues])
```

`normalize(mapping, ...)` handles one record and raises `RecordValidationError` on
rejection. `normalize_many(iterable, ...)` and `ingest_csv(text_stream, ...)` retain
accepted records and structured per-row errors. Missing required CSV headers reject the export, including header-only files. CSV
syntax errors stop parsing when row boundaries cannot be trusted. A registry record without separately supplied
activity facts is flagged for qualification review. Target-state audits accept
`is_qualified`, `registered_agent`, and a custom `registry` just like the audit API.
There is no inferred foreign qualification from a business name, mailing address,
or a registry's “Active” label.
