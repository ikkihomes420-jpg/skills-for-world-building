#!/usr/bin/env python3
"""Validate a JSON research bundle used by the AI Research Suite governance layer.

Usage:
    python validate_research_bundle.py path/to/research.json [--strict]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def add(report: dict[str, list[dict[str, str]]], level: str, code: str, message: str) -> None:
    report[level].append({"code": code, "message": message})


def records(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def collect_ids(rows: list[Any], section: str, report: dict[str, list[dict[str, str]]]) -> set[str]:
    seen: list[str] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or not row.get("id"):
            add(report, "errors", "ID", f"{section}[{index}] requires an id.")
            continue
        seen.append(str(row["id"]))
    for ident, count in Counter(seen).items():
        if count > 1:
            add(report, "errors", "DUPLICATE_ID", f"{section} has duplicate id '{ident}'.")
    return set(seen)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an evidence-first research JSON bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    report: dict[str, list[dict[str, str]]] = {"errors": [], "warnings": []}
    try:
        bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(json.dumps({"errors": [{"code": "FILE", "message": "Research bundle was not found."}]}))
        return 2
    except json.JSONDecodeError as exc:
        print(json.dumps({"errors": [{"code": "JSON", "message": str(exc)}]}))
        return 2

    if not isinstance(bundle, dict):
        add(report, "errors", "ROOT", "The research bundle must be a JSON object.")
        print(json.dumps(report, indent=2))
        return 1

    project = bundle.get("project", {})
    if not isinstance(project, dict):
        add(report, "errors", "PROJECT", "project must be an object.")
        project = {}
    for field in ("id", "question", "status"):
        if not project.get(field):
            add(report, "errors", "PROJECT_FIELD", f"project requires {field}.")

    hypotheses = records(bundle.get("hypotheses"))
    hypothesis_ids = collect_ids(hypotheses, "hypotheses", report)
    for index, hypothesis in enumerate(hypotheses, start=1):
        if not isinstance(hypothesis, dict):
            continue
        if not hypothesis.get("statement") or not hypothesis.get("prediction"):
            add(report, "warnings", "HYPOTHESIS", f"hypotheses[{index}] should state a mechanism and testable prediction.")

    protocols = records(bundle.get("protocols"))
    protocol_ids = collect_ids(protocols, "protocols", report)
    for index, protocol in enumerate(protocols, start=1):
        if not isinstance(protocol, dict):
            continue
        label = f"protocols[{index}]"
        if str(protocol.get("hypothesis")) not in hypothesis_ids:
            add(report, "errors", "PROTOCOL_HYPOTHESIS", f"{label} references an unknown hypothesis.")
        for field in ("type", "primary_metric", "prediction", "analysis_plan"):
            if not protocol.get(field):
                add(report, "errors", "PROTOCOL_FIELD", f"{label} requires {field}.")
        if protocol.get("type") == "confirmatory":
            for field in ("preregistered_at", "controls_and_baselines", "stopping_rule"):
                if not protocol.get(field):
                    add(report, "errors", "CONFIRMATORY_PROTOCOL", f"Confirmatory {label} requires {field} before execution.")

    experiments = records(bundle.get("experiments"))
    experiment_ids = collect_ids(experiments, "experiments", report)
    for index, experiment in enumerate(experiments, start=1):
        if not isinstance(experiment, dict):
            continue
        label = f"experiments[{index}]"
        if str(experiment.get("protocol")) not in protocol_ids:
            add(report, "errors", "EXPERIMENT_PROTOCOL", f"{label} references an unknown protocol.")
        if experiment.get("status") == "completed":
            outcome = experiment.get("outcome", {})
            if not isinstance(outcome, dict) or not outcome.get("primary_metric"):
                add(report, "errors", "EXPERIMENT_OUTCOME", f"Completed {label} needs outcome.primary_metric.")
            if not records(experiment.get("sanity_checks")):
                add(report, "warnings", "SANITY_CHECK", f"Completed {label} has no recorded sanity checks.")
            if not records(experiment.get("artifacts")):
                add(report, "warnings", "ARTIFACTS", f"Completed {label} has no reproducibility artifacts.")

    evidence = records(bundle.get("evidence"))
    evidence_ids = collect_ids(evidence, "evidence", report)
    valid_targets = hypothesis_ids | experiment_ids
    for index, card in enumerate(evidence, start=1):
        if not isinstance(card, dict):
            continue
        label = f"evidence[{index}]"
        for field in ("type", "source", "claim", "limitations", "confidence"):
            if card.get(field) in (None, "", []):
                add(report, "warnings", "EVIDENCE_FIELD", f"{label} should record {field}.")
        for target in records(card.get("supports")):
            if str(target) not in valid_targets:
                add(report, "warnings", "EVIDENCE_TARGET", f"{label} supports unknown target '{target}'.")

    claims = records(bundle.get("claims"))
    claim_ids = collect_ids(claims, "claims", report)
    evidence_types = {str(card.get("id")): str(card.get("type")) for card in evidence if isinstance(card, dict)}
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            continue
        label = f"claims[{index}]"
        for field in ("text", "kind", "scope", "status", "confidence", "limitations"):
            if claim.get(field) in (None, "", []):
                add(report, "errors", "CLAIM_FIELD", f"{label} requires {field}.")
        linked = [str(x) for x in records(claim.get("evidence"))]
        if not linked:
            add(report, "errors", "CLAIM_EVIDENCE", f"{label} has no evidence links.")
        for ident in linked:
            if ident not in evidence_ids:
                add(report, "errors", "CLAIM_EVIDENCE", f"{label} references unknown evidence '{ident}'.")
        if claim.get("kind") in {"causal", "mechanistic"} and not any(evidence_types.get(ident) == "experiment" for ident in linked):
            add(report, "warnings", "CAUSAL_EVIDENCE", f"{label} is {claim.get('kind')} without linked experiment evidence.")

    report["summary"] = {
        "hypotheses": len(hypotheses),
        "protocols": len(protocols),
        "experiments": len(experiments),
        "evidence_cards": len(evidence),
        "claims": len(claims),
        "errors": len(report["errors"]),
        "warnings": len(report["warnings"]),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] or (args.strict and report["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
