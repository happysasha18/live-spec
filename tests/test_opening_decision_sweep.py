"""M-485 — a session's opening step reads the previous session's extract (SPEC INV-302, R303.19..R303.23).

A session's opening writes no committed artifact, so no push gate can hold this step. It is a
discipline the seat holds, stated in the specification and carried to the working moment by the base
rulebook, the same road Requirement 93 takes for the resume-side re-read of a deferred item.

These are clause-presence tests, the form this project uses for a law no machine can watch.
"""
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def flat(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return " ".join(f.read().split())


class TestOpeningDecisionSweep(unittest.TestCase):

    def test_the_spec_states_the_opening_step(self):
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn("have a fresh agent read the previous session's handover and its extract", spec)
        self.assertIn("list every decision the person made, each with its timestamp", spec)

    def test_the_spec_names_the_two_records_compared(self):
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn("compare that list against `DECISIONS.md` and `NEXT_STEPS.md`", spec)
        self.assertIn("report it to the seat before work starts", spec)

    def test_the_rulebook_carries_the_rule(self):
        """RED-FIRST: the rulebook is where a session meets this at its opening moment."""
        base = flat("skills/live-spec-base/SKILL.md")
        self.assertIn("session extract", base)
        self.assertIn("DECISIONS.md", base)
        self.assertIn("NEXT_STEPS.md", base)

    def test_the_rulebook_names_the_closing_step_too(self):
        base = flat("skills/live-spec-base/SKILL.md")
        self.assertIn("session handover", base)
        self.assertIn("written by", base)

    def test_the_spec_says_why_no_gate_holds_it(self):
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn("a discipline the seat holds, since a session's opening writes no committed artifact",
                      spec)


if __name__ == "__main__":
    unittest.main()
