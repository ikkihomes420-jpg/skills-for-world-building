#!/usr/bin/env python3
"""Approve, apply, reject, or roll back a Living Canon transaction.

Usage:
  apply_transaction.py <bundle-path> <transaction-id> --approve-by <name>
  apply_transaction.py <bundle-path> <transaction-id> --reject --note <reason>
  apply_transaction.py <bundle-path> <transaction-id> --rollback --approve-by <name>
"""

from __future__ import annotations

import argparse
import copy
import subprocess
import sys
from pathlib import Path
from typing import Any

from canon_lib import (
    dump_data,
    get_path_value,
    load_data,
    record_fingerprint,
    record_index,
    session_delta_path,
    set_path_value,
    target_path_for_new_record,
    utc_now,
    write_record_at,
)


def transaction_path(bundle: Path, transaction_id: str) -> Path:
    return bundle / "transactions" / f"{transaction_id.replace('.', '-')}.yaml"


def stale_messages(transaction: dict[str, Any], records: dict[str, tuple[Path, int | None, dict[str, Any]]]) -> list[str]:
    problems: list[str] = []
    for operation in transaction.get("operations", []):
        op = operation.get("op")
        target_id = operation.get("target_id")
        if op == "create":
            if target_id in records:
                problems.append(f"Create target '{target_id}' already exists.")
            continue
        current = records.get(target_id)
        if current is None:
            problems.append(f"Target '{target_id}' no longer exists.")
            continue
        expected_fingerprint = operation.get("base_fingerprint")
        if expected_fingerprint and record_fingerprint(current[2]) != expected_fingerprint:
            problems.append(f"Target '{target_id}' changed since draft.")
            continue
        for field, expected in (operation.get("before") or {}).items():
            if get_path_value(current[2], field) != expected:
                problems.append(f"Target '{target_id}' field '{field}' changed since draft.")
    return problems


def apply_operations(bundle: Path, transaction: dict[str, Any]) -> list[str]:
    records = record_index(bundle)
    changed: list[str] = []
    now = utc_now()
    for operation in transaction.get("operations", []):
        op = operation["op"]
        target_id = operation["target_id"]
        if op == "create":
            record = copy.deepcopy(operation["after"])
            record["last_transaction"] = transaction["id"]
            record["updated_at"] = now
            record["last_transaction_fingerprint"] = record_fingerprint(record)
            output = target_path_for_new_record(bundle, record)
            dump_data(output, record)
            changed.append(target_id)
            continue
        path, index, current = records[target_id]
        record = copy.deepcopy(current)
        for field, value in (operation.get("after") or {}).items():
            set_path_value(record, field, value)
        record["last_transaction"] = transaction["id"]
        record["updated_at"] = now
        record["last_transaction_fingerprint"] = record_fingerprint(record)
        write_record_at(path, index, record)
        changed.append(target_id)
    return changed


def write_delta(bundle: Path, transaction: dict[str, Any], changed: list[str], event: str) -> Path:
    path = session_delta_path(bundle, transaction["id"])
    lines = [
        f"# {event}: {transaction['title']}",
        "",
        f"**Transaction:** `{transaction['id']}`  ",
        f"**Time:** `{transaction.get('applied_at') or utc_now()}`  ",
        f"**Branch:** `{transaction.get('branch', 'mainline')}`",
        "",
        "## Rationale",
        "",
        str(transaction.get("rationale") or "Not recorded."),
        "",
        "## Affected records",
        "",
    ]
    lines.extend(f"- `{record_id}`" for record_id in changed)
    if transaction.get("source_locators"):
        lines.extend(["", "## Evidence", ""])
        lines.extend(f"- `{source}`" for source in transaction["source_locators"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def rebuild_derived_views(bundle: Path) -> None:
    for script_name in ("build_snapshot.py", "build_index.py"):
        script = Path(__file__).with_name(script_name)
        subprocess.run([sys.executable, str(script), str(bundle)], check=True, capture_output=True, text=True)


def rollback(bundle: Path, transaction: dict[str, Any], approver: str) -> tuple[list[str], list[str]]:
    """Reverse a transaction only if every target remains untouched since application."""
    records = record_index(bundle)
    problems: list[str] = []
    planned: list[tuple[dict[str, Any], tuple[Path, int | None, dict[str, Any]]]] = []
    now = utc_now()

    # Complete preflight before touching any file. A rollback must be atomic at the
    # operation level: one blocked target prevents every other target from changing.
    for operation in reversed(transaction.get("operations", [])):
        target_id = operation["target_id"]
        location = records.get(target_id)
        if location is None:
            problems.append(f"Cannot roll back '{target_id}': it no longer exists.")
            continue
        path, index, record = location
        if record.get("last_transaction") != transaction["id"] or record_fingerprint(record) != record.get("last_transaction_fingerprint"):
            problems.append(f"Cannot roll back '{target_id}': it was changed after this transaction.")
            continue
        if operation["op"] == "create" and index is not None:
            problems.append(f"Cannot roll back list-backed created record '{target_id}' automatically.")
            continue
        planned.append((operation, location))

    if problems:
        return [], problems

    changed: list[str] = []
    for operation, (path, index, record) in planned:
        target_id = operation["target_id"]
        if operation["op"] == "create":
            path.unlink(missing_ok=True)
            changed.append(target_id)
            continue
        restored = copy.deepcopy(record)
        for field, value in (operation.get("before") or {}).items():
            set_path_value(restored, field, value)
        restored["last_transaction"] = f"rollback.{transaction['id']}"
        restored["updated_at"] = now
        restored["last_transaction_fingerprint"] = record_fingerprint(restored)
        write_record_at(path, index, restored)
        changed.append(target_id)

    transaction["status"] = "reverted"
    transaction["rollback"] = {"approved_by": approver, "applied_at": now}
    return changed, []


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply or roll back a reviewable Living Canon transaction.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("transaction_id")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--approve-by", help="Approver identity; applies a proposed transaction.")
    action.add_argument("--reject", action="store_true", help="Reject without changing canon records.")
    action.add_argument("--rollback", action="store_true", help="Safely revert an applied transaction.")
    parser.add_argument("--note", help="Required review note for rejection; optional approval/rollback note.")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    path = transaction_path(bundle, args.transaction_id)
    if not path.is_file():
        print(f"ERROR: Transaction not found: {path}", file=sys.stderr)
        return 1
    transaction = load_data(path)
    if not isinstance(transaction, dict) or transaction.get("kind") != "transaction":
        print(f"ERROR: Not a transaction record: {path}", file=sys.stderr)
        return 1

    if args.reject:
        if transaction.get("status") != "proposed":
            print(f"ERROR: Only proposed transactions can be rejected (current: {transaction.get('status')}).", file=sys.stderr)
            return 1
        if not args.note:
            print("ERROR: Rejection requires --note.", file=sys.stderr)
            return 1
        transaction["status"] = "rejected"
        transaction.setdefault("review_notes", []).append({"at": utc_now(), "note": args.note})
        dump_data(path, transaction)
        print(f"Rejected transaction: {args.transaction_id}")
        return 0

    if args.rollback:
        if transaction.get("status") != "applied":
            print(f"ERROR: Only applied transactions can be rolled back (current: {transaction.get('status')}).", file=sys.stderr)
            return 1
        approver = args.note or "author-approved rollback"
        changed, problems = rollback(bundle, transaction, approver)
        if problems:
            print("ERROR: Rollback stopped; no transaction status was changed:", file=sys.stderr)
            for problem in problems:
                print(f"- {problem}", file=sys.stderr)
            return 1
        dump_data(path, transaction)
        delta = write_delta(bundle, transaction, changed, "Rolled back transaction")
        rebuild_derived_views(bundle)
        print(f"Rolled back transaction: {args.transaction_id}")
        print(f"Wrote delta: {delta}")
        return 0

    if transaction.get("status") != "proposed":
        print(f"ERROR: Only proposed transactions can be applied (current: {transaction.get('status')}).", file=sys.stderr)
        return 1
    stale = stale_messages(transaction, record_index(bundle))
    if stale:
        print("ERROR: Transaction is stale; reconcile before approval:", file=sys.stderr)
        for item in stale:
            print(f"- {item}", file=sys.stderr)
        return 1
    changed = apply_operations(bundle, transaction)
    transaction["status"] = "applied"
    transaction["applied_at"] = utc_now()
    transaction["approval"] = {"approved_by": args.approve_by, "note": args.note}
    dump_data(path, transaction)
    delta = write_delta(bundle, transaction, changed, "Applied transaction")
    rebuild_derived_views(bundle)
    print(f"Applied transaction: {args.transaction_id}")
    print(f"Updated records: {', '.join(changed)}")
    print(f"Wrote delta: {delta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
