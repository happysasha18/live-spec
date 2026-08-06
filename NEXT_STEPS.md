# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-06, 16:53)

The three landings of 2026-08-06 are committed and pushed. They are the measured published counts
(row 555), the check registry with gate ae (row 556), and the spoken setup entry (row 557). The push chain runs
31 checks. Matrix rows M-505 to M-511 stand built. The freeze baseline covers the spec, the
architecture and the matrix at this state.

The public prover edition is repaired for any product kind and sits under its prose ceilings. Two
fresh runs over the shipped sample returned 32 and 30 findings, with 24 reached by both. The
edition's front page states exactly that, and both full run records ship beside the sample.

The suite is green. The five reds of the morning handover were repaired at their roots. The repairs were a scoped-run pin, three synced
skill copies, a cleanup notice in the counts generator, and a reinstalled push hook. The last
handover also names its extract file now.

## Forward queue

1. Row 558: give the opening read an artifact and make the handover gate refuse a push from a session
   that wrote none. The newest handover under `docs/handovers/` is dated 2026-08-06.
2. Row 559: put a machine over the reading panel — a gate that reds a round whose two readers came
   from one brief, and a stated test for what counts as a stop that blocks. The design sits at
   `~/live-spec-carry/2026-08-06/design-D-reading-bar.md`.
3. Row 560 waits on Alexander's word: the surface registry a new project copies carries two names,
   and the rename has been offered twice with no answer.
4. Row 561: give the settings ladder a `pack.tree` line, which the setup walk's routing card needs
   and nothing reads yet.
5. Run the next reading round on the audit skill, with one prompted reader and one unprompted reader.
6. Rows 562 to 565 carry the push review's findings of 2026-08-06. They are the real scoring run
   for the spoken-entry phrases, the counts published outside the declared registry, the
   founding-walk tests that re-implement the walk's readers, and the two run-record shapes.
7. Take rows 532 to 546 through the pipeline. Rows 537 and 538 open with a freshness re-check, since
   the reds they cite no longer reproduce.
8. Four stale work copies under `.claude/worktrees/` carry no unmerged commits (all from 2026-07-21,
   plus the merged registry branch). Removing them awaits Alexander's listed approval, since nothing
   is deleted silently.

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. It gives the hours each file still owes. Each column carries a note saying what it counts
and what it aims at. Build it with `python3 scripts/measurements-table.py`. Every number stated to
the person who decides what ships carries five things. It names what it counts and in what unit. It
names the decision it informs, and what changes when it moves. It names the command that produced
it and the value it aims at. A bare number is a defect of the same kind as an undefined term.

`guardrails/tree-counts.json` is the home for every count this repository publishes about its own
tree. It carries the measurement that produces each count and every page that states it, and gate ad
re-measures them on every push. Four surfaces stay outside it. A number
a session writes into chat. A number in a rendered artifact. A count inside a skill body. A count on
an undeclared page. The undeclared-page class has its row (563); the other three stand named as
unheld in the count row's non-goal (555).

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When the commit it names differs from the one you recorded at the
start of your session, read what changed and run `bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs `git checkout -- <path>`,
`git checkout .`, or `git restore` outside `--staged`. The same holds for `git stash` in every
form. It holds for `git reset` with `--hard`, `--merge` or `--keep`, and for `git clean` with `-f`
or `-x`. To put a file back, write back the bytes you read before you changed it.

Never give two workers the same file. Two workers held one file on 2026-07-29, and the second read
the first one's edits as an intrusion and reverted them. A test result is the printed count of
passes and failures. Run `python3 -m pytest -q > <scratch>/suite.log 2>&1` and read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py
--freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

`bash guardrails/pre-push` runs the whole push gate set, listed in `guardrails/README.md`. New
requirements, invariants and queue rows take the next identifier above the highest one in use in
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md`. Read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask. Publish
once the suite passes. Write documents in plain English. Before you ask the person who decides what
ships anything, check whether a document already answers it. If it does, act on that answer and
cite it. Say aloud whether a request is one-time or standing before acting.
