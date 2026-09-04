#!/usr/bin/env python3
"""Audit a structured conlang lexicon against project-level constraints.

Usage:
    python audit_conlang.py PATH/lexicon.csv --config PATH/phonology-audit-config.json
    python audit_conlang.py PATH/lexicon.csv --config PATH/config.json --json

The script intentionally performs only deterministic checks. It does not infer a
phonology, judge naturalism, or replace a linguistic audit. Configure the
language-specific grapheme inventory and illegal sequences before use.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Issue:
    severity: str
    row: int
    entry_id: str
    rule: str
    detail: str


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Configuration file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Configuration is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a JSON object.")
    return data


def require_string_list(config: dict[str, Any], key: str, default: list[str]) -> list[str]:
    value = config.get(key, default)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Configuration field '{key}' must be a list of strings.")
    return value


def tokenize(form: str, graphemes: list[str]) -> tuple[list[str], list[str]]:
    """Greedily tokenise a form with the longest declared grapheme first."""
    tokens: list[str] = []
    unknown: list[str] = []
    remaining = form
    ordered = sorted(set(graphemes), key=lambda item: (-len(item), item))
    while remaining:
        match = next((unit for unit in ordered if remaining.startswith(unit)), None)
        if match is None:
            unknown.append(remaining[0])
            remaining = remaining[1:]
        else:
            tokens.append(match)
            remaining = remaining[len(match) :]
    return tokens, unknown


def collect_issues(lexicon_path: Path, config: dict[str, Any]) -> tuple[list[Issue], int]:
    required_columns = require_string_list(
        config,
        "required_columns",
        ["ID", "Form", "IPA", "POS", "Gloss", "Status"],
    )
    graphemes = require_string_list(config, "graphemes", [])
    illegal_sequences = require_string_list(config, "illegal_sequences", [])
    allowed_statuses = require_string_list(config, "allowed_statuses", [])
    id_column = config.get("id_column", "ID")
    form_column = config.get("form_column", "Form")
    allow_duplicate_forms = bool(config.get("allow_duplicate_forms", False))
    allow_spaces = bool(config.get("allow_spaces", False))

    if not isinstance(id_column, str) or not isinstance(form_column, str):
        raise ValueError("'id_column' and 'form_column' must be strings.")
    if not graphemes:
        raise ValueError("'graphemes' must list at least one spelling unit.")
    if any(not unit for unit in graphemes):
        raise ValueError("'graphemes' cannot contain empty strings.")
    if any(not sequence for sequence in illegal_sequences):
        raise ValueError("'illegal_sequences' cannot contain empty strings.")

    try:
        source = lexicon_path.open("r", encoding="utf-8-sig", newline="")
    except FileNotFoundError as exc:
        raise ValueError(f"Lexicon file not found: {lexicon_path}") from exc

    issues: list[Issue] = []
    with source:
        reader = csv.DictReader(source)
        headers = reader.fieldnames or []
        missing_columns = [column for column in required_columns if column not in headers]
        if missing_columns:
            issues.append(
                Issue(
                    "error",
                    1,
                    "",
                    "required-columns",
                    f"Missing required column(s): {', '.join(missing_columns)}",
                )
            )
            return issues, 0

        ids: dict[str, int] = {}
        forms: dict[str, list[tuple[int, str]]] = {}
        row_count = 0
        for csv_row_number, row in enumerate(reader, start=2):
            row_count += 1
            entry_id = (row.get(id_column) or "").strip()
            form = (row.get(form_column) or "").strip()

            for column in required_columns:
                if not (row.get(column) or "").strip():
                    issues.append(
                        Issue(
                            "error",
                            csv_row_number,
                            entry_id or "<missing ID>",
                            "required-value",
                            f"Column '{column}' is empty.",
                        )
                    )

            if entry_id:
                if entry_id in ids:
                    issues.append(
                        Issue(
                            "error",
                            csv_row_number,
                            entry_id,
                            "duplicate-id",
                            f"Duplicates ID first used on CSV row {ids[entry_id]}.",
                        )
                    )
                else:
                    ids[entry_id] = csv_row_number

            if not form:
                continue

            forms.setdefault(form, []).append((csv_row_number, entry_id or "<missing ID>"))
            if not allow_spaces and any(character.isspace() for character in form):
                issues.append(
                    Issue(
                        "error",
                        csv_row_number,
                        entry_id or "<missing ID>",
                        "spaces-in-form",
                        "Form contains whitespace but the configuration disallows it.",
                    )
                )

            _, unknown = tokenize(form, graphemes)
            if unknown:
                issues.append(
                    Issue(
                        "error",
                        csv_row_number,
                        entry_id or "<missing ID>",
                        "undeclared-grapheme",
                        "Form contains undeclared spelling unit(s): " + ", ".join(sorted(set(unknown))),
                    )
                )

            for sequence in illegal_sequences:
                if sequence in form:
                    issues.append(
                        Issue(
                            "error",
                            csv_row_number,
                            entry_id or "<missing ID>",
                            "illegal-sequence",
                            f"Form contains forbidden sequence '{sequence}'.",
                        )
                    )

            if allowed_statuses:
                status = (row.get("Status") or "").strip()
                if status and status not in allowed_statuses:
                    issues.append(
                        Issue(
                            "warning",
                            csv_row_number,
                            entry_id or "<missing ID>",
                            "unrecognized-status",
                            f"Status '{status}' is not in the configured controlled vocabulary.",
                        )
                    )

        if not allow_duplicate_forms:
            for form, entries in forms.items():
                if len(entries) > 1:
                    positions = ", ".join(f"{entry_id} (row {row})" for row, entry_id in entries)
                    for row, entry_id in entries:
                        issues.append(
                            Issue(
                                "warning",
                                row,
                                entry_id,
                                "duplicate-form",
                                f"Form '{form}' also occurs in: {positions}.",
                            )
                        )

    return issues, row_count


def print_text_report(issues: list[Issue], row_count: int, lexicon_path: Path) -> None:
    counts = Counter(issue.severity for issue in issues)
    print(f"Conlang audit: {lexicon_path}")
    print(f"Entries scanned: {row_count}")
    print(f"Errors: {counts['error']}  Warnings: {counts['warning']}")
    if not issues:
        print("PASS: No configured issues found.")
        return
    print()
    for issue in issues:
        entry = f" [{issue.entry_id}]" if issue.entry_id else ""
        print(f"{issue.severity.upper()} row {issue.row}{entry} {issue.rule}: {issue.detail}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a CSV conlang lexicon using a JSON configuration.")
    parser.add_argument("lexicon", type=Path, help="UTF-8 CSV lexicon file")
    parser.add_argument("--config", required=True, type=Path, help="JSON audit configuration")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report")
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Return a non-zero exit code when warnings are found as well as errors.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        config = load_json(args.config)
        issues, row_count = collect_issues(args.lexicon, config)
    except ValueError as exc:
        print(f"CONFIGURATION ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {
                    "lexicon": str(args.lexicon),
                    "entries_scanned": row_count,
                    "errors": sum(issue.severity == "error" for issue in issues),
                    "warnings": sum(issue.severity == "warning" for issue in issues),
                    "issues": [asdict(issue) for issue in issues],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print_text_report(issues, row_count, args.lexicon)

    has_error = any(issue.severity == "error" for issue in issues)
    has_warning = any(issue.severity == "warning" for issue in issues)
    return 1 if has_error or (args.fail_on_warning and has_warning) else 0


if __name__ == "__main__":
    raise SystemExit(main())
