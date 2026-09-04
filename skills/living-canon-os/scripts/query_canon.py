#!/usr/bin/env python3
"""Query a derived Living Canon index and render a status-aware evidence packet.

Usage: query_canon.py <bundle-path> <query> [options]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def terms(value: str) -> list[str]:
    return [term for term in normalize(value).split() if term]


def load_index(bundle: Path, rebuild: bool) -> dict[str, Any]:
    path = bundle / ".canon" / "index.json"
    if rebuild or not path.is_file():
        script = Path(__file__).with_name("build_index.py")
        subprocess.run([sys.executable, str(script), str(bundle)], check=True)
    return json.loads(path.read_text(encoding="utf-8"))


def score_record(record: dict[str, Any], query: str, query_terms: list[str], aliases: dict[str, list[str]]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    normalized_query = normalize(query)
    record_id = normalize(record["id"])
    label = normalize(record["label"])
    text = normalize(record["text"])
    if normalized_query == record_id:
        score += 100
        reasons.append("exact ID")
    if normalized_query == label:
        score += 70
        reasons.append("exact label")
    if record["id"] in aliases.get(normalized_query, []):
        score += 60
        reasons.append("alias match")
    if record.get("has_display_label") and normalized_query and normalized_query in label:
        score += 35
        reasons.append("label phrase")
    if normalized_query and normalized_query in text:
        score += 15
        reasons.append("record phrase")
    matched_terms = sum(1 for term in query_terms if term in text)
    if matched_terms:
        score += matched_terms * 6
        reasons.append(f"{matched_terms}/{len(query_terms)} term match")
    if record["status"] == "approved":
        score += 3
    if record["authority"] == "user-approved":
        score += 2
    return score, reasons


def expand_records(index: dict[str, Any], seed_ids: list[str], hops: int, allowed_status: set[str]) -> list[str]:
    if hops <= 0:
        return []
    seen = set(seed_ids)
    frontier = list(seed_ids)
    expanded: list[str] = []
    for _ in range(hops):
        next_frontier: list[str] = []
        for record_id in frontier:
            record = index["records"].get(record_id, {})
            neighbors = list(record.get("references", [])) + list(index.get("reverse_links", {}).get(record_id, []))
            for neighbor in neighbors:
                candidate = index["records"].get(neighbor)
                if candidate and neighbor not in seen and candidate.get("status") in allowed_status:
                    seen.add(neighbor)
                    expanded.append(neighbor)
                    next_frontier.append(neighbor)
        frontier = next_frontier
        if not frontier:
            break
    return expanded


def statement(record: dict[str, Any], detail_level: str) -> str:
    brief = str(record.get("excerpt") or record.get("text", "").replace("\n", " "))
    if detail_level == "brief":
        return brief[:360]
    if detail_level == "context":
        detail = str(record.get("detail_context") or "")
        return (brief + ("\n\n" + detail if detail else ""))[:1800]
    return str(record.get("text") or brief)[:6000]


def main() -> int:
    parser = argparse.ArgumentParser(description="Query a Living Canon bundle and produce a grounded evidence packet.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("query")
    parser.add_argument("--kind", action="append", help="Limit to one or more record kinds.")
    parser.add_argument("--status", action="append", help="Limit to one or more statuses; defaults to approved.")
    parser.add_argument("--branch", default="mainline")
    parser.add_argument("--include-noncanonical", action="store_true", help="Include provisional and disputed records.")
    parser.add_argument("--hops", type=int, default=0, help="Expand direct graph neighbors up to this many hops.")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--detail", choices=["brief", "context", "full"], default="brief", help="Amount of context to render for each selected record.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the derived index first.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2
    index = load_index(bundle, args.rebuild)
    allowed_status = set(args.status or (["approved", "provisional", "disputed"] if args.include_noncanonical else ["approved"]))
    query_terms = terms(args.query)
    matches: list[dict[str, Any]] = []
    for record in index.get("records", {}).values():
        if record.get("status") not in allowed_status:
            continue
        if args.kind and record.get("kind") not in args.kind:
            continue
        if args.branch and record.get("branch", "mainline") != args.branch:
            continue
        score, reasons = score_record(record, args.query, query_terms, index.get("alias_index", {}))
        # Status and authority can boost a relevant result, but they must never
        # cause unrelated approved records to enter a targeted evidence packet.
        if reasons:
            matches.append({"record": record, "score": score, "reasons": reasons, "expanded": False})
    matches.sort(key=lambda item: (-item["score"], item["record"]["id"]))
    matches = matches[: max(args.limit, 1)]

    expanded_ids = expand_records(index, [item["record"]["id"] for item in matches], args.hops, allowed_status)
    for record_id in expanded_ids:
        if len(matches) >= max(args.limit, 1):
            break
        matches.append({"record": index["records"][record_id], "score": 0, "reasons": ["relationship expansion"], "expanded": True})

    report = {
        "kind": "evidence-packet",
        "query": args.query,
        "index_built_at": index.get("built_at"),
        "filters": {"kinds": args.kind or [], "statuses": sorted(allowed_status), "branch": args.branch, "hops": args.hops, "detail": args.detail},
        "matches": [
            {
                "id": item["record"]["id"], "kind": item["record"]["kind"], "label": item["record"]["label"],
                "status": item["record"]["status"], "authority": item["record"]["authority"],
                "confidence": item["record"]["confidence"], "branch": item["record"]["branch"],
                "sources": item["record"].get("sources", []), "references": item["record"].get("references", []),
                "score": item["score"], "reasons": item["reasons"], "expanded": item["expanded"],
                "excerpt": statement(item["record"], args.detail),
            }
            for item in matches
        ],
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"# Evidence packet: {args.query}\n")
    print(f"**Index built:** `{report['index_built_at']}`  ")
    print(f"**Filters:** branch `{args.branch}`; statuses `{', '.join(sorted(allowed_status))}`; hops `{args.hops}`; detail `{args.detail}`\n")
    if not report["matches"]:
        print("No matching canon records were found under the selected filters. This is **unknown**, not proof that the subject does not exist.\n")
        return 0
    print("| Record | Status | Confidence | Basis |")
    print("|---|---|---|---|")
    for item in report["matches"]:
        basis = "; ".join(item["reasons"])
        print(f"| `{item['id']}` — {item['label']} | {item['status']} | {item['confidence']} | {basis} |")
    print()
    for item in report["matches"]:
        heading = "Relationship context" if item["expanded"] else item["status"].capitalize()
        print(f"## {heading}: {item['label']} (`{item['id']}`)\n")
        print(item["excerpt"] + "\n")
        if item["sources"]:
            print("**Evidence:** " + ", ".join(f"`{source}`" for source in item["sources"]) + "  ")
        if item["references"]:
            print("**Linked records:** " + ", ".join(f"`{ref}`" for ref in item["references"]) + "  ")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
