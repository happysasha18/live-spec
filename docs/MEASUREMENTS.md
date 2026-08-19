# Measurements — one row per file, every indicator

Generated 2026-08-19 by `python3 scripts/measurements-table.py`. This table is the source of truth for where the work stands. Add `--html` to also build `docs/MEASUREMENTS.html`, the page to read it on — a transient render, swept once its reading closes (SPEC INV-286).

| # | file | state | both stopped | readers ok | find | script ok | est h | cum h | reads | long | style | lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **The text that enters every turn** ||||||||||||
| 1 | `hooks/chat-law-hook.sh` | open | n/m | no | n/m | n/m | 2.3 | 2 | 1 | n/m | n/m | 9 |
| | **The text that enters every session at its start** ||||||||||||
| 2 | `~/.claude/CLAUDE.md` | open | — | n/m | n/m | n/m | 2.3 | 5 | 0 | n/m | n/m | n/m |
| 3 | `~/.claude/live-spec/profile.md` | open | — | n/m | n/m | n/m | 2.3 | 7 | 0 | n/m | n/m | n/m |
| | **The file every session reads first** ||||||||||||
| 4 | `NEXT_STEPS.md` | open | — | n/m | 0 | ok | 2.1 | 9 | 0 | 25 | 0 | 180 |
| | **The four documents behind the language rules (text-audit itself moved to its own repository, 2026-08-18 — skills/text-audit-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)** ||||||||||||
| 5 | `docs/language-rules.md` | open | n/m | no | 33 | no | 2.1 | 11 | 2 | 89 | 8 | 1,078 |
| 6 | `docs/spec-style.md` | open | — | n/m | 65 | no | 2.2 | 13 | 0 | 64 | 33 | 152 |
| 7 | `docs/spec-format.md` | open | — | n/m | 13 | no | 2.1 | 15 | 0 | 98 | 1 | 76 |
| 8 | `docs/language-worked-example.md` | open | — | n/m | 8 | no | 2.1 | 18 | 0 | 41 | 2 | 636 |
| | **The three skills loaded in every task run by the method** ||||||||||||
| 9 | `skills/live-spec-base/SKILL.md` | open | — | n/m | 20 | no | 2.1 | 20 | 0 | 47 | 14 | 620 |
| 10 | `skills/build-pipeline/SKILL.md` | open | — | n/m | 37 | no | 2.1 | 22 | 0 | 47 | 33 | 727 |
| 11 | `skills/communicator/SKILL.md` | open | — | n/m | 17 | no | 2.1 | 24 | 0 | 52 | 15 | 497 |
| | **ROADMAP.md, read whenever a session picks up work** ||||||||||||
| 12 | `ROADMAP.md` | open | — | n/m | 215 | no | 2.4 | 26 | 0 | 242 | 207 | 270 |
| | **The remaining six skills (product-prover moved to its own repository, 2026-08-13 — skills/product-prover-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)** ||||||||||||
| 13 | `skills/design-reviewer/SKILL.md` | open | — | n/m | 0 | ok | 2.1 | 28 | 0 | 25 | 0 | 431 |
| 14 | `skills/feedback-collector/SKILL.md` | open | — | n/m | 14 | no | 2.1 | 31 | 0 | 34 | 11 | 143 |
| 15 | `skills/feedback-intake/SKILL.md` | open | — | n/m | 23 | no | 2.1 | 33 | 0 | 52 | 10 | 104 |
| 16 | `skills/publish/SKILL.md` | open | — | n/m | 61 | no | 2.2 | 35 | 0 | 85 | 29 | 161 |
| 17 | `skills/spec-author/SKILL.md` | open | — | n/m | 46 | no | 2.2 | 37 | 0 | 98 | 0 | 271 |
| 18 | `skills/test-author/SKILL.md` | open | — | n/m | 54 | no | 2.2 | 39 | 0 | 91 | 18 | 230 |
| | **The specification family** ||||||||||||
| 19 | `PRODUCT_SPEC.md` | open | — | n/m | 130 | no | 2.3 | 42 | 0 | 103 | 0 | 305 |
| 20 | `ARCHITECTURE.md` | open | — | n/m | 0 | ok | 2.1 | 44 | 0 | 25 | 0 | 917 |
| 21 | `TEST_MATRIX.md` | open | — | n/m | 76 | no | 2.2 | 46 | 0 | 46 | 68 | 1,202 |
| | **The documents a stranger meets on arrival** ||||||||||||
| 22 | `README.md` | open | — | n/m | 4 | no | 2.1 | 48 | 0 | 122 | 0 | 227 |
| 23 | `OVERVIEW.md` | open | — | n/m | 8 | no | 2.1 | 50 | 0 | 98 | 0 | 123 |
| 24 | `adopt/ADOPT.md` | open | — | n/m | 46 | no | 2.2 | 52 | 0 | 93 | 0 | 309 |
| | **Every remaining live document, worst first** ||||||||||||
| 25 | `spec/design-spec-review.md` | open | — | n/m | 233 | no | 2.5 | 55 | 0 | 69 | 0 | 928 |
| 26 | `spec/guardrails-freshness.md` | open | — | n/m | 209 | no | 2.4 | 57 | 0 | 78 | 0 | 997 |
| 27 | `spec/queue-intake-priority.md` | open | — | n/m | 185 | no | 2.4 | 59 | 0 | 60 | 0 | 760 |
| 28 | `spec/doc-order-generated.md` | open | — | n/m | 178 | no | 2.4 | 62 | 0 | 53 | 0 | 775 |
| 29 | `spec/roles-and-agents.md` | open | — | n/m | 145 | no | 2.3 | 64 | 0 | 76 | 0 | 565 |
| 30 | `docs/prior-art-frameworks.md` | open | — | n/m | 112 | no | 2.3 | 66 | 0 | 42 | 105 | 317 |
| 31 | `spec/live-status-reporting.md` | open | — | n/m | 105 | no | 2.3 | 69 | 0 | 63 | 0 | 499 |
| 32 | `docs/language-rule-coverage.md` | open | — | n/m | 98 | no | 2.2 | 71 | 0 | 64 | 22 | 1,299 |
| 33 | `spec/push-gate-milestone-audit.md` | open | — | n/m | 84 | no | 2.2 | 73 | 0 | 52 | 0 | 443 |
| 34 | `docs/restyle-repoint-log.md` | open | — | n/m | 83 | no | 2.2 | 75 | 0 | 78 | 63 | 141 |
| 35 | `spec/parallel-lanes.md` | open | — | n/m | 82 | no | 2.2 | 78 | 0 | 69 | 0 | 339 |
| 36 | `spec/project-setup-tuning.md` | open | — | n/m | 82 | no | 2.2 | 80 | 0 | 56 | 0 | 443 |
| 37 | `docs/prior-art-longtail.md` | open | — | n/m | 78 | no | 2.2 | 82 | 0 | 53 | 63 | 277 |
| 38 | `spec/test-honesty.md` | open | — | n/m | 74 | no | 2.2 | 84 | 0 | 59 | 0 | 251 |
| 39 | `MIGRATION.md` | open | — | n/m | 62 | no | 2.2 | 86 | 0 | 65 | 0 | 372 |
| 40 | `docs/plans/2026-08-07-recovery-plan.md` | open | — | n/m | 61 | no | 2.2 | 89 | 0 | 99 | 6 | 348 |
| 41 | `skills/build-pipeline/references/delegation-protocol.md` | open | — | n/m | 53 | no | 2.2 | 91 | 0 | 71 | 24 | 111 |
| 42 | `spec/owner-questions-drafts.md` | open | — | n/m | 49 | no | 2.2 | 93 | 0 | 57 | 0 | 216 |
| 43 | `guardrails/README.md` | open | — | n/m | 48 | no | 2.2 | 95 | 0 | 68 | 19 | 351 |
| 44 | `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | open | — | n/m | 41 | no | 2.2 | 97 | 0 | 65 | 27 | 131 |
| 45 | `spec/customer-feedback.md` | open | — | n/m | 40 | no | 2.1 | 99 | 0 | 62 | 0 | 168 |
| 46 | `docs/lenses.md` | open | — | n/m | 39 | no | 2.1 | 102 | 0 | 49 | 2 | 293 |
| 47 | `docs/decisions/2026-07-07-morning-round3.md` | open | — | n/m | 38 | no | 2.1 | 104 | 0 | 64 | 32 | 63 |
| 48 | `hooks/conduct-law.md` | open | — | n/m | 38 | no | 2.1 | 106 | 0 | 72 | 27 | 45 |
| 49 | `docs/language-defects.md` | open | n/m | no | 37 | no | 2.1 | 108 | 9 | 78 | 4 | 472 |
| 50 | `docs/spec-compaction-protocol.md` | open | — | n/m | 36 | no | 2.1 | 110 | 0 | 60 | 25 | 104 |
| 51 | `spec/work-board.md` | open | — | n/m | 36 | no | 2.1 | 112 | 0 | 46 | 0 | 168 |
| 52 | `docs/roadmap-format.md` | open | — | n/m | 33 | no | 2.1 | 114 | 0 | 60 | 0 | 77 |
| 53 | `docs/test-matrix-format.md` | open | — | n/m | 33 | no | 2.1 | 117 | 0 | 59 | 1 | 80 |
| 54 | `docs/prose-quality-gate-design.md` | open | — | n/m | 32 | no | 2.1 | 119 | 0 | 65 | 23 | 80 |
| 55 | `spec/internal-failure-log.md` | open | — | n/m | 32 | no | 2.1 | 121 | 0 | 66 | 0 | 146 |
| 56 | `spec/public-text-rules.md` | open | — | n/m | 32 | no | 2.1 | 123 | 0 | 66 | 0 | 137 |
| 57 | `docs/decisions/2026-07-06-overnight-decisions.md` | open | — | n/m | 31 | no | 2.1 | 125 | 0 | 51 | 23 | 110 |
| 58 | `inbox/README.md` | open | — | n/m | 31 | no | 2.1 | 127 | 0 | 75 | 3 | 136 |
| 59 | `spec/settings-layers.md` | open | — | n/m | 26 | no | 2.1 | 129 | 0 | 45 | 0 | 131 |
| 60 | `skills/spec-author/references/facet-sweep.md` | open | — | n/m | 25 | no | 2.1 | 131 | 0 | 84 | 0 | 124 |
| 61 | `docs/audits/2026-08-07-number-census.md` | open | — | n/m | 22 | no | 2.1 | 134 | 0 | 135 | 17 | 236 |
| 62 | `skills/communicator/references/field-examples.md` | open | — | n/m | 21 | no | 2.1 | 136 | 0 | 51 | 4 | 110 |
| 63 | `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | open | — | n/m | 19 | no | 2.1 | 138 | 0 | 60 | 10 | 59 |
| 64 | `skills/build-pipeline/references/lanes-and-pen.md` | open | — | n/m | 19 | no | 2.1 | 140 | 0 | 74 | 4 | 56 |
| 65 | `docs/wishes/2026-07-09-prover-unwritten-seams.md` | open | — | n/m | 18 | no | 2.1 | 142 | 0 | 59 | 9 | 45 |
| 66 | `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | open | — | n/m | 18 | no | 2.1 | 144 | 0 | 36 | 12 | 38 |
| 67 | `docs/worker-liveness.md` | open | — | n/m | 17 | no | 2.1 | 146 | 0 | 52 | 1 | 60 |
| 68 | `skills/spec-author/references/how-it-reads.md` | open | — | n/m | 17 | no | 2.1 | 148 | 0 | 99 | 0 | 129 |
| 69 | `spec/bug-priority-queue.md` | open | — | n/m | 17 | no | 2.1 | 151 | 0 | 55 | 0 | 54 |
| 70 | `templates/agent.template.md` | open | — | n/m | 17 | no | 2.1 | 153 | 0 | 47 | 7 | 99 |
| 71 | `docs/architecture-format.md` | open | — | n/m | 16 | no | 2.1 | 155 | 0 | 49 | 0 | 131 |
| 72 | `docs/migration-sample/2026-07-20-backdescribe-sample.md` | open | — | n/m | 16 | no | 2.1 | 157 | 0 | 76 | 8 | 35 |
| 73 | `skills/design-reviewer/README.md` | open | — | n/m | 16 | no | 2.1 | 159 | 0 | 55 | 0 | 100 |
| 74 | `docs/test-method.md` | open | — | n/m | 15 | no | 2.1 | 161 | 0 | 52 | 0 | 129 |
| 75 | `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | open | — | n/m | 14 | no | 2.1 | 163 | 0 | 54 | 7 | 51 |
| 76 | `scripts/judge-rubric.md` | open | — | n/m | 13 | no | 2.1 | 165 | 0 | 25 | 13 | 22 |
| 77 | `skills/build-pipeline/references/verify-step-detail.md` | open | — | n/m | 13 | no | 2.1 | 167 | 0 | 73 | 4 | 42 |
| 78 | `skills/build-pipeline/references/work-kind-table.md` | open | — | n/m | 13 | no | 2.1 | 169 | 0 | 22 | 13 | 19 |
| 79 | `docs/architecture-method.md` | open | — | n/m | 12 | no | 2.1 | 172 | 0 | 47 | 0 | 142 |
| 80 | `skills/build-pipeline/references/footprint-read.md` | open | — | n/m | 12 | no | 2.1 | 174 | 0 | 61 | 2 | 33 |
| 81 | `spec/agent-request.md` | open | — | n/m | 12 | no | 2.1 | 176 | 0 | 44 | 0 | 59 |
| 82 | `spec/engine-instance-pair.md` | open | — | n/m | 12 | no | 2.1 | 178 | 0 | 46 | 0 | 41 |
| 83 | `skills/build-pipeline/references/architecture-step-detail.md` | open | — | n/m | 11 | no | 2.1 | 180 | 0 | 69 | 5 | 37 |
| 84 | `skills/build-pipeline/references/guardrails-catalog.md` | open | — | n/m | 11 | no | 2.1 | 182 | 0 | 76 | 9 | 22 |
| 85 | `skills/communicator/references/page-lifecycle.md` | open | — | n/m | 11 | no | 2.1 | 184 | 0 | 50 | 0 | 117 |
| 86 | `skills/spec-author/README.md` | open | — | n/m | 11 | no | 2.1 | 186 | 0 | 52 | 0 | 63 |
| 87 | `spec/public-contract.md` | open | — | n/m | 11 | no | 2.1 | 188 | 0 | 42 | 0 | 48 |
| 88 | `spec/settings-card.md` | open | — | n/m | 11 | no | 2.1 | 191 | 0 | 52 | 0 | 48 |
| 89 | `docs/plans/2026-07-28-top-level-readability.md` | open | — | n/m | 10 | no | 2.1 | 193 | 0 | 51 | 4 | 279 |
| 90 | `skills/build-pipeline/README.md` | open | — | n/m | 10 | no | 2.1 | 195 | 0 | 60 | 1 | 65 |
| 91 | `spec/agent-identity.md` | open | — | n/m | 10 | no | 2.1 | 197 | 0 | 47 | 0 | 41 |
| 92 | `spec/pack-upgrade.md` | open | — | n/m | 10 | no | 2.1 | 199 | 0 | 46 | 0 | 30 |
| 93 | `docs/onboarding-and-settings.md` | open | — | n/m | 9 | no | 2.1 | 201 | 0 | 40 | 0 | 113 |
| 94 | `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | open | — | n/m | 9 | no | 2.1 | 203 | 0 | 35 | 4 | 32 |
| 95 | `skills/spec-author/references/primary-unit.md` | open | — | n/m | 9 | no | 2.1 | 205 | 0 | 58 | 0 | 49 |
| 96 | `spec/adopt-existing-project.md` | open | — | n/m | 9 | no | 2.1 | 207 | 0 | 44 | 0 | 32 |
| 97 | `spec/product-map.md` | open | — | n/m | 9 | no | 2.1 | 209 | 0 | 45 | 0 | 29 |
| 98 | `docs/pipeline.md` | open | — | n/m | 8 | no | 2.1 | 211 | 0 | 44 | 0 | 141 |
| 99 | `docs/spec-format-by-project-type.md` | open | — | n/m | 8 | no | 2.1 | 214 | 0 | 41 | 6 | 89 |
| 100 | `inbox/2026-08-08-verdict-lands-same-minute.md` | open | — | n/m | 8 | no | 2.1 | 216 | 0 | 54 | 4 | 29 |
| 101 | `skills/communicator/references/writing-register.md` | open | — | n/m | 8 | no | 2.1 | 218 | 0 | 45 | 1 | 156 |
| 102 | `skills/spec-author/references/the-spine.md` | open | — | n/m | 8 | no | 2.1 | 220 | 0 | 70 | 0 | 51 |
| 103 | `skills/test-author/README.md` | open | — | n/m | 8 | no | 2.1 | 222 | 0 | 35 | 4 | 96 |
| 104 | `docs/pair-adoption.md` | open | — | n/m | 7 | no | 2.1 | 224 | 0 | 47 | 0 | 116 |
| 105 | `inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md` | open | — | n/m | 7 | no | 2.1 | 226 | 0 | 33 | 0 | 61 |
| 106 | `scripts/read-grant-ask.md` | open | — | n/m | 7 | no | 2.1 | 228 | 0 | 28 | 4 | 20 |
| 107 | `skills/build-pipeline/references/drafter-applier-example.md` | open | — | n/m | 7 | no | 2.1 | 230 | 0 | 67 | 4 | 16 |
| 108 | `skills/communicator/references/rule-histories.md` | open | — | n/m | 7 | no | 2.1 | 232 | 0 | 43 | 4 | 37 |
| 109 | `skills/product-prover-pack/SKILL.md` | open | — | n/m | 7 | no | 2.1 | 235 | 0 | 47 | 0 | 121 |
| 110 | `spec/agent-birth.md` | open | — | n/m | 7 | no | 2.1 | 237 | 0 | 49 | 0 | 35 |
| 111 | `docs/push-law.md` | open | — | n/m | 6 | no | 2.1 | 239 | 0 | 53 | 1 | 82 |
| 112 | `skills/feedback-intake/README.md` | open | — | n/m | 6 | no | 2.1 | 241 | 0 | 35 | 0 | 95 |
| 113 | `skills/publish/README.md` | open | — | n/m | 6 | no | 2.1 | 243 | 0 | 40 | 4 | 18 |
| 114 | `skills/text-audit-pack/SKILL.md` | open | — | n/m | 6 | no | 2.1 | 245 | 0 | 58 | 0 | 93 |
| 115 | `docs/adoption.md` | open | — | n/m | 5 | no | 2.1 | 247 | 0 | 51 | 0 | 138 |
| 116 | `docs/norms/work-board.provenance.md` | open | — | n/m | 5 | no | 2.1 | 249 | 0 | 52 | 0 | 18 |
| 117 | `skills/spec-author/references/composition-sweep.md` | open | — | n/m | 5 | no | 2.1 | 251 | 0 | 55 | 0 | 39 |
| 118 | `spec/draft-sandbox.md` | open | — | n/m | 5 | no | 2.1 | 253 | 0 | 61 | 0 | 21 |
| 119 | `templates/DECISIONS.template.md` | open | — | n/m | 5 | no | 2.1 | 255 | 0 | 36 | 4 | 30 |
| 120 | `templates/JOURNAL.template.md` | open | — | n/m | 5 | no | 2.1 | 258 | 0 | 24 | 5 | 20 |
| 121 | `templates/NEXT_STEPS.template.md` | open | — | n/m | 5 | no | 2.1 | 260 | 0 | 27 | 4 | 25 |
| 122 | `templates/PROBLEMS.template.md` | open | — | n/m | 5 | no | 2.1 | 262 | 0 | 25 | 5 | 21 |
| 123 | `docs/matrix-notes/guardrails.md` | open | — | n/m | 4 | no | 2.1 | 264 | 0 | 48 | 0 | 64 |
| 124 | `skills/build-pipeline/references/minor-bump-gate.md` | open | — | n/m | 4 | no | 2.1 | 266 | 0 | 65 | 0 | 20 |
| 125 | `skills/communicator/references/words.md` | open | — | n/m | 4 | no | 2.1 | 268 | 0 | 57 | 0 | 87 |
| 126 | `spec/external-publish.md` | open | — | n/m | 4 | no | 2.1 | 270 | 0 | 44 | 0 | 21 |
| 127 | `templates/KILL_LIST.template.md` | open | — | n/m | 4 | no | 2.1 | 272 | 0 | 16 | 4 | 12 |
| 128 | `templates/profile.template.md` | open | — | n/m | 4 | no | 2.1 | 274 | 0 | 72 | 2 | 30 |
| 129 | `work/ladder-measurement.md` | open | — | n/m | 4 | no | 2.1 | 276 | 0 | 33 | 0 | 143 |
| 130 | `SURFACES.md` | open | — | n/m | 3 | no | 2.1 | 278 | 0 | 26 | 2 | 15 |
| 131 | `docs/MEASUREMENTS.md` | open | — | n/m | 3 | no | 2.1 | 281 | 0 | 36 | 0 | 243 |
| 132 | `docs/audits/2026-08-07-cost-map.md` | open | — | n/m | 3 | no | 2.1 | 283 | 0 | 20 | 3 | 74 |
| 133 | `docs/norms/onboarding-card-2026-07-10.provenance.md` | open | — | n/m | 3 | no | 2.1 | 285 | 0 | 35 | 0 | 6 |
| 134 | `inbox/2026-08-08-profile-briefed-worker-ab-result.md` | open | — | n/m | 3 | no | 2.1 | 287 | 0 | 79 | 0 | 35 |
| 135 | `inbox/2026-08-12-preshow-lint-script-missing.md` | open | — | n/m | 3 | no | 2.1 | 289 | 0 | 39 | 1 | 25 |
| 136 | `scripts/grant-ask.md` | open | — | n/m | 3 | no | 2.1 | 291 | 0 | 19 | 3 | 12 |
| 137 | `skills/build-pipeline/references/request-kind-table.md` | open | — | n/m | 3 | no | 2.1 | 293 | 0 | 28 | 2 | 28 |
| 138 | `skills/communicator/README.md` | open | — | n/m | 3 | no | 2.1 | 295 | 0 | 37 | 1 | 49 |
| 139 | `skills/feedback-collector/README.md` | open | — | n/m | 3 | no | 2.1 | 297 | 0 | 32 | 1 | 45 |
| 140 | `spec/wish-intake.md` | open | — | n/m | 3 | no | 2.1 | 299 | 0 | 42 | 0 | 21 |
| 141 | `skills/build-pipeline/references/excuses-table.md` | open | — | n/m | 2 | no | 2.1 | 301 | 0 | 18 | 2 | 14 |
| 142 | `skills/build-pipeline/references/mockup-first-entry.md` | open | — | n/m | 2 | no | 2.1 | 304 | 0 | 42 | 1 | 12 |
| 143 | `skills/live-spec-base/references/settings-ladder.md` | open | — | n/m | 2 | no | 2.1 | 306 | 0 | 28 | 0 | 84 |
| 144 | `skills/spec-author/references/anti-patterns.md` | open | — | n/m | 2 | no | 2.1 | 308 | 0 | 54 | 0 | 29 |
| 145 | `skills/spec-author/references/change-record.md` | open | — | n/m | 2 | no | 2.1 | 310 | 0 | 54 | 0 | 31 |
| 146 | `spec/fresh-start.md` | open | — | n/m | 2 | no | 2.1 | 312 | 0 | 34 | 0 | 46 |
| 147 | `templates/skill-review.template.md` | open | — | n/m | 2 | no | 2.1 | 314 | 0 | 14 | 2 | 20 |
| 148 | `docs/plans/2026-07-29-specification-subdivision.md` | open | — | n/m | 1 | no | 2.1 | 316 | 0 | 44 | 0 | 778 |
| 149 | `docs/prior-art.md` | open | — | n/m | 1 | no | 2.1 | 318 | 0 | 17 | 1 | 20 |
| 150 | `skills/live-spec-base/README.md` | open | — | n/m | 1 | no | 2.1 | 320 | 0 | 28 | 0 | 4 |
| 151 | `skills/spec-author/references/completeness-pass.md` | open | — | n/m | 1 | no | 2.1 | 322 | 0 | 39 | 0 | 36 |
| 152 | `skills/spec-author/references/glossary.md` | open | — | n/m | 1 | no | 2.1 | 324 | 0 | 43 | 0 | 53 |
| 153 | `templates/ARCHITECTURE.template.md` | open | — | n/m | 1 | no | 2.1 | 326 | 0 | 25 | 1 | 231 |
| 154 | `PRODUCT_SPEC.index.md` | open | — | n/m | 0 | ok | 2.1 | 329 | 0 | 0 | 0 | 396 |
| 155 | `adopt/START.md` | open | — | n/m | 0 | ok | 2.1 | 331 | 0 | 25 | 0 | 139 |
| 156 | `docs/PROGRESS.md` | open | — | n/m | 0 | ok | 2.1 | 333 | 0 | 22 | 0 | 325 |
| 157 | `docs/audits/2026-08-07-number-rulings.md` | open | — | n/m | 0 | ok | 2.1 | 335 | 0 | 24 | 0 | 122 |
| 158 | `docs/plans/2026-07-28-two-goals-one-campaign.md` | open | n/m | no | 0 | ok | 2.1 | 337 | 1 | 25 | 0 | 153 |
| 159 | `docs/plans/2026-08-07-night-plan.md` | open | — | n/m | 0 | ok | 2.1 | 339 | 0 | 25 | 0 | 91 |
| 160 | `skills/build-pipeline/references/project-setup.md` | open | — | n/m | 0 | ok | 2.1 | 341 | 0 | 24 | 0 | 73 |
| 161 | `skills/live-spec-base/references/glossary.md` | open | — | n/m | 0 | ok | 2.1 | 343 | 0 | 22 | 0 | 49 |
| 162 | `skills/live-spec-base/references/worked-examples.md` | open | — | n/m | 0 | ok | 2.1 | 345 | 0 | 22 | 0 | 31 |
| 163 | `templates/PRODUCT_SPEC.template.md` | open | — | n/m | 0 | ok | 2.1 | 347 | 0 | 24 | 0 | 140 |
| 164 | `templates/ROADMAP.template.md` | open | — | n/m | 0 | ok | 2.1 | 349 | 0 | 24 | 0 | 128 |
| 165 | `templates/TEST_MATRIX.template.md` | open | — | n/m | 0 | ok | 2.1 | 351 | 0 | 25 | 0 | 95 |
| 166 | `work/2026-08-15-branch-table.md` | open | — | n/m | 0 | ok | 2.1 | 354 | 0 | 19 | 0 | 47 |
| 167 | `work/2026-08-15-unowned-numbers.md` | open | — | n/m | 0 | ok | 2.1 | 356 | 0 | 25 | 0 | 84 |

### The specification's own size

| indicator | today | target |
|---|---|---|
| bytes | 49,381 | under 840,000 |
| requirements | 0 | no target |
| acceptance criteria | 0 | no target |
| bytes per criterion | not measured | falls or holds, bound 207.2 |
| repeated pairs | 0 | falls or holds |
| lines per part file | not measured | 250, once the division lands |

## What each column means

Each indicator carries five things: what it counts, why the project measures it, what changes when it moves, the command that produces it, and the value it aims at.

A file is carried to `finished` by two checks, and the table gives each check a count column and an ok column beside it. The first check is a script: it counts writing defects and reaches zero or it does not. The second check is live readers: two fresh readers read the file and their two lists are compared. The first check costs one command, the second costs two workers and a repair pass per round, which is why the table shows them apart.

**state** — a file reads `finished` when both checks read ok. Every other file reads `unfinished`. This is the campaign's only finish line, and the queue advances when a file reaches it.

**findings** — how many writing defects the script counts. Three counts added together: prose sentences longer than 25 words, plus the findings of the style check, plus the findings of the register check. The 25 is the human-prose cap of rule r08 in `guardrails/language-rules.json`, and the counter applies it to every file. `python3 scripts/rule-census.py`. Target: zero.

**longest sentence** — the words in the file's longest prose sentence. One long sentence marks the paragraph a reader will reread, so it names where to start. Same command. Target: 25 words. The rule allows a numbered acceptance criterion 35 words, and the counter makes no such exception. So part of PRODUCT_SPEC.md's count is criteria the rule permits.

**style** — the findings of `scripts/spec-style-lint.py --tier full` alone, carried as its own column because a style finding is repaired differently from a long sentence. Target: zero.

**readings** — how many fresh readers have read this file. A reader holds no project access: only the file and one fixed list of questions, at `docs/briefs/reader-prompt.md`. Each reading writes a dated record under `docs/language-reads/`. Target: the count rises until two readers of one round agree on nothing.

**both stopped** — how many places both readers of the latest round stopped at. A single reader's list never repeats, so one reader measures that reader's path and two readers agreeing measures the text. While this stands above zero the file is repaired and read again. Counted by hand from the two reading records and stored per round in `guardrails/progress-baseline.json`. Target: zero.

**script ok** — the findings column at zero. The same number is a push check: `guardrails/check-doc-findings-bound.py` refuses the push when a file counts more findings than `guardrails/rule-census.json` records for it.

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
