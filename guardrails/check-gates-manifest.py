#!/usr/bin/env python3
"""check-gates-manifest.py — gate af: the gate device has one home, and a CI mirror step cannot
silently restate a gate's law (SPEC INV-210/INV-212).

BLOCKING (guardrails/README.md convention 2): a fault exits non-zero and carries the contract's one
typed JSON line beside its human lines. It writes nothing at all, so convention 3 holds by having no
output to half-write.

THE LAW behind it: guardrails/pre-push carries every gate's device — its letter, its script, its SPEC
anchor, and the one sentence stating its law. Two more places carry a SECOND, hand-typed copy of that
law sentence: .github/workflows/gates.yml (for the CI reader) and guardrails/README.md's generated
roster (built FROM pre-push by scripts/gen-tree-counts.py, so it cannot drift from it). Nothing before
this gate ever compared gates.yml's copy against pre-push's own — guardrails/check-ci-mirror.sh (gate
u) compares LETTER SETS only, never the sentence beside a letter. Gate ad's law sentence drifted
between pre-push and gates.yml for over a month as a result: pre-push says a published count "matches
the tree, and the reproduction command beside it returns the published number"; gates.yml said only "is
built from the tree" — a materially narrower claim that named ARM ONE of the gate and left ARM TWO
unstated, and nothing red.

guardrails/gates-manifest.json is the fix: it holds ONE canonical copy of every gate's law (read
straight from pre-push, so it is never hand-typed), joined with the gate's script, its red proof
(guardrails/gate-red-proofs.json), and whether it is mirrored to CI and why not where it stands down
(guardrails/ci-mirror.json). This gate runs two arms:

ARM ONE — the manifest is generated, never hand-edited. A fresh build of the manifest
(scripts/gen-gates-manifest.py, run in-process so no second copy of the join logic can drift from
the one this gate calls) must equal the committed guardrails/gates-manifest.json exactly. A hand edit
to the manifest, or a change to any of its four sources with the manifest left stale, reds here —
exactly the shape check-tree-counts.py (gate ad) and check-index-generated.py (gate x) already hold
their own generated artifacts to.

ARM TWO — a mirrored gate's CI step states the same law pre-push does. For every `.github/workflows
/gates.yml` step whose name reads `gate X — LAW...`, LAW must equal the manifest's `law` field for
gate X, verbatim. This is the arm the living finding above shows was missing: it is what would have
caught gate ad's drift the day gates.yml's copy first went stale, rather than a month later by an
outside read. A step whose name does not open with `gate X — ` (gate b's CI step, which legitimately
runs the suite differently than the local reach-scoped chain and says so in its own name) is not held
to this arm — it carries no second copy of the law to compare.

WHAT IT DOES NOT CLAIM. It does not generate any gate's executable check — pre-push stays the one live
script that runs every gate, gate b's reach-scoped local chain and gate g's own skip function
unsimplified. It does not touch guardrails/README.md's prose notes on 15 of the 28 gates: those are a
person's own commentary, not a second copy of the law, and stay outside every mechanical net by the
project's own stated choice.

Usage:
  check-gates-manifest.py [--root DIR]
Exit 0 where the committed manifest matches a fresh build and every mirrored gate's CI text matches
the manifest; exit 1 naming each fault. Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — green_reach, the gate family's shared verdict line

CHECK = "check-gates-manifest"

MANIFEST_REL = "guardrails/gates-manifest.json"
GENERATOR_REL = "scripts/gen-gates-manifest.py"

# A gates.yml step name reading `gate X — LAW...` — the shape a mirrored gate's step is held to.
# `- +` accepts an em dash or a hyphen, matching either house style already in the file.
CI_STEP_LAW_RE = re.compile(r"- name: gate ([a-z]{1,2}) [—-] (.+)")


def load_generator(root):
    """Load scripts/gen-gates-manifest.py by path, so this gate calls the ONE join builder rather
    than holding a second copy of the join logic that could itself drift from it."""
    path = os.environ.get("GATES_MANIFEST_GENERATOR", os.path.join(root, GENERATOR_REL))
    spec = importlib.util.spec_from_file_location("gen_gates_manifest", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def diff_summary(fresh, committed):
    """The letters a fresh build and the committed manifest disagree about, or that only one side
    carries — kept short so a red line names the disagreement rather than reprinting both files."""
    fresh_gates = fresh.get("gates", {})
    committed_gates = committed.get("gates", {})
    problems = []
    for letter in sorted(set(fresh_gates) | set(committed_gates), key=lambda l: (len(l), l)):
        if letter not in committed_gates:
            problems.append("gate %s stands in a fresh build but not in the committed manifest" % letter)
            continue
        if letter not in fresh_gates:
            problems.append("gate %s stands in the committed manifest but no fresh build produces it "
                            "(a stale entry, or a gate pre-push no longer runs)" % letter)
            continue
        if fresh_gates[letter] != committed_gates[letter]:
            problems.append("gate %s's committed entry differs from a fresh build: %s"
                            % (letter, fresh_gates[letter]))
    return problems


def check_ci_text(manifest, gates_yml_text):
    """ARM TWO: every `gate X — LAW` step in gates.yml states the same law the manifest (and so
    pre-push) does. Returns a list of problems."""
    problems = []
    gates = manifest.get("gates", {})
    for m in CI_STEP_LAW_RE.finditer(gates_yml_text):
        letter, ci_law = m.group(1), m.group(2).strip()
        if letter not in gates:
            problems.append(".github/workflows/gates.yml names gate %s, which the manifest does not "
                            "carry — run %s" % (letter, GENERATOR_REL))
            continue
        canon_law = gates[letter]["law"]
        if ci_law != canon_law:
            problems.append(
                "gate %s's CI step states a different law than pre-push does:\n"
                "      gates.yml : %s\n"
                "      pre-push  : %s" % (letter, ci_law, canon_law))
    return problems


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description="Hold the gate device to one home.")
    parser.add_argument("--root", default=REPO_ROOT, help="read the tree under this directory")
    args = parser.parse_args(argv[1:])
    root = os.path.abspath(args.root)

    manifest_path = os.environ.get("GATES_MANIFEST_FILE", os.path.join(root, MANIFEST_REL))
    gates_yml_path = os.environ.get("GATES_MANIFEST_GATES_YML",
                                    os.path.join(root, ".github", "workflows", "gates.yml"))

    def red(problems, fix):
        print("%s: %d fault(s):" % (CHECK, len(problems)))
        for problem in problems:
            print("  - %s" % problem)
        print(json.dumps({
            "severity": "error",
            "code": "gates-manifest",
            "message": "%d fault(s) in the gate device's single home: %s"
                       % (len(problems), " | ".join(p.replace("\n", " ") for p in problems)),
            "fix": fix,
        }))
        return 1

    try:
        gen = load_generator(root)
    except Exception as e:
        return red(["cannot load %s: %s" % (GENERATOR_REL, e)],
                   "repair %s so it imports cleanly." % GENERATOR_REL)

    try:
        fresh = gen.build_manifest(root=root)
    except gen.BuildError as e:
        return red([str(e)],
                   "repair the source named above; the manifest is built from pre-push, "
                   "gate-red-proofs.json, ci-mirror.json and gates.yml, in that order of blame.")

    if not os.path.isfile(manifest_path):
        return red(["no manifest stands at %s" % os.path.relpath(manifest_path, root)],
                   "run `python3 %s` to write it." % GENERATOR_REL)
    try:
        with open(manifest_path, encoding="utf-8") as f:
            committed = json.load(f)
    except ValueError as e:
        return red(["%s does not parse as JSON: %s" % (MANIFEST_REL, e)],
                   "run `python3 %s` to rebuild it." % GENERATOR_REL)

    problems = diff_summary(fresh, committed)
    if problems:
        return red(problems, "run `python3 %s` to rebuild the manifest from its four sources, "
                             "and commit the result." % GENERATOR_REL)

    if not os.path.isfile(gates_yml_path):
        return red(["no CI workflow stands at %s" % os.path.relpath(gates_yml_path, root)],
                   "restore .github/workflows/gates.yml.")
    gates_yml_text = read(gates_yml_path)
    problems = check_ci_text(committed, gates_yml_text)
    if problems:
        return red(problems,
                   "edit the gates.yml step name to state the same law pre-push's `-- gate X: ...` "
                   "marker does, verbatim — copy it rather than re-describing the gate by hand.")

    print(sf.green_reach(CHECK, [MANIFEST_REL, ".github/workflows/gates.yml"],
                         len(committed["gates"]), len(committed["gates"]),
                         "gates joined: %d; CI law sentences checked against the manifest: %d"
                         % (len(committed["gates"]), len(CI_STEP_LAW_RE.findall(gates_yml_text)))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
