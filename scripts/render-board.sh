#!/bin/bash
# render-board.sh — renders the plan's Canon (PLAN.md's `## Tasks` section, state read the way
# scripts/state-probe.sh reads it — from acceptance commands, not from a hand-set mark)
# as one self-contained HTML page, a pseudo-kanban with columns.
#
# Why: the owner asked four times for "one page I can just look at" instead of asking the
# agent how things are going. He does not want a separate board feature — the board is a
# rendering of the same Canon this project already computes (PLAN.md, §"Already decided"). This
# script does not invent a second source of state: every field it draws comes from PLAN.md's
# own text and from the same check commands state-probe.sh runs (both live in one home,
# scripts/plan_checks.py — its parse_tasks() and its CHECKS map).
#
# Card fields follow his own words, 2026-08-06 (recon: docs/research/2026-08-26-board-ticket-fields.md):
#   - a short, sharp handle first (the task title, verbatim from PLAN.md)
#   - a description right after it
#   - everything else behind a collapsible details toggle, never auto-closing
#   - a status shown as an icon, not a paragraph; "done" as an emoji, to save space
#   - no legend — the page must read on its own
#   - no options/choices shown on a card once its task is in progress
# Since PLAN.md's task-list merge (commit bc6f862b), every task also carries a Group, a
# Priority and a Source line — shown on every card, and used to cluster cards inside each
# column (his page, unlike the chat Canon, has the room to show everything; grouping is what
# keeps "everything" readable). Fields he asked for that no task carries (branch/worktree,
# given-vs-actual time, agent name, lanes) are left out rather than invented — those belong to
# the F-work-board product feature (spec/work-board.md, requirement 309), a separate, larger,
# still-unbuilt surface for host projects' own task queues, not this project's own plan.
#
# Usage: bash scripts/render-board.sh [output-file]   (default: board.html at repo root)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
OUT="${1:-board.html}"

python3 - "$OUT" <<'PYEOF'
import html
import re
import subprocess
import sys
from datetime import datetime

out_path = sys.argv[1]

# The parser and the commands that verify each plan task live in one home,
# scripts/plan_checks.py: a status board a person edits by hand must not also be an execution
# surface, and two copies of either would let this reader and scripts/state-probe.sh disagree
# about what a task is or what "done" means for it.
# Both readers cd to the repository root before this block runs, so "scripts" resolves.
sys.path.insert(0, "scripts")
from plan_checks import parse_tasks

# ---------------------------------------------------------------- read PLAN.md's tasks
# Same parser state-probe.sh uses: parse_tasks() reads the "## Tasks" section, one entry per
# "### <mark> Title — id: <id>" header, with its Group/Priority/Source lines and the rest of
# its body (the full original prose and Acceptance line the plan-N tasks still carry).
text = open("PLAN.md", encoding="utf-8").read()
lines = text.splitlines()
steps = parse_tasks(text)
for s in steps:
    s["num"] = s["id"]

# ---------------------------------------------------------------- split each step's body
# into its prose paragraphs (in source order), a bullet list (its deliverables/details, each
# carrying its own checkbox mark when it has one), and the acceptance line
# ("**Acceptance:**...") — the things his 2026-08-06 words asked for: a short summary up
# front, then everything else behind a details toggle.
def split_body(body_lines):
    paragraphs, bullets, accept = [], [], []
    cur_para = []
    in_accept = False
    for ln in body_lines:
        s = ln.strip()
        if s == "---":
            break  # the horizontal rule that closes a step; nothing after it is this step's
        if not s:
            if in_accept:
                break  # a blank line ends the acceptance paragraph
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
                # a soft-wrapped continuation of the previous bullet
                bullets[-1]["text"] += " " + s
            else:
                cur_para.append(s)
    if cur_para:
        paragraphs.append(" ".join(cur_para))
    return paragraphs, bullets, " ".join(accept)

# ---------------------------------------------------------------- run acceptance commands
# Exactly state-probe.sh's rule: a task with a command in CHECKS is VERIFIED by running it; a
# task with none is DECLARED — its mark is the only claim, and the page says so plainly rather
# than pretending it was measured (law 3: every accepted task has a command and an observable
# result; a task without one is a wish, not a fact). A checked task that fails its command
# falls back to its own mark (🔄/⛔/👁️/⬜) rather than a flat "not done" — the new mark
# vocabulary already distinguishes those states, unlike the plan's old x/~/!/space marks.
for s in steps:
    paragraphs, bullets, accept = split_body(s["body"])
    s["paragraphs"], s["bullets"], s["accept"] = paragraphs, bullets, accept
    if s["check"]:
        ok = subprocess.run(s["check"], shell=True, capture_output=True).returncode == 0
        s["verified"] = True
        s["icon"] = "✅" if ok else s["mark"]
    else:
        ok = s["mark"] == "✅"
        s["verified"] = False
        s["icon"] = s["mark"]
    s["done"] = ok

# ---------------------------------------------------------------- assign one column each
# Same four columns as before the task-list merge. The board can show every task (it is a
# page, not the chat Canon), so — unlike state-probe.sh, which has to ration lines — a task's
# own mark decides its column directly: ✅ (or a passing command) is Done; 🔄 is In progress
# (several can run at once, his own Canon rule: "tasks running side by side show as several
# 🔄 at once"); ⛔ and 👁️ both land on Blocked — a task needing his eyes can't move without
# him either, the same "waiting on the owner's word" this column already names; ⬜ is Not
# started.
for s in steps:
    if s["icon"] == "✅":
        s["column"] = "done"
    elif s["icon"] == "🔄":
        s["column"] = "inwork"
    elif s["icon"] in ("⛔", "👁️"):
        s["column"] = "blocked"
    else:
        s["column"] = "backlog"

COLUMNS = [
    ("backlog", "Not started", "waiting in queue"),
    ("inwork", "In progress", "in the pipeline right now"),
    ("done", "Done", "verified by its acceptance command"),
    ("blocked", "Blocked", "waiting on the owner's word"),
]

# ---------------------------------------------------------------- blockers (§Blockers)
# Shown once, off to the side — the same list state-probe.sh already prints, not a second
# board (WAITING.md is its own separate board for a separate thing: what waits on his eyes
# mid-conversation. PLAN.md's §Blockers is project-decision blockers; the two stay distinct).
blockers = []
in_blockers = False
for line in lines:
    if line.strip() == "## Blockers":
        in_blockers = True
        continue
    if in_blockers and line.startswith("## "):
        break
    if in_blockers and line.strip().startswith("- **"):
        blockers.append(line.strip()[2:])

# ---------------------------------------------------------------- git state (same facts state-probe.sh shows)
def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout.strip()

head_sha = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
branch = git("branch", "--show-current")
dirty = len([l for l in git("status", "--porcelain").splitlines() if l.strip()])
ahead = git("rev-list", "--count", "origin/main..HEAD") or "0"

now = datetime.now().strftime("%H:%M, %d.%m.%Y")

# ---------------------------------------------------------------- render
def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------- a small, dependency-free
# Markdown-to-HTML converter for exactly the constructs PLAN.md's step bodies actually use
# (checked by reading the file, not guessed): **bold** and `inline code`. No italics, no
# links, no headings, no fenced code blocks appear in any step body or blocker line, so none
# are handled — this stays a small converter for the plan's own vocabulary, not a general
# Markdown engine. Bullet lists and `- [x]`/`- [ ]` checkbox items are structural (parsed in
# split_body) and rendered separately in card_html/bullet_html, not by this function.
#
# Inline code is protected before bold is matched (and restored after everything else is
# escaped) so a bold span that contains code, e.g. "**`x` is stale**", nests correctly instead
# of one marker eating the other's delimiters.
_CODE_RE = re.compile(r"`([^`]+?)`")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")

def render_inline_md(text):
    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return "\x00CODE%d\x00" % (len(codes) - 1)

    tmp = _CODE_RE.sub(stash_code, text)
    tmp = _BOLD_RE.sub(lambda m: "\x00B\x00" + m.group(1) + "\x00/B\x00", tmp)
    tmp = esc(tmp)
    tmp = tmp.replace("\x00B\x00", "<b>").replace("\x00/B\x00", "</b>")
    for i, code_text in enumerate(codes):
        tmp = tmp.replace("\x00CODE%d\x00" % i, "<code>%s</code>" % esc(code_text))
    return tmp

def balance_markup(s):
    # A summary built by cutting a paragraph short can leave one half of a **bold** or `code`
    # pair behind. Close it rather than let render_inline_md leave a literal "**" or "`" in the
    # rendered prose (the owner's complaint in the first place).
    if s.count("**") % 2 == 1:
        s += "**"
    if s.count("`") % 2 == 1:
        s += "`"
    return s

def summarize(paragraph, limit=200):
    """The face of a card gets one short line — his 2026-08-06 words, matched to task 0's
    shape. Prefer the paragraph's first sentence; fall back to a word-boundary cut."""
    text = paragraph.strip()
    if not text:
        return "", False
    m = re.search(r"[.!?](?=\s|$)", text)
    if m and m.end() <= limit:
        return text[: m.end()], False
    if len(text) <= limit:
        return text, False
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")
    return (cut or text[:limit]), True

def mark_icon(mark):
    # Same icon vocabulary as the card's own chip and as state-probe.sh's mark icons — a
    # subtask's status reads in the same visual language as its parent task's (his complaint:
    # subtasks should carry their own status, on this board's own terms).
    return {"x": "✅", "~": "🔄", "!": "⛔"}.get(mark, "⬜")

def bullet_html(b):
    text_html = render_inline_md(b["text"])
    if b["mark"] is None:
        return "<li>%s</li>" % text_html
    return "<li class='subtask'><span class='mark'>%s</span> %s</li>" % (mark_icon(b["mark"]), text_html)

def card_html(s):
    chip = s["icon"]
    verified = "verified by command" if s["verified"] else "declared, no acceptance command"

    # Face: title, a short summary (first sentence of the first paragraph, if there is one),
    # then the status line. Everything else — the rest of the prose, the bullets, the
    # acceptance line — sits behind "more", uniformly, task 0's shape carried to every card.
    summary_html = ""
    extra_paragraphs = []
    if s["paragraphs"]:
        summary_raw, truncated = summarize(s["paragraphs"][0])
        summary_html = render_inline_md(balance_markup(summary_raw))
        if truncated:
            summary_html += "…"
        extra_paragraphs = s["paragraphs"][1:]

    details = ""
    for p in extra_paragraphs:
        details += "<p>%s</p>" % render_inline_md(p)
    if s["bullets"]:
        details += "<ul>%s</ul>" % "".join(bullet_html(b) for b in s["bullets"])
    if s["accept"]:
        details += "<p class='accept'><b>Acceptance:</b> %s</p>" % render_inline_md(s["accept"])
    details_block = ""
    if details:
        details_block = (
            "<details><summary>more</summary>%s</details>" % details
        )

    # Every task carries a Group, a Priority and a Source since the task-list merge
    # (commit bc6f862b) — shown on the card face, not hidden behind "more": the id sits with
    # them for the rare case two titles are close enough to need it.
    meta = "%s · %s priority · %s" % (
        esc(s["group"] or "—"), esc((s["priority"] or "—").lower()), esc(s["id"]),
    )
    source_html = "<div class='source'>%s</div>" % render_inline_md(s["source"]) if s["source"] else ""

    return """
    <div class="card">
      <div class="handle">%s <span class="chip">%s</span></div>
      <div class="meta">%s</div>
      %s
      %s
      <div class="status">%s</div>
      %s
    </div>""" % (
        esc(s["title"]),
        chip,
        meta,
        "<p class='desc'>%s</p>" % summary_html if summary_html else "",
        source_html,
        esc(verified),
        details_block,
    )

# Cards cluster by the task's own Group field inside each column — a page has the room to
# show every one of the 160 tasks, and grouping is what keeps that readable (the chat Canon
# in state-probe.sh instead rations lines; this is the page's own way of handling the same
# volume). Groups sort alphabetically; cards inside a group keep PLAN.md's own order.
columns_html = ""
for key, label, sub in COLUMNS:
    col_steps = [s for s in steps if s["column"] == key]
    groups = {}
    for s in col_steps:
        groups.setdefault(s["group"] or "Ungrouped", []).append(s)
    if not col_steps:
        body = "<p class='empty'>empty</p>"
    else:
        body = "".join(
            "<div class='group'><h3>%s <span class='count'>%d</span></h3>%s</div>"
            % (esc(g), len(groups[g]), "".join(card_html(s) for s in groups[g]))
            for g in sorted(groups)
        )
    columns_html += """
  <div class="col">
    <h2>%s <span class="count">%d</span></h2>
    <div class="sub">%s</div>
    %s
  </div>""" % (esc(label), len(col_steps), esc(sub), body)

blockers_html = ""
if blockers:
    # Each blocker is captured as one line (the same first-line-per-finding convention
    # state-probe.sh's own printout uses; the full multi-paragraph finding stays in PLAN.md
    # itself), which can cut a **bold** or `code` span in half — close it before rendering so
    # no stray marker survives into the page.
    blockers_html = "<ul>%s</ul>" % "".join(
        "<li>%s</li>" % render_inline_md(balance_markup(b)) for b in blockers
    )
else:
    blockers_html = "<p class='empty'>no blockers</p>"

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>live-spec — board</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 15px/1.5 -apple-system, "Segoe UI", sans-serif; max-width: 1180px;
         margin: 1.5rem auto 3rem; padding: 0 1.2rem; color: #1c1c1e; background: #fff; }}
  @media (prefers-color-scheme: dark) {{ body {{ color: #e6e6e8; background: #161618; }} }}
  h1 {{ font-size: 1.25rem; margin: .2rem 0 .1rem; }}
  .stamp {{ opacity: .7; font-size: .9rem; margin-bottom: 1.2rem; }}
  .board {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; align-items: start; }}
  @media (max-width: 900px) {{ .board {{ grid-template-columns: 1fr 1fr; }} }}
  @media (max-width: 560px) {{ .board {{ grid-template-columns: 1fr; }} }}
  .col {{ border: 1px solid #8884; border-radius: 10px; padding: .7rem .8rem; min-height: 3rem; }}
  .col h2 {{ font-size: .92rem; margin: 0 0 .1rem; text-transform: uppercase; letter-spacing: .03em; opacity: .8; }}
  .col .sub {{ font-size: .8rem; opacity: .6; margin-bottom: .6rem; }}
  .count {{ opacity: .55; font-weight: 400; }}
  .card {{ border: 1px solid #8883; border-radius: 8px; padding: .6rem .7rem; margin-bottom: .6rem; }}
  .handle {{ font-weight: 700; display: flex; justify-content: space-between; gap: .5rem; }}
  .chip {{ flex: 0 0 auto; }}
  .meta {{ font-size: .78rem; opacity: .6; margin-top: .15rem; }}
  .source {{ font-size: .82rem; opacity: .75; margin-top: .3rem; }}
  .group {{ margin-bottom: .8rem; }}
  .group h3 {{ font-size: .78rem; margin: 0 0 .35rem; text-transform: uppercase;
              letter-spacing: .02em; opacity: .55; font-weight: 600; }}
  .desc {{ margin: .35rem 0; opacity: .88; }}
  .status {{ font-size: .8rem; opacity: .65; margin-top: .3rem; }}
  details {{ margin-top: .4rem; font-size: .9rem; }}
  summary {{ cursor: pointer; opacity: .7; }}
  details ul {{ margin: .3rem 0; padding-left: 1.1rem; }}
  details li {{ margin: .25rem 0; }}
  details li.subtask {{ list-style: none; margin-left: -1.1rem; }}
  details li.subtask .mark {{ margin-right: .3rem; }}
  code {{ font: 85% ui-monospace, SFMono-Regular, Menlo, monospace; background: #8882; padding: .05rem .3rem; border-radius: 4px; }}
  .accept {{ margin: .4rem 0 0; opacity: .85; }}
  .empty {{ opacity: .5; font-size: .85rem; }}
  .blockers {{ margin-top: 1.6rem; }}
  .blockers h2 {{ font-size: .95rem; }}
  .blockers ul {{ padding-left: 1.2rem; }}
  .blockers li {{ margin: .35rem 0; }}
  .git {{ font-size: .82rem; opacity: .65; margin-top: 1.6rem; }}
</style>
</head>
<body>

<h1>live-spec — board</h1>
<div class="stamp">Updated {now} · branch {branch} · {head_sha} "{head_subj}"{dirty_note}{ahead_note}</div>

<div class="board">{columns}</div>

<div class="blockers">
  <h2>Blockers</h2>
  {blockers}
</div>

<div class="git">This page reads PLAN.md and runs the same acceptance commands as scripts/state-probe.sh — there is no second source of state.</div>

</body>
</html>
""".format(
        now=now,
        branch=esc(branch),
        head_sha=esc(head_sha),
        head_subj=esc(head_subj),
        dirty_note=" · uncommitted files: %d" % dirty if dirty else " · tree clean",
        ahead_note=" · not pushed: %s" % ahead if ahead != "0" else "",
        columns=columns_html,
        blockers=blockers_html,
    )

with open(out_path, "w", encoding="utf-8") as f:
    f.write(page)

print("written: %s (%d steps, %d blockers)" % (out_path, len(steps), len(blockers)))
PYEOF
