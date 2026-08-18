"""INV-165 — the design review's standing motion-parity lens (the tlvphotos pinch miss, 2026-07-15).

A gesture / overlay / motion spec triggers a standing lens the design review runs by construction,
naming three same-kind groups the bottom-up similarity lens (INV-141) can miss: entry mirrors exit,
every object type behaves alike, every position behaves alike. Landed as the capstone fix for a real
review miss: a shipped pinch whose desktop entry did not mirror its exit, a phone pinch-out that would
not fly the picture home, and a door picture that behaved differently by slot — none surfaced by a
review that carried only the bottom-up lens.
"""
import os
import sys
import unittest

from conftest import ROOT, criteria_citing, open_spec, read, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


def _read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


class TestGestureOverlayParityLens(unittest.TestCase):
    def test_spec_clause_names_the_three_groups(self):
        # the lens's own framing lives in the requirement's Context block
        self.assertIn("a standing lens the design review runs by construction",
                      read_flat("PRODUCT_SPEC.md"))
        # the three groups and how each behaves are read from INV-165's own criteria, each
        # criterion taken with the bullets under it — what the second and third groups owe
        # now sits in those bullets.
        clause = criteria_citing(read("PRODUCT_SPEC.md"), "INV-165")
        self.assertTrue(clause, "INV-165 has no declaring criterion in PRODUCT_SPEC.md")
        # entry mirrors exit
        self.assertIn("entry-mirrors-exit as the first group", clause)
        self.assertIn("a layer closes by the reverse of the motion that opened it", clause)
        # every object type behaves alike, each to its own rectangle
        self.assertIn("every object type the gesture acts on as the second group", clause)
        self.assertIn("lands back on its own on-screen rectangle", clause)
        # every position behaves alike
        self.assertIn("every position as the third group", clause)
        self.assertIn("the same gesture on the same type in a different slot behaves the same",
                      clause)

    def test_spec_anchor_and_index_row(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only,
        # no prose. "motion-parity lens" is asserted against the spec body instead
        # (Requirement 62's heading and test_spec_clause_names_the_three_groups above).
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("INV-165", spec)
        self.assertIn("motion-parity lens", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-165 |") and "R62.1" in line:
                    return
        self.fail("INV-165 Formal-index row missing")

    def test_design_reviewer_skill_carries_the_lens(self):
        skill = _read("skills/design-reviewer/SKILL.md")
        self.assertIn("standing motion-parity lens", skill)
        self.assertIn("SPEC INV-165", skill)
        for group in ("Entry mirrors exit", "Every object type behaves alike",
                      "Every position behaves alike"):
            self.assertIn(group, skill, "design-reviewer lens missing group: %s" % group)
        # it is registered as the echo channel's second producer
        self.assertIn("two producers", skill)

    def test_architecture_owns_165_under_design_reviewer(self):
        nodes = archformat.parse_nodes(_read("ARCHITECTURE.md"))
        design_reviewer = next((n for n in nodes if n.name == "design-reviewer"), None)
        if design_reviewer is not None and "INV-165" in design_reviewer.anchors_expanded:
            return
        self.fail("the design-reviewer node does not own INV-165")

    def test_matrix_row_present(self):
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-314 |") and "INV-165" in line:
                    return
        self.fail("M-314 (INV-165) matrix row missing")


if __name__ == "__main__":
    unittest.main()
