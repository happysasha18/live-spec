# `SKILL-REVIEW` — live-spec-base, bare dated citations move to `docs/lenses.md`

Skill: live-spec-base. Date: 2026-08-25. Range: this commit (ships with the reviewed change).

Verdict: ALLOW. Pure subtraction, no rule reworded, no fact lost.

## What changed

Five rules (22, 31's first sub-bullet, 33, 34, 35) each carried a trailing dated citation —
"the owner's word, DATE: ..." — that was pure provenance with no narrated worked case, the
class a prior reverted attempt (`docs/prover/2026-08-25-live-spec-base-second-pass.md`)
found: 197 of that attempt's 259 saved bytes came from exactly two such removals (rules
33, 35, done then only by accident), because `docs/lenses.md` already calls itself "the
provenance home for the pack's rules... keyed by the rule's code" and no skill session ever
loads it — filing provenance there needs no pointer sentence left behind in the body.

This edit repeats that pattern deliberately for all five bare citations still in the file
(re-derived by a dedicated read-through, not assumed from the prior attempt's count — see
`docs/prover/2026-08-25-live-spec-base-lenses-extraction.md`, the accompanying prover
record, for the full re-derivation). Each citation is deleted from `SKILL.md` with nothing
put back in its place; each becomes a new dated entry in `docs/lenses.md`, keyed by its
INV code (INV-98, INV-189, INV-237, INV-247, INV-302).

## Cold read of each cut, against the body as it now stands

- **Rule 22 (INV-98).** The cut sentence: "the owner's word, 2026-07-10: convergence covers
  every process and every kind of artifact — there is a goal, and we walk toward it,
  always." The rule's own bold lead-in already states this: "Every process converges on its
  goal." Nothing normative was carried only in the citation.
- **Rule 31, first sub-bullet (INV-189).** The cut sentence: "the owner's word, 2026-08-07
  11:19: a request is written down, and nothing stands in the way." The kept sentence one
  clause earlier already carries the substance: "a deposit is recorded on arrival and never
  blocks a push."
- **Rule 33 (INV-237).** The cut sentence named the 2.7.0 release incident. The rule's own
  body, two sentences earlier, already tells the same story in full ("the 2.7.0 release's
  own breach of this rule... is written out under rule 33 in
  `references/worked-examples.md`") — the cut sentence was a second, shorter retelling of a
  story the rule already points at elsewhere.
- **Rule 34 (INV-247).** The cut sentence: "the owner asked the pack to hold it,
  2026-07-20." Purely a provenance stamp; the rule's normative content (re-derive a deferred
  item's state before resuming it) is stated in full in the sentences before it.
- **Rule 35 (INV-302).** The cut sentence: "the owner asked for this reading as a standing
  process, 2026-07-28." Same shape — provenance only, the rule's mechanism (fresh agent
  reads at both ends) is stated in full above it.

Every cut leaves its paragraph grammatically complete — read each in context in the diff;
none ends on an orphaned connective or a sentence that now refers to nothing.

## What did not happen

No pointer sentence was added to `SKILL.md` in place of any of the five (the prior attempt's
mistake, which made 9 of 11 edits net byte-losers). No rule's meaning changed. No `INV-` code
lost its substance — each substantive claim the citation touched is independently stated
elsewhere in the same rule, confirmed above rule by rule, not assumed.

## Independently verified before this record was written

An independent adversarial reviewer (separate agent, briefed to find a reason to reject, not
confirm) re-derived the byte/line delta from `wc -lc` directly (`607→602` lines,
`52202→51705` bytes, `-497` bytes), re-ran `tests/test_live_spec_base_body_thinned.py` (6
passed) and `tests/test_convergence_rule.py` (4 passed), ran `spec-style-lint.py --tier full`
against both `HEAD` and the edited tree and confirmed byte-for-byte identical error output
(14 errors both times — no new register violation, unlike the prior attempt's `scissors`
regression), and grepped `tests/` broadly for all five removed phrases, finding one
docstring-only mention (`tests/test_convergence_rule.py`'s module docstring paraphrases
rule 22's citation for human context; no assertion targets it). Verdict: CONFIRMED-SAFE-TO-COMMIT.
