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

    @staticmethod
    def _scratch_ignore(directory, names):
        """What the scratch copy leaves behind: caches, and the pack's own repository.

        Any OTHER repository installed inside the tree — an external skill, product-prover
        today — travels into the copy WHOLE, its `.git` included. That marker is what every
        fence in the pack reads to tell an installed clone from a shipped skill (see
        tests/test_skill_count_agrees.py::is_external_skill, install.sh, scripts/sync-skills.sh),
        so carrying it makes the copy read exactly as the real tree does: the clone stays
        external, stays out of the skill count and out of the one-version law, and its body is
        present for the tests that prove the canon.

        Leaving the clone behind instead (the shape shipped in 4e8df4c) kept those two laws
        green but cost the body. Locally the clone-dependent tests then skip and nothing shows;
        on CI, where GITHUB_ACTIONS reaches the inner run, they are written to FAIL on a missing
        clone rather than skip silently — dozens of inner failures, gate b red, CI red, and no
        local run without the CI variables can see it. Copying the clone whole answers both:
        the marker is there for the fences, the body is there for the proofs.

        Excluded, as before: the pack's own root `.git` — the copy is deliberately git-less, and
        several checks skip themselves by that name — and `__pycache__` anywhere.
        """
        ignored = {n for n in names if n == "__pycache__"}
        if os.path.realpath(directory) == os.path.realpath(ROOT):
            ignored.update(n for n in names if n == ".git")
        return ignored

    def _scratch_tests_dir(self, tmp):
        dest = os.path.join(tmp, "repo")
        shutil.copytree(ROOT, dest, ignore=self._scratch_ignore)
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


class TestGateG_PinDrift(unittest.TestCase):
    """Gate (g): architecture pins must not rot (SPEC E-14, row 90, row 541) — file-missing,
    beyond-EOF, and a label the target line does not carry are all RED, with no --strict to
    opt into. A line pin is proved against its own line within ±2 lines, by the label's
    NAMING words: document furniture ("rule", "line", "table") does not count while the label
    carries a word that names something, and counts only for a label that has nothing else.
    A `:1` file-level pin is proved against the whole file, and an unlabelled pin by the
    file's existence, named on the green line."""

    SCRIPT = os.path.join(GUARDRAILS, "check-pin-drift.sh")

    def _arch(self, tmp, pin_line):
        """An ARCHITECTURE.md holding one node with one pin."""
        arch = os.path.join(tmp, "ARCHITECTURE.md")
        with open(arch, "w") as f:
            f.write("### [node: n]\n\n**responsibility** — r\n\n**owns** — E-1\n\n"
                    "**pins** — %s\n" % pin_line)
        return arch

    def _rulebook(self, tmp):
        """A skill body shaped like the pack's own: rule 19 opens twenty lines above rule 20,
        the shape the 2026-08-05 prover pass caught (a pin labelled rule 20 sitting on rule
        19's opening line, green under the old 51-line window)."""
        target = os.path.join(tmp, "RULES.md")
        body = ["# The shared rules", ""]
        body.append("19. **The problem ledger — workshop noise is owned.** Operational noise is")
        body += ["    written down the moment it fires and never re-suffered." for _ in range(19)]
        body.append("20. **Search for a skill before reinventing.** At a project's setup, scan the")
        body.append("    installed skills and the catalogs you can reach.")
        with open(target, "w") as f:
            f.write("\n".join(body) + "\n")
        return body.index("20. **Search for a skill before reinventing.** At a project's setup, scan the") + 1

    def test_real_repo_passes(self):
        result = run([self.SCRIPT, os.path.join(ROOT, "ARCHITECTURE.md")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_green_line_names_the_files_it_read(self):
        """Row 541's third clause: the reach line names the files the gate opened."""
        result = run([self.SCRIPT, os.path.join(ROOT, "ARCHITECTURE.md")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("reach: files=[", result.stdout)
        self.assertIn("ARCHITECTURE.md", result.stdout)
        self.assertIn("skills/live-spec-base/SKILL.md", result.stdout)
        self.assertIn("guardrails/pre-push", result.stdout)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            arch = self._arch(tmp, "`ghost.py:5` (spine)")
            result = run([self.SCRIPT, arch])
            self.assertEqual(result.returncode, 1, "missing pinned file must be RED")
            self.assertIn("pinned file missing", result.stdout)

    def test_label_on_a_neighbouring_rules_line_reds(self):
        """THE recorded failure class (ROADMAP row 541, prover record F4, 2026-08-05): a pin
        labelled rule 20 landed on rule 19's opening line and read clean, because the old matcher
        accepted the generic word "rule", which stands in every window of a rulebook. The label's
        naming words — skill, search, setup, INV-65 — are what must stand on the pinned line."""
        with tempfile.TemporaryDirectory() as tmp:
            self._rulebook(tmp)
            arch = self._arch(tmp, "`RULES.md:3` (rule 20, INV-65 — skill search at setup)")
            result = run([self.SCRIPT, arch])
            self.assertEqual(result.returncode, 1,
                             "a pin labelled rule 20 sitting on rule 19's line must be RED:\n"
                             + result.stdout)
            self.assertIn("RULES.md:3", result.stdout)
            self.assertIn("no naming word", result.stdout)
            self.assertIn("looked for [", result.stdout)
            self.assertIn("line 3 reads:", result.stdout)

    def test_a_fabricated_label_on_the_right_rule_reds(self):
        """The probe the review asked for: a label naming something the pack never wrote, on the
        line of the rule it cites. The generic word "rule" holds no evidence, so the pin reds even
        though it sits on rule 20's own line."""
        with tempfile.TemporaryDirectory() as tmp:
            line = self._rulebook(tmp)
            arch = self._arch(tmp, "`RULES.md:%d` (rule 20 — the totally-invented-thing)" % line)
            result = run([self.SCRIPT, arch])
            self.assertEqual(result.returncode, 1,
                             "a fabricated label must red on the right line too:\n" + result.stdout)
            self.assertIn("totally-invented-thing", result.stdout)

    def test_a_pin_on_its_own_rules_line_passes(self):
        """The same fixture, pointed at rule 20's own line: green — the gate judges the pin, not
        the file, so the red above is not an always-red."""
        with tempfile.TemporaryDirectory() as tmp:
            line = self._rulebook(tmp)
            arch = self._arch(tmp, "`RULES.md:%d` (rule 20, INV-65 — skill search at setup)" % line)
            result = run([self.SCRIPT, arch])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_a_label_word_seventy_lines_away_reds(self):
        """Row 541's other sentence: a pin pointing seventy lines from its sentence read clean
        under the old window. The tolerance is now ±2 lines, and it is stated in the green line."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "code.py")
            with open(target, "w") as f:
                f.write("\n".join(["# filler"] * 70 + ["def render_widget():", "    pass"]) + "\n")
            arch = self._arch(tmp, "`code.py:2` (render_widget)")
            far = run([self.SCRIPT, arch])
            self.assertEqual(far.returncode, 1,
                             "a label seventy lines from the pinned line must be RED:\n" + far.stdout)
            near = run([self.SCRIPT, self._arch(tmp, "`code.py:71` (render_widget)")])
            self.assertEqual(near.returncode, 0, near.stdout + near.stderr)

    def test_a_label_the_line_does_not_carry_reds_with_no_strict_flag(self):
        """The old gate reported a label miss as advisory DRIFT unless --strict was passed, and
        the push chain passed no --strict — which is how 29 stale pins crossed a green gate."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "code.py")
            with open(target, "w") as f:
                f.write("\n" * 100)
            arch = self._arch(tmp, "`code.py:50` (nonexistent-symbol)")
            plain = run([self.SCRIPT, arch])
            self.assertEqual(plain.returncode, 1, "a label miss is RED with no flag to pass")
            self.assertIn("nonexistent-symbol", plain.stdout)
            strict = run([self.SCRIPT, arch, "--strict"])
            self.assertEqual(strict.returncode, 1, "--strict is still accepted and still RED")
            self.assertIn("the flag changes nothing", strict.stdout)

    def test_a_file_level_pin_is_proved_against_the_whole_file(self):
        """A `:1` pin names the file — line 1 is a shebang or a brace — so its label is proved
        against the whole file, and a label the file never carries still reds."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "installer.sh")
            with open(target, "w") as f:
                f.write("#!/usr/bin/env bash\n" + "echo filler\n" * 40 +
                        "# the ratchet seeding step\n")
            ok = run([self.SCRIPT, self._arch(tmp, "`installer.sh:1` (the ratchet seeding)")])
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            bad = run([self.SCRIPT, self._arch(tmp, "`installer.sh:1` (the telemetry uploader)")])
            self.assertEqual(bad.returncode, 1, "a label the file never carries must be RED")
            self.assertIn("no naming word", bad.stdout)

    def test_a_sub_item_label_is_judged_by_its_own_words(self):
        """A pin naming a sub-item inside a rule ("rule 7's worker-restore sub-rule") points at
        the sub-item's line, and its naming words — worker, restore, INV-298 — are found there,
        while the generic "rule" carries no weight either way."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "RULES.md")
            with open(target, "w") as f:
                f.write("# The shared rules\n\n7. **The concurrent-edit fence.**\n"
                        + "   - filler\n" * 20 +
                        "   - **A worker never restores a working tree with a git command.**\n")
            arch = self._arch(tmp, "`RULES.md:24` (rule 7's worker-restore sub-rule, INV-298)")
            result = run([self.SCRIPT, arch])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            drifted = self._arch(tmp, "`RULES.md:3` (rule 7's worker-restore sub-rule, INV-298)")
            self.assertEqual(run([self.SCRIPT, drifted]).returncode, 1,
                             "the same label on rule 7's opening line carries no evidence")

    def test_a_label_of_generic_words_alone_is_proved_by_them(self):
        """"gates" and "the rules" name nothing beyond the furniture, so the furniture is what
        proves them — a label with nothing else to give is still judged by what it has."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "SKILL.md")
            with open(target, "w") as f:
                f.write("# A skill\n\n" + "prose line\n" * 30 + "## Gates worth remembering\n"
                        + "prose line\n" * 5)
            ok = run([self.SCRIPT, self._arch(tmp, "`SKILL.md:33` (gates)")])
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            bad = run([self.SCRIPT, self._arch(tmp, "`SKILL.md:10` (gates)")])
            self.assertEqual(bad.returncode, 1, "the same one-word label elsewhere must be RED")

    def _assert_counts_close(self, result):
        m = re.search(r"OK \(pin drift\): (\d+) pin\(s\) checked — (\d+) line pin\(s\).*?"
                      r"(\d+) file-level :1 pin\(s\).*?(\d+) unlabelled pin\(s\)"
                      r" proved by the file's existence alone: (.+?)\.\n", result.stdout, re.S)
        self.assertIsNotNone(m, "the green line must state its four counts:\n" + result.stdout)
        total, line_pins, file_pins, bare, names = m.groups()
        self.assertEqual(int(total), int(line_pins) + int(file_pins) + int(bare),
                         "the three kinds must account for every pin checked")
        self.assertEqual(int(bare), len([n for n in names.split(",") if n.strip()]),
                         "every unlabelled pin is named: " + names)
        return int(total)

    def test_the_green_line_accounts_for_every_pin(self):
        """The counts close: line pins + file-level pins + unlabelled pins = pins checked, and the
        unlabelled ones — proved by existence alone — are named rather than folded in silently."""
        result = run([self.SCRIPT, os.path.join(ROOT, "ARCHITECTURE.md")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self._assert_counts_close(result)

    def test_the_counts_close_in_ci_too_with_a_pin_skipped(self):
        """The second net (SPEC M-5) skips a machine-local pin, so that pin stands outside the
        count as well as outside the buckets — it is named by the note line instead. A pin counted
        and bucketed nowhere would red CI after a green local push."""
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("machine-local pin behaviour — meaningless in a git-less scratch copy")
        local = run([self.SCRIPT], extra_env={"CI": "", "HOME": os.path.expanduser("~")})
        self.assertEqual(local.returncode, 0, local.stdout + local.stderr)
        in_ci = run([self.SCRIPT], extra_env={"CI": "true", "HOME": "/nonexistent-ci-home"})
        self.assertEqual(in_ci.returncode, 0, in_ci.stdout + in_ci.stderr)
        self.assertIn("machine-local pin, absent in CI; skipped", in_ci.stdout)
        self.assertEqual(self._assert_counts_close(in_ci) + 1, self._assert_counts_close(local),
                         "the skipped pin leaves the count, and only that pin")


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
