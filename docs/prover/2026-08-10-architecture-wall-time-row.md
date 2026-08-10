# Prover record — the architecture's wall-time row, 2026-08-10

Re-check of `ARCHITECTURE.md` against the tree, covering the change it took in commit `740dc0f`,
"Four published numbers come back to what the tree holds, and the resume is written for a clean
start". Root: Alexander's word of 2026-08-10 20:30 to commit the previous seat's finished work, and
the standing habit of pushing on green.

The push gate wants a committed prover record that is at least as new as the last `ARCHITECTURE.md`
change (SPEC M-6, INV-116, read out by `guardrails/check-prover-record.sh`). `740dc0f` moved the
architecture and the newest committed record predates it, so the gate is armed and this pass answers
it.

Verdict: every number `740dc0f` changed in `ARCHITECTURE.md` matches what the tree holds today. One
sibling number in a resume file has gone one behind the tree, recorded below as a minor finding.

## What the commit changed in the architecture

`git show 740dc0f -- ARCHITECTURE.md` returns one line, the full suite wall-time row at line 878. One
figure inside it moved: the test count the budget is stated over went from 2,502 to 2,492. Every
other figure in the row stayed where it was, including the two historical counts the row keeps on
purpose as the readings it replaced.

The commit's message names four published numbers. Three of them live outside the architecture, in
`NEXT_STEPS.md` and under `.live-spec/`. They are re-checked at the end of this record for
completeness, and they carry no weight in the architecture gate.

## Each changed number, re-derived

### 2,492 tests — matches

The row states the budget over "one full `python3 -m pytest -q` run at 2,492 tests with the
suite-in-suite meta-test firing".

Counted two ways from the tree at this commit. `python3 -m pytest -q --collect-only` reports 2492
tests collected. A real full run reports `1 failed, 2491 passed in 463.51s`, which is 2492 tests
executed. The one red is `tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`,
the prover-record gate this record exists to answer, and it turns green once this file is committed.

The count the row replaced, 2,502, no longer describes the tree. The gap of ten is the handover
provenance check and its cases, retired earlier in the campaign. So the change was owed and its
direction is right.

## The rest of the row, re-checked

The row is the unit the reader acts on, so the figures beside the changed one were re-derived as
well.

### The bound of 605 s — holds, with 141 s of headroom

`guardrails/check-suite-budget.sh` reads this row by grepping for the literal string
`| full suite wall-time |` and pulling the first `≤ <int>` figure out of it. Run by hand against the
row as it stands, that parse returns 605.

Today's full run measured 463.51 s of serial wall-time. Running the budget check over that run's own
log returns `OK (suite budget): measured 463.51 s within the stated 605 s`. The bound holds and the
run sits 141.49 s under it, which is the load headroom the row says it was derived to carry.

### The meta-test at near 282 s — holds, and measures 292.0 s today

The row states that the meta-test alone takes near 282 s of the run, which is the sentence that
justifies a smaller diff skipping it and finishing far shorter.

Measured today with `--durations=15` over the same run. The suite-in-suite work sits in two cases of
`tests/test_guardrails.py::TestGateB_Tests`: `test_real_content_passes` at 147.69 s and
`test_broken_suite_fails` at 144.33 s. Together they are 292.02 s, which is 63 per cent of the whole
run. The stated figure is hedged as an approximation and 292 s sits inside that hedge, so the
sentence stands. A later seat that wants the tighter figure has today's measurement here.

### The pointers the row names — all resolve

- `guardrails/check-suite-budget.sh` exists and reads the pytest tail line, as the row says.
- `guardrails/doc-bounds.json` exists, and its comment records the same seeding habit the row cites:
  a measured size plus stated headroom.
- M-346 is registered in `TEST_MATRIX.md` at line 571, marked built, and its stated behaviour is the
  behaviour the script has.
- Queue row 553 exists in `.live-spec/day1-queue-for-striking.md` at line 104, reading "Stop one slow
  test from re-running the whole suite to prove itself". That is the work the row says brings the
  number down by narrowing the meta-test's own run.
- The command the row names is the command both nets run. `.github/workflows/gates.yml` runs
  `python3 -m pytest -q`, and `guardrails/check-tests.sh` runs the same line, with a comment saying
  the two must match.

### The historical readings the row keeps

The row keeps three earlier readings so a reader can see the direction: 474 s at 2,502 tests on
2026-08-07, 470 s at 2,404 tests on 2026-08-06, and 383–405 s at 1,856 tests on 2026-07-24. These are
records of runs that happened, and a later tree cannot reproduce them. They were left alone by
`740dc0f`, which is the right treatment, and the day 1 sweep reached the same reading at
`docs/push-review/2026-08-09-the-culling-first-day.md:149`.

## The three sibling numbers, for completeness

These sit outside `ARCHITECTURE.md` and outside the gate this record answers. They are reported here
because the same commit moved them.

### Minor finding — the commit count in the resume is one behind the tree

`740dc0f` rewrote the resume line to read "Commits since the last push of 2026-08-07: 26, all local."
`git rev-list --count ba479b6..HEAD` returns 27, and it returned 27 at `740dc0f` as well, since that
commit is itself one of them.

The line was true while it was being written and went one behind the moment it landed. The commit's
own purpose was to stop a published number from going stale, so the shape is worth naming even
though the drift is one. A count that includes the commit carrying it has to be written as such, or
left to a command.

This is a resume file, no gate reads the figure, and the repair belongs to whoever next touches the
live-state block.

### The install measure of 218 — outside this pass

`.live-spec/day3-opening-2026-08-09.md` now reads 218 references pointing at nothing on the short
path, down from the 219 the day 1 census took at `.live-spec/day1-measures-2026-08-09.md:11`.

The census method scans the installed tree under the home directory, which sits outside this
repository and outside this pass. The arithmetic the commit gives is coherent: the retired check took
one counted reference with it. The figure itself is left unverified here and says so.

### The 16 per cent target — a plan figure, unchanged by this commit

The resume carries the day 1 finding that the plan's criterion protects 26 of the 35 rules, so
deleting the rest moves 3.7 per cent. That figure was established and reviewed on 2026-08-09 in
`docs/prover/2026-08-09-redrawn-rule-verdicts.md` and no architecture claim rests on it.

## Verdict

The architecture matches the tree. The one number `740dc0f` changed, 2,492 tests, is what the tree
runs, counted by collection and by a real run. The bound of 605 s holds with headroom against a
measured 463.51 s. The meta-test figure holds at a measured 292.0 s. Every script, matrix code and
queue row the changed row names resolves to something real that says what the row claims it says.

Nothing in the architecture blocks the commit or the push.

One minor finding stands, in a resume file, against a number no gate reads.

## Reach

Read whole: the wall-time row at `ARCHITECTURE.md:878`, `guardrails/check-suite-budget.sh`,
`guardrails/check-prover-record.sh`, `guardrails/check-tests.sh`, and
`docs/prover/2026-08-09-redrawn-rule-verdicts.md` as the model for this record's form.

Read in part: `.github/workflows/gates.yml` at its pytest step, `TEST_MATRIX.md` at M-346,
`guardrails/doc-bounds.json` at its comment and its four entries, `.live-spec/day1-queue-for-striking.md`
at row 553, `.live-spec/day1-measures-2026-08-09.md` at its measures table, and
`.live-spec/day3-opening-2026-08-09.md` at the install measure.

Commands run: `git show 740dc0f -- ARCHITECTURE.md` and `git show --stat 740dc0f`;
`git rev-list --count ba479b6..HEAD` and the same against `740dc0f`; `python3 -m pytest -q
--collect-only`; a full `python3 -m pytest -q tests --durations=15`; the budget row's own parse by
hand; and `guardrails/check-suite-budget.sh` over the run's log.

Not verified: the install measure of 218, which counts the installed tree outside this repository.
The three historical wall-time readings the row keeps, which are records of past runs.

Files written by this pass: this record alone. The working tree also carries the day's routine
regeneration of `docs/PROGRESS.md` and `guardrails/progress-baseline.json`, which is a date bump with
the finding totals unchanged at 4876 and 22 documents at zero.
