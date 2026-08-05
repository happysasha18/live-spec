# What guards text that has not been written yet — twelve findings

**The item.** An outside audit read this project on 2026-07-30 with one question: when new text is
written next — a new spec section, a new skill paragraph, a new report, a page shown in chat — what keeps
it readable and keeps the document from swelling. The readability of text already written was out of
scope; a separate campaign owns that. Below are twelve findings, ordered by leverage. Each carries the
path that proves it. The full coverage map, stage by stage, is at
`/Users/sashaabramovich/context-slimdown/reports/spec-future-text-coverage.md`.

**Why.** Two rewrites in the current campaign grew 10–25% and no gate objected. The audit went looking
for the missing brake and found it is nearly built.

**Who threw it.** An audit session in the context-slimdown window, reading this tree read-only.

---

## 1. The size brake is one comparison away from existing

Gate aa (`guardrails/check-doc-findings-bound.py`) walks every live document at every push and compares
each one's count of reading defects against a recorded ceiling. The record it reads,
`guardrails/rule-census.json`, stores a `bytes` field for all 115 documents beside the counts it does
compare. `scripts/rule-census.py` measures that field at line 243 on every run. **No code ever reads it
back.** The gate's own comparison sits at `check-doc-findings-bound.py:196–204`, over `total` alone.

Adding the same ratchet shape over `bytes` — may fall, may hold, never rises without a written reason —
would use the measurement already taken, the record already written, the gate already wired into the push
chain, and the raise-with-a-reason shape the record already carries in its `reason` field. It is the
highest-leverage change in this list by a wide margin: one comparison, no new instrument.

## 2. Eleven of eighteen places where new text is born have no guard

The audit mapped eighteen stages. Seven carry a check that blocks: the five checkers armed against the
live spec through the suite, the density ratchet, the duplicate-fact ceiling, the register lint held at
zero, the four byte ceilings at gate z, the findings ratchet at gate aa, and the chat scanners on the
reply-finished event. Eleven carry nothing, or carry an instruction with no machine behind it — among
them every report, every audit note, every brief, every handover, every page shown in chat, and every
file created outside this tree.

The pipeline skill that carries a change from request to commit
(`~/.claude/skills/build-pipeline/SKILL.md`) names no readability check at any step. A new skill body or
report can travel the whole road without meeting a cold reader.

## 3. Four size brakes exist, and each one misses this case

- **Byte ceilings on four documents** — `guardrails/doc-bounds.json`, gate z in `guardrails/pre-push`.
  Each ceiling was seeded roughly 100 KB above the file's size at the time, and the stated remedy for
  crossing one is moving closed rows to an archive rather than writing less. Three of the four sit well
  below their ceiling today, so the gate is silent through any plausible rewrite.
- **Density ratchet on the spec** — `guardrails/spec-ratchet.json`, armed on the live document through
  `tests/test_size_ratchet.py:82`. It holds bytes per criterion. Adding a thousand criteria of average
  length passes cleanly, so it bounds fatness per rule and not total size.
- **500 bytes per newly declared criterion, plus a per-delivery growth budget** — the real brake, at
  `guardrails/check-delta-record.py:59` and `:156–182`. It sits in no gate chain and in no suite check;
  `tests/test_delta_classifier.py:81` asserts it is absent from the push gate. Its only trigger is a
  paragraph at `~/.claude/skills/spec-author/SKILL.md:605`.
- **The findings ratchet** — gate aa, above. It counts defects, not bytes. A rewrite that keeps the
  defect count flat and adds a quarter more text passes.

Nothing anywhere states a growth ratio, and nothing bounds a document outside the four named ones.

## 4. The two-clean-readings loop has no trigger and no witness

Rule 54 in `guardrails/language-rules.json` binds every changed section: fresh readers with no project
background read it until two readings in a row come back with nothing blocking. Four format documents
carry the sentence verbatim. Its own record shows no pattern catcher and no model catcher, and its
arming point reads `nowhere`. No script runs the loop, and no script checks that it ran.

The evidence a checker would need already exists: 27 dated reading records sit in
`docs/language-reads/`. Nothing opens that folder. The rule's own note already names the fix — a script
that reads whether two consecutive readings came back clean.

## 5. Thirty-eight of sixty-three writing rules run nowhere

Counted from the `armed` field of `guardrails/language-rules.json`: 38 rules run nowhere, 16 run by hand,
15 have a machine behind them. The field is itself slightly behind the wiring — one-name-per-thing (r04)
is marked as running nowhere while `tests/test_one_name_check.py:48` arms its checker against the live
spec — so the record understates coverage in at least one place and is worth a sweep of its own.

## 6. A change that alters existing behaviour never has to edit the old sentence

Two duties exist on paper and neither has a machine:

- The intake table (`~/.claude/skills/build-pipeline/references/request-kind-table.md`) requires that a
  defect fix whose fact also lives in spec prose update that spec sentence in the same change.
- The change record (`~/.claude/skills/spec-author/SKILL.md:604`) requires that a sharpened criterion
  prove the old sentence no longer survives anywhere in the document — the only removal rule the audit
  found. It binds sentences carrying a bracket code, in the spec alone, and only when a change record is
  written; the classifier that would enforce it is the same hand-run script from finding 3.

So a change classed as touching existing behaviour may land as new text sitting beside stale text, and
outside the spec's coded sentences no rule and no check objects.

## 7. Removal is taxed and addition is free

Requirement 24 in `PRODUCT_SPEC.md` is the one rule governing how an editor treats existing text. It
requires every removed section, argument, rationale or worked example to be listed in the delivery report
with a line of justification each, and it explicitly leaves "a tightened sentence or a reordered clause
needing no account".

Read against this problem, it points backwards. A writer who appends owes nobody anything; a writer who
cuts owes a justification per cut. The cheapest path through the rules is the one that grows the
document. Any size brake added under finding 1 should be read alongside this asymmetry, or writers will
meet a ceiling with no permitted way down.

## 8. There is no split policy anywhere, and the shape of one is derivable

`docs/spec-format.md`, `docs/architecture-format.md`, `docs/roadmap-format.md` and
`docs/test-matrix-format.md` state no threshold, budget or trigger for splitting a document. Archiving
closed rows is the only stated remedy for growth, it covers four documents, and it preserves the live
file's shape rather than restructuring it. `docs/plans/2026-07-29-specification-subdivision.md` exists as
a plan, not as a rule.

*The following is the auditor's inference, not this project's rule, and is offered as a starting shape
rather than a proposal to adopt as written.* The existing rules already imply what a split policy would
look like: each fact lives in one place and others point at it; each ceiling carries a written reason;
a ceiling may fall and never rise. A policy consistent with those would say — a document declares a
working size well below the ceiling that reds; crossing it obliges the next delivery to move one named,
self-contained part into its own file with a pointer left behind, the way archiving already works; the
moved part enters the record at zero defects, so a split cannot launder defects into a fresh file; and
the parent's recorded byte count falls with the move, which the ratchet from finding 1 then holds. The
missing piece is the same one: a comparison on a number already stored.

## 9. Most new prose is born in folders the measured set skips

Gate aa is strict about new files — "A live document missing from the record also reds" — and that arm
is the strongest single mechanism found. Its reach is set by `live_files()` at
`scripts/rule-census.py:122–139`, whose exclusion list at lines 71–79 skips the folders holding reports,
audits, research, briefs, handovers, design notes, evaluations and reviews, on the reasoning that a record
of a moment is bound when written and not afterwards.

Those folders are where the majority of newly written prose lands. Files outside the repository
altogether are outside everything. A registered new file may also be any size at birth, since its byte
count is recorded and never bounded.

## 10. The rule that a first draft comes from an outside writer has no evidence to check

Rule 53 and Requirement 129 both require a draft from a writer with none of this project's vocabulary
loaded. There is no checker, and none is possible as things stand: finished prose carries no trace of
who wrote it. The rule's own record names the fix — record the brief handed to the drafting writer, and
have a script read whether that record stands beside the text — and states plainly that no such record
exists today. The model-based judge listed as holding part of this rule is one of the two switched off on
2026-07-30.

## 11. The spec's own reading-defect ratchet runs nowhere

`guardrails/check-criterion-readability.py` carries five arms over acceptance criteria — welded
sentences, a definition inside a rule, a closing clause with no verb, a crowded anchor, more than one
rule per criterion — each with a recorded baseline in `guardrails/criterion-readability.json`. Nothing
triggers it. `tests/test_criterion_readability.py` exercises fixtures and asserts the checker is absent
from the push gate; unlike its sibling ratchets it makes no assertion over the live document.
`docs/language-rule-coverage.md:309` states it in three places: "check-criterion-readability.py is armed
nowhere."

## 12. No check reads a file as it is written

No hook anywhere inspects the content of a file being written or edited. `guardrails/pre-commit` runs a
time-stamp check, a stale-edit fence and a parked-item rule, and carries no readability or size check at
all. The earliest moment any of this is caught is the push, by which point the text is already in the
tree and the writing session may be over. Every guard in this project is a late guard.

---

**Blocked:** nothing of the sender's stands still on this.
**Lived:** the audit ran the checkers and the census over this tree read-only, read the gate chain, the
rule file, the two authoring skills and the wired hooks, and found the gaps above by reading what each
gate compares against what each instrument already measures. The evidence is the paths cited under each
finding.
**Need-by:** none.
**Id:** authoring-coverage-2026-07-30
