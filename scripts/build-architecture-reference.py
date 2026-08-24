#!/usr/bin/env python3
"""build-architecture-reference.py — generate the architecture's spec-anchor to node Reference
(SPEC INV-315, R312).

This is the BUILDER, not a gate. It is the sibling of `scripts/build-matrix-reference.py` and
`scripts/build-index.py`: at freeze it reads ARCHITECTURE.md's node sections through the shared reader
`guardrails/archformat.py` (INV-280's one-reader law) and emits the `| Anchor | Nodes |` table, mapping
each spec anchor a node owns to the node names that own it. The table is OUTPUT ONLY — no one edits it
by hand; the architecture-reference gate (`guardrails/check-architecture-reference.py`) reds a committed
Reference that differs from a fresh build or disagrees with the nodes (INV-315).

Anchors are read from each node's `owns` field only, never `pins` — archformat.py's own documented
boundary. A range anchor such as `INV-250..INV-265` expands to its member codes through
`Node.anchors_expanded` before mapping, so a per-code ownership check finds each member.

ARCHITECTURE.md is a single file today (no parts map the way the spec and the matrix carry one), so this
builder takes exactly one input path — the sibling shape simplifies the moment the document grows parts.

Usage:
  build-architecture-reference.py <ARCHITECTURE.md>            # print the generated Reference table
  build-architecture-reference.py <ARCHITECTURE.md> -o <file>  # write the generated table to <file>
Stdlib only.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS = os.path.join(os.path.dirname(SCRIPT_DIR), "guardrails")
sys.path.insert(0, GUARDRAILS)
import archformat as af  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "build-architecture-reference"


def code_sort_key(code):
    """A stable sort key for a code token: (prefix, first number)."""
    m = re.match(r"([A-Z]+)-(\d+)", code)
    return (m.group(1), int(m.group(2))) if m else (code, 0)


def parse_nodes(text):
    """The architecture's node sections, parsed through the shared reader (INV-280). Raises
    ValueError when the text still carries the retired `## Nodes` table shape — archformat's own
    guard, surfaced here rather than re-implemented."""
    return af.parse_nodes(text)


def anchor_to_nodes(nodes):
    """{anchor: [node names, first-seen order]} over the parsed nodes' owns fields, ranges expanded."""
    mapping = {}
    for n in nodes:
        for a in n.anchors_expanded:
            mapping.setdefault(a, [])
            if n.name not in mapping[a]:
                mapping[a].append(n.name)
    return mapping


def node_anchors(nodes):
    """The set of anchors owned by at least one node's owns field, ranges expanded."""
    out = set()
    for n in nodes:
        out.update(n.anchors_expanded)
    return out


def build_reference_table(nodes):
    """The generated Reference table (INV-315): each anchor a node's owns field carries, mapped to the
    node names that own it, both dimensions sorted stably. Output only — this is what the gate rebuilds
    to compare against the committed section."""
    mapping = anchor_to_nodes(nodes)
    lines = ["| Anchor | Nodes |", "|---|---|"]
    for a in sorted(mapping, key=code_sort_key):
        names = sorted(mapping[a])
        lines.append("| %s | %s |" % (a, ", ".join(names)))
    return "\n".join(lines) + "\n"


def table_anchors(section_text):
    """The set of anchors in the first column of a committed Reference table."""
    out = set()
    for line in section_text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if first.lower() == "anchor" or set(first) <= set("-: "):
            continue
        if af.ANCHOR_RE.fullmatch(first):
            out.add(first)
    return out


def build(text):
    """The generated table for an architecture document's text. Raises VacuousInputError when the
    document carries no node section (INV-218) — a Reference built over nothing is the defect, not a
    happy void."""
    nodes = require_nonempty(CHECK, "the architecture node sections", parse_nodes(text))
    return build_reference_table(nodes)


def main(argv):
    args = list(argv[1:])
    out_path = None
    if "-o" in args:
        i = args.index("-o")
        if i != len(args) - 2:
            print("%s: usage: %s <ARCHITECTURE.md> [-o <file>]" % (CHECK, os.path.basename(argv[0])))
            return 2
        out_path = args[i + 1]
        args = args[:i]
    if len(args) != 1:
        print("%s: usage: %s <ARCHITECTURE.md> [-o <file>]" % (CHECK, os.path.basename(argv[0])))
        return 2
    path = args[0]
    if not os.path.isfile(path):
        print("%s: cannot read %s — the builder stands on the architecture file." % (CHECK, path))
        return 1
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        table = build(text)
    except ValueError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    if out_path is not None:
        if os.path.realpath(out_path) == os.path.realpath(path):
            print("%s: -o %s is the input architecture file itself — the builder never overwrites its "
                  "input; write the table elsewhere and point the gate at it." % (CHECK, out_path))
            return 1
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(table)
        print("%s: wrote the generated Reference to %s" % (CHECK, out_path))
    else:
        sys.stdout.write(table)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
