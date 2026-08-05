# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-05, 14:11)

The morning's forward queue is walked to its end. One step remains: the push, waiting on the
suite run now writing its log. This session's landings, from 13:12 on, stand below; the morning process landed its own before.

The five morning inbox messages became rows 532 to 540, and row 531 grew. The prover pass added row 541. Two afternoon arrivals became one landed gate fix and row 542. The
audit skill `skills/text-audit/SKILL.md` closed reading round 30 and 31. Eight stops both
readers hit are repaired against their named sources. Thirty single-reader stops went to
`docs/language-defects.md`. Two stops one reader marked blocking were repaired the same day.

A **reading** is one agent reading one file cold and filing a record under `docs/language-reads/`.
A **round** is two readings of one version of a file, one on the strong tier and one on the
cheap tier, per `docs/measure/2026-07-29-reader-tier-comparison.md`.

The three writing rules holding a script part and a reader part split into six rules, each
with one owner. The rule home `guardrails/language-rules.json` holds 66 rules. Three totals
that drifted by hand now generate inside fenced blocks, and the drift gate reads every block
a page carries.

The reading queue dropped the test fixtures and the templates for other projects: 29 entries
left the census record, which now holds 98 measured files. The design map in `ARCHITECTURE.md` had 31 stale
line-pointers; they point at their lines again, with a check record beside the edit.

The restore gate `guardrails/check-worker-restore.py` places a command in the directory it
really ran in. The morning alarm at 09:44 was a false positive from a scratch fixture, and
nothing was lost.

The finding ceilings, the measurements table, and the progress page are regenerated. The
three guarded documents are re-frozen. Every skill carries a review record newer than its
last change.

One decision stays open for the person who decides what ships, a policy call: the bar a
text must clear before it ships. Today's rule stands at two clean rounds in a row.
Round 30-31 found stops, so the file in hand has not reached the bar. Three shapes stand
ready: zero places for both readers, zero by agreement, or shipping with the remaining stops
listed at the text's head. Reading rounds go on while this is open.

## Forward queue

1. Push once the suite log reads green: `bash guardrails/pre-push`, then push.
2. Run the next reading round on the audit skill: one strong and one cheap cold reader, then
   merge and repair by step 3 of the loop.
3. Take rows 532 to 542 through the pipeline. Row 537 starts with a freshness re-check.
4. Re-seed the rounds-per-file estimate once a second file finishes its readings. Every hour
   figure on the measurements page rests on `skills/text-audit/SKILL.md` alone.

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
