# Skill review — live-spec-base (rule 43 added, budgets)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-08
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/scripts/quick_validate.py`,
plus the skill-creator Skill Writing Guide applied by hand (the eval/iterate loop does not fit a
prose rulebook, the same carve-out earlier records for this skill state).

Verdict: PASS (`quick_validate.py`, quoted below). Two real, non-blocking findings: rule 43 carries
no entry in `references/rule-origins.md` and cites no incident or outside source inline, the same
gap the rule-40 and rule-41 records already flagged for their own rules and left unfixed; and rule
43's paragraph is hard-wrapped several characters narrower than every neighbouring rule in the
file, a cosmetic inconsistency. Neither is folded here (this record holds no edit authority over
`skills/live-spec-base/`).

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
(exit 0)
```

## What changed

`skills/live-spec-base/SKILL.md` gained rule 43 — a budget is a named, finite set of work, never
certified by a clock, host load, a quiet-machine comparison, p50/p95 figures, or any single
measurement; a timeout is an emergency stop, not a verdict; a performance measurement only settles
anything inside the controlled environment a stated product performance requirement declares. The
frontmatter `description` rule count moved from "twenty-eight" to "twenty-nine" to match.

## Findings

1. **Rule 43 has no entry in `references/rule-origins.md`, and states no inline source or incident
   either.** `references/rule-origins.md` stops at "## Rule 41" (grep confirms no "Rule 42" or
   "Rule 43" heading); rule 42, landed earlier, has the same gap, so this is not new to rule 43
   alone. But rule 43 is also unlike its immediate neighbours in the body itself: rule 38 states
   "This cost four stalled lanes in one night before it was written down," rule 39 requires that no
   new threshold "enters the tree without an outside source or an incident that already happened,"
   and rule 41 closes with a pointer to `rule-origins.md` for its own history. Rule 43 states its
   instruction and reasoning but names no dated incident, no owner's word, and no pointer to where
   either lives — the same class of gap the rule-40 and rule-41 records already raised for their
   own rules and left for a later pass. `recommendation · now · missing-scenario (state-space)`

2. **Rule 43's paragraph is wrapped narrower than the rest of the file.** Every other rule in this
   section (36 through 42) wraps its lines at roughly 90–100 characters; rule 43's five body lines
   wrap at 80–88. The content is unaffected — this is a soft-wrap inconsistency only, visible on a
   raw diff of the file — but it is the kind of thing a text-audit pass over this file would flag,
   and no other rule in the surrounding block has it. `recommendation · cosmetic`

3. **No collision with rule 39.** Rule 39 forbids inventing a new gate, hook, counter, threshold,
   registry or exception list without an outside source or incident, and requires any existing
   threshold to move only downward. Rule 43 does not introduce a threshold, counter, or gate of its
   own — it states what a budget must be (a named, finite set) and what a clock or host measurement
   can never do (certify one). The two rules sit in the same territory — both distrust an
   invented, ungrounded number — but neither restates the other, and neither's instruction
   contradicts the other's. No finding.

4. **No collision with rule 42.** Rule 42 forbids rewriting a done to fit what already shipped;
   rule 43 is about what evidence certifies a budget. Disjoint subjects. No finding.

5. **Frontmatter rule count verified.** 29 active numbers counted directly off the file's own
   numbered list at this review (1–10, 12–13, 16–17, 22, 24–27, 29, 31, 36–43). The description's
   "twenty-nine" is correct. No finding.

6. **Writing Style.** Rule 43 opens with its instruction, then what a budget is not read off, then
   what a fixed budget is, then what a timeout is, then where a performance measurement is valid —
   consistent with the file's register elsewhere (instruction first, reasoning after). No bare
   imperative, no capitalised MUST. It is also the one rule in this stretch with no worked example
   and no dated citation, which is finding 1 above stated in Writing-Style terms rather than a
   second, separate defect.

## Size

```
$ wc -c skills/live-spec-base/SKILL.md
   35290 skills/live-spec-base/SKILL.md
```

Well under the guide's ~500-line ideal by line count; no in-file table of contents needed.

## Follow-up

Finding 1's missing-origin recommendation was acted on the same night: rule 43 now has an entry
in `skills/live-spec-base/references/rule-origins.md`, under the heading "Rule 43 — a budget is a
named, finite set of work, and a clock never certifies one".
