#!/usr/bin/env python3
"""sweep-rendered.py — clear the rendered pages whose reading is over (SPEC INV-286).

A rendered page is built to be read once. Without a sweep it stays in the tree until someone
notices it, so a working directory carries several at any moment and the count only grows.
This script performs the clearing: it finds each transient page, moves it to the attic with a
manifest line, and says out loud what it moved.

WHICH KIND A PAGE IS — the renderer decides. A page the pack's document renderer produced is
**transient**: it was built for one reading and rebuilds from its source in a second. Every other
page in the tree is the artifact itself and stays — a hand-built decision page, a frozen norm card,
a test fixture, a prototype sketch, a host's built site.

The rule reads the renderer's own mark, `<meta name="generator" content="live-spec render-doc">`,
which `scripts/render-doc.py` stamps into every page it writes. A page rendered before that mark
existed is recognised by the second half of the same evidence: its source document standing beside
it under the same name, which is what makes a render a render.

The renderer is the rule because it is the one thing that knows. A naming convention is a habit a
writer forgets on one file, and one forgotten name loses a page for good. A directory allowlist has
to be kept honest by hand, and it reads a host's `dist/`, `site/`, and `node_modules/` as pages
built for one reading, which is how a sweep eats a shipped website. The mark is written by the act
that creates the page, so it cannot drift from the truth, and it is carried by nothing else.

  4. A page committed before this law existed stands outside the reach and keeps standing. Clearing
     it is a deletion commit somebody makes deliberately, which this script leaves to them.

THE REACH, read before the rule. The sweep touches what version control does not track. A tracked
page is committed history, and removing it is a commit with its own gate — a different act from a
clearing, and one this script never performs silently. Four homes stand outside the reach beside
that: `.git/` and `.claude/` (git's own state and the harness's worktrees), `.live-spec/` (the host
state directory whose files the checkpoint law governs), and `attic/` (the clearing's own
destination). A host declares its own homes in `guardrails.config.json` under `rendered_pages`, the
same road the reach map's directory classes take (SPEC INV-224), so a host adopts without editing
this script.

DECISION: a declared home is ADDED to the pack's own four, never in their place. The four are a
floor, not a default a declaration can lower — a host that genuinely wants `.git/` or the attic
itself swept has no case worth serving, and a declaration meant to spare one extra directory must
never be read as the whole reach (R296.12, R296.13). `_config` below returns the four followed by
whatever the host adds, so the attic can never end up inside its own sweep's reach and a host that
declares one home of its own never loses `.git/` or `.live-spec` by saying nothing about them.

WHERE A CLEARED PAGE GOES — the attic, base rule 10's own home, never a second one. The attic copy
is the recovery: a page that turns out to be needed is moved back. The bytes stay out of git (a
rendered page rebuilds from its source, and `.gitignore` keeps `*.html` out of history), and
`attic/MANIFEST.md` is tracked, so the record of what was cleared is durable while the page itself
rests on disk the way a file rests in the trash.

The name a page takes in the attic follows the one collision law in its two moves (base rule 18,
SPEC E-9): the source directory prefixes the basename first, and a numeric ordinal before the
extension follows while the name is still taken. Nothing is ever overwritten.

WHAT THIS DOES NOT SEE, stated at its real width:

  1. It reads a page's mark, and never whether the person finished reading. The clearing is run at
     the close of an exchange and at a release, and a rule that tried to read attention would guess.
  2. A directory reached only through a symbolic link stands outside the walk, since following links
     invites a cycle. A page there is never cleared and never harmed.
  3. A page a person built by hand and then re-saved through the renderer carries the mark and reads
     as transient. The attic is what makes that recoverable.

Usage:
  sweep-rendered.py [--root PATH] [--dry-run]
    --root     the tree to sweep; defaults to the repo root this script sits in
    --dry-run  name what would move and move nothing
Exit 0 when the tree is readable; the clearing is not a verdict. The check
`guardrails/check-rendered-sweep.py` is what reds while a transient page still stands.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

# The renderer's mark, read from its one home so the two files can never disagree on its wording.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from importlib import util as _importutil
    _spec = _importutil.spec_from_file_location(
        "render_doc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "render-doc.py"))
    _rd = _importutil.module_from_spec(_spec)
    _spec.loader.exec_module(_rd)
    GENERATOR = _rd.GENERATOR
except Exception:                                            # a standalone copy with no renderer
    GENERATOR = "live-spec render-doc"

OUTSIDE_REACH = (".git", ".claude", ".live-spec", "attic")
SOURCE_SUFFIX = ".md"
ATTIC = "attic"
MANIFEST = "MANIFEST.md"
PAGE_SUFFIX = ".html"
# The mark sits in <head>; no page needs more than this read. A read bound on a file, not a bar any
# page is judged against — machinery tuning, kept and marked under the owner-ruled class
# (docs/audits/2026-08-07-number-rulings.md §3, which names this file; standing under his 2026-08-07
# 09:16 word). No incident or source behind the figure itself; it is one filesystem block, the
# ordinary size for "read the head and stop".
HEAD_BYTES = 4096

MANIFEST_HEADER = """# The attic manifest

Every file that left active use rests here with one line saying what it was (SPEC INV-7, A-4,
base rule 10). Nothing here was deleted; a file that turns out to be needed is moved back.

"""


def _config(root):
    """The pack's own four homes, plus whatever the host adds under guardrails.config.json.

    The four are a floor, never a default a declaration replaces (R296.12, R296.13): a host that
    declares one home of its own still keeps `.git/`, `.claude/`, `.live-spec/` and `attic/`
    outside the reach with no word said. Declaring the same name twice is harmless; it is kept
    once, in the order the four are always read first.
    """
    path = os.path.join(root, "guardrails.config.json")
    try:
        with open(path, encoding="utf-8") as f:
            block = json.load(f).get("rendered_pages") or {}
    except (OSError, ValueError):
        block = {}
    declared = block.get("outside_reach") or ()
    normalized = (n.strip().strip("/").replace(os.sep, "/") for n in tuple(OUTSIDE_REACH) + tuple(declared))
    seen = []
    for n in normalized:
        if n and n not in seen:
            seen.append(n)
    return tuple(seen)


def _under(rel, home):
    """True when a repo-relative path sits inside the given home directory."""
    return rel == home or rel.startswith(home.rstrip("/") + "/")


def tracked_pages(root):
    """Every page version control tracks, or None where the tree carries no git of its own.

    A tracked page is committed history: removing it is a commit with its own gate, which is a
    different act from a clearing. So the reach stops at what git tracks. None is the honest
    answer for a tree git does not cover, and it is not an empty set: the caller narrows the rule
    instead of assuming nothing is committed (SPEC INV-286, R296.11).
    """
    try:
        out = subprocess.run(["git", "-C", root, "ls-files", "-z", "--", "*.html", "*.HTML"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return {p for p in out.stdout.split("\0") if p}


def evidence(path, legacy_fallback=True):
    """Why this page reads as a render, or None when nothing says it is one.

    Two readings of one fact, and the returned words become the page's manifest line. The
    renderer's mark says so outright, and it is written by the act that creates the page, so it
    cannot be wrong. A source document standing beside the page under the same name says so by
    evidence, which is how a page rendered before the mark existed is recognised.

    That second reading is a heuristic, and it runs only where the tracked-page guard can stand
    behind it — a hand-built page kept beside notes of the same name looks exactly like an old
    render, and being committed is what tells the two apart. In a tree git does not cover, nothing
    can make that call, so the mark alone decides and the older pages stay standing.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(HEAD_BYTES)
    except OSError:
        return None                                   # a page that cannot be read is never moved
    if GENERATOR in head:
        return "carried the `%s` generator mark" % GENERATOR
    if legacy_fallback and os.path.isfile(path[: -len(PAGE_SUFFIX)] + SOURCE_SUFFIX):
        return "its source document stood beside it"
    return None


def classify(root):
    """(transient, records) — every page inside the reach, split by the renderer rule.

    `transient` holds (path, evidence) pairs and `records` holds paths, both sorted and
    repo-relative. A page version control tracks and a page in a home outside the reach are
    counted in neither: they stand beyond what a clearing may touch.
    """
    outside_reach = _config(root)
    tracked = tracked_pages(root)
    # No git over this tree means no way to tell a committed artifact from an uncommitted render,
    # so the legacy source-beside reading stands down and the mark alone decides.
    legacy_fallback = tracked is not None
    tracked = tracked or set()
    transient, records = [], []

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/")

        dirnames[:] = [d for d in dirnames
                       if not any(_under("/".join(filter(None, (rel_dir, d))), h)
                                  for h in outside_reach)]

        for name in sorted(filenames):
            # Case-folded, because a case-insensitive filesystem lets `REPORT.HTML` stand beside
            # `report.html` and a case-exact test would read past it.
            if not name.lower().endswith(PAGE_SUFFIX):
                continue
            rel = "/".join(filter(None, (rel_dir, name)))
            if rel in tracked:
                continue
            why = evidence(os.path.join(dirpath, name), legacy_fallback)
            if why:
                transient.append((rel, why))
            else:
                records.append(rel)

    return sorted(transient), sorted(records)


def attic_name(attic_dir, rel, claimed=()):
    """The name this page takes in the attic, under the one collision law (E-9, base rule 18).

    The law names two moves in order. The semantic mark the attic defines comes first: the page's
    source directory prefixes its basename, so `docs/x.html` and `notes/x.html` land apart on the
    first move. A page cleared from the tree root carries no source directory and keeps its bare
    name. A numeric ordinal before the extension follows while the name is still taken. Never an
    overwrite, never a third scheme.

    `claimed` holds the names this run already handed out, so two pages sharing one name land
    apart even when neither has moved yet (a dry run).
    """
    rel = rel.replace(os.sep, "/")
    source_dir, _, basename = rel.rpartition("/")
    candidate = "%s-%s" % (source_dir.replace("/", "-"), basename) if source_dir else basename

    stem, ext = os.path.splitext(candidate)
    n = 1
    while candidate in claimed or os.path.exists(os.path.join(attic_dir, candidate)):
        n += 1
        candidate = "%s-%d%s" % (stem, n, ext)
    return candidate


def _open_attic(root):
    """The attic directory, ready to receive, with its manifest header in place.

    A plain file already standing where the attic belongs is a collision the caller must see, so
    it is raised by name and the caller reports it in plain words.
    """
    attic_dir = os.path.join(root, ATTIC)
    if os.path.exists(attic_dir) and not os.path.isdir(attic_dir):
        raise RuntimeError("%s stands as a file where the attic belongs; move it and run again"
                           % ATTIC)
    os.makedirs(attic_dir, exist_ok=True)
    manifest = os.path.join(attic_dir, MANIFEST)
    if not os.path.exists(manifest):
        with open(manifest, "w", encoding="utf-8") as f:
            f.write(MANIFEST_HEADER)
    return attic_dir


def _record(attic_dir, line):
    """Append one manifest line and flush it to disk.

    Written per page, straight after that page moves, so a run that dies partway leaves every page
    it already moved accounted for. A batch write at the end loses the provenance of everything
    moved before the failure, and the attic keeps only a basename (SPEC INV-286, R296.5).
    """
    with open(os.path.join(attic_dir, MANIFEST), "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())


def sweep(root, dry_run=False, today=None):
    """Clear every transient page. Returns the list of (from, to) pairs it moved."""
    today = today or datetime.date.today().isoformat()
    transient, _ = classify(root)
    if not transient:
        return []

    attic_dir = os.path.join(root, ATTIC) if dry_run else _open_attic(root)
    moved, claimed = [], set()

    for rel, why in transient:
        target = attic_name(attic_dir, rel, claimed)
        claimed.add(target)
        dest_rel = "%s/%s" % (ATTIC, target)
        if not dry_run:
            shutil.move(os.path.join(root, rel), os.path.join(attic_dir, target))
            # The line records WHY this page moved, in the evidence the rule actually read, so a
            # reader of the manifest can tell one page's grounds from another's (SPEC INV-7).
            _record(attic_dir, "- `%s` -> `%s` * a rendered page whose reading is over: %s * %s"
                               % (rel, dest_rel, why, today))
        moved.append((rel, dest_rel))

    return moved


def declaration(moved, dry_run=False):
    """The line the sweep says out loud — what moved, and where it comes back from."""
    if not moved:
        return "No rendered page is waiting to be cleared; every page in the tree is an artifact."
    verb = "would clear" if dry_run else "cleared"
    names = ", ".join(src for src, _ in moved)
    return ("%s %d rendered page%s to attic/: %s. Each rests in the attic and comes back from "
            "there if it turns out to be needed (SPEC INV-286, base rule 10)."
            % (verb, len(moved), "" if len(moved) == 1 else "s", names))


def main(argv=None):
    parser = argparse.ArgumentParser(description="clear the rendered pages whose reading is over")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    try:
        moved = sweep(root, dry_run=args.dry_run)
    except (OSError, RuntimeError) as err:
        print("sweep-rendered: halted — %s" % err)
        print("  Every page moved before this point carries its own manifest line in "
              "%s/%s." % (ATTIC, MANIFEST))
        return 1

    print(declaration(moved, dry_run=args.dry_run))
    for src, dest in moved:
        print("  %s -> %s" % (src, dest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
