"""A norm-pointered clause owes a norm-conformance matrix row — M-227 (SPEC INV-43, row 216).

Born of the onboarding card's bounce, 2026-07-10 ~10:15: the first render invented its own row
format, dropped three norm sections, and shipped green — no derivation rule demanded a row
checking the render against the frozen norm. The law lands in test-author's derivation rules
(the matrix half); build-pipeline's code step already carries the norm-open + diff-line half.
"""

import unittest

from conftest import read_flat


class TestNormConformanceLaw(unittest.TestCase):
    def test_derivation_owes_the_conformance_row(self):
        body = read_flat("skills/test-author/SKILL.md")
        self.assertIn("norm-conformance row", body)
        self.assertIn("every norm section and row name present in the render", body)

    def test_never_side_names_the_bounce(self):
        body = read_flat("skills/test-author/SKILL.md")
        self.assertIn("a render that invents its own structure never ships green", body)

    def test_both_halves_cited_together(self):
        body = read_flat("skills/test-author/SKILL.md")
        self.assertIn("plan-vs-prototype diff line", body)

    def test_look_stays_the_humans_eye(self):
        body = read_flat("skills/test-author/SKILL.md")
        self.assertIn("the look itself stays the human's eye", body)


if __name__ == "__main__":
    unittest.main()
