# Prover record — ADDENDUM to the 2026-07-27 push gate (the three new requirements, their node, their matrix rows, and the two queue corrections), 2026-07-27

**This is an addendum. It reviews only the delta that landed after the day's first record.** The first
record is `docs/prover/2026-07-27-push-gate.md` — a CROSS-LINK pass with the architecture lens over
`d7400d8..6b11c7e`, verdict LANDS WITH FIXES on findings F1–F8. Everything it covered is covered there and
is not re-argued here. PRODUCT_SPEC.md changed after that record was written, so the push gate wants a
review record that post-dates the change; this file is that record, and it stands on top of the first
rather than replacing it.

Prover skill: product-prover, live-spec pack v4.3.0. Mode: delta-focused with the architecture lens.
Reviewed by a seat that authored none of the work (SPEC INV-237).

**Scope — what this addendum reviews.** Two commits:

- `10dd65b` (both chat hooks get their real reach) — `hooks/affirmation-scan.py` now reads the whole turn
  through `hooks/turn_reader.py` instead of the last message alone, and `hooks/code-anchor-scan.py` gained
  this repository's own citation idioms plus a carve-out for a reference to a line inside a source file.
  Both are the fold of the first record's F6 and part of its F4.
- `7b7d953` (the three new mechanisms get their requirement, their node and their matrix row) — the fold
  of the first record's F2 and F8. Requirements 292, 293 and 294 appended with the generated reference
  table and `PRODUCT_SPEC.index.md` rebuilt; the guardrails node gained INV-282/283/284 in its owns list
  and five pins; TEST_MATRIX.md gained M-458, M-459 and M-460; the snapshot row reopened from the archive
  and the two lane rows flipped back to queued.

**Scope — what neither record covers.** Three commits sit between the first record and this delta and are
reviewed by no record: `7818f66` (the queue correction that also wrote the first record into the tree),
`27d8856`, `1f2fd51` and `c545b20`. All four touch NEXT_STEPS.md, ROADMAP.md and the archive only, and
`7818f66`'s two substantive moves were both reversed inside this delta, so the material reaches this
record through what it reversed. No spec, architecture, matrix or code change hides in that stretch.

**Verdict: LANDS WITH FIXES — the push waits on A1–A4.** Four must-fix defects, five should-fix, one note.
The delta does what its commit message claims: three mechanisms that shipped owned by nothing now carry a
requirement, an architecture entry and a matrix row each; the matrix rows name real tests that assert the
stated facts (26 of them, all green, re-run here); the first record's F3 and F4 are folded outright (every
fixture payload now carries a relative transcript path, and `tests/test_affirmation_arm.py` exists with ten
tests holding both directions). What the delta does not carry is agreement between the three new
requirements and the code they describe. One criterion (R292.6) is implemented nowhere and is false today
against the shipped registry; one requirement (R294) describes the reach the affirmation scan had before
this same delta widened it; and the architecture's own shared-reader pin still names three consumers where
the tree holds five.

| # | Kind / severity | Claim / evidence | Folded / open |
|---|-----|--------------------------|-----|
| A1 | defect / must-fix | R292.6 and R292.1 are false against the shipped registry and mechanized nowhere: `clock-hook.sh` and `chat-law-hook.sh` are wired session hooks classified in neither map, and nothing reds | OPEN |
| A2 | defect / must-fix | R294 and M-460 state the affirmation scan reads the reply the person receives; `10dd65b` in this same delta made it read the whole turn, and INV-281's index row does not carry R294 | OPEN |
| A3 | defect / must-fix | The guardrails node's `turn_reader.py` pin names three nets reading through the shared reader; five files import it after this delta | OPEN |
| A4 | defect / must-fix | The mid-turn-reach bug row (row 482) sits in the archive at `*queued*` while this delta ships its remaining half; the same archive-stray class was corrected for row 55 in this commit and left standing for row 482 | OPEN |
| A5 | defect / should-fix | R293 states no criterion for three shipped behaviours: the document-name form, the spaced multi-letter code form, and the source-line carve-out that makes the scan pass | OPEN |
| A6 | defect / should-fix | The code-anchor patterns compile case-insensitively, so `act 3`, `b-2` and `f-16` red as internal codes; no criterion and no test covers the false-positive direction for the shapes the net added | OPEN |
| A7 | defect / should-fix | Row 55's reopened cell reads all three acceptance legs MET while its own reopening note says the third leg has no owner — one cell denying itself, against the whole-close law | OPEN |
| A8 | defect / should-fix | `guardrails/hook-red-proofs.json`'s affirmation-scan entry carries a `source_fallback` note saying no repo copy exists under `hooks/`; one exists and the runner proves it, printing no fall-back note | OPEN |
| A9 | defect / should-fix | R292 and R293 state no criterion for the stand-downs both hooks ship (an active stop hook, an unreadable transcript), though M-460 names one of them as a covered fact | OPEN |
| N1 | note | R292 states nothing about where the runner runs; the architecture and the matrix both say it rides the suite, which answers the first record's F8 outside the spec | OPEN |

## A1 — The registry law reds nothing, and is false today

> "The system *shall* classify every session hook in a red-proof registry" — R292.1; and "*if* a hook
> shipped under the pack's hooks directory is classified in neither map, *then* the system *shall* red it
> by name." — R292.6 [INV-282, INV-211]

`guardrails/check-hooks-can-fire.py` reads `hook-red-proofs.json` and walks the two maps it declares. It
lists no directory. There is no code path in the runner, and no test in
`tests/test_check_hooks_can_fire.py` (three tests: a stub hook that never fires, a fixture carrying no
trigger, and the census over the real fixtures), that asks whether a file under `hooks/` appears in either
map. The law lives as prose in the registry's own `_comment` field, which states the finding exactly and
mechanizes nothing.

The gap is not hypothetical. `guardrails/judge-hooks.json` classifies nine hooks as wired live, and two of
them — `clock-hook` (UserPromptSubmit) and `chat-law-hook` (UserPromptSubmit) — appear in neither
`proofs` nor `cannot_red`. They are live session hooks by the pack's own declaration, running on every
prompt in every adopting host, with no proof that they still fire and nothing that notices. R292.1 says
every session hook is classified; today seven are.

A second edge sits inside the criterion's own wording. Taken literally, "a hook shipped under the pack's
hooks directory" reaches `turn_reader.py`, `register_judge_core.py` and `conduct-law.md`, which are a
shared reader, a shared mechanism and a prose file. `judge-hooks.json` already owns the discrimination the
criterion lacks: a `library` list for a file another hook invokes or a host opts into. R292.6 needs that
carve-out named, or it reds seven lawful files on the day it is implemented.

Either write the census the criterion promises — reading `judge-hooks.json`'s wired list as the population
and its library list as the carve-out, with `clock-hook.sh` and `chat-law-hook.sh` given fixtures or a
recorded `cannot_red` reason — or narrow R292.1 and R292.6 to the population the runner actually walks and
open a row for the two unproven wired hooks. A criterion that describes a check nobody wrote is the exact
shape the first record's F2 named one commit earlier.

`defect · missing-rule (invariant)`

## A2 — The requirement describes the reach the code had before this delta

> "*when* the reply the person reads carries an empty-validation phrase from the pattern list, after a
> quoted, backticked, or fenced span is stripped, the system *shall* block the stop" — R294.1 [INV-284,
> INV-238]; and M-460: "the Stop hook `hooks/affirmation-scan.py` reads the reply the person receives".

`hooks/affirmation-scan.py` line 104 reads `turn_reader.turn_text(payload.get("transcript_path", ""))` —
every assistant message shown since the last human turn, mid-turn narration included. Its own docstring
says so and dates the change to 2026-07-27. `tests/test_affirmation_arm.py` pins it in both directions:
`test_affirmation_in_an_early_narration_line_reds` and `test_docstring_boundary_the_final_message_still_fires`.
The widening landed in `10dd65b`, inside this delta, hours before R294 was written.

R294 carries four criteria and none of them names the reach. The neighbouring requirement written in the
same commit does carry it — R293.3 states the whole-turn read for the code-anchor scan and cites INV-281.
The reference table confirms the asymmetry: INV-281 maps to R230.6, R230.7 and R293.3, with no R294 row.
So a reader of the spec learns that the code-anchor scan reads the whole turn and that the affirmation
scan reads the reply, and the tree disagrees with the second half.

This matters beyond bookkeeping. The affirmation scan's reach is the thing a human paid for: the
2026-07-23 field report that opened the mid-turn-reach row was two banned frames reaching him through a
narration line. The requirement that finally states this hook's law states the reach he complained about
rather than the reach he got.

Add the reach criterion to R294 citing INV-281, rebuild the reference table, and correct M-460's opening
clause. A3 and A4 are the same fact seen from the architecture and from the queue.

`defect · internal-conflict (consistency)`

## A3 — The shared reader's pin names three consumers where five read through it

The guardrails node pins `hooks/turn_reader.py:1` as "the shared full-turn reader the contrast-frame,
hedge, and register nets read through, INV-281". Grep for the import across `hooks/`: `scissors-scan.py`,
`hedge-scan.py`, `register-judge.py`, `affirmation-scan.py`, `code-anchor-scan.py`. Five, and the pin
names three.

The two missing names are the two hooks this delta is about, and the pin was left untouched while the same
commit rewrote the owns line and added five pins beside it. The first record's F2 named this exact failure
mode one commit earlier — a document edited while denying the files it should have gained — and it recurs
here in a narrower place.

The pin's parenthetical is the architecture's own inventory of who depends on a shared mechanism, which is
what a reader consults before changing that mechanism. A person widening `turn_reader.turn_text` today
would read three consumers and test three.

Add both nets to the pin's list. The same sentence carries the answer to A2: once the pin is honest, the
requirement that is silent about the reach becomes visible against it.

`defect · internal-conflict (consistency)`

## A4 — A live bug row sits in the archive while this delta ships its remaining half

Row 482 (mid-turn chat lines reach the human ungated) reads `*queued* 2026-07-23` and lives in
`docs/queue-archive/rotated-ROADMAP-2026-07.md`, listed in ROADMAP.md's rotated manifest. It is absent
from the live body. The queue's own preamble holds that the body carries open, in-work and deferred rows
alone and the archive keeps the closed ones, so a queued row in the archive is a row nobody can reach: it
appears in no what-is-left answer, no cap count, no dependency graph, and no landing gate.

Its work is half done and this delta did the other half. `d7400d8` gave the contrast-frame and hedge scans
the whole-turn reach and archived the row in the same commit; `10dd65b` gave the affirmation scan the same
reach. Two of the row's three done-when clauses are now discharged. The third — a coverage note stating
which chat surfaces each register net reads — exists nowhere: grep for its wording returns only the
archived row itself, and the reach facts live scattered across three docstrings, R293.3, M-457 and the
architecture pin A3 corrects.

The sharper point is that this delta corrected the identical defect for a different row and left this one.
Row 55 (snapshot machinery) had been moved to the archive at `*deferred*` by `7818f66`, and this commit
brought it back into the live body. The same commit's diff touches the archive file in the same block. So
the class was seen, and one instance was fixed. Under the recurring-problem rule the second instance owes
the same fix, or a net that finds both: an assertion that every row in an archive file carries a terminal
status.

Move row 482 back to the live body at `*in-work*` with the coverage-note leg named as its open leg, or
close it whole with the note written and its delivery report riding along.

`defect · boundary-issue (composition)`

## A5 — Three shipped behaviours of the code-anchor scan are stated by no criterion

R293's six criteria describe a scan that reds a queue row number in either working language and a bracket
code the documents use, and that passes anchors, fenced and quoted spans, table rows and bare numbers.
The shipped `find_hits` does three further things:

- It reds a document name run against a number — `ROADMAP 480`, `ARCHITECTURE 122`, `PRODUCT_SPEC 352`,
  `TEST_MATRIX 6` (pattern 4). A document name is neither a queue row named by its number nor a bracket
  code, so criterion 1's population does not contain it. M-459 repeats criterion 1's wording and misses it
  too.
- It reds the multi-letter codes read aloud with a space — `INV 281`, `ROW 386`, `ACT 3` (pattern 5) —
  while holding the single-letter codes to the dash form. That split is a real design decision with a
  stated reason in the docstring, and the spec records neither half.
- It **passes** a naming word plus a number when the same line carries a file word or a filename-shaped
  token (`_is_file_line_reference`), on the reading that this names a line inside a source file. This is a
  pass no criterion authorizes, which means no acceptance protects it: a future tightening of the pattern
  list can delete the carve-out and red nothing.

All three came in with `10dd65b` as the fold of the first record's F6, and the requirement written after
them describes the state before them. The docstring carries every one of these facts in careful prose,
which is the right place for the reasoning and the wrong place for the law.

State the population criterion 1 actually covers, and give the source-line carve-out its own criterion in
the case that already holds the lawful passes.

`defect · missing-rule (invariant)`

## A6 — The added patterns are case-insensitive, and only the firing direction is tested

`COMPILED` applies `re.IGNORECASE` to all six patterns. Two of the three shapes added in `10dd65b` carry
ordinary English inside them once case is dropped: `(?:INV|ROW|ACT)[-\s]+\d+` reds "act 3" in a sentence
about a play or a step, and `(?:M|E|T|S|D|A|B|C|F|R)-\d+` reds "b-2", "f-16", "c-4" and any lowercase
letter-dash-digit pair not preceded by a word character. The docstring reasons carefully about why the
single-letter codes keep the dash-only requirement, and the reasoning assumes the uppercase reading that
`IGNORECASE` removes.

`tests/test_code_anchor_scan.py` holds eight tests. The five silent-direction tests cover the shapes the
first cut already passed — parentheses, brackets, a table row, a code block, a clean reply — and the three
firing tests cover the naked forms. Nothing exercises the shapes the new patterns brought into range. A
Stop hook that blocks costs the human a turn on every false positive, which is the expensive direction, and
for the added patterns nothing measures it.

Either drop `IGNORECASE` for the two code patterns and keep it for the working-language naming word, or
add the lowercase-English cases to the silent-direction tests and accept them deliberately.

`defect · over-specific (abstraction)`

## A7 — The reopened row's cell contradicts itself

Row 55 now reads `*queued* 2026-07-27` with an acceptance cell whose three legs each end in MET, followed
by a reopening note saying the mechanical slice named as riding another row has no open owner and this row
carries it again. The third leg reads "declared-scope diff feeds the guardrails — MET as the named seam and
the E-6 check clause (the mechanical slice rides row 3, said)", which is the sentence the note contradicts.
A reader of the cell cannot tell what the row owes.

The whole-close law asks an open row to name its open leg. The note names it in prose at the end of a cell
whose structured legs all say the work is done, so the row's own machine-readable shape says finished.

Flip the third leg from MET to OPEN with the slice named, and let the note carry the history of why.

`defect · internal-conflict (consistency)`

## A8 — The registry's own note denies the tree

`hook-red-proofs.json`'s `affirmation-scan.py` entry carries `"source_fallback": "no repo copy exists under
hooks/ as of this writing; proven against the installed copy at ~/.claude/hooks/affirmation-scan.py — see
the census in the movement report"`. `hooks/affirmation-scan.py` exists and this delta edited it. Run here,
the runner prints `OK affirmation-scan.py — fired: decision=block` with no NOTE line, because
`resolve_hook_path` found the repo copy first.

R292.3 makes the fall back a reported event. A stale note claiming a fall back that no longer happens
teaches a reader of the registry that the pack's own copy of a shipped hook is missing.

Drop the field.

`defect · internal-conflict (consistency)`

## A9 — The stand-downs ship in both hooks and are stated in neither requirement

Both new hooks exit silently on `stop_hook_active` and on an empty transcript read. Both stand-downs are
load-bearing: the first prevents a block loop when the hook fires on its own correction message, and the
second is the clause that made the first record's F3 dangerous, since an unreadable transcript looks
exactly like a clean turn. `tests/test_affirmation_arm.py::test_stop_hook_active_stands_down` pins one of
them, and M-460 names it as a covered fact. R293 and R294 state neither.

The gap composes badly with A1: the runner proves a hook fires, the stand-down is what makes a broken hook
look identical to a clean turn, and no requirement holds the stand-down to a shape.

Add the stand-down clause to each requirement's boundary case.

`defect · missing-rule (invariant)`

## Note

**N1 — where the runner runs is answered outside the spec.** The first record's F8 asked that the hook
proof runner either take a gate letter or be pinned with the riding-the-suite note the convention uses.
The delta took the second road: the architecture's owns entry for INV-282 says "rides the suite not the
push chain, no gate letter" and M-458 repeats it, discharged in practice by
`tests/test_check_hooks_can_fire.py::test_runner_is_green_on_the_real_shipped_fixtures`. R292 says nothing
about placement, which is correct by the one-home law — runtime placement belongs to the architecture. The
remainder worth naming: row 489's done-when asks for "a red fixture the release gate runs", and the suite
discharges that only if the suite is read as that gate. One sentence in row 489's cell closes it.
`note · hard-to-operate (ops-ux)`

## The four questions this addendum was asked

**1. Do the three new requirements say what the code does?** R292: criteria 2, 3, 4, 5 and 7 hold against
`guardrails/check-hooks-can-fire.py`, verified line by line and by running it (7 hooks fire, 1
`cannot_red`, exit 0). Criteria 1 and 6 do not — A1. R293: criteria 1 through 6 hold against
`hooks/code-anchor-scan.py`, with three shipped behaviours that no criterion states — A5. R294: criteria 1
through 4 hold against `hooks/affirmation-scan.py`, and criterion 1 understates the reach the same delta
built — A2. Behaviour with no criterion, across all three: the two stand-downs (A9), the runner's reds on
a missing fixture directory and on an unknown detect mode, and the source-line carve-out (A5).

**2. Do the matrix rows name tests that exist and assert the stated fact?** Yes, with A2's exception.
`python3 -m pytest tests/test_code_anchor_scan.py tests/test_affirmation_arm.py
tests/test_check_hooks_can_fire.py -q` → 26 passed. M-458's three named tests exist and are the ones that
red the runner on a silent hook and on a triggerless fixture; M-459's eight named tests exist and split
three firing against five silent; M-460 names a module that exists with ten tests covering both directions
plus the stand-down. The one fact a named test does not assert is M-460's opening clause about reading the
reply, since the module's own tests assert the wider reach instead.

**3. Does the guardrails node claim anything the other documents deny?** One claim, A3 — the shared
reader's pin names three consumers where five read through it. The three new owns entries agree with their
requirements: INV-284's parenthetical matches R294.4 clause for clause (setup walk, config-health,
judge-hooks, meter), verified against `scripts/install-pack-hooks.sh` lines 33/79-80 and
`guardrails/judge-hooks.json`; INV-282's placement note is stated by no requirement and contradicted by
none (N1); INV-283's note that the plain-language law's own home stays communicator agrees with R293's
citation of INV-28. The five new pins all resolve to files that exist.

**4. Was the reopening sound, or was the gate over-strict?** Sound, and the gate was right. The tag is
real: R1.4 carries an own-line `[target]` marker citing E-6, E-7, A-6 and E-18, and
`tests/test_traceability.py`'s `TARGET_ROW_OWNERS` map ties five of those anchors — E-6, E-7, E-10,
INV-17 and A-6 — to row 55, asserting each owning row is present in the live queue and non-terminal. With
row 55 in the archive the first assertion fails by construction. The promise is also genuinely unbuilt:
grep for the snapshot machinery across `guardrails/`, `scripts/` and `skills/` returns nothing, and R177.9
still promises a first baseline snapshot saved at adoption. So closing it was wrong on the merits and not
only on the gate's reading. One correction to the reopening note's account: the row was never *landed*.
`7818f66` moved it to the archive while it read `*deferred*`, which the live-body law forbids on its own,
independent of who owns the tag. That is the same defect A4 names for row 482 — the note treats it as a
mistaken close, and the class underneath is a non-terminal row reaching the archive.

## What is sound (verified against primary sources)

- The first record's F3 is folded: all six transcript-reading fixture payloads carry the relative
  `transcript.jsonl`, and the runner's rewrite is what makes them absolute. The gate no longer reds on a
  fresh clone for a path reason.
- The first record's F4 is folded: `tests/test_affirmation_arm.py` exists with ten tests — the universal
  English tier, the overlay tier and its silent fall back on an absent or malformed file, four
  silent-direction cases, the early-narration case, the stand-down, and the end-to-end block shape.
- `guardrails/check-hooks-can-fire.py` executes the real scripts against the real fixtures and is green
  today over seven hooks with one declared carve-out whose reason prints on every run. Its three tests red
  it on a stub hook that never prints and on a fixture carrying no trigger.
- The code-anchor scan's anchor span now tolerates an embedded line break (`BRACKETED` compiled with
  `re.DOTALL`), which closes the lawful-shape half of the first record's F6, and the source-line carve-out
  closes the other half for the working language.
- The two lane rows (386, 412) are back at `*queued*` with a dated re-derivation naming what each still
  owes, and the live in-work count reads two (rows 489 and 490), inside the cap of three.
- The reference table and `PRODUCT_SPEC.index.md` are rebuilt consistently: INV-282, INV-283 and INV-284
  carry complete criterion lists, and every borrowed anchor the three requirements cite (INV-28, INV-173,
  INV-175, INV-202, INV-203, INV-211, INV-212, INV-238, INV-281) gained its new criterion rows, with the
  single exception A2 names.
- The matrix's anchor-to-row table gained INV-282 → M-458, INV-283 → M-459, INV-284 → M-460, and the three
  rows sit under the guardrails node block, matching the node that owns their invariants.
