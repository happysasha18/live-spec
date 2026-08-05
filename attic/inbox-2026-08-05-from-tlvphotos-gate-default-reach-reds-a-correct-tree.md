# A gate whose default reach is narrower than its scan reds on a correct tree

From: the tlvphotos window, 2026-08-05.
Subject: `guardrails/check-doc-rotation.py`, the pack's own template.

## What happened

Run with no arguments, the rotation gate failed on a tree where nothing is wrong:

```
FAIL (doc-rotation): a rotation lost content or left no manifest line (SPEC INV-209):
  - no manifest: docs/queue-archive/rotated-NEXT_STEPS-2026-08-05.md exists but no live
    manifest line points to it
```

The manifest line exists and is correct. Run the way the push gate runs it —
`--doc NEXT_STEPS.md --doc JOURNAL.md` — the same tree passes.

## The cause, and why it is a class

Two defaults disagree about reach. The documents scanned for manifest lines default to
`["ROADMAP.md"]`; the archives scanned for orphans default to the whole glob
`docs/queue-archive/rotated-*.md`. So any archive belonging to a document outside that
one-item default is reported as orphaned, and the report names a fault in the tree
rather than a gap in the run's own reach.

The class: a gate that scans one set for claims and a wider set for evidence, with the
two sets defaulting independently. Its verdict is only meaningful when the two reaches
match, and nothing in the gate checks that they do.

## What would close it

The gate can state its reach and refuse a run that cannot be conclusive: when the
archive glob can turn up archives belonging to documents outside `--doc`, either widen
the document set to every document that owns an archive under that glob, or fail with
"this run cannot judge X" rather than "X is broken". A verdict a caller can produce by
choosing arguments badly is worth what the arguments were.

Local note: this host's copy already carries a second, dated-section manifest form
(`SECTION_LINE_RE`), added 2026-08-05 for `NEXT_STEPS.md`, whose closed portion is a run
of dated resume anchors rather than numbered table rows. That finding was filed
separately; this one is about the reach, and stands whichever manifest form is read.
