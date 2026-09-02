# Prover record — 2026-09-02, the full pushed range read as one

PUSH-REVIEW

Prover skill version: product-prover 4.3.0, with product-prover-pack bindings (live-spec-base 6.1.0).
Mode: FULL — the whole range the push sends, read for reasons to refuse it, not for confirmation.

This record exists because `guardrails/check-prover-record.sh` (SPEC M-6/INV-116/INV-304) holds one
record per push whose `Range:` names the base and every reviewed commit, and no record on file named
the whole of `411a353..de25754`. Two records already cover parts of it —
`docs/prover/2026-09-02-reopened-state-and-open-count-review.md` (over `72a52a4b`) and
`docs/prover/2026-09-02-no-finished-total-review.md` (over `bb59f354`). Their findings are not
repeated here. What is read here instead: whether the fixes committed against them hold, and the
eleven commits neither of them opened.

Range: 411a353..de25754
- de25754 The done line names a real transition, and the board's done column drops its total
- bb59f35 No running total of finished work; the rows closed since the last push speak for themselves
- b36ed9d q-807's own acceptance was too brittle to survive the next edit
- 9261c3a q-807 closes: blocked carries only work that genuinely cannot move
- 2961ffc The review of today's spec change, and the three defects it found, fixed
- f666863 q-809: the rulebook a session loads is 40 KB no longer, and no rule left it
- 43d5f38 Director re-record: the cut is reverted, and the eval's own resolution is now written down
- 72a52a4 Reopened is its own state; the count that leads is the open work; the row's name comes first
- c6ffc70 q-809: census every standing file, and stop plan-0 reading edits-in-hand as unfinished
- 37c40c7 A row that turns out not to be done goes back on the queue, never to blocked
- 9bede80 q-809: cut session start-up weight to a quarter, and judge every standing file
- fc4e919 Two tasks his own reading found: status abuse, and an unreadable task list
- 6e50298 DECISIONS.md: record two standing rules from tonight's chat, verbatim
- 25b4fbd contract: note the parallel-visibility request for the future board work
- 71a4280 state-probe: stop calling the spec/architecture/matrix byte count "canon"
- 4b898f6 q-806: close the turnkey product contract, package 1 done
- 1d3fd61 q-806: open a real ticket + checkpoint for the turnkey-contract work itself
- ba7bc8e Stop gitignoring checkpoints -- resume only ever worked on one machine

Files read: `skills/live-spec-base/SKILL.md` in full at `411a353` and at `de25754`, rule by rule, all
twenty-two rules; `skills/live-spec-base/references/rule-origins.md` in full; `scripts/state-probe.sh`
(all 375 lines); `scripts/render-board.sh` (the acceptance block, the column map, the column header
render, the summary print); `scripts/plan_checks.py` (`CHECKS` for `plan-0`, `q-807`, `plan-7`,
`q-590`, `q-595`; `_CANONICAL_MARKS`, `normalize_mark`, `parse_tasks`); `spec/wish-intake.md`
Requirement 4 clauses 1-13; `spec/message-first-read.md` Requirement 314 clauses 6-10;
`spec/project-setup-tuning.md` criterion [A-9]; `tests/test_tasks_parser_finds_every_task.py` in
full; `tests/test_one_home_per_rule.py` (its reach statement); `evals/director/README.md` at
`411a353` and at HEAD; `.live-spec/checkpoints/q809-startup-weight.md` at `43d5f38` and at HEAD;
`.live-spec/checkpoints/q809-unreferenced-files.txt`; `.live-spec/turnkey-contract-composed.md`
(§10 and its head); `docs/prover/2026-09-02-turnkey-contract-review-fable.md` (its fold column);
`PLAN.md` rows `plan-0`, `q-806`, `q-807`; the full commit message of all eighteen commits above.

Checks run: fourteen, each run here against this tree rather than taken from a commit message.
`python3 -m pytest -q tests/test_plan_is_not_executable.py tests/test_board_matches_the_canon.py
tests/test_tasks_parser_finds_every_task.py` — 25 passed. `python3 -m pytest -q
tests/test_request_classifier.py tests/test_compaction_discipline.py` — 25 passed. `python3
tests/test_one_home_per_rule.py` — four rules, one home each, green. `python3
evals/director/check.py --all` — 30 of 35, 2 extra acts. Every acceptance command in
`scripts/plan_checks.py` run against the live plan — 61 done, 9 queued, 1 in hand, no reopened row.
A phrase table over sixteen distinctive sentences of the old rulebook, each grepped against both the
new body and `references/rule-origins.md` (F2). `git show 411a353:skills/live-spec-base/SKILL.md`
diffed rule by rule against HEAD. `git log 411a353..de25754 -- skills/director/SKILL.md` and
`git hash-object` on that file against `git rev-parse 411a353:…` (F6). Five fixtures built outside
this tree, each proving one finding by construction: a clean tree byte-identical to its own push that
still prints a done line (F3); a postponed row and a folded row both drawn as reopened live work, and
the same postponed row vanishing outright the moment it gains a real `Blocked by:` (F4); twelve closed
rows of which nine print and three are named nowhere (F7); the throwaway test fixture, proving
`printed_done` is structurally zero there (F8); a tree that never ran the migration passing `plan-0`
(F9); a mutation of both readers that restores the exact bug `q-807` closed while `q-807`'s own
acceptance stays green (F10).

Findings: ten. Four are blocking, listed under `Blocking:` below. The two largest sit in the
rulebook cut, whose stated bar — no rule lost — is not met, and one of the losses inverts an
instruction into the opposite of its spec.

One note on state. The tree was clean when this review opened and gained three uncommitted files
partway through it — `skills/live-spec-base/SKILL.md`, `references/rule-origins.md` and
`references/worked-examples.md`, a skill-review lane running beside this one
(`docs/skill-review/2026-09-02-live-spec-base.md`). Every finding below is stated against
`de25754`, and each phrase in F2's table was re-grepped against `git show
de25754:skills/live-spec-base/SKILL.md` and its `rule-origins.md` after those edits appeared; all
fifteen still read zero in both. That lane's diff carries one repair in F2's direction — rule 24's
three footprints, stranded in `rule-origins.md`, moved to `worked-examples.md` where the rule's own
line now points — so the cut's losses are already being worked. F1 is untouched by it: rule 10 reads
the same at `de25754` and in the working tree.

## Findings

**F1 — defect · direct-contradiction (contradiction). Rule 10's deletion clause was inverted by the
cut, and now instructs the opposite of the spec it cites.**

> "A removed feature leaves a dated tombstone in the spec and retired matrix rows. Only junk that can
> be regenerated may be deleted, listed and approved by the person first (SPEC INV-7, A-4, A-9)."
> — `skills/live-spec-base/SKILL.md` rule 10, lines 192-193, at `411a353`

> "tombstone a removed feature; get human approval first except for regenerable junk (SPEC INV-7,
> …)" — the same rule at HEAD, line 166

The old sentence said two things: regenerable junk is the *only* thing that may be deleted, and it is
deleted after being listed and approved. The new sentence says regenerable junk is the one thing
*exempt* from approval. The spec the rule cites is unambiguous the other way:

> "*when* adoption offers a cruft sweep, the system *shall* list the file counts and sizes of
> regenerable junk — caches, build leftovers, already-gitignored files — and *shall* delete only on
> the human's explicit approval. [A-9]" — `spec/project-setup-tuning.md:249`

A session that loads the rulebook and acts on rule 10 as it now reads deletes caches, build leftovers
and already-gitignored files without asking. Nothing in `references/rule-origins.md` restores the
clause — grepped, zero hits for "regenerab" there. This is a rewrite that changed a rule's meaning
inside a commit whose subject is "no rule left it". Fix: restore the clause's direction — deletion is
confined to regenerable junk, and that junk is listed and approved before it goes.

**F2 — defect · missing-rule (invariant). The rulebook cut's own bar is not met: instructions from at
least a dozen rules are absent from both the new body and `references/rule-origins.md`.**

> "q-809: the rulebook a session loads is 40 KB no longer, and no rule left it" — `f666863`, subject
> line

Sixteen distinctive sentences of the old rulebook were grepped against both files. Fifteen are in
neither. Each is an instruction, not a citation, a history or a worked example:

| old sentence, by rule | in the new body | in rule-origins |
|---|---|---|
| 5 — "A one-shot with no decision goes to haiku, multi-step mechanical work to sonnet, and anything carrying judgment or design to the seat." | no | no |
| 5 — "The worker pastes raw output (command + exit code + failing lines) as it works." | no | no |
| 6 — "Red at a pause is never committed: the failing test name and the hypothesis become the top item of `NEXT_STEPS.md`" | no | no |
| 7 — the whole "No unprotected concurrency" bullet, incl. "Sequencing is the default; parallelism is the exception that states its own proof at brief-time." | no | history line only |
| 7 — "Every session mints a stable identity at its start … the start time joined with the worktree path and a single-use random string." | no | no |
| 7 — "or by walking the same steps by hand" | no | no |
| 9 — "A shipped change updates its `README.md`, `CHANGELOG.md`, and `SKILL.md` before the session ends." | no | no |
| 13 — "Your memory, a worker's summary, and a document's prose are leads, each confirmed against that evidence" | no | no |
| 16 — "screen banner · `_prototype: true` field/header · first-line CLI banner · name/header marker" | no | no |
| 17 — "always stop for the human's word, whatever the proactivity mode" | no | no |
| 22 — "The distance to the goal only shrinks." | no | no |
| 25 — "A read to verify a claim or settle a decision stays with the seat." | no | no |
| 31 — "the sender has hit a fault in that zone and carries the evidence" | no | no |
| 31 — "a field with no recorded permission stays home" | no | no |
| 36 — "Never infer this from a title, a repository, or the fact that they are technical elsewhere." | no | no |

Three of these leave a rule unactionable as it now stands. Rule 5's title still promises routing "to
the cheapest tier that passes its brief" and the body no longer names a single tier — grepped,
"haiku" and "sonnet" appear nowhere in `skills/`, `scripts/`, `guardrails/` or `spec/` except
`skills/communicator/` and the glossary, neither of which the routing rule points at. Rule 6's
red-at-a-pause bullet is reduced to the trailing metaphor, "Red at a pause is itself the checkpoint",
dropping a `never` clause, a named file, and the two things the entry must hold. Rule 7 gives a
session no way to mint the identity its own tie-break turns on.

Rule 25's loss is worse than absence: with the carve-out gone, the body now says every read past a
glance is dispatched, which contradicts rule 13's standing duty on the seat to read the primary
source itself.

The commit cites `tests/test_one_home_per_rule.py` as its guard. That test's own reach statement
says what it does: it reds when a rule's sentences appear in **two** homes. It cannot fire on a
sentence that appears in none. Nothing in the suite holds the direction the commit's subject claims,
so "the tests caught both, which is what they are for" states the reach of two greps
(`q-595`, `q-590`) and not the bar. Fix: re-derive the cut from the old file rule by rule, restoring
every clause that tells a session what to do, and — since no check can hold this — say in the record
which clauses were dropped deliberately and why.

**F3 — defect · direct-contradiction (contradiction). The done line is read from two different
predicates, so a row can be reported closed-since-push on a tree byte-identical to its own push, for
ever.**

> "The system *shall* give a row closed since the last push its own line in that account, under the
> done state, and *shall* drop the line once the push lands" — `spec/message-first-read.md` R314
> clause 10

> "It now compares the plan against its own state at the branch's upstream: a row done now that the
> upstream did not have done." — `de25754`, commit message

The code applies one predicate on the current side and a different one at the upstream
(`scripts/state-probe.sh` lines 140-141):

```
_done_at_push = {b["id"] for b in parse_tasks(_base.stdout) if b["mark"] == "✅"}
closed_since_push = {t["id"] for t in tasks if t["icon"] == "✅"} - _done_at_push
```

`icon` is the acceptance command's verdict; `mark` is what a person typed. A row whose command
passes while its mark is still `⬜` has `icon == "✅"` now and `mark != "✅"` upstream, so it enters
the set — and pushing cannot remove it, because the mark upstream never becomes `✅`.

Proved by construction, outside this tree: a fixture with `q-1` marked `⬜` carrying a passing check
and `q-2` marked `⬜` carrying none, committed and pushed to its own remote, working tree clean and
byte-identical to the pushed head. The real `scripts/state-probe.sh` prints:

```
  q-1 ✅ Ship the widget  verified
  q-2 ⬜ Other work  declared  <-- NEXT
  … 1 open · 0 more below · full list in PLAN.md / board.html
```

Clause 10's "shall drop the line once the push lands" never fires. The same nine lines carry their
own contradicting comment: "a row that went green because its command started passing on its own
leaves no trace here and shows only by leaving the open list" (lines 123-125) — that row is exactly
`q-1`, and it leaves a trace on every run.

The mirror case loses a line that is owed: a row marked `✅` upstream whose command was failing there
(drawn `🔁`) and now passes is in `_done_at_push` by mark, so closing a reopened row — the very state
this range invented — produces no done line at all. Nothing tests either direction: grepped, no test
in `tests/` names `closed_since_push` or `@{u}` against the probe. Fix: read the same predicate on
both sides — the upstream plan run through the same acceptance verdict, or the mark on both sides —
and state in clause 10 which one "done" means there.

**F4 — defect · boundary-issue (composition). The class the previous review named was fixed for one
field of three, and the fixing commit records the finding as fixed.**

> "The same silent drop applies to `covered_by` (a row whose work is actually carried by another
> task) and `deferred` (his own decision to hold it) … Fix: … reopened applies only where
> `blocked_by`/`covered_by`/`deferred` are all empty. Write that sentence into clause 10, and extend
> `state-probe.sh`'s reweighting set to include `🔁`."
> — `docs/prover/2026-09-02-reopened-state-and-open-count-review.md`, F1

> "**A row shaped like both.** … Blocked now wins … New clause 12 in spec/wish-intake.md." — `2961ffc`,
> listing this among "the three defects it found, fixed"

Only `blocked_by` was read. The reweighting set was not extended: `scripts/state-probe.sh` line 150
still reads `if t["icon"] not in ("⛔", "⬜"): continue`, and `🔁` is never in that set. Clause 10 and
the new clause 12 name `blocked_by` alone. `covered_by` and `deferred` are still unread for a
reopened row, in both readers.

Proved by construction with the real `scripts/state-probe.sh` over a three-row fixture — a
done-marked row carrying `**Deferred:** after the release (his word)` whose command fails, a
done-marked row carrying `**Covered by:** q-D` whose command fails, and one genuinely queued row:

```
  q-D 🔁 Postponed by the owner, and its proof stopped holding  marked done — its acceptance command fails
  q-Q ⬜ Real queued work  declared  <-- NEXT
  q-C 🔁 Folded into another task, and its proof stopped holding  marked done — its acceptance command fails
```

Both rank as live reopened work above the queued row, and neither prints the `Deferred:` or
`Covered by:` line it carries. On the board they land in the in-progress column, under
"in the pipeline right now".

The composition also inverts. Adding a real outside cause to that postponed row — the case clause 12
was written for — makes it disappear from the account instead of stating both facts:

```
  q-C 🔁 Folded into another task, and its proof stopped holding  marked done — its acceptance command fails
  q-Q ⬜ Real queued work  declared  <-- NEXT
  … 3 open · 1 more below · full list in PLAN.md / board.html
```

`q-D` now has `icon == "⛔"`, enters the reweighting block, hits `if t["deferred"]: excluded = True`
and drops out of the ranking entirely. Clause 12 says the system "*shall* state both facts beside it:
the cause it names, and that the command meant to prove it done is failing." It states neither. A
person adding the reason a row cannot move is the action that hides the row. Fix: read all three
fields for `🔁` as the clause's fix asked, and state in clause 12 what happens when a blocked,
failing, done-marked row is also postponed or folded — today the answer is silence, and it is
reachable.

**F5 — defect · direct-contradiction (contradiction). `q-806` is marked done while its own
deliverable and its own review record both say it is not.**

> "**Acceptance:** A short product contract … reviewed by product-prover twice … with every defect
> folded, and the one remaining owner-only question answered." — `PLAN.md`, `q-806`

Three files in this tree disagree about that row today. `PLAN.md` marks it `✅` (`4b898f6`).
`.live-spec/turnkey-contract-composed.md`, added by that same commit, still reads at line 17
"One open item remains … Ready for test-author once that one answer lands", and its §10 still opens
"**One question only the owner can answer** … does a ticket carry a time estimate?".
`docs/prover/2026-09-02-turnkey-contract-review-fable.md`, also committed by that same commit, carries
a fold column whose fifteen rows all read `open`, above a readiness line of "needs another iteration
… it must not start before they land."

The question was in fact answered — two commits later, in `DECISIONS.md` (`6e50298`, lines 186-188,
the estimate at take-up and the pair at close). So the mark was ahead of its own acceptance when it
was set, and the two artifacts were never brought forward. This is the shape `q-807` was opened
about, one level up: a row asserting a state its own evidence contradicts. Fix: update §10 and line
17 of the composed contract and the Fable record's fold column, or move the mark back until they are.

**F6 — defect · direct-contradiction (contradiction). The director eval record carries three
different scores for one byte-identical skill, and the run it says decided the question has no data.**

`skills/director/SKILL.md` was never modified anywhere in this range —
`git log 411a353..de25754 -- skills/director/SKILL.md` is empty, and
`git rev-parse 411a353:skills/director/SKILL.md` and `git hash-object` on the working file are the
same blob, `22738bd4`. No 21,900-byte version exists on any ref. So the "revert" is a no-op on the
committed history, and under the README's own standing rule ("Any change to `skills/director/SKILL.md`
re-records all thirty-five scenarios") no re-record was owed.

What the record says, at HEAD:

> "per scenario under the isolation protocol above, graded once: 34 of 35 pass" — `evals/director/README.md:99`

> "| the skill as it stands (25,613 bytes) | 30 of 35, 2 extra acts |
> | the same skill cut to 21,900 bytes | 29 of 35, 4 extra acts |" — the same file, lines 116-117

Line 99 and line 116 report the same skill text. `.live-spec/checkpoints/q809-startup-weight.md`
independently says 32. Nothing on the page reconciles the three. I ran the committed grader:
`python3 evals/director/check.py --all` → `30 of 35 recorded runs pass; 2 named an act the scenario
did not ask for`, matching line 116 and not line 99. `evals/director/` holds one trace set of 35
files; the 29-of-35 row has no trace directory, no result file, and no artifact in `43d5f38`'s stat.
The README does say in prose that "the run does not certify the cut either way" — but the commit's
own subject, "the eval's own resolution is now written down", and its ordering of the two rows read
as though the score decided it.

Separately, `43d5f38` committed a checkpoint stating two size reductions as accomplished that had not
happened in any commit at that moment: `| skills/live-spec-base/SKILL.md | 40443 | ~16500 |` while
that file was still 40,443 bytes at `43d5f38`, and `| skills/director/SKILL.md | 25613 | 21900 |` for
a file no commit ever changed, under "Total ~53.4 KB, a third off." Both were corrected two commits
later. In a project whose premise is that the recorded state is the measured state, a checkpoint that
was false at the moment it was committed is the defect, not the correction. Fix: strike or reconcile
line 99, and either publish the cut run's traces or remove the comparison table and say the revert
was a judgment call.

**F7 — defect · missing-outcome-check (postcondition). Closed rows past the line budget are dropped
from the account and counted nowhere.**

> "So a done line costs nothing here, and the list runs past the budget only while closed work is
> waiting to be pushed" — `scripts/state-probe.sh`, lines 187-191

> "They already cost nothing against the line budget" — `de25754`, commit message

The `✅` category is exempted inside the round-robin body, but the loop's own guard is not:
`while budget > 0 and progressed` (line 193). Once the open categories exhaust the nine lines, the
loop exits with closed rows still unshown. Proved by construction with the real script, twelve closed
rows and nine queued rows:

```
  d-08 ✅ Closed thing 08  verified
  o-08 ⬜ Open thing 08  declared
  … 9 open · 0 more below · full list in PLAN.md / board.html
```

Nine of twelve done lines printed; `d-09`, `d-10` and `d-11` appear nowhere. `more_below` (line 245)
counts only rows whose icon is not `✅`, so it reports 0. Three rows the person closed are neither
shown nor mentioned. Fix: either exempt `✅` from the loop guard too, or add the dropped closed rows
to a figure the summary line carries.

**F8 — defect · missing-outcome-check (postcondition). The assertion added to answer the previous
review's F5 cannot fail: its fixture forces the quantity to zero.**

> "printed done rows cannot outnumber the rows that are not open … so the narrowing is visible rather
> than silent" — `de25754`, commit message; the assertion is
> `tests/test_tasks_parser_finds_every_task.py`, `assertLessEqual(printed_done, len(self.declared) - open_count)`

`setUp` copies a list of files into a temp directory with `shutil.copy2` and never copies `.git`. In
that fixture `git rev-parse --abbrev-ref --symbolic-full-name @{u}` fails, `closed_since_push` stays
empty, and no `✅` line is ever printed. I ran the fixture's own `_run_probe` directly: 9 rows
printed, **0** printed as done, `.git` absent. `printed_done` is structurally zero, so the assertion
is green for every possible tree. The same fixture is why F3 and F7 above are untested: the whole
closed-since-push feature — the headline of the range's last two commits — has no coverage at all.
Fix: give the fixture a real upstream (the pattern is already in `tests/test_wind_down.py`), or drop
the assertion rather than carry a green that proves nothing.

**F9 — defect · missing-outcome-check (postcondition). `plan-0`'s acceptance is satisfied by a fresh
clone of this repository on a machine that never ran the migration.**

> "`bash scripts/state-probe.sh` confirms it matches `origin/main`, the tree is clean, and no
> `/private/tmp` line appears in ALARM." — `PLAN.md`, `plan-0`

> `test "$(git rev-parse --abbrev-ref --symbolic-full-name @{u} …)" = "origin/main" && ! test -d
> /private/tmp/ls-director && grep -q "Владелец подтвердил" attic/DIRECTOR_HANDOFF-2026-08-26-decisions.md`
> — `scripts/plan_checks.py`

Each arm is satisfied by the ordinary state of any clone. Proved by construction: a fixture repo
holding one file — `attic/DIRECTOR_HANDOFF-2026-08-26-decisions.md` with the grepped phrase — pushed
to a remote and tracking `origin/main`, with an untracked file in the working tree and no `PLAN.md`,
no `scripts/`, and nothing the migration produced. All three arms pass.

Three narrower gaps sit under that. Arm 1 reads "the upstream is configured as origin/main", which is
not what the probe means by "matches origin/main" (line 32: zero ahead and zero behind). Arm 2 covers
one of the two `/private/tmp` ALARM arms — `git worktree add /private/tmp/x` makes the probe print
"working tree in /private/tmp" (line 340) while the check stays green. And the dropped
`git status --porcelain` clause was replaced by nothing: the comment in `scripts/plan_checks.py`
defines the row's "tree is clean" as "no project files left outside it — the 133 outside-git files it
checked", then checks no such thing. Fix: check the thing the comment names, or say in the row that
the clause has no replacement.

**F10 — defect · missing-outcome-check (postcondition). `q-807`'s acceptance stays green over a
mutation that restores the exact bug `q-807` closed.**

> "Anchored on the assignment and on the guard, the two smallest things that must survive any
> rewording of these blocks" — `scripts/plan_checks.py`, `q-807`'s own comment (`b36ed9d`)

The four arms are fixed-string greps for the assignment `["icon"] = "🔁"` and for the guard text
`failing_key"] and t["blocked_by"]` in each reader. They hold that the two strings are *present*,
not that the guard is reachable. Proved by construction: copy both readers outside this tree and
swap the two branches in each, so the blocked branch becomes unreachable dead code —

```
        if t["failing_key"]:
            t["icon"] = "🔁"
        elif t["failing_key"] and t["blocked_by"]:
            t["icon"] = "⛔"
```

— and run `q-807`'s own acceptance against the mutated pair. It exits 0. Under that mutation a
done-marked, failing, `blocked_by`-carrying row is drawn reopened again, which is precisely the
defect `9261c3a` and `2961ffc` closed. The end-to-end guard the comment names
(`tests/test_plan_is_not_executable.py::TestADoneMarkCannotOutliveItsKey`) does hold it, and it is
not what the row's key runs. Fix: anchor the key on the behaviour — the ordering, or a two-line
Python that constructs the composed row and reads the icon back — rather than on two strings.

Class lens: swept. F1 and F2 are one class — a compaction that changed instructions while its subject
claimed none changed — and the sweep is the whole rulebook, done rule by rule above. F3, F4, F7 and
F10 are one class: a state or a set derived from the wrong predicate, and a check anchored on text
rather than on the outcome. F8 is that class's reason — every one of them survives because the only
fixture that exercises the probe end to end cannot reach the code they live in. F5 and F6 are one
class, a record committed ahead of the tree it describes; checked for siblings across the range's
other records and found `.live-spec/checkpoints/q809-unreferenced-files.txt`, which writes "zero hits
anywhere" for files that are cited elsewhere (`turnkey-contract-draft-fable.md` is cited by
`docs/prover/2026-09-02-turnkey-contract-review.md` and by `.live-spec/turnkey-contract-composed.md`,
both written the same day), and `c6ffc70`, whose "26 of those 34 are still cited by the prover review
records under `docs/`" holds for 23; the eight files it actually deleted are genuinely unreferenced,
and one file it kept, `.live-spec/s1-rule-29-2026-08-12.md`, was orphaned by the same commit, its
only citation being inside a file the commit deleted. F9 stands alone.

Carried forward, not re-argued: `🔁` is still absent from `_CANONICAL_MARKS` and from the
"Five marks and no more get invented" line the code names as its one home, and clause 10 still
carves out no exemption for a computed-only mark. `2961ffc` names this as standing rather than fixed,
so it is recorded here as still open, not as a new finding.

Blocking: four — F1, F2, F3, F4.
- F1 rule 10's deletion clause inverted, contradicting `spec/project-setup-tuning.md` [A-9] — stands: not fixed in this pass; this reviewer does not clear the push while a loaded rule instructs a session to delete without the approval its own spec requires.
- F2 fifteen instruction sentences absent from both the body and `references/rule-origins.md`, against a commit subject of "no rule left it" — stands: not fixed in this pass; the cut needs re-deriving rule by rule, and no check in the suite holds this direction.
- F3 the done line read from `icon` now against `mark` at the upstream, so a line can never drop off — stands: not fixed in this pass; it breaks R314 clause 10 as written and has no test.
- F4 `covered_by` and `deferred` unread for a reopened row, and clause 12 silently violated when a postponed row gains a real cause — stands: not fixed in this pass; the previous review named the class and the fix closed one field of three.

## Verdict

Needs another iteration before this range goes out. F1 is the one to fix first and is small: one
sentence restored to rule 10. F2 is the largest piece of work in the range and the least bounded —
the cut has to be re-derived against `411a353`'s file, and since no check can hold the bar, the
record has to name what was dropped on purpose. F3 and F4 are each a few lines in
`scripts/state-probe.sh` plus one sentence in the spec, and both need the fixture of F8 before either
fix can be proved. F5 through F10 are records and checks that say more than the tree supports; none
of them changes what the code does, and each is a short edit.

---

## Adjudication, written by the seat, 2026-09-02

The findings above were read a second time, in clean context, with a different question: for each
sentence the review calls lost, does the substance survive somewhere a session actually reads, and
where it genuinely does not, is the removal a defect or an improvement. That reading is
`.live-spec/checkpoints/q809-rule-loss-verdicts.md`. Its verdict on finding 2's sixteen sentences:
ten survive, four are genuine defects, one is a genuine improvement. Eight of the review's claims
rest on a grep for wording rather than for the rule, and are withdrawn here:

- **Rule 5's tier mapping.** The concrete model names were removed because the rulebook's own scope
  rule bans host- and person-specific values from it; the vendor-neutral mapping stands at
  `spec/roles-and-agents.md:279`, and the concrete tier is the profile's `worker-tier` line.
- **Rule 7's "No unprotected concurrency" bullet.** Its operative clause is the bullet now headed
  "Brief-time disjointness"; `spec/roles-and-agents.md:296` holds them as one clause. The old file
  stated one rule under two headings.
- **Rule 7's session identity**, **rule 16's label forms**, **rule 31's field permission**, **rule
  36's never-infer clause** — each survives, in the body or in the spec code the rule cites.
- **Rule 25 contradicting rule 13.** The review quotes the body with four words removed and reasons
  from the shortened sentence. The carve-out is `spec/roles-and-agents.md:377` [INV-137].
- **"No record says which clauses were dropped and why."** That record is
  `.live-spec/checkpoints/q809-inventory-base.md`, rule by rule.

The four genuine defects are repaired in the body, each as one sentence: rule 6's red-at-a-pause
premises, rule 7's push-in-flight clause, rule 9's shipped-document duty, and rule 31's second
ground for an earned message. Rule 10 is repaired too, in neither direction the review proposed:
the old sentence stated the adoption cruft sweep's rule as a universal ban, its compression exempted
regenerable junk from approval everywhere, and the body now says what `spec/project-setup-tuning.md:249`
[A-9] actually says.

Findings 3, 4, 7 and 8 are upheld and fixed in the code: the done set compared the icon now against
the hand mark at the upstream, the reopened mark skipped the fold bookkeeping every other open state
passes through, the line loop dropped done rows once the open budget ran out, and the assertion
answering the earlier review was vacuous on a fixture with no `.git`. Finding 8's repair is a new
real-repository test that re-derives the owed set independently.

Finding 6 is upheld: `skills/director/SKILL.md` is unchanged across this whole range. The cut lived
in the working tree and was withdrawn before it was committed, so the commit that reports a revert
overstates what git carries. `evals/director/README.md` now says so, and says which of its recorded
scores are comparable with each other.

Findings 5, 9 and 10 stand open, recorded here rather than fixed: q-806's own deliverable and the
Fable review record were never brought forward after the question they wait on was answered;
plan-0's acceptance passes on a fresh clone that never ran the migration; and q-807's fixed-string
greps stay green over a mutation that makes the blocked branch dead code. None changes what this
range ships, and each is a row's own work.
