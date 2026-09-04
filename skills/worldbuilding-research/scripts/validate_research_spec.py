#!/usr/bin/env python3
"""Validate a structured multi-item research specification.

This checks record completeness only. It does not establish the factual accuracy,
source quality, or methodological adequacy of the planned research.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

VALID_OBJECT_STATUSES = {"planned", "investigating", "complete", "blocked"}
VALID_EVIDENCE_TYPES = {
    "primary_source",
    "original_paper",
    "official_dataset",
    "direct_measurement",
    "credible_secondary_source",
    "other",
}
VALID_SPEC_STATUSES = {"draft", "approved", "in_progress", "complete", "paused"}


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_string(mapping: dict[str, Any], key: str, location: str, errors: list[str]) -> None:
    if not nonempty_string(mapping.get(key)):
        errors.append(f"{location}.{key} must be a non-empty string")


def require_string_list(mapping: dict[str, Any], key: str, location: str, errors: list[str]) -> None:
    value = mapping.get(key)
    if not isinstance(value, list) or not value or not all(nonempty_string(item) for item in value):
        errors.append(f"{location}.{key} must be a non-empty list of strings")


def validate_spec(document: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(document, dict):
        return ["The YAML document must be a mapping."], warnings
    spec = document.get("research_spec")
    if not isinstance(spec, dict):
        return ["research_spec must be a mapping."], warnings

    for key in ("topic", "question", "purpose"):
        require_string(spec, key, "research_spec", errors)

    scope = spec.get("scope")
    if not isinstance(scope, dict):
        errors.append("research_spec.scope must be a mapping")
    else:
        require_string_list(scope, "included", "research_spec.scope", errors)
        require_string_list(scope, "excluded", "research_spec.scope", errors)
        require_string(scope, "time_boundary", "research_spec.scope", errors)
        context = scope.get("geography_or_context")
        if context is not None and not nonempty_string(context):
            errors.append("research_spec.scope.geography_or_context must be a non-empty string or null")

    objects = spec.get("objects")
    if not isinstance(objects, list) or not objects:
        errors.append("research_spec.objects must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        for index, obj in enumerate(objects, start=1):
            location = f"research_spec.objects[{index}]"
            if not isinstance(obj, dict):
                errors.append(f"{location} must be a mapping")
                continue
            for key in ("id", "name", "rationale"):
                require_string(obj, key, location, errors)
            object_id = obj.get("id")
            if nonempty_string(object_id):
                if object_id in seen_ids:
                    errors.append(f"Duplicate object id: {object_id}")
                seen_ids.add(object_id)
            if obj.get("status") not in VALID_OBJECT_STATUSES:
                allowed = ", ".join(sorted(VALID_OBJECT_STATUSES))
                errors.append(f"{location}.status must be one of: {allowed}")

    fields = spec.get("fields")
    if not isinstance(fields, list) or not fields:
        errors.append("research_spec.fields must be a non-empty list")
    else:
        seen_names: set[str] = set()
        required_field_count = 0
        for index, field in enumerate(fields, start=1):
            location = f"research_spec.fields[{index}]"
            if not isinstance(field, dict):
                errors.append(f"{location} must be a mapping")
                continue
            for key in ("name", "description"):
                require_string(field, key, location, errors)
            name = field.get("name")
            if nonempty_string(name):
                normalized_name = name.strip().casefold()
                if normalized_name in seen_names:
                    errors.append(f"Duplicate field name: {name}")
                seen_names.add(normalized_name)
            if field.get("evidence_type") not in VALID_EVIDENCE_TYPES:
                allowed = ", ".join(sorted(VALID_EVIDENCE_TYPES))
                errors.append(f"{location}.evidence_type must be one of: {allowed}")
            if not isinstance(field.get("required"), bool):
                errors.append(f"{location}.required must be true or false")
            elif field["required"]:
                required_field_count += 1
        if required_field_count == 0:
            warnings.append("No fields are required; the final comparison may be under-specified.")

    standard = spec.get("evidence_standard")
    if not isinstance(standard, dict):
        errors.append("research_spec.evidence_standard must be a mapping")
    else:
        source_count = standard.get("minimum_sources_per_material_claim")
        if not isinstance(source_count, int) or isinstance(source_count, bool) or source_count < 1:
            errors.append("research_spec.evidence_standard.minimum_sources_per_material_claim must be an integer of at least 1")
        elif source_count == 1:
            warnings.append("Only one source is required per material claim; triangulate consequential claims where feasible.")
        preferred = standard.get("preferred_source_types")
        if not isinstance(preferred, list) or not preferred or not all(item in VALID_EVIDENCE_TYPES for item in preferred):
            errors.append("research_spec.evidence_standard.preferred_source_types must be a non-empty list of supported evidence types")
        require_string(standard, "source_cutoff", "research_spec.evidence_standard", errors)

    require_string_list(spec, "completion_criteria", "research_spec", errors)

    checkpoint = spec.get("human_checkpoint")
    if not isinstance(checkpoint, dict):
        errors.append("research_spec.human_checkpoint must be a mapping")
    else:
        require_string_list(checkpoint, "required_before", "research_spec.human_checkpoint", errors)
        require_string(checkpoint, "approver", "research_spec.human_checkpoint", errors)

    if spec.get("status") not in VALID_SPEC_STATUSES:
        allowed = ", ".join(sorted(VALID_SPEC_STATUSES))
        errors.append(f"research_spec.status must be one of: {allowed}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a structured research specification YAML file.")
    parser.add_argument("spec_path", type=Path, help="Path to research-spec.yaml")
    args = parser.parse_args()

    try:
        with args.spec_path.open("r", encoding="utf-8") as handle:
            document = yaml.safe_load(handle)
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.spec_path}", file=sys.stderr)
        return 2
    except yaml.YAMLError as exc:
        print(f"ERROR: Invalid YAML: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_spec(document)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    print(f"Validation summary: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
