#!/usr/bin/env python3
"""check-earned-message.py — the mechanical net for the earned message (SPEC INV-189).

Rule 31 / INV-189 states it: a message from one agent to another is born of the sender's
own work, and it names its birth in the message. The births are a closed set of two — the
sender is blocked by the receiver's zone as it stands, or the sender lived a fault in that
zone and carries the evidence it lived. A message that can name neither is never sent,
because curiosity, tidiness, and the thought that a neighbour might want to know each
describe a message the sender's own work does not need. Until now that was discipline
only, and discipline is what a long session spends first.

This gate is its mechanical arm. It reads the inbox as a folder of deposits, finds each
one an AGENT sent, and reds when such a deposit names neither birth. The red clears one of
two ways: the sender named the birth and the field was malformed, or the sweep declines the
message at the door and archives it. Declining at the door is the design's point — an
unearned message dies without a human reading it.

  Where the source lives. The filename holds it, and `inbox/README.md` is the home that
  prescribes the form (SPEC E-11):

    inbox/YYYY-MM-DD-from-<agent>-<slug>.md

  Every agent deposit in this folder's real corpus has carried that form since
  2026-07-10. The gate reads the `from-` prefix and leaves the source name undelimited,
  because a hyphenated source and a hyphenated slug share one separator and the trigger
  needs the prefix alone.

  What is owed, and by whom. The law binds agent-to-agent traffic. Two doors carry their
  own authority and owe nothing, so the README reserves a source word for each and the
  gate honours it ahead of every other read:

    from-owner-<slug>.md          the owner's own wish, which needs no warrant (INV-193)
    stranger-<kind>-<n>-<slug>.md a bridged Issue, whose door is the wish template (INV-146)

  The reserved word is the role. A shipped file names no person, and the language gate
  refuses one (INV-120).

  What an agent's message owes. A message names its birth, and the two births owe different
  things (INV-189). A message blocked by this zone names the work standing still; a message
  carrying a lived fault names the fault and the evidence the sender lived, and nothing of
  that sender's need stand still. A gate demanding blocked work of both would refuse the
  fault message, which is the message a neighbour most wants — the outside view this zone's
  own instruments cannot take. So either field names a birth, and the gate reds a deposit
  naming neither:

    Blocked: <the sender's own work standing until this is answered>   (INV-189, gated)
    Lived: <the fault hit here, and the evidence: what ran, what        (INV-189, gated)
            happened, how it showed>
    Need-by: <a date, or none>                                         (INV-192, reported)
    Id: <a stable identifier this message's reply can name>            (INV-192, reported)

  What a reply owes instead:

    Re: <the identifier of the message this answers>                   (INV-192)

  A reply owes no blocked work of its own: the message it discharges already named the
  blocked work that earned the exchange, and the reply names that message's identifier,
  which is what ties it to the named work (INV-192). So a deposit naming a message is
  read as a reply and passes.

  Need-by and Id are read and reported, and neither moves the exit code. INV-192 gives an
  expired need-by one road: the escalation surfaces in the sender's own status report as
  blocked work aged past its stated need-by, and the human reads that line. A receiver's
  pre-push gate is a different road, so redding a receiver's push for a sender's clock
  would stop work no law asked to stop. This gate's red belongs to INV-189, the law it is
  the arm of. Every field this gate's help names is a field this gate reads.

  A field inside a fenced code block is an example, and the gate reads past every fence
  before it reads any field — the source mark included, so a deposit quoting the agent
  card's block is not made agent traffic by the quote.

Known bounds, stated at their real width:

  1. The trigger is self-declared. A deposit announces itself as agent traffic by its
     filename's source, or by carrying the agent card's `From: <name> (agent)` line. A
     sender who names the file without the prefix and writes no marker is not read here at
     all. The filename is the narrowest available home for the declaration, since naming
     the file is an act the sender performs anyway, and a body field is one a sender simply
     omits — which is how the pre-2026-07-17 gate came to pass every real deposit in this
     folder. It stays a declaration, and a declaration can be withheld.
  2. The reply exemption is self-declared too. The gate reads that a `Re:` line names an
     identifier; no registry ties that identifier to a message this tree sent, so it cannot
     tell a discharged exchange from an invented one.
  3. The sentence's truth is beyond it. The gate reads that a `Blocked:` or a `Lived:` line
     exists and carries words past the placeholder set. Whether the named work stands still,
     and whether the named evidence was lived, is judgment, and it stays with the receiving
     sweep and the prover (INV-150's honest split). "Blocked: my work is blocked" passes
     this gate and fails the sweep's read: a tautology check reads meaning, and its
     false-positive risk outruns its catch.

  All three are the same shape: the gate nets a forgotten field, and the prover reads
  intent. That is the posture every gate here takes.

Usage:
  check-earned-message.py [PATH ...]
    PATH  inbox folders or single files; defaults to ./inbox when present.
Exit 0 when every agent message names one of its two births; exit 1 (with path:line:
findings) when one names neither. Stdlib only.
"""

import datetime
import os
import re
import sys

# A deposit's fields, as `inbox/README.md` prescribes them. Written wide on purpose: the
# separator may be an ascii or a fullwidth colon, the field may wear a list bullet or bold
# markers, and a mark the gate fails to read is a deposit that goes unread.
_SEP = r"[:：]"


def _field(names):
    return re.compile(
        r"^\s*(?:[-*+]\s*)?(?:\*\*)?(?:%s)(?:\*\*)?\s*%s\s*(.*)$" % (names, _SEP),
        re.IGNORECASE,
    )


# The agent card's source mark, which the gate accepts as a second declaration whatever the
# filename says, so a sender following the card's block is read (INV-184's card).
SOURCE_MARK = _field(r"From|Sender")
IS_AGENT = re.compile(r"[(\[{]\s*agent\s*[)\]}]", re.IGNORECASE)

# The named blocked work. A heading form and a field form both count — the deposit is
# prose a person may read, and the pack's own inbox files are written both ways.
BLOCKED_FIELD = _field(r"Blocked(?:\s+work)?")

# The lived fault, the message's second birth (INV-189, corrected 2026-07-17 when the first
# real deposit — a fault message from track-coach — was refused by a gate demanding blocked
# work of everything). A fault message owes the evidence it lived; nothing of the sender's
# need stand still for this birth.
LIVED_FIELD = _field(r"Lived(?:\s+fault)?|Fault")

# The reply's tie to the message it discharges (INV-192).
REPLY_FIELD = _field(r"Re")

# The lifecycle fields the gate reads and reports (INV-192).
NEEDBY_FIELD = _field(r"Need-by")
ID_FIELD = _field(r"Id")

# Words that fill a field without naming anything. A field is present and empty in spirit
# when it says only this; the sweep still reads the sentence, and this catches the
# placeholder a worker leaves behind (the stub-grep family, SPEC INV-46). The match is the
# WHOLE field, so a field that points at the prose AND names work stays legal.
PLACEHOLDER = re.compile(
    r"^\s*(?:tbd|todo|n/?a|none|-+|\.+|<[^>]*>|placeholder|fixme"
    r"|see\s+(?:above|below)|as\s+above)\s*\.?\s*$",
    re.IGNORECASE,
)

# The doors whose own authority stands: the owner's wish (INV-193) and the monitor's
# bridged Issue (INV-146). Matched against the filename with its date stripped.
RESERVED_SOURCE = re.compile(r"(?:from-)?(?:owner|stranger)(?:-|$)", re.IGNORECASE)

DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
ISO_DATE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\b")


def _uncode(lines):
    """The deposit's lines with every fenced block blanked, line numbers preserved.

    A field inside a fence is an example — the card's block quoted back, a template shown
    to a reader. Blanking keeps each surviving line at its own number, so a finding cites
    the line a person opens the file to.
    """
    out = []
    fence = None
    for line in lines:
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0]
                out.append("")
                continue
            out.append(line)
            continue
        if m and m.group(1)[0] == fence:
            fence = None
        out.append("")
    return out


def _source_stem(path):
    """The filename's source segment: the name with its extension and its date dropped."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return DATE_PREFIX.sub("", stem)


def _is_agent_message(path, lines):
    """True when a deposit declares itself agent-to-agent traffic.

    The filename is the source's one home, so it is read first. The agent card's body mark
    is accepted alongside it, which catches a deposit written to the card's block and named
    some other way. A reserved door wins over both: the owner's wish and a bridged Issue owe
    nothing, and a phrase in a stranger's quoted Issue body never turns their door into an
    agent's (INV-193, INV-146).
    """
    stem = _source_stem(path)
    if RESERVED_SOURCE.match(stem):
        return False
    if stem.lower().startswith("from-"):
        return True
    for i, line in enumerate(lines):
        m = SOURCE_MARK.match(line)
        if not m:
            continue
        # The mark may wrap: `From: live-spec` with `(agent)` on the line below.
        window = m.group(1) + " " + (lines[i + 1] if i + 1 < len(lines) else "")
        if IS_AGENT.search(window):
            return True
    return False


def _read_field(pattern, lines):
    """(lineno, text) of the first line matching this field, or None when it is absent."""
    for i, line in enumerate(lines, 1):
        m = pattern.match(line)
        if m:
            return i, m.group(1).strip()
    return None


def _names_something(found):
    """True when a field is present and carries words past the placeholder set."""
    return bool(found and found[1] and not PLACEHOLDER.match(found[1]))


def _lifecycle_notes(lines, today):
    """INV-192's fields, read and reported. None of these moves the exit code."""
    notes = []

    needby = _read_field(NEEDBY_FIELD, lines)
    if needby is None:
        notes.append("the message states no need-by; every message states one and reaches a "
                     "terminal state (SPEC INV-192)")
    else:
        m = ISO_DATE.match(needby[1])
        if m:
            try:
                stated = datetime.date.fromisoformat(m.group(1))
            except ValueError:
                stated = None
            if stated and stated < today:
                notes.append("the need-by %s has passed; the escalation surfaces in the SENDER's "
                             "own status report as blocked work aged past it (SPEC INV-192)"
                             % m.group(1))

    if not _names_something(_read_field(ID_FIELD, lines)):
        notes.append("the message carries no identifier for a reply to name (SPEC INV-192)")

    return notes


def scan_file(path, today=None):
    """(findings, notes) for one deposit — findings red the run, notes report."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except (UnicodeDecodeError, OSError):
        return [], []  # a deposit the gate cannot read as text is no message it can judge

    lines = _uncode(raw.split("\n"))
    if not _is_agent_message(path, lines):
        return [], []

    today = today or datetime.date.today()
    notes = _lifecycle_notes(lines, today)

    # A reply inherits its passage from the message it discharges, and owes no blocked work
    # of its own — the message it answers already named the work that earned the exchange.
    if _names_something(_read_field(REPLY_FIELD, lines)):
        return [], notes

    # The message names its birth, and the two births owe different things: a blocked message
    # owes the work standing still, a fault message owes the evidence it lived (INV-189).
    # Either field earns the passage; a deposit carrying both is legal and reads as both.
    blocked = _read_field(BLOCKED_FIELD, lines)
    lived = _read_field(LIVED_FIELD, lines)

    if blocked is None and lived is None:
        return [(1, "an agent message naming neither birth — it names no blocked work of its "
                    "own and no lived fault with its evidence, so it is not earned "
                    "(SPEC INV-189, base rule 31)")], notes

    for field, what in ((blocked, "blocked-work"), (lived, "lived-fault")):
        if field is not None and not _names_something(field):
            return [(field[0], "the %s field carries a placeholder where a birth belongs — %r"
                               % (what, field[1]))], notes
    return [], notes


def _targets(paths):
    """Every complete deposit in the given folders and files.

    Each file is read whatever its extension, with one exception: a name ending `.draft` is a deposit
    still being written under the atomic-write protocol (SPEC INV-249), so the gate passes over it
    exactly as the receiving sweep does — the two agree, and a mid-write deposit reds nothing. This
    grants no evasion: a file left `.draft` forever is never harvested or delivered either, so it
    stays outside the traffic the gate judges.
    """
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(
                os.path.join(p, n) for n in os.listdir(p)
                if os.path.isfile(os.path.join(p, n))
                and not n.startswith(".")
                and not n.endswith(".draft")
                and os.path.splitext(n)[0].lower() != "readme"
            )
        elif os.path.isfile(p) and not p.endswith(".draft"):
            files.append(p)
    return files


def main(argv):
    paths = argv[1:] or ([os.path.join(os.getcwd(), "inbox")]
                         if os.path.isdir(os.path.join(os.getcwd(), "inbox")) else [])

    any_found = False
    for path in _targets(paths):
        findings, notes = scan_file(path)
        for n, msg in findings:
            any_found = True
            print("%s:%d: %s" % (path, n, msg))
        for msg in notes:
            print("%s: note: %s" % (path, msg))

    if any_found:
        print()
        print("An agent's deposit names its source in the filename, and an agent's message")
        print("names its birth inside the file:")
        print()
        print("  inbox/YYYY-MM-DD-from-<agent>-<slug>.md")
        print()
        print("Blocked by this zone — the message names the work standing still:")
        print()
        print("    Blocked: <the work of mine that stands until this is answered>")
        print("    Need-by: <a date, or none>")
        print("    Id: <a stable identifier this message's reply can name>")
        print()
        print("Carrying a lived fault — the message names the fault and the evidence, and")
        print("nothing of the sender's need stand still:")
        print()
        print("    Lived: <the fault I hit in your zone, and the evidence I hold: what ran,")
        print("            what happened, how it showed>")
        print("    Need-by: <a date, or none>")
        print("    Id: <a stable identifier this message's reply can name>")
        print()
        print("A reply names the message it discharges and owes no birth of its own:")
        print()
        print("    Re: <that message's identifier>")
        print()
        print("The owner's own wish (from-owner-...) and a bridged Issue (stranger-...) owe")
        print("nothing. A message that can name neither birth is never sent. The sweep clears")
        print("this red by declining the message at the door, so no human reads it — the whole")
        print("format lives in inbox/README.md (SPEC INV-189, INV-190, INV-192, base rule 31).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
