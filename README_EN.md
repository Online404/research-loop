# Research Loop

**Turn each research cycle into inspectable evidence, reusable lessons, and a concrete next step.**

Research Loop is a general-purpose agent skill connecting literature reading, cross-paper synthesis, hypothesis discovery, bounded experiments or analyses, independent critique, research memory, and manuscript development. The project supplies its own discipline, resources, tools, and constraints.

[中文](README.md) · [Skill](skills/research-loop/SKILL.md) · [Module transfer](skills/research-loop/references/model-grafting.md) · [Provenance](docs/PROVENANCE.md) · [Record format](skills/research-loop/references/memory.md)

## Read around a baseline and improve it incrementally

Select a baseline such as FB-CLIP and map its actual paper-to-code architecture. Every subsequent detailed paper reading ends with a decision: which operation can transfer, where it belongs in the current model, what interface adaptations it needs, and which experiment will decide whether to retain it.

```text
B0 -> transfer A -> compare and retain V1
V1 -> transfer or replace B -> compare and retain V2
V2 -> optional C -> combination checks and ablations -> manuscript argument
```

Track both gains over the parent and cumulative gains over B0. Keep the original baseline runnable, preserve the best eligible variant when an experiment fails, and retrieve prior failures before proposing another change. A candidate that helps B0 may conflict with the current model.

This mode defaults to **2–3 retained module additions or replacements**, configurable by the user. Replacing the same block twice counts as one retained change. The count is a search target; it does not establish novelty or justify retaining a harmful change. Develop the final narrative from combination and ablation evidence. The architecture map, transfer cards, queue and variant lineage persist across sessions. See [model-grafting.md](skills/research-loop/references/model-grafting.md).

## What it integrates

- **ARIS:** budgeted iteration, independent review, resumable work, and checking results before promoting claims.
- **nature-skills:** source anchors, method-to-evidence reasoning, isolated reviewer contexts, and evidence-led scientific artifacts.
- **Academic anti-defensive writing:** a clear contribution and an argument organized around its strongest evidence.
- **Direct prose practices:** concrete language with scientifically meaningful uncertainty preserved.

This is an original implementation with optional integrations. Upstream skill packages are not redistributed. Reviewed revisions and deliberate differences are listed in [PROVENANCE](docs/PROVENANCE.md); attribution appears in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).

## Install

Python helpers require Python 3.10+ and use only its standard library.

```bash
git clone https://github.com/Online404/research-loop.git
cd research-loop
python scripts/install.py --dest /your/agent/skills
```

The destination is the parent skills directory. The installer copies only `skills/research-loop`, refuses an existing destination, and does not download dependencies. Manual copying of that complete folder is also supported. Follow the host's current documentation for its discovery location. In Codex, invoke `$research-loop` once the skill is discovered; other hosts can load `SKILL.md` directly.

## Initialize and resume

```bash
python skills/research-loop/scripts/init_project.py --path ../my-study --domain "your field" --objective "the question or capability to investigate"
python skills/research-loop/scripts/validate_project.py --path ../my-study
```

Initialization creates `.research/project.json`, `STATE.md`, three memory ledgers, and an experiments directory. It does not launch an experiment or access credentials. Existing workspaces are preserved by refusing initialization over them.

For incremental model development, initialize its additional records:

```bash
python skills/research-loop/scripts/init_model_search.py --path ../my-study --baseline "FB-CLIP" --target-modules 2 3
```

This creates `.research/model-search/` with explicitly unread/unreproduced baseline placeholders. It does not download or train the named model. Ask the agent:

> Use research-loop with FB-CLIP as the baseline. Map its paper-to-code architecture and reproduce it. For each new paper, identify transferable modules and exact insertion or replacement sites. Run bounded comparisons in the configured environment, retain verified improvements and continue from the best variant. Aim for 2–3 retained changes, validate their combination and ablations, then build the paper's argument. Persist candidates, failures and the next action.

Ask your agent:

> Use research-loop in my project. Inspect existing sources and results, propose three testable candidates, identify the closest prior work and the cheapest discriminating experiment, and update research memory.

Or constrain the scope:

> Read and synthesize only. Separate source-supported statements from hypotheses, and do not execute experiments this round.

## Evidence and memory

Reading depth is explicit: metadata, abstract, partial, or full text. Reproduction is recorded separately. Claims reference source locations or experiment artifacts. A completed process, an inspected result, and a convincing scientific conclusion are different milestones.

Both problem-first inquiry and exploratory recombination are supported. After discovering an effect, formulate and independently test its explanation. Preserve failed attempts and material contradictions. Lessons describe conditions and evidence, and can be revised or retired.

The validator checks structure, record references, and artifact existence. It does not certify scientific truth, novelty, full-text comprehension, or publication quality. See [memory.md](skills/research-loop/references/memory.md).

## Execution requirements

The host provides source access, parsing, analysis tools, execution environments and any independent reviewers. Optional specialist integrations are described in [integrations.md](skills/research-loop/references/integrations.md). Recurring execution requires an actual host scheduler; installing this skill does not start a background service. Publication acceptance and AI-detector outcomes are not guaranteed.

Keep generated research projects outside this source repository, or retain `.research/` in ignore rules. Publish only material you intend to release.

## Develop

```bash
python -m unittest discover -s tests -v
```

Contribute reproducible workflow improvements and synthetic or openly licensed examples. See [CONTRIBUTING](CONTRIBUTING.md).

Original material is licensed under [Apache-2.0](LICENSE). Optional upstream projects retain their own licenses.
