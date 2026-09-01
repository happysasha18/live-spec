# Prover record — 2026-09-01, three targets reopened (q-385, q-804, q-436) and criterion 15 narrowed

PUSH-REVIEW

Range: 11987b8..5c8ebb8
- 5c8ebb87 Fix shipped-language gate: allowlist plan_checks.py's real grep string, mark PLAN.md's direct quotes user-language
- 7c25768c plan_checks.py: back five done tasks, and drop pytest from q-802's key
- 0a9a431a PLAN.md: three findings from tonight's traceability/done-mark audit
- 084c3eb4 communicator's body drops back under its size ideal, q-536's rulings moved to references
- 16878f0c Cut the scissors contrast frame from q-398's new referral criterion
- 476f5246 Fix INV-196 trailing-tag order so its declaration paragraph is found
- 0d668348 config-health: routing hook installed, communicator's copy re-synced
- 4c95f679 NEXT_STEPS.md: name the real date behind plan-9's "Alexander's own word" deferral
- 7551744b docs/language-rule-coverage.md: rebuild off hooks/register_judge_core.py's source note
- fc5c2792 PRODUCT_SPEC.index.md: rebuild the generated code-to-location table off today's spec edits
- ce3a7e30 spec: Requirement 163's heading loses a stray [default] tag it never should have carried
- 6ea75939 architecture pins: re-point nine line pins that drifted when today's session edited skills/live-spec-base/SKILL.md and skills/communicator/SKILL.md
- 97799c24 NEXT_STEPS.md: full suite is red, 30 failures -- state it honestly
- 29faa996 NEXT_STEPS.md: re-heal two commits whose heal phrase wrapped across a line
- d35dc003 README rewritten short, product-prover's shape: what you get, then how, install last
- b1f0963c NEXT_STEPS.md catches up with today's full landing range
- 67bd98d1 q-386's convergence test lands
- 1280cd99 q-536's fourteen rulings land for real
- 287e019c q-163's M-620 matrix row lands for real
- 67f9ce6e q-802 lands: the snapshot's baseline only ever moves for what a delivery actually declared
- caa7f6a7 Old leftovers actually confirmed dead, not just old, are cut
- adceb60b q-166: board.html already answers the daily ask he remembered
- cf244b5b The false Known Issue claim gets a guard against a fourth return, not a fourth manual fix
- e3b745b1 q-501 / the front page's own false Known Issue closes, again
- 54bde341 Revert TEST_MATRIX.index.md, matrix/test-author.md, skills/communicator/SKILL.md from the q-398 commit
- e2a0e8c4 q-398 lands: a routing preamble now reaches an adopted project automatically
- 2858c023 q-800: close the playbook-repo row now that his permission this session is the read that was waited on
- c30491b9 q-48: the deferred trigger already fired 24.07 -- the row catches up
- 8905d7af q-536 lands: the fourteen communicator collisions each get their ruling, in the rule's own text
- 24152152 q-163: the wiring proves itself; the host field-leg still needs its own project's window
- 4f86dfd9 q-591 lands: M-313's cited home follows the requirement that actually moved
- d673c75c q-166 re-marked queued, not needs-his-eyes -- nothing built yet to look at
- 3147d6e2 Journal: plan-2 re-recorded, q-437 lands, sync catches up
- 14808ef2 plan-2 re-recorded: all thirty-five traces fresh, 32 of 35 hold
- 7e3f32e1 q-437 lands: the axis-verdict sweep runs at every level, not just siblings
- b9708261 plan-10 lands: every done mark now proves itself, none turned out false
- a488854f plan-10: sixteen done marks now carry a real check or a dated reading, not a typed mark
- bf319751 plan-10's own instrument: a done mark now has to prove itself
- 3d4b8ae4 q-803: a skill's rule states itself, the journal carries who said it
- 5aacf3aa Concurrency without a stated safety measure gets its own rule
- 62394f45 q-576 lands: the page it asked for exists, and the tree holds nothing ungrounded
- c8adff22 q-576: the twelve unlabelled survivors and one new constant get the same source-admission every other unproven number already carries; r14's stale note is corrected

Files read: spec/design-spec-review.md (criterion 15, narrowed), tests/test_traceability.py
(TARGET_ROW_OWNERS re-pointing), PLAN.md (q-385, q-804, q-436 rows in full, plus the three
shipped-language spots this same range fixes), spec/doc-order-generated.md (Requirement 1
criterion 4), spec/internal-failure-log.md (Requirement 163's stray [default] tag),
spec/roles-and-agents.md (Requirement 196 criterion 7 tag order, criterion 21 new), PRODUCT_SPEC.md
and ARCHITECTURE.md (core files — confirmed untouched in this range; only their parts changed),
architecture/exchange.md, architecture/outward.md, architecture/pipeline-and-lanes.md,
architecture/rules-and-settings.md, .live-spec/r5-rule-prices-2026-08-11.md (the nine re-pointed
pins), hooks/routing-preamble-hook.sh, .live-spec/snapshot/baseline.py and MANIFEST.md,
.gitignore, guardrails/judge-hooks.json, scripts/install-session-hooks.sh,
skills/live-spec-base/SKILL.md (the new no-unprotected-concurrency bullet), skills/communicator/SKILL.md
and references/rule-histories.md, skills/product-prover-pack/SKILL.md (axis-verdict sweep lens),
skills/spec-author/references/facet-sweep.md, matrix/build-pipeline.md, matrix/test-author.md
(M-620's new row), scripts/plan_checks.py (157-line diff, incl. this range's own q-802 and q-800
key changes and this record's own plan_checks.py:32 allowlist fix), scripts/shipped-language-allowlist.json,
guardrails/check-prover-record.sh, guardrails/check-pin-drift.sh, guardrails/check-shipped-language.sh,
guardrails/check-doc-rotation.py, guardrails/check-landing-next-steps.py, guardrails/check-authority-anchor.py,
docs/prover/README.md (this record's own shape).

Checks run: (1) python3 -m pytest -q tests/test_traceability.py tests/test_plan_done_marks_are_backed.py
tests/test_tasks_parser_finds_every_task.py tests/test_composition_axes.py
tests/test_lane_open_act_convergence.py tests/test_readme_stance.py tests/test_routing_preamble_hook.py
tests/test_snapshot_baseline.py tests/test_compaction_discipline.py — 253 passed, 2 skipped; (2)
python3 -m pytest -q tests/test_board_matches_the_canon.py tests/test_one_home_per_rule.py
tests/test_plan_is_not_executable.py — 26 passed, 1 skipped; (3) python3 -m pytest -q
tests/test_architect_extraction.py tests/test_host_count_agrees.py
tests/test_minor_gate_reconciliations.py tests/test_no_self_certification.py — 18 passed (the
class of README-content test that caught product-prover's own dropped sentence this same session,
run here against the live-spec root README's own rewrite — clean); (4) python3 -m pytest -q
tests/test_formal_index.py tests/test_index_generated.py — 11 passed (confirms PRODUCT_SPEC.index.md's
rebuild is not stale); (5) bash guardrails/check-shipped-language.sh — OK, 0 offences; (6) python3
guardrails/check-doc-rotation.py — OK; (7) python3 guardrails/check-landing-next-steps.py — one
pre-existing error (0a9a431a closes plan-3 with no same-commit NEXT_STEPS.md touch) plus seven
already-healed WARNs, all citing their own healing commit — see Findings; (8) python3
guardrails/check-authority-anchor.py — OK, candidate NOTEs only, non-blocking; (9) bash
guardrails/check-pin-drift.sh — FAILS again, five ARCHITECTURE.md arms plus the r5 range-pin leg —
see Findings; (10) direct re-run of scripts/plan_checks.py's own "plan-0" and "q-802" shell
commands (not trusted from a commit message) — both exit 0 against the live tree; (11) manual diff
read of every file in the range's stat output against its own commit message's claim (git show on
each of the higher-risk commits: 0a9a431a, 6ea75939, 67f9ce6e, 5aacf3aa, e2a0e8c4, ce3a7e30,
476f5246) — each commit's message matches its actual diff, no silent scope creep found. Full-suite
run intentionally not repeated here: this session is mid-pipeline (steps 4 and 5 below still
pending, both of which touch files this same run would re-read), and the standing rule against a
second full-suite run while the tree is still moving applies; the full suite runs once, at the end
of this session's remaining steps, per this session's own brief.

Findings: three. None repaired here — two are already scheduled as this same session's next two
steps; one is disclosed and left as a judgment call.

1. **The gap this record exists to close: TestGateA_ProverRecord::test_real_repo_passes was red
   because the newest committed docs/prover/ record (62394f45) predated 0a9a431a, which reopened
   q-385/q-804/q-436 and narrowed criterion 15.** Read spec/design-spec-review.md and
   tests/test_traceability.py's TARGET_ROW_OWNERS directly rather than trusting 0a9a431a's own
   commit message: the narrowed criterion 15 text ("the value-space in-between forcing step
   promised as a later increment") matches PLAN.md's q-436 row word for word, and each of
   INV-185→q-385, INV-198/199/201→q-804, INV-244→q-436 in the map matches an open, substantive
   PLAN.md row (not a stub) carrying its own Source, Definition of done, and — for q-385 and
   q-436 — a Revisit trigger. Confirmed q-437 (INV-244's former owner) is genuinely closed:
   PLAN.md marks it ✅ with a "Done 2026-09-01" paragraph, and tests/test_composition_axes.py
   (the axis-verdict sweep q-437 built) passed clean above. **Closed by this record's own
   existence** — being fresh and committed is what the gate demands.

2. **Pin drift is broken again**, exactly as this session's brief expected: commit 084c3eb4
   (landing after 6ea75939's nine-pin re-point) trimmed skills/communicator/SKILL.md's body back
   under its size ideal, shifting lines again. `bash guardrails/check-pin-drift.sh` currently
   fails five ARCHITECTURE.md pins (four in architecture/exchange.md, one range pin in
   .live-spec/r5-rule-prices-2026-08-11.md) — same file, same class of drift 6ea75939 already
   fixed once tonight. **Not closed here — stands, by design:** this session's own next step (the
   brief's step 4) re-points these pins by their naming words against the file's current content,
   deliberately ordered after this record so the fix lands against settled content rather than
   content still moving. Recording it here rather than leaving it silent.

3. **NEXT_STEPS.md is stale against 0a9a431a, which closed plan-3 (the header-restoration finding)
   without a same-commit NEXT_STEPS.md refresh.** `python3 guardrails/check-landing-next-steps.py`
   reds this one as an error (INV-242); the other seven WARNs it prints are already healed forward
   by name (b1f0963c or 29faa996 cited in each), so they are not fresh debt. **Not closed here —
   stands, by design:** this session's own next step (the brief's step 5, run last) folds a note
   for plan-3's closure — plus this record's own arrival and the pin-drift refix — into
   NEXT_STEPS.md's LIVE STATE block in one pass, rather than a partial heal now that the pin-drift
   fix would immediately require touching again.

Blocking: two
- pin drift on ARCHITECTURE.md (finding 2): stands — fixed in this same session's very next step,
  ordered deliberately after this record so it lands against settled content.
- NEXT_STEPS.md stale against 0a9a431a (finding 3): stands — fixed in this same session's final
  step, folded in with the pin-drift heal and this record's own arrival in one pass.
