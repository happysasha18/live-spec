"""A rendered page built for one reading is cleared once its moment passes (SPEC INV-286, ROADMAP 494).

A page the renderer builds is built to be read once. Today it stays in the tree until someone
notices it, so a working directory carries several at any moment and the count only grows: four
stood at this repo's own root when the row opened and eleven more under docs/ and prototype/, the
oldest twenty-one days old, one of them a render of a document that no longer exists under that name.

The law: the renderer says which kind a page is. A page carrying the document renderer's generator
mark is transient — built for one reading, cleared once that reading is over. Every other page in
the tree is the artifact itself and stays. A clearing moves the file to the attic with its manifest
line, base rule 10's own road, and says out loud what it moved.

Two machines hold it. `scripts/sweep-rendered.py` performs the clearing; `guardrails/check-rendered-sweep.py`
reds while a transient page still stands. The check rides the suite, where the push chain's own
letters run a..z with every one taken, the same placement the named-reference nets and the
wrong-referral check take.
"""
import json
import os
import re
import stat
import subprocess

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "check-rendered-sweep.py")
SWEEP = os.path.join(ROOT, "scripts", "sweep-rendered.py")
RENDERER = os.path.join(ROOT, "scripts", "render-doc.py")
MARK = "live-spec render-doc"


def _gate(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def _sweep(*args):
    return subprocess.run(["python3", SWEEP, *args], capture_output=True, text=True)


def _page(path, title="a page", rendered=True):
    """A page on disk. `rendered` stamps the renderer's own generator mark, which is what makes a
    page transient; without it the page is an artifact a person built by hand."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mark = "<meta name='generator' content='%s'>" % MARK if rendered else ""
    with open(path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head>%s<title>%s</title></head>"
                "<body><p>%s</p></body></html>" % (mark, title, title))


def _tree(tmp_path, name):
    root = tmp_path / name
    root.mkdir()
    return str(root)


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def _repo(tmp_path, name):
    root = _tree(tmp_path, name)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "worker@example.invalid")
    _git(root, "config", "user.name", "worker")
    return root


# --- both machines ship ---

def test_gate_ships():
    assert os.path.isfile(GATE), "guardrails/check-rendered-sweep.py missing"


def test_mechanism_ships():
    assert os.path.isfile(SWEEP), "scripts/sweep-rendered.py missing"


# --- the renderer stamps the mark the rule reads [R296.1] ---

def test_the_renderer_stamps_its_mark(tmp_path):
    src = tmp_path / "note.md"
    src.write_text("# A note\n\nOne line.\n", encoding="utf-8")
    out = tmp_path / "note.html"
    r = subprocess.run(["python3", RENDERER, str(src), str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    page = out.read_text(encoding="utf-8")
    assert 'name="generator"' in page or "name='generator'" in page, \
        "the renderer stamps no generator mark"
    assert MARK in page, "the renderer's mark does not carry its own name"


def test_the_sweep_reads_the_mark_from_the_renderers_own_home():
    # One home per fact: the sweep imports the wording rather than restating it, so the two
    # files cannot drift apart.
    assert "GENERATOR" in read("scripts/render-doc.py"), "the renderer names no mark constant"
    sweep = read("scripts/sweep-rendered.py")
    assert "render-doc.py" in sweep, "the sweep does not read the mark from the renderer"


# --- the check tells the two kinds apart by the mark [R296.1, R296.2, R296.3] ---

def test_gate_reds_a_marked_page_left_standing(tmp_path):
    # RED-FIRST: a page the renderer produced, still standing past its one reading.
    root = _tree(tmp_path, "standing")
    _page(os.path.join(root, "REPORT.html"))
    r = _gate("--root", root)
    assert r.returncode != 0, "gate passed a rendered page left standing"
    out = r.stdout + r.stderr
    assert "REPORT.html" in out
    assert "INV-286" in out


def test_gate_reds_a_marked_page_anywhere_in_the_tree(tmp_path):
    # The mark travels with the page, so no directory shelters a render.
    root = _tree(tmp_path, "anywhere")
    _page(os.path.join(root, "docs", "decisions", "2026-07-27-morning.html"))
    r = _gate("--root", root)
    assert r.returncode != 0, "a directory sheltered a rendered page from the rule"
    assert "docs/decisions/2026-07-27-morning.html" in (r.stdout + r.stderr)


def test_gate_passes_a_page_the_renderer_did_not_produce(tmp_path):
    # A hand-built decision page, a frozen norm card, a test fixture, a prototype sketch: each
    # is the artifact itself and stays.
    root = _tree(tmp_path, "artifacts")
    # The prototype path is assembled rather than written whole: the prototype fence reads
    # literal paths out of production files, and this test names no real file — every path here
    # is a name inside the temporary tree the test builds.
    sketch = "/".join(("prototype", "work-board-sketch.html"))
    for rel in ("docs/decisions/2026-07-05-research.html", "docs/norms/card.html",
                "tests/fixtures/legibility_red.html", sketch):
        _page(os.path.join(root, *rel.split("/")), rendered=False)
    r = _gate("--root", root)
    assert r.returncode == 0, "gate redded a page nothing regenerates:\n%s" % (r.stdout + r.stderr)


def test_a_projects_built_site_is_left_alone(tmp_path):
    # The failure a directory allowlist causes: `dist/`, `site/`, `node_modules/` and a virtual
    # environment read as pages built for one reading, and a sweep eats a shipped website.
    root = _tree(tmp_path, "host")
    for rel in ("dist/index.html", "dist/about.html", "site/index.html",
                "node_modules/lodash/doc/index.html",
                ".venv/lib/python3.9/site-packages/pip/_vendor/idna/doc.html"):
        _page(os.path.join(root, *rel.split("/")), rendered=False)
    r = _gate("--root", root)
    assert r.returncode == 0, "the rule reached a project's own build output:\n%s" % (
        r.stdout + r.stderr)
    s = _sweep("--root", root)
    assert s.returncode == 0, s.stdout + s.stderr
    assert not os.path.exists(os.path.join(root, "attic")), "the sweep took a project's built site"
    assert os.path.isfile(os.path.join(root, "dist", "index.html"))


def test_a_page_rendered_before_the_mark_is_read_by_its_source(tmp_path):
    # R296.2: the second half of the same evidence — the source document standing beside it. It
    # runs where the tracked-page guard can stand behind it, so the tree is a real repository.
    root = _repo(tmp_path, "legacy")
    _page(os.path.join(root, "docs", "old.html"), rendered=False)
    with open(os.path.join(root, "docs", "old.md"), "w", encoding="utf-8") as f:
        f.write("# Old\n")
    r = _gate("--root", root)
    assert r.returncode != 0, "a pre-mark render with its source beside it went unread"
    assert "docs/old.html" in (r.stdout + r.stderr)


def test_the_legacy_reading_stands_down_where_no_git_covers_the_tree(tmp_path):
    # The source-beside reading is a heuristic: a hand-built page kept beside notes of the same
    # name looks exactly like an old render, and being committed is what tells them apart. Where
    # nothing can make that call, the mark alone decides and the older page stays standing. This
    # is also why a copy of a repository taken without its .git never loses a page.
    root = _tree(tmp_path, "nogit")
    _page(os.path.join(root, "docs", "old.html"), rendered=False)
    with open(os.path.join(root, "docs", "old.md"), "w", encoding="utf-8") as f:
        f.write("# Old\n")
    _page(os.path.join(root, "docs", "fresh.html"))            # carries the mark
    r = _gate("--root", root)
    assert r.returncode != 0, "the marked page went unread in a tree with no git"
    out = r.stdout + r.stderr
    assert "docs/fresh.html" in out, "the mark stopped deciding without git"
    assert "docs/old.html" not in out, "the legacy reading ran with nothing standing behind it"


def test_gate_leaves_the_attic_alone(tmp_path):
    root = _tree(tmp_path, "atticked")
    _page(os.path.join(root, "attic", "REPORT.html"))
    r = _gate("--root", root)
    assert r.returncode == 0, "gate redded a page already resting in the attic:\n%s" % (
        r.stdout + r.stderr)


def test_gate_stays_out_of_the_state_and_harness_homes(tmp_path):
    # R296.12: git's own directory, the harness's worktrees, the host state directory whose files
    # the checkpoint law governs, and the attic itself.
    root = _tree(tmp_path, "outside")
    _page(os.path.join(root, ".git", "x.html"))
    _page(os.path.join(root, ".claude", "worktrees", "lane-1", "REPORT.html"))
    _page(os.path.join(root, ".live-spec", "checkpoints", "draft.html"))
    _page(os.path.join(root, "attic", "old.html"))
    r = _gate("--root", root)
    assert r.returncode == 0, "gate reached past its stated reach:\n%s" % (r.stdout + r.stderr)


def test_a_committed_page_stands_outside_the_reach(tmp_path):
    # RED-FIRST, and the defect this closes was live: the sweep moved five git-tracked committed
    # pages into an attic whose bytes git ignores, so a fresh clone would have lost them. Removing
    # tracked history is a commit with its own gate (R296.11).
    root = _repo(tmp_path, "committed")
    _page(os.path.join(root, "docs", "archive.html"))         # carries the renderer's own mark
    _git(root, "add", "-f", "docs/archive.html")
    _git(root, "commit", "-qm", "the page as committed history")

    r = _gate("--root", root)
    assert r.returncode == 0, "the check redded a page git tracks:\n%s" % (r.stdout + r.stderr)
    s = _sweep("--root", root)
    assert s.returncode == 0, s.stdout + s.stderr
    assert os.path.isfile(os.path.join(root, "docs", "archive.html")), \
        "the sweep moved a page git tracks, which a fresh clone could never recover"


def test_an_uncommitted_page_beside_a_committed_one_is_still_cleared(tmp_path):
    # The reach stops at tracked pages and nowhere wider: an untracked render in the same
    # directory is still cleared.
    root = _repo(tmp_path, "mixed")
    _page(os.path.join(root, "docs", "kept.html"))
    _git(root, "add", "-f", "docs/kept.html")
    _git(root, "commit", "-qm", "kept")
    _page(os.path.join(root, "docs", "fresh.html"))

    r = _gate("--root", root)
    assert r.returncode != 0, "an untracked render went unread beside a tracked one"
    assert "docs/fresh.html" in (r.stdout + r.stderr)
    assert "docs/kept.html" not in (r.stdout + r.stderr)
    _sweep("--root", root)
    assert os.path.isfile(os.path.join(root, "docs", "kept.html"))
    assert not os.path.exists(os.path.join(root, "docs", "fresh.html"))


def test_an_upper_case_extension_is_read_too(tmp_path):
    # RED-FIRST: a case-insensitive filesystem lets REPORT.HTML stand, and a case-exact suffix
    # test would read straight past it.
    root = _tree(tmp_path, "upper")
    _page(os.path.join(root, "REPORT.HTML"))
    r = _gate("--root", root)
    assert r.returncode != 0, "gate read past an upper-case page extension"


def test_a_host_declares_its_own_homes_outside_the_reach(tmp_path):
    # R296.12: the reach is host configuration on INV-224's road.
    root = _tree(tmp_path, "declared")
    with open(os.path.join(root, "guardrails.config.json"), "w", encoding="utf-8") as f:
        json.dump({"rendered_pages": {"outside_reach": ["vendor/"]}}, f)
    _page(os.path.join(root, "vendor", "REPORT.html"))
    r = _gate("--root", root)
    assert r.returncode == 0, "a declared home outside the reach was still swept:\n%s" % (
        r.stdout + r.stderr)


def test_a_malformed_config_falls_back_to_the_pack_defaults(tmp_path):
    root = _tree(tmp_path, "broken")
    with open(os.path.join(root, "guardrails.config.json"), "w", encoding="utf-8") as f:
        f.write("{ this is not json")
    _page(os.path.join(root, ".live-spec", "checkpoints", "draft.html"))
    r = _gate("--root", root)
    assert r.returncode == 0, "a malformed config lost the default reach:\n%s" % (
        r.stdout + r.stderr)


def test_gate_states_its_reach_on_the_green_line(tmp_path):
    # R296.10 names three things the green line owes: the count of pages read, the mark they were
    # read for, and the homes outside the reach. Each is asserted on its own.
    root = _tree(tmp_path, "reach")
    _page(os.path.join(root, "a.html"), rendered=False)
    _page(os.path.join(root, "b.html"), rendered=False)
    r = _gate("--root", root)
    assert r.returncode == 0, r.stdout + r.stderr
    out = r.stdout + r.stderr
    assert re.search(r"\bRead 2 pages\b", out), "the green line does not name the count it read"
    assert MARK in out, "the green line does not name the mark it read for"
    assert "tracks" in out, "the green line does not say tracked pages stand outside the reach"
    for home in (".git", ".claude", ".live-spec"):
        assert home in out, "the green line omits the home %r standing outside the reach" % home


def test_gate_passes_the_real_tree():
    # The row's own evidence: fifteen rendered pages stood in this tree when it opened.
    r = _gate()
    assert r.returncode == 0, "a rendered page still stands in the tree:\n%s" % (
        r.stdout + r.stderr)


# --- the clearing lands in the attic, with its declaration [R296.5, R296.6, R296.7] ---

def test_sweep_moves_a_page_to_the_attic(tmp_path):
    root = _tree(tmp_path, "move")
    _page(os.path.join(root, "REPORT.html"), "a report")
    r = _sweep("--root", root)
    assert r.returncode == 0, r.stdout + r.stderr
    assert not os.path.exists(os.path.join(root, "REPORT.html")), "the page still stands"
    moved = os.path.join(root, "attic", "REPORT.html")
    assert os.path.isfile(moved), "the page did not land in the attic"
    assert "a report" in open(moved, encoding="utf-8").read(), "the page lost its content"


def test_sweep_writes_the_declaration_line(tmp_path):
    root = _tree(tmp_path, "manifest")
    _page(os.path.join(root, "REPORT.html"))
    _sweep("--root", root)
    manifest = open(os.path.join(root, "attic", "MANIFEST.md"), encoding="utf-8").read()
    assert "`REPORT.html`" in manifest, "the manifest does not name the page"
    assert "`attic/REPORT.html`" in manifest, "the manifest does not say where the page went"
    assert re.search(r"\d{4}-\d{2}-\d{2}", manifest), "the manifest line carries no date"
    assert "generator mark" in manifest, "the manifest line does not say why the page moved"


def test_the_manifest_records_each_pages_own_evidence(tmp_path):
    # R296.7: the reason is the evidence the rule actually read, so two pages taken on different
    # grounds do not share one constant sentence.
    root = _repo(tmp_path, "why")            # the legacy reading runs where git can back it
    _page(os.path.join(root, "marked.html"))
    _page(os.path.join(root, "legacy.html"), rendered=False)
    with open(os.path.join(root, "legacy.md"), "w", encoding="utf-8") as f:
        f.write("# Legacy\n")
    _sweep("--root", root)
    manifest = open(os.path.join(root, "attic", "MANIFEST.md"), encoding="utf-8").read()
    marked = [l for l in manifest.split("\n") if "`marked.html`" in l]
    legacy = [l for l in manifest.split("\n") if "`legacy.html`" in l]
    assert marked and "generator mark" in marked[0]
    assert legacy and "source document stood beside it" in legacy[0]


def test_a_halted_sweep_keeps_the_manifest_of_what_it_already_moved(tmp_path):
    # RED-FIRST: a manifest written once after the whole loop loses the provenance of every page
    # already moved when a later move fails, and the attic keeps only a basename.
    root = _tree(tmp_path, "halt")
    _page(os.path.join(root, "AAA.html"), "aaa")
    _page(os.path.join(root, "locked", "BBB.html"), "bbb")
    os.chmod(os.path.join(root, "locked"), stat.S_IRUSR | stat.S_IXUSR)
    try:
        r = _sweep("--root", root)
        assert r.returncode != 0, "the sweep reported success over a page it could not move"
        assert "halted" in (r.stdout + r.stderr).lower()
        manifest_path = os.path.join(root, "attic", "MANIFEST.md")
        assert os.path.isfile(manifest_path), "a halted sweep left no manifest at all"
        manifest = open(manifest_path, encoding="utf-8").read()
        assert "`AAA.html`" in manifest, \
            "the page moved before the failure lost its provenance"
        assert os.path.isfile(os.path.join(root, "locked", "BBB.html")), \
            "the page that could not move was lost"
    finally:
        os.chmod(os.path.join(root, "locked"), stat.S_IRWXU)


def test_an_attic_standing_as_a_file_halts_by_name(tmp_path):
    root = _tree(tmp_path, "atticfile")
    _page(os.path.join(root, "REPORT.html"))
    with open(os.path.join(root, "attic"), "w", encoding="utf-8") as f:
        f.write("not a directory")
    r = _sweep("--root", root)
    assert r.returncode != 0, "the sweep ran over an attic that is a file"
    assert "attic" in (r.stdout + r.stderr)
    assert os.path.isfile(os.path.join(root, "REPORT.html")), "the page was lost"


def test_sweep_says_out_loud_what_it_moved(tmp_path):
    root = _tree(tmp_path, "spoken")
    _page(os.path.join(root, "REPORT.html"))
    r = _sweep("--root", root)
    out = r.stdout + r.stderr
    assert "REPORT.html" in out, "the sweep moved a page without naming it"
    assert "attic" in out, "the sweep never said where the page can be brought back from"


def test_sweep_leaves_an_artifact_standing(tmp_path):
    root = _tree(tmp_path, "spare")
    kept = os.path.join(root, "docs", "decisions", "2026-07-05-research.html")
    _page(kept, rendered=False)
    r = _sweep("--root", root)
    assert r.returncode == 0, r.stdout + r.stderr
    assert os.path.isfile(kept), "the sweep took a page nothing regenerates"


def test_two_pages_sharing_one_basename_take_their_source_dir_first(tmp_path):
    # The one collision law's FIRST move (E-9, base rule 18): the source directory prefixes the
    # basename. The ordinal is the second move and never the first.
    root = _tree(tmp_path, "twins")
    _page(os.path.join(root, "a", "REPORT.html"), "from a")
    _page(os.path.join(root, "b", "REPORT.html"), "from b")
    r = _sweep("--root", root)
    assert r.returncode == 0, r.stdout + r.stderr
    a = os.path.join(root, "attic", "a-REPORT.html")
    b = os.path.join(root, "attic", "b-REPORT.html")
    assert os.path.isfile(a), "the page from a/ did not take its source-directory mark"
    assert os.path.isfile(b), "the page from b/ did not take its source-directory mark"
    assert "from a" in open(a, encoding="utf-8").read()
    assert "from b" in open(b, encoding="utf-8").read()


def test_a_nested_source_dir_flattens_into_the_mark(tmp_path):
    root = _tree(tmp_path, "nested")
    _page(os.path.join(root, "reports", "june", "x.html"))
    _sweep("--root", root)
    assert os.path.isfile(os.path.join(root, "attic", "reports-june-x.html")), \
        "a nested source directory lost its mark"


def test_a_second_clearing_of_one_page_takes_the_ordinal(tmp_path):
    root = _tree(tmp_path, "again")
    _page(os.path.join(root, "REPORT.html"), "first")
    _sweep("--root", root)
    _page(os.path.join(root, "REPORT.html"), "second")
    _sweep("--root", root)
    assert "first" in open(os.path.join(root, "attic", "REPORT.html"), encoding="utf-8").read()
    assert os.path.isfile(os.path.join(root, "attic", "REPORT-2.html")), \
        "the second clearing overwrote the first"
    assert "second" in open(os.path.join(root, "attic", "REPORT-2.html"), encoding="utf-8").read()


def test_a_dry_run_moves_nothing_and_names_each_target(tmp_path):
    root = _tree(tmp_path, "dry")
    _page(os.path.join(root, "a", "REPORT.html"))
    _page(os.path.join(root, "b", "REPORT.html"))
    r = _sweep("--root", root, "--dry-run")
    assert os.path.isfile(os.path.join(root, "a", "REPORT.html")), "a dry run moved a page"
    assert not os.path.exists(os.path.join(root, "attic")), "a dry run wrote to the attic"
    assert "attic/a-REPORT.html" in r.stdout and "attic/b-REPORT.html" in r.stdout, \
        "a dry run did not name each page's own target"


def test_sweep_clears_the_check(tmp_path):
    root = _tree(tmp_path, "clears")
    _page(os.path.join(root, "REPORT.html"))
    assert _gate("--root", root).returncode != 0
    _sweep("--root", root)
    assert _gate("--root", root).returncode == 0, "the sweep did not clear the check's red"


# --- the rendering skill states the walk [R296.4, R296.7] ---
#
# These read the skill BODY, apart from its references, so the body's own sentence is pinned; the
# walk's own page is asserted separately. Reading the whole surface would let either half alone
# satisfy both.

def _walk():
    return read("skills/communicator/references/page-lifecycle.md")


def test_communicator_body_states_the_clearing():
    body = read("skills/communicator/SKILL.md")
    assert "INV-286" in body, "the skill body carries no clearing law"
    assert "CLEARED" in body or "cleared" in body, "the skill body never says a page is cleared"
    assert "references/page-lifecycle.md" in body, "the body points at no clearing walk"


def test_the_walk_states_when_a_page_is_cleared():
    walk = _walk()
    assert "INV-286" in walk, "the walk carries no anchor"
    assert re.search(r"(?i)when a page is cleared", walk), "the walk names no clearing moment"
    assert "harvested" in walk, "the walk omits the answered-decision moment"
    assert "release" in walk, "the walk omits the release sweep"


def test_the_walk_tells_the_two_kinds_apart_by_the_renderer():
    walk = _walk()
    assert "transient" in walk.lower(), "the walk never names the transient kind"
    assert "generator" in walk.lower(), "the walk states no rule the machine can read"
    assert MARK in walk, "the walk does not name the mark itself"


def test_the_walk_names_the_attic_and_what_a_clearing_declares():
    walk = _walk()
    assert "attic" in walk.lower(), "the walk names no recoverable home"
    assert "MANIFEST.md" in walk, "the walk does not say where the declaration lands"


def test_publish_sweeps_the_accumulation_at_a_release():
    text = read("skills/publish/SKILL.md")
    assert "sweep-rendered.py" in text, "the release walk runs no sweep"
    assert "INV-286" in text, "the release walk does not carry the clearing law's anchor"
    assert "communicator rule 5" in text, "the release walk points at no live rule"


def test_the_reach_is_declared_as_host_config():
    with open(os.path.join(ROOT, "guardrails.config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    reach = cfg.get("rendered_pages", {}).get("outside_reach")
    assert reach, "guardrails.config.json declares no reach for the sweep"
    for home in (".git", ".claude", ".live-spec"):
        assert home in reach, "the declared reach omits %r" % home


# --- the law's four document homes ---
#
# Each asserts the law's OWN sentence in that document, so a stray mention of the anchor
# elsewhere in a six-hundred-kilobyte file cannot satisfy it.

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    m = re.search(r"\n## Requirement \d+: A rendered page built for one reading is cleared.*?"
                  r"(?=\n## )", spec, re.S)
    assert m, "PRODUCT_SPEC.md carries no requirement for the clearing law"
    body = m.group(0)
    assert body.count("[INV-286") + body.count(", INV-286") >= 8, \
        "the requirement's criteria do not anchor on INV-286"
    for owed in ("generator mark", "attic", "release", "outside the sweep", "version control tracks"):
        assert owed in body, "the requirement never states %r" % owed


def test_index_carries_the_anchor():
    m = re.search(r"^\| INV-286 \| (.+) \|$", read("PRODUCT_SPEC.index.md"), re.M)
    assert m, "the generated index carries no INV-286 row"
    assert len(m.group(1).split(",")) >= 8, \
        "the index maps INV-286 to fewer criteria than the requirement states"


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    m = re.search(r"### \[node: communicator\].*?(?=\n### \[node: )", arch, re.S)
    assert m, "ARCHITECTURE.md carries no communicator node"
    node = m.group(0)
    owns = re.search(r"\*\*owns\*\* — (.+)", node)
    assert owns and "INV-286" in owns.group(1), "the communicator node does not own INV-286"
    assert "sweep-rendered.py" in node, "the node pins no clearing mechanism"
    assert "check-rendered-sweep.py" in node, "the node pins no clearing check"


def test_matrix_row_covers_the_law():
    m = re.search(r"^\| M-463 \| (.+?) \| (\S+) \| (.+?) \| \*(\w+)\* \|$",
                  read("TEST_MATRIX.md"), re.M)
    assert m, "TEST_MATRIX.md carries no M-463 row"
    fact, level, tests, status = m.groups()
    assert "[INV-286" in fact or "INV-286]" in fact, "the row does not anchor on INV-286"
    assert "never" in fact, "the row states no never side"
    assert level == "string"
    assert status == "built"
    assert "test_gate_reds_a_marked_page_left_standing" in tests, \
        "the row does not name the test that reds a page left standing"
