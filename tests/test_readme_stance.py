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
