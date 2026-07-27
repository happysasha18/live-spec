"""INV-218 (M-399, ROADMAP 384) — a check that looked at nothing is not a pass.

The vacuous-pass class: a check whose INPUT SET is empty reports clean while testing
nothing, and an empty input set is nearly always the defect. The drafter's own self-catch
minted this row — it scanned its freshly minted codes for collisions, the codes were absent
from the prose entirely, and the scan compared zero against zero and reported clean.

The law (sibling of the unexpected-skip law INV-155): a check DECLARES the input set it
expects to be non-empty, and an empty set REDS BY NAME rather than passing silently. This
movement builds the shared shape (`guardrails/nonempty_input.py`) and applies it to the first
named instance — the traceability index prose check `guardrails/check-index-prose.py`, which
today has no home for the "a Formal-index code whose home prose never carries the anchor"
defect: `test_spec_index_unique_anchors` checks uniqueness alone.

Every check here asserts the SHIPPED files on disk, never a source fragment or a memory of one.
"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDRAILS = os.path.join(REPO, "guardrails")
CHECK = os.path.join(GUARDRAILS, "check-index-prose.py")
SHAPE = os.path.join(GUARDRAILS, "nonempty_input.py")


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


def run_check(env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, CHECK], cwd=REPO, capture_output=True, text=True, env=env)


# A spec fixture whose Formal index carries anchors that ARE present in the prose body — a clean
# tree the gate passes.
CLEAN_SPEC = """# Fixture spec

Some prose that names INV-900 and the transition T-900 in its body. [INV-900]
Another paragraph carrying M-900 in a worked sentence. [M-900]

## Formal index

| anchor | fact | scenario |
|---|---|---|
| INV-900 | a law | A scenario |
| T-900 | a transition | A scenario |
| M-900 | a test | A scenario |
"""

# A spec fixture whose index carries INV-901, absent from every prose line before the index —
# the "index code whose home prose never carries the anchor" defect the gate must red on.
ABSENT_HOME_SPEC = """# Fixture spec

Some prose that names INV-900 in its body. [INV-900]

## Formal index

| anchor | fact | scenario |
|---|---|---|
| INV-900 | a law | A scenario |
| INV-901 | a law with no home | A scenario |
"""

# A spec fixture whose Formal-index section is present but carries NO anchor rows, so the
# index-anchor input set parses EMPTY — the vacuous case the shared shape must red on BY NAME
# rather than pass by looking at nothing.
EMPTY_INDEX_SPEC = """# Fixture spec

Prose with an index header but no rows under it. [INV-900]

## Formal index

| anchor | fact | scenario |
|---|---|---|
"""


def write_spec(tmpdir, text):
    path = os.path.join(tmpdir, "SPEC_FIXTURE.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TestSharedShape(unittest.TestCase):
    """The general guardrail shape: a check declares its expected-non-empty input set."""

    def _import_shape(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("nonempty_input", SHAPE)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_shape_ships(self):
        self.assertTrue(os.path.isfile(SHAPE), "the shared shape is absent: guardrails/nonempty_input.py")

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


class TestIndexProseGate(unittest.TestCase):
    """The retired index-prose gate — `guardrails/check-index-prose.py`: every Formal-index anchor
    is carried in the spec prose (its home), and the index-anchor input set is expected non-empty.
    check-index-generated.py took over gate x at the row-445 conversion (see below); this class
    exercises the retired script's still-shipped fixture red-proofs."""

    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK), "the gate is absent: guardrails/check-index-prose.py")

    def test_gate_reds_on_empty_input(self):
        # The vacuous case: an index that parses to zero anchors reds BY NAME, in place of
        # reporting clean while looking at nothing (the shape's red proof, gate x since retired).
        with tempfile.TemporaryDirectory() as tmp:
            path = write_spec(tmp, EMPTY_INDEX_SPEC)
            r = run_check({"INDEX_PROSE_SPEC": path})
            self.assertNotEqual(r.returncode, 0, "an empty index input set must RED:\n%s\n%s" % (r.stdout, r.stderr))
            self.assertIn("empty", (r.stdout + r.stderr).lower(),
                          "the red must NAME the empty input set, not fail generically")

    def test_gate_reds_an_index_anchor_absent_from_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_spec(tmp, ABSENT_HOME_SPEC)
            r = run_check({"INDEX_PROSE_SPEC": path})
            self.assertNotEqual(r.returncode, 0,
                                "an index anchor absent from prose must RED:\n%s\n%s" % (r.stdout, r.stderr))
            self.assertIn("INV-901", r.stdout + r.stderr,
                          "the red must NAME the index anchor whose home prose is empty")

    def test_gate_passes_a_clean_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_spec(tmp, CLEAN_SPEC)
            r = run_check({"INDEX_PROSE_SPEC": path})
            self.assertEqual(r.returncode, 0, "a clean fixture must pass:\n%s\n%s" % (r.stdout, r.stderr))

    # Gate x on the real tree retired at the row-445 conversion: the requirements format removed the
    # `## Formal index`/prose-carries-code shape check-index-prose parsed (SPEC INV-271). Gate x now
    # runs check-index-generated, whose real-spec pass is proven by
    # tests/test_index_generated.py::TestArmedOnTheRealSpec::test_armed_passes_on_the_real_spec, and
    # whose empty-body red (the INV-218 vacuous-input guard) rides the same nonempty_input.py shape
    # tested by TestSharedShape above. The fixture red-proofs below still exercise check-index-prose
    # (the script still ships) for the shape's historical red direction.

    def test_gate_x_now_runs_the_generated_index(self):
        self.assertIn("check-index-generated.py", read("guardrails/pre-push"))
        self.assertIn("check-index-generated.py", read(".github/workflows/gates.yml"))


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
        self.assertIn("| INV-218 |", read("PRODUCT_SPEC.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-218", arch)
        # INV-218's shared shape is nonempty_input.py; check-index-generated (gate x) uses it.
        self.assertIn("nonempty_input.py", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-218", read("TEST_MATRIX.md"))


if __name__ == "__main__":
    unittest.main()
