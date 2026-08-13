# Skill review — product-prover standalone reliability contract

SKILL-REVIEW

Skill: product-prover

Date: 2026-08-13
Reviewer: Codex, in a dedicated clone from the owner's current `live-spec` HEAD. The change was
requested after comparing the public mirror with its version two weeks earlier.

Verdict: passes the targeted skill and edition checks. The pass changes presentation and release
discipline. It adds no new product-review lens.

## What changed

1. The conversation and persisted record now have separate duties. Chat carries the verdict,
   compact model, three expanded findings, an index of the rest, and readiness under a 1,500-word
   default. The record carries every finding and the coverage evidence.
2. A prover pass leaves the reviewed document unchanged by default. It proposes clauses and
   provisional defaults, and applies them only on an explicit request. Writing the review record
   remains part of the review.
3. A missing maintained surface registry no longer disables the policy-uniformity sweep. Phase 1
   supplies a review-derived inventory, while the missing registry is reported once.
4. The standalone edition moves to `1.1.0-standalone`. Its record names the version and runtime-file
   fingerprints. A validator now refuses runtime changes made without a version bump.
5. The edition carries a compact sample response and a versioned acceptance rubric. The rubric pins
   seven critical classes, two negative controls, readiness, and the output budget.
6. The public mirror receives its own GitHub Actions workflow when the ordinary mirror sync runs.
   The workflow validates packaging and the release-version edge.
7. Both skill frontmatter descriptions are now quoted, valid YAML. The previous unquoted colon made
   the frontmatter invalid under the skill-creator validator.

## Boundaries checked

- The full evidence survives in the persisted record; shortening chat drops no finding.
- The reviewed document and the review record have separate write permissions.
- N/A remains available where no surface can be enumerated or the whole document is out of view.
- The two historical sample records stay unchanged as evidence from edition 1.0.0.
- The standalone release clock stays separate from the live-spec pack version.
- Internal and public copies carry the same user-facing output, write, and inventory contracts.

## Verification

- `python3 editions/product-prover/scripts/validate.py` — OK, edition 1.1.0.
- `skill-creator/scripts/quick_validate.py editions/product-prover` — valid skill. PyYAML was loaded
  from a temporary dependency directory because neither system Python nor the bundled runtime
  carried it.
- Targeted pytest set covering the new release contract, mirror selection, class lens, prover homes,
  and full-pass record shape — 49 passed.
- The version-bump test creates a temporary git repository, changes a runtime file under the same
  version, and observes the validator refuse it.
- Rule census over both skill copies, the edition README and reference, and the compact sample — no
  new long sentence. The one edition style count is the pre-existing `SMS` token in its worked quote.
- `git diff --check` — clean.

The repository-wide suite reached 923 passed and 2 skipped before it was stopped after 7 minutes.
Its four failures reproduce inherited state outside this unit: missing installed hooks in the clone,
installed skill copies from another tree, one stale prover record after a prior spec commit, and
pre-existing document-census drift in `PRODUCT_SPEC.md` and `skills/live-spec-base/SKILL.md`. Every
changed product-prover document is held clean by that same census gate.
