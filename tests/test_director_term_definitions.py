"""Director defines the four terms its own act table leans on — commit 5db30805.

PLAN.md step 2 named four terms `skills/director/SKILL.md` used but never defined: decision,
grounds stated with an act, halt, and correction (contrasted against decision). Each was verified
missing by grep before landing, then placed beside the act-table paragraph it belongs to. This is
a content-presence check, not a behavioral gate — nothing here proves the Director APPLIES a
definition correctly (evals/director/scenarios.json carries that). It proves the definition text
itself survives edits to the file around it: each needle is the substantive claim the definition
makes, not a throwaway word that would pass against a rewrite that lost the meaning.
"""
import unittest

from conftest import read_all_flat


class TestDirectorTermDefinitions(unittest.TestCase):
    def setUp(self):
        self.director = read_all_flat("skills/director/SKILL.md")

    def test_decision_is_defined(self):
        # a decision is a standing rule/grant/division of responsibility that travels with a
        # request but is recorded apart from that request's own work, so it survives the work
        # item's own close.
        self.assertIn("A decision is a standing rule, not only a single choice", self.director)
        self.assertIn(
            "a standing rule, a grant of authority, a division of responsibility",
            self.director,
        )
        self.assertIn(
            "it travels with the request and gets recorded separately, so the rule survives "
            "after that work item closes",
            self.director,
        )

    def test_halt_is_defined(self):
        # a halt is about the session's own work in progress stopping, not about the wording
        # used to ask for it, and not about some other system that happens to be running.
        self.assertIn("A halt is about state, not about words", self.director)
        self.assertIn(
            "What makes it a halt is that something running should stop running",
            self.director,
        )
        self.assertIn(
            '"stop the server" said in the middle of a procedure names a step of that '
            "procedure",
            self.director,
        )
        self.assertIn("it is an instruction, part of the work, not a halt", self.director)

    def test_correction_is_defined_against_decision(self):
        # a correction attaches to work already in flight and reshapes its goal or constraints,
        # explicitly contrasted with a decision, which settles an open choice within work that
        # keeps going as planned.
        self.assertIn("A correction attaches to work, not to a queue", self.director)
        self.assertIn(
            "A correction is not a decision: a decision settles an open choice within work "
            "that keeps going as planned; a correction changes that work's goal or constraints "
            "so the remainder has to be replanned",
            self.director,
        )

    def test_grounds_stated_with_an_act_is_defined(self):
        # grounds given alongside an act (a reason attached to a halt, a fact attached to a
        # request) are their own act only when they say something the neighbouring act's own
        # goal does not already carry; otherwise they are that act's goal in other words.
        self.assertIn(
            "Grounds stated with an act carry their own act only when they say something new",
            self.director,
        )
        self.assertIn(
            "when it only restates why the neighbouring act wants what it wants, it is not a "
            "second act, it is that act's goal in other words",
            self.director,
        )

    def test_all_four_terms_sit_beside_the_act_table_they_serve(self):
        # each definition lands in the "First -- what did the human just do?" section, beside
        # the seven-act table it clarifies, rather than off in an unrelated reference file.
        idx_table = self.director.index("First")
        idx_decision = self.director.index("A decision is a standing rule")
        idx_halt = self.director.index("A halt is about state")
        idx_correction = self.director.index("A correction attaches to work")
        idx_grounds = self.director.index("Grounds stated with an act carry their own act")
        idx_turn = self.director.index("One turn, several acts")
        self.assertLess(idx_table, idx_decision)
        self.assertLess(idx_table, idx_halt)
        self.assertLess(idx_table, idx_correction)
        # decision/correction/halt sit before the "one turn, several acts" subsection; grounds
        # sits after it, beside the act-splitting rules it clarifies.
        self.assertLess(idx_decision, idx_turn)
        self.assertLess(idx_correction, idx_turn)
        self.assertLess(idx_halt, idx_turn)
        self.assertGreater(idx_grounds, idx_turn)


if __name__ == "__main__":
    unittest.main()
