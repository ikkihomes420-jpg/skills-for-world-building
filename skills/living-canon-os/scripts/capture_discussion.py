#!/usr/bin/env python3
"""Capture an exploratory discussion without creating a canon transaction.

Usage: capture_discussion.py <bundle-path> <discussion-spec> [--id <discussion-id>]

The input YAML/JSON may include title, summary, content, disposition, detail_level,
source_locators, related_ids, tags, branch, and authority.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from canon_lib import ID_PATTERN, dump_data, load_data, make_transaction_id, record_index, slugify, utc_now

VALID_DISPOSITIONS = {"exploratory", "analysis", "reference", "draft", "rejected"}
VALID_DETAIL_LEVELS = {"verbatim", "detailed", "summary"}


def make_discussion_id(title: str) -> str:
    transaction_id = make_transaction_id(title)
    return "discussion." + transaction_id.split(".", 1)[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Store a rich exploratory discussion without proposing canon.")
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("discussion_spec", type=Path)
    parser.add_argument("--id", dest="discussion_id")
    args = parser.parse_args()

    bundle = args.bundle_path.expanduser().resolve()
    spec_path = args.discussion_spec.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: Bundle path is not a directory: {bundle}", file=sys.stderr)
        return 2
    if not spec_path.is_file():
        print(f"ERROR: Discussion spec is not a file: {spec_path}", file=sys.stderr)
        return 2
    try:
        spec = load_data(spec_path)
        if not isinstance(spec, dict):
            raise ValueError("Discussion spec root must be a mapping.")
        title = str(spec.get("title") or "Exploratory discussion")
        content = spec.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Discussion spec requires non-empty text in 'content'.")
        disposition = str(spec.get("disposition", "exploratory"))
        detail_level = str(spec.get("detail_level", "detailed"))
        if disposition not in VALID_DISPOSITIONS:
            raise ValueError(f"Invalid disposition '{disposition}'.")
        if detail_level not in VALID_DETAIL_LEVELS:
            raise ValueError(f"Invalid detail_level '{detail_level}'.")
        known_records = record_index(bundle)
        related_ids = spec.get("related_ids", [])
        if not isinstance(related_ids, list):
            raise ValueError("related_ids must be a list.")
        missing = [item for item in related_ids if isinstance(item, str) and ID_PATTERN.match(item) and item not in known_records]
        if missing:
            raise ValueError("Unknown related ID(s): " + ", ".join(missing))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    discussion_id = args.discussion_id or make_discussion_id(title)
    if not ID_PATTERN.match(discussion_id):
        print(f"ERROR: Invalid discussion ID '{discussion_id}'.", file=sys.stderr)
        return 1
    output_dir = bundle / "discussions"
    output = output_dir / f"{slugify(discussion_id.replace('.', '-'))}.yaml"
    if output.exists() or discussion_id in known_records:
        print(f"ERROR: Discussion ID already exists: {discussion_id}", file=sys.stderr)
        return 1

    now = utc_now()
    discussion: dict[str, Any] = {
        "kind": "discussion",
        "id": discussion_id,
        "title": title,
        "summary": spec.get("summary"),
        "content": content,
        "disposition": disposition,
        "canonical_status": "not-proposed",
        "detail_level": detail_level,
        "status": "provisional",
        "authority": spec.get("authority", "user-approved"),
        "confidence": "unknown",
        "visibility": spec.get("visibility", "author-only"),
        "branch": spec.get("branch", "mainline"),
        "source_locators": spec.get("source_locators", []),
        "related_ids": related_ids,
        "tags": spec.get("tags", []),
        "created_at": now,
        "updated_at": now,
    }
    dump_data(output, discussion)
    print(f"Captured {detail_level} {disposition} discussion without proposing canon: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
