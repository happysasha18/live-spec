# Prover record — the night's five landings, push re-check, 2026-08-04

Prover skill: product-prover, live-spec pack v4.3.0. Mode: cross-link over the five commits waiting to
be pushed, plus the whole-document quantifier re-verify (SPEC INV-170). Written by a seat that authored
none of this work (SPEC INV-237).

## Scope

**What this record reviews.** The tree at `9bf8da7`, with `900c80e`, `904fe0d`, `30fcc97`, `d09db47`
and `9bf8da7` as the delta against `b6430d0`. Five surfaces carry it:

- `scripts/preshow-register-lint.py` gained a marked region whose contents the check skips, and
  `tests/test_preshow_register_lint.py` gained six tests for it;
- `guardrails/language-rules.json` and the two pages built from it were rebuilt, and the coverage page
  corrected its statement of which language this machine uses for conversation;
- `docs/PROGRESS.md` is new, `docs/MEASUREMENTS.md` was rewritten, and
  `scripts/measurements-table.py` with `guardrails/progress-baseline.json` moved beside them;
- four report files landed under `inbox/`, holding roughly 53 findings between them;
- `NEXT_STEPS.md`, the file a session reads to pick up where the last one stopped, took 43 more lines,
  and `attic/MANIFEST.md`, the list of files moved out of the tree to a recoverable store, took two.

The delta claims shipped machines, so this pass reads the machines beside the text:

- `scripts/preshow-register-lint.py:125-155` · `:158-166` · `scripts/register-lint-floor.json`;
- `guardrails/check-doc-findings-bound.py` · `guardrails/rule-census.json`;
- `guardrails/check-rendered-sweep.py` · `guardrails/check-prover-record.sh:32-60`;
- `PRODUCT_SPEC.md` Requirements 18, 127, 141, 256 and 302 · `TEST_MATRIX.md:418-421` · `:887`.

**The records this pass stands on.** `docs/prover/2026-07-29-night-landings-push-recheck.md` and
`docs/prover/2026-07-29-ratchet-arm-and-extract-recheck.md` hold seventeen findings between them, and
the open ones stand by decision. This pass files nothing that repeats them. Where a finding below
touches the same machine, it says so and stays on the part this delta created.

**Commands run.** Every claim below was taken from a run or from the file.

- `python3 -m pytest -q tests` — 9 failed, 2302 passed, log at `suite-run-2.log` in this session's
  scratch directory. The section below names all nine.
- `python3 guardrails/check-doc-findings-bound.py` — exit 0 on the working tree, 119 live documents,
  21 held at zero. Exit 1 on the committed tree, naming the four new `inbox/` files. F3 rests on that
  pair.
- `python3 guardrails/check-rendered-sweep.py` — exit 0, no page standing.
- `python3 -m pytest -q tests/test_language_rules.py` — 23 passed, closing the tenth failure of the
  earlier run.
- `python3 scripts/preshow-register-lint.py` on two probe files written for this pass. Both are quoted
  inside F2.
- `git show HEAD:guardrails/rule-census.json` and `git show HEAD:NEXT_STEPS.md`, read against their
  working-tree copies.

## Verdict

**The wording check's new exemption is sound machinery standing on no written rule, and two of
tonight's commits ship a state the push gate refuses.**

The exemption itself behaves the way its commit message describes. A marked region is skipped, an
unclosed marker exempts nothing, the reported line numbers still point at the real lines of the real
file, and the six tests cover each of those. The rebuilt language pages match a fresh build, and the
coverage page's statement about this machine's conversation language is now correct.

The strongest hole is F1. Requirement 18 says the check reads a surface's text, and the shipped check
now reads part of a surface's text. No criterion states the exemption, no matrix row claims it, and the
glossary entry still describes the older behaviour.

F2 is the exemption's own weak point, and the ask that opened this pass named it. Nothing compares a
marked region against the document it claims to reproduce. A probe confirmed that words written for
this pass, wrapped in the marker, pass the check silently.

Two more sit on the committed tree. Four report files were committed as documents the counting record
must cover, and their record rows stand in an uncommitted working tree. And the resume file went from
124 lines to 167 against a stated cap of 100.

| # | Kind | Claim | Status |
|---|---|---|---|
| F1 | defect | The check now skips part of a surface's text, and no criterion, matrix row, or glossary line says so | open |
| F2 | defect | Nothing tests that a marked region reproduces another document, so a page marks its own words and the check goes quiet | open |
| F3 | defect | Four report files were committed as documents the counting record must cover, and their rows stand only in an uncommitted working tree | open |
| F4 | defect | The one-file deposit rule and the counting-record rule cannot both be satisfied by a deposit from another machine | open |
| F5 | defect | The resume file stands at 167 lines against its stated cap of 100, and this delta added 43 of them | open |
| F6 | defect | The suite demands a `## LIVE STATE` block in the resume file, no criterion names that heading, and the file carries none | open |
| F7 | recommendation | The progress page, the measurement script, and its baseline carry no criterion, no owning node, and no test row | open |

## Phase 1 — the model, as the delta leaves it

**The wording check.** A page about to be shown to a person is read line by line for machine dialect:
an internal coined phrase shown raw, an English term of this project translated word for word into
another language, or such a term spelled out in another alphabet. A hit blocks the showing. The check
holds 23 fixed patterns, and a separate file records 23 as the floor that count may never fall below.

Tonight the check gained a fourth state for a page's text. A region opened by `<!-- register-lint:quoted-source -->`
and closed by `<!-- register-lint:/quoted-source -->` is blanked before the read, with its newlines
kept so later line numbers still hold. A page with no marker is read whole. A page whose marker is
never closed is read whole. Everything outside a closed region is read.

**The counting record.** `guardrails/rule-census.json` holds one row per live document, each row
carrying that document's measured count of writing-rule findings. A push is refused when a live
document's count stands above its recorded row, and refused again when a live document has no row at
all. Tonight added four live documents: the four report files under `inbox/`.

**Actors.** A person or an agent about to show a page runs the wording check. A person writes the
marked region into the page. Another machine's agent deposits a single report file into `inbox/` and
pushes it under its own grant. A session rewrites the resume file at the end of a movement.

### What I assumed

- I read Requirement 18 criterion 1 as governing the whole of a surface's text, since it says "read its
  text" with no part named. F1 rests on that reading. The other reading is that the criterion leaves
  the check free to decide what counts as the surface's own text, and F1 then becomes a request for
  that sentence rather than a broken promise.
- I read the marker's purpose from the script's own comment and its commit message, both of which say
  the region reproduces another document. Nothing in the code carries that meaning, which is F2.
- I treated the base-reference question raised as F3 of `2026-07-29-ratchet-arm-and-extract-recheck.md`
  as still open, and filed nothing repeating it. It bears on this tree: the local copy of the shared
  branch was last updated on 2026-07-28, so the record arm compares against a week-old copy.
- I treated the resume file's length as in scope because this delta added 43 lines to it. The file
  already stood at 124 lines before the delta, over the same cap.
- I found no criterion naming `docs/PROGRESS.md`, `docs/MEASUREMENTS.md`, `scripts/measurements-table.py`,
  or `guardrails/progress-baseline.json` anywhere in the specification, the architecture, the matrix, or
  the queue. F7 rests on that search.

## Phase 2 — the shipped machines, read against the text

**What holds in the wording check.** `scripts/preshow-register-lint.py:141-151` blanks each closed
region with the same count of newlines it removed, so a hit found later in the file still reports its
real line. `:148-150` returns the text untouched when an opening marker survives the blanking, so a
half-written region exempts nothing. `:158-166` runs every pattern over the blanked text. The pattern
count reads 23 against a floor of 23, so the delta removed no pattern.

**What holds in the language pages.** `python3 -m pytest -q tests/test_language_rules.py` returns 23
passed. That test was red before this delta, because the generated pages held line numbers of documents
that had since been rewritten. The coverage page's note now reads that this machine uses English for
conversation with a Russian aside answered in Russian, which matches the instruction the machine runs
under.

**What holds in the recoverable-file list.** The three rendered pages the suite named have been moved
out of the tree and the gate returns exit 0. The two entries added to `attic/MANIFEST.md` name them.
A third entry, for the page cleared after the commit, stands in the working tree and is uncommitted.

**What the committed tree shows.** `git show HEAD:guardrails/rule-census.json` holds no row for any of
the four new report files. The working-tree copy holds all four. So the tree a push would carry is the
tree the counting gate refuses, and the repair sits beside it uncommitted. That is F3.

## Phase 3 — findings

F1 — The check now skips part of a surface's text, and no written rule says so

> "Before a human-facing surface is shown, the system *shall* have `scripts/preshow-register-lint.py`
> read its text and block the showing on a red result until the flagged text is rewritten into the
> reader's plain words." — PRODUCT_SPEC.md, Requirement 18, criterion 1

The criterion says the check reads the surface's text. Since `904fe0d` the check reads the surface's
text minus every closed marked region. Requirement 18 holds five criteria and none of them mentions a
region, a marker, or a quotation. The glossary entry carries the same older description: the check
"reads a surface's text for machine dialect and blocks the showing on a red result"
(PRODUCT_SPEC.md, glossary). The matrix lists six rows under this rule — M-196, M-197, M-215, M-216,
M-250 and M-384 — and the six new tests are claimed by none of them. M-196 states "never a fixture leak
passing", which a marked leak now does by design.

The person affected is the next session that reads Requirement 18 to decide what the check promises. It
will read a whole-text guarantee, show a page carrying a marked region, and believe the page was read
whole. A later session repairing the code to match the criterion would delete the exemption and take
the six tests red with it.

Write one criterion under a new case in Requirement 18, in these words:

> *when* a surface marks a region as reproduced from another document, the system *shall* read that
> region as quotation and *shall* read every other part of the surface in full; *if* an opening mark
> carries no closing mark, *then* the system *shall* read the surface whole.

Then add a matrix row claiming the six tests and pointing at the new criterion, and correct the
glossary entry to say the check reads what the surface states in its own words. The neighbouring rule
already carries the sentence this one owes: "*when* a scan hook reads text inside quotation marks or
code fences, the system *shall* skip it, since such text names a pattern rather than using it, so a
demonstration is never flagged" (PRODUCT_SPEC.md, Requirement 262, criterion 5). The two checks now do
the same thing for the same reason, and one of them says so.

`defect · missing-rule (invariant)`

F2 — Nothing tests that a marked region reproduces another document

> "A page marks each region it reproduces verbatim from another document with a fence, and this lint
> reads what is inside as quotation." — scripts/preshow-register-lint.py:130

The marker's whole justification is that the words inside it belong to some other document, so charging
the page for them would be charging it for a faithful copy. The code checks nothing of the kind. It
matches an opening marker, a closing marker, and blanks whatever lies between them. No source document
is named in the marker, none is opened, and no comparison is made.

Probed on two files written for this pass. A file holding one sentence of my own invention, carrying
two of the check's patterns, exits 1 and names both hits at line 3. The same sentence with the two
markers around it exits 0 with the green line "no coined metaphor, calque, or transliterated pack term
found". The person affected is the reader the check exists to protect: a page written in machine
dialect throughout, wrapped end to end in one pair of markers, is shown to them with the check's
blessing.

Two roads stand. Road a: the opening marker names its source, as
`<!-- register-lint:quoted-source: docs/spec-style.md -->`, and the check reads that file and refuses
the exemption for any line the named file does not contain. Road b: the check caps how much of a page
a marked region may cover, refusing an exemption over some share of the page's own lines. I prefer road
a, since it answers the actual question and the named file is already on disk in every real use. Road b
costs less and stops only the extreme case. A third answer is legitimate: state in the criterion that
the exemption is taken on the author's word, so a reader of the rule knows what it rests on. The
section below says plainly which of the three I think this delta owes.

`defect · unenforceable-promise (discharge)`

F3 — Four documents were committed with no row in the counting record, and the rows sit uncommitted

> "*if* a live document carries no entry in the record, *then* the system *shall* refuse the push and
> *shall* name that document." — PRODUCT_SPEC.md, Requirement 302, criterion 6

`d09db47` committed four report files under `inbox/`. Each is a live document by the counting rule, so
each owes a row in `guardrails/rule-census.json`. `git show HEAD:guardrails/rule-census.json` holds
none of the four. The rows were written afterwards and stand in the working tree, uncommitted alongside
two other uncommitted changes.

This has two consequences with two different owners. A person pushing from this machine gets a green
local gate, because the local gate reads the working tree. The continuous-integration run then reads
the pushed commits alone, finds four live documents with no row, and reds — after the push, where the
failure is a message rather than a block. Second, the four rows were written by a run separated from
the commit that made them necessary, so a session that pushes and then discards its working tree ships
the documents and loses the rows.

Commit `guardrails/rule-census.json` before pushing, so the four rows travel with the documents that
need them. For the class behind the instance: have the deposit path write the row in the same commit as
the file, the way the queue-archive rule already binds a row's move to its closing commit. State it as
a criterion under Requirement 302: a commit that adds a live document carries that document's row.

`defect · partial-success-risk (atomicity)`

F4 — The one-file deposit rule and the counting-record rule cannot both be satisfied

> "*when* a push's diff is exactly one new file under `inbox/`, the system *shall* owe the fence and no
> re-check record, a diff carrying anything more riding the full gate." — PRODUCT_SPEC.md,
> Requirement 141, criterion 3

That rule exists so an agent on another machine can drop one report file and push it without owning
this project's review process. Requirement 302 criterion 6, quoted in F3, refuses a push carrying a
live document with no row in the counting record. A deposited report file is a live document. So the
depositing agent has two moves and both are refused. Pushing the one file alone satisfies the deposit
rule and is refused by the counting rule. Adding the record row makes the diff two files, which loses
the deposit exemption and demands a fresh review record the depositing agent has no standing to write.

The affected actor is the remote agent named in Requirement 254 — the one that "*shall* commit one new
inbox file touching the inbox alone with the source named, and *shall* push it under a per-repository
grant". Its push is rejected, and the message it reads tells it to run a measurement command over this
project's whole document set, which its grant does not cover. Tonight's four files are the local
instance of the same collision; the remote one has no local hand to fix it.

Carve `inbox/` out of the live set the counting record must cover, and state the reason: a deposited
file is another machine's text, arriving unedited, and holding it to this project's writing rules
charges the sender for words this project did not write. The row it would carry is the row the harvest
drops when the file leaves the inbox anyway. The other road is to let the counting gate seed a missing
row from its own measurement rather than refusing, which keeps the coverage and gives up the
"every document was measured deliberately" guarantee. I prefer the carve-out, since the deposit rule
was written to keep a stranger's push cheap.

`defect · direct-contradiction (contradiction)`

F5 — The resume file stands at 167 lines against a stated cap of 100

> "The system *shall* hold the whole resume file at 100 lines or fewer and *shall* have a suite check
> own the number, reddening on a bloated file proven with a synthetic one." — PRODUCT_SPEC.md,
> Requirement 127, criterion 1

`NEXT_STEPS.md` is the file a session reads first to learn where the work stopped. It measures 167
lines at `9bf8da7`, and it measured 124 before this delta. The check named in the criterion is doing
its job: `tests/test_resume_digest.py` reds and names the number. The failure is that a commit landed
over it.

The affected actor is the next session after a memory wipe, which is exactly who this file is for. It
opens a digest built to be read in one pass and meets a document that has become a narrative, with the
older sections describing a campaign the owner stopped. Requirement 127 criterion 2 states the repair
shape already: each open leg restated as one terse line naming where its detail lives.

Rewrite `NEXT_STEPS.md` to the cap before the push, moving the campaign narrative in its opening
sections to the journal and leaving one line per open leg. The suite turns green on the same commit.

`defect · unenforceable-promise (discharge)`

F6 — The suite demands a section heading the specification never names

> `blocks = re.findall(r"^## LIVE STATE", body, re.M)` — tests/test_traceability.py:614

`tests/test_traceability.py` requires `NEXT_STEPS.md` to hold exactly one `## LIVE STATE` heading,
carrying a date. `guardrails/check-landing-next-steps.py:5` describes the same file as "LIVE STATE +
queue only". The words "LIVE STATE" appear nowhere in `PRODUCT_SPEC.md`. The file at `9bf8da7` carries
no such heading, and its top section is headed "Read this first, 2026-07-29 evening".

So a blocking check owns a rule no criterion states, and the file it guards has drifted away from that
rule with no criterion to appeal to. A session repairing the file has to read the test to learn what
shape is required. A session repairing the test has nothing to check it against. This is the
code-with-no-clause shape, and it sits on the same file as F5, so one rewrite answers both.

Add a criterion to Requirement 127 stating the file's shape: a single dated live-state section followed
by the queue, replaced at each landing rather than stacked. Then restore the heading in the rewrite F5
asks for.

`defect · missing-rule (invariant)`

F7 — The progress page and the script behind it carry no criterion, no owning node, and no test row

> "Progress and measurement pages state where the two promises stand" — the commit message of `30fcc97`

`docs/PROGRESS.md` joined the tree in this delta at 273 lines. `scripts/measurements-table.py` and
`guardrails/progress-baseline.json` moved with it. A search of `PRODUCT_SPEC.md`, `ARCHITECTURE.md`,
`TEST_MATRIX.md` and `ROADMAP.md` for any of those four names returns nothing. So the project ships a
script, a stored baseline, and two pages a person reads, with no sentence saying what they promise and
no test asserting anything about them.

The affected reader is the owner, who reads these pages to judge where the work stands. The numbers on
them come from a script nothing constrains: no clause states what the baseline means, when it may be
rewritten, or what the pages must show when a measurement refuses to run. The pages themselves are
clean of machine dialect — the wording check passes both — so this is a backing gap rather than a
reader problem.

Write one requirement covering the measurement pages: what each page states, which command produces it,
when the baseline is rewritten and by whose decision, and what a page shows for a measurement that did
not run. Give the script an owning node in the architecture, and one matrix row asserting that a run
reproduces the committed page. Until that exists, these pages are a working aid rather than something
the project stands behind, and the requirement is what turns them into the second.

`recommendation · now · hard-to-operate (ops-ux)`

## The fence, judged plainly

The reviewer's objection is correct, and the objection matters less than it first looks.

Nothing in the shipped check verifies that a marked region reproduces another document. A page can mark
its own sentences and the check falls silent over them. I confirmed it with a probe: a sentence I wrote
for this pass, carrying two of the check's own patterns, passes at exit 0 once the markers are around
it. So the exemption is taken on the word of whoever writes the page.

Whether that is acceptable turns on who writes the marker and what the check is for. This check is the
last thing standing between a page and a person's eyes, and every page it reads is written by the same
session that then shows it. A session willing to mark its own dialect as quotation is a session willing
to skip the check entirely, which it can already do by not running it. The exemption grants no power
the writer lacked. It removes an obstacle that was stopping honest pages — two comparison pages that
could never be shown, because reproducing a document faithfully meant reproducing its coined terms.

So I would ship it. What I would fix now is smaller and firmer than the objection: the criterion F1
asks for should state, in the specification itself, that the exemption is taken on the author's word.
A rule that rests on trust and says so is a rule a reader can weigh. A rule that says the check reads
the surface's text, while the check reads part of it, is the one that misleads. That sentence costs one
line and closes the honest half of this gap today.

The mechanical half — road a of F2, where the marker names its source and the check reads that file —
is worth a queue row rather than a block. It becomes urgent the day a page is marked by something other
than the session that wrote it: a generated comparison page, a report assembled from several sources,
or a page written by an agent whose output another agent shows. None of those exists yet.

## The suite, 9 failed and 2302 passed

The run: `python3 -m pytest -q tests` — **9 failed, 2302 passed** in 489 seconds. The previous run over
this tree read 10 failed, 2295 passed. The two numbers reconcile exactly: seven tests moved from red or
absent to green — one language-rules test that `900c80e` repaired, and the six new tests `904fe0d`
brought — and no test moved the other way.

The nine that remain, each with its cause:

1. `tests/test_config_health.py::TestConfigHealth::test_this_repo_installed_hooks_match_source` — the
   copies of four hooks and eleven skills installed under the user's home directory have drifted from
   the sources in this repository. The check names each one and names its own repair:
   `scripts/install-pack-hooks.sh` and `scripts/sync-skills.sh`. Environment state rather than tree
   state.
2. `tests/test_config_health.py::TestPermissionPathHealth::test_real_personal_settings_stands_down_or_passes`
   — the same drift reported through a second entry point. The permission half of that check reports
   clean: 69 rules, 9 naming a path, every path resolving.
3. `tests/test_doc_findings_bound.py::TestDocFindingsBound::test_the_real_repository_passes` — the four
   report files committed in `d09db47` are live documents with no row in the counting record. This is
   F3. The working tree now passes; the committed tree does not.
4. `tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes` — no file matching
   `docs/prover/2026-08-04*.md` existed when the suite ran. This record answers it.
5. `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes` — this test copies the tree to
   a temporary directory and runs the whole suite there. It reports four failures of its own, which are
   numbers 3, 7, 8 and 9 of this list surviving the copy. It carries no cause of its own.
6. `tests/test_guardrails.py::TestGateShippedLanguage::test_gate_green_on_the_swept_tree` — five lines
   of Russian in two fixture files, `guardrails/measured-number-fixtures/bare-number.md` and
   `guardrails/measured-number-fixtures/measured-number.md`, carry no marker saying the Russian is
   deliberate. Both fixtures arrived in `b6430d0`, one commit before this delta. The check names the
   repair: a `user` code fence or an inline `user-language` comment.
7. `tests/test_rendered_sweep.py::test_gate_passes_the_real_tree` — three pages built for a single
   reading still stood in the tree: `docs/MEASUREMENTS.html`, `docs/PROGRESS.html`, and
   `docs/plans/2026-07-29-specification-subdivision.html`. All three have since been moved to the
   recoverable store, and `python3 guardrails/check-rendered-sweep.py` now exits 0. The pages were
   untracked, so a fresh checkout never held them and this failure is local to this machine.
8. `tests/test_resume_digest.py::TestResumeDigestCap::test_resume_digest_cap` — `NEXT_STEPS.md` is 167
   lines against the 100-line cap. This is F5.
9. `tests/test_traceability.py::TestDoors::test_next_steps_live_state` — `NEXT_STEPS.md` carries no
   `## LIVE STATE` block and the test requires exactly one. This is F6.

Read by owner: two belong to this machine's installed copies (1, 2), one is answered by this file (4),
one is a mirror carrying no cause of its own (5), one is now closed in the tree (7), one arrived one
commit before this delta (6), and three are the delta's own to repair before the push (3, 8, 9).

## The mandatory sweeps over the delta

The whole-document sweeps of a full pass are out of scope for a cross-link mode. The sweeps below were
run over the delta's own surfaces, and each verdict names what it read.

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The wording check's exemption | hit — F1, a shipped behaviour with no criterion, no matrix row, and a glossary line describing the older reading | clean — the empty region, the unclosed marker, and the file with no marker are each covered by a test | hit — F1, the sibling scan hooks state their own quoting rule and this one states none | N/A — the check keeps no state between runs | hit — F2, the region whose source is never read |
| The language rules and their pages | clean — the generating script and its comparison test both ship and read green | clean — the rebuild covers every entry in the source | clean — both generated pages come from the one source | clean — a rebuild replaces each page whole | clean |
| The counting record's coverage | clean — the check is named, wired to the push, and red-proven | hit — F3, the commit that adds a document without its row | hit — F4, the deposit rule and this rule refusing the same push | clean — a row's states are stated | clean |
| The resume file | clean — two suite checks own it | hit — F5, the cap crossed and committed over | clean — no sibling digest | hit — F6, the section shape held by a test alone | clean |
| The progress and measurement pages | hit — F7, no rule declares them and no check reads them | N/A — no stated bound to test the ends of | clean — the two pages share one generator | N/A — no state carried between runs | hit — F7, the baseline's rewrite rule unwritten |

**The quantifier re-verify (INV-170).** Six enumerations were re-read against the delta. The pattern
floor reads 23 in `scripts/register-lint-floor.json` and the shipped check holds 23 patterns, so M-215
holds and the delta removed nothing. The matrix's rule index lists M-196, M-197, M-215, M-216, M-250
and M-384 under the wording rule, and the six new tests belong to none of them — the first failure,
folded into F1. M-196's "never a fixture leak passing" is now false as written for a marked leak — the
second failure, the same finding's second half. The glossary's description of the check is the third,
also F1. The language coverage page's list of the places each rule is stated was rebuilt and its line
numbers now match the files. The recoverable-file list holds one line per page moved, with the newest
line uncommitted. Requirement 302's criteria are each still claimed by exactly one matrix row.

## Phase 3.5 — acknowledged gaps

Requirements 18, 127, 141, 256 and 302 carry no open item, no marked decision, and no rhetorical
question. The four report files that landed under `inbox/` are themselves 53 acknowledged gaps awaiting
harvest into the queue, and this pass files nothing that anticipates them. `NEXT_STEPS.md` states in
its own words that the campaign behind those reports measured the wrong quantity and that the owner
stopped it; that statement is the document's own known issue and F5 asks only that it be restated
inside the cap.

## Phase 4 — human and operational factors

**What a person sees.** The wording check's green line says no coined metaphor, calque, or
transliterated term was found. After this delta that line is true of the unmarked part of a page, and
the line says nothing about how much of the page was marked. One number on the green line — how many
lines the exemption covered — would let a reader judge the verdict they are being handed. That is the
reach rule this project already applies to its other checks, and it is the cheapest half of F2.

**What an operator sees.** The counting gate's green line names 119 live documents and 21 held at zero.
Its record arm names the copy it compared against. On this machine that copy is a week old, because the
local pointer to the shared branch was last updated on 2026-07-28. The arm reports what it read, so the
staleness is visible rather than hidden, and the base-reference finding of the 2026-07-29 record already
owns the repair.

**Scale.** The full suite took 489 seconds in this run, against 396 seconds in the run before it. The
new tests account for little of that; the counting gate's two measurement passes over 119 documents
account for most. Nothing states a ceiling for the suite's wall time on this project, and the document
set grows with the tree.

**Privacy.** This delta adds no path that carries private conversation. The ignore rule added to
`.gitignore` in the working tree keeps backup copies of rewritten files out of the repository, which
narrows rather than widens what leaves the machine.

## Phase 5 — closing

**Three to fix before this push.** F3, because the four documents and their record rows are in
different places and only one of them is going to be pushed. F5 and F6 together, because one rewrite of
the resume file closes both and both are red in the suite right now. F1, because the specification
currently describes a check that no longer exists.

**Properties the documents should state.**

- A surface may mark a region as reproduced from another document, and the wording check reads that
  region as quotation while reading every other part of the surface in full.
- An opening mark with no closing mark exempts nothing, and the surface is read whole.
- The exemption is taken on the word of whoever wrote the surface, and no check compares the marked
  region against its claimed source.
- A commit that adds a live document carries that document's row in the counting record.
- A file deposited from another machine into the inbox stands outside the counting record's coverage.
- The resume file holds one dated live-state section followed by the queue, replaced at each landing.

**Open questions for Alexander.** Whether the marked region should name its source file and be checked
against it, or stay a matter of the author's word with the specification saying so. Whether the progress
and measurement pages become a stated promise of this project or stay a working aid.

**Queued for a taste call.** F7, together with the recommendations left open by the two records of
2026-07-29.

**Readiness.** The specification is sound enough for these five commits to be pushed once F3, F5 and F6
are closed, and closing all three is one commit: the counting record committed, the resume file rewritten
to its cap with its live-state section restored. F1 and F2 are honest debts against a working machine
rather than reasons to hold the code back, and F1's criterion is cheap enough to ride the same commit.
Pushing before those three are closed sends a tree its own suite refuses.
