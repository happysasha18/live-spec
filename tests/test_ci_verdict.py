"""The push walk reads the remote gate's verdict; a red CI is the session's own immediate bug — M-245 (SPEC INV-106, row 228).

Alexander's 2026-07-10 ~11:00 word: why does a mail arrive about a failed deploy the session should have
caught and fixed itself. The law: the push step reads the remote gate's own verdict (the CI run the push
triggered), and a red verdict is the pushing session's own immediate bug, fixed and re-pushed the same
session before the human ever meets it in his mailbox. String rows on the law's two homes plus the
INV-106 anchor and index.
"""

import re
import unittest

from conftest import open_spec, read_flat


class TestCIVerdictLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/publish/SKILL.md")

    def test_verdict_read_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("the push step reads the remote gate's own verdict", body, home)

    def test_red_is_immediate_bug_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("red verdict is the pushing session's own immediate bug", body, home)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertRegex(spec, r"\[[^\]\n]*\bINV-106\b[^\]\n]*\]")
        self.assertIn(
            "read the gate's verdict", spec,
            "INV-106's body criterion doesn't carry the verdict phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-106 |"):
                    return
        self.fail("INV-106 index row missing")


if __name__ == "__main__":
    unittest.main()
