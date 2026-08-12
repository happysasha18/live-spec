# Skill review — live-spec-base (rule 7 rewritten shorter, stage-2 batch 1)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author
the rewrite, it did not run the clean-context requirement check that preceded it, and it wrote no
file but this record.

Verdict: passes as a skill and is fit to stand. The description still agrees with the body, the rule
keeps its number and its eight sub-rules, every pinned literal survives, and nothing inside the skill
points at wording the rewrite removed. Three findings follow: one sentence to restore, one term to put
back, and one closing measure in the batch record whose scope needs naming. None blocks.

## What changed

Commit `56c9473` rewrote rule 7, the concurrent-edit fence, at `skills/live-spec-base/SKILL.md` lines
170 to 207. The rule's body falls from 5,477 to 5,171 bytes on the reviewer's own measure, three lines
shorter. The sub-rule on a worker never restoring a tree with a git command is held byte-for-byte, as
INV-299 requires of the wording that rides every brief. Long sentences were split, one pointer
sentence was dropped whole, and the lead-in above the sub-rule list came out. Eighteen architecture
line pins were reshifted to follow. No rule was added or removed, so the count stands at thirty-four.

## Findings

1. **The sub-rule list lost the sentence that said what it is.** Recommended repair, one line. The old
   text introduced the eight bullets with a lead-in naming them the parallel-lanes rules that sit
   underneath the fence. The bullets now hang directly off the fence paragraph's closing code list. A
   requirement check reads this as no loss, since a framing sentence prescribes nothing, and that is
   why it survived the check that preceded this review. What it cost is the grouping: a reader meets
   eight bullets with no sentence saying they are one family, and the first of them opens on lanes,
   which the fence paragraph above never mentions. Restoring a short lead-in returns the frame at
   about forty bytes of the three hundred the rewrite saved.

2. **The shared living document lost its name.** Recommended repair, two words. The old sentence
   called the document the lanes share a convergence point that the pen reconciles at integration. The
   new one says the pen reconciles that document at integration. The mechanism survives and the name
   does not, and the name is the pack's own: `PRODUCT_SPEC.md` states it in the edge rule, `TEST_MATRIX.md`
   row M-147 carries it, `tests/test_traceability.py` asserts it there, and two working skills say it
   in nearly these words — `skills/build-pipeline/SKILL.md` line 582 and `skills/product-prover/SKILL.md`
   line 837. This file uses it elsewhere too, at line 370. Base rule 3 asks one surface to answer to one
   name everywhere, and the rulebook is where that name should be firmest, so a reader crossing from
   either working skill into the rule they point at now meets a description where the term was.

3. **The by-hand path lost its pointer to the preconditions.** Recommended, one clause. The dropped
   pointer sentence said the script's own header states what it expects on disk. The rule still names
   `scripts/open-lane.sh` and still allows walking the same steps by hand, and it lists three steps.
   The script enforces four preconditions the rule never states: run from the primary worktree on
   main, only the queue file staged, the fence unbroken where it is armed, and the lane branch not
   already present. The batch record says the dropped sentence's facts stand in the script, and they
   do. What the sentence carried was the route to them, and the reader who most needs that route is
   exactly the one doing it by hand.

4. **The batch record's over-cap figure needs its scope.** Correction owed to
   `.live-spec/batch1-verdicts-2026-08-12.md`, not to the skill. Its S2 line reads that over-cap
   sentences inside the rule went from 4 to 0. On the reviewer's own measure with `scripts/rule-census.py`,
   the rule held 9 sentences past the word cap before and holds 5 after. All five sit inside the
   worker-restore clause held byte-frozen by INV-299, and its longest runs 47 words, unmoved in either
   version. The rewritten prose does reach zero, which is what the figure means and not what it says. A
   later pass reading a bare 0 would take rule 7 for finished, when what stands is five over-cap
   sentences that cannot be touched without the owner's word on the one-wording freeze.

5. **The actor is dropped from one sentence.** Minor. The old text closed the lane-open bullet by
   saying the recorded reason is a discipline the session holds; the new one says this stays a
   discipline, with the holder gone and two candidate referents for the pronoun. The register's own
   actor check asks a rule sentence to answer who does this, and naming the session again costs three
   words.

6. **Nothing inside the skill points at the removed wording.** Reviewed and clear. A grep of every
   file of this skill, and of the other ten skills, for the removed phrases returns nothing. The
   file's own pointer at rule 7, the line about the worker-restore sub-rule riding each brief in one
   wording, still holds, since that clause is byte-frozen. The one cross-skill pointer,
   `skills/build-pipeline/SKILL.md` line 423, cites base rule 7 for a repo you were not assigned to
   staying read-only, and that sentence survives the rewrite in its new phrasing.

## The measures this review was held to

The census reads `skills/live-spec-base/SKILL.md` at 70 findings after the rewrite against 74 before —
56 sentences past the word cap and 14 style findings, the style count unmoved and no register findings
in either reading. Rule 7 alone measures 5,171 bytes against 5,477, and the frozen clause inside it
1,567 bytes with 5 of the rule's remaining over-cap sentences. The body still holds 34 numbered rule
heads against the description's thirty-four. The pin-drift gate passes, 209 pins checked. The
loadability gate reports eleven skills loading, named, versioned and negative-scoped. The
language-rules gate passes. The tests that pin this rule's literals and the rule count pass under this
reviewer's own run: 138 across the lane road, brief-time disjointness, worker-restore and skill-count
files, and 36 across the four files the preceding cut touched.
