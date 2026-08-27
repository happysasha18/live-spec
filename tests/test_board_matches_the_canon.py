"""The board and the Canon name every task the same way, character for character
(the owner's standing rule: "наш канонический формат и названия тасков — одно и то же,
дословно всегда").

`scripts/state-probe.sh` prints the plain-text Canon a session opens with. `scripts/
render-board.sh` renders the same steps as `board.html`. Both parse `### [mark] N. Title`
headings out of `PLAN.md`, independently, in two different languages (a Python heredoc
inside a bash script, in each case) — nothing stops the two parses from drifting apart, and
they briefly did (a divergence closed alongside this test, see PLAN.md step 1). This test
compares what each script actually PRINTS/RENDERS, not a third reimplementation of the
parsing regex — a change to either script's parsing shows up here without this test itself
needing an update.

Runs against a THROWAWAY COPY of the repo in a temp directory, following the pattern in
tests/test_plan_is_not_executable.py: never touches the real PLAN.md, never mutates the
working tree.
"""
import html
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)

# What a reader needs from the tree to run at all: the plan it reads, the two reader scripts,
# and the one home the acceptance-command map now lives in (scripts/plan_checks.py).
NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh", "scripts/plan_checks.py")

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# state-probe.sh prints one PLAN line per step as:
#   "  <icon> <title> <verified-or-declared>[  <-- NEXT]"
# (scripts/state-probe.sh's embedded python: `print(f"  {icon} {colour}{s['title']}{X} "
#  f"{verified}{tail}")`). The icon is one of a small fixed set and the trailing tag is
# always "verified" or "declared" — stripping ANSI colour codes first, then peeling those
# off both ends, leaves exactly the title text.
_PROBE_LINE_RE = re.compile(
    r"^(?:✅|🔄|⛔|⬜)\s+(.+?)\s+(?:verified|declared)(?:\s*<-- NEXT)?\s*$"
)

# render-board.sh's card markup: `<div class="handle">N. Title <span class="chip">...`
_BOARD_HANDLE_RE = re.compile(r'<div class="handle">(.*?)\s*<span class="chip">')


def _make_repo_copy(tmp):
    for rel in NEEDED:
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)


def _probe_titles(tmp):
    r = subprocess.run(
        ["bash", str(tmp / "scripts" / "state-probe.sh")],
        cwd=str(tmp),
        capture_output=True,
        text=True,
    )
    plain = _ANSI_RE.sub("", r.stdout)
    # Only the "PLAN" section's lines carry step titles; FACTS/ALARM/BLOCKERS lines don't
    # match _PROBE_LINE_RE's icon+tag shape, so scanning the whole output is safe.
    titles = []
    for line in plain.splitlines():
        m = _PROBE_LINE_RE.match(line.strip())
        if m:
            titles.append(m.group(1))
    return titles


def _board_titles(tmp):
    out = tmp / "board.html"
    subprocess.run(
        ["bash", str(tmp / "scripts" / "render-board.sh"), str(out)],
        cwd=str(tmp),
        capture_output=True,
        text=True,
    )
    rendered = out.read_text(encoding="utf-8")
    titles = []
    for m in _BOARD_HANDLE_RE.finditer(rendered):
        # The board HTML-escapes titles for display (an em dash or an apostrophe survives
        # unescaped, but "&", "<", ">" would come back as entities) — unescape here so the
        # comparison is against the underlying text, not the markup.
        titles.append(html.unescape(m.group(1)))
    return titles


class TestBoardTitlesMatchTheCanon(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)
        _make_repo_copy(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_both_readers_find_the_same_titles(self):
        probe_titles = _probe_titles(self.tmp)
        board_titles = _board_titles(self.tmp)

        self.assertTrue(probe_titles, "the probe printed no step titles — its PLAN-section "
                                       "print shape changed; update _PROBE_LINE_RE")
        self.assertTrue(board_titles, "the board rendered no card titles — its handle markup "
                                       "changed; update _BOARD_HANDLE_RE")
        self.assertEqual(
            len(probe_titles), len(board_titles),
            "the probe and the board found a different NUMBER of step titles: "
            "%r vs %r" % (probe_titles, board_titles),
        )
        self.assertEqual(
            sorted(probe_titles), sorted(board_titles),
            "the Canon and the board disagree on a task's title, character for character",
        )


if __name__ == "__main__":
    unittest.main()
