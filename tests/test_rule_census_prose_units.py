"""What the census reads as a prose sentence, and what it reads as a list of names.

The word cap exists so a reader can hold a sentence. A run of short names separated by the
interpunct this project uses for lists carries no such load, so its length is no finding. A run of
prose clauses separated by the same mark is still prose, and it stays counted.
"""

import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(ROOT, "scripts", "rule-census.py")


def _census():
    spec = importlib.util.spec_from_file_location("rule_census", CENSUS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCodeRosterIsNoSentence(unittest.TestCase):

    def setUp(self):
        self.census = _census()

    def test_a_roster_of_short_names_is_no_long_sentence(self):
        """A generated roster of rule identifiers runs past the cap and reads as a list."""
        roster = ("Binds 11 of the 58 rules: r10 · r12 · r13 · r14 · r15 · r18 · r27 · r48 · r61 "
                  "· r66 · r67.\n")
        over, longest = self.census.long_sentences(roster, 25)
        self.assertEqual(over, 0, "a roster of short names was counted as a long sentence")
        self.assertEqual(longest, 0, "a roster of short names was measured as a sentence")

    def test_prose_clauses_split_by_the_same_mark_stay_counted(self):
        """A run of prose clauses carries the reading load the cap is there to hold."""
        clauses = ("The intake skill brings what comes back to its home · the collector offers a "
                   "rare private note up to the authors · the audit skill reads a text as a "
                   "stranger and repairs where they stop.\n")
        over, _ = self.census.long_sentences(clauses, 25)
        self.assertEqual(over, 1, "a run of prose clauses stopped being counted")

    def test_a_short_roster_is_left_alone(self):
        """Two members are a pair inside a sentence, so the roster test never reaches them."""
        pair = "The rule binds two surfaces: spec-body · human-prose.\n"
        over, longest = self.census.long_sentences(pair, 25)
        self.assertEqual(over, 0)
        self.assertGreater(longest, 0, "a short line stopped being read as a sentence")


if __name__ == "__main__":
    unittest.main()
