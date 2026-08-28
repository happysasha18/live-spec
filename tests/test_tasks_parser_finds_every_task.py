"""Neither reader is allowed to silently stop finding tasks.

Commit bc6f862b replaced PLAN.md's `## Steps` section with a `## Tasks` section carrying 160
entries, and both readers kept parsing the old shape — `scripts/state-probe.sh` printed an
empty PLAN block and `scripts/render-board.sh` wrote a board with 0 tasks, on a green exit
code from both. Nothing red-flagged that: the readers just quietly found nothing. This is the
regression this file exists to catch, the next time PLAN.md's shape moves again.

Three checks, each independent of `scripts/plan_checks.py`'s own `parse_tasks()` (a fresh
regex against PLAN.md's raw text, not a re-import of the thing being tested):

  - `scripts/render-board.sh` renders every id PLAN.md's `## Tasks` section declares — no
    more, no fewer. The board shows everything (it is a page, not a chat reply), so this is
    the direct "the reader found every task" proof.
  - every id `scripts/state-probe.sh` prints is a real declared task — it never invents one.
  - the probe's own numbers add up: the tasks it shows, plus its own "N more below" count,
    plus its own "done" count, equal PLAN.md's total declared task count. The probe only
    prints the top of the list (CLAUDE.md's Canon report is capped at seven to ten lines), so
    it cannot be checked by counting printed lines the way the board can — this checks that
    its bookkeeping never drops or double-counts a task, which is what "stopped finding the
    tasks" would look like from a reader that only shows a subset.

Runs against a THROWAWAY COPY of the repo in a temp directory, following the pattern in
tests/test_plan_is_not_executable.py: never touches the real PLAN.md, never mutates the
working tree.
"""
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)

NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh", "scripts/plan_checks.py")

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# A fresh, independent read of PLAN.md's own task-header shape — deliberately not importing
# scripts/plan_checks.py's parse_tasks(), since the point is to notice if THAT parser (and so
# both readers built on it) stops matching PLAN.md's real shape.
_DECLARED_HEADER_RE = re.compile(r"^### \S+ .+? — id: (\S+)$")

# render-board.sh's card carries its id in the meta line:
#   <div class="meta">Group · priority priority · id</div>
# "priority" can itself be two words ("quick win"), so the id is whatever sits between the
# LAST " · " and the closing tag — the lazy .*? backtracks to find that split correctly.
_BOARD_META_ID_RE = re.compile(r'<div class="meta">.*? · (\S+)</div>')

# state-probe.sh's PLAN line: "  <icon> <title>  (<id>) <verified-or-declared>[ — <reason>][  <-- NEXT]"
_PROBE_LINE_RE = re.compile(
    r"^(?:✅|🔄|⛔|⬜|👁️)\s+.+?\s+\((\S+)\)\s+(?:verified|declared)(?:\s+—\s+.+?)?(?:\s*<-- NEXT)?\s*$"
)
# state-probe.sh's summary line: "  … N more below · M done · full list in PLAN.md / board.html"
_PROBE_SUMMARY_RE = re.compile(r"… (\d+) more below · (\d+) done")


def _declared_ids(plan_text):
    ids = []
    in_section = False
    for line in plan_text.splitlines():
        if line.strip() == "## Tasks":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        m = _DECLARED_HEADER_RE.match(line.rstrip())
        if m:
            ids.append(m.group(1))
    return ids


class TestNeitherReaderStopsFindingTheTasks(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)
        for rel in NEEDED:
            dst = self.tmp / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        self.plan_text = (self.tmp / "PLAN.md").read_text(encoding="utf-8")
        self.declared = _declared_ids(self.plan_text)

    def tearDown(self):
        self._tmp.cleanup()

    def test_the_fixture_actually_declares_tasks(self):
        # A guard on the guard: if this is ever 0, every other assertion below would pass
        # vacuously (an empty set matches an empty set), which is exactly the bug this file
        # exists to catch.
        self.assertGreater(len(self.declared), 0, "PLAN.md's ## Tasks section declares no tasks")
        self.assertEqual(
            len(self.declared), len(set(self.declared)),
            "PLAN.md declares the same task id more than once",
        )

    def test_board_renders_every_declared_id_and_no_others(self):
        out = self.tmp / "board.html"
        r = subprocess.run(
            ["bash", str(self.tmp / "scripts" / "render-board.sh"), str(out)],
            cwd=str(self.tmp), capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, "render-board.sh failed: " + r.stdout + r.stderr)
        rendered_ids = _BOARD_META_ID_RE.findall(out.read_text(encoding="utf-8"))
        self.assertTrue(rendered_ids, "the board rendered no task ids — its meta markup "
                                       "changed; update _BOARD_META_ID_RE")
        declared_set, rendered_set = set(self.declared), set(rendered_ids)
        self.assertEqual(
            declared_set, rendered_set,
            "the board and PLAN.md disagree on which tasks exist — missing from the board: "
            "%r; on the board but not declared: %r"
            % (sorted(declared_set - rendered_set), sorted(rendered_set - declared_set)),
        )
        self.assertEqual(
            len(self.declared), len(rendered_ids),
            "the board rendered a different NUMBER of task cards than PLAN.md declares tasks",
        )

    def _run_probe(self):
        r = subprocess.run(
            ["bash", str(self.tmp / "scripts" / "state-probe.sh")],
            cwd=str(self.tmp), capture_output=True, text=True,
        )
        return _ANSI_RE.sub("", r.stdout)

    def test_probe_never_prints_an_id_plan_md_does_not_declare(self):
        plain = self._run_probe()
        shown_ids = [
            m.group(1) for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip()))
        ]
        self.assertTrue(shown_ids, "the probe printed no task ids — its PLAN-section print "
                                    "shape changed; update _PROBE_LINE_RE")
        unknown = set(shown_ids) - set(self.declared)
        self.assertFalse(unknown, "the probe printed id(s) PLAN.md never declared: %r" % sorted(unknown))

    def test_probe_summary_accounts_for_every_declared_task(self):
        plain = self._run_probe()
        shown_ids = {
            m.group(1) for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip()))
        }
        m = _PROBE_SUMMARY_RE.search(plain)
        self.assertIsNotNone(
            m, "the probe printed no summary line — a person can no longer see how much is "
               "left below or how much is done",
        )
        more_below, done = int(m.group(1)), int(m.group(2))
        self.assertEqual(
            len(shown_ids) + more_below + done, len(self.declared),
            "shown (%d) + more-below (%d) + done (%d) = %d, but PLAN.md declares %d tasks — "
            "the probe silently lost or double-counted some"
            % (len(shown_ids), more_below, done, len(shown_ids) + more_below + done, len(self.declared)),
        )


class TestTheAcceptanceCommandsStayHonestMachinery(unittest.TestCase):
    """The acceptance-command table is machinery that runs at every session start, everywhere.

    `scripts/plan_checks.py`'s CHECKS map is read by both readers and executed by the probe,
    which is the first command a session runs on any machine that opens this project. Two
    properties keep that from turning into a cost nobody asked for, and neither is guarded by
    the tests above, which look only at what the readers print.

    Both were written 2026-08-28 with plan-10's own thirteen keys, and both name a thing that
    already happened here. A key outliving its row is the first: plan-1's key survived its task
    into the 28.08 board rotation and had to be removed by hand, still running every morning
    against a step that no longer existed. A key that writes is the second: PLAN.md's own trap
    list records `tests/test_guardrails.py` leaving a `git stash` unrestored on an interrupt,
    and a resume step that can do the same to a person's uncommitted work would be the worst
    possible place for it.
    """

    #: Commands that change the tree, the index, or the machine. A check exists to READ state.
    #: Each entry is matched as a whole word against the command text.
    WRITING_WORDS = (
        "rm", "rmdir", "mv", "cp", "truncate", "tee", "install", "chmod", "chown",
        "stash", "checkout", "restore", "reset", "clean", "commit", "push", "add",
        "kill", "pkill", "killall",
    )

    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import CHECKS
        self.checks = CHECKS
        self.declared = set(_declared_ids((ROOT / "PLAN.md").read_text(encoding="utf-8")))

    def test_the_fixture_actually_carries_checks(self):
        # The same guard-on-the-guard the class above keeps: an empty table would pass both
        # assertions below without reading anything.
        self.assertGreater(len(self.checks), 0, "scripts/plan_checks.py declares no checks")
        self.assertGreater(len(self.declared), 0, "PLAN.md's ## Tasks section declares no tasks")

    def test_every_key_names_a_task_the_plan_declares(self):
        orphans = sorted(set(self.checks) - self.declared)
        self.assertEqual(
            orphans, [],
            "scripts/plan_checks.py runs a command for %s, which PLAN.md's ## Tasks section no "
            "longer declares — the row was renamed, folded or archived and its command was left "
            "behind, running at every session start against nothing" % orphans,
        )

    def test_no_check_can_write_to_the_tree_or_the_machine(self):
        # A check is mostly greps, and a grep's PATTERN is prose that may legitimately contain
        # any of these words — "…run at every push" is a sentence in a skill file, not a command.
        # Patterns in this table are single-quoted, so the quoted spans come out before the
        # search and what is left is the shell's own words.
        for task_id, raw in sorted(self.checks.items()):
            command = re.sub(r"'[^']*'", " ", raw)
            for word in self.WRITING_WORDS:
                self.assertIsNone(
                    re.search(r"(?<![\w./-])%s(?![\w-])" % re.escape(word), command),
                    "the check for %s runs %r, and a check exists to read state, never to "
                    "change it — this one runs on every machine that opens this project, "
                    "before anyone has decided anything" % (task_id, word),
                )


if __name__ == "__main__":
    unittest.main()
