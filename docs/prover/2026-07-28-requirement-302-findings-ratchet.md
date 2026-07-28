# Prover record — Requirement 302, the per-document findings ratchet, 2026-07-28

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK over one added requirement, plus
the whole-document quantifier re-verify (SPEC INV-170). Written by a seat that authored none of this
work (SPEC INV-237).

## Scope

**What this record reviews.** Commit `84f74bd`, and one requirement inside it. Requirement 302 reads
"A document repaired to zero stays at zero, and every other count moves down alone". It carries INV-301
and eight acceptance criteria. The requirement claims a shipped machine, so the pass reads that machine
beside the text:

- `guardrails/check-doc-findings-bound.py` — gate aa, the refusal;
- `guardrails/rule-census.json` — the record of counts, 107 documents, 15 of them at zero;
- `scripts/rule-census.py` — the measure both the gate and the report read through;
- `tests/test_doc_findings_bound.py` and `TEST_MATRIX.md` row M-479 — the coverage;
- `guardrails/pre-push:231`, `.github/workflows/gates.yml:100`, `guardrails/gate-red-proofs.json:106`
  — the wiring;
- `ARCHITECTURE.md:148` and `:150` — the owning node and its pins.

**Two siblings this record reads for comparison.** Requirement 297's criteria 13 through 18 hold the
criterion-readability ratchet. Requirement 245's criteria 1 through 4 hold the growable-doc bounds.
This pass judges neither of them, and F1 rests on the difference.

**The tree moved while this pass ran.** `scripts/rule-census.py` gained an interpunct-roster carve-out
from another session, and `guardrails/rule-census.json` was re-seeded three counts lower. The verdict
below judges the requirement as committed at `84f74bd` against the machine as it stands. The live
record shows zero raised counts against HEAD, so the hole F1 names is unexercised so far.

**Commands run.** `python3 guardrails/check-doc-findings-bound.py` on the live tree. It exits 1 at
23:05, on one document another session added during this pass:
`docs/plans/2026-07-28-two-goals-one-campaign.md` carries no entry in the record. That is criterion 6
refusing in the wild, and the run prints the 15 held-clean documents beside it. Six further probes ran
on one-document trees under a scratch root. Each probe is quoted inside the finding it proves.

## Verdict

**The law is right and the machine holds one half of it.** The gate refuses a rise on every push. It
rides the pre-push chain and the CI mirror. It carries a registered red proof, and it refuses an empty
live set by name. The requirement's own arrival was refused by it, which is a red-first proof taken in
the wild.

The other half is open. The record is the ceiling, and nothing holds the record itself. One printed
command rewrites every entry to whatever the text measures today, upward included, and the gate prints
that command itself. The nearest sibling already states the three criteria that close this. It is the
criterion-readability ratchet at Requirement 297. No run raises a recorded count. A rebaseline runs
only when nothing stands above its record. A raise is a hand edit carrying its reason. Requirement 302
copies that sibling's first three criteria and stops before those three.

Three further roads lower a count with every gate green. A reading that fails to run scores zero. A
looser word cap in the rule home shrinks every count. A document leaves the live set by moving under a
carved-out directory prefix. The term "live document" carries the whole law and sits in two Python
tuples.

| # | Kind / severity | Claim | Status |
|---|---|---|---|
| F1 | defect / must-fix | The ceiling has no direction: `rule-census.py --json` rewrites every entry upward, and the gate prints that command | OPEN |
| F2 | defect / must-fix | The word cap the record was measured under is recorded and never compared, so loosening rule r08 slackens every ceiling | OPEN |
| F3 | defect / must-fix | A reading that fails to run counts as zero findings, and the gate reads the lowered total as the truth | OPEN |
| F4 | defect / must-fix | "Live document" is defined by two tuples in `scripts/rule-census.py`, matched by prefix, and stated in no criterion | OPEN |
| F5 | defect / must-fix | Criterion 6 covers a live document with no entry; a record entry with no live document never reds | OPEN |
| F6 | defect / must-fix | Criterion 8's reach line is printed on the pass path alone; every refusal states no reach | OPEN |
| F7 | defect / must-fix | Criterion 5 prints a command and imposes no duty, so a fall leaves headroom nobody must record | OPEN |
| F8 | defect / must-fix | Criterion 7's branch and criterion 3's message are covered by no test, and M-479 claims both | OPEN |
| F9 | recommendation / should-fix | The Fix line prints an empty file name when only unrecorded documents red | OPEN |
| F10 | recommendation / should-fix | The spec sits at 1831 of 1831, so the growth consequence deserves a stated sentence | OPEN |
| F11 | recommendation / should-fix | Eleven gate fixtures sit in the live set while two other fixture roots are carved out | OPEN |
| F12 | recommendation / later | The cleared-document refusal omits the recorded count criterion 3 asks for on every rise | OPEN |
| F13 | recommendation / later | The record holds five numbers per document and the gate compares one | OPEN |

## Phase 1 — the model

**Entities.**

- **A live document** — a markdown file under the repository root, outside the record directories and
  the five record files. 107 stand today.
- **A record entry** — one object per live document in `guardrails/rule-census.json`, carrying `file`,
  `bytes`, `long`, `longest`, `style`, `register`, and `total`. The file also carries `cap` and
  `cap_rule` at its top level.
- **A reading** — one of three measures over a document: `long` (sentences past the word cap), `style`
  (`scripts/spec-style-lint.py --tier full`), and `register` (`scripts/preshow-register-lint.py`).
  Their sum is the document's finding count.
- **The word cap** — rule r08's `human_prose_flag_above_words` in `guardrails/language-rules.json`,
  read fresh on every run. It stands at 25.
- **The gate** — `guardrails/check-doc-findings-bound.py`, gate aa, run from the pre-push chain and
  from the CI mirror.

**States of a live document.** *Held clean* — recorded at zero and measuring zero. It exits to *risen*
on its first finding. *Under its ceiling* — measuring below its record; it
exits to *at its ceiling* once the lower number is recorded. *At its ceiling* — measuring exactly its
record. *Risen* — measuring above its record, which is the one state that refuses a push. *Unrecorded*
— live with no entry, which also refuses. A document also leaves the live set entirely by moving, and
that transition is stated nowhere (F5).

**Actors.** A writer edits a document. The gate measures and refuses at every push. A person runs
`scripts/rule-census.py --json` to rewrite the record, and that person is the only actor who moves a
ceiling. The rule home's owner sets the word cap, and that edit reaches every count (F2).

**Composition.** The guardrails node owns INV-301 and pins all four files. The measure reads its cap
out of the language-rule home, so Requirement 300's data file sits under Requirement 302's verdict. The
record is a third ceiling in this repository. Its siblings are the growable-doc bounds (INV-234,
Requirement 245), the bytes-per-criterion ratchet (INV-264, Requirement 280), and the
criterion-readability counts (INV-288, Requirement 297).

### What I assumed

- I read "the record is the ceiling" as binding the record file as well as the documents. A ceiling
  that any run may raise is a ceiling in name alone, and F1 rests on that reading.
- I read a "finding" as the sum of the three readings, since the record's `total` is that sum and the
  gate compares `total` alone.
- I treated the interpunct carve-out landing in `scripts/rule-census.py` during this pass as another
  session's in-flight work, and I judged nothing about it.
- I found no authoritative surface in this requirement for the measure's own definition. The three
  readings, the carve-out lists, and the sentence splitter live in one script that no criterion
  describes.

## Phase 2 — the criteria against the machine that shipped

**What the machine carries.** Criterion 1 holds: the record is one entry per live document, keyed by
path, 107 entries with no duplicate. Criterion 2 holds at the push: `guardrails/pre-push:231` runs the
gate, and `.github/workflows/gates.yml:100` mirrors it. Criterion 3 holds on the non-zero branch, which
prints the document, its recorded count, and its measured count. Criterion 4 holds and names the
document as one already cleared. Criterion 6 holds and names the unrecorded document. Criterion 7 is
met by the code, through a path Phase 3 reads. Criterion 5 and criterion 8 are each half met, in F7 and
F6 below.

Two pieces of the delivery are worth recording as done well. The gate imports the census module and
measures through it, so the report and the refusal can never drift apart in method. And the gate
refuses an empty live set by name, which is the INV-218 shape held properly.

### F1 — the ceiling has no direction, and the gate prints the command that raises it

> "The record of counts is the ceiling, and the direction of every count is down." — Requirement 302 /
> Context

`scripts/rule-census.py:283` writes `{r["file"]: r for r in rows}` for every measured document, with no
comparison against what the record already holds. The gate prints that command as its own remedy on a
fall (`guardrails/check-doc-findings-bound.py:101`). So the operator whose push was refused has, in the
refusal itself, the one command that turns the refusal into a pass.

Proved on a one-document tree. A document recorded at zero, carrying one over-cap sentence, reds with
"CLEAN.md was repaired to zero and now carries 1 finding(s)". Re-seeding the record exactly as
`--json` writes it turns that red green. The gate then gives exit 0 and "1 live documents, 0 held at
zero, none above its record". The law survives today on habit alone, and the live record shows no
raised count against HEAD.

The sibling ratchet already states the repair. Requirement 297 carries it in three criteria, and this
requirement copies the first three of that sibling's six and stops. Write the missing three here, in
the same shape:

> 9. No run *shall* raise a recorded count. [INV-301]
> 10. *when* the census writes the record and no live document stands above its recorded count, the
>     system *shall* write each measured count back. [INV-301]
> 11. A raised recorded count *shall* be a hand edit to the record stating its reason, run through this
>     same pipeline. [INV-301]

The mechanical arm reads the record against its committed version and reds any entry whose number rose
with no reason beside it. Requirement 245's own bound file carries a `reason` field per entry, so the
shape exists in this repository already.

`defect · missing-rule (invariant)`

### F2 — the cap the record was measured under is recorded and never read

> "Each run *shall* state its reach: the count of live documents read, the count held at zero, and the
> word cap it measured against." — Requirement 302, criterion 8 / Case: nothing ships unmeasured

`guardrails/rule-census.json` carries `cap: 25` and `cap_rule: "r08"` at its top level. The gate loads
the record's `files` key alone (`guardrails/check-doc-findings-bound.py:64`) and takes its own cap from
`guardrails/language-rules.json` through `census.load_word_cap()`. The two are never compared.

Proved: a record declaring `cap: 5` and `cap_rule: "r99"`, measured against a live cap of 25, passes
with "OK ... (cap 25, rule r08)". Raising rule r08's threshold to 40 would drop the `long` reading of
every document at once. Every count falls, every fall is lawful, the re-seed records the lower numbers,
and the ratchet is permanently slackened with no gate red anywhere. The same class reaches the other
two readings, whose definitions live in two lint scripts under no ceiling of their own. The
interpunct carve-out that landed during this pass is that class in motion.

> 12. *if* the recorded word cap or its rule differs from the rule home's, *then* the system *shall*
>     refuse the push and *shall* name both numbers. [INV-301, INV-292]

`defect · unenforceable-promise (discharge)`

### F3 — a reading that fails to run scores zero findings

> "*when* a push runs, the system *shall* measure every live document and *shall* compare each count
> against its recorded count." — Requirement 302, criterion 2 / Case: the record is the ceiling

`run_lint` in `scripts/rule-census.py:180` returns a count off the lint's own JSON record line. A lint
that starts and exits without that line falls through to the fallback at line 197, which returns zero
findings and no error. A lint that fails to start raises `OSError`, which sets a `refused` key. The gate
never inspects that key, and it tests for `unread` alone at line 80. The census script's own `main`
returns 1 on a refusal. The gate imports the module and calls `measure` directly, so that refusal runs
nowhere.

Proved on a live file: `SURFACES.md` measures 3 with the style lint in place, and 1 with the style
lint's path broken. No key on the row marks the difference. A style lint that crashes on a syntax error
drops every document's count. Every document then reads as fallen, and a re-seed writes the hollow
numbers in as the new ceiling.

> 13. *if* any reading over a document fails to produce its count, *then* the system *shall* refuse the
>     push and *shall* name the document and the reading. [INV-301, INV-218]

`defect · missing-outcome-check (postcondition)`

### F4 — the term that carries the law is defined in two Python tuples

> "The system *shall* hold one recorded finding count per live document in
> `guardrails/rule-census.json`." — Requirement 302, criterion 1 / Case: the record is the ceiling

The requirement uses "live document" four times and defines it nowhere, and the spec's glossary carries
no entry for it. The definition is `RECORD_DIRS` and `RECORD_FILES` at `scripts/rule-census.py:52`
and `:60`. Line 98 asks `os.path.join(rel_dir, d).startswith(RECORD_DIRS)`, which compares the head of
a path against every carved-out name.

Proved on a scratch tree holding five documents. `attic-new/b.md`, `docs/reports-2026/c.md`, and
`docs/researchers/d.md` all fall out of the live set, because their directory names start with
"attic", "docs/reports", and "docs/research". A person who creates any such directory removes its
documents from every count, and no output names what was dropped.

Two repairs. Write the definition into the requirement, and name the carve-out as a class. A document
recording something that happened at a moment stands outside the live set, and every other markdown
file stands inside it. Then compare a directory against the whole carved-out path, so a name that
merely starts with a carved-out name stays measured.

> 14. A live document *shall* be every markdown file in the repository outside the directories that
>     hold a dated record of something that happened. [INV-301]
> 15. Each run *shall* name the count of files it passed over as records. [INV-301, INV-269]

`defect · over-general (abstraction)`

### F5 — a record entry outliving its document is the unstated half of criterion 6

> "*if* a live document carries no entry in the record, *then* the system *shall* refuse the push and
> *shall* name that document." — Requirement 302, criterion 6 / Case: nothing ships unmeasured

The gate walks the live set and looks each file up in the record. It never walks the record and looks
each entry up in the live set. So an entry for a document that left the tree, or moved under a
record directory, stands forever and reds nothing.

That leaves repair-by-relocation open. A page carrying 112 findings moves to `docs/reports/`, the gate
greens, the count leaves the census, and the stale entry is the only trace. Nothing reads that trace.
The same road covers a plain deletion, where a stale entry is harmless and still worth naming.

> 16. *if* the record carries an entry naming no live document, *then* the system *shall* name that
>     entry and *shall* refuse the push until the entry is removed. [INV-301]

`defect · missing-scenario (state-space)`

### F6 — the reach line is printed on the pass path alone

> "Each run *shall* state its reach: the count of live documents read, the count held at zero, and the
> word cap it measured against." — Requirement 302, criterion 8 / Case: nothing ships unmeasured

Those three numbers are printed inside the `OK` line at
`guardrails/check-doc-findings-bound.py:104`, which is reached only when nothing rose and nothing is
unrecorded. Every refusal prints the failing documents and stops.

Proved: the red output on a cleared document reads "FAIL ... A cleared document stays cleared", the
per-reading line, and the Fix line. No document count, no held-at-zero count, no cap. The live tree's
own red at 23:05 reads the same way. The operator reading a refusal cannot tell whether the run covered
107 documents or four, which is the exact question a refusal raises. INV-269 asks each run for its
reach, and a run is a red as much as a green.

Move the reach line above the verdict branch, so it prints on both paths.

`defect · hard-to-monitor (observability)`

### F7 — a fall states a print where the law needs a duty

> "*when* a document's count falls below its recorded count, the system *shall* pass that document and
> *shall* print the command that records the lower count." — Requirement 302, criterion 5 / Case: a
> fall tightens the ceiling

The case is titled "a fall tightens the ceiling", and the criterion tightens nothing. It passes, and it
prints a command that a person may run or skip. Between the fall and a re-seed, the gap between the two
numbers is headroom. Every new finding inside that gap ships green.

`ROADMAP.md` stands at 215 today. A repair pass taking it to 100, with no re-seed, leaves 115 findings
of room that the next writer spends without a single red. The law's own sentence, that every count
moves down alone, is false across that window.

> 5. *when* a document's count falls below its recorded count, the system *shall* pass that document,
>    and the landing that lowered it *shall* record the lower count in the same commit. [INV-301]

The arm is the same one F1 needs: the record read against its committed version, redding a fall that
was measured and never written down.

`defect · missing-outcome-check (postcondition)`

### F8 — two criteria are claimed by a matrix row and reached by no test

> "... an empty record reds rather than passing over nothing; each run states the documents read ..." —
> `TEST_MATRIX.md`, row M-479

`test_an_empty_record_reds_rather_than_passing_on_nothing` writes `{"files": {}}` into a temporary
directory holding no markdown file. The gate reds there on the empty-live-set branch, which prints
"the live set came out empty". Criterion 7's own branch is never reached. Re-running that scenario with
one document present shows the real behaviour. The gate reds through the unrecorded path, one line per
document, and it names no empty record.

`test_gate_reds_a_document_above_a_non_zero_record` seeds a recorded total of 0, so it repeats the
red-first case above it. One branch prints "rose from %d to %d", and that is the only place criterion
3's three numbers appear together. No test in the suite exercises it.

Fix the two fixtures. Seed the empty-record case with a document present, and assert a message naming
the empty record. Seed the second case with a recorded total of 1 against a document measuring 2. Add
a criterion-8 assertion over the red path once F6 is folded.

`defect · missing-outcome-check (postcondition)`

## Phase 3 — property analysis

**Safety.** The stated invariant is that no document's count ever rises. It holds over the documents
and fails over the record, in the four ways F1 through F4 name. Each of them lowers a number with every
gate green. Three need no bad intent at all: a crashed lint, a widened cap, and a renamed directory.

**Atomicity.** The gate measures 107 documents through 214 subprocess runs and refuses the push as one
verdict, so no half state is observable. The re-seed is the opposite case. It re-measures the whole
live set at a later moment than the gate's own reading. The number recorded is the number the text held
at re-seed time. No criterion ties the recorded number to the reading that justified it.

**Liveness.** No document state is a dead end. A refused push always has a road out: repair the text,
or record a lower number. The state that carries no road is the one F7 names, where a fallen count
waits on a person to notice.

**Enforceability.** Criterion 2 promises that a push measures every live document. The gate returns at
the first unreadable file (`guardrails/check-doc-findings-bound.py:80-82`), so a single unreadable
document leaves the rest unmeasured. The refusal is right and the enumeration stops early, which
matters once a run reports its reach on the red path.

**Overlapping data.** The record holds five numbers per document and the gate compares one. A document
that trades a style finding for an over-cap sentence holds its total, passes, and its recorded shape is
now wrong in two columns. Nothing states whether the four sub-counts bind (F13).

## Phase 3e — mandatory sweep verdicts

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The requirement text (R302) | hit — INV-301 names gate aa as its net, and the net covers the documents alone (F1) | hit — the fall end of the range states a print and no duty (F7) | hit — F1, three of Requirement 297's six ratchet criteria are missing here | N/A — the text holds no state | hit — F4, "live document" is defined in no criterion |
| `guardrails/rule-census.json` (the record) | hit — the record is a declared bound outside Requirement 245's reason law | hit — F2, the recorded cap and the live cap may differ without bound | hit — Requirement 245 requires a reason per bound; this record carries none | hit — F5, an entry outliving its document has no exit | clean |
| `guardrails/check-doc-findings-bound.py` (gate aa) | clean — INV-301 owns it, `gate-red-proofs.json:106` registers its red | hit — F6, the reach line stands on the pass path alone | clean — the pre-push chain and the CI mirror both carry it | N/A — the gate holds no state across runs | hit — an unreadable file ends the walk early |
| `scripts/rule-census.py` (the measure) | hit — the measure's definition is under no criterion | hit — F3, a reading that fails to run scores zero | hit — F4, the carve-out is matched by prefix and two fixture roots are missing from it | N/A | hit — F11, gate fixtures are measured as live prose |

**Quantifier re-verify (SPEC INV-170).** Four sentences fired. "A document repaired to zero is held at
zero on every push, without exception" is falsified by F1 through F4. Each of those four lowers a
number with every gate green. "The direction of every count is down" is falsified by the re-seed's own
write path (F1). "measure every live document" is narrowed by the prefix carve-out (F4). "Each run
shall state its reach" is false on every red (F6). Two sentences re-verified clean: the record holds
exactly one entry per live document, and the gate refuses an empty live set by name.

Create-read-update-delete and authorization tables are N/A here. The product is a method pack with one
operator and no user-mutated persistent entity. The surface-by-sweep table above stands in their place
(SPEC INV-171).

## Phase 3.5 — acknowledged gaps

Requirement 302 carries no Open Item, no TBD, and no unanswered question in its body. The commit
message names one thing the requirement leaves out. The gate refused its own arrival, and the prose
was repaired until the spec returned to 1831. That episode is recorded in the
journal, and the requirement itself states none of it. F10 asks for that sentence.

`acknowledged · missing-rule (invariant)`

## Phase 4 — human and operational factors

**What an operator sees.** A refusal names the document, the two numbers, and the three readings that
make up the count. That is a good message, and it points at the census command that lists each finding.
Two rough edges sit beside it: the missing reach line (F6), and the Fix line's empty file name when
only unrecorded documents red (F9).

**The scale of the refusal.** An empty record against the live tree prints 107 refusal lines. One line
lands per document, and the Fix line then names no file. The single sentence criterion 7 asks for would
replace all of it.

**Domain language.** The gate's own output speaks the product's words: held clean, fell, rose, cleared.
No internal identifier leaks into it. The record's field names stay inside the data file.

**Cost.** The run measures 107 documents through 214 subprocess calls on every push, in roughly seven
seconds by the commit's own note. That number grows with the document count, and it carries no declared
budget. Requirement 245 governs document bytes and leaves this run time alone.

### F9 — the Fix line names no file when only unrecorded documents red

`guardrails/check-doc-findings-bound.py:120` builds its last line from `rose[0][0] if rose else ""`, so
a run whose only refusals are unrecorded documents prints "read `python3 scripts/rule-census.py `".
The live tree printed exactly that line at 23:05. The operator is handed a command with its argument
missing. Print the re-seed command on that path instead, since recording the document is the remedy.

`recommendation · now · hard-to-operate (ops-ux)`

### F10 — the growth consequence deserves a stated sentence

`PRODUCT_SPEC.md` is recorded at 1831 and measures 1831, so its headroom is zero. The ceiling holds a
count of findings, so it gives a growing document no allowance. Every new requirement must add no
over-cap sentence, or repair an old one in the same landing. That is what happened when this
requirement landed. A session that meets the red
without that sentence reads it as a bug in the gate.

Add one line to the Context: a document at its ceiling grows only by repairing existing prose in the
same landing.

`recommendation · now · confusing-for-users (cognitive-load)`

### F11 — gate fixtures are measured as live prose

Eleven files under `guardrails/far-tier-fixtures/` and `guardrails/release-note-fixtures/` sit in the
record, all at zero. `guardrails/board-fixtures/`, `guardrails/authority-anchor-fixtures/`, and
`tests/fixtures/` are carved out. So the next gate whose fixtures are markdown must either write them
in clean prose or add a directory to a tuple in `scripts/rule-census.py`. A fixture built to carry a
defect on purpose would red gate aa on arrival. Carve out fixture roots as a class, by the directory
suffix the three carved-out names already share.

`recommendation · now · boundary-issue (composition)`

### F12 — the cleared-document refusal omits its recorded count

Criterion 3 asks every refusal to name the document, its recorded count, and its measured count.
Criterion 4's case is a subset of criterion 3's, and its message reads "was repaired to zero and now
carries 1 finding(s)". That message names the recorded count in words, and criterion 3 asks for the
number. Either print the number too, or scope criterion 3 to a non-zero record.

`recommendation · later · internal-conflict (consistency)`

### F13 — the record's other four numbers bind nothing

Each entry carries `bytes`, `long`, `longest`, `style`, and `register` beside `total`, and the gate
compares `total` alone. A document that trades a style finding for an over-cap sentence holds its total
and passes, and its recorded shape is wrong in two columns. State which numbers bind: either the gate
reds a risen sub-count, or the record says the four are informational.

`recommendation · later · boundary-issue (composition)`

## Phase 5 — closing

### Top three to fold

1. **F1** — give the record a direction. Requirement 297's criteria 16 through 18 are the wording, and
   the arm reads the record against its committed version.
2. **F3 and F2 together** — a count is trustworthy only when every reading ran and the cap held. Both
   roads lower a number today with every gate green.
3. **F4 and F5** — define "live document" in the requirement, and red an entry that outlives its
   document, so relocation stops working as a repair.

### Properties to state in the document

- No run raises a recorded count, and a raise is a hand edit stating its reason.
- The recorded word cap and the rule home's word cap are the same number, or the push is refused.
- A count stands only when all three readings over that document produced a number.
- A live document is every markdown file outside the directories holding a dated record of something
  that happened.
- A record entry naming no live document is refused until it is removed.
- The landing that lowers a document's count records the lower count in the same commit.

### Open questions for the author

1. May a document leave the live set at all? Moving one under `docs/reports/` is a lawful edit today
   and it discharges the ceiling. F5's criterion assumes the answer is no.
2. Should the four sub-counts bind, or stand as information beside the total? F13 waits on that.
3. Should a fixture root be carved out as a class? F11 proposes the suffix rule, and the call is
   yours.

### Recommendations queued for a taste call

F9, F10, F11, F12, and F13, in the shapes above. F10 is the one worth taking first, since it costs one
sentence and it saves the next session a wrong reading of a red.

### The `[default]` count

This is a CROSS-LINK pass over one requirement, so the whole-document default sweep stands down. The
requirement itself carries no `[default]`-tagged sentence.

### Readiness

The law is right and the machine holds the documents. Needs another iteration: fold F1 through F8, and
the record becomes a ceiling in fact as well as in name.
