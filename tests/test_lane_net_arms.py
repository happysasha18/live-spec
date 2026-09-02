"""The branch road's net, machine-checked rather than merely narrated (PLAN q-804, SPEC INV-198,
INV-199, INV-201).

Three of the branch road's promises stood as their own `[target]` lines in spec/parallel-lanes.md,
each naming a check "the prover's station" covered until it shipped: a config-health arm reading
the primary tree's checked-out branch, a merge-base arm ahead of the landing gate, and an
adoption-gate arm reading a host's vendored worktree line. q-386 closed its own row without
touching any of the three, orphaning them; q-804 is the row that builds them.

Each arm below is proven the way this project already proves a real git mechanism (see
tests/test_lane_branch_road.py's `_ProbeRepo`): plant the exact condition the arm exists to catch
on a real, hermetic repo, run the shipped script, and read its exit code and its message — never an
assertion against the script's source text standing in for actually running it.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT
from test_lane_branch_road import _ProbeRepo, _git

GUARDRAILS = os.path.join(ROOT, "guardrails")
CONFIG_HEALTH = os.path.join(GUARDRAILS, "check-config-health.sh")
MERGE_BASE = os.path.join(GUARDRAILS, "check-merge-base.sh")
WORKTREE_LINE = os.path.join(GUARDRAILS, "check-worktree-line.sh")


class TestConfigHealthPrimaryTreeArm(_ProbeRepo):
    """SPEC Requirement 85 criterion 5 (INV-198): "keep the config-health check on the primary
    tree holding main promised, git's refusal the net until it ships." The refusal INV-198 leans
    on — git refusing another worktree's checkout/force/push against a branch a tree holds checked
    out — only fires for a branch a tree actually holds. A primary tree drifted off main leaves
    main free for any lane to move, with nothing refusing it; this arm is the check.
    """

    def run_config_health(self, cwd, env=None):
        return subprocess.run([CONFIG_HEALTH], cwd=cwd, capture_output=True, text=True, env=env)

    def test_primary_tree_on_main_passes(self):
        result = self.run_config_health(self.main_tree)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('"code":"config-health"', result.stdout)

    def test_primary_tree_drifted_off_main_reds(self):
        self.run_ok(self.main_tree, "checkout", "-q", "-b", "other-branch")
        result = self.run_config_health(self.main_tree)
        self.assertNotEqual(result.returncode, 0, "the gate passed a primary tree off main")
        self.assertIn('"code":"config-health"', result.stdout)
        self.assertIn("other-branch", result.stdout)
        self.assertIn("INV-198", result.stdout)

    def test_a_detached_primary_tree_reds(self):
        self.run_ok(self.main_tree, "checkout", "-q", "--detach", "HEAD")
        result = self.run_config_health(self.main_tree)
        self.assertNotEqual(result.returncode, 0, "the gate passed a detached primary tree")
        self.assertIn('"code":"config-health"', result.stdout)
        self.assertIn("detached HEAD", result.stdout)

    def test_the_read_is_of_the_primary_tree_not_the_invoking_one(self):
        """The check must read the PRIMARY tree's branch even when invoked from the lane
        worktree — git's own `worktree list` always lists the primary tree first, and this arm
        reads that shared metadata rather than the invoking tree's own HEAD."""
        result_from_lane = self.run_config_health(self.lane_tree)
        self.assertEqual(result_from_lane.returncode, 0, result_from_lane.stdout + result_from_lane.stderr)

        self.run_ok(self.main_tree, "checkout", "-q", "-b", "other-branch")
        result_from_lane = self.run_config_health(self.lane_tree)
        self.assertNotEqual(
            result_from_lane.returncode, 0,
            "invoked from the LANE tree, the check should still read the PRIMARY tree's branch "
            "and red — it did not, so it is reading the wrong tree's checkout",
        )
        self.assertIn("other-branch", result_from_lane.stdout)

    def test_the_arm_still_fires_under_a_ci_environment(self):
        """The script's own top-of-file carve-out (`if GITHUB_ACTIONS/CI = true; then skip;
        exit 0; fi`) exists for the installed-hooks/skills/perms checks, which are genuinely
        meaningless on a CI checkout. It used to sit ahead of the INV-198 worktree arm too,
        so on the real GitHub runner — where GITHUB_ACTIONS is always set — the whole script
        exited before the arm ever ran, and every test in this class passed locally (a dev
        machine never sets that variable) while failing on CI, silently, with a clean exit
        code (2026-09-02: all four of this class's own tests came back green on a real CI run
        that had a deliberately drifted primary tree). This plants that exact condition and
        runs the check with GITHUB_ACTIONS set, so the arm's CI-reachability is never again
        provable only by a hypothesis about a real runner nobody here has a shell on."""
        self.run_ok(self.main_tree, "checkout", "-q", "-b", "other-branch")
        env = dict(os.environ)
        env["GITHUB_ACTIONS"] = "true"
        result = self.run_config_health(self.main_tree, env=env)
        self.assertNotEqual(
            result.returncode, 0,
            "the arm passed a drifted primary tree under a CI environment — it is not being "
            "reached, the exact shape that let this bug hide on every dev machine",
        )
        self.assertIn('"code":"config-health"', result.stdout)
        self.assertIn("other-branch", result.stdout)

    def test_a_failed_worktree_list_read_reds_loudly_instead_of_standing_down(self):
        """`git worktree list` can fail for reasons this project's own machine never hits locally
        — a container/CI runner's "detected dubious ownership" refusal chief among them (3 of
        this class's own tests failed on CI, 2026-09-02, with no diagnostic naming why). The arm
        must red with git's own error rather than reading zero worktrees and passing silently, so
        this plants a git wrapper that fails only the `worktree list` subcommand and confirms the
        arm reds with that failure named, never mistaking "could not check" for "nothing to
        check."""
        real_git = shutil.which("git")
        fake_bin = os.path.join(self.tmp, "fake-git-bin")
        os.makedirs(fake_bin, exist_ok=True)
        fake_git = os.path.join(fake_bin, "git")
        with open(fake_git, "w") as f:
            f.write(
                "#!/bin/sh\n"
                'case " $* " in\n'
                '  *" worktree list "*)\n'
                '    echo "fatal: detected dubious ownership in repository at '"'"'$PWD'"'"'" >&2\n'
                "    exit 128\n"
                "    ;;\n"
                "esac\n"
                f'exec "{real_git}" "$@"\n'
            )
        os.chmod(fake_git, 0o755)
        env = dict(os.environ)
        env["PATH"] = fake_bin + os.pathsep + env["PATH"]

        result = subprocess.run([CONFIG_HEALTH], cwd=self.main_tree, capture_output=True, text=True, env=env)
        self.assertNotEqual(result.returncode, 0, "the arm passed even though git worktree list itself failed")
        self.assertIn('"code":"config-health"', result.stdout)
        self.assertIn("worktree list failed", result.stdout)
        self.assertIn("dubious ownership", result.stdout)


class TestMergeBaseArm(_ProbeRepo):
    """SPEC Requirement 86 criterion 5 (INV-199): "keep the merge-base check ahead of the gate ...
    promised, the prover's station [its] net until then." Criterion 2 names the predicate: the
    branch's merge-base with main equals main's tip; a lane that has not rebased reds so the
    landing gate never reads a stale tree.
    """

    def run_merge_base(self, cwd, *args):
        return subprocess.run([MERGE_BASE, *args], cwd=cwd, capture_output=True, text=True)

    def test_a_lane_just_cut_from_mains_tip_passes(self):
        result = self.run_merge_base(self.lane_tree)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("merge-base: OK", result.stdout)

    def test_a_lane_stale_behind_a_moved_main_reds(self):
        self.commit(self.main_tree, "h", "three\n", "three")  # another lane lands, main moves
        result = self.run_merge_base(self.lane_tree)
        self.assertNotEqual(result.returncode, 0, "the gate passed a lane that never rebased")
        self.assertIn('"code":"merge-base"', result.stdout)
        self.assertIn("INV-199", result.stdout)

    def test_the_same_lane_rebased_passes_again(self):
        self.commit(self.main_tree, "h", "three\n", "three")
        self.run_ok(self.lane_tree, "rebase", "main")
        result = self.run_merge_base(self.lane_tree)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("merge-base: OK", result.stdout)

    def test_a_worktree_path_argument_is_read_from_elsewhere(self):
        """Requirement 86's landing walk runs the check ahead of the gate, from whichever tree is
        doing the integrating — so the script must be able to read another tree's HEAD by path
        rather than only its own, invoked cwd."""
        self.commit(self.main_tree, "h", "three\n", "three")
        result = self.run_merge_base(self.main_tree, self.lane_tree)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"code":"merge-base"', result.stdout)

        self.run_ok(self.lane_tree, "rebase", "main")
        result = self.run_merge_base(self.main_tree, self.lane_tree)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestWorktreeLineArm(unittest.TestCase):
    """SPEC Requirement 88 criterion 6 (INV-201): "keep the adoption gate for the host's worktree
    line promised, the prover's station its net until the build lands." Criterion 4 names the
    predicate: red a host whose project instructions carry no worktree line.
    """

    def run_worktree_line(self, host):
        return subprocess.run([WORKTREE_LINE, host], cwd=ROOT, capture_output=True, text=True)

    def test_a_host_with_no_claude_md_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_worktree_line(tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('"code":"worktree-line"', result.stdout)

    def test_a_host_whose_instructions_carry_no_worktree_line_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "CLAUDE.md"), "w", encoding="utf-8") as fh:
                fh.write("# a host project\n\nRules that never mention the worktree tool.\n")
            result = self.run_worktree_line(tmp)
            self.assertNotEqual(result.returncode, 0, "the gate passed a host with no worktree line")
            self.assertIn('"code":"worktree-line"', result.stdout)
            self.assertIn("INV-201", result.stdout)

    def test_a_host_carrying_the_vendored_line_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "CLAUDE.md"), "w", encoding="utf-8") as fh:
                fh.write(
                    "# a host project\n\n"
                    "Two lanes with overlapping write-sets get worktree isolation "
                    "(SPEC INV-105).\n"
                )
            result = self.run_worktree_line(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("worktree-line: OK", result.stdout)

    def test_a_line_that_only_names_a_worktree_with_no_citation_still_reds(self):
        """The gate reads for the citation, not merely the word "worktree" — a line that
        restates the condition instead of citing INV-105 is exactly what criterion 1 forbids."""
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "CLAUDE.md"), "w", encoding="utf-8") as fh:
                fh.write("# a host project\n\nUse a worktree for isolated work.\n")
            result = self.run_worktree_line(tmp)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
