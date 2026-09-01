"""tests/test_scaffold_install.py — the turnkey scaffold-adoption kit (SPEC INV-97, INV-177).

adopt/install-scaffold.sh vendors the four project-side checks + their shared library + README into a
host's guardrails/, seeds the host's guardrails config from the example (never clobbering a filled one),
and writes or MERGES the one ratchet manifest (scripts/ratchet-manifest.json) — pinning each vendored
check under its pack-relative source path so the daily update check resolves it against the pack and can
tell a current copy from a stale one. A host that already ran the ratchet installer keeps its ratchet
entries untouched. Mirrors the shape of TestStyleGatesInstall in test_style_gate_kit.py.
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL_SCAFFOLD = os.path.join(ROOT, "adopt", "install-scaffold.sh")
CHECK_UPDATE = os.path.join(ROOT, "scripts", "check-pack-update.sh")

SCAFFOLD_CODE = (
    "check_completeness.py",
    "check_tests_present.py",
    "check_traces_to_spec.py",
    "check_conflicts.py",
    "gate_lib.py",
)


def run(args, cwd=None, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, env=env)


def _init_host(tmp):
    run(["git", "init", "-q"], cwd=tmp)
    run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
    run(["git", "config", "user.name", "a"], cwd=tmp)


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


class TestScaffoldInstall(unittest.TestCase):
    def test_vendors_checks_seeds_config_and_pins_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            for name in SCAFFOLD_CODE + ("README.md",):
                self.assertTrue(os.path.isfile(os.path.join(tmp, "guardrails", name)),
                                "missing vendored: guardrails/%s" % name)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "guardrails.config.json")))

            manifest_path = os.path.join(tmp, "scripts", "ratchet-manifest.json")
            self.assertTrue(os.path.isfile(manifest_path))
            manifest = json.load(open(manifest_path, encoding="utf-8"))
            pack_version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
            self.assertEqual(manifest["pack_version"], pack_version)

            for name in SCAFFOLD_CODE:
                key = "scaffold/guardrails/%s" % name
                self.assertIn(key, manifest["vendored"])
                self.assertEqual(manifest["vendored"][key],
                                 _sha(os.path.join(tmp, "guardrails", name)))
            # README and config are vendored but not pinned (docs/host-owned, not staleness targets).
            self.assertNotIn("scaffold/guardrails/README.md", manifest["vendored"])

    def test_manifest_key_resolves_against_the_pack_source(self):
        # the pinned key must point at the pack's own copy of the check (scaffold/guardrails/), so the
        # sha the installer pins equals the pack source's sha — that is what makes staleness detectable.
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            manifest = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))
            for name in SCAFFOLD_CODE:
                key = "scaffold/guardrails/%s" % name
                pack_src = os.path.join(ROOT, key)
                self.assertTrue(os.path.isfile(pack_src), "key must resolve against pack: %s" % key)
                self.assertEqual(manifest["vendored"][key], _sha(pack_src))

    def test_merge_preserves_ratchet_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            os.makedirs(os.path.join(tmp, "scripts"))
            prior = {
                "pack_version": "0.0.1",
                "vendored": {"scripts/spec-style-lint.py": "a" * 64,
                             "guardrails/check-freeze.sh": "b" * 64},
                "seeded": {"style_errors": 3, "redundancy_open": 1},
                "tier": "universal",
            }
            json.dump(prior, open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), "w"))

            result = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))

            # the other kit's entries survive untouched, a legacy `seeded` block included
            self.assertEqual(manifest["vendored"]["scripts/spec-style-lint.py"], "a" * 64)
            self.assertEqual(manifest["vendored"]["guardrails/check-freeze.sh"], "b" * 64)
            self.assertEqual(manifest["seeded"], {"style_errors": 3, "redundancy_open": 1})
            self.assertEqual(manifest["tier"], "universal")
            # scaffold keys added; pack_version advanced to current
            for name in SCAFFOLD_CODE:
                self.assertIn("scaffold/guardrails/%s" % name, manifest["vendored"])
            self.assertNotEqual(manifest["pack_version"], "0.0.1")

    def test_idempotent_rerun_no_duplicate_or_stale_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            first = open(os.path.join(tmp, "scripts", "ratchet-manifest.json")).read()
            run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            second = open(os.path.join(tmp, "scripts", "ratchet-manifest.json")).read()
            self.assertEqual(first, second, "re-run must be idempotent")
            manifest = json.loads(second)
            # no broken host-relative guardrails/<name> scaffold keys
            for name in SCAFFOLD_CODE:
                self.assertNotIn("guardrails/%s" % name, manifest["vendored"])

    def test_dedupes_prior_host_relative_scaffold_pin(self):
        # a ratchet run that opportunistically pinned guardrails/<name> gets that broken key replaced by
        # the pack-relative one, not duplicated.
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            os.makedirs(os.path.join(tmp, "scripts"))
            prior = {"pack_version": "0.0.1",
                     "vendored": {"guardrails/check_completeness.py": "c" * 64}}
            json.dump(prior, open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), "w"))
            run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            manifest = json.load(open(os.path.join(tmp, "scripts", "ratchet-manifest.json")))
            self.assertNotIn("guardrails/check_completeness.py", manifest["vendored"])
            self.assertIn("scaffold/guardrails/check_completeness.py", manifest["vendored"])

    def test_never_clobbers_a_filled_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_host(tmp)
            cfg = os.path.join(tmp, "guardrails.config.json")
            open(cfg, "w").write('{"spec_path": "MY_SPEC.md"}\n')
            run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(open(cfg).read(), '{"spec_path": "MY_SPEC.md"}\n')

    def test_watcher_flags_scaffold_staleness_after_pack_moves(self):
        # the whole point (SPEC INV-177): a scaffold-only host now gains a manifest the update check
        # reads, and a pack-side scaffold change with a version bump flags the stale file by name.
        with tempfile.TemporaryDirectory() as tmp:
            packcopy = os.path.join(tmp, "pack")
            host = os.path.join(tmp, "host")
            shutil.copytree(ROOT, packcopy, ignore=shutil.ignore_patterns(".git"))
            os.makedirs(host)
            _init_host(host)

            installer = os.path.join(packcopy, "adopt", "install-scaffold.sh")
            self.assertEqual(run(["bash", installer], cwd=host).returncode, 0)

            # pack moves ahead: bump VERSION + change a vendored check
            open(os.path.join(packcopy, "VERSION"), "w").write("9.9.9")
            with open(os.path.join(packcopy, "scaffold", "guardrails", "check_conflicts.py"), "a") as f:
                f.write("\n# pack-side change\n")

            remote = os.path.join(tmp, "REMOTE")
            open(remote, "w").write("9.9.9")
            stamp = os.path.join(tmp, "stamp")
            r = run(["bash", os.path.join(packcopy, "scripts", "check-pack-update.sh"),
                     "--remote-file", remote, "--installed-file", os.path.join(packcopy, "VERSION"),
                     "--stamp-file", stamp, "--force", "--pack-root", packcopy], cwd=host)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("VENDORED GATES PINNED", r.stdout)
            self.assertIn("stale vs current pack: scaffold/guardrails/check_conflicts.py", r.stdout)


if __name__ == "__main__":
    unittest.main()
