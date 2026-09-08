# Prover record — 2026-09-08 q-828 holds, and a quoted copy of the changed sentence goes stale

PUSH-REVIEW

Mode: closure
Range: 5020064c..71e28121
- 71e28121 The one stale quote the closure review found, repaired where it stood — written after
  this read, and by it: the deposit's first paragraph named the quote, and the change's author
  closed it in the same landing rather than leaving it for a sweep. Re-read here: the page's
  current-text quote and the spec bullet it quotes now carry the same words, and the word count
  beside it covers the sentence above the list, which this row never touched.
- cbe2f56c The closure review q-828's push stands on — this record's own first commit
- fa05011c The two skill reviews this landing's edits owe
- 031b0b9e The pack's own two sentences that grew a second queue
- 5020064c The closure review the row's close stands on (base)

This pass produced none of the work it reads. It ran the closure reach and nothing wider: the row's
definition of done, the row's own recorded acceptance command run verbatim at this commit, the diff
of the two pushed commits, and every path that diff touches together with the callers of what it
changed. Seven true things it noticed outside that reach are deposited whole in
`inbox/2026-09-08-closure-notes-beside-q828.md` and open no row.

Files read: `PLAN.md` (the q-828 block through `scripts/plan-step.sh`),
`.live-spec/checkpoints/q-828.md` and `.live-spec/readers/q-828-reader.md`, `scripts/plan_checks.py`
(`CHECKS["q-828"]` and its comment), `skills/product-prover-pack/SKILL.md` (the closure and global
sections), `docs/prover/README.md`, `guardrails/check-prover-record.sh`; every path in the diff —
`hooks/conduct-law.md`, `spec/guardrails-freshness.md`, `skills/live-spec-base/SKILL.md` (rules 4, 5,
6, 7, 26, 27, 39, 41 and each pinned line), `skills/design-reviewer/SKILL.md` (its frontmatter and
the closing no-landing bullet), `architecture/pipeline-and-lanes.md`,
`architecture/rules-and-settings.md`, `tests/test_one_queue_and_same_lane.py`, `tests/conftest.py`
(`read_flat`), `PLAN.md`, `JOURNAL.md`, `FEEDBACK.md`,
`docs/queue-archive/2026-09-08-from-tlvphotos-the-pack-grows-the-board.md`,
`docs/skill-review/2026-09-08-live-spec-base-same-lane.md` and
`docs/skill-review/2026-09-08-design-reviewer-named-exception.md`; and the callers —
`hooks/conduct-judge.py`, `hooks/lean-orchestrator-scan.py`, `guardrails/judge-hooks.json`,
`docs/spec-format.md`, `docs/language-rules.md`, `docs/language-rule-coverage.md`,
`guardrails/language-rules.json`, `NEXT_STEPS.md`, `templates/NEXT_STEPS.template.md`,
`spec/push-gate-milestone-audit.md`, `matrix/templates.md`, `spec/design-spec-review.md` (INV-154),
`skills/live-spec-base/references/glossary.md`, `inbox/README.md`, and the installed copies under
`~/.claude/`.

Checks run: sixteen, each with its result.

- `CHECKS["q-828"]` run verbatim from the repo root — exit 0.
- the same command against a reverted copy of the four files in a scratch tree — exit 1. The change
  is what makes it pass.
- `python3 -m pytest -q tests/test_one_queue_and_same_lane.py` — 4 passed.
- the same test file against that reverted scratch tree — 4 failed, one per file: the standing law,
  the spec law list, the rulebook rule and the reviewer's exception each red on their own arm. The
  live tree was never mutated.
- `pytest` over six consumer files — `test_live_spec_base_body_thinned`, `test_one_home_per_rule`,
  `test_conduct_judge`, `test_lean_orchestrator_arm`, `test_worker_restore_made_good`,
  `test_design_reviewer` — 80 passed, 1 skipped.
- `pytest` over ten more — `test_architecture_format`, `test_prover_doc_homes`,
  `test_review_record_class`, `test_skill_count_agrees`, `test_seat_acts_by_default`,
  `test_orchestrator_read_discipline`, `test_version_is_one_fact`, `test_clean_context_review`,
  `test_push_review`, `test_review_modes` — 88 passed.
- `pytest tests/test_traceability.py -k "pin or architecture or skill or rule"` — 44 passed, 146
  deselected. The whole file was run and did not finish; the full suite hangs on this machine, so
  the run was narrowed to the arms that read the changed paths.
- `guardrails/check-pin-drift.sh` — OK, 195 pins, none drifting, plus 39 range pins.
- `python3 guardrails/check-doc-rotation.py` — OK.
- `bash guardrails/check-skill-review.sh` — OK; both edited skills carry a fresh record.
- `bash guardrails/check-skill-loadability.sh` — OK, 14 skills.
- `python3 guardrails/check-board.py` — OK.
- `python3 guardrails/check-close-receipt.py` — OK; every done row stands on a passed receipt.
- the done digest recomputed over the current `**Done when:**` — `8fd38f27…` matches both the row's
  `**DOD hash.**` and the checkpoint's `DOD:` anchor, so the row closed against the contract it was
  admitted with.
- the acceptance digest recomputed over `CHECKS["q-828"]` — `8aa297c8…` matches the checkpoint's
  `ACCEPT:` anchor, so the command that ran is the command the row was admitted against.
- `diff` of `skills/live-spec-base/SKILL.md`, `skills/design-reviewer/SKILL.md`,
  `skills/product-prover-pack/SKILL.md` and `hooks/conduct-law.md` against their installed copies
  under `~/.claude/` — identical in all four.

Findings: none material. Each of the four clauses of the definition of done was read against the
files as they now stand, not taken on the commit message's word. The standing orchestration law in
`hooks/conduct-law.md` names the board, the project's one queue, and the phrase it replaced survives
nowhere in the tree as a standing instruction — the remaining occurrences are dated handovers, plans,
audit and prover records, and the prohibitive sentences in `NEXT_STEPS.md`, its template,
`spec/push-gate-milestone-audit.md` and `matrix/templates.md`. The spec's law list drops the phrase.
The shared rulebook states the same-lane rule as a sub-bullet of rule 5, the briefing rule, and the
design reviewer's no-landing is named as the one deliberate exception in both the rulebook and the
reviewer's own skill, each carrying the reason. The new sub-bullet was read against rules 27, 39 and
41 and contradicts none: rule 41 already says a finding of our own review is repaired inside the work
that needed it, rule 39's ban on new machinery is answered by the incident of 2026-09-08 that
produced this one, and rule 27 speaks to a different question. The reviewer's new text agrees with
its own frontmatter, which already says it holds no landing, and with INV-154, whose first criterion
is the reason the new text gives. `hooks/conduct-judge.py` loads the law from beside itself at run
time rather than holding a copy, and `hooks/lean-orchestrator-scan.py` names the file only in a
docstring, so neither reads a phrase that no longer exists. Eleven architecture pins were re-aimed by
the same ten lines the edit inserted, and each new line holds text byte-identical to what the old pin
pointed at. The commit message's own claims were checked and hold: eleven pins, ten lines, a verdict
from a checker that produced none of the work. The acceptance is not vacuous — it reds on a revert —
though its hold on `spec/guardrails-freshness.md` is one negative grep alone, which is in the inbox
deposit with six other things this reach did not cover.

Blocking: none
