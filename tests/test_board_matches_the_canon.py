"""The board and the Canon name a task the same way, character for character
(the owner's standing rule: "наш канонический формат и названия тасков — одно и то же,
дословно всегда").

`scripts/state-probe.sh` prints the plain-text Canon a session opens with; `scripts/
render-board.sh` renders every task as `board.html`. Both parse `### <mark> Title — id: <id>`
headings out of PLAN.md's `## Tasks` section through the one shared parser,
`scripts/plan_checks.py`'s `parse_tasks()` — but each still turns a task into its own printed
line independently (a Python heredoc inside a bash script, in each case), and that is where the
two drifted apart once before (the divergence this test was written to catch, PLAN.md step 1).
This test compares what each script actually PRINTS/RENDERS, not the shared parser itself.

Since PLAN.md's task-list merge (commit bc6f862b), the probe shows only the top of the list —
the tasks needing his eyes, in hand, blocked or next up in queue, plus one summary line (the
Canon report this feeds into chat is capped at seven to ten lines; see CLAUDE.md and
scripts/state-probe.sh's own comment) — while the board is a page and can render all of them.
So the two no longer print the SAME SET of titles; what still has to hold is that every title
the probe DOES print also appears, character for character, on the board — the probe can show
less, never something different. `tests/test_tasks_parser_finds_every_task.py` covers the
board's own completeness (every id PLAN.md declares lands on the board) and the probe's
internal bookkeeping (shown + more-below + done == every declared task).

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
# the one home the acceptance-command map lives in (scripts/plan_checks.py), and the generic
# parser/state core both readers reach through it (scripts/plan_checks_core.py).
NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh",
          "scripts/plan_checks.py", "scripts/plan_checks_core.py")

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# state-probe.sh prints one PLAN line per shown task as:
#   "  <id> <icon> <title>  <verified-or-declared>[ — <reason>][  <-- NEXT]"
# (scripts/state-probe.sh's embedded python: `print(f"  {D}{t['id'].ljust(id_width)}{X} "
#  f"{t['icon']} {colour}{t['title']}{X}  {verified}{reason}{tag}")`). The id leads the line
# (his word, 02.09 — it used to trail at the end in parentheses), then the icon — one of the
# plan's five marks — then the title. The trailing tag is one of THREE — "verified", "declared",
# or "marked done" — optionally followed by a ranked ⛔ task's own blocked_by reason (27.08) or
# a failing key's own note (28.08); stripping ANSI colour codes first, then peeling those off
# both ends, leaves exactly the title text.
#
# The third tag arrived on 28.08 with the failing-key mark: a done row whose acceptance command
# fails prints "marked done" rather than "verified". This regex kept the two it knew, so every such
# line was silently DROPPED from the comparison and this test's reach over exactly the rows the
# change introduced was zero — it passed only because all the keys happened to pass. Its sibling in
# tests/test_tasks_parser_finds_every_task.py was taught the third tag that same day and this one
# was not, which is one vocabulary written in two homes and only one of them corrected (the
# adversarial read of 2026-08-31).
_PROBE_LINE_RE = re.compile(
    r"^\S+\s+(?:✅|🔄|🔁|⛔|⬜)\s+(.+?)\s+(?:verified|declared|marked done)"
    r"(?:\s+—\s+.+?)?(?:\s*<-- NEXT)?\s*$"
)

# render-board.sh's card markup: `<div class="handle">Title <span class="chip">...`
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

    def test_every_shown_probe_title_appears_on_the_board(self):
        probe_titles = _probe_titles(self.tmp)
        board_titles = _board_titles(self.tmp)

        self.assertTrue(probe_titles, "the probe printed no task titles — its PLAN-section "
                                       "print shape changed; update _PROBE_LINE_RE")
        self.assertTrue(board_titles, "the board rendered no card titles — its handle markup "
                                       "changed; update _BOARD_HANDLE_RE")
        # The board renders every task PLAN.md declares (checked directly in
        # test_tasks_parser_finds_every_task.py); the probe only shows its top-of-list
        # subset. What has to hold here is character-for-character agreement on the ones the
        # probe DOES show, not equal counts — the probe legitimately shows fewer.
        board_title_set = set(board_titles)
        missing = [t for t in probe_titles if t not in board_title_set]
        self.assertFalse(
            missing,
            "the Canon printed a task title the board doesn't carry, character for character: "
            "%r" % missing,
        )
        self.assertLessEqual(
            len(probe_titles), len(board_titles),
            "the probe printed MORE task lines than the board rendered — it should be showing "
            "a subset of the full list, not more than it",
        )


if __name__ == "__main__":
    unittest.main()
