# Archived off PLAN.md: a row whose only reason to stay open was that the owner might ask again

Date: 2026-09-03. The owner's words that morning govern this: a task never sits open with no real
reason the Director itself understands; an amorphous ask is never accepted; and nothing gets built
beside the plan, not even a place to park ideas in. Both words are on record in `DECISIONS.md`
under 2026-09-03 ~10:08 and ~10:20.

The criterion, and it is the one q-813 wrote into the board's own working rule: a row stays open
only where a person could check, from outside, that its reason still holds — it is in hand, or it
waits on a named event someone can see happen. `q-385` is the worked example of a real one, "the
first host declaring a contract in its card". `q-811`'s was "a real ask for it", which asks the
owner to raise the subject again before the row can move. Nothing outside the row settles that, so
the row could sit open forever while reading, to anyone glancing at the board, exactly like work
somebody had committed to.

Nothing is lost. The row's own text stands in full below. The spec chapter it kept alive,
`spec/work-board.md` Requirement 309 and its ninety-nine acceptance criteria, rests at
`attic/spec-work-board-R309.md`, and its test-matrix block at `attic/matrix-work-board-R309.md`,
each with a line in `attic/MANIFEST.md`. The form the owner approved on 2026-08-06 is untouched at
`docs/norms/work-board.html` and `docs/norms/work-board.provenance.md`, and the evening's own
record of every word he gave, with its time, is at
`docs/handovers/2026-08-06-evening-work-board-handover.md`. If the board is wanted again it comes
back through a fresh design conversation and a new row, never by resurrecting this one.

## Index

One line for the archived row, findable by its own number — the pointer a reader who greps the
live list for that number follows to get here.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
| --- | --- | --- | --- | --- |
| 811 | A bigger board — worker lanes, timing, who's on what | surface | declined 2026-09-03 | its revisit trigger asked the owner to raise the subject again, which nothing outside the row can check, so it was an idea wearing a task's marks; the spec chapter it held open retired with it, and the approved form stays findable under `docs/norms/` |

## What the owner actually asked for, in his own words

The board grew out of nine turns on the evening of 2026-08-06, all recorded. This is the one that
names what `q-811` carried after `q-166` closed on the cheap leg — the lanes and the per-task
detail:

> and there are also lanes for parallel agents, and also info per taks like what is the
> branch/worktree etc. frankly, I don't get what's on the kanban you showed me. these tiles do not
> look like tasks, it's a text I need to crack my mind to understand what it is.

— 2026-08-06 20:36, `docs/handovers/2026-08-06-evening-work-board-handover.md`, §"Every word
Alexander gave, with its time". The other eight turns stand there under their own times, and
`DECISIONS.md` carries each as its own dated entry.

He has not raised the board since that evening. `board.html` and `scripts/render-board.sh`, built
2026-08-31, already give him a page to look at instead of asking; that page is not this row, and
its own header says so.

---

### ⬜ A bigger board — worker lanes, timing, who's on what — waits until it's actually asked for — id: q-811
**Group:** Board & visibility · **Priority:** normal
**Source:** found 2026-09-02, closing q-166 — `spec/work-board.md` still promises this feature
whole, on two `[target]` lines (`INV-308`, `INV-67`), never withdrawn when q-166 closed on its
cheap leg alone. A promise nobody is building stands here as its own open row rather than inside
a task that closed without it, the same repair shape as q-385 and q-804 above.

**What it is.** `spec/work-board.md` Requirement 309 describes a kanban-style task queue for a
HOST project's own work — worker lanes, given-vs-actual time per task, per-agent attribution, one
stable published link — built on top of the same Canon `board.html` already renders for this
project's own plan. `q-166` closed on the cheap leg only (`board.html`, already shipping); this
row carries the larger feature's own unbuilt promise so it isn't silently orphaned.

**Revisit trigger:** a real ask for it, since the last one was 2026-08-06 and none has come since.
Until then this stays queued rather than in hand — building it now, with nobody asking, is the
"don't serve machinery nobody needs" standing rule, the same reasoning q-166's own close names.

**Acceptance:** unchanged from `spec/work-board.md` Requirement 309's own criteria — a card per
task, one lane per worker, given-vs-actual time, per-agent attribution, one published link — proven
live over one real stretch of work, the same way q-166's own acceptance read before this split.
