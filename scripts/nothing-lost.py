#!/usr/bin/env python3
"""nothing-lost — one command that proves a document split or restructure lost nothing.

    python3 scripts/nothing-lost.py --before OLD.md --after new/*.md
    git show REV:OLD.md | python3 scripts/nothing-lost.py --before - --after new/*.md

It takes the document as it stood and the files it became, and prints the parts of the old document
that are present in none of the new files. Empty output and exit 0 mean every word and every mark
was accounted for. Any block that did not survive is printed whole, and the exit code is 1.

WHAT IT COMPARES

The comparison granularity is the BLOCK: a heading, a paragraph, a list item with its continuation
lines, a table row, a fenced code block, a thematic break. Each block is normalized -- runs of
whitespace collapsed to one space, leading and trailing whitespace dropped, a table row's cells
stripped of their padding, a fenced block dedented to its own opening fence -- and the two sides are
compared as multisets of those normalized blocks.

Two coarser and two stricter levels were available, and the block is the level that holds:

  - A bag of WORDS passes a document whose paragraphs were shredded and reassembled in the wrong
    order, and it can never print "this paragraph is gone" because it has no paragraphs to print.
    The row asks the command to print the paragraph it lost.
  - A bag of LINES fails on the thing every restructure does: rewrapping. It also cannot tell a
    dropped sentence from a rewrapped one.
  - A byte DIFF reds on every legitimate split -- new file headings, changed section order, one
    added newline at the end of a part.
  - An ordered diff of blocks reds on reordering, and reordering is the whole point of a split:
    sections move into separate files, and the files are read in a new order.

A block is compared verbatim after that normalization, so every word inside it is accounted for: a
paragraph with one sentence trimmed off is a DIFFERENT block, and the original is reported missing.
Marks are kept, never stripped: the `#` of a heading, the `-` of a bullet, the `|` of a table row,
the backticks of an inline code span, a `[^1]` footnote marker, a link's brackets and target all sit
inside the normalized text and all have to survive somewhere.

What the restructure ADDED -- a new part's own title, a parts-map table, a front-matter line -- is
not loss. The count of added blocks is reported on the summary line so nothing is hidden, and it
does not affect the exit code. Loss is what this command judges.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE_ROW = re.compile(r"^\s*\|")
BREAK = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s")


def _normalize_table_row(line):
    """A table row with its cell padding removed, so a reflowed table is not read as loss."""
    cells = line.strip().split("|")
    return "|".join(" ".join(c.split()) for c in cells)


def _normalize_fence(lines, indent):
    """A fenced block dedented to its own opening fence, each line's trailing space dropped.

    Whitespace INSIDE a code block carries meaning, so it is kept; the block's own indentation
    changes when it moves out of a list or into a file of its own, and that is not loss.
    """
    out = []
    for line in lines:
        if line[:indent].strip() == "":
            line = line[indent:]
        out.append(line.rstrip())
    return "\n".join(out)


def blocks(text, origin):
    """Every block of a markdown document, as (normalized_text, kind, origin, line_number).

    Blocks that normalize to nothing are dropped: a run of blank lines is not content.
    """
    lines = text.splitlines()
    found = []
    para, para_at, para_kind = [], 0, "paragraph"

    def flush():
        if para:
            joined = " ".join(" ".join(para).split())
            if joined:
                found.append((joined, para_kind, origin, para_at))
        del para[:]

    i = 0
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if m:
            flush()
            indent, marker = len(m.group(1)), m.group(2)[0]
            closer = re.compile(r"^\s*%s{%d,}\s*$" % (re.escape(marker), len(m.group(2))))
            fence, start = [line], i
            i += 1
            while i < len(lines):
                fence.append(lines[i])
                if closer.match(lines[i]):
                    i += 1
                    break
                i += 1
            body = _normalize_fence(fence, indent)
            if body.strip():
                found.append((body, "code block", origin, start + 1))
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        if HEADING.match(line):
            flush()
            found.append((" ".join(line.split()), "heading", origin, i + 1))
            i += 1
            continue
        if BREAK.match(line):
            flush()
            found.append((" ".join(line.split()), "thematic break", origin, i + 1))
            i += 1
            continue
        if TABLE_ROW.match(line):
            flush()
            found.append((_normalize_table_row(line), "table row", origin, i + 1))
            i += 1
            continue
        if LIST_ITEM.match(line):
            flush()
            para_kind, para_at = "list item", i + 1
            para.append(line)
            i += 1
            continue
        if not para:
            para_kind, para_at = "paragraph", i + 1
        para.append(line)
        i += 1
    flush()
    return found


def read_document(path):
    if path == "-":
        return sys.stdin.read(), "<stdin>"
    with open(path, encoding="utf-8") as f:
        return f.read(), path


def compare(before_blocks, after_blocks):
    """The blocks of `before` that no file of `after` accounts for, in the order they were written.

    Multiset, not set: a paragraph the old document carried twice and the new files carry once has
    lost one copy, and that copy is reported.
    """
    available = Counter(b[0] for b in after_blocks)
    seen = Counter()
    missing = []
    for norm, kind, origin, lineno in before_blocks:
        seen[norm] += 1
        if seen[norm] > available[norm]:
            missing.append((norm, kind, origin, lineno))
    return missing


def report(missing, before_blocks, after_blocks, after_paths, out, err):
    added = sum((Counter(b[0] for b in after_blocks) - Counter(b[0] for b in before_blocks)).values())
    print(
        "%d blocks before, %d blocks across %d file(s); %d missing, %d added by the restructure"
        % (len(before_blocks), len(after_blocks), len(after_paths), len(missing), added),
        file=err,
    )
    if not missing:
        return 0
    by_kind = defaultdict(int)
    for _norm, kind, _origin, _lineno in missing:
        by_kind[kind] += 1
    summary = ", ".join("%d %s" % (n, k) for k, n in sorted(by_kind.items()))
    print("Present before, present in none of the files it became: %d block(s) (%s)"
          % (len(missing), summary), file=out)
    for norm, kind, origin, lineno in missing:
        print("", file=out)
        print("  %s:%d  %s" % (origin, lineno, kind), file=out)
        for line in norm.splitlines():
            print("  | %s" % line, file=out)
    return 1


def main(argv=None, out=None, err=None):
    out = out or sys.stdout
    err = err or sys.stderr
    ap = argparse.ArgumentParser(
        prog="nothing-lost.py",
        description="Prove a document split or restructure lost no word and no mark.",
    )
    ap.add_argument("--before", required=True,
                    help="the document as it stood; `-` reads it from standard input")
    ap.add_argument("--after", required=True, nargs="+",
                    help="the files it became, in any order")
    args = ap.parse_args(argv)

    before_text, before_origin = read_document(args.before)
    before_blocks = blocks(before_text, before_origin)

    after_blocks = []
    for path in args.after:
        text, origin = read_document(path)
        after_blocks.extend(blocks(text, origin))

    missing = compare(before_blocks, after_blocks)
    return report(missing, before_blocks, after_blocks, args.after, out, err)


if __name__ == "__main__":
    sys.exit(main())
