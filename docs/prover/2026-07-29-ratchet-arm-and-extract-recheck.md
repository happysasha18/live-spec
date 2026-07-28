# Prover record — the ratchet arm and the session extract, push re-check, 2026-07-29

Prover skill: product-prover, live-spec pack v4.3.0. Mode: cross-link over the two commits that landed
after the night record, plus the whole-document quantifier re-verify (SPEC INV-170). Written by a seat
that authored none of this work (SPEC INV-237).

## Scope

**What this record reviews.** The tree at `67ac6f7`, with `de23cd6` and `67ac6f7` as the delta against
`3d1b9a2`. Four surfaces carry it:

- Requirement 302 gained criteria 12 to 16, over the record arm of gate aa and the census write;
- Requirement 303 gained criteria 32 to 38, over which transcript a run reads and where its extract
  lands;
- `TEST_MATRIX.md` gained rows M-486 to M-490, and row M-483 gave up two claims;
- `.github/workflows/gates.yml` hands gate aa the push event's own base commit.

Both requirements claim a shipped machine, so this pass reads the machine beside the text:

- `guardrails/check-doc-findings-bound.py` · `scripts/rule-census.py` · `guardrails/rule-census.json`;
- `scripts/session-extract.py` · `guardrails/check-handover-provenance.py`;
- `guardrails/pre-push:16-40` · `:230-234` · `.github/workflows/gates.yml:99-105`;
- `PRODUCT_SPEC.index.md` · `ARCHITECTURE.md:148` · `:150` · `guardrails/gate-red-proofs.json`.

**The record this pass stands on.** `docs/prover/2026-07-29-night-landings-push-recheck.md` holds eight
findings. Five of them are the defects this delta answers, and this pass judges each one below. Its
three recommendations, F6 through F8, stand open by decision, and this pass files nothing that repeats
them. The two earlier records it names, on Requirement 302 and Requirement 303, keep their own open
rows the same way.

**Commands run.** Every claim below was taken from a run or from the file.

- `python3 guardrails/check-doc-findings-bound.py` — exit 0, 108 live documents, 16 held at zero, the
  record arm reading against the copy `origin/main` holds.
- `python3 guardrails/check-handover-provenance.py` — exit 0, standing down by name over four files,
  one of them a session handover, every one dated before the counting start.
- `bash guardrails/check-prover-record.sh` — exit 1 before this record, naming `67ac6f7` as the spec
  change the newest record predates. That is the gate this file answers.
- `python3 -m pytest tests/test_doc_findings_bound.py tests/test_rule_census_ratchet.py
  tests/test_session_extract.py` — 36 passed.
- Five probes on scratch trees, one per finding that needed one. Each is quoted inside its finding.
  This record sits under `docs/prover/`, which the census carves out, so the live set never reads it.

## Verdict

**The five defects the night record raised are closed, and the two repairs left seven more behind
them.**

Gate aa's record arm now reads the copy the base commit holds, and a raise committed before the run
reds by name. The census computes its refusals above the write, and a refused reading leaves the record
on disk exactly as it stood. The extractor takes a session identity, refuses an identity that answers to
none or to several, and refuses an output path landing inside the tree.

The strongest hole is F1. A `reason` field licenses a raise once and then stays on the entry forever,
because the census copies it onto every later write. The second raise on that entry rides the first
raise's sentence. Row 525 is the landing that will write those reasons in, so the licences arrive with
it.

Two more sit on the same arm. An entry the base copy never held is skipped, so a ceiling born high with
no reason passes. And the arm reads `origin/main` while the pushed ref's own remote copy sits on the
hook's stdin. That reds a lane branch which touched no record at all.

| # | Kind | Claim | Status |
|---|---|---|---|
| F1 | defect | A `reason` written for one raise licenses every later raise on that entry, since the census carries the field forward on every write | open |
| F2 | defect | A record entry the base copy never held is skipped by the arm, so a ceiling born above its measured count with no reason passes | open |
| F3 | defect | The arm reads `origin/main` where the pushed ref's own remote copy is already on the hook's stdin, which reds a lane branch that raised nothing | open |
| F4 | defect | An empty session identity is read as no identity, so the run falls back to the newest transcript and the closing session guesses again | open |
| F5 | defect | The census report is written from a reading that refused, showing zeros and a measured count, while the record write refuses the same numbers | open |
| F6 | defect | The extractor accepts the leading part of an identity, and criterion 32 asks for the file named for that identity | open |
| F7 | defect | Criterion 15 states that the arm says nothing, and the shipped arm names the copy it read on every run | open |
| F8 | recommendation | `--repo` carries two meanings at once: which transcripts a run takes, and where an extract may not land | open |
| F9 | recommendation | Criterion 16 sits under the case named for the record moving down, while it governs a fall | open |

## Phase 1 — the model, as the delta leaves it

**The findings ratchet.** The record `guardrails/rule-census.json` holds one entry per live document.
Gate aa now reads it twice. The document arm measures each live document and compares it against its
recorded count. The record arm compares the record against the copy a base commit holds, and reds an
entry whose count rose with no reason. The base commit comes off a ladder: a stated base, then
`origin/main`, then the commit before the tip, then the tip. The census refuses to store a rise, and it
now refuses to write at all when any reading refused.

**The session extract.** A run takes the transcripts that name this repository, then chooses one of
them. A named identity picks the file named for it, and an identity answering to none or to several
refuses the run. An unnamed run takes the transcript written last and says how many it chose among. The
output path is resolved before it is judged, and a path landing inside the repository refuses the run.

**Actors.** A closing session names its own identity to the extractor. An operator running by hand names
none. A person edits the record by hand and states a reason. Gate aa runs from `guardrails/pre-push` and
from the continuous-integration mirror, which hands it the push event's base commit.

### What I assumed

- I read criterion 15's "say nothing" as a demand for silence on the whole arm, which is what F7 rests
  on. The other reading is that the arm files no refusal, and the shipped reach line then holds.
- I read criterion 12's lead sentence as the claim, and its bullet as the road to it. F3 rests on the
  two disagreeing for any ref whose remote copy is not `origin/main`.
- I read criterion 13 as governing a raise against a count the base copy holds, which leaves the
  entry born high outside it. F2 rests on that reading.
- I treated the handover's identity check as owned by row 528, and I filed nothing for it.
- I treated the report heading's fixed date as owned by the night record's F8, and I filed nothing for
  it.

## Phase 2 — the night record's five defects, judged against the machine

**F1 of that record is closed.** The arm resolves a base through the ladder at
`guardrails/check-doc-findings-bound.py:102-118` and reads the record through `git show` at `:141`.
Probed on a scratch repository. A count was committed at 0, raised to 9 by hand, and committed again.
The gate ran with the earlier commit as its base. It printed the raise by name and exited 1.
The same tree with no raise exited 0.

**F2 of that record is closed.** Criteria 12 to 15 now state the arm. They name the copy it reads, the
refusal it files, the stand-down, and the silence over an unchanged record. Row M-486 carries them
with three tests, red-proven against `3d1b9a2`. Criterion 11 keeps the hand-edit rule alone.

**F3 of that record is closed.** `scripts/rule-census.py:314-326` computes every refused and unread row
above the record write. Probed against the shipped module with the lint call refusing. An entry recorded
at 7 stood at 7 after the run. The run named the refusal and exited 1.

**F4 of that record is closed.** `scripts/session-extract.py:248-256` matches the transcript file named
for the identity it was given. An identity answering to none or to several prints every path it matched
and exits 1, proven by two tests in `tests/test_session_extract.py`.

**F5 of that record is closed.** `scripts/session-extract.py:182-187` resolves the output path and
compares it against the repository root. A path under the root refuses the run with nothing written.
The row's four tests cover the link, the two-dot path, and the path outside.

**What else holds.** The formal index carries R302.12 through R302.16 under INV-301, and R303.32 through
R303.38 under INV-302. Four of them sit under INV-218 as well: R302.14, R303.34, R303.35 and R303.37.
The continuous integration mirror hands gate aa `github.event.before`, and the pull-request case
falls to `origin/main` under a full-depth checkout. Row M-483 gave up its two claims to rows M-488 and M-490. Every one of
Requirement 303's thirty-eight criteria is claimed by exactly one row.

## Phase 3 — findings

F1 — A reason written for one raise licenses every later raise on that entry

> "the census carries a recorded reason forward, so a later write keeps it." — PRODUCT_SPEC.md,
> Requirement 302, criterion 11

`scripts/rule-census.py:341-343` copies a recorded reason onto the entry it writes, whatever the new
count is. `guardrails/check-doc-findings-bound.py:160-161` skips any entry carrying a non-empty reason.
So a reason survives the repair it was written for, and the next hand raise on that entry rides it. The
person who raised a ceiling once has raised every ceiling on that document for good.

Probed on a scratch repository. An entry was recorded at 9 with a reason naming row 525. The census then
measured the repaired page at 0 and wrote the entry back, keeping the reason. The count was raised by
hand to 50 and committed, and the gate exited 0 with no mention of the raise.

The live record holds 109 entries and none of them carries a reason today, so nothing is licensed yet.
Row 525 is the landing that writes the first ones, and it writes them across every recorded document.

Bind the reason to the count it excuses. Two roads stand. Road a: the entry carries the count its
reason was written for. The arm then reads a reason as spent once the recorded count moves past it.
Road b: the census drops the reason whenever it writes a different count. A reason then lasts exactly
as long as its number. I prefer road a, since road b erases a sentence a person wrote. Either way one
criterion states when a reason expires.

`defect · missing-rule (invariant)`

F2 — A record entry the base copy never held is skipped, so a ceiling born high passes

> "*if* an entry's recorded count rose against that copy with no reason beside it, *then* the gate
> *shall* red." — PRODUCT_SPEC.md, Requirement 302, criterion 13

`guardrails/check-doc-findings-bound.py:155-157` skips every entry the base copy holds nothing for. A
new document therefore enters the record at whatever count the hand that added it wrote. The document
arm then measures the page, finds it under that ceiling, and prints a fall. The push is green, and the
headroom stands until someone runs the census.

Probed on a scratch repository. A page measuring 1 was given an entry recorded at 99 with no reason, and
both were committed. The gate printed "fell: NEW.md — recorded 99, measured 1" and exited 0.

Read a missing base entry as a count of zero, so any first entry above the page's own measure reds
without a reason. The census seeds a new entry from its own measure, so the lawful road never trips
this. State it as a bullet under criterion 13: an entry the base copy holds nothing for is read against
zero.

`defect · missing-scenario (state-space)`

F3 — The arm guesses a base while the pushed ref's own remote copy sits on the hook's stdin

> "the base commit is the one the remote holds, read from the stated base, then `origin/main`, then the
> commit before the tip" — PRODUCT_SPEC.md, Requirement 302, criterion 12

`guardrails/pre-push:25-30` reads git's ref-update lines once and exports them as `PUSH_REF_LINES`. Each
line names the remote's current object id for the ref being pushed, which is the copy criterion 12's
lead sentence asks for. `guardrails/pre-push:232` then calls gate aa with no base, and the arm falls to
`origin/main`. For a push to main the two agree. For a lane branch they do not, and the lane law makes a
lane branch the ordinary case here.

Probed on a scratch repository. A lane branched while the record recorded 50, main was repaired to 10,
and the lane landed a commit that touched no record entry. The gate read `origin/main`, reported a raise
from 10 to 50, and exited 1. The lane is blocked, and the message names a hand edit nobody made.

Have `guardrails/pre-push` export the remote object id off its own ref-update line as
`LIVE_SPEC_DIFF_BASE`. The ladder then stands as the fallback for a hand run.
The lines are already read and exported, so this is one parse. `guardrails/check-prover-record.sh` reads
the same variable and gains the same accuracy.

`defect · internal-conflict (consistency)`

F4 — An empty session identity is read as no identity, and the run guesses again

> "*if* the named identity matches no transcript, or matches more than one, *then* the system *shall*
> write no extract and *shall* refuse the run." — PRODUCT_SPEC.md, Requirement 303, criterion 34

`scripts/session-extract.py:248` tests the identity for truth, so an empty string falls to the branch at
`:257` that takes the transcript written last. A closing step builds its call from a checkpoint field,
and a field that reads back empty produces exactly that call. The run then extracts another lane's
transcript and exits 0, which is the coin toss this landing was built to end.

Probed on two transcripts under a scratch home. The call carrying an empty identity printed "no session
named", took the newer file, wrote the extract, and exited 0.

Test the option for presence, and treat a named-but-empty identity as an identity matching no
transcript. That is criterion 34's refusal, and it costs one word in the branch condition. Add the
empty-identity case to row M-489's tests.

`defect · missing-prerequisite (precondition)`

F5 — The census report is written from a reading that refused, and says nothing of it

> "*if* any reading refuses to run, *then* the census *shall* write no record and *shall* name that
> reading." — PRODUCT_SPEC.md, Requirement 302, criterion 16

`scripts/rule-census.py:310-313` writes the markdown report above the refusal check at `:314`. The
report's table prints the refused row's zeros, and its totals line states how many files were measured.
The table names unread files in a section of their own, and it carries no such section for a reading
that refused. So the record is protected and the page a person reads is not.

Probed against the shipped module with the lint call refusing. The record stood at 7 and the run
exited 1.
The report on disk read a total of 0 for that document, and its totals line said that one file was
measured.

The night record's F3 was folded at the record write, and its sibling on the same run went unswept. Mark
each refused row in the table and name it in a section beside the unread one, the way the class lens
asks. The report then states what it could not read.

`defect · hard-to-monitor (observability)`

F6 — The extractor accepts the leading part of an identity, and no criterion states that

> "The system *shall* take a session identity from the caller and *shall* read the transcript file named
> for that identity." — PRODUCT_SPEC.md, Requirement 303, criterion 32

`scripts/session-extract.py:173-179` falls back to a prefix match when no file name equals the identity.
Row M-488 states that behaviour, and no criterion does. A caller passing a truncated identity reads
another session's transcript at exit 0. The reach line names the file and never says that the match was
partial. The same call refuses on the day a second session's identity shares that prefix, so one
brief's behaviour changes under it.

Probed on three transcripts under a scratch home. The identity "a" took one file and exited 0. A third
transcript was written whose name also starts with "a", and the same call then refused and named both.

Two roads stand. Road a: state the leading-part match as a criterion, and have the run say that it
matched a leading part. Road b: drop the fallback, so an identity is the file name or nothing. I prefer
road b, since the closing session holds the whole identity and the fallback serves a hand run alone.

`defect · undefined-path (transitions)`

F7 — Criterion 15 states that the arm says nothing, and the arm speaks on every run

> "*when* no recorded count stands above that copy, that arm *shall* say nothing and *shall* leave the
> verdict to the document arm." — PRODUCT_SPEC.md, Requirement 302, criterion 15

`guardrails/check-doc-findings-bound.py:216-219` prints one line on every run, naming the copy the arm
read or the reason it stood down. The real tree's green run carries it: the record arm read the record
against the copy `origin/main` holds. Row M-482's test asserts the absence of two words, so the row's
claim of silence rests on nothing that reads the line. A later session repairing the code to match the
criterion would delete the arm's own statement of its ground.

The reach line is the better behaviour, and INV-269 already asks each run to state what it read. Reword
criterion 15: the arm files no refusal, and it names the copy it read. Then add an assertion to M-482
that reads the named copy on the green line.

`defect · direct-contradiction (contradiction)`

F8 — One option carries two meanings, and a fixture run turns the privacy check off

> "The system *shall* refuse an output path that lands inside the repository, and the refusal *shall*
> name that path and the reason." — PRODUCT_SPEC.md, Requirement 303, criterion 37

`scripts/session-extract.py:219` takes `--repo` as the path a transcript must name, and
`:223` hands the same value to the privacy check. A run pointed at a fixture repository therefore judges
its output path against the fixture, and a path under the real tree passes. The option's help text names
one meaning of the two.

Give the privacy check its own option, defaulting to the repository the script sits in, and leave
`--repo` to the transcript search. The two questions have one answer in every real run, and a fixture is
the case where they part.

`recommendation · later · boundary-issue (composition)`

F9 — A criterion governing a fall sits under the case named for the record moving down

> "**Case: the record moves only down**" — PRODUCT_SPEC.md, Requirement 302

Criteria 9 to 15 hold the rise. Criterion 16 holds the opposite move: a reading that never ran scores
zero, and that zero would lower the ceiling. A reader scanning the case headings meets the fall guard
under a heading that promises the rise. Those headings are what a reader of thirty-eight criteria
navigates by.

Give criterion 16 its own case, headed for a reading that never ran. The criterion and its bullet move
whole, and the case above keeps its four members.

`recommendation · now · confusing-for-users (cognitive-load)`

## The mandatory sweeps over the delta

The whole-document sweeps of a full pass are out of scope for a cross-link mode. The sweeps below were
run over the delta's own surfaces, and each verdict names what it read.

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The record arm, R302.12-15 | clean — INV-301 names gate aa, wired in the hook and the mirror, red proof registered | hit — F2, the entry with no count in the base copy | hit — F3, the ref whose remote copy is not `origin/main` | hit — F1, the reason outliving its raise | clean |
| The census write, R302.16 | clean — the same net holds it | clean — a refused reading and an unread file both stop the write | hit — F5, the report write on the same run | N/A — the run keeps no state between runs | clean |
| The transcript choice, R303.32-36 | clean — INV-302 names gate ab, and row 528 owns the identity comparison | hit — F4, the empty identity | clean — no sibling extractor | clean — each run stands alone | hit — F6, the leading part |
| The output path, R303.37-38 | clean — the path check and the ignore rule stand as two nets | clean — the link, the two-dot path and the absolute path each judged where they land | hit — F8, the option carrying two meanings | N/A | clean |

**The quantifier re-verify (INV-170).** Seven enumerations were re-read against the delta. The formal
index carries R302.12 to R302.16 under INV-301, and R303.32 to R303.38 under INV-302. It carries the
two new criteria under INV-117, and the four refusal criteria under INV-218. Requirement 302's
sixteen criteria are each claimed by one of rows M-479 to M-482 and M-486 to M-487. Requirement 303's thirty-eight are each
claimed by one of rows M-483 to M-485 and M-488 to M-490, and M-483's two given-up claims land whole.
The gate-letter roster ends at ab in the hook, the mirror and the red-proof registry, unchanged by this
delta. The matrix level column reads browser-computed for M-486, which is the word the eight sibling
by-deed rows carry. The census docstring's exit sentence names the new refusal. One enumeration fails:
the case heading over criterion 16, which is F9.

## Phase 3.5 — acknowledged gaps

Requirement 302 and Requirement 303 carry no open item, no marked decision and no rhetorical question.
The queue holds the gaps their prover passes named: rows 520, 523, 524, 525, 526, 527 and 528. Row 526
owns the gate's own read of a refused reading, which is why F5 above speaks of the report alone. Row 528
owns the handover naming another lane's transcript, and F4 above is the extractor's side of that same
lane question. Row 527 waits on Alexander's word about what closes a worker-command finding.

## Phase 4 — human and operational factors

**Privacy.** The criterion that keeps an extract out of the tree now has a machine behind it. The
ignore rule stands as the second net. The residual privacy hole is F4. A run that guesses reads another
lane's private conversation. The extract it writes carries that lane's words under this lane's name.

**What an operator sees.** Gate aa's green line names the live count, the count held at zero, and the
word cap. It also names the rung the record arm read. That last line is the one F7 asks the criterion
to admit. Gate ab stood down today over four files, one of them a session handover, every one dated before the counting
start of 2026-07-29. So the handover law counts from today and has read nothing yet.

**Scale.** The census runs two lint subprocesses over 108 documents, and the gate run for this pass took
minutes. Nothing states a ceiling for that run's time, and the live set grows with the tree. The suite
budget check owns the suite's wall time, and this gate sits on the push chain beside it.

## Phase 5 — closing

**Three to fix before the next landing on these requirements.** F1, because row 525 writes the first
reasons in and each one is permanent. F3, because a lane branch that raised nothing is blocked by name.
F4, because an empty field reinstates the guess this delta removed.

**Properties the documents should state.**

- A recorded reason excuses one raise, and it expires when the recorded count moves again.
- A record entry the base copy holds nothing for is read against a count of zero.
- The base a push is judged against is the object id the remote holds for the ref being pushed.
- A named identity that carries no characters refuses the run the way an unmatched identity does.

**Open questions for Alexander.** Whether a spent reason is dropped from the record or kept beside the
count it excused. Whether the leading-part match stays as a hand-run convenience or leaves.

**Queued for a taste call.** F8 and F9, together with F6, F7 and F8 of the night record, which stand
open by decision.

**Readiness.** The push gate's record demand is met by this file. Gate aa, gate ab and the three test
files for this delta all read green. Requirement 302 and Requirement 303 each need another iteration,
and the seven defects above owe queue rows before the next landing on either one.
