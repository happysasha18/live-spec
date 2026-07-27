#!/usr/bin/env python3
"""spec-freeze — the meaning-preservation floor for a spec readability + compaction pass.

A rewrite that only simplifies wording must not change what a rule REQUIRES. This script freezes
the load-bearing facts of a doc BEFORE the rewrite and verifies them AFTER, so a dropped citation,
a mangled marker line, a lost number, or a moved path is caught mechanically. It is the reusable
compaction machine's Phase-0 net (docs/spec-compaction-protocol.md) and wires into the push gate.

Frozen per doc:
  - anchors: every [CODE] and [CODE kin] and range token (T-1..T-7), with OCCURRENCE COUNT — a
    dropped trailing citation mid-paragraph passes a unique-set check yet loses a rule's governing
    law, so counts (not just the set) are frozen. `kin` markers and ranges are distinct tokens.
  - markers: every line carrying a bare [target] / [default] / an H3 heading tag — structural law,
    frozen verbatim as a set of stripped lines.
  - literals: numbers-with-units, backticked paths/script names, and defined ALL-CAPS status
    vocabularies — the values a fluent rewrite can silently drift.

Usage:
  spec-freeze.py --freeze FILE...            # write .spec-freeze/<name>.json baselines
  spec-freeze.py --verify FILE...            # diff current vs baseline; exit 1 on any violation
  spec-freeze.py --verify FILE... --allow allow.json   # occurrence-count drops listed there are legal

A legal anchor-count decrease (a deleted duplicate restatement) is recorded in the allow file as
{"<doc>": {"<anchor>": <new_count>, ...}} with a reason; anything else is a hard violation.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FREEZE_DIR = os.path.join(ROOT, ".spec-freeze")

# The classes this script freezes are NOT written here. They live in spec-freeze.json beside this
# file, which docs/language-rules.md also reads at build time, so the rule a writer reads and the
# expressions this script compiles are one list and cannot drift apart. Each entry carries the
# pattern the script compiles and the same class in plain words for the page. A missing or
# unreadable home raises rather than freezing nothing: a freeze over zero classes passes on every
# drift it exists to catch.
#
# The classes, in plain words:
#   anchors         an anchor citation: [INV-141], [E-26], [T-15], [INV-28 kin]; the whole bracket
#                   body is captured, so "INV-28 kin" stays distinct from "INV-28".
#   ranges          a bare range token like T-1..T-7 (the traceability expand() depends on the syntax)
#   numbers         a literal with a unit, which a fluent rewrite drifts
#   paths           a backticked path/script token: no whitespace inside, so a giant prose span
#                   between two backticks that merely contains a slash is never captured as a "path"
#   marker_token    a bare [target] / [default] token
#   tagged_heading  an H3 heading carrying its tag or marker
LISTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec-freeze.json")


def _classes(key):
    """The {id: compiled pattern} map for one class group, or a hard failure naming the home."""
    try:
        with open(LISTS_PATH, encoding="utf-8") as f:
            entries = json.load(f)[key]
        compiled = {e["id"]: re.compile(e["pattern"]) for e in entries}
    except (OSError, ValueError, KeyError, TypeError, re.error) as e:
        raise SystemExit("spec-freeze: cannot read `%s` from scripts/spec-freeze.json (%s) — that file "
                         "is the one home of these classes and the freeze will not run without it." % (key, e))
    if not compiled:
        raise SystemExit("spec-freeze: `%s` in scripts/spec-freeze.json is empty — a freeze over no "
                         "classes catches no drift." % key)
    return compiled


_LITERALS = _classes("literal_classes")
_MARKERS = _classes("marker_lines")

ANCHOR_RE = _LITERALS["anchors"]
RANGE_RE = _LITERALS["ranges"]
NUM_UNIT_RE = _LITERALS["numbers"]
BACKTICK_PATH_RE = _LITERALS["paths"]
MARKER_TOKEN_RE = _MARKERS["marker_token"]
H3_RE = _MARKERS["tagged_heading"]


def _read(rel_or_abs):
    path = rel_or_abs if os.path.isabs(rel_or_abs) else os.path.join(ROOT, rel_or_abs)
    with open(path, encoding="utf-8") as f:
        return f.read()


def _counts(tokens):
    d = {}
    for t in tokens:
        d[t] = d.get(t, 0) + 1
    return d


def extract(text):
    lines = text.splitlines()
    anchors = _counts(ANCHOR_RE.findall(text))
    ranges = _counts(RANGE_RE.findall(text))
    # structural marker lines live in scenario prose and headings; a Formal-index table row
    # (starting "| CODE |") only DESCRIBES a rule and may mention [target]/[default] in passing,
    # so it is not a structural marker and is excluded (it is compacted, and its numbers/anchors
    # are still frozen by the other checks).
    markers = sorted({ln.strip() for ln in lines
                      if not ln.lstrip().startswith("|")
                      and (MARKER_TOKEN_RE.search(ln) or (H3_RE.match(ln) and ("[" in ln)))})
    nums = _counts(NUM_UNIT_RE.findall(text))
    paths = _counts(BACKTICK_PATH_RE.findall(text))
    return {"anchors": anchors, "ranges": ranges, "markers": markers,
            "numbers": nums, "paths": paths}


def _name(f):
    return os.path.basename(f).replace("/", "_")


def freeze(files):
    os.makedirs(FREEZE_DIR, exist_ok=True)
    for f in files:
        data = extract(_read(f))
        out = os.path.join(FREEZE_DIR, _name(f) + ".json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
        print("frozen %-24s anchors=%d ranges=%d markers=%d numbers=%d paths=%d"
              % (os.path.basename(f), len(data["anchors"]), len(data["ranges"]),
                 len(data["markers"]), len(data["numbers"]), len(data["paths"])))
    return 0


def verify(files, allow, compaction=False):
    # compaction mode: removing a DUPLICATE index row drops the redundant copies of its cross-ref
    # citations, whose law lives on in the prose clause — so a count DROP where the anchor still
    # appears (count > 0) is the intended compaction and is allowed; a VANISH (-> 0, the last copy
    # gone) or a RISE (an invented cite) is still a hard violation. Markers/numbers/paths stay strict.
    violations = []
    for f in files:
        base_path = os.path.join(FREEZE_DIR, _name(f) + ".json")
        if not os.path.exists(base_path):
            violations.append("%s: no frozen baseline (run --freeze first)" % f)
            continue
        with open(base_path, encoding="utf-8") as fh:
            base = json.load(fh)
        cur = extract(_read(f))
        allowed = (allow.get(os.path.basename(f), {}) if allow else {})

        # anchors: unique-set identical is hard; a count DROP is legal only if the allow file
        # names the anchor's new count; a count RISE or a vanished anchor is always a violation.
        b_set, c_set = set(base["anchors"]), set(cur["anchors"])
        for a in sorted(b_set - c_set):
            if allowed.get(a) == 0:
                continue
            violations.append("%s: anchor %s vanished (was %d)" % (f, a, base["anchors"][a]))
        for a in sorted(c_set - b_set):
            violations.append("%s: anchor %s INVENTED (now %d) — a rewrite adds no law"
                              % (f, a, cur["anchors"][a]))
        for a in sorted(b_set & c_set):
            bn, cn = base["anchors"][a], cur["anchors"][a]
            if cn == bn:
                continue
            if cn < bn and allowed.get(a) == cn:
                continue
            if cn < bn and compaction:      # a duplicate copy removed, the law survives in prose
                continue
            violations.append("%s: anchor %s count %d -> %d (%s)"
                              % (f, a, bn, cn, "unlogged drop" if cn < bn else "rose — invented cite"))

        # ranges / markers / numbers / paths: any change is a violation unless explicitly allowed
        for key, label in (("ranges", "range token"), ("numbers", "number/unit"), ("paths", "path")):
            b, c = base[key], cur[key]
            for t in sorted(set(b) - set(c)):
                if t in allowed.get("_drop_%s" % key, []):
                    continue
                violations.append("%s: %s %r lost (was x%d)" % (f, label, t, b[t]))
            for t in sorted(set(c) - set(b)):
                if t in allowed.get("_add_%s" % key, []):
                    continue
                violations.append("%s: %s %r appeared (x%d)" % (f, label, t, c[t]))
        b_m, c_m = set(base["markers"]), set(cur["markers"])
        for m in sorted(b_m - c_m):
            if m in allowed.get("_drop_markers", []):
                continue
            violations.append("%s: marker/heading line changed or lost: %s" % (f, m[:90]))

    if violations:
        print("SPEC-FREEZE: RED (%d violation(s))" % len(violations))
        for v in violations:
            print("  " + v)
        return 1
    print("SPEC-FREEZE: GREEN (%d file(s))" % len(files))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", nargs="+", metavar="FILE")
    ap.add_argument("--verify", nargs="+", metavar="FILE")
    ap.add_argument("--allow", metavar="allow.json")
    ap.add_argument("--compaction", action="store_true",
                    help="allow anchor-count drops where the anchor survives (a duplicate row removed)")
    args = ap.parse_args()
    if args.freeze:
        return freeze(args.freeze)
    if args.verify:
        allow = json.load(open(args.allow, encoding="utf-8")) if args.allow else {}
        return verify(args.verify, allow, compaction=args.compaction)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
