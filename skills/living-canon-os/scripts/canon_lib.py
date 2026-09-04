#!/usr/bin/env python3
"""Shared file, record, and transaction helpers for Living Canon OS utilities."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*\.[a-z0-9][a-z0-9-]*(?:-[0-9]+)?$")
DATA_SUFFIXES = {".yaml", ".yml", ".json"}
IGNORED_PARTS = {".git", "__pycache__", ".venv", "node_modules", ".canon"}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "update"


def load_data(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle) if path.suffix.lower() == ".json" else yaml.safe_load(handle)


def dump_data(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        else:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True, width=100)


def iter_data_files(bundle: Path) -> list[Path]:
    return sorted(
        path for path in bundle.rglob("*")
        if path.is_file() and path.suffix.lower() in DATA_SUFFIXES
        and not any(part in IGNORED_PARTS for part in path.parts)
    )


def load_records(bundle: Path) -> list[tuple[Path, int | None, dict[str, Any]]]:
    """Return one entry per record. List-backed records retain their list index."""
    records: list[tuple[Path, int | None, dict[str, Any]]] = []
    for path in iter_data_files(bundle):
        try:
            data = load_data(path)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict):
            records.append((path, None, data))
        elif isinstance(data, list):
            for index, record in enumerate(data):
                if isinstance(record, dict):
                    records.append((path, index, record))
    return records


def record_index(bundle: Path) -> dict[str, tuple[Path, int | None, dict[str, Any]]]:
    result: dict[str, tuple[Path, int | None, dict[str, Any]]] = {}
    for path, index, record in load_records(bundle):
        record_id = record.get("id")
        if isinstance(record_id, str):
            result[record_id] = (path, index, record)
    return result


def get_manifest(bundle: Path) -> dict[str, Any]:
    manifests = [record for _, _, record in load_records(bundle) if record.get("kind") == "manifest"]
    if len(manifests) != 1:
        raise ValueError("Bundle must contain exactly one manifest record.")
    return manifests[0]


def target_path_for_new_record(bundle: Path, record: dict[str, Any]) -> Path:
    kind = str(record.get("kind") or "records")
    record_id = str(record.get("id") or "new-record")
    directory_names = {
        "entity": "entities",
        "consequence": "consequences",
        "analysis": "analyses",
    }
    folder = bundle / "registry" / directory_names.get(kind, f"{kind}s")
    return folder / f"{slugify(record_id.replace('.', '-'))}.yaml"


def write_record_at(path: Path, index: int | None, record: dict[str, Any]) -> None:
    if index is None:
        dump_data(path, record)
        return
    data = load_data(path)
    if not isinstance(data, list) or index >= len(data):
        raise ValueError(f"Record location is no longer valid: {path}")
    data[index] = record
    dump_data(path, data)


def get_path_value(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return copy.deepcopy(current)


def set_path_value(data: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current: dict[str, Any] = data
    for key in parts[:-1]:
        next_value = current.get(key)
        if not isinstance(next_value, dict):
            next_value = {}
            current[key] = next_value
        current = next_value
    if value is None:
        current.pop(parts[-1], None)
    else:
        current[parts[-1]] = copy.deepcopy(value)


def make_transaction_id(title: str) -> str:
    return f"transaction.{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{slugify(title)[:32]}"


def transaction_dir(bundle: Path) -> Path:
    path = bundle / "transactions"
    path.mkdir(parents=True, exist_ok=True)
    return path


def session_delta_path(bundle: Path, transaction_id: str) -> Path:
    path = bundle / "state" / "session-deltas"
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{transaction_id.replace('.', '-')}.md"


def record_fingerprint(record: dict[str, Any]) -> str:
    """Hash canonical content while excluding mutable transaction metadata."""
    canonical = copy.deepcopy(record)
    for key in ("last_transaction", "last_transaction_fingerprint", "updated_at"):
        canonical.pop(key, None)
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
