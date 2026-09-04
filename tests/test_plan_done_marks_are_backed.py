"""Every ✅ mark on the board is backed by a command or a named reading, never a proxy.

plan-10's own text (`PLAN.md`, id: plan-10): measured 27.08, of the plan's steps three had a
check that ran their own acceptance, four had no check at all — so the probe and the board
showed whatever mark a hand typed and called it "declared" — and three ran a proxy, "the render
script exists and is executable", which stays green while the step is honestly open. Its own
acceptance: "A test reads PLAN.md and scripts/plan_checks.py together and fails when a task
marked done carries neither a command in the checks file nor a line in its own body saying who
read it and where. The same test fails a command that only asks whether a file exists."

`PLAN.md`'s own "How this file works" section (search "A task that closes writes its own check
in the same breath") already states the two legitimate outs for a closed task: a command in
`scripts/plan_checks.py`'s CHECKS, keyed by task id — or, where the result is prose, a
measurement or a decision no command can read, one body line saying who read it and where. The
file's own established phrasing for that second case, checked directly by scanning every
bold, date-stamped lead-in sentence in the file (2026-09-01), comes in exactly two recurring
shapes and no others: "**Checked by reading on DD.MM.**" (nine ✅ rows — q-568, q-570, plan-4,
plan-5, q-609, q-610, q-205, q-612, q-584) and "**Read DD.MM, and it holds.**" (two ✅ rows —
q-611, q-608). Every other bold date-stamped lead-in in the file ("Done DD.MM.", "Landed DD.MM.",
"Checked DD.MM, and it stays its own task.", and so on) reports a status or a re-check, not a
named reading standing in for a missing command, so this test matches only those two shapes
rather than inventing a broader rule of its own.

This is the instrument, not the fix: it is expected to fail today, and fixing every row it names
is plan-10's own larger job, not this file's.
"""
import pathlib
import re
import sys
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)

sys.path.insert(0, str(ROOT / "scripts"))
from plan_checks import CHECKS, parse_tasks  # noqa: E402

# The two established phrasings PLAN.md's own done rows already use to name who read them and
# when, in place of a command (see the module docstring's scan). A row that says either of these
# is read, not merely typed done.
_NAMED_READING_RE = re.compile(
    r"Checked by reading on \d{1,2}\.\d{1,2}|Read \d{1,2}\.\d{1,2}, and it holds"
)

# A clause that only asks whether something exists on disk — `test -f`, `test -d`, `test -x`,
# `test -e`, `test -s`, and so on, each against one static path, optionally negated with `!`.
# This is the exact shape plan-10's own text names as the defect it found: the render script's
# dropped check asked only "does this file exist and is it executable" while the step's own
# acceptance was about the render actually working. A command counts as a bare-existence proxy
# only when EVERY one of its top-level `&&` clauses has this shape — a command that adds even one
# real check (a grep, a diff, a content comparison, a script actually run) is doing more than
# asking whether a file exists, and is not a proxy.
_BARE_EXISTENCE_CLAUSE_RE = re.compile(r"^!?\s*test\s+-[a-zA-Z]\s+\S+$")


def is_bare_existence_proxy(command):
    """True when `command`'s every top-level `&&` clause is a bare presence test.

    Splitting on the literal `&&` is safe here: none of `CHECKS`' own values carry a stray `&&`
    outside that separator (checked directly against the live dict before this test was written —
    the embedded `python3 -c "..."` bodies use Python's `and`/`if`, never the shell operator).
    """
    clauses = [c.strip() for c in command.split("&&")]
    return bool(clauses) and all(_BARE_EXISTENCE_CLAUSE_RE.match(c) for c in clauses)


# A closed row's own record moved off the plan page on 2026-09-04 so the board reads as one
# screen; the plan keeps the heading and points at the archive. Both files are read here, so a
# done row is still backed by the same evidence it always was, wherever that evidence now sits.
_CLOSED_ARCHIVE = ROOT / "docs/queue-archive/2026-09-04-closed-rows.md"


def _done_tasks():
    """Every done row, with its body, whichever of the two files now carries it.

    The parser reads one "## Tasks" section per document, so the two are parsed separately and
    merged by id: the plan holds the heading, the archive holds the record.
    """
    rows = {}
    for path in (ROOT / "PLAN.md", _CLOSED_ARCHIVE):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if path is _CLOSED_ARCHIVE:
            text = "## Tasks\n" + text
        for t in parse_tasks(text):
            if t["mark"] != "✅":
                continue
            # A row already seen from the plan is the stub; the archive's copy carries the body.
            if t["id"] not in rows or len(t["body"]) > len(rows[t["id"]]["body"]):
                rows[t["id"]] = t
    return list(rows.values())


class TestEveryDoneMarkIsBackedByACommandOrANamedReading(unittest.TestCase):
    """A ✅ task needs either (a) a command in `plan_checks.CHECKS` that is not a bare-existence
    proxy, or (b) a body line in the project's own established phrasing naming who read it and
    when. A task with neither is done on nothing but a hand-typed mark; a task with only a
    bare-existence command is done on nothing but a file's mere presence — both are the drift
    plan-10's own acceptance names, reported here as two separate findings, not fixed here."""

    def test_no_done_task_is_unverified_and_unread(self):
        unverified_and_unread = []
        for t in _done_tasks():
            body = "\n".join(t["body"])
            has_named_reading = bool(_NAMED_READING_RE.search(body))
            if t["check"] is None and not has_named_reading:
                unverified_and_unread.append(t["id"])
        self.assertFalse(
            unverified_and_unread,
            "these tasks are marked done with neither a command in scripts/plan_checks.py's "
            "CHECKS nor a body line saying who read them and where (this project's own "
            "convention: '**Checked by reading on DD.MM.**'): %s" % unverified_and_unread,
        )

    def test_no_done_task_is_verified_only_by_a_files_bare_existence(self):
        proxy_only = []
        for t in _done_tasks():
            if t["check"] and is_bare_existence_proxy(t["check"]):
                proxy_only.append(t["id"])
        self.assertFalse(
            proxy_only,
            "these tasks are marked done and carry a command in scripts/plan_checks.py's "
            "CHECKS, but the command only asks whether a file exists — the exact proxy "
            "plan-10's own text names as a defect (step 1's dropped 'the render script exists "
            "and is executable' check): %s" % proxy_only,
        )


class TestTheClassifiersThemselvesAreCorrect(unittest.TestCase):
    """A narrow self-check on the two functions above, independent of PLAN.md's own content
    today — so a future edit to PLAN.md changing which ids fail cannot also hide a broken
    classifier."""

    def test_a_pure_existence_command_is_a_proxy(self):
        self.assertTrue(is_bare_existence_proxy("test -f PLAN.md"))
        self.assertTrue(is_bare_existence_proxy(
            'test -f a && test -d b && ! test -d c && test -x d/e-f.sh'
        ))

    def test_a_command_that_greps_or_compares_content_is_not_a_proxy(self):
        self.assertFalse(is_bare_existence_proxy("grep -q foo bar.md"))
        self.assertFalse(is_bare_existence_proxy('test -f a && grep -q foo a'))
        self.assertFalse(is_bare_existence_proxy('test -f a && cmp -s a b'))
        self.assertFalse(is_bare_existence_proxy('test "$(cat VERSION)" != 5.0.0'))

    def test_the_named_reading_pattern_matches_the_established_phrasing(self):
        self.assertTrue(_NAMED_READING_RE.search(
            "**Checked by reading on 28.08.** The answer stands in the review record."
        ))
        self.assertTrue(_NAMED_READING_RE.search(
            "**Read 28.08, and it holds.** The row asked that a review say so in its own record."
        ))
        self.assertFalse(_NAMED_READING_RE.search(
            "**Checked 28.08, and it stays its own task.** No reading is named here."
        ))


if __name__ == "__main__":
    unittest.main()
