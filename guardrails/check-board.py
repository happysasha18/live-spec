#!/usr/bin/env python3
"""check-board.py — the waiting list keeps what waits for his eyes, and nothing on it is ever lost
(SPEC INV-206, ROADMAP 408).

Chat is a display and it scrolls, so a question parked for the person and an answer he never saw both
evaporate. One small file at the host root — the board, `WAITING.md` — holds them, and chat renders it.
An item clears on his acknowledgement alone; it is never auto-expired, because expiring an item he never
read is a silent loss (his 2026-07-17 ~15:57 correction, which caught the pack breaking its own base
rule 10). The bound governs only what is SHOWN: the board shows at most CAP items in front of him, and
when a new item arrives to a full shown set the oldest shown item demotes to the list below — whole and
alive, not deleted. The list itself is unbounded, and so is the attic a cleared or superseded item moves
to with a manifest line (base rule 10).

The board's regions are keyed by machine markers, so a human's section wording is free to change:

  <!-- board:shown -->      the shown set — what his status answer prints in front of him (cap CAP)
  <!-- board:list -->       the rest of the list — alive, opens on request, no cap
  <!-- board:attic -->      cleared or superseded items, each on a manifest line (nothing lost)
  <!-- board:demotions -->  the record that an item moved from the shown set into the list

An item is a line naming its id (`w-<n>`) and its status; an OPEN item is alive. A demotion record names
the id that moved. This gate reds three violations:

  (a) a CLOSING report that omits a still-open item on the board — a report meant to account for what
      waits cannot leave an alive item unnamed (checked only when a report is given);
  (b) a DEMOTION with no matching line — an id recorded as demoted from the shown set that is accounted
      for nowhere on the board (not alive on the list, not on an attic manifest line): the silent loss
      the correction forbids;
  (c) an OVER-CAP shown set — more than CAP items shown at once, when the design demotes the oldest
      instead.
  (d) a PARKED QUESTION with no default (SPEC INV-229, ROADMAP 409) — a board item marked as a parked
      question (a `[[park]]` tag) that records no default (a `default:` note). When the pack parks a
      question for the person it carries the recommended default the work ALREADY took, so the work
      proceeds on the recommendation without stalling (INV-4 — the lane never parks on a proposal). A
      parked question with no default is a stalled question wearing a parked question's clothes.

A genuine board passes quiet. Honest boundary: this reads the board's structure, not the meaning of a
free line — a report that names an id while burying it stays the author's own to write straight. It is a
structural scan, kin of check-touchpoint-kind.py and check-cleanup-notice.sh.

Usage:
  check-board.py                              push mode: validate the repo's real WAITING.md (b and c).
  check-board.py --board FILE                 validate one board file (b and c).
  check-board.py --board FILE --report FILE   also check the closing report omits no open item (a).
"""
import argparse
import os
import re
import sys

# The shown set's bound: a thirteenth item demotes the oldest shown into the list.
#
# No incident or source behind the 12 — an engineering default, not a policy decision. The
# 2026-08-07 census (docs/audits/2026-08-07-number-census.md, row 1) found no trace, and the commit
# that introduced it (607d40a, 2026-07-17) states the value without a reason. It is closer to a
# display width than to a bar: nothing is lost when it is crossed, because the oldest shown item
# demotes into the list whole and alive and the list is unbounded (SPEC INV-206). What the number
# governs is only how much of the board a person meets at once. Duplicated in PRODUCT_SPEC.md and
# tests/test_board.py, so a change here is a three-file change.
CAP = 12

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BOARD = os.path.join(REPO_ROOT, "WAITING.md")

MARKER = re.compile(r"<!--\s*board:(shown|list|attic|demotions)\s*-->")
ITEM = re.compile(r"^\s*[-*]\s*(w-\d+)\b", re.IGNORECASE)
STATUS = re.compile(r"\bOPEN\b")
ID = re.compile(r"w-\d+", re.IGNORECASE)
PARK = re.compile(r"\[\[park\]\]")            # a board item marked as a parked question (INV-229)
DEFAULT = re.compile(r"\bdefault:", re.IGNORECASE)  # the recommended default the parked question carries


def regions(text):
    """Split a board's text into {region_name: [lines]} keyed by the <!-- board:X --> markers.

    Lines before the first marker belong to no region and are dropped.
    """
    out = {"shown": [], "list": [], "attic": [], "demotions": []}
    current = None
    for line in text.splitlines():
        m = MARKER.search(line)
        if m:
            current = m.group(1)
            continue
        if current is not None:
            out[current].append(line)
    return out


def open_ids(lines):
    """The ids of OPEN (alive) items in a region's lines, lowercased, in order."""
    ids = []
    for line in lines:
        m = ITEM.match(line)
        if m and STATUS.search(line):
            ids.append(m.group(1).lower())
    return ids


def all_ids(lines):
    """Every id mentioned in a region's lines (a manifest or demotion line has no OPEN status)."""
    ids = []
    for line in lines:
        m = ITEM.match(line)
        if m:
            ids.append(m.group(1).lower())
    return ids


def check_board(board_text, report_text=None):
    """Return a list of violation strings for one board, optionally against one closing report."""
    reg = regions(board_text)
    shown = open_ids(reg["shown"])
    listed = open_ids(reg["list"])
    alive = shown + listed
    accounted = set(alive) | set(all_ids(reg["attic"]))
    demoted = all_ids(reg["demotions"])

    violations = []

    # (c) over-cap shown set.
    if len(shown) > CAP:
        violations.append(
            "the shown set holds %d items (cap %d) — the oldest shown demotes into the list instead "
            "of a thirteenth being shown" % (len(shown), CAP))

    # (d) a parked question with no default (INV-229) — an item marked [[park]] carrying no `default:`.
    for line in reg["shown"] + reg["list"]:
        if PARK.search(line) and not DEFAULT.search(line):
            m = ITEM.match(line)
            wid = m.group(1).lower() if m else "a parked item"
            violations.append(
                "INV-229: %s is a parked question ([[park]]) carrying no default — a question parked "
                "for the person carries the recommended default the work already took, so the work "
                "proceeds without stalling (INV-4); a parked question with no default is a stalled "
                "question wearing a parked question's clothes" % wid)

    # (b) a demotion with no matching line anywhere on the board = a silent loss.
    for wid in demoted:
        if wid not in accounted:
            violations.append(
                "%s is recorded as demoted from the shown set but is accounted for nowhere on the "
                "board (not alive on the list, not on an attic manifest line) — a demoted item must "
                "move into the list whole and alive, never vanish" % wid)

    # (a) a closing report that omits a still-open item on the board.
    if report_text is not None:
        named = {m.group(0).lower() for m in ID.finditer(report_text)}
        for wid in alive:
            if wid not in named:
                violations.append(
                    "the closing report omits %s, which is still open on the board — a report that "
                    "accounts for what waits names every alive item" % wid)

    return violations


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", default=None)
    ap.add_argument("--report", default=None)
    args = ap.parse_args(argv)

    board_path = args.board or DEFAULT_BOARD
    if not os.path.exists(board_path):
        if args.board is None:
            # push mode with no board yet: the surface is not built, the gate stands down by name.
            print("OK (board): no WAITING.md in this tree — the waiting list is not built here, the "
                  "gate stands down by name (INV-206).")
            return 0
        print("FAIL (board): the waiting-list file %s is missing — there is nothing here to check "
              "(SPEC INV-206)." % board_path)
        return 1

    report_text = read(args.report) if args.report else None
    violations = check_board(read(board_path), report_text)

    if violations:
        print("FAIL (board): the waiting list would lose or misreport something still waiting on the "
              "product owner's answer (SPEC INV-206):")
        for v in violations:
            print("  " + v)
        print("  An item only clears once that person has actually seen and acknowledged it — nothing "
              "else should make it disappear.")
        print("  Fix: ask your agent to keep every demoted item whole and alive in the list, keep the "
              "shown set at or under %d items, name every still-open item in a closing report, and give "
              "any parked question ([[park]]) the default the work already took (a `default:` note). "
              "The list lives at WAITING.md." % CAP)
        return 1

    print("OK (board): the waiting list keeps every alive item, demotes nothing into the void, and "
          "shows at most %d at once (INV-206)." % CAP)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
