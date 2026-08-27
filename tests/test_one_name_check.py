"""The one-name-per-thing gate (SPEC INV-255).

`guardrails/check-one-name.py` reds a document that references one artifact under an alias from
`guardrails/one-name-aliases.json`, and passes one that uses the canonical name. UNARMED (INV-270).
"""
import os
import subprocess
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-one-name.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "tests", "fixtures", "specformat", "good_corpus_section.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


class TestOneNameGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "guardrails", "one-name-aliases.json")),
                        "the alias data file does not ship")

    def test_clean_corpus_passes_with_reach(self):
        r = run(CORPUS)
        self.assertEqual(r.returncode, 0, "the gate red the clean corpus:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)

    def test_reds_two_names_for_one_thing(self):
        r = run(os.path.join(FX, "onename_alias.md"))
        self.assertNotEqual(r.returncode, 0, "passed a two-name reference:\n%s" % r.stdout)
        self.assertIn("ticket", r.stdout)
        self.assertIn("backlog item", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-one-name", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-one-name", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate runs on the live
        # PRODUCT_SPEC.md via the suite (gate b), the INV-239 suite-riding placement.
        r = run(*spec_paths())
        self.assertEqual(r.returncode, 0, "the armed gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
