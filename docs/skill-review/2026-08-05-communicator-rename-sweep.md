# Skill review addendum — the communicator rename sweep reaches its remaining spots

`SKILL-REVIEW`

Skills: communicator.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes — the sweep is complete.

`docs/skill-review/2026-08-05-communicator.md` found that commit 83ebd2d renamed "station" to "step" in
rule 13. The old word remained in the skill's own glossary and worked example, in rule 14's
pointer, and in the live-status tooth. It remained, too, in the departures-board criterion, which
lives in `TEST_MATRIX.md` and a test docstring (findings 2, 4, and 6). This pass swept
`references/words.md`, `references/field-examples.md`, SKILL.md's rule 14 pointer and live-status
tooth, `TEST_MATRIX.md` row M-112, and `tests/test_report_format.py`'s docstring to the plain word.
Rule 13's own teeth (finding 3) were left on the old word, since `tests/test_traceability.py` pins
that exact phrasing and stood outside this pass's write-set. The 396 tests that read this skill
pass, and the register lint, one-name check, and `guardrails/check-skill-review.sh` all read the
skill clean.
