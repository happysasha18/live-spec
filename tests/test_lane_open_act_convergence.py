"""The lane-open act's two live descriptions, proven to still agree (PLAN q-386, SPEC INV-214).

`scripts/open-lane.sh` performs the lane-open act. `skills/live-spec-base/SKILL.md`'s "The
lane-open act" bullet (rule 7) describes the same act in its own words, for a session opening
a lane by hand. `tests/test_lane_branch_road.py` already proves each side on its own — the
script's behaviour by deed on a real repo, and the law's own phrases present in the shipped
document — but neither of those checks reads the OTHER side, so the two descriptions could
drift apart (the branch-name pattern reworded, a step reordered, a step dropped) and nothing
would notice. That gap is what PLAN row q-386 names as its one open leg.

This file closes it by reading the law's own text at run time — not a copy of it hardcoded
here — and using what it says to build the expectation the by-deed run is checked against. A
hand edit to the law's stated branch pattern, its step order, or its third step's handoff
wording moves what this test expects from the real script's run; if the script's actual
behaviour no longer matches, the test reds. A hand edit to the script that changes what it
actually does, with the law left as it reads today, reds the same way.
"""

import re
import unittest

from conftest import read_all_flat
from test_lane_branch_road import _LaneOpenActRepo

SKILL = "skills/live-spec-base/SKILL.md"

_BULLET_START = "The lane-open act.**"
_BULLET_END = "- **Worktree isolation on overlap.**"

_FIRST = re.compile(r"First,\s*(.*?)\s*Second,")
_SECOND = re.compile(r"Second,\s*(.*?)\s*Third,")
_THIRD = re.compile(r"Third,\s*(.*?\.)\s")
_BRANCH_PATTERN = re.compile(r"the branch `(lane/[^`]+)`")


def _law_bullet():
    """The lane-open act's own paragraph, read live off the shipped rulebook — never a copy
    kept here, so an edit to the law is what this test reads on its next run."""
    text = read_all_flat(SKILL)
    i = text.find(_BULLET_START)
    assert i != -1, "%s no longer carries \"The lane-open act.\" bullet (rule 7)" % SKILL
    j = text.find(_BULLET_END, i)
    assert j != -1, "could not find the bullet's end (\"Worktree isolation on overlap\") after it in %s" % SKILL
    return text[i:j]


def _law_steps():
    """The bullet's First/Second/Third clauses and the branch-name pattern it states, all
    pulled out of the live text rather than restated by hand."""
    bullet = _law_bullet()
    first = _FIRST.search(bullet)
    second = _SECOND.search(bullet)
    third = _THIRD.search(bullet)
    branch = _BRANCH_PATTERN.search(bullet)
    assert first and second and third, (
        "the law's First/Second/Third steps no longer parse out of the bullet — "
        "its wording moved and this test's extraction needs to move with it: %r" % bullet
    )
    assert branch, "the law's Second step no longer states a `lane/...` branch pattern: %r" % bullet
    return bullet, first.group(1), second.group(1), third.group(1), branch.group(1)


class TestTheLawStatesTheThreeOrderedSteps(unittest.TestCase):
    """The law's own text, read alone: three steps, in this order, each saying what it must."""

    def test_first_second_third_appear_in_that_order(self):
        bullet = _law_bullet()
        i_first = bullet.find("First,")
        i_second = bullet.find("Second,")
        i_third = bullet.find("Third,")
        self.assertTrue(
            -1 < i_first < i_second < i_third,
            "the law's steps are no longer in First/Second/Third order: %r" % bullet,
        )

    def test_first_step_is_the_claim_commit_under_the_pen(self):
        _, first, _second, _third, _branch = _law_steps()
        self.assertIn("committed to main under the pen", first)

    def test_second_step_cuts_the_branch_into_its_own_worktree(self):
        _, _first, second, _third, branch = _law_steps()
        self.assertIn("cut from that claim commit into its own worktree", second)
        self.assertIn(branch, second)

    def test_third_step_hands_the_lane_to_a_worker_by_its_brief(self):
        _, _first, _second, third, _branch = _law_steps()
        self.assertIn("worker", third)
        self.assertIn("brief", third)
        self.assertIn("branch", third)


class TestTheScriptsDeedConvergesWithTheLaw(_LaneOpenActRepo):
    """The script, run for real on a hermetic repo, checked against what the law — read live,
    not copied here — says the act does. `_LaneOpenActRepo` (test_lane_branch_road.py) is the
    same hermetic harness M-395's by-deed tests already use for `scripts/open-lane.sh`.
    """

    def test_the_branch_the_script_cuts_matches_the_laws_own_pattern(self):
        _bullet, _first, _second, _third, branch_template = _law_steps()
        row, slug = "q-999", "convergence-check"
        expected_branch = branch_template.replace("<row>", row).replace("<slug>", slug)

        self.stage_flip(row)
        rc, out = self.act(row, slug)
        self.assertEqual(rc, 0, out)

        listed = self.run_ok("branch", "--list", "lane/*")
        self.assertIn(
            expected_branch,
            listed,
            "the law's stated pattern %r, instantiated for %s/%s, names %r — the branch the "
            "script actually cut was %r. Either the law's pattern or the script's naming moved "
            "without the other." % (branch_template, row, slug, expected_branch, listed),
        )

    def test_the_deed_walks_the_laws_three_steps_in_the_laws_own_order(self):
        _bullet, first, second, third, branch_template = _law_steps()
        row, slug = "q-999", "convergence-order"
        expected_branch = branch_template.replace("<row>", row).replace("<slug>", slug)

        self.stage_flip(row)
        rc, out = self.act(row, slug)
        self.assertEqual(rc, 0, out)

        # First: "the row->in-work flip is committed to main under the pen" — the claim
        # commit lands on main and its message names the row, exactly as the staged flip.
        self.assertEqual(self.run_ok("rev-parse", "--abbrev-ref", "HEAD").strip(), "main")
        claim_msg = self.run_ok("log", "-1", "--format=%s")
        self.assertIn("row %s" % row, claim_msg, "First step's own words: %r" % first)
        claim_sha = self.run_ok("rev-parse", "HEAD").strip()

        # Second: "the branch ... is cut from that claim commit into its own worktree" — the
        # branch's tip IS the claim commit, and a worktree holds it.
        self.assertEqual(
            self.run_ok("rev-parse", expected_branch).strip(),
            claim_sha,
            "Second step's own words: %r" % second,
        )
        self.assertIn(expected_branch, self.run_ok("worktree", "list"))

        # Third: "the lane goes to a worker whose brief names the branch" — the script's own
        # printed account hands the lane off by naming the branch for a worker's brief.
        self.assertIn("worker", out.lower(), "Third step's own words: %r" % third)
        self.assertIn("brief", out.lower(), "Third step's own words: %r" % third)
        self.assertIn(expected_branch, out)

        # And the script's own printed account keeps the law's order: the claim is reported
        # before the worktree, which is reported before the worker handoff.
        i_claim = out.find("claim commit")
        i_worktree = out.find("worktree")
        i_worker = out.lower().find("worker")
        self.assertTrue(
            -1 < i_claim < i_worktree < i_worker,
            "the script's printed account no longer reports First/Second/Third in that order:\n%s" % out,
        )


if __name__ == "__main__":
    unittest.main()
