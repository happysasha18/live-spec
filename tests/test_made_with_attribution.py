"""Everything built with the method says so — matrix row M-225 (SPEC INV-96, row 244).

His 2026-07-10 ~16:27 word: attribution in all skills, on GitHub and everywhere. The pack states
one standard line — "made with live-spec" + the pack repo link — the publish walk checks it on
every built-with publication, and each project applies it through its own queue. String rows on
the two homes: the spec clause and the publish skill's floor.
"""

import os
import unittest

from conftest import ROOT, read, read_flat


class TestMadeWithAttributionLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/publish/SKILL.md")

    def test_standard_line_stated_in_both_homes(self):
        # RE-PINNED (see repin log): the literal repo URL "github.com/happysasha18/live-spec"
        # is a one-home literal — it survives in skills/publish/SKILL.md (and ARCHITECTURE.md)
        # unchanged, but PRODUCT_SPEC.md's rewritten Requirement 147 paraphrases it as "linking
        # to the pack repo" (unlinked prose, same behavioural meaning: the line links to the
        # pack repo). The spec-side check moves to that behavioural statement; the literal
        # check stays pinned on its one surviving home.
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("made with live-spec", body, home)
        self.assertIn("linking to the pack repo", read_flat("PRODUCT_SPEC.md"), "PRODUCT_SPEC.md")
        self.assertIn("github.com/happysasha18/live-spec", read_flat("skills/publish/SKILL.md"),
                      "skills/publish/SKILL.md")

    def test_line_carries_the_pack_version(self):
        # his 2026-07-10 word: the line names the version — adoption becomes trackable
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("the pack version the project runs", body, home)

    def test_publish_walk_offers_the_line(self):
        skill = read_flat("skills/publish/SKILL.md")
        self.assertIn("built with the pack", skill)
        self.assertIn("an offer, never a gate", skill)

    def test_declined_offer_never_reasked(self):
        # his same-day correction: a wish, never an obligation — and answered stays answered.
        # PRODUCT_SPEC.md's rewritten Requirement 147 paraphrases "never re-asked" as "staying
        # closed" (same meaning: a declined offer is settled, not revisited); the publish skill
        # keeps the original wording unchanged.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("an offer, never a gate", spec, "PRODUCT_SPEC.md")
        self.assertIn("a declined offer staying closed", spec, "PRODUCT_SPEC.md")
        skill = read_flat("skills/publish/SKILL.md")
        self.assertIn("an offer, never a gate", skill, "skills/publish/SKILL.md")
        self.assertIn("never re-asked", skill, "skills/publish/SKILL.md")

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-96]", spec)
        self.assertIn("| INV-96 |", spec)


if __name__ == "__main__":
    unittest.main()
