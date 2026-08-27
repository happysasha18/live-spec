#!/usr/bin/env python3
"""trace-phrase extract — the mechanical safety gate for the SPEC-humanize migration.

A *traceability check-phrase* is a verbatim prose literal the test suite asserts a section still
carries; this tool derives them live so a section rewrite can be proven lossless. (Filename kept for the
dated records that reference it; the vocabulary is plain: "check-phrase", never the old "needle".)

Direction matters (Fable MUST-FIX 2): we match the traceability suite's verbatim prose literals
AGAINST a section, never grep the section's prose for fragments. And the check is SECTION-SCOPED
(Fable MUST-FIX 1): a check-phrase the OLD section carried must still live in the NEW section — a copy
surviving elsewhere in the doc does NOT excuse dropping it here.

The registry is `tests/test_traceability.py` (+ any skill doc that echoes a clause; pass extra files
with --also). No copy of the check-phrases is kept anywhere — this script derives them live, so the
tests stay the one home.

Flow per batch:
  1. BEFORE editing:  needle-extract.py --section "What live-spec is" --capture /tmp/nx.json
  2. edit PRODUCT_SPEC.md
  3. AFTER editing:   needle-extract.py --section "What live-spec is" --verify /tmp/nx.json
     -> exit 0 and "OK: N check-phrases preserved"  |  exit 1 and the list of DROPPED check-phrases.

Also: --list dumps every check-phrase the current section carries; --between A B uses a line range
instead of a heading name (for sections whose heading text you don't want to type).
"""
import ast, re, sys, os, json, argparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(REPO, "tests", "test_traceability.py")
SPEC = os.path.join(REPO, "PRODUCT_SPEC.md")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def registry_literals(extra_files):
    """Every plain, prose-like string constant in the traceability suite (+ any --also file).

    Conservative on purpose: over-collecting is safe (we only ever ASSERT a phrase we kept stays),
    under-collecting drops a check-phrase. So we take every string constant that reads like prose and
    skip only format strings / anchors / paths.
    """
    lits = set()
    for path in [TESTS] + list(extra_files):
        try:
            tree = ast.parse(open(path).read())
        except (SyntaxError, FileNotFoundError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                v = norm(node.value)
                # >= 8 chars: the floor separating a prose-like check phrase from an identifier or a
                # fragment. It is the weaker of the two conditions here — the `" " in v` beside it is
                # what actually requires a phrase, since any two-word string already clears 8 chars
                # in practice. No incident or source behind the 8 (the 2026-08-07 census, row 67,
                # found no trace); an engineering default, and a redundant one at that.
                if len(v) >= 8 and " " in v and "%" not in v and "\\" not in v:
                    lits.add(v)
    return lits


def section_text(name=None, between=None):
    lines = open(SPEC).read().split("\n")
    if between:
        return "\n".join(lines[between[0] - 1:between[1]])
    out, grab = [], False
    for ln in lines:
        if ln.startswith("## "):
            if grab:
                break
            grab = norm(ln[3:]) == norm(name)
            continue
        if grab:
            out.append(ln)
    return "\n".join(out)


def trace_phrases_in(text, extra_files):
    body = norm(text)
    return sorted(p for p in registry_literals(extra_files) if p in body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section")
    ap.add_argument("--between", nargs=2, type=int)
    ap.add_argument("--also", nargs="*", default=[], help="extra registry files (skill docs echoing a clause)")
    ap.add_argument("--capture", metavar="PATH")
    ap.add_argument("--verify", metavar="PATH")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    text = section_text(name=args.section, between=tuple(args.between) if args.between else None)
    if not text.strip():
        print("ERROR: empty section — check the heading text / line range", file=sys.stderr)
        return 2
    current = trace_phrases_in(text, args.also)

    if args.capture:
        json.dump(current, open(args.capture, "w"), ensure_ascii=False, indent=0)
        print("captured %d check-phrases -> %s" % (len(current), args.capture))
        return 0

    if args.verify:
        want = json.load(open(args.verify))
        body = norm(text)
        dropped = [p for p in want if p not in body]
        if dropped:
            print("DROPPED %d check-phrase(s) — the rewrite lost verbatim prose the suite asserts:" % len(dropped))
            for p in dropped:
                print("  - " + (p[:110] + ("…" if len(p) > 110 else "")))
            return 1
        print("OK: %d check-phrases preserved (section-scoped)." % len(want))
        return 0

    for p in current:
        print(p)
    print("\n(%d check-phrases in section)" % len(current), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
