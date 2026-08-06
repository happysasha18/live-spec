# Two review runs over one sample spec — a comparison

- **Date:** 2026-08-06
- **Run 1:** `editions/product-prover/examples/sample-review-run-1.md`
- **Run 2:** `editions/product-prover/examples/sample-review-run-2.md`
- **Document both runs reviewed:** `editions/product-prover/examples/sample-spec.md`

Both runs read the same committed text of the skill: each record names product-prover edition
`1.0.0-standalone` from `SKILL.md` metadata, and no change to the skill sits between them.

This record is written by a third reader who read the sample spec, the stress-lens reference, and the
two review records. It compares what the two runs found. It judges neither run's method.

---

## 1. What each run counted

**Run 1** numbers its main findings `F1`–`F32`. Its ledger totals 32 findings: 30 defects and 2
recommendations. It records 3 acknowledged gaps as `A1`–`A3`, and its own ledger line says those
carry no kind and are not counted as findings.

**Run 2** numbers its main findings `F1`–`F30`. Reading the kind tag on each one gives 25 defects and
5 recommendations (`F4`, `F24`, `F27`, `F29` recommend now; `F28` recommends later). Its closing
readiness line says twenty-five defects, which agrees. It records the same 3 acknowledged gaps as
`A1`–`A3`, also with no kind.

Both runs tag the Section 13 items as acknowledged and give them no kind. This comparison counts
main findings only, meaning items carrying a kind of `defect` or `recommendation`, and it counts them
the same way for both runs. The three acknowledged gaps are excluded on both sides. They cover the
same three clauses of Section 13 in both records, so nothing turns on the exclusion.

---

## 2. Match table

One row per main finding of run 1. The right column names the run-2 finding that reaches the same
underlying issue, meaning the same clause of the sample document and the same failure. A dash means
run 2 filed no finding on that issue.

| Run 1 | Underlying issue | Run 2 |
|---|---|---|
| F1 | The carrier acts twice and is absent from the actor list | — |
| F2 | The bank / central boundary is never drawn, so ownership of code checks, the clock, and the sweep is unassigned | — |
| F3 | Compartment's two-value state set is too small for the flow | F21 |
| F4 | Bank is load-bearing and is not an entity | F4 |
| F5 | Pickup codes carry no uniqueness rule, so two live codes can collide | F5 |
| F6 | Deposit flips state before the code exists, with no behaviour between the four steps | F6 |
| F7 | The 72-hour window's start instant is never fixed | — |
| F8 | A shut door marks PickedUp with no check that the parcel left | F8 |
| F9 | Deposit has no precondition on the parcel's current state | — |
| F10 | The courier badge is scanned and no rule says what a bad badge does | F7 |
| F11 | A compartment opened for a deposit that never completes has no recovery | F21 |
| F12 | Expired is a dead end: no exit state, no actor, no time bound | F1, F2 |
| F13 | Registered has one exit, so a stale registration never ages out | F13 |
| F14 | The retry ladder ends and nothing follows the third failure | F14 |
| F15 | The one-minute code rule cannot be discharged and Section 10 contradicts it | F10 |
| F16 | "Only the recipient can open" is unenforceable over a bearer code with no attempt limit | F12 |
| F17 | Section 6 and Section 8 contradict each other on who may open a compartment, and an operator open has no state effect | F11, F3 |
| F18 | A 72-hour window ended by a daily sweep is really 72 to 96 hours | F9 |
| F19 | Expiry revokes no code, so an expired parcel stays collectable | — |
| F20 | Offline operation and the deposit flow cannot both hold as written | F19 |
| F21 | The dashboard's counts and bank occupancy have no tying invariant | F15 |
| F22 | The declared cross-cutting rules name no enforcer, and the log law misses the surfaces that matter | F16, F17 |
| F23 | One dependency's failure is written and the other dependencies are silent | — |
| F24 | Retry policy is written for one integration and none of its siblings | — |
| F25 | The 03:00 sweep can fire on a parcel a recipient is collecting | F22 |
| F26 | Per-bank dashboard rows carry no staleness mark for an offline bank | — |
| F27 | SMS delivery is asynchronous and pending, arrived, and failed are observable nowhere | F18 |
| F28 | The SMS's content beyond the code is never specified | F26 |
| F29 | The keypad's answer to a wrong, expired, or unknown code is unstated | F20 |
| F30 | The stated budgets name no measurement point and no watcher, and no scale ceiling exists | F29 |
| F31 | The recipient's phone number crosses to a third party with no privacy or retention line | F30 |
| F32 | Section 5's deposit paragraph packs seven ordered steps into prose | F28 |

Notes on individual rows.

- **F3 and F11** both land on run 2's `F21`. They stay two rows here, because they are two issues: an
  incomplete state set, and an abandoned deposit with no recovery. Run 2 writes both into one finding.
- **F12** maps to two run-2 findings, which split the dead end from the compartment that is never
  freed. It counts once.
- **F17** carries two halves. Run 2 files the contradiction as `F11` and the operator open's missing
  state effect as `F3`.
- **F19** is a dash on a close call. Run 2 reaches the symptom twice: `F20` lists an expired code
  among the keypad cases that owe a message, and `F22` describes an offline bank opening a door for a
  parcel central has already expired. Neither one files the underlying defect, which is that expiry
  performs no revocation act.
- **F31** matches on its privacy half. The other half, a refused courier who is told nothing, is
  unfiled by run 2; run 2's `F7` asks for a message on a badge refusal alone.

Several run-1 dashes appear in run 2 outside its findings. Run 2 names the bank / central seam in its
composition section and calls it the seam the document writes least about, and it files nothing (F2).
It states the unfixed window start in its assumption list and again in its invariant table, and it
files nothing (F7).

### Run-2 findings with no run-1 match

| Run 2 | Underlying issue |
|---|---|
| F23 | Two couriers at one bank can be sent to the same free compartment, since selection reserves nothing |
| F24 | A repeated or corrected manifest for a known tracking number has no stated effect |
| F25 | The carrier seam runs one way: no terminal state is published back to the carrier |
| F27 | Internal state names are the document's only vocabulary, and two surfaces show them to people |

Run 1 touches three of these four outside its findings. It names the two-courier collision as a
consequence sentence inside `F3`, and a duplicate manifest as a consequence sentence inside `F1`. It
handles the carrier as an authoritative surface through the assumption line the surface-authority
lens prescribes. It states the vocabulary rule for the keypad alone, inside `F29`'s fix.

---

## 3. Headline numbers

- **N = 32** — run 1's main findings.
- **M = 30** — run 2's main findings.
- **K = 24** — underlying issues both runs reached.

K counts the matched rows of the table above. Run 1 reached 8 issues run 2 did not file. Run 2
reached 4 issues run 1 did not file.

---

## 4. The character of the gap

The two runs agree on the document's spine. Every contradiction, every dead end, every unenforceable
promise, and every observability hole in the sample spec appears in both records, usually with the
same quoted clause. What one run reached alone sits at the edges of that shared core, and the two
edges have different shapes.

Run 1 alone reached specification hygiene around issues both runs had already opened: a participant
missing from the actor list, an undrawn component boundary, an undefined start instant for a stated
window, a per-dependency failure matrix, a retry policy owed to sibling integrations, and a staleness
mark on reported numbers. Run 2 alone reached concurrency and cross-system integration: two couriers
acting on one bank at once, a carrier feed that repeats itself, an outbound seam back to the carrier
that nobody writes, and internal state names reaching a person's screen.

The gap is thinner than the counts suggest. Most items only one run filed appear in the other record
as an assumption line, a table cell, or a sentence inside a neighbouring finding. The two runs
disagree less about what is wrong with the document, and more about where the line between a finding
and a note falls.
