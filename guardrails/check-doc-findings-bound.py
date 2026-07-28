#!/usr/bin/env python3
"""check-doc-findings-bound.py — gate aa: no live document carries more findings than its record.

THE LAW (the owner's word, 2026-07-28 evening): a document repaired to zero stays at zero, on every
push, with no exception. A document still carrying findings never carries more than it did. The
direction of the count is down and never up.

WHAT IT READS. `guardrails/rule-census.json` holds one entry per live document with the count recorded
when it was last measured. `scripts/rule-census.py` measures the live set the same way for both, so the
record and the measure can never drift apart in method.

THE THREE VERDICTS.

  (a) measured == recorded, and recorded is 0  -> pass, and the document is named as held clean.
  (b) measured  < recorded                     -> pass, and the gate prints the re-seed command, so the
      lower number becomes the new ceiling rather than leaving headroom the next edit can spend.
  (c) measured  > recorded                     -> RED. A document recorded at 0 reds on its first
      finding, which is the uncompromising half of the law.

A live document missing from the record also reds: a new document is measured and recorded before it
can pass, so nothing enters the tree unmeasured.

WHY IT SITS AT THE PUSH. The census is a report and reports do not refuse anything. Between the morning
of 2026-07-28 and that evening one page rose from 107 findings to 112 with nothing noticing. This gate
is what noticing looks like.

THE SECOND ARM: THE RECORD ITSELF (SPEC INV-301, R302.11 to R302.15). The verdicts above hold the law
over the DOCUMENTS. The record is a file a person can edit, so this arm holds the law over the RECORD.
It reads the record against the copy the base commit holds and reds an entry whose recorded count rose
with no reason beside it. A raise is lawful when the entry carries a non-empty `reason` field, which is the
shape `guardrails/doc-bounds.json` already uses for a raised byte ceiling; inventing a second shape for
one idea is what the pack's one-home rule forbids. The writing arm lives in `scripts/rule-census.py`,
which refuses to store a rise at all, so between the two of them the printed remedy can only lower a
number.

WHY THIS ARM SITS HERE AND NOT UNDER A GATE LETTER OF ITS OWN. One law takes one gate letter. Gate aa
already owns "a recorded count moves down alone", and the record is the other half of that one law, so a
new letter would owe an entry in `guardrails/gate-red-proofs.json` for a fact this gate already stands
for. The arm's own red proof rides gate aa's registered entry.

WHICH COPY IT READS AGAINST, AND WHY NOT `HEAD`. This gate runs from `guardrails/pre-push` and from the
CI mirror, and at both of those moments the raise is ALREADY COMMITTED. An arm comparing the working
folder against `HEAD` therefore reads two copies that agree, prints nothing, and passes every real push;
it reaches an uncommitted edit alone, and a push never carries one. The honest ground for a gate on the
push chain is the state the REMOTE ALREADY HOLDS, so the arm reads the record against a BASE COMMIT.

HOW THE BASE COMMIT IS RESOLVED. Through the same ladder `guardrails/check-prover-record.sh` reads, so
one idea keeps one shape: the environment value `LIVE_SPEC_DIFF_BASE` where it resolves to a commit (CI
passes the push event's base commit, a planted test passes its own), then `origin/main`, then the commit
before the tip. A fourth rung follows the first three: the TIP ITSELF, which is the only copy a
repository holding one commit and no upstream can reach, and which keeps the arm's reach over an
uncommitted hand edit in such a tree. Each run names the rung it read, so the arm's ground is visible.

HOW IT READS THAT COPY. It asks git, through `git rev-parse --show-toplevel` beside the record and then
`git show <base>:<path>`. Where git answers nothing — no repository, no commit yet, no copy of that
record at the base, or a copy that will not parse — the arm STANDS DOWN BY NAME and says what it read
nothing of (INV-218's shape). That covers a fresh clone, a machine with no network, and the first push
of a branch whose base holds no record; none of them is evidence of a raise, and the document arm above
still holds. The CI mirror answers the same question the same way: `.github/workflows/gates.yml` hands
gate aa the event's base commit in `LIVE_SPEC_DIFF_BASE`, and a pull request with no such value falls to
`origin/main`, which the full-depth checkout carries.

WHY AN UNCHANGED RECORD IS SILENT. The arm speaks only of an entry whose recorded count ROSE against the
base copy. A record identical to that copy yields no such entry, so the arm prints nothing and the
gate's verdict is the document arm's alone. A gate that reds on an unchanged tree blocks every push in
the repository, which is the failure this silence avoids.

Usage:
  check-doc-findings-bound.py                    push mode: the repository's own record and live set.
  check-doc-findings-bound.py --record FILE      read the record from FILE (fixtures).
  check-doc-findings-bound.py --root DIR         measure the live set under DIR (fixtures).
Exit 0 when every document sits at or under its record and no recorded count rose by hand with no
reason; exit 1 naming each document that rose and each record entry raised without one.
Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CENSUS = os.path.join(REPO_ROOT, "scripts", "rule-census.py")
RECORD = os.path.join(REPO_ROOT, "guardrails", "rule-census.json")

CHECK = "doc-findings-bound"
# The base the record is read against, named the way `guardrails/check-prover-record.sh` names it.
BASE_ENV = "LIVE_SPEC_DIFF_BASE"
EMPTY_SHA = "0" * 40


def load_census():
    """The census module itself, so the gate and the report measure by one definition."""
    spec = importlib.util.spec_from_file_location("rule_census", CENSUS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_commit(top):
    """The commit the record is read against, by the ladder the prover-record gate already reads.

    `LIVE_SPEC_DIFF_BASE` where it resolves, then `origin/main`, then the commit before the tip, then
    the tip itself. Returns the ref name, or None where the repository holds no commit at all.
    """
    ladder = []
    stated = (os.environ.get(BASE_ENV) or "").strip()
    if stated and stated != EMPTY_SHA:
        ladder.append(stated)
    ladder += ["origin/main", "HEAD~1", "HEAD"]
    for ref in ladder:
        proc = subprocess.run(["git", "-C", top, "rev-parse", "--verify", "--quiet",
                               "%s^{commit}" % ref], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            return ref
    return None


def base_record(path):
    """The record's `files` as the base commit holds it, or a note saying what git answered nothing of.

    Returns (files, ref, None) on success and (None, ref, note) where no base copy can be read.
    """
    # The real path on both sides: git answers with symlinks resolved, and a temporary directory under
    # /var on this platform is reached through one, which would otherwise make the two paths disagree.
    real = os.path.realpath(path)
    directory = os.path.dirname(real) or "."
    try:
        top = subprocess.run(["git", "-C", directory, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True).stdout.strip()
    except OSError as e:
        return None, None, "no git command answered here (%s)" % e
    if not top:
        return None, None, "no git repository holds %s" % path
    ref = base_commit(top)
    if not ref:
        return None, None, "no commit in %s holds a record to read against" % top
    rel = os.path.relpath(real, os.path.realpath(top))
    proc = subprocess.run(["git", "-C", top, "show", "%s:%s" % (ref, rel)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return None, ref, "%s holds no copy of %s" % (ref, rel)
    try:
        return json.loads(proc.stdout)["files"], ref, None
    except (ValueError, KeyError) as e:
        return None, ref, "the copy of %s at %s would not be read (%s)" % (rel, ref, e)


def hand_raises(recorded, base):
    """Every entry whose recorded count rose against the base copy while carrying no reason."""
    out = []
    for rel, entry in sorted(recorded.items()):
        was = base.get(rel)
        if not isinstance(was, dict) or not isinstance(entry, dict):
            continue
        if entry.get("total", 0) <= was.get("total", 0):
            continue
        if str(entry.get("reason") or "").strip():
            continue
        out.append((rel, was.get("total", 0), entry.get("total", 0)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", default=RECORD)
    ap.add_argument("--root", default=REPO_ROOT)
    args = ap.parse_args(argv)

    try:
        with open(args.record, encoding="utf-8") as f:
            recorded = json.load(f)["files"]
    except (OSError, ValueError, KeyError) as e:
        print("FAIL (%s): cannot read the record %s (%s) — the record is this gate's whole ground, "
              "and a gate with no ground passes on everything." % (CHECK, args.record, e))
        return 1

    base, base_ref, stood_down = base_record(args.record)
    raised = hand_raises(recorded, base) if base is not None else []

    census = load_census()
    cap, cap_rule = census.load_word_cap()
    files = census.live_files(args.root)
    if not files:
        print("FAIL (%s): the live set came out empty, so this gate would pass on nothing." % CHECK)
        return 1

    rose, fell, held, unrecorded = [], [], [], []
    for rel in files:
        reading = census.measure(rel, cap, root=args.root)
        if "unread" in reading:
            print("FAIL (%s): %s refused to be read (%s)." % (CHECK, rel, reading["unread"]))
            return 1
        total = reading["total"]
        if rel not in recorded:
            unrecorded.append((rel, total))
            continue
        bound = recorded[rel]["total"]
        if total > bound:
            rose.append((rel, bound, total, reading))
        elif total < bound:
            fell.append((rel, bound, total))
        elif bound == 0:
            held.append(rel)

    for rel in held:
        print("  held clean: %s" % rel)
    for rel, bound, total in fell:
        print("  fell: %s — recorded %d, measured %d" % (rel, bound, total))
    if fell:
        print("  Lower the ceiling to what the text now measures:")
        print("    python3 scripts/rule-census.py --json guardrails/rule-census.json")

    if stood_down:
        print("  stands down: the record arm read no base copy of the record — %s." % stood_down)
    else:
        print("  the record arm read the record against the copy %s holds." % base_ref)

    if not rose and not unrecorded and not raised:
        print("OK (%s): %d live documents, %d held at zero, none above its record (cap %d, rule %s)."
              % (CHECK, len(files), len(held), cap, cap_rule))
        return 0

    for rel, was, now in raised:
        print("FAIL (%s): the record for %s was raised from %d to %d against the copy %s holds, with no "
              "reason beside it. A raise states its reason in that entry's `reason` field, the way a "
              "raised byte ceiling does in guardrails/doc-bounds.json."
              % (CHECK, rel, was, now, base_ref))
    for rel, total in unrecorded:
        print("FAIL (%s): %s is live and carries no entry in the record. Measure it into the record "
              "before it ships: python3 scripts/rule-census.py --json guardrails/rule-census.json"
              % (CHECK, rel))
    for rel, bound, total, reading in rose:
        if bound == 0:
            print("FAIL (%s): %s was repaired to zero and now carries %d finding(s). A cleared document "
                  "stays cleared." % (CHECK, rel, total))
        else:
            print("FAIL (%s): %s rose from %d to %d findings." % (CHECK, rel, bound, total))
        print("    long %d (longest sentence %d words), style %d, register %d"
              % (reading["long"], reading["longest"], reading["style"], reading["register"]))
    if rose:
        print("  Fix: repair the text, or read `python3 scripts/rule-census.py %s` to see each "
              "finding." % rose[0][0])
    return 1


if __name__ == "__main__":
    sys.exit(main())
