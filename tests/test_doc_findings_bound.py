"""Gate aa — no live document carries more findings than its record (SPEC INV-301, M-479).

The owner's word, 2026-07-28 evening: a document repaired to zero stays at zero on every push, with no
exception, and every other document's count moves down alone. The census reports; this gate refuses.

The red-first proof is `test_gate_reds_a_cleared_doc_that_regressed`: a document recorded at zero, given
one sentence past the word cap, drives `guardrails/check-doc-findings-bound.py` to a non-zero exit.
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-doc-findings-bound.py")

OVER_CAP = ("# page\n\nA sentence of more than twenty-five words that runs on and on and on and on and "
            "on and on past the cap it is held to here.\n")
UNDER_CAP = "# page\n\nA short sentence.\n"


def run(record, root):
    return subprocess.run(["python3", GATE, "--record", record, "--root", root],
                          capture_output=True, text=True)


def seed(tmp, body, recorded_total):
    """A one-document tree plus a record naming that document's ceiling."""
    doc = os.path.join(tmp, "CLEAN.md")
    with open(doc, "w", encoding="utf-8") as f:
        f.write(body)
    record = os.path.join(tmp, "record.json")
    with open(record, "w", encoding="utf-8") as f:
        json.dump({"cap": 25, "cap_rule": "r08",
                   "files": {"CLEAN.md": {"file": "CLEAN.md", "total": recorded_total, "long": 0,
                                          "longest": 0, "style": 0, "register": 0, "bytes": 0}}}, f)
    return record, tmp


class TestDocFindingsBound(unittest.TestCase):

    def test_gate_reds_a_cleared_doc_that_regressed(self):
        """RED-FIRST: a document recorded at zero, carrying one finding, turns the gate red."""
        with tempfile.TemporaryDirectory() as tmp:
            record, root = seed(tmp, OVER_CAP, 0)
            r = run(record, root)
            self.assertEqual(r.returncode, 1, "a regressed clean document passed the gate:\n%s" % r.stdout)
            self.assertIn("stays cleared", r.stdout)
            self.assertIn("CLEAN.md", r.stdout)

    def test_gate_passes_a_document_at_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            record, root = seed(tmp, UNDER_CAP, 0)
            r = run(record, root)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("held clean: CLEAN.md", r.stdout)

    def test_gate_reds_a_document_above_a_non_zero_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            record, root = seed(tmp, OVER_CAP, 0)
            # rewrite the record with a ceiling the text still exceeds
            with open(record, encoding="utf-8") as f:
                data = json.load(f)
            data["files"]["CLEAN.md"]["total"] = 0
            with open(record, "w", encoding="utf-8") as f:
                json.dump(data, f)
            r = run(record, root)
            self.assertEqual(r.returncode, 1, r.stdout)

    def test_a_fall_passes_and_names_the_reseed(self):
        with tempfile.TemporaryDirectory() as tmp:
            record, root = seed(tmp, UNDER_CAP, 5)
            r = run(record, root)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("fell: CLEAN.md", r.stdout)
            self.assertIn("rule-census.py --json", r.stdout)

    def test_an_unrecorded_live_document_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            record, root = seed(tmp, UNDER_CAP, 0)
            with open(os.path.join(root, "NEW.md"), "w", encoding="utf-8") as f:
                f.write(UNDER_CAP)
            r = run(record, root)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("NEW.md", r.stdout)

    def test_an_empty_record_reds_rather_than_passing_on_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = os.path.join(tmp, "record.json")
            with open(record, "w", encoding="utf-8") as f:
                json.dump({"files": {}}, f)
            r = run(record, tmp)
            self.assertEqual(r.returncode, 1, r.stdout)

    def test_the_real_repository_passes(self):
        r = subprocess.run(["python3", GATE], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, "the live tree is above its record:\n%s" % r.stdout)
        self.assertIn("held at zero", r.stdout)


if __name__ == "__main__":
    unittest.main()
