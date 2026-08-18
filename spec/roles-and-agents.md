## Requirement 2: The pipeline runs as a set of roles carried by the working skills

**Context:** Behind the pipeline is a full set of roles. An analyst writes the spec, an architect stress-tests the design and finds the edge cases and dead ends before any code is written, a design reviewer judges the design and checks that same-kind things behave alike, a tester works out the tests and writes them, and a project manager runs the process and reports back to the person. The design reviewer proposes the groupings of same-kind things the spec never declared and checks behaviour parity inside each group. These roles are the working skills, and one base skill holds the shared rulebook and the default settings the other skills work by.

**User Story:** As a person relying on the pipeline, I want each request run by a full set of roles carried by named working skills over one base rulebook, so that every request meets an analyst, an architect, a reviewer, a tester, and a manager, five distinct roles in one pass.

### Acceptance Criteria

**Case: the roles are the working skills**

1. The system *shall* run each request through a set of roles — an analyst who writes the spec, an architect who finds the edge cases and dead ends before any code, a design reviewer who checks that same-kind things behave alike by proposing the groupings the spec never declared and checking behaviour parity inside each group, a tester who works out and writes the tests, and a project manager who runs the process and reports back. [E-12]
2. The system *shall* carry those roles as the working skills, bringing the person in where an answer needs a fact no artifact holds — a taste, a policy, or an act irreversible outside git. [E-12, INV-17]
3. The system *shall* hold the shared rulebook and the default settings the working skills run by in one base skill. [E-12]

---

## Requirement 51: Each step is worked with its craft's standards

**Context:** A single generalist working the whole pipeline produces generalist artifacts. Each step therefore names the profession the agent works it as, and each artifact is judged by that craft's standards. The craft, like the step's form, follows the kind.

**User Story:** As a person relying on each artifact, I want each step worked with its own craft's standards, so that a spec reads like a product manager's and a test matrix like a quality-assurance engineer's rather than one generalist's notes.

### Acceptance Criteria

**Case: each step names its craft**

1. The system *shall* work the spec as a strong product manager, the architecture as a software architect, the test matrix and tests as a quality-assurance automation engineer, the code as a senior developer, the two prove steps as the prover's formal-reviewer role, commit-and-show as a careful release engineer, and the verify walk as the visitor's own outside eyes. [INV-33, E-12]
2. The system *shall* judge each artifact by its craft's standards and speak the delivery report's step accounting in them. [INV-33]

**Case: the craft follows the kind**

3. The system *shall* let the wish's kind say what each craft's standards look like in its medium, working the code step as a strong writer on a prose product and as a tool builder on infra. [INV-33, INV-22, INV-30]

---

## Requirement 189: An agent and a skill are told apart by what outlives a conversation

**Context:** Several agents work on one person's projects, and the moment they can talk to each other they can generate noise. The layer that governs them opens by telling an agent from a skill, since only an agent holds standing work of its own that another agent can address. An agent is a project window with a tree, a queue, gates, contracts, a standing mission, and a card; a skill is a capability a window loads for one conversation.

**User Story:** As a person running several agents on one machine, I want an agent and a skill told apart by what outlives a conversation, so that only the trees holding standing work are addressed as agents.

### Acceptance Criteria

**Case: what an agent carries**

1. *when* a tree carries its own spec, queue, gates, published contracts, standing mission, and agent card, the system *shall* treat that tree as an agent, each of those outliving any one conversation. [E-31]
2. one window *shall* serve one agent, the same rule the engine-and-instance pair already holds for its two repos. [E-31, INV-86]

**Case: what a skill carries**

3. *when* a capability loads into a window, holds no tree, no standing mission, and no queue, and leaves nothing standing once the conversation closes, the system *shall* treat that capability as a skill. [E-31]

**Case: the line between the two**

4. the system *shall* count a capability as an agent *when* it holds durable state, a standing mission, and a zone of its own, and *shall* count a capability that lives wholly inside one session as a skill. [INV-182]
5. *when* a real capability sits on the line between the two, the owner's word *shall* place it. [INV-182, T-22]

---

## Requirement 190: Two channels carry everything between agents, and the traffic's kind picks the transport

**Context:** A message between two agents travels two roads and no more. One is the receiver's inbox, which carries a one-shot request to change something; the other is a published contract, a versioned read the reader takes on its own clock. Which road a given message takes is decided by whether it needs a timely answer, while who may talk and when stays the same on either road.

**User Story:** As a person whose agents pass work between them, I want exactly two channels to carry everything between two agents, so that no third improvised road grows to carry the traffic the two were meant to hold.

### Acceptance Criteria

**Case: the two channels**

1. the receiver's inbox *shall* carry a one-shot request to change something, one new file per item. [INV-183, E-11]
2. a published contract *shall* carry a recurring read, versioned, taken on the reader's own clock. [INV-183, E-33]
3. a reply *shall* ride the inbox in the other direction, so the count of channels between two agents stays at two. [INV-183, INV-192]

**Case: the traffic's kind picks the transport**

4. *when* a message needs no answer within a deadline, the system *shall* send it by the store. [INV-236, E-11, T-10, INV-112]
   - such a message is a durable record read on the neighbour's own clock, or a notification;
   - the file is reachable while the receiver is not running;
   - *when* the sender is remote, the file is committed and pushed.
5. *when* a message is a back-and-forth needing a live peer that answers in turn, the router (`guardrails/route_agent_transport.py`) *shall* route it to the direct channel. [INV-236]
6. *while* the harness has shipped no listener, the direct channel *shall* stand unavailable, and the router *shall* name the listener it waits on. [INV-236, INV-231]

**Case: the store road's watcher**

7. *when* a receiver arms a one-shot check that reads a deposit on the receiver's own rhythm, whenever it next runs, the system *shall* treat that check as the store road's watcher. [INV-236, INV-231, INV-129]

**Case: the contract holds across transports**

8. whichever transport carries a message, the system *shall* leave the two-channel contract untouched, so who talks and when stays as it stands. [INV-236, INV-183]

---

## Requirement 191: Every reference to an internal item carries its code and a plain description

**Context:** The method names its internal items with short codes, and a code alone tells a person nothing. So every reference to a named item carries a pair — the item's stable code beside a plain one-sentence description of what it does and the problem it solves. The pair travels in a cross-agent message and in a report a human reads alike, and each description lives where its code is written — the criterion the code trails, and the glossary for an entity code's definition.

**User Story:** As a reader of a report or a cross-agent message, I want every internal code carried beside a plain one-sentence description, so that a bare code never stands alone before me and a second agent reasons in the same terms.

### Acceptance Criteria

**Case: the pair travels together**

1. *when* a reference names an internal item the method carries a code for, the system *shall* carry the item's stable code beside a plain one-sentence description pinned to the item at its owning surface. [E-35, INV-239, E-4]
2. the system *shall* carry that pair in a message across the agent channel and in a human-facing report alike. [INV-239, INV-183]
3. within one report, the system *shall* carry the full pair on a code's first mention and the code alone on each later mention of that code. [INV-239, INV-28, INV-31]

**Case: one home for the description**

4. the system *shall* keep each code's plain statement in its authored home — the criterion the code trails carries the code's rule, and an entity code's definition lives in the glossary — written once and read by every reference, the generated code-to-location table carrying locations only. [INV-239, INV-271]
5. the system *shall* back-describe the whole existing code set in one pass at a major release carrying one MIGRATION.md chapter. [INV-239, INV-217]
6. *when* the project runs in another language, the system *shall* translate the English description in real time and translate it consistently, so one item reads under one translation across a session. [INV-239, INV-83]

**Case: the description's presence is checked, its quality sampled**

7. *when* the migration to the requirements format lands, the dedicated description-field gate *shall* retire with the criteria and the glossary as its stated successor, the requirement-shape gate thereafter holding that every code trails a criterion carrying its rule. [INV-239, INV-271]
8. for a code deposited on the agent channel with no description beside it, the reviewer's review *shall* stand as the net. [INV-239, INV-189, INV-150]
   - the reviewer role's review is the enforcement until the named gate ships;
   - the law declares the mechanism as the deposit-time lint over each `from-<agent>` inbox file.
9. a human *shall* sample descriptions against the quality bar at the migration's authoring and each periodic audit, and *shall* accept each that reads as clear. A description below the bar *shall* become a queue row. [INV-239, INV-41, INV-145]
   - the periodic audit's own count defaults to every ten deliveries, the host setting its own count in its profile.

**Case: the quality bar a description is written to**

10. a description *shall* say what the item does and the problem it solves, *shall* show the whole class *when* the rule governs a class, *shall* name its key term in plain words, and *shall* use the accurate actor and object. [INV-239, INV-153, INV-83]

---

## Requirement 192: A description a reader could not follow is rewritten by the agent that owns the item

**Context:** A description can be clear to its author and still leave a reader asking what one of its terms means. That re-asked question is the signal the description did not land. The agent that owns the item rewrites the description, and it does so on its next turn writing that item's home document rather than in the middle of another turn.

**User Story:** As a reader who re-asks what a term means, I want the description rewritten by the agent that owns the item, so that each description earns its clarity from real use each time it is re-asked.

### Acceptance Criteria

**Case: the re-asked question is the signal**

1. *when* a human re-asks what a term a reference carries means, the system *shall* read that question as a signal the description did not land. [INV-240, INV-83]

**Case: the owning agent writes the rewrite**

2. the system *shall* let only the window that owns the item write that item's description, its one home being the item's owning surface. [INV-240, INV-10]
3. *when* the confusion lands in the owning window, the owning agent *shall* reformulate the description to answer the question just asked and overwrite it in its one home on its next turn writing that document. [INV-240]
4. *when* the confusion lands at a window that does not own the item, that window *shall* carry the confusion to the owning agent as a lived-fault earned message, and the owning agent *shall* rewrite the description on its next turn writing that document. [INV-240, INV-189]

**Case: the rewrite waits for a written turn**

5. whichever window the confusion arrived at, the system *shall* record the re-question and defer the rewrite to the owning agent's next turn writing the document, holding clear of a rewrite in the middle of another turn. [INV-240, INV-39]
6. the deferred rewrite *shall* take the description's home document under its own pen and *shall* ride as a named intended change to the identity check the restructure procedure runs — word-token and punctuation multisets unchanged except the named changes — which expects it as a matched token. [INV-240, INV-198, INV-111]

**Case: the rewrite meets the same bar**

7. the rewrite *shall* obey the quality bar every description obeys, sampled against a real reference by the human sampling net, with the presence gate beneath it. [INV-240, INV-41]

---

## Requirement 196: A misdirected question is referred back, and no refer-and-resend loop runs on

**Context:** A question can land on an agent that does not own it. The answer is a referral: the question lives in another agent's zone, so it goes back to whoever asked. Every message carries an identifier and a stated need-by and reaches a terminal state, and one question crosses between the same two agents at most twice before the third crossing goes to the owner.

**User Story:** As an agent handed a question from another agent's zone, I want to refer it back to whoever asked and let no refer-and-resend loop run on, so that a misdirected question reaches its owner without manufacturing traffic.

### Acceptance Criteria

**Case: a referral returns to whoever asked**

1. *when* a question belongs to another agent's zone, the system *shall* refer it back to whoever asked, and the zone's owner *shall* receive nothing from a referral. [INV-190]
2. *when* a human asks, the system *shall* answer in chat that the answer is the other agent's and to ask that agent, sending nothing. [INV-190]
3. *when* an agent asks, the system *shall* answer along the reply road as the message's terminal state, declined and naming the zone that owns the question. [INV-190, INV-192]

**Case: a question dropped for want of a home**

4. *when* a question pins to no artifact and no work of the sender's stands on it, the system *shall* drop it, the holding of it being the finding. [INV-191, INV-153]

**Case: a concern no zone owns**

5. *when* a concern is real work whose owning zone does not exist yet, the system *shall* carry it to the pack's inbox. Sweeping that inbox, the pack repo's assigned session *shall* answer who owns it. [INV-197, T-22, INV-182, INV-97, T-10]
   - the answer names an existing agent, a new agent the owner ratifies, or a skill.
6. *while* ownership is being settled, the agent *shall* do the work it can do now in whatever tree can hold it and mark that work provisional, the re-home landing later as ordinary pipeline work. [INV-197]

**Case: the crossing bound**

7. the system *shall* let one question cross between the same two agents at most twice, counted by the message identifier, and *shall* send the third crossing to the owner. [INV-196, INV-192, INV-27, INV-130]
   - the sender's status report names the third crossing as a zone question the two could not settle;
   - this is the shape the human-decision withdrawal loop already takes.
8. neither agent *shall* reopen the count by rewording the question. [INV-196]

**Case: a wrong referral is named**

9. *when* an exchange reaches the crossing bound through a referral met by a counter-referral between the same two agents, the system *shall* name the wrong referral in the sender's status report. [INV-225, INV-196, INV-27]
   - a wrong referral pointed at a zone which, by its own referring-back, does not own the target.
10. *when* a referral is answered by an acceptance, or an onward referral to a third zone answers it, the system *shall* reach no bound and name nothing. [INV-225]
11. the checker `guardrails/check-wrong-referral.py` *shall* read the shape of the exchange and ride the suite, staying clear of the push chain — the sequence of checks a push runs — *while* whether the target falls inside a zone's claim stays the receiving sweep's and the reviewer's judgment. [INV-225, INV-150, INV-222]

**Case: the message identifier**

12. the system *shall* mint a stable identifier per message from the sender's session identity plus a discriminator the sender mints for that message, so one session's two messages carry two identifiers. [INV-192, INV-117]
   - the sender's session identity is the harness session id where the context carries one, or else the session's start time joined with its worktree path and a nonce, recorded in the session checkpoint;
   - an exchange is keyed to its first message's identifier, which every reply names, so the crossing bound counts questions rather than sessions and outlives the sender's own session.
13. a reply *shall* name the message by that identifier after the file has left the inbox and become a row in the receiver's queue. [INV-192, E-11]

**Case: the reply and the terminal state**

14. a reply *shall* travel back to the sender as one new file in the sender's inbox, owing no blocked work of its own since the message it discharges already named the work. [INV-192, E-11]
15. every message *shall* state its need-by and *shall* reach one terminal state — delivered, declined, or escalated past its stated need-by. [INV-192, INV-1]
    [GAP: the spec does not name what checks that a message has passed its stated need-by, nor who sets the need-by value, so the move to the escalated state has no named watcher.]
16. *when* a message escalates, the system *shall* surface it in the sender's status report as blocked work aged past its need-by, and *shall* wake a dormant window on no occasion. [INV-192, INV-27]

**Case: authority does not travel by relay**

17. an agent-initiated message *shall* stand as a proposal in the receiver's queue until the owner ratifies it, *while* an owner-initiated message carries the owner's authority. [INV-193, INV-94]
18. relaying a message *shall* change only its carrier and leave its authority where it started. [INV-193, INV-94]

**Case: zones may overlap**

19. the system *shall* let two agents' zones overlap, each card recording what its own agent claims and two cards claiming one area both standing, and *shall* force no agent to carve a disjoint zone. [INV-197, INV-225]
20. the system *shall* build no uniqueness check over zone claims, the wrong referral alone earning a name. [INV-225]

---

## Requirement 198: The shared rules live once in the base skill

**Context:** Open any skill in the pack and the same working rules meet the reader. The five rules every skill works by are these: ask and never guess, plain words with the code trailing quietly, one surface with one name, one canonical home per fact, and a worker resuming from a checkpoint. These rules live once in the base skill, the pack's shared rulebook, and each working skill references them rather than restating them.

**User Story:** As a reader opening any skill in the pack, I want the shared rules stated once in the base skill and only referenced elsewhere, so that every skill reads one authoritative copy and no near-copy drifts.

### Acceptance Criteria

**Case: the shared rules have one home**

1. The base skill *shall* state each shared rule normatively beside the pack's default settings, and every working skill *shall* reference the shared rules rather than restate them. [E-12, E-13]
2. *when* a working skill states a shared rule in full a second time, the system *shall* read it as drift and fold it back, since a shared rule has one normative home in the base skill. [INV-13]
3. The pack *shall* treat the package as the source and the standalone repositories as read-only mirrors of it. [D-4]

**Case: a working skill names the base and stands alone**

4. Every working skill *shall* open with one line naming the base skill and the base version it was written against, swept in the same session that bumps the base so the pin never goes stale. [E-12]
5. The system *shall* keep a working skill usable outside the pack, its opening line reading as plain advice and nothing in its own domain needing the base installed. [E-12]

**Case: restatements are pruned at milestones**

6. *when* a milestone is reached, the compaction pass *shall* prune restatements older than the base one skill at a time, so no single rewrite is needed. [M-1, INV-13]

---

## Requirement 199: Every place the pack lists its skills names the same set

**Context:** The pack lists its skills in more than one reader-facing place — the working-skills sentence, the closing lists the skills carry, and the README table. A list is the kind of fact that drifts as the pack grows. A check runs at every commit and reds a list that names fewer skills than the complete set. The check's reach is that missing-member drift; a stale extra name past the complete set is outside its net and waits for a reader's pass.

**User Story:** As a reader trusting any skill list in the pack, I want every list to name the identical complete set under a mechanical check, so that a list that has fallen behind the pack turns the suite red instead of misinforming a reader.

### Acceptance Criteria

**Case: the lists agree or the suite reds**

1. The system *shall* name the identical complete set of skills in every place the pack lists them — the working-skills sentence, the closing lists, and the README table. [INV-66]
2. *when* a commit leaves a skill list naming fewer than the complete set, the system *shall* red the suite. [INV-66]

---

## Requirement 206: The seat owns judgment and workers run the tiers

**Context:** The seat owns every judgment call — spec deltas, matrix levels, findings triage, and this document. Workers own mechanical execution, each keeping a persistent checkpoint file under the host's `.live-spec/checkpoints/`. Three tiers stand: a no-decision one-shot worker, a multi-step mechanical worker, and the seat for judgment.

**User Story:** As a person watching work split between judgment and mechanism, I want judgment held by the seat and mechanical work run by tiered workers with durable checkpoints, so that the calls that shape the work stay with the agent qualified to make them.

### Acceptance Criteria

**Case: judgment stays with the seat**

1. The seat *shall* own every judgment call — spec deltas, matrix levels, findings triage, and this document — and that judgment *shall* never route down to a worker. [ACT-2]
2. The routing rule *shall* propose which tier a unit of work runs at before the seat may overrule it. [INV-69]

**Case: workers run the mechanical tiers**

3. The system *shall* run mechanical work on tiered workers — a no-decision one-shot worker, a multi-step mechanical worker, and the seat for judgment. [INV-69]
4. Each worker *shall* keep a persistent checkpoint file under the host's `.live-spec/checkpoints/`, kept out of git and off the temporary directory so a reboot never erases a resume point. [ACT-3, INV-69]

---

## Requirement 207: The worker contract binds every delegation

**Context:** One contract binds every delegation. A worker inherits its session's write-ownership narrowed to the files its brief names, reads outside them, and never writes there. Its brief carries the clock, the live setting lines, and the problem-ledger duty, and it heartbeats its checkpoint so a busy worker is never mistaken for a dead one. At teardown the worker reaps only the process group it spawned.

**User Story:** As a person relying on delegated work, I want every worker bound by one contract — narrowed write-ownership, an inherited clock and settings, a ledger duty, a heartbeat, and a scoped teardown — so that parallel help never corrupts the tree or the record.

### Acceptance Criteria

**Case: write-ownership is narrowed to the brief**

1. A worker *shall* inherit its session's write-ownership narrowed to the files its brief names, reading outside them and never writing there. [INV-10]
2. *when* a brief names an isolated copy of the tree, the system *shall* let that copy's delta reach the shared tree only through the seat's integration under the pen. [T-18, INV-39]
3. *when* the seat means to spawn another concurrent writer, it *shall* confirm the brief's write-set is disjoint from every running writer's brief or give it an isolated worktree, since the concurrent-edit fence stays quiet between same-session siblings. [INV-11, INV-105, ACT-3]

**Case: the brief carries the clock, the settings, and the ledger**

4. The system *shall* ride the session's live setting lines into the brief verbatim, since a worker cannot resolve the ladder itself. [E-13]
5. The system *shall* carry the clock into the brief so a worker's stamps come off the brief's clock and are never invented, and *shall* carry the problem-ledger path so any noise the worker meets becomes one recorded ledger line. [INV-24, INV-23]

**Case: the heartbeat and the scoped teardown**

6. A worker *shall* touch its checkpoint file on a fixed interval near 60 seconds as a heartbeat, so a compute-bound run that writes no product file for minutes is never read as dead. [INV-76]
7. *when* a result fails its brief's acceptance, the worker *shall* escalate one tier with a logged line and *shall* never retry silently on the same tier or skip a rung. [ACT-3]
8. *when* a worker tears down, the system *shall* reap only the process group it spawned, reading a stall as the checkpoint's modification time going untouched past about 2 minutes and confirming ownership before any reap, never a kill by name. [INV-162, INV-230, INV-76]

---

## Requirement 208: The routing rule proposes the cheapest tier and the senior may overrule

**Context:** Before anyone delegates a unit of work, the routing rule proposes its tier from what the work is, its size only a coarse prior — a judgment step to the seat and never down, a no-decision one-shot to the cheapest worker, a multi-step mechanical brief to the mid worker. The economy rung moves the threshold. The proposal is advisory: the seat may overrule it per wish, and the override rides one logged line reading proposed tier, chosen tier, and why.

**User Story:** As a person paying for the right tier on each unit of work, I want the routing rule to propose the cheapest tier that can pass the brief and the senior's override always logged, so that no tier changes silently and judgment work never routes down.

### Acceptance Criteria

**Case: the proposal reads the work**

1. The routing rule *shall* propose a judgment step to the seat and never route it down, a no-decision one-shot to the cheapest worker, and a multi-step mechanical brief to the mid worker. [INV-69, ACT-2]
2. The system *shall* treat the size class as a coarse prior only, the step inside the work deciding its tier. [INV-69]

**Case: the economy rung moves the threshold**

3. *when* the economy rung is lean, the system *shall* let an airtight brief — one that leaves the worker nothing to decide — ride one tier cheaper and *shall* raise the bar for keeping a step on the seat. [T-19, INV-69]
4. *when* the economy rung is tight, the system *shall* propose the cheapest tier that can pass the brief and *shall* spend the seat's hours on judgment alone. [T-19, INV-69]

**Case: the override is advisory and logged**

5. The seat *shall* be free to overrule the proposal per wish, and the system *shall* ride one logged line — proposed tier, chosen tier, and why — on the checkpoint and the delivery report. [D-2, INV-69]
6. The system *shall* keep this assignment-time override distinct from the failed-acceptance escalation, both logged on their own lines, so a silent tier change cannot stand. [ACT-3, INV-69]

**Case: an expensive dispatch proves its own need**

7. *when* a unit of work is dispatched to the expensive tier, the system *shall* open its brief with the refusal instruction, which assumes a cheaper tier and asks the run to answer first. [INV-300, INV-69]
   - the instruction and the tier ladder live in `guardrails/tier-refusal.json`;
   - a refusing run replies with one line naming the tier that fits and the reason.
8. *when* a run refuses, the system *shall* record the refusal with its task text, the named tier, the reason, and the date, and *shall* re-run the same brief at the named tier. [INV-300]
9. The system *shall* turn a task away before any model call once three recorded refusals name one tier and share a phrase from their task texts. [INV-300]
   - the promoted phrases sit in `guardrails/tier-refusal.json`, where a person reads them.

---

## Requirement 209: A delivered row carries its delegation accounting

**Context:** Every delivered queue row records how its work was delegated: the unit that went to a worker with an estimated saving, or a stood-down line naming why the seat kept the work. The line rides the delivery report the archived row carries, and a suite check reds a delivered row that omits it, reading it from the archive for a row landed after the format conversion. The duty binds the orchestrating seat whatever tier leads it.

**User Story:** As a person auditing how work was delegated, I want every delivered row to carry its delegation accounting under a suite check, so that the account of who did each piece of work is never silently dropped.

### Acceptance Criteria

**Case: the delivered row carries the line**

1. The system *shall* record on each delivered row's delivery report how its work was delegated — the unit sent to a worker with its saving, or why the seat kept it — and *shall* red the suite *when* a row landed after the conversion omits the line, reading it from the archive. [INV-103, INV-276]
   [GAP: the delegation accounting records a saving for each delegated unit, but the source names no unit or baseline the saving is measured against — tokens, wall-time, or cost — so a correct saving figure is undefined and a test author cannot pin it.]
2. The system *shall* bind the duty to the orchestrating seat whatever tier leads it, and *shall* bind it forward from its own reach rather than over rows already delivered. [INV-103, INV-159]

---

## Requirement 210: The seat reads to decide and dispatches the discovery reads

**Context:** The seat keeps its context lean by dispatching reads rather than performing them. It holds orchestration material — the human's words, the decisions taken, the distilled results workers return, and the anchors it must cite — and dispatches any reading done to understand or design past a bounded glance to a reader worker that returns a distillation. A read done to verify a claim or settle a decision stays with the seat. The leanness is load-bearing: a context filled with raw source it could have distilled loses the room to hold the whole arc.

**User Story:** As a person relying on the seat's judgment across a long arc, I want discovery reads dispatched to reader workers and only distillations kept, so that the seat's context stays lean and its judgment does not degrade under raw source.

### Acceptance Criteria

**Case: discovery reads route to workers**

1. The seat *shall* dispatch any read done to understand or design past a bounded glance to a reader worker and *shall* keep only the distillation. [INV-137, INV-69]
2. The system *shall* bound a glance to one small file or a handful of targeted lines whose result is itself the deliverable, past which the read routes like any unit of work. [INV-137, INV-69]
   [GAP: the glance's size bound carries no number in the source; its only stated test is that the read's result is itself the deliverable.]

**Case: verify reads stay, discovery reads show**

3. The system *shall* keep a read done to verify a claim or settle a decision with the seat, checking the real artifact and re-reading a primary source being its own hands. [INV-137]
4. The system *shall* dispatch the brief-owed read of the files a change will touch to the reader worker whose distillation returns the per-file lines, or make it a bounded decide-read for a small edit. [INV-53, INV-137]
   [GAP: the source names no size or line count for a small edit here, so where a bounded decide-read ends and a dispatched read begins is undefined.]
5. The system *shall* name the reads dispatched in the delivery report's delegation accounting, so a session that slid into reading to discover shows it. [INV-103, INV-137]

---

## Requirement 211: The seat decides what it can and surfaces only what it cannot

**Context:** The seat decides what it can decide and reports the choice — a mechanical step, a value a proven artifact already determines, a sensible default it can pick and name. It surfaces a decision to the human only where the decision genuinely cannot be made without them: a taste call, a trade-off no artifact settles, or a change to the definition of correct. It never parks derivable work on the human's queue to avoid deciding, and the posture holds even on a session resumed from its files after a memory wipe.

**User Story:** As a person who should be asked only what genuinely needs me, I want the seat to decide every derivable question and report it, so that a taste call reaches me while derivable work never waits on my queue.

### Acceptance Criteria

**Case: it decides what an artifact or a default settles**

1. The seat *shall* decide a mechanical step, a value a proven artifact already determines, or a default it can pick, and *shall* report the choice with its `[default]` tag. [INV-143, INV-121, INV-70]
2. The system *shall* hold this posture on every session, including one resumed from its files after a memory wipe. [INV-143, INV-48]

**Case: it surfaces only what needs the human**

3. The seat *shall* surface a decision to the human only where it cannot be made without them — a taste call, a trade-off no artifact settles, or a change to the definition of correct. [INV-143, INV-121]
4. The system *shall* never park derivable work on the human's queue to avoid deciding. [INV-143, INV-4]

---

## Requirement 212: A deferral must justify itself or the item is the seat's to do

**Context:** A backlog item carrying a needs-the-human's-word marker is re-tested for derivability every time it is touched, not only when first written. Where the answer pins to an existing artifact — a base rule, a spec sentence, the architecture, an approved prototype, or an already-answered decision — the item is the seat's to do, cite, and drop the marker. Where it needs a fact no artifact holds — a taste, a policy, a move irreversible outside git, or the feel of a real device — it is the human's and the marker stands, but writing the marker requires naming that human-only fact.

**User Story:** As a person handed only the questions that truly need me, I want every deferral marker re-tested for derivability and made to name its human-only fact, so that a derivable item becomes the seat's own work and stays off my board.

### Acceptance Criteria

**Case: a derivable item is the seat's**

1. *when* a held backlog item is touched, the system *shall* re-test it for derivability, and *when* the answer pins to an existing artifact the seat *shall* do the item, cite the artifact, and drop the marker. [INV-152, INV-59, INV-121, INV-143]
2. *if* the item needs a fact no artifact holds — a taste, a policy, a move irreversible outside git, or the feel of a real device (a feel judged only by the human's own hand on the human's own device) — *then* the marker *shall* stand and *shall* name that human-only fact. [INV-152, INV-17]
3. The system *shall* default a marker that cannot name its human-only fact to the seat's own, the unnamed marker being the finding, the same shape as a request matching no kind in the closed door set. [INV-152, INV-151]

**Case: two arms enforce the deferral**

4. The system *shall* red a commit *when* a mechanical net finds a parked item in the resume file or a decision page naming no reason category — taste, policy, irreversible, or device-feel (a feel judged only by the human's own hand on the human's own device). [INV-152, INV-155]
5. *when* a marker is written or a question is opened to the human, a delivery arm *shall* re-fire the derivability test at that moment, reading the grammatical shape of a deferral itself. [INV-152, INV-28, INV-4]

---

## Requirement 213: A worker's green earns a second pair of eyes

**Context:** A worker's report is a lead and never counts as evidence, since the head that made the work is blind to its own gap. So the verify step carries an audit — a whole-read that sets out to break the work: a fresh-context checker briefed with the spec sentences the delivery claims and the artifact paths, never the worker's summary or the senior's plan. It walks each claimed fact up a fixed ladder — that it exists, that it is substantive, that it is wired, and that real values flow end to end — and its findings become rows or red.

**User Story:** As a person trusting a green suite, I want a high-stakes delivery whose only review is its author's checked by a fresh adversarial reader, so that a green machine that is actually hollow is caught before it is called done.

### Acceptance Criteria

**Case: the audit walks a fixed ladder from a fresh context**

1. The verify step *shall* brief a fresh-context checker with the delivery's spec sentences and artifact paths, never the worker's summary or the senior's plan, opening on the hypothesis that the tasks were done and the goal missed. [INV-46]
2. The checker *shall* walk each claimed fact up a fixed ladder — that it exists, that it is substantive against the placeholder-stub list, that it is wired, and that real values flow end to end — its findings becoming rows or red. [INV-46]

**Case: it fires mandatory on a high-stakes author-only delivery**

3. The system *shall* fire the audit mandatory *when* a delivery is high-stakes and its only review is the author's own. [INV-46]
   - a delivery is high-stakes when it is a surface-sized delta or a change to the method itself;
   - a change to the method itself means a rule whose meaning changed.
4. The system *shall* count a review independent only *when* a differently-contexted head is briefed from the primary sources on the goal-missed hypothesis, a same-context prover pass never counting and delegation alone never making it independent. [INV-46]
5. One fresh checker *shall* cover every law in a delivery batch, the checker being a worker under its own contract whose verdict rides the delivery report. [INV-61, ACT-3]

---

## Requirement 216: A brief is born from read files, never from memory

**Context:** Before writing a brief that edits existing files, the brief-writer reads in full every file the work will modify. The brief records three lines per file — its current state, what changes, and what must survive — and every step back-references the spec sentence it serves while every technical claim cites its source. A brief written from memory hands the worker a guess dressed up as fact.

**User Story:** As a worker handed a brief, I want it born from a full read of the files it touches with three recorded lines each, so that I am handed evidence rather than the senior's guess.

### Acceptance Criteria

**Case: the brief is read from the files**

1. The system *shall* write a brief that edits existing files only after reading in full every file the work will modify, recording three lines per file — current state, what changes, and what must survive. [INV-53]
2. The system *shall* have every step back-reference its spec sentence and every technical claim cite its source as a file-and-line reference or a command's output. [INV-53]
3. The system *shall* dispatch this read to the reader worker whose distillation returns the three per-file lines, or make it a bounded decide-read for a small edit. [INV-53, INV-137]
   [GAP: the source names no size or line count for a small edit at this second occurrence either, so a test author cannot pin the boundary case.]

---

## Requirement 217: A worker stops only on a named condition

**Context:** The brief carries a closed, short halt list: an ambiguous requirement, two consecutive unexplained failures of one command, a missing config or dependency, or an acceptance impossible as briefed. On any of these the worker stops with evidence; otherwise it runs to completion. This is sharper than an open standing instruction to ask when unsure, and it composes with the one-tier escalation.

**User Story:** As a person delegating a bounded job, I want the worker to stop only on a closed list of named conditions and otherwise run to completion, so that it neither pushes past a real blocker nor stalls on ordinary uncertainty.

### Acceptance Criteria

**Case: the closed halt list**

1. The system *shall* carry a closed halt list in the brief — an ambiguous requirement, two consecutive unexplained failures of one command, a missing config or dependency, or an acceptance impossible as briefed. [INV-54]
2. *when* a halt condition holds, the worker *shall* stop with evidence, and otherwise *shall* run to completion, composing with the one-tier escalation. [INV-54, ACT-3]

---

## Requirement 218: A brief is sized to its worker's head

**Context:** A brief targets a bounded share of its worker's context and splits above it, the default bound being the brief's own text within about 300 lines and at most about 8 files to edit. Above either limit the work splits into staged briefs. A brief passes paths and never inlined file bodies, since an inlined body goes stale the moment a sibling edits the file.

**User Story:** As a worker with a bounded head, I want a brief kept under a concrete size bound and passing paths not file bodies, so that I read my own current truth from disk and no pasted copy goes stale.

### Acceptance Criteria

**Case: the size bound and the split**

1. The system *shall* keep a brief within its default bound — about 300 lines of brief text and at most about 8 files to edit — and *shall* split the work into staged briefs above either limit. [INV-55]
2. The system *shall* pass paths in a brief and never an inlined file body, so the worker reads its own current truth from disk. [INV-55]

---

## Requirement 219: The economy ladder names what a tight budget may shed

**Context:** Rigor costs money and time, so the pack names what a tight budget may legally shed and makes it a setting the human moved deliberately. The pressure lives as one setting, `budget.pressure`, with package default full, and it moves only on the human's word. Three rungs each name their legal sheds, and every shed actually taken is said in the delivery report.

**User Story:** As a person under a money or time pressure, I want the sheds named as a rung I set rather than improvised, so that cost-cutting is a recorded choice and every shed appears in the delivery report.

### Acceptance Criteria

**Case: the rung is a setting the human moved**

1. The system *shall* hold the pressure as one setting, `budget.pressure`, defaulting to full, moved only on the human's word — a session word for today or a profile line to stand. [T-19, E-13, INV-9]
2. *when* the human names a money or time pressure, the agent *shall* propose a rung and *shall* never set one, and the pack *shall* ask the rung or state the standing default at project setup beside the project kind. [T-19, INV-36]

**Case: each rung names its legal sheds**

3. *when* the rung is full, the system *shall* run the full suite at every delivery gate, run the prover at its recorded cadence, and route tiers by the routing rule. [T-19, INV-69]
4. *when* the rung is lean, the system *shall* scope mid-work test runs to the touched architecture node's rows while running the full suite at every delivery gate and before every push, and *shall* write a deferred full pass as a dated debt line in its queue row. [T-19, INV-69]
5. *when* the rung is tight, the system *shall* batch consecutive small deliveries into one full-suite run at the batch's end, keep each commit at one row's delta, and bisect a batch-end red by delivery order before reverting to the last green base. [T-19, INV-39]
   [GAP: the source names no size or count bound for a small delivery under the tight rung, so which deliveries qualify to share one batch-end run is unstated.]
6. *when* a push runs under any rung, the system *shall* still require the batch's reach-scoped gate green at the tree's head and the host's recorded prover cadence. [INV-45, M-6]

**Case: the tight rung's batch rollback**

7. *when* a batch-end run reds under the tight rung, the system *shall* bisect by delivery order; the system reverts the batch to its last green base and re-applies the clean landings, so `HEAD` never sits red across a breakpoint. [INV-39, T-19]

---

## Requirement 220: The never-bend list holds at every rung

**Context:** A short list of protections holds at every rung of the economy ladder no matter how tight the budget, and this never-bend list does not bend. It carries the door law and its tripwires, red-before-fix, the human's gates, the delivery report with its taken defaults and named sheds, delivery purity, the push gate running every check the diff can reach, the safety net, and whole narration. An explicit host line outlives any rung. The standard the work is held to stands outside every rung as well. A rung moves the project's pace, and a check the method calls for runs at whatever the plan costs.

**User Story:** As a person cutting cost under pressure, I want a named never-bend list that no rung touches, so that a tight budget slows spend without dropping the guarantees that matter.

### Acceptance Criteria

**Case: what never bends**

1. The system *shall* hold at every rung the door law and its tripwires, red-before-fix, and the human's gates over irreversible moves, publishing, authored content, and taste. [INV-40, T-12, INV-16, INV-9]
2. The system *shall* hold at every rung the delivery report carrying its taken defaults and named sheds, delivery purity at one row's delta per commit, and whole narration. [INV-40, INV-5, INV-31, INV-39, INV-35]
3. The system *shall* hold at every rung the push gate — work leaving the machine only when every check the diff can reach is green at the tree's head, plus the host's recorded prover cadence — and the safety net no work-kind or scope cut touches. [INV-40, INV-45, M-6, T-15, T-16]

**Case: an explicit host line outlives the rung**

4. *when* a host profile pins a tighter cadence, the system *shall* keep it even under the tight rung. [E-13, INV-40]
5. The system *shall* move `budget.pressure` only by the human's word and *shall* switch no rung automatically. [T-19, INV-40]

**Case: a rung moves the pace alone**

6. The system *shall* hold at every rung the standard the work is held to, moving the project's pace alone. [INV-40, T-19]
7. The system *shall* run a check the method calls for at whatever the plan costs. [INV-40, T-19]
8. The system *shall* hold at every rung the fresh clean-context agent any ask of the method raises. [INV-40, INV-46]
9. The system *shall* count an adversarial review, a cold reading, a release re-prove, and a deep audit among those asks. [INV-46, INV-145, INV-237, INV-266]
10. The system *shall* buy economy from pace, from batching, and from a cheaper tier on mechanical work, and *shall* buy it from no check. [INV-40, T-19, INV-69]

## Requirement 221: Every process converges on a goal named as an artifact

**Context:** Every piece of work the pack runs walks toward a goal. So the work names that goal up front as a concrete artifact it can be measured against — a frozen norm, an exemplar bank, a failing test, a written acceptance. A paraphrase cannot serve as that goal. Each pass measures its distance to the goal itself, and a level once reached is locked by a mechanism so the work cannot slide back. The machines this whole section lists are that principle's hands.

**User Story:** As a person relying on the pack, I want every process to name its goal as a checkable artifact and lock each level it reaches, so that work converges toward the goal rather than drifting near a look-alike.

### Acceptance Criteria

**Case: the goal is a named artifact**

1. *when* a process begins, the system *shall* name its goal as a concrete artifact the work can be held against, and *shall* refuse a paraphrase as that goal. [INV-98]
2. *while* a process runs, the system *shall* measure each pass against the goal artifact itself, since a stand-in is where a look-alike is born. [INV-98]

**Case: a reached level locks**

3. *when* a process reaches a level, the system *shall* lock it by a mechanism — a norm template, a conformance test, a lint floor that only rises, or a cap that only ratchets down. [INV-98]
4. *if* a stretch of work is deliberately divergent, such as an exploration or a labelled prototype, *then* the system *shall* allow it only when it is named and bounded by its convergence point. [INV-98]

---

