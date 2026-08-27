#!/usr/bin/env python3
"""measurements-table.py — one table, one row per file, every indicator this project measures.

WHY IT EXISTS. The project states numbers about its documents in whatever shape the reporting session
reaches for. This script fixes one shape: docs/MEASUREMENTS.md, a single table in the reading queue's
order, one row per file, one column per indicator, with every explanation below the table. That table
is the source of truth for where the work stands.

WHERE EACH NUMBER COMES FROM.
  - the writing-finding columns, the longest sentence, the style column and the per-file byte
    column read "not measured" everywhere: their source, guardrails/rule-census.json (written by
    scripts/rule-census.py), retired 2026-08-21;
  - the reading columns read the dated records under docs/language-reads/, one file per reading;
  - the agreed-stop column reads the `rounds` block of guardrails/progress-baseline.json, which
    records each round's two readings and the places both readers stopped at;
  - the specification columns read PRODUCT_SPEC.md directly, counting the way
    guardrails/check-size-ratchet.py counts;
  - the repeated-pair column runs scripts/spec-redundancy-precheck.py.

A cell with no source prints `not measured`. A cell whose indicator does not apply to that file prints
an em dash.

THE HTML PAGE IS BUILT ON REQUEST, NOT ON EVERY RUN (SPEC INV-286). A number-only remeasure — the
common case, run every time a script or a round finishes — needs no page: the table's own numbers are
the source of truth, and no one is about to read them off a browser tab. Building `docs/MEASUREMENTS.html`
unconditionally on every run left a transient render standing after most runs, since most runs serve no
reading exchange at all: this one page alone carries five separate sweep entries in attic/MANIFEST.md
(2026-08-04 through 2026-08-19), every other rendered page in the project's history carrying at most two
— the evidence that this page, uniquely, was being rendered far more often than it was being read. So
the page is opt-in: pass `--html` when a person is actually about to read the numbers, and the reminder
to sweep it once that reading closes prints right there. Every other command below writes the `.md`
alone.

Usage:
  python3 scripts/measurements-table.py            writes docs/MEASUREMENTS.md only
  python3 scripts/measurements-table.py --html      also writes docs/MEASUREMENTS.html, the page to
                                                     read the table on; sweep it once the reading is
                                                     over (python3 scripts/sweep-rendered.py, SPEC INV-286)
Stdlib only.
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

# The renderer's mark, read from its one home so a page this script builds and the sweep gate that
# reads it can never disagree on the wording (same pattern scripts/sweep-rendered.py uses). Before
# this fix render_html() carried no mark at all, and check-rendered-sweep.py's evidence() fell back
# to its legacy "source .md stands beside the .html" heuristic — a heuristic gated on `git ls-files`
# succeeding, which is a strictly weaker guarantee than the mark and the one that let the CI run
# (`git -C root ls-files -- '*.html' '*.HTML'`) read docs/MEASUREMENTS.html as un-evidenced and the
# sweep gate pass green with the page standing (2026-08-19, SPEC INV-286).
try:
    _spec = importlib.util.spec_from_file_location(
        "render_doc", os.path.join(SCRIPT_DIR, "render-doc.py"))
    _rd = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_rd)
    GENERATOR = _rd.GENERATOR
except Exception:                                            # a standalone copy with no renderer
    GENERATOR = "live-spec render-doc"
ROOT = os.path.dirname(SCRIPT_DIR)
GUARDRAILS = os.path.join(ROOT, "guardrails")
sys.path.insert(0, GUARDRAILS)

CENSUS_RECORD = os.path.join(GUARDRAILS, "rule-census.json")
BASELINE = os.path.join(GUARDRAILS, "progress-baseline.json")
SPEC = os.path.join(ROOT, "PRODUCT_SPEC.md")
READS_DIR = os.path.join(ROOT, "docs", "language-reads")
OUT = os.path.join(ROOT, "docs", "MEASUREMENTS.md")

NOT_MEASURED = "not measured"
NA = "—"
SPEC_ONLY = {"PRODUCT_SPEC.md"}

READ_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-read(\d+)-(.+)\.md$")
STOPS_RE = re.compile(r"Stops:\s*(\d+)\s*[—-]\s*(\d+)\s*blocking")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_census():
    """The per-file writing-defect record, or an empty one where none ships.

    Retired 2026-08-21 alongside scripts/rule-census.py and gate aa (guardrails/check-doc-findings-
    bound.py): the census-derived columns below now read "not stated" everywhere, the same fallback
    they already use for any other file this record carries no entry for.
    """
    if not os.path.isfile(CENSUS_RECORD):
        return {"files": {}}
    return load(CENSUS_RECORD)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def readings_by_slug():
    """One entry per reading record: its date, its number, and the blocking count it states."""
    out = {}
    for path in sorted(glob.glob(os.path.join(READS_DIR, "*.md"))):
        m = READ_FILE_RE.match(os.path.basename(path))
        if not m:
            continue
        date, number, slug = m.group(1), int(m.group(2)), m.group(3)
        with open(path, encoding="utf-8") as f:
            head = " ".join(f.read().split("\n")[:25])
        stops = STOPS_RE.search(head)
        blocking = int(stops.group(2)) if stops else None
        out.setdefault(slug, []).append({"date": date, "n": number, "blocking": blocking})
    for slug in out:
        out[slug].sort(key=lambda r: r["n"])
    return out


def spec_numbers():
    """The specification's own counts, taken the way the size gate takes them."""
    try:
        import specformat as sf
        text = open(SPEC, encoding="utf-8").read()
        doc = sf.parse(text)
        ratchet = load_module(os.path.join(GUARDRAILS, "check-size-ratchet.py"), "csr")
        crit_bytes, crit_count = ratchet.bytes_per_criterion(doc)
        # The bound is READ from the live ratchet record, never copied here. A hand-copied bound goes
        # stale the moment the ratchet moves: this table published 207.2 while the record had moved
        # through 185.4, 185.6 and 185.8 — the same staleness the 2026-08-07 census called a plain bug
        # (docs/audits/2026-08-07-number-census.md, rows 53/54), whose recorded fix was to read the
        # live record itself so the copied number cannot go stale again.
        with open(os.path.join(GUARDRAILS, "spec-ratchet.json"), encoding="utf-8") as f:
            bound = json.load(f).get("bytes_per_criterion")
        return {
            "requirements": len(doc.requirements),
            "criteria": len(doc.criteria),
            "per_criterion": round(crit_bytes / crit_count, 1) if crit_count else None,
            "bound": bound,
        }
    except Exception:
        return {"requirements": None, "criteria": None, "per_criterion": None, "bound": None}


def repeated_pairs():
    proc = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "spec-redundancy-precheck.py"),
                           SPEC], capture_output=True, text=True, cwd=ROOT)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1]).get("open")
    except ValueError:
        return None


def file_lines(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return len(f.read().split("\n"))


def fmt(value):
    if value is None:
        return NOT_MEASURED
    if isinstance(value, int):
        return "{:,}".format(value)
    return str(value)


def queue_rows(baseline, census, reads, slug_map, rounds):
    """One row per file, in the reading queue's order, then every remaining measured document."""
    rows = []
    seen = set()
    position = 0
    for group in baseline["priority"]["groups"]:
        members = group.get("members", [])
        if not members:
            continue
        rows.append({"group": group["title"]})
        for rel in members:
            position += 1
            rows.append(build_row(position, rel, census, reads, slug_map, rounds))
            seen.add(rel)
    remaining = sorted(((p, r) for p, r in census.items() if p not in seen),
                       key=lambda kv: -kv[1].get("total", 0))
    if remaining:
        rows.append({"group": "Every remaining live document, worst first"})
        for rel, _ in remaining:
            position += 1
            rows.append(build_row(position, rel, census, reads, slug_map, rounds))
    return rows


def build_row(position, rel, census, reads, slug_map, rounds):
    entry = census.get(rel)
    slug = slug_map.get(rel)
    my_reads = reads.get(slug, []) if slug else []
    agreed = rounds.get(rel)

    findings = entry.get("total") if entry else None
    longest = entry.get("longest") if entry else None
    style = entry.get("style") if entry else None
    byts = entry.get("bytes") if entry else None

    measured_clean = "yes" if findings == 0 else ("no" if findings is not None else NOT_MEASURED)
    if agreed is None:
        read_clean = NOT_MEASURED if not my_reads else "no"
        agreed_cell = NOT_MEASURED if my_reads else NA
    else:
        # Read clean means the last TWO rounds each returned zero agreed stops, which is the bar
        # PRODUCT_SPEC.md states at INV-267 and scripts/progress-report.py already applies. One
        # clean round is a reader's luck; two in a row is the text.
        last_two = agreed[-2:]
        read_clean = ("yes" if len(last_two) == 2 and all(r["agreed"] == 0 for r in last_two)
                      else "no")
        agreed_cell = str(agreed[-1]["agreed"])

    if measured_clean == "yes" and read_clean == "yes":
        state = "finished"
    else:
        state = "unfinished"

    row = {
        "n": position, "file": rel, "state": state,
        "findings": fmt(findings), "longest": fmt(longest), "style": fmt(style),
        "readings": str(len(my_reads)) if slug else "0",
        "agreed": agreed_cell,
        "measured_clean": measured_clean, "read_clean": read_clean,
        "bytes": fmt(byts), "lines": fmt(file_lines(rel)),
    }
    if rel in SPEC_ONLY:
        s = spec_numbers()
        row["requirements"] = fmt(s["requirements"])
        row["criteria"] = fmt(s["criteria"])
        row["per_criterion"] = fmt(s["per_criterion"])
        row["pairs"] = fmt(repeated_pairs())
    else:
        row["requirements"] = row["criteria"] = row["per_criterion"] = row["pairs"] = NA
    return row


COLUMNS = [
    ("n", "#", "Position in the reading queue. The queue runs by what enters a working context "
               "earliest, so the file an agent reads on every turn stands first."),
    ("file", "file", "The file this row measures."),
    ("state", "state", "DONE when both check columns read ok: the script count sits at zero and "
                       "the last two reading rounds each returned zero agreed stops. Every other "
                       "file reads open. This is the only finish line."),
    ("findings", "find", "How many writing defects a script counted in this file: prose sentences "
                         "longer than 25 words, the human-prose cap read out of "
                         "guardrails/language-rules.json rule r08 and applied to every file, plus "
                         "every finding of the style check (scripts/spec-style-lint.py --tier "
                         "full), plus every finding of the register check "
                         "(scripts/preshow-register-lint.py). Retired 2026-08-21 with "
                         "scripts/rule-census.py: this column now reads \"not measured\" for "
                         "every file."),
    ("longest", "long", "Words in the file's longest prose sentence. One long sentence marks the "
                        "paragraph a reader rereads. Target: 25 words. The rule allows a numbered "
                        "acceptance criterion 35, and the counter does not yet make that "
                        "exception, so PRODUCT_SPEC.md counts criteria of 26 to 35 words as "
                        "findings the rule permits. Retired 2026-08-21 with scripts/rule-census.py: "
                        "this column now reads \"not measured\" for every file."),
    ("style", "style", "Findings of the style check alone (scripts/spec-style-lint.py --tier full). "
                       "Carried apart because a style finding is repaired differently. Retired "
                       "2026-08-21 with scripts/rule-census.py: this column now reads \"not "
                       "measured\" for every file."),
    ("measured_clean", "script ok", "Read ok when the find column sat at zero. A script settled "
                                    "this column, so it cost a command and no reader; it also ran "
                                    "as a push check, gate aa (guardrails/check-doc-findings-"
                                    "bound.py), which refused the push when a file counted more "
                                    "findings than the record kept for it. Both retired "
                                    "2026-08-21."),
    ("readings", "reads", "How many fresh readers have read this file. A reader holds no project "
                          "access: only the file and one fixed list of questions. Each reading "
                          "writes a dated record under docs/language-reads/."),
    ("agreed", "both stopped", "How many places BOTH readers of the last round stopped at. A round "
                               "is two fresh readers sent at the same version of the file, one on "
                               "the strong tier and one on the cheap tier; a place "
                               "counts only when both of them stopped there, because one reader "
                               "measures that reader's path and two agreeing measure the text. "
                               "Counted by hand from the two reading records and stored per round "
                               "in guardrails/progress-baseline.json. While it stands above zero "
                               "the file is repaired and read again. Target: zero."),
    ("read_clean", "readers ok", "Reads ok when the last TWO rounds each came back at zero on the "
                                 "both-stopped column. Only live readers settle this column, so it "
                                 "costs two workers and a repair pass per round. One clean round "
                                 "is a reader's luck; two in a row is the text."),
    ("lines", "lines", "Lines in the file. It says whether one reader holds the file in one pass. "
                       "No numeric target for a specification part file; set by the reading."),
    ("est", "est h", "Estimated hours left to carry this file to DONE. Basis: minutes per hundred "
                     "findings for the mechanical repair, plus the reading rounds still owed times "
                     "the minutes one round costs. Every input is recorded in "
                     "guardrails/progress-baseline.json under estimate."),
    ("cum", "cum h", "Cumulative hours if the files run one at a time, which is what campaign rule 1 "
                     "says today."),
]

# Most significant first: where the file stands, then the bar that decides it, then the cost, then
# the detail numbers behind each bar.
ORDER = ["n", "file", "state", "agreed", "read_clean", "findings", "measured_clean",
         "est", "cum", "readings", "longest", "style", "lines"]
COLUMNS = sorted(COLUMNS, key=lambda c: ORDER.index(c[0]))
SHORT = {"not measured": "n/m", "unfinished": "open", "finished": "DONE", "yes": "ok"}


def short(value):
    return SHORT.get(str(value), str(value))


def estimate_minutes(row, rounds_done, est):
    """Hours still owed on one file. Every input is recorded, and the report states the basis."""
    minutes = 0
    findings = row["findings"]
    if findings == NOT_MEASURED:
        minutes += est["first_measurement_minutes"]
        findings_n = est["assumed_findings_when_unmeasured"]
    else:
        findings_n = int(str(findings).replace(",", ""))
    minutes += (findings_n / 100.0) * est["mechanical_minutes_per_100_findings"]
    owed = max(0, est["rounds_expected"] - rounds_done)
    minutes += owed * est["round_minutes"]
    return minutes


def html_escape(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def spec_table():
    """The four indicators that belong to the specification alone, kept out of the wide table."""
    s = spec_numbers()
    return ["", "### The specification's own size", "",
            "| indicator | today | target |", "|---|---|---|",
            # No byte target. The 840,000-byte ceiling this column used to publish belonged to
            # guardrails/doc-bounds.json and gate z, both "retired whole 2026-08-18 as an unrequested
            # bound" (guardrails/spec-ratchet.json's own note). The figure outlived its home by nine
            # days; the size question is the ratchet's below, and the owner's own word on this class
            # stands at DECISIONS.md 2026-08-07 ~01:10 — no numeric size caps on specifications, the
            # standard is no redundancy.
            "| bytes | %s | no target |" % fmt(load_census()["files"]
                                               .get("PRODUCT_SPEC.md", {}).get("bytes")),
            "| requirements | %s | no target |" % fmt(s["requirements"]),
            "| acceptance criteria | %s | no target |" % fmt(s["criteria"]),
            "| bytes per criterion | %s | falls or holds, bound %s |" % (fmt(s["per_criterion"]),
                                                                        fmt(s["bound"])),
            "| repeated pairs | %s | falls or holds |" % fmt(repeated_pairs()),
            "| lines per part file | %s | 250, once the division lands |" % NOT_MEASURED, ""]


def render_md(rows, today):
    heads = [h for _, h, _ in COLUMNS]
    out = ["# Measurements — one row per file, every indicator", "",
           "Generated %s by `python3 scripts/measurements-table.py`. This table is the source of "
           "truth for where the work stands. Add `--html` to also build `docs/MEASUREMENTS.html`, "
           "the page to read it on — a transient render, swept once its reading closes (SPEC "
           "INV-286)." % today, "",
           "| " + " | ".join(heads) + " |",
           "|" + "|".join(["---"] * len(heads)) + "|"]
    for row in rows:
        if "group" in row:
            out.append("| | **%s** |%s" % (row["group"], "|" * (len(heads) - 2)))
            continue
        cells = []
        for key, _, _ in COLUMNS:
            value = row.get(key, NA)
            cells.append("`%s`" % value if key == "file" else short(value))
        out.append("| " + " | ".join(cells) + " |")
    out.extend(spec_table())
    out.extend(NOTES)
    return "\n".join(out) + "\n"


HTML_STYLE = """
:root { color-scheme: light dark; --line: rgba(127,127,127,.32); --head: rgba(127,127,127,.14); }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", system-ui, sans-serif; margin: 0; padding: 0;
       font-size: 15px; line-height: 1.5; }
header { padding: 1rem 1.25rem .6rem; border-bottom: 1px solid var(--line); }
h1 { font-size: 1.15rem; margin: 0 0 .3rem; }
header p { margin: .2rem 0; font-size: .85rem; opacity: .8; }
.wrap { height: calc(100vh - 8.5rem); overflow: auto; }
table { border-collapse: separate; border-spacing: 0; width: 100%; font-size: .84rem;
        font-variant-numeric: tabular-nums; }
thead th { position: sticky; top: 0; z-index: 3; background: var(--head);
           backdrop-filter: blur(6px); border-bottom: 1px solid var(--line);
           padding: .5rem .6rem; text-align: left; white-space: nowrap; cursor: help;
           text-decoration: underline dotted; text-underline-offset: 3px; }
thead th .tip { display: none; position: absolute; top: 100%; left: 0; z-index: 9;
                width: 26rem; max-width: 70vw; white-space: normal; font-weight: 400;
                font-size: .8rem; line-height: 1.45; padding: .7rem .85rem;
                border: 1px solid var(--line); border-radius: 8px;
                background: Canvas; color: CanvasText;
                box-shadow: 0 10px 30px rgba(0,0,0,.28); }
thead th:hover .tip, thead th:focus-within .tip { display: block; }
thead th:nth-last-child(-n+4) .tip { left: auto; right: 0; }
tbody td { border-bottom: 1px solid var(--line); padding: .3rem .6rem; white-space: nowrap; }
tbody td.file { white-space: normal; font-family: ui-monospace, Menlo, monospace;
                font-size: .82em; }
tbody tr.group td { background: var(--head); font-weight: 600; }
tbody tr:hover td { background: rgba(127,127,127,.10); }
td.num { text-align: right; }
td.done { font-weight: 700; }
td.nm { opacity: .5; }
footer { padding: .8rem 1.25rem; border-top: 1px solid var(--line); font-size: .8rem; opacity: .8; }
"""


def render_html(rows, today, totals):
    head_cells = "".join(
        '<th tabindex="0">%s<span class="tip">%s</span></th>'
        % (html_escape(head), html_escape(tip))
        for _, head, tip in COLUMNS)
    body = []
    for row in rows:
        if "group" in row:
            body.append('<tr class="group"><td></td><td colspan="%d">%s</td></tr>'
                        % (len(COLUMNS) - 1, html_escape(row["group"])))
            continue
        cells = []
        for key, _, _ in COLUMNS:
            value = short(row.get(key, NA))
            cls = []
            if key == "file":
                cls.append("file")
            if key in ("n", "findings", "longest", "style", "readings", "agreed", "lines",
                       "est", "cum"):
                cls.append("num")
            if value == "n/m":
                cls.append("nm")
            if value == "DONE":
                cls.append("done")
            attr = ' class="%s"' % " ".join(cls) if cls else ""
            cells.append("<td%s>%s</td>" % (attr, html_escape(value)))
        body.append("<tr>%s</tr>" % "".join(cells))
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="%s">
<title>Measurements — live-spec</title><style>%s</style></head><body>
<header><h1>Measurements — one row per file, every indicator</h1>
<p>Generated %s by <code>python3 scripts/measurements-table.py</code>. Hover a column name to read
what it measures, why, and what it aims at.</p>
<p>%s</p></header>
<div class="wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>
<footer>%s</footer></body></html>
""" % (GENERATOR, HTML_STYLE, today, html_escape(totals["headline"]), head_cells, "".join(body),
       html_escape(totals["footer"]))


NOTES = [
"## What each column means",
"",
"Each indicator carries five things: what it counts, why the project measures it, what changes when "
"it moves, the command that produces it, and the value it aims at.",
"",
"A file is carried to `finished` by two checks, and the table gives each check a count column and an ok "
"column beside it. The first check is a script: it counts writing defects and reaches zero or it does "
"not. The second check is live readers: two fresh readers read the file and their two lists are "
"compared. The first check costs one command, the second costs two workers and a repair pass per "
"round, which is why the table shows them apart.",
"",
"**state** — a file reads `finished` when both checks read ok. Every other file reads `unfinished`. "
"This is the campaign's only finish line, and the queue advances when a file reaches it.",
"",
"**findings** — how many writing defects a script counted: prose sentences longer than 25 words, "
"plus the findings of the style check, plus the findings of the register check. The 25 was the "
"human-prose cap of rule r08 in `guardrails/language-rules.json`. Retired 2026-08-21 with "
"`scripts/rule-census.py`: this column now reads \"not measured\" for every file.",
"",
"**longest sentence** — the words in the file's longest prose sentence. One long sentence marks the "
"paragraph a reader will reread, so it names where to start. Same command. Target: 25 words. The rule "
"allows a numbered acceptance criterion 35 words, and the counter makes no such exception. So part of "
"PRODUCT_SPEC.md's count is criteria the rule permits.",
"",
"**style** — the findings of `scripts/spec-style-lint.py --tier full` alone, carried as its own column "
"because a style finding is repaired differently from a long sentence. Target: zero.",
"",
"**readings** — how many fresh readers have read this file. A reader holds no project access: only the "
"file and one fixed list of questions, at `docs/briefs/reader-prompt.md`. Each reading "
"writes a dated record under `docs/language-reads/`. Target: the count rises until two readers of one "
"round agree on nothing.",
"",
"**both stopped** — how many places both readers of the latest round stopped at. A single reader's "
"list never repeats, so one reader measures that reader's path and two readers agreeing measures the "
"text. While this stands above zero the file is repaired and read again. Counted by hand from the two "
"reading records and stored per round in `guardrails/progress-baseline.json`. Target: zero.",
"",
"**script ok** — the findings column at zero. Until 2026-08-21 the same number was also a push "
"check, gate aa (`guardrails/check-doc-findings-bound.py`), which refused the push when a file "
"counted more findings than the record kept for it. Both retired.",
"",
"**readers ok** — the both-stopped column at zero for two rounds in a row.",
"",
"**bytes**, **lines** — the file's size. They say whether a file is growing, and whether one reader "
"holds it in one pass. Target for a specification part file: 250 lines of requirement bodies, from "
"`docs/plans/2026-07-29-specification-subdivision.md`.",
"",
"**requirements**, **criteria** — the specification's numbered requirements and their acceptance "
"criteria, counted the way `guardrails/check-size-ratchet.py` counts them. They are the inputs to the "
"density column.",
"",
"**bytes per criterion** — the bytes of the criterion lines divided by the number of criteria. It "
"separates growth by addition from growth by wordiness. A delivery may lower it or leave it; raising "
"it needs a written reason in `guardrails/spec-ratchet.json`. Target: it falls or holds.",
"",
"**repeated pairs** — pairs of sentences whose wording overlaps enough for a pattern to catch them, "
"from `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`. A pattern catches only wording "
"that repeats: it reaches five of the thirty-nine requirement pairs a judged reading found on "
"2026-07-29, recorded in `docs/measure/2026-07-29-specification-size.md`. Target: it falls or holds.",
"",
"## Indicators this table cannot yet fill",
"",
"Each one names what it would decide, and what it needs to exist.",
"",
"**Rounds and cost per file.** They price the campaign, and they decide whether the queue is "
"reachable at all. The reading records hold the data; no script counts it.",
"",
"**Requirements a fresh agent builds unaided.** This is the only number that says whether the "
"readability work changed anything. It needs a recorded run naming the requirements handed over, the "
"agent, and what it produced.",
"",
"**Judged duplication.** The requirement pairs stating one fact twice, the requirement groups sharing "
"one shape, and the glossary entries naming one thing twice were measured by hand once, on "
"2026-07-29. As standing runs they become a push check, and the specification stops growing by rule.",
"",
"**The share of findings a machine catches.** Every class a machine catches is a class no reader "
"spends attention on. It reads the census and the reading records together.",
"",
"## The rule this page enforces",
"",
"Every number stated to a person, in chat or in a document, carries what it counts, why it is "
"measured, what changes when it moves, the command that produced it, and the value it aims at. A "
"number stated bare is a defect of the same kind as an undefined term.",
]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="build docs/MEASUREMENTS.md; --html also builds the reading page")
    parser.add_argument("--html", action="store_true",
                        help="also write docs/MEASUREMENTS.html, the page to read the table on "
                             "(a transient render, SPEC INV-286 — sweep it once the reading closes)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    census = load_census().get("files", {})
    baseline = load(BASELINE)
    slug_map = baseline.get("reading_slugs", {})
    rounds = baseline.get("rounds", {})
    est = baseline["estimate"]
    reads = readings_by_slug()
    today = datetime.date.today().isoformat()
    rows = queue_rows(baseline, census, reads, slug_map, rounds)

    running = 0.0
    done = 0
    files = 0
    for row in rows:
        if "group" in row:
            continue
        files += 1
        if row["state"] == "finished":
            done += 1
            row["est"] = "0"
            row["cum"] = "%.0f" % (running / 60.0)
            continue
        minutes = estimate_minutes(row, len(rounds.get(row["file"], [])), est)
        running += minutes
        row["est"] = "%.1f" % (minutes / 60.0)
        row["cum"] = "%.0f" % (running / 60.0)

    hours = running / 60.0
    day = est["working_hours_per_day"]
    sequential_days = hours / day
    lanes = est["parallel_lanes"]
    parallel_days = hours / (day * lanes)
    totals = {
        "headline": ("%d files, %d finished. %.0f hours of work still owed. One file at a time, at "
                     "%g hours a day, that is %.0f working days. With %d files running side by "
                     "side it is %.0f working days."
                     % (files, done, hours, day, sequential_days, lanes, parallel_days)),
        "footer": ("Estimate basis, all inputs recorded in guardrails/progress-baseline.json: %g "
                   "minutes of mechanical repair per hundred findings, %g minutes per reading "
                   "round, %d rounds expected per file, %g working hours a day. The rounds figure "
                   "rests on one file measured today, so it is the weakest input."
                   % (est["mechanical_minutes_per_100_findings"], est["round_minutes"],
                      est["rounds_expected"], day)),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render_md(rows, today))
    print("measurements-table: wrote %s" % OUT)
    if args.html:
        html_path = OUT.replace(".md", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_html(rows, today, totals))
        print("measurements-table: wrote %s" % html_path)
        print("measurements-table: %s is a page built for one reading — run "
              "python3 scripts/sweep-rendered.py once you are done reading it (SPEC INV-286)."
              % html_path)
    else:
        print("measurements-table: docs/MEASUREMENTS.html not built (pass --html to build the "
              "reading page; the numbers above are already current without it)")
    print(totals["headline"])


if __name__ == "__main__":
    main()
