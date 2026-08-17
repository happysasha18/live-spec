# `SKILL-REVIEW` — communicator, the tool-boundary arm's retirement

Skill: communicator. Date: 2026-08-17. Range: f9eaecc..HEAD.

Commits of the range touching `skills/communicator/`:

    49f26a7 Retire the tool-boundary chat arm: it could not prove whose work it stopped

Verdict: ALLOW. Two sentences change, both in one direction: a promise of machinery that no longer
exists comes out, and what now holds the rule is named.

## What changed

`skills/communicator/SKILL.md`, the measurement bullet under the chat face, had said:

> The chat floor is mechanical: the measurement arm of `hooks/midturn-chat-scan.py` denies the next
> tool call on a count whose method stands nowhere in its paragraph.

It now says that no machine holds this rule in chat, that the scan which did was retired, and that a
person holds it. `references/writing-register.md` carried the same promise under rule 17 and takes the
same correction, with the added sentence that all four parts of a number now rest where the other three
already did.

## Read for what a removal can break here

The rule itself is untouched. A number still carries four things, the writing register is still its
home, and rule 17 still states it — the edit reaches only the sentence that named the catcher. No
procedure changes, no step is dropped from any walk, and no path is named that does not exist.

The risk a removal carries in a skill body is the opposite of an addition's: a reader who relied on the
machine now has nothing telling them the rule is theirs to hold. That is why both files say so in words
rather than falling silent — a bullet that simply lost its last sentence would have read as a rule with
no consequence.

Length and register: both edits stay inside the prose cap, and `check-doc-findings-bound.py` reads 129
live documents with none above its record after them. `check-shipped-language.sh` passes with zero
offences.

## The net

The four tests that held this law's written homes were deleted with the retired arm's own test file,
and the retirement's second review named that as a blocking over-deletion. They stand again at
`tests/test_measurement_law_homes.py`, which now also carries `test_the_communicator_body_names_no_machine_for_the_rule`
— an assertion that neither of these two files promises a scan again. That test is what keeps this
review's verdict true after today.

Reviewer: an independent adversarial reviewer read the whole retirement three times and refused it
twice; its findings and their closures are recorded in `docs/prover/2026-08-17-midturn-arm-refusal.md`.
The over-deletion above is finding 10 of that record's second pass. This skill's own two sentences were
read by this session against the record's findings.
