# Prover record — 2026-08-28 the board's done marks, re-checked, and the eleven keys

PUSH-REVIEW

Range: d69372c..67d6a25 (5 commits), reviewed as one pass. Base commit `d69372c`, the tip this push
starts from. Reviewed commits, in order: `f6e889b`, `da51fff`, `7ecd89b`, `1badfc4` (this record),
`67d6a25`.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

plan-10's own work: "Every done mark on the board gets checked." `PLAN.md` carried thirty-seven
hand-typed done marks and no way to tell a fact from a claim. This range re-checks every one of them
against the tree, corrects the five that did not hold, restores fifteen open rows' definition of
done from the archive the 27.08 merge dropped it into, and gives thirteen rows a command in
`scripts/plan_checks.py` so their marks are computed at every session start instead of typed.

Three files change: `PLAN.md`, `scripts/plan_checks.py` and
`tests/test_tasks_parser_finds_every_task.py`, which gains the two guards finding 11 describes.
Nothing else in the tree is touched. A
second session was writing `.github/workflows/gates.yml`, `matrix/product-prover.md` and
`tests/test_prover_doc_homes.py` at the same time; those are that session's, are not in this range,
and were not read as part of it beyond establishing that they explain three of the suite's reds.

## How this review was run

Read to refuse. Every mark this range moves, and every mark it leaves standing, was checked against
the artifact the row names — the script, the test, the commit — and never against the row's own
prose. Three marks the audit brief handed this session as wrong were checked the same way as the
rest, and one of them survived the check and is left where it stood, with the reason written out
under Findings.

Range: d69372c..7ecd89b

Files read: `PLAN.md`, `scripts/plan_checks.py`, `scripts/state-probe.sh`,
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`,
`guardrails/check-config-health.sh`, `scripts/install-session-hooks.sh`,
`tests/test_install_session_hooks.py`, `guardrails/check-pin-drift.sh`,
`guardrails/check-worker-restore.py`, `tests/test_worker_restore.py`,
`tests/test_compaction_discipline.py`, `tests/test_request_classifier.py`,
`matrix/build-pipeline.md`, `skills/live-spec-base/SKILL.md`,
`skills/live-spec-base/references/glossary.md`, `skills/build-pipeline/SKILL.md`,
`skills/communicator/SKILL.md`, `skills/communicator/references/words.md`,
`skills/director/references/landing-law.md`, `skills/product-prover/SKILL.md`,
`docs/skill-review/2026-08-12-product-prover.md`,
`docs/skill-review/2026-08-12-product-prover-2.md`, `DECISIONS.md`, `CLAUDE.md`.

Commits read: `e61b29b7` (the twelve self-referential checks removed, gate af among them),
`7b2980df` (the mirror-sync script and its three tests removed).

Checks run: `python3 -m pytest -q`, the whole suite the way CI runs it — 4 failed, 2464 passed, 4
skipped, 1 error, in 10m52s, against a tree that then held both sessions' uncommitted work. Three of
the four failures and the error are the other session's, re-run after this range's own commits
landed: `tests/test_guardrails.py::TestGateShippedLanguage` and
`tests/test_worker_restore_run_scope.py` — 30 passed, 0 error, so the error was the dirty-tree
artifact the plan's own trap list warns about. `tests/test_guardrails.py::TestGateShippedLanguage`
stayed red on this range's own doing; finding 1. After the repair — 24 passed.
`python3 -m pytest -q tests/test_board_matches_the_canon.py tests/test_plan_is_not_executable.py` —
8 passed. `python3 guardrails/check-board.py` — exit 0. `bash scripts/render-board.sh` — exit 0.
`bash scripts/state-probe.sh` — reads 35 done, 28 open, 63 rows. Every command in
`scripts/plan_checks.py` run in one pass and timed: all green but `plan-9`, which is the deferred
photo-site row and is correctly red; whole table 0.79s.
`time bash guardrails/check-config-health.sh` — 0.35s. `time bash guardrails/check-pin-drift.sh` —
36.7s, which is why it is not a key.

Findings: eleven, listed below — three defects this range carried, all found and repaired inside it,
and eight readings of what the marks on the board actually stand on.

## Findings

**1 — defect, found and repaired here. The restored text carried the owner's own name into a
shipped artifact.** The archive's acceptance for q-596 and q-166 names him three times.
`guardrails/check-shipped-language.sh` (gate i) refuses a personal name in a shipped file, and
`tests/test_guardrails.py::TestGateShippedLanguage::test_gate_green_on_the_swept_tree` went red on
both rows the moment the restore landed. Repaired in `da51fff` by the substitution the rest of
`PLAN.md` already makes everywhere — the owner — with §Blockers recording that the restore is
verbatim apart from this. No allowlist entry was written: the gate is right, and the imported
wording was the thing out of step. This is the same anti-self-dealing line `PLAN.md` law 1 draws.

**2 — defect, found and repaired here. Two keys would have gone green on a deleted file.** plan-7's
first form asserted only that the thirteen retired rule numbers are absent from
`skills/live-spec-base/SKILL.md` — true of a rulebook that no longer exists. plan-17's asserted that
`scripts/plan-step.sh` exists, not that it runs. Both are law 10's own shape, written into the very
table built to close law 10's gap. Repaired in `7ecd89b`: plan-7 proves the rulebook is present and
numbered before it reads the holes, and plan-17 tests the step reader is executable. Every other key
in the table is a positive assertion and was re-read for the same hole; none has it.

**3 — the brief's q-529 call does not survive the check, and the mark stays.** The audit handed this
session seven wrong marks. Six check out. q-529 does not. The reason given was the row's own line
saying it waits on the owner's policy answer about whether a written reason expires. That line is
undated, traces to `Source: found 2026-07-29`, and quotes nobody. §Blockers carries a later and
dated fact: his word of 27.08, that machinery is this seat's call and he is asked only about
machinery he set up himself, recorded with the file it went into. The base rulebook's rule 13 settles
which of the two wins — an attribution to the person names the exchange it came from, and only one of
these does. Checked past the paperwork as well: `scripts/rule-census.py` and
`guardrails/check-doc-findings-bound.py`, the two pieces the 2026-07-29 report described, are both
out of the tree, and `guardrails/check-size-ratchet.py:16` states in its own text that it never
writes the config the reason lives in — so a reason cannot copy itself forward onto a raise it never
justified. The mark stays closed; the stale line goes, because it contradicts him.

**4 — q-537 re-verified whole, and it is genuinely done.** The row was cited to this session as red on
its own evidence. It is not, and the reason is that the drift was repaired earlier today.
`guardrails/check-config-health.sh` exits 0 in 0.35s. The half nobody had checked is standing too:
`scripts/install-session-hooks.sh:78-84` refuses a registration whose filename already appears in the
settings command, in whatever form the machine wrote it, and
`tests/test_install_session_hooks.py::test_a_meter_wrapped_existing_entry_is_recognized_not_duplicated`
seeds a meter-wrapped entry and asserts exactly one survives. Both greps are in the key.

**5 — two rows are closed over a subject that was deliberately deleted, and reopening them would ask
for work nobody wants.** q-625 shipped a generated gate manifest, its builder and its check on 19.08;
`e61b29b7` removed all three on 21.08, naming gate af in its own commit message as one of twelve
checks whose only subject was another check. q-597 fixed a copy-out step's error reporting on 12.08;
`7b2980df` removed the whole copy-out step on 19.08, naming the three tests it retired with it.
Neither has an artifact left for a command to read. Both keep the closed mark and carry a line naming
the commit. This is the honest third state the board had no vocabulary for, written in words rather
than as a sixth mark.

**6 — q-576 and q-591 are back open, and q-591 is the more interesting of the two.** q-576 asks for a
page listing every number in the tree with its home and a verdict, read by the owner. A sweep ran and
its fixes landed; no such page exists anywhere under `docs/`, and the sweep's own account sits in a
gitignored working note. q-591 is a re-drift: the row closed on 12.08 by dropping a stale home leg
from matrix row M-313. `matrix/build-pipeline.md:63` still names its proof
`test_build_pipeline_carries_compaction_every_pass`, and that test reads
`skills/director/references/landing-law.md:38` — `skills/build-pipeline/SKILL.md` carries no mention
of INV-164 at all. The pointer went stale a second time when the rule changed house. Worth naming as
a class rather than a row: a matrix pin that names its proof by a test's name inherits whatever that
name asserted at birth, and a test name does not move when its subject does.

**7 — the fifteen restored definitions of done are all sentences, and this range does not fix that.**
`PLAN.md:45-49` sets the bar: a row earns its queued mark when its definition of done is a command.
Not one of the fifteen restored from the archive is a command; the closest, q-398 and q-453, name a
red-proof and a test inside a sentence. So every one of the fifteen still fails the file's own bar,
and the board now shows that plainly instead of showing nothing. Rewriting fifteen acceptance lines
is a judgment call per row and is left to its own pass, said out loud in §Blockers rather than
papered over.

**8 — q-568 is closed and its own acceptance was never met.** The row asked for a page listing each
fixed step of the method with its price, the rule demanding it, its author and a verdict, read by the
owner. That page was never produced and nothing in the tree stands in for it. What closed the row is
plan-17's measurement of what a session really carries, which answered the question underneath it —
a defensible close, recorded as such in §Blockers on 27.08. The mark is left where it is and the row
now says in its own words that the page does not exist, so nobody reads the mark as proof it does.

**9 — thirteen keys, not thirty-seven, and the reason is the boot.** Every command in
`scripts/plan_checks.py` runs at every session start. Nine closed rows are true but verifiable only
by reading, and three of those nine pin prose in the reviewer's own repository, which this tree does
not own and which moved twice today. A key per row would have put weight back into the exact place
plan-7 and plan-17 just spent effort cutting. The thirteen written are each a grep, a `test`, or one
guard that already exists; the whole table runs in 0.79s, and `guardrails/check-pin-drift.sh` is
deliberately outside it at 36.7s. The nine reading-verified rows each carry one line naming who read
them and the `file:line` that proves it.

Correction to this range's own writing: `f6e889b`'s message opens by saying eleven rows gain a key and
then lists thirteen. Thirteen is the number, and the table itself is the fact — the sentence miscounted
its own list.

**10 — the class rule is in the plan's rules section, where the board's own laws live.** One
sentence: a task that closes writes its check the same moment, wherever its subject is an artifact
that can drift back; a task whose result is prose, a measurement or a decision writes no command and
says instead who read it and where. Without it this audit is a one-time sweep and the thirty-eighth
unchecked mark is written tomorrow.

**11 — defect, caught by the push gate and repaired here. The command table had no guard of its
own.** Gate h's tests-present check refused the push: `scripts/plan_checks.py` changed with nothing
under `tests/`. It was right, and the gap is older than this range — the table has been read by both
readers and executed by the probe with nothing standing behind it.
`tests/test_tasks_parser_finds_every_task.py` gains two checks in `67d6a25`, each naming an incident
rather than a worry. A key outliving its row: plan-1's key survived its task into the 28.08 board
rotation and ran every morning against a step that no longer existed, until someone removed it by
hand. A key that writes: `PLAN.md`'s own trap list records `tests/test_guardrails.py` leaving a
`git stash` unrestored on an interrupt, and the probe is the first command a session runs, before
anyone has decided anything. The write guard drops single-quoted spans before it looks, because a
grep's pattern is prose — "run at every push" is a sentence in a skill file, not a command — and it
is red-proven against `git stash list`, `rm -rf` and `git checkout --`, green against that quoted
pattern and against `hooks/worker-restore-guard.py`'s own filename.

Blocking: three items, all closed.
- closed: `tests/test_guardrails.py::TestGateShippedLanguage::test_gate_green_on_the_swept_tree`
  reddened on this range's own restore (finding 1). Repaired in `da51fff` by making the imported
  wording read the way the rest of the file reads. No allowlist entry, no exception, no waiver: gate
  i's reach over the shipped set is exactly what it was.
- closed: gate h's tests-present check refused the push over `scripts/plan_checks.py` changing with
  nothing under `tests/` (finding 11). Repaired in `67d6a25` by writing the two guards the table had
  never had, each red-proven. The gate was not scoped, exempted, or routed around.
- closed: two keys in this range's own new table would have gone green on a deleted file
  (finding 2). Repaired in `7ecd89b` before the push, and the remaining eleven re-read for the same
  hole.

## Verdict

The range does what it says. Three defects were found in it — two by this review and one by the push
gate — and all three are repaired in it. One of the seven marks the audit brief called wrong is left
standing, with the dated word and the
code that settle it. Three things this range deliberately does not do, each said out loud on the
board rather than left for a later reader to discover: the fifteen restored acceptance lines are
still sentences and still fail the plan's own bar, the cost-per-step audit page q-568 asks for does
not exist, and q-591's re-drift is left open rather than fixed inside a row about marks.
