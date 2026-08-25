"""A mid-work re-door rebuilds the parallel-lanes independence graph — INV-131 (row 286, prover F7).

A lane re-doored to feature mid-work (INV-16) can create a surface overlapping a rolling sibling, but the
independence graph (INV-49) was not rebuilt, so the departures board kept asserting "independent" after it
stopped being true. The fix: the mid-work door re-check also re-runs the independence edges against every
rolling lane, and a new edge pulls the re-doored lane back to serial with a board line, so the board never
asserts a stale independence. Homes: the mid-work re-door clause + Formal index, and build-pipeline's door
re-fire. String level, matrix M-272.
"""

import unittest

from conftest import open_spec, read_flat


class TestRedoorIndependenceRebuild(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "A mid-work re-door that creates a surface or state re-runs the independence "
            "edges between the parallel lanes",
            spec,
        )
        self.assertIn("[INV-131]", spec)

    def test_spec_states_the_rebuild_and_the_board_line(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "re-run the independence edges against every rolling lane",
            "the system *shall* pull the re-doored lane back to serial",
            "the departures board never asserts a stale independence",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-131 |"):
                    break
            else:
                self.fail("INV-131 Formal-index row missing")
        # the index row is location-only (SPEC INV-271); "independence" prose lives on the body
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("the re-door rebuilds the independence graph".lower(), spec.lower())

    def test_build_pipeline_carries_the_rebuild(self):
        bp = read_flat("skills/director/references/lanes-and-pen.md")
        self.assertIn(
            "re-runs the independence edges against every rolling lane (SPEC INV-131)",
            bp,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
