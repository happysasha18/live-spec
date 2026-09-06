# Skill review — build-pipeline after the three closure guarantees

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-06
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`, read by a fresh
agent holding no context from the edit it judged.

Verdict: valid with four defects, all folded — the same fact stated in both documents three times,
one command signature that would exit 2 as written, a denial a body-only session could not clear,
and one claim stronger than the code makes.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Run against the documents' final state, after the folds below.

## What the change was

Three guarantees landed in `scripts/task-admission.py`, `guardrails/worker-admission-guard.py` and
`guardrails/check-close-receipt.py`, and both documents were edited to state them: the pre-spawn
rule moved onto the subagent tool itself, the verifier runs the acceptance the tree recorded for
the row instead of whatever the command line hands it, and the done's digest is anchored on the
checkpoint so deleting the row's hash line cannot mint a fresh contract.

## The findings, and what was done

1. **Two homes, three times.** The body and the reference each stated in full: what the verifier
   runs, where the done's digest lives, and what the spawn guard is. The body keeps the mechanic
   and the command shapes, because a session holding only that page has to be able to run them;
   the reference keeps what the body does not carry — the 2026-09-06 incidents each guarantee
   answers, `pre_spawn_check` as the one function the guard and the brief share, and the guard's
   two ceilings. This is the same defect two earlier reviews of this skill found, and it was
   folded the same way.

2. **A signature that would exit 2.** The reference wrote `hold --lanes <n>`; the CLI takes the id
   positionally and requires `--holder`. Corrected to `hold <id> --holder <name> [--lanes <n>]`.
   The line predates this change and was wrong before it.

3. **A denial a body-only session could not clear.** The body said the guard refuses a spawn
   without a recorded acceptance command and never said who writes one. Admission writes the row's
   `**Verification:**` prose and no key, so the body now says the key goes into
   `scripts/plan_checks.py` under the row's id by hand, before the first spawn. The reference
   dropped that half so it keeps one home.

4. **One claim stronger than the code.** The reference read "anchored where a hand cannot quietly
   reach it"; a hand can edit the checkpoint's `DOD:` line, and the code's own comment claims only
   that the row's copy is made tamper-evident. The sentence now says that, and says what the hand
   that reaches both copies still runs into: the receipt `close` reads out of the same file.

Nothing false was found in the three new claims themselves, and no coined term is used before it
is defined.

## Second pass — what the adversarial push review sent back to these documents

The adversarial read of the range (`docs/prover/2026-09-06-the-three-guarantees-and-their-own-holes.md`)
found three blocking defects in the code and, with them, two sentences here that the repaired code
no longer matched and two that were never true:

- the reference claimed a done row with a checkpoint must carry a receipt "whose frozen done is the
  done the row now reads" — true only once the gate reads the checkpoint's anchor, which it now
  does, so the sentence names the anchor;
- neither document said what the kernel does NOT hold. Both ceilings are now written down: no gate
  judges what an acceptance key TESTS, and a receipt is plain text in a directory the tree hash
  leaves out, so a hand-written one satisfies the close. What the kernel buys is stated in the same
  breath — forging a done now costs a forged receipt in the diff instead of one typed character;
- the body said the recorded key clears the spawn denial and did not say the same key is what
  `verify` runs, so a freshly attached host would meet the refusal at its first close with nothing
  in the body to explain it. The body now says both, and says that naming a closed row does not
  clear the guard.

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Run again against the documents' final state, after these folds.
