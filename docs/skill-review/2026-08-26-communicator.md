# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over 12 skills)

Verdict: clean pass, no blocking findings; one nuance in the frontmatter/body narration framing is
worth naming even though it resolves as intentional on a close read, and the body is close enough to
the Progressive Disclosure line that a future addition should go to `references/`, not inline.

## What changed

This is not a review of a code edit. It is the plan-mandated pack-wide skill-creator pass over every
working skill ahead of PLAN.md step 8 ("Релиз наружу"), and this record covers `communicator` on its
own.

## Findings

1. **Frontmatter description** — passes. The `description` states both WHAT (show work, ask for a
   decision) and WHEN, in specific, pushy terms: a landing or milestone REPORTED, "did we do X", showing
   what the product does, raising a problem that needs the human's word — plus an explicit NOT-a-reason
   list (a passing narration line, an internal note, a plain factual answer). That is a genuinely
   specific trigger surface, not a vague one.
   One nuance worth naming: the frontmatter's NOT-list names "a passing mid-work narration line" as not
   worth loading the skill for, while the body's "When it fires" section lists narration as trigger (e)
   and devotes all of rule 13 (lines 81–144, the single longest rule in the file) to it. Read together
   these are not actually a contradiction — the NOT-list is about not loading the whole skill *solely* to
   say one passing line, while rule 13 describes a standing habit that continues once the skill is
   already in play for the session — but a fresh reader deciding whether to load the skill from the
   frontmatter alone could reasonably read the two as pulling in different directions. Not a defect, but
   worth flagging as a place the description could be one clause more explicit about the distinction.

2. **Anatomy of a Skill** — passes. SKILL.md holds the twenty-two rules and the pre-report walk;
   `references/` carries five files that do real Progressive Disclosure work rather than sitting there as
   clutter: `field-examples.md` (worked examples, forks, anti-patterns), `rule-histories.md` (the dated
   provenance behind each rule, deliberately kept out of the body), `words.md` (the glossary and the two
   numbering systems), `writing-register.md` (the eighteen-rule prose register plus its checklist), and
   `page-lifecycle.md` (the clearing walk for rendered pages). Every one of the five is linked from
   SKILL.md, and none sits over ~300 lines (largest is `writing-register.md` at 160), so none needs a
   table of contents.

3. **Progressive Disclosure** — SKILL.md is 499 lines: effectively at the ~500-line guideline ceiling.
   Nothing here is padding — the body already pushes worked examples, rule provenance, the glossary, and
   the writing register out to `references/`, and what remains inline is the rule statements themselves,
   which is the right thing to keep at the top level. Given it is already sitting on the line, the file
   has no headroom left: the next rule or clause added to the body should go to a reference file (or
   extend an existing one) rather than growing SKILL.md further.

4. **Principle of Lack of Surprise** — passes. Nothing misleading found. The body's own claim of holding
   "twenty-two rules" was checked by counting every `*(rule N)*` tag in the file: 1 through 22 are all
   present and none is skipped or duplicated, so the number in the prose is accurate, not aspirational.

5. **Writing style** — passes. Rule headers are imperative ("Show, don't describe", "Retell, don't
   reference", "Be honest about the result"), and nearly every rule states why it exists, usually pinned
   to a dated incident (2026-07-05 through 2026-08-17) rather than an assertion. The NEVER-list in rule 8
   is the one place bare prohibition-by-list appears, and it is immediately followed by a worked ❌/✅ pair
   that shows the replacement, which is the pattern skill-creator asks for.

6. **Reference-file consistency** — passes for the skill's own `references/` set: a `grep -rln` for each
   of the five filenames across the skill directory confirms every one is linked from SKILL.md, and none
   is orphaned. Separately, the pre-report walk (steps 3–5) points at `scripts/preshow-lint.py`,
   `scripts/preshow-register-lint.py`, `scripts/preshow-legibility-lint.py`, and
   `scripts/spec-style-lint.py`; these are not skill-local (there is no `communicator/scripts/`) but
   resolve at the pack repository's own root `scripts/` directory, where all four were confirmed to
   exist. That is a deliberate pack-wide convention — several skills share these lint scripts rather than
   each vendoring a copy — consistent with how the sibling build-pipeline/director skill-review record
   already treats pack-root scripts, not a communicator-specific gap.
