"""Production artifacts fail the gate when metadata, graph or link behavior changes."""

import json
import re
import subprocess
import sys
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest
from us_new_entities.geo.generator import LandingPageGenerator
from us_new_entities.geo.verify import (
    SiteVerificationReport,
    VerificationIssue,
    main,
    verify_site,
)
from us_new_entities.models import EntityType
from us_new_entities.rules.registry import DEFAULT_REGISTRY

BASE = "https://us-new-entities.pages.dev"
PAGE = "ca-llc-foreign-qualification.html"
SCRIPT = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL)


@pytest.fixture
def site(tmp_path, monkeypatch):
    for key in ("PUBLIC_SITE_URL", "NORTHWEST_AFFILIATE_URL", "HARBOR_AFFILIATE_URL"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "dist"
    LandingPageGenerator(
        base_url=BASE,
        layout="flat",
        entity_types=(EntityType.LLC, EntityType.C_CORP),
        extensionless_urls=True,
    ).write_site(root)
    return root


def codes(report):
    return {issue.code for issue in report.errors}


def replace_html(site, old, new):
    path = site / PAGE
    source = path.read_text()
    assert old in source
    path.write_text(source.replace(old, new, 1))


def mutate_graph(site, mutate):
    source = (site / PAGE).read_text()
    graph = json.loads(SCRIPT.search(source)[2])
    mutate(graph)
    for suffix in (".html", ".md"):
        path = site / PAGE.replace(".html", suffix)
        path.write_text(
            SCRIPT.sub(lambda match: match[1] + json.dumps(graph) + match[3], path.read_text())
        )


def test_current_production_artifact_contract_passes_without_network(site):
    report = verify_site(site, base_url=BASE)
    assert report.ok, report.errors
    assert report.files == 4 * len(DEFAULT_REGISTRY.states) + 3
    assert report.pages == 2 * len(DEFAULT_REGISTRY.states) + 1
    assert len(report.routes) == 2 * len(DEFAULT_REGISTRY.states)
    assert "/ca-llc-foreign-qualification" in report.routes
    assert report.live_checks == 0
    with pytest.raises(FrozenInstanceError):
        report.files = 0


def test_all_50_states_have_reviewed_guides_or_explicit_placeholders(site):
    generator = LandingPageGenerator(
        base_url=BASE,
        layout="flat",
        entity_types=(EntityType.LLC, EntityType.C_CORP),
        extensionless_urls=True,
        include_coming_soon=True,
    )
    generator.write_site(site, overwrite=True)
    report = verify_site(site, base_url=BASE, include_coming_soon=True)
    assert report.ok, report.errors
    assert report.files == 203
    assert report.pages == 101
    directory_path = site / "index.html"
    state_headings = re.findall(r"<h3>(.*?)</h3>", directory_path.read_text())
    assert len(state_headings) == 50
    assert state_headings == sorted(state_headings)
    assert state_headings[0] == "Alabama"
    assert state_headings[-1] == "Wyoming"
    assert directory_path.read_text().count("<a href=") == 100
    assert "Guide coming soon" in directory_path.read_text()
    assert len({route[1:3] for route in report.routes}) == 50
    assert not any(route.startswith("/dc-") for route in report.routes)
    placeholder = site / "ri-llc-foreign-qualification.html"
    source = placeholder.read_text()
    assert "Guide coming soon." in source
    assert "noindex, follow" in source
    graph = json.loads(SCRIPT.search(source)[2])
    assert graph["@type"] == "WebPage"
    assert "Offer" not in graph
    assert "GovernmentService" not in source
    assert "GovernmentService" in (site / PAGE).read_text()
    placeholder.write_text(source.replace("Guide coming soon.", "Guide available."))
    assert "placeholder" in codes(verify_site(site, base_url=BASE, include_coming_soon=True))


def test_default_origin_is_read_from_current_environment(site, monkeypatch):
    monkeypatch.setenv("PUBLIC_SITE_URL", BASE)
    assert verify_site(site).ok


def test_directory_requires_complete_links_and_valid_html(site):
    path = site / "index.html"
    source = path.read_text()
    path.write_text(source.replace(f'{BASE}/ca-llc-foreign-qualification"', f'{BASE}/missing"'))
    assert {"directory", "broken_link"} <= codes(verify_site(site, base_url=BASE))
    path.write_text(source.replace("</nav>", ""))
    assert "invalid_html" in codes(verify_site(site, base_url=BASE))


@pytest.mark.parametrize(
    "old,new,expected",
    [
        ("<!doctype html>", "", "doctype"),
        ('lang="en"', 'lang="fr"', "language"),
        ('charset="utf-8"', 'charset="iso-8859-1"', "charset"),
        ('name="viewport"', 'name="other"', "viewport"),
        ('rel="canonical"', 'rel="alternate"', "canonical"),
        (BASE + '/ca-llc-foreign-qualification"', BASE + '/wrong"', "canonical"),
        ("</main>", "", "invalid_html"),
    ],
)
def test_html_header_and_structure_mutations_fail(site, old, new, expected):
    replace_html(site, old, new)
    assert expected in codes(verify_site(site, base_url=BASE))


def test_title_in_body_does_not_satisfy_head_metadata(site):
    path = site / PAGE
    source = path.read_text()
    title = re.search(r"<title>.*?</title>", source)[0]
    path.write_text(source.replace(title, "").replace("<body>", "<body>" + title))
    assert "title" in codes(verify_site(site, base_url=BASE))


def test_json_ld_script_must_be_in_head(site):
    path = site / PAGE
    source = path.read_text()
    script = SCRIPT.search(source)[0]
    path.write_text(source.replace(script, "").replace("<body>", "<body>" + script))
    assert "json_ld_script" in codes(verify_site(site, base_url=BASE))


def test_malformed_json_is_reported_without_crashing(site):
    replace_html(site, '{"@context":', '{bad "@context":')
    assert "invalid_json_ld" in codes(verify_site(site, base_url=BASE))


def test_duplicate_json_keys_are_rejected(site):
    replace_html(
        site,
        '{"@context": "https://schema.org",',
        '{"@context": "https://schema.org", "@context": "https://schema.org",',
    )
    assert "invalid_json_ld" in codes(verify_site(site, base_url=BASE))


@pytest.mark.parametrize(
    "mutate",
    [
        lambda graph: graph.update({"@context": "http://schema.org"}),
        lambda graph: graph.update({"@graph": []}),
        lambda graph: graph["@graph"][0].update({"@type": "Unknown"}),
        lambda graph: graph["@graph"][0].update({"offers": [{"@id": BASE + "/missing#offer"}]}),
        lambda graph: graph["@graph"][1].update({"priceCurrency": "EUR"}),
        lambda graph: graph["@graph"][1].update({"price": "NaN"}),
        lambda graph: graph["@graph"][1].update({"price": "-1.00"}),
        lambda graph: graph["@graph"][1].update({"price": True}),
        lambda graph: graph["@graph"][-1].update({"url": BASE + "/wrong"}),
        lambda graph: graph["@graph"][-1]["mainEntity"][0].update({"name": "Invisible question?"}),
    ],
)
def test_minimal_graph_contract_mutations_fail(site, mutate):
    mutate_graph(site, mutate)
    assert "json_ld_schema" in codes(verify_site(site, base_url=BASE))


def test_semantic_graph_fragments_do_not_require_dom_ids(site):
    assert 'id="faq"' not in (site / PAGE).read_text()
    assert verify_site(site, base_url=BASE).ok


def test_unsourced_private_price_cannot_be_invented(site):
    def mutate(graph):
        private = next(
            n
            for n in graph["@graph"]
            if n.get("@type") == "Offer" and n["seller"]["@type"] == "Organization"
        )
        private["price"] = "0.00"

    mutate_graph(site, mutate)
    report = verify_site(site, base_url=BASE)
    assert any(
        "Private price requires source attribution" in issue.message for issue in report.errors
    )


def test_private_offer_can_remain_unpriced(site):
    assert verify_site(site, base_url=BASE).ok


def test_markdown_graph_must_match_html(site):
    path = site / PAGE.replace(".html", ".md")
    path.write_text(path.read_text().replace('"price": "70.00"', '"price": "71.00"', 1))
    assert "markdown_schema" in codes(verify_site(site, base_url=BASE))


@pytest.mark.parametrize(
    "link",
    [
        "missing.html",
        "/missing",
        "ca-llc-foreign-qualification#missing-id",
        "javascript:alert(1)",
        "http://official.example/",
    ],
)
def test_broken_relative_routes_fragments_and_unsafe_links_fail(site, link):
    replace_html(site, "<main>", f'<main><a href="{link}">Link</a>')
    assert "broken_link" in codes(verify_site(site, base_url=BASE))


def test_internal_relative_routes_and_real_dom_fragments_resolve(site):
    replace_html(
        site,
        "<main>",
        '<main><a href="de-llc-foreign-qualification#target">DE</a>'
        '<a href="ca-llc-foreign-qualification.md">Markdown</a>',
    )
    target = site / "de-llc-foreign-qualification.html"
    target.write_text(target.read_text().replace("<main>", '<main><p id="target">Target</p>'))
    assert verify_site(site, base_url=BASE).ok


def test_external_https_source_link_is_accepted_without_fetching(site):
    replace_html(site, "<main>", '<main><a href="https://official.example/unknown#id">Source</a>')
    assert verify_site(site, base_url=BASE).ok


def test_markdown_broken_relative_link_is_checked(site):
    path = site / PAGE.replace(".html", ".md")
    path.write_text(path.read_text() + "\n[Broken](missing.md)\n")
    assert "broken_link" in codes(verify_site(site, base_url=BASE))


def test_discovery_requires_each_canonical_once(site):
    path = site / "llms.txt"
    path.write_text(
        path.read_text().replace("/ca-llc-foreign-qualification", "/de-llc-foreign-qualification")
    )
    assert "discovery" in codes(verify_site(site, base_url=BASE))


@pytest.mark.parametrize(
    "robot_rules",
    [
        "User-agent: *\nDisallow: /\n",
        "User-agent: GPTBot\nDisallow: /llms.txt\n",
        "User-agent: PerplexityBot\nDisallow: /ca-llc-foreign-qualification\n",
    ],
)
def test_robots_cannot_block_a_required_target(site, robot_rules):
    (site / "robots.txt").write_text(robot_rules)
    assert "blocked_target" in codes(verify_site(site, base_url=BASE))


def test_longest_robots_rule_and_allow_tie_take_precedence(site):
    (site / "robots.txt").write_text("User-agent: *\nDisallow: /\nAllow: /\n")
    assert verify_site(site, base_url=BASE).ok


def test_extra_and_missing_assets_fail_the_exact_flat_contract(site):
    (site / "extra.txt").write_text("Extra")
    (site / "llms.txt").unlink()
    assert {"extra_file", "missing_file"} <= codes(verify_site(site, base_url=BASE))


def test_symlinks_and_directories_are_not_followed(site, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (site / "nested").mkdir()
    (site / "external").symlink_to(outside, target_is_directory=True)
    assert "invalid_file" in codes(verify_site(site, base_url=BASE))


def test_root_symlink_is_rejected(site, tmp_path):
    link = tmp_path / "site-link"
    link.symlink_to(site, target_is_directory=True)
    assert "invalid_directory" in codes(verify_site(link, base_url=BASE))


def test_non_utf8_asset_is_rejected(site):
    (site / PAGE).write_bytes(b"\xff\xfe")
    assert "invalid_content" in codes(verify_site(site, base_url=BASE))


def test_wrong_origin_is_reported_as_canonical_and_discovery_errors(site):
    assert {"canonical", "discovery"} <= codes(verify_site(site, base_url="https://other.example"))


def test_invalid_origin_produces_a_structured_failure(site):
    assert "invalid_base_url" in codes(verify_site(site, base_url="http://invalid.example"))


def test_live_validation_is_opt_in_and_follows_local_success(site, monkeypatch):
    calls = []
    helper = SimpleNamespace(
        verify_live_assets=lambda root, origin: calls.append((root, origin)) or ()
    )
    monkeypatch.setitem(sys.modules, "us_new_entities.geo.health", helper)
    assert verify_site(site, base_url=BASE).ok
    assert calls == []
    report = verify_site(site, base_url=BASE, check_live=True)
    assert report.ok and report.live_checks == 4 * len(DEFAULT_REGISTRY.states) + 3
    assert calls == [(site, BASE)]
    (site / "llms.txt").unlink()
    assert not verify_site(site, base_url=BASE, check_live=True).ok
    assert len(calls) == 1


def test_live_helper_failure_produces_a_nonzero_cli_result(site, monkeypatch, capsys):
    helper = SimpleNamespace(
        verify_live_assets=lambda root, origin: ("Public asset returned HTTP 404",)
    )
    monkeypatch.setitem(sys.modules, "us_new_entities.geo.health", helper)
    assert main([str(site), "--base-url", BASE, "--check-live"]) == 1
    assert "live_asset" in capsys.readouterr().out


def test_cli_module_reports_success_and_nonzero_failure(site):
    command = [sys.executable, "-m", "us_new_entities.geo.verify", str(site), "--base-url", BASE]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert (
        f"Verified {4 * len(DEFAULT_REGISTRY.states) + 3} files, "
        f"{2 * len(DEFAULT_REGISTRY.states) + 1} pages and "
        f"{2 * len(DEFAULT_REGISTRY.states)} extensionless routes"
    ) in result.stdout
    (site / "robots.txt").unlink()
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "missing_file" in result.stdout


def test_github_error_annotations_escape_control_sequences(monkeypatch, capsys):
    import us_new_entities.geo.verify as module

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setattr(
        module,
        "verify_site",
        lambda *args, **kwargs: SiteVerificationReport(
            0,
            0,
            (),
            (VerificationIssue("asset", "problem", "50%\r\nFailed"),),
        ),
    )
    assert main(["unused", "--base-url", BASE]) == 1
    assert "::error::asset: problem: 50%25%0D%0AFailed" in capsys.readouterr().out
