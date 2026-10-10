"""Check deployed flat assets without following redirects or exposing network credentials."""

import codecs
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .redirect import validate_public_site_url

_MEDIA_TYPES = {
    ".html": frozenset({"text/html"}),
    ".txt": frozenset({"text/plain"}),
    ".md": frozenset({"text/plain", "text/markdown", "text/x-markdown"}),
}


class _NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def verify_live_assets(root: Path, base_url: str) -> tuple[str, ...]:
    """GET each validated local asset, stopping at the first deployment mismatch.

    The caller validates the local artifact set before using this network check.
    Flat HTML files use extensionless public routes. Markdown and discovery files
    retain their filenames. Proxy settings and TLS verification use urllib defaults.
    """
    try:
        origin = validate_public_site_url(base_url)
    except (TypeError, ValueError):
        return ("Invalid public HTTPS origin for asset verification",)
    try:
        files = sorted((path for path in root.iterdir() if path.is_file()), key=lambda p: p.name)
    except OSError:
        return ("Local asset directory is unavailable",)
    if not files:
        return ("No regular local assets to verify",)
    opener = build_opener(_NoRedirectHandler())
    for path in files:
        name = path.name
        if path.is_symlink():
            return (f"{name}: local asset must not be a symlink",)
        allowed_types = _MEDIA_TYPES.get(path.suffix)
        if allowed_types is None:
            return (f"{name}: unsupported local asset type",)
        try:
            expected = path.read_bytes()
        except OSError:
            return (f"{name}: could not read the local asset",)
        route = path.stem if path.suffix == ".html" else name
        request = Request(
            origin + "/" + quote(route, safe="-_."),
            headers={"Accept-Encoding": "identity"},
            method="GET",
        )
        try:
            with opener.open(request, timeout=10) as response:
                if response.getcode() != 200:
                    return (f"{name}: HTTP {response.getcode()} (expected 200)",)
                content_type = response.headers.get("Content-Type", "")
                if content_type.split(";", 1)[0].strip().lower() not in allowed_types:
                    return (f"{name}: response has an unexpected or missing Content-Type",)
                charset = response.headers.get_content_charset()
                if charset is not None:
                    try:
                        is_utf8 = codecs.lookup(charset).name == "utf-8"
                    except LookupError:
                        is_utf8 = False
                    if not is_utf8:
                        return (f"{name}: declared response charset must be UTF-8",)
                # Limit the download to one byte more than the expected artifact.
                if response.read(len(expected) + 1) != expected:
                    return (f"{name}: deployed content differs from the local artifact",)
        except HTTPError as exc:
            exc.close()
            return (f"{name}: HTTP {exc.code} (expected 200; redirects are not allowed)",)
        except (URLError, OSError, HTTPException):
            return (f"{name}: network request failed",)
    return ()
