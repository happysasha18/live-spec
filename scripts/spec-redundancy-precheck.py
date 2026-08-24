#!/usr/bin/env python3
"""spec-redundancy-precheck.py — the cheap, mechanical first layer of the redundancy gate.

Regex cannot see "says the same thing twice". This does not either, fully — but it catches the CHEAP
class: near-verbatim repeats, reordered repeats, copy-paste-with-edits, and a definition restated in the
same terms. It shrinks the LLM judge's job to true paraphrase (disjoint-vocabulary) duplication. It is a
gate (open == 0, every candidate resolved or waived), not an auto-blocker on raw hits.

Method: segment the doc into sentence/bullet units; normalize each to content tokens (drop a stoplist) and
word 3-gram shingles; flag a pair as a candidate when the shorter unit has >= MIN_TOKENS content tokens and
(jaccard(shingles) >= JAC or containment(tokens) >= CON). False-positive controls: the min-length floor kills
short defined-term collisions; sibling bullets in one list go to a separate 'parallel-structure' bucket (they
are similar by design); every candidate prints both verbatim spans + line numbers for one-glance disposition.

Honest limit: it CANNOT catch paraphrase with disjoint vocabulary (e.g. "not for you to read" vs "you can
ignore them as you read" share almost no content words) — that is exactly what the LLM judge (spec-judge.py)
is for.

Usage: spec-redundancy-precheck.py [--jac F] [--con F] FILE
Exit 0 = open == 0 (clean or all waived) · exit 1 = open candidates remain.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS = os.path.join(os.path.dirname(SCRIPT_DIR), "guardrails")
sys.path.insert(0, SCRIPT_DIR)
import gate_common  # noqa: E402

# specformat.py (the core+parts reader) lives in the pack's guardrails/ dir, a sibling of scripts/.
# This script is ALSO vendored standalone into host repos by adopt/install-ratchet.sh (VENDOR_FILES),
# which does not vendor guardrails/specformat.py — a host runs style/redundancy/freeze gates on its
# own doc, with no core+parts convention assumed. So the import is optional: where specformat IS
# available (this pack's own checkout), a core file's `## Parts map` is expanded before scanning;
# where it is not (a vendored host), main() falls back to reading exactly the named file, unchanged
# from this script's behaviour before the core+parts fix.
sys.path.insert(0, GUARDRAILS)
try:
    import specformat as sf  # noqa: E402
except ImportError:
    sf = None

WAIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec-waivers.json")

# 0.60 / 0.85 / 6 kept — ruled 2026-08-15 (decision-dossier-2026-08-15.md, Number 3): matches the
# design doc's own worked reasoning (docs/prose-quality-gate-design.md), no incident traces either
# value (2026-08-07 census: "no trace found" x3); the dossier named no single recommended replacement
# value, so today's values stand. Hand-duplicated in guardrails/language-rules.json
# (thresholds.jaccard_min / containment_min / min_unit_tokens) under the same ruling. A durable,
# recorded override belongs in the settings ladder's package-defaults table
# (skills/live-spec-base/references/settings-ladder.md).
MIN_TOKENS = 6      # shorter unit must have at least this many content tokens
JAC = 0.60          # 3-gram shingle Jaccard threshold
CON = 0.85          # content-token containment threshold (|A∩B| / min(|A|,|B|))
SHARE_MIN = 3       # inverted-index: only compare pairs sharing at least this many content tokens

STOP = set("""a an the this that these those and or but nor so yet for of to in on at by with from into
onto over under as is are was were be been being it its it's they them their there here then than
each every any all some no not only also just both either neither which who whom whose what when where
while whenever wherever if unless until once because since though although whether does do did done has
have had can may might must shall will would could should one two three per via across between among
""".split())

BULLET = re.compile(r"^(\s*)[-*+]\s+")


def _tokens(raw):
    return [w for w in re.findall(r"[a-z0-9']+", raw.lower()) if w not in STOP and len(w) > 1]


def _shingles(tokens, n=3):
    if len(tokens) < n:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def _list_ids(text):
    """Map 1-based line number -> a list-run id, so sibling bullets in one contiguous list (equal
    indent) share an id. Non-bullet, non-blank lines break a run."""
    ids, run, indent = {}, 0, None
    prev_bullet = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        m = BULLET.match(raw)
        if m:
            ind = len(m.group(1))
            if not prev_bullet or ind != indent:
                run += 1
                indent = ind
            ids[lineno] = run
            prev_bullet = True
        elif not raw.strip():
            prev_bullet = prev_bullet  # a blank line inside a list keeps the run
        else:
            prev_bullet = False
            indent = None
    return ids


def find_candidates(text, jac=JAC, con=CON):
    units = gate_common.segment_units(text)
    for u in units:
        u["T"] = set(_tokens(u["raw"]))
        u["S"] = _shingles(_tokens(u["raw"]))
    list_ids = _list_ids(text)
    # inverted index on content tokens
    index = {}
    for i, u in enumerate(units):
        for t in u["T"]:
            index.setdefault(t, []).append(i)
    seen_pairs, pairs = set(), []
    for t, members in index.items():
        if len(members) < 2:
            continue
        for a_i in range(len(members)):
            for b_i in range(a_i + 1, len(members)):
                key = (members[a_i], members[b_i])
                if key in seen_pairs:
                    continue
                a, b = units[members[a_i]], units[members[b_i]]
                shared = a["T"] & b["T"]
                if len(shared) < SHARE_MIN:
                    continue
                seen_pairs.add(key)
                m = min(len(a["T"]), len(b["T"]))
                if m < MIN_TOKENS:
                    continue
                su = a["S"] | b["S"]
                j = len(a["S"] & b["S"]) / len(su) if su else 0.0
                c = len(shared) / m
                if j >= jac or c >= con:
                    metric, score = ("jaccard", round(j, 2)) if j >= jac else ("containment", round(c, 2))
                    same_list = (a["line"] in list_ids and list_ids.get(a["line"]) == list_ids.get(b["line"]))
                    pairs.append({
                        "metric": metric, "score": score,
                        "bucket": "parallel-structure" if same_list else "redundancy",
                        "a_line": a["line"], "a_text": a["raw"][:120],
                        "b_line": b["line"], "b_text": b["raw"][:120],
                    })
    pairs.sort(key=lambda p: (-p["score"], p["a_line"]))
    return pairs


def main(argv):
    args, jac, con = [], JAC, CON
    it = iter(argv[1:])
    for a in it:
        if a == "--jac":
            jac = float(next(it))
        elif a == "--con":
            con = float(next(it))
        elif not a.startswith("--"):
            args.append(a)
    if len(args) != 1:
        sys.stderr.write("usage: spec-redundancy-precheck.py [--jac F] [--con F] FILE\n")
        return 2
    src = args[0]
    if src == "-":
        text = sys.stdin.read()
    elif sf is not None:
        # Read through the core+parts mechanism (specformat.spec_paths / read_document) rather than
        # opening `src` directly: a core file carrying a `## Parts map` expands to the core followed
        # by its parts and the segmenter below sees the WHOLE document, not just the core's preamble
        # and glossary. A file with no map (or an ordinary non-core file, e.g. a matrix/*.md part) is
        # unaffected — expansion is idempotent by `spec_paths`'s own construction, so this reads
        # exactly the same bytes it always did.
        _resolved, text = sf.read_document([src])
    else:
        # Vendored standalone (no guardrails/specformat.py alongside) — read exactly the named file,
        # same as before the core+parts fix.
        text = open(src, encoding="utf-8").read()
    pairs = find_candidates(text, jac, con)

    waivers = gate_common.load_waivers(WAIVER_PATH)
    open_pairs, waived, matched = [], [], set()
    for p in pairs:
        if p["bucket"] == "parallel-structure":
            continue  # sibling bullets are similar by design — not redundancy
        w = gate_common.match_waiver("spec-redundancy", src, p["b_text"], waivers) or \
            gate_common.match_waiver("spec-redundancy", src, p["a_text"], waivers)
        if w:
            p["waiver"] = w["id"]
            waived.append(p)
            matched.add(w["id"])
        else:
            open_pairs.append(p)

    for p in open_pairs:
        print("REDUNDANCY [%s %.2f]  lines %d & %d:" % (p["metric"], p["score"], p["a_line"], p["b_line"]))
        print("    a: %s" % p["a_text"])
        print("    b: %s" % p["b_text"])
    if waived:
        print("REDUNDANCY — WAIVED (dated debt): %d pair(s)." % len(waived))
    print('{"code":"spec-redundancy","candidates":%d,"open":%d,"waived":%d}'
          % (len(pairs), len(open_pairs), len(waived)))
    return 1 if open_pairs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
