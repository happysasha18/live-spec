## Requirement 7: Open questions arrive together on one decision page

**Context:** Several open questions reach the person together on one decision page rather than one at a time in chat. The page opens in its own window while the rest of the work carries on. Each question is a card with its recommended answer marked and room to write another. Once answered, the page is filed and every answer folded into its queue row the same session.

**User Story:** As a person who owes the pipeline several decisions, I want them gathered on one page I answer on my own clock, so that questions never dribble out one at a time and no answer I give is lost.

### Acceptance Criteria

**Case: questions arrive together and are folded back**

1. *when* more than one open question stands, the system *shall* carry them to the person on one decision page that opens in its own window while the rest of the work carries on. [E-22, INV-4]
2. The system *shall* present each question as a card with its recommended answer marked and room to write a different one. [E-22]
3. *when* the decision page comes back answered, the system *shall* file it in the decision archive `docs/decisions/` and fold every answer into its queue row the same session, since an answer left unread is a decision lost. [E-22]

**Case: the person's word settles it**

4. The system *shall* treat the person's word as what settles a decision and *shall* read a click as recording only a first pick, so a pick taken back in plain speech is withdrawn, logged as answered-then-withdrawn, and asked again later in plainer terms. [INV-9]
5. The system *shall* settle nothing that needs the person's considered word on a pick made without understanding. [INV-9]
   [GAP: the at-pick signal for a without-understanding pick is unstated in the source; the stated mechanisms are the plain-speech withdrawal and the card-defect rule (a card unanswerable without its mechanism is a defect).]

**Case: a withdrawn decision converges**

6. *when* the same decision is withdrawn a second time, the system *shall* take the recommended option, surface it as a `[default]` in the delivery report, and never re-ask it, silence staying consent from there. [INV-130, INV-31]
7. The system *shall* close an answered question for good and *shall* route a later change of mind as a new wish, the closed decision staying closed. [INV-59, INV-130]

**Case: the page mechanics have one home**

8. The system *shall* keep how the page works — its filename, its ordering, its round-trip — written once in the communicator skill's rule 10. [INV-13]

---

## Requirement 8: A decision card asks in consequences

**Context:** A decision card opens with what each option changes for the person — what it gives them or what problem it removes — in the product's own words. The mechanism follows only where it aids the choice. Each option is labelled by its consequence, never by its implementation.

**User Story:** As a person answering a decision card, I want each option framed by what it changes for me, so that I can decide without first learning how the machinery works.

### Acceptance Criteria

**Case: the card asks in consequences**

1. *when* a decision card is shown, the system *shall* open it with what each option changes for the person and *shall* label every option by its consequence, bringing in the mechanism only where it aids the choice. [INV-32]
2. The system *shall* read a card that cannot be answered without understanding the mechanism as a defect of the card. [INV-32, INV-28]

---

## Requirement 31: A review surface shows its sources and accepts the person's edits

**Context:** A review surface shows its sources and accepts the person's edits. Anything shown for review carries per-claim provenance, marking each claim by where it came from — read from the artifact, the person's own recorded word, or the agent's inference. Inferences are flagged most prominently.

**User Story:** As a person reviewing a surface the agent shows, I want each claim marked by its source and the surface open to my edits, so that no work reaches me as a read-only wall or an unmarked guess.

### Acceptance Criteria

**Case: per-claim provenance**

1. The system *shall* mark each claim on a review surface by where it came from — read from the artifact, the person's own recorded word, or the agent's inference — and *shall* flag an inference most prominently. [INV-64]

**Case: the surface is commentable**

2. The system *shall* keep the surface commentable and open, giving line-by-line room for the person's word and capturing the answers. [INV-64]
3. The system *shall* extend the decision page's saved-answers rule to a review surface as one round-trip back to the project. [INV-64, INV-32]

---

## Requirement 32: The person's word is read as meant, and the person's cuts hold

**Context:** The person's word on a shown artifact is read as meant, and the person's cuts hold. A phrasing the person removed in a review round stays removed in every later draft of that artifact. A vivid phrase from the person is adopted only as meant, since a person sometimes writes mockery of a bad draft rather than guidance.

**User Story:** As a person who cut a phrasing and wrote a colorful remark, I want the cut to hold across every later draft and the remark read for its intent, so that a cut word never reappears and a parody is never baked in as if prescribed.

### Acceptance Criteria

**Case: a cut holds across drafts**

1. The system *shall* keep a phrasing the person removed in a review round removed in every later draft of that artifact, holding the removal list where the artifact's project keeps its records rather than in session memory alone. [INV-42]
2. The system *shall* read a cut word reappearing a later round as a defect, however fresh it looks, since a memory wipe restores no cut phrasing. [INV-42]

**Case: a vivid phrase is read for intent**

3. Before a colorful phrase from the person shapes the work, the system *shall* read its intent from context or ask, rather than assuming a mockery of a bad draft is prescriptive. [INV-42, INV-4]
4. The system *shall* cross-link the two standing bans this rests on — no self-praising drama, and no approval-begging under silence-is-consent — rather than restate them. [INV-42, INV-31]

---

## Requirement 33: Approved text is frozen, and a revision applies only the named correction

**Context:** Approved text is frozen, and a revision applies only the named correction. Once the person approves a text it is settled material. A later revision applies exactly the correction the person named and does not rewrite the surrounding text.

**User Story:** As a person who approved a text, I want a later revision to apply only the correction I named, so that approved material never churns under a rewrite I did not ask for.

### Acceptance Criteria

**Case: only the named correction lands**

1. *when* the person approves a text, the system *shall* treat it as settled material. [INV-58]
2. *when* a revision is applied, the system *shall* make exactly the correction the person named — trim what they said to trim, swap what they said to swap — and *shall* leave the surrounding text untouched. [INV-58]
3. The system *shall* read churn of approved material as a defect, kin of a reappearing cut. [INV-58, INV-42]

---

## Requirement 34: No question is asked twice, and dialogues converge

**Context:** No question is asked twice, and dialogues converge. Before any ask, the agent searches the recorded word — the decision archives, the review records, the journal, and the profile. An answered question closes permanently and is recorded into its row the same session.

**User Story:** As a person whose answers are on record, I want the agent to search them before asking and to close an answered question for good, so that I am never asked a question a record already answers and a solved problem returns with evidence rather than re-described.

### Acceptance Criteria

**Case: the search before every ask**

1. Before any ask, the system *shall* search the recorded word — the decision archives, the review records, the journal, and the profile — and *shall* read asking a question a record already answers as a defect. [INV-59]

**Case: dialogues converge**

2. The system *shall* close an answered question permanently and record it into its row the same session. [INV-59]
3. The system *shall* return a problem the person named solved with evidence rather than re-described, so a later round carries only new material. [INV-59]

---

## Requirement 35: A taste ask arrives carrying the agent's own researched proposal

**Context:** A taste ask arrives carrying the agent's own researched proposal. A genuine taste question arrives with work already done — mined exemplars, precedents, and real options with citations — and a chosen recommendation with its evidence.

**User Story:** As a person asked a taste question, I want it to arrive with the agent's own research and a recommendation, so that I am never asked to supply what the agent should have mined first.

### Acceptance Criteria

**Case: research precedes the ask**

1. The system *shall* mine the material first — exemplars, precedents, and real options with citations — and *shall* then ask with a chosen recommendation and its evidence. [INV-60]
2. The system *shall* read asking the person to supply what the agent should have mined as a defect, this sharpening the recommended-option rule for a taste call. [INV-60, INV-4]

---

## Requirement 36: The removal list has a mechanical form

**Context:** The removal list has a mechanical form. For a host with taste-reviewed artifacts, the pack ships a removal-list template that holds the person's cuts as dated literals, appended the moment a cut happens and never removed. The pack also ships guardrails guidance for a scanner.

**User Story:** As a person whose cuts must hold, I want the removal list backed by a shipped template and a scanner, so that a literal I once cut turns the suite red if it reappears in the artifact's surfaces.

### Acceptance Criteria

**Case: the template and the scanner**

1. The system *shall* ship a removal-list template holding the person's cuts as dated literals, appended the moment a cut happens and never removed. [E-26]
2. The system *shall* ship guardrails guidance for a scanner that reads the table and greps the artifact's surfaces, turning the suite red *when* a removed literal reappears. [E-26, INV-42]

**Case: the scanner stays per-project**

3. The system *shall* keep the scanner per-project, the pack shipping the shape — the template and the guidance — while each host owns the greps that read its own surfaces and holds its own dated cuts. [E-26, INV-163]
4. *when* a host's scanner grows a genuinely generic seam, the system *shall* lift that seam to the pack and *shall* keep the host-specific greps at home. [E-26, INV-163]

## Requirement 69: Every design review finding carries a confidence read, and a strong likely one becomes one question

**Context:** Each design review finding carries a confidence read of confident or likely. A confident finding is written as a recommendation that queues and never blocks; a likely finding is written as one question to the human with both objects in hand, raised only when the signal is strong. At most three such questions ride per pass, strongest first, and an unanswered question is held quietly for the person.

**User Story:** As a person the design review would ask, I want a confident finding queued and a strong likely one raised as one batched question, so that the strongest genuine questions reach me without the lane ever waiting on them.

### Acceptance Criteria

**Case: confident queues, likely asks**

1. The system *shall* write a confident finding as a recommendation that queues and never blocks, a finding being confident *when* the reviewer would defend the grouping and the divergence on the spec text alone. [INV-142, INV-140]
2. The system *shall* write a likely finding as one question to the human with both objects and each object's spec sentence, raised only *when* the shared role fits one plain sentence, the difference is a whole behaviour one member lacks, and no spec sentence already decides it. [INV-142, INV-141]

**Case: the batched channel and the held question**

3. The system *shall* ride these questions on the batched report, at most three per pass strongest first, holding a signal below that bar silent. [INV-142, E-22, INV-4]
4. The system *shall* not apply the recommended default to the spec the pack's usual proceed-on-recommended way, landing the class sentence only on the human's word while the lane never blocks. [INV-142, INV-4, INV-141]
5. *while* a question stands unanswered, the system *shall* hold it on the dated record and not raise it again on its own until the human answers, each pass first reading the open questions and dropping a freshly-derived divergence already carried there. [INV-142, INV-130]

---

## Requirement 238: A recorded decision names the exchange it came from

**Context:** Every claim in the pack stands on an artifact a reader can check. A human's word is the one input with no artifact behind it, and so the one claim no agent, prover, or gate questions — which makes it the one slot a fabrication, once placed there, is never reached again. So a sentence carrying human authority names the exchange it came from, and a claim the pack reasoned out is written in the pack's own voice, challengeable by everything that reads it.

**User Story:** As a person whose recorded decisions the pack quotes back, I want each one to name the exchange it came from while the pack's own reasoning stays in the pack's voice, so that a fabricated decision cannot hide in the one slot nothing challenges.

### Acceptance Criteria

**Case: authority names its exchange**

1. The system *shall* have a sentence set down as the person's decision name the exchange it came from, at minimum a marker a reader can go to and check in the profile's own style. [INV-207]
2. The system *shall* write a sentence the pack reasoned out for itself in the pack's own voice with no such attribution, challengeable by every agent, prover, and gate. [INV-207]
3. The system *shall* treat an autonomy grant as room to act that the agent owns as its own judgment, and *shall* never record it as a decision of the person's for the record to quote back. [INV-207]

**Case: the read-back surface and its gate**

4. The system *shall* show the person the decision-set record (`DECISIONS.md`), each entry naming its exchange, rendered so the person reads on the person's own clock and strikes what the person never said. [INV-207, INV-205]
5. *when* a live on-record entry in a decision-record surface carries no exchange, the system *shall* red the authority-anchor gate, a struck entry being skipped. [INV-207]

---

## Requirement 241: A parked question carries a recommended default

**Context:** When a question's value is the person's own input yet the work cannot wait on the person's free minute, the pack does not stall: the question is born onto the waiting board already carrying the default the work took, so the work proceeds on the recommendation and the person's free minute picks when to read it. A parked question with no default is a stalled question in a parked question's clothes.

**User Story:** As a person the pack would enjoy asking, I want a parked question born with the default the work already took, so that the work keeps moving and I answer at my own free minute rather than blocking the lane.

### Acceptance Criteria

**Case: the default travels with the question**

1. *when* the pack parks a question whose value is the person's input, the system *shall* place it on the waiting board already carrying the default the work took, and *shall* proceed on that recommendation. [INV-229, INV-4]
2. *when* a board item marked a parked question records no default, the system *shall* red the board gate, and *shall* pass a parked question naming its default. [INV-229]

**Case: an unanswered parked question keeps standing**

3. *while* a parked question stands unanswered, the system *shall* hold its default and record that the default stood unreviewed as a fact rather than an expiry. [INV-229, INV-206]
4. *when* a parked question is answered, the system *shall* route it through intake and close it, distinct from a decision an agent may not settle without the person. [INV-229, INV-152]

---

