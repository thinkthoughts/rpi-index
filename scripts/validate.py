#!/usr/bin/env python3
"""Validate the lightweight cross-project RPI registry (stdlib only)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"theorem", "reference", "implication", "equivalence"}
SOURCE_STATES = {
    "published_kernel_checked", "third_party_kernel_check_reported",
    "reference_definition", "interpretation_requires_audit", "unverified",
    "project_verified_vps",
}
LOCAL_STATES = {"not_reproduced_here", "reproduced", "not_applicable"}


def validate(path: Path) -> tuple[int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data.get("group"), str) and data["group"]
    points = data["points"]
    ids = [point["id"] for point in points]
    assert len(ids) == len(set(ids)), f"duplicate IDs in {path}"
    for point in points:
        assert point["id"].startswith("RPI-"), point
        assert point["kind"] in KINDS, point
        assert point["source_status"] in SOURCE_STATES, point
        assert point["local_status"] in LOCAL_STATES, point
        assert point["title"] and point["statement"] and point["source"], point
        assert point["source"].startswith("https://"), point
    for edge in data["edges"]:
        assert edge["from"] in ids and edge["to"] in ids, edge
        assert edge["via"] in ids, edge
        assert next(p for p in points if p["id"] == edge["via"])["kind"] in {"theorem", "implication", "equivalence"}
        assert edge["relation"] in {"implies", "refutes", "equivalent"}, edge
    return len(points), len(data["edges"])


if __name__ == "__main__":
    paths = sorted((ROOT / "data").glob("*.json"))
    assert paths, "no registry files"
    total_points = total_edges = 0
    for path in paths:
        count, edges = validate(path)
        print(f"OK {path.relative_to(ROOT)}: {count} points, {edges} edges")
        total_points += count
        total_edges += edges
    print(f"Validated {total_points} RPIs and {total_edges} edges")
