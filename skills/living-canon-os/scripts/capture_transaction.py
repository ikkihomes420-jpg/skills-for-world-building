#!/usr/bin/env python3
"""Create a proposed Living Canon transaction from a YAML/JSON capture spec.

Usage: capture_transaction.py <bundle-path> <capture-spec> [--id <transaction-id>]

The capture spec accepts `title`, `rationale`, `source_locators`, and `operations`.
Operations are `create`, `update`, `deprecate`, or `redirect`.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

from canon_lib import (
    ID_PATTERN,
    dump_data,
    get_manifest,
    get_path_value,
    load_data,
    make_transaction_id,
    record_fingerprint,
    record_index,
    transaction_dir,
    utc_now,
)


def normalize_operation(operation: dict[str, Any], records: dict[str, tuple[Path, int | None, dict[str, Any]]]) -> dict[str, Any]:
    op = operation.get("op")
    if op == "create":
        record = operation.get("record")
        if not isinstance(record, dict):
            raise ValueError("Create operation requires a mapping in 'record'.")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not ID_PATTERN.match(record_id):
            raise ValueError(f"Create operation has invalid record id: {record_id!r}")
        if record_id in records:
            raise ValueError(f"Create operation conflicts with existing ID '{record_id}'.")
        return {"op": "create", "target_id": record_id, "before": None, "after": copy.deepcopy(record)}

    target_id = operation.get("target_id")
    if not isinstance(target_id, str) or target_id not in records:
        raise ValueError(f"Operation '{op}' references unknown target_id '{target_id}'.")
    before_record = records[target_id][2]

    if op == "update":
        changes = operation.get("set")
        if not isinstance(changes, dict) or not changes:
            raise ValueError("Update operation requires a non-empty mapping in 'set'.")
        before = {field: get_path_value(before_record, field) for field in changes}
        return {"op": "update", "target_id": target_id, "before": before, "after": copy.deepcopy(changes), "base_fingerprint": record_fingerprint(before_record)}

    if op == "deprecate":
        return {
            "op": "deprecate",
            "target_id": target_id,
            "before": {"status": before_record.get("status"), "supersedes": before_record.get("supersedes")},
            "after": {"status": "deprecated", "supersedes": operation.get("supersedes")},
            "base_fingerprint": record_fingerprint(before_record),
        }

    if op == "redirect":
        replacement = operation.get("replacement_id")
        if not isinstance(replacement, str) or replacement not in records:
            raise ValueError("Redirect operation requires an existing replacement_id.")
        return {
            "op": "redirect",
            "target_id": target_id,
            "before": {"redirects_to": before_record.get("redirects_to"), "status": before_record.get("status")},
            "after": {"redirects_to": replacement, "status": "superseded"},
            "base_fingerprint": record_fingerprint(before_record),
        }

    raise ValueError(f"Unsupported operation '{op}'.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a reviewable proposed canon transaction.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("capture_spec", type=Path, help="YAML or JSON transaction proposal.")
    parser.add_argument("--id", dest="transaction_id", help="Optional stable transaction ID.")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    spec_path = args.capture_spec.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2
    if not spec_path.is_file():
        print(f"ERROR: Capture spec is not a file: {spec_path}", file=sys.stderr)
        return 2
    try:
        manifest = get_manifest(bundle)
        spec = load_data(spec_path)
        if not isinstance(spec, dict):
            raise ValueError("Capture spec root must be a mapping.")
        title = str(spec.get("title") or "Canon update")
        raw_operations = spec.get("operations")
        if not isinstance(raw_operations, list) or not raw_operations:
            raise ValueError("Capture spec requires a non-empty operations list.")
        records = record_index(bundle)
        operations = [normalize_operation(item, records) for item in raw_operations if isinstance(item, dict)]
        if len(operations) != len(raw_operations):
            raise ValueError("Every operation must be a mapping.")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    transaction_id = args.transaction_id or make_transaction_id(title)
    if not ID_PATTERN.match(transaction_id):
        print(f"ERROR: Invalid transaction ID '{transaction_id}'.", file=sys.stderr)
        return 1
    output = transaction_dir(bundle) / f"{transaction_id.replace('.', '-')}.yaml"
    if output.exists():
        print(f"ERROR: Transaction already exists: {output}", file=sys.stderr)
        return 1

    transaction = {
        "kind": "transaction",
        "id": transaction_id,
        "title": title,
        "rationale": spec.get("rationale"),
        "status": "proposed",
        "authority": spec.get("authority", "assistant-proposed"),
        "branch": spec.get("branch", (manifest.get("canon_policy") or {}).get("default_branch", "mainline")),
        "source_locators": spec.get("source_locators", []),
        "created_at": utc_now(),
        "operations": operations,
        "review_notes": [],
        "approval": None,
    }
    dump_data(output, transaction)
    print(f"Created proposed transaction: {output}")
    print(f"Policy: {(manifest.get('canon_policy') or {}).get('capture_mode', 'approval-required')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
