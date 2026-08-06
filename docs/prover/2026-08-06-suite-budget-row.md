# Prover check — the suite budget row's raised ceiling, 2026-08-06 10:56

Independent check of `ARCHITECTURE.md`'s full suite wall-time budget row. The row moved from
≤ 420 s to ≤ 470 s. The old figure measured 383–405 s at 1,856 tests. The new figure measured
456 s at 2,404 tests, with the meta-test alone costing 282 s. This record is written by a seat
that made none of the edit (SPEC INV-237).

The brief named commit `30b1d31` as the row's author. `git show 30b1d31 -- ARCHITECTURE.md`
comes back empty. That commit touches a 2026-08-05 prover record instead. `git log --
ARCHITECTURE.md` names the real author. It is `ef0f0a0`, titled "The suite budget reads its
measured figure at 2404 tests, and the fat gets a row" (2026-08-06 10:41:05 +0300). This check
reads `ef0f0a0`.

Four questions were asked of this check, each judged on evidence gathered directly. Is the
measurement true. Is raising the ceiling lawful here. Does the row still state a real bound. Is
the 282 s figure right.

## Method

Read `git show ef0f0a0 -- ARCHITECTURE.md` and `-- ROADMAP.md` for the delta itself. Read the
row's full history with `git log -p --follow -- ARCHITECTURE.md | grep "full suite wall-time"`,
six stated values across the file's life. Ran `guardrails/check-suite-budget.sh` against the
supplied run log.

Read the project's down-only ratchet family: Requirement 221 criterion 3, the general
lock-mechanism menu (INV-98); the size ratchet (INV-264); the node-file cap (INV-233). Read the
debt cap too, Requirement 132 criterion 1 (INV-164, INV-98).

Read those against the suite wall-time budget's own governing text: the "## Quality budgets"
section header, Requirement 121, and Requirement 226 criterion 3. Read `ROADMAP.md` row 553.

Timed `tests/test_guardrails.py::TestGateB_Tests` independently, as a cross-check on the 282 s
figure. The coordinator supplied its own directly-measured figure mid-check. It asked this
record to carry that figure as the seat's own. This check's slower concurrent run stands beside
it instead of replacing it.

## What was checked

- `ARCHITECTURE.md`'s budget row, before and after, via `git show ef0f0a0 -- ARCHITECTURE.md`.
- The run log `suite5.log` (35 lines) and its tail line.
- `guardrails/check-suite-budget.sh`, run against that log.
- The row's full history: six stated values. `≤ 60 s` carried no measurement. `≤ 470 s` is this
  move. Each value was read with its own test count and measured figure.
- `PRODUCT_SPEC.md` Requirement 221 (`## Requirement 221: Every process converges on a goal
  named as an artifact`), criterion 3.
- `PRODUCT_SPEC.md` Requirement 132 (`## Requirement 132: Compaction is continuous, a gate on
  every push`), criterion 1. The debt cap is an explicit down-only instance.
- `PRODUCT_SPEC.md` Requirement 121 (`## Requirement 121: The architecture owes numbers, not
  just names`), both criteria.
- `PRODUCT_SPEC.md` Requirement 226 (`## Requirement 226: The push gate derives its reach from
  the diff`), criterion 3. This is the wall-time budget's own governing clause.
- `ARCHITECTURE.md`'s `## Quality budgets` section header, the sentence directly above the
  table.
- `ROADMAP.md` row 553.
- The coordinator's own timed run of `tests/test_guardrails.py::TestGateB_Tests`, 10:36 today:
  `2 passed in 282.18s (0:04:42)`. This check's own concurrent run of the same class: `2 passed
  in 306.28s (0:05:06)`.

## Findings

Zero blocking. Four judgments follow.

### 1. Is the measurement true — yes

The log's tail line reads `2404 passed in 456.18s (0:07:36)`. That matches the row's stated
figure exactly: 456 s at 2,404 tests. `guardrails/check-suite-budget.sh` against the supplied
log returned, exit 0:

    OK (suite budget): measured 456.18 s within the stated 470 s (ARCHITECTURE.md, full suite wall-time).

### 2. Is raising the ceiling lawful here — yes, plainly

The project does hold a down-only law. It binds a narrower, separately-named family than every
numeric cap in the project. The suite wall-time budget sits outside that family.

Requirement 221 criterion 3 states the general principle. A process that reaches a level locks
it by a mechanism.

Four mechanisms are named: a norm template, a conformance test, a lint floor that only rises,
and "a cap that only ratchets down."

The requirement offers these four as a menu of lock mechanisms. No numeric cap in the pack is
bound to the fourth kind by default.

Three concrete instances pick the ratchet-down mechanism explicitly, each in its own
acceptance-criteria text.

The size ratchet carries its own case heading: "the ratchet moves only down."

Its own criterion reads: "*if* a delivery's new bytes-per-criterion is above the recorded
bound, *then* the ratchet gate *shall* red" (INV-264).

The node-file cap reads "*shall* red any increase while the cap ratchets down only" (INV-233).

The debt cap, Requirement 132 criterion 1, reads "the debt cap ratcheting down only" (INV-164,
INV-98).

Each of the three calls itself a ratchet in its own text. Each states its own down-only behavior
in its own criterion.

The suite wall-time budget's governing text carries neither shape. `ARCHITECTURE.md`'s
`## Quality budgets` header stands directly above the table this row lives in. It reads: "What
quality means for a skill pack, in numbers." Numbers are "proposed by the agent, **tunable on
the human's word**" (INV-70). Requirement 226 criterion 3 is the criterion
`check-suite-budget.sh` implements. It says a full run reds "on an overrun naming both figures"
(INV-41, INV-164). It carries no down-only clause.

Requirement 121, the budgets requirement itself, calls the numbers "the host's taste, proposed
by the architecture and set on the human's word."

Again, no down-only clause appears.

The wall-time criterion does carry INV-164. That code names a different principle: any
machine-verifiable quality gets wired as a blocking gate, held by no pass's attention.
Requirement 132 is that principle's own home. The claim is that the check exists and runs on its
own. It says nothing about which direction the stated number may move.

The row's own text states its actual practice. It moves with the fresh measured figure each
time the suite grows. Six data points bear this out, and every one moved the ceiling upward.
Each move ties to test-count growth or to a stated correction:

- `≤ 60 s` — no measurement stated.
- `≤ 180 s` — measured 92–97 s at 940 tests.
- `≤ 360 s` — measured 281–302 s at 941 tests, a correction. The earlier figure "did not reflect
  a serial full run."
- `≤ 380 s` — measured 322–373 s at 1,809 tests, the 4.0.0 migration.
- `≤ 420 s` — measured 383–405 s at 1,856 tests, the row-456 format landing.
- `≤ 470 s` — measured 456 s at 2,404 tests, this move.

This move continues that practice exactly. The suite grew from 1,856 to 2,404 real tests. The
fresh measurement, 456 s, exceeded the old ceiling of 420 s. The new ceiling sits 14 s above the
fresh measurement. That headroom matches the two prior moves: 15 s, then 7 s.

Verdict: lawful. The down-only ratchet law binds a distinct, self-declared family: the size
ratchet, the node-file cap, the debt cap. This row is not a member of that family. It is a
tunable quality budget under Requirement 121, Requirement 226, and INV-70. This move is the
row's own stated, repeatedly-exercised practice. It raises no ceiling past its own law. This
finding does not block.

### 3. Does the row still state a real bound — yes, narrowly, with row 553 still queued

The ceiling sits with headroom above the fresh measurement. It carries a buffer: 14 s here,
then 15 s and 7 s at the two prior moves. An unexplained slowdown on the same test count would
still red today, ahead of any human-authored move. The mechanism gives the number no path to
silently track every run on its own. Every widening step so far has needed a dated, reasoned,
human-authored commit naming a real cause. The row bounds something real: regression between
landings, apart from the suite's absolute cost.

The six-move history runs one way in practice. Nothing has yet pulled the ceiling down.
`ROADMAP.md` row 553, "The suite-in-suite test proves the runner without re-running everything,"
queued 2026-08-06, is a real, scoped counterweight. Its Done-when criteria are concrete. The
meta-test must prove its verdicts against a narrow, real test selection alone. The measured
wall-time with the meta-test firing must drop under 300 s. The budget row in `ARCHITECTURE.md`
must move down to the fresh figure.

The row sits queued today. Building it is still ahead. Six moves ran the ceiling up so far, and
one queued item aims to bring it back down. That gap is worth naming plainly. Neither
Requirement 121 nor 226 obligates a downward trend for this budget class, so this stands as an
honest state. Row 553 already carries the counterweight, queued.

### 4. Is the 282 s figure right — corroborated by two runs, short of a matched reproduction

The coordinator measured `tests/test_guardrails.py::TestGateB_Tests` directly at 10:36 today.
The result: `2 passed in 282.18s (0:04:42)`. This record carries that as the coordinator's own
measurement.

This check had independently started a concurrent timed run of the same class before that
figure arrived. This check let it run to completion, on a machine sharing load with other work
at the time. That run read `2 passed in 306.28s (0:05:06)`.

The row's own figure names its condition as "on an idle machine."

The two runs agree within about 8% and land in the same order of magnitude. That agreement
corroborates the 282 s figure as plausible. An independent reproduction to the second, under
matching idle-machine conditions, is a separate claim this check does not make.

## Verdict

Confirmed as claimed, with zero blocking findings. The 456 s measurement at 2,404 tests is true.
It reads from the log's tail line and passes `guardrails/check-suite-budget.sh`.

Raising the ceiling to 470 s is lawful. It follows the row's own six-times-stated practice. It
follows the tunable-budget law: Requirement 121, Requirement 226 criterion 3, INV-70. It stands
outside the project's separately-named down-only ratchet family: the size ratchet, the
node-file cap, the debt cap.

The row still bounds a same-size-suite regression. Its six-move history runs one way. Row 553,
the queued counterweight aimed at pulling it back down, has not yet landed.

The 282 s meta-test figure is the coordinator's own direct measurement. An independent
concurrent run corroborates it, landing in the same range.

## Reach

Files read directly: `ARCHITECTURE.md`, the budget row and the `## Quality budgets` header, at
`ef0f0a0` and its parent. The full row history via `git log -p --follow`. `ROADMAP.md`, row 553,
via `git show ef0f0a0 -- ROADMAP.md`. `PRODUCT_SPEC.md`, Requirements 121, 132, 221, 226.
`guardrails/check-suite-budget.sh`, run against the supplied log.

Commits read: `ef0f0a0`, the row's actual author, and `30b1d31`, ruled out as the wrong commit.
Log read: the supplied `suite5.log`.

Tests run: `tests/test_guardrails.py::TestGateB_Tests`, this check's own run, independent of and
concurrent with the coordinator's.

Read for form and precedent: `docs/prover/2026-08-05-pin-repoint-check.md`,
`docs/prover/2026-08-06-spec-table-regeneration.md`.
