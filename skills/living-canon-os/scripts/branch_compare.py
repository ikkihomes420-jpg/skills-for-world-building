#!/usr/bin/env python3
"""Compare a branch bundle with a source/mainline bundle.

Usage: branch_compare.py <source-bundle> <branch-bundle> [--output <report.md>] [--json]
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from canon_lib import load_records, utc_now


def canonical(record: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(record)
    for key in ("updated_at", "last_transaction"):
        value.pop(key, None)
    return value


def record_map(bundle: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for _, _, record in load_records(bundle):
        record_id = record.get("id")
        if isinstance(record_id, str) and record.get("kind") not in {"manifest", "source", "transaction"}:
            result[record_id] = canonical(record)
    return result


def label(record: dict[str, Any]) -> str:
    return str(record.get("label") or record.get("name") or record.get("id") or "<unnamed>")


def changed_fields(source: dict[str, Any], branch: dict[str, Any]) -> list[str]:
    keys = sorted(set(source) | set(branch))
    return [key for key in keys if source.get(key) != branch.get(key)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a Living Canon branch to a source bundle.")
    parser.add_argument("source_bundle", type=Path)
    parser.add_argument("branch_bundle", type=Path)
    parser.add_argument("--output", type=Path, help="Default: <branch>/audit/branch-comparison.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    source_path = args.source_bundle.expanduser().resolve()
    branch_path = args.branch_bundle.expanduser().resolve()
    if not source_path.is_dir() or not branch_path.is_dir():
        print("ERROR: Both source and branch paths must be directories.", file=sys.stderr)
        return 2

    source_records = record_map(source_path)
    branch_records = record_map(branch_path)
    added = sorted(set(branch_records) - set(source_records))
    removed = sorted(set(source_records) - set(branch_records))
    changed = []
    unchanged = 0
    for record_id in sorted(set(source_records) & set(branch_records)):
        fields = changed_fields(source_records[record_id], branch_records[record_id])
        if fields:
            changed.append({"id": record_id, "label": label(branch_records[record_id]), "fields": fields})
        else:
            unchanged += 1
    report = {
        "kind": "branch-comparison",
        "compared_at": utc_now(),
        "source_bundle": str(source_path),
        "branch_bundle": str(branch_path),
        "added": [{"id": record_id, "label": label(branch_records[record_id]), "kind": branch_records[record_id].get("kind")} for record_id in added],
        "removed": [{"id": record_id, "label": label(source_records[record_id]), "kind": source_records[record_id].get("kind")} for record_id in removed],
        "changed": changed,
        "unchanged_count": unchanged,
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    lines = ["# Branch Comparison", "", f"**Compared:** `{report['compared_at']}`  ", f"**Source:** `{source_path}`  ", f"**Branch:** `{branch_path}`  ", f"**Unchanged records:** `{unchanged}`", ""]
    for heading, key in (("Added in branch", "added"), ("Removed from branch", "removed")):
        lines.extend([f"## {heading}", ""])
        items = report[key]
        if not items:
            lines.append("None.\n")
        else:
            lines.extend(["| Record | Kind |", "|---|---|"])
            lines.extend(f"| `{item['id']}` — {item['label']} | {item['kind']} |" for item in items)
            lines.append("")
    lines.extend(["## Changed records", ""])
    if not changed:
        lines.append("None.\n")
    else:
        lines.extend(["| Record | Changed fields |", "|---|---|"])
        lines.extend(f"| `{item['id']}` — {item['label']} | {', '.join(f'`{field}`' for field in item['fields'])} |" for item in changed)
        lines.extend(["", "## Merge guidance", "", "Treat this report as an impact inventory, not an automatic merge. Select only intentional branch changes, draft an explicit transaction or change set for each mainline adoption, then validate and rebuild derived views."])
    output = args.output.expanduser().resolve() if args.output else branch_path / "audit" / "branch-comparison.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote branch comparison: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
