"""Growable-artifact bound — every growable working doc declares the number that bounds it and the
watcher that reads it (SPEC INV-234, ROADMAP row 392, the growth-law family).

INV-41 states the shape: a budget plus the watcher that reds past it. This lifts it to every growable
artifact: the four large working docs (PRODUCT_SPEC.md, ROADMAP.md, TEST_MATRIX.md, JOURNAL.md) each
declare a byte ceiling with a recorded reason in `guardrails/doc-bounds.json`, and the watcher
`guardrails/check-doc-bound.py` (gate z, in the push chain) reds a doc past its bound with no fresh
rotation and no raised bound. It COMPOSES with the doc-rotation gate (gate t, INV-209): crossing the
bound earns a rotation, and the rotation is the remedy the red points to — a doc rotated today passes.

Caution held: each declared bound sits ABOVE the current file, so this very push does not red on the four
already-large docs; the ratchet points down (rotation resets the live file well under the ceiling).

Red-first: run against the pre-delta tree and the watcher and its bounds file are absent, the push chain
unwired, and spec/index/architecture/matrix carry no INV-234.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-doc-bound.py")
BOUNDS = os.path.join(ROOT, "guardrails", "doc-bounds.json")
FOUR_DOCS = ["PRODUCT_SPEC.md", "ROADMAP.md", "TEST_MATRIX.md", "JOURNAL.md"]


def run_gate(base, bounds_path, today=None):
    cmd = [sys.executable, GATE, "--base", base, "--bounds", bounds_path]
    if today:
        cmd += ["--today", today]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _write(path, nbytes):
    with open(path, "w", encoding="utf-8") as f:
        f.write("x" * nbytes)


ROTATED_MANIFEST = (
    "<!-- rotated-manifest -->\n"
    "Rotated closed rows (base rule 10 — nothing lost):\n"
    "- rows 14, 27 -> docs/queue-archive/rotated-BIG-{date}.md\n"
    "<!-- /rotated-manifest -->\n"
)


class TestDocBoundMechanism(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE), "guardrails/check-doc-bound.py must ship")

    def test_bounds_config_declares_the_four_docs(self):
        self.assertTrue(os.path.isfile(BOUNDS), "guardrails/doc-bounds.json must ship")
        cfg = json.load(open(BOUNDS))
        for d in FOUR_DOCS:
            self.assertIn(d, cfg["docs"], "the growable-doc bound must declare %s" % d)
            self.assertIn("max_bytes", cfg["docs"][d])

    def test_gate_passes_the_real_tree(self):
        """The caution, verified: the four already-large docs sit within their declared bounds, so
        this push does not red on them."""
        code, out = run_gate(ROOT, BOUNDS)
        self.assertEqual(code, 0, "the real tree must pass gate z — a bound below a live doc would "
                                  "block every push:\n" + out)

    def test_each_bound_is_above_the_current_file(self):
        """Each declared ceiling sits above the current byte size (with rotation headroom)."""
        cfg = json.load(open(BOUNDS))
        for d in FOUR_DOCS:
            cur = os.path.getsize(os.path.join(ROOT, d))
            bound = cfg["docs"][d]["max_bytes"]
            self.assertGreater(bound, cur,
                               "%s bound %d is not above its current size %d" % (d, bound, cur))

    def test_each_bound_carries_a_recorded_reason(self):
        """A bound rises only with a recorded reason — every declared bound carries a non-empty one."""
        cfg = json.load(open(BOUNDS))
        for d, entry in cfg["docs"].items():
            self.assertTrue(entry.get("reason", "").strip(),
                            "%s bound carries no recorded reason" % d)

    def test_gate_reds_a_doc_over_its_bound(self):
        """Red-prove (the gate-red proof, check-doc-bound): a doc over its bound with no rotation reds."""
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "BIG.md"), 5000)
            bounds = os.path.join(tmp, "b.json")
            json.dump({"docs": {"BIG.md": {"max_bytes": 1000, "reason": "seed"}}}, open(bounds, "w"))
            code, out = run_gate(tmp, bounds)
            self.assertNotEqual(code, 0, "an over-bound doc with no rotation must red:\n" + out)
            self.assertIn("BIG.md", out)

    def test_gate_passes_a_doc_within_its_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "BIG.md"), 500)
            bounds = os.path.join(tmp, "b.json")
            json.dump({"docs": {"BIG.md": {"max_bytes": 1000, "reason": "seed"}}}, open(bounds, "w"))
            code, out = run_gate(tmp, bounds)
            self.assertEqual(code, 0, "a within-bound doc must pass:\n" + out)

    def test_gate_passes_a_freshly_rotated_doc(self):
        """Composition with INV-209: a doc over its bound but freshly rotated today passes — the
        rotation is the remedy the bound points to."""
        with tempfile.TemporaryDirectory() as tmp:
            manifest = ROTATED_MANIFEST.format(date="2026-07-18")
            body = manifest + ("y" * 5000)
            with open(os.path.join(tmp, "BIG.md"), "w", encoding="utf-8") as f:
                f.write(body)
            bounds = os.path.join(tmp, "b.json")
            json.dump({"docs": {"BIG.md": {"max_bytes": 1000, "reason": "seed"}}}, open(bounds, "w"))
            code, out = run_gate(tmp, bounds, today="2026-07-18")
            self.assertEqual(code, 0, "a doc rotated today must pass even over its bound:\n" + out)

    def test_gate_reds_an_over_bound_doc_with_a_stale_rotation(self):
        """A rotation from another day is not the remedy for today's overflow — still reds."""
        with tempfile.TemporaryDirectory() as tmp:
            manifest = ROTATED_MANIFEST.format(date="2026-06-01")
            body = manifest + ("y" * 5000)
            with open(os.path.join(tmp, "BIG.md"), "w", encoding="utf-8") as f:
                f.write(body)
            bounds = os.path.join(tmp, "b.json")
            json.dump({"docs": {"BIG.md": {"max_bytes": 1000, "reason": "seed"}}}, open(bounds, "w"))
            code, out = run_gate(tmp, bounds, today="2026-07-18")
            self.assertNotEqual(code, 0, "a stale rotation must not clear a fresh overflow:\n" + out)

    def test_gate_reds_a_bound_with_no_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "BIG.md"), 500)
            bounds = os.path.join(tmp, "b.json")
            json.dump({"docs": {"BIG.md": {"max_bytes": 1000, "reason": ""}}}, open(bounds, "w"))
            code, out = run_gate(tmp, bounds)
            self.assertNotEqual(code, 0, "a bound with no recorded reason must red:\n" + out)


class TestDocBoundWiring(unittest.TestCase):
    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-doc-bound", read("guardrails/pre-push"),
                      "gate z must be wired into guardrails/pre-push")
        self.assertRegex(read("guardrails/pre-push"), r"-- gate z:",
                         "pre-push must carry the -- gate z: marker")

    def test_gate_mirrored_in_ci(self):
        gates = read(".github/workflows/gates.yml")
        self.assertIn("check-doc-bound", gates, "gate z must run in CI")
        self.assertRegex(gates, r"gate z", "gates.yml must name the gate z step")

    def test_gate_registered_in_red_proofs(self):
        proofs = json.load(open(os.path.join(ROOT, "guardrails", "gate-red-proofs.json")))
        self.assertIn("z", proofs["proofs"], "gate z must carry a known-red proof (INV-212)")
        self.assertIn("check-doc-bound", proofs["proofs"]["z"]["reds"])


class TestDocBoundDocs(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = read("PRODUCT_SPEC.md")
        self.assertIn("INV-234", spec)
        self.assertRegex(spec, r"growable|bound|ceiling",
                         "the spec prose must state the growable-artifact bound")

    def test_spec_composes_with_rotation(self):
        """The clause names the composition with INV-209 (the rotation is the remedy)."""
        spec = read("PRODUCT_SPEC.md")
        # R245.3 (the requirements-format criterion for "rotation is the remedy") tags both
        # invariants together directly, rather than INV-209 trailing somewhere before INV-234's
        # own standalone tag as in the old prose-paragraph shape.
        self.assertIn("[INV-234, INV-209]", spec,
                      "the INV-234 clause must name its composition with INV-209")

    def test_formal_index_row(self):
        self.assertRegex(read("PRODUCT_SPEC.md"), r"\| INV-234 \|", "INV-234 must have a Formal-index row")

    def test_architecture_owns_the_invariant(self):
        self.assertIn("INV-234", read("ARCHITECTURE.md"), "some node's owns-list must carry INV-234")

    def test_matrix_row_covers_the_law(self):
        matrix = read("TEST_MATRIX.md")
        self.assertIn("INV-234", matrix)
        self.assertRegex(matrix, r"\| M-415 \|", "M-415 must cover INV-234")


if __name__ == "__main__":
    unittest.main()
