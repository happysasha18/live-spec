#!/usr/bin/env python3
"""rule-census.py — every live document measured against the rules that carry a machine.

WHY IT EXISTS. The rules this project holds its own writing to live in `guardrails/language-rules.json`
and were applied to one document, the spec's acceptance criteria. The rest of the live documents were
never measured against them. This script produces the number per document, which is what gives the
rewrite its order and what seeds the limit that only falls (ROADMAP 148, 460).

WHAT IT MEASURES. Three readings per file, each naming the rules it stands for:

  - `long` — sentences past the human-prose word cap, which is rule r08's `human_prose_flag_above_words`
    read out of the rule home. A sentence here is a run of prose ended by `.`, `!` or `?`; headings,
    code fences, tables, and link-only lines are skipped.
  - `style` — `scripts/spec-style-lint.py --tier full`, whose findings stand for r10 (a thing named by
    denying its neighbour), r02 (machine jargon), r12 (a grading word), r24-r26 (person), and the
    caps rule. The script's own JSON record gives the count.
  - `register` — `scripts/preshow-register-lint.py`, whose patterns stand for r02's coinage,
    loan-translation and respelling arms and for the affirmation class.

WHAT IT PASSES OVER. A recorded case — a list item holding a quoted text, an arrow, and its quoted
repair — is evidence a rule rests on, and its left side is a defect on purpose. The `long` reading skips
such a line. Every other list item is read.

WHAT IT REFUSES. It refuses a file list that comes out empty, since a census of nothing reports clean.
It names every file it could not read rather than dropping it.

WHAT IT REFUSES TO WRITE (SPEC INV-301, R302.9, R302.10). The record of counts is a ceiling whose
direction is down. So `--json` reads the record it is about to write, and a run where any measured
document stands above its recorded count names every such document and writes nothing at all. A run
where none stands above its record writes each measured count back, as before. Gate aa
(`guardrails/check-doc-findings-bound.py`) prints this command as its remedy for a document whose count
fell; before this refusal, that same command stored a RISEN count with the rest, so the operator whose
push was refused held the one command that turned the refusal into a pass.

HOW A HAND-WRITTEN REASON SURVIVES A REWRITE (R302.11). A raise is lawful when a person states its
reason in the entry's `reason` field, the shape `guardrails/doc-bounds.json` already carries for a
raised byte ceiling. A record write rewrites every entry, so a reason written by hand would be erased by
the next run and the hand-edit path with it. This run therefore reads each path's existing entry and
copies its `reason` onto the entry it writes for that same path. Nothing else of the old entry survives:
every count is the count this run measured.

Usage:
  rule-census.py                       # measure the live set, print the table
  rule-census.py --out FILE            # also write the table as markdown
  rule-census.py --json FILE           # also write the counts as JSON, which is the limit's seed
  rule-census.py --root DIR            # measure the live set under DIR (fixtures; parity with gate aa)
  rule-census.py PATH [PATH ...]       # measure these files instead of the live set
Exit 0 once every file is measured; exit 1 when the set is empty, a reading refused, or a measured
document stands above its recorded count while `--json` was asked to write the record. A run where any
reading refused or any file went unread writes NO record at all: the refusals are read above the write,
because a reading that never ran scores 0 and that 0 would become the ceiling (R302.16).
Stdlib only.
"""
import argparse
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
RULES_PATH = os.path.join(REPO_ROOT, "guardrails", "language-rules.json")
STYLE_LINT = os.path.join(SCRIPT_DIR, "spec-style-lint.py")
REGISTER_LINT = os.path.join(SCRIPT_DIR, "preshow-register-lint.py")

CHECK = "rule-census"

# Directories holding a record of something that happened. A record states what was written at the
# time, so the rules bind it at the moment it is written and never afterwards.
RECORD_DIRS = (
    "attic", "prototype", "nonexistent-home", "nonexistent-ci-home",
    "docs/attic", "docs/queue-archive", "docs/language-reads", "docs/prover", "docs/audit",
    "docs/design-review", "docs/evals", "docs/skill-review", "docs/reports", "docs/handovers",
    "docs/push-review",
    "docs/measure", "docs/gate-audit", "docs/briefs", "docs/design", "docs/research",
    "guardrails/board-fixtures", "guardrails/authority-anchor-fixtures", "tests/fixtures",
    "scaffold", "evals", ".git",
)
RECORD_FILES = ("JOURNAL.md", "DECISIONS.md", "FEEDBACK.md", "MIGRATION.md", "WAITING.md")

FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^\s*#{1,6}\s")
TABLE = re.compile(r"^\s*\|")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
# A line that is its own unit: a list item, a numbered step, a quotation, or a label line of the
# `**field** — value` shape these documents use for a node's parts.
STANDS_ALONE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|>|\*\*[^*]+\*\*\s*(?:—|-|:))")
# A recorded case: a list item holding a quoted defective text, an arrow, and its quoted repair. The
# left side is a defect on purpose, so counting it would score the evidence a rule rests on.
QUOTED_CASE = re.compile(r"^\s*[-*+]\s+`[^`]+`\s*(?:→|->)\s*`[^`]+`\s*$")
# The interpunct this project writes lists with. A run of short names carries none of the load the
# word cap holds a reader to, so its length is no finding. A run of prose clauses split by the same
# mark is prose, and the member length below is what tells the two apart.
ROSTER_MARK = "·"
ROSTER_MIN_MEMBERS = 4
ROSTER_MEMBER_MAX_WORDS = 4


def load_word_cap(path=RULES_PATH):
    """The human-prose word cap, read out of the rule home so the census and the rule cannot drift."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for rule in data.get("rules", []):
        cap = (rule.get("thresholds") or {}).get("human_prose_flag_above_words")
        if cap:
            return int(cap), rule["id"]
    raise SystemExit("%s: no rule in %s carries `human_prose_flag_above_words`" % (CHECK, path))


def load_record(path):
    """The record this run is about to write, as it stands on disk, or an empty record where none is.

    An absent or unreadable record is read as empty, so the first seed of a record writes every count.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("files", {})
    except (OSError, ValueError, AttributeError):
        return {}


def live_files(root=REPO_ROOT):
    """Every markdown file the rules bind today, in sorted order."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir
        dirnames[:] = [d for d in dirnames
                       if not os.path.join(rel_dir, d).startswith(RECORD_DIRS)
                       and os.path.join(rel_dir, d) not in RECORD_DIRS
                       and not d.startswith(".")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            rel = os.path.join(rel_dir, name) if rel_dir else name
            if rel in RECORD_FILES:
                continue
            out.append(rel)
    return sorted(out)


def prose_sentences(text):
    """The prose sentences of a markdown file: no fences, headings, tables, or bare-link lines.

    Running prose wraps across lines, so a paragraph's lines are joined before it is split into
    sentences. A list item and a label line (`**field** — value`) each stand alone: joining them the
    way wrapped prose is joined once read a block of 40 label lines in `ARCHITECTURE.md` as one
    sentence of 1914 words, since none of them ends in a full stop.
    """
    units, buffer, in_fence = [], [], False

    def flush():
        if buffer:
            units.append(" ".join(buffer))
            del buffer[:]

    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            flush()
            continue
        if in_fence or HEADING.match(line) or TABLE.match(line):
            flush()
            continue
        if not line.strip():
            flush()
            continue
        if QUOTED_CASE.match(line):
            flush()
            continue
        if STANDS_ALONE.match(line):
            flush()
            units.append(line.strip())
            continue
        buffer.append(line.strip())
    flush()

    out = []
    for unit in units:
        out += [s.strip() for s in SENTENCE_END.split(unit) if s.strip()]
    return out


def is_code_roster(sentence):
    """Whether this unit is a list of short names written with the interpunct.

    The lead-in before a colon is dropped, so `Binds 11 of the 58 rules: r10 · r12` is read by its
    members. Every member stays at or under the member cap for the unit to count as a list.
    """
    members = [part.strip() for part in sentence.split(ROSTER_MARK)]
    if len(members) < ROSTER_MIN_MEMBERS:
        return False
    if ":" in members[0]:
        members[0] = members[0].split(":", 1)[1].strip()
    return all(len(member.split()) <= ROSTER_MEMBER_MAX_WORDS for member in members)


def long_sentences(text, cap):
    """How many prose sentences run past the cap, and the longest count seen."""
    over, longest = 0, 0
    for sentence in prose_sentences(text):
        if is_code_roster(sentence):
            continue
        words = len(sentence.split())
        longest = max(longest, words)
        if words > cap:
            over += 1
    return over, longest


def run_lint(script, path, extra=()):
    """A lint's finding count, read off its own JSON record where it prints one."""
    try:
        proc = subprocess.run([sys.executable, script] + list(extra) + [path],
                              capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return None, str(e)
    for line in reversed(proc.stdout.strip().split("\n")):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                record = json.loads(line)
            except ValueError:
                continue
            return int(record.get("errors", 0)) + int(record.get("warnings", 0)), None
    # A lint with no record line reports one finding per printed line under its header.
    body = [l for l in proc.stdout.strip().split("\n") if l.strip().startswith("line ")]
    return len(body), None


def measure(rel, cap, root=REPO_ROOT):
    path = os.path.join(root, rel)
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        return {"file": rel, "unread": str(e)}
    over, longest = long_sentences(text, cap)
    style, style_err = run_lint(STYLE_LINT, path, extra=("--tier", "full"))
    register, register_err = run_lint(REGISTER_LINT, path)
    row = {
        "file": rel,
        "bytes": len(text.encode("utf-8")),
        "long": over,
        "longest": longest,
        "style": style if style is not None else 0,
        "register": register if register is not None else 0,
    }
    row["total"] = row["long"] + row["style"] + row["register"]
    refused = [e for e in (style_err, register_err) if e]
    if refused:
        row["refused"] = "; ".join(refused)
    return row


def table(rows, cap, rule_id):
    out = ["# Rule census — 2026-07-28", "",
           "Every live document measured against the rules that carry a machine. This is the order the "
           "rewrite runs in, worst first, and the seed of the limit that only falls (ROADMAP 148, 460).",
           "",
           "A record of something that happened is out of scope: the journal, the decision log, the "
           "prover records, the readings, the attic, and the prototype trees state what was written at "
           "the time.",
           "",
           "`long` counts prose sentences past %d words, which is rule %s's human-prose cap read out of "
           "the rule home. `style` is `scripts/spec-style-lint.py --tier full`. `register` is "
           "`scripts/preshow-register-lint.py`. `longest` is the longest prose sentence in the file."
           % (cap, rule_id),
           "",
           "| file | bytes | long | longest | style | register | total |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        if "unread" in row:
            continue
        out.append("| `%s` | %d | %d | %d | %d | %d | **%d** |"
                   % (row["file"], row["bytes"], row["long"], row["longest"],
                      row["style"], row["register"], row["total"]))
    unread = [r for r in rows if "unread" in r]
    if unread:
        out += ["", "## Files this census could not read", ""]
        out += ["- `%s` — %s" % (r["file"], r["unread"]) for r in unread]
    measured = [r for r in rows if "unread" not in r]
    out += ["", "## Totals", "",
            "%d files measured. %d sentences past the cap, %d style findings, %d register findings, "
            "%d in all." % (len(measured), sum(r["long"] for r in measured),
                            sum(r["style"] for r in measured),
                            sum(r["register"] for r in measured),
                            sum(r["total"] for r in measured))]
    return "\n".join(out) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description="Measure the live documents.")
    parser.add_argument("paths", nargs="*", help="files to measure; the live set when omitted")
    parser.add_argument("--out", help="write the table here as markdown")
    parser.add_argument("--json", dest="json_out", help="write the counts here as JSON")
    parser.add_argument("--root", default=REPO_ROOT,
                        help="measure the live set under this directory (fixtures)")
    args = parser.parse_args(argv[1:])

    cap, rule_id = load_word_cap()
    files = args.paths or live_files(args.root)
    if not files:
        print("%s: the file set is EMPTY — a census of nothing reports clean." % CHECK)
        return 1
    rows = [measure(f, cap, root=args.root) for f in files]
    rows.sort(key=lambda r: r.get("total", 0), reverse=True)
    text = table(rows, cap, rule_id)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%s: wrote %s" % (CHECK, args.out))
    refused = [r for r in rows if "refused" in r or "unread" in r]
    if args.json_out and refused:
        # A reading that never ran scores 0 (SPEC INV-301, R302.16), and a 0 written here becomes the
        # ceiling the ratchet holds. So the refusals are read BEFORE the write, the shape the risen
        # case below already carries. Queue row 525 covers the neighbouring path, where a reading
        # produces no count at all; once such a reading refuses instead of scoring 0, it stops the
        # write right here with no further change.
        print("%s: REFUSED to write %s — a reading that never ran scores 0, and a 0 recorded here "
              "becomes the next ceiling (SPEC INV-301, R302.16)." % (CHECK, args.json_out))
        for row in refused:
            print("  %s — %s" % (row["file"], row.get("refused") or row.get("unread")))
        print("  Repair the reading and run the census again; the record on disk is left as it stood.")
        return 1
    if args.json_out:
        recorded = load_record(args.json_out)
        measured = {r["file"]: r for r in rows if "unread" not in r}
        risen = [(rel, recorded[rel].get("total", 0), row["total"])
                 for rel, row in sorted(measured.items())
                 if rel in recorded and row["total"] > recorded[rel].get("total", 0)]
        if risen:
            print("%s: REFUSED to write %s — the record is a ceiling and its direction is down "
                  "(SPEC INV-301, R302.9)." % (CHECK, args.json_out))
            for rel, was, now in risen:
                print("  %s stands above its record: recorded %d, measured %d" % (rel, was, now))
            print("  Repair the text, or state the reason in the entry's `reason` field by hand.")
            return 1
        for rel, row in measured.items():
            reason = (recorded.get(rel) or {}).get("reason")
            if reason:
                row["reason"] = reason
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump({"cap": cap, "cap_rule": rule_id, "files": measured},
                      fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print("%s: wrote %s" % (CHECK, args.json_out))
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
