from email.message import Message
from io import BytesIO
from urllib.error import HTTPError, URLError

import pytest
from us_new_entities.geo import health

ORIGIN = "https://compliance.example.org"


class FakeResponse:
    def __init__(self, content, content_type="text/html; charset=UTF-8", status=200):
        self.content = BytesIO(content)
        self.headers = Message()
        if content_type is not None:
            self.headers["Content-Type"] = content_type
        self.status = status
        self.closed = False
        self.read_limit = None

    def getcode(self):
        return self.status

    def read(self, limit):
        self.read_limit = limit
        return self.content.read(limit)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closed = True


class FakeOpener:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []
        self.handlers = ()

    def open(self, request, *, timeout):
        self.calls.append((request, timeout))
        result = self.responses[request.full_url]
        if isinstance(result, Exception):
            raise result
        return result


@pytest.fixture
def assets(tmp_path, monkeypatch):
    root = tmp_path / "dist"
    root.mkdir()
    for state in ("ca", "de", "fl", "tx", "wy"):
        for entity in ("llc", "c-corp"):
            stem = f"{state}-{entity}-foreign-qualification"
            (root / (stem + ".html")).write_bytes(f"<!doctype html><p>{stem}</p>".encode())
            (root / (stem + ".md")).write_bytes(f"# {stem}\n".encode())
    (root / "llms.txt").write_bytes(b"# Jurisdiction guides\n")
    (root / "robots.txt").write_bytes(b"User-agent: *\nAllow: /\n")
    responses = {}
    for path in root.iterdir():
        route = path.stem if path.suffix == ".html" else path.name
        media_type = "text/html" if path.suffix == ".html" else "text/plain"
        responses[ORIGIN + "/" + route] = FakeResponse(
            path.read_bytes(),
            media_type + "; charset=UTF-8",
        )
    opener = FakeOpener(responses)

    def build_opener(*handlers):
        opener.handlers = handlers
        return opener

    monkeypatch.setattr(health, "build_opener", build_opener)
    return root, opener


def test_all_twenty_two_assets_use_sorted_get_routes_and_match_exact_bytes(assets):
    root, opener = assets
    assert health.verify_live_assets(root, ORIGIN + "/") == ()
    expected_urls = [
        ORIGIN + "/" + (path.stem if path.suffix == ".html" else path.name)
        for path in sorted(root.iterdir())
    ]
    assert len(opener.calls) == 22
    assert [request.full_url for request, _ in opener.calls] == expected_urls
    assert all(request.get_method() == "GET" for request, _ in opener.calls)
    assert all(timeout == 10 for _, timeout in opener.calls)
    assert all(request.get_header("Accept-encoding") == "identity" for request, _ in opener.calls)
    assert not any(url.endswith(".html") for url in expected_urls)
    assert sum(url.endswith(".md") for url in expected_urls) == 10
    assert all(response.closed for response in opener.responses.values())
    assert all(
        response.read_limit == len(response.content.getvalue()) + 1
        for response in opener.responses.values()
    )


def test_root_index_is_checked_at_root_without_redirect(assets):
    root, opener = assets
    source = b"<!doctype html><html><body>State directory</body></html>"
    (root / "index.html").write_bytes(source)
    opener.responses[ORIGIN + "/"] = FakeResponse(source)
    assert health.verify_live_assets(root, ORIGIN) == ()
    urls = [request.full_url for request, _ in opener.calls]
    assert ORIGIN + "/" in urls
    assert ORIGIN + "/index" not in urls


@pytest.mark.parametrize("media_type", ["text/plain", "text/markdown", "text/x-markdown"])
def test_markdown_accepts_supported_text_media_types(assets, media_type):
    root, opener = assets
    for url, response in opener.responses.items():
        if url.endswith(".md"):
            response.headers.replace_header("Content-Type", media_type + "; charset=utf8")
    assert health.verify_live_assets(root, ORIGIN) == ()


def test_charset_is_optional_but_utf8_aliases_are_accepted_when_declared(assets):
    root, opener = assets
    for index, response in enumerate(opener.responses.values()):
        media_type = response.headers.get_content_type()
        declaration = "" if index % 2 else '; charset="UTF-8"'
        response.headers.replace_header("Content-Type", media_type + declaration)
    assert health.verify_live_assets(root, ORIGIN) == ()


@pytest.mark.parametrize("status", [201, 204, 301, 302, 404, 500])
def test_any_status_other_than_200_fails_without_checking_more_assets(assets, status):
    root, opener = assets
    first_url = ORIGIN + "/" + sorted(root.iterdir())[0].stem
    opener.responses[first_url].status = status
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert f"HTTP {status}" in errors[0]
    assert len(opener.calls) == 1


@pytest.mark.parametrize("content_type", [None, "", "application/json", "text/plain", "bad-type"])
def test_html_missing_or_wrong_media_type_fails_before_downloading_content(assets, content_type):
    root, opener = assets
    first_path = sorted(root.iterdir())[0]
    response = FakeResponse(first_path.read_bytes(), content_type)
    opener.responses[ORIGIN + "/" + first_path.stem] = response
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert "Content-Type" in errors[0]
    assert response.read_limit is None
    assert response.closed
    assert len(opener.calls) == 1


@pytest.mark.parametrize("filename", ["llms.txt", "robots.txt"])
def test_discovery_assets_require_plain_text_rather_than_an_html_fallback(assets, filename):
    root, opener = assets
    opener.responses[ORIGIN + "/" + filename].headers.replace_header("Content-Type", "text/html")
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert errors[0].startswith(filename + ":")
    assert "Content-Type" in errors[0]


@pytest.mark.parametrize("charset", ["us-ascii", "latin-1", "bogus-private-token", ""])
def test_non_utf8_declared_charsets_are_rejected_without_echoing_the_declaration(assets, charset):
    root, opener = assets
    first_url = ORIGIN + "/" + sorted(root.iterdir())[0].stem
    opener.responses[first_url].headers.replace_header(
        "Content-Type", "text/html; charset=" + charset
    )
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert "UTF-8" in errors[0]
    assert "bogus-private-token" not in errors[0]
    assert len(opener.calls) == 1


@pytest.mark.parametrize("content", [b"A different deployment", b"", b"x" * 100000])
def test_wrong_content_or_a_different_deployment_fails_and_limits_the_response_read(
    assets, content
):
    root, opener = assets
    first_path = sorted(root.iterdir())[0]
    response = FakeResponse(content)
    opener.responses[ORIGIN + "/" + first_path.stem] = response
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert "differs from the local artifact" in errors[0]
    assert response.read_limit == len(first_path.read_bytes()) + 1
    assert len(opener.calls) == 1


def test_default_urllib_redirect_handling_is_disabled_and_diagnostics_do_not_leak_location(assets):
    root, opener = assets
    first_url = ORIGIN + "/" + sorted(root.iterdir())[0].stem
    headers = Message()
    headers["Location"] = "https://user:secret@other.example.org/?token=private"
    body = BytesIO(b"redirect")
    opener.responses[first_url] = HTTPError(first_url, 302, "secret token=private", headers, body)
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert "HTTP 302" in errors[0]
    assert "redirects are not allowed" in errors[0]
    assert "secret" not in errors[0] and "private" not in errors[0]
    assert len(opener.calls) == 1
    assert body.closed
    assert len(opener.handlers) == 1
    assert (
        opener.handlers[0].redirect_request(
            None, None, 302, "", headers, "https://other.example.org"
        )
        is None
    )


@pytest.mark.parametrize(
    "error",
    [
        URLError("proxy=https://user:secret@proxy.example.org?token=private"),
        TimeoutError("private-token"),
        OSError("private-token"),
    ],
)
def test_network_errors_fail_fast_without_credential_or_exception_details(assets, error):
    root, opener = assets
    first_url = ORIGIN + "/" + sorted(root.iterdir())[0].stem
    opener.responses[first_url] = error
    errors = health.verify_live_assets(root, ORIGIN)
    assert len(errors) == 1
    assert "network request failed" in errors[0]
    assert "secret" not in errors[0] and "private" not in errors[0]
    assert len(opener.calls) == 1


def test_empty_or_unavailable_local_assets_never_report_live_success(tmp_path):
    assert health.verify_live_assets(tmp_path / "missing", ORIGIN)
    assert health.verify_live_assets(tmp_path, ORIGIN)


def test_invalid_origins_are_rejected_without_network_requests_or_credential_echo(assets):
    root, opener = assets
    errors = health.verify_live_assets(
        root, "https://user:secret@compliance.example.org/?token=private"
    )
    assert errors
    assert "secret" not in errors[0] and "private" not in errors[0]
    assert not opener.calls


def test_symlinked_local_asset_is_rejected_before_a_request(assets, tmp_path):
    root, opener = assets
    first_path = sorted(root.iterdir())[0]
    target = tmp_path / "target.html"
    target.write_bytes(first_path.read_bytes())
    first_path.unlink()
    first_path.symlink_to(target)
    assert "symlink" in health.verify_live_assets(root, ORIGIN)[0]
    assert not opener.calls
