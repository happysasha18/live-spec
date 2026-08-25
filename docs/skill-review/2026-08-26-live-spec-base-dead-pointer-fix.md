# Skill review — live-spec-base

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is reserved for Полоса B п.10, after the whole build-pipeline
cutover completes, per the owner's explicit instruction not to skip that step)

Verdict: no blocking findings; frontmatter unchanged, one body sentence corrected.

## What changed

Полоса B п.9's final wide sweep (grep across TEST_MATRIX.md, ARCHITECTURE.md, adopt/,
MIGRATION.md, and other skills' rosters for cutover leftovers) found that base rule 14 (the class
hunt a confirmed bug drives before it closes, INV-124) still named `skills/build-pipeline/
SKILL.md`'s bug entry as one of the four-move law's homes, even though that prose fully moved to
`skills/director/references/class-hunt.md` earlier in the build-pipeline cutover — confirmed by
grep that `skills/build-pipeline/SKILL.md` (now 66 lines) carries no mention of "bug" anywhere.
Fixed the sentence to name only the current home (`director/references/class-hunt.md`) and the
spec anchor (INV-124), dropping the dead build-pipeline reference. `skills/live-spec-base/
SKILL.md` loads before every session of every skill in the pack, so a stale pointer here carries
real operational cost even though no test's assertion depended on the exact wording (confirmed:
`tests/test_class_hunt.py::test_base_rule_14_goes_and_finds_the_class` checks different phrases
in the same rule, not this sentence).

## Findings

None blocking, after one round of independent review caught an unswept sibling. Per-skill check:

- **live-spec-base** — frontmatter `description` (unchanged) still accurately describes the
  skill's scope (shared rules, settings ladder, three reference modules). The corrected sentence
  reads coherently in context (verified: lines 216-230 read as one continuous paragraph, no
  broken line-wrap), matches the file's existing register (a flat list of homes, no embedded
  migration history — the file carries no other "formerly/moved from" phrasing anywhere, so an
  initial draft that added a parenthetical "(moved there from build-pipeline in the build-pipeline
  cutover)" was dropped as stylistically foreign to this evergreen rulebook; that kind of
  process-historical annotation belongs in dated records like `docs/prover/`/`docs/director/
  capability-map.md`, not in a rule a session reads with no time context). The edit shortens the
  file by one line (228-229 → 228 alone); `guardrails/check-pin-drift.sh` confirmed green with
  every line-pin (tolerance ±2 lines) still resolving, independently re-checked by the second
  reviewer round.

Independent adversarial review (a fresh reviewer instructed to find grounds to reject) ran twice
on this single-sentence fix. First round: **BLOCK** — its own grep for the same dead phrase
across the repo (the same discipline base rule 14 itself demands: "fix all siblings in the same
change... since one instance reported means the whole class is owned") found that `tests/
test_class_hunt.py`'s module docstring (lines 7-9) still listed "build-pipeline's bug entry" as a
live parallel home alongside "director's own reference," even though that test's own body
(`test_build_pipeline_bug_entry_drives_the_hunt`) had already been redirected to check director's
file in an earlier commit (`dadb67db`) — the docstring was never updated to match. Also flagged
the parenthetical historical gloss as stylistically foreign to live-spec-base's register. Both
fixed: the docstring now says "director's own reference (moved there from build-pipeline's former
bug entry in the build-pipeline cutover)" — correctly historicized with "former," no longer
implying a live parallel home — and the SKILL.md sentence dropped the parenthetical entirely.
Second round (same reviewer, re-verifying its own prior findings, not taken on trust): **ALLOW**
— re-ran the same grep (one hit remaining, the now-correctly-historicized docstring line itself,
expected and safe), re-ran the same test target (196 passed, 3 skipped), re-confirmed pin-drift
green independently. No findings remain.
