#!/usr/bin/env python3
"""Initialize a baseline-centered module search without reading papers or running models."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Sequence

from validate_project import decode, safe_path


def init_model_search(path: Path, baseline: str, target_modules: Sequence[int] = (2, 3)) -> Path:
    """Add empty model-search memory to an existing version-1 research project."""
    if not isinstance(baseline, str) or not baseline.strip() or "\n" in baseline or "\r" in baseline:
        raise ValueError("baseline must be a nonempty, single-line name")
    if (
        len(target_modules) != 2
        or any(type(value) is not int or value < 1 for value in target_modules)
        or target_modules[0] > target_modules[1]
    ):
        raise ValueError("target modules must be two positive integers MIN MAX with MIN <= MAX")
    baseline = baseline.strip()
    root = safe_path(path)
    workspace = safe_path(root / ".research")
    if not workspace.is_dir():
        raise ValueError("existing .research workspace required; initialize the research project first")
    project_file = safe_path(workspace / "project.json")
    if not project_file.is_file():
        raise ValueError("existing .research/project.json required")
    project = decode(project_file.read_text(encoding="utf-8"))
    if not isinstance(project, dict) or type(project.get("schema_version")) is not int or project["schema_version"] != 1:
        raise ValueError("existing project.json must have schema_version 1")
    target = safe_path(workspace / "model-search")
    if target.exists():
        raise FileExistsError("model-search already exists; refusing to replace search memory")

    baseline_record = {
        "id": "B0",
        "parent_id": None,
        "baseline_name": baseline,
        "modules": [],
        "module_count": 0,
        "reading_status": "unread",
        "execution_status": "planned",
        "evidence_status": "unvalidated",
        "results": None,
        "experiment_ids": [],
        "code_ref": None,
        "decision": "baseline_pending",
    }
    search = {
        "schema_version": 1,
        "baseline_id": "B0",
        "current_incumbent": "B0",
        "target_module_count": list(target_modules),
        "selection_protocol": None,
        "next_action": "Read the baseline paper and code, map module interfaces, then configure the selection protocol and reproduce B0 within the authorized budget.",
    }
    baseline_template = f"""# Baseline B0

Baseline name: {baseline}

Paper reading: unread. Reproduction: not_started. Evidence: unvalidated. Results: none.
This is an empty planning template. Initialization has not read a paper, inspected code, run an experiment, or verified any outcome.

## Source and architecture

- Paper ID and source anchors: unset
- Architecture and existing module roles: unset
- Original inputs, outputs, objectives, and training/inference flow: unset
- Original paper's reported results and protocol (attribution only): unset

## Code identity

- Repository and immutable revision: unset
- Entry points, environment, configuration, and checkpoint identity: unset
- Files and functions that implement each module: unset

## Tensor interfaces

| Module or boundary | File/function | Input shape, dtype, semantics | Output shape, dtype, semantics | Training/inference constraints |
| --- | --- | --- | --- | --- |
| To be mapped | unset | unset | unset | unset |

## Freeze and replacement plan

- Reference code/configuration snapshot: unset
- Parameters/components intended to remain fixed: unset
- Parameters/components that may be trained, added, or replaced: unset
- Dependencies and compatibility requirements: unset
- Freeze status: not_configured; no component has been inspected or frozen by initialization.

## Reproduction and selection protocol

- Dataset/version, split identities, and selection versus held-out evaluation data: unset
- Seeds, preprocessing, metrics, aggregation, and baseline comparison: unset
- Authorized resource budget and stopping conditions: unset
- Run IDs and actual output artifact paths: none
- Local reproduction results: none
- Reproduction discrepancies and decision: pending

B0 is the designated starting model, not an experimentally established winner. Record real results before promoting a variant. Count introduced or replaced modules relative to B0; unchanged baseline components do not count. The target module count is a search preference, not evidence of novelty or publication readiness.
"""
    state_template = f"""# Model search state

Baseline: {baseline} (B0)
Current incumbent: B0, pending reproduction; no measured winner exists.
Target introduced/replaced module count relative to B0: {target_modules[0]} to {target_modules[1]}.

## Current evidence

- Baseline paper reading: unread
- Baseline reproduction: not_started
- Candidate papers/modules read or tested in this search: none
- Experiments executed by initialization: none
- Results: none
- Validated evidence: none
- Selection protocol: not_configured

## Resume from here

1. Read baseline sources and code; fill baseline.md with source anchors and tensor interfaces.
2. Configure selection data, comparison rules, resource budget, and stopping criteria before trials.
3. Reproduce B0 and record actual runs in the project's experiment ledger.
4. Read one candidate paper at a time; record its transferable module and smallest justified test.
5. Compare a variant with the current incumbent using the same selection protocol. Record retain, reject, or inconclusive decisions with evidence; only then update search.json.

## Latest decision

- Candidate and donor-paper ID: unset
- Parent variant and proposed addition/replacement: unset
- Hypothesis and expected interface/cost changes: unset
- Experiment IDs and evidence artifacts: none
- Observed result and uncertainty: none
- Decision and rationale: pending
- Next action: establish and reproduce B0.

Keep this state, candidates.jsonl, variants.jsonl, and search.json consistent after each decision. Initialization does not alter the parent project's STATE.md or authorize execution.
"""
    staging = Path(tempfile.mkdtemp(prefix=".model-search-init-", dir=workspace))
    staged = staging / "model-search"
    try:
        staged.mkdir()
        (staged / "baseline.md").write_text(baseline_template, encoding="utf-8")
        (staged / "candidates.jsonl").write_text("", encoding="utf-8")
        (staged / "variants.jsonl").write_text(json.dumps(baseline_record, ensure_ascii=False) + "\n", encoding="utf-8")
        (staged / "search.json").write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staged / "STATE.md").write_text(state_template, encoding="utf-8")
        safe_path(target)
        if target.exists():
            raise FileExistsError("model-search appeared during initialization; refusing replacement")
        staged.rename(target)
    finally:
        if safe_path(staging).parent != workspace:
            raise ValueError("refusing to clean staging outside the research workspace")
        shutil.rmtree(staging)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True, help="Existing research project directory")
    parser.add_argument("--baseline", required=True, help="Name of the fixed starting model")
    parser.add_argument("--target-modules", type=int, nargs=2, default=(2, 3), metavar=("MIN", "MAX"), help="Preferred added/replaced module-count range relative to B0 (default: 2 3)")
    args = parser.parse_args()
    try:
        target = init_model_search(args.path, args.baseline, args.target_modules)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    print(f"Initialized pending model search at {target}; no papers read or experiments run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
