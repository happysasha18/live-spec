"""Each scenario states how it is entered and how it exits — INV-127 (row 192).

A person-facing scenario is a flow with edges: it states how it is ENTERED (from where, what must already
hold) and how it EXITS (to where, what it leaves true). The per-operation precondition/postcondition lenses
lifted to the scenario level, kin of the entry-symmetry lens (INV-50) and the runtime view's flow walks
(INV-74). The prover carries the scenario-level lens; an unstated edge is a finding. Binds forward. Homes:
the composition clause, the entry/exit duty in spec-author, product-prover's scenario-level lens. (Alexander
2026-07-09, deferred large theme revived at the next prover-method landing.)
"""

import os
import unittest

from conftest import ROOT, external_clone_or_skip, read_all_flat, read_flat


class TestScenarioEntryExit(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Each scenario states how it is entered and how it exits", spec)
        self.assertIn("[INV-127]", spec)

    def test_spec_lifts_pre_post_to_scenario_level(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "the scenario-level lift of the per-operation precondition and postcondition lenses",
            "the prover reads a flow whose entry or exit is unstated, the system *shall* report it as a finding",
            "binds forward",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
        # "entry"/"exit" prose is asserted against the spec body in test_spec_clause_stands
        # (the requirement heading itself: "how it is entered and how it exits").
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-127 |"):
                    self.assertIn("R65.1", line)
                    return
        self.fail("INV-127 Formal-index row missing")

    def test_spec_author_carries_the_entry_exit_duty(self):
        sa = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("Each scenario states how it is entered and how it exits (SPEC INV-127)", sa)

    def test_prover_carries_the_scenario_level_lens(self):
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Scenario entry and exit", pv)
        self.assertIn("a whole flow's edges", pv)

    def test_matrix_row_covers_the_entry_exit_law(self):
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-268 |"):
                    self.assertIn("INV-127", line)
                    return
        self.fail("M-268 matrix row missing")


if __name__ == "__main__":
    unittest.main()
