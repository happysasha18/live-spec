#!/usr/bin/env python3
"""check-every-gate-can-fail.py — every push gate carries a known-red proof (SPEC INV-212, gate w).

THE LAW behind it: a gate that cannot red is a check that looks at nothing — it reports green
because it never fires. This movement paid for the lesson: the authority-anchor gate shipped hollow
(commit 8a0209f rebuilt it), reporting green without reaching the surfaces it claimed to inspect,
and a worker's false "zero violations" was the same disease, a claim that protected nothing because
nothing could make it fail. So every gate the push chain runs must carry a KNOWN-RED PROOF: a
committed red-first test that drives that gate's own check to a non-zero exit, so the gate is shown
to fire. A gate with no such proof is itself the finding.

This check enumerates the gate letters guardrails/pre-push invokes — its "-- gate X:" markers, the
same enumeration check-ci-mirror.sh (gate u) reads — and requires each classified in
guardrails/gate-red-proofs.json as one of:

  * a "proof" — a red-first test `<file>::<function>` that drives the gate's check to red, tied to
    that gate by a `reds` token (usually the check's basename) the proof file must reference; or
  * "covered" — a gate that invokes no independent check of its own but rides another gate's red
    (gate c rides the pytest suite, gate b), declared with the reason it carries no separate fixture.

A registered proof is verified by reading its structure, since the suite already runs it under gate b
(exactly as check-ci-mirror.sh's own red-proof runs there): the proof file exists, the named function
is defined in it, the `reds` token appears in the file (tying the proof to this gate's check), and the
function body carries a non-zero-exit assertion, so a bare "the gate ships" presence test cannot pass
as a red proof.

A gate marker classified in none of the three maps reds — the self-widening teeth, so a gate added
later without a proof cannot slip through. A "covered" entry with no reason reds — papering over a
hollow gate is the one thing this gate exists to stop. And a gate that genuinely can never be made to
red by construction is a finding, not a carve-out: the "cannot_red" map exists so such a gate is named
loudly and reds this check, never silently waved through. A registry key naming a letter that is no
local gate is itself drift and reds, like a stale CI carve-out (INV-210).

This is the guard over the guards — a structural scan kin of config-health (INV-175) and the CI-mirror
gate (INV-210).
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

PREPUSH = os.environ.get("GATE_PROOFS_PREPUSH", os.path.join(REPO_ROOT, "guardrails", "pre-push"))
REGISTRY = os.environ.get("GATE_PROOFS_JSON", os.path.join(REPO_ROOT, "guardrails", "gate-red-proofs.json"))

GATE_MARKER = re.compile(r"-- gate ([a-z]{1,2}):")   # the chain outgrew one letter per gate

# A genuine non-zero-exit assertion, in the idioms the suite's red-proof tests use. It matches an
# assertion that the check FAILED (returncode 1/2, or not 0), or a call to a red-asserting helper.
# It deliberately does NOT match a green assertion (returncode 0) or a mere function name, so a bare
# presence test cannot pass as a red proof.
RED_ASSERT = re.compile(
    r"assert_red\(|expect_red\("
    r"|assertNotEqual\([^)\n]*(?:returncode|\bcode)\b[^)\n]*,\s*0\b"
    r"|assertEqual\([^)\n]*(?:returncode|\bcode)\b[^)\n]*,\s*[12]\b"
    r"|(?:returncode|\bcode)\s*!=\s*0\b"
    r"|(?:returncode|\bcode)\s*==\s*[12]\b"
)


def read(path):
    with open(path) as f:
        return f.read()


def gate_letters(prepush_text):
    return sorted(set(GATE_MARKER.findall(prepush_text)))


def function_body(src_text, fn):
    """The text of function `fn`: from its `def` line to the next def/class at the same or lower
    indent. Returns None if the function is not defined."""
    lines = src_text.splitlines()
    pat = re.compile(r"\bdef " + re.escape(fn) + r"\b")
    for i, line in enumerate(lines):
        if pat.search(line):
            indent = len(line) - len(line.lstrip())
            body = [line]
            for m in lines[i + 1:]:
                if m.strip() and (len(m) - len(m.lstrip())) <= indent and re.match(r"\s*(def |class )", m):
                    break
                body.append(m)
            return "\n".join(body)
    return None


def main():
    for f in (PREPUSH, REGISTRY):
        if not os.path.isfile(f):
            print("every-gate-can-fail: cannot read %s — the gate stands on both files." % f)
            return 1

    letters = gate_letters(read(PREPUSH))
    if not letters:
        print("every-gate-can-fail: no `-- gate X:` markers found in %s — the enumeration is empty, "
              "so the chain cannot be proven." % PREPUSH)
        return 1

    reg = json.loads(read(REGISTRY))
    proofs = reg.get("proofs", {})
    covered = reg.get("covered", {})
    cannot = reg.get("cannot_red", {})

    fail = 0

    # A registry key must name a real local gate — a stale key is drift, exactly like a stale CI
    # carve-out (INV-210).
    for section_name, section in (("proofs", proofs), ("covered", covered), ("cannot_red", cannot)):
        for k in section:
            if k not in letters:
                print("every-gate-can-fail: registry key '%s' in %s names no local pre-push gate — "
                      "remove the stale entry." % (k, section_name))
                fail = 1

    for g in letters:
        homes = [name for name, sec in
                 (("proofs", proofs), ("covered", covered), ("cannot_red", cannot)) if g in sec]

        if not homes:
            print("every-gate-can-fail: gate %s runs in pre-push but is classified in neither "
                  "proofs, covered, nor cannot_red of gate-red-proofs.json — add a red-first test "
                  "that drives its check to a non-zero exit and register it as a proof, or declare "
                  "it covered with the reason it rides another gate." % g)
            fail = 1
            continue
        if len(homes) > 1:
            print("every-gate-can-fail: gate %s is classified in more than one section (%s) — a "
                  "gate has one home in the registry." % (g, ", ".join(homes)))
            fail = 1
            continue

        home = homes[0]

        if home == "cannot_red":
            print("every-gate-can-fail: gate %s is declared cannot_red (%s) — a gate that by "
                  "construction can never fail guards nothing. This is a finding, not a pass: give "
                  "the gate a red-first test, or the gate has no reason to run." % (g, cannot[g]))
            fail = 1
            continue

        if home == "covered":
            reason = covered[g]
            if not (isinstance(reason, str) and reason.strip()):
                print("every-gate-can-fail: gate %s is declared covered but carries no reason — a "
                      "covered gate names the gate whose red it rides and why it holds no separate "
                      "fixture, so the line is settled rather than papered." % g)
                fail = 1
            continue

        # home == "proofs": verify the red proof by structure.
        entry = proofs[g]
        proof = entry.get("proof", "") if isinstance(entry, dict) else ""
        redtok = entry.get("reds", "") if isinstance(entry, dict) else ""

        if "::" not in proof:
            print("every-gate-can-fail: gate %s proof %r is not in `<file>::<function>` form." % (g, proof))
            fail = 1
            continue
        relfile, fn = proof.split("::", 1)
        fpath = os.path.join(REPO_ROOT, relfile)
        if not os.path.isfile(fpath):
            print("every-gate-can-fail: gate %s proof file %s does not exist." % (g, relfile))
            fail = 1
            continue
        src = read(fpath)
        if not re.search(r"\bdef " + re.escape(fn) + r"\b", src):
            print("every-gate-can-fail: gate %s proof function %s is not defined in %s." % (g, fn, relfile))
            fail = 1
            continue
        if not redtok or redtok not in src:
            print("every-gate-can-fail: gate %s proof %s carries the reds token %r, which does not "
                  "appear in %s — the proof is not tied to this gate's check, so it cannot be shown "
                  "to drive the right gate to red." % (g, fn, redtok, relfile))
            fail = 1
            continue
        body = function_body(src, fn)
        if not body or not RED_ASSERT.search(body):
            print("every-gate-can-fail: gate %s proof %s in %s carries no non-zero-exit assertion — "
                  "a red proof must drive the check to red (assert its returncode is 1/2 or not 0), "
                  "not merely assert the gate ships." % (g, fn, relfile))
            fail = 1
            continue

    if fail == 0:
        print("every-gate-can-fail: OK (every pre-push gate carries a known-red proof or a declared "
              "covered ride; %d gates checked)." % len(letters))
    return fail


if __name__ == "__main__":
    sys.exit(main())
