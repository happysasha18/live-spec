# Skill review — director, live-spec-base

SKILL-REVIEW

Skill: director
Skill: live-spec-base

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is disproportionate for one table-cell edit and two verbatim
reference extractions)

Verdict: no blocking findings.

## What changed

Two independent pieces of work, reviewed together since both landed the same session and both
touch shared skill surfaces:

1. **Batch-2b slice 3 (final)** — `skills/director/references/request-kind-table.md`'s "a
   defect" row gained the recurring-bug reasoning and detection mechanism, closing the last of
   11 original batch-2b candidates. Went through two rounds of adversarial correction (a
   near-verbatim-phrasing/intra-doc-repetition/misplaced-citation REJECT, then a
   scissors-lint-violation REJECT) before final APPROVE — both real, both fixed.
2. **A.5** — `skills/live-spec-base/SKILL.md` shrank by two verbatim extractions (rule 7's
   worker-restore sub-rule, rule 35's session-handover mechanism) to two new reference files,
   following the file's own established two-prior-extractions pattern. `tests/
   test_worker_restore.py`'s `CLAUSE_HOMES` updated to match. Five stale line-pins in
   `architecture/*.md` re-pointed as a mechanical follow-up.

## Findings

No blocking findings.

- `director/references/request-kind-table.md`'s table stays valid markdown; the row grew but the
  file's overall shape (one table, one closing-paragraph pair) is unchanged.
- `live-spec-base/SKILL.md` dropped from 602 to 598 lines, moving further under its 608-line
  ratchet (`tests/test_live_spec_base_body_thinned.py`) — the third extraction of this kind for
  this file, consistent with its established shrinking pattern (glossary.md, worked-examples.md,
  now worker-restore.md + session-handover.md).
- Both new reference files (`worker-restore.md`, `session-handover.md`) carry a one-line framing
  header before the verbatim body, matching the convention already used by
  `lanes-and-pen.md`/`work-kind-table.md`/`guardrails-catalog.md` in `director/references/`.
- **Real defect caught by adversarial review, not by the implementer or the first review pass:**
  rule 35's rewritten pointer sentence had split the literal two-word phrase "session handover"
  across two different clauses, silently breaking `tests/test_opening_decision_sweep.py`, which
  reads `SKILL.md` directly rather than through its references — a test neither the
  implementation brief nor the first review pass's test list included. Caught by the
  orchestrator's own wide content-grep (a standing lesson from earlier the same session), fixed
  with a one-word insertion, independently re-verified by a second review pass including a fresh,
  broader grep for any other exact-phrase dependency. None found.
- `scripts/sync-skills.sh` re-run after both edits: `director` and `live-spec-base` both synced,
  installed copies match source, no drift.

Re-verified independently across both changes: `python3 -m pytest -q
tests/test_request_classifier.py tests/test_setup_entry.py tests/test_traceability.py
tests/test_live_spec_base_body_thinned.py tests/test_worker_restore.py
tests/test_session_extract.py tests/test_minor_gate_reconciliations.py
tests/test_opening_decision_sweep.py` — all green (223 + 350 passed across the two runs, 1
pre-existing unrelated skip). `scripts/spec-style-lint.py --tier universal` on every touched
file: 0 errors (a real scissors-tier error was caught and fixed on the request-kind-table.md
side before this final state). `guardrails/check-pin-drift.sh`: exits 0, no FAIL lines.
