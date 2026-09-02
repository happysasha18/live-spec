# Prover record — 2026-09-02 turnkey-contract-review

product-prover skill version reviewed against: no version line in this skill's own SKILL.md at
review time; ran the skill as loaded from `~/.claude/skills/product-prover/SKILL.md`.

Document reviewed: `.live-spec/turnkey-contract-composed.md` (226 lines), composed from
`.live-spec/turnkey-contract-draft-orchestrator.md` and `.live-spec/turnkey-contract-draft-fable.md`
per the owner's word of 09:12, 2026-09-02. Pre-code contract review — no PRODUCT_SPEC/ARCHITECTURE
entry exists for this proposal yet; this is the review gating whether it may get one.

## Findings

**F1 — defect · undefined-path (transitions).** The checkpoint's declared lifecycle (§2/§4: "queued
has none yet"; T2 requires "no open checkpoint for this id") contradicts
`skills/director/SKILL.md`'s own Execution section, which opens a checkpoint at instruction
acceptance (the contract's own T1), before any holder/specialist is assigned. Fix: either move
checkpoint creation to T2 as a real behavior change to the shipped script (named in §9), or amend
the entity model so `queued` may carry an open, holderless checkpoint and T2 only assigns a holder
to it. The second is cheaper and matches what's shipped.

**F2 — defect · missing-rule (invariant).** `Requirement 309`/`matrix/work-board.md` (26 `*todo*`
facts: worker lanes, per-agent attribution, given-vs-actual time, a five-second refresh budget) is
retired by the contract's one clause "q-166's 'live' leg falls out of scope," with no retirement
record. This same session retired a comparable requirement (`Requirement 280`, q-805) with a named
pattern: struck text, `INV-264`/`INV-265` left as recorded gaps, matrix rows marked *retired*. Fix:
commit §9's `R309` row to that same pattern rather than a bare scope-drop.

**F3 — defect · partial-success-risk (atomicity).** T7 writes the checkpoint-close and the `PLAN.md`
✅ mark as two separate file writes ("in the same step" is not atomic in the underlying scripts). A
crash between them leaves a state this project's own history shows happens (`plan-9`'s "in hand"
mark disagreeing with its own real state, resolved by hand). Fix: name `PLAN.md`'s mark as
authoritative on disagreement, and add a `state-probe.sh` alarm class for a closed checkpoint on a
non-done ticket (and the reverse).

**Recommendation · now · confusing-for-users (cognitive-load).** Retiring the idea shelf (Requirement
315 criterion 3: exact-wording recall on later ask) in favor of "the transcript" is a real capability
risk given this project's own conversations get compacted/summarized over a long session — "the
transcript" is not the durable store the shelf promises today. Flagged for the owner's own weighing,
not a blocking defect.

## §10's four questions, answered

1. Exact-match (goal line or pointer set) is sufficient as the mechanical gate; overlap-without-match
   is never a mechanical block, only Director's own semantic judgment via proof A — the contract
   already implies this in §4 and should say so plainly.
2. Resume picks the top `queued` ticket by `PLAN.md`'s own existing order, the same rule §4 already
   states for "nothing in hand" — not recency, which this model doesn't track.
3. No — T4's own row already says Director triggers it from a worker's reported fact, never the
   worker directly; Code's own three-kind-reason requirement already refuses a bare "this got hard."
   Add one clarifying clause to §6's Code row.
4. No deadlock — this session's own tonight's commits are the worked proof: delivery lands and passes
   CI first, the `PLAN.md` mark is always a separate, later commit.

## Verdict

Needs another iteration, not significant rework. Three named, bounded defects (F1–F3), each with a
concrete one-line fix already proposed; §10's four self-raised questions all have real answers above.
Ready for test-author once §9 names F1's resolution and F2's retirement mechanics, and T7 carries
F3's recovery sentence.

Class lens: swept — one class filed (F1, F3): a transition's precondition or postcondition asserted
in prose without checking what the cited script actually does. Checked every other script citation
in the document against the real file; found no third instance.

Full findings, phase-by-phase model, and the four §10 answers with their reasoning: this session's
own chat transcript, same timestamp — not duplicated here in full to keep this record proportional
to a three-defect review.
