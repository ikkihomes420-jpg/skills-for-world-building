#!/usr/bin/env python3
"""Build a rebuildable full-text, alias, and relationship index for a Living Canon bundle.

Usage: build_index.py <bundle-path> [--output <index-path>]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from canon_lib import ID_PATTERN, load_records, utc_now


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def strings_in(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, str):
        values.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"last_transaction", "updated_at"}:
                continue
            values.extend(strings_in(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(strings_in(item))
    return values


def references_in(value: Any, own_id: str | None = None) -> list[str]:
    found: set[str] = set()
    if isinstance(value, str) and ID_PATTERN.match(value) and value != own_id:
        found.add(value)
    elif isinstance(value, dict):
        for item in value.values():
            found.update(references_in(item, own_id))
    elif isinstance(value, list):
        for item in value:
            found.update(references_in(item, own_id))
    return sorted(found)


def label(record: dict[str, Any]) -> str:
    return str(record.get("label") or record.get("name") or record.get("id") or "<unnamed>")


def excerpt(record: dict[str, Any]) -> str:
    for key in ("summary", "statement", "proposition", "question", "objective_now", "current_pressure"):
        value = record.get(key)
        if value:
            return str(value)
    return label(record)


def rich_context(record: dict[str, Any]) -> str:
    """Keep high-detail context available without making it the default recall view."""
    preferred_fields = (
        "detail", "details", "context", "content", "notes", "annotations",
        "immediate_effects", "delayed_effects", "causes", "consequences",
        "attributes", "private_agenda", "public_position", "internal_divisions",
        "resources", "constraints", "exceptions",
    )
    sections: list[str] = []
    for key in preferred_fields:
        value = record.get(key)
        if value not in (None, "", [], {}):
            if isinstance(value, (dict, list)):
                rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
            else:
                rendered = str(value)
            sections.append(f"{key}: {rendered}")
    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a derived Living Canon search and graph index.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("--output", type=Path, help="Default: <bundle>/.canon/index.json")
    args = parser.parse_args()
    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2

    records: dict[str, dict[str, Any]] = {}
    aliases: dict[str, list[str]] = {}
    for path, _, record in load_records(bundle):
        record_id = record.get("id")
        if not isinstance(record_id, str) or record.get("kind") in {"manifest", "source", "transaction"}:
            continue
        record_label = label(record)
        has_display_label = bool(record.get("label") or record.get("name"))
        alias_values = [record_label] + [str(item) for item in record.get("aliases", []) if isinstance(item, str)]
        text = "\n".join(strings_in(record))
        references = references_in(record, record_id)
        records[record_id] = {
            "id": record_id,
            "kind": record.get("kind", "unknown"),
            "label": record_label,
            "has_display_label": has_display_label,
            "aliases": alias_values[1:],
            "excerpt": excerpt(record),
            "detail_context": rich_context(record),
            "status": record.get("status", "unknown"),
            "authority": record.get("authority", "unknown"),
            "confidence": record.get("confidence", "unknown"),
            "branch": record.get("branch", "mainline"),
            "visibility": record.get("visibility", "author-only"),
            "updated_at": record.get("updated_at"),
            "file": str(path.relative_to(bundle)),
            "text": text,
            "references": references,
            "sources": record.get("sources", record.get("support", [])),
        }
        for alias in alias_values:
            key = normalize(alias)
            if key:
                aliases.setdefault(key, []).append(record_id)

    reverse: dict[str, list[str]] = {record_id: [] for record_id in records}
    for record_id, record in records.items():
        for reference in record["references"]:
            if reference in reverse:
                reverse[reference].append(record_id)
    for values in aliases.values():
        values.sort()
    for values in reverse.values():
        values.sort()

    index = {
        "kind": "derived-canon-index",
        "built_at": utc_now(),
        "schema_version": "2.1",
        "record_count": len(records),
        "records": records,
        "alias_index": aliases,
        "reverse_links": reverse,
    }
    output = args.output.expanduser().resolve() if args.output else bundle / ".canon" / "index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built derived index for {len(records)} record(s): {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
