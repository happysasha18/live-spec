# Skill review — build-pipeline (the worker-restore clause and its gate at verify)

`SKILL-REVIEW`

Skill: build-pipeline
Date: 2026-07-28
Reviewer: skill-creator (Anthropic)

Verdict: passes with findings, folded — the review wrote its records and left the skill files
alone; the findings it handed back were folded into the skill on 2026-07-28. The findings on the
figurative sentence, the queue-row anchor, the unsaid window, the neighbouring-tree red, the
empty-root red and the clause's placement are folded, each in the wording the review proposed; the
findings on the deliberate duplication and on the description are reviewed with a reason and stand
as they are. The frontmatter description holds. The clause now stands as its own bullet, and the
body is still past the length where a reader keeps their place, so the size finding stays open.

## What changed

The delegation bullet gained the worker-restore clause: a worker holds a file's bytes before it
mutates the file, writes those bytes back, runs none of the discarding git commands, and halts
when it holds no saved bytes, with the orchestrator owning recovery and committing a finished
build stage before the next worker touches its files (`skills/build-pipeline/SKILL.md:546`, its own
bullet since F6 was folded). The same clause landed in `references/delegation-protocol.md:49`, where
it also carries the incidents behind it. The verify step gained a paragraph naming `guardrails/check-worker-restore.py` and the
moment a session reads its verdict (`skills/build-pipeline/SKILL.md:341`).

## A wording lock governs what a finding may propose

`tests/test_worker_restore.py` holds the clause's sentences word for word across the homes it
names — the rulebook, this skill, the delegation protocol, `templates/agent.template.md` and
`scripts/open-lane.sh` — so a home that states the rule in words of its own reds the suite (SPEC
INV-299). Every proposal below leaves those sentences untouched and moves only the framing around
them: the lead-ins, the anchors, the paragraph the verify step carries, and where the clause sits
on the page. A proposal that changed a locked sentence would have to move every home and the
test's own list in one pass.

## Findings

**F1 — folded. `skills/build-pipeline/SKILL.md:344` described a destruction in figurative
words.** The verify paragraph separated "a worker that put a file back" from "a worker that took a
lane's night away". The pack holds its own texts to plain mechanisms, and the brief this skill
composes states the no-dramatization law to every worker (SPEC INV-221). The sentence also left
the damage unnamed, where the gate names it precisely. The wording folded in, after the
dash: "…which is the one signal that separates a worker that wrote a file's bytes back from a
worker that discarded a lane's uncommitted work — the `git status` both paste afterwards reads
"clean"."

**F2 — folded. The clause anchored on a queue row in three places.** The lead-ins at
`skills/build-pipeline/SKILL.md:341` and `:538`, and at `references/delegation-protocol.md:49`,
each read "(ROADMAP row 479)". The rule's home in the spec is INV-298 and its machine is INV-299;
`ARCHITECTURE.md:50` already pins the rulebook's line as INV-298. A queue row is archived when it
closes, so a reader following row 479 next month lands in a rotated file. The wording folded into
each lead-in: "(SPEC INV-298; the gate INV-299)" — the second one now heads the bullet F6 lifted,
at `skills/build-pipeline/SKILL.md:546`. Row 479 keeps its home in the journal and the queue.

**F3 — folded. The verify step named the command and left its window unsaid.**
`skills/build-pipeline/SKILL.md:341` said to run `python3 guardrails/check-worker-restore.py` with
no flags, and the gate reads the last 24 hours by default
(`guardrails/check-worker-restore.py:90`). A session that ran longer than a day got a green over
a window that never reached its worker. The sentence folded in, after the command: "The gate reads the
last 24 hours; a session whose worker ran earlier than that passes `--since-hours` wide enough to
cover the run it is accepting."

**F4 — folded. A red naming another project's run had no instruction, and the sentence that
stood there pointed at an act base rule 7 refuses.** The gate reads the harness transcript root
whole, so its findings can name a worker from a neighbouring tree — which is the case the rule was
written from. `skills/build-pipeline/SKILL.md:345` then said the session recovers the named files
from the last committed stage, and a repo the session was not assigned to is read-only. The
wording folded in, replacing that sentence: "A red names the run, the command and the paths. Where the run is
this project's, the session recovers the named files from the last committed stage before anything
else, and the worker's result waits on that. Where the paths belong to another project's tree, the
session writes what it read into that project's intake folder and touches no file there, since a
repo it was not assigned to stays read-only (base rule 7)."

**F5 — folded. An empty transcript root reds, and the paragraph gave that red no reading.**
The gate reds by name when the root exists and holds no worker run, since a clean verdict over
zero runs would protect nothing
(`tests/test_worker_restore.py::test_a_root_holding_no_worker_run_reds_by_name`). The paragraph at
`skills/build-pipeline/SKILL.md:341` described only the discarding-command red, so a session
meeting the empty red read it as a destruction. The sentence folded in, beside the stand-down
sentence: "A red naming an empty transcript root says the layout the gate reads has moved: no
worker discarded anything, and the gate's reach is what the session repairs."

**F6 — folded. The clause sat inside another bullet and buried the duty that resumes after
it.** The "Junior delegation" bullet ran from `skills/build-pipeline/SKILL.md:524` to `:560`:
routing, the brief's birth laws, the worker contract, cleanup safety, the restore clause, then
"Every delegation reports its saving in the row's delivery report" resuming mid-line at `:555`,
where it read as a further sentence of the restore clause. Two sentences five lines apart also
opened on the same words, at `:533` and `:538` ("And the brief carries the…"). Folded: the
clause stands as its own bullet under the same list, at `skills/build-pipeline/SKILL.md:546`,
headed "**A worker never restores a working tree with a git command (SPEC INV-298; the gate
INV-299).**" — F2's anchor form for this file — and placed after the junior-delegation bullet. The
locked sentences moved whole, the delegation bullet keeps its own closing duties beside its pointer
at `references/delegation-protocol.md`, and the repeated opening went with the move. The new
bullet's own opening states that every brief this skill composes carries the clause verbatim, which
is what the lead-in it replaced said.

**F7 — reviewed, with the reason stated. The clause stands in full in the body and again in the
reference by design.** Inside one skill that reads as the duplication the pack folds at the next
milestone (SPEC INV-13), and a future editor would fold it and red `tests/test_worker_restore.py`.
The reason it stands: a worker learns its contract from whichever home its brief was written from,
and a brief that named fewer commands than the gate reds on is what the rule was built after. The
carve-out sentence belongs in the rulebook, where the drift law is stated; it is proposed in
`docs/skill-review/2026-07-28-live-spec-base.md`, finding F1.

**F8 — reviewed, no change. The frontmatter description still says when to load this skill and
when to leave it alone.** It names the occasions — a new feature, a new stateful surface, a
behaviour change, a bug, a refactor, a docs-only change, a removal — and it names the occasions
that route elsewhere, a tiny reversible edit and pure research. The restore clause fires inside
the delegation step of a run this skill is already carrying, so it asks the description for no new
trigger. One path stays uncovered by this skill's description and is covered by other means: a
session that takes the tiny-edit shortcut and still spawns a worker never loads this file, and
reaches the clause through `live-spec-base`, through `templates/agent.template.md`, and through
the gate reading its transcripts afterwards.

**F9 — folded in part; the size finding stays open. The body was 576 lines and now runs 578.**
Anthropic's guidance for a
SKILL.md is to stay under 500 and to add a layer of hierarchy when a body approaches it; this one
is past that line and grew by 28 lines in this delivery. A reader walking the pipeline steps stops
at the delegation bullet: it is one bullet of 37 lines carrying routing, the brief's birth laws,
the worker contract, cleanup safety and the restore clause, and the restore clause is now the
longest of them. F6 buys back the bullet's shape. The body's own remedy for size is the reference
directory it already uses, and the clause is the one paragraph that cannot move there, since the
wording lock names this file as a home. What shrank instead: the cleanup-safety sentences at
`:534`–`:538` restated base rule 17 and SPEC INV-162 at full length inside this body, where the
same bullet's other duties cite their rule and move on. They now state the rule and its anchor in
one sentence, at `:539`–`:541`. The verify paragraph's four new sentences (F3, F4, F5) spend more
than that compression returns, so the body stands at 578 lines and the size finding stays open for
the owner.
