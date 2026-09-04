#!/usr/bin/env python3
"""Validate a Storycraft OS world bundle (JSON or YAML) and inspect change impact.

Usage:
    python validate_world_bundle.py path/to/world.yaml [--strict]
    python validate_world_bundle.py path/to/world.yaml --impact fac-001

Validation checks structural traceability, declared references, and selected
semantic states. It does not judge creative quality, real-world accuracy,
genre fit, or authorial intent.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

WORLD_STATUS = {"draft", "active", "frozen", "retired"}
ENTITY_STATUS = {"approved", "provisional", "disputed", "deprecated"}
EVENT_STATUS = {"proposed", "approved", "disputed", "superseded"}
RULE_STATUS = {"approved", "provisional", "deprecated"}
RULE_STRENGTH = {"invariant", "default", "local-custom", "disputed"}
CLAIM_CONFIDENCE = {"confirmed", "plausible", "speculative", "unknown"}
CHANGE_STATUS = {"proposed", "approved", "applied", "reverted"}
CHANGE_ACTION = {"add", "modify", "deprecate", "redirect", "split", "merge"}


def add(report: dict[str, list[dict[str, str]]], level: str, code: str, message: str) -> None:
    report[level].append({"code": code, "message": message})


def rows(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def load_bundle(path: Path, fmt: str) -> Any:
    text = path.read_text(encoding="utf-8")
    resolved = "yaml" if fmt == "auto" and path.suffix.lower() in {".yaml", ".yml"} else fmt
    if resolved == "auto":
        resolved = "json"
    if resolved == "yaml":
        if yaml is None:
            raise RuntimeError("PyYAML is unavailable. Install pyyaml or validate a JSON bundle.")
        return yaml.safe_load(text)
    return json.loads(text)


def collect_ids(records: list[Any], section: str, report: dict[str, list[dict[str, str]]]) -> set[str]:
    identifiers: list[str] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict) or not record.get("id"):
            add(report, "errors", "ID", f"{section}[{index}] requires an id.")
            continue
        identifiers.append(str(record["id"]))
    for ident, count in Counter(identifiers).items():
        if count > 1:
            add(report, "errors", "DUPLICATE_ID", f"{section} has duplicate id '{ident}'.")
    return set(identifiers)


def check_enum(value: Any, allowed: set[str], label: str, report: dict[str, list[dict[str, str]]], required: bool = True) -> None:
    if value is None or value == "":
        if required:
            add(report, "errors", "ENUM_MISSING", f"{label} is required.")
        return
    if str(value) not in allowed:
        add(report, "errors", "ENUM", f"{label} value '{value}' is not allowed.")


def register_reference(index: dict[str, list[dict[str, str]]], target: Any, owner: str, field: str) -> None:
    if target is not None and str(target):
        index.setdefault(str(target), []).append({"owner": owner, "field": field})


def check_refs(values: list[Any], valid: set[str], label: str, report: dict[str, list[dict[str, str]]], index: dict[str, list[dict[str, str]]]) -> None:
    for value in values:
        register_reference(index, value, label, "list")
        if str(value) not in valid:
            add(report, "warnings", "REFERENCE", f"{label} references unknown id '{value}'.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON or YAML Storycraft OS world bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as a failing result.")
    parser.add_argument("--format", choices=["auto", "json", "yaml"], default="auto")
    parser.add_argument("--impact", metavar="ID", help="Report direct references to a canonical id.")
    args = parser.parse_args()

    report: dict[str, list[dict[str, str]]] = {"errors": [], "warnings": []}
    try:
        bundle = load_bundle(args.bundle, args.format)
    except FileNotFoundError:
        print(json.dumps({"errors": [{"code": "FILE", "message": "World bundle was not found."}]}))
        return 2
    except json.JSONDecodeError as exc:
        print(json.dumps({"errors": [{"code": "JSON", "message": str(exc)}]}))
        return 2
    except RuntimeError as exc:
        print(json.dumps({"errors": [{"code": "YAML_UNAVAILABLE", "message": str(exc)}]}))
        return 2
    except Exception as exc:
        if yaml is not None and isinstance(exc, yaml.YAMLError):
            print(json.dumps({"errors": [{"code": "YAML", "message": str(exc)}]}))
            return 2
        raise

    if not isinstance(bundle, dict):
        add(report, "errors", "ROOT", "The world bundle must be an object.")
        print(json.dumps(report, indent=2))
        return 1

    ref_index: dict[str, list[dict[str, str]]] = {}
    world = bundle.get("world", {})
    if not isinstance(world, dict):
        add(report, "errors", "WORLD", "world must be an object.")
        world = {}
    for field in ("id", "version", "design_promise"):
        if not world.get(field):
            add(report, "errors", "WORLD_FIELD", f"world requires {field}.")
    check_enum(world.get("status"), WORLD_STATUS, "world.status", report, required=False)
    if not bundle.get("schema_version"):
        add(report, "warnings", "SCHEMA_VERSION", "Bundle should record schema_version (for example, '0.3').")

    entities = rows(bundle.get("entities"))
    entity_ids = collect_ids(entities, "entities", report)
    name_owners: dict[str, list[str]] = {}
    for index, entity in enumerate(entities, start=1):
        if not isinstance(entity, dict):
            continue
        label = f"entities[{index}]"
        for field in ("type", "name", "status"):
            if not entity.get(field):
                add(report, "errors", "ENTITY_FIELD", f"{label} requires {field}.")
        check_enum(entity.get("status"), ENTITY_STATUS, f"{label}.status", report)
        name = str(entity.get("name", "")).casefold()
        if name:
            name_owners.setdefault(name, []).append(str(entity.get("id", label)))
        for alias in rows(entity.get("aliases")):
            alias_key = str(alias).casefold()
            if alias_key:
                name_owners.setdefault(alias_key, []).append(str(entity.get("id", label)))
        check_refs(rows(entity.get("dependencies")), entity_ids, f"{label}.dependencies", report, ref_index)
        for relation in rows(entity.get("relationships")):
            if not isinstance(relation, dict):
                add(report, "warnings", "RELATIONSHIP", f"{label} contains a non-object relationship.")
                continue
            target = relation.get("target")
            register_reference(ref_index, target, label, "relationships.target")
            if target and str(target) not in entity_ids:
                add(report, "warnings", "RELATIONSHIP", f"{label} targets unknown entity '{target}'.")
    for name, owners in name_owners.items():
        unique = sorted(set(owners))
        if len(unique) > 1:
            add(report, "warnings", "NAME_COLLISION", f"Name or alias '{name}' is shared by {', '.join(unique)}.")

    systems = rows(bundle.get("systems"))
    system_ids = collect_ids(systems, "systems", report)
    for index, system in enumerate(systems, start=1):
        if not isinstance(system, dict):
            continue
        label = f"systems[{index}]"
        for field in ("domain", "statement"):
            if not system.get(field):
                add(report, "errors", "SYSTEM_FIELD", f"{label} requires {field}.")
        if not rows(system.get("inputs")) and not rows(system.get("constraints")):
            add(report, "warnings", "SYSTEM_INTERFACE", f"{label} should record inputs or constraints.")
        check_refs(rows(system.get("linked_entities")), entity_ids, f"{label}.linked_entities", report, ref_index)

    decisions = rows(bundle.get("decisions"))
    decision_ids = collect_ids(decisions, "decisions", report)
    events = rows(bundle.get("events"))
    event_ids = collect_ids(events, "events", report)
    known_core = entity_ids | system_ids | decision_ids | event_ids
    for index, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            continue
        label = f"events[{index}]"
        for field in ("name", "event", "status"):
            if not event.get(field):
                add(report, "errors", "EVENT_FIELD", f"{label} requires {field}.")
        check_enum(event.get("status"), EVENT_STATUS, f"{label}.status", report)
        if not event.get("date_or_sequence"):
            add(report, "warnings", "EVENT_TIME", f"{label} should record date_or_sequence.")
        check_refs(rows(event.get("affected_entities")), entity_ids, f"{label}.affected_entities", report, ref_index)
        check_refs(rows(event.get("causes")), known_core, f"{label}.causes", report, ref_index)
    for index, decision in enumerate(decisions, start=1):
        if not isinstance(decision, dict):
            continue
        label = f"decisions[{index}]"
        for field in ("question", "status"):
            if not decision.get(field):
                add(report, "warnings", "DECISION_FIELD", f"{label} should record {field}.")
        check_enum(decision.get("status"), ENTITY_STATUS | {"superseded"}, f"{label}.status", report, required=False)
        check_refs(rows(decision.get("affected_ids")), known_core, f"{label}.affected_ids", report, ref_index)

    rules = rows(bundle.get("rules"))
    rule_ids = collect_ids(rules, "rules", report)
    for index, rule in enumerate(rules, start=1):
        if not isinstance(rule, dict):
            continue
        label = f"rules[{index}]"
        for field in ("layer", "statement", "strength", "status"):
            if not rule.get(field):
                add(report, "errors", "RULE_FIELD", f"{label} requires {field}.")
        check_enum(rule.get("strength"), RULE_STRENGTH, f"{label}.strength", report)
        check_enum(rule.get("status"), RULE_STATUS, f"{label}.status", report)
        register_reference(ref_index, rule.get("supersedes"), label, "supersedes")
        if rule.get("supersedes") and str(rule["supersedes"]) not in rule_ids:
            add(report, "warnings", "RULE_SUPERSEDES", f"{label} supersedes unknown rule '{rule['supersedes']}'.")

    locations = rows(bundle.get("locations"))
    location_ids = collect_ids(locations, "locations", report)
    for index, location in enumerate(locations, start=1):
        if not isinstance(location, dict):
            continue
        label = f"locations[{index}]"
        for field in ("type", "name", "status"):
            if not location.get(field):
                add(report, "errors", "LOCATION_FIELD", f"{label} requires {field}.")
        parent = location.get("parent")
        register_reference(ref_index, parent, label, "parent")
        if parent and str(parent) not in location_ids:
            add(report, "warnings", "LOCATION_PARENT", f"{label} parent '{parent}' is not a location id.")
        if parent and str(parent) == str(location.get("id")):
            add(report, "errors", "LOCATION_SELF_PARENT", f"{label} cannot be its own parent.")
        check_refs(rows(location.get("controlling_entities")), entity_ids, f"{label}.controlling_entities", report, ref_index)

    connections = rows(bundle.get("connections"))
    collect_ids(connections, "connections", report)
    for index, connection in enumerate(connections, start=1):
        if not isinstance(connection, dict):
            continue
        label = f"connections[{index}]"
        for field in ("from", "to", "mode", "availability"):
            if not connection.get(field):
                add(report, "errors", "CONNECTION_FIELD", f"{label} requires {field}.")
        for field in ("from", "to"):
            target = connection.get(field)
            register_reference(ref_index, target, label, field)
            if target and str(target) not in location_ids:
                add(report, "warnings", "CONNECTION_LOCATION", f"{label}.{field} references unknown location '{target}'.")
        if connection.get("from") and str(connection.get("from")) == str(connection.get("to")):
            add(report, "warnings", "CONNECTION_LOOP", f"{label} begins and ends at the same location.")
        check_refs(rows(connection.get("rules")), rule_ids, f"{label}.rules", report, ref_index)

    sources = rows(bundle.get("sources"))
    source_ids = collect_ids(sources, "sources", report)
    claims = rows(bundle.get("claims"))
    collect_ids(claims, "claims", report)
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            continue
        label = f"claims[{index}]"
        for field in ("statement", "status", "confidence"):
            if not claim.get(field):
                add(report, "warnings", "CLAIM_FIELD", f"{label} should record {field}.")
        check_enum(claim.get("confidence"), CLAIM_CONFIDENCE, f"{label}.confidence", report, required=False)
        check_refs(rows(claim.get("support")), source_ids, f"{label}.support", report, ref_index)
        check_refs(rows(claim.get("affected_ids")), known_core | rule_ids | location_ids, f"{label}.affected_ids", report, ref_index)

    knowledge = rows(bundle.get("knowledge_ledger"))
    collect_ids(knowledge, "knowledge_ledger", report)
    for index, item in enumerate(knowledge, start=1):
        if not isinstance(item, dict):
            continue
        label = f"knowledge_ledger[{index}]"
        for field in ("proposition", "truth_status", "public_status"):
            if not item.get(field):
                add(report, "warnings", "KNOWLEDGE_FIELD", f"{label} should record {field}.")
        check_refs(rows(item.get("holders")), entity_ids, f"{label}.holders", report, ref_index)

    consequences = rows(bundle.get("consequence_ledger"))
    consequence_ids = collect_ids(consequences, "consequence_ledger", report)
    for index, consequence in enumerate(consequences, start=1):
        if not isinstance(consequence, dict):
            continue
        label = f"consequence_ledger[{index}]"
        for field in ("origin", "scale", "current_state", "next_surface"):
            if not consequence.get(field):
                add(report, "errors", "CONSEQUENCE_FIELD", f"{label} requires {field}.")
        origin = consequence.get("origin")
        register_reference(ref_index, origin, label, "origin")
        if origin and str(origin) not in event_ids | decision_ids:
            add(report, "warnings", "CONSEQUENCE_ORIGIN", f"{label} origin '{origin}' is not an event or decision id.")
        check_refs(rows(consequence.get("affected")), entity_ids, f"{label}.affected", report, ref_index)

    state = bundle.get("session_state")
    if state is not None and not isinstance(state, dict):
        add(report, "errors", "SESSION_STATE", "session_state must be an object when supplied.")
    if isinstance(state, dict):
        for field in ("date_or_sequence", "pause_point"):
            if not state.get(field):
                add(report, "warnings", "SESSION_FIELD", f"session_state should record {field}.")
        check_refs(rows(state.get("active_entities")), entity_ids, "session_state.active_entities", report, ref_index)
        check_refs(rows(state.get("consequence_ids")), consequence_ids, "session_state.consequence_ids", report, ref_index)
        uses = rows(world.get("uses"))
        if any(str(use) in {"interactive-fiction", "campaign", "simulation"} for use in uses) and "player_choice_boundary" not in state:
            add(report, "warnings", "CHOICE_BOUNDARY", "Interactive/campaign state should record player_choice_boundary, even when null.")

    transitions = rows(bundle.get("state_transitions"))
    collect_ids(transitions, "state_transitions", report)
    for index, transition in enumerate(transitions, start=1):
        if not isinstance(transition, dict):
            continue
        label = f"state_transitions[{index}]"
        for field in ("from_state", "next_state", "state_delta", "canon_status"):
            if not transition.get(field):
                add(report, "errors", "TRANSITION_FIELD", f"{label} requires {field}.")
        if isinstance(transition.get("resolution_basis"), dict):
            check_refs(rows(transition["resolution_basis"].get("rules")), rule_ids, f"{label}.resolution_basis.rules", report, ref_index)
        delta = transition.get("state_delta")
        if isinstance(delta, dict):
            check_refs(rows(delta.get("entities_changed")), entity_ids, f"{label}.state_delta.entities_changed", report, ref_index)
            check_refs(rows(delta.get("systems_changed")), system_ids, f"{label}.state_delta.systems_changed", report, ref_index)
            check_refs(rows(delta.get("consequences_created")), consequence_ids, f"{label}.state_delta.consequences_created", report, ref_index)
            check_refs(rows(delta.get("consequences_resolved")), consequence_ids, f"{label}.state_delta.consequences_resolved", report, ref_index)

    changes = rows(bundle.get("change_sets"))
    collect_ids(changes, "change_sets", report)
    for index, change_set in enumerate(changes, start=1):
        if not isinstance(change_set, dict):
            continue
        label = f"change_sets[{index}]"
        for field in ("from_version", "to_version", "status"):
            if not change_set.get(field):
                add(report, "errors", "CHANGE_SET_FIELD", f"{label} requires {field}.")
        check_enum(change_set.get("status"), CHANGE_STATUS, f"{label}.status", report)
        for change_index, change in enumerate(rows(change_set.get("changes")), start=1):
            if not isinstance(change, dict):
                add(report, "warnings", "CHANGE", f"{label}.changes[{change_index}] is not an object.")
                continue
            action = change.get("action")
            check_enum(action, CHANGE_ACTION, f"{label}.changes[{change_index}].action", report)
            target = change.get("target_id")
            register_reference(ref_index, target, f"{label}.changes[{change_index}]", "target_id")
            if target and str(target) not in known_core | rule_ids | location_ids | consequence_ids:
                add(report, "warnings", "CHANGE_TARGET", f"{label}.changes[{change_index}] targets unknown id '{target}'.")
            check_refs(rows(change.get("replacement_ids")), known_core | rule_ids | location_ids | consequence_ids, f"{label}.changes[{change_index}].replacement_ids", report, ref_index)

    all_ids = known_core | rule_ids | location_ids | source_ids | consequence_ids
    report["summary"] = {
        "entities": len(entities),
        "systems": len(systems),
        "events": len(events),
        "rules": len(rules),
        "locations": len(locations),
        "sources": len(sources),
        "claims": len(claims),
        "transitions": len(transitions),
        "change_sets": len(changes),
        "consequences": len(consequences),
        "errors": len(report["errors"]),
        "warnings": len(report["warnings"]),
    }
    if args.impact:
        report["impact"] = {
            "id": args.impact,
            "known": args.impact in all_ids,
            "direct_references": ref_index.get(args.impact, []),
            "reference_count": len(ref_index.get(args.impact, [])),
            "note": "Direct declared references only; inspect semantic dependencies before approving a canon migration.",
        }
        if args.impact not in all_ids:
            add(report, "warnings", "IMPACT_UNKNOWN", f"Impact id '{args.impact}' is not a declared canonical id.")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] or (args.strict and report["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
