"""The pack's own wording never grows a second queue — q-828 (SPEC INV-48, base rules 5 and 41).

An incident on 2026-09-08: a session opened no row all day and still had a backlog ready for the
next one. Two sentences the pack itself states had made that look like the pack's own shape. A
standing orchestration law told the seat to walk a *forward queue* after a landing, which INV-48
already forbids the resume file to carry. And the design reviewer's no-landing, right for a
reviewer, was the only visible model of what a brief looks like, so a brief that asked a lane to
name a repair without building it read as ordinary.

Both sentences were corrected where they stood. These are the guards on that: the wording may be
rewritten, and it may not go back to naming a second queue or to leaving the reviewer's exception
unexplained.
"""

import unittest

from conftest import read_flat


class TestOneQueue(unittest.TestCase):
    """The board is the one queue, in every place the pack states the law."""

    def test_the_standing_law_names_the_board(self):
        law = read_flat("hooks/conduct-law.md")
        self.assertNotIn("forward queue", law)
        self.assertIn("walks the board", law)

    def test_the_spec_law_list_names_the_board(self):
        spec = read_flat("spec/guardrails-freshness.md")
        self.assertNotIn("unblocked queue work", spec)
        self.assertIn("pulling unblocked work off the board", spec)


class TestSameLane(unittest.TestCase):
    """A lane that finds a cause repairs it, and the one exception says why it is one."""

    def test_the_rulebook_states_the_rule(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("repairs it in the same lane", base)
        self.assertIn("the one deliberate exception", base)

    def test_the_reviewer_names_its_exception_and_its_reason(self):
        reviewer = read_flat("skills/design-reviewer/SKILL.md")
        self.assertIn("the one deliberate exception", reviewer)
        # The reason, not just the label: a grouping is not yet a defect anyone meets.
        self.assertIn("not yet a defect anybody meets", reviewer)
        self.assertIn("never as the shape of an ordinary brief", reviewer)


if __name__ == "__main__":
    unittest.main()
