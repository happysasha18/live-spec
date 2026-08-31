# Prover record — 2026-08-31, a cleared mistake stops blocking every future push

PUSH-REVIEW

Range: `6cbec19d..HEAD` on `worktree-agent-a99bbbe59f59a4143`. Base commit `6cbec19d`, the head
origin/main carried when this lane opened. Commits reviewed: `ee5c6933` (the definition and the
check), `37ebdd07` (the fixture and its two-direction proof), `b09a6c01` (the landing — the row's
✅, the live-state paragraph, the rebuilt index, and two readings of the prose).

Prover version that ran: this seat, reading the change against the requirement it edits and the
check it governs. No external prover clone was invoked; the spec change is five criteria inside one
existing requirement, and the review below states what was read and what was run.

## What changed

`spec/guardrails-freshness.md` Requirement 301 gains one case, criteria 21 to 25, stating what counts
as a worker-restore finding **made good**: every file the command named carries, in the repository
that command ran in, a commit dated later than the command. Criteria 23 to 25 state the three
shapes that can never be made good and hold the verify arm out of the reading entirely. The
requirement's Context gains the paragraph saying why the way out exists.

`guardrails/check-worker-restore.py` implements it in the census arm alone: `_named_files` decides
whether a finding's blast radius names files at all, `repair_commit` puts the question to git, and
`main` carries a YES into a third bucket beside history, printed under its own heading and counted in
the reach sentence. The verify arm (`--run`) never reaches that branch.

`tests/test_worker_restore_made_good.py` holds it. `matrix/guardrails.md` gains M-614.
`guardrails/README.md` gains the operator paragraph pointing at Requirement 301.

## What was read

`guardrails/check-worker-restore.py` whole (its header states the gate's law, its counting start and
its two arms); `spec/guardrails-freshness.md` Requirement 301; `guardrails/README.md`'s
worker-restore section; `tests/test_worker_restore.py`,
`tests/test_worker_restore_run_scope.py`; `matrix/guardrails.md` rows M-477, M-546, M-601;
`matrix/base-rulebook.md` M-476; `docs/spec-format.md` on the shape of a case;
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md` row 527, the row's own original
wording, which asked for a recorded recovery with one home.

## What was run

Six checks, each with its result.

1. `python3 -m pytest -q tests/test_worker_restore*.py` — 173 passed.
2. `python3 guardrails/check-worker-restore.py` against this machine's live transcript root, before
   and after the change: five finding lines both times, none made good. The reading cleared nothing
   real on this machine, which is the check that matters most for a way out.
3. The two-direction fixture itself, printed by hand rather than only asserted, so the red page and
   the green page were read as a person reads them.
4. `git log -1 --format=%H --after=<stamp> -- <path>` against a purpose-built repository, for a path
   that exists, a path that does not, and the word `HEAD`: the last two return empty with exit 0,
   which the check reads as no answer and leaves red.
5. `check-requirement-shape.py`, `scripts/spec-style-lint.py`, `check-size-ratchet.py`,
   `check-matrix-reference.py`, `check-board.py` — each green on the edited files. The two shape
   findings on `spec/guardrails-freshness.md` are the part-file preamble and glossary headings, which
   read identically against the file at `6cbec19d`.
6. `python3 -m pytest -q` whole, twice. The mid-change run read 4 failed, 2567 passed, 55 skipped,
   1 error; the error was `tests/conftest.py`'s own guard noticing HEAD move during the run, because
   this seat committed while it was running, and not a test result. The run after the repairs below
   read green, with nothing committed underneath it.

## Findings

Five, three repaired here, two standing as named bounds.

1. **The definition was written between a case heading and its criteria.** Real; the format family
   says a case is one bold line followed by numbered criteria. Repaired: the paragraph moved into
   the requirement's Context block.
2. **`PRODUCT_SPEC.index.md` went stale on the five new criteria.** Real; caught by
   `tests/test_index_generated.py`. Repaired by rebuilding the index, not by editing it.
3. **The landing commit did not refresh `NEXT_STEPS.md`.** Real; caught by
   `tests/test_landing_next_steps.py`, which reads the closing commit rather than the range.
   Repaired: the live-state paragraph and the row's ✅ now land in one commit.
4. **The reading is more generous than the recovery it stands for, and the bound is named rather
   than closed.** Any commit touching the named path after the command clears the finding, not only
   the commit that redid the discarded work. Nothing a repository holds can tell those apart, and
   the honest claim is the one the criterion makes: the work at that path is saved in history again,
   later than the command. This is contained by construction — only the census arm reads it, the arm
   that blocks pushes long after the bytes are gone, so an over-generous reading costs a forensic
   notice and never an acceptance. Criterion 25 keeps the verify arm out.
5. **A timestamp carrying a numeric offset rather than `Z` would shift the boundary by that
   offset.** `_normalize_stamp` truncates at the nineteenth character, so `+03:00` is dropped and the
   remainder is read as UTC. The harness writes `Z` on every record this machine holds. Not repaired,
   because `is_history` has carried the identical property since the counting start existed, and a
   repair belongs to both readings at once or to neither.

Neither 4 nor 5 is blocking. Both are named so a future pass does not re-discover them.

## What was deliberately not built

A record of cleared findings — a ledger, a flag, a date, a counter — which is what row 527's own
original wording asked for ("the record of a recovery has one home"). Such a record is the machinery
this pack rules against: it would have to be trusted, kept true, and swept. The question is put to
the tree instead, afresh on every run, so the answer flips the moment the commit exists and would
flip back if that commit ever left the history. The counting start did not move.

Two alternatives were weighed and dropped. A "this commit or later" test in the tree's history ties
the way out to one hand-written constant, unrelated to any particular finding, and clears every
finding at once including those whose work is still lost — the counting start's own defect, at a
second address. A test asserting the defect class is fixed and green does not bring back bytes
already discarded, and this check's own header already refuses installation time as a proxy for
which configuration a long-running session loaded.

Suite: 2570 passed, 56 skipped, 0 failed, in 14m15s. Chain: the gates reachable from this range read
green on the run just before this file was written.
