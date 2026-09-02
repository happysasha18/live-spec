# Prover record — 2026-09-02, reopened state and the open count

product-prover skill version reviewed against: no version line in this skill's own SKILL.md at
review time; ran the skill as loaded from `~/.claude/skills/product-prover/SKILL.md`, with the
pack bindings at `~/.claude/skills/product-prover-pack/SKILL.md`.

Reviewed: commit `72a52a4b` (spec-only slice of the range `c6ffc709..72a52a4b`) — the two spec
edits, `spec/wish-intake.md` Requirement 4 clauses 10-11 (INV-321, the reopened state) and
`spec/message-first-read.md` Requirement 314 clause 7's amendment plus new clauses 8-9
(INV-319, ranking/open-count/id-lead), read against what the same commit built:
`scripts/state-probe.sh`, `scripts/render-board.sh`, and their shared parser
`scripts/plan_checks.py` (`parse_tasks`, the `covered_by`/`deferred`/`blocked_by` fields). Also
read: `spec/work-board.md` Requirement 309 (the board's own, unbuilt columns), and
`~/.claude/playbook/CLAUDE.md` / `~/.claude/CLAUDE.md` — the single home
`scripts/plan_checks.py`'s own comment names for "which marks exist." Checks run:
`python3 -m pytest -q tests/test_plan_is_not_executable.py tests/test_board_matches_the_canon.py
tests/test_tasks_parser_finds_every_task.py` — 25 passed. A live read of `PLAN.md`'s current rows
through `parse_tasks` confirmed the concrete cases below (`plan-9`: marked `⬜`, carrying a
`**Deferred:**` line, excluded from the ranked/shown set).

This is a targeted review of the one spec delta named above, not a full push range: other lanes
are mid-edit on `PLAN.md`, `DECISIONS.md`, `NEXT_STEPS.md` and `scripts/plan_checks.py` in the
working tree, and this record touches none of them. It closes the specific gap
`guardrails/check-prover-record.sh` names — the newest committed prover record predates the last
`PRODUCT_SPEC.md`/`spec/` change — for this change.

Two of the new clauses hold up as written and as built: clause 11 (a reopened row draws in the
in-progress column) matches `render-board.sh`'s column map exactly, and R314 clause 7's amended
order matches `state-probe.sh`'s `CATEGORY_ORDER` exactly. The rest carry real gaps.

## Findings

**F1 — defect · boundary-issue (composition).** Reopened is computed purely from `mark == "✅"
and not ok`, with no read of `blocked_by`, `covered_by`, or `deferred` at all — the reweighting
block that reads those three fields only runs `if t["icon"] not in ("⛔", "⬜")`, and `🔁` is never
in that set.

> "distinct from blocked — a real cause outside the row, held in its own `blocked_by` — and from
> queued, which never started" — `spec/wish-intake.md`, Requirement 4, clause 10

Take a row marked `✅` that also carries `**Blocked by:** the vendor API is down` — a real,
already-named outside cause — whose acceptance command starts failing because that same vendor
API is down. The clause reads this as "distinct from blocked," but the row's own `blocked_by`
line names exactly the outside cause blocked is defined by. The code reads it as reopened anyway:
icon `🔁`, drawn in the in-progress column, ranked ahead of blocked and queued, printed with no
mention of the `blocked_by` reason state-probe.sh prints for a genuine `⛔` row. A person scanning
the Canon sees "live work in hand" for a row that is, by its own recorded field, stuck on
something outside it. The same silent drop applies to `covered_by` (a row whose work is actually
carried by another task) and `deferred` (his own decision to hold it) — both are read for `⛔`/`⬜`
today, on purpose, per the code's own comment, and neither is read for `🔁` at all.
Fix: state which field wins when a row is both reopened-shaped and carries `blocked_by` — the
cheaper reading, matching the shipped `⛔`/`⬜` precedent the code already reasons through, is that
a populated `blocked_by` on such a row keeps it blocked, and reopened applies only where
`blocked_by`/`covered_by`/`deferred` are all empty. Write that sentence into clause 10, and extend
`state-probe.sh`'s reweighting set to include `🔁`.

**F2 — defect · missing-outcome-check (postcondition).** Clause 10 states the entry condition for
reopened and never states its exit.

> "a row once closed and closed no longer" — `spec/wish-intake.md`, Requirement 4, clause 10

What state does a reopened row read as once its acceptance command passes again? The code answers
this mechanically — `t["icon"] = "🔁" if failing_key else ("✅" if ok else t["mark"])` — the row
snaps straight back to `✅` on the next run where the command passes, with no hand edit and no
distinct "reopened, closed again" language; it is indistinguishable from a row marked done for the
first time. Nothing in clauses 10-11 or in R314 says this is the intended exit, so a reader of the
spec alone cannot tell whether the intended path back is this automatic flip, or a person's own
hand-edit of the mark (the way clause 9 describes marks changing generally). Fix: add one sentence
to clause 10 naming the exit — "the row reads as done again the next time its acceptance command
passes, with no separate mark for a row reopened once versus done from the start."

**F3 — defect · missing-rule (invariant).** The "open" clause 8 introduces is not the same set the
ranking logic already calls open.

> "lead the printed account of open work with a count of the rows not done" — `spec/message-first-read.md`,
> Requirement 314, clause 8

`state-probe.sh` defines `open_count = len(tasks) - done_count`, over every row in `PLAN.md`. But
the same file's own ranking already carves a narrower set: a row that is `deferred` or `covered_by`
with no `blocked_by` is explicitly excluded as not competing — "neither is blocked, so neither
competes for the board's top slots; they drop out of the current set." `plan-9` is exactly this
today: marked `⬜`, carrying `**Deferred:** after the release (his word)`, excluded from `eligible`
and from `shown`. It is still counted in the leading `open_count`, and — the same root cause —
also inflates `more_below`, which is computed the same way (`t["id"] not in shown_ids and
t["icon"] != "✅"`, not `t["excluded"]`). Clause 8 doesn't say which "open" it means; the person
reading "N open" now gets a number one larger than the count of rows the tool itself treats as
live, competing work. Fix: name the set explicitly — either "every row not marked done, deferred
rows included" (and say why a deferred row still counts as open work outstanding), or "every row
not excluded from ranking" (and have `open_count`/`more_below` both read off `eligible` the way
the ranking already does).

**F4 — defect · direct-contradiction (contradiction).** The single home
`scripts/plan_checks.py`'s own comment names for the mark vocabulary was not updated with this
delta.

> "Which marks exist and what each means is not decided here: that has one home, the owner's own
> `~/.claude/playbook/CLAUDE.md`, 'How a reply to him looks'." — `scripts/plan_checks.py`,
> `_CANONICAL_MARKS`'s own comment

Both `~/.claude/playbook/CLAUDE.md` and `~/.claude/CLAUDE.md` (identical text at that section)
still read: "Five marks and no more get invented: ✅ done · 🔄 in hand · ⬜ queued · ⛔ blocked ·
👁️ needs his eyes." `🔁` is not among them, and `_CANONICAL_MARKS` in `plan_checks.py` does not
carry it either — it is computed, never typed, so it never round-trips through `normalize_mark`.
This is the exact "two homes for one fact" shape `state-probe.sh`'s own ALARM section already
watches for elsewhere (`evals/director.md` vs `evals/director/`). Fix: add the sixth mark to the
"Five marks and no more" line at its one home, or state in clause 10 that reopened is deliberately
a computed-only icon exempt from the typed-mark legend — as written today, the code's own citation
and the cited file disagree.

**F5 — recommendation · now · boundary-issue (composition).** `spec/work-board.md` Requirement
309 was left alone on purpose (the commit's own words), but its own text ties itself to the same
entity this delta changed, and its closed enumeration is now stale under one reading of that tie.

> "an open row's column read off the status its queue row records" — awaiting validation reads off
> *queued*, ready off *ready*, and in work off *in-work* — `spec/work-board.md`, Requirement 309,
> clauses 20-22

R309's own context paragraph opens "A task reaches the work board when its wish is captured,
before its statement is validated" — the same "wish captured" language `spec/wish-intake.md`
Requirement 4 uses for its own rows, which reads as the same entity rather than an unrelated one.
Read that way, R309's three-way closed enumeration (queued/ready/in-work) was already short one
state before today (there is no `👁️`/needs-eyes mapping in clause 22, only a separate blocked
clause 18) and is now short two, with reopened nowhere in the file. `render-board.sh`'s own header
comment reads R309 as a different, host-generic queue, not this project's `PLAN.md` rows — if that
reading is the intended one, neither file says so, and the "queue row" wording each uses is
identical enough that a later reader has no way to tell the two apart from the text alone. Not
blocking: the feature is `[target]`, unbuilt, and no test or gate reads R309 today. Fix: pick one
reading and write it — either name R309's "queue row" as a distinct, host-generic status field
disjoint from `PLAN.md`'s own marks (and say so in both files), or, if it is the same field,
re-open clause 22's enumeration when the feature is actually built rather than carrying a stale
closed list forward.

Class lens: swept — F1 and F3 share one class, a leading/summary figure or a ranking exclusion
computed over the wrong set (`tasks` where the code elsewhere already has a narrower, reasoned
set: `eligible`, or the `⛔`/`⬜`-only reweighting). Checked whether `🔄` and `👁️` have the same gap
as `🔁` in F1 — they don't: the code's own comment explicitly reasons through excluding them from
the fold-bookkeeping reweighting ("a task already in hand or needing his own decision is live
regardless of any fold bookkeeping"). `🔁` is the one state added without that same reasoning being
extended to it.

## Verdict

Needs another iteration, not significant rework. Two clauses (R314 cl. 7, wish-intake cl. 11)
hold as written; two (wish-intake cl. 10, R314 cl. 8) each owe one added sentence (F1/F2's exit
and precedence rule, F3's definition of "open"); F4 is a one-line fix outside this repo, in the
file the code itself names as authoritative. F5 is a scoping question for the owner, not a block.
