# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-04)

The project is rewriting its own documents so that a stranger can read them, one queued file at a
time: two agents read the file cold, and every place both stopped is repaired.
`skills/text-audit/SKILL.md` is the file in hand, and six rounds have run on it.

A **reading** is one agent reading one file cold and filing a record under `docs/language-reads/`. A
**round** is two readings of one version of a file, one on the strong tier (`claude-opus-5`) and one
on the cheap tier (`claude-sonnet-5`); the tiers are named in
`docs/measure/2026-07-28-tier-routing-experiment.md` and the pairing was settled by
`docs/measure/2026-07-29-reader-tier-comparison.md`. A place counts against a text when both readers
of a round stopped there; one reader alone files it to `docs/language-defects.md` and blocks nothing.

Five commits landed on branch `main`: generated pages for the language rules, a wording check
that reads a quoted document as quotation, the progress and measurement pages, the findings filed
from the campaign, and this queue. The branch stands 21 commits ahead of `origin/main`
(`git rev-list --count origin/main..main`) and nothing has been pushed. Two files carry uncommitted
work: `attic/MANIFEST.md` changed, and `guardrails/language-rules.json.bak-pre-langsweep` is new and
untracked (`git status --porcelain`).

The last full test run finished 9 failing and 2302 passing (`python3 -m pytest -q`, log
`suite-run-2.log` in the session scratch directory). Two were this file and are repaired here.
Re-running the other seven gives 4 failing and 3 passing: two in `tests/test_config_health.py`, plus
`TestGateA_ProverRecord` and `TestGateB_Tests` in `tests/test_guardrails.py`.

Three push gates are failing. `guardrails/rule-census.json` is missing rows for four files under
`inbox/` (its `files` key read against `ls inbox/*.md`). No review record for today exists under
`docs/prover/` (`bash guardrails/check-prover-record.sh`). Russian text in two files under
`guardrails/measured-number-fixtures/` gives 5 offences (`bash guardrails/check-shipped-language.sh`).
The rendered-page sweep passes (`python3 guardrails/check-rendered-sweep.py`).

One decision is owed by the person who decides what ships: what bar a text must clear before it
ships. The rule today asks for two consecutive rounds with nothing blocking, and six rounds on the
file in hand never reached it. Three shapes stand ready: zero places for both readers; zero places by
agreement; or shipping with the remaining stops listed at the text's head. Repairs and reading rounds
continue while this is open, and no file is declared finished until it is answered.

## Forward queue

1. Add census rows for the four `inbox/` files, record today's review under `docs/prover/`, and mark
   the Russian passages in `guardrails/measured-number-fixtures/` as deliberate samples with the
   user-language fence `bash guardrails/check-shipped-language.sh` names in its fix line. Then push.
2. Repair the three places both strong readers of round six stopped at, listed in
   `docs/measure/2026-07-29-reader-tier-comparison.md`, plus the two the cheap reader found alone.
   Then run round seven as one strong reader and one cheap reader.
3. Split the three language rules that mix a part a script can decide with a part a reader has to
   judge. `guardrails/language-rules.json` holds 63 rules; 18 belong to a script, 42 to the reading
   agent, and 3 carry `"by": "split"` and wait for the division.
4. Generate the rule totals three documents state by hand: 54 in
   `docs/plans/2026-07-28-top-level-readability.md`, 53 in `docs/language-defects.md`, 39 in
   `docs/language-worked-example.md`, against 63 in the rule home.
5. Separate the test fixtures and the templates for other projects out of the reading queue. Nobody
   reads them, and removing them is the largest reduction available on the estimated hours.
6. Re-seed the estimate of rounds per file once a second file has been carried through. Every hour
   figure on the measurements page rests on `skills/text-audit/SKILL.md` alone.

## Where the numbers live

`docs/MEASUREMENTS.html` holds one row per file and one column per indicator, in the reading queue's
order, with the hours each file still owes and a note on each column saying what it counts and what
it aims at. Build it with `python3 scripts/measurements-table.py`, which also writes
`docs/MEASUREMENTS.md`. Every number stated to the person who decides what ships carries five things:
what it counts and in what unit; the decision it informs; what changes when it moves; the command
that produced it; and the value it aims at. A bare number is a defect of the same kind as an
undefined term.

## Rules you must not break

Several sessions share this repository. Stage files by name and never run `git add -A`. Read
`git log -1` before you write; when the commit it names differs from the one you recorded at the
start of your session, read what changed and run `bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs `git checkout -- <path>`,
`git checkout .`, `git restore` outside `--staged`, any form of `git stash`, `git reset` with
`--hard`, `--merge` or `--keep`, or `git clean` with `-f` or `-x`. To put a file back, write back the
bytes you read before you changed it.

Never give two workers the same file. Two workers held one file on 2026-07-29, and the second read
the first one's edits as an intrusion and reverted them. A test result is the printed count of passes
and failures: run `python3 -m pytest -q > <scratch>/suite.log 2>&1` and read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py --freeze
PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

`bash guardrails/pre-push` runs the whole push gate set, listed in `guardrails/README.md`. New
requirements, invariants and queue rows take the next identifier above the highest one in use in
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md`; read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask, publish
once the suite passes, and write documents in plain English. Before you ask the person who decides
what ships anything, check whether a document already answers it; if it does, act on that answer and
cite it. Say aloud whether a request is one-time or standing before acting.
