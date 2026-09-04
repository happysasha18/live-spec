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

Two poles, one check. A `VERSION` file is not this pack's own property — an ordinary host project
carries one too — so it is the wrong question and is not asked. When the repo being checked itself
carries the shipped source, `scaffold/status-view/state-probe.sh`, it IS the pack: the one pair
Requirement 319 criteria 1 and 2 actually claim byte-identity for is compared directly, and no
manifest is needed (the pack is not a host of itself). A host carries the vendored copy and no
`scaffold/` kit of its own, so this test never fires for one. Not the whole of either scaffold kit:
`scaffold/status-view/plan_checks.py` is a seed a host fills with its own commands and is never
pinned against the pack's own `scripts/plan_checks.py`, and `scaffold/guardrails/` is
install-scaffold.sh's own kit for a host's `guardrails/`, under INV-177 — the pack carries no
same-named files there to compare against. Otherwise the repo is a host, and the pack is located
by --pack-root; else by the
`pack_root` key adopt/install-status-view.sh records in this host's own ratchet-manifest.json at
install time; else the directory this script itself lives in, two levels up (a loose invocation
with neither). A machine with no readable pack there — no VERSION file at that root — has nothing
to diff against; the check stands down with one honest line and exits 0, the shape
scripts/check-pack-update.sh already uses for an unreachable pack.

Usage:
  check-status-view-drift.py [HOST_ROOT] [--pack-root PACK_ROOT]
    HOST_ROOT     the repo to check (default: the current repo root, via `git rev-parse
                  --show-toplevel`, else the current directory). The pack's own pair is checked
                  when HOST_ROOT itself carries the shipped source; otherwise HOST_ROOT is read as
                  a host.
Exit 0 when the pack is not on this machine, a host carries no manifest, or every resolvable
vendored copy matches its pack source byte-for-byte; exit 1 naming each file that differs. A
comparison that resolves zero pairs never exits 0 with the ordinary pass line — it names the zero
count instead. Stdlib only.
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


# The one pair Requirement 319 criteria 1 and 2 actually claim byte-identity for — not every
# same-named file under the two scaffold kits. scaffold/status-view/plan_checks.py is a seed a
# host fills in with its own commands and is never meant to match the pack's own
# scripts/plan_checks.py (never pinned in any manifest, by design); scaffold/guardrails/ is
# install-scaffold.sh's own kit for a HOST's guardrails/ directory, under INV-177, a separate,
# pre-existing mechanism this requirement does not touch — the pack carries no same-named files
# under its own guardrails/ to compare against. Widening the scan to "every file under either
# scaffold kit" read both of those as drift the first time it ran against this repo.
_PACK_SELF_PAIR = ("scaffold/status-view/state-probe.sh", "scripts/state-probe.sh")


def _is_pack_root(root):
    """`root` IS the pack when it carries the shipped source itself — the thing a VERSION file
    does not name, since an ordinary host project carries one too (R1)."""
    src_rel, _ = _PACK_SELF_PAIR
    return os.path.isfile(os.path.join(root, src_rel))


def _shipped_pairs(root):
    """The pack's own self-pair, when its source half exists under `root` — used only when
    `root` IS the pack, so the pair is compared directly with no manifest needed to say what
    should match."""
    src_rel, dst_rel = _PACK_SELF_PAIR
    if os.path.isfile(os.path.join(root, src_rel)):
        return [(src_rel, dst_rel)]
    return []


def _finish(checked, faults, target):
    """A comparison that opened zero pairs must never read as a clean pass (R1's general form —
    it matters more than the discriminator above). Print a distinct stand-down naming that instead
    of the ordinary pass line."""
    if faults:
        print("%s: %d vendored file(s) drifted from the pack:" % (CHECK, len(faults)))
        for line in faults:
            print("  %s" % line)
        return 1
    if checked == 0:
        print("%s: compared 0 vendored file(s) against %s — nothing resolved to check, standing "
              "down" % (CHECK, target))
        return 0
    print("%s: %d vendored file(s) checked against %s — no drift" % (CHECK, checked, target))
    return 0


def _compare(pairs, root):
    """Compare every (src_rel, dst_rel) pair's bytes under one root (the pack pole: src and dst
    both live in the same tree). Returns (checked, faults); a pair whose dst file is missing
    counts as a fault too, named the same way a drifted byte is."""
    faults = []
    checked = 0
    for src_rel, dst_rel in pairs:
        src_path = os.path.join(root, src_rel)
        if not os.path.isfile(src_path):
            continue  # not a file this tree carries — not this check's to judge
        dst_path = os.path.join(root, dst_rel)
        checked += 1
        if not os.path.isfile(dst_path):
            faults.append("%s is missing — re-run adopt/install-status-view.sh --force, or move "
                          "the change into the pack" % dst_rel)
            continue
        if _sha256(dst_path) != _sha256(src_path):
            faults.append("%s differs from the pack's own copy — re-run "
                          "adopt/install-status-view.sh --force, or move the change into the pack"
                          % dst_rel)
    return checked, faults


def main(argv):
    ap = argparse.ArgumentParser(prog=CHECK, add_help=True)
    ap.add_argument("host_root", nargs="?", default=None)
    ap.add_argument("--pack-root", default=None)
    args = ap.parse_args(argv)

    host_root = os.path.abspath(args.host_root or _default_host_root())

    # Pole 1: the repo being checked IS the pack — it carries the shipped source itself, not
    # merely a VERSION file (R1: an ordinary host project carries one of those too). No manifest
    # is needed — a manifest is a HOST's bookkeeping, and the pack is not a host of itself —
    # Requirement 319 criterion 2's byte-identity is proved directly against the shipped vendor
    # map, pair by pair (F1: before this, the pack carried no ratchet-manifest.json, so this
    # check compared zero files on every push from this repository).
    if _is_pack_root(host_root):
        checked, faults = _compare(_shipped_pairs(host_root), host_root)
        return _finish(checked, faults, host_root)

    # Pole 2: a host. Locate the pack: --pack-root wins when given; else the pack root
    # adopt/install-status-view.sh recorded in this host's own manifest at install time (F2);
    # else the two-levels-up default, kept for a bare invocation with neither. A recorded or
    # defaulted root this machine does not actually carry a pack at is the honest "not reachable
    # from this machine" stand-down, never an error.
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

    pack_root = os.path.abspath(
        args.pack_root or manifest.get("pack_root")
        or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if not os.path.isfile(os.path.join(pack_root, "VERSION")):
        print("%s: no live-spec pack checkout found at %s — nothing to diff against, standing "
              "down (pass --pack-root to point at one)" % (CHECK, pack_root))
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

    return _finish(checked, faults, pack_root)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
