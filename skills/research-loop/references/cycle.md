# Cycle and decision gates

This workflow supports computational, theoretical, observational, and experimental research. Choose controls and evidence standards appropriate to the study. Numerical batch sizes, review counts, and resource allocations are project choices, not universal requirements.

## Research contract

Record the question or exploratory objective, target audience, available data and instruments, legitimate information access, budget, time constraints, and desired artifact. "Find a strong contribution" is a valid starting objective: narrow it to a tractable problem family using available evidence. Revisit that choice at an agreed checkpoint.

For recurring work, keep a small active portfolio and a queue. Allocate resources by evidence and expected learning value. Stop increasing parallelism when it prevents careful interpretation or comparable experiments.

| Stage | Concrete output | Decision to advance |
|---|---|---|
| intake | Objective, source inventory, constraints, capability map | A useful next step is executable |
| read | Anchored paper records and source-depth labels | Central method and evidence can be inspected |
| synthesize | Comparison across assumptions, mechanisms, information and outcomes | A question, contradiction or transferable mechanism is identified |
| ideate | Candidate hypotheses, nearest prior work, alternatives | A candidate has a discriminating test or analysis |
| design | Protocol, controls, primary observations, budget and stop rule | The experiment can answer the stated question fairly |
| execute | Actual logs, inputs, versions, raw results and failures | Artifacts exist and execution status is known |
| review | Artifact checks, competing explanations and independent critique | The claim is supported, narrowed, contested or rejected |
| write | Claim–evidence outline, figures/tables, prose and references | The contribution and scope match the evidence |
| archive | Decision, reusable lessons and next-step state | Another session can resume accurately |

## Reading a large collection

When a baseline model is selected for incremental improvement, use [model-grafting.md](model-grafting.md). Each detailed reading should end with a transfer or skip decision against the current model, and promising candidates feed its persistent experiment queue.

Index all relevant sources, then calibrate a small representative batch before increasing throughput. Each detailed record should explain the research question, central method or mechanism, assumptions, crucial comparisons, author-stated results, evidence locators, and what remains uncertain. Review the actual figures, equations and supplementary material when they carry the claim.

After each useful batch, synthesize across papers. Compare how similarly named methods actually work and how differently named methods may share a mechanism. Preserve contradictory results and protocol differences. Store reusable ingredients with their prerequisites, not just model or module names.

Depth is explicit: metadata, abstract, partial, or full_text. Code inspection and reproduction are separate achievements. Source extraction success alone is not deep reading. When parsing or access fails, retain the strongest available scope and mark missing evidence.

## Candidate design

Both routes are allowed:

- **Observed problem → explanation → intervention.** Start with a stable failure, a measurement discrepancy, an unmet capability or an unresolved prediction.
- **Recombination → observation → explanation.** Try a justified combination, changed representation, transferred mechanism, or analysis to discover an informative phenomenon.

Each candidate records its source evidence, concrete modification, conditions, simple alternatives, testable prediction, nearest work, implementation/measurement dependencies, and initial budget. An unexplained signal may advance to a diagnostic experiment; it is not yet a mechanism claim.

For novelty assessment, search the same problem, the same mechanism, adjacent terminology, backward references and recent forward citations where available. Save the search date and scope. Report the nearest work and a concrete difference, with uncertainty about incomplete coverage. Never convert a model's confidence score into a publication probability.

## Experiments and analysis

1. Define a small probe that can distinguish important alternatives. Reuse validated inputs or cached artifacts only when their provenance and compatibility are known.
2. Preserve information access, data selection, observation conditions and comparison budgets. Include a simple baseline or alternative explanation before adding complexity.
3. Record primary outcomes, selection rules, a practically meaningful effect, uncertainty assessment and stop conditions before confirmation. Amendments after observing data remain visible and motivate new confirmation.
4. Capture actual configuration, code/instrument version, data/sample identity, randomness or replication scheme, logs and output artifacts. Preserve engineering failure separately from a hypothesis contradicted by evidence.
5. Inspect raw artifacts before promoting a result to validated. Repeatedly checking an evaluation set turns it into development evidence; renaming it does not restore independence.
6. Expand only when the probe supports a useful next question. Budget exhaustion can yield inconclusive, without proving a method ineffective.

For wet-lab or instrument-dependent work, the skill may prepare protocols and analyze authorized measurements. It does not substitute an agent-generated number for a measurement or imply that physical execution occurred.

## Review, promotion and stopping

Use the decision that fits the evidence: continue, narrow the claim, change the experiment, investigate a new phenomenon, or retire the candidate. If a predeclared sequence of informative tests defeats the central explanation, archive that explanation rather than repeatedly changing metrics to preserve it.

Promote a lesson from candidate to observed only with traceable evidence, and to validated only within the inspected scope. Scientific generalization may require additional replication even when the local record passes structural validation.

Promote a project toward a manuscript when its question matters, the contribution is distinct from nearest work, the central evidence is reliable, and the scope is defensible. Organize the paper by the argument that survived investigation. Preserve the complete research record separately.
