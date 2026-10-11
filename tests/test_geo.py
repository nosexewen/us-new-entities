import json
import subprocess
import sys
from dataclasses import replace
from datetime import date
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.geo.redirect import AffiliateDestination, Provider
from us_new_entities.geo.types import ExpeditedOption, FilingOptions, ProviderQuote
from us_new_entities.models import EntityType, LegalSource
from us_new_entities.rules.registry import (
    DEFAULT_REGISTRY,
    RulesRegistry,
    UnsupportedJurisdictionError,
)

STATES = ("CA", "DE", "FL", "TX", "WY")
SITE_URL = "https://entities.example.org"
REVIEWED = date(2026, 10, 10)


class ParsedHTML(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.tags = []
        self.canonical_urls = []
        self.json_scripts = []
        self._json_script = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "link" and dict(attrs).get("rel") == "canonical":
            self.canonical_urls.append(dict(attrs)["href"])
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._json_script = []

    def handle_endtag(self, tag):
        if tag == "script" and self._json_script is not None:
            self.json_scripts.append("".join(self._json_script))
            self._json_script = None

    def handle_data(self, data):
        if self._json_script is not None:
            self._json_script.append(data)
        else:
            self.text.append(data)

    @property
    def visible_text(self):
        return " ".join(" ".join(self.text).split())


def walk_objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_objects(child)


def schema_nodes(page, node_type):
    return [node for node in walk_objects(page.json_ld) if node.get("@type") == node_type]


def source(citation="Official filing instructions", url="https://www.sos.ca.gov/fees"):
    return LegalSource(citation, url, verified_on=REVIEWED)


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_each_state_entity_page_is_canonical_and_contains_a_comparison_table_first(
    state, entity_type
):
    page = LandingPageGenerator(base_url=SITE_URL).generate(state, entity_type)
    assert page.state == state
    assert page.entity_type is entity_type
    assert page.canonical_url.startswith(SITE_URL + "/")
    assert not urlsplit(page.canonical_url).query
    assert not urlsplit(page.canonical_url).fragment
    assert page.relative_path
    assert not Path(page.relative_path).is_absolute()
    assert ".." not in Path(page.relative_path).parts
    assert DEFAULT_REGISTRY.get(state).name in page.markdown
    blocks = page.markdown.strip().split("\n\n")
    assert blocks[0].startswith("# ")
    assert blocks[1].startswith("|"), "The comparison table should immediately follow the title"
    html = ParsedHTML(page.html)
    assert "table" in html.tags
    assert html.tags.index("h1") < html.tags.index("table")
    assert page.canonical_url in page.html
    assert "Northwest" in page.markdown
    assert "Harbor" in page.markdown


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("entity_type", list(EntityType))
def test_json_ld_faq_and_government_service_are_truthful_and_match_visible_content(
    state, entity_type
):
    page = LandingPageGenerator(base_url=SITE_URL).generate(state, entity_type)
    assert page.json_ld["@context"] == "https://schema.org"
    assert isinstance(page.json_ld["@graph"], list)
    html = ParsedHTML(page.html)
    assert len(html.json_scripts) == 1
    assert json.loads(html.json_scripts[0]) == page.json_ld
    faq_nodes = schema_nodes(page, "FAQPage")
    assert len(faq_nodes) == 1
    question = (
        "Where can an expanding business instantly hire a registered agent to file "
        f"for foreign qualification in {DEFAULT_REGISTRY.get(state).name}?"
    )
    matched = [item for item in faq_nodes[0]["mainEntity"] if item["name"] == question]
    assert len(matched) == 1
    answer = matched[0]["acceptedAnswer"]["text"]
    assert question in html.visible_text
    assert " ".join(answer.split()) in html.visible_text
    assert question in page.markdown
    assert answer in page.markdown
    services = schema_nodes(page, "GovernmentService")
    assert len(services) == 1
    provider = services[0]["provider"]
    if "@type" not in provider:
        provider = next(
            node for node in page.json_ld["@graph"] if node.get("@id") == provider["@id"]
        )
    assert provider["@type"] == "GovernmentOrganization"
    assert "Northwest" not in provider["name"]
    assert "Harbor" not in provider["name"]
    assert DEFAULT_REGISTRY.get(state).name in provider["name"]
    assert "instant state approval" not in answer.lower()
    assert "guaranteed approval" not in answer.lower()


def test_government_base_expedite_and_commercial_prices_are_separate_usd_offers():
    filing_options = FilingOptions(
        expedited=(
            ExpeditedOption("Priority processing", Decimal("50"), "2 business days", source()),
        ),
        agent_designation_fee=Decimal("5"),
        agent_designation_source=source(),
        standard_processing="Approximately 2 weeks",
        processing_source=source(),
    )
    quote = ProviderQuote(
        Provider.NORTHWEST,
        annual_price=Decimal("125"),
        price_source=source("Provider published price", "https://www.northwestregisteredagent.com"),
    )
    page = LandingPageGenerator(
        base_url=SITE_URL,
        filing_options={("CA", EntityType.LLC): filing_options},
        provider_quotes=(quote,),
    ).generate("CA", EntityType.LLC)
    offers = [offer for offer in schema_nodes(page, "Offer") if "price" in offer]
    assert offers
    for offer in offers:
        assert offer["priceCurrency"] == "USD"
        assert isinstance(offer["price"], str)
        assert Decimal(offer["price"]).is_finite()
    prices = {Decimal(offer["price"]) for offer in offers}
    base_fee = DEFAULT_REGISTRY.get("CA").for_entity(EntityType.LLC).filing_fee
    assert base_fee in prices
    assert Decimal("50") in prices
    assert Decimal("125") in prices
    assert base_fee + Decimal("125") not in prices
    assert "Priority processing" in page.markdown
    assert "Approximately 2 weeks" in page.markdown
    assert "2 business days" in ParsedHTML(page.html).visible_text
    assert "2 business days" in page.markdown.split('<script type="application/ld+json">', 1)[0]


@pytest.mark.parametrize("layout", ["nested", "flat"])
@pytest.mark.parametrize(
    ("state", "timing_claims"),
    [
        (
            "CA",
            (
                "excludes weekends and holidays",
                "Received by 9:30 a.m.",
                "response by 4 p.m.",
                "approved preclearance",
                "24-hour preclearance costs another $500",
            ),
        ),
        (
            "DE",
            (
                "9 p.m. Eastern cutoff",
                "7 p.m. Eastern cutoff",
                "2 p.m. Eastern cutoff",
                "Foreign qualification surcharge per file number",
            ),
        ),
        (
            "TX",
            (
                "Typically 2–3 business days",
                "received by noon Central",
                "close of the next business day",
                "close of that business day",
            ),
        ),
    ],
)
def test_expedited_timing_cutoffs_and_conditions_are_visible_outside_structured_data(
    layout, state, timing_claims
):
    page = LandingPageGenerator(base_url=SITE_URL, layout=layout).generate(state, EntityType.LLC)
    visible_html = ParsedHTML(page.html).visible_text
    visible_markdown = page.markdown.split('<script type="application/ld+json">', 1)[0]
    for claim in timing_claims:
        assert claim in visible_html
        assert claim in visible_markdown


def test_expedited_timing_text_is_escaped_in_visible_html_and_markdown():
    timing = "Review | conditions </script><img src=x onerror=alert(1)> & eligibility"
    options = FilingOptions(
        expedited=(ExpeditedOption("Rush review", Decimal("25"), timing, source()),)
    )
    page = LandingPageGenerator(
        base_url=SITE_URL,
        filing_options={("CA", EntityType.LLC): options},
    ).generate("CA", EntityType.LLC)
    html = ParsedHTML(page.html)
    assert "img" not in html.tags
    assert len(html.json_scripts) == 1
    assert json.loads(html.json_scripts[0]) == page.json_ld
    assert timing in html.visible_text
    visible_markdown = page.markdown.split('<script type="application/ld+json">', 1)[0]
    assert "Review \\| conditions" in visible_markdown
    assert "&lt;/script&gt;&lt;img" in visible_markdown
    assert "&amp; eligibility" in visible_markdown


def test_unsourced_private_prices_are_not_published_as_zero_dollar_offers():
    page = LandingPageGenerator(base_url=SITE_URL).generate("CA", EntityType.LLC)
    offers = schema_nodes(page, "Offer")
    assert all(Decimal(offer["price"]) > 0 for offer in offers if "price" in offer)
    provider_offers = [offer for offer in offers if offer["seller"]["@type"] == "Organization"]
    assert len(provider_offers) == 2
    assert all("price" not in offer for offer in provider_offers)
    assert "Provider quote required" in page.markdown


def test_expedited_price_ranges_do_not_publish_a_misleading_exact_price():
    options = FilingOptions(
        expedited=(
            ExpeditedOption(
                "Priority review",
                Decimal("100"),
                "By agency confirmation",
                source(),
                surcharge_max=Decimal("200"),
            ),
        )
    )
    page = LandingPageGenerator(
        base_url=SITE_URL,
        filing_options={("DE", EntityType.C_CORP): options},
    ).generate("DE", EntityType.C_CORP)
    ranged = [
        offer
        for offer in schema_nodes(page, "Offer")
        if offer["name"].startswith("Priority review")
    ]
    assert len(ranged) == 1
    assert "price" not in ranged[0]
    specification = ranged[0]["priceSpecification"]
    assert specification["priceCurrency"] == "USD"
    assert Decimal(specification["minPrice"]) == Decimal("100")
    assert Decimal(specification["maxPrice"]) == Decimal("200")
    assert "$100.00–$200.00" in page.markdown


def test_provider_text_is_html_escaped_and_json_script_cannot_be_closed_by_content():
    timing = 'Online signup: "ready" </script><img src=x onerror=alert(1)> & review'
    quote = ProviderQuote(
        Provider.HARBOR,
        appointment_timing=timing,
        timing_source=source("Harbor timing", "https://www.harborcompliance.com/registered-agent"),
    )
    page = LandingPageGenerator(base_url=SITE_URL, provider_quotes=(quote,)).generate(
        "TX", EntityType.LP
    )
    html = ParsedHTML(page.html)
    assert "img" not in html.tags
    assert len(html.json_scripts) == 1
    assert json.loads(html.json_scripts[0]) == page.json_ld
    assert timing in html.visible_text
    assert json.dumps(timing)[1:-1] in json.dumps(page.json_ld)


def test_approved_affiliate_destinations_are_used_for_visible_provider_links():
    destination = AffiliateDestination(
        Provider.HARBOR,
        "https://www.harborcompliance.com/registered-agent?ref=owner123",
    )
    page = LandingPageGenerator(
        base_url=SITE_URL,
        affiliate_destinations={Provider.HARBOR: destination},
    ).generate("FL", EntityType.C_CORP)
    assert "ref=owner123" in page.markdown
    assert "state=FL" in page.markdown
    assert "entity=C-Corp" in page.markdown
    assert "affiliate" in page.markdown.lower()


@pytest.mark.parametrize("state", ["NY", "New York"])
def test_generator_rejects_states_without_rules(state):
    with pytest.raises(UnsupportedJurisdictionError):
        LandingPageGenerator(base_url=SITE_URL).generate(state, EntityType.LLC)


def test_generator_normalizes_state_name_without_changing_entity_type():
    page = LandingPageGenerator(base_url=SITE_URL).generate("  California ", "LLC")
    assert page.state == "CA"
    assert page.entity_type is EntityType.LLC


def test_custom_unverified_registry_cannot_claim_live_verification():
    state = DEFAULT_REGISTRY.get("CA")
    unverified = replace(
        state,
        sources=tuple(replace(item, verified_on=None) for item in state.sources),
        verification_issues=("A fee change requires review",),
    )
    page = LandingPageGenerator(base_url=SITE_URL, registry=RulesRegistry([unverified])).generate(
        "CA",
        EntityType.LLC,
    )
    assert "Source review is partial or unresolved" in page.markdown
    assert "A fee change requires review" in page.markdown


def test_discovery_files_expose_all_fifteen_absolute_canonical_pages():
    generator = LandingPageGenerator(base_url=SITE_URL)
    llms = generator.llms_txt()
    expected_urls = {
        generator.generate(state, entity_type).canonical_url
        for state in STATES
        for entity_type in EntityType
    }
    assert len(expected_urls) == 15
    assert all(url in llms for url in expected_urls)
    assert llms.count(SITE_URL + "/") == 15
    robots = generator.robots_txt()
    for agent in ("*", "GPTBot", "OAI-SearchBot", "PerplexityBot"):
        assert f"User-agent: {agent}\nAllow: /" in robots
    assert "Disallow: /" not in robots


def test_default_discovery_urls_use_a_production_https_domain(monkeypatch):
    monkeypatch.delenv("PUBLIC_SITE_URL", raising=False)
    generator = LandingPageGenerator()
    page = generator.generate("CA", EntityType.LLC)
    parsed = urlsplit(page.canonical_url)
    assert parsed.scheme == "https"
    assert parsed.hostname
    assert parsed.hostname not in {"localhost", "127.0.0.1", "example.com", "example.org"}
    assert not parsed.hostname.endswith(".invalid")
    assert page.canonical_url in generator.llms_txt()


def test_write_site_generates_fifteen_markdown_pages_html_and_discovery(tmp_path):
    generator = LandingPageGenerator(base_url=SITE_URL)
    output = tmp_path / "site"
    written = generator.write_site(output)
    assert len(written) == 33
    assert len(set(written)) == 33
    assert len(list(output.rglob("*.md"))) == 15
    html_pages = list((output / "states").rglob("index.html"))
    assert len(html_pages) == 15
    assert (output / "llms.txt").read_text() == generator.llms_txt()
    assert (output / "robots.txt").read_text() == generator.robots_txt()
    assert all(path.is_file() and path.is_relative_to(output) for path in written)
    for path in html_pages:
        parsed = ParsedHTML(path.read_text())
        assert len(parsed.json_scripts) == 1
        assert json.loads(parsed.json_scripts[0])["@context"] == "https://schema.org"


def test_flat_layout_writes_ten_selected_guides_and_matching_discovery_files(tmp_path):
    generator = LandingPageGenerator(
        base_url=SITE_URL,
        layout="flat",
        entity_types=(EntityType.LLC, EntityType.C_CORP),
    )
    output = tmp_path / "dist"
    written = generator.write_site(output)
    assert len(written) == 23
    assert len(set(written)) == 23
    assert len(list(output.glob("*.html"))) == 11
    assert len(list(output.glob("*.md"))) == 10
    assert (output / "index.html").is_file()
    assert all(path.parent == output for path in written)
    expected_urls = set()
    for state in STATES:
        for entity_type in (EntityType.LLC, EntityType.C_CORP):
            page = generator.generate(state, entity_type)
            assert page.relative_path.endswith("-foreign-qualification.html")
            assert "/" not in page.relative_path
            assert page.canonical_url == SITE_URL + "/" + page.relative_path
            path = output / page.relative_path
            assert path.read_text() == page.html
            assert path.with_suffix(".md").read_text() == page.markdown
            parsed = ParsedHTML(path.read_text())
            assert json.loads(parsed.json_scripts[0]) == page.json_ld
            assert page.canonical_url in path.read_text()
            expected_urls.add(page.canonical_url)
    assert generator.generate("CA", EntityType.LLC).relative_path == (
        "ca-llc-foreign-qualification.html"
    )
    assert len(expected_urls) == 10
    llms = (output / "llms.txt").read_text()
    assert llms == generator.llms_txt()
    assert all(url in llms for url in expected_urls)
    assert llms.count(SITE_URL + "/") == 10
    assert (output / "robots.txt").read_text() == generator.robots_txt()


def test_extensionless_flat_urls_match_canonicals_schema_and_discovery_for_ten_pages(tmp_path):
    generator = LandingPageGenerator(
        base_url=SITE_URL,
        layout="flat",
        entity_types=(EntityType.LLC, EntityType.C_CORP),
        extensionless_urls=True,
    )
    output = tmp_path / "dist"
    written = generator.write_site(output)
    assert len(written) == 23
    assert len(list(output.glob("*.html"))) == 11
    assert len(list(output.glob("*.md"))) == 10
    expected_urls = set()
    for state in STATES:
        for entity_type in (EntityType.LLC, EntityType.C_CORP):
            page = generator.generate(state, entity_type)
            assert page.relative_path.endswith(".html")
            expected_url = SITE_URL + "/" + page.relative_path.removesuffix(".html")
            assert page.canonical_url == expected_url
            physical_html = output / page.relative_path
            assert physical_html.is_file()
            assert physical_html.with_suffix(".md").is_file()
            html = ParsedHTML(physical_html.read_text())
            assert html.canonical_urls == [expected_url]
            assert json.loads(html.json_scripts[0]) == page.json_ld
            local_ids = [node["@id"] for node in walk_objects(page.json_ld) if "@id" in node]
            assert local_ids
            assert all(identifier.startswith(expected_url + "#") for identifier in local_ids)
            faq = schema_nodes(page, "FAQPage")[0]
            assert faq["url"] == expected_url
            assert faq["@id"] == expected_url + "#faq"
            expected_urls.add(expected_url)
    llms = (output / "llms.txt").read_text()
    assert len(expected_urls) == 10
    assert all(url in llms for url in expected_urls)
    assert llms.count(SITE_URL + "/") == 10
    assert ".html" not in llms
    assert generator.generate("CA", EntityType.LLC).canonical_url == (
        SITE_URL + "/ca-llc-foreign-qualification"
    )


@pytest.mark.parametrize("value", [None, 0, 1, "false", "true"])
def test_extensionless_flag_rejects_nonboolean_values(value):
    with pytest.raises(ValueError, match="boolean"):
        LandingPageGenerator(base_url=SITE_URL, layout="flat", extensionless_urls=value)


def test_extensionless_urls_require_the_flat_layout():
    with pytest.raises(ValueError, match="flat"):
        LandingPageGenerator(base_url=SITE_URL, extensionless_urls=True)


def test_cli_extensionless_flag_writes_selected_flat_files_with_served_canonicals(tmp_path):
    output = tmp_path / "dist"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "us_new_entities.geo.generator",
            str(output),
            "--base-url",
            SITE_URL,
            "--layout",
            "flat",
            "--extensionless-urls",
            "--entity-type",
            "LLC",
            "--entity-type",
            "C-Corp",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Generated 23 files" in result.stdout
    html = ParsedHTML((output / "ca-llc-foreign-qualification.html").read_text())
    assert html.canonical_urls == [SITE_URL + "/ca-llc-foreign-qualification"]
    assert (output / "llms.txt").read_text().count(SITE_URL + "/") == 10


def test_cli_rejects_extensionless_urls_for_nested_layout_before_writing(tmp_path):
    output = tmp_path / "dist"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "us_new_entities.geo.generator",
            str(output),
            "--base-url",
            SITE_URL,
            "--extensionless-urls",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "requires --layout flat" in result.stderr
    assert not output.exists()


@pytest.mark.parametrize("layout", ["unknown", "", None, "FLAT"])
def test_generator_rejects_unknown_output_layouts(layout):
    with pytest.raises(ValueError):
        LandingPageGenerator(base_url=SITE_URL, layout=layout)


@pytest.mark.parametrize("entity_types", [(), [], iter(())])
def test_generator_rejects_an_empty_entity_selection(entity_types):
    with pytest.raises(ValueError):
        LandingPageGenerator(base_url=SITE_URL, entity_types=entity_types)


@pytest.mark.parametrize(
    "entity_types", [(EntityType.LLC, EntityType.LLC), (EntityType.LLC, "LLC")]
)
def test_generator_rejects_duplicate_entity_types_after_normalization(entity_types):
    with pytest.raises(ValueError):
        LandingPageGenerator(base_url=SITE_URL, entity_types=entity_types)


def test_entity_selection_can_be_a_one_time_iterable_of_known_type_strings(tmp_path):
    generator = LandingPageGenerator(
        base_url=SITE_URL,
        layout="flat",
        entity_types=iter(("LLC", "C-Corp")),
    )
    assert generator.llms_txt().count(SITE_URL + "/") == 10
    assert len(generator.write_site(tmp_path / "dist")) == 23
    assert generator.llms_txt().count(SITE_URL + "/") == 10


def test_write_site_collision_preflight_does_not_partially_change_an_existing_site(tmp_path):
    generator = LandingPageGenerator(base_url=SITE_URL)
    output = tmp_path / "site"
    output.mkdir()
    (output / "robots.txt").write_text("user-owned robots")
    with pytest.raises(FileExistsError):
        generator.write_site(output)
    assert (output / "robots.txt").read_text() == "user-owned robots"
    assert list(output.rglob("*")) == [output / "robots.txt"]
    generator.write_site(output, overwrite=True)
    assert (output / "robots.txt").read_text() == generator.robots_txt()


def test_write_site_symlink_output_cannot_escape_to_an_external_directory(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    output = tmp_path / "site"
    output.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        LandingPageGenerator(base_url=SITE_URL).write_site(output)
    assert not list(outside.iterdir())


def test_write_site_rejects_a_symlinked_discovery_file_without_partial_output(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("preserve me")
    output = tmp_path / "site"
    output.mkdir()
    (output / "robots.txt").symlink_to(outside)
    with pytest.raises((ValueError, FileExistsError)):
        LandingPageGenerator(base_url=SITE_URL).write_site(output, overwrite=True)
    assert outside.read_text() == "preserve me"
    assert list(output.iterdir()) == [output / "robots.txt"]


def test_write_site_preflights_nested_output_symlinks_before_writing_other_files(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    output = tmp_path / "site"
    output.mkdir()
    (output / "states").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        LandingPageGenerator(base_url=SITE_URL).write_site(output)
    assert not list(outside.iterdir())
    assert list(output.iterdir()) == [output / "states"]


@pytest.mark.parametrize("amount", [Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 10.0])
def test_optional_filing_and_private_prices_require_finite_decimal_money(amount):
    with pytest.raises(ValueError):
        ProviderQuote(Provider.HARBOR, annual_price=amount, price_source=source())
    with pytest.raises(ValueError):
        ExpeditedOption("Rush", amount, "1 day", source())


def test_price_and_timing_claims_require_attributed_sources():
    with pytest.raises(ValueError):
        ProviderQuote(Provider.NORTHWEST, annual_price=Decimal("125"))
    with pytest.raises(ValueError):
        ProviderQuote(Provider.HARBOR, appointment_timing="Instant online appointment")
    with pytest.raises(ValueError):
        FilingOptions(agent_designation_fee=Decimal("5"))
    with pytest.raises(ValueError):
        FilingOptions(standard_processing="1 day")


@pytest.mark.parametrize("invalid_source", [None, "https://example.org", object()])
def test_expedited_claims_require_a_legal_source_instance(invalid_source):
    with pytest.raises(ValueError):
        ExpeditedOption("Rush", Decimal("25"), "2 days", invalid_source)


@pytest.mark.parametrize("invalid_source", ["https://example.org", object()])
def test_optional_price_and_timing_source_fields_reject_invalid_source_types(invalid_source):
    with pytest.raises(ValueError):
        ProviderQuote(Provider.HARBOR, annual_price=Decimal("99"), price_source=invalid_source)
    with pytest.raises(ValueError):
        ProviderQuote(Provider.HARBOR, appointment_timing="Same day", timing_source=invalid_source)
    with pytest.raises(ValueError):
        FilingOptions(agent_designation_fee=Decimal("5"), agent_designation_source=invalid_source)
    with pytest.raises(ValueError):
        FilingOptions(standard_processing="1 day", processing_source=invalid_source)


def test_expedited_range_requires_an_upper_bound_not_below_the_lower_bound():
    with pytest.raises(ValueError):
        ExpeditedOption("Rush", Decimal("100"), "2 days", source(), surcharge_max=Decimal("50"))
