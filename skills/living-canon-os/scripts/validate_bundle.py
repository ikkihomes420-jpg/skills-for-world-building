#!/usr/bin/env python3
"""Validate a Living Canon OS YAML/JSON bundle.

Usage: validate_bundle.py <bundle-path> [--strict]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to validate YAML bundles.") from exc

ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*\.[a-z0-9][a-z0-9-]*(?:-[0-9]+)?$")
VALID_STATUS = {"approved", "provisional", "disputed", "deprecated", "superseded", "archived", "active", "proposed", "applied", "reverted", "rejected"}
VALID_AUTHORITY = {"user-approved", "source-backed", "imported", "assistant-proposed", "inferred"}
VALID_CONFIDENCE = {"confirmed", "plausible", "speculative", "unknown"}
VALID_BRANCH = {"mainline", "alternate", "hypothetical", "abandoned"}
VALID_DISCUSSION_DISPOSITIONS = {"exploratory", "analysis", "reference", "draft", "rejected"}
VALID_DETAIL_LEVELS = {"verbatim", "detailed", "summary"}

REQUIRED: dict[str, tuple[str, ...]] = {
    "manifest": ("id", "name", "version", "status", "design_promise"),
    "entity": ("id", "type", "label", "status", "authority", "confidence"),
    "claim": ("id", "statement", "status", "authority", "confidence"),
    "rule": ("id", "statement", "layer", "strength", "scope", "status", "authority", "confidence"),
    "event": ("id", "label", "summary", "status", "authority", "confidence"),
    "knowledge": ("id", "proposition", "truth_status", "holders", "status", "authority", "confidence"),
    "relationship": ("id", "from_id", "to_id", "relation_type", "status", "authority", "confidence"),
    "decision": ("id", "question", "status", "authority", "confidence"),
    "open-question": ("id", "question", "status", "authority", "confidence"),
    "actor-state": ("id", "entity_id", "status", "authority", "confidence"),
    "consequence": ("id", "origin", "current_state", "status", "authority", "confidence"),
    "state-transition": ("id", "from_state", "next_state", "state_delta", "status", "authority", "confidence"),
    "change-set": ("id", "from_version", "to_version", "status", "changes"),
    "audit-finding": ("id", "severity", "type", "status", "authority", "confidence"),
    "source": ("id", "source_type", "locator", "reliability", "use_status"),
    "transaction": ("id", "title", "status", "operations", "created_at"),
    "discussion": ("id", "title", "content", "disposition", "canonical_status", "detail_level", "status", "authority", "confidence", "branch", "created_at"),
}

REFERENCE_FIELDS = {
    "entity_id", "from_id", "to_id", "affected_ids", "dependencies", "holders",
    "support", "contradicts", "sources", "knowledge_accounts", "knowledge_ids",
    "related_ids", "target_id", "replacement_ids", "origin", "supersedes",
    "redirects_to", "records_changed", "consequences_created", "consequences_resolved",
}


def load_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)


def iter_data_files(bundle: Path) -> list[Path]:
    ignored = {".git", "__pycache__", ".venv", "node_modules", ".canon"}
    return sorted(
        path for path in bundle.rglob("*")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json"}
        and not any(part in ignored for part in path.parts)
    )


def references_in(record: Any) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if not isinstance(record, dict):
        return found
    for key, value in record.items():
        if key in REFERENCE_FIELDS:
            values = value if isinstance(value, list) else [value]
            for item in values:
                if isinstance(item, str) and ID_PATTERN.match(item):
                    found.append((key, item))
        if isinstance(value, dict):
            found.extend(references_in(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    found.extend(references_in(item))
    return found


def records_from_loaded(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Living Canon OS bundle.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat unresolved internal references as errors.")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}")
        return 2

    files = iter_data_files(bundle)
    if not files:
        print(f"ERROR: No YAML or JSON records found in {bundle}")
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    records: list[tuple[Path, dict[str, Any]]] = []

    for path in files:
        try:
            loaded = load_file(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(bundle)}: unreadable YAML/JSON ({exc})")
            continue
        for record in records_from_loaded(loaded):
            records.append((path, record))
        if loaded is None:
            warnings.append(f"{path.relative_to(bundle)}: empty file ignored")
        elif not isinstance(loaded, (dict, list)):
            errors.append(f"{path.relative_to(bundle)}: root must be a mapping or list of mappings")

    ids: dict[str, tuple[Path, dict[str, Any]]] = {}
    manifest_count = 0
    for path, record in records:
        rel = path.relative_to(bundle)
        kind = record.get("kind")
        record_id = record.get("id")
        if not kind:
            errors.append(f"{rel}: missing required field 'kind'")
            continue
        if kind not in REQUIRED:
            warnings.append(f"{rel}: unknown kind '{kind}' was not checked against a full schema")
        if kind == "manifest":
            manifest_count += 1
        if not record_id or not isinstance(record_id, str):
            errors.append(f"{rel}: missing or invalid required field 'id'")
        elif not ID_PATTERN.match(record_id):
            errors.append(f"{rel}: invalid id '{record_id}' (expected kind.lower-kebab-case)")
        elif record_id in ids:
            errors.append(f"{rel}: duplicate id '{record_id}' also appears in {ids[record_id][0].relative_to(bundle)}")
        else:
            ids[record_id] = (path, record)

        for field in REQUIRED.get(kind, ()):
            if field not in record or record[field] in (None, ""):
                errors.append(f"{rel} [{record_id or 'no-id'}]: missing required field '{field}'")

        status = record.get("status")
        if status is not None and status not in VALID_STATUS:
            errors.append(f"{rel} [{record_id or 'no-id'}]: invalid status '{status}'")
        authority = record.get("authority")
        if authority is not None and authority not in VALID_AUTHORITY:
            errors.append(f"{rel} [{record_id or 'no-id'}]: invalid authority '{authority}'")
        confidence = record.get("confidence")
        if confidence is not None and confidence not in VALID_CONFIDENCE:
            errors.append(f"{rel} [{record_id or 'no-id'}]: invalid confidence '{confidence}'")
        branch = record.get("branch")
        if branch is not None and branch not in VALID_BRANCH:
            errors.append(f"{rel} [{record_id or 'no-id'}]: invalid branch '{branch}'")
        if kind == "discussion":
            disposition = record.get("disposition")
            detail_level = record.get("detail_level")
            if disposition not in VALID_DISCUSSION_DISPOSITIONS:
                errors.append(f"{rel} [{record_id or 'no-id'}]: invalid discussion disposition '{disposition}'")
            if detail_level not in VALID_DETAIL_LEVELS:
                errors.append(f"{rel} [{record_id or 'no-id'}]: invalid discussion detail_level '{detail_level}'")

    if manifest_count == 0:
        errors.append("Bundle has no manifest record.")
    elif manifest_count > 1:
        errors.append(f"Bundle has {manifest_count} manifest records; it must have exactly one.")

    for path, record in records:
        rel = path.relative_to(bundle)
        owner = record.get("id", "no-id")
        # Transaction operations are historical proposals. Their targets may be absent
        # after a rollback, so validate their schema without treating them as live links.
        if record.get("kind") == "transaction":
            continue
        for field, reference in references_in(record):
            if reference not in ids:
                message = f"{rel} [{owner}]: unresolved reference '{reference}' in '{field}'"
                (errors if args.strict else warnings).append(message)

    print(f"Validated {len(records)} record(s) across {len(files)} data file(s) in {bundle}.")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASS: 0 error(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
