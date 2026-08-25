"""A fix touching a spec-backed literal owes its docs and test the same session — M-239 (SPEC INV-104, row 225).

Born of the row 220 audit (2026-07-10): one-line fixes touching spec-backed literals kept shipping
without same-session doc sync. The rules already existed (docs travel with the change; the red-first
small-fix path); the gap was a tripwire at build-pipeline's bug and skip doors, so the door step itself
asks whether the edit touches a spec-backed literal or clause, and a yes routes the docs-and-test duty
into the same session mechanically. His 2026-07-10 ~11:00 word queued row 225; landed 2026-07-12. String
rows on the law's two homes plus the spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestVoicedFixTripwire(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/director/references/landing-law.md")

    def test_tripwire_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("does this edit touch a spec-backed literal or clause", body, home)

    def test_binds_docs_and_test_same_session(self):
        # PRODUCT_SPEC.md's rewritten Requirement 42 states the fact in its own words
        # ("the documentation update and the red-first test"); director's landing-law
        # reference (build-pipeline's cutover replacement home) keeps the original phrasing
        # unchanged.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "land the documentation update and the red-first test in the same session",
            spec, "PRODUCT_SPEC.md",
        )
        skill = read_flat("skills/director/references/landing-law.md")
        self.assertIn("the docs and the test land in the same session", skill,
                      "skills/director/references/landing-law.md")

    def test_reads_content_not_diff_size(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("tripwire reads the edit's content", body, home)

    def test_spec_anchor_and_index(self):
        # the new-format index carries locations only (SPEC INV-271); the "literal" prose
        # check moves to the body criterion that carries the code.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-104]", spec)
        self.assertIn("touches a spec-backed literal or clause", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-104 |"):
                    return
        self.fail("INV-104 index row missing")


if __name__ == "__main__":
    unittest.main()
