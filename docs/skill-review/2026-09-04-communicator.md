# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/communicator/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop (spawn with-skill vs. baseline subagents, grade assertions, benchmark) needs a
gradeable file output to compare against; communicator is a prose/conversation skill with no such
artifact, so that loop does not apply here — the structural review below is what skill-creator
actually supports for a skill of this shape.

Verdict: one real finding (invalid frontmatter YAML — quoted below), not folded — this record holds
no edit authority over `skills/communicator/SKILL.md`.

## Concurrent-edit note

Per the brief for this review round: communicator may be edited by another lane while read. Checked
`skills/communicator/SKILL.md` byte count and md5 at the start of this review and again immediately
before writing this record — both reads returned 48934 bytes, md5 `140bb0add4ef02a6ee234ba07454dd97`,
unchanged across the window. `git status --short` shows the file as modified (uncommitted) against
HEAD (`d0bbc72b`, 2026-09-02) — this record covers the working-tree snapshot at those bytes, not a
committed state. A push-gate freshness check will need a record dated at or after whatever commit
actually lands.

## The tool's own verdict

```
$ python3 scripts/quick_validate.py skills/communicator
Invalid YAML in frontmatter: mapping values are not allowed here
  in "<unicode string>", line 2, column 249:
     ... ir word. NOT a reason to LOAD it: a passing mid-work narration l ... 
                                         ^
(exit 1)
```

## Sizes

- `skills/communicator/SKILL.md`: 48934 bytes, 498 lines.
- `skills/communicator/` (whole directory, `wc -c` summed over all files): 90704 bytes.

## Findings

1. **Frontmatter `description:` is invalid YAML.** The description is an unquoted plain scalar, and
   it contains a colon followed by a space — `...NOT a reason to LOAD it: a passing mid-work
   narration line...` — which YAML's plain-scalar grammar reads as a nested mapping key, not literal
   text. `quick_validate.py` (Anthropic's own packaging validator) refuses to parse the frontmatter
   at all over this. **Fix it:** quote the description string (`description: "..."`) or reword past
   the bare colon (e.g. "an internal working note" instead of "LOAD it:"); either is a one-line
   change and this is exactly what the real packager (`package_skill.py`, which calls the same
   frontmatter parse) would choke on before a publish.
2. **SKILL.md is 498 lines** — the skill-creator guide's own "<500 lines ideal" ceiling, one line
   under it. **Not a fix:** the file already delegates five reference files under `references/`
   (`field-examples.md`, `writing-register.md`, `words.md`, `rule-histories.md`,
   `page-lifecycle.md`, 575 lines / 38198 bytes combined) — sitting at the edge is the shape of a
   file that already offloads what it can, not a file that needs another split.
3. **One `NEVER` in all-caps** (skill-creator's own "yellow flag" for heavy-handed MUSTs). **Not a
   fix:** a single instance across 498 lines is not the pattern the guide warns against; the body
   otherwise explains its reasoning rather than issuing bare imperatives.
4. **Frontmatter description matches the body.** Checked the opening section against the
   `description:` line's claims (show work, ask a decision, the NOT-a-reason-to-load carve-out) —
   they line up; no finding.
