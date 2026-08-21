#!/usr/bin/env python3
"""check-deposit-description.py — the agent-channel deposit-time description lint (SPEC INV-239, M-422).

BLOCKING. The presence net over the named-reference pair's new reach: the agent channel.

THE LAW behind it (E-35, INV-239). The named-reference pair — a stable code beside its plain
one-sentence description — travels in every cross-agent message, so a neighbour reads a self-explaining
file and never a bare code it cannot decode [INV-183]. This lint reads every `from-<agent>` inbox
deposit and reds a referenced internal code that arrives with no non-empty description beside it,
naming the code and the file. It is homed beside the earned-message gate `check-earned-message.py`,
which already reads those same deposited files, and it reuses that gate's file-discovery so the two
nets read one corpus by one rule [INV-189].

It judges PRESENCE ALONE, never the semantic match: whether the words beside a code truly describe it
is undecidable on a translated or reformulated sentence and belongs to the human net [INV-41, INV-83].
"INV-189 has nothing to do with the price of tea" carries words beside the code and passes this lint;
the human sweep reads whether they describe it.

WHERE IT LIVES. This lint RIDES THE SUITE (gate b) and takes NO push-gate letter, the same placement
`check-board.py`'s own suite test takes: its enforcement is a suite test
(tests/test_deposit_description.py) that runs it against the REAL inbox and asserts the expected
result, so a real violation reds the suite and gate b blocks the push. It is NOT wired into the
pre-push chain directly — a suite-riding check carries no gate letter, and its known-red proof is
the red-first test the suite runs.

WHAT COUNTS AS A DESCRIPTION (presence). The pair travels in full on a code's FIRST mention, and a
later reference in the same file carries the code alone [INV-28, INV-31]. So the lint reads each
distinct code's FIRST occurrence: on that line, with every code token, bracket, and punctuation
stripped, at least two plain words must stand beside it. A first mention with no words beside it — a
bare `Refs: INV-189, INV-190` line — reds; a later bare mention of an already-described code passes.

Honest bounds, the same shape the earned-message gate states:
  1. The trigger is self-declared. Only a `from-<agent>` deposit (or one carrying the agent card's
     `From: <name> (agent)` mark) is read; the owner's own wish and a bridged stranger Issue owe
     nothing and are skipped, exactly as the earned-message gate skips them.
  2. Presence, not correctness. The lint reads that words stand beside a code, not that they describe
     it. The false-positive risk of a meaning check outruns its catch, so the sweep and the prover
     own the semantic read [INV-150's honest split].

Usage:
  check-deposit-description.py [PATH ...]
    PATH  inbox folders or single files; defaults to ./inbox when present.
Exit 0 when every referenced code in every agent deposit carries a description on its first mention;
exit 1 (with file:code findings) when one stands bare. Stdlib only.
"""
import importlib.util
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# Reuse the earned-message gate's file-discovery and agent-declaration read, so the two nets read one
# corpus by one rule (the hyphenated filename blocks a plain import, so load it by path).
_CEM_PATH = os.path.join(SCRIPT_DIR, "check-earned-message.py")
_spec = importlib.util.spec_from_file_location("check_earned_message", _CEM_PATH)
_cem = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cem)

# An internal code token — the Formal-index anchor shape (INV-, E-, T-, A-, M-, ACT-, and the rest).
CODE = re.compile(r"\b[A-Z]{1,5}-[0-9]+\b")
# A plain word standing beside a code: a run of letters, two or more, not itself a bare field label.
WORD = re.compile(r"[A-Za-z]{2,}")
# The deposit's own field labels — words that are structure, not a description of a code.
FIELD_LABEL = re.compile(r"^(from|sender|blocked|lived|fault|need-by|id|re|refs?|subject)$", re.IGNORECASE)

MIN_WORDS = 2  # a first mention carries a description when at least this many plain words stand beside it


def _describing_words(line):
    """The plain words on a line that could describe a code — code tokens, brackets, punctuation, and
    bare field labels removed."""
    stripped = CODE.sub(" ", line)
    words = [w for w in WORD.findall(stripped) if not FIELD_LABEL.match(w)]
    return words


def scan_file(path):
    """[(code, lineno)] for each distinct code whose FIRST mention in this agent deposit stands bare."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except (UnicodeDecodeError, OSError):
        return []
    lines = _cem._uncode(raw.split("\n"))  # blank every fenced block: a quoted code is an example
    if not _cem._is_agent_message(path, lines):
        return []

    findings = []
    seen = set()
    for i, line in enumerate(lines, 1):
        for m in CODE.finditer(line):
            code = m.group(0)
            if code in seen:
                continue  # a later reference legally carries the code alone [INV-31]
            seen.add(code)
            if len(_describing_words(line)) < MIN_WORDS:
                findings.append((code, i))
    return findings


def main(argv):
    paths = argv[1:] or ([os.path.join(os.getcwd(), "inbox")]
                         if os.path.isdir(os.path.join(os.getcwd(), "inbox")) else [])

    any_found = False
    for path in _cem._targets(paths):
        for code, lineno in scan_file(path):
            any_found = True
            print("%s:%d: the referenced code %s arrives with no description beside it — the "
                  "named-reference pair travels in full on a code's first mention, so a neighbour "
                  "reads a self-explaining file (SPEC INV-239/E-35)." % (path, lineno, code))

    if any_found:
        print()
        print("An agent deposit names each internal code beside its plain one-sentence description on")
        print("the code's first mention, so a bare code never stands alone before the neighbour:")
        print()
        print("    Lived: the earned-message law [INV-189], which nets an unearned deposit, blocked my")
        print("           message, and I carry the evidence.")
        print()
        print("A later reference in the same file carries the code alone [INV-31]. This lint judges")
        print("presence alone; whether the words describe the code is the human sweep's read (INV-41).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
