#!/usr/bin/env python3
"""Copy this repository's standalone research-loop skill to an explicit skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import tempfile
from pathlib import Path


def safe_path(path: Path) -> Path:
    path = Path(os.path.abspath(path))
    for component in [*reversed(path.parents), path]:
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"symlink or reparse point is not permitted: {component}")
    return path


def install(destination: Path, source: Path | None = None) -> Path:
    source = safe_path(source if source is not None else Path(__file__).absolute().parents[1] / "skills" / "research-loop")
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise ValueError("source skill must contain SKILL.md")
    for file in source.rglob("*"):
        safe_path(file)
        if not file.is_file() and not file.is_dir():
            raise ValueError(f"unsupported source file: {file}")
    parent = safe_path(destination)
    target = safe_path(parent / "research-loop")
    if target.exists():
        raise FileExistsError("research-loop is already installed; refusing to replace it")
    if parent == source or source in parent.parents:
        raise ValueError("installation destination cannot be inside source skill")
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".research-loop-install-", dir=parent))
    staged = staging / "research-loop"
    try:
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        safe_path(target)
        if target.exists():
            raise FileExistsError("research-loop appeared during installation; refusing replacement")
        staged.rename(target)
    finally:
        if safe_path(staging).parent != parent:
            raise ValueError("refusing to clean staging outside the skills directory")
        shutil.rmtree(staging)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="Explicit destination skills directory")
    args = parser.parse_args()
    try:
        target = install(args.dest)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    print(f"Installed research-loop at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
