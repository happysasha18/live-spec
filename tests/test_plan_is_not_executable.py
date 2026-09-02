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
import re
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
        # Matched as an import of the name rather than as one exact line: a reader that also
        # imports the shared failure note beside the parser still reads the plan through the one
        # home, and an assertion pinned to the line's wording would call that a violation.
        importing_the_parser = re.compile(r"^from plan_checks import .*\bparse_tasks\b", re.M)
        for reader in READERS:
            self.assertRegex(
                (ROOT / reader).read_text(encoding="utf-8"),
                importing_the_parser,
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


class TestADoneMarkCannotOutliveItsKey(unittest.TestCase):
    """A ✅ whose acceptance command fails must not print as done, on either reader.

    The keys exist so a command can contradict the mark somebody typed. Until 2026-08-28 it could
    not: a failing command fell back to the task's own mark, so a ✅ printed ✅, carried the
    verified tag, and was counted among the done — the one case the whole key table was written
    for was the one case it could not report. Both readers are held here, because they format a
    task independently and that is where they drifted apart before.
    """

    PLAN = (
        "# Plan\n\n## Tasks\n\n"
        "### ✅ A task whose key cannot hold — id: plan-0\n"
        "**Group:** Machinery · **Priority:** normal\n"
        "**Source:** the test.\n\n"
        "Its acceptance command is `false`, so the command and the mark disagree.\n\n"
        "## Blockers\n\n- none\n"
    )

    def _run(self, reader):
        tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, str(tmp), True)
        for rel in NEEDED:
            dst = tmp / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        (tmp / "PLAN.md").write_text(self.PLAN, encoding="utf-8")
        checks = tmp / "scripts" / "plan_checks.py"
        checks.write_text(
            checks.read_text(encoding="utf-8") + '\nCHECKS.clear()\nCHECKS["plan-0"] = "false"\n',
            encoding="utf-8",
        )
        r = subprocess.run(
            ["bash", str(tmp / reader)],
            cwd=str(tmp),
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": str(tmp)},
        )
        return tmp, r

    def test_the_probe_does_not_print_a_failing_done_mark_as_done(self):
        _, r = self._run("scripts/state-probe.sh")
        line = [ln for ln in r.stdout.splitlines() if "plan-0" in ln]
        self.assertTrue(line, "the probe printed no line for the task:\n%s" % r.stdout)
        # ⬜, back on the queue: the row is not done, and it is not blocked either. It read ⛔
        # until 02.09, when he named the two as different states — blocked is an outside cause
        # held in blocked_by, and a failing acceptance means the work is simply back in hand.
        self.assertIn("⬜", line[0], "a ✅ whose command fails still reads as something other "
                                    "than unfinished: %r" % line[0])
        self.assertNotIn("✅", line[0])
        self.assertNotIn("⛔", line[0], "a row that is merely unfinished is drawn as blocked, "
                                       "which reserves that mark for a real outside cause: %r" % line[0])
        self.assertIn("its acceptance command fails", line[0])
        # And the tag beside the mark has to agree with the mark. The board's own reader stopped
        # saying "verified" here on 28.08 and the probe did not, so the two readers of one plan
        # disagreed on the row the whole change is about (found by the adversarial read that
        # evening).
        self.assertNotIn("verified", line[0],
                         "the probe still calls a row verified whose acceptance command fails, "
                         "while the board does not: %r" % line[0])
        self.assertIn("marked done", line[0])

    def test_the_probe_does_not_count_a_failing_done_mark_among_the_done(self):
        _, r = self._run("scripts/state-probe.sh")
        summary = [ln for ln in r.stdout.splitlines() if "more below ·" in ln]
        self.assertTrue(summary, "the probe printed no summary line:\n%s" % r.stdout)
        self.assertIn("0 done", summary[0],
                      "a ✅ whose command fails is still counted as done: %r" % summary[0])

    def test_the_board_does_not_draw_a_failing_done_mark_as_done(self):
        tmp, r = self._run("scripts/render-board.sh")
        page = (tmp / "board.html").read_text(encoding="utf-8")
        self.assertNotIn('<span class="chip">✅</span>', page,
                         "a ✅ whose command fails still wears the done chip:\n%s" % r.stdout)
        self.assertIn('<span class="chip">⬜</span>', page)
        self.assertNotIn('<span class="chip">⛔</span>', page,
                         "a row that is merely unfinished is drawn as blocked")
        self.assertIn("marked done in the plan, but its acceptance command fails", page)


class TestAKeyThatReadsThisMachineSaysSo(unittest.TestCase):
    """A key reaching outside the tracked tree reds on a fresh clone for a reason that is about
    the machine, and the note has to say so or the red reads as an alarm about the project."""

    def _note(self, command):
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import key_failure_note

        return key_failure_note(command, subprocess.run(command, shell=True, capture_output=True))

    def test_a_key_reaching_into_the_home_directory_is_named_as_machine_local(self):
        self.assertIn("reads this machine", self._note('test -f "$HOME/no-such-file-here"'))
        self.assertIn("reads this machine", self._note("test -f ~/no-such-file-here"))

    def test_a_key_reading_only_the_tree_is_not_named_as_machine_local(self):
        self.assertNotIn("reads this machine", self._note("test -f no-such-file-here"))

    def test_the_note_carries_the_commands_own_first_line(self):
        self.assertIn("the board has not been drawn", self._note("echo 'the board has not been "
                                                                 "drawn here yet'; false"))


if __name__ == "__main__":
    unittest.main()
