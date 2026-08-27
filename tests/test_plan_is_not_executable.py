"""The plan is prose; the probe is the program.

`PLAN.md` is the owner's status board — the file a session ticks a task in and writes a blocker in.
It once also carried `<!-- check: ... -->` comments that `scripts/state-probe.sh` and
`scripts/render-board.sh` ran with `shell=True`, and the probe is the first command every session
runs. So a status board could execute arbitrary shell on every machine that opened the project.
Nobody asked for that mechanism, so it was removed at the root rather than fenced: the commands
moved to `scripts/plan_checks.py`, one home, and both readers import them from there.

These tests hold that removal. The planted-command tests run against a THROWAWAY COPY of the repo
in a temp directory and never touch the real `PLAN.md`. An earlier version of this file edited the
real plan and restored it in a `finally`; two of those runs overlapped, each took the other's
half-written file as its "original", and the plan ended up with 722 junk lines appended. A test
that mutates a file a person owns is a bad test even when its restore is correct, because the
restore is only correct while nothing else is running.
"""
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)
PLAN = ROOT / "PLAN.md"
READERS = ("scripts/state-probe.sh", "scripts/render-board.sh")

# What a reader needs from the tree to run at all: the plan it reads, the two reader scripts, and
# the one home the checks now live in.
NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh", "scripts/plan_checks.py")


class TestAPlantedCommandNeverRuns(unittest.TestCase):
    """Plant a check comment in a COPY of the plan, run a reader there, see whether it fired."""

    def _plant_and_run(self, reader):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            for rel in NEEDED:
                dst = tmp / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, dst)

            canary = tmp / "canary-fired"
            plan = tmp / "PLAN.md"
            plan.write_text(
                plan.read_text(encoding="utf-8")
                + "\n<!-- check: touch %s -->\n" % canary,
                encoding="utf-8",
            )

            subprocess.run(
                ["bash", str(tmp / reader)],
                cwd=str(tmp),
                capture_output=True,
                env={**os.environ, "HOME": str(tmp)},
            )
            return canary.exists()

    def test_the_probe_runs_nothing_written_into_the_plan(self):
        self.assertFalse(
            self._plant_and_run("scripts/state-probe.sh"),
            "the probe ran a command written into the plan — the status board is executable again",
        )

    def test_the_board_renderer_runs_nothing_written_into_the_plan(self):
        self.assertFalse(
            self._plant_and_run("scripts/render-board.sh"),
            "the board renderer ran a command written into the plan — the status board is "
            "executable again",
        )


class TestNeitherReaderLooksForACommandInThePlan(unittest.TestCase):
    def test_no_reader_carries_the_check_comment_pattern(self):
        for reader in READERS:
            self.assertNotIn(
                "<!-- check:",
                (ROOT / reader).read_text(encoding="utf-8"),
                "%s still looks for an execution directive in the plan" % reader,
            )

    def test_the_plan_itself_carries_no_executable_line(self):
        for i, line in enumerate(PLAN.read_text(encoding="utf-8").splitlines(), 1):
            self.assertFalse(
                line.startswith("<!-- check:"),
                "PLAN.md:%d is an execution directive; the plan is prose" % i,
            )


class TestTheChecksHaveOneHome(unittest.TestCase):
    def test_both_readers_import_the_shared_map(self):
        # Both readers import parse_tasks() rather than CHECKS directly since PLAN.md's
        # task-list merge (commit bc6f862b): parse_tasks() is scripts/plan_checks.py's own
        # parser for PLAN.md's "## Tasks" section, and it looks up CHECKS internally (each
        # parsed task's "check" field is CHECKS.get(task id)) — so the check map still has the
        # one home this test exists to hold, reached through the shared parser instead of a
        # bare import.
        for reader in READERS:
            self.assertIn(
                "from plan_checks import parse_tasks",
                (ROOT / reader).read_text(encoding="utf-8"),
                "%s does not read the plan through the shared parser/checks home" % reader,
            )

    def test_no_reader_defines_its_own_copy_of_the_map(self):
        for reader in READERS:
            self.assertNotIn(
                "CHECKS = {",
                (ROOT / reader).read_text(encoding="utf-8"),
                "%s defines a second copy of the step checks; the two can then disagree about "
                "what 'done' means for a step" % reader,
            )

    def test_every_check_is_cheap_enough_for_the_probe(self):
        """The probe runs every one of these at the start of every session, so none may run a
        test suite. A suite in here made the owner's morning command hang."""
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import CHECKS

        self.assertTrue(CHECKS, "the shared check map is empty")
        for step, cmd in CHECKS.items():
            self.assertNotIn(
                "pytest",
                cmd,
                "step %s's check runs a test suite; the probe must stay fast" % step,
            )


if __name__ == "__main__":
    unittest.main()
