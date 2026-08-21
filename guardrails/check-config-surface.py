#!/usr/bin/env python3
"""check-config-surface.py — the founding declares what the owner changes without a build (SPEC INV-291).

THE LAW. A project kind whose product is deployed carries a seam. On one side is the build: the
behaviour and the structure, everything that reaches production only by building the product again. On
the other side is the configuration: the values the shipped product already reads — an experiment
switch, a piece of copy, a threshold or budget, a feature toggle — which reach production by a deploy
of configuration alone. The founding names that seam once, on a `project.config-surface` line in the
host profile, beside the kind, the layers, the proofs, the design principles, and the composition axes
(INV-135, INV-136, INV-244). A host that deploys nothing answers an explicit "none" and passes; a host
that records a kind and says nothing at all reds.

WHY THE CHECK HOLDS PRESENCE AND SELF-CONSISTENCY, AND NOT THE CLASSIFICATION. Which kinds are
deployed is a judgment, and its home is the per-kind design-principles table in ARCHITECTURE.md, which
a founding reads and answers from. So this gate carries no list of kinds: it reads the host's own two
declarations and reports where they are missing or where they disagree. A list of kinds in check code
would be the literal-list design the base rulebook already names as the wrong answer to a class.

THE THREE ARMS.

  A. silence — the profile records `project.kind` and carries no `project.config-surface` record.
     A deployed kind is the case the row was opened for; a kind that deploys nothing clears this arm
     by writing its explicit "none", which is present text.
  B. empty — the record exists and carries no words. A key with nothing after it declares nothing.
  C. contradiction — the record answers "none" while the host's own `project.layers` line names a
     deployment layer. Two declarations of the same host disagree, and the report quotes both.

NOT MECHANICALLY CHECKED, and reported rather than skipped in silence: whether the declared surface
really reaches production with no build. No script can read a host's deploy pipeline from one profile
line, so the founding conversation and the proof by deed hold that half — the owner turns a switch in
production and no build runs.

REACH (INV-269). This gate opens two files: the host profile named on the command line (default from
the config) and its config `guardrails/config-surface.json`. Inside the profile it reads three
records — `project.kind`, `project.layers`, `project.config-surface` — and nothing else.

STANDING. It rides the suite and stays off the push chain, the standing suite-riding placement
INV-225 already carries: the pack ships no deployed product of its own, so the gate has a host's
profile to read and no push of this repo to block.

Usage:
  check-config-surface.py [<host-profile.md>]
  CONFIG_SURFACE_JSON overrides the config path (the suite points it at a missing file for the red).
Exit 0 on a complete founding, printing the reach line; 1 on a finding; 2 on a usage error.
Stdlib only.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.environ.get("CONFIG_SURFACE_JSON",
                             os.path.join(SCRIPT_DIR, "config-surface.json"))
CHECK = "check-config-surface"

RECORD_START = re.compile(r"^\s*[-*]\s+`?[A-Za-z][\w.-]*\s*:")


def _record(text, key):
    """The whole record for one profile key: its line plus the lines it wraps onto.

    A record ends at the first blank line or at the next record's opening line, so a profile that
    writes each declaration as one wrapped bullet reads back as one record.
    """
    opener = re.compile(r"^\s*[-*]?\s*`?%s\s*:" % re.escape(key))
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if opener.search(line):
            start = i
            break
    if start is None:
        return None, None
    out = [lines[start]]
    for line in lines[start + 1:]:
        if not line.strip() or RECORD_START.search(line):
            break
        out.append(line)
    return start + 1, "\n".join(out)


def _value(record, key):
    """The declaration's own text: everything after the key's colon, backticks stripped."""
    body = re.split(r"%s\s*:" % re.escape(key), record, maxsplit=1)[-1]
    return body.replace("`", " ").strip()


def _is_none_answer(value, none_answers):
    m = re.search(r"[A-Za-z]+", value)
    return bool(m) and m.group(0).lower() in [w.lower() for w in none_answers]


def _names_a_deployment_layer(layers_value, deploy_words):
    for word in deploy_words:
        if re.search(r"\b%s\b" % re.escape(word), layers_value, re.IGNORECASE):
            return word
    return None


def _first_line(record):
    return " ".join(record.splitlines()[0].split())


def check(profile_text, cfg):
    """Returns (findings, facts). A finding is one human sentence; facts feed the reach line."""
    kind_key = cfg["kind_key"]
    layers_key = cfg["layers_key"]
    decl_key = cfg["declaration_key"]

    kind_no, kind_rec = _record(profile_text, kind_key)
    decl_no, decl_rec = _record(profile_text, decl_key)
    layers_no, layers_rec = _record(profile_text, layers_key)
    facts = {"kind": kind_no, "layers": layers_no, "declaration": decl_no}

    if kind_rec is None:
        return [], facts  # no kind recorded — no founding to complete yet

    if decl_rec is None:
        return ["%s:%s records `%s` and declares no `%s`. Name what the owner can change without a "
                "build, where those values live, and how a change reaches production; a project that "
                "deploys nothing writes an explicit \"none\" and passes."
                % (cfg["_path"], kind_no, kind_key, decl_key)], facts

    value = _value(decl_rec, decl_key)
    if not re.search(r"[A-Za-z]", value):
        return ["%s:%s carries `%s` with no declaration after it. A key with nothing after it "
                "declares nothing." % (cfg["_path"], decl_no, decl_key)], facts

    findings = []
    if _is_none_answer(value, cfg["none_answers"]) and layers_rec is not None:
        layers_value = _value(layers_rec, layers_key)
        word = _names_a_deployment_layer(layers_value, cfg["deploy_words"])
        if word:
            findings.append(
                "%s: the two declarations disagree. `%s` answers \"none\", while `%s` names a "
                "deployment layer (%s).\n      line %s: %s\n      line %s: %s\n      A project with "
                "a deployment layer runs somewhere its readers reach; name the values its owner "
                "turns there without a build, or drop the deployment layer from the layers line."
                % (cfg["_path"], decl_key, layers_key, word,
                   decl_no, _first_line(decl_rec), layers_no, _first_line(layers_rec)))
    return findings, facts


def _at(line_no):
    return "line %d" % line_no if line_no else "absent"


def _reach_line(path, cfg, facts):
    return ("%s: reach: files=[%s, %s]; read the `%s` (%s), `%s` (%s), and `%s` (%s) records of the "
            "profile alone; no other line and no other file is in this gate's reach."
            % (CHECK, os.path.basename(path), os.path.basename(CONFIG_PATH),
               cfg["kind_key"], _at(facts["kind"]),
               cfg["layers_key"], _at(facts["layers"]),
               cfg["declaration_key"], _at(facts["declaration"])))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) > 1:
        print("%s: usage: %s [<host-profile.md>]" % (CHECK, os.path.basename(argv[0])))
        return 2
    if not os.path.isfile(CONFIG_PATH):
        print("%s: no config at %s — the gate reads its keys and its word lists from that file "
              "(INV-291)." % (CHECK, CONFIG_PATH))
        return 1
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    for key in ("kind_key", "layers_key", "declaration_key", "none_answers", "deploy_words"):
        if key not in cfg:
            print("%s: the config at %s declares no %s — every word this gate reads lives in that "
                  "file." % (CHECK, CONFIG_PATH, key))
            return 1

    path = args[0] if args else os.path.join(REPO_ROOT, cfg.get("profile_default",
                                                                ".live-spec/profile.md"))
    if not os.path.isfile(path):
        print("%s: cannot read %s — the gate stands on the host profile, and a profile it cannot "
              "open is a red, never a silent pass." % (CHECK, path))
        return 1
    with open(path, encoding="utf-8") as f:
        profile_text = f.read()

    cfg["_path"] = os.path.basename(path)
    findings, facts = check(profile_text, cfg)
    if findings:
        print("%s: the founding's configuration-surface declaration does not hold — %d %s (SPEC "
              "INV-291)." % (CHECK, len(findings),
                             "finding" if len(findings) == 1 else "findings"))
        for finding in findings:
            print("   - %s" % finding)
        print(_reach_line(path, cfg, facts))
        return 1
    print("%s: the founding's configuration surface stands (SPEC INV-291)." % CHECK)
    print(_reach_line(path, cfg, facts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
