"""Build fixed-provider links from bounded, allowlisted campaign query fields.

No browser redirect or network request is performed. Provider query support is not
implied. Default links contain user-supplied example tracking IDs, which do not
establish an affiliate association. Configuration is read when helpers are called.
"""

import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from ..models import EntityType, normalize_state


class Provider(StrEnum):
    NORTHWEST = "northwest"
    HARBOR = "harbor"


_PROVIDER_HOSTS = {
    Provider.NORTHWEST: frozenset(
        {"northwestregisteredagent.com", "www.northwestregisteredagent.com"}
    ),
    Provider.HARBOR: frozenset(
        {
            "harborcompliance.com",
            "www.harborcompliance.com",
            "shareasale.com",
            "www.shareasale.com",
        }
    ),
}
_DEFAULT_CONFIG = {
    "PUBLIC_SITE_URL": "https://compliance-hub.example.com",
    "NORTHWEST_AFFILIATE_URL": (
        "https://www.northwestregisteredagent.com/?ref=EXAMPLE_AFFILIATE_ID"
    ),
    "HARBOR_AFFILIATE_URL": ("https://www.shareasale.com/r.cfm?b=99010&u=EXAMPLE_USER_ID&m=99010"),
}
_PROVIDER_CONFIG_KEYS = {
    Provider.NORTHWEST: "NORTHWEST_AFFILIATE_URL",
    Provider.HARBOR: "HARBOR_AFFILIATE_URL",
}
_SHAREASALE_HOSTS = frozenset({"shareasale.com", "www.shareasale.com"})
_FORWARDED_KEYS = frozenset(
    {
        "state",
        "entity",
        "source",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_content",
        "utm_term",
    }
)
_MAX_QUERY_LENGTH = 4096
_MAX_URL_LENGTH = 8192
_MAX_PAIRS = 64
_MAX_KEY_LENGTH = 64
_MAX_VALUE_LENGTH = 512
_ENCODED_CONTROL = re.compile(r"%(?:0[0-9a-f]|1[0-9a-f]|7f)", re.IGNORECASE)
_BAD_PERCENT_ESCAPE = re.compile(r"%(?![0-9a-f]{2})", re.IGNORECASE)
_MAX_ENV_FILE_LENGTH = 65536


def _configuration_values(env_file: Path | str | None) -> dict[str, str]:
    """Read only known literal values, without shell syntax or variable expansion."""
    values = dict(_DEFAULT_CONFIG)
    path = Path(env_file) if env_file is not None else Path.cwd() / ".env"
    if path.exists():
        if path.stat().st_size > _MAX_ENV_FILE_LENGTH:
            raise ValueError("Configuration file exceeds the supported size limit")
        seen: set[str] = set()
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].lstrip()
            key, separator, value = line.partition("=")
            key = key.strip()
            if key not in _DEFAULT_CONFIG:
                continue
            if not separator or key in seen:
                raise ValueError(f"Invalid or duplicate configuration assignment: {key}")
            seen.add(key)
            value = value.strip()
            if value.startswith(("'", '"')):
                quote = value[0]
                end = value.find(quote, 1)
                if (
                    end == -1
                    or value[end + 1 :].strip() not in ("",)
                    and not (value[end + 1 :].lstrip().startswith("#"))
                ):
                    raise ValueError(f"Invalid quoted configuration assignment: {key}")
                value = value[1:end]
            else:
                value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
            values[key] = value
    elif env_file is not None:
        raise FileNotFoundError("Specified configuration file does not exist")
    for key in _DEFAULT_CONFIG:
        if key in os.environ:
            values[key] = os.environ[key]
    return values


def _reject_controls(value: str) -> None:
    """Reject raw or percent-encoded controls, including nested percent encoding."""
    while True:
        if any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value):
            raise ValueError("Control characters are not allowed in URLs or query fields")
        if _ENCODED_CONTROL.search(value):
            raise ValueError("Percent-encoded control characters are not allowed")
        decoded = unquote(value)
        if decoded == value:
            return
        value = decoded


def _parse_query(query: str) -> list[tuple[str, str]]:
    if len(query) > _MAX_QUERY_LENGTH:
        raise ValueError(f"Query exceeds {_MAX_QUERY_LENGTH} characters")
    _reject_controls(query)
    if _BAD_PERCENT_ESCAPE.search(query):
        raise ValueError("Query contains an invalid percent escape")
    return parse_qsl(
        query,
        keep_blank_values=True,
        strict_parsing=True,
        encoding="utf-8",
        errors="strict",
        max_num_fields=_MAX_PAIRS,
    )


def _incoming_pairs(query: str | Mapping[str, str | Sequence[str]]) -> list[tuple[str, str]]:
    if isinstance(query, str):
        pairs = _parse_query(query.removeprefix("?"))
    elif isinstance(query, Mapping):
        if len(query) > _MAX_PAIRS:
            raise ValueError(f"Query exceeds {_MAX_PAIRS} fields")
        pairs = []
        for key, values in query.items():
            if not isinstance(key, str):
                raise ValueError("Query keys must be strings")
            if isinstance(values, str):
                values = (values,)
            elif not isinstance(values, Sequence) or isinstance(values, bytes | bytearray):
                raise ValueError("Query values must be strings or sequences of strings")
            if len(values) + len(pairs) > _MAX_PAIRS:
                raise ValueError(f"Query exceeds {_MAX_PAIRS} fields")
            for value in values:
                if not isinstance(value, str):
                    raise ValueError("Query values must be strings")
                pairs.append((key, value))
    else:
        raise ValueError("Query must be a raw query string or a mapping")
    for key, value in pairs:
        if len(key) > _MAX_KEY_LENGTH or len(value) > _MAX_VALUE_LENGTH:
            raise ValueError("Query field exceeds the supported size limit")
        _reject_controls(key)
        _reject_controls(value)
    if len(urlencode(pairs)) > _MAX_QUERY_LENGTH:
        raise ValueError(f"Encoded query exceeds {_MAX_QUERY_LENGTH} characters")
    return pairs


@dataclass(frozen=True, slots=True)
class AffiliateDestination:
    """Owner configuration on an approved provider host, separate from incoming data."""

    provider: Provider
    url: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider", Provider(self.provider))
        if not isinstance(self.url, str) or not self.url or len(self.url) > _MAX_URL_LENGTH:
            raise ValueError("Destination must be a nonempty URL within the supported size limit")
        _reject_controls(self.url)
        if "\\" in self.url:
            raise ValueError("Backslashes are not allowed in destination URLs")
        parsed = urlsplit(self.url)
        if parsed.scheme != "https" or parsed.hostname not in _PROVIDER_HOSTS[self.provider]:
            raise ValueError("Destination must use HTTPS on an approved provider host")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("Destination URLs cannot contain user credentials")
        if parsed.fragment or "#" in self.url:
            raise ValueError("Destination URLs cannot contain fragments")
        if parsed.port not in (None, 443):
            raise ValueError("Destination URLs must use the default HTTPS port")
        if parsed.hostname in _SHAREASALE_HOSTS and parsed.path != "/r.cfm":
            raise ValueError("Harbor ShareASale destination must use the exact /r.cfm path")
        _parse_query(parsed.query)
        # A bare approved origin uses the same safe service path as defaults.
        if not parsed.path:
            object.__setattr__(self, "url", urlunsplit(parsed._replace(path="/registered-agent")))


def _public_origin(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > _MAX_URL_LENGTH:
        raise ValueError("PUBLIC_SITE_URL must be a nonempty HTTPS origin")
    _reject_controls(value)
    if any(char.isspace() for char in value) or "\\" in value:
        raise ValueError("PUBLIC_SITE_URL cannot contain whitespace or backslashes")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or "%" in parsed.hostname:
        raise ValueError("PUBLIC_SITE_URL must be an absolute HTTPS origin")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("PUBLIC_SITE_URL cannot contain user credentials")
    if (
        parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or "?" in value
        or "#" in value
    ):
        raise ValueError("PUBLIC_SITE_URL must be an origin without a path, query or fragment")
    # Accessing port rejects malformed/out-of-range authority even when it is unused.
    _ = parsed.port
    return urlunsplit(parsed._replace(path=""))


@dataclass(frozen=True, slots=True)
class GeoConfig:
    public_site_url: str
    northwest_affiliate_url: str
    harbor_affiliate_url: str

    def destination_for(self, provider: Provider) -> AffiliateDestination:
        selected = Provider(provider)
        url = (
            self.northwest_affiliate_url
            if selected == Provider.NORTHWEST
            else self.harbor_affiliate_url
        )
        return AffiliateDestination(selected, url)


def load_geo_config(env_file: Path | str | None = None) -> GeoConfig:
    """Load and validate defaults, optional literal .env, then current OS environment.

    Only PUBLIC_SITE_URL, NORTHWEST_AFFILIATE_URL and HARBOR_AFFILIATE_URL are read.
    The default file is .env in the current directory, if it exists. Values are never
    interpolated, evaluated or executed. OS environment values take precedence.
    """
    values = _configuration_values(env_file)
    public_site = _public_origin(values["PUBLIC_SITE_URL"])
    northwest = AffiliateDestination(Provider.NORTHWEST, values["NORTHWEST_AFFILIATE_URL"])
    harbor = AffiliateDestination(Provider.HARBOR, values["HARBOR_AFFILIATE_URL"])
    return GeoConfig(public_site, northwest.url, harbor.url)


def get_public_site_url(env_file: Path | str | None = None) -> str:
    """Read the current PUBLIC_SITE_URL and validate it as an HTTPS origin."""
    return _public_origin(_configuration_values(env_file)["PUBLIC_SITE_URL"])


def validate_public_site_url(value: str) -> str:
    """Validate an explicit public HTTPS origin and remove its optional trailing slash."""
    return _public_origin(value)


def build_affiliate_url(
    provider: Provider,
    query: str | Mapping[str, str | Sequence[str]],
    *,
    destination: AffiliateDestination | None = None,
    env_file: Path | str | None = None,
) -> str:
    """Append state/entity/campaign labels to an owner-selected provider destination.

    All other incoming keys, including redirect URLs, account IDs, emails, tokens
    and affiliate IDs, are discarded. Do not put personal data in campaign labels.
    Owner query parameters remain unchanged and incoming data cannot replace them.
    State and entity are singular; repeated values are ambiguous and rejected.
    ``state`` accepts 50 US states. Known LLC, C-Corp and LP entity values are
    preserved; other entity strings fall back to LLC without forwarding the name.
    ``source`` and ``utm_source`` are independent attribution fields. Both pass
    through when supplied, unless the owner destination already defines that key.
    """
    selected_provider = Provider(provider)
    if destination is None:
        values = _configuration_values(env_file)
        destination = AffiliateDestination(
            selected_provider, values[_PROVIDER_CONFIG_KEYS[selected_provider]]
        )
    elif not isinstance(destination, AffiliateDestination):
        raise ValueError("destination must be an AffiliateDestination")
    elif destination.provider != selected_provider:
        raise ValueError("Destination provider does not match the selected provider")
    parsed = urlsplit(destination.url)
    owner_keys = {key.casefold() for key, _ in _parse_query(parsed.query)}
    additions: list[tuple[str, str]] = []
    seen_singular: set[str] = set()
    for key, value in _incoming_pairs(query):
        if key not in _FORWARDED_KEYS:
            continue
        if key in {"state", "entity"}:
            if key in seen_singular:
                raise ValueError(f"Ambiguous duplicate query field: {key}")
            seen_singular.add(key)
        if key == "state":
            value = normalize_state(value)
            if value == "DC":
                raise ValueError("state must identify one of the 50 US states")
        elif key == "entity":
            try:
                value = EntityType(value).value
            except ValueError:
                value = EntityType.LLC.value
        if key.casefold() not in owner_keys:
            additions.append((key, value))
    if not additions:
        return destination.url
    encoded = urlencode(additions)
    combined = parsed.query + "&" + encoded if parsed.query else encoded
    result = urlunsplit(parsed._replace(query=combined))
    if len(result) > _MAX_URL_LENGTH:
        raise ValueError(f"Destination URL exceeds {_MAX_URL_LENGTH} characters")
    return result
