"""Node growth — a node's fitness is re-answered as it grows, and node co-residence in one file is
the counted signal (SPEC INV-233, ROADMAP row 390, the growth-law family).

The three-question fitness test [INV-122] governs a node's BIRTH; a node born right and then grown
carries a standing yes nobody re-reads. So co-residence — two nodes whose pins share one file — is the
mechanical face of a failed growth answer, read from the architecture's own pin column. The counter
`guardrails/node_growth_counter.py` reads nodes-per-file and reds any file that rose past its ratchet;
the ratchet `guardrails/node-file-cap.json` is seeded at the tree's current count so the tree lands green,
standing debt flagged, and ratchets DOWN only [INV-164's lesson transfers whole].

This ratchet RIDES THE SUITE (like the prose-debt cap, tests/test_convergence_locks.py) — it takes no
push-gate letter, so these tests assert it is NOT wired into the push chain. Two prose homes carry the
law's review duties: product-prover's seventh architecture lens (the growth re-ask) and the
design-reviewer's split-proposal shape.

Red-first: run against the pre-delta tree and the counter/cap are absent, the prover carries no seventh
lens, the design review no split-proposal shape, and spec/index/architecture/matrix carry no INV-233.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from conftest import external_clone_or_skip, read

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COUNTER = os.path.join(ROOT, "guardrails", "node_growth_counter.py")
CAP = os.path.join(ROOT, "guardrails", "node-file-cap.json")

# The reached-ceiling floor, pinned HERE (the debt-cap discipline, tests/test_convergence_locks.py):
# raising a cap above its reached value means editing this dict — a deliberate, visible act named in the
# landing, never a quiet json touch. Seeded at the 2026-07-18 tree (three SKILL.md files carry three
# nodes each through design-sync / parallel-lanes wiring pins; every other file two or fewer).
REACHED_CEILING = {
    "skills/live-spec-base/SKILL.md": 3,
    "skills/communicator/SKILL.md": 3,
    "skills/build-pipeline/SKILL.md": 3,
}
PROPOSED_DEFAULT = 2  # two nodes per code file (the host's word sets it, INV-41)


def run_counter(architecture_path, cap_path):
    p = subprocess.run(
        [sys.executable, COUNTER, "--architecture", architecture_path, "--cap", cap_path],
        capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# A minimal architecture fixture: node sections (guardrails/archformat.py) with a pins field the
# counter reads.
def _arch(rows):
    head = "# Fixture architecture\n\n## Nodes\n\n"
    body = "".join(rows)
    tail = "\n## Seams\n\n| From | To | Carries |\n|---|---|---|\n| a | b | x |\n"
    return head + body + tail


def _row(node, pins):
    return ("### [node: %s]\n"
            "**responsibility** — does one thing\n"
            "**owns** — E-1\n"
            "**pins** — %s\n\n" % (node, pins))


class TestNodeGrowthMechanism(unittest.TestCase):
    def test_counter_ships(self):
        self.assertTrue(os.path.isfile(COUNTER), "guardrails/node_growth_counter.py must ship")

    def test_cap_config_ships(self):
        self.assertTrue(os.path.isfile(CAP), "guardrails/node-file-cap.json must ship")
        cfg = json.load(open(CAP))
        self.assertIn("default", cfg)
        self.assertIn("caps", cfg)

    def test_live_architecture_within_caps(self):
        """The watcher passes on the real tree — the ratchet is seeded at the current count so the
        tree lands green (INV-164's lesson transfers whole)."""
        code, out = run_counter(os.path.join(ROOT, "ARCHITECTURE.md"), CAP)
        self.assertEqual(code, 0, "the real architecture must sit within its seeded ratchet:\n" + out)

    def test_counter_reds_a_file_over_its_ratchet(self):
        """Red-prove: a fixture file whose node count rose past its ratchet reds (non-zero exit)."""
        with tempfile.TemporaryDirectory() as tmp:
            arch = os.path.join(tmp, "ARCHITECTURE.md")
            # three distinct nodes co-residing in one file — past the default ratchet of two.
            with open(arch, "w", encoding="utf-8") as f:
                f.write(_arch([
                    _row("alpha", "`engine/big.py:1`"),
                    _row("beta", "`engine/big.py:40`"),
                    _row("gamma", "`engine/big.py:80`"),
                ]))
            cap = os.path.join(tmp, "cap.json")
            json.dump({"default": 2, "caps": {}}, open(cap, "w"))
            code, out = run_counter(arch, cap)
            self.assertNotEqual(code, 0, "a file over its ratchet must red:\n" + out)
            self.assertIn("engine/big.py", out)

    def test_counter_passes_a_file_at_or_below_its_ratchet(self):
        """A count at or below the ratchet passes (zero exit) — the other half of the red-prove."""
        with tempfile.TemporaryDirectory() as tmp:
            arch = os.path.join(tmp, "ARCHITECTURE.md")
            with open(arch, "w", encoding="utf-8") as f:
                f.write(_arch([
                    _row("alpha", "`engine/big.py:1`"),
                    _row("beta", "`engine/big.py:40`"),
                ]))
            cap = os.path.join(tmp, "cap.json")
            json.dump({"default": 2, "caps": {}}, open(cap, "w"))
            code, out = run_counter(arch, cap)
            self.assertEqual(code, 0, "a file at its ratchet must pass:\n" + out)

    def test_a_seeded_cap_admits_standing_debt_but_reds_growth(self):
        """A file seeded at three passes at three and reds at four — the ratchet admits standing debt
        yet reds any INCREASE past it."""
        with tempfile.TemporaryDirectory() as tmp:
            cap = os.path.join(tmp, "cap.json")
            json.dump({"default": 2, "caps": {"engine/big.py": 3}}, open(cap, "w"))
            arch3 = os.path.join(tmp, "a3.md")
            with open(arch3, "w", encoding="utf-8") as f:
                f.write(_arch([_row("a", "`engine/big.py:1`"), _row("b", "`engine/big.py:2`"),
                               _row("c", "`engine/big.py:3`")]))
            self.assertEqual(run_counter(arch3, cap)[0], 0, "seeded standing debt must pass")
            arch4 = os.path.join(tmp, "a4.md")
            with open(arch4, "w", encoding="utf-8") as f:
                f.write(_arch([_row("a", "`engine/big.py:1`"), _row("b", "`engine/big.py:2`"),
                               _row("c", "`engine/big.py:3`"), _row("d", "`engine/big.py:4`")]))
            self.assertNotEqual(run_counter(arch4, cap)[0], 0, "growth past the seeded ratchet must red")

    def test_cap_ratchets_down_only(self):
        """The lock: every cap in the config sits at or below its reached-ceiling floor, and the
        default sits at or below the proposed two. Raising a cap means editing REACHED_CEILING here."""
        cfg = json.load(open(CAP))
        self.assertLessEqual(cfg["default"], PROPOSED_DEFAULT,
                             "the default nodes-per-file was raised above the proposed two")
        for f, allowed in cfg["caps"].items():
            self.assertIn(f, REACHED_CEILING,
                          "a cap entry %s names no reached-ceiling floor — a cap must be seeded at a "
                          "real current count, pinned in REACHED_CEILING" % f)
            self.assertLessEqual(allowed, REACHED_CEILING[f],
                                 "cap for %s (%d) rose above its reached ceiling (%d) — the ratchet "
                                 "only tightens" % (f, allowed, REACHED_CEILING[f]))

    def test_rides_the_suite_not_the_push_chain(self):
        """The node-growth ratchet takes no push-gate letter — it rides the suite like the debt cap."""
        prepush = read("guardrails/pre-push")
        self.assertNotIn("node_growth_counter", prepush,
                         "the node-growth counter must NOT be wired into the push chain — it rides the "
                         "suite (this test)")
        gates = read(".github/workflows/gates.yml")
        self.assertNotIn("node_growth_counter", gates,
                         "the node-growth counter must not be a CI gate step — it rides the suite")


class TestNodeGrowthReviewDuties(unittest.TestCase):
    def test_product_prover_carries_the_seventh_lens(self):
        """The prover's architecture lens grows a seventh check — the node-growth re-ask (INV-233).

        The externalized canon describes the check in words with no project codes; the pack
        adapter's pin map carries the INV-233 anchor for it."""
        pack = read("skills/product-prover-pack/SKILL.md")
        self.assertIn("INV-233", pack,
                      "the pack adapter must pin INV-233 to the node-growth re-ask")
        external_clone_or_skip()
        prover = read("skills/product-prover/SKILL.md")
        self.assertRegex(prover.lower(), r"node[- ]growth|co-residen|re-ask",
                         "the seventh lens must be described in words, not only cited")

    def test_design_reviewer_carries_the_split_proposal_shape(self):
        """The design review carries the split-proposal shape in its two-objects form (INV-233)."""
        dr = read("skills/design-reviewer/SKILL.md")
        self.assertIn("INV-233", dr,
                      "design-reviewer must state the split-proposal shape for an over-grown file")
        self.assertRegex(dr.lower(), r"split",
                         "the split-proposal shape must be described in words, not only cited")


class TestNodeGrowthDocs(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = read("PRODUCT_SPEC.md")
        self.assertIn("INV-233", spec)
        self.assertRegex(spec, r"node[- ]growth|co-residen|nodes-per-file|node co-residence",
                         "the spec prose must state the node-growth law")

    def test_formal_index_row(self):
        spec = read("PRODUCT_SPEC.md")
        self.assertRegex(spec, r"\| INV-233 \|", "INV-233 must have a Formal-index row")

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-233", arch, "some node's owns-list must carry INV-233")

    def test_matrix_row_covers_the_law(self):
        matrix = read("TEST_MATRIX.md")
        self.assertIn("INV-233", matrix)
        self.assertRegex(matrix, r"\| M-414 \|", "M-414 must cover INV-233")


if __name__ == "__main__":
    unittest.main()
