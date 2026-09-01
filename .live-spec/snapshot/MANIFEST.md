# Design-sync snapshot manifest

One line per surface (SPEC E-7, `spec/doc-order-generated.md` Requirement 247): the surface's
name, the delivery id that set its current baseline, the content hash of that baseline, and how
the baseline's rendered bytes are held.

A light surface holds its bytes inline, tracked beside this manifest as `<surface>.snap`. A
heavy-byte surface — too heavy to hold in git — holds only its manifest line and hash under git;
its rendered bytes live outside git under `blobs/` (gitignored) and the next run diffs against the
hash alone.

The baseline advances only at a delivery, and only for the surfaces that delivery declared — an
undeclared surface keeps its old line untouched. `baseline.py` in this folder is the one place that
writes a line; nothing else in the pack edits this file by hand.

## Surfaces

(none yet)
