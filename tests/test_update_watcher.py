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
import re
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
            self.assertIn("install-style-gates.sh --force", r.stdout)
            self.assertNotIn("install-scaffold.sh --force", r.stdout,
                              "a style-gate-only stale key must not propose the scaffold road")
            self.assertIn("PROPOSAL ONLY", r.stdout)

    def test_stale_scaffold_key_proposes_the_scaffold_reinstall_road(self):
        # Defect 3 (2026-07-16 fix): the road named must match the kit that is actually stale — a
        # scaffold-only host was pointed at the style-gate installer, which never touches
        # scaffold/guardrails/.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scaffold/guardrails/gate_lib.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stale vs current pack: scaffold/guardrails/gate_lib.py", r.stdout)
            self.assertIn("install-scaffold.sh --force", r.stdout)
            self.assertNotIn("install-style-gates.sh --force", r.stdout,
                              "a scaffold-only stale key must not propose the style-gate road")

    def test_stale_run_mode_keys_propose_the_scaffold_road(self):
        # q-832 (2026-09-09): install-scaffold.sh vendors five run-mode files under their
        # host-relative paths, outside the scaffold/guardrails/ prefix the sorting used to test.
        # A host stale on exactly those was handed install-style-gates.sh, whose vendor set holds
        # none of them, so following the advice changed nothing and the watcher repeated it.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"guardrails/run_modes.py": "0" * 64,
                                    "scripts/task-admission.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stale vs current pack: guardrails/run_modes.py", r.stdout)
            self.assertIn("stale vs current pack: scripts/task-admission.py", r.stdout)
            self.assertIn("install-scaffold.sh --force", r.stdout)
            self.assertNotIn("install-style-gates.sh --force", r.stdout,
                             "run-mode files are vendored by install-scaffold.sh, so the "
                             "style-gate road repairs nothing a host stale on them can use")

    def test_stale_style_gate_keys_still_propose_the_style_gate_road_alone(self):
        # The other side of the same sorting: widening what counts as scaffold must not pull a
        # style-gate vendor file across with it.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/spec-style-lint.py": "0" * 64,
                                    "scripts/spec-freeze.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stale vs current pack: scripts/spec-style-lint.py", r.stdout)
            self.assertIn("install-style-gates.sh --force", r.stdout)
            self.assertNotIn("install-scaffold.sh --force", r.stdout,
                             "a style-gate-only stale set must not propose the scaffold road")

    def test_the_scaffold_road_reads_the_installers_own_vendor_list(self):
        # The sorting reads adopt/install-scaffold.sh's VENDOR_MODES array rather than keeping a
        # second copy of it, so the two cannot drift apart. Every pack-relative half of that array
        # is claimed by the scaffold road.
        with open(os.path.join(REPO, "adopt", "install-scaffold.sh"), encoding="utf-8") as fh:
            installer = fh.read()
        block = re.search(r"VENDOR_MODES=\((.*?)\n\)", installer, re.S)
        self.assertIsNotNone(block, "install-scaffold.sh no longer carries a VENDOR_MODES array")
        pairs = [q.split("|")[0] for q in re.findall(r'"([^"]+)"', block.group(1))]
        self.assertTrue(pairs, "VENDOR_MODES is empty")
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {rel: "0" * 64 for rel in pairs}}, open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("install-scaffold.sh --force", r.stdout)
            self.assertNotIn("install-style-gates.sh --force", r.stdout,
                             "every file the scaffold installer vendors takes the scaffold road")

    def test_stale_status_view_keys_propose_the_status_view_road(self):
        # The third kit. adopt/install-status-view.sh keeps its own VENDOR array and writes its
        # keys into the same manifest, so a rule that knows only two installers sends a host stale
        # on these to one that carries none of them — the same defect one kit over.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/render-board.sh": "0" * 64,
                                    "scaffold/status-view/state-probe.sh": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("install-status-view.sh --force", r.stdout)
            self.assertNotIn("install-style-gates.sh --force", r.stdout,
                             "install-status-view.sh is what re-vendors the status-view kit")
            self.assertNotIn("install-scaffold.sh --force", r.stdout)

    def test_a_key_no_installer_vendors_is_said_rather_than_routed(self):
        # A key that reaches the manifest from somewhere else must not fall through to whichever
        # road the code happened to end on. scripts/stamp-versions.py is a real pack file that no
        # adopt installer vendors.
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/stamp-versions.py": "0" * 64}}, open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("no installer under adopt/ vendors scripts/stamp-versions.py", r.stdout)
            self.assertNotIn("--force", r.stdout,
                             "no installer claims this key, so no re-install road is named")

    def test_every_adopt_installer_is_a_road_the_watcher_can_name(self):
        # The sorting reads every adopt/install-*.sh rather than a list beside them, so a kit added
        # later is routed without touching the watcher. Each installer's own array, driven through
        # the real script, comes back as that installer's road.
        adopt = os.path.join(REPO, "adopt")
        installers = sorted(n for n in os.listdir(adopt)
                            if n.startswith("install-") and n.endswith(".sh"))
        self.assertGreaterEqual(len(installers), 3, installers)
        for name in installers:
            with open(os.path.join(adopt, name), encoding="utf-8") as fh:
                body = fh.read()
            keys = []
            for array in re.findall(r"VENDOR[A-Z_]*=\((.*?)\n\)", body, re.S):
                for entry in re.findall(r'"([^"]+)"', array):
                    rel = entry.split("|")[0]
                    keys.append(rel if "/" in rel else "scaffold/guardrails/" + rel)
            self.assertTrue(keys, "%s carries no vendor array the watcher can read" % name)
            with tempfile.TemporaryDirectory() as tmp:
                man = os.path.join(tmp, "ratchet-manifest.json")
                json.dump({"pack_version": "0.0.1",
                           "vendored": {k: "0" * 64 for k in keys}}, open(man, "w"))
                r = run_check(tmp, manifest=man)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertNotIn("no installer under adopt/ vendors", r.stdout,
                                 "%s's own keys must all resolve to a road" % name)
                self.assertIn("adopt/%s --force" % name, r.stdout,
                              "%s's own keys must name %s" % (name, name))

    def test_mixed_stale_keys_propose_both_reinstall_roads(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"scripts/gate_common.py": "0" * 64,
                                    "scaffold/guardrails/gate_lib.py": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("install-style-gates.sh --force", r.stdout)
            self.assertIn("install-scaffold.sh --force", r.stdout)

    def test_all_three_kits_stale_propose_all_three_roads(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1",
                       "vendored": {"guardrails/run_modes.py": "0" * 64,
                                    "scripts/spec-style-lint.py": "0" * 64,
                                    "scripts/render-board.sh": "0" * 64}},
                      open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for name in ("install-scaffold.sh", "install-status-view.sh",
                         "install-style-gates.sh"):
                self.assertIn("%s --force" % name, r.stdout)

    def test_an_old_pin_with_nothing_stale_names_only_the_kits_it_pins(self):
        # The one branch the road-per-kit rewrite first left behind: nothing differs from the pack,
        # so there is nothing to sort, and the old code named install-style-gates.sh whatever the
        # host had adopted. A status-view-only host is told about its own kit and no other.
        import hashlib
        keys = ["scripts/render-board.sh", "scripts/plan-step.sh"]
        pins = {}
        for rel in keys:
            with open(os.path.join(REPO, rel), "rb") as fh:
                pins[rel] = hashlib.sha256(fh.read()).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            man = os.path.join(tmp, "ratchet-manifest.json")
            json.dump({"pack_version": "0.0.1", "vendored": pins}, open(man, "w"))
            r = run_check(tmp, manifest=man)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("the pin alone is old", r.stdout)
            self.assertIn("install-status-view.sh --force", r.stdout)
            self.assertNotIn("install-style-gates.sh --force", r.stdout,
                             "a host that pins only the status-view kit hears about that kit")
            self.assertNotIn("install-scaffold.sh --force", r.stdout)

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
            r = subprocess.run(["bash", os.path.join(REPO, "adopt", "install-style-gates.sh"), "DOC.md"],
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
