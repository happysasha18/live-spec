#!/usr/bin/env python3
"""progress-report.py — one document, the same shape every run: docs/PROGRESS.md.

WHY IT EXISTS. Two promises govern this repository: a reader gets through a document without
stopping, and the specification stops growing. Progress on both is reported by hand today, in
whatever shape the reporting session happens to reach for, so a person comparing two days compares
layouts before they compare numbers. This script fixes the shape. It never invents a number: every
cell comes from a live measurement taken this run, or from `guardrails/progress-baseline.json`, a
small seed file recording what was true at named past moments.

WHAT IT NEVER DOES. It never re-runs the slow per-file census (`scripts/rule-census.py` reading
every live document against the style and register lints) — that record already lives in
`guardrails/rule-census.json`, written by a run that already paid that cost, and this script reads
it rather than paying it again. Where a number has no source — no live measurement and no baseline
entry — the cell reads "not stated", never a zero standing in for an absence.

THE SIX SECTIONS, in the fixed order this document always carries:
  1. Where the two promises stand — two sentences, one per promise, each carrying one live number.
  2. The queue, in the plan's order — one table per priority group, held in
     `guardrails/progress-baseline.json` rather than re-derived here.
  3. Promise one (comprehension): Table A, the whole-repository counts; Table B, the fifteen
     documents carrying the most findings.
  4. Promise two (the spec stops growing): Table C, the spec's own size measures against the
     format-change baseline and each measure's recorded ceiling.
  5. Readings run so far: one row per file under `docs/language-reads/`.
  6. What no measure here covers: a short, fixed list of the holes, held in this script.

Usage: python3 scripts/progress-report.py [--out PATH]
Writes docs/PROGRESS.md, or PATH when --out is given (a test-only escape hatch so the suite can
point a run at a scratch file instead of the tracked page; the real regeneration road never
passes it). Stdlib only.
"""
import argparse
import datetime
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GUARDRAILS = os.path.join(REPO_ROOT, "guardrails")
sys.path.insert(0, GUARDRAILS)
import specformat as sf  # noqa: E402

NOT_STATED = "not stated"

SPEC_PATH = os.path.join(REPO_ROOT, "PRODUCT_SPEC.md")
RULE_CENSUS_PATH = os.path.join(GUARDRAILS, "rule-census.json")
BASELINE_PATH = os.path.join(GUARDRAILS, "progress-baseline.json")
SPEC_RATCHET_PATH = os.path.join(GUARDRAILS, "spec-ratchet.json")
DOC_BOUNDS_PATH = os.path.join(GUARDRAILS, "doc-bounds.json")
SPEC_DEBT_CAP_PATH = os.path.join(SCRIPT_DIR, "spec-debt-cap.json")
REDUNDANCY_SCRIPT = os.path.join(SCRIPT_DIR, "spec-redundancy-precheck.py")
SIZE_RATCHET_SCRIPT = os.path.join(GUARDRAILS, "check-size-ratchet.py")
READS_DIR = os.path.join(REPO_ROOT, "docs", "language-reads")
OUT_PATH = os.path.join(REPO_ROOT, "docs", "PROGRESS.md")

WORD_NUMBERS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen", "twenty"]
WORD_TO_NUM = {w: i for i, w in enumerate(WORD_NUMBERS)}

READ_FILENAME_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-read(\d+)-(.+)\.md$')
STOPS_COUNT_RE = re.compile(r'Stops:\s*\d+\s*[—-]\s*(\d+)\s*blocking')
STOPS_ALL_RE = re.compile(r'Stops:\s*(\d+),\s*all blocking')
FLOOR_SAT_RE = re.compile(r'floor sat at\s+(' + "|".join(WORD_NUMBERS) + r')\s+blocking\s+stops',
                           re.IGNORECASE)
BACKTICK_RE = re.compile(r'`([^`]+)`')
READ_TOP_LINES = 20        # how far down a record's blocking count is read from
READ_PATH_LINES = 25       # how far down a record's real text-read path is read from


# ---------------------------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_module(path, name):
    """Import a hyphenated script file as a module, the way check-doc-findings-bound.py does, so
    this report reuses the gate's own counting instead of re-implementing it."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------------------------
# Live measurements
# ---------------------------------------------------------------------------------------------

def measure_spec():
    """PRODUCT_SPEC.md's own size, counted the way check-size-ratchet.py counts a document: bytes,
    lines, words directly; requirements and criteria through specformat.parse, the one shared
    reader the format's seven gates already use."""
    text = read_text(SPEC_PATH)
    doc = sf.parse(text)
    ratchet = load_module(SIZE_RATCHET_SCRIPT, "check_size_ratchet")
    crit_bytes, crit_count = ratchet.bytes_per_criterion(doc)
    return {
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "words": len(text.split()),
        "requirements": len(doc.requirements),
        "acceptance_criteria": len(doc.criteria),
        "bytes_per_criterion": (crit_bytes / crit_count) if crit_count else None,
    }


def measure_redundancy_open():
    """The pairs-stating-one-fact-twice count, from spec-redundancy-precheck.py's own JSON
    tail line — the live measurement, run once per report."""
    proc = subprocess.run([sys.executable, REDUNDANCY_SCRIPT, SPEC_PATH],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    try:
        record = json.loads(lines[-1])
    except ValueError:
        return None
    return record.get("open")


def live_document_paths():
    """The true live set, from rule-census.py's own file walk — a directory listing, not the slow
    per-file lint measurement, so this stays cheap to call on every run."""
    census = load_module(os.path.join(SCRIPT_DIR, "rule-census.py"), "rule_census")
    return set(census.live_files(REPO_ROOT))


# ---------------------------------------------------------------------------------------------
# The rule-census record (read, not re-measured)
# ---------------------------------------------------------------------------------------------

def load_rule_census():
    record = load_json(RULE_CENSUS_PATH)
    return record.get("files", {}), record.get("cap"), record.get("cap_rule")


# ---------------------------------------------------------------------------------------------
# docs/language-reads/*.md — the reading records
# ---------------------------------------------------------------------------------------------

def parse_read_record(path):
    """One docs/language-reads/<date>-read<N>-<slug>.md file, parsed for its date, its reading
    number and slug (from the filename, per the fixed naming law), the blocking-stop count it
    states near its top, and the real repository path it names as the text it read."""
    fn = os.path.basename(path)
    m = READ_FILENAME_RE.match(fn)
    if not m:
        return None
    date, num, slug = m.group(1), int(m.group(2)), m.group(3)
    lines = read_text(path).splitlines()

    top_text = " ".join(lines[:READ_TOP_LINES])
    blocking = None
    for pat in (STOPS_COUNT_RE, STOPS_ALL_RE, FLOOR_SAT_RE):
        mm = pat.search(top_text)
        if mm:
            g = mm.group(1)
            blocking = int(g) if g.isdigit() else WORD_TO_NUM[g.lower()]
            break

    doc_path = None
    for line in lines[:READ_PATH_LINES]:
        for cand in BACKTICK_RE.findall(line):
            cand = cand.strip()
            if cand.startswith("/"):
                continue  # an absolute path is a scratch copy, never the repository's own file
            if os.path.isfile(os.path.join(REPO_ROOT, cand)):
                doc_path = cand
                break
        if doc_path:
            break

    return {"date": date, "num": num, "slug": slug, "blocking": blocking, "doc_path": doc_path,
            "filename": fn}


def load_all_reads():
    paths = sorted(glob.glob(os.path.join(READS_DIR, "*.md")))
    records = [parse_read_record(p) for p in paths]
    return [r for r in records if r is not None]


def documents_passed(reads):
    """A document passes when its two highest-numbered readings both state zero blocking stops
    (the rule the brief states outright). Grouped by slug, since one slug names one document
    across this record set."""
    by_slug = {}
    for r in reads:
        by_slug.setdefault(r["slug"], []).append(r)
    passed = 0
    for slug, group in by_slug.items():
        group_sorted = sorted(group, key=lambda r: r["num"])
        top_two = group_sorted[-2:]
        if len(top_two) == 2 and all(r["blocking"] == 0 for r in top_two):
            passed += 1
    return passed


def readings_for_doc_path(reads, doc_path):
    return [r for r in reads if r["doc_path"] == doc_path]


def doc_passed(reads, doc_path):
    group = sorted(readings_for_doc_path(reads, doc_path), key=lambda r: r["num"])
    top_two = group[-2:]
    return len(top_two) == 2 and all(r["blocking"] == 0 for r in top_two)


# ---------------------------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------------------------

def target_val(baseline, key):
    """The recorded target for one measure, read from `guardrails/progress-baseline.json`'s
    `targets` block. A measure the file does not hold prints "not stated", never a guess."""
    return baseline.get("targets", {}).get(key, {}).get("value", NOT_STATED)


def fmt(n, decimals=None):
    if n is None:
        return NOT_STATED
    if isinstance(n, float):
        return ("%.1f" % n) if decimals is None else ("%.*f" % (decimals, n))
    return "{:,}".format(n)


def fmt_pct(n):
    if n is None:
        return NOT_STATED
    return "%.1f%%" % n


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------------------------

WHAT_NO_MEASURE_COVERS = [
    "The register lint prints no count field for a caught leak. A cold read once found a real "
    "finding scored as zero because of that gap.",
    "A near-duplicate pair with disjoint vocabulary needs a language-model judge, spec-judge.py, "
    "which this report does not run.",
    "A document at zero recorded findings has not necessarily cleared a cold read. The mechanical "
    "census and the reader bar measure two different things.",
    "Table B's readings-run count only finds a reading record when that record states a real "
    "repository path near its top. An informal read leaves no trace here.",
    "A document with no entry under docs/language-reads/ carries no reading history in this page, "
    "whether or not anyone has read it informally.",
]


def build_section1(census_files, spec_measure, findings_total, doc_bounds):
    max_bytes = doc_bounds.get("PRODUCT_SPEC.md", {}).get("max_bytes")
    s1 = ("Promise one, a reader gets through a document without stopping, measures %s open "
          "writing findings across the live set today." % fmt(findings_total))
    s2 = ("Promise two, the specification stops growing, measures PRODUCT_SPEC.md at %s bytes "
          "against its %s-byte ceiling today."
          % (fmt(spec_measure["bytes"]), fmt(max_bytes) if max_bytes else NOT_STATED))
    return s1, s2


def build_table_a(census_files, baseline, reads, live_paths):
    live_count = len(census_files)
    findings_total = sum(v.get("total", 0) for v in census_files.values())
    zero_count = sum(1 for v in census_files.values() if v.get("total", 0) == 0)
    passed_count = documents_passed(reads)

    night = baseline.get("findings_2026_07_29_night", {})
    recorded_docs = night.get("documents")
    recorded_findings = night.get("total_findings")
    recorded_zero = night.get("zero_findings_documents")

    rows = [
        ["live documents measured", fmt(live_count), fmt(recorded_docs),
         target_val(baseline, "live documents measured")],
        ["writing findings across all documents", fmt(findings_total), fmt(recorded_findings),
         target_val(baseline, "writing findings across all documents")],
        ["documents at zero findings", fmt(zero_count), fmt(recorded_zero),
         target_val(baseline, "documents at zero findings")],
        ["documents that passed two consecutive readings with nothing blocking",
         fmt(passed_count), NOT_STATED,
         target_val(baseline, "documents that passed two consecutive readings with nothing "
                    "blocking")],
    ]
    return rows, {"live_count": live_count, "findings_total": findings_total,
                  "zero_count": zero_count, "passed_count": passed_count}


def build_table_b(census_files, reads):
    top15 = sorted(census_files.items(), key=lambda kv: -kv[1].get("total", 0))[:15]
    rows = []
    for path, v in top15:
        run = readings_for_doc_path(reads, path)
        passed = "yes" if doc_passed(reads, path) else "no"
        rows.append([
            "`%s`" % path,
            fmt(v.get("total", 0)),
            fmt(v.get("long", 0)),
            fmt(v.get("style", 0)),
            fmt(v.get("longest", 0)),
            fmt(len(run)),
            passed,
        ])
    return rows


def build_table_c(spec_measure, baseline, ratchet_bound, max_bytes, redundancy_open, debt_cap):
    fc = baseline.get("format_change_2026_07_23", {})
    fc_bytes = fc.get("bytes")
    fc_req = fc.get("requirements")
    fc_ac = fc.get("acceptance_criteria")
    fc_redundancy = baseline.get("redundancy_pairs", {}).get(
        "before_format_change", {}).get("value")

    today_share = (100.0 * spec_measure["bytes"] / max_bytes) if max_bytes else None
    fc_share = (100.0 * fc_bytes / max_bytes) if (max_bytes and fc_bytes is not None) else None

    rows = [
        ["bytes", fmt(spec_measure["bytes"]), fmt(fc_bytes), fmt(max_bytes),
         target_val(baseline, "bytes")],
        ["lines", fmt(spec_measure["lines"]), NOT_STATED, NOT_STATED,
         target_val(baseline, "lines")],
        ["words", fmt(spec_measure["words"]), NOT_STATED, NOT_STATED,
         target_val(baseline, "words")],
        ["requirements", fmt(spec_measure["requirements"]), fmt(fc_req), NOT_STATED,
         target_val(baseline, "requirements")],
        ["acceptance criteria", fmt(spec_measure["acceptance_criteria"]), fmt(fc_ac), NOT_STATED,
         target_val(baseline, "acceptance criteria")],
        ["bytes per criterion", fmt(spec_measure["bytes_per_criterion"], decimals=1), NOT_STATED,
         fmt(ratchet_bound, decimals=1), target_val(baseline, "bytes per criterion")],
        ["pairs stating one fact twice", fmt(redundancy_open), fmt(fc_redundancy),
         fmt(debt_cap), target_val(baseline, "pairs stating one fact twice")],
        ["share of the byte ceiling used", fmt_pct(today_share), fmt_pct(fc_share), NOT_STATED,
         NOT_STATED],
    ]
    return rows


# ---------------------------------------------------------------------------------------------
# The queue, in the plan's order
# ---------------------------------------------------------------------------------------------

PRIORITY_NOTE_1 = ("The order below comes from `docs/plans/2026-07-28-two-goals-one-campaign.md`, "
                    "the section \"The order of documents\".")
PRIORITY_NOTE_2 = ("Three members carry no entry in the findings record: "
                    "`hooks/chat-law-hook.sh` and two files outside this repository, "
                    "`~/.claude/CLAUDE.md` and `~/.claude/live-spec/profile.md`. Their findings "
                    "column reads not measured.")


def resolve_group_ten(used_paths, census_files):
    """Every live document the nine named groups leave out, worst first. Ties break by path, so
    two runs over the same census agree on order."""
    remaining = [p for p in census_files if p not in used_paths]
    remaining.sort(key=lambda p: (-census_files[p].get("total", 0), p))
    return remaining


def build_priority(baseline, census_files, reads):
    """The ten groups from `guardrails/progress-baseline.json`'s `priority` block, group ten's
    members resolved live, and one row per member carrying its findings, its two clean states,
    and its queue state. The first unfinished row in queue order is "in hand"; every other
    unfinished row is "waiting"."""
    groups_def = baseline.get("priority", {}).get("groups", [])
    fixed = [g for g in groups_def if g.get("number") != 10]
    used = {p for g in fixed for p in g.get("members", [])}
    ten_def = next((g for g in groups_def if g.get("number") == 10), None)
    ten_title = ten_def["title"] if ten_def else "Every remaining live document, worst first"
    groups = fixed + [{"number": 10, "title": ten_title,
                       "members": resolve_group_ten(used, census_files)}]
    groups.sort(key=lambda g: g["number"])

    flat = [(g["number"], path) for g in groups for path in g["members"]]

    rows, in_hand_assigned = [], False
    for idx, (gnum, path) in enumerate(flat, start=1):
        entry = census_files.get(path)
        if entry is None:
            findings, measured_clean = "not measured", "not measured"
        else:
            findings = fmt(entry.get("total", 0))
            measured_clean = "yes" if entry.get("total", 0) == 0 else "no"
        read_clean = "yes" if doc_passed(reads, path) else "no"
        finished = measured_clean == "yes" and read_clean == "yes"
        if finished:
            state = "finished"
        elif not in_hand_assigned:
            state, in_hand_assigned = "in hand", True
        else:
            state = "waiting"
        rows.append({"idx": idx, "group": gnum, "path": path, "findings": findings,
                     "measured_clean": measured_clean, "read_clean": read_clean, "state": state})
    return groups, rows


def render_priority_section(groups, rows):
    by_group = {}
    for r in rows:
        by_group.setdefault(r["group"], []).append(r)

    out = [PRIORITY_NOTE_1, "", PRIORITY_NOTE_2, ""]
    for g in groups:
        out.append("### %d. %s" % (g["number"], g["title"]))
        out.append("")
        table_rows = [[str(r["idx"]), "`%s`" % r["path"], r["findings"], r["measured_clean"],
                       r["read_clean"], r["state"]] for r in by_group.get(g["number"], [])]
        out.append(md_table(["#", "document", "findings today", "measured clean", "read clean",
                              "state"], table_rows))
        out.append("")
    return out


def build_section4(reads):
    ordered = sorted(reads, key=lambda r: (r["date"], r["num"]))
    rows = []
    for r in ordered:
        blocking = fmt(r["blocking"]) if r["blocking"] is not None else NOT_STATED
        rows.append([r["date"], r["slug"].replace("-", " "), fmt(r["num"]), blocking])
    return rows


# ---------------------------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------------------------

def render(now, census_files, cap, cap_rule, spec_measure, baseline, ratchet_bound, max_bytes,
           redundancy_open, debt_cap, reads, live_paths):
    findings_total = sum(v.get("total", 0) for v in census_files.values())
    s1, s2 = build_section1(census_files, spec_measure, findings_total,
                             load_json(DOC_BOUNDS_PATH)["docs"])
    table_a, _ = build_table_a(census_files, baseline, reads, live_paths)
    table_b = build_table_b(census_files, reads)
    table_c = build_table_c(spec_measure, baseline, ratchet_bound, max_bytes, redundancy_open,
                             debt_cap)
    table_d = build_section4(reads)
    priority_groups, priority_rows = build_priority(baseline, census_files, reads)

    out = []
    out.append("# Progress — the two promises")
    out.append("")
    out.append("Generated %s by `python3 scripts/progress-report.py`, reading the tree as it "
                "stands today." % now)
    out.append("")
    out.append("## Where the two promises stand")
    out.append("")
    out.append(s1)
    out.append("")
    out.append(s2)
    out.append("")
    out.append("## The queue, in the plan's order")
    out.append("")
    out.extend(render_priority_section(priority_groups, priority_rows))
    out.append("## Promise one — a reader gets through a document without stopping")
    out.append("")
    out.append("The counts below come from the record `guardrails/rule-census.json`. It states "
                "when each document was last measured.")
    out.append("")
    out.append(md_table(["measure", "today", "recorded before", "target"], table_a))
    out.append("")
    out.append("The fifteen documents carrying the most findings:")
    out.append("")
    out.append(md_table(["document", "findings", "of which long sentences", "style",
                          "longest sentence", "readings run", "passed"], table_b))
    out.append("")
    out.append("## Promise two — the specification stops growing")
    out.append("")
    out.append(md_table(["measure", "today", "at the format change, 2026-07-23", "ceiling",
                          "target"], table_c))
    out.append("")
    out.append("## Readings run so far")
    out.append("")
    out.append(md_table(["date", "document read", "reading number", "blocking stops left"],
                         table_d))
    out.append("")
    out.append("## What no measure covers")
    out.append("")
    for item in WHAT_NO_MEASURE_COVERS:
        out.append(item)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=OUT_PATH,
                         help="write here instead of docs/PROGRESS.md (test-only; the real "
                              "regeneration road never passes this)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    census_files, cap, cap_rule = load_rule_census()
    baseline = load_json(BASELINE_PATH)
    spec_measure = measure_spec()
    ratchet_bound = load_json(SPEC_RATCHET_PATH).get("bytes_per_criterion")
    doc_bounds = load_json(DOC_BOUNDS_PATH)
    max_bytes = doc_bounds.get("docs", {}).get("PRODUCT_SPEC.md", {}).get("max_bytes")
    redundancy_open = measure_redundancy_open()
    debt_cap = load_json(SPEC_DEBT_CAP_PATH).get("max_redundancy_open", {}).get(
        "PRODUCT_SPEC.md")
    reads = load_all_reads()
    live_paths = live_document_paths()

    now = datetime.date.today().isoformat()
    text = render(now, census_files, cap, cap_rule, spec_measure, baseline,
                   ratchet_bound, max_bytes, redundancy_open, debt_cap, reads, live_paths)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    print("progress-report: wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
