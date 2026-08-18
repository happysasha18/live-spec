# PUSH-REVIEW — a test says out loud which tree it runs in

Date: 2026-08-18 evening. Range: RANGE-PLACEHOLDER — the pushed range: the two fixes,
the catcher and this record.
Root: every push today was blocked, and none of them by the package under it. A freshly
built clean branch grew hundreds of commits mid-run — 711, then 403, then 429 — titled
`fixture`, `skill v1`, `base`, `scratch`, authored by `t <t@t>` and `a <a@example.com>`,
and its working tree lost tracked files and gained a stray `nonexistent-ci-home`
directory. Gate (ad) then reported, correctly, that it would be measuring bytes the push
does not send. It was reading wreckage the guard had just made while running the suite.

What happened: two independent mechanisms, both closed here.

The first is live and reproducible. `tests/test_guardrails.py` had a `run()` helper whose
`cwd` defaulted to `ROOT` — the very tree under judgement. Two of its call sites handed
`HOME=/nonexistent-ci-home` to `guardrails/check-pin-drift.sh`, which shells out to
`python3`; this machine's system Python cannot resolve that HOME and falls back to
writing its cache relative to the current directory, which was the judged tree. `cwd` is
now a required keyword argument, so it cannot be forgotten: 47 call sites in
`test_guardrails.py`, seven more in `test_guardrails_unit.py` which imports the same
helper, and the sites in `test_clock_hook.py`, `test_deletion_only_push.py` and
`test_ratchet_kit.py` now each name their tree out loud. Gates that must judge the real
repository still say `cwd=ROOT`, explicitly, and lose nothing. The two HOME sites use a
real temporary directory instead of a path that never existed.

The second was the fabricated commits, and it was already closed earlier today by
`check-tests.sh` taking its repo root from the tests directory it is handed rather than
from the caller's ambient cwd. That fix is the first commit of this range. It was proved
red to green on its own regression test and then held across three full twenty-minute
suite runs and an eightfold concurrent race.

Checks run: the full suite on the fixed tree leaves zero new commits, zero
`nonexistent-ci-home`, and the same five pre-existing environment failures the unfixed
tree has — no more. A targeted run here (`test_ratchet_kit.py`, `test_clock_hook.py`, 19
passed) left the working copy clean. The catcher is
`tests/conftest.py::judged_tree_gains_no_commits`: it snapshots the judged tree's HEAD
and status around the whole session and reds on any drift. It was proved by planting a
deliberate empty commit — red — and then green.

Findings:
- A default that points at the real repository is not a convenience, it is a loaded gun.
  The repair that lasts is not fixing the call sites but removing the default, so the
  next person cannot omit the argument at all.
- The blind spot on the first pass is worth naming: a second file imported the same
  helper and kept seven unfixed call sites. It was caught only by running the full suite.
  A fix scoped to the file where the bug was found would have shipped half a repair.
- The branch that carried the earlier attempt still holds its fabricated tail. It was
  left alone rather than rewritten; this package was rebuilt clean from main instead.

Blocking:
- none.
