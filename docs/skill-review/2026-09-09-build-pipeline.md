# Skill review — build-pipeline (the closing kernel's verify bullet)

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-09
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/scripts/quick_validate.py`,
plus the skill-creator Skill Writing Guide applied by hand — progressive disclosure, one home per
fact, and the body matching what the tool does.

Verdict: PASS (`quick_validate.py`, quoted below), with four findings folded into the two files
this review holds edit authority over. The changed text was accurate about the executor and stated
one instruction; what it lacked was a single home for its own reasoning, the file's paragraph
shape, and the name of the thing a session has to change when the mode refusal fires.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

The same command was run again after the folds below and printed the same line.

## What changed

Commit 0aa429a0 edited the closing kernel's `verify` bullet in
`skills/build-pipeline/SKILL.md` and the matching signature in
`skills/build-pipeline/references/accepted-work-execution.md`: `--command` leaves the signature,
the recorded acceptance becomes the only command the receipt is made of, a command handed on the
command line is refused, a broader check is named as a manual run that closes no row, and a run
made under a mode the tree records as deciding no verdict writes no receipt. The reference gained
one paragraph carrying the reasoning.

## Findings

1. **The reasoning had two homes in one file.** The reference already carries a paragraph whose
   whole subject is this — "**The verifier runs the acceptance the row already recorded** — the
   body carries the mechanic and the command shape. Why it is so: until 2026-09-06 the receipt was
   made of whatever the command line handed it…". The new paragraph told the second half of the
   same story thirty lines earlier, so a reader met the `--command true` hole twice, once dated
   2026-09-06 and once dated 2026-09-09, with no line saying they are one hole in two stages.
   `folded` — the new paragraph's content moved into that existing home, as a second paragraph
   under the same bold claim, opening on where the 2026-09-06 fix stopped short.

2. **The new paragraph did not take the file's own paragraph shape.** Every explanatory paragraph
   in this stretch of the reference opens with a bolded claim and then the words "Why it is so",
   which is how the file marks the difference between what the body carries and why it is so. The
   new paragraph opened with a bare "It runs the recorded acceptance and that command alone",
   which restated the body's instruction and read as a second body rather than as the why.
   `folded` — the merge in finding 1 removes the restatement, and the reasoning now stands under
   the bolded claim that already governs it.

3. **Neither page said where a mode is named.** The refusal a session meets ends "Run this row's
   recorded acceptance with no mode named", and a session holding these two pages could not act on
   that: the mode is read from the environment, by `LIVE_SPEC_RUN_MODE`, or by
   `LIVE_SPEC_PUSH_FULL`, which `guardrails/run_modes.py` resolves as `release`. A run that
   inherited either variable would meet the refusal with no way to find what to unset.
   `folded` — the reference names both variables in one clause at the end of the merged paragraph.
   The body stays free of it, since the environment is a mechanic and the reference is the
   mechanics home.

4. **The body bullet stranded its own condition and repeated a phrase.** The bullet stated the
   recorded acceptance, then the manual run, then came back to "A row with no recorded acceptance
   cannot be verified at all" three clauses later, so the two facts about the recorded acceptance
   stood on either side of an unrelated one. "at all" also closed two adjacent sentences.
   `folded` — the recorded-acceptance facts are now one sentence, the refusals follow, and the
   manual run's own bookkeeping (its purpose and its finite sample, recorded before it starts)
   drops to the reference, which already carries it. The bullet keeps every instruction a session
   loaded on this page alone can act on.

5. **The body says a handed command is refused; the executor refuses a handed command that differs
   from the recorded key.** `scripts/task-admission.py`'s `verify` builds its refusal list as
   `[str(c) for c in commands if str(c).strip() and str(c).strip() != key]`, so a caller who
   retypes the recorded key exactly, or hands an empty string, passes through and the receipt is
   made of the recorded key either way. `rejected` — the sentence describes what the receipt is
   made of, and that holds on both branches; wording the exception would add a clause about a
   caller retyping what the tree already records, which changes nothing a session would do.

6. **`--command` still exists in the argument parser, and the body is right to leave it out.** The
   parser keeps the flag with a help string that opens "REFUSED", so a caller who passes it meets
   one stated reason instead of an unknown-argument error. The body's signature is a usage line,
   and the flag has no use. No finding.

7. **The frontmatter description still matches.** It names deriving the outcome and the done,
   admitting work, calling specialists, verifying, closing and reporting, and the setup and
   MINOR-bump entries. Nothing in it turned on `--command`, and the change moves no triggering
   context. No finding.

8. **"finite sample" is this tree's standing term.** It reads as a coinage on first meeting, so it
   was checked: `guardrails/run_modes.py`, `guardrails/check-acceptance-rerun.py`,
   `MIGRATION.md`, `PLAN.md` and the executor's own refusals all use it for what
   `run_modes.manual`'s `records_before_start` lists as `purpose` and `limit`. The changed text
   adopts a word the tree already speaks. No finding.

9. **The body matches the executor on every other claim.** Checked against
   `scripts/task-admission.py` line by line: `--by` naming the holder is refused, the key is read
   from `scripts/plan_checks.py` by the row's id, a row with no recorded key is refused with a
   sentence saying a command line cannot stand in for it, `named_mode` raises on an unknown mode
   name, a config that cannot answer `decides_verdict` refuses on its own fault, and a mode
   carrying `decides_verdict` false writes no receipt. `guardrails.config.json` records
   `run_modes.row` as covering the one accepted task's recorded acceptance with no check outside
   that task, and `run_modes.manual` as `decides_verdict` false. No finding.

## Size

```
$ wc -l skills/build-pipeline/SKILL.md skills/build-pipeline/references/accepted-work-execution.md
     171 skills/build-pipeline/SKILL.md
     398 skills/build-pipeline/references/accepted-work-execution.md
```

The body stands well inside the guide's ~500-line ideal, and the reference is the page it defers to.
