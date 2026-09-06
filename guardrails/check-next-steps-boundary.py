#!/usr/bin/env python3
"""Keep NEXT_STEPS as transient resume state, never a second task board (SPEC INV-242)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TASK_SHAPES = (
    ("task section", re.compile(r"(?im)^##+\s+(?:tasks?|forward queue|priorities?)\b")),
    ("task id", re.compile(r"(?i)\b(?:q|plan)-\d+\b")),
    # The board's own six marks, in the one spelling every reader compares against
    # (`scripts/task-admission.py`'s four statuses plus the reopened and needs-your-eyes marks).
    # This used to list ✅🟡⏳🧊⛔ — three of those five have never been board marks, and the
    # three the board writes most (⬜ queued, 🔄 in hand, 🔁 reopened) were missing, so a copied
    # queue of in-hand rows passed the gate that exists to refuse exactly that. Alternation, not
    # a character class: 👁️ is two code points and a class would match only the first.
    ("board row",
     re.compile(r"(?m)^###\s+(?:⬜|🔄|🔁|⛔|✅|👁️)\s+.+?\s+—\s+id:\s*\S+")),
    ("task state", re.compile(r"(?im)^\s*(?:status|priority|next task|queue order)\s*:")),
)


def findings(path: Path) -> list[dict[str, object]]:
    body = path.read_text(encoding="utf-8")
    result: list[dict[str, object]] = []
    for label, pattern in TASK_SHAPES:
        for match in pattern.finditer(body):
            result.append({
                "file": str(path),
                "line": body.count("\n", 0, match.start()) + 1,
                "shape": label,
                "text": match.group(0).strip(),
            })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or [Path("NEXT_STEPS.md"), Path("templates/NEXT_STEPS.template.md")]

    missing = [str(path) for path in paths if not path.is_file()]
    bad = [item for path in paths if path.is_file() for item in findings(path)]
    if missing or bad:
        print(json.dumps({"status": "red", "invariant": "INV-242",
                          "missing": missing, "findings": bad}, ensure_ascii=False))
        return 1
    print("OK: NEXT_STEPS carries transient execution state and no task-board shapes (INV-242).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
