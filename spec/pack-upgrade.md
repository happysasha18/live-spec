## Requirement 180: The catch-up sequence brings an adopted host onto the current pack  [feature: F-catchup]

**Context:** An already-adopted host falls behind the pack as the pack moves. The catch-up sequence brings the host's documents and records onto the current pack. The owner asks in any wording; the version delta decides that catch-up fires, whatever words the ask used. The sequence runs four phases in fixed order.

**User Story:** As the owner of an already-adopted host that has fallen behind, I want catch-up to bring it onto the current pack in fixed phases behind my gate, so that the host is brought current with nothing lost. [A-11]

### Acceptance Criteria

**Case: a release that owes host actions ships a chapter**

1. *when* a pack release changes something a host must act on, that release *shall* land one dated, versioned migration chapter stating the host-side steps; a release owing nothing *shall* add no chapter and *shall* say so in its changelog. [INV-91]
2. The system *shall* build the work list as the ordered chain of migration chapters from the host's recorded pack version to the current one, oldest first. [INV-91]
3. *if* the host's record carries no readable pack version, *then* the system *shall* start the chain at the earliest chapter. [INV-91, INV-89]

**Case: the four phases in order**

4. The system *shall* run catch-up in four phases in fixed order: orient on the delta, plan behind the owner's gate, execute while preserving facts, then verify and re-record. [A-11]
5. *when* orient runs, the system *shall* read the host's installed-set record and tree, read the pack's current version and journal, and build the work list as the difference; *when* preconditions in the guide disagree with the tree, the system *shall* take the tree as the truth. [A-11]
6. *when* the delta includes founding questions the host has never answered, orient *shall* read the host's recorded `founding.set-version` against the current set and name each question added since. [INV-227]
7. *when* the plan is written, the system *shall* write it into the host's `.live-spec/adopt/`, list every file that moves, merges, or retires and every open conflict, and *shall* move no file before the owner's word on the plan. A plan that finds nothing to do *shall* report that and end. [A-11, A-8]
8. *when* execute runs, the system *shall* open with a clean-tree baseline commit, run under the checkpoint discipline, and resume an interrupted run from the checkpoint under the already-given gate. [A-11, A-5]
9. *when* verify runs, the system *shall* run the host's own gates including the suite, keep the sequence open until the gates read green, re-record the installed-set record in the current format, and land one journal chapter. [A-11, M-7]

**Case: machine-level steps run once**

10. *when* a step touches the machine's shared homes — the installed-skills folder or the personal profile — the system *shall* run it once per machine and *shall* report it done and skip it when its already-done check passes. [A-11]

---

