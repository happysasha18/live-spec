#!/usr/bin/env python3
"""check-status-view-drift.py — a host's vendored pack files must not drift from the pack (row
q-818: the shipped status renderer had forked from the pack's own copy, and a fix to one never
reached the other).

Reads a host's scripts/ratchet-manifest.json (written by adopt/install-status-view.sh,
install-scaffold.sh and install-style-gates.sh — they share one manifest). For every entry whose
pack-relative source path resolves to a real file inside the pack, it opens BOTH that pack file and
the host's own vendored copy and compares their bytes directly. It never trusts the sha256 the
manifest carries and never trusts the manifest's word about whether a copy still matches — a
recorded hash only says what a file looked like at install time, not what it looks like now, and
matching the vendored file's own bytes is the only thing that proves the row's "done when" (the
check reads the two files, not a record about them).

Locating the host's own copy: every installer today vendors either at the same relative path the
pack uses, or at a fixed destination under one of two `scaffold/` kits
(`scaffold/status-view/<name>` -> `scripts/<name>`, `scaffold/guardrails/<name>` -> `guardrails/<name>`,
per adopt/install-status-view.sh and adopt/install-scaffold.sh); this check applies that same,
already-shipped mapping rather than inventing a new one.

Locating the pack: --pack-root, else the directory this script itself lives in, two levels up (the
pack root when this copy is the pack's own; a host's vendored copy defaults to its own root, which
carries no VERSION file, so it falls into the stand-down below rather than comparing a host against
itself). A machine with no readable pack there — no VERSION file at that root — has nothing to
diff against; the check stands down with one honest line and exits 0, the shape
scripts/check-pack-update.sh already uses for an unreachable pack.

Usage:
  check-status-view-drift.py [HOST_ROOT] [--pack-root PACK_ROOT]
    HOST_ROOT     the host repo to check (default: the current repo root, via `git rev-parse
                  --show-toplevel`, else the current directory).
Exit 0 when the pack is not on this machine, the host carries no manifest, or every resolvable
vendored copy matches its pack source byte-for-byte; exit 1 naming each file that differs. Stdlib
only.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

CHECK = "check-status-view-drift"

# The two known scaffold-kit destinations (adopt/install-status-view.sh, adopt/install-scaffold.sh).
# Every other vendored entry lands at the same relative path in the host as in the pack.
_SCAFFOLD_DESTS = (
    ("scaffold/status-view/", "scripts/"),
    ("scaffold/guardrails/", "guardrails/"),
)


def _host_rel(pack_rel):
    for prefix, dest in _SCAFFOLD_DESTS:
        if pack_rel.startswith(prefix):
            return dest + pack_rel[len(prefix):]
    return pack_rel


def _default_host_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return os.getcwd()


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main(argv):
    ap = argparse.ArgumentParser(prog=CHECK, add_help=True)
    ap.add_argument("host_root", nargs="?", default=None)
    ap.add_argument("--pack-root", default=None)
    args = ap.parse_args(argv)

    host_root = os.path.abspath(args.host_root or _default_host_root())
    pack_root = os.path.abspath(
        args.pack_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if not os.path.isfile(os.path.join(pack_root, "VERSION")):
        print("%s: no live-spec pack checkout found at %s — nothing to diff against, standing "
              "down (pass --pack-root to point at one)" % (CHECK, pack_root))
        return 0

    manifest_path = os.path.join(host_root, "scripts", "ratchet-manifest.json")
    if not os.path.isfile(manifest_path):
        print("%s: %s carries no scripts/ratchet-manifest.json — nothing vendored to check"
              % (CHECK, host_root))
        return 0

    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("%s: %s is unreadable (%s) — standing down" % (CHECK, manifest_path, exc))
        return 0

    vendored = manifest.get("vendored") or {}
    faults = []
    checked = 0
    for pack_rel in sorted(vendored):
        pack_path = os.path.join(pack_root, pack_rel)
        if not os.path.isfile(pack_path):
            continue  # not a file this pack checkout carries — not this check's to judge
        host_rel = _host_rel(pack_rel)
        host_path = os.path.join(host_root, host_rel)
        checked += 1
        if not os.path.isfile(host_path):
            faults.append("%s is missing — re-run adopt/install-status-view.sh --force, or move "
                           "the change into the pack" % host_rel)
            continue
        if _sha256(host_path) != _sha256(pack_path):
            faults.append("%s differs from the pack's own copy — re-run "
                           "adopt/install-status-view.sh --force, or move the change into the pack"
                           % host_rel)

    if faults:
        print("%s: %d vendored file(s) drifted from the pack:" % (CHECK, len(faults)))
        for line in faults:
            print("  %s" % line)
        return 1

    print("%s: %d vendored file(s) checked against %s — no drift" % (CHECK, checked, pack_root))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
