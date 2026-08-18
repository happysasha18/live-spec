# Prover record — 2026-08-18 backlog-queue-bundles

PUSH-REVIEW

Range: ebc4d428..52d31762
- 52d31762 Raise the ROADMAP.md doc-bound for the queue-bundle cross-references
- a2956014 ROADMAP rows carry their queue-bundle notes
Files read: ROADMAP.md, guardrails/doc-bounds.json, guardrails/check-doc-bound.py, tests/test_doc_bound.py, docs/prover/README.md
Checks run: python3 -m pytest tests/test_authority_anchor.py tests/test_doc_bound.py tests/test_doc_rotation.py tests/test_far_tier.py tests/test_landing_next_steps.py tests/test_traceability.py -q — 297 passed; python3 guardrails/check-doc-bound.py — OK; bash guardrails/check-pin-drift.sh — OK, 207 pins + 53 range pins, no drift
Findings: the delivered work is real and correctly scoped, but it was cherry-picked from a single commit rather than merged from the branch tip, and it grew ROADMAP.md past its declared bound. See findings below for both, plus a serious environment-defect finding.
Blocking: none

Root: 235 open ROADMAP rows had no way to see which other rows shared the same underlying
ask. The queue's own cross-reference convention (a row naming another row by number, with
plain words for why) already existed for individual rows; it had never been used to mark
whole natural bundles. The backlog report grouped the 235 rows into 35 bundles (201 rows)
plus 34 standalone rows, by reading the actual row text rather than trusting either of two
stale prior counts (244 from the night before, 275 from the original brief) — both were
checked against the live file and rejected.

What was done: commit a2956014 (cherry-picked from 23a0497a, the branch's real deliverable)
edits the first-numbered row of each of the 35 bundles to name the other rows in its bundle
and the shared reason, in the existing per-row cross-reference style. 35 insertions, 35
deletions — same row count, no row added, removed, or status-changed. Commit 52d31762 raises
ROADMAP.md's byte ceiling in guardrails/doc-bounds.json from 291721 to 297423 (one byte above
the file's new measured size), because the added cross-reference text pushed the file 5701
bytes past its 2026-08-17 ratchet. Rotation was not the remedy — nothing closed, every grown
row is still live queue — so the bound was raised by name with a reason, the path the check's
own remedy message names.

Proved by: running the targeted suite instead of trusting the branch's own report. Initially
tests/test_doc_bound.py::test_each_bound_is_above_the_current_file and
test_gate_passes_the_real_tree both failed — ROADMAP.md at 297422 bytes against a 291721-byte
ceiling. After raising the bound, both pass and check-doc-bound.py reports OK across all five
growable docs. check-pin-drift.sh reports 207 pins plus 53 range pins clean, confirming the
row-content edits did not shift any pinned line number. 297 tests pass across the six targeted
files (authority-anchor, doc-bound, doc-rotation, far-tier, landing-next-steps, traceability).

Findings:
- The doc-bound miss above was not in the branch's own report; it only surfaced when the
  point tests were run for real. The fix (raising the ceiling by name, with a reason, per the
  gate's own documented remedy) is content-neutral — it does not touch what the 35 rows say,
  only how much room the file is allowed.
- Serious environment defect, found by inspection, not by any script. lane/2026-08-18-backlog's
  branch tip had moved far past the real deliverable commit (23a0497a). Roughly 300 commits had
  landed on top of it, authored by test-fixture identities (t <t@t>, a <a@example.com>,
  gate <gate@example.com>, fixture@example.invalid, worker@example.invalid,
  livespec-test@example.invalid), and that pile deleted nearly the entire repository —
  ARCHITECTURE.md, PRODUCT_SPEC.md, README.md, every test file, guardrails configs. Merging the
  branch tip as instructed would have wiped most of main; the original source worktree
  (/private/tmp/live-spec-backlog/wt) carried the same corrupted tip and the same uncommitted
  deletions in its own working tree, so this was not local damage from the delivery process
  itself. This is the same environment defect already seen twice today in a smaller form (a
  commit's author rewritten to gate@example.com, a stray test-corruption email on an otherwise
  real commit) and once as content corruption; here it reached the point of nearly erasing the
  product outright. It was caught only because the branch's commit authors were read by a human
  before merging, not because any gate checked for it. The remedy taken here was narrow and
  specific to this push: cherry-pick the one real commit (23a0497a) onto a fresh copy of
  origin/main, leaving the corrupted branch itself untouched and unrepaired, since repairing a
  shared branch ref was out of scope for a single delivery and risked touching other lanes'
  work.

Blocking:
- none.
