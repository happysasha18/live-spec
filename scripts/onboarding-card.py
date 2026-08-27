#!/usr/bin/env python3
"""onboarding-card.py — render the settings card (M-206..M-212, INV-87/INV-88).

v2: the frozen norm (docs/norms/onboarding-card-2026-07-10.html) IS the
template. This script reads it and outputs that same document with values
injected at known slots; every section, heading, row name, style rule and
copy line in the norm survives verbatim except the specific slots decision 2
names. It also reads the package-defaults table from the base skill (to
validate it and fail loudly on a malformed row) and the profile files
(personal + host) to source the injected values and the project-rules part.

Usage:
  onboarding-card.py --base PATH --personal PATH --host PATH --out PATH [--norm PATH]
"""
import argparse
import html
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NORM = REPO_ROOT / "docs" / "norms" / "onboarding-card-2026-07-10.html"

HEADER_CELLS = 4  # | Setting | Default | A profile may say | Card |

# Norm row name -> the table/profile keys that row represents (decision 2).
# First key is primary (goes on the row's own data-setting-key); any further
# keys are secondary (same visual row, separate key identity for tracing).
ROW_KEYS = {
    "What kind of project this is": ["project.kind"],
    "How thorough it is on each change": ["budget.pressure"],
    "Language": ["language.chat", "language.docs"],
    "How often it stops to ask you": ["proactivity.mode"],
    "What it calls you": ["address"],
}
KNOWN_KEYS = {k for keys in ROW_KEYS.values() for k in keys}

EXTRA_CSS = """
.your-value{color:var(--accent);font-weight:600}
.notice{background:var(--warn-bg);color:var(--warn);border:1px solid color-mix(in srgb,var(--warn) 30%,transparent);
  border-radius:10px;padding:10px 14px;font-size:14px;margin:0 0 14px}
"""


def fail(message):
    sys.stderr.write(message.rstrip("\n") + "\n")
    sys.exit(2)


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- base table

def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return s.split("|")


def parse_base(path):
    """Parse and VALIDATE the "### Package defaults" table; a malformed row
    (wrong cell count, or a Card cell that is neither visible nor internal)
    fails the render loudly, naming the row. Returns the parsed rows (not
    otherwise used for rendering in v2 — the norm's own named rows are the
    template; this is validation plus a traceability source)."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == "### Package defaults":
            start = i
            break
    if start is None:
        fail("no '### Package defaults' section found in %s" % path)

    rows = []
    header_cells = None
    in_table = False
    i = start + 1
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("|"):
            in_table = True
            cells = split_row(ln)
            if header_cells is None:
                header_cells = cells
                i += 1
                continue
            if all(re.match(r"^:?-+:?$", c.strip()) for c in cells):
                i += 1
                continue
            rows.append((ln, cells))
            i += 1
            continue
        elif in_table:
            break
        i += 1

    if header_cells is None:
        fail("the Package defaults table has no header row in %s" % path)

    out = []
    for ln, cells in rows:
        if len(cells) != len(header_cells):
            fail("malformed package-defaults table row (wrong cell count): %s" % ln.strip())
        key_cell = cells[0].strip()
        card_cell = cells[-1].strip()
        m = re.match(r"^`([\w.-]+)`$", key_cell)
        if not m or card_cell not in ("visible", "internal"):
            fail("malformed package-defaults table row: %s" % ln.strip())
        out.append((m.group(1), cells[1].strip(), cells[2].strip(), card_cell))
    return out


# ------------------------------------------------------------- profile files

def split_entries(text):
    """A profile entry starts at a line beginning "- " and continues over
    subsequent non-blank, non-"- " lines (indented/wrapped continuations)
    until the next "- " line or a heading. Blank lines do not by themselves
    end an entry (real content always resumes with a fresh "- " line or a
    heading, which does)."""
    entries = []
    cur = []
    for ln in text.splitlines():
        if ln.startswith("#"):
            if cur:
                entries.append(cur)
                cur = []
            continue
        if ln.startswith("- "):
            if cur:
                entries.append(cur)
            cur = [ln]
        elif ln.strip():
            if cur:
                cur.append(ln)
        # blank line: leave any open entry as-is
    if cur:
        entries.append(cur)
    return entries


KEYED_ENTRY_RE = re.compile(r"^`([\w.-]+):\s*([^`]*)`")


def classify_entry(lines):
    """Join an entry's physical lines with single spaces, then classify:
    keyed if the joined text (leading "- " stripped) matches `key: value`
    with the backtick now closed after the join — value stops at that
    closing backtick, the provenance tail is dropped. Otherwise prose: the
    whole joined text, leading "- " stripped, verbatim."""
    joined = " ".join(l.strip() for l in lines)
    if joined.startswith("- "):
        joined = joined[2:].strip()
    m = KEYED_ENTRY_RE.match(joined)
    if m:
        return ("keyed", m.group(1), m.group(2).strip())
    return ("prose", joined, "")


def parse_profile_entries(path):
    if not Path(path).exists():
        return []
    text = Path(path).read_text(encoding="utf-8")
    return [classify_entry(e) for e in split_entries(text)]


# --------------------------------------------------------------- HTML build

def inject_known_row(doc, row_name, keys, values):
    """Mark the norm row named row_name with data-setting-key/data-source
    for each of its keys, and inject any recorded value: a pill-shaped
    value slot gets its pill text replaced; a prose-only slot gets the
    recorded value appended after the existing copy (the fixed copy must
    survive alongside the reader's own value, per INV-88)."""
    primary, secondary = keys[0], keys[1:]

    open_pat = re.compile(r'(<div class="row">)(\s*<div class="name">%s</div>)' % re.escape(row_name))

    def open_repl(m):
        markers = "".join(
            '<span data-setting-key="%s" data-source="table" style="display:none"></span>' % esc(k)
            for k in secondary)
        return '<div class="row" data-setting-key="%s" data-source="table">%s%s' % (
            esc(primary), m.group(2), markers)

    doc, n = open_pat.subn(open_repl, doc, count=1)
    if n == 0:
        fail("norm template is missing the expected row: %s" % row_name)

    val_pat = re.compile(r'(<div class="name">%s</div>.*?<div class="val">)(.*?)(</div>)'
                          % re.escape(row_name), re.S)

    def val_repl(m):
        content = m.group(2)
        if '<span class="pill">' in content:
            value = values.get(primary)
            if value:
                content = re.sub(
                    r'<span class="pill">.*?</span>',
                    '<span class="pill your-value" data-source="profile-line">%s</span>' % esc(value),
                    content, count=1, flags=re.S)
        else:
            for key in keys:
                value = values.get(key)
                if value:
                    content += (' <span class="your-value" data-setting-key="%s" '
                                'data-source="profile-line">%s</span>' % (esc(key), esc(value)))
        return m.group(1) + content + m.group(3)

    doc, n2 = val_pat.subn(val_repl, doc, count=1)
    if n2 == 0:
        fail("norm template is missing the expected value slot for row: %s" % row_name)
    return doc


# A display width: past this many characters a project-rules value is cut rather than shown whole on
# the card. Not a threshold anything is checked against — nothing reds off it, and the underlying
# entry is unchanged. No source behind the 160 (2026-08-07 census, row 68; the introducing commit
# 64b0457 never mentions it); a chosen card width, named the way the progress report's table width
# was named (commit 31d3375, 2026-08-19).
LONG_VALUE_BOUND = 160


def format_project_line(text, key=None):
    """A project-rules row's BODY is the entry's readable text, never a raw
    dotted key standing as a heading. Text past the bound is truncated with
    an ellipsis and a plain note; a keyed entry additionally carries its key
    as a quiet trailing anchor — legal there, since it is not a heading."""
    if len(text) > LONG_VALUE_BOUND:
        text = text[:LONG_VALUE_BOUND].rstrip() + "… (the full line lives in your profile)"
    if key:
        text += " (recorded as `%s`)" % key
    return text


def build_project_rules_rows(entries):
    if not entries:
        return '\n    <p class="means">No project-specific rules recorded yet for this host.</p>\n'
    out = []
    for kind, a, b in entries:
        if kind == "keyed":
            key, value = a, b
            body = format_project_line(value, key=key)
            attrs = ' data-setting-key="%s" data-source="profile-line"' % esc(key)
        else:
            body = format_project_line(a)
            attrs = ""
        out.append('\n    <div class="row"%s>\n      <p class="means">%s</p>\n    </div>' % (attrs, esc(body)))
    return "".join(out) + "\n"


def inject_project_rules(doc, host_entries):
    """The norm's "Two rules this project sets for itself" section holds two
    example rows, but those rows are DATA (one host's own recorded rules),
    not template — on a different host they would show false content. The
    section is emptied of them entirely and shows only the real parsed host
    lines, or the one plain no-rules-recorded line when there are none."""
    doc, n = re.subn(
        r'(<section>)(\s*<h2>Two rules this project sets for itself</h2>)',
        r'<section id="project-rules">\2', doc, count=1)
    if n == 0:
        fail("norm template is missing the 'Two rules this project sets for itself' section")
    rows_html = build_project_rules_rows(host_entries)
    pattern = re.compile(
        r'(<h2>Two rules this project sets for itself</h2>\s*<p class="sub">.*?</p>)(.*?)(</section>)',
        re.S)
    doc, n2 = pattern.subn(lambda m: m.group(1) + rows_html + m.group(3), doc, count=1)
    if n2 == 0:
        fail("norm template is missing the end of the 'Two rules' section")
    return doc


def finalize_about_you_section(doc, personal_missing, unmatched_personal):
    notice_html = ""
    if personal_missing:
        notice_html = (
            '\n    <p class="notice">No personal profile exists yet — the founding offer at '
            "project setup creates one from the template.</p>")
    rows_html = ""
    if unmatched_personal:
        # Unmatched personal entries never wall the card, however many there
        # are: they collapse into one counted summary row, never per-entry
        # (no key, no value text — those stay in the profile itself).
        rows_html = (
            '\n    <div class="row"><span class="plain">You have %d more preferences recorded '
            "— they live in your personal profile.</span></div>" % len(unmatched_personal))

    pat = re.compile(r'(<h2>About you.*?</h2>\s*<p class="sub">.*?</p>)(.*?)(?=</section>)', re.S)

    def repl(m):
        return m.group(1) + notice_html + m.group(2) + rows_html

    doc, n = pat.subn(repl, doc, count=1)
    if n == 0:
        fail("norm template is missing the 'About you' section")
    return doc


def build(base_path, personal_path, host_path, norm_path):
    parse_base(base_path)  # validates, fails loudly on a malformed row

    personal_missing = not Path(personal_path).exists()
    personal_entries = parse_profile_entries(personal_path)
    personal_keyed = {k: v for (kind, k, v) in personal_entries if kind == "keyed"}

    host_entries = parse_profile_entries(host_path)
    host_keyed = {k: v for (kind, k, v) in host_entries if kind == "keyed"}

    values = {}
    for key in KNOWN_KEYS:
        if key in host_keyed:
            values[key] = host_keyed[key]
        elif key in personal_keyed:
            values[key] = personal_keyed[key]

    unmatched_personal = [(k, v) for k, v in personal_keyed.items() if k not in KNOWN_KEYS]

    doc = Path(norm_path).read_text(encoding="utf-8")
    doc = doc.replace("</style>", EXTRA_CSS + "</style>", 1)

    for row_name, keys in ROW_KEYS.items():
        doc = inject_known_row(doc, row_name, keys, values)

    doc = inject_project_rules(doc, host_entries)
    doc = finalize_about_you_section(doc, personal_missing, unmatched_personal)

    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--personal", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--norm", default=str(DEFAULT_NORM))
    args = ap.parse_args()

    t0 = time.monotonic()
    out_html = build(args.base, args.personal, args.host, args.norm)
    render_ms = int((time.monotonic() - t0) * 1000)
    Path(args.out).write_text(out_html, encoding="utf-8")
    print(args.out)
    print("render-ms: %d" % render_ms)


if __name__ == "__main__":
    main()
