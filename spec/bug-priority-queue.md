## Requirement 160: A bug preempts the lane, and rolling features park  [feature: F-bug]

**Context:** Mid-feature, the human reports a bug in the shipped product — the card is broken on the phone. The feature in work is set aside at a checkpoint, the bug takes the lane, and once no bug waits the feature returns as the next thing to finish. When nothing is in work, the bug takes the lane directly.

**User Story:** As the product owner, I want a reported bug fixed before anything else while the mid-build feature comes back on its own afterward, so that an urgent defect is handled at once and no in-flight work is lost.

### Acceptance Criteria

**Case: the bug takes the lane, the feature parks**

1. *when* a bug report arrives mid-feature, the system *shall* move the feature to parked with a checkpoint written first — the failing test names when any are red, the current hypothesis, and the touched files — and *shall* commit no work while a test is red. [T-9]
2. *when* the bug holds the lane, the system *shall* run it to completion, and *shall* have an arriving bug join the waiting line and interrupt nothing. [T-9]
3. The system *shall* order waiting bugs critical-first, by the same three conditions the priority mark carries [INV-12], and *shall* order bugs of equal priority by arrival. [T-9, INV-12]
   - a bug is critical when the shipped product is broken for its user.

**Case: resume order and the parking bound**

4. *when* no bug waits, the system *shall* resume parked features ahead of the whole queue. A wish marked critical or quick win may bubble. It jumps only fresh queued wishes. It never jumps a resume. [T-11]
5. The system *shall* park at most one feature per lane, and *when* more than one lane was rolling *shall* park them all, each at its own checkpoint, resuming in their landing order. [T-18]

**Case: a resumed feature re-proves on the new tree**

6. *when* a parked feature resumes, the system *shall* re-fence and re-prove its spec-delta against the now-committed truth before it integrates, since the bug's fix may have moved the law the spec-delta was built against. [T-9, INV-39]
7. The system *shall* integrate no spec-delta proven only against the pre-bug truth without re-verifying it on the new tree, and *shall* leave every parked feature back in work or landed in its original order once the fix has landed, with no red work committed anywhere. [T-9, INV-39]

---

## Requirement 161: A confirmed bug drives a class hunt before it closes  [feature: F-bug]

**Context:** A confirmed bug is one sample of its class. Before the fix is called done, the method drives four moves rather than one — name the class and hunt its siblings, check the architecture, check the spec, and escalate a boundary call to the human — so a point fix that leaves the rest of the class standing is a status, never a landing.

**User Story:** As the product owner, I want a confirmed bug treated as one instance of a class and its siblings hunted before the fix closes, so that the same kind of defect is cleared everywhere it lives, hunted past the one place it happened to show.

### Acceptance Criteria

**Case: name the class and hunt its siblings**

1. *when* a bug is confirmed, the system *shall* name the defect abstractly, then search every surface where that kind could live and fix every sibling found in the same change. [INV-124, INV-56]
   - naming it abstractly means naming the kind of mistake: a scope too narrow, a missing guard, or an assumption that holds in one place and fails in its neighbour.

**Case: check the architecture and the spec**

2. *when* the bug has a structural cause — a boundary the architecture drew wrong or left silent, a node owning what it should not — the system *shall* update the architecture in the same change. [INV-124]
3. *if* the spec is silent on the broken behaviour or under-describes its composition, *then* the system *shall* fix the spec first so the prover can flag it, and *shall* land the code fix under it. [INV-124, INV-15]

**Case: escalate a boundary call, and the close condition**

4. *when* the class boundary needs the human's read — which behaviours are one class, the intended design, whether a whole area wants a rethink — the system *shall* stop and ask rather than guess the boundary. [INV-124, INV-4]
5. The system *shall* treat the four moves as the bug's close condition, and *shall* read a point fix that leaves the siblings standing as a status short of a landing. [INV-124, INV-26]
6. The system *shall* have the prover carry a class lens on a found defect — whether the same kind lives elsewhere, whether the architecture accounts for it, and whether the spec describes it. [INV-124]

---

