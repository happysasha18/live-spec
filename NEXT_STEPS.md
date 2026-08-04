# Next steps — live-spec

## Read this first, 2026-07-29 evening

The owner stopped the readability campaign here and opened a fresh session to rethink it. Three
things stand settled, and one decision is his. Everything below this section describes the campaign
as it ran before that stop, and the measurements page it points at still holds.

**The campaign measured the wrong thing, and this is on record.** The count of 4,813 findings
over 115 documents holds 3,454 sentences past 25 words. It holds 1,202 words written in capitals.
Every other class together is 157. The register check finds nothing at all: it carries 23 fixed
patterns and matches none of them anywhere in the tree. A number of this shape says little about
whether a stranger can read a document.

**Every rule now names its owner.** `guardrails/language-rules.json` carries 63 rules. Each one holds
an `owner` block naming the thing that decides a break of it. A script owns 18 and the reading agent
owns 42. Three bundle a mechanical arm with a meaning arm, and they owe a division before one owner
fits. The reason stands in the same block, and `docs/language-rule-coverage.md` prints it under each
rule.

**The reader now gets the rules.** `skills/text-audit/references/reader-prompt.md` is generated out
of the rule home. It prints the 38 rules that bind human prose and belong to the reading agent. It
carried five hand-written classes before.

**The decision the owner holds: what bar a text must clear to ship.** The rule says two consecutive
readings with nothing blocking. Nine readings of one file returned 11, 8, 12, 6, 5, 5, 6, 5, 8 and
never reached it. The agreement rule added on 2026-07-29 lowers the count by dropping every place
one reader of a round found alone. Three shapes stand ready: zero for both readers; zero by
agreement; or shipping with the remaining stops listed at the text's head. No file closes until this
is answered.

**The state of the tree.** Eight files carry uncommitted work. They are the rule home, the
generator, the language-rules gate, the measurements script and its page, the repair brief, and the
baseline record. `docs/PROGRESS.md` stands untracked beside them. The language-rules gate, the findings-bound
gate and the register lint are green over all of it. Six tests were red before this work started and
are red still: `test_guardrails` twice, `test_rendered_sweep`, `test_resume_digest`,
`test_traceability`, and `test_worker_restore`. One of the six is Russian text inside shipped test
fixtures written on 2026-07-28. No commit goes out until those six are green.

**Stale counts to repair.** Three files state rule totals written by hand and left behind. The
readability plan says 54 rules, and its six families reach 43 codes. `docs/language-defects.md` says
53 rules and `r62`. `docs/language-worked-example.md` says 39 rules bind human prose. The home holds
63 rules and its highest identifier is `r72`. Each of these counts should be generated out of the
home.

## Start here

Open `docs/MEASUREMENTS.html` in a browser. That page is the source of truth for where the work
stands. It carries one row per file and one column per indicator, in the reading queue's order, with
the hours each file still owes. Build it with `python3 scripts/measurements-table.py`, which writes
both that page and `docs/MEASUREMENTS.md`.

The owner set that page's format on 2026-07-29 and it holds until this project ends. Its shape stays
fixed. Columns run in order of significance and the header row pins to the top of the window. Every
column name carries a hover note saying what it counts and what it aims at. Every explanation sits
below the table.

## The two promises

**A reader gets through a document without stopping.** Two measures cover it. A script settles the
writing-finding count, and fresh readers report every place they stopped.

**The specification stops growing.** Measured by its size, by the text per acceptance criterion, and
by the pairs stating one fact twice.

Both are open. No file has reached finished.

## The rule that makes a reading loop close

A place counts against the text when **both readers of one round stopped there**. A place one reader
found alone is recorded as residue in `docs/language-defects.md`, and it blocks nothing.

The session settled this on 2026-07-29. Five rounds on one file returned fifteen and ten blocking
stops, then five and eight, then nine and four. No single reader's list repeated. Under the
agreement rule the counts ran eight, three, two, two, two.

## Where the work stopped, 2026-07-29 around 12:45

`skills/text-audit/SKILL.md` is the file in hand, fourth in the queue. Four repair rounds have landed
and the file measures zero on the counter. Its body was split, so the writing rules and the reader's
question list now sit under `skills/text-audit/references/`.

Round six of readings was running when the session closed: readings 27 and 28 on the strong tier, and
reading 29 on the cheap tier. Their records land in `docs/language-reads/`. Compare 27 against 28 for
the agreement rule, and compare 29 against both for the tier question below.

## What the next session does first

1. Repair the three places both strong readers of round six stopped at, listed in
   `docs/measure/2026-07-29-reader-tier-comparison.md`, plus the two the cheap reader found alone.
   Then run round seven as one strong reader and one cheap reader.
2. Record round six in `guardrails/progress-baseline.json` under `rounds`, then rebuild the page with
   `python3 scripts/measurements-table.py`.

The tier question is answered. `docs/measure/2026-07-29-reader-tier-comparison.md` holds it. A cheap
reader reached one of the three places the two strong readers agreed on. It also found two real
places neither strong reader reached. A round therefore runs as one strong reader and one cheap
reader. That pair costs less and loses no coverage the agreement rule uses.

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

Every number stated to the owner, in chat or in a document, carries five things:

- what it counts, and in what unit;
- why it is measured, meaning the decision it informs;
- what changes when it moves;
- the command or procedure that produced it;
- the value it aims at.

A number stated bare is a defect of the same kind as an undefined term.

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
