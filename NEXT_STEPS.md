# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-05)

The project is rewriting its own documents so that a stranger can read them. It takes one queued
file at a time. Two agents read the file cold, and every place both of them stopped is repaired.
`skills/text-audit/SKILL.md` is the file in hand.

A **reading** is one agent reading one file cold and filing a record under `docs/language-reads/`.
The file in hand has 14 readings on record
(`ls docs/language-reads/ | grep -c text-audit-skill`). A **round** is two readings of one version
of a file. One runs on the strong tier (`claude-opus-5`) and one on the cheap tier
(`claude-sonnet-5`). The tiers are named in
`docs/measure/2026-07-28-tier-routing-experiment.md`. The pairing was settled by
`docs/measure/2026-07-29-reader-tier-comparison.md`. A place counts against a text when both
readers of a round stopped there. A place one reader found alone goes to
`docs/language-defects.md` and blocks nothing.

Branch `main` stands 24 commits ahead of `origin/main`
(`git rev-list --count origin/main..main`), and nothing has been pushed. Uncommitted work sits in
the tree; read it with `git status --porcelain`.

The last full test run finished 18 failing and 2298 passing on 2026-08-04 (`python3 -m pytest -q`).
The run before it gave 9 failing and 2302 passing. The run before that gave 10 failing and 2295
passing. A repair of 16 of the 18 is under way in another process as this is written.

`bash guardrails/pre-push` blocks the push today. Four gates are red. The test gate is red. The
skill-review gate names 11 skills whose review record predates the skill's last change. The freeze
gate reports drift in a guarded document. The findings-bound gate names
`skills/text-audit/SKILL.md`. The same run shows 9 skill files whose recorded finding count now
stands above what they measure.

One decision is open for the person who decides what ships: the bar a text must clear before it
ships. Today's rule asks for two consecutive rounds with nothing blocking, and the file in hand has
not reached it. Three shapes stand ready. The first is zero places for both readers. The second is
zero places by agreement. The third is shipping with the remaining stops listed at the text's head.
Repairs and reading rounds go on while this is open. No file is called finished until it is
answered.

## Forward queue

1. Get `bash guardrails/pre-push` to green and push. The test gate, the skill-review records, the
   frozen baselines and the findings record all need work first.
2. Lower the recorded finding counts to what the files now measure:
   `python3 scripts/rule-census.py --json guardrails/rule-census.json`.
3. Repair the places both readers of the last round stopped at, listed in
   `docs/measure/2026-07-29-reader-tier-comparison.md`. Then run the next round as one strong
   reader and one cheap reader.
4. Split the three language rules that mix a part a script can decide with a part a reader has to
   judge. `guardrails/language-rules.json` holds 63 rules (`grep -c '"id": "r' <that file>`). By its
   `owner.by` field, 18 belong to a script, 42 to the reading agent, and 3 await the division.
5. Generate the rule totals that three documents state by hand. The readability plan says 54,
   `docs/language-defects.md` says 53, and `docs/language-worked-example.md` says 39, against 63 in
   the rule home.
6. Take the test fixtures and the templates for other projects out of the reading queue. Nobody
   reads them, and removing them is the largest cut available on the estimated hours.
7. Re-seed the estimate of rounds per file once a second file has been carried through. Every hour
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
