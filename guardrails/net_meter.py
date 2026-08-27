#!/usr/bin/env python3
"""net_meter.py — every net keeps its own liveness numbers (SPEC INV-202, ROADMAP row 391).

A net is a hook or a guard that watches for something. The law: every net records its own two numbers,
how often it RAN and how often it FIRED, and a silent net is read rather than trusted. A net that never
fires is a fact about itself with two readings — the defect is gone and the net is dead weight to retire,
or the net is broken and its trigger sits where the work does not pass. Two numbers tell them apart, and
no net keeps them on its own.

This is the pack-side, every-adopting-host arm of the personal layer's `~/.claude/hooks/hook-meter.py`.
It has two faces, sharing one log:

  net_meter.py --wrap <net-name> <cmd> [args...]   run the net, pass stdin through untouched, re-emit its
                                                   stdout, exit with its own code, and record one JSON
                                                   line of the outcome. A transparent instrument: a
                                                   failure to log is swallowed, since an instrument must
                                                   never break the thing it measures.

  net_meter.py --report [--roster FILE] [--window N]
                                                   read the log against the declared roster of nets and
                                                   give the three readings per net. A roster net with ZERO
                                                   runs reds by name (its trigger sits where work never
                                                   passes). A net with runs at or over the declared window
                                                   and ZERO fires is SURFACED as a retirement candidate
                                                   whose retirement is the human's call — never auto-red,
                                                   never auto-retired. Everything firing reads as live.

The log is one JSON line per invocation, e.g.:

    {"net": "scissors-scan", "event": "Stop", "fired": true, "hits": 2}

Its home is `NET_METER_LOG` (default `.live-spec/net-meter.jsonl`). The roster — the set of nets the host
declares it runs — is what lets a zero-run net be named at all, since a net that never runs writes no line.
The window is the host's declared number of runs a net must reach before its silence reads as retirement.

Kin of ROADMAP row 384 (a check that looked at nothing is not a pass — a net that never ran is that same
check, measured over time rather than over an input set) and INV-41 (the number names its watcher).
"""

import collections
import json
import os
import subprocess
import sys

DEFAULT_LOG = os.environ.get("NET_METER_LOG", ".live-spec/net-meter.jsonl")
# Runs a net must reach before its silence reads as a retirement candidate. [default].
#
# Truth about the override, in the shape check-runaway-child.py's own note uses: this is tunable per
# RUN, not per host — `--window N` on the command line is the only override, and no env var or config
# file is read for it. No incident or source behind the 20 (the 2026-08-07 census, row 18, found no
# trace). It judges no work and retires nothing: a net over the window with zero fires is only
# SURFACED for the owner's word, never auto-retired, which is what keeps a wrong value cheap.
DEFAULT_WINDOW = 20


class Report:
    """The reading of a log against a roster: the printed lines, the broken and silent net names, and the
    exit code the check carries (non-zero exactly when a net is broken)."""

    def __init__(self, lines, broken, retirement_candidates, live, exit_code):
        self.lines = lines
        self.broken = broken
        self.retirement_candidates = retirement_candidates
        self.live = live
        self.exit_code = exit_code


def classify(runs, fires, window=DEFAULT_WINDOW):
    """A net's two numbers give one of three readings. Returns (reading, broken, candidate).

    - zero runs                          -> broken: the trigger never fires, its condition sits where the
                                            work does not pass. Reds by name.
    - runs, zero fires, over the window  -> a retirement candidate, surfaced for the human's word.
    - anything firing (or too few runs)  -> live, or not yet enough runs to read.
    """
    if runs == 0:
        return ("broken — the trigger never fires", True, False)
    if fires > 0:
        return ("live", False, False)
    if runs >= window:
        return ("silent over %d runs — retirement candidate (the human's call)" % runs, False, True)
    return ("silent over %d runs — below the %d-run window, too few to read yet" % (runs, window), False, False)


def tally(records):
    """records -> (runs Counter, fires Counter), one line per net invocation."""
    runs = collections.Counter()
    fires = collections.Counter()
    for r in records:
        name = r.get("net", "?")
        runs[name] += 1
        if r.get("fired"):
            fires[name] += 1
    return runs, fires


def report(records, roster=None, window=DEFAULT_WINDOW):
    """Read the records against the declared roster and return a Report.

    A net named in the roster but absent from the log has zero runs and reds by name. A net in the log but
    not the roster is still read (its numbers are real) but never reds — only a declared net's absence is a
    broken trigger, since an undeclared net's silence may just mean the host never wired it here.
    """
    runs, fires = tally(records)
    roster = list(roster) if roster is not None else []
    names = sorted(set(roster) | set(runs))

    lines = ["%-28s %8s %8s   reading" % ("net", "runs", "fires")]
    broken, retirement_candidates, live = [], [], []
    for name in names:
        n, f = runs.get(name, 0), fires.get(name, 0)
        reading, is_broken, is_candidate = classify(n, f, window)
        # Only a DECLARED (roster) net's silence is actionable; an undeclared net is read, never judged.
        if name not in roster:
            is_broken = False
            is_candidate = False
        if is_broken:
            broken.append(name)
        elif is_candidate:
            retirement_candidates.append(name)
        elif f > 0:
            live.append(name)
        lines.append("%-28s %8d %8d   %s" % (name, n, f, reading))

    if broken:
        lines.append("")
        lines.append("BROKEN — zero-run nets red by name (their trigger sits where the work never passes):")
        for name in broken:
            lines.append("  %s" % name)
    if retirement_candidates:
        lines.append("")
        lines.append("RETIREMENT CANDIDATES over the %d-run window — the human's call, never auto-retired:"
                     % window)
        for name in retirement_candidates:
            lines.append("  %s" % name)

    exit_code = 1 if broken else 0
    return Report(lines, broken, retirement_candidates, live, exit_code)


def _read_log(log_path):
    records = []
    try:
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    return records


def _read_roster(roster_path):
    """The roster is one net name per line; blank lines and # comments are skipped."""
    names = []
    try:
        with open(roster_path, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    names.append(line)
    except OSError:
        pass
    return names


def _log_invocation(record, log_path):
    # transparent instrument: a failure to log never breaks the net it measures.
    try:
        d = os.path.dirname(log_path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _wrap(net_name, cmd, log_path):
    """Run the net transparently, record its outcome. A net FIRES when it signals it caught something:
    a non-zero exit (a guard that blocked) or a block-decision JSON on stdout (a Claude Code hook)."""
    payload = sys.stdin.read()
    proc = subprocess.run(cmd, input=payload, capture_output=True, text=True)
    out = proc.stdout

    fired = proc.returncode != 0
    hits = 0
    try:
        decision = json.loads(out) if out.strip() else {}
        if isinstance(decision, dict) and decision.get("decision") == "block":
            fired = True
            hits = decision.get("reason", "").count("  · ")
    except ValueError:
        pass

    event = "?"
    try:
        parsed = json.loads(payload) if payload.strip() else {}
        if isinstance(parsed, dict):
            event = parsed.get("hook_event_name", "?")
    except ValueError:
        pass

    _log_invocation({"net": net_name, "event": event, "fired": fired, "hits": hits}, log_path)

    sys.stdout.write(out)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def main(argv):
    args = argv[1:]
    log_path = os.environ.get("NET_METER_LOG", DEFAULT_LOG)

    if args and args[0] == "--wrap":
        if len(args) < 3:
            print("usage: net_meter.py --wrap <net-name> <cmd> [args...]", file=sys.stderr)
            return 2
        return _wrap(args[1], args[2:], log_path)

    if args and args[0] == "--report":
        roster_path = None
        window = DEFAULT_WINDOW
        rest = args[1:]
        i = 0
        while i < len(rest):
            if rest[i] == "--roster" and i + 1 < len(rest):
                roster_path = rest[i + 1]
                i += 2
            elif rest[i] == "--window" and i + 1 < len(rest):
                window = int(rest[i + 1])
                i += 2
            else:
                i += 1
        records = _read_log(log_path)
        roster = _read_roster(roster_path) if roster_path else None
        result = report(records, roster=roster, window=window)
        print("\n".join(result.lines))
        return result.exit_code

    print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
