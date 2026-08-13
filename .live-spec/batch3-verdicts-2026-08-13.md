# Stage-2 batch 3 — base rule 29, the deferral test — 2026-08-13

Root: the accepted culling plan `.live-spec/culling-plan-v3-2026-08-10.md`, stage 2 (accepted
2026-08-11 21:22), batch 3 on base rule 29; the session order of 2026-08-13 08:27 runs it.

## The rule

- Number 29, heading: **A deferral must justify itself, or the item is the seat's to do (SPEC INV-152).**
- Home: `skills/live-spec-base/SKILL.md`. Span before the rewrite: lines 471-493. Span after: 471-487.
- Span verified live before any edit: heading at 471, rule 31's heading at 494, so the census span
  convention gives 471-493.
- **Body bytes: 2,138 → 1,693 (−445, −20.8%).** The opening figure matches the day-1 census
  (`.live-spec/day1-census-rules.md:41`) and the S1 re-measurement to the byte.
- All eight codes the body carried are still in it: INV-152, INV-59, INV-121, INV-143, INV-151,
  INV-153, INV-155, INV-28. Both script paths stay in the body, and the heading still opens with
  `29. **A deferral must justify itself`, the literal `tests/test_minor_gate_reconciliations.py:44`
  pins.

Where the bytes came from. S1 priced blocks F and G at 1,125 bytes, 52.6% of the rule: the kinship
retelling and the prose descriptions of the two machines. Both blocks also carry live requirements
(7, 8, 9, 10), so they compress rather than disappear. Block F is now one sentence naming rule 27's
posture and one naming rule 15's twin with the routing principle. Block G is now one sentence per
arm, each keeping its file path and its code, with the machines' behaviour left where it is already
described: `PRODUCT_SPEC.md` R212.4 and R212.5, matrix rows M-297 and M-302, the gate's own
docstring, and `guardrails/README.md:137`. No text moved into an appendix or a reference file.

## The ten requirements and the sentences that carry them

Carrying sentences are quoted from the new body; the reach of each demand is the S1 inventory's.

1. **A marked item is re-tested for derivability at every touch.** Carried by: "A backlog item
   carrying a needs-the-human's-word marker is re-tested by derivability at its first writing and at
   every touch after." Reaches any seat that writes or touches a parked backlog item, in any project
   on the pack.
2. **Three surfaces carry such a marker.** Carried by: "Three things carry such a marker: a queue row
   held for the human's word, a `NEXT_STEPS.md` line, and a decision a setup script leaves open."
   Reaches a seat writing in the queue, in the resume file, or in a setup script's decision page.
3. **A pinned answer makes the item the seat's own.** Carried by: "Where the answer pins to an
   existing artifact — a base rule, a spec sentence, the architecture, an approved prototype, or an
   already-answered decision [INV-59] — the item is the seat's: do it, cite the artifact, and drop
   the marker [INV-121, INV-143]." Reaches the seat holding the parked item.
4. **A fact no artifact holds keeps the item with the human.** Carried by: "Where it needs a fact no
   artifact holds — a taste, a policy, an act irreversible outside git (rule 17), or the feel of a
   real device in the human's own hands — it is the human's, and the marker stands." Reaches the seat
   deciding whether to park, and the human who receives the parked item. This is the sentence the GAP
   resolution widened from three facts to four.
5. **Writing a marker requires naming the human-only fact.** Carried by: "Writing such a marker
   requires naming that human-only fact; a marker that cannot name it defaults to the seat's and is
   itself the finding." Reaches the seat writing the marker, at commit time.
6. **An unjustified marker is itself the finding.** Carried by the closing clause of the same
   sentence: "a marker that cannot name it defaults to the seat's and is itself the finding." Reaches
   the seat reading the parked item, and any reviewer sweeping the resume file.
7. **The posture binds the orchestrator seat at any tier.** Carried by: "The posture is rule 27's,
   applied to a backlog item, and it binds the orchestrator seat whatever tier holds it." Reaches
   every seat in the orchestrator role, on Opus, Sonnet, or Haiku. The old label for the control and
   the phrase describing rule 27's posture are gone; the demand they wrapped stands in the sentence
   above.
8. **Everything incoming routes to the home whose sentence governs it.** Carried by: "Rule 15's
   closed door set is its twin [INV-151]: one routing principle covers both, that every incoming
   thing routes to the home whose declared sentence governs it, and a thing that pins to no home is
   itself the finding [INV-153]." Reaches every seat handling any incoming item — a request, a parked
   row, a property, a message.
9. **The mechanical arm reds a commit on a reasonless park.** Carried by:
   "`guardrails/check-deferral-marker.py` reds a commit where a parked item in the resume file or a
   decision page names none of the four [INV-155]." Reaches the pack's own maintainers and every host
   that installs the commit hook. The gate's reach — the resume file and a decision page — stays
   stated, so the rule still claims no mechanical enforcement wider than the commit gate wires
   (M-297's own prohibition).
10. **The delivery arm re-fires the test where the leak happens.** Carried by: "The deferral line of
    `hooks/chat-law-hook.sh` re-fires the test the moment a marker is written or an `AskUserQuestion`
    is opened; it reminds and cannot block (SPEC INV-28)." Reaches the seat in chat, at the moment it
    opens a question to the human.

## The GAP resolution

`PRODUCT_SPEC.md:5129` carried a recorded gap: the rule's prose named three human-only facts (taste,
policy, an act irreversible outside git) while the mechanical net accepted four reason categories,
device-feel standing only in the net's list. It resolves to the **four-category** list: a taste, a
policy, an act irreversible outside git, and the feel of a real device.

Ground:

- The standing session law names four and calls an unnamed marker the finding. `hooks/chat-law-hook.sh`,
  law 6: park only what needs their taste, a policy call, an act that cannot be undone, or a real
  device, and name which one; a marker or a question that cannot name one of the four is itself the
  finding.
- The gate already accepts the fourth. `guardrails/check-deferral-marker.py:85-89` lists
  `taste`, `policy`, `irreversible`, and `device-?feel` / `device feel` / `real device` as its core
  reasons, and `:220-221` prints the same four in its finding line.

One correction to the premise the order carried into this lane: the personal profile does **not**
name the device case. `~/.claude/live-spec/profile.md:31` names three facts and carries no device
clause, so the ground for the four-list is the session law plus the gate, and the profile's own line
is the remaining three-fact site. Repairing it falls outside this lane's write-set.

The `[GAP]` line is removed from the spec, and the four-list now stands in the rule body, in the
spec's context paragraph, in spec criterion R212.2, and in matrix rows M-297 and M-302.

## S3 — clean-context check

One round, one fresh Sonnet subagent, given only the ten requirement quotes and the new rule text,
with no repo access.

**Verdict: PASS.** Ten of ten requirements carried, zero misses. Each prohibition binds the same
actor in the same case as before — the unjustified marker defaults to the seat's, the hook reminds
and cannot block, and "itself the finding" still binds in both of its original cases (the unnamed
marker and the unhomed thing). No narrowing found. No sentence of the banned contrast shape. The
jargon list it returned holds the pack's own standing vocabulary — seat, tier, derivability, backlog
item, closed door set, resume file, decision page, the INV codes and the two script paths — and no
term this rewrite minted.

## S4 — surfaces and tests

Spec, index, matrix:

- `PRODUCT_SPEC.md` Requirement 212: the context paragraph and criterion 2 now carry the four-list,
  and the `[GAP]` line under criterion 4 is deleted. Live lines 5118, 5127, and criteria 4 and 5 now
  adjacent at 5132-5133.
- `PRODUCT_SPEC.index.md:211`: no change. Requirement ids R212.1 through R212.5 are unchanged, so the
  INV-152 row still reads true.
- `TEST_MATRIX.md:177` (M-297) and `:178` (M-302): each row restated the human-only-fact list in
  three items and now states four. Nothing else on either row changed.
- The three strings the suite pins inside the spec block are untouched: "A deferral must justify
  itself", "re-tested for derivability every time it is touched", and "default a marker that cannot
  name its human-only fact to the seat's own".

Test run, raw:

```
$ python3 -m pytest tests/test_chat_law_hook.py tests/test_code_anchor_scan.py \
    tests/test_deferral_marker.py tests/test_expensive_decision_read.py \
    tests/test_hedge_arm.py tests/test_request_classifier.py -x -q
........................................................................ [ 84%]
.............                                                            [100%]
85 passed in 2.06s
exit 0
```

No failing lines. The run above is the lane's own re-run after the subagent's, on the same tree, with
the same result.

Gates, raw:

```
$ python3 guardrails/check-deferral-marker.py
exit 0            (no output; the script defaults to ./NEXT_STEPS.md and ./docs/decisions/*.md)

$ python3 guardrails/check-one-name.py skills/live-spec-base/SKILL.md
check-one-name: OK — reach: files=[SKILL.md]; matched 0 of 13 rows scanned; no known alias
present across 13 alias(es) of 5 artifact(s)
exit 0

$ python3 guardrails/check-one-name.py skills/build-pipeline/SKILL.md
check-one-name: OK — reach: files=[SKILL.md]; matched 0 of 13 rows scanned; no known alias
present across 13 alias(es) of 5 artifact(s)
exit 0

$ python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md
OK (preshow-register): no coined metaphor, calque, or transliterated pack term found.
exit 0
```

## The two inherited questions

- **Queue row 539, the one-name lint.** The row records that rule 29 breaks the pack's own one-name
  lint at two lines, and that `check-one-name.py` passed clean over both skill bodies at the HEAD of
  2026-08-05. The freshness re-check the row asks for was run here. `check-one-name.py` exits 0 on
  `skills/live-spec-base/SKILL.md` and on `skills/build-pipeline/SKILL.md`, both before the rewrite
  and after it. The rewrite keeps the canonical noun `backlog item` and introduces none of its
  aliases. On the live tree the two-line claim in row 539 has no live instance the lint can see; a
  drift the alias file does not yet know stays the cold-reader panel's catch, by the lint's own
  stated bound.
- **Queue row 451, the definition of taste.** The row leans on this rule for the working definition
  of the word through the derivability test. The rewrite keeps that test stated whole: an answer that
  pins to an existing artifact makes the item the seat's, and an answer needing a fact no artifact
  holds — the first of the four being a taste — makes it the human's. Both halves of the boundary
  stand in the body, so the definition row 451 borrows is intact and now names four facts instead of
  three.

## Rulebook volume

Measured with the plan appendix's fixed command:

```
{ find skills/live-spec-base -name '*.md' -not -name 'README.md' -print0 | xargs -0 cat; cat ~/.claude/live-spec/profile.md; } | wc -c
```

- Before the batch: **72,466 bytes**, matching batch 2's closing figure exactly, no drift.
- After the batch: **72,021 bytes**.
- Net fall: **445 bytes**, the whole of it rule 29's body. The batch's own test — volume at close
  below volume at open — **passes**.

## Left open

- `guardrails/check-deferral-marker.py:5-6` names three human-only facts in its docstring while its
  own `CORE_REASONS` at `:85-89` accepts four. The docstring is now the last three-fact site inside
  the gate itself, and it sits outside this lane's write-set.
- `~/.claude/live-spec/profile.md:31` names three facts. Same class, same reason for leaving it.
- Neither is red anywhere: no test pins either text against the rule.
