# Trains, one pen — the lane law

The full lane law referenced from `SKILL.md`'s "Gates worth remembering" section: the cap and the
independence test, the pen-stage rules, the lane graph, the open-lane act, and the drafter-applier
form (SPEC T-18, INV-39, INV-49, INV-214). Every line below reads exactly as it read in the body.

- **Trains, one pen (SPEC T-18, INV-39):** one session may roll up to the profile-declared lane cap of
  INDEPENDENT build lanes without asking (`lanes.cap`, package default three [E-13]; the owner's
  2026-07-06 value three in his profile; one more opens only on the human's asked word, never silently) —
  pairwise independent: no true dependency between them and no same-section / same-behaviour collision —
  mere co-location in a shared living doc is not an edge. Opening each lane is narrated, and
  every train rides the departures board, a waiting lane naming whom it waits behind. Only penless
  stages overlap: a later train's code and tests in its own isolated tree (its delta integrates only
  under the pen; the disjoint-file road stays within one lane), read-only analysis free.

  Every shared-doc edit, the integration, and the closing of a row take the pen one lane at a time — a
  pen-stage is never cut mid-edit — and a landing commit carries exactly one row's delta, its gate run
  on a tree clean of the other lanes' unfinished work; that same closing commit moves the row from the
  queue's body to the month's archive file with its delivery report (the live-body law, SPEC INV-276).
  After a landing, waiting lanes re-fence and
  re-run their gates on the new truth. Never across sessions, never mid-milestone. A bug takes the pen
  at the end of the current pen-stage and parks every rolling lane, each at its own checkpoint,
  resuming in landing order.
  **Lanes are picked by a graph, never by mood (SPEC INV-49):** at queue-take read the runnable head
  and build the mini dependency graph — an edge only on a true dependency (one row needs another's
  landed output) or a same-section / same-behaviour collision (the two rewrite one clause or one
  behaviour's rule). Mere co-location in a shared living doc draws no edge: the shared living docs
  (PRODUCT_SPEC, ARCHITECTURE, TEST_MATRIX) are a convergence point reconciled at integration, never a
  serializing surface. Open lanes on a pairwise-independent set up to the cap. Rows that
  collide only at integration — co-location included — pre-roll isolated build stages with the landing
  order DECLARED at claim (first-declared lands first, the later re-fences). Tiny rows ride serial — parallel pays only when
  build stages dominate the pen work — and the chosen set, the order, and a said-aloud "serial by the
  graph" are board lines. The same queue-take also re-scans every deferred row's revisit trigger against
  the current moment (SPEC INV-129): a time-bound trigger can come true and lapse between two milestone
  gates, so the milestone re-scan is not its only reader — a fired trigger returns its row to the runnable
  head right then, so a deferred wish never waits on a trigger nobody reads whichever cadence comes first.

  **Opening a lane is an act you PERFORM (SPEC INV-214):** once the graph picks a
  pairwise-independent set of two or more runnable rows with lanes free under the cap, open each one — do
  not fall back to single-file. The act, `scripts/open-lane.sh <row> <slug>` or the same walk by hand:
  stage the row→in-work flip in the queue, run the script to fence-check, refuse a lane past the profile
  cap (`lanes.cap`, default three), commit that flip alone to main under the pen (the one-row claim
  commit), cut `lane/<row>-<slug>` from it into its own worktree under `.claude/worktrees/`, and print the
  worker brief stub naming the branch. Then delegate the lane with the Agent tool's `isolation:
  "worktree"` option (it carries no gate, usable today), the brief naming the branch its work rides. Going
  single-file while independent lanes stand free is a recorded choice: say the "serial by the graph" board
  line and name why (the rows collide, the cap is full, the rows are tiny, or a dependency orders them).
  That recorded reason is a discipline you hold, since no gate can judge whether two rows were independent
  and owed a parallel lane — that judgment is the graph itself, a senior read (SPEC INV-49, INV-214).

  **The drafter-applier pipeline is the standard colliding-rows form (SPEC INV-49):** on colliding rows
  the penless DRAFT stage overlaps the current landing, a drafter worker preparing the next row's exact
  edit strings while the applier lands the current row under the pen. See
  [drafter-applier-example.md](drafter-applier-example.md) for the drafter's
  self-verify list and the 2026-07-12 worked run [T-18, INV-39, INV-49].

  Re-fire the door mid-work the moment the work is about to create a surface or state its door doesn't
  grant. Stop, reclassify, and continue by the right door. The re-door sometimes creates a surface or
  state that did not exist when the lanes opened. In that case the same re-check **re-runs the
  independence edges against every rolling lane (SPEC INV-131)**. The new surface can collide with a
  sibling that was independent a moment ago. A new edge pulls the re-doored lane back to serial, waiting
  behind the lane it now shares a surface with. The board carries a line for that move. That way the
  departures board never asserts a stale independence after the ground moved. The integration re-fence
  [INV-39] still catches the collision at landing; this closes the board's observability gap and adds
  no new net.
