"""Row 350 — a remote seat shows textually by construction (the seat law INV-67 sharpened).

A session teleported to the cloud that keeps calling `open` shows into nowhere — the
unopened-window defect one seat later. The remote channel is inline markdown or a host-rendered
artifact page; local-display verbs stay the local seat's arms; the seat is re-detected after any
move between machines.
"""
from conftest import read


def test_remote_show_is_textual_by_construction():
    s = read("skills/communicator/SKILL.md")
    assert "textual by construction" in s
    assert "never attempted from a remote seat" in s
