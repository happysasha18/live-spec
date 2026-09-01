"""tests/test_style_gate_kit.py — the turnkey style-gate adoption kit (SPEC INV-172) and the
canonical hook home (SPEC INV-173).

Two things under test: hooks/scissors-scan.py (the pack's own copy of the scissors Stop-hook,
universal tier only, with a personal-overlay hook and a quoted-demo skip) and
adopt/install-style-gates.sh (vendors the style lint, the near-duplicate reading, the freeze tool
and their shared library into a host repo, pins each vendored copy's source, and wires the style
gate into the host's push gate).

The installer used to do one more thing, and this file used to hold it under test: measure the
host's documents at adoption time, write those counts into scripts/spec-debt-cap.json as caps, and
generate tests/test_ratchet_lock.py to pin them. That was a bound seeded from whatever the host's
documents happened to measure that day, and a bound of that shape reds a delivery that improves the
document — proven on the pack's own copy 2026-08-19. The whole class was cut 2026-09-02; the tests
below assert the installer writes neither the cap file nor the lock test, and repairs a push gate
still calling the one it used to generate.
"""
import hashlib
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "scissors-scan.py")
INSTALL_PACK_HOOKS = os.path.join(ROOT, "scripts", "install-pack-hooks.sh")
INSTALL_STYLE_GATES = os.path.join(ROOT, "adopt", "install-style-gates.sh")
INSTALL_SCAFFOLD = os.path.join(ROOT, "adopt", "install-scaffold.sh")


def run(args, *, cwd, extra_env=None, input_text=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, env=env, input=input_text,
    )


def _write_transcript(tmp, lines):
    """Write a Stop-hook transcript .jsonl with one assistant text turn."""
    path = os.path.join(tmp, "transcript.jsonl")
    text = "\n".join(lines)
    ev = {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")
    return path


def _stop_payload(transcript_path):
    return json.dumps({"transcript_path": transcript_path, "stop_hook_active": False})


class TestCanonicalHook(unittest.TestCase):
    def test_canonical_hook_exists_with_universal_patterns_only(self):
        self.assertTrue(os.path.isfile(HOOK), "hooks/scissors-scan.py must ship")
        body = open(HOOK, encoding="utf-8").read()
        self.assertIn(r",\s+not\s+\S", body)
        self.assertIn(r"\s+—\s+not\s+\S", body)
        self.assertNotIn("а не", body)
        self.assertNotIn("но не", body)

    def test_hook_skips_quoted_demos(self):
        with tempfile.TemporaryDirectory() as tmp:
            transcript = _write_transcript(tmp, ["the «X — not Y» frame is banned"])
            result = run(["python3", HOOK], input_text=_stop_payload(transcript), cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout.strip(), "", "quoted demo must not fire the block")

            transcript2 = _write_transcript(tmp, ["this is good — not bad"])
            result2 = run(["python3", HOOK], input_text=_stop_payload(transcript2), cwd=ROOT)
            self.assertIn('"decision": "block"', result2.stdout)

    def test_hook_reads_personal_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "home")
            hooks_dir = os.path.join(home, ".claude", "hooks")
            os.makedirs(hooks_dir)
            overlay = os.path.join(hooks_dir, "scissors-personal.json")
            with open(overlay, "w", encoding="utf-8") as f:
                json.dump([r",\s+а\s+не\s+\S"], f)

            transcript = _write_transcript(tmp, ["свежий, а не недельный"])

            result = run(
                ["python3", HOOK],
                extra_env={"HOME": home},
                input_text=_stop_payload(transcript), cwd=ROOT,
            )
            self.assertIn('"decision": "block"', result.stdout)

            # without the overlay (a HOME with no scissors-personal.json), no block.
            home2 = os.path.join(tmp, "home2")
            os.makedirs(os.path.join(home2, ".claude", "hooks"))
            result2 = run(
                ["python3", HOOK],
                extra_env={"HOME": home2},
                input_text=_stop_payload(transcript), cwd=ROOT,
            )
            self.assertEqual(result2.returncode, 0)
            self.assertEqual(result2.stdout.strip(), "")


class TestInstaller(unittest.TestCase):
    def test_installer_dry_run_touches_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "home")
            os.makedirs(home)
            result = run(
                ["bash", INSTALL_PACK_HOOKS, "--dry-run"],
                extra_env={"HOME": home}, cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(
                os.path.exists(os.path.join(home, ".claude", "hooks", "scissors-scan.py"))
            )


class TestStyleGatesInstall(unittest.TestCase):
    VENDOR_FILES = (
        "scripts/spec-style-lint.py",
        "scripts/spec-redundancy-precheck.py",
        "scripts/spec-freeze.py",
        "scripts/gate_common.py",
        "guardrails/check-freeze.sh",
    )

    def _init_host(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def _measured_style_errors(self, doc_path):
        result = run(["python3", os.path.join(ROOT, "scripts", "spec-style-lint.py"),
                       "--tier", "universal", doc_path], cwd=ROOT)
        last_line = result.stdout.strip().splitlines()[-1]
        return json.loads(last_line)["errors"]

    def _write_doc(self, tmp):
        doc = os.path.join(tmp, "DOC.md")
        with open(doc, "w", encoding="utf-8") as f:
            f.write(
                "# Test doc\n\n"
                "The output is good — not bad quality.\n\n"
                "The result is good — not bad quality.\n"
            )
        return doc

    def test_install_vendors_the_gate_files_and_pins_each_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            doc = self._write_doc(tmp)
            self.assertGreater(self._measured_style_errors(doc), 0,
                               "fixture doc must trip at least one style error")

            result = run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            for rel in self.VENDOR_FILES:
                self.assertTrue(os.path.isfile(os.path.join(tmp, rel)), "missing vendored: %s" % rel)

            manifest_path = os.path.join(tmp, "scripts", "ratchet-manifest.json")
            self.assertTrue(os.path.isfile(manifest_path))
            manifest = json.load(open(manifest_path, encoding="utf-8"))
            pack_version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
            self.assertEqual(manifest["pack_version"], pack_version)
            for rel in self.VENDOR_FILES:
                actual_sha = hashlib.sha256(open(os.path.join(tmp, rel), "rb").read()).hexdigest()
                self.assertEqual(manifest["vendored"][rel], actual_sha)

    def test_install_seeds_no_ceiling_and_generates_no_lock_test(self):
        """The cut of 2026-09-02, held by a test: adoption reads the host's documents and prints
        what it finds, and writes down no count for anything to be held against later."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            self._write_doc(tmp)
            result = run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            self.assertFalse(os.path.exists(os.path.join(tmp, "scripts", "spec-debt-cap.json")),
                             "adoption must seed no debt cap at the host's current size")
            self.assertFalse(os.path.exists(os.path.join(tmp, "tests", "test_ratchet_lock.py")),
                             "adoption must generate no lock test pinning a seeded count")

            manifest = json.load(
                open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8"))
            self.assertNotIn("seeded", manifest,
                             "the manifest must record no measured size for anything to hold to")

    def test_a_prior_install_s_seeded_counts_are_dropped_from_the_manifest(self):
        """A host that ran the retired ratchet kit carries a `seeded` block naming two counts. A
        re-run clears it, so no later reader mistakes a record of one day's size for a live bound."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            self._write_doc(tmp)
            os.makedirs(os.path.join(tmp, "scripts"))
            json.dump({"pack_version": "0.0.1", "vendored": {},
                       "seeded": {"style_errors": 12, "redundancy_open": 40}},
                      open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), "w"))

            result = run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.load(
                open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8"))
            self.assertNotIn("seeded", manifest)


class TestStyleGatesMissingDoc(unittest.TestCase):
    """Defect (2026-08-18 show-rehearsal report): on a fresh project, before step 2 (or a by-hand
    doc write) has created the gated doc, the installer must refuse with a clean human-readable
    line and a non-zero exit — never a raw Python traceback. A doc resolved from
    guardrails.config.json's spec_path but not yet written to disk is the ordinary state of a fresh
    project, not breakage, so the refusal must say so and must leave nothing vendored.
    """

    def _init_host(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def test_doc_named_on_argv_but_absent_fails_cleanly_not_with_a_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            result = run(["bash", INSTALL_STYLE_GATES, "PRODUCT_SPEC.md"], cwd=tmp)
            self.assertNotEqual(result.returncode, 0, "a missing doc must not silently succeed")
            combined = result.stdout + result.stderr
            self.assertNotIn("Traceback (most recent call last)", combined,
                              "must be a clean refusal, not a raw Python traceback")
            self.assertNotIn("JSONDecodeError", combined)
            self.assertIn("PRODUCT_SPEC.md", result.stdout)
            self.assertFalse(os.path.exists(os.path.join(tmp, "scripts", "spec-style-lint.py")),
                              "a clean refusal must vendor nothing")

    def test_doc_resolved_from_config_but_absent_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            config = {"spec_path": "PRODUCT_SPEC.md"}
            with open(os.path.join(tmp, "guardrails.config.json"), "w", encoding="utf-8") as f:
                json.dump(config, f)
            # No PRODUCT_SPEC.md written — the ordinary state of a fresh project before step 2.
            result = run(["bash", INSTALL_STYLE_GATES], cwd=tmp)
            self.assertNotEqual(result.returncode, 0)
            combined = result.stdout + result.stderr
            self.assertNotIn("Traceback (most recent call last)", combined)
            self.assertNotIn("JSONDecodeError", combined)
            self.assertFalse(os.path.exists(os.path.join(tmp, "scripts", "spec-style-lint.py")))

    def test_doc_present_after_the_fact_installs_cleanly(self):
        """Proves the refusal is transient, not a permanent block: write the doc and re-run."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            result = run(["bash", INSTALL_STYLE_GATES, "PRODUCT_SPEC.md"], cwd=tmp)
            self.assertNotEqual(result.returncode, 0)

            with open(os.path.join(tmp, "PRODUCT_SPEC.md"), "w", encoding="utf-8") as f:
                f.write("# Spec\n\nA plain sentence.\n")
            result2 = run(["bash", INSTALL_STYLE_GATES, "PRODUCT_SPEC.md"], cwd=tmp)
            self.assertEqual(result2.returncode, 0, result2.stdout + result2.stderr)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "scripts", "spec-style-lint.py")))


class TestGateRWiring(unittest.TestCase):
    """Defect 1 (2026-07-16 track-coach report,
    inbox/2026-07-16-from-track-coach-install-ratchet-appends-past-exit.md): the installer's wiring
    step must not blind-append the gate-r block past a host pre-push's terminating exit — that
    lands the block as dead code while the installer still reports "wired". The insertion ladder:
    before a trailing fail-check if one is found; else above a trailing bare exit; else append (the
    plain-EOF case); manual recipe when no safe anchor is found. Idempotency keys off a stable
    marker, repairing a marker (or drifted label) caught in a dead position — and, since 2026-09-02,
    repairing a live block that still calls the retired lock test.
    """

    def _init_host(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def _write_pre_push(self, tmp, body):
        path = os.path.join(tmp, "guardrails", "pre-push")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        return path

    def _install(self, tmp):
        doc = os.path.join(tmp, "DOC.md")
        if not os.path.isfile(doc):
            open(doc, "w", encoding="utf-8").write("# Doc\n\nA plain sentence.\n")
        return run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)

    def _lines(self, path):
        return open(path, encoding="utf-8").read().splitlines()

    def _index(self, lines, needle):
        for i, line in enumerate(lines):
            if needle in line:
                return i
        return -1

    def test_a_trailing_bare_exit_inserts_above_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            path = self._write_pre_push(tmp, "#!/bin/sh\necho hello\nexit 0\n")
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("wired: guardrails/pre-push gate r", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            lines = self._lines(path)
            marker_i = self._index(lines, "live-spec:gate-r")
            exit_i = self._index(lines, "exit 0")
            self.assertGreaterEqual(marker_i, 0)
            self.assertLess(marker_i, exit_i, "gate r must land BEFORE the trailing exit, not after")

    def test_b_trailing_fail_check_inserts_before_it_not_just_before_the_final_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = (
                "#!/bin/sh\n"
                "fail=0\n"
                'if [ "$fail" -ne 0 ]; then\n'
                "  echo blocked\n"
                "  exit 1\n"
                "fi\n"
                "echo ok\n"
                "exit 0\n"
            )
            path = self._write_pre_push(tmp, body)
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("wired: guardrails/pre-push gate r", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            lines = self._lines(path)
            marker_i = self._index(lines, "live-spec:gate-r")
            fail_check_i = self._index(lines, 'if [ "$fail" -ne 0 ]; then')
            self.assertGreaterEqual(marker_i, 0)
            self.assertLess(marker_i, fail_check_i,
                             "gate r must land before the fail-check, not merely before the final exit")

    def test_c_no_exit_at_all_appends_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = "#!/bin/sh\necho no exit statement here\n"
            path = self._write_pre_push(tmp, body)
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("wired: guardrails/pre-push gate r", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            lines = self._lines(path)
            marker_i = self._index(lines, "live-spec:gate-r")
            echo_i = self._index(lines, "echo no exit statement here")
            self.assertGreater(marker_i, echo_i)

    def test_d_marker_in_dead_position_is_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = (
                "#!/bin/sh\n"
                "fail=0\n"
                'if [ "$fail" -ne 0 ]; then\n'
                "  exit 1\n"
                "fi\n"
                "exit 0\n"
                "\n"
                "# live-spec:gate-r\n"
                'echo ""\n'
                'echo "-- gate r — ratchet caps --"\n'
                "if ! python3 -m pytest -q tests/test_ratchet_lock.py; then\n"
                "  fail=1\n"
                "fi\n"
            )
            path = self._write_pre_push(tmp, body)
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("repaired: guardrails/pre-push gate r", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            lines = self._lines(path)
            self.assertEqual(
                sum(1 for line in lines if "live-spec:gate-r" in line), 1,
                "repair must not leave a duplicate block")
            marker_i = self._index(lines, "live-spec:gate-r")
            fail_check_i = self._index(lines, 'if [ "$fail" -ne 0 ]; then')
            self.assertLess(marker_i, fail_check_i, "repair must move the block to the safe anchor")

    def test_d2_drifted_label_in_dead_position_is_repaired_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = (
                "#!/bin/sh\n"
                "fail=0\n"
                'if [ "$fail" -ne 0 ]; then\n'
                "  exit 1\n"
                "fi\n"
                "exit 0\n"
                "\n"
                'echo ""\n'
                'echo "-- gate r: ratchet caps --"\n'
                "if ! python3 -m pytest -q tests/test_ratchet_lock.py; then\n"
                "  fail=1\n"
                "fi\n"
            )
            path = self._write_pre_push(tmp, body)
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("repaired", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            lines = self._lines(path)
            self.assertEqual(
                sum(1 for line in lines if "live-spec:gate-r" in line), 1,
                "repair of a drifted label must not leave a duplicate block")
            self.assertEqual(
                sum(1 for line in lines if "ratchet caps" in line), 0,
                "the drifted old block must be gone, not left standing beside the new one")

    def test_e_marker_in_live_position_stays_already_wired_and_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = (
                "#!/bin/sh\n"
                "fail=0\n"
                "\n"
                "# live-spec:gate-r\n"
                'echo ""\n'
                'echo "-- gate r — style gate --"\n'
                "for doc in DOC.md; do\n"
                '  if ! python3 scripts/spec-style-lint.py --tier universal "$doc"; then\n'
                "    fail=1\n"
                "  fi\n"
                "done\n"
                "\n"
                'if [ "$fail" -ne 0 ]; then\n'
                "  exit 1\n"
                "fi\n"
                "exit 0\n"
            )
            path = self._write_pre_push(tmp, body)
            before = open(path, encoding="utf-8").read()
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("already wired: guardrails/pre-push gate r", result.stdout)
            after = open(path, encoding="utf-8").read()
            self.assertEqual(before, after, "an already-live wiring must not be touched")

    def test_e2_a_live_block_calling_the_retired_lock_test_is_replaced(self):
        """A host adopted under the retired ratchet kit carries a live gate-r block running
        tests/test_ratchet_lock.py — a file this installer no longer writes. Re-running must replace
        that block rather than report it already wired and leave the host pushing against a test
        that is not there."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            body = (
                "#!/bin/sh\n"
                "fail=0\n"
                "\n"
                "# live-spec:gate-r\n"
                'echo ""\n'
                'echo "-- gate r — ratchet caps --"\n'
                "if ! python3 -m pytest -q tests/test_ratchet_lock.py; then\n"
                "  fail=1\n"
                "fi\n"
                "\n"
                'if [ "$fail" -ne 0 ]; then\n'
                "  exit 1\n"
                "fi\n"
                "exit 0\n"
            )
            path = self._write_pre_push(tmp, body)
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("repaired: guardrails/pre-push gate r", result.stdout)
            self.assertEqual(run(["bash", "-n", path], cwd=ROOT).returncode, 0, "must stay valid bash")
            text = open(path, encoding="utf-8").read()
            self.assertNotIn("test_ratchet_lock", text,
                             "the retired lock test must no longer be called")
            self.assertIn("spec-style-lint.py", text)
            self.assertEqual(text.count("live-spec:gate-r"), 1)

    def test_f_ambiguous_tail_prints_manual_recipe_and_does_not_touch_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            # a bare top-level exit that is NOT the last line and is not a fail-check — the tail is
            # not a plain end-of-file, and the heuristics cannot safely classify it.
            body = (
                "#!/bin/sh\n"
                "echo start\n"
                "exit 0\n"
                "echo unreachable already, appended by hand after someone's own exit\n"
            )
            path = self._write_pre_push(tmp, body)
            before = open(path, encoding="utf-8").read()
            result = self._install(tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("no safe wiring point", result.stdout)
            after = open(path, encoding="utf-8").read()
            self.assertEqual(before, after, "an ambiguous tail must never be blind-appended")


class TestManifestMerge(unittest.TestCase):
    """Defect 2 (2026-07-16 fix): the installer must MERGE the manifest, not rebuild it from
    scratch — a prior scaffold install's keys survive a later run, and a stale host-relative
    scaffold key an old run wrote gets deduped (mirrors install-scaffold.sh's own dedupe).
    """

    SCAFFOLD_NAMES = ("check_completeness.py", "check_tests_present.py",
                       "check_traces_to_spec.py", "check_conflicts.py", "gate_lib.py")

    def _init_host(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def test_scaffold_keys_survive_a_later_style_gate_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            open(os.path.join(tmp, "DOC.md"), "w", encoding="utf-8").write(
                "# Doc\n\nA plain sentence.\n")

            r1 = run(["bash", INSTALL_SCAFFOLD], cwd=tmp)
            self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)

            r2 = run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)
            self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)

            manifest = json.load(
                open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8"))
            for name in self.SCAFFOLD_NAMES:
                key = "scaffold/guardrails/%s" % name
                self.assertIn(key, manifest["vendored"], "the style-gate run dropped scaffold key %s" % key)
                pack_src = os.path.join(ROOT, key)
                self.assertEqual(
                    manifest["vendored"][key],
                    hashlib.sha256(open(pack_src, "rb").read()).hexdigest(),
                    "scaffold key %s must still resolve against the pack" % key)

    def test_stale_host_relative_scaffold_key_deduped_on_reinstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_host(tmp)
            open(os.path.join(tmp, "DOC.md"), "w", encoding="utf-8").write(
                "# Doc\n\nA plain sentence.\n")
            os.makedirs(os.path.join(tmp, "scripts"))
            prior = {"pack_version": "0.0.1",
                     "vendored": {"guardrails/gate_lib.py": "c" * 64}}
            json.dump(prior, open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), "w"))

            result = run(["bash", INSTALL_STYLE_GATES, "DOC.md"], cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.load(
                open(os.path.join(tmp, "scripts", "ratchet-manifest.json"), encoding="utf-8"))
            self.assertNotIn("guardrails/gate_lib.py", manifest["vendored"],
                              "stale host-relative scaffold key must be deduped")


if __name__ == "__main__":
    unittest.main()
