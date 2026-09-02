# q-809 — session start-up weight, and every standing file

**Root:** his word 2026-09-02: "80кб много. можно удешевить? раза в 4?" and "зачем decision если
есть доска и journal? нам точно все файлы нужны?"

## Measured before

`scripts/state-probe.sh` line: required context (boot + profile + base + director) = 18501 tokens,
80122 bytes.

| file | bytes |
|---|---|
| `~/.claude/CLAUDE.md` | 4386 |
| `~/.claude/live-spec/profile.md` | 9680 |
| `~/.claude/skills/live-spec-base/SKILL.md` | 40443 |
| `~/.claude/skills/director/SKILL.md` | 25613 |

Inside live-spec-base, one section carries 34436 of the 40443: `## The shared rules`, 22 rules.
Inside director, the two heavy sections are `## First — what did the human just do?` (6088) and
`## Execution` (5277); director already keeps 13 reference files (44 KB) outside the loaded body.

Target: ~20 KB loaded, no rule lost.

## Method

The pattern is already in the tree: live-spec-base keeps the glossary, the worked examples and the
settings ladder in `references/`, opened only when a question needs them. Extend it. What a session
needs at start is the rule as an instruction. What it needs rarely is the rule's history, its dated
citation, its justification, and its worked example. Those move to a reference file per document;
the loaded body keeps one imperative statement per rule plus the pointer.

## Steps

1. ⬜ Per-rule inventory of the 22 shared rules — core sentence, byte count, what the rest is.
2. ⬜ Same inventory for director, profile, boot file.
3. ⬜ Standing-file census: every standing document, one line on what breaks if it is gone.
4. ⬜ Judge and cut.
5. ⬜ skill-creator over each skill touched.
6. ⬜ Re-measure with the same probe line; land the row.
