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
import sys
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)
PLAN = ROOT / "PLAN.md"
READERS = ("scripts/state-probe.sh", "scripts/render-board.sh")

# What a reader needs from the tree to run at all: the plan it reads, the two reader scripts, the
# one home the checks now live in, and the checkpoint readers the probe uses to decide whether a
# done row's recorded state still holds (q-826) — without these two, the probe's own
# `import task_admission` fails to load, silently, and its recheck line never fires.
NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh",
          "scripts/plan_checks.py", "scripts/plan_checks_core.py",
          "scripts/task-admission.py", "scripts/checkpoint.py")


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
        # The probe runs no acceptance command at all now (q-826) — CHECKS["plan-0"] = "false"
        # above is planted for the board's own test below and never reaches the probe. A ✅ can
        # no longer be contradicted by a live re-run there; instead it is caught by the recorded-
        # state read, because this fixture carries no checkpoint for plan-0 at all. The guarantee
        # this test held — a done mark that cannot be trusted must not print as plain done — is
        # now the recheck line's job, not the ranked list's.
        _, r = self._run("scripts/state-probe.sh")
        body_lines = [ln for ln in r.stdout.splitlines()
                      if "plan-0" in ln and "need a fresh check" not in ln]
        self.assertFalse(body_lines,
                         "a done row with no checkpoint to confirm it still printed in the main "
                         "list: %r" % body_lines)
        recheck = [ln for ln in r.stdout.splitlines() if "need a fresh check" in ln]
        self.assertTrue(recheck, "the probe printed no recheck line:\n%s" % r.stdout)
        self.assertIn("1 done row(s)", recheck[0],
                     "a done row with no checkpoint was not counted as needing a fresh check: %r"
                     % recheck[0])
        # A single-row fixture with no push history — plan-0 is not one of the (normally 0-1)
        # rows this push just closed, so it is not named by id here; a person reads the count and
        # the pointer to the board, not a second copy of the plan's own done list (q-822).
        self.assertIn("full list on the board", recheck[0])

    def test_the_probe_counts_a_failing_done_mark_among_the_open(self):
        # Same fixture, same reasoning as above: the probe never runs plan-0's command, so the
        # row cannot be reopened by a live result. It also cannot count as quietly finished —
        # the recheck line has to carry it instead of the summary staying silent about it.
        _, r = self._run("scripts/state-probe.sh")
        summary = [ln for ln in r.stdout.splitlines() if "more below ·" in ln]
        self.assertTrue(summary, "the probe printed no summary line:\n%s" % r.stdout)
        self.assertIn("0 open", summary[0],
                      "a done row with no checkpoint is counted as open work, which is not what "
                      "the recorded-state read decides: %r" % summary[0])
        recheck = [ln for ln in r.stdout.splitlines() if "need a fresh check" in ln]
        self.assertTrue(recheck, "the probe printed no recheck line:\n%s" % r.stdout)
        self.assertIn("1 done row(s)", recheck[0],
                     "an unconfirmed done row left no trace at all: %r" % recheck[0])

    def test_the_board_does_not_draw_a_failing_done_mark_as_done(self):
        tmp, r = self._run("scripts/render-board.sh")
        page = (tmp / "board.html").read_text(encoding="utf-8")
        self.assertNotIn('<span class="mk">✅</span>', page,
                         "a ✅ whose command fails still wears the done chip:\n%s" % r.stdout)
        self.assertIn('<span class="mk">🔁</span>', page)
        self.assertNotIn('<span class="mk">⛔</span>', page,
                         "a row that is merely unfinished is drawn as blocked")
        self.assertNotIn('<span class="mk">⬜</span>', page,
                         "a reopened row is drawn as queued, which reserves that mark for work "
                         "that never started")
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


class TestAKeyCannotHideAFailureInsideAPipe(unittest.TestCase):
    """A key runs under `set -o pipefail`, so a trailing `grep` cannot pass for a failing pipe.

    Without it, `<something red> | grep -q ''` exits on grep's own status and reads green while
    the thing the key exists to test is red — the shape that closed a row on a grader's own
    conditional line rather than on its result (q-823, 2026-09-06).
    """

    def _evaluate(self, command):
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks_core import evaluate

        task = {"mark": "\u2705", "check": command, "blocked_by": None}
        return evaluate([task])[0]

    def test_a_failing_command_inside_a_pipe_reads_red(self):
        # The key named in the order, `false | grep -q ''`, was already red before pipefail —
        # grep finds nothing in an empty stream and exits 1 on its own. The key that actually
        # hid a failure is the one whose failing command PRINTS the line the grep looks for
        # first, which is the exact shape of the q-823 incident: a grader that printed
        # `shared reds: 0` and then exited 1.
        self.assertFalse(self._evaluate("false | grep -q ''")["ok"])
        self.assertFalse(self._evaluate("{ echo 'shared reds: 0'; false; } | "
                                        "grep -q 'shared reds: 0'")["ok"])

    def test_a_pipe_whose_every_stage_passes_still_reads_green(self):
        self.assertTrue(self._evaluate("echo hi | grep -q hi")["ok"])


if __name__ == "__main__":
    unittest.main()


class TestAPassingCommandDoesNotCloseARow(unittest.TestCase):
    """The mark governs. A row leaves the open list through `verify` and `close`, never because
    its acceptance command started to pass.

    `evaluate` drew ✅ on any passing command whatever the row's own mark said. So on 2026-09-06
    the probe printed "0 open" and "every row is finished" while q-816 stood 🔄 with a holder on
    it, and the board filed that row's card under Done as *landed*. The command tells whether the
    work would pass acceptance today; it does not perform the close.
    """

    PLAN = (
        "# Plan\n\n## Tasks\n\n"
        "### 🔄 A task in hand whose key already passes — id: plan-0\n"
        "**Group:** Machinery · **Priority:** normal\n"
        "**Source:** the test.\n\n"
        "Its acceptance command is `true`, and nobody has closed it.\n\n"
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
            checks.read_text(encoding="utf-8") + '\nCHECKS.clear()\nCHECKS["plan-0"] = "true"\n',
            encoding="utf-8",
        )
        r = subprocess.run(
            ["bash", str(tmp / reader)], cwd=str(tmp), capture_output=True, text=True,
            env={**os.environ, "HOME": str(tmp)},
        )
        return tmp, r

    def test_the_probe_keeps_the_rows_own_mark_and_counts_it_open(self):
        # The probe runs no command at all now (q-826), so "acceptance passes" — an annotation
        # that only ever came from a live result — can no longer appear; the guarantee this test
        # held is the stronger one that replaced it: nothing on the row's line can come from a
        # run that never happens, and the mark still governs, so the row stays open regardless.
        _, r = self._run("scripts/state-probe.sh")
        line = [ln for ln in r.stdout.splitlines() if "plan-0" in ln]
        self.assertTrue(line, "the probe printed no line for the task:\n%s" % r.stdout)
        self.assertIn("🔄", line[0], "a row in hand was promoted by its own command: %r" % line[0])
        self.assertNotIn("✅", line[0])
        self.assertIn("declared", line[0],
                      "the row's line claims a command decided something, though the probe runs "
                      "none: %r" % line[0])
        self.assertNotIn("acceptance", line[0],
                         "the probe still reports on a command result it never computed: %r"
                         % line[0])
        summary = [ln for ln in r.stdout.splitlines() if "more below ·" in ln]
        self.assertTrue(summary, "the probe printed no summary line:\n%s" % r.stdout)
        self.assertIn("1 open", summary[0],
                      "work in hand is counted as finished: %r" % summary[0])
        self.assertNotIn("every row is finished", r.stdout,
                         "the probe called the plan finished over a row in hand:\n%s" % r.stdout)

    def test_the_board_stands_the_row_in_work_and_not_in_done(self):
        tmp, r = self._run("scripts/render-board.sh")
        page = (tmp / "board.html").read_text(encoding="utf-8")
        inwork = page.split("col inwork", 1)[-1].split("col ready", 1)[0]
        self.assertIn("card-plan-0", inwork,
                      "the row in hand left the in-work column:\n%s" % r.stdout)
        self.assertNotIn("landed", page.split("<h2>Done</h2>", 1)[-1].split("</div>", 1)[0])
        self.assertIn("a card leaves when its row closes", page,
                      "the in-work column still says a passing command empties it")

class TestAReaderNeverRunsInsideACheck(unittest.TestCase):
    """The circuit breaker: an acceptance command can never re-enter the probe or the renderer.

    evaluate() runs every key; a key that runs a reader runs evaluate() again, and each level
    plants a copy of the tree. On 2026-09-06 two board keys did exactly that, and the fan-out
    reached hundreds of renderers four levels deep and a load average past 160 before it was
    killed by hand. The breaker lives in the one home every reader shares, plan_checks_core:
    run_key() marks each child with LIVE_SPEC_EVALUATING and evaluate() refuses to start under
    that mark — exit 3, one line, no child of its own. So the depth is one, whatever a key says.
    """

    PLAN = (
        "# Plan\n\n## Tasks\n\n"
        "### ✅ A key that runs the probe — id: plan-0\n"
        "**Group:** Machinery · **Priority:** normal\n"
        "**Source:** the test.\n\n"
        "Its acceptance command runs the probe itself.\n\n"
        "## Blockers\n\n- none\n"
    )

    def _plant(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, str(tmp), True)
        for rel in NEEDED:
            dst = tmp / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        (tmp / "PLAN.md").write_text(self.PLAN, encoding="utf-8")
        checks = tmp / "scripts" / "plan_checks.py"
        # The key counts its own entries, then runs the probe: without the breaker every level
        # appends a line and starts another level; with it the inner probe refuses at once. The
        # key stops itself at three lines, so the red-proof against a core with no breaker is
        # bounded by construction and can never fan out.
        checks.write_text(
            checks.read_text(encoding="utf-8")
            + '\nCHECKS.clear()\nCHECKS["plan-0"] = "echo x >> depth.txt && test $(wc -l < depth.txt) -lt 3 && bash scripts/state-probe.sh >/dev/null 2>depth.err; test $? -eq 3"\n',
            encoding="utf-8",
        )
        return tmp

    def test_a_key_that_runs_the_probe_stops_at_depth_one(self):
        # The probe itself no longer runs any row's key (q-826), so it can no longer be the
        # driver that starts this chain — a key only ever runs today from inside the board
        # renderer, which still executes CHECKS by default. The breaker this test holds is the
        # one shared home, plan_checks_core, so entering through the renderer still proves it:
        # the renderer runs plan-0's key, that key calls into the probe, and the probe's own
        # evaluate() call (it still makes that call, just with every row's command already
        # nulled) sees LIVE_SPEC_EVALUATING on it and refuses before touching a row.
        tmp = self._plant()
        env = {k: v for k, v in os.environ.items() if k != "LIVE_SPEC_EVALUATING"}
        env["HOME"] = str(tmp)
        r = subprocess.run(["bash", str(tmp / "scripts" / "render-board.sh")], cwd=str(tmp),
                           capture_output=True, text=True, env=env, timeout=120)
        depth = (tmp / "depth.txt").read_text(encoding="utf-8").count("x") if (tmp / "depth.txt").exists() else 0
        self.assertEqual(depth, 1, "the probe re-entered itself %d level(s) deep" % depth)
        err = (tmp / "depth.err").read_text(encoding="utf-8") if (tmp / "depth.err").exists() else ""
        self.assertIn("refuses to re-enter", err, "the inner probe did not refuse with the breaker's line: %r" % err)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])

    def test_evaluate_refuses_under_the_mark_before_reading_a_row(self):
        r = subprocess.run([sys.executable, "-c",
                            "import sys; sys.path.insert(0, 'scripts'); import plan_checks_core as c; c.evaluate([])"],
                           cwd=str(ROOT), capture_output=True, text=True,
                           env={**os.environ, "LIVE_SPEC_EVALUATING": "1"})
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertIn("refuses to re-enter", r.stderr)
