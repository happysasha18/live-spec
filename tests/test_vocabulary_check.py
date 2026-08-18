"""The closed-vocabulary gate (SPEC INV-254).

`guardrails/check-vocabulary.py` reds a glossary term defined twice, a glossary entry no body line
uses, and a banned coinage from `guardrails/spec-coinages.json`; it passes a document whose vocabulary
is closed. UNARMED (INV-270): driven over fixtures and the clean corpus, never the live spec.
"""
import os
import subprocess
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-vocabulary.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "prototype", "2026-07-22-spec-format", "pilot", "section.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


class TestVocabularyGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE))
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "guardrails", "spec-coinages.json")),
                        "the coinage data file does not ship")

    def test_clean_corpus_passes_with_reach(self):
        r = run(CORPUS)
        self.assertEqual(r.returncode, 0, "the gate red the clean corpus:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)
        self.assertIn("rows scanned", r.stdout)

    def test_reds_a_dead_glossary_entry(self):
        r = run(os.path.join(FX, "vocab_dead_entry.md"))
        self.assertNotEqual(r.returncode, 0, "passed a dead glossary entry:\n%s" % r.stdout)
        self.assertIn("sprocket", r.stdout)

    def test_reds_a_banned_coinage(self):
        r = run(os.path.join(FX, "vocab_coinage.md"))
        self.assertNotEqual(r.returncode, 0, "passed a banned coinage:\n%s" % r.stdout)
        self.assertIn("leverage", r.stdout)

    def test_reds_one_thing_defined_twice(self):
        r = run(os.path.join(FX, "vocab_duplicate.md"))
        self.assertNotEqual(r.returncode, 0, "passed a term with two entries:\n%s" % r.stdout)
        self.assertIn("two glossary entries", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-vocabulary", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-vocabulary", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate runs on the live
        # PRODUCT_SPEC.md via the suite (gate b), the INV-239 suite-riding placement.
        r = run(*spec_paths())
        self.assertEqual(r.returncode, 0, "the armed gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
