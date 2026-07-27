#!/usr/bin/env python3
"""rank-criterion-defects.py — the full offender list behind the criterion-readability ratchet.

guardrails/check-criterion-readability.py measures four reading defects over PRODUCT_SPEC.md's
acceptance criteria (long-criterion, inline-gloss, absolute-tail, anchor-noise), but it only prints
an arm's offenders when that arm's count climbs above its recorded baseline
(guardrails/criterion-readability.json, INV-288) — a quiet run on a document that has not regressed,
since nothing has risen yet. This script wants the offender list on its own terms, baseline or not:
every criterion that breaks at least one arm, ranked worst first, with the counts behind each break.

It reuses the check's own arm functions rather than re-measuring the four defects itself. Because the
check's filename carries a dash, it is loaded here with importlib.util.spec_from_file_location, and
this script calls its (module-private) arm_* functions directly instead of copying their logic — one
home for what counts as a defect stays true even when a second script reads the same corpus.

Reads: the document named on the command line, guardrails/criterion-readability.json (the four
thresholds and baselines), and guardrails/check-criterion-readability.py (the arm functions and the
shared parser, specformat.py, that module already imports).

Usage:
  rank-criterion-defects.py <document.md> [--json OUT] [--top N]
--top caps the printed table (default 40, worst first). The full ranked list is always written to
OUT as JSON when --json is given, regardless of --top. Prints a summary block after the table: total
criteria scanned, how many break at least one arm, the distribution of criteria by how many arms they
break (1 through 4), and the per-arm counts held up against the config's four recorded baselines.
Stdlib only.
"""
import importlib.util
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GUARDRAILS_DIR = os.path.join(REPO_ROOT, "guardrails")
CHECK_PATH = os.path.join(GUARDRAILS_DIR, "check-criterion-readability.py")

ARMS = ("long-criterion", "inline-gloss", "absolute-tail", "anchor-noise")


def _load_check():
    """The check module itself, loaded by path since its filename carries a dash and cannot be
    imported with a plain `import` statement. Its own sys.path insert (of the guardrails dir) runs
    as a side effect of exec_module, so its sibling imports (specformat, nonempty_input) resolve."""
    spec = importlib.util.spec_from_file_location("check_criterion_readability", CHECK_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _score(cr, crit, arms_cfg, glossary_terms):
    """One criterion's arm breaks and its three counts, using the check's own arm functions and its
    own word/aside readers — never a second measure of what those functions already decide."""
    broken = []
    if cr.arm_long_criterion(crit, arms_cfg["long-criterion"]["threshold"]):
        broken.append("long-criterion")
    if cr.arm_inline_gloss(crit, arms_cfg["inline-gloss"]["threshold"], glossary_terms):
        broken.append("inline-gloss")
    if cr.arm_absolute_tail(crit, arms_cfg["absolute-tail"]["threshold"]):
        broken.append("absolute-tail")
    if cr.arm_anchor_noise(crit, arms_cfg["anchor-noise"]["threshold"]):
        broken.append("anchor-noise")
    body = cr._plain(crit.body)
    word_count = len(cr._words(body))
    aside_count = len(cr._asides(body))
    anchor_code_count = len(crit.codes)
    return broken, word_count, aside_count, anchor_code_count


def rank(path, cr, cfg):
    """Every criterion breaking at least one arm, worst first: most arms broken, then most words.
    Returns the ranked rows, the total criteria scanned, and the per-arm counts over the whole
    document (the numbers the config's baselines are meant to hold)."""
    with open(path, encoding="utf-8") as f:
        doc = cr.sf.parse(f.read())
    terms = doc.glossary_terms
    arms_cfg = cfg["arms"]
    rows = []
    per_arm_counts = dict((name, 0) for name in ARMS)
    for crit in doc.criteria:
        broken, word_count, aside_count, anchor_code_count = _score(cr, crit, arms_cfg, terms)
        for name in broken:
            per_arm_counts[name] += 1
        if not broken:
            continue
        rows.append({
            "req_code": "R%d.%d" % (crit.req_num, crit.number),
            "line_no": crit.line_no,
            "text": crit.body,
            "arms_broken": broken,
            "word_count": word_count,
            "aside_count": aside_count,
            "anchor_code_count": anchor_code_count,
        })
    rows.sort(key=lambda r: (-len(r["arms_broken"]), -r["word_count"]))
    return rows, len(doc.criteria), per_arm_counts


def _print_table(rows, top_n):
    shown = rows[:top_n]
    print("top %d of %d offenders (most arms broken first, ties by word count):" % (len(shown), len(rows)))
    for r in shown:
        print("  %5d  %-9s  arms=%d [%s]  words=%2d asides=%d anchor_codes=%d"
              % (r["line_no"], r["req_code"], len(r["arms_broken"]), ", ".join(r["arms_broken"]),
                 r["word_count"], r["aside_count"], r["anchor_code_count"]))
        print("         %s" % r["text"])


def _print_summary(scanned, rows, per_arm_counts, cfg):
    broken_n = len(rows)
    dist = dict((k, 0) for k in (1, 2, 3, 4))
    for r in rows:
        n = len(r["arms_broken"])
        dist[n] = dist.get(n, 0) + 1
    print("")
    print("summary: %d criteria scanned, %d break at least one arm" % (scanned, broken_n))
    print("  breaking N arms: " + ", ".join("%d arm=%d" % (n, dist.get(n, 0)) for n in (1, 2, 3, 4)))
    print("  per-arm counts vs config baseline:")
    for name in ARMS:
        base = cfg["arms"][name].get("baseline")
        count = per_arm_counts[name]
        if base is not None and count == base:
            print("    %-15s %d — matches the config baseline" % (name, count))
        else:
            print("    %-15s %d — config baseline is %s (differs)" % (name, count, base))


def main(argv):
    args = []
    json_out = None
    top_n = 40
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            i += 1
            if i >= len(argv):
                print("rank-criterion-defects: --json needs a path")
                return 2
            json_out = argv[i]
        elif a == "--top":
            i += 1
            if i >= len(argv):
                print("rank-criterion-defects: --top needs a number")
                return 2
            top_n = int(argv[i])
        elif a.startswith("--"):
            print("rank-criterion-defects: unknown flag %s" % a)
            return 2
        else:
            args.append(a)
        i += 1

    if len(args) != 1:
        print("rank-criterion-defects: usage: %s <document.md> [--json OUT] [--top N]"
              % os.path.basename(argv[0]))
        return 2
    path = args[0]
    if not os.path.isfile(path):
        print("rank-criterion-defects: cannot read %s" % path)
        return 1

    cr = _load_check()
    if not os.path.isfile(cr.CONFIG_PATH):
        print("rank-criterion-defects: no config at %s" % cr.CONFIG_PATH)
        return 1
    with open(cr.CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)

    rows, scanned, per_arm_counts = rank(path, cr, cfg)

    _print_table(rows, top_n)
    _print_summary(scanned, rows, per_arm_counts, cfg)

    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump({
                "document": path,
                "scanned": scanned,
                "broken": len(rows),
                "per_arm_counts": per_arm_counts,
                "rows": rows,
            }, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("")
        print("full ranked list (%d rows) written to %s" % (len(rows), json_out))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
