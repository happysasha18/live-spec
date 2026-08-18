"""The live-channel law: a behavioural rule that breaks mid-turn twice earns a live channel — M-246 (SPEC INV-108, row 256).

His 2026-07-12 ~00:39-00:40 word (why a recurring rule lives in a file read once, and that it must be
written into live-spec) plus the worked proof: the routing rule lived in once-read files since June and
broke mid-turn until the every-prompt hook line and the after-the-fact suite check landed (rows 253/254,
2026-07-12), the same cure that killed invented clock stamps. String rows on the law's two homes plus the
spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestLiveChannelLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/live-spec-base/SKILL.md")

    def test_law_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("earns a live channel", body, home)
            self.assertIn("every-prompt hook line", body, home)
            self.assertIn("mechanical after-the-fact check", body, home)
            self.assertIn("once-read", body, home)

    def test_worked_proof_in_both_homes(self):
        # PRODUCT_SPEC.md's rewrite declares its own scope in its preamble ("Edit history
        # lives in JOURNAL.md; this spec states what is true today") and no longer carries
        # historical worked-proof narrative anywhere in its body; only the general rule
        # remains there (asserted in test_law_in_both_homes above). The worked-proof
        # anecdote itself now lives only in the skill's own home.
        body = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("the same cure that killed invented clock stamps", body)

    def test_spec_anchor_and_index(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
        # "live channel" prose is asserted against the flattened spec body instead
        # (already covered by "earns a live channel" in test_law_in_both_homes).
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-108]", spec)
        self.assertIn("live channel", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-108 |"):
                    self.assertIn("R222.1", line)
                    return
        self.fail("INV-108 index row missing")


if __name__ == "__main__":
    unittest.main()
