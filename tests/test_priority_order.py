"""What a priority means is written in the plan, and the next move is derived from it.

PLAN.md row q-819: the field existed on every task and only the word "critical" changed
anything, hardcoded in the renderer. A project now states its own priority words and their
order in one place — the "Words used here" bullet that begins "- **Priority**" — and
scripts/plan_checks_core.py's reader is that statement's one machine reading.

The load-bearing case is the last one: a plan that names no order gets none invented for it.
"""
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import plan_checks_core as core  # noqa: E402


BULLET = """## Words used here

- **Priority** — the one word on a task's own line.
  1. `critical` — the pack is wrong about something today.
  2. `normal` — real work the goal needs.

  Prose that belongs to the bullet and names no word sits here.

- **Gates** — something else entirely.
  1. `nope` — this sub-item belongs to another bullet and must not be read.
"""


def test_the_order_is_read_in_the_order_it_is_written():
    assert core.read_priority_order(BULLET) == ["critical", "normal"]


def test_a_later_bullet_does_not_leak_its_own_numbered_items():
    assert "nope" not in core.read_priority_order(BULLET)


def test_a_plan_that_names_no_order_gets_none_invented():
    assert core.read_priority_order("# a plan with no such bullet\n\n- **Gates** — no words.\n") == []


def test_an_unnamed_priority_word_ranks_last():
    order = ["critical", "normal"]
    assert core.priority_rank("critical", order) == 0
    assert core.priority_rank("normal", order) == 1
    assert core.priority_rank("someone's own word", order) == len(order)
    assert core.priority_rank(None, order) == len(order)


def test_the_rank_reads_the_word_however_it_is_spelled_on_the_line():
    order = ["critical", "normal"]
    assert core.priority_rank("  CRITICAL ", order) == 0


def test_this_project_states_its_own_order():
    with open(os.path.join(REPO, "PLAN.md"), encoding="utf-8") as fh:
        plan = fh.read()
    order = core.read_priority_order(plan)
    assert order, "PLAN.md no longer says what a priority means here (q-819)"
    assert order[0] == "critical", "the plan's highest-ranking priority word moved"


def test_the_templates_seeded_statement_parses_and_names_every_word_its_own_examples_use():
    """R5: the template's intake-notes prose names `critical` and `quick win`; its seeded
    "Words used here" list must name the same words its own worked wish row and prose use, or a
    host that follows the template's own instruction gets the word it used ranked last."""
    with open(os.path.join(REPO, "templates", "PLAN.template.md"), encoding="utf-8") as fh:
        tmpl = fh.read()
    order = core.read_priority_order(tmpl)
    assert order, "templates/PLAN.template.md's seeded priority statement failed to parse"
    used_by_the_templates_own_examples = {"critical", "quick win", "normal"}
    missing = used_by_the_templates_own_examples - set(order)
    assert not missing, (
        "the template's own prose and worked wish row use these priority words, and its seeded "
        f"list never names them, so priority_rank ranks them last: {missing}"
    )


def test_every_task_carries_a_word_the_plan_names():
    """A word the list does not name still ranks and still prints, so this is a readability
    check on the plan rather than a gate on the reader. It reds when an open task starts using
    a word the plan never explained.

    Only open tasks are read. A closed row carries no priority line at all — the finished rows
    live in a table that never had the field — and reading them would make this assert on the
    shape of the archive rather than on the work in hand.
    """
    with open(os.path.join(REPO, "PLAN.md"), encoding="utf-8") as fh:
        plan = fh.read()
    order = core.read_priority_order(plan)
    unnamed = sorted({
        (t["priority"] or "").strip().lower() or "(no priority line)"
        for t in core.parse_tasks(plan)
        if t["mark"] != "✅" and (t["priority"] or "").strip().lower() not in order
    })
    assert not unnamed, (
        "these open tasks carry a priority the plan's own list explains nowhere: "
        f"{unnamed}"
    )


class TheRendererFollowsThePlansOwnStatement(unittest.TestCase):
    """The printed order and the next-move line read the statement, rather than a hardcoded word.

    Before q-819 the renderer sorted on the literal word "critical" and nothing else, so a project
    using any other vocabulary got no ranking at all and the next move was whatever sat topmost on
    the page. These cases run the real renderer against a plan whose page order and whose priority
    order disagree, so a renderer that had gone back to reading position would fail them.
    """

    PLAN_WITH_A_STATEMENT = """# demo — Plan

## Words used here

- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `later` — real work, nothing wrong today.

## Tasks

### ⬜ Sits first on the page and ranks second — id: demo-1
**Group:** One · **Priority:** later
**Source:** the fixture.

### ⬜ Sits second on the page and ranks first — id: demo-2
**Group:** Two · **Priority:** urgent
**Source:** the fixture.

### ⬜ Carries a word the statement never names — id: demo-3
**Group:** Three · **Priority:** whenever
**Source:** the fixture.
"""

    PLAN_WITHOUT_A_STATEMENT = PLAN_WITH_A_STATEMENT.replace(
        """- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `later` — real work, nothing wrong today.
""", "- **Gates** — the checks that run before a push.\n")

    #: A row already in hand outranks nothing: SPEC Requirement 320 criterion 6 says the next move
    #: is the highest-ranking row nobody is working yet — the shipped renderer used to prefer
    #: whatever sat in the 🔄 bucket over a higher-ranking free row (F3).
    PLAN_INHAND_OUTRANKED_BY_FREE = """# demo — Plan

## Words used here

- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `later` — real work, nothing wrong today.

## Tasks

### 🔄 Already in hand, and ranks highest — id: demo-1
**Group:** One · **Priority:** urgent
**Source:** the fixture.

### ⬜ Free, and ranks lower — id: demo-2
**Group:** Two · **Priority:** later
**Source:** the fixture.
"""

    #: A blocked row never wins the next move: clearing its outside cause comes first, whatever its
    #: priority word (F3).
    PLAN_BLOCKED_OUTRANKED_BY_FREE = """# demo — Plan

## Words used here

- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `later` — real work, nothing wrong today.

## Tasks

### ⛔ Blocked, and ranks highest — id: demo-1
**Group:** One · **Priority:** urgent
**Source:** the fixture.
**Blocked by:** a dead credential.

### ⬜ Free, and ranks lower — id: demo-2
**Group:** Two · **Priority:** later
**Source:** the fixture.
"""

    #: A reopened row (🔁) is nobody's work in progress, so it is a candidate for the next move
    #: ahead of the queue — rule 38's own group order and criterion 6's words both say so (R2).
    #: demo-1 is marked done; its own acceptance command is wired (below) to keep failing, which
    #: is the only way evaluate() ever draws a row 🔁.
    PLAN_REOPENED_OUTRANKS_QUEUED = """# demo — Plan

## Words used here

- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `later` — real work, nothing wrong today.

## Tasks

### ✅ Reopened, and ranks highest — id: demo-1
**Group:** One · **Priority:** urgent
**Source:** the fixture.

### ⬜ Queued, and ranks lower — id: demo-2
**Group:** Two · **Priority:** later
**Source:** the fixture.
"""

    #: A backticked priority name can be more than one word (R5): the statement's own list names
    #: `quick win` and a row carrying that word must rank by it rather than falling to the bottom,
    #: the way an unparsed word does.
    PLAN_WITH_A_TWO_WORD_WORD = """# demo — Plan

## Words used here

- **Priority** — the one word on a task's own line.
  1. `urgent` — the thing is wrong today.
  2. `quick win` — low effort, free to bubble up.
  3. `later` — real work, nothing wrong today.

## Tasks

### ⬜ Carries the two-word priority word — id: demo-1
**Group:** One · **Priority:** quick win
**Source:** the fixture.

### ⬜ Carries the lowest-ranking word — id: demo-2
**Group:** Two · **Priority:** later
**Source:** the fixture.
"""

    #: With no candidate row at all, the block must still print one line saying why, rather than
    #: vanish (R3). Its only open row is in hand; nothing free, nothing reopened, nothing blocked.
    PLAN_NOTHING_QUALIFIES_ONLY_IN_HAND = """# demo — Plan

## Tasks

### 🔄 In hand, the only open row — id: demo-1
**Group:** One · **Priority:** urgent
**Source:** the fixture.
"""

    #: Nothing open at all — every row is finished (R3's other named state).
    PLAN_NOTHING_QUALIFIES_ALL_FINISHED = """# demo — Plan

## Tasks

### ✅ Finished, the only row — id: demo-1
**Group:** One · **Priority:** urgent
**Source:** the fixture.
"""

    def _run(self, plan_text, checks=None):
        host = tempfile.mkdtemp(prefix="livespec-priority-")
        subprocess.run(["git", "init", "-q"], cwd=host, check=True)
        os.makedirs(os.path.join(host, "scripts"), exist_ok=True)
        for name in ("state-probe.sh", "plan_checks_core.py"):
            src = os.path.join(REPO, "scaffold", "status-view", "state-probe.sh") \
                if name == "state-probe.sh" else os.path.join(REPO, "scripts", name)
            with open(src, encoding="utf-8") as fh:
                body = fh.read()
            with open(os.path.join(host, "scripts", name), "w", encoding="utf-8") as fh:
                fh.write(body)
        if checks:
            # A row's mark reopens (🔁) only through evaluate() finding its own acceptance
            # command failing (plan_checks_core.py never lets 🔁 be typed) — so a reopened-row
            # fixture needs a command wired for its id, not the seed's empty CHECKS.
            seed = (
                "from plan_checks_core import evaluate, key_failure_note, normalize_mark, "
                "reads_outside_the_tree\n"
                "from plan_checks_core import parse_tasks as _parse_tasks\n"
                "CHECKS = %r\n\n"
                "def parse_tasks(text):\n"
                "    return _parse_tasks(text, CHECKS)\n" % checks
            )
        else:
            with open(os.path.join(REPO, "scaffold", "status-view", "plan_checks.py"),
                      encoding="utf-8") as fh:
                seed = fh.read()
        with open(os.path.join(host, "scripts", "plan_checks.py"), "w", encoding="utf-8") as fh:
            fh.write(seed)
        with open(os.path.join(host, "PLAN.md"), "w", encoding="utf-8") as fh:
            fh.write(plan_text)
        r = subprocess.run(["bash", os.path.join(host, "scripts", "state-probe.sh")],
                           cwd=host, capture_output=True, text=True)
        return r.stdout + r.stderr

    def test_the_highest_ranking_free_row_is_next_however_the_page_is_ordered(self):
        out = self._run(self.PLAN_WITH_A_STATEMENT)
        self.assertIn("Sits second on the page and ranks first", out)
        # The word NEXT appears twice: as the tag beside the winning row in the list, and as the
        # closing block's own heading. The closing block is the last one.
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Sits second on the page and ranks first", next_block)
        self.assertNotIn("Sits first on the page and ranks second", next_block)

    def test_the_next_move_prints_the_word_it_won_on(self):
        out = self._run(self.PLAN_WITH_A_STATEMENT)
        self.assertIn("urgent — the highest the plan names", out)

    def test_a_plan_with_no_statement_keeps_its_own_order_and_says_so(self):
        out = self._run(self.PLAN_WITHOUT_A_STATEMENT)
        self.assertIn("the plan does not say what a priority means here", out)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Sits first on the page and ranks second", next_block)

    def test_a_row_in_hand_never_wins_next_over_a_higher_ranking_free_row(self):
        out = self._run(self.PLAN_INHAND_OUTRANKED_BY_FREE)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Free, and ranks lower", next_block)
        self.assertNotIn("Already in hand, and ranks highest", next_block)

    def test_a_blocked_row_never_wins_next(self):
        out = self._run(self.PLAN_BLOCKED_OUTRANKED_BY_FREE)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Free, and ranks lower", next_block)
        self.assertNotIn("Blocked, and ranks highest", next_block)

    def test_a_reopened_row_wins_next_over_a_queued_row_and_the_reason_names_it(self):
        out = self._run(self.PLAN_REOPENED_OUTRANKS_QUEUED, checks={"demo-1": "false"})
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Reopened, and ranks highest", next_block)
        self.assertNotIn("Queued, and ranks lower", next_block)
        self.assertNotIn("nothing of higher priority is free", out)

    def test_a_two_word_priority_name_ranks_by_its_own_word_rather_than_last(self):
        out = self._run(self.PLAN_WITH_A_TWO_WORD_WORD)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("Carries the two-word priority word", next_block)
        self.assertNotIn("Carries the lowest-ranking word", next_block)

    def test_no_candidate_row_prints_one_line_naming_in_hand_rather_than_vanishing(self):
        out = self._run(self.PLAN_NOTHING_QUALIFIES_ONLY_IN_HAND)
        self.assertIn("NEXT", out)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("in hand", next_block)

    def test_no_candidate_row_and_no_open_row_prints_finished(self):
        out = self._run(self.PLAN_NOTHING_QUALIFIES_ALL_FINISHED)
        self.assertIn("NEXT", out)
        next_block = out.rsplit("NEXT", 1)[-1]
        self.assertIn("finished", next_block)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
