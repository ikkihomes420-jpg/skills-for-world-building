#!/usr/bin/env python3
"""Validate a structured conlang JSON bundle.

Usage:
    python validate_language_bundle.py path/to/language.json [--strict]

This validator checks declared structure and cross-references. It does not
establish grammaticality, IPA accuracy, naturalism, semantics, historical
plausibility, originality, or cultural appropriateness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


VALID_STATES = {"proposed", "approved", "deprecated", "exception", "open"}
VALID_APPLICATIONS = {"simultaneous", "iterative", "left_to_right", "right_to_left"}


def add(report: dict[str, list[dict[str, str]]], level: str, code: str, message: str) -> None:
    report[level].append({"code": code, "message": message})


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def label(section: str, index: int) -> str:
    return f"{section}[{index}]"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a structured conlang JSON bundle.")
    parser.add_argument("bundle", type=Path, help="JSON file containing language state")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as a failing result")
    args = parser.parse_args()

    report: dict[str, list[dict[str, str]]] = {"errors": [], "warnings": []}
    try:
        data = json.loads(args.bundle.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(json.dumps({"errors": [{"code": "FILE", "message": "Bundle file was not found."}]}))
        return 2
    except json.JSONDecodeError as exc:
        print(json.dumps({"errors": [{"code": "JSON", "message": str(exc)}]}))
        return 2

    if not isinstance(data, dict):
        add(report, "errors", "ROOT", "The bundle must be a JSON object.")
        print(json.dumps(report, indent=2))
        return 1

    for section in ("language", "profile", "phonology", "writing", "lexicon"):
        if section not in data:
            add(report, "errors", "SECTION", f"Missing required section: {section}.")

    schema_version = data.get("schema_version")
    if schema_version is None:
        add(report, "warnings", "SCHEMA_VERSION", "No schema_version; treating the bundle as legacy-compatible.")
    elif not nonempty(schema_version):
        add(report, "errors", "SCHEMA_VERSION", "schema_version must be a non-empty string.")

    language = mapping(data.get("language"))
    if not nonempty(language.get("id")) or not nonempty(language.get("version")):
        add(report, "errors", "MANIFEST", "language.id and language.version are required.")

    constraints = items(data.get("constraints"))
    constraint_ids: set[str] = set()
    for index, constraint in enumerate(constraints, start=1):
        item_label = label("constraints", index)
        if not isinstance(constraint, dict):
            add(report, "errors", "CONSTRAINT_TYPE", f"{item_label} must be an object.")
            continue
        constraint_id = constraint.get("id")
        if not nonempty(constraint_id):
            add(report, "errors", "CONSTRAINT_ID", f"{item_label} lacks an id.")
        elif constraint_id in constraint_ids:
            add(report, "errors", "CONSTRAINT_ID", f"Duplicate constraint id '{constraint_id}'.")
        else:
            constraint_ids.add(constraint_id)
        for field in ("statement", "pass_condition"):
            if not nonempty(constraint.get(field)):
                add(report, "warnings", "CONSTRAINT_FIELD", f"{item_label} lacks a documented {field}.")

    phonology = mapping(data.get("phonology"))
    normalization = phonology.get("normalization")
    if normalization is not None and normalization not in {"NFC", "NFD", "NFKC", "NFKD"}:
        add(report, "warnings", "NORMALIZATION", f"Unknown phonology.normalization '{normalization}'.")

    phoneme_ids: set[str] = set()
    phoneme_symbols: set[str] = set()
    raw_phonemes = items(phonology.get("phonemes"))
    if not raw_phonemes:
        add(report, "warnings", "PHONEMES", "No phoneme inventory supplied; segment coverage cannot be checked.")
    for index, phoneme in enumerate(raw_phonemes, start=1):
        item_label = label("phonology.phonemes", index)
        if isinstance(phoneme, str):
            symbol = phoneme.strip()
            if not symbol:
                add(report, "errors", "PHONEME", f"{item_label} cannot be empty.")
            elif symbol in phoneme_symbols:
                add(report, "warnings", "PHONEME_DUPLICATE", f"Duplicate legacy phoneme symbol '{symbol}'.")
            else:
                phoneme_symbols.add(symbol)
            continue
        if not isinstance(phoneme, dict):
            add(report, "errors", "PHONEME_TYPE", f"{item_label} must be a string or object.")
            continue
        phoneme_id = phoneme.get("id")
        symbol = phoneme.get("symbol")
        if not nonempty(phoneme_id) or not nonempty(symbol):
            add(report, "errors", "PHONEME_FIELD", f"{item_label} requires non-empty id and symbol.")
            continue
        if phoneme_id in phoneme_ids:
            add(report, "errors", "PHONEME_ID", f"Duplicate phoneme id '{phoneme_id}'.")
        phoneme_ids.add(phoneme_id)
        if symbol in phoneme_symbols:
            add(report, "warnings", "PHONEME_DUPLICATE", f"Duplicate phoneme symbol '{symbol}'.")
        phoneme_symbols.add(symbol)

    group_ids: set[str] = set()
    for index, group in enumerate(items(phonology.get("groups")), start=1):
        item_label = label("phonology.groups", index)
        if not isinstance(group, dict):
            add(report, "errors", "GROUP_TYPE", f"{item_label} must be an object.")
            continue
        group_id = group.get("id")
        if not nonempty(group_id):
            add(report, "errors", "GROUP_ID", f"{item_label} lacks an id.")
            continue
        if group_id in group_ids:
            add(report, "errors", "GROUP_ID", f"Duplicate group id '{group_id}'.")
        group_ids.add(group_id)
        members = items(group.get("members"))
        if not members:
            add(report, "warnings", "GROUP_MEMBERS", f"{item_label} has no members.")
        for member in members:
            if phoneme_ids and member not in phoneme_ids:
                add(report, "warnings", "GROUP_MEMBER", f"{item_label} references unknown phoneme id '{member}'.")

    for index, template in enumerate(items(phonology.get("syllable_templates")), start=1):
        item_label = label("phonology.syllable_templates", index)
        if isinstance(template, str):
            continue
        if not isinstance(template, dict):
            add(report, "errors", "TEMPLATE_TYPE", f"{item_label} must be a string or object.")
            continue
        if not nonempty(template.get("id")):
            add(report, "errors", "TEMPLATE_ID", f"{item_label} lacks an id.")
        slots = items(template.get("slots"))
        if not slots:
            add(report, "warnings", "TEMPLATE_SLOTS", f"{item_label} has no declared slots.")
        for slot_index, slot in enumerate(slots, start=1):
            slot_label = f"{item_label}.slots[{slot_index}]"
            if not isinstance(slot, dict):
                add(report, "errors", "TEMPLATE_SLOT", f"{slot_label} must be an object.")
                continue
            group = slot.get("group")
            phoneme = slot.get("phoneme")
            if not group and not phoneme:
                add(report, "errors", "TEMPLATE_SLOT", f"{slot_label} must name a group or phoneme.")
            if group and group_ids and group not in group_ids:
                add(report, "warnings", "TEMPLATE_GROUP", f"{slot_label} references unknown group '{group}'.")
            if phoneme and phoneme_ids and phoneme not in phoneme_ids:
                add(report, "warnings", "TEMPLATE_PHONEME", f"{slot_label} references unknown phoneme '{phoneme}'.")

    writing = mapping(data.get("writing"))
    writing_normalization = writing.get("unicode_normalization")
    if writing_normalization is not None and writing_normalization not in {"NFC", "NFD", "NFKC", "NFKD"}:
        add(report, "warnings", "WRITING_NORMALIZATION", f"Unknown writing.unicode_normalization '{writing_normalization}'.")
    direction = writing.get("direction")
    if direction is not None and direction not in {"LTR", "RTL", "mixed"}:
        add(report, "warnings", "WRITING_DIRECTION", f"Unknown writing.direction '{direction}'.")

    lexicon = items(data.get("lexicon"))
    forms: list[str] = []
    lexeme_ids: set[str] = set()
    sense_ids: set[str] = set()
    for index, entry in enumerate(lexicon, start=1):
        item_label = label("lexicon", index)
        if not isinstance(entry, dict):
            add(report, "errors", "LEX_TYPE", f"{item_label} must be an object.")
            continue
        for field in ("id", "headword", "pos", "status"):
            if not nonempty(entry.get(field)):
                add(report, "errors", "LEX_FIELD", f"{item_label} lacks required field {field}.")
        lexeme_id = entry.get("id")
        if nonempty(lexeme_id):
            if lexeme_id in lexeme_ids:
                add(report, "errors", "LEX_ID", f"Duplicate lexeme id '{lexeme_id}'.")
            lexeme_ids.add(lexeme_id)
        status = entry.get("status")
        if nonempty(status) and status not in VALID_STATES:
            add(report, "warnings", "LEX_STATUS", f"{item_label} uses an unrecognized status '{status}'.")
        form = str(entry.get("headword", "")).strip()
        if form:
            forms.append(form.casefold())
            for cluster in items(phonology.get("illegal_clusters")):
                if str(cluster) and str(cluster) in form:
                    add(report, "errors", "ILLEGAL_CLUSTER", f"{item_label} headword '{form}' contains prohibited cluster '{cluster}'.")
        forms_bundle = entry.get("forms")
        if forms_bundle is not None and not isinstance(forms_bundle, dict):
            add(report, "errors", "LEX_FORMS", f"{item_label}.forms must be an object when supplied.")
        provenance = entry.get("provenance")
        if provenance is not None and not isinstance(provenance, dict):
            add(report, "errors", "LEX_PROVENANCE", f"{item_label}.provenance must be an object when supplied.")
        if status == "approved" and provenance is None:
            add(report, "warnings", "LEX_PROVENANCE", f"Approved {item_label} has no provenance record.")
        tokens = items(entry.get("tokenization"))
        for token in tokens:
            if phoneme_ids and token not in phoneme_ids:
                add(report, "warnings", "LEX_TOKEN", f"{item_label} tokenization references unknown phoneme id '{token}'.")
        senses = items(entry.get("senses"))
        if status == "approved" and not senses:
            add(report, "warnings", "LEX_SENSE", f"Approved {item_label} has no documented sense.")
        for sense_index, sense in enumerate(senses, start=1):
            sense_label = f"{item_label}.senses[{sense_index}]"
            if not isinstance(sense, dict):
                add(report, "errors", "SENSE_TYPE", f"{sense_label} must be an object.")
                continue
            sense_id = sense.get("id")
            if not nonempty(sense_id):
                add(report, "warnings", "SENSE_ID", f"{sense_label} lacks a stable id.")
            elif sense_id in sense_ids:
                add(report, "errors", "SENSE_ID", f"Duplicate sense id '{sense_id}'.")
            else:
                sense_ids.add(sense_id)
            if status == "approved" and not nonempty(sense.get("definition")):
                add(report, "warnings", "SENSE_DEFINITION", f"Approved {sense_label} lacks a definition.")

    for form, count in Counter(forms).items():
        if count > 1:
            add(report, "errors", "DUPLICATE", f"Duplicate headword after case-folding: '{form}' ({count} entries).")

    all_rules: list[tuple[str, Any]] = []
    for section in ("rules", "morphology_rules", "rewrite_rules"):
        all_rules.extend((section, value) for value in items(data.get(section)))
    seen_rule_ids: set[str] = set()
    seen_orders: dict[str, set[int]] = {}
    for index, (section, rule) in enumerate(all_rules, start=1):
        item_label = f"{section}[{index}]"
        if not isinstance(rule, dict):
            add(report, "errors", "RULE_TYPE", f"{item_label} must be an object.")
            continue
        rule_id = rule.get("id")
        if not nonempty(rule_id):
            add(report, "errors", "RULE_ID", f"{item_label} lacks id.")
        elif rule_id in seen_rule_ids:
            add(report, "errors", "RULE_ID", f"Duplicate rule id '{rule_id}'.")
        else:
            seen_rule_ids.add(rule_id)
        rule_order = rule.get("order")
        if not isinstance(rule_order, int):
            add(report, "errors", "RULE_ORDER", f"{item_label} requires integer order.")
        else:
            layer = str(rule.get("layer", section))
            layer_orders = seen_orders.setdefault(layer, set())
            if rule_order in layer_orders:
                add(report, "warnings", "RULE_ORDER", f"{item_label} shares order {rule_order} within layer '{layer}'; precedence is ambiguous.")
            layer_orders.add(rule_order)
        when = mapping(rule.get("when"))
        match = when.get("match")
        if match:
            try:
                re.compile(str(match))
            except re.error as exc:
                add(report, "errors", "RULE_REGEX", f"{item_label} has invalid match regex: {exc}.")
        if section in {"rules", "morphology_rules"} and not rule.get("transform"):
            add(report, "errors", "RULE_TRANSFORM", f"{item_label} lacks transform.")
        if section == "rewrite_rules":
            if "input" not in rule or "output" not in rule:
                add(report, "errors", "REWRITE_FIELDS", f"{item_label} requires input and output.")
            application = rule.get("application")
            if application not in VALID_APPLICATIONS:
                add(report, "errors", "REWRITE_APPLICATION", f"{item_label} requires a valid application model.")

    candidates = items(data.get("candidates"))
    candidate_ids: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        item_label = label("candidates", index)
        if not isinstance(candidate, dict):
            add(report, "errors", "CANDIDATE_TYPE", f"{item_label} must be an object.")
            continue
        candidate_id = candidate.get("id")
        if not nonempty(candidate_id):
            add(report, "errors", "CANDIDATE_ID", f"{item_label} lacks an id.")
        elif candidate_id in candidate_ids:
            add(report, "errors", "CANDIDATE_ID", f"Duplicate candidate id '{candidate_id}'.")
        else:
            candidate_ids.add(candidate_id)
        if not nonempty(candidate.get("verdict")):
            add(report, "warnings", "CANDIDATE_VERDICT", f"{item_label} lacks a curation verdict.")

    corpus = items(data.get("corpus"))
    if not corpus:
        add(report, "warnings", "CORPUS", "No regression corpus entries found.")
    else:
        for index, test in enumerate(corpus, start=1):
            item_label = label("corpus", index)
            if not isinstance(test, dict) or not nonempty(mapping(test).get("id")):
                add(report, "warnings", "CORPUS", f"{item_label} should include a stable id.")

    tests = items(data.get("tests"))
    for index, test in enumerate(tests, start=1):
        item_label = label("tests", index)
        if not isinstance(test, dict) or not nonempty(mapping(test).get("id")):
            add(report, "warnings", "TEST", f"{item_label} should include a stable id.")
        elif "expected" not in test:
            add(report, "warnings", "TEST_EXPECTED", f"{item_label} lacks expected output or analysis.")

    release = mapping(data.get("release"))
    if release and language.get("version") and release.get("language_version") and release.get("language_version") != language.get("version"):
        add(report, "warnings", "RELEASE_VERSION", "release.language_version differs from language.version.")

    report["summary"] = {
        "schema_version": schema_version or "legacy",
        "lexicon_entries": len(lexicon),
        "rules": len(all_rules),
        "candidates": len(candidates),
        "corpus_tests": len(corpus),
        "declared_tests": len(tests),
        "errors": len(report["errors"]),
        "warnings": len(report["warnings"]),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] or (args.strict and report["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
