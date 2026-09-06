# Skill review — build-pipeline after the closure-kernel repair

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-06
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with two review defects folded and one more the eval pair forced — the body claimed
Director is the only first reader while its own setup section carves an entry Director never sees,
the reference restated the lane cap thirty lines above the sentence that says the lane law is not
repeated there, and the closing paragraph named only half of when a redefinition is the person's
fork, which two independent producers then read the same wrong way

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

```
$ python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Both run against the documents' final state, after the folds below.

## What changed

The adversarial push review of `aa361dea..7993fa9b` (commit `9edf7c25`) edited
`skills/build-pipeline/references/accepted-work-execution.md` in three places: `hold --lanes <n>`
gained the lane-cap bound and the board's in-work column split behind it, take-up gained a refusal
for a row whose checkpoint stands closed with T8 `reopen` named as the door back, and `close` gained
the clause that it reads the receipt whatever the checkpoint's own status. The skill body did not
change in that commit.

Two documents were reviewed separately, each read cold by its own fresh agent:
`skills/build-pipeline/SKILL.md`, and `references/accepted-work-execution.md` read alongside the
body it hangs off. Both were asked the same four questions the reviews before this one used:
whether every paragraph is needed at the depth it sits, whether an agent can tell when the document
applies, whether any rule has two owners or any pointer cycles, and whether a quiet message — a
question, a thank-you, a musing, an answer to a question the agent asked — leads to execution or a
task. Every finding below was checked against the file before it was acted on.

## Folded

- **"Director is the only first reader" is false in this document's own next section.** The body's
  reader quoted the opening — "Director is the only first reader. It classifies every act, says
  whether the turn proposes new work or changes existing work, and returns a route contract" —
  against the setup section, which says a session that hears "attach live-spec to this project"
  runs a setup walk first and that "The setup entry stands outside the derivation chain", and
  against the skill's own `description`, which lists those spoken forms as triggers. So one class
  of human message reaches this skill matched by its own description, with no Director route in
  front of it, while the first sentence an agent reads says that never happens. The sentence now
  reads "Director is the first reader of every message but the setup entry below", which fixes the
  absolute claim where it is made rather than adding a second sentence to qualify it. Nothing
  pins the old wording: `tests/test_front_door_boundaries.py` reads the section headings and the
  quiet-turn sentence in Director, not this one. `SKILL.md`: 8,002 → 8,040 bytes.
- **The lane cap is stated in a file that says it does not state the lane law.** The reference now
  reads, in the take-up paragraph, "`<n>` is bounded by the profile's lane cap, and so is the number
  of rows standing in hand at once"; thirty lines later the same file reads
  "`skills/live-spec-base/SKILL.md` rule 7 carries the lane law in full and is not repeated here".
  Rule 7 does carry it — "Lanes roll unasked up to the profile cap (`lanes.cap`, default three
  [E-13]) (SPEC T-18)" and "The act reads the profile cap [E-13] and refuses a lane past it" — so
  the new sentence is the two-homes shape this pack forbids, and the same shape the reviews of
  2026-09-05 folded twice on this pair of documents. What the sentence adds that rule 7 does not
  carry is the board's own consequence, and that half stays: the paragraph now reads "The number of
  rows standing in hand at once is bounded by the same profile cap rule 7 carries: the board splits
  the in-work column into exactly that many lanes, so a row past the cap is a row with no lane to
  stand in." Nothing pins the old wording — `spec/work-board.md` criterion 27 and
  `scripts/task-admission.py:744` state the column split on their own.
- **The same fold repairs the paragraph the insert broke.** `9edf7c25` wedged both new sentences
  between `hold`'s freeze and the sentence that names it — "…T8 `reopen` is the door back. From that
  freeze on the task is spoken in those words letter for letter" — on a 152-character line, so the
  referent of "that freeze" sat two sentences away from the freeze. The freeze sentence is back
  against `hold`, and the two facts the commit added follow it.
  `references/accepted-work-execution.md`: 17,375 → 17,368 bytes.

## Kept, with the reason

- **The three closing commands stand in the body and their refusals again in the reference.** The
  reference's reader called this a defect and quoted all three pairs — the body's "`verify <id>
  --by <name> …` — the acceptance receipt, refused when `--by` names the row's own holder" against
  the reference's "`--by` is refused when it names the row's own holder, because the holder is the
  producer", and the same for `correct` and `close`. It is the decision the fourth review of
  2026-09-05 recorded and it has not changed: the body's own header says "Loaded alone, every
  section below still runs", so a session holding only the body would otherwise learn that a
  receipt exists and not what to run to write one. The reference carries the mechanism behind each
  clause, which is what that section is for. The reader also noted, correctly, that the reference
  keeps the opposite discipline one paragraph over for the statement fields; the difference is that
  a body-only session can still derive a statement by reading the body, and cannot write a receipt
  without the flags.
- **The "full execution procedure" pointer against the body's own self-sufficiency claim.** The
  body's reader read "Read references/accepted-work-execution.md for the full execution procedure"
  against "Loaded alone, every section below still runs" and asked whether the reference adds
  interpretation only or a materially different procedure. This is the same finding the third
  review recorded as the execution procedure's two apparent homes, and it is settled the same way:
  deciding what the always-loaded body owns against what the reference owns runs across both whole
  documents, which is larger than a review fix.
- **The MINOR-bump gate's own entry is left unstated.** The body's reader noted that the setup
  entry says outright that it stands outside the derivation chain while the gate section says
  nothing about whether it needs a Director route. The second review of 2026-09-05 already weighed
  this and left it: the gate is a moment inside a landing rather than a way a human message enters,
  and a sentence saying so would grow the always-loaded body for a case the pipeline only reaches
  from inside itself. The fold above says "every message but the setup entry below" for the same
  reason — the gate is not a message.
- **The one-row specialist table and the craft ladder's two worked sentences.** The body's reader
  read the single-row table as incomplete beside eight craft steps, and the "on a prose product…on
  infra…" pair as reference material sitting in the body. Both are pinned:
  `tests/test_traceability.py::test_director_names_test_author_at_the_derivation_step` puts that
  exact row here with a recorded red proof behind it, and `::test_craft_ladder` states this
  ladder's one home is build-pipeline.
- **The reference's forward pointer to "The specialist brief" at its own foot.** The reference's
  reader named it as the one place content is stated twice inside the file, and called it not a
  defect itself. It stays: the pointer is one clause and the section it names is three sentences.
- **The 2026-08-08 tlvphotos incident.** Unchanged from the second, third and fourth reviews, and
  unchanged for the same reason: build-pipeline has no rule-origins file, and standing one up for a
  single paragraph is machinery this pack keeps refusing.

## Clean on these

Neither document points back into Director. The body names Director descriptively and says "This
skill never reclassifies the message"; the reference opens with "classification stays in Director
and nothing here reclassifies the person's message", and its one forward mention of Director — "the
first wish enters through `director` like any other request" — describes a later message, not a
re-read of the one in hand. On quiet messages both hold: the body's "A route for a question writes
nothing; a correction names existing work and writes nothing new", and the reference's "A question,
an idea, an observation Director routed as evidence, or a halt gets no sheet, per above — and
nothing below applies to it". Every pointer in both documents resolves. The body is 134 lines and
the reference 251, both inside the 500-line guidance.

## The eval pair beside this review, and the third fold it forced

The reference changed in `9edf7c25` and again in the folds above, so the closing set was recorded
twice under the protocol `evals/build-pipeline/README.md` states. That pair came back 8 of 9 twice
with the same red on both runs — the first shared red the set has produced — and under that
directory's own rule a scenario red on two separate recordings is a finding that gets fixed on the
pipeline side, not recorded again. Both producers held
`ask-when-the-change-reaches-past-what-was-ordered` open, which the fixture expects, and both
labelled the reason "ordinary delivered result": a delivered change reaching past the narrow
instruction had no home among the three cases rule 12/27 reserve for the person, because the
closing paragraph said only that a redefinition he ordered himself is not the third case and said
nothing about the converse. The reference gained that missing half, in the same sentence's shape —
where a delivered change reaches past what he ordered and redefines behaviour he never named, that
wider half is the third case, and an artifact describing the old behaviour is what the change is
weighed against rather than a decision to change it.
`references/accepted-work-execution.md`: 17,368 → 17,641 bytes. The set was then recorded twice
more against the edited text and came back 9 of 9 twice, intersection and symmetric difference both
empty. Both pairs are written up in the README's run log under "2026-09-06 (the reference after the
push review) — a shared red, and the pair that cleared it".

Final sizes after every fold on this page: `SKILL.md` 8,002 → 8,040 bytes,
`references/accepted-work-execution.md` 17,375 → 17,641 bytes. The validator output quoted above
was run against those final bytes.

---

# Skill review — build-pipeline after the kernel's four holes, the wake-up rule and the prover pass

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-06 (evening, the session's final pass)
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with one defect folded — the reference cites the rules reserving the three human
cases as bare "rule 12/27" while giving rule 7 its file in the same document, so a cold reader
cannot see which ladder those two numbers belong to; every other finding from both readers is a
decision already recorded above or on 2026-09-05, or is pinned by a test.

## The tool's own verdict

```
$ python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Both run against the documents' final state, after the fold below.

## What changed since the section above

The section above closed with `SKILL.md` at 8,040 bytes and the reference at 17,641. Both moved
again the same day: the kernel's four holes were closed in `scripts/task-admission.py` and the
reference gained the three sentences that state them, the body's `verify` signature was corrected
to the reference's (`[--command ...]`, `<path-or-url>`), the reference took the owner's word of
15:24 as the wake-up rule, and a prover pass then added the round-two monitoring rule, the brief's
line about a lead watching its own spawns, the estimate-basis rule, the pre-spawn paragraph, and
the reopen/abandon repairs. `SKILL.md` stood at 8,065 bytes and the reference at 20,702 when this
review opened.

Two documents were read separately, each by its own fresh `sonnet` agent holding only that
document — the reference's reader also held the body, as context and not under review — with no
repository, no other file, and no sight of any earlier review. Both were asked the same four
questions every review on this pair has used: whether every paragraph sits at the depth it belongs,
whether an agent can tell when the document applies, whether any rule has two owners or any pointer
cycles, and whether a quiet message leads to execution or a task. Every finding below was checked
against the file before it was acted on.

## Folded

- **The reference cites "rule 12/27" with no ladder named, in the one file that gives rule 7 its
  path.** The reference's reader quoted "a row's own definition of done that names his eye as the
  check is describing one of the three cases rule 12/27 already reserve for him" and "For the taste
  calls rule 12/27 reserve for him" against the same file's "`skills/live-spec-base/SKILL.md` rule
  7 carries the lane law in full and is not repeated here", and called the asymmetry a routing
  defect: a reader who meets those two numbers cold has nothing saying which rulebook they index.
  Checked and true — `grep` finds "rule 12/27" nowhere in this repository but those two lines, and
  the rules themselves are `skills/live-spec-base/SKILL.md:194` ("The human's gates are the
  human's") and `:258` ("The seat decides what it can decide"). The fix names the ladder at the
  first mention and nowhere else, in the pack's own established form — `skills/spec-author/SKILL.md`
  writes "base rule 27" and `skills/design-reviewer/SKILL.md` "Base rule 27" — so the citation
  gains its owner without a second path statement or a repeated word three lines apart:
  `references/accepted-work-execution.md:178` now reads "base rule 12/27 already reserve for him".
  Nothing pins the old wording; no test in the tree matches the string at all.
  `references/accepted-work-execution.md`: 20,702 → 20,707 bytes. `SKILL.md` unchanged at 8,065.

## Kept, with the reason

- **The craft ladder read as reference material inside an always-loaded body.** The body's reader
  ranked this its first real defect and quoted all eight craft postures, arguing a turn touches one
  or two of them. It is pinned:
  `tests/test_traceability.py::test_craft_ladder` asserts this section's heading and four of its
  phrases in `skills/build-pipeline/SKILL.md` by name and records that the ladder's one home is
  build-pipeline, so moving it to a reference would red the suite and move a fact the SPEC points
  here for. The same reader flagged, unconfirmed, that citing SPEC INV-33 and then stating the rule
  in full might be a second home; the test says the opposite — the SPEC pins the invariant, this
  page holds the ladder.
- **The one-row specialist table.** Named again as unclear-whether-deliberate. It is pinned to this
  exact row, character for character, by
  `tests/test_traceability.py::test_director_names_test_author_at_the_derivation_step`, with a
  recorded red proof behind it, and the same test forbids the body from restating test-author's own
  method beside the call. Recorded as kept in the review above for the same reason.
- **No stated path for the person's answer to a question the pipeline itself asked.** The body's
  reader called this a real gap and asked for one sentence after the admission list. Adding it would
  put a classification rule in the pipeline body, which is Director's one home:
  `tests/test_front_door_boundaries.py::test_a_quiet_turn_loads_no_pipeline` pins "A question,
  musing or conversation is answered without loading a pipeline." in `skills/director/SKILL.md`, and
  the body already says "This skill never reclassifies the message" and "A route for a question
  writes nothing". The reader itself found the structural protection sound — the admission facts
  deny a row to anything with no source, outcome and machine-decidable done — and the reference's
  reader reached the opposite conclusion on the same case, calling it a scope boundary rather than a
  defect.
- **The MINOR-bump gate's trigger is not self-contained in the body.** Named again, as it was in the
  second review of 2026-09-05 and the section above. Unchanged for the same reason: the gate is a
  moment inside a landing, not a way a human message enters, and a sentence saying so would grow the
  always-loaded body for a case the pipeline only reaches from inside itself.
- **The lane-cap sentence against the same file's "not repeated here".** The reference's reader
  found this independently and ranked it a real defect. It is the finding the review above already
  folded, and the half that stayed is deliberate: `skills/live-spec-base/SKILL.md:141` and `:152`
  carry the cap and the refusal, and neither carries the board consequence — "the board splits the
  in-work column into exactly that many lanes" — which `spec/work-board.md` criterion 27 and
  `scripts/task-admission.py` state on their own. Re-read against rule 7's actual text before this
  was decided, not taken from the earlier record.
- **`--by` refused for the row's own holder, in both documents.** Named as a duplicate, and the
  reader itself judged it justified by the body's "a session holding only this page can run them".
  Same decision as the fourth review of 2026-09-05 and the one above.
- **The dated incidents — tlvphotos 2026-08-08, the three unrelated estimate ranges, the pre-spawn
  defect.** The reference's reader wanted all three moved to a rule-origins file. build-pipeline has
  no such file, and standing one up for three clauses — two of which are a single parenthetical
  each — is machinery this pack refuses (base rule 39). Unchanged from four earlier reviews.
- **"Past the second or third round" beside "never lets a cascade run to a fourth round".** Named as
  a phrasing split. The two agree: stopping at the second or third round is what never reaching a
  fourth means, and the brief's line is what a lead is told, not a second threshold.

## Clean on these

Neither reader found a rule folded into Director, and neither document reclassifies the message:
the body says "This skill never reclassifies the message", the reference opens with "classification
stays in Director and nothing here reclassifies the person's message". On quiet messages both hold
— the reference states the guard twice, at the head of the file and again at the head of Execution
("A question, an idea, an observation Director routed as evidence, or a halt gets no sheet, per
above — and nothing below applies to it"), and the body's admission facts refuse a row to anything
without them. Every pointer in both documents resolves, and neither reader found a cycle. The body
is 135 lines and the reference 291, both inside the 500-line guidance.

## The eval pair beside this review

Both documents' final bytes, after the fold above, were put through the closing set twice under the
protocol `evals/build-pipeline/README.md` states. The pair is written up in that README's run log
under "2026-09-06 (the session's final pass) — the pair on file"; `recorded_run` in
`closing-scenarios.json` carries its hash, score and producers, and its `status: stale…` note is
gone with the runs it described.

Final sizes after the fold on this page: `SKILL.md` unchanged at 8,065 bytes,
`references/accepted-work-execution.md` 20,702 → 20,707 bytes. The validator output quoted above
was run against those final bytes.
