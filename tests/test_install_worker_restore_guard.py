"""The worker-restore prevention hook installs safely and repeatably."""

import json
import os
import pathlib
import subprocess
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[1]
INSTALLER = REPO / "scripts" / "install-worker-restore-guard.sh"


class TestWorkerRestoreGuardInstaller(unittest.TestCase):
    def run_installer(self, home, *args):
        env = dict(os.environ, HOME=str(home))
        return subprocess.run(
            ["bash", str(INSTALLER), *args], cwd=REPO, env=env,
            text=True, capture_output=True,
        )

    def test_dry_run_describes_work_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            result = self.run_installer(home, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("dry-run", result.stdout.lower())
            self.assertFalse((home / ".claude").exists())

    def test_install_copies_hook_wires_settings_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            first = self.run_installer(home)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            hook = home / ".claude" / "hooks" / "worker-restore-guard.py"
            settings = home / ".claude" / "settings.json"
            self.assertEqual(hook.read_bytes(), (REPO / "hooks" / hook.name).read_bytes())
            data = json.loads(settings.read_text())
            pre = data["hooks"]["PreToolUse"]
            commands = [h["command"] for group in pre for h in group["hooks"]]
            self.assertIn("python3 ~/.claude/hooks/worker-restore-guard.py", commands)
            before = (hook.read_bytes(), settings.read_bytes())

            second = self.run_installer(home)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(before, (hook.read_bytes(), settings.read_bytes()))

    def test_malformed_settings_leave_hook_and_settings_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            settings = home / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text("{ this is not json\n")
            result = self.run_installer(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot parse", result.stderr)
            self.assertEqual(settings.read_text(), "{ this is not json\n")
            self.assertFalse((home / ".claude" / "hooks" / "worker-restore-guard.py").exists())

    def test_install_preserves_existing_settings_and_hook_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            settings = home / ".claude" / "settings.json"
            settings.parent.mkdir()
            original = {
                "keep": "this value",
                "hooks": {"PreToolUse": [{
                    "matcher": "Write", "hooks": [{"type": "command", "command": "existing"}],
                }]},
            }
            settings.write_text(json.dumps(original) + "\n")
            result = self.run_installer(home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(settings.read_text())
            self.assertEqual(data["keep"], "this value")
            self.assertEqual(data["hooks"]["PreToolUse"][0], original["hooks"]["PreToolUse"][0])
            self.assertEqual(len(data["hooks"]["PreToolUse"]), 2)


if __name__ == "__main__":
    unittest.main()
