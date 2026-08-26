"""Eval-craft follow-ups from the 2026-07-12 skill-evals re-run — row 268.

S1: communicator's INV-27 pipeline-station criterion scored PARTIAL a third re-run; it earns an owner —
a dated decision that the plain-words form is acceptable and the literal station handle is optional.
S2: build-pipeline's delegation-brief PARTIAL persisted because the scenario only brushes delegation;
the fix is a delegation-forcing scenario variant on the eval. (N1's floor folds are prose in three eval
files; this guards the two structural additions.)
"""

import unittest

from conftest import read_flat


class TestEvalCraftRow268(unittest.TestCase):
    def test_s1_dated_decision_on_inv27(self):
        body = read_flat("evals/communicator.md")
        self.assertIn("DATED DECISION 2026-07-12 (row 268)", body)
        self.assertIn("literal station handle is OPTIONAL", body)

    def test_s2_delegation_forcing_scenario_variant(self):
        body = read_flat("evals/build-pipeline.md")
        self.assertIn("parse_row", body)  # the rename that trips the >3-files tripwire

    def test_n1_floor_folds_recorded(self):
        for rel in ("evals/build-pipeline.md", "evals/feedback-intake.md", "evals/test-author.md"):
            self.assertIn("row 268/N1", read_flat(rel), f"{rel} missing its N1 floor fold")


if __name__ == "__main__":
    unittest.main()
