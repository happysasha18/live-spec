"""M-485 — a session's opening step reads the previous session's extract (SPEC INV-302, R303.20..R303.26).

A session's opening writes no committed artifact, so no push gate can hold this step. It is a
discipline the seat holds, stated in the specification and carried to the working moment by the base
rulebook, the same road Requirement 93 takes for the resume-side re-read of a deferred item.

These are clause-presence tests, the form this project uses for a law no machine can watch.
"""
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read_all_flat, read_flat as flat


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
        """RED-FIRST: the rulebook is where a session meets this at its opening moment.

        Base rule 35, which restated this informally in SKILL.md's own body, was cut
        2026-08-26 (PLAN.md step 7, commit 0ae778bc): no eval fixture or executable script
        enforced its exact wording, only this clause-presence check. Its mechanism —
        session extract, DECISIONS.md/NEXT_STEPS.md cross-check, session handover shape —
        was never in the cut rule's body anyway; it always lived in the on-demand reference
        module the rule pointed to, references/session-handover.md, which this test now reads
        via the skill's whole normative surface (SKILL.md + references/*.md) rather than the
        SKILL.md body alone. Same precedent as tests/test_class_hunt.py's rule-14 fix and
        tests/test_live_channel_law.py's rule-23 fix.
        """
        base = read_all_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("session extract", base)
        self.assertIn("DECISIONS.md", base)
        self.assertIn("NEXT_STEPS.md", base)

    def test_the_rulebook_names_the_closing_step_too(self):
        base = read_all_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("session handover", base)
        self.assertIn("written by", base)

    def test_the_spec_says_why_no_gate_holds_it(self):
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn("a discipline the seat holds, since a session's opening writes no committed artifact",
                      spec)


if __name__ == "__main__":
    unittest.main()
