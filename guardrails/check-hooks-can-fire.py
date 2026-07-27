#!/usr/bin/env python3
"""check-hooks-can-fire.py — every classified session hook proves it still fires (the hook-side
sibling of check-every-gate-can-fail.py, gate w). Zero hooks carried a red proof before this file;
guardrails/gate-red-proofs.json only ever covered pre-push gates.

Reads guardrails/hook-red-proofs.json. For every entry in its "proofs" map, this RUNS the actual
hook script (the repo copy under hooks/ when one exists, else the installed copy under
~/.claude/hooks/ — a fallback that is itself reported, never hidden) against its fixture directory
under guardrails/hook-red-fixtures/, and asserts the hook's own stdout carries a live decision:

  * "json-block" — stdout parses as JSON with "decision": "block" (the shape every Stop-hook scan
    in this family emits: scissors-scan, hedge-scan, answer-first-scan, affirmation-scan,
    lean-orchestrator-scan).
  * "nonempty-contains" — stdout is non-empty and contains a named substring (register-judge-report.sh,
    a UserPromptSubmit hook that prints a plain reason line, not a decision object).

A hook that stays silent against a fixture built to trigger it is named and FAILS the whole run — the
same "a check that cannot fail is a check that watches nothing" law gate-red-proofs.json states for
push gates. Every entry under "cannot_red" is reported, never run, and never counted as a failure —
its reason is printed so the carve-out stays visible rather than silent.

Fixture shape: guardrails/hook-red-fixtures/<hook-stem>/payload.json (the JSON a hook reads on
stdin; a "transcript_path" value is a filename resolved relative to the fixture directory, rewritten
to an absolute path before the hook runs) plus, for a transcript-reading hook, transcript.jsonl (JSONL
transcript records). register-judge-report.sh's fixture instead carries verdict.json, the verdict
file content the runner pre-seeds under a temp $HOME so the real ~/.claude/hooks/.judge/ directory is
never touched.

Env overrides (for testing this runner itself, the same pattern check-judge-listed.py uses):
  HOOKS_PROOFS_JSON     - path to the declaration file (default guardrails/hook-red-proofs.json)
  HOOKS_REPO_DIR        - repo hooks/ directory (default <repo>/hooks)
  HOOKS_INSTALLED_DIR   - installed hooks directory (default ~/.claude/hooks)
  HOOKS_FIXTURES_DIR    - fixtures root (default guardrails/hook-red-fixtures)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

PROOFS_JSON = os.environ.get("HOOKS_PROOFS_JSON", os.path.join(SCRIPT_DIR, "hook-red-proofs.json"))
REPO_HOOKS_DIR = os.environ.get("HOOKS_REPO_DIR", os.path.join(REPO_ROOT, "hooks"))
INSTALLED_HOOKS_DIR = os.environ.get("HOOKS_INSTALLED_DIR", os.path.expanduser("~/.claude/hooks"))
FIXTURES_DIR = os.environ.get("HOOKS_FIXTURES_DIR", os.path.join(SCRIPT_DIR, "hook-red-fixtures"))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve_hook_path(stem):
    """The repo copy when it exists, else the installed copy — reported either way."""
    repo_path = os.path.join(REPO_HOOKS_DIR, stem)
    if os.path.isfile(repo_path):
        return repo_path, False
    installed_path = os.path.join(INSTALLED_HOOKS_DIR, stem)
    if os.path.isfile(installed_path):
        return installed_path, True
    return None, False


def interpreter_for(stem):
    return ["python3"] if stem.endswith(".py") else ["sh"]


def build_payload(fixture_dir):
    """Load payload.json, rewriting a relative transcript_path to an absolute path in-place."""
    payload = load_json(os.path.join(fixture_dir, "payload.json"))
    tp = payload.get("transcript_path")
    if tp and not os.path.isabs(tp):
        payload["transcript_path"] = os.path.join(fixture_dir, tp)
    return payload


def run_json_block_proof(stem, hook_path, fixture_dir):
    """Run a Stop-hook scan and check its stdout is {"decision": "block", ...}."""
    payload = build_payload(fixture_dir)
    proc = subprocess.run(
        interpreter_for(stem) + [hook_path],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )
    out = proc.stdout.strip()
    if not out:
        return False, "stdout was empty (exit %d); stderr: %s" % (proc.returncode, proc.stderr.strip()[:300])
    try:
        decision = json.loads(out)
    except ValueError:
        return False, "stdout did not parse as JSON: %r" % out[:300]
    if decision.get("decision") != "block":
        return False, "stdout carried no \"decision\": \"block\": %r" % out[:300]
    return True, "fired: decision=block"


def run_nonempty_contains_proof(stem, hook_path, fixture_dir, contains):
    """register-judge-report.sh: pre-seed a verdict under an isolated temp $HOME, run the hook, and
    check its stdout contains the named substring. The real ~/.claude/hooks/.judge/ is never touched —
    the hook's own VERDICT_DIR is derived from $HOME, which this run overrides."""
    payload = load_json(os.path.join(fixture_dir, "payload.json"))
    session = payload.get("session_id", "unknown")
    verdict = load_json(os.path.join(fixture_dir, "verdict.json"))

    tmp_home = tempfile.mkdtemp(prefix="hook-red-proof-home-")
    try:
        judge_dir = os.path.join(tmp_home, ".claude", "hooks", ".judge")
        os.makedirs(judge_dir, exist_ok=True)
        with open(os.path.join(judge_dir, session + ".json"), "w", encoding="utf-8") as f:
            json.dump(verdict, f)

        env = dict(os.environ)
        env["HOME"] = tmp_home
        proc = subprocess.run(
            interpreter_for(stem) + [hook_path],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        out = proc.stdout.strip()
        if not out:
            return False, "stdout was empty (exit %d); stderr: %s" % (proc.returncode, proc.stderr.strip()[:300])
        if contains not in out:
            return False, "stdout did not contain %r: %r" % (contains, out[:300])
        return True, "fired: stdout contains %r" % contains
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)


def main():
    decl = load_json(PROOFS_JSON)
    proofs = decl.get("proofs", {})
    cannot_red = decl.get("cannot_red", {})

    fail = 0
    print("check-hooks-can-fire: %d hook(s) to prove, %d classified cannot_red" % (len(proofs), len(cannot_red)))

    for stem, spec in sorted(proofs.items()):
        fixture_dir = os.path.join(FIXTURES_DIR, os.path.basename(spec["fixture"]))
        if not os.path.isdir(fixture_dir):
            print("check-hooks-can-fire: SILENT %s — no fixture directory at %s" % (stem, fixture_dir))
            fail = 1
            continue

        hook_path, used_fallback = resolve_hook_path(stem)
        if hook_path is None:
            print("check-hooks-can-fire: SILENT %s — not found under %s or %s"
                  % (stem, REPO_HOOKS_DIR, INSTALLED_HOOKS_DIR))
            fail = 1
            continue
        if used_fallback:
            print("check-hooks-can-fire: NOTE %s — no repo copy under %s; proving the installed copy "
                  "at %s instead" % (stem, REPO_HOOKS_DIR, hook_path))

        detect = spec.get("detect")
        try:
            if detect == "json-block":
                ok, detail = run_json_block_proof(stem, hook_path, fixture_dir)
            elif detect == "nonempty-contains":
                ok, detail = run_nonempty_contains_proof(stem, hook_path, fixture_dir, spec["contains"])
            else:
                ok, detail = False, "unknown detect mode %r in hook-red-proofs.json" % detect
        except subprocess.TimeoutExpired:
            ok, detail = False, "hook timed out"
        except Exception as e:  # a broken fixture or hook must be reported, never crash the runner silently
            ok, detail = False, "runner error: %r" % e

        if ok:
            print("check-hooks-can-fire: OK %s — %s" % (stem, detail))
        else:
            print("check-hooks-can-fire: SILENT %s — %s" % (stem, detail))
            fail = 1

    for stem, reason in sorted(cannot_red.items()):
        print("check-hooks-can-fire: CANNOT_RED %s — %s" % (stem, reason))

    if fail:
        print("check-hooks-can-fire: FAIL — at least one hook stayed silent against its own fixture.")
    else:
        print("check-hooks-can-fire: OK (every classified hook fired against its fixture).")
    return fail


if __name__ == "__main__":
    sys.exit(main())
