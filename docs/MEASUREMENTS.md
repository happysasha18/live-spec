# Measurements — one row per file, every indicator

Generated 2026-07-29 by `python3 scripts/measurements-table.py`. This table is the source of truth for where the work stands, and `docs/MEASUREMENTS.html` is the page to read it on.

| # | file | state | agree | read | find | cnt | est h | cum h | reads | long | style | lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **The text that enters every turn** ||||||||||||
| 1 | `hooks/chat-law-hook.sh` | open | n/m | no | n/m | n/m | 2.3 | 2 | 1 | n/m | n/m | 14 |
| | **The text that enters every session at its start** ||||||||||||
| 2 | `~/.claude/CLAUDE.md` | open | — | n/m | n/m | n/m | 2.3 | 5 | 0 | n/m | n/m | n/m |
| 3 | `~/.claude/live-spec/profile.md` | open | — | n/m | n/m | n/m | 2.3 | 7 | 0 | n/m | n/m | n/m |
| | **The file every session reads first** ||||||||||||
| 4 | `NEXT_STEPS.md` | open | — | n/m | 0 | ok | 2.1 | 9 | 0 | 25 | 0 | 125 |
| | **The text-audit skill and the four documents it points at** ||||||||||||
| 5 | `skills/text-audit/SKILL.md` | open | 3 | no | 0 | ok | 0.0 | 9 | 14 | 25 | 0 | 352 |
| 6 | `docs/language-rules.md` | open | n/m | no | 38 | no | 2.1 | 11 | 2 | 89 | 8 | 1,079 |
| 7 | `docs/spec-style.md` | open | — | n/m | 65 | no | 2.2 | 13 | 0 | 64 | 33 | 152 |
| 8 | `docs/spec-format.md` | open | — | n/m | 16 | no | 2.1 | 15 | 0 | 98 | 1 | 77 |
| 9 | `docs/language-worked-example.md` | open | — | n/m | 8 | no | 2.1 | 18 | 0 | 41 | 2 | 629 |
| | **The three skills loaded in every task run by the method** ||||||||||||
| 10 | `skills/live-spec-base/SKILL.md` | open | — | n/m | 229 | no | 2.5 | 20 | 0 | 97 | 88 | 575 |
| 11 | `skills/build-pipeline/SKILL.md` | open | — | n/m | 261 | no | 2.5 | 23 | 0 | 198 | 123 | 579 |
| 12 | `skills/communicator/SKILL.md` | open | — | n/m | 181 | no | 2.4 | 25 | 0 | 105 | 95 | 500 |
| | **ROADMAP.md, read whenever a session picks up work** ||||||||||||
| 13 | `ROADMAP.md` | open | — | n/m | 215 | no | 2.4 | 27 | 0 | 242 | 207 | 193 |
| | **The remaining seven skills** ||||||||||||
| 14 | `skills/design-reviewer/SKILL.md` | open | — | n/m | 77 | no | 2.2 | 30 | 0 | 92 | 7 | 125 |
| 15 | `skills/feedback-collector/SKILL.md` | open | — | n/m | 21 | no | 2.1 | 32 | 0 | 41 | 17 | 138 |
| 16 | `skills/feedback-intake/SKILL.md` | open | — | n/m | 25 | no | 2.1 | 34 | 0 | 48 | 11 | 99 |
| 17 | `skills/product-prover/SKILL.md` | open | — | n/m | 0 | ok | 2.1 | 36 | 0 | 25 | 0 | 948 |
| 18 | `skills/publish/SKILL.md` | open | — | n/m | 66 | no | 2.2 | 38 | 0 | 85 | 33 | 156 |
| 19 | `skills/spec-author/SKILL.md` | open | — | n/m | 117 | no | 2.3 | 40 | 0 | 121 | 0 | 661 |
| 20 | `skills/test-author/SKILL.md` | open | — | n/m | 57 | no | 2.2 | 43 | 0 | 91 | 19 | 222 |
| | **The specification family** ||||||||||||
| 21 | `PRODUCT_SPEC.md` | open | — | n/m | 1,831 | no | 5.1 | 48 | 0 | 80 | 0 | 7,778 |
| 22 | `ARCHITECTURE.md` | open | — | n/m | 88 | no | 2.2 | 50 | 0 | 916 | 0 | 514 |
| 23 | `TEST_MATRIX.md` | open | — | n/m | 76 | no | 2.2 | 52 | 0 | 46 | 68 | 1,139 |
| | **The documents a stranger meets on arrival** ||||||||||||
| 24 | `README.md` | open | — | n/m | 16 | no | 2.1 | 54 | 0 | 88 | 0 | 105 |
| 25 | `OVERVIEW.md` | open | — | n/m | 8 | no | 2.1 | 56 | 0 | 67 | 0 | 102 |
| 26 | `adopt/ADOPT.md` | open | — | n/m | 46 | no | 2.2 | 59 | 0 | 93 | 0 | 301 |
| | **Every remaining live document, worst first** ||||||||||||
| 27 | `docs/prior-art-frameworks.md` | open | — | n/m | 112 | no | 2.3 | 61 | 0 | 42 | 105 | 317 |
| 28 | `docs/language-rule-coverage.md` | open | — | n/m | 105 | no | 2.3 | 63 | 0 | 81 | 22 | 1,150 |
| 29 | `docs/restyle-repoint-log.md` | open | — | n/m | 83 | no | 2.2 | 65 | 0 | 78 | 63 | 141 |
| 30 | `docs/prior-art-longtail.md` | open | — | n/m | 78 | no | 2.2 | 67 | 0 | 53 | 63 | 277 |
| 31 | `skills/build-pipeline/references/delegation-protocol.md` | open | — | n/m | 52 | no | 2.2 | 70 | 0 | 71 | 24 | 98 |
| 32 | `guardrails/README.md` | open | — | n/m | 49 | no | 2.2 | 72 | 0 | 68 | 19 | 235 |
| 33 | `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | open | — | n/m | 41 | no | 2.2 | 74 | 0 | 65 | 27 | 131 |
| 34 | `docs/lenses.md` | open | — | n/m | 39 | no | 2.1 | 76 | 0 | 49 | 2 | 291 |
| 35 | `templates/ARCHITECTURE.template.md` | open | — | n/m | 39 | no | 2.1 | 78 | 0 | 51 | 16 | 168 |
| 36 | `docs/decisions/2026-07-07-morning-round3.md` | open | — | n/m | 38 | no | 2.1 | 80 | 0 | 64 | 32 | 63 |
| 37 | `docs/language-defects.md` | open | n/m | no | 38 | no | 2.1 | 83 | 9 | 78 | 4 | 413 |
| 38 | `hooks/conduct-law.md` | open | — | n/m | 38 | no | 2.1 | 85 | 0 | 72 | 27 | 45 |
| 39 | `docs/spec-compaction-protocol.md` | open | — | n/m | 36 | no | 2.1 | 87 | 0 | 60 | 25 | 104 |
| 40 | `docs/roadmap-format.md` | open | — | n/m | 33 | no | 2.1 | 89 | 0 | 60 | 0 | 76 |
| 41 | `docs/test-matrix-format.md` | open | — | n/m | 33 | no | 2.1 | 91 | 0 | 59 | 1 | 80 |
| 42 | `docs/prose-quality-gate-design.md` | open | — | n/m | 32 | no | 2.1 | 93 | 0 | 65 | 23 | 80 |
| 43 | `docs/decisions/2026-07-06-overnight-decisions.md` | open | — | n/m | 31 | no | 2.1 | 95 | 0 | 51 | 23 | 110 |
| 44 | `inbox/README.md` | open | — | n/m | 31 | no | 2.1 | 98 | 0 | 75 | 3 | 136 |
| 45 | `skills/communicator/references/field-examples.md` | open | — | n/m | 21 | no | 2.1 | 100 | 0 | 51 | 4 | 106 |
| 46 | `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | open | — | n/m | 19 | no | 2.1 | 102 | 0 | 60 | 10 | 59 |
| 47 | `docs/wishes/2026-07-09-prover-unwritten-seams.md` | open | — | n/m | 18 | no | 2.1 | 104 | 0 | 59 | 9 | 45 |
| 48 | `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | open | — | n/m | 18 | no | 2.1 | 106 | 0 | 36 | 12 | 38 |
| 49 | `docs/worker-liveness.md` | open | — | n/m | 17 | no | 2.1 | 108 | 0 | 52 | 1 | 60 |
| 50 | `templates/agent.template.md` | open | — | n/m | 17 | no | 2.1 | 110 | 0 | 47 | 7 | 99 |
| 51 | `docs/architecture-format.md` | open | — | n/m | 16 | no | 2.1 | 112 | 0 | 49 | 0 | 131 |
| 52 | `docs/migration-sample/2026-07-20-backdescribe-sample.md` | open | — | n/m | 16 | no | 2.1 | 114 | 0 | 76 | 8 | 35 |
| 53 | `skills/design-reviewer/README.md` | open | — | n/m | 16 | no | 2.1 | 117 | 0 | 55 | 0 | 100 |
| 54 | `docs/test-method.md` | open | — | n/m | 15 | no | 2.1 | 119 | 0 | 52 | 0 | 129 |
| 55 | `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | open | — | n/m | 14 | no | 2.1 | 121 | 0 | 54 | 7 | 51 |
| 56 | `scripts/judge-rubric.md` | open | — | n/m | 13 | no | 2.1 | 123 | 0 | 25 | 13 | 22 |
| 57 | `skills/build-pipeline/references/work-kind-table.md` | open | — | n/m | 13 | no | 2.1 | 125 | 0 | 22 | 13 | 19 |
| 58 | `docs/architecture-method.md` | open | — | n/m | 12 | no | 2.1 | 127 | 0 | 47 | 0 | 142 |
| 59 | `templates/ROADMAP.template.md` | open | — | n/m | 12 | no | 2.1 | 129 | 0 | 74 | 0 | 96 |
| 60 | `skills/build-pipeline/references/guardrails-catalog.md` | open | — | n/m | 11 | no | 2.1 | 131 | 0 | 76 | 9 | 22 |
| 61 | `skills/communicator/references/page-lifecycle.md` | open | — | n/m | 11 | no | 2.1 | 133 | 0 | 50 | 0 | 114 |
| 62 | `skills/spec-author/README.md` | open | — | n/m | 11 | no | 2.1 | 135 | 0 | 52 | 0 | 63 |
| 63 | `docs/onboarding-and-settings.md` | open | — | n/m | 10 | no | 2.1 | 138 | 0 | 53 | 0 | 112 |
| 64 | `docs/plans/2026-07-28-top-level-readability.md` | open | — | n/m | 10 | no | 2.1 | 140 | 0 | 51 | 4 | 274 |
| 65 | `skills/build-pipeline/README.md` | open | — | n/m | 10 | no | 2.1 | 142 | 0 | 60 | 1 | 65 |
| 66 | `skills/communicator/references/writing-register.md` | open | — | n/m | 10 | no | 2.1 | 144 | 0 | 45 | 2 | 156 |
| 67 | `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | open | — | n/m | 9 | no | 2.1 | 146 | 0 | 35 | 4 | 32 |
| 68 | `docs/pipeline.md` | open | — | n/m | 8 | no | 2.1 | 148 | 0 | 44 | 0 | 141 |
| 69 | `docs/spec-format-by-project-type.md` | open | — | n/m | 8 | no | 2.1 | 150 | 0 | 41 | 6 | 89 |
| 70 | `skills/test-author/README.md` | open | — | n/m | 8 | no | 2.1 | 152 | 0 | 35 | 4 | 96 |
| 71 | `docs/pair-adoption.md` | open | — | n/m | 7 | no | 2.1 | 154 | 0 | 47 | 0 | 116 |
| 72 | `scripts/read-grant-ask.md` | open | — | n/m | 7 | no | 2.1 | 156 | 0 | 28 | 4 | 20 |
| 73 | `skills/build-pipeline/references/drafter-applier-example.md` | open | — | n/m | 7 | no | 2.1 | 159 | 0 | 67 | 4 | 16 |
| 74 | `templates/PRODUCT_SPEC.template.md` | open | — | n/m | 7 | no | 2.1 | 161 | 0 | 32 | 1 | 84 |
| 75 | `templates/TEST_MATRIX.template.md` | open | — | n/m | 7 | no | 2.1 | 163 | 0 | 95 | 2 | 83 |
| 76 | `docs/adoption.md` | open | — | n/m | 6 | no | 2.1 | 165 | 0 | 51 | 0 | 109 |
| 77 | `docs/push-law.md` | open | — | n/m | 6 | no | 2.1 | 167 | 0 | 53 | 1 | 82 |
| 78 | `skills/feedback-intake/README.md` | open | — | n/m | 6 | no | 2.1 | 169 | 0 | 35 | 0 | 95 |
| 79 | `skills/publish/README.md` | open | — | n/m | 6 | no | 2.1 | 171 | 0 | 40 | 4 | 18 |
| 80 | `templates/DECISIONS.template.md` | open | — | n/m | 5 | no | 2.1 | 173 | 0 | 36 | 4 | 30 |
| 81 | `templates/JOURNAL.template.md` | open | — | n/m | 5 | no | 2.1 | 175 | 0 | 24 | 5 | 20 |
| 82 | `templates/NEXT_STEPS.template.md` | open | — | n/m | 5 | no | 2.1 | 177 | 0 | 27 | 4 | 24 |
| 83 | `templates/PROBLEMS.template.md` | open | — | n/m | 5 | no | 2.1 | 179 | 0 | 25 | 5 | 21 |
| 84 | `skills/build-pipeline/references/minor-bump-gate.md` | open | — | n/m | 4 | no | 2.1 | 182 | 0 | 65 | 0 | 20 |
| 85 | `templates/KILL_LIST.template.md` | open | — | n/m | 4 | no | 2.1 | 184 | 0 | 16 | 4 | 12 |
| 86 | `templates/profile.template.md` | open | — | n/m | 4 | no | 2.1 | 186 | 0 | 72 | 2 | 30 |
| 87 | `SURFACES.md` | open | — | n/m | 3 | no | 2.1 | 188 | 0 | 26 | 2 | 15 |
| 88 | `docs/MEASUREMENTS.md` | open | — | n/m | 3 | no | 2.1 | 190 | 0 | 36 | 0 | 192 |
| 89 | `docs/norms/onboarding-card-2026-07-10.provenance.md` | open | — | n/m | 3 | no | 2.1 | 192 | 0 | 35 | 0 | 6 |
| 90 | `scripts/grant-ask.md` | open | — | n/m | 3 | no | 2.1 | 194 | 0 | 19 | 3 | 12 |
| 91 | `skills/build-pipeline/references/request-kind-table.md` | open | — | n/m | 3 | no | 2.1 | 196 | 0 | 28 | 2 | 19 |
| 92 | `skills/communicator/README.md` | open | — | n/m | 3 | no | 2.1 | 198 | 0 | 37 | 1 | 44 |
| 93 | `skills/feedback-collector/README.md` | open | — | n/m | 3 | no | 2.1 | 200 | 0 | 32 | 1 | 45 |
| 94 | `skills/build-pipeline/references/excuses-table.md` | open | — | n/m | 2 | no | 2.1 | 202 | 0 | 18 | 2 | 14 |
| 95 | `templates/skill-review.template.md` | open | — | n/m | 2 | no | 2.1 | 205 | 0 | 14 | 2 | 20 |
| 96 | `docs/plans/2026-07-29-specification-subdivision.md` | open | — | n/m | 1 | no | 2.1 | 207 | 0 | 44 | 0 | 778 |
| 97 | `docs/prior-art.md` | open | — | n/m | 1 | no | 2.1 | 209 | 0 | 17 | 1 | 20 |
| 98 | `guardrails/release-note-fixtures/note-neither.md` | open | — | n/m | 1 | no | 2.1 | 211 | 0 | 28 | 0 | 9 |
| 99 | `guardrails/release-note-fixtures/note-offers.md` | open | — | n/m | 1 | no | 2.1 | 213 | 0 | 30 | 0 | 11 |
| 100 | `skills/live-spec-base/README.md` | open | — | n/m | 1 | no | 2.1 | 215 | 0 | 28 | 0 | 4 |
| 101 | `PRODUCT_SPEC.index.md` | open | — | n/m | 0 | ok | 2.1 | 217 | 0 | 0 | 0 | 389 |
| 102 | `docs/PROGRESS.md` | open | — | n/m | 0 | ok | 2.1 | 219 | 0 | 22 | 0 | 274 |
| 103 | `docs/plans/2026-07-28-two-goals-one-campaign.md` | open | n/m | no | 0 | ok | 2.1 | 221 | 1 | 25 | 0 | 153 |
| 104 | `guardrails/far-tier-fixtures/report-names-far-in-runnable.md` | open | — | n/m | 0 | ok | 2.1 | 223 | 0 | 14 | 0 | 14 |
| 105 | `guardrails/far-tier-fixtures/report-runnable-no-standdown.md` | open | — | n/m | 0 | ok | 2.1 | 225 | 0 | 9 | 0 | 10 |
| 106 | `guardrails/far-tier-fixtures/report-stands-far-down.md` | open | — | n/m | 0 | ok | 2.1 | 227 | 0 | 14 | 0 | 13 |
| 107 | `guardrails/far-tier-fixtures/vocab-clean.md` | open | — | n/m | 0 | ok | 2.1 | 230 | 0 | 15 | 0 | 5 |
| 108 | `guardrails/far-tier-fixtures/vocab-deferred-without-trigger.md` | open | — | n/m | 0 | ok | 2.1 | 232 | 0 | 10 | 0 | 4 |
| 109 | `guardrails/far-tier-fixtures/vocab-far-with-trigger.md` | open | — | n/m | 0 | ok | 2.1 | 234 | 0 | 15 | 0 | 5 |
| 110 | `guardrails/far-tier-fixtures/window-first-offer-after-window.md` | open | — | n/m | 0 | ok | 2.1 | 236 | 0 | 12 | 0 | 8 |
| 111 | `guardrails/far-tier-fixtures/window-second-offer-in-window.md` | open | — | n/m | 0 | ok | 2.1 | 238 | 0 | 12 | 0 | 8 |
| 112 | `guardrails/measured-number-fixtures/bare-number.md` | open | — | n/m | 0 | ok | 2.1 | 240 | 0 | 8 | 0 | 2 |
| 113 | `guardrails/measured-number-fixtures/measured-number.md` | open | — | n/m | 0 | ok | 2.1 | 242 | 0 | 21 | 0 | 5 |
| 114 | `guardrails/release-note-fixtures/note-no-offer.md` | open | — | n/m | 0 | ok | 2.1 | 244 | 0 | 21 | 0 | 8 |
| 115 | `skills/product-prover/README.md` | open | — | n/m | 0 | ok | 2.1 | 246 | 0 | 25 | 0 | 168 |
| 116 | `skills/text-audit/README.md` | open | — | n/m | 0 | ok | 2.1 | 248 | 0 | 25 | 0 | 101 |
| 117 | `skills/text-audit/references/human-prose-rules.md` | open | — | n/m | 0 | ok | 2.1 | 250 | 0 | 25 | 0 | 230 |
| 118 | `skills/text-audit/references/reader-prompt.md` | open | — | n/m | 0 | ok | 2.1 | 252 | 0 | 23 | 0 | 52 |

### The specification's own size

| indicator | today | target |
|---|---|---|
| bytes | 661,342 | under 840,000 |
| requirements | 303 | no target |
| acceptance criteria | 1,609 | no target |
| bytes per criterion | 189.3 | falls or holds, bound 207.2 |
| repeated pairs | 119 | falls or holds |
| lines per part file | not measured | 250, once the division lands |

## What each column means

Each indicator carries five things: what it counts, why the project measures it, what changes when it moves, the command that produces it, and the value it aims at.

**state** — a file reads `finished` when it is measured clean and read clean. Every other file reads `unfinished`. This is the campaign's only finish line, and the queue advances when a file reaches it.

**findings** — sentences past the word cap of the file's surface, plus the findings of the style check and the register check. It separates the cheap defects a script settles from the ones needing a reader. A file above its recorded count refuses the push. `python3 scripts/rule-census.py`. Target: zero.

**longest sentence** — the words in the file's longest prose sentence. One long sentence marks the paragraph a reader will reread, so it names where to start. Same command. Target: 25 words for human prose, 35 for a numbered acceptance criterion.

**style** — the findings of `scripts/spec-style-lint.py --tier full` alone, carried as its own column because a style finding is repaired differently from a long sentence. Target: zero.

**readings** — how many fresh readers have read this file. A reader holds no project access: only the file and one fixed list of questions, at `skills/text-audit/references/reader-prompt.md`. Each reading writes a dated record under `docs/language-reads/`. Target: the count rises until two readers of one round agree on nothing.

**agreed stops** — places where both readers of the latest round stopped. A single reader's list never repeats, so one reader measures that reader's path and two readers agreeing measures the text. While this stands above zero the file is repaired again. Recorded per round in `guardrails/progress-baseline.json`. Target: zero.

**measured clean** — the findings column at zero.

**read clean** — the agreed-stop column at zero for two rounds in a row.

**bytes**, **lines** — the file's size. They say whether a file is growing, and whether one reader holds it in one pass. Target for a specification part file: 250 lines of requirement bodies, from `docs/plans/2026-07-29-specification-subdivision.md`.

**requirements**, **criteria** — the specification's numbered requirements and their acceptance criteria, counted the way `guardrails/check-size-ratchet.py` counts them. They are the inputs to the density column.

**bytes per criterion** — the bytes of the criterion lines divided by the number of criteria. It separates growth by addition from growth by wordiness. A delivery may lower it or leave it; raising it needs a written reason in `guardrails/spec-ratchet.json`. Target: it falls or holds.

**repeated pairs** — pairs of sentences whose wording overlaps enough for a pattern to catch them, from `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`. This is the cheap layer: it reaches five of the thirty-nine requirement pairs the judged measure found on 2026-07-29, recorded in `docs/measure/2026-07-29-specification-size.md`. Target: it falls or holds.

## Indicators this table cannot yet fill

Each one names what it would decide, and what it needs to exist.

**Cheap reader against strong reader.** Every reading so far ran on the expensive tier, with no evidence the expense buys anything. The campaign plan requires this measurement before the tier is chosen. It needs one cheap worker reading the same text as a strong worker, and the two reports compared place by place.

**Rounds and cost per file.** They price the campaign, and they decide whether the queue is reachable at all. The reading records hold the data; no script counts it.

**Requirements a fresh agent builds unaided.** This is the only number that says whether the readability work changed anything. It needs a recorded run naming the requirements handed over, the agent, and what it produced.

**Judged duplication.** The requirement pairs stating one fact twice, the requirement groups sharing one shape, and the glossary entries naming one thing twice were measured by hand once, on 2026-07-29. As standing runs they become a push check, and the specification stops growing by rule.

**The share of findings a machine catches.** Every class a machine catches is a class no reader spends attention on. It reads the census and the reading records together.

## The rule this page enforces

Every number stated to a person, in chat or in a document, carries what it counts, why it is measured, what changes when it moves, the command that produced it, and the value it aims at. A number stated bare is a defect of the same kind as an undefined term.
