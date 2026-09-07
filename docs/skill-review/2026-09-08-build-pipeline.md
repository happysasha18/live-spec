# Skill review — build-pipeline (record-read admission, narrowed stop-and-ask)

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-08
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/scripts/quick_validate.py`

Verdict: passes; no defect found. Both edits check out against the spec text they implement.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

## What changed

Against `origin/main`, two edits, both in service of SPEC Requirement 321 (`spec/queue-intake-
priority.md:761`, INV-327):

- `SKILL.md`'s admission-facts list gained a fifth bullet: read `python3 scripts/task-
  admission.py prior <words>` before writing a route, and admission refuses a reference that
  resolves to nothing on record. The write door's own sentence gained "the record's own read, and
  a title the record already carries" as refusal grounds, plus the one road past that refusal — a
  `supersedes` record naming the row, what is new, and why the standing decision does not cover it.
- `references/accepted-work-execution.md` narrowed when the pipeline stops to ask a question. The
  old text claimed the pipeline "still proceeds once heard out, on the human's word either way" —
  an unconditional claim. The new text splits it: one rare case (the request reads as an oversight
  or a slip) waits for a plain answer; every other disagreement is stated in one sentence and the
  work carries on.

## Findings

1. **The `prior` command matches what the body claims for it.** `scripts/task-admission.py:1666`
   `prior()` reads, in order, the rows on the live plan and queue archive, the decision record, and
   the commit log (`git log --oneline`), and returns every line carrying all the given words, "no
   similarity score here and no cutoff". That is exactly Requirement 321 criterion 6 and the body's
   "prints the rows on the live plan, the rows in the queue archive, the decisions on record, and
   the commit subjects carrying those words." No finding.

2. **`read_prior_record` and `read_supersedes` back the refusal the body now states.**
   `scripts/task-admission.py:140` refuses a route with no `prior_record` naming what was read and
   what it found; `:164` `read_supersedes` refuses a `supersedes` record missing any of names/new/
   why. The body's new sentence — "the one road past that refusal is a `supersedes` record naming
   that row, what is new in this request, and why the decision already on record does not cover it,
   and all three land on the admitted row" — is the plain-language form of that code and of
   Requirement 321 criterion 5, word for word on the three fields. No finding.

3. **The narrowed stop-and-ask text matches Requirement 321 criteria 7 and 8, not a looser
   paraphrase of them.** Criterion 7: "when the request reads as an oversight — the person appears
   to have forgotten something already settled, or to have made a slip — the system shall ask one
   plain question and wait for the answer." The reference: "Where the request reads as an
   oversight — the person appears to have forgotten something already settled, or to have made a
   slip — the pipeline asks one plain question and waits." Near-verbatim. Criterion 8: "state the
   conflict in one sentence and shall carry on with the work" against "say it in one sentence and
   keep going." Same content, and the reference cites the criteria numbers directly. No finding.

4. **The edit is a correction of an overstatement, not a new behaviour bolted on.** The removed
   sentence — "the pipeline still proceeds once heard out, on the human's word either way" — was
   flatly false once criterion 7 exists: a real oversight case does wait. The fix narrows the claim
   to match the rule already on record rather than adding a second, competing sentence beside the
   false one. No finding.

5. **No collision with rule 39 (live-spec-base) on inventing machinery.** The new admission field
   is not a threshold, counter, or gate invented from nothing — it wires the write door to a read
   the pipeline already needed (the record) and a command (`prior`) that already exists in
   `scripts/task-admission.py`. No finding.

## Size

`skills/build-pipeline/SKILL.md` and `references/accepted-work-execution.md` both stay comfortably
under the pack's guidance; the diff added four lines to the body and nine to the reference.
