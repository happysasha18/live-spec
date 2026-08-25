"""The README states the feels boundary as the method's own position — M-250 (rides INV-84/INV-83, row 242).

Born of gate h (SPEC INV-97, this repo attached as its own first host) correctly blocking a
README-only push (2026-07-12): `check_tests_present.py` reds on any user-facing diff (README.md is a
registered `user_facing_globs` entry) that touches nothing under tests/, whether or not the row mints
an invariant or matrix row. Row 242 is prose-only (INV-84 clean-writer authorship, INV-83 the pre-show
register lint) and mints no new spec clause — this string pin exists solely to satisfy that gate, not
because the row needed a new law. It pins the clean writer's paragraph appended to the README's "Why
live-spec, when BMAD…" critique block, before "## Known issues".
"""

import os
import unittest

from conftest import ROOT, read_flat


class TestReadmeStanceParagraph(unittest.TestCase):
    def test_stance_paragraph_present(self):
        body = read_flat("README.md")
        self.assertIn("A spec owns what a project can write down and test.", body)
        self.assertIn("Feel belongs to the owner's eye.", body)
        # "will ever catch" tightened to "will catch" in the current copy.
        self.assertIn("no rubric will catch honestly", body)

    def test_stance_paragraph_before_known_issues(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        stance_idx = text.find("A spec owns what a project can write down and test.")
        known_issues_idx = text.find("Known issues")
        self.assertGreater(stance_idx, -1, "stance paragraph not found")
        self.assertGreater(known_issues_idx, -1, "Known-issues section not found")
        self.assertLess(
            stance_idx, known_issues_idx,
            "stance paragraph must sit before the Known-issues section",
        )


class TestReadmeNoCommandSurface(unittest.TestCase):
    """Row 312: the README states plainly there is no command surface to learn — you drive
    it by talking and the pipeline runs underneath. Pins the strengthened intro sentence."""

    def test_no_command_surface_stated(self):
        body = read_flat("README.md")
        # the semicolon join became two sentences: "There is no CLI. You talk to it."
        self.assertIn("There is no CLI. You talk to it", body)


class TestReadmeTurnkeyGoalParagraph(unittest.TestCase):
    """The README states the pack's actual end goal, not only the spec-code gap it already
    closes — the owner asked for this directly, 2026-08-25: a compact autonomous software
    house (the mandate's own words, `LIVESPEC_DIRECTOR_REBUILD_PLAN.md`) was the pack's whole
    point and the README never said so. Pins the added paragraph and its explicit
    still-under-construction framing (a fast reader could otherwise mistake the direction for
    an already-shipped capability, since the surrounding prose reads as present-tense fact)."""

    def test_turnkey_goal_paragraph_present(self):
        body = read_flat("README.md")
        self.assertIn(
            "a small, self-running engineering team sitting behind your one conversation", body)
        self.assertIn(
            "ask you only about taste, strategy, authority, and anything irreversible", body)

    def test_turnkey_goal_paragraph_marked_not_yet_delivered(self):
        body = read_flat("README.md")
        self.assertIn("still under construction", body)
        self.assertIn("What ships today is the first working piece of that goal", body)

    def test_turnkey_goal_paragraph_after_the_spec_code_gap(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        gap_idx = text.find("There is no CLI. You talk to it")
        goal_idx = text.find("self-running engineering team sitting behind your one conversation")
        self.assertGreater(gap_idx, -1, "the spec-code gap paragraph not found")
        self.assertGreater(goal_idx, -1, "turnkey goal paragraph not found")
        self.assertLess(
            gap_idx, goal_idx,
            "the turnkey goal paragraph must follow the spec-code gap it builds on",
        )


class TestReadmeFirstStepInstallsTheProver(unittest.TestCase):
    """A stranger who obeys the first step ends up with the reviewer the pack pins a version
    of. `install.sh` skips any skill carrying its own `.git`, and `product-prover` only ever
    exists as such a clone, so the page must name the script that fetches it — a rehearsal of
    the stranger walk ended with ten skills and no reviewer when the page did not."""

    def test_step_one_names_the_external_skill_installer(self):
        body = read_flat("README.md")
        step_one = body.split("Step 2", 1)[0]
        self.assertIn("scripts/install-external-skills.sh", step_one,
                      "the first step must name the script that installs product-prover")

    def test_the_pack_still_needs_the_skill_that_step_installs(self):
        """If the prover pack ever stops naming it, this step stops being load-bearing."""
        self.assertIn("product-prover", read_flat("skills/product-prover-pack/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
