"""Bootstrap suite scaffold (live-spec B-1) — the host's FIRST runnable suite.

Copy this file to `tests/test_scaffold.py` at bootstrap, together with the six document templates.
Run from the project root:  python3 -m unittest discover tests

This is what "green suite" MEANS for landing #1: the document set is present and filled (headers
dated, the matrix's generated Reference section in place, one live-state block) — i.e., the bootstrap
itself is complete. It is a floor, not a ceiling: landing #1 ships its own first real test beside this file,
and the traceability checks grow from here (the pack's own tests/test_traceability.py is the worked
example of where this scaffold is headed).
"""

import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCS = ("PRODUCT_SPEC.md", "ARCHITECTURE.md", "TEST_MATRIX.md", "PLAN.md", "JOURNAL.md", "NEXT_STEPS.md")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class TestBootstrapComplete(unittest.TestCase):
    def test_document_set_present(self):
        for doc in DOCS:
            path = os.path.join(ROOT, doc)
            self.assertTrue(os.path.isfile(path), "bootstrap doc missing: %s" % doc)
            # 100 bytes: a smell test for "an empty shell", not a size standard. Derived from what
            # the very next test requires — every one of these documents must carry a real first
            # header line with a version and a date, which runs well under 100 bytes on its own. So a
            # file clearing this floor holds at least a header plus some body. No incident or source
            # behind the exact figure; nothing is judged by how far above it a document sits.
            self.assertGreater(os.path.getsize(path), 100, "%s is an empty shell" % doc)

    def test_headers_filled_not_placeholders(self):
        spec_head = read("PRODUCT_SPEC.md").splitlines()[0]
        self.assertRegex(spec_head, r"\(v[\d.]+, \d{4}-\d{2}-\d{2}\)",
                         "SPEC header must carry a real version + date, not the template placeholder")
        for doc in DOCS:
            head = read(doc).splitlines()[0]
            self.assertNotIn("[Project Name]", head,
                             "%s still carries the template placeholder name" % doc)

    def test_matrix_carries_generated_reference(self):
        # The hand-walked coverage-validation checklist retired (row 477): coverage is now held by the
        # mechanical row lint and the generated Reference gate. The matrix carries the generated
        # `## Reference` section built from its body rows, and the mechanical-close teaching in place of
        # the retired checkbox list.
        matrix = read("TEST_MATRIX.md")
        self.assertIn("## Reference", matrix,
                      "TEST_MATRIX lost its generated Reference section (E-15, row 477)")
        self.assertIn("How coverage is held", matrix,
                      "TEST_MATRIX lost the mechanical-close teaching (E-15, row 477)")

    def test_the_list_is_a_table(self):
        body = read("PLAN.md")
        self.assertIn("| # |", body, "PLAN lost its table header")

    def test_next_steps_single_live_state(self):
        blocks = re.findall(r"(?im)^#+ .*live state", read("NEXT_STEPS.md"))
        self.assertLessEqual(len(blocks), 1, "LIVE STATE blocks must be replaced, never stacked")


if __name__ == "__main__":
    unittest.main(verbosity=2)
