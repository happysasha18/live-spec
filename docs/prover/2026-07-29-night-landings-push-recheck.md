# Prover record — the night's six landings, push re-check, 2026-07-29

Prover skill: product-prover, live-spec pack v4.3.0. Mode: cross-link over the six commits that landed
between 23:58 and 00:00, plus the whole-document quantifier re-verify (SPEC INV-170). Written by a seat
that authored none of this work (SPEC INV-237).

## Scope

**What this record reviews.** The pushed state at `04f4a2f`, with the six commits `5a5f86a`, `db9586d`,
`35e8a1d`, `a6bd34b`, `9477afb` and `04f4a2f` as the delta. Four surfaces carry that delta:

- Requirement 302 gained criteria 9, 10 and 11 under the case "the record moves only down";
- Requirement 303 is new, with 31 criteria over the session record read at both ends;
- `skills/live-spec-base/SKILL.md` gained rule 35, and `ARCHITECTURE.md` gained the pins under INV-302;
- `TEST_MATRIX.md` gained rows M-480 to M-485, and `ROADMAP.md` took rows 521 to 525.

Both requirements claim a shipped machine, so the pass reads the machine beside the text:

- `scripts/rule-census.py` · `guardrails/check-doc-findings-bound.py` · `guardrails/rule-census.json`;
- `scripts/session-extract.py` · `guardrails/check-handover-provenance.py`;
- `guardrails/pre-push:225-241` · `.github/workflows/gates.yml:100-102`;
- `guardrails/gate-red-proofs.json:106-110` · `ARCHITECTURE.md:48` · `:50` · `:148` · `:150`.

**The two records this pass stands on.** `docs/prover/2026-07-28-requirement-302-findings-ratchet.md`
holds thirteen findings, of which F2 through F8 stand open by the owner's decision. This pass leaves
those seven where they are and files nothing that repeats them.
`docs/prover/2026-07-28-session-record-read.md` holds seventeen findings on Requirement 303, fifteen
folded and two carried to rows 523 and 524.

**Commands run.** Every claim below was taken from a run or from the file.

- `python3 guardrails/check-doc-findings-bound.py` — exit 0, "108 live documents, 16 held at zero".
- `python3 guardrails/check-handover-provenance.py` — exit 0, standing down by name over one handover
  dated before the counting start.
- `bash guardrails/check-prover-record.sh` — exit 1 before this record, which is the gate this pass
  answers.
- `python3 scripts/session-extract.py --list` — 183 transcripts under the transcript home name this
  repository.
- `python3 scripts/rule-census.py --json guardrails/rule-census.json` — exit 0, 108 files measured,
  4810 findings in all. No recorded total moved. The write refreshed byte counts and dropped the
  harvested inbox entry. This record sits under `docs/prover/`, which the census carves out, so the
  live set never reads it.
- Two probes on scratch trees, one per finding that needed one. Each is quoted inside its finding.

## Verdict

**The two laws are right, and three of tonight's machines stop short of their own text.**

The census now refuses to store a risen count, and that half holds under probe. The gate's document arm
holds 108 documents and 16 of them at zero. The handover gate reds a handover naming fewer than three
lines, and it stands down by name today.

The strongest hole is F1. Gate aa's second arm reads the record against the copy `HEAD` holds. At a
push and in the CI run, the working tree and `HEAD` carry one record, so the arm finds nothing to
compare. A ceiling raised by hand, committed, and pushed passes green. The arm bites on an uncommitted
edit alone, which is the one shape a push never carries.

Two further holes sit on the session-record side. The extractor takes the newest of 183 transcripts,
where criterion 10 asks for the closing session's own. And criterion 8 promises the extract lands
outside the repository, while `--out` takes any path and nothing refuses one inside the tree.

| # | Kind | Claim | Status |
|---|---|---|---|
| F1 | defect | Gate aa's record arm compares the working tree against `HEAD`, so a committed hand-raise passes at every push and in every CI run | open |
| F2 | defect | No criterion states the record arm, and "the arm" in criterion 11 has no antecedent, while M-482 claims a machine the spec never states | open |
| F3 | defect | The census writes the record before it reads whether a reading refused, so a refused reading lowers a ceiling and the ratchet makes that permanent | open |
| F4 | defect | Criterion 10 asks for that session's transcript, and the run takes the newest of 183 candidates by modification time | open |
| F5 | defect | Criterion 8 promises the extract lands outside the repository, and nothing refuses an output path inside it | open |
| F6 | recommendation | Row M-484 claims R303.11 through R303.24, and its tests reach neither the file-name shape nor the handover's body | open |
| F7 | recommendation | INV-302 spans two nodes on one code, where the nearest sibling mints a code per side | open |
| F8 | recommendation | The census report's heading carries a fixed date, so a report written today reads 2026-07-28 | open |

## Phase 1 — the model, as the delta leaves it

**The findings ratchet.** A live document is a markdown file outside the record directories and the
five record files. The record `guardrails/rule-census.json` holds one entry per live document. Three
states matter to the push: at or under its record, above it, and absent from it. The census writes the
record, and gate aa reads it. Tonight added a fourth actor: a person who edits the record by hand,
stating a reason.

**The session record.** A session transcript holds one session's whole traffic. A session extract holds
the person's own turns from one transcript. A session handover is a committed file under
`docs/handovers/` whose name ends in `-handover.md`. The closing step writes the extract, then the
handover. The opening step reads the previous handover and its extract.

**Actors.** A closing session spawns a fresh agent that writes the handover. An opening session spawns
a fresh agent that lists the person's decisions. Gate ab reads the handover's three provenance lines.
The seat holds the opening step, since a session's opening writes no committed artifact.

### What I assumed

- I read criterion 11's third bullet as describing the gate arm that shipped in `a6bd34b`. The bullet
  names "the arm" and the criteria introduce none, so F2 rests on that reading.
- I read criterion 10 of Requirement 303 as binding the extract to the closing session's own
  transcript. The words are "that session's transcript", and F4 rests on that reading.
- I treated the register-count hole as already owned by row 525, and I filed nothing for it.
- I found no criterion in either requirement that names which transcript a run selects among many.

## Phase 2 — the criteria against the machine that shipped

**What holds.** Criterion 9 holds: `scripts/rule-census.py:313-324` reads the record before it writes,
names every risen document, and returns 1 without writing. Criterion 10 holds on its stated path: a run
where nothing rose writes each measured count back. Criterion 11's first two bullets hold: the entry
carries a `reason` field, and `main` copies a recorded reason onto the entry it writes. The third
bullet holds: `committed_record` returns a note, and the gate prints "stands down".

On the session side, criteria 1 through 7 hold. `human_turns` skips a line carrying `toolUseResult`, a
sidechain mark, or a meta mark. `strip_wrappers` drops a wrapper-only turn and cuts a wrapper out of a
turn that keeps real words. Criterion 9's reach line prints the transcript, the turn count and both
sizes. Criteria 19 through 24 hold in `guardrails/check-handover-provenance.py`, and the vacuity guard
reads the declared handovers, so a directory of drafts alone reds.

**What the shipped record shows.** The record holds 109 entries and the live set holds 108. The extra
entry is `inbox/2026-07-28-from-tlvphotos-a-parked-question-stays-in-the-list-after-its-answer-arrives.md`,
the deposit harvested in `04f4a2f`. That entry names no live document and reds nothing, which is the
open F5 of the 302 record showing itself in the tree. The next record write drops it silently.

## Phase 3 — findings

F1 — Gate aa's record arm compares the working tree against `HEAD`, so a committed raise passes

> "never a ceiling raised by hand with no reason, and never a red on a tree whose record stands as HEAD
> holds it" — TEST_MATRIX.md, row M-482

The arm reads the record on disk and the copy `HEAD` holds, and it reports an entry whose count rose
between them. The gate runs from `guardrails/pre-push:232` and from `.github/workflows/gates.yml:100`.
At both of those moments the raise is already committed, so the two copies agree and the arm reports
nothing. A person raising a ceiling by hand, committing it, and pushing gets a green gate. The arm
reaches an uncommitted working-tree edit alone, and a push never carries one.

Probed on a scratch repository: a record committed with `total` 0, then raised by hand to 9 with no
reason and committed again. The gate printed "fell: CLEAN.md — recorded 9, measured 0" and then
"OK (doc-findings-bound): 1 live documents", exit 0. The fixture behind M-482 raises the count in the
working tree and never commits it. The test and the running gate therefore stand on different trees.

Compare the record against the push's base ref instead of `HEAD`.
`guardrails/check-prover-record.sh:40-49` already carries that ladder: `LIVE_SPEC_DIFF_BASE`, then
`origin/main`, then `HEAD~1`. Read the arm through the same ladder, and add a test that commits the
raise before the run. The second road runs the arm from `guardrails/pre-commit`, where the edit is
still uncommitted. That road leaves the CI mirror blind, so the base-ref road is the one I would take.

`defect · missing-outcome-check (postcondition)`

F2 — No criterion states the record arm, and criterion 11 names an arm the spec never introduces

> "*where* git holds no committed record, the arm stands down by name." — PRODUCT_SPEC.md,
> Requirement 302, criterion 11

Criterion 11 states that a raised count is a hand edit made under Requirement 297's rule. Its third
bullet then speaks of "the arm", and no criterion of Requirement 302 introduces one. A reader meets a
subject the document never named. Row M-482 meanwhile claims a whole machine. The gate asks git for the
record as `HEAD` holds it, compares each count, and reds a raise carrying no reason. A blocking gate
arm rides the push chain with no clause behind it, which is the code-with-no-spec-clause shape of the
three-source read.

Add one criterion to the case "the record moves only down", in these words:

> *if* a recorded count stands above the count the base commit holds and carries no reason, *then* the
> system *shall* refuse the push.

Put the stand-down bullet under that new criterion, where its subject exists. Criterion 11 then keeps
the hand-edit rule alone.

`defect · missing-rule (invariant)`

F3 — The census writes the record before it reads whether a reading refused

> "*when* the census writes the record and no live document stands above its recorded count, the system
> *shall* write each measured count back." — PRODUCT_SPEC.md, Requirement 302, criterion 10

`scripts/rule-census.py:329-332` writes the record. `scripts/rule-census.py:334` then computes which
rows refused, and line 335 returns 1. A run whose lint subprocess fails scores that reading 0, since
`measure` stores `style if style is not None else 0`. The lowered total reaches the record, the file is
written, and the exit code arrives after the damage. The ratchet then holds the lowered number as the
ceiling, and only a hand edit with a reason raises it back.

Probed against the shipped module, with `run_lint` returning a refusal. An entry recorded at total 7
was rewritten to total 0, the run printed "wrote ...record.json", and it exited 1. The written entry
even carries `'refused': 'the reading refused to run'`. The record therefore states that it was written
from a reading that never ran, and the gate compares `total` alone.

Move the refusal check above the `--json` write, and return 1 without writing when any row carries
`refused` or `unread`. That is the same shape criterion 9 already gives the risen case. Row 525 covers
the neighbouring path, where a check prints no count and scores 0 with no refusal at all. This finding
is the other path, and the two want one repair between them.

`defect · partial-success-risk (atomicity)`

F4 — The extractor takes the newest transcript, where the criterion asks for that session's own

> "*when* a session closes, the system *shall* run the extractor over that session's transcript before
> the handover is written." — PRODUCT_SPEC.md, Requirement 303, criterion 10

`scripts/session-extract.py:204` reads `taken = found[-1]`, and `candidates` sorts by modification
time, newest last. Criterion 3 says which files are taken, and no criterion says which one of them is
read. `python3 scripts/session-extract.py --list` printed 183 transcripts naming this repository. Two
of them were written within one minute of each other tonight, so the newest is decided by seconds. A
closing session on one lane picks up another lane's transcript, and its handover then reports another
session's decisions as its own. The lane law makes two live sessions a normal state, so this is the
ordinary case rather than the rare one.

Give the script a `--session ID` option that matches the transcript file named for that session, and
have the closing step pass its own identity. Refuse by name when the identity names no transcript. Then
state the selection rule as a criterion, so the document says which of many files a run reads.

`defect · missing-prerequisite (precondition)`

F5 — The extract's privacy promise rests on the caller's choice of path

> "The system *shall* write the session extract outside the repository, since a transcript holds private
> conversation." — PRODUCT_SPEC.md, Requirement 303, criterion 8

`scripts/session-extract.py:211` writes to whatever `--out` names, and no line refuses a path under the
repository root. The ignore rule added in `9477afb` covers the file name `session-extract-*.md` alone. A
closing agent that writes `--out docs/handovers/2026-07-29-extract.md` lands the person's own turns in
the tree, and the next commit carries them to a public remote. The criterion promises what the script
does not hold, and the owner is the person whose words leak.

Refuse an output path that resolves under the repository root, naming it and naming the reason. The
repository root is already computed at `default_repo()`, so the check is two lines. Keep the ignore
rule as the second net.

`defect · unenforceable-promise (discharge)`

F6 — Row M-484 claims fourteen criteria and its tests reach nine of them

> "A session handover's file name *shall* carry its date and its session identity, so two closes write
> two files." — PRODUCT_SPEC.md, Requirement 303, criterion 16

Row M-484 heads its fact with "(R303.11..R303.24)". Its nine tests hold the provenance arms, the
vacuity guard and the stand-down. Nothing there reads a file name for its date and its session
identity, and nothing reads a handover's body against criteria 17 and 18. Two sessions closing on one
day can write one file name, and the second overwrites the first with a green gate. The gate already
parses the date out of the name at `in_scope`, so the arm has its reader in hand.

Add a name-shape arm to gate ab and a test row for it, or narrow M-484's claimed range to the criteria
its tests reach. I would add the arm, since the overwrite it prevents destroys a committed record. The
302 record's F8 already names this class, where a row's claimed range runs wider than its tests. That
finding stands open, and this one is its sibling on the new requirement.

`recommendation · now · hard-to-operate (ops-ux)`

F7 — INV-302 spans two nodes on one code, where the nearest sibling mints a code per side

> "INV-302 (the two session steps sit in rule 35 beside the checkpoint and resume rules, and the closing
> step's mechanical arm, `guardrails/check-handover-provenance.py`, is the guardrails node's)" —
> ARCHITECTURE.md:48

The base-rulebook node owns INV-302, and the guardrails node pins the gate under that same code without
owning it. The nearest sibling splits the two: INV-298 carries the worker-restore rule on the
base-rulebook node, and INV-299 carries its mechanical arm on the guardrails node. A reader following
the ownership rule finds one code in one owns cell and its machine in another node's pins. Every fact
still has one owner, so nothing is broken; the two siblings answer one question two ways.

Mint an invariant for the gate arm and give it to the guardrails node, the way INV-299 sits beside
INV-298. The other road is to keep one code and state in the parenthetical why this pair differs from
that one. I prefer the split, since the matrix rows already separate the rule from its arm.

`recommendation · later · boundary-issue (composition)`

F8 — The census report's heading carries a fixed date

> `out = ["# Rule census — 2026-07-28", "",` — scripts/rule-census.py:255

The report's heading is a literal. `docs/audit/2026-07-28-rule-census.md` carries it today and reads
true. A report regenerated at any later date reads 2026-07-28 in its own first line, and a reader
takes the numbers for that day's. The audit directory is a record directory, so no gate measures the
page and nothing catches the stale line.

Write the heading from the run's own date. One call to `datetime.date.today().isoformat()` closes it.

`recommendation · later · hard-to-monitor (observability)`

## The mandatory sweeps over the delta

The whole-document sweeps of a full pass are out of scope for a cross-link mode. The sweeps below were
run over the delta's own surfaces, and each verdict names what it read.

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The findings ratchet, R302.9-11 | clean — INV-301 names gate aa as its net, wired and red-proofed | hit — F3, the refused reading at the write path | hit — F1, the ceiling law's other three records hold no committed-copy arm, and row 520 owns the merge | clean — the record's states are stated | hit — F2, the arm with no clause |
| The session extract, R303.1-10 | clean — INV-302 names gate ab for the closing step | hit — F4, the selection among many candidates | clean — no sibling extractor | N/A — the script holds no state between runs | hit — F5, the output path inside the tree |
| The handover gate, R303.11-24 | clean — the gate is named, wired and red-proofed | clean — the counting start and the empty set both answered | clean — the vacuity shape matches its siblings | hit — F6, two closes on one day | clean |
| The opening step, R303.25-31 | clean — criterion 31 states why no gate holds it | clean — the missing-extract case is criterion 27 | clean | clean — the entry and exit are stated | clean |

**The quantifier re-verify (INV-170).** Six enumerations were re-read against the delta. The glossary
now carries both new terms, at PRODUCT_SPEC.md:211 and :212. The base rulebook's rule count reads
thirty-five in its own description and its body ends at rule 35. The gate letters run to ab in
`guardrails/pre-push`, in the CI mirror and in `guardrails/gate-red-proofs.json`, with no roster left
behind. INV-301's row list in the matrix carries M-479 through M-482, and INV-302's carries M-483
through M-485. The formal index carries R303.1 through R303.31 under INV-302. One enumeration fails:
row M-484's claimed criterion range, which is F6.

## Phase 3.5 — acknowledged gaps

Requirement 302 and Requirement 303 carry no open item, no marked decision and no rhetorical question.
The queue holds the gaps their prover passes named: rows 520, 523, 524 and 525. Row 525 states that the
register column reads zero for every recorded document, because that reading never produced a count.
The row says its repair covers the class. This pass read that row as owning the no-count path, and F3
names the refused-reading path beside it.

## Phase 4 — human and operational factors

**Privacy.** F5 is the privacy finding of this pass. A transcript holds the person's own conversation,
and the criterion that keeps it out of the tree rests on the caller's discipline. The repository is
public, so a committed extract reaches strangers.

**What an operator sees.** Gate aa's green line names the count of live documents, the count held at
zero and the word cap. Gate ab's green line names the directory, the file count, the handovers, the
in-scope count and the counting start. Both read well from a push log.

**Scale.** The census runs two lint subprocesses over 108 documents, which took several minutes in this
pass. The number of live documents grows with the tree, and nothing states a ceiling for that run's
time. The suite budget check owns wall time for the suite; this gate sits on the push chain instead.

## Phase 5 — closing

**Three to fix before the next landing on these requirements.** F1, because the second arm of gate aa
passes on every real push. F3, because a failed reading lowers a ceiling the ratchet then holds. F5,
because a private transcript can reach a public tree.

**Properties the documents should state.**

- A recorded count that stands above the count the base commit holds carries a reason beside it.
- A run that writes the record writes only counts every reading produced.
- A closing session's extract is read from that session's own transcript, named by its identity.

**Open questions for the owner.** Whether the handover's file-name shape earns a gate arm now or waits
for row 524's retention work. Whether F7's split is worth a new invariant code.

**Queued for a taste call.** F6, F7 and F8.

**Readiness.** The push gate's record demand is met by this file. The tree's other gates read green.
Requirement 302 and Requirement 303 each need another iteration, and the five defects above owe queue
rows before the next landing on either one.
