"""The one reader of an inbox letter's own state.

Before this, a letter's state was guessed: its position (inbox/ open, inbox/handled/ done) plus a
prose section eight of the eleven archived letters never wrote. A cancelled letter read the same
as a live one, and a noted letter read the same as an untouched one. Now a letter carries a
`Status:` line, and — when the state is `superseded` — a `Superseded-by:` line naming the letter
that replaces it. This module is the one home for reading those two lines; every reader of a
letter's state calls in here rather than growing its own copy (`scripts/state-probe.sh`'s INBOX
block and its row line, and `scripts/task-admission.py`'s admission).

A letter written before this line existed carries none, and still reads: OPEN where it stands
in the inbox root, HANDLED where it stands in the root's `handled/` folder. Nothing here rewrites
an existing letter — a caller that wants to move a letter to a new state edits the file itself,
the same way any other inbox deposit is written.
"""
from __future__ import annotations

import re
from pathlib import Path

OPEN, HANDLED, NOTED, SUPERSEDED = "open", "handled", "noted", "superseded"
STATES = (OPEN, HANDLED, NOTED, SUPERSEDED)

_STATUS_RE = re.compile(r"(?m)^Status:\s*(\S+)\s*$")
_SUPERSEDED_BY_RE = re.compile(r"(?m)^Superseded-by:\s*(\S+)\s*$")


class InboxLifecycleError(ValueError):
    """A letter's own Status/Superseded-by lines do not hold together. The message names the
    fault in plain words; nothing here guesses past it."""


def find_letter(inbox_root, filename: str):
    """Where a letter named `filename` actually sits: open in `inbox_root`, or archived under
    `inbox_root/handled`. None where it is in neither.

    This is also how a `Superseded-by:` reference and an admission's own recorded letter are
    checked against disk — a name that resolves to nothing here names nothing anywhere.
    """
    root = Path(inbox_root)
    for candidate in (root / filename, root / "handled" / filename):
        if candidate.is_file():
            return candidate
    return None


def read_state(inbox_root, filename: str) -> dict:
    """The letter's own state: `{"state", "superseded_by", "path"}`.

    Read from the `Status:` line the letter carries, one of the four words in `STATES`. A letter
    with none reads by where it stands, unedited: OPEN under `inbox_root`, HANDLED under
    `inbox_root/handled`.
    """
    path = find_letter(inbox_root, filename)
    if path is None:
        raise InboxLifecycleError(
            "%s is not on disk under %s or %s/handled" % (filename, inbox_root, inbox_root))
    text = path.read_text(encoding="utf-8")
    m = _STATUS_RE.search(text)
    if not m:
        state = HANDLED if path.parent.name == "handled" else OPEN
        return {"state": state, "superseded_by": None, "path": path}
    word = m.group(1).strip().lower()
    if word not in STATES:
        raise InboxLifecycleError(
            "%s names Status: %s, which is none of %s" % (filename, word, ", ".join(STATES)))
    sm = _SUPERSEDED_BY_RE.search(text)
    successor = sm.group(1).strip() if sm else None
    if word != SUPERSEDED:
        return {"state": word, "superseded_by": None, "path": path}
    if not successor:
        raise InboxLifecycleError(
            "%s is Status: superseded with no Superseded-by naming what replaced it" % filename)
    if find_letter(inbox_root, successor) is None:
        raise InboxLifecycleError(
            "%s names Superseded-by: %s, which is not on disk" % (filename, successor))
    return {"state": word, "superseded_by": successor, "path": path}
