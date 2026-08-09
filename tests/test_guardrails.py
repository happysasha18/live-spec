"""Guardrails suite — the pack's own git-hook gates, mechanized (ROADMAP row 3).

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest -q tests

Asserts the SHIPPED guardrails/ scripts on disk, and exercises each gate's check
logic both against the real repo state (must be green today) and against scratch
fixtures (must fail the way the gate promises to fail).
"""

import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest

from conftest import ROOT
GUARDRAILS = os.path.join(ROOT, "guardrails")


def run(args, cwd=None, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        args, cwd=cwd or ROOT, capture_output=True, text=True, env=env
    )


GATE_MACHINERY_PREFIXES = (
    "guardrails/",
    "scaffold/guardrails/",
    "guardrails.config.json",
    ".github/workflows/",
    "tests/test_guardrails.py",
)


def gate_machinery_diff(files):
    """SPEC INV-45 / M-345 (row 362 arm 2): classifies whether a diff touches gate machinery —
    the class the suite-in-suite meta-test (TestGateB_Tests' scratch runs) exists to guard.
    Returns (should_run: bool, reason: str). An empty file list is CONSERVATIVE (should_run=True)
    — an unreadable diff must never silently skip the meta-test."""
    if not files:
        return True, "conservative: empty or unreadable diff — the meta-test runs by default"
    for f in files:
        for prefix in GATE_MACHINERY_PREFIXES:
            if f == prefix or f.startswith(prefix):
                return True, "gate-machinery diff: '%s' matches %s" % (f, prefix)
    return False, (
        "suite-in-suite meta-test: the diff touches no gate-machinery file (guardrails/, "
        "scaffold/guardrails/, guardrails.config.json, workflows, or this file) — skipped by "
        "reach, SPEC INV-45 / M-345"
    )


def machinery_digest(root=None):
    """Row 573 (the cost audit's repair a): one content hash over every gate-machinery file on
    disk — the same class GATE_MACHINERY_PREFIXES names. The digest moves the moment any byte
    of the machinery changes, however the change arrived: committed, staged, or loose."""
    import hashlib
    base = root or ROOT
    h = hashlib.sha256()
    rels = []
    for prefix in GATE_MACHINERY_PREFIXES:
        full = os.path.join(base, prefix)
        if os.path.isfile(full):
            rels.append(prefix)
        elif os.path.isdir(full):
            for dirpath, dirnames, filenames in os.walk(full):
                dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                for name in filenames:
                    rels.append(os.path.relpath(os.path.join(dirpath, name), base))
    for rel in sorted(rels):
        h.update(rel.encode("utf-8"))
        with open(os.path.join(base, rel), "rb") as f:
            h.update(f.read())
        h.update(b"\0")
    return h.hexdigest()


def _green_digest_store():
    override = os.environ.get("LIVE_SPEC_META_STORE")
    if override:
        return override
    return os.path.join(ROOT, ".live-spec", "checkpoints", "meta-suite-green.json")


def green_digest_matches(test_name, digest):
    """True when the stored last-green digest for this scratch test equals the current one —
    the machinery is byte-identical to a state this test already verified green, so the
    expensive scratch run proves nothing new and may skip. Missing or unreadable store is
    CONSERVATIVE: no match, the run fires."""
    try:
        with open(_green_digest_store(), encoding="utf-8") as f:
            stored = json.load(f)
    except (OSError, ValueError):
        return False
    return stored.get(test_name) == digest


def record_green_digest(test_name, digest):
    """After a green scratch run, remember the machinery digest it verified, so unchanged
    machinery stops paying the inner suite on every ordinary work run (row 573)."""
    store = _green_digest_store()
    try:
        with open(store, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    data[test_name] = digest
    os.makedirs(os.path.dirname(store), exist_ok=True)
    with open(store, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)


def _push_diff_files():
    """The files this push's diff touches: the committed delta against origin/main UNION the
    working tree's own uncommitted changes — so a meta-test decision made mid-session (before a
    commit) still sees the real footprint. META_REACH_FILES (newline-separated) overrides both
    for tests. Any git error returns [] — CONSERVATIVE, since gate_machinery_diff([]) always
    runs."""
    override = os.environ.get("META_REACH_FILES")
    if override is not None:
        return [f for f in override.split("\n") if f]
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            cwd=ROOT, capture_output=True, text=True,
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT, capture_output=True, text=True,
        )
        if diff.returncode != 0 or status.returncode != 0:
            return []
        files = set(f for f in diff.stdout.splitlines() if f)
        for line in status.stdout.splitlines():
            path = line[3:]  # porcelain: 2-char status + space, then the path
            if " -> " in path:  # a rename: "old -> new" — the new side is what's live now
                path = path.split(" -> ", 1)[1]
            if path:
                files.add(path)
        return sorted(files)
    except OSError:
        return []


class TestGuardrailFilesShip(unittest.TestCase):
    HOOKS = ("pre-commit", "pre-push")
    SCRIPTS = (
        "check-prover-record.sh",
        "check-tests.sh",
        "check-matrix-reference.py",
        "fence-refresh.sh",
        "install.sh",
        "check-shipped-language.sh",
    )

    def test_hooks_and_scripts_exist_and_executable(self):
        for name in self.HOOKS + self.SCRIPTS:
            path = os.path.join(GUARDRAILS, name)
            self.assertTrue(os.path.isfile(path), "missing guardrails file: %s" % name)
            mode = os.stat(path).st_mode
            self.assertTrue(mode & stat.S_IXUSR, "%s is not executable" % name)

    def test_readme_ships(self):
        path = os.path.join(GUARDRAILS, "README.md")
        self.assertTrue(os.path.isfile(path))
        self.assertGreater(os.path.getsize(path), 200, "README suspiciously small")

    def test_fence_ignored_by_git(self):
        gitignore = os.path.join(ROOT, ".gitignore")
        with open(gitignore, encoding="utf-8") as f:
            body = f.read()
        self.assertIn(".live-spec-fence", body)


class TestGateA_ProverRecord(unittest.TestCase):
    """Gate (a): a committed prover record dated today must exist."""

    def test_real_repo_passes(self):
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("real-repo state check — meaningless in a git-less scratch copy")
        result = run([os.path.join(GUARDRAILS, "check-prover-record.sh")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK (prover record)", result.stdout)

    def test_missing_record_fails(self):
        """Runs against its OWN scratch repo (not the real repo's cwd/HEAD): a spec
        change with no prover record at all must fail regardless of what the real
        repo's HEAD looks like on the day the suite runs (row 302 — a sibling test
        running in the real repo's cwd let the script's remote-deposit carve-out
        fire when the real HEAD happened to be an inbox-only commit, flipping this
        must-fail assertion)."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1 — a change with no prover record.\n")
            self._commit_all(tmp, "spec change, no prover record")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh")],
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL (prover record)", result.stdout)

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def _write(self, tmp, relpath, content):
        path = os.path.join(tmp, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _commit_all(self, tmp, msg):
        run(["git", "add", "-A"], cwd=tmp)
        run(["git", "commit", "-q", "-m", msg], cwd=tmp)

    def test_work_road_accepts_fresh_yesterday_record_and_push_road_refuses(self):
        """Row 571 (the cost audit's repair b): after midnight a clean tree is not a defect.
        The default WORK road accepts the newest committed record of any date while it stays
        fresh for the guarded documents; the --push road keeps demanding a record dated today
        (his recorded line: a full re-check before every push)."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            self._write(tmp, "docs/prover/2026-07-05-x.md", "prover record for v1\n")
            self._commit_all(tmp, "record for v1, after the spec change")
            script = os.path.join(GUARDRAILS, "check-prover-record.sh")
            work = run([script, "docs/prover", "2026-07-06"], cwd=tmp)
            self.assertEqual(work.returncode, 0, work.stdout + work.stderr)
            self.assertIn("work-run road", work.stdout)
            push = run([script, "--push", "docs/prover", "2026-07-06"], cwd=tmp)
            self.assertEqual(push.returncode, 1, push.stdout + push.stderr)
            self.assertIn("FAIL (prover record)", push.stdout)

    def test_stale_record_fails(self):
        """A record committed BEFORE the last PRODUCT_SPEC.md change is stale (row 61,
        SPEC M-6): the gate must refuse it even though it is dated today and
        committed — gate (a)'s original checks alone would wrongly pass this."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            self._write(tmp, "docs/prover/2026-07-05-x.md", "prover record for v1\n")
            self._commit_all(tmp, "record for v1")
            self._write(tmp, "PRODUCT_SPEC.md", "spec v2 — changed after the record\n")
            self._commit_all(tmp, "spec v2, no new record")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh"), "docs/prover", "2026-07-05"],
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("predates the last PRODUCT_SPEC.md change", result.stdout)

    def test_stale_when_architecture_changed_after_record(self):
        """A record committed BEFORE the last ARCHITECTURE.md change is stale too (INV-116,
        row 271): the architecture pass records beside the spec's and carries the spec's
        freshness rule, so the gate must refuse a record a later ARCHITECTURE.md change
        outdates, even though it is dated today and committed."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            self._write(tmp, "docs/prover/2026-07-05-x.md", "prover record for v1\n")
            self._commit_all(tmp, "record for v1")
            self._write(tmp, "ARCHITECTURE.md", "architecture v2 — changed after the record\n")
            self._commit_all(tmp, "architecture v2, no new record")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh"), "docs/prover", "2026-07-05"],
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL (prover record)", result.stdout)

    def test_record_with_spec_same_commit_passes(self):
        """A record committed in the SAME commit as the PRODUCT_SPEC.md change it
        covers is fresh, not stale — this is the normal push shape."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            self._write(tmp, "PRODUCT_SPEC.md", "spec v2\n")
            self._write(tmp, "docs/prover/2026-07-05-x.md", "prover record for v2\n")
            self._commit_all(tmp, "spec v2 + its record, same commit")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh"), "docs/prover", "2026-07-05"],
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inbox_only_push_carve_out_needs_no_record(self):
        """Row 269 (INV-112/M-6): a push whose diff is exactly one new inbox/ file owes
        no fresh prover record — the CI script must carry the same diff-scoped carve-out
        the spec gained, so an inbox deposit on a day with no committed record stays green."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            base = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self._write(tmp, "inbox/2026-07-12-from-track-coach-wish.md", "a new wish\n")
            self._commit_all(tmp, "inbox deposit")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh"), "docs/prover", "2026-07-05"],
                cwd=tmp,
                extra_env={"LIVE_SPEC_DIFF_BASE": base},
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("carve-out", result.stdout)

    def test_diff_beyond_one_inbox_file_still_needs_a_record(self):
        """The carve-out is diff-scoped: a push that touches anything beyond one new
        inbox/ file rides the full gate and still owes a fresh record (row 269)."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
            self._commit_all(tmp, "spec v1")
            base = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self._write(tmp, "inbox/2026-07-12-from-track-coach-wish.md", "a new wish\n")
            self._write(tmp, "PRODUCT_SPEC.md", "spec v2 — a real change\n")
            self._commit_all(tmp, "inbox deposit + a spec edit")
            result = run(
                [os.path.join(GUARDRAILS, "check-prover-record.sh"), "docs/prover", "2026-07-05"],
                cwd=tmp,
                extra_env={"LIVE_SPEC_DIFF_BASE": base},
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL (prover record)", result.stdout)


class TestGateB_Tests(unittest.TestCase):
    """Gate (b): the test suite must be green (also covers gate c, anchor ownership).

    Both checks here run against a SCRATCH COPY of the whole repo (test_traceability.py
    resolves its fixture paths — PRODUCT_SPEC.md, ARCHITECTURE.md, etc. — relative to the repo
    root, so a bare copy of tests/ alone would 404 on every one of them). The copy
    keeps test_guardrails.py — architecture pins and BUILT matrix rows now reference
    it, so a copy without it is not a green repo — and recursion is cut by an env
    guard instead: the inner run gets LIVE_SPEC_SCRATCH=1, under which these two
    scratch-suite tests skip themselves (one level of nesting, never a fork bomb).
    """

    def _scratch_tests_dir(self, tmp):
        dest = os.path.join(tmp, "repo")
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return os.path.join(dest, "tests")

    def _skip_if_inner(self):
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("inner scratch run — recursion guard")

    def _skip_unless_gate_machinery_diff(self):
        """Row 362 arm 2 (M-345): these two scratch runs re-run the WHOLE suite in a scratch
        copy — expensive — so they ride the reach map like the gate they guard: fire only when
        the diff touches gate machinery, skip under a named reason otherwise."""
        should_run, reason = gate_machinery_diff(_push_diff_files())
        if not should_run:
            self.skipTest(reason)

    def _skip_if_machinery_unchanged_since_green(self, test_name):
        """Row 573 (the cost audit's repair a): the diff-reach skip above cannot help while an
        unpushed gate-machinery commit sits in origin/main..HEAD — every ordinary work run all
        day re-paid the ~2-minute inner suite for the same unchanged bytes. So a green scratch
        run records the machinery's content digest, and the run skips while that digest stands.
        Conservative teeth kept: no recorded green, an unreadable store, or any changed
        machinery byte fires the run. Returns the current digest for the green recording."""
        digest = machinery_digest()
        if green_digest_matches(test_name, digest):
            self.skipTest(
                "suite-in-suite meta-test: gate machinery is byte-identical to the state this "
                "test last verified green (row 573) — skipped; any machinery edit re-fires it"
            )
        return digest

    def test_real_content_passes(self):
        self._skip_if_inner()
        self._skip_unless_gate_machinery_diff()
        digest = self._skip_if_machinery_unchanged_since_green("test_real_content_passes")
        with tempfile.TemporaryDirectory() as tmp:
            scratch_tests = self._scratch_tests_dir(tmp)
            result = run([os.path.join(GUARDRAILS, "check-tests.sh"), scratch_tests],
                         extra_env={"LIVE_SPEC_SCRATCH": "1"})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK (tests)", result.stdout)
        record_green_digest("test_real_content_passes", digest)

    def test_broken_suite_fails(self):
        self._skip_if_inner()
        self._skip_unless_gate_machinery_diff()
        digest = self._skip_if_machinery_unchanged_since_green("test_broken_suite_fails")
        with tempfile.TemporaryDirectory() as tmp:
            scratch_tests = self._scratch_tests_dir(tmp)
            target = os.path.join(scratch_tests, "test_traceability.py")
            with open(target, encoding="utf-8") as f:
                content = f.read()
            broken = content.replace(
                "self.assertGreater(len(raw), 40",
                "self.assertGreater(len(raw), 999999",
            )
            self.assertNotEqual(content, broken, "fixture edit did not match — test is stale")
            with open(target, "w", encoding="utf-8") as f:
                f.write(broken)
            result = run([os.path.join(GUARDRAILS, "check-tests.sh"), scratch_tests],
                         extra_env={"LIVE_SPEC_SCRATCH": "1"})
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL (tests)", result.stdout)
        record_green_digest("test_broken_suite_fails", digest)


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


class TestGateD_MatrixReference(unittest.TestCase):
    """Gate (d), row 477: the hand-walked coverage-validation checkbox gate retired, and gate d now
    runs the generated matrix-Reference gate (check-matrix-reference.py). The checkbox gate's own
    exercising tests retired with it; the reference gate is red-proven in tests/test_matrix_reference.py
    (gate d's registered red proof). Here we hold only the guardrails-level facts: the new gate passes
    the real matrix, and the retired script is no longer wired into the push gate."""

    def test_real_matrix_passes(self):
        result = run(["python3", os.path.join(GUARDRAILS, "check-matrix-reference.py"),
                      os.path.join(ROOT, "TEST_MATRIX.md")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("reach:", result.stdout)

    def test_missing_file_fails(self):
        result = run(["python3", os.path.join(GUARDRAILS, "check-matrix-reference.py"),
                      "/nonexistent/TEST_MATRIX.md"])
        self.assertEqual(result.returncode, 1)

    def test_retired_checkbox_gate_unwired(self):
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            body = f.read()
        self.assertNotIn("check-matrix-coverage.sh", body,
                         "the retired checkbox gate is still wired into pre-push")


class TestGateE_PrototypeFence(unittest.TestCase):
    """Gate (e): a PROD file must not reference into a fenced prototype/ home
    (SPEC INV-17) — the prototype fence catches structural wiring (a prod file
    naming a fenced file); narrative mentions (JOURNAL.md, docs/, etc.) are excluded.
    """

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def _write(self, tmp, relpath, content):
        path = os.path.join(tmp, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _commit_all(self, tmp):
        run(["git", "add", "-A"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "scratch"], cwd=tmp)

    def test_real_repo_passes(self):
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("real-repo state check — meaningless in a git-less scratch copy")
        result = run([os.path.join(GUARDRAILS, "check-prototype-fence.sh")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK (prototype fence)", result.stdout)

    def test_prod_reference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "prototype/sketch.html", "<html>sketch</html>\n")
            self._write(tmp, "index.html", '<script src="prototype/sketch.html"></script>\n')
            self._commit_all(tmp)
            result = run([os.path.join(GUARDRAILS, "check-prototype-fence.sh"), tmp])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL (prototype fence)", result.stdout)
            self.assertIn("index.html", result.stdout)
            self.assertIn("prototype/sketch.html", result.stdout)

    def test_narrative_mention_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "prototype/sketch.html", "<html>sketch</html>\n")
            self._write(tmp, "JOURNAL.md", "Tried prototype/sketch.html today, promising.\n")
            self._write(tmp, "docs/note.md", "See prototype/sketch.html for the sketch.\n")
            self._commit_all(tmp)
            result = run([os.path.join(GUARDRAILS, "check-prototype-fence.sh"), tmp])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK (prototype fence)", result.stdout)

    def test_empty_prototype_dir_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            os.makedirs(os.path.join(tmp, "prototype"), exist_ok=True)
            self._write(tmp, "readme.txt", "ordinary file, nothing fenced here.\n")
            self._commit_all(tmp)
            result = run([os.path.join(GUARDRAILS, "check-prototype-fence.sh"), tmp])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK (prototype fence)", result.stdout)


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


class TestPreCommitFence(unittest.TestCase):
    """Gate: the concurrent-edit fence (SPEC INV-11), opt-in via .live-spec-fence."""

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)
        hooks_dir = os.path.join(tmp, ".git", "hooks")
        for hook in ("pre-commit", "post-commit"):
            shutil.copy(os.path.join(GUARDRAILS, hook), os.path.join(hooks_dir, hook))
            os.chmod(os.path.join(hooks_dir, hook), 0o755)
        with open(os.path.join(tmp, "f.txt"), "w") as f:
            f.write("hi\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "init"], cwd=tmp)

    def _commit_more(self, tmp, msg, extra_env=None):
        with open(os.path.join(tmp, "f.txt"), "a") as f:
            f.write(msg + "\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        return run(["git", "commit", "-q", "-m", msg], cwd=tmp, extra_env=extra_env)

    def test_unarmed_fence_passes_silently(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            result = self._commit_more(tmp, "no fence")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_armed_matching_head_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            refresh = run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp)
            self.assertEqual(refresh.returncode, 0, refresh.stdout + refresh.stderr)
            self.assertTrue(os.path.isfile(os.path.join(tmp, ".live-spec-fence")))
            result = self._commit_more(tmp, "fenced, matches")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_armed_stale_head_blocks_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            with open(os.path.join(tmp, ".live-spec-fence"), "w") as f:
                f.write("0" * 40 + "\n")
            result = self._commit_more(tmp, "should be blocked")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("COMMIT BLOCKED", result.stdout + result.stderr)


class TestPostCommitFenceReArm(unittest.TestCase):
    """Gate: the fence re-arms on the session's OWN successful commit (ROADMAP row
    572) — a second commit in the same session never needs a manual
    guardrails/fence-refresh.sh, while a commit carrying a different session token
    (another window) still leaves the fence stale, so the next commit still blocks."""

    SESSION_A = {"LIVE_SPEC_SESSION_ID": "session-A-0001"}
    SESSION_B = {"LIVE_SPEC_SESSION_ID": "session-B-9999"}

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)
        hooks_dir = os.path.join(tmp, ".git", "hooks")
        for hook in ("pre-commit", "post-commit"):
            shutil.copy(os.path.join(GUARDRAILS, hook), os.path.join(hooks_dir, hook))
            os.chmod(os.path.join(hooks_dir, hook), 0o755)
        with open(os.path.join(tmp, "f.txt"), "w") as f:
            f.write("hi\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "init"], cwd=tmp)

    def _commit(self, tmp, msg, extra_env):
        with open(os.path.join(tmp, "f.txt"), "a") as f:
            f.write(msg + "\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        return run(["git", "commit", "-q", "-m", msg], cwd=tmp, extra_env=extra_env)

    def _fence_lines(self, tmp):
        with open(os.path.join(tmp, ".live-spec-fence")) as f:
            return [ln.strip() for ln in f.readlines()]

    def _commit_no_verify(self, tmp, msg, extra_env):
        with open(os.path.join(tmp, "f.txt"), "a") as f:
            f.write(msg + "\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        return run(["git", "commit", "-q", "--no-verify", "-m", msg], cwd=tmp,
                    extra_env=extra_env)

    def test_no_verify_commit_after_foreign_move_does_not_rearm(self):
        """Regression pin, adversarial review D1 (row 572): session A arms and
        commits; foreign session B commits first-through, leaving the fence stale;
        A then commits with --no-verify, which skips pre-commit entirely but still
        runs post-commit. Token matching alone used to re-arm the fence to a HEAD
        that CONTAINS B's commit, silently absorbing B's move. The fix requires
        this commit's own parent to equal the recorded sha before re-arming — since
        A's --no-verify commit's parent is B's commit, not the recorded sha, the
        fence must stay untouched, and A's next NORMAL commit must still block."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp, extra_env=self.SESSION_A)

            own = self._commit(tmp, "session A's own commit", self.SESSION_A)
            self.assertEqual(own.returncode, 0, own.stdout + own.stderr)
            fence_sha_after_own = self._fence_lines(tmp)[0]

            # Foreign session B commits first-through — allowed (first writer through
            # an armed-but-unmoved HEAD), but leaves the fence stale at A's sha.
            foreign = self._commit(tmp, "session B's foreign commit", self.SESSION_B)
            self.assertEqual(foreign.returncode, 0, foreign.stdout + foreign.stderr)
            self.assertEqual(self._fence_lines(tmp)[0], fence_sha_after_own)

            # Session A commits with --no-verify: pre-commit's staleness check is
            # skipped entirely, but post-commit still runs and A's token still
            # matches the recorded one. This is exactly the defect sequence.
            no_verify = self._commit_no_verify(tmp, "A's no-verify commit", self.SESSION_A)
            self.assertEqual(no_verify.returncode, 0, no_verify.stdout + no_verify.stderr)

            # The fence must still be stale at A's last honest commit — NOT re-armed
            # to a HEAD that contains B's commit.
            self.assertEqual(self._fence_lines(tmp)[0], fence_sha_after_own,
                              "post-commit must not re-arm across a foreign commit "
                              "just because a --no-verify commit's token matched")
            head_after_no_verify = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self.assertNotEqual(self._fence_lines(tmp)[0], head_after_no_verify)

            # A's next NORMAL commit (pre-commit runs) must now BLOCK — B's move was
            # never surfaced, so the fence must still catch it here.
            blocked = self._commit(tmp, "A tries a normal commit next", self.SESSION_A)
            self.assertEqual(blocked.returncode, 1, blocked.stdout + blocked.stderr)
            self.assertIn("COMMIT BLOCKED", blocked.stdout + blocked.stderr)

    def test_recorded_token_present_but_session_empty_at_commit_no_rearm(self):
        """R4 gap: the fence is armed WITH a real recorded token, but the commit
        happens with no session token available at all (plain shell, both env vars
        empty). post-commit must not re-arm — it exits at the empty-token guard
        before ever comparing tokens or parents."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp, extra_env=self.SESSION_A)
            fence_sha_after_arm = self._fence_lines(tmp)[0]

            no_token_env = {"LIVE_SPEC_SESSION_ID": "", "CLAUDE_CODE_SESSION_ID": ""}
            result = self._commit(tmp, "commit with no session token present", no_token_env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            # fence untouched: still recorded at the armed sha, not the new HEAD
            self.assertEqual(self._fence_lines(tmp)[0], fence_sha_after_arm)
            head_after = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self.assertNotEqual(self._fence_lines(tmp)[0], head_after)

            # so the very next commit blocks, even though it's session A trying again
            blocked = self._commit(tmp, "A tries again", self.SESSION_A)
            self.assertEqual(blocked.returncode, 1, blocked.stdout + blocked.stderr)
            self.assertIn("COMMIT BLOCKED", blocked.stdout + blocked.stderr)

    def test_same_session_two_commits_no_manual_refresh(self):
        """Deliverable 2a: one session lands two commits with no manual refresh."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            refresh = run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp,
                           extra_env=self.SESSION_A)
            self.assertEqual(refresh.returncode, 0, refresh.stdout + refresh.stderr)
            fence_after_arm = self._fence_lines(tmp)
            self.assertEqual(fence_after_arm[1], self.SESSION_A["LIVE_SPEC_SESSION_ID"])

            first = self._commit(tmp, "own commit 1", self.SESSION_A)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            # the fence's recorded sha must have moved to the new HEAD (re-armed)
            head_after_first = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self.assertEqual(self._fence_lines(tmp)[0], head_after_first)

            # the session's own SECOND commit — this is exactly what used to block
            # (row 572) demanding a manual guardrails/fence-refresh.sh
            second = self._commit(tmp, "own commit 2", self.SESSION_A)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertNotIn("COMMIT BLOCKED", second.stdout + second.stderr)

            third = self._commit(tmp, "own commit 3", self.SESSION_A)
            self.assertEqual(third.returncode, 0, third.stdout + third.stderr)

    def test_foreign_session_commit_still_blocks(self):
        """Deliverable 2b: a commit from another session/window still blocks the
        armed session's next commit — the re-arm must not fire for a foreign move."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp, extra_env=self.SESSION_A)

            own = self._commit(tmp, "session A's own commit", self.SESSION_A)
            self.assertEqual(own.returncode, 0, own.stdout + own.stderr)
            fence_sha_after_own = self._fence_lines(tmp)[0]

            # session B (another window) lands a commit in the same repo. Nothing has
            # diverged from B's own view yet (HEAD still matches the recorded sha), so
            # this first foreign commit is allowed through — same as any first writer
            # through an armed-but-unmoved HEAD. What matters is what happens next.
            foreign = self._commit(tmp, "session B's foreign commit", self.SESSION_B)
            self.assertEqual(foreign.returncode, 0, foreign.stdout + foreign.stderr)

            # the fence must NOT have been re-armed by the foreign session — it stays
            # stale at session A's last commit, not at session B's new HEAD.
            self.assertEqual(self._fence_lines(tmp)[0], fence_sha_after_own)
            head_after_foreign = run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()
            self.assertNotEqual(self._fence_lines(tmp)[0], head_after_foreign)

            # session A's next commit must now BLOCK: HEAD moved via a foreign commit
            # the fence never accounted for.
            blocked = self._commit(tmp, "session A tries again", self.SESSION_A)
            self.assertEqual(blocked.returncode, 1, blocked.stdout + blocked.stderr)
            self.assertIn("COMMIT BLOCKED", blocked.stdout + blocked.stderr)

    def test_no_session_token_never_auto_rearms(self):
        """No session token available (plain shell) — post-commit stays a no-op, the
        historical manual-refresh-only behavior, so a second commit still blocks."""
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            no_token_env = {"LIVE_SPEC_SESSION_ID": "", "CLAUDE_CODE_SESSION_ID": ""}
            refresh = run([os.path.join(GUARDRAILS, "fence-refresh.sh")], cwd=tmp,
                           extra_env=no_token_env)
            self.assertEqual(refresh.returncode, 0, refresh.stdout + refresh.stderr)

            first = self._commit(tmp, "no-token commit 1", no_token_env)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            second = self._commit(tmp, "no-token commit 2", no_token_env)
            self.assertEqual(second.returncode, 1, second.stdout + second.stderr)
            self.assertIn("COMMIT BLOCKED", second.stdout + second.stderr)


class TestFenceSessionTokenFallback(unittest.TestCase):
    """R4 gap: $LIVE_SPEC_SESSION_ID unset but $CLAUDE_CODE_SESSION_ID set — the
    fallback branch (fence-refresh.sh and post-commit both do
    "${LIVE_SPEC_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}") must arm AND re-arm on
    the CLAUDE_CODE_SESSION_ID value, not silently treat it as no-token."""

    CLAUDE_TOKEN = "claude-code-session-token-only"

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)
        hooks_dir = os.path.join(tmp, ".git", "hooks")
        for hook in ("pre-commit", "post-commit"):
            shutil.copy(os.path.join(GUARDRAILS, hook), os.path.join(hooks_dir, hook))
            os.chmod(os.path.join(hooks_dir, hook), 0o755)
        with open(os.path.join(tmp, "f.txt"), "w") as f:
            f.write("hi\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "init"], cwd=tmp)

    def _run_no_livespec_token(self, args, cwd):
        """Like the module-level run(), but explicitly ensures LIVE_SPEC_SESSION_ID
        is ABSENT (not merely empty) so only the CLAUDE_CODE_SESSION_ID fallback is
        exercised, regardless of what the ambient test environment carries."""
        env = dict(os.environ)
        env.pop("LIVE_SPEC_SESSION_ID", None)
        env["CLAUDE_CODE_SESSION_ID"] = self.CLAUDE_TOKEN
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)

    def _commit(self, tmp, msg):
        with open(os.path.join(tmp, "f.txt"), "a") as f:
            f.write(msg + "\n")
        self._run_no_livespec_token(["git", "add", "f.txt"], tmp)
        return self._run_no_livespec_token(["git", "commit", "-q", "-m", msg], tmp)

    def _fence_lines(self, tmp):
        with open(os.path.join(tmp, ".live-spec-fence")) as f:
            return [ln.strip() for ln in f.readlines()]

    def test_claude_code_session_id_fallback_arms_and_rearms(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            refresh = self._run_no_livespec_token(
                [os.path.join(GUARDRAILS, "fence-refresh.sh")], tmp)
            self.assertEqual(refresh.returncode, 0, refresh.stdout + refresh.stderr)
            # arm recorded the CLAUDE_CODE_SESSION_ID value as the token (line 2)
            self.assertEqual(self._fence_lines(tmp)[1], self.CLAUDE_TOKEN)

            first = self._commit(tmp, "fallback commit 1")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            head_after_first = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=tmp, capture_output=True, text=True
            ).stdout.strip()
            # re-armed to the new HEAD purely off the CLAUDE_CODE_SESSION_ID fallback
            self.assertEqual(self._fence_lines(tmp)[0], head_after_first)

            # a second commit under the same fallback token must not block
            second = self._commit(tmp, "fallback commit 2")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertNotIn("COMMIT BLOCKED", second.stdout + second.stderr)


class TestFenceCorruptedFile(unittest.TestCase):
    """R4 gap: a corrupted .live-spec-fence (garbage line 1, or extra lines) must
    fail CLOSED — pre-commit blocks rather than passing a malformed sha compare —
    and post-commit must never touch a fence it did not itself just re-arm cleanly
    (no commit succeeds here, so post-commit never even fires; this pins that the
    file is left byte-for-byte as written, not "fixed up" or cleared)."""

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)
        hooks_dir = os.path.join(tmp, ".git", "hooks")
        for hook in ("pre-commit", "post-commit"):
            shutil.copy(os.path.join(GUARDRAILS, hook), os.path.join(hooks_dir, hook))
            os.chmod(os.path.join(hooks_dir, hook), 0o755)
        with open(os.path.join(tmp, "f.txt"), "w") as f:
            f.write("hi\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "init"], cwd=tmp)

    def _try_commit(self, tmp, msg):
        with open(os.path.join(tmp, "f.txt"), "a") as f:
            f.write(msg + "\n")
        run(["git", "add", "f.txt"], cwd=tmp)
        return run(["git", "commit", "-q", "-m", msg], cwd=tmp)

    def test_one_line_garbage_fence_blocks_and_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            fence_path = os.path.join(tmp, ".live-spec-fence")
            garbage = "not-a-real-sha-at-all\n"
            with open(fence_path, "w") as f:
                f.write(garbage)

            result = self._try_commit(tmp, "should be blocked by garbage fence")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("COMMIT BLOCKED", result.stdout + result.stderr)

            with open(fence_path) as f:
                self.assertEqual(f.read(), garbage,
                                  "a blocked commit must leave the corrupted fence "
                                  "exactly as written, not rewrite or clear it")

    def test_three_line_fence_blocks_and_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            fence_path = os.path.join(tmp, ".live-spec-fence")
            garbage = "also-not-a-real-sha\nsome-token\nunexpected-third-line\n"
            with open(fence_path, "w") as f:
                f.write(garbage)

            result = self._try_commit(tmp, "should be blocked by 3-line fence")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("COMMIT BLOCKED", result.stdout + result.stderr)

            with open(fence_path) as f:
                self.assertEqual(f.read(), garbage,
                                  "a blocked commit must leave the corrupted fence "
                                  "exactly as written, not rewrite or clear it")


class TestInstallScript(unittest.TestCase):
    def test_install_copies_hooks_into_scratch_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            run(["git", "init", "-q"], cwd=tmp)
            scratch_guardrails = os.path.join(tmp, "guardrails")
            shutil.copytree(GUARDRAILS, scratch_guardrails)
            result = run(["./install.sh"], cwd=scratch_guardrails)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for hook in ("pre-commit", "pre-push", "post-commit"):
                dest = os.path.join(tmp, ".git", "hooks", hook)
                self.assertTrue(os.path.isfile(dest), "%s not installed" % hook)
                self.assertTrue(os.stat(dest).st_mode & stat.S_IXUSR)
            # idempotent: re-running does not error
            result2 = run(["./install.sh"], cwd=scratch_guardrails)
            self.assertEqual(result2.returncode, 0, result2.stdout + result2.stderr)
            # does not arm the fence
            self.assertFalse(os.path.isfile(os.path.join(tmp, ".live-spec-fence")))


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestGateF_SkillLoadability(unittest.TestCase):
    """Gate (f): every shipped skill LOADS — frontmatter parses, name matches its
    folder, description + metadata version present, a 'Work that belongs elsewhere' section
    scopes it negatively (row 80). Red-first proven on a broken scratch skill."""

    def test_real_repo_passes(self):
        result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"),
                      os.path.join(ROOT, "skills")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_broken_skill_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "broken")
            os.makedirs(bad)
            with open(os.path.join(bad, "SKILL.md"), "w") as f:
                f.write("---\nname: wrongname\n---\nno negative section\n")
            result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"), tmp])
            self.assertEqual(result.returncode, 1, "broken skill must turn the gate RED")
            self.assertIn("does not match its folder", result.stdout)
            self.assertIn("no 'Work that belongs elsewhere' section", result.stdout)

    def test_missing_skills_dir_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([os.path.join(GUARDRAILS, "check-skill-loadability.sh"), tmp])
            self.assertEqual(result.returncode, 1, "empty skills dir must fail, not pass silently")


class TestGateG_PinDrift(unittest.TestCase):
    """Gate (g): architecture pins must not rot (SPEC E-14, row 90) — file-missing or
    beyond-EOF is RED; label-not-near-line is reported drift (RED under --strict)."""

    def test_real_repo_passes(self):
        result = run([os.path.join(GUARDRAILS, "check-pin-drift.sh"),
                      os.path.join(ROOT, "ARCHITECTURE.md")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            arch = os.path.join(tmp, "ARCHITECTURE.md")
            with open(arch, "w") as f:
                f.write("### [node: n]\n\n**responsibility** — r\n\n**owns** — E-1\n\n"
                        "**pins** — `ghost.py:5` (spine)\n")
            result = run([os.path.join(GUARDRAILS, "check-pin-drift.sh"), arch])
            self.assertEqual(result.returncode, 1, "missing pinned file must be RED")
            self.assertIn("pinned file missing", result.stdout)

    def test_label_drift_strict_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "code.py")
            with open(target, "w") as f:
                f.write("\n" * 100)
            arch = os.path.join(tmp, "ARCHITECTURE.md")
            with open(arch, "w") as f:
                f.write("### [node: n]\n\n**responsibility** — r\n\n**owns** — E-1\n\n"
                        "**pins** — `code.py:50` (nonexistent-symbol)\n")
            soft = run([os.path.join(GUARDRAILS, "check-pin-drift.sh"), arch])
            self.assertEqual(soft.returncode, 0, "non-strict drift must report, not block")
            self.assertIn("DRIFT", soft.stdout)
            strict = run([os.path.join(GUARDRAILS, "check-pin-drift.sh"), arch, "--strict"])
            self.assertEqual(strict.returncode, 1, "strict drift must be RED")


class TestGateTimeFence(unittest.TestCase):
    """Row 104 (M-110, INV-24 second arm): an added line pairing today's date with a
    clock time later than the commit moment goes red at pre-commit."""

    def _run_check(self, line, today="2026-01-01", now="12:00"):
        import subprocess, tempfile, os
        script = os.path.join(ROOT, "guardrails", "check-future-times.sh")
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            p = os.path.join(d, "note.md")
            with open(p, "w") as f:
                f.write(line + "\n")
            subprocess.run(["git", "-C", d, "add", "note.md"], check=True)
            return subprocess.run(
                ["bash", script],
                cwd=d,
                env={**os.environ, "CHECK_TODAY": today, "CHECK_NOW": now},
                capture_output=True, text=True)

    def test_future_time_today_goes_red(self):
        r = self._run_check("landed 2026-01-01 13:00, session 99")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_past_time_today_stays_green(self):
        r = self._run_check("landed 2026-01-01 11:00, session 99")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_other_day_time_stays_green(self):
        r = self._run_check("landed 2025-12-31 13:00 (quoted past incident)")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_mixed_history_line_stays_green(self):
        """F9: a line mixing today's date with QUOTED times of other moments
        (a ledger occurrence list) is legal — only the ADJACENT stamp shape trips."""
        r = self._run_check(
            'occurrences: 2025-12-31 (stamps "23:50"/"23:58" corrected), '
            '2026-01-01 ~11:00 (fourth catch; the "13:40" quote stays legal)')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_adjacent_future_stamp_still_red_after_narrowing(self):
        r = self._run_check("queued 2026-01-01 ~13:05, session 99")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


class TestGateReachMap(unittest.TestCase):
    """Row 147 (M-142, INV-45): the reach map's deciding script — a prose-only diff
    stands the suite down; tested documents, unknown files, and empty diffs fall to
    FULL by construction."""

    SCRIPT = os.path.join(GUARDRAILS, "check-push-reach.sh")

    def reach(self, files):
        return run(["bash", self.SCRIPT], extra_env={"REACH_FILES": files})

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
                   extra_env={"REACH_FILES": files, "REACH_CONFIG": config_path})

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


class TestPytestFromRoot(unittest.TestCase):
    """Row 106 (M-143): a stranger's `python3 -m pytest` from the repo root must
    collect the real suite cleanly and never trip over the scaffold template."""

    def test_pytest_collects_clean_from_root(self):
        import sys
        r = run([sys.executable, "-m", "pytest", "--collect-only", "-q"], cwd=ROOT)
        self.assertEqual(r.returncode, 0, (r.stdout or "")[-2000:] + (r.stderr or "")[-2000:])
        self.assertNotIn("test_scaffold.template", r.stdout,
                         "the scaffold template must never be collected")


class TestGateHygieneContract(unittest.TestCase):
    """Row 114 (M-145, INV-47): the gate contract — a typed failure line on a
    blocking gate's red, a declared blocking/advisory taxonomy, all-or-nothing
    writes; the reach decider exempt by name."""

    def _init_repo(self, tmp):
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "a"], cwd=tmp)

    def _write(self, tmp, relpath, content):
        path = os.path.join(tmp, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _commit_all(self, tmp):
        run(["git", "add", "-A"], cwd=tmp)
        run(["git", "commit", "-q", "-m", "scratch"], cwd=tmp)

    def test_readme_states_contract(self):
        with open(os.path.join(GUARDRAILS, "README.md"), encoding="utf-8") as f:
            body = f.read()
        for needle in ('"severity"', "blocking or advisory", "before writing any",
                       "check-push-reach.sh", "INV-47"):
            self.assertIn(needle, body, "guardrails README missing: %s" % needle)

    def test_prototype_fence_emits_typed_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            self._write(tmp, "prototype/sketch.html", "<html>sketch</html>\n")
            self._write(tmp, "index.html", '<script src="prototype/sketch.html"></script>\n')
            self._commit_all(tmp)
            result = run([os.path.join(GUARDRAILS, "check-prototype-fence.sh"), tmp])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            json_line = None
            for line in result.stdout.splitlines():
                if line.startswith("{"):
                    json_line = line
                    break
            self.assertIsNotNone(json_line, "no typed JSON failure line found in: " + result.stdout)
            payload = json.loads(json_line)
            self.assertEqual(
                set(payload.keys()), {"severity", "code", "message", "fix"},
                "typed failure line has unexpected keys: %r" % (payload,)
            )
            self.assertEqual(payload["severity"], "error")
            self.assertEqual(payload["code"], "prototype-fence")


class TestCIMirror(unittest.TestCase):
    """Row 14 (M-154, SPEC M-5): the CI mirror ships — the same gate scripts as a
    second net; the reach map stays a local optimization."""

    def test_workflow_ships_and_mirrors_the_gates(self):
        path = os.path.join(ROOT, ".github", "workflows", "gates.yml")
        self.assertTrue(os.path.isfile(path), "gates.yml missing")
        with open(path, encoding="utf-8") as f:
            body = f.read()
        for needle in ("pytest", "check-prover-record.sh", "check-matrix-reference.py",
                       "check-pin-drift.sh", "check-skill-loadability.sh",
                       "check-prototype-fence.sh", "check-shipped-language.sh", "fetch-depth: 0"):
            self.assertIn(needle, body, "gates.yml missing: %s" % needle)

    def test_readme_carries_the_mirror_guidance(self):
        with open(os.path.join(GUARDRAILS, "README.md"), encoding="utf-8") as f:
            body = f.read()
        for needle in ("CI mirror", "second net", "never redefines"):
            self.assertIn(needle, body, "guardrails README missing: %s" % needle)

    def test_local_gate_uses_the_same_runner_as_ci(self):
        # M-5/M-154: the local net and the CI net must run the SAME test runner, or the local net
        # under-runs relative to the second net. check-tests.sh once used `unittest discover`, which
        # cannot collect the plain-function pytest-style tests (monkeypatch/tmp_path fixtures) and
        # false-greened while CI's pytest caught the failure. Both must invoke pytest.
        with open(os.path.join(GUARDRAILS, "check-tests.sh"), encoding="utf-8") as f:
            gate = f.read()
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            ci = f.read()
        self.assertIn("python3 -m pytest", gate,
                      "check-tests.sh must run pytest, the same runner as the CI mirror")
        self.assertNotIn("-m unittest", gate,
                         "check-tests.sh must not invoke unittest (it under-collects the suite)")
        self.assertIn("pytest", ci, "the CI mirror must run pytest")

    def test_machine_local_pins_skip_in_ci_only(self):
        """The CI net must not false-red on pins that live only on the author's
        machine (~/.claude/...), while the local run stays strict (row 14's first
        live CI run caught exactly this)."""
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("machine-local pin behaviour — meaningless in a git-less scratch copy")
        script = os.path.join(GUARDRAILS, "check-pin-drift.sh")
        in_ci = run([script], extra_env={"CI": "true", "HOME": "/nonexistent-ci-home"})
        self.assertEqual(in_ci.returncode, 0, in_ci.stdout + in_ci.stderr)
        self.assertIn("machine-local pin, absent in CI; skipped", in_ci.stdout)
        local = run([script], extra_env={"CI": "", "HOME": "/nonexistent-ci-home"})
        self.assertEqual(local.returncode, 1,
                         "outside CI a missing machine-local pin must stay a hard FAIL")


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
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            spec = f.read()
        lines = spec.splitlines()
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("## Requirement") and "intake line names the work-kind" in l)
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
        section = "\n".join(lines[start:end])
        r = self._lint(section)
        self.assertEqual(r.returncode, 0,
                         "the converted intake section must stay register-clean:\n%s" % r.stdout)


class TestGateShippedLanguage(unittest.TestCase):
    """The shipped-language gate (SPEC INV-120, ROADMAP row 275, matrix M-260): a shipped
    artifact carries no Cyrillic outside a deliberate user-language string, and no owner or
    personal name in a requirement's statement. Proven on fixtures here, and (row 279, adopt)
    wired into the pack's own pre-push hook and CI mirror so a new attribution in a shipped
    doc goes red."""

    ENGINE = os.path.join(ROOT, "scripts", "check-shipped-language.py")
    WRAPPER = os.path.join(GUARDRAILS, "check-shipped-language.sh")

    def _write(self, tmp, relpath, content):
        path = os.path.join(tmp, relpath)
        os.makedirs(os.path.dirname(path) or tmp, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_engine_and_wrapper_ship_executable(self):
        self.assertTrue(os.path.isfile(self.ENGINE), "missing engine: %s" % self.ENGINE)
        self.assertTrue(os.path.isfile(self.WRAPPER), "missing wrapper: %s" % self.WRAPPER)
        mode = os.stat(self.WRAPPER).st_mode
        self.assertTrue(mode & stat.S_IXUSR, "wrapper is not executable")

    def test_offence_fixture_fails_with_file_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "A clean English line.\n"
                "Alexander wants the card to open calm.\n"
                "Это требование написано по-русски.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("SKILL.md:2", result.stdout)
            self.assertIn("[owner-name]", result.stdout)
            self.assertIn("SKILL.md:3", result.stdout)
            self.assertIn("[cyrillic]", result.stdout)

    def test_clean_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "README.md",
                "This feature landed 2026-07-12 after review.\n"
                "It ships with no personal names and no untranslated text.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_deliberate_user_language_region_is_spared(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "Before the fence, clean English.\n"
                "```user\n"
                "Это пример пользовательского текста.\n"
                "```\n"
                "After the fence, clean English.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allowlisted_authorship_byline_is_spared(self):
        with tempfile.TemporaryDirectory() as tmp:
            allowlist_path = self._write(tmp, "allowlist.json",
                json.dumps({"authorship_globs": ["LICENSE"]}))
            license_path = self._write(tmp, "LICENSE",
                "Copyright (c) 2026 Alexander Abramovich\n")
            result = run(["python3", self.ENGINE, "--root", tmp,
                          "--allowlist", allowlist_path, license_path])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_gate_wired_into_pre_push_and_ci(self):
        """Row 279 (adopt): the shipped-language gate runs in the pack's own pre-push hook
        AND the CI mirror, the way the other guardrails run, so a new attribution in a
        shipped doc is blocked on both nets."""
        with open(os.path.join(GUARDRAILS, "pre-push"), encoding="utf-8") as f:
            pre_push = f.read()
        self.assertIn("check-shipped-language.sh", pre_push,
                      "pre-push does not wire the shipped-language gate")
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            gates = f.read()
        self.assertIn("check-shipped-language.sh", gates,
                      "gates.yml does not mirror the shipped-language gate")

    def test_gate_green_on_the_swept_tree(self):
        """Row 279 (adopt): after the attribution sweep the gate reports zero active
        offences over the pack's own real shipped set — the wiring runs clean, not red."""
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("real-tree offence count — meaningless in a git-less scratch copy")
        result = run(["python3", self.ENGINE, "--root", ROOT])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"offences":0', result.stdout.replace(" ", ""))

    def test_gate_reads_a_staged_file_and_leaves_the_rest_of_the_tree_alone(self):
        """The shipped set is the index. A file staged for this delivery is read before it is ever
        committed, and a file the person merely keeps in the tree — a local note, a vendored library —
        belongs to no delivery, so a blocking gate leaves it alone."""
        import subprocess as sp
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            sp.run(["git", "init", "-q", tmp], check=True)
            self._write(tmp, "shipped.py", "# clean english only\n")
            sp.run(["git", "-C", tmp, "add", "shipped.py"], check=True)
            sp.run(["git", "-C", tmp, "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "seed"], check=True)
            # a local file nobody staged: outside every delivery
            self._write(tmp, "local_note.py", '# \u0441\u0442\u0440\u043e\u043a\u0430 482\n')
            result = run(["python3", self.ENGINE, "--root", tmp])
            self.assertEqual(result.returncode, 0,
                             "an unstaged local file must stay outside the scan:\n" + result.stdout)
            # the same content, staged for this delivery: read now, one commit before it lands
            self._write(tmp, "fresh.py", '# \u0441\u0442\u0440\u043e\u043a\u0430 482\n')
            sp.run(["git", "-C", tmp, "add", "fresh.py"], check=True)
            result = run(["python3", self.ENGINE, "--root", tmp])
            self.assertNotEqual(result.returncode, 0,
                                "a staged shipped file's offence must red:\n" + result.stdout)
            self.assertIn("fresh.py", result.stdout)

    # --- ROADMAP 417: the owner-name arm inverts to a DECLARED ALPHABET read from data, so the
    # detector's own code names no person and covering a collaborator is one data line, not a code
    # edit. Every string it reds today still reds; the alphabet form is not four hardcoded spellings. ---

    def test_declared_alphabet_is_data_driven_not_hardcoded_in_code(self):
        # RED-FIRST against the pre-delta hardcoded regex: an out-of-alphabet name DECLARED in the
        # allowlist data (a collaborator, not the four hardcoded spellings) must red — which the old
        # code, ignoring the data, never did.
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allowlist.json", json.dumps({
                "declared_alphabet": {"out_of_alphabet_name_patterns": [r"\bBartholomew\b"]}}))
            doc = self._write(tmp, "SKILL.md",
                "A clean English line.\n"
                "Bartholomew asked for the calmer layout.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("SKILL.md:2", result.stdout)
            self.assertIn("[owner-name]", result.stdout)

    def test_detector_source_names_no_person(self):
        # the inversion's safety win: the shipped detector code carries no personal name — the alphabet
        # of out-of-alphabet names lives in the (excluded, dated-debt) allowlist data instead.
        with open(self.ENGINE, encoding="utf-8") as f:
            src = f.read()
        for spelling in ("Alexander", "Sasha", "Sashka", "Alexandr"):
            self.assertNotIn(spelling, src,
                             "detector source hardcodes a person's name: %r" % spelling)

    def test_owner_name_still_reds_under_the_alphabet_form(self):
        # the existing catch is not weakened: the owner's name, declared out-of-alphabet in the pack's
        # own allowlist, still reds through the default allowlist path.
        with tempfile.TemporaryDirectory() as tmp:
            doc = self._write(tmp, "SKILL.md",
                "A clean English line.\n"
                "Alexander wants the card to open calm.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, doc])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("[owner-name]", result.stdout)

    # --- INV-245: the project-name arm. A core spec names no foreign project and tells no dated
    # incident. Rides gate i's mechanism; the forbidden project names live as allowlist DATA under
    # `project_name_patterns`, so the detector's own source names no project. STRICT on PRODUCT_SPEC.md
    # and ARCHITECTURE.md (a bare project name, or one beside an ISO date, reds); on TEST_MATRIX.md a
    # dated-incident provenance turn reds while the fixture-ledger kind names and a test-function-name
    # substring are permitted. ---

    PROJECT_ALLOW = {"project_name_patterns": [r"\btrack-coach\b", r"\btlvphotos?\b", r"\bpromoter\b"]}

    def test_project_arm_reds_a_bare_project_name_in_a_core_spec(self):
        # RED-FIRST against the pre-arm engine: a bare foreign project name in PRODUCT_SPEC.md reds.
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "PRODUCT_SPEC.md",
                "The card opens calm.\n"
                "The lens grew from three items to six on track-coach evidence.\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("PRODUCT_SPEC.md:2", r.stdout)
            self.assertIn("[project-name]", r.stdout)

    def test_project_arm_greens_a_core_spec_stated_as_the_rule(self):
        # the reworded shape passes: the rule stated in plain present tense, no project name, no date.
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "PRODUCT_SPEC.md",
                "The card opens calm.\n"
                "The lens grew from three items to six because a mandate with no checking seam gets skipped.\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_project_arm_reds_a_project_name_beside_a_date_in_architecture(self):
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "ARCHITECTURE.md",
                "| node | a photo kind (tlvphotos) inspect-zoom miss 2026-07-16 | pin |\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("[project-name]", r.stdout)

    def test_matrix_permits_the_fixture_ledger_and_a_test_name(self):
        # TEST_MATRIX permits a bare kind-name in the fixture ledger (no adjacent date) and a
        # project-name substring of a test-function name (word-bounded, so it never matches).
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "TEST_MATRIX.md",
                "| M-1 | red-proven against three real hosts as fixtures — a code kind (track-coach), "
                "a photo kind (tlvphotos), a prose kind | INV-1 | string | `test_promoter_harvest_trio` | BUILT |\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_matrix_reds_a_dated_incident(self):
        # RED-FIRST: a dated-incident provenance turn (a project name beside an ISO date) reds in the
        # matrix even though a bare fixture-ledger name does not.
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "TEST_MATRIX.md",
                "| M-2 | the reversibility half, tlvphotos openable-face miss 2026-07-14 | INV-1 | "
                "string | `test_x` | BUILT |\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("[project-name]", r.stdout)

    def test_project_arm_inert_outside_the_core_specs(self):
        # the arm is scoped to the three core specs: a skill card naming a project (an example) does not
        # red under the project arm — that surface is the shipped-language name/Cyrillic arms' domain.
        with tempfile.TemporaryDirectory() as tmp:
            allow = self._write(tmp, "allow.json", json.dumps(self.PROJECT_ALLOW))
            doc = self._write(tmp, "SKILL.md", "The track-coach widget is the code-kind example.\n")
            r = run(["python3", self.ENGINE, "--root", tmp, "--allowlist", allow, doc])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_detector_source_names_no_project(self):
        # the arm's safety win, mirroring the owner-name arm: the shipped detector code carries no
        # foreign project name — the forbidden names live in the (excluded, dated-debt) allowlist data.
        with open(self.ENGINE, encoding="utf-8") as f:
            src = f.read()
        for name in ("track-coach", "tlvphotos", "tlvphoto", "promoter"):
            self.assertNotIn(name, src,
                             "detector source hardcodes a project name: %r" % name)

    # --- USER_REGION_MARK anchoring (commit 91ab6aa widened the marker untested and over-cleared):
    # the comment opener must follow start-of-line or whitespace, so a URL fragment or a bare path
    # cannot masquerade as a real trailing comment. ---

    def test_inline_marker_clears_cyrillic_for_every_opener_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "Привет # user-language\n"
                "Привет <!-- user-language -->\n"
                "Привет /* user-language */\n"
                "Привет // user-language\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_url_fragment_does_not_masquerade_as_the_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "see https://user-language.example.com — Привет\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("[cyrillic]", result.stdout)

    def test_bare_path_does_not_masquerade_as_the_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "docs//user-language.md — Привет\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("[cyrillic]", result.stdout)

    def test_bare_cyrillic_with_no_marker_still_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "SKILL.md",
                "Это требование написано по-русски.\n")
            result = run(["python3", self.ENGINE, "--root", tmp, path])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("[cyrillic]", result.stdout)


class TestScopedReachDeletedFile(unittest.TestCase):
    """Audit fold (2.3.0 audit, finding 6): a deleted test file in the diff must never be handed to
    pytest as its own owner — a nonexistent path reds collection, a false red. It falls through to
    by-name discovery and, unowned, to FULL (conservative)."""

    SCRIPT = os.path.join(GUARDRAILS, "check-push-reach.sh")

    def test_scoped_reach_deleted_test_file_falls_full(self):
        # the fixture name is assembled at runtime so no test file carries it literally — a
        # by-content grep must find NO owner for a genuinely deleted, unreferenced test file
        ghost = "tests/test_zz_" + "deleted_nonexistent.py"
        r = run(["bash", self.SCRIPT], extra_env={"REACH_FILES": ghost})
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertNotIn("SCOPED " + ghost, r.stdout)
