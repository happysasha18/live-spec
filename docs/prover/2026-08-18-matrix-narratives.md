# Prover record — 2026-08-18 matrix-narratives

PUSH-REVIEW

Range: 7dbb9f7f..fa495dc3
- fa495dc3 The record carries the narratives' move and its merge
- 256641e The census follows the resolved merge
- 67c46a5 Merge matrix/2026-08-18-narratives: guardrails incident stories leave the fact cells
- 71b39c1 Move guardrails-node incident narratives out of TEST_MATRIX.md fact cells
Files read: TEST_MATRIX.md, docs/matrix-notes/guardrails.md, guardrails/rule-census.json
Findings: an estimate of this move was wrong by two orders of magnitude, and the merge with the judges package would have dropped one of its clauses silently — both are set out below
Blocking: none

The guardrails node's incident stories leave the fact cells.

Root: the `[node: guardrails [target]]` block carried dated incident stories — owner asks
with timestamps, outage and hang timelines, defect postmortems — woven into thirteen rows'
fact sentences, in the same cells that state the operational criteria a reader is there
for. The story and the criterion competed for the same cell.

What happened: the narrative spans move word for word into `docs/matrix-notes/guardrails.md`,
one heading per row id. Each cell keeps its mechanism, its never-clause and its trailing
anchor, and gains a short `(history: …)` pointer before that anchor. Rows touched: M-154,
M-330, M-388, M-389, M-390, M-391, M-392, M-393, M-394, M-397, M-401, M-461, M-466.

The move was accounted for word by word before the merge: every word removed from the
thirteen cells stands either in the kept cell or in the notes file, with one exception — a
colon after `DECISIONS.md` in M-401 that the rewritten sentence does not need. 135 words
are new: thirteen pointers and the notes file's headings. Nothing was summarised.

The merge onto today's main conflicted, because the judges package had rewritten the same
thirteen rows an hour earlier. It was resolved row by row rather than by taking a side: the
narrative move wins the cells, and M-392's judges clause — six hooks are library entries the
gate never demands, and the Stop branch is proven against a fixture declaration built from
the real one, Requirement 311 — was carried back in by hand, because the matrix branch
predates it and its version of that row does not contain it.

Numbers: TEST_MATRIX.md 484,267 to 482,845 bytes (minus 1,422) before the merge; the census
is rebuilt over the resolved tree by its own script.

Checks run: `tests/test_matrix_reference.py` and `tests/test_rule_census_ratchet.py` — 20
passed, which is gate (d) proving the committed Reference equals a fresh build over the
moved bodies, and the ratchet accepting a byte count that only fell. The working copy was
checked after the run: no fabricated commits, no missing files.

Findings:
- The fleet's estimate for this move was 132 KB. The honest figure is 1.4 KB — wrong by two
  orders of magnitude, because the estimate counted a whole node while the work was the
  narrative spans inside thirteen cells. An estimate of a move is worth nothing until the
  spans themselves are marked.
- A merge of two branches that rewrote the same rows would have dropped a clause silently if
  either side had been taken whole. Both sides were legitimate work an hour apart. Row by row
  is the only honest way to merge a document whose cells are the unit of meaning; taking
  ours or theirs wholesale is wrong here by construction.

Blocking:
- none.
