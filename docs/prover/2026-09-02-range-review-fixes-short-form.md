# Prover short-form — the range review's own fixes (2026-09-02 20:50)

Short-form per the cadence for a small delta. Two commits stand between the full-range review
(`docs/prover/2026-09-02-full-range-review.md`) and the head being pushed, `581243c7`. Both are
answers to findings that record and the skill review
(`docs/skill-review/2026-09-02-live-spec-base.md`) already identified. No new ground.

**`33ee1b38` — the four restored rules, rule 10, and three code defects.** Each was checked against
what the two records actually asked for, and against a second reading of the range review's own
finding 2 in clean context (`.live-spec/checkpoints/q809-rule-loss-verdicts.md`), which put ten of
its sixteen claimed losses as surviving substance, four as genuine defects, one as a genuine
improvement, and eight of its claims as measurements of wording rather than of the rule. That
adjudication is appended to the review itself rather than replacing it, so the record stands with
its corrections readable beside it.

Verified here independently of the workers that proposed them: `skills/live-spec-base/SKILL.md`
carries the four restored sentences and rule 10's repair; `spec/project-setup-tuning.md:249` [A-9]
is what rule 10 now states, checked by reading the clause; `bash guardrails/check-pin-drift.sh`
green, 184 pins; `python3 scripts/check-shipped-language.py` green;
`python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md` green. The three code
defects (the done set comparing an icon against a hand mark, the reopened mark skipping the fold
bookkeeping, the line loop dropping done rows at budget exhaustion) each red the probe's own output
before the change and pass after; the vacuous assertion the earlier review named is replaced by
`TestADoneLineNamesARealClose`, which runs the probe in the real repository and re-derives the owed
set from `PLAN.md` at the branch's upstream rather than trusting the probe's own arithmetic.

**`581243c7` — one test re-pinned.** `tests/test_agent_channels.py` asserted the exact phrase
"names the sender's own blocked work", the exclusive form of the earned-message law. Widening the
rule to the grounds `spec/agent-request.md:25` recognises made that test red, so the test was
holding the rulebook at a shape whose cost is recorded in the guardrail's own source
(`guardrails/check-earned-message.py:128-130`, the 2026-07-17 correction, where a gate demanding
blocked work of everything refused the first real deposit). It now asserts the law and its first
ground and leaves the sentence free to name the others.

**Reason to refuse, looked for and not found.** The one this record went looking for: whether
widening rule 31 lets a message through that the guardrail should stop. It does not —
`guardrails/check-earned-message.py` is the mechanical arm and it already reads the three grounds;
the body had been the narrower of the two, which is the direction of the defect being repaired.

**Suite.** `python3 -m pytest -q` on this exact tree: 2738 passed, 6 skipped, 0 failed.

**Left open, recorded in the range review's adjudication and owed to their own rows:** q-806's
deliverable and the Fable review record were never brought forward after the owner answered the
question they wait on; `plan-0`'s acceptance passes on a fresh clone that never ran the migration;
`q-807`'s fixed-string greps stay green over a mutation that makes the blocked branch dead code.
