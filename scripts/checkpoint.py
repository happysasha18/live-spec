#!/usr/bin/env python3
"""Deterministic parsing, validation, and writing of `.live-spec/checkpoints/*.md` files.

A checkpoint used to be pure convention: free-form markdown that nothing on disk validated,
where `Status`/`DONE`/`IN PROGRESS`/`NEXT` were habits an agent followed when it remembered
to. This module makes the format mechanical:

  - `read_checkpoint` parses a file into its structural pieces, raising `ValueError` only on
    structural breakage (no `# ` title, no `Status:`/`Owner:` key, a bad `Status:` value, a
    duplicate section header, or a `## ` header outside the closed set of recognized section
    names) — a well-formed file merely missing a *required* section still parses cleanly.
    The recognized `## ` headers are a closed allowlist — DONE, IN PROGRESS, NEXT, DECISION
    SHEET, and WATCHED (a pre-existing "workshop noise" ledger convention) — precisely so
    that unfinished-work text can never hide from validation inside an ad hoc heading nobody
    checks; an unrecognized header is a parse-time error, not a silently-ignored section.
  - `validate_checkpoint` checks the semantic rules (DONE/IN PROGRESS/NEXT present, DECISION
    SHEET present when director-owned, closed checkpoints carry no open work) and returns a
    list of issue strings.
  - `new_checkpoint` writes a fresh, valid, open checkpoint.
  - `close_checkpoint` mechanically enforces "a landing that ships a checkpoint's items flips
    that checkpoint to its closed state" — previously just prose nobody checked.

Pure standard library, importable with no side effects (the CLI only runs under
`if __name__ == "__main__":`).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_SECTIONS = ("DONE", "IN PROGRESS", "NEXT")
DIRECTOR_SECTION = "DECISION SHEET"

# WATCHED is the one section name that is neither required nor director-only: a pre-existing
# "workshop noise" ledger convention already used by worker checkpoints in this project. It
# stays allowed but, like before, ignored by validate_checkpoint. Together with the required
# and director sections, this is the CLOSED set of `## ` headers a checkpoint may contain —
# read_checkpoint rejects any header outside it, so unfinished-work text can never hide inside
# an ad hoc heading that nothing checks.
_OTHER_ALLOWED_SECTIONS = ("WATCHED",)
ALLOWED_SECTIONS = set(REQUIRED_SECTIONS) | {DIRECTOR_SECTION} | set(_OTHER_ALLOWED_SECTIONS)

_EMPTY_PLACEHOLDERS = {"", "none", "-"}


def _is_director_owned(owner: str) -> bool:
    return owner.strip().lower().startswith("director")


def _is_empty_body(body: str) -> bool:
    """True if `body` (already stripped) is empty or a recognized placeholder.

    Recognized placeholder forms (case-insensitive): "", "(nothing)", "(nothing — ...)",
    "none", "-" alone on a line. Anything else counts as non-empty content.
    """
    stripped = body.strip()
    if stripped.lower() in _EMPTY_PLACEHOLDERS:
        return True
    lowered = stripped.lower()
    if lowered.startswith("(nothing") and lowered.endswith(")"):
        return True
    return False


def read_checkpoint(path) -> dict:
    """Parse the checkpoint file at `path` into its structural pieces.

    Returns a dict with keys: title (str), status ("open"/"closed"), owner (str),
    sections (dict of header text -> stripped body text), is_director_owned (bool).

    Raises ValueError only on structural breakage: missing `# ` title line, missing
    Status:/Owner: metadata key, a Status: value that is not open/closed, a duplicate
    `## ` section header, or a `## ` header whose text is not one of the closed set of
    recognized section names (ALLOWED_SECTIONS: DONE, IN PROGRESS, NEXT, DECISION SHEET,
    WATCHED) — a checkpoint may not carry a hidden, unchecked section. A file that is
    well-formed but simply lacks a required section (DONE/IN PROGRESS/NEXT/DECISION SHEET)
    still parses — that gap is validate_checkpoint's job to flag, not read_checkpoint's.
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or not lines[0].startswith("# ") or not lines[0][2:].strip():
        raise ValueError("missing '# ' title line")
    title = lines[0][2:].strip()

    # Metadata block: immediately after the title line, "Key: value" lines until the
    # first blank line (or a "## " section header, or end of file).
    idx = 1
    metadata: dict = {}
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "" or line.startswith("## "):
            break
        if ":" not in line:
            raise ValueError("malformed metadata line (expected 'Key: value'): %r" % line)
        key, _, value = line.partition(":")
        metadata[key.strip()] = value.strip()
        idx += 1

    if "Status" not in metadata:
        raise ValueError("missing required metadata key: Status:")
    if "Owner" not in metadata:
        raise ValueError("missing required metadata key: Owner:")

    status = metadata["Status"]
    if status not in ("open", "closed"):
        raise ValueError(
            "Status: value must be exactly 'open' or 'closed', got %r" % status
        )

    owner = metadata["Owner"]
    if not owner:
        raise ValueError("Owner: value must be non-empty")

    # Remainder of the file: "## " sections, in whatever order they appear.
    remainder = "\n".join(lines[idx:])
    sections: dict = {}
    header = None
    body_lines: list = []

    def _flush():
        if header is not None:
            body = "\n".join(body_lines).strip()
            if header in sections:
                raise ValueError("duplicate section header: ## %s" % header)
            sections[header] = body

    for line in remainder.splitlines():
        if line.startswith("## "):
            _flush()
            header = line[3:].strip()
            if header not in ALLOWED_SECTIONS:
                raise ValueError("unrecognized section header: ## %s" % header)
            body_lines = []
        else:
            if header is not None:
                body_lines.append(line)
    _flush()

    return {
        "title": title,
        "status": status,
        "owner": owner,
        "sections": sections,
        "is_director_owned": _is_director_owned(owner),
    }


def validate_checkpoint(path) -> list:
    """Check the semantic rules on the checkpoint at `path`.

    Calls read_checkpoint first, letting a ValueError propagate (a caller can catch parse
    failures separately from a non-empty issues list). Returns a list of human-readable
    issue strings; an empty list means the checkpoint is valid.
    """
    data = read_checkpoint(path)
    sections = data["sections"]
    issues = []

    for name in REQUIRED_SECTIONS:
        if name not in sections:
            issues.append("missing required section: ## %s" % name)

    if data["is_director_owned"]:
        body = sections.get(DIRECTOR_SECTION)
        if body is None or not body.strip():
            issues.append(
                "director-owned checkpoint is missing a non-empty ## %s section"
                % DIRECTOR_SECTION
            )

    if data["status"] == "closed":
        for name in ("IN PROGRESS", "NEXT"):
            body = sections.get(name, "")
            if not _is_empty_body(body):
                issues.append(
                    "closed checkpoint still has an open %s section" % name
                )

    return issues


def new_checkpoint(path, title: str, owner: str, decision_sheet=None) -> None:
    """Write a fresh, valid, open checkpoint file to `path`.

    DONE/IN PROGRESS/NEXT each get the placeholder "(nothing yet)". If `owner` is
    director-owned and `decision_sheet` is given, it is written verbatim as the DECISION
    SHEET body; director-owned without a decision_sheet raises ValueError, as does passing
    a decision_sheet for a non-director owner.
    """
    if not title or not title.strip():
        raise ValueError("title must be non-empty")
    if not owner or not owner.strip():
        raise ValueError("owner must be non-empty")

    director_owned = _is_director_owned(owner)

    if director_owned:
        if not decision_sheet:
            raise ValueError(
                "a director-owned checkpoint cannot be created without decision_sheet"
            )
    else:
        if decision_sheet is not None:
            raise ValueError(
                "decision_sheet must not be given for a non-director-owned checkpoint"
            )

    lines = [
        "# %s" % title,
        "Status: open",
        "Owner: %s" % owner,
        "",
        "## DONE",
        "",
        "(nothing yet)",
        "",
        "## IN PROGRESS",
        "",
        "(nothing yet)",
        "",
        "## NEXT",
        "",
        "(nothing yet)",
        "",
    ]

    if director_owned:
        lines.append("## %s" % DIRECTOR_SECTION)
        lines.append("")
        lines.append(decision_sheet.strip())
        lines.append("")

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def close_checkpoint(path) -> None:
    """Flip the checkpoint at `path` from open to closed, in place.

    Raises ValueError if already closed, or if IN PROGRESS or NEXT still has non-empty
    content (the caller must clear it first — content is never silently discarded). On
    success, rewrites the file with "Status: closed" in place of "Status: open", leaving
    every other byte unchanged (same title, owner, section bodies, and section order).
    """
    data = read_checkpoint(path)

    if data["status"] == "closed":
        raise ValueError("checkpoint is already closed: %s" % path)

    for name in ("IN PROGRESS", "NEXT"):
        body = data["sections"].get(name, "")
        if not _is_empty_body(body):
            raise ValueError(
                "checkpoint still has open work in ## %s — clear it before closing" % name
            )

    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n").rstrip("\r")
        if stripped.startswith("Status:") and stripped[len("Status:"):].strip() == "open":
            newline = line[len(stripped):]  # preserve original line ending, if any
            lines[i] = "Status: closed" + newline
            break
    else:
        raise ValueError("could not locate 'Status: open' line to rewrite")

    Path(path).write_text("".join(lines), encoding="utf-8")


def _cli_validate_one(path: Path) -> bool:
    """Validate one file, printing ISSUE:/OK:/ERROR: lines. Returns True if clean."""
    try:
        issues = validate_checkpoint(path)
    except ValueError as exc:
        print("ERROR: %s: %s" % (path, exc))
        return False
    if issues:
        for issue in issues:
            print("ISSUE: %s" % issue)
        return False
    print("OK: %s" % path)
    return True


def _cli_validate(args) -> int:
    if args.all:
        repo_root = Path(__file__).resolve().parent.parent
        checkpoint_dir = repo_root / ".live-spec" / "checkpoints"
        files = sorted(checkpoint_dir.glob("*.md"))
        all_clean = True
        for f in files:
            if not _cli_validate_one(f):
                all_clean = False
        return 0 if all_clean else 1
    else:
        return 0 if _cli_validate_one(Path(args.path)) else 1


def _cli_new(args) -> int:
    try:
        new_checkpoint(
            Path(args.path),
            title=args.title,
            owner=args.owner,
            decision_sheet=args.decision_sheet,
        )
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 1
    print("wrote: %s" % args.path)
    return 0


def _cli_close(args) -> int:
    try:
        close_checkpoint(Path(args.path))
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 1
    print("closed: %s" % args.path)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="checkpoint.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="validate one or all checkpoints")
    p_validate.add_argument("path", nargs="?", default=None)
    p_validate.add_argument("--all", action="store_true")
    p_validate.set_defaults(func=_cli_validate)

    p_new = sub.add_parser("new", help="write a fresh, valid, open checkpoint")
    p_new.add_argument("path")
    p_new.add_argument("--title", required=True)
    p_new.add_argument("--owner", required=True)
    p_new.add_argument("--decision-sheet", dest="decision_sheet", default=None)
    p_new.set_defaults(func=_cli_new)

    p_close = sub.add_parser("close", help="flip an open checkpoint to closed")
    p_close.add_argument("path")
    p_close.set_defaults(func=_cli_close)

    args = parser.parse_args(argv)
    if args.command == "validate" and args.path is None and not args.all:
        parser.error("either a path or --all is required")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
