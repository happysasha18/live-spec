"""The unit half of the guardrail tests (fast lane, ROADMAP row 366 hygiene home).

Every class here reads config or text, or runs one guardrail script on a small
fixture. This file's contract: no repository copy, no git sandbox, no nested
pytest and no pre-push run. The sandboxed integration half stays in
tests/test_guardrails.py and runs on explicit ask and in the full suite. Shared
helpers keep their one home in test_guardrails and are imported here.
"""

import json
import os
import re
import subprocess
import tempfile
import unittest

from conftest import ROOT, open_spec
from test_guardrails import (
    GUARDRAILS,
    gate_machinery_diff,
    green_digest_matches,
    machinery_digest,
    record_green_digest,
    run,
)

class TestGateD_MatrixReference(unittest.TestCase):
    """Gate (d), row 477: the hand-walked coverage-validation checkbox gate retired, and gate d now
    runs the generated matrix-Reference gate (check-matrix-reference.py). The checkbox gate's own
    exercising tests retired with it; the reference gate is red-proven in tests/test_matrix_reference.py
    (gate d's registered red proof). Here we hold only the guardrails-level facts: the new gate passes
    the real matrix, and the retired script is no longer wired into the push gate."""

    def test_real_matrix_passes(self):
        result = run(["python3", os.path.join(GUARDRAILS, "check-matrix-reference.py"),
                      os.path.join(ROOT, "TEST_MATRIX.md")], cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("reach:", result.stdout)

    def test_missing_file_fails(self):
        result = run(["python3", os.path.join(GUARDRAILS, "check-matrix-reference.py"),
                      "/nonexistent/TEST_MATRIX.md"], cwd=ROOT)
        self.assertEqual(result.returncode, 1)

    def test_retired_checkbox_gate_unwired(self):
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            body = f.read()
        self.assertNotIn("check-matrix-coverage.sh", body,
                         "the retired checkbox gate is still wired into pre-push")


class TestScratchRunDigestCache(unittest.TestCase):
    """Row 573: the last-green digest memory behind the suite-in-suite scratch runs — a
    machinery byte-change re-fires the run, an unchanged machinery skips it, and a missing
    or unreadable store stays conservative."""

    def test_digest_moves_on_a_machinery_byte_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            gd = os.path.join(tmp, "guardrails")
            os.makedirs(gd)
            with open(os.path.join(gd, "check.sh"), "w", encoding="utf-8") as f:
                f.write("echo one\n")
            d1 = machinery_digest(root=tmp)
            with open(os.path.join(gd, "check.sh"), "w", encoding="utf-8") as f:
                f.write("echo two\n")
            d2 = machinery_digest(root=tmp)
            self.assertNotEqual(d1, d2)

    def test_store_round_trip_and_conservative_misses(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "sub", "store.json")
            old = os.environ.get("LIVE_SPEC_META_STORE")
            os.environ["LIVE_SPEC_META_STORE"] = store
            try:
                self.assertFalse(green_digest_matches("t", "abc"),
                                 "a missing store must be conservative (no match)")
                record_green_digest("t", "abc")
                self.assertTrue(green_digest_matches("t", "abc"))
                self.assertFalse(green_digest_matches("t", "def"),
                                 "a changed digest must re-fire the run")
                self.assertFalse(green_digest_matches("other", "abc"),
                                 "each scratch test owns its own green record")
                with open(store, "w", encoding="utf-8") as f:
                    f.write("not json")
                self.assertFalse(green_digest_matches("t", "abc"),
                                 "an unreadable store must be conservative (no match)")
            finally:
                if old is None:
                    del os.environ["LIVE_SPEC_META_STORE"]
                else:
                    os.environ["LIVE_SPEC_META_STORE"] = old


class TestPrePush(unittest.TestCase):
    """pre-push wires the four check scripts together. It is NOT executed here:
    it calls check-tests.sh with no argument, which defaults to the real tests/
    dir — the very dir this file lives in — so running it from inside a test
    would make a running suite re-invoke itself (and its own re-invocation)
    without end. pre-push's real-repo behaviour is proven by a direct manual
    run outside the suite (recorded in the row-3 checkpoint); here we only
    assert its wiring is intact.
    """

    def test_pre_push_calls_all_four_checks(self):
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            body = f.read()
        for script in (
            "check-prover-record.sh",
            "check-tests.sh",
            "check-push-reach.sh",
            "check-matrix-reference.py",
            "check-prototype-fence.sh",
            "check-shipped-language.sh",
        ):
            self.assertIn(script, body, "pre-push no longer wires in %s" % script)
        self.assertIn("gate c", body.lower())

    def test_reach_classified_once_before_gate_a(self):
        # P2-lite: the reach classifier runs exactly once, ahead of gate a, and both
        # gates a and b read that one verdict — never a second classifier run.
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            body = f.read()
        call = '"$GUARDRAILS/check-push-reach.sh"'
        self.assertEqual(body.count(call), 1,
                         "the reach classifier must be invoked exactly once")
        self.assertLess(body.index(call), body.index("-- gate a"),
                        "the reach verdict must exist before gate a reads it")

    def test_gate_a_runs_the_record_check_on_every_reach_verdict(self):
        # The 2718c69 stand-down is reverted (the owner's 2026-08-15 word): a prose-only or
        # scoped diff still carries commits a push range must answer for, so gate a reads the
        # reach verdict for nothing. The record check runs unconditionally again; the only
        # stand-downs that exist are the two PRODUCT_SPEC.md R226.6 names by hand.
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            body = f.read()
        gate_a = body[body.index("-- gate a"):body.index("-- gate b")]
        self.assertNotIn('case "$reach_code" in', gate_a,
                         "gate a must not branch on the reach verdict")
        self.assertRegex(
            gate_a, r'if ! "\$GUARDRAILS/check-prover-record\.sh" --push',
            "gate a must run the prover-record check")


class TestThePrePushChainIsTheFastSet(unittest.TestCase):
    """The local chain runs the checks that take seconds; the suite is the server's job (2026-08-18).

    Measured on this machine: every gate in the chain except gate b finishes inside about two and a
    half minutes together, and gate b — the whole pytest suite — takes over twenty on its own. The
    server already runs that suite on every push, so a local re-run bought a slower push and no new
    protection. Gate b is therefore the one member of the chain the local run leaves to the server,
    and `LIVE_SPEC_PUSH_FULL=1` puts it back, reach-scoped, exactly as the chain always ran it.

    pre-push is not executed here: it would call check-tests.sh, which defaults to the very tests/
    dir this file lives in. The class asserts its wiring, the same way TestPrePush above does.
    """

    def _body(self):
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            return f.read()

    def _gate_b_block(self):
        body = self._body()
        return body[body.index("-- gate b"):body.index("-- gate c")]

    def test_the_suite_does_not_run_locally_by_default(self):
        block = self._gate_b_block()
        self.assertIn('if [ -z "$PUSH_FULL" ]; then', block,
                      "gate b no longer branches on the full-chain flag, so a local push pays the "
                      "suite's twenty minutes again")
        default_arm = block[:block.index("else")]
        self.assertNotIn("check-tests.sh", default_arm,
                         "the default local chain still runs the suite")
        self.assertIn("gates.yml", default_arm,
                      "the default arm never says who runs the suite instead")

    def test_the_flag_is_named_where_a_person_will_look(self):
        block = self._gate_b_block()
        self.assertIn("LIVE_SPEC_PUSH_FULL=1", block,
                      "the printed line never names the flag that runs the suite locally")
        self.assertIn("LIVE_SPEC_PUSH_FULL", self._body().split("== live-spec push gate ==")[0],
                      "the flag is never read at the top of the chain")

    def test_the_old_chain_is_still_reachable_by_the_flag(self):
        """Reachable and unchanged: the flag's arm carries the reach-scoped suite the chain ran
        before, SCOPED_TEST_FILES and all, so nobody loses the old behaviour."""
        block = self._gate_b_block()
        full_arm = block[block.index("else"):]
        self.assertIn('case "$reach_code" in', full_arm)
        self.assertIn('SCOPED_TEST_FILES="$scoped_files" "$GUARDRAILS/check-tests.sh"', full_arm)
        self.assertIn('if ! "$GUARDRAILS/check-tests.sh"; then', full_arm)
        self.assertIn("prose-only diff: the suite stands down by name", full_arm)

    def test_only_the_two_slow_gates_are_conditional(self):
        """Speed must not cost a guarantee. Two gates read the flag: b, which the server runs
        anyway, and g, which stands down only for a diff that cannot have moved a pin. Every other
        gate — gate a's fresh prover record above all — runs on every push, flag or no flag."""
        body = self._body()
        conditional = ("$PUSH_FULL", "gate_g_can_skip")
        blocks = {
            "b": body[body.index("-- gate b"):body.index("-- gate c")],
            "g": body[body.index("-- gate g"):body.index("-- gate f")],
        }
        rest = body[body.index("== live-spec push gate =="):]
        for letter, block in blocks.items():
            rest = rest.replace(block, "")
            self.assertTrue(any(name in block for name in conditional),
                            "gate %s stopped reading the flag" % letter)
        for name in conditional:
            self.assertNotIn(name, rest,
                             "a third gate now depends on the flag — the fast chain dropped a "
                             "check whose whole value is running before the push")
        gate_a = body[body.index("-- gate a"):body.index("-- gate b")]
        self.assertRegex(gate_a, r'if ! "\$GUARDRAILS/check-prover-record\.sh" --push',
                         "gate a stopped running the prover-record check on every push")

    def _gate_g_block(self):
        body = self._body()
        return body[body.index("-- gate g"):body.index("-- gate f")]

    def _can_skip(self, changed, env=None):
        """Ask the chain's own `gate_g_can_skip` about one changed-file list.

        The function is sourced out of pre-push rather than copied here, so a test can never pass
        against a rule the chain stopped carrying."""
        body = self._body()
        start = body.index("gate_g_can_skip() {")
        end = body.index("\n}\n", start) + 3
        script = ('set -uo pipefail\ncd "$1"\nGUARDRAILS="$1/guardrails"\nREPO_ROOT="$1"\n'
                  'PUSH_FULL="${LIVE_SPEC_PUSH_FULL:-}"\n' + body[start:end]
                  + '\nif gate_g_can_skip; then echo SKIP; else echo RUN; fi\n')
        run_env = dict(os.environ, PIN_REACH_FILES=changed)
        run_env.pop("LIVE_SPEC_PUSH_FULL", None)
        run_env.update(env or {})
        out = subprocess.run(["bash", "-c", script, "bash", ROOT],
                             capture_output=True, text=True, env=run_env)
        self.assertTrue(out.stdout.strip(), out.stdout + out.stderr)
        verdict = out.stdout.strip().splitlines()[-1]
        self.assertIn(verdict, ("SKIP", "RUN"), out.stdout + out.stderr)
        return verdict == "SKIP"

    def test_gate_g_stands_down_when_the_diff_can_move_no_pin(self):
        """Gate g cost 56 seconds of every push on 2026-08-18, more than the rest of the fast set
        together. A diff that touches nothing a pin can name pays none of it."""
        self.assertTrue(self._can_skip("docs/PROGRESS.md\ninbox/2026-08-18-note.md"),
                        "gate g still runs on a diff that cannot have moved a pin")

    def test_gate_g_runs_on_anything_that_can_move_a_pin(self):
        """Three ways a pin moves: the page holding the pins, the page of range pins, and the skill
        files those range pins name. A fourth: the file an ARCHITECTURE.md pin points at."""
        for changed in ("ARCHITECTURE.md",
                        ".live-spec/r5-rule-prices-2026-08-11.md",
                        "skills/live-spec-base/SKILL.md",
                        "guardrails/check-pin-drift.sh"):
            self.assertFalse(self._can_skip(changed),
                             "gate g stood down on a diff touching %s, which can move a pin"
                             % changed)

    def test_gate_g_runs_when_the_answer_cannot_be_read(self):
        """Conservative by construction: no changed-file list and no usable base means run it."""
        self.assertFalse(self._can_skip("", env={"LIVE_SPEC_DIFF_BASE": "no-such-ref-for-a-test"}),
                         "gate g stood down on a diff it could not read")

    def test_the_flag_puts_gate_g_back_unconditionally(self):
        self.assertFalse(self._can_skip("docs/PROGRESS.md", env={"LIVE_SPEC_PUSH_FULL": "1"}),
                         "the full-chain flag no longer runs gate g on every push")

    def test_the_gate_g_stand_down_says_who_still_runs_it(self):
        block = self._gate_g_block()
        self.assertIn("gate_g_can_skip", block, "gate g no longer asks whether it can stand down")
        self.assertIn("check-pin-drift.sh", block, "gate g no longer runs its check at all")
        self.assertIn("gates.yml", block,
                      "the stand-down line never says the server still runs gate g")

    def test_the_server_runs_gate_g_on_every_push(self):
        """The real guarantee is not "no `if:` line" — it is "this step cannot be skipped for
        any reason but a cancelled run". A step with no `if:` at all runs unconditionally as
        long as the job itself is not cancelled. A step reading exactly
        `if: ${{ !cancelled() }}` runs under that same one condition — it removes the implicit
        `success()` GitHub Actions would otherwise attach, so an earlier gate's failure can no
        longer skip it (2026-08-19: every gate step in this job took that condition, so one push
        surfaces every finding instead of stopping at the first red gate). Either shape upholds
        gate g running on every push; anything else — a narrower or an additional clause — does
        not, and must red here. A substring check for "!cancelled()" would wave through
        `if: ${{ !cancelled() && github.actor == 'x' }}`, so the comparison is exact."""
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            workflow = f.read()
        step = workflow[workflow.index("name: gate g"):].split("- name:")[0]
        self.assertIn("check-pin-drift.sh", step,
                      "the server's gate g step no longer runs the pin-drift check")
        if_lines = [ln.strip() for ln in step.splitlines() if ln.strip().startswith("if:")]
        self.assertLessEqual(len(if_lines), 1,
                             "the server's gate g step carries more than one if: line: %r" % if_lines)
        if if_lines:
            self.assertEqual(
                if_lines[0], "if: ${{ !cancelled() }}",
                "the server's gate g step carries a condition narrower or wider than "
                "!cancelled() — the guarantee that it runs on every push weakened: %r"
                % if_lines[0])

    def test_the_server_still_runs_the_full_suite(self):
        """The other half of the split, read off the workflow itself."""
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            workflow = f.read()
        self.assertIn("name: test suite (gate b, full", workflow,
                      "the workflow no longer carries gate b's step, so nothing runs the suite")
        step = workflow[workflow.index("name: test suite (gate b, full"):]
        self.assertIn("python3 -m pytest -q", step.split("- name:")[0],
                      "the server's gate b step no longer runs the whole suite")


class TestGateF_SkillLoadability(unittest.TestCase):
    """Gate (f): every shipped skill LOADS — frontmatter parses, name matches its
    folder, description + metadata version present, a 'Work that belongs elsewhere' section
    scopes it negatively (row 80). Red-first proven on a broken scratch skill."""

    def test_real_repo_passes(self):
        result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"),
                      os.path.join(ROOT, "skills")], cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_broken_skill_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "broken")
            os.makedirs(bad)
            with open(os.path.join(bad, "SKILL.md"), "w") as f:
                f.write("---\nname: wrongname\n---\nno negative section\n")
            result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"), tmp], cwd=ROOT)
            self.assertEqual(result.returncode, 1, "broken skill must turn the gate RED")
            self.assertIn("does not match its folder", result.stdout)
            self.assertIn("no 'Work that belongs elsewhere' section", result.stdout)

    def test_missing_skills_dir_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"), tmp], cwd=ROOT)
            self.assertEqual(result.returncode, 1, "empty skills dir must fail, not pass silently")


class TestGateReachMap(unittest.TestCase):
    """Row 147 (M-142, INV-45): the reach map's deciding script — a prose-only diff
    stands the suite down; tested documents, unknown files, and empty diffs fall to
    FULL by construction."""

    SCRIPT = os.path.join(GUARDRAILS, "check-push-reach.sh")

    def reach(self, files):
        return run(["bash", self.SCRIPT], extra_env={"REACH_FILES": files}, cwd=ROOT)

    def test_prose_only_diff_stands_suite_down(self):
        r = self.reach("README.md\ndocs/research/example.md")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_tested_documents_stay_full_reach(self):
        # guardrails/pre-push and tests/test_traceability.py moved off this list at row 362
        # (M-344): both are now the INFRA class and ride the scoped middle road (exit 2), not
        # FULL — see the test_scoped_reach_* methods below for their scoped-verdict coverage.
        # The documents remaining here are genuinely outside PROSE union INFRA and must still
        # force FULL.
        for f in ("PRODUCT_SPEC.md", "TEST_MATRIX.md", "ARCHITECTURE.md", "ROADMAP.md",
                  "skills/publish/SKILL.md", "JOURNAL.md", "NEXT_STEPS.md"):
            r = self.reach("README.md\n" + f)
            self.assertEqual(r.returncode, 1, "%s must force FULL, got: %s" % (f, r.stdout))

    def test_unknown_and_empty_fall_to_full(self):
        self.assertEqual(self.reach("something/new-place.txt").returncode, 1)
        self.assertEqual(self.reach("\n").returncode, 1)

    def test_scoped_reach_guardrails_diff_exits_scoped(self):
        # row 362 (M-344): a lone INFRA change scopes to the test files that name it (found by
        # basename, one referrer level deep) plus the traceability net — never full.
        r = self.reach("guardrails/check-muted-launch.sh")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("SCOPED tests/test_muted_launch_guardrail.py", r.stdout)
        self.assertIn("SCOPED tests/test_traceability.py", r.stdout)

    def test_scoped_reach_unnamed_file_falls_full(self):
        # an INFRA file no test names (directly or via a referrer) is not safely scopable —
        # conservative fall-through to FULL, naming the untested file. Built via concatenation
        # so the fixture's own basename never sits as one literal token in this file — that
        # would make THIS file its own "owning test" via the grep-by-basename search and
        # defeat the fixture's whole point (an infra file NO test names).
        fname = "guardrails/zz-nothing-names-me" + ".sh"
        r = self.reach(fname)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(fname, r.stdout)

    def test_scoped_reach_mixed_diff_falls_full(self):
        # a diff outside PROSE union INFRA (PRODUCT_SPEC.md here) still forces FULL even
        # alongside a scopable INFRA file.
        r = self.reach("guardrails/check-muted-launch.sh\nPRODUCT_SPEC.md")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    # --- row 380 (M-405, INV-224): the reach classes are host config, not script constants ---

    def reach_with_config(self, files, config_path):
        return run(["bash", self.SCRIPT],
                   extra_env={"REACH_FILES": files, "REACH_CONFIG": config_path}, cwd=ROOT)

    def _write_config(self, tmpdir, mutate):
        """Write a fixture config: the committed config with reach_classes mutated in place.

        Only reach_classes differs from the pack default, so any verdict change the test sees is
        the reclassification alone, never a second drifted field."""
        with open(os.path.join(ROOT, "guardrails.config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        mutate(cfg["reach_classes"])
        path = os.path.join(tmpdir, "reach-fixture.config.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        return path

    def test_reach_reads_classes_from_config_flips_verdict(self):
        # The row's own case: track-coach keeps its product ENGINE under scripts/, so it must
        # class scripts/ OUT of infra — an engine change then reaches the full suite instead of
        # scoping to a couple of tests and false-greening. Proven here with the guardrails/ dir,
        # which reliably scopes by default: a fixture config that reclassifies it OUT of infra
        # must flip the verdict from SCOPED (2) to FULL (1). A script that read a body constant
        # would ignore the config and never flip — this is the red-first proof it reads config.
        f = "guardrails/check-muted-launch.sh"
        with tempfile.TemporaryDirectory() as tmpdir:
            default_cfg = self._write_config(tmpdir, lambda rc: None)
            self.assertEqual(self.reach_with_config(f, default_cfg).returncode, 2,
                             "the default classes must still scope a lone guardrails/ change")
            flipped = self._write_config(
                tmpdir,
                lambda rc: rc.__setitem__(
                    "infra_dirs", [d for d in rc["infra_dirs"] if d != "guardrails"]),
            )
            r = self.reach_with_config(f, flipped)
            self.assertEqual(r.returncode, 1,
                             "reclassifying guardrails/ out of infra must flip the verdict to "
                             "FULL — the script reads config, not a body constant: %s" % r.stdout)

    def test_reach_default_config_reproduces_todays_verdicts(self):
        # No-regression: the committed default config reproduces today's behaviour on the three
        # verdict classes — prose stands the suite down (0), a lone infra file scopes (2), an
        # unmapped file falls to full (1).
        self.assertEqual(self.reach("README.md\ndocs/research/example.md").returncode, 0)
        r = self.reach("guardrails/check-muted-launch.sh")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("SCOPED tests/test_traceability.py", r.stdout)
        self.assertEqual(self.reach("something/new-place.txt").returncode, 1)
        # the conservative floor: a config naming no classes leaves every file unclassified, so
        # the whole diff falls to FULL — never a false-green scope on a missing/empty config.
        with tempfile.TemporaryDirectory() as tmpdir:
            empty = self._write_config(
                tmpdir,
                lambda rc: rc.clear() or rc.update(
                    {"prose_files": [], "prose_dirs": [], "infra_dirs": [],
                     "infra_files": [], "infra_globs": [], "referrer_dirs": []}),
            )
            self.assertEqual(self.reach_with_config("README.md", empty).returncode, 1,
                             "an empty class config must fall to FULL, never scope")


class TestScopedReachHygiene(unittest.TestCase):
    """Row 366 (M-348, INV-45): the by-name discovery blind spot. check-push-reach.sh finds a
    changed infra file's owning tests by grepping the file's basename as a literal token over
    tests/test_*.py; a test that reaches an infra directory by directory walk or glob, never
    naming a changed file's basename, is invisible to that search and would silently escape
    every scoped run. This net statically scans the suite's own test files for such an
    enumeration and requires every match to ride along — pinned into the script's marked
    ALWAYS_SCOPED block, where tests/test_traceability.py now sits as the first permanent member,
    an integrity rider that rides every scoped run for the suite's own integrity [ROADMAP 366]."""

    SCRIPT = os.path.join(GUARDRAILS, "check-push-reach.sh")

    # the enumeration surfaces this scan catches: an unqualified directory walk (root-eligible),
    # the module-level glob call, a Path glob/rglob method call, and a directory listing call
    _ENUM_CALLS = (
        (re.compile(r"os\.walk\("), True),
        (re.compile(r"glob\.glob\("), False),
        (re.compile(r"\.rglob\("), False),
        (re.compile(r"\.glob\("), False),
        (re.compile(r"os\.listdir\("), False),
        (re.compile(r"\.iterdir\("), False),
        (re.compile(r"os\.scandir\("), False),
    )

    @staticmethod
    def _call_args(text, open_paren_index):
        """Return the balanced substring from an opening paren to its matching close."""
        depth = 0
        i = open_paren_index
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[open_paren_index:i + 1]
            i += 1
        return text[open_paren_index:]

    @classmethod
    def _enumerating_infra_tests(cls, scan_dir, infra_dirs):
        """Pure: the set of test_*.py basenames directly under scan_dir whose source contains
        an enumeration call naming one of infra_dirs in its arguments, or an unqualified
        whole-repository-root walk. scan_dir is a parameter precisely so the red-first proof
        can point this at a scratch directory instead of the real tree."""
        flagged = set()
        scan_dir = str(scan_dir)
        for name in sorted(os.listdir(scan_dir)):
            if not (name.startswith("test_") and name.endswith(".py")):
                continue
            path = os.path.join(scan_dir, name)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except OSError:
                continue
            for pattern, root_eligible in cls._ENUM_CALLS:
                if name in flagged:
                    break
                for m in pattern.finditer(text):
                    args = cls._call_args(text, m.end() - 1).strip()
                    if root_eligible and re.fullmatch(r"\(\s*ROOT\s*\)", args):
                        flagged.add(name)
                        break
                    if any(re.search(r"\b" + re.escape(d) + r"\b", args) for d in infra_dirs):
                        flagged.add(name)
                        break
        return flagged

    @staticmethod
    def _infra_dirs_from_config():
        """The referrer directory prefixes the reach map declares — read from their one home,
        guardrails.config.json's reach_classes.referrer_dirs (SPEC INV-224, ROADMAP 380). The
        classes moved off the script body to config, so this net reads the same one home the
        script reads, never a second copy."""
        with open(os.path.join(ROOT, "guardrails.config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        dirs = cfg.get("reach_classes", {}).get("referrer_dirs", [])
        assert dirs, "guardrails.config.json must declare reach_classes.referrer_dirs"
        return dirs

    @staticmethod
    def _always_scoped(script_text):
        """Parse the pinned test paths out of the script's ALWAYS_SCOPED marked block — the
        one home both the script's own scoped verdict and this net read from."""
        m = re.search(r"ALWAYS_SCOPED=\((.*?)\)", script_text, re.DOTALL)
        if not m:
            return set()
        return set(re.findall(r'"([^"]+)"', m.group(1)))

    def test_enumerating_infra_tests_are_pinned(self):
        with open(self.SCRIPT, encoding="utf-8") as f:
            script_text = f.read()
        self.assertTrue(
            "ALWAYS_SCOPED" in script_text,
            "check-push-reach.sh must carry the marked ALWAYS_SCOPED block — the one home "
            "the script's own scoped verdict and this net both read [ROADMAP 366]",
        )
        infra_dirs = self._infra_dirs_from_config()
        always_scoped = {os.path.basename(t) for t in self._always_scoped(script_text)}
        tests_dir = os.path.join(ROOT, "tests")
        flagged = self._enumerating_infra_tests(tests_dir, infra_dirs)
        # test_traceability.py is no longer special-cased here: it lives inside ALWAYS_SCOPED as
        # the integrity rider, so always_scoped already covers it [ROADMAP 366 fold].
        unpinned = flagged - always_scoped
        self.assertEqual(
            unpinned, set(),
            "enumerating infra test(s) not pinned into ALWAYS_SCOPED: %s" % sorted(unpinned),
        )
        # The fast-lane split (his word 2026-08-13 16:50): every scoped run rides the guardrail
        # unit half beside the traceability net, and the by-name discovery never pulls the
        # sandboxed integration half back in. Pinned three ways: both riders sit in the block,
        # the integration module sits in SCOPED_EXCLUDED, and a live scoped run proves both.
        self.assertIn("test_guardrails_unit.py", always_scoped)
        self.assertIn("test_traceability.py", always_scoped)
        excluded = re.search(r"SCOPED_EXCLUDED=\((.*?)\)", script_text, re.DOTALL)
        self.assertIsNotNone(excluded, "the SCOPED_EXCLUDED list left check-push-reach.sh")
        self.assertIn("tests/test_guardrails.py", excluded.group(1))
        live = subprocess.run(
            ["bash", self.SCRIPT],
            env={**os.environ, "REACH_FILES": "guardrails/check-freeze.sh"},
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(live.returncode, 2, live.stdout + live.stderr)
        self.assertIn("SCOPED tests/test_guardrails_unit.py", live.stdout)
        self.assertNotIn("SCOPED tests/test_guardrails.py", live.stdout)

    def test_synthetic_enumerating_infra_test_reds_unpinned(self):
        """Red-first proof of the net's own logic: a synthetic test file, planted in a scratch
        directory, that reaches an infra directory by name rather than by basename is flagged
        by the scanner; left unpinned it reads as a violation; pinning its name closes it. No
        real file is written into the repo tree — the scratch directory is cleaned by the
        context manager."""
        with open(self.SCRIPT, encoding="utf-8") as f:
            script_text = f.read()
        infra_dirs = self._infra_dirs_from_config()
        real_always_scoped = {os.path.basename(t) for t in self._always_scoped(script_text)}

        synth_name = "test_synth_enum.py"
        # built by concatenation at runtime: the WRITTEN fixture carries a real enumeration
        # call naming an infra directory as a plain token, but neither the call syntax nor the
        # infra token ever sits as one contiguous literal in THIS file's own source — the same
        # concatenation discipline test_scoped_reach_unnamed_file_falls_full uses above, kept
        # here for the opposite reason (so the token DOES appear as a scannable literal in the
        # fixture this test writes to disk, never in this file).
        call_name = "glob" + "." + "glob"
        dir_token = "guard" + "rails"
        synth_body = (
            "import glob\n"
            "import os\n\n"
            "def test_walks_infra_dir():\n"
            "    " + call_name + "(os.path.join(" + repr(dir_token) + ", " + repr("*.sh") + "))\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, synth_name), "w", encoding="utf-8") as f:
                f.write(synth_body)

            flagged = self._enumerating_infra_tests(tmpdir, infra_dirs)
            self.assertEqual(
                flagged, {synth_name},
                "the scanner must flag a synthetic test enumerating an infra dir",
            )

            unpinned = flagged - real_always_scoped
            self.assertEqual(
                unpinned, {synth_name},
                "an unpinned enumerating-infra test must read as a violation",
            )

            fabricated_always_scoped = {synth_name}
            closed = flagged - fabricated_always_scoped
            self.assertEqual(
                closed, set(),
                "pinning the synthetic file's name into ALWAYS_SCOPED must close the violation",
            )


class TestGateMachineryReach(unittest.TestCase):
    """Row 362 arm 2 (M-345): the gate-machinery classifier that decides whether the
    suite-in-suite meta-test (TestGateB_Tests' scratch runs) fires on this diff."""

    def test_meta_reach_fires_on_gate_machinery_diff(self):
        should_run, _reason = gate_machinery_diff(["guardrails/check-tests.sh"])
        self.assertTrue(should_run)

    def test_meta_reach_skips_off_class_with_named_reason(self):
        should_run, reason = gate_machinery_diff(["README.md", "docs/x.md"])
        self.assertFalse(should_run)
        self.assertIn("gate-machinery", reason)
        self.assertIn("INV-45", reason)

    def test_meta_reach_conservative_on_empty_diff(self):
        should_run, _reason = gate_machinery_diff([])
        self.assertTrue(should_run)


class TestPreShowLint(unittest.TestCase):
    """Row 170 (M-177, INV-28 mechanical arm): the pre-show lint catches a human-facing
    line that OPENS with an internal handle (a spec code or a row/session number) before
    the human sees it — the leak that put 'Rows 166 …' at the head of a chat report."""

    SCRIPT = os.path.join(ROOT, "scripts", "preshow-lint.py")

    def _lint(self, text):
        return subprocess.run(["python3", self.SCRIPT, "-"], input=text,
                              capture_output=True, text=True)

    def test_leading_handle_goes_red(self):
        for bad in ("Rows 166 and 148 await your word.",
                    "INV-70 landed and pushed.",
                    "- row 170 is the durable fix.",
                    "M-176 pins the test."):
            r = self._lint(bad)
            self.assertEqual(r.returncode, 1, "should flag a leading handle: %r" % bad)
            self.assertIn("leading-handle", r.stdout)

    def test_outcome_led_and_trailing_anchor_pass(self):
        for good in ("The live board is now just chat narration, no HTML (row 166).",
                     "A guard catches jargon before you see it (INV-28).",
                     "The feature map is readable on demand."):
            r = self._lint(good)
            self.assertEqual(r.returncode, 0,
                             "outcome-led / trailing-anchor text must pass: %r\n%s" % (good, r.stdout))


class TestSpecStyleLint(unittest.TestCase):
    """The mechanical arm of the SPEC prose register (docs/spec-style.md): the durable fix for the
    hand-rewrite drift that kept re-styling the spec into an ugly voice. It flags the register tells
    a reader caught late — a rule that defines by exclusion ('X does not become Y') before saying
    what it is, machine jargon, ALL-CAPS shout, the «X — not Y» scissors — so a section is driven to
    clean against a machine at any length, not against a human's patience."""

    SCRIPT = os.path.join(ROOT, "scripts", "spec-style-lint.py")

    def _lint(self, text):
        return subprocess.run(["python3", self.SCRIPT, "-"], input=text,
                              capture_output=True, text=True)

    def test_register_tells_go_red(self):
        cases = [
            ("Several open picks do not become a serialized questionnaire.", "negation-opener"),
            ("The map is not a separate document.", "negation-opener"),
            ("A wish carries a serialized questionnaire of open picks.", "machine-jargon"),
            ("The card shows the outcome — not the mechanism.", "scissors"),
        ]
        for text, code in cases:
            r = self._lint(text)
            self.assertEqual(r.returncode, 1, "should flag %s: %r\n%s" % (code, text, r.stdout))
            self.assertIn(code, r.stdout, "expected %s for %r\n%s" % (code, text, r.stdout))

    def test_legit_register_passes_clean(self):
        # a PROHIBITION ("does not ask" / "never re-carves") is correct register (R4), not a tell;
        # a noun-negative ("no design decision inside") and a fronted condition are fine too.
        for good in ("The walk does not ask how long a wish will take.",
                     "A restructure verdict never re-carves in passing.",
                     "Quick win: low effort, immediate value, no design decision inside.",
                     "When the classifier cannot call a size, it asks the human at intake.",
                     "Each question is a card, the recommended answer marked, with room to write a different one."):
            r = self._lint(good)
            self.assertEqual(r.returncode, 0,
                             "correct-register prose must pass clean: %r\n%s" % (good, r.stdout))

    def test_soft_signals_warn_but_do_not_fail(self):
        # caps-shout and second-person are advisory: printed, but exit 0 (they do not block a gate
        # the way an ERROR does — the whole un-converted spec still carries them).
        r = self._lint("You open the page and it CHANGES the queue.")
        self.assertEqual(r.returncode, 0, "warn-only text must exit 0\n%s" % r.stdout)
        self.assertIn("second-person", r.stdout)
        self.assertIn("caps-shout", r.stdout)

    def test_converted_intake_section_is_clean(self):
        # the calibration section is the standing gold: it must stay clean of register ERRORS, so a
        # regression in the linter OR in the section trips here. Re-aimed at the requirements format
        # (row 445): the old `#### Intake:` scenario became the intake work-kind requirement, and the
        # gold section is that requirement's own block.
        with open_spec() as f:
            spec = f.read()
        lines = spec.splitlines()
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("## Requirement") and "intake line names the work-kind" in l)
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
        section = "\n".join(lines[start:end])
        r = self._lint(section)
        self.assertEqual(r.returncode, 0,
                         "the converted intake section must stay register-clean:\n%s" % r.stdout)
