#!/usr/bin/env python3
"""check.py — grade one Director run against what a scenario expected.

WHAT THIS IS FOR. Package 1 is finished when the Director's behaviour is checked by
scenarios rather than by grepping its own skill file for required phrases. A phrase check
passes on a skill that says the right words and does the wrong thing. So the evidence here
is a verdict the Director actually produced, from a real message, graded against what the
scenario says the right verdict is.

THE THREE PARTS, KEPT APART ON PURPOSE.

  fixtures  evals/director/scenarios.json — the messages and the expected verdicts. Data.
  producer  a fresh agent per scenario, holding skills/director/SKILL.md and the message,
            returning the verdict as JSON. Judgment. Not this file.
  grader    this file. Deterministic. Knows nothing about the Director's reasoning and
            cannot be talked round.

Keeping the producer out of this script is the point. A grader that also produces the
answer grades itself.

WHY THE FIELDS ARE GRADED DIFFERENTLY. The acts and the four booleans are the claim the
mandate makes: a question must not become work, an idea must not become an instruction, a
correction must attach to work in flight. Those are graded exactly. Dimensions and
specialists are professional judgment with a defensible range, so a scenario states only
what must be present and what must be absent, and anything else is the Director's call.

USAGE
  check.py --scenario ONE.json --actual RUN.json
  check.py --all       grade every scenario in scenarios.json that has a run in traces/
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACTS = {"question", "idea", "observation", "decision", "correction", "instruction", "halt"}
EXACT_BOOLS = ("creates_work", "shelves_idea", "attaches_to_existing_work")


def grade(scenario, actual):
    """Return (list of failure strings, count of checks made)."""
    fails, checks = [], 0
    want = scenario["expect"]

    checks += 1
    got_acts = set(actual.get("acts") or [])
    want_acts = set(want["acts"])
    unknown = got_acts - ACTS
    if unknown:
        fails.append(f"acts: not speech acts: {sorted(unknown)}")
    elif got_acts != want_acts:
        missed = sorted(want_acts - got_acts)
        spare = sorted(got_acts - want_acts)
        detail = []
        if missed:
            detail.append(f"missed {missed}")
        if spare:
            detail.append(f"invented {spare}")
        fails.append(f"acts: {', '.join(detail)}")

    for field in EXACT_BOOLS:
        if field not in want:
            continue
        checks += 1
        if bool(actual.get(field)) is not bool(want[field]):
            fails.append(f"{field}: wanted {want[field]}, got {bool(actual.get(field))}")

    for field, key in (("dimensions", "dimensions"), ("specialists", "specialists")):
        got = set(actual.get(key) or [])
        for kind, ok in (("required", lambda m: m - got), ("forbidden", lambda m: m & got)):
            names = want.get(f"{field}_{kind}")
            if not names:
                continue
            checks += 1
            bad = sorted(ok(set(names)))
            if bad:
                word = "missing" if kind == "required" else "must not name"
                fails.append(f"{field}: {word} {bad}")

    if "work_items" in want:
        checks += 1
        got = actual.get("work_items")
        if got != want["work_items"]:
            fails.append(f"work_items: wanted {want['work_items']}, got {got!r}")

    # A verdict that neither accepts new work nor changes work in flight has nothing to
    # route, so its routing fields must be empty. A correction is exempt: it changes work
    # that is already running, and naming what that work now touches is the point of it.
    if want.get("creates_work") is False and not want.get("attaches_to_existing_work"):
        checks += 1
        spill = sorted(set(actual.get("dimensions") or []) | set(actual.get("specialists") or []))
        if spill:
            fails.append(f"routed work that was never accepted: {spill}")

    return fails, checks


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def report(name, fails, checks):
    if fails:
        print(f"FAIL  {name}  ({len(fails)} of {checks})")
        for f in fails:
            print(f"        {f}")
    else:
        print(f"ok    {name}  ({checks} checks)")
    return not fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario")
    ap.add_argument("--actual")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    if a.all:
        book = load(os.path.join(HERE, "scenarios.json"))
        pairs, missing = [], []
        for sc in book["scenarios"]:
            run = os.path.join(HERE, "traces", sc["id"] + ".json")
            if os.path.exists(run):
                pairs.append((sc, load(run)))
            else:
                missing.append(sc["id"])
        for m in missing:
            print(f"----  {m}  no recorded run")
        if not pairs:
            print("no recorded runs to grade")
            return 2
    elif a.scenario and a.actual:
        pairs = [(load(a.scenario), load(a.actual))]
    else:
        ap.error("give --scenario and --actual, or --all")

    passed = 0
    for sc, actual in pairs:
        fails, checks = grade(sc, actual)
        if report(sc.get("id", "scenario"), fails, checks):
            passed += 1

    total = len(pairs) + (len(missing) if a.all else 0)
    print(f"\n{passed} of {len(pairs)} recorded runs pass"
          + (f"; {len(missing)} scenarios have no run" if a.all and missing else ""))
    return 0 if passed == len(pairs) and not (a.all and missing) else 1


if __name__ == "__main__":
    sys.exit(main())
