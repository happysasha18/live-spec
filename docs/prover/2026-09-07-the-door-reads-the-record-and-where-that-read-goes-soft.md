# Prover record — 2026-09-07 the door reads the record, and where that read goes soft

PUSH-REVIEW

Prover skill version: product-prover 1.6.2, installed under `skills/product-prover/`, read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 and `skills/live-spec-base/SKILL.md` v6.1.0.
Lens-set digests: `SKILL.md` 5d98c4309c91, `reference/stress-lenses.md` 422e3b9a43a9. The pass was
run by a fresh seat that authored none of this change, briefed to find reasons to refuse it and to
hold it defective until evidence said otherwise. Mode: feature-fit review, scoped to Requirement
321 and its fit against the document it entered.

Range: 186dc4a..18f41e1, one commit reviewed.

- 18f41e17 Admission reads the record before it writes a row — Requirement 321 added to
  `spec/queue-intake-priority.md` under INV-327 with criteria 1 to 8 plus a criterion 6a; matrix
  rows M-651 to M-656; `record_rows`, `resolve_ref`, `read_prior_record`, `read_supersedes` and
  `prior` added to `scripts/task-admission.py`, with three refusals wired into `admit`

Read with that commit, as the record's own shape requires: the uncommitted repairs to
`spec/queue-intake-priority.md`, `scripts/task-admission.py` and `tests/test_task_admission.py`
that close F3 and F8 below. This record was written against the commit, then re-run over those
repairs and updated in place.

Files read: `spec/queue-intake-priority.md` (Requirement 321 whole, Requirement 5, Requirement 43,
Requirement 92, Requirement 93, Requirement 94), `scripts/task-admission.py`
(`record_rows`, `resolve_ref`, `read_prior_record`, `read_supersedes`, `render_task`,
`_read_paragraph`, `admit`, `prior`, `main`), `tests/test_task_admission.py` (the six M-65x tests
and the `host` and `new_route` fixtures), `matrix/build-pipeline.md` rows M-651 to M-656,
`PRODUCT_SPEC.index.md`, `TEST_MATRIX.index.md`, `guardrails/specformat.py`,
`guardrails/check-prover-record.sh`, `docs/prover/README.md`, `scripts/plan_checks.py` (the q-825
key), `skills/build-pipeline/references/accepted-work-execution.md`, and the two records dated
today under `docs/prover/`.

Checks run: the six matrix tests, the two spec-format gates over the whole document, the row's own
acceptance command, and four read-only probes against the shipped code in throwaway trees. Each
with its result below. The full suite was not run; this pass is a document review scoped to one
requirement, and the suite's own green for this range is the pushing session's to record.

```
$ python3 -m pytest -q tests/test_task_admission.py -k "m651 or m652 or m653 or m654 or m655 or m656"
6 passed, 62 deselected in 0.23s
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

```
$ bash -o pipefail -c "<the q-825 acceptance key>"
(exit 0)
```

Re-run after the F3 and F8 repairs landed in the working tree:

```
$ python3 -m pytest -q tests/test_task_admission.py
69 passed in 4.41s
(exit 0)
```

```
$ python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md
OK — all 1829 criteria well-shaped across 315 requirements
(exit 0)
```

Probe 1, the parser's own reading of Requirement 321:

```
$ python3 -c "import specformat as sf; ... [c.number for c in r321.criteria]"
criteria: [1, 2, 3, 4, 5, 6, 7, 8]
```

Probe 2 and 3, `admit` run against two acceptance keys in a throwaway tree:

```
key 'python3 -m unittest -q tests.test_all'   -> admitted: q-1 written, checkpoint written
key 'grep -q pytest tests/conftest.py'        -> refused: "runs a test suite"
```

Probe 4, `admit` against the title of a far row in a throwaway tree:

```
refused: q-9 already carries this title (PLAN.md). Saying it again is admitted only against a
supersedes record naming that row, what is new in this request, and why the decision already on
record does not cover it
```

Findings: ten, of which three blocked. Two of the three are repaired in this range and one stands. The change moves the door from reading nothing to reading the
plan and the archive, and that part holds. The findings below are the distance between what
Requirement 321 says and what the door does.

F1 — Criterion 6a is invisible to every gate that reads a criterion.

> "6a. The system *shall* refuse at the door an acceptance command that runs a test suite" —
> `spec/queue-intake-priority.md`, Requirement 321, Case: the check a row is admitted against can
> actually run

`guardrails/specformat.py:75` matches a criterion as `^(\s*)(\d+)\.\s+`. The token `6a.` carries a
letter between the digit and the dot, so it matches nothing. Probe 1 above shows the parser reading
Requirement 321 as eight criteria. `PRODUCT_SPEC.index.md:379` maps INV-327 to R321.1 through
R321.8 and names no 6a, and the index gate calls that a correct build. `check-requirement-shape.py`
counts 1829 criteria across the document and 6a is in none of them. An author who edits 6a, or
deletes it, moves nothing any gate can see. A later reader who works off the index believes
Requirement 321 has eight criteria. This is a class rather than one spot: any criterion anywhere in
this spec numbered with a letter suffix is dropped the same way, silently.

Renumber 6a as criterion 9 and move it after criterion 8, where document order and criterion order
agree. Then make the drop loud rather than silent: `check-requirement-shape.py` should red on a
line under a requirement that opens with a digit, a letter and a dot, since that shape is a
criterion somebody wrote and no gate will read.

`defect · missing-outcome-check (postcondition)`

F2 — Criterion 6a holds a class and the mechanism is a one-item list of a runner's name.

> "the system *shall* refuse at the door an acceptance command that runs a test suite, since the
> session-start probe runs every recorded check" — Requirement 321 criterion 6a

`scripts/task-admission.py:754` reads `if "pytest" in key`. Probes 2 and 3 above were run against
that code. A key reading `python3 -m unittest -q tests.test_all` runs a whole suite and is
admitted: the row is written and the checkpoint with it. A key reading
`grep -q pytest tests/conftest.py` runs no suite and costs milliseconds, and it is refused. The
refusal's own message tells the author to "run them through a single named unittest case", which is
the spelling the substring does not catch, so the door forbids one name and recommends another name
for the same act. The thing the criterion is trying to hold is a cost the session-start probe
cannot afford. A runner's name is not that cost, and base rule 39 is explicit that a list is the
wrong answer to a class.

Judge the key by what it runs. Two roads: (a) measure the recorded command once at admission and
refuse a key past a stated budget; (b) refuse a key that invokes a runner with no target — no test
file, no test function, no named case. I prefer (b). It is static, it needs no clock and no
threshold nobody agreed on, and it separates `python3 -m pytest -q` from
`python3 -m pytest tests/x.py::test_y` on what the command actually does. Recorded for the class:
the owner has said criterion 6a comes out in separate work tonight, and the class outlives the
criterion, because the next check that has to be cheap will be spelled some other way.

`defect · over-specific (abstraction)`

F3 — REPAIRED. Criterion 1 claimed four reads by the system, and the door made two.

The criterion said the system "shall read the record — the live plan's rows, the queue archive's
rows, the decision record, and the commit log". `admit` read the plan and the archive through
`record_rows`. `DECISIONS.md` and `git log` opened only inside `resolve_ref`, and only where the
route already named a reference of that shape, and `read_prior_record` accepts an empty reference
list on purpose. So two of the four named sources went unread on a legal route, and
`new_route()` in `tests/test_task_admission.py:54` ships exactly that route.

Repaired in `spec/queue-intake-priority.md`. Criterion 1 now reads: "*when* new work is admitted,
the system *shall* read the live plan's rows and the queue archive's rows, and *shall* resolve any
decision-record or commit-log reference the route names, before the row is written." The Context
paragraph and the User Story were corrected with it: the Context now says the door reads the plan
and the archive directly and the route carries what it read elsewhere, and the User Story says
admission checks against the record.

Re-read against the code: the new sentence holds. `admit` calls `record_rows`, which reads
`PLAN.md` and `docs/queue-archive/*.md`. `read_prior_record` passes every named reference through
`resolve_ref`, which resolves a commit against the tree and a date against `DECISIONS.md`. Both run
before any write, since every refusal raises ahead of `checkpoint.write_atomic`. The criterion now
names less than the code does — `resolve_ref` also resolves a row id — and understating is not the
failure this finding was about. No overstatement survives in criterion 1.

One residue in the Context, and it belongs to F4 rather than here. "the route carries what it read
elsewhere — the decision record, the commit log" still reads as a guarantee, and an empty reference
list is legal, so a route can carry nothing from either. F4 stands and names that hole. The claim
that the SYSTEM performs those two reads is gone, which is what this finding was.

`defect · unenforceable-promise (discharge)` — closed in this range.

F4 — The one mandatory field of the read is the one nothing can check, and the field with teeth is
optional.

> "the system *shall* carry that read on the route as the references consulted and the finding they
> produced" — Requirement 321 criterion 2

`read_prior_record` refuses an empty `finding` and accepts an empty `read`. Every reference named is
resolved, so a fabricated id is caught; a fabricated finding is not, and cannot be. The cheapest
legal admission is therefore one arbitrary sentence and no citation at all. That inverts the
pressure the requirement is trying to apply: it costs work to cite and none to assert, so the door
rewards asserting.

Require a resolving reference exactly where the record has something to cite: run the row's own
title words through `prior` at admission, and where it prints any hit, refuse a `read` list that is
empty. That uses the command criterion 6 already builds, it demands nothing on a genuinely new
area, and it closes the road the fixture currently takes. Where that is judged too strong, say in
the criterion that the finding is unverified evidence for the next reader, so nobody reads it as a
guarantee.

`defect · unenforceable-promise (discharge)`

F5 — The requirement's story promises intent and the mechanism delivers string equality.

> "so that finished work stays finished and a settled decision stays settled without me holding it
> all in my head" — Requirement 321, User Story

`admit` compares `" ".join(route["title"].lower().split())` against the same normalization of every
row header. Case and runs of whitespace fold, and nothing else. "Send the weekly digest" and "Send
weekly digests" are two different rows to this door. Criterion 4's own sentence — "the title stands
on the record already" — describes the mechanism accurately. The Context paragraph and the User
Story around it describe something larger, and a reader takes their promise from those.

Rewrite the Context and the User Story to say what the door catches: a title already standing on the
record. Then name the widening as out of scope with its reason, in the same sentence. Do not reach
for a similarity score: criterion 6 refuses one by name, and the two clauses would then contradict
inside one requirement.

`defect · over-general (abstraction)`

F6 — Criterion 4 says the refusal names the file the row stands in, and never says which file when
it stands in two.

> "the system *shall* refuse the admission and *shall* name the row and the file it stands in" —
> Requirement 321 criterion 4

Measured on this repository: `record_rows` yields 176 unique rows from `docs/queue-archive/` and 82
from `PLAN.md`, and 72 rows stand in both. `record_rows` dedupes on `(title, id)` and yields the
first file it read, and it reads `PLAN.md` before the archive. So for those 72 rows the refusal
names `PLAN.md`, which carries the stub, and never the archive file, which carries the full record.
Three of them are q-527, q-570 and q-584, each on `PLAN.md` and in
`docs/queue-archive/2026-09-04-closed-rows.md`. The Context says the archive read exists because a
closed row's full record had rotated there and was invisible. For 72 of 176 archived rows the
refusal still points away from it.

Have the refusal name every home the matched row stands in, archive first, and say in the criterion
that a row standing in two homes is named in both.

`defect · missing-scenario (state-space)`

F7 — Requirement 321 leaves the seam with Requirement 5 criteria 3 and 4 blank, and its refusal
message sends the reader down the wrong road.

> "the system *shall* keep a far row in the queue's body with no revisit trigger and no plan to run,
> so a thought worth keeping is not discarded." — Requirement 5 criterion 4

`record_rows` reads every `### <mark> <title> — id:` header on `PLAN.md`, whatever the mark, so a
far row's title and a deferred row's title are both on the record. Probe 4 above admits the title of
a far row and gets the refusal in full: the only road out it names is a supersedes record saying
"why the decision already on record does not cover it". No decision was ever taken on a far row.
Requirement 92 and Requirement 93 already own the right route, which is to resume the row that
exists. Requirement 321 names two outcomes, refuse and admit-with-supersedes, and never the third.
A person who follows the message writes a supersedes record about a decision nobody made, ends up
with a duplicate row, and leaves the far row parked beside it forever. This is the case the
requirement most needed an answer for, since a far row is a thought the person intends to come back
to.

Add a criterion for a matched row that is still live rather than terminally closed: the door names
the row, states its tier, and routes to the resume path of Requirements 92 and 93. Make the refusal
message say which of the two roads applies, read off the matched row's mark.

`defect · undefined-path (transitions)`

F8 — PARTLY REPAIRED. Criterion 5's lift takes three fields and judges one; the scan that read
them stopped early, and that half is closed.

> "the system *shall* lift that refusal only against a written record naming the row superseded,
> what is new in this request, and why the decision already on record does not cover it" —
> Requirement 321 criterion 5

The half that is repaired: `admit` used to `break` out of the duplicate scan on the first row the
supersedes record named, so where one title stood on two rows, superseding one admitted the row
past the other without ever looking at it. `scripts/task-admission.py` now reads `continue` in that
branch, with the reason in a comment beside it, so the loop runs to the end of `record_rows` and a
second colliding row the supersedes does not name still refuses. Held by
`test_m654_a_second_colliding_row_still_refuses_when_supersedes_names_only_the_first`, which plants
q-31 and q-77 under the same title, supersedes q-31 alone, and asserts the refusal names q-77 and
its archive file and that no row is written. Verified here: `python3 -m pytest -q
tests/test_task_admission.py` reads 69 passed, exit 0.

The half that stands: `read_supersedes` requires `names`, `new` and `why` to be non-empty after
stripping, and resolves `names` alone. One character in `new` and one in `why` still lift the
strongest refusal this door has. The three-field shape reads as a substantive bar and is a
presence bar.

Say in the criterion that the door checks the record is present and complete, and that judging its
content is the reader's. The multi-row case the criterion never stated now has an answer in the
code; state it in the criterion too, since a reader of the spec still cannot tell what happens
when a title matches more than one row.

`defect · missing-prerequisite (precondition)` — the early-exit half closed in this range; the
presence-bar half stands.

F9 — Criteria 7 and 8 have no mechanical check, no matrix row, and one grep standing behind them.

> "the system *shall* ask one plain question and wait for the answer" — Requirement 321 criterion 7

M-651 to M-656 cover criteria 2, 3, 4, 5, 6 and 6a. Nothing covers 7 or 8. The only thing in the
tree that touches them is one clause of q-825's acceptance key:
`grep -q 'One case waits for the answer' skills/build-pipeline/references/accepted-work-execution.md`.
That holds that a sentence exists in a skill file. It holds nothing about any pipeline ever asking a
question or ever stating a conflict, so it is a gate anchored on prose and it passes whatever the
pipeline does. Two of the nine criteria are unbacked, and INV-327's row in `TEST_MATRIX.index.md`
gives no sign of it.

Mark criteria 7 and 8 in the requirement as seat discipline that no gate holds, with the reason.
Requirement 93 criterion 3 already does exactly this for its own resume read, so the spec has the
shape and the precedent. That is honest and costs nothing; leaving them as they stand lets INV-327
read as fully backed.

`recommendation · now · hard-to-monitor (observability)`

F10 — Criterion 6 says every row, and `prior` searches a row's title.

> "the system *shall* print, on one command, every row, decision line and commit subject carrying
> all the words given" — Requirement 321 criterion 6

`prior` builds one line per row as `id  title  (file)` out of `record_rows`, and matches the
caller's words against that line. A row whose title lacks a word and whose body carries it is never
printed, and a row's body is where its reasoning lives. For `DECISIONS.md` and for the log the
command does match whole lines and whole subjects, so the narrowing is on rows alone.

Either search the row's whole block, or say in the criterion that the row's title is what is
matched. I prefer saying it: the title is a deliberate, cheap filter, and a reader who knows that
picks different words.

`recommendation · now · over-general (abstraction)`

Criterion 6, the promise it makes about scoring: held. `prior` filters on all-words-present without
case, prints every hit, and applies no ranking, no limit and no threshold. It reports a count per
heading and then the lines. There is no score and no cutoff anywhere in it.

Composition against Requirement 43: no contradiction and no duplication. R43's three-source impact
read and R321's record read run at the same intake moment, produce different fields, and neither
writes the other's. One gap sits beside them: R43 criterion 2 says the footprint is written in the
row's footprint note, and `render_task` writes no footprint note — `PLAN.md` carries none, on any
row. That is Requirement 43's gap and predates this change, so it is a tracked follow-up under the
scoped-review rule rather than a block on this range.

Composition against Requirement 5 criterion 1: no contradiction. R5.1 puts a terminally-closed row
in the queue archive verbatim and grepable, and R321.4 depends on that home existing. The gap is
with R5 criteria 3 and 4, and it is F7 above.

Spec and architecture re-check: `PRODUCT_SPEC.md` itself is unchanged in this range; the delta lands
in `spec/queue-intake-priority.md`, which the freshness arm reads as part of the same document.
`ARCHITECTURE.md` is unchanged; `architecture/pipeline-and-lanes.md` gained the INV-327 line and the
pin at `scripts/task-admission.py:36`, and that pin resolves to the record-reading block.

Blocking: three, of which two stand and one is closed in this range. This pass reports and does not
repair; F3 was repaired by the session that owns the spec, and this record was re-run over it.
- F1 stands: criterion 6a is invisible to `specformat.py`, so the index, the shape gate and every
  criterion-reading check skip it. It stands because the owner has separate work queued tonight that
  removes criterion 6a, and the renumbering would collide with it. The class outlives that removal:
  the letter-suffix criterion is dropped silently anywhere in this spec, and that repair is owed
  whether or not 6a survives.
- F2 stands: `if "pytest" in key` admits `python3 -m unittest -q tests.test_all`, which runs a whole
  suite, and refuses `grep -q pytest tests/conftest.py`, which runs none. Both proved against the
  shipped code. It stands for the same reason: the criterion is being removed tonight in work this
  review does not touch. The finding is filed for the class, so the next cheap-check rule is not
  written as a name match.
- F3 closed: criterion 1 now names the two reads the door performs and the resolution it runs over
  what the route names, and the Context and the User Story were corrected with it. The defect: the
  criterion claimed the system read the decision record and the commit log, and a legal route left
  both unopened. Re-read against `admit` and `resolve_ref`, and the sentence now holds.
