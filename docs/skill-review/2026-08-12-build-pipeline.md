# Skill review — build-pipeline (the cut rule's restatement removed from the gates section)

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author
the edit, and it wrote no file but this record.

Verdict: passes as a skill, with one recommendation the reviewer would carry before the next release.
The description is untouched and still describes the body, the edited paragraph reads whole, and no
reference to the cut rule survives anywhere in the skill. The recommendation concerns what the
paragraph no longer says, and a test that no longer reaches what its name promises.

## What changed

Commit `3866a6c` removed three lines from the gates section of `skills/build-pipeline/SKILL.md`: the
restatement of base rule 30, which said any machine-verifiable quality ships as a runnable gate held
by no pass's attention. The compaction bullet keeps its INV-164 title and its compaction half. The
terms paragraph at line 73, which tells a reader what a base rule N points at, moved from thirty-five
to thirty-four.

## Findings

1. **The bullet keeps half of what its invariant now says.** Recommended, one sentence. INV-164 today
   carries two clauses: compaction runs at every push, and a check is opened from a second dated break
   or the owner's word, never from the property being checkable. Only the first reaches this file.
   `TEST_MATRIX.md` row M-313 names the gates section of build-pipeline among INV-164's homes and
   states the second clause in its never-list, so the matrix's home claim is now wider than the file.
   Two closes are honest: drop build-pipeline from that leg's home list, or return one sentence. The
   reviewer recommends the sentence, because this file is where a seat stands when it decides whether
   a new gate is owed, and the rulebook no longer answers that question either.

2. **The one mechanical hold on this home does not reach it.** Recommended.
   `test_build_pipeline_carries_compaction_every_pass` asserts only that the string INV-164 appears
   somewhere in the file. Its name and its docstring promise that compaction is baked in as a station
   run every pass. Today the file carries INV-164 exactly once, in the bullet, so the assertion binds
   that line by accident of scarcity. Delete the bullet and add the code in any comment and the test
   stays green. An assertion on the bullet's own sentence would hold what the name claims.

3. **The paragraph reads whole after the removal.** Reviewed and clear. It now runs from compaction at
   every push, through the three mechanical gates that hold the reached-clean floor, to the 2026-07-15
   bloat it fixes. Nothing in it depends on the removed lines, and the removal took the paragraph's
   only over-cap sentence with it: the census reads this file at 135 sentences past the word cap
   against 136 before.

4. **The line wrap was not re-flowed.** Cosmetic, and this edit made it. Lines 545 and 546 run 97 and
   76 characters against roughly 103 through the rest of the paragraph, and the article splits from
   its noun across the break. A re-flow fits the words on the line above without crossing the norm.

5. **The rule count is restated here, and no machine holds the copy.** Recommended for the pack, not
   for this file alone. The count of the base rulebook's rules lives in four places: the base's own
   frontmatter, this file's line 73, and two lines in communicator. Only the first is asserted, by
   `test_base_description_counts_the_rule`, which derives the number from the body, and by two literal
   assertions in `test_clean_context_review.py` and `test_resume_rederive.py`. A grep of `tests/` and
   `guardrails/` finds nothing reading the copy in this file. One cut number therefore cost four edits,
   and the next rule change will cost them again with three of the four free to drift. Base rule 4 —
   one canonical home per fact, everything else a pointer — points at the fix: let this sentence point
   at the rulebook instead of counting it.

6. **No dangling reference to the cut rule.** Reviewed and clear. A grep across `SKILL.md` and the
   eight files under `references/` for the cut rule's number, for thirty-five, for INV-164 and for the
   generator wording returns one hit: the legitimate INV-164 citation in the compaction bullet, whose
   invariant survives with a rewritten meaning.

## The measures this review was held to

The census reads `skills/build-pipeline/SKILL.md` at 255 findings after the edit — 135 sentences past
the word cap, 120 style findings, no register findings — against 256 before, the difference being the
removed sentence. The file measures 64,007 bytes against 64,220. The loadability gate passes. The
tests covering INV-164 and the rule count pass, 36 of 36 across the four files the commit touched. The
installed copy at `~/.claude/skills/build-pipeline` is byte-identical to the repository copy.
