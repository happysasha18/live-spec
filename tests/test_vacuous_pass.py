"""INV-218 (M-399, ROADMAP 384) — a check that looked at nothing is not a pass.

The vacuous-pass class: a check whose INPUT SET is empty reports clean while testing
nothing, and an empty input set is nearly always the defect. The drafter's own self-catch
minted this row — it scanned its freshly minted codes for collisions, the codes were absent
from the prose entirely, and the scan compared zero against zero and reported clean.

The law (sibling of the unexpected-skip law INV-155): a check DECLARES the input set it
expects to be non-empty, and an empty set REDS BY NAME rather than passing silently. This
movement builds the shared shape (`guardrails/nonempty_input.py`), which check-matrix-reference.py
and check-size-ratchet.py both apply it to today.

Every check here asserts the SHIPPED files on disk, never a source fragment or a memory of one.
"""
import os
import re
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDRAILS = os.path.join(REPO, "guardrails")
SHAPE = os.path.join(GUARDRAILS, "nonempty_input.py")


class TestSharedShape(unittest.TestCase):
    """The general guardrail shape: a check declares its expected-non-empty input set."""

    def _import_shape(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("nonempty_input", SHAPE)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_shape_reds_by_name_on_empty_input(self):
        mod = self._import_shape()
        with self.assertRaises(mod.VacuousInputError) as cm:
            mod.require_nonempty("some-check", "the widget set", [])
        msg = str(cm.exception)
        self.assertIn("the widget set", msg, "the vacuous-input error must NAME the empty input set")
        self.assertIn("some-check", msg, "the vacuous-input error must NAME the check")

    def test_shape_passes_a_nonempty_input(self):
        mod = self._import_shape()
        out = mod.require_nonempty("some-check", "the widget set", ["a", "b"])
        self.assertEqual(list(out), ["a", "b"])


class TestIndexProseSubstance(unittest.TestCase):
    """The substantive arm on the real tree, re-aimed at the requirements format (SPEC INV-271): the
    generated index carries locations only, and every code it lists is carried by a body criterion —
    the successor of "every index code has a home", now keyed to criteria rather than prose. The
    committed index lives at PRODUCT_SPEC.index.md and is embedded in the spec's `## Reference`."""

    def test_every_index_code_has_a_body_home(self):
        spec = read("PRODUCT_SPEC.md")
        index = read("PRODUCT_SPEC.index.md")
        # The body: everything before the closing `## Reference` (the generated table).
        body = spec.split("## Reference", 1)[0]

        def expand(a):
            m = re.match(r"([A-Z]+)-(\d+)\.\.(?:[A-Z]+-)?(\d+)$", a)
            if m:
                p, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
                return ["%s-%d" % (p, i) for i in range(lo, hi + 1)]
            return [a]

        raw = re.findall(r"^\| ([A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?) \|", index, re.M)
        codes = set()
        for a in raw:
            codes.update(expand(a))
        carried = set(re.findall(r"[A-Z]+-[0-9]+", body))
        for rng in re.findall(r"[A-Z]+-[0-9]+\.\.[A-Z]*-?[0-9]+", body):
            carried.update(expand(rng))
        missing = sorted(a for a in codes if a not in carried)
        self.assertEqual(missing, [], "index codes carried by no body criterion: %s" % missing)


class TestTraceability(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = " ".join(read("PRODUCT_SPEC.md").split())
        self.assertIn("[INV-218]", spec)
        # The requirements-format spec states the law, not the implementing script filenames.
        self.assertIn("declare the input set it expects to be non-empty", spec)
        self.assertIn("the default being that empty is a finding", spec)

    def test_formal_index_row(self):
        # lived a second time under the spec's own trailing "## Reference" heading until the spec
        # split removed that inline duplicate (ROADMAP row 621); PRODUCT_SPEC.index.md is its one
        # home now.
        self.assertIn("| INV-218 |", read("PRODUCT_SPEC.index.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-218", arch)
        # INV-218's shared shape is nonempty_input.py; check-index-generated (gate x) uses it.
        self.assertIn("nonempty_input.py", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-218", read("TEST_MATRIX.md"))


if __name__ == "__main__":
    unittest.main()
