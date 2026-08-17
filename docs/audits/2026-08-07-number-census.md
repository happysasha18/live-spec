# Row 576 — numeric-standard census

Read-only sweep of /Users/sashaabramovich/live-spec for every NUMERIC STANDARD (floor, cap, ceiling,
target, budget, timeout-as-bar, cadence, ratio, or gating count). Excludes measured facts, versions,
dates, line-number pins, ids, fixture data, loop indices. One row per distinct standard; every home it
appears in is listed. Provenance leads come from grepping DECISIONS.md, JOURNAL.md, and
docs/queue-archive/ — they are leads for the seat's ruling, not the ruling itself.

Two prior findings bear directly on this sweep and are not repeated as rows below:
- DECISIONS.md 2026-08-07 ~01:10 (row 568, the cost audit): "no numeric size caps on specifications... no
  self-invented numeric standards anywhere... every standard the process holds itself to is either
  yours, derived and justified, or absent." This is the ruling class this census exists to apply.
- The same entry names one standard already struck: an invented 360-second suite-run budget. The suite
  wall-time budget in ARCHITECTURE.md now reads `<= 470 s [default]` and re-measures itself at every
  gate landing (watched by guardrails/check-suite-budget.sh, INV-41/INV-164, row 361) — this is the
  "derived and justified" shape, not an invented fixed number, per journal 2026-07-16/2026-08-06.

## guardrails/*.py, *.sh

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 1 | 12 | guardrails/check-board.py:51 (also PRODUCT_SPEC.md:5678, tests/test_board.py:7) | max items shown on the waiting board before the oldest is demoted | no trace found |
| 2 | 12 | guardrails/check-criterion-readability.py:368 (also guardrails/criterion-readability.json:4) | max findings printed per readability report run | no trace found |
| 3 | 500 | guardrails/check-delta-record.py:59 (also tests/test_delta_classifier.py:72, skills/spec-author/SKILL.md:684, PRODUCT_SPEC.md:6743) | byte cap on one declared-new spec criterion | no trace found — DECISIONS.md ~01:10 explicitly rejects numeric size caps on spec text; this cap predates that ruling and looks like the class it struck |
| 4 | 4 | guardrails/check-deferral-marker.py:132 | word-lookback window to detect a negator before a deferral signal | no trace found |
| 5 | 2 | guardrails/check-deposit-description.py:69 (also check-description-field.py:74, tests/test_description_field.py:141) | min plain words for a first-mention/Formal-index description to count as non-empty | journal 2026-07-17: "the presence floors of the two nets were aligned to two words" — session-set, no cited exchange with Alexander |
| 6 | 14 | guardrails/check-far-tier.py:85 (also skills/live-spec-base/SKILL.md:701, PRODUCT_SPEC.md:5719) | day-window: at most one unasked far-tier/far-backlog surfacing offer per window | journal row 414/INV-223: "cadence default carried by the base-rulebook settings ladder... at most once every 14 days" — session default, no trace of his word on the number 14 |
| 7 | 2 | guardrails/check-landing-next-steps.py:191 | min day-lag between a commit and its landed date to read as historical relocation, not a fresh landing | no trace found |
| 8 | 4 | guardrails/check-language-rules.py:69 | cap on rules allowed to stand with no held catcher and no stated reason | no trace found |
| 9 | 25 | guardrails/check-pin-drift.sh:57 | line-window searched around a pin for a drifted label | no trace found |
| 10 | 4 | guardrails/check-pin-drift.sh:63 | min label-word length counted toward drift matching | no trace found |
| 11 | 50.0 (%) | guardrails/check-runaway-child.py:52 | CPU-share percentage at/above which a descendant process counts as "burning" | no trace found |
| 12 | 40 | guardrails/check-skill-loadability.sh:23 | max lines within which a skill's frontmatter closing `---` must appear | no trace found |
| 13 | 3 | guardrails/check-tier-refusal.py:213 (also guardrails/tier-refusal.json:17) | refusals required in the record before a phrase is promoted to a routing pattern | no trace found |
| 14 | 2–8 | guardrails/tier-refusal.json:18 | min/max word length for a promotable refusal phrase | no trace found |
| 15 | 3 | guardrails/check-vocabulary.py:64 | min word length counted as "significant" when checking glossary-term usage | no trace found |
| 16 | 24.0 (hours) | guardrails/check-worker-restore.py:122 (also tests/test_worker_restore.py:484, guardrails/README.md:215) | default lookback window scanning recent worker-run transcripts | no trace found |
| 17 | 3 | guardrails/crosscut_counter.py:28 (also tests/test_crosscut_counter.py:49, skills/build-pipeline/references/minor-bump-gate.md:10) | landings on one node pair that flags it as a boundary-move candidate | no trace found |
| 18 | 20 | guardrails/net_meter.py:47 (also tests/test_net_meter.py:45) | run-window before a net's zero-fire streak reads as a retirement candidate | no trace found |
| 19 | 2 | guardrails/node_growth_counter.py:73 (also guardrails/node-file-cap.json:3, tests/test_node_growth.py:138, skills/design-reviewer/SKILL.md:169) | default max nodes co-resident in one code file before the growth ratchet flags it | journal row 390/INV-233: "seeded at the current count... every other file two or fewer" — session-derived from measuring the tree at landing time, not an arbitrary invention, but no cited word from Alexander on the number itself |
| 20 | 3 (x3 files) | guardrails/node-file-cap.json:6–8 | per-file seeded node cap for the three SKILL.md files that already carried three nodes at landing | same journal row 390 lead as #19 — measured-at-landing seed |
| 21 | 120.0 (sec) | guardrails/reap_owned_group.py:39 (also tests/test_reap_owned_group.py:107) | seconds an output file's mtime must lag before a "running" worker counts as idle-output | no trace found |

## guardrails/*.json

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 22 | 35 | guardrails/criterion-readability.json:9 (also language-rules.json:713, rule-census.json:2 [25, general prose variant], skills/text-audit/SKILL.md:92, docs/language-rules.md:256) | max words for a spec-body criterion sentence (r08) before it reds | no trace found — r08 word caps are process rule; not found named in DECISIONS.md/JOURNAL.md |
| 23 | 25 | guardrails/language-rules.json:714 (also rule-census.json:2, scripts/measurements-table.py:208, skills/text-audit/SKILL.md:92,318, docs/language-rules.md:256) | word count above which a general human-prose/artifact sentence is flagged (r08) | no trace found |
| 24 | 15–25 | skills/communicator/references/writing-register.md:13 (also skills/text-audit/SKILL.md:318) | target word-count band for a one-idea human-prose sentence | no trace found |
| 25 | 469 | guardrails/criterion-readability.json:11 (also language-rules.json:719, docs/language-rules.md:256) | grandfathered baseline count of over-word-cap criteria the r08 arm tolerates (ratchets down only) | journal 2026-07-27: "the criterion-readability ratchet holds four arms over the spec's acceptance criteria at the counts measured today" — session-measured baseline, no exchange cited |
| 26 | 25 (chars) | guardrails/criterion-readability.json:17 (also language-rules.json:2183, scripts/spec-style-lint.py, docs/language-rules.md:594) | max characters an inline-defined term's aside may run before it reds (r35) | no trace found |
| 27 | 120 | guardrails/criterion-readability.json:50 (also language-rules.json:2184) | grandfathered baseline count of criteria carrying an inline gloss (r35 arm) | same lead as #25 (measured-baseline ratchet) |
| 28 | 4 | guardrails/criterion-readability.json:56 (also language-rules.json:2233, docs/language-rules.md:608) | min words required in a criterion's closing clause to escape the absolute-tail arm (r36) | no trace found |
| 29 | 147 | guardrails/criterion-readability.json:106 (also language-rules.json:2234) | grandfathered baseline count of absolute-tail defects tolerated (r36) | same lead as #25 |
| 30 | 3 | guardrails/criterion-readability.json:112–113 (also language-rules.json:903–904, docs/language-rules.md:302) | max anchor codes / code spans a criterion may carry before the anchor-noise arm reds (r11) | no trace found |
| 31 | 61 | guardrails/criterion-readability.json:115 (also language-rules.json:905, docs/language-rules.md:302) | grandfathered baseline count of anchor-noise defects (r11) | same lead as #25 |
| 32 | 60 | guardrails/criterion-readability.json:121 | max total words (line + bullets) a criterion may run before the criterion-load arm reds | no trace found |
| 33 | 31 | guardrails/criterion-readability.json:123 | grandfathered baseline count of criterion-load defects | same lead as #25 |
| 34 | 840,000 (bytes) | guardrails/doc-bounds.json:5 (also docs/PROGRESS.md:11, scripts/measurements-table.py:288) | byte ceiling for PRODUCT_SPEC.md | no trace found — reads like the size-cap class DECISIONS.md ~01:10 rejected ("no numeric size caps on specifications; the standard is no redundancy") |
| 35 | 700,000 (bytes) | guardrails/doc-bounds.json:9 | byte ceiling for ROADMAP.md | no trace found; same size-cap concern as #34 |
| 36 | 530,000 (bytes) | guardrails/doc-bounds.json:13 | byte ceiling for TEST_MATRIX.md | no trace found; same size-cap concern as #34 |
| 37 | 640,000 (bytes) | guardrails/doc-bounds.json:17 | byte ceiling for JOURNAL.md | no trace found; same size-cap concern as #34 |
| 38 | 120 (chars) | guardrails/language-rules.json:1095 (also hooks/register-judge.py:30, docs/language-rules.md:347) | min reply length below which the register judge never fires (r14) | no trace found |
| 39 | 12 (chars) | guardrails/language-rules.json:1096 (also hooks/register_judge_core.py:41, docs/language-rules.md:347) | min quote length below which an offense quote is dropped as hallucinated (r14) | no trace found |
| 40 | 12 (words) | guardrails/language-rules.json:1758 (also scripts/spec-style-lint.py:94) | word-window scanned at a sentence's start for the opener-negation catcher (r27) | no trace found |
| 41 | 550 (chars) | guardrails/language-rules.json:2605 (also hooks/answer-first-scan.json:3, docs/language-rules.md:703) | reply length above which an opening lead/answer-first is required (r46) | no trace found |
| 42 | 220 (chars) | hooks/answer-first-scan.json:8 | max chars for the opening-sentence lead signal | no trace found |
| 43 | 450 (chars) | hooks/answer-first-scan.json:13 | max chars for the opening-block lead signal | no trace found |
| 44 | 2 | guardrails/language-rules.json:2997 (also scripts/measurements-table.py:168, docs/language-rules.md:808) | consecutive clean cold-reads required before a rewritten section counts as fixed (r54) | **his word** — Alexander 2026-08-05 ~22:52, DECISIONS.md: "A text ships when both cold readers return nothing that blocks, twice in a row... zero blocking places for both readers, held over two consecutive rounds" |
| 45 | 0.6 | guardrails/language-rules.json:3115 (also scripts/spec-redundancy-precheck.py:33, docs/language-rules.md:841) | min Jaccard similarity flagging two text units as a possible duplicate (r56) | no trace found |
| 46 | 0.85 | guardrails/language-rules.json:3116 (also scripts/spec-redundancy-precheck.py:34, docs/language-rules.md:841) | min containment ratio flagging two text units as a possible duplicate (r56) | no trace found |
| 47 | 6 | guardrails/language-rules.json:3117 (also scripts/spec-redundancy-precheck.py:32, docs/language-rules.md:841) | min token length before a text unit is eligible for the r56 duplicate check | no trace found |
| 48 | 3 | scripts/spec-redundancy-precheck.py:35 | min shared content tokens before two units are even compared (r56 pre-filter) | no trace found |
| 49 | 25 | guardrails/rule-census.json:2 | word cap the census counts a sentence as "long" against (r08) | duplicate home of #23 |
| 50 | 207.2 | guardrails/spec-ratchet.json:4 | bytes-per-criterion ceiling PRODUCT_SPEC.md must not exceed on a later delivery | no trace found |
| 51 | 10 (sec) | guardrails/tree-counts.json:4 | expected seconds a tree-count reproduction command should take | no trace found |
| 52 | 0 / 119 (or 121) / 0 | scripts/spec-debt-cap.json:1 (also tests/test_convergence_locks.py:59,80,82,84) | ratchet caps: max waivers = 0; max open redundancy pairs, PRODUCT_SPEC.md = 119 (json's own `_reason` field notes it was lowered from 121, and the test still asserts the older <=121 ceiling — a live discrepancy); ARCHITECTURE.md = 0; max style errors = 0 | json's own comment: "Lowered 121 to 119 by the sub-list repair sweep... 116 was raised to 121 at the row-456 architecture-format landing... A later delivery may lower this floor or leave it, never raise it without the same justification." — session-derived, self-documented, no cited word from Alexander |
| 53 | 23 | scripts/register-lint-floor.json:3 (also tests/test_no_self_certification.py:38) | floor on the register lint's pattern count (grows only, never shrinks) | json's own comment cites INV-83 and "the convergence lock, row 217/F2" — session/process rule, no cited word from Alexander on the number 23 itself |
| 54 | 17 | tests/test_convergence_locks.py:52 | an older, lower hard-coded floor-check on the same register-lint-floor.json value (stale relative to the live 23) | same lead as #53; the 17 figure looks like a superseded checkpoint left in the test |

## tests/ (asserts encoding a standard, not fixture noise)

Most rows here duplicate homes already listed above; the ones below are additional or worth a distinct note.

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 55 | 500 | tests/test_communicator_body_thinned.py:22,29-30 (also journal 2026-07-27: "sits at exactly 499 lines, one under the ~500 ideal the size gate holds") | communicator SKILL.md body line-count ideal | journal 2026-07-27 names the "~500 ideal" as "the size gate holds" — a process rule, no cited word from Alexander |
| 56 | 22 | tests/test_communicator_body_thinned.py:36 | count of numbered communicator rule tags that must remain present | no trace found — this reads as a structural/regression count, not clearly a "standard" the work is held to; flagged for the seat to judge |
| 57 | 1 | tests/test_clock_hook.py:57 | script-reported clock time must land within 1 minute of actual now | no trace found (plausible tolerance for a mechanical check, not obviously a chosen "standard") |
| 58 | 100 | tests/test_resume_digest.py:20 (also templates/NEXT_STEPS.template.md:3, docs/worker-liveness.md:57, PRODUCT_SPEC.md:2864) | hard line cap on NEXT_STEPS.md (the resume digest) | no trace found |
| 59 | 6 | tests/test_setup_entry.py:447 | max reads in the routing card's ordered lists | no trace found |
| 60 | 3 | tests/test_traceability.py:556 (also scripts/open-lane.sh:52, PRODUCT_SPEC.md:1891, docs/roadmap-format.md:21, skills/build-pipeline/SKILL.md:563, skills/communicator/SKILL.md:236, skills/live-spec-base/SKILL.md:699) | build-lane cap: at most 3 independent lanes in-work without asking | **his word** — DECISIONS.md 2026-07-06: "the build-lane cap is three parallel lanes; a fourth opens only on your asked word [T-18]" |

## scripts/

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 61 | 10 (sec) | scripts/check-pack-update.sh:45 | max seconds for the remote VERSION curl fetch | no trace found |
| 62 | 40 (chars) | scripts/check-shipped-language.py:89 | character proximity window deciding whether a project name counts as a dated-incident mention | no trace found |
| 63 | 30 (days) | scripts/gate_common.py:119 (also tests/test_prose_gate.py:222, docs/prose-quality-gate-design.md:57) | max days a spec waiver may remain active before it expires | no trace found |
| 64 | 120 (sec) | scripts/gen-tree-counts.py:86 | seconds allowed for one tree-count stage subprocess before timeout | no trace found |
| 65 | 2 | scripts/measurements-table.py:168 | duplicate home of #44 (consecutive clean reading rounds, r54) | see #44 — his word 2026-08-05 |
| 66 | 250 (lines) | scripts/measurements-table.py:242 (also docs/MEASUREMENTS.md:164) | line-count target for a specification part file after subdivision | no trace found — looks like the size-cap class DECISIONS.md ~01:10 rejected |
| 67 | 8 (chars) | scripts/needle-extract.py:53 | min character length for a string constant to count as a traceable check-phrase | no trace found |
| 68 | 160 (chars) | scripts/onboarding-card.py:224 | truncation bound before a project-rules card value is cut | no trace found |
| 69 | 4.5 / 3.0 (ratio), 24.0 / 18.66 / 12.0 (px) | scripts/preshow-legibility-lint.py:52-56 (also PRODUCT_SPEC.md:4060) | WCAG-style contrast-ratio and font-size floors for normal/large/bold-large/body text | journal 2026-07-13 (row 304, INV-139): "a legibility floor... Text meets a minimum contrast ratio against its background and a minimum size... the pack ships the law, the default numbers (host-settable)." These numbers match the published WCAG AA thresholds (4.5:1 / 3:1, 18pt/14pt-bold ≈ 24px/18.66px) — plausibly derived-and-justified from an external standard rather than invented, but no explicit citation to WCAG is in the tree, and no word from Alexander on the specific figures |
| 70 | 2 | scripts/progress-report.py:197 | count of highest-numbered readings that must both show zero blocking stops for a document to pass | no trace found |
| 71 | 15 | scripts/progress-report.py:323 (also tests/test_progress_report.py:136) | count of worst-scoring files shown in the comprehension summary table | no trace found |
| 72 | 40 | scripts/rank-criterion-defects.py:131 | default cap on rows printed in the criterion-defects table | no trace found |
| 73 | 4 / 4 (words) | scripts/rule-census.py:108-109 | min members for a run of items to score as a roster; max words per member for it to still count as a roster | no trace found |
| 74 | 120 (sec) | scripts/rule-census.py:228 | seconds allowed for a lint subprocess before timeout | no trace found |
| 75 | 0 / 0 / 0 | scripts/spec-done-gate.py:61,64,68 | style-lint errors / open redundancy pairs / surviving judge findings allowed for a spec doc to pass the done gate | consistent with the debt-cap ratchet (#52/#75 overlap); DECISIONS.md ~01:10 rejects size caps but not a zero-defect bar; no explicit citation for the "zero" bar itself |
| 76 | 45 (chars) | scripts/spec-style-lint.py:231 | character window for detecting a definitional lead | no trace found |
| 77 | 3600 (sec) | scripts/stranger-wish-monitor.py:61 (also PRODUCT_SPEC.md:6064, templates/headless_harness.py:173) | seconds after which an ownerless lock/claim (or browser profile dir) is considered abandoned and stealable | no trace found |
| 78 | 4096 (bytes) | scripts/sweep-rendered.py:95 | byte budget read from a page's head to find its clearing mark | no trace found |
| 79 | 30 (sec) | scripts/sweep-rendered.py:143 | seconds allowed for the git ls-files subprocess before timeout | no trace found |

## hooks/

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 80 | 120 (sec) | hooks/conduct-judge-collect.sh:44 (also hooks/register-judge-collect.sh:43) | default timeout for the conduct/register judge's background model call | no trace found |
| 81 | 50 (KB) | hooks/lean-orchestrator-scan.py:56 (also PRODUCT_SPEC.md:5554) | cumulative inline raw-content ceiling before a dispatch-free session is flagged for hoarding reads | no trace found |
| 82 | 6 | PRODUCT_SPEC.md:5554 | count of literal file-dump verbs counted toward the inline-read threshold above | no trace found |
| 83 | 500 | attic/midturn-chat-scan.py:74 (the arm was retired on 2026-08-17) | cap on fragment hashes retained per session state file | no trace found |
| 84 | 25 (sec) | hooks/register_judge_core.py:35 | default timeout for the judge's model subprocess call | no trace found |
| 85 | 80 (chars) | hooks/register_judge_core.py:42 | max verbatim quote span the judge asks the model to copy | no trace found |

## templates/

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 86 | 3600 (sec) | templates/headless_harness.py:173 | seconds after which an ownerless browser profile dir is treated as a killed run's leftover | duplicate concern to #77 |
| 87 | 50 | templates/headless_harness.py:175 | count of harness profile dirs that triggers a leak warning | no trace found |
| 88 | 20 (sec) | templates/headless_harness.py:659 | default timeout waiting for Chrome to write its debug port | no trace found |
| 89 | 100 (retries, ~10s) | templates/headless_harness.py:684 | retry cap waiting for a CDP page target to appear | no trace found |
| 90 | 60 (sec) | templates/headless_harness.py:737 | default per-command timeout for CDP commands | no trace found |
| 91 | 2.0 (sec) | templates/headless_harness.py:738 | default timeout for the launch frame probe | no trace found |
| 92 | 100 (bytes) | templates/test_scaffold.template.py:32 | min byte size a bootstrap document must exceed to not count as an empty shell | no trace found |
| 93 | 1 | templates/test_scaffold.template.py:60 (also PRODUCT_SPEC.md:3859) | max LIVE STATE blocks allowed in NEXT_STEPS.md | no trace found |

## skills/*/SKILL.md and references/*.md

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 94 | 4 | skills/build-pipeline/SKILL.md:177 | required moves in a confirmed bug's class hunt before the bug closes | no trace found |
| 95 | 30 (days) | skills/build-pipeline/SKILL.md:189 (also references/request-kind-table.md:10) | window within which a second bug in the same area re-doors to a feature rather than another patch | no trace found — distinct standard from the 30-day waiver expiry (#63), same numeral |
| 96 | 2 | skills/build-pipeline/SKILL.md:320 | count of additional architecture views owed beside the node map | no trace found |
| 97 | 3 | skills/build-pipeline/SKILL.md:337 | questions in the node-fitness test run at a node's birth | no trace found |
| 98 | 2 | skills/build-pipeline/SKILL.md:339 | "no" answers on the fitness test that make a node premature | no trace found |
| 99 | 6 | skills/build-pipeline/SKILL.md:353 | required checks run when proving the architecture | no trace found |
| 100 | 1 | skills/build-pipeline/SKILL.md:366 (also skills/test-author/SKILL.md:37) | min test-matrix rows owed per spec fact | no trace found |
| 101 | 1 | skills/build-pipeline/SKILL.md:373 | min rows owed per anchor at the verify-by-deed walk | no trace found |
| 102 | 3 | skills/build-pipeline/references/delegation-protocol.md:29 | recorded lines per file required in a brief born from reading existing files | no trace found |
| 103 | 2 | skills/build-pipeline/references/delegation-protocol.md:32 | consecutive unexplained command failures that trigger a worker HALT | no trace found |
| 104 | 300 (lines) / 8 (files) | skills/build-pipeline/references/delegation-protocol.md:34 (also PRODUCT_SPEC.md:5221) | cap on a delegation brief's text length / files-to-edit before it must split | no trace found |
| 105 | 3 | skills/build-pipeline/references/minor-bump-gate.md:5 | required preventive-audit passes before a MINOR version bump | no trace found |
| 106 | 3 | skills/build-pipeline/references/minor-bump-gate.md:8 (also PRODUCT_SPEC.md:1677) | max design-review questions echoed per pass at the minor-bump gate | no trace found |
| 107 | 2 | skills/build-pipeline/references/minor-bump-gate.md:16 (also PRODUCT_SPEC.md:3704, skills/live-spec-base/SKILL.md:329) | occurrence count at which a repeated problem-ledger signature earns an owner | no trace found |
| 108 | 3 | skills/live-spec-base/SKILL.md:332 (also PRODUCT_SPEC.md:3710) | recurrence count at which an unowned ledger signature escalates to a method-level defect | no trace found |
| 109 | 3 | skills/communicator/SKILL.md:88 | max sentences in a step-completion digest ("2-3") | no trace found |
| 110 | 10 (min) | skills/communicator/SKILL.md:93 (also PRODUCT_SPEC.md:736) | beatless-stretch minutes before narration owes a heartbeat line | no trace found |
| 111 | 2 (min) | skills/communicator/SKILL.md:98 (also PRODUCT_SPEC.md:737, skills/live-spec-base/SKILL.md:160, PRODUCT_SPEC.md:4994) | cadence minutes for a detached operation's start-and-recurring beat / worker heartbeat staleness | no trace found |
| 112 | 60 (sec) | skills/live-spec-base/SKILL.md:160 (also PRODUCT_SPEC.md:4992) | seconds interval for a worker's checkpoint heartbeat touch | no trace found |
| 113 | 1 | skills/live-spec-base/SKILL.md:195 | rows owed per landing commit in a tracking table | no trace found |
| 114 | 10 (landings) | skills/live-spec-base/SKILL.md:456 (also PRODUCT_SPEC.md:3029) | cadence: a full audit runs every N landings since the last one | no trace found |
| 115 | 2 | skills/product-prover/SKILL.md:106 | max header levels (H2/H3) in prover output | no trace found |
| 116 | 30 (sec) | skills/product-prover/SKILL.md:116,451 | target: prover notes scannable in 30 seconds / opening framed as the first 30 seconds of a review | no trace found |
| 117 | 5 (min) | skills/product-prover/SKILL.md:116 | target: prover notes readable carefully in 5 minutes | no trace found |
| 118 | 10-15 (sec) | skills/product-prover/SKILL.md:120 | target: each finding scanned in 10-15 seconds | no trace found |
| 119 | 3 (of 4) | skills/product-prover/SKILL.md:134 | min required elements named for a valid operational consequence | no trace found |
| 120 | 3 / 4 | skills/product-prover/SKILL.md:250-251 | entity/state count above which a diagram is warranted | no trace found |
| 121 | 2-4 / 2-3 | skills/product-prover/SKILL.md:443-444 | observation / clarifying-question counts for a NEEDS_CLARIFICATION verdict | no trace found |
| 122 | 1-2 / 1-2 | skills/product-prover/SKILL.md:455-456 | count of biggest-things-working / needing-attention listed in the opening assessment | no trace found |
| 123 | 5-8 (sentences) | skills/product-prover/SKILL.md:459 | cap on the opening assessment's length | no trace found |
| 124 | 3 | skills/product-prover/SKILL.md:765 | questions required before the class-lens hunt writes a finding | no trace found |
| 125 | 3 | skills/product-prover/SKILL.md:938 | top-N things to fix listed in the closing summary | no trace found |
| 126 | 2 | skills/product-prover/SKILL.md:940 | example count given for properties to state, in the closing summary | no trace found |
| 127 | 5 | skills/product-prover/SKILL.md:945 | oldest N [default]-tagged sentences a FULL pass lists | no trace found |
| 128 | 3 | skills/spec-author/SKILL.md:154 | count of parallel facts that must become a list | no trace found |
| 129 | 2-3 (sentences) | skills/spec-author/SKILL.md:167 | length of the spec preamble's coverage statement | no trace found |
| 130 | 3-5 (lines) | skills/spec-author/SKILL.md:182 | cap on a layer-overview map | no trace found |
| 131 | 1 | skills/test-author/SKILL.md:35 | min rendered-level rows owed per artifact-inventory file | no trace found |
| 132 | 1 | skills/test-author/SKILL.md:105 | min interface-level rows owed per module block | no trace found |
| 133 | 10 | skills/text-audit/SKILL.md:194 | requirements audited per batch in a spec-section read | no trace found |
| 134 | 2 | skills/design-reviewer/SKILL.md:169 | duplicate home of #19 (node-per-file default cap) | see #19 |

## PRODUCT_SPEC.md (standards not already cross-referenced above)

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 135 | 3 | PRODUCT_SPEC.md:1702 | default cap on progressing rounds in the prover/design-review loop before it surfaces unsettled groupings | no trace found |
| 136 | 1 | PRODUCT_SPEC.md:3634 | max features parked per lane when a bug preempts rolling work | no trace found |
| 137 | 2 | PRODUCT_SPEC.md:4709 | max times one question may cross between the same two agents before it escalates to the owner | no trace found |
| 138 | 2 | PRODUCT_SPEC.md:5310 | mid-turn count at which a broken standing behavioral rule earns a live enforcement channel | no trace found |
| 139 | 5 (sec) | PRODUCT_SPEC.md:7781 | seconds within which a work-board update must complete after the stage change it records | no trace found |
| 140 | 5 (sec) | PRODUCT_SPEC.md:7794 | seconds cadence at which an open work-board page re-reads itself | no trace found |
| 141 | 1 (hour) | PRODUCT_SPEC.md:6064 | duplicate of #77 (lock-age threshold, stated in hours) | see #77 |

## README.md, guardrails/README.md, docs/

| # | Number | file:line | Governs | Provenance lead |
|---|---|---|---|---|
| 142 | 3.9 | README.md:37 | minimum Python version the guardrail checks require | no trace found (plausibly a tooling constraint, not a chosen "standard") |
| 143 | 3 | README.md:64 | corroborating signals required before a dead session's background worker is treated as stopped | no trace found |
| 144 | 470 (sec) | ARCHITECTURE.md:880 (guardrails/check-suite-budget.sh reads this row) | ceiling on the full test suite's wall-time, re-measured at every gate landing | derived and justified — journal 2026-07-16 (row 361, INV-41/INV-164): watcher mechanism named `check-suite-budget.sh` reads this row against the measured run and reds on drift; the row itself is explicitly re-set to the fresh measured figure at every full-prover pass (60 -> 180 -> 360 -> 470 across landings). DECISIONS.md ~01:10 calls an earlier 360-second figure "invented" and drops it as a fixed target — the current 470 s row is the self-correcting descendant of that same lineage, so the *mechanism* is derived/justified while the specific number is a moving measurement, not a chosen standard |

## Count

**144 distinct numeric standards found** across guardrails/*.py+*.sh (21), guardrails/*.json (33, rows 22-54), tests/ additions (6), scripts/ (19), hooks/ (6), templates/ (8), skills/ (41), PRODUCT_SPEC.md-only (7), and README/docs (3).

## Standards whose provenance lead says "no trace found" (likeliest process-invented)

The large majority — well over 100 of the 144 rows above are tagged "no trace found." The handful with
a positive lead are: #44 (2 consecutive clean reads — his word), #60 (lane cap 3 — his word), #19/#20
(node-file-cap — session-derived from measurement, cited), #25/#27/#29/#31/#33 (criterion-readability
grandfathered baselines — session-measured, cited), #52 (spec-debt-cap ratchet — session-derived,
self-documented with its own justification note), #53 (register-lint floor — tied to INV-83/row 217 but
not to a word of his), #69 (legibility floor — plausibly WCAG-derived but uncited in the tree), and #144
(suite wall-time budget — mechanism is derived/measured, watched by a real gate).

Everything else — roughly 130 rows — returned nothing in DECISIONS.md, JOURNAL.md, or
docs/queue-archive/ tying the specific number to either Alexander's word or a stated derivation. This
includes entire families that read as arbitrary process invention on their face: every word/character/
byte cap in guardrails/language-rules.json and guardrails/criterion-readability.json beyond the cited
baselines (25-word, 35-word, 12-char, 25-char, 60-word, 550-char, 220-char, 450-char, 45-char caps); the
four PRODUCT_SPEC.md/ROADMAP.md/TEST_MATRIX.md/JOURNAL.md byte ceilings in guardrails/doc-bounds.json
(840,000 / 700,000 / 530,000 / 640,000 — squarely the size-cap class his ~01:10 word rejected); the
spec-ratchet.json bytes-per-criterion figure (207.2); every timeout in scripts/ and hooks/ (10s, 30s,
40s, 45s, 80s, 120s, 25s curl/subprocess/model-call timeouts); every retry/leak-warning count in
templates/headless_harness.py (20s, 60s, 100 retries, 50 leaked dirs, 3600s); and nearly the entire set
of skill-prose numbers in product-prover, build-pipeline, spec-author, and test-author SKILL.md files
(scan-in-N-seconds targets, N-question checklists, N-sentence caps, N-day recurrence windows) — none of
which trace to a cited exchange or a stated derivation anywhere in the tree's own record.
