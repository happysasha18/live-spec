#!/usr/bin/env python3
"""gen-gates-manifest.py — build guardrails/gates-manifest.json, the one join of every push gate's
device, from the four places that already state it.

WHY THIS EXISTS. The push gate's device — which script a letter runs, what SPEC anchor it answers to,
which test proves it can fail, whether it is mirrored to CI and why not where it isn't, and the one
sentence naming its law — is written by hand in five places today: `guardrails/pre-push` (the letter,
the script, the law sentence, the SPEC anchor), `.github/workflows/gates.yml` (a second, hand-typed
copy of the law sentence, for the CI reader), `guardrails/gate-red-proofs.json` (the red proof),
`guardrails/ci-mirror.json` (the CI carve-outs), and `guardrails/README.md`'s generated roster (a third
copy of the law sentence, built from pre-push). Nothing ever compared the three copies of the law
sentence to each other — `guardrails/check-ci-mirror.sh` (gate u) compares LETTER SETS only. Gate ad's
law sentence drifted between all three: pre-push and the generated README roster say a published count
"matches the tree, and the reproduction command beside it returns the published number"; gates.yml
says only "is built from the tree" — a materially narrower claim, silently wrong for over a month.

THIS SCRIPT is a BUILDER, not a gate, the sibling of `scripts/build-matrix-reference.py` and
`scripts/gen-tree-counts.py`. It writes nothing that pre-push, gates.yml, gate-red-proofs.json or
ci-mirror.json do not already state; it joins them. `guardrails/check-gates-manifest.py` (gate af) is
the gate: it reds where a fresh build of this join differs from the committed manifest (so the
manifest can never be hand-edited out of step with its four sources), and it reds where a gates.yml
step's law sentence differs from the gate's own — the check the "living finding" above shows was
missing.

pre-push stays the live script it is; nothing here parses it into a runnable form, generates its
control flow, or replaces `-- gate X: ... --` as the place a gate's law is first written. This script
only reads that line back, the same way `scripts/gen-tree-counts.py` reads `guardrails/pre-push` for
its gate-roster count and never runs it.

Usage:
  gen-gates-manifest.py               # rebuild guardrails/gates-manifest.json in place
  gen-gates-manifest.py --print       # print the built manifest to stdout instead of writing
Exit 0 after writing (or printing); exit 1 naming what refused to build. Stdlib only.
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

PREPUSH_REL = "guardrails/pre-push"
PROOFS_REL = "guardrails/gate-red-proofs.json"
CI_MIRROR_REL = "guardrails/ci-mirror.json"
GATES_YML_REL = ".github/workflows/gates.yml"
MANIFEST_REL = "guardrails/gates-manifest.json"

GATE_MARKER_RE = re.compile(r"-- gate ([a-z]{1,2}): ([^\n]*?) --")
SPEC_TOKEN_RE = re.compile(r"SPEC ([A-Za-z0-9/.\-]+)\)?\s*$")
GUARDRAILS_SCRIPT_RE = re.compile(r"\$GUARDRAILS/([A-Za-z0-9_./-]+\.(?:sh|py))")
SCAFFOLD_SCRIPT_RE = re.compile(r"\$REPO_ROOT/(scaffold/[A-Za-z0-9_./${}-]+)")
HOSTCHECK_LOOP_RE = re.compile(r"for hostcheck in ([^;]+); do")
CI_YML_LETTER_RE = re.compile(r"gate ([a-z]{1,2})")


class BuildError(Exception):
    """The manifest refused to build. Raised before anything is written."""


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        raise BuildError("cannot read %s: %s" % (path, e))


# --- pre-push: the letter, the law sentence, the SPEC anchor, the script(s) --------------------

def gate_segments(prepush_text):
    """Every gate letter mapped to the text run between its own marker and the next one (or EOF) —
    the block of pre-push that letter's marker introduces, which is what a gate's own commands
    (and no other gate's) live inside."""
    marks = [(m.group(1), m.start()) for m in GATE_MARKER_RE.finditer(prepush_text)]
    if not marks:
        raise BuildError("no `-- gate X:` markers found in %s" % PREPUSH_REL)
    segments = {}
    for i, (letter, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(prepush_text)
        # a letter may legitimately mark more than one echo (none does today); concatenate if so.
        segments[letter] = segments.get(letter, "") + prepush_text[start:end]
    return segments


def gate_laws(prepush_text):
    """Every gate letter mapped to its law sentence, verbatim, exactly as `-- gate X: ... --`
    states it — the one canonical formulation this manifest exists to give a single home."""
    laws = {}
    for m in GATE_MARKER_RE.finditer(prepush_text):
        letter, law = m.group(1), m.group(2).strip()
        if letter in laws and laws[letter] != law:
            raise BuildError("gate %s carries two different `-- gate %s:` marker texts in %s"
                             % (letter, letter, PREPUSH_REL))
        laws[letter] = law
    return laws


def gate_spec(law):
    """The SPEC anchor token trailing a law sentence, or None where the sentence states none (gates
    c and e today: their law is stated with no SPEC token on this line)."""
    m = SPEC_TOKEN_RE.search(law)
    return m.group(1) if m else None


def gate_scripts(segment_text):
    """Every guardrail script this gate's own segment invokes, in the order it names them, deduped.

    Reads two shapes: a direct `$GUARDRAILS/check-*.(sh|py)` call, and gate h's dynamic
    `scaffold/guardrails/check_${hostcheck}.py` loop, resolved against the loop's own literal word
    list so the manifest names the four real files rather than the unresolved template.
    """
    scripts = []
    for m in GUARDRAILS_SCRIPT_RE.finditer(segment_text):
        rel = "guardrails/" + m.group(1)
        if rel not in scripts:
            scripts.append(rel)
    loop = HOSTCHECK_LOOP_RE.search(segment_text)
    if loop:
        for word in loop.group(1).split():
            rel = "scaffold/guardrails/check_%s.py" % word
            if rel not in scripts:
                scripts.append(rel)
    for m in SCAFFOLD_SCRIPT_RE.finditer(segment_text):
        rel = m.group(1)
        if "${" in rel:
            continue  # the unresolved loop template; the resolved names above already stand in
        if rel not in scripts:
            scripts.append(rel)
    return scripts


# --- CI mirror status: gates.yml presence, ci-mirror.json's declared carve-outs -----------------

def ci_mirrored_letters(gates_yml_text):
    """Every gate letter `.github/workflows/gates.yml` names in a step's `name:` line — the same
    read `guardrails/check-ci-mirror.sh` performs for gate u, so "mirrored" here can never disagree
    with what gate u already treats as mirrored."""
    letters = set()
    for line in gates_yml_text.splitlines():
        if "name:" in line and "gate " in line:
            letters.update(CI_YML_LETTER_RE.findall(line))
    return letters


# --- the join -------------------------------------------------------------------------------------

def build_manifest(prepush_path=None, proofs_path=None, ci_mirror_path=None, gates_yml_path=None,
                   root=REPO_ROOT):
    prepush_path = prepush_path or os.path.join(root, PREPUSH_REL)
    proofs_path = proofs_path or os.path.join(root, PROOFS_REL)
    ci_mirror_path = ci_mirror_path or os.path.join(root, CI_MIRROR_REL)
    gates_yml_path = gates_yml_path or os.path.join(root, GATES_YML_REL)

    prepush_text = read(prepush_path)
    proofs_reg = load_json(proofs_path)
    ci_mirror_reg = load_json(ci_mirror_path)
    gates_yml_text = read(gates_yml_path)

    laws = gate_laws(prepush_text)
    segments = gate_segments(prepush_text)
    ci_letters = ci_mirrored_letters(gates_yml_text)
    carve = ci_mirror_reg.get("ci_excluded", {})
    proofs = proofs_reg.get("proofs", {})
    covered = proofs_reg.get("covered", {})
    cannot_red = proofs_reg.get("cannot_red", {})

    gates = {}
    for letter in sorted(laws, key=lambda l: (len(l), l)):
        law = laws[letter]
        mirrored = letter in ci_letters
        reason = carve.get(letter)
        if mirrored and reason is not None:
            raise BuildError("gate %s is both mirrored in %s and carved out in %s — a gate is one "
                             "or the other" % (letter, GATES_YML_REL, CI_MIRROR_REL))
        if not mirrored and reason is None:
            raise BuildError("gate %s is mirrored in neither %s nor %s — this is what "
                             "check-ci-mirror.sh (gate u) exists to catch; run it first"
                             % (letter, GATES_YML_REL, CI_MIRROR_REL))

        if letter in proofs:
            proof_kind, proof_value = "proof", proofs[letter]
        elif letter in covered:
            proof_kind, proof_value = "covered", covered[letter]
        elif letter in cannot_red:
            proof_kind, proof_value = "cannot_red", cannot_red[letter]
        else:
            raise BuildError("gate %s is classified in none of proofs/covered/cannot_red in %s — "
                             "this is what check-every-gate-can-fail.py (gate w) exists to catch; "
                             "run it first" % (letter, PROOFS_REL))

        gates[letter] = {
            "spec": gate_spec(law),
            "law": law,
            "scripts": gate_scripts(segments.get(letter, "")),
            "mirrored": mirrored,
            "mirror_reason": reason,
            "proof_kind": proof_kind,
            "proof": proof_value,
        }

    return {
        "_comment": (
            "The one join of every push gate's device (SPEC INV-210/INV-212). Generated by "
            "scripts/gen-gates-manifest.py from the four places that already state each part by "
            "hand: guardrails/pre-push (letter, law sentence, SPEC anchor, script), "
            "guardrails/gate-red-proofs.json (red proof), guardrails/ci-mirror.json (CI carve-out), "
            "and .github/workflows/gates.yml (whether the letter is mirrored). No field here is "
            "typed by a person — this file is output only, exactly like guardrails/tree-counts.json's "
            "generated blocks, and guardrails/check-gates-manifest.py (gate af) reds a committed copy "
            "that differs from a fresh build, or a gates.yml step whose law sentence differs from the "
            "`law` field here. It does NOT generate any gate's executable check: pre-push stays the "
            "live script that runs every gate, unsimplified."
        ),
        "generated_from": [PREPUSH_REL, PROOFS_REL, CI_MIRROR_REL, GATES_YML_REL],
        "gates": gates,
    }


def render(manifest):
    return json.dumps(manifest, indent=2, sort_keys=False, ensure_ascii=False) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description=__doc__)
    parser.add_argument("--root", default=REPO_ROOT)
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="print the built manifest to stdout instead of writing it")
    args = parser.parse_args(argv[1:])
    try:
        manifest = build_manifest(root=args.root)
        text = render(manifest)
    except BuildError as e:
        print("gen-gates-manifest: nothing written — %s" % e)
        return 1
    if args.print_only:
        sys.stdout.write(text)
        return 0
    out_path = os.path.join(args.root, MANIFEST_REL)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("gen-gates-manifest: wrote %s (%d gates)" % (out_path, len(manifest["gates"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
