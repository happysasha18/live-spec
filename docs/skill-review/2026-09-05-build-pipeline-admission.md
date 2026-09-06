# Skill review — build-pipeline admission

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-05
Reviewer: skill-creator (OpenAI)

Verdict: passes; the description, accepted-work trigger, admission contract and referenced execution detail were reviewed

## The tool's own verdict

```
$ python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

## What changed

build-pipeline now begins only after Director returns a work route, validates admission, writes the
one board row and checkpoint, and owns execution through close.

## Findings

- Folded: the old short adapter gave execution no owner after Director was cut. The operative
  procedure and its references now live here.
- Folded: admission was prose-only. The skill now calls `scripts/task-admission.py`, whose tests
  prove question/correction zero-write cases and one-row/one-checkpoint new work.
- Folded: setup trigger coverage required the exact spoken setup forms in the description; they are
  present without making ordinary conversation a trigger.
- Kept: long execution detail is behind one reference so it loads only after accepted work exists.

---

## Second review — Anthropic skill-creator, 2026-09-05

Date: 2026-09-05
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with two defects folded — a roadmap aside left the always-loaded body, and the
execution reference no longer contradicts its own worked example on what earns a decision sheet

This is a second, independent review beside the OpenAI skill-creator review above. It does not
replace that verdict. Two documents were reviewed separately, each read cold by its own fresh
agent: `skills/build-pipeline/SKILL.md`, and `skills/build-pipeline/references/accepted-work-execution.md`
read alongside the skill body it hangs off. Both were asked the same four questions: whether every
paragraph is needed at the depth it sits, whether an agent can tell when the document applies,
whether any rule has two owners or any pointer cycles, and whether a quiet message — a question, a
thank-you, a musing, an answer to a question the agent asked — leads to execution or a task. Model
evals were not run; they are a separate stage.

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

## Findings folded

- The MINOR-bump gate ended "— until Package 5 gives this gate its own permanent home." That clause
  says nothing about running the gate; it records where the gate is expected to move, in a body that
  loads on every trigger. It was cut. The gate's own contents stay, because
  `tests/test_crosscut_counter.py` reads the cross-cut counter out of this body.
- The execution reference said "For a question, an idea, an observation or a halt there is no sheet",
  and repeated it as "A question, an idea, an observation or a halt gets no sheet, per above". The
  worked example directly below is an observation and carries a full nine-line sheet, so the document
  contradicted itself on the same page. Both sentences now say "an observation Director routed as
  evidence", which keys off the route contract's own action field rather than re-deriving Director's
  beyond-doubt test here. The reference gained 58 bytes and is loaded only once work is executing.

build-pipeline came down from 6,342 to 6,281 bytes; the reference went from 12,427 to 12,485.

## Findings not folded, and why

- The craft ladder — "Each artifact is judged by its own craft's standards" through the work-kind
  paragraph — is judgment standards used at the judging step, not on every load, so it reads as a
  candidate for a reference. It stays: `tests/test_traceability.py::test_craft_ladder` states this
  ladder's one home is build-pipeline, the body is 6 KB with no pressure on it, and moving a KB out
  of a document that only loads after work is accepted buys nothing this row is trying to buy.
- The description names the MINOR-bump gate as a trigger, and unlike the setup walk — which says
  outright that it "stands outside the derivation chain" — the gate section never says whether
  reaching it needs a Director route first. Read as written, the gate is a moment inside a landing
  rather than a way a human message enters, so no sentence was added; saying so would grow the body
  for a case the pipeline only reaches from inside itself.
- The execution reference carries the 2026-08-08 tlvphotos incident in full — a rejection that
  arrived mid-conversation while the task state read "awaits his walk" for two hours. It is history
  behind a rule, not the rule, and it loads whenever work executes. It stays because build-pipeline
  has no rule-origins file, and standing one up for a single paragraph is machinery this row exists
  to avoid.
- The specialist-brief paragraph says the fixed protocol it replaces "carried tier ladders, escrow
  law and a reporting bureaucracy... none of it survives the cut into this skill", while
  `skills/build-pipeline/references/delegation-protocol.md` is still in the tree and
  `tests/test_delegation_line.py` requires its content as part of this skill's normative surface.
  The text and the gate disagree about whether that file is retired. Settling it means deciding the
  file's home, which is larger than a review fix.
- The one-row specialist table pairing Test author with its call condition looks like an odd shape
  for a table, and it repeats a row Director's own specialist table carries. It stays:
  `tests/test_traceability.py::test_director_names_test_author_at_the_derivation_step` pins that
  exact row here, with a recorded red proof behind it, because the pipeline is what calls the
  specialist after admission while Director only names it.

## Clean on these

Every pointer in both documents resolves: the six references named in the body exist, and so do
`scripts/task-admission.py`, `scripts/checkpoint.py` and `scripts/open-lane.sh`. No pointer cycle
runs back to Director — the body names Director descriptively and says "This skill never
reclassifies the message", and the reference opens by saying classification stays in Director. The
hand-off sentence is unambiguous read alone: "It begins only after that contract exists, and owns
everything from a candidate's observable outcome and definition of done through verification and
close." Nothing essential hides behind an unfollowed pointer. On quiet messages both documents
hold: "A route for a question writes nothing", the derivation list refuses a row when source,
outcome or definition of done is missing, and the reference is only reached once Director has
already routed work here. The body is 104 lines and the reference 185, both inside the 500-line
guidance.

---

## Third review — Anthropic skill-creator, 2026-09-06, the statement half

Date: 2026-09-06
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with one defect folded — the execution reference restated the four statement fields
and the validate command the skill body already owns, and now states only what the body defers to it

The two documents changed the same day: the skill body gained a paragraph saying admission derives
the task's statement and that validation runs before take-up, and the execution reference gained the
procedure behind it plus one sentence putting the closing check on real data. Each was read cold by
its own fresh agent, on the same four questions the second review used: whether every paragraph is
needed at the depth it sits, whether an agent can tell when the document applies, whether any rule
has two owners or any pointer cycles, and whether a quiet message could be read as work to admit.

### The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Run by both readers independently, on both documents' final state.

### Folded

- **The reference restated the body.** Both readers found it, separately, and both quoted the same
  pair of sentences: the body's "Admission also derives the task's statement onto that row — an
  echo-name of two to five words, a description a stranger can act on, a plan whose steps stand in
  the order they run, and a time estimate given as a range" against the reference's "Admission
  derives that statement from the route the pipeline already holds — echo-name, description, plan,
  estimate". Same four fields, same person-never-writes-it fact, same command, stated twice. The
  second reader pointed at the discipline the same file already keeps one paragraph over — "rule 7
  carries the lane law in full and is not repeated here" — and asked for the same shape. The
  reference's opening now says the body carries those and is not repeated, and goes straight to
  what the body defers: who writes the reader's file, and what take-up freezes.
  `references/accepted-work-execution.md`: 14,069 → 14,027 bytes.
- **The verify sentence repeated its own paragraph's thesis and borrowed one project's nouns.** It
  read "the page as it renders, the archives as they stand", which the reader took as a rule about
  web pages and photo archives rather than an illustration. It now reads "the thing as it actually
  runs, over the records it really reads — never a stand-in built for the test, and never the
  producer's own test alone."

### Kept, with the reason

- **The body still names the `validate` command rather than deferring all of it.** The first reader
  asked for the new paragraph to collapse to a policy sentence and a pointer, since it already ends
  by deferring half its subject. It stays as it is: `hold` refuses a row whose validation has not
  passed, and this is the one gate an agent must run before it takes work up. The body's own header
  says "Loaded alone, every section below still runs" — a session that loaded only the body would,
  under the shorter wording, learn that a gate exists and not what to run.
- **The execution procedure has two apparent homes.** The first reader read the body's pointer
  ("Read references/accepted-work-execution.md for the full execution procedure") against the body
  then narrating admission itself, and called it two homes for one fact. It predates the statement
  half and is the same finding the second review recorded about the reference's own depth. Settling
  it means deciding what the always-loaded body owns against what the reference owns, across the
  whole document — larger than a review fix, and not this row's work.
- **The new reference paragraph does not restate its own precondition.** The second reader noted
  that "A task enters work only through a validated statement" reads as a free-standing universal
  to an agent that lands on it from a search rather than reading down the page. The two carve-out
  lines twenty lines above already fence the section ("For a question, an idea, an observation
  Director routed as evidence, or a halt there is no sheet", "and nothing below applies to it"),
  and repeating the fence per paragraph is the shape this document already refuses.
- **The 2026-08-08 tlvphotos incident and the reference's own depth.** Unchanged from the second
  review, and unchanged for the same reason: build-pipeline has no rule-origins file, and standing
  one up for a single paragraph is machinery this pack keeps refusing.

---

## Fourth review — Anthropic skill-creator, 2026-09-06 (the trusted closure kernel)

Date: 2026-09-06
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with one defect folded — the body's new closing section restated four of the
reference's ten clauses almost word for word, found separately by both cold readers, and now states
the law plus the three commands with the clauses' one home named

Two documents were reviewed separately, each read cold by its own fresh agent:
`skills/build-pipeline/SKILL.md`, and `skills/build-pipeline/references/accepted-work-execution.md`
read alongside the body it hangs off. Both were asked the same four questions as the reviews above:
whether every paragraph is needed at the depth it sits, whether an agent can tell when the document
applies, whether any rule has two owners or any pointer cycles, and whether a quiet message — a
question, a thank-you, a musing, an answer to a question the agent asked — leads to execution or a
task. The eval pair was run beside this review and held no finding of its own.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

## What changed

The closure rule landed: the definition of done is fixed at admission and its sha256 rides on the
row, changing it is an explicit operation that keeps the previous text and hash with its source and
reason, an acceptance receipt is written by a verifier who is not the row's holder, and `close`
reads that receipt instead of an agent's sentence.

## Folded

- **The body restated the reference's clauses instead of pointing at them.** Both readers found it
  independently and both quoted the same pairs: the body's "The definition of done is fixed when the
  row is admitted and is never quietly rewritten afterwards" against the reference's "The definition
  of done (DOD) is fixed at admission and cannot be silently changed after work starts"; the body's
  "The executor hands over evidence and never issues the acceptance verdict itself" against the
  reference's "The executor may provide evidence but may not issue the final acceptance verdict
  itself"; the body's "Close is then a state transition code runs against that receipt, not a
  sentence an agent writes" against the reference's "close is a controlled state transition, never a
  textual claim by an agent". The second reader counted four of the ten clauses restated, the exact
  command and its flags included, and named the clean pattern the same file keeps everywhere else —
  one-line pointer, full content only at the far end. The body now carries the law in one sentence
  and the three commands a body-only session must be able to run (`correct`, `verify`, `close`),
  and says the reference is the clauses' one home. `SKILL.md`: 8,077 → 8,002 bytes.
- **The same fold removed the duplicated verifier sentence** the first reader flagged: the pipeline
  paragraph's "verify it without the producer's self-report" and the kernel's expanded restatement
  of it were the same rule stated twice on one page. Only the pipeline paragraph's version stands.

## Kept, with the reason

- **The three commands stay in the always-loaded body.** The first reader would have accepted a
  pointer alone. They stay for the reason the second review already recorded about `validate`: the
  body's own header says "Loaded alone, every section below still runs", and a session holding only
  the body would otherwise learn that a receipt exists and not what to run to write one.
- **The reference's ten clauses stay in the owner's own wording.** Both readers noted the clause
  list reads flatter than the prose around it. It is the fixed wording of the rule as it was given,
  and rewriting it into this file's register would make the reference a paraphrase of the law rather
  than the law.
- **"A change after verification voids the evidence" appears twice inside the reference** — once in
  the clause list and once in the `close` paragraph that says what it means in code. The second
  reader called it a third statement. It is the clause and its mechanism, which is what this section
  is for; collapsing them would leave the clause with no command behind it.
