"""The light vehicle for an owner-scoped docs-layout pass is sanctioned — M-249 (SPEC INV-111, row 240).

The track-coach audit (2026-07-10 ~14:23) found track-coach s63, lacking a named vehicle, correctly
improvised one for a pure docs-layout pass: a checkpoint carrying the owner's locked decisions, work
on a clean pushed base so restore is one command, and a multiset proof that content survived. The
pack now names that shape so hosts neither skip discipline nor over-apply the catch-up machinery.
Two homes: the spec's F-catchup vehicle clause and build-pipeline's docs-only/restructure door.
"""

import unittest

from conftest import open_spec, read_flat


class TestDocsLayoutVehicle(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/build-pipeline/SKILL.md")

    def test_vehicle_in_both_homes(self):
        self.assertIn(
            "A same-version docs-layout pass rides one sanctioned light vehicle",
            read_flat("skills/build-pipeline/SKILL.md"),
        )
        self.assertIn(
            "A same-version docs-layout pass rides one named vehicle",
            read_flat("PRODUCT_SPEC.md"),
        )
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn(
                "a word-token multiset check and a punctuation multiset check",
                body,
                home,
            )

    def test_vehicle_owes_the_full_shape(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("lock the owner's decisions in a checkpoint before any file moves", spec)
        self.assertIn("build on a clean pushed base", spec)
        self.assertIn("full suite green on the restructured tree", spec)
        self.assertIn("land one journal chapter", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-111]", spec)
        # the index row is location-only (SPEC INV-271); the "vehicle" prose lives on the body
        self.assertIn("A same-version docs-layout pass rides one named vehicle", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-111 |"):
                    return
        self.fail("INV-111 index row missing")


if __name__ == "__main__":
    unittest.main()
