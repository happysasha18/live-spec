# Measurements — one row per file, every indicator

Generated 2026-08-28 by `python3 scripts/measurements-table.py`. This table is the source of truth for where the work stands. Add `--html` to also build `docs/MEASUREMENTS.html`, the page to read it on — a transient render, swept once its reading closes (SPEC INV-286).

| # | file | state | both stopped | readers ok | find | script ok | est h | cum h | reads | long | style | lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **The text that enters every turn** ||||||||||||
| 1 | `hooks/chat-law-hook.sh` | open | n/m | no | n/m | n/m | 2.3 | 2 | 1 | n/m | n/m | 9 |
| | **The text that enters every session at its start** ||||||||||||
| 2 | `~/.claude/CLAUDE.md` | open | — | n/m | n/m | n/m | 2.3 | 5 | 0 | n/m | n/m | n/m |
| 3 | `~/.claude/live-spec/profile.md` | open | — | n/m | n/m | n/m | 2.3 | 7 | 0 | n/m | n/m | n/m |
| | **The file every session reads first** ||||||||||||
| 4 | `NEXT_STEPS.md` | open | — | n/m | n/m | n/m | 2.3 | 9 | 0 | n/m | n/m | 156 |
| | **The four documents behind the language rules (text-audit itself moved to its own repository, 2026-08-18 — skills/text-audit-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)** ||||||||||||
| 5 | `docs/language-rules.md` | open | n/m | no | n/m | n/m | 2.3 | 12 | 2 | n/m | n/m | 1,078 |
| 6 | `docs/spec-style.md` | open | — | n/m | n/m | n/m | 2.3 | 14 | 0 | n/m | n/m | 152 |
| 7 | `docs/spec-format.md` | open | — | n/m | n/m | n/m | 2.3 | 16 | 0 | n/m | n/m | 76 |
| 8 | `docs/language-worked-example.md` | open | — | n/m | n/m | n/m | 2.3 | 19 | 0 | n/m | n/m | 636 |
| | **The three skills loaded in every task run by the method** ||||||||||||
| 9 | `skills/live-spec-base/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 21 | 0 | n/m | n/m | 451 |
| 10 | `skills/build-pipeline/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 23 | 0 | n/m | n/m | 68 |
| 11 | `skills/communicator/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 25 | 0 | n/m | n/m | 500 |
| | **PLAN.md, read whenever a session picks up work** ||||||||||||
| 12 | `PLAN.md` | open | — | n/m | n/m | n/m | 2.3 | 28 | 0 | n/m | n/m | 1,679 |
| | **The remaining six skills (product-prover moved to its own repository, 2026-08-13 — skills/product-prover-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)** ||||||||||||
| 13 | `skills/design-reviewer/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 30 | 0 | n/m | n/m | 431 |
| 14 | `skills/feedback-collector/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 32 | 0 | n/m | n/m | 143 |
| 15 | `skills/feedback-intake/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 35 | 0 | n/m | n/m | 105 |
| 16 | `skills/publish/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 37 | 0 | n/m | n/m | 175 |
| 17 | `skills/spec-author/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 39 | 0 | n/m | n/m | 277 |
| 18 | `skills/test-author/SKILL.md` | open | — | n/m | n/m | n/m | 2.3 | 42 | 0 | n/m | n/m | 231 |
| | **The specification family** ||||||||||||
| 19 | `PRODUCT_SPEC.md` | open | — | n/m | n/m | n/m | 2.3 | 44 | 0 | n/m | n/m | 307 |
| 20 | `ARCHITECTURE.md` | open | — | n/m | n/m | n/m | 2.3 | 46 | 0 | n/m | n/m | 69 |
| 21 | `TEST_MATRIX.md` | open | — | n/m | n/m | n/m | 2.3 | 49 | 0 | n/m | n/m | 160 |
| | **The documents a stranger meets on arrival** ||||||||||||
| 22 | `README.md` | open | — | n/m | n/m | n/m | 2.3 | 51 | 0 | n/m | n/m | 237 |
| 23 | `OVERVIEW.md` | open | — | n/m | n/m | n/m | 2.3 | 53 | 0 | n/m | n/m | 128 |
| 24 | `adopt/ADOPT.md` | open | — | n/m | n/m | n/m | 2.3 | 56 | 0 | n/m | n/m | 309 |

### The specification's own size

| indicator | today | target |
|---|---|---|
| bytes | not measured | no target |
| requirements | 0 | no target |
| acceptance criteria | 0 | no target |
| bytes per criterion | not measured | falls or holds, bound 185.8 |
| repeated pairs | 116 | falls or holds |
| lines per part file | not measured | 250, once the division lands |

## What each column means

Each indicator carries five things: what it counts, why the project measures it, what changes when it moves, the command that produces it, and the value it aims at.

A file is carried to `finished` by two checks, and the table gives each check a count column and an ok column beside it. The first check is a script: it counts writing defects and reaches zero or it does not. The second check is live readers: two fresh readers read the file and their two lists are compared. The first check costs one command, the second costs two workers and a repair pass per round, which is why the table shows them apart.

**state** — a file reads `finished` when both checks read ok. Every other file reads `unfinished`. This is the campaign's only finish line, and the queue advances when a file reaches it.

**findings** — how many writing defects a script counted: prose sentences longer than 25 words, plus the findings of the style check, plus the findings of the register check. The 25 was the human-prose cap of rule r08 in `guardrails/language-rules.json`. Retired 2026-08-21 with `scripts/rule-census.py`: this column now reads "not measured" for every file.

**longest sentence** — the words in the file's longest prose sentence. One long sentence marks the paragraph a reader will reread, so it names where to start. Same command. Target: 25 words. The rule allows a numbered acceptance criterion 35 words, and the counter makes no such exception. So part of PRODUCT_SPEC.md's count is criteria the rule permits.

**style** — the findings of `scripts/spec-style-lint.py --tier full` alone, carried as its own column because a style finding is repaired differently from a long sentence. Target: zero.

**readings** — how many fresh readers have read this file. A reader holds no project access: only the file and one fixed list of questions, at `docs/briefs/reader-prompt.md`. Each reading writes a dated record under `docs/language-reads/`. Target: the count rises until two readers of one round agree on nothing.

**both stopped** — how many places both readers of the latest round stopped at. A single reader's list never repeats, so one reader measures that reader's path and two readers agreeing measures the text. While this stands above zero the file is repaired and read again. Counted by hand from the two reading records and stored per round in `guardrails/progress-baseline.json`. Target: zero.

**script ok** — the findings column at zero. Until 2026-08-21 the same number was also a push check, gate aa (`guardrails/check-doc-findings-bound.py`), which refused the push when a file counted more findings than the record kept for it. Both retired.

**readers ok** — the both-stopped column at zero for two rounds in a row.

**bytes**, **lines** — the file's size. They say whether a file is growing, and whether one reader holds it in one pass. Target for a specification part file: 250 lines of requirement bodies, from `docs/plans/2026-07-29-specification-subdivision.md`.

**requirements**, **criteria** — the specification's numbered requirements and their acceptance criteria, counted the way `guardrails/check-size-ratchet.py` counts them. They are the inputs to the density column.

**bytes per criterion** — the bytes of the criterion lines divided by the number of criteria. It separates growth by addition from growth by wordiness. A delivery may lower it or leave it; raising it needs a written reason in `guardrails/spec-ratchet.json`. Target: it falls or holds.

**repeated pairs** — pairs of sentences whose wording overlaps enough for a pattern to catch them, from `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`. A pattern catches only wording that repeats: it reaches five of the thirty-nine requirement pairs a judged reading found on 2026-07-29, recorded in `docs/measure/2026-07-29-specification-size.md`. Target: it falls or holds.

## Indicators this table cannot yet fill

Each one names what it would decide, and what it needs to exist.

**Rounds and cost per file.** They price the campaign, and they decide whether the queue is reachable at all. The reading records hold the data; no script counts it.

**Requirements a fresh agent builds unaided.** This is the only number that says whether the readability work changed anything. It needs a recorded run naming the requirements handed over, the agent, and what it produced.

**Judged duplication.** The requirement pairs stating one fact twice, the requirement groups sharing one shape, and the glossary entries naming one thing twice were measured by hand once, on 2026-07-29. As standing runs they become a push check, and the specification stops growing by rule.

**The share of findings a machine catches.** Every class a machine catches is a class no reader spends attention on. It reads the census and the reading records together.

## The rule this page enforces

Every number stated to a person, in chat or in a document, carries what it counts, why it is measured, what changes when it moves, the command that produced it, and the value it aims at. A number stated bare is a defect of the same kind as an undefined term.
