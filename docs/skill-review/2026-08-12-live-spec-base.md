# Skill review — live-spec-base (rule 30 cut, its number left a hole)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author
the cut, and it wrote no file but this record. Base rule 33 asks for that freshness.

Verdict: passes as a skill. The description agrees with the body, no neighbour rule lost meaning, and
nothing under `skills/` still points at the cut rule. Two findings are recommendations, one of them a
one-clause repair the reviewer would make before the next release; neither blocks the push.

## What changed

Commit `3866a6c` cut rule 30 whole from `skills/live-spec-base/SKILL.md` — the generator rule, which
said any machine-verifiable quality is shipped as a blocking gate. The number is left standing as a
hole between rules 29 and 31, so every citation elsewhere keeps pointing at the number it names. The
frontmatter description moved from thirty-five rules in the body to thirty-four. Nothing else in the
file changed.

## Findings

1. **The count is true as a tally and misleading as a numbering claim.** Recommended repair, one
   clause. The body holds 34 numbered heads, and they run 1 to 35 with 30 absent. No sentence in the
   skill says a number was retired. A reader who reaches rule 35 and reads thirty-four rules in the
   description has nothing in the file to reconcile the two with. The hole is recorded in
   `DECISIONS.md`, in `NEXT_STEPS.md` and in the docstring of `test_base_description_counts_the_rule`,
   and none of those three travels to an adopting host: `scripts/sync-skills.sh` copies skill
   directories only. One clause at the head of the shared rules, or in the description, closes it.

2. **The birth of a check is now stated in no skill file.** Recorded, deferred, and named here for
   its reach. Cut rule 30 was the pack's only host-facing sentence on when a gate is minted. Its
   replacement clause lives in `PRODUCT_SPEC.md` at the INV-164 requirement — mint no gate from the
   sole fact that a quality is machine-verifiable, open a check where a standing rule has broken a
   second time or the owner has asked. A host receives skills, not the spec. Rule 23 carries the
   nearest half: a behavioural rule that breaks mid-turn twice earns a live channel. It does not reach
   document drift, and it does not name the owner's word as a second birth channel. `DECISIONS.md`
   already records the rule-23 broadening as a campaign-close post-action on the owner's word of
   2026-08-11, so the gap is a known interim, not a new one.

3. **The neighbours read whole.** Reviewed and clear. Rules 29 and 31 stand complete, and neither
   leaned on rule 30. A grep of every file of this skill for the cut rule's number, its invariant code
   and its wording — the phrases about a machine verifying a quality and a quality left to attention —
   returns nothing. The same grep across all eleven skills of the pack returns one unrelated hit in
   `spec-author` about a machine-checkable tag form.

4. **The cut closes a tension an earlier review recorded.** Reviewed and clear. Finding 2 of
   `docs/skill-review/2026-08-09-live-spec-base.md` said rule 35 carried a stated exception — both
   ends of a session stay a discipline the seat holds — against rule 30, which admitted none. Rule 35
   is unchanged and now stands against no such clause.

5. **One live pointer to the cut rule survives outside this skill.** Named, not this skill's to fix.
   `MIGRATION.md` line 125, in the 2.0.0 chapter, tells a host the method rule is rule 30 in
   `skills/live-spec-base/SKILL.md`. The path resolves and the rule is gone. `NEXT_STEPS.md` and
   `DECISIONS.md` both record that a migration chapter is owed at the next release for exactly this.

## The measures this review was held to

The census reads `skills/live-spec-base/SKILL.md` at 74 findings after the cut — 60 sentences past the
word cap, 14 style findings, no register findings — level with the 74 the same file measured before
it, so the cut removed no over-cap sentence and added none. The file measures 65,496 bytes against
66,435 before, which matches the figure `DECISIONS.md` records for this slice. The loadability gate
reports eleven skills loading, named, versioned and negative-scoped. The findings-bound gate reports
no document above its record. The four test files this commit touched pass, 36 of 36. The installed
copy at `~/.claude/skills/live-spec-base` is byte-identical to the repository copy.
