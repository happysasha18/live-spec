"""THIS PROJECT'S OWN commands that verify each plan row, in one home.

`adopt/install-status-view.sh` puts this file in a project's `scripts/` the first time the status
view is installed, and never overwrites it afterwards: everything below is yours.

A plan a person edits by hand must not also be an execution surface, so `PLAN.md` holds only prose
and the commands that decide whether a row is really done live here, keyed by the row's own id —
stable across title edits, unlike the title text.

A row with no command here is reported DECLARED: the mark somebody typed is the only claim, and
the probe and the board both say so plainly rather than pretending it was measured. That is the
right state for a row whose result is prose, a measurement, or a decision. Write a command for a
row whose subject is an artifact that can drift back — a file, a script, a setting.

Two rules the commands live under:

- **Cheap.** `scripts/state-probe.sh` runs every command below at the start of every session. A
  command that runs a whole test suite makes the first command of the morning hang. Reach for a
  `grep`, a `test`, or one already-fast script; run a single test module directly rather than
  through the test runner.
- **Read the row's own acceptance, not a path.** `test -f <the file the row made>` passes on an
  empty file, so it proves the row was done only in the sense that somebody typed the name. Read
  the substance the row promised.

The parsing, the marks and the state computation are the same for every project and live in
`scripts/plan_checks_core.py`, imported below. Nothing in this file is shared with anyone.
"""

from plan_checks_core import (  # noqa: F401  (re-exported for this module's own callers)
    evaluate,
    key_failure_note,
    normalize_mark,
    reads_outside_the_tree,
)
from plan_checks_core import parse_tasks as _parse_tasks

#: row id -> the shell command that proves that row done, run from the project root.
#: Example, once a row has earned one:
#:     "q-1": "grep -q 'the sentence the row promised' docs/the-page-it-wrote.md",
CHECKS = {}


def parse_tasks(text):
    """The plan's rows, with this project's own acceptance command attached to each.

    `CHECKS` is read at call time rather than bound here, so a caller that edits the map is
    honoured.
    """
    return _parse_tasks(text, CHECKS)
