"""Separate domestic formation drafts from FOREIGN qualification requirements.

No foreign qualification form, fee, or obligation is reused. All drafts have
noindex until independently sourced and approved for publication.
Run: python -m us_new_entities.formation_guides dist/formation-drafts
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from .models.entity import STATE_NAMES

# Official domestic-formation source entrypoints reviewed 2026-10-30.
# These are not sufficient alone to verify all legal fields of a guide.
OFFICIAL_DOMESTIC_SOURCES = {
    "CA": "https://www.sos.ca.gov/business-programs/business-entities/starting-business/types",
    "DE": "https://corp.delaware.gov/howtoform/",
    "TX": "https://www.sos.state.tx.us/corp/forms_boc.shtml",
}
REQUIRED_REVIEW_FIELDS = (
    "official_domestic_form",
    "state_filing_fee",
    "registered_agent_rules",
    "name_availability",
    "filing_method",
    "initial_report",
    "recurring_report_or_tax",
    "state_specific_exceptions",
)
ENTITY_TYPES = {"llc": "LLC", "corporation": "Corporation"}


def record(state: str, name: str, kind: str) -> dict:
    return {
        "state": state,
        "state_name": name,
        "entity": kind,
        "jurisdiction": "domestic formation",
        "status": "research_required",
        "reviewed_on": None,
        "official_source_entrypoint": OFFICIAL_DOMESTIC_SOURCES.get(state),
        "review_fields": {field: None for field in REQUIRED_REVIEW_FIELDS},
        "publication_eligible": False,
    }


def render_page(data: dict) -> str:
    state = html.escape(data["state_name"])
    kind = html.escape(ENTITY_TYPES[data["entity"]])
    source = data["official_source_entrypoint"]
    source_html = (
        f'<p>Official domestic formation entrypoint: <a href="{html.escape(source, quote=True)}">'
        "State filing office</a></p>"
        if source else
        "<p>Official state formation source not yet independently reviewed.</p>"
    )
    fields = "".join(
        f"<li>{html.escape(key.replace('_', ' ').capitalize())}: "
        "<strong>Not verified</strong></li>"
        for key in REQUIRED_REVIEW_FIELDS
    )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="robots" content="noindex, nofollow">'
        f"<title>Draft: Form a {kind} in {state}</title></head><body>"
        f"<main><h1>Form a new {kind} in {state}</h1>"
        "<p><strong>UNVERIFIED RESEARCH DRAFT — NOT A FILING GUIDE.</strong></p>"
        "<p>This page concerns a NEW domestic entity, not registration of an "
        "existing out-of-state company. No amounts, deadlines or filing forms "
        "have been approved for publication.</p>"
        f"{source_html}<h2>State-specific fields awaiting source review</h2>"
        f"<ul>{fields}</ul></main></body></html>"
    )


def build(destination: Path) -> int:
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for state, name in sorted(STATE_NAMES.items()):
        for kind in ENTITY_TYPES:
            data = record(state, name, kind)
            path = destination / f"{state.lower()}-{kind}-formation"
            path.mkdir(exist_ok=True)
            (path / "record.json").write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            (path / "index.html").write_text(render_page(data), encoding="utf-8")
            manifest.append({"path": path.name, "status": data["status"]})
    (destination / "manifest.json").write_text(
        json.dumps({"guide_count": len(manifest), "guides": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    if len(manifest) != 100:
        raise RuntimeError(f"Expected 100 domestic formation drafts, got {len(manifest)}")
    return len(manifest)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(f"Generated {build(args.output)} unverified domestic formation drafts.")


if __name__ == "__main__":
    main()
