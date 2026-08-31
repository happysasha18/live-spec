"""One home per rule: a rule's own sentences appear where the rule lives, and nowhere else.

Base rule 4 says every fact has one canonical home and everything else is a pointer. Nothing
enforced it, so three rules drifted into several homes at once and the copies disagreed — the
report the owner reads every turn was stated three ways, the lane law twice under two names, and
the ask-never-guess duty across four base rules and six skill files. plan-16 converged them. This
is the check that keeps them converged.

HOW IT WORKS. Each rule below declares its one home and a few probes: short strings taken from the
rule's own wording, the kind of thing only a restatement would carry. A probe may appear in the
home and nowhere else in the reach. A pointer names the home instead of quoting the rule, so a
pointer passes; a second copy quotes the rule, so a second copy reds.

THE REACH, said plainly because a verdict without its reach is worth nothing. This check reads the
surfaces that tell a session how to work: `skills/`, `scripts/`, `guardrails/`, `hooks/`,
`templates/`, `adopt/`, `scaffold/`, `evals/`, `.live-spec/agent.md`, `README.md`, `OVERVIEW.md`
and `CLAUDE.md`. Four kinds of file are outside it, each for a reason and none of them to make the
check pass:

  * the spec (`PRODUCT_SPEC.md`, `spec/`) is the requirement register every surface above cites;
    a requirement and the base rule that carries it are one design, not drift.
  * the suite quotes text in order to pin it, this file included; a test that could not name the
    sentence it guards would guard nothing.
  * `PLAN.md`, `JOURNAL.md`, `DECISIONS.md`, `NEXT_STEPS.md` are a work queue and a history, not
    places a session reads a rule from.
  * `attic/` and `docs/` hold records of what was decided, which stay as they were written.

WHAT IT DOES NOT CATCH. A copy reworded end to end carries none of these probes and passes. The
probes catch the copy-paste and the near-copy, which is what actually happened all three times.
Judging a reworded copy stays a reader's job.

WHERE A HOME SITS OUTSIDE THIS REPOSITORY, as the report format's does, `home` is None: no file in
the reach may carry the probes at all, and the pointer test below reads the file that must name it.

Run it on its own to see one line per rule:
  python3 tests/test_one_home_per_rule.py

That plain form is what `PLAN.md`'s own check for this task calls. The probe a session prints at its
start runs every such check, so none of them may start a test suite; the same three assertions run
either way, and `python3 -m pytest tests/test_one_home_per_rule.py -v` is the suite's road in.
"""

import os

import pytest

from conftest import ROOT


# ---------------------------------------------------------------- the reach
REACH_DIRS = (
    "skills",
    "scripts",
    "guardrails",
    "hooks",
    "templates",
    "adopt",
    "scaffold",
    "evals",
)
REACH_FILES = (
    os.path.join(".live-spec", "agent.md"),
    "README.md",
    "OVERVIEW.md",
    "CLAUDE.md",
)
REACH_SUFFIXES = (".md", ".py", ".sh", ".json", ".txt")

# This file carries every probe by definition; it is the check, not a second copy of the rules.
SELF = os.path.join("tests", "test_one_home_per_rule.py")


# ---------------------------------------------------------------- the rules and their homes
RULES = {
    "report-format": {
        # The owner's own file, in his personal layer, outside this repository. Every surface in
        # the reach points at it; none states it.
        "home": None,
        "home_name": '~/.claude/playbook/CLAUDE.md, "How a reply to him looks"',
        "pointer_in": (
            os.path.join("skills", "communicator", "SKILL.md"),
            os.path.join(".live-spec", "agent.md"),
        ),
        "pointer": "~/.claude/playbook/CLAUDE.md",
        "probes": (
            "seven to ten lines",
            "ten lines at most",
            "10 lines or fewer",
            "✅ done · 🔄 in hand · ⬜ queued",
            "the recommendation and its reason",
            "external review's verdict",
        ),
    },
    "lane-law": {
        "home": os.path.join("skills", "live-spec-base", "SKILL.md"),
        "home_name": "skills/live-spec-base/SKILL.md, rule 7",
        "pointer_in": (
            os.path.join("skills", "director", "SKILL.md"),
            os.path.join("skills", "director", "references", "lanes-and-pen.md"),
        ),
        "pointer": "rule 7",
        # A probe is a sentence of the rule, never its name: "the lane-open act" is what a
        # pointer legitimately calls the thing, and using the name as a probe would red every
        # honest pointer. Each of these is wording only a restatement would carry.
        "probes": (
            "one more opens only on the human's asked word",
            "a landing commit carries exactly one row's delta",
            "the row→in-work flip is committed to main under the pen",
            "the act reads the profile cap",
        ),
    },
    "ask-never-guess": {
        "home": os.path.join("skills", "live-spec-base", "SKILL.md"),
        "home_name": "skills/live-spec-base/SKILL.md, rules 1 and 27",
        "pointer_in": (
            os.path.join("skills", "design-reviewer", "SKILL.md"),
            os.path.join("skills", "spec-author", "SKILL.md"),
            os.path.join("skills", "communicator", "SKILL.md"),
        ),
        "pointer": "rule 27",
        "probes": (
            "never invent intent",
            "a threshold, a policy, a domain wording",
            "three cases qualify",
            "never parks derivable work",
        ),
    },
}


# ---------------------------------------------------------------- reading
def _reach_paths():
    """Every file in the reach, as paths relative to the repository root."""
    seen = []
    for rel in REACH_FILES:
        if os.path.isfile(os.path.join(ROOT, rel)):
            seen.append(rel)
    for top in REACH_DIRS:
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for name in sorted(filenames):
                if not name.endswith(REACH_SUFFIXES):
                    continue
                seen.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(set(seen))


def _flat(rel):
    """The file's text, whitespace collapsed and case folded, so a probe matches across a
    line wrap and survives a copy that changed a capital."""
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
        return " ".join(f.read().split()).lower()


REACH = {rel: _flat(rel) for rel in _reach_paths() if rel != SELF}


# ---------------------------------------------------------------- the checks
# The floor, named here because the three checks below cannot name it themselves. They are
# parametrized over RULES, so an empty table generates no cases at all: pytest reports three SKIPS
# and this file run on its own exits 0, which is how the whole check disarms without a red anywhere.
# Dropping one rule from the table narrows the reach the same silent way. This is the shape the
# gates in guardrails/ already refuse — each declares its expected-non-empty input and reds by name
# rather than passing over nothing (SPEC INV-218) — and scripts/plan_checks.py's own reader takes
# the same precaution on its map. The floor only grows: a fourth rule joining the table is welcome,
# and any of these three leaving it is not.
FLOOR = ("ask-never-guess", "lane-law", "report-format")


def test_the_table_still_names_every_rule_this_check_was_built_for():
    missing = [rule_id for rule_id in FLOOR if rule_id not in RULES]
    assert not missing, (
        "the one-home table no longer names %s, so nothing here checks %s any more; a rule leaves "
        "this table only when its own convergence is undone, and then this line goes with it"
        % (", ".join(missing), "them" if len(missing) > 1 else "it"))


@pytest.mark.parametrize("rule_id", sorted(RULES))
def test_the_rule_is_stated_in_one_home_only(rule_id):
    rule = RULES[rule_id]
    home = rule["home"]
    strays = []
    for probe in rule["probes"]:
        needle = " ".join(probe.split()).lower()
        for rel, text in REACH.items():
            if rel == home:
                continue
            if needle in text:
                strays.append((rel, probe))
    assert not strays, (
        "%s belongs to one home, %s. These files state it a second time instead of pointing "
        "at it:\n%s" % (
            rule_id, rule["home_name"],
            "\n".join("  %s carries %r" % (rel, probe) for rel, probe in strays)))


@pytest.mark.parametrize("rule_id", sorted(RULES))
def test_the_home_still_states_the_rule(rule_id):
    """The other half: converging on one home must not empty the home. Skipped where the home
    lives outside this repository — the next check reads the pointers instead."""
    rule = RULES[rule_id]
    if rule["home"] is None:
        pytest.skip("%s lives at %s, outside this repository" % (rule_id, rule["home_name"]))
    text = _flat(rule["home"])
    missing = [p for p in rule["probes"] if " ".join(p.split()).lower() not in text]
    assert not missing, (
        "%s's home %s no longer carries %r — the rule was moved or lost, and the pointers at it "
        "now point at nothing" % (rule_id, rule["home_name"], missing))


@pytest.mark.parametrize("rule_id", sorted(RULES))
def test_every_place_the_copy_stood_now_points_at_the_home(rule_id):
    rule = RULES[rule_id]
    pointer = " ".join(rule["pointer"].split()).lower()
    for rel in rule["pointer_in"]:
        text = REACH.get(rel)
        assert text is not None, "%s is not in the reach, so its pointer cannot be read" % rel
        assert pointer in text, (
            "%s held a copy of %s and must now name its home %s; it names neither the rule nor "
            "where the rule lives, which leaves the reader nowhere to go"
            % (rel, rule_id, rule["home_name"]))


if __name__ == "__main__":
    import sys

    failures = []
    try:
        test_the_table_still_names_every_rule_this_check_was_built_for()
    except AssertionError as exc:
        failures.append(str(exc))
    for _rule_id in sorted(RULES):
        for _check in (test_the_rule_is_stated_in_one_home_only,
                       test_the_home_still_states_the_rule,
                       test_every_place_the_copy_stood_now_points_at_the_home):
            try:
                _check.__wrapped__(_rule_id) if hasattr(_check, "__wrapped__") else _check(_rule_id)
            except AssertionError as exc:
                failures.append(str(exc))
            except BaseException as exc:  # pytest.skip on a home outside this repository
                if type(exc).__name__ not in ("Skipped", "OutcomeException"):
                    raise
        print("%-16s one home: %s" % (_rule_id, RULES[_rule_id]["home_name"]))
    for _f in failures:
        print("\nFAIL: %s" % _f, file=sys.stderr)
    sys.exit(1 if failures else 0)
