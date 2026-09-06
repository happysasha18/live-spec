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
