# Next steps — live-spec

## Start here

Open `docs/MEASUREMENTS.html` in a browser. That page is the source of truth for where the work
stands: one row per file, one column per indicator, the reading queue's order, and the hours still
owed. Build it with `python3 scripts/measurements-table.py`, which writes both that page and
`docs/MEASUREMENTS.md`.

The owner set that page's format on 2026-07-29 and it holds until this project ends. Its shape stays
fixed: columns in order of significance, the header row pinned to the top, a hover note on every
column name saying what it counts and what it aims at, and every explanation below the table.

## The two promises

**A reader gets through a document without stopping.** Measured by the writing-finding count, which a
script settles, and by fresh readers, who report every place they stopped.

**The specification stops growing.** Measured by its size, by the text per acceptance criterion, and
by the pairs stating one fact twice.

Both are open. No file has reached finished.

## The rule that makes a reading loop close

A place counts against the text when **both readers of one round stopped there**. A place one reader
found alone is recorded as residue in `docs/language-defects.md`, and it blocks nothing.

The session settled this on 2026-07-29 after five rounds on one file returned fifteen and ten
blocking stops, then five and eight, then nine and four. No single reader's list repeated. Under the
agreement rule the counts ran eight, three, two, two, two.

## Where the work stopped, 2026-07-29 around 12:45

`skills/text-audit/SKILL.md` is the file in hand, fourth in the queue. Four repair rounds have landed
and the file measures zero on the counter. Its body was split, so the writing rules and the reader's
question list now sit under `skills/text-audit/references/`.

Round six of readings was running when the session closed: readings 27 and 28 on the strong tier, and
reading 29 on the cheap tier. Their records land in `docs/language-reads/`. Compare 27 against 28 for
the agreement rule, and compare 29 against both for the tier question below.

## What the next session does first

1. Read the three reading records of round six and take the agreed places.
2. Answer the tier question from reading 29: does the cheap reader find what the strong readers find?
   The campaign plan requires this measurement before the tier is chosen, and every reading before
   round six ran on the strong tier with no evidence behind that choice.
3. Record round six in `guardrails/progress-baseline.json` under `rounds`, then rebuild the page.

## Three findings worth acting on

**The queue counts files nobody reads.** The page lists 118 files, and some are test fixtures and
templates for other projects. Separating them is the largest single reduction available on the 252
hours the page now estimates.

**One file at a time costs 31 working days.** Campaign rule 1 says one file is carried to finished
before the next opens. That rule was written so a class repaired on one file helps the next. The
classes repeat, so after two or three files the rule buys little. Four files side by side takes 11
working days instead of 42.

**The estimate rests on one file.** The figure of five reading rounds per file comes from
`skills/text-audit/SKILL.md` alone, and that file is unfinished. The second file re-seeds it.

## The measurement rule, standing from 2026-07-29

Every number stated to the owner, in chat or in a document, carries five things: what it counts and in
what unit, why it is measured, what changes when it moves, the command that produced it, and the value
it aims at. A number stated bare is a defect of the same kind as an undefined term.

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When HEAD has moved, read what changed, then run
`bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs any of these:

- `git checkout -- <path>` or `git checkout .`;
- `git restore`, outside `--staged`;
- any form of `git stash`;
- `git reset` with `--hard`, `--merge`, or `--keep`;
- `git clean` with `-f` or `-x`.

To put a file back, write back the bytes you read before you changed it.

Never give two workers the same file. Two workers held one file on 2026-07-29, and the second one read
the first one's edits as an intrusion and reverted them.

A test result is the printed count of passes and failures. Write the output to a file:
`python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py --freeze
PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

These numbers are free: requirement 304, INV-303, E-36, T-25, M-491, queue row 533.

## What waits, unpushed

Thirteen commits stand unpushed. A check that reads worker records caught a worker running a command
that discards uncommitted work, at 00:12 on 2026-07-29. Nothing was lost, and the proof sits in
`docs/reports/2026-07-29-session-report.md`. That finding clears twenty-four hours after the event.

## The owner's standing instructions

Run a whole movement alone: one wish carried from its first edit to a green suite and a push. Save and
publish on green without asking. Write documents in plain English. Run every gate in `guardrails/`.

Before you ask the owner anything, check whether an existing document already answers it. If it does,
act on that answer and cite the document. Name every request as one-time or standing before you act on
it, and say which it is.
