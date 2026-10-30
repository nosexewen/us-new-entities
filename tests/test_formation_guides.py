"""Domestic-formation draft contract: exactly fifty states, two entity kinds, no legal claims."""
from pathlib import Path

from us_new_entities.formation_guides import build, REQUIRED_REVIEW_FIELDS


def test_formation_drafts_are_unpublished(tmp_path: Path):
    assert build(tmp_path) == 100
    paths = list(tmp_path.glob("*/record.json"))
    assert len(paths) == 100
    import json
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["jurisdiction"] == "domestic formation"
        assert data["publication_eligible"] is False
        assert set(data["review_fields"]) == set(REQUIRED_REVIEW_FIELDS)
        assert all(value is None for value in data["review_fields"].values())
        page = (path.parent / "index.html").read_text(encoding="utf-8")
        assert 'noindex, nofollow' in page
        assert "foreign qualification filing fee" not in page.lower()
