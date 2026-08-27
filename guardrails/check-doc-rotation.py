#!/usr/bin/env python3
"""check-doc-rotation.py — gate t: the pack's append-only working docs are split and rotated, and
nothing rotated is lost (SPEC INV-209, ROADMAP rows 390 + 392).

ROADMAP.md, JOURNAL.md, PRODUCT_SPEC.md, and TEST_MATRIX.md grow with every landing until a guard's
scan and a grep run slow (the owner's word, 2026-07-17 ~18:25). So a fully-closed portion of a growable
document is rotated out of the live file into a dated archive under docs/queue-archive/, and the live
file keeps only live material while the archive keeps everything. Base rule 10's superseded-file-moves-
to-attic-with-a-manifest law, applied to a document's own closed portion: the live file keeps a MANIFEST
line naming which rows moved and the archive they moved to, so a ROADMAP row — cited by number across the
tree — stays findable. A reader who greps the live file for a rotated row's number meets the manifest
pointer and follows it to the archived row, which keeps its own `| n |` line so a grep resolves it there.

The manifest is a marker-keyed block in the live doc (its wording is free between the markers):

  <!-- rotated-manifest -->
  Rotated closed rows (base rule 10 — nothing lost; the archive keeps everything):
  - rows 14, 27, 33 → docs/queue-archive/rotated-ROADMAP-2026-07-18.md
  <!-- /rotated-manifest -->

Each manifest line names a row list (`14, 27, 33` or a range `14-16`) and the archive it moved to,
joined by `→` (or `->`). This gate reds four violations and passes a clean rotation:

  (a) CONTENT DROPPED — a row the manifest declares rotated is found in neither the live file nor its
      named archive (the archive is missing, or the archive holds no `| n |` line for it): the
      nothing-lost violation.
  (b) NO MANIFEST — a `rotated-*.md` archive file exists under the scanned archive glob yet no manifest
      line in any live doc points to it: the base-rule-10 violation (a superseded portion moved with no
      manifest line).

  (c) AMBIGUOUS ROTATION — a row declared rotated yet still present as a live `| n |` table row, so the
      row is findable twice and the canonical copy is unclear.
  (d) A NON-TERMINAL ROW IN AN ARCHIVE — a row inside a `rotated-*.md` archive file whose Status cell
      carries none of the terminal words the queue format states in one home (docs/roadmap-format.md):
      landed, decided, declined, superseded,
      matched case-insensitively and satisfied by a bolded or dated form like `**LANDED 2026-07-07
      ~11:47**`. A row's Status cell can open on a stale narration word (a `queued` or `in-work` opener
      on a row that later landed), with the terminal word standing anywhere in the cell, so this reads
      the whole cell rather than its leading word. It names the file and the row number and states that
      a non-terminal row belongs in the live queue body.

A clean rotation passes: every manifested row is grepable in its archive, no rotated row is still live,
every rotation archive is referenced by a manifest line, and every row inside an archive carries a
terminal status. Honest boundary: this reads the manifest's
promises against the archives — a structural scan, kin of check-board.py and check-cleanup-notice.sh. The
judgment of WHICH closed rows are ripe to rotate stays the author's own (scripts/rotate-doc.py performs
the move; this gate guards that it lost nothing).

Usage:
  check-doc-rotation.py                             push mode: scan the repo's ROADMAP.md + archives.
  check-doc-rotation.py --doc FILE [--doc FILE...]  scan the named live docs (relative to --base).
  check-doc-rotation.py --base DIR                  resolve docs/archives under DIR (default: repo root).
  check-doc-rotation.py --archive-glob GLOB         relative glob for orphan-archive scan
                                                    (default: docs/queue-archive/rotated-*.md).
"""
import argparse
import glob
import os
import re
import sys

MANIFEST_OPEN = "<!-- rotated-manifest -->"
MANIFEST_CLOSE = "<!-- /rotated-manifest -->"
# a manifest line: "rows 14, 27, 33-35 → <path>"  (arrow may be → or ->)
MANIFEST_LINE_RE = re.compile(r"rows\s+([0-9,\s–—-]+?)\s*(?:→|->)\s*(\S+)")
# an archive table row: "| 482 | ... | Status | ... |"
ARCHIVE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")
# The terminal words a row's exit carries, in any case, standing anywhere in the cell: a wish that
# shipped reads landed, a wish refused reads declined, a wish another row took over reads superseded,
# and a decision row's exit reads decided (the vocabulary the queue format states in one home,
# docs/roadmap-format.md, and scripts/rotate-doc.py reads the same list as its closed signals).
TERMINAL_WORD_RE = re.compile(r"\b(landed|decided|declined|superseded)\b", re.IGNORECASE)


def repo_root():
    import subprocess
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                      stderr=subprocess.DEVNULL, text=True).strip()
        if out:
            return out
    except Exception:
        pass
    return os.getcwd()


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse_numbers(spec):
    """'14, 27, 33-35' -> [14, 27, 33, 34, 35]."""
    nums = []
    for tok in re.split(r"[,\s]+", spec.strip()):
        if not tok:
            continue
        m = re.match(r"^(\d+)(?:[-–—](\d+))?$", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        nums.extend(range(a, b + 1))
    return nums


def _manifest_entries(doc_text):
    """[(rownum, archive_relpath)] parsed from the doc's manifest block(s)."""
    entries = []
    for block in re.findall(re.escape(MANIFEST_OPEN) + r"(.*?)" + re.escape(MANIFEST_CLOSE),
                            doc_text, re.S):
        for line in block.splitlines():
            m = MANIFEST_LINE_RE.search(line)
            if not m:
                continue
            archive = m.group(2)
            for n in _parse_numbers(m.group(1)):
                entries.append((n, archive))
    return entries


def _has_table_row(text, n):
    return re.search(r"(?m)^\|\s*%d\s*\|" % n, text) is not None


def _status_index(archive_text):
    """The Status column's position, read from the archive table's own header row rather than assumed.
    A legacy archive writes its header as `| # | Wish | Class | Status | Decision |` and the current
    format writes `| # | Wish (plain words) | Class | Status | Decision / acceptance |`; both are read
    the same way. A file whose header names no Status column falls back to the fourth field, the
    position every archive shipped so far uses."""
    for line in archive_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().lower() for c in line.split("|")[1:-1]]
        if not cells:
            continue
        for i, c in enumerate(cells):
            if c == "status":
                return i
        if cells[0].startswith("#"):
            break
    return 3


def _non_terminal_rows(archive_text):
    """[(rownum, status_snippet)] for archive rows whose Status cell carries none of the terminal
    words. The Status column's index comes from the table's own header. A row's free-form prose
    occasionally holds a stray literal `|` of its own, ahead of or inside the Status text; the field at
    that index opens on the Status cell's own text either way, which is where its stated word stands."""
    idx = _status_index(archive_text)
    bad = []
    for line in archive_text.splitlines():
        m = ARCHIVE_ROW_RE.match(line)
        if not m:
            continue
        n = int(m.group(1))
        fields = line.split("|")[1:-1]  # drop the row's bounding empty strings
        status = fields[idx].strip() if len(fields) > idx else ""
        if not TERMINAL_WORD_RE.search(status):
            bad.append((n, status))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None)
    ap.add_argument("--doc", action="append", default=None)
    ap.add_argument("--archive-glob", default="docs/queue-archive/rotated-*.md")
    args = ap.parse_args()

    base = args.base or repo_root()
    docs = args.doc or ["ROADMAP.md"]

    violations = []
    referenced = set()

    for doc in docs:
        doc_path = os.path.join(base, doc)
        if not os.path.isfile(doc_path):
            # a doc named for scanning that is absent is the caller's error, reported plainly.
            violations.append("scanned doc missing: %s" % doc)
            continue
        live_text = _read(doc_path)
        for n, archive in _manifest_entries(live_text):
            referenced.add(os.path.normpath(archive))
            arch_path = os.path.join(base, archive)
            if not os.path.isfile(arch_path):
                violations.append(
                    "content dropped: %s declares row %d rotated to %s, which is missing "
                    "(the row is in neither the live file nor an archive)" % (doc, n, archive))
            elif not _has_table_row(_read(arch_path), n):
                violations.append(
                    "content dropped: %s declares row %d rotated to %s, but that archive holds no "
                    "`| %d |` line for it — the row is lost" % (doc, n, archive, n))
            if _has_table_row(live_text, n):
                violations.append(
                    "ambiguous rotation: %s declares row %d rotated yet still carries it as a live "
                    "`| %d |` table row — findable twice, canonical copy unclear" % (doc, n, n))

    # orphan-archive scan: every rotation archive must be pointed to by a manifest line, and every row
    # inside an archive must carry a terminal status.
    for arch_path in sorted(glob.glob(os.path.join(base, args.archive_glob))):
        rel = os.path.normpath(os.path.relpath(arch_path, base))
        if rel not in referenced and os.path.basename(arch_path) not in {os.path.basename(r) for r in referenced}:
            violations.append(
                "no manifest: %s exists but no live manifest line points to it (base rule 10 — a "
                "superseded portion moved with no manifest line)" % rel)
        for n, status in _non_terminal_rows(_read(arch_path)):
            violations.append(
                "non-terminal row in archive: %s row %d carries Status %r, holding none of landed / "
                "decided / declined / superseded — a non-terminal row belongs in the live queue body" %
                (rel, n, status[:80]))

    if violations:
        print("FAIL (doc-rotation): moving old content into its archive lost something along the way —")
        print("  either the content itself or the note that says where to find it (SPEC INV-209).")
        print("  Without both, that content is effectively gone:")
        for v in violations:
            print("  - " + v)
        print("  Fix: ask your agent to redo the move with scripts/rotate-doc.py, which writes the")
        print("  archive and its manifest line together, and to restore anything dropped from git history.")
        return 1

    print("OK (doc-rotation): every rotated row is findable in its archive and every archive is "
          "named in a manifest line — nothing lost (INV-209).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
