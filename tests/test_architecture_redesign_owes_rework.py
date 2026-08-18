"""A deliberate architecture redesign re-shapes and re-proves ARCHITECTURE.md in the same movement — M-252 (SPEC INV-113, row 257).

The tlvphotos window's word, 2026-07-11 ~23:11: a second-finger bug (a moving finger dragged the
underlying room layer into view in the polaroid side room, the resting-finger fix having opened the
window for it) led Alexander to order a rethink of the UI-layer architecture plus a spec update, and he
asked whether the pack already forces the document rework in that case. The honest answer was only
partly: build-pipeline step 3 updates the doc from the spec and the refactor line updates its pins, but
after a real restacking the old document's own shape lies even with fresh pins. The law: when structure
is deliberately redesigned (layers restacked, a surface's ownership moved, nodes merged or split) the
architecture document is re-shaped to the new form and re-proven with the architecture lens in the same
movement; the pins-only path is scoped to a boundary shift that leaves the shape standing. String rows
on the law's two prose homes plus the spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestRedesignOwesReworkLaw(unittest.TestCase):
    HOMES = (
        "PRODUCT_SPEC.md",
        "skills/build-pipeline/SKILL.md",
    )

    def test_redesign_owes_rework_in_both_homes(self):
        phrase_by_home = {
            "PRODUCT_SPEC.md": (
                "re-shape the architecture document to the new form and "
                "re-prove it with the architecture lens in the same movement"
            ),
            "skills/build-pipeline/SKILL.md": (
                "re-shaped to the new form and re-proven with the architecture "
                "lens in the same movement"
            ),
        }
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn(phrase_by_home[home], body, home)

    def test_pins_only_scoped_to_boundary_shift_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn(
                "a boundary shift that leaves the document's shape standing", body, home
            )

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-113]", spec)
        self.assertIn("A deliberate redesign re-shapes the architecture document", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-113 |"):
                    return
        self.fail("INV-113 index row missing")


if __name__ == "__main__":
    unittest.main()
