"""The run-mode contract's one reader (SPEC rule 43): a budget names, in advance, a finite
composition of work — which targets run, how many — and no number in it is read off a clock.
An `emergency_timeout_seconds` is a stop on a process the run owns, never a verdict input.

Exactly four modes exist, defined in guardrails.config.json under "run_modes": row,
integration, release, manual. This module resolves which one a run was asked for and answers,
for a mode, its composition — it runs nothing itself.
"""

import json
import os

MODES = ("row", "integration", "release", "manual")

# The pack's own law about composition, which a host does not get to widen (Requirement 322
# criteria 2 and 3, and criterion 20's split: the pack ships the mechanism and its laws, the host
# keeps its own subject — its targets, its layer map, its release core). A `row` run covers one
# target and an `integration` run at most five, the figure the pack already carries as
# `MOST_DELIVERABLES` in scripts/task-admission.py.
#
# These are the FLOOR, read when a config names no cap of its own. Before them, a missing
# `max_targets` meant "admit whatever you are given", so every host adopt/install-scaffold.sh
# seeded — its `row` and `integration` keys carry no cap — had a row run that admitted forty
# targets without a word (the adversarial read of 2026-09-08). Absent now means the pack's law
# rather than no law. A config MAY name a lower cap; a higher one is its own business and this
# module records it, since a host's own tuning is the host's (the same read `mode_composition`
# already takes for every other key).
MODE_LAW = {"row": 1, "integration": 5}

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "guardrails.config.json"
)


class RunModesUnreadable(ValueError):
    """This tree carries no readable run-mode contract for the mode being asked about."""


def _load_run_modes(config_path=_CONFIG_PATH):
    """The four modes as this tree records them.

    A tree whose config carries no `run_modes` key refuses by name. `adopt/install-scaffold.sh`
    seeds that key only into a config it creates itself, keeping its never-clobber promise to a
    host's own filled config — so a host that adopted the pack before the key existed has one
    without it, and every reader here used to end in a bare KeyError traceback with no verdict
    (the adversarial read of 2026-09-08).
    """
    try:
        with open(config_path, encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError) as exc:
        raise RunModesUnreadable("%s does not load: %s" % (config_path, exc))
    if "run_modes" not in cfg:
        raise RunModesUnreadable(
            "%s carries no \"run_modes\" key, so no run here knows what its mode covers. A tree "
            "that adopted this pack before the key existed writes its own: the four names are "
            "%s, and adopt/install-scaffold.sh seeds them into a config it creates."
            % (config_path, ", ".join(MODES)))
    return cfg["run_modes"]


def named_mode(env=None):
    """The mode this environment NAMED, or None where it named none.

    One home for the precedence every caller reads: `LIVE_SPEC_RUN_MODE` by name, else
    `LIVE_SPEC_PUSH_FULL` (guardrails/pre-push's own switch, which that hook treats as set-or-not
    rather than as the string "1"), else nothing. A caller that refuses an unnamed run asks this;
    `resolve_mode` below is the same read with the default on top. Two callers spelling this
    precedence themselves disagreed about an empty string and about `PUSH_FULL=yes` (the
    adversarial read of 2026-09-08), which is what one home is for.
    """
    env = os.environ if env is None else env
    raw = env.get("LIVE_SPEC_RUN_MODE")
    if raw is not None and raw.strip():
        if raw not in MODES:
            raise ValueError(
                "unknown run mode %r; the four modes are %s" % (raw, ", ".join(MODES))
            )
        return raw
    if env.get("LIVE_SPEC_PUSH_FULL"):
        return "release"
    return None


def resolve_mode(env=None):
    """The mode a run was asked for, with the standing default: a run that named none is a `row`
    run. A caller for which an unnamed run is a defect asks `named_mode` and refuses on None."""
    return named_mode(env) or "row"


def mode_composition(mode, run_modes=None):
    """The named mode's composition, as recorded in guardrails.config.json."""
    if mode not in MODES:
        raise ValueError(
            "unknown run mode %r; the four modes are %s" % (mode, ", ".join(MODES))
        )
    run_modes = _load_run_modes() if run_modes is None else run_modes
    if mode not in run_modes:
        raise RunModesUnreadable(
            "this tree's run_modes names %s, and nothing for %r — a mode a run asks for and the "
            "config does not carry has no composition to fix the run to."
            % (", ".join(sorted(run_modes)) or "no mode at all", mode))
    return run_modes[mode]


class ModeCapExceeded(ValueError):
    """A run asked to cover more than its own mode's composition allows."""


def admit_targets(mode, targets, run_modes=None):
    """The targets a mode may run. Refuses when more than the mode's own cap are asked for,
    naming the mode, the cap, and how many were asked for.

    The cap is the config's `max_targets` where it names one, and otherwise the pack's own law
    for that mode (MODE_LAW): one target for `row`, five for `integration`. `release` and
    `manual` carry no law here and admit what they are given — a release run's composition is its
    own versioned core list, and a manual run decides no verdict at all.
    """
    composition = mode_composition(mode, run_modes)
    # A key written as null is a key naming no cap, the same as a key nobody wrote — `.get` with a
    # default hands back the null and the law is walked, which is how a one-word edit could have
    # widened `row` to everything.
    cap = composition.get("max_targets")
    if cap is None:
        cap = MODE_LAW.get(mode)
    if cap is not None and len(targets) > cap:
        raise ModeCapExceeded(
            "mode %r allows at most %d target(s); %d were asked for"
            % (mode, cap, len(targets))
        )
    return list(targets)


def stands_as_a_gate(mode, run_modes=None):
    """Whether a run of this mode may stand as a CI or release gate (criterion 8).

    Read off the mode's own `in_ci` key, which `manual` ships as false and which nothing read
    until now — a config field no code opens is a comment. The caller pairs this with whether it
    is actually running in CI; the mode alone says what it is allowed to be.
    """
    return mode_composition(mode, run_modes).get("in_ci", True)


def decides_verdict(mode, run_modes=None):
    """Whether the named mode's run decides a verdict."""
    return mode_composition(mode, run_modes)["decides_verdict"]
