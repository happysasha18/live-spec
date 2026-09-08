"""A long run says what it is doing, and a closed row's real duration is readable — q-831.

Two things a person needs and did not have, both on paths that already existed and stopped short.

The acceptance-rerun gate printed its whole report after the last target returned, so a run that
takes hours said nothing at all while it ran and a watcher could not tell work from a hang. It
already settles its list of targets before the first one starts, so it can say what that list is
and then say each target as it moves.

`comparable_durations` measured a checkpoint file's birth and modification stamps, while
`_write_delivery_trail` in the same file explains why those are worthless: every write renames a
fresh file over the old one, so the span they yield is zero however long the work ran. The number
that means something is the one the close wrote down, and nothing read it back.

Both are driven here through the real thing — the gate as a subprocess over a throwaway repository,
and the reader through its own command — rather than by reading what either says about itself.
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from conftest import ROOT

SCRIPTS = Path(ROOT) / "scripts"
RERUN = Path(ROOT) / "guardrails" / "check-acceptance-rerun.py"
sys.path.insert(0, str(SCRIPTS))
_spec = importlib.util.spec_from_file_location("task_admission", SCRIPTS / "task-admission.py")
admission = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(admission)


def _git(tree, *args):
    return subprocess.run(["git", *args], cwd=str(tree), capture_output=True, text=True, check=True)


# ------------------------------------------------------------ 1. the run says what it is doing

# Each key names the same watched file, so the second commit below touches a file every row's
# acceptance names and the gate selects all three — the shape a real push has when a shared file
# moves.
CHECKS = {
    "q-one": "test -f watched.txt",
    "q-two": "test -f watched.txt",
    "q-three": "test -f watched.txt",
}


def _rerun_tree(tmp):
    """A throwaway tree with three done rows, each carrying its own acceptance command."""
    (tmp / "scripts").mkdir()
    for name in ("plan_checks_core.py", "checkpoint.py"):
        shutil.copy(SCRIPTS / name, tmp / "scripts" / name)
    (tmp / "scripts" / "plan_checks.py").write_text(
        "from plan_checks_core import evaluate  # noqa: F401\n"
        "from plan_checks_core import parse_tasks as _parse_tasks\n\n"
        "CHECKS = %r\n\n\ndef parse_tasks(text):\n    return _parse_tasks(text, CHECKS)\n" % CHECKS,
        encoding="utf-8")
    rows = "\n\n".join(
        "### ✅ Row %s — id: %s\n**Group:** Core · **Priority:** normal\n\n"
        "**Done when:** it is done\n\n**Verification:** true" % (rid, rid) for rid in CHECKS)
    (tmp / "PLAN.md").write_text("# Plan\n\n## Tasks\n\n%s\n" % rows, encoding="utf-8")
    (tmp / "watched.txt").write_text("v1\n", encoding="utf-8")
    _git(tmp, "init", "-q")
    _git(tmp, "config", "user.email", "t@example.invalid")
    _git(tmp, "config", "user.name", "t")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "base")
    base = _git(tmp, "rev-parse", "HEAD").stdout.strip()
    (tmp / "watched.txt").write_text("v2\n", encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "the watched file moves, so every row is selected")
    return base


def _run_gate(tmp, base, mode="release"):
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base, LIVE_SPEC_RUN_MODE=mode)
    env.pop("LIVE_SPEC_EVALUATING", None)
    env.pop("LIVE_SPEC_PUSH_FULL", None)
    return subprocess.run(
        [sys.executable, str(RERUN), "--plan", str(tmp / "PLAN.md"),
         "--checkpoints", str(tmp / ".live-spec" / "checkpoints")],
        cwd=str(tmp), env=env, capture_output=True, text=True, timeout=300)


class TestTheRunSaysWhatItIsDoing(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.dir.name)
        self.base = _rerun_tree(self.tmp)
        self.got = _run_gate(self.tmp, self.base)
        self.assertEqual(self.got.returncode, 0, self.got.stdout + self.got.stderr)

    def tearDown(self):
        self.dir.cleanup()

    def test_the_mode_and_the_whole_composition_come_before_the_first_target(self):
        out = self.got.stdout
        composition = out.index("composition fixed before the first target")
        self.assertLess(out.index("run mode: release"), composition)
        for rid in CHECKS:
            self.assertIn(rid, out[composition:out.index("\n", composition)])
        self.assertLess(composition, out.index("started"),
                        "a target started before the run said what the composition was")

    def test_every_target_is_named_when_it_starts_and_when_it_ends(self):
        out = self.got.stdout
        for rid in CHECKS:
            self.assertIn("-> %s started" % rid, out)
            self.assertIn("<- %s passed" % rid, out)

    def test_each_finish_says_how_many_are_still_to_come(self):
        counts = re.findall(r"\((\d+) of (\d+) finished, (\d+) to come\)", self.got.stdout)
        self.assertEqual(len(counts), len(CHECKS))
        self.assertEqual([c[0] for c in counts], ["1", "2", "3"])
        self.assertEqual([c[2] for c in counts], ["2", "1", "0"])
        self.assertTrue(all(c[1] == str(len(CHECKS)) for c in counts))

    def test_the_run_says_its_composition_never_grew(self):
        self.assertIn("the composition never grew: 3 target(s) named before the first started, "
                      "3 finished.", self.got.stdout)

    def test_a_failing_target_is_named_as_it_finishes_rather_than_only_at_the_end(self):
        """The live line carries the verdict, so a watcher sees the failure when it happens."""
        keys = self.tmp / "scripts" / "plan_checks.py"
        keys.write_text(keys.read_text(encoding="utf-8").replace(
            "'q-two': 'test -f watched.txt'", "'q-two': 'test -f gone.txt'"), encoding="utf-8")
        _git(self.tmp, "add", "-A")
        _git(self.tmp, "commit", "-qm", "one row's acceptance now fails")
        got = _run_gate(self.tmp, self.base)
        self.assertEqual(got.returncode, 1, got.stdout)
        self.assertIn("<- q-two FAILED", got.stdout)
        self.assertLess(got.stdout.index("<- q-two FAILED"), got.stdout.index("BLOCKED"))

    def test_nothing_here_reads_a_clock_or_watches_anything(self):
        """This output is for a person: it decides nothing and starts nothing.

        The verdict is what the acceptance commands returned, and the live lines carry no duration,
        no threshold and no comparison. The one timeout in this file is the emergency stop that
        already existed on the child process, and criterion 11 keeps it out of every verdict.
        """
        src = RERUN.read_text(encoding="utf-8")
        body = src[src.index("def say("):src.index("def main(")]
        for banned in ("time.time", "time.monotonic", "datetime", "sleep", "Thread(",
                       "loadavg", "elapsed", "poll("):
            self.assertNotIn(banned, body, "the live output reached for %r" % banned)


# --------------------------------------------- 2. the duration a close recorded, read back out

class TestTheDurationIsTheOneTheCloseRecorded(unittest.TestCase):

    def _sheet(self, tmp, rid, done_body):
        cps = tmp / ".live-spec" / "checkpoints"
        cps.mkdir(parents=True, exist_ok=True)
        (cps / ("%s.md" % rid)).write_text(
            "# %s\nStatus: closed\nOwner: pipeline\n\n## DONE\n\n%s\n\n## IN PROGRESS\n\n(nothing)\n"
            "\n## NEXT\n\n(nothing)\n" % (rid, done_body), encoding="utf-8")
        return cps

    def _plan(self, tmp, rid, group="Core"):
        (tmp / "PLAN.md").write_text(
            "# Plan\n\n## Tasks\n\n### ✅ A closed row — id: %s\n"
            "**Group:** %s · **Priority:** normal\n\n**Done when:** it is done\n" % (rid, group),
            encoding="utf-8")
        return tmp / "PLAN.md"

    def test_the_duration_comes_out_of_the_delivery_trail(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self._plan(tmp, "q-1")
            cps = self._sheet(tmp, "q-1", "OPENED: 2026-09-01T10:00:00\n"
                                          "estimate 3–5 hours → actual 1.7 hours")
            rows = admission.comparable_durations("Core", plan.read_text(encoding="utf-8"), cps)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "q-1")
            self.assertAlmostEqual(rows[0][1], 102.0)
            self.assertEqual(rows[0][2], "1.7 hours")

    def test_a_close_that_recorded_nothing_contributes_nothing(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self._plan(tmp, "q-1")
            cps = self._sheet(tmp, "q-1", "estimate 3–5 hours → actual not recorded")
            self.assertEqual(
                admission.comparable_durations("Core", plan.read_text(encoding="utf-8"), cps), [])

    def test_no_file_stamp_is_read(self):
        """The regression this row exists to close: the reader answered off the checkpoint file's
        own birth and modification times, and every write renames a fresh file over the old one, so
        the span was zero however long the work ran. Touching the file moves nothing here."""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self._plan(tmp, "q-1")
            cps = self._sheet(tmp, "q-1", "estimate 3–5 hours → actual 1.7 hours")
            before = admission.comparable_durations("Core", plan.read_text(encoding="utf-8"), cps)
            os.utime(cps / "q-1.md", (0, 0))
            after = admission.comparable_durations("Core", plan.read_text(encoding="utf-8"), cps)
            self.assertEqual(before, after)
            self.assertAlmostEqual(after[0][1], 102.0)

    def test_the_group_is_the_basis_and_another_group_is_not_read(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self._plan(tmp, "q-1", group="Core")
            cps = self._sheet(tmp, "q-1", "estimate 1–2 hours → actual 40 minutes")
            self.assertEqual(len(admission.comparable_durations(
                "Core", plan.read_text(encoding="utf-8"), cps)), 1)
            self.assertEqual(admission.comparable_durations(
                "Some other group", plan.read_text(encoding="utf-8"), cps), [])


class TestTheHistoryCommand(unittest.TestCase):
    """The end a person reaches: one command, its source and its basis named, or `unavailable`."""

    def _run(self, tmp, scope):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "task-admission.py"), "history", scope,
             "--plan", str(tmp / "PLAN.md"),
             "--checkpoints", str(tmp / ".live-spec" / "checkpoints")],
            capture_output=True, text=True, timeout=60)

    def _tree(self, tmp, trail):
        (tmp / "PLAN.md").write_text(
            "# Plan\n\n## Tasks\n\n### ✅ A closed row — id: q-1\n"
            "**Group:** Core · **Priority:** normal\n\n**Done when:** it is done\n",
            encoding="utf-8")
        cps = tmp / ".live-spec" / "checkpoints"
        cps.mkdir(parents=True)
        (cps / "q-1.md").write_text(
            "# q-1\nStatus: closed\nOwner: pipeline\n\n## DONE\n\n%s\n\n## IN PROGRESS\n\n(nothing)"
            "\n\n## NEXT\n\n(nothing)\n" % trail, encoding="utf-8")

    def test_it_names_the_row_the_duration_the_source_and_the_basis(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self._tree(tmp, "estimate 3–5 hours → actual 1.7 hours")
            got = self._run(tmp, "Core")
            self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
            self.assertIn("q-1", got.stdout)
            self.assertIn("1.7 hours", got.stdout)
            self.assertIn("delivery trail", got.stdout)
            self.assertIn("**Group:** line", got.stdout)

    def test_a_group_straddling_the_hour_line_reports_one_unit(self):
        """`_span` switches to hours at ninety minutes, so a group with a 40-minute row and a
        102-minute row yielded its two ends in different units and printed them under one label —
        "40 to 1.7 minutes" in the verifier's own run of 2026-09-09."""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self._tree(tmp, "estimate 1–2 hours → actual 40 minutes")
            plan = tmp / "PLAN.md"
            plan.write_text(plan.read_text(encoding="utf-8")
                            + "\n### ✅ A second closed row — id: q-2\n"
                              "**Group:** Core · **Priority:** normal\n\n"
                              "**Done when:** it is done\n", encoding="utf-8")
            (tmp / ".live-spec" / "checkpoints" / "q-2.md").write_text(
                "# q-2\nStatus: closed\nOwner: pipeline\n\n## DONE\n\n"
                "estimate 1–2 hours → actual 1.7 hours\n\n## IN PROGRESS\n\n(nothing)\n\n"
                "## NEXT\n\n(nothing)\n", encoding="utf-8")

            out = self._run(tmp, "Core").stdout
            self.assertIn("range of what they actually took: 0.7 to 1.7 hours", out)

    def test_it_says_unavailable_where_no_closed_row_recorded_one(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self._tree(tmp, "estimate 3–5 hours → actual not recorded")
            got = self._run(tmp, "Core")
            self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
            self.assertIn("unavailable", got.stdout)

    def test_it_forecasts_nothing(self):
        """It reports what was recorded. No forecast, no measure of how alike two rows are, no
        deadline, no budget, and no ordering read off past hours."""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self._tree(tmp, "estimate 3–5 hours → actual 1.7 hours")
            out = self._run(tmp, "Core").stdout.lower()
            for banned in ("predict", "forecast", "expect", "similar", "score", "deadline",
                           "limit", "priority", "should take"):
                self.assertNotIn(banned, out, "the history reader offered %r" % banned)


# ---------------------------------------------------------------------- 3. the release itself

def test_the_pack_is_stamped_and_carries_its_host_chapter():
    assert (Path(ROOT) / "VERSION").read_text(encoding="utf-8").strip() == "6.1.2"
    assert "### 6.1.2" in (Path(ROOT) / "MIGRATION.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
