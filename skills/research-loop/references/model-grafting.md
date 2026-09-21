# Read papers to improve a chosen model

Use this mode for requests such as: "Start from model X, read other papers, identify modules worth importing, choose where they fit, test them, keep improvements, and assemble a model with two or three changes before writing."

The persistent object is the evolving model. Paper reading supplies candidate interventions; experiments select versions; the final paper explains the supported contribution. Do not substitute a generic literature summary for a placement decision. Do not require a finished story before trying a plausible combination.

## 1. Establish the original baseline and current best version

Initialize the main research project first, then run:

```bash
python PATH_TO_SKILL/scripts/init_model_search.py --path PROJECT --baseline "chosen model" --target-modules 2 3
```

This only scaffolds records. Fill them by inspecting the actual paper, pinned repository revision, configuration and execution. A named baseline has not automatically been read or reproduced.

In `.research/model-search/baseline.md`, map the model as a directed dataflow. For each meaningful block record:

- Paper section/equation and repository revision, file, class/function and call site.
- Input/output meaning, observed tensor shapes, token or spatial ordering, normalization and dtype.
- Trainable/frozen parameters, gradient routes, supervision and train/inference dependencies.
- What follows this block and which existing block a replacement would remove.

Useful slots may include input processing, visual feature extraction, text representation, feature interaction, objective, or output scoring. These are inspection prompts, not a claim that every model contains them. A conceptual slot without code access remains `placement_unverified`.

Keep **B0**, the original baseline, immutable. Record its actual reproduction protocol, artifacts, metrics and discrepancy from the paper. Also track the **incumbent**, the current best eligible variant under the agreed selection rule. Until B0 runs successfully, do source analysis and implementation preparation without claiming any improvement.

For FB-CLIP specifically, [fb-clip-example.md](fb-clip-example.md) gives pinned, inspected code boundaries and source/target protocol notes. It is an orientation example, not a completed baseline reproduction. Other models require their own source inspection.

## 2. End each detailed reading with a transfer card

Load the current architecture, remaining weaknesses, existing modules and failed attempts before analyzing a new paper. Compare against both B0 and the incumbent: a mechanism useful for B0 may already be covered by an accepted module.

Record one or more candidate cards, or an explicit skip with a reason. Each candidate contains:

| Field | Required decision |
|---|---|
| Source | Paper ID, inspected section/equation, source code revision if available; reading scope |
| Transferable operation | What computation or learning constraint is borrowed; distinguish it from the donor's entire model |
| Expected benefit | Which observed weakness it could affect and why; an exploratory rationale is sufficient for a probe |
| Placement | Target variant; file/function and dataflow edge; add before/after or replace exactly which block |
| Interface adaptation | Input/output shape and semantics, projections/resizing, token correspondence, gradient and normalization changes |
| Compatibility | Required labels, support data, auxiliary models, training, inference cost and licenses; overlap/conflict with current modules |
| Minimal implementation | Isolated change, feature flag, configuration and dependency preparation |
| Experiment | Parent comparison, primary metric and direction, development data, useful effect threshold, budget and rollback rule |
| Decision | Queue, implement, defer pending evidence, or skip with a concrete reason |

When placement is ambiguous, compare at most a small budgeted set of plausible positions and record what each tests. Do not invent an exact function name or tensor dimension from the abstract. Inspect code or trace the forward pass before execution. A reasonable answer can be "replace block S after verifying its feature ordering," with that verification as the next action.

Maintain a queue ranked by expected useful information, compatibility, complementarity with the incumbent and implementation cost. Similarity of module names is insufficient. Revisit deferred candidates when the architecture or evidence changes; retrieve failed attempts before retrying one.

## 3. Define how an improvement will be selected

Configure `selection_protocol` before using results to promote a variant: dataset/version and data access, development split or development domains, preprocessing, metric aggregation and direction, comparison budget, randomness/repeats, meaningful effect rule, cost constraints and confirmation evidence. Record the original baseline and parent results under the same protocol.

Respect the task's information setting. A target-labeled module cannot silently become part of a zero-shot comparison. Either adapt it to permitted information or record a separate task setting. Repeatedly inspected public test results are development evidence; preserve a genuinely independent confirmation set or domain when possible and state when it is unavailable. Replicating an exact deterministic computation is not an independent repeat; choose appropriate uncertainty or robustness checks instead.

Budget allocation and execution scope belong to the project, not this generic skill. Within an already authorized scope, perform the next bounded implementation and experiment without repeatedly asking for approval. If execution dependencies are missing, leave an executable plan and continue useful reading/code work. Installing the skill alone does not run jobs or create a schedule.

## 4. Implement, compare, retain, then continue

The usual path is:

```text
B0 -> B0 + A -> B0 + A + B -> B0 + A + B + C
```

Here A/B/C are retained interventions. `+` may represent replacing an existing block, not only appending a layer. A variant may also revise or remove an earlier change. Keep the graph explicit.

For each step:

1. Pin the parent code/configuration and record the proposed module operation. Use a distinct variant configuration and independent output directory. Keep B0 runnable and avoid overwriting the incumbent checkpoint.
2. Implement one intervention behind a switch or equivalent isolated configuration. Check the forward path, shapes, losses, gradient reachability and resource use as relevant. With the change disabled, recover the parent behavior within appropriate tolerance.
3. Run a small comparison with the parent under the selection protocol. Save actual raw results and experiment IDs. Separate implementation failure from a completed experiment that did not support improvement.
4. Check artifacts and decision criteria. A promising screening result may receive a larger confirmation budget; it is not yet a retained best version. Promote only after the configured retention checks pass, and preserve the prior incumbent.
5. Record retain, reject, revise, or inconclusive, with the exact evidence and updated active module set. If retained, use this new incumbent for subsequent paper-to-module mapping. If rejected, keep the incumbent and move to another candidate or a clearly motivated revision.

The search need not be strictly greedy. If two individually weak candidates have a concrete complementarity hypothesis, allocate a bounded pair test against B0 and their single-module versions. Record that reason before running it. Do not combine arbitrary failures indefinitely or silently change the primary metric to retain a candidate.

Always report both **incremental gain over the parent** and **cumulative gain over B0**, including cost and relevant regressions. A module may help alone but hurt the incumbent; that outcome must change the decision.

## 5. Count the final architecture, not the history of edits

`target_module_count` defaults to `[2, 3]` in this mode and can be changed by the user. Count identifiable retained additions or replacements relative to B0. Each has a distinct operation, placement, provenance and experimental rationale.

- Replacing the same block twice leaves one retained replacement at that slot.
- Renaming a module, splitting one operation into wrappers, or adjusting a hyperparameter does not create an additional module.
- Existing baseline modules are not newly introduced contributions.
- A borrowed operation remains attributed to its source; combining several borrowed modules does not by itself establish novelty.

Keep searching toward the requested count within budget. If only one intervention survives, preserve it and report the target as unmet. Do not force in a harmful second module to satisfy a counter. Reaching the count triggers combination validation and paper development, not an automatic success or acceptance claim.

## 6. Validate the combination, then build the story

For two retained modules A/B, compare B0, A alone, B alone and A+B. For three, aim for all eight subsets when affordable; otherwise include B0, the incremental path and leave-one-out variants, and identify untested interactions. Keep the selected architecture and settings fixed for final confirmation. Confirm meaningful gains across the relevant seeds, domains, categories or independent measurements, with appropriate uncertainty and comparable training/inference budgets.

After this evidence is available, construct:

1. The concrete limitation exposed by the baseline results.
2. A unifying design idea explaining how the retained changes address it.
3. Each module's distinct role, supported by ablations or diagnostics.
4. The demonstrated benefits, costs and conditions, compared with the nearest work.

It is acceptable that the explanatory idea emerged after exploration. Keep that history in research records. Test predictions that would distinguish the explanation from alternatives before making a mechanism claim. If evidence only establishes performance, frame the contribution at that level. Do not invent a shared mechanism or three novelty claims merely because three modules survived. Then use [writing.md](writing.md) to write a focused, direct manuscript.

## Persistent records and resumption

```text
.research/model-search/
  baseline.md       # source-grounded architecture and original reproduction
  search.json       # chosen baseline, incumbent, target count, selection protocol
  candidates.jsonl  # donor -> target placement -> decision -> experiment references
  variants.jsonl    # immutable baseline and subsequent configurations/lineage
  STATE.md          # current decision, evidence, next bounded action
```

The initializer creates empty or explicitly unverified records. Enrich a candidate with a stable ID, `source_paper_id`, `target_variant`, `operation`, `placement`, `interface`, `rationale`, `status` and `experiment_ids`. Enrich variants with stable IDs, parent IDs, retained module IDs, code/configuration references, protocol ID, experiment IDs, metrics, costs and decision. Preserve revisions/history rather than erasing failed attempts. Link papers and runs to the main `.research/memory` and `.research/experiments` records.

Update the main project `STATE.md` to point to this active search. At a checkpoint, save the incumbent, retained count, running jobs, next candidate and next executable action. On resume, verify actual job status and artifacts before resubmitting work. Resume this search instead of producing another disconnected list of ideas.

`validate_project.py` checks the core project records; it does not validate these flexible model-search ledgers or certify a module-count/retention decision. The agent must reconcile module membership, lineage, protocol and experiment references when updating them.

In user-facing updates, use a compact table: donor paper → proposed operation → insertion/replacement site → current evidence → decision. Show what changed in the model and why the next experiment is useful.
