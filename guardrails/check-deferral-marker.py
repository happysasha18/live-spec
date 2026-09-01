#!/usr/bin/env python3
"""check-deferral-marker.py — the mechanical net for the deferral test (SPEC INV-152).

Rule 29 / INV-152 already require it: writing a needs-the-human's-word marker on a
work item obliges you to NAME the human-only fact behind it — a taste, a policy, or
an act irreversible outside git — and a marker that cannot name its reason defaults
to the seat, the marker itself being the finding. Until now that was discipline only.

This gate is its mechanical arm, the same shape as INV-155's retry-plugin grep: it
reads a resume or decision file as a list of logical WORK ITEMS, finds each item that
parks work for the human, and reds when such an item names no reason category. To
pass, an item either names its reason (one of the four categories below, or a close
natural kin) or drops the marker because the seat can derive the answer and just do it.

A park is recognised by the GRAMMATICAL SHAPE of a deferral rather than a closed list of
phrasings (ROADMAP 417): an open-decision marker (⟨DECIDE⟩, TBD, "to be decided") or a
deferral predicate whose object is the human. So the ⟨DECIDE⟩ marker — the very token
that polices open decisions — is itself caught when it names no human-only fact, instead
of walking straight through the gate policing it.

  Reason categories that satisfy the rule: taste · policy · irreversible · device-feel.

An item is a bullet plus its wrapped continuation lines, folded into one unit before
scanning — because NEXT_STEPS files hard-wrap, a signal and its reason routinely sit on
different physical lines of one bullet. A blank line, a heading, or a new bullet starts
a new item; a fenced code block is skipped whole. A NEGATED mention ("NOT owner-reserved")
and a signal narrated inside quotes are both left alone.

Known bound: two independent parks jammed into one physical bullet, one reasoned and one
not, read as a single item, so the reasoned clause can cover the bare one. Splitting on
every clause boundary would instead FALSE-BLOCK a legitimate wrapped reason (the more
damaging failure, since a spurious red trains a human to bypass the whole commit hook),
so the item is the unit and this narrow case is accepted.

Usage:
  check-deferral-marker.py [FILE ...]
    FILE  files to scan; defaults to ./NEXT_STEPS.md and ./docs/decisions/*.md when present.
Exit 0 when every parked item names its reason; exit 1 (with path:line: findings)
when one does not. Stdlib only.
"""

import glob
import os
import re
import sys

# The GRAMMATICAL SHAPE of a deferral, read rather than a closed literal list (ROADMAP 417). A parked
# item takes one of two grammatical forms, and either is a deferral whatever its exact words:
#
#   (1) an OPEN-DECISION MARKER — a bracketed decide/decision token (⟨DECIDE⟩, <DECISION>, [DECIDE]) or
#       a to-be-decided phrase (TBD, "to be decided", "decision pending", "open decision"). This is the
#       form the old literal list was blind to, so ⟨DECIDE⟩ — the very marker that polices deferrals —
#       used to walk straight through the gate policing it.
#   (2) a DEFERRAL PREDICATE whose object is the human — a verb of holding/handing (hold, reserve,
#       defer, await, wait, leave) pointed at him (for/to/on his ...), or the possessive "his to
#       <verb>" / "still his". A version-bump park ("row N reserved") is one instance of (2).
#
# Kept narrow at the edges on purpose: a blocking gate must not fire on narration that merely quotes
# "his word" while describing a decision already made, so bare "his word" is NOT a marker — a genuine
# park says more. The pack's resume and decision files are written in English (docs language), which the
# gate scans; a human-language marker in chat is caught by the hook's delivery arm instead.
# (1) OPEN-DECISION MARKERS — the grammatical shape of an undecided fork handed forward. An open marker
# is an unresolved decision by definition, so it parks something whatever noun follows it.
OPEN_DECISION = [
    r"[⟨<\[]\s*dec(?:ide|ision)\s*[⟩>\]]",
    r"\bto be decided\b",
    r"\bdecision pending\b",
    r"\bopen decision\b",
    r"\bTBD\b",
]
# (2) a DEFERRAL PREDICATE whose object is the human.
PREDICATE = [
    r"his to (?:correct|call|pick|tune|decide|say|choose)",
    r"(?:needs?|awaits?|left to|reserved for|held for|held until|waiting on|waits on|deferred to|deferred until) his\b",
    r"(?:reserved|held|deferred|left) for (?:the )?(?:human|owner)\b",
    r"owner-?reserved",
    r"owner-?held",
    r"still his\b",
    r"row \d+ reserved",
]
SIGNALS = OPEN_DECISION + PREDICATE

# Naming the human-only fact — the CORE reason categories and their close judgement kin. These are words
# that only a human's judgement can settle, so any of them clears a park.
CORE_REASONS = [
    r"taste",
    r"policy",
    r"irreversible",
    r"device-?feel", r"device feel", r"real device",
    r"\bfeel\b", r"motion", r"visual",
    r"eye-?call", r"\bveto\b", r"his meter", r"visual meter",
]
# Craft nouns that name a human-only call in one context and a plain config/technical thing in another
# (a `sound` file, a `voice` feature, a `tone` value, an image `crop`). They clear a deferral PREDICATE
# already pointed at the human, but they do NOT by themselves clear an OPEN-DECISION marker: an open
# `⟨DECIDE⟩ which sound file to bundle` is a config choice the marker parks on nobody, and the bare
# noun's presence must not launder it through (the owner's 2026-07-17 adversarial-review finding).
SOFT_REASONS = [
    r"\bvoice\b", r"\btone\b", r"\bsound\b", r"crop",
]
REASONS = CORE_REASONS + SOFT_REASONS

NEGATORS = re.compile(r"\b(?:not|never|no)\b", re.IGNORECASE)
SIGNAL_RE = re.compile("|".join(SIGNALS), re.IGNORECASE)
OPEN_DECISION_RE = re.compile("|".join(OPEN_DECISION), re.IGNORECASE)
REASON_RE = re.compile("|".join(REASONS), re.IGNORECASE)
CORE_REASON_RE = re.compile("|".join(CORE_REASONS), re.IGNORECASE)
QUOTES = re.compile(r"'[^']*'|\"[^\"]*\"|«[^»]*»")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# A new work item opens with a list marker, optionally behind blockquote '>' prefixes,
# or with a bold lead used as an item head.
ITEM_START = re.compile(r"^(?:>\s*)*(?:[-*+]\s|\d+\.\s|\*\*\S)")


def _quoted_spans(text):
    """Character ranges wrapped in quotes — a signal there is narrated, not parked."""
    return [(m.start(), m.end()) for m in QUOTES.finditer(text)]


def _in_span(pos, spans):
    return any(a <= pos < b for a, b in spans)


def _negated(text, start):
    """True when a negator sits within the few words before the signal.

    A token window, not a fixed character count: "not currently owner-reserved" and
    "is not yet his to correct" both negate across filler a 9-char look-back would miss.
    Bounded to the last four words so an incidental negator far away cannot silence a
    real park. No source behind the exact 4 (2026-08-07 census, row 10); an engineering
    default, not a policy decision.
    """
    words = re.findall(r"\S+", text[:start])[-4:]
    return bool(NEGATORS.search(" ".join(words)))


def _fold_items(lines):
    """Yield (start_lineno, folded_text) for each logical work item.

    A bullet's wrapped continuation lines fold into one unit. A heading, a blank line,
    or a new bullet starts a new item; a fenced code block is skipped whole.
    """
    items = []
    cur = None
    in_fence = False
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip()
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            cur = None
            continue
        if in_fence:
            continue
        if stripped.startswith("#") or stripped == "":
            cur = None
            continue
        if cur is None or ITEM_START.match(line):
            cur = [i, [line]]
            items.append(cur)
        else:
            cur[1].append(line)
    for start, ls in items:
        text = HTML_COMMENT.sub(" ", " ".join(ls))
        yield start, " ".join(text.split())


def _fires(regex, text, spans):
    """True when the pattern matches unquoted and unnegated somewhere in the folded item."""
    return any(
        not _negated(text, m.start()) and not _in_span(m.start(), spans)
        for m in regex.finditer(text)
    )


def _parks_without_reason(text):
    """True when a folded item parks work for the human but names no reason it can accept.

    An OPEN-DECISION marker (⟨DECIDE⟩, TBD, ...) is an unresolved decision by definition, so it must
    name a CORE human-only fact to stand — a soft craft noun that merely happens to appear (a `sound`
    file) does not clear it. A deferral PREDICATE already pointed at the human accepts any reason, core
    or soft, since the human ownership is not in doubt, only its justification.
    """
    spans = _quoted_spans(text)
    if _fires(OPEN_DECISION_RE, text, spans):
        return not CORE_REASON_RE.search(text)
    if _fires(SIGNAL_RE, text, spans):
        return not REASON_RE.search(text)
    return False


def scan_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    return [(start, text) for start, text in _fold_items(lines) if _parks_without_reason(text)]


def _default_targets():
    targets = []
    ns = os.path.join(os.getcwd(), "NEXT_STEPS.md")
    if os.path.isfile(ns):
        targets.append(ns)
    targets += sorted(glob.glob(os.path.join(os.getcwd(), "docs", "decisions", "*.md")))
    return targets


def main(argv):
    paths = argv[1:] or _default_targets()

    any_found = False
    for path in paths:
        if not os.path.isfile(path):
            continue
        for n, text in scan_file(path):
            any_found = True
            shown = text if len(text) <= 160 else text[:157] + "..."
            print("%s:%d: parked for the human with no named reason — %s" % (path, n, shown))

    if any_found:
        print()
        print("A parked item must name its human-only fact (taste / policy / irreversible /")
        print("device-feel), or drop the marker and do it (SPEC INV-152, base rule 29).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
