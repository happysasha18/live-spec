# Rule census — 2026-07-28

Every live document measured against the rules that carry a machine. This is the order the rewrite runs in, worst first, and the seed of the limit that only falls (ROADMAP 148, 460).

A record of something that happened is out of scope: the journal, the decision log, the prover records, the readings, the attic, and the prototype trees state what was written at the time.

`long` counts prose sentences past 25 words, which is rule r08's human-prose cap read out of the rule home. `style` is `scripts/spec-style-lint.py --tier full`. `register` is `scripts/preshow-register-lint.py`. `longest` is the longest prose sentence in the file.

| file | bytes | long | longest | style | register | total |
|---|---:|---:|---:|---:|---:|---:|
| `PRODUCT_SPEC.md` | 651195 | 1831 | 80 | 0 | 0 | **1831** |
| `skills/build-pipeline/SKILL.md` | 56815 | 139 | 198 | 137 | 0 | **276** |
| `skills/product-prover/SKILL.md` | 60263 | 127 | 86 | 126 | 0 | **253** |
| `skills/live-spec-base/SKILL.md` | 57996 | 141 | 97 | 103 | 0 | **244** |
| `ROADMAP.md` | 167284 | 8 | 242 | 213 | 0 | **221** |
| `skills/communicator/SKILL.md` | 45364 | 87 | 105 | 115 | 0 | **202** |
| `skills/spec-author/SKILL.md` | 57661 | 117 | 121 | 0 | 0 | **117** |
| `docs/prior-art-frameworks.md` | 16009 | 7 | 42 | 107 | 0 | **114** |
| `docs/language-rule-coverage.md` | 69828 | 83 | 81 | 24 | 0 | **107** |
| `ARCHITECTURE.md` | 90015 | 88 | 870 | 0 | 0 | **88** |
| `skills/design-reviewer/SKILL.md` | 23527 | 70 | 92 | 18 | 0 | **88** |
| `docs/prior-art-longtail.md` | 17043 | 15 | 53 | 68 | 0 | **83** |
| `docs/restyle-repoint-log.md` | 14510 | 20 | 78 | 63 | 0 | **83** |
| `TEST_MATRIX.md` | 439981 | 8 | 46 | 73 | 0 | **81** |
| `docs/language-rules.md` | 44751 | 63 | 91 | 17 | 0 | **80** |
| `skills/publish/SKILL.md` | 13656 | 33 | 85 | 35 | 0 | **68** |
| `docs/spec-style.md` | 14461 | 32 | 64 | 33 | 0 | **65** |
| `skills/test-author/SKILL.md` | 19008 | 38 | 91 | 20 | 0 | **58** |
| `guardrails/README.md` | 15259 | 30 | 68 | 24 | 0 | **54** |
| `skills/build-pipeline/references/delegation-protocol.md` | 8388 | 28 | 71 | 25 | 0 | **53** |
| `skills/text-audit/SKILL.md` | 17487 | 29 | 62 | 24 | 0 | **53** |
| `adopt/ADOPT.md` | 22159 | 46 | 93 | 0 | 0 | **46** |
| `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | 9035 | 14 | 65 | 27 | 0 | **41** |
| `skills/product-prover/README.md` | 11272 | 21 | 71 | 19 | 0 | **40** |
| `templates/ARCHITECTURE.template.md` | 10989 | 23 | 51 | 17 | 0 | **40** |
| `docs/lenses.md` | 19283 | 37 | 49 | 2 | 0 | **39** |
| `docs/decisions/2026-07-06-overnight-decisions.md` | 6878 | 8 | 51 | 30 | 0 | **38** |
| `docs/decisions/2026-07-07-morning-round3.md` | 4653 | 6 | 64 | 32 | 0 | **38** |
| `docs/language-defects.md` | 18368 | 34 | 78 | 4 | 0 | **38** |
| `hooks/conduct-law.md` | 3744 | 11 | 72 | 27 | 0 | **38** |
| `docs/spec-compaction-protocol.md` | 7695 | 11 | 60 | 25 | 0 | **36** |
| `inbox/README.md` | 9996 | 28 | 75 | 7 | 0 | **35** |
| `docs/prose-quality-gate-design.md` | 6575 | 9 | 65 | 25 | 0 | **34** |
| `docs/roadmap-format.md` | 11994 | 33 | 60 | 0 | 0 | **33** |
| `docs/test-matrix-format.md` | 10829 | 32 | 59 | 1 | 0 | **33** |
| `skills/communicator/references/field-examples.md` | 7318 | 17 | 51 | 15 | 0 | **32** |
| `README.md` | 10536 | 16 | 88 | 13 | 0 | **29** |
| `skills/feedback-intake/SKILL.md` | 7681 | 14 | 48 | 12 | 0 | **26** |
| `NEXT_STEPS.md` | 8132 | 11 | 71 | 12 | 0 | **23** |
| `skills/feedback-collector/SKILL.md` | 8032 | 4 | 41 | 19 | 0 | **23** |
| `docs/migration-sample/2026-07-20-backdescribe-sample.md` | 8025 | 8 | 76 | 14 | 0 | **22** |
| `skills/design-reviewer/README.md` | 6593 | 16 | 55 | 5 | 0 | **21** |
| `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | 4528 | 9 | 60 | 11 | 0 | **20** |
| `templates/agent.template.md` | 5328 | 10 | 47 | 9 | 0 | **19** |
| `docs/spec-format.md` | 9332 | 15 | 98 | 3 | 0 | **18** |
| `docs/wishes/2026-07-09-prover-unwritten-seams.md` | 3013 | 9 | 59 | 9 | 0 | **18** |
| `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | 2122 | 6 | 36 | 12 | 0 | **18** |
| `docs/worker-liveness.md` | 7719 | 16 | 52 | 1 | 0 | **17** |
| `docs/architecture-format.md` | 8321 | 16 | 49 | 0 | 0 | **16** |
| `skills/spec-author/README.md` | 5148 | 11 | 52 | 5 | 0 | **16** |
| `docs/test-method.md` | 7940 | 15 | 52 | 0 | 0 | **15** |
| `skills/build-pipeline/README.md` | 5020 | 9 | 60 | 6 | 0 | **15** |
| `skills/communicator/references/writing-register.md` | 9062 | 8 | 45 | 7 | 0 | **15** |
| `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | 3566 | 7 | 54 | 7 | 0 | **14** |
| `skills/text-audit/README.md` | 5393 | 9 | 47 | 5 | 0 | **14** |
| `templates/DECISIONS.template.md` | 1493 | 1 | 36 | 13 | 0 | **14** |
| `docs/spec-format-by-project-type.md` | 5529 | 2 | 41 | 11 | 0 | **13** |
| `scripts/judge-rubric.md` | 2280 | 0 | 25 | 13 | 0 | **13** |
| `skills/build-pipeline/references/work-kind-table.md` | 3103 | 0 | 22 | 13 | 0 | **13** |
| `docs/architecture-method.md` | 8856 | 12 | 47 | 0 | 0 | **12** |
| `skills/build-pipeline/references/guardrails-catalog.md` | 2041 | 2 | 76 | 10 | 0 | **12** |
| `skills/test-author/README.md` | 6396 | 4 | 35 | 8 | 0 | **12** |
| `templates/ROADMAP.template.md` | 5808 | 12 | 74 | 0 | 0 | **12** |
| `skills/communicator/references/page-lifecycle.md` | 6211 | 11 | 50 | 0 | 0 | **11** |
| `docs/onboarding-and-settings.md` | 6970 | 10 | 53 | 0 | 0 | **10** |
| `OVERVIEW.md` | 7141 | 8 | 67 | 1 | 0 | **9** |
| `docs/language-worked-example.md` | 24176 | 6 | 41 | 3 | 0 | **9** |
| `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | 2389 | 5 | 35 | 4 | 0 | **9** |
| `skills/feedback-collector/README.md` | 2901 | 2 | 32 | 7 | 0 | **9** |
| `docs/pipeline.md` | 8733 | 8 | 44 | 0 | 0 | **8** |
| `skills/communicator/README.md` | 2208 | 2 | 37 | 6 | 0 | **8** |
| `skills/feedback-intake/README.md` | 5640 | 6 | 35 | 2 | 0 | **8** |
| `templates/PRODUCT_SPEC.template.md` | 4373 | 6 | 32 | 2 | 0 | **8** |
| `docs/pair-adoption.md` | 7425 | 7 | 47 | 0 | 0 | **7** |
| `scripts/read-grant-ask.md` | 1286 | 3 | 28 | 4 | 0 | **7** |
| `skills/build-pipeline/references/drafter-applier-example.md` | 1166 | 3 | 67 | 4 | 0 | **7** |
| `templates/TEST_MATRIX.template.md` | 3943 | 5 | 95 | 2 | 0 | **7** |
| `docs/adoption.md` | 7111 | 6 | 51 | 0 | 0 | **6** |
| `docs/push-law.md` | 4951 | 5 | 53 | 1 | 0 | **6** |
| `skills/publish/README.md` | 1041 | 2 | 40 | 4 | 0 | **6** |
| `templates/JOURNAL.template.md` | 1011 | 0 | 24 | 6 | 0 | **6** |
| `templates/NEXT_STEPS.template.md` | 1099 | 1 | 27 | 4 | 0 | **5** |
| `templates/PROBLEMS.template.md` | 1267 | 0 | 25 | 5 | 0 | **5** |
| `SURFACES.md` | 779 | 1 | 26 | 3 | 0 | **4** |
| `guardrails/release-note-fixtures/note-offers.md` | 543 | 1 | 30 | 3 | 0 | **4** |
| `skills/build-pipeline/references/excuses-table.md` | 1297 | 0 | 18 | 4 | 0 | **4** |
| `skills/build-pipeline/references/minor-bump-gate.md` | 1814 | 4 | 65 | 0 | 0 | **4** |
| `templates/KILL_LIST.template.md` | 674 | 0 | 16 | 4 | 0 | **4** |
| `templates/profile.template.md` | 1622 | 2 | 72 | 2 | 0 | **4** |
| `docs/norms/onboarding-card-2026-07-10.provenance.md` | 654 | 3 | 35 | 0 | 0 | **3** |
| `scripts/grant-ask.md` | 685 | 0 | 19 | 3 | 0 | **3** |
| `skills/build-pipeline/references/request-kind-table.md` | 2108 | 1 | 28 | 2 | 0 | **3** |
| `templates/skill-review.template.md` | 489 | 0 | 14 | 2 | 0 | **2** |
| `docs/prior-art.md` | 1249 | 0 | 17 | 1 | 0 | **1** |
| `guardrails/release-note-fixtures/note-neither.md` | 399 | 1 | 28 | 0 | 0 | **1** |
| `skills/live-spec-base/README.md` | 279 | 1 | 28 | 0 | 0 | **1** |
| `PRODUCT_SPEC.index.md` | 25028 | 0 | 0 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/report-names-far-in-runnable.md` | 367 | 0 | 14 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/report-runnable-no-standdown.md` | 225 | 0 | 9 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/report-stands-far-down.md` | 311 | 0 | 14 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/vocab-clean.md` | 147 | 0 | 15 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/vocab-deferred-without-trigger.md` | 129 | 0 | 10 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/vocab-far-with-trigger.md` | 183 | 0 | 15 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/window-first-offer-after-window.md` | 183 | 0 | 12 | 0 | 0 | **0** |
| `guardrails/far-tier-fixtures/window-second-offer-in-window.md` | 183 | 0 | 12 | 0 | 0 | **0** |
| `guardrails/release-note-fixtures/note-no-offer.md` | 417 | 0 | 21 | 0 | 0 | **0** |

## Totals

106 files measured. 3676 sentences past the cap, 1753 style findings, 0 register findings, 5429 in all.
