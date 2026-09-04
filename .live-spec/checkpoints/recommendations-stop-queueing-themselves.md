# A review's recommendation stops becoming work by itself
Status: open
Owner: director

## DONE

- **Spec delta written (spec author, 04.09).** Requirement 60 rewritten: a recommendation is written
  into the review record and ends there; nothing opens a row for it; it becomes work only when the
  human writes it onto the plan. Requirement 4's re-decision made — a pre-existing defect a
  delta-scoped gate meets outside its delta is recorded the way a recommendation is recorded, not
  blocked; the reason stands in the requirement's own Context. Traces swept in the same pass: the
  glossary entry for *recommendation*, R69 (the design review's confidence read), R70.2, R141.2 (the
  flagship push gate), R184 (the restructure/migration merge gate, INV-114's own home, which stated
  the same queuing disposition), matrix rows M-282, M-253 and M-284, and the regenerated
  `PRODUCT_SPEC.index.md`. The spec-format guardrails (requirement shape, vocabulary, weak words,
  one-name, index) run clean.

## IN PROGRESS

(nothing yet)

## NEXT

Two adversarial reviews are running (one cold, one steered). After their findings are judged: the three tests that hold the old requirement wording are rewritten by the test author, the prover record for the whole range is written, then the gates and the push.

## DECISION SHEET

Goal in his words (04.09 01:07): the process that writes findings back into the project's own journal is written in the spec, so the spec is what has to change — and it goes through the flow, not an ad-hoc prover run from the seat.

Observable outcome: spec/design-spec-review.md no longer tells the push gate to queue a recommendation. A recommendation is answered inside the review record and dies there; only the owner's own word turns one into a row on the board. A defect still blocks and still gets folded.

Dimensions touched: quality and safety (the gate's own behaviour changes); documentation (the spec chapter, the matrix rows, the review-record shape).

Known: spec/design-spec-review.md lines 191-197 carry the rule; INV-140 is its invariant; matrix/product-prover.md rows M-282/M-325/M-338 trace it; tests test_finding_kind.py, test_review_record_class.py, test_design_reviewer.py, test_minor_gate_reconciliations.py read it. PLAN.md's own laws carried the same instruction and were cut tonight. spec/push-gate-milestone-audit.md req 1 makes every push write a fresh review record - 505 records exist.

Unknown: whether push-gate-milestone-audit req 1 is a second loop of the same shape or a constant-cost treadmill; whether the prover was ever run against either chapter.

Risk: reversible in git. The gate gets weaker in one direction - a real defect mislabelled a recommendation would now be dropped rather than queued; the fold rule for defects is untouched, which is the guard against that.

Specialists: spec author (the delta), product prover (reviews the delta, as a step in the flow), test author (the traces), independent verifier.

Evidence: a test that reds on today's spec text and passes after; the review-record shape carrying a recommendation with no queue row behind it.

What runs next: this, then the board's own remaining row (onboarding, q-54).

Documents that must change: spec/design-spec-review.md, matrix/product-prover.md, the four test files above.
