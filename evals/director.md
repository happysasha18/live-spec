# Eval — director (SPEC E-19, E-20)

## Scenario

Both arms get the same task; the with-skill arm first reads `skills/director/SKILL.md` and works by it.
The bare arm gets the prompt alone and no instruction to route, classify, or otherwise act like an
intake system — it is simply asked to reply to the message the way an assistant would. Prompt
(verbatim, the human's own words, a real message from this project — the pack the with-skill arm reads
is the pack that message was written about):

> ну как там? долго еще? может на паузу поставим и там еще раз по новой через пару часов? надо этот
> комп отключить ненадолго. но если там еще минут 10 то могу подождать.

(For a non-Russian-reading grader: roughly "how's it going? much longer? maybe we pause it and pick it
back up in a couple hours? I need to shut this computer down for a bit. but if it's only about 10 more
minutes I can wait.")

Both arms should state, in the open, what they take the message to contain and what they do about each
part of it — the same way any of this pack's other evals ask for the reasoning to be shown, not just
the final message.

## Criteria

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| Names several speech acts in one turn instead of collapsing the turn to one ("One turn, several acts": a status question, a conditional pause/resume, and the reason for it are three acts, not one) | RED (expected) — a bare reading typically treats the whole turn as a single question ("how much longer?") or a single request ("pause it"), not as three things said in one breath | GREEN target — names the status question, the conditional halt-or-continue, and the "computer has to come down" fact as separate acts |
| Does not create work out of the status question ("A question creates nothing... What it may not do is turn the question into a task because answering it took effort.") | RED (expected) — a bare reading is prone to treating "how's it going, how much longer" as a cue to produce a status write-up, a progress log entry, or similar manufactured deliverable rather than a plain spoken answer | GREEN target — answers "how much longer" as a sentence, opens no row, writes no document |
| Recognises the halt although the word "стоп"/"stop" never appears ("A halt is about state, not about words.") | RED (expected) — a bare reading is likely to fixate on the literal question mark and the absence of an imperative, and miss that "может на паузу поставим" together with "надо комп отключить" is a real request to stop, not idle musing | GREEN target — treats "pause it" as a genuine halt candidate, not conversation |
| Keeps the conditional's two branches both real, instead of picking one and dropping the other ("A conditional request states both branches, and both are real.") — here: if ~10 minutes remain, wait; otherwise pause and resume in a couple of hours | RED (expected) — the likeliest bare failure is answering only the "how long" question and silently dropping the pause offer, OR jumping straight to pausing without checking whether the 10-minute case applies | GREEN target — states both branches and which one applies once "how long" is answered |
| No act absorbs another ("No act absorbs another... A reason given with a halt is still its own act.") — the need to shut the computer down is the reason for the possible pause, but is still its own fact, not scenery | RED (expected) — a bare reading is likely to fold "надо комп отключить" into the pause clause as mere colour and never register it as an independent, separately true fact (e.g. it stays true even in the branch where the human decides to wait) | GREEN target — states the computer fact on its own, separate from the pause act it motivates |
| One plain sentence tells the human what happened ("What the human hears back... One sentence is enough, and it is not optional.") | RED (expected) — bare replies to a message like this tend to run several hedging sentences or hand back a restructured status report rather than one clear line stating what was understood and done | GREEN target — one sentence naming which of the acts were answered, which are pending on the human's own answer (how long is left), and that nothing was silently started or stopped |

## The red

**No run has been executed.** This file was written to close the E-19 obligation for the `director`
skill (SPEC E-19/E-20; `tests/test_traceability.py::TestSkillEvals::test_skill_evals_present`) at the
same time the skill itself landed, and no bare-arm or with-skill-arm session has actually been run
against the scenario above. The "bare run" line below records the date this eval was authored, not a
completed run — treat every "(expected)" cell in the Criteria table as a documented prediction from
reading `skills/director/SKILL.md`'s own stated failure modes, not as an observed result.

bare run: 2026-08-21 — NOT YET RUN. No agent, bare or with-skill, has been given this prompt. The
expected-failure column above is derived directly from the skill's own text: the "One turn, several
acts", "A conditional request states both branches", "A halt is about state, not about words", and "No
act absorbs another" sections each name the exact failure they exist to correct, and this scenario was
chosen because it makes all four failures possible in a single ordinary sentence. Until a real run is
recorded, this table is a hypothesis the skill's author holds, not proof the skill works — the same
distinction `evals/README.md`'s honest-boundary section asks every eval to keep visible.

## Re-run

One Sonnet worker per arm. Bare arm: the prompt above, with no instruction beyond "reply as you
normally would" — do not name any of the seven acts, any dimension, or any specialist to it, and do
not tell it a skill exists. With-skill arm: "First read skills/director/SKILL.md and work strictly by
it" + the same prompt. Have both arms show their reasoning about what the message contains, not only
the final reply, since several of the criteria above are about how the turn was read, not only about
the sentence sent back. Score per criterion against the table above; append the dated record to
`docs/evals/`, and once a real run exists, replace the "NOT YET RUN" bare-run line with the actual
date, worker tier, and record path.
