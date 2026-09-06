# Prover record — 2026-09-06 the closure kernel, and the board this push publishes

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 (pack bindings) and `skills/live-spec-base/SKILL.md`.
This pass was run from a seat that authored none of the two commits below, briefed to find reasons
to refuse them.

Range: aa361dea..9edf7c25
- 9edf7c25 Adversarial push review of aa361dea..7993fa9b: the closure kernel's bypass and the
  board's public lie, both closed — this pass's own fixes, tests and this record
- 7993fa9b Trusted closure kernel, statement validation, a truthful board, and its public link
- 4a1579d0 Director reads and routes; build-pipeline owns accepted work (q-822, q-823, q-816, q-385)

The two commits under review are the first two. `9edf7c25` is this record's own landing: the
repairs the findings below name, their tests, the re-pinned q-816 row and this file. It is read
here the way any commit in the range is — the fixes were each proved red first against 7993fa9b,
and nothing in it changes behaviour the findings do not describe.

Files read: `spec/work-board.md` (Requirement 309, whole), `spec/live-status-reporting.md`
(Requirement 257, both versions), `spec/public-contract.md`, `.live-spec/turnkey-contract-composed.md`
(sections 3 and 4, the T1–T9 transition table), `scripts/task-admission.py` (whole, 1112 lines),
`scripts/plan_checks_core.py` (`evaluate`, `reads_outside_the_tree`, `run_key`),
`scripts/checkpoint.py` (`close_checkpoint`), `scripts/render-board.sh` (whole),
`scripts/open-lane.sh`, `scripts/state-probe.sh`, `scripts/state-probe-extras.sh`,
`.github/workflows/pages.yml`, `skills/build-pipeline/references/accepted-work-execution.md`
(whole), `matrix/work-board.md`, `PLAN.md` (q-816's row), `PRODUCT_SPEC.md`, `ARCHITECTURE.md`,
`.live-spec/escort-inventory-R7-2026-08-11.md`, `guardrails/check-prover-record.sh`,
`guardrails/check-landing-next-steps.py` (the deleted one, at `origin/main`),
`guardrails/check-next-steps-boundary.py`, `docs/queue-archive/rotated-PLAN-2026-09-06-q385-no-producer-declined.md`,
`attic/MANIFEST.md`, `attic/spec-public-contract-R194-C15.md`, `tests/test_task_admission.py`,
`tests/test_statement_validation.py`, `tests/test_board_publish.py`, `tests/test_work_board.py`,
`tests/test_priority_order.py`.

Checks run: four targeted pytest runs (392 passed, 2 skipped), the board rendered four ways and diffed, the pin-drift and spec-style gates, the three index builders, and the acceptance command of every row this pass edited code for — each with its result below.
- `python3 -m pytest -q tests/test_task_admission.py tests/test_statement_validation.py` — 68 passed
  (the three new refusal tests among them, each red first against 7993fa9b).
- `python3 -m pytest -q tests/test_task_admission.py tests/test_statement_validation.py
  tests/test_priority_order.py tests/test_traceability.py tests/test_board_matches_the_canon.py
  tests/test_tasks_parser_finds_every_task.py tests/test_next_steps_boundary.py` — 293 passed, 2 skipped.
- `python3 -m pytest -q tests/test_work_board.py` — 26 passed.
- `python3 -m pytest -q tests/test_board_publish.py` — 5 passed (the new one among them).
- `bash scripts/render-board.sh --json`, run four ways — as this machine, with `HOME` pointed at an
  empty directory, the same with the interpreter's site-packages restored, and with
  `LIVE_SPEC_BOARD_CHECKS=off` — and the four models diffed card by card. This is the measurement
  F2 rests on.
- `bash guardrails/check-pin-drift.sh` — 193 pins, clean; `python3 scripts/spec-style-lint.py --gate`
  on `PRODUCT_SPEC.md`, `spec/work-board.md`, `spec/live-status-reporting.md` — all clean.
- `python3 scripts/build-index.py PRODUCT_SPEC.md`, `build-matrix-reference.py`,
  `build-architecture-reference.py` — all three rebuilt; no index content moved.
- Each acceptance command of the rows whose code this pass edited: q-807, q-166, q-823, q-819,
  plan-10 — all exit 0. q-816 and q-537 exit 1, both already failing at 7993fa9b before this pass
  touched anything.
- The full suite was NOT run here; it runs after this record lands.

Findings: two blocking defects, three further defects, and four recommendations. Both blocking
defects are closed in this same commit; every fix carries a test that was red against 7993fa9b
first. Two things worth saying that worked: the DOD hash and its `correct --source --reason` door
are genuinely airtight against a hand edit, and q-385's retirement is unusually complete — the
criterion, its `[target]` marker, its traceability owner, its two matrix rows and a test docstring
all moved together, and a sweep for live references to R194 C15 across the spec, the indexes, the
matrix and the tests found none.

F1 (blocking, closed) — the trusted closure kernel stops holding the moment the checkpoint is not
open, and two legal moves reach that state.

> "`close` reads that receipt rather than any agent's sentence. It refuses when there is none" —
> `skills/build-pipeline/references/accepted-work-execution.md`, "The trusted closure kernel"

The whole kernel — the receipt's presence, its verdict, the frozen done's hash, the tree hash —
sat inside `if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open"` at
`scripts/task-admission.py:870` (7993fa9b). T9 `abandon` closes the checkpoint and marks the row
⬜; `hold` read only the mark, so it took the row back up under a new holder; `close` then found a
checkpoint that was not open, skipped every arm, and wrote ✅. Run end to end in a scratch tree:
admit → validate → hold → abandon → hold → close produced a row marked done with no receipt, no
verdict, no frozen done and no tree — the exact "textual claim by an agent" the kernel's tenth
clause names. Closed: the kernel now runs against the checkpoint's content whenever the file
exists, and only the two writes that finish an open checkpoint stay behind the status test
(`scripts/task-admission.py:931-958`); and `hold` refuses a ticket whose checkpoint stands closed,
pointing at T8 `reopen` as the one door back (`:738`). T7's stated crash-recovery no-op is
unaffected and still passes its own test — the receipt that closed the checkpoint the first time
is still in it, and every write recovery repeats lands in the checkpoint directory, which the tree
hash leaves out. Red-proved by `test_an_abandoned_ticket_is_not_taken_back_up_while_its_checkpoint_stands_closed`
and `test_a_close_over_a_closed_checkpoint_that_carries_no_receipt_is_refused`.
`defect · trusted-close-bypassed (safety)`

F2 (blocking, closed) — the board published at the project's one public link shows landed work as
reopened, and this push is what puts it in front of a reader.

> "bash scripts/render-board.sh _site/board.html" — `.github/workflows/pages.yml`, the render step

`scripts/render-board.sh:365` (7993fa9b; `:378` now) calls `evaluate(tasks)`, which executes every row's real
acceptance command and turns a ✅ row whose command fails into 🔁, "was done and is not". The Pages
job runs that same renderer on a bare `ubuntu-latest` checkout carrying neither the installed pack
nor the suite's dependencies. Measured against this tree's own PLAN.md: 29 rows the plan records as
landed drew as 🔁, and `column_of` stood every one of them in the in-work column — the done column
fell from 83 rows to 54, in-work rose from 2 to 31. Installing the missing dependency does not fix
it: with the interpreter's site-packages restored, 19 rows still flipped. The page is published at
`https://happysasha18.github.io/live-spec/board.html` on every push to main, so a person opening the
link sees 31 rows announcing that finished work came undone — a verdict about the runner, dressed
as a verdict about the work, on the surface this commit calls a truthful board. Requirement 309
criterion 22 asks the opposite: an open row's column is read off "the status its queue row records."
Closed, in two places. The published render now reads the recorded marks: `render-board.sh` honours
`LIVE_SPEC_BOARD_CHECKS=off` by blanking each row's command before `evaluate` — the same code path
the reader already had for a row with no command — and the page's own stamp line then tells its
reader that the acceptance commands are re-run on the machine that holds the work, not there;
`pages.yml` sets that variable on the render step. Separately, in `evaluate` itself, a failing key
that `reads_outside_the_tree` — a function already in the file, whose own docstring names this exact
class — no longer reopens a landed row: it keeps its mark and carries the reason as its note, since
a machine that does not hold the state returns unknown, and unknown is not false. Red-proved by
`test_the_published_render_reads_the_recorded_marks_and_says_so` (`tests/test_board_publish.py`) and
`test_a_key_that_reaches_outside_the_tree_never_reopens_a_landed_row` (`tests/test_priority_order.py`);
the pre-fix bytes were re-read out of 7993fa9b to confirm both assertions failed there.
`defect · published-state-contradicts-the-record (safety)`

F3 (defect, closed) — the lane cap the contract and the spec both bind take-up to was read nowhere,
and the matrix called the clause built.

> "holder named; lane cap not exceeded; no checkpoint already open for this id" —
> `.live-spec/turnkey-contract-composed.md`, section 4, T2's "Code requires" cell

`hold` checked the holder and the open checkpoint and never the cap. `hold --lanes 9` was accepted
and wrote "lane decision runs 9" onto the delivery trail, and any number of rows could stand in hand
at once — while Requirement 309 criterion 27 splits the in-work column into exactly `lanes.cap`
lanes, so a row past the cap is a row the board has no lane to stand it in. Requirement 309
criterion 47 states the same bound from the other side. `matrix/work-board.md` M-535 carried "the
steps running together inside one task are bounded by the same lane cap" as *built*, and its two
named tests assert the divergence line and nothing about the cap. Closed: `hold` reads the cap from
the `lanes.cap` profile line `scripts/open-lane.sh` and `scripts/render-board.sh` already read, and
refuses a lane decision past it and a take-up that would put more rows in hand than there are lanes;
with no lane decision named, the cap makes it, and the divergence line then says the plan expected
more. M-535 now names the test that proves the cap half. Red-proved by
`test_a_take_up_past_the_lane_cap_is_refused`.
`defect · unenforced-declared-bound (invariant)`

F4 (defect, closed) — the one open row's own pins address a file that no longer exists in that shape,
and it is the resume point.

> "`scripts/task-admission.py:305` (`block`), `:342` (`unblock`), `:367` (`park`), `:385` (`close`)"
> — `PLAN.md`, q-816's row, added by this push

All nine pins in that sentence are wrong at 7993fa9b, eight of them by four hundred lines or more:
`block` is at 790, not 305; `correct` at 743, not 285; `abandon` at 976, not 431. They address a
draft the file outgrew. q-816 is the only open row on the board, which makes it the resume point a
new session opens first, and each pin lands that session inside a different function than the one
named beside it — the exact failure the file's own `_pointers` docstring exists to stop ("an exact
address into a document that exists"). `check-pin-drift.sh` does not reach pins written in this
shape inside PLAN.md prose. Closed: all nine re-pinned against the file as it now stands and each
verified by reading the line back. No new gate was built for the class; the honest note is in R3
below.
`defect · stale-pin (traceability)`

F5 (defect, closed) — a duty carried on the owner's own dated word was retired with no sentence
saying where it went.

> "**HIS WORD** — roadmap row 433 … 'A landing that ships a movement refreshes the forward map in
> the same breath (Alexander's word, 2026-07-19…)'" — `.live-spec/escort-inventory-R7-2026-08-11.md`

This push deleted `guardrails/check-landing-next-steps.py` (450 lines) and rewrote Requirement 257
from "a delivery that closes a roadmap row refreshes the forward map" to "the resume file never
becomes a second board." The rewrite's reasoning is sound and recorded, and the replacement gate,
its tests and the template all landed together — this is a substitution, not a silent drop, and a
line-by-line walk of the old gate's checks against the new spec confirmed it. What was missing is
the reconciliation: the one page in the tree that records the duty's provenance still presented it
as live, with its middle column pinning a deleted file and a line range in `build-pipeline/SKILL.md`
that now says the opposite. Closed: R257's Context now names the superseded 2026-07-19 word and says
where it lands today — Requirement 309 criterion 88, the work board's update inside the landing's
own commit, the same duty on the surface that now holds the forward map — and the escort inventory's
row is marked retired 2026-09-06 with that pointer and a note that its pins are dead.
`defect · unreconciled-owner-word (provenance)`

R1 (recommendation, stands) — the published board can no longer show a genuinely reopened row. F2's
fix trades one lie for one silence: with the commands off, a ✅ row whose acceptance has really
stopped passing publishes as done. Measured on this tree today that is exactly one row, q-537,
against 29 false ones the other way. The page says in its own stamp line that the commands are re-run
on the machine that holds the work, so the reader is not misled about what they are looking at, and
the probe on that machine still raises the row. Living with the silence rather than building a
second verdict channel for the runner.
`recommendation · later · partial-signal (ops-ux)`

R2 (recommendation, stands) — `verify`'s producer bar reads the row's `**Holder:**` paragraph, and
T6 `park` deletes that paragraph. So hold → park → `verify --by <the producer>` → close accepts a
receipt the executor wrote for its own work, and the kernel's third clause is bypassed without a
single illegal move. Nothing in the tree durably records who produced a row's work — the checkpoint
records `Owner: pipeline` and nothing else — so closing this properly means giving the checkpoint a
place to keep the holders it has had, which is a new field and a new write on three transitions.
Out of scope for a review pass. Folds into q-816.
`recommendation · later · producer-bar-evadable (safety)`

R3 (recommendation, stands) — F4's class has no mechanical reach. `check-pin-drift.sh` walks 193
pins and none of them are the `path:line` citations written inline in PLAN.md's row prose, which is
where the pack keeps the pointers a resuming session opens first. Widening the drift check to that
shape is a real repair and a gate change; the pack's own standing rule is that no gate gets built
without an incident, and F4 is now that incident on record. Folds into q-816 rather than opening a
row of its own.
`recommendation · later · unreached-class (traceability)`

R4 (recommendation, stands) — two staleness alarms left `scripts/state-probe.sh` and
`scaffold/status-view/state-probe.sh` in this push with no line saying why. The `NEXT_STEPS.md`
alarm goes with R257's rewrite and needs no separate word. The director-eval alarm is not deleted —
the identical comparison lives on in `scripts/state-probe-extras.sh:15-20`, where a pack-specific
path belongs and where the scaffold shipped to hosts should never have carried it. What did change
is its weight: it was `warn` plus `ALARM=1` and is now a plain line in the FACTS block, so a
Director skill edited after the last eval run no longer raises the probe's alarm — and this push
rewrote that very skill. Restoring the alarm level is a one-line change in the extras file, left
for the owner's read since it is his probe's noise budget.
`recommendation · later · downgraded-alarm (ops-ux)`

R5 (recommendation, stands) — Requirement 309 criterion 45 ("keep a plan's deliverables to a
handful", retunable, standing at five) has no implementation: `floor_issues` counts no steps.
Criterion 44 likewise. Requirement 309 is marked `[target]`, and no matrix row claims either
clause, so this is unbuilt work rather than a false green — unlike F3, which had a row calling it
built. Folds into q-816, whose acceptance is the whole of Requirement 309.
`recommendation · later · unbuilt-criterion (completeness)`

R6 (recommendation, stands) — `scripts/render-board.sh:26` sets `-uo pipefail` without `-e`. It
does not matter today because the heredoc is the last statement and its exit code propagates, but it
is one added line away from swallowing a failure. Left alone: changing a shell script's error mode
under a review pass is a change nobody asked for, and the condition is stated here so the next edit
to that file knows.
`recommendation · later · shell-strictness (robustness)`

Class lens: swept. F1's class is "a kernel arm guarded by a state that another transition can leave"
— the other seven transitions were each re-read for the same shape, and `verify` carries the second
instance, reported as R2 rather than fixed. F2's class is "a check re-run on a machine that does not
hold the state it reaches for" — swept across the Pages workflow's only other step (the artifact
upload, which runs nothing) and across `state-probe-extras.sh`, which reads recorded scores rather
than re-running them. F3's class is "a contract cell naming a code requirement no code carries" —
T1's duplicate check, T2's open-checkpoint check, T4's three reason kinds, T5's named fact, T7's
empty IN PROGRESS and NEXT, T8's named false condition and T9's reason were each read against their
implementation and all seven are carried. F4's class is "a pin written against a draft" — the other
`path:line` citations added by this push (`architecture/*.md`, `matrix/work-board.md`,
`spec/work-board.md`) ride `check-pin-drift.sh`, which is clean; q-816's inline prose pins were the
only ones outside its reach.

Blocking: two, both closed.
- F1 the trusted closure kernel is bypassed whenever the checkpoint is not open — closed: the
  receipt, verdict, done-hash and tree arms now run against the checkpoint's content rather than its
  status (`scripts/task-admission.py:931`), and `hold` refuses a ticket whose checkpoint stands
  closed (`:738`); two tests, both red against 7993fa9b first.
- F2 the public board shows 29 landed rows as reopened — closed: the published render reads the
  recorded marks and says so on the page
  (`scripts/render-board.sh`, `.github/workflows/pages.yml`), and a key reaching outside the tree no
  longer reopens a landed row (`scripts/plan_checks_core.py`); two tests, both red first.
