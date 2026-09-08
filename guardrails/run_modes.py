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
# keeps its own subject — its targets, its layer map, its release core).
#
# One number lives here, and it is `row`, because one target IS what a row run means: the one
# accepted task's own acceptance command. It is the FLOOR, read when a config names no cap of its
# own — before it, a missing `max_targets` meant "admit whatever you are given", so every host
# adopt/install-scaffold.sh seeded had a row run that admitted forty targets without a word (the
# adversarial read of 2026-09-08). Absent means the pack's law rather than no law.
#
# `integration` carried a second number until 2026-09-08 — at most five, borrowed from
# `MOST_DELIVERABLES`, a figure about how many deliverables one plan holds and about nothing a run
# covers. A cap counts targets and says nothing about which ones, so it admitted any five and
# refused a sixth for no reason anybody could state. What an integration run is admitted against is
# a composition somebody named before it started, and the other two modes read the same way: a
# release run against its own versioned core, a manual run against the purpose and the finite
# sample it recorded. `NAMED_COMPOSITION` below is that reading, and it holds no number at all.
MODE_LAW = {"row": 1}

# What each mode other than `row` must have written down before a run of it is admitted, and where
# `admit_targets` reads it. The value is the composition key naming the run's own targets; the
# second element is what else that mode's composition owes.
NAMED_COMPOSITION = {
    # Requirement 322 criterion 3: the layers the change touched, each resolved through the mode's
    # own layer_map to its own named test targets. `targets` is that resolution, written down, and
    # a run of this mode covers what that list names and nothing beside it.
    "integration": ("targets", ()),
    # Criterion 5: a fixed, versioned list of core gates. The list names GATES, so it is what the
    # composition owes rather than a set the run's own selection has to sit inside — what holds a
    # release run's selection down is criterion 6's `never_grows_with`, checked by its own reader.
    "release": ("core", ("core_version",)),
}

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


class ModeCompositionUnnamed(ValueError):
    """A run asked for a mode whose composition nobody wrote down before it started."""


def _finite(value) -> bool:
    """A recorded sample is finite when somebody can count it: a list, or a positive number."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (list, tuple)):
        return True
    return isinstance(value, int) and value > 0


def admit_targets(mode, targets, run_modes=None):
    """The targets a mode may run, and the refusal when a run outgrows its own mode.

    `row` is the one mode judged by a number, because one target is what a row run means: the one
    accepted task's own acceptance command. The cap is the config's `max_targets` where it names
    one, and otherwise MODE_LAW.

    Every other mode is judged by its composition instead. An `integration` run is admitted against
    the targets its composition names, a `release` run against its versioned core, and a `manual`
    run against the purpose and the finite sample it recorded before it started. A mode whose
    composition names none of that refuses by name — an unnamed composition is the state this
    reading exists to catch, and admitting it under a count was the thing that let any five targets
    through and stopped a sixth for no stateable reason.
    """
    composition = mode_composition(mode, run_modes)
    if mode == "row":
        # A key written as null is a key naming no cap, the same as a key nobody wrote — `.get`
        # with a default hands back the null and the law is walked, which is how a one-word edit
        # could have widened `row` to everything.
        cap = composition.get("max_targets")
        if cap is None:
            cap = MODE_LAW["row"]
        if len(targets) > cap:
            raise ModeCapExceeded(
                "mode 'row' allows at most %d target(s); %d were asked for" % (cap, len(targets)))
        return list(targets)

    if mode == "manual":
        # Criterion 7: a person starts a manual run, and its purpose and its limit are recorded
        # before it starts. What the PACK owns is that the mode declares those two things; the
        # values themselves belong to the person's own run, and a reader that demanded them in the
        # contract would make every manual audit impossible rather than bounded.
        declares = [str(name) for name in (composition.get("records_before_start") or [])]
        for owed_name, alternatives in (("purpose", ("purpose",)), ("limit", ("limit", "sample"))):
            if not any(alt in declares for alt in alternatives):
                raise ModeCompositionUnnamed(
                    "mode 'manual' runs only against what it wrote down before it started, and its "
                    "composition declares no %s. Its `records_before_start` names what a run of it "
                    "records: a purpose, and a finite sample." % owed_name)
        # Where the composition carries the values too, they bind: a sample nobody can count is
        # not a limit, and one written down and never read is a number for show.
        for name in ("limit", "sample"):
            value = composition.get(name)
            if value is None:
                continue
            if not _finite(value):
                raise ModeCompositionUnnamed(
                    "mode 'manual' records %r as %r, which nobody can count. A sample is a named "
                    "list or a positive count." % (name, value))
            if isinstance(value, (list, tuple)):
                stray = [t for t in targets if t not in value]
                if stray:
                    raise ModeCompositionUnnamed(
                        "mode 'manual' was asked for %s, which its recorded %r does not name."
                        % (", ".join(repr(s) for s in stray), name))
            elif len(targets) > value:
                raise ModeCompositionUnnamed(
                    "mode 'manual' recorded a sample of %d and was asked for %d."
                    % (value, len(targets)))
        return list(targets)

    key, owed = NAMED_COMPOSITION[mode]
    named = composition.get(key)
    if not named:
        raise ModeCompositionUnnamed(
            "mode %r runs only against a composition written down before it started, and its "
            "%r names none. Write it into that key first; there is no count that stands in for "
            "naming it." % (mode, key))
    for owed_key in owed:
        if not composition.get(owed_key):
            raise ModeCompositionUnnamed(
                "mode %r names its %r and no %r, so nothing says which version of that list this "
                "run covers." % (mode, key, owed_key))
    if mode == "release":
        # The core names the gates a release runs, so it is not a set this run's own selection sits
        # inside. Naming it, and naming its version, is the whole of what this mode is admitted on.
        return list(targets)
    stray = [t for t in targets if t not in named]
    if stray:
        raise ModeCompositionUnnamed(
            "mode %r was asked for %s, which its own %r does not name. A run covers what its "
            "composition names and nothing beside it."
            % (mode, ", ".join(repr(s) for s in stray), key))
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
