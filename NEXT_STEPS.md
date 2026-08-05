# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-05, 22:26)

The branch is pushed. Every gate in `bash guardrails/pre-push` passed, and the day's 57 commits
carry one adversarial review record at `docs/push-review/2026-08-05-day-of-readability-repairs.md`.

The afternoon ran the whole forward queue through parallel workers. The audit skill
closed reading round 30 and 31, and every stop the two readers shared. Four adversarial reviewers then read the day's commits and found eleven defects; all
eleven were repaired the same day. The restore gate took four repairs and now reads a command
string the way a shell does. The public edition of the spec-review skill is current again. The
three writing rules that held two owners became six rules with one owner each, and the rule home
holds 66. Three totals that drifted by hand now generate inside fenced blocks.

Eleven inbox messages were harvested into rows 532 to 546, and every message rests in `attic/`
with a manifest line.

Both questions the review raised are answered (`DECISIONS.md`, 2026-08-05). A text ships when
both cold readers return nothing that blocks, twice in a row. The templates are measured again,
and the test fixtures stay outside the reading queue.

## Forward queue

1. Run the next reading round on the audit skill. The skill asks for one prompted reader and one
   unprompted reader; today's round ran two prompted readers, which the next round corrects.
2. Take rows 532 to 546 through the pipeline. Rows 537 and 538 open with a freshness re-check,
   since the reds they cite no longer reproduce.
3. Re-seed the rounds-per-file estimate once a second file finishes its readings.

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. It gives the hours each file still owes. Each column carries a note saying what it counts
and what it aims at. Build it with `python3 scripts/measurements-table.py`. Every number stated to
the person who decides what ships carries five things. It names what it counts and in what unit. It
names the decision it informs, and what changes when it moves. It names the command that produced
it and the value it aims at. A bare number is a defect of the same kind as an undefined term.

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
