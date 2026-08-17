"""The lane's branch-and-merge road (SPEC E-34, T-23, INV-198..201; ROADMAP rows 386, 412).

A lane's isolated copy is a git worktree holding a branch of its own, cut from the claim
commit on main, penless while it rolls, landed by fast-forward from a rebased branch, and
torn down at its landing.

Two kinds of fact live here and they get two honest treatments.

The document law — the branch's name, the walk's order, the pen's reach, the vendored line —
is a string assertion against the shipped spec, live-spec's own rendered rung.

The road's central claim is a different animal: INV-198 says git ITSELF refuses another
worktree's attempt to move a branch a tree holds checked out, which is why "holding the pen
is the sole right to move main" needs no gate the pack writes. That claim is about a real
engine's runtime behaviour, and no string assertion against a shipped file can see it — the
spec's sentence would read exactly the same on the day git stopped refusing. So those rows
are proven by deed on a real two-worktree repo built in the system temp home (SPEC INV-100:
the suite's own prefix, erased at teardown), and the probe is hermetic — the user's global
and system git config are switched off, so the run reads git's defaults rather than this
machine's habits (SPEC INV-155).

The boundary is pinned beside the guarantee on purpose. Git's refusal covers the three
porcelain roads an agent walks by habit and leaves named doors open, and a suite that pinned
only the happy three would certify a guarantee wider than the one git actually gives.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT, read_all_flat, read_flat


def _robust_rmtree(path):
    """Remove a temp probe tree that holds a real git worktree, so a lane probe never leaks a
    `livespec-test-*` directory (SPEC INV-100). A plain rmtree can leave a read-only git object or a
    worktree admin file behind on some runners; this chmods each stubborn entry writable and retries,
    then makes a final ignore-errors sweep, so the tree is gone whatever the run's timing."""
    import stat

    def _onerror(func, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except OSError:
            pass

    shutil.rmtree(path, onerror=_onerror)
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def _git(cwd, *args):
    """Run git hermetically: the machine's own global/system config never speaks here."""
    env = dict(os.environ)
    env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_AUTHOR_NAME": "livespec-test",
        "GIT_AUTHOR_EMAIL": "livespec-test@example.invalid",
        "GIT_COMMITTER_NAME": "livespec-test",
        "GIT_COMMITTER_EMAIL": "livespec-test@example.invalid",
        "GIT_TERMINAL_PROMPT": "0",
    })
    proc = subprocess.run(("git",) + args, cwd=cwd, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


class _ProbeRepo(unittest.TestCase):
    """A real repo in two worktrees: the primary tree holds main, a lane worktree holds lane/x.

    This is the shape INV-198 legislates, so every deed below runs against the real thing.
    setUp asserts the probe IS that shape before any test reads it — a probe that quietly
    failed to build would hand every assertion below a vacuous pass (ROADMAP row 384).
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="livespec-test-lane-")
        self.addCleanup(_robust_rmtree, self.tmp)
        self.main_tree = os.path.join(self.tmp, "primary")
        self.lane_tree = os.path.join(self.tmp, "lane")
        os.makedirs(self.main_tree)
        self.run_ok(self.main_tree, "init", "-q", "-b", "main")
        self.commit(self.main_tree, "f", "one\n", "one")
        self.run_ok(self.main_tree, "worktree", "add", "-q", self.lane_tree, "-b", "lane/x")
        self.commit(self.lane_tree, "g", "two\n", "two")

        self.lane_sha = self.rev("HEAD", self.lane_tree)
        self.main_sha = self.rev("main", self.lane_tree)
        self.assertNotEqual(self.lane_sha, self.main_sha,
                            "probe did not build: the lane never diverged from main")
        _, listing = _git(self.lane_tree, "worktree", "list")
        self.assertIn("[main]", listing,
                      "probe did not build: no tree holds main, which is the very condition "
                      "INV-198's guarantee rests on")
        _, status = _git(self.main_tree, "status", "--short")
        self.assertEqual(status.strip(), "",
                         "probe did not build: the primary tree is dirty before any test ran")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_ok(self, cwd, *args):
        rc, out = _git(cwd, *args)
        self.assertEqual(rc, 0, "probe setup failed: git %s -> %s" % (" ".join(args), out))
        return out

    def commit(self, tree, name, body, message):
        with open(os.path.join(tree, name), "w", encoding="utf-8") as fh:
            fh.write(body)
        self.run_ok(tree, "add", name)
        self.run_ok(tree, "commit", "-qm", message)

    def rev(self, ref, cwd=None):
        rc, out = _git(cwd or self.lane_tree, "rev-parse", ref)
        self.assertEqual(rc, 0, "rev-parse %s: %s" % (ref, out))
        return out.strip()


class TestGitRefusesAnotherWorktreeMovingMain(_ProbeRepo):
    """M-373 (INV-198), by deed: the pen's central clause, enforced by the tool itself.

    Verified on a probe repo 2026-07-17, and re-verified here at every run — because this is
    the one fact the road leans on that no document can hold up.
    """

    def test_checkout_of_a_checked_out_main_is_refused_by_name(self):
        rc, out = _git(self.lane_tree, "checkout", "main")
        self.assertNotEqual(rc, 0, "the lane checked out main while the primary tree held it")
        self.assertIn("already used by worktree", out,
                      "git refused for some other reason than the worktree holding main: %s" % out)
        self.assertEqual(self.rev("HEAD"), self.lane_sha, "the lane's HEAD moved off its own branch")

    def test_force_update_of_a_checked_out_main_is_refused_by_name(self):
        rc, out = _git(self.lane_tree, "branch", "-f", "main", self.lane_sha)
        self.assertNotEqual(rc, 0, "the lane force-moved main while the primary tree held it")
        self.assertIn("cannot force update the branch", out,
                      "git refused for some other reason: %s" % out)
        self.assertEqual(self.rev("main"), self.main_sha, "main moved under the primary tree")

    def test_push_to_a_checked_out_main_is_refused_by_name(self):
        rc, out = _git(self.lane_tree, "push", ".", "HEAD:main")
        self.assertNotEqual(rc, 0, "the lane pushed to main while the primary tree held it")
        self.assertIn("refusing to update checked out branch", out,
                      "git refused for some other reason: %s" % out)
        self.assertEqual(self.rev("main"), self.main_sha, "main moved under the primary tree")

    def test_the_push_refusal_is_not_bought_off_with_force(self):
        """--force is the first thing a stuck agent reaches for, so the refusal is pinned against it."""
        rc, out = _git(self.lane_tree, "push", "--force", ".", "HEAD:main")
        self.assertNotEqual(rc, 0, "--force bought off the refusal")
        self.assertIn("refusing to update checked out branch", out)
        self.assertEqual(self.rev("main"), self.main_sha, "main moved under the primary tree")


class TestTheRefusalsBoundary(_ProbeRepo):
    """M-374 (INV-198), by deed: where the tool's guarantee stops.

    INV-198 names the guarantee's condition — the primary tree holds main — and marks the
    config-health check that asserts it [target]. These deeds are why that check is owed, and
    they pin the doors git leaves open, so the road never reads as wider than the tool it rests on.
    Each of these going red would be good news: it would mean git closed a door and the law can grow.
    """

    def test_the_refusals_lapse_when_no_tree_holds_main(self):
        self.run_ok(self.main_tree, "checkout", "-q", "--detach", "HEAD")
        rc, out = _git(self.lane_tree, "branch", "-f", "main", self.lane_sha)
        self.assertEqual(rc, 0, "git kept refusing though no tree held main: %s" % out)
        self.assertEqual(self.rev("main"), self.lane_sha,
                         "main did not move once no tree held it — INV-198's guarantee would not "
                         "rest on the primary tree holding main, and its config-health check "
                         "would be moot")

    def test_update_ref_walks_past_every_refusal(self):
        """git's plumbing carries no worktree check at all, and plumbing is what a script reaches for."""
        rc, out = _git(self.lane_tree, "update-ref", "refs/heads/main", self.lane_sha)
        self.assertEqual(rc, 0, "update-ref failed for an unrelated reason: %s" % out)
        self.assertEqual(self.rev("main"), self.lane_sha,
                         "update-ref no longer moves a checked-out main — git closed the door and "
                         "INV-198's guarantee is wider than it was when this was written")

    def test_update_ref_leaves_the_primary_tree_inconsistent(self):
        """The damage the porcelain refusals name in their own error text, done silently."""
        self.run_ok(self.lane_tree, "update-ref", "refs/heads/main", self.lane_sha)
        _, status = _git(self.main_tree, "status", "--short")
        self.assertNotEqual(status.strip(), "",
                            "the primary tree read clean after its branch moved under it")

    def test_the_checkout_refusal_carries_a_documented_override_flag(self):
        rc, out = _git(self.lane_tree, "checkout", "--ignore-other-worktrees", "main")
        self.assertEqual(rc, 0, "--ignore-other-worktrees no longer overrides the refusal: %s" % out)

    def test_the_push_refusal_is_a_config_default_rather_than_a_law(self):
        self.run_ok(self.main_tree, "config", "receive.denyCurrentBranch", "ignore")
        rc, out = _git(self.lane_tree, "push", ".", "HEAD:main")
        self.assertEqual(rc, 0, "the push stayed refused under denyCurrentBranch=ignore: %s" % out)
        self.assertEqual(self.rev("main"), self.lane_sha,
                         "main did not move though the config said to allow it")


class TestLaneIntegrationMechanics(_ProbeRepo):
    """M-375 (INV-199) and M-376 (INV-200), by deed: the gate's own check and the tool's conflict net."""

    def merge_base_equals_main_tip(self):
        """INV-199's gate check, run exactly as the spec states it."""
        base = self.rev("HEAD", self.lane_tree)
        rc, out = _git(self.lane_tree, "merge-base", "main", "HEAD")
        self.assertEqual(rc, 0, "merge-base failed: %s" % out)
        base = out.strip()
        return base == self.rev("main", self.lane_tree)

    def test_merge_base_check_separates_a_stale_lane_from_a_rebased_one(self):
        self.assertTrue(self.merge_base_equals_main_tip(),
                        "a lane cut from main's tip read as stale before main ever moved")
        # another lane lands: main moves under this one
        self.commit(self.main_tree, "h", "three\n", "three")
        self.assertFalse(self.merge_base_equals_main_tip(),
                         "a lane that has not rebased read as rebased — the landing gate would "
                         "run on a stale tree, which is the exact thing the check stands against")
        self.run_ok(self.lane_tree, "rebase", "main")
        self.assertTrue(self.merge_base_equals_main_tip(),
                        "a rebased lane still read as stale — the check would red every landing")

    def test_a_rebased_lane_fast_forwards_main_with_no_merge_commit(self):
        self.commit(self.main_tree, "h", "three\n", "three")
        self.run_ok(self.lane_tree, "rebase", "main")
        self.run_ok(self.main_tree, "merge", "--ff-only", "lane/x")
        _, parents = _git(self.main_tree, "rev-list", "--parents", "-n", "1", "main")
        self.assertEqual(len(parents.split()), 2,
                         "main's tip carries more than one parent — a merge commit's second "
                         "parent breaks INV-39's one-row landing commit")
        self.assertEqual(self.rev("main", self.main_tree), self.rev("lane/x", self.main_tree),
                         "the fast-forward did not land the lane's work on main")

    def test_git_halts_a_rebase_on_a_textual_conflict(self):
        self.commit(self.main_tree, "f", "the pen's line\n", "main edits f")
        self.commit(self.lane_tree, "f", "the lane's line\n", "lane edits f")
        rc, out = _git(self.lane_tree, "rebase", "main")
        self.assertNotEqual(rc, 0, "the rebase sailed through a textual conflict")
        self.assertIn("CONFLICT", out.upper(), "git halted for some other reason: %s" % out)
        self.run_ok(self.lane_tree, "rebase", "--abort")

    def test_two_worktrees_share_one_ref_store_so_a_foreign_claim_needs_no_fetch(self):
        """T-18/INV-198: the pen's arbitration reads a foreign session's claim the moment it looks."""
        self.commit(self.main_tree, "queue", "row 1: in-work\n", "claim row 1")
        claim = self.rev("main", self.main_tree)
        self.assertEqual(self.rev("main", self.lane_tree), claim,
                         "the lane read a stale main — a foreign session's claim commit would "
                         "need a fetch, and INV-2's ancestry ordering could not read it")
        rc, out = _git(self.lane_tree, "log", "-1", "--format=%s", "main")
        self.assertEqual(rc, 0, out)
        self.assertIn("claim row 1", out, "the lane could not read the foreign claim's own commit")


class TestLaneTeardown(_ProbeRepo):
    """M-382 (INV-199), by deed: teardown's refusal is the thing that protects a parked lane's work."""

    def test_teardown_is_refused_on_a_worktree_holding_uncommitted_work(self):
        with open(os.path.join(self.lane_tree, "unfinished.txt"), "w", encoding="utf-8") as fh:
            fh.write("a parked lane's half-done work\n")
        rc, out = _git(self.main_tree, "worktree", "remove", self.lane_tree)
        self.assertNotEqual(rc, 0, "teardown erased a lane worktree holding uncommitted work")
        self.assertIn("contains modified or untracked files", out,
                      "teardown refused for some other reason: %s" % out)
        self.assertTrue(os.path.isdir(self.lane_tree), "the lane's tree was removed anyway")

    def test_the_teardown_refusal_carries_a_force_override(self):
        """The boundary beside the guarantee: the refusal is a default, and --force walks past it."""
        with open(os.path.join(self.lane_tree, "unfinished.txt"), "w", encoding="utf-8") as fh:
            fh.write("a parked lane's half-done work\n")
        rc, out = _git(self.main_tree, "worktree", "remove", "--force", self.lane_tree)
        self.assertEqual(rc, 0, "--force no longer overrides the teardown refusal: %s" % out)
        self.assertFalse(os.path.isdir(self.lane_tree), "the lane's tree survived a forced removal")


class TestLaneBranchLaw(unittest.TestCase):
    """M-372 / M-373 / M-375 / M-376 / M-377: the document law, at live-spec's rendered rung."""

    def test_spec_names_the_worktree_mechanism_and_the_branch_name(self):
        # RE-PINNED (see repin log): the literal command "git branch --list 'lane/*'" is a
        # one-home literal — it survives in ARCHITECTURE.md's config-health row (the pack's
        # actual mechanism reference) but PRODUCT_SPEC.md's rewritten Requirement 84/86 states
        # the same behaviour without the raw command ("red a lane worktree or a lane branch
        # with no open row in the config-health gate"). The spec-side check moves to that
        # behavioural statement; the literal check stays pinned on its surviving home.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("a git worktree holding a branch of its own", spec)
        self.assertIn("`lane/<row>-<slug>`", spec)
        self.assertIn("no open row in the config-health gate", spec)
        self.assertIn("git branch --list 'lane/*'", read_flat("ARCHITECTURE.md"))

    def test_spec_grants_a_worker_lane_its_worktree_with_no_gate(self):
        # Re-pinned at row-445 pass 2 (one-home literal): the spec states the law behaviourally
        # ("the Agent tool's worktree isolation option with no permission gate"); the literal
        # parameter snippet's one home is build-pipeline's Trains section, the skill that performs
        # the delegation.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("the Agent tool's worktree isolation option with no permission gate", spec)
        bp = read_all_flat("skills/build-pipeline/SKILL.md")
        self.assertIn('`isolation: "worktree"`', bp)
        self.assertIn("it carries no gate, usable today", bp)

    def test_the_claim_commits_to_main_and_the_spec_states_why(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A lane branch is born from the claim commit, on main", spec)
        self.assertIn("two claims are ordered by git ancestry", spec)
        self.assertIn("each reading itself as first", spec)

    def test_the_pen_moves_main_and_the_lane_branch_is_penless(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("holding the pen is the sole right to move main", spec)
        self.assertIn("that traffic is penless", spec)

    def test_the_pen_keeps_the_documents_and_the_spec_states_why(self):
        # RE-PINNED (see repin log): "the collision the pen prevents was never textual" is
        # paraphrased, not dropped — PRODUCT_SPEC.md's rewritten Requirement 85 (R49.3/R49.4)
        # states the identical fact in its own words: two branches would each prove against a
        # spec the OTHER is about to move (a moving target for the proof), which is exactly why
        # a textual merge cannot be the fix ("no suite reads a proof").
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "two lanes drafting deltas on two branches would each prove against a spec the "
            "other is about to move",
            spec,
        )
        self.assertIn("no suite reads a proof", spec)

    def test_the_landing_is_rebase_then_gate_then_fast_forward(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A lane lands by fast-forward from a rebased branch", spec)
        self.assertIn("the branch's merge-base with main equals main's tip", spec)

    def test_teardown_and_the_stale_lane_check(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("refuse teardown on a worktree holding uncommitted work", spec)
        self.assertIn(
            "red a lane worktree or a lane branch with no open row in the config-health gate",
            spec,
        )

    def test_the_semantic_residual_is_named_rather_than_papered_over(self):
        # RE-PINNED (see repin log): the pre-rewrite spec stated "a fact no test covers, WHICH
        # IS a matrix gap" — the two phrases were an explicit apposition, the same fact stated
        # twice. PRODUCT_SPEC.md's rewritten Requirement 87 criterion 3 keeps the term that
        # carries the meaning ("test-matrix gap") and drops only the elaborative synonym.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Git halts the rebase on a textual conflict", spec)
        self.assertIn("test-matrix gap", spec)

    def test_the_vendored_line_cites_inv105_rather_than_restating_it(self):
        # CANDIDATE REAL DEFECT (see repin log): "A line in the machine-wide instruction file
        # would reach every project" — the explanatory WHY behind scoping the vendored line
        # per-host — has no surviving text in PRODUCT_SPEC.md's rewritten Requirement 88;
        # criterion 2 states the WHAT (scope to the host) with the reasoning dropped. Left red.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "cites the isolation law's write-set condition rather than restating it", spec
        )
        self.assertIn("keeping the condition's one home", spec)
        # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-b mapping — the WHY of host-scoping; the scoping duty itself is asserted above.)

    def test_every_new_anchor_carries_an_index_row(self):
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as fh:
            index = [line for line in fh if line.startswith("| ")]
        for anchor in ("E-34", "T-23", "INV-198", "INV-199", "INV-200", "INV-201"):
            rows = [line for line in index if line.startswith("| %s |" % anchor)]
            self.assertEqual(len(rows), 1, "%s owes exactly one Formal index row" % anchor)


SCRIPT = os.path.join(ROOT, "scripts", "open-lane.sh")


class _LaneOpenActRepo(unittest.TestCase):
    """A minimal repo the lane-open act runs against, hermetic like the probe above.

    The act (SPEC INV-214) is a real git ceremony, so its guards are proven by deed on a
    real repo rather than trusted from the script's own prose: the claim commit lands on
    main, the lane branch is cut into its own worktree, the cap refuses a lane past it, and
    the one-row claim commit refuses anything but the queue file.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="livespec-test-openlane-")
        self.addCleanup(_robust_rmtree, self.tmp)
        self.repo = os.path.join(self.tmp, "repo")
        os.makedirs(self.repo)
        self.run_ok("init", "-q", "-b", "main")
        self._write("ROADMAP.md", "| 500 | a wish | surface | queued | acc |\n")
        self.run_ok("add", "ROADMAP.md")
        self.run_ok("commit", "-qm", "init")
        self.wt = os.path.join(self.tmp, "wts")
        self.profile = os.path.join(self.tmp, "profile.md")
        self.write_cap(3)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, name, body):
        with open(os.path.join(self.repo, name), "w", encoding="utf-8") as fh:
            fh.write(body)

    def write_cap(self, n):
        with open(self.profile, "w", encoding="utf-8") as fh:
            fh.write("- `lanes.cap: %d` blah\n" % n)

    def run_ok(self, *args):
        rc, out = _git(self.repo, *args)
        self.assertEqual(rc, 0, "git %s -> %s" % (" ".join(args), out))
        return out

    def stage_flip(self, row):
        with open(os.path.join(self.repo, "ROADMAP.md"), "a", encoding="utf-8") as fh:
            fh.write("| %s | flip | surface | in-work | acc |\n" % row)
        self.run_ok("add", "ROADMAP.md")

    def act(self, row, slug, profile=None):
        env = dict(os.environ)
        env.update({
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_AUTHOR_NAME": "livespec-test",
            "GIT_AUTHOR_EMAIL": "livespec-test@example.invalid",
            "GIT_COMMITTER_NAME": "livespec-test",
            "GIT_COMMITTER_EMAIL": "livespec-test@example.invalid",
            "GIT_TERMINAL_PROMPT": "0",
            "LIVE_SPEC_PROFILE": profile if profile is not None else self.profile,
            "LIVE_SPEC_WORKTREES": self.wt,
        })
        proc = subprocess.run(["bash", SCRIPT, str(row), slug], cwd=self.repo, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        return proc.returncode, proc.stdout.decode("utf-8", "replace")


class TestTheLaneOpenActByDeed(_LaneOpenActRepo):
    """M-395 (INV-214), by deed."""

    def test_the_act_commits_the_claim_to_main_and_cuts_the_lane_worktree(self):
        self.stage_flip(500)
        rc, out = self.act(500, "my-slug")
        self.assertEqual(rc, 0, out)
        # the claim commit is on main and names the row
        self.assertEqual(self.run_ok("rev-parse", "--abbrev-ref", "HEAD").strip(), "main")
        self.assertIn("row 500", self.run_ok("log", "-1", "--format=%s"))
        # the lane branch exists and is cut from the claim commit (main's tip)
        self.assertIn("lane/500-my-slug", self.run_ok("branch", "--list", "lane/*"))
        self.assertEqual(self.run_ok("rev-parse", "lane/500-my-slug").strip(),
                         self.run_ok("rev-parse", "main").strip())
        # the lane has its own worktree
        self.assertIn("lane/500-my-slug", self.run_ok("worktree", "list"))

    def test_the_act_refuses_a_lane_past_the_profile_cap(self):
        self.write_cap(1)
        self.run_ok("branch", "lane/499-already")   # one lane already open, cap is one
        self.stage_flip(500)
        rc, out = self.act(500, "my-slug")
        self.assertNotEqual(rc, 0)
        self.assertIn("cap reached", out)
        self.assertNotIn("lane/500-my-slug", self.run_ok("branch", "--list", "lane/*"))

    def test_the_cap_defaults_to_three_with_no_profile_line(self):
        self.run_ok("branch", "lane/1-a")
        self.run_ok("branch", "lane/2-b")           # two open, a third fits the default of three
        self.stage_flip(500)
        rc, out = self.act(500, "my-slug", profile=os.path.join(self.tmp, "absent.md"))
        self.assertEqual(rc, 0, out)
        self.assertIn("of 3", out)

    def test_the_act_refuses_a_claim_carrying_more_than_the_queue_file(self):
        self.stage_flip(500)
        self._write("other.txt", "x\n")
        self.run_ok("add", "other.txt")
        rc, out = self.act(500, "my-slug")
        self.assertNotEqual(rc, 0)
        self.assertIn("one row's delta", out)

    def test_the_act_refuses_when_nothing_is_staged(self):
        rc, out = self.act(500, "my-slug")
        self.assertNotEqual(rc, 0)
        self.assertIn("stage the row", out)

    def test_the_act_refuses_off_main(self):
        self.run_ok("checkout", "-q", "-b", "feature")
        self.stage_flip(500)
        rc, out = self.act(500, "my-slug")
        self.assertNotEqual(rc, 0)
        self.assertIn("on main", out)


class TestTheLaneOpenActLaw(unittest.TestCase):
    """M-395 (INV-214): the act and its discipline as shipped document law."""

    def test_spec_states_the_lane_open_act(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Opening a lane is a performed act", spec)
        self.assertIn("scripts/open-lane.sh", spec)
        self.assertIn("refuses to open a lane past that value", spec)

    def test_the_serial_check_is_a_discipline_the_spec_states_why(self):
        # CANDIDATE REAL DEFECT (see repin log): "a judgment call is never a gate" — the
        # explicit maxim naming why this stays a discipline rather than a mechanical gate —
        # has no surviving text in PRODUCT_SPEC.md's rewritten Requirement 91 criterion 4.
        # Left red.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("keep the recorded-reason duty a matter of discipline", spec)
        # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-b mapping — the maxim framing; the recorded-reason discipline is asserted above.)
        self.assertIn("torn down at each landing", spec)

    def test_inv214_carries_one_index_row(self):
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as fh:
            index = [line for line in fh if line.startswith("| INV-214 |")]
        self.assertEqual(len(index), 1, "INV-214 owes exactly one Formal index row")

    def test_the_cap_reads_off_the_profile_not_a_hardcoded_three(self):
        # RE-PINNED (see repin log): the config-key backtick "`lanes.cap`" is a one-home
        # literal — it survives in skills/live-spec-base/SKILL.md (the base settings ladder,
        # both the prose rule and the defaults table row) but PRODUCT_SPEC.md itself never
        # names a settings key literally, only the behavioural "profile-declared lane cap".
        # The spec-side check stays on the paraphrase; the literal check moves to its one
        # surviving home.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("the profile-declared lane cap", spec)
        self.assertIn("`lanes.cap`", read_flat("skills/live-spec-base/SKILL.md"))

    def test_base_rulebook_and_build_pipeline_state_the_act(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("The lane-open act", base)
        self.assertIn("`lanes.cap`", base)   # the cap row in the package defaults
        pipe = read_all_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("Opening a lane is an act you PERFORM", pipe)

    def test_architecture_owns_inv214(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("INV-214", arch)
        self.assertIn("scripts/open-lane.sh", arch)


if __name__ == "__main__":
    unittest.main()
