# Skill review — director

SKILL-REVIEW

Skill: director

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is disproportionate for one short reference file and a
4-sentence body paragraph)

Verdict: no blocking findings.

## What changed

`skills/director/references/class-hunt.md` (new) carries a reworded statement of the confirmed-bug
4-move class hunt (name the defect's class and hunt siblings, check architecture, check spec,
escalate to the human on judgment calls) — a fact `docs/director/capability-map.md` had flagged
as homeless but the original 11-item batch-2b list never included. A 4-sentence paragraph in
`skills/director/SKILL.md`'s Execution section points at it.

## Findings

No blocking findings.

- `director/SKILL.md`'s Execution section reads naturally with the new paragraph in place —
  it sits between the existing "A new fact can change the remaining graph" and "The verifier gets
  the goal and the artifacts" paragraphs, matching their bold-lead-sentence-plus-bracket-link
  voice.
- Two rounds of independent adversarial review, each catching a real defect: round 1 found a
  near-verbatim 5-word lift from build-pipeline's source text and a stray literal "door" inside
  an unrelated idiom ("next door"); round 2, after both were reworded, found the replacement
  phrasing had introduced a NEW 6-word verbatim run against both the source and live-spec-base's
  own rule 14. Fixed with a second reword, verified clean by a programmatic 5-gram overlap check
  (not eyeballing) on the third pass.
- A genuine cross-task coupling defect was caught and corrected mid-review: a first attempt at
  wiring `live-spec-base/SKILL.md` rule 14's cross-reference to this new file was reverted after
  an independent reviewer on a separate, concurrent task (unrelated rule compression touching the
  same file) correctly flagged it as coupling a stable rulebook to a same-session, still-under-
  review reference. That cross-reference is deliberately deferred to its own fast-follow commit.
- `scripts/sync-skills.sh` re-run: nothing changed (director's installed copy already matched —
  confirmed no drift from the sequence of edits/reverts this file went through).

Re-verified independently: `python3 -m pytest -q tests/test_class_hunt.py tests/test_traceability.py
tests/test_director_scenarios.py` — 206 passed, 3 skipped (external-clone-gated, expected).
`scripts/spec-style-lint.py --tier universal` on both touched files: `class-hunt.md` 0 errors/0
warnings; `director/SKILL.md` 29 errors/9 warnings, identical count to the pre-edit baseline
(confirmed by diffing lint output against `git show HEAD~1:skills/director/SKILL.md`'s own run) —
zero new errors introduced. `guardrails/check-pin-drift.sh`: exits 0, no FAIL lines.
