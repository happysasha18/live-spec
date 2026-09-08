# Prover record — 2026-09-08 what the three reads left standing

PUSH-REVIEW

This is the closure record for the range, written by the seat that carried the work, from the three
adversarial reads already on file and from the diff of the three commits. It opens no new
examination: every judgement below is either quoted from one of those reads or read off the diff
itself, and where a finding was closed after the read that raised it, this record says which commit
closed it and how the closure was checked at the time. The owner asked for exactly this and no more
(2026-09-08 21:21), so nothing here is a fresh audit and nothing here claims to be one.

The reads it stands on, all three committed under `docs/prover/`:

- `2026-09-08-the-door-learns-two-program-names.md` — the first attempt, which put the
  mode-and-composition judgement at the admission door and read a command's own text for a bare
  test-runner invocation. Refused: the read matched a program's name before anything else, so
  `grep -rn pytest` was refused while `python3 -m unittest discover -s tests` was admitted, and any
  trailing token walked it. That commit was dropped from the branch rather than repaired; its head
  line says so.
- `2026-09-08-the-mode-binds-here-and-not-on-a-host.md` — the read of e7869159. Three blocking
  findings.
- `2026-09-08-the-three-close-and-the-suite-reds-in-ci.md` — the read of e2f819c3. It confirmed
  those three closed and refused on two more.

Range: 5be3dd27..6a12ecde — the base the remote holds, then the commits this push sends. Three of
them change the tree and one carries records alone.

- e7869159 The acceptance run names its mode, and the mode binds what it may take — `run_modes`
  imported by `guardrails/check-acceptance-rerun.py`; a refusal for a run that named no mode; the
  selection put through `admit_targets`; a `decides_verdict` arm so a manual run reports without a
  verdict; `LIVE_SPEC_RUN_MODE: release` on gate v's workflow step; M-661 and M-662 pointed at
  tests; four new tests.
- e2f819c3 The three the review refused, and two proofs that were never run — `MODE_LAW` as the
  floor a missing `max_targets` falls to; the same two figures seeded by
  `adopt/install-scaffold.sh`; `stands_as_a_gate` reading the config's own `in_ci` against a CI
  marker; `named_mode` as the precedence's one home; `ModeCapExceeded` as the cap's own exception
  type; a `CheckpointUnreadable` arm; M-661 and M-662 rewritten to what their tests hold; the two
  fixture-proof pairs nobody called given tests; twelve further tests.
- 41ac93c2 The two the third read refused, and the release core's own keeper — the CI markers
  cleared in `run_rerun`; `RunModesUnreadable` out of `_load_run_modes` and `mode_composition`,
  caught in `main`; `max_targets: null` falling to the pack's law like a missing key; the release
  core held against the gate letters in `.github/workflows/gates.yml` in both directions and its
  `core_version` against `VERSION`; M-659 pointed at those two checks; the installer's contradicting
  header comment and the fixture block's misdated comment corrected; five new tests.
- 6a12ecde The three reads this range paid for — `docs/prover/` alone, the exemption this gate
  carries for a commit that ships a record.

Files read: the diff of all three changing commits and their messages; the three prover records
named above, in full; `guardrails/run_modes.py`; `guardrails/check-acceptance-rerun.py`;
`guardrails.config.json` (`run_modes`); `adopt/install-scaffold.sh` (the `run_modes` seed and its
header comment); `.github/workflows/gates.yml` (gate v's step); `matrix/build-pipeline.md`
(M-657..M-667); `tests/test_acceptance_rerun_reach.py`; `tests/test_run_modes.py`;
`tests/test_guardrail_fixture_proofs.py`; `tests/test_closure_kernel_bypasses.py`;
`spec/queue-intake-priority.md` Requirement 322.

Checks run: five, each with its result. All were run before this record was written, on the tree as
it now stands; this record adds none of its own.

- `python3 -m pytest -q` over the thirteen files that touch the changed code, with `GITHUB_ACTIONS`
  and `CI` set, which is how the server sees it — 440 passed, 2 skipped.
- The same thirteen files with both markers unset — 440 passed, 2 skipped. The two runs agree,
  which is the finding the third read raised and the thing that had to be true before a push.
- The release core against the CI chain, driven by removing gate v from the core in memory — the
  check names the missing letter, so it reds in the direction that matters. On the tree as it
  stands the two sides agree, 23 letters and 23, at `core_version` 6.1.0 against `VERSION` 6.1.0.
- The pack's law against the shape `adopt/install-scaffold.sh` seeded before this range: a `row`
  run asked for 40 targets is refused naming a cap of 1, and an `integration` run asked for 6 is
  refused naming 5. That shape admitted all 40 without a word before e2f819c3.
- The whole local push chain, `guardrails/pre-push`, on this range — every gate green except gate
  a, which is the record this file is.

Findings: nine were raised across the three reads. Seven are closed and two stand as recorded
deferrals, both named by the read that raised them and neither introduced by this range.

- Closed by the branch itself: the program-name judgement at the admission door. The commit was
  reset away, `names_no_target` exists nowhere in the tree, and no program name is matched anywhere
  in the code this range ships. The third read verified that independently.
- Closed by e2f819c3, each verified against the tree by the third read rather than by its commit
  message: the cap absent on every installed host, where a missing `max_targets` meant admit;
  `manual` standing as a one-word green in a CI gate, with `in_ci: false` sitting in the config with
  no reader; M-661 and M-662 wearing *built* over partial tests.
- Closed by e2f819c3 from the same read's non-blocking set: the mode precedence living in two homes
  and disagreeing about an empty string and about `PUSH_FULL=yes`; the over-broad `except
  ValueError` that reported any fault inside `judge` in the mode's own words.
- Closed by 41ac93c2: the suite reding in CI through the markers `run_rerun` inherited; the gate
  dying with a traceback on a host whose config pre-dates the seed. Both were introduced by this
  range's own earlier commits, and both are held by tests that drive a vendored host rather than the
  pack's own copy.
- Closed by 41ac93c2 on the owner's own reading of the range (2026-09-08 21:08): the release core
  was 23 letters copied out of CI with nothing keeping the two in step, so M-659 promised a fixed
  versioned composition that nothing held.
- Stands, recorded by the third read: criterion 12's literal words are "a targeted test run", and
  the fixtures that hold its admission half use `touch` rather than a runner. What is held is that a
  target is admitted in a `row` run and in an `integration` run, which is one assertion short of the
  criterion's own wording.
- Stands, recorded by the second and third reads: M-657 and M-658 remain overstated against the
  tests they name. This range narrowed M-659, M-661 and M-662 to what is held and left those two
  where it found them.

Neither of the two that stand is a defect in what this range ships: the mode contract has its
caller, the caps bind on this tree and on an installed host, a manual run cannot stand as a gate in
CI, an unreadable host config and an unreadable checkpoint are named refusals rather than
tracebacks, and the release core has a keeper. Both are bookkeeping against a criterion's own
wording, and both are recorded by the reads that raised them.

Blocking: none
