# Prover record — 2026-08-26 director-cutover-architecture-catchup

PUSH-REVIEW

Range: a42c6fd2..a0da72b2 (39 commits from `origin/main`; 37 reviewed — 2 merge commits,
a716fb52 and 12e70348, carry no diff of their own and are named for completeness only). No
prior committed record covers this full range back to `origin/main`; every 2026-08-25/26
record on file names only a partial delta since some earlier point, which is why gate a
(`guardrails/check-prover-record.sh`) has stood red all evening per PLAN.md's own
§Блокеры note — this record closes that gap in full, not by widening a partial one.

- a0da72b2 Fix 5 real regressions the rule-cutover's fallout sweep missed (adversarial pass)
- 88d42577 Add the missing test for director's four term definitions (gate h)
- 3dcf7b82 Bump VERSION to 6.0.0 and add the MIGRATION.md chapter for the director cutover
- 7e3188e8 PLAN.md: step 8 in work
- 59bc66cc Retire step-7 fallout: prose-lock tests for the 13 attic'd rules
- e043a6b4 PLAN.md: step 7 status, before/after recorded
- 0ae778bc PLAN.md step 7: cut 13 unbacked rules out of live-spec-base's mandatory context
- 630a61cc PLAN.md: step 7 in work
- ce97c11d PLAN.md: step 4 status, two flags for his read
- 9b23940a Converge seat/senior/orchestrator/lead to one word, per PLAN.md step 4
- 4d5360df PLAN.md: probe's step-2 check is too loose, law 10 finding
- 18777bec PLAN.md: step 4 in work
- 60cc6704 Fix E-19 regression: director's eval outgrew the flat-file shape
- 12e70348 Merge step 6 (no diff of its own)
- c3be01a3 PLAN step 6: remove proven-dead phrase tests and vacuous file-exists tests
- 613eec82 PLAN.md: step 3 status, garbage list and PROBLEMS.md rows await his read
- a716fb52 Merge step 3 (no diff of its own)
- 96652793 PLAN.md: real push attempt run, five gates named precisely
- cb9b3a4d Append this month's crisis-diagnosis findings to .live-spec/PROBLEMS.md
- 55c28708 PLAN.md: step 5 landed durably, two of his words still needed
- b0fcc12f PLAN.md: step 2 in work, honest score recorded in Блокеры
- 8c09de3d Copy this project's Claude Code session transcripts into attic/transcripts/
- 70a3d360 Director eval: regenerate all 35 traces against today's skill
- 402d6005 Director eval: fix three fixtures, tighten check.py's act grading
- 5db30805 Director: define decision, grounds, halt and correction
- d69bf796 Retire evals/director.md, the dead duplicate of evals/director/
- 0093cd9e Step 1's board renders the plan's own Canon, and its ticket fields trace to his words
- 3245cb9a The board is a kanban, and its ticket fields were already specified
- 2c7a3fb3 Ten commits stop living in one copy
- 4945b5ec The plan carries the goal it serves, and says it is the only one
- 062f17d0 The next-step line and the step list disagreed on one screen
- 339087cc The gate stays blunt until the Director is measured
- b3f1008f Three more checks were green over work that had not happened
- 256d60c8 The measurement refuted the case for cutting the phrase tests
- 6249f2d5 A cold reader found the entry point by luck, and two alarms watched the wrong thing
- c3284c8e Step zero's check was passing on work it had not done
- 1482c6a5 The plan's step status is measured, and drift has a way back
- 0fd08f22 The plan carries the owner's own report format and the root-naming law
- 8f69a7c8 Foundation: the project comes home, and its state is computed instead of written

Files read: PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, ARCHITECTURE.md,
`architecture/pipeline-and-lanes.md`, `architecture/rules-and-settings.md` (both in full, spot-
checked line by line against the live files their pins name — see Findings), `MIGRATION.md`
(the 5.0.0 chapter and the new 6.0.0 chapter), `VERSION`, `README.md`,
`skills/director/SKILL.md`, `skills/build-pipeline/SKILL.md`, `skills/architect/SKILL.md`,
`skills/live-spec-base/SKILL.md`, `skills/live-spec-base/references/session-handover.md`,
`attic/live-spec-base-unbacked-rules-2026-08-26.md`, `attic/MANIFEST.md`,
`guardrails/pre-push`, `guardrails/check-prover-record.sh`,
`scaffold/guardrails/check_tests_present.py`, `docs/prover/README.md` and its four most recent
2026-08-26 records, `tests/test_class_hunt.py`, `tests/test_live_channel_law.py`,
`tests/test_minor_gate_reconciliations.py`, `tests/test_opening_decision_sweep.py`,
`tests/test_architect_extraction.py`, `tests/test_director_term_definitions.py`.

Checks run: `bash guardrails/check-pin-drift.sh` — OK, 174 pins (56 line pins within tolerance,
112 file-level, 6 unlabelled), plus the r5 range-pin set — green both before and after this
range's own edits. `python3 scaffold/guardrails/check_tests_present.py --base origin/main`
(gate h) — OK, 14 user-facing changes travel with 63 test changes. `python3 -m pytest tests/ -q`
run in full before any fix in this range's own commits: 2,242 passed, 8 failed, 52 skipped.
After the fixes in a0da72b2, the same 8 targets plus their siblings
(`test_architect_extraction.py`, `test_config_health.py`, `test_language_rules.py`,
`test_minor_gate_reconciliations.py`, `test_opening_decision_sweep.py`,
`test_live_channel_law.py`, `test_class_hunt.py`, `test_traceability.py`,
`test_director_scenarios.py`, `test_director_term_definitions.py`) re-run together: 286 passed,
4 failed (the pre-existing class named below), 4 skipped. A full `pytest tests/ -q` re-run was
attempted a second time to re-confirm the whole-suite count post-fix; it did not finish cleanly
in this environment (the local-hang gotcha several 2026-08-26 records already name, "CI-only");
the targeted re-run above is the scoped local equivalent, covering every file this range's own
commits or this record's fixes touch.

Findings: Adversarial re-read of the rule-renumbering and pin-shift fallout from PLAN.md step 7
(commits 0ae778bc, cutting 13 base rules with no eval fixture or executable script behind them
to `attic/live-spec-base-unbacked-rules-2026-08-26.md`; 59bc66cc, an 8-file fallout sweep
repointing tests that had asserted the cut rules' text against `skills/live-spec-base/SKILL.md`
directly) plus PLAN.md step 2's director term-definition addition (5db30805) and this record's
own VERSION/MIGRATION and gate-h work.

Pin accuracy (architecture/pipeline-and-lanes.md, architecture/rules-and-settings.md): spot-
checked every pin 5db30805 and 0ae778bc touched or that sits beside a touched one, by reading
the named line of the live file directly rather than trusting the commit diff — `director/
SKILL.md:227` (Execution heading, moved from :210), `live-spec-base/SKILL.md:104/122/149/213/
229/283/291/317/390` (rules 6/7/7-sub/16/22/26/27/31, settings-ladder pointer), `build-pipeline/
SKILL.md:21/45`, `architect/SKILL.md:144`, `director/references/delegation-protocol.md:71`,
`live-spec-base/SKILL.md:128/154` (lanes sub-rule, one-row-per-landing). Every one resolves
exactly, no drift found — consistent with `check-pin-drift.sh`'s own green. Also checked the
architecture note's claim that the 13 attic'd rules' formal SPEC anchors (INV-23, INV-65,
INV-84, INV-108, INV-145, INV-217, INV-237, INV-247, INV-302) "stay owned" though their
informal SKILL.md restatement moved: confirmed each still resolves in `PRODUCT_SPEC.index.md`
against real requirement rows — true as stated, nothing silently dropped from the spec itself.

Real regressions found and fixed (commit a0da72b2, detailed in that commit's own message):
five tests asserted content that the rule cutover legitimately moved out of
`skills/live-spec-base/SKILL.md`'s body, and the 8-file fallout sweep missed them —
`test_live_channel_law.py` (base rule 23, RED before the fix), `test_minor_gate_
reconciliations.py` (base rule 28, RED before the fix), `test_opening_decision_sweep.py` (base
rule 35's mechanism, which in fact always lived in `references/session-handover.md` rather than
the cut rule's own body — the test read too narrow a surface), `test_architect_extraction.py`
(a version literal this session's own VERSION bump broke — the exact vacuous-pin class this
same file's sibling test already warns against by name), and `README.md`'s stale "thirty-four
shared rules" line (the actual count fell to 21 with the cut; the number is now correct and the
matching test's README-mirror assertion passes).

Pre-existing, non-blocking, out-of-scope class found and left alone: a full local `pytest
tests/ -q` surfaces four more failures, all one class the project's own memory already names
("installed-side untested") plus one unrelated stale pin, neither touched by this range's
commits nor within this record's ARCHITECTURE.md-adjacent scope: `test_config_health.py`'s two
assertions that the machine's installed `~/.claude/skills/` copy matches the repo source (it
lags — still frontmatter `version: 5.0.0`, last synced before tonight's work; fixing it means
running `scripts/sync-skills.sh` against a SHARED machine directory every live-spec worktree on
this machine reads, which this record's own MIGRATION.md 6.0.0 chapter already names as the
correct action, but at real install/catch-up time, not from an unmerged worktree branch ahead
of the owner's push), and `test_language_rules.py`'s two assertions sharing one root cause
(`guardrails/language-rules.json`'s r18 rule has named `~/.claude/skills/live-spec-base/
SKILL.md:528` as a source pin since 2026-07-28 — `git log -S` confirms the line predates
tonight's work by a month, and the file has shrunk past line 528 across several unrelated
sessions since; not this cutover's fault and not this record's scope to fix).

Blocking: none
