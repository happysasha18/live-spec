#!/usr/bin/env python3
"""check-touchpoint-kind.py — every point of contact with the person has a kind, and the kind decides
what may be said there (SPEC INV-205, ROADMAP 413).

Every touchpoint declares its kind in the manifest `guardrails/touchpoints.json`. A touchpoint is
SYNCHRONOUS when the person is present and the work waits on him (a live question, a decision page he is
looking at now), and ASYNCHRONOUS when he reads on his own clock while the work rolls (a status line,
the resume file, an inbox note, the waiting list he opens on request). The kind licenses the traffic:

  * an INTERRUPTION is afforded only on a synchronous point — interrupting a person who is absent is a
    loss, not a message;
  * a TEACHING line — one that introduces a capability he has not met — is afforded only where the
    person OPENS the point himself (any synchronous point, or an asynchronous point he opens on request),
    so the product teaches itself through use on a surface he chose to open;
  * WAITING traffic is afforded everywhere.

This gate reds a surface that speaks in a kind its touchpoint lacks: an interruption raised from an
asynchronous point, or a teaching line on a point the person did not open. A genuine touchpoint passes
quiet.

Usage:
  check-touchpoint-kind.py                      push mode: validate the manifest, then scan every
                                                declared surface that exists on disk (default, the gate).
  check-touchpoint-kind.py [--manifest FILE] FILE...
                                                scan one or more surface files, each against the
                                                touchpoint it declares (a `TOUCHPOINT-KIND: <name>`
                                                line) — used by the guardrail's own test over its
                                                fixtures.

A surface names its touchpoint with a `TOUCHPOINT-KIND: <name>` line and tags a line's traffic with an
`[[interrupt]]`, `[[teach]]`, or `[[wait]]` marker; an untagged line is waiting traffic by default.

Honest boundary: this reads a declared marker, not the meaning of an arbitrary line — a surface that
interrupts through wording the markers cannot read stays the author's own to declare. It is the
structural net that keeps the frame checkable, kin of check-cleanup-notice.sh and the muted-launch net.
"""
import argparse
import json
import os
import re
import sys

MARKER = "TOUCHPOINT-KIND:"
TRAFFIC = {
    "interrupt": re.compile(r"\[\[interrupt\]\]"),
    "teach": re.compile(r"\[\[teach\]\]"),
    "wait": re.compile(r"\[\[wait\]\]"),
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(REPO_ROOT, "guardrails", "touchpoints.json")


def load_manifest(path):
    """Read and validate the manifest. Returns {name: entry}. Raises ValueError on a malformed entry."""
    with open(path) as f:
        data = json.load(f)
    entries = data["touchpoints"] if isinstance(data, dict) else data
    by_name = {}
    for e in entries:
        name = e.get("name")
        if not name:
            raise ValueError("a touchpoint entry has no name: %r" % e)
        if name in by_name:
            raise ValueError("duplicate touchpoint name %r" % name)
        if e.get("kind") not in ("synchronous", "asynchronous"):
            raise ValueError("touchpoint %r has an invalid kind %r "
                             "(must be synchronous or asynchronous)" % (name, e.get("kind")))
        if e.get("opened_by") not in ("person", "agent"):
            raise ValueError("touchpoint %r has an invalid opened_by %r "
                             "(must be person or agent)" % (name, e.get("opened_by")))
        by_name[name] = e
    return by_name


def afforded(entry):
    """The set of traffic kinds a touchpoint's kind licenses.

    An interruption rides only a synchronous point; a teaching line rides only a point the person opens
    himself (a synchronous point, or an asynchronous point he opens on request); waiting rides every
    point.
    """
    kinds = {"wait"}
    if entry["kind"] == "synchronous":
        kinds.add("interrupt")
    if entry["kind"] == "synchronous" or entry["opened_by"] == "person":
        kinds.add("teach")
    return kinds


def declared_touchpoint(text):
    """The touchpoint name a surface declares via its `TOUCHPOINT-KIND: <name>` line, or None."""
    m = re.search(re.escape(MARKER) + r"\s*(\S+)", text)
    return m.group(1) if m else None


def scan_surface(path, entry):
    """Return a list of violation strings for one surface file read against its touchpoint entry."""
    allowed = afforded(entry)
    violations = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            for kind, pat in TRAFFIC.items():
                if pat.search(line) and kind not in allowed:
                    why = ("an interruption belongs on a synchronous point"
                           if kind == "interrupt"
                           else "a teaching line belongs on a point the person opens himself")
                    violations.append(
                        "%s:%d speaks a %r on touchpoint %r (%s, opened by %s) — %s"
                        % (path, n, kind, entry["name"], entry["kind"], entry["opened_by"], why))
    return violations


def scan_by_declaration(path, by_name):
    """Scan a surface that self-declares its touchpoint. Returns (violations, note)."""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    name = declared_touchpoint(text)
    if name is None:
        return [], "no TOUCHPOINT-KIND declaration — not a touchpoint surface, skipped"
    entry = by_name.get(name)
    if entry is None:
        return (["%s declares touchpoint %r, which the manifest does not name" % (path, name)],
                None)
    return scan_surface(path, entry), None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("files", nargs="*")
    args = ap.parse_args(argv)

    try:
        by_name = load_manifest(args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("FAIL (touchpoint-kind): the manifest %s is unreadable or malformed (SPEC INV-205):"
              % args.manifest)
        print("  %s" % e)
        return 1

    violations = []

    if args.files:
        # explicit scan: each file against the touchpoint it self-declares.
        for path in args.files:
            v, _ = scan_by_declaration(path, by_name)
            violations.extend(v)
    else:
        # push mode: scan every declared surface that exists on disk. A [target] touchpoint whose
        # surface is not built yet (null) is skipped — the frame is stated, the surface pending.
        for name, entry in by_name.items():
            surface = entry.get("surface")
            if not surface:
                continue
            path = surface if os.path.isabs(surface) else os.path.join(REPO_ROOT, surface)
            if not os.path.exists(path):
                continue
            violations.extend(scan_surface(path, entry))

    if violations:
        print("FAIL (touchpoint-kind): a message in the product is written for a moment it isn't shown")
        print("  at (SPEC INV-205) — an urgent interruption placed somewhere the person won't see it in")
        print("  time, or a lesson dropped where they can't take it in:")
        for v in violations:
            print("  " + v)
        print("  Fix: ask your agent to move the message to a moment that fits it, or drop it if it")
        print("  isn't needed there.")
        return 1

    print("OK (touchpoint-kind): the manifest is well-formed and every declared surface speaks only "
          "the kinds its touchpoint affords (INV-205).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
