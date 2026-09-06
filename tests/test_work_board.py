"""The work board — one test per fact in matrix/work-board.md (SPEC spec/work-board.md
Requirement 309, spec/live-status-reporting.md Requirement 310 criterion 10, row q-816).

The board is `scripts/render-board.sh`: the rendered status page this project already drew from
PLAN.md's Canon, grown up into the board Requirement 309 describes. It invents no second source of
state — every field comes from PLAN.md read through the one shared parser, the checkpoints under
`.live-spec/checkpoints/`, the lanes git itself holds, `WAITING.md`, `docs/queue-archive/` and the
surface registry `SURFACES.md`.

Every test below runs against a THROWAWAY TREE built in a temp directory: its own plan, its own
checkpoints, its own git repository with a real lane branch and worktree, its own registry and
waiting list. Nothing here reads or writes the real PLAN.md, and nothing runs this project's own
acceptance commands (the fixture's check map is empty), so the whole file renders the board twice
and finishes in a couple of seconds.

Two facts of the block are NOT covered here and their matrix rows stay *todo*: the periodic
auto-refresh heartbeat halves of M-540 and M-542 are retired on the owner's 2026-09-02 12:46 word
(`.live-spec/turnkey-contract-composed.md:304`) and are tested only as an ABSENCE, and the
statement-validation check (M-531 to M-535) is not built — it is not part of q-816's acceptance.

Red-proved 2026-09-06 against the renderer as it stood before this landing — the four-column
pseudo-kanban, kept at /tmp for the proof and re-runnable by pointing LIVE_SPEC_BOARD_RENDERER at
any earlier copy. All 21 tests fail on it. Eighteen of them fail on their own words: that page
carried no session on a row, no registry needle, no column classes, no card ids, no head collapse,
no lanes, no placement chip, no lane branch, no waiting region, no craft chip, no time pair, no
archive, no step trail, no stage line, no in-work-first order and no empty-board line, and the
craft set lived nowhere. The remaining three (M-519's one-page write, M-540's absent heartbeat,
M-543's no-second-source line) had arms the old page already met, and each of those tests still
fails on its other arms.
"""
import json
import os
import re
import shutil
import subprocess
import time

import pytest

from conftest import ROOT

# The generator under test. The override exists for one purpose: the red-proof, which points this
# at the renderer as it stood before this landing and watches every test below fail.
RENDERER = os.environ.get("LIVE_SPEC_BOARD_RENDERER",
                          os.path.join(ROOT, "scripts", "render-board.sh"))
NORM = os.path.join(ROOT, "docs", "norms", "work-board.html")

# The fixture's own rows. Twelve queued rows stand behind the head so the collapse (criterion 24,
# head nine) has something to collapse; one is deferred, one is parked, one is blocked, one is in
# hand on a lane, and one is closed.
IN_HAND = "\U0001f504"
QUEUED = "⬜"
BLOCKED = "⛔"
DONE = "✅"


def _row(mark, title, task_id, group="Board & visibility", source="owner 2026-09-06, INV-308",
         extra=""):
    return (
        "### %s %s — id: %s\n"
        "**Group:** %s · **Priority:** normal\n"
        "**Source:** %s\n"
        "%s\n"
        "%s\n"
    ) % (mark, title, task_id, group, source, extra, "")


def _plan(rows):
    return "# Plan\n\n## Tasks\n\n" + "\n".join(rows) + "\n"


def _checkpoint(title, owner, status, done, in_progress, next_):
    return (
        "# %s\nStatus: %s\nOwner: %s\n\n"
        "## DONE\n\n%s\n\n"
        "## IN PROGRESS\n\n%s\n\n"
        "## NEXT\n\n%s\n\n"
        "## DECISION SHEET\n\nGoal: %s\nObservable outcome: a page\nDefinition of done: it renders\n"
        "Verification: this test\nProject: fixture\nScope: Board\nSource: the fixture\n"
    ) % (title, status, owner, done, in_progress, next_, title)


ROWS = [
    _row(IN_HAND, "The board shows what is in hand", "q-2",
         source="owner 2026-09-06 — spec/work-board.md Requirement 309",
         extra="\n**Holder:** Builder (sonnet) — lane worker\n\n"
               "One page answers what the agent is doing without anyone asking it.\n\n"
               "- [~] Draw the columns\n"
               "- [ ] Draw the lanes\n"),
    _row(QUEUED, "The parked row keeps its place", "q-3",
         extra="\nA row put aside when a bug jumped the lane.\n"),
    _row(BLOCKED, "The blocked row names its cause", "q-4",
         extra="\n**Holder:** Checker (haiku)\n\n**Blocked by:** outside dependency: the "
               "credential expired\n\nA row stopped by something outside the work.\n"),
    _row(DONE, "The closed row keeps its row", "q-5",
         extra="\nA row that landed and stays on the board.\n"),
    _row(QUEUED, "The deferred row waits on its trigger", "q-6",
         extra="\n**Deferred:** the upstream release ships\n\nA row postponed on a named trigger.\n"),
] + [
    _row(QUEUED, "Queued row number %d" % n, "q-1%02d" % n,
         extra="\nA row waiting in the queue.\n")
    for n in range(1, 13)
]

ARCHIVE_ROW = _row(DONE, "The archived row reads from the archive", "q-9",
                   extra="\nThis row landed and moved off the plan page.\n")


def _run(tree, *args, env=None):
    e = dict(os.environ)
    e["LIVE_SPEC_PROFILE"] = os.path.join(tree, "profile.md")
    e.update(env or {})
    return subprocess.run(["bash", os.path.join(tree, "scripts", "render-board.sh"), *args],
                          capture_output=True, text=True, cwd=tree, env=e)


def _build_tree(tmp_path, plan_rows=None, waiting="an answer you have not read yet",
                surfaces=True, renderer=RENDERER, checkpoints=True):
    tree = str(tmp_path)
    os.makedirs(os.path.join(tree, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(tree, ".live-spec", "checkpoints"), exist_ok=True)
    os.makedirs(os.path.join(tree, "docs", "queue-archive"), exist_ok=True)

    shutil.copy(renderer, os.path.join(tree, "scripts", "render-board.sh"))
    for name in ("plan_checks_core.py", "checkpoint.py"):
        shutil.copy(os.path.join(ROOT, "scripts", name), os.path.join(tree, "scripts", name))
    # The fixture's own check map: empty, so no acceptance command runs and every row reads
    # DECLARED — which is the parser's correct behaviour, not a gap.
    with open(os.path.join(tree, "scripts", "plan_checks.py"), "w", encoding="utf-8") as fh:
        fh.write("from plan_checks_core import evaluate, parse_tasks as _p\n"
                 "CHECKS = {}\n"
                 "def parse_tasks(text):\n    return _p(text, CHECKS)\n")

    with open(os.path.join(tree, "PLAN.md"), "w", encoding="utf-8") as fh:
        fh.write(_plan(plan_rows if plan_rows is not None else ROWS))
    with open(os.path.join(tree, "profile.md"), "w", encoding="utf-8") as fh:
        fh.write("- lanes.cap: 3 — run up to that many lanes in parallel\n")
    with open(os.path.join(tree, "WAITING.md"), "w", encoding="utf-8") as fh:
        fh.write("# The waiting list\n\n## In front of you\n<!-- board:shown -->\n%s\n\n"
                 "## The rest\n<!-- board:list -->\n(nothing waiting)\n" % waiting)
    if surfaces:
        with open(os.path.join(tree, "SURFACES.md"), "w", encoding="utf-8") as fh:
            fh.write("| Surface | Needle | Spec anchors |\n|---|---|---|\n"
                     "| work-board | what is in hand, who runs it, and what it took | "
                     "INV-308, INV-71 |\n")

    if checkpoints:
        cps = os.path.join(tree, ".live-spec", "checkpoints")
        with open(os.path.join(cps, "q-2.md"), "w", encoding="utf-8") as fh:
            fh.write(_checkpoint("The board shows what is in hand", "pipeline", "open",
                                 "(nothing yet)", "Drawing the columns", "Draw the lanes"))
        with open(os.path.join(cps, "q-3.md"), "w", encoding="utf-8") as fh:
            fh.write(_checkpoint("The parked row keeps its place", "pipeline", "open",
                                 "(nothing yet)", "(nothing)", "q-2 took the lane; resume here"))
        with open(os.path.join(cps, "q-4.md"), "w", encoding="utf-8") as fh:
            fh.write(_checkpoint("The blocked row names its cause", "pipeline", "open",
                                 "(nothing yet)",
                                 "Blocked: outside dependency: the credential expired", "wait"))
        with open(os.path.join(cps, "q-5.md"), "w", encoding="utf-8") as fh:
            fh.write(_checkpoint("The closed row keeps its row", "pipeline", "closed",
                                 "Step one shipped, Builder, 40 min\n"
                                 "Step two shipped, Checker, 20 min",
                                 "(nothing)", "(nothing)"))
        # A closed checkpoint's stamps are what the actual is read from: born when the ticket was
        # admitted, written last at the close. Set them a known hour apart.
        path = os.path.join(cps, "q-5.md")
        now = time.time()
        os.utime(path, (now, now))

    with open(os.path.join(tree, "docs", "queue-archive",
                          "%s-closed-rows.md" % time.strftime("%Y-%m-%d")), "w",
              encoding="utf-8") as fh:
        fh.write("# Closed rows\n\n" + ARCHIVE_ROW)
    with open(os.path.join(tree, "docs", "queue-archive", "2026-01-01-closed-rows.md"), "w",
              encoding="utf-8") as fh:
        fh.write("# Closed rows of an earlier month\n\n"
                 + _row(DONE, "An older closed row", "q-8", extra="\nIt landed long ago.\n"))

    # A real git repository with a real lane branch and a real worktree, so the branch and the
    # worktree the board prints are read from git rather than typed onto the row.
    def g(*a):
        subprocess.run(["git", *a], cwd=tree, capture_output=True, text=True)

    g("init", "-q", "-b", "main")
    g("config", "user.email", "fixture@example.com")
    g("config", "user.name", "fixture")
    g("add", "-A")
    g("commit", "-qm", "fixture tree")
    g("branch", "lane/q-2-in-hand")
    g("worktree", "add", "-q", os.path.join(tree, ".worktrees", "lane-q-2"), "lane/q-2-in-hand")
    return tree


@pytest.fixture(scope="module")
def board(tmp_path_factory):
    tree = _build_tree(tmp_path_factory.mktemp("board"))
    r = _run(tree)
    assert r.returncode == 0, r.stderr
    with open(os.path.join(tree, "board.html"), encoding="utf-8") as fh:
        page = fh.read()
    model = json.loads(_run(tree, "--json").stdout)
    return {"tree": tree, "page": page, "model": model}


def cards_html(page):
    """Each card's own HTML block, keyed by row id."""
    out = {}
    for m in re.finditer(r'<div class="card[^"]*" id="card-([^"]+)">(.*?)\n    </div>', page, re.S):
        out[m.group(1)] = m.group(2)
    return out


# --------------------------------------------------------------------------- M-519
def test_m519_one_surface_one_source_file_one_stable_link(board):
    """One rendered status surface under one name, held as one source file, published at one
    stable link — never a second rendered status surface and never a second generator."""
    tree = board["tree"]
    # The generator writes exactly one page, at one path, and re-rendering keeps that path.
    before = set(os.listdir(tree))
    r = _run(tree)
    assert r.returncode == 0
    assert set(os.listdir(tree)) - before == set(), "the render wrote a second file"
    assert "written: board.html" in r.stdout
    # One generator in the pack, not two.
    generators = [n for n in os.listdir(os.path.join(ROOT, "scripts"))
                  if re.search(r"render.*board|board.*render", n)]
    assert generators == ["render-board.sh"], generators
    # The link is registered once, under one name.
    with open(os.path.join(ROOT, "SURFACES.md"), encoding="utf-8") as fh:
        registry = fh.read()
    assert registry.count("| work-board |") == 1, "the board is registered twice or not at all"


# --------------------------------------------------------------------------- M-520
def test_m520_one_board_per_project_every_row_names_its_session(board, tmp_path):
    """One board per host project, every row naming the session that wrote it, and a write that
    re-reads its sources rather than trusting a cache of its own."""
    page, model = board["page"], board["model"]
    for task_id, card in cards_html(page).items():
        assert "session: " in card, "%s names no session" % task_id
    assert model["project"] == os.path.basename(board["tree"])
    # A second project renders its own board, not this one's.
    other = _build_tree(tmp_path)
    assert _run(other).returncode == 0
    with open(os.path.join(other, "board.html"), encoding="utf-8") as fh:
        other_page = fh.read()
    assert os.path.basename(other) in other_page
    assert os.path.basename(board["tree"]) not in other_page
    # A blocked write re-reads and re-applies: the board holds no rows of its own, so a re-render
    # after the plan moves carries the new text and never a stale copy.
    plan = os.path.join(other, "PLAN.md")
    with open(plan, encoding="utf-8") as fh:
        text = fh.read()
    with open(plan, "w", encoding="utf-8") as fh:
        fh.write(text.replace("The board shows what is in hand", "A re-read title"))
    assert _run(other).returncode == 0
    with open(os.path.join(other, "board.html"), encoding="utf-8") as fh:
        again = fh.read()
    cards = cards_html(again)
    assert "A re-read title" in cards["q-2"], "the re-render did not re-read the plan"
    assert "The board shows what is in hand" not in cards["q-2"], \
        "the board served a stale copy of the row"


# --------------------------------------------------------------------------- M-521
def test_m521_identifier_line_and_registry_before_it_renders(board, tmp_path):
    """The board leads with the one-line identifier every opened artifact carries, and registers
    in SURFACES.md before it renders."""
    page = board["page"]
    head = page[page.index("<body"):page.index("</div>", page.index('class="stamp"'))]
    assert os.path.basename(board["tree"]) in head, "the page does not name its project"
    assert "the work board" in head
    assert "what is in hand, who runs it, and what it took" in head, "the registry needle is absent"
    assert "waiting on you" in head, "the line does not say what the board needs of the person"
    # RED-FIRST: a tree whose registry carries no work-board row renders nothing.
    unregistered = _build_tree(tmp_path)
    with open(os.path.join(unregistered, "SURFACES.md"), "w", encoding="utf-8") as fh:
        fh.write("| Surface | Needle | Spec anchors |\n|---|---|---|\n")
    assert not os.path.exists(os.path.join(unregistered, "board.html"))
    r = _run(unregistered)
    assert r.returncode != 0, "the board rendered ahead of its registry row"
    assert "registers before it renders" in r.stderr
    assert not os.path.exists(os.path.join(unregistered, "board.html"))


# --------------------------------------------------------------------------- M-522
def test_m522_form_follows_the_frozen_norm_and_carries_a_timestamped_feed(board):
    """The board's form follows the frozen norm `docs/norms/work-board.html`, and the page shows
    rows in feature language, the work in hand, and a timestamped feed."""
    page = board["page"]
    with open(NORM, encoding="utf-8") as fh:
        norm = fh.read()
    # The structural vocabulary the approved form uses, read out of the frozen copy itself so this
    # test cannot drift from it: every one of these classes must stand on the rendered page.
    for cls in ("col inwork", "col ready", "col validate", "col done", "colhead", "colbody",
                "lane", "lanelbl", "freebox", "chips", "chip est", "chip worker", "chip place",
                "card", "handle", "behav", "doneline", "pile", "empty", "tier"):
        assert 'class="%s' % cls in norm or "class='%s" % cls in norm, \
            "the frozen norm does not use %r — this test is aimed at the wrong form" % cls
        assert 'class="%s' % cls in page or "class='%s" % cls in page, \
            "the page does not carry the norm's %r" % cls
    # Rows read in feature language: the echo-name is the row's own title, not an id.
    assert "The board shows what is in hand" in page
    # The timestamped feed.
    feed = page[page.index("What was written, and when"):]
    assert re.search(r"<span class=['\"]ts['\"]>\d{2}:\d{2}, \d{2}\.\d{2}</span>", feed), \
        "the feed carries no timestamps"


# --------------------------------------------------------------------------- M-523
def test_m523_every_row_stands_in_exactly_one_column(board):
    """The whole queue stands in columns, one column per recorded state, every row in exactly one
    — never a row dropped in silence and never a row in two columns."""
    model = board["model"]
    columns = model["columns"]
    placed = [i for ids in columns.values() for i in ids]
    assert len(placed) == len(set(placed)), "a row stands in two columns at once"
    plan_ids = re.findall(r"— id: (\S+)", open(os.path.join(board["tree"], "PLAN.md"),
                                               encoding="utf-8").read())
    assert set(plan_ids) <= set(placed), \
        "rows dropped from the page: %s" % (set(plan_ids) - set(placed))
    # An open row's column is read off the status its own row records.
    assert "q-2" in columns["inwork"], "an in-hand row is not in the in-work column"
    assert "q-101" in columns["validate"], "a queued row is not awaiting validation"
    assert "q-5" in columns["done"], "a done row is not in the done column"
    # Every id the page shows is on the page.
    page = board["page"]
    for task_id in plan_ids:
        assert 'id="card-%s"' % task_id in page, "%s has no card" % task_id


# --------------------------------------------------------------------------- M-524
def test_m524_far_tier_named_head_collapses_deferred_counted(board):
    """The far tier stands down by name, the queued rows below the runnable head collapse into a
    stated count that opens on the person's act, and the deferred rows show as a stated count with
    each revisit trigger behind an expand — none of them dropped in silence."""
    page, model = board["page"], board["model"]
    assert "The far tier stands down by name" in page
    head = model["queue_head"]
    runnable = [i for i in model["columns"]["validate"] if i not in model["deferred"]]
    assert len(runnable) > head, "the fixture has nothing below the head to collapse"
    m = re.search(r"<summary>(\d+) more queued rows stand below the head — open them</summary>",
                  page)
    assert m, "the queued rows below the head do not collapse into a stated count"
    assert int(m.group(1)) == len(runnable) - head
    # Nothing is dropped: every collapsed row is still on the page, inside the fold.
    for task_id in runnable:
        assert 'id="card-%s"' % task_id in page
    # The deferred rows: a stated count, the trigger behind the expand.
    assert model["deferred"] == ["q-6"], model["deferred"]
    dm = re.search(r"<summary>(\d+) deferred rows — each opens on its own revisit trigger"
                   r"</summary>(.*?)</details>", page, re.S)
    assert dm and int(dm.group(1)) == 1
    assert "the upstream release ships" in dm.group(2), "the revisit trigger is not behind the expand"


# --------------------------------------------------------------------------- M-525
def test_m525_lanes_match_the_cap_free_lanes_read_free_parked_row_kept(board):
    """The in-work column splits into one lane per build lane the cap allows, a lane holding no
    row reads as free, and a parked row stands in the in-work column marked parked, naming the row
    that preempted it — never a lane count diverging from the cap, never a parked row cleared."""
    page, model = board["page"], board["model"]
    assert model["lane_cap"] == 3, "the cap is not read from the profile"
    assert len(model["lane_rows"]) == model["lane_cap"], \
        "the lane count diverges from the cap: %s" % model["lane_rows"]
    # Two lanes are busy: the row in hand, and the blocked row, whose holder still holds its lane.
    assert model["lanes_busy"] == 2
    assert sorted(l["id"] for l in model["lane_rows"] if l["id"]) == ["q-2", "q-4"]
    assert "Lane 1" in page and "Lane 2" in page
    assert "Lane 3 — free" in page, "the free lane does not read as free"
    # The parked row: in the in-work column, marked parked, naming what took its lane.
    assert model["parked"] == ["q-3"], model["parked"]
    assert "q-3" in model["columns"]["inwork"]
    parked_card = cards_html(page)["q-3"]
    assert "parked" in parked_card
    assert "q-2 took the lane" in parked_card


# --------------------------------------------------------------------------- M-526
def test_m526_card_reads_as_a_task_at_a_glance(board):
    """A card reads echo-name first, then the description of the behaviour, then the chips, every
    other detail behind the card — with a placement tag and a spec link on every row."""
    page = board["page"]
    for task_id, card in cards_html(page).items():
        if 'class="doneline"' in card:
            continue  # a closed row is one line by criterion 69, tested under M-537
        order = [card.index('class="handle"'), card.index('class="behav"'),
                 card.index('class="chips"'), card.index("<details>")]
        assert order == sorted(order), "%s does not read echo-name, description, chips" % task_id
        assert "class='chip place'" in card, "%s carries no placement tag" % task_id
        assert "class='chip spec" in card, "%s carries no spec link" % task_id
    live = cards_html(page)["q-2"]
    assert "The board shows what is in hand" in live.split('class="behav"')[0]
    assert "spec/work-board.md" in live, "the row's own spec anchor is not on its card"
    assert "<a href='spec/work-board.md'>" in live, "the spec anchor is not linked"


# --------------------------------------------------------------------------- M-527
def test_m527_in_work_row_shows_its_plan_its_stage_and_its_lane(board):
    """An in-work row shows the steps of its own plan with the stage its record names, and names
    its branch and worktree read from the lane itself — never typed onto the row."""
    card = cards_html(board["page"])["q-2"]
    assert "Draw the columns" in card and "Draw the lanes" in card, "the plan's steps are absent"
    # Each deliverable's line leads with its state mark alone and carries no numbering (crit 37).
    for li in re.findall(r"<li class='subtask'>(.*?)</li>", card):
        assert li.lstrip().startswith("<span class='mark'>"), li
        assert not re.match(r"<span class='mark'>\S+</span>\s*\d+[.)]", li), li
    assert "Stage the record names:</b> Drawing the columns" in card, \
        "the stage is not read from the checkpoint's own record"
    assert "lane/q-2-in-hand" in card, "the lane's branch is not on the row"
    assert "lane-q-2" in card, "the lane's worktree is not on the row"
    model = board["model"]
    assert model["cards"]["q-2"]["branch"] == "lane/q-2-in-hand"
    assert model["cards"]["q-2"]["worktree"], "the worktree was not read from git"


# --------------------------------------------------------------------------- M-528
def test_m528_waiting_region_renders_the_waiting_board(board, tmp_path):
    """The board's waiting region renders WAITING.md and keeps no list of its own, so one clearing
    rule and one gate hold every waiting item."""
    page = board["page"]
    assert "an answer you have not read yet" in page, "the waiting item is not rendered"
    assert "renders WAITING.md" in page, "the region does not say where its items come from"
    # The list is the file's, not the board's: change the file and the region changes.
    other = _build_tree(tmp_path, waiting="a different item entirely")
    assert _run(other).returncode == 0
    with open(os.path.join(other, "board.html"), encoding="utf-8") as fh:
        other_page = fh.read()
    assert "a different item entirely" in other_page
    assert "an answer you have not read yet" not in other_page
    # And the generator keeps no waiting list of its own.
    with open(RENDERER, encoding="utf-8") as fh:
        source = fh.read()
    assert "an answer you have not read" not in source


# --------------------------------------------------------------------------- M-529
def test_m529_each_running_step_names_its_worker_or_says_it_is_unnamed(board):
    """Each running step names its worker by a fixed craft name and icon with a muted tier note,
    read from the record — and a step whose record names no craft is shown unnamed, never guessed."""
    cards = cards_html(board["page"])
    live = cards["q-2"]
    assert "\U0001f528 Builder" in live, "the craft name and icon are not on the running step"
    assert "<span class='tier'>· sonnet</span>" in live, "the tier note is not beside the craft"
    blocked = cards["q-4"]
    assert "\U0001f9ea Checker" in blocked and "haiku" in blocked
    # A row whose record names no craft.
    assert "craft unnamed" in cards["q-101"], "a craft was guessed for a record that names none"
    assert board["model"]["cards"]["q-101"]["craft"] == "craft unnamed"
    # Which worker runs which task reads at one glance across the whole in-work column.
    inwork = board["page"][board["page"].index("col inwork"):board["page"].index("col ready")]
    assert inwork.count("class='chip worker'") >= len(board["model"]["columns"]["inwork"])


# --------------------------------------------------------------------------- M-530
def test_m530_the_craft_set_has_one_home_and_no_skill_name_reaches_a_card(board):
    """The fixed craft set and its icons live in the board's own source file as their one home,
    and the names shown are display names — the pipeline's skill names stay internal."""
    with open(RENDERER, encoding="utf-8") as fh:
        source = fh.read()
    assert re.search(r"(?m)^CRAFTS = \(", source), \
        "the craft set does not live in the board's own source file"
    for craft in ("Reader", "Drafter", "Reviewer", "Builder", "Checker"):
        assert '("%s"' % craft in source
    # One home: no other reader of the plan defines the set.
    for name in os.listdir(os.path.join(ROOT, "scripts")):
        if name == "render-board.sh":
            continue
        path = os.path.join(ROOT, "scripts", name)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            other = fh.read()
        # A DEFINITION, at the start of a line — a key that greps for the name is not a
        # second home for the set.
        assert not re.search(r"(?m)^CRAFTS = \(", other), \
            "%s keeps a second copy of the craft set" % name
    # No internal skill name reaches a worker chip on the page.
    for chip in re.findall(r"<span class='chip worker'>(.*?)</span>", board["page"]):
        assert not re.search(r"test-author|spec-author|product-prover|build-pipeline|communicator",
                             chip), chip


# --------------------------------------------------------------------------- M-536
def test_m536_the_row_carries_the_time_it_was_given_beside_the_time_it_took(board):
    """The estimate is written onto the row and the actual stands beside it at the close.

    NOTHING IN THIS TREE RECORDS AN ESTIMATE — no ticket field, no checkpoint line, no delivery
    report — so what the board must never do is print one anyway. It states the absence per row and
    prints the actual, which the checkpoint's own stamps do carry.
    """
    page, model = board["page"], board["model"]
    for task_id, card in cards_html(page).items():
        assert "chip est" in card or "no estimate recorded" in card, \
            "%s carries no time pair" % task_id
    closed = model["cards"]["q-5"]
    assert closed["estimate"] is None, "an estimate was invented for a row that records none"
    assert closed["actual"], "no actual was read from the closed checkpoint's stamps"
    assert closed["opened"] and closed["closed"], "the end-to-end stamps are missing"
    assert "took %s" % closed["actual"] in page
    live = model["cards"]["q-2"]
    assert live["running"], "an in-work row shows no time so far"
    assert "no estimate recorded" in page, "the page hides that no estimate exists"


# --------------------------------------------------------------------------- M-537
def test_m537_closed_rows_are_kept_and_the_done_column_reads_the_archive(board):
    """Every closed task keeps its row, the done column reads the month's archive with older
    months opening on the person's ask, and each closed row shows its terminal state and its door."""
    page, model = board["page"], board["model"]
    assert "q-5" in model["columns"]["done"], "the plan's own closed row was cleared"
    assert "q-9" in model["columns"]["done"], "the current month's archive is not read"
    assert "q-8" not in model["columns"]["done"], "an older month stands open unasked"
    assert "earlier months — open one" in page, "older months do not open on the person's ask"
    assert "2026-01" in page, "the older month is not named"
    # One line per closed row — mark, echo-name, time pair — the rest behind a fold.
    for task_id in ("q-5", "q-9"):
        card = cards_html(page)[task_id]
        assert 'class="doneline"' in card, "%s is not rendered as one line" % task_id
        assert "<details>" in card
        assert model["cards"][task_id]["terminal"] in ("landed", "declined", "superseded",
                                                       "decided") or task_id == "q-5"
    assert "door not recorded" in page, "a door was invented for rows that record none"


# --------------------------------------------------------------------------- M-538
def test_m538_a_closed_rows_step_trail_is_drawn_from_the_record(board):
    """The trail over the plan's steps — each step's outcome, the worker that ran it and its share
    of the time — is drawn from the record, never composed on the board itself."""
    card = cards_html(board["page"])["q-5"]
    assert "Step one shipped, Builder, 40 min" in card, "the step trail is not on the closed row"
    assert "Step two shipped, Checker, 20 min" in card
    # Drawn from the record, byte for byte: the same lines stand in the checkpoint file.
    with open(os.path.join(board["tree"], ".live-spec", "checkpoints", "q-5.md"),
              encoding="utf-8") as fh:
        record = fh.read()
    for line in ("Step one shipped, Builder, 40 min", "Step two shipped, Checker, 20 min"):
        assert line in record
    assert "Record: <code>" in card, "the closed row does not name where its trail was read"


# --------------------------------------------------------------------------- M-539
def test_m539_the_page_never_stands_stale_against_the_record_it_reports(board, tmp_path):
    """The board updates at every stage change, at take-up and at a worker's spawn and finish, and
    its update rides inside the landing's own commit — so no stage leaves the page stale."""
    tree = _build_tree(tmp_path)
    assert _run(tree).returncode == 0
    cp = os.path.join(tree, ".live-spec", "checkpoints", "q-2.md")
    with open(cp, encoding="utf-8") as fh:
        text = fh.read()
    with open(cp, "w", encoding="utf-8") as fh:
        fh.write(text.replace("Drawing the columns", "Drawing the lanes"))
    assert _run(tree).returncode == 0
    with open(os.path.join(tree, "board.html"), encoding="utf-8") as fh:
        page = fh.read()
    assert "Drawing the lanes" in page and "Drawing the columns" not in page, \
        "a stage change left the page standing stale"
    # The page holds no state of its own, so the one file a landing commits carries the update.
    assert not os.path.exists(os.path.join(tree, "board.json"))
    assert not os.path.exists(os.path.join(tree, ".board-cache"))
    assert "built " in page, "the page does not say when it was drawn"


# --------------------------------------------------------------------------- M-540
def test_m540_a_board_update_delays_no_stage(board, tmp_path):
    """A board update delays no stage it touches.

    The periodic auto-refresh heartbeat this fact once also carried is retired on the owner's
    2026-09-02 12:46 word, so the page's own re-read is tested here as an ABSENCE: no timer, no
    meta refresh, no poll.
    """
    tree = _build_tree(tmp_path)
    start = time.time()
    r = _run(tree)
    elapsed = time.time() - start
    assert r.returncode == 0
    assert elapsed < 5.0, "the board's own render took %.1fs — it would hold a stage back" % elapsed
    with open(os.path.join(tree, "board.html"), encoding="utf-8") as fh:
        page = fh.read()
    for banned in ("setInterval", "setTimeout", "http-equiv=\"refresh\"", "http-equiv='refresh'",
                   "EventSource", "fetch("):
        assert banned not in page, "the retired heartbeat is back on the page: %s" % banned


# --------------------------------------------------------------------------- M-541
def test_m541_one_column_on_a_narrow_screen_with_the_work_in_hand_on_top(board):
    """The board lays out in one column on a narrow screen with the work in hand at the top, every
    control reachable by touch and by keyboard, and the page holds its contrast."""
    page = board["page"]
    assert re.search(r"@media \(max-width: \d+px\) \{[^}]*grid-template-columns: 1fr;", page,
                     re.S), "the board does not fall to one column on a narrow screen"
    # The work in hand is first in the document, so one column puts it at the top.
    assert page.index("col inwork") < page.index("col ready") < page.index("col validate") \
        < page.index("col done")
    # Nothing is reachable only by hover, and every control is natively keyboard-reachable.
    assert ":hover" not in page, "a control is gated behind a hover"
    controls = re.findall(r"<(summary|a|button|input|select)\b", page)
    assert set(controls) <= {"summary", "a"}, set(controls)
    assert "summary:focus-visible" in page, "the page drops the focus ring"
    # Colour is stated for both schemes rather than inherited from the reader's chrome.
    assert "prefers-color-scheme: dark" in page and "--ink" in page and "--bg" in page


# --------------------------------------------------------------------------- M-542
def test_m542_an_empty_board_says_so_and_every_board_carries_its_stamp(board, tmp_path):
    """An empty board says so and shows the queue's head in its place, and every board carries the
    stamp of the time it last updated.

    The page's own five-second re-read this fact once also carried is retired (owner, 2026-09-02
    12:46), and M-540 above proves its absence.
    """
    assert re.search(r"built \d{2}:\d{2}, \d{2}\.\d{2}\.\d{4}", board["page"]), \
        "the page carries no freshness stamp"
    empty = _build_tree(tmp_path, plan_rows=[
        _row(QUEUED, "The head of an idle queue", "q-70", extra="\nNothing is running.\n")],
        checkpoints=False)
    assert _run(empty).returncode == 0
    with open(os.path.join(empty, "board.html"), encoding="utf-8") as fh:
        page = fh.read()
    assert "Nothing is in hand right now" in page, "an empty board reads like a broken one"
    assert "The head of an idle queue" in page, "an empty board does not show the queue's head"
    assert re.search(r"built \d{2}:\d{2}", page)


# --------------------------------------------------------------------------- M-543
def test_m543_the_board_writes_no_history_and_takes_over_no_chat_duty(board):
    """The board writes no history the journal already owns, merges no other project's work in,
    and the chat's own duties stand unreduced."""
    page, model = board["page"], board["model"]
    # Only this project's own rows.
    plan_ids = set(re.findall(r"— id: (\S+)",
                              open(os.path.join(board["tree"], "PLAN.md"), encoding="utf-8").read()))
    shown = {i for ids in model["columns"].values() for i in ids}
    assert shown - plan_ids <= {"q-9"}, "rows from outside this project's plan and archive"
    # The generator reads no journal: the history stays where it lives.
    with open(RENDERER, encoding="utf-8") as fh:
        source = fh.read()
    assert "JOURNAL" not in source, "the board reaches into the journal's own history"
    assert "there is no second source of state" in page, \
        "the page does not say it keeps no second source of state"
    # The chat's own report keeps its scope: the probe still prints its own PLAN block.
    with open(os.path.join(ROOT, "scripts", "state-probe.sh"), encoding="utf-8") as fh:
        probe = fh.read()
    assert "PLAN" in probe and "NEXT" in probe, "the board's arrival reduced the chat's own report"


# --------------------------------------------------------------------------- M-544
def test_m544_the_four_questions_are_answered_from_the_page_alone(board):
    """The board counts as working when the person answers four questions from the page alone:
    what is now being done, who runs what, what was done, and how long each took against its
    estimate. The human read over one real working stretch is the honest level for this row; this
    is its machine half — that each of the four has an answer standing on the page.
    """
    page = board["page"]
    cards = cards_html(page)
    # 1 — what is now being done.
    assert "The board shows what is in hand" in cards["q-2"]
    assert "Stage the record names:" in cards["q-2"]
    # 2 — who runs what.
    assert "\U0001f528 Builder" in cards["q-2"] and "session: " in cards["q-2"]
    # 3 — what was done.
    assert "The closed row keeps its row" in cards["q-5"]
    assert "The archived row reads from the archive" in cards["q-9"]
    # 4 — how long each took against its estimate.
    assert "took " in cards["q-5"]
    assert "no estimate recorded" in cards["q-5"], \
        "the page neither shows an estimate nor says none was recorded"
