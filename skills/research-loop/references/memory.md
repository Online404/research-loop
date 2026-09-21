# Project memory and record contract

The bundled tools create and validate file-backed records. They never read a paper for you, run an experiment, or promote a result to scientifically valid. Author reports, local observations, interpretations and hypotheses remain distinct in the record text and provenance.

## Workspace

All helpers take `--path PROJECT`; their private state lives in `PROJECT/.research`. File references inside records are relative to **PROJECT**, so a card inside the workspace is `.research/cards/P001.md`. Keep generated state separate from the public skill source.

```text
.research/
  project.json
  STATE.md
  memory/papers.jsonl
  memory/claims.jsonl
  memory/lessons.jsonl
  experiments/E001.json
  cards/                  # create when reading
  results/                # create when actual evidence exists
```

JSONL means one complete JSON object per line. IDs must be unique across all four record types. Use UTF-8. Unknown extra fields may hold domain-specific details. Duplicate JSON keys and non-finite numbers are rejected. Portable artifact references cannot escape the project or traverse symlinks.

## Project and state

The initializer writes:

```json
{
  "schema_version": 1,
  "domain": "your discipline",
  "objective": "your research objective",
  "stage": "intake",
  "resource_budget": null,
  "local_capabilities": null
}
```

Stages: intake, read, synthesize, ideate, design, execute, review, write, archive. Budget and capabilities are null until established, then objects with project-specific units and constraints. Empty ledgers are valid before work begins. Record permissions from the actual user context; do not interpret missing configuration as additional authorization.

`STATE.md` describes the current decision, evidence pointers, unresolved questions, next action and dependencies. Update it at meaningful checkpoints. Preserve decision history in the related artifacts rather than silently rewriting conclusions.

## Papers

Required: `id`, `title`, `source`, `reading_depth`.

- `reading_depth`: metadata, abstract, partial, full_text.
- `source`: a stable URI or source identifier. Add DOI, version, local file and retrieval date when known.
- `source_anchors`: exact nonempty locator strings used by evidence references.
- `card_ref`: a real, nonempty project-relative file path.
- `full_text` requires both anchors and a card. Declaring these is only a structural prerequisite: the agent still has to read the evidence and inspect the relevant method, figures and results.

Synthetic format example, not an actual citation:

```json
{"id":"P001","title":"Example source (synthetic)","source":"https://example.org/paper","reading_depth":"partial","source_anchors":["section:Methods/paragraph:2"]}
```

An abstract record can carry abstract locators but cannot serve as supporting evidence for a claim marked supported by this validator. Review the needed original passage and upgrade only its actual reading scope. Reproduction is a separate experiment record, not a reading-depth label.

## Experiments or analyses

One JSON file per record under `.research/experiments/`. Required: `id`, `execution_status`, `evidence_status`, `protocol`.

```json
{
  "id": "E001",
  "execution_status": "planned",
  "evidence_status": "unvalidated",
  "protocol": "A bounded comparison or measurement plan",
  "artifacts": []
}
```

Execution status: planned, running, completed, failed, cancelled. Evidence status: unvalidated or validated. Every declared artifact on a completed record must already exist as a nonempty file inside the project, even before evidence validation. Planned records may name future artifacts. A validated record additionally requires completed execution, a nonempty protocol, and a nonempty artifact list.

The agent sets validated only after inspecting provenance, execution and outputs. The validator does not make this decision. Preserve the scientific outcome separately, for example `outcome: inconclusive` or `outcome: contradicted`; successful execution can have either outcome.

Add domain-appropriate inputs/sample identifiers, code or instrument version, conditions, controls, information access, randomness, repetitions, uncertainty, selection rules, cost, timestamps, logs and raw results. An artifact path can refer to measurements or a proof/analysis record; GPU training is not assumed.

## Claims and evidence

Required: `id`, `text`, `status`, `evidence`.

- Status: hypothesis, supported, contested, rejected.
- Optional kind: literature, empirical, interpretation (default).
- Each evidence reference has `type: paper|experiment`, `id`, and `locator`.
- A paper locator must exactly match an entry in that paper's `source_anchors`.
- An experiment locator must exactly match an entry in its `artifacts`.
- A supported claim requires evidence; supporting papers must be partial/full_text and supporting experiments must be validated. A supported empirical claim must include a validated experiment.

Synthetic format example:

```json
{"id":"C001","kind":"literature","text":"The example source reports a specified method, within the inspected passage.","status":"supported","evidence":[{"type":"paper","id":"P001","locator":"section:Methods/paragraph:2"}]}
```

A supported literature attribution does not establish that its result was reproduced locally or that a proposed extension works. Specify conditions and uncertainty in the claim; keep explanations as hypotheses until their actual evidence warrants promotion. Use extra detail fields for a figure, subresult or competing explanation when useful.

## Lessons

Required: `id`, `lesson`, `conditions`, `evidence`. Optional `evidence_strength`: candidate (default), observed, validated.

Candidate lessons may have an empty evidence list. Observed lessons require real referenced records. Validated lessons require supporting evidence under the same structural rules as supported claims. All evidence references use the claim format above.

Preserve the triggering condition, operation, expected observation, failure boundary and counterevidence. "Validated" describes the inspected local scope; it is not a universal scientific guarantee. Add replication scope or a superseding record as knowledge changes.

## Retrieval and validation

Start from the active question, then retrieve related papers, claims, experiments and failed attempts. Keyword search over these small ledgers is a valid starting point; a database or semantic index can be added when retrieval needs justify it. Always retain original records and evidence anchors.

Run:

```bash
python PATH_TO_SKILL/scripts/validate_project.py --path PROJECT
```

It checks declared structure, references, paths and the basic completed/validated distinction. It does not check numerical correctness, statistical adequacy, source authenticity, novelty, or whether prose conceals a material contradiction. Those remain research and review tasks.
