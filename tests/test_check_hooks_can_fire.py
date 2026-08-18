"""tests/test_check_hooks_can_fire.py — the hook red-proof runner proves it can red itself.

guardrails/check-hooks-can-fire.py is the hook-side sibling of check-every-gate-can-fail.py (gate w):
it runs every classified session hook against a fixture built to trigger it and fails when a hook
stays silent. A runner that can only ever pass is itself a hollow check, so this file proves the
runner REDS on a hook that never fires and on a fixture carrying no trigger, before it proves the
runner stays green against the real, shipped fixtures.
"""
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = os.path.join(REPO_ROOT, "guardrails", "check-hooks-can-fire.py")
REAL_FIXTURES_DIR = os.path.join(REPO_ROOT, "guardrails", "hook-red-fixtures")
REAL_HOOKS_DIR = os.path.join(REPO_ROOT, "hooks")
REAL_INSTALLED_DIR = os.path.expanduser("~/.claude/hooks")


def _run(env_overrides):
    env = dict(os.environ)
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, RUNNER], capture_output=True, text=True, timeout=60, env=env,
    )


def test_runner_reds_on_a_hook_that_never_fires(tmp_path):
    """Point the runner at a stub hook that always exits 0 with empty stdout — a hook that can never
    fire — and assert the runner's own exit is non-zero and names the silent hook."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    (stub_hooks_dir / "scissors-scan.py").write_text(
        "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"
    )

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "scissors-scan.py": {"fixture": "hook-red-fixtures/scissors-scan", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "SILENT scissors-scan.py" in proc.stdout, proc.stdout


def test_runner_reds_on_a_fixture_that_carries_no_trigger(tmp_path):
    """Break the FIXTURE instead of the hook: a transcript with no offending text must not make the
    real hook fire, so the runner reds exactly as it would for a genuinely blind hook."""
    fixtures_root = tmp_path / "fixtures"
    fixture_dir = fixtures_root / "scissors-scan"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "payload.json").write_text(json.dumps({
        "transcript_path": "transcript.jsonl", "session_id": "broken", "stop_hook_active": False,
    }))
    (fixture_dir / "transcript.jsonl").write_text(
        json.dumps({"type": "user", "message": {"role": "user",
                    "content": [{"type": "text", "text": "hi"}]}}) + "\n"
        + json.dumps({"type": "assistant", "message": {"role": "assistant",
                      "content": [{"type": "text", "text": "All is well, nothing notable here."}]}}) + "\n"
    )

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "scissors-scan.py": {"fixture": "hook-red-fixtures/scissors-scan", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_REPO_DIR": REAL_HOOKS_DIR,
        "HOOKS_INSTALLED_DIR": REAL_INSTALLED_DIR,
        "HOOKS_FIXTURES_DIR": str(fixtures_root),
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "SILENT scissors-scan.py" in proc.stdout, proc.stdout


def test_runner_is_green_on_the_real_shipped_fixtures():
    """The actual census: every hook classified in guardrails/hook-red-proofs.json fires against its
    real, shipped fixture under guardrails/hook-red-fixtures/."""
    proc = _run({})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FAIL" not in proc.stdout
    assert "UNCLASSIFIED" not in proc.stdout, proc.stdout


# ---- A1 (2026-07-27 prover addendum): the registry census the runner never performed ---------------
# guardrails/judge-hooks.json's "wired" list is the population of session hooks live in every adopting
# host. A hook wired there but classified in neither "proofs" nor "cannot_red" is a live hook nobody
# proves and nothing notices — the exact gap that let clock-hook.sh and chat-law-hook.sh ship unproven.

def test_runner_is_census_complete_on_the_real_shipped_registry():
    """Every one of judge-hooks.json's wired hooks must be classified today, and the runner must say
    so by naming the count, not merely by staying green."""
    wired = json.load(open(os.path.join(REPO_ROOT, "guardrails", "judge-hooks.json")))["wired"]
    expected = len(wired)
    proc = _run({})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ("census %d/%d wired hook(s) classified" % (expected, expected)) in proc.stdout, proc.stdout


def test_every_opt_in_hook_is_classified_too():
    """The census counts the wired list alone, and six hooks left that list on 2026-08-17 when the
    owner stood them down (PRODUCT_SPEC.md Requirement 311). They still ship, a host still turns them
    on, and their red proofs still run — so the population this file was written for is asserted here
    directly rather than lost with the census it fell out of."""
    decl = json.load(open(os.path.join(REPO_ROOT, "guardrails", "judge-hooks.json")))
    six = {"scissors-scan", "hedge-scan", "affirmation-scan", "code-anchor-scan",
           "register-judge-collect", "register-judge-report"}
    assert set(decl["opt_in_surface"]) == six, (
        "the opt-in roster moved; this test reads the declaration, so the roster is pinned here too")
    proofs = json.load(open(os.path.join(REPO_ROOT, "guardrails", "hook-red-proofs.json")))
    classified = set(proofs.get("proofs", {})) | set(proofs.get("cannot_red", {}))
    unclassified = []
    for stem in sorted(decl["opt_in_surface"]):
        if not any(stem + ext in classified for ext in (".py", ".sh")):
            unclassified.append(stem)
    assert not unclassified, (
        "an opt-in hook carries no red proof and no cannot_red note: %r" % unclassified)


def test_runner_reds_on_wired_hook_absent_from_both_maps(tmp_path):
    """Build a temporary registry pair (proofs.json + judge-hooks.json), not the real one: a hook
    judge-hooks.json wires live but hook-red-proofs.json classifies nowhere must red the run by name,
    even though nothing ever tries to fire it."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    (stub_hooks_dir / "scissors-scan.py").write_text("#!/usr/bin/env python3\n")
    (stub_hooks_dir / "clock-hook.sh").write_text("#!/bin/sh\necho hi\n")

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {},
        "cannot_red": {"scissors-scan.py": "test double, not exercised by this census-only test"},
    }))

    judge_hooks_json = tmp_path / "judge-hooks.json"
    judge_hooks_json.write_text(json.dumps({
        "wired": {"scissors-scan": "Stop", "clock-hook": "UserPromptSubmit"},
        "library": [],
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(judge_hooks_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "UNCLASSIFIED clock-hook.sh" in proc.stdout, proc.stdout


def test_census_never_demands_a_library_list_file(tmp_path):
    """judge-hooks.json's library list is the pack's own carve-out for a shared reader or an opt-in
    net that gate v never wires live. A name that lives only in library, never in wired, must not be
    demanded by the census even when it is classified nowhere in hook-red-proofs.json."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    (stub_hooks_dir / "scissors-scan.py").write_text("#!/usr/bin/env python3\n")

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {},
        "cannot_red": {"scissors-scan.py": "test double, not exercised by this census-only test"},
    }))

    judge_hooks_json = tmp_path / "judge-hooks.json"
    judge_hooks_json.write_text(json.dumps({
        "wired": {"scissors-scan": "Stop"},
        "library": ["turn_reader"],  # classified nowhere, on purpose — must not fail the census
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(judge_hooks_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "turn_reader" not in proc.stdout, proc.stdout


# ---- S1 (2026-07-27 fold review): a wired name resolving to no file at all --------------------------
# R292.6 covers a wired hook classified in neither map; R292.8 covers a map entry naming a file found
# under neither directory. Neither reaches a THIRD case the runner already reds: a wired name with no
# file under either extension at all — the drift signature of a registry naming a hook that was renamed
# or deleted.

def test_runner_reds_on_a_wired_name_resolving_to_no_file(tmp_path):
    """A wired hook whose name resolves to no .py or .sh file anywhere must red UNRESOLVED, distinct
    from an existing file classified in neither map (UNCLASSIFIED, covered above)."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    # deliberately no file for "ghost-hook" under either extension

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({"proofs": {}, "cannot_red": {}}))

    judge_hooks_json = tmp_path / "judge-hooks.json"
    judge_hooks_json.write_text(json.dumps({
        "wired": {"ghost-hook": "Stop"},
        "library": [],
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(judge_hooks_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "UNRESOLVED ghost-hook" in proc.stdout, proc.stdout


# ---- S3 (2026-07-27 fold review): R292.8's "either map" mirrored for the proofs arm -------------------
# test_runner_reds_on_a_cannot_red_entry_naming_a_missing_file (below) seeds cannot_red alone. The proofs
# loop is the older code path and the one more likely touched next, so it owes the same proof.

def test_runner_reds_on_a_proofs_entry_naming_a_missing_file(tmp_path):
    """The mirror case: a proofs entry naming a hook file that exists nowhere under either hooks
    directory must red by name, the same as a cannot_red entry naming a missing file does."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    # deliberately no ghost-hook.py under either hooks directory

    fixtures_root = tmp_path / "fixtures"
    fixture_dir = fixtures_root / "ghost-hook"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "payload.json").write_text(json.dumps({
        "transcript_path": "transcript.jsonl", "session_id": "ghost", "stop_hook_active": False,
    }))
    (fixture_dir / "transcript.jsonl").write_text("")

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "ghost-hook.py": {"fixture": "hook-red-fixtures/ghost-hook", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(tmp_path / "no-such-judge-hooks.json"),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": str(fixtures_root),
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "SILENT ghost-hook.py — not found under" in proc.stdout, proc.stdout


# ---- S5 (2026-07-27 fold review): the closing line must name which rule broke -------------------------
# The runner reds four ways: a hook silent against its fixture, a wired hook classified in neither map,
# a wired name resolving to no file, and a registry entry naming a missing file. Before this fix the
# closing line named only the first for all four paths.

def test_failure_summary_names_each_red_path(tmp_path):
    """Trigger two distinct causes in one run — a hook silent against its fixture and a wired hook
    classified in neither map — and assert the closing line carries a sentence naming each, not one
    generic line that fits only the first."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    (stub_hooks_dir / "scissors-scan.py").write_text(
        "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"
    )
    (stub_hooks_dir / "clock-hook.sh").write_text("#!/bin/sh\necho hi\n")

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "scissors-scan.py": {"fixture": "hook-red-fixtures/scissors-scan", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    judge_hooks_json = tmp_path / "judge-hooks.json"
    judge_hooks_json.write_text(json.dumps({
        "wired": {"scissors-scan": "Stop", "clock-hook": "UserPromptSubmit"},
        "library": [],
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(judge_hooks_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    tail = proc.stdout.strip().splitlines()[-1]
    assert tail.startswith("check-hooks-can-fire: FAIL"), tail
    assert "silent against its own fixture" in tail, tail
    assert "classified in neither map" in tail, tail


def test_runner_reds_on_a_cannot_red_entry_naming_a_missing_file(tmp_path):
    """A proofs/cannot_red key that names a file that exists nowhere under either hooks directory must
    red, the same class of finding as a wired hook classified nowhere."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {},
        "cannot_red": {"ghost-hook.py": "names a file that exists nowhere"},
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_JUDGE_HOOKS_JSON": str(tmp_path / "no-such-judge-hooks.json"),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "ghost-hook.py" in proc.stdout, proc.stdout
