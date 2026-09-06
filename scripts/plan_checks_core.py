"""The host-portable half of the plan readers: how a plan's rows are parsed, how a mark is
spelled, and how a row's real state is computed from the command that verifies it.

Nothing in this file knows anything about any one project. The commands that verify a project's
own tasks are that project's own property and live in its own `scripts/plan_checks.py`, keyed by
task id; this module never carries a command of its own and never reaches for one. A caller hands
its check map to `parse_tasks` and gets tasks back with each row's command attached; a caller with
no map (a project that has not written one yet) gets tasks whose every row reports DECLARED, which
is correct behaviour rather than a gap.

That split is what makes the status view installable. Before it, `parse_tasks` looked this
project's own `CHECKS` up inside itself, so a host adopting the probe and the board inherited this
project's literal shell commands along with the parser — commands naming files no host has.

The three readers built on this module — `scripts/state-probe.sh` (the report a session prints at
its start), `scripts/render-board.sh` (the same state as a page) and `scripts/plan-step.sh` (one
row on its own) — travel to a host through `adopt/install-status-view.sh`.

## The two plan shapes

A plan reaches this parser in one of two shapes, and both are read here so the readers cannot
disagree about which one they are looking at:

- **headings** — a `## Tasks` section of `### <mark> <title> — id: <id>` rows, each followed by
  its `**Group:**`/`**Source:**` lines and its prose. This project's own `PLAN.md`.
- **table** — a `## The body` section holding one markdown table row per wish, the shape
  `templates/PLAN.template.md` lands on a project at its founding: id, wish, class, status,
  acceptance. Its status cell carries a word (*queued*, *in-work*, *deferred*, *far*) rather than
  a mark, and the word is translated to the mark the readers draw.

The shape is decided by which section heading the document actually carries, never by a setting:
a plan that has been rewritten from one shape into the other reads correctly the moment it is
saved.
"""

import re
import subprocess

# The variation selectors an emoji may carry. `✅` and `✅️` are one mark on the screen and two
# different strings to a comparison, and a plan may write one mark with the selector and another
# without it. Every reader of a mark compares it literally, so a done mark typed with a selector
# read as done to the eye while no reader agreed — the board would show it done and the landing
# gate would ask no resume refresh of the commit that set it (the adversarial read of 2026-08-31).
# Stripping the selector where the mark is PARSED is what keeps the one home one home; every
# comparison downstream then goes on working as written.
_VARIATION_SELECTORS = "︎️"

# The marks a plan types, each in the ONE spelling every reader and every renderer uses. A mark
# typed the other way comes back to its canonical spelling here, and nowhere else has to know that
# two spellings exist. 🔁 (reopened) is never typed — evaluate() below is its only source — so it
# carries no entry here.
_CANONICAL_MARKS = {m.strip(_VARIATION_SELECTORS): m for m in ("✅", "🔄", "⬜", "⛔")}

# 👁️ ("needs his eyes") retired 2026-09-04, his standing word: needing to consult a person is not
# a task state — it is a question asked in the reply. A row still wearing 👁️ is a defect, not a
# fourth state; it reads as ⬜ queued rather than falling through every mark comparison downstream
# and disappearing from the board unexplained. ⛔ ("blocked") stays, narrowed the same day: it
# names only a real outside thing stopping the work — an expired key, a dead credential, a
# service that is down — never waiting on someone or on a decision.
_RETIRED_MARKS = {m.strip(_VARIATION_SELECTORS) for m in ("👁️",)}


def normalize_mark(mark):
    """The canonical spelling of a mark a keyboard can type two ways, or ⬜ for a retired one."""
    if not mark:
        return mark
    stripped = mark.strip(_VARIATION_SELECTORS)
    if stripped in _RETIRED_MARKS:
        return "⬜"
    return _CANONICAL_MARKS.get(stripped, mark)


def run_key(command):
    """Run one acceptance key and hand back the completed process.

    Under `set -o pipefail`, so a command that fails inside a pipe cannot be hidden by a trailing
    stage that succeeds anyway. Without it, `<a grader that prints its line and then exits 1> |
    grep -q '<that line>'` reads green while the thing the key exists to test is red — which is
    how q-823 closed once on its Director arm (2026-09-06). One home, because both the plan
    readers and the acceptance receipt run their commands through it.
    """
    return subprocess.run("set -o pipefail; " + command, shell=True,
                          executable="/bin/bash", capture_output=True)


def reads_outside_the_tree(command):
    """True when a key reaches for state git does not carry — a path under the person's home.

    Such a key goes red on a fresh clone for a reason about the machine rather than about the
    project, and a reader who is not told that reads an alarm where there is none. Derived from
    the command's own text rather than kept as a list of ids, so a key written tomorrow is
    covered the day it is written.
    """
    return "$HOME" in command or "~/" in command


def key_failure_note(command, result):
    """One short line saying why a done task's acceptance command failed.

    Every reader of the plan prints this, so they give one account. It carries the command's own
    first printed line where the command printed one — those messages already name the missing
    thing and the way to put it back — and it says when the key reached outside the tracked tree.
    """
    first = ""
    for stream in (result.stdout, result.stderr):
        if not stream:
            continue
        text = stream.decode("utf-8", "replace") if isinstance(stream, bytes) else stream
        for line in text.splitlines():
            if line.strip():
                first = line.strip()
                break
        if first:
            break
    note = "its acceptance command fails"
    if reads_outside_the_tree(command):
        note += ", and that command reads this machine rather than the tree"
    if first:
        note += " — " + (first[:80].rstrip() + "…" if len(first) > 80 else first)
    return note


# ---------------------------------------------------------------- the headings shape
# A task header looks like "### <mark emoji> <Task Name> — id: <plan-N|q-N>" — no brackets
# around the mark, an em dash before "id:". The title is matched non-greedy so a title that
# itself contains an em dash still stops at the literal " — id: " that ends the heading.
_HEADER_RE = re.compile(r"^### (\S+) (.+?) — id: (\S+)$")
_GROUP_RE = re.compile(r"^\*\*Group:\*\*\s*(.+?)\s*·\s*\*\*Priority:\*\*\s*(.+)$")
_SOURCE_RE = re.compile(r"^\*\*Source:\*\*\s*(.+)$")
_COVERED_BY_RE = re.compile(r"^\*\*Covered by:\*\*\s*(.+)$")
_DEFERRED_RE = re.compile(r"^\*\*Deferred:\*\*\s*(.+)$")
_BLOCKED_BY_RE = re.compile(r"^\*\*Blocked by:\*\*\s*(.+)$")

# ---------------------------------------------------------------- what a priority means here
# A project says in its own plan what its priority words mean and how they rank, under the
# "Words used here" bullet that begins "- **Priority**". The words are the backticked names of
# that bullet's own numbered sub-items, read in the order they are written. This is the one home
# for that order (PLAN q-819): the reader below is its one machine reading, and nothing else may
# hardcode a priority word.
#
# A plan that has not written the bullet gets no invented order. read_priority_order returns an
# empty list, and a caller that ranks by it says the list is missing and falls back to the plan's
# own order rather than deciding for the project.
_PRIORITY_BULLET_RE = re.compile(r"^- \*\*Priority\*\*")
# Requirement 320 criterion 1a puts no single-token limit on a priority word, so a backticked
# name of several words (`quick win`) must parse the same as a one-word name (R5).
_PRIORITY_WORD_RE = re.compile(r"^\s+\d+\.\s+`([a-z][a-z0-9-]*(?: [a-z][a-z0-9-]*)*)`")


def read_priority_order(plan_text):
    """Return the plan's own priority words, highest-ranking first; [] when it names none."""
    words, inside = [], False
    for line in plan_text.splitlines():
        if _PRIORITY_BULLET_RE.match(line):
            inside = True
            continue
        if inside:
            m = _PRIORITY_WORD_RE.match(line)
            if m:
                words.append(m.group(1))
                continue
            # The bullet ends at the next top-level bullet or heading; a blank line and the
            # bullet's own continuation prose sit inside it and are skipped.
            if line.startswith("- ") or line.startswith("#"):
                break
    return words


def priority_rank(priority, order):
    """Where one task's priority word sits in the plan's own order. An unnamed word ranks last,
    so it stays visible rather than reading as the middle of the list."""
    word = (priority or "").strip().lower()
    try:
        return order.index(word)
    except ValueError:
        return len(order)


# ---------------------------------------------------------------- the table shape
# The status vocabulary templates/PLAN.template.md defines for a row, and the mark each word
# draws as. The four terminal words are read too: the live-body law moves a row out of the body
# when it reaches one, but a plan mid-edit can hold one for a moment, and a reader that dropped
# such a row would show the work as gone rather than as done.
_TABLE_STATUS_MARKS = {
    "queued": "⬜",
    "in-work": "🔄",
    "deferred": "⬜",
    "far": "⬜",
    "landed": "✅",
    "declined": "✅",
    "superseded": "✅",
    "decided": "✅",
}
_TABLE_PARKED = ("deferred", "far")
_STATUS_WORD_RE = re.compile(r"\*([a-z-]+)\*")
_ASKED_BY_RE = re.compile(r"(Asked by [^.]+\.)")
_PRIORITY_RE = re.compile(r"priority:\s*([a-z ]+?)\s*(?:·|$)")
_SEPARATOR_ROW_RE = re.compile(r"^[\s|:-]+$")


def _first_sentence(text, limit=90):
    """The row's own handle: a table's wish cell opens with the ask and then carries its
    provenance and its intake notes, and only the ask belongs in a one-line report."""
    text = text.strip()
    m = re.search(r"[.!?](?=\s|$)", text)
    if m and m.end() <= limit:
        return text[: m.end() - 1].strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")


def _new_task(mark, title, task_id):
    return {
        "mark": normalize_mark(mark),
        "title": title,
        "id": task_id,
        "group": None,
        "priority": None,
        "source": None,
        "covered_by": None,
        "deferred": None,
        "blocked_by": None,
        "check": None,
        "body": [],
    }


def _section(text, heading):
    """The lines of one `## <heading>` section, or None when the document has no such heading."""
    found = False
    lines = []
    for line in text.splitlines():
        if line.strip() == heading:
            found = True
            continue
        if found and line.startswith("## "):
            break
        if found:
            lines.append(line)
    return lines if found else None


def _parse_headings(lines):
    tasks = []
    cur = None
    for line in lines:
        m = _HEADER_RE.match(line.rstrip())
        if m:
            cur = _new_task(m.group(1), m.group(2), m.group(3))
            tasks.append(cur)
            continue
        if cur is None:
            continue
        stripped = line.strip()
        gm = _GROUP_RE.match(stripped)
        if gm and cur["group"] is None:
            cur["group"], cur["priority"] = gm.group(1), gm.group(2)
            continue
        sm = _SOURCE_RE.match(stripped)
        if sm and cur["source"] is None:
            cur["source"] = sm.group(1)
            continue
        cbm = _COVERED_BY_RE.match(stripped)
        if cbm and cur["covered_by"] is None:
            cur["covered_by"] = cbm.group(1)
            continue
        dm = _DEFERRED_RE.match(stripped)
        if dm and cur["deferred"] is None:
            cur["deferred"] = dm.group(1)
            continue
        bbm = _BLOCKED_BY_RE.match(stripped)
        if bbm and cur["blocked_by"] is None:
            cur["blocked_by"] = bbm.group(1)
            continue
        cur["body"].append(line)
    return tasks


def _parse_table(lines):
    tasks = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if _SEPARATOR_ROW_RE.match(stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        task_id, wish, klass, status = cells[0], cells[1], cells[2], cells[3]
        if not task_id or task_id == "#":
            continue  # the table's own header row
        sm = _STATUS_WORD_RE.search(status)
        word = sm.group(1) if sm else ""
        task = _new_task(_TABLE_STATUS_MARKS.get(word, "⬜"), _first_sentence(wish), task_id)
        task["group"] = klass or None
        pm = _PRIORITY_RE.search(wish)
        task["priority"] = pm.group(1).strip() if pm else "normal"
        am = _ASKED_BY_RE.search(wish)
        task["source"] = am.group(1) if am else None
        if word in _TABLE_PARKED:
            # The template's own reading of these two words: the row is parked on a decision or on
            # a named revisit trigger, which is not an obstacle. Recorded so a reader ranking rows
            # can drop it from the live set rather than show it as work waiting to start.
            task["deferred"] = status
        if len(cells) > 4 and cells[4]:
            task["body"] = ["**Acceptance:** " + cells[4]]
        tasks.append(task)
    return tasks


def parse_tasks(text, checks=None):
    """Parse a plan's rows into a list of task dicts, in file order.

    Each dict carries: mark (canonically spelled), title, id, group, priority, source, covered_by,
    deferred, blocked_by (each None if that line was missing), check (`checks[id]`, or None when
    the caller passed no map or the map has no entry for this row), and body — the remaining lines
    of the row's block, for a caller that wants more than the summary fields.

    `checks` is the CALLER's own map of task id to the shell command that verifies that task. It
    is a parameter and not a thing this module owns: the commands belong to one project, and this
    parser is read by every project that installs the status view.

    covered_by/deferred/blocked_by are what a reader uses to tell a row that only LOOKS idle apart:
    covered_by names the row that actually carries this work (a fold pointer); deferred names a
    decision to postpone it, not an obstacle; blocked_by names a real, understood cause a ⛔ row
    cannot move past on its own — narrowed 2026-09-04, his standing word: ⛔ names only an outside
    thing stopped the work (an expired key, a dead credential, a service that is down), never
    waiting on someone or on a decision, which is a question asked in the reply, not a task state.
    A ⛔ row with none of the three is a mislabel, not a fourth state.
    """
    lines = _section(text, "## Tasks")
    if lines is not None:
        tasks = _parse_headings(lines)
    else:
        lines = _section(text, "## The body")
        tasks = _parse_table(lines) if lines is not None else []
    if checks:
        for t in tasks:
            t["check"] = checks.get(t["id"])
    return tasks


def evaluate(tasks):
    """Run each row's acceptance command and record what it says, in place.

    Every reader of a plan needs this and none of them may decide it differently, which is why it
    is here and not in any one of them. Sets, per row: `ok` (the command passed, or — with no
    command — the mark says done), `verified` (a command decided it), `failing_key` (the mark says
    done and the command disagrees), `icon` (the mark to draw), and `note` (why a failing key
    failed).

    A row's real state can outrun or lag the mark a person typed — the command is the fact. On a
    failure the row falls back to its own mark rather than a flat "not done", which keeps a real
    distinction: a row with no command at all is DECLARED, while a row marked in hand whose command
    fails is genuinely in hand and genuinely unfinished.

    A done mark is the one exception, and it is why the commands were written at all: a ✅ whose
    command fails printed itself back as ✅ and was counted among the done, so the command could
    never contradict the mark it was there to test. Such a row is REOPENED (🔁) — it was done and
    is done no longer, which is neither blocked (a real outside cause) nor queued (never started).
    A row shaped like both — done-marked, command failing, and carrying a real `Blocked by:` cause
    — draws as blocked, because the row names an obstacle outside the work and reopened names none.
    """
    for t in tasks:
        if t["check"]:
            r = run_key(t["check"])
            ok = r.returncode == 0
            t["failing_key"] = t["mark"] == "✅" and not ok
            if t["failing_key"] and t["blocked_by"]:
                t["icon"] = "⛔"
            elif t["failing_key"]:
                t["icon"] = "🔁"
            else:
                t["icon"] = "✅" if ok else t["mark"]
            t["note"] = key_failure_note(t["check"], r) if t["failing_key"] else ""
            t["verified"] = True
        else:
            ok = t["mark"] == "✅"
            t["icon"] = t["mark"]
            t["failing_key"] = False
            t["note"] = ""
            t["verified"] = False
        t["ok"] = ok
    return tasks
