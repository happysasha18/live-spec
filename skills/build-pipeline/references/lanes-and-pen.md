# Trains, one pen — the lane graph

The lane law itself has one home: `skills/live-spec-base/SKILL.md` rule 7, the concurrent-edit
fence, whose parallel-lanes bullets carry the cap, the pen, the lane-open act, worktree isolation on
overlap, brief-time disjointness, one row per landing commit, the prior-context worker, and the
session identity that breaks a pen tie. None of that is restated here. ("Trains" is the spec's own
word for lanes at SPEC T-18; the two name one thing.)

This file carries the half rule 7 leaves to the seat's judgment, which is the pipeline's own: how the
graph picks the lane set, what happens to the lanes around a landing, and the two forms a colliding
pair takes (SPEC INV-39, INV-49, INV-129, INV-131, INV-214, INV-276).

## The graph picks the lane set, never mood (SPEC INV-49)

At queue-take, read the runnable head and build the mini dependency graph. An edge is drawn on a true
dependency — one row needs another's landed output — or on a same-section / same-behaviour collision,
where the two rewrite one clause or one behaviour's rule. Mere co-location in a shared living doc
draws no edge: `PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are a convergence point
reconciled at integration, never a serializing surface. Open lanes on a pairwise-independent set, up
to the cap rule 7 names, and do not fall back to single-file while independent lanes stand free.

Rows that collide only at integration — co-location included — pre-roll isolated build stages with
the landing order DECLARED at claim: first-declared lands first, and the later one re-fences. Tiny
rows ride serial, because parallel pays only when the build stages dominate the pen work. The chosen
set and its order are board lines, and so is a said-aloud "serial by the graph".

The same queue-take re-scans every deferred row's revisit trigger against the current moment (SPEC
INV-129). A time-bound trigger can come true and lapse between two milestone gates, so the milestone
re-scan is not its only reader — a fired trigger returns its row to the runnable head right then, and
a deferred wish never waits on a trigger nobody reads.

## Around a landing

Only penless stages overlap: a later train's code and tests sit in its own isolated tree, its delta
integrating only under the pen, and read-only analysis runs free. Opening each lane is narrated, and
every train rides the departures board, a waiting lane naming whom it waits behind. A pen-stage is
never cut mid-edit.

The closing commit also moves the row from the queue's body to the month's archive file with its
delivery report (the live-body law, SPEC INV-276). After a landing, waiting lanes re-fence and re-run
their gates on the new truth — never across sessions, never mid-milestone. A bug takes the pen at the
end of the current pen-stage and parks every rolling lane, each at its own checkpoint, resuming in
landing order.

Delegating a lane to a worker uses the Agent tool's `isolation: "worktree"` option (it carries no
gate, usable today), the brief naming the branch its work rides. That literal has its one home here.

## The drafter-applier pipeline, the standard colliding-rows form (SPEC INV-49)

On colliding rows the penless DRAFT stage overlaps the current landing: a drafter worker prepares the
next row's exact edit strings while the applier lands the current row under the pen. See
[drafter-applier-example.md](drafter-applier-example.md) for the drafter's self-verify list and the
2026-07-12 worked run [T-18, INV-39, INV-49].

## A mid-work re-door rebuilds the graph (SPEC INV-131)

Re-fire the door the moment the work is about to create a surface or state its door doesn't grant.
Stop, reclassify, and continue by the right door. A re-door sometimes creates a surface or state that
did not exist when the lanes opened, and the same re-check then **re-runs the independence edges
against every rolling lane (SPEC INV-131)**. The new surface can collide with a sibling that was
independent a moment ago; a new edge pulls the re-doored lane back to serial, waiting behind the lane
it now shares a surface with, and the board carries a line for that move. The integration re-fence
[INV-39] still catches the collision at landing; this closes the board's observability gap and adds
no new net.
