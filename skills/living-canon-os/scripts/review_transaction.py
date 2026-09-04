#!/usr/bin/env python3
"""Render a proposed or applied Living Canon transaction as a reviewable diff.

Usage: review_transaction.py <bundle-path> <transaction-id> [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from canon_lib import get_path_value, load_data, record_fingerprint, record_index


def transaction_path(bundle: Path, transaction_id: str) -> Path:
    return bundle / "transactions" / f"{transaction_id.replace('.', '-')}.yaml"


def display(value: Any) -> str:
    if value is None:
        return "*(unset)*"
    if isinstance(value, (dict, list)):
        return "`" + json.dumps(value, ensure_ascii=False, sort_keys=True) + "`"
    return str(value).replace("\n", " ")


def review(bundle: Path, transaction: dict[str, Any]) -> dict[str, Any]:
    records = record_index(bundle)
    operations: list[dict[str, Any]] = []
    stale: list[str] = []
    for operation in transaction.get("operations", []):
        op = operation.get("op")
        target_id = operation.get("target_id")
        detail: dict[str, Any] = {"op": op, "target_id": target_id, "before": operation.get("before"), "after": operation.get("after")}
        if op == "create":
            if target_id in records:
                stale.append(f"Create target '{target_id}' now already exists.")
        else:
            current = records.get(target_id)
            if current is None:
                stale.append(f"Target '{target_id}' no longer exists.")
            else:
                expected_fingerprint = operation.get("base_fingerprint")
                if expected_fingerprint and record_fingerprint(current[2]) != expected_fingerprint:
                    detail["stale_fingerprint"] = True
                    stale.append(f"Target '{target_id}' changed since this transaction was drafted.")
                elif isinstance(operation.get("before"), dict):
                    mismatches = []
                    for path, expected in operation["before"].items():
                        actual = get_path_value(current[2], path)
                        if actual != expected:
                            mismatches.append({"path": path, "expected": expected, "actual": actual})
                    if mismatches:
                        detail["stale_differences"] = mismatches
                        stale.append(f"Target '{target_id}' changed since this transaction was drafted.")
        operations.append(detail)
    return {
        "id": transaction.get("id"),
        "title": transaction.get("title"),
        "status": transaction.get("status"),
        "authority": transaction.get("authority"),
        "branch": transaction.get("branch"),
        "rationale": transaction.get("rationale"),
        "source_locators": transaction.get("source_locators", []),
        "operations": operations,
        "stale": stale,
        "approval": transaction.get("approval"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a Living Canon transaction without applying it.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("transaction_id")
    parser.add_argument("--json", action="store_true")
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
    report = review(bundle, transaction)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"# Review: `{report['id']}`\n")
    print(f"**Title:** {report['title']}  ")
    print(f"**Status:** `{report['status']}`  ")
    print(f"**Authority / branch:** `{report['authority']}` / `{report['branch']}`  ")
    print(f"**Rationale:** {report['rationale'] or 'Not recorded.'}\n")
    if report["source_locators"]:
        print("**Evidence:** " + ", ".join(f"`{item}`" for item in report["source_locators"]) + "\n")

    print("## Proposed changes\n")
    for number, operation in enumerate(report["operations"], start=1):
        print(f"### {number}. `{operation['op']}` — `{operation['target_id']}`\n")
        if operation["op"] == "create":
            print("This creates the following record:\n")
            print("```yaml")
            import yaml
            print(yaml.safe_dump(operation["after"], sort_keys=False, allow_unicode=True).rstrip())
            print("```\n")
        else:
            print("| Field | Current at draft | Proposed value |")
            print("|---|---|---|")
            before = operation.get("before") or {}
            after = operation.get("after") or {}
            for field in sorted(set(before) | set(after)):
                print(f"| `{field}` | {display(before.get(field))} | {display(after.get(field))} |")
            print()
        for mismatch in operation.get("stale_differences", []):
            print(f"> **Stale draft warning:** `{mismatch['path']}` is now `{display(mismatch['actual'])}`, not `{display(mismatch['expected'])}`.\n")

    print("## Decision\n")
    if report["stale"]:
        print("This proposal has stale assumptions. Reconcile it before approval:\n")
        for item in report["stale"]:
            print(f"- {item}")
    elif report["status"] == "proposed":
        print("The proposal is internally current. Approve with `apply_transaction.py` or reject by changing its status to `rejected` with a review note.\n")
    else:
        print(f"This transaction is `{report['status']}`.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
