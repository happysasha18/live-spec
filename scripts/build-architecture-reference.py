#!/usr/bin/env python3
"""build-architecture-reference.py — generate the architecture's spec-anchor to node Reference, and
the node-to-part router table (SPEC INV-315, R312).

This is the BUILDER, not a gate. It is the sibling of `scripts/build-matrix-reference.py` and
`scripts/build-index.py`: at freeze it reads ARCHITECTURE.md's node sections through the shared reader
`guardrails/archformat.py` (INV-280's one-reader law) and emits TWO generated tables into
ARCHITECTURE.index.md:

  1. `| Anchor | Nodes |` — each spec anchor a node owns, mapped to the node names that own it.
  2. `| Node | Part | Responsibility |` — one row per node, sorted by node name, naming the part
     file that node's section lives in today and a one-line copy of its own `responsibility` field.
     This second table is GENERATED OUTPUT ONLY, the same law as the first: it is built fresh from
     the node sections every run, never a second hand-kept home for a node's responsibility — the
     authoritative text stays the node section's own field, this is a router reading of it.

Both tables are output only — no one edits them by hand; the architecture-reference gate
(`guardrails/check-architecture-reference.py`) reds a committed Reference that differs from a fresh
build or disagrees with the nodes (INV-315).

Anchors are read from each node's `owns` field only, never `pins` — archformat.py's own documented
boundary. A range anchor such as `INV-250..INV-265` expands to its member codes through
`Node.anchors_expanded` before mapping, so a per-code ownership check finds each member.

ARCHITECTURE.md may be written as a core file plus part files (specformat's parts map): every path
named before the `-o` flag is read as ONE document, in the order given, and the anchor table is built
over that whole concatenation — the sibling shape `build-matrix-reference.py` already carries. The
router table additionally needs to know, per node, WHICH of the named files its section came from; each
named path is therefore also parsed on its own (never assumed — a node could in principle move to any
part) to build that node-to-part map.

Usage:
  build-architecture-reference.py <ARCHITECTURE.md> [<part.md> ...]            # print both tables
  build-architecture-reference.py <ARCHITECTURE.md> [<part.md> ...] -o <file>  # write both tables
Stdlib only.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS = os.path.join(os.path.dirname(SCRIPT_DIR), "guardrails")
sys.path.insert(0, GUARDRAILS)
import archformat as af  # noqa: E402
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "build-architecture-reference"

ROUTER_HEAD = "| Node | Part | Responsibility |"


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
    """The generated Anchor Reference table (INV-315): each anchor a node's owns field carries,
    mapped to the node names that own it, both dimensions sorted stably. Output only — this is what
    the gate rebuilds to compare against the committed section."""
    mapping = anchor_to_nodes(nodes)
    lines = ["| Anchor | Nodes |", "|---|---|"]
    for a in sorted(mapping, key=code_sort_key):
        names = sorted(mapping[a])
        lines.append("| %s | %s |" % (a, ", ".join(names)))
    return "\n".join(lines) + "\n"


def node_to_part(paths):
    """{node name: display path} for every node found in any of `paths`, each parsed on its own so a
    node's actual file of origin is read, never assumed from grouping. `paths` are shown relative to
    the first path's directory (the core's directory) — the same display form the core's own Parts
    map table uses, so a router row and a Parts map row name the same file the same way."""
    if not paths:
        return {}
    base = os.path.dirname(os.path.abspath(paths[0])) or "."
    out = {}
    for p in paths:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        try:
            nodes = af.parse_nodes(text)
        except ValueError:
            continue
        if not nodes:
            continue
        rel = os.path.relpath(os.path.abspath(p), base)
        for n in nodes:
            out[n.name] = rel
    return out


def escape_cell(text):
    """A table cell's text with a literal `|` escaped, so a responsibility sentence that happens to
    carry one never breaks the row it sits in."""
    return text.replace("|", "\\|")


def build_router_table(nodes, part_of):
    """The generated node-to-part router table: one row per node, sorted by name, naming the part
    file the node's section lives in today (from `part_of`, built by parsing each named file on its
    own) and a one-line copy of the node's own `responsibility` field — GENERATED, never a second
    hand-kept home for that text (the node section's own field stays authoritative)."""
    lines = [ROUTER_HEAD, "|---|---|---|"]
    for n in sorted(nodes, key=lambda n: n.name):
        part = part_of.get(n.name, "?")
        resp = escape_cell(" ".join(n.responsibility.split()))
        lines.append("| %s | `%s` | %s |" % (n.name, part, resp))
    return "\n".join(lines) + "\n"


def router_table_rows(section_text):
    """{node name: (part, responsibility)} read back from a committed router table section."""
    out = {}
    for line in section_text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 3:
            continue
        name = cells[0]
        if name.lower() == "node" or set(name) <= set("-: "):
            continue
        out[name] = (cells[1].strip("`"), cells[2])
    return out


def table_anchors(section_text):
    """The set of anchors in the first column of a committed anchor-Reference table."""
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


def split_tables(committed_text):
    """(anchor-table-text, router-table-text) split at the router table's own header line. Either
    half may be empty (a pre-router-table committed file carries only the first)."""
    idx = committed_text.find(ROUTER_HEAD)
    if idx == -1:
        return committed_text, ""
    return committed_text[:idx], committed_text[idx:]


def build(text, paths):
    """The two generated tables for an architecture document's text plus the file set it came from.
    Raises VacuousInputError when the document carries no node section (INV-218) — a Reference built
    over nothing is the defect, not a happy void."""
    nodes = require_nonempty(CHECK, "the architecture node sections", parse_nodes(text))
    anchor_table = build_reference_table(nodes)
    part_of = node_to_part(paths)
    router_table = build_router_table(nodes, part_of)
    return anchor_table + "\n" + router_table


def main(argv):
    args = list(argv[1:])
    out_path = None
    if "-o" in args:
        i = args.index("-o")
        if i != len(args) - 2:
            print("%s: usage: %s <ARCHITECTURE.md> [<part.md> ...] [-o <file>]"
                  % (CHECK, os.path.basename(argv[0])))
            return 2
        out_path = args[i + 1]
        args = args[:i]
    if not args:
        print("%s: usage: %s <ARCHITECTURE.md> [<part.md> ...] [-o <file>]"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    paths = sf.spec_paths(args)
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        print("%s: cannot read %s — the builder stands on the architecture file."
              % (CHECK, ", ".join(missing)))
        return 1
    _read, text = sf.read_document(paths, expand=False)
    try:
        table = build(text, paths)
    except ValueError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    if out_path is not None:
        inputs = [os.path.realpath(p) for p in paths]
        if os.path.realpath(out_path) in inputs:
            print("%s: -o %s is the input architecture file itself — the builder never overwrites "
                  "its input; write the tables elsewhere and point the gate at it." % (CHECK, out_path))
            return 1
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(table)
        print("%s: wrote the generated Reference to %s" % (CHECK, out_path))
    else:
        sys.stdout.write(table)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
