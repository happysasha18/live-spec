"""The weak-word gate (SPEC INV-256).

`guardrails/check-weak-words.py` reds a criterion carrying a weak word from
`guardrails/weak-words.json` with no reference point, measure, or reason nearby and no [GAP] line, and
passes the same weak word once its slot is filled. Both directions are proven: `weak_unfilled.md` reds,
`weak_filled.md` (the same word with a measure) passes, and the clean corpus passes. UNARMED (INV-270).
"""
import os
import subprocess
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-weak-words.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "prototype", "2026-07-22-spec-format", "pilot", "section.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


class TestWeakWordGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "guardrails", "weak-words.json")),
                        "the weak-word data file does not ship")

    def test_clean_corpus_passes_with_reach(self):
        r = run(CORPUS)
        self.assertEqual(r.returncode, 0, "the gate red the clean corpus:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)

    def test_reds_a_weak_word_with_an_unfilled_slot(self):
        r = run(os.path.join(FX, "weak_unfilled.md"))
        self.assertNotEqual(r.returncode, 0, "passed an unfilled weak word:\n%s" % r.stdout)
        self.assertIn("weak word", r.stdout.lower())

    def test_passes_the_same_weak_word_once_its_slot_is_filled(self):
        r = run(os.path.join(FX, "weak_filled.md"))
        self.assertEqual(r.returncode, 0, "red a weak word whose slot is filled:\n%s" % r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-weak-words", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-weak-words", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate runs on the live
        # PRODUCT_SPEC.md via the suite (gate b), the INV-239 suite-riding placement.
        r = run(*spec_paths())
        self.assertEqual(r.returncode, 0, "the armed gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
