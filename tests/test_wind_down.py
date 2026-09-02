"""One command safely winds down all the work before you leave (PLAN q-235, scripts/wind-down.py).

The acceptance: one command halts every running worker, writes each one's checkpoint to disk,
gets what is unpushed off the machine, and prints a single closing line saying what is safe and
what is still open. This suite builds a throwaway fixture tree (a bare "origin", a working repo
tracking it, and a locked worker worktree holding a real live process) and runs the command over
it, red on any one of the four things being skipped:

  1. the live worker is actually signaled and stops running;
  2. a checkpoint file is written to disk for it, in this project's own checkpoint format
     (scripts/checkpoint.py), so it parses/validates clean;
  3. the unpushed commit reaches "origin" -- but ONLY when the push gate is green; a red gate
     must leave it unpushed rather than being bypassed;
  4. exactly one closing summary line is printed, naming what's safe and what's open.

It also proves the safety guard never asked for by the acceptance in so many words but implied
by "safely": a worktree whose lock names this test process's OWN pid (an ancestor of the
wind-down subprocess, since the subprocess is spawned by this test) is never signaled -- ending
that pid would end the session running the command.

Every fixture directory here is built under tempfile.mkdtemp() (this run's own temp root, per
tests/conftest.py) and removed in tearDown -- nothing here ever touches this worktree's real,
gitignored .live-spec/checkpoints/.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
WIND_DOWN = os.path.join(SCRIPTS, "wind-down.py")

sys.path.insert(0, SCRIPTS)
import checkpoint  # noqa: E402  (scripts/checkpoint.py)


def git(repo, *args):
    # An explicit identity, never the machine's own global config: a commit here has no author to
    # inherit on a fresh CI runner (no ~/.gitconfig at all), where `git commit` fails outright
    # (exit 128, "Please tell me who you are") — reproduced live on CI, 2026-09-02, six tests deep
    # into this fixture. A dev machine with its own global user.name/user.email masked the gap.
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "livespec-test",
        "GIT_AUTHOR_EMAIL": "livespec-test@example.invalid",
        "GIT_COMMITTER_NAME": "livespec-test",
        "GIT_COMMITTER_EMAIL": "livespec-test@example.invalid",
    })
    return subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True, env=env)


GREEN_GATE = "#!/bin/bash\nexit 0\n"
RED_GATE = "#!/bin/bash\nexit 1\n"


class WindDownFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="livespec-test-wind-down-")
        self.origin = os.path.join(self.tmp, "origin.git")
        self.repo = os.path.join(self.tmp, "repo")
        self._procs = []

        r = subprocess.run(["git", "init", "--bare", self.origin], capture_output=True, text=True)
        self.assertEqual(0, r.returncode, r.stderr)

        r = subprocess.run(["git", "init", "-b", "main", self.repo], capture_output=True, text=True)
        self.assertEqual(0, r.returncode, r.stderr)

        Path(self.repo, "README.md").write_text("fixture repo\n", encoding="utf-8")
        self.assertEqual(0, git(self.repo, "add", "README.md").returncode)
        self.assertEqual(0, git(self.repo, "commit", "-m", "initial").returncode)

        self.assertEqual(0, git(self.repo, "remote", "add", "origin", self.origin).returncode)
        r = git(self.repo, "push", "-u", "origin", "main")
        self.assertEqual(0, r.returncode, r.stderr)

    def tearDown(self):
        for p in self._procs:
            if p.poll() is None:
                p.kill()
                p.wait(timeout=5)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def add_unpushed_commit(self, name="second.txt"):
        Path(self.repo, name).write_text("more work\n", encoding="utf-8")
        self.assertEqual(0, git(self.repo, "add", name).returncode)
        self.assertEqual(0, git(self.repo, "commit", "-m", "unpushed work: %s" % name).returncode)

    def install_gate(self, script_text):
        gdir = Path(self.repo, "guardrails")
        gdir.mkdir(parents=True, exist_ok=True)
        gate = gdir / "pre-push"
        gate.write_text(script_text, encoding="utf-8")
        gate.chmod(0o755)

    def add_locked_worker(self, branch="worker-branch", pid=None, reason_extra=""):
        """git worktree add + lock, with a reason carrying `pid` in the format this project's
        agent worktrees already use: `claude agent <name> (pid N start <timestamp>)`."""
        wpath = os.path.join(self.tmp, branch)
        r = git(self.repo, "worktree", "add", wpath, "-b", branch)
        self.assertEqual(0, r.returncode, r.stderr)
        pid_text = ("pid %d" % pid) if pid is not None else "pid 999999"
        reason = "claude agent %s (%s start Mon Jan  1 00:00:00 2026)%s" % (branch, pid_text, reason_extra)
        r = git(self.repo, "worktree", "lock", wpath, "--reason", reason)
        self.assertEqual(0, r.returncode, r.stderr)
        return wpath

    def spawn_worker_process(self):
        proc = subprocess.Popen(["sleep", "60"])
        self._procs.append(proc)
        return proc

    def run_wind_down(self):
        return subprocess.run(
            [sys.executable, WIND_DOWN, "--repo", self.repo], capture_output=True, text=True
        )


class TestGreenPath(WindDownFixture):
    """A live worker, an unpushed commit, and a green gate: all four things happen."""

    def setUp(self):
        super().setUp()
        self.install_gate(GREEN_GATE)
        git(self.repo, "add", "guardrails/pre-push")
        git(self.repo, "commit", "-m", "add push gate")
        git(self.repo, "push")

        self.worker_proc = self.spawn_worker_process()
        self.worker_path = self.add_locked_worker("worker-branch", pid=self.worker_proc.pid)
        self.add_unpushed_commit()

    def test_1_live_worker_is_actually_halted(self):
        self.assertIsNone(self.worker_proc.poll(), "fixture setup bug: worker died before wind-down ran")
        result = self.run_wind_down()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        # give the OS a moment to reap the signaled process
        deadline = time.time() + 5
        while time.time() < deadline and self.worker_proc.poll() is None:
            time.sleep(0.1)
        self.assertIsNotNone(
            self.worker_proc.poll(),
            "the worker process was still running after wind-down claimed success:\n%s" % result.stdout,
        )

    def test_2_checkpoint_is_written_and_valid(self):
        result = self.run_wind_down()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        ckpt_dir = Path(self.repo, ".live-spec", "checkpoints")
        files = list(ckpt_dir.glob("*worker-branch*.md")) if ckpt_dir.is_dir() else []
        self.assertTrue(files, "no checkpoint file written for the locked worktree; found: %s" % (
            list(ckpt_dir.glob("*")) if ckpt_dir.is_dir() else "(no checkpoint dir at all)"
        ))
        data = checkpoint.read_checkpoint(files[0])  # raises on structural breakage
        issues = checkpoint.validate_checkpoint(files[0])
        self.assertEqual([], issues, "checkpoint failed its own validation: %s" % issues)
        self.assertIn(self.worker_path, data["sections"].get("IN PROGRESS", ""))

    def test_3_unpushed_commit_reaches_origin(self):
        before = git(self.repo, "rev-list", "--count", "@{u}..HEAD").stdout.strip()
        self.assertNotEqual("0", before, "fixture setup bug: nothing unpushed before wind-down")

        result = self.run_wind_down()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        after = git(self.repo, "rev-list", "--count", "@{u}..HEAD").stdout.strip()
        self.assertEqual("0", after, "commit was not pushed to origin:\n%s" % result.stdout)

        # and it is really on the bare "origin", not just locally re-pointed
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        remote_branches = subprocess.run(
            ["git", "--git-dir", self.origin, "branch", "--contains", head],
            capture_output=True, text=True,
        )
        self.assertIn("main", remote_branches.stdout)

    def test_4_prints_exactly_one_closing_line(self):
        result = self.run_wind_down()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        closing_lines = [l for l in result.stdout.splitlines() if l.startswith("WIND-DOWN:")]
        self.assertEqual(1, len(closing_lines), "expected exactly one closing line, got: %r" % closing_lines)
        self.assertIn("SAFE", closing_lines[0])
        self.assertIn("OPEN", closing_lines[0])
        self.assertIn("none", closing_lines[0].lower())  # nothing left open on the green path


class TestRedGatePath(WindDownFixture):
    """A red push gate must leave the commit unpushed -- never bypassed -- and be reported open."""

    def setUp(self):
        super().setUp()
        self.install_gate(RED_GATE)
        git(self.repo, "add", "guardrails/pre-push")
        git(self.repo, "commit", "-m", "add failing push gate")
        git(self.repo, "push")
        self.add_unpushed_commit()

    def test_gate_red_withholds_the_push_and_reports_open(self):
        before = git(self.repo, "rev-list", "--count", "@{u}..HEAD").stdout.strip()
        self.assertNotEqual("0", before)

        result = self.run_wind_down()
        self.assertNotEqual(0, result.returncode, "a red push gate must not be a clean exit")

        after = git(self.repo, "rev-list", "--count", "@{u}..HEAD").stdout.strip()
        self.assertEqual(before, after, "the gate was red but the commit left the machine anyway")

        closing_lines = [l for l in result.stdout.splitlines() if l.startswith("WIND-DOWN:")]
        self.assertEqual(1, len(closing_lines))
        self.assertIn("OPEN", closing_lines[0])
        self.assertNotIn("OPEN -- none", closing_lines[0])


class TestSelfGuard(WindDownFixture):
    """A worktree locked under THIS test process's own pid is never signaled: killing it would
    end the session running wind-down, since this test's pid is an ancestor of the wind-down
    subprocess it spawns below."""

    def setUp(self):
        super().setUp()
        self.install_gate(GREEN_GATE)
        git(self.repo, "add", "guardrails/pre-push")
        git(self.repo, "commit", "-m", "add push gate")
        git(self.repo, "push")
        self.worker_path = self.add_locked_worker("self-worker", pid=os.getpid())

    def test_own_controlling_process_is_left_running_and_reported_open(self):
        result = self.run_wind_down()
        # This assertion is the point: if wind-down had signaled os.getpid(), this very test
        # process would not be here to make it.
        self.assertEqual(0, os.kill(os.getpid(), 0) or 0)
        closing_lines = [l for l in result.stdout.splitlines() if l.startswith("WIND-DOWN:")]
        self.assertEqual(1, len(closing_lines))
        self.assertIn("still open", closing_lines[0].lower())


if __name__ == "__main__":
    unittest.main()
