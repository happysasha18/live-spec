#!/usr/bin/env python3
"""archformat.py — the shared reader for the architecture format (PROTOTYPE, ROADMAP row 456).

The sibling of `guardrails/specformat.py`: one home for reading ARCHITECTURE.md's node body, so every
consumer — the traceability suite's helpers, the node-growth counter, the pin-drift check, every test
that asks which node owns an anchor — reads the shape the same way. A consumer that greps the raw node
shape on its own is the defect the row-456 conversion retires; this module is the one reader they import.

THE NODE SHAPE this reader returns:

- A NODE is a section under the heading `### [node: <name>]`. A node promised under an owned queue row,
  its machinery still ahead, marks `[target]` after the closing bracket: `### [node: <name>] [target]`.
- A node section carries labelled fields, each `**<label>** — <text>`: `responsibility`, `owns`, `pins`,
  and an optional `notes`. The field text is read verbatim (a multi-line body is joined with spaces).
- The `owns` field lists the spec anchors the node owns; an anchor is `[A-Z]+-[0-9]+` with an optional
  `..` range tail, the same token shape specformat.py's CODE carries. Anchors are read from `owns` only.
- The `pins` field lists backticked `path:line` pins, each with an optional parenthetical label.

The OLD shape — one 4-column table row per node under `## Nodes` — is detected and refused with a clear
message, so a caller never silently reads a pre-conversion document as if it held sections.

Stdlib only.
"""
import re
import sys

# A spec anchor token: a letter-run, dash, number, with an optional range tail — the same shape
# specformat.py's CODE carries, so the two readers agree on what an anchor is.
ANCHOR = r"[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?"
ANCHOR_RE = re.compile(ANCHOR)

# A range anchor, e.g. `INV-250..INV-265` or `INV-260..263` or `T-1..T-6`. The spec tags each member as
# its own criterion, so an owns cell citing the range owns every member; expand it so a per-code
# ownership check (the traceability suite) finds each member. A mixed-family range is kept whole.
RANGE_RE = re.compile(r"^([A-Z]+)-([0-9]+)\.\.(?:([A-Z]+)-)?([0-9]+)$")


def expand_anchor(tok):
    """A range anchor to the list of its member codes; a plain anchor to itself in a one-item list."""
    m = RANGE_RE.match(tok)
    if not m:
        return [tok]
    pre, start, pre2, end = m.groups()
    if pre2 and pre2 != pre:
        return [tok]
    lo, hi = int(start), int(end)
    if hi < lo:
        return [tok]
    return ["%s-%d" % (pre, n) for n in range(lo, hi + 1)]

# A node heading: `### [node: <name>]` with an optional trailing `[target]` mark.
NODE_HEAD_RE = re.compile(r"^###\s+\[node:\s*(.+?)\]\s*(\[target\])?\s*$")

# A field line: `**<label>** — <text>` (em dash separator).
FIELD_RE = re.compile(r"^\*\*(responsibility|owns|pins|notes)\*\*\s*—\s*(.*)$")

# A pin: a backticked `path:line`, with an optional parenthetical label that follows it.
PIN_RE = re.compile(r"`([^`]+:\d+)`(?:\s*\(([^)]*)\))?")

# The retired 4-column table header (`| Node | Responsibility ... |`) — its presence means the old shape.
OLD_TABLE_HEADER_RE = re.compile(r"^\|\s*Node\s*\|\s*Responsibility")

FIELD_LABELS = ("responsibility", "owns", "pins", "notes")


class Node(object):
    def __init__(self, name, is_target, line_no):
        self.name = name                # the node name, the [target] mark stripped
        self.is_target = is_target      # True when the heading carried a [target] mark
        self.line_no = line_no          # 1-based source line of the heading
        self.fields = {}                # label -> raw field text

    @property
    def responsibility(self):
        return self.fields.get("responsibility", "")

    @property
    def owns(self):
        return self.fields.get("owns", "")

    @property
    def pins_text(self):
        return self.fields.get("pins", "")

    @property
    def notes(self):
        return self.fields.get("notes", "")

    @property
    def anchors(self):
        """The distinct spec anchors this node owns, read from the `owns` field only, ranges whole."""
        return set(ANCHOR_RE.findall(self.owns))

    @property
    def anchors_expanded(self):
        """The owned anchors with every range expanded to its member codes — the set a per-code
        ownership check (the traceability suite) compares against the spec's individual criteria."""
        out = set()
        for tok in ANCHOR_RE.findall(self.owns):
            out.update(expand_anchor(tok))
        return out

    @property
    def pins(self):
        """The pins list: (path:line, label) tuples, the label '' when a pin trails none."""
        return PIN_RE.findall(self.pins_text)

    @property
    def name_cell(self):
        """The node's name as the old table's first cell wrote it: name plus the mark when target."""
        return "%s [target]" % self.name if self.is_target else self.name


def parse_nodes(text):
    """Parse an architecture document's node sections into a list of Node objects, in source order.

    Refuses the retired table shape: if the old `## Nodes` table header is present, raises ValueError
    with a message naming the line and the fix, so a caller never reads a pre-conversion document as if
    it carried sections. Tolerant otherwise: a field's body may span lines (joined with spaces), and a
    non-node heading ends the current node's fields."""
    lines = text.split("\n")

    for i, ln in enumerate(lines):
        if OLD_TABLE_HEADER_RE.match(ln.strip()):
            raise ValueError(
                "archformat: refusing the retired table shape — line %d is the old 4-column Nodes "
                "table header (`| Node | Responsibility ... |`). This document predates the ROADMAP "
                "row-456 conversion to per-node `### [node: <name>]` sections; run convert.py before "
                "reading it." % (i + 1))

    nodes = []
    cur = None
    cur_field = None
    for i, raw in enumerate(lines):
        mhead = NODE_HEAD_RE.match(raw)
        if mhead:
            cur = Node(mhead.group(1).strip(), bool(mhead.group(2)), i + 1)
            nodes.append(cur)
            cur_field = None
            continue
        if cur is None:
            continue
        # Any other heading (a `## ` section, or a `### ` that is not a node) ends the current node.
        if raw.startswith("## ") or raw.startswith("### "):
            cur = None
            cur_field = None
            continue
        mfield = FIELD_RE.match(raw)
        if mfield:
            cur_field = mfield.group(1)
            cur.fields[cur_field] = mfield.group(2).strip()
            continue
        # A continuation line extends the current field's body (the future hand-edited multi-line form).
        if cur_field is not None and raw.strip():
            cur.fields[cur_field] = (cur.fields[cur_field] + " " + raw.strip()).strip()
    return nodes


def _summary(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    nodes = parse_nodes(text)
    n_anchor = sum(len(n.anchors) for n in nodes)
    n_pin = sum(len(n.pins) for n in nodes)
    print("archformat summary: %s" % path)
    print("  nodes:   %d" % len(nodes))
    print("  anchors: %d" % n_anchor)
    print("  pins:    %d" % n_pin)
    for n in nodes:
        print("    - %-16s target=%-5s anchors=%3d pins=%3d"
              % (n.name, str(n.is_target).lower(), len(n.anchors), len(n.pins)))
    return len(nodes), n_anchor, n_pin


def _emit_pins(path):
    """Print every node pin as `path<TAB>line<TAB>label`, one per line — the pin feed a consumer drives
    off instead of slicing the raw Nodes section itself (the pin-drift check is the first such consumer,
    SPEC INV-280). The label is the pin's parenthetical, empty when the pin trails none."""
    with open(path, encoding="utf-8") as f:
        nodes = parse_nodes(f.read())
    for n in nodes:
        for pin, label in n.pins:
            p, _, line = pin.rpartition(":")
            sys.stdout.write("%s\t%s\t%s\n" % (p, line, label))


if __name__ == "__main__":
    import os
    default = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "ARCHITECTURE.md")
    args = sys.argv[1:]
    if args and args[0] == "--pins":
        _emit_pins(args[1] if len(args) > 1 else default)
    else:
        _summary(args[0] if args else default)
