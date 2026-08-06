# Prover check — the never-bend budget rule, 2026-08-06 08:42

Prover skill version 4.3.0. Mode: a delta re-check over one commit, run by a seat that authored none
of it (SPEC INV-237).

Subject: the delta in commit `df4a56d` to `PRODUCT_SPEC.md`. Requirement 220's never-bend list gained
a fourth case, "a rung moves the pace alone", carrying criteria R220.6 to R220.9. Two sentences joined
the requirement's Context. The generated code table gained R220.6 to R220.9 under INV-40, R220.8 under
INV-46, R220.9 under INV-69, and R220.6, R220.7 and R220.9 under T-19.

## Method

Read Requirement 220 whole as it now stands, then Requirement 219 around it, then the glossary lines
for the economy ladder and the never-bend list. Read the pre-delta text of the same span through
`git show df4a56d^` to tell a delta finding from an older one. Read the commit's edit to
`skills/live-spec-base/SKILL.md`, since that skill is the rule's consumer. Then walk four questions
over the new criteria, the ones this check was asked: do they contradict a neighbouring clause, does
each say a testable thing, does the case name match what its criteria do, and does the requirement
still read as one rule. Last, read the four codes the criteria ride against their homes and against
the matrix.

## What was checked

Requirement 220 in full, all nine criteria. Requirement 219 in full, all seven. Requirement 226, the
other carrier of INV-40. Requirement 214 criterion 3 and Requirement 215 criterion 2, the homes of the
audit and the release re-prove. Requirement 281, the cold reader's home. `TEST_MATRIX.md` rows M-134,
M-135, M-144 and M-175. The test body at `tests/test_traceability.py:2579`. `ROADMAP.md` row 549.

## Findings

F1 — Criterion 8 drops the rung scope its four siblings carry, and the base skill states the same rule
wider

> "The system *shall* raise a fresh clean-context agent for an adversarial review, a cold reading, a
> release re-prove, and a deep spec-and-architecture audit." — PRODUCT_SPEC.md, Requirement 220 /
> Case: a rung moves the pace alone / criterion 8

An agent under the tight rung reads Requirement 220 for what a budget may not touch. Every other
criterion there names its rung: criteria 1 to 3 and 6 say "at every rung", criterion 4 says "even
under the tight rung". Criterion 8 names none, so the agent cannot tell a never-bend item from a
free-standing rule. The same commit wrote the base skill wider. It raises a fresh agent "every time
the method asks for one", with the four as examples. An agent holding the skill therefore protects the
clean-writer road at Requirement 129; an agent holding the spec does not. The spec is the definition of
correct (SPEC INV-144), so the skill's wider promise stands unbacked.

Rewrite criterion 8 to the pattern its siblings keep, opening the list the way the skill does: "The
system *shall* hold at every rung the fresh clean-context agent any ask of the method raises, among
them an adversarial review, a cold reading, a release re-prove, and a deep spec-and-architecture
audit." That restores the rung scope and closes the gap against the skill.

`defect · internal-conflict (consistency)`

F2 — Criterion 8 names four protections and carries two codes

> "[INV-40, INV-46]" — PRODUCT_SPEC.md, Requirement 220 / criterion 8, its code bracket

The code-to-location table is generated from the criteria's own brackets. INV-46 homes the adversarial
fresh-context checker at Requirement 213 and matrix row M-144. The other three asks home elsewhere: the
release re-prove at INV-237 (R215.2), the deep audit at INV-145 (R214.3), the cold reading at INV-266
and INV-267 (R281). A maintainer tracing INV-237 for its never-bend standing reads the table and finds
no Requirement 220 row. The siblings hold the convention: R220.2 carries five codes for its five named
items, and R220.9 carries T-19 for pace and INV-69 for the tier.

Add INV-237, INV-145 and INV-266 to criterion 8's bracket. Then regenerate the code table in
`PRODUCT_SPEC.md` and `PRODUCT_SPEC.index.md`, which are generated output.

`defect · hard-to-operate (ops-ux)`

F3 — Criterion 6 states the case's thesis where a testable criterion belongs

> "The system *shall* hold at every rung the standard the work is held to, moving the project's pace
> alone." — PRODUCT_SPEC.md, Requirement 220 / criterion 6

"The standard the work is held to" names no members. Criteria 1 to 3 each enumerate theirs: the door
law, its tripwires, red-before-fix, the delivery report, the push gate, the safety net. A test author
writing ROADMAP row 549 can pin a needle for criteria 7, 8 and 9, since each names a phrase whose
removal changes what an agent does. Criterion 6 offers none. So row 549's own bar, "a test fails when
any one of them is removed", cannot bind this criterion as written.

Two options. (a) Move the sentence into the requirement's Context, where a thesis lives, and let the
case run from criterion 7. (b) Ground it, by stating that the standard is the union of criteria 1 to 3
and every check the method calls for. I prefer (b). It keeps the case's own claim inside the criteria
row 549 will test.

`recommendation · over-general (abstraction)`

F4 — Requirement 219 says a rung sheds rigor, criterion 9 says economy is bought from no check, and no
sentence ties the two words

> "The system *shall* buy economy from pace, from batching, and from a cheaper tier on mechanical
> work, and *shall* buy it from no check." — PRODUCT_SPEC.md, Requirement 220 / criterion 9

Requirement 219's title reads "The economy ladder names what a tight budget may shed", and the glossary
line for the economy ladder repeats it. Requirement 219 criterion 4 puts the lean rung's mid-work test
runs on the touched node's rows. An agent setting the lean rung asks whether that narrowing buys
economy from a check. Criterion 4's own debt line answers it: the deferred full pass runs later as a
dated debt. So the shed moves a check's timing. That reading holds, and neither requirement states it.
An agent reading criterion 9 alone may keep running the full suite mid-work, which drops what the lean
rung was set for.

Add one sentence to criterion 9 or to Requirement 219's Context: a rung's legal shed moves a check's
timing or its breadth at one moment, and every shed check still runs, its dated debt line the proof.

`recommendation · internal-conflict (consistency)`

## The queued matrix finding — ROADMAP row 549

Row 549 was filed by the adversarial review of 2026-08-06. It holds that no matrix row names the four
new criteria, and that deleting all four leaves the suite green. This check confirms it, and the proof
is mechanical.

| What was read | What it holds | Bearing on row 549 |
|---|---|---|
| `TEST_MATRIX.md`, whole file | zero occurrences of the string `R220` | no row cites the requirement by number |
| M-135, the only row under INV-40 | enumerates the door law, tripwires, red-before-fix, the gates, the report, purity, the push gate, the safety net, narration, the host line | the pre-delta list alone; names neither the standard nor the fresh agent |
| M-134, the row under T-19 | the rungs, their legal sheds, the setting moved by the human's word | the ladder itself; no new criterion |
| M-175, the row under INV-69 | the routing rule and its tiers | no new criterion |
| M-144, the row under INV-46 | verify's adversarial fresh-context checker | no new criterion |
| `tests/test_traceability.py:2579`, `test_economy_ladder` | asserts ten string needles against the spec | listed below |

The ten needles are "economy ladder", "`budget.pressure`", "defaulting to full", "moved only on the
human's word", "ask the rung or state the standing default at project setup beside the project kind",
"every shed actually taken is said in the delivery report", "The never-bend list holds at every rung",
"require the batch's reach-scoped gate green at the tree's head", "bisect a batch-end red by delivery
order", and "An explicit host line outlives any rung". Each lands in the Context or in criteria 1 to 5.
None reads any word of criteria 6 to 9.

Verdict on row 549: **confirmed**, as written. Removing criteria 6 to 9 from the spec today leaves
`test_economy_ladder` green and leaves every other row's needles untouched. The row stays queued, and
this check adds one note to its Done-when: F3 above says criterion 6 needs grounding before a removal
test can bind it.

## Checked and holding

Five things were read for a contradiction and found none.

The requirement still reads as one rule. The Context's two new sentences match criteria 6, 7 and 9,
and the case heading sits in the requirement's own pattern.

The case name fits three of its four criteria. "A rung moves the pace alone" is what criteria 6, 7 and
9 say. Criterion 8 sits outside it, which F1 carries.

Criterion 9 agrees with INV-69. The routing rule keeps a judgment step off a cheaper tier, and
criterion 9 buys the cheaper tier on mechanical work alone.

Criterion 7 agrees with Requirement 226. The push gate derives its check-set from the diff's reach at
every rung equally, so that narrowing is no rung buying economy, and criterion 9 leaves it alone.

The missing `---` before Requirement 221 is older than this delta. `git show df4a56d^` shows criterion
5, a blank line, then the heading. Sixteen of the spec's 305 requirements lack the separator, so this
is a standing gap in the file rather than a delta finding.

## Verdict

Four findings: two defects and two recommendations. Both defects land on criterion 8, and one rewrite
of that sentence with its code bracket folds them together. The two recommendations queue for a taste
call. Row 549 is confirmed, with the needle list above as its proof.

The two defects block under M-6 until criterion 8 is folded. The fold belongs to the delta's author,
and this record names no fix as landed.

## Reach

Files read directly, by line: `PRODUCT_SPEC.md` (requirements 213, 214, 215, 219, 220, 221, 226, 281,
the glossary, the generated code table), `PRODUCT_SPEC.index.md`, `TEST_MATRIX.md`,
`tests/test_traceability.py`, `ROADMAP.md`, `skills/live-spec-base/SKILL.md` (the commit's diff),
`ARCHITECTURE.md` (the code lists), and `docs/lenses.md`. The pre-delta spec was read through
`git show df4a56d^`. Read for form and precedent: `docs/prover/2026-08-05-pin-repoint-check.md`.
