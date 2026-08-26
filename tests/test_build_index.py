"""The generated-index builder (SPEC INV-258).

`scripts/build-index.py` builds the code-to-location table from a document's body criteria. It is the
builder, not a gate — this suite proves it emits the expected table, stays deterministic, and reds an
empty body by name (the vacuous-input guard, INV-218).
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

BUILDER = os.path.join(ROOT, "scripts", "build-index.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
MINI = os.path.join(FX, "mini_good.md")


def run(*args):
    return subprocess.run(["python3", BUILDER, *args], capture_output=True, text=True)


class TestBuildIndex(unittest.TestCase):
    def test_emits_the_code_to_location_table(self):
        r = run(MINI)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("| Code | Location |", r.stdout)
        self.assertIn("| INV-1 | R1.1 |", r.stdout)
        self.assertIn("| INV-2 | R1.2 |", r.stdout)
        self.assertIn("| INV-3 | R2.1 |", r.stdout)

    def test_build_is_deterministic(self):
        self.assertEqual(run(MINI).stdout, run(MINI).stdout,
                         "the builder is not deterministic on one input")

    def test_matches_the_committed_fixture(self):
        with open(os.path.join(FX, "mini_index_good.md"), encoding="utf-8") as f:
            committed = f.read()
        self.assertEqual(run(MINI).stdout, committed,
                         "the committed index fixture drifted from a fresh build")

    def test_refuses_to_overwrite_its_own_input(self):
        # A builder whose -o lands on its input would replace the document with its own index
        # (the 2026-07-23 row-477 clobber). It refuses and leaves the document untouched.
        import shutil
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
            doc = tf.name
        try:
            shutil.copyfile(MINI, doc)
            with open(doc, encoding="utf-8") as f:
                before = f.read()
            r = run(doc, "-o", doc)
            self.assertNotEqual(r.returncode, 0, "the builder accepted -o onto its own input")
            self.assertIn("input", r.stdout.lower())
            with open(doc, encoding="utf-8") as f:
                self.assertEqual(f.read(), before, "the builder rewrote its input document")
        finally:
            os.unlink(doc)

    def test_reds_an_empty_body_by_name(self):
        # INV-218: a document that parses to zero coded criteria reds rather than building over nothing.
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
            tf.write("# Empty\n\n## Glossary\n\n- **x** — a thing.\n")
            empty = tf.name
        try:
            r = run(empty)
            self.assertNotEqual(r.returncode, 0, "built over an empty body:\n%s" % r.stdout)
            self.assertIn("EMPTY", r.stdout.upper())
        finally:
            os.unlink(empty)


if __name__ == "__main__":
    unittest.main()
