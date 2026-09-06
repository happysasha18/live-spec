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
