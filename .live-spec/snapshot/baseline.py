"""The snapshot's own baseline machinery (SPEC E-7, `spec/doc-order-generated.md` Requirement 247).

`.live-spec/snapshot/` is git-tracked. Its manifest (`MANIFEST.md`) carries one line per surface:
the surface's name, the delivery id that set its current baseline, the content hash of that
baseline, and how the baseline's rendered bytes are held — inline (a `<surface>.snap` file tracked
beside the manifest) or external (a pointer into `blobs/`, gitignored, for a surface too heavy to
hold in git; only the manifest line and the hash travel under git for that surface).

The baseline advances only at a delivery, and only for the surfaces that delivery declares
(Requirement 247, criterion 1). `advance_baseline` is the one function that ever rewrites a
manifest line; a surface a delivery does not declare is left byte-for-byte as it was — its
manifest line, and any `.snap` or blob file it owns, are never touched.
"""

import hashlib
import os
import re

MANIFEST_NAME = "MANIFEST.md"
BLOBS_DIRNAME = "blobs"  # gitignored — where a heavy surface's bytes live outside git

_ENTRY_RE = re.compile(
    r"^- `(?P<surface>[^`]+)` \| baseline: `(?P<baseline>[^`]+)` \| "
    r"hash: `sha256:(?P<hash>[0-9a-f]+)` \| content: (?P<kind>inline|external) `(?P<pointer>[^`]+)`$"
)

_HEADER = """# Design-sync snapshot manifest

One line per surface (SPEC E-7, `spec/doc-order-generated.md` Requirement 247): the surface's
name, the delivery id that set its current baseline, the content hash of that baseline, and how
the baseline's rendered bytes are held.

A light surface holds its bytes inline, tracked beside this manifest as `<surface>.snap`. A
heavy-byte surface — too heavy to hold in git — holds only its manifest line and hash under git;
its rendered bytes live outside git under `blobs/` (gitignored) and the next run diffs against the
hash alone.

The baseline advances only at a delivery, and only for the surfaces that delivery declared — an
undeclared surface keeps its old line untouched. `baseline.py` in this folder is the one place that
writes a line; nothing else in the pack edits this file by hand."""


def content_hash(data: bytes) -> str:
    """The manifest's content hash for a surface's rendered bytes."""
    return hashlib.sha256(data).hexdigest()


def format_entry(surface, baseline, sha_hex, kind, pointer):
    return "- `%s` | baseline: `%s` | hash: `sha256:%s` | content: %s `%s`" % (
        surface, baseline, sha_hex, kind, pointer,
    )


def parse_manifest(text):
    """The manifest's surface lines, read in order. Returns (entries, order):
    entries maps surface name -> its parsed fields, order lists surface names as they appear.
    A line that does not match the entry shape (header prose, the placeholder line) is skipped."""
    entries = {}
    order = []
    for line in text.splitlines():
        m = _ENTRY_RE.match(line.strip())
        if not m:
            continue
        d = m.groupdict()
        entries[d["surface"]] = d
        order.append(d["surface"])
    return entries, order


def render_manifest(entries, order):
    lines = [_HEADER, "", "## Surfaces", ""]
    if not order:
        lines.append("(none yet)")
    else:
        for surface in order:
            e = entries[surface]
            lines.append(format_entry(surface, e["baseline"], e["hash"], e["kind"], e["pointer"]))
    return "\n".join(lines) + "\n"


def read_manifest(snapshot_dir):
    path = os.path.join(snapshot_dir, MANIFEST_NAME)
    if not os.path.exists(path):
        return {}, []
    with open(path, encoding="utf-8") as f:
        return parse_manifest(f.read())


def write_manifest(snapshot_dir, entries, order):
    os.makedirs(snapshot_dir, exist_ok=True)
    path = os.path.join(snapshot_dir, MANIFEST_NAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_manifest(entries, order))


def advance_baseline(snapshot_dir, delivery_id, declared, rendered, heavy=()):
    """Advance the baseline for exactly the surfaces `delivery_id` declared.

    `declared` — iterable of surface names the delivery declares.
    `rendered` — {surface_name: bytes}, the newly rendered content for each declared surface.
    `heavy` — the subset of `declared` whose bytes are held outside git: written under
      `blobs/<surface>.bin` and pointed to by the manifest line, only the line and the hash
      travelling under git. Every other declared surface is light: its bytes are written inline,
      tracked beside the manifest as `<surface>.snap`.

    A surface `delivery_id` does not declare is left untouched: its manifest line is rewritten
    byte-for-byte as it stood, and no file of its is read or written. (Requirement 247, criterion 1.)

    Returns the manifest's full entries dict after the advance.
    """
    declared = set(declared)
    heavy = set(heavy)
    entries, order = read_manifest(snapshot_dir)
    blobs_dir = os.path.join(snapshot_dir, BLOBS_DIRNAME)

    for surface in declared:
        if surface not in rendered:
            raise ValueError("declared surface %r has no rendered content" % surface)
        data = rendered[surface]
        sha_hex = content_hash(data)

        if surface in heavy:
            os.makedirs(blobs_dir, exist_ok=True)
            pointer = "%s/%s.bin" % (BLOBS_DIRNAME, surface)
            with open(os.path.join(snapshot_dir, pointer), "wb") as f:
                f.write(data)
            kind = "external"
        else:
            pointer = "%s.snap" % surface
            with open(os.path.join(snapshot_dir, pointer), "wb") as f:
                f.write(data)
            kind = "inline"

        entries[surface] = {
            "surface": surface,
            "baseline": delivery_id,
            "hash": sha_hex,
            "kind": kind,
            "pointer": pointer,
        }
        if surface not in order:
            order.append(surface)

    write_manifest(snapshot_dir, entries, order)
    return entries
