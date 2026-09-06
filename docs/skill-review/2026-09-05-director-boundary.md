# Skill review — director boundary

SKILL-REVIEW

Skill: director

Date: 2026-09-05
Reviewer: skill-creator (OpenAI)

Verdict: passes; the description, trigger, route contract and on-demand references were reviewed

## The tool's own verdict

```
$ python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/director
Skill is valid!
(exit 0)
```

## What changed

Director now owns the first read and route contract only; accepted-work execution moved to
build-pipeline.

## Findings

- Folded: the old description still promised checkpoint, verification and close after those
  sections moved. It now stops at the route contract and points accepted work to build-pipeline.
- Folded: execution references made Director look like their owner. They now live below
  build-pipeline; Director retains only classification references.
- Kept: the detailed act distinctions remain in the main file because they are the judgment the
  skill must make on every turn, not optional explanation.

---

## Second review — Anthropic skill-creator, 2026-09-05

Date: 2026-09-05
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`

Verdict: passes with two defects folded — the hand-off for a correction, decision or halt now
names build-pipeline, and one sentence of retired-design history left the always-loaded body

This is a second, independent review beside the OpenAI skill-creator review above. It does not
replace that verdict. The document was read cold by a fresh agent that saw only
`skills/director/SKILL.md` and the four questions below: whether every body paragraph is needed on
every load, whether an agent reading Director alone can tell when build-pipeline gets loaded,
whether any rule has two owners or any pointer cycles, and whether a quiet message loads the
pipeline or creates a task. Model evals were not run; they are a separate stage.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/director
Skill is valid!
(exit 0)
```

```
$ python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/director
Skill is valid!
(exit 0)
```

## Findings folded

- The route contract read "A correction, decision or halt points at the existing work and creates
  none." It said what does not happen and never said who makes the change happen. The acts table
  meanwhile hands Director execution-shaped verbs — "change that work's goal and replan what is
  left", "record the decision and apply it to the work already running", "change the state of that
  work" — while the same page says the Director does not run the work. An agent reading Director
  alone could not tell whether a correction loads build-pipeline. The sentence now names
  `skills/build-pipeline` as the one that changes the existing work.
- The dimensions section carried "This is where the pack's old classification failed: its intake
  made a change that cut across everything choose one word for itself." The rule it explains — "These
  are dimensions, not classes" — is stated in full in the two sentences before it. What was left is
  the history of a design this pack no longer runs, loaded on every human turn. It was cut.

Director came down from 21,536 to 21,439 bytes across the two edits.

## Findings not folded, and why

- Two passages were named as pure justification loaded every turn: the paragraph opening "Say that
  in the numbers a verdict carries, because this is where it goes wrong in practice", and the pair
  opening "Grounds stated with an act carry their own act only when they say something new" and
  "Which act a standing clause is depends on which half of it is new". Both carry act-counting rules
  the scenario suite grades on, and this row's own history is the reason to leave them: the
  2026-09-02 cut of the Director was withdrawn when the same producers scored the trimmed version
  29 of 35 against 30, and on 2026-09-04 four added paragraphs turned three failing correction
  scenarios green. The scenario suite is the stop sign for a cut of that size, and it did not run in
  this review.
- "The idea just became the instruction it was waiting to become, and a fresh row opens for it."
  Director does not open rows, so the phrasing blurs the boundary, and read away from its own
  example it could be over-read as opening a row for any reply to a Director question. The example's
  condition is stated in the same sentence chain, the section's own rule is that nothing new was
  said, and the recorded scenario trace
  `evals/director/traces/not-an-act-answering-the-director.json` reasons from this exact wording to
  a correct verdict. Changing wording a passing trace rests on belongs with the scenario run, not
  here.
- `skills/director/references/footprint-read.md` exists and no sentence in `SKILL.md` points at it.
  Its own opening line still claims it is "referenced from `SKILL.md`'s intake line", which the
  intake's removal made untrue, and its content is execution routing — which steps run, how far each
  reaches — which now belongs to build-pipeline. The file is read by
  `tests/test_impact_analysis_entry.py` at its current path, so giving it a home is a move plus a
  test change, which is a decision for a later stage of this row rather than a minimal review fix.

## Clean on these

Every pointer in the body resolves: `references/request-kind-table.md` exists and carries the
routing principle and the five houses the pointer names, and every `skills/…` path in the specialist
table exists. No rule is stated in full in Director and also delegated away. The quiet-message path
holds: the acts table forbids a roadmap row for a question or musing, "A greeting, a thank-you, a
thumbs-up on something already agreed, a joke or a curse that reports nothing new: these are
conversation. Answer like a person and record nothing", and "An answer to the Director's own
question is not a new act" each close one of the four quiet cases, and the route contract answers a
question without loading a pipeline. The body is 318 lines, inside the 500-line guidance.

## Re-review 2026-09-06, after the q-823 reopening

Two classification sentences were added to `skills/director/SKILL.md` that night — one in *An idea
is not an instruction*, one in *Some observations carry their repair with them* — to settle three
`operation` reds two independent recordings agreed on. The body went from 21,977 to 22,548 bytes, so
the Anthropic review was run again over the changed file: one fresh Sonnet reader holding
`~/.claude/skills/skill-creator/SKILL.md`, this skill in full, its `references/` listing, and the
build-pipeline front matter and headings for the ownership question. It was given the four questions
below and nothing else, and it did not see this file.

Both quick validators pass on the changed skill: `python3
~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/director` and `python3
~/.claude/skills/skill-creator/scripts/quick_validate.py skills/director` each print `Skill is
valid!` and exit 0.

- **Progressive disclosure — pass with a caveat.** The body is 331 lines, inside the 500-line
  guidance. The caveat has two halves. The first is the orphan already on record above:
  `references/footprint-read.md` still exists, still opens by claiming it is "referenced from
  `SKILL.md`'s intake line", and no sentence in the body points at it — the reader found it
  independently and named it the single most-worth-fixing defect. It stays unfixed for the reason
  given above: the file is read by `tests/test_impact_analysis_entry.py` at its current path, so
  moving it is a move plus a test change, and this session's write-set did not include either. The
  second half is new: the reader judged that more than half the body is edge-case prose every turn
  loads — conditional requests, the standing-clause taxonomy, correction against decision against
  caution — and that skill-creator's own domain-organization pattern would push some of it into a
  reference, the way `request-kind-table.md` was already pushed. That is a real observation and it
  is not acted on here, because this directory's own record says what happens when this skill is cut
  on a size argument alone: the 2026-09-02 cut scored 29 of 35 against 30 and was withdrawn, and the
  2026-09-04 addition of four paragraphs turned three failing scenarios green. A cut of those
  passages has to be recorded against, not reasoned about.
- **Routing clarity — pass.** The route contract names every field returned and states where each
  outcome goes, and the specialist table names the skill each specialist lives in.
- **Circular ownership — pass.** Director's "Work that belongs elsewhere" and build-pipeline's own
  defer exactly what the other claims; the reader found no loop and no gap, and read the
  correction/decision/halt handoff as stated identically on both sides.
- **A quiet message loads no pipeline — pass.** Three places say it: the acts table's must-not column
  for a question or musing, "Not every message is one of the seven", and the route contract's own
  sentence. The reader called it unambiguous.

Nothing in the review contradicts the two sentences added that night; neither is quoted as a defect.
