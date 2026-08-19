# Prover record — 2026-08-19 invented-numbers-out (part a)

PUSH-REVIEW

Range: 1b186298..7349e54f
- 7349e54f Re-baseline the size ratchet: Requirement 297 left leaner-than-average criteria
- 063a55df Sweep a rendered docs/MEASUREMENTS.html left over from an earlier session run
- 88644236 Pin the two new numbering gaps Requirement 297's retirement left; drop its standalone-release tests
- 5f7ac194 Close rows 618 and 619: both guarded a copy that no longer exists here
- 037e2329 Remove the dead editions/product-prover mirror and its unreachable skip
- 31d33754 Name the progress report's table-B row count as a display width
- e7b0565d Cut the criterion-readability word-and-anchor ceiling family
Files read: guardrails/check-criterion-readability.py, guardrails/criterion-readability.json, guardrails/language-rules.json, guardrails/rule-census.json, tests/test_criterion_readability.py, scripts/rank-criterion-defects.py, scripts/rule-census.py, scripts/gen-language-consumers.py, scripts/build-index.py, ARCHITECTURE.md, TEST_MATRIX.md, PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, ROADMAP.md, spec/doc-order-generated.md (including Requirement 280), spec/guardrails-freshness.md, docs/spec-format.md, docs/language-rules.md, docs/language-rule-coverage.md, docs/language-defects.md, docs/plans/2026-07-28-top-level-readability.md, scripts/progress-report.py, docs/PROGRESS.md, hooks/answer-first-scan.py (attic), hooks/answer-first-scan.json (attic), hooks/chat-law-hook.sh, DECISIONS.md, scripts/sync-mirrors.sh, editions/product-prover/ (deleted), tests/test_prover_adapter_contract.py, tests/test_mirror_editions.py, scripts/install-external-skills.sh, docs/roadmap-format.md, scripts/rotate-doc.py, docs/queue-archive/rotated-ROADMAP-2026-08.md, scripts/check-registry.json, docs/MEASUREMENTS.md, guardrails/spec-ratchet.json, guardrails/check-size-ratchet.py, scripts/sweep-rendered.py, attic/MANIFEST.md
Checks run: `python3 -m pytest tests/test_language_rules.py tests/test_declared_laws.py tests/test_index_generated.py tests/test_matrix_reference.py tests/test_architecture_pins.py -q` — 59 passed, 2 skipped. `python3 -m pytest tests/test_check_registry.py tests/test_convergence_locks.py tests/test_convergence_rule.py tests/test_doc_findings_bound.py tests/test_rule_census_prose_units.py tests/test_rule_census_ratchet.py tests/test_tree_counts.py tests/test_withdrawal_convergence.py -q` — 105 passed, 2 skipped. `python3 -m pytest tests/test_mirror_editions.py tests/test_doc_findings_bound.py tests/test_prover_adapter_contract.py tests/test_mirror_autosync.py tests/test_mirror_release_history.py tests/test_made_with_attribution.py tests/test_progress_report.py tests/test_rule_census_ratchet.py -q` — 93 passed, 1 skipped. `python3 guardrails/check-language-rules.py`, `python3 guardrails/check-doc-findings-bound.py`, `python3 guardrails/check-index-generated.py <spec parts> PRODUCT_SPEC.index.md`, `bash -n scripts/sync-mirrors.sh` — all OK/exit 0. `python3 -m pytest tests/test_formal_index.py tests/test_rendered_sweep.py tests/test_size_ratchet.py tests/test_progress_report.py -q` — 70 passed. `python3 -m pytest tests/test_language_rules.py tests/test_declared_laws.py tests/test_index_generated.py tests/test_matrix_reference.py tests/test_architecture_pins.py tests/test_check_registry.py tests/test_convergence_locks.py tests/test_doc_findings_bound.py tests/test_rule_census_prose_units.py tests/test_rule_census_ratchet.py tests/test_tree_counts.py tests/test_mirror_editions.py tests/test_prover_adapter_contract.py tests/test_mirror_autosync.py tests/test_mirror_release_history.py tests/test_made_with_attribution.py tests/test_progress_report.py tests/test_formal_index.py tests/test_rendered_sweep.py tests/test_size_ratchet.py tests/test_doc_rotation.py -q` re-run on this branch after the cherry-pick split — 304 passed, 3 skipped. `git diff origin/main --stat -- skills/` — empty, confirming no skills/ content crossed onto this branch. The full suite runs server-side, on the coordinator's word.
Findings: (1) the family this range cuts (r08's spec-body cap, r11's anchor thresholds, r35, r36, and the whole check-criterion-readability.py gate) rode the pytest suite with no push-gate letter and no entry in guardrails/gate-red-proofs.json or .github/workflows/gates.yml — confirmed absent before concluding no CI step needed removing, not assumed. (2) r08 and r11 in language-rules.json carried this family's thresholds bolted onto rules with other live catchers (r08 feeds scripts/rule-census.py and gate aa; r11 is held by code-anchor-scan.py and preshow-lint.py); the edit was surgical, not wholesale, verified by re-running gate aa and check-language-rules.py after. (3) spec/doc-order-generated.md and PRODUCT_SPEC.index.md are gate-x GENERATED output (guardrails/check-index-generated.py, scripts/build-index.py); a hand edit was caught red by the real gate and replaced with a real rebuild before landing. (4) two of this session's own added sentences (in language-rules.json's r08/r11 retirement notes) tripped gate aa's own word-cap census on the file they render into; both sentences were shortened and the gate re-run green. (5) spec/guardrails-freshness.md's R302.11 and ROADMAP row 520 cited the retired Requirement 297 by name; both now state their own rule instead of pointing at a home that no longer exists. (6) hooks/answer-first-scan.json does not exist — already retired 2026-08-11 on the owner's word (D8, DECISIONS.md, commit a829e8b0) after 3,095 runs and zero catches; no live file cites its 220/450/550-char figures. (7) docs/MEASUREMENTS.md is stale since 2026-08-05, predating this range, and stays so — an unrelated, unguarded pre-existing condition, deliberately not fixed here. Its stale render, docs/MEASUREMENTS.html, was a leftover of an earlier exploratory run and did need clearing (scripts/sweep-rendered.py to attic/); the source .md's own staleness stands as before. (8) Requirement 297's retirement left two new empty numbers in the code index (INV-287, INV-288); pinned in tests/test_formal_index.py::EXPECTED_GAPS with a reason, the same shape as yesterday's INV-234 precedent (commit d1353580). (9) Requirement 297's eighteen criteria ran shorter than the spec's own average line, so removing them raised bytes-per-criterion (185.5137 measured, above the 185.4 recorded bound) even as the document shrank; re-baselined to 185.6 with the reason recorded in guardrails/spec-ratchet.json, the same procedure the ratchet's history already used for its one prior raise; a stale "Requirement 4" citation (now Requirement 280) fixed in the same file and in guardrails/check-size-ratchet.py's docstring. (10) tests/test_product_prover_standalone_release.py's four tests (three collected, one silently skipping here via external_clone_or_skip) all pinned editions/product-prover/, removed whole alongside that directory; no orphaned helper file survives it. (11) A parallel package on origin/main (base 1b186298) added `${{ !cancelled() }}` to every CI gate step and loosened gate g's test; this range never touched .github/workflows/gates.yml (finding 1), so rebasing onto it carried no conflict. (12) This push was originally one combined package with a skill-review-step naming addition to skills/build-pipeline/SKILL.md and skills/publish/SKILL.md. Gate s (guardrails/check-skill-review.sh, SPEC INV-208) then reds the push on any substantive skill-body change with no fresh docs/skill-review/ record, which the naming addition was; a real review followed and both verdicts were ALLOW, but a SEPARATE gate then caught config-health drift between those two skills' newly-edited source and their installed ~/.claude copies, which no session may repair without the sleeping owner's word. Rather than hold every finding in this record hostage to that one unrelated gate, the package split: this branch (part-a) carries every commit that touches no file under skills/ — verified by `git diff origin/main --stat -- skills/` reading empty — and the skills/build-pipeline, skills/publish, tests/test_skill_review.py, and docs/skill-review/2026-08-19-*.md changes stay on cull/2026-08-19-invented-numbers, held for the owner's word on ~/.claude.
Blocking: none

Root: the brief named four independent invented-number cleanups plus a documentation gap, drawn
from an earlier census pass. Two of the four numeric items (the criterion-readability family, the
dead product-prover mirror) needed real surgery once opened; one (the answer-first thresholds) was
already closed by an earlier, unrelated ruling; one (report-row caps) was cosmetic once its larger
sibling (rank-criterion-defects.py) turned out to be dead code rather than a file to trim.

check-criterion-readability.py, criterion-readability.json, r35 and r36, tests/test_criterion_readability.py
and its four fixtures, and scripts/rank-criterion-defects.py are gone whole. r08 and r11 kept their
surviving surfaces and catchers; only the spec-body-specific thresholds, the retired script's
mentions, and one now-broken cross-reference in a shared reader-question index came out.
Requirement 297 (INV-287, INV-288), TEST_MATRIX rows M-464/M-474/M-475, and two glossary entries in
PRODUCT_SPEC.md that had no referent left went with it. Every generated consumer this touches —
docs/language-rules.md, docs/language-rule-coverage.md, docs/language-defects.md, one plans page,
PRODUCT_SPEC.index.md, guardrails/rule-census.json — was rebuilt by its own generator rather than
hand-edited, and each rebuild was verified against its own gate before the commit that carries it.

editions/product-prover/ (12 files) is gone with the case-statement skip in scripts/sync-mirrors.sh
that named it — that skip matched a folder name the tracked skills/*/ loop never produces, so it
never fired; a one-line comment stands in its place. tests/test_prover_adapter_contract.py pinned
the retired case-statement text directly and was rewritten to check for the explanatory sentence
instead, keeping the fact under test rather than the mechanism that used to carry it. The mirror
road itself — publish-source selection, release-history generation, and the tests around them —
was not touched, on the coordinator's explicit word to leave that decision for daylight.

ROADMAP rows 618 and 619 named editions/product-prover/SKILL.md in their own footprints — one
proposing to split it further, one proposing a drift guard against it — and both went stale the
moment the folder left, the same breed of drift a hand-kept list leaves behind a mechanical
deletion. Both rows declined (their subject is gone, not their idea rejected on its merits) and
rotated through the normal closing-commit path into this month's archive, each carrying the reason.

The coordinator's full-suite run named ten red against the combined package; of those, six were
this range's own drift to fix (a numbering gap, a dead test file, a leftover rendered page, a
ratchet re-baseline, plus the rows-618/619 closure) and are carried on this branch. Two of the
coordinator's own guesses about root cause were checked and did not hold before concluding: a
pin-drift red was transient EINTR inside check-pin-drift.sh's own subprocess, not a gate-count
mismatch (reproduced once, cleared twice on rerun, no code touched); and the remaining two red
(config-health) named installed-skill-copy drift in `~/.claude`, real but entirely about the two
skills this branch does not carry — see finding (12) for why and where they went instead. No red
weakened a test's shape or a check's reach; every fix either recorded a legitimate hole with its
reason (the two EXPECTED_GAPS entries, the ratchet's raised bound) or removed a test alongside the
exact thing it guarded (the standalone-release suite, alongside editions/product-prover/ itself).

tests/test_worker_restore.py is red on this machine, on other projects' state unrelated to this
range and confirmed silent on the server; not investigated further per the coordinator's standing
word on that specific test.
