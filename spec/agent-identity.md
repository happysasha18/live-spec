## Requirement 193: An agent is found by the card it writes and a live scan  [feature: F-roster]

**Context:** An agent reaches this point the moment it meets something that might belong to another agent — a capability it lacks, data another project holds, a question about a neighbour's zone. It answers by scanning for cards, since a card is what makes a tree an agent. It comes away holding the owning agent's name, mission, zones, contracts, and inbox address, or it learns no agent owns the thing, which opens the birth scenario.

**User Story:** As an agent meeting something outside its own zone, I want to find the owning agent from a card it wrote and a live scan, so that who owns what is always a lookup.

### Acceptance Criteria

**Case: the card is the declaration**

1. the agent card *shall* live in the agent's own tree at `.live-spec/agent.md` and *shall* name the agent's name, its standing mission, the zones it owns, each contract it publishes with the path its artifact lives at, and its inbox address. [E-32]
2. the system *shall* treat a tree that carries a card as an agent, and writing the card *shall* be the one act that seats it. [E-32, INV-184]
3. *when* an agent finds no card on a thing that might not be its own, the system *shall* ask one plain question rather than guess. [INV-184, INV-4]

**Case: discovery is a live scan**

4. the system *shall* discover agents by reading two globs under each root — `<root>/*/.live-spec/agent.md` and `<root>/*/*/.live-spec/agent.md` — and *shall* treat every card it finds as an agent. [INV-184, E-32]
5. the scan's roots *shall* be the parent directory of the reader's own tree together with any root the personal profile names. [INV-184, E-16]
6. the scan *shall* descend no branch, so its whole cost is two directory listings per root and one stat per candidate. [INV-184]
7. the system *shall* run the scan live on every lookup and *shall* keep no cached index of who exists, since a scan reads the machine as it stands *while* a cached list answers from a past moment and is the shared file two windows race to edit. [INV-184, INV-10, INV-11]

**Case: no shared file describes an agent**

8. the system *shall* let no file outside any tree describe any agent, each agent owning its own description the way it owns its own tree. [INV-184, INV-10]
9. the system *shall* read the owning card before acting on anything that might not be its own, the reviewer's review standing as the net for that discipline. [INV-184, INV-150]

**Case: the card needs no permission, and its bounds**

10. the system *shall* grant the card by write-ownership, so writing it needs no permission act. [INV-184, INV-10]
11. the card *shall* hold the agent's own identity and addresses, and product data placed in a card *shall* be a contract field taking the contract's permission road. [INV-184, INV-185]

**Case: a tree with no card is flagged**

12. *when* an inventoried live-spec host tree carries no `.live-spec/agent.md`, the system *shall* flag it as an incomplete record and *shall* have the host write its card at its catch-up walk. [INV-184, A-10, A-11, INV-159, INV-36, INV-135]
   - an incomplete record ranks the same as a project kind recorded with no declared layers;
   - the duty binds forward.
13. the gate `guardrails/check-agent-card.py` *shall* read a host tree's root and fail by name *when* the root carries no `.live-spec/agent.md`, and the pack carries its own card so the gate reads the pack's tree and passes. [INV-219, INV-97]

---

