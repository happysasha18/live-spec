"""INV-210/INV-212 — the gate device has one home, and a CI mirror step cannot silently restate a
gate's law (gate af).

The push gate's device is written by hand in five places: guardrails/pre-push (letter, script, SPEC
anchor, and the law sentence), .github/workflows/gates.yml (a second, hand-typed copy of the law
sentence), guardrails/gate-red-proofs.json (the red proof), guardrails/ci-mirror.json (the CI
carve-outs), and guardrails/README.md's generated roster (a third copy, built FROM pre-push and so
never independently wrong). Nothing before this gate ever compared the three copies of the law
sentence: guardrails/check-ci-mirror.sh (gate u) compares LETTER SETS only. Gate ad's law sentence
drifted between pre-push and gates.yml for over a month as a direct result — pre-push and the
generated README roster state both arms of the gate ("matches the tree, and the reproduction command
beside it returns the published number"); gates.yml stated only the first ("is built from the tree").

guardrails/gates-manifest.json (built by scripts/gen-gates-manifest.py) is the one join of every
gate's device, read from its four sources with no field typed by hand. guardrails/check-gates-
manifest.py (gate af) runs two arms: ARM ONE holds the committed manifest to a fresh build of that
join (so it can never be hand-edited out of step, the same discipline guardrails/check-tree-counts.py
holds guardrails/tree-counts.json to). ARM TWO holds every gates.yml step whose name reads
`gate X — LAW` to the SAME law pre-push's own `-- gate X: ... --` marker states — the arm that would
have caught gate ad's drift the day it happened.
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import read, read_flat

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "guardrails", "check-gates-manifest.py")
GENERATOR = os.path.join(REPO, "scripts", "gen-gates-manifest.py")
MANIFEST = os.path.join(REPO, "guardrails", "gates-manifest.json")
GATES_YML = os.path.join(REPO, ".github", "workflows", "gates.yml")


def run_check(env_extra=None, root=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    cmd = ["python3", CHECK]
    if root:
        cmd += ["--root", root]
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env=env)


def write_temp(text, suffix):
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


class TestGatesManifest(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK))
        self.assertTrue(os.path.isfile(GENERATOR))

    def test_manifest_ships_and_parses(self):
        with open(MANIFEST) as f:
            data = json.load(f)
        self.assertIn("gates", data)
        self.assertGreaterEqual(len(data["gates"]), 28)

    def test_real_tree_is_compliant(self):
        # the compliance proof: after this row synced seven drifted gates.yml step names to
        # pre-push's own wording, the committed manifest matches a fresh build and every mirrored
        # gate's CI step states the same law pre-push does.
        r = run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_stale_manifest_reds(self):
        # a manifest hand-edited (or left stale after a source changed) must red, naming the gate.
        with open(MANIFEST) as f:
            data = json.load(f)
        data["gates"]["a"]["law"] = "a hand-typed law nobody rebuilt from pre-push"
        fixture = write_temp(json.dumps(data), ".json")
        try:
            r = run_check({"GATES_MANIFEST_FILE": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate a", r.stdout)
        finally:
            os.unlink(fixture)

    def test_ci_step_text_drift_reds(self):
        # THE LIVING FINDING, reproduced directly: diverge one gate's CI step text from pre-push's
        # own wording — exactly the shape gate ad's law sentence actually drifted into ("is built
        # from the tree" against pre-push's fuller "matches the tree, and the reproduction command
        # beside it returns the published number") — and the gate must red, naming the letter and
        # quoting both sides.
        yml = read(".github/workflows/gates.yml")
        drifted = yml.replace(
            "gate ad — published tree counts (every count this repository publishes about its own "
            "tree matches the tree, and the reproduction command beside it returns the published "
            "number, SPEC INV-305)",
            "gate ad — published tree counts (a count this repository publishes about its own tree "
            "is built from the tree, SPEC INV-305)")
        self.assertNotEqual(drifted, yml, "the fixture edit did not match the real gates.yml text")
        fixture = write_temp(drifted, ".yml")
        try:
            r = run_check({"GATES_MANIFEST_GATES_YML": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate ad", r.stdout)
            self.assertIn("is built from the tree", r.stdout)
            self.assertIn("matches the tree", r.stdout)
        finally:
            os.unlink(fixture)

    def test_missing_manifest_reds(self):
        r = run_check({"GATES_MANIFEST_FILE": os.path.join(REPO, "guardrails", "no-such-manifest.json")})
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("no manifest stands", r.stdout)

    def test_missing_gates_yml_reds(self):
        r = run_check({"GATES_MANIFEST_GATES_YML": os.path.join(REPO, "no-such-file.yml")})
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_generator_and_gate_agree(self):
        # the generator's own fresh build, printed straight to stdout, parses and carries the same
        # gate count the committed manifest does — the two never read differently by construction,
        # since the gate loads the generator module rather than holding a second copy of the join.
        r = subprocess.run(["python3", GENERATOR, "--print"], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        fresh = json.loads(r.stdout)
        with open(MANIFEST) as f:
            committed = json.load(f)
        self.assertEqual(fresh, committed)

    def test_manifest_never_carries_gate_control_flow(self):
        # boundary: the manifest is a JOIN, not a generator of executable gate logic. It names gate
        # g's script but never gate g's own skip function, and gate h's script list is the four
        # resolved file paths, never the unresolved `${hostcheck}` loop template.
        with open(MANIFEST) as f:
            data = json.load(f)
        self.assertNotIn("gate_g_can_skip", json.dumps(data))
        self.assertNotIn("${hostcheck}", json.dumps(data))
        self.assertEqual(
            sorted(data["gates"]["h"]["scripts"]),
            sorted([
                "scaffold/guardrails/check_completeness.py",
                "scaffold/guardrails/check_tests_present.py",
                "scaffold/guardrails/check_traces_to_spec.py",
                "scaffold/guardrails/check_conflicts.py",
            ]))

    def test_readme_notes_untouched(self):
        # boundary: this gate does not require guardrails/README.md's prose notes (15 of 28 gates,
        # deliberately incomplete) to carry or match a gate's canonical law; the check reads only
        # the manifest and gates.yml, never guardrails/README.md itself.
        source = read("guardrails/check-gates-manifest.py")
        self.assertNotIn('"guardrails", "README.md"', source)
        self.assertNotIn("guardrails/README.md", source.split('"""', 2)[-1])

    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-gates-manifest.py", read("guardrails/pre-push"))
        self.assertIn("-- gate af:", read("guardrails/pre-push"))

    def test_gate_mirrored_in_ci(self):
        self.assertIn("check-gates-manifest.py", read(".github/workflows/gates.yml"))
        self.assertIn("gate af —", read(".github/workflows/gates.yml"))

    def test_registered_as_a_proof(self):
        with open(os.path.join(REPO, "guardrails", "gate-red-proofs.json")) as f:
            proofs = json.load(f)
        self.assertIn("af", proofs["proofs"])
        self.assertEqual(proofs["proofs"]["af"]["reds"], "check-gates-manifest")

    def test_matrix_row_covers_the_law(self):
        matrix = read("TEST_MATRIX.md")
        self.assertIn("gate af", matrix)
        self.assertIn("gates-manifest.json", matrix)


if __name__ == "__main__":
    unittest.main()
