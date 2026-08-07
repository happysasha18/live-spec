# Skill review — build-pipeline (the report-grounding sentences, Requirement 310 / INV-314)

`SKILL-REVIEW`

Skill: build-pipeline
Date: 2026-08-07 10:48
Reviewer: a worker session raised for this review alone. It did not author the change under review.

Verdict: the addition states the law faithfully and sits inside the right bullet. One finding goes
to the seat: the reference page the bullet points to for "the full protocol" does not carry the new
duty, so a reader who follows that pointer misses it. This is a recommendation, not a block.

## What was reviewed

Three sentences added to `skills/build-pipeline/SKILL.md`'s delegation-reporting bullet, landed in
two commits: `d245b7b` wrote them, `c8a0d59` re-split them for the file's own sentence-length law.
The final text: "Each work block in the report opens by naming its root. The root is the person's
dated request, a standing instruction, or a stated reason, and machinery is never a root. The report
accounts each block against its announced plan line (SPEC INV-314)."

## Finding 1 — the law reads faithfully, scoped to the report side alone

`PRODUCT_SPEC.md` Requirement 310 states eleven criteria. The addition covers three: criterion 6
(a report line opens with its block's root), criterion 2 read together with 4 (a root is the
person's dated request, a standing instruction, or a stated reason; machinery is never one), and
criterion 11 (each block is accounted against its plan line in the delivery report). All three match
their spec source in substance.

The addition leaves out criteria 1, 3, 7, and 8 — naming the root when a block starts, refusing to
start a rootless block, and stopping to announce an out-of-plan step before taking it. That is not a
gap. The bullet it sits in is scoped to delegation reporting, not to block-start behavior, and the
commit message names "the pipeline skill's report shape" as this addition's one home. The narrower
scope matches the section it landed in.

## Finding 2 — the placement sits in the right bullet, but the pointer beside it now under-promises

The three sentences land in the "Junior delegation" bullet, directly after the sentence naming "the
delegation-reporting duty" and pointing at `references/delegation-protocol.md` for "the full
protocol." That is the correct bullet — it is the one place in the file that already owns delegation
reporting.

`references/delegation-protocol.md` carries no mention of INV-314 or of a report line's root. A
reader who follows the "full protocol" pointer to find every reporting duty will not find this one;
it exists only in the three sentences that sit after the pointer, back in `SKILL.md`. The bullet's
own promise ("full protocol") now slightly overstates what the reference page holds.

Recommendation: either fold a short pointer to INV-314 into `delegation-protocol.md`, or soften "the
full protocol" to acknowledge that one duty lives beside the pointer rather than behind it. Neither
is required to land what already shipped; both close the reachability gap for the next reader.

## Finding 3 — no contradiction found nearby, register holds

The bullet immediately after (worker git-restore discipline) does not touch reporting or roots, and
nothing else in the file restates the root-naming law in conflicting terms. The word "root" is used
elsewhere in the file for the repository root and for a test flake's root cause; both are common,
contextually distinct uses, and neither sits near the new sentences, so no real collision.

All three added sentences measure at 11, 20, and 12 words, each under the file's 25-word ceiling.

## Checks run

- `git log --oneline -3 -- skills/build-pipeline/SKILL.md` and `git show` on `d245b7b` and `c8a0d59`
  — the delta read in full, across its two-commit split.
- `PRODUCT_SPEC.md` Requirement 310 (lines 7808-7837) read against the three added sentences.
- A grep for `root` and for `INV-314` across `skills/build-pipeline/SKILL.md` and
  `skills/build-pipeline/references/delegation-protocol.md`.
- A word count on each of the three added sentences.
