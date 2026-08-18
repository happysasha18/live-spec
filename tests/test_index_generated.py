"""The generated-index gate (SPEC INV-258, INV-259).

`guardrails/check-index-generated.py` passes when the committed table equals a fresh build and body
and table agree, and reds on drift (a hand edit), a body code the index misses, a code the index
carries that no body criterion does, and an empty body (INV-218). UNARMED (INV-270).
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-index-generated.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
MINI = os.path.join(FX, "mini_good.md")
INDEX = os.path.join(FX, "mini_index_good.md")


def run(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def write(tmp, name, text):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


class TestIndexGeneratedGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE))

    def test_matching_index_passes_with_reach(self):
        r = run(MINI, INDEX)
        self.assertEqual(r.returncode, 0, "the gate red a matching committed index:\n%s" % r.stdout)
        self.assertIn("reach:", r.stdout)
        self.assertIn("rows scanned", r.stdout)

    def test_reds_a_hand_edited_index(self):
        # INV-258: a committed table with an extra row differs from a fresh build.
        with open(INDEX, encoding="utf-8") as f:
            drifted = f.read().rstrip() + "\n| ZZ-999 | R9.9 |\n"
        with tempfile.TemporaryDirectory() as tmp:
            idx = write(tmp, "drift.md", drifted)
            r = run(MINI, idx)
            self.assertNotEqual(r.returncode, 0, "passed a hand-edited index:\n%s" % r.stdout)
            self.assertIn("INV-258", r.stdout)

    def test_reds_a_body_code_the_index_misses(self):
        # INV-259: mini_added.md carries INV-4; the mini_good index does not.
        r = run(os.path.join(FX, "mini_added.md"), INDEX)
        self.assertNotEqual(r.returncode, 0, "passed a body code missing from the index:\n%s" % r.stdout)
        self.assertIn("INV-4", r.stdout)
        self.assertIn("INV-259", r.stdout)

    def test_reds_an_index_code_no_body_criterion_carries(self):
        # INV-259: an index row for a code the body never carries — an empty home.
        with open(INDEX, encoding="utf-8") as f:
            orphaned = f.read().rstrip() + "\n| INV-9 | R1.1 |\n"
        with tempfile.TemporaryDirectory() as tmp:
            idx = write(tmp, "orphan.md", orphaned)
            r = run(MINI, idx)
            self.assertNotEqual(r.returncode, 0, "passed an orphan index code:\n%s" % r.stdout)
            self.assertIn("INV-9", r.stdout)

    def test_reds_an_empty_body_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "empty.md", "# Empty\n\n## Glossary\n\n- **x** — a thing.\n")
            idx = write(tmp, "idx.md", "| Code | Location |\n|---|---|\n")
            r = run(doc, idx)
            self.assertNotEqual(r.returncode, 0, "passed an empty body:\n%s" % r.stdout)
            self.assertIn("EMPTY", r.stdout.upper())

    def test_gate_wired_as_gate_x(self):
        # Armed at the row-445 conversion delivery (INV-270): check-index-generated took over gate x
        # from the retired check-index-prose, wired into the local push gate and the CI mirror.
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertIn("check-index-generated.py", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertIn("check-index-generated.py", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the gate runs on the live
        # PRODUCT_SPEC.md and its committed index PRODUCT_SPEC.index.md via the suite (gate b).
        r = run(*spec_paths(), os.path.join(ROOT, "PRODUCT_SPEC.index.md"))
        self.assertEqual(r.returncode, 0, "the armed index gate red the live spec:\n%s" % r.stdout)

    def test_a_live_part_left_out_of_the_read_reds(self):
        # The aggregator does not forgive a missing part (INV-259): drop the last part of the live
        # spec and the codes its criteria carry lose their body home, so the committed table
        # over-carries them and the gate reds. While the parts map is empty there is no part to
        # drop — the core IS the whole spec — and this proof skips saying so; it arms itself the
        # moment the first part lands. The same fault is proven now over fixtures in
        # tests/test_spec_parts.py, so nothing waits on the move to be tested.
        paths = spec_paths()
        if len(paths) < 2:
            self.skipTest("the parts map is empty — the core is the whole spec, so no part can be "
                          "left out yet (tests/test_spec_parts.py proves the fault over fixtures)")
        r = run(*paths[:-1], os.path.join(ROOT, "PRODUCT_SPEC.index.md"))
        self.assertNotEqual(r.returncode, 0,
                            "the gate passed a spec read with %s left out — a part can go missing "
                            "unnoticed:\n%s" % (os.path.basename(paths[-1]), r.stdout))
        self.assertIn("INV-259", r.stdout)


if __name__ == "__main__":
    unittest.main()
