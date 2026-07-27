# Prover record — the FOLD of the 2026-07-27 push-gate addendum (A1–A9 and N1, and what the fold uncovered), 2026-07-27

**This record reviews the fold.** The day's first record is `docs/prover/2026-07-27-push-gate.md`
(CROSS-LINK with the architecture lens over `d7400d8..6b11c7e`, findings F1–F8). The second is
`docs/prover/2026-07-27-push-gate-addendum.md`, which held the push on nine findings A1–A9 plus one note
N1. This third record reads the fold of those ten items and what folding them uncovered. It stands on top
of the first two rather than replacing them, and it does not re-argue what they covered.

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK with the architecture lens, delta
scoped. Reviewed by a seat that authored none of the work (SPEC INV-237).

## Scope

**What this record reviews.** Everything uncommitted in the working tree at HEAD `b5ebe02`, read through
`git diff` and `git status`, including the untracked fixture directories
`guardrails/hook-red-fixtures/clock-hook/` and `guardrails/hook-red-fixtures/chat-law-hook/`.

**What this record was asked to skip.** The files of a separate movement still under construction:
`hooks/midturn-chat-scan.py`, `hooks/chat-calques.json`, `tests/test_midturn_chat_scan.py`, and the
fixture directory `guardrails/hook-red-fixtures/midturn-chat-scan/`.

**The skip does not hold, and that is a finding of its own (M2).** That movement has written itself into
seven files this record must read: `guardrails/judge-hooks.json`, `guardrails/hook-red-proofs.json`,
`scripts/install-pack-hooks.sh`, `hooks/code-anchor-scan.py`, `ARCHITECTURE.md`, `PRODUCT_SPEC.md` and
`ROADMAP.md`. Two of the fold's own machine counts are true only while that movement's registry entry
stands. So the verdict below is a verdict on the combined tree, because the combined tree is the only
thing that exists.

**The tree moved while this record was written.** `guardrails/check-hooks-can-fire.py` changed at 14:39,
`tests/test_check_hooks_can_fire.py` at 14:40, `ARCHITECTURE.md` and `PRODUCT_SPEC.md` again after 15:00.
A test that failed at 14:36 passed at 14:44 because its asserted literal was edited underneath the run.
Every claim below is pinned to the tree **as of 15:03**, and the state at that moment is what the verdict
judges. The concurrent-edit fence (live-spec-base) exists for exactly this: a review record is only worth
what the state it read is worth, so the timestamp is load-bearing here.

## Verdict

**HOLD — the push does not go on the reviewed state.** Three must-fix defects, nine should-fix. One of
the three is decisive on its own: the full suite is red.

The fold is real work and most of it is right. Nine of the ten items fold in substance, verified against
the files, the runs, and the machines rather than against the claim. The census A1 asked for exists, has
a stated population and a stated carve-out, and reds three ways it could not red before; I confirmed by
running it against a registry with an entry removed and watching it name the hook. A4's net found seven
further rows nobody had asked it to find, which is what a net is for. A2, A3, A7, A8, A9 and N1 fold
cleanly. What holds the push is not the fold's substance. It is that the tree the push would carry does
not pass its own gates, that the delta cannot be committed apart from a movement this review was told to
skip, and that A4's headline claim — one home for the terminal vocabulary — is written in one document
while four surfaces state three different lists.

| # | Kind / severity | Claim / evidence | Status |
|---|---|---|---|
| M1 | defect / must-fix | The full suite is red on the tree the push would carry: three failures at 15:03, one of them in a file the fold claims as its own | OPEN |
| M2 | defect / must-fix | The delta cannot be pushed on its own: its new census test pins a literal count that is true only while the skipped movement's registry entry stands | OPEN |
| M3 | defect / must-fix | A4 claims one home for the terminal vocabulary; four surfaces state three different lists, and the two machines pointed at that home read different ones | OPEN |
| S1 | defect / should-fix | The census reds a third way (a wired name with no file at all) that no criterion states and no test covers | OPEN |
| S2 | defect / should-fix | Three stand-down criteria A9 added ship with no test, and M-460 names one of them as a covered fact | OPEN |
| S3 | defect / should-fix | R292.8 says "either map"; only the `cannot_red` arm is tested | OPEN |
| S4 | defect / should-fix | R293.8 says "every code form" where the machine holds two of the four forms to the capital shape | OPEN |
| S5 | recommendation / should-fix | The runner's failure line names one cause for four different red paths | OPEN |
| S6 | defect / should-fix | Row 489's cell says "all seven fire" beside the sentence this fold just wrote into it; the runner proves ten | OPEN |
| S7 | defect / should-fix | M-390's fact cell gained the fourth fixture; no matrix cell names the six tests that hold it, and R243.5 has no matrix row | OPEN |
| S8 | recommendation / should-fix | The archive Status cell is read by field index, defended by an empirical claim about rows read so far | OPEN |
| S9 | recommendation / should-fix | The shared reader's consumer count has no net; it moved from three to five to six inside one day, each time by hand | OPEN |

---

## M1 — The suite is red on the tree the push would carry

> "8 failed, 1920 passed in 505.27s" — full-suite run, 14:47, log at `runs/full-suite.log`

I ran the whole suite rather than the three files the brief named. Eight failed. Five of the eight have since
gone green as the tree moved (two were the installed copies under `~/.claude/hooks` lagging the repo, one
was a mid-edit size ratchet, one was a status-cell correction that tripped the delegation-line law and was
patched, one was a cascade of the others). Three are live at 15:03 and I re-ran them myself:

> "AssertionError: 1 not less than or equal to 0 : ARCHITECTURE.md re-grew redundancy: 1 open pairs (floor 0)" — `tests/test_convergence_locks.py::TestConvergenceLocks::test_live_spec_sits_at_the_clean_floor`

> "hooks/code-anchor-scan.py:124 [cyrillic] The fragment is the matched code itself — …" — `bash guardrails/check-shipped-language.sh`, offences 2

> "check-no-history: 1 history/provenance marker(s) … line 6780 carries a date marker (2026-07-27)" — `tests/test_no_history.py::TestArmedOnTheRealSpec::test_armed_passes_on_the_real_spec`

`ARCHITECTURE.md` at HEAD reports `{"open":0}`; the worktree reports `{"open":1}`, the pair being lines
148 and 152, both restating that a scan installs by the setup walk beside the scissors scan and is covered
by config-health parity. The Cyrillic offence at `hooks/code-anchor-scan.py:124` sits in the docstring the
fold's own A6 file gained, and the neighbouring offence sits in `guardrails/hook-red-proofs.json`, another
file the fold claims. The no-history marker sits in a spec Context block added after 15:00.

Re-checked at 15:07, while this record was being written: the no-history marker had been fixed and two of
the three remained red — `ARCHITECTURE.md` still at `{"open":1}` against a floor of 0, and the
shipped-language gate still at two offences. The finding stands on the state at 15:03 and this re-check
says which parts of it were still true four minutes later.

The pack gates a commit on a green suite log rather than on an exit code. A seat that ran only the three
files the brief named would have read three green files and pushed a red tree.

Re-run the full suite and land it green before the push. Two of the three reds are one sentence each: move
the dated incident out of the spec Context block into `JOURNAL.md`, and mark or de-Cyrillicize the two
docstring samples the way the file's existing `# user-language:` markers already do.

`defect · unenforceable-promise (discharge)`

## M2 — The delta cannot be pushed apart from the movement this review was told to skip

> "assert \"census 10/10 wired hook(s) classified\" in proc.stdout" — `tests/test_check_hooks_can_fire.py:114`

The census test pins the count as a literal string. Ten is the wired-hook count only while
`guardrails/judge-hooks.json` carries `"midturn-chat-scan": "PreToolUse"`, which belongs to the movement
this record was told to skip. I checked what the delta alone would do: I copied both registries, removed
that entry and the paired `chat-calques` library line, and ran the runner against the copies. It printed
`census 9/9 wired hook(s) classified` and exited 0. So committing A1–A9 without the movement reds the
delta's own new test, and committing them together ships a hook that has a wired registry entry, a line in
`scripts/install-pack-hooks.sh` that installs it into every adopting host, a red-proof entry and a
fixture, while its requirement and matrix row were still being written at 15:00.

The entanglement is not only the count. `hooks/code-anchor-scan.py`'s split of `find_hits` into
`find_matches` exists to serve that movement and says so in its own docstring — "hooks/midturn-chat-scan.py
is that caller" — inside the file the fold claims as A6. `scripts/install-pack-hooks.sh` is modified
entirely for that movement and appears in no claim in the fold at all.

I read this the way the false-independence lens reads a concurrency plan: two movements that rewrite the
same clauses in the same files are not independent, and opening them in parallel on one tree is the
finding. The shared living documents are a convergence point; `guardrails/judge-hooks.json`,
`hook-red-proofs.json` and `hooks/code-anchor-scan.py` are not — they are one behaviour's rules, rewritten
by both.

Either finish the movement and review it, so one push carries both with the count honest, or take its six
insertions out of the four shared files and push the fold alone. Replace the literal `10/10` with a count
read from `judge-hooks.json` itself either way (see S9): the assertion should be that every wired hook is
classified, and the number is the machine's business.

`defect · boundary-issue (composition)`

## M3 — The terminal vocabulary has one claimed home and four surfaces stating three different lists

> "Those four words are the whole terminal vocabulary, and this sentence is their one home … the rotation gate reads this list, and `scripts/rotate-doc.py` reads it as its closed signals" — `docs/roadmap-format.md`, the live-body law

That sentence makes two checkable claims about shipped code. One holds and one does not.

`guardrails/check-doc-rotation.py`'s `TERMINAL_WORD_RE` reads `landed|decided|declined|superseded` — four,
matching. `scripts/rotate-doc.py`'s `CLOSED_SIGNALS` reads `("landed", "decided", "declined",
"superseded", "met")` — five. The two machines the sentence points at do not read the same list. A row
whose status headline carries `met` is treated as closed by `rotate-doc.py`, moved into an archive, and
then named as a violation by `check-doc-rotation.py`, which holds no such word. The author is left with a
row one machine put where the other machine forbids.

Two further surfaces state three words where four are legal. The gate's own docstring, describing the
violation it just gained:

> "a row inside a `rotated-*.md` archive file whose Status cell carries none of the terminal words the archive's own preamble names: landed, declined, superseded" — `guardrails/check-doc-rotation.py`, the header comment

And the message an author actually reads when the gate reds:

> "holding none of landed / declined / superseded — a non-terminal row belongs in the live queue body" — `guardrails/check-doc-rotation.py`, the violation string

The archive preamble the docstring defers to says the same three. So the docstring names the archive
preamble as the vocabulary's home while `docs/roadmap-format.md` says the home is itself — two homes for
one fact, which is the condition A4 set out to end. The operational consequence is small but real and
lands on a person: an author whose decision row reds is told by the machine to pick one of three words,
none of which is `decided`, and the honest fix is to write the word the message omits.

Point both machines at one list in one place. The cheapest shape that actually discharges the one-home
claim: put the four words in `guardrails.config.json` or a tiny shared module, have
`check-doc-rotation.py` and `rotate-doc.py` both read it, and settle `met` by name — either it is a fifth
terminal word and `docs/roadmap-format.md` and R243.5 say so, or it comes out of `CLOSED_SIGNALS`. Then
rewrite the gate's docstring, its violation message and the archive preamble off that one list.

`defect · internal-conflict (consistency)`

## S1 — The census reds a third way that no criterion states and no test covers

> "check-hooks-can-fire: UNRESOLVED %s — wired live in judge-hooks.json's \"wired\" list but no .py or .sh file found under %s or %s" — `guardrails/check-hooks-can-fire.py`, `run_census`

R292.6 covers a wired hook classified in neither map. R292.8 covers an entry in either map naming a file
found under neither directory. The runner reds a third case neither criterion reaches: a name in the wired
list with no file at all, under either extension. `grep -rn UNRESOLVED tests/ TEST_MATRIX.md
PRODUCT_SPEC.md` returns only unrelated hits in `tests/test_legibility_floor.py`, so no test holds it
either.

This is the same class A5 and A9 just closed for the other two hooks: behaviour that ships with no
criterion. It matters more here than usual, because the case it catches is a registry naming a hook that
was renamed or deleted — the drift the census was built to notice.

Add a criterion to R292's "the registry names files that exist" case for a wired name that resolves to no
file, and a test that seeds a temporary `judge-hooks.json` wiring a name with no file and asserts the
runner names it. The existing `test_runner_reds_on_wired_hook_absent_from_both_maps` is one line away from
being that test.

`defect · missing-outcome-check (postcondition)`

## S2 — Three stand-down criteria ship with no test, and the matrix claims one of them

> "never reds when the stop hook is already active or when the turn's record cannot be read" — TEST_MATRIX.md, M-460's fact cell

A9's fold added four stand-down criteria. Three of them have no test anywhere:

- R293.10 (the code-anchor scan stands down when the stop hook is already active). `tests/test_code_anchor_scan.py` passes `"stop_hook_active": False` on every payload it builds and never sets it True.
- R293.11 (the same scan stands down on an unreadable payload or turn record). The hook's `except ValueError: sys.exit(0)` and its two later guards are reached by nothing.
- R294.7 (the empty-validation scan stands down on an unreadable payload or turn record). `tests/test_affirmation_arm.py` has no such case.

R294.6 is the exception and is properly held by `test_stop_hook_active_stands_down`.

M-460 claims the unreadable-record stand-down as a covered fact. A matrix row is the pack's own promise
that a fact is held by a test; here the promise is written and the test is absent, which is the state a
matrix exists to make impossible. A9's own reasoning is what makes this bite: it argued that the
stand-down is load-bearing precisely because an unreadable transcript looks exactly like a clean turn. A
stand-down that silently stops standing down is invisible by construction, so a test is the only thing
that would ever notice.

Write three tests, one per criterion: a payload with `stop_hook_active: True` on the code-anchor scan, a
payload that is not JSON, and a payload whose `transcript_path` points nowhere. `tests/test_midturn_chat_scan.py`
already carries `test_unreadable_payload_stands_down` and `test_missing_transcript_stands_down` and is the
shape to copy.

`defect · missing-outcome-check (postcondition)`

## S3 — R292.8 says "either map"; one arm is tested

> "*if* an entry in either map names a hook found under neither the pack's own directory nor the installed one, *then* the system *shall* red it by name" — PRODUCT_SPEC.md, R292.8

Both arms are built: the `proofs` loop reds through `resolve_hook_path` returning None, and the new
`cannot_red` loop reds the same way. Only the second is tested —
`test_runner_reds_on_a_cannot_red_entry_naming_a_missing_file` seeds `cannot_red` alone, though its
docstring speaks of "a proofs/cannot_red key". The `proofs` arm is the older code path and is the one more
likely to be touched, since it sits inside the loop that grew a new detect mode in this same delta.

Add the mirror case: a `proofs` entry naming a hook file that exists nowhere, asserted red by name.

`defect · missing-outcome-check (postcondition)`

## S4 — A criterion claims a rule over every code form; the machine holds two of four

> "shall hold every code form to the capital shape the documents write it in, so an ordinary word carrying a letter and a number in lower case passes" — PRODUCT_SPEC.md, R293.8

The hook splits its patterns into two lists. `CASE_SENSITIVE_PATTERNS` holds the multi-letter codes
(`INV|ROW|ACT`) and the single-letter dash codes to upper case. `CASE_INSENSITIVE_PATTERNS` keeps the
working-language naming word and the document-name form matching either case, and the hook says so in its
own comment: "the working-language naming word and the document-name form match either case". R293.7 calls
the document-name form a code. So "every code form" is false for two of the four forms the requirement
itself enumerates.

Nothing misbehaves — a lower-case `roadmap 480` is no ordinary English word, so the wider match costs
nothing today. What costs something is the next reader who takes R293.8 at its word and reports a bug when
`roadmap 480` reds in lower case, or the next author who narrows the pattern to match the criterion.

Scope the criterion to what the machine does: the internal-code forms are held to the capital shape, and
the naming word and the document name are read in either case because neither has a lower-case ordinary
reading.

`defect · over-general (abstraction)`

## S5 — One failure line for four different causes

> "check-hooks-can-fire: FAIL — at least one hook stayed silent against its own fixture." — `guardrails/check-hooks-can-fire.py`, `main`

The runner now reds four ways: a hook that stayed silent, a wired hook classified in neither map, a wired
name that resolves to no file, and a map entry naming a missing file. The closing line names only the
first. An operator who reads the last line of a red run goes looking for a silent hook, and on three of the
four paths there is no silent hook to find. The per-line messages above it are good and specific; only the
summary misdirects.

Make the closing line name the counts it actually saw, or state the general case: at least one hook failed
its proof or its census.

`recommendation · hard-to-monitor (observability)`

## S6 — The row this fold edited still says seven where the runner proves ten

> "all seven fire, and the collector half is declared unprovable this way with its reason. The run rides the full suite, which is the gate every release passes …" — ROADMAP.md, row 489's acceptance cell

N1's fold added the second sentence and left the first standing. The runner today prints "10 hook(s) to
prove, 1 classified cannot_red" and "census 10/10". Seven was true when the row was written and is not
true beside the sentence just added to the same cell. This is the count-drift class the pack knows well:
the count and the thing counted live in two places, and only one of them was read at edit time.

Drop the number. "Every classified hook fires, and the collector half is declared unprovable this way with
its reason" says the same thing and never goes stale.

`defect · internal-conflict (consistency)`

## S7 — The matrix's fourth fixture names no test, and R243.5 has no row

> "reds four fixtures … and a row inside an archive whose status carries no terminal word … reds by name" — TEST_MATRIX.md, M-390's fact cell

M-390's fact cell was widened from three fixtures to four. Its owning-test cell was not touched. The six
tests do exist — `tests/test_doc_rotation.py::TestNonTerminalArchiveRow` holds the queued-row red and four
terminal-word passes plus the stale-opener case — and they run green. Nothing names them:
`grep -n "queued_row_in_the_archive\|terminal_word_" TEST_MATRIX.md` returns nothing across the whole
matrix. R243.5, the criterion the arm was written for, appears in no matrix row at all.

The tests being real is what keeps this a should-fix. The matrix is the pack's map from a stated fact to
the test that holds it, and a fact whose row points at the wrong tests sends the next reader looking in the
wrong file, which is precisely the cost the map exists to remove.

Add the six test names to M-390's owning-test cell and give R243.5 its matrix row. Worth checking the same
cell for the two older classes it already omits (`TestMonthlyClosingCommitGate`, `TestClosingCommitMechanism`),
which predate this delta and are the same omission.

`defect · hard-to-operate (ops-ux)`

## S8 — The Status cell is read by field index, defended by a count of rows read so far

> "A row's free-form prose occasionally holds a stray literal `|` of its own, ahead of or inside the Status text; the fourth field then opens on the Status cell's own text either way, which is where its stated word stands in every row read so far." — `guardrails/check-doc-rotation.py`, `_non_terminal_rows`

`_non_terminal_rows` splits the line on `|` and takes field 3 as the Status. The docstring is honest that
rows carry stray pipes, and then rests the correctness of the read on an observation about the rows that
happen to exist today. A stray pipe standing before the Status cell shifts the read one field left onto the
Class cell, and a Class cell holds none of the four terminal words, so the gate would name a properly
closed row as a violation. A stray pipe inside a long status could equally hand the check a fragment that
happens to contain "landed" and pass a row that should red.

Both archives in the glob share the same five-column header today, so the shape holds as written. The
defence is empirical rather than structural, which is what makes it worth naming now, while the gate is new
and the archives are small.

Read the Status cell by locating the header row's `Status` column index per file rather than by a fixed
number, or split on a delimiter the prose cannot contain. Either removes the standing assumption.

`recommendation · missing-prerequisite (precondition)`

## S9 — The shared reader's consumer count has no net

> "the shared full-turn reader six checks read through, each reading every assistant message shown since the last human turn: the contrast-frame scan, the hedge scan, the register judge, the code-anchor scan, the empty-validation scan, and the tool-boundary scan" — ARCHITECTURE.md, the guardrails node's pins

A3 asked for three to become five, the fold wrote five, and by 15:03 the same clause read six because a
seventh party edited the same line. Each move was a hand edit against a `grep` somebody remembered to run.
`grep -ln turn_reader hooks/*.py` is the fact, and today it agrees with the document — six importers beside
`turn_reader.py` itself, with the answer-first arm correctly named as taking no part.

The count is right and has no keeper. When a seventh net imports the reader, nothing reds. This is the
same shape as the census literal in M2: a number written by hand beside a number a machine could read.

One small test, in the spirit of the existing pin-honesty checks: count the importers of `hooks/turn_reader.py`
and assert the architecture's clause names that many, each by name. That closes the count in both documents
at once and lets M2's fix drop the literal too.

`recommendation · hard-to-monitor (observability)`

---

## What is sound, verified against primary sources

Each item below was checked against the file, the run, or the machine, never against the fold's summary.

**The census exists and reds where it could not before.** `python3 guardrails/check-hooks-can-fire.py`
exits 0 and prints `census 10/10 wired hook(s) classified (library-list carve-outs excluded)`. I confirmed
the population is what the criteria now say by building temporary registries in the scratchpad: removing
the skipped movement's wired entry drops the run to `census 9/9`, still exit 0, and the runner's own tests
prove the three red directions — an unclassified wired hook named by name, a library-only name never
demanded, and a `cannot_red` entry naming a missing file.

**Both previously unproven hooks now fire for real.** `clock-hook.sh` fires with "Wall clock at this
prompt" and `chat-law-hook.sh` with "Answer first (live-spec)", each against a stub payload in the new
untracked fixture directories, each run as the real script with nothing mocked.

**The four gates the brief named all exit 0.** `check-hooks-can-fire.py`, `check-doc-rotation.py`,
`check-requirement-shape.py PRODUCT_SPEC.md`, `check-index-generated.py PRODUCT_SPEC.md
PRODUCT_SPEC.index.md`.

**The three test files the brief named pass at 15:03** — 58 tests. They did not pass at 14:36, when the
census literal read `9/9` against a runner printing `10/10`; the literal was edited at 14:40.

**A2's fold is complete in all four places.** R294.1 reads "any message the seat showed since the last
human turn", R294.5 states the reach and cites INV-281, the generated index row for INV-281 carries R294.5,
and M-460's fact cell carries the whole-turn reach with `test_affirmation_in_an_early_narration_line_reds`
holding it.

**A3's pin is honest against the tree.** `grep -ln turn_reader hooks/*.py` returns exactly the files the
clause names, with the answer-first arm correctly excluded.

**A4's net found more than it was asked to.** The new arm reds a non-terminal row inside an archive, and it
turned up seven rows past row 482. Rows 130, 420 and 468 in the current archive were corrected off their
own delivery reports, each carrying a dated note saying what was corrected and against what, with the
pre-conversion narration kept beside it. Row 482 closed whole.

**A6's case split is tested in the direction that matters.** `tests/test_code_anchor_scan.py` pins `act 3`,
`b-2`, `f-16` and `c-4` silent in lower case and red in upper, which is the false-positive direction the
addendum asked for.

**A7 folds.** Row 55's third acceptance leg reads OPEN with its reason, and the cell no longer denies
itself.

**A8 folds.** `source_fallback` is gone from the affirmation-scan entry, and the runner prints no fall-back
note for it, which is the deed the removed note contradicted.

**N1 folds.** Row 489's cell states the suite placement and keeps its still-owed list intact. The claim is
true: `tests/test_check_hooks_can_fire.py::test_runner_is_green_on_the_real_shipped_fixtures` runs the
runner, so it rides the suite.

**One correct change appears in no claim.** `hooks/clock-hook.sh`'s header comment said its repo home was
`scripts/clock-hook.sh`; the file lives under `hooks/` and the comment now says so. Small, right, and worth
naming so the next reader does not hunt for its row.

**A4's in-place archive correction has fan-out the fold met honestly.** Promoting row 420 to `**landed`
subjected it to the delegation-line law, which red the suite; the cell now records that no delegation was
recorded at the time, the row being corrected long after the work. That is the right answer, and it is
evidence for the general point: a status word is read by more laws than the one that prompted the edit.

---

## The five questions this record was asked

**1. Does each of A1–A9 and N1 actually fold, judged against the tree?**

Nine fold in substance. A1 folds with two gaps that are new findings rather than unfolded pieces (S1, and
the count literal in M2). A2, A3, A7, A8 and N1 fold cleanly, N1 with a stale count left beside its own new
sentence (S6). A5 folds with one criterion wider than its machine (S4). A6 folds, and the same file carries
one of the two offences reddening the shipped-language gate (M1). A9 folds — and the addendum's own A9
headline said "R292 and R293" while its body said "R293 and R294"; the body is right and the fold followed
the body, which is where the stand-downs belong. Three of A9's four criteria have no test (S2).

**A4 is the one that is folded in words while a neighbouring document disagrees.** Row 482 closed, the gate
arm built, the seven rows found and corrected — all real. The claim that did not fold is the headline one:
the terminal vocabulary does not have one home. `docs/roadmap-format.md` says four words and says both
machines read it; `check-doc-rotation.py` reads four but documents three in its comment and tells the author
three in its failure message; the archive preamble says three; `rotate-doc.py` reads five. That is M3.

**2. Do the new and re-worded criteria say what the code does?**

No criterion describes an unbuilt check. I read each new and re-worded criterion against the shipped code
line by line: R292.1 and R292.6 against `run_census`, R292.8 against both missing-file branches, R243.5
against `TERMINAL_WORD_RE` and `_non_terminal_rows`, R293.7/8/9 against the two pattern lists and
`_is_file_line_reference`, R293.10/11 and R294.6/7 against the guards in each hook's `main`, R294.1 and
R294.5 against the `turn_reader` call. All are built.

Shipped behaviour left with no criterion: the census's `UNRESOLVED` red (S1). One criterion states more
than its machine does (S4). The machines ran as recorded above; the full suite did not (M1).

**3. Do the matrix rows name tests that exist and assert the stated fact?**

M-458 and M-459 do, in full: every one of the seven and twenty named functions exists, and I read their
bodies — the census tests assert the printed census line and the named red, and the code-anchor tests run
the real hook and assert `decision == "block"` for the reds and no block for the passes. M-460 names a file
whose tests hold the whole-turn reach and the active-stop-hook stand-down, and claims one further fact —
standing down when the turn's record cannot be read — that no test holds (S2). M-390's fact cell gained a
fourth fixture and its owning-test cell names no test for it, though the tests exist (S7).

**4. Does any document claim something another denies?**

Three, and the first is a must-fix. The terminal vocabulary, across four surfaces and two machines (M3).
Row 489's cell against the runner it describes, seven against ten, inside the cell this fold edited (S6).
R293.8 against `hooks/code-anchor-scan.py`'s own comment about which forms are case-sensitive (S4).

One more was live for part of the afternoon and closed while I read: the architecture said five nets read
through the shared reader while the census counted ten wired hooks including the sixth net, so two
artifacts of one push disagreed about whether that net existed. The architecture went to six after 15:00.
It is worth recording because it is the shape M2 describes — two movements writing one clause — and because
nothing but a person noticing keeps that number true (S9).

**5. The judgment calls.**

*Extending the terminal vocabulary to four words rather than correcting the four legacy decision rows* —
**holds.** Rows 27, 33, 42 and 43 in `rotated-ROADMAP-2026-07-18.md` read `**decided 2026-07-05**`, and
`decided` is the honest terminal exit of a row that exists to settle a question; a decision row does not
land. Rewriting four archived cells to a word their authors never wrote would falsify the record the
nothing-lost law protects, and it would fix four instances of a class rather than the class. Widening the
vocabulary is the root fix. The choice is right and its execution is incomplete, which is M3.

*Correcting three archive status cells in place with a dated note* — **holds.** Each correction names the
date, names the source it was corrected off (the row's own delivery report), and keeps the pre-conversion
narration beside it, so the archive still holds what it held plus a labelled amendment. The alternative —
leaving a landed row reading `queued` in the archive forever — would keep the archive honest about its own
text while lying about the work. Named consequence for next time: a status word is read by more laws than
the one prompting the edit, and row 420's promotion red the delegation-line law before anyone noticed. A
correction sweep should re-run the suite before it is called done.

*Closing row 482 whole with the coverage leg discharged by the architecture pin* — **holds, with the
reservation in S9.** The reach itself is covered by tests rather than by the pin: the whole-turn reach lands in
`d7400d8` and `10dd65b` with the 2026-07-23 line reproduced as the red case, and M-457 and
`test_affirmation_in_an_early_narration_line_reds` hold it. The pin is the one-home statement of which nets
read through the shared reader, which is the architecture's proper job. The whole-close law is satisfied
because every leg has a discharge, and the coverage leg's discharge is a test. What the pin lacks is a
keeper: it is a count in prose that moved twice in one day.

*Widening the standing readability row (148) with the 2026-07-24 self-read* — **holds.** The added sentence
is an acceptance criterion of the same wish (each converted section's bodies pass two consecutive cold
reads, R88 first), so the one-wish-one-row law is not strained; this is a sub-behaviour, which is what
acceptance is for. The reservation is about the row rather than the choice: row 148 has stood since
2026-07-06 and each new reading finding makes its acceptance stricter, so its closing condition recedes as
it is worked. Worth giving it a bound — a named set of sections rather than every converted section — so
the row can reach a terminal word.

*Taking in row 494 as its own row* — **holds cleanly.** Clearing rendered pages after their moment shares
no behaviour with anything else in this delta; it came in as its own word at 14:30 and it is one wish with
its own done-when. Bundling it into a readability or a queue-hygiene row would have hidden a real wish
inside another row's acceptance.

---

## What to do next

1. Land the live suite failures green and re-run the whole suite, reading the log rather than the exit code (M1).
2. Decide the push's shape: finish and review the mid-turn movement so one push carries both, or lift its six insertions out of the four shared files (M2).
3. Give the terminal vocabulary one machine-readable home and rewrite the gate's comment, its failure message and the archive preamble off it (M3).
4. The nine should-fix findings ride the next movement. S1, S2 and S3 are three small tests and one criterion between them, and they close the same gap the addendum opened: behaviour that ships with nothing holding it.

Overall readiness: needs another iteration.

## Fold of this record's own findings, same movement (2026-07-27, by the authoring seat)

Every finding above is folded before the push; each disposition below is verifiable in the tree.

- **M1** — the suite is green: `python3 -m pytest tests/ -q` → 1938 passed, exit 0. The three live failures folded at their source: the architecture's redundancy pair went by pointing one owns entry at the shipped-and-covered terms its sibling states rather than restating them; the two shipped-language offences went by writing the registry note and the matcher's docstring in English; the dated marker left the spec body, its account living in the journal.
- **M2** — the census test derives its count from `guardrails/judge-hooks.json`'s wired list, so no literal ties the two movements together. The mid-turn scan's requirement, node entry and matrix row now stand, so the delta ships whole.
- **M3** — the terminal vocabulary reads four words on every surface: the queue format states it in one home, the rotation gate's regex, its docstring and its failure message read that list, the archive preamble names it, and `scripts/rotate-doc.py`'s closed signals are the same four.
- **S1, S3** — the census's two further red paths carry tests: a wired name resolving to no file, and a `proofs` entry naming a missing file. Requirement 292's criterion 8 now covers both maps and the wired declaration.
- **S2** — the code-anchor scan's three stand-downs carry tests, and the criteria for them live in one home beside the shared reader's own law (R230.9) rather than restated per hook.
- **S4** — the capital-shape criterion names the two code forms it holds.
- **S5** — the runner's closing line names whichever red path fired, each in its own sentence.
- **S6** — row 489's cell states the census over the wired declaration in place of the seven-hook count.
- **S7** — the rotation arm's six tests are named in M-390's evidence.
- **S8** — the Status column is located from the archive table's own header, with two tests over a reordered header.
- **S9** — the shared reader's consumer list has a net: `tests/test_architecture_pins.py` reads the real importers under `hooks/` and reds a pin naming fewer or more.
