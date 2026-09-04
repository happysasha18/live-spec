"""Every automatic check proves it can actually catch its problem — id: q-489.

The row's corrected acceptance (PLAN.md, 28.08): every check that ships under `guardrails/` owns
a fixture it reds against without its fix, and the suite runs that fixture; a test walking
`guardrails/` reds a check that arrives with no such fixture. One check completes the walk end to
end, so the shape is proved on a real one before it binds the rest — this file does not retrofit
the other forty.

`check-prototype-fence.sh` is that one check: `_prototype_fence_reds_the_bug` plants the exact
wiring fault the gate exists to catch (a PROD file structurally referencing into the fenced
`prototype/` home) and asserts the gate reds; `_prototype_fence_passes_the_fix` removes the
reference — the fix — and asserts the same gate passes. Both run live, here, every suite run.

The walk itself (`missing_fixture_proofs`) lists every `check-*.py` / `check-*.sh` file directly
under a `guardrails/` directory (the naming convention every check in this pack follows — verified
2026-08-31 against `ls guardrails/check-*.{py,sh}`, 41 files) and flags any that is neither in
PROVEN (owns a live fixture proof, like the one above) nor in GRANDFATHERED (the other 40, named
here explicitly, out of this row's scope by its own corrected acceptance). GRANDFATHERED is a fixed
list, not "everything not proven" — a name that is not on it and ships with no proof is exactly the
class this row exists to catch, so `test_walk_reds_a_new_check_shipped_with_no_fixture` plants one
in a scratch directory and confirms the walk reds on it.
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

GUARDRAILS = os.path.join(ROOT, "guardrails")


def _git_scratch_repo(tmp):
    subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "a@example.com"], cwd=tmp, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "a"], cwd=tmp, capture_output=True, text=True)


def _write(tmp, rel, content):
    path = os.path.join(tmp, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _commit_all(tmp):
    subprocess.run(["git", "add", "-A"], cwd=tmp, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-q", "-m", "scratch"], cwd=tmp, capture_output=True, text=True)


def _run_prototype_fence(tmp):
    return subprocess.run(
        [os.path.join(GUARDRAILS, "check-prototype-fence.sh"), tmp],
        cwd=ROOT, capture_output=True, text=True,
    )


def prototype_fence_reds_the_bug():
    """The bug: a shipping file structurally references into the fenced prototype/ home. The
    fixture check-prototype-fence.sh exists to catch. Returns True when the gate reds it."""
    with tempfile.TemporaryDirectory() as tmp:
        _git_scratch_repo(tmp)
        _write(tmp, "prototype/sketch.html", "<html>sketch</html>\n")
        _write(tmp, "index.html", '<script src="prototype/sketch.html"></script>\n')
        _commit_all(tmp)
        result = _run_prototype_fence(tmp)
        return result.returncode != 0 and "FAIL (prototype fence)" in result.stdout


def prototype_fence_passes_the_fix():
    """The same fixture, fixed: the wiring reference is gone (promoted or removed), nothing
    outside prototype/ names the fenced file any more. Returns True when the gate passes it."""
    with tempfile.TemporaryDirectory() as tmp:
        _git_scratch_repo(tmp)
        _write(tmp, "prototype/sketch.html", "<html>sketch</html>\n")
        _write(tmp, "index.html", "<html>nothing fenced referenced here</html>\n")
        _commit_all(tmp)
        result = _run_prototype_fence(tmp)
        return result.returncode == 0 and "OK (prototype fence)" in result.stdout


def _run_worktree_line(host):
    return subprocess.run(
        [os.path.join(GUARDRAILS, "check-worktree-line.sh"), host],
        cwd=ROOT, capture_output=True, text=True,
    )


def worktree_line_reds_the_bug():
    """The bug: a host's project instructions carry no vendored worktree line citing the
    isolation law's write-set condition (SPEC INV-201, PLAN q-804). Returns True when the gate
    reds it."""
    with tempfile.TemporaryDirectory() as tmp:
        _write(tmp, "CLAUDE.md", "# a host project\n\nSome other instructions entirely.\n")
        result = _run_worktree_line(tmp)
        return result.returncode != 0 and '"code":"worktree-line"' in result.stdout


def worktree_line_passes_the_fix():
    """The same fixture, fixed: the host's CLAUDE.md carries a line naming a worktree and
    citing INV-105. Returns True when the gate passes it."""
    with tempfile.TemporaryDirectory() as tmp:
        _write(
            tmp, "CLAUDE.md",
            "# a host project\n\n"
            "Two lanes with overlapping write-sets get worktree isolation (SPEC INV-105).\n",
        )
        result = _run_worktree_line(tmp)
        return result.returncode == 0 and "worktree-line: OK" in result.stdout


def _write_status_view_fixture(tmp, host_contents, pack_contents="#!/bin/bash\necho hi\n"):
    """A pack root plus a host root, wired so the host's `scripts/ratchet-manifest.json` pins
    the pack's `scaffold/status-view/state-probe.sh` against the host's own `scripts/state-
    probe.sh` (SPEC INV-325, PLAN q-818). Returns (host_dir, pack_dir)."""
    import json
    pack = os.path.join(tmp, "pack")
    host = os.path.join(tmp, "host")
    os.makedirs(os.path.join(pack, "scaffold", "status-view"))
    os.makedirs(os.path.join(host, "scripts"))
    _write(pack, "VERSION", "1.0.0\n")
    _write(pack, os.path.join("scaffold", "status-view", "state-probe.sh"), pack_contents)
    _write(host, os.path.join("scripts", "state-probe.sh"), host_contents)
    manifest = {"pack_version": "1.0.0",
                "vendored": {"scaffold/status-view/state-probe.sh": "deadbeef" * 8}}
    _write(host, os.path.join("scripts", "ratchet-manifest.json"), json.dumps(manifest))
    return host, pack


def _run_status_view_drift(host, pack):
    return subprocess.run(
        [os.path.join(GUARDRAILS, "check-status-view-drift.py"), host, "--pack-root", pack],
        cwd=ROOT, capture_output=True, text=True,
    )


def status_view_drift_reds_the_bug():
    """The bug: a host's vendored `scripts/state-probe.sh` has a local edit the pack's own
    `scaffold/status-view/state-probe.sh` does not carry (SPEC INV-325, PLAN q-818). Returns True
    when the gate reds it."""
    with tempfile.TemporaryDirectory() as tmp:
        host, pack = _write_status_view_fixture(tmp, "#!/bin/bash\necho HACKED\n")
        result = _run_status_view_drift(host, pack)
        return result.returncode != 0 and "differs from the pack's own copy" in result.stdout


def status_view_drift_passes_the_fix():
    """The same fixture, fixed: the host's vendored copy is byte-identical to the pack's own.
    Returns True when the gate passes it."""
    with tempfile.TemporaryDirectory() as tmp:
        host, pack = _write_status_view_fixture(tmp, "#!/bin/bash\necho hi\n")
        result = _run_status_view_drift(host, pack)
        return result.returncode == 0 and "no drift" in result.stdout


def _git_two_worktree_scratch(tmp):
    """A primary tree plus one lane worktree, both committed once — the shape the merge-base
    check reads (SPEC INV-199, PLAN q-804). Returns (primary_dir, lane_dir)."""
    primary = os.path.join(tmp, "primary")
    lane = os.path.join(tmp, "lane")
    os.makedirs(primary)
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "livespec-test", "GIT_AUTHOR_EMAIL": "livespec-test@example.invalid",
        "GIT_COMMITTER_NAME": "livespec-test", "GIT_COMMITTER_EMAIL": "livespec-test@example.invalid",
    })
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=primary, env=env, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=primary, env=env,
                    capture_output=True, text=True)
    subprocess.run(["git", "worktree", "add", "-q", "-b", "lane/x", lane], cwd=primary, env=env,
                    capture_output=True, text=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "lane work"], cwd=lane, env=env,
                    capture_output=True, text=True)
    return primary, lane, env


def _run_merge_base(cwd):
    return subprocess.run(
        [os.path.join(GUARDRAILS, "check-merge-base.sh")], cwd=cwd, capture_output=True, text=True,
    )


def merge_base_reds_the_bug():
    """The bug: main moved under a lane that never rebased (SPEC INV-199, PLAN q-804). Returns
    True when the gate reds it."""
    with tempfile.TemporaryDirectory() as tmp:
        primary, lane, env = _git_two_worktree_scratch(tmp)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "main moved"], cwd=primary,
                        env=env, capture_output=True, text=True)
        result = _run_merge_base(lane)
        return result.returncode != 0 and '"code":"merge-base"' in result.stdout


def merge_base_passes_the_fix():
    """The same fixture, fixed: the lane rebases onto main's new tip. Returns True when the gate
    passes it."""
    with tempfile.TemporaryDirectory() as tmp:
        primary, lane, env = _git_two_worktree_scratch(tmp)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "main moved"], cwd=primary,
                        env=env, capture_output=True, text=True)
        subprocess.run(["git", "rebase", "main"], cwd=lane, env=env, capture_output=True, text=True)
        result = _run_merge_base(lane)
        return result.returncode == 0 and "merge-base: OK" in result.stdout


#: Checks that own a live fixture proof, run by this suite — the shape q-489 asks every check to
#: carry eventually. check-prototype-fence.sh is the one check that completes the walk end to end;
#: check-merge-base.sh and check-worktree-line.sh (PLAN q-804) are the next two, shipped with the
#: fixture proof from the start rather than grandfathered in unproven.
PROVEN = {
    "check-prototype-fence.sh": (prototype_fence_reds_the_bug, prototype_fence_passes_the_fix),
    "check-merge-base.sh": (merge_base_reds_the_bug, merge_base_passes_the_fix),
    "check-worktree-line.sh": (worktree_line_reds_the_bug, worktree_line_passes_the_fix),
    "check-status-view-drift.py": (status_view_drift_reds_the_bug, status_view_drift_passes_the_fix),
}

#: Every other check-*.py / check-*.sh shipping in guardrails/ on 2026-08-31, when this row's
#: acceptance was narrowed to "one check, not all of them." Named explicitly rather than derived
#: as "everything not in PROVEN" — a derived list could never miss a new arrival, which would make
#: the walk below vacuous. A name added to guardrails/ after this date and absent from both sets
#: is exactly what the walk exists to catch.
GRANDFATHERED = frozenset({
    "check-agent-card.py",
    "check-architecture-reference.py",
    "check-authority-anchor.py",
    "check-board.py",
    "check-broad-kill.sh",
    "check-cleanup-notice.sh",
    "check-config-health-perms.py",
    "check-config-health.sh",
    "check-config-surface.py",
    "check-deferral-marker.py",
    "check-deletion-only-push.sh",
    "check-delta-record.py",
    "check-deposit-description.py",
    "check-doc-rotation.py",
    "check-earned-message.py",
    "check-freeze.sh",
    "check-future-times.sh",
    "check-index-generated.py",
    "check-landing-next-steps.py",
    "check-language-rules.py",
    "check-matrix-reference.py",
    "check-muted-launch.sh",
    "check-no-history.py",
    "check-one-name.py",
    "check-pin-drift.sh",
    "check-prover-record.sh",
    "check-push-reach.sh",
    "check-rendered-sweep.py",
    "check-requirement-shape.py",
    "check-runaway-child.py",
    "check-shipped-language.sh",
    "check-skill-loadability.sh",
    "check-skill-review.sh",
    "check-tests.sh",
    "check-tier-refusal.py",
    "check-touchpoint-kind.py",
    "check-vocabulary.py",
    "check-weak-words.py",
    "check-worker-restore.py",
})


def list_checks(guardrails_dir):
    """Every check-*.py / check-*.sh file directly under guardrails_dir — not recursive, so an
    attic/ (retired) or a nested scaffold copy never counts as a shipping check."""
    if not os.path.isdir(guardrails_dir):
        return []
    out = []
    for name in sorted(os.listdir(guardrails_dir)):
        full = os.path.join(guardrails_dir, name)
        if not os.path.isfile(full):
            continue
        if name.startswith("check-") and (name.endswith(".py") or name.endswith(".sh")):
            out.append(name)
    return out


def missing_fixture_proofs(guardrails_dir, proven=PROVEN, grandfathered=GRANDFATHERED):
    """Every shipping check under guardrails_dir that owns no proven fixture and is not
    grandfathered — the walk q-489 asks for. Empty means the walk is clean."""
    return [
        name for name in list_checks(guardrails_dir)
        if name not in proven and name not in grandfathered
    ]


class TestOneCheckCompletesTheWalk(unittest.TestCase):
    """check-prototype-fence.sh proves the shape live: reds the bug, passes the fix."""

    def test_prototype_fence_reds_without_its_fix(self):
        self.assertTrue(
            prototype_fence_reds_the_bug(),
            "check-prototype-fence.sh must red the fixture with the wiring bug present",
        )

    def test_prototype_fence_passes_with_its_fix(self):
        self.assertTrue(
            prototype_fence_passes_the_fix(),
            "check-prototype-fence.sh must pass the same fixture once the reference is gone",
        )

    def test_merge_base_reds_without_its_fix(self):
        self.assertTrue(
            merge_base_reds_the_bug(),
            "check-merge-base.sh must red a lane whose branch has not rebased onto main's tip",
        )

    def test_merge_base_passes_with_its_fix(self):
        self.assertTrue(
            merge_base_passes_the_fix(),
            "check-merge-base.sh must pass the same lane once it has rebased onto main's tip",
        )

    def test_worktree_line_reds_without_its_fix(self):
        self.assertTrue(
            worktree_line_reds_the_bug(),
            "check-worktree-line.sh must red a host whose CLAUDE.md carries no worktree line",
        )

    def test_worktree_line_passes_with_its_fix(self):
        self.assertTrue(
            worktree_line_passes_the_fix(),
            "check-worktree-line.sh must pass the same host once the line is vendored in",
        )

    def test_status_view_drift_reds_without_its_fix(self):
        self.assertTrue(
            status_view_drift_reds_the_bug(),
            "check-status-view-drift.py must red a host whose vendored state-probe.sh diverged "
            "from the pack's own copy",
        )

    def test_status_view_drift_passes_with_its_fix(self):
        self.assertTrue(
            status_view_drift_passes_the_fix(),
            "check-status-view-drift.py must pass the same host once its vendored copy is "
            "byte-identical to the pack's own",
        )


class TestWalkGuardrailsForFixtureProofs(unittest.TestCase):
    """The walking test itself: today's real tree is clean, and a new check with no fixture reds."""

    def test_real_tree_walk_is_clean(self):
        missing = missing_fixture_proofs(GUARDRAILS)
        self.assertEqual(
            missing, [],
            "check(s) shipping in guardrails/ with neither a proven fixture nor a grandfathered "
            "entry: %r — either the check is new (give it a fixture, PROVEN) or this suite's "
            "GRANDFATHERED list has drifted from guardrails/'s real contents" % (missing,),
        )

    def test_walk_reds_a_new_check_shipped_with_no_fixture(self):
        """Plants a fake check with no fixture proof in a scratch guardrails/ and confirms the
        walk reds on it — the "as a class, going forward" half of q-489's acceptance."""
        with tempfile.TemporaryDirectory() as tmp:
            for name in list(GRANDFATHERED) + list(PROVEN):
                open(os.path.join(tmp, name), "w").close()
            open(os.path.join(tmp, "check-new-thing-nobody-proved.sh"), "w").close()
            missing = missing_fixture_proofs(tmp)
            self.assertEqual(missing, ["check-new-thing-nobody-proved.sh"])

    def test_walk_is_clean_with_no_new_arrivals(self):
        """The negative control for the test above: the same scratch tree, minus the planted
        fake check, walks clean — the red above is caused by the new arrival, nothing else."""
        with tempfile.TemporaryDirectory() as tmp:
            for name in list(GRANDFATHERED) + list(PROVEN):
                open(os.path.join(tmp, name), "w").close()
            missing = missing_fixture_proofs(tmp)
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
