"""tests/test_status_view_install.py — the turnkey status-view adoption kit (PLAN.md, plan-14).

`adopt/install-status-view.sh` vendors the three plan readers (probe · board · one-row reader) and
their shared parser into a host's `scripts/`, seeds the host's own acceptance-command file where it
has none (never clobbering a filled one), and pins each vendored copy under its pack-relative source
path in `scripts/ratchet-manifest.json`. Mirrors the shape of `tests/test_scaffold_install.py`.

What the first class below proves is the half an installer test usually misses: that the readers a
host receives read the HOST's plan and the HOST's commands, and carry none of this pack's own. Before
plan-14, `parse_tasks()` looked this pack's own `CHECKS` map up inside itself, so the parser and this
one project's literal shell commands were one thing — a host could not have taken the reader without
taking commands naming files it does not have.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL = os.path.join(ROOT, "adopt", "install-status-view.sh")

#: pack-relative source -> where the host carries it. The manifest pins the left-hand side.
VENDORED = {
    "scaffold/status-view/state-probe.sh": "scripts/state-probe.sh",
    "scripts/render-board.sh": "scripts/render-board.sh",
    "scripts/plan-step.sh": "scripts/plan-step.sh",
    "scripts/plan_checks_core.py": "scripts/plan_checks_core.py",
    "scripts/check-success-measure-feed.py": "scripts/check-success-measure-feed.py",
}

#: A host's plan, in the headings shape, with ids that share no name with any row of this pack's own
#: PLAN.md. Three rows: one with no command (DECLARED), one whose command passes, one whose fails.
HOST_PLAN = """# demo-project — Plan

## Tasks

### ⬜ Ship the widget catalogue — id: demo-1
**Group:** Catalogue · **Priority:** normal
**Source:** the fixture.

The row with no command of its own.

### ✅ Name every greeting — id: demo-2
**Group:** Greetings · **Priority:** normal
**Source:** the fixture.

### ✅ Draw the delivery map — id: demo-3
**Group:** Maps · **Priority:** normal
**Source:** the fixture.

## Blockers

- **A blocker of the host's own.** Nothing of the pack's.
"""

#: The same host's plan in the OTHER shape a plan reaches the reader in: the markdown table
#: `templates/PLAN.template.md` lands on a project at its founding.
HOST_PLAN_TABLE = """# demo-project — Plan

## The body

| # | Wish (plain words) | Class | Status | Decision / acceptance |
|---|---|---|---|---|
| demo-1 | Ship the widget catalogue. Asked by Ada, 2026-09-01. door: feature · kind: product | small | *queued* 2026-09-01 | the catalogue lists every widget |
| demo-2 | Name every greeting. Asked by Ada, 2026-09-01. door: feature · kind: product · priority: critical | small | *in-work* 2026-09-02 | each greeting has a name |
"""


def host_checks(demo2, demo3):
    """The host's own command map, written the way a host writes one."""
    return ('from plan_checks_core import evaluate, key_failure_note, normalize_mark  # noqa: F401\n'
            'from plan_checks_core import parse_tasks as _parse_tasks\n'
            'CHECKS = {"demo-2": %r, "demo-3": %r}\n'
            'def parse_tasks(text):\n'
            '    return _parse_tasks(text, CHECKS)\n' % (demo2, demo3))


def run(args, cwd=None):
    # No bytecode cache. This machine's python keeps one in a shared directory keyed by source path
    # (sys.pycache_prefix), and this file rewrites the host's command map twice in the same second at
    # the same size — which reads as unchanged, so the second run would answer with the first map. A
    # person editing that file never writes two versions a millisecond apart.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, env=env)


def _init_host(tmp, plan=HOST_PLAN):
    run(["git", "init", "-q"], cwd=tmp)
    run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
    run(["git", "config", "user.name", "a"], cwd=tmp)
    with open(os.path.join(tmp, "PLAN.md"), "w", encoding="utf-8") as fh:
        fh.write(plan)
    run(["git", "add", "-A"], cwd=tmp)
    run(["git", "commit", "-qm", "the host's own first commit"], cwd=tmp)


def _pack_ids():
    """Every task id this pack writes a command for — the ids that must not appear in a host's own
    status view. Read from the pack rather than listed here, so an id added tomorrow is covered."""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from plan_checks import CHECKS
    return set(CHECKS)


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


#: The pack files adopt/install-status-view.sh itself reaches for — real content copied from this
#: checkout, so a fake pack directory runs the real installer script exactly as this repo does.
_PACK_FILES = [
    "VERSION",
    "scaffold/status-view/state-probe.sh",
    "scaffold/status-view/plan_checks.py",
    "scripts/render-board.sh",
    "scripts/plan-step.sh",
    "scripts/plan_checks_core.py",
    "guardrails/check-status-view-drift.py",
    "scripts/check-success-measure-feed.py",
    "adopt/install-status-view.sh",
]


def _make_fake_pack(parent):
    """A pack-shaped directory under `parent`, so a host also placed under `parent` sits beside it
    the way `~/live-spec` sits beside `~/my-project` (R12's sibling layout)."""
    pack_root = os.path.join(parent, "pack")
    for rel in _PACK_FILES:
        dest = os.path.join(pack_root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            _write(dest, fh.read())
    return pack_root


class TestTheInstalledViewIsTheHostsOwn(unittest.TestCase):
    """The genericity proof: a host's probe and board read the host's plan and the host's commands."""

    def _installed_host(self, demo2="true", demo3="false", plan=HOST_PLAN):
        tmp = tempfile.mkdtemp(prefix="livespec-status-view-")
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", tmp]))
        _init_host(tmp, plan)
        r = run(["bash", INSTALL], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        _write(os.path.join(tmp, "scripts", "plan_checks.py"), host_checks(demo2, demo3))
        return tmp

    def test_the_probe_prints_the_hosts_own_rows(self):
        tmp = self._installed_host()
        r = run(["bash", os.path.join(tmp, "scripts", "state-probe.sh")], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("demo-1", r.stdout)
        self.assertIn("Ship the widget catalogue", r.stdout)
        self.assertIn("A blocker of the host's own", r.stdout)
        # the page it draws is the host's page, named for the host
        self.assertIn(os.path.basename(tmp), r.stdout)

    def test_the_probe_prints_none_of_this_packs_own_rows(self):
        tmp = self._installed_host()
        r = run(["bash", os.path.join(tmp, "scripts", "state-probe.sh")], cwd=tmp)
        leaked = sorted(i for i in _pack_ids() if i in r.stdout)
        self.assertEqual(leaked, [], "this pack's own task ids reached a host's probe: %s" % leaked)

    def test_the_hosts_own_commands_decide_each_row(self):
        """The point of the whole split. Same three rows, the host's two commands swapped: the row
        whose command passes leaves the open list, and the row whose command fails comes back as
        reopened. Nothing but the host's own map moved between the two readings."""
        tmp = self._installed_host(demo2="true", demo3="false")
        probe = os.path.join(tmp, "scripts", "state-probe.sh")
        first = run(["bash", probe], cwd=tmp).stdout
        # demo-2's command passes: the mark is honoured and the row is done, so it is off the list.
        self.assertNotIn("demo-2", first)
        # demo-3's done mark is contradicted by its own command: reopened, and it says why.
        self.assertIn("demo-3", first)
        self.assertIn("🔁", first)
        self.assertIn("marked done", first)
        self.assertIn("its acceptance command fails", first)
        # demo-1 has no command at all, so it is DECLARED rather than invented either way.
        self.assertIn("declared", first)

        _write(os.path.join(tmp, "scripts", "plan_checks.py"), host_checks("false", "true"))
        second = run(["bash", probe], cwd=tmp).stdout
        self.assertIn("demo-2", second, "a planted red did not reopen the row it names")
        self.assertNotIn("demo-3", second, "a planted pass did not close the row it names")
        self.assertNotEqual(first, second)

    def test_the_board_draws_the_hosts_own_rows_and_none_of_this_packs(self):
        tmp = self._installed_host()
        r = run(["bash", os.path.join(tmp, "scripts", "render-board.sh")], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        page = open(os.path.join(tmp, "board.html"), encoding="utf-8").read()
        for row in ("demo-1", "demo-2", "demo-3", "Ship the widget catalogue"):
            self.assertIn(row, page)
        self.assertIn("<title>%s — board</title>" % os.path.basename(tmp), page)
        leaked = sorted(i for i in _pack_ids() if i in page)
        self.assertEqual(leaked, [], "this pack's own task ids reached a host's board: %s" % leaked)

    def test_one_row_reader_prints_the_hosts_own_row(self):
        tmp = self._installed_host()
        r = run(["bash", os.path.join(tmp, "scripts", "plan-step.sh"), "demo-1"], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Ship the widget catalogue", r.stdout)
        self.assertNotIn("demo-2", r.stdout)

    def test_the_seeded_command_file_carries_no_command_of_this_packs(self):
        tmp = tempfile.mkdtemp(prefix="livespec-status-view-")
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", tmp]))
        _init_host(tmp)
        self.assertEqual(run(["bash", INSTALL], cwd=tmp).returncode, 0)
        seeded = open(os.path.join(tmp, "scripts", "plan_checks.py"), encoding="utf-8").read()
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        from plan_checks import CHECKS
        for task_id, command in CHECKS.items():
            self.assertNotIn(command, seeded,
                             "the host was seeded with this pack's own command for %s" % task_id)
        self.assertIn("CHECKS = {}", seeded)

    def test_the_table_shaped_plan_a_founding_lands_is_read_too(self):
        """A project founded on templates/PLAN.template.md carries the table shape, not the headings
        shape this pack's own plan uses. A reader that saw only one of the two would print an empty
        list on every freshly founded project."""
        tmp = self._installed_host(demo2="false", demo3="false", plan=HOST_PLAN_TABLE)
        r = run(["bash", os.path.join(tmp, "scripts", "state-probe.sh")], cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("demo-1", r.stdout)
        self.assertIn("Ship the widget catalogue", r.stdout)
        # the table's status WORDS become the marks the readers draw
        self.assertIn("⬜", r.stdout)   # *queued*
        self.assertIn("🔄", r.stdout)   # *in-work*
        # and the host's own command still decides: demo-2's fails, so it reads verified-and-open,
        # while demo-1, which has none, reads declared.
        self.assertIn("verified", r.stdout)
        self.assertIn("declared", r.stdout)
        leaked = sorted(i for i in _pack_ids() if i in r.stdout)
        self.assertEqual(leaked, [], "this pack's own task ids reached a host's probe: %s" % leaked)


class TestStatusViewInstall(unittest.TestCase):
    def test_vendors_the_readers_seeds_the_commands_and_pins_the_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            r = run(["bash", INSTALL], cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            for host_rel in list(VENDORED.values()) + ["scripts/plan_checks.py"]:
                self.assertTrue(os.path.isfile(os.path.join(tmp, host_rel)),
                                "missing vendored: %s" % host_rel)

            manifest = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))
            self.assertEqual(manifest["pack_version"],
                             open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip())
            # the pack root travels with the install, so a host's own push gate needs no
            # --pack-root flag to find the pack (SPEC Requirement 319 criterion 9a, F2). It is
            # recorded relative to the host root (R12) — resolved back against the host, it names
            # the pack checkout the install actually ran from.
            self.assertFalse(os.path.isabs(manifest["pack_root"]))
            self.assertEqual(os.path.normpath(os.path.join(tmp, manifest["pack_root"])), ROOT)
            for src_rel in VENDORED:
                self.assertIn(src_rel, manifest["vendored"])
                self.assertTrue(os.path.isfile(os.path.join(ROOT, src_rel)),
                                "a pinned key must resolve against the pack: %s" % src_rel)
            # the host's own commands are the host's content from minute one, so nothing pins them
            self.assertNotIn("scripts/plan_checks.py", manifest["vendored"])

    def test_a_sibling_hosts_recorded_pack_root_is_relative(self):
        """R12: PLAN.md's parent and my-project's parent are the same directory in the ordinary
        layout, so the recorded pack_root must be a short relative path a second clone or CI can
        resolve against its own checkout, not this machine's absolute one."""
        with tempfile.TemporaryDirectory() as parent:
            pack_root = _make_fake_pack(parent)
            host_root = os.path.join(parent, "my-project")
            os.makedirs(host_root)
            _init_host(host_root)
            r = run(["bash", os.path.join(pack_root, "adopt", "install-status-view.sh")],
                    cwd=host_root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            manifest = json.load(open(os.path.join(host_root, "scripts", "ratchet-manifest.json")))
            self.assertFalse(os.path.isabs(manifest["pack_root"]), manifest["pack_root"])
            self.assertEqual(
                os.path.normpath(os.path.join(host_root, manifest["pack_root"])), pack_root)

    def test_a_host_with_no_priority_statement_is_told_where_its_form_lives(self):
        """R6: the installer never touches a host's PLAN.md and never copies the template, so a
        host with no "Words used here" priority bullet (HOST_PLAN carries none) has nothing
        shipped naming the statement's form unless the installer says so itself."""
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            r = run(["bash", INSTALL], cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("templates/PLAN.template.md", r.stdout)
            self.assertIn("priority", r.stdout.lower())

    def test_never_clobbers_the_hosts_own_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            run(["bash", INSTALL], cwd=tmp)
            mine = host_checks("true", "false")
            _write(os.path.join(tmp, "scripts", "plan_checks.py"), mine)
            # a plain re-run, and the --force re-run the catch-up walk uses, both leave it as found
            for args in ([], ["--force"]):
                r = run(["bash", INSTALL] + args, cwd=tmp)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertEqual(open(os.path.join(tmp, "scripts", "plan_checks.py")).read(), mine)
                self.assertIn("keep your commands", r.stdout)

    def test_merge_preserves_another_kits_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
            prior = {"pack_version": "0.0.1",
                     "vendored": {"scaffold/guardrails/check_conflicts.py": "a" * 64},
                     "tier": "universal"}
            json.dump(prior, open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), "w"))
            self.assertEqual(run(["bash", INSTALL], cwd=tmp).returncode, 0)
            manifest = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))
            self.assertEqual(manifest["vendored"]["scaffold/guardrails/check_conflicts.py"], "a" * 64)
            self.assertEqual(manifest["tier"], "universal")
            self.assertIn("scripts/plan_checks_core.py", manifest["vendored"])
            self.assertNotEqual(manifest["pack_version"], "0.0.1")

    def test_idempotent_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            run(["bash", INSTALL], cwd=tmp)
            first = open(os.path.join(tmp, "scripts", "ratchet-manifest.json")).read()
            r = run(["bash", INSTALL], cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(first, open(os.path.join(tmp, "scripts", "ratchet-manifest.json")).read())
            for host_rel in VENDORED.values():
                self.assertIn("skip (exists, use --force to overwrite): %s" % host_rel, r.stdout)


if __name__ == "__main__":
    unittest.main()
