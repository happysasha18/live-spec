# -*- coding: utf-8 -*-
"""The spoken setup entry — a sentence in plain words sets a project up on the pack.

SPEC Requirement 308 · INV-307 · matrix rows M-512 through M-518 · ROADMAP row 557.
The orchestrating session lands those documents; this file is the proof they cite.

WHAT IS UNDER TEST. The pack promises that a person who has installed it says "attach live-spec to
this project" or "found a new project on live-spec" and the right setup walk runs. Three pieces make
that real: one arm on `build-pipeline`'s description that a spoken sentence loads, a routing card at
`skills/build-pipeline/references/project-setup.md` that resolves the pack's own tree and picks the
walk, and `adopt/START.md`, the founding walk for a tree with no code and no documents.

THE CASES, and the matrix row each carries:

    M-512  case A  the spoken entry reaches one skill (the presence floor)
    M-513  case B  the routing card ships with the skill and holds no phases
    M-514  case C  the founding walk exists and points where it must
    M-515  case D  the request set can place all three setup sentences
    M-516  case E  the pack's own tree stays reachable on both install routes
    M-517  case F  a founding runs on a throwaway tree (the deed)
    M-518  case G  the arm loads on the sentences people say — scored in `evals/build-pipeline.md`;
                   the floor here is that the scored list stands written where a later session can
                   audit it against the shipped description field

THE RED, watched before any of the three pieces was built (2026-08-06):

    22 failed, 2 passed

    the description fields carry no setup arm; skills/build-pipeline/references/project-setup.md
    does not exist; adopt/START.md does not exist; the request-kind table has no setup row;
    docs/adoption.md still says a person copies the templates by hand.

CASE F RUNS A FOUNDING. It builds a throwaway home under a temporary directory that mirrors the real
plugin-cache layout, `<home>/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, with an
`installed_plugins.json` in the shape this machine's own file uses, and an empty project beside it.
The driver below reads the copy table out of the resolved tree's `adopt/START.md`, so the walk stays
the one home of what lands where and the driver is only a reader of it. `tests/test_traceability.py`
::TestBootstrapScaffold is the worked precedent for a bootstrap proven by deed; this follows its shape
and goes further by resolving the pack tree the way an installed session must.

WHAT CASE F DOES NOT COVER, said plainly: Phases 1, 4 and 5 of the founding wait on a person or on
installers that write outside the fixture. They are covered by the string criteria in cases B and C
and by the eval. Every temporary tree is removed by its own context manager (SPEC INV-100).
"""

import glob
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARD = "skills/build-pipeline/references/project-setup.md"
START = "adopt/START.md"
ADOPT = "adopt/ADOPT.md"
CATCHUP = "MIGRATION.md"
REQUEST_KINDS = "skills/director/references/request-kind-table.md"

# The two ADOPT.md headings the founding walk points at rather than restating (design F8).
ADOPT_VCS_HEADING = "Phase 0 — Version-control gate first"
ADOPT_ORIENT_HEADING = "Phase 1 — Orient: read everything first"

# The six words criterion 2 measures the pack's name against, and the reach it allows.
SETUP_WORDS = ("adopt", "install", "onboard", "found", "attach", "update")
NEAR = 40

# The eight sentences case G scores as loading, and the two that must miss (criteria 24, 25).
LOADING_PHRASES = (
    "attach live-spec to this project",
    "adopt live-spec here",
    "set live-spec up on this repo",
    "add live-spec to this codebase",
    "found a new project on live-spec",
    "start a new project with live-spec",
    "I just installed live-spec, what now",
    "update live-spec here",
)
MISSING_PHRASES = ("install the requests library", "start a new project")

# The settings about the person, which the host profile never carries (criterion 20).
PERSONAL_KEYS = ("language.chat", "language.docs", "address", "proactivity.mode")


def read(rel, root=ROOT):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return " ".join(text.split())


def descriptions():
    """Every installed skill's description field, keyed by the skill's directory name."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        block = text.split("---", 2)[1] if text.startswith("---") else ""
        field, taking = [], False
        for line in block.splitlines():
            if line.startswith("description:"):
                taking = True
                field.append(line[len("description:"):].strip())
                continue
            if taking:
                if re.match(r"^\S", line):          # the next frontmatter key ends the field
                    break
                field.append(line.strip())
        out[name] = flat(" ".join(field))
    return out


def within(text, word, pack="live-spec", reach=NEAR):
    """True when some occurrence of `word` stands within `reach` characters of the pack's name.

    The distance counts the characters between the two spans, so a word touching the name scores 0.
    """
    words = [m.span() for m in re.finditer(r"\b%s\b" % re.escape(word), text, re.IGNORECASE)]
    names = [m.span() for m in re.finditer(re.escape(pack), text, re.IGNORECASE)]
    for wstart, wend in words:
        for nstart, nend in names:
            gap = nstart - wend if nstart >= wend else wstart - nend
            if 0 <= gap <= reach:
                return True
    return False


def ordered_lists(text):
    """Every run of ordered-list items in a markdown text, as a list of item-number lists."""
    runs, current = [], []
    for line in text.splitlines():
        m = re.match(r"^(\d+)\.\s", line)
        if m:
            current.append(int(m.group(1)))
            continue
        if line.strip() and not line.startswith(("   ", "\t")):
            if current:
                runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def table_rows(text, cells):
    """Every body row of a markdown table with the given cell count, backticks stripped."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|") or not s.endswith("|"):
            continue
        parts = [c.strip().strip("`").strip() for c in s.strip("|").split("|")]
        if len(parts) != cells:
            continue
        if all(set(p) <= set("-: ") for p in parts):        # the header rule
            continue
        rows.append(parts)
    return rows


def sections(text):
    """The document split by its headings: {heading text: the body under it}."""
    out, heading, body = {}, None, []
    for line in text.splitlines():
        if line.startswith("#"):
            if heading is not None:
                out[heading] = "\n".join(body)
            heading = line.lstrip("#").strip()
            body = []
            continue
        body.append(line)
    if heading is not None:
        out[heading] = "\n".join(body)
    return out


# --- the founding driver: the walk's mechanical spine, read out of the walk ----------------------


class SetupError(RuntimeError):
    """A setup run that stops honestly, naming what it lacks."""


def install_paths(registry_path, key="live-spec@live-spec"):
    with open(registry_path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [entry.get("installPath") for entry in data.get("plugins", {}).get(key, [])
            if entry.get("installPath")]


def resolve_pack_tree(project_root, home, plugin_root=None, neighbour=None):
    """The routing card's six ordered reads, first hit winning. Returns (read number, path).

    Read 6 is the honest stop: it raises, naming the one action that supplies the tree.
    """
    if os.path.isfile(os.path.join(project_root, "adopt", "ADOPT.md")):
        return 1, project_root
    if plugin_root and os.path.isfile(os.path.join(plugin_root, "adopt", "ADOPT.md")):
        return 2, plugin_root
    registry = os.path.join(home, ".claude", "plugins", "installed_plugins.json")
    if os.path.isfile(registry):
        for path in install_paths(registry):
            if os.path.isfile(os.path.join(path, "adopt", "ADOPT.md")):
                return 3, path
    cache = os.path.join(home, ".claude", "plugins", "cache", "*", "*", "*", "adopt", "ADOPT.md")
    for hit in sorted(glob.glob(cache)):
        return 4, os.path.dirname(os.path.dirname(hit))
    beside = neighbour or os.path.join(os.path.dirname(os.path.abspath(project_root)), "live-spec")
    if os.path.isfile(os.path.join(beside, "adopt", "ADOPT.md")):
        return 5, beside
    raise SetupError(
        "no read answered: the pack tree did not resolve. One action supplies it — install the "
        "plugin with the two lines in the README, or clone the repository to ~/.live-spec-pack.")


def copy_table(pack_tree):
    """Phase 2's copy table, read out of `adopt/START.md`: (template, lands as, when)."""
    rows = []
    for parts in table_rows(read(START, root=pack_tree), 3):
        template, lands_as, when = parts
        if not template.endswith((".md", ".py")):
            continue
        rows.append((template, lands_as, when))
    return rows


PLACEHOLDER_NAME = re.compile(r"\[[Pp]roject [Nn]ame\]|<agent name>|<project>"
                              r"|<artifact or project name>")


def fill_first_line(body, name, day):
    """The first line takes this project's name and the day the founding runs. Every other

    placeholder stays as it stands — a founding fills what it knows and guesses nothing.
    """
    lines = body.split("\n")
    head = PLACEHOLDER_NAME.sub(name, lines[0]).replace("[date]", day)
    lines[0] = head
    return "\n".join(lines)


def host_profile_keys(pack_tree):
    """One key per founding question whose key names no path, plus the two the walk adds."""
    data = json.loads(read(os.path.join("scripts", "founding-questions.json"), root=pack_tree))
    keys = []
    for question in data["questions"]:
        key = question["key"]
        if "/" in key:                 # a key naming a path is satisfied by that file
            continue
        for part in key.split(" + "):
            keys.append(part.split(" (")[0].strip())
    keys += ["budget.pressure", "founding.set-version"]
    return keys, data["set_version"]


def found(project_root, pack_tree, name=None, day="2026-08-06", fill=True):
    """Phases 0, 2 and 3 of `adopt/START.md`, driven mechanically over a real tree.

    Every phase reads its precondition from the tree; a destination that already stands is reported
    done and skipped. `fill=False` drives the red proof of criterion 23 alone: it copies the
    documents with their template placeholders intact, which the scaffold suite must refuse.
    """
    name = name or os.path.basename(os.path.abspath(project_root))
    report = {"copied": [], "skipped": [], "commits": 0}

    # Phase 0 — version control first.
    if not os.path.isdir(os.path.join(project_root, ".git")):
        subprocess.run(["git", "init", "-q"], cwd=project_root, check=True)
        with open(os.path.join(project_root, ".gitignore"), "w", encoding="utf-8") as fh:
            fh.write(".live-spec/checkpoints/\n__pycache__/\n")
        subprocess.run(["git", "add", ".gitignore"], cwd=project_root, check=True)
        subprocess.run(["git", "-c", "user.email=founding@example.invalid",
                        "-c", "user.name=founding", "commit", "-q", "-m", "baseline"],
                       cwd=project_root, check=True)
    else:
        report["skipped"].append("Phase 0 — the tree is already a git repository")
    counted = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=project_root,
                             capture_output=True, text=True)
    report["commits"] = int(counted.stdout.strip() or 0)

    # Phase 2 — the templates land. Every source is checked before anything is written.
    rows = copy_table(pack_tree)
    report["rows"] = rows
    missing = [t for t, _, _ in rows
               if not os.path.isfile(os.path.join(pack_tree, "templates", t))]
    if missing:
        raise SetupError("the copy table names a template this pack tree does not carry: %s"
                         % ", ".join(sorted(missing)))
    for template, lands_as, when in rows:
        if when.lower() != "always":
            report["skipped"].append("%s — waits on the founding's word" % lands_as)
            continue
        dest = os.path.join(project_root, lands_as)
        if os.path.exists(dest):
            report["skipped"].append("%s — already stands" % lands_as)
            continue
        parent = os.path.dirname(dest)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        body = read(os.path.join("templates", template), root=pack_tree)
        if fill:
            body = fill_first_line(body, name, day)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(body)
        report["copied"].append(lands_as)

    # Phase 2 — the host profile, written from the founding-question set, never from a template.
    profile = os.path.join(project_root, ".live-spec", "profile.md")
    if os.path.exists(profile):
        report["skipped"].append(".live-spec/profile.md — already stands")
    else:
        keys, set_version = host_profile_keys(pack_tree)
        lines = ["# %s — host profile" % name, "",
                 "This project's own lines alone. Every setting about the person lives in the",
                 "personal profile and is never copied here.", ""]
        for key in keys:
            if key == "founding.set-version":
                lines.append("%s: %s" % (key, set_version))
            else:
                lines.append("%s: ⟨DECIDE⟩ — asked at Phase 1, unanswered in this run" % key)
        if not os.path.isdir(os.path.dirname(profile)):
            os.makedirs(os.path.dirname(profile))
        with open(profile, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        report["copied"].append(".live-spec/profile.md")

    # Phase 3 — the first green.
    run = subprocess.run(["python3", "-m", "unittest", "discover", "tests"],
                         cwd=project_root, capture_output=True, text=True)
    report["scaffold_exit"] = run.returncode
    report["scaffold_output"] = run.stderr
    return report


def build_fixture(tmp, pack_source=ROOT, version="4.3.0", drop=None):
    """A throwaway home mirroring the plugin cache, plus the empty project being founded.

    `drop` names a template file to leave out of the copied pack tree — the red proof of
    criterion 22. Returns (home, project root, pack tree).
    """
    home = os.path.join(tmp, "home")
    pack = os.path.join(home, ".claude", "plugins", "cache", "live-spec", "live-spec", version)
    os.makedirs(pack)
    for rel in ("VERSION", "adopt", "templates", "scaffold"):
        src = os.path.join(pack_source, rel)
        dst = os.path.join(pack, rel)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)
    os.makedirs(os.path.join(pack, "scripts"))
    for script in ("founding-questions.json", "onboarding-card.py"):
        shutil.copy(os.path.join(pack_source, "scripts", script),
                    os.path.join(pack, "scripts", script))
    if drop:
        os.remove(os.path.join(pack, "templates", drop))
    with open(os.path.join(home, ".claude", "plugins", "installed_plugins.json"),
              "w", encoding="utf-8") as fh:
        json.dump({"version": 2, "plugins": {"live-spec@live-spec": [
            {"scope": "user", "installPath": pack, "version": version}]}}, fh)
    project = os.path.join(tmp, "project")
    os.makedirs(project)
    return home, project, pack


# --- case A: the spoken entry reaches one skill (M-512) ------------------------------------------


class TestSpokenEntryReachesOneSkill(unittest.TestCase):
    """M-512 — criteria 1 through 4. A description field is read by a matcher, so a string in the
    file is a floor; the load itself is scored in the eval (case G)."""

    def test_one_description_carries_both_setup_phrases(self):
        """Criterion 1 [A-0]."""
        carriers = [name for name, field in descriptions().items()
                    if "attach live-spec" in field and "set a project up on live-spec" in field]
        self.assertEqual(carriers, ["build-pipeline"],
                         "exactly one installed skill description carries the setup entry, and it "
                         "is build-pipeline's; found: %s" % carriers)

    def test_the_pack_is_named_beside_every_setup_word(self):
        """Criterion 2 [A-0]: the pack's name stands within 40 characters of each of six words."""
        field = descriptions()["build-pipeline"]
        for word in SETUP_WORDS:
            self.assertTrue(within(field, word),
                            "'%s' stands with no 'live-spec' within %d characters of it, so the "
                            "word alone could match a request about any other tool" % (word, NEAR))

    def test_no_second_description_carries_the_setup_phrases(self):
        """Criterion 3 [INV-13]: one home for the entry."""
        for name, field in descriptions().items():
            if name == "build-pipeline":
                continue
            for phrase in ("attach live-spec", "set a project up on live-spec"):
                self.assertNotIn(phrase, field,
                                 "%s's description contests the setup entry on '%s'" % (name, phrase))

    def test_spec_author_names_the_earlier_door(self):
        """Criterion 4 [INV-13]: the nearest neighbour points at the setup entry."""
        field = descriptions()["spec-author"]
        for needle in ("build-pipeline", "setup entry", "earlier"):
            self.assertIn(needle, field,
                          "spec-author's description does not name build-pipeline's setup entry as "
                          "the earlier door (missing: %s)" % needle)


# --- case B: the routing card (M-513) ------------------------------------------------------------


class TestRoutingCard(unittest.TestCase):
    """M-513 — criteria 5 through 7."""

    def test_card_exists_and_names_all_three_walks(self):
        """Criterion 5 [INV-90]."""
        self.assertTrue(os.path.isfile(os.path.join(ROOT, CARD)), "the routing card is missing: %s" % CARD)
        body = read(CARD)
        for walk in (ADOPT, START, CATCHUP):
            self.assertIn(walk, body, "the card does not name the walk %s by path" % walk)

    def test_card_carries_six_ordered_reads_ending_in_one_action(self):
        """Criterion 6 [E-21]."""
        body = read(CARD)
        runs = ordered_lists(body)
        self.assertTrue(runs, "the card carries no ordered list of reads")
        longest = max(runs, key=len)
        self.assertEqual(longest, [1, 2, 3, 4, 5, 6],
                         "the card's read list is not six reads numbered in order: %s" % longest)
        self.assertIn("installed_plugins.json", body, "the card names no plugin registry by path")
        self.assertIn("CLAUDE_PLUGIN_ROOT", body, "the card names no plugin-root variable")
        last = body.split("\n6. ", 1)[1]
        self.assertIn("stops", last, "the last read does not stop the run")
        self.assertIn("one action", last, "the last read hands the person no single action")

    def test_card_holds_no_phases(self):
        """Criterion 7 [INV-13]: the walks own the phases; the card owns the routing."""
        body = read(CARD)
        for line in body.splitlines():
            self.assertIsNone(re.match(r"^#+ .*Phase", line),
                              "the card carries a phase heading, which belongs to a walk: %r" % line)
        for run in ordered_lists(body):
            self.assertLessEqual(len(run), 6,
                                 "an ordered list longer than the six reads: %s" % run)
        # The body names the card by the path a session reads it at: beside the SKILL.md, inside
        # the skill folder. The pack's own tree may be absent on the install.sh route, so an
        # absolute path into that tree would name a file the reader cannot open.
        self.assertIn("references/project-setup.md", read("skills/build-pipeline/SKILL.md"),
                      "the skill body does not name the routing card by path")


# --- case C: the founding walk (M-514) -----------------------------------------------------------


class TestFoundingWalk(unittest.TestCase):
    """M-514 — criteria 8 through 14. Criterion 10, the one-home rule for the canonical document
    set, is held by the existing sweep in tests/test_catchup_walk.py, which START.md now joins."""

    def test_walk_exists_and_every_template_it_names_ships(self):
        """Criterion 8 [B-1]."""
        self.assertTrue(os.path.isfile(os.path.join(ROOT, START)), "the founding walk is missing: %s" % START)
        rows = copy_table(ROOT)
        self.assertGreaterEqual(len(rows), 8, "the copy table carries %d rows" % len(rows))
        for template, _lands_as, _when in rows:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "templates", template)),
                            "the copy table names a template that does not ship: %s" % template)
        unconditional = {lands: t for t, lands, when in rows if when.lower() == "always"}
        self.assertEqual(
            set(unconditional),
            {"PRODUCT_SPEC.md", "ARCHITECTURE.md", "TEST_MATRIX.md", "PLAN.md", "JOURNAL.md",
             "NEXT_STEPS.md", "tests/test_scaffold.py", ".live-spec/agent.md"},
            "the eight unconditional destinations moved")

    def test_walk_points_at_adopt_rather_than_restating_it(self):
        """Criterion 9 [INV-13]."""
        body = read(START)
        for heading in (ADOPT_VCS_HEADING, ADOPT_ORIENT_HEADING):
            self.assertNotIn(heading, body,
                             "the founding walk restates an ADOPT.md heading instead of pointing "
                             "at it: %s" % heading)
        pointing = []
        for heading, chunk in sections(body).items():
            if ADOPT in chunk:
                pointing.append(heading)
        for phase in ("Phase 0", "Phase 1", "Phase 5"):
            self.assertTrue(any(h.startswith(phase) for h in pointing),
                            "%s carries no pointer to %s" % (phase, ADOPT))

    def test_walk_is_safe_on_a_half_done_tree(self):
        """Criterion 11 [INV-89]: the two clauses its siblings use, and no bare copy order."""
        body = read(START)
        flat_body = flat(body)
        self.assertIn("reads its precondition from the tree", flat_body)
        self.assertIn("already holds is reported done and skipped", flat_body)
        for line in body.splitlines():
            self.assertIsNone(re.match(r"^\s*(?:[-*]|\d+\.)?\s*[Cc]opy\b", line),
                              "an unconditional copy instruction stands outside the table's own "
                              "condition column: %r" % line)

    def test_walk_names_the_judge_and_no_check_list_of_its_own(self):
        """Criterion 12 [B-1]: the shipped scaffold states what it checks."""
        body = flat(read(START))
        self.assertIn("tests/test_scaffold.py", body)
        for stale in ("coverage-validation checklist", "coverage checklist", "four checks",
                      "every header is filled", "one live-state block"):
            self.assertNotIn(stale, body,
                             "the walk enumerates a check the scaffold owns, which goes stale the "
                             "next time that file moves: %s" % stale)

    def test_registry_is_created_after_the_config_and_takes_its_name(self):
        """Criterion 13 [INV-97]."""
        body = read(START)
        installer_phase = [chunk for heading, chunk in sections(body).items()
                           if "install-scaffold.sh" in chunk]
        self.assertTrue(installer_phase, "no phase runs the scaffold installer")
        self.assertIn("registry_path", installer_phase[0],
                      "the registry is not created from the config's registry path in the phase "
                      "that runs the installers")
        self.assertIn("guardrails.config.json", installer_phase[0])
        for own_name in ("SURFACES.md", "SURFACE_REGISTRY.md"):
            self.assertNotIn(own_name, body,
                             "the walk states a registry filename of its own: %s" % own_name)

    def test_host_profile_carries_the_projects_own_lines(self):
        """Criterion 14 [B-3]."""
        body = flat(read(START))
        self.assertIn(".live-spec/profile.md", body)
        self.assertIn("scripts/founding-questions.json", body)
        self.assertNotIn("profile.template.md", body,
                         "the walk names a personal-profile template as the host profile's source")


# --- case D: the request set places all three sentences (M-515) ----------------------------------


class TestRequestSetPlacesEverySetupSentence(unittest.TestCase):
    """M-515 — criteria 15 and 16."""

    def test_three_setup_rows_each_naming_entry_and_back_check(self):
        """Criterion 15 [INV-151]."""
        rows = table_rows(read(REQUEST_KINDS), 3)
        wanted = {
            "setting an existing project up on the pack": ADOPT,
            "founding a new project on the pack": START,
            "bringing an already-adopted project onto the current pack": CATCHUP,
        }
        for kind, entry in wanted.items():
            match = [r for r in rows if r[0] == kind]
            self.assertEqual(len(match), 1, "the closed set has no row for: %s" % kind)
            self.assertIn(entry, match[0][1],
                          "the row for '%s' does not name its entry document %s" % (kind, entry))
            self.assertGreater(len(match[0][2].split()), 3,
                               "the row for '%s' states no mandatory back-check" % kind)

    def test_adoption_guide_routes_a_fresh_project_and_drops_the_hand_copy(self):
        """Criterion 16 [INV-90]."""
        body = read("docs/adoption.md")
        self.assertIn(START, body, "docs/adoption.md names no fresh-project entry")
        self.assertNotIn("copies them by hand", body,
                         "docs/adoption.md still says a person copies the templates by hand, which "
                         "the founding walk makes false")

    def test_the_templates_list_names_every_template_that_ships(self):
        """The stale-list repair riding criterion 16: the guide named ten of fourteen files.

        A template is a file the host copies. What the interpreter leaves behind next to one —
        `__pycache__` for `headless_harness.py`, a dotfile the tree never ships — is not a
        template and is not named by the guide. The cache folder is born inside the scratch copy
        after the copy is taken, so a run that imports the harness would otherwise red on it."""
        body = read("docs/adoption.md")
        for entry in sorted(os.listdir(os.path.join(ROOT, "templates"))):
            if entry.startswith(".") or entry == "__pycache__":
                continue
            self.assertIn(entry, body,
                          "docs/adoption.md's templates section does not name %s" % entry)


# --- case E: both install routes reach the tree (M-516) ------------------------------------------


class TestBothInstallRoutesReachTheTree(unittest.TestCase):
    """M-516 — criteria 17 and 18."""

    def test_every_skills_path_the_card_names_sits_under_a_skill_folder(self):
        """Criterion 17 [E-21]: install.sh copies skill folders whole and touches nothing else."""
        body = read(CARD) + "\n" + read("skills/build-pipeline/SKILL.md")
        for match in set(re.findall(r"skills/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", body)):
            parts = match.split("/")
            self.assertGreaterEqual(len(parts), 3,
                                    "a path under skills/ that is not inside a skill folder: %s" % match)
            if match.endswith((".md", ".py", ".json", ".sh")):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, match)),
                                "the card names a file that does not ship: %s" % match)

    def test_a_file_or_symlink_at_the_destination_is_backed_up_before_it_is_removed(self):
        """install.sh's `rm -rf "$dest"` takes anything at that path; the backup above it only
        covered a directory, so a skill installed as a file or a symlink — the shape a person
        who symlinked one skill at the pack has — was deleted with no copy kept. Red-proved
        2026-09-06 against `[ -d "$dest" ]`: the attic came back empty."""
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "home")
            skills = os.path.join(home, ".claude", "skills")
            os.makedirs(skills)
            victim = os.path.join(skills, "director")
            with open(victim, "w", encoding="utf-8") as fh:
                fh.write("a hand-placed file where a skill folder belongs\n")

            r = subprocess.run(["bash", os.path.join(ROOT, "install.sh")],
                               capture_output=True, text=True,
                               env={**os.environ, "HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            attic = skills + "-attic"
            kept = [n for n in os.listdir(attic)] if os.path.isdir(attic) else []
            self.assertTrue([n for n in kept if n.startswith("director.bak_")],
                            "the file at the destination was removed with no backup: %r" % kept)
            backup = os.path.join(attic, [n for n in kept if n.startswith("director.bak_")][0])
            with open(backup, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "a hand-placed file where a skill folder belongs\n")
            self.assertTrue(os.path.isdir(victim), "the skill did not install over the file")

    def test_a_version_disagreement_is_said_aloud(self):
        """Criterion 18 [M-7]."""
        body = flat(read(CARD))
        self.assertIn("VERSION", body)
        self.assertIn("both numbers", body,
                      "the card does not require both version numbers said aloud before the walk "
                      "continues")


# --- case F: a founding runs (M-517) -------------------------------------------------------------


class TestAFoundingRuns(unittest.TestCase):
    """M-517 — criteria 19 through 23, proven by deed on a throwaway tree."""

    def test_a_founding_resolves_the_pack_and_reaches_the_first_green(self):
        """Criterion 19 [B-1]."""
        with tempfile.TemporaryDirectory() as tmp:
            home, project, pack = build_fixture(tmp)
            number, resolved = resolve_pack_tree(project, home)
            self.assertEqual(number, 3, "the plugin registry did not answer; read %d did" % number)
            self.assertEqual(os.path.realpath(resolved), os.path.realpath(pack))
            self.assertEqual(read("VERSION", root=resolved).strip(), read("VERSION").strip())

            report = found(project, resolved, name="demo")
            self.assertEqual(report["commits"], 1,
                             "the founded tree holds %d commits" % report["commits"])
            for doc in ("PRODUCT_SPEC.md", "ARCHITECTURE.md", "TEST_MATRIX.md", "PLAN.md",
                        "JOURNAL.md", "NEXT_STEPS.md"):
                path = os.path.join(project, doc)
                self.assertTrue(os.path.isfile(path), "%s did not land" % doc)
                head = read(doc, root=project).splitlines()[0]
                self.assertNotIn("[Project Name]", head, "%s kept its name placeholder" % doc)
            for record in (".live-spec/agent.md", ".live-spec/profile.md"):
                self.assertTrue(os.path.isfile(os.path.join(project, record)),
                                "%s did not land" % record)
            self.assertEqual(report["scaffold_exit"], 0,
                             "the scaffold suite did not reach green:\n%s" % report["scaffold_output"])

    def test_the_host_profile_carries_the_hosts_keys_and_none_of_the_persons(self):
        """Criterion 20 [B-3]."""
        with tempfile.TemporaryDirectory() as tmp:
            home, project, _pack = build_fixture(tmp)
            _number, resolved = resolve_pack_tree(project, home)
            found(project, resolved, name="demo")
            profile = read(".live-spec/profile.md", root=project)
            keys, set_version = host_profile_keys(resolved)
            for key in keys:
                self.assertIn(key, profile, "the host profile carries no line for %s" % key)
            self.assertIn("founding.set-version: %s" % set_version, profile)
            for key in PERSONAL_KEYS:
                self.assertNotIn(key, profile,
                                 "a setting about the person reached the host profile: %s" % key)

    def test_a_second_founding_keeps_what_the_person_wrote(self):
        """Criterion 21 [INV-89] — the red the design named: a second run must not overwrite."""
        sentence = "This product exists to settle one argument about coffee."
        with tempfile.TemporaryDirectory() as tmp:
            home, project, _pack = build_fixture(tmp)
            _number, resolved = resolve_pack_tree(project, home)
            found(project, resolved, name="demo")
            spec = os.path.join(project, "PRODUCT_SPEC.md")
            with open(spec, "a", encoding="utf-8") as fh:
                fh.write("\n" + sentence + "\n")
            report = found(project, resolved, name="demo")
            self.assertIn(sentence, read("PRODUCT_SPEC.md", root=project),
                          "the second founding overwrote the person's own sentence")
            self.assertTrue(any("PRODUCT_SPEC.md — already stands" in s for s in report["skipped"]),
                            "the second run did not report the standing document done and skipped")
            self.assertEqual(report["commits"], 1, "the second run committed again")

    def test_a_missing_template_fails_by_name(self):
        """Criterion 22 [B-1]."""
        with tempfile.TemporaryDirectory() as tmp:
            home, project, _pack = build_fixture(tmp, drop="PLAN.template.md")
            _number, resolved = resolve_pack_tree(project, home)
            with self.assertRaises(SetupError) as caught:
                found(project, resolved, name="demo")
            self.assertIn("PLAN.template.md", str(caught.exception),
                          "the run failed without naming the template it lacked")
            self.assertFalse(os.path.exists(os.path.join(project, "PRODUCT_SPEC.md")),
                             "the run copied documents before it checked its sources")

    def test_surviving_placeholders_are_red(self):
        """Criterion 23 [B-1]."""
        with tempfile.TemporaryDirectory() as tmp:
            home, project, _pack = build_fixture(tmp)
            _number, resolved = resolve_pack_tree(project, home)
            report = found(project, resolved, name="demo", fill=False)
            self.assertNotEqual(report["scaffold_exit"], 0,
                                "the scaffold suite stayed green on documents that kept their "
                                "template placeholders")

    def test_a_tree_that_resolves_nothing_stops_with_one_action(self):
        """The card's read 6, proven by deed [INV-307]."""
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "home")
            project = os.path.join(tmp, "project")
            os.makedirs(os.path.join(home, ".claude", "plugins"))
            os.makedirs(project)
            with self.assertRaises(SetupError) as caught:
                resolve_pack_tree(project, home)
            self.assertIn("One action", str(caught.exception))


# --- case G's floor: the scored list stands written (M-518) --------------------------------------


class TestScoredPhrasesAreWritten(unittest.TestCase):
    """M-518 — criterion 26. The loading itself is scored by a run recorded in the eval; the floor
    here is that the list a later session audits against the shipped field stands written."""

    def test_the_eval_carries_every_scored_phrase(self):
        body = flat(read("evals/build-pipeline.md"))
        for phrase in LOADING_PHRASES:
            self.assertIn(phrase, body, "the eval does not score the phrase: %s" % phrase)
        for phrase in MISSING_PHRASES:
            self.assertIn(phrase, body, "the eval does not carry the negative: %s" % phrase)


if __name__ == "__main__":
    unittest.main()
