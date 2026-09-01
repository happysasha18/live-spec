# Skill review — five skills changed in tonight's overnight run

SKILL-REVIEW

Skills: live-spec-base, product-prover-pack, publish, spec-author, text-audit-pack

Date: 2026-09-02

Reviewer: skill-creator quality lens (Progressive Disclosure, Anatomy of a Skill,
frontmatter-description accuracy) applied by hand, against `git diff 534cb16b..HEAD -- skills/`.

Verdict: all five changes are sound in substance, correctly placed, and lose no rule's own
meaning. Findings names one editorial note for a future pass, folded nowhere else here.

## What changed, and why each holds

**`live-spec-base/SKILL.md`, `live-spec-base/references/settings-ladder.md` (q-803).** Two inline
provenance citations removed — `"— his word, 2026-09-01."` off the concurrency rule, `"(both his
word, 2026-08-27)"` off the one-name rule, and a three-line citation block off the economy-ladder
reference. Each rule's own substance is untouched; only the trailing citation clause is gone. The
provenance itself is not lost — `JOURNAL.md`'s matching 2026-09-01/2026-08-27 entries and
`DECISIONS.md` already carry it, which is the whole point of `q-803`'s row (a `SKILL.md` rule
states itself; the journal carries who said it and when). Read each rule after the cut: both still
parse as complete, standalone instructions with no dangling reference to a citation that used to
sit there.

**`product-prover-pack/SKILL.md` (q-436).** One new bullet, "the co-occurrence value lens," added
beside the existing axis-verdict lens it's structurally identical to — same shape ("a sibling axis
carrying no verdict is a finding, of the blank-answer class"), same mechanism reused rather than a
new one invented. Cites `[SPEC INV-244]` correctly (verified against `spec/design-spec-review.md`
Requirement 265 criterion 15, which the same INV-244 anchors). No overlap with the existing
axis-verdict bullet — one covers a blank pole answer, this one covers a blank co-occurrence answer
between two answered poles, a genuinely different gap.

**`publish/SKILL.md` (q-803).** One inline citation, `"(his word 2026-07-10)"`, removed from the
Known-issues re-read rule. Rule reads complete without it; the fact already lives in `JOURNAL.md`.

**`spec-author/references/change-record.md` (q-805), `spec-author/references/facet-sweep.md`
(q-436).** Two unrelated changes to two different reference files under the same skill, both real:

1. `change-record.md` drops the retired size-ratchet's own description and states current truth in
   its place — the figure is still measured and printed, no gate holds it to a bound, and a
   document that genuinely outgrows one file has a real answer already (`skill-creator`'s own
   split guidance) rather than a mechanical ceiling. Checked against the actual current state:
   `guardrails/check-size-ratchet.py` and `guardrails/spec-ratchet.json` are gone from the tree
   (confirmed by `git status`), so this reference no longer describes machinery that doesn't
   exist — a real correctness fix, not just tone.
2. `facet-sweep.md` gains the co-occurrence forcing-step duty beside the two-poles duty it sits
   next to — matches `product-prover-pack`'s new lens above exactly (same anchor, same mechanism,
   author's and reviewer's sides of one contract). Read in context: doesn't restate the two-poles
   duty above it, correctly scopes itself to "reaches only the co-occurrence of the poles already
   owed, not [refinement values]," avoiding scope creep into taste-level axis values.

**`text-audit-pack/SKILL.md` (q-803).** One inline citation, `"The owner's word on 2026-08-18
settles it, "`, removed from the cheap-reader definition. Reads complete without it: "It follows
rule 74ef247, which first split a round into one strong and one cheap reader: a cheap reader is a
reader with none of this pack's own skills or rules loaded" — the definition that follows is the
substance, the citation was never load-bearing for understanding it.

## Findings

Nothing blocking. Worth a future look, when either file is next opened for other work:
`live-spec-base/SKILL.md` and `product-prover-pack/SKILL.md` both grew tonight (a rule trimmed, a
bullet added — roughly a wash for the first, pure growth for the second) with no fresh byte-count
check against either skill's own documented size ideal — a measurement to read then, in the same
spirit `q-805` just argued for, never a reason to gate this pass.
