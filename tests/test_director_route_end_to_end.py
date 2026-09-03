"""tests/test_director_route_end_to_end.py — the task lifecycle, walked on a scratch host (PLAN.md, q-812).

The Director's route already has its per-piece proofs: `tests/test_checkpoint_mechanism.py` holds
every branch of `scripts/checkpoint.py`, and `tests/test_plan_is_not_executable.py` holds a done mark
against a failing key inside this pack's own tree. What none of them walk is the ROUTE: one piece of
work, on one clean host, from the turn that accepts it to the turn that closes it, through the same
commands a session actually runs.

So the host here is real. `adopt/install-status-view.sh` vendors the probe and the shared parser into
a fresh git repository the way it vendors them into any host, `scripts/checkpoint.py` is copied in
beside them, and the plan is the host's own. No model runs: the routing decision is played by the
test — "the Director already read this turn as an instruction" — and what is asserted is the
mechanical consequence, which is the half a deterministic test can hold. Whether the reading itself
was right is the other half, and it lives where it already lived, in `evals/director/`.

The four rows this file carries:

  M-630  an accepted turn leaves exactly one row and one checkpoint carrying a real sheet, and a
         turn that accepts nothing leaves the tree exactly as it was found
  M-631  a correction lands on the same checkpoint file, and the create operation is the one that
         would lose it
  M-632  a done mark whose acceptance command fails reads reopened, and reads done again on the
         command alone
  M-633  the recorded state names one next action, the same one on every reading

Every one of the four is proven red-then-green against the host rather than against a description of
it: the state is mutated, the real reader is run, and the reading is asserted to move.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL = os.path.join(ROOT, "adopt", "install-status-view.sh")

#: The host's own plan. Two open rows, so naming which one runs next is a real choice rather than
#: the only row there is. The ids share no name with any row of this pack's own PLAN.md.
HOST_PLAN = """# route-host — Plan

## Tasks

### 🔄 Open the board by itself after a push — id: route-1
**Group:** Board · **Priority:** critical
**Source:** the person, in the turn this walk starts from.

The work this route carries from its first turn to its last.

### ⬜ Rename the export button — id: route-2
**Group:** Copy · **Priority:** normal
**Source:** the fixture.

A second open row, so the next-up answer has somewhere else it could have gone.

## Blockers

- **A blocker of the host's own.** Nothing of the pack's.
"""

#: What the person asked for, in their own words — the goal line of the sheet the accepted work
#: carries. Kept here so the test can assert the sheet holds the ask rather than a placeholder.
GOAL = "the board opens by itself after a push"

SHEET = (
    "Goal: %s. Outcome: a push leaves the board page open on the person's screen. "
    "Dimensions: product behaviour. Known: the board is drawn by a script already. "
    "Unknown: which hook the open belongs on. Risk: none, reversible. "
    "Specialist: developer. Evidence: a push opens the page. Next: write the open step." % GOAL
)


def host_checks(**commands):
    """The host's own acceptance-command map, written the way a host writes one."""
    entries = ", ".join("%r: %r" % (k.replace("_", "-"), v) for k, v in sorted(commands.items()))
    return ("from plan_checks_core import evaluate, key_failure_note, normalize_mark  # noqa: F401\n"
            "from plan_checks_core import parse_tasks as _parse_tasks\n"
            "CHECKS = {%s}\n"
            "def parse_tasks(text):\n"
            "    return _parse_tasks(text, CHECKS)\n" % entries)


def run(args, cwd):
    # No bytecode cache: this file rewrites the host's command map more than once in the same second
    # at the same size, which reads as unchanged, and the second run would answer with the first map.
    # Borrowed from tests/test_status_view_install.py, which met the same thing.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def snapshot(root):
    """Every tracked-shaped file in the host and its hash, `.git` left out.

    This is the detector the "nothing was created" half of M-630 rests on. A detector that sees
    nothing is worth nothing, so the same function is run either side of a turn that DOES accept
    work, and asserted to see it.
    """
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            full = os.path.join(base, name)
            with open(full, "rb") as fh:
                out[os.path.relpath(full, root)] = hashlib.sha256(fh.read()).hexdigest()
    return out


class RouteHost(unittest.TestCase):
    """A fresh host per test: a git repository, the vendored readers, the checkpoint command."""

    def setUp(self):
        self.host = tempfile.mkdtemp(prefix="livespec-director-route-")
        self.addCleanup(shutil.rmtree, self.host, True)
        run(["git", "init", "-q"], cwd=self.host)
        run(["git", "config", "user.email", "a@example.com"], cwd=self.host)
        run(["git", "config", "user.name", "a"], cwd=self.host)
        write(os.path.join(self.host, "PLAN.md"), HOST_PLAN)
        run(["git", "add", "-A"], cwd=self.host)
        run(["git", "commit", "-qm", "the host's own first commit"], cwd=self.host)

        installed = run(["bash", INSTALL], cwd=self.host)
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)

        # The checkpoint command travels with the readers here: the route's own writes go through it.
        self.checkpoint = os.path.join(self.host, "scripts", "checkpoint.py")
        shutil.copy(os.path.join(ROOT, "scripts", "checkpoint.py"), self.checkpoint)
        self.checkpoints_dir = os.path.join(self.host, ".live-spec", "checkpoints")
        os.makedirs(self.checkpoints_dir)
        self.set_checks()

    # -- the host's own surfaces ---------------------------------------------------------------

    def set_checks(self, **commands):
        write(os.path.join(self.host, "scripts", "plan_checks.py"), host_checks(**commands))

    def probe(self):
        r = run(["bash", os.path.join(self.host, "scripts", "state-probe.sh")], cwd=self.host)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def cp(self, *args):
        return run([sys.executable, self.checkpoint] + list(args), cwd=self.host)

    def checkpoint_files(self):
        return sorted(os.listdir(self.checkpoints_dir))

    def plan(self):
        return read(os.path.join(self.host, "PLAN.md"))

    def set_plan(self, text):
        write(os.path.join(self.host, "PLAN.md"), text)

    def accept_the_turn(self):
        """What the route does when a turn is read as an instruction: one row, one checkpoint.

        The row is written into the plan (the queue is a document a person edits, and the pack
        claims no command that writes a row when somebody speaks — wish-intake criteria 6 and 9),
        and the sheet goes into the work's own checkpoint through the checkpoint command.
        """
        self.set_plan(self.plan().replace(
            "\n## Blockers",
            "\n### 🔄 Send the weekly digest — id: route-3\n"
            "**Group:** Reports · **Priority:** normal\n"
            "**Source:** the person, this turn.\n\n"
            "What the accepted turn asked for.\n\n## Blockers"))
        r = self.cp("new", os.path.join(self.checkpoints_dir, "route-3.md"),
                    "--title", "Send the weekly digest", "--owner", "director",
                    "--decision-sheet", SHEET)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestAnAcceptedTurnLeavesOneRowAndOneSheet(RouteHost):
    """M-630 — Requirement 314 criteria 1, 2 and 4; wish-intake Requirement 4 criteria 1 and 3."""

    def test_the_accepted_turn_leaves_exactly_one_row_and_one_checkpoint_holding_the_ask(self):
        before = snapshot(self.host)
        self.accept_the_turn()
        after = snapshot(self.host)

        added = sorted(set(after) - set(before))
        self.assertEqual(added, [os.path.join(".live-spec", "checkpoints", "route-3.md")],
                         "the accepted turn wrote something besides the work's own checkpoint")
        self.assertEqual(sorted(set(before) - set(after)), [])
        changed = sorted(p for p in set(before) & set(after) if before[p] != after[p])
        self.assertEqual(changed, ["PLAN.md"],
                         "the accepted turn changed a file other than the queue")

        self.assertEqual(self.checkpoint_files(), ["route-3.md"])
        sheet = read(os.path.join(self.checkpoints_dir, "route-3.md"))
        self.assertIn("## DECISION SHEET", sheet)
        self.assertIn(GOAL, sheet, "the sheet does not carry the person's own ask")
        self.assertEqual(self.cp("validate", os.path.join(self.checkpoints_dir, "route-3.md")).returncode, 0)

        # One row for the one ask, and the two rows already there are untouched.
        self.assertEqual(self.plan().count("— id: route-3"), 1)
        for row in ("route-1", "route-2"):
            self.assertIn("— id: %s" % row, self.plan())

    def test_a_checkpoint_with_no_sheet_is_refused_before_it_reaches_disk(self):
        """The preventive half, Requirement 314 criterion 4: accepted work carries a real sheet,
        and a first-read-owned checkpoint without one is refused rather than written empty."""
        r = self.cp("new", os.path.join(self.checkpoints_dir, "route-3.md"),
                    "--title", "Send the weekly digest", "--owner", "director")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("cannot be created without decision_sheet", r.stdout)
        self.assertEqual(self.checkpoint_files(), [], "the refused checkpoint reached disk anyway")

    def test_a_turn_that_accepts_nothing_leaves_the_host_exactly_as_it_was(self):
        """The negative case, wish-intake criterion 3 and Requirement 313 criterion 5.

        A question and a halt run no command that writes: the route's writing step is the one
        `accept_the_turn` performs, and a turn read as either of those never reaches it. Asserting
        that on its own would be asserting nothing, so the same detector is run over an accepting
        turn in the same test and has to see it.
        """
        before = snapshot(self.host)
        # the question turn, and the halt turn: read, answered, and nothing written
        self.assertEqual(snapshot(self.host), before, "a turn that accepted nothing changed the host")
        self.assertEqual(self.checkpoint_files(), [])
        self.assertNotIn("— id: route-3", self.plan())

        self.accept_the_turn()
        self.assertNotEqual(snapshot(self.host), before,
                            "the detector cannot see an accepted turn, so it proves nothing about "
                            "a turn that accepted none")


class TestACorrectionLandsOnTheSameCheckpoint(RouteHost):
    """M-631 — Requirement 314 criteria 3, 11 and 12."""

    def setUp(self):
        super().setUp()
        self.accept_the_turn()
        self.path = os.path.join(self.checkpoints_dir, "route-3.md")
        r = self.cp("update", self.path, "--done", "- The digest's first draft is written.",
                    "--in-progress", "- Wiring the send step.")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_two_corrections_land_on_the_one_file_and_lose_nothing(self):
        for correction, mark in (("weekly, not daily", "weekly"), ("plain text, no html", "plain text")):
            r = self.cp("update", self.path,
                        "--next", "- Redo the send step: %s." % correction,
                        "--decision-sheet", SHEET + " Correction: %s." % correction)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            self.assertEqual(self.checkpoint_files(), ["route-3.md"],
                             "a correction opened a second checkpoint for one piece of work")
            body = read(self.path)
            self.assertIn(mark, body, "the correction did not reach the checkpoint")
            self.assertIn("The digest's first draft is written.", body,
                          "the correction discarded work already done")
            self.assertIn("Status: open", body)
            self.assertEqual(self.cp("validate", self.path).returncode, 0)

        # The plan gained no second row for either correction.
        self.assertEqual(self.plan().count("— id: route-3"), 1)
        self.assertEqual(len([l for l in self.plan().splitlines() if l.startswith("### ")]), 3)

    def test_the_create_operation_is_the_one_that_would_lose_the_work(self):
        """Criterion 12's second half, and the reason a correction goes through update.

        Red-then-green on the same file: create writes a blank template over it and the finished
        work is gone; update against the same path carries it through.
        """
        self.assertIn("The digest's first draft is written.", read(self.path))
        r = self.cp("new", self.path, "--title", "Send the weekly digest", "--owner", "director",
                    "--decision-sheet", SHEET)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("The digest's first draft is written.", read(self.path),
                         "create no longer overwrites, so criterion 12 says something untrue")
        self.assertEqual(self.checkpoint_files(), ["route-3.md"])

        self.cp("update", self.path, "--done", "- The digest's first draft is written.")
        self.assertIn("The digest's first draft is written.", read(self.path))

    def test_nothing_in_the_host_counts_a_piece_of_works_checkpoints(self):
        """Criterion 11, stated as what it is. The one-checkpoint rule is held by the reading
        skill's text; a second file opened for the same work passes every command the host has,
        and a test claiming otherwise would be certifying a guarantee nobody built."""
        second = os.path.join(self.checkpoints_dir, "route-3-again.md")
        r = self.cp("new", second, "--title", "Send the weekly digest", "--owner", "director",
                    "--decision-sheet", SHEET)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.checkpoint_files(), ["route-3-again.md", "route-3.md"])
        both = self.cp("validate", "--all")
        self.assertEqual(both.returncode, 0, both.stdout + both.stderr)
        self.assertEqual(self.probe().count("route-3"), 1,
                         "the probe reads the queue, so a second checkpoint is invisible to it")


class TestADoneMarkWaitsOnItsCheck(RouteHost):
    """M-632 — wish-intake Requirement 4 criteria 9, 10 and 13."""

    def test_a_done_mark_reads_reopened_until_the_check_passes_and_then_reads_done(self):
        # route-1's acceptance: the thing the work was for is actually on disk.
        self.set_checks(route_1="test -f board-opened-by-itself")
        self.set_plan(self.plan().replace("### 🔄 Open the board", "### ✅ Open the board"))

        red = self.probe()
        self.assertIn("route-1", red, "a done mark with a failing check dropped off the open list")
        self.assertIn("🔁", red)
        self.assertIn("marked done", red)
        self.assertIn("its acceptance command fails", red)

        # The DOD is met — and only that. Nobody touches the mark.
        plan_before = self.plan()
        write(os.path.join(self.host, "board-opened-by-itself"), "the page opened\n")
        green = self.probe()
        self.assertEqual(self.plan(), plan_before,
                         "the row was re-marked by hand, so the check is not what decided it")
        self.assertNotIn("route-1", green, "the passing check did not close the row")
        self.assertIn("route-2", green)

    def test_the_reopened_reading_comes_from_the_check_and_not_from_the_mark(self):
        """The same plan, read twice, with only the host's own command moved between the readings."""
        self.set_plan(self.plan().replace("### 🔄 Open the board", "### ✅ Open the board"))

        self.set_checks(route_1="true")
        self.assertNotIn("route-1", self.probe())

        self.set_checks(route_1="false")
        reopened = self.probe()
        self.assertIn("route-1", reopened)
        self.assertIn("🔁", reopened)


class TestTheRecordedStateNamesOneNextAction(RouteHost):
    """M-633 — Requirement 314 criteria 6 and 7."""

    def setUp(self):
        super().setUp()
        r = self.cp("new", os.path.join(self.checkpoints_dir, "route-1.md"),
                    "--title", "Open the board by itself after a push", "--owner", "director",
                    "--decision-sheet", SHEET)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = self.cp("update", os.path.join(self.checkpoints_dir, "route-1.md"),
                    "--next", "- Write the open step into the push script.")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_one_row_is_named_next_and_the_open_checkpoint_names_the_same_work(self):
        out = self.probe()
        self.assertEqual(out.count("<-- NEXT"), 1, "the state named more than one next action")
        line = next(l for l in out.splitlines() if "<-- NEXT" in l)
        self.assertIn("route-1", line)
        self.assertNotIn("route-2", line)

        # The one open checkpoint on the host is that same work's, and it says what to do next.
        opened = [f for f in self.checkpoint_files()
                  if "Status: open" in read(os.path.join(self.checkpoints_dir, f))]
        self.assertEqual(opened, ["route-1.md"])
        self.assertIn("Write the open step into the push script.",
                      read(os.path.join(self.checkpoints_dir, "route-1.md")))

    def test_a_second_reading_of_the_same_state_names_the_same_row(self):
        """A fresh session reads the same recorded state; nothing about it admits a second answer."""
        first = self.probe()
        second = self.probe()
        pick = lambda out: next(l for l in out.splitlines() if "<-- NEXT" in l)
        self.assertEqual(pick(first), pick(second))

    def test_the_next_answer_follows_the_recorded_state_rather_than_standing_still(self):
        """Red-then-green on the answer itself: close the row the state names, and the next
        answer moves to the row underneath it — which is what says the tag is read and not fixed."""
        self.assertIn("route-1", next(l for l in self.probe().splitlines() if "<-- NEXT" in l))

        self.set_checks(route_1="true")
        self.set_plan(self.plan().replace("### 🔄 Open the board", "### ✅ Open the board"))
        moved = self.probe()
        self.assertEqual(moved.count("<-- NEXT"), 1)
        self.assertIn("route-2", next(l for l in moved.splitlines() if "<-- NEXT" in l))


if __name__ == "__main__":
    unittest.main()
