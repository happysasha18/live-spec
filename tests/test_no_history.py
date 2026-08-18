"""The no-history / provenance gate (SPEC INV-253).

`guardrails/check-no-history.py` reds a dated note or a provenance sentence in the spec body, and
passes a body that states today's behaviour only. UNARMED (INV-270).
"""
import os
import subprocess
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-no-history.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "prototype", "2026-07-22-spec-format", "pilot", "section.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


class TestNoHistoryGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE))

    def test_clean_corpus_passes_with_reach(self):
        r = run(CORPUS)
        self.assertEqual(r.returncode, 0, "the gate red the clean corpus:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)

    def test_reds_a_dated_note_in_the_body(self):
        r = run(os.path.join(FX, "history_date.md"))
        self.assertNotEqual(r.returncode, 0, "passed a dated note:\n%s" % r.stdout)
        self.assertIn("2026-07-05", r.stdout)

    def test_reds_a_provenance_sentence(self):
        r = run(os.path.join(FX, "history_provenance.md"))
        self.assertNotEqual(r.returncode, 0, "passed a provenance sentence:\n%s" % r.stdout)
        self.assertIn("recorded-word", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-no-history", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-no-history", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate runs on the live
        # PRODUCT_SPEC.md via the suite (gate b), the INV-239 suite-riding placement.
        r = run(*spec_paths())
        self.assertEqual(r.returncode, 0, "the armed gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
