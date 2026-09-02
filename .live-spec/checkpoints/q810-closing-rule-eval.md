# A finished task is shown and closed; a complaint becomes new work, not a stuck one
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

(nothing yet)

## NEXT

(nothing yet)

## DECISION SHEET

Goal: prove the new director/SKILL.md closing rule (commit 9a300f9e) actually works when a fresh producer follows it, not just that the prose reads right. Outcome: a small new eval (distinct from evals/director/scenarios.json's 35 act-classification traces, which test a different layer -- classifying an incoming message, not closing accepted work) exercises the closing rule specifically: at least two scenarios where a fresh producer, given only director/SKILL.md and a short situation, correctly closes an ordinary delivered result without asking, and at least two where it correctly still asks/waits because the fork is a genuine taste call, an undecided trade-off, or a change to the definition of correct (rule 12/27). TEST_MATRIX.md gains a row tracing q-810's rule to this real eval, the same pattern q-163's M-620 row used for test-author's wiring. Dimensions: method reliability (this is the acceptance mechanism itself), documentation (a new eval file + matrix row). Known: the existing evals/director harness's own README explains why classification is checked by scenario+grader rather than skill-text search -- the same discipline applies here: a producer that can see the expected verdict is not being tested. Unknown: exact scenario wording that cleanly forces one of the two outcomes without ambiguity. Risk: none, additive only, reversible. Specialist: opus-tier worker (judgment: designing scenarios that actually isolate the rule, not mechanical). Evidence: the new eval's own pass/fail transcript (real fresh-producer runs, not a self-report), full suite green after the matrix row lands. Next: dispatch worker with commit 9a300f9e's diff and PLAN.md q-810's own body as primary source.
