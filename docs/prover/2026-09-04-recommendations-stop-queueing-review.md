# Prover record — 2026-09-04 recommendations stop queueing, and the target tag with no row

Ran under **product-prover 4.3.0** with **product-prover-pack 6.1.0** bindings, mode FULL, from a
seat that authored none of the changes below.

PUSH-REVIEW

Range: d8d5305..1d4a6b6, 12 commits
- 1d4a6b6 The second queue is gone, and the rules a person reads live where every project inherits them
  (the commit that landed the working tree this review read; its nine defects were folded before it
  was written, and the fold is inside it — F1 through F9 all verified against the tree as committed)
- 2848a1a NEXT_STEPS: session close -- board scope corrected, tangent unpushed pending his review
- d185a26 Fix the six findings from tonight's rule-adoption-batch review
- 5c0b96c Prover record: the rule-adoption batch (d8d5305..fb836474) reviewed
- fb83647 adopt/install-style-gates.sh vendors scripts/preshow-register-lint.py
- d9b6125 PLAN.md: close the roadmap-format naming Blockers finding
- d2d57d2 docs/roadmap-format.md: fix framing to stop naming the retired ROADMAP.md
- 1e95276 Re-record all 45 Director eval traces against tonight's follow-on commit
- 4961131 Enter two playbook-only rules into the pack (SKILL.md rules 22, 37)
- 85ddbda Adopt: a verdict on shown work is a movement end for its artifact
- 12840c5 PLAN.md cleanup + role-profile brief rule adopted; pin drift fixed
- 363d0a8 q-816: widen acceptance to name R310 criterion 10; close the Blockers finding
Files read: spec/design-spec-review.md, spec/doc-order-generated.md, spec/queue-intake-priority.md, spec/owner-questions-drafts.md, spec/project-setup-tuning.md, spec/push-gate-milestone-audit.md, PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, ARCHITECTURE.md parts (authoring-and-review, host-adoption, pipeline-and-lanes, rules-and-settings), matrix/product-prover.md, matrix/design-reviewer.md, matrix/package-docs.md, matrix/guardrails.md, skills/live-spec-base/SKILL.md, skills/live-spec-base/references/rule-origins.md, skills/director/SKILL.md, skills/director/references/landing-law.md, skills/design-reviewer/SKILL.md, skills/design-reviewer/README.md, skills/communicator/SKILL.md, scripts/state-probe.sh, scripts/render-board.sh, scripts/plan_checks.py, scripts/plan_checks_core.py, scaffold/status-view/state-probe.sh, tests/test_traceability.py, tests/test_finding_kind.py, tests/test_authority_anchor.py, tests/test_no_row_waits_on_the_person.py, DECISIONS.md, PLAN.md, docs/upstream-notes-2026-09-04.md, docs/queue-archive/2026-09-04-rows-taken-off-the-board.md, attic/MANIFEST.md, evals/director/closing-scenarios.json, evals/director/README.md
Checks run: `python3 -m pytest -q tests/test_traceability.py tests/test_finding_kind.py tests/test_no_row_waits_on_the_person.py tests/test_landing_next_steps.py tests/test_board_matches_the_canon.py tests/test_plan_done_marks_are_backed.py tests/test_authority_anchor.py tests/test_tasks_parser_finds_every_task.py tests/test_restructure_merge_gate.py tests/test_minor_gate_reconciliations.py tests/test_plan_step_reader.py tests/test_status_view_install.py tests/test_director_route_end_to_end.py` — 1 failed, 314 passed, 2 skipped (F1 below); `shasum -a 256 skills/director/SKILL.md` — matches the pin in evals/director/closing-scenarios.json; `git ls-files --error-unmatch skills/product-prover/SKILL.md` — untracked, the file F6 rests on. A full `python3 -m pytest -q` was started and had not finished when this record was written; no number from it is claimed here, and F1's red stands on the targeted run above, which reproduces it deterministically
Findings: nine defects and seven recommendations, listed below. Four defects (F1, F2, F3, F4) sit on the two substantive spec changes and on the suite itself; the rest are class-sweep misses of the same two rewrites. Verified clean and named as such: the rule count in all three homes reads twenty-five and matches the body; rule 38's stated group order matches the machine reading in `scripts/state-probe.sh` line for line; the director eval's `skill_sha256` matches the live SKILL.md byte-for-byte; PRODUCT_SPEC.index.md's INV-140, INV-114, INV-156, M-6 and S-0 rows were re-derived against the renumbered R60 criteria and are correct; no dangling reference to the deleted `check-eyes-marker.py` survives in live code.
Blocking: five findings stand — the seat was briefed to write this record and change nothing else
- F1 the suite is red on a renamed test the matrix still cites — stands: the fix is one line in matrix/guardrails.md and belongs to the author, not to this read; the push cannot go green until it lands
- F2 rule-origins.md names this delta's own R1 criterion 5 as the violation rule 39 was written to forbid, and the criterion ships anyway — stands: one of the two documents has to change and only the author can decide which
- F3 R1 criterion 5 contradicts R5 criteria 1, 2 and 3 in spec/queue-intake-priority.md — stands: the repair is a spec decision, and the smaller one needs no new criterion at all
- F4 the new archive tie is unenforceable as built, asserting only that a file exists — stands: it is the mechanization of F3's criterion and moves with it
- F6 tests/test_finding_kind.py now asserts on an untracked hand-patched copy of another repository's file — stands: closing it means landing the sentence upstream first, which is outside this tree

---

## Triage

`TRIAGE: PROCEED`. The delta carries two substantive requirement rewrites, two new rulebook rules,
one rewritten rule, and their ripples across the matrix, the architecture pins, the status scripts
and the suite. It describes a shipped system, and the architecture parts carry `file:line` node
pins, so the findings below are unconditional rather than conditional on currency. Four pins moved
in this delta and were re-checked against their targets; all four are correct as re-pinned.

## Opening assessment

The delta does one clear thing well and one thing in the wrong place. The clear thing is R60: a
recommendation now ends in the review record instead of opening a row, and the rewrite is carried
all the way through — the glossary, the index, the matrix, the design-reviewer skill, the push-gate
clause and the restructure-merge clause all move together, which is the class sweep this pack
usually has to be reminded to run. The thing in the wrong place is R1 criterion 5. A gate went red
because the owner took three rows off the board, and the answer was a second ownership map and a new
spec criterion admitting exactly the case that had just failed. The tree's own `rule-origins.md`
says so in writing, in the same landing, while explaining where rule 39 came from. Beside that, the
suite is red on an unrelated rename the matrix did not follow. Confidence: **needs another
iteration** — the R60 half is ready, the R1 half is not.

## Phase 1 — The model

**Entities.** A *finding* (kind: defect | recommendation | acknowledged). A *review record* under
`docs/prover/`. A *queue row* in `PLAN.md`'s `## Tasks`. A *target tag* on a spec line, anchored to
a requirement code. A *queue-archive record* under `docs/queue-archive/`. A *status mark* on a row.

**States and transitions of a finding.** filed → (defect) blocks → folded → non-blocking; filed →
(recommendation) written into the record → terminal, unless the person copies it onto the plan in
their own words, which is a new row rather than a transition of the finding. The delta's change is
that the recommendation path lost its `→ queue row` edge, and the pre-existing-defect-outside-a-delta
path was re-pointed onto the recommendation path.

**States of a target tag.** Before this delta: one state, *owned by an open row*, with two red
transitions (row lands with tag on; tag vanishes). After: two states, *owned by an open row* and
*owned by an archive record*, and the transition between them is the row leaving the board.

**States of a status mark.** ✅ done, 🔄 in hand, 🔁 reopened, ⬜ queued, ⛔ blocked. 👁️ retired;
`normalize_mark` maps it to ⬜.

**Actors.** The prover files findings. The push gate folds defects. The person, and only the person,
writes a row onto the plan. The suite reads the two ownership maps. The status script prints the
list; nothing but `evaluate()` mints 🔁.

**What I assumed.** I read "the queue archive's dated record of its row leaving the board" as the
existing `docs/queue-archive/` directory that `PRODUCT_SPEC.md`'s glossary defines, not a new
directory sharing its name — the test's paths confirm this. I read the owner's 01:17 word as
recorded in `DECISIONS.md`, and I have not treated my sharpening of it as his. I treated the
`~/.claude/` personal layer as out of this repository's write scope and did not file findings
against it, though F7 and R4 touch its boundary. I read `skills/product-prover/` as untracked and
outside this repo's ownership, per the pack bindings' own version-discipline section.

## Phase 2 — Structural issues

### F1 — The suite is red: the matrix still names a test this delta renamed away

> `test_push_mode_reports_risky_surface_candidates` — matrix/guardrails.md:44, M-388's owning-test list

`tests/test_authority_anchor.py:350` renamed that test to `test_push_mode_reaches_the_risky_surfaces`
in this delta. `matrix/guardrails.md:44` still cites the old name, so
`tests/test_traceability.py::TestMatrix::test_matrix_built_rows_name_real_tests` fails with
"M-388: BUILT row cites missing test ... (no exact def)". Anyone running the suite before pushing
meets a red on a change that has nothing to do with what they were working on, and the push gate
refuses a red suite outright.

Replace the cited name in `matrix/guardrails.md:44` with `test_push_mode_reaches_the_risky_surfaces`.
This is the same landing that did the rename, so the two belong in one commit.

`defect · internal-conflict (consistency)`

### F2 — The rulebook names this delta's own spec criterion as the violation rule 39 forbids, and the criterion ships anyway

> "The night it entered, this tree had just answered a failing check by widening it — a spec criterion added so a promise with no owner could pass a gate that existed to catch exactly that. The rule names that move as the same failure as inventing a threshold" — skills/live-spec-base/references/rule-origins.md:167-170

`spec/doc-order-generated.md:22` is that criterion, and it is in this same working tree. Two
documents shipping together say opposite things about one change: the spec says it is law, the
rulebook's own origin note says it is the failure the new rule exists to name. A reader who
resolves the conflict either way is right on the text and wrong on the other half. Worse, the next
session that meets a red ownership check has written precedent for widening it, and written
precedent for refusing to.

Pick one and land it. Either strike the second and third sentences of the rule-39 origin note and
justify criterion 5 on its own merits, or strike criterion 5 (see F3, whose repair needs no new
criterion). I hold the second: F3 shows the criterion is misplaced independently of rule 39.

`defect · direct-contradiction (contradiction)`

### F3 — Criterion 5 ties a target tag to an archive record the spec forbids from existing

> "*while* no queue row is building a promised part, the system *shall* keep that part's target tag standing and *shall* tie the tag to the queue archive's dated record of its row leaving the board" — spec/doc-order-generated.md:22, Requirement 1 criterion 5

Three clauses already govern what the queue archive holds, and criterion 5 walks past all three.

- `spec/queue-intake-priority.md:11` (R5 criterion 1) admits a row to the archive on one condition:
  a terminal exit, *landed*, *declined*, or *superseded*. "Taken off the board on the owner's word,
  unbuilt" is none of the three.
- `spec/queue-intake-priority.md:12` (R5 criterion 2): "The system *shall* keep in the archive only
  wishes no longer due back." `docs/queue-archive/2026-09-04-rows-taken-off-the-board.md:13` says of
  the very rows it files: "Each returns as a fresh row when someone asks for it."
- `spec/queue-intake-priority.md:16` (R5 criterion 3): a deferred row stays in the queue's body
  carrying its revisit trigger. q-385's record carries its trigger verbatim ("the first host
  declaring a contract in its card") and q-816's carries its own ("package 2 ... closes"). Both are
  deferred rows by the spec's own definition, filed where deferred rows may not go.

`PRODUCT_SPEC.md:194`'s glossary agrees with R5 and not with criterion 5. The operational cost:
someone reading `spec/public-contract.md` R194 criterion 15 follows its `[target]` to a record
saying the row is gone, then follows the archive's own law to conclude a row in that file is never
coming back, and drops a promise the owner explicitly kept.

The repair the ladder reaches first needs no new criterion at all. Put q-385 and q-816 back in
`## Tasks` as deferred rows carrying the triggers they already have — criterion 3 then covers their
tags unchanged, and TARGET_ARCHIVE_OWNERS drops to one entry or none. q-54 is the only genuinely
rowless case, and its promise (E-18, the design-sync machine) has a cheaper answer than a spec
criterion: drop the `[target]` line, since the owner's word was «онбординг вычисти». If instead the
owner's 01:17 word is read as retiring the deferred tier itself, then the spec change this delta
owes is to R5's exit vocabulary and archive-contents rule — and R1 still needs no criterion 5.

`defect · direct-contradiction (contradiction)`

### F4 — The archive tie is unenforceable as built: the check asserts only that a file exists

> `self.assertTrue(os.path.exists(os.path.join(ROOT, record)), ...)` — tests/test_traceability.py, TestTargetOwnership

Criterion 5 promises the tag is *tied to the dated record of its row leaving the board*. The check
holds only that a file sits at the named path. A record that never mentions E-18, never mentions
q-54, and says nothing about a row leaving anything satisfies it, as does the file's continued
existence long after its content is rewritten. Criterion 3's tie is real by comparison: it reads the
row's live mark out of `PLAN.md` and reds when the row lands or vanishes. The new tie reds on
nothing a person would ever do by accident.

Assert the record's text names the row the map's comment already names — `q-54`, `q-385`, `q-816` —
so the tie holds a fact rather than a filename. That is one `assertIn` per entry and it is what
makes the map self-closing in the direction it claims.

`defect · unenforceable-promise (discharge)`

## Phase 3 — Property analysis

### F5 — Two files were deleted outright where this pack's own rule 10 requires the attic and a manifest line

> "Nothing is silently deleted. Move a superseded file to the attic with a manifest line" — skills/live-spec-base/SKILL.md:183, rule 10 (SPEC INV-7, A-4, A-9)

`scripts/check-eyes-marker.py` and `tests/test_eyes_marker_traces_to_owner.py` are deleted in the
working tree with no `attic/` copy and no line in `attic/MANIFEST.md`. The precedent for exactly
this class is in that manifest: `attic/MANIFEST.md:8` for a retired guardrail script and
`attic/MANIFEST.md:47` for a retired gate. A session six months from now asking why the 👁️
provenance check existed and what it caught has the retirement reason in a code comment and the
code itself nowhere.

Move both to `attic/` and add their two manifest lines, naming the 2026-09-04 mark retirement as the
reason. Rule 39's "deletion is the preferred repair" governs *whether* to remove; rule 10 governs
*how*, and it is unchanged by this delta.

`defect · hard-to-operate (ops-ux)`

### F6 — A suite assertion now rests on an untracked, hand-patched copy of another repository's file

> "The next upstream update to product-prover will overwrite `~/.claude/skills/product-prover/SKILL.md`, so this wording belongs in the upstream skill source, not only here." — docs/upstream-notes-2026-09-04.md

`tests/test_finding_kind.py` was changed in this delta to assert `"written into the review record and
ends there"` in `skills/product-prover/SKILL.md`. That file is untracked here — the pack bindings say
so themselves, under "Version discipline": "The installed copy under `skills/product-prover/` is not
tracked by this repository; the external repository is its only source of truth." It is green today
because this session hand-edited it. The next run of `scripts/install-external-skills.sh` reverts the
sentence and reds the suite, on a machine and at a moment nobody chose, with the failure pointing at
a file `git` will report as unchanged. The note names the hazard and nothing holds it.

Land the sentence in the external product-prover repository, raise the minimum in
`skills/product-prover-pack/SKILL.md`'s metadata to the release carrying it, and keep the assertion.
Until that lands, drop the canon assertion and keep only the tracked-side ones — a green that
depends on a local edit to somebody else's file is worse than an absent check.

`defect · unenforceable-promise (discharge)`

### F7 — The status script reverses a dated owner decision, and its own comment six lines above still states the old one

> "then reopened (was done and is done no longer — outranked by work already running, but ahead of a real outside blocker and of work never started, added 02.09 on his word)" — scripts/state-probe.sh:132-134
>
> `CATEGORY_ORDER = ["✅", "🔄", "⛔", "🔁", "⬜"]` — scripts/state-probe.sh:148

The comment says reopened outranks blocked, and cites the owner's word of 2026-09-02 for it. The
line below puts blocked ahead of reopened. `skills/live-spec-base/SKILL.md:329` (rule 38) states the
new order and gives it a fresh reason — "only a person can unstick it" — with no dated word behind
it, while `DECISIONS.md`'s 2026-09-04 entries record four rulings and none of them is this one. A row
that came back because its check stopped passing now sits below a blocked row on the list the person
reads first, and the file's own comment tells the next reader that is a bug.

Either restore `🔁` ahead of `⛔` and drop the clause from rule 38, or keep the new order, strike the
stale half of the comment at line 133, and record the reversal in `DECISIONS.md` as the pack's own
judgment rather than as his. I hold the first: a dated word is on record for the old order and none
is on record for the new one.

`defect · internal-conflict (consistency)`

### F8 — The design-reviewer's own README still tells the reader a recommendation queues

> "a recommendation that queues for a taste call" — skills/design-reviewer/README.md:35

The class sweep behind R60's rewrite reached `skills/design-reviewer/SKILL.md` in four places,
`matrix/design-reviewer.md`, `matrix/product-prover.md`, `matrix/package-docs.md`, `PRODUCT_SPEC.md`'s
glossary, the index and three spec parts. It missed this file, which is tracked and is the page a
person reads to learn what the design review does to their board. It now states the retired law.

Rewrite the clause to match `skills/design-reviewer/SKILL.md`: a confident finding is written into
the review record and ends there.

`defect · internal-conflict (consistency)`

### F9 — A case heading in the spec states the law its own criterion just stopped stating

> "**Case: confident queues, likely asks**" — spec/owner-questions-drafts.md:162, Requirement 69

Criterion 1 beneath it was changed in this delta to "a recommendation that is recorded and never
blocks". The heading was not. A spec section labelled by the behaviour it no longer has is the same
defect class as F8, one level up: the heading is what a reader scanning the requirement list sees
first, and it now says "queues".

Retitle to `**Case: confident is recorded, likely asks**`.

`defect · internal-conflict (consistency)`

## Phase 3e — Mandatory sweeps

This delta's documents place no user-facing surface, so the surface × sweep table collapses to a
single row, as Phase 3e provides for.

| Surface | Declared cross-cutting laws | Edge-condition completeness | Cross-surface policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| the rulebook + spec parts (no user-facing surface) | clean — rules 38 and 39 each name their enforcement, rule 38 the status script's `CATEGORY_ORDER` and rule 39 prose-only with its reason stated; rule 36's own named check `guardrails/check-language-rules.py` survives the rewrite | hit — F3 (the state "no row is building it" is admitted with no answer for how it ends, see R6 below) | hit — R1 (the no-row-without-the-person's-word policy stops at the prover and the director, and `spec/internal-failure-log.md:36` still opens rows on its own) | clean — the finding lifecycle's new terminal state (recorded, ends there) states its one exit, the person copying it onto the plan in their own words | hit — F4 (the tie between a tag and an archive record has a blank answer for what the record must contain) |

`Class lens: swept — two classes filed. (1) The R60 rewrite's stale-wording class: swept across spec/, skills/, matrix/, PRODUCT_SPEC.md and the index; two live instances remain, F8 and F9, and one lives in an untracked file (skills/product-prover/PROVENANCE.md:50) outside this repo's ownership. (2) The gate-anchored-on-existence class: swept across the delta's test changes; F4 is the filed instance and R2 is its near neighbour, a behavioural assertion replaced by a source-text literal in tests/test_authority_anchor.py.`

## Recommendations — written here, opening nothing

Under this project's own new R60 criterion 3, each of these ends in this record. None opens a row,
and none becomes work unless the owner writes it onto the plan in his own words.

**R1** — `spec/internal-failure-log.md:36` still has the system open a queue row on its own when a
failure signature fires twice. The reason R60's new context sentence gives — "a review that opens
rows of its own fills the human's list with work nobody asked for" — is general, and this is a
sibling producer the policy did not reach. `recommendation · boundary-issue (composition)`

**R2** — `tests/test_authority_anchor.py` replaced an assertion that the advisory report actually
emits a candidate with an assertion that a literal line appears in the gate's own source. The
docstring names the gap honestly, which is why this is not a defect, but the substitute cannot fail
if the code path breaks. `recommendation · hard-to-monitor (observability)`

**R3** — `skills/director/SKILL.md:48`'s idea-for-later row now sends both branches to the same
place: "worth raising gets one live question", "unclear gets one live question of its own". Two
classifications with one output are one classification. `recommendation · over-general (abstraction)`

**R4** — the reply's row order now has two declared homes. `scripts/state-probe.sh:144` says
"~/.claude/playbook/CLAUDE.md ... Change it there first"; line 146 says "The order is the rulebook's
rule 38". Rule 4 asks for one. `recommendation · internal-conflict (consistency)`

**R5** — `evals/director/closing-scenarios.json`'s `recorded_run` block now carries both
`"date": "2026-09-04"` and `"recorded": "2026-09-04"`. Two fields, one fact.
`recommendation · internal-conflict (consistency)`

**R6** — criterion 5 states how a rowless promise is held but never how that state ends. Every other
target-tag state has a red transition; this one has none, so a promise can sit tagged and archived
indefinitely with nothing ever asking whether it is still a promise. If criterion 5 survives F3, it
owes a sentence naming what returns the tag to a row or removes it.
`recommendation · stuck-state (liveness)`

**R7** — `evals/director/traces/idea-add-a-date.json` lost its trailing newline in the re-record.
`recommendation · later · hard-to-operate (ops-ux)`

## Phase 3.5 — Acknowledged gaps

`docs/upstream-notes-2026-09-04.md` flags the upstream drift itself; F6 is the second-order
consequence it does not spell out — that a suite assertion now depends on it.
`tests/test_authority_anchor.py`'s docstring flags its own uncovered firing shape; R2 is that gap,
already named by the author. `evals/director/closing-scenarios.json`'s `judgment_read` flags the
score spread and routes it to q-820, which exists and is well-formed with the owner's own worry as
its source, so no finding is filed for it.

## Phase 4 — Human and operational factors

`scripts/plan_checks_core.py`'s `normalize_mark` maps a retired 👁️ silently to ⬜. The docstring
argues this beats falling through every comparison, which is right, but nothing tells anyone it
happened: a row typed 👁️ reads as queued forever and its author never learns the mark is gone. A
one-line note on the printed row would close it. Not filed as a finding — no invariant stands behind
it, and it belongs with the recommendations above in spirit.

`scaffold/status-view/state-probe.sh:122` still renders a `BLOCKERS` section from a host's
`PLAN.md`, and `templates/PLAN.template.md` no longer lands one. The `grep -q` guard makes it inert
rather than broken, and hosts keeping their own Blockers section are served correctly, so this is
noted and not filed.

Domain language on the person-facing surfaces reads clean. Rule 36's rewrite, rule 38's prose and
the board column sub-line ("a real outside cause stops it — each card says why") all speak in the
person's words with no codes or script names leaking through.

## Phase 5 — Closing

**Top three to fix before this pushes.** F1 (one line in `matrix/guardrails.md:44`; the suite is red
until it lands). F3 with F2 and F4 riding on it (criterion 5 is in the wrong requirement; the
cheapest repair puts two deferred rows back on the board and needs no spec change). F6 (a green that
depends on a local edit to another repository's untracked file).

**Sentences the spec should state.** "A row leaves the queue's body only at a terminal exit or on
the person's own word, and a row that left on the person's word carries its revisit trigger with it."
"Every target tag has exactly one owner at any time, and a tag whose owner is an archive record names
the row that record covers."

**Open questions only the owner can answer.** Does his 01:17 word retire the deferred tier of R5, or
only the six-mark vocabulary? The answer decides whether F3's repair is two rows going back on the
board or an amendment to R5. And did he set the blocked-before-reopened order of F7, or was it the
pack's own reading of his word?

**`[default]` tags.** No `[default]`-tagged sentence was added or removed in this delta, so the
standing count is unchanged and no oldest-five call is owed here.

**Readiness: needs another iteration.** The R60 half is ready to push once F8 and F9 close. The R1
half should not push in its current shape.

## My answer on criterion 5

**It does not hold, and the second adversarial reviewer was right — though for a narrower reason
than the one they gave.**

The charge of "a gate widened to admit its own case" is fair on the shape but not decisive on its
own. The owner's decision genuinely created a state the spec had no word for: a promise standing
with no row building it. Meeting a new state with a new clause is ordinary spec work, and the second
map is honestly self-closing in the direction that matters — a tag in neither map still reds, which
is more discipline than a real loophole would carry.

What sinks it is that the state already had a home, and criterion 5 put it somewhere the spec
forbids. R5 criterion 3 gives a deferred row the queue's body and its revisit trigger; q-385 and
q-816 carry those triggers verbatim in the very record that files them away. R5 criterion 2 says the
archive holds "only wishes no longer due back"; the record's own closing line says each of them
returns. So criterion 5 does not fill a gap — it routes three deferred rows around a rule that
already covered them, and ties a suite check to a file whose existence proves nothing (F4). The rule
39 reading and the internal-consistency reading arrive at the same place: this is machinery added to
explain a fact rather than the fact being changed back.

The repair is smaller than the criterion. Put q-385 and q-816 back in `## Tasks` as deferred rows —
criterion 3 covers their tags with no edit at all. Drop E-18's `[target]` line, since the owner's own
word on onboarding was to clear it out. `TARGET_ARCHIVE_OWNERS` then empties, criterion 5 comes out,
and the rule-39 origin note in `rule-origins.md` stands true without contradicting the spec beside
it.

If the owner's 01:17 word does retire the deferred tier — a reading I can construct but will not
apply as his — then the change this delta owes is to R5, naming a fourth exit and widening what the
archive may hold. Even then criterion 5 stays unnecessary: with R5 amended, criterion 3's tie needs
only the word "or archived" and no new case of its own.
