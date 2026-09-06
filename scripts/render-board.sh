#!/bin/bash
# render-board.sh — the work board (SPEC spec/work-board.md Requirement 309, matrix/work-board.md).
#
# One rendered surface under one name: the status page this project already drew from PLAN.md's
# Canon, grown up into the board Requirement 309 describes — the whole queue in columns, the
# in-work column split into lanes, a card per task with the worker on it, the time it was given
# against the time it took, and every closed row kept rather than cleared.
#
# It invents no second source of state. Every field comes from something already on disk:
#   PLAN.md                       the rows, their marks, their groups, sources, deferrals
#   scripts/plan_checks.py        the acceptance command that decides a row's real state
#   .live-spec/checkpoints/*.md   the holder, the work in flight, the plan's next step, the stamps
#   git branch lane/* + worktrees the build lanes and each lane's branch and worktree
#   WAITING.md                    the waiting region — the board keeps no waiting list of its own
#   docs/queue-archive/*.md       the closed rows that have left the plan page
#   SURFACES.md                   the registry row the board must hold before it renders
#
# The periodic auto-refresh heartbeat Requirement 309 once carried (former criteria 88, 90, 96 and
# the matching halves of M-540/M-542) is retired on the owner's 2026-09-02 12:46 word
# (`.live-spec/turnkey-contract-composed.md:304`). This page does not reload itself, polls nothing,
# and runs no timer. It is static HTML, drawn again when something changes.
#
# Usage: bash scripts/render-board.sh [output-file]   (default: board.html at repo root)
#        bash scripts/render-board.sh --json          (the model the page is drawn from, no write)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

python3 - "$@" <<'PYEOF'
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime

args = sys.argv[1:]
json_mode = "--json" in args
positional = [a for a in args if not a.startswith("--")]
out_path = positional[0] if positional else "board.html"

# The parser and the commands that verify each plan row live in one home, scripts/plan_checks.py:
# a status board a person edits by hand must not also be an execution surface, and two copies of
# either would let this reader and scripts/state-probe.sh disagree about what a row is or what
# "done" means for it. Both readers cd to the repository root before this block runs.
sys.path.insert(0, "scripts")
from plan_checks import evaluate, parse_tasks
from plan_checks_core import _parse_headings  # the same row parser, over an archive file's rows

try:
    import checkpoint
except ImportError:  # a host that has not installed the checkpoint format yet
    checkpoint = None

CHECKPOINTS = os.path.join(".live-spec", "checkpoints")
ARCHIVE = os.path.join("docs", "queue-archive")

# ---------------------------------------------------------------- the craft set, one home
# Requirement 309 criteria 77-84: the fixed craft set and its icons live in the board's own source
# file and nowhere else, and they are DISPLAY names of the pipeline's craft standards — the skill
# names stay internal and never reach a card. A step whose record names no craft is shown with its
# craft unnamed rather than guessed (criterion 84).
CRAFTS = (
    ("Reader", "\U0001f4d6"),
    ("Drafter", "✍️"),
    ("Reviewer", "\U0001f50e"),
    ("Builder", "\U0001f528"),
    ("Checker", "\U0001f9ea"),
)
CRAFT_UNNAMED = "craft unnamed"
# The tier note stands muted beside the craft name (criterion 81). These are the tiers this
# project's own workers are logged under; a record naming none carries no tier note.
TIERS = ("opus", "sonnet", "haiku", "fable")

# How many queued rows stand visible at the head before the rest collapse (criterion 24, the
# retunable value). Not a number invented here: it is the same nine rows scripts/state-probe.sh
# shows at the head of the Canon, so the page and the probe ration the same queue the same way.
QUEUE_HEAD = 9

# The surface registry row this page must hold before it renders (criterion 9). The needle is the
# text the completeness check reads back in the rendered page.
SURFACE_NAME = "work-board"


def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    return r.stdout.strip()


def read_text(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


# ---------------------------------------------------------------- stamps
# Requirement 309 criteria 63-67 want the time a task was given against the time it took. No
# artifact in this tree carries an ESTIMATE — no ticket field, no checkpoint line, no report —
# so the board states that plainly per card rather than printing an invented number. The ACTUAL
# comes from the stamps the checkpoint file already carries: it is created when the ticket is
# admitted and written again at every transition, the last of which is the close.
NOW = datetime.now()


def stamps(path):
    try:
        st = os.stat(path)
    except OSError:
        return None, None
    born = getattr(st, "st_birthtime", st.st_ctime)
    return datetime.fromtimestamp(born), datetime.fromtimestamp(st.st_mtime)


def span(minutes):
    minutes = int(round(minutes))
    if minutes < 60:
        return "%d min" % minutes
    if minutes < 60 * 24:
        return "%dh %02dm" % (minutes // 60, minutes % 60)
    return "%dd %dh" % (minutes // 1440, (minutes % 1440) // 60)


# ---------------------------------------------------------------- the checkpoints
def read_checkpoints():
    out = {}
    if checkpoint is None or not os.path.isdir(CHECKPOINTS):
        return out
    for name in sorted(os.listdir(CHECKPOINTS)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(CHECKPOINTS, name)
        try:
            cp = checkpoint.read_checkpoint(path)
        except (ValueError, OSError):
            continue
        born, changed = stamps(path)
        cp["path"] = path
        cp["opened"] = born
        cp["changed"] = changed
        out[name[:-3]] = cp
    return out


CPS = read_checkpoints()


def section(cp, name):
    return (cp.get("sections", {}).get(name) or "").strip() if cp else ""


def is_empty_section(text):
    low = text.strip().lower()
    return not low or low == "none" or low == "-" or (low.startswith("(nothing") and low.endswith(")"))


# ---------------------------------------------------------------- attribution
def craft_of(text):
    low = (text or "").lower()
    for name, icon in CRAFTS:
        if name.lower() in low:
            return name, icon
    return None


def tier_of(text):
    low = (text or "").lower()
    for tier in TIERS:
        if re.search(r"\b%s\b" % tier, low):
            return tier
    return None


HOLDER_RE = re.compile(r"^\*\*Holder:\*\*\s*(.+)$", re.M)


def holder_of(task):
    m = HOLDER_RE.search("\n".join(task["body"]))
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------- the lanes
def lane_cap():
    """The same cap scripts/open-lane.sh enforces, read from the same place: no second number."""
    profile = os.environ.get("LIVE_SPEC_PROFILE",
                             os.path.expanduser("~/.claude/live-spec/profile.md"))
    text = read_text(profile)
    if text:
        m = re.search(r"lanes\.cap:\s*(\d+)", text)
        if m:
            return int(m.group(1))
    return 3


LANE_BRANCH_RE = re.compile(r"^lane/([a-z]+-\d+)-")


def lane_claims():
    """Row id -> the branch and worktree its lane rides, read from git itself (criterion 40)."""
    claims = {}
    for line in git("branch", "--list", "lane/*").splitlines():
        # git marks the current branch with "*" and a branch checked out in ANOTHER worktree
        # with "+" — a lane branch is always the second case, so stripping only "*" left every
        # open lane unread and every in-work row printing the primary tree instead of its lane.
        name = line.strip().lstrip("*+").strip()
        m = LANE_BRANCH_RE.match(name)
        if m:
            claims[m.group(1)] = {"branch": name, "worktree": None}
    current = None
    for line in git("worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            current = line[len("worktree "):].strip()
        elif line.startswith("branch "):
            branch = line[len("branch "):].strip().replace("refs/heads/", "")
            m = LANE_BRANCH_RE.match(branch)
            if m and m.group(1) in claims:
                claims[m.group(1)]["worktree"] = current
    return claims


CAP = lane_cap()
CLAIMS = lane_claims()
PRIMARY_TREE = git("rev-parse", "--show-toplevel") or os.path.abspath(".")
PRIMARY_BRANCH = git("branch", "--show-current") or "main"


# ---------------------------------------------------------------- where a card points
SPEC_ANCHOR_RE = re.compile(r"(spec/[a-z0-9-]+\.md|PRODUCT_SPEC\.md|INV-\d+|R\d+\.\d+"
                            r"|Requirement \d+|M-\d+|E-\d+|T-\d+)")


def spec_anchor(task):
    """The part of the product spec a row changes, read from the row's own words (criterion 33).

    Never guessed: a row naming no anchor says so, which is a defect a reader can see and fix,
    not a chip the board fills in for it.
    """
    haystack = " ".join(filter(None, [task.get("source"), " ".join(task["body"])]))
    m = SPEC_ANCHOR_RE.search(haystack)
    return m.group(1) if m else None


TERMINAL_RE = re.compile(r"\b(landed|declined|superseded|decided)\b", re.I)
DOOR_RE = re.compile(r"\b(feature|bug|refactor|docs-only|skip)\b", re.I)


def terminal_state(task):
    m = TERMINAL_RE.search(" ".join(task["body"]))
    return m.group(1).lower() if m else "landed"


def door_of(task):
    """Criterion 72's door chip, read from the row's own intake note. Nothing in this tree's rows
    records a door, so a row carrying none says so rather than being sorted into a made-up one."""
    m = DOOR_RE.search(task.get("source") or "")
    return m.group(1).lower() if m else None


# ---------------------------------------------------------------- read the plan
text = read_text("PLAN.md") or ""
tasks = parse_tasks(text)
evaluate(tasks)

# ---------------------------------------------------------------- split each row's body
def split_body(body_lines):
    paragraphs, bullets, accept = [], [], []
    cur_para = []
    in_accept = False
    for ln in body_lines:
        s = ln.strip()
        if s == "---":
            break
        if not s:
            if in_accept:
                break
            if cur_para:
                paragraphs.append(" ".join(cur_para))
                cur_para = []
            continue
        if s.startswith("**Acceptance:**"):
            in_accept = True
            accept.append(s[len("**Acceptance:**"):].strip())
        elif in_accept:
            accept.append(s)
        else:
            bm = re.match(r"^-\s+(?:\[(.)\]\s*)?(.+)$", s)
            if bm:
                bullets.append({"mark": bm.group(1), "text": bm.group(2)})
            elif bullets:
                bullets[-1]["text"] += " " + s
            else:
                cur_para.append(s)
    if cur_para:
        paragraphs.append(" ".join(cur_para))
    return paragraphs, bullets, " ".join(accept)


def summarize(paragraph, limit=200):
    t = paragraph.strip()
    if not t:
        return "", False
    m = re.search(r"[.!?](?=\s|$)", t)
    if m and m.end() <= limit:
        return t[: m.end()], False
    if len(t) <= limit:
        return t, False
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")
    return (cut or t[:limit]), True


# ---------------------------------------------------------------- build one card
def split_source_tail(task):
    """The plan's Source line wraps, and the parser keeps only its first line in `source`.

    Its continuation lines sit at the head of the body with no blank line before them, so a card
    whose description was read straight off the first body paragraph opened mid-sentence. They
    belong to the source, and this puts them back before the description is read.
    """
    body = list(task["body"])
    if not task.get("source") or not body or not body[0].strip():
        return body
    tail = []
    while body and body[0].strip():
        tail.append(body.pop(0).strip())
    if tail:
        task["source"] = task["source"] + " " + " ".join(tail)
    return body


def build_card(task, archived=False, archive_file=None):
    paragraphs, bullets, accept = split_body(split_source_tail(task))
    cp = CPS.get(task["id"])
    holder = holder_of(task)
    who = holder or (cp.get("owner") if cp else None)
    # The craft the RECORD names, never one guessed for it (criterion 84): the holder line the
    # plan carries, else the checkpoint's own IN PROGRESS line, else unnamed.
    craft = craft_of(holder or "") or (craft_of(section(cp, "IN PROGRESS")) if cp else None)
    tier = tier_of(holder or "") or (tier_of(cp.get("owner", "")) if cp else None)

    opened = cp["opened"] if cp else None
    changed = cp["changed"] if cp else None
    closed = changed if (cp and cp.get("status") == "closed") else None

    actual = None
    running = None
    if opened and closed:
        actual = span((closed - opened).total_seconds() / 60.0)
    elif opened:
        running = span((NOW - opened).total_seconds() / 60.0)

    parked = (task["icon"] == "⬜" and cp is not None and cp.get("status") == "open"
              and not is_empty_section(section(cp, "NEXT")))
    preempted_by = None
    if parked:
        m = re.search(r"\b([a-z]+-\d+)\b", section(cp, "NEXT"))
        preempted_by = m.group(1) if m else None

    summary, truncated = ("", False)
    if paragraphs:
        summary, truncated = summarize(paragraphs[0])

    card = {
        "id": task["id"],
        "echo": task["title"],
        "icon": task["icon"],
        "description": summary + ("…" if truncated else ""),
        "paragraphs": paragraphs[1:] if paragraphs else [],
        "bullets": bullets,
        "accept": accept,
        "group": task.get("group") or "ungrouped",
        "priority": (task.get("priority") or "normal").lower(),
        "source": task.get("source") or "",
        "deferred": task.get("deferred"),
        "blocked_by": task.get("blocked_by"),
        "holder": holder,
        "session": who or "session not recorded",
        "craft": craft[0] if craft else CRAFT_UNNAMED,
        "craft_icon": craft[1] if craft else "",
        "tier": tier,
        "spec_anchor": spec_anchor(task),
        "door": door_of(task),
        "estimate": None,   # no artifact in this tree carries one — see criteria 63-65 below
        "actual": actual,
        "running": running,
        "opened": opened.isoformat(timespec="minutes") if opened else None,
        "closed": closed.isoformat(timespec="minutes") if closed else None,
        "closed_date": closed.date().isoformat() if closed else None,
        "parked": parked,
        "preempted_by": preempted_by,
        "verified": task["verified"],
        "failing_key": task["failing_key"],
        "note": task["note"],
        "archived": archived,
        "archive_file": archive_file,
        "terminal": terminal_state(task) if archived else None,
        "stage": None,
        "checkpoint": None,
        "branch": None,
        "worktree": None,
    }

    if cp:
        in_progress = section(cp, "IN PROGRESS")
        card["checkpoint"] = {
            "path": cp["path"],
            "status": cp.get("status"),
            "done": section(cp, "DONE"),
            "in_progress": in_progress,
            "next": section(cp, "NEXT"),
        }
        # Criterion 35 asks for the one pipeline stage of the nine the row stands at. No artifact
        # in this tree records a pipeline stage, so the board shows the stage the record DOES
        # carry — the checkpoint's own IN PROGRESS line — and says when there is none.
        card["stage"] = (in_progress.splitlines()[0].strip()
                         if not is_empty_section(in_progress) else None)

    claim = CLAIMS.get(task["id"])
    if claim:
        card["branch"], card["worktree"] = claim["branch"], claim["worktree"]
    elif task["icon"] in ("\U0001f504", "\U0001f501"):
        card["branch"], card["worktree"] = PRIMARY_BRANCH, PRIMARY_TREE
    return card


# ---------------------------------------------------------------- one column each
# Criterion 22: an open row's column is read off the status its own queue row records — awaiting
# validation off *queued*, ready off *ready*, in work off *in-work*. A blocked row keeps the
# column its own state names (criterion 18): the state machine's own T5 lands a cleared block in
# hand when a holder is named and queued when none is, so that is where a blocked row stands.
# A parked row stands in the in-work column marked parked (criterion 26) — its checkpoint is open
# and its NEXT says what remains, which is work in flight with nobody holding it.
def column_of(card):
    if card["icon"] == "✅":
        return "done"
    if card["parked"]:
        return "inwork"
    if card["icon"] in ("\U0001f504", "\U0001f501"):
        return "inwork"
    if card["icon"] == "⛔":
        return "inwork" if card["holder"] else "validate"
    return "validate"


cards = [build_card(t) for t in tasks]
for c in cards:
    c["column"] = column_of(c)

# ---------------------------------------------------------------- the done column's archive half
# Criterion 68: a closed row keeps its row rather than being cleared. Criterion 70: the done column
# reads the month's archive file under docs/queue-archive/, the current month standing by default
# and an older month opening on the person's ask. In this host a row stays on the plan page when it
# closes and moves to an archive later, so the done column is both: the plan's own closed rows and
# the current month's archive.
MONTH = NOW.strftime("%Y-%m")


def archive_months():
    months = {}
    if not os.path.isdir(ARCHIVE):
        return months
    for name in sorted(os.listdir(ARCHIVE)):
        if not name.endswith(".md"):
            continue
        m = re.search(r"(\d{4}-\d{2})", name)
        if m:
            months.setdefault(m.group(1), []).append(name)
    return months


ARCHIVE_MONTHS = archive_months()


def archive_cards(month):
    out = []
    for name in ARCHIVE_MONTHS.get(month, []):
        body = read_text(os.path.join(ARCHIVE, name)) or ""
        for task in _parse_headings(body.splitlines()):
            task.setdefault("check", None)
            evaluate([task])
            card = build_card(task, archived=True, archive_file=name)
            card["column"] = "done"
            out.append(card)
    return out


seen = {c["id"] for c in cards}
for card in archive_cards(MONTH):
    if card["id"] not in seen:
        cards.append(card)
        seen.add(card["id"])

BY_COLUMN = {"validate": [], "ready": [], "inwork": [], "done": []}
for c in cards:
    BY_COLUMN[c["column"]].append(c)

# Criterion 25: the deferred rows show as a stated count alone, each revisit trigger behind an
# expand. Criterion 23: the far tier stands down by name. Neither is a column: they are rows held
# out of the runnable head, and the page says how many and on what trigger.
# The far tier is the plan's own *far* status word, which the shared parser records in a row's
# deferred cell (plan_checks_core._TABLE_PARKED). This project's plan is the headings shape and
# writes no status word at all, so its far tier is empty — and the page still names it, because a
# reader has to be told the tier exists and opens on request rather than left to assume it does not.
FAR = [c for c in BY_COLUMN["validate"] if c["deferred"] and "far" in c["deferred"].lower()]
DEFERRED = [c for c in BY_COLUMN["validate"] if c["deferred"] and c not in FAR]
RUNNABLE = [c for c in BY_COLUMN["validate"] if not c["deferred"]]

CLOSED_TODAY = sum(1 for c in BY_COLUMN["done"] if c["closed_date"] == NOW.date().isoformat())

# ---------------------------------------------------------------- lanes
# Criterion 27-29: the in-work column splits into one lane per build lane the cap allows; a lane
# holding no row reads as free; a free lane draws the head *ready* task into it, and this host's
# plan records no *ready* status, so a free lane says what it is waiting for.
INWORK = [c for c in BY_COLUMN["inwork"] if not c["parked"]]
PARKED = [c for c in BY_COLUMN["inwork"] if c["parked"]]

lanes = []
claimed = [c for c in INWORK if c["branch"] and c["branch"].startswith("lane/")]
loose = [c for c in INWORK if c not in claimed]
for n in range(1, CAP + 1):
    lanes.append({"n": n, "card": None})
for card in claimed + loose:
    free = next((l for l in lanes if l["card"] is None), None)
    if free:
        free["card"] = card
    else:
        lanes.append({"n": len(lanes) + 1, "card": card, "over_cap": True})
BUSY = sum(1 for l in lanes if l["card"])

# ---------------------------------------------------------------- the waiting region
# Criterion 17: the region renders WAITING.md and keeps no list of its own, so one clearing rule
# and one gate hold every waiting item.
def waiting_items():
    body = read_text("WAITING.md")
    if body is None:
        return None
    m = re.search(r"<!-- board:shown -->(.*?)(?=\n## |\Z)", body, re.S)
    if not m:
        return []
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    return [ln for ln in lines if not ln.startswith("(nothing")]


WAITING = waiting_items()

# ---------------------------------------------------------------- the timestamped feed
# Criterion 16's feed: the records this project actually writes, each with the time it was written.
FEED = sorted((cp for cp in CPS.values() if cp.get("changed")),
              key=lambda cp: cp["changed"], reverse=True)[:8]

# ---------------------------------------------------------------- the registry (criterion 9)
def registry_needle():
    body = read_text("SURFACES.md")
    if body is None:
        return None, "no registry in this tree"
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0] == SURFACE_NAME:
            if not cells[1]:
                return None, "the %s row carries no needle" % SURFACE_NAME
            return cells[1], cells[2]
    return None, "SURFACES.md has no %s row" % SURFACE_NAME


NEEDLE, ANCHORS = registry_needle()
if NEEDLE is None and read_text("SURFACES.md") is not None:
    sys.stderr.write(
        "render-board: the work board registers before it renders (Requirement 309 criterion 9) — "
        "%s\n" % ANCHORS)
    raise SystemExit(2)

# ---------------------------------------------------------------- git state
project = os.path.basename(os.path.abspath("."))
head_sha = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
dirty = len([l for l in git("status", "--porcelain").splitlines() if l.strip()])
now_h = NOW.strftime("%H:%M, %d.%m.%Y")

# What the board needs of the person, on the one identifying line every opened artifact carries
# (criterion 10) — read from the waiting list, which is where an item waiting on him actually is.
if WAITING:
    NEEDS = "%d item%s waiting on you" % (len(WAITING), "" if len(WAITING) == 1 else "s")
else:
    NEEDS = "nothing waiting on you"

model = {
    "project": project,
    "built": NOW.isoformat(timespec="minutes"),
    "needle": NEEDLE,
    "anchors": ANCHORS,
    "needs": NEEDS,
    "lane_cap": CAP,
    "lanes_busy": BUSY,
    "closed_today": CLOSED_TODAY,
    "queue_head": QUEUE_HEAD,
    "crafts": [name for name, _ in CRAFTS],
    "waiting": WAITING,
    "deferred": [c["id"] for c in DEFERRED],
    "far": len(FAR),
    "columns": {k: [c["id"] for c in v] for k, v in BY_COLUMN.items()},
    "parked": [c["id"] for c in PARKED],
    "lane_rows": [{"n": l["n"], "id": l["card"]["id"] if l["card"] else None} for l in lanes],
    "cards": {c["id"]: c for c in cards},
}

if json_mode:
    print(json.dumps(model, ensure_ascii=False, indent=1, default=str))
    raise SystemExit(0)


# ---------------------------------------------------------------- render
def esc(s):
    return html.escape(str(s), quote=False)


_CODE_RE = re.compile(r"`([^`]+?)`")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def render_inline_md(t):
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return "\x00CODE%d\x00" % (len(codes) - 1)

    tmp = _CODE_RE.sub(stash, t)
    tmp = _BOLD_RE.sub(lambda m: "\x00B\x00" + m.group(1) + "\x00/B\x00", tmp)
    tmp = esc(tmp)
    tmp = tmp.replace("\x00B\x00", "<b>").replace("\x00/B\x00", "</b>")
    for i, code_text in enumerate(codes):
        tmp = tmp.replace("\x00CODE%d\x00" % i, "<code>%s</code>" % esc(code_text))
    return tmp


def balance(s):
    if s.count("**") % 2 == 1:
        s += "**"
    if s.count("`") % 2 == 1:
        s += "`"
    return s


def mark_icon(mark):
    return {"x": "✅", "~": "\U0001f504", "!": "⛔"}.get(mark, "⬜")


def chips(card):
    """A card's chips, in the one order criterion 30 fixes: they come after the echo-name and the
    description, and every other detail sits behind the card."""
    out = []
    out.append("<span class='chip place'>%s</span>" % esc(card["group"]))
    out.append("<span class='chip door'>%s</span>"
               % esc(card["door"] or "door not recorded"))
    if card["spec_anchor"]:
        out.append("<span class='chip spec'>%s</span>" % esc(card["spec_anchor"]))
    else:
        out.append("<span class='chip spec none'>no spec anchor on this row</span>")
    out.append("<span class='chip est'>%s</span>" % esc(time_pair(card)))
    craft = "%s %s" % (card["craft_icon"], card["craft"]) if card["craft_icon"] else card["craft"]
    tier = "<span class='tier'>· %s</span>" % esc(card["tier"]) if card["tier"] else ""
    out.append("<span class='chip worker'>%s%s</span>" % (esc(craft.strip()), tier))
    out.append("<span class='chip who'>session: %s</span>" % esc(card["session"]))
    if card["blocked_by"]:
        since = ""
        if card["checkpoint"] and card["opened"]:
            since = " · standing since %s" % esc(card["opened"].replace("T", " "))
        out.append("<span class='chip blocked'>blocked — %s%s</span>"
                   % (esc(card["blocked_by"]), since))
    if card["parked"]:
        by = (" — %s took the lane" % esc(card["preempted_by"])) if card["preempted_by"] \
            else " — the row that took the lane is not recorded"
        out.append("<span class='chip parked'>parked%s</span>" % by)
    return "".join(out)


def time_pair(card):
    """Criteria 63-67 — the time the task was given beside the time it took.

    THE ESTIMATE IS NOT RECORDED ANYWHERE IN THIS TREE. No ticket field, no checkpoint line and no
    delivery report carries one, so the board says so instead of printing a number nobody wrote.
    The actual and the end-to-end are real: they are read off the checkpoint's own stamps, which
    are written when the ticket is admitted and again at every transition through to the close.
    """
    if card["actual"]:
        return "no estimate recorded → took %s (opened %s, closed %s)" % (
            card["actual"], card["opened"].replace("T", " "), card["closed"].replace("T", " "))
    if card["running"]:
        return "no estimate recorded → running %s so far (opened %s)" % (
            card["running"], card["opened"].replace("T", " "))
    return "no estimate recorded, and no checkpoint stamps to read a time from"


def bullet_html(b):
    t = render_inline_md(b["text"])
    if b["mark"] is None:
        return "<li>%s</li>" % t
    return "<li class='subtask'><span class='mark'>%s</span> %s</li>" % (mark_icon(b["mark"]), t)


def details_html(card):
    d = ""
    if card["stage"]:
        d += "<p class='st'><b>Stage the record names:</b> %s</p>" % render_inline_md(card["stage"])
    else:
        d += "<p class='st'><b>Stage:</b> not recorded on this row's checkpoint</p>"
    if card["branch"]:
        d += ("<p class='st'><b>Branch and worktree:</b> <code>%s</code> in <code>%s</code></p>"
              % (esc(card["branch"]), esc(card["worktree"] or "not checked out")))
    if card["bullets"]:
        d += "<p class='dl'><b>The plan for this task</b></p><ul>%s</ul>" % "".join(
            bullet_html(b) for b in card["bullets"])
    cp = card["checkpoint"]
    if cp:
        if not is_empty_section(cp["next"]):
            d += "<p class='st'><b>Next on this task:</b> %s</p>" % render_inline_md(cp["next"])
        if not is_empty_section(cp["done"]):
            d += "<p class='st'><b>Done on this task:</b> %s</p>" % render_inline_md(
                cp["done"][:1200])
        d += "<p class='st'>Record: <code>%s</code> (%s)</p>" % (esc(cp["path"]), esc(cp["status"]))
    for p in card["paragraphs"]:
        d += "<p>%s</p>" % render_inline_md(p)
    d += "<p class='st'>session: %s · %s</p>" % (esc(card["session"]), esc(
        ("%s %s" % (card["craft_icon"], card["craft"])).strip()))
    if card["source"]:
        d += "<p class='st'><b>Source:</b> %s</p>" % render_inline_md(card["source"])
    if card["accept"]:
        d += "<p class='accept'><b>Acceptance:</b> %s</p>" % render_inline_md(card["accept"])
    if card["spec_anchor"] and card["spec_anchor"].startswith("spec/"):
        d += "<p class='st'>Spec this row changes: <a href='%s'>%s</a></p>" % (
            esc(card["spec_anchor"]), esc(card["spec_anchor"]))
    if card["failing_key"]:
        d += "<p class='st'>%s</p>" % esc(card["note"])
    return d


def card_html(card):
    verified = ("marked done in the plan, but %s" % card["note"]) if card["failing_key"] else (
        "verified by its acceptance command" if card["verified"]
        else "declared, no acceptance command")
    return """
    <div class="card" id="card-%s">
      <div class="handle">%s <span class="mk">%s</span></div>
      <p class="behav">%s</p>
      <div class="chips">%s</div>
      <div class="meta">%s · %s priority · %s</div>
      <details><summary>more</summary>%s</details>
    </div>""" % (
        esc(card["id"]), esc(card["echo"]), card["icon"],
        render_inline_md(balance(card["description"])) or "no description on this row",
        chips(card), esc(card["id"]), esc(card["priority"]), esc(verified),
        details_html(card),
    )


def done_line(card):
    """Criterion 69: a closed task renders as one line — state mark, echo-name, time pair — the
    rest behind a fold. Criterion 71: its own terminal state stands on it."""
    return """
    <div class="card closed" id="card-%s">
      <div class="doneline">%s <b>%s</b> <span class="st">%s · %s</span></div>
      <details><summary>more</summary>%s</details>
    </div>""" % (
        esc(card["id"]), card["icon"], esc(card["echo"]),
        esc(card["terminal"] or "landed"), esc(time_pair(card)), details_html(card))


# ---------------------------------------------------------------- the in-work column
lane_html = ""
for lane in lanes:
    if lane["card"]:
        lane_html += ("<div class='lane'><div class='lanelbl'>Lane %d</div>%s</div>"
                      % (lane["n"], card_html(lane["card"])))
free_lanes = [l["n"] for l in lanes if not l["card"]]
if free_lanes:
    lane_html += ("<div class='lane free'><div class='lanelbl'>Lane%s %s — free</div>"
                  "<p class='freebox'>%s. A free lane draws the head ready task the moment one "
                  "passes validation; a lane already holding a row draws none.</p></div>"
                  % ("" if len(free_lanes) == 1 else "s",
                     ", ".join(str(n) for n in free_lanes),
                     "Holding no row" if len(free_lanes) == 1
                     else "%d of the %d lanes the cap allows hold no row" % (len(free_lanes), CAP)))
if PARKED:
    lane_html += "<div class='lane'><div class='lanelbl'>Parked — holding no lane</div>%s</div>" % (
        "".join(card_html(c) for c in PARKED))
if not INWORK and not PARKED:
    head = ("The head of the queue is: %s." % esc(RUNNABLE[0]["echo"])) if RUNNABLE \
        else "The queue behind it is empty too."
    lane_html += "<p class='empty'>Nothing is in hand right now. %s</p>" % head

# ---------------------------------------------------------------- the awaiting-validation column
head_cards = RUNNABLE[:QUEUE_HEAD]
rest_cards = RUNNABLE[QUEUE_HEAD:]
validate_html = "".join(card_html(c) for c in head_cards) or "<p class='empty'>empty</p>"
if rest_cards:
    validate_html += ("<details class='pile'><summary>%d more queued rows stand below the head "
                      "— open them</summary>%s</details>"
                      % (len(rest_cards), "".join(card_html(c) for c in rest_cards)))
if DEFERRED:
    # A stated count alone, each row's revisit trigger behind the expand (criterion 25) — and the
    # row's own card inside it, since criterion 24's "drop none in silence" holds here too.
    validate_html += ("<details class='pile'><summary>%d deferred rows — each opens on its own "
                      "revisit trigger</summary>%s</details>"
                      % (len(DEFERRED), "".join(
                          "<p class='st'>revisits when: %s</p>%s"
                          % (render_inline_md(c["deferred"]), card_html(c)) for c in DEFERRED)))
validate_html += ("<p class='colnote'>The far tier stands down by name: %d rows are kept off this "
                  "board and open only when you ask for them.</p>" % len(FAR))

# ---------------------------------------------------------------- the done column
done_sorted = sorted(BY_COLUMN["done"], key=lambda c: c["closed"] or "", reverse=True)
done_html = "".join(done_line(c) for c in done_sorted) or "<p class='empty'>empty</p>"
other_months = [m for m in sorted(ARCHIVE_MONTHS, reverse=True) if m != MONTH]
if other_months:
    done_html += ("<details class='pile'><summary>earlier months — open one</summary>%s</details>"
                  % "".join("<p class='st'>%s: %s</p>"
                            % (esc(m), ", ".join("<a href='%s/%s'>%s</a>" % (esc(ARCHIVE), esc(n), esc(n))
                                                 for n in ARCHIVE_MONTHS[m]))
                            for m in other_months))

# ---------------------------------------------------------------- the ready column
ready_html = ("".join(card_html(c) for c in BY_COLUMN["ready"])
              or "<p class='empty'>Nothing is checked and waiting. A row lands here when its "
                 "statement passes validation, and the check that would pass it is not built.</p>")

COLUMNS = [
    ("inwork", "In work", "%d of %d lanes busy" % (BUSY, CAP),
     "a card leaves when its acceptance command passes", lane_html),
    ("ready", "Ready", "%d" % len(BY_COLUMN["ready"]),
     "a card leaves when a free lane draws it", ready_html),
    ("validate", "Awaiting validation", "%d" % len(RUNNABLE),
     "a card leaves when its statement passes validation", validate_html),
    ("done", "Done", "%d today" % CLOSED_TODAY,
     "nothing leaves this column — a closed row is kept, never cleared", done_html),
]

columns_html = "".join(
    "<div class='col %s'><div class='colhead'><h2>%s</h2><span class='count'>%s</span></div>"
    "<div class='sub'>%s</div><div class='colbody'>%s</div></div>" % (
        key, esc(label), esc(count), esc(leaves), body)
    for key, label, count, leaves, body in COLUMNS)

waiting_html = ""
if WAITING is None:
    waiting_html = "<p class='empty'>This project keeps no waiting list file.</p>"
elif not WAITING:
    waiting_html = "<p class='empty'>Nothing is waiting on you.</p>"
else:
    waiting_html = "<ul>%s</ul>" % "".join("<li>%s</li>" % render_inline_md(w) for w in WAITING)

feed_html = "".join(
    "<li><span class='ts'>%s</span> %s — %s</li>"
    % (esc(cp["changed"].strftime("%H:%M, %d.%m")), esc(cp["title"]), esc(cp["status"]))
    for cp in FEED) or "<li>no records written yet</li>"

craft_html = ", ".join("%s %s" % (icon, name) for name, icon in CRAFTS)

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{project} — the work board</title>
<style>
  :root {{ color-scheme: light dark; --ink: #16161a; --bg: #ffffff; --dim: #5a5a63;
           --line: #d5d5dd; --soft: #f4f4f7; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --ink: #ececf0; --bg: #141416; --dim: #a2a2ad; --line: #35353d; --soft: #1e1e22; }} }}
  body {{ font: 15px/1.55 -apple-system, "Segoe UI", sans-serif; max-width: 1440px;
         margin: 1.4rem auto 3rem; padding: 0 1.1rem; color: var(--ink); background: var(--bg); }}
  h1 {{ font-size: 1.3rem; margin: .2rem 0 .15rem; }}
  a {{ color: inherit; }}
  .stamp {{ color: var(--dim); font-size: .87rem; margin-bottom: 1.1rem; }}
  .board {{ display: grid; grid-template-columns: 1.4fr 1fr 1fr 1.1fr; gap: .9rem;
            align-items: start; }}
  .col {{ border: 1px solid var(--line); border-radius: 10px; padding: .65rem .7rem; }}
  .colhead {{ display: flex; justify-content: space-between; align-items: baseline; gap: .4rem; }}
  .col h2 {{ font-size: .9rem; margin: 0; text-transform: uppercase; letter-spacing: .04em; }}
  .count {{ color: var(--dim); font-size: .82rem; }}
  .sub {{ font-size: .78rem; color: var(--dim); margin: .1rem 0 .6rem; }}
  .colnote {{ font-size: .78rem; color: var(--dim); margin-top: .7rem; }}
  .lane {{ border: 1px dashed var(--line); border-radius: 8px; padding: .4rem .45rem;
           margin-bottom: .55rem; }}
  .lanelbl {{ font-size: .74rem; text-transform: uppercase; letter-spacing: .05em;
              color: var(--dim); margin-bottom: .3rem; }}
  .freebox {{ font-size: .82rem; color: var(--dim); margin: .1rem 0 .2rem; }}
  .card {{ border: 1px solid var(--line); border-radius: 8px; padding: .55rem .6rem;
           margin-bottom: .55rem; background: var(--bg); }}
  .handle {{ font-weight: 700; display: flex; justify-content: space-between; gap: .5rem; }}
  .behav {{ margin: .3rem 0; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: .3rem; margin: .35rem 0 .2rem; }}
  .chip {{ font-size: .74rem; border: 1px solid var(--line); border-radius: 999px;
           padding: .05rem .45rem; background: var(--soft); }}
  .chip.none {{ color: var(--dim); font-style: italic; }}
  .tier {{ color: var(--dim); }}
  .meta {{ font-size: .76rem; color: var(--dim); }}
  .doneline {{ display: flex; flex-wrap: wrap; gap: .4rem; align-items: baseline; }}
  .doneline .st {{ font-size: .78rem; color: var(--dim); }}
  details {{ margin-top: .35rem; font-size: .9rem; }}
  summary {{ cursor: pointer; color: var(--dim); padding: .15rem 0; }}
  summary:focus-visible {{ outline: 2px solid currentColor; }}
  details ul {{ margin: .3rem 0; padding-left: 1.1rem; }}
  li.subtask {{ list-style: none; margin-left: -1.1rem; }}
  li.subtask .mark {{ margin-right: .3rem; }}
  code {{ font: 85% ui-monospace, SFMono-Regular, Menlo, monospace; background: var(--soft);
          padding: .05rem .3rem; border-radius: 4px; }}
  .empty {{ color: var(--dim); font-size: .84rem; }}
  .below {{ display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; margin-top: 1.3rem; }}
  .panel {{ border: 1px solid var(--line); border-radius: 10px; padding: .65rem .75rem; }}
  .panel h2 {{ font-size: .9rem; margin: 0 0 .4rem; text-transform: uppercase;
               letter-spacing: .04em; }}
  .feed {{ list-style: none; padding: 0; margin: 0; font-size: .85rem; }}
  .feed .ts {{ color: var(--dim); }}
  .foot {{ font-size: .8rem; color: var(--dim); margin-top: 1.4rem; }}
  @media (max-width: 1000px) {{
    .board {{ grid-template-columns: 1fr; }}
    .below {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>

<h1>{project} — the work board</h1>
<div class="stamp">{needle} · {needs} · built {now} · {busy} of {cap} lanes busy
 · branch {branch} · {sha} &ldquo;{subj}&rdquo;{dirty}</div>

<div class="board">{columns}</div>

<div class="below">
  <div class="panel">
    <h2>Waiting on you</h2>
    <p class="empty">This region renders {waiting_file}. The board keeps no waiting list of its
    own, so one clearing rule holds every item on it.</p>
    {waiting}
  </div>
  <div class="panel">
    <h2>What was written, and when</h2>
    <ul class="feed">{feed}</ul>
  </div>
</div>

<div class="foot">
Every mark carries its meaning where it stands: ✅ done · \U0001f504 in hand ·
\U0001f501 was done and is not · ⬜ queued · ⛔ blocked on a cause outside the
work. The crafts a running step is named by: {crafts}; a step whose record names no craft reads
&ldquo;{unnamed}&rdquo;. This page reads PLAN.md, the checkpoints under {cpdir}, the lanes git
itself holds, {waiting_file} and the archive under {archive}:
there is no second source of state, and no history the journal already owns is written here. It answers to {anchors}. It does
not reload itself: draw it again when something changes.
</div>

</body>
</html>
""".format(
    project=esc(project), needle=esc(NEEDLE or "the work board"), needs=esc(NEEDS),
    now=esc(now_h), busy=BUSY, cap=CAP, branch=esc(PRIMARY_BRANCH), sha=esc(head_sha),
    subj=esc(head_subj), dirty=(" · uncommitted files: %d" % dirty) if dirty else " · tree clean",
    columns=columns_html, waiting=waiting_html, waiting_file="WAITING.md", feed=feed_html,
    crafts=craft_html, unnamed=CRAFT_UNNAMED, cpdir=esc(CHECKPOINTS), archive=esc(ARCHIVE),
    anchors=esc(ANCHORS or "no registry row"),
)

with open(out_path, "w", encoding="utf-8") as f:
    f.write(page)

print("written: %s (%d in work, %d awaiting validation, %d closed today)"
      % (out_path, len(INWORK) + len(PARKED), len(RUNNABLE), CLOSED_TODAY))
PYEOF
