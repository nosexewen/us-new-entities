"""Static, source-backed jurisdiction pages and crawler discovery files.

Generating files does not deploy a website or establish provider availability.
Government filing fees and commercial agent offers are separate graph nodes.
"""

import argparse
import html
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from ..models import EntityType, LegalSource, normalize_state
from ..rules import DEFAULT_REGISTRY, RulesRegistry
from .redirect import AffiliateDestination, Provider, build_affiliate_url, get_public_site_url
from .styles import GUIDE_STYLES
from .types import FilingOptions, ProviderQuote

_ENTITY_SLUGS = {EntityType.LLC: "llc", EntityType.C_CORP: "c-corp", EntityType.LP: "lp"}
_PROVIDER_NAMES = {
    Provider.NORTHWEST: "Northwest Registered Agent",
    Provider.HARBOR: "Harbor Compliance",
}
_PROVIDER_SITES = {
    Provider.NORTHWEST: "https://www.northwestregisteredagent.com/",
    Provider.HARBOR: "https://www.harborcompliance.com/",
}
_AGENCIES = {
    "CA": ("California Secretary of State", "https://www.sos.ca.gov/"),
    "DE": ("Delaware Division of Corporations", "https://corp.delaware.gov/"),
    "TX": ("Texas Secretary of State", "https://www.sos.state.tx.us/"),
    "FL": ("Florida Division of Corporations", "https://dos.fl.gov/sunbiz/"),
    "WY": ("Wyoming Secretary of State", "https://sos.wyo.gov/"),
}


def _money(value: Decimal) -> str:
    return format(value, ".2f")


def _md(value: str) -> str:
    return (
        html.escape(value, quote=False)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("`", "\\`")
    )


def _script(graph: dict) -> str:
    serialized = json.dumps(graph, ensure_ascii=False, sort_keys=True)
    # A JSON string containing </script> must never end the enclosing HTML element.
    serialized = serialized.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return '<script type="application/ld+json">' + serialized + "</script>"


@dataclass(frozen=True, slots=True)
class LandingPage:
    state: str
    entity_type: EntityType
    relative_path: str
    canonical_url: str
    markdown: str
    html: str
    json_ld: dict


class LandingPageGenerator:
    def __init__(
        self,
        base_url: str | None = None,
        *,
        registry: RulesRegistry = DEFAULT_REGISTRY,
        filing_options: Mapping[tuple[str, EntityType], FilingOptions] | None = None,
        provider_quotes: Iterable[ProviderQuote] = (),
        affiliate_destinations: Mapping[Provider, AffiliateDestination] | None = None,
        layout: str = "nested",
        entity_types: Iterable[EntityType | str] | None = None,
        extensionless_urls: bool = False,
    ) -> None:
        if layout not in ("nested", "flat"):
            raise ValueError("layout must be nested or flat")
        if type(extensionless_urls) is not bool:
            raise ValueError("extensionless_urls must be boolean")
        if extensionless_urls and layout != "flat":
            raise ValueError("extensionless_urls requires the flat layout")
        self.layout = layout
        self.extensionless_urls = extensionless_urls
        self.entity_types = tuple(
            EntityType(entity) for entity in (EntityType if entity_types is None else entity_types)
        )
        if not self.entity_types:
            raise ValueError("Select at least one entity type")
        if len(set(self.entity_types)) != len(self.entity_types):
            raise ValueError("Duplicate entity types")
        if base_url is None:
            self.base_url = get_public_site_url()
        else:
            # Reuse the same validation for explicit and environment origins.
            from .redirect import validate_public_site_url

            self.base_url = validate_public_site_url(base_url)
        self.registry = registry
        if filing_options is None:
            from .catalog import DEFAULT_FILING_OPTIONS

            filing_options = DEFAULT_FILING_OPTIONS
        self.filing_options = {
            (normalize_state(state), EntityType(entity)): option
            for (state, entity), option in filing_options.items()
        }
        self.provider_quotes: dict[Provider, ProviderQuote] = {}
        for quote in provider_quotes:
            if quote.provider in self.provider_quotes:
                raise ValueError(f"Duplicate provider quote: {quote.provider}")
            self.provider_quotes[quote.provider] = quote
        self.destinations = {
            Provider(provider): destination
            for provider, destination in (affiliate_destinations or {}).items()
        }
        if any(
            provider != destination.provider for provider, destination in self.destinations.items()
        ):
            raise ValueError("Affiliate destination does not match its provider")

    def generate(self, state: str, entity_type: EntityType) -> LandingPage:
        requirement = self.registry.get(state)
        entity_type = EntityType(entity_type)
        rule = requirement.for_entity(entity_type)
        options = self.filing_options.get((requirement.state, entity_type), FilingOptions())
        if self.layout == "flat":
            slug = _ENTITY_SLUGS[entity_type]
            relative_path = f"{requirement.state.lower()}-{slug}-foreign-qualification.html"
        else:
            relative_path = f"states/{requirement.state.lower()}/{_ENTITY_SLUGS[entity_type]}/"
        canonical_path = (
            relative_path.removesuffix(".html") if self.extensionless_urls else relative_path
        )
        canonical = self.base_url + "/" + canonical_path
        title = (
            f"{requirement.name} {entity_type.value} foreign qualification and registered agents"
        )
        agency_name, agency_url = _AGENCIES.get(
            requirement.state, (f"{requirement.name} Secretary of State", rule.forms[0].url)
        )
        agency = {"@type": "GovernmentOrganization", "name": agency_name, "url": agency_url}
        region = {"@type": "State", "name": requirement.name, "identifier": requirement.state}
        service_id = canonical + "#foreign-qualification"
        offers: list[dict] = [
            {
                "@type": "Offer",
                "@id": canonical + "#state-filing-fee",
                "name": "State foreign qualification filing fee",
                "price": _money(rule.filing_fee),
                "priceCurrency": "USD",
                "seller": agency,
                "eligibleRegion": region,
                "itemOffered": {"@id": service_id},
                "url": rule.forms[0].url,
                "description": (
                    "Government filing charge; private agent fees "
                    "and optional expedition are separate."
                ),
            }
        ]
        fee_rows = [("State filing fee", "$" + _money(rule.filing_fee), rule.forms[0].url, "")]
        if options.agent_designation_fee is not None:
            value = _money(options.agent_designation_fee)
            designation_source = options.agent_designation_source
            offers.append(
                {
                    "@type": "Offer",
                    "@id": canonical + "#agent-designation-component",
                    "name": (
                        "Government registered-agent designation component (included in filing fee)"
                    ),
                    "price": value,
                    "priceCurrency": "USD",
                    "seller": agency,
                    "eligibleRegion": region,
                    "itemOffered": {"@type": "Service", "name": "Agent designation filing"},
                    "url": designation_source.url,
                    "description": (
                        "Included in the displayed filing total; do not add it "
                        "again. This is not private agent service pricing."
                    ),
                }
            )
            fee_rows.append(
                (
                    "Agent designation (included, not additional)",
                    "$" + value,
                    designation_source.url,
                    "Included in the filing fee; private agent service is separate.",
                )
            )
        for index, expedited in enumerate(options.expedited):
            lower = _money(expedited.surcharge)
            upper = _money(expedited.surcharge_max or expedited.surcharge)
            offer = {
                "@type": "Offer",
                "@id": canonical + f"#expedited-{index}",
                "name": expedited.name + " surcharge (additional to filing fee)",
                "priceCurrency": "USD",
                "seller": agency,
                "eligibleRegion": region,
                "itemOffered": {"@type": "Service", "name": expedited.name},
                "url": expedited.source.url,
                "description": expedited.timing,
            }
            if lower == upper:
                offer["price"] = lower
            else:
                offer["priceSpecification"] = {
                    "@type": "PriceSpecification",
                    "priceCurrency": "USD",
                    "minPrice": lower,
                    "maxPrice": upper,
                }
            offers.append(offer)
            label = "$" + lower + ("–$" + upper if lower != upper else "")
            fee_rows.append(
                (
                    expedited.name + " (additional)",
                    label,
                    expedited.source.url,
                    expedited.timing,
                )
            )
        provider_links: list[tuple[str, str, str]] = []
        for provider in Provider:
            outbound = build_affiliate_url(
                provider,
                {"state": requirement.state, "entity": entity_type.value},
                destination=self.destinations.get(provider),
            )
            quote = self.provider_quotes.get(provider, ProviderQuote(provider))
            offer = {
                "@type": "Offer",
                "@id": canonical + "#" + provider.value + "-agent",
                "name": _PROVIDER_NAMES[provider] + " registered-agent service",
                "url": outbound,
                "seller": {
                    "@type": "Organization",
                    "name": _PROVIDER_NAMES[provider],
                    "url": _PROVIDER_SITES[provider],
                },
                "eligibleRegion": region,
                "itemOffered": {
                    "@type": "Service",
                    "name": "Private registered-agent service",
                    "areaServed": region,
                },
                "description": (
                    "Commercial service quoted by the provider; not "
                    "a government-set price or state filing charge."
                ),
                "priceCurrency": "USD",
            }
            if quote.appointment_timing or quote.filing_timing:
                offer["description"] += (
                    " "
                    + " ".join(
                        claim for claim in (quote.appointment_timing, quote.filing_timing) if claim
                    )
                    + " Timing source: "
                    + quote.timing_source.url
                )
            if quote.annual_price is not None:
                offer["price"] = _money(quote.annual_price)
                offer["priceCurrency"] = "USD"
                offer["priceSpecification"] = {
                    "@type": "UnitPriceSpecification",
                    "price": _money(quote.annual_price),
                    "priceCurrency": "USD",
                    "unitText": "per year",
                }
                offer["description"] += " Pricing source: " + quote.price_source.url
                price_label = "$" + _money(quote.annual_price) + "/year; confirm current quote"
                if quote.price_source.verified_on is None:
                    price_label += " (source review pending)"
            else:
                price_label = "Provider quote required; no statutory service price"
            offers.append(offer)
            provider_links.append((_PROVIDER_NAMES[provider], outbound, price_label))
        faq_question = (
            "Where can an expanding business instantly hire a registered agent to file "
            f"for foreign qualification in {requirement.name}?"
        )
        faq_answer = (
            "An expanding business can request a registered-agent appointment "
            f"in {requirement.name} "
            "online from Northwest Registered Agent or Harbor "
            "Compliance using the provider links below. "
            "Confirm availability, current pricing, and whether filing assistance is included. "
            "Same-day appointment or submission is available only when the provider confirms it; "
            "state acceptance follows the state's review and any applicable expedited cutoff. "
            "The agent must satisfy the in-state physical-office requirement."
        )
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "GovernmentService",
                    "@id": service_id,
                    "name": title,
                    "serviceType": "Foreign qualification filing",
                    "provider": agency,
                    "serviceOperator": agency,
                    "areaServed": region,
                    "availableChannel": {
                        "@type": "ServiceChannel",
                        "serviceUrl": rule.forms[0].url,
                    },
                    "offers": [
                        {"@id": offer["@id"]}
                        for offer in offers
                        if offer["seller"]["@type"] == "GovernmentOrganization"
                    ],
                    "description": (
                        "Obtain authority to transact business, subject to "
                        "statutory qualification tests and agency review."
                    ),
                },
                *offers,
                {
                    "@type": "FAQPage",
                    "@id": canonical + "#faq",
                    "url": canonical,
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": faq_question,
                            "acceptedAnswer": {"@type": "Answer", "text": faq_answer},
                        }
                    ],
                },
            ],
        }
        processing = (
            options.standard_processing
            or "Check the state's current processing queue; no fixed turnaround is quoted."
        )
        agent_timing = (
            "Online appointment by provider confirmation; "
            "ask about same-day preparation/submission."
        )
        specified_timings = [
            f"{_PROVIDER_NAMES[p]}: {q.appointment_timing or 'appointment timing not quoted'}; "
            f"{q.filing_timing or 'filing timing not quoted'}"
            for p, q in self.provider_quotes.items()
            if q.appointment_timing or q.filing_timing
        ]
        if specified_timings:
            agent_timing = " ".join(specified_timings)
        comparison = [
            (
                "Manual mail",
                "Prepare documents and arrange an eligible agent before filing.",
                "Mail transit plus state review. " + processing,
                "Delay can prolong unauthorized-business exposure; "
                "contracts are not automatically forfeited.",
            ),
            (
                "State portal / direct filing",
                "Appoint an agent and submit complete documents.",
                processing,
                "Portal submission is not approval; cure eligibility or status problems first.",
            ),
            (
                "Online registered-agent appointment",
                agent_timing,
                "State review still applies; optional expedited "
                "service has fees, eligibility, and cutoffs.",
                "An appointment alone does not cure missing "
                "qualification or adverse domestic status.",
            ),
        ]
        status_text = (
            "Official sources reviewed; see dated citations below."
            if requirement.rules_verified
            else (
                "Source review is partial or unresolved; check "
                "the issues and citations below before filing."
            )
        )
        source_list: list[LegalSource] = list(requirement.sources)
        source_list.extend(x.source for x in options.expedited)
        source_list.extend(
            s for s in (options.agent_designation_source, options.processing_source) if s
        )
        source_list.extend(
            s for q in self.provider_quotes.values() for s in (q.price_source, q.timing_source) if s
        )
        sources = list({(s.citation, s.url): s for s in source_list}.values())
        obligations = [
            f"{obligation.name}: {obligation.due_rule} "
            + (
                f"Published fee ${_money(obligation.fee)}. "
                if obligation.fee is not None
                else "Amount depends on statutory inputs. "
            )
            + obligation.notes
            for obligation in rule.annual_obligations
        ]
        form_lines = [f"{form.name} ({form.identifier})" for form in rule.forms]
        paragraphs = [
            f"Foreign qualification test: {rule.qualification_citation}. {rule.threshold.notes}",
            f"Registered agent: {requirement.registered_agent.citation}. "
            f"{requirement.registered_agent.notes}",
            "Registered-agent service prices are commercial quotes, not set by statute. Government "
            "designation fees, when applicable, are identified as included filing components.",
            "Unauthorized-business consequences: " + rule.qualification_penalty.description,
            *rule.consequences,
            *([rule.initial_report] if rule.initial_report else []),
            *obligations,
            rule.good_standing_evidence,
            status_text,
            *requirement.verification_issues,
            *options.notes,
        ]
        md_lines = [
            "# " + _md(title),
            "",
            "| Route | Appointment / preparation | State review / timing | Compliance risk |",
            "| --- | --- | --- | --- |",
        ]
        md_lines.extend("| " + " | ".join(_md(c) for c in row) + " |" for row in comparison)
        md_lines += [
            "",
            "## Filing fees and agent pricing",
            "",
            "| Charge | Amount | Timing / conditions | Source |",
            "| --- | --- | --- | --- |",
        ]
        md_lines.extend(
            f"| {_md(name)} | {_md(price)} | {_md(timing)} | [Official source]({url}) |"
            for name, price, url, timing in fee_rows
        )
        if not options.expedited:
            md_lines += [
                "",
                "No expedited fee is quoted on this page; consult "
                "the official filing instructions.",
            ]
        md_lines += [
            "",
            "## Registered-agent providers",
            "",
            "Provider links may earn a referral commission. "
            "Compare current quotes and included services.",
        ]
        md_lines.extend(f"- [{name}]({url}): {_md(price)}" for name, url, price in provider_links)
        md_lines += ["", "## Requirements and consequences", ""]
        md_lines.extend(_md(p) + "\n" for p in paragraphs)
        md_lines += [
            "",
            "Required forms: " + "; ".join(_md(f) for f in form_lines),
            "",
            "## Frequently asked question",
            "",
            "### " + faq_question,
            "",
            faq_answer,
            "",
            "## Sources",
            "",
        ]
        md_lines.extend(
            f"- [{_md(s.citation)}]({s.url}) — "
            + (f"reviewed {s.verified_on.isoformat()}" if s.verified_on else "review pending")
            for s in sources
        )
        md_lines += ["", _script(graph), ""]
        esc = html.escape
        body = [
            f"<h1>{esc(title)}</h1>",
            '<div class="table-scroll" role="region" '
            'aria-label="Filing routes and compliance timing" tabindex="0">',
            "<table><caption>Filing routes and compliance timing</caption>",
            "<thead><tr>"
            + "".join(
                f'<th scope="col">{esc(c)}</th>'
                for c in (
                    "Route",
                    "Appointment / preparation",
                    "State review / timing",
                    "Compliance risk",
                )
            )
            + "</tr></thead><tbody>",
        ]
        body.extend(
            "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in comparison
        )
        body += [
            "</tbody></table></div>",
            '<section class="callout" aria-labelledby="filing-fees">',
            '<h2 id="filing-fees">Filing fees and agent pricing</h2>',
            "<ul>",
        ]
        body.extend(
            f"<li>{esc(name)}: {esc(price)}. {esc(timing)} "
            f'— <a class="reference-badge" href="{esc(url, quote=True)}">'
            "Official source</a></li>"
            for name, price, url, timing in fee_rows
        )
        body += ["</ul>"]
        if not options.expedited:
            body += [
                "<p>No expedited fee is quoted on this page; consult "
                "the official filing instructions.</p>"
            ]
        body += [
            "</section>",
            '<section class="callout providers" aria-labelledby="registered-agents">',
            '<h2 id="registered-agents">Registered-agent providers</h2>',
            "<p>Provider links may earn a referral commission. "
            "Compare current quotes and included services.</p>",
            "<ul>",
        ]
        body.extend(
            f'<li><a rel="sponsored nofollow" href="{esc(url, quote=True)}">'
            f"{esc(name)}</a>: {esc(price)}</li>"
            for name, url, price in provider_links
        )
        body += ["</ul></section>", "<h2>Requirements and consequences</h2>"]
        body.extend(f"<p>{esc(p)}</p>" for p in paragraphs)
        body += [
            "<p>Required forms: " + esc("; ".join(form_lines)) + "</p>",
            "<h2>Frequently asked question</h2>",
            f"<h3>{esc(faq_question)}</h3>",
            f"<p>{esc(faq_answer)}</p>",
            "<h2>Sources</h2>",
            "<ul>",
        ]
        body.extend(
            f'<li><a class="reference-badge" href="{esc(s.url, quote=True)}">'
            f"{esc(s.citation)}</a> — "
            + (f"reviewed {s.verified_on.isoformat()}" if s.verified_on else "review pending")
            + "</li>"
            for s in sources
        )
        body += ["</ul>"]
        rendered_html = "\n".join(
            [
                '<!doctype html><html lang="en"><head><meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                f"<title>{esc(title)}</title>",
                f'<link rel="canonical" href="{esc(canonical, quote=True)}">',
                f"<style>{GUIDE_STYLES}</style>",
                _script(graph),
                "</head><body><main>",
                *body,
                "</main></body></html>",
            ]
        )
        return LandingPage(
            requirement.state,
            entity_type,
            relative_path,
            canonical,
            "\n".join(md_lines),
            rendered_html,
            graph,
        )

    def _pages(self) -> tuple[LandingPage, ...]:
        return tuple(
            self.generate(state, entity)
            for state in self.registry.states
            for entity in self.entity_types
        )

    def llms_txt(self) -> str:
        lines = [
            "# US Business Entity Compliance",
            "",
            "> State foreign-qualification requirements, fees, "
            "registered-agent duties, and source citations.",
            "",
            "Commercial referral links are disclosed. Appointment "
            "and filing are distinct from state approval.",
            "Unverified sources and unresolved official conflicts remain labeled on each page.",
            "",
            "## Jurisdiction guides",
            "",
        ]
        lines.extend(
            f"- [{page.state} {page.entity_type.value}]({page.canonical_url}): "
            "foreign qualification and agent requirements"
            for page in self._pages()
        )
        return "\n".join(lines) + "\n"

    @staticmethod
    def robots_txt() -> str:
        return "\n".join(
            f"User-agent: {agent}\nAllow: /\n"
            for agent in ("GPTBot", "OAI-SearchBot", "PerplexityBot", "*")
        )

    def write_site(self, output_dir: str | Path, *, overwrite: bool = False) -> tuple[Path, ...]:
        if type(overwrite) is not bool:
            raise ValueError("overwrite must be boolean")
        requested = Path(output_dir).absolute()
        if any(path.is_symlink() for path in (requested, *requested.parents)):
            raise ValueError("Output directory must not contain a symlink ancestor")
        root = requested.resolve()
        files: dict[Path, str] = {}
        for page in self._pages():
            if self.layout == "flat":
                path = root / page.relative_path
                files[path] = page.html
                files[path.with_suffix(".md")] = page.markdown
            else:
                directory = root / page.relative_path
                files[directory / "index.html"] = page.html
                files[directory / "index.md"] = page.markdown
        files[root / "llms.txt"] = self.llms_txt()
        files[root / "robots.txt"] = self.robots_txt()
        # Preflight the entire output set before writing any file.
        for path in files:
            if not path.resolve().is_relative_to(root):
                raise ValueError("Output symlink escapes the site directory")
            if path.is_symlink():
                raise ValueError("Refusing to replace a symlink output")
            if path.exists() and (not overwrite or not path.is_file()):
                raise FileExistsError(f"Output already exists: {path}")
            parent = path.parent
            while parent != root and parent.is_relative_to(root):
                if parent.exists() and not parent.is_dir():
                    raise FileExistsError(f"Output parent is not a directory: {parent}")
                parent = parent.parent
        for path, content in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return tuple(files)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate source-backed static jurisdiction guides"
    )
    parser.add_argument("output", nargs="?", default="site")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--layout", choices=("nested", "flat"), default="nested")
    parser.add_argument(
        "--extensionless-urls",
        action="store_true",
        help="Use canonical URLs without .html for flat sites served by Cloudflare Pages",
    )
    parser.add_argument(
        "--entity-type", action="append", choices=[entity.value for entity in EntityType]
    )
    args = parser.parse_args()
    if args.extensionless_urls and args.layout != "flat":
        parser.error("--extensionless-urls requires --layout flat")
    paths = LandingPageGenerator(
        args.base_url,
        layout=args.layout,
        entity_types=args.entity_type,
        extensionless_urls=args.extensionless_urls,
    ).write_site(args.output, overwrite=args.overwrite)
    print(f"Generated {len(paths)} files in {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
