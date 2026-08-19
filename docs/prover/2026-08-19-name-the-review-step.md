# Prover record — 2026-08-19 name-the-review-step

PUSH-REVIEW

Range: 61d2a7ea..bb0aab5a
- bb0aab5a Reword the build-pipeline review's ran-tests line off the bare word 'publish'
- 3cc66d0d Skill-creator review records for the skill-review-step bullets in build-pipeline and publish
- ff9685fd Name the skill-creator review step where the pipeline lists its steps
Files read: skills/build-pipeline/SKILL.md, skills/publish/SKILL.md, tests/test_skill_review.py, guardrails/check-skill-review.sh, guardrails/rule-census.json, docs/skill-review/2026-08-19-build-pipeline.md, docs/skill-review/2026-08-19-publish.md, TEST_MATRIX.md (row M-303), ~/.claude/skills/skill-creator/SKILL.md
Checks run: `bash guardrails/check-skill-review.sh` — OK for both build-pipeline and publish, freshness re-verified after the cherry-pick changed both skill-edit and record commit hashes: the gate's own rule is ancestry (the record's commit is the skill-edit commit itself or a descendant of it), not a literal hash match, and cherry-picking in the original order (skill edit, then record) preserved that ancestry on this branch. `python3 -m pytest tests/ -q -k "skill_review or build_pipeline or publish"` — 51 passed, 2427 deselected. `git diff origin/main --stat` — six files, exactly the skill-review-step transfer (docs/skill-review/2026-08-19-{build-pipeline,publish}.md, guardrails/rule-census.json, skills/build-pipeline/SKILL.md, skills/publish/SKILL.md, tests/test_skill_review.py); nothing else crossed onto this branch.
Findings: (1) The skill-creator review is an already-live law (gate s, guardrails/check-skill-review.sh, SPEC INV-208); this delivery only named it where a reader scans for "what does this pipeline require" — one bullet in build-pipeline's "Gates worth remembering" list, one clause on publish's existing `skill` row. (2) That one-line addition to each skill counted as a substantive body change under gate s's own rule, so the gate reds the first real push of this branch's ancestor commit until a review record existed — the law working as designed on itself. A real skill-creator review followed for both (reading ~/.claude/skills/skill-creator/SKILL.md for method, then applying it to the actual changed and surrounding text), found both additions accurate against the real gate, directory and TEST_MATRIX row, and non-contradictory with a neighboring rule (build-pipeline already names a different, older duty under INV-99; TEST_MATRIX row M-303 already documents INV-99 and INV-208 as deliberately distinct) — no defect in either skill, both verdicts ALLOW. (3) The first version of build-pipeline's review record spelled the word "publish" once inside a quoted pytest -k filter; guardrails/check-skill-review.sh's own matching is a literal grep -qw scan, so that token let the gate accept build-pipeline's record as a match for publish's requirement too (alphabetically first), rather than each skill resolving to its own dedicated record. Reworded off the bare token and reverified: each skill now resolves only to its own record. (4) This branch was cherry-picked from cull/2026-08-19-invented-numbers, which carried this work bundled with an unrelated invented-numbers cull; that cull already landed on origin/main (61d2a7ea) through a separate branch, so only these three commits were picked here, in their original relative order, confirmed carrying nothing else via `git diff origin/main --stat`.
Blocking: none

Root: origin/main (61d2a7ea) already carries this session's other work — the criterion-readability
cull and the editions/product-prover mirror retirement — landed through cull/2026-08-19-part-a. The
one piece still outstanding was this: naming the already-live skill-creator-review gate in the two
skills whose pipeline listings a reader actually scans. Rebuilt clean on top of the current main
rather than merged from the old combined branch, since the same content already exists there
through the transplant and a merge would fight itself over identical diffs.

The push this record covers will still need one manual step after it lands: refreshing the two
skills' installed copies under `~/.claude/skills/build-pipeline` and `~/.claude/skills/publish`,
which `scripts/sync-skills.sh` writes and which no session runs without the owner's word. That step
is expected and outside this record's scope, per the coordinator's own word.
