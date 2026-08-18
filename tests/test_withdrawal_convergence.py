"""A withdrawn decision converges — after two withdrawals the recommended option is taken as a surfaced
[default]. INV-130 (row 285, prover F6).

An answered question closes forever [INV-59], but a withdrawn decision re-asks "in plainer terms" [INV-9]
with no cap, so a genuine taste call could loop unbounded. The fix bounds it: after the SECOND withdrawal of
the same decision the session takes the recommended option as a `[default]` surfaced in the landing report
(silence stays consent, INV-31), the same convergence an answered question already has. Homes: the
decision-page clause + Formal index, and communicator's rule 10. String level, matrix M-271.
"""

import unittest

from conftest import open_spec, read_flat


class TestWithdrawalConvergence(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # the old summary sentence is gone; R7's own Case heading + R7.6's shall-subjunctive
        # criterion carry the identical rule (second withdrawal -> recommended option surfaced
        # as a default, never re-asked).
        self.assertIn("Case: a withdrawn decision converges", spec)
        self.assertIn(
            "the same decision is withdrawn a second time, the system *shall* take the "
            "recommended option, surface it as a `[default]`",
            spec,
        )
        self.assertIn("INV-130", spec)

    def test_spec_states_the_bound_and_its_kin(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "withdrawn a second time",
            "surface it as a `[default]`",
            "silence staying consent",
        ):
            self.assertIn(needle, spec, needle)
        # the old "the same convergence an answered question already has" summary sentence is
        # gone; the same relationship now stands structurally as R7.7, the very next criterion
        # under the same "a withdrawn decision converges" Case, sharing INV-130's tag with the
        # answered-question closing rule INV-59.
        self.assertIn(
            "The system *shall* close an answered question for good and *shall* route a later "
            "change of mind as a new wish, the closed decision staying closed",
            spec,
        )
        # the bound is stated beside both kin invariants
        self.assertIn("INV-59", spec)

    def test_formal_index_row(self):
        row = None
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-130 |"):
                    row = line
                    break
        self.assertIsNotNone(row, "INV-130 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — the "withdraw" prose check moves
        # onto the body Case heading that carries INV-130 (already asserted above).
        self.assertIn("Case: a withdrawn decision converges", read_flat("PRODUCT_SPEC.md"))

    def test_communicator_rule_carries_the_bound(self):
        cm = read_flat("skills/communicator/SKILL.md")
        self.assertIn("after the second withdrawal of the same decision (SPEC INV-130)", cm)


if __name__ == "__main__":
    unittest.main(verbosity=2)
