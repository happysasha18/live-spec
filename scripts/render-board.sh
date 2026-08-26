#!/bin/bash
# render-board.sh — renders the plan's Canon (PLAN.md's ten steps, state read the way
# scripts/state-probe.sh reads it — from acceptance commands, not from a hand-set checkbox)
# as one self-contained HTML page, a pseudo-kanban with columns.
#
# Why: the owner asked four times for "one page I can just look at" instead of asking the
# agent how things are going. He does not want a separate board feature — the board is a
# rendering of the same Canon this project already computes (PLAN.md, §"Already decided"). This
# script does not invent a second source of state: every field it draws comes from PLAN.md's
# own text and from the same check commands state-probe.sh runs.
#
# Card fields follow his own words, 2026-08-06 (recon: docs/research/2026-08-26-board-ticket-fields.md):
#   - a short, sharp handle first (the step title, verbatim from PLAN.md)
#   - a description right after it
#   - everything else behind a collapsible details toggle, never auto-closing
#   - a status shown as an icon, not a paragraph; "done" as an emoji, to save space
#   - no legend — the page must read on its own
#   - no options/choices shown on a card once its step is in progress
# Fields he asked for that PLAN.md's steps do not carry (branch/worktree, given-vs-actual
# time, agent name, lanes) are left out rather than invented — those belong to the F-work-board
# product feature (spec/work-board.md, requirement 309), a separate, larger, still-unbuilt
# surface for host projects' own task queues, not this project's own ten-step plan.
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

# ---------------------------------------------------------------- read PLAN.md's steps
# Same parse shape as state-probe.sh: a step is a "### [mark] N. Title" header, optionally
# followed by a "<!-- check: CMD -->" comment, then body lines up to the next header or the
# "## Blockers" section close.
text = open("PLAN.md", encoding="utf-8").read()
lines = text.splitlines()

steps = []
cur = None
in_steps_section = False
for line in lines:
    if line.strip() == "## Steps":
        in_steps_section = True
        continue
    if in_steps_section and line.startswith("## "):
        break
    if not in_steps_section:
        continue
    m = re.match(r"^### \[(.)\] (\d+)\. (.+)$", line.rstrip())
    if m:
        cur = {"mark": m.group(1), "num": m.group(2), "title": m.group(3),
               "check": None, "body": []}
        steps.append(cur)
        continue
    m = re.match(r"^<!-- check: (.+) -->$", line.strip())
    if m and cur is not None:
        cur["check"] = m.group(1)
        continue
    if cur is not None:
        cur["body"].append(line)

# ---------------------------------------------------------------- split each step's body
# into a lead description paragraph, a bullet list (its deliverables/details), and the
# acceptance line ("**Acceptance:**...") — the three things his 2026-08-06 words asked for:
# description, then everything else behind a details toggle.
def split_body(body_lines):
    desc, bullets, accept = [], [], []
    in_accept = False
    for ln in body_lines:
        s = ln.strip()
        if s == "---":
            break  # the horizontal rule that closes a step; nothing after it is this step's
        if not s:
            if in_accept:
                break  # a blank line ends the acceptance paragraph
            continue
        if s.startswith("**Acceptance:**"):
            in_accept = True
            accept.append(s[len("**Acceptance:**"):].strip())
        elif in_accept:
            accept.append(s)
        elif s.startswith("- ") or s.startswith("  - "):
            bullets.append(s.lstrip("- ").strip())
        elif bullets:
            bullets[-1] = bullets[-1] + " " + s  # a soft-wrapped continuation of the last bullet
        elif not bullets:
            desc.append(s)
    return " ".join(desc), bullets, " ".join(accept)

# ---------------------------------------------------------------- run acceptance commands
# Exactly state-probe.sh's rule: a step with a check comment is VERIFIED by running it; a
# step with none is DECLARED — its mark is the only claim, and the page says so plainly
# rather than pretending it was measured (law 3: every accepted step has a command and an
# observable result; a step without one is a wish, not a fact).
for s in steps:
    desc, bullets, accept = split_body(s["body"])
    s["desc"], s["bullets"], s["accept"] = desc, bullets, accept
    if s["check"]:
        ok = subprocess.run(s["check"], shell=True, capture_output=True).returncode == 0
        s["verified"] = True
        s["done"] = ok
    else:
        s["verified"] = False
        s["done"] = s["mark"] == "x"

# ---------------------------------------------------------------- assign one column each
# Columns mirror PLAN.md's own mark vocabulary — "not started / in progress / closed / blocked" —
# plus the same "NEXT" (next up) rule state-probe.sh uses: the first step that is not done
# and not itself marked blocked is the one step in progress. Only one step is ever "in
# progress" at a time (his own definition, 2026-08-06 18:34: in-work means "in your pipeline"
# now, not a pile of maybes).
next_assigned = False
for s in steps:
    if s["mark"] == "!":
        s["column"] = "blocked"
    elif s["done"]:
        s["column"] = "done"
    elif not next_assigned:
        s["column"] = "inwork"
        next_assigned = True
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

def card_html(s):
    chip = ("✅" if s["done"] else "⛔") if s["mark"] in ("x", "!") else ("🔄" if s["column"] == "inwork" else "⬜")
    verified = "verified by command" if s["verified"] else "declared, no acceptance command"
    details = ""
    if s["bullets"]:
        items = "".join("<li>%s</li>" % esc(b) for b in s["bullets"])
        details += "<ul>%s</ul>" % items
    if s["accept"]:
        details += "<p class='accept'><b>Acceptance:</b> %s</p>" % esc(s["accept"])
    details_block = ""
    if details:
        details_block = (
            "<details><summary>more</summary>%s</details>" % details
        )
    return """
    <div class="card">
      <div class="handle">%s <span class="chip">%s</span></div>
      %s
      <div class="status">%s</div>
      %s
    </div>""" % (
        esc("%s. %s" % (s["num"], s["title"])),
        chip,
        "<p class='desc'>%s</p>" % esc(s["desc"]) if s["desc"] else "",
        esc(verified),
        details_block,
    )

columns_html = ""
for key, label, sub in COLUMNS:
    cards = "".join(card_html(s) for s in steps if s["column"] == key)
    if not cards:
        cards = "<p class='empty'>empty</p>"
    columns_html += """
  <div class="col">
    <h2>%s <span class="count">%d</span></h2>
    <div class="sub">%s</div>
    %s
  </div>""" % (esc(label), sum(1 for s in steps if s["column"] == key), esc(sub), cards)

blockers_html = ""
if blockers:
    blockers_html = "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(b) for b in blockers)
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
  .desc {{ margin: .35rem 0; opacity: .88; }}
  .status {{ font-size: .8rem; opacity: .65; margin-top: .3rem; }}
  details {{ margin-top: .4rem; font-size: .9rem; }}
  summary {{ cursor: pointer; opacity: .7; }}
  details ul {{ margin: .3rem 0; padding-left: 1.1rem; }}
  details li {{ margin: .25rem 0; }}
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
