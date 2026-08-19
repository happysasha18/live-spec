#!/usr/bin/env python3
"""build-matrix-reference.py — generate the matrix's spec-anchor to matrix-row Reference (SPEC INV-273).

This is the BUILDER, not a gate. It is the sibling of `scripts/build-index.py`: at freeze it reads
TEST_MATRIX.md's body rows and emits the `## Reference` table, mapping each spec anchor to the matrix
rows that cover it. The table is OUTPUT ONLY — no one edits it by hand; the matrix-reference gate
(`guardrails/check-matrix-reference.py`) reds a committed Reference that differs from a fresh build or
disagrees with the body (INV-273).

It reads a row's anchors the way the suite reads them (docs/test-matrix-format.md): the LAST trailing
bracket group of the fact sentence is the row's parent anchor; a row may cite several codes in that one
group, each mapped, and a range anchor of the form `T-1..T-7` expands to its members before mapping.
Only the last group is read, so an inline citation earlier in the sentence is never mistaken for the
row's anchor.

The matrix may be written as a core file plus part files (specformat's parts map): every path named
before the `-o` flag is read as ONE document, in the order given, and the table is built over that
whole concatenation. With one path and no parts this is the single file, byte for byte.

Usage:
  build-matrix-reference.py <matrix.md> [<part.md> ...]            # print the generated Reference table
  build-matrix-reference.py <matrix.md> [<part.md> ...] -o <file>  # write the generated table to <file>
Stdlib only.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS = os.path.join(os.path.dirname(SCRIPT_DIR), "guardrails")
sys.path.insert(0, GUARDRAILS)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "build-matrix-reference"

NODE_RE = re.compile(r"^### \[node: (.*)\]\s*$")
ANCHOR_TOKEN = r"[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?"
ANCHOR_RE = re.compile(ANCHOR_TOKEN)
LAST_BRACKET_RE = re.compile(r"\[([^\[\]]*)\]\s*$")
REFERENCE_HEAD = "## Reference"
# A line-anchored `## Reference` heading — never an inline `## Reference` mention in the preamble prose.
REFERENCE_SPLIT_RE = re.compile(r"(?m)^## Reference *$")


def expand(anchor):
    """`T-1..T-7` -> [T-1 ... T-7]; a plain anchor passes through."""
    m = re.match(r"([A-Z]+)-(\d+)\.\.(?:[A-Z]+-)?(\d+)$", anchor)
    if m:
        prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        return ["%s-%d" % (prefix, i) for i in range(lo, hi + 1)]
    return [anchor]


def code_sort_key(code):
    """A stable sort key for a code token: (prefix, first number)."""
    m = re.match(r"([A-Z]+)-(\d+)", code)
    return (m.group(1), int(m.group(2))) if m else (code, 0)


def body_text(text):
    """The matrix text up to the generated `## Reference` section — the body the Reference maps. The
    split is line-anchored, so a `## Reference` mention in the preamble prose never cuts the body."""
    return REFERENCE_SPLIT_RE.split(text, 1)[0]


def row_anchors(fact):
    """The expanded anchors of a fact sentence, read from its LAST trailing bracket group."""
    m = LAST_BRACKET_RE.search(fact.strip())
    anchors = []
    if m:
        for tok in ANCHOR_RE.findall(m.group(1)):
            anchors.extend(expand(tok))
    return anchors


def parse_rows(text):
    """[(row_id, [expanded anchors])] for each converted five-cell data row under a node block."""
    rows = []
    current = None
    for line in body_text(text).splitlines():
        m = NODE_RE.match(line)
        if m:
            current = m.group(1)
            continue
        if current and line.startswith("|") and not line.startswith("|---") and "Owning test" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) == 5:
                rows.append((cells[0], row_anchors(cells[1])))
    return rows


def anchor_to_rows(text):
    """{anchor: [row ids, first-seen order]} over the body rows."""
    mapping = {}
    for rid, anchors in parse_rows(text):
        for a in anchors:
            mapping.setdefault(a, [])
            if rid not in mapping[a]:
                mapping[a].append(rid)
    return mapping


def body_anchors(text):
    """The set of anchors carried on the body rows."""
    out = set()
    for _rid, anchors in parse_rows(text):
        out.update(anchors)
    return out


def build_reference_table(text):
    """The generated Reference table (INV-273): each anchor a body row carries, mapped to the row ids
    that cover it, both dimensions sorted stably. Output only — this is what the gate rebuilds to
    compare against the committed section."""
    mapping = anchor_to_rows(text)
    lines = ["| Anchor | Rows |", "|---|---|"]
    for a in sorted(mapping, key=code_sort_key):
        rids = sorted(mapping[a], key=code_sort_key)
        lines.append("| %s | %s |" % (a, ", ".join(rids)))
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
        if ANCHOR_RE.fullmatch(first):
            out.add(first)
    return out


def build(text):
    """The generated table for a matrix's text. Raises VacuousInputError when the body carries no
    converted row (INV-218) — a Reference built over nothing is the defect, not a happy void."""
    require_nonempty(CHECK, "the matrix body rows", parse_rows(text))
    return build_reference_table(text)


def main(argv):
    args = list(argv[1:])
    out_path = None
    if "-o" in args:
        i = args.index("-o")
        if i != len(args) - 2:
            print("%s: usage: %s <matrix.md> [<part.md> ...] [-o <file>]"
                  % (CHECK, os.path.basename(argv[0])))
            return 2
        out_path = args[i + 1]
        args = args[:i]
    if not args:
        print("%s: usage: %s <matrix.md> [<part.md> ...] [-o <file>]"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    paths = sf.spec_paths(args)
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        print("%s: cannot read %s — the builder stands on the matrix file."
              % (CHECK, ", ".join(missing)))
        return 1
    _read, text = sf.read_document(paths, expand=False)
    try:
        table = build(text)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    if out_path is not None:
        inputs = [os.path.realpath(p) for p in paths]
        if os.path.realpath(out_path) in inputs:
            print("%s: -o %s is the input matrix itself — the builder never overwrites its input; "
                  "write the table elsewhere and splice it under ## Reference." % (CHECK, out_path))
            return 1
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(table)
        print("%s: wrote the generated Reference to %s" % (CHECK, out_path))
    else:
        sys.stdout.write(table)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
