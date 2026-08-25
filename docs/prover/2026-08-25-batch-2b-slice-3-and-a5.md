# Prover record — 2026-08-25 batch-2b-slice-3-and-a5

PUSH-REVIEW

Range: eca83ce4..c56c4fb6 (3 commits)
- f7f30c2c Give recurring-bug-redoor's residual a home (batch-2b slice 3, final)
- a739a76e Move rule 7's worker-restore sub-rule and rule 35's mechanism to references (A.5)
- c56c4fb6 Skill-review record for batch-2b slice 3 + A.5 (director, live-spec-base)

Files read: full diff of f7f30c2c and a739a76e (7 files total, 56 insertions / 21 deletions);
`skills/director/references/request-kind-table.md`, `skills/live-spec-base/SKILL.md`,
`skills/live-spec-base/references/{worker-restore,session-handover}.md`,
`tests/test_worker_restore.py`, `architecture/{pipeline-and-lanes,rules-and-settings}.md`
(current state, not just the diff); the corresponding source passages in
`skills/build-pipeline/SKILL.md` (recurring-bug-redoor) and the pre-edit
`skills/live-spec-base/SKILL.md` (rule 7's worker-restore bullet, rule 35's full text, read via
`git show`); an independent investigation's findings on all 4 remaining batch-2b candidates
before any drafting began (recorded below); `PRODUCT_SPEC.md`/`spec/*.md` grepped for T-9,
"missing an invariant", "grep JOURNAL.md for the area" (all absent, confirming a genuine gap);
`tests/test_opening_decision_sweep.py` (the test whose break neither the brief nor the first
review pass caught).

Checks run: this range closes two independent lines of work.

**Batch-2b slice 3 (recurring-bug-redoor, the last of the original 11 items):** before drafting
anything, an independent investigation re-checked all 4 remaining candidates
(recurring-bug-redoor, Step 7 INV-62/63, push-mechanics INV-82/106, docs-layout pass INV-111)
against `PRODUCT_SPEC.md`/`spec/*.md` closed-home-set tests — the exact lesson slice 2 left
open. Three were confirmed false positives (already fully spec'd with closed home-sets excluding
`director/SKILL.md` — `tests/test_traceability.py::test_sample_first_and_source_reopen`,
`tests/test_ci_verdict.py`'s `HOMES` tuple, `tests/test_docs_layout_vehicle.py`'s `HOMES` tuple)
and dropped from the list without drafting anything. Only recurring-bug-redoor was genuine, and
only a narrow residual of it (the bare re-door fact was already in
`request-kind-table.md`; the reasoning and the journal-grep detection mechanism were not).

The draft went through two REJECT rounds by an independent adversarial reviewer before landing:
- Round 1 REJECT: near-verbatim phrasing lifted from `build-pipeline/SKILL.md`, intra-document
  repetition (the same "missing an invariant" idea stated twice, three lines apart, once in the
  table cell and once in a separate new paragraph), and a disrupted table→explanation pairing
  (the new paragraph split the table from its existing follow-up paragraph). One of the
  reviewer's cited grounds (a one-home-per-fact objection) was itself contested by the
  orchestrator with evidence from the four already-landed batch-2b siblings sharing the identical
  "test only names one home" shape — the reviewer re-checked that evidence directly and retracted
  the objection, while the three craft findings stood and were fixed: merged into one reworded
  clause, no separate paragraph, no repetition.
- Round 2 REJECT: `scripts/spec-style-lint.py --tier universal` — a mechanical check the
  orchestrator had skipped before resubmitting — found a real scissors-pattern error ("a repeat
  means the area is missing an invariant, not that it needs a second patch" tripped the banned
  comma-contrast shape). Fixed by dropping the "not that..." tail; the reviewer additionally
  caught that the retained `(INV-104, INV-124)` citation didn't back the elaborated claim (INV-124
  is the same-instant "class hunt," not the over-time recurring-bug pattern) and recommended
  repositioning `(INV-104)` beside the clause it actually supports and dropping `INV-124`
  entirely (this fact has no formal INV code, confirmed by spec grep). Final round: APPROVE,
  independently re-verified (lint 0 errors, 223 tests passed).

**A.5 (live-spec-base extractions):** the diff was reviewed once, independently, checking seven
named constraints (rule headings survive, line ratchet holds, extraction is verbatim,
`CLAUSE_HOMES` complete, no other test expects the moved prose inline, pin re-pointing correct,
capability-map.md not stale) — initial verdict APPROVE. Before committing, the orchestrator ran
an additional wide content-grep across all of `tests/*.py` (the standing lesson from earlier
today) and found `tests/test_opening_decision_sweep.py::test_the_rulebook_names_the_closing_
step_too` — outside the reviewer's tested file list — asserts the literal phrase "session
handover" against `SKILL.md` directly; rule 35's rewrite had split that two-word phrase apart.
Fixed with a one-word insertion (no line-count change). Sent back for a second, fresh review pass
including the reviewer's own broader grep for any other exact-phrase risk from either moved rule
— none found. Final verdict: APPROVE.

Independently, both changes: `python3 -m pytest -q tests/test_request_classifier.py
tests/test_setup_entry.py tests/test_traceability.py tests/test_live_spec_base_body_thinned.py
tests/test_worker_restore.py tests/test_session_extract.py
tests/test_minor_gate_reconciliations.py tests/test_opening_decision_sweep.py` — 223 + 350
passed across the two runs (the recurring-bug-redoor set and the A.5 set share
`test_traceability.py`, counted once), 1 pre-existing unrelated skip.
`scripts/spec-style-lint.py --tier universal` on every touched file: 0 errors in the final state
(one real error caught and fixed mid-review on the request-kind-table.md side, described above).
`bash guardrails/check-pin-drift.sh`: exits 0, no FAIL lines, including the five pins re-pointed
in `architecture/pipeline-and-lanes.md`/`architecture/rules-and-settings.md` after rule 7's
extraction shifted lines below it by +4. `bash scripts/sync-skills.sh`: `director` and
`live-spec-base` both synced, no drift. `bash guardrails/check-config-health.sh`: clean.

Findings: two real defects caught by adversarial review before push (both described above, both
fixed and independently re-verified) plus one real defect caught by the orchestrator's own wide
grep after a review pass had already approved (also described above, fixed and independently
re-verified by a second review pass). No other defect found. `build-pipeline/SKILL.md` is
untouched by the slice-3 half of this range — its now-duplicated recurring-bug text is left in
place until cutover step 3 removes the whole displaced body in one movement.

This closes batch-2b entirely (all 11 original items resolved: 6 landed across 3 slices, 5
confirmed already-spec'd and dropped) and closes item 5 of Полоса A (`live-spec-base`'s two safe
extractions). Полоса B item 5 (batch-2b) is now fully done; Полоса A items 6-7 (review/prover
already folded into this record; the rules 6/14/19/29/31 compression) and Полоса B items 6-10
(transitional adapter, test classification, worker fan-out, wide grep before final deletion,
skill-creator eval) remain.

Blocking: none
