"""What a priority means is written in the plan, and the next move is derived from it.

PLAN.md row q-819: the field existed on every task and only the word "critical" changed
anything, hardcoded in the renderer. A project now states its own priority words and their
order in one place — the "Words used here" bullet that begins "- **Priority**" — and
scripts/plan_checks_core.py's reader is that statement's one machine reading.

The load-bearing case is the last one: a plan that names no order gets none invented for it.
"""
import os
import sys

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
