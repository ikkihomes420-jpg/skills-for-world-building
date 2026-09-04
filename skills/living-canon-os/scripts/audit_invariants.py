#!/usr/bin/env python3
"""Run semantic integrity checks over a Living Canon bundle.

Usage: audit_invariants.py <bundle-path> [--output <report.md>] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from canon_lib import ID_PATTERN, load_records, utc_now


def compact(value: Any, limit: int = 170) -> str:
    text = str(value).replace("\n", " ")
    return text[:limit] + ("…" if len(text) > limit else "")


def references(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str) and ID_PATTERN.match(value):
        found.add(value)
    elif isinstance(value, dict):
        for item in value.values():
            found.update(references(item))
    elif isinstance(value, list):
        for item in value:
            found.update(references(item))
    return found


def finding(severity: str, kind: str, record_ids: list[str], message: str, repair: str) -> dict[str, Any]:
    return {"severity": severity, "type": kind, "record_ids": record_ids, "message": message, "repair": repair}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit semantic invariants in a Living Canon bundle.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("--output", type=Path, help="Default: <bundle>/audit/latest-invariant-audit.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2

    records = [record for _, _, record in load_records(bundle) if record.get("kind") not in {"transaction", "source", "manifest"}]
    by_id = {record.get("id"): record for record in records if isinstance(record.get("id"), str)}
    findings: list[dict[str, Any]] = []

    labels: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for record in records:
        record_id = record.get("id")
        label = record.get("label") or record.get("name")
        if record_id and isinstance(label, str) and record.get("kind") in {"entity", "relationship", "rule", "event"}:
            labels[(str(record.get("kind")), str(record.get("branch", "mainline")), label.strip().lower())].append(record_id)
    for (kind, branch, label, ), ids in labels.items():
        if len(ids) > 1:
            findings.append(finding("moderate", "duplicate-identity", ids, f"{kind.title()} label '{label}' occurs more than once in branch '{branch}'.", "Confirm aliases, merge deliberately, or clarify distinct identities with different display labels."))

    for record in records:
        record_id = str(record.get("id", "<missing-id>"))
        kind = record.get("kind")
        branch = record.get("branch", "mainline")
        for reference in references(record):
            if reference == record_id or reference not in by_id:
                continue
            target_branch = by_id[reference].get("branch", "mainline")
            if branch == "mainline" and target_branch != "mainline":
                findings.append(finding("major", "branch-leak", [record_id, reference], f"Mainline record '{record_id}' directly references non-mainline record '{reference}' ({target_branch}).", "Move the relationship to the branch, replace it with a mainline record, or create an approved merge transaction."))
        if kind == "relationship":
            start, end = record.get("valid_from"), record.get("valid_to")
            if isinstance(start, str) and isinstance(end, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", start) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", end) and start > end:
                findings.append(finding("major", "invalid-validity-range", [record_id], f"Relationship '{record_id}' ends before it begins ({start} > {end}).", "Correct the dates or mark the chronology uncertain rather than forcing a false order."))
        if kind == "knowledge":
            for holder in record.get("holders", []):
                if isinstance(holder, str) and ID_PATTERN.match(holder) and holder not in by_id:
                    findings.append(finding("moderate", "unknown-knowledge-holder", [record_id, holder], f"Knowledge record '{record_id}' names missing holder '{holder}'.", "Create the holder, correct the ID, or make the holder a non-record text description."))
        if kind == "rule":
            for index, exception in enumerate(record.get("exceptions", [])):
                if isinstance(exception, dict):
                    missing = [field for field in ("scope", "mechanism", "cost") if not exception.get(field)]
                    if missing:
                        findings.append(finding("minor", "underspecified-exception", [record_id], f"Rule '{record_id}' exception {index + 1} lacks {', '.join(missing)}.", "State the exception's scope, mechanism, and cost/limit so it cannot become an unlimited loophole."))
                elif exception:
                    findings.append(finding("minor", "underspecified-exception", [record_id], f"Rule '{record_id}' has an unstructured exception: {compact(exception)}.", "Convert the exception into a mapping with scope, mechanism, cost, and source."))
        if kind == "state-transition":
            if not record.get("player_choice_boundary") and record.get("authority") == "inferred":
                findings.append(finding("minor", "missing-choice-boundary", [record_id], f"Inferred transition '{record_id}' has no next choice boundary.", "Record whether the next high-impact choice belongs to the user/player or was intentionally resolved."))

    severity_order = {"major": 0, "moderate": 1, "minor": 2}
    findings.sort(key=lambda item: (severity_order.get(item["severity"], 9), item["type"], item["record_ids"]))
    report = {"kind": "invariant-audit", "audited_at": utc_now(), "record_count": len(records), "finding_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    lines = ["# Living Canon Integrity Audit", "", f"**Audited:** `{report['audited_at']}`  ", f"**Records checked:** `{report['record_count']}`  ", f"**Findings:** `{report['finding_count']}`", ""]
    if not findings:
        lines.append("No semantic integrity findings were detected by the current invariant set. This is not proof that the canon is complete; it means the configured checks found no issue.\n")
    else:
        lines.extend(["| Severity | Type | Affected records |", "|---|---|---|"])
        for item in findings:
            lines.append(f"| {item['severity']} | {item['type']} | {', '.join(f'`{record_id}`' for record_id in item['record_ids'])} |")
        for number, item in enumerate(findings, start=1):
            lines.extend(["", f"## {number}. {item['severity'].title()}: {item['type']}", "", item["message"], "", f"**Repair path:** {item['repair']}"])
    output = args.output.expanduser().resolve() if args.output else bundle / "audit" / "latest-invariant-audit.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote invariant audit with {len(findings)} finding(s): {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
