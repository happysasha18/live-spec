"""tests/test_run_modes_install.py — the four-mode contract's own adopt/update path (row q-826,
the owner's word, 2026-09-07 22:00).

Extends adopt/install-scaffold.sh rather than a second installer: vendors the run-mode reader
(guardrails/run_modes.py), the push-time acceptance re-run (guardrails/check-acceptance-rerun.py,
owned by another worker — vendored by path only, never opened by this file), the repo-local spawn
guard (guardrails/worker-admission-guard.py) plus its wiring into the HOST's own repo-local
.claude/settings.json, and the minimal runtime admission the four modes rest on
(scripts/task-admission.py, scripts/checkpoint.py). Mirrors the shape of
tests/test_scaffold_install.py.

The run_modes key: guardrails.config.json is SEEDED (never overwritten) the way the whole file
already is, so the four names ride that same seed — reaching a freshly adopted host, and never
touching a host's pre-existing file, filled or not (test_scaffold_install.py's
test_never_clobbers_a_filled_config already proves that byte-for-byte immutability and this file
must not weaken it).
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL_SCAFFOLD = os.path.join(ROOT, "adopt", "install-scaffold.sh")

#: pack-relative source -> where the host carries it (the "<pack-rel>|<host-rel>" pairs
#: adopt/install-scaffold.sh's own VENDOR_MODES array uses).
RUN_MODES_VENDORED = {
    "guardrails/run_modes.py": "guardrails/run_modes.py",
    "guardrails/check-acceptance-rerun.py": "guardrails/check-acceptance-rerun.py",
    "guardrails/worker-admission-guard.py": "guardrails/worker-admission-guard.py",
    "scripts/task-admission.py": "scripts/task-admission.py",
    "scripts/checkpoint.py": "scripts/checkpoint.py",
}

RUN_MODE_NAMES = ("row", "integration", "release", "manual")

WORKTREE_LINE = ("Two lanes whose write-sets overlap each get their own worktree "
                 "(SPEC INV-105).\n")

HOOK_NEEDLE = "worker-admission-guard.py"


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True)


def _init_host(tmp, worktree_line=True):
    run(["git", "init", "-q"], cwd=tmp)
    run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
    run(["git", "config", "user.name", "a"], cwd=tmp)
    if worktree_line:
        with open(os.path.join(tmp, "CLAUDE.md"), "w", encoding="utf-8") as fh:
            fh.write("# a host project\n\n" + WORKTREE_LINE)


class TestRunModesInstall(unittest.TestCase):
    def test_fresh_install_lands_all_five_deliverables(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for host_rel in RUN_MODES_VENDORED.values():
                self.assertTrue(os.path.isfile(os.path.join(tmp, host_rel)),
                                 "missing vendored: %s" % host_rel)

    def test_fresh_install_seeds_run_modes_with_the_four_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            cfg = json.load(open(os.path.join(tmp, "guardrails.config.json"), encoding="utf-8"))
            self.assertIn("run_modes", cfg)
            for name in RUN_MODE_NAMES:
                self.assertIn(name, cfg["run_modes"])

    def test_a_hosts_own_run_modes_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            own_config = {
                "spec_path": "MY_SPEC.md",
                "run_modes": {"row": {"decides_verdict": True, "note": "the host's own tuning"}},
            }
            cfg_path = os.path.join(tmp, "guardrails.config.json")
            with open(cfg_path, "w", encoding="utf-8") as fh:
                json.dump(own_config, fh)
            before = open(cfg_path, encoding="utf-8").read()
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(open(cfg_path, encoding="utf-8").read(), before,
                              "a host's own run_modes tuning was touched")

    def test_a_second_update_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            first = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            tree_before = _tree_snapshot(tmp)
            manifest_before = open(
                os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8").read()

            second = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

            self.assertEqual(_tree_snapshot(tmp), tree_before, "a second run changed the tree")
            manifest_after = open(
                os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8").read()
            self.assertEqual(manifest_after, manifest_before, "a second run changed the manifest")

            manifest = json.loads(manifest_after)
            keys = list(manifest["vendored"].keys())
            self.assertEqual(len(keys), len(set(keys)), "duplicate manifest keys after a rerun")

    def test_settings_json_gains_the_spawn_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            settings_path = os.path.join(tmp, ".claude", "settings.json")
            self.assertTrue(os.path.isfile(settings_path))
            settings = json.load(open(settings_path, encoding="utf-8"))
            pre_tool_use = settings["hooks"]["PreToolUse"]
            self.assertTrue(any(
                HOOK_NEEDLE in (h.get("command") or "")
                for group in pre_tool_use
                for h in group.get("hooks", [])
            ), "no PreToolUse hook names worker-admission-guard.py")
            for group in pre_tool_use:
                if HOOK_NEEDLE in " ".join(h.get("command") or "" for h in group.get("hooks", [])):
                    self.assertEqual(group.get("matcher"), "Task|Agent")

    def test_a_hosts_own_hook_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            claude_dir = os.path.join(tmp, ".claude")
            os.makedirs(claude_dir)
            own_settings = {
                "hooks": {
                    "PreToolUse": [
                        {
                            "matcher": "Task|Agent",
                            "hooks": [{
                                "type": "command",
                                "command": "python3 \"$CLAUDE_PROJECT_DIR/my-own-guard.py\" "
                                           "worker-admission-guard.py",
                            }],
                        }
                    ]
                },
                "extra_key_of_the_hosts_own": True,
            }
            settings_path = os.path.join(claude_dir, "settings.json")
            with open(settings_path, "w", encoding="utf-8") as fh:
                json.dump(own_settings, fh)
            before = open(settings_path, encoding="utf-8").read()
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(open(settings_path, encoding="utf-8").read(), before,
                              "a host's own settings.json was rewritten")

    def test_nothing_under_the_users_home_is_written(self):
        text = open(INSTALL_SCAFFOLD, encoding="utf-8").read()
        self.assertNotIn("$HOME", text)
        self.assertNotIn("~/.claude", text)

    def test_every_vendored_file_is_pinned_in_the_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.load(
                open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8"))
            for src_rel in RUN_MODES_VENDORED:
                self.assertIn(src_rel, manifest["vendored"],
                              "not pinned in the manifest: %s" % src_rel)
                pack_src = os.path.join(ROOT, src_rel)
                self.assertTrue(os.path.isfile(pack_src),
                                "pinned key must resolve against the pack: %s" % src_rel)


def _tree_snapshot(root):
    """path -> content for every regular file under root, .git excluded — a plain equality check
    that a rerun changed nothing anywhere in the host, not just in the manifest."""
    snapshot = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            with open(path, "rb") as f:
                snapshot[rel] = f.read()
    return snapshot


if __name__ == "__main__":
    unittest.main()
