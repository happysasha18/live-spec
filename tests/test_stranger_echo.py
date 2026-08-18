"""The stranger arm's echo-and-close law (INV-147/INV-27) — M-337.

M-337 asserts a captured stranger wish is answered on its source too, not just harvested:
the capture echo posted as a comment on the source Issue at harvest, the Issue closed once
its row reaches a terminal exit — extending M-289's no-wish close (a no-wish item is closed
with a recorded note) to the yes-wish case.
"""
from pathlib import Path

from conftest import SPEC, read

REPO = Path(__file__).resolve().parent.parent


def test_stranger_yes_wish_echoes_and_closes_source():
    spec = read(SPEC)     # the whole spec: the core and the parts its map names
    # INV-147's body clause: the captured wish's echo lands as a comment on the source Issue
    # at harvest, and the Issue closes once its row reaches a terminal exit.
    assert "comment on the source Issue" in spec
    # R195.5: "at harvest" as a standalone adverbial is gone; the timing now lives in the same
    # criterion sentence that ties the harvest act to the comment-posting act directly.
    assert "harvest it into a queue row and post the capture echo" in spec
    # R195.6: "closed once its row reaches a terminal exit" becomes the shall-subjunctive
    # "when the row reaches a terminal exit, the system shall close the source Issue".
    assert "the row reaches a terminal exit, the system *shall* close the source Issue" in spec
    # INV-27's body clause carries the bridged-stranger pointer to that same echo.
    assert "bridged in from a stranger's Issue" in spec
