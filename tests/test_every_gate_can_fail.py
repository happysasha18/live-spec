"""INV-212 — every gate carries a known-red proof (gate w, ROADMAP 420 candidate 3).

A gate reports green two ways: because the input was clean, or because the check never fires at
all. The second is the hollow gate this movement had to rebuild — the authority-anchor gate shipped
green without reaching the surfaces it claimed to inspect (commit 8a0209f), and a worker's false
"zero violations" was the same disease. So every gate the push chain runs carries a known-red proof:
a committed red-first test that drives that gate's own check to a non-zero exit.

guardrails/check-every-gate-can-fail.py (gate w) enumerates the `-- gate X:` markers pre-push invokes
(the enumeration gate u reads) and requires each classified in guardrails/gate-red-proofs.json — a
`proof` (a red-first test `<file>::<function>` that reds the gate's check, tied by a `reds` token the
proof file references, verified by structure since the suite runs it under gate b) or a `covered`
gate that runs no independent check and rides another gate's red (gate c rides the suite, gate b). An
unclassified gate, a hollow proof, a reasonless covered, a cannot_red gate, or a stale registry key
each reds.
"""
import json
import os
import re
import subprocess
import tempfile
import unittest

from conftest import read_flat

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "guardrails", "check-every-gate-can-fail.py")
REGISTRY = os.path.join(REPO, "guardrails", "gate-red-proofs.json")
PREPUSH = os.path.join(REPO, "guardrails", "pre-push")


def read(rel):
    with open(os.path.join(REPO, rel)) as f:
        return f.read()


def run_check(env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["python3", CHECK], cwd=REPO, capture_output=True, text=True, env=env)


def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def write_registry(data):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


class TestEveryGateCanFail(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK), "the meta-gate script must ship")
        self.assertTrue(os.access(CHECK, os.X_OK), "the meta-gate must be executable")

    def test_registry_ships_and_parses(self):
        data = load_registry()
        for key in ("proofs", "covered", "cannot_red"):
            self.assertIn(key, data, "registry missing section %s" % key)
        # every covered entry states a non-empty reason so the line is settled, not papered
        for letter, reason in data["covered"].items():
            self.assertTrue(str(reason).strip(), "covered gate %s carries no reason" % letter)

    def test_real_chain_is_compliant(self):
        # the compliance proof: run the meta-gate against the real pre-push + real registry.
        r = run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_gate_marker_is_classified(self):
        # self-widening teeth: every `-- gate X:` marker pre-push invokes has a registry home.
        letters = set(re.findall(r"-- gate ([a-z]):", read("guardrails/pre-push")))
        data = load_registry()
        classified = set(data["proofs"]) | set(data["covered"]) | set(data["cannot_red"])
        self.assertTrue(letters, "no gate markers parsed from pre-push")
        self.assertEqual(letters - classified, set(),
                         "gate markers with no registry home: %s" % (letters - classified))

    def test_registered_proofs_exist(self):
        # every registered proof names a real file, a real function, and its reds token appears there
        data = load_registry()
        for letter, entry in data["proofs"].items():
            proof = entry["proof"]
            self.assertIn("::", proof, "gate %s proof is not file::function: %s" % (letter, proof))
            relfile, fn = proof.split("::", 1)
            self.assertTrue(os.path.isfile(os.path.join(REPO, relfile)),
                            "gate %s proof file missing: %s" % (letter, relfile))
            src = read(relfile)
            self.assertRegex(src, r"\bdef " + re.escape(fn) + r"\b",
                             "gate %s proof function %s not defined in %s" % (letter, fn, relfile))
            self.assertIn(entry["reds"], src,
                          "gate %s reds token %r absent from %s" % (letter, entry["reds"], relfile))

    # --- the red-proofs: the meta-gate must itself be able to fire ---

    def test_missing_proof_reds(self):
        # a gate marker classified in no section reds the meta-gate, naming it.
        # (this is also gate w's own registered red-proof — it drives check-every-gate-can-fail.py to red)
        data = load_registry()
        data["proofs"].pop("a", None)
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate a", r.stdout)
        finally:
            os.unlink(fixture)

    def test_hollow_proof_with_no_red_assertion_reds(self):
        # a proof that points at a real function carrying no non-zero-exit assertion (a bare
        # "the gate ships" presence test) must red — the exact hollow-gate disease this guards.
        data = load_registry()
        data["proofs"]["a"] = {
            "proof": "tests/test_guardrails.py::test_clean_fixture_passes",
            "reds": "check-prover-record.sh",
        }
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate a", r.stdout)
        finally:
            os.unlink(fixture)

    def test_proof_missing_reds_token_reds(self):
        # a proof whose reds token does not appear in the proof file is not tied to this gate's
        # check, so the meta-gate cannot know the test drives the right gate — it reds.
        data = load_registry()
        entry = dict(data["proofs"]["a"])
        entry["reds"] = "no-such-token-anywhere.sh"
        data["proofs"]["a"] = entry
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate a", r.stdout)
        finally:
            os.unlink(fixture)

    def test_reasonless_covered_reds(self):
        # a covered entry with an empty reason papers over a gate — it reds.
        data = load_registry()
        data["covered"]["c"] = ""
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate c", r.stdout)
        finally:
            os.unlink(fixture)

    def test_cannot_red_entry_reds(self):
        # a gate declared cannot_red guards nothing by construction — a finding, so it reds loudly.
        data = load_registry()
        data["proofs"].pop("a", None)
        data["cannot_red"]["a"] = "suppose gate a could never be made to fail"
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate a", r.stdout)
        finally:
            os.unlink(fixture)

    def test_stale_registry_key_reds(self):
        # a registry key naming a letter that is no local gate is itself drift and reds.
        data = load_registry()
        data["proofs"]["z"] = {"proof": "tests/test_x.py::test_x", "reds": "nope"}
        fixture = write_registry(data)
        try:
            r = run_check({"GATE_PROOFS_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("z", r.stdout)
        finally:
            os.unlink(fixture)

    # --- wiring + traceability across the four documents ---

    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-every-gate-can-fail.py", read("guardrails/pre-push"))

    def test_gate_mirrored_in_ci(self):
        # gate w reads only repo files, so it runs in CI (no carve-out) and represents itself there
        self.assertIn("check-every-gate-can-fail.py", read(".github/workflows/gates.yml"))

    def test_spec_states_the_law(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-212]", spec)
        # The requirements-format spec states the law, not the implementing script/data filenames.
        self.assertIn("each pushed gate letter to be classified with a red-first proof", spec)
        self.assertIn("a gate can by construction never be made to fail", spec)

    def test_formal_index_row(self):
        self.assertIn("| INV-212 |", read("PRODUCT_SPEC.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-212", arch)
        self.assertIn("check-every-gate-can-fail.py", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-212", read("TEST_MATRIX.md"))


if __name__ == "__main__":
    unittest.main()
