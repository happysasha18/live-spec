# A README replacement, audited twice — the draft is beside this note

**From:** the promoter, live-spec campaign window (`~/promoter-alexander-live-spec`)
**Date:** 2026-07-27
**Born of:** Alexander's word this evening — take the strongest material out of the public page the
promoter wrote today, fold it into the README so the result is no worse than what ships now, stop
repeating the platform's name, audit it, and hand it over.
**The draft:** `inbox/2026-07-27-from-promoter-README-draft.md`, beside this note. It is a full
replacement for `README.md`.

## What it is

The shipped README's structure, section order, voice, and every one of its links are kept. Nothing was
dropped: a coverage pass compared the two files sentence by sentence, and the install path is byte for
byte the same. Three things came in from the page, and several claims were corrected against the code.

**It opens on the 17 July catch instead of a hypothetical.** Six cold readers read the public page
today, each an early-stage founder with no context, none of whom saw an earlier draft. Every one of them
was convinced by the same thing, and it was the recorded failure. The shipped README opens on an
invented date-filter example; the draft opens on what actually happened and keeps the date-filter
example as the second paragraph, where it explains the shape rather than carrying the weight.

**It states what the four host scripts actually read, and what they cannot see.** This is the finding
already sent this afternoon in `2026-07-27-from-promoter-readme-overstates-guardrail-reach.md`. The
draft is the promoter's proposal for how to say it: each script named by what it opens, then a paragraph
naming what walks past all four — a changed calculation, a new sort order, an altered edge, a new API
field. The boundary sentence from `scaffold/guardrails/README.md` is quoted as the source.

**It carries the rules ladder as the answer to the obvious objection.** A reader who is told that most
of the discipline is a model following written text asks what stops the model. The draft answers with
the two-strike rule and the problem ledger's three rungs, and the timestamp case as the worked example.

## What the audit changed, and why this note is long

An adversarial pass read the first draft against the code, briefed to refute rather than confirm. It
returned sixteen findings, six of them falsifiable by a stranger in minutes. A second pass over the
corrected draft returned two new errors that the first correction had introduced, three residual
overstatements, and four places where the draft conceded more than the code owes. All are folded. The
things worth knowing, because several of them are facts about the product rather than about the text:

1. **The promoter's own page had claimed an agent rewrote its own tests to pass.** No record says that.
   What the records say: a background race destroyed every verdict the judge wrote, and a missing
   installed hook counted as a green skip. That claim is out of the page and was never in the README.
2. **The reviews on 17 July ran in the same session that did the work.** The draft says so, and says the
   clean-context rule was written the next day because of it.
3. **A release review from a clean seat is a discipline with no gate.** The rule hedges exactly where a
   first draft did not: whether a context was truly clean is a process fact no script sees, and the gate
   under it checks only that a record exists, is dated to the release, and names a different seat. The
   draft says that plainly, which suits a README whose own thesis is that only scripts are independent.
4. **Twenty-five of the twenty-six gates on the hook carry their own red proof.** The twenty-sixth is
   declared as riding another gate's suite. The draft says twenty-five and names the exception.
5. **A host gets no CI mirror and no hook wiring.** The installer prints four lines and leaves
   `.git/hooks` alone; the linked workflow is this repository's own. The shipped README's phrasing lets
   a reader conclude otherwise. The draft states the manual step and lists the real prerequisites,
   including the resolvable base branch that `check_tests_present.py` needs.
6. **The skill count contradicted itself.** The shipped README's opening line says ten and its skills
   paragraph lists eleven names. The draft says ten skills over one shared rulebook, which is what the
   rulebook itself says.
7. **The 10 July probe was against this repository**, and two of the three planted breaks were blocked
   at the push. The draft says both, because the blocks make the miss land harder.

Four things the draft now claims that the shipped README leaves on the table: the meta-gate refusing a
gate declared unable to fail, in its own words; the pre-commit chain, which is a second hook's worth of
teeth and appears nowhere on the current page; the three-way promotion test behind the declined gate;
and the two blocked breaks in the probe.

## What was yours to decide — answered 2026-07-27, swept 2026-07-28

- **Whether to take it at all.** You took it. `README.md` now carries the draft's own sentences, among
  them the builder passage and the printed-defaults line.
- **The project count.** Answered at ~18:11 on 2026-07-27 and recorded in `DECISIONS.md`: three
  projects, the pack's own repository being the third. `README.md` says three today.
- **The version line.** The draft does not touch `VERSION`.

## What is closed

Three lints pass on the draft (register, scissors, structure). No link lost. The platform's name appears
once. Word count 1,682 → about 2,550, and every added paragraph is a dated, checkable fact or a stated
limit, which is the shipped README's own habit.

Nothing is owed back to the promoter window. The public page ships either way.
