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
| 14 | Reader-worker returns pointers, not pasted text | `skills/director/references/delegation-protocol.md` (moved from `build-pipeline` 2026-08-25, cutover slice 1) | prose | `skills/director/SKILL.md` | 1 |
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

## 2026-08-25 — cutover slice plan (design only, nothing executed yet)

The scenario gate closed (`docs/prover/2026-08-25-director-scenario-gate-resample.md`),
unblocking this cutover. Re-verified against the current tree before committing to a plan
(§1.2.1's own rule: read the real file, don't trust the map's memory of it) — two things the
"worth extracting" section above didn't yet say plainly:

- `skills/director/SKILL.md` cites `delegation-protocol.md` by its build-pipeline path only
  to say what it replaces ("none of that survives the cut into this skill") — not a live
  read. Correction to an earlier draft of this note, which had this backwards.
- **The real, mechanical dependency is `tests/test_worker_restore.py`'s `CLAUSE_HOMES`
  list** — five files (`skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md`,
  `skills/build-pipeline/references/delegation-protocol.md`, `templates/agent.template.md`,
  `scripts/open-lane.sh`) whose worker-restore-clause wording the test asserts is
  byte-identical, sentence by sentence (`CLAUSE_SENTENCES` in the same file). Moving or
  deleting `delegation-protocol.md` without updating this list in the SAME commit breaks the
  test outright — this is not prose to reconcile by judgment, it is a hard mechanical gate.
  `skills/director/references/verify-step-detail.md` is NOT in this list today; whether it
  needs to be (or whether Director's own SKILL.md should carry the clause verbatim instead)
  is an open question this note flags rather than answers — check both against
  `CLAUSE_SENTENCES` before touching either file.
- `references/architecture-step-detail.md` (quality budgets, the three-question node
  fitness test, runtime/placement views) is real architect craft, but `skills/architect/`
  has no `references/` directory at all — this content is orphaned, not duplicated. Row 21
  said its own cutover "is not part of this slice"; that debt is still open and blocks a
  clean `architect` skill exactly as much as it blocks `build-pipeline`'s removal.

**Three reference files have no ready target home yet** — `project-setup.md` (merges into
the package 6 migrator, not built), `footprint-read.md` and `minor-bump-gate.md` (package 5
examines these gates on their own merits, not started). The mandate bans partial extraction
(no forbidden "re-homing under a new name" of superseded logic, no half-cut pipeline), but a
**short transitional adapter is explicitly sanctioned** ("удаляется или превращается в
короткий переходный адаптер") — and it is the only honest option while packages 5/6 don't
exist yet: three real, still-needed capabilities (project setup, footprint reads,
minor-bump-gate procedure) have nowhere else to live today.

**Slice plan, in dependency order (each its own push per §1.1, not one giant commit):**

1. Move `delegation-protocol.md`, `excuses-table.md`, `lanes-and-pen.md`,
   `guardrails-catalog.md` to `skills/director/references/` (mirroring how
   `verify-step-detail.md` already moved there). Repoint every consumer found by a fresh
   grep, not the list here — `guardrails/README.md` and `skills/director/SKILL.md` cite
   `delegation-protocol.md`'s old path in prose (safe, not a live dependency — see finding
   above). **`delegation-protocol.md` specifically also needs `tests/test_worker_restore.py`'s
   `CLAUSE_HOMES` list updated to its new path in the SAME commit** — the test asserts
   `CLAUSE_SENTENCES` byte-identical across that closed list; moving the file without
   updating the list reds the suite outright, not a judgment call.
2. Move `architecture-step-detail.md` to `skills/architect/references/`, wire
   `skills/architect/SKILL.md` to read it directly — this closes row 21's deferred debt as
   its own small slice, before touching build-pipeline's body.
3. Delete the superseded content from `skills/build-pipeline/SKILL.md`: the door table and
   tripwires, the work-kind table, the footprint scale, the request-kind table, the fixed
   step sequence (current lines ~305-596). Director's dynamic graph is the replacement,
   already shipped.
4. Rewrite what remains as the short transitional adapter: a page that states plainly
   `build-pipeline` is no longer the entry point (`skills/director/SKILL.md` is), and parks
   only `project-setup.md`, `footprint-read.md`, `minor-bump-gate.md` until packages 5/6
   give them permanent homes. Frontmatter `description` changes so the skill is no longer
   invoked as a router — only for the setup-walk case its remaining content still serves.
5. The costly step: every one of the ~40 tests currently asserting build-pipeline's deleted
   prose needs a per-test decision — retired outright (the behaviour it checked is now
   Director's, covered by `evals/director/scenarios.json` instead), rewritten to test the
   adapter's narrower remaining scope, or left alone (a handful test the reference files
   moving in steps 1-2, which still exist, just elsewhere). This step is what actually
   determines the slice's size; steps 1-4 are mechanical by comparison. Grep broadly before
   touching anything (§5.16's own lesson from the architect extraction, which is the same
   file family this cutover touches again) — TEST_MATRIX.md, ARCHITECTURE.md, adopt/,
   MIGRATION.md, and every closing-roster the architect extraction already found scattered
   across 6 files.

Not started. Recommended order above is designed so each step alone is independently safe
and revertible if a later step turns out wrong — steps 1-2 in particular can land, prove
green, and be walked away from without committing to steps 3-5 in the same sitting.
- **Rows 8, 12–15, 31–36** — untouched by this slice; still read as this map already states.

## 2026-08-25 evening — steps 1-2 landed; step 3's own premise checked and found wrong

Steps 1-2 above are done: the 4 reference files moved to `skills/director/references/`, and
`architecture-step-detail.md` to `skills/architect/references/`, `c6c7b51b` on `origin/main`, CI
green. Full detail in `docs/prover/2026-08-25-build-pipeline-cutover-slice-1.md` and
`docs/skill-review/2026-08-25-build-pipeline-cutover-slice-1.md`.

**Step 3's assumption — that lines 113-596 are cleanly "superseded, safe to delete" — does not
hold on inspection.** A dedicated read (comparing `build-pipeline/SKILL.md`'s full 113-596 range
against `director/SKILL.md`'s full body plus every specialist skill it delegates to) found:
only a small slice is genuinely superseded by Director itself (the routing one-liners, and the
verify-by-deed audit already migrated to `director/references/verify-step-detail.md`); a real
middle slice duplicates content that already lives in the specialist skills
(`spec-author`/`product-prover-pack`/`design-reviewer`/`architect`/`test-author`) rather than in
Director — safe to delete from build-pipeline for that reason, but not because "Director covers
it"; and a substantial remainder has **no home anywhere in the tree today**: the bug-door class
hunt (INV-104/124), the five feature-tripwires, the work-kind APPLIED/STOOD-DOWN accounting
contract, the mockup-first entry condition (INV-43, not even acknowledged on this map's own "no
ready home" list below), the closed request-kind set with its mandatory back-checks, the entire
Step 4 (prove-architecture's six checks), the entire Step 7 (code step's smallest-first build,
norm-pointer building, "a rejected artifact reopens its source"), and the entire Step 9 (commit &
show — PATCH/MINOR/MAJOR judgment, the CHANGELOG-speaks-to-user-vs-journal-speaks-to-builder
rule, DECISIONS.md's `[default]`-authorship accounting). Deleting these with no new home would be
a real, silent loss of load-bearing craft — exactly the failure class the pack's own rule 10 and
rule 14 exist to catch, applied here to the pack's own body.

Separately, this same read found the **footprint scale is on both sides of this map's own
contradiction**: this section's step 3 (above) calls it superseded, while the "no ready home yet"
paragraph three sections up lists `footprint-read.md` as having nowhere to go. `footprint-read.md`
also documents live mechanical gates (`INV-134`/`INV-135`, `guardrails/crosscut_counter.py`) that
still run — its prose cannot simply vanish. And `director/references/excuses-table.md` (already
migrated, step 1) still reads in the old door/tripwire vocabulary ("take the pipeline door you
were about to skip") — correct today, since build-pipeline still has doors, but due for a rewrite
the moment step 3 actually retires them, not before.

**Revised step 3: give every genuinely-homeless (class-b) piece a real landing spot — in
Director's own body, a Director reference file, or the owning specialist skill — before deleting
anything from `build-pipeline/SKILL.md`.** This is several slices, not one. The full section-by-
section classification (line ranges, a/b/c verdict, reasoning against director's and every
specialist skill's actual current text) lives in this session's research agent output only, not
yet a committed file — the next session should re-run the same comparison (build-pipeline's
113-596 against director + spec-author/product-prover-pack/design-reviewer/architect/test-author's
full bodies) rather than trust a paraphrase, per this map's own §1.2.1 rule.
