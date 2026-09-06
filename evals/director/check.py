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

WHY THE FIELDS ARE GRADED DIFFERENTLY. The four booleans are the claim the mandate makes: a
question must not become work, an idea must not become an instruction, a correction must
attach to work in flight. Those are graded exactly. The acts a scenario names as expected
are graded exactly too — every one of them has to show up, or the scenario is red.
Dimensions and specialists are professional judgment with a defensible range, so a scenario
states only what must be present and what must be absent, and anything else is the
Director's call.

WHY AN ACT BEYOND THE EXPECTED SET IS SOMETIMES A NOTE AND SOMETIMES A FAIL. These are two
different mistakes with two different prices in the skill, and the scenario's own expected
acts list says which one applies.

When the scenario expects one or more real acts, an extra one beside them is the cheap
mistake priced in "One turn, several acts" (SKILL.md, ~lines 126-128): "When you cannot tell
whether a clause is its own act or part of the neighbouring one, it is its own act. Naming
one act too many costs a sentence. Naming one too few loses what somebody said." That
passage prices splitting ONE REAL ACT that happened into two — a turn that did carry
something is over-segmented. So it is recorded as a note rather than failed: two of the nine
reds in the 2026-08-26 run were scenarios whose every material field was right and whose
only defect was this kind of extra act (re-derived directly against that commit's traces;
an earlier count of six here over-counted the same run under a different check).

When the scenario expects NO acts at all, an extra one is a different mistake with its own
section, "Not every message is one of the seven" (SKILL.md, ~lines 148-152): "A greeting, a
thank-you, a thumbs-up on something already agreed ... Reaching for one of the seven acts
here is how a thank-you becomes a roadmap row." That is not one real act split in two — it
is an act invented on a turn that carried none — so it fails.

The note is printed on every run, passing or failing, and counted in the closing summary,
because a producer that always drifts toward over-segmentation is worth seeing. It does not
turn a pass into a fail on its own. Everything else still does: a missing act, a wrong
boolean, a wrong work_items, a missing or forbidden dimension or specialist, an act named on
a turn the scenario expects to carry none, and a name that is not a speech act at all.

WHEN `operation` IS REQUIRED. Section 7A of the turnkey contract requires every verdict to
carry the state operation beside its acts, so any run recorded on or after OPERATION_REQUIRED_FROM
must carry the field: a scenario that names an `operation` against such a run that has none
fails, the same as a missing act. Recordings made before that date are graded on their other
fields and skipped on this one, because the field did not exist when the producer answered
and no re-reading of an old trace can invent it. That skip is a fact about those recordings,
not an allowance for new ones.

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
OPERATIONS = {"none", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"}
# Runs recorded on or after this date must carry `operation`; see the header.
OPERATION_REQUIRED_FROM = "2026-09-06"
EXACT_BOOLS = ("creates_work", "shelves_idea", "attaches_to_existing_work")


def grade(scenario, actual):
    """Return (list of failure strings, list of note strings, count of checks made).

    A failure flips the scenario to red. A note is carried and printed and does not.
    """
    fails, notes, checks = [], [], 0
    want = scenario["expect"]

    checks += 1
    got_acts = set(actual.get("acts") or [])
    want_acts_list = want["acts"]
    want_acts = set(want_acts_list)
    unknown = got_acts - ACTS
    if unknown:
        fails.append(f"acts: not speech acts: {sorted(unknown)}")
    elif want_acts_list:
        # The scenario's primary act — the first one listed — and every secondary act
        # beyond it are graded as their own required-present checks, the same way each
        # EXACT_BOOLS field below gets its own check rather than one lumped verdict for
        # the whole set: every expected act is named and counted on its own.
        checks += 1
        primary = want_acts_list[0]
        if primary not in got_acts:
            fails.append(f"acts: primary act missing: {primary!r}")

        for act in want_acts_list[1:]:
            checks += 1
            if act not in got_acts:
                fails.append(f"acts: missing secondary act {act!r}")

        # One act too many, beside at least one real act the scenario did ask for, is the
        # cheap mistake by the skill's own cost statement ("One turn, several acts"), so
        # it is recorded and reported and does not redden the scenario by itself. See the
        # header note. An act the scenario asked for and did not get is still a failure,
        # and it is checked above, so a run that misses one act and adds another is red
        # on the miss.
        for act in sorted(got_acts - want_acts):
            checks += 1
            notes.append(f"acts: extra act {act!r} beyond what the scenario asked for")
    else:
        # The scenario expects no acts at all — the turn is conversation by the skill's
        # own rule ("Not every message is one of the seven"). Naming an act here is not
        # the cheap "one too many" mistake priced above, which prices splitting ONE REAL
        # ACT that happened; this is inventing an act on a turn that carried none, so it
        # fails rather than notes. See the header.
        for act in sorted(got_acts):
            checks += 1
            fails.append(
                f"acts: named {act!r} on a turn the scenario expects to carry no act at all"
            )

    # See the header, "WHEN `operation` IS REQUIRED": a run recorded on or after
    # OPERATION_REQUIRED_FROM must carry the field, and fails the scenario without it.
    # Older recordings are skipped on this field alone.
    if "operation" in want and "operation" not in actual:
        if str(actual.get("recorded") or "") >= OPERATION_REQUIRED_FROM:
            checks += 1
            fails.append(
                "operation: missing on a run recorded "
                f"{actual.get('recorded')!r}, on or after {OPERATION_REQUIRED_FROM}"
            )
    elif "operation" in want and "operation" in actual:
        checks += 1
        want_ops = set(want["operation"])
        got_ops = set(actual["operation"] or [])
        unknown_ops = got_ops - OPERATIONS
        if unknown_ops:
            fails.append(f"operation: not in the closed vocabulary: {sorted(unknown_ops)}")
        if got_ops != want_ops:
            fails.append(f"operation: wanted {sorted(want_ops)}, got {sorted(got_ops)}")

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

    # creates_work:true with work_items:0 is not a state the skill's own definitions
    # allow — accepted new work carries at least one work item. This is a check on the
    # verdict's own coherence, independent of whatever the scenario expected, so it runs
    # unconditionally rather than only when `want` happens to name these fields.
    if actual.get("creates_work") is True and actual.get("work_items") == 0:
        checks += 1
        fails.append(
            "creates_work is true but work_items is 0 — accepted work must carry at "
            "least one work item"
        )

    # A verdict that neither accepts new work nor changes work in flight has nothing to
    # route, so its routing fields must be empty. A correction is exempt: it changes work
    # that is already running, and naming what that work now touches is the point of it.
    if want.get("creates_work") is False and not want.get("attaches_to_existing_work"):
        checks += 1
        spill = sorted(set(actual.get("dimensions") or []) | set(actual.get("specialists") or []))
        if spill:
            fails.append(f"routed work that was never accepted: {spill}")

    return fails, notes, checks


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def report(name, fails, notes, checks):
    if fails:
        print(f"FAIL  {name}  ({len(fails)} of {checks})")
    else:
        print(f"ok    {name}  ({checks} checks)")
    for f in fails:
        print(f"        {f}")
    for n in notes:
        print(f"        note: {n}")
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
    noted = 0
    op_only = 0
    for sc, actual in pairs:
        fails, notes, checks = grade(sc, actual)
        if report(sc.get("id", "scenario"), fails, notes, checks):
            passed += 1
        elif all(f.startswith("operation:") for f in fails):
            # Red on the operation field and nothing else. Counted apart so a reader can
            # see that field's own share of the score rather than inferring it.
            op_only += 1
        if notes:
            noted += 1

    # The pass line stays the last line printed, and the note count lives ON it rather
    # than on a line above: scripts/state-probe.sh and scripts/plan_checks.py both read
    # this script's score with `tail -1`, so a line above the last is invisible to both.
    # plan_checks.py also greps this line for the literal phrase " 0 of ", so that
    # phrasing stays intact at the start of the line.
    line = f"{passed} of {len(pairs)} recorded runs pass"
    if a.all and missing:
        line += f"; {len(missing)} scenarios have no run"
    if noted:
        line += f"; {noted} named an act the scenario did not ask for"
    print(f"\noperation-only reds: {op_only}")
    print(line)
    return 0 if passed == len(pairs) and not (a.all and missing) else 1


if __name__ == "__main__":
    sys.exit(main())
