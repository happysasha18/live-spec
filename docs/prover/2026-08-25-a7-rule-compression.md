# Prover record — 2026-08-25 a7-rule-compression

PUSH-REVIEW

Range: ff43d281..99699916 (2 commits)
- 6a99bf32 Compress rules 6/14/19/29/31 in place (A.7)
- 99699916 Skill-review record for A.7 rule compression

Files read: full diff of 6a99bf32 (2 files, 112 insertions / 118 deletions);
`skills/live-spec-base/SKILL.md` (current state, not just the diff, all 5 touched rules read in
full before and after); `architecture/rules-and-settings.md`; the exact test-pinned substrings
for each of the 5 rules, verified present before drafting a compression and re-verified after
(`tests/test_live_spec_base_body_thinned.py`, `tests/test_checkpoint_closes.py`,
`tests/test_leave_command.py`, `tests/test_class_hunt.py`, `tests/test_deferral_marker.py`,
`tests/test_agent_channels.py`); `skills/communicator/SKILL.md`'s leave-word bullet (to confirm
rule 6's cut material is genuinely restated there, not silently lost).

Checks run: an investigation identified the 5 compressible rules, measured their current
density, found each rule's test-pinned floor by grep, and drafted a concrete per-rule
compression plan (estimated ~1413 bytes / 10.8% total savings) before any file was touched. The
implementation followed that plan, compressing all 5 rules by merging sentences and cutting
connective filler, with one confirmed content removal: rule 6's closing paragraph fully restated
the leave-word mechanic already canonical in `PRODUCT_SPEC.md` + `communicator/SKILL.md` — this
was independently verified true (grepped `tests/test_leave_command.py`, confirmed it requires
only the bare substring "leave-word") before the restatement was replaced with a one-line
cross-reference.

Independent adversarial review (a different agent than the implementer, briefed to reject not
confirm) found one real defect: a first draft of rule 14's cross-reference sentence had been
rewritten to add a new home, `skills/director/references/class-hunt.md` — a file from a separate,
concurrent, still-under-review task (giving the bug-class-hunt fact a home in Director). This
coupled a pure-compression change to an unstable external file the reviewer correctly noted could
still be renamed, reworded, or rejected on its own merits. Fixed by reverting rule 14's sentence
to its exact original wording; the cross-reference is deferred to a fast-follow commit, to land
only once the other task is independently approved and committed on its own. Reviewer
independently re-verified the revert byte-for-byte and gave APPROVE.

Independently: `python3 -m pytest -q tests/test_live_spec_base_body_thinned.py
tests/test_checkpoint_closes.py tests/test_leave_command.py tests/test_class_hunt.py
tests/test_deferral_marker.py tests/test_agent_channels.py tests/test_request_classifier.py
tests/test_traceability.py tests/test_minor_gate_reconciliations.py` — 346 passed, 4 skipped
(pre-existing, unrelated), run independently by both the implementer and the reviewer with
matching results. `scripts/spec-style-lint.py --tier universal skills/live-spec-base/SKILL.md`:
0 errors, 8 pre-existing advisory warnings (identical count before and after, confirmed by
diffing the lint output against `git show HEAD~2:skills/live-spec-base/SKILL.md`'s own lint run).
`guardrails/check-pin-drift.sh`: one real drift caught (rule 22's pin in
`architecture/rules-and-settings.md`, `:323` → `:319`, from the net -6 line shift), fixed in the
same commit, re-verified exit 0 with no FAIL lines. `bash scripts/sync-skills.sh`: installed copy
matches source, no drift. `bash guardrails/check-config-health.sh`: clean.

Findings: one real cross-task coupling defect caught by adversarial review before push (described
above, fixed, independently re-verified). No other defect found. Body: 598 → 592 lines, further
under the 608-line ratchet.

This closes Полоса A item 5 (see `docs/prover/2026-08-25-batch-2b-slice-3-and-a5.md` for the
worker-restore/session-handover extraction it follows) and item 7 (this compression) — item 6
(review/prover/push) is this record itself. Полоса A is now fully closed except nothing remains:
items 1-7 all done.

Blocking: none
