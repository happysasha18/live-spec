# -*- coding: utf-8 -*-
"""A project with no git history keeps its files as they were found when it joins (PLAN q-55).

`adopt/ADOPT.md` Phase 0 told a session to run `git init` and make a baseline commit by hand, so
each setup walk reinvented the step and each one was free to forget it. `adopt/record-starting-state.sh`
is that step as something that runs.

The positive walk builds a throwaway directory that is not a git repository, runs the real step over
it, and holds it to three things: the directory is a repository, its first commit carries the files
as they stood with no pack file among them, and `git diff <that commit> --stat` runs from the project
root. The negative walk builds the same directory, skips the step, and asserts each of the three
fails — so a step that silently did nothing could not pass here.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "adopt", "record-starting-state.sh")


def git(project, *args):
    return subprocess.run(["git", "-C", project] + list(args), capture_output=True, text=True)


class StartingStateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="livespec-test-starting-state-")
        self.project = os.path.join(self.tmp, "host")
        os.makedirs(os.path.join(self.project, "src"))
        open(os.path.join(self.project, "README.md"), "w").write("the project\n")
        open(os.path.join(self.project, "src", "app.py"), "w").write("x = 1\n")
        self.as_found = ["README.md", "src/app.py"]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def join(self):
        return subprocess.run(["bash", SCRIPT, self.project], capture_output=True, text=True)

    def test_joining_commits_the_files_as_they_were_found(self):
        run = self.join()
        self.assertEqual(run.returncode, 0, run.stderr)

        # (a) the project is now a git repository
        self.assertEqual(0, git(self.project, "rev-parse", "--show-toplevel").returncode)

        # (b) its first commit holds the files as they stood, and no pack file
        first = git(self.project, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
        self.assertTrue(first)
        listed = git(self.project, "ls-tree", "-r", "--name-only", first).stdout.split()
        self.assertEqual(sorted(self.as_found), sorted(listed))

        # (c) the diff command works, and shows nothing on a tree nothing has touched since
        stat = git(self.project, "diff", first, "--stat")
        self.assertEqual(0, stat.returncode, stat.stderr)
        self.assertEqual("", stat.stdout.strip())

    def test_a_change_since_joining_shows_in_that_diff(self):
        self.join()
        first = git(self.project, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
        open(os.path.join(self.project, "src", "app.py"), "w").write("x = 2\n")
        self.assertIn("src/app.py", git(self.project, "diff", first, "--stat").stdout)

    def test_all_three_fail_when_the_joining_step_is_skipped(self):
        # The step never runs. Each assertion the positive walk makes has to fail here.
        self.assertNotEqual(0, git(self.project, "rev-parse", "--show-toplevel").returncode)
        self.assertEqual("", git(self.project, "rev-list", "--max-parents=0", "HEAD").stdout.strip())
        self.assertNotEqual(0, git(self.project, "diff", "HEAD", "--stat").returncode)

    def test_a_project_that_already_has_history_gains_no_commit(self):
        git(self.project, "init", "-q")
        git(self.project, "add", "-A")
        git(self.project, "-c", "user.name=t", "-c", "user.email=t@example.com",
            "commit", "-q", "-m", "the project's own first commit")
        before = git(self.project, "rev-parse", "HEAD").stdout.strip()

        run = self.join()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(before, git(self.project, "rev-parse", "HEAD").stdout.strip())


if __name__ == "__main__":
    unittest.main()
