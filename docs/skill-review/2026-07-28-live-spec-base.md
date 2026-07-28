# Skill review — live-spec-base (the worker-restore sub-rule under rule 7)

`SKILL-REVIEW`

Skill: live-spec-base
Date: 2026-07-28
Reviewer: skill-creator (Anthropic)

Verdict: passes with findings, folded — the review wrote its records and left the skill files
alone; the findings it handed back were folded into the rulebook on 2026-07-28. The findings on the
missing carve-out, the queue-row anchor, the ageing closing sentences and the description's load
trigger are folded; the finding on placement is reviewed with a reason and stands as it is. On the
check this review was asked for: the clause carries its whole elaboration inside this file, which
departs from the shape this file sets for itself, and the departure is deliberate and armed by a
test. F1's sentence now says so in the file's own opening.

## What changed

Rule 7, the concurrent-edit fence, gained a sub-bullet after brief-time disjointness, at
`skills/live-spec-base/SKILL.md:107` (`:104` before F1's sentence landed): a worker holds a file's bytes before it mutates the file,
writes those bytes back, runs none of the discarding git commands, and halts when it holds no
saved bytes; the orchestrator restores from the last committed stage, re-briefs, records the halt,
and commits a finished build stage before the next worker touches its files. The clause names
`guardrails/check-worker-restore.py` as the machine that reads it. The body's numbered rules stay
at thirty-four, since the clause landed as a sub-bullet of a rule that already exists.

## A wording lock governs what a finding may propose

`tests/test_worker_restore.py` holds the clause's sentences word for word across the homes it
names — this rulebook, `skills/build-pipeline/SKILL.md`, that skill's
`references/delegation-protocol.md`, `templates/agent.template.md` and `scripts/open-lane.sh` — so
a home that states the rule in words of its own reds the suite (SPEC INV-299). Every proposal
below leaves those sentences untouched. What it moves is the framing this file carries alone: the
anchor in the lead-in, the closing sentences no other home holds, and the frontmatter.

## The check this review was asked for: does the clause state its rule once?

It does not, in the sense this file's own opening uses. The opening says a working skill
references these rules and elaborates only its own domain, and that a second full statement of a
shared rule inside a working skill is drift, a defect to fold at the next milestone (SPEC INV-13).
The worker-restore clause is the shape that law describes: the rulebook carries the command list,
the blast-radius reason, the worktree scope, the halt walk and the orchestrator's recovery, and
`skills/build-pipeline/SKILL.md` and `references/delegation-protocol.md` carry the same paragraph
again, word for word.

The departure earns itself. A rule that lives in a skill file reaches a worker only when the
worker loads that skill, and a worker is briefed from whichever home its orchestrator was reading;
a brief that named fewer commands than the gate reds on is the event the rule was written after.
So the clause rides every brief-shaped surface verbatim, and `tests/test_worker_restore.py` reds a
home that drifts to its own words.

What this file lacked was the sentence that says so: a reader who applied INV-13 to the pack would
have folded the duplicate and red the suite. F1's carve-out now stands in the opening paragraph,
beside the drift law.

The clause is also the longest item in its own list by a wide margin. Its neighbours — the
lane-open act, worktree isolation on overlap, brief-time disjointness, one row per landing commit,
a prior-context worker, the stable session identity — each state a rule in a sentence or two and
leave the walk to a working skill. The clause runs the length of all of them together. The locked
sentences account for most of that and cannot move; the sentences that could move were F3's, and
they are gone.

## Findings

**F1 — folded. The file stated the no-duplicate law and carried a deliberate duplicate with
no carve-out.** A reader who folds it reds `tests/test_worker_restore.py`. The sentence folded in,
standing in the opening paragraph beside the drift law (`skills/live-spec-base/SKILL.md:15`): "One rule is carried whole by
every skill that briefs a worker: the worker-restore sub-rule under rule 7 rides each brief in one
wording, and `tests/test_worker_restore.py` reds a home that states it in words of its own (SPEC
INV-299)."

**F2 — folded. The clause anchored on a queue row.** The lead-in at
`skills/live-spec-base/SKILL.md:104` read "(ROADMAP row 479)"; the rule's home in the spec is
INV-298 and its machine is INV-299, and `ARCHITECTURE.md:50` already pins this very line as
INV-298. Every neighbouring sub-bullet in rule 7 anchors on a SPEC code. A queue row is archived
when it closes, so the reader who follows row 479 next month lands in a rotated file. The wording
folded into the lead-in: "(SPEC INV-298)". The same finding stood against the same lead-in in
`skills/build-pipeline/SKILL.md:341` and `:538` and in `references/delegation-protocol.md:49`, and
is recorded in `docs/skill-review/2026-07-28-build-pipeline.md`, finding F2.

**F3 — folded. The clause closed on sentences that belong elsewhere, and one of them was
already out of date.** The first, "Brief-time disjointness above fences EDITS and cannot reach
this act…", argues the clause against the sub-bullet directly above it; the same argument stands
at `skills/build-pipeline/references/delegation-protocol.md:65`, which is where a reader who wants
the reasoning goes. The second, "Mutating a shipped artifact to prove a row red is the pack's own
red-first method, so this act recurs in every parallel session until the clause rides every
brief", states a condition that ended when this delivery landed: the clause now rides
`templates/agent.template.md` and the stub that `scripts/open-lane.sh` prints. A rulebook that
narrates a roll-out ages against itself. Folded: both sentences are cut and the sub-bullet ends at
the gate sentence, the delegation protocol keeping the reasoning at
`skills/build-pipeline/references/delegation-protocol.md:65`. The proposal also offered to keep one
clause of the first sentence; the owner's fold took the whole cut, since that clause re-argues the
sub-bullet above it as well. The rulebook loses no rule and the sub-bullet comes back within reach
of its neighbours.

**F4 — reviewed, no change. The clause sits under the right rule.** Rule 7 governs the fence a
session holds before every write and every commit, and its sub-bullets are the parallel-lanes
rules underneath it. A discarding command is the act that reaches past a brief's write-set, so it
belongs beside the disjointness rule it defeats. `ARCHITECTURE.md:48` states the same placement
for INV-298. The clause landed as a sub-bullet, so the numbered rules stay at thirty-four and the
description's count stays true.

**F5 — folded. The frontmatter description says when to load this file and when to leave it
alone, and it understated one occasion.** The load triggers read: a pack skill is in use,
resolving how the pack behaves for a human or a host, or two skills seem to state one rule
differently. The leave-alone line reads: sessions outside the pack's work, and host- or
person-specific values. Both still hold for the file as a whole. The new clause reaches further
than the triggers do — it binds a worker in every tree, and the session that most needs it is the
one briefing a worker while carrying no other pack skill, which is the case the rule was written
after. The addition folded into the load list, after "is in use": "…, before a session briefs a
worker that will write files,". The leave-alone line stays as written: a session outside the pack's work
meets this rule through the brief it is handed and through `guardrails/check-worker-restore.py`;
loading the rulebook stays its own occasion.

**F6 — the size finding stays open. The body was 554 lines and now runs 557.** Anthropic's guidance
for a SKILL.md is to stay under 500 lines and to add a layer of hierarchy on approaching that; this
rulebook is past it. Its kind is read by lookup, which softens the cost. Rule 7 no longer reads by
lookup: its sub-bullet list was a scannable ladder of one-sentence rules, and one item still runs a
full screen. F3's cut shortened that item, and F1's carve-out spent three lines in the opening, so
the body grew by three. The remainder is the wording lock's price, paid where the pack chose to pay
it.
