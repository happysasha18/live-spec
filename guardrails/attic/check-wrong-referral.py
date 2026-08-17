#!/usr/bin/env python3
"""check-wrong-referral.py — a wrong referral is named as the finding (SPEC INV-225).

PARKED 2026-08-18 in `guardrails/attic/`. It is wired into nothing — no push chain, no CI step, no
runtime caller — and the only exchange it has ever read is the fixture its suite writes, so no real
wrong referral has ever been caught by it. Its suite still drives it here.

Rule / INV-225 states it: a referral names the zone it says owns the question, and it is
WRONG when that zone does not own it. A wrong referral shows itself in the exchange — the
named zone refers the question back rather than answering it, and the question crosses the
same two agents twice, the event the two-crossing bound counts (SPEC INV-196). That bound
sends the third crossing to the owner and, today, names it neutrally ("a zone question the
two could not settle"), which absorbs the wrong referral without ever saying one was made.
This checker is the mechanical arm that NAMES it.

  What is mechanically tellable, and what is not. A wrong referral cannot be told from a
  legitimate cross-zone referral at the MOMENT of sending — both read "that lives in zone
  X's zone, ask X", and whether X's claim actually covers the target is a natural-language
  match, the receiving sweep's and the prover's judgment (SPEC INV-150, the honest split
  every net here keeps). It becomes tellable from the exchange's SHAPE: a referral the named
  zone answers, or an onward referral to a THIRD zone that then answers, reaches no cap and
  names nothing; a referral the named zone refers BACK — a counter-referral between the same
  two agents — is the wrong referral, proven wrong by the named zone's own act of referring
  it back. So the checker reads the shape, never the target-vs-claim match.

  The overlap half of the same audit finding is refused by the owner's word — two agents'
  zones may overlap and no forced disjointness is wanted (the promoter inbox deposit,
  2026-07-17) — so this checker builds NO uniqueness or overlap check; only the wrong
  referral earns a name.

  Not a push gate. Like the far-tier report-shape check (SPEC INV-222/INV-223), an exchange
  is a status-report surface the agents speak at runtime; no committed exchange file exists
  for a push gate to scan (a chat surface is not machine-gatable, SPEC INV-83's sibling). The
  suite drives this checker over fixtures to red-prove the shape.

Exchange format. One file per exchange, a hop per line (fenced blocks are examples and are
skipped, so a file quoting this help is not read as hops):

    <!-- exchange: <id> -->
    Hop: referral from <agent-a> to <agent-b>
    Hop: referral from <agent-b> to <agent-a>      <- counter-referral => wrong referral
    Hop: answer   from <agent-a>

  A `referral` hop names the zone it points at (its `to`). An `answer` hop needs no `to`.
  A wrong referral is a referral hop later met by a referral hop that reverses it (the same
  unordered pair, the other direction). A referral met by an answer, or an onward referral to
  a new zone that is then answered, passes.

Usage:
  check-wrong-referral.py FILE [FILE ...]
Exit 0 when no exchange carries a wrong referral; exit 1 (with file:line: findings) when one
does. Stdlib only.
"""

import re
import sys

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HOP = re.compile(
    r"^\s*Hop:\s*(referral|answer)\s+from\s+(\S+)(?:\s+to\s+(\S+))?",
    re.IGNORECASE,
)


def _uncode(lines):
    """Lines with every fenced block blanked, line numbers preserved — a hop inside a fence is
    an example (this help quoted back), never a real hop."""
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


def _hops(lines):
    """(lineno, kind, frm, to) for every hop line, in order."""
    hops = []
    for i, line in enumerate(_uncode(lines), 1):
        m = HOP.match(line)
        if not m:
            continue
        kind = m.group(1).lower()
        frm = m.group(2)
        to = (m.group(3) or "").strip() or None
        hops.append((i, kind, frm, to))
    return hops


def scan_exchange(hops):
    """The wrong-referral findings for one exchange's ordered hops.

    A referral hop is WRONG when a LATER referral hop reverses it — points from the zone this
    referral named back to this referral's own sender (the same unordered pair, the other
    direction). That reversal is the named zone refusing ownership, which is what proves the
    referral pointed at a zone that does not own the target. A referral answered (an `answer`
    hop), or carried onward to a new third zone, never reverses and is never flagged.
    """
    findings = []
    referrals = [h for h in hops if h[1] == "referral" and h[3]]
    for idx, (ln, _kind, frm, to) in enumerate(referrals):
        for later in referrals[idx + 1:]:
            _ln2, _k2, frm2, to2 = later
            if frm2 == to and to2 == frm:
                findings.append(
                    (ln, "a wrong referral: %s referred the question to zone %s, which does "
                         "not own the target — %s referred it back rather than answering, so "
                         "the question crossed the same two agents twice (SPEC INV-225, "
                         "INV-196). Name the wrong referral in the sender's status report, "
                         "never absorb it silently under the hop-count cap."
                         % (frm, to, to))
                )
                break
    return findings


def scan_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except (UnicodeDecodeError, OSError):
        return []
    return scan_exchange(_hops(lines))


def main(argv):
    paths = argv[1:]
    if not paths:
        print("usage: check-wrong-referral.py FILE [FILE ...]", file=sys.stderr)
        return 2
    any_found = False
    for path in paths:
        for ln, msg in scan_file(path):
            any_found = True
            print("%s:%d: %s" % (path, ln, msg))
    if any_found:
        print()
        print("A referral names the zone it says owns the question, and it is wrong when that")
        print("zone refers it back rather than answering. Name the wrong referral as the finding")
        print("in the sender's own status report (SPEC INV-225); the two-crossing cap alone")
        print("(SPEC INV-196) would absorb it without ever saying one was made.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
