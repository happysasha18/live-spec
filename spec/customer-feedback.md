## Requirement 152: Handing feedback back to the workshop  [feature: F-feedback]

**Context:** A person looks at what shipped and something occurs to them. It might be a reaction, an answer, a screenshot with a red circle, or a log file. Feedback is anything a person hands back, at any size and through any channel. Two promises hold over all of it: nothing handed in is ever lost, and every item is answered by a route.

**User Story:** As a person handing something back to the project, I want every item captured and routed to one home, so that nothing I hand in is lost and I never have to hand the same thing in twice.

### Acceptance Criteria

**Case: every item lands in its route's home**

1. *when* a session receives a handed-in item, the system *shall* land it the same session in the home its route owns. [INV-68]
   - a wish lands in its queue row;
   - an answer lands in its decision archive and harvested row;
   - a fix lands in its commit and journal line;
   - workshop noise lands in the problem ledger.
2. *when* an item's route had no prior home — field evidence, a plain reaction, or a wordless drop — the system *shall* record it as one dated line in the feedback ledger. [INV-68, E-28]

**Case: the ledger line and its echo**

3. The system *shall* record each feedback-ledger line with when the item arrived, who handed it in and through which channel, what it concerns on the feature map, the item in plain words, and where it went. [INV-68]
4. *when* an item arrives, the system *shall* echo it back in one sentence, one echo per item, a wish-shaped item taking the wish echo and any other item taking a note stating what was heard and where it went. [INV-27]
5. *if* a person mentions an already-recorded item again, *then* the system *shall* append the new date to the existing line and change nothing else. [INV-68]
   [GAP: the matching rule that decides a new mention is the same item as an existing ledger line is unstated in the source.]

**Case: the promise is checkable**

6. The system *shall* keep every received item findable in the ledger, with its route, in the same session, so the same item never has to be handed in twice. [INV-68]

---

## Requirement 153: The three channels feedback arrives through  [feature: F-feedback]

**Context:** Feedback reaches the project through three channels, and all three meet one contract. A person speaks or types it, comments on something shown, or drops a file. An outside session reaches the project only through the inbox door.

**User Story:** As a person with something to hand back, I want any of the three channels to carry it under one contract, so that the channel I happen to use never changes whether the item is captured and answered.

### Acceptance Criteria

**Case: spoken or typed**

1. *when* a person makes a remark in the conversation or points at a note in a file, the system *shall* receive it as a feedback item on the spoken-or-typed channel. [T-20]

**Case: a comment on something shown**

2. *when* a person comments on a decision page or a review page, the system *shall* capture the answer as saved data, each saved answer being one feedback item whose home is the decision archive and its harvested row. [T-20, INV-4, INV-64]

**Case: a dropped file**

3. *when* a file arrives — a screenshot, a log, or a document — from the person in the conversation or from an outside session through the inbox, the system *shall* take it as one new committed file under the naming and collision law that wishes use, swept in by the host's own session. [T-20, E-11, T-10]
4. *if* a dropped file carries no words, *then* the system *shall* ask one plain question about what it means and *shall* record no guess in the ledger. [T-20]

---

## Requirement 154: Every item takes exactly one of five routes  [feature: F-feedback]

**Context:** Every item takes exactly one route, and each route already has its law and its home. The seam between the product and the workshop decides the last two: the product's behaviour goes to the feedback ledger, the workshop's own behaviour goes to the problem ledger, one home each. The seam turns on what ships: a fault in what the product ships is the product's own, and a fault in the tooling that builds, tests, or runs it without shipping is the workshop's own. A second seam separates the first two behavioural routes from the third: shown work is the artifact in front of the person for review before it lands — a diff, a decision page, a review page — while a shipped feature already carries a scenario in the spec and sits in use. A comment on shown work takes route 2; a reaction to a shipped feature takes route 4.

**User Story:** As a person handing in items of every kind, I want each item sorted to exactly one route with its own home, so that a wish, an answer, a fix, a field reaction, and a workshop hiccup each land where their law already governs them.

### Acceptance Criteria

**Case: the behavioural routes**

1. *when* an item asks for new behaviour, the system *shall* route it as a wish through wish intake with its own echo, door, and row, that row being its home. [T-20, T-12, INV-27]
2. *when* a fix-sized comment lands on shown work, the system *shall* fix it the same session with its commit and journal line as its home, and *shall* queue a story-sized comment as a wish instead. [T-20]
   [GAP: the source names no numeric measure for the size boundary; the glossary's user-story test decides it — a comment naming a distinct new thing a person does and sees is story-sized and queues, and any other comment is fix-sized.]
3. *when* a person answers an open question, the system *shall* harvest it the same session into the decision archive and the harvested row, closing the question for good. [T-20, INV-59]

**Case: the field and workshop routes**

4. *when* a person reacts to a shipped feature, the system *shall* land it as field evidence in the feedback ledger with the line citing the feature's scenario, and *shall* grow it into a wish only on the person's word or a tripwire verdict. [T-20, INV-21]
5. *when* the noise is the workshop's own — a flaky tool, a missing dependency — the system *shall* route it to the problem ledger, and *shall* record a standing behavioural rule's mid-turn break there as one entry the once-read-rules sweep reads. [T-20, INV-23, INV-108]

---

## Requirement 155: feedback-intake receives and never opens a row  [feature: F-feedback]

**Context:** The skill feedback-intake owns this behaviour. It fires the moment a session receives an item, and again at every inbox sweep for any file that carries feedback. It stays quiet when there is nothing to receive, and it holds no verdict of its own on what becomes a queue row.

**User Story:** As a person relying on the pack to catch what I hand in without inventing work, I want feedback-intake to fire on a real handed-in item and stay silent otherwise, so that every item is caught while my passing mentions and the agent's own output never spawn a row.

### Acceptance Criteria

**Case: when it fires**

1. *when* any session receives a handed-in item, the system *shall* run feedback-intake, and *shall* run it again at every inbox sweep for any file that carries feedback. [T-20, T-10]

**Case: when it stays quiet**

2. The system *shall* keep feedback-intake quiet on the agent's own output, on a question the agent asked, and on something a person merely mentions without handing it in. [T-20]
3. *if* it is unclear whether a remark was handed in, *then* the system *shall* ask one plain question rather than record it. [T-20]
4. The system *shall* never open a queue row on feedback-intake's own judgment, the intake door owning that verdict. [T-20]

---

## Requirement 156: A strong reaction earns an offer to note the authors  [feature: F-feedback]

**Context:** The pack carries a third arm beside carrying work out and taking feedback in: an occasional note up to the pack's own authors, so they learn what delighted or hurt real use. The skill feedback-collector owns the arm. It reads the agent's own observation, exactly the moment feedback-intake leaves alone, and the two arms do disjoint work rather than compete.

**User Story:** As a person whose strong reactions could teach the pack's authors, I want a rare one-line offer to send them a note, so that a real delight or hurt reaches the people who wrote the pack while a mild moment passes in silence.

### Acceptance Criteria

**Case: the rare offer**

1. *when* the conversation shows a genuinely strong reaction, the system *shall* offer to send an upstream note. It *shall* stay silent on a mild or routine reaction. [E-30]
   - the offer is one line, made only where the host has switched the upstream-note arm on;
   - such a reaction reads as a real delight, a real hurt, or a comparably notable moment.
   [GAP: the source defers the reading of a strong reaction to a conservative floor and a later design pass, so the measure that separates a strong reaction from a routine one is unstated.]

**Case: the two arms do disjoint work**

2. *when* a person hands in a strong moment, the system *shall* both log its field-evidence ledger line through feedback-intake and, when the moment reads as strong, offer the upstream note through feedback-collector. [E-30, T-20]
3. *when* the agent's own unhanded observation reads as a strong moment, the system *shall* let feedback-collector offer the note while feedback-intake stays silent, since that observation is the arm feedback-intake leaves alone. [E-30, T-20]

---

## Requirement 157: The upstream note is distilled, consented, and deposited  [feature: F-feedback]

**Context:** When the person gives a positive word, the pack writes an upstream note and deposits it; the person delivers it. Consent here is the deliberate opposite of the pack's usual silence-is-consent, because the move is an outbound send about a real person. The arm is off by default and honours its flag on every read.

**User Story:** As a person deciding whether a note about my use travels upstream, I want the pack to send nothing without my explicit yes and to hand me a distilled, anonymized note to deliver myself, so that no private detail leaves the machine on the pack's own and I hold the send.

### Acceptance Criteria

**Case: consent is a positive word**

1. *when* feedback-collector would send a note, the system *shall* ask the person's explicit consent every time and *shall* leave the note unwritten on a silence or an unclear answer. [INV-161, INV-31]
2. The system *shall* keep the arm off by default under its package-default flag, *shall* never fire, read for a strong moment, or ask on a host that has not switched it on, and *shall* turn it on only where a host records a profile line. [INV-161, INV-14]

**Case: what the note holds and where it goes**

3. *when* the person gives a positive word, the system *shall* write a short distilled account that carries its own context to a reader who does not know this user, holding no raw material, transcript, or private content beyond its self-containment test: the note's author strips everything a reader who does not know this user can do without while still understanding the point. [T-21, INV-161]
4. *when* the note is written, the system *shall* deposit it into the host's gitignored outbox directory named by date, *shall* open no network connection and no public request, and *shall* leave the delivery upstream as the person's own step. [T-21, INV-161]
5. The system *shall* anonymize the draft written after the person's positive word, turning the host's real entities into neutral role words while the pack's own public names stay, and *shall* let the note travel only once the person has read and approved that anonymized draft. [INV-179]

**Case: the note's own name and its record**

6. The system *shall* carry this arm's own name, the upstream note, distinct from the station-completion digest (the two or three plain sentences a finished pipeline station's beat carries) and the resume-file digest (the capped restatement of each open leg written into the resume file). [T-21, INV-35, INV-48]
7. The system *shall* record one dated ledger line that an offer was made and answered — when, an upstream-note offer, the person's answer, and the outbox filename when the answer is yes. [INV-161, INV-68]

---

## Requirement 158: Only the assigned session writes the ledger, and it never trims  [feature: F-feedback]

**Context:** The feedback ledger is a shared file. Outside sessions never edit it; they use the inbox door, and only the assigned session appends the ledger. The ledger is append-only and archives like the queue, extending the no-wish-ever-lost law rather than amending it.

**User Story:** As a person trusting the ledger to hold everything, I want only the assigned session to write it and the file never trimmed, so that concurrent work cannot scramble it and no recorded item is ever dropped.

### Acceptance Criteria

**Case: one writer, one door**

1. The system *shall* let only the assigned session append the feedback ledger, and *shall* route every outside session through the inbox door under the write-ownership and concurrent-edit fences. [INV-10, INV-11]

**Case: append-only, never trimmed**

2. The system *shall* keep the feedback ledger a file where nothing is ever deleted or trimmed — a repeat mention adds its date to its existing line — and *shall* archive it like the queue, extending the no-wish-ever-lost law rather than amending it. [INV-1]
3. The system *shall* read a feedback ledger holding only its header as a healthy empty state. [INV-68]

**Case: what this section does not add**

4. The system *shall* add no end-user feedback widget on a host's own product, a site's visitors riding the measurement family or their own wish. [E-28]
5. The system *shall* add no automatic reading, scoring, or aggregation of the ledger, and *shall* reuse the inbox as it stands with no new door mechanics. [INV-68]

---

