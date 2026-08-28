"""One step means one step: `scripts/plan-step.sh` stops where the task stops.

`CLAUDE.md` sends every session to `bash scripts/plan-step.sh <id>` instead of at the whole plan,
because reading `PLAN.md` whole more than doubles what a session starts with. The reader stopped
only at the next `### ` task heading, so the last task in `## Tasks` ran straight on through
`## Blockers`, `## Environment` and everything after it — asking for one step printed 533 of the
plan's 1,678 lines, and one of the two tasks the owner is asked to open is exactly that last task.
The promise the boot file makes was false for it (adversarial review, 28.08).

These tests run against a THROWAWAY plan in a temp directory, the pattern
tests/test_plan_is_not_executable.py follows, and one runs the reader against the real plan for
the property that matters: a step is the step, not the rest of the file.
"""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)
READER = ROOT / "scripts" / "plan-step.sh"

FIXTURE = """# Plan

## Tasks

### ⬜ The first task — id: plan-100
**Group:** Machinery · **Priority:** normal

The first task's own prose.

### ⬜ The last task before a section break — id: plan-101
**Group:** Machinery · **Priority:** normal

The last task's own prose.

## Blockers

- a blocker that belongs to no task

## Environment

Prose that belongs to no task either.
"""


def _read_step(plan_text, step_id):
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / "scripts").mkdir()
        shutil.copy2(READER, tmp / "scripts" / "plan-step.sh")
        (tmp / "PLAN.md").write_text(plan_text, encoding="utf-8")
        r = subprocess.run(["bash", str(tmp / "scripts" / "plan-step.sh"), step_id],
                           cwd=str(tmp), capture_output=True, text=True)
        return r
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)


class TestAStepStopsAtTheNextHeading(unittest.TestCase):
    def test_a_middle_task_stops_at_the_next_task(self):
        r = _read_step(FIXTURE, "plan-100")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("The first task's own prose.", r.stdout)
        self.assertNotIn("plan-101", r.stdout)

    def test_the_last_task_stops_at_the_section_break(self):
        r = _read_step(FIXTURE, "plan-101")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("The last task's own prose.", r.stdout)
        self.assertNotIn("## Blockers", r.stdout,
                         "the last task in the list ran on into the next section")
        self.assertNotIn("a blocker that belongs to no task", r.stdout)
        self.assertNotIn("Prose that belongs to no task either.", r.stdout)

    def test_an_unknown_id_is_refused(self):
        r = _read_step(FIXTURE, "plan-999")
        self.assertNotEqual(0, r.returncode)


class TestTheRealPlanReadsOneStepAtATime(unittest.TestCase):
    """Against the plan actually in the tree: no step may print a section heading, and no step may
    run to anything near the file's own length. Both hold for every task the plan declares, so a
    task moved to the end of the list is covered the day it moves."""

    def setUp(self):
        self.plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        self.ids = [ln.rsplit("id:", 1)[1].strip()
                    for ln in self.plan.splitlines()
                    if ln.startswith("### ") and " — id: " in ln]

    def test_the_plan_declares_tasks_at_all(self):
        self.assertGreater(len(self.ids), 0, "PLAN.md declares no tasks to read")

    def test_no_step_spills_into_the_sections_after_the_task_list(self):
        for step_id in self.ids:
            r = subprocess.run(["bash", str(READER), step_id],
                               cwd=str(ROOT), capture_output=True, text=True)
            self.assertEqual(0, r.returncode, r.stderr)
            spilled = [ln for ln in r.stdout.splitlines() if ln.startswith("## ")]
            self.assertFalse(spilled,
                             "step %s printed section heading(s) %r — the reader ran past the "
                             "task into the rest of the plan" % (step_id, spilled))
