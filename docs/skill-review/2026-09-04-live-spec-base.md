# Skill review — live-spec-base (rule count fixed, rule 38 reply-shape, rule 36 rewritten)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-04
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Anatomy of a Skill, Progressive Disclosure, frontmatter-description accuracy, Writing Style —
applied by hand against the working tree as re-read at write time; skill-creator's own
`quick_validate.py` re-run immediately before writing this record, quoted below)

Verdict: validator passes; the description/body mismatch this record flagged earlier tonight is
now fixed on disk — nothing outstanding is folded here, and one finding (rule 36's enforcement
gap) stands, unresolved, carried forward from the earlier draft. This record holds no edit
authority over `skills/live-spec-base/SKILL.md`.

This record covers the working tree at the moment it was written, not a fixed commit —
`skills/live-spec-base/SKILL.md` is still uncommitted. Sizes read at that moment:
`skills/live-spec-base/SKILL.md` is **28,929 bytes** (this record's own re-read at write time; the
coordinator's own count agrees). The whole skill directory (`SKILL.md` + `LICENSE` + `README.md`
+ the six `references/` modules) is **61,351 bytes** total. This supersedes every earlier draft
of this record, each stale before it was read again.

## Validator

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
```

## What changed since the last draft of this record

The frontmatter `description:` now reads "twenty-four rules in the body," in place of the earlier
"twenty-three." Counted directly off the file again at this re-read: 1–10, 12–13, 16–17, 22,
24–27, 29, 31, 36, 37, 38 — **24 numbered rules**, matching the new description exactly. The
mismatch the earlier draft of this record flagged is resolved; nothing else in the file's rules
or reference-module list changed since that draft.

## Findings

1. **Description/body rule-count mismatch — resolved.** Folded. The description now states the
   count actually present (24), counted from the file rather than assumed, matching what the
   earlier draft asked for.

2. **Rule 38 belongs in the always-loaded body, not a reference module — carried forward,
   unchanged.** The six existing `references/` files (glossary, worked examples, settings ladder,
   worker-restore wording, session handover, rule-origins) share one shape: each is opened only
   "when its own kind of question needs resolving" — occasional, on-demand lookups. Rule 38
   governs the opening and shape of every reply the session sends, this one included; moving it to
   a reference a session must re-open before each reply would defeat the rule's own purpose. Rule
   36, body-resident for the same reason (who the person is, on every surface), is the closest
   comparison, and nobody proposes moving that one either. Kept in the body is the right call.

3. **Rule 36's three paragraphs carry no trailing enforcement citation, and coverage is uneven —
   carried forward, unresolved.** This is a true finding about the tree as it stands, not tied to
   either drafting pass, so it stays on the record even though the description mismatch that
   prompted the last rewrite is now fixed. Checked what actually covers each of rule 36's three
   clauses, rather than trusting the (now-removed) citation:
   - **"Blocked" narrowed to a real outside cause, and the plan's five status marks** — covered.
     `scripts/plan_checks.py` and `scripts/plan_checks_core.py` carry this in force, by their own
     comments (`plan_checks_core.py:269`: "blocked_by names a real, understood cause"; `:304`:
     "which is neither blocked... nor queued"), and `guardrails/check-board.py` also touches
     status-word matter.
   - **"A task whose content is getting the person's word" is never filed as a task or a status —
     nothing covers this.** No script or test in `guardrails/`, `scripts/`, or `hooks/` names this
     pattern. `guardrails/check-board.py` and the plan-status scripts above check that the five
     marks are used correctly once a row exists; none of them check that a "get his word" item was
     kept off the board as a row in the first place.
   - **"Report a result flat" — the banned self-congratulatory phrases — nothing covers this
     either.** The nearest existing law is `r12` in `guardrails/language-rules.json` ("no grading
     importance or quality without a concrete fact"), enforced through `hooks/register-judge.py` —
     but its own examples target evaluative adjectives ("a strong point," "far better"), not
     self-referential completion phrases like "exactly where you said," and its catcher reads
     `"armed": ["manual"]` — not a check that runs on its own. Read plainly: today, nothing
     automatically catches the phrases rule 36 now bans.
   Not folded — restoring or retargeting a citation, and building the missing checks, are edits
   to `skills/live-spec-base/SKILL.md` and its enforcement scripts, outside this review's
   write-set.

No findings against rule 38's reply shape or rule 7's nested-worker bullet on their own terms —
both state one mechanism plainly and match the file's register. Anatomy, progressive disclosure
(389 lines, still under the guide's <500-line target) and writing style all still pass. The
slimming proposal from the earlier drafts still stands unchanged: rule 7's "lane-open act"
mechanics (~220–250 bytes) and rule 22's playbook citation/worked-trigger aside (~330–360 bytes)
are both still present verbatim, so roughly 550–600 bytes remain movable into `references/`
without losing a rule — recommended, not applied.

## Follow-up, same night, after this record was written

One of the two uncovered clauses now has a reader. `tests/test_no_row_waits_on_the_person.py` reads
every open row's finish condition in `PLAN.md` and reds when the condition is somebody looking at
it, which is rule 36's ban on a task standing in for the person's word. It is red-proven against the
tree's own history rather than asserted: run over `PLAN.md` at `ead4a705` it catches three open
rows, among them `q-166`, whose acceptance read "No command decides this one; his own eye is the
check." The flat-reporting ban still has no reader, and none is planned — it governs chat, which no
file-reading check can see.
