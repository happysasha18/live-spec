"""The standalone mirrors sync automatically, from two homes — the local push gate and the CI net.

The pack is the single source of truth for every skill; a standalone skill (e.g. product-prover)
also lives as its own read-only mirror repo, updated only by scripts/sync-mirrors.sh. Left to a hand,
that sync drifts: a mirror was found one version behind the pack on 2026-07-13. So the sync is wired to
run on its own from both nets that already guard a push — the local pre-push hook (this developer's
machine) and the CI workflow (any machine, after the gates pass). The CI arm is token-gated: it skips
gracefully until a MIRROR_SYNC_TOKEN secret with write access to the mirror repos is present. Extends
the push gate (SPEC M-6) and the attribution/mirror mechanism (SPEC INV-96)."""
import os
import subprocess
import unittest
from conftest import ROOT


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


class TestMirrorAutosync(unittest.TestCase):
    def test_local_prepush_syncs_on_a_green_gate(self):
        hook = read("guardrails/pre-push")
        # runs the one sync script, never a second scheme
        self.assertIn("scripts/sync-mirrors.sh", hook)
        # non-blocking: the sync sits in the green-gate path and warns rather than failing the push
        self.assertIn("mirror sync (non-blocking)", hook)
        # the sync must sit AFTER the blocked-push exit, so a blocked push never reaches a mirror
        blocked = hook.index("PUSH BLOCKED")
        sync = hook.index("scripts/sync-mirrors.sh")
        self.assertLess(blocked, sync, "mirror sync must run only past the blocked-push gate")

    def test_ci_job_syncs_after_the_gates(self):
        ci = read(".github/workflows/gates.yml")
        self.assertIn("sync-mirrors:", ci)
        # runs only after the gates pass, only on a push to main
        self.assertIn("needs: gates", ci)
        self.assertIn("refs/heads/main", ci)
        # calls the one source-of-truth script, never a reimplementation
        self.assertIn("scripts/sync-mirrors.sh", ci)

    def test_ci_arm_is_key_gated_and_skips_gracefully(self):
        ci = read(".github/workflows/gates.yml")
        # auth is a per-mirror SSH deploy key held as a secret
        self.assertIn("MIRROR_SYNC_DEPLOY_KEY", ci)
        # a missing key is a clean skip, never a red CI (honest-failure by name, SPEC INV-112)
        self.assertIn("skipping mirror sync", ci)
        # CI reaches the mirror over SSH (the deploy key), the script's MIRROR_SSH path
        self.assertIn("MIRROR_SSH=1", ci)


class TestMirrorAbsenceCheckSurvivesAFailingGh(unittest.TestCase):
    """The absence check must reach its branches when `gh` fails (push review 2026-08-12, finding 4).

    `scripts/sync-mirrors.sh` runs under `set -euo pipefail`. Under `set -e` an assignment whose
    command substitution exits non-zero IS the failing simple command, so the plain form

        gh_view_err="$(gh repo view "$repo" 2>&1 >/dev/null)"
        gh_view_status=$?

    kills the script on the assignment line. Neither the loud FAIL for a check that could not
    answer nor the quiet skip for a genuinely absent mirror can print. That shipped on 2026-08-12
    in `7520a42`, and queue row 597 was closed on it. The two tests below read the script's own
    bytes and run them, so the shape cannot regress silently."""

    def _script_lines(self):
        src = read("scripts/sync-mirrors.sh")
        lines = [ln.strip() for ln in src.splitlines()]
        seed = [ln for ln in lines if ln == "gh_view_status=0"]
        call = [ln for ln in lines if ln.startswith('gh_view_err="$(gh repo view')]
        return seed, call

    def test_the_script_seeds_the_status_and_guards_the_assignment(self):
        seed, call = self._script_lines()
        self.assertEqual(len(seed), 1, "the status must be seeded before the guarded assignment")
        self.assertEqual(len(call), 1, "one absence check, one assignment")
        self.assertIn("|| gh_view_status=$?", call[0],
                      "a bare assignment dies on errexit before any branch can run")

    def test_the_script_s_own_two_lines_reach_the_branch_when_gh_fails(self):
        seed, call = self._script_lines()
        snippet = "\n".join([
            "set -euo pipefail",
            'gh() { echo "HTTP 500 something broke" >&2; return 7; }',
            'repo="happysasha18/does-not-matter"',
            seed[0],
            call[0],
            'echo "REACHED status=${gh_view_status} err=${gh_view_err}"',
        ])
        result = subprocess.run(["bash", "-c", snippet],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0,
                         "the script's own lines must survive a failing gh: " + result.stderr)
        self.assertIn("REACHED status=7", result.stdout)
        self.assertIn("HTTP 500 something broke", result.stdout)


if __name__ == "__main__":
    unittest.main()
