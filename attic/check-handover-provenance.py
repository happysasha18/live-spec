#!/usr/bin/env python3
"""check-handover-provenance.py — a session handover names where it was read from (SPEC INV-302, gate ab).

THE LAW it enforces, Requirement 303 (R303.10..R303.18). A session that lived the work is a poor
reader of its own record: on 2026-07-28 a session wrote its handover from memory and named a question
as waiting for the owner, though the owner had answered it earlier that same day. So the handover is
written by a fresh agent session reading a session extract — the person's own turns, pulled out of the
transcript by `scripts/session-extract.py` — and the session that lived the work writes no handover of
its own.

WHY A PUSH GATE IS THIS STEP'S HOME. Of the three homes open to it, a push gate is the only one whose
subject exists: a session handover is a committed artifact a machine can read, and any quality a
machine can verify is held by a gate rather than by a session's attention (base rule 30). A session
hook cannot make an agent spawn a reader, and a rule in prose alone is a rule a busy session skips.

WHAT THIS GATE ACTUALLY ENFORCES, and what it does not. It enforces the SHAPE of the provenance: that
a handover names the transcript it was read from, the extract file it was written from, and the agent
that wrote it. Whether the writing session was genuinely fresh is a process fact no gate sees, and it
stays with the session's discipline — the same boundary the clean-context review record draws
(INV-237). The opening step has no committed artifact at all, so no gate holds it either; it is a
discipline the seat holds, for the reason Requirement 93 already gives for the resume-side re-read.

THE SUBJECT. A session handover is a file under `docs/handovers/` whose name ends in `-handover.md`.
That directory also holds drafts and notes, which this gate leaves alone. A file naming no date is
read as in scope, since a record that does not date itself cannot claim to predate the law.

THE COUNTING START. The law lands on 2026-07-28, and the one handover already in the tree carries that
date — it is the very record whose defect paid for this gate. So the counting start is the day after,
and history before the law reds nothing, the same carry `guardrails/check-worker-restore.py` makes.

THE VACUITY GUARD (INV-218). A directory holding no session handover at all reds rather than passing
over nothing, and the emptiness is read over the DECLARED handovers: a directory of drafts alone
would otherwise pass green over no subject. A directory holding only pre-law handovers is a different
case: the gate stands down BY NAME and says what it read nothing of.

Usage:
  check-handover-provenance.py [--dir DIR] [--start YYYY-MM-DD]
Exit 0 when every in-scope handover names all three (printing the reach line, INV-269); exit 1 naming
each handover that does not, or an empty directory.
Stdlib only.
"""
import argparse
import os
import re
import sys

CHECK = "check-handover-provenance"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_DIR = os.path.join(REPO_ROOT, "docs", "handovers")
COUNTING_START = "2026-07-29"

HANDOVER_SUFFIX = "-handover.md"
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

# The three lines a handover owes, each read for a label and real text after it.
WANTED = (
    ("transcript", re.compile(r"^\s*transcript\s*:\s*\S", re.IGNORECASE | re.MULTILINE)),
    ("extract", re.compile(r"^\s*extract\s*:\s*\S", re.IGNORECASE | re.MULTILINE)),
    ("written by", re.compile(r"^\s*written by\s*:\s*\S", re.IGNORECASE | re.MULTILINE)),
)


def handovers(directory):
    """Every file in the directory, and the subset that declares itself a session handover."""
    everything = sorted(f for f in os.listdir(directory)
                        if os.path.isfile(os.path.join(directory, f)))
    declared = [f for f in everything if f.endswith(HANDOVER_SUFFIX)]
    return everything, declared


def in_scope(name, start):
    """A handover the law reaches: dated on or after the counting start, or carrying no date."""
    found = DATE_RE.match(name)
    if not found:
        return True
    return found.group(1) >= start


def missing_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    return [label for label, pattern in WANTED if not pattern.search(text)]


def main(argv):
    ap = argparse.ArgumentParser(prog=CHECK, add_help=True)
    ap.add_argument("--dir", default=DEFAULT_DIR, help="the handover directory to read")
    ap.add_argument("--start", default=COUNTING_START, help="the counting start, YYYY-MM-DD")
    args = ap.parse_args(argv[1:])

    if not os.path.isdir(args.dir):
        print("%s: cannot read %s — the gate stands on the handover directory." % (CHECK, args.dir))
        return 1

    everything, declared = handovers(args.dir)
    if not declared:
        # The subject is the declared session handovers, never the directory's whole contents: a
        # directory of drafts alone would otherwise pass green over no subject at all.
        print("%s: %s holds no session handover at all, over %d file(s) — the gate refuses rather "
              "than passing over nothing." % (CHECK, args.dir, len(everything)))
        return 1

    scoped = [f for f in declared if in_scope(f, args.start)]
    if not scoped:
        print("%s: OK — stands down by name: %d file(s) under %s, %d of them session handovers, "
              "and every one predates the counting start %s, so this run read nothing of the law."
              % (CHECK, len(everything), args.dir, len(declared), args.start))
        return 0

    problems = []
    for name in scoped:
        gaps = missing_lines(os.path.join(args.dir, name))
        if gaps:
            problems.append((name, gaps))

    if problems:
        print("%s: %d session handover(s) name no reader:" % (CHECK, len(problems)))
        for name, gaps in problems:
            print("  - %s carries no %s line" % (name, ", no ".join(gaps)))
        print("  a handover is written by a fresh agent from a session extract, and it says so in "
              "three lines: transcript, extract, written by.")
        return 1

    print("%s: OK — reach: dir=%s; %d file(s) read, %d session handovers, %d in scope from %s, "
          "%d predating it; every in-scope handover names its transcript, its extract and its writer"
          % (CHECK, args.dir, len(everything), len(declared), len(scoped), args.start,
             len(declared) - len(scoped)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
