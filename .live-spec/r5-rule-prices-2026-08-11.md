# R5 — pricing the 53 rules outside the shared rulebook

Pins verified by `guardrails/check-pin-drift.sh` (its r5 leg, ROADMAP row 588) — run it after any edit to a home file above; a rotted `path:start-end` pin reds.

Root: the frozen plan `.live-spec/culling-plan-v3-2026-08-10.md`, step R5. The day 1 census, `.live-spec/day1-census-rules.md`, measured only the 35 rules in `skills/live-spec-base/SKILL.md`. The plan's queue for the next phase runs from the most expensive rule first, and it needs a price for every rule the day 1 census left out. This page prices those rules: the ones that live inside the nine working skill files rather than the shared rulebook.

## The count check

`NEXT_STEPS.md:15` today does not carry the 88-rule claim. The line that names it moved to `NEXT_STEPS.md:26` ("Rules cut: 0 of 88."), because the live-state block above it grew between when the plan cited line 15 and today. The citation drifted with that edit. The number itself holds steady: 88 total rules, 35 shared plus 53 in the working skills, is stated in three places — `.live-spec/culling-plan-v2-2026-08-09.md` line 18, `.live-spec/handover-2026-08-09.md` line 40, and `NEXT_STEPS.md` line 26.

**Finding the 53.** Neither the plan nor the day 1 census writes down how a "rule" is told apart from a process step inside a working skill's file. The day 1 census identified all 35 rules in `skills/live-spec-base/SKILL.md` the same way: each is a top-level numbered list item with a bold lead-in sentence, for example line 110, `1. **Ask, never guess.** A gap only the human can fill...`. Applying that same shape — a line matching `^[0-9]+\. \*\*` at the start of the line, inside the skill's own `SKILL.md` body — to the nine working skills (`build-pipeline`, `communicator`, `design-reviewer`, `feedback-intake`, `product-prover`, `publish`, `spec-author`, `test-author`, `text-audit`) returns exactly 53 items. `feedback-collector` is not one of the nine: its own file states it is "off by default" and silent unless a host turns it on, so it sits outside the working set the plan counts (`skills/feedback-collector/SKILL.md` line 22).

This shape does not match every skill evenly. Three skills — `product-prover`, `publish`, and `feedback-intake` — carry numbered lists too, but none of their numbered items open with a bold lead-in phrase, so this method counts zero rules in each of them. `communicator` carries its own explicit list of twenty-two items it calls rules and marks `(rule 1)` through `(rule 22)`; those are written with dashes, so this method skips them. The six items this method counts inside `communicator` come from a different, numbered list further down the same file, "the pre-report walk." The count still lands on exactly 53, the same number the plan states. That match is this session's own reading of an undefined convention landing on the plan's number, worth flagging as a coincidence to confirm rather than treating as settled. A session that instead counted communicator's twenty-two self-declared rules, or counted every numbered list regardless of bold lead-in (which would add product-prover's and publish's process lists), would reach a different number. This gap in the method is itself worth a line in the plan.

**Method for each column below.**

- **Home file** — the skill's `SKILL.md`, with the line range the rule's own text occupies. A rule's span runs from its own numbered line to the line before the next numbered item in the same list, or the next heading, whichever comes first — the same boundary rule day 1 used to keep one rule's text from swallowing its neighbor's.
- **Opening line** — the rule's own first line, quoted exactly as written, numeral and bold lead-in included.
- **Body bytes** — `len(text.encode("utf-8"))` over the exact line range above, counted with a short Python script reading each file directly (the same unit day 1 used for the 35 shared rules).
- **Pinned tests** — a rule's own SPEC codes (`INV-`, `T-`, `E-`, `ACT-`, `M-`, `A-` followed by a number), read out of its body text, searched with `grep -rlF '<code>' tests/` and counted as the union of distinct files any of its codes hit. Nineteen of the 53 rules cite no such code in their own text; for those, the search falls back to the rule's bold lead-in phrase itself (quotation marks and markdown stripped) as the `grep -rlF` pattern, and the exact phrase used is named next to each such row. A rule with no code and a lead-in too generic to search safely ("Purpose", "Entities", "Actors") still ran the same search on that word and returned zero, which the table reports as zero rather than skipping the row.
- **Price** — body bytes plus pinned-test count, the plan's own starting cost measure (`.live-spec/culling-plan-v3-2026-08-10.md` line 86).

**Totals.** 53 rules found. 46,121 body bytes in all. 310 pinned-test hits in all, summed across rules (a test file pinning more than one rule is counted again for each). Combined price: 46,431.

**Repaired at HEAD.** The pins above were re-derived against commit `a5b94f85b8bd607e0ff462eb9e07e0c96235354d` (2026-08-12): every row's home file, line range, body bytes and pinned-test count were re-measured by the same methods stated above. All 53 rules still exist under their original title and number; 48 of the 53 line ranges had drifted (later edits to the same skill files shifted them), and 3 rows' pinned-test counts moved by one file because `tests/` itself changed since d11331f. No row's price-rank order changed.

**Re-pointed after the spec-author offload (2026-08-17).** Nine sections of `skills/spec-author/SKILL.md` moved word for word into `skills/spec-author/references/`. Seven of this page's spec-author rows — the seven items of the spine — now live in `skills/spec-author/references/the-spine.md`, and the ten that stayed in the body shifted up. Every affected row's home path and line range was re-derived by matching its exact text in the new tree. No rule's text, body-byte count, pinned-test count or price changed, and no row's price-rank order changed: the move was verbatim.

## The price table, most expensive first

| # | skill | home file : lines | opening line | body bytes | pinned tests | price |
|---:|---|---|---|---:|---:|---:|
| 1 | build-pipeline | `skills/build-pipeline/SKILL.md:404-470` | 8. **Verify by deed.** Run it and see the result with your own eyes. Only call it done/working af... | 5,954 | 32 | 5,986 |
| 2 | build-pipeline | `skills/build-pipeline/SKILL.md:286-352` | 3. **Architecture — write or update `ARCHITECTURE.md` from the proven spec** (template: | 5,705 | 20 | 5,725 |
| 3 | build-pipeline | `skills/build-pipeline/SKILL.md:471-500` | 9. **Commit & show.** Commit when green with no regression (unasked) — same or better is enough, ... | 4,028 | 14 | 4,042 |
| 4 | spec-author | `skills/spec-author/references/the-spine.md:21-50` | 7. **Terms** — every domain term is defined in the glossary, once, under one name. A word of ordi... | 2,286 | 25 | 2,311 |
| 5 | communicator | `skills/communicator/SKILL.md:459-479` | 6. **Account for every removal of substance (SPEC INV-109).** When the movement being reported re... | 2,292 | 7 | 2,299 |
| 6 | build-pipeline | `skills/build-pipeline/SKILL.md:263-285` | 2. **Prove — invoke `product-prover`.** The prover only catches a cross-section hole when both si... | 2,230 | 7 | 2,237 |
| 7 | build-pipeline | `skills/build-pipeline/SKILL.md:243-262` | 1. **Spec — invoke `spec-author`.** Write or grow the project `PRODUCT_SPEC.md`: entities, states... | 1,625 | 49 | 1,674 |
| 8 | build-pipeline | `skills/build-pipeline/SKILL.md:364-380` | 5. **Test spec — invoke `test-author` to DERIVE `TEST_MATRIX.md` from the proven spec through the... | 1,466 | 10 | 1,476 |
| 9 | text-audit | `skills/text-audit/SKILL.md:173-193` | 5. **Read again, and close on two clean rounds.** After the fixes land, hand the text to a fresh ... | 1,473 | 0 | 1,473 |
| 10 | build-pipeline | `skills/build-pipeline/SKILL.md:385-403` | 7. **Code — implement until green.** Delegate well-scoped, mechanical implementation to a junior ... | 1,452 | 2 | 1,454 |
| 11 | text-audit | `skills/text-audit/SKILL.md:152-169` | 3. **The auditor merges the two lists.** The auditor is the session running this skill, and the m... | 1,179 | 0 | 1,179 |
| 12 | communicator | `skills/communicator/SKILL.md:449-457` | 4. **Run the register lint — a hard BLOCK (SPEC INV-83).** Feed every human-facing | 1,039 | 9 | 1,048 |
| 13 | spec-author | `skills/spec-author/SKILL.md:193-202` | 1. **Author / grow the relevant requirement** in `PRODUCT_SPEC.md`: find (or open) the requiremen... | 1,044 | 3 | 1,047 |
| 14 | build-pipeline | `skills/build-pipeline/SKILL.md:353-363` | 4. **Prove the architecture — invoke `product-prover` with the architecture lens** whenever the doc | 1,003 | 27 | 1,030 |
| 15 | test-author | `skills/test-author/SKILL.md:64-74` | 8. **Close by the mechanical gates, not a hand-walked list.** The coverage checklist the matrix once | 941 | 0 | 941 |
| 16 | design-reviewer | `skills/design-reviewer/SKILL.md:204-215` | 3. **Every position behaves alike.** The same gesture on the same type in a different slot behave... | 859 | 7 | 866 |
| 17 | design-reviewer | `skills/design-reviewer/SKILL.md:131-139` | 1. **Enumerate.** Build your own inventory of the elements. Use the prover's Phase 1 extraction h... | 751 | 9 | 760 |
| 18 | communicator | `skills/communicator/SKILL.md:458-458` | 5. **Legibility floor (a BLOCK, SPEC INV-139).** For any STYLED artifact about to be shown — an H... | 748 | 4 | 752 |
| 19 | test-author | `skills/test-author/SKILL.md:56-63` | 7. **A norm-pointered clause owes a norm-conformance row.** When a spec clause carries a | 711 | 2 | 713 |
| 20 | communicator | `skills/communicator/SKILL.md:444-448` | 3. **Run the mechanical check** — feed the drafted prose to `python3 scripts/preshow-lint.py -` a... | 620 | 24 | 644 |
| 21 | text-audit | `skills/text-audit/SKILL.md:145-151` | 2. **Hand the text to two fresh cold readers.** Both sessions hold zero context on the text's his... | 549 | 0 | 549 |
| 22 | design-reviewer | `skills/design-reviewer/SKILL.md:148-154` | 4. **Check parity.** For each candidate group, list the declared interactions of each member from... | 537 | 0 | 537 |
| 23 | design-reviewer | `skills/design-reviewer/SKILL.md:155-162` | 5. **Fire the tight ask.** A divergence becomes a finding only when the signal is strong. Every | 517 | 0 | 517 |
| 24 | design-reviewer | `skills/design-reviewer/SKILL.md:199-203` | 2. **Every object type behaves alike.** Each kind of thing the gesture acts on — a gallery frame, a | 425 | 1 | 426 |
| 25 | design-reviewer | `skills/design-reviewer/SKILL.md:195-198` | 1. **Entry mirrors exit.** A layer that opens by a motion from its source closes by the reverse of | 398 | 1 | 399 |
| 26 | test-author | `skills/test-author/SKILL.md:52-55` | 6. **Matrix-local row ids are legal, spec anchors stay the parent.** One spec fact may project into | 387 | 0 | 387 |
| 27 | test-author | `skills/test-author/SKILL.md:48-51` | 5. **Name the state space before filling cells.** Axes first: view states (mode, toggles), data | 374 | 0 | 374 |
| 28 | spec-author | `skills/spec-author/references/the-spine.md:16-19` | 5. **Invariants** — the properties that must hold across *every* reachable state, stated as crite... | 373 | 0 | 373 |
| 29 | text-audit | `skills/text-audit/SKILL.md:141-144` | 1. **Run the mechanical lints, and fix every hit.** Run every check that a script or a grep can d... | 361 | 0 | 361 |
| 30 | build-pipeline | `skills/build-pipeline/SKILL.md:381-384` | 6. **Test — with `test-author`, write tests that assert the REAL shipped artifact.** Render the w... | 355 | 0 | 355 |
| 31 | communicator | `skills/communicator/SKILL.md:440-443` | 2. **Pass the draft phrase by phrase through one question:** *does this sentence stand for a read... | 344 | 0 | 344 |
| 32 | communicator | `skills/communicator/SKILL.md:437-439` | 1. **Re-read the rules above, and the full writing register** — open this file and read the live ... | 340 | 0 | 340 |
| 33 | spec-author | `skills/spec-author/SKILL.md:210-214` | 5. **Then walk the two layers to the tests** — the architecture doc (nodes owning the spec's facts, | 337 | 0 | 337 |
| 34 | design-reviewer | `skills/design-reviewer/SKILL.md:140-144` | 2. **Describe by role.** For each element, write its role sentence: "a photo a viewer opens large to | 326 | 1 | 327 |
| 35 | spec-author | `skills/spec-author/SKILL.md:207-209` | 4. **Hand off to `product-prover` on the whole spec — the delta included.** The prover catches a | 304 | 0 | 304 |
| 36 | text-audit | `skills/text-audit/SKILL.md:170-172` | 4. **Write each fix from the source.** For a blocking finding, take the fix from the material the... | 270 | 0 | 270 |
| 37 | spec-author | `skills/spec-author/SKILL.md:203-205` | 2. **Ask, don't silently fill.** When the spec needs a decision only the author can make (a thres... | 250 | 0 | 250 |
| 38 | spec-author | `skills/spec-author/SKILL.md:94-97` | 5. **The two closing sentences** — non-goals + one success measure (SPEC INV-20, INV-21). | 218 | 31 | 249 |
| 39 | spec-author | `skills/spec-author/references/the-spine.md:10-11` | 2. **Entities** — the nouns. Each defined in the **glossary**, with its attributes, its unit/vali... | 208 | 0 | 208 |
| 40 | test-author | `skills/test-author/SKILL.md:41-42` | 1. **Open with the artifact inventory** — every file the user receives, each owning at least one | 197 | 0 | 197 |
| 41 | test-author | `skills/test-author/SKILL.md:45-46` | 3. **Every row states BOTH sides** — what the fact does, and what it must never do. The never sid... | 186 | 0 | 186 |
| 42 | spec-author | `skills/spec-author/references/the-spine.md:12-13` | 3. **States & transitions** — every move an entity can make, told as criteria (which action, whic... | 183 | 0 | 183 |
| 43 | design-reviewer | `skills/design-reviewer/SKILL.md:145-147` | 3. **Propose groups.** Elements whose role sentences match are a candidate same-kind group. The | 180 | 0 | 180 |
| 44 | test-author | `skills/test-author/SKILL.md:43-44` | 2. **Blocks per architecture node; every spec fact ≥ 1 row.** A fact with no row is a derivation | 170 | 0 | 170 |
| 45 | spec-author | `skills/spec-author/references/the-spine.md:14-15` | 4. **Actors** — who initiates each significant action (user, role, automated service, external sy... | 168 | 0 | 168 |
| 46 | spec-author | `skills/spec-author/SKILL.md:92-92` | 3. **The standard-facet sweep** — every facet a spec sentence, decided or `[default]`-tagged (SPE... | 116 | 15 | 131 |
| 47 | spec-author | `skills/spec-author/SKILL.md:90-90` | 1. **Regression fences** — when the wish touches a live surface (next section; SPEC T-14, INV-19); | 101 | 6 | 107 |
| 48 | spec-author | `skills/spec-author/SKILL.md:91-91` | 2. **The new behaviour itself** — entities, states, transitions, composed across the canonical axes; | 103 | 0 | 103 |
| 49 | test-author | `skills/test-author/SKILL.md:47-47` | 4. **Every row pins a LEVEL** — the ladder below. The level is the row's most important judgment. | 100 | 0 | 100 |
| 50 | spec-author | `skills/spec-author/SKILL.md:93-93` | 4. **The fit walk** — how the feature sits in the person's path, kind-scaled (SPEC INV-29); | 94 | 4 | 98 |
| 51 | spec-author | `skills/spec-author/references/the-spine.md:20-20` | 6. **Cross-section composition** — the part most specs miss. See the dedicated step below. | 93 | 0 | 93 |
| 52 | spec-author | `skills/spec-author/references/the-spine.md:9-9` | 1. **Purpose** — why the product exists, in plain words: the opening preamble. | 81 | 0 | 81 |
| 53 | spec-author | `skills/spec-author/SKILL.md:206-206` | 3. **Run the completeness pass** (below) on the section just written. | 70 | 0 | 70 |

## Every rule, in full, in the same order

### 1. build-pipeline — The steps, item 8

Home: `skills/build-pipeline/SKILL.md:404-470`.

Opening line, quoted in full: "8. **Verify by deed.** Run it and see the result with your own eyes. Only call it done/working after that;"

Body bytes: 5,954, counted over `skills/build-pipeline/SKILL.md` lines 404-470 with `len(text.encode('utf-8'))`.

Pinned tests: 32, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-23, INV-45, INV-46, INV-61, INV-155, INV-237, INV-298, INV-299), files unioned across codes.

Price: 5,954 body bytes plus 32 pinned tests = 5,986.

### 2. build-pipeline — The steps, item 3

Home: `skills/build-pipeline/SKILL.md:286-352`.

Opening line, quoted in full: "3. **Architecture — write or update `ARCHITECTURE.md` from the proven spec** (template:"

Body bytes: 5,705, counted over `skills/build-pipeline/SKILL.md` lines 286-352 with `len(text.encode('utf-8'))`.

Pinned tests: 20, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-36, INV-37, INV-41, INV-74, INV-75, INV-113, INV-122), files unioned across codes.

Price: 5,705 body bytes plus 20 pinned tests = 5,725.

### 3. build-pipeline — The steps, item 9

Home: `skills/build-pipeline/SKILL.md:471-500`.

Opening line, quoted in full: "9. **Commit & show.** Commit when green with no regression (unasked) — same or better is enough, never wait for perfect. Where the host has a remote, PUSH accepted work there by rule (SPEC INV-82): every gate the diff reaches ran and passed (the verdict read from the suite log's own line), plus the host's own push lines; the remote is discovered from the tree, and only a host with no remote gets one contextual question at the first push moment (create one — GitHub, GitLab, whatever the human names — or stay local, recorded in the host profile). Every push re-walks the README against the pushed truth — crisp and current, a stale claim fixed before the push (the shopfront law at every-push cadence). After the push the push step reads the remote gate's own verdict (the CI run the push triggered, one `gh run` read), and a red verdict is the pushing session's own immediate bug: fixed and re-pushed the same session before anything else, so the human never meets the red first in a GitHub email; a slow gate is watched to its verdict on the detached-work cadence (SPEC INV-106, INV-35). The human's personally named gates still wait for his word. Bump the version, PATCH by default; the number reports what taking the release costs a host, and the tier is read off that cost — a patch fixes a machine to hold a law already stated (the host does nothing), a minor grows what a host may adopt by re-running its catch-up walk with nothing rewritten, a major forces a host action and ships its dated MIGRATION.md chapter (base rule 32 / SPEC INV-217). The minor-versus-major call is a stated judgment the releasing session makes and names, held by no gate."

Body bytes: 4,028, counted over `skills/build-pipeline/SKILL.md` lines 471-500 with `len(text.encode('utf-8'))`.

Pinned tests: 14, from `grep -rlF '<code>' tests/` over each of this rule's own codes (E-18, INV-31, INV-35, INV-44, INV-70, INV-82, INV-106, INV-207, INV-217), files unioned across codes.

Price: 4,028 body bytes plus 14 pinned tests = 4,042.

### 4. spec-author — The spine — what every spec must contain (not its section order), item 7

Home: `skills/spec-author/references/the-spine.md:21-50`.

Opening line, quoted in full: "7. **Terms** — every domain term is defined in the glossary, once, under one name. A word of ordinary"

Body bytes: 2,286, counted over `skills/spec-author/references/the-spine.md` lines 21-50 with `len(text.encode('utf-8'))`.

Pinned tests: 25, from `grep -rlF '<code>' tests/` over each of this rule's own codes (E-17, INV-16, INV-43), files unioned across codes.

Price: 2,286 body bytes plus 25 pinned tests = 2,311.

### 5. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 6

Home: `skills/communicator/SKILL.md:459-479`.

Opening line, quoted in full: "6. **Account for every removal of substance (SPEC INV-109).** When the movement being reported rewrote or restyled existing text, the removal accounting runs before the report closes. A rewrite or restyle that removes substance — a section, an argument, a rationale, a worked example — lists every removal in the delivery report, one line of judgment each: the fact was kept and where, the owner killed it by name, or the rewriter proposes dropping and asks. A removal the rewriter cannot justify becomes a question before the report closes. Never cut substance silently. The rule scopes to substance and leaves line-level wording free, so a tightened sentence or a reordered clause needs no accounting."

Body bytes: 2,292, counted over `skills/communicator/SKILL.md` lines 459-479 with `len(text.encode('utf-8'))`.

Pinned tests: 7, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-31, INV-81, INV-109), files unioned across codes.

Price: 2,292 body bytes plus 7 pinned tests = 2,299.

### 6. build-pipeline — The steps, item 2

Home: `skills/build-pipeline/SKILL.md:263-285`.

Opening line, quoted in full: "2. **Prove — invoke `product-prover`.** The prover only catches a cross-section hole when both sides are"

Body bytes: 2,230, counted over `skills/build-pipeline/SKILL.md` lines 263-285 with `len(text.encode('utf-8'))`.

Pinned tests: 7, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-141, INV-142, INV-154), files unioned across codes.

Price: 2,230 body bytes plus 7 pinned tests = 2,237.

### 7. build-pipeline — The steps, item 1

Home: `skills/build-pipeline/SKILL.md:243-262`.

Opening line, quoted in full: "1. **Spec — invoke `spec-author`.** Write or grow the project `PRODUCT_SPEC.md`: entities, states, transitions,"

Body bytes: 1,625, counted over `skills/build-pipeline/SKILL.md` lines 243-262 with `len(text.encode('utf-8'))`.

Pinned tests: 49, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-18, INV-19, INV-20, INV-21, INV-29, INV-31, T-13, T-14), files unioned across codes.

Price: 1,625 body bytes plus 49 pinned tests = 1,674.

### 8. build-pipeline — The steps, item 5

Home: `skills/build-pipeline/SKILL.md:364-380`.

Opening line, quoted in full: "5. **Test spec — invoke `test-author` to DERIVE `TEST_MATRIX.md` from the proven spec through the proven architecture (the method's one home, SPEC E-27).** The"

Body bytes: 1,466, counted over `skills/build-pipeline/SKILL.md` lines 364-380 with `len(text.encode('utf-8'))`.

Pinned tests: 10, from `grep -rlF '<code>' tests/` over each of this rule's own codes (E-27, INV-6), files unioned across codes.

Price: 1,466 body bytes plus 10 pinned tests = 1,476.

### 9. text-audit — The loop, item 5

Home: `skills/text-audit/SKILL.md:173-193`.

Opening line, quoted in full: "5. **Read again, and close on two clean rounds.** After the fixes land, hand the text to a fresh pair"

Body bytes: 1,473, counted over `skills/text-audit/SKILL.md` lines 173-193 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Read again, and close on two clean rounds' tests/`.

Price: 1,473 body bytes plus 0 pinned tests = 1,473.

### 10. build-pipeline — The steps, item 7

Home: `skills/build-pipeline/SKILL.md:385-403`.

Opening line, quoted in full: "7. **Code — implement until green.** Delegate well-scoped, mechanical implementation to a junior worker"

Body bytes: 1,452, counted over `skills/build-pipeline/SKILL.md` lines 385-403 with `len(text.encode('utf-8'))`.

Pinned tests: 2, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-43, INV-62, INV-63), files unioned across codes.

Price: 1,452 body bytes plus 2 pinned tests = 1,454.

### 11. text-audit — The loop, item 3

Home: `skills/text-audit/SKILL.md:152-169`.

Opening line, quoted in full: "3. **The auditor merges the two lists.** The auditor is the session running this skill, and the merge"

Body bytes: 1,179, counted over `skills/text-audit/SKILL.md` lines 152-169 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'The auditor merges the two lists' tests/`.

Price: 1,179 body bytes plus 0 pinned tests = 1,179.

### 12. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 4

Home: `skills/communicator/SKILL.md:449-457`.

Opening line, quoted in full: "4. **Run the register lint — a hard BLOCK (SPEC INV-83).** Feed every human-facing"

Body bytes: 1,039, counted over `skills/communicator/SKILL.md` lines 449-457 with `len(text.encode('utf-8'))`.

Pinned tests: 9, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-83), files unioned across codes.

Price: 1,039 body bytes plus 9 pinned tests = 1,048.

### 13. spec-author — How spec-author works, item 1

Home: `skills/spec-author/SKILL.md:193-202`.

Opening line, quoted in full: "1. **Author / grow the relevant requirement** in `PRODUCT_SPEC.md`: find (or open) the requirement the"

Body bytes: 1,044, counted over `skills/spec-author/SKILL.md` lines 193-202 with `len(text.encode('utf-8'))`.

Pinned tests: 3, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-37), files unioned across codes.

Price: 1,044 body bytes plus 3 pinned tests = 1,047.

### 14. build-pipeline — The steps, item 4

Home: `skills/build-pipeline/SKILL.md:353-363`.

Opening line, quoted in full: "4. **Prove the architecture — invoke `product-prover` with the architecture lens** whenever the doc"

Body bytes: 1,003, counted over `skills/build-pipeline/SKILL.md` lines 353-363 with `len(text.encode('utf-8'))`.

Pinned tests: 27, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-41, INV-74, INV-75, INV-116, INV-279, M-1, M-6), files unioned across codes.

Price: 1,003 body bytes plus 27 pinned tests = 1,030.

### 15. test-author — Deriving the matrix (the pipeline's step 5), item 8

Home: `skills/test-author/SKILL.md:64-74`.

Opening line, quoted in full: "8. **Close by the mechanical gates, not a hand-walked list.** The coverage checklist the matrix once"

Body bytes: 941, counted over `skills/test-author/SKILL.md` lines 64-74 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Close by the mechanical gates, not a hand-walked list' tests/`.

Price: 941 body bytes plus 0 pinned tests = 941.

### 16. design-reviewer — The standing motion-parity lens (SPEC INV-165), item 3

Home: `skills/design-reviewer/SKILL.md:204-215`.

Opening line, quoted in full: "3. **Every position behaves alike.** The same gesture on the same type in a different slot behaves the"

Body bytes: 859, counted over `skills/design-reviewer/SKILL.md` lines 204-215 with `len(text.encode('utf-8'))`.

Pinned tests: 7, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-125), files unioned across codes.

Price: 859 body bytes plus 7 pinned tests = 866.

### 17. design-reviewer — The similarity lens — five steps, item 1

Home: `skills/design-reviewer/SKILL.md:131-139`.

Opening line, quoted in full: "1. **Enumerate.** Build your own inventory of the elements. Use the prover's Phase 1 extraction habit"

Body bytes: 751, counted over `skills/design-reviewer/SKILL.md` lines 131-139 with `len(text.encode('utf-8'))`.

Pinned tests: 9, from `grep -rlF '<code>' tests/` over each of this rule's own codes (E-10, INV-97), files unioned across codes.

Price: 751 body bytes plus 9 pinned tests = 760.

### 18. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 5

Home: `skills/communicator/SKILL.md:458-458`.

Opening line, quoted in full: "5. **Legibility floor (a BLOCK, SPEC INV-139).** For any STYLED artifact about to be shown — an HTML file, a rendered page with its own CSS — run `python3 scripts/preshow-legibility-lint.py FILE`. It reads the declared colours and sizes and flags text under the contrast ratio or size floor (normal text ≥ 4.5:1, large ≥ 3:1, body/caption ≥ 12px). The script counts text as large at a font size of 24px or more, and at 18.66px or more when bold. A red result BLOCKS the showing until the text is lifted to the floor. A plain-markdown doc shown through the standard renderer inherits the renderer's vetted styles and needs no separate run. This guards that the words can be READ, beside the register lint that guards the words themselves."

Body bytes: 748, counted over `skills/communicator/SKILL.md` lines 458-458 with `len(text.encode('utf-8'))`.

Pinned tests: 4, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-139), files unioned across codes.

Price: 748 body bytes plus 4 pinned tests = 752.

### 19. test-author — Deriving the matrix (the pipeline's step 5), item 7

Home: `skills/test-author/SKILL.md:56-63`.

Opening line, quoted in full: "7. **A norm-pointered clause owes a norm-conformance row.** When a spec clause carries a"

Body bytes: 711, counted over `skills/test-author/SKILL.md` lines 56-63 with `len(text.encode('utf-8'))`.

Pinned tests: 2, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-43), files unioned across codes.

Price: 711 body bytes plus 2 pinned tests = 713.

### 20. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 3

Home: `skills/communicator/SKILL.md:444-448`.

Opening line, quoted in full: "3. **Run the mechanical check** — feed the drafted prose to `python3 scripts/preshow-lint.py -` and clear"

Body bytes: 620, counted over `skills/communicator/SKILL.md` lines 444-448 with `len(text.encode('utf-8'))`.

Pinned tests: 24, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-28), files unioned across codes.

Price: 620 body bytes plus 24 pinned tests = 644.

### 21. text-audit — The loop, item 2

Home: `skills/text-audit/SKILL.md:145-151`.

Opening line, quoted in full: "2. **Hand the text to two fresh cold readers.** Both sessions hold zero context on the text's history."

Body bytes: 549, counted over `skills/text-audit/SKILL.md` lines 145-151 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Hand the text to two fresh cold readers' tests/`.

Price: 549 body bytes plus 0 pinned tests = 549.

### 22. design-reviewer — The similarity lens — five steps, item 4

Home: `skills/design-reviewer/SKILL.md:148-154`.

Opening line, quoted in full: "4. **Check parity.** For each candidate group, list the declared interactions of each member from the"

Body bytes: 537, counted over `skills/design-reviewer/SKILL.md` lines 148-154 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Check parity' tests/`.

Price: 537 body bytes plus 0 pinned tests = 537.

### 23. design-reviewer — The similarity lens — five steps, item 5

Home: `skills/design-reviewer/SKILL.md:155-162`.

Opening line, quoted in full: "5. **Fire the tight ask.** A divergence becomes a finding only when the signal is strong. Every"

Body bytes: 517, counted over `skills/design-reviewer/SKILL.md` lines 155-162 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Fire the tight ask' tests/`.

Price: 517 body bytes plus 0 pinned tests = 517.

### 24. design-reviewer — The standing motion-parity lens (SPEC INV-165), item 2

Home: `skills/design-reviewer/SKILL.md:199-203`.

Opening line, quoted in full: "2. **Every object type behaves alike.** Each kind of thing the gesture acts on — a gallery frame, a"

Body bytes: 425, counted over `skills/design-reviewer/SKILL.md` lines 199-203 with `len(text.encode('utf-8'))`.

Pinned tests: 1. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Every object type behaves alike' tests/`.

Price: 425 body bytes plus 1 pinned tests = 426.

### 25. design-reviewer — The standing motion-parity lens (SPEC INV-165), item 1

Home: `skills/design-reviewer/SKILL.md:195-198`.

Opening line, quoted in full: "1. **Entry mirrors exit.** A layer that opens by a motion from its source closes by the reverse of"

Body bytes: 398, counted over `skills/design-reviewer/SKILL.md` lines 195-198 with `len(text.encode('utf-8'))`.

Pinned tests: 1. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Entry mirrors exit' tests/`.

Price: 398 body bytes plus 1 pinned tests = 399.

### 26. test-author — Deriving the matrix (the pipeline's step 5), item 6

Home: `skills/test-author/SKILL.md:52-55`.

Opening line, quoted in full: "6. **Matrix-local row ids are legal, spec anchors stay the parent.** One spec fact may project into"

Body bytes: 387, counted over `skills/test-author/SKILL.md` lines 52-55 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Matrix-local row ids are legal, spec anchors stay the parent' tests/`.

Price: 387 body bytes plus 0 pinned tests = 387.

### 27. test-author — Deriving the matrix (the pipeline's step 5), item 5

Home: `skills/test-author/SKILL.md:48-51`.

Opening line, quoted in full: "5. **Name the state space before filling cells.** Axes first: view states (mode, toggles), data"

Body bytes: 374, counted over `skills/test-author/SKILL.md` lines 48-51 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Name the state space before filling cells' tests/`.

Price: 374 body bytes plus 0 pinned tests = 374.

### 28. spec-author — The spine — what every spec must contain (not its section order), item 5

Home: `skills/spec-author/references/the-spine.md:16-19`.

Opening line, quoted in full: "5. **Invariants** — the properties that must hold across *every* reachable state, stated as criteria that"

Body bytes: 373, counted over `skills/spec-author/references/the-spine.md` lines 16-19 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Invariants' tests/`.

Price: 373 body bytes plus 0 pinned tests = 373.

### 29. text-audit — The loop, item 1

Home: `skills/text-audit/SKILL.md:141-144`.

Opening line, quoted in full: "1. **Run the mechanical lints, and fix every hit.** Run every check that a script or a grep can decide,"

Body bytes: 361, counted over `skills/text-audit/SKILL.md` lines 141-144 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Run the mechanical lints, and fix every hit' tests/`.

Price: 361 body bytes plus 0 pinned tests = 361.

### 30. build-pipeline — The steps, item 6

Home: `skills/build-pipeline/SKILL.md:381-384`.

Opening line, quoted in full: "6. **Test — with `test-author`, write tests that assert the REAL shipped artifact.** Render the widget / produce the file /"

Body bytes: 355, counted over `skills/build-pipeline/SKILL.md` lines 381-384 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Test — with `test-author`, write tests that assert the REAL shipped artifact' tests/`.

Price: 355 body bytes plus 0 pinned tests = 355.

### 31. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 2

Home: `skills/communicator/SKILL.md:440-443`.

Opening line, quoted in full: "2. **Pass the draft phrase by phrase through one question:** *does this sentence stand for a reader who"

Body bytes: 344, counted over `skills/communicator/SKILL.md` lines 440-443 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Pass the draft phrase by phrase through one question:' tests/`.

Price: 344 body bytes plus 0 pinned tests = 344.

### 32. communicator — The pre-report walk — run before any movement-end or milestone report, and before any surface is shown (SPEC INV-34, INV-83), item 1

Home: `skills/communicator/SKILL.md:437-439`.

Opening line, quoted in full: "1. **Re-read the rules above, and the full writing register** — open this file and read the live text each"

Body bytes: 340, counted over `skills/communicator/SKILL.md` lines 437-439 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Re-read the rules above, and the full writing register' tests/`.

Price: 340 body bytes plus 0 pinned tests = 340.

### 33. spec-author — How spec-author works, item 5

Home: `skills/spec-author/SKILL.md:210-214`.

Opening line, quoted in full: "5. **Then walk the two layers to the tests** — the architecture doc (nodes owning the spec's facts,"

Body bytes: 337, counted over `skills/spec-author/SKILL.md` lines 210-214 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Then walk the two layers to the tests' tests/`.

Price: 337 body bytes plus 0 pinned tests = 337.

### 34. design-reviewer — The similarity lens — five steps, item 2

Home: `skills/design-reviewer/SKILL.md:140-144`.

Opening line, quoted in full: "2. **Describe by role.** For each element, write its role sentence: "a photo a viewer opens large to"

Body bytes: 326, counted over `skills/design-reviewer/SKILL.md` lines 140-144 with `len(text.encode('utf-8'))`.

Pinned tests: 1. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Describe by role' tests/`.

Price: 326 body bytes plus 1 pinned tests = 327.

### 35. spec-author — How spec-author works, item 4

Home: `skills/spec-author/SKILL.md:207-209`.

Opening line, quoted in full: "4. **Hand off to `product-prover` on the whole spec — the delta included.** The prover catches a"

Body bytes: 304, counted over `skills/spec-author/SKILL.md` lines 207-209 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Hand off to `product-prover` on the whole spec — the delta included' tests/`.

Price: 304 body bytes plus 0 pinned tests = 304.

### 36. text-audit — The loop, item 4

Home: `skills/text-audit/SKILL.md:170-172`.

Opening line, quoted in full: "4. **Write each fix from the source.** For a blocking finding, take the fix from the material the text"

Body bytes: 270, counted over `skills/text-audit/SKILL.md` lines 170-172 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Write each fix from the source' tests/`.

Price: 270 body bytes plus 0 pinned tests = 270.

### 37. spec-author — How spec-author works, item 2

Home: `skills/spec-author/SKILL.md:203-205`.

Opening line, quoted in full: "2. **Ask, don't silently fill.** When the spec needs a decision only the author can make (a threshold, a"

Body bytes: 250, counted over `skills/spec-author/SKILL.md` lines 203-205 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Ask, don't silently fill' tests/`.

Price: 250 body bytes plus 0 pinned tests = 250.

### 38. spec-author — The feature delta, assembled — one home for its mandatory parts, item 5

Home: `skills/spec-author/SKILL.md:94-97`.

Opening line, quoted in full: "5. **The two closing sentences** — non-goals + one success measure (SPEC INV-20, INV-21)."

Body bytes: 218, counted over `skills/spec-author/SKILL.md` lines 94-97 with `len(text.encode('utf-8'))`.

Pinned tests: 31, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-20, INV-21), files unioned across codes.

Price: 218 body bytes plus 31 pinned tests = 249.

### 39. spec-author — The spine — what every spec must contain (not its section order), item 2

Home: `skills/spec-author/references/the-spine.md:10-11`.

Opening line, quoted in full: "2. **Entities** — the nouns. Each defined in the **glossary**, with its attributes, its unit/valid range if"

Body bytes: 208, counted over `skills/spec-author/references/the-spine.md` lines 10-11 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Entities' tests/`.

Price: 208 body bytes plus 0 pinned tests = 208.

### 40. test-author — Deriving the matrix (the pipeline's step 5), item 1

Home: `skills/test-author/SKILL.md:41-42`.

Opening line, quoted in full: "1. **Open with the artifact inventory** — every file the user receives, each owning at least one"

Body bytes: 197, counted over `skills/test-author/SKILL.md` lines 41-42 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Open with the artifact inventory' tests/`.

Price: 197 body bytes plus 0 pinned tests = 197.

### 41. test-author — Deriving the matrix (the pipeline's step 5), item 3

Home: `skills/test-author/SKILL.md:45-46`.

Opening line, quoted in full: "3. **Every row states BOTH sides** — what the fact does, and what it must never do. The never side is"

Body bytes: 186, counted over `skills/test-author/SKILL.md` lines 45-46 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Every row states BOTH sides' tests/`.

Price: 186 body bytes plus 0 pinned tests = 186.

### 42. spec-author — The spine — what every spec must contain (not its section order), item 3

Home: `skills/spec-author/references/the-spine.md:12-13`.

Opening line, quoted in full: "3. **States & transitions** — every move an entity can make, told as criteria (which action, which actor,"

Body bytes: 183, counted over `skills/spec-author/references/the-spine.md` lines 12-13 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'States & transitions' tests/`.

Price: 183 body bytes plus 0 pinned tests = 183.

### 43. design-reviewer — The similarity lens — five steps, item 3

Home: `skills/design-reviewer/SKILL.md:145-147`.

Opening line, quoted in full: "3. **Propose groups.** Elements whose role sentences match are a candidate same-kind group. The"

Body bytes: 180, counted over `skills/design-reviewer/SKILL.md` lines 145-147 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Propose groups' tests/`.

Price: 180 body bytes plus 0 pinned tests = 180.

### 44. test-author — Deriving the matrix (the pipeline's step 5), item 2

Home: `skills/test-author/SKILL.md:43-44`.

Opening line, quoted in full: "2. **Blocks per architecture node; every spec fact ≥ 1 row.** A fact with no row is a derivation"

Body bytes: 170, counted over `skills/test-author/SKILL.md` lines 43-44 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Blocks per architecture node; every spec fact ≥ 1 row' tests/`.

Price: 170 body bytes plus 0 pinned tests = 170.

### 45. spec-author — The spine — what every spec must contain (not its section order), item 4

Home: `skills/spec-author/references/the-spine.md:14-15`.

Opening line, quoted in full: "4. **Actors** — who initiates each significant action (user, role, automated service, external system)."

Body bytes: 168, counted over `skills/spec-author/references/the-spine.md` lines 14-15 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Actors' tests/`.

Price: 168 body bytes plus 0 pinned tests = 168.

### 46. spec-author — The feature delta, assembled — one home for its mandatory parts, item 3

Home: `skills/spec-author/SKILL.md:92-92`.

Opening line, quoted in full: "3. **The standard-facet sweep** — every facet a spec sentence, decided or `[default]`-tagged (SPEC T-13, INV-18);"

Body bytes: 116, counted over `skills/spec-author/SKILL.md` lines 92-92 with `len(text.encode('utf-8'))`.

Pinned tests: 15, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-18, T-13), files unioned across codes.

Price: 116 body bytes plus 15 pinned tests = 131.

### 47. spec-author — The feature delta, assembled — one home for its mandatory parts, item 1

Home: `skills/spec-author/SKILL.md:90-90`.

Opening line, quoted in full: "1. **Regression fences** — when the wish touches a live surface (next section; SPEC T-14, INV-19);"

Body bytes: 101, counted over `skills/spec-author/SKILL.md` lines 90-90 with `len(text.encode('utf-8'))`.

Pinned tests: 6, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-19, T-14), files unioned across codes.

Price: 101 body bytes plus 6 pinned tests = 107.

### 48. spec-author — The feature delta, assembled — one home for its mandatory parts, item 2

Home: `skills/spec-author/SKILL.md:91-91`.

Opening line, quoted in full: "2. **The new behaviour itself** — entities, states, transitions, composed across the canonical axes;"

Body bytes: 103, counted over `skills/spec-author/SKILL.md` lines 91-91 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'The new behaviour itself' tests/`.

Price: 103 body bytes plus 0 pinned tests = 103.

### 49. test-author — Deriving the matrix (the pipeline's step 5), item 4

Home: `skills/test-author/SKILL.md:47-47`.

Opening line, quoted in full: "4. **Every row pins a LEVEL** — the ladder below. The level is the row's most important judgment."

Body bytes: 100, counted over `skills/test-author/SKILL.md` lines 47-47 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Every row pins a LEVEL' tests/`.

Price: 100 body bytes plus 0 pinned tests = 100.

### 50. spec-author — The feature delta, assembled — one home for its mandatory parts, item 4

Home: `skills/spec-author/SKILL.md:93-93`.

Opening line, quoted in full: "4. **The fit walk** — how the feature sits in the person's path, kind-scaled (SPEC INV-29);"

Body bytes: 94, counted over `skills/spec-author/SKILL.md` lines 93-93 with `len(text.encode('utf-8'))`.

Pinned tests: 4, from `grep -rlF '<code>' tests/` over each of this rule's own codes (INV-29), files unioned across codes.

Price: 94 body bytes plus 4 pinned tests = 98.

### 51. spec-author — The spine — what every spec must contain (not its section order), item 6

Home: `skills/spec-author/references/the-spine.md:20-20`.

Opening line, quoted in full: "6. **Cross-section composition** — the part most specs miss. See the dedicated step below."

Body bytes: 93, counted over `skills/spec-author/references/the-spine.md` lines 20-20 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Cross-section composition' tests/`.

Price: 93 body bytes plus 0 pinned tests = 93.

### 52. spec-author — The spine — what every spec must contain (not its section order), item 1

Home: `skills/spec-author/references/the-spine.md:9-9`.

Opening line, quoted in full: "1. **Purpose** — why the product exists, in plain words: the opening preamble."

Body bytes: 81, counted over `skills/spec-author/references/the-spine.md` lines 9-9 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Purpose' tests/`.

Price: 81 body bytes plus 0 pinned tests = 81.

### 53. spec-author — How spec-author works, item 3

Home: `skills/spec-author/SKILL.md:206-206`.

Opening line, quoted in full: "3. **Run the completeness pass** (below) on the section just written."

Body bytes: 70, counted over `skills/spec-author/SKILL.md` lines 206-206 with `len(text.encode('utf-8'))`.

Pinned tests: 0. This rule cites no SPEC code in its own text, so the search fell back to its lead-in phrase: `grep -rlF 'Run the completeness pass' tests/`.

Price: 70 body bytes plus 0 pinned tests = 70.

