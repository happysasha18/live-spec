# Prover record — 2026-09-08 the time oracle changes what it proves

PUSH-REVIEW

Prover skill version: product-prover 1.6.2, installed under `skills/product-prover/`, read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 and `skills/live-spec-base/SKILL.md` v6.1.0.
Lens-set digests: `SKILL.md` 5d98c4309c91, `reference/stress-lenses.md` 422e3b9a43a9. The pass was
run by a seat that authored none of these three commits, briefed to find reasons to refuse them
and to hold them defective until evidence said otherwise. The third commit repairs a red test by
editing the test, so it was judged by planting the regression the test exists for, twice, rather
than by reading the commit message's own claim about it.

Range: 186dc4a..cdae2e34 — the base the remote holds, then the four commits this push sends,
18f41e17 through cdae2e34. The fourth, cdae2e3, carries this record's first version along with
other work, and is reviewed in F5 and F6 below. The commit that ships this extension carries only
`docs/prover/`, so the gate's record-only exemption covers it and it needs no naming of its own.

- 18f41e17 Admission reads the record before it writes a row — Requirement 321 under INV-327, matrix
  rows M-651 to M-656, and the record-reading block in `scripts/task-admission.py`. Reviewed in full
  in `docs/prover/2026-09-07-the-door-reads-the-record-and-where-that-read-goes-soft.md`; not
  re-derived here.

- 07544d0e The record's own read is stated as the door performs it — criterion 1, the Context
  paragraph and the User Story of Requirement 321 reworded; `admit`'s collision scan `break` became
  a `continue`; `test_m654_a_second_colliding_row_still_refuses_when_supersedes_names_only_the_first`
  added; the 2026-09-07 record committed. This commit closes findings F3 and F8 of that record, and
  the updated record it carries states both closures.

- cdae2e34 The day's reviews: the spec, the two skills, and rule 43's origin — this record's own
  first version, the two skill-creator review records under `docs/skill-review/` for
  `build-pipeline` and `live-spec-base`, a new origin entry for rule 43 in
  `skills/live-spec-base/references/rule-origins.md`, and a rewrap of rule 43's paragraph in
  `skills/live-spec-base/SKILL.md`. Reviewed in F5 and F6 below. This commit touches
  `docs/skill-review/` and `skills/`, both outside `docs/prover/`, so the gate's record-only
  exemption does not reach it and naming it here is owed rather than optional.

- e30ad7a2 The board's time oracle reads a committed record and says when it cannot —
  `tests/test_work_board.py` only, 45 lines added and 5 removed. `_checkpoint_opened_line` is new.
  `TestFreshClone::test_every_time_on_the_page_is_a_recorded_one_not_the_checkout_instant` now
  prefers a row's own recorded `OPENED:` line over git's first-commit time for that row's
  checkpoint.

Files read (second pass, over cdae2e3): `skills/live-spec-base/references/rule-origins.md`
(the new rule 43 entry), `skills/live-spec-base/SKILL.md` (rule 43's paragraph either side of the
rewrap), `DECISIONS.md` (the entries at 2026-09-07 22:32 and 22:33),
`docs/skill-review/2026-09-08-live-spec-base.md`, `docs/skill-review/2026-09-08-build-pipeline.md`,
`skills/build-pipeline/SKILL.md`, and the diff `git diff 186dc4a2..cdae2e34 -- skills/`.

Files read: `tests/test_work_board.py` (the `clone` fixture, `_git_recorded`,
`_checkpoint_opened_line`, and both tests of `TestFreshClone`), `scripts/render-board.sh`
(`git_stamps`, `stamps`, `recorded_open`, `read_checkpoints`), `scripts/task-admission.py`
(`admit`'s collision scan, `read_prior_record`, `read_supersedes`, and the `OPENED:` write at
admission), `spec/queue-intake-priority.md` Requirement 321, `tests/test_task_admission.py`
(the new M-654 test), `PRODUCT_SPEC.index.md`, the three commits' own diffs, and the 2026-09-07
record this one carries forward from.

Checks run: the two test files the range touches, the two spec-format gates, and three planted
regressions against the renderer, each run through the changed test. Each with its result below.
The full suite was not run here; the pushing session records its own green for this range.

```
$ python3 -m pytest -q tests/test_work_board.py
32 passed in 74.83s
(exit 0)
```

```
$ python3 -m pytest -q tests/test_task_admission.py
69 passed in 6.04s
(exit 0)
```

```
$ python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md
OK — all 1829 criteria well-shaped across 315 requirements
(exit 0)
```

```
$ python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md
OK — committed index equals the fresh build; 404 codes agree body-to-table
(exit 0)
```

Second pass, over cdae2e3:

```
$ bash guardrails/check-shipped-language.sh
OK (shipped-language): no Cyrillic, owner-name, or project-name offences in the shipped set.
(exit 0)
```

```
$ python3 scripts/task-admission.py prior weekly digest
rows on the record: 0 / DECISIONS.md: 0 / commits: 0
(exit 0 — the command the build-pipeline body now tells a session to run does run)
```

The rewrap check, run as a token comparison rather than by eye.
`git show <rev>:skills/live-spec-base/SKILL.md` either side of cdae2e3, rule 43's paragraph sliced
from its number to the next heading, and both slices split on whitespace:

```
word count before/after: 120 120
token streams identical: True
```

So the paragraph's words and their order are unchanged and only the line breaks moved. A
whitespace-insensitive comparison is the right instrument here: a rewrap is by definition a
whitespace change, and a line diff cannot tell one from an edit.

The three planted regressions, each a copy of `scripts/render-board.sh` pointed at through
`LIVE_SPEC_BOARD_RENDERER`, the override the test file already carries for this purpose. The
repository's own renderer was not touched.

```
plant 1 — `cp["opened"] = born`, the recorded line ignored and the stamp taken instead
$ LIVE_SPEC_BOARD_RENDERER=<plant> python3 -m pytest -q tests/test_work_board.py -k <the time test>
FAILED — AssertionError: ('q-825', '2026-09-07T23:15', '2026-09-07T21:31')  at line 1166
```

```
plant 2 — the records-only branch of `stamps` deleted, so the fallback reads the filesystem
FAILED — at line 1150, the checkout-instant scan, before the per-row oracle is reached
```

```
plant 3 — `git_stamps` returns git's LAST write where it should return the first appearance
FAILED — AssertionError: ('q-816', '2026-09-06T17:58', '2026-09-06T07:17')  at line 1166
```

Findings: six new, of which none blocks, and four carried forward from 2026-09-07 that still
stand. The verdict on the third commit is F1 below; the fourth commit is F5 and F6.

F1 — The oracle change is right, and the guarantee it gives is not the guarantee it gave.

> "each recorded time is the one the row itself carries — its own OPENED line where admission wrote
> one, and git's first sight of the checkpoint where it did not." — `tests/test_work_board.py`,
> `TestFreshClone::test_every_time_on_the_page_is_a_recorded_one_not_the_checkout_instant`

I agree with the repair. The old oracle compared the page against git's first-commit time for a
row's checkpoint. That was a proxy for the promise, and the promise is that the page's times come
from the record rather than from the checkout instant. The proxy held only while rows were
committed as they were worked. Two rows admitted, worked and committed in one batch broke the
coincidence, and when it broke the page was right and the oracle was wrong. Repairing an oracle
that has drifted from the promise it stands for is the correct move, and the product was not the
thing at fault here. Base rule 42 is the rule this shape has to answer to, and it is answered:
the definition of done was not rewritten to fit what shipped, because nothing shipped — the
renderer is unchanged in this commit, which touches one test file and nothing else.

I did not take the commit message's word that the guard still bites. Plants 1 and 3 above are mine.
Plant 1 makes the renderer ignore the recorded line and take the stamp; the test reds on q-825, a
record-carrying row, at the per-row oracle. Plant 3 makes the git branch return git's last write
instead of its first appearance; the test reds on q-816, a git-checked row, at the same line. Both
halves of the oracle bite. Plant 2, which sends the fallback to the filesystem, reds at the coarser
checkout-instant scan before the per-row oracle is reached, so that plant proves the outer assertion
rather than the oracle.

What the oracle now promises for the two rows carrying a recorded line, stated plainly: the page's
opened time equals, to the minute, the `OPENED:` string standing in the DONE section of that row's
checkpoint as git holds it at HEAD. Reading it through `git show HEAD:<path>` makes committedness
part of the check, so an uncommitted local edit to a checkpoint can no longer satisfy the oracle.
That is a real gain over reading the clone's filesystem.

The boundary of that promise is its own sentence. For those two rows the check no longer touches
git's history at all. It compares a string on the page against a string in a committed file, and
the older oracle proved the page's time was one git independently knew. A checkpoint committed with
a hand-written or fabricated `OPENED:` line now passes, where the git proxy would have caught it by
disagreeing. Whether that line is trustworthy is `task-admission.py`'s job, and today 2 of the 25
checkpoints in the tree carry one, so 23 rows still ride the git branch. The trade is defensible
and it is a trade, and it belongs in the test's own words rather than only here.

Add one sentence to the test's docstring saying what the recorded branch proves and what it stops
proving. The docstring still reads "Times here come from git — the record", which described the
oracle before this commit and now describes only the fallback half.

`recommendation · now · hard-to-monitor (observability)`

F2 — The test's name still fits, and the named-row assertion at its foot did not learn the new
oracle.

> "card = model['cards']['q-816']; born, _ = _git_recorded(clone['tree'],
> '.live-spec/checkpoints/q-816.md')" — the last three lines of the same test

The name, `test_every_time_on_the_page_is_a_recorded_one_not_the_checkout_instant`, still describes
what the test holds. Both branches yield a recorded value, one recorded by admission and one
recorded by git, and neither is the checkout instant, which the separate minute scan holds on its
own. No rename is owed.

The foot of the test is a different matter. After the loop learned the two-branch oracle, the
by-name check on q-816 still calls `_git_recorded` unconditionally. It holds today because q-816's
checkpoint carries no `OPENED:` line, which I confirmed. `task-admission.py` writes that line at
admission for every row admitted from now on, so the git branch is the shrinking one. Should q-816's
checkpoint ever gain the line, the renderer would prefer it, the loop above would pass, and this
tail alone would red with a message about a row nobody changed.

Have the tail call `_checkpoint_opened_line` first and fall back the same way the loop does, so the
named-row check cannot drift from the oracle it is meant to illustrate.

`recommendation · now · internal-conflict (consistency)`

F3 — A malformed `OPENED:` line makes the renderer and the oracle disagree by design.

> "return line[len('OPENED: '):].strip()" — `_checkpoint_opened_line`, against
> "return datetime.fromisoformat(...)  except ValueError: return None" — `recorded_open` in
> `scripts/render-board.sh`

The renderer parses the line and falls back to the git stamp when the parse fails. The oracle
returns the raw string and takes its first sixteen characters, with no parse and no fallback. So a
checkpoint carrying an `OPENED:` line that is not an ISO timestamp sends the two down different
branches: the page shows a git time, the oracle demands a string, and the test reds with a
comparison a reader cannot act on. Nothing in the tree carries such a line today, since
`task-admission.py` writes `isoformat(timespec="seconds")` every time, so this is a latent seam
rather than a live defect.

Parse the line in the helper with `datetime.fromisoformat` and return None on a `ValueError`, which
is the renderer's own rule, so a malformed line puts both sides on the git branch together.

`recommendation · later · undefined-path (transitions)`

F4 — Observed during this review, not a finding against the range: another session wrote to the
judged tree while the suite ran.

A first run of `tests/test_work_board.py` and `tests/test_task_admission.py` together ended with an
error at the teardown of `test_m656`, raised by the session-scoped `judged_tree_gains_no_commits`
fixture. The cause was not that test. `skills/live-spec-base/SKILL.md`,
`skills/live-spec-base/references/rule-origins.md` and two new files under `docs/skill-review/`
changed under the run, from a concurrent session landing a skill review. Both files run green on
their own with the tree held still, which I confirmed by snapshotting `git status` either side of
each run. The guard did its job. It names whichever test ran last rather than the writer, which is
worth knowing before somebody chases the named test. Recorded here because a reader of this record
may see the same error and reach for the wrong cause. Base rule 7's fence is the rule that governs
the situation itself, and it is the concurrent session's to keep.

`recommendation · now · hard-to-operate (ops-ux)`

F5 — Rule 43's origin entry cites a real, dated source, and its worked example rests on two
numbers with no home.

> "earlier that same evening this seat had proposed 600 and 1800 seconds as an acceptance and a
> release budget for a run-mode contract, derived from two full-suite runs measured on one machine
> that day — 843 seconds and 1393 seconds." — `skills/live-spec-base/references/rule-origins.md`,
> "## Rule 43"

The citation holds. `DECISIONS.md` carries an entry at 2026-09-07 22:32 and 22:33, exactly as the
origin names it, with the owner's words in the original and an English rendering beside them. The
origin's paraphrase is faithful to that rendering on every clause I checked: no budget derived from
a measurement, two local full runs are no policy, a budget fixes composition and volume — named
targets, the count of cases and samples, no N-squared sweep and no historical sweep — and a timeout
stays an emergency stop on a process the run owns, never derived from this machine's speed, taking
no part in a green verdict, calling for no baseline, load or quiet-machine comparison. Nothing is
added and nothing is softened.

The language bar holds. The entry is English throughout: a character scan of
`skills/live-spec-base/references/rule-origins.md` finds zero Cyrillic in the file and zero in the
rule 43 section, and `guardrails/check-shipped-language.sh` reads OK. The owner's own words stay in
`DECISIONS.md`, where the quoted original belongs, and the origin cites that entry by date and time
rather than reproducing it.

The worked example is where it goes soft. The two measurements it rests on, 843 seconds and 1393
seconds, appear nowhere else in this tree — not in `JOURNAL.md`, not in `DECISIONS.md`, not in any
file. The entry explains why the proposed 600 and 1800 are absent, since the draft was killed before
they landed, and that explanation does not reach the two runs the proposal was derived from. So the
one paragraph in the pack that illustrates "a clock never certifies a budget" carries two unsourced
durations of its own. Nothing reads them and no threshold turns on them, so this is a recommendation
rather than a defect, and the irony is the reason to fix it rather than the finding itself.

Either name where the two runs were measured — a journal line, a commit, a transcript — or drop the
two figures. The example works without them: two full runs on one machine is the whole point, and
their durations add nothing the sentence needs.

`recommendation · now · unenforceable-promise (discharge)`

F6 — The two skill reviews found real things; one repaired a class pointwise, the other proved prose
against prose.

> "rule 42, landed earlier, has the same gap, so this is not new to rule 43 alone." —
> `docs/skill-review/2026-09-08-live-spec-base.md`, finding 1

The live-spec-base review earned its place. It found rule 43 standing with no origin entry and no
inline incident, and it found rule 43's paragraph wrapped narrower than every neighbour. Both were
repaired in the same commit, which is the right shape: a finding lands with its fix rather than
becoming a row. Its count check is right too — the body carries 29 numbered rules and the
frontmatter now reads "twenty-nine".

The repair is pointwise, and the review's own sentence says why that is wrong. It names rule 42 as
carrying the same gap and points at the rule-40 and rule-41 records for the same class. The origins
file still runs "## Rule 41" and then "## Rule 43", with no rule 42 entry, so a class the review
identified in writing was answered for one member. The pack's own rule of thinking is that an
incoming item is a symptom and the answer owed is a rule about its class. Add rule 42's origin in
the same pass, and say in the origins file which rules deliberately carry none, so the next reader
can tell a gap from a decision.

The build-pipeline review is five findings, every one of them "No finding", and its method is why.
Findings 3 and 4 check the skill's new stop-and-ask text against Requirement 321 criteria 7 and 8,
word against word — "near-verbatim", "same content". That proves the skill paraphrases the criteria
correctly. It does not ask the question a reader most needs answered, which is whether anything
makes the pipeline behave that way. Nothing does: criteria 7 and 8 carry no matrix row, and their
only backing in the tree is one `grep -q` for the sentence "One case waits for the answer" in the
very file the review was reading. A review comparing a skill's prose to a spec's prose, where the
spec clause is itself unbacked, closes a loop that never touched behaviour. That is the finding my
2026-09-07 record filed as F9, reached here from the other side.

Have a skill review state, for each clause it clears, whether the behaviour behind it is held by a
test, by a gate, or by nobody. The third answer is the useful one, and it is the one this review
owed three times.

`recommendation · now · unenforceable-promise (discharge)`

Carried forward from 2026-09-07, still standing against this tree. Each was verified present at
HEAD today rather than assumed; the detail, the evidence and the proposed repair for each live in
`docs/prover/2026-09-07-the-door-reads-the-record-and-where-that-read-goes-soft.md`.

- The substring match on a runner's name. `scripts/task-admission.py:758` still reads
  `if "pytest" in key`. It admits `python3 -m unittest -q tests.test_all`, which runs a whole
  suite, and refuses `grep -q pytest tests/conftest.py`, which runs none. Filed for the class:
  the criterion behind it is being removed in separate work, and the next cheap-check rule must
  not be written as a name match. Record of 2026-09-07, F2.
- The letter-suffixed criterion invisible to the spec parser and to the generated index.
  `spec/queue-intake-priority.md:782` still opens `6a.`, `specformat.py` matches only `^(\d+)\.`,
  and `PRODUCT_SPEC.index.md:379` still maps INV-327 to R321.1 through R321.8 with no 6a in it.
  Both format gates read green over that, today, in this record's own check block. Record of
  2026-09-07, F1.
- The supersedes lift judging one field of three. `scripts/task-admission.py:177` still requires
  `names`, `new` and `why` to be non-empty and resolves `names` alone, so one character in each of
  the other two lifts the door's strongest refusal. The early-exit half of that finding was closed
  in 07544d0e and is not carried. Record of 2026-09-07, F8.
- A route may legally name no references at all. `read_prior_record` still accepts an empty `read`
  list by design, and `new_route()` in the test fixture still ships one, so the finding — the only
  mandatory field of the read is the one nothing can check — is unchanged. Record of 2026-09-07, F4.

Also still standing, unchanged and not re-derived: the exact-title scan against the requirement's
own story, the refusal naming `PLAN.md` over the archive file for the 72 rows that stand in both,
and the blank seam between Requirement 321 and Requirement 5 criteria 3 and 4. Records of
2026-09-07, F5, F6 and F7.

Spec and architecture re-check: `PRODUCT_SPEC.md` is unchanged in this range; the delta lands in
`spec/queue-intake-priority.md`, which the freshness arm reads as part of the same document, and
07544d0e is its only touch. `ARCHITECTURE.md` and everything under `architecture/` are unchanged in
this range. e30ad7a2 touches one test file and no product code, so it moves neither document.
cdae2e34 touches no product code either: two skill files gain an origin entry and a rewrap,
and everything else in it is records.

Blocking: two, both standing, and both carried from the record of 2026-09-07 rather than raised by
this range. Nothing in these three commits blocks.
- The substring match on a runner's name stands: `if "pytest" in key` admits a whole unittest suite
  and refuses a grep that runs nothing, both proved against the shipped code on 2026-09-07 and the
  line unchanged at HEAD today. It stands because the criterion it enforces is being removed in
  separate work the owner has already ruled on, and this review does not touch `scripts/`.
- The letter-suffixed criterion stands: `6a.` is invisible to `specformat.py`, so the index gate,
  the shape gate and every criterion-reading check pass over it, which both gates did again in this
  record's checks. It stands for the same reason, and the class outlives the criterion — any
  letter-suffixed criterion anywhere in this spec is dropped the same silent way.
