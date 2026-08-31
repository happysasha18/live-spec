# Prover record — 2026-08-31 three lanes land, and an adversarial read refuses them

PUSH-REVIEW

Range: 6cbec19d..6d0e8738
- 6d0e8738 The new criteria follow the spec's own register
- 1223b3f4 An adversarial read refused the merged range; nine findings are repaired
- 2ce57aab The board's own text follows the honest re-measurement
- 592a831f Land q-497: the assistant never puts words in your mouth
- 34619279 Land q-527: a cleared mistake stops blocking every future push
- 5a84924e Land plan-2: the director's thirty-five traces are re-recorded honestly
- 1d024593 An adversarial read refused the first build of the named arm; the holes are closed
- 98f3c8a2 Prover record: a cleared mistake stops blocking every future push
- 0350fb79 Director eval: a full re-record of all 35, and the rule that it is always all 35
- b3c47f42 Director eval: observation-carrying-its-repair stops arguing against itself
- 248cdb5b Director eval: an extra act is reported, and a missing one still fails
- b09a6c01 q-527 closes: the definition is written and the way out is proved
- 45a50927 The architecture pins follow rule 13's new paragraph down the file
- 71ab9bb1 q-497 lands: the row and the resume file record what reds where
- 4420abb1 An instruction's authority and how a conflict over it is spoken get one home
- 37ebdd07 The way out is proved in both directions over one fixture
- ee5c6933 A finding the tree shows made good stops blocking every future push
- a4cb80d1 The authority gate reaches every text page the project tracks

Files read: PRODUCT_SPEC.md, ARCHITECTURE.md, spec/guardrails-freshness.md (Requirement 301),
architecture/rules-and-settings.md, skills/live-spec-base/SKILL.md (rule 13),
evals/director/check.py, evals/director/README.md, evals/director/scenarios.json,
guardrails/check-worker-restore.py, guardrails/check-authority-anchor.py,
guardrails/authority-anchor.json, guardrails/pre-push, guardrails/README.md,
guardrails/check-prover-record.sh, matrix/guardrails.md, PRODUCT_SPEC.index.md, TEST_MATRIX.md,
PLAN.md, NEXT_STEPS.md, tests/test_director_scenarios.py, tests/test_worker_restore_made_good.py,
tests/test_authority_anchor.py, tests/test_one_home_per_rule.py, scripts/state-probe.sh,
scripts/plan_checks.py, scripts/sync-skills.sh

Checks run: python3 -m pytest -q — 2630 passed, 4 skipped, 0 failed (the merged tree, before the
repairs below) · python3 -m pytest -q — the full suite re-run alone after every repair, result on
the closing line of this record · python3 -m pytest tests/test_worker_restore_made_good.py
tests/test_worker_restore.py tests/test_worker_restore_run_scope.py -q — 142 passed ·
python3 -m pytest tests/test_authority_anchor.py -q — 31 passed · python3 -m pytest
tests/test_director_scenarios.py -q — 15 passed · python3 evals/director/check.py --all — 34 of 35
· python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md — 404 of 404 ·
bash scripts/sync-skills.sh — live-spec-base resynced · python3 -m pytest
tests/test_config_health.py -q — 34 passed · bash guardrails/pre-push — verdict on the closing line

Findings: an independent read with clean context was briefed to find reasons to refuse this push and
held it defective. It returned nine blocking findings. Every one was real, and every one is repaired
in 1223b3f4 rather than argued away. The two that mattered most were both a check that had been
loosened rather than corrected — the highest-priority class, and it was present in two of the three
lanes.

1. The director grader forgave an extra act everywhere, including on a scenario whose expectation is
   that the turn carries no act at all. Reproduced against the shipped grader: a thank-you graded as
   producing an instruction returned zero failures. That is the one thing the case exists to catch.
   The justification had also over-read its own source — the skill prices splitting one real act in
   two, while inventing an act on a turn that carried none is a separate rule with its own section.
   Repaired: an extra act is a note where some act was expected, and a failure against an expectation
   of none.
2. The number carrying that change was wrong by three times. "Six of the nine reds" was published in
   three places; re-derived twice and independently against that run's own recorded traces, the true
   number is two. Repaired in all three.
3. The score published as 34 was set beside a 26 read by a different grader. The same traces score 30
   on the old grader, so four scenarios are real movement and the rest is the corrected cost model.
   Both readings are now stated on the row.
4. The compensating visibility never reached the surface the score is read on: the note count printed
   one line above the pass line, and both readers of that score take the last line alone. Repaired by
   moving the count onto the score line, keeping the "N of M" opening the plan check greps.
5. The way out for a cleared worker-restore finding counted a glob pathspec as a named file, so
   `git checkout -- '*'` — which discards the whole working tree — was cleared by one unrelated
   commit. Repaired: a path carrying a glob character or git's pathspec-magic prefix is refused, and
   the remaining path must name exactly one tracked file by git's own answer.
6. The same arm asked the filesystem whether a path was a directory, which is a present-tense answer
   to a question about the past, so a directory already deleted passed. The same git-side check
   answers it.
7. A later commit that only deletes the named path counted as restoring it. Repaired by requiring the
   file to sit in the repository's HEAD now.
8. `git commit --amend` and a rebase cleared a finding with no repair at all, because the arm read the
   committer date, which both reset. Repaired by reading the author date, which both preserve. A
   hand-set author date is a bound no repository fact can close, and the requirement now names it
   instead of implying it is closed.
9. The new attribution block reddened sentences that carry their date correctly, because the sentence
   splitter breaks on a colon and severed a leading date stamp from the claim it dates — the form the
   read-back page writes its own entries in. The next live page to write a dated attribution would
   have blocked the push. Repaired: the tree-wide arm takes a real date anywhere on the line.

Beyond those, six architecture pins had drifted two lines at the merge and pointed at the wrong rule;
three matcher measurements in a shipped docstring reproduced at neither the published nor the
reviewed figure and were re-derived with their method written beside them; the spared-set counts had
been moved by this push's own new files. All corrected.

Two claims the read made were checked and did not hold as stated. It reported the made-good arm as
wired to no push at all; the census arm is indeed absent from this repository's own `pre-push`, but a
host project calls this same script from its gate, which is how a stray command in this tree blocked
a neighbour's push three times in August, so the motivation stands and only this repo's own wiring is
absent. It also reported three matcher counts that a third derivation did not reproduce either; the
numbers now shipped are the ones whose method is written down, and the disagreement between three
readings of one docstring measurement is recorded here as a soft spot rather than settled.

Deliberately not closed, each named where a reader will meet it: the eval's one real disagreement,
`idea-for-another-project`, where the skill and the fixture differ on all three material fields;
a year-less date and a denial, both of which the attribution block still reds, each costing a writer
one edit and neither letting a fabrication through; and the hand-set author date above.

Blocking: none — the nine blocking findings the read returned are all closed.
- the director grader forgave an act on a zero-act expectation — closed: fails there, notes elsewhere, test added
- "six of the nine reds" was two — closed: re-derived twice, corrected in all three homes
- 34 was set beside a 26 from another grader — closed: both readings stated on the row
- the note count never reached the score readers — closed: moved onto the score line
- a glob pathspec counted as a named file — closed: refused, and git confirms the single file
- a deleted directory passed the filesystem check — closed: answered by git rather than the disk
- a deleting commit counted as a repair — closed: the file must sit in HEAD now
- an amended commit cleared a finding — closed: author date replaces committer date
- the attribution block reddened correctly dated sentences — closed: the whole line carries the anchor
