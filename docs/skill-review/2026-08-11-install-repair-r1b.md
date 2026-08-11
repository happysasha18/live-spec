# Skill review — the install repair reaches build-pipeline and design-reviewer (R1b)

`SKILL-REVIEW`

Skills: build-pipeline, design-reviewer
Date: 2026-08-11
Reviewer: a fresh reviewer raised for this review alone, with clean context. It did not author the
repair, and it wrote no file. Base rule 33 asks for that freshness. The unit closes finding M3 of
`docs/skill-review/2026-08-11-install-repair-eight-files.md`: these two pages placed the product
spec in the pack's tree, against the other nine.

First verdict: blocked, on one inherited sentence. The page's replacement for the false pack-root
identification told the reader to run every command from the pack repository's root. The page's
own reference card says an installed reader has no such root, and the lane-opening script must run
in the host project's tree. The reviewer also caught the last unanchored "beside this one" in the
family, inside the rewritten paragraph.

Repairs ordered and applied the same hour: the blanket run-from-root sentence is deleted, and each
command's own line names its tree, the shape the suite sentence and design-reviewer's counter line
already used; "beside this one" reads "beside this file"; the bracket-codes sentence takes the
family's "this pack's own" form.

What the review confirmed by hand:
- Both pages now place PRODUCT_SPEC.md with the host project, and a sweep of all eleven skills
  finds no page placing it in the pack. The class is closed.
- The catch-all closings assign every previously unlocated path to the host; the two exposed
  cases (docs/norms/, guardrails.config.json) land right by the spec's and installer's own words.
- Twelve pack paths spot-verified on disk. The bracket-codes paragraphs stand on four pages in
  the same arrangement, so leaving them was right.
- Census counts held exactly on both files, register 0, style finding sets identical line for
  line. Scoped tests: 686 passed, 0 failed.

Standing findings, carried with owners:
- No machine reads any locating paragraph; the check proposal remains decision candidate D11,
  reserved for Alexander's word under the campaign's rule 2.
- Any pack-root file a page later adds is misfiled to the host by the catch-all's default; the
  liability is recorded here and rides with D11's decision.
