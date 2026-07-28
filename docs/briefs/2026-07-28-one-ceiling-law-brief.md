# Brief — one ceiling law, one home

Written 2026-07-28 for one worker starting with an empty context. Every anchor is named below by path.

## What happened an hour ago

A worker landed the findings-record ratchet. Requirement 302 gained a case named "the record moves only down", carrying criteria 9, 10 and 11.

Criterion 11 was copied word for word from the prover record. The prover record had itself copied it from criterion 18 of Requirement 297.

The two sentences now differ in one word: the record each names.

The sibling sits at `PRODUCT_SPEC.md:7117`, and it reads:

> 18. A raised recorded count *shall* be a hand edit to the config stating its reason, run through this same pipeline. [INV-288]

The new one sits at `PRODUCT_SPEC.md:7310`, and it reads:

> 11. A raised recorded count *shall* be a hand edit to the record stating its reason, run through this same pipeline. [INV-301]

`scripts/spec-redundancy-precheck.py` counted that as a new duplicate pair. The test `test_live_spec_sits_at_the_clean_floor` went red at 120 against a floor of 119.

The worker raised the floor in `scripts/spec-debt-cap.json` from 119 to 120. Its reason is recorded beside it, in the field `_reason_redundancy_PRODUCT_SPEC`. The worker flagged the raise as the session lead's call.

## Why it matters

This repository runs a campaign whose second goal is a specification that stops growing. The goal is stated in `docs/plans/2026-07-28-two-goals-one-campaign.md`.

A recorded number that may only fall is the law that same landing shipped. So a landing forbidding a rise, while raising a neighbouring ceiling by hand, argues against itself.

Your job is to settle that, in three parts.

## Part one — the attempt

State criterion 11 so the law lives in one home. Requirement 302 then points at that home, over its own record.

The rule you serve is rule 4 of `skills/live-spec-base/SKILL.md`, at lines 67 to 69. It reads:

```text
4. **One canonical home per fact.** Everything else that mentions the fact is a pointer, and pointers are
   kept live — a doc superseded or moved gets every inbound reference repointed the same session. Two
   documents claiming authority over one fact is undefined behaviour when they disagree.
```

One question comes before any edit. May a criterion in this specification reference another requirement's criterion at all?

Settle that question from the repository before you write a word of the new criterion.

**The gates that judge criterion text.** Read each one, because each can refuse your form:

- `guardrails/check-requirement-shape.py`;
- `guardrails/check-criterion-readability.py`;
- `guardrails/check-deferral-marker.py`;
- `scripts/spec-style-lint.py`.

**The genre the criterion is written in.** It is stated in `docs/spec-format.md` and `docs/spec-style.md`. Read both.

**The precedent.** An existing cross-reference between two requirements is the form you follow. Search for one, and follow what you find rather than invent a shape.

A first pass ran three searches over `PRODUCT_SPEC.md` and each returned nothing:

- a numbered criterion line carrying the word "Requirement" and a number;
- a numbered criterion line carrying a code of the form `R297.18`;
- an indented bullet under a criterion carrying the word "Requirement" and a number.

Search wider than those three before you conclude. Report the searches you ran and what each returned.

Criterion 11 today carries three indented bullets beneath it, at `PRODUCT_SPEC.md:7311` to `:7313`. Decide what happens to them, and say why.

## Part two — the verdict

Run these with the new wording in place:

- `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`;
- the four criterion gates named in part one;
- the tests over the debt cap and the redundancy floor.

**When the count returns to 119.** Restore `scripts/spec-debt-cap.json` to 119. Rewrite its `_reason_redundancy_PRODUCT_SPEC` field so the note about the raise disappears.

Keep the field's earlier history word for word. That history runs from the sentence beginning "Lowered 121 to 119" to the end of the field, and every word of it survives your edit.

**When a gate refuses the reference form.** Put the copied sentence back, leave the floor at 120, and stop there.

Report which gate refused, and quote the words it printed.

Both outcomes are a success for this brief. The one failure is an unreported guess.

## Part three — the finding

Four requirements in this specification carry the same ceiling law over four different records:

- Requirement 245 at `PRODUCT_SPEC.md:5734`, over the document byte bounds;
- Requirement 280 at `PRODUCT_SPEC.md:6653`, over the bytes-per-criterion ratchet;
- Requirement 297 at `PRODUCT_SPEC.md:7084`, over the criterion-readability config;
- Requirement 302 at `PRODUCT_SPEC.md:7279`, over the document findings record.

The prover record names all four in its Composition paragraph, at `docs/prover/2026-07-28-requirement-302-findings-ratchet.md`, lines 100 to 104.

Four statements of one law are a specimen of what the campaign's second goal hunts. Write the specimen up as a queue item.

The item describes what the four requirements share, and it proposes that one requirement carry the law with the record as its parameter.

**You build no such merge in this pass.** The queue item is the whole deliverable of part three.

Say that to yourself again before you start part three. **The merge is out of scope here, and a queue item is what you write.**

**Where the item goes.** Find the home the repository gives a queue item. `ROADMAP.md` and `NEXT_STEPS.md` are the two candidates, and `docs/roadmap-format.md` states the row shape.

Another worker holds `NEXT_STEPS.md` right now, so that file is closed to you. `ROADMAP.md` is open, its highest row is 519, and `NEXT_STEPS.md` names row 520 as free.

Write the item into your report instead when you find every queue home held. Say plainly in the report that you did so, and give the item in the words you would have written into the file.

## What you must not touch

Two other workers are editing this tree right now.

The first holds `hooks/chat-law-hook.sh`, `hooks/language-laws.json`, `tests/test_chat_law_hook.py`, `skills/text-audit/SKILL.md`, and `docs/language-reads/2026-07-28-read16-chat-law-hook.md`.

The second holds `DECISIONS.md`, `NEXT_STEPS.md`, `docs/plans/2026-07-28-two-goals-one-campaign.md`, `docs/handovers/2026-07-28-readability-campaign-handover.md`, and the message under `inbox/`.

Leave all ten alone.

Make every change as a targeted edit to the lines you mean to change. A whole-file rewrite in a shared tree destroys another worker's concurrent edit.

Commit nothing and push nothing. The session lead does that.

Re-seed `guardrails/rule-census.json` never. A re-seed is no way to make a check green.

Leave `JOURNAL.md` to the session lead, and report the line it owes.

## The writing standard your prose is held to

Every document this repository ships is measured. Keep each sentence at or under 25 words. Use plain product words. Keep an internal code out of the front of a sentence, where it names nothing to a reader. A sentence that names a thing by denying its neighbour is refused.

`PRODUCT_SPEC.md` is recorded at 1831 findings and measures 1831 findings, so it carries no headroom at all. Any sentence you write into it must add no finding.

`ROADMAP.md` is recorded at 215. A row you add there is held to the same standard.

Rebuild the index whenever criterion text changes: `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md`. The same table is embedded in the specification under `## Reference`, and the two copies must match line for line.

## The checks that close the work

Run each command from the repository root and record what it printed:

1. `python3 scripts/rule-census.py PRODUCT_SPEC.md ROADMAP.md`
2. `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md`
3. `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md`
4. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md`
5. `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md`
6. `python3 guardrails/check-doc-findings-bound.py`
7. `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`
8. the tests over the debt cap and the redundancy floor, run by name
9. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log

Find the real names for step 8 rather than trusting a name handed to you. One place to start is `tests/test_convergence_locks.py`, which holds `test_live_spec_sits_at_the_clean_floor` and `test_debt_cap_only_downward`. Search the whole `tests/` directory for every file naming `spec-debt-cap.json` or `spec-redundancy-precheck.py`, and run all of them.

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is no test result, so quote the log.

## What done means

Report these eight things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- your answer to whether a criterion may reference another requirement's criterion, with the gate text or the precedent that settled it;
- the searches you ran for a precedent, and what each returned;
- criterion 11 as it now stands, quoted from the specification, with what became of its three bullets;
- the redundancy count before and after, quoted from the check's own output;
- the value in `scripts/spec-debt-cap.json` and its reason field as they now stand;
- the name of every test you ran for step 8, and its result;
- the full-suite counts quoted from the suite log.

Report the queue item you wrote for part three, and the file it went into. Report the census count for every document you edited, beside the count it held before. Report anything you found and left alone.
