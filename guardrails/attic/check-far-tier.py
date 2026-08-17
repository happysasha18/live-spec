#!/usr/bin/env python3
"""check-far-tier.py — the far tier stands down by name, and it surfaces itself rarely.

PARKED 2026-08-18 in `guardrails/attic/`, with `far-tier-fixtures/` beside it. It stands in no push
chain and no CI step, and the only reports it has ever read are those fixtures: no real what's-left
report has ever been handed to it, so it has caught nothing. Its suite still drives it here.

Two report-shape laws, checked here so the suite can red them on a fixture. This checker is
NOT in the pre-push chain: the status report and the feature map are chat surfaces the agent
speaks at runtime, so no committed report file exists for a push gate to scan (a chat surface
is not machine-gatable, SPEC INV-83's sibling). The tests drive this checker over fixtures to
red-prove the shape, and the real ROADMAP's far rows are asserted by the test directly.

Three modes:

  --report FILE   SPEC INV-222 (ROADMAP 382). The runnable "what's-left" region of a report
                  must not name a far-tier row, and a report that enumerates runnable work must
                  stand the far tier down by name (an offer on request). Markers:
                    <!-- far-tier:members 411,381 -->     the far-tier row numbers
                    <!-- far-tier:runnable --> ... <!-- /far-tier:runnable -->   the runnable region
                    <!-- far-tier:standdown -->           the line that stands the tier down
                  A far member named inside the runnable region reds. A runnable region with no
                  stand-down line reds. A report standing the tier down and offering on request passes.

  --window FILE   SPEC INV-223 (ROADMAP 403). The far tier surfaces itself at most once per
                  cadence window. Markers:
                    <!-- far-tier:cadence-days 14 -->     the window in days (a settings default)
                    <!-- far-tier:last-surfaced 2026-07-04 -->   when the tier last self-surfaced
                    <!-- far-tier:offer 2026-07-10 -->    the date this report offers the tier
                  An offer whose date falls inside the window after the last surfacing reds
                  (a second offer inside the same window). A first offer once the window has
                  passed, or with no prior marker, passes.

  --vocab FILE    SPEC INV-222. The far-versus-deferred distinction, made mechanical. A far row
                  carries no revisit trigger and nothing re-scans it; a deferred row carries one
                  the queue-take re-scans every time [INV-129]. Lines shaped:
                    far-row: 411 | trigger: none
                    deferred-row: 300 | trigger: when-the-campaign-ships
                  A far row carrying a trigger reds (it is a deferred row wearing the wrong token).
                  A deferred row carrying no trigger reds (INV-129 has nothing to re-scan).
"""
import argparse
import datetime
import re
import sys


def _runnable_region(text):
    m = re.search(r"<!--\s*far-tier:runnable\s*-->(.*?)<!--\s*/far-tier:runnable\s*-->", text, re.S)
    return m.group(1) if m else None


def _members(text):
    m = re.search(r"<!--\s*far-tier:members\s+([0-9,\s]+)-->", text)
    if not m:
        return []
    return [n.strip() for n in m.group(1).split(",") if n.strip()]


def check_report(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    violations = []
    members = _members(text)
    region = _runnable_region(text)
    if region is not None:
        for n in members:
            if re.search(r"(?<![0-9])%s(?![0-9])" % re.escape(n), region):
                violations.append(
                    "INV-222: far-tier row %s named inside the runnable what's-left region" % n
                )
        has_standdown = (
            "far-tier:standdown" in text
            or ("far backlog" in text.lower() and "on request" in text.lower())
        )
        if not has_standdown:
            violations.append(
                "INV-222: the report enumerates runnable work but stands the far tier down nowhere "
                "(no stand-down line, no offer on request)"
            )
    return violations


def check_window(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    violations = []
    mc = re.search(r"<!--\s*far-tier:cadence-days\s+(\d+)\s*-->", text)
    cadence = int(mc.group(1)) if mc else 14
    ml = re.search(r"<!--\s*far-tier:last-surfaced\s+(\d{4}-\d{2}-\d{2})\s*-->", text)
    last = datetime.date.fromisoformat(ml.group(1)) if ml else None
    offers = re.findall(r"<!--\s*far-tier:offer\s+(\d{4}-\d{2}-\d{2})\s*-->", text)
    if last is not None:
        for od in offers:
            offer = datetime.date.fromisoformat(od)
            gap = (offer - last).days
            if 0 <= gap < cadence:
                violations.append(
                    "INV-223: a second far-tier offer on %s falls %d days after the last surfacing "
                    "on %s, inside the %d-day window" % (od, gap, last.isoformat(), cadence)
                )
    return violations


def check_vocab(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    violations = []
    seen = False
    for line in lines:
        m = re.match(r"\s*(far-row|deferred-row):\s*(\S+)\s*\|\s*trigger:\s*(.+?)\s*$", line)
        if not m:
            continue
        seen = True
        kind, row, trigger = m.group(1), m.group(2), m.group(3).strip().lower()
        has_trigger = trigger not in ("none", "-", "")
        if kind == "far-row" and has_trigger:
            violations.append(
                "INV-222: far row %s carries a revisit trigger (%s); a far row carries none — "
                "a triggered row is deferred" % (row, trigger)
            )
        if kind == "deferred-row" and not has_trigger:
            violations.append(
                "INV-222/INV-129: deferred row %s carries no revisit trigger; the queue-take "
                "re-scan has nothing to read" % row
            )
    if not seen:
        # A vacuous input is the defect, never a silent pass (SPEC INV-218).
        violations.append("INV-222: --vocab input carried no far-row/deferred-row lines")
    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report")
    ap.add_argument("--window")
    ap.add_argument("--vocab")
    args = ap.parse_args()
    violations = []
    if args.report:
        violations += check_report(args.report)
    if args.window:
        violations += check_window(args.window)
    if args.vocab:
        violations += check_vocab(args.vocab)
    if not (args.report or args.window or args.vocab):
        ap.error("name one of --report / --window / --vocab")
    if violations:
        for v in violations:
            print("FAIL (far-tier): %s" % v)
        return 1
    print("OK (far-tier): the far tier stands down by name and surfaces within its window.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
