"""test_board_publish.py — the work board stands at no published address, and is drawn on demand
from its one source file (SPEC spec/work-board.md Requirement 309 criteria 8, 9 and 10; INV-308).

Criterion 8 read the other way until 2026-09-07: the board was published at one stable link, and
GitHub Pages of this repository served exactly the `board.html` that `scripts/render-board.sh`
writes. The owner ended that — «только доску нафига ты выкатил на урл гитхаба? убери оттуда плиз» —
and stated the rule this file now guards: the report he leads every reply with is shown always, the
board is shown on demand, and both are kept current because the board is where the context of every
task is held from one session to the next.

So the thing under test is that nothing draws the board towards an address again: no publishing
workflow, no address in the registry row or the identifier line the page leads with, and no address
anywhere in what the pack ships. The renderer itself is unchanged and still proves out here — a
board drawn from this tree names its own project and carries what the plan records.

RED-PROVED 2026-09-07 against HEAD 26958245, which carried `.github/workflows/pages.yml`, a
registry row naming `https://happysasha18.github.io/live-spec/board.html`, and a rendered page
leading with that same address: every assertion below failed on that tree.
"""
import os
import re
import subprocess

from conftest import ROOT

# The address the board used to stand at. It appears here so the assertions can look for it, and
# it must appear nowhere the pack ships.
RETIRED_URL = "https://happysasha18.github.io/live-spec/board.html"
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")


def render(tmp_path, **env):
    out = os.path.join(str(tmp_path), "board.html")
    r = subprocess.run(["bash", os.path.join(ROOT, "scripts", "render-board.sh"), out],
                       capture_output=True, text=True, env=dict(os.environ, **env))
    assert r.returncode == 0, r.stderr
    with open(out, encoding="utf-8") as fh:
        return fh.read()


def test_no_workflow_publishes_the_board():
    """A workflow that renders the board and hands it to a host is the address coming back."""
    for name in sorted(os.listdir(WORKFLOWS)):
        path = os.path.join(WORKFLOWS, name)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        if "render-board.sh" not in body:
            continue
        assert "pages" not in body.lower().replace("live-spec", ""), (
            "%s draws the board and hands it to a page host — the board is drawn on demand from "
            "this tree and stands at no address (Requirement 309 criterion 8)" % name)


def test_the_registry_row_names_no_address(tmp_path):
    """Criterion 9: the board registers once, and its needle is content rather than a link."""
    with open(os.path.join(ROOT, "SURFACES.md"), encoding="utf-8") as fh:
        registry = fh.read()
    row = [ln for ln in registry.splitlines() if ln.startswith("| work-board |")]
    assert len(row) == 1, "the board registers once, under one name"
    assert "http" not in row[0], "the registry row names an address for a board that has none"
    needle = row[0].split("|")[2].strip()
    assert needle, "the registry row carries no needle for the completeness check to read"
    # The completeness check reads the needle in the pack's rendered artifacts — the set
    # guardrails.config.json names, README.md among them — so that is where it has to stand.
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        assert needle in fh.read(), (
            "the registry needle stands in no rendered artifact, so the completeness check "
            "cannot find the surface it registers")


def test_the_page_leads_with_its_project_and_no_address(tmp_path):
    """Criterion 10: the identifier line names the project and what it needs of the person."""
    page = render(tmp_path)
    head = page[page.index('class="stamp"'):page.index("</div>", page.index('class="stamp"'))]
    assert "http" not in head, "the page leads with an address it no longer stands at"
    assert RETIRED_URL not in page


def test_the_retired_address_is_gone_from_everything_the_pack_ships():
    """A dead address in a shipped document is the first thing a reader walks into."""
    shipped = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs
                   if d not in {".git", "attic", "docs", ".live-spec", "node_modules",
                                ".pytest_cache", ".spec-freeze"}]
        for name in files:
            if name.endswith((".md", ".py", ".sh", ".yml", ".json")):
                shipped.append(os.path.join(base, name))
    offenders = []
    for path in shipped:
        if os.path.abspath(path) == os.path.abspath(__file__):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            if RETIRED_URL in fh.read():
                offenders.append(os.path.relpath(path, ROOT))
    assert not offenders, (
        "these still name the address the board was taken off on 2026-09-07: %s" % offenders)


def test_the_render_reads_the_recorded_marks_when_it_is_told_to(tmp_path):
    """A machine that cannot judge a row must not try.

    Criterion 22 reads an open row's column off the status its queue row records. The renderer also
    re-runs each row's acceptance command, which is worth something only where the state those
    commands reach for actually lives. RED-PROVED 2026-09-06 against HEAD 7993fa9b: rendered in a
    checkout carrying neither the installed pack nor the suite's dependencies, 29 rows the plan
    records as landed drew as 🔁 "was done and is not". That mode stays, for any reader drawing
    this tree somewhere else.
    """
    page = render(tmp_path, LIVE_SPEC_BOARD_CHECKS="off")
    head = page[page.index('class="stamp"'):page.index("</div>", page.index('class="stamp"'))]
    assert "as the plan records it" in head, (
        "the page shows recorded marks and does not tell its reader that is what they are")
    assert not re.search(r"BRIEF-TOKEN", page), "a spawn token reached the page"
