# Prover record — 2026-09-08 the mode binds here and not on a host

PUSH-REVIEW

The pass was run by a seat that authored none of this commit, briefed to find reasons to refuse it
and to hold it defective until evidence said otherwise. Every judgement below about what the gate
admits, refuses or returns was taken by running the shipped script or the shipped function, never by
reading the code and reasoning about it. Where the commit message states a number or a red-proof,
it was recomputed against this tree and against a clean clone of the pre-change one.

Range: 5be3dd27..e7869159 — the base the remote holds, then the one commit this push sends.

- e7869159 The acceptance run names its mode, and the mode binds what it may take — `run_modes`
  imported by `guardrails/check-acceptance-rerun.py`, a refusal for a run that named no mode, the
  selection put through `run_modes.admit_targets`, a `decides_verdict` arm, `LIVE_SPEC_RUN_MODE:
  release` on gate v's step in `.github/workflows/gates.yml`, matrix rows M-661 and M-662 moved to
  *built*, four new tests in `tests/test_acceptance_rerun_reach.py` and a changed helper in
  `tests/test_closure_kernel_bypasses.py`.

Files read: the commit's own diff and message; `guardrails/check-acceptance-rerun.py` whole
(module docstring, `acceptance_table`, `select`, `run_one`, `judge`, `main`);
`guardrails/run_modes.py` (`resolve_mode`, `mode_composition`, `admit_targets`, `decides_verdict`);
`guardrails.config.json` (`run_modes`, all four modes); `.github/workflows/gates.yml` (gate v's
step and its neighbours); `spec/queue-intake-priority.md` Requirement 322 with its Context
paragraph and all twenty criteria; `matrix/build-pipeline.md` M-655..M-667;
`tests/test_acceptance_rerun_reach.py` (the four new tests, their docstrings, `run_rerun`,
`build_fixture`); `tests/test_closure_kernel_bypasses.py` (`rerun` and its four callers);
`tests/test_run_modes.py` (every test name); `tests/test_guardrail_fixture_proofs.py`
(`_acceptance_rerun_tree`, `_run_acceptance_rerun`, both fixture-proof halves, `PROVEN`, the test
methods that drive it); `adopt/install-scaffold.sh` (the vendor list and the `run_modes` seed);
`adopt/install-status-view.sh` (its vendor list); `guardrails/pre-push` (its check list and its
`LIVE_SPEC_PUSH_FULL` arm); `skills/build-pipeline/SKILL.md` at its description of this gate;
`guardrails/check-prover-record.sh`; `docs/prover/README.md`;
`docs/prover/2026-09-08-the-door-learns-two-program-names.md` whole.

Checks run: nine, each with its result below.
`python3 -m pytest -q tests/test_acceptance_rerun_reach.py tests/test_closure_kernel_bypasses.py
tests/test_run_modes.py tests/test_run_modes_install.py tests/test_guardrail_fixture_proofs.py
tests/test_probe_reads_state.py`, with `LIVE_SPEC_RUN_MODE` and `LIVE_SPEC_PUSH_FULL` cleared from
the environment so no test could borrow a mode from the shell — 78 passed;
`python3 -m pytest -q` over the ten further files that read `matrix/build-pipeline.md`,
`.github/workflows/gates.yml` or `guardrails.config.json` and could react to a row's status word
moving (`tests/test_traceability.py`, `tests/test_matrix_reference.py`,
`tests/test_requirement_shape.py`, `tests/test_vacuous_pass.py`, `tests/test_index_generated.py`,
`tests/test_gate_common_table_rows.py`, `tests/test_suite_hygiene.py`,
`tests/test_row_id_uniqueness.py`, `tests/test_config_health.py`,
`tests/test_scaffold_guardrails.py`) — 295 passed, 2 skipped; 373 passed and 2 skipped over the
sixteen files together, nothing red;
gate v run exactly as the workflow now runs it, `LIVE_SPEC_RUN_MODE=release
LIVE_SPEC_DIFF_BASE=$(git rev-parse origin/main) python3 guardrails/check-acceptance-rerun.py` — 2
of 83 done rows selected (q-812 and q-826, each because a file its acceptance command names moved
in the range), both pass, the summary prints the mode line, exit 0;
the mode guard's four edge cases put through the shipped script directly — both variables unset,
`LIVE_SPEC_PUSH_FULL=yes`, `LIVE_SPEC_RUN_MODE=""` and `LIVE_SPEC_RUN_MODE=nightly` — the results
are F5;
`run_modes.admit_targets` called against this tree's own `guardrails.config.json` and, separately,
against the exact `run_modes` shape `adopt/install-scaffold.sh` seeds onto a host — the results are
F1;
a red-proof of the four new tests: `git clone --no-hardlinks` of this repo into a scratch
directory, `git checkout e7869159^` there, the pushed `tests/test_acceptance_rerun_reach.py` copied
in over the clone's own, `python3 -m pytest -q tests/test_acceptance_rerun_reach.py` in that clone
— the result is F10;
both halves of this check's registered fixture proof driven directly,
`test_guardrail_fixture_proofs.acceptance_rerun_reds_the_bug()` and
`.acceptance_rerun_passes_the_fix()`, on this tree and on the pre-change clone — the result is F7;
`grep` across the tree for every invocation of `check-acceptance-rerun.py`, every reader of
`LIVE_SPEC_RUN_MODE`, `LIVE_SPEC_PUSH_FULL` and `run_modes`, every reader of the config's `in_ci`
key, and every trace of `names_no_target` — the results are F2, F4 and F7;
`git status --short` before and after the red-proof — the tree carries nothing but this record, the
earlier untracked record and the untracked `inbox/` deposit this pass was told not to touch.

Findings: ten. Three are blocking and all three stand. The design is right and it is a real
improvement: the judgement moved from the admission door, where it read command text, to the run
itself, where a mode and a composition are actually known, and it judges no command text at all.
The refused approach is gone — `names_no_target` appears nowhere in the tree and no program name is
matched anywhere in this commit. What it does not hold is the binding it claims: the cap it rests
on is absent on every host the pack installs onto and fails open there, a one-word edit to the
workflow now turns a release gate green with faults printed, and the two matrix rows this commit is
named for wear *built* over tests that hold less than the rows promise — the same reading error the
earlier review refused this afternoon, in the same two rows.

## F1 — The cap this commit rests on is absent on every host `adopt/` installs, and it fails open

`run_modes.admit_targets` refuses only when the mode's composition carries a `max_targets` key: "A
mode carrying no cap (max_targets absent) admits whatever it is given". In this repo's own
`guardrails.config.json` the two caps are there, and both were exercised: `row` refuses two targets
naming the cap, `integration` refuses six, `release` and `manual` admit five hundred.

`adopt/install-scaffold.sh` seeds a host's `run_modes` with neither cap. Its seed is, verbatim,
`row: {decides_verdict, emergency_timeout_seconds, timeout_is_never_a_verdict}` and `integration:
{the same three, layer_map}`. Put that exact shape through the shipped function: `row` admits forty
targets and `integration` admits forty, with no refusal, no warning and no line in the summary
saying a cap was looked for and not found. The gate then runs whatever the range selected, under a
mode name that says it may run one.

The installer's own comment calls this deliberate — "The host owns every budget under it —
max_targets, the release core list, the layer map". For the release core and the layer map that is
right; for these two figures it is not. Criterion 2 fixes a `row` run at "at most one target".
Criterion 3 fixes an `integration` run at "at most five named targets, the figure taken from the
pack's own `MOST_DELIVERABLES`" — the requirement names the source and the pack owns it. Those two
numbers are the mechanism's law, which criterion 20 says the pack ships, not the host's budget,
which criterion 20 says the host keeps. Seeding them out puts the pack's law in the host's hands and
defaults it to absent.

The direction it fails is the wrong one. A missing cap could refuse, or print that the mode names no
bound, and either would be loud. It admits, silently, and the mechanism this commit exists to give
its first caller then binds nothing at all on a host.

What would close it: seed `row: {"max_targets": 1}` and `integration: {"max_targets": 5}` with the
rest, since criteria 2 and 3 own those two figures; or have `admit_targets` refuse a mode that
decides a verdict and carries no cap, so an absent bound is a stop rather than a pass. Either is a
few lines and neither invents a number — both figures are already written in the requirement.

`defect · a-bound-that-is-absent-where-it-ships (safety)`

## F2 — One word in the workflow turns a release gate green, and nothing holds it out

Criterion 8 has two halves: a `manual` run "shall never stand as a CI or release gate", and it
"shall decide no verdict". This commit builds the second half and nothing in the pack builds the
first.

`guardrails.config.json` carries `"in_ci": false` under `manual`. Grepped across the tree: no code
reads that key. The script does not ask whether it is running in CI, on any mode. And no test reads
`.github/workflows/gates.yml` for gate v's step or its environment — grepped, and the ten
workflow-reading test files were run.

So `LIVE_SPEC_RUN_MODE: release` on that step is held in place by nothing but the line itself.
Change that one word to `manual` and gate v prints every failing row and exits 0, under a line that
reads "the 'manual' run reports the row(s) above and decides no verdict on them" — a sentence that
looks like a considered decision rather than a disarmed gate. The suite stays green, because nothing
in it looks at that step. Deleting the line instead is safe: the run is refused, exit 1, loudly. It
is only the dangerous direction that is unguarded.

This gate exists because a receipt anybody can type was buying a passing acceptance. Before this
commit there was no word that could make it pass over a failing row. There is one now, and the
person who can write it is anybody who can edit a workflow — which is anybody who can push. That
this needs a privileged act is not much comfort: so did editing the receipt.

The rest of the road is clear, and was checked rather than assumed. `guardrails/pre-push` does not
run this script at all — its check list carries no reference to it — so nothing local reads this
exit code, and the manual arm weakens no other gate. `.github/workflows/gates.yml:134` is the one
invocation of the script in the tree, and a step-level `env` in Actions is not overridable by a
repository variable, so the release name cannot be displaced from outside.

What would close it: read the key the config already carries — refuse `manual` when the environment
says CI — and add one test that reads gates.yml and holds that gate v's step names a mode which
decides a verdict. Neither adds a parameter; `in_ci` is already written and currently binds nothing.

`defect · a-gate-that-can-be-stood-down-by-one-word (safety)`

## F3 — M-661 and M-662 wear *built* over tests that hold less than the rows say

M-661's own text: "A check judges an acceptance command's mode and composition; never the name of
the program that runs it — a command naming `pytest` is admitted in a `row` run and in an
`integration` run once its mode and composition are right". The two tests it now names are
`test_a_run_that_names_no_mode_is_refused_before_it_selects_anything`, which holds criterion 1, and
`test_a_row_run_is_refused_by_its_own_cap_when_more_than_one_row_is_affected`, which holds the cap.
Both are refusals. Nothing in the range admits anything under `row`, and nothing anywhere drives
this gate under `integration` at all — the clause after the dash, which is the row's whole point and
is criterion 12 word for word, is held by nothing. The row promises an admission and its tests prove
two refusals.

M-662's own text: "No registry of forbidden verifier commands is kept anywhere in the mechanism".
Its test, `test_the_gate_judges_no_program_name`, plants two keys — one running a test runner, one
merely mentioning its name — and asserts both run in this one script. That is a two-command
behavioural sample of one of the several places the mechanism lives: `scripts/task-admission.py`,
`scripts/plan_checks_core.py` and the board renderer are the others, and the second of them is where
the registry was written this afternoon. "Anywhere" is what a static read of those files holds, and
a static read is what a row worded like this asks for. The test's own docstring is honest — it says
plainly that it is a standing guard which passes against the earlier gate — and the red-proof
confirms it. The docstring tells the truth; the row's status word does not.

This is the same pattern the earlier record refused today in its F4 and F6, in these same two rows:
a count of tests read as a count of proofs, and a row's status word moved further than its evidence.
It should not be the thing that recurs in the commit written to answer it.

What would close it: narrow both rows to what their tests hold, or write the two tests the rows
promise — one that admits a targeted key under `row` where exactly one row is affected and under
`integration`, and one that reads the mechanism's files for a program-name list. The second is the
row that would have caught this afternoon's defect; a behavioural sample of one script will not
catch the next one written somewhere else.

`defect · a-row-marked-built-over-a-partial-test (completeness)`

## F4 — Criterion 12 is still unheld, and this range does not reach it

Criterion 12: "The system *shall* admit a targeted test run in a `row` run and in an `integration`
run." The earlier record found nothing holding it. Nothing holds it now either.

Every drive of this gate in the range names `release` or `manual`, except the one that names `row`
and is refused by the cap. `tests/test_run_modes.py` holds
`test_row_admits_one_target_and_refuses_two_naming_the_cap`, but that calls `admit_targets` as a
function on a list of one string — it is the cap's arithmetic, not a targeted run admitted by a
check. No test in the tree admits a real acceptance command under `row`, and no test names
`integration` to any caller of `run_modes` outside `admit_targets` itself.

Said plainly: criterion 12 is unheld, and the row that cites it now says *built*. It closes with
F3's first repair.

`defect · a-criterion-unheld-by-the-row-that-cites-it (completeness)`

## F5 — The mode refusal reads the two variables itself instead of asking the module

The block in `main` reads `os.environ.get("LIVE_SPEC_RUN_MODE") is None` and
`os.environ.get("LIVE_SPEC_PUSH_FULL") != "1"`, which is `resolve_mode`'s own precedence written a
second time in a second file. All four edge cases were put through the shipped script:

- both unset — "BLOCKED — this run named no mode", exit 1. Right answer.
- `LIVE_SPEC_PUSH_FULL=yes` — "BLOCKED — this run named no mode", exit 1. `guardrails/pre-push`
  treats any non-empty value of that variable as on (`[ -n "$PUSH_FULL" ]`); `run_modes` and this
  block both require exactly `1`. Two spellings of the same switch in one pack, and this one refuses
  the spelling the other accepts.
- `LIVE_SPEC_RUN_MODE=""` — "BLOCKED — unknown run mode ''", exit 1. An empty value is precisely a
  run that named no mode, and it takes the other branch and gets the other message.
- `LIVE_SPEC_RUN_MODE=nightly` — "BLOCKED — unknown run mode 'nightly'", exit 1. Right answer.

No case admits a run that `resolve_mode` would have handed a default, so today the divergence costs
a message rather than a verdict, and every arm exits 1. It is still the resolution order living in
two homes: a variable added to `resolve_mode` tomorrow will not reach this block, and the two will
then disagree in the direction that matters.

What would close it: a truthy read rather than an `is None` one, and the precedence asked of the
module that owns it — one function in `run_modes` answering whether the environment named a mode at
all, called from here.

`defect · one-fact-with-two-homes (traceability)`

## F6 — On this gate `integration` is a ceiling, and `row` can only refuse

The config says an `integration` run's targets are "only the layers a change touched, each resolved
through this mode's own layer_map to its own named test targets". `layer_map` is `{}` and no code
reads it. Naming `integration` on this gate therefore gives the ordinary range-diff selection with a
ceiling of five over it: the cap binds, the selection rule does not.

`row` is the same shape from the other side. Criterion 2 says a `row` run runs "the one currently
accepted task's own deterministic acceptance command". This gate has no notion of a currently
accepted task; it selects by what moved in the pushed range and then refuses if that is more than
one. So the `row` arm here can only refuse — it never narrows to the accepted row, which is the
positive half of the criterion.

None of this is misstated in the commit message, which claims the cap and delivers the cap. It
matters for the matrix: the earlier record's F5 asked that M-657 and M-658 either drop to *todo* or
have their text narrowed to the cap their unit tests hold. Neither happened, this commit does not
change their standing, and a reader arriving after it will find a live caller beside two rows saying
*built* and conclude the rows are held. They are held at the cap and nowhere else.

What would close it: answer the earlier record where it asked — in M-657's and M-658's own status
words or their own text.

`no test · a-mode-name-that-carries-only-its-ceiling (completeness)`

## F7 — A caller in the tree still names no mode, and the message says none does

The commit message says "Every caller of the run now names its mode, which is the point".
`tests/test_guardrail_fixture_proofs.py` has `_run_acceptance_rerun`, which runs the script as a
subprocess inheriting the ambient environment and naming nothing. It is registered in that file's
`PROVEN` map as this check's live fixture proof — the red-and-green pair the pack asks every check
to carry.

Both halves were driven directly rather than reasoned about. On this tree,
`acceptance_rerun_reds_the_bug()` and `acceptance_rerun_passes_the_fix()` both return False. On the
pre-change clone they also both return False, so this commit did not break them — they were already
dead, for their own separate reason, and no test method in that file drives either. The suite stays
green and nothing announces it.

So the sentence is not true as written, and the fixture proof this check owns is nameless as well as
dead. The other roads are clean: `.github/workflows/gates.yml` names the mode, all four
closure-kernel callers now name `release` (counted — four distinct test functions call the changed
helper, which is what the message says), `guardrails/pre-push` does not call the script,
`adopt/install-scaffold.sh` vendors it beside `run_modes.py` rather than without it, and
`adopt/install-status-view.sh` vendors neither, so no installed host gets the script without its
reader.

One doc lags. `skills/build-pipeline/SKILL.md` still describes this gate as one that "takes every
done row carrying an admitted key and runs that key at the pushed commit", which was already stale
about the range and is now stale about the mode too — a host wiring the script into its own CI from
that sentence gets an unconditional exit 1 and no hint why.

What would close it: name the mode in `_run_acceptance_rerun`, then either wire the pair into a test
or delete it; correct the message's sentence; add the mode to the pack's own description of the
gate.

`defect · a-caller-the-claim-does-not-cover (completeness)`

## F8 — The cap's refusal is caught by a clause wide enough to catch anything

`judge` is wrapped in `except ValueError` whose message reads "Name the mode this run actually is,
or narrow what it covers". `admit_targets` raises `ValueError`, and so can the plan parse, the table
load, and `select`, none of which have anything to do with a mode. Any of them now sends the reader
after the wrong thing.

Nothing fails open — the arm returns 1 either way — so this costs a diagnosis rather than a verdict.
It is worth naming because the gate's whole value is that a red is legible: a wrong cause printed
over a real fault is how a real fault gets called a configuration problem.

What would close it: raise a named exception from the cap and catch that.

`no test · a-refusal-that-explains-the-wrong-thing (traceability)`

## F9 — Every other claim in the commit message checks out

Checked one at a time against this tree:

- "`guardrails/run_modes.py` had no caller outside its own test" — true. At 5be3dd27 the name
  appears in a vendor list, two comments and one recorded acceptance key, and in no import.
- "That commit is gone from this branch and its text is not in this one" — true. `names_no_target`
  appears nowhere in the tree outside the earlier record's own prose, and no program name is matched
  anywhere in the new code. The refused approach is genuinely gone rather than reworded.
- "`release` carries none and admits the affected set, `row` admits one target and `integration`
  five" — true of this repo's config, exercised directly. See F1 for what it is on a host.
- "the four closure-kernel tests that drove it namelessly say `release`" — true, four distinct test
  functions.
- "the summary says which mode ran and whether it decided anything" — true; the line printed in the
  live gate-v run above.
- "Ran: 420 passed, 2 skipped over the twelve files touching the changed code" — the set is not
  enumerated, so it could not be reproduced exactly. This pass ran sixteen files chosen the same way
  and saw 373 passed, 2 skipped. Every file in both descriptions is green and nothing behind either
  number is red.
- "Every caller of the run now names its mode" — false; F7.

## F10 — The red-proof holds, and the fourth test says so itself

Red-proved independently. This repo was cloned with `git clone --no-hardlinks` into a scratch
directory and checked out at `e7869159^`; the pushed `tests/test_acceptance_rerun_reach.py` was
copied in over the clone's own, leaving every other file at the pre-change state. Against that tree:

- `test_a_run_that_names_no_mode_is_refused_before_it_selects_anything` — FAILED.
- `test_a_row_run_is_refused_by_its_own_cap_when_more_than_one_row_is_affected` — FAILED.
- `test_a_release_run_decides_the_verdict_and_a_manual_run_decides_none` — FAILED, on the manual
  arm: the pre-change gate returns 1 and prints BLOCKED where the new one reports and returns 0.
- `test_the_gate_judges_no_program_name` — PASSED, which its own docstring states in advance and
  explains: it is a standing guard against a rule that was written into this pack twice, not a proof
  of the change beside it.

That is exactly what the commit message claims. One more test failed there,
`test_a_stopped_command_is_unjudged_and_never_a_failed_verdict`, because `judge` took three
arguments before this commit and the pushed test passes four; that is the changed signature, not a
proof of anything, and it is named here so the count of four failures is not read as four proofs.
Each new test's docstring says what it holds, and each is true — the fourth's is the most useful,
because it is the one that could have been over-read.

## The verdict on the range

The move this commit makes is the right one. The judgement left the admission door, where it was
reading command text and matching program names, and went to the run, where a mode and a composition
are actually known. It judges no command text at all, and the two-name list is gone from the tree
rather than reworded. Gate v runs green on this very range, selecting two rows of eighty-three and
saying why. The reason to refuse is not that the design is wrong.

The reason to refuse is that the binding is thinner than the commit says. The cap it rests on is
seeded absent onto every host the pack installs, and absent means admit — so on a host, `row` runs
forty rows without a word, which is the thing Requirement 322 exists to bound. A release gate that
existed because a typed receipt bought a pass can now be stood down by one word on a workflow step,
and the key that would forbid it is already written in the config and read by nobody. And the two
matrix rows this commit is named for moved to *built* over tests that prove two refusals where the
rows promise an admission — which is the reading error the earlier review refused today, recurring
in the same two rows, in the commit written to answer it.

What a reader of this record should be wary of, in order:

- **On a host the cap binds nothing** (F1). Everything the commit claims about `row` and
  `integration` is true here and false there, and it fails toward admitting.
- **`manual` is a one-word green** (F2), and `in_ci: false` sits in the config with no reader.
- **The rows say more than the tests hold** (F3, F4). Criterion 12 is still held by nothing.
- **One caller still names no mode** (F7), so the message's strongest sentence is the one that is
  wrong.

The whole suite was left to CI. This pass ran the sixteen files that touch the changed code or read
the changed documents, and every command named above; no finding here rests on a suite total.

On the other record on disk. `docs/prover/2026-09-08-the-door-learns-two-program-names.md` is
untracked, and the commit it reviews, 4af78315, is no longer on this branch. It should be committed
as it stands rather than deleted: it is the written reason the program-name approach was dropped,
and this commit's own message leans on it. Because its `Range:` names a commit nobody can now
resolve, whoever commits it should add one line at its head saying the range it covers was dropped
from the branch and what replaced it. This pass left the file byte-for-byte as it found it.

Blocking: three, and all three stand.
- F1 stands: `run_modes.admit_targets` admits whatever it is given when a mode carries no `max_targets`, and `adopt/install-scaffold.sh` seeds `row` and `integration` with no cap at all — proved by running the shipped function against the exact seeded shape, where `row` admitted forty targets with no refusal and no warning. Criterion 2 fixes `row` at one target and criterion 3 fixes `integration` at five from the pack's own `MOST_DELIVERABLES`, so those two figures are the mechanism the pack ships rather than a budget the host keeps. It closes by seeding both figures, or by having `admit_targets` refuse a verdict-deciding mode that names no bound.
- F2 stands: criterion 8's first half — a `manual` run never stands as a CI or release gate — is enforced by nothing, the config's `"in_ci": false` is read by no code in the tree, and no test reads gate v's step, so changing one word in `.github/workflows/gates.yml` makes a release gate print its faults and exit 0. It closes by reading the key the config already carries and pinning the workflow's mode in a test.
- F3 stands: M-661 and M-662 moved to *built* over tests that hold less than the rows promise — M-661's clause "admitted in a `row` run and in an `integration` run" is held by nothing, both its named tests being refusals, and M-662's "anywhere in the mechanism" is held by a two-command sample of one script whose own docstring says it passed before the change. It closes by narrowing both rows to their evidence, or by writing the admission test and the static read the rows describe.
