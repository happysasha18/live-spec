# Prover record — 2026-09-08 the door learns two program names

**The range this record reviews was dropped from the branch.** Its commit `4af78315` put the
mode-and-composition judgement at the admission door and read the command's own text for a bare
test-runner invocation; this record refused it, and the seat took the refusal rather than repairing
the approach — the commit was reset away and the work was rebuilt on the acceptance run instead
(`e7869159` and after). `4af78315` resolves in the tree it was written in and in no clone, so a
reader following it will find nothing. The record stands because it is the written reason a
program-name rule was dropped for the second time, which is the thing most likely to be written a
third time by someone who never saw it.

PUSH-REVIEW

The pass was run by a seat that authored none of this commit, briefed to find reasons to refuse it
and to hold it defective until evidence said otherwise. Every judgement below about what the new
check admits or refuses was taken by running the shipped function and the shipped `admit` command
against planted hosts, never by reading the code and reasoning about it. Where the commit message
states a number, that number was recomputed against this tree.

Range: 5be3dd27..4af78315 — the base the remote holds, then the one commit this push sends.

- 4af78315 The run-mode contract gets its caller, at the door that writes the row —
  `plan_checks_core.names_no_target` added, a block in `scripts/task-admission.py:admit` that reads
  it and consults `guardrails/run_modes.py`, and four tests in `tests/test_task_admission.py` that
  drive the real `admit` command as a subprocess.

Files read: the commit's own diff and message, `scripts/plan_checks_core.py` (`names_no_target`,
`reads_outside_the_tree`, `run_key`, `evaluate`'s icon arm, `key_failure_note`),
`scripts/task-admission.py` (`admit`, `acceptance_key`, the module's imports),
`guardrails/run_modes.py`, `guardrails.config.json` (`run_modes`),
`guardrails/check-acceptance-rerun.py` (`select`'s screening arms), `scripts/render-board.sh`,
`spec/queue-intake-priority.md` Requirement 322 with its Context paragraph and criteria 12, 13
and 14, `matrix/build-pipeline.md` M-657..M-667,
`docs/prover/2026-09-08-four-named-modes-and-the-runner-that-never-arrived.md` F6 and F8 and its
closing section, `tests/test_task_admission.py` (the new section and the fixture host above it),
`tests/test_run_modes.py` (every test name in it), `tests/test_run_modes_install.py`,
`adopt/install-scaffold.sh` and `adopt/install-status-view.sh` (their vendor lists),
`guardrails/check-prover-record.sh`, `docs/prover/README.md`.

Checks run: `python3 -m pytest -q tests/test_task_admission.py tests/test_run_modes.py
tests/test_run_modes_install.py` — 90 passed;
`python3 -m pytest -q` over the fourteen further files that name either changed module
(`tests/test_acceptance_rerun_reach.py`, `tests/test_board_matches_the_canon.py`,
`tests/test_checkpoint_mechanism.py`, `tests/test_closure_kernel_bypasses.py`,
`tests/test_director_route_end_to_end.py`, `tests/test_plan_is_not_executable.py`,
`tests/test_priority_order.py`, `tests/test_probe_reads_state.py`,
`tests/test_statement_validation.py`, `tests/test_status_view_install.py`,
`tests/test_success_measure_view.py`, `tests/test_tasks_parser_finds_every_task.py`,
`tests/test_traceability.py`, `tests/test_work_board.py`) — 406 passed, 2 skipped, 120 seconds;
44 command strings put through `plan_checks_core.names_no_target` directly, chosen to separate a
whole-suite run from a targeted one across wrappers, shell chains, redirections, broad `-k`
expressions, directory arguments, `unittest discover`, and commands that merely mention a path
ending in `pytest`;
13 of those same strings put through the real `admit` command as a subprocess against a planted
host whose `CHECKS` names one row, with `LIVE_SPEC_RUN_MODE` and `LIVE_SPEC_PUSH_FULL` cleared —
the results are F1 and F2;
the same command run under `LIVE_SPEC_RUN_MODE` set to each of `row`, `integration`, `release`,
`manual`, to the empty string and to `bogus`, and under `LIVE_SPEC_PUSH_FULL=1` — the four names
behave as the message says, and an unknown name surfaces as a red status carrying
`unknown run mode`, not as a traceback;
`admit` run in a planted host holding `scripts/task-admission.py`, `scripts/plan_checks_core.py`
and `scripts/checkpoint.py` and no `guardrails/` beside them — refused, exit 2, the message naming
the missing file and the way out, and the row not written;
a red-proof of the four new tests: the working tree's own `scripts/`, `guardrails/` and `tests/`
copied to a scratch directory, the two added blocks removed from the copies by hand, each copy then
diffed against `git show 4af78315^:<path>` and confirmed byte-identical to the pre-fix source while
`tests/test_task_admission.py` stayed byte-identical to the pushed one, then
`python3 -m pytest tests/test_task_admission.py -k "whole_suite or targeted_key_naming"` in that
copy — 2 failed, 2 passed, the result in F4;
`grep` across the tree for every reader of `names_no_target` and `reads_outside_the_tree` — one
caller of the new function, `admit`, and none anywhere else;
`grep` for the test function names `matrix/build-pipeline.md` M-661 and M-662 record — neither
exists in `tests/`;
`git status --short` before and after the red-proof — the tree carries nothing but this record and
the untracked `inbox/` deposit it was told not to touch.

Findings: nine. Two are blocking and both stand. The commit is a real improvement over a tree with
no check at all, and its lean in a host missing `guardrails/` is the right one. It does not hold
what it says it holds: the function at the centre of it starts by matching two program names, and
both halves of the exact defect Requirement 322 was written to end are reproducible against the
shipped code today.

## F1 — Both halves of the defect Requirement 322 exists to end are back, in one function

> "An adversarial review proved the refusal wrong on both sides at once: a command that ran a whole
> suite through `unittest` was admitted, because the word it forbade never appeared, while a
> harmless `grep` for the word `pytest` inside a config file was refused, because the word appeared
> and the check never asked what the command did."
> — spec/queue-intake-priority.md, Requirement 322, Context

That paragraph is the requirement's own statement of what this mechanism must never do. Both of its
examples were re-run against the shipped `admit` command. Admitted, exit 0, row written:

- `python3 -m unittest discover -s tests` — a whole suite through `unittest`, which is the Context's
  first example verbatim. `discover` is filtered out of the trailing tokens, but `-s` is a flag and
  `tests` is not, so a target reads as named.
- `pytest tests/` and `pytest .` — a directory argument is a token, so the whole suite reads as one
  named target.
- `make test`, `npm test`, `tox`, `./scripts/run-all-tests.sh` — a wrapper runs the same suite and
  never matches, because the check never sees the program it wraps.
- `python3 -m pytest -q -k ""` and `python3 -m pytest -q -k 'test or not test'` — a `-k` expression
  that selects everything donates a token.
- `python3 -c 'import pytest,sys; sys.exit(pytest.main([]))'` — a suite run with no matching token
  anywhere.

Refused, exit 2, row not written:

- `grep -rn pytest` — a recursive search of the tree for the word, which is the Context's second
  example. Nothing runs a suite. `pytest` is a bare token with no non-flag token after it, so the
  check calls it a run of everything.
- `which pytest`, `env pytest`, `test -f /usr/local/bin/pytest`, `cat docs/pytest`,
  `ls scripts/pytest` — the token match is on the path's last segment, so any command whose text
  ends in a path named `pytest` is refused as a whole-suite run.

Criterion 13 says a check judging an acceptance command "shall judge its mode and its composition,
and shall never judge the name of the program that runs it". Criterion 14 says the system "shall
keep no registry of forbidden verifier commands". The function's first act, on every token, is
`tok.rsplit("/", 1)[-1] == "pytest"` or `-m` followed by `pytest` or `unittest`. Two program names,
matched by name, deciding whether any further reading happens at all. The composition read — does a
non-flag token follow — is real and is the honest half of the change, but it is downstream of a
name gate, and it is the name gate that decides every case above. A run of everything through a
name not on the list is admitted; a command that runs nothing but carries a name on the list is
refused. That is not the forbidden thing wearing a new coat by resemblance — it is the forbidden
thing with a second test bolted behind it, and the two-name list is doing the work.

The judgement is structural in shape and program-named in fact. A command string cannot say what a
program will run; only the row can say what its check covers.

What would close it: take the target out of the command string. A row's entry in
`scripts/plan_checks.py` names its command and, beside it, the targets that command covers; `admit`
judges those named targets against the mode's composition and never parses the command at all. Then
no program name appears anywhere in the mechanism, `make test` and `pytest` are judged the same
way, and M-662 becomes true rather than aspirational. Short of that, deleting `names_no_target` and
leaving the door as it was at 5be3dd27 is a smaller wrong than shipping a two-name registry under a
comment that says it is not one.

`defect · the-deleted-rule-returns-under-a-new-name (safety)`

## F2 — Any trailing token walks the refusal, including the safer spelling

Put through the real `admit` command, all of these are admitted, exit 0, row written, each of them
a full suite run:

- `python3 -m pytest -q; echo ok`
- `python3 -m pytest -q > /dev/null`
- `python3 -m pytest -q 2>&1`
- `python3 -m pytest -q | tail -1`
- `python3 -m pytest -q -n 4`
- `python3 -m pytest -q --tb short`
- `python3 -m pytest -p no:cacheprovider`
- `pytest -q # tests/test_x.py`
- `python3 -m pytest --deselect tests/test_slow.py`
- `timeout 600 python3 -m pytest -q`

The check reads `command.split()` and asks whether anything that does not begin with `-` follows
the tool. A redirection target, a pipeline's next word, a flag value written with a space, a shell
comment, the argument of `-n` — each is an ordinary part of writing a command, and each satisfies
the check. `python3 -m pytest -q` is refused and `python3 -m pytest -q > /dev/null` is admitted, and
those two run the same thing.

The last line is the sharpest: `timeout 600 python3 -m pytest -q` is admitted while the bare form is
refused. The board renderer runs every recorded key through `run_key` with `timeout=None`, so the
one spelling that would bound the hazard is the one the door lets through, and the naked spelling
that would hang it is the one it stops. The check rewards the more dangerous form.

What would close it: the same repair F1 names. No read of a command's text is closed under shell
decoration, and no patch to this one will make it so — a token filter cannot tell a redirection
from a test path, because at the level it reads they are the same thing.

`defect · a-refusal-one-character-wide (safety)`

## F3 — Three places state the property the code does not have

The commit message: "it reads the run's own mode and its composition, and never the name of the
program that runs it (Requirement 322 criterion 13)". The comment above the new block in
`scripts/task-admission.py`: "never on the name of the program that runs it
(`plan_checks_core.names_no_target` reads the command's shape, not its program)". The function's own
docstring: "Read off the command's own tokens, never off the name of the tool alone (INV-328
criterion 13...)". F1 shows all three untrue. The docstring's parenthetical is the most misleading
of the three, because it cites the criterion it breaks.

This matters past the wording. The next reader who wants to know whether the pack keeps a list of
verifier names has three statements in the tree saying it does not, and one function saying it does.
That reader is the one who will decide whether M-662 can be marked built.

Two further claims in the message were checked. "`guardrails/run_modes.py` had no caller outside its
own test" — true at 5be3dd27, and it now has exactly one. The stated run, "478 passed, 2 skipped" —
this pass ran the seventeen files that name either changed module and saw 496 passed, 2 skipped,
which is one eighteen-test file more than the message counts; the message's set is described loosely
("every other file touching the two modules"), every file in it is green, and nothing behind the
number is red.

What would close it: with F1 repaired, delete all three sentences and write what the mechanism then
does. Without F1 repaired, they are false statements about a safety check and should not ship.

`defect · code-and-its-own-comment-disagree (traceability)`

## F4 — Two of the four new tests pass against the tree without the fix

Red-proved. The working tree's `scripts/`, `guardrails/` and `tests/` were copied to a scratch
directory; the added function and the added `admit` block were removed from the copies by hand; each
copy was then diffed against `git show 4af78315^:<path>` and came back byte-identical to the pre-fix
source, while `tests/test_task_admission.py` in the copy stayed byte-identical to the pushed one.
Against that tree:

- `test_a_whole_suite_key_is_refused_at_the_real_admit_cli_when_no_mode_is_named` — FAILED, the
  admission returned 0 and wrote the row.
- `test_a_whole_suite_key_is_refused_under_row_integration_and_release` — FAILED, same, on `row`.
- `test_a_whole_suite_key_is_admitted_only_as_an_explicit_manual_audit` — PASSED.
- `test_a_targeted_key_naming_pytest_is_admitted_with_no_mode_named` — PASSED.

Two of the four hold the change. The other two assert that something is admitted, on a door that
admitted everything before the change, so they are green on a tree with no check in it at all. They
are worth keeping as guards against a later over-refusal, and neither is evidence for anything this
commit did. The commit message says the four tests drive the real command, which is true; it does
not say what each one holds, and a reader counting four tests will over-read the coverage — the same
reading error F8 of the earlier record names.

What would close it: say in the section comment which two hold the refusal and which two guard
against over-refusal, so the count is not read as four proofs.

`defect · a-test-that-is-green-before-the-fix (completeness)`

## F5 — The caller F8 asked for cannot refuse anything

`run_modes.admit_targets(mode, [key])` is called with a list of exactly one element, always. `row`'s
cap is 1, `integration`'s is 5, `release` and `manual` carry none. The call can never raise. It is a
line that makes `admit_targets` reachable without making it capable of a verdict.

F8 of the earlier record asked for one of two things: move M-657 and M-658 to `*todo*` until a
caller exists, or narrow the rows' text to the cap their tests hold. Neither happened. A caller now
exists in the sense that a name is called; what M-657 promises — a `row` run resolving the one
currently accepted task and running its own command — is still resolved by nothing, and the two rows
still wear `*built*`. Someone reading the matrix after this commit will find a caller and conclude
the rows are held.

What would close it: leave the call out, since it decides nothing, and answer F8 where F8 asked —
in the matrix rows' own status words.

`defect · a-call-that-cannot-fail (completeness)`

## F6 — The matrix rows this commit is named for are untouched

M-661 promises exactly the judgement this commit claims to build, names
`test_an_acceptance_command_naming_pytest_is_judged_by_mode_not_by_its_name` in
`tests/test_run_modes.py`, and stands at `*todo*`. Grepped: that function does not exist anywhere in
`tests/`. The four tests that partly hold the row live under other names in another file, and the
row does not know it. So the commit that answers F6's most load-bearing item leaves the matrix
saying the item is unbuilt and pointing at a test that was never written.

M-662 is the row that would have caught F1: "No registry of forbidden verifier commands is kept
anywhere in the mechanism; never a list of banned words or programs standing in for the
mode-and-composition judgment". It is `*todo*`, and the test it names,
`test_no_registry_of_forbidden_verifier_commands_exists`, does not exist either. The one row whose
job is to stop this change from being written is unbuilt, which is why nothing went red.

What would close it: build M-662 first, as a test that reads the mechanism for program names, and
let it judge whatever replaces `names_no_target`. Then rewrite M-661 against the tests that actually
hold it, in the file they live in.

`defect · the-row-that-would-have-caught-it-is-unbuilt (completeness)`

## F7 — Criterion 12 is still unheld, and the new test does not reach it

Criterion 12: "The system *shall* admit a targeted test run in a `row` run and in an `integration`
run." `test_a_targeted_key_naming_pytest_is_admitted_with_no_mode_named` admits a targeted key with
no mode named — and because `names_no_target` returns False for it, the whole new block is skipped
and `run_modes` is never imported, never resolved, never consulted. The test proves the check does
not fire; it proves nothing about a `row` run or an `integration` run admitting anything, because no
mode is ever asked. Nothing in the range holds criterion 12.

What would close it: a test that names `LIVE_SPEC_RUN_MODE=integration`, admits a targeted key under
it, and asserts the mode was read.

`defect · a-criterion-unheld-by-the-test-that-cites-it (completeness)`

## F8 — The hazard is reachable by a road the door does not stand on

`scripts/plan_checks.py` is a hand-edited table. `admit` screens a key once, at the moment the row is
written. After that, `plan_checks_core.evaluate` runs every row's recorded key through
`run_key(t["check"])` with `timeout=None` on every board render, and `LIVE_SPEC_BOARD_CHECKS`
defaults to on. A key edited into that table after admission — or edited over an admitted one — is
never put through `names_no_target` again by anything. `guardrails/check-acceptance-rerun.py`
screens `reads_outside_the_tree` and the admission digest, and does not read the new function at
all; the digest arm files a rewritten key as a fault, so that gate is safe, and the board render is
not.

The commit claims the door, and the door is what it changed — this is not a claim it broke. It is
the reason F1 and F2 matter more than they would if the door were the only road: the hazard the
earlier record called the most load-bearing of the six is still one hand edit away, and the door was
the cheap half of closing it. The half that actually holds is a bound on `run_key`, which is M-663's
territory and is still `*todo*`.

What would close it: bound `run_key`, so no recorded command can hang a render whatever road it
arrived by.

`defect · a-guard-on-one-road-only (safety)`

## F9 — On a host installed by the status-view road the refusal is unconditional

`adopt/install-scaffold.sh` vendors both `guardrails/run_modes.py` and `scripts/task-admission.py`.
`adopt/install-status-view.sh` vendors `scripts/task-admission.py` and not `run_modes.py`. Proved by
running `admit` in a planted host holding the scripts and no `guardrails/`: the import arm fires, the
key is refused, exit 2, the row is not written, and the message names the missing file.

The lean is right — refusing the key rather than admitting it is the correct direction, and this was
checked rather than assumed. Two smaller things follow. A host installed by that road can never
admit such a key even under `manual`, because the mode is never reached; and the message points at
`guardrails/run_modes.py`, which that installer does not deliver, so its second sentence ("Name the
test by its own name or path instead") is the only usable half. The lazy import itself is clean: it
sits inside the branch, no other reader of `scripts/task-admission.py` pays for it, the `sys.path`
entry is added only on that path and only when absent, and no module name under `guardrails/`
shadows a standard-library name that a later import in the same process could pick up.

What would close it: say in the message that a host installed through the status-view road names
the target instead, and stop pointing at a file that road does not carry.

`no test · the-message-names-a-file-this-road-never-vendors (completeness)`

## The verdict on the range

This range set out to give the run-mode contract its first caller, and the caller it wrote is a
two-name list of verifier programs with a shape test behind it. Requirement 322 exists because that
exact mechanism was tried, failed on both sides at once, and was deleted. Its Context paragraph
names two examples of the failure. Both were re-run this afternoon against the shipped code, and
both reproduce: `python3 -m unittest discover -s tests` is admitted, `grep -rn pytest` is refused.
The door refuses one spelling of a whole-suite run and admits ten others, including the one that
carries a timeout.

The range is not safe to push as it stands. Nothing in it is broken that was working — the tree at
5be3dd27 had no check here at all, and a session writing an ordinary bare `pytest -q` key will now
be stopped, which is a real gain. The reason to refuse is not that the check is weak. It is that the
check is the thing the requirement forbids, that three sentences in the tree say it is not, and that
the row which would have caught it is one of the six carrying no test. Shipping it writes into the
pack a worked example of a program-name registry, sitting under a comment citing the criterion that
bans one, and the next person to build M-662 will find the pack contradicting itself and will have
to choose which half to believe.

What a reader of this record should be wary of, in order:

- **The judgement turns on two program names.** Everything the check gets right and everything it
  gets wrong follows from `pytest` and `unittest` being on a list and `make`, `npm`, `tox` and a
  wrapper script not being (F1).
- **A trailing token is a full walk-around** (F2). No further patching of a text read fixes this;
  the target has to leave the command string.
- **Half the new tests are green without the change** (F4), and the matrix rows this commit answers
  still say the work is not done and name tests that do not exist (F5, F6).
- **The board still runs every recorded key unbounded** (F8). The door was the cheap half.

And the lesson the range teaches about itself: a check written to satisfy a criterion, with the
criterion's own number in its docstring, is the check least likely to be tested against the
criterion. The citation did the reassuring, and nothing ran the requirement's own two examples until
this pass did.

The whole suite was left to CI. This pass ran the seventeen files that name either changed module
and every command named above; no finding here rests on a suite total.

Blocking: two, and both stand.
- F1 stands: the new check gates on the program names `pytest` and `unittest`, which Requirement 322 criterion 13 forbids and criterion 14 names as a registry, and both examples in the requirement's own Context paragraph reproduce against the shipped code — a whole suite through `unittest discover` is admitted, a `grep` for the word is refused. Closing it means naming a row's targets beside its command and judging those, so no program name appears in the mechanism; deleting `names_no_target` and leaving the door as it was is the smaller alternative.
- F2 stands: any non-flag token after the tool — a redirection, a pipeline, a spaced flag value, a shell comment, or the `timeout 600` that would bound the hazard — walks the refusal, proved against the real `admit` command on ten spellings that all run the whole suite. It closes with F1's repair and with nothing short of it.
