#!/usr/bin/env python3
"""director-wire-report.py — a standalone, read-only, INFORMATIONAL report on how far a
Director decision sheet already covers the commits gate (a) (guardrails/check-prover-record.sh)
would demand a fresh prover record for.

WHAT THIS IS NOT. This script is not called from anywhere — not guardrails/pre-push, not
guardrails/install.sh, not any CI workflow — and it never will be from this script alone. It
never gates a push: its exit code signals only whether the script itself ran cleanly (bad
arguments, git unreadable), never whether any commit is "covered." A real skip of gate (a)
would need a new STAND-DOWN class named in guardrails/check-prover-record.sh, a matching new
PRODUCT_SPEC.md R226 criterion, and an update to tests/test_deletion_only_push.py's
enumeration of both — a spec-level decision that needs the owner's own word, not a guess made
here. This script only reports; see the disclaimer line it always prints.

WHAT IT REPORTS. It resolves the same commit range gate (a) would use — DIFF_BASE from
$LIVE_SPEC_DIFF_BASE if set and valid, else origin/main, else HEAD~1 as a last resort,
mirroring guardrails/check-prover-record.sh:105-119 exactly — then, for each closed checkpoint
under .live-spec/checkpoints/*.md whose file was itself touched by a commit in that range, reads
its ## DECISION SHEET section (via scripts/checkpoint.py's own read_checkpoint, imported rather
than reimplemented) and extracts the "Documents that must change" bullet's body. A body that
scripts/checkpoint.py's own _is_empty_body() calls empty marks every commit that checkpoint file
was touched by, in range, as "covered" — a Director decision already on record, in this run,
that no document needed to change for that work. Everything else stays uncovered.

Note for a reader of the report, not enforced by this script: .live-spec/checkpoints/ is
gitignored in this repository (see .gitignore), so a checkpoint file is normally never itself
part of any commit range, and "covered" will usually be empty here. That is a fact about how
checkpoints are stored today, not something this script papers over.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import checkpoint as checkpoint_mod  # noqa: E402  (module lives next to this script)

DISCLAIMER = (
    "INFORMATIONAL ONLY — this does not affect any gate. Wiring this into gate (a) needs a "
    "new STAND-DOWN class and a PRODUCT_SPEC.md R226 criterion, which needs the owner's "
    "word, not this script."
)

CHECKPOINTS_SUBDIR = Path(".live-spec") / "checkpoints"

_ZERO_SHA = "0" * 40

# The "Documents that must change" bullet as the director skill writes it (skills/director/
# SKILL.md): "- **Documents that must change** — <body>". checkpoint.py's own read_checkpoint
# only splits a checkpoint into its "## " sections — the DECISION SHEET body is free-form prose
# it never parses further, so this sub-line extraction is this script's own, tolerant of a
# missing leading "-", missing bold markers, "-"/":" standing in for the em dash, and — because
# the skill's own worked example (skills/director/SKILL.md:245) writes the field as the short
# "**Documents**" rather than the long "**Documents that must change**" defined elsewhere in the
# same file — either form of the label naming the same field.
#
# Known limitation, not this script's to fix: the skill's own worked example body reads "none.
# The spec already says what should happen" — that does not match _is_empty_body()'s recognized
# empty forms ("", "none", "-", "(nothing...)" exactly), so that literal example still comes back
# "uncovered" here. _is_empty_body() is scripts/checkpoint.py's own function, reused as-is.
_DOC_FIELD_RE = re.compile(
    r"^\s*-?\s*\*{0,2}Documents(?: that must change)?\*{0,2}\s*(?:[—:-]+)\s*(.*)$",
    re.IGNORECASE,
)

# A line starting a new top-level "- **Field**" bullet in the DECISION SHEET section — the
# boundary that ends a multi-line "Documents..." field body (finding 4: a real decision sheet
# often puts the label on its own line with the actual list on the lines below it).
_TOP_LEVEL_BULLET_RE = re.compile(r"^\s*-\s*\*\*")


class ReportError(Exception):
    """A genuine script error (bad args, git unreadable) — never raised for "found nothing"."""


def _run_git(args, cwd):
    try:
        return subprocess.run(
            ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
        )
    except OSError as exc:
        raise ReportError("could not run git %s: %s" % (args, exc)) from exc


def _git_verify_quiet(rev: str, cwd) -> bool:
    return _run_git(["rev-parse", "--verify", "--quiet", rev], cwd).returncode == 0


def resolve_diff_base(repo_root: Path):
    """Mirror guardrails/check-prover-record.sh:105-119 exactly.

    Returns (diff_base, is_last_resort). diff_base is "" if nothing resolves at all — the
    same case that script's own comment says leaves the carve-out (and here, the report)
    unable to judge.
    """
    env_base = os.environ.get("LIVE_SPEC_DIFF_BASE", "")
    if (
        env_base
        and env_base != _ZERO_SHA
        and _git_verify_quiet("%s^{commit}" % env_base, repo_root)
    ):
        return env_base, False
    if _git_verify_quiet("origin/main", repo_root):
        return "origin/main", False
    if _git_verify_quiet("HEAD~1", repo_root):
        return "HEAD~1", True
    return "", False


def commit_range(repo_root: Path, diff_base: str):
    result = _run_git(["rev-list", "%s..HEAD" % diff_base], repo_root)
    if result.returncode != 0:
        raise ReportError("git rev-list %s..HEAD failed: %s" % (diff_base, result.stderr.strip()))
    return [line for line in result.stdout.splitlines() if line.strip()]


def _resolve_sha(repo_root: Path, rev: str) -> str:
    result = _run_git(["rev-parse", rev], repo_root)
    if result.returncode != 0:
        raise ReportError("git rev-parse %s failed: %s" % (rev, result.stderr.strip()))
    return result.stdout.strip()


def commits_touching_path(repo_root: Path, diff_base: str, rel_path: Path):
    result = _run_git(
        ["log", "--format=%H", "%s..HEAD" % diff_base, "--", str(rel_path)], repo_root
    )
    if result.returncode != 0:
        raise ReportError(
            "git log for %s failed: %s" % (rel_path, result.stderr.strip())
        )
    return {line for line in result.stdout.splitlines() if line.strip()}


def extract_documents_field(decision_sheet_body: str):
    """Return the "Documents that must change" (or short-form "Documents") bullet's FULL body
    text, or None if the DECISION SHEET body carries no such line at all (distinct from an
    explicitly empty one).

    The body is not just whatever follows the label on its own line — a real decision sheet
    routinely puts the label alone (em dash, nothing after it) and lists the actual documents
    on the lines below it. The body spans from the label line's tail through every following
    line up to (but not including) whichever comes first: the next top-level "- **Field**"
    bullet in the section, or the end of the section text.
    """
    lines = decision_sheet_body.splitlines()
    for i, line in enumerate(lines):
        m = _DOC_FIELD_RE.match(line)
        if m:
            body_lines = [m.group(1)]
            for cont in lines[i + 1 :]:
                if _TOP_LEVEL_BULLET_RE.match(cont):
                    break
                body_lines.append(cont)
            return "\n".join(body_lines).strip()
    return None


def find_covering_checkpoints(repo_root: Path, diff_base: str):
    """Return (covering_commits, notes).

    covering_commits: the set of commit hashes, in range, covered by a closed checkpoint file
    (itself touched by a commit in range) whose DECISION SHEET says no documents need to
    change, per scripts/checkpoint.py's own _is_empty_body().
    notes: human-readable per-checkpoint lines for the report.
    """
    covering_commits = set()
    notes = []
    checkpoints_dir = repo_root / CHECKPOINTS_SUBDIR
    if not checkpoints_dir.is_dir():
        return covering_commits, notes

    for path in sorted(checkpoints_dir.glob("*.md")):
        rel = path.relative_to(repo_root)
        touching = commits_touching_path(repo_root, diff_base, rel)
        if not touching:
            continue

        try:
            data = checkpoint_mod.read_checkpoint(path)
        except (ValueError, OSError) as exc:
            notes.append(
                "  %s: unreadable (%s) — commits it touches in range stay uncovered" % (rel, exc)
            )
            continue

        if data["status"] != "closed":
            notes.append("  %s: open — commits it touches in range stay uncovered" % rel)
            continue

        body = data["sections"].get(checkpoint_mod.DIRECTOR_SECTION)
        if body is None:
            notes.append(
                "  %s: closed, no ## %s section — commits it touches in range stay uncovered"
                % (rel, checkpoint_mod.DIRECTOR_SECTION)
            )
            continue

        doc_field = extract_documents_field(body)
        if doc_field is None:
            notes.append(
                "  %s: closed, DECISION SHEET has no 'Documents that must change' line — "
                "commits it touches in range stay uncovered" % rel
            )
            continue

        if checkpoint_mod._is_empty_body(doc_field):
            covering_commits |= touching
            notes.append(
                "  %s: closed, 'Documents that must change' says nothing needs to change "
                "-> covers %d commit(s) it touches in range" % (rel, len(touching))
            )
        else:
            notes.append(
                "  %s: closed, 'Documents that must change' is non-empty (%r) -> still "
                "requires the record for the commit(s) it touches in range" % (rel, doc_field)
            )

    return covering_commits, notes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="director-wire-report.py",
        description=(
            "Informational report: which commits in the range gate (a) "
            "(guardrails/check-prover-record.sh) would check are already 'covered' by a "
            "closed Director checkpoint whose decision sheet says no documents need to "
            "change. Reports only — never gates, never skips anything."
        ),
    )
    parser.parse_args(argv)

    repo_root_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if repo_root_result.returncode != 0:
        print("ERROR: not inside a git repository", file=sys.stderr)
        return 2
    repo_root = Path(repo_root_result.stdout.strip())

    try:
        diff_base, is_last_resort = resolve_diff_base(repo_root)
        if not diff_base:
            print("Range: could not resolve (no LIVE_SPEC_DIFF_BASE, no origin/main, no HEAD~1)")
            print()
            print(DISCLAIMER)
            return 0

        commits = commit_range(repo_root, diff_base)
        head_sha = _resolve_sha(repo_root, "HEAD")
        base_sha = _resolve_sha(repo_root, diff_base)
        covering_commits, notes = find_covering_checkpoints(repo_root, diff_base)
        if is_last_resort:
            # gate (a) itself (guardrails/check-prover-record.sh) treats the HEAD~1
            # last-resort base as "a base no real push would ever measure against" and never
            # runs any of its own stand-down reasoning against it. This report holds itself
            # to the same rule: nothing counts as "covered" here either when the base is this
            # unreliable — the "Checkpoints touched in range" notes above stay informational.
            covering_commits = set()
    except ReportError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    print(
        "Range: %s%s (%s) .. HEAD (%s), %d commit(s)"
        % (
            diff_base,
            " [last-resort]" if is_last_resort else "",
            base_sha[:12],
            head_sha[:12],
            len(commits),
        )
    )
    print()

    if notes:
        print("Checkpoints touched in range:")
        for note in notes:
            print(note)
        print()

    covered = [c for c in commits if c in covering_commits]
    uncovered = [c for c in commits if c not in covering_commits]

    print("Covered commits (%d) — a closed, in-range checkpoint says no documents change:" % len(covered))
    if covered:
        for c in covered:
            print("  %s" % c[:12])
    else:
        print("  (none)")
    if is_last_resort:
        print(
            "Note: base resolved via HEAD~1 (last resort) — gate (a) itself treats this base "
            "as unreliable for any stand-down reasoning, so no commit is ever reported "
            "\"covered\" against it."
        )
    print()

    print(
        "Uncovered commits (%d) — not claimed by any covering checkpoint; the single prover "
        "record gate (a) demands for this push still needs to account for them:" % len(uncovered)
    )
    if uncovered:
        for c in uncovered:
            print("  %s" % c[:12])
    else:
        print("  (none)")
    print()

    print(DISCLAIMER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
