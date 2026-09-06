"""test_board_publish.py — the work board is published at one stable link, from its one source file
(SPEC spec/work-board.md Requirement 309 criteria 8, 9 and 10; INV-308, INV-67).

Criterion 8 asks for ONE stable link the person opens from any device, updated FROM the board's own
source file. The owner's decision (2026-09-06) names that link: GitHub Pages of this repository,
serving exactly the `board.html` that `scripts/render-board.sh` writes. So the thing under test is
not "a page exists somewhere" — it is that the published bytes have no second author:

  * the workflow renders with the repository's own renderer, not a copy of it;
  * it uploads a directory holding that one file and nothing else, so no index, no second page and
    no committed artifact can drift from what the renderer said;
  * the same canonical URL string stands in the surface registry AND in the identifier line the
    rendered page leads with (criteria 9 and 10), so a reader of either can reach the other.

RED-PROVED 2026-09-06 against HEAD 4a1579d0, which carried no `.github/workflows/pages.yml` at all
and a `work-board` registry row whose needle matched nothing in the rendered content: every
assertion below failed on that tree, and `check_completeness.py` was red on the same registry row.
"""
import os
import re
import subprocess

import pytest
import yaml

from conftest import ROOT

URL = "https://happysasha18.github.io/live-spec/board.html"
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "pages.yml")


@pytest.fixture(scope="module")
def workflow():
    assert os.path.isfile(WORKFLOW), (
        "no publishing workflow — the board has a source file and no stable link (criterion 8)")
    with open(WORKFLOW, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    # YAML 1.1 reads a bare `on:` key as the boolean True; GitHub reads it as the trigger block.
    doc["on"] = doc.pop("on", doc.pop(True, None))
    return doc


def _steps(workflow):
    jobs = workflow["jobs"]
    assert len(jobs) == 1, "one job publishes the board; a second job is a second author"
    return next(iter(jobs.values()))


def test_the_workflow_publishes_from_the_repositorys_own_renderer(workflow):
    job = _steps(workflow)
    run = "\n".join(s.get("run", "") for s in job["steps"])
    assert "scripts/render-board.sh" in run, (
        "the page must be drawn by the board's own source file, never by a copy of it")
    # No second source of truth: nothing checks out, downloads or copies a board from elsewhere.
    assert not re.search(r"\bcurl\b|\bwget\b|board\.html.*(?:scp|rsync)", run), (
        "the published page comes from this tree alone")


def test_it_deploys_only_board_html(workflow):
    job = _steps(workflow)
    upload = next(s for s in job["steps"] if "upload-pages-artifact" in (s.get("uses") or ""))
    path = upload["with"]["path"]
    run = "\n".join(s.get("run", "") for s in job["steps"])
    assert re.search(r'ls -A %s\)" = "board\.html"' % re.escape(path.rstrip("/")), run), (
        "the uploaded directory must be asserted to hold board.html and nothing else — the "
        "canonical URL names the file, so an index.html would be a second unregistered page")
    assert "index.html" not in run, "no index page is invented beside the board"
    assert any("deploy-pages" in (s.get("uses") or "") for s in job["steps"])


def test_it_runs_on_main_and_pins_every_action(workflow):
    assert workflow["on"]["push"]["branches"] == ["main"]
    assert "workflow_dispatch" in workflow["on"], "a hand-run redraws the page without a push"
    perms = workflow["permissions"]
    assert perms["pages"] == "write" and perms["id-token"] == "write"
    assert _steps(workflow)["environment"]["name"] == "github-pages"
    for step in _steps(workflow)["steps"]:
        uses = step.get("uses")
        if uses:
            assert re.search(r"@(v\d+|[0-9a-f]{40})$", uses), (
                "unpinned action %r — a moving ref changes what gets published" % uses)


def test_one_canonical_url_in_the_registry_and_in_the_rendered_page(tmp_path):
    with open(os.path.join(ROOT, "SURFACES.md"), encoding="utf-8") as fh:
        registry = fh.read()
    row = [ln for ln in registry.splitlines() if ln.startswith("| work-board |")]
    assert len(row) == 1, "the board registers once, under one name"
    assert URL in row[0], "the registry row does not name the canonical link (criterion 9)"

    out = os.path.join(str(tmp_path), "board.html")
    r = subprocess.run(["bash", os.path.join(ROOT, "scripts", "render-board.sh"), out],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    with open(out, encoding="utf-8") as fh:
        page = fh.read()
    head = page[page.index('class="stamp"'):page.index("</div>", page.index('class="stamp"'))]
    assert URL in head, (
        "the identifier line the page leads with does not carry the canonical link (criterion 10) "
        "— it prints the registry needle, so the needle is where the link belongs")
    assert page.count(URL) == 1, "the link stands once on the page, not repeated into a second home"


def test_the_published_render_reads_the_recorded_marks_and_says_so(workflow, tmp_path):
    """The runner that draws the public page cannot judge a row, so it must not try.

    Criterion 22 reads an open row's column off the status its queue row records. The renderer
    also re-runs each row's acceptance command, which is worth something only on the machine that
    owns the state those commands reach for. RED-PROVED 2026-09-06 against HEAD 7993fa9b: rendered
    in a checkout without this machine's installed pack or test dependencies — the shape of the
    Pages runner — 29 rows the plan records as landed drew as 🔁 "was done and is not" and stood
    in the in-work column of the page published at the project's one public link.
    """
    step = [s for s in _steps(workflow)["steps"] if "render-board.sh" in (s.get("run") or "")]
    assert len(step) == 1, "the publishing workflow renders once"
    assert (step[0].get("env") or {}).get("LIVE_SPEC_BOARD_CHECKS") == "off", (
        "the Pages job re-runs every row's acceptance command on a machine that carries neither "
        "the installed pack nor the suite — a verdict about the runner published as a verdict "
        "about the work")

    out = os.path.join(str(tmp_path), "board.html")
    env = dict(os.environ, LIVE_SPEC_BOARD_CHECKS="off")
    r = subprocess.run(["bash", os.path.join(ROOT, "scripts", "render-board.sh"), out],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    with open(out, encoding="utf-8") as fh:
        page = fh.read()
    head = page[page.index('class="stamp"'):page.index("</div>", page.index('class="stamp"'))]
    assert "as the plan records it" in head, (
        "the page shows recorded marks and does not tell its reader that is what they are")
