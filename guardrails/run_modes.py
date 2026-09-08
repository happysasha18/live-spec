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

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "guardrails.config.json"
)


def _load_run_modes(config_path=_CONFIG_PATH):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["run_modes"]


def resolve_mode(env=None):
    """The mode a run was asked for: LIVE_SPEC_RUN_MODE if set (one of the four names, by
    name only); else LIVE_SPEC_PUSH_FULL=1 resolves to "release" (guardrails/pre-push's own
    switch); else "row"."""
    env = os.environ if env is None else env
    raw = env.get("LIVE_SPEC_RUN_MODE")
    if raw is not None:
        if raw not in MODES:
            raise ValueError(
                "unknown run mode %r; the four modes are %s" % (raw, ", ".join(MODES))
            )
        return raw
    if env.get("LIVE_SPEC_PUSH_FULL") == "1":
        return "release"
    return "row"


def mode_composition(mode, run_modes=None):
    """The named mode's composition, as recorded in guardrails.config.json."""
    if mode not in MODES:
        raise ValueError(
            "unknown run mode %r; the four modes are %s" % (mode, ", ".join(MODES))
        )
    run_modes = _load_run_modes() if run_modes is None else run_modes
    return run_modes[mode]


def admit_targets(mode, targets, run_modes=None):
    """The targets a mode may run. Refuses when more than the mode's own max_targets are
    asked for, naming the mode, the cap, and how many were asked for. A mode carrying no cap
    (max_targets absent) admits whatever it is given."""
    composition = mode_composition(mode, run_modes)
    cap = composition.get("max_targets")
    if cap is not None and len(targets) > cap:
        raise ValueError(
            "mode %r allows at most %d target(s); %d were asked for"
            % (mode, cap, len(targets))
        )
    return list(targets)


def decides_verdict(mode, run_modes=None):
    """Whether the named mode's run decides a verdict."""
    return mode_composition(mode, run_modes)["decides_verdict"]
