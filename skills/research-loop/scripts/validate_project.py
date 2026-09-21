#!/usr/bin/env python3
"""Check research memory structure and local evidence references, not scientific truth."""

from __future__ import annotations

import argparse
import json
import os
import stat
from pathlib import Path, PureWindowsPath
from typing import Any

STAGES = {"intake", "read", "synthesize", "ideate", "design", "execute", "review", "write", "archive"}
DEPTHS = {"metadata", "abstract", "partial", "full_text"}


def safe_path(path: Path) -> Path:
    """Normalize an explicit CLI target, then reject symlink/junction components."""
    path = Path(os.path.abspath(path))
    for component in [*reversed(path.parents), path]:
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"symlink or reparse point is not permitted: {component}")
    return path


def local_file(root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a nonempty workspace-relative file path")
    portable = value.replace("\\", "/")
    parts = portable.split("/")
    if Path(portable).is_absolute() or PureWindowsPath(value).drive or any(p in {"", ".", ".."} or ":" in p for p in parts):
        raise ValueError("file reference must stay inside the workspace")
    result = safe_path(root.joinpath(*parts))
    if not result.is_file() or result.stat().st_size == 0:
        raise ValueError(f"referenced file is missing, empty, or not regular: {value}")
    return result


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def decode(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)


def validate_project(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = safe_path(path)
        workspace = safe_path(root / ".research")
        if not workspace.is_dir():
            raise ValueError(".research directory is missing")
    except (OSError, ValueError) as exc:
        return [str(exc)]

    def error(label: str, message: str) -> None:
        errors.append(f"{label}: {message}")

    def text_field(record: dict[str, Any], field: str, label: str) -> bool:
        value = record.get(field)
        valid = isinstance(value, str) and bool(value.strip())
        if not valid:
            error(label, f"{field} must be a nonempty string")
        return valid

    def enum(record: dict[str, Any], field: str, choices: set[str], label: str, default: str | None = None) -> None:
        value = record.get(field, default)
        if not isinstance(value, str) or value not in choices:
            error(label, f"{field} must be one of {', '.join(sorted(choices))}")

    def strings(record: dict[str, Any], field: str, label: str) -> list[str]:
        values = record.get(field, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            error(label, f"{field} must be a list of nonempty strings")
            return []
        if len(set(values)) != len(values):
            error(label, f"{field} contains duplicate entries")
        return values

    def read(file: Path, lines: bool = False) -> list[dict[str, Any]]:
        try:
            safe_path(file)
            content = file.read_text(encoding="utf-8")
        except (OSError, ValueError, UnicodeError) as exc:
            error(str(file.relative_to(root)), str(exc))
            return []
        records: list[dict[str, Any]] = []
        for number, raw in enumerate(content.splitlines() if lines else [content], 1):
            if lines and not raw.strip():
                continue
            label = f"{file.relative_to(root)}:{number}"
            try:
                record = decode(raw)
                if not isinstance(record, dict):
                    raise ValueError("expected a JSON object")
                records.append(record)
            except (ValueError, RecursionError) as exc:
                error(label, str(exc))
        return records

    config = read(workspace / "project.json")
    if config:
        project = config[0]
        if type(project.get("schema_version")) is not int or project["schema_version"] != 1:
            error("project.json", "schema_version must be integer 1")
        for field in ("domain", "objective"):
            text_field(project, field, "project.json")
        enum(project, "stage", STAGES, "project.json")
        for field in ("resource_budget", "local_capabilities"):
            if field not in project or (project[field] is not None and not isinstance(project[field], dict)):
                error("project.json", f"{field} must be null or an object")
    try:
        local_file(root, ".research/STATE.md")
    except (OSError, ValueError) as exc:
        error("STATE.md", str(exc))

    data = {name: read(workspace / "memory" / f"{name}.jsonl", lines=True) for name in ("papers", "claims", "lessons")}
    experiments = workspace / "experiments"
    data["experiments"] = []
    try:
        safe_path(experiments)
        if not experiments.is_dir():
            raise ValueError("experiments directory is missing")
        for file in sorted(experiments.glob("*.json")):
            data["experiments"].extend(read(file))
    except (OSError, ValueError) as exc:
        error("experiments", str(exc))

    index: dict[str, dict[str, dict[str, Any]]] = {}
    owners: dict[str, str] = {}
    for name, records in data.items():
        index[name] = {}
        for position, record in enumerate(records, 1):
            label = f"{name}[{position}]"
            if text_field(record, "id", label):
                record_id = record["id"]
                if record_id in owners:
                    error(label, f"duplicate id {record_id!r}; already in {owners[record_id]}")
                else:
                    owners[record_id] = name
                index[name][record_id] = record

    for paper in data["papers"]:
        label = f"paper {paper.get('id', '?')}"
        for field in ("title", "source"):
            text_field(paper, field, label)
        enum(paper, "reading_depth", DEPTHS, label)
        anchors = strings(paper, "source_anchors", label)
        if paper.get("reading_depth") == "full_text" and not anchors:
            error(label, "full_text requires source_anchors")
        if "card_ref" in paper or paper.get("reading_depth") == "full_text":
            try:
                local_file(root, paper.get("card_ref"))
            except (OSError, ValueError) as exc:
                error(label, f"card_ref: {exc}")

    for experiment in data["experiments"]:
        label = f"experiment {experiment.get('id', '?')}"
        enum(experiment, "execution_status", {"planned", "running", "completed", "failed", "cancelled"}, label)
        enum(experiment, "evidence_status", {"unvalidated", "validated"}, label)
        if "protocol" not in experiment or not isinstance(experiment["protocol"], str):
            error(label, "protocol must be a string")
        artifacts = strings(experiment, "artifacts", label)
        if experiment.get("evidence_status") == "validated":
            if experiment.get("execution_status") != "completed":
                error(label, "validated evidence requires execution_status completed")
            text_field(experiment, "protocol", label)
            if not artifacts:
                error(label, "validated evidence requires actual artifacts")
        if experiment.get("execution_status") == "completed" or experiment.get("evidence_status") == "validated":
            for artifact in artifacts:
                try:
                    local_file(root, artifact)
                except (OSError, ValueError) as exc:
                    error(label, str(exc))

    def evidence(record: dict[str, Any], label: str, supporting: bool, required: bool) -> set[str]:
        refs = record.get("evidence")
        types: set[str] = set()
        if not isinstance(refs, list):
            error(label, "evidence must be a list")
            return types
        if required and not refs:
            error(label, "requires evidence references")
        for ref in refs:
            if not isinstance(ref, dict):
                error(label, "each evidence reference must be an object")
                continue
            kind, record_id = ref.get("type"), ref.get("id")
            if not isinstance(kind, str) or kind not in {"paper", "experiment"} or not isinstance(record_id, str):
                error(label, "evidence requires type paper/experiment and string id")
                continue
            target = index[f"{kind}s"].get(record_id)
            if target is None:
                error(label, f"missing {kind} evidence reference: {record_id}")
                continue
            types.add(kind)
            if not text_field(ref, "locator", label):
                continue
            locations = target.get("source_anchors" if kind == "paper" else "artifacts", [])
            if not isinstance(locations, list) or ref["locator"] not in locations:
                error(label, f"locator is not registered on {record_id}")
            if supporting and kind == "paper" and target.get("reading_depth") not in ("partial", "full_text"):
                error(label, f"supporting paper {record_id} requires partial or full_text reading")
            if supporting and kind == "experiment" and target.get("evidence_status") != "validated":
                error(label, f"supporting experiment {record_id} requires validated evidence; completed alone is insufficient")
        return types

    for claim in data["claims"]:
        label = f"claim {claim.get('id', '?')}"
        text_field(claim, "text", label)
        enum(claim, "status", {"hypothesis", "supported", "contested", "rejected"}, label)
        enum(claim, "kind", {"literature", "empirical", "interpretation"}, label, "interpretation")
        supported = claim.get("status") == "supported"
        types = evidence(claim, label, supported, supported)
        if supported and claim.get("kind") == "empirical" and "experiment" not in types:
            error(label, "supported empirical claim requires a validated experiment")

    for lesson in data["lessons"]:
        label = f"lesson {lesson.get('id', '?')}"
        for field in ("lesson", "conditions"):
            text_field(lesson, field, label)
        enum(lesson, "evidence_strength", {"candidate", "observed", "validated"}, label, "candidate")
        strength = lesson.get("evidence_strength", "candidate")
        evidence(lesson, label, strength == "validated", strength != "candidate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True, help="Research project directory")
    args = parser.parse_args()
    errors = validate_project(args.path)
    for issue in errors:
        print(f"ERROR: {issue}")
    if errors:
        return 1
    print("Structure and local references are valid. This does not certify scientific truth or grant execution permission.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
