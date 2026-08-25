# Prover record — 2026-08-25 build-pipeline-cutover-slice-plan

PUSH-REVIEW

Range: f96dad65..9e123c44 (1 commit: `9e123c44` "capability-map: design cutover slice plan
for build-pipeline (no code changes)"). One file changed, `docs/director/capability-map.md`
(74 insertions, 0 deletions). No file under `skills/`, `tests/`, or `guardrails/` touched.

## What this is

Package 3's cutover of `skills/build-pipeline/` (step 5) was unblocked by the scenario gate
closing (`f96dad65`, prior push). Before touching any code, this records a dependency-ordered
slice plan in `docs/director/capability-map.md` — the project's own migration manifest,
extending its existing "What build-pipeline is actually worth" section rather than starting
a new document (rule 10, no bureaucracy without need).

Read `skills/build-pipeline/SKILL.md` in full (729 lines) before writing anything — the file
is not a stale router the mandate assumed superseded; it is the software-delivery method
itself (spec → prove → architecture → prove architecture → matrix → test → code → verify →
commit, with craft standards per step, the door/tripwire law, class-hunt on bugs, versioning
and push rules). Director replaces the FIXED step sequence and the door/tripwire/work-kind/
footprint/request-kind classification tables (superseded outright); it does not reimplement
each specialist's craft, which mostly already lives in the specialist's own SKILL.md.

## What the design pass found, corrected in the writing itself

1. Re-verified the existing "worth extracting" list against the current tree rather than
   trusting the map's memory of it (§1.2.1's own rule). `verify-step-detail.md` is confirmed
   already moved to `skills/director/references/` (row 24, prior slice) — the one item on
   the extract list that's actually done.
2. `references/architecture-step-detail.md` (quality budgets, the node fitness test,
   runtime/placement views) is orphaned, not duplicated: `skills/architect/` has no
   `references/` directory at all. Row 21's note that "build-pipeline's own cutover to
   calling this skill is not part of this slice" is still true and still open.
3. Three reference files (`project-setup.md`, `footprint-read.md`, `minor-bump-gate.md`) have
   no ready target home — their homes are packages 6 and 5, neither started. This makes full
   deletion of `build-pipeline/` premature regardless of scenario-gate status; the mandate's
   sanctioned "short transitional adapter" is the only honest option until those packages
   land, not a corner cut.
4. First draft of this note claimed `skills/director/SKILL.md` "already reads
   `delegation-protocol.md` from its original location... Director depends on a file it does
   not own." **Checked the actual citation (line 234 of `skills/director/SKILL.md`) before
   committing that claim and found it backwards** — the citation names the file only to say
   what Director replaces ("none of that survives the cut into this skill"), not a live read.
   Corrected in the same draft, not shipped wrong.
5. The real mechanical dependency, found by reading `tests/test_worker_restore.py` directly
   rather than trusting the prose citations: its `CLAUSE_HOMES` list names five files
   (`skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md`,
   `skills/build-pipeline/references/delegation-protocol.md`, `templates/agent.template.md`,
   `scripts/open-lane.sh`) whose worker-restore-clause wording the test asserts
   byte-identical, sentence by sentence (`CLAUSE_SENTENCES`, same file). Moving
   `delegation-protocol.md` without updating this list in the same commit reds the suite
   outright — recorded as a hard requirement on the relevant slice step, not left as prose to
   reconcile by judgment later.

## What this means for the next slice

Five ordered steps recorded in the map (extract 4 reference files + repoint consumers
including the `CLAUSE_HOMES` fix; close the orphaned `architecture-step-detail.md` debt onto
`skills/architect/`; delete the superseded fixed-sequence content from
`skills/build-pipeline/SKILL.md`; rewrite the remainder as the short transitional adapter;
retriage roughly 40 tests currently asserting the deleted prose). Steps 1-2 are independently
safe and revertible without committing to 3-5 in the same sitting. Not started — this record
covers the design pass only.

Files read: `skills/build-pipeline/SKILL.md` (full, 729 lines), `docs/director/capability-map.md`
(full, both before and after this edit), `skills/director/SKILL.md` (the delegation-protocol
citation at line 234 plus surrounding context, and the verify-step-detail citation at
lines 255-263), `tests/test_worker_restore.py` (the `CLAUSE_HOMES`/`CLAUSE_SENTENCES` block),
`guardrails/README.md` (its own worker-restore clause and file-list citation),
`skills/build-pipeline/references/delegation-protocol.md` (full), and a grep sweep for every
other consumer of the four extract-candidate reference file names outside
`skills/build-pipeline/` itself.

Checks run: `git diff --stat -- docs/director/capability-map.md` — one file, 74 insertions,
0 deletions, confirmed nothing else touched. `git diff origin/main --stat -- skills/ tests/
guardrails/` — empty, confirming no code-bearing directory was touched by this slice. No test
suite run — this commit carries no executable content to test; the correctness claim rests on
the file reads listed above, not on a pytest result.

Findings: one design-only planning update, and one self-caught drafting error (the
delegation-protocol dependency direction) corrected before it shipped rather than after. No
blocking implementation defect — there is no implementation yet.

Blocking: none
