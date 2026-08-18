# Prover record — 2026-08-18 cull-readme-count

PUSH-REVIEW

Range: 2cad4de..14eb889d
- 14eb889d Merge lane/2026-08-18-cull into deliver/cull
- 11d9fbfb README stops publishing the skills-lines count
Files read: README.md, guardrails/tree-counts.json, tests/test_tree_counts.py, guardrails/check-tree-counts.py, guardrails/check-doc-bound.py, scripts/gen-tree-counts.py
Checks run: python3 -m pytest tests/test_tree_counts.py -q — 43 passed; python3 guardrails/check-tree-counts.py --allow-uncommitted — OK; python3 guardrails/check-doc-bound.py — OK; python3 scripts/gen-tree-counts.py — no diff produced
Findings: README no longer publishes the skills-lines count; the two remaining published counts (gate-roster, scaffold-checks) still verify. See findings below.
Blocking: none

Root: the owner did not ask for a skills-lines count on the front page. README stated
"you do not read them, they run" two paragraphs above a block that then invited the reader
to count the skill lines by hand. The count served the builder, not the reader, and every
skill edit paid a rebuild cost for a block nobody asked for.

What was done: the delivered branch removes the generated skills-lines block and its proof
paragraph from README.md, removes the skills-lines entry from guardrails/tree-counts.json,
and removes the skills-lines-only regression test from tests/test_tree_counts.py along with
its registry-contents assertion (updated from three counts to two). scripts/gen-tree-counts.py
and guardrails/check-tree-counts.py are untouched on purpose: they still judge the two
remaining published counts (gate-roster, scaffold-checks), so gate ad keeps a live subject.

Merge conflict: README.md conflicted on merge, because origin/main and the lane branch each
carried the same block at the same location with no other drift around it. The conflict was
resolved by taking the lane branch's deletion of that one block and keeping every surrounding
line as both sides already agreed on it — nothing else in the file was touched or dropped.

Authorship: the incoming commit's author was gate <gate@example.com>, a known test-corruption
artifact. It was unpushed, so it was fixed with git commit --amend --reset-author --no-edit
before merging, and the merge was redone clean.

Proved by: running the point tests instead of trusting the report. All 43 tests in
tests/test_tree_counts.py pass. check-tree-counts.py reports OK with counts read:
gate-roster, scaffold-checks — matching the report's claim that only those two remain.
check-doc-bound.py reports OK across all five growable docs, unaffected by README shrinking
since it only bounds growth. Regenerating scripts/gen-tree-counts.py produced no diff, so the
committed guardrails/README.md counts already match the tree.

Findings:
- The cull report also surveyed the wider checks-census cull and found three of the census's
  "never caught" verdicts were false negatives (check-no-history.py, check-freeze.sh caught
  real problems on 2026-08-05 and 2026-08-09) and two more were load-bearing dependencies
  (check-config-health-perms.py inside gate m, check-size-ratchet.py used live by
  scripts/measurements-table.py). None of that is part of this package — it is audit output,
  not a deletion, and this push does not act on it.
- One stale cross-reference was noted but deliberately not fixed here to avoid colliding with
  another in-flight lane: PRODUCT_SPEC.md:4744 and TEST_MATRIX.md:191 still cite
  guardrails/check-wrong-referral.py, which another lane already moved to
  guardrails/attic/check-wrong-referral.py today.

Blocking:
- none.
