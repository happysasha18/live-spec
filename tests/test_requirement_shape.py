"""The requirements-format shape gate (SPEC INV-250, INV-251, INV-252).

`guardrails/check-requirement-shape.py` reds a document whose requirements, cases, or criteria break
the format's shape, and passes a well-shaped one. The gate is UNARMED — it arms only in the spec-format
conversion delivery (INV-270), so this suite drives it over FIXTURES and the prototype's clean corpus
(`tests/fixtures/specformat/good_corpus_section.md`), never the live PRODUCT_SPEC.md, and asserts the
gate takes no pre-push or CI letter.

Red-first proof: each red case has its own synthetic fixture under tests/fixtures/specformat/, proven
to red; the clean corpus proves the green direction, including the reach line the family owes (INV-269).
"""
import os
import subprocess
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-requirement-shape.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
CORPUS = os.path.join(ROOT, "tests", "fixtures", "specformat", "good_corpus_section.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


class TestRequirementShapeGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE), "the gate script does not ship: %s" % GATE)

    def test_clean_corpus_passes(self):
        r = run(CORPUS)
        self.assertEqual(r.returncode, 0, "the gate red the clean corpus:\n%s" % r.stdout)

    def test_green_line_states_reach(self):
        # INV-269: the green line names the file opened and the rows matched of rows scanned.
        r = run(CORPUS)
        self.assertIn("reach:", r.stdout)
        self.assertIn("good_corpus_section.md", r.stdout)
        self.assertIn("rows scanned", r.stdout)

    def test_reds_a_requirement_missing_its_context(self):
        r = run(os.path.join(FX, "shape_missing_context.md"))
        self.assertNotEqual(r.returncode, 0, "passed a requirement with no Context:\n%s" % r.stdout)
        self.assertIn("Context", r.stdout)

    def test_reds_a_criterion_with_no_trailing_anchor(self):
        r = run(os.path.join(FX, "shape_no_anchor.md"))
        self.assertNotEqual(r.returncode, 0, "passed a criterion trailing no anchor:\n%s" % r.stdout)
        self.assertIn("anchor", r.stdout)

    def test_reds_discontinuous_numbering(self):
        r = run(os.path.join(FX, "shape_discontinuous.md"))
        self.assertNotEqual(r.returncode, 0, "passed discontinuous numbering:\n%s" % r.stdout)
        self.assertIn("continuously", r.stdout)

    def test_reds_a_malformed_gap_line(self):
        r = run(os.path.join(FX, "shape_bad_gap.md"))
        self.assertNotEqual(r.returncode, 0, "passed a malformed gap marker:\n%s" % r.stdout)
        self.assertIn("gap", r.stdout.lower())

    def test_reds_an_all_capital_shouting_word(self):
        r = run(os.path.join(FX, "shape_shouting.md"))
        self.assertNotEqual(r.returncode, 0, "passed an all-capital word:\n%s" % r.stdout)
        self.assertIn("ALWAYS", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        # INV-270: the gate arms only in the conversion delivery; until then no pre-push or CI step
        # invokes it.
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-requirement-shape", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-requirement-shape", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate now runs on the live
        # PRODUCT_SPEC.md via the suite (gate b), the same suite-riding placement the INV-239
        # nets take (guardrails/pre-push lines 152-157). It must pass on the root document.
        r = run(*spec_paths())
        self.assertEqual(r.returncode, 0, "the armed gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
