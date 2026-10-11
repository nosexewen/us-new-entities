"""Bounded validation for flat Cloudflare Pages guides and optional coming-soon pages.

Checks the generated contract, rather than every HTML or Schema.org rule. External
source links are accepted over HTTPS without fetching them. Optional live checks
read this site's assets and compare their bytes with the verified build.
"""

import argparse
import html
import json
import os
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from ..models.entity import STATE_NAMES
from ..rules import DEFAULT_REGISTRY
from .redirect import get_public_site_url, validate_public_site_url

_STEMS = tuple(
    f"{state}-{entity}-foreign-qualification"
    for state in ("ca", "de", "fl", "tx", "wy")
    for entity in ("llc", "c-corp")
)
_EXPECTED_FILES = frozenset(
    [stem + suffix for stem in _STEMS for suffix in (".html", ".md")] + ["llms.txt", "robots.txt"]
)
_MAX_FILE_BYTES = 2 * 1024 * 1024
_VOID_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
_MD_LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)\)")
_JSON_SCRIPT = re.compile(
    r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', re.DOTALL | re.IGNORECASE
)


@dataclass(frozen=True, slots=True)
class VerificationIssue:
    file: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class SiteVerificationReport:
    files: int
    pages: int
    routes: tuple[str, ...]
    errors: tuple[VerificationIssue, ...]
    live_checks: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _text(value: str) -> str:
    return " ".join(value.split())


class _Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.problems: list[str] = []
        self.doctypes: list[str] = []
        self.tags: list[tuple[str, dict[str, str | None], bool]] = []
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.visible: list[str] = []
        self.titles: list[tuple[bool, str]] = []
        self.json_scripts: list[tuple[bool, str]] = []
        self._script: list[str] | None = None
        self._script_head = False
        self._title: list[str] | None = None
        self._title_head = False
        self.feed(source)
        self.close()
        if self.stack:
            self.problems.append("Unclosed HTML elements")

    def handle_decl(self, decl: str) -> None:
        self.doctypes.append(decl.casefold())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if len({key for key, _ in attrs}) != len(attrs):
            self.problems.append("Duplicate HTML attributes")
        values = dict(attrs)
        in_head = "head" in self.stack
        if tag in {"head", "body"} and self.stack != ["html"]:
            self.problems.append("Head and body must be direct children of the HTML root")
        if tag == "body" and not any(t == "head" for t, _, _ in self.tags):
            self.problems.append("Head must precede body")
        if tag == "head" and any(t == "body" for t, _, _ in self.tags):
            self.problems.append("Head must precede body")
        self.tags.append((tag, values, in_head))
        if tag == "base":
            self.problems.append("Base elements would change relative-link resolution")
        identifier = values.get("id")
        if identifier:
            if identifier in self.ids:
                self.problems.append("Duplicate HTML ID")
            self.ids.add(identifier)
        for key in ("href", "src", "action"):
            if values.get(key) is not None:
                self.links.append(values[key])
        if tag == "title":
            self._title = []
            self._title_head = in_head
        if tag == "script" and values.get("type") == "application/ld+json":
            self._script = []
            self._script_head = in_head
        if tag not in _VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in _VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script is not None:
            self.json_scripts.append((self._script_head, "".join(self._script)))
            self._script = None
        if tag == "title" and self._title is not None:
            self.titles.append((self._title_head, "".join(self._title)))
            self._title = None
        if tag not in _VOID_TAGS:
            if not self.stack or self.stack[-1] != tag:
                self.problems.append(f"Mismatched HTML closing element: {tag}")
            else:
                self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._script is not None:
            self._script.append(data)
        elif self._title is not None:
            self._title.append(data)
        elif "body" in self.stack and "script" not in self.stack and "style" not in self.stack:
            self.visible.append(data)


def _json_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key")
        result[key] = value
    return result


def _load_json(source: str) -> object:
    def reject_constant(value: str) -> None:
        raise ValueError("Non-finite JSON number")

    return json.loads(source, object_pairs_hook=_json_object, parse_constant=reject_constant)


def _objects(value: object):
    pending = [(value, 0)]
    count = 0
    while pending:
        item, depth = pending.pop()
        count += 1
        if count > 10000 or depth > 64:
            raise ValueError("Structured data exceeds supported complexity")
        if isinstance(item, dict):
            yield item
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)


def _schema_errors(graph: object, canonical: str, visible: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(graph, dict) or graph.get("@context") != "https://schema.org":
        return ["JSON-LD requires the https://schema.org context"]
    nodes = graph.get("@graph")
    if not isinstance(nodes, list) or not nodes or not all(isinstance(n, dict) for n in nodes):
        return ["JSON-LD requires a nonempty object @graph"]
    identifiers: set[str] = set()
    for node in nodes:
        identifier = node.get("@id")
        if not isinstance(identifier, str) or not identifier.startswith(canonical + "#"):
            errors.append(
                "Graph node ID must identify this canonical page with a semantic fragment"
            )
        elif identifier in identifiers:
            errors.append("Duplicate graph node ID")
        else:
            identifiers.add(identifier)
        if node.get("@type") not in {"GovernmentService", "FAQPage", "Offer"}:
            errors.append("Graph node requires a supported type")
    for node in _objects(graph):
        if set(node) == {"@id"} and node["@id"] not in identifiers:
            errors.append("Dangling JSON-LD graph reference")
    services = [n for n in nodes if n.get("@type") == "GovernmentService"]
    faqs = [n for n in nodes if n.get("@type") == "FAQPage"]
    offers = [n for n in nodes if n.get("@type") == "Offer"]
    if len(services) != 1 or len(faqs) != 1 or len(offers) < 3:
        errors.append(
            "Graph requires one GovernmentService, one FAQPage and government/provider Offers"
        )
    for service in services:
        if not service.get("name") or not service.get("offers"):
            errors.append("GovernmentService requires a name and offer references")
        provider = service.get("provider")
        if not isinstance(provider, dict) or provider.get("@type") != "GovernmentOrganization":
            errors.append("GovernmentService requires a GovernmentOrganization provider")
    for offer in offers:
        if not offer.get("name") or not offer.get("url") or not offer.get("itemOffered"):
            errors.append("Offer requires name, URL and itemOffered")
        if offer.get("priceCurrency") != "USD":
            errors.append("Offer currency must be USD")
        specification = offer.get("priceSpecification")
        amounts = [offer["price"]] if "price" in offer else []
        if specification is not None:
            if not isinstance(specification, dict) or specification.get("priceCurrency") != "USD":
                errors.append("Price specification must be an object in USD")
            else:
                amounts.extend(
                    specification[k]
                    for k in ("price", "minPrice", "maxPrice")
                    if k in specification
                )
                if ("minPrice" in specification) != ("maxPrice" in specification):
                    errors.append("Price ranges require both monetary bounds")
        try:
            prices = [Decimal(str(amount)) for amount in amounts if not isinstance(amount, bool)]
            if len(prices) != len(amounts) or any(not p.is_finite() or p < 0 for p in prices):
                raise ValueError("Invalid monetary amount")
            if (
                isinstance(specification, dict)
                and "minPrice" in specification
                and "maxPrice" in specification
            ):
                if Decimal(str(specification["minPrice"])) > Decimal(
                    str(specification["maxPrice"])
                ):
                    errors.append("Price range minimum exceeds maximum")
        except (InvalidOperation, ValueError):
            errors.append("Offer amounts must be finite nonnegative prices")
        seller = offer.get("seller")
        if not isinstance(seller, dict) or seller.get("@type") not in {
            "Organization",
            "GovernmentOrganization",
        }:
            errors.append("Offer requires an organization seller")
        elif seller["@type"] == "GovernmentOrganization" and not amounts:
            errors.append("Government charge requires an amount")
        elif (
            seller["@type"] == "Organization"
            and amounts
            and not re.search(r"Pricing source: https://\S+", str(offer.get("description", "")))
        ):
            errors.append(
                "Private price requires source attribution; an unknown quote must stay unpriced"
            )
    for faq in faqs:
        if faq.get("url") != canonical:
            errors.append("FAQPage URL must match canonical")
        questions = faq.get("mainEntity")
        if not isinstance(questions, list) or not questions:
            errors.append("FAQPage requires questions")
            continue
        for question in questions:
            if not isinstance(question, dict) or question.get("@type") != "Question":
                errors.append("FAQ requires Question nodes")
                continue
            answer = question.get("acceptedAnswer")
            if not isinstance(answer, dict) or answer.get("@type") != "Answer":
                errors.append("FAQ requires accepted Answer nodes")
                continue
            for content in (question.get("name"), answer.get("text")):
                if (
                    not isinstance(content, str)
                    or not content.strip()
                    or _text(content) not in visible
                ):
                    errors.append("Structured FAQ question and answer must match visible content")
    return errors


def _resolve_link(
    link: str, current_url: str, base_url: str, files: set[str]
) -> tuple[str, str] | None:
    if any(ord(c) < 32 or ord(c) == 127 for c in link) or "\\" in link:
        raise ValueError("Link contains controls or backslashes")
    target = urlsplit(urljoin(current_url, link))
    if target.scheme != "https" or not target.hostname or target.username is not None:
        raise ValueError("Links must resolve to absolute HTTPS URLs without credentials")
    origin = urlsplit(base_url)
    if (target.hostname.casefold(), target.port or 443) != (
        origin.hostname.casefold(),
        origin.port or 443,
    ):
        return None
    path = unquote(target.path)
    filename = path.removeprefix("/")
    if filename not in files and filename + ".html" in files:
        filename += ".html"
    if filename not in files:
        raise ValueError("Internal link does not resolve to an output file")
    return filename, unquote(target.fragment)


def _robots_allows(source: str, agent: str, path: str) -> bool:
    groups: list[tuple[list[str], list[tuple[bool, str]]]] = []
    agents: list[str] = []
    rules: list[tuple[bool, str]] = []
    for line in source.splitlines() + ["User-agent: _end"]:
        name, separator, value = line.split("#", 1)[0].partition(":")
        if not separator:
            continue
        name, value = name.strip().casefold(), value.strip()
        if name == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.casefold())
        elif name in {"allow", "disallow"} and agents and value:
            rules.append((name == "allow", value))
    matched: list[tuple[int, list[tuple[bool, str]]]] = []
    for group_agents, group_rules in groups:
        lengths = [
            0 if a == "*" else len(a) for a in group_agents if a == "*" or a in agent.casefold()
        ]
        if lengths:
            matched.append((max(lengths), group_rules))
    if not matched:
        return True
    specificity = max(length for length, _ in matched)
    applicable = []
    for length, group_rules in matched:
        if length != specificity:
            continue
        for allow, pattern in group_rules:
            expression = re.escape(pattern).replace(r"\*", ".*")
            if pattern.endswith("$"):
                expression = expression[:-2] + "$"
            if re.match(expression, path):
                applicable.append((len(pattern.replace("*", "").rstrip("$")), allow))
    return max(applicable)[1] if applicable else True


def verify_site(
    output_dir: Path | str,
    *,
    base_url: str | None = None,
    check_live: bool = False,
    include_coming_soon: bool = False,
) -> SiteVerificationReport:
    """Check reviewed guides and optional 50-state coverage; optionally check live assets.

    Live checks run only after local success, use verified TLS and a ten-second
    request timeout, perform no retries, and stop at the first failure.
    """
    errors: list[VerificationIssue] = []

    def issue(file: str, code: str, message: str) -> None:
        errors.append(VerificationIssue(file, code, message))

    stems = (
        tuple(
            f"{state.lower()}-{entity}-foreign-qualification"
            for state in sorted(set(STATE_NAMES) - {"DC"})
            for entity in ("llc", "c-corp")
        )
        if include_coming_soon
        else _STEMS
    )
    expected_files = frozenset(
        [stem + suffix for stem in stems for suffix in (".html", ".md")]
        + ["llms.txt", "robots.txt"]
    )
    routes = tuple("/" + stem for stem in stems)
    try:
        origin = get_public_site_url() if base_url is None else validate_public_site_url(base_url)
    except (ValueError, OSError):
        return SiteVerificationReport(
            0,
            0,
            routes,
            (
                VerificationIssue(
                    ".", "invalid_base_url", "Expected a configured absolute HTTPS origin"
                ),
            ),
        )
    root = Path(output_dir)
    if root.is_symlink() or not root.is_dir():
        return SiteVerificationReport(
            0,
            0,
            routes,
            (
                VerificationIssue(
                    ".", "invalid_directory", "Output must be an existing nonsymlink directory"
                ),
            ),
        )
    entries = list(root.iterdir())
    files: set[str] = set()
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            issue(
                entry.name,
                "invalid_file",
                "Only regular flat files are allowed; no symlinks/directories",
            )
        else:
            files.add(entry.name)
    for name in sorted(expected_files - files):
        issue(name, "missing_file", "Required production asset is missing")
    for name in sorted(files - expected_files):
        issue(name, "extra_file", "Unexpected production asset")
    content: dict[str, str] = {}
    for filename in sorted(files & expected_files):
        try:
            with (root / filename).open("rb") as stream:
                data = stream.read(_MAX_FILE_BYTES + 1)
            if len(data) > _MAX_FILE_BYTES:
                raise ValueError("Asset exceeds supported size limit")
            content[filename] = data.decode("utf-8-sig")
        except (OSError, UnicodeError, ValueError):
            issue(filename, "invalid_content", "Asset must be readable UTF-8 within the size limit")
    documents: dict[str, _Document] = {}
    for stem in stems:
        filename = stem + ".html"
        if filename not in content:
            continue
        canonical = origin + "/" + stem
        document = _Document(content[filename])
        documents[filename] = document
        for problem in document.problems:
            issue(filename, "invalid_html", problem)
        if document.doctypes != ["doctype html"] or not content[
            filename
        ].lstrip().casefold().startswith("<!doctype html>"):
            issue(filename, "doctype", "HTML must start with exactly one HTML5 doctype")
        html_tags = [a for t, a, _ in document.tags if t == "html"]
        if len(html_tags) != 1 or html_tags[0].get("lang") != "en":
            issue(filename, "language", "HTML requires one root with lang=en")
        if (
            sum(t == "head" for t, _, _ in document.tags) != 1
            or sum(t == "body" for t, _, _ in document.tags) != 1
        ):
            issue(filename, "html_structure", "HTML requires one head and one body")
        if (
            len(document.titles) != 1
            or not document.titles[0][0]
            or not document.titles[0][1].strip()
        ):
            issue(filename, "title", "HTML head requires one nonempty title")
        metas = [a for t, a, h in document.tags if t == "meta" and h]
        if sum(str(a.get("charset", "")).casefold() == "utf-8" for a in metas) != 1:
            issue(filename, "charset", "HTML head requires one UTF-8 charset declaration")
        if not any(
            a.get("name") == "viewport" and "width=device-width" in str(a.get("content", ""))
            for a in metas
        ):
            issue(filename, "viewport", "HTML head requires a device-width viewport")
        canonicals = [
            a.get("href")
            for t, a, h in document.tags
            if t == "link" and h and "canonical" in str(a.get("rel", "")).split()
        ]
        if canonicals != [canonical]:
            issue(
                filename,
                "canonical",
                "Canonical must match this page's extensionless production route",
            )
        if len(document.json_scripts) != 1 or not document.json_scripts[0][0]:
            issue(filename, "json_ld_script", "Exactly one JSON-LD script must appear in the head")
            continue
        try:
            graph = _load_json(document.json_scripts[0][1])
            visible = _text(" ".join(document.visible))
            if include_coming_soon and stem[:2].upper() not in DEFAULT_REGISTRY.states:
                if (
                    not isinstance(graph, dict)
                    or graph.get("@context") != "https://schema.org"
                    or graph.get("@type") != "WebPage"
                    or graph.get("@id") != canonical
                    or graph.get("url") != canonical
                    or len(document.titles) != 1
                    or graph.get("name") != document.titles[0][1]
                    or not graph.get("description")
                    or graph.get("description") not in visible
                    or "Guide coming soon." not in visible
                    or "have not yet been reviewed" not in visible
                    or any(
                        n.get("@type") in {"Offer", "GovernmentService"} for n in _objects(graph)
                    )
                    or not any(
                        a.get("name") == "robots" and a.get("content") == "noindex, follow"
                        for a in metas
                    )
                ):
                    issue(filename, "placeholder", "Coming-soon page must disclose missing review")
            else:
                for problem in _schema_errors(graph, canonical, visible):
                    issue(filename, "json_ld_schema", problem)
            markdown = content.get(stem + ".md", "")
            scripts = _JSON_SCRIPT.findall(markdown)
            if len(scripts) != 1 or _load_json(scripts[0]) != graph:
                issue(stem + ".md", "markdown_schema", "Markdown JSON-LD must match the HTML graph")
        except (ValueError, TypeError, RecursionError):
            issue(
                filename,
                "invalid_json_ld",
                "Structured data must be valid bounded JSON without duplicate keys",
            )
    for filename, document in documents.items():
        for link in document.links:
            try:
                resolved = _resolve_link(
                    link, origin + "/" + filename.removesuffix(".html"), origin, files
                )
                if resolved and resolved[1] and resolved[0].endswith(".html"):
                    if (
                        resolved[0] not in documents
                        or resolved[1] not in documents[resolved[0]].ids
                    ):
                        raise ValueError("HTML anchor fragment has no matching target ID")
            except ValueError as exc:
                issue(filename, "broken_link", str(exc))
    for filename, source in content.items():
        if filename.endswith(".md") or filename == "llms.txt":
            visible = _JSON_SCRIPT.sub("", source)
            for link in _MD_LINK.findall(visible):
                try:
                    _resolve_link(html.unescape(link), origin + "/" + filename, origin, files)
                except ValueError as exc:
                    issue(filename, "broken_link", str(exc))
    if "llms.txt" in content:
        discovered = _MD_LINK.findall(content["llms.txt"])
        expected_urls = {origin + route for route in routes}
        if len(discovered) != len(routes) or set(discovered) != expected_urls:
            issue(
                "llms.txt",
                "discovery",
                "Discovery must link each canonical route exactly once",
            )
    if "robots.txt" in content:
        for agent in ("*", "GPTBot", "OAI-SearchBot", "PerplexityBot"):
            targets = routes + tuple(
                "/" + name for name in sorted(files) if not name.endswith(".html")
            )
            if any(not _robots_allows(content["robots.txt"], agent, route) for route in targets):
                issue(
                    "robots.txt",
                    "blocked_target",
                    f"Crawler {agent} is blocked from a required asset",
                )
    checks = 0
    if check_live and not errors:
        from .health import verify_live_assets

        failures = verify_live_assets(root, origin)
        for problem in failures:
            issue("deployment", "live_asset", problem)
        if not failures:
            checks = len(expected_files)
    return SiteVerificationReport(len(files), len(documents), routes, tuple(errors), checks)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--include-coming-soon", action="store_true")
    args = parser.parse_args(argv)
    report = verify_site(
        args.output_dir,
        base_url=args.base_url,
        check_live=args.check_live,
        include_coming_soon=args.include_coming_soon,
    )
    if not report.ok:
        for error in report.errors:
            message = f"{error.file}: {error.code}: {error.message}"
            print(message)
            if os.environ.get("GITHUB_ACTIONS") == "true":
                annotation = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print("::error::" + annotation)
        print(f"Verification failed with {len(report.errors)} issue(s).")
        return 1
    suffix = f"; {report.live_checks} live assets match" if args.check_live else ""
    print(
        f"Verified {report.files} files, {report.pages} pages and "
        f"{len(report.routes)} extensionless routes{suffix}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
