# Prover record — 2026-09-08 the three close and the suite reds in CI

PUSH-REVIEW

The pass was run by a seat that authored none of these two commits, briefed to find reasons to
refuse them and to hold them defective until evidence said otherwise. This is the third adversarial
read of this work today; the first refused a commit that has since been dropped from the branch, the
second refused e7869159 on three counts. The second read's three blocking findings are reported
closed by e2f819c3, so the first job of this pass was to verify each closure against the tree rather
than against the commit message. Every judgement below about what the gate admits, refuses, prints
or returns was taken by running the shipped script or the shipped function — against this tree,
against a planted host, and against two clean clones checked out at `origin/main` and at e7869159.

Range: 5be3dd27..e2f819c3 — the base the remote holds, then the two commits this push sends.

- e7869159 The acceptance run names its mode, and the mode binds what it may take — `run_modes`
  imported by `guardrails/check-acceptance-rerun.py`, a refusal for a run that named no mode, the
  selection put through `admit_targets`, a `decides_verdict` arm, `LIVE_SPEC_RUN_MODE: release` on
  gate v's workflow step, M-661 and M-662 moved to *built*, four new tests.
- e2f819c3 The three the review refused, and two proofs that were never run — `MODE_LAW` as the
  floor a missing `max_targets` falls to, `max_targets` seeded by `adopt/install-scaffold.sh`,
  `stands_as_a_gate` reading the config's `in_ci` against a CI marker, `named_mode` as the
  precedence's one home, `ModeCapExceeded` as the cap's own exception type, a `CheckpointUnreadable`
  arm, M-661 and M-662 rewritten, twelve further tests.

Files read: both commits' diffs and messages; `guardrails/run_modes.py` whole (`MODE_LAW`,
`_load_run_modes`, `named_mode`, `resolve_mode`, `mode_composition`, `ModeCapExceeded`,
`admit_targets`, `stands_as_a_gate`, `decides_verdict`);
`guardrails/check-acceptance-rerun.py` (`admitted_acceptance`, `CheckpointUnreadable`, `select`,
`judge`'s loop, `main`'s mode block and its exception arms, the summary prints);
`guardrails.config.json` (`run_modes`, all four modes); `adopt/install-scaffold.sh` (steps a, b and
the `run_modes` seed, with the block's own header comment); `.github/workflows/gates.yml` (gate v's
step); `spec/queue-intake-priority.md` Requirement 322, its Context paragraph and all twenty
criteria; `matrix/build-pipeline.md` M-655..M-667; `tests/test_acceptance_rerun_reach.py` (all eight
new tests, their docstrings, `run_rerun`, `build_fixture`); `tests/test_run_modes.py` (the four new
tests); `tests/test_guardrail_fixture_proofs.py` (`_close_receipt_tree`, `_acceptance_rerun_tree`,
`_run_acceptance_rerun`, `_run_close_receipt`, all four proof halves, `PROVEN`, the four new test
methods); `tests/test_closure_kernel_bypasses.py` (`rerun`); `tests/test_run_modes_install.py` (its
five install cases); `scripts/checkpoint.py` (`read_checkpoint` and its raise sites);
`guardrails/pre-push`; `skills/build-pipeline/SKILL.md` at its description of this gate;
`guardrails/check-prover-record.sh` whole; `docs/prover/README.md`;
`docs/prover/2026-09-08-the-door-learns-two-program-names.md` and
`docs/prover/2026-09-08-the-mode-binds-here-and-not-on-a-host.md`, both whole.

Checks run: fourteen, each with its result below.
`python3 -m pytest -q` over the sixteen files that touch the changed code or read the changed
documents (`test_acceptance_rerun_reach`, `test_closure_kernel_bypasses`, `test_run_modes`,
`test_run_modes_install`, `test_guardrail_fixture_proofs`, `test_probe_reads_state`,
`test_scaffold_guardrails`, `test_traceability`, `test_matrix_reference`, `test_requirement_shape`,
`test_vacuous_pass`, `test_config_health`, `test_index_generated`, `test_gate_common_table_rows`,
`test_suite_hygiene`, `test_row_id_uniqueness`), with `LIVE_SPEC_RUN_MODE` and
`LIVE_SPEC_PUSH_FULL` cleared — 385 passed, 2 skipped, 55 seconds, nothing red;
the same files re-run with `GITHUB_ACTIONS=true CI=true` in the environment, which is how the gates
workflow runs this suite — 1 failed, 116 passed over the seven that drive the gate; the failure is
F1 and it is blocking;
`run_modes.admit_targets` driven against the exact `run_modes` shape the PRE-CHANGE installer
seeded — `row` refuses 40 targets naming the cap of 1, `integration` refuses 40 naming 5, so the
floor reaches a host whose config is never re-seeded; and against the new seed — `row` admits 1 and
refuses 2, `integration` admits 5 and refuses 6, `release` and `manual` admit 500;
`admit_targets` against a config naming `"max_targets": null` — 40 targets admitted under `row`, the
result in F4;
`mode_composition`, `stands_as_a_gate`, `decides_verdict` and `admit_targets` against a config
holding only a `row` key — `KeyError`, not a named refusal, which is F2;
the shipped gate run in a planted host carrying `guardrails/run_modes.py`,
`guardrails/check-acceptance-rerun.py`, `scripts/checkpoint.py`, `scripts/plan_checks_core.py`, a
`PLAN.md`, a `scripts/plan_checks.py` and a `guardrails.config.json` with no `run_modes` key — a
Python traceback out of `_load_run_modes`, exit 1, no verdict, on and off CI; that is F2;
gate v run exactly as the workflow now runs it, `LIVE_SPEC_RUN_MODE=release
LIVE_SPEC_DIFF_BASE=$(git rev-parse origin/main) python3 guardrails/check-acceptance-rerun.py` — 3
of 83 done rows selected (q-489, q-812, q-826), all three run, all three pass, the mode line
printed, exit 0;
the four walks of gate v's own step put through the shipped script on this real range — the `env:`
line deleted (BLOCKED, named no mode, exit 1), the one word changed to `manual` under
`GITHUB_ACTIONS` (BLOCKED, naming the variable, exit 1), the same `manual` with both CI markers
cleared (reports and exits 0), and `row` on this range (BLOCKED by the cap, "1 target(s); 3 were
asked for") — the results are F3 and F6;
all four fixture-proof halves called directly on this tree — `close_receipt_reds_the_bug`,
`close_receipt_passes_the_fix`, `acceptance_rerun_reds_the_bug`, `acceptance_rerun_passes_the_fix`
all True — and the same four called on a clone at `origin/main` — all four False, so the claim that
these pairs were dead is exact;
each of the four fixture halves re-driven with its subprocess output printed, to see whether it
passes for the right reason — one row selected and its own command run in every case, the red half
naming "its acceptance command failed here", the green half naming "every selected row's acceptance
passes here"; not vacuous;
the ORIGINAL `origin/main` fixture pair run against the ORIGINAL `origin/main` gates, to find why
the pairs were dead — all three runs died on `ValueError: missing required metadata key: Status:`
out of `read_checkpoint`, which is F7;
`git log -S` on the summary sentence in `guardrails/check-acceptance-rerun.py` — the wording moved
to "every selected row's acceptance passes here" in 5ca8697c, exactly as the message says;
a red-proof of all sixteen added tests: `git clone --no-hardlinks` of this repo into a scratch
directory checked out at `origin/main`, the four pushed test files copied in over the clone's own,
every other file left at the pre-change state, then `python3 -m pytest` over the sixteen — 11
failed, 5 passed; and the same against a second clone at e7869159 for the twelve e2f819c3 adds — 6
failed, 6 passed. The results are F8;
`grep` across the whole tree — every reader of `named_mode`, `resolve_mode`, `stands_as_a_gate`,
`MODE_LAW`, `LIVE_SPEC_RUN_MODE`, `LIVE_SPEC_PUSH_FULL` and `in_ci`, in hosts, scaffold, skills and
workflows alike; one caller of each and no second spelling of the precedence anywhere, which is F5;
`git status --short` before and after every clone and planted-host run — the tree carries nothing
but this record, the two earlier untracked records and the untracked `inbox/` deposit this pass was
told not to touch.

Findings: nine. Two are blocking and both stand. The three findings the last read refused are
genuinely closed, each proved against the tree rather than read off the message: the cap now binds
on a host whose config carries no `max_targets`, a `manual` mode named on a CI step is refused by
name and by variable, and M-661 and M-662 now carry tests that drive the gate under `row` and under
`integration` and admit. The fixture work is better than the message claims for it — two proof pairs
the pack listed as live had never once been called, both were dead, and calling them found a real
defect in the gate. What holds the push is not the closures. It is that this range reds its own CI
suite in a way no local run shows, and that the mode reader it installs kills the gate outright on a
host whose config pre-dates the four-mode seed — the same host road the last refusal was about, and
the same defect class this very commit fixed for a row's checkpoint.

## F1 — One of this range's own tests reds under CI, and only under CI

`test_a_release_run_decides_the_verdict_and_a_manual_run_decides_none` (added by e7869159) drives
the gate under `manual` and asserts it exits 0 with the faults reported. `run_rerun` builds its
environment as `dict(os.environ, ...)` and pops `LIVE_SPEC_EVALUATING` and `LIVE_SPEC_PUSH_FULL`
only. `GITHUB_ACTIONS` and `CI` ride through untouched.

e2f819c3's own F2 repair reads exactly those two variables. So on any machine where either is set —
which is every GitHub Actions runner, and this suite runs there — the manual arm is refused by the
new guard and the test's `assert audit.returncode == 0` fails. Proved by running the same file
twice against this tree:

- `env -u GITHUB_ACTIONS -u CI python3 -m pytest -k release_run_decides_the_verdict` — 1 passed.
- `env GITHUB_ACTIONS=true CI=true python3 -m pytest -k release_run_decides_the_verdict` — 1 failed,
  the assertion carrying the gate's own refusal text: "this is a CI run (GITHUB_ACTIONS is set) and
  mode 'manual' may never stand as a CI or release gate".

The seven files that drive the gate were then swept the same way: 1 failed, 116 passed. It is this
one test and no other.

This is not a cosmetic ordering problem. The commit that closes F2 makes a test written in the
commit below it red, on the one machine whose verdict counts, and the message's own run — "436
passed, 2 skipped" — was taken where the markers were unset, so nothing said a word. A range whose
CI cannot be green is not pushable, and this one cannot: gate w runs this suite in Actions.

What would close it: clear `GITHUB_ACTIONS` and `CI` in `run_rerun` the way it already clears
`LIVE_SPEC_PUSH_FULL`, so a test that means "off a CI step" says so rather than inheriting an
answer, and leave `test_a_manual_run_may_not_stand_as_a_gate_in_ci` to set the marker deliberately,
which it already does. One line, and it makes both halves of criterion 8 testable side by side
instead of one of them depending on where the suite is run.

`defect · a-test-whose-verdict-depends-on-where-it-runs (safety)`

## F2 — The mode reader kills this gate outright on a host whose config pre-dates the seed

`_load_run_modes` does `cfg["run_modes"]` and `mode_composition` does `run_modes[mode]`, neither
guarded. `adopt/install-scaffold.sh` seeds the `run_modes` key only when it created the config file
in this same run (`CONFIG_SEEDED`); a host that already carried a `guardrails.config.json` is told,
in the installer's own words, `skip (guardrails.config.json pre-dates this install, keep your
tuning): run_modes`. That host gets the vendored `check-acceptance-rerun.py` and the vendored
`run_modes.py` and a config with no `run_modes` key in it.

Proved, not reasoned. A host was planted holding `guardrails/run_modes.py`,
`guardrails/check-acceptance-rerun.py`, `scripts/checkpoint.py`, `scripts/plan_checks_core.py`, a
`PLAN.md` with one done row, a `scripts/plan_checks.py` naming its key, and
`guardrails.config.json` holding `{"paths": {}}`. Under `LIVE_SPEC_RUN_MODE=release` the run ends in
a Python traceback out of `run_modes.py` line 38, `KeyError: 'run_modes'`, exit 1, no verdict, no
sentence a reader can act on. With `CI=1` the traceback comes one frame earlier, out of
`stands_as_a_gate`. Before e7869159 that host ran this gate and got a verdict.

The partial shape is worse, because the pack ships a fixture of it. `mode_composition` was driven
against `{"row": {...}}` — a config naming `row` and no other mode — and every entry point raises
`KeyError: 'manual'`. That is the exact config `tests/test_run_modes_install.py`
`test_a_hosts_own_run_modes_is_left_untouched` plants to prove the installer leaves a host's tuning
alone. The pack writes that shape in its own suite and never once runs the gate against it.

This is the same defect class e2f819c3 fixed one file over. Its own docstring, on
`admitted_acceptance`: "Before this, an unreadable checkpoint took the whole gate down with a
traceback and no verdict at all." A config the mechanism itself reads now does precisely that, and
the fix is the same three lines. It fails closed, so no false green rides on it — but a gate that
cannot say what is wrong on the host road is the thing the last refusal was about, and the host road
is where this mechanism was found unbound yesterday.

What would close it: the same shape `TableUnreadable` and `CheckpointUnreadable` already use — a
named exception out of `_load_run_modes` and `mode_composition`, caught in `main`, printing which
key this host's `guardrails.config.json` is missing and that `adopt/install-scaffold.sh` seeds the
four names. No new parameter, no new number.

`defect · the-gate-dies-where-it-cannot-read-its-own-contract (safety)`

## F3 — F1 of the last read is closed, and the floor reaches the hosts it had to reach

The last read refused e7869159 because `admit_targets` refused only where a config named
`max_targets`, and the installer seeded none, so a `row` run on a host admitted forty targets
silently. Both halves of the repair were driven directly.

The exact PRE-CHANGE seed shape — `row: {decides_verdict, emergency_timeout_seconds,
timeout_is_never_a_verdict}`, `integration: {the same three, layer_map}` — was put through the
shipped `admit_targets` against this tree's module. `row` refuses forty targets naming a cap of 1;
`integration` refuses forty naming 5. That is the case that matters most, and it is the one the
message does not spell out: the never-clobber promise means a host that installed yesterday keeps
its capless config forever, so the repair had to live in the module rather than the seed, and it
does. `MODE_LAW` is read through `composition.get("max_targets", MODE_LAW.get(mode))`, so an absent
key falls to the pack's law and a config that names a cap still owns it.

The seed's own copy was checked too, and the new shape refuses at 2 and at 6 and admits at 1 and at
5. Both figures are criterion 2's and criterion 3's own, so nothing here is a number pulled from the
air.

`release` and `manual` carry no law and admit what they are given. That is right rather than a
second hole: a `release` run's composition is its versioned core list (criterion 5), which is a
different mechanism from a target cap, and a `manual` run decides no verdict at all (criterion 8) so
there is no verdict for a cap to bound. The one thing a cap would buy for `manual` — that it cannot
be the vehicle for an unbounded run — is bought instead by F5's CI refusal.

One residual, in F4.

`no test · closed (completeness)`

## F4 — `"max_targets": null` walks the floor, and the installer's own header says the opposite

`composition.get("max_targets", MODE_LAW.get(mode))` falls to the law when the key is ABSENT. A
config carrying `"max_targets": null` returns `None` and admits whatever it is given: driven, 40
targets under `row`. That spelling is not exotic in this pack — `guardrails.config.json` writes
`"emergency_timeout_seconds": null` in all four modes, so null is this file's own idiom for "no
figure here".

The installer's inline comment says "guardrails/run_modes.py carries the same two figures as its
floor, so a host that edits these keys away still gets them". That is true of a deletion and false
of a null, which is the likelier edit given the file's own habits.

Eight lines above it, the block's header comment still reads "The host owns every budget under it —
max_targets, the release core list, the layer map, timeouts". The commit's whole F1 repair rests on
max_targets NOT being the host's budget, and the new comment directly below says so. Two comments in
one block now contradict each other about the one figure the commit changed, and the stale one is
the one a reader meets first.

The module's docstring says a config "MAY name a lower cap; a higher one is its own business", so
widening is a stated stance rather than an oversight — which is why this is not blocking. It is
still worth closing, because the null spelling widens to infinity without anybody meaning to.

What would close it: `cap = composition.get("max_targets") or MODE_LAW.get(mode)` — or, if a
deliberate infinity must stay expressible, say so in the docstring — and rewrite the header comment
so the block says one thing about who owns `max_targets`.

`defect · a-floor-with-one-spelling-under-it (safety)`

## F5 — F2 of the last read is closed for the direction it named, with two edges left

`stands_as_a_gate` reads the mode's own `in_ci` key, which `manual` ships as false and which nothing
in the tree read before. `main` pairs it with `next((name for name in ("GITHUB_ACTIONS", "CI") if
os.environ.get(name)), None)`. All four walks of gate v's step were run against this real range:

- the `env:` line deleted — "BLOCKED — this run named no mode", exit 1. The safe direction is still
  loud, which was the last read's own test of this repair.
- the one word changed to `manual`, `GITHUB_ACTIONS` set — "BLOCKED — this is a CI run
  (GITHUB_ACTIONS is set) and mode 'manual' may never stand as a CI or release gate", exit 1, and
  the message names the variable. The one-word green is gone.
- `row` on this range — BLOCKED by the cap, "1 target(s); 3 were asked for". Narrowing the mode is
  not a silent green either.
- `manual` with both markers cleared — reports the rows and exits 0, which is the audit the mode is
  for.

Two edges remain, and neither is blocking. The marker list is two names: a CI that sets neither —
Jenkins and TeamCity set neither by default — never trips the guard, and `env -u CI -u
GITHUB_ACTIONS` walks it from inside one that does. On GitHub Actions itself the walk is not
available, since `GITHUB_ACTIONS` cannot be set from a workflow's own `env:`, so the road this pack
actually runs on is held. And the last read asked for a second thing that did not arrive: no test
reads `.github/workflows/gates.yml` for gate v's step, so the `LIVE_SPEC_RUN_MODE: release` line is
still pinned by nothing. That matters less than it did, because every direction that line can be
edited in is now either loud or a narrower real verdict.

Nothing else in the tree needs this reader: `grep` finds one invocation of the script,
`guardrails/pre-push` does not call it, and no other check consults a mode.

`no test · closed with two edges (safety)`

## F6 — F3 of the last read is closed for M-662 and all but one clause of M-661

M-662 was rewritten rather than re-evidenced, which is one of the two repairs the last read named:
"No registry of forbidden verifier commands is kept anywhere in the mechanism" became "The
acceptance run keeps no registry of forbidden verifier commands: a key naming a test runner and a
key merely mentioning one are both run like any other key". Its one test plants exactly those two
keys and asserts both run. The row now says what the test holds. Honest.

The cost is named here rather than left implicit: criterion 14 says "the system shall keep no
registry of forbidden verifier commands", and after this narrowing no row in the matrix holds the
"anywhere" reach. `scripts/task-admission.py` — where a two-name registry was written this
afternoon and refused — is not covered by any row. The last read offered the narrowing as one of two
acceptable closures, so this is a closure and not a defect, but the pack now has no guard against
the next registry being written at the door.

M-661 keeps its text and gains four tests, two of them admissions:
`test_a_row_run_takes_its_one_target_and_decides_on_it` narrows a fixture to one affected row and
asserts the gate takes it, runs its command and prints "run mode: row — it decides the verdict
below"; `test_an_integration_run_covers_the_targets_it_names_and_decides_a_verdict` does the same
for three rows under `integration`. Both were driven and both are real: the sentinels for the taken
rows exist and the untouched row's does not. The clause the last read said was held by nothing —
"admitted in a `row` run and in an `integration` run" — is held now.

Criterion 12 reads "a targeted test run" and the two admission tests admit rows whose commands are
`touch sentinel-*.txt`. The one test that runs a command actually naming a test runner,
`test_the_gate_judges_no_program_name`, runs under `release`. So the criterion is held as "a target
is admitted under row and under integration", one assertion short of its literal words. That is
close enough to call criterion 12 held, and one line — a key naming `pytest --version` in either
admission fixture — would make it exact.

M-657 and M-658 are untouched and still say *built* over unit tests of the cap alone, which is the
third time in three records that this has been raised (the first read's F5, the second read's F6).
M-657 promises "the one currently accepted task's own deterministic acceptance command"; this gate
selects by what moved in the pushed range and has no notion of an accepted task. A row's status word
that survives three reviews is not going to be fixed by a fourth mention, so it is named here once
and left as a standing item for the owner rather than repeated as a finding.

`no test · closed with a residual (completeness)`

## F7 — The dead-proof work is real, and the comment beside it names the wrong cause

The message's strongest claim is its most checkable, and it holds. At `origin/main`,
`tests/test_guardrail_fixture_proofs.py` listed six checks in `PROVEN` and carried test methods for
four; `close_receipt_*` and `acceptance_rerun_*` had none. Both pairs were called directly on a
clone at `origin/main`: all four halves returned False. Called on this tree: all four return True.
A pair that returns False on both halves and is called by nothing is a check the pack believed it
had proved and had not.

The four halves were then re-driven with their subprocess output printed, to see whether they now
pass for the right reason rather than vacuously. Each one selects its single planted row and runs
that row's own command: `acceptance_rerun_reds_the_bug` gets "q-1: its acceptance command failed
here, at this commit" and exit 1 over a fixture whose command is `false`;
`acceptance_rerun_passes_the_fix` gets "1 selected here", "ran 1", "every selected row's acceptance
passes here" and exit 0 over the same fixture with `true`; the close-receipt pair reds on "holds no
acceptance receipt" and greens on "stands on a passed acceptance receipt". None of the four is
vacuous, and the red half fails for the reason it names.

The defect this found in the gate is real too, and is the best thing in the range: a selected row
whose checkpoint will not parse used to take the run down with a traceback. `CheckpointUnreadable`
was read for what it swallows — `read_checkpoint` raises only `ValueError` in this tree, `cp.exists()`
already guards the missing file, and every case now caught was a case that previously killed the
whole run. No row that the old code would have run correctly becomes a fault; the direction is
always toward a red on that one row, never toward a pass, and the other selected rows still run,
which the new test asserts and which the live gate-v run shows.

The wrong part is the cause. The section comment above the four new methods says the acceptance
pair went dead "when its gate began requiring a named mode" — that is this range's own change, at
e7869159. Both pairs were dead at `origin/main`, before any mode was required. Driven there against
the original gates: all three runs die on `ValueError: missing required metadata key: Status:` out
of `read_checkpoint`, because the fixture wrote a blank line between its title and its metadata.
That single cause explains both pairs and both halves; the mode and the stale sentence are causes
only from e7869159 forward, once the shape is fixed. The commit message lists all three as reasons
"both halves returned False", which is true at the tip and not true of when the pairs died. The
"stale since 5ca8697c" half was checked with `git log -S` and is exactly right.

What would close it: say in the comment that the fixture's own checkpoint shape is what killed both
pairs, and that the mode and the sentence were found behind it. The date a proof died is the only
thing that says how long the pack was wrong about what it had proved.

`defect · a-comment-that-dates-a-death-to-the-wrong-commit (traceability)`

## F8 — The red-proof of all sixteen added tests, and what each one holds

The range adds sixteen tests, not the nine a reader of the two messages would count. All sixteen
were red-proved: this repo cloned with `git clone --no-hardlinks` into a scratch directory and
checked out at `origin/main`, the four pushed test files copied in over the clone's own, every other
file left at the pre-change state.

Failed against `origin/main` — 11, each holding something the range built:
`test_a_run_that_names_no_mode_is_refused_before_it_selects_anything`,
`test_a_row_run_is_refused_by_its_own_cap_when_more_than_one_row_is_affected`,
`test_a_release_run_decides_the_verdict_and_a_manual_run_decides_none`,
`test_a_manual_run_may_not_stand_as_a_gate_in_ci`,
`test_an_integration_run_covers_the_targets_it_names_and_decides_a_verdict`,
`test_an_unreadable_checkpoint_reds_its_row_instead_of_killing_the_run`,
`test_a_row_run_takes_its_one_target_and_decides_on_it`,
`test_a_mode_carrying_no_cap_falls_to_the_packs_own_law`,
`test_the_host_seed_carries_the_two_caps_the_law_names`,
`test_named_mode_answers_none_where_nothing_named_one`,
`test_only_manual_is_barred_from_standing_as_a_gate`.

Passed against `origin/main` — 5. `test_the_gate_judges_no_program_name` says so in its own
docstring, in advance, and explains why it is a standing guard rather than a proof; that docstring is
the most useful one in the range. The four fixture-proof methods pass there because what was broken
lived in the test file itself — carry the fixed fixtures back and the old gates satisfy them. They
hold the fixture repair, which is a real thing to hold, and no docstring in that block claims they
prove the gate changed.

Against a second clone at e7869159, the twelve tests e2f819c3 adds split 6 failed / 6 passed. The
six that pass there — the two admission tests, and the four fixture methods — hold e7869159's code
rather than e2f819c3's. That is not a defect: the range is what a record covers, and all twelve are
red against the range's base. It is worth writing down so nobody later reads twelve tests in one
commit as twelve proofs of it, which is the reading error both earlier records refused.

Every other docstring in the range was read against what its test does, and each is true. Two are
loose about their citation rather than their content:
`test_a_run_that_names_no_mode_is_refused_before_it_selects_anything` cites M-661, but a run naming
its kind before it selects is criterion 1, which no matrix row carries at all. That is a gap in the
matrix, not in the test.

`no test · the-count-of-tests-is-not-the-count-of-proofs (completeness)`

## F9 — Every remaining claim in both messages, checked one at a time

- "`admit_targets` refused only where a config named `max_targets`, and the seed writes none, so a
  `row` run on an installed host took forty targets without a word" — true, reproduced against the
  pre-change seed shape.
- "`guardrails/run_modes.py` now carries them as the floor a missing key falls to, and the seed
  names them outright as well. Proved against the exact seeded shape the review used" — true, both
  halves driven.
- "`run_modes.stands_as_a_gate` is that reader, and the run refuses when a CI marker is set and the
  mode may not stand as a gate, naming the variable that made it a CI run" — true, and the variable
  is named in the printed line.
- "The safe direction stays as it was: deleting the line is a loud refusal" — true, run.
- "two tests now drive the gate under each, take the targets and decide a verdict, and they hold
  criterion 12 with them, which nothing held before" — true but for the literal reading in F6; both
  tests pass at e7869159, so they are evidence for the row rather than for this commit.
- "the row now says what it holds, the acceptance run" — true, M-662's text was rewritten.
- "it lives in `run_modes.named_mode` now, and `resolve_mode` is that read with the default on top"
  — true. Grepped the whole tree, hosts and scaffold included: `named_mode` has one caller,
  `resolve_mode` none outside its own test, and no second spelling of the precedence exists
  anywhere. The two disagreements the last read found are gone: `LIVE_SPEC_RUN_MODE=""` now answers
  None instead of raising, and `LIVE_SPEC_PUSH_FULL=yes` names release, matching what
  `guardrails/pre-push` has always treated as on. No branch of `named_mode` fails open — an unknown
  name still raises, a blank one answers None, and the caller refuses on None.
- "the cap refusal carries its own exception type, so a fault inside `judge` is no longer reported in
  the mode's words" — true. `ModeCapExceeded` subclasses `ValueError`, `main` catches it by its own
  name, and the wide `except ValueError` is gone.
- "lists six checks as owning a live fixture proof, and only four had a test that called one" —
  true at `origin/main`, counted.
- "both halves of this gate's pair returned False" — true; the three causes it names are true at the
  tip and not at the death, which is F7.
- "All four now have tests" — true, and all four pass.
- "a selected row whose checkpoint does not parse took the whole run down with a traceback and no
  verdict at all. It is now a fault on that row, named, with the other selected rows still judged" —
  true, and independently reproduced against the pre-change clone.
- "Ran: 436 passed, 2 skipped over the thirteen files touching this code" — the thirteen are not
  enumerated, so the number could not be reproduced. This pass ran sixteen files chosen the same way
  and saw 385 passed, 2 skipped with the CI markers unset. Nothing behind either number is red with
  the markers unset; with them set, F1.
- One doc still lags, carried from the last read's F7 and not fixed here:
  `skills/build-pipeline/SKILL.md` line 110 still says this gate "takes every done row carrying an
  admitted key and runs that key at the pushed commit", which is stale about the range and now stale
  about the mode. A host wiring the gate from that sentence gets an unconditional exit 1 and no hint
  why — or, on a config that pre-dates the seed, F2's traceback.

## On the two records already on disk

Both are untracked and both should be committed with this one, in the same commit as this record.
The push gate is satisfied by that: `guardrails/check-prover-record.sh` globs every tracked
`docs/prover/2026-09-08*.md`, then walks them looking for ONE that names the base short sha and
every reviewed commit, breaking at the first match. This record names 5be3dd27, e7869159 and
e2f819c3, so it matches; the other two name commits this range does not fully cover and are simply
passed over, which costs nothing. `docs/prover/README.md` already provides for records that no push
carries — "a milestone re-prove, a periodic audit" live in the same directory under the same naming
— and a record of a refused push is exactly that. Committing all three together satisfies the gate
and is the right thing besides: they are the written reasons the first approach was dropped and the
second was reworked, and this record leans on both.

One thing the pusher must do, which this pass could not: the door record's `Range:` names 4af78315,
a commit no branch contains. It still resolves in this working repo and will resolve in no clone.
Add one line at that record's head saying the range it covers was dropped from the branch and what
replaced it, exactly as the second record asked. This pass left both files byte-for-byte as it found
them.

## The verdict on the range

The three findings that refused e7869159 are closed, and each was checked against the tree rather
than against the message. The cap now binds on a host whose config was never re-seeded, which was
the whole of the last refusal's first item and is the one that had to live in the module rather than
the seed. `manual` on a CI step is refused by name and by variable, and the safe direction is still
loud. M-661 and M-662 now carry tests that admit under `row` and under `integration` and a row text
that says what its test holds. The fixture work goes further than the message sells it: two proof
pairs the pack listed as live had never been called, both were dead since before this range, and
calling them turned up a real defect in the gate that is now fixed and tested.

The range is not safe to push as it stands, for one reason that is arithmetic rather than judgement:
one of its own tests fails on a CI runner and passes everywhere else, because it inherits the two
variables this range taught the gate to read. The push cannot be green. That is a one-line fix and
it should be made before this record's checks are re-run.

The second reason is the host road again. The mode reader this range installs reads a config key
that the pack's own installer promises never to add to a host that already had a config, and where
the key is missing the gate dies with a traceback instead of saying which key. The same commit
carries a careful, well-tested repair of exactly that defect one file over, for a row's checkpoint.
It is the same three lines and the same reasoning; it just was not applied to the contract the
mechanism reads about itself.

What a reader of this record should be wary of, in order:

- **The suite is green here and red in Actions** (F1). One test, one line, and no local run will
  ever show it.
- **On a host with a pre-existing config the gate cannot start** (F2), and the pack's own install
  test plants that config shape without ever running the gate against it.
- **`"max_targets": null` walks the new floor** (F4), and the installer's header comment still says
  the host owns the figure the commit just took away from it.
- **Sixteen tests, eleven of them red before the range** (F8). Five are standing guards, and the
  block's own comment misdates why two proofs were dead (F7).

The whole suite was left to CI. This pass ran the sixteen files that touch the changed code or read
the changed documents, twice — once with the CI markers cleared and once with them set — plus every
command named above; no finding here rests on a suite total.

Blocking: two, and both stand.
- F1 stands: `test_a_release_run_decides_the_verdict_and_a_manual_run_decides_none` inherits `GITHUB_ACTIONS` and `CI` through `run_rerun`'s `dict(os.environ, ...)`, and e2f819c3's own CI guard then refuses the manual arm it asserts exits 0 — proved by running that one test twice against this tree, passing with the markers cleared and failing with them set, and by sweeping the seven gate-driving files under the markers for 1 failed, 116 passed. The suite cannot be green in Actions, so this range cannot be pushed green. It closes by clearing both markers in `run_rerun`, the way it already clears `LIVE_SPEC_PUSH_FULL`.
- F2 stands: `run_modes._load_run_modes` and `mode_composition` read `cfg["run_modes"]` and `run_modes[mode]` unguarded, and `adopt/install-scaffold.sh` never adds the `run_modes` key to a host whose `guardrails.config.json` pre-dates the install — proved by running the shipped gate in a planted host of exactly that shape, where it ends in a `KeyError` traceback, exit 1 and no verdict, on and off CI, and by driving every entry point against the partial config `tests/test_run_modes_install.py` itself plants, which raises `KeyError: 'manual'`. Before e7869159 that host got a verdict. It closes the way this same commit closed the identical defect for a row's checkpoint: a named exception out of the reader, caught in `main`, printing which key the host's config is missing and that `adopt/install-scaffold.sh` seeds the four names.
