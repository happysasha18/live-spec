# Prover record — the three closure guarantees, and the three holes in the fix itself

The pass ran on the evening of 2026-09-06 and the push crossed midnight; the file carries the
day the push goes out, which is what the gate reads, and this line carries the day the review
was actually done.

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 and `skills/live-spec-base/SKILL.md`. The adversarial
read of `9ff033c6` was run by a fresh seat that authored none of it, briefed to find reasons to
refuse it and holding it defective until evidence said otherwise. Its verdict was **refuse**, with
three blocking findings. All three are closed in the second commit of this range, which this
record is committed with.

Range: f54d1b44..HEAD

- 9ff033c6 Three bypasses of the closure kernel, closed on the paths they actually ran on —
  the pre-spawn guard on the subagent tool, the verifier running the acceptance the tree
  recorded, the done's digest anchored on the checkpoint, push gate u and its CI step, and the
  board refusing to draw a done over a failed receipt
- 0ba7f1d5 The three holes the adversarial read of `9ff033c6` found, plus its two minor findings
  and its four ceilings written down
- 81477952 The live board's day count is judged against the day, not against one past day — the
  wall-clock red the final full run met at 00:5x, read below as finding 10
- 1c204091 The suite's own green record, off the final full run of this range — the checkpoint
  `python3 -m pytest -q` writes for the session guard, carrying nothing else

This record ships in its own commit after those four, which the gate exempts because a record
cannot name the commit that first carries it.

Files read: `scripts/task-admission.py`, `scripts/plan_checks_core.py`, `scripts/render-board.sh`,
`scripts/plan_checks.py`, `scripts/checkpoint.py`, `guardrails/check-close-receipt.py`,
`guardrails/worker-admission-guard.py`, `guardrails/pre-push`, `guardrails/check-muted-launch.sh`,
`guardrails/check-prototype-fence.sh`, `scripts/check-shipped-language.py`,
`scaffold/status-view/plan_checks.py`, `.github/workflows/gates.yml`, `.claude/settings.json`,
`.gitignore`, `tests/test_closure_kernel_bypasses.py`, `skills/build-pipeline/SKILL.md`,
`skills/build-pipeline/references/accepted-work-execution.md`.

Checks run: the full suite on this range's final code, the local gate chain on the same tree, the new bypass file on its own, and the one command behind finding 2. Each with its result below.

```
$ python3 -m pytest -q                      (on this range's final code)
2991 passed, 5 skipped, 1 xfailed in 1317.02s (0:21:57)
(exit 0)
```

The xfail is the `build-pipeline` closing eval, declared stale on its own record — see finding 9.
An earlier full run on `9ff033c6`'s tree read 2987 passed, 5 skipped, 1 xfailed, exit 0; the run
between them met the wall-clock red of finding 10.

```
$ bash guardrails/pre-push                  (local chain, this tree)
All gates green — push allowed.
(exit 0)
```

```
$ python3 -m pytest -q tests/test_closure_kernel_bypasses.py
21 passed
(exit 0)
```

```
$ git show ":PLAN.md" >/dev/null 2>&1 ; echo $?
0
```
The one command behind finding 2: an empty base made `git show <base>:PLAN.md` read the INDEX and
exit 0, which is why the gate's newly-done arm stood down in silence rather than reddening.

Findings: three blocking defects, two minor ones, four ceilings written down rather than left to be discovered, one answered with evidence, one wall-clock red the final run met, and two things named and not repaired here. Every blocking defect is closed in this range.

1. **The anchor bought nothing after the close.** `check-close-receipt.py` compared the receipt's
   hash against the row's `**DOD hash.**` line and skipped the comparison when that line was
   absent. `verify` is the only other reader of the checkpoint's anchor and never runs again on a
   closed row, so deleting the hash line one step later published exactly the contract swap the
   anchor was added to catch. The reviewer proved it on a copy of this project's own plan: exit 0,
   green, with the anchor present. **Closed** — the gate reads the anchor, faults on a done row
   whose hash line is gone while its anchor stands, faults when the two disagree, and compares the
   receipt against both. `test_deleting_the_hash_after_the_close_is_caught_before_publication`.

2. **The CI arm was vacuous on every pull request.** `LIVE_SPEC_DIFF_BASE: ${{ github.event.before }}`
   is EMPTY on a pull request and forty zeros on a branch's first push. Empty made the gate read
   the index and exit 0, so the base marks equalled the current marks and no row was ever "newly
   done"; zeros made it unreadable and the arm dropped. The two sibling gates already guard
   non-empty, not-all-zeros and `rev-parse --verify`; this one copied none of the three, and the
   step's own comment claimed the opposite. **Closed** — `resolve_base` normalizes both to
   `origin/main` and verifies it names a commit, the comment says what happens, and
   `test_an_empty_or_zero_base_does_not_stand_the_new_done_arm_down` runs both shapes.

3. **A closed row cleared the spawn guard.** `pre_spawn_check` read that a checkpoint EXISTS and
   never its status, so naming any long-finished row in a prompt satisfied the guard — admission
   in name and nothing else. **Closed** — a row whose sheet is not open is refused by name, with
   `reopen` named as the door. `test_a_closed_row_does_not_clear_the_spawn_guard`.

4. Minor: `correct --done` on a row whose checkpoint `abandon` had closed reached
   `_write_dod_anchor` and raised out of the checkpoint format instead of refusing in this
   module's words. **Closed** — the anchor is written only while the sheet is open; the row
   carries the corrected hash either way.

5. Minor: the guard stood down whenever `cwd` was a subdirectory of the project, while its own
   text framed that stand-down as "outside a live-spec tree". **Closed** — the board is looked
   for at the cwd and above it. `test_the_guard_finds_the_board_from_a_subdirectory`.

6. **Not a defect, recorded as the fix's ceiling** (and now written into the documents rather than
   left to be discovered): the acceptance table is an ordinary tracked file and no gate judges
   what a key TESTS, so a key reading `true` clears everything and only a person reading the diff
   sees it; a receipt is plain text in the checkpoint, which `tree_hash` deliberately leaves out
   of the tree it pins, so a hand-written RECEIPT line satisfies `close` and the gate alike; the
   spawn guard reads the board and never the worker's conduct; and it binds the sessions that load
   this repository's settings and no others.

7. **Not a defect, answered with evidence.** The reviewer noted that the guard did not fire on its
   own spawn and asked whether the claim rested on a fixture. It does not: a real session opened
   on this project (`claude -p` with cwd at the repository root) had a trivial subagent spawn
   denied by `guardrails/worker-admission-guard.py`, quoting the refusal verbatim. The reviewer
   itself was spawned from a session opened on a different directory, which loads a different
   settings file — the ceiling named in finding 6.

8. **Not repaired here, named.** A host attached today ships `scripts/plan_checks.py` with an
   empty table, and `verify` now refuses a row with no recorded key, so such a host writes its
   first key before its first close. That is the guarantee working, and the setup path now says
   so in `skills/build-pipeline/SKILL.md`. Any host holding an outstanding receipt written before
   this commit must verify again, because the receipt carries no `acceptance` field; the refusal
   names the change rather than reading as tampering.

10. **Found by the final full run, not by the review, and repaired.** `tests/test_work_board.py`'s
   real-tree arm for the board's day count demanded that something had closed today and named
   q-822, a row closed on 2026-09-06 — so it reddened at every midnight after that day, on the
   wall clock rather than on a defect. It met this range at 00:5x on 2026-09-07. The mechanism it
   guards is proved on fixtures in the same file; the real-tree arm now asserts that the live page
   agrees with the live tree, which holds on a day nothing closed. Outside the three guarantees
   this range is about, repaired because it is the cause of a red final gate.

9. **Not repaired here, named.** The closing eval for `build-pipeline` grades the two documents as
   they stood before this range and is declared stale on its own record. Re-recording it is nine
   producer runs, which the instruction this pass ran under forbade.

Spec and architecture re-check: `PRODUCT_SPEC.md` is unchanged in this range. `ARCHITECTURE.md`
itself is unchanged; two of its pins moved with the lines they name (`architecture/guardrails.md`,
`architecture/pipeline-and-lanes.md`) and gate g proves all 193 against the code as it stands. The
closure kernel still has no requirement of its own in the spec, which is a gap this range does not
close and does not widen: the kernel's one home stays
`skills/build-pipeline/references/accepted-work-execution.md`.

Blocking: three, all closed.
- F1 closed: `guardrails/check-close-receipt.py` reads the checkpoint's anchor, faults on a done
  row whose hash line is gone while the anchor stands, faults when the two disagree, and compares
  the receipt against both. The defect: the anchor was invisible after the close, so deleting the
  row's hash line one step later published a done nobody verified. Held by
  `test_deleting_the_hash_after_the_close_is_caught_before_publication`, red against the code the
  review read.
- F2 closed: `resolve_base` normalizes an empty and an all-zero base to `origin/main` and verifies
  it names a commit, and the workflow's own comment now says so. The defect: the CI arm was
  vacuous on every pull request, because an empty base made `git show :PLAN.md` read the index and
  exit 0. Held by `test_an_empty_or_zero_base_does_not_stand_the_new_done_arm_down`, which runs
  both shapes.
- F3 closed: a row whose sheet is not open is refused by name, with `reopen` named as the door.
  The defect: `pre_spawn_check` read that a checkpoint exists and never its status, so any
  long-finished row id in a prompt cleared the guard. Held by
  `test_a_closed_row_does_not_clear_the_spawn_guard`.
