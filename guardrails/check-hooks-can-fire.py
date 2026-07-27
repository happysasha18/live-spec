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
  * "json-deny" — stdout parses as JSON carrying hookSpecificOutput.permissionDecision == "deny",
    the documented PreToolUse verdict shape (midturn-chat-scan.py). $HOME is isolated per run, since
    a PreToolUse scan that reports each offence once per session keeps state under $HOME.
  * "nonempty-contains" — stdout is non-empty and contains a named substring (register-judge-report.sh,
    a UserPromptSubmit hook that prints a plain reason line, not a decision object).

A hook that stays silent against a fixture built to trigger it is named and FAILS the whole run — the
same "a check that cannot fail is a check that watches nothing" law gate-red-proofs.json states for
push gates. Every entry under "cannot_red" is reported, never run, and never counted as a failure —
its reason is printed so the carve-out stays visible rather than silent.

REGISTRY CENSUS. Reading the two maps proves nothing about a hook that appears in neither. This runner
also reads guardrails/judge-hooks.json's "wired" list — every session hook a fresh install actually
turns on — and checks each one resolves to a file classified in "proofs" or "cannot_red". judge-hooks.json's
own "library" list (a shared reader, a shared mechanism, or an opt-in net a host turns on) is never
demanded; population is "wired" alone. A wired hook classified in neither map REDS the run by name.
A "proofs" or "cannot_red" key that names a file found under neither hooks directory also REDS.

Fixture shape: guardrails/hook-red-fixtures/<hook-stem>/payload.json (the JSON a hook reads on
stdin; a "transcript_path" value is a filename resolved relative to the fixture directory, rewritten
to an absolute path before the hook runs) plus, for a transcript-reading hook, transcript.jsonl (JSONL
transcript records). register-judge-report.sh's fixture instead carries verdict.json, the verdict
file content the runner pre-seeds under a temp $HOME so the real ~/.claude/hooks/.judge/ directory is
never touched.

Env overrides (for testing this runner itself, the same pattern check-judge-listed.py uses):
  HOOKS_PROOFS_JSON      - path to the declaration file (default guardrails/hook-red-proofs.json)
  HOOKS_JUDGE_HOOKS_JSON - path to the wired/library declaration (default guardrails/judge-hooks.json)
  HOOKS_REPO_DIR         - repo hooks/ directory (default <repo>/hooks)
  HOOKS_INSTALLED_DIR    - installed hooks directory (default ~/.claude/hooks)
  HOOKS_FIXTURES_DIR     - fixtures root (default guardrails/hook-red-fixtures)
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
JUDGE_HOOKS_JSON = os.environ.get("HOOKS_JUDGE_HOOKS_JSON", os.path.join(SCRIPT_DIR, "judge-hooks.json"))
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


def resolve_wired_stem(name):
    """judge-hooks.json's "wired" keys carry no extension; the shipped file may be a .py or a .sh
    script. Try both, resolving each candidate the same way resolve_hook_path already does for a
    proofs/cannot_red key. Returns (stem, hook_path) for whichever extension resolves, or (None, None)."""
    for ext in (".py", ".sh"):
        stem = name + ext
        hook_path, _ = resolve_hook_path(stem)
        if hook_path is not None:
            return stem, hook_path
    return None, None


def run_census(proofs, cannot_red):
    """The registry census: every hook guardrails/judge-hooks.json wires live must resolve to a file
    classified in "proofs" or "cannot_red". judge-hooks.json's own "library" list is the carve-out for
    a shared reader, a shared mechanism, or an opt-in net gate v never demands live, so population is
    the "wired" list alone. Returns (fail, classified_count, total_count, had_unresolved,
    had_unclassified) — the last two name which of the census's two red paths fired, for the closing
    summary line to report by name rather than by one shared word."""
    if not os.path.isfile(JUDGE_HOOKS_JSON):
        print("check-hooks-can-fire: census SKIPPED — no judge-hooks.json at %s" % JUDGE_HOOKS_JSON)
        return 0, 0, 0, False, False

    judge_decl = load_json(JUDGE_HOOKS_JSON)
    wired = judge_decl.get("wired", {})

    fail = 0
    had_unresolved = False
    had_unclassified = False
    classified_count = 0
    for name in sorted(wired):
        stem, _ = resolve_wired_stem(name)
        if stem is None:
            print("check-hooks-can-fire: UNRESOLVED %s — wired live in judge-hooks.json's \"wired\" "
                  "list but no .py or .sh file found under %s or %s"
                  % (name, REPO_HOOKS_DIR, INSTALLED_HOOKS_DIR))
            fail = 1
            had_unresolved = True
            continue
        if stem in proofs or stem in cannot_red:
            classified_count += 1
        else:
            print("check-hooks-can-fire: UNCLASSIFIED %s — wired live in judge-hooks.json's \"wired\" "
                  "list but classified in neither \"proofs\" nor \"cannot_red\"" % stem)
            fail = 1
            had_unclassified = True

    total = len(wired)
    print("check-hooks-can-fire: census %d/%d wired hook(s) classified (library-list carve-outs excluded)"
          % (classified_count, total))
    return fail, classified_count, total, had_unresolved, had_unclassified


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


def run_json_deny_proof(stem, hook_path, fixture_dir):
    """Run a PreToolUse hook and check its stdout carries the documented deny verdict.

    A PreToolUse hook states its verdict through hookSpecificOutput.permissionDecision, a different
    shape from the Stop family's top-level "decision": "block", so it is proven under its own mode.
    $HOME is isolated to a temp dir for the run: a PreToolUse scan that reports each offence once per
    session keeps a small state file under $HOME, and a census run against the real home would both
    write into it and go silent on its own second run.
    """
    payload = build_payload(fixture_dir)
    tmp_home = tempfile.mkdtemp(prefix="hook-red-proof-home-")
    try:
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
        try:
            verdict = json.loads(out)
        except ValueError:
            return False, "stdout did not parse as JSON: %r" % out[:300]
        body = verdict.get("hookSpecificOutput", {})
        if body.get("permissionDecision") != "deny":
            return False, "stdout carried no hookSpecificOutput.permissionDecision == \"deny\": %r" % out[:300]
        return True, "fired: permissionDecision=deny"
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)


def run_nonempty_contains_proof(stem, hook_path, fixture_dir, contains):
    """A UserPromptSubmit hook that prints a plain reason line unconditionally on stdout. When the
    fixture directory carries a verdict.json (register-judge-report.sh: pre-seed a verdict under an
    isolated temp $HOME so the hook's own VERDICT_DIR read finds it — the real ~/.claude/hooks/.judge/
    is never touched), it is pre-seeded first; a hook whose stdout depends on no such state
    (clock-hook.sh, chat-law-hook.sh print unconditionally) skips straight to running it. Either way
    $HOME is isolated to a temp dir for the run."""
    payload = load_json(os.path.join(fixture_dir, "payload.json"))
    session = payload.get("session_id", "unknown")
    verdict_path = os.path.join(fixture_dir, "verdict.json")

    tmp_home = tempfile.mkdtemp(prefix="hook-red-proof-home-")
    try:
        if os.path.isfile(verdict_path):
            verdict = load_json(verdict_path)
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
    had_silent = False
    had_missing_file = False
    print("check-hooks-can-fire: %d hook(s) to prove, %d classified cannot_red" % (len(proofs), len(cannot_red)))

    for stem, spec in sorted(proofs.items()):
        fixture_dir = os.path.join(FIXTURES_DIR, os.path.basename(spec["fixture"]))
        if not os.path.isdir(fixture_dir):
            print("check-hooks-can-fire: SILENT %s — no fixture directory at %s" % (stem, fixture_dir))
            fail = 1
            had_silent = True
            continue

        hook_path, used_fallback = resolve_hook_path(stem)
        if hook_path is None:
            print("check-hooks-can-fire: SILENT %s — not found under %s or %s"
                  % (stem, REPO_HOOKS_DIR, INSTALLED_HOOKS_DIR))
            fail = 1
            had_missing_file = True
            continue
        if used_fallback:
            print("check-hooks-can-fire: NOTE %s — no repo copy under %s; proving the installed copy "
                  "at %s instead" % (stem, REPO_HOOKS_DIR, hook_path))

        detect = spec.get("detect")
        try:
            if detect == "json-block":
                ok, detail = run_json_block_proof(stem, hook_path, fixture_dir)
            elif detect == "json-deny":
                ok, detail = run_json_deny_proof(stem, hook_path, fixture_dir)
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
            had_silent = True

    for stem, reason in sorted(cannot_red.items()):
        hook_path, _ = resolve_hook_path(stem)
        if hook_path is None:
            print("check-hooks-can-fire: SILENT %s — cannot_red entry names a file found under neither "
                  "%s nor %s" % (stem, REPO_HOOKS_DIR, INSTALLED_HOOKS_DIR))
            fail = 1
            had_missing_file = True
        else:
            print("check-hooks-can-fire: CANNOT_RED %s — %s" % (stem, reason))

    census_fail, _, _, had_unresolved, had_unclassified = run_census(proofs, cannot_red)
    fail = fail or census_fail

    if fail:
        # Each red path gets its own sentence, since one line naming only "silent" leaves an operator
        # hunting for a silent hook on the three paths where there is none to find.
        causes = []
        if had_silent:
            causes.append("a hook stayed silent against its own fixture")
        if had_unclassified:
            causes.append("a wired hook was classified in neither map")
        if had_unresolved:
            causes.append("a wired name resolved to no file")
        if had_missing_file:
            causes.append("a registry entry named a file found under neither hooks directory")
        print("check-hooks-can-fire: FAIL — " + "; ".join(causes) + ".")
    else:
        print("check-hooks-can-fire: OK (every classified hook fired against its fixture).")
    return fail


if __name__ == "__main__":
    sys.exit(main())
