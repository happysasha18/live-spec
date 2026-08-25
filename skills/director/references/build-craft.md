# Building the work — smallest-first, and a rejected artifact reopens its source

The pointer referenced from `SKILL.md`'s specialist table, the Developer row.

**Taste-heavy deliverables build smallest-first (SPEC INV-62).** Taste rules a deliverable of
voice, copy, visual style, or spec prose. There, stop at the cheapest judgeable sample: one
paragraph, one card, two sections. Take the human's word on it before the full build spends
anything. Five full packs once failed on a problem a one-paragraph sample would have caught.

**A rejected artifact reopens its SOURCE (SPEC INV-63).** The fix starts at the spec clause /
card / brief that produced it: correct the source, then rebuild from it. Line-patching the
rejected output against an unchanged source is the five-round trap, banned.

**A norm-pointered surface builds with the artifact open (SPEC INV-43).** When the surface's spec
clauses carry a `norm: <path>` pointer, OPEN the artifact before building. The frozen prototype is
the norm for look and feel, and the clause text only its laws. Record a one-line plan-vs-prototype
diff in the landing's accounting. A missing diff line is a defect at review.
