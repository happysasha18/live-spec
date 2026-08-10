# R2 — repetition inside the rulebook body

Root: Alexander's ask to measure how much the rulebook repeats itself, so the plan
(`.live-spec/culling-plan-v3-2026-08-10.md`) knows how much volume phase 2 (shortening)
can reclaim from repetition alone, separate from any content cut. Measured 2026-08-11.

## The body measured

Eleven skill files plus the personal profile, the same set the day-1 census priced:

| file | bytes | command |
|---|---:|---|
| `skills/build-pipeline/SKILL.md` | 64 194 | `wc -c` |
| `skills/communicator/SKILL.md` | 45 831 | `wc -c` |
| `skills/design-reviewer/SKILL.md` | 27 827 | `wc -c` |
| `skills/feedback-collector/SKILL.md` | 7 544 | `wc -c` |
| `skills/feedback-intake/SKILL.md` | 7 088 | `wc -c` |
| `skills/live-spec-base/SKILL.md` | 66 435 | `wc -c` |
| `skills/product-prover/SKILL.md` | 66 872 | `wc -c` |
| `skills/publish/SKILL.md` | 13 169 | `wc -c` |
| `skills/spec-author/SKILL.md` | 62 599 | `wc -c` |
| `skills/test-author/SKILL.md` | 18 533 | `wc -c` |
| `skills/text-audit/SKILL.md` | 30 365 | `wc -c` |
| `~/.claude/live-spec/profile.md` | 7 143 | `wc -c` |
| **total** | **417 600** | `cat <the 12 files above> \| wc -c` |

## The method

Script: `python3 repetition.py`, held at
`/private/tmp/claude-501/-Users-sashaabramovich/d733a845-a851-4115-896f-c860d235bbd8/scratchpad/repetition.py`
(a short script, per the plan's allowance, since the sentence rule needs more than one pipe stage).
It does, per file:

1. Drop fenced code blocks, table rows (lines starting `|`), horizontal rules, and a leading
   `>` blockquote marker on each line — none of these are prose sentences.
2. Collapse all whitespace, including line breaks, to single spaces.
3. Split on `.`, `!`, or `?` followed by whitespace, using the regex `(?<=[.!?])\s+`.
4. Keep a fragment as a sentence only if it is 20 characters or longer after the collapse, so
   stray headings and short bullet labels drop out.
5. Normalize each kept sentence by lowercasing and re-collapsing whitespace.
6. Count how many times each normalized sentence appears, across all twelve files together.
   A sentence appearing twice or more counts once as its first appearance and the rest as
   duplicated occurrences.
7. Byte weight of a duplicated sentence is its own byte length times (occurrences minus one) —
   the bytes that would disappear if every repeat collapsed to the one first occurrence.

A second pass runs the same steps with a looser key: markdown emphasis marks (`` ` ``, `*`, `_`,
`#`) and punctuation stripped before the count, to catch sentences that repeat with only a
formatting change (bold in one file, plain in another). This is the near-duplicate count.

## The numbers

| what it counts | value | command / source |
|---|---:|---|
| total sentences across the 12 files | 3 117 | `repetition.py`, `TOTAL_SENTENCES` |
| unique sentences (exact match) | 3 065 | `repetition.py`, `UNIQUE_SENTENCES` |
| sentences that are exact repeats of an earlier one | 52 | `repetition.py`, `DUPLICATE_OCCURRENCES` |
| groups of exact-duplicate sentences | 37 | `repetition.py`, `DUPLICATE_GROUPS` |
| bytes an exact-duplicate collapse would reclaim | 6 363 | `repetition.py`, `DUPLICATE_BYTES` |

The near-duplicate pass (markdown and punctuation stripped before comparing) finds the same 37
groups as the exact-match pass, with the same 52 repeat occurrences. No pair of sentences in this
body repeats with only a formatting change and nothing else — every repeat found is a word-for-word
copy already caught by the exact-match pass. So 6 363 bytes is the whole finding.

### Day-1 total, re-derived

The plan asks for duplicated bytes as a share of the day-1 total that
`.live-spec/day1-measures-2026-08-09.md` recorded as 73 645 bytes for measure 2 ("rulebook a
session reads before work"). That command covers a narrower body than this report — only
`skills/live-spec-base/` plus the profile, not all eleven skills. Re-run today:

`{ find skills/live-spec-base -name '*.md' -not -name 'README.md' -print0 | xargs -0 cat; cat ~/.claude/live-spec/profile.md; } | wc -c`

gives **73 578 bytes** today, close to the 73 645 recorded on day 1 (the file has taken small
edits since). Against that narrower total, the 6 363 duplicated bytes found in this report
(drawn from the larger eleven-skill body, not from `live-spec-base` alone) come to **8.7%** of it
— useful only as an order of magnitude, since the two figures cover different bodies.

Against the full body this report actually measured (417 600 bytes, the eleven skills plus the
profile), the same 6 363 duplicated bytes are **1.5%** of the total.

## What this tells the plan

Sentence-level exact repetition is small: 6 363 bytes across the whole eleven-skill body, and the
near-duplicate pass found nothing beyond that same set of 37 groups. Roughly 1 800 of those bytes
sit in a single repeated line (the pack-roster sentence), and the rest are spread thin across the
other 36 groups, one or two sentences each. Phase 2's volume goal should come from cutting or
compressing content that stands alone. Collapsing every exact repeat this report found reclaims
under 1.5% of the eleven-skill body, and under 9% of the narrower `live-spec-base` load that
measure 2 prices.

## The ten heaviest repeated sentences

Ranked by bytes reclaimed (sentence length times repeats beyond the first), from the exact-match
pass:

| bytes reclaimed | times seen | where it lives | sentence (start) |
|---:|---:|---|---|
| 1 827 | 4 | communicator, feedback-intake, live-spec-base, test-author | "The pack, whole: **live-spec-base** holds the shared rules and defaults..." |
| 351 | 4 | build-pipeline, design-reviewer, product-prover, spec-author | "Each sentence beside a code states its own rule in full, so a reader holding this page alone can pass the codes over." |
| 302 | 3 | communicator, design-reviewer, text-audit | "Four scopes settle a setting there, in this order: the session's live word, then the host profile..." |
| 296 | 2 | build-pipeline, live-spec-base | "A worker runs no command that discards uncommitted work, in any tree: `git checkout -- <path>`..." |
| 270 | 3 | communicator, design-reviewer, text-audit | "The shared working rules live once in the pack's base skill, `live-spec-base` (v4.3.0)..." |
| 257 | 2 | build-pipeline, live-spec-base | "The orchestrator owns recovery: it restores the named file from the last committed stage..." |
| 231 | 4 | build-pipeline, design-reviewer, product-prover, spec-author | "- **red**, used as a verb — a check fails and stops the work at that point." |
| 220 | 2 | build-pipeline, live-spec-base | "A worker that holds no saved bytes for a file it mutated... HALTS and reports..." |
| 212 | 2 | build-pipeline, live-spec-base | "This rule binds a worker in every tree, including its own isolated worktree..." |
| 178 | 3 | design-reviewer, product-prover, spec-author | "- **Landing** — one piece of work reaching the repository's shared truth as one commit." |

The pattern across most of these rows is the same: a working skill restates a rule that
`live-spec-base/SKILL.md` already carries in full, word for word, where a pointer to the base file
would carry the same meaning. The
pack-roster line (row 1) appears in `live-spec-base/SKILL.md` itself and three other skills that
each copy it in full. The glossary-style bullets ("- **red**...", "- **Landing**...") and the
settings-scope sentence ("Four scopes settle a setting...") are further shapes that repeat across
three or four files each.

## Reproduce

```
python3 /private/tmp/claude-501/-Users-sashaabramovich/d733a845-a851-4115-896f-c860d235bbd8/scratchpad/repetition.py
```

The file list, the sentence-split regex, and the byte-weight formula are all stated above and in
the script's own header comment.
