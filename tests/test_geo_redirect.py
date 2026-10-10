"""Provider destinations and owner tracking cannot be controlled by incoming queries."""

from dataclasses import FrozenInstanceError
from urllib.parse import parse_qsl, urlsplit

import pytest
from us_new_entities.geo.redirect import (
    AffiliateDestination,
    Provider,
    build_affiliate_url,
    get_public_site_url,
    load_geo_config,
    validate_public_site_url,
)


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for key in ("PUBLIC_SITE_URL", "NORTHWEST_AFFILIATE_URL", "HARBOR_AFFILIATE_URL"):
        monkeypatch.delenv(key, raising=False)


def query_fields(url):
    return parse_qsl(urlsplit(url).query, keep_blank_values=True)


def test_default_configuration_matches_user_supplied_placeholder_templates():
    assert get_public_site_url() == "https://compliance-hub.example.com"
    assert build_affiliate_url(Provider.NORTHWEST, {}) == (
        "https://www.northwestregisteredagent.com/?ref=EXAMPLE_AFFILIATE_ID"
    )
    assert build_affiliate_url(Provider.HARBOR, {}) == (
        "https://www.shareasale.com/r.cfm?b=99010&u=EXAMPLE_USER_ID&m=99010"
    )


@pytest.mark.parametrize("query", ["", "?", {}])
def test_empty_inputs_preserve_destination(query):
    destination = AffiliateDestination(Provider.HARBOR, "https://harborcompliance.com/?ref=owner")
    assert build_affiliate_url(Provider.HARBOR, query, destination=destination) == destination.url


def test_state_and_entity_are_normalized_and_campaign_values_are_encoded():
    url = build_affiliate_url(
        Provider.NORTHWEST,
        {
            "state": "New York",
            "entity": "C-Corp",
            "utm_campaign": "Research & growth / 2026 +",
            "utm_content": "Étude",
        },
    )
    assert dict(query_fields(url)) == {
        "ref": "EXAMPLE_AFFILIATE_ID",
        "state": "NY",
        "entity": "C-Corp",
        "utm_campaign": "Research & growth / 2026 +",
        "utm_content": "Étude",
    }
    assert "Research+%26+growth+%2F+2026+%2B" in url
    assert "%C3%89tude" in url


def test_sequence_values_are_supported_for_campaign_fields():
    url = build_affiliate_url(Provider.HARBOR, {"utm_term": ["one", "two"], "state": ["ca"]})
    assert query_fields(url)[-3:] == [("utm_term", "one"), ("utm_term", "two"), ("state", "CA")]


def test_unknown_private_and_destination_fields_are_dropped():
    url = build_affiliate_url(
        Provider.NORTHWEST,
        {
            "state": "CA",
            "entity": "LLC",
            "utm_source": "state-guide",
            "email": "person@example.com",
            "token": "secret",
            "sos_entity_id": "001234",
            "affiliate": "attacker",
            "ref": "attacker",
            "next": "https://evil.example",
            "url": "https://evil.example",
            "destination": "https://evil.example",
        },
    )
    assert urlsplit(url).hostname == "www.northwestregisteredagent.com"
    assert dict(query_fields(url)) == {
        "ref": "EXAMPLE_AFFILIATE_ID",
        "state": "CA",
        "entity": "LLC",
        "utm_source": "state-guide",
    }
    assert "person" not in url and "secret" not in url and "attacker" not in url


def test_owner_tracking_is_preserved_exactly_and_cannot_be_overwritten():
    owner_url = (
        "https://www.harborcompliance.com/registered-agent?ref=owner%2B123&affiliate_id=0088"
        "&utm_source=owned%20channel&STATE=TX"
    )
    destination = AffiliateDestination(Provider.HARBOR, owner_url)
    url = build_affiliate_url(
        Provider.HARBOR,
        "state=CA&entity=LP&utm_source=attacker&utm_medium=guide&ref=attacker&affiliate_id=9999",
        destination=destination,
    )
    assert url.startswith(owner_url + "&")
    assert query_fields(url) == [
        ("ref", "owner+123"),
        ("affiliate_id", "0088"),
        ("utm_source", "owned channel"),
        ("STATE", "TX"),
        ("entity", "LP"),
        ("utm_medium", "guide"),
    ]


@pytest.mark.parametrize(
    "query",
    [
        "state=CA&state=CA",
        "state=CA&state=TX",
        "entity=LLC&entity=LP",
        {"state": ["CA", "CA"]},
        {"entity": ["LLC", "LP"]},
    ],
)
def test_duplicate_state_or_entity_is_rejected(query):
    with pytest.raises(ValueError, match="Ambiguous duplicate"):
        build_affiliate_url(Provider.HARBOR, query)


@pytest.mark.parametrize("state", ["XX", "Ontario", "DC", "District of Columbia", ""])
def test_invalid_state_values_fail_explicitly(state):
    with pytest.raises(ValueError):
        build_affiliate_url(Provider.NORTHWEST, {"state": state})


@pytest.mark.parametrize("entity", ["AcmeCorp", "llc", "Corporation", "S-Corp", ""])
def test_unrecognized_entity_strings_fall_back_without_forwarding_the_company_name(entity):
    url = build_affiliate_url(Provider.NORTHWEST, {"entity": entity})
    assert dict(query_fields(url))["entity"] == "LLC"


@pytest.mark.parametrize("entity", ["LLC", "C-Corp", "LP"])
def test_recognized_entity_values_are_preserved(entity):
    url = build_affiliate_url(Provider.HARBOR, {"entity": entity})
    assert dict(query_fields(url))["entity"] == entity


def test_company_name_from_chatgpt_keeps_source_attribution_and_normalizes_entity():
    url = build_affiliate_url(Provider.NORTHWEST, "state=CA&entity=AcmeCorp&source=chatgpt")
    assert dict(query_fields(url)) == {
        "ref": "EXAMPLE_AFFILIATE_ID",
        "state": "CA",
        "entity": "LLC",
        "source": "chatgpt",
    }
    assert "AcmeCorp" not in url


@pytest.mark.parametrize(
    "query",
    [
        "source=chatgpt&utm_source=campaign",
        {"source": "chatgpt", "utm_source": "campaign"},
    ],
)
def test_both_source_attribution_fields_pass_through_without_coalescing(query):
    url = build_affiliate_url(Provider.HARBOR, query)
    assert dict(query_fields(url))["source"] == "chatgpt"
    assert dict(query_fields(url))["utm_source"] == "campaign"


@pytest.mark.parametrize(
    "owner_query,expected",
    [
        ("source=owned", {"source": "owned", "utm_source": "inbound-campaign"}),
        ("utm_source=owned", {"utm_source": "owned", "source": "inbound-source"}),
        (
            "source=owned-source&utm_source=owned-campaign",
            {"source": "owned-source", "utm_source": "owned-campaign"},
        ),
    ],
)
def test_owner_attribution_takes_precedence_independently_for_each_source_key(
    owner_query, expected
):
    destination = AffiliateDestination(
        Provider.NORTHWEST, "https://www.northwestregisteredagent.com/?" + owner_query
    )
    url = build_affiliate_url(
        Provider.NORTHWEST,
        "source=inbound-source&utm_source=inbound-campaign",
        destination=destination,
    )
    assert dict(query_fields(url)) == expected


def test_owner_source_keys_are_protected_case_insensitively():
    destination = AffiliateDestination(
        Provider.HARBOR,
        "https://harborcompliance.com/?SOURCE=owned-source&UTM_SOURCE=owned-campaign",
    )
    assert (
        build_affiliate_url(
            Provider.HARBOR,
            "source=inbound-source&utm_source=inbound-campaign",
            destination=destination,
        )
        == destination.url
    )


@pytest.mark.parametrize(
    "query",
    [
        "entity=AcmeCorp&entity=LLC",
        "entity=AcmeCorp&entity=AnotherCorp",
    ],
)
def test_entity_fallback_does_not_bypass_duplicate_rejection(query):
    with pytest.raises(ValueError, match="Ambiguous duplicate"):
        build_affiliate_url(Provider.HARBOR, query)


@pytest.mark.parametrize(
    "query",
    [
        "entity=Acme%0aCorp&source=chatgpt",
        "source=chat%0d%0agpt",
        {"entity": "Acme\nCorp"},
        {"source": "x" * 513},
    ],
)
def test_entity_fallback_and_source_forwarding_keep_control_and_size_checks(query):
    with pytest.raises(ValueError):
        build_affiliate_url(Provider.NORTHWEST, query)


def test_invalid_provider_fails_explicitly():
    with pytest.raises(ValueError):
        build_affiliate_url("other", "state=CA")


@pytest.mark.parametrize(
    "url",
    [
        "http://www.harborcompliance.com/registered-agent",
        "https://evil.example/registered-agent",
        "https://www.harborcompliance.com.evil.example/registered-agent",
        "https://www.harborcompliance.com@evil.example/registered-agent",
        "https://user:password@www.harborcompliance.com/registered-agent",
        "https://www.harborcompliance.com/registered-agent#section",
        "https://www.harborcompliance.com/registered-agent#",
        "https://www.harborcompliance.com:444/registered-agent",
        "https://www.harborcompliance.com\\@evil.example/registered-agent",
        "https://www.northwestregisteredagent.com/registered-agent",
        "//www.harborcompliance.com/registered-agent",
        "https://www.harborcompliance.com./registered-agent",
    ],
)
def test_destination_host_scheme_and_authority_are_validated(url):
    with pytest.raises(ValueError):
        AffiliateDestination(Provider.HARBOR, url)


def test_bare_origin_uses_safe_default_path():
    assert AffiliateDestination(Provider.HARBOR, "https://harborcompliance.com?ref=owner").url == (
        "https://harborcompliance.com/registered-agent?ref=owner"
    )


def test_destination_configuration_is_immutable():
    destination = AffiliateDestination(Provider.HARBOR, "https://harborcompliance.com")
    with pytest.raises(FrozenInstanceError):
        destination.url = "https://evil.example"


def test_destination_and_selected_provider_must_match():
    destination = AffiliateDestination(Provider.HARBOR, "https://harborcompliance.com")
    with pytest.raises(ValueError, match="does not match"):
        build_affiliate_url(Provider.NORTHWEST, "state=CA", destination=destination)


@pytest.mark.parametrize(
    "query",
    [
        "utm_source=a%0D%0AInjected",
        "utm_source=a%250dInjected",
        "utm_source=a%25250aInjected",
        "utm_source=a\nInjected",
        {"utm_source": "a\rInjected"},
        {"token": "a\x00b"},
        "state=CA&token=a%0aInjected",
        {"utm_source": "a\x85b"},
    ],
)
def test_raw_or_encoded_control_characters_are_rejected(query):
    with pytest.raises(ValueError, match="[Cc]ontrol"):
        build_affiliate_url(Provider.HARBOR, query)


@pytest.mark.parametrize(
    "url",
    [
        "https://harborcompliance.com/registered-agent?ref=a%0dInjected",
        "https://harborcompliance.com/registered-agent?ref=a\nInjected",
    ],
)
def test_destination_controls_are_rejected(url):
    with pytest.raises(ValueError, match="[Cc]ontrol"):
        AffiliateDestination(Provider.HARBOR, url)


@pytest.mark.parametrize(
    "query",
    [
        "utm_source=" + "x" * 4097,
        {"utm_source": "x" * 513},
        {"utm_source": ["x"] * 65},
        "&".join(f"unknown{i}=x" for i in range(65)),
        {"utm_source": "😀" * 400},
    ],
)
def test_excessive_inputs_are_rejected(query):
    with pytest.raises(ValueError):
        build_affiliate_url(Provider.HARBOR, query)


@pytest.mark.parametrize(
    "query",
    [
        "utm_source=%GG",
        "utm_source=%FF",
        "state",
        {1: "x"},
        {"state": 42},
        {"state": [42]},
        b"state=CA",
    ],
)
def test_malformed_query_types_or_encodings_are_rejected(query):
    with pytest.raises(ValueError):
        build_affiliate_url(Provider.HARBOR, query)


def test_percent_encoded_unicode_campaign_labels_remain_valid():
    url = build_affiliate_url(Provider.NORTHWEST, "utm_content=%C3%89tude")
    assert dict(query_fields(url))["utm_content"] == "Étude"


def test_shareasale_tracking_is_preserved_and_inbound_owner_overrides_are_dropped():
    url = build_affiliate_url(
        Provider.HARBOR,
        "b=attacker&u=attacker&m=attacker&state=Wyoming&entity=LP&utm_source=state-guide",
    )
    assert urlsplit(url).hostname == "www.shareasale.com"
    assert urlsplit(url).path == "/r.cfm"
    assert query_fields(url) == [
        ("b", "99010"),
        ("u", "EXAMPLE_USER_ID"),
        ("m", "99010"),
        ("state", "WY"),
        ("entity", "LP"),
        ("utm_source", "state-guide"),
    ]


@pytest.mark.parametrize("host", ["shareasale.com", "www.shareasale.com"])
def test_shareasale_exact_harbor_path_is_accepted(host):
    destination = AffiliateDestination(Provider.HARBOR, f"https://{host}/r.cfm?b=1&u=2&m=3")
    assert destination.provider == Provider.HARBOR


@pytest.mark.parametrize(
    "provider,path",
    [
        (Provider.NORTHWEST, "/r.cfm"),
        (Provider.HARBOR, "/"),
        (Provider.HARBOR, "/other"),
        (Provider.HARBOR, "/r.cfm/"),
        (Provider.HARBOR, "/r%2ecfm"),
        (Provider.HARBOR, "/r.cfm/../other"),
    ],
)
def test_shareasale_is_only_allowed_for_harbor_on_exact_tracking_path(provider, path):
    with pytest.raises(ValueError):
        AffiliateDestination(provider, "https://www.shareasale.com" + path)


def test_environment_is_read_dynamically_between_calls(monkeypatch):
    monkeypatch.setenv("PUBLIC_SITE_URL", "https://first.example/")
    monkeypatch.setenv("NORTHWEST_AFFILIATE_URL", "https://northwestregisteredagent.com/?ref=first")
    assert get_public_site_url() == "https://first.example"
    assert build_affiliate_url(Provider.NORTHWEST, {}) == (
        "https://northwestregisteredagent.com/?ref=first"
    )
    monkeypatch.setenv("PUBLIC_SITE_URL", "https://second.example")
    monkeypatch.setenv(
        "NORTHWEST_AFFILIATE_URL", "https://northwestregisteredagent.com/?ref=second"
    )
    assert get_public_site_url() == "https://second.example"
    assert build_affiliate_url(Provider.NORTHWEST, {}) == (
        "https://northwestregisteredagent.com/?ref=second"
    )


def test_current_directory_dotenv_is_optional_and_only_known_keys_are_loaded(tmp_path):
    env_file = tmp_path / ".env"
    marker = tmp_path / "executed"
    env_file.write_text(
        "# literal settings\n"
        "PUBLIC_SITE_URL='https://local.example/' # public URL\n"
        'export NORTHWEST_AFFILIATE_URL="https://northwestregisteredagent.com/?ref=$USER"\n'
        f"UNRELATED=$(touch {marker})\n"
        "IGNORED_SHELL=anything; exit 99\n"
    )
    config = load_geo_config()
    assert config.public_site_url == "https://local.example"
    assert config.northwest_affiliate_url == "https://northwestregisteredagent.com/?ref=$USER"
    assert config.harbor_affiliate_url.endswith("b=99010&u=EXAMPLE_USER_ID&m=99010")
    assert not marker.exists()
    assert not hasattr(config, "UNRELATED")


def test_os_environment_overrides_explicit_dotenv_path(monkeypatch, tmp_path):
    env_file = tmp_path / "geo.settings"
    env_file.write_text(
        "PUBLIC_SITE_URL=https://file.example\n"
        "NORTHWEST_AFFILIATE_URL=https://northwestregisteredagent.com/?ref=file\n"
        "HARBOR_AFFILIATE_URL=https://www.shareasale.com/r.cfm?b=1&u=file&m=3\n"
    )
    monkeypatch.setenv("PUBLIC_SITE_URL", "https://environment.example")
    monkeypatch.setenv("NORTHWEST_AFFILIATE_URL", "https://northwestregisteredagent.com/?ref=env")
    monkeypatch.setenv("HARBOR_AFFILIATE_URL", "https://www.shareasale.com/r.cfm?b=4&u=env&m=6")
    config = load_geo_config(str(env_file))
    assert config.public_site_url == "https://environment.example"
    assert config.northwest_affiliate_url.endswith("ref=env")
    assert config.harbor_affiliate_url.endswith("b=4&u=env&m=6")
    assert get_public_site_url(env_file) == "https://environment.example"
    assert build_affiliate_url(Provider.HARBOR, "state=CA", env_file=env_file).endswith(
        "b=4&u=env&m=6&state=CA"
    )


def test_explicit_destination_remains_independent_of_environment(monkeypatch):
    monkeypatch.setenv("HARBOR_AFFILIATE_URL", "https://invalid.example/")
    destination = AffiliateDestination(Provider.HARBOR, "https://harborcompliance.com/?ref=owner")
    assert build_affiliate_url(Provider.HARBOR, {}, destination=destination) == destination.url


def test_loaded_configuration_is_immutable_and_creates_provider_destination():
    config = load_geo_config()
    assert config.destination_for(Provider.HARBOR).url == config.harbor_affiliate_url
    with pytest.raises(FrozenInstanceError):
        config.public_site_url = "https://evil.example"


@pytest.mark.parametrize(
    "value",
    [
        "http://site.example",
        "https://user:password@site.example",
        "https://site.example/path",
        "https://site.example?token=secret",
        "https://site.example#fragment",
        "https://site.example?",
        "https://site.example#",
        "https://site.example\\path",
        " https://site.example",
        "",
        "https://site.example:99999",
        "https://site.example%2fother",
    ],
)
def test_invalid_public_site_origins_are_rejected(monkeypatch, value):
    monkeypatch.setenv("PUBLIC_SITE_URL", value)
    with pytest.raises(ValueError):
        get_public_site_url()


@pytest.mark.parametrize(
    "content",
    [
        "PUBLIC_SITE_URL='https://site.example\n",
        "PUBLIC_SITE_URL='https://site.example' junk\n",
        "PUBLIC_SITE_URL=https://one.example\nPUBLIC_SITE_URL=https://two.example\n",
    ],
)
def test_malformed_known_dotenv_assignments_are_rejected(tmp_path, content):
    env_file = tmp_path / ".env"
    env_file.write_text(content)
    with pytest.raises(ValueError):
        load_geo_config()


def test_explicit_missing_dotenv_path_has_a_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_geo_config(tmp_path / "missing.env")


def test_explicit_public_site_url_validation():
    assert validate_public_site_url("https://configured.example/") == "https://configured.example"
    with pytest.raises(ValueError):
        validate_public_site_url("https://configured.example/path?token=private")
