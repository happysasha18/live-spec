"""The review-record class is declared once (SPEC INV-156, ROADMAP row 323).

The prover record and the design-review record were declared mirror siblings, but the
skill-creator craft-walk record and the verify-by-deed audit — the same kind of pass —
were never named members of a class. INV-156 declares the class once, names every review
pass's record a member, and states verify's deliberate difference (its outcome lands in
the landing record, not a dated file of this class).

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest -q tests
"""

import unittest

from conftest import read_flat


class TestReviewRecordClass(unittest.TestCase):
    def setUp(self):
        self.spec = read_flat("PRODUCT_SPEC.md")

    def test_review_record_class_declared(self):
        self.assertIn("Every review pass writes its record of one class", self.spec,
                      "the review-record class clause is missing from the spec body")
        # the tag now always rides grouped with sibling codes, never solo
        self.assertIn("INV-156", self.spec, "INV-156 has no body owner")

    def test_names_every_member(self):
        # every review pass is named a member (or the named difference) with its anchor
        # (the codes ride grouped with siblings now, so citation is checked by substring)
        for phrase, anchor in (
            ("the prover's spec re-check", "INV-140"),
            ("the design review", "INV-141"),
            ("the periodic adversarial audit", "INV-145"),
            ("the verify-by-deed audit", "INV-46"),
        ):
            self.assertIn(phrase, self.spec, "review-record class does not name member: %s" % phrase)
            self.assertIn(anchor, self.spec, "member anchor missing: %s" % anchor)
        # the whole-pack skill-creator craft walk rides the audit member
        self.assertIn("skill-creator craft review", self.spec, "the craft walk/review is not named")
        # the shared dated-file shape names each home; the concrete record-directory paths for the
        # design-review and audit members consolidated into ARCHITECTURE.md under one-home-per-fact,
        # while the prover's record home survives in the spec body.
        self.assertIn("`docs/prover/`", self.spec, "spec does not name the prover record home")
        # Since the row-456 conversion the dated review records live in the relocated architecture
        # prover-record file, the architecture itself stating today's structure alone (SPEC INV-279).
        record = read_flat("docs/prover/architecture-prover-record.md")
        for home in ("docs/design-review/", "docs/audit/"):
            self.assertIn(home, record, "the prover-record home does not name the record home: %s" % home)

    def test_states_verify_difference(self):
        self.assertIn("the verify-by-deed audit is the one deliberate difference", self.spec.lower(),
                      "verify's deliberate difference from the class is not stated")
        self.assertIn(
            "in the landing record, since verify is a per-landing gate and keeps no dated "
            "file of this class",
            self.spec, "verify's difference is not stated as landing-record vs a dated class file")
        # the per-landing skill-creator review shares verify's landing-record home, not a class file
        self.assertIn("its per-landing skill-creator review", self.spec,
                      "the per-landing skill-creator review is not placed with verify")

    def test_formal_index_and_ownership(self):
        self.assertIn("| INV-156 |", self.spec, "INV-156 has no Formal-index row")
        # the class is declared once; the pack-side record carriers point at it, never restate it.
        # Since the v5.0.0 externalization the prover's pack-facing pointer lives on the tracked
        # adapter, not on the generic external canon.
        pp = read_flat("skills/product-prover-pack/SKILL.md")
        dr = read_flat("skills/design-reviewer/SKILL.md")
        for body, who in ((pp, "product-prover-pack"), (dr, "design-reviewer")):
            self.assertIn("review-record class", body, "%s does not point at the class" % who)
            self.assertIn("INV-156", body, "%s does not cite INV-156" % who)


if __name__ == "__main__":
    unittest.main()
