"""Every skill-kind landing walks skill-creator's review — matrix row M-235 (SPEC INV-99, row 219).

His 2026-07-10 ~10:26 word, raised ~10:29: every skill goes through skill-creator, always — the
work-kind classifier is the trigger. The verify step of a skill-kind wish additionally runs the
installed skill-creator's review of the touched skill; findings fold or get rejected by name in
the landing record. String rows on the two homes: the spec clause and the pipeline's work-kind
table (verify row, skill column).
"""

import unittest

from conftest import open_spec, read_all, read_all_flat, read_flat


class TestSkillKindReview(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/build-pipeline/SKILL.md")

    def test_walk_in_both_homes(self):
        # The work-kind table sits in skills/build-pipeline/references/ after the q-822
        # classifier/pipeline split: the verify step is execution. It still carries the concrete
        # worked example (format/frontmatter/description-triggering); the spec's
        # requirements-format rewrite generalized its Context to the class statement "its craft
        # and its evals where applicable" and left the concrete example to the table.
        load_needles = {
            "PRODUCT_SPEC.md": "its craft and its evals where applicable",
            "skills/build-pipeline/SKILL.md": "does the skill load when it should",
        }
        for home in self.HOMES:
            body = read_all_flat(home)
            self.assertIn("skill-creator", body, home)
            self.assertIn(load_needles[home], body, home)

    def test_findings_fold_by_name(self):
        fold_needles = {
            "PRODUCT_SPEC.md": "folding or rejecting each finding by name in the landing record",
            "skills/build-pipeline/SKILL.md": "folded or rejected by name in the landing record",
        }
        for home in self.HOMES:
            body = read_all_flat(home)
            self.assertIn(fold_needles[home], body, home)

    def test_classifier_is_the_trigger(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("The classifier is the trigger", spec)
        # "mood plays no part" was dropped as an idiom; the same fact (nothing but the classifier
        # decides) stands as R49.2's own wording.
        self.assertIn("fire the walk on every skill-kind landing from the classifier alone", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-99]", spec)
        self.assertIn(
            "skill-creator", spec,
            "INV-99's body criterion doesn't carry the skill-creator phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-99 |"):
                    return
        self.fail("INV-99 index row missing")


if __name__ == "__main__":
    unittest.main()
