"""The generated matrix-Reference gate and its builder (SPEC INV-273, R284; ROADMAP 477).

`scripts/build-matrix-reference.py` builds the Reference table from TEST_MATRIX.md's body rows,
mapping each row's trailing spec anchors (compound anchors and `T-1..T-7` ranges expand) to the row
ids that carry them — output only, committed at TEST_MATRIX.index.md, never hand-written.
`guardrails/check-matrix-reference.py` takes the matrix (a core plus any parts) and the committed
index as its trailing argument — the sibling shape of `check-index-generated.py` — and reds a hand
edit (drift), a body anchor absent from the committed Reference, or a Reference anchor no body row
carries, and on green states its reach. The gate arms in the conversion delivery, so these tests are
green only once TEST_MATRIX.md is converted and the table is generated (red-first before then).

Zero dependencies beyond the stdlib; run from the repo root: python3 -m pytest -q tests
"""
import os
import re
import subprocess
import tempfile
import unittest

from conftest import ROOT, _sf

BUILDER = os.path.join(ROOT, "scripts", "build-matrix-reference.py")
GATE = os.path.join(ROOT, "guardrails", "check-matrix-reference.py")
MATRIX = os.path.join(ROOT, "TEST_MATRIX.md")
MATRIX_INDEX = os.path.join(ROOT, "TEST_MATRIX.index.md")
# A line-anchored `## Reference` heading — never an inline mention in the preamble prose.
REFERENCE_SPLIT_RE = re.compile(r"(?m)^## Reference *$")


def split_reference(text):
    """(body, reference-section) split at the line-anchored `## Reference` heading."""
    parts = REFERENCE_SPLIT_RE.split(text, 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (text, "")


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
    def test_builder_and_gate_ship_executable(self):
        for p in (BUILDER, GATE):
            self.assertTrue(os.path.isfile(p), "missing: %s" % p)
            self.assertTrue(os.access(p, os.X_OK), "not executable: %s" % p)

    def test_builder_refuses_to_overwrite_its_input(self):
        # the build-index.py guard: -o <input> is refused, the builder never overwrites its source.
        r = run(BUILDER, MATRIX, "-o", MATRIX)
        self.assertNotEqual(r.returncode, 0, "builder overwrote its own input:\n%s" % r.stdout)
        self.assertIn("never overwrites", r.stdout.lower() + r.stderr.lower())

    def test_builder_expands_ranges_and_compounds(self):
        # a tiny matrix with a compound anchor and a range: both expand to per-code rows.
        mini = (
            "## Matrix rows\n\n"
            "### [node: demo]\n\n"
            "| ID | Fact (from spec) | Test level | Owning test | Status |\n"
            "|---|---|---|---|---|\n"
            "| M-1 | does a thing; never the bad thing [E-3, INV-75] | string | `t_a` | *built* |\n"
            "| M-2 | does another; never worse [T-1..T-3] | string | `t_b` | *todo* |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            doc = write(tmp, "m.md", mini)
            r = run(BUILDER, doc)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            out = r.stdout
            for code in ("E-3", "INV-75", "T-1", "T-2", "T-3"):
                self.assertIn("| %s |" % code, out, "range/compound did not expand to %s:\n%s" % (code, out))
            self.assertIn("M-1", out)
            self.assertIn("M-2", out)


class TestGateOnRealMatrix(unittest.TestCase):
    """Armed on the converted TEST_MATRIX.md — green with its reach line (R284.5, INV-269)."""

    def test_gate_passes_on_the_committed_matrix_with_reach(self):
        r = run(GATE, MATRIX, MATRIX_INDEX)
        self.assertEqual(r.returncode, 0, "the gate red the committed matrix:\n%s" % (r.stdout + r.stderr))
        self.assertIn("reach:", r.stdout)
        self.assertIn("rows scanned", r.stdout)

    def test_committed_reference_equals_a_fresh_build(self):
        committed = read(MATRIX_INDEX)
        fresh = run(BUILDER, MATRIX).stdout
        self.assertEqual(committed.strip(), fresh.strip(),
                         "the committed Reference differs from a fresh build — it is generated output")


class TestGateReds(unittest.TestCase):
    """The three faults, each red-proven off a mutated copy of the real matrix and its committed
    index, the sibling shape of test_index_generated.py's fault tests."""

    def _matrix_parts(self):
        # The real matrix is a core plus the parts its own `## Parts map` names (TEST_MATRIX.md
        # today), so reading it the way every other caller does means joining core and parts into
        # one text through the shared spec_paths()/read_document() the gate itself uses. Neither the
        # core nor a part carries an embedded `## Reference` any more — that section lives once, at
        # the committed TEST_MATRIX.index.md — so there is nothing left to split off here.
        #
        # These red tests write `body` back out as a single, standalone TEST_MATRIX.md with no
        # sibling parts on disk, so the joined text must carry no `## Parts map` of its own — a
        # written-back copy that still named `matrix/*.md` would send the gate looking for parts
        # that were never written beside it. The map, and the preamble bytes it replaces in the
        # core, are cut out here; the node blocks that follow are unaffected by the cut.
        _, joined = _sf.read_document([MATRIX])
        self.assertFalse(REFERENCE_SPLIT_RE.search(joined),
                         "the joined matrix body still carries an embedded ## Reference section")
        pm_start = joined.index("## Parts map")
        node_start = joined.index("### [node:")
        body = joined[:pm_start] + joined[node_start:]
        index = read(MATRIX_INDEX)
        return body, index

    def test_reds_a_hand_edited_reference(self):
        # DRIFT (INV-273): a committed Reference with an extra hand-added row differs from a fresh build.
        body, index = self._matrix_parts()
        drifted = index.rstrip() + "\n| ZZ-999 | M-000 |\n"
        with tempfile.TemporaryDirectory() as tmp:
            m = write(tmp, "TEST_MATRIX.md", body)
            idx = write(tmp, "TEST_MATRIX.index.md", drifted)
            r = run(GATE, m, idx)
            self.assertNotEqual(r.returncode, 0, "passed a hand-edited Reference:\n%s" % r.stdout)
            self.assertIn("INV-273", r.stdout)

    def test_reds_a_body_anchor_missing_from_the_reference(self):
        # a committed Reference with one anchor row deleted — a body anchor the table now misses.
        body, index = self._matrix_parts()
        lines = index.splitlines()
        # drop the first real anchor row of the table (a `| CODE | ... |` line after the separator)
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
            m = write(tmp, "TEST_MATRIX.md", body)
            idx = write(tmp, "TEST_MATRIX.index.md", mutated)
            r = run(GATE, m, idx)
            self.assertNotEqual(r.returncode, 0, "passed a missing body anchor:\n%s" % r.stdout)
            self.assertIn(anchor, r.stdout, "the gate did not name the missing anchor %s" % anchor)

    def test_reds_a_reference_anchor_no_body_row_carries(self):
        # a committed Reference with an anchor row for a code no body row carries — an empty home.
        body, index = self._matrix_parts()
        orphaned = index.rstrip() + "\n| INV-9999 | M-000 |\n"
        with tempfile.TemporaryDirectory() as tmp:
            m = write(tmp, "TEST_MATRIX.md", body)
            idx = write(tmp, "TEST_MATRIX.index.md", orphaned)
            r = run(GATE, m, idx)
            self.assertNotEqual(r.returncode, 0, "passed an orphan Reference anchor:\n%s" % r.stdout)
            self.assertIn("INV-9999", r.stdout)

    def test_reds_an_empty_body_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = write(tmp, "TEST_MATRIX.md", "# X\n\n## Matrix rows\n\nno rows here\n")
            idx = write(tmp, "TEST_MATRIX.index.md", "| Anchor | Rows |\n|---|---|\n")
            r = run(GATE, m, idx)
            self.assertNotEqual(r.returncode, 0, "passed an empty body:\n%s" % r.stdout)
            self.assertIn("EMPTY", (r.stdout + r.stderr).upper())


class TestGateWiredAsGateD(unittest.TestCase):
    def test_gate_wired_into_pre_push_keeping_letter_d(self):
        body = read(os.path.join(ROOT, "guardrails", "pre-push"))
        self.assertIn("check-matrix-reference.py", body,
                      "pre-push does not wire in the matrix-reference gate")
        self.assertIn("-- gate d:", body, "gate d marker lost from pre-push")
        self.assertNotIn("check-matrix-coverage.sh", body,
                         "the retired checkbox gate is still wired into pre-push")

    def test_gate_mirrored_in_ci(self):
        yml = read(os.path.join(ROOT, ".github", "workflows", "gates.yml"))
        self.assertIn("check-matrix-reference.py", yml, "CI mirror missing the matrix-reference gate")

    def test_gate_d_red_proof_registered(self):
        import json
        reg = json.loads(read(os.path.join(ROOT, "guardrails", "gate-red-proofs.json")))
        entry = reg["proofs"].get("d")
        self.assertIsNotNone(entry, "gate d carries no red proof")
        self.assertIn("test_matrix_reference.py", entry["proof"],
                      "gate d's red proof no longer points at test_matrix_reference.py")
        self.assertEqual(entry["reds"], "check-matrix-reference",
                         "gate d's reds token no longer names the matrix-reference gate")


if __name__ == "__main__":
    unittest.main()
