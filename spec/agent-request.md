## Requirement 195: An agent earns a message before it deposits one  [feature: F-agent-ask]

**Context:** A sender agent reaches this point holding the receiver's card and inbox address and a piece of its own work the receiver's zone blocks. A message is one new file in the receiver's inbox, and every message names the work of the sender's own that earned it. The agent recognizes the neighbour's zone on its own and deposits the message in the course of its work, telling its user each time.

**User Story:** As an agent blocked by a neighbour's zone, I want to deposit a message only when my own work earns it, so that curiosity and tidiness generate no traffic on the channel.

### Acceptance Criteria

**Case: the transport**

1. a message *shall* be one new file in the receiver's inbox, named and shaped as every inbox item, naming its source with the `from-<agent>` form the inbox uses. [INV-189, E-11, INV-193, INV-146]
   - two source words are reserved and own no ground;
   - `from-owner` names the owner's own message;
   - `stranger-` names a stranger's bridged item, the inbox file the monitor commits from a stranger's issue.
2. the system *shall* deposit that one file by the standing arms — a co-located sender writes it and stops, a remote sender commits and pushes it under its per-repo grant, and the receiver's sweep carries it into the receiver's queue. [E-11, INV-10, INV-174, INV-112, T-10]

**Case: a message names the work that earned it**

3. a message *shall* name the sender's own work that earned it, and a message that can name no such work *shall* stay unsent. [INV-189]
4. a blocked message *shall* name the blocked work — a real row, a real failing step, a real thing the sender cannot finish *while* the receiver's zone stands as it does. [INV-189]
5. a lived-fault message *shall* name the fault and the evidence the sender lived — what it ran, what happened, and how the fault showed itself. [INV-189]

**Case: three grounds, and the set is closed**

6. the system *shall* recognize exactly three grounds for a message. [INV-189, INV-197]
   - the sender is blocked by the receiver's zone as it stands;
   - the sender has lived a fault in that zone and carries the evidence;
   - the sender holds a concern no agent's zone owns, carried to the pack as its default owner.
7. a candidate message matching no ground *shall* stay unsent, and the third ground *shall* carry only to the pack and only *while* no zone owns the thing. [INV-189, INV-197]

**Case: the owner's zone is presumed informed**

8. the system *shall* report to a zone's owner nothing that owner's own instruments already see, so a fault the owner's instruments cannot see, carried with the evidence the sender lived, is the case that earns the file. [INV-189]

**Case: the agent recognizes the zone and deposits on its own**

9. *when* an agent's own work meets a fault or a lack in something another agent's zone owns, the system *shall* scan for cards, find the owning agent, and take the channel that fits, on its own recognition. [INV-195, E-32, INV-183]
10. *when* the agent's work earns a message under a ground, the agent *shall* write the file to the neighbour's inbox in the course of its own work. [T-24, INV-189, INV-153, INV-163]
   - the trigger is any earned ground the work meets, so every occasion that earns a ground qualifies;
   - the pack states the form of a message, and the host's work states its content.
11. the deposited message *shall* name its references by the pair, so the neighbour reads a self-explaining file. [T-24, E-35]

**Case: the user is told**

12. *when* the agent deposits a message, the system *shall* tell its own user in the status report, naming the message's subject by its pair and the neighbour it reached, in a plain notice. [T-24, INV-27, INV-28, INV-31]
13. *when* the earned-message law declines a message the agent had drafted, the system *shall* tell the user in the status report with the reason it was withheld, and *shall* raise no tell for an impulse the discipline turned away before it became a draft. [T-24, INV-190, INV-191]

**Case: a capability is reached across its zone**

14. an agent needing a capability another agent's zone owns *shall* send a message or read a contract rather than keep a local copy of it. [INV-194, INV-183]

**Case: a deposit is written whole**

15. the system *shall* write a deposit into another window's inbox under a `.draft` name and make it final by an atomic rename once the content is complete. [INV-249]
16. the receiving sweep *shall* act only on a finished deposit and *shall* pass over any name still carrying the `.draft` suffix, leaving a routed deposit earned in place rather than removing it under a live writer. [INV-249, INV-247]

---

