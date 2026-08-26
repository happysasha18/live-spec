"""The generated architecture-Reference gate and its builder (SPEC INV-315, R312).

`scripts/build-architecture-reference.py` builds the Reference table from ARCHITECTURE.md's node
sections, reading each node's `owns` field through the shared reader `guardrails/archformat.py`
(INV-280's one-reader law) and mapping every anchor it names (a range such as `INV-250..INV-265`
expanded to its members) to the node names that own it — output only, committed at
ARCHITECTURE.index.md, never hand-written.
`guardrails/check-architecture-reference.py` takes the architecture file and the committed index as its
trailing argument — the sibling shape of `check-matrix-reference.py` (gate d) and
`check-index-generated.py` (gate x) — and reds a hand edit (drift), an owns anchor absent from the
committed Reference, or a Reference anchor owned by no node, and on green states its reach.

Zero dependencies beyond the stdlib; run from the repo root: python3 -m pytest -q tests
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

BUILDER = os.path.join(ROOT, "scripts", "build-architecture-reference.py")
GATE = os.path.join(ROOT, "guardrails", "check-architecture-reference.py")
ARCH = os.path.join(ROOT, "ARCHITECTURE.md")
ARCH_INDEX = os.path.join(ROOT, "ARCHITECTURE.index.md")

# A tiny architecture document: two node sections, a compound owns cell and a range owns cell, so the
# builder's range/compound expansion is exercised the same way test_matrix_reference.py exercises it.
MINI = (
    "# Mini architecture\n\n"
    "This is how mini is built.\n\n"
    "### [node: alpha]\n\n"
    "**responsibility** — does the alpha things\n\n"
    "**owns** —\n"
    "- E-3, INV-75\n\n"
    "**pins** —\n"
    "- `alpha.py:1`\n\n"
    "### [node: beta]\n\n"
    "**responsibility** — does the beta things\n\n"
    "**owns** —\n"
    "- T-1..T-3\n\n"
    "**pins** —\n"
    "- `beta.py:1`\n\n"
    "## Seams\n\n"
    "alpha talks to beta.\n"
)


def run(script, *args):
    return subprocess.run(["python3", script, *args], capture_output=True, text=True)


def write(tmp, name, text):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class TestBuilderShips(unittest.TestCase):
    def test_builder_refuses_to_overwrite_its_input(self):
        # the build-index.py guard: -o <input> is refused, the builder never overwrites its source.
        r = run(BUILDER, ARCH, "-o", ARCH)
        self.assertNotEqual(r.returncode, 0, "builder overwrote its own input:\n%s" % r.stdout)
        self.assertIn("never overwrites", r.stdout.lower())

    def test_builder_expands_ranges_and_compounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "a.md", MINI)
            r = run(BUILDER, doc)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            out = r.stdout
            self.assertIn("| E-3 | alpha |", out)
            self.assertIn("| INV-75 | alpha |", out)
            for code in ("T-1", "T-2", "T-3"):
                self.assertIn("| %s | beta |" % code, out, "range did not expand to %s:\n%s" % (code, out))

    def test_build_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "a.md", MINI)
            self.assertEqual(run(BUILDER, doc).stdout, run(BUILDER, doc).stdout,
                             "the builder is not deterministic on one input")

    def test_builder_reds_an_empty_body_by_name(self):
        # INV-218: a document that parses to zero node sections reds rather than building over nothing.
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "a.md", "# Empty\n\nNo nodes here, just prose.\n")
            r = run(BUILDER, doc)
            self.assertNotEqual(r.returncode, 0, "built over an empty document:\n%s" % r.stdout)
            self.assertIn("EMPTY", r.stdout.upper())

    def test_builder_refuses_the_retired_table_shape(self):
        old = ("## Nodes\n\n"
               "| Node | Responsibility (one line) | Owns spec facts (anchors) | Pinned to (file:line) |\n"
               "|---|---|---|---|\n"
               "| alpha | does things | E-3 | `alpha.py:1` |\n")
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "a.md", old)
            r = run(BUILDER, doc)
            self.assertNotEqual(r.returncode, 0, "built over the retired table shape:\n%s" % r.stdout)
            self.assertIn("retired", r.stdout.lower())


class TestGateOnRealArchitecture(unittest.TestCase):
    """Green with its reach line (R312.4, INV-269)."""

    def test_gate_passes_on_the_committed_architecture_with_reach(self):
        r = run(GATE, ARCH, ARCH_INDEX)
        self.assertEqual(r.returncode, 0, "the gate red the committed architecture:\n%s" % (r.stdout + r.stderr))
        self.assertIn("reach:", r.stdout)
        self.assertIn("rows scanned", r.stdout)

    def test_committed_reference_equals_a_fresh_build(self):
        committed = read(ARCH_INDEX)
        fresh = run(BUILDER, ARCH).stdout
        self.assertEqual(committed.strip(), fresh.strip(),
                         "the committed Reference differs from a fresh build — it is generated output")


class TestGateReds(unittest.TestCase):
    """The three faults, each red-proven off a mutated copy of the real architecture and its committed
    index, the sibling shape of test_matrix_reference.py's fault tests."""

    def test_reds_a_hand_edited_reference(self):
        # DRIFT (INV-315): a committed Reference with an extra hand-added row differs from a fresh build.
        index = read(ARCH_INDEX)
        drifted = index.rstrip() + "\n| ZZ-999 | nowhere |\n"
        with tempfile.TemporaryDirectory() as tmp:
            idx = write(tmp, "ARCHITECTURE.index.md", drifted)
            r = run(GATE, ARCH, idx)
            self.assertNotEqual(r.returncode, 0, "passed a hand-edited Reference:\n%s" % r.stdout)
            self.assertIn("INV-315", r.stdout)

    def test_reds_an_owns_anchor_missing_from_the_reference(self):
        index = read(ARCH_INDEX)
        lines = index.splitlines()
        dropped = None
        out = []
        for l in lines:
            s = l.strip()
            if (dropped is None and s.startswith("|") and not s.startswith("|---")
                    and "Anchor" not in s):
                dropped = s
                continue
            out.append(l)
        self.assertIsNotNone(dropped, "found no anchor row to drop")
        anchor = dropped.strip("|").split("|")[0].strip()
        mutated = "\n".join(out)
        with tempfile.TemporaryDirectory() as tmp:
            idx = write(tmp, "ARCHITECTURE.index.md", mutated)
            r = run(GATE, ARCH, idx)
            self.assertNotEqual(r.returncode, 0, "passed a missing owns anchor:\n%s" % r.stdout)
            self.assertIn(anchor, r.stdout, "the gate did not name the missing anchor %s" % anchor)

    def test_reds_a_reference_anchor_no_node_owns(self):
        index = read(ARCH_INDEX)
        orphaned = index.rstrip() + "\n| INV-9999 | nowhere |\n"
        with tempfile.TemporaryDirectory() as tmp:
            idx = write(tmp, "ARCHITECTURE.index.md", orphaned)
            r = run(GATE, ARCH, idx)
            self.assertNotEqual(r.returncode, 0, "passed an orphan Reference anchor:\n%s" % r.stdout)
            self.assertIn("INV-9999", r.stdout)

    def test_reds_an_empty_body_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = write(tmp, "ARCHITECTURE.md", "# Empty\n\nNo nodes here.\n")
            idx = write(tmp, "ARCHITECTURE.index.md", "| Anchor | Nodes |\n|---|---|\n")
            r = run(GATE, a, idx)
            self.assertNotEqual(r.returncode, 0, "passed an empty body:\n%s" % r.stdout)
            self.assertIn("EMPTY", (r.stdout + r.stderr).upper())

    def test_gate_usage_error_exits_two(self):
        r = run(GATE, ARCH)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)


class TestGateWiredAsGateZ(unittest.TestCase):
    def test_gate_wired_into_pre_push(self):
        body = read(os.path.join(ROOT, "guardrails", "pre-push"))
        self.assertIn("check-architecture-reference.py", body,
                      "pre-push does not wire in the architecture-reference gate")
        self.assertIn("-- gate z:", body, "gate z marker missing from pre-push")

    def test_gate_mirrored_in_ci(self):
        yml = read(os.path.join(ROOT, ".github", "workflows", "gates.yml"))
        self.assertIn("check-architecture-reference.py", yml, "CI mirror missing the architecture-reference gate")

    def test_gate_documented_in_readme(self):
        readme = read(os.path.join(ROOT, "guardrails", "README.md"))
        self.assertIn("gate z", readme, "guardrails/README.md does not document gate z")
        self.assertIn("check-architecture-reference", readme + read(os.path.join(ROOT, "guardrails", "pre-push")),
                      "no surviving mention of the architecture-reference gate script")


if __name__ == "__main__":
    unittest.main()
