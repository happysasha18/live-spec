# One home per rule — the converging landing, 2026-08-31

SKILL-REVIEW

Skill: live-spec-base
Skill: director
Skill: communicator
Skill: spec-author
Skill: design-reviewer
Skill: feedback-intake
Skill: architect
Skill: test-author
Skill: publish
Skill: feedback-collector

Verdict: PASS — every change is a removal of a second copy or the pointer that replaced it, plus one
new section in the director giving a rule its home. No skill gained a rule; three lost restatements
of rules they do not own.

## What moved, skill by skill

**live-spec-base.** Rule 7's lane law stays where it was and is now the only place it is written.
Rule 27 becomes the one home for what only the person can settle: its three cases are unchanged, and
one sentence was added saying they are the whole set and naming the other faces the retired copies
used (a threshold, a policy, a domain wording, the feel of a real device), so nobody has to write the
list again. Rules 1, 12 and 29 lost their own versions of that list and point at 27 instead. Nothing
was deleted that is not now readable at 27.

**director.** `references/lanes-and-pen.md` was a full second statement of rule 7 whose own opening
line said so ("Every line below reads exactly as it read in the body"), and whose stated inbound
pointer named a section of `SKILL.md` that no longer exists. It now opens by naming rule 7 as the
law's home and keeps only what rule 7 leaves to the seat: the dependency graph and its edges, what
happens to the lanes around a landing, the drafter-applier form, and the re-door's rebuild of the
independence edges. `SKILL.md` gains the paragraph that closes plan-16's last leg — see the recorded
run below.

**communicator.** One example line used a sixth status mark the owner's own legend never allowed;
it now uses one of his five. Its rule 7 stopped drawing the line between what to ask and what to
decide, and points at base rule 27. `references/words.md` cited base rule 18, retired on 2026-08-26,
and now cites 27, which the body actually uses.

**spec-author, design-reviewer, feedback-intake.** Each restated ask-never-guess or the human-only
set in its own words. Each now applies the rule and cites it.

**architect, test-author, publish, feedback-collector** (and spec-author's own header). All six
opened by listing sixteen shared rules by nickname, three of which were retired on 2026-08-26 and
nine of which the base carries and the list omitted. The list is gone; the pointer stays, in the form
`design-reviewer` and `communicator` already used.

## The recorded director run — a rule it had never seen

The last leg of plan-16 asks that the director name the right home for a rule it has never seen. The
sentence that makes this possible is in `skills/director/SKILL.md` under "what does it touch?", and
the five houses with their declared sentences are in `references/request-kind-table.md`. Run against a
rule invented for the run and written nowhere in this tree:

> "A worker's brief always names the branch its work rides, and a brief that names none is refused
> at the door."

Walking the five declared sentences: it is not a law of the product, so not the spec. It fires
whenever a worker is briefed, which is every job that delegates rather than one skill's own job, so
not a skill. It is not a value that varies by person or repository, so not a profile. It is a way of
working every skill obeys — the base rulebook — and its teeth, the refusal at the door, belong to a
gate that enforces what the base states. Home named: the base rulebook, with a gate holding the
teeth. One house, arrived at by reading the five sentences and nothing else.

Second run, on a rule that pins to two, to check the finding fires:

> "A status report is ten lines, and a report about the photo site is seven."

The first half is a way of working; the second half is true of one repository. Two houses, so the
verdict is the finding the paragraph names: this is two rules wearing one sentence, and it is said as
that rather than filed in whichever house looked closer.

## The check

`tests/test_one_home_per_rule.py`. Its reach and its blind spot are written in its own opening. It
was red-proved both ways on 2026-08-31: a second copy of all three rules planted into
`skills/architect/SKILL.md` redded all three rules; the same text rewritten as a pointer at the three
homes passed; the plant was then removed. It costs about 0.15 s and reads roughly ninety files once.
