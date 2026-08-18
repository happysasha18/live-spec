"""A landing closes the checkpoints it shipped — M-240 (SPEC INV-107, row 226).

The closing half of the checkpoint law. The audit (2026-07-10) found two engine checkpoints still
reading "not started" after everything in them shipped, so a resuming session would have redone done
work. A landing that ships a checkpoint's items flips that checkpoint to its closed state in the same
landing; a checkpoint whose items all live in git history is stale by definition. String rows on the
law's two homes (the spec breakpoint clause + base rule 6) plus the spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestCheckpointClosesLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/live-spec-base/SKILL.md")

    def test_closing_half_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn(
                "A landing that ships a checkpoint's items flips that checkpoint "
                "to its closed state in the same landing",
                body,
                home,
            )
            self.assertIn("so a returning session never reopens finished work", body, home)

    def test_stale_checkpoint_is_a_defect_in_both_homes(self):
        # common needle across both homes: the "stale by definition" verdict itself.
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("stale by definition", body, home)
        # skill home keeps the original phrasing verbatim.
        skill = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn(
            "A checkpoint whose items all live in git history is stale by definition "
            "and reads as a resume defect",
            skill,
        )
        # spec home (R126.2 [INV-107]): same rule, requirements-format phrasing — the
        # resume-defect verdict is now the landing failing on a checkpoint left "not started"
        # after its items shipped.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "read a checkpoint whose items all live in git history as stale by definition",
            spec,
        )
        self.assertIn(
            "fail the landing on a checkpoint left reading as not started after its items shipped",
            spec,
        )

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-107]", spec)
        # index now carries locations only (SPEC INV-271) — assert the row exists, and move the
        # "landing" prose check onto the body criterion that carries INV-107.
        found_row = False
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-107 |"):
                    found_row = True
                    break
        self.assertTrue(found_row, "INV-107 index row missing")
        self.assertIn(
            "a landing ships a checkpoint's items, the system *shall* flip that checkpoint "
            "to its closed state in the same landing",
            spec,
        )


if __name__ == "__main__":
    unittest.main()
