# Prover record — 2026-09-02, no finished total

Prover skill version: product-prover 4.3.0, with product-prover-pack bindings (live-spec-base 6.1.0).
Mode: targeted delta review (CROSS-LINK-shaped), not FULL — one commit against the requirement it
carries. No `Range:` beyond the single commit named below is owed.

Reviewed: commit `bb59f354` — `spec/message-first-read.md` Requirement 314 clause 8 (rewritten) and
new clause 10 (INV-319), read against what the same commit built: `scripts/state-probe.sh`
(`closed_since_push`, `CATEGORY_ORDER`, the summary print line) and `scripts/render-board.sh` (the
Done column and its own summary print line). Also read: `spec/wish-intake.md` Requirement 4 clauses
10-13 as the commit rewrote them, for meaning against their prior text (`git show bb59f354`'s diff).

Files read in full: `spec/message-first-read.md`, `spec/wish-intake.md`, `scripts/state-probe.sh`
(all 360 lines), `scripts/render-board.sh` (parsing through the column/count rendering and the
summary print block), `tests/test_plan_is_not_executable.py` (the changed test and its class),
`tests/test_tasks_parser_finds_every_task.py` (the changed test and its class).

Checks run: `git show bb59f354` (full diff, all seven changed files); a constructed two-commit git
repo proving the `closed_since_push` regex fires on a title-only edit to an already-done row (below,
F1); a constructed single-commit repo with no `origin/main` proving `git diff origin/main...HEAD`
exits 128 there (below, F2); `grep -n "Done\|count" scripts/render-board.sh` and a read of
`tests/test_plan_is_not_executable.py` confirming no test reads the board's Done-column count text.

The wish-intake rewrite (clauses 10, 12, 13) drops dated provenance and the contrast-frame
sentences the lint flagged, and keeps each clause's operative rule as written before: reopened is
still distinct from blocked and from queued, blocked still wins when a done-marked, failing row also
carries its own `blocked_by`, and a reopened row still reads as done again on the acceptance command
alone. No finding there.

## Findings

**F1 — defect · missing-outcome-check (postcondition).** `closed_since_push` is a text-diff match on
the row's rendered line, not a check that the row's own state changed from not-done to done. A
title edit on a row that was already done before the push window began produces the identical
`+### ✅ … — id: X` line the regex is built to catch, and the row is shown again as freshly closed.

> "a row closed since the last push takes its own done line in the printed account... and drops off
> once the push lands" — commit message; codified as `spec/message-first-read.md` R314 clause 10

Proved by construction: a one-line repo where `id: q-1` is already `✅` at `origin/main`, and the
only change on `HEAD` is the row's title text (`Ship the widget` → `Ship the widget, v2`, mark
unchanged). `git diff origin/main...HEAD -- PLAN.md` prints `-### ✅ Ship the widget — id: q-1` /
`+### ✅ Ship the widget, v2 — id: q-1`; the `+` line matches `^\+### ✅ .*— id: (\S+)\s*$` and
`state-probe.sh` adds `q-1` to `closed_since_push`. A person who fixes a typo in an already-closed
row's title, or reorders its clause text, sees that row printed a second time as if it had just
finished — the exact re-surfacing the owner's word (02.09, quoted in the commit message) named as
unwanted for the count as a whole, now happening per-row instead. Fix: derive `closed_since_push`
from the mark's own transition (no `### ✅ … id: X` line at all on the `origin/main` side for that
id, i.e. a genuinely added line, not a changed one), not from whether a `+` line matching the
pattern exists.

**F2 — defect · undefined-path (transitions).** "The last push" the spec names has no single meaning
the code computes; it is read as one hardcoded thing — divergence from `origin/main` — that does not
hold on a branch other than `main`, and fails outright with no `origin/main` in reach.

> "and drops off once the push lands" — `spec/message-first-read.md` R314 clause 10

Two cases, both reachable and neither addressed by clause 10 or by the code around it:

- On a branch other than `main` with its own upstream, `git diff origin/main...HEAD -- PLAN.md`
  still measures against `origin/main`, not against that branch's own remote. A row closed and
  pushed to `origin/feature-x` keeps appearing on every `state-probe.sh` run — it never "drops off
  once the push lands" as clause 10 promises — until the branch itself merges into `main`.
- With no `origin/main` ref reachable at all (a fresh clone before the first `git fetch`, or no
  `origin` remote configured), `git diff origin/main...HEAD` fails outright. Proved by construction:
  a fresh one-commit repo with no remote returns exit 128 on that exact command. `state-probe.sh`'s
  `_d.returncode == 0` guard (line 129) catches the failure and leaves `closed_since_push` empty —
  silently. The summary line still prints as if the account were complete; nothing tells the reader
  that the freshly-closed rows are simply unreadable in this state, as distinct from there being
  none.

Fix: state in clause 10 (or a sub-bullet) what "the last push" means when the working branch is not
`main`, and what the printed account owes the reader when that reference point cannot be resolved at
all — silence and a report both read the same today, and the spec doesn't say that is the intended
answer.

**F3 — defect · direct-contradiction (contradiction).** Clause 8 forbids a count of finished work in
the printed account, and the commit's own message claims the figure is gone from both readers of the
plan; `render-board.sh`'s HTML page still prints one.

> "shall carry no count of finished work in that account. A running total of finished rows only
> grows, and it answers nothing without a window over which to read it." — `spec/message-first-read.md`
> R314 clause 8

`render-board.sh`'s own summary print line was edited to drop its done count (`"written: %s (%d
open, %d blockers)"`, no `%d done` left). The board page it writes was not: the Done column's own
header renders `<span class="count">%d</span>` over `len(col_steps)` for every task whose icon is
`✅` — every row ever marked done, unfiltered by `closed_since_push` and unbounded by any push
window. That is exactly the shape the owner's word (quoted in the commit message: "не надо писать
сколько сделано, то есть это число будет только расти... это за месяц? с начала проекта?") named as
unwanted — a total that only grows, with no stated window. No test reads that count's text (checked:
neither `tests/test_plan_is_not_executable.py` nor the board test in it asserts anything about the
Done-column header), so nothing would catch it drifting further. Fix: either drop the Done column's
own count the same way the console line was dropped, or write the reason it's kept as a stated
exception to clause 8 — clause 8 as written names one account and the commit message claims two
readers, and the code delivers one.

**F4 — defect · missing-rule (invariant).** The freshly-closed done rows now sit inside the same
fixed nine-line budget as open work, ahead of every other category in `CATEGORY_ORDER`, and no
clause says a done row should ever outrank a row needing the person's own eyes for a line.

> "order the open work by the states the plan records — what needs the person's eyes... and shall
> claim no ordering read from anywhere else" — `spec/message-first-read.md` R314 clause 7, beside the
> new clause 10

`CATEGORY_ORDER = ["✅", "👁️", "🔄", "🔁", "⛔", "⬜"]` places the closed-since-push class first,
literally ahead of 👁️, the category clause 7 names first in its own ranking. The round-robin fill
(lines 180-190) breaks out of its `for` loop the moment `budget <= 0`, so on a pass where the
remaining budget is smaller than the number of categories still holding items, the categories
earlier in `CATEGORY_ORDER` win the slots that remain and later ones are pushed into `more_below`,
unprinted. A session that closes several rows in one sitting can therefore push a row that needs the
person's decision below the fold in favour of the news that other rows just finished — clause 7's
own ranking governs only "the open work," so a wholly separate class competing for the same physical
lines is a real precedence question clause 7 never answers and clause 10 never raises. Fix: state
which yields — a stated cap on how many closed-since-push lines can print regardless of budget, or an
explicit statement that 👁️ (and, arguably, 🔄) always print before any closed-since-push row.

**F5 — recommendation · now · missing-outcome-check (postcondition).** The test that proved every
declared row is accounted for somewhere — shown, below the fold, or done, summing to the full
declared count — was replaced by a self-consistency check that no longer touches the full count.

> "shown (%d) + more-below (%d) + done (%d) = %d, but PLAN.md declares %d tasks" (removed) —
> `tests/test_tasks_parser_finds_every_task.py`, `test_probe_summary_accounts_for_every_declared_task`

The new version checks `shown_open + more_below == open_count` (the printed numbers agree with each
other) and `0 < open_count <= len(self.declared)` (a loose bound). Neither checks that a
closed-since-push row printed via F1's mechanism, or an old done row left off the board, is counted
exactly once against the total row count `PLAN.md` declares. INV-1 ("The system shall never delete a
row... shall carry every wish to a recorded terminal state") had a mechanical proof that nothing was
silently lost or double-counted; that proof is gone, and nothing in this commit or the surrounding
suite replaces it. Fix: keep a full-accounting assertion — `len(shown non-done) + more_below +
len(closed_since_push shown) + (old-done not shown) == len(declared)` — rather than dropping the
identity because the "done" figure it used to reference no longer prints.

Class lens: swept — F1 and F2 share one class, "closed since the last push" implemented as a
text-diff match against a single hardcoded ref rather than as a defined state transition measured
against whatever the actual push boundary is; both trace to the same nine lines in
`scripts/state-probe.sh` (127-133). F3 stands alone: it is the one place the commit's stated goal
("gone from both readers") and its actual diff (one reader's print line only) disagree. F4 and F5
are each their own class — a missing precedence rule, and a weakened regression test — checked for
siblings and found none: no other category competes across a budget boundary the way ✅ now does, and
no other conservation-style test in either changed file lost its full-count assertion the same way.

## Verdict

Needs another iteration. F1 is a construction-proven false positive in the mechanism clause 10
depends on; F2 leaves "the last push" undefined in two reachable states; F3 means the commit's stated
result — no growing total on either reader — is not what shipped. None of the four defects is large:
each is a bounded fix to `state-probe.sh`, `render-board.sh`, or one added sentence in the spec. F5
is a test-coverage regression alongside them, not a spec defect.
