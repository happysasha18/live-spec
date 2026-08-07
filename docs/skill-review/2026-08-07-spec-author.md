# Skill review — spec-author (the 500-byte criterion cap removed)

`SKILL-REVIEW`

Skill: spec-author
Date: 2026-08-07 10:48
Reviewer: a worker session raised for this review alone. It did not author the change under review.

Verdict: the remaining sentence stands on its own and matches the owner's decision. One finding goes
to the seat: a sibling document the removal's own rulings page names as a home still carries the cap
in its glossary text. This is a recommendation, not a block.

## What was reviewed

Commit `2d34616` removed one clause from `skills/spec-author/SKILL.md`: "Each declared `new`
criterion fits a **500-byte cap**, and" — leaving the growth-budget sentence that follows it intact.
The file now reads: "A `sharpen` also proves the old sentence no longer survives anywhere in the new
document. The delivery's measured criterion-byte growth (excluding sharpen deltas and glossary
additions) stays within the sum of the byte counts of its declared new criteria."

## Finding 1 — the remaining sentence stands grammatically and lawfully

The cut clause was a separate sentence joined by "and" to the growth-budget sentence. Removing it and
dropping the joining "and" leaves a complete, self-sufficient sentence at 24 words, under the file's
25-word ceiling. It matches `PRODUCT_SPEC.md` Requirement (INV-263) criterion 10 verbatim in
substance: growth is measured excluding sharpen and glossary-addition bytes, bounded by the sum of
new criteria's declared bytes. No per-criterion cap remains as law anywhere in that requirement.

## Finding 2 — no stale reference inside the file itself

A grep of `skills/spec-author/SKILL.md` for "500" and "byte cap" returns nothing. The removal is
clean within this one file: no other sentence, example, or cross-reference in it still cites the cap
or a byte number tied to it.

## Finding 3 — the decision matches the owner's word, but one named sibling home was missed

`DECISIONS.md` at 2026-08-07 ~01:10 records the owner's word directly: "no numeric size caps on
specifications; the standard is no redundancy," striking "the audit page's proposed per-size sentence
caps." The removed clause is exactly this class of cap, and the removal matches the ruling.

`docs/audits/2026-08-07-number-rulings.md` names four homes for this one cap: `guardrails/check-
delta-record.py`, `skills/spec-author/SKILL.md`, `PRODUCT_SPEC.md`, and `tests/test_delta_classifier
.py`. Three are clean — the guard script and the test carry no remaining "500" or byte-cap text, and
this file is clean per finding 2. `PRODUCT_SPEC.md` line 154, the glossary entry for "new-criteria
budget," still reads "each within the per-criterion byte cap" — the cap's own acceptance criterion is
gone from the requirement body, but this one defining line was not swept with it.

Recommendation: strike or reword the glossary line at `PRODUCT_SPEC.md:154` so the growth-budget term
it defines no longer names a cap that no longer exists.

## Checks run

- `git log --oneline -3 -- skills/spec-author/SKILL.md` and `git show 2d34616` — the delta read in
  full.
- A grep for `500`, `byte cap`, and `byte-cap` across `skills/spec-author/SKILL.md` — clean.
- A grep for the same terms across the repository, cross-checked against
  `docs/audits/2026-08-07-number-rulings.md`'s named homes for this specific cap.
- `PRODUCT_SPEC.md` read at its `bytes-per-criterion`, `new-criteria budget` glossary entries and at
  its growth-budget acceptance criterion (line 6748, INV-263).
- `DECISIONS.md` read at 2026-08-07 ~01:10 for the owner's word.
- A word count on the remaining sentence: 24 words, under the file's 25-word ceiling.
