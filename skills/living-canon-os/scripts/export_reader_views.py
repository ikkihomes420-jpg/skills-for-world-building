#!/usr/bin/env python3
"""Export readable Living Canon dossiers, chronicle, and changelog.

Usage: export_reader_views.py <bundle-path> [--output <directory>]
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

from canon_lib import load_records, utc_now


def label(record: dict[str, Any]) -> str:
    return str(record.get("label") or record.get("name") or record.get("id") or "<unnamed>")


def references(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("_id") and isinstance(item, str):
                found.add(item)
            elif key.endswith("_ids") and isinstance(item, list):
                found.update(str(value) for value in item if isinstance(value, str))
            else:
                found.update(references(item))
    elif isinstance(value, list):
        for item in value:
            found.update(references(item))
    return found


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export reader-friendly views from a Living Canon bundle.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("--output", type=Path, help="Default: <bundle>/reader")
    args = parser.parse_args()
    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        raise SystemExit(f"ERROR: Bundle path is not a directory: {bundle}")
    output = args.output.expanduser().resolve() if args.output else bundle / "reader"
    records = [record for _, _, record in load_records(bundle)]
    by_id = {record["id"]: record for record in records if isinstance(record.get("id"), str)}
    manifest = next((record for record in records if record.get("kind") == "manifest"), None)
    if manifest is None:
        raise SystemExit("ERROR: Bundle requires one manifest record.")

    entities = sorted((record for record in records if record.get("kind") == "entity"), key=lambda item: label(item).lower())
    events = sorted((record for record in records if record.get("kind") == "event"), key=lambda item: str(item.get("date_or_sequence") or ""))
    transactions = sorted((record for record in records if record.get("kind") == "transaction"), key=lambda item: str(item.get("created_at") or ""), reverse=True)
    incoming: dict[str, list[str]] = defaultdict(list)
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str):
            continue
        for target in references(record):
            if target in by_id and target != record_id:
                incoming[target].append(record_id)

    dossier_dir = output / "dossiers"
    for entity in entities:
        entity_id = entity["id"]
        summary = entity.get("summary") or "No summary recorded."
        lines = [f"# {label(entity)}", "", f"**ID:** `{entity_id}`  ", f"**Type:** `{entity.get('type', 'unknown')}`  ", f"**Canon status:** `{entity.get('status', 'unknown')}`  ", f"**Authority / confidence:** `{entity.get('authority', 'unknown')}` / `{entity.get('confidence', 'unknown')}`  ", f"**Branch:** `{entity.get('branch', 'mainline')}`", "", "## Summary", "", str(summary), ""]
        aliases = entity.get("aliases", [])
        if aliases:
            lines.extend(["## Aliases", "", ", ".join(f"`{alias}`" for alias in aliases), ""])
        outgoing = sorted(ref for ref in references(entity) if ref in by_id)
        linked = sorted(set(outgoing + incoming.get(entity_id, [])))
        lines.extend(["## Linked canon", ""])
        if linked:
            lines.extend(f"- `{record_id}` — {label(by_id[record_id])}" for record_id in linked)
        else:
            lines.append("No linked canonical records are currently indexed.")
        sources = entity.get("sources", [])
        if sources:
            lines.extend(["", "## Evidence", ""])
            lines.extend(f"- `{source}`" for source in sources)
        write(dossier_dir / f"{entity_id.replace('.', '-')}.md", "\n".join(lines))

    chronicle = [f"# Chronicle: {manifest.get('name', 'Living Canon')}", "", f"**Exported:** `{utc_now()}`", "", "## Events", ""]
    if events:
        chronicle.extend(["| Date or sequence | Event | Status |", "|---|---|---|"])
        chronicle.extend(f"| {event.get('date_or_sequence') or 'Unplaced'} | `{event['id']}` — {label(event)} | {event.get('status', 'unknown')} |" for event in events)
        for event in events:
            chronicle.extend(["", f"## {event.get('date_or_sequence') or 'Unplaced'} — {label(event)}", "", str(event.get("summary") or "No summary recorded.")])
            if event.get("causes"):
                chronicle.extend(["", "**Causes:** " + "; ".join(str(item) for item in event["causes"])])
            if event.get("delayed_effects"):
                chronicle.extend(["", "**Delayed effects:** " + "; ".join(str(item) for item in event["delayed_effects"])])
    else:
        chronicle.append("No event records are available.")
    write(output / "chronicle.md", "\n".join(chronicle))

    changelog = [f"# Canon Changelog: {manifest.get('name', 'Living Canon')}", "", f"**Exported:** `{utc_now()}`", ""]
    if transactions:
        for transaction in transactions:
            changelog.extend([f"## {transaction.get('created_at', 'Undated')} — {transaction.get('title', transaction.get('id'))}", "", f"**Transaction:** `{transaction.get('id')}`  ", f"**Status:** `{transaction.get('status')}`  ", f"**Rationale:** {transaction.get('rationale') or 'Not recorded.'}", ""])
            for operation in transaction.get("operations", []):
                changelog.append(f"- `{operation.get('op')}` — `{operation.get('target_id')}`")
            changelog.append("")
    else:
        changelog.append("No transaction history is available.")
    write(output / "canon-changelog.md", "\n".join(changelog))

    index_lines = [f"# Reader Views: {manifest.get('name', 'Living Canon')}", "", f"**Exported:** `{utc_now()}`", "", "## Available views", "", "- [Chronicle](chronicle.md)", "- [Canon changelog](canon-changelog.md)", "", "## Entity dossiers", ""]
    if entities:
        index_lines.extend(f"- [{label(entity)}](dossiers/{entity['id'].replace('.', '-')}.md) — `{entity['id']}`" for entity in entities)
    else:
        index_lines.append("No entity dossiers are available.")
    write(output / "index.md", "\n".join(index_lines))

    print(f"Exported reader views for {len(entities)} entity dossier(s), {len(events)} event(s), and {len(transactions)} transaction(s): {output}")
    return 0


if __name__ == "__main__":
    main()
