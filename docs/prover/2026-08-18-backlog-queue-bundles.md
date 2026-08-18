# Prover record — 2026-08-18 backlog-queue-bundles

PUSH-REVIEW

Range: 55032d9f..e4c77d08
- e4c77d08 Merge origin/main (spec split, 55032d9f) into deliver/backlog
- 9ba13c32 Update the prover record for the doc-bound and style-lint fixes
- 10dbb6e1 Adjust the ROADMAP.md doc-bound to the final measured size
- 4137dd72 Reword row 553's bundle note to clear the scissors style rule
- 0bfe6326 Confirm the prover record's range against the merged head
- 2146221d Prover record for the ROADMAP queue-bundle package
- 52d31762 Raise the ROADMAP.md doc-bound for the queue-bundle cross-references
- a2956014 ROADMAP rows carry their queue-bundle notes

Range confirmed against `git log --oneline 55032d9f..HEAD` after main moved to 55032d9f under a
separate spec-split package (PRODUCT_SPEC.md split into a core plus 30 files under spec/) and
this worktree merged that new origin/main in: eight commits, all listed above, base is
`origin/main` at push time (`55032d9f`). The merge (e4c77d08) was clean — no conflict markers,
`ort` strategy auto-resolved the one file both sides touched (guardrails/doc-bounds.json, each
side raising a different document's bound) — and this package touches no file under spec/ or
PRODUCT_SPEC.md, so the split itself needed no adaptation here. The merge also pulled in the
spec-split's own fix to guardrails/check-prover-record.sh, which now reads freshness off
PRODUCT_SPEC.md plus spec/ together.
Files read: ROADMAP.md, guardrails/doc-bounds.json, guardrails/check-doc-bound.py, guardrails/check-prover-record.sh, tests/test_doc_bound.py, scripts/rule-census.py, scripts/spec-style-lint.py, docs/prover/README.md
Checks run: python3 -m pytest tests/test_authority_anchor.py tests/test_doc_bound.py tests/test_doc_rotation.py tests/test_far_tier.py tests/test_landing_next_steps.py tests/test_traceability.py -q — 297 passed (re-run after the merge, unchanged); python3 guardrails/check-doc-bound.py — OK; bash guardrails/check-pin-drift.sh — OK, 207 pins + 53 range pins, no drift; python3 guardrails/check-doc-findings-bound.py — OK, 177 documents, none above its record; python3 scripts/rule-census.py ROADMAP.md — 215 findings, matching the pre-change count
Findings: the delivered work is real and correctly scoped, but the branch it came from was corrupted, and two point-testing passes turned up real gate misses the branch's own report never mentioned. See findings below.
Blocking: none

Root: 235 open ROADMAP rows had no way to see which other rows shared the same underlying
ask. The queue's own cross-reference convention (a row naming another row by number, with
plain words for why) already existed for individual rows; it had never been used to mark
whole natural bundles. The backlog report grouped the 235 rows into 35 bundles (201 rows)
plus 34 standalone rows, by reading the actual row text rather than trusting either of two
stale prior counts (244 from the night before, 275 from the original brief) — both were
checked against the live file and rejected.

What was done: commit a2956014 (cherry-picked from 23a0497a, the branch's real deliverable —
see the branch-corruption finding below for why it was cherry-picked rather than merged) edits
the first-numbered row of each of the 35 bundles to name the other rows in its bundle and the
shared reason, in the existing per-row cross-reference style. 35 insertions, 35 deletions —
same row count, no row added, removed, or status-changed. Commit 52d31762 raises ROADMAP.md's
byte ceiling in guardrails/doc-bounds.json to cover the added text. Commit 4137dd72 rewords one
of the 35 added bundle notes (row 553) that tripped the pack's own scissors style rule. Commit
10dbb6e1 nudges the doc-bound ceiling up by the 22 bytes that reword added.

Proved by: running the targeted suite instead of trusting the branch's own report, twice.
First pass: tests/test_doc_bound.py::test_each_bound_is_above_the_current_file and
test_gate_passes_the_real_tree both failed — ROADMAP.md at 297422 bytes against a 291721-byte
ceiling, a miss the report never mentioned. Raising the bound (52d31762) cleared it. Second
pass, running the local `git push` gate chain directly (not just the point tests) before
asking for the actual push: gate aa (doc-findings-bound) failed — ROADMAP.md's rule-census
finding count rose from 215 to 216. `python3 scripts/rule-census.py ROADMAP.md` plus a diff of
`spec-style-lint.py --tier full` output before and after isolated the new finding to exactly
one line: row 553's bundle note read "reacts to machine load, not to the code", the
comma-appositive contrast frame the pack's scissors rule bans outright (any ", not X" that
isn't "not only/just/merely/simply"). It was reworded to "answers to machine load, a separate
cost from the code itself" — same meaning, no banned frame — which dropped the finding count
back to 215, matching the pre-change baseline exactly. After both fixes: check-doc-bound.py
OK across all five growable docs, check-doc-findings-bound.py OK with no document above its
recorded count, check-pin-drift.sh clean at 207 pins plus 53 range pins (confirming the
row-content edits never shifted a pinned line number), and 297 tests pass across the six
targeted files (authority-anchor, doc-bound, doc-rotation, far-tier, landing-next-steps,
traceability).

Findings:
- The spec-split merge (e4c77d08) is content-neutral to this package: it only touches
  PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, spec/, and the check scripts that read the spec by
  path. ROADMAP.md and guardrails/doc-bounds.json's ROADMAP.md entry came through untouched by
  the merge itself (the TEST_MATRIX.md entry in the same file did collide with a separate
  same-day raise, and git's `ort` strategy reconciled it automatically with no marker left
  behind — reviewed, not this package's concern, but confirmed clean).
- Two real gate misses (doc-bound, then doc-findings-bound/scissors) surfaced only by actually
  running the checks, not by reading the branch's report. Both fixes are content-neutral to the
  35 rows' substance: one widens a size ceiling to match real growth, the other rewords one
  sentence to say the same thing without the banned contrast frame.
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
