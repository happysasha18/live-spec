#!/usr/bin/env python3
"""apply-criterion-rewrites.py — the single applier for drafted criterion rewrites.

WHY THIS EXISTS. Acceptance criteria in a spec document get rewritten for readability by several
drafters working in parallel. Each drafter hands back a proposal file: a list of {line, code, old,
new, why} objects, one per criterion it wants replaced. This script is the one place those proposals
turn into an edited document. It reads the document once, reads one or more proposal files, and
either applies every proposal in the batch or applies none of them.

WHAT IT READS. The document named on the command line, and one or more proposal JSON files, each a
list of objects shaped:
  {"line": 2833, "code": "R130.7", "old": "<verbatim line>", "new": "<replacement, 1+ lines>",
   "why": "<one sentence>"}
`new` may hold embedded newlines when a criterion is split into a sub-list.

WHAT IT CHECKS, before writing anything.
  1. Each proposal's `old` must equal the document's actual line at `line`. When it does not match
     there, the script searches the whole document for `old`; a single match elsewhere is accepted
     and its true line number is reported, but zero matches or more than one match is a failure.
  2. No two proposals in the batch may target the same line, and no two proposals' `old` spans may
     overlap.
  3. Any failure means nothing is written. Every failure is printed with its proposal's index, its
     code, its stated line, and the reason, and the script exits non-zero. A batch stands or falls
     together — there is no partial apply.

WHAT IT DOES ON SUCCESS. With every check passed and `--dry-run` absent, it applies all replacements
in one write, working from the highest line number down so an earlier replacement's line numbers
never shift under a later one. It prints a report — proposals applied, a count per requirement code,
and the net change in line count — and writes that same report as markdown when `--report` names a
file.

WHAT IT REFUSES TO REASON ABOUT. It does not judge whether a proposed rewrite reads better than the
original; that call belongs to the drafter and whoever reviews the diff. It checks `git diff
--name-only` for the document and prints a warning when the document already carries uncommitted
changes, but it does not block on that alone — the batch's own match check against the document's
current text is what actually stands guard.

Usage:
  apply-criterion-rewrites.py <document.md> <proposals.json> [<proposals2.json> ...] [--dry-run]
                              [--report OUT.md]
Exit 0 when the batch applies (or would apply, under --dry-run). Exit 1 when any proposal fails a
check, or when the input is malformed. Stdlib only.
"""
import json
import os
import subprocess
import sys

CHECK = "apply-criterion-rewrites"


def usage(prog):
    return ("%s: usage: %s <document.md> <proposals.json> [<proposals2.json> ...] "
            "[--dry-run] [--report OUT.md]" % (CHECK, os.path.basename(prog)))


def load_proposals(path):
    """The list of proposal objects a single JSON file holds, tagged with their source file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("%s does not hold a JSON list of proposals" % path)
    out = []
    for i, item in enumerate(data):
        for key in ("line", "code", "old", "new"):
            if key not in item:
                raise ValueError("%s: proposal %d is missing `%s`" % (path, i, key))
        item = dict(item)
        item["_source"] = path
        item["_source_index"] = i
        out.append(item)
    return out


def find_match(doc_lines, proposal):
    """Where a proposal's `old` sits in the document right now.

    Returns (start_line, end_line, reason) where start_line/end_line are 1-based and inclusive, and
    reason is None on success or a failure string. Checks the stated line first; when the text there
    does not match, it falls back to a whole-document search and accepts a single unambiguous hit.
    """
    old_lines = proposal["old"].split("\n")
    stated_line = proposal["line"]
    n = len(old_lines)

    def slice_at(start_1based):
        start = start_1based - 1
        end = start + n
        if start < 0 or end > len(doc_lines):
            return None
        return doc_lines[start:end]

    at_stated = slice_at(stated_line)
    if at_stated is not None and "\n".join(at_stated) == proposal["old"]:
        return stated_line, stated_line + n - 1, None

    # Fall back to a whole-document search for exactly one occurrence.
    hits = []
    for start_1based in range(1, len(doc_lines) - n + 2):
        window = slice_at(start_1based)
        if window is not None and "\n".join(window) == proposal["old"]:
            hits.append(start_1based)
    if len(hits) == 1:
        start = hits[0]
        return start, start + n - 1, None
    if len(hits) == 0:
        return None, None, ("`old` does not match the document at line %d, and no exact match "
                             "exists anywhere in the document" % stated_line)
    return None, None, ("`old` does not match the document at line %d, and %d matches exist "
                         "elsewhere in the document — not unambiguous" % (stated_line, len(hits)))


def check_batch(doc_lines, proposals):
    """Every proposal checked against the document and against each other.

    Returns (resolved, failures). `resolved` is a list of dicts carrying each proposal plus its
    matched start_line/end_line, in proposal order. `failures` is a list of human-readable strings,
    one per problem, each naming the proposal's batch index, its code, and its stated line.
    """
    resolved = []
    failures = []
    for idx, p in enumerate(proposals):
        start, end, reason = find_match(doc_lines, p)
        if reason is not None:
            failures.append("proposal %d (%s, stated line %d): %s"
                            % (idx, p.get("code", "?"), p.get("line", "?"), reason))
            continue
        resolved.append(dict(p, _start=start, _end=end, _batch_index=idx))

    # No two proposals may target the same line or overlapping `old` spans. Each proposal's own
    # batch index travels with it (_batch_index), so this never depends on list identity or
    # equality — two proposals can carry identical fields and still be told apart.
    by_span = sorted(resolved, key=lambda r: r["_start"])
    for i in range(1, len(by_span)):
        prev, cur = by_span[i - 1], by_span[i]
        if cur["_start"] <= prev["_end"]:
            failures.append(
                "proposal %d (%s, stated line %d) overlaps proposal %d (%s, stated line %d) at "
                "resolved lines %d-%d vs %d-%d"
                % (cur["_batch_index"], cur.get("code", "?"), cur.get("line", "?"),
                   prev["_batch_index"], prev.get("code", "?"), prev.get("line", "?"),
                   cur["_start"], cur["_end"], prev["_start"], prev["_end"]))

    return resolved, failures


def apply_batch(doc_lines, resolved):
    """The document's lines with every resolved proposal's span replaced, highest line first."""
    lines = list(doc_lines)
    for r in sorted(resolved, key=lambda r: r["_start"], reverse=True):
        start, end = r["_start"] - 1, r["_end"]
        lines[start:end] = r["new"].split("\n")
    return lines


def build_report(doc_path, resolved, before_count, after_count):
    by_code = {}
    for r in resolved:
        by_code.setdefault(r["code"], 0)
        by_code[r["code"]] += 1
    lines = []
    lines.append("# apply-criterion-rewrites report")
    lines.append("")
    lines.append("document: %s" % doc_path)
    lines.append("proposals applied: %d" % len(resolved))
    lines.append("line count: %d -> %d (%+d)" % (before_count, after_count,
                                                   after_count - before_count))
    lines.append("")
    lines.append("| code | count |")
    lines.append("| --- | --- |")
    for code in sorted(by_code):
        lines.append("| %s | %d |" % (code, by_code[code]))
    lines.append("")
    lines.append("| code | line | source | why |")
    lines.append("| --- | --- | --- | --- |")
    for r in sorted(resolved, key=lambda r: r["_start"]):
        why = r.get("why", "").replace("|", "/")
        lines.append("| %s | %d | %s | %s |" % (r["code"], r["_start"], r["_source"], why))
    lines.append("")
    return "\n".join(lines)


def check_git_conflict(doc_path):
    """A warning line when the document already carries uncommitted changes, else None.

    This is informational only (the batch's own match check is the real guard): a modified working
    tree just means the proposals were written against a text that may already have moved.
    """
    try:
        out = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True,
                             cwd=os.path.dirname(os.path.abspath(doc_path)) or ".")
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    changed = set(out.stdout.splitlines())
    base = os.path.basename(doc_path)
    if any(os.path.basename(c) == base for c in changed):
        return ("%s: %s already carries uncommitted changes — proposals may have been drafted "
                "against different text; the batch's match check against the current document is "
                "the real guard here." % (CHECK, doc_path))
    return None


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = argv[1:]
    dry_run = "--dry-run" in flags
    report_path = None
    if "--report" in flags:
        i = flags.index("--report")
        if i + 1 >= len(flags):
            print(usage(argv[0]))
            return 1
        report_path = flags[i + 1]
        args = [a for a in args if a != report_path]

    if len(args) < 2:
        print(usage(argv[0]))
        return 1

    doc_path = args[0]
    proposal_paths = args[1:]

    if not os.path.isfile(doc_path):
        print("%s: cannot read %s — the applier stands on the document file." % (CHECK, doc_path))
        return 1
    for pp in proposal_paths:
        if not os.path.isfile(pp):
            print("%s: cannot read %s — every named proposal file must exist." % (CHECK, pp))
            return 1

    warning = check_git_conflict(doc_path)
    if warning:
        print(warning)

    proposals = []
    for pp in proposal_paths:
        try:
            proposals.extend(load_proposals(pp))
        except (ValueError, json.JSONDecodeError) as e:
            print("%s: %s" % (CHECK, e))
            return 1

    if not proposals:
        print("%s: no proposals in %s — nothing to apply." % (CHECK, ", ".join(proposal_paths)))
        return 1

    with open(doc_path, encoding="utf-8") as f:
        text = f.read()
    had_trailing_newline = text.endswith("\n")
    doc_lines = text.split("\n")
    if had_trailing_newline:
        doc_lines = doc_lines[:-1]

    resolved, failures = check_batch(doc_lines, proposals)

    if failures:
        print("%s: %d failure(s) — nothing written, the batch is refused whole:"
              % (CHECK, len(failures)))
        for f in failures:
            print("  - %s" % f)
        return 1

    before_count = len(doc_lines)
    new_lines = apply_batch(doc_lines, resolved)
    after_count = len(new_lines)

    report = build_report(doc_path, resolved, before_count, after_count)

    if dry_run:
        print("%s: dry run — %d proposal(s) would apply to %s, nothing written."
              % (CHECK, len(resolved), doc_path))
    else:
        new_text = "\n".join(new_lines)
        if had_trailing_newline:
            new_text += "\n"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("%s: %d proposal(s) applied to %s." % (CHECK, len(resolved), doc_path))

    print(report)

    if report_path:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
