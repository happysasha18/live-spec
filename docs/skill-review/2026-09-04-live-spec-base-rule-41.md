# Skill review — live-spec-base (rule 41 added)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/live-spec-base/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop does not fit this skill (a prose rulebook with no gradeable file output), the
same carve-out the two prior 2026-09-04 records for this skill already state.

Verdict: PASS (`quick_validate.py`, quoted below). One real, non-blocking finding, the same class
the prior rule-40 record already flagged and left unfixed for its own rule: rule 41 carries no
entry in `references/rule-origins.md` yet. Not folded here (this record holds no edit authority
over `skills/live-spec-base/`).

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
(exit 0)
```

## What changed

Since the last covering record (`docs/skill-review/2026-09-04-live-spec-base-rule-40-and-repairs.md`,
commit `bb684786`), `skills/live-spec-base/SKILL.md` changed twice more: the frontmatter
`description` count moved from "twenty-six" to "twenty-seven" rules; the shared filter paragraph
(the rule of thinking, above the numbered rules) gained four sentences narrowing what the three
channels license — reading it as licence to open work from any of the three is named as the cause
of one project's board growing by fifty rows in two days; and rule 41 itself was added — a row is
opened by the person, or by a defect someone outside this repository actually meets, tested by
naming that person and what they see.

## Findings

1. **Rule 41 has no entry in `references/rule-origins.md` yet — the same gap the rule-40 record
   already found and left for later.** That record flagged rule 40's own missing section; a rule 41
   section now belongs beside it, and the file still stops at rule 40 (`## Rule 40 —`, no `## Rule
   41 —` after it). The class recurs because the addition and the reference update are two separate
   edits, and this rule's own landing did the first without the second — exactly the shape rule 40's
   review named. Not fixed here, same reason: `references/` is outside this record's write-set.
   `recommendation · now · missing-scenario (state-space)`

2. **The filter paragraph's narrowing reads as a genuine repair, not a rewrite of the same fact
   twice.** The old text — "the three are one filter" — is literally true only for *how* an item is
   answered (its class), and the new sentences separate that from *whether* it opens work, pointing
   the reader at rule 41 by number rather than restating rule 41's own words. No duplication: the
   shared paragraph names the distinction and its consequence; rule 41 carries the mechanism. No
   finding.

3. **Frontmatter `description:` rule count verified.** Counted directly off the numbered list in
   the file at this review: 27 active numbers (1–10, 12–13, 16–17, 22, 24–27, 29, 31, 36–41 — 14
   numbers among 1–41 retired: 11, 14, 15, 18, 19, 20, 21, 23, 28, 30, 32, 33, 34, 35). The
   description's "twenty-seven" is correct. No finding.

4. **Progressive Disclosure and Anatomy.** `SKILL.md` is now 35,276 bytes (up from 31,995 at the
   last review), still under the guide's ~500-line ideal by line count and needing no in-file table
   of contents. Rule 41's own closing line — "prose-only, no dedicated check" — states its own
   enforcement boundary in the body, matching how every other prose-only rule in this file names
   its own status rather than leaving it implicit. No finding.

5. **Writing Style.** Rule 41 opens with its instruction and the door test in the same two
   sentences, then its reasoning, then its own worked numbers (the two boards, 2026-09-04) —
   consistent with the file's own register elsewhere (reasoning stated, not asserted; a cited
   measurement rather than a claim). No bare imperative, no capitalised MUST, no birth-story
   smuggled into the instruction itself — the history sits in its own paragraph, clearly marked as
   history ("This rule exists because..."). No finding.

## Size

```
$ wc -c skills/live-spec-base/SKILL.md
   35276 skills/live-spec-base/SKILL.md
```

```
$ find skills/live-spec-base -type f -exec wc -c {} + | tail -1
   69184 total
```

`skills/live-spec-base/SKILL.md`: 35,276 bytes. `skills/live-spec-base/` (whole directory —
`SKILL.md`, `LICENSE`, `README.md`, and the six `references/` files): 69,184 bytes.
