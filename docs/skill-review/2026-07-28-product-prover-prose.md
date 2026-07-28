# Skill review — product-prover (its body rewritten by the rules it holds a text to)

`SKILL-REVIEW`

Skill: product-prover
Date: 2026-07-28
Reviewer: this session, working against the skill-creator criteria. No fresh reviewer read it, because
the session's own instructions carried a line against dispatching workers. That line had no standing
word behind it and was lifted the same afternoon (2026-07-28), so the next session dispatches a fresh
reviewer. This record names what was checked and what was found.

Verdict: passes with two findings, both recorded as queue rows rather than fixed here.

## What changed

The skill body was measured against `guardrails/language-rules.json` and rewritten worst-first. Its
count fell from 253 findings to 27, and the README's from 40 to 15. No sentence in the body now runs
past the 25-word cap; 71 did this morning.

Three kinds of change:

- **Structure.** Four lists had collapsed into running prose, their items separated by a stray ` - `
  mid-sentence. The three review modes read as one paragraph. Inside the property-analysis phase, the
  declared-law demands, the five edge-condition checks, the paired-transition reads, and three whole
  lenses were buried the same way. Each is a list again, and the nesting matches the level it sits at.
- **Sentences.** About sixty sentences past the cap were split. Where the sentence carried a run of
  parallel items, the items became a list, which is the rule's own repair.
- **Capitals and denial frames.** Four literal tokens the pass prints now carry backticks: the three
  triage verdicts and the word a triage prints before the opening assessment. Two shouted words were
  lowercased. Two sentences naming a thing by denying its neighbour were rewritten as what the thing is.

## What was checked

- **The full suite is green**: 2217 passed, 0 failed, read from the run's own last line.
- **The suite caught twelve meaning losses**, which is what it exists for. Seven pinned phrases had
  been dropped or reworded by the rewrite and were restored in the text. The tests pin a phrase inside
  one line of the file, so a restored phrase also had to stay unwrapped. Four tests moved with a
  deliberate change of register (three shouted words lowercased, two labels backticked), and each of
  those moves is named in the commit.
- **The description still holds.** Every trigger phrase stands: the review verbs, "is this spec ready /
  what did I miss / poke holes in this", the uploaded document, and "Product Prover". One 57-word
  sentence became three.
- **Size.** 887 lines. That is past the ~500-line ideal for a skill body, and it was past it before this
  change; nothing was added.
- **No instruction was dropped.** The diff was read line by line against the old text. One example was
  lost in a first pass — the phrase "once there are several" among the four vague range clauses — and
  it was restored.

## Finding 1: a heading shouts, in this skill and ten others

`## When NOT to use` carries a capitalised word for emphasis, which the capitals rule refuses. The
carve-out list takes a defined term, an acronym, a document name, or a closed-vocabulary value, and this
word is none of them. The repair is one heading worded the same in every skill, so it belongs to a pass
over the whole pack. Queue row 519.

## Finding 2: twenty-five findings stand on a checker's reach

The style lint applies the spec-body person rule to this whole file, and a skill body is human-prose,
where the rule asks for the reader to be addressed directly. The 25 second-person findings are that
mismatch, already recorded as queue row 513 and stated inside the rule home. They were left alone.

## What a fresh reviewer should look at

Whether the restored list structure in the property-analysis phase nests at the level a reader expects.
Three lenses had been buried inside a neighbouring bullet's body, and lifting them to siblings is the
reading this seat made of a text that no longer stated its own shape.
