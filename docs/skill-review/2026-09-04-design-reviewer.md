# Skill review — design-reviewer

SKILL-REVIEW

Skill: design-reviewer

Date: 2026-09-04

Reviewer: skill-creator quality lens. The `skill-creator` skill was invoked directly (via the Skill
tool, args: "Review the skill at skills/design-reviewer for quality (structure, progressive
disclosure, frontmatter description accuracy, writing style). This is a prose/methodology skill with
no gradeable eval output — if the standard eval/benchmark loop needs a gradeable file output this
skill doesn't produce, skip that loop and run the structural/quality review instead."). The tool's own
reply confirmed its full workflow is a draft → spawn with-skill/baseline subagents on test prompts →
grade with assertions → `generate_review.py` benchmark viewer → iterate loop, built for skills with a
*gradeable file output*. `design-reviewer` produces recommendations and questions on a proven spec —
there is no fixed right answer a grader script can diff against, and this task's write-set is scoped
to `docs/skill-review/` only, with no room for a `design-reviewer-workspace/` sibling the eval loop
would need. So this record runs the structural/quality review the tool's own guide supports without
the benchmark loop: "Anatomy of a Skill", "Progressive Disclosure", frontmatter-description accuracy,
and "Writing Style", applied by hand against `skills/design-reviewer/`.

Verdict: holds up on description accuracy and writing style; one real structural finding, not folded
— this record holds no edit authority over `skills/design-reviewer/SKILL.md`.

## Size

`skills/design-reviewer/SKILL.md`: 28,164 bytes (431 lines) — the largest `SKILL.md` of the four
skills reviewed today by a wide margin (architect 201, spec-author 274, test-author 228).
Whole `skills/design-reviewer/` directory: 35,834 bytes (`SKILL.md`, `LICENSE`, `README.md` — no
`references/` folder).

## The tool's own guide, quoted

> Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of
> hierarchy along with clear pointers about where the model using the skill should go next to follow
> up.
> ...
> Reference files clearly from SKILL.md with guidance on when to read them
> ...
> These word counts are approximate and you can feel free to go longer if needed.

## Findings

1. **431 of the guide's own 500-line ceiling, and the only one of the four reviewed skills carrying
   that much body with zero reference-file offload.** `architect` (201 lines) and `spec-author` (274
   lines) both already push detail — worked examples, checklists, glossaries — into `references/`
   files pointed at from the body, exactly the pattern the guide describes ("add an additional layer
   of hierarchy along with clear pointers about where the model... should go next"). `design-reviewer`
   instead holds five self-contained, cleanly-bounded sections directly in `SKILL.md` that read as
   natural reference-file candidates by the same pattern already proven elsewhere in this pack: the
   similarity lens's five steps, the node-growth split proposal, the standing motion-parity lens, the
   standing named-part lens, and the confidence-read/echo-channel/loop-convergence mechanics (roughly
   lines 140–360, the bulk of the file). Each already opens with a clear head naming its own SPEC
   invariant, which is exactly the kind of self-contained unit the guide's "Domain organization"
   pattern splits into its own file. At 431/500 lines this skill has the least headroom of the four
   before the next real addition (a sixth lens, a new record-column value) pushes it over the guide's
   own ceiling with no split plan in place. **Not folded** — this task's write-set is
   `docs/skill-review/` only; restructuring `skills/design-reviewer/SKILL.md` is explicitly out of
   scope for this review, and a split this size is a real diff against a skill under active use, not a
   drive-by edit. Recorded as the one finding worth acting on before this skill grows further.
2. **Frontmatter description accuracy.** The description ("Use after a spec is proven to check
   whether similar features behave consistently and flag ungrouped same-kind items the spec missed.
   It holds no landing; every finding is a recommendation or a question.") matches the body's opening
   paragraph almost verbatim ("Everything you produce is a recommendation or a question. You file no
   defects and you hold up no commit.") and the "When it fires" / "Work that belongs elsewhere"
   sections below it. **No fix needed.**
3. **Writing style.** Zero hits for caps `ALWAYS`/`MUST`/`NEVER` in the body. Obligations are carried
   in lowercase prose with the reason stated alongside ("Never file a defect, never hold a landing.
   The pass produces recommendations and questions, and no blocking defects") and worked incidents are
   cited by name and date rather than asserted abstractly (the tlvphotos 2026-07-15 pinch-zoom case,
   the 2026-07-16 landscape-caption case) — matches the guide's "explain to the model why things are
   important" register. **No fix needed.**
4. **Vocabulary section doubles as a glossary already.** The "Words this skill uses" section (14
   defined terms) is exactly the shape of content `spec-author` already carries as its own
   `references/glossary.md` (53 lines). Here it stays inline, at roughly 40 lines — small enough on
   its own that inlining it is defensible, but it is also the first, and easiest, candidate section to
   move out if finding 1's split is ever taken up. **Not folded**, same reasoning as finding 1 — noted
   as part of the same future split rather than a separate action.

Findings: 4 raised. 2 clean (no fix needed). 2 real and related — both point at the same fix (split
`design-reviewer/SKILL.md` into a body plus `references/`, mirroring `architect` and `spec-author`'s
own existing pattern) — left unfolded because this review's write-set carries no authority to edit the
skill itself.
