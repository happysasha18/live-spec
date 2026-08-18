""""Critical" priority heads the queue but never preempts a rolling lane, and the bound is echoed at
intake — INV-133 (row 284, prover F5).

"Critical" is defined in bug terms but liftable onto any door, so a critical non-bug (a violated safety gate
the tripwires route to the feature door) heads the queue and then waits for the current lane — only the bug
door preempts — while a human who said "critical" for a live break expects bug-like preemption. The spec
already states the bound (critical heads the queue whatever its door; only the bug door preempts the in-work
lane); the fix makes it unambiguous and ECHOES it back at intake, so the human hears that his critical
non-bug will head the queue but not stop the rolling lane. Homes: the priority clause + Formal index, and
communicator's capture echo (rule 12). String level, matrix M-274.
"""

import unittest

from conftest import open_spec, read_flat


class TestCriticalPreemptBound(unittest.TestCase):
    def test_spec_states_the_bound_unambiguously(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "the pen-holder's next pen-stage boundary without interrupting the rolling lane, "
            "since preemption belongs to the bug door alone",
            spec,
        )
        self.assertIn("INV-133", spec)

    def test_spec_states_the_intake_echo(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "the bound is echoed back at intake",
            "only the bug door preempts",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
        # The "critical" prose is asserted against the flattened spec body above.
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-133 |"):
                    self.assertIn("R38.1", line)
                    return
        self.fail("INV-133 Formal-index row missing")

    def test_communicator_echo_carries_the_bound(self):
        cm = read_flat("skills/communicator/SKILL.md")
        self.assertIn(
            "critical heads the queue but does not preempt the rolling lane (SPEC INV-133)",
            cm,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
