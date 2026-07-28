#!/usr/bin/env python3
"""session-extract.py — one session's human turns, compact enough for a cheap reader (SPEC INV-302).

THE RULE IT SERVES (Requirement 303, R303.1..R303.9). A session that lived the work reads its own
record badly: on 2026-07-28 a session wrote its handover from memory and named a question as waiting
for the owner, though the owner had answered it earlier that same day. So a session's record is read
at both ends by a fresh agent — one that did not live the work — and this script writes what that
agent reads: the person's own turns from one transcript, each with its timestamp and its text.

WHY IT IS WORTH A SCRIPT. The point of the output is SIZE. A raw transcript runs to megabytes and
most of its bulk is machine traffic, while the person's own words fit in kilobytes. A cheap model
reads the kilobytes.

THE FOUR TRAPS, each checked against the real files on 2026-07-28:

  1. The wrong directory looks right. The sibling directory `-Users-sashaabramovich-live-spec` holds
     one-shot machine calls and no human turns at all. The real conversations sit in the top-level
     directory named for the home, which is what --root defaults to.
  2. The working directory changes mid-file. A session's opening human turns carry the home as their
     `cwd`, and the repository path appears only after the first tool call inside the repository. So
     a file is taken WHOLE when any line in it names the repository path, and every human turn in
     that file is then read; a line-by-line filter would drop the turns that open a session.
  3. A `user` line is usually a machine. One live transcript held 8 human turns against 34 machine
     lines of the same type. A machine line carries a `toolUseResult` key, or a content list holding
     only tool results.
  4. The harness writes in the human's slot. Some turns are wrappers the harness generated. A turn
     whose whole text is such a wrapper is dropped, and a wrapper riding beside real words is
     stripped out of the turn that keeps them.

WHERE THE OUTPUT GOES. A transcript holds private conversation, so the extract is written to a
scratch directory and never into the repository. The one thing that legitimately crosses is a
decision entry in DECISIONS.md, which owes its evidence in the person's own words. The conventional
name is `session-extract-<session>.md`, and this repository's ignore rules carry that pattern, so a
run that names its output here leaves an ignored file rather than a committed one.

Usage:
  session-extract.py --out FILE [--root DIR] [--repo PATH]
  session-extract.py --out FILE --transcript FILE
  session-extract.py --list [--root DIR] [--repo PATH]
Exit 0 once the extract is written (or the candidates are listed); exit 1 when no transcript names
the repository, when a named transcript cannot be read, or when a taken transcript holds no human
turn; exit 2 on a usage error.
Stdlib only.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

CHECK = "session-extract"

# The harness writes these wrappers into the human's slot. A turn that is only wrappers is dropped;
# a wrapper beside real words is cut out and the words are kept.
WRAPPERS = ("local-command-caveat", "command-name", "command-message", "command-args",
            "system-reminder")
WRAPPER_RE = re.compile(
    r"<(%s)\b[^>]*>.*?</\1>|<(?:%s)\b[^>]*/?>" % ("|".join(WRAPPERS), "|".join(WRAPPERS)),
    re.DOTALL)


def default_root():
    """The transcript home for this machine's projects, named for the home directory."""
    home = os.path.expanduser("~")
    encoded = "-" + home.strip("/").replace("/", "-")
    return os.path.join(home, ".claude", "projects", encoded)


def default_repo():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def local_stamp(raw):
    """A recorded timestamp as a plain local date and time, the clock the person reads."""
    if not raw:
        return "unstamped"
    text = raw.replace("Z", "+00:00")
    try:
        when = datetime.datetime.fromisoformat(text)
    except ValueError:
        return raw
    if when.tzinfo is not None:
        when = when.astimezone()
    return when.strftime("%Y-%m-%d %H:%M")


def turn_text(message):
    """The person's own words in one line's message, or an empty string for a machine's line."""
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(p for p in parts if p)


def strip_wrappers(text):
    return WRAPPER_RE.sub(" ", text).strip()


def human_turns(path):
    """Every human turn in one transcript: a list of (stamp, text), in the order they were said."""
    turns = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                line = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(line, dict) or line.get("type") != "user":
                continue
            if "toolUseResult" in line:
                continue
            if line.get("isSidechain") or line.get("isMeta"):
                continue
            text = strip_wrappers(turn_text(line.get("message")))
            if not text:
                continue
            turns.append((local_stamp(line.get("timestamp")), text))
    return turns


def candidates(root, repo):
    """Every transcript file in root that names the repository path on any line, newest last."""
    found = []
    for path in glob.glob(os.path.join(root, "*.jsonl")):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                # Read line by line: a transcript runs to megabytes, and the first line naming the
                # repository settles the file.
                if any(repo in line for line in f):
                    found.append(path)
        except OSError:
            continue
    return sorted(found, key=os.path.getmtime)


def write_extract(path, transcript, turns):
    name = os.path.splitext(os.path.basename(transcript))[0]
    lines = ["# Session extract — %s" % name, ""]
    lines.append("Every turn below is the person's own, in the order it was said, on the local clock.")
    lines.append("")
    lines.append("transcript: %s" % transcript)
    lines.append("turns: %d" % len(turns))
    if turns:
        lines.append("span: %s to %s" % (turns[0][0], turns[-1][0]))
    lines.append("")
    for stamp, text in turns:
        lines.append("## [%s]" % stamp)
        lines.append("")
        lines.append(text)
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main(argv):
    ap = argparse.ArgumentParser(prog=CHECK, add_help=True)
    ap.add_argument("--root", default=None, help="the transcript directory to read")
    ap.add_argument("--repo", default=None, help="the repository path a transcript must name")
    ap.add_argument("--transcript", default=None, help="one transcript file, named outright")
    ap.add_argument("--out", default=None, help="where the extract is written")
    ap.add_argument("--list", action="store_true", help="list the transcripts that name the repository")
    args = ap.parse_args(argv[1:])

    root = args.root or default_root()
    repo = args.repo or default_repo()

    if not args.list and not args.out:
        print("%s: usage: %s --out FILE [--root DIR] [--repo PATH]" % (CHECK, CHECK))
        return 2

    if args.transcript:
        if not os.path.isfile(args.transcript):
            print("%s: cannot read %s — the run stands on the transcript file." % (CHECK, args.transcript))
            return 1
        taken = args.transcript
    else:
        if not os.path.isdir(root):
            print("%s: no transcript directory at %s — nothing was read." % (CHECK, root))
            return 1
        found = candidates(root, repo)
        if args.list:
            for path in found:
                print(path)
            print("%s: %d transcript(s) under %s name %s" % (CHECK, len(found), root, repo))
            return 0
        if not found:
            print("%s: no transcript under %s names %s — nothing was read." % (CHECK, root, repo))
            return 1
        taken = found[-1]

    turns = human_turns(taken)
    if not turns:
        print("%s: %s holds no human turn — no extract was written." % (CHECK, taken))
        return 1

    write_extract(args.out, taken, turns)
    print("%s: OK — reach: transcript=%s (%d bytes); human turns=%d; extract=%s (%d bytes)"
          % (CHECK, taken, os.path.getsize(taken), len(turns), args.out, os.path.getsize(args.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
