---
name: research-loop
description: >-
  Run a reusable research cycle across disciplines: source-grounded literature reading,
  hypothesis discovery, bounded experiments or analyses, persistent evidence memory,
  independent critique, and manuscript development. Includes baseline-centered module
  transfer and cumulative model experiments. Use for a research agent, ongoing research
  program, or resuming a study; also supports 科研智能体、围绕基线读论文、模块融合与替换.
license: Apache-2.0
---

# Research Loop

Produce a research decision backed by inspectable evidence, then leave enough state for another session to continue. Adapt to the field, available tools, and the user's current request. This is an agent workflow with local helpers; running the skill does not create a background scheduler.

## Start or resume

1. Use the user's chosen project directory. If it already contains `.research`, read `project.json` and `STATE.md` before relevant records. Otherwise establish the objective, constraints, available evidence, and meaningful next step; initialize with `scripts/init_project.py` when persistent work is desired. Resolve scripts relative to this skill, never a guessed working directory.
2. Keep the domain, hardware, data locations, budgets, and local capabilities in the project. Do not assume a GPU, an ML benchmark, a specific model provider, an installed integration, or an institutional subscription.
3. Inherit the user's existing authorization. Distinguish planning from executing an experiment and preparing a submission from submitting it. Unknown capabilities or credentials are execution dependencies; continue useful independent work while resolving them.
4. Load only the references needed for the task:
   - [Cycle and decision gates](references/cycle.md): selecting or advancing work.
   - [Memory and records](references/memory.md): saving, retrieving, or validating evidence.
   - [Independent review](references/review.md): evaluating plans, results, or manuscripts.
   - [Scientific writing](references/writing.md): drafting or revising prose.
   - [Optional integrations](references/integrations.md): invoking ARIS, nature-skills, or writing skills.
   - [Baseline-centered module transfer](references/model-grafting.md): reading papers to improve a chosen model, locating insertion/replacement points, and accumulating experimentally supported changes.

## When the user wants to build on a chosen model

Use the baseline-centered mode when the user asks to read other papers for modules that can be introduced into a particular model, or to accumulate several improvements before writing. Read [model-grafting.md](references/model-grafting.md). Keep the original reproduced baseline and the current best variant in persistent memory. Every new detailed paper reading must end with a concrete transfer decision against that model, including the exact placement or the missing evidence needed to choose it.

For this mode, default to a configurable target of **2–3 retained module additions or replacements**. Initialize its records with `scripts/init_model_search.py --path PROJECT --baseline NAME`. This is an architecture search objective, not proof of novelty or a reason to keep a harmful module. Advance from measured improvements under a stable selection protocol, retain the variant lineage, and develop the final narrative after combination and ablation evidence are available. Other research modes do not inherit this module-count target.

On resumption, read `.research/model-search/search.json` and its `STATE.md` when present, then the relevant baseline, candidates and variants. Continue the next authorized, budgeted action; do not restart generic idea generation or require the user to approve each routine candidate already inside that scope.

## Core cycle

**Read → synthesize → propose → design → execute/analyze → review → write → remember.** Enter at the stage supported by the available evidence. Do not require a complete library before a useful experiment, or invent experiment results to reach the writing stage.

- Ground important statements in original documents, data, code, or observed results. Record the exact locator and whether a statement is an author report, an observation, an interpretation, or a hypothesis. Search snippets and abstracts can identify leads; they do not establish unseen methods, figures, or results.
- Read in batches, then compare mechanisms, assumptions, information requirements, evidence, and failure conditions across papers. Maintain version and identity links. A file count is not a count of distinct papers read.
- Permit both problem-first research and exploratory recombination. A combination with unexplained gains can justify a probe. Write the expected observation, simple alternatives, cost, and decision rule before expanding it. Literature absence within one collection is not evidence of worldwide novelty.
- Separate exploration from confirmation. In computational work, preserve the information boundary between selection and evaluation. In other fields, define the equivalent independent samples, measurements, controls, or proofs. Adapt replication and uncertainty assessment to the actual design.
- Before execution, inspect the environment and running work, measure or estimate cost, and set a bounded plan. Tool availability alone does not reserve a machine or authorize spending. Prefer the experiment most able to distinguish competing explanations within the budget.
- A process finishing is an execution fact. A result being checked is an evidence decision. A contribution being persuasive requires scientific judgment. Keep these separate in records and reports.
- Independent critique uses access to primary artifacts and a neutral task brief. Report whether review used an independent context, a different model, or a human; agreement among agents is not empirical confirmation.
- Preserve failed attempts and conclusion-changing contradictions. Record useful lessons as conditions, operations, expected observations, and failure boundaries. Strengthen, narrow, or retire a lesson when evidence changes; do not turn one improvement into a universal rule.
- Write around the strongest supported contribution with clear scope and concrete evidence. Remove empty hedging and formulaic prose without changing the claims, comparisons, numerical results, or necessary uncertainty.

## Durable completion

At a meaningful checkpoint, save:

1. The decision: continue, revise, park, retire, or prepare a manuscript.
2. Its evidence and unresolved competing explanations.
3. The resources actually used and artifacts produced, when applicable.
4. The next executable step and any dependency.

Update `.research/STATE.md` and relevant records. Run `scripts/validate_project.py --path PROJECT` after structural changes to records. The validator checks declared structure and file references; it does not verify scientific truth, full-text comprehension, novelty, or publication quality.

If interrupted, resume from the earliest unsupported decision, not merely the last successful command. A recurring host automation may invoke this skill later, but only report a schedule as active after that automation exists and is verified.
