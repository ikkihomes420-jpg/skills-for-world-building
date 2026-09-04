#!/usr/bin/env python3
"""Report direct record dependencies before changing a Living Canon ID.

Usage: impact_report.py <bundle-path> <record-id> [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to inspect YAML bundles.") from exc


def load_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle) if path.suffix.lower() == ".json" else yaml.safe_load(handle)


def iter_records(bundle: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(bundle.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in path.parts):
            continue
        try:
            loaded = load_file(path)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(loaded, dict):
            records.append((path, loaded))
        elif isinstance(loaded, list):
            records.extend((path, item) for item in loaded if isinstance(item, dict))
    return records


def paths_with_value(data: Any, target: str, prefix: str = "") -> list[str]:
    matches: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            location = f"{prefix}.{key}" if prefix else key
            if value == target:
                matches.append(location)
            else:
                matches.extend(paths_with_value(value, target, location))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            location = f"{prefix}[{index}]"
            if value == target:
                matches.append(location)
            else:
                matches.extend(paths_with_value(value, target, location))
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="List records directly affected by a Living Canon record change.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("record_id")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON rather than Markdown.")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2

    records = iter_records(bundle)
    target: tuple[Path, dict[str, Any]] | None = None
    dependents: list[dict[str, Any]] = []
    for path, record in records:
        if record.get("id") == args.record_id:
            target = (path, record)
            continue
        paths = paths_with_value(record, args.record_id)
        if paths:
            dependents.append({
                "id": record.get("id", "<missing-id>"),
                "kind": record.get("kind", "<missing-kind>"),
                "file": str(path.relative_to(bundle)),
                "reference_paths": paths,
                "status": record.get("status", "<missing-status>"),
            })

    if target is None:
        print(f"ERROR: Record '{args.record_id}' was not found in {bundle}", file=sys.stderr)
        return 1

    target_path, target_record = target
    outbound = []
    for other_path, other_record in records:
        other_id = other_record.get("id")
        if not isinstance(other_id, str) or other_id == args.record_id:
            continue
        paths = paths_with_value(target_record, other_id)
        if paths:
            outbound.append({
                "id": other_id,
                "kind": other_record.get("kind", "<missing-kind>"),
                "file": str(other_path.relative_to(bundle)),
                "reference_paths": paths,
                "status": other_record.get("status", "<missing-status>"),
            })

    report = {
        "record": {
            "id": args.record_id,
            "kind": target_record.get("kind", "<missing-kind>"),
            "label": target_record.get("label", target_record.get("name", "<unnamed>")),
            "file": str(target_path.relative_to(bundle)),
            "status": target_record.get("status", "<missing-status>"),
            "branch": target_record.get("branch", "mainline"),
        },
        "direct_dependents": dependents,
        "outbound_links": outbound,
        "migration_checklist": [
            "Preserve the original record and ID history; do not delete provenance.",
            "Classify the operation as add, modify, deprecate, redirect, split, or merge.",
            "Review every direct dependent and any stated semantic consequence before approval.",
            "Write a change-set with rationale, expected impacts, migration notes, and author decision.",
            "Revalidate the bundle and rebuild the active snapshot after approval.",
        ],
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"# Impact report: `{args.record_id}`\n")
    print(f"**Record:** `{report['record']['kind']}` — {report['record']['label']}  ")
    print(f"**File:** `{report['record']['file']}`  ")
    print(f"**Status / branch:** `{report['record']['status']}` / `{report['record']['branch']}`\n")

    print("## Direct dependents")
    if not dependents:
        print("\nNo direct internal references were found. This does not prove there are no narrative or semantic effects.\n")
    else:
        print("\n| Record | Kind | Status | Reference path(s) |")
        print("|---|---|---|---|")
        for item in dependents:
            paths = "<br>".join(f"`{path}`" for path in item["reference_paths"])
            print(f"| `{item['id']}` | {item['kind']} | {item['status']} | {paths} |")
        print()

    print("## Outbound links")
    if not outbound:
        print("\nNo other registered record IDs are directly named by this record.\n")
    else:
        print("\n| Record | Kind | Status | Reference path(s) |")
        print("|---|---|---|---|")
        for item in outbound:
            paths = "<br>".join(f"`{path}`" for path in item["reference_paths"])
            print(f"| `{item['id']}` | {item['kind']} | {item['status']} | {paths} |")
        print()

    print("## Migration checklist")
    for step in report["migration_checklist"]:
        print(f"- {step}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
