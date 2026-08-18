## Requirement 197: A new agent is created only on the owner's word  [feature: F-agent-birth]

**Context:** An agent reaches this point when a capability pins to no agent's zone, or when a capability has outgrown the agent hosting it. Any agent may propose a new agent, and the owner alone brings a new tree into being. The founded agent then declares itself by writing its own card, so every scan finds it from that moment.

**User Story:** As the owner of the machine, I want a new agent created only on my own word and declared by its own hand, so that a new tree and its standing cost never come into being without me and every scan still finds what is really there.

### Acceptance Criteria

**Case: any agent may propose**

1. *when* a capability pins to no agent's zone, or a capability has outgrown its host, the system *shall* let any agent propose a new agent, naming the capability, the zone the new agent would own, and the contracts it would publish. [T-22]
   [GAP: the spec does not name who judges that a capability has outgrown its host, or by what measure.]
2. the proposal *shall* carry the adversarial read an expensive decision earns and *shall* stand as a proposal until the owner ratifies the creation. [T-22, INV-235, INV-193]

**Case: the owner ratifies, the agent declares itself**

3. the owner's word *shall* authorize the creation, since a new agent is a new tree, a new queue, a new set of gates, and a standing cost the owner carries. [T-22, INV-10]
4. the owner *shall* ratify on the adversarial read the proposal carries, the read reaching the owner with its findings and a recommendation and the taste call staying the owner's. [T-22, INV-235, INV-143]
5. the founded agent *shall* declare itself by writing its own card, and every scan *shall* find it from that moment, no third party seating it. [T-22, E-32]
6. creating an agent *shall* be a delivery, so the new tree's journal *shall* record it with its date and the request row it cites. [T-22, INV-3, INV-24]

**Case: a false declaration travels the same scan**

7. *when* a tree declares itself with a card the owner never authorized, the system *shall* show that card in the same scan that finds every other, so the owner reading it sees what stands on the machine. [T-22, E-32]
   [GAP: no gate today catches a card whose creation carries no ratification, and the spec records that this behaviour owes one.]

**Case: the contract survives the migration**

8. *when* a capability moves from its old host to a new agent, the system *shall* let the consumer keep reading its pinned version until it chooses to move, the new owner publishing at the address its own card names. [T-22, INV-187, E-32]

**Case: the kind is the owner's call**

9. *when* a capability sits on the line between a skill and an agent, the owner's word *shall* settle which it is, the call recorded with its date in the proposing agent's journal. [T-22, INV-182, INV-152, INV-24]

