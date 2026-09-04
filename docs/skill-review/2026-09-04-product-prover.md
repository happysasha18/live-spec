# Skill review — product-prover

SKILL-REVIEW

Skill: product-prover

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/product-prover/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop (spawn with-skill vs. baseline subagents, grade assertions against a
gradeable file output, benchmark) does not fit here: product-prover is a prose-and-methodology
review skill whose output is a judgment call over a spec, not a gradeable file artifact a script
could check — the structural review below is what skill-creator actually supports for a skill of
this shape. This is an external skill with its own upstream history, vendored under
`skills/product-prover/` (its own `.git`, `CHANGELOG.md`, `PROVENANCE.md`); this record holds no
edit authority over its files and folds nothing into them.

Verdict: PASS (`quick_validate.py`, quoted below) — two real, not-blocking findings on progressive
disclosure and one on frontmatter-description coverage, none folded here.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/product-prover
Skill is valid!
(exit 0)
```

`quick_validate.py` is Anthropic's own packaging validator (the same check `package_skill.py` runs
before producing a `.skill` file): frontmatter YAML parses, only allowed keys are present, `name` is
kebab-case, `description` is ≤1024 characters with no angle brackets. All pass; no scriptable defect
found.

## What changed

Nothing in this skill's body changed today. This record exists to close a gap, not to cover an
edit: `product-prover` was the one skill under `skills/` the 2026-09-04 pass had not reached — its
newest prior record was `docs/skill-review/2026-07-18-product-prover.md`, while every sibling skill
already carries a record dated today. PLAN row q-817 asks that every skill go through
Anthropic's `skill-creator` once, its own verdict quoted; this record is that pass for
`product-prover`.

## Findings

1. **`SKILL.md` runs 734 lines, above the ~500-line "ideal" the Skill Writing Guide names.** Not a
   bare wall of text, though: five `reference/` files (`stress-lenses.md` 437 lines,
   `review-modes.md` 139, `code-lenses.md` 82, `architecture-lens.md` 48, `glossary-terms.md` 24 —
   730 lines total) already carry phase-specific and mode-specific detail out of the main body, and
   the body itself points to them by name at the moment each is needed (e.g. "Its seven lenses...
   live in `reference/review-modes.md`. Open it once this mode is chosen."). The Anatomy pattern is
   followed correctly; the raw line count is still over guide-ideal. **Not folded** — vendored,
   edit authority sits upstream.
2. **`reference/stress-lenses.md` is 437 lines with no table of contents.** The guide calls for one
   past the 300-line threshold on a reference file; this file has none. A reader opening it mid-pass
   (as Phase 3 sends them to do) has to scroll rather than jump. **Not folded** — same reason as
   above.
3. **Frontmatter `description:` does not name Glossary mode.** The description (498 of 1024
   characters used) covers the review-and-critique surface and Code mode fully, but says nothing
   about `## Glossary mode` (SKILL.md lines 699–724): a standalone plain-English lookup ("glossary",
   "define atomicity", "what does liveness mean?") that answers without running a review at all. A
   request shaped exactly like that trigger list, arriving with no review context, has nothing in
   the description pointing this skill at it. **Not folded** — vendored; a description clause
   naming glossary lookups would close the gap on a future upstream release.
4. **Writing style checks out clean.** No bare `MUST`/`ALWAYS`/`NEVER` all-caps imperatives found
   (`grep -c` returns 0 for each); rules are stated with their reasoning attached (e.g. "A standard
   nobody stated is never applied as though they had stated it," "That makes the outcome verifiable
   after memory is gone"). Consistent with the guide's "explain the why" preference. No finding.
5. **Anatomy and domain organization are sound.** `scripts/validate.py` (3,334 bytes) is the only
   bundled script and matches the "executable code for deterministic tasks" pattern; `reference/`
   holds only what Phase-specific detail should live outside the main body; no speculative
   `assets/`. No finding.

## Size

```
$ wc -c skills/product-prover/SKILL.md
   42989 skills/product-prover/SKILL.md
```

`skills/product-prover/SKILL.md`: 42,989 bytes (734 lines).

```
$ find skills/product-prover -type f -not -path '*/.git/*' -print0 | xargs -0 wc -c | tail -1
  267706 total
```

`skills/product-prover/` content (all files except the vendored `.git/` history — SKILL.md,
README.md, CHANGELOG.md, LICENSE, PROVENANCE.md, docs/, evals/, examples/, reference/, scripts/):
267,706 bytes.

```
$ find skills/product-prover -type f -print0 | xargs -0 wc -c | tail -1
  872425 total
```

`skills/product-prover/` whole directory including its vendored `.git/` (this skill carries its own
upstream git history and object pack, per the task note that it is "an external skill with its own
history, vendored here"): 872,425 bytes. The `.git/` subtree accounts for the difference
(872,425 − 267,706 = 604,719 bytes) and is upstream repository history, not skill content.
