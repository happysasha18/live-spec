# Measurements — one row per file, every indicator

Generated 2026-08-05 by `python3 scripts/measurements-table.py`. This table is the source of truth for where the work stands, and `docs/MEASUREMENTS.html` is the page to read it on.

| # | file | state | both stopped | readers ok | find | script ok | est h | cum h | reads | long | style | lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **The text that enters every turn** ||||||||||||
| 1 | `hooks/chat-law-hook.sh` | open | n/m | no | n/m | n/m | 2.3 | 2 | 1 | n/m | n/m | 19 |
| | **The text that enters every session at its start** ||||||||||||
| 2 | `~/.claude/CLAUDE.md` | open | — | n/m | n/m | n/m | 2.3 | 5 | 0 | n/m | n/m | n/m |
| 3 | `~/.claude/live-spec/profile.md` | open | — | n/m | n/m | n/m | 2.3 | 7 | 0 | n/m | n/m | n/m |
| | **The file every session reads first** ||||||||||||
| 4 | `NEXT_STEPS.md` | open | — | n/m | 0 | ok | 2.1 | 9 | 0 | 24 | 0 | 74 |
| | **The text-audit skill and the four documents it points at** ||||||||||||
| 5 | `skills/text-audit/SKILL.md` | open | 3 | no | 0 | ok | 0.0 | 9 | 16 | 25 | 0 | 482 |
| 6 | `docs/language-rules.md` | open | n/m | no | 38 | no | 2.1 | 11 | 2 | 89 | 8 | 1,121 |
| 7 | `docs/spec-style.md` | open | — | n/m | 65 | no | 2.2 | 13 | 0 | 64 | 33 | 152 |
| 8 | `docs/spec-format.md` | open | — | n/m | 16 | no | 2.1 | 15 | 0 | 98 | 1 | 77 |
| 9 | `docs/language-worked-example.md` | open | — | n/m | 8 | no | 2.1 | 18 | 0 | 41 | 2 | 636 |
| | **The three skills loaded in every task run by the method** ||||||||||||
| 10 | `skills/live-spec-base/SKILL.md` | open | — | n/m | 92 | no | 2.2 | 20 | 0 | 49 | 14 | 731 |
| 11 | `skills/build-pipeline/SKILL.md` | open | — | n/m | 256 | no | 2.5 | 22 | 0 | 198 | 120 | 663 |
| 12 | `skills/communicator/SKILL.md` | open | — | n/m | 175 | no | 2.4 | 25 | 0 | 97 | 91 | 500 |
| | **ROADMAP.md, read whenever a session picks up work** ||||||||||||
| 13 | `ROADMAP.md` | open | — | n/m | 215 | no | 2.4 | 27 | 0 | 242 | 207 | 208 |
| | **The remaining seven skills** ||||||||||||
| 14 | `skills/design-reviewer/SKILL.md` | open | — | n/m | 0 | ok | 2.1 | 29 | 0 | 25 | 0 | 427 |
| 15 | `skills/feedback-collector/SKILL.md` | open | — | n/m | 14 | no | 2.1 | 31 | 0 | 34 | 11 | 138 |
| 16 | `skills/feedback-intake/SKILL.md` | open | — | n/m | 22 | no | 2.1 | 33 | 0 | 49 | 10 | 99 |
| 17 | `skills/product-prover/SKILL.md` | open | — | n/m | 0 | ok | 2.1 | 36 | 0 | 25 | 0 | 1,055 |
| 18 | `skills/publish/SKILL.md` | open | — | n/m | 61 | no | 2.2 | 38 | 0 | 85 | 29 | 156 |
| 19 | `skills/spec-author/SKILL.md` | open | — | n/m | 113 | no | 2.3 | 40 | 0 | 99 | 0 | 740 |
| 20 | `skills/test-author/SKILL.md` | open | — | n/m | 53 | no | 2.2 | 42 | 0 | 91 | 18 | 224 |
| | **The specification family** ||||||||||||
| 21 | `PRODUCT_SPEC.md` | open | — | n/m | 1,830 | no | 5.1 | 47 | 0 | 80 | 0 | 7,862 |
| 22 | `ARCHITECTURE.md` | open | — | n/m | 0 | ok | 2.1 | 49 | 0 | 25 | 0 | 879 |
| 23 | `TEST_MATRIX.md` | open | — | n/m | 76 | no | 2.2 | 52 | 0 | 46 | 68 | 1,147 |
| | **The documents a stranger meets on arrival** ||||||||||||
| 24 | `README.md` | open | — | n/m | 13 | no | 2.1 | 54 | 0 | 88 | 0 | 122 |
| 25 | `OVERVIEW.md` | open | — | n/m | 8 | no | 2.1 | 56 | 0 | 67 | 0 | 113 |
| 26 | `adopt/ADOPT.md` | open | — | n/m | 46 | no | 2.2 | 58 | 0 | 93 | 0 | 301 |
| | **Every remaining live document, worst first** ||||||||||||
| 27 | `docs/prior-art-frameworks.md` | open | — | n/m | 112 | no | 2.3 | 60 | 0 | 42 | 105 | 317 |
| 28 | `docs/language-rule-coverage.md` | open | — | n/m | 101 | no | 2.3 | 62 | 0 | 81 | 22 | 1,335 |
| 29 | `docs/restyle-repoint-log.md` | open | — | n/m | 83 | no | 2.2 | 65 | 0 | 78 | 63 | 141 |
| 30 | `docs/prior-art-longtail.md` | open | — | n/m | 78 | no | 2.2 | 67 | 0 | 53 | 63 | 277 |
| 31 | `skills/build-pipeline/references/delegation-protocol.md` | open | — | n/m | 52 | no | 2.2 | 69 | 0 | 71 | 24 | 98 |
| 32 | `guardrails/README.md` | open | — | n/m | 49 | no | 2.2 | 71 | 0 | 68 | 19 | 235 |
| 33 | `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | open | — | n/m | 41 | no | 2.2 | 73 | 0 | 65 | 27 | 131 |
| 34 | `docs/lenses.md` | open | — | n/m | 39 | no | 2.1 | 76 | 0 | 49 | 2 | 291 |
| 35 | `docs/decisions/2026-07-07-morning-round3.md` | open | — | n/m | 38 | no | 2.1 | 78 | 0 | 64 | 32 | 63 |
| 36 | `hooks/conduct-law.md` | open | — | n/m | 38 | no | 2.1 | 80 | 0 | 72 | 27 | 45 |
| 37 | `docs/language-defects.md` | open | n/m | no | 37 | no | 2.1 | 82 | 9 | 78 | 4 | 472 |
| 38 | `docs/spec-compaction-protocol.md` | open | — | n/m | 36 | no | 2.1 | 84 | 0 | 60 | 25 | 104 |
| 39 | `docs/roadmap-format.md` | open | — | n/m | 33 | no | 2.1 | 86 | 0 | 60 | 0 | 76 |
| 40 | `docs/test-matrix-format.md` | open | — | n/m | 33 | no | 2.1 | 88 | 0 | 59 | 1 | 80 |
| 41 | `docs/prose-quality-gate-design.md` | open | — | n/m | 32 | no | 2.1 | 91 | 0 | 65 | 23 | 80 |
| 42 | `docs/decisions/2026-07-06-overnight-decisions.md` | open | — | n/m | 31 | no | 2.1 | 93 | 0 | 51 | 23 | 110 |
| 43 | `inbox/README.md` | open | — | n/m | 31 | no | 2.1 | 95 | 0 | 75 | 3 | 136 |
| 44 | `editions/product-prover/SKILL.md` | open | — | n/m | 24 | no | 2.1 | 97 | 0 | 44 | 2 | 771 |
| 45 | `skills/communicator/references/field-examples.md` | open | — | n/m | 21 | no | 2.1 | 99 | 0 | 51 | 4 | 110 |
| 46 | `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | open | — | n/m | 19 | no | 2.1 | 101 | 0 | 60 | 10 | 59 |
| 47 | `docs/wishes/2026-07-09-prover-unwritten-seams.md` | open | — | n/m | 18 | no | 2.1 | 103 | 0 | 59 | 9 | 45 |
| 48 | `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | open | — | n/m | 18 | no | 2.1 | 105 | 0 | 36 | 12 | 38 |
| 49 | `docs/worker-liveness.md` | open | — | n/m | 17 | no | 2.1 | 108 | 0 | 52 | 1 | 60 |
| 50 | `templates/agent.template.md` | open | — | n/m | 17 | no | 2.1 | 110 | 0 | 47 | 7 | 99 |
| 51 | `docs/architecture-format.md` | open | — | n/m | 16 | no | 2.1 | 112 | 0 | 49 | 0 | 131 |
| 52 | `docs/migration-sample/2026-07-20-backdescribe-sample.md` | open | — | n/m | 16 | no | 2.1 | 114 | 0 | 76 | 8 | 35 |
| 53 | `skills/design-reviewer/README.md` | open | — | n/m | 16 | no | 2.1 | 116 | 0 | 55 | 0 | 100 |
| 54 | `docs/test-method.md` | open | — | n/m | 15 | no | 2.1 | 118 | 0 | 52 | 0 | 129 |
| 55 | `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | open | — | n/m | 14 | no | 2.1 | 120 | 0 | 54 | 7 | 51 |
| 56 | `editions/product-prover/README.md` | open | — | n/m | 14 | no | 2.1 | 122 | 0 | 36 | 2 | 268 |
| 57 | `scripts/judge-rubric.md` | open | — | n/m | 13 | no | 2.1 | 124 | 0 | 25 | 13 | 22 |
| 58 | `skills/build-pipeline/references/work-kind-table.md` | open | — | n/m | 13 | no | 2.1 | 126 | 0 | 22 | 13 | 19 |
| 59 | `docs/architecture-method.md` | open | — | n/m | 12 | no | 2.1 | 129 | 0 | 47 | 0 | 142 |
| 60 | `editions/product-prover/reference/stress-lenses.md` | open | — | n/m | 11 | no | 2.1 | 131 | 0 | 42 | 1 | 384 |
| 61 | `skills/build-pipeline/references/guardrails-catalog.md` | open | — | n/m | 11 | no | 2.1 | 133 | 0 | 76 | 9 | 22 |
| 62 | `skills/communicator/references/page-lifecycle.md` | open | — | n/m | 11 | no | 2.1 | 135 | 0 | 50 | 0 | 117 |
| 63 | `skills/spec-author/README.md` | open | — | n/m | 11 | no | 2.1 | 137 | 0 | 52 | 0 | 63 |
| 64 | `docs/onboarding-and-settings.md` | open | — | n/m | 10 | no | 2.1 | 139 | 0 | 53 | 0 | 112 |
| 65 | `docs/plans/2026-07-28-top-level-readability.md` | open | — | n/m | 10 | no | 2.1 | 141 | 0 | 51 | 4 | 279 |
| 66 | `skills/build-pipeline/README.md` | open | — | n/m | 10 | no | 2.1 | 143 | 0 | 60 | 1 | 65 |
| 67 | `skills/communicator/references/writing-register.md` | open | — | n/m | 10 | no | 2.1 | 145 | 0 | 45 | 2 | 158 |
| 68 | `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | open | — | n/m | 9 | no | 2.1 | 147 | 0 | 35 | 4 | 32 |
| 69 | `docs/pipeline.md` | open | — | n/m | 8 | no | 2.1 | 150 | 0 | 44 | 0 | 141 |
| 70 | `docs/spec-format-by-project-type.md` | open | — | n/m | 8 | no | 2.1 | 152 | 0 | 41 | 6 | 89 |
| 71 | `skills/test-author/README.md` | open | — | n/m | 8 | no | 2.1 | 154 | 0 | 35 | 4 | 96 |
| 72 | `docs/pair-adoption.md` | open | — | n/m | 7 | no | 2.1 | 156 | 0 | 47 | 0 | 116 |
| 73 | `scripts/read-grant-ask.md` | open | — | n/m | 7 | no | 2.1 | 158 | 0 | 28 | 4 | 20 |
| 74 | `skills/build-pipeline/references/drafter-applier-example.md` | open | — | n/m | 7 | no | 2.1 | 160 | 0 | 67 | 4 | 16 |
| 75 | `docs/adoption.md` | open | — | n/m | 6 | no | 2.1 | 162 | 0 | 51 | 0 | 110 |
| 76 | `docs/push-law.md` | open | — | n/m | 6 | no | 2.1 | 164 | 0 | 53 | 1 | 82 |
| 77 | `editions/product-prover/examples/sample-spec.md` | open | — | n/m | 6 | no | 2.1 | 166 | 0 | 36 | 3 | 96 |
| 78 | `skills/feedback-intake/README.md` | open | — | n/m | 6 | no | 2.1 | 168 | 0 | 35 | 0 | 95 |
| 79 | `skills/publish/README.md` | open | — | n/m | 6 | no | 2.1 | 171 | 0 | 40 | 4 | 18 |
| 80 | `templates/DECISIONS.template.md` | open | — | n/m | 5 | no | 2.1 | 173 | 0 | 36 | 4 | 30 |
| 81 | `templates/JOURNAL.template.md` | open | — | n/m | 5 | no | 2.1 | 175 | 0 | 24 | 5 | 20 |
| 82 | `templates/NEXT_STEPS.template.md` | open | — | n/m | 5 | no | 2.1 | 177 | 0 | 27 | 4 | 24 |
| 83 | `templates/PROBLEMS.template.md` | open | — | n/m | 5 | no | 2.1 | 179 | 0 | 25 | 5 | 21 |
| 84 | `skills/build-pipeline/references/minor-bump-gate.md` | open | — | n/m | 4 | no | 2.1 | 181 | 0 | 65 | 0 | 20 |
| 85 | `skills/communicator/references/words.md` | open | — | n/m | 4 | no | 2.1 | 183 | 0 | 57 | 0 | 84 |
| 86 | `templates/KILL_LIST.template.md` | open | — | n/m | 4 | no | 2.1 | 185 | 0 | 16 | 4 | 12 |
| 87 | `templates/profile.template.md` | open | — | n/m | 4 | no | 2.1 | 187 | 0 | 72 | 2 | 30 |
| 88 | `SURFACES.md` | open | — | n/m | 3 | no | 2.1 | 189 | 0 | 26 | 2 | 15 |
| 89 | `docs/MEASUREMENTS.md` | open | — | n/m | 3 | no | 2.1 | 191 | 0 | 36 | 0 | 175 |
| 90 | `docs/norms/onboarding-card-2026-07-10.provenance.md` | open | — | n/m | 3 | no | 2.1 | 194 | 0 | 35 | 0 | 6 |
| 91 | `scripts/grant-ask.md` | open | — | n/m | 3 | no | 2.1 | 196 | 0 | 19 | 3 | 12 |
| 92 | `skills/build-pipeline/references/request-kind-table.md` | open | — | n/m | 3 | no | 2.1 | 198 | 0 | 28 | 2 | 19 |
| 93 | `skills/communicator/README.md` | open | — | n/m | 3 | no | 2.1 | 200 | 0 | 37 | 1 | 49 |
| 94 | `skills/feedback-collector/README.md` | open | — | n/m | 3 | no | 2.1 | 202 | 0 | 32 | 1 | 45 |
| 95 | `editions/product-prover/PROVENANCE.md` | open | — | n/m | 2 | no | 2.1 | 204 | 0 | 33 | 1 | 81 |
| 96 | `skills/build-pipeline/references/excuses-table.md` | open | — | n/m | 2 | no | 2.1 | 206 | 0 | 18 | 2 | 14 |
| 97 | `templates/skill-review.template.md` | open | — | n/m | 2 | no | 2.1 | 208 | 0 | 14 | 2 | 20 |
| 98 | `docs/plans/2026-07-29-specification-subdivision.md` | open | — | n/m | 1 | no | 2.1 | 210 | 0 | 44 | 0 | 778 |
| 99 | `docs/prior-art.md` | open | — | n/m | 1 | no | 2.1 | 212 | 0 | 17 | 1 | 20 |
| 100 | `skills/live-spec-base/README.md` | open | — | n/m | 1 | no | 2.1 | 214 | 0 | 28 | 0 | 4 |
| 101 | `templates/ARCHITECTURE.template.md` | open | — | n/m | 1 | no | 2.1 | 216 | 0 | 25 | 1 | 231 |
| 102 | `PRODUCT_SPEC.index.md` | open | — | n/m | 0 | ok | 2.1 | 219 | 0 | 0 | 0 | 391 |
| 103 | `docs/PROGRESS.md` | open | — | n/m | 0 | ok | 2.1 | 221 | 0 | 22 | 0 | 259 |
| 104 | `docs/plans/2026-07-28-two-goals-one-campaign.md` | open | n/m | no | 0 | ok | 2.1 | 223 | 1 | 25 | 0 | 153 |
| 105 | `skills/product-prover/README.md` | open | — | n/m | 0 | ok | 2.1 | 225 | 0 | 25 | 0 | 168 |
| 106 | `skills/text-audit/README.md` | open | — | n/m | 0 | ok | 2.1 | 227 | 0 | 25 | 0 | 101 |
| 107 | `skills/text-audit/references/human-prose-rules.md` | open | — | n/m | 0 | ok | 2.1 | 229 | 0 | 25 | 0 | 233 |
| 108 | `skills/text-audit/references/reader-prompt.md` | open | — | n/m | 0 | ok | 2.1 | 231 | 0 | 23 | 0 | 77 |
| 109 | `skills/text-audit/references/rewrite-meaning-check.md` | open | — | n/m | 0 | ok | 2.1 | 233 | 0 | 22 | 0 | 122 |
| 110 | `skills/text-audit/references/unprompted-reader-brief.md` | open | — | n/m | 0 | ok | 2.1 | 235 | 0 | 24 | 0 | 60 |
| 111 | `templates/PRODUCT_SPEC.template.md` | open | — | n/m | 0 | ok | 2.1 | 237 | 0 | 24 | 0 | 140 |
| 112 | `templates/ROADMAP.template.md` | open | — | n/m | 0 | ok | 2.1 | 239 | 0 | 24 | 0 | 128 |
| 113 | `templates/TEST_MATRIX.template.md` | open | — | n/m | 0 | ok | 2.1 | 241 | 0 | 25 | 0 | 95 |

### The specification's own size

| indicator | today | target |
|---|---|---|
| bytes | 667,689 | under 840,000 |
| requirements | 305 | no target |
| acceptance criteria | 1,631 | no target |
| bytes per criterion | 188.3 | falls or holds, bound 207.2 |
| repeated pairs | 119 | falls or holds |
| lines per part file | not measured | no target |

## What each column means

Each indicator carries five things: what it counts, why the project measures it, what changes when it moves, the command that produces it, and the value it aims at.

A file is carried to `finished` by two checks, and the table gives each check a count column and an ok column beside it. The first check is a script: it counts writing defects and reaches zero or it does not. The second check is live readers: two fresh readers read the file and their two lists are compared. The first check costs one command, the second costs two workers and a repair pass per round, which is why the table shows them apart.

**state** — a file reads `finished` when both checks read ok. Every other file reads `unfinished`. This is the campaign's only finish line, and the queue advances when a file reaches it.

**findings** — how many writing defects the script counts. Three counts added together: prose sentences longer than 25 words, plus the findings of the style check, plus the findings of the register check. The 25 is the human-prose cap of rule r08 in `guardrails/language-rules.json`, and the counter applies it to every file. `python3 scripts/rule-census.py`. Target: zero.

**longest sentence** — the words in the file's longest prose sentence. One long sentence marks the paragraph a reader will reread, so it names where to start. Same command. Target: 25 words. The rule allows a numbered acceptance criterion 35 words, and the counter makes no such exception. So part of PRODUCT_SPEC.md's count is criteria the rule permits.

**style** — the findings of `scripts/spec-style-lint.py --tier full` alone, carried as its own column because a style finding is repaired differently from a long sentence. Target: zero.

**readings** — how many fresh readers have read this file. A reader holds no project access: only the file and one fixed list of questions, at `skills/text-audit/references/reader-prompt.md`. Each reading writes a dated record under `docs/language-reads/`. Target: the count rises until two readers of one round agree on nothing.

**both stopped** — how many places both readers of the latest round stopped at. A single reader's list never repeats, so one reader measures that reader's path and two readers agreeing measures the text. While this stands above zero the file is repaired and read again. Counted by hand from the two reading records and stored per round in `guardrails/progress-baseline.json`. Target: zero.

**script ok** — the findings column at zero. The same number is a push check: `guardrails/check-doc-findings-bound.py` refuses the push when a file counts more findings than `guardrails/rule-census.json` records for it.

**readers ok** — the both-stopped column at zero for two rounds in a row.

**bytes**, **lines** — the file's size. They say whether a file is growing, and whether one reader holds it in one pass. No numeric target for a specification part file; set by the reading, per `docs/plans/2026-07-29-specification-subdivision.md`.

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
