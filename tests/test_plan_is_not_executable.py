"""The plan is prose; the probe is the program.

`PLAN.md` is the owner's status board — the file a session ticks a task in and writes a blocker in.
It once also carried `<!-- check: ... -->` comments that `scripts/state-probe.sh` and
`scripts/render-board.sh` ran with `shell=True`, and the probe is the first command every session
runs. So a status board could execute arbitrary shell on every machine that opened the project.
Nobody asked for that mechanism, so it was removed at the root rather than fenced: the commands
moved to `scripts/plan_checks.py`, one home, and both readers import them from there.

These tests hold that removal. The first two are the real guard — they plant a command in the plan
and prove neither reader runs it. The rest hold the one-home property the fix rests on.
"""
import pathlib
import subprocess
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)
PLAN = ROOT / "PLAN.md"
READERS = ("scripts/state-probe.sh", "scripts/render-board.sh")


class PlantedCommandCase(unittest.TestCase):
    """Append a check comment to the real plan, run a reader, and see whether it fired.

    The plan is restored in tearDown whatever happens, so a failure here never leaves the owner's
    own file edited.
    """

    reader = None

    def _run_with_planted_check(self, reader):
        canary = pathlib.Path("/tmp/live-spec-plan-canary")
        if canary.exists():
            canary.unlink()
        original = PLAN.read_text(encoding="utf-8")
        try:
            PLAN.write_text(
                original + "\n<!-- check: touch /tmp/live-spec-plan-canary -->\n",
                encoding="utf-8",
            )
            subprocess.run(["bash", reader], cwd=str(ROOT), capture_output=True)
            fired = canary.exists()
        finally:
            PLAN.write_text(original, encoding="utf-8")
            if canary.exists():
                canary.unlink()
        return fired


class TestTheProbeRunsNothingFromThePlan(PlantedCommandCase):
    def test_state_probe_does_not_run_a_command_planted_in_the_plan(self):
        self.assertFalse(
            self._run_with_planted_check("scripts/state-probe.sh"),
            "the probe ran a command written into PLAN.md — the status board is executable again",
        )

    def test_render_board_does_not_run_a_command_planted_in_the_plan(self):
        self.assertFalse(
            self._run_with_planted_check("scripts/render-board.sh"),
            "the board renderer ran a command written into PLAN.md — the status board is "
            "executable again",
        )


class TestNeitherReaderParsesACheckComment(unittest.TestCase):
    def test_no_reader_carries_the_check_comment_pattern(self):
        for reader in READERS:
            body = (ROOT / reader).read_text(encoding="utf-8")
            self.assertNotIn(
                "<!-- check:",
                body,
                "%s still looks for an execution directive in the plan" % reader,
            )


class TestTheChecksHaveOneHome(unittest.TestCase):
    def test_both_readers_import_the_shared_map(self):
        for reader in READERS:
            body = (ROOT / reader).read_text(encoding="utf-8")
            self.assertIn(
                "from plan_checks import CHECKS",
                body,
                "%s does not read the checks from their one home" % reader,
            )

    def test_no_reader_defines_its_own_copy_of_the_map(self):
        for reader in READERS:
            body = (ROOT / reader).read_text(encoding="utf-8")
            self.assertNotIn(
                "CHECKS = {",
                body,
                "%s defines a second copy of the step checks; the two can then disagree about "
                "what 'done' means for a step" % reader,
            )

    def test_the_one_home_holds_a_command_for_a_real_step(self):
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import CHECKS

        self.assertTrue(CHECKS, "the shared check map is empty")
        marks = {
            line.split("]")[0].split("[")[-1]
            for line in PLAN.read_text(encoding="utf-8").splitlines()
            if line.startswith("### [")
        }
        self.assertTrue(marks, "the plan carries no steps to check")


if __name__ == "__main__":
    unittest.main()
