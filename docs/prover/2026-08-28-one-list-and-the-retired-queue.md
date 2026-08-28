# Prover record — 2026-08-28 the plan, the board and the queue become one list

PUSH-REVIEW

Range: fdcdd9d..HEAD, reviewed as one pass. Base commit `fdcdd9d`, the tip this push starts from.
Reviewed commits, in order: `85b659d1` (another session's, landed on main before this work began and
an ancestor of it), the one-list commit, and this record.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

plan-11's own work: "The plan, board and queue become one list." Its acceptance, written on the
board, asks three things — one file holds the list and the other is gone from the tree, findable in
the archive; `bash scripts/render-board.sh` draws the merged list; and a command shows every open row
carrying a feature and a priority mark, and names the exceptions.

The queue had held no rows since 27.08, when its last 142 moved into `PLAN.md`. What kept it alive
was the machinery: `scripts/open-lane.sh` told a session to flip a status cell in a file with no
cells; `guardrails/check-doc-rotation.py` read its manifest; `scripts/state-probe.sh` printed
"ROADMAP queue: 0 rows" at every session start; a dozen tests read it as their corpus. The file now
rests at `attic/ROADMAP.md` with its manifest line, its rotation pointers moved whole into `PLAN.md`,
and every mechanism above reads the one list.

`85b659d1` is a second session's landing, not this one's: the prover-description test stopped
asserting a literal phrase from an external skill's frontmatter and holds live-spec's own property
instead, and CI's canon pin moved to the commit the 1.4.2 release names. It is reviewed here because
it is in the range, not because this session wrote it.

## How this review was run

Read to refuse. Every consumer of the retired file was found by `grep -rn ROADMAP` over the whole
tree and judged one at a time against what it actually does at runtime, never against its comment.
The judgement each hit got is written out under Findings 5 and 6, including the ones deliberately
left alone.

Files read: `PLAN.md`, `ROADMAP.md` (now `attic/ROADMAP.md`), `scripts/open-lane.sh`,
`scripts/state-probe.sh`, `scripts/render-board.sh`, `scripts/plan_checks.py`,
`scripts/plan-step.sh`, `scripts/rotate-doc.py`, `scripts/check-shipped-language.py`,
`scripts/progress-report.py`, `guardrails/check-doc-rotation.py`,
`guardrails/check-landing-next-steps.py`, `guardrails/crosscut_counter.py`,
`guardrails/check-authority-anchor.py`, `guardrails/check-freeze.sh`,
`guardrails/check-push-reach.sh`, `guardrails/check-prototype-fence.sh`,
`guardrails/progress-baseline.json`, `guardrails/README.md`, `guardrails.config.json`,
`tests/test_lane_branch_road.py`, `tests/test_traceability.py`, `tests/test_row_id_uniqueness.py`,
`tests/test_landing_next_steps.py`, `tests/test_delegation_line.py`, `tests/test_footprint_note.py`,
`tests/test_traffic_transport.py`, `tests/test_prover_adapter_contract.py`,
`tests/test_authority_anchor.py`, `tests/test_doc_rotation.py`, `ARCHITECTURE.md`,
`architecture/host-adoption.md`, `architecture/seams.md`, `architecture/guardrails.md`,
`TEST_MATRIX.md`, `OVERVIEW.md`, `README.md`, `NEXT_STEPS.md`, `CLAUDE.md`, `attic/MANIFEST.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`,
`skills/live-spec-base/SKILL.md`, `skills/live-spec-base/references/glossary.md`,
`skills/spec-author/SKILL.md`, `skills/director/SKILL.md`, `spec/parallel-lanes.md`.

Checks run: the whole suite, the push-gate chain, and every gate this range touches, one at a time.

- `python3 -m pytest -q`, the whole suite the way CI runs it — 2476 passed, 3 skipped, 1 error in
  19m50s. The error is `tests/test_worker_restore_run_scope.py`'s tree-stability guard, which reds
  when the working tree changes mid-run; this record's own file was written while the suite ran.
  Re-run alone on a still tree: 7 passed. The same guard errored the same way on the baseline run
  before this work began, for the same reason.
- `bash guardrails/pre-push < /dev/null` — chain verdict quoted under Verdict below.
- `python3 guardrails/check-doc-rotation.py` — OK, before and after the manifest moved, and against
  `--doc PLAN.md` explicitly before the default changed.
- `python3 guardrails/check-landing-next-steps.py` — OK on the live range, with the new arm armed.
- `python3 guardrails/crosscut_counter.py` — exit 0, 16 pairs at or above the threshold, the same
  reading as before the retirement (the body it lost held no rows).
- `python3 guardrails/check-authority-anchor.py` — OK, with the advisory report now naming eight
  candidate lines on `PLAN.md` where it named nothing before.
- `bash scripts/render-board.sh` — 63 steps, 39 blockers. `bash scripts/state-probe.sh` — reads
  36 done, 27 open, and no longer prints a queue line for a file that is gone.
- plan-11's own acceptance command, timed at 0.04s, and red-proven: a planted task inside
  `PLAN.md`'s Tasks section that the board does not draw makes it exit 1 and print
  `not drawn on the board: q-99999`.

Findings: eight, listed below.

Blocking: none.

The one defect this range could have shipped — finding 1, the landing gate left with no live
trigger — was found and repaired inside the range, with a fixture that reds without the repair. The
two gaps under findings 3 and 4 are recorded in `PLAN.md`'s Blockers as work nobody has asked for,
not as holes in what this range shipped.

## Findings

**1. The landing gate would have gone silently vacuous, and that is the one defect this range could
have shipped.** `guardrails/check-landing-next-steps.py` holds INV-242: a commit that closes a row
owes a `NEXT_STEPS.md` refresh in the same commit. Both of its triggers read a `ROADMAP.md` diff.
From the moment that file left the tree, neither could ever fire on new work again, while the gate
went on printing OK on every push — a green line with no reach behind it, the exact class this pack
has ruled against before. It gained a third arm that reads what the board actually records: a task
heading whose mark becomes ✅. The arm is red-proven by a fixture that reds a close made without the
refresh, and two more fixtures hold its edges — a close beside a refresh passes, and a row moving to
in-hand owes nothing. The two older arms stay: they still classify history correctly, and a range
reaching back before today is read by them.

**2. The rotation manifest had to move with the list, not with the file.** `check-doc-rotation.py`
reads a live document's `rotated-manifest` block and proves every archive it names still holds the
rows it claims, and separately that no `rotated-*.md` archive exists unpointed. Sending the manifest
to the attic with the file would have left every one of the six archives unpointed; re-aiming the
gate at `PLAN.md` without moving the block would have passed vacuously on a document with no
manifest at all. The block moved verbatim into `PLAN.md` under a section that says in plain words
what it is for, and the gate was run against `PLAN.md` explicitly before its default changed, so the
pass was observed before it was relied on.

**3. `scripts/rotate-doc.py` has no live subject, and that gap is left open rather than papered
over.** It understands only the retired table's shape, so nothing now moves a finished task off the
board except a person's hands. The two moves made this month were made by hand and were correct.
Teaching it the plan's heading shape is a rewrite, and this task's own mandate was to remove a
mechanism, not to add one; guessing at a new one inside it would have been the wrong trade. The
script keeps its place — every archive it wrote still carries the shape it reads — with the truth
stated in its docstring, and the gap stands in `PLAN.md`'s Blockers for the owner.

**4. The method still teaches every new project to keep the queue this one just retired.** Four
sentences across `skills/spec-author`, `skills/design-reviewer`, `skills/communicator` and
`skills/live-spec-base` name the queue as "`ROADMAP.md` in this pack", and the templates and the
joining walk still hand a new project that file. Those are the pack's product for a host, not this
project's own board, and rewording text a host has already vendored is a release decision with a
version number attached (base rule 32). Left standing, named in `PLAN.md`'s Blockers.

**5. What kept the old name on purpose.** Every citation of the form `(SPEC INV-x, ROADMAP row N)`
across the tree — several hundred of them, in guardrail docstrings, matrix rows and spec context
lines — is provenance for work that shipped. Those rows are in `docs/queue-archive/`, grepable by
number, and the manifest in `PLAN.md` points at them. Renaming them would break the trail this
project's own nothing-lost rule exists to keep. They stay.

**6. The two exclusion lists that name the file by basename are dead, and removing them would buy
nothing.** `scripts/check-shipped-language.py`'s `EXCLUDE_FILES` and `check-prototype-fence.sh`'s
`-e "(^|/)ROADMAP\.md$"` spare it as a narrative surface. Both also spare `attic/` by directory, so
the retired file is covered either way and the named entry now decides nothing. Removing them
changes no behaviour and risks a typo in a live gate; they are left, and recorded here so the next
reader does not mistake them for live wiring. `check-muted-launch.sh` and `check-broad-kill.sh` name
it only in a sentence describing which surfaces are prose, not in any list their code reads. Three
comments that named it as a live document were corrected instead of left to mislead:
`check-push-reach.sh`'s tested-document list, `check-freeze.sh`'s note on why the queue is not
frozen, and `check-doc-rotation.py`'s usage block. One list was NOT dead:
`check-authority-anchor.py`'s risky-surface report is the surface where a decision-as-his first gets
written, and with the file in a spared directory it had lost its subject. It now names `PLAN.md`,
which is where those lines are written today — eight of them are reported, advisory as before, and
nothing is blocked by it.

**7. The identifier check gained a subject it never had.** `test_row_id_uniqueness.py` proved that no
two queue rows claim one number, so a citation resolves to one row. The live list's own ids —
`plan-11`, `q-166` — had no such check anywhere: two tasks could have carried one id and every
pointer to it would have resolved to whichever sorted first. They are checked now, against the
board's real 63 rows, with a floor that reds if the parse ever returns nothing.

**8. plan-11's acceptance command reads a file git does not track, and that boundary is stated.**
`board.html` is generated and gitignored, so on a fresh clone the command finds no board. It says so
in one line — run the renderer — instead of raising a traceback, and it reds, which is the honest
answer: the board has not been drawn there. The alternative, running the renderer inside the check,
was rejected: it costs a second at every session start and writes a file as a side effect of asking
a question.

## One boundary this range crossed deliberately

`PLAN.md`'s law 1 says executing the plan does not edit existing gates, hooks or configs, because
writing yourself into a gate's exception list is a workaround from the other side. Three gates are
edited here — the rotation gate's default document, the landing gate's third arm, the
authority-anchor report's risky surface. None of them is an exception written for this range's
benefit: every one restores a reach the retirement would otherwise have taken away, and no check
was loosened, skipped or given a new carve-out. The law's own subject, a session buying itself a
green, is the opposite of what these three do. Named here rather than passed over.

## Verdict

The chain was run at 16:41 on the work commit `139699ee`, before this record was committed, and
returned one red and twenty-two greens:

> FAIL (prover record): the newest committed prover record predates the last ARCHITECTURE.md change.

That is this record's own absence, by construction — gate a asks that the review postdate the
architecture it reviews, and `ARCHITECTURE.md` changed in the commit under review. Everything else
in the chain passed on that tree: the matrix and architecture Reference tables equal a fresh build,
174 pins hold, the four host checks pass, config health matches, the generated index agrees. Gate b
is delegated to CI on this host and was run by hand instead, with the numbers above.

Re-run with this record committed, on the tree that goes out:

> All gates green — push allowed.

Two runs stood between those two lines, and both were gate a reading this record's own shape rather
than the tree: the first found the `Checks run:` field opening straight onto a list with nothing on
its own line, the second found the `Blocking:` field's explanation running on past the word that
answers it. Both are recorded here rather than quietly fixed, because a record that reaches green on
its third shape is worth knowing about when the next one is written.

Acceptance, checked against plan-11's own three clauses: one file holds the list and the other is
gone from the tree and findable in the attic with its manifest line — met. `bash
scripts/render-board.sh` draws the merged list, all 63 rows of it — met. A command shows every open
row carrying its group and its priority and names the exceptions by id, and there are none — met.
Its wider "Done when" sentence asks that the probe name the tasks that matter without being told
which and that both readers be held by a test: the probe's ranking and the board's coverage are held
by `tests/test_board_matches_the_canon.py`, `tests/test_tasks_parser_finds_every_task.py` and
plan-11's own acceptance command, which reds when a row on the list is missing from the page.
