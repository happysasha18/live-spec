"""A test's expected value derives independently of the code under test — M-238 (SPEC INV-102, row 224).

His 2026-07-10 ~11:00 word, from row 220's audit (item 3): green suites missed real walk bugs because
tests recomputed the code's own formula as the expected value, so the assertion only proved the code
equal to itself. A test's expected value must come from an independent source — a hand-computed
constant, an independent derivation, or a recorded real output reviewed by a human. String rows on the
law's two homes plus the spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestMirrorAssertionBanLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/test-author/SKILL.md")

    def test_independence_stated_in_both_homes(self):
        self.assertIn(
            "derives independently of the code under test",
            read_flat("skills/test-author/SKILL.md"),
        )
        self.assertIn(
            "is independent of the code under test", read_flat("PRODUCT_SPEC.md")
        )
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("a mirror that can never catch the formula being wrong", body, home)

    def test_legal_sources_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn(
                "a hand-computed constant, an independent derivation, or a recorded real output",
                body,
                home,
            )

    def test_boundary_stated_in_spec(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("allow a round-trip or property test over the outputs", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-102]", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-102 |"):
                    self.assertIn("mirror", spec)
                    return
        self.fail("INV-102 index row missing")


if __name__ == "__main__":
    unittest.main()
