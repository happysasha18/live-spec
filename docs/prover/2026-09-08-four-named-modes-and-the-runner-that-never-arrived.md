# Prover record — 2026-09-08 four named modes and the runner that never arrived

PUSH-REVIEW

Prover skill version: product-prover 1.6.2, installed under `skills/product-prover/`, read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 and `skills/live-spec-base/SKILL.md` v6.1.0. The pass
was run by a seat that authored none of this commit, briefed to find reasons to refuse it and to
hold it defective until evidence said otherwise. Where the commit message states a number, that
number was recomputed against this tree rather than read. Extended 2026-09-08 over `ba34202e`,
the commit that repairs three of this record's four blocking items; each repair was re-derived
against the tree rather than accepted from its own message. Extended again over `6db4ca8a`, which
repairs F11 and the summary residual F2 named.

Range: ed35c92e..6db4ca8a — the base the remote holds, then the three commits this push sends.

- 6db4ca8a The matrix says what the law says, and no summary covers an unjudged row — `M-667`
  rewritten to the amended criterion 15, and `main`'s closing line in
  `guardrails/check-acceptance-rerun.py` split so the blanket pass sentence cannot print over an
  unjudged row. Judged in F11's closure and in F2's, and it raises F12.

- ba34202e Three repairs the pre-push review asked for, and a correction to 5ca8697c — Requirement
  322 criterion 15 rewritten; the emergency stop reported UNJUDGED in
  `guardrails/check-acceptance-rerun.py`; the probe names an unreadable reader and
  `adopt/install-status-view.sh` vendors `scripts/task-admission.py` and `scripts/checkpoint.py`;
  three test fixtures plant their own open row. Judged in the closures below.

- 5ca8697c Test runs go by a named mode and a fixed set of checks — `run_modes` and
  `guardrails/run_modes.py`; the session-start probe stops executing acceptance commands;
  `guardrails/check-acceptance-rerun.py` narrows to the rows the range touched; the `pytest`
  substring refusal leaves the door, Requirement 321, the matrix and the probe-cost test;
  `adopt/install-scaffold.sh` vendors the contract into a host; Requirement 322 under INV-328
  with matrix rows M-657..M-667.

Files read: `guardrails.config.json` (`run_modes`), `guardrails/run_modes.py`,
`guardrails/check-acceptance-rerun.py` (`select`, `judge`, `run_one`, `main`),
`scripts/state-probe.sh` and its twin `scaffold/status-view/state-probe.sh`,
`scripts/plan_checks_core.py` (`run_key`, `reads_outside_the_tree`, `evaluate`'s icon arm),
`scripts/task-admission.py` (`admit`), `adopt/install-scaffold.sh`, `adopt/install-status-view.sh`,
`scripts/render-board.sh`, `.github/workflows/gates.yml`, `spec/queue-intake-priority.md`
Requirement 322, `matrix/build-pipeline.md` M-657..M-667, `architecture/pipeline-and-lanes.md`,
`PRODUCT_SPEC.index.md`, `TEST_MATRIX.index.md`, `tests/test_run_modes.py`,
`tests/test_run_modes_install.py`, `tests/test_plan_is_not_executable.py`,
`tests/test_status_view_install.py`, `tests/test_acceptance_rerun_reach.py`,
`guardrails/check-prover-record.sh`, `docs/prover/README.md`, and both commits' own diffs. For
`ba34202e`: `guardrails/check-acceptance-rerun.py` (`run_one`, `judge`'s completion arm, `main`'s
summary), `scripts/state-probe.sh`, `adopt/install-status-view.sh`, `spec/queue-intake-priority.md`
criterion 15, `matrix/build-pipeline.md` M-667, `tests/test_acceptance_rerun_reach.py`,
`tests/test_probe_reads_state.py`, `tests/test_tasks_parser_finds_every_task.py`,
`tests/test_board_matches_the_canon.py`.

Checks run: `python3 -m pytest -q tests/test_run_modes.py tests/test_run_modes_install.py
tests/test_probe_reads_state.py tests/test_acceptance_rerun_reach.py
tests/test_plan_is_not_executable.py tests/test_task_admission.py` — 115 passed, the six files this
commit adds or rewrites;
`python3 guardrails/check-acceptance-rerun.py` on this clean tree — 15 of 83 selected, BLOCKED on
`plan-11` (locally only: `board.html` is gitignored and CI draws it first);
`bash scripts/state-probe.sh` — 78 done rows reported as needing a fresh check;
`bash scripts/state-probe.sh` in a planted host carrying the vendored probe, `PLAN.md`,
`plan_checks.py`, `plan_checks_core.py` and the checkpoints, run three times — with neither
`scripts/task-admission.py` nor `scripts/checkpoint.py`, with the first alone, and with both;
`importlib` load of `scripts/task-admission.py` in that host — `ModuleNotFoundError: No module
named 'checkpoint'`; `admission.admit` against a planted host whose `CHECKS` holds
`python3 -m pytest -q` — admitted; a set comparison of `run_modes.release.core` against every
gate letter in `.github/workflows/gates.yml`; `git grep -l PreToolUse` over `adopt/` at ed35c92e
and at 5ca8697c; `grep` for each of the six test function names the *todo* matrix rows name.
Over `ba34202e`: `run_one(".", "sleep 5")` with `EMERGENCY_STOP_SECONDS` set to 1 — returns
`(None, "the check hit the emergency stop before finishing (1s)", True)`, so the stopped arm carries
no code a caller could read as a failure; a second planted host built by running
`adopt/install-status-view.sh` itself — 8 files vendored, `scripts/task-admission.py` and
`scripts/checkpoint.py` among them, and the probe prints "78 done row(s) need a fresh check";
the same host with `scripts/checkpoint.py` deleted by hand — the probe prints "the recorded-state
read did not run — scripts/task-admission.py did not load: No module named 'checkpoint'; re-run
adopt/install-status-view.sh ...";
`python3 -m pytest -q tests/test_acceptance_rerun_reach.py tests/test_probe_reads_state.py
tests/test_tasks_parser_finds_every_task.py tests/test_board_matches_the_canon.py
tests/test_status_view_install.py` — 39 passed, the five files `ba34202e` touches. Over
`6db4ca8a`: `python3 -m pytest -q tests/test_acceptance_rerun_reach.py` — 8 passed; and
`python3 guardrails/check-acceptance-rerun.py` on this tree at `6db4ca8a` — 15 of 83 selected, all
15 ran and passed, 13 of them named as predating the acceptance anchor (this machine carries a
drawn `board.html`, which `plan-11`'s command reads; CI draws it before gate v).

Findings: twelve. Four were blocking at 5ca8697c and all four are closed by `ba34202e`; F11, raised
by that repair, is closed by `6db4ca8a`; F12 is raised by `6db4ca8a` and does not block. The mechanism this commit names is a contract with no
runner: `resolve_mode`, `admit_targets` and `decides_verdict` have no caller outside their own
test file, so the four modes are declarations and the composition law they state is enforced
nowhere. Two executions did change, and both changed honestly; the cost is that the one thing
which had been re-establishing 78 unbacked done marks — gate v running every done row at every
push — is narrowed in the same commit that first counts them. The install step contradicts the
requirement it ships. A timeout decides a verdict.

## F1 — Installing the pack now writes a tool hook into the host's own settings, which this same commit's law forbids

> "The system *shall* add no new hook, listener, daemon, or global session hook to run or to watch
> a check." — spec/queue-intake-priority.md, Requirement 322 criterion 15

`adopt/install-scaffold.sh` gained a block that opens `$HOST_ROOT/.claude/settings.json` and
appends a `PreToolUse` entry matching `Task|Agent`, pointing at
`guardrails/worker-admission-guard.py`. At ed35c92e no file under `adopt/` mentioned `PreToolUse`;
at 5ca8697c `adopt/install-scaffold.sh` does. So a person adopting live-spec gets an agent
configuration change they did not ask for, in a file that is normally committed, and every
teammate on that repository inherits a guard that can deny their `Task` calls. The commit message
answers a narrower question than the law asks — "No global hook, nothing under the user's home" —
and the matrix row that would have caught the gap, M-667, is one of the six carrying no test.

Take the wiring out of the installer and print the two-line JSON block for the host to paste,
which is what the same script already does for every other host decision it refuses to make.
Failing that, put it behind an explicit flag and default it off. If the intent is that criterion 15
means "no *global* hook", amend the criterion to say so and build M-667 against the amended text —
but the criterion as written is the one shipped in this commit.

**Closed in `ba34202e`.** Criterion 15 now reads: no new global session hook, no new listener, no
new daemon, and the repo-local spawn guard delivered only by wiring it into the host's own
repository-local settings, writing nothing under the user's home. That is what
`adopt/install-scaffold.sh` does — it writes `$HOST_ROOT/.claude/settings.json` with
`$CLAUDE_PROJECT_DIR/guardrails/worker-admission-guard.py` and touches nothing under `$HOME`. The
criterion and the code now say the same thing.

I read this as the correct repair rather than a widening base rule 39 forbids, and the reason is
narrow: criterion 15 and the install step shipped in the same commit, so the criterion was a
mis-statement of intent from birth rather than a standing law the work then broke. The amended text
also names the permitted thing exactly once and by name — "the repo-local spawn guard the pack
already carries" — so it licenses one guard rather than a class of hooks. The guarantee that leaves
is that nothing now stops a second repo-local hook arriving through the same door; naming it that
tightly is what keeps that cheap to catch. What the repair did not carry with it is F11.

`defect · law-contradicted-by-its-own-delivery (safety) — closed`

## F2 — A runtime timeout decides a verdict, in the file that says it does not

> "*when* a runtime timeout stops a spent process, the system *shall* have that timeout take no
> part in the verdict" — Requirement 322 criterion 11; and `"timeout_is_never_a_verdict": true` in
> all four modes of `guardrails.config.json`

In `guardrails/check-acceptance-rerun.py`, `run_one` catches `subprocess.TimeoutExpired` and
returns `1, "the check hit the emergency stop before finishing (300s)"`. `judge` treats any
non-zero code as a fault. `main` prints `BLOCKED` and returns 1. A selected row whose check runs
long on a loaded runner therefore refuses the push, and the same commit checked on a quiet machine
passes — which also breaks criterion 9, that a verdict depend only on the commit and the check.
Renaming `PER_KEY_SECONDS` to `EMERGENCY_STOP_SECONDS` changed the word while the wiring stayed.

The only test touching this is `test_every_mode_ships_emergency_timeout_seconds_as_null`, which
asserts that the config carries `timeout_is_never_a_verdict: true`. A declaration checking its own
text passes whatever the code does.

Make `run_one` return a third outcome. Report a timed-out row under its own heading — "did not
finish, so it returned no verdict" — and leave `faults` untouched, so the gate's exit code is
decided by checks that finished. Then test it: plant a key that sleeps, set
`EMERGENCY_STOP_SECONDS` to 1, and assert the gate exits 0 and names the row as unfinished.

**Closed in `ba34202e`.** `run_one` now returns `(code, first, stopped)`; a `TimeoutExpired`
returns `(None, ..., True)`, and `judge` files that row under `unjudged` and `continue`s before
`ran.append`, so it can reach neither `ran` nor `faults`. `main` prints the unjudged rows by name
and its exit code still reads `faults` alone. Re-derived rather than read: `run_one(".", "sleep 5")`
with `EMERGENCY_STOP_SECONDS` monkeypatched to 1 returns `(None, "the check hit the emergency stop
before finishing (1s)", True)`, and `code` is `None` precisely so no caller can read it as a
verdict. `test_a_stopped_command_is_unjudged_and_never_a_failed_verdict` holds it.

No other road left for a stopped command to redden the gate: the only other fault source in that
loop is a genuine exception out of `future.result()`, which is an error rather than a stop; the
probe runs no commands at all; and `scripts/render-board.sh` passes `timeout=None`, so it has no
stop to convert. Two residuals, neither blocking. A row stopped by the limit is now proven by
nothing at push time and leaves only a printed line — which is what criterion 11 demands, and it
means a permanently slow obligation can go unchecked indefinitely. And `main` still prints "every
selected row's acceptance passes here." after listing unjudged rows, which overstates by exactly
the rows it just named. **That second residual is closed in `6db4ca8a`**: `main` now branches, and
with unjudged rows present it prints how many returned a verdict and that the rest "were decided by
nothing", keeping the old wording only when there are none.
`test_the_summary_never_claims_a_pass_over_an_unjudged_row` asserts the blanket sentence is absent
from a run carrying an unjudged row, so restoring that sentence reds the test rather than passing
vacuously. The first residual stands: a row the limit stops is still proven by nothing at push time,
which is what criterion 11 asks for. The unanchored half of the same overstatement is F12.

`defect · clock-in-a-verdict (safety) — closed`

## F3 — In a host, the probe's whole recheck arm fails silently, and the pack fixed that class for its own tree only

> "A module that will not load names no anchor rather than stopping the probe over an optional
> cross-check." — scripts/state-probe.sh

The probe loads `scripts/task-admission.py` through `importlib` and, on any exception, sets
`task_admission = None`. Every arm that decides whether a done row's recorded state still stands
sits behind `if task_admission is not None`, so the failure prints nothing at all — no line, no
warning, indistinguishable from a tree where all 83 done marks hold.

Proved in a planted host carrying the vendored probe, `PLAN.md`, both plan readers and the real
checkpoints. With neither `scripts/task-admission.py` nor `scripts/checkpoint.py`: no recheck line.
With `task-admission.py` alone: still no recheck line, because it imports `checkpoint`
(`ModuleNotFoundError: No module named 'checkpoint'`). With both: "78 done row(s) need a fresh
check". `adopt/install-status-view.sh` is the installer that vendors the probe, and it vendors
neither of those two files — so the silent state is the shipped state for every status-view host.

`tests/test_probe_reads_state.py`, the file that red-proves M-664, copies both files into every
planted tree it builds, so its five tests always run with the module present and the silent path is
never exercised.

The pack saw this. `tests/test_plan_is_not_executable.py` adds both files to `NEEDED` with a
comment naming the exact failure — "silently, and its recheck line never fires" — which pins it for
this repository's own fixture and leaves every host fail-open. The same file already holds the
correct shape twenty lines away: a missing `scripts/check-success-measure-feed.py` prints "a feed
exists but ... is missing — re-run adopt/install-status-view.sh to vendor it".

Do the same here: on a failed load, print one warning naming the missing reader and the installer
that supplies it, and add `scripts/task-admission.py` and `scripts/checkpoint.py` to
`adopt/install-status-view.sh`'s vendor list.

**Closed in `ba34202e`, both halves, re-proved in a second planted host.** The host was built by
running `adopt/install-status-view.sh` itself rather than by copying files: it vendors 8 files,
`scripts/task-admission.py` and `scripts/checkpoint.py` among them, and the probe there prints "78
done row(s) need a fresh check" — the arm works in a host now. Deleting `scripts/checkpoint.py` by
hand from that same host makes the probe print "the recorded-state read did not run —
scripts/task-admission.py did not load: No module named 'checkpoint'; re-run
adopt/install-status-view.sh to vendor scripts/task-admission.py and scripts/checkpoint.py beside
it", in the same voice the feed checker already used. The `else` arm covers the missing-file case
as well as the failed-import one, so both silences are named.
`test_the_probe_names_what_it_could_not_read_instead_of_falling_silent` holds it.

`defect · fail-open-in-the-shipped-configuration (safety) — closed`

## F4 — The commit's claim about the re-run's reach is wrong by fifteen rows

> "On this tree it selects 0 of 82 where it used to run all 82." — the commit message of 5ca8697

`python3 guardrails/check-acceptance-rerun.py`, on a clean tree at 5ca8697c with `origin/main` at
ed35c92e, prints: "83 row(s) in the plan, 83 marked done, 15 selected here". Fourteen come through
`files_named_moved`, which is a literal substring test — every acceptance command whose text names
`scripts/task-admission.py`, `spec/queue-intake-priority.md`, `matrix/build-pipeline.md` or any
other path this commit touched is pulled in. The fifteenth is `q-826` itself, correctly selected as
"its Done-when text or DOD hash moved in the pushed range". The gate then exits BLOCKED on
`plan-11`, whose check reads `board.html`; that one is local only, since CI draws the board before
gate v.

So the selection is not broken — the Done-when arm demonstrably works, and it is the arm a reader
would most doubt. What is broken is the sentence about it. A number in a commit message that a
reader will cite as the cost of the change should be the number the tree produces.

Recompute and restate it. If the intended figure was measured with `LIVE_SPEC_DIFF_BASE` set to
`HEAD`, say which base it was taken against.

**Closed in `ba34202e`.** Its message carries the correction by name — "it said the push-time
re-run selects 0 of 82 rows on this tree ... it selects 15 of 83, q-826 among them by the
moved-Done-when arm. The selection is sound; the sentence was not." A wrong figure in a landed
message is corrected by the next message in the same push, which is the repair available.

`defect · measured-claim-contradicted-by-the-tree (traceability) — closed`

## F5 — Requirement 322 criterion 18 promises a reach the gate refuses to have

> "The system *shall* have the push-time re-run cover the release core and the rows whose own
> definition of done, acceptance command, or named files moved" — Requirement 322 criterion 18

`select()` in `guardrails/check-acceptance-rerun.py` states the opposite in its own docstring: "No
release-core list is read here ... that would be a gate asking whether it is a gate." The reasoning
is sound — `release.core` is a list of gate letters, and this script is one of them — but the
criterion was written as though the core were a set of rows, and it shipped in the same commit as
the code that refuses to read it. M-665 is marked *built* against
`test_the_summary_line_names_the_count_selected_and_the_reason_for_each`, which covers the second
half of the criterion only.

Rewrite criterion 18 to say what the mechanism does: the push-time re-run covers the rows whose own
definition of done, acceptance command or named files moved in the pushed range, and it is itself
one entry in the release core.

`defect · spec-and-code-disagree-in-one-commit (traceability)`

## F6 — Six matrix rows carry no test, and each names a test function that does not exist

Every one of the six names was grepped across `tests/`; all six return nothing. What each row
promises, and what a reader of the spec would wrongly take from it:

- **M-660, `manual`.** Promises that a person starts the run, that its purpose and its limit are
  recorded before it starts, that it never stands as a CI or release gate, and that it decides no
  verdict. Nothing starts a manual run; `records_before_start: ["purpose", "limit"]` is two strings
  no code reads; `in_ci: false` is read by nothing. A reader believes a manual mode exists and is
  fenced. Only "decides no verdict" is held, and by a differently-named test that reads the config
  field back. Declaring a mode nothing runs is a wish. A law here would be the runner that
  refuses to start without a purpose and a limit on the record.
- **M-661, mode-and-composition over program name.** Promises the judgement that replaced the
  deleted substring refusal. Nothing judges composition anywhere. Proved: `admission.admit` against
  a planted host whose `CHECKS` is `{'q-1': 'python3 -m pytest -q'}` — the whole suite as one row's
  acceptance — is admitted, and the row is written. `run_modes.admit_targets` is the cap that would
  have refused it and has no caller. A reader believes the refusal moved to a better place. It was
  removed, and the door now holds only "an acceptance command exists" and "it does not name
  `$HOME`". The hazard the deleted rule existed to stop also changed reader rather than ending:
  `scripts/render-board.sh` still runs every row's command by default (`LIVE_SPEC_BOARD_CHECKS=on`)
  through `run_key(t["check"])` with `timeout=None`, so an admitted whole-suite key hangs the board
  render with no emergency stop at all — and CI draws the board immediately before gate v. This is
  the most load-bearing of the six.
- **M-662, no registry of forbidden verifier commands.** Promises no list of banned words or
  programs. True for verifier names now. `plan_checks_core.reads_outside_the_tree` still matches
  `$HOME` and `~/` textually; that is a two-item list about a command's reach rather than about
  which program runs it, and the row should say so, or the next reader will read M-662 as
  forbidding it and delete a working check.
- **M-663, the process group.** Promises the run waits on the pid or group it started and ends only
  the group it owns. `plan_checks_core.run_key` calls `subprocess.run("set -o pipefail; " + command,
  shell=True, executable="/bin/bash", timeout=...)` with no `start_new_session` and no process
  group. On timeout Python kills the `/bin/bash` child alone; every grandchild is orphaned. With
  M-661 unbuilt, that grandchild can now be a whole pytest run left alive on the runner.
- **M-666, receipt binding on an installed host.** Promises a receipt stays bound to the commit it
  was taken at and to the done frozen at admission, on a host that installed through `adopt/`. F3
  shows the host-side reader that would check exactly this does not load in such a host.
- **M-667, no new hook on install.** F1.

Build M-661 and M-663 before the next push that touches this area; they are the two whose absence
is already load-bearing. For the other four, either build them or move the row's status word to
match what is held — a `*built*` mark is the only thing distinguishing a promise from a plan. These
four wear `*todo*` honestly; M-657, M-658 and M-659 wear `*built*` over partial tests (F8, F7).

`defect · unheld-criteria-read-as-shipped (completeness)`

## F7 — The release core is 23 letters copied out of CI with nothing keeping the two in step

> `"core_version_source": "VERSION at the time this list was taken from .github/workflows/gates.yml"`
> — guardrails.config.json

Checked: the 23 letters in `run_modes.release.core` and the 23 gate letters in
`.github/workflows/gates.yml` are the same set, symmetric difference empty, and `core_version`
"6.1.0" equals `VERSION`. So the list is right today. Nothing holds it there.
`test_release_core_list_is_non_empty_and_never_grows_with_named_things` asserts `len(core) > 0` and
that four words appear in `never_grows_with`. A gate added to CI, a gate dropped, a letter renamed,
or a VERSION bump all leave this file green — and the failure is silent in the direction that
matters, since a release core that has quietly stopped naming a gate still reads as a fixed
versioned list.

One assert closes it: parse the gate letters out of `gates.yml` and compare the sets, with the
failure message naming which side has the extra. Add the `core_version == VERSION` assert beside
it. Then M-659 holds the row it is marked `*built*` for.

`defect · snapshot-with-no-keeper (traceability)`

## F8 — Two rows marked built are held by a cap test that covers a third of what they say

M-657 says a `row` run runs "the one currently accepted task's own deterministic acceptance
command, judged only by that task's own named checks, against at most one target". The test it
names, `test_row_admits_one_target_and_refuses_two_naming_the_cap`, proves the last clause. Nothing
resolves "the currently accepted task", and no caller asks.

M-658 says an `integration` run "selects only the layers an explicit map names as touched". Its
`layer_map` is `{}`, no code reads it, and `test_integration_refuses_a_sixth_named_target` proves
the cap alone. Integration mode does nothing today: with an empty map no layer is ever named, so
the mode would select zero targets even if something called it, and nothing calls it. The empty map
is defensible as "never filled with an invented figure" — the gap is the `*built*` mark over it.

Either move M-657 and M-658 to `*todo*` until a caller exists, or narrow the rows' text to the cap
their tests hold and open new rows for the selection halves. The architecture pin
`guardrails/run_modes.py:1` in `architecture/pipeline-and-lanes.md` names a node that no runtime
flow reaches, which is the same gap seen from the architecture side.

`defect · built-mark-over-a-partial-test (completeness)`

## F9 — The probe can no longer print the reopened mark, and nothing says so

`plan_checks_core.evaluate` sets `t["failing_key"]` from a command result and only then reaches
the reopened icon; its own comment says "evaluate() below is its only source". The probe now sets
`t["check"] = None` for every row, so `failing_key` is never true and the reopened mark is
unreachable from the probe. `tests/test_plan_is_not_executable.py` records the change honestly in
its rewritten assertions — a done row whose command fails is now "0 open" rather than reopened —
and the board, which still runs checks, can still draw it.

What goes unsaid is where that mark was being read. Base rule 38 fixes the order of the list a
person reads at the top of every reply and names one of its groups "the ones that came back because
their check stopped passing". That list is built from the probe. The board is a separate reader a
person opens on request. So a group the rule names can no longer appear on the surface the rule is
about.

One comment already misstates the tree because of this: `scripts/render-board.sh` line 464 says
"the probe on the owner's own machine keeps the live verdict, which is where a reopened row is a
fact rather than a guess". The probe keeps no live verdict from this commit on.

Say it in the requirement: name the board as the one reader that can produce the reopened mark, and
state what the session-start read prints in its place. Repair that comment in the same pass. If a
reopened row must still reach the reply, the recheck line is where it goes — which is F10.

`defect · unwritten-seam (completeness)`

## F10 — The 78 is honest; its pointer is false and nothing reads the count

The count is real and this review reproduced it: `bash scripts/state-probe.sh` prints "78 done
row(s) need a fresh check — recorded state alone does not stand for them". That is the change's
best act. Naming a pack's own 78 unbacked done marks out loud is the opposite of covering them
over, and the rows fail on the first arm — no checkpoint, or no passed receipt — rather than on
anything subtle.

Two things weaken it.

The line ends "full list on the board (bash scripts/render-board.sh / board.html)". The board
computes no such set. `scripts/render-board.sh` never calls `read_receipt`, `read_dod_anchor` or
`read_accept_anchor`; its only `recheck` string is about whether the board itself re-runs
acceptance commands. A reader who follows the pointer finds 83 rows drawn as the plan records
them and no list of the 78. The probe deliberately stopped printing the ids to spare a person the
weight, and sent them to a page that does not carry them.

And nothing acts on the count. No gate reads it. The rows keep their done mark. Until this commit,
gate v re-ran all 82 done rows at every push in a fresh CI checkout, which is precisely what had been
making those marks true from the outside; this commit narrows gate v to the rows the range touched.
So the 78 rows whose recorded state does not stand are, from this commit on, re-established by
nothing at all. The narrowing is the owner's own word and this review does not argue it. The gap is
that the change reports the debt and removes the only thing that had been paying it, in one commit,
and says only the first half.

Either draw the set on the board, so the pointer is true, or print the ids behind one named command
(`bash scripts/state-probe.sh --stale`) and point at that. Then decide what reads the count: the
honest answer is that a done row failing the recorded-state read is a row whose mark stands on
nothing, and the pack already has a word for that state.

`defect · false-pointer-and-an-unread-number (traceability)`

## F11 — The matrix row now forbids what the amended criterion permits

> "Installing the mechanism through `adopt/` adds no new hook, listener, daemon or global session
> hook; never an install step that wires a watcher the host did not have before" —
> matrix/build-pipeline.md, M-667

`ba34202e` rewrote criterion 15 and left M-667 standing in its old words. `matrix/build-pipeline.md`
is untouched by that commit. So the spec now permits the repo-local spawn guard by name while the
matrix row that exists to hold criterion 15 still forbids "an install step that wires a watcher the
host did not have before" — which is exactly what `adopt/install-scaffold.sh` does. Nothing catches
the disagreement, because M-667 is one of the six rows carrying no test (F6): the row named
`test_installing_run_modes_adds_no_new_hook_listener_daemon_or_global_session_hook` does not exist,
so whoever writes it next will write it against whichever of the two texts they happen to open.

Rewrite M-667 in criterion 15's amended words — no new global session hook, listener or daemon, and
the repo-local spawn guard delivered only into the host's own repository-local settings with
nothing under the user's home — before anyone builds the test. A test written against the stale row
would red the shipped installer.

**Closed in `6db4ca8a`.** M-667 now reads in criterion 15's own terms: no new global session hook,
listener or daemon to run or watch a check, the repo-local spawn guard delivered only into the
host's own repository-local settings, "never a hook, listener or daemon reaching wider than that one
named guard, and never a file written under the user's home". Read against criterion 15 clause by
clause the two agree, and the row's two `never` clauses add the negative half the criterion states
positively without contradicting it.

Still writable as a test, and more writable than the row it replaces: run the installer into a
temporary host with `HOME` pointed at an empty temp directory, then assert the only `PreToolUse`
entry added names `worker-admission-guard.py`, that `settings.json` gained nothing else, and that
the temp `HOME` is still empty. The old row could not be written at all without redding the shipped
installer.

`defect · spec-and-matrix-disagree-after-a-repair (traceability) — closed`

## F12 — The same overstatement the summary just lost for unjudged rows still stands for unanchored ones

> "13 of them predate the acceptance anchor, so what ran is the command the tree records now" then
> "every selected row's acceptance passes here." — `guardrails/check-acceptance-rerun.py`, both
> lines printed by the run recorded above

`6db4ca8a` split the closing line so the blanket pass sentence cannot print over a row the emergency
stop left undecided. The sibling case is untouched. On this tree the gate selects 15 rows, 13 of
them carry no `ACCEPT:` anchor, and for those 13 the command that ran is whatever the tree records
today — nobody can say it is the command the row was closed against. Requirement 322 criterion 19
is the promise at stake: a receipt stays bound to the done frozen at admission. The gate's own line
names the fact and stops there; the sentence after it then reads over all 15 without qualification,
so a reader counts 15 obligations re-established where 2 were.

This is the class the repair answered pointwise. One summary line overstating what its run proved
was repaired for one of its two cases. Give the unanchored rows the same treatment: say "2 selected
row(s) passed against the command they were admitted with; 13 passed against the command the tree
records today, which is no check of the contract they were closed against." The count is already in
hand — `unanchored` is a list at that point in `main`.

`recommendation · summary-reads-stronger-than-its-run (traceability)`

## What ba34202e adds beside the repairs

Three test fixtures — `tests/test_tasks_parser_finds_every_task.py`,
`tests/test_board_matches_the_canon.py` and `tests/test_probe_reads_state.py` — plant a synthetic
open row rather than resting on the live `PLAN.md` carrying one. That is the right direction: the
anti-vacuous guard was reading the project's own state, so closing q-826 reddened three sound
readers. The repair makes the guard independent of how close the real plan is to done.

One nit, no blocking weight: the 14-line guard block, its comment and `_add_open_guard_row` are
copied verbatim into more than one test file. Base rule 4 wants one home per fact; put
`_add_open_guard_row` in the shared test helper the next time one of the three is edited.

## What this commit closes

Two findings carried in `docs/prover/2026-09-07-the-door-reads-the-record-and-where-that-read-goes-soft.md`
and repeated as blocking in `docs/prover/2026-09-08-the-time-oracle-changes-what-it-proves.md` are
closed here, and both were verified gone rather than assumed. The substring match on a runner's
name is deleted from `scripts/task-admission.py`, from `tests/test_plan_is_not_executable.py`, from
Requirement 321 and from the matrix. The letter-suffixed criterion `6a.`, invisible to
`specformat.py` and to the generated index, is deleted with it, and `PRODUCT_SPEC.index.md` now maps
INV-327 to R321.1 through R321.8 with the hole gone. Deleting the rule rather than widening it is
the repair base rule 39 asks for.

## Spec and architecture re-check

`PRODUCT_SPEC.md` is unchanged in this range. The delta lands in `spec/queue-intake-priority.md`,
which the freshness arm reads as part of the same document: Requirement 321 loses criterion 6a and
Requirement 322 arrives under INV-328 with twenty criteria, indexed in `PRODUCT_SPEC.index.md`.
`ba34202e` edits one criterion of that same requirement, criterion 15, leaving the criterion count
and so `PRODUCT_SPEC.index.md` untouched, and moves no other spec text. `6db4ca8a` touches no spec
file at all; it edits one matrix row, one summary branch and one test.
`ARCHITECTURE.md` is unchanged; `architecture/pipeline-and-lanes.md` gains the INV-328 line and the
`guardrails/run_modes.py:1` pin — a pin to a module with no caller, noted in F8. Against base rule
43 the composition figures hold: `max_targets` 1 and 5 are counts of targets, the 5 traced to
`MOST_DELIVERABLES`, the release core is a named list of gates, `never_grows_with` names the four
things a budget must not scale on, and every mode ships `emergency_timeout_seconds: null`. No number
in the config is read off a clock. The one clock that does reach a verdict is
`EMERGENCY_STOP_SECONDS` in the gate, F2.

Blocking: four were raised against 5ca8697 and all four are closed by ba34202e, each re-derived here rather than accepted from that commit's message; F11 and F2's summary residual are closed by 6db4ca8a, and nothing in this range is left blocking.
- F1 closed: Requirement 322 criterion 15 now bans a new global session hook, listener or daemon and permits the repo-local spawn guard wired into the host's own repository-local settings, which is what `adopt/install-scaffold.sh` does — it writes `$HOST_ROOT/.claude/settings.json` and nothing under `$HOME`. The criterion, the code and — since 6db4ca8a — matrix row M-667 all agree.
- F2 closed: `run_one` returns `(None, ..., True)` on the emergency stop, `judge` files that row under `unjudged` and skips both `ran` and `faults`, and the exit code reads `faults` alone. Re-derived with `EMERGENCY_STOP_SECONDS` at 1 against `sleep 5`. Of the two non-blocking residuals F2 named, the summary one is closed in 6db4ca8a and the other stands as criterion 11 requires.
- F3 closed: `adopt/install-status-view.sh` now vendors `scripts/task-admission.py` and `scripts/checkpoint.py`, and the probe names an unreadable reader. Re-proved in a host built by running that installer: the recheck line appears, and deleting `scripts/checkpoint.py` produces the named warning instead of silence.
- F4 closed: ba34202e's own message corrects 5ca8697c's "0 of 82" to 15 of 83, the figure this review measured.

The whole suite was left to the three commits' own claims (3,034 passed, 4 then 5 skipped, 1
xfailed) and to CI. This pass ran the six files the change touches and every command named above; no finding
here rests on a suite total.
