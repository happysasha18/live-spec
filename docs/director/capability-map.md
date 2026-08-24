# Capability map — what the Director needs, where it lives today, where it goes

This is the migration manifest for the Director rebuild. One row per capability the
mandate asks the finished system to have. Each row answers three questions: which file
holds the capability today, whether that file *runs* the capability or only *describes*
it in prose a model may or may not follow, and which package moves it to its target home.

It is a manifest, not a control system. Nothing reads this file at runtime. It exists so
that a later agent can tell a real gap from a gap that only looks real because the
capability was written down somewhere unexpected.

Read the verdict column strictly:

- **runs** — a deterministic program performs it. Deleting the prose around it changes
  nothing about whether it happens.
- **prose** — it happens only because a model read an instruction and complied. No code
  observes whether it happened.
- **mixed** — a model decides, then a program checks the shape of what the model produced.
- **absent** — no file in the tree holds it.

## Understanding what the human said

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 1 | Recognise the speech act — question, idea, observation, decision, correction, instruction, cancellation | nowhere; nearest relative is the "name the door aloud" rule, `skills/build-pipeline/SKILL.md:96-180`, which classifies *what to build* and never asks *what the human did* | absent | `skills/director/SKILL.md` | 1 |
| 2 | Decline to create work from a question, a musing, or a remark | `skills/build-pipeline/references/request-kind-table.md` rows for research/question and sketch | prose | `skills/director/SKILL.md` | 1 |
| 3 | Separate an idea from an instruction | same table, `inbox wish` row versus the product-behaviour row | prose | `skills/director/SKILL.md` | 1 |
| 4 | Split one turn carrying several speech acts without fragmenting one goal into several tickets | absent | absent | `skills/director/SKILL.md` | 1 |
| 5 | Bind a correction to the work already running instead of opening a duplicate | the re-door rule, `skills/build-pipeline/SKILL.md:129-136`, which reclassifies work but does not connect a new utterance to an existing row | prose | `skills/director/SKILL.md` | 1 |
| 6 | Hold uncommitted ideas apart from accepted commitments | `ROADMAP.md` is one flat table; `deferred` and `far` statuses stand in for a shelf, and a row gets a task id at the moment it is written down | mixed — row shape is linted, the distinction is not | shelf section in `ROADMAP.md`, rule in `docs/roadmap-format.md` | 1 shadow, 3 write |
| 7 | Say plainly which of the four things happened — answered, remembered, changed the running work, took new work | `skills/communicator/SKILL.md` report rules | prose | `skills/director/SKILL.md` names it; communicator words it | 1 |

## Routing the work that was accepted

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 8 | Name every affected dimension at once — value, journey, architecture, quality, analytics, docs, release | `skills/build-pipeline/references/work-kind-table.md` (`product · infra · skill · prose`) and the footprint scale (`presentation-only · single-module · cross-cutting`) — mutually exclusive classes, so a cross-cutting feature must pick one | prose | `skills/director/SKILL.md` | 1 |
| 9 | Write the working plan — goal, observable outcome, affected surfaces, knowns, unknowns, risks, irreversible steps, specialists, dependencies, evidence, documents that must change | absent as a unit; pieces are scattered through the intake line and the step sections of `build-pipeline` | absent | decision sheet in `skills/director/SKILL.md`; persisted in the active checkpoint | 1 |
| 10 | Assemble a specialist graph that differs per task | `skills/build-pipeline/SKILL.md:305-596` — one fixed chain, whose steps vary in *form* by work-kind but never in *membership* | prose | `skills/director/SKILL.md` | 1 shadow, 3 real |
| 11 | Rebuild the remaining graph when a new fact arrives | absent | absent | `skills/director/SKILL.md` | 3 |

## Reading only what is needed

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 12 | Compact entry point — project card, active work, indices, nothing else | absent. Today the boot chain is `~/.claude/CLAUDE.md` → `live-spec-base/SKILL.md` (53 KB) → `build-pipeline/SKILL.md` (56 KB) before the first action | absent | project card at `.live-spec/agent.md`, which exists but only declares that the tree is a host | 2 |
| 13 | Addressable reading of a canonical document | `PRODUCT_SPEC.index.md` and `TEST_MATRIX.index.md`, both rebuilt from the body and gated on push by `guardrails/check-index-generated.py` and `check-matrix-reference.py` | runs — for two documents out of thirteen | same mechanism extended to `ARCHITECTURE.md` (107 KB), then the rest | 2 |
| 14 | Reader-worker returns pointers, not pasted text | `skills/build-pipeline/references/delegation-protocol.md` | prose | `skills/director/SKILL.md` | 1 |
| 15 | Assemble a logical view from prefix, requested parts and suffix so old consumers still see one document | absent | absent | reader in `scripts/` | 2 |

## The specialists

All ten exist as skills and none needs to move. What changes is who calls them: today the
pipeline calls a fixed sequence, and the Director will call the ones a given task needs.

| # | Specialist | Lives in | Verdict | Note |
|---|---|---|---|---|
| 16 | Researcher | absent — no skill covers external or project fact-finding | absent | added in package 4 alongside analytics |
| 17 | Product analyst / spec author | `skills/spec-author/SKILL.md` (20 KB, 9 references) | prose | strongest prose in the tree; no mechanical support at all |
| 18 | Product prover | `skills/product-prover-pack/SKILL.md` (7 KB) binding the external `product-prover` skill | mixed | record gated by `guardrails/check-prover-record.sh` |
| 19 | Analyst of data and experiments | absent | absent | package 4 |
| 20 | Design reviewer | `skills/design-reviewer/SKILL.md` (28 KB) | prose | advisory by construction; nothing calls it |
| 21 | Architect | `skills/architect/SKILL.md` (new) | mixed | kept in-repo as its own skill, mirroring `test-author`; the document it produces is checked at the edges by `guardrails/check-architecture-reference.py`, writing it is model judgment |
| 22 | Test author | `skills/test-author/SKILL.md` (19 KB) | mixed | matrix is really built and really checked |
| 23 | Developer | absent as a skill; it is the agent itself | — | correct as is |
| 24 | Independent verifier | `skills/build-pipeline/references/verify-step-detail.md` | prose | package 3 gives it goal and artefacts instead of the executor's self-report |
| 25 | Publisher and communicator | `skills/publish/SKILL.md` (13 KB), `skills/communicator/SKILL.md` (45 KB) | mixed | four deterministic linters run before anything is shown |
| 26 | Feedback in and out | `skills/feedback-intake/SKILL.md`, `skills/feedback-collector/SKILL.md` | prose | unchanged |

## Carrying work across a window

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 27 | Active work survives a window change | rule 6 of `skills/live-spec-base/SKILL.md:118-134`. Files live in `.live-spec/checkpoints/`, which is gitignored. No program writes, reads, validates or notices a checkpoint — grep for the word finds it only in skill prose and in the checkpoint files themselves | prose | schema plus a writer and a reader; the decision sheet of row 9 is what it carries | 3 |
| 28 | Minimal brief to a specialist naming primary sources | `references/delegation-protocol.md` | prose | `skills/director/SKILL.md` | 3 |
| 29 | Independent branches run in parallel | `scripts/open-lane.sh` — real code: checks HEAD, staged files, a lane cap | runs | unchanged; Director decides which branches are independent | 3 |
| 30 | One integration owner per canonical surface | `references/lanes-and-pen.md` | prose | `skills/director/SKILL.md` | 3 |

## Learning what the product should be

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 31 | Observation → hypothesis → measurement → result → conclusion → updated product knowledge | absent | absent | existing homes first: `PRODUCT_SPEC.md` for confirmed behaviour, `DECISIONS.md` for decisions, `docs/research/` for work in flight. A new canonical document only if a real end-to-end task proves those three cannot hold a hypothesis | 4 |

## Proof proportional to risk

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 32 | One verification entry that prints the checks it chose and why | `guardrails/pre-push` runs a fixed chain of 29 lettered gates and prints no reason for any of them | runs, but unconditionally | one entry, selection derived from affected components | 5 |
| 33 | Keep the checks that protect something real | 20 of 69 leaf checks. Several were bought with real incidents: `check-broad-kill.sh` after `pkill chrome` killed a live browser, `check-muted-launch.sh` after a test played sound, `check-runaway-child.py` after a process burned a core for 46 minutes, `check-config-health-perms.py` after a renamed folder gave a week of silently failed deploys, `hooks/worker-restore-guard.py` after a worker restored the tree over unsaved work | runs | unchanged | — |
| 34 | Delete the checks that guard only the shape of LiveSpec itself | 39 of 69. The pure meta-guards are gates `u`, `v`, `w`, `ae`, `af`, plus `check-hooks-can-fire.py` and the tree-count arm of `ad` — each one's whole subject is another check, its registry or its manifest. `guardrails/attic/` holds 6 more that nothing calls and that say so in their own docstrings | runs | deleted with their manifests, configs, docs and tests | 5 |
| 35 | Retire the invented numeric ceilings | 2 architecture nodes per file; 185.8 bytes per spec criterion; 25 words per sentence; 12 items on the board; 4 reason-less language rules; a 1780-second suite budget | runs | deleted unless an outside product reason is found for each | 5 |

## Moving an existing project onto the new system

| # | Capability | Lives today in | Verdict | Target home | Pkg |
|---|---|---|---|---|---|
| 36 | One versioned migrator with inspect, dry-run, backup, apply, verify and restore | `install.sh` copies skills with a backup; `adopt/START.md` lands templates; `MIGRATION.md` states rules in prose. No mode set, no manifest of hashes, no tested restore path | mixed | one script with the six modes | 6 |

## What build-pipeline is actually worth

The 56 KB file is not uniformly waste. Package 3 extracts, and the rest goes:

**Worth extracting** — `references/delegation-protocol.md` (how a worker is briefed),
`references/excuses-table.md` (the rationalisations that precede skipping a real check),
`references/lanes-and-pen.md` (parallel-work ownership), `references/verify-step-detail.md`
(independent verification), `references/guardrails-catalog.md` (what each gate is for).

**Superseded by the Director** — the door table and its tripwires, the work-kind table,
the footprint scale, the request-kind table, the fixed step sequence at lines 305-596.
These are the fixed pipeline the mandate replaces, and re-homing them under a new name
would be the forbidden move.

**Belongs elsewhere** — `references/project-setup.md` merges into the package 6 migrator;
`references/footprint-read.md` and `references/minor-bump-gate.md` describe gates that
package 5 examines on their own merits.

## What this map found that the mandate did not predict

Three things the mandate assumed were present and are not:

1. **There is no intake code of any kind.** Not a weak classifier, not a regex — nothing.
   Every routing decision in LiveSpec today is a model reading an instruction. The
   mandate forbids implementing understanding as keywords and regex; that prohibition
   costs nothing here, because there is nothing to dismantle.

2. **The checkpoint is a convention, not a mechanism.** Scenario 9 of the acceptance
   list — a new agent resumes from a compact checkpoint — has no implementation behind it
   at all. It works today only when the agent that ended the window happened to write a
   good file.

3. **The idea shelf and the commitment queue are the same table.** Every wish gets a task
   id the moment it is uttered. Splitting them is not a new board; it is a section break
   and a rule about when an id is issued.

One thing the mandate assumed was harder than it is: two canonical documents already have
generated, push-gated indices. Package 2 extends a working mechanism rather than inventing
one.

## Package 3 progress (2026-08-24) — rows this map should no longer read as pending

This section is dated status, not a rewrite of the rows above — the rows still name where
each capability *lives*, which is the point of the map; read them together with this note
rather than treating either alone as current.

- **Row 27 (checkpoint)** — `runs`. `scripts/checkpoint.py` (writer/reader/validator/CLI).
  Landed first, on its own, before anything below depended on it.
- **Rows 9, 10, 11, 28, 30** — the Director no longer only writes a decision sheet for
  review; `skills/director/SKILL.md` v6.0.0's "Execution" section opens a director-owned
  checkpoint (row 9's decision sheet is now that checkpoint's DECISION SHEET section,
  mechanically validated), sends specialists a minimal brief (row 28), rebuilds the plan on
  a new fact (row 11), and treats a shared canonical document as a serialized convergence
  point under one integration owner (row 30). Verdict for all four stays **prose** — which
  specialist to call, when a fact changes the plan, and who holds the pen are still model
  judgment, same as the mandate says they should be (rule 11) — but the target home in each
  row is now populated, not empty.
- **Row 24 (independent verifier)** — the mechanics moved verbatim from
  `skills/build-pipeline/references/verify-step-detail.md` to
  `skills/director/references/verify-step-detail.md`, called from Director's Execution
  section instead of a fixed pipeline stage. Still prose; still real, since the underlying
  worker-restore gate and audit walk it invokes are code (`guardrails/check-worker-restore.py`).
- **Row 29 (parallel lanes)** — unchanged, as predicted: `scripts/open-lane.sh` already ran
  before this package; Director's Execution section now states the independence judgment
  inline instead of leaving it implicit.
- **Row 21 (architect)** — resolved. Architect ships as its own standalone in-repo skill,
  `skills/architect/SKILL.md`, mirroring `test-author` rather than being extracted to a
  separate repository (that pattern stays reserved for capabilities proven reusable
  standalone, like `product-prover` and `text-audit`) or kept as a Director-read reference
  file (that pattern stays for the independent verifier, which is always in service of
  other work rather than a task a human invokes on its own). `skills/director/SKILL.md`'s
  specialist table points to it directly. `skills/build-pipeline/SKILL.md` step 3 and its
  `references/architecture-step-detail.md` are untouched — build-pipeline's own cutover to
  calling this skill is not part of this slice; no partial migration.
- **Rows 8, 12–15, 31–36** — untouched by this slice; still read as this map already states.
