"""The census stores no risen count (SPEC INV-301, R302.9, R302.10, R302.11; M-480, M-481).

The record of finding counts is a ceiling, and gate aa prints `rule-census.py --json` as the remedy for
a document whose count fell. Before this, that same command stored a RISEN count with the rest, so the
refused operator held the one command that turned the refusal into a pass. The write path now reads the
record it is about to write and refuses to store a rise.

The red-first proof is `test_the_census_refuses_to_store_a_risen_count`: a document recorded at zero,
given one sentence past the word cap, drives `scripts/rule-census.py --json` to a non-zero exit with the
record on disk left exactly as it stood.

No test here writes `guardrails/rule-census.json`. Every run is given a scratch record under a scratch
root, so the repository's own record is untouched.
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(ROOT, "scripts", "rule-census.py")

OVER_CAP = ("# page\n\nA sentence of more than twenty-five words that runs on and on and on and on and "
            "on and on past the cap it is held to here.\n")
UNDER_CAP = "# page\n\nA short sentence.\n"


def run(record, root):
    return subprocess.run(["python3", CENSUS, "--root", root, "--json", record],
                          capture_output=True, text=True)


def seed(tmp, body, recorded_total=None, reason=None):
    """A one-document tree, and a record naming that document's ceiling where one is asked for."""
    with open(os.path.join(tmp, "CLEAN.md"), "w", encoding="utf-8") as f:
        f.write(body)
    record = os.path.join(tmp, "record.json")
    if recorded_total is not None:
        entry = {"file": "CLEAN.md", "total": recorded_total, "long": 0, "longest": 0,
                 "style": 0, "register": 0, "bytes": 0}
        if reason:
            entry["reason"] = reason
        with open(record, "w", encoding="utf-8") as f:
            json.dump({"cap": 25, "cap_rule": "r08", "files": {"CLEAN.md": entry}}, f)
    return record


def read(record):
    with open(record, encoding="utf-8") as f:
        return json.load(f)["files"]


class TestRuleCensusRatchet(unittest.TestCase):

    def test_the_census_refuses_to_store_a_risen_count(self):
        """RED-FIRST: a document above its recorded count is named, and the record is left alone."""
        with tempfile.TemporaryDirectory() as tmp:
            record = seed(tmp, OVER_CAP, 0)
            r = run(record, tmp)
            self.assertEqual(r.returncode, 1, "a risen count was stored:\n%s" % r.stdout)
            self.assertIn("CLEAN.md", r.stdout)
            self.assertEqual(read(record)["CLEAN.md"]["total"], 0,
                             "the record was rewritten in a run that should have written nothing")

    def test_the_census_writes_when_nothing_rose(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = seed(tmp, UNDER_CAP, 5)
            r = run(record, tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(read(record)["CLEAN.md"]["total"], 0)

    def test_the_census_carries_a_recorded_reason_forward(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = seed(tmp, UNDER_CAP, 5, reason="raised on 2026-07-28 for the merged page")
            r = run(record, tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            entry = read(record)["CLEAN.md"]
            self.assertEqual(entry["total"], 0)
            self.assertEqual(entry.get("reason"), "raised on 2026-07-28 for the merged page",
                             "the rewrite erased the reason a person wrote by hand")

    def test_the_census_seeds_an_absent_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = seed(tmp, UNDER_CAP)
            r = run(record, tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("CLEAN.md", read(record))


if __name__ == "__main__":
    unittest.main()
