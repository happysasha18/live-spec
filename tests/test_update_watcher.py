"""INV-177 — the update check reads the host's vendored pins beside the pack version.

E-25's daily check proposes when the pack moved past this machine; the ratchet manifest
(INV-172) pins the pack version a host's vendored gate scripts came from. When the pack moved
past the pin, the check proposes the re-install and names the vendored files whose content
differs from the local pack's current copies. Proposal only; the per-file list is read against
the LOCAL pack checkout (E-25's no-per-skill-remote-diff line holds — the pack version speaks
for the whole).
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import SPEC, read

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "scripts", "check-pack-update.sh")


def run_check(tmp, manifest=None, remote_version="9.9.9"):
    remote = os.path.join(tmp, "REMOTE_VERSION")
    open(remote, "w").write(remote_version)
    stamp = os.path.join(tmp, "stamp")
    args = ["bash", CHECK, "--remote-file", remote, "--stamp-file", stamp, "--force",
            "--installed-file", os.path.join(REPO, "VERSION"), "--pack-root", REPO]
    if manifest:
        args += ["--manifest", manifest]
    return subprocess.run(args, cwd=tmp, capture_output=True, text=True)


class TestUpdateWatcherManifestArm(unittest.TestCase):
    def test_old_pin_proposes_reinstall_and_names_stale_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/gate_common.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("VENDORED GATES PINNED TO 0.0.1", r.stdout)
            self.assertIn("stale vs current pack: scripts/gate_common.py", r.stdout)
            self.assertIn("install-ratchet.sh --force", r.stdout)
            self.assertNotIn("install-scaffold.sh --force", r.stdout,
                              "a ratchet-only stale key must not propose the scaffold road")
            self.assertIn("PROPOSAL ONLY", r.stdout)

    def test_stale_scaffold_key_proposes_the_scaffold_reinstall_road(self):
        # Defect 3 (2026-07-16 fix): the road named must match the kit that is actually stale — a
        # scaffold-only host was pointed at install-ratchet.sh, which never touches scaffold/guardrails/.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scaffold/guardrails/gate_lib.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stale vs current pack: scaffold/guardrails/gate_lib.py", r.stdout)
            self.assertIn("install-scaffold.sh --force", r.stdout)
            self.assertNotIn("install-ratchet.sh --force", r.stdout,
                              "a scaffold-only stale key must not propose the ratchet road")

    def test_mixed_stale_keys_propose_both_reinstall_roads(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/gate_common.py": "0" * 64,
                                    "scaffold/guardrails/gate_lib.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("install-ratchet.sh --force", r.stdout)
            self.assertIn("install-scaffold.sh --force", r.stdout)

    def test_current_pin_stays_silent_on_vendored_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "9.9.9",
                       "vendored": {"scripts/gate_common.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn("VENDORED GATES PINNED", r.stdout)

    def test_no_manifest_keeps_the_plain_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_check(tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("PACK UPDATE AVAILABLE", r.stdout)
            self.assertNotIn("VENDORED GATES PINNED", r.stdout)


class TestManifestArmRunsWhenPackIsCurrent(unittest.TestCase):
    def test_old_pin_proposes_even_with_pack_up_to_date(self):
        # the born-from scenario (batch audit 2026-07-16, F1): pack current, host pin old
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/gate_common.py": "0" * 64}},
                      open(man, "w"))
            installed = open(os.path.join(REPO, "VERSION")).read().strip()
            r = run_check(tmp, manifest=man, remote_version=installed)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("up to date", r.stdout)
            self.assertIn("VENDORED GATES PINNED TO 0.0.1", r.stdout)
            self.assertIn("stale vs current pack: scripts/gate_common.py", r.stdout)


class TestManifestCoversScaffoldKit(unittest.TestCase):
    def test_installer_pins_scaffold_files_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            doc = os.path.join(tmp, "DOC.md")
            open(doc, "w").write("A plain sentence.\n")
            os.makedirs(os.path.join(tmp, "scaffold", "guardrails"))
            open(os.path.join(tmp, "scaffold", "guardrails", "gate_lib.py"), "w").write("# lib\n")
            r = subprocess.run(["bash", os.path.join(REPO, "adopt", "install-ratchet.sh"), "DOC.md"],
                               cwd=tmp, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            man = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))
            self.assertIn("scaffold/guardrails/gate_lib.py", man["vendored"])


class TestSpecStatesTheLaw(unittest.TestCase):
    def test_spec_block_and_index_row(self):
        spec = read(SPEC)
        self.assertIn("the check reads vendored pins", spec)
        self.assertIn("| INV-177 |", spec)


if __name__ == "__main__":
    unittest.main()
