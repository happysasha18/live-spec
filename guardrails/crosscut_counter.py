#!/usr/bin/env python3
"""crosscut_counter — the boundary-health signal, mechanized (SPEC INV-128 boundary-health, INV-37 re-carve).

The boundary-health law states the bar and the signal: a right node boundary keeps a typical request in
one node, and repeated cross-cutting landings on the same node pair are the signal that a boundary sits in
the wrong place (ARCHITECTURE.md, SPEC INV-128). This counter is the mechanical half INV-128 deferred to a
follow-on row: it reads the closed queue's cross-cutting landings and counts, per unordered NODE PAIR, how
many cross-cutting changes touched both nodes. A pair reaching the threshold within the window is FLAGGED
for the MINOR audit as a boundary-move candidate — the mechanized form of "seen twice, own it" (base rule
19) applied to module boundaries.

The flag is an AUDIT SIGNAL, not a per-push red: a boundary moves only through the architecture step and
its re-prove (SPEC INV-37), never on a hunch and never on a bare count. So the `__main__` runner exits 0
always and prints the flagged pairs for the MINOR audit to weigh; it never blocks a push.

Usage:  crosscut_counter.py [ROADMAP.md] [threshold]
"""

import glob
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)

DEFAULT_THRESHOLD = 3  # a pair cross-cut this many times is a boundary-move candidate; [default], tunable


def count_pairs(landings, threshold=DEFAULT_THRESHOLD):
    """landings: an iterable of node-sets, one per cross-cutting landing.
    Returns {frozenset(pair): count} for every unordered node pair reaching the threshold."""
    tally = {}
    for nodes in landings:
        uniq = sorted(set(nodes))
        for a, b in itertools.combinations(uniq, 2):
            key = frozenset((a, b))
            tally[key] = tally.get(key, 0) + 1
    return {k: c for k, c in tally.items() if c >= threshold}


def flagged_pairs(landings, threshold=DEFAULT_THRESHOLD):
    """The flagged pairs as a sorted list of (sorted-pair-tuple, count), highest count first."""
    flagged = count_pairs(landings, threshold)
    return sorted(
        ((tuple(sorted(k)), c) for k, c in flagged.items()),
        key=lambda kc: (-kc[1], kc[0]),
    )


def _crosscut_rows_by_number(text, known_nodes):
    """{rownum: named-nodes-set} for each landed row carrying a `footprint: cross-cutting` note whose
    status cell names two or more known nodes. Keyed by row number so a row that appears in both the
    body and an archive (a closed row that moved out under the live-body law) is counted once."""
    by_row = {}
    for line in text.splitlines():
        cells = line.split("|")
        status = next(
            (c for c in cells if re.search(r"footprint:\s*cross-cutting", c, re.IGNORECASE)),
            None,
        )
        if status is None:
            continue
        named = {n for n in known_nodes if re.search(r"\b" + re.escape(n) + r"\b", status)}
        if len(named) < 2:
            continue
        num = cells[1].strip() if len(cells) > 1 and cells[1].strip().isdigit() else None
        key = num if num is not None else ("_anon-%d" % len(by_row))
        by_row[key] = named
    return by_row


def crosscut_landings_from_roadmap(text, known_nodes):
    """Best-effort adapter for the real queue: the node-sets of the cross-cutting landed rows in one
    text. ADVISORY input to the MINOR audit — a cross-cutting note names its nodes in prose, not a
    structured field, so the auditor reads the flag and weighs it, never a green/red gate."""
    return list(_crosscut_rows_by_number(text, known_nodes).values())


def crosscut_landings_union(base, known_nodes):
    """The union of the body and the archives: the closed queue's cross-cutting landings now live in
    docs/queue-archive/*.md as well as (pre-conversion) the ROADMAP.md body. Both are scanned and the
    rows deduped by number, so a row counted in the body is not double-counted after it moves to an
    archive under the live-body law (SPEC INV-276)."""
    import os
    by_row = {}
    roadmap = os.path.join(base, "ROADMAP.md")
    files = []
    if os.path.isfile(roadmap):
        files.append(roadmap)
    files += sorted(glob.glob(os.path.join(base, "docs", "queue-archive", "*.md")))
    anon = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            for k, v in _crosscut_rows_by_number(f.read(), known_nodes).items():
                if str(k).startswith("_anon"):
                    by_row["_anon-%s-%d" % (os.path.basename(path), anon)] = v
                    anon += 1
                else:
                    by_row.setdefault(k, v)  # first home wins; body precedes archives
    return list(by_row.values())


def pack_nodes(architecture_path):
    """The pack's own node names, read live from ARCHITECTURE.md's node sections (guardrails/
    archformat.py, SPEC INV-280) — the known vocabulary the cross-cutting-note adapter matches
    against, rederived every run instead of held as a literal that drifts from the real map.
    ARCHITECTURE.md may be a core plus parts (its own `## Parts map`); archformat's own reader
    expands that the same way its `--pins` CLI does, so this sees every node either way."""
    text = archformat.read_architecture(architecture_path)
    return [node.name for node in archformat.parse_nodes(text)]


def main(argv):
    roadmap = argv[1] if len(argv) > 1 else "ROADMAP.md"
    threshold = int(argv[2]) if len(argv) > 2 else DEFAULT_THRESHOLD
    # Read the UNION of the body and the archives, deduped by row number: the closed queue's
    # cross-cutting landings live in docs/queue-archive/*.md as well as (pre-conversion) the body.
    base = os.path.dirname(os.path.abspath(roadmap)) or "."
    landings = crosscut_landings_union(base, pack_nodes(os.path.join(base, "ARCHITECTURE.md")))
    ranked = flagged_pairs(landings, threshold)
    if not ranked:
        print("cross-cut counter: no node pair reached threshold %d — boundaries look healthy" % threshold)
    else:
        print("cross-cut counter: %d node pair(s) at or above threshold %d — boundary-move candidates for "
              "the MINOR audit (SPEC INV-128, INV-37):" % (len(ranked), threshold))
        for (a, b), c in ranked:
            print("  %s <-> %s : %d cross-cutting landings" % (a, b, c))
    return 0  # advisory only — never blocks a push


if __name__ == "__main__":
    sys.exit(main(sys.argv))
