"""INV-210 — the CI mirror carries every local gate (gate u, ROADMAP 420 candidate 1).

guardrails/pre-push runs the push gate on this machine; .github/workflows/gates.yml re-runs it
in CI as the second, any-machine net (SPEC M-5). gates.yml is hand-maintained, so it drifts the
moment a gate is added locally and the CI file is not touched — the worked instance: gates h, k,
and n were missing from CI on 2026-07-18. check-ci-mirror.sh reads the gate letters pre-push
invokes and the gate letters gates.yml invokes, subtracts the declared CI carve-outs
(guardrails/ci-mirror.json, each with its reason), and reds on any local gate letter missing
from CI.
"""
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest

from conftest import read, read_flat

_shq = shlex.quote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "guardrails", "check-ci-mirror.sh")
GATES_YML = os.path.join(REPO, ".github", "workflows", "gates.yml")
CARVE_JSON = os.path.join(REPO, "guardrails", "ci-mirror.json")


def run_check(env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["bash", CHECK], cwd=REPO, capture_output=True, text=True, env=env)


class TestCiMirror(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK))

    def test_carve_json_ships_and_parses(self):
        import json
        with open(CARVE_JSON) as f:
            data = json.load(f)
        self.assertIn("ci_excluded", data)
        # every carve-out states a non-empty reason so the line is settled, not re-walked
        for letter, reason in data["ci_excluded"].items():
            self.assertTrue(reason.strip(), "carve-out %s has no reason" % letter)

    def test_real_tree_is_compliant(self):
        # the compliance proof: after this row synced gates h, n, and u into gates.yml,
        # every local gate is mirrored in CI or a declared carve-out.
        r = run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_gate_step_reds(self):
        # a fixture gates.yml with a should-be-present gate step removed must red, naming it.
        yml = read(".github/workflows/gates.yml")
        stripped = "\n".join(
            ln for ln in yml.splitlines() if "gate d " not in ln
        )
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write(stripped)
            fixture = f.name
        try:
            r = run_check({"CI_MIRROR_GATES_YML": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("gate d", r.stdout)
        finally:
            os.unlink(fixture)

    def test_compliant_fixture_passes(self):
        # the untouched real gates.yml, pointed at explicitly, passes
        r = run_check({"CI_MIRROR_GATES_YML": GATES_YML})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_stale_carveout_reds(self):
        # a carve-out naming no local gate is itself drift and reds. The gate letters run single then
        # double (a..y, aa..), so the fixture uses a token no `-- gate [a-z]{1,2}:` marker can ever be
        # — a doubled unused letter — which can never match a real gate letter.
        import json
        with open(CARVE_JSON) as f:
            data = json.load(f)
        data["ci_excluded"]["zz"] = "no such local gate"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            fixture = f.name
        try:
            r = run_check({"CI_MIRROR_JSON": fixture})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("zz", r.stdout)
        finally:
            os.unlink(fixture)

    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-ci-mirror.sh", read("guardrails/pre-push"))

    def test_gate_mirrored_in_ci(self):
        # gate u must represent itself in CI, so it never reds on its own absence
        self.assertIn("check-ci-mirror.sh", read(".github/workflows/gates.yml"))

    def test_compliance_added_h_n_u(self):
        # the three letters this row synced into CI are present in gates.yml step names
        ci = read(".github/workflows/gates.yml")
        for letter in ("gate h", "gate n", "gate u"):
            self.assertIn(letter, ci, "%s missing from CI mirror" % letter)

    # --- traceability across the four documents ---

    def test_spec_states_the_law(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-210]", spec)
        # The requirements-format spec states the law, not the implementing script filename.
        self.assertIn("a gate letter locally that the remote mirror does not run", spec)
        self.assertIn("ci-mirror.json", spec)

    def test_formal_index_row(self):
        self.assertIn("| INV-210 |", read("PRODUCT_SPEC.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-210", arch)
        self.assertIn("check-ci-mirror.sh", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-210", read("TEST_MATRIX.md"))


class TestExtractionFailureIsNeverData(unittest.TestCase):
    """A failed or partial extraction pipeline must never be judged as complete data.

    The gate reads three lists through shell pipelines: the local gate letters off pre-push, the
    CI gate letters off gates.yml, and the declared carve-outs off ci-mirror.json. Each read used
    to end in `|| true`, which suspends the script's own `set -euo pipefail` for exactly that line,
    so a stage that failed or was cut off mid-stream left a silently empty or short list behind and
    the comparison ran on it. What came out was not an error but a FALSE RED naming whichever gate
    letters the broken read happened to drop — a verdict about the tree, sourced from a read that
    never finished. These three cases are the proven shapes, each pinned by substituting `grep` on
    PATH so the pipeline breaks while every input file stays intact and readable.
    """

    @staticmethod
    def _grep_shim(tmp, pattern, body):
        """A `grep` on PATH that breaks for one pattern and is the real grep for every other call."""
        real = shutil.which("grep")
        path = os.path.join(tmp, "grep")
        with open(path, "w") as f:
            f.write(
                "#!/bin/bash\n"
                'for a in "$@"; do\n'
                '  if [[ "$a" == %s ]]; then\n'
                "%s\n"
                "  fi\n"
                "done\n"
                'exec %s "$@"\n' % (_shq(pattern), body, real)
            )
        os.chmod(path, 0o755)
        return real

    def _run_with_broken_grep(self, pattern, body):
        with tempfile.TemporaryDirectory() as tmp:
            self._grep_shim(tmp, pattern, body)
            return run_check({"PATH": tmp + os.pathsep + os.environ["PATH"]})

    def test_full_stage_failure_is_not_read_as_absence(self):
        # The gates.yml read fails outright and returns nothing. Every local gate then looks
        # unmirrored. The gate must say the read failed, not accuse 25 innocent gates.
        r = self._run_with_broken_grep("name:.*gate [a-z]", "    exit 1")
        out = r.stdout + r.stderr
        self.assertNotIn("absent from", out, out)
        self.assertIn("could not be read", out, out)
        self.assertNotEqual(r.returncode, 0, out)

    def test_partial_stage_output_is_not_read_as_complete(self):
        # The same read is cut off mid-stream: it yields every line but the two naming gates d
        # and e, then fails. The short list must not become the verdict.
        real = shutil.which("grep")
        body = '    %s "$@" | %s -vE "gate (d|e) "\n    exit 1' % (real, real)
        r = self._run_with_broken_grep("name:.*gate [a-z]", body)
        out = r.stdout + r.stderr
        self.assertNotIn("gate d runs in", out, out)
        self.assertNotIn("gate e runs in", out, out)
        self.assertIn("could not be read", out, out)
        self.assertNotEqual(r.returncode, 0, out)

    def test_local_letter_read_failure_is_not_read_as_a_stale_carveout(self):
        # The pre-push read is cut off and loses gate c. Carve-out 'c' then names no local gate
        # and reads as stale drift — a second false verdict off the same broken pipe.
        real = shutil.which("grep")
        body = '    %s "$@" | %s -v -- "-- gate c:"\n    exit 1' % (real, real)
        r = self._run_with_broken_grep("-- gate [a-z]{1,2}:", body)
        out = r.stdout + r.stderr
        self.assertNotIn("names no local pre-push gate", out, out)
        self.assertIn("could not be read", out, out)
        self.assertNotEqual(r.returncode, 0, out)

    def test_a_repo_declaring_no_carveouts_is_not_a_failed_read(self):
        # The intended empty case stays intended: `ci_excluded: {}` is a repo that carves nothing
        # out, which jq reports as an empty list on a clean exit. That must never read as a broken
        # pipeline. It may still red for an unmirrored gate — it must not red for the read itself.
        import json
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"ci_excluded": {}}, f)
            fixture = f.name
        try:
            r = run_check({"CI_MIRROR_JSON": fixture})
            self.assertNotIn("could not be read", r.stdout + r.stderr)
        finally:
            os.unlink(fixture)


if __name__ == "__main__":
    unittest.main()
