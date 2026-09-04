"""Every open row on the board says what raised it (rule 41, PLAN q-825).

The owner's own words, 2026-09-04, about two of his projects at once: the titles read plainly and
he still cannot tell where any row came from, so he sees work producing work and cannot control it.
On this project's own board that day, four of five open rows had been raised by the pack's own
reviews rather than by him, and nothing he reads said so.

The load-bearing case is the last one: a row naming a word outside the three is refused, so the
vocabulary cannot quietly grow a fourth member that means "a session decided".
"""
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(REPO, "guardrails", "check-row-origin.py")

ROW = """### {mark} {title} — id: {rid}
**Group:** G · **Priority:** normal{raised}
**Source:** the fixture.

"""


def plan(rows):
    return "# demo — Plan\n\n## Tasks\n\n" + "".join(rows)


def row(rid, mark="⬜", raised="asked", title="A row of the fixture's own"):
    tail = "" if raised is None else " · **Raised:** %s" % raised
    return ROW.format(mark=mark, title=title, rid=rid, raised=tail)


class TheBoardSaysWhoRaisedEachRow(unittest.TestCase):
    def run_guard(self, text):
        d = tempfile.mkdtemp(prefix="livespec-row-origin-")
        path = os.path.join(d, "PLAN.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return subprocess.run(["python3", GUARD, path], capture_output=True, text=True)

    def test_a_row_that_names_its_origin_passes(self):
        r = self.run_guard(plan([row("d-1", raised="asked"), row("d-2", raised="found"),
                                 row("d-3", raised="sent")]))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("3 open row(s)", r.stdout)

    def test_a_row_that_names_nothing_reds_and_is_named(self):
        r = self.run_guard(plan([row("d-1"), row("d-2", raised=None)]))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("d-2", r.stdout)
        self.assertNotIn("d-1,", r.stdout)

    def test_a_word_outside_the_three_reds(self):
        r = self.run_guard(plan([row("d-1", raised="decided")]))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("outside the three words", r.stdout)
        self.assertIn("decided", r.stdout)

    def test_a_closed_row_is_not_read(self):
        r = self.run_guard(plan([row("d-1", mark="✅", raised=None), row("d-2", raised="asked")]))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_this_project_own_board_names_every_origin(self):
        r = subprocess.run(["python3", GUARD], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_the_parser_reads_the_word_off_the_row(self):
        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import plan_checks_core as core
        tasks = core.parse_tasks(plan([row("d-1", raised="found")]))
        self.assertEqual(tasks[0]["raised"], "found")
        self.assertEqual(tasks[0]["priority"], "normal")
        self.assertEqual(core.RAISED_WORDS, ("asked", "found", "sent"))

    def test_a_row_written_without_the_field_still_parses(self):
        """A plan mid-edit must still read. The guard is what refuses it, never the parser."""
        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import plan_checks_core as core
        tasks = core.parse_tasks(plan([row("d-1", raised=None)]))
        self.assertIsNone(tasks[0]["raised"])
        self.assertEqual(tasks[0]["priority"], "normal")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
