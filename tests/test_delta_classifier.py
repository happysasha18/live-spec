"""The delta classifier (SPEC INV-260, INV-261, INV-262, INV-263).

`guardrails/check-delta-record.py` diffs an old criteria set against a new one under normalization and
reds where the delta record and the diff disagree. Every red case has its own fixture pair and record;
the identity case (no delta) and each correctly-declared change prove the green direction. UNARMED
(INV-270).
"""
import os
import subprocess
import unittest

from conftest import ROOT

GATE = os.path.join(ROOT, "guardrails", "check-delta-record.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "prototype", "2026-07-22-spec-format", "pilot", "section.md")


def fx(name):
    return os.path.join(FX, name)


def run(old, new, rec):
    return subprocess.run(["python3", GATE, fx(old), fx(new), fx(rec)], capture_output=True, text=True)


class TestDeltaClassifier(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE))

    def test_identity_no_delta_passes_with_reach(self):
        r = subprocess.run(["python3", GATE, CORPUS, CORPUS, fx("rec_empty.json")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, "the classifier red an identity delivery:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)

    # --- appeared / disappeared / changed vs the record (INV-261) ---
    def test_declared_new_passes(self):
        self.assertEqual(run("mini_good.md", "mini_added.md", "rec_added_new.json").returncode, 0)

    def test_appeared_undeclared_reds(self):
        r = run("mini_good.md", "mini_added.md", "rec_empty.json")
        self.assertNotEqual(r.returncode, 0, "passed an undeclared appearance:\n%s" % r.stdout)
        self.assertIn("INV-4", r.stdout)

    def test_declared_retire_passes(self):
        self.assertEqual(run("mini_good.md", "mini_retired.md", "rec_retire.json").returncode, 0)

    def test_disappeared_undeclared_reds(self):
        r = run("mini_good.md", "mini_retired.md", "rec_empty.json")
        self.assertNotEqual(r.returncode, 0, "passed an undeclared disappearance:\n%s" % r.stdout)
        self.assertIn("INV-2", r.stdout)

    def test_declared_sharpen_passes(self):
        self.assertEqual(run("mini_good.md", "mini_sharpened.md", "rec_sharpen.json").returncode, 0)

    def test_changed_text_undeclared_reds(self):
        r = run("mini_good.md", "mini_sharpened.md", "rec_empty.json")
        self.assertNotEqual(r.returncode, 0, "passed an undeclared text change:\n%s" % r.stdout)
        self.assertIn("INV-2", r.stdout)

    # --- the sharpen-survival check (INV-262) ---
    def test_sharpen_whose_old_sentence_survives_reds(self):
        r = run("mini_good.md", "mini_sharpened_survives.md", "rec_sharpen_survives.json")
        self.assertNotEqual(r.returncode, 0, "passed a sharpen whose old sentence survives:\n%s" % r.stdout)
        self.assertIn("survives", r.stdout)

    # --- the growth budget (INV-263) ---
    def test_growth_over_the_declared_budget_reds(self):
        r = run("mini_good.md", "mini_budget_over.md", "rec_added_new.json")
        self.assertNotEqual(r.returncode, 0, "passed growth over the budget:\n%s" % r.stdout)
        self.assertIn("budget", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-delta-record", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-delta-record", f.read())


if __name__ == "__main__":
    unittest.main()
