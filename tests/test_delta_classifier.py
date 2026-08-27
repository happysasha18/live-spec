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
CORPUS = os.path.join(ROOT, "tests", "fixtures", "specformat", "good_corpus_section.md")


def fx(name):
    return os.path.join(FX, name)


def run(old, new, rec):
    return subprocess.run(["python3", GATE, fx(old), fx(new), fx(rec)], capture_output=True, text=True)


class TestDeltaClassifier(unittest.TestCase):
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

    # --- a criterion added under an existing code (INV-315) ---
    # `mini_extended.md` is `mini_good.md` with ONE bullet added under the code INV-2 already there; the
    # old INV-2 line is untouched word for word. Before the fifth kind existed this case had no green
    # outcome at all: declaring nothing/new/retire/scenario-only red on "not `sharpen`", and declaring
    # `sharpen` red on the old sentence surviving — but that survival is the point of an addition.

    def test_declared_extend_passes(self):
        """Pins the green: only `extend` passes this pair, so the outcome is reachable."""
        r = run("mini_good.md", "mini_extended.md", "rec_extend.json")
        self.assertEqual(r.returncode, 0, "the classifier red a correctly declared extend:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)

    def test_extend_missing_reds(self):
        """Discriminates extend from `nothing`: an undeclared addition must still red, and red as an
        extend — not as the old mis-diagnosed `sharpen`."""
        r = run("mini_good.md", "mini_extended.md", "rec_empty.json")
        self.assertNotEqual(r.returncode, 0, "passed an undeclared extend:\n%s" % r.stdout)
        self.assertIn("not `extend`", r.stdout)

    def test_extend_wrongly_declared_sharpen_reds_survival_false_positive(self):
        """Discriminates extend from `sharpen` in the direction the old classifier got wrong. Declaring
        `sharpen` over an addition must red on the granularity, and the survival red it used to raise
        here is exactly the false positive that left this case with no green."""
        r = run("mini_good.md", "mini_extended.md", "rec_extend_as_sharpen.json")
        self.assertNotEqual(r.returncode, 0, "passed an addition declared `sharpen`:\n%s" % r.stdout)
        self.assertIn("not `extend`", r.stdout)

    def test_extend_declared_over_a_real_sharpen_reds(self):
        """Discriminates in the other direction: `mini_sharpened.md` REPLACES INV-2's sentence, so it is
        a sharpen and `extend` must not pass it. Without this, `extend` would be a way round INV-262."""
        r = run("mini_good.md", "mini_sharpened.md", "rec_extend_wrong.json")
        self.assertNotEqual(r.returncode, 0, "passed a sharpen declared `extend`:\n%s" % r.stdout)
        self.assertIn("INV-315", r.stdout)

    def test_sharpen_fixture_stays_green_and_is_not_an_extend(self):
        """Fixture 2 of the three: the existing sharpen pair keeps its exact old verdict."""
        self.assertEqual(run("mini_good.md", "mini_sharpened.md", "rec_sharpen.json").returncode, 0)

    def test_extend_declared_over_no_change_reds(self):
        """Fixture 3 of the three, made discriminating: a no-change pair is green with an empty record,
        and declaring `extend` over a code that gained nothing must red — so no-change and extend cannot
        both explain the same delivery."""
        self.assertEqual(run("mini_good.md", "mini_good.md", "rec_empty.json").returncode, 0)
        r = run("mini_good.md", "mini_good.md", "rec_extend_wrong.json")
        self.assertNotEqual(r.returncode, 0, "passed `extend` over a code that gained nothing:\n%s" % r.stdout)
        self.assertIn("INV-315", r.stdout)

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
