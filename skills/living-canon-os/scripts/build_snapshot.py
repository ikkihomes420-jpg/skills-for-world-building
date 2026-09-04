#!/usr/bin/env python3
"""Build a compact reader-oriented active snapshot for a Living Canon bundle.

Usage: build_snapshot.py <bundle-path> [--output <path>]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to read YAML bundles.") from exc


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


def label(record: dict[str, Any]) -> str:
    return str(record.get("label") or record.get("name") or record.get("id") or "<unnamed>")


def state_text(record: dict[str, Any]) -> str:
    parts = []
    for key in ("summary", "objective_now", "current_pressure", "statement", "proposition"):
        value = record.get(key)
        if value:
            parts.append(str(value))
    if parts:
        return " — ".join(parts[:2])
    outcomes = record.get("outcomes")
    if isinstance(outcomes, list) and outcomes:
        return "; ".join(str(item) for item in outcomes[:2])
    return "No current-state summary recorded."


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    output = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        output.append("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in row) + " |")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a compact active-snapshot.md from bundle records.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("--output", type=Path, help="Default: <bundle>/state/active-snapshot.md")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2
    records = iter_records(bundle)
    manifests = [record for _, record in records if record.get("kind") == "manifest"]
    if len(manifests) != 1:
        print("ERROR: Snapshot creation requires exactly one manifest record.", file=sys.stderr)
        return 1

    manifest = manifests[0]
    record_by_id = {str(record.get("id")): record for _, record in records if record.get("id")}
    entities = {record_id: label(record) for record_id, record in record_by_id.items() if record.get("kind") == "entity"}
    current_transitions = [record for _, record in records if record.get("kind") == "state-transition" and record.get("status") not in {"deprecated", "superseded", "archived"}]
    current_transition = sorted(current_transitions, key=lambda item: str(item.get("date_or_sequence") or ""))[-1] if current_transitions else None

    active_actor_states = [
        record for _, record in records
        if record.get("kind") == "actor-state" and record.get("status") in {"approved", "provisional", "disputed"}
        and any(record.get(key) for key in ("objective_now", "current_pressure", "private_agenda"))
    ]
    live_consequences = [
        record for _, record in records
        if record.get("kind") == "consequence" and record.get("status") in {"approved", "provisional", "disputed"}
        and record.get("current_state") != "resolved"
    ]
    open_items = [
        record for _, record in records
        if record.get("kind") in {"open-question", "decision"}
        and record.get("status") in {"provisional", "disputed"}
    ]
    unsettled = [
        record for _, record in records
        if record.get("kind") not in {"manifest", "source"}
        and record.get("status") in {"provisional", "disputed"}
    ]
    recent = sorted(
        [record for _, record in records if record.get("kind") not in {"manifest", "source"}],
        key=lambda item: str(item.get("updated_at") or item.get("last_updated") or item.get("date_or_sequence") or ""),
        reverse=True,
    )[:6]

    now = date.today().isoformat()
    project_name = label(manifest)
    version = str(manifest.get("version", "unknown"))
    branch = str((manifest.get("canon_policy") or {}).get("default_branch", "mainline"))
    sequence = str(current_transition.get("date_or_sequence")) if current_transition and current_transition.get("date_or_sequence") else "Not recorded"

    lines = [
        f"# Active Snapshot: {project_name}",
        "",
        f"**Version:** `{version}`  ",
        f"**Branch:** `{branch}`  ",
        f"**Current date/state:** `{sequence}`  ",
        f"**Last rebuilt:** `{now}`",
        "",
        "## World or project contract",
        "",
        str(manifest.get("design_promise") or "No design promise recorded."),
        "",
        "## Established current state",
        "",
    ]
    if current_transition:
        lines.append(f"**Latest transition:** `{current_transition.get('id')}` — {state_text(current_transition)}")
    else:
        lines.append("No recorded state transition is available. Treat the current state as incomplete until a session state or transition is committed.")
    lines.extend(["", "## Active entities and systems", ""])

    actor_rows = []
    for record in active_actor_states[:12]:
        entity_id = str(record.get("entity_id", "<unlinked>"))
        actor_rows.append([
            f"`{entity_id}` — {entities.get(entity_id, entity_id)}",
            str(record.get("objective_now") or record.get("public_position") or "No stated role"),
            str(record.get("current_pressure") or record.get("private_agenda") or "No active pressure recorded"),
        ])
    lines.extend(md_table(["Record", "Current role/state", "Immediate pressure"], actor_rows) or ["No active actor state records are currently flagged."])

    lines.extend(["", "## Live threads and consequences", ""])
    consequence_rows = []
    for record in live_consequences[:12]:
        consequence_rows.append([
            f"`{record.get('id')}`",
            str(record.get("current_state") or "unknown"),
            str(record.get("next_surface") or "No next surface recorded"),
        ])
    lines.extend(md_table(["Record", "State", "Next surface or decision point"], consequence_rows) or ["No unresolved consequence records are currently flagged."])

    lines.extend(["", "## Recent records", ""])
    recent_rows = []
    for record in recent:
        recent_rows.append([
            f"`{record.get('id')}`",
            str(record.get("kind", "unknown")),
            str(record.get("status", "unknown")),
            label(record),
        ])
    lines.extend(md_table(["Record", "Kind", "Status", "Summary"], recent_rows) or ["No substantive records are available."])

    lines.extend(["", "## Provisional and contested material", ""])
    if unsettled:
        for record in unsettled[:12]:
            lines.append(f"- **{record.get('status')}:** `{record.get('id')}` — {label(record)}")
    else:
        lines.append("No provisional or disputed records are currently flagged.")

    lines.extend(["", "## Open author decisions", ""])
    if open_items:
        for record in open_items[:12]:
            question = record.get("question") or label(record)
            lines.append(f"1. {question} (`{record.get('id')}`)")
    else:
        lines.append("No explicit open decisions are currently recorded.")

    lines.extend(["", "## Drift watch", ""])
    drift = manifest.get("drift_watch") or []
    if isinstance(drift, list) and drift:
        lines.extend(f"- {item}" for item in drift)
    else:
        lines.append("- Check future additions against the design promise, current rules, actor information horizons, and active consequences.")

    output = args.output.expanduser().resolve() if args.output else bundle / "state" / "active-snapshot.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote snapshot: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
