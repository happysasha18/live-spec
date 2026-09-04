# Skill review — live-spec-base (rule 40 added, three cold-reader repairs)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/live-spec-base/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop (spawn with-skill vs. baseline subagents, grade assertions against a
gradeable file output, benchmark) does not fit here: live-spec-base is a prose rulebook with no
file artifact it produces that a grader could check — the structural and quality review below is
what skill-creator actually supports for a skill of this shape.

Verdict: PASS (`quick_validate.py`, quoted below) — both today's edits read clean; one real,
non-blocking finding on `references/rule-origins.md` not yet carrying an entry for the new rule,
not folded here (this record holds no edit authority over `skills/live-spec-base/`).

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
(exit 0)
```

`quick_validate.py` is Anthropic's own packaging validator (the same check `package_skill.py` runs
before producing a `.skill` file): frontmatter YAML parses, only allowed keys are present, `name`
is kebab-case, `description` is ≤1024 characters with no angle brackets. All pass; no scriptable
defect found.

## What changed

Today's edits to `skills/live-spec-base/SKILL.md` are two. First, rule 40 was added: the person is
the client, and checking the work is never their job — no row's finish condition is their
attention, only an irreversible act or a taste-fork still stops for their word. Second, three
places two independent cold readers both stopped on were repaired: "each number is retired and
stays open" became "retired and left as a hole, never given to a new rule" (line ~60, the retired-
rule-numbers note); rule 7's undefined capitalised "PEN" became the lowercase "pen" with its own
definition folded in at first use — "the right to write the shared truth, held by one lane at a
time" — where before the term was used without ever being defined; and rule 31's clause "a fault it
lived in that zone carried with its evidence" became "a fault the sender itself ran into in that
zone, carried with its evidence," replacing an ambiguous "it" with a named actor.

## Findings

1. **Rule 40 has no entry in `references/rule-origins.md`.** The base's own claim (line 58) is that
   "each rule's background — citation, history, justification, and worked example — lives in
   `references/rule-origins.md`, opened only to dispute or amend a rule." Read that file end to
   end: it runs through rule 39 ("## Rule 39 — nothing new is built to serve the process itself,"
   entered 2026-09-04) and stops there — no "## Rule 40" section exists yet, so the newest rule is
   the one rule in the body with no citation, history, or worked example behind it. **Not fixed
   here** — adding that section is an edit to `references/rule-origins.md`, outside this record's
   write-set (`docs/skill-review/` only); flagging for whenever this reference file is next opened
   for a real reason. Every other active rule (1–10, 12–13, 16–17, 22, 24–27, 29, 31, 36–39) has a
   matching section there; rule 40 is the sole gap.

2. **Both repairs read as intended and cost nothing structurally.** "Retired and left as a hole,
   never given to a new rule" reads as a plain restatement of the same fact the old wording named
   ("stays open" was the ambiguous half — open to what, was unclear on a cold read); the new wording
   removes that ambiguity without changing what actually happens to a retired number. The pen fix
   is a net improvement beyond just being defined: `references/glossary.md:32` already carries its
   own entry, "the pen — the single write-lock a repository holds, under which one delivery reaches
   ..." — the body's fix (lowercase, defined at first use, "SPEC INV-39" cited) now agrees with the
   glossary's own term instead of introducing a second, capitalised, uncited name for the same
   thing. The rule 31 fix names the actor ("the sender itself") the earlier clause's bare "it" left
   floating between two candidate antecedents (the sender, or the zone). No finding against any of
   the three; all three are pure readability repairs with no rule-count, cross-reference, or
   enforcement-script impact.

3. **Frontmatter `description:` rule count still correct.** The description states "twenty-six
   rules in the body." Counted directly off the file at this review: 1–10, 12–13, 16–17, 22,
   24–27, 29, 31, 36–40 — 26 numbered rules (14 numbers among 1–40 are retired: 11, 14, 15, 18, 19,
   20, 21, 23, 28, 30, 32, 33, 34, 35). Rule 40's addition did not change the count the description
   already claimed, since it lands on a number never retired. No finding.

4. **Progressive Disclosure and Anatomy.** `SKILL.md` is 427 lines (31,995 bytes), under the
   guide's ~500-line ideal and under the 300-line threshold that would call for an in-file table of
   contents — none is present, and none is needed at this length. Six `references/` modules exist
   (glossary, worked examples, settings ladder, worker-restore wording, session handover,
   rule-origins), each opened, by the body's own words, "only when its own kind of question needs
   resolving" — the on-demand shape the guide asks for. No finding beyond item 1 above (a content
   gap in one reference module, not a structural defect in the split itself).

5. **Writing Style.** Rule 40 states its own reasoning before its instruction ("Taking a piece of
   work means knowing how it will be checked..."), consistent with every other rule in the file;
   no bare imperative, no heavy-handed capitalised MUST. The two repaired clauses read as plain
   prose after the fix, matching the file's own register elsewhere. No finding.

## Size

```
$ wc -c skills/live-spec-base/SKILL.md
   31995 skills/live-spec-base/SKILL.md
```

```
$ find skills/live-spec-base -type f -exec wc -c {} + | tail -1
   64806 total
```

`skills/live-spec-base/SKILL.md`: 31,995 bytes, 427 lines. `skills/live-spec-base/` (whole
directory — `SKILL.md`, `LICENSE`, `README.md`, and the six `references/` files): 64,806 bytes.
