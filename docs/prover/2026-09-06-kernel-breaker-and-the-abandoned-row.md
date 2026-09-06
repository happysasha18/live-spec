# Prover record — 2026-09-06 the re-entry breaker, the pre-spawn gate, and the row a halt stranded

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 (pack bindings) and `skills/live-spec-base/SKILL.md`.
This pass was run from a seat that authored none of the work below, briefed to find reasons to
refuse it.

Range: 9407487d..f330d285
- f330d285 The published board names its publisher in the stamp, on every render from a runner — the one test the server's gates run reddened on a clone with no row in hand; one sentence in the records-only stamp
- b60fca2f The closure kernel holds on real rows; the readers cannot re-enter; the board's link is live — this record's own landing; the sentence that stood here before the commit existed said the head was pending
commits already on the branch and the whole working tree that will land beside them; the
coordinator fills the head sha in at commit time.

- e65ae0ee The review record names the fresh-clone render fix as the range's seventh commit
- e0a0f8f6 The published board tells the truth on a fresh clone, and the stable link's targets retire
- \<pending\> the uncommitted change under review — the repaired closure kernel, the re-entry
  circuit breaker, the pre-spawn gate, the statement floor for criteria 44 and 45, the probe and
  board mark semantics, the reader's answers kept as evidence, the execution reference's new rules,
  the pruned build-pipeline recordings, and the three rows closed through the kernel (q-816, q-823,
  q-822)

Files read: `PLAN.md` (the three closed rows whole, q-816's pin sentence, the three statements),
`scripts/task-admission.py` (whole, 1332 lines), `scripts/plan_checks_core.py` (`run_key`,
`refuse_reentry`, `evaluate`, `reads_outside_the_tree`), `scripts/plan_checks.py` (the whole key
table's diff), `scripts/render-board.sh` (the wrapper, `stamps`, `read_checkpoints`, `evaluate`'s
two call sites, `time_pair`, `trail_settlement`, `TRAIL_RE`, the stamp line),
`scripts/state-probe.sh` and `scaffold/status-view/state-probe.sh` (the note arm),
`scripts/checkpoint.py` (`write_atomic`, `new_checkpoint`, `update_checkpoint`,
`reopen_checkpoint`, `close_checkpoint`), `.live-spec/turnkey-contract-composed.md` (sections 3
and 4, the T1–T9 table whole, and the paragraphs under it), `spec/work-board.md` (Requirement 309
criteria 41–67, criterion 45's own sub-item), `skills/build-pipeline/SKILL.md` (whole),
`skills/build-pipeline/references/accepted-work-execution.md` (whole),
`.live-spec/checkpoints/q-816.md`, `q-822.md`, `q-823.md` (each receipt parsed and its verdict,
verifier, checks and hashes checked against the row), `matrix/work-board.md` (M-649, M-650),
`TEST_MATRIX.md`, `architecture/guardrails.md`, `evals/build-pipeline/README.md`,
`evals/build-pipeline/closing-scenarios.json`, `evals/director/README.md`,
`tests/test_task_admission.py`, `tests/test_statement_validation.py`,
`tests/test_plan_is_not_executable.py`, `tests/test_work_board.py`, `tests/test_board_publish.py`,
`tests/test_director_scenarios.py`, `tests/test_tasks_parser_finds_every_task.py`,
`guardrails/check-prover-record.sh`, `docs/prover/README.md`,
`docs/prover/2026-09-06-closure-kernel-and-the-public-board.md`.

Checks run: eight measurements and twelve pytest files, each with its result below. No probe and no render was started from inside an acceptance key at any point.
- `python3 -m pytest -q` over the twelve files this pass touched or reached —
  `tests/test_task_admission.py tests/test_statement_validation.py tests/test_checkpoint_mechanism.py
  tests/test_work_board.py tests/test_plan_is_not_executable.py tests/test_board_publish.py
  tests/test_tasks_parser_finds_every_task.py tests/test_director_scenarios.py
  tests/test_traceability.py tests/test_architecture_format.py tests/test_board_matches_the_canon.py
  tests/test_priority_order.py` — 433 passed, 2 skipped, 1 xfailed (the declared-stale closing pair).
- `LIVE_SPEC_EVALUATING=1 bash scripts/render-board.sh --json` — exit 3, one line, no page. Run
  again with `LIVE_SPEC_BOARD_RENDERING=1` set beside it — exit 3 again. This is the measurement F5
  rests on: the records-only nested path never ran.
- The dead end, run end to end in a scratch git tree: admit → validate → hold → abandon, then each
  of `hold`, `reopen`, `unblock` and `close` in turn — all four refused, the row stranded at ⬜ with
  a closed checkpoint. This is the measurement F1 rests on.
- `python3 -c` over the real `PLAN.md` through `task-admission`: each of q-816, q-822 and q-823
  read for its done source, its recorded hash and its holder — all three hashes match their text,
  q-816's done read off `**Acceptance:**` and the other two off `**Done when:**`, and no receipt's
  `by` is the row's own holder.
- `python3 -c` over `os.replace` — a file's `st_birthtime` after an atomic replace is not the one
  before it. This is the measurement F4 rests on.
- `shasum -a 256` over `skills/build-pipeline/SKILL.md` and its execution reference against the
  hashes `closing-scenarios.json` pins, and `wc -c` on both at HEAD and in the tree — the body
  matches its pin, the reference does not, and the run log's byte figures were 25 out.
- `bash guardrails/check-pin-drift.sh` — FAILED on two pins before this pass, 193 pins clean after.
- `python3 scripts/build-architecture-reference.py`, `build-matrix-reference.py`, `build-index.py`
  — all three rebuilt; only `TEST_MATRIX.index.md` moved, and it was already in the change.
- `bash scripts/state-probe.sh` — clean, no alarms, q-816 reads ✅ verified, q-537 reads 🔁 as it
  did before this range.
- `bash guardrails/check-prover-record.sh` — its non-range arms print OK (this file is uncommitted,
  so the arm that passes is the one over today's already-committed record).
- The full suite was NOT run here; it runs after this record lands.

Findings: three blocking defects, five further defects, six recommendations. Every blocking defect
is closed in the same tree, each with a test that was red first against the tree as it stood. Two
things worth saying that held up: the receipt kernel itself is airtight along every code path — the
missing-checkpoint arm, the missing-hash arm and the `**Acceptance:**` fallback each refuse exactly
what they claim to, proved by running them — and the re-entry breaker really does hold depth at one,
including for `--json` and for the renderer, which was the sharpest question this delta raised.

F1 (blocking, closed) — two legal moves strand a row where no transition can reach it, and the
refusal that strands it names a door that is locked.

> "T8 `reopen` is the one door back." — `scripts/task-admission.py`, `hold`'s closed-checkpoint arm
> (and `skills/build-pipeline/references/accepted-work-execution.md`, the take-up paragraph)

T9 `abandon` closes the checkpoint and leaves the row marked ⬜ in `## Tasks`. `hold` then refused it
— the arm the previous review added for F1 of that pass — and pointed at `reopen`. `reopen` opens
with `if mark != DONE: raise ... only a done ticket reopens`. Run end to end in a scratch tree:
after abandon, `hold`, `reopen`, `unblock` and `close` all four refuse, and the row stands ⬜ on the
board forever with a closed checkpoint nobody can reopen. The contract's T9 row says the ticket
leaves the list ("`in hand`/`queued` → archived"), which the code does not do — it rewrites the mark
and leaves the row in place — so the stranded state is reachable by the pack's own operations, not
by misuse. Closed: `hold` now reopens the sheet a halt left, writing into NEXT that the work resumes
rather than starts fresh (`scripts/task-admission.py`, the take-up arm); a done row is still refused
there and still sent to `reopen`, which is where the false condition and its evidence are recorded.
Nothing is bypassed by the change — the walk-past that arm was written for is shut at `close`, whose
kernel now runs unconditionally. The previous pass's test for that property was rewritten to hold it
end to end over the very sequence that broke it rather than by refusing the second take-up
(`test_an_abandoned_ticket_taken_back_up_still_cannot_close_without_a_receipt`), and two new tests
carry the new behaviour and its boundary (`test_an_abandoned_row_can_be_taken_up_again`,
`test_a_done_row_is_still_refused_and_still_sent_to_reopen`), each red first.
`defect · unreachable-state (liveness)`

F2 (blocking, closed) — the change reds a test its own landing wrote, on the surface that landing
is about.

> "the link stands once on the page, not repeated into a second home" —
> `tests/test_board_publish.py::test_one_canonical_url_in_the_registry_and_in_the_rendered_page`

This push writes into q-816's row prose: "The page answers at
`https://happysasha18.github.io/live-spec/board.html`". The renderer prints a row's own prose onto
its card, so the address then stands twice on the rendered page — once in the identifier line the
test requires it in, once inside a card — and the test counts two. Measured: the test fails on the
tree as handed over, and the same file's four other tests pass, so this is not a broken fixture.
Closed: the sentence now names the link the way the rest of the plan does, through `SURFACES.md`,
and says in its own parenthesis why it does not write the address out. No test changed.
`defect · self-reddened-gate (regression)`

F3 (blocking, closed) — the tree fails a push gate.

> "FAIL (pin drift): `scripts/plan_checks_core.py:135` (`read_priority_order` …) — the code has
> moved on" — `bash guardrails/check-pin-drift.sh` on the tree as handed over

The circuit breaker adds 27 lines near the top of `scripts/plan_checks_core.py`, which pushed
`read_priority_order` from 135 to 180 and `priority_rank` from 154 to 199. `architecture/guardrails.md`
still addressed the old lines, and `check-pin-drift.sh` — gate on the push road — refused. Closed:
both pins re-pointed and each verified by reading the line back; the gate now reports 193 pins clean.
`defect · stale-pin (traceability)`

F4 (defect, closed) — every close settles the estimate against a duration the code cannot measure,
and the three rows this push closes each ship it.

> "estimate 4–8 hours → actual 0.0 hours" — `.live-spec/checkpoints/q-816.md`, written by this
> push's own close

`_write_delivery_trail` read the actual as `st_mtime - st_birthtime` on the checkpoint file, and
every checkpoint write goes through `checkpoint.write_atomic`, which renames a fresh file over the
old one. A rename gives the new file a new creation stamp, so the two stamps are always the same
instant and the span is always zero, however long the work ran — proved directly by replacing a file
and comparing its birth stamps. All three rows closed today carry `actual 0.0 hours` against
estimates of 4–8, 6–10 and 8–14 hours. The renderer reads the same stamps at `scripts/render-board.sh`,
so a card said "took 0 min" and an in-work row said "standing since" whenever its sheet was last
written. The fixture that proves M-536 wrote `os.utime(path, (now, now))` under a comment reading
"Set them a known hour apart", and its assertion was only that the actual is truthy — `"0 min"` is
truthy, so the row read *built* on a measurement that was zero by construction. Closed: the open time
is now RECORDED rather than inferred — `admit` writes one `OPENED: <iso>` line into the checkpoint,
`_write_delivery_trail` reads it, and a checkpoint carrying none settles `actual not recorded` rather
than a number nobody wrote; the renderer prefers the same recorded line over the file's stamps. The
three shipped trail lines are corrected to `actual not recorded`, which is what those three rows can
honestly say — their sheets predate the line. Red-proved by
`test_the_close_reads_the_actual_off_the_recorded_open_time` and
`test_a_close_with_no_recorded_open_time_says_so_instead_of_printing_zero`
(`tests/test_statement_validation.py`), and by tightening M-536's own assertion to the hour its
fixture records, which read `0 min` before the fix.
`defect · fabricated-measurement (safety)`

F5 (defect, closed) — the breaker's graceful half never runs in the one case it exists for.

> "a render that finds it already set reads the plan's recorded marks instead of re-running the
> acceptance table … The chain therefore ends one level in." — `scripts/render-board.sh`, the wrapper

Two breakers were added, and they disagreed. `run_key` marks every acceptance command with
`LIVE_SPEC_EVALUATING`, and `evaluate` exits 3 under that mark. The renderer's own wrapper looked only
for `LIVE_SPEC_BOARD_RENDERING`. A render started by a key therefore arrives carrying *both*, sets its
checks off — and then dies at `evaluate` anyway, because the mark is still set. Measured: exit 3 with
either marker alone and with both, no page written, `--json` the same. So the records-only branch, the
`LIVE_SPEC_BOARD_NESTED` stamp line the page prints, and the test that covers them
(`test_a_render_started_by_a_render_runs_no_acceptance_command`, which sets `LIVE_SPEC_BOARD_RENDERING`
by hand with no evaluating mark — a combination nothing in the tree produces) all describe behaviour
that cannot happen. Depth one was never at risk; the honesty of the page's own stamp was. Closed: the
wrapper reads either mark as the same signal, and a records-only render drops the evaluating mark it
inherited, since with its checks off it starts no key that could need it. Red-proved by an added arm on
`test_a_key_that_renders_the_board_cannot_recurse`, which now requires the inner render to have
produced a page saying it was drawn inside another render; it failed with "produced no page" first.
`defect · unreachable-branch (robustness)`

F6 (defect, closed) — the eval run log names evidence that exists nowhere, and its numbers are wrong.

> "recordings 21, 22, 23 and 25 are kept whole under `recordings/2026-09-06-pair-11/` …" —
> `evals/build-pipeline/README.md`, added by this push

`evals/build-pipeline/recordings/` does not exist in the tree at all: this push deletes the eight
committed pair directories, and pairs 11 to 13 were never committed — `git log --diff-filter=A` finds
no commit that ever added them. So the paragraph above names four directories that are in neither the
tree nor git history, and the section that closes the file — "Only the pair the record names lives
under `recordings/`" — is false in the other direction, since nothing lives there. `closing-scenarios.json`
repeats the same claim five times in its `judgment_read`. Separately, the log records the signature
fold as taking `SKILL.md` from 8,065 to 8,090 bytes; the file went 8,040 → 8,065, so both figures are
25 out. And the staleness note names two paragraphs as having moved after the recording — the
round-two rule and the brief's lead line — where four did: the estimate-basis rule and the pre-spawn
paragraph moved too, and the reference stands at 20,147 bytes against the 18,734 the runs were graded
at. The declaration itself is sound and the suite's stale arm is doing its job (one xfail, not a false
green); what was wrong is what the declaration says moved. Closed: all three corrected in both files,
including which pairs can be read back from git history and which cannot be read back at all.
`defect · evidence-named-but-absent (provenance)`

F7 (defect, closed) — the pre-spawn gate refuses every freshly admitted row, with a message naming
something the row appears to carry.

> "`%s carries no acceptance command`" — `scripts/task-admission.py`, `worker_brief`

The gate's third leg calls `_has_acceptance_key`, which loads the tree's `scripts/plan_checks.py` and
looks for the row's id in `CHECKS`. Admission never writes a key there: it writes the row's
`**Verification:**` paragraph, which `REQUIRED_NEW` makes mandatory. So the normal walk — admit, hold,
brief a worker — is refused on every new row until somebody hand-edits the key table, and no document
in the pack says that is what has to happen or where. Two candidate homes for one fact with the gate
silently picking one is the seam. The refusal is the right behaviour — a row whose acceptance nobody
made runnable should not get a worker — so it stands; what was missing was saying so. Closed: the
message now names `scripts/plan_checks.py` as the home it reads, and the reference's pre-spawn
paragraph says the key is written before the first worker starts rather than after the work comes
back. No behaviour changed, so no new test; `test_no_brief_for_a_row_with_no_acceptance_command` still
matches and still passes.
`defect · unwritten-seam (completeness)`

F8 (defect, closed) — q-816's inline pins drifted again, this time under this pass's own edits.

The nine `path:line` pins in q-816's row prose were re-pinned yesterday by the previous review and
were correct against `e65ae0ee`. This pass's repairs moved `scripts/task-admission.py` by some tens of
lines, and seven of the nine then addressed the wrong function again — `block` landed on a bare
`kind = str(kind)...`, `close` on a comment. Closed: all nine re-pinned and each verified by reading
the line back, with the row's own parenthesis now saying plainly that `check-pin-drift.sh` reads
ARCHITECTURE's pins and reaches none written in a plan row's prose, so this shape drifts silently.
`defect · stale-pin (traceability)`

R1 (recommendation, stands) — a hand edit of `PLAN.md`'s mark still walks past the whole kernel.
Every code path to ✅ runs through `close`, and `close` now refuses a missing checkpoint, a missing
recorded hash, a moved done, a missing receipt, a failed verdict, a moved done-hash and a moved tree
— checked one at a time against the code and exercised in a scratch tree. The one remaining door is a
person or an agent typing ✅ into the row. The contract states that door shut in words —
"the Director never edits `PLAN.md` or a checkpoint by hand", section 4 — and nothing refuses it
mechanically. That is a stated rule rather than a hole, and building a guard for it is a new gate,
which this pack's own standing rule holds until an incident calls for one. Folds into q-816.
`recommendation · later · discipline-not-enforced (safety)`

R2 (recommendation, stands) — the inline-pin class has now produced two incidents in one day (the
previous review's F4, and F8 above). `check-pin-drift.sh` walks 193 pins out of ARCHITECTURE.md and
reaches none of the `path:line` citations written inline in `PLAN.md`'s row prose, which is exactly
where the pack keeps the pointers a resuming session opens first. Widening its reach to that shape is
a gate change and belongs to the row that owns the board, not to a review pass. Folds into q-816,
where the previous record already left it.
`recommendation · later · unreached-class (traceability)`

R3 (recommendation, stands) — the estimate-basis rule this push writes into the execution reference
names a sentence all three of the tree's statements carry. The rule says a derivation-shaped sentence
in front of a number nobody derived is refused, and cites "read off the plan's steps" as the shape,
"since three rows with the same sentence and unrelated numbers were found on 2026-09-06". Those three
rows are q-816, q-823 and q-822, and each still reads "no comparable history in this tree; the range
is read off the plan's steps", with 4–8, 6–10 and 8–14 hours behind it. The plain admission in front
of the clause is what the rule's first half allows, so the statements are not simply illegal — but a
reader holding the rule and the plan together sees the rule's own example standing in all three. The
journal entry this push writes says the three keep their wording as frozen text, which is the honest
call: the statements froze at take-up, `correct` refuses a row that is not queued, and rewriting them
by hand is the act the kernel exists to refuse. What the rule could gain is a sentence saying which of
the two halves a basis like theirs falls in. Folds into q-816, whose acceptance is Requirement 309
whole and whose criterion 48 owns the estimate.
`recommendation · later · rule-and-instance-disagree (clarity)`

R4 (recommendation, stands) — criterion 44's check is a keyword heuristic at the head of a step:
`^\W*(writ|add|cover)\w*[^.]*\btests?\b`. "2) write the tests for it" is caught; "2) the tests are
written" and "2) coverage for the parser" are not. It is the criterion's own example made mechanical
and it is honest about being that, but a plan can walk past it by rewording. Leaving it: the reader
half of validation is what judges a deliverable, and widening a regex until it reads English is the
machinery this pack refuses. Folds into q-816.
`recommendation · later · partial-reach (completeness)`

R5 (recommendation, stands) — `_keep_reader_record` keeps nothing, and says nothing, when the
reader's record fails to parse, when the checkpoint is missing, or when it is not open. So a
validation can pass with the evidence unrecorded and the `Validation.` line still reading
"reader: passed" — which is the exact gap the entry was added to close, narrowed rather than shut. A
failing reader's answers are the ones a later reader most wants. One line returning what was kept
would close it. Folds into q-816.
`recommendation · later · silent-skip (completeness)`

R6 (recommendation, stands) — the previous record's R2 is unchanged and was re-read here: `verify`'s
producer bar reads the row's `**Holder:**` paragraph and T6 `park` deletes it, so hold → park →
`verify --by <the producer>` → close still accepts a receipt the executor wrote for its own work.
Nothing in the tree durably records who produced a row's work. It was already folded into q-816 and
stays there.
`recommendation · later · producer-bar-evadable (safety)`

Class lens: swept. F1's class is "a refusal that names a door another transition does not open" — the
other seven transitions were each read against the state their predecessor can leave: T4→T5 pairs
(unblock refuses a row that is not blocked, and only `block` reaches that state), T6→T2 (park leaves
the checkpoint open, so take-up is clean), T7→T8 (done, and reopen accepts exactly done), T3 (queued
only, and `correct`'s refusal names the checkpoint as the door, which `checkpoint.py update` opens).
T9 was the only stranded one. F4's class is "a measurement taken from state a safe writer destroys" —
swept across every other `stat` in the two readers: `render-board.sh`'s worker-liveness read is the
only other one, and it reads mtime alone, which a rename preserves the meaning of. F5's class is "two
guards for one property, in disagreement" — the only other pair in the delta is `close`'s
checkpoint-status test beside its content tests, and the content tests now run unconditionally, so
they cannot disagree. F6's class is "a record naming evidence that is not there" — swept across the
receipts in the three checkpoints: every path, pair directory and file each receipt's checks name was
checked to exist, and `evals/director/recordings/2026-09-06-pair-6/` is on file with its 36 traces.
F7's class is "a fact with two homes and code silently picking one" — swept across the other fields
the gate reads (the done, which `read_dod` resolves with a stated order of preference, and the mark,
which `_row_span` owns alone).

Blocking: three, all closed.
- F1 a row abandoned by T9 could be moved by no transition at all — closed: `hold` reopens the sheet
  a halt left and a done row is still sent to `reopen` (`scripts/task-admission.py`); three tests,
  the first red against the tree as handed over, and the previous pass's own test restated to hold
  its property end to end.
- F2 the change reds its own landing's test over the canonical board link — closed: q-816's prose
  names the link through `SURFACES.md` instead of writing the address a second time onto the page,
  which `tests/test_board_publish.py::test_one_canonical_url_in_the_registry_and_in_the_rendered_page`
  counts; no test changed, and the file's five tests pass.
- F3 the tree fails `guardrails/check-pin-drift.sh` — closed: the two pins the breaker's new lines
  moved are re-pointed in `architecture/guardrails.md`; the gate reports 193 pins clean.
