"""Deferred rows are revisited at every queue-take, not only at milestones — INV-129 (row 282, prover F3).

A deferred row carries a revisit trigger [T-8]; a time-bound one ("before the next release", "when the
campaign ships") can come true and lapse between two milestone gates, so the milestone re-scan [M-1] read
the triggers too rarely. The fix states a second cadence: at every queue-take the session re-scans each
deferred row's revisit trigger, and a fired trigger returns its row to the runnable head [INV-49] right
then — the same triggers read by the same rule at both cadences, so a deferred wish never waits on a
trigger nobody reads [INV-1], whichever comes first. Homes: the queue-take clause + build-pipeline's
queue-take walk. String level, matrix M-270.
"""

import unittest

from conftest import open_spec, read_all_flat, read_flat


class TestDeferredRevisitCadence(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "Deferred rows are revisited at every queue-take",
            spec,
        )
        self.assertIn("the milestone re-scan is not the trigger's only reader", spec)
        self.assertIn("[INV-129,", spec)

    def test_spec_states_both_cadences(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "at every queue-take the session also re-scans each deferred row's revisit trigger",
            "a fired trigger returns its row to the runnable head",
            "a deferred wish never waits on a trigger nobody reads",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-129 |"):
                    break
            else:
                self.fail("INV-129 Formal-index row missing")
        # the index row is now location-only (SPEC INV-271); the prose lives on the body
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Deferred rows are revisited at every queue-take", spec)

    def test_build_pipeline_carries_the_queue_take_rescan(self):
        # lanes-and-pen.md moved to skills/director/references/ in the build-pipeline cutover
        bp = read_all_flat("skills/director/SKILL.md")
        self.assertIn(
            "re-scans every deferred row's revisit trigger against the current moment (SPEC INV-129)",
            bp,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
