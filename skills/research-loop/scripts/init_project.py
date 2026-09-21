#!/usr/bin/env python3
"""Initialize empty, local research memory without running research or granting permissions."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from validate_project import safe_path, validate_project


def init_project(path: Path, domain: str, objective: str) -> Path:
    if not isinstance(domain, str) or not domain.strip() or not isinstance(objective, str) or not objective.strip():
        raise ValueError("domain and objective must be nonempty text")
    root = safe_path(path)
    target = safe_path(root / ".research")
    if target.exists():
        raise FileExistsError(".research already exists; refusing to replace existing research memory")
    if root.exists() and not root.is_dir():
        raise ValueError("project path must be a directory")
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".research-init-", dir=root))
    staged = staging / ".research"
    try:
        (staged / "memory").mkdir(parents=True)
        (staged / "experiments").mkdir()
        project = {
            "schema_version": 1,
            "domain": domain.strip(),
            "objective": objective.strip(),
            "stage": "intake",
            "resource_budget": None,
            "local_capabilities": None,
        }
        (staged / "project.json").write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staged / "STATE.md").write_text(
            "# Research state\n\nStage: intake\n\n"
            "No literature has been read, experiments executed, or evidence validated by initialization.\n\n"
            "Next: establish the research question, available sources, and authorized resource budget.\n",
            encoding="utf-8",
        )
        for name in ("papers", "claims", "lessons"):
            (staged / "memory" / f"{name}.jsonl").write_text("", encoding="utf-8")
        errors = validate_project(staging)
        if errors:
            raise ValueError("initialization validation failed: " + "; ".join(errors))
        safe_path(target)
        if target.exists():
            raise FileExistsError(".research appeared during initialization; refusing replacement")
        staged.rename(target)
    finally:
        if safe_path(staging).parent != root:
            raise ValueError("refusing to clean staging outside the project directory")
        shutil.rmtree(staging)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--objective", required=True)
    args = parser.parse_args()
    try:
        target = init_project(args.path, args.domain, args.objective)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    print(f"Initialized empty research memory at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
