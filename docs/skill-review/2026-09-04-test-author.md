# Skill review — test-author

SKILL-REVIEW

Skill: test-author

Date: 2026-09-04

Reviewer: skill-creator quality lens. The `skill-creator` skill was invoked directly (via the Skill
tool, args: "Review the skill at skills/test-author for quality (structure, progressive disclosure,
frontmatter description accuracy, writing style). This is a prose/methodology skill with no gradeable
eval output — if the standard eval/benchmark loop needs a gradeable file output this skill doesn't
produce, skip that loop and run the structural/quality review instead."). The tool's own reply
confirmed its full workflow is a draft → spawn with-skill/baseline subagents on test prompts → grade
with assertions → `generate_review.py` benchmark viewer → iterate loop, built for skills with a
*gradeable file output*. `test-author` produces a derived matrix and judgment calls about test levels
— there is no fixed right answer a grader script can diff against, and this task's write-set is
scoped to `docs/skill-review/` only, with no room for a `test-author-workspace/` sibling the eval loop
would need. So this record runs the structural/quality review the tool's own guide supports without
the benchmark loop: "Anatomy of a Skill", "Progressive Disclosure", frontmatter-description accuracy,
and "Writing Style", applied by hand against `skills/test-author/`.

Verdict: holds up — no findings that call for a fix.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/test-author
Skill is valid!
(exit 0)
```

## Size

`skills/test-author/SKILL.md`: 18,827 bytes (228 lines).
Whole `skills/test-author/` directory: 26,300 bytes (`SKILL.md`, `LICENSE`, `README.md` — no
`references/` folder).

## The tool's own guide, quoted

> Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of
> hierarchy along with clear pointers about where the model using the skill should go next to follow
> up.
> ...
> **description**: When to trigger, what it does. ... All "when to use" info goes here, not in the
> body.
> ...
> Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs.

## Findings

1. **Length and the choice to hold everything in `SKILL.md` with no `references/` split.** 228 lines
   is under half the tool's 500-line ceiling — nowhere near the point the guide says to "add an
   additional layer of hierarchy." Unlike `architect` and `spec-author` (reviewed the same day, both
   of which shed detail into reference files), `test-author` carries its whole level ladder, the
   ladder's four invariant rules (SPEC INV-135, INV-128, INV-101, INV-77), and the test-writing
   checklist in the body directly. At 228 lines this is a legitimate choice under the guide's own
   threshold, not a violation of it — the guide's split trigger is line count, and this file is well
   short of it. **No fix needed**, but it is the one of the four reviewed skills with the least
   headroom before a future addition would tip it toward needing the same reference-file split
   `spec-author` already uses.
2. **Frontmatter description accuracy.** The description ("Use to derive a test matrix and write
   tests from a proven spec and architecture. Not a substitute for reviewing the spec itself.") is
   short and matches the body's own "Work that belongs elsewhere" section: "Use it only with a proven
   spec and architecture... Not for reviewing documents (product-prover's job)." **No fix needed.**
3. **Writing style.** Zero hits for caps `ALWAYS`/`MUST`/`NEVER` — the file states obligations with
   reasons attached in lowercase prose ("Never edit a test to make a change pass. A red test means the
   change or the matrix cell is wrong"). One place uses emphasis-caps mid-sentence for a specific
   technical contrast rather than a blanket command ("proves the code SAYS the right thing while the
   page showed the wrong one") — this is the guide's own permitted "Examples pattern" register, not
   the "heavy-handed musty MUSTs" it warns against. **No fix needed.**
4. **Credits and borrowing are named plainly** ("paraphrased from track-coach's matrix (MIT,
   credited)"), which the guide does not require but which strengthens, rather than weakens, the
   "Writing Style" section's call for honesty about where a pattern came from. **No fix needed.**

No findings against this skill required a fix; none were folded because none were raised.
