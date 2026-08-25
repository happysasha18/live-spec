"""The drafter-applier pipeline is the standard colliding-rows form — M-242 (SPEC INV-49, row 255).

Born live 2026-07-12: the law batch all touched the spec/matrix/version chain, so landings serialized
under the pen, and the queue still moved at two rows an hour once a drafter worker prepared the next
row's edit strings while the applier landed the current one. String needles on the pipeline's text.
"""

import os
import unittest

from conftest import ROOT, read_flat, read_all, read_all_flat
HOME = "skills/director/SKILL.md"  # drafter-applier-example.md moved to director/ in the build-pipeline cutover


class TestDrafterApplierForm(unittest.TestCase):
    def test_form_named_in_the_pipeline(self):
        body = read_all_flat(HOME)
        self.assertIn("the penless DRAFT stage overlaps the current landing", body)
        self.assertIn(
            "a drafter worker at the judgment tier prepares the next row's exact edit strings", body
        )

    def test_born_live_and_cited(self):
        body = read_all_flat(HOME)
        self.assertIn("still moved at two rows an hour", body)
        self.assertIn("[T-18, INV-39, INV-49]", body)

    def test_standing_self_verify_list(self):
        """Row 263: the drafter brief carries a standing self-verify list for the
        suite's cross-reference laws, walked before handoff."""
        body = read_all_flat(HOME)
        self.assertIn(
            "walks a standing self-verify list against the suite's cross-reference laws", body
        )
        self.assertIn("index density (every new INV anchor gets its Formal-index row)", body)
        self.assertIn(
            "owning node (every new anchor's node stands in ARCHITECTURE.md's owns-list)", body
        )
        self.assertIn(
            "matrix-row-under-owner (every new M-row sits under its owning node)", body
        )


if __name__ == "__main__":
    unittest.main()
