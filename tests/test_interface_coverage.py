"""Interface tests and the layer-to-level rule — row 294 (P8+P9, anchored on INV-101).

P8: the test level follows the footprint's layer — a presentation change is asserted at browser-computed
or above, a single-module change at its module's interface, a cross-cutting law by a string/traceability
test across every surface. P9: each module's tests assert its declared INTERFACE (one interface-level row
per architecture-node block), and a cross-cutting law (the declared-laws home, INV-101) gets one test per
surface it governs.

The traceability enforcement extends in two directions, each red-proven on a synthetic fixture:
  (A) a declared law with a surface that has no test row goes red — the same shape as a spec invariant
      with no matrix row;
  (B) a module block with no interface-level row goes red — a derivation defect at the coverage walk.
The real matrix satisfies both (every node block owns an interface row; every declared law is covered),
so the suite stays green while the checks have teeth on a violation.
"""

import os
import re
import sys
import unittest

from conftest import ROOT, external_clone_or_skip, read, read_all_flat, read_flat

sys.path.insert(0, os.path.join(ROOT, "tests"))
from test_traceability import matrix_blocks  # reuse the block parser

LADDER_LEVELS = {"string", "DOM-text", "browser-computed", "pixel"}


# --- the two check functions (the traceability extension) ---

def is_interface_row(row):
    """An interface-level row asserts the node's contract: a row that pins a ladder level and cites an
    owning test, not a bare hand-note."""
    return bool(row.get("owning", "").strip()) and row.get("level") in LADDER_LEVELS


def blocks_missing_interface_row(blocks):
    """A module block (architecture node) owns at least one interface-level row. A block with none is a
    derivation defect (P9). Returns the offending node names."""
    return [node for node, rows in blocks.items()
            if not any(is_interface_row(r) for r in rows)]


def declared_law_surface_gaps(laws):
    """laws: list of {name, surfaces: set, tested: set}. A surface a declared law governs with no test row
    is a gap (P9 / INV-101). Returns (law, surface) pairs."""
    gaps = []
    for law in laws:
        for surface in sorted(law["surfaces"]):
            if surface not in law["tested"]:
                gaps.append((law["name"], surface))
    return gaps


# --- (A) red-proven synthetically, then green on the real declared laws ---

class TestDeclaredLawSurfaceCoverage(unittest.TestCase):
    def test_untested_surface_is_flagged(self):
        laws = [{"name": "register", "surfaces": {"home", "room", "card"},
                 "tested": {"home", "room"}}]  # 'card' untested
        gaps = declared_law_surface_gaps(laws)
        self.assertIn(("register", "card"), gaps, "an untested surface of a declared law must be flagged")

    def test_fully_covered_law_flags_nothing(self):
        laws = [{"name": "clock-honesty", "surfaces": {"a", "b"}, "tested": {"a", "b"}}]
        self.assertEqual(declared_law_surface_gaps(laws), [])

    def test_pack_declared_laws_each_have_a_covering_test(self):
        """The pack's three declared laws (INV-101) are each covered by a matrix row."""
        matrix = read("TEST_MATRIX.md")
        # register on every human-facing surface [INV-28, INV-34, INV-83], clock-honest stamps [INV-24],
        # no self-certification [INV-94] — the declared-laws home names these.
        for law_anchor in ("INV-28", "INV-34", "INV-83", "INV-24", "INV-94"):
            self.assertIn(law_anchor, matrix,
                          "declared-law anchor %s has no covering matrix row" % law_anchor)


# --- (B) red-proven synthetically, then green on the real matrix ---

class TestModuleInterfaceRow(unittest.TestCase):
    def test_block_without_interface_row_is_flagged(self):
        blocks = {"good": [{"owning": "`test_x`", "level": "string"}],
                  "bad-empty": [],
                  "bad-note-only": [{"owning": "", "level": "n/a"}]}
        missing = blocks_missing_interface_row(blocks)
        self.assertIn("bad-empty", missing)
        self.assertIn("bad-note-only", missing)
        self.assertNotIn("good", missing)

    def test_every_real_node_block_owns_an_interface_row(self):
        self.assertEqual(blocks_missing_interface_row(matrix_blocks()), [],
                         "an architecture node block owns no interface-level row (P9 derivation defect)")


class TestLayerToLevelAndInterfaceLaw(unittest.TestCase):
    def test_test_author_states_the_layer_to_level_rule(self):
        ta = read_flat("skills/test-author/SKILL.md")
        self.assertIn("the test level follows the layer the change touches", ta)
        for needle in ("presentation change is asserted at browser-computed",
                       "single-module change is asserted at its module's interface",
                       "a cross-cutting law"):
            self.assertIn(needle, ta, "test-author lost the layer-to-level rule: %s" % needle)

    def test_test_author_states_the_interface_test_requirement(self):
        ta = read_flat("skills/test-author/SKILL.md")
        for needle in ("each module's tests assert its declared interface",
                       "one interface-level row per architecture-node block",
                       "one test per surface it governs"):
            self.assertIn(needle, ta, "test-author lost the interface-test requirement: %s" % needle)

    def test_coverage_checklist_gains_both(self):
        ta = read_flat("skills/test-author/SKILL.md")
        tmpl = read_flat("templates/TEST_MATRIX.template.md")
        for body, home in ((ta, "test-author"), (tmpl, "matrix template")):
            self.assertIn("interface-level row", body, "%s coverage checklist lost the interface rule" % home)
            self.assertIn("layer", body, "%s coverage checklist lost the layer-to-level rule" % home)

    def test_prover_declared_laws_station_owns_the_per_surface_test_duty(self):
        # the canon states the duty as the declared-laws sweep's second demand ("A test per
        # surface."); the INV-101 anchor is a pack fact carried by the pack adapter's pin map.
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("A test per surface", pv,
                      "product-prover's declared-laws station lost the per-surface-test duty")
        pack = read_flat("skills/product-prover-pack/SKILL.md")
        self.assertIn("INV-101", pack)


if __name__ == "__main__":
    unittest.main()
