# Skill review — build-pipeline after the acceptance moved into CI

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-07
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/SKILL.md`, read by a fresh
agent holding no context from the edit it judged.

Verdict: valid with nine defects, all folded — the same three facts stated in full in both
documents, one ceiling stated twice inside one file, one banned contrast heading, two sentences
about the CI leg that were false, a refusal named for half its condition, and two things a session
holding only the body could not do.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

Run against the documents' final state, after the folds below.

## What the change was

The acceptance command became a condition of admission with its digest anchored on the checkpoint;
the pre-spawn guard moved from reading a row id to requiring a spawn token the brief cuts; and the
acceptance that decides moved to a CI re-run at the pushed commit, with the board's workflow
publishing only behind it.

## The findings, and what was done

1. **Two homes, three times again.** Each of the three mechanisms was written out in full in both
   the body and the reference. The body keeps the mechanic and the commands, because a session
   holding only that page has to run them; the reference keeps the incident each one answers, the
   shared `pre_spawn_check` leg, and the ceilings.

2. **A ceiling stated twice inside one file.** The reference said the guard reads the board and
   never the worker's conduct in two paragraphs. One of them is gone.

3. **A banned frame.** The reference's heading read "A passing acceptance comes from a run, not
   from a text" — the "X, not Y" shape this pack forbids. It now says what it is.

4. **Two sentences false about the CI leg.** "Runs every done row's own recorded command" was
   false — the re-run skips a row with no key and one whose key reads the machine. And "publishes
   only behind a green gates run" was false while `workflow_dispatch` could publish with no gates
   verdict at all; that trigger has since been removed, and the sentence now says what the code
   does.

5. **A refusal named for half its condition.** The body said a key reading `$HOME` is refused;
   `reads_outside_the_tree` refuses `$HOME` or `~/`, so a session acting on the body alone would
   write a `~/` key and be refused without knowing why.

6. **Two things a body-only session could not do.** The route file's field names appeared nowhere
   in the tree, so `admit --route <route.json>` could not be run from the documents; the reference
   now carries the route as a fenced example. And `hold`'s signature lived only in the reference
   while the guard's own denial tells the session to run it; it is now beside `brief` in the body.

Also folded, from the adversarial read of the same change: the token is not single-use and both
documents said it was, and every anchor here is a line in a checkpoint a hand can write, which the
documents had stated as an impossibility. Both now say what holds and what does not.
