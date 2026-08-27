#!/usr/bin/env python3
"""check-tier-refusal.py — the tier-refusal record and its learned patterns hold their shape
(ROADMAP row 507, the routing experiment opened 2026-07-28).

BLOCKING. A fault flips the exit code to 1 and carries one parseable JSON object beside its human
lines, the gate contract's typed line (guardrails/README.md convention 1). It writes nothing to disk,
so the all-or-nothing write convention has nothing to hold here; it reads and reports only.

THE LAW. A dispatch to the expensive tier proves its own need in three steps, and money is spent only
on the middle one. Patterns learned from past refusals turn a task away before any model call; a
dispatch that gets through opens with one instruction, and a run that stops names a cheaper tier and
one sentence of reason; the full run proceeds when both let it through. The record is the whole
evidence: a refusal that names no tier teaches no re-dispatch, a refusal that names no reason teaches
no phrase, and a pattern promoted on thin evidence turns work away on a guess. This gate holds those
faults:

  - A REFUSAL NAMING NO TIER. The orchestrator re-runs a refused brief a tier down, and the row that
    says which tier is the only thing that says where down is.
  - A REFUSAL NAMING NO REASON. A phrase is promoted from agreeing reasons; an empty cell, a dash, or
    a placeholder word carries no agreement.
  - A PATTERN ON THIN EVIDENCE. A promoted phrase cites fewer refusals than
    `promotion.refusals_required` in guardrails/tier-refusal.json, cites a row the record lacks, cites
    a row naming another tier, or carries words absent from a cited row's task text.
  - A BROKEN RECORD. The header row moved, a row carries the wrong cell count, a date is unreadable, a
    tier stands outside the declared ladder, an Id repeats, or the task cell is empty.

THE LEARNED-PATTERN STEP. `--brief "<text>"` runs step one: it reads the promoted patterns and prints
the tier a pattern says the task needs, with the phrase that matched. A task matching nothing prints a
verdict with a null tier and passes through. This mode reports a ROUTING verdict, so its exit code
stays 0 either way and the answer is read off the printed JSON object.

WHERE IT RUNS. It mints no push-gate letter. The check rides the suite through
tests/test_tier_refusal.py, which runs it against the shipped record and the shipped pattern list on
every suite run, the way the far-tier and node-growth checks ride the suite. A brief-writing session
reaches it directly at dispatch time through `--brief`.

WHAT IT DOES NOT SEE. It calls no model and reads no transcript. Whether a named tier was the RIGHT
tier is answered by re-running the brief a tier down, and the cost of a wrong refusal is counted in
docs/measure/2026-07-28-tier-routing-experiment.md.

THE EMPTY RECORD. A record holding zero rows is the experiment's declared start state (row 507: the
pattern list starts empty and grows from the record), so an empty row set is a permitted empty set
here, declared at this call site the way SPEC INV-218 asks. The gate says how many rows it read, so a
reader sees the zero. A record file that is absent, or one whose header row is gone, is the broken
shape above and reds.

Usage:
  check-tier-refusal.py [--config PATH] [--record PATH]
  check-tier-refusal.py --brief "the task text" [--config PATH]
Exit 0 when the record and the patterns hold their shape, 1 otherwise. Stdlib only.
"""
import argparse
import datetime
import json
import os
import re
import sys

CHECK = "check-tier-refusal"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "tier-refusal.json")

# A reason cell holding one of these says nothing a phrase can be read out of.
PLACEHOLDER_REASONS = {"", "-", "--", "—", "n/a", "na", "none", "tbd", "?", "todo"}

_WORD = re.compile(r"[a-z0-9]+")


def normalize(text):
    """A text as space-separated lowercase words, punctuation dropped.

    Both a task text and a pattern phrase pass through here, so a phrase matches a task the way a
    person reading the two would say they match, and a comma or a backtick changes no verdict.
    """
    return " ".join(_WORD.findall((text or "").lower()))


def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_record(text, columns):
    """The record's rows, plus the faults its shape carries.

    Returns `(rows, faults)`. A row is a dict keyed by the declared column names, carrying `line`,
    the 1-based line number it was read from. A fault is a plain sentence.
    """
    faults = []
    lines = text.splitlines()
    header_at = None
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = _cells(line)
        if cells == columns:
            header_at = i
            break
    if header_at is None:
        faults.append("the header row naming %s is missing, so no row can be read"
                      % ", ".join(columns))
        return [], faults

    if header_at + 1 >= len(lines) or not _is_separator(lines[header_at + 1]):
        faults.append("the line under the header (line %d) is no separator row, so the table's shape "
                      "is broken" % (header_at + 2))
        return [], faults

    rows = []
    for i in range(header_at + 2, len(lines)):
        line = lines[i]
        if not line.strip().startswith("|"):
            if line.strip():
                break
            continue
        cells = _cells(line)
        if len(cells) != len(columns):
            faults.append("line %d carries %d cells where the record declares %d (%s)"
                          % (i + 1, len(cells), len(columns), ", ".join(columns)))
            continue
        row = dict(zip(columns, cells))
        row["line"] = i + 1
        rows.append(row)
    return rows, faults


def _cells(line):
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") else body
    return [c.strip() for c in body.split("|")]


def _is_separator(line):
    cells = _cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def check_rows(rows, tiers, columns):
    """The faults the recorded refusals carry, each a finding dict."""
    findings = []
    seen = {}
    id_col, date_col, task_col, tier_col, reason_col = columns
    for row in rows:
        where = "%s (line %d)" % (row[id_col] or "an unnamed row", row["line"])
        rid = row[id_col]
        if not rid:
            findings.append(_finding(
                "record-shape",
                "the refusal on line %d carries no Id, so no pattern can cite it" % row["line"],
                "give every recorded refusal a short unique Id (TR-001, TR-002, …)"))
        elif rid in seen:
            findings.append(_finding(
                "record-shape",
                "the Id %s is used twice, on lines %d and %d" % (rid, seen[rid], row["line"]),
                "an Id names one refusal; renumber the later row"))
        else:
            seen[rid] = row["line"]

        if not _is_date(row[date_col]):
            findings.append(_finding(
                "record-shape",
                "%s carries the date %r, which is unreadable as YYYY-MM-DD"
                % (where, row[date_col]),
                "write the day of the refusal as YYYY-MM-DD"))

        if not row[task_col]:
            findings.append(_finding(
                "record-shape",
                "%s carries no task text, so no phrase can ever be read out of it" % where,
                "copy the brief's own sentence saying what the work is into the Task cell"))

        tier = row[tier_col]
        if not tier:
            findings.append(_finding(
                "missing-tier",
                "%s names no tier" % where,
                "name the tier the run said does this task; the orchestrator re-runs the brief there"))
        elif tier not in tiers:
            findings.append(_finding(
                "record-shape",
                "%s names the tier %r, which stands outside the declared ladder (%s)"
                % (where, tier, ", ".join(tiers)),
                "name a tier from the ladder in guardrails/tier-refusal.json, or add it there"))

        if row[reason_col].strip().lower() in PLACEHOLDER_REASONS:
            findings.append(_finding(
                "missing-reason",
                "%s names no reason (%r)" % (where, row[reason_col]),
                "write one sentence saying what makes this work fit the named tier; the reasons are "
                "what a phrase is later read out of"))
    return findings


def check_patterns(patterns, rows, config, columns):
    """The faults the promoted patterns carry, each a finding dict."""
    findings = []
    promotion = config.get("promotion") or {}
    required = promotion.get("refusals_required")
    # No fallback width. These stood at 1 and 99 — invented magnitudes with no source (the
    # 2026-08-07 census, row 14, found no trace behind the declared 2-8 either), and they made a
    # config that omits its bounds pass almost any phrase silently instead of saying so. A width the
    # config does not declare is a config defect, reported below the way its sibling
    # `refusals_required` already reports one; there is no width to check until it is declared.
    min_words = promotion.get("phrase_min_words")
    max_words = promotion.get("phrase_max_words")
    tiers = config.get("tiers") or []
    id_col, _date_col, task_col, tier_col, _reason_col = columns
    by_id = {row[id_col]: row for row in rows if row[id_col]}

    if not isinstance(required, int) or required < 1:
        findings.append(_finding(
            "config-shape",
            "promotion.refusals_required reads %r, which names no count of agreeing refusals"
            % (required,),
            "state promotion.refusals_required as a whole number of refusals (row 507 states three)"))
        required = 3

    bounds_declared = (isinstance(min_words, int) and not isinstance(min_words, bool)
                       and isinstance(max_words, int) and not isinstance(max_words, bool)
                       and 1 <= min_words <= max_words)
    if patterns and not bounds_declared:
        findings.append(_finding(
            "config-shape",
            "promotion.phrase_min_words/phrase_max_words read %r and %r, which name no phrase width"
            % (min_words, max_words),
            "state both as whole numbers of words, the smaller first; a promoted phrase is checked "
            "against the width the config declares, and an undeclared width checks nothing"))

    seen_phrases = {}
    for pattern in patterns:
        phrase = (pattern.get("phrase") or "").strip()
        name = phrase or "an unnamed pattern"
        words = normalize(phrase).split()
        if not words:
            findings.append(_finding(
                "config-shape",
                "a promoted pattern carries no phrase",
                "give every pattern the run of words it fires on"))
            continue
        if phrase in seen_phrases:
            findings.append(_finding(
                "config-shape",
                "the phrase %r is promoted twice" % phrase,
                "one entry per phrase; merge the two and keep every Id behind it"))
        seen_phrases[phrase] = True
        if bounds_declared and not (min_words <= len(words) <= max_words):
            findings.append(_finding(
                "config-shape",
                "the pattern %r is %d words long, outside the declared %d to %d"
                % (phrase, len(words), min_words, max_words),
                "a pattern a person can check is a short run of words copied out of the refused "
                "tasks; trim or widen it"))

        tier = pattern.get("tier")
        if tier not in tiers:
            findings.append(_finding(
                "config-shape",
                "the pattern %r names the tier %r, which stands outside the declared ladder (%s)"
                % (name, tier, ", ".join(tiers)),
                "a pattern names the tier its refusals named"))

        cited = pattern.get("refusals") or []
        if len(cited) < required:
            findings.append(_finding(
                "thin-pattern",
                "the pattern %r cites %d refusal%s where %d agreeing refusals are required"
                % (name, len(cited), "" if len(cited) == 1 else "s", required),
                "a phrase is promoted once %d recorded refusals name the same tier and carry the "
                "phrase in their task text; leave it out of the pattern list until then" % required))

        for rid in cited:
            row = by_id.get(rid)
            if row is None:
                findings.append(_finding(
                    "thin-pattern",
                    "the pattern %r cites the refusal %s, which the record does not hold"
                    % (name, rid),
                    "cite the Ids of real rows in the record; a pattern is re-read against them "
                    "every run"))
                continue
            if row[tier_col] != tier:
                findings.append(_finding(
                    "thin-pattern",
                    "the pattern %r names the tier %r while its refusal %s named %r"
                    % (name, tier, rid, row[tier_col]),
                    "a pattern is promoted from refusals that AGREE on the tier; split the pattern "
                    "or drop the row that disagrees"))
            if normalize(phrase) not in normalize(row[task_col]):
                findings.append(_finding(
                    "thin-pattern",
                    "the pattern %r carries words the task text of its refusal %s does not"
                    % (name, rid),
                    "a phrase is copied out of the refused tasks word for word, so a person reading "
                    "the pattern sees why it fires"))
    return findings


def _finding(code, message, fix):
    return {"code": "tier-refusal-" + code, "message": message, "fix": fix}


def _is_date(text):
    try:
        datetime.date.fromisoformat((text or "").strip())
        return True
    except ValueError:
        return False


def tier_for(brief, patterns):
    """The tier a learned pattern says this brief needs, with the pattern that matched.

    Returns `{"tier": ..., "phrase": ..., "refusals": [...]}` for the first matching pattern, or
    None when no pattern matches and the brief goes on to the paid steps. The longest phrase is read
    first, then alphabetical order, so the same brief always meets the same answer.
    """
    words = " " + normalize(brief) + " "
    ordered = sorted(patterns,
                     key=lambda p: (-len(normalize(p.get("phrase") or "").split()),
                                    normalize(p.get("phrase") or "")))
    for pattern in ordered:
        phrase = normalize(pattern.get("phrase") or "")
        if phrase and (" " + phrase + " ") in words:
            return {"tier": pattern.get("tier"), "phrase": pattern.get("phrase"),
                    "refusals": pattern.get("refusals") or []}
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="the tier-refusal record and its learned patterns hold their shape")
    parser.add_argument("--config", default=os.environ.get("LIVE_SPEC_TIER_REFUSAL_CONFIG",
                                                           DEFAULT_CONFIG))
    parser.add_argument("--record", default=os.environ.get("LIVE_SPEC_TIER_REFUSAL_RECORD"))
    parser.add_argument("--brief", help="run the learned-pattern step against this task text")
    args = parser.parse_args(argv)

    config_path = os.path.abspath(os.path.expanduser(args.config))
    try:
        config = load_config(config_path)
    except (OSError, ValueError) as e:
        return _red([_finding("config-shape",
                              "the tier-refusal data at %s could not be read: %s" % (config_path, e),
                              "restore guardrails/tier-refusal.json; it holds the instruction, the "
                              "tier ladder, and the promoted patterns")])

    patterns = config.get("patterns") or []

    if args.brief is not None:
        hit = tier_for(args.brief, patterns)
        if hit:
            print("%s: a learned pattern turns this task away before any model call — %r says the "
                  "%s tier does it, on the refusals %s."
                  % (CHECK, hit["phrase"], hit["tier"], ", ".join(hit["refusals"]) or "it cites"))
        else:
            print("%s: no learned pattern matches this task, so it goes on to the instruction step "
                  "(read %d promoted pattern%s)."
                  % (CHECK, len(patterns), "" if len(patterns) == 1 else "s"))
        print(json.dumps({"tier": hit["tier"] if hit else None,
                          "phrase": hit["phrase"] if hit else None,
                          "refusals": hit["refusals"] if hit else [],
                          "patterns_read": len(patterns)}))
        return 0

    columns = config.get("record_columns") or []
    if len(columns) != 5:
        return _red([_finding("config-shape",
                              "record_columns reads %r, and the record's five columns are the Id, "
                              "the date, the task, the named tier, and the reason" % (columns,),
                              "state the five column names in guardrails/tier-refusal.json")])

    record_path = args.record or os.path.join(REPO_ROOT, config.get("record") or "")
    record_path = os.path.abspath(os.path.expanduser(record_path))
    try:
        with open(record_path, encoding="utf-8") as f:
            record_text = f.read()
    except OSError as e:
        return _red([_finding("record-shape",
                              "the refusal record at %s could not be read: %s" % (record_path, e),
                              "the record is where every refusal lands; create it with its header "
                              "row, or point the config's `record` field at its home")])

    rows, shape_faults = parse_record(record_text, columns)
    findings = [_finding("record-shape", fault,
                         "the record's rows are read by column; restore the table's shape "
                         "(docs/measure/tier-refusals.md says how a row is written)")
                for fault in shape_faults]
    findings += check_rows(rows, config.get("tiers") or [], columns)
    findings += check_patterns(patterns, rows, config, columns)

    if findings:
        return _red(findings)

    print("OK (%s): %d recorded refusal%s and %d promoted pattern%s hold their shape. Read the table "
          "in %s by the columns %s — every row for its named tier, its reason, its Id, and its date — "
          "and every pattern in %s for the agreeing refusals behind it (%s required), each cited row's "
          "tier, and the phrase standing word for word in that row's task text. It calls no model and "
          "reads no transcript; whether a named tier was the right one is answered by re-running the "
          "brief a tier down (ROADMAP row 507)."
          % (CHECK, len(rows), "" if len(rows) == 1 else "s", len(patterns),
             "" if len(patterns) == 1 else "s", record_path, ", ".join(columns), config_path,
             (config.get("promotion") or {}).get("refusals_required")))
    if not rows:
        print("%s: the record holds zero refusals. That is the experiment's declared start state — "
              "the pattern list starts empty and grows from the record — so the empty row set is a "
              "permitted empty set here and is named rather than passed over (SPEC INV-218)." % CHECK)
    return 1 if findings else 0


def _red(findings):
    for f in findings:
        print("%s: %s" % (CHECK, f["message"]))
    print()
    print("A refusal names the tier the brief is re-run on and the reason the work fits it; a pattern")
    print("is promoted only once the required refusals agree, and it is re-read against their rows on")
    print("every run. The record's shape is stated in docs/measure/tier-refusals.md and in")
    print("guardrails/tier-refusal.json (ROADMAP row 507).")
    first = findings[0]
    print(json.dumps({"severity": "error", "code": first["code"],
                      "message": first["message"], "fix": first["fix"]}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
