## Requirement 11: A proven artifact settles a fork before the person hears it

**Context:** Before surfacing a design choice, a session checks whether an existing proven artifact — the architecture, the spec, the invariants — already determines the answer. When it does, the session derives the requirement and states it back with the section cited, offering no fork. A fork reaches the person only for what the artifacts leave genuinely open.

**User Story:** As a person asked only about real choices, I want a session to derive from a proven artifact whatever the artifact already settles, so that I hear a fork only for a taste call or a trade-off no document has decided.

### Acceptance Criteria

**Case: a settled fork is derived**

1. Before surfacing a design choice, the system *shall* check whether a proven artifact already determines the answer, and *when* one does *shall* derive the requirement and state it back with the section cited as its ground, offering no fork. [INV-121, INV-4]
2. The system *shall* raise a fork to the person only for what the artifacts leave genuinely open — a taste call, or a trade-off with no artifact-grounded winner. [INV-121]
3. The system *shall* apply this check as the design-fork sharpening of the pre-ask decide-or-verify gate. [INV-4, INV-81]

---

## Requirement 52: A feature is specified past what the human knows to ask

**Context:** The human says add a room where photos hang; the human does not say and decide what happens on a phone, because the human cannot know that is a question. So a feature-doored wish's spec-delta walks a fixed sweep of the standard facets — the dimensions every visible feature has whether or not anyone names them. The facet list has one home in the spec-author skill, and the inline list is its reader's echo.

**User Story:** As a person asking for a feature in plain words, I want its spec-delta to sweep the standard facets, so that the questions I did not know to ask — the phone layout, touch, the empty state — are each decided before the feature ships.

### Acceptance Criteria

**Case: the sweep runs the facet set**

1. *when* a wish's door says feature, the system *shall* walk its spec-delta through the standard facets — the viewport width and height bands, touch where the design assumed a mouse, the empty and error and loading states of each new surface, keyboard reach and readable contrast, the performance envelope, visual hierarchy, two windows at once, and a missing source. [T-13, INV-138]
2. The system *shall* end a layout-bearing feature's sweep with a decided or defaulted sentence per viewport band its layout law names or excludes, letting a law scoped to one band answer for the others. [T-13, INV-138]

**Case: the sweep's scope and the curated list**

3. The system *shall* scope the sweep to the feature's visible surfaces, satisfying a feature with none by one explicit sentence that no visible surface exists and the facets do not apply, never a silent skip. [T-13]
4. *when* a wish is re-doored to feature mid-work, the system *shall* walk the sweep before work resumes, and *shall* not sweep a fenced prototype, firing the sweep only when promotion makes it a feature. [T-13, INV-16, E-17]
5. The system *shall* keep the facet list in the spec-author skill as one closed enumerable set that grows a member only with a named real incident it would have caught, re-justified at milestones, naming every facet on its own line rather than letting any facet ride unnamed inside another's. [T-13, INV-226]

---

## Requirement 53: Every facet ends as a spec sentence

**Context:** A facet sentence is written one of two ways: decided, when the human or the walk's batched questions called it, or defaulted, when the recommended option is taken so the lane keeps moving. A defaulted sentence carries the literal tag `[default]` at its line end, and a facet with no sentence at all is a spec defect the prover flags.

**User Story:** As a person whose feature has many facets, I want each one written decided or defaulted rather than left silent, so that a later prover can tell a taken default from a hole and no facet ships as an unasked question.

### Acceptance Criteria

**Case: decided or defaulted, never silent**

1. The system *shall* write each facet as a decided sentence or a defaulted sentence tagged `[default]` at its line end, deriving the facet's test row either way. [INV-18, E-15]
2. The system *shall* never ask the human to confirm a default and never ping once per facet, since silence is consent and the human's veto becomes a new wish. [INV-18, INV-31]
3. *when* a facet has neither a decided nor a defaulted sentence, the system *shall* have the prover flag it a spec defect. [INV-18]

**Case: defaults on a live surface, and the split by time**

4. *when* a surface already lives, the system *shall* read a default from the shipped truth and reconcile it like any re-engineered claim, never inventing it against live behaviour. [INV-18, A-10, A-3]
5. The system *shall* let the facet sweep author the facet sentences when the feature is first specified and let the axis rule compose and test them across views once the surface exists. [INV-18, C-1]

---

## Requirement 54: The spec names its cross-cutting laws in one place, and every section answers them

**Context:** A product declares laws that cut across every surface — measurement, accessibility, error handling, a register of speech. The spec keeps that list in one declared-laws home, and each new surface's section states its line against each declared law before the prover reads it. Each declared law also names the net that enforces it.

**User Story:** As a person guarding a product-wide law, I want the laws listed in one home with each surface answering each and each law naming its net, so that a missing clause or a missing net ranks as a broken invariant.

### Acceptance Criteria

**Case: the declared-laws home and the per-surface answer**

1. The system *shall* keep the cross-cutting laws in one declared-laws home and *shall* have each new surface's section state its clause or a dated exemption against each declared law before the prover reads it. [INV-101]
2. The system *shall* have the prover's station enumerate every surface and transition per declared law and demand the clause or the dated exemption per item, ranking a missing clause a broken invariant. [INV-101]

**Case: this pack's declared laws and their nets**

3. The system *shall* declare this pack's three laws — the plain-language register on every human-facing surface, clock-honest stamps on every dated line, and no self-certification on any claim of done — each naming its mechanical gate. [INV-101, INV-28, INV-34, INV-83, INV-24, INV-94]
4. *when* a declared law names no net, the system *shall* rank the missing net a broken invariant, the same rank as a missing per-surface clause. [INV-101]

---

## Requirement 55: Every declared law names its enforcing net, and declaration moves a property to a blocking net

**Context:** A law that cuts across surfaces is enforced by one of three nets, and the law names which: a mechanical gate where a deterministic check can decide the violation, the prover's judgment station where the violation pins to a stated sentence, or the design review's recommendation where the deciding fact lives only in the person's intent. Declaration is the lever that moves a property between the nets.

**User Story:** As a person deciding how a law is enforced, I want each law to name one of three nets by where its violation can be decided, so that declaring a property promotes it from a soft recommendation to a blocking net with no property owned by two nets at once.

### Acceptance Criteria

**Case: the three nets and where each law belongs**

1. The system *shall* assign a law to a mechanical gate *when* a deterministic check can decide the violation, to the prover *when* the violation pins to a stated sentence, and to the design review *when* the deciding fact lives only in the person's intent. [INV-150, INV-125]
2. The system *shall* record each law's net beside it in the declared-laws home and *shall* rank a law with no named net a broken invariant. [INV-150, INV-101]
3. *when* a law is held at watch-level, the system *shall* name the design review as its net with a dated reason, so a watch-level choice reads as a deliberate decision. [INV-150]

**Case: declaration promotes and blocks**

4. *when* the author declares a grouping, a facet, or a law in the declared-laws home, the system *shall* move the property from the design review to the prover or a mechanical gate and start blocking on it, keeping the architecture's one-owner check as the backstop. [INV-150, INV-141]

---

## Requirement 56: Every incoming thing routes to the home whose declared sentence governs it

**Context:** The request classifier, the property net, the deferral test, and the earned message are one principle stated four times: every incoming thing routes to the home whose declared sentence governs it, and a thing that pins to no home is itself the finding. The four stay separate controls under the one principle because they run at different moments under different verifiers.

**User Story:** As a person handing the pack many kinds of thing, I want each routed to the home whose declared sentence governs it and a homeless thing made the finding, so that nothing is homeless by silence and declaration is the one lever across all four controls.

### Acceptance Criteria

**Case: each thing routes to its governing home**

1. The system *shall* route each thing to its own governing home. [INV-153, INV-151, INV-150, INV-152, INV-189]
   - a request, to the highest document whose sentences it changes;
   - a property, to the net that can pin its violation to a stated sentence;
   - a backlog item, to the seat, unless it names a fact only the human holds;
   - a question, to the sender's own blocked work.
2. *when* a thing pins to no home, the system *shall* make the thing itself the finding. [INV-153, INV-4, INV-101, INV-143, INV-191]
   - an unmatched request becomes a plain question;
   - a netless declared law becomes a broken invariant;
   - a held backlog item defaults to the seat;
   - a groundless question is dropped, with the holding named.

**Case: declaration is the lever, verified adjacent to each thing**

3. The system *shall* let declaration promote a property to a blockable check, a door or tripwire to a mechanical route, and named blocked work to a gate-readable message. [INV-153, INV-150]
4. The system *shall* verify each control adjacent to the thing it audits — the classifier by the landing's applied-or-stood-down contract, the property net by the declared-laws station, the deferral test by the seat's derive-before-defer posture, and the earned message by the receiving sweep's gate. [INV-153, INV-22, INV-101]

---

## Requirement 57: A feature is interrogated for how it fits the product

**Context:** The device facets ask what every visible feature owes; nobody has yet asked how this feature sits in the person's path. Path holes ship green because no clause ever promised the way out. So a feature-doored wish's spec-delta also walks the fit walk, scaled to the wish's kind, and the prover gains the matching focused mode, feature-fit.

**User Story:** As a person adding a feature, I want its spec-delta walked for how the person arrives, acts, and moves on, so that a path hole with no way out is caught at intake, before it ever ships green.

### Acceptance Criteria

**Case: the fit walk, scaled to the kind**

1. *when* a wish enters the feature door, the system *shall* walk its spec-delta through the fit walk scaled to its kind — a product wish through the visitor's journey, an infra wish through its flows, a skill wish through trigger, correction, and when not to fire. [INV-29]
2. The system *shall* interrogate the feature and not the person, deriving each answer from the existing spec and the shipped truth first. [INV-29]

**Case: holes closed, defaulted, or asked**

3. *when* a hole is trivially closable — its answer pins to an existing artifact: a base rule, a spec sentence, the architecture, or an already-answered decision — the system *shall* close it and write the closing down, writing the rest decided or `[default]`-tagged and sending only genuine taste calls out in a batch. [INV-29, INV-4, INV-18]
4. The system *shall* give the prover the feature-fit mode that walks the journey seams against the whole spec, and *shall* owe a landed feature its walk at the first landing that touches it rather than retroactively. [INV-29, INV-159]

---

## Requirement 58: A face that can be entered once owes a way back or a written one-way

**Context:** A surface's faces get entered under conditions — a first-visit door, an empty state, an onboarding screen, a one-time banner. A face whose condition can never re-arise is a dead end the state lenses miss. Trigger wording is the tell: only on first visit, only on first run, until dismissed.

**User Story:** As a person who can leave and re-enter a surface, I want every conditionally-entered face to state its re-entry path or name its one-way, so that a face reachable again always says how it is reached.

### Acceptance Criteria

**Case: the return sentence or the written one-way**

1. The system *shall* have every conditionally-entered face state its deliberate re-entry path or state the one-way as a decision by name. [INV-50]
2. *when* a face carries trigger wording such as only on first visit or until dismissed, the system *shall* owe that clause its return sentence and have the prover read for it through the entry-symmetry lens. [INV-50, INV-29]

---

## Requirement 59: Verify-by-deed walks the visit and judges the feel

**Context:** For the product kind, the verify step includes a named visitor walk: the whole journey as the person will live it. The agent walks the first visit, the return visit, entry through another door, where am I and how do I move on from any point, and the exits. The agent also runs a feel pass against the approved prototype as the bar, in the form the medium actually has.

**User Story:** As a person shipping a product feature, I want verify to walk the visit and judge the feel against the prototype, so that shipped work is checked the way a person actually lives it and findings become rows or red rather than a mental note.

### Acceptance Criteria

**Case: the visitor walk and the feel pass**

1. *when* the verify step runs on a product-kind wish, the system *shall* walk the first visit, the return visit, entry through another door, where the person is and how they move on from any point, and the exits. [INV-30]
2. *when* the feel pass runs, the system *shall* judge motion quality and each affordance's craft against the approved prototype as the bar, turning findings into rows or red. [INV-30, E-17]

**Case: the walk runs in the medium's own form**

3. The system *shall* run the walk in the form the medium has — motion and affordance for a browser, reading path and chapter flow for a book, the command round-trip for a command-line tool — reading its checklist from the build-pipeline product cell. [INV-30, E-12, INV-22]

---

## Requirement 60: The prover labels each finding a defect or a recommendation

**Context:** Every prover finding carries its kind, so the human knows at a glance what the finding asks of them. A defect blocks and the design becomes buildable only once it is folded; a recommendation does not block and queues for a taste call. The kind is derivable from the finding's own ground.

**User Story:** As a person reading prover findings, I want each labelled a defect or a recommendation, so that I sort what blocks from what queues at the point of report rather than by hand.

### Acceptance Criteria

**Case: the two kinds and their verdicts**

1. The system *shall* label a finding a defect *when* it names a violated invariant, a false spec claim, or a missing required invariant, blocking until it is folded. [INV-140]
2. The system *shall* label a finding a recommendation *when* nothing stated is broken and nothing required is missing, queuing it for a taste call with an optional now-or-later grade. [INV-140]

**Case: the gate folds and queues**

3. The system *shall* have the push gate fold every defect and queue every recommendation, deriving the kind from the finding's own ground. [INV-140, M-6]
4. *when* a delta-scoped gate meets a pre-existing defect outside the delta, the system *shall* queue it by that law rather than block the merge it did not create. [INV-140, INV-114]

---

## Requirement 61: A design review reads a proven spec and judges the design behind it

**Context:** After the prover has checked a spec, a separate pass called the design review reads the same spec and judges its design. It builds its own transient inventory of every element a person acts on, writes one plain sentence of what the person does with each, and proposes elements whose sentences match as a same-kind group. Its findings are recommendations or questions and never block a landing.

**User Story:** As a person guarding design consistency, I want a design review to group the elements a person acts on and check each group for behaviour parity, so that same-kind things behave alike and a divergence is brought to me with two concrete objects in hand.

### Acceptance Criteria

**Case: the inventory and the same-kind groups**

1. *when* the prover has checked a spec, the system *shall* have the design review read the same spec, build its own transient inventory of every element a person acts on that a spec sentence names, and write one plain sentence of what the person does with each in the person's own action words, never writing that inventory into the surface list the host authors. [INV-141, E-10]
2. The system *shall* propose elements whose sentences match as a same-kind group, check each group for the same gestures, transitions, and affordances, and stay silent where the grouping or the difference is not plain. [INV-141]

**Case: findings recommend or ask, never block**

3. The system *shall* name two concrete objects with the spec sentence each comes from on every finding, produce no blocking defects, and write a dated record with a per-finding outcome column. [INV-141, INV-140]
4. *when* the human confirms two elements are the same kind, the system *shall* have the spec author write a class sentence the existing checks then hold, and *when* the human says they differ by intent, *shall* write a decided sentence that closes the question. [INV-141, INV-125, INV-59]

**Case: the review runs in the kind's own form**

5. *when* a kind has no element a person acts on, the system *shall* stand the design review down by name in the record rather than run it vacuously. [INV-141, INV-22, INV-125, INV-30, INV-136, INV-139]
6. The design review *shall* run in the project kind's own form, the way the verify walk and the design principles do. [INV-141, INV-136]
7. The spec's own declared-class check *shall* keep governing *where* a class is already declared. [INV-125]

---

## Requirement 62: A gesture or overlay spec triggers the design review's motion-parity lens

**Context:** The bottom-up similarity lens builds its groups from matching role sentences, so it can miss a same-kind grouping the medium makes obvious. A spec that ships a gesture, a motion, or a layer that opens and closes over another carries a standing lens the design review runs by construction, naming three same-kind groups the text need not have declared.

**User Story:** As a person shipping a gesture or overlay, I want the design review's motion-parity lens run by construction, so that the way out mirrors the way in, every object type behaves alike, and every slot behaves alike before a device ever shows a divergence.

### Acceptance Criteria

**Case: the three same-kind groups**

1. *when* a spec ships a gesture, a motion, or a layer that opens and closes over another, the system *shall* run the motion-parity lens by construction, naming entry-mirrors-exit as the first group so a layer closes by the reverse of the motion that opened it. [INV-165, INV-141]
2. The system *shall* name every object type the gesture acts on as the second group, and every position as the third group. [INV-165]
   - in the second group, each kind opens and closes the same way and lands back on its own on-screen rectangle;
   - in the third group, the same gesture on the same type in a different slot behaves the same.

**Case: each finding recommends or asks**

3. The system *shall* make each motion-parity finding a recommendation or a question and never a blocker, holding it by the prover's uniformity check once the human declares the parity a class sentence. [INV-165, INV-125]

---

## Requirement 63: A feature delta adding a second member of a kind draws the scoped design review at intake

**Context:** The moment an undeclared same-kind grouping comes into existence is the intake of its second member: the first member ships alone with no class to belong to, so when a delta adds a sibling the uniformity check has no class clause to hold and the full design review is not due until the next milestone. Feature intake therefore carries one standing question the feature-fit walk asks by construction.

**User Story:** As a person adding a sibling to an existing kind, I want the scoped design review drawn at intake, so that the window where a second sibling ships and diverges before the next full pass is closed.

### Acceptance Criteria

**Case: the second-sibling question**

1. *when* a feature delta adds a second member of a kind an existing surface already has — the same gesture, overlay shape, or one-sentence role — the system *shall* draw the scoped design review over the delta's elements against the existing inventory. [INV-169, INV-141]
2. *when* a delta adds no such sibling, the system *shall* hold the intake stand-down and record the no as a lens verdict in the feature-fit record. [INV-169, INV-29]

**Case: the closed window**

3. The system *shall* close the window a second sibling entered by drawing this pass at intake, the same channel the uniformity lens and the motion-parity lens were born from. [INV-169, INV-125, INV-165]

---

## Requirement 64: A re-enterable surface triggers the prover's entry-state lens

**Context:** The prover reasons in states, transitions, and initialization, so a surface a visitor can leave and re-enter carries a standing lens the prover runs by construction. The entry-symmetry lens tests that a re-entry path exists; this lens tests the state that re-entry opens in.

**User Story:** As a person shipping a re-enterable surface, I want the prover's entry-state lens run by construction, so that a spec pinning the open, exit, and guards while leaving the entry position and reset-or-resume blank raises an open question before code.

### Acceptance Criteria

**Case: the entry state the lens demands**

1. *when* a surface can be left and re-entered, the system *shall* have the prover demand the spec declare where the surface opens focused or positioned and whether entering resets its internal state or resumes the state a prior visit left. [INV-167, INV-1]
2. *when* the spec pins the open ceremony, exit, variants, and guards while the entry position and reset-or-resume semantics stay blank, the system *shall* raise the unstated transition end-state as an open question before any code is written. [INV-167, INV-50]

**Case: the lens hands off once declared**

3. *when* the human declares the entry state a spec sentence, the system *shall* let the prover's ordinary state-coverage hold it. [INV-167, INV-125]

---

## Requirement 65: Every stated transition carries a payload lens

**Context:** The prover verifies the state graph's topology — that a way in, a way out, and a way back exist. Beside topology it reads each transition's payload: the parameters a person perceives across it. A parameter the spec leaves blank is answered by the platform's own default alone, so the payload a transition carries is the hole the topology lenses miss.

**User Story:** As a person specifying a transition, I want each one's perceived payload enumerated and demanded, so that a parameter left to the platform default becomes a finding, surfaced before it can silently become the behaviour.

### Acceptance Criteria

**Case: enumerate and demand each payload parameter**

1. *when* the prover reads a stated transition, the system *shall* enumerate the parameters a person perceives across it — where focus and selection land, what scroll or playback position holds, whether sound continues, whether a timer keeps running, whether a shown value is fresh or stale — and demand the spec name each. [INV-168, INV-72, INV-127]
2. The system *shall* raise each unstated payload parameter as an open question, the author writing it as a spec sentence or the human deciding it where the choice is theirs alone. [INV-168, INV-30]

**Case: the lens generalizes its instances**

3. The system *shall* read the motion-parity lens as this lens on the exit's animation and the entry-state lens as this lens on a re-entry's internal state, both instances this parent generalizes. [INV-168, INV-165, INV-167]

---

## Requirement 66: A surface add re-verifies the document's quantified claims

**Context:** A new surface falsifies existing document-level sentences without touching them: a class clause's member enumeration excludes the newcomer, a sentence quantified over every, only, all, or exactly one ranges over a set that just grew, and a previously terminal scenario's decided edge may no longer be terminal. A seam-scoped pass misses these, so the cross-link mode carries one mandatory whole-document step.

**User Story:** As a person adding a surface or a member, I want the document's quantified claims re-verified against the grown set, so that a sentence the newcomer falsifies is a finding at the add itself, ahead of the next full pass.

### Acceptance Criteria

**Case: the quantifier re-verify**

1. *when* a surface is added, the system *shall* have the cross-link mode sweep the document for enumerations and universal quantifiers, and re-verify each such sentence against the surface set that now includes the newcomer. [INV-170, INV-125, INV-127]
   - the quantifiers it sweeps for are every, only, all, and exactly, and the enumerations are the explicit member lists.
2. The system *shall* fire the step on every member add, and *shall* re-verify the same way in the full pass's own sweep. A surface add is one kind of member add. [INV-170, INV-169, INV-171]
   - a member add covers a new invariant joining a family, a new skill joining the pack, and a second sibling the intake question catches.

---

## Requirement 67: A full prover pass owes a coverage record

**Context:** Phase-level prose proves nothing about which lenses actually ran, and on a kind where the classic coverage tables all go not-applicable a skipped lens is indistinguishable from a lens that found nothing. The prover's stress lenses therefore split into three tiers. Each mandatory sweep owes one verdict line, and the imaginative probes owe none. The class lens is the third tier, the standing sweep that owes one record line every pass.

**User Story:** As a person trusting a full prover pass, I want each mandatory sweep to owe one verdict line rendered as a surface-by-sweep table, so that a missing verdict reads as a skipped sweep, its absence never passing for a clean one.

### Acceptance Criteria

**Case: the mandatory sweeps owe verdicts**

1. The system *shall* have each mandatory sweep — the declared-laws walk, edge-condition completeness, cross-surface uniformity, the lifecycle sweep under the transition-payload parent, and the unwritten-seams derivation — owe one verdict line in the persisted record: hit, clean, or not-applicable with its reason. [INV-171, INV-101, INV-138, INV-125, INV-168, INV-50, INV-167, INV-126, INV-127, INV-72]
2. The system *shall* render the verdicts as a surface-by-sweep table, the replacement for the coverage tables on a kind where those go not-applicable, and leave the imaginative probes — the checks the prover invents for the particular document beyond the mandatory sweeps — discretionary owing no verdict. [INV-171, INV-135, INV-156]
3. *when* a verdict line is missing, the system *shall* read it as a skipped sweep and never as a clean one. [INV-171]

**Case: the class line the record carries**

4. The system *shall* have every pass write one class line in its record, beneath the verdict table. The line *shall* read swept with the classes filed, no class, or not-applicable with its reason. [INV-171, INV-124]

---

## Requirement 68: Every review pass writes its record of one class

**Context:** A review pass — the prover's spec re-check, the design review, the periodic adversarial audit (the fresh-checker read run over a high-stakes delivery, set on refuting its claims and finding its holes; its cadence and rules live in the rules section of this document), and the verify-by-deed audit — records its outcome so a later session reads every pass the same way. Three of them write a dated file of one shared shape under the pass's own home, and the verify-by-deed audit is the one deliberate difference.

**User Story:** As a later session reading past passes, I want each review pass to write its record of one class with a per-finding disposition column, so that the prover, the design review, and the audit read the same way and the verify audit's difference is named.

### Acceptance Criteria

**Case: the shared record shape**

1. The system *shall* have the prover, the design review, and the periodic audit each write a dated file of one shared shape under its own home. [INV-156, INV-140, INV-141, INV-145]
   - the file names the skill and version that ran the pass;
   - it carries a per-finding disposition column;
   - it takes a same-day suffix so two passes never overwrite.
2. The system *shall* land a feature-fit record in the prover's own home in this shape, and give the design review alone a held-ask home since it alone carries a question across passes. [INV-156, INV-29, INV-169, INV-142]

**Case: the verify audit's difference, and forward binding**

3. The system *shall* land the verify-by-deed audit's verdict and its per-landing skill-creator review in the landing record, since verify is a per-landing gate and keeps no dated file of this class. [INV-156, INV-46, INV-99]
4. The system *shall* have a new review pass state its record against this class and *shall* leave records written before the class was declared unreshaped. [INV-156, INV-159]

---

## Requirement 70: The prover and the design review iterate to a bounded fixed point

**Context:** The prover and the design review form a loop over repeated rounds. A round is one prover re-read of the changed part of the spec followed by one design-review re-read over the current spec. Only a human-accepted declaration advances the loop, and it is capped at three progressing rounds by default. On reaching the cap the loop surfaces the unsettled groupings without holding the landing.

**User Story:** As a person watching the design settle, I want the prover and design review to iterate to a bounded fixed point and surface non-convergence without holding the landing, so that a design converges in the ordinary case and a live cap keeps the loop from running away.

### Acceptance Criteria

**Case: what advances the loop**

1. The system *shall* advance the loop only on a human-accepted declaration — a class sentence over a grouping or a decided sentence over a difference — re-reading the changed part and the re-partitioned elements in the next round. [INV-154, INV-125, INV-59]
2. The system *shall* not advance the loop on a confident finding queued as a recommendation or a likely finding riding as a question, since neither re-reads the spec on its own. [INV-154, INV-142]

**Case: the loop rests with a named reason**

3. *when* a round produces no new class sentence and no new decided sentence, the system *shall* rest the loop and name why in the record — it converges when the design review left no open question and no new grouping, it waits when a question stands unanswered, and it stands down when no element a person acts on exists. [INV-154, INV-141, INV-142]

**Case: the cap and the surfacing**

4. The system *shall* cap the loop at three progressing rounds by default, let a host set its own cap, and count progressing rounds on the design-review pass alone, resetting when a fresh pass opens. [INV-154]
5. *when* the loop reaches the cap without convergence, the system *shall* surface the unsettled groupings on the dated record with its best reading of the cause, and *shall* let the landing proceed with the unsettled groupings recorded. [INV-154, INV-141]

---

## Requirement 71: A taste choice made without asking is told, never confirmed

**Context:** While building a feature, the walk makes small taste calls itself so the lane keeps moving — an animation's speed, a button's shape, a caption's wording. The agent writes each into the spec with its `[default]` tag, names it in the delivery report, and re-asks nothing later.

**User Story:** As a person whose feature carries small taste calls, I want each one told in plain words with an example and marked tweakable rather than confirmed, so that the lane keeps moving and every such choice stays findable.

### Acceptance Criteria

**Case: told with an example, marked tweakable**

1. *when* the walk makes a taste call without asking, the system *shall* write it into the spec with its `[default]` tag and name it in the delivery report in plain words with an example, marked tweakable. [INV-31, INV-18]
2. The system *shall* request no confirmation and re-ask nothing later, since silence is consent, and *shall* keep every such choice findable by its `[default]` tag so the person can ask when they want it changed. [INV-31]

---

## Requirement 72: A tunable parameter is set to a default and told, never asked

**Context:** Some choices are a mechanical knob with a range — an image's resolution, a batch size, a timeout, a sampling rate. The walk sets each knob itself and keeps the lane moving, writing it with its `[default]` tag and naming what it trades in the delivery report.

**User Story:** As a person whose feature carries tunable knobs, I want each set to a default and reported with what it trades rather than asked, so that the agent never stalls on a knob it can set and I tune it afterward only if I want a different point.

### Acceptance Criteria

**Case: set, tagged, and told**

1. *when* the walk meets a tunable knob, the system *shall* set it to a default value, choosing the cheaper or faster point wherever quality allows, write it with its `[default]` tag, and name in the delivery report what it trades. [INV-70, INV-31, INV-18]
   [GAP: the quality bar that permits the cheaper point is unstated in the source.]
2. The system *shall* owe no re-ask, letting the human tune the knob afterward and updating it together at most, the same idea the economy ladder applies to cost. [INV-70] [T-19]

**Case: the agent moves every task it can**

3. The system *shall* move every task it can and reserve a question for what it genuinely cannot decide. [INV-70, INV-4]
4. *where* the human has granted it, the system *shall* ship to production on its own certification once the work is sound, keeping the grant the human's to give or withdraw. [INV-70, M-6, INV-9]

---

## Requirement 73: The smallest sample is judged before the full artifact

**Context:** For a taste-heavy deliverable — voice, copy, visual style, spec prose — the build stops at the cheapest judgeable sample: one paragraph, one card, two sections. The human's word on that sample sets the bar before the full build spends anything. This is the agent's own discipline, distinct from a declared show-me-first entry condition.

**User Story:** As a person whose deliverable is taste-heavy, I want the smallest judgeable sample put before me before the full build, so that my word sets the bar before the full build spends anything.

### Acceptance Criteria

**Case: the cheapest judgeable sample first**

1. *when* a deliverable is taste-heavy, the system *shall* stop the build at the cheapest judgeable sample — one paragraph, one card, two sections — and take the human's word on that sample before the full build spends. [INV-62]
   [GAP: the boundary classifying a deliverable as taste-heavy is unstated in the source; the source names examples (voice, copy, visual style, spec prose) and no closed test.]
2. The system *shall* build smallest first as the agent's own discipline even unasked, distinct from the human's declared show-me-first entry condition. [INV-62, INV-43]

---

## Requirement 74: A rejected artifact reopens its source

**Context:** When the human rejects an artifact, the fix starts at the artifact's source — the spec clause, the card, or the brief that produced it. Patching the rejected output line-by-line against an unchanged source is the five-round trap by name, and it is banned.

**User Story:** As a person rejecting an artifact, I want the fix to reopen its source and rebuild from it, so that the correction lands at the root rather than looping the same rejection against an unchanged source.

### Acceptance Criteria

**Case: correct the source, rebuild from it**

1. *when* the human rejects an artifact, the system *shall* correct its source — the spec clause, the card, or the brief — first and rebuild the artifact from it. [INV-63]
2. The system *shall* ban patching the rejected output line-by-line against an unchanged source, the five-round trap by name. [INV-63]

---

## Requirement 75: What already works is fenced before it is touched

**Context:** When a feature-doored wish touches a surface that already lives, its spec-delta opens with regression fences before the facet sweep authors anything new. A fence is one sentence for a neighbouring promise that must stay true through the change, citing the existing clause it guards. The delta splits everything it touches in two: promises that stay are fenced and untouched, behaviour being changed is re-authored as new law.

**User Story:** As a person changing a live surface, I want its neighbouring promises fenced and cited before anything new is authored, so that fixed one thing and quietly broke the neighbour turns red before it ships.

### Acceptance Criteria

**Case: the fence and what it guards**

1. *when* a feature-doored wish touches a surface that already lives, the system *shall* open its spec-delta with regression fences before the facet sweep authors anything new, each fence one sentence for a neighbouring promise that must stay true and citing the existing spec clause it guards. [T-14]
2. The system *shall* earn no new test-matrix row for a fence, discharging it through the cited clause's own never-side and proving the fence held by the landing's full-suite run. [T-14, INV-19, INV-6]

**Case: an unwritten promise, and where fencing belongs**

3. *when* a fence finds no clause behind it, the system *shall* reconcile the discovered promise from the shipped truth like an adopted claim, write it as its own spec fact with its own row, and surface it rather than silently assume it. [T-14, A-3, INV-5]
4. The system *shall* name the wish's fences by the anchors they cite in the queue row, keep fence-authoring to the feature door, let the bug and refactor doors inherit only the catching, and fence nothing on a prototype since it promises nothing. [T-14, T-7, E-17]

---

## Requirement 76: A feature says its non-goals and its success measure

**Context:** Every feature's spec-delta closes with two short sentences, both always written: the non-goals, what is deliberately left out, and the success measure, how the feature's working would be noticed for its person. A non-goal that narrows what the wish asked for is a scope decision, and a success measure derives no test-matrix row.

**User Story:** As a person closing a feature's spec, I want its non-goals and its success measure both written rather than left silent, so that what the feature excludes is on the record and how we would notice it worked is a written promise.

### Acceptance Criteria

**Case: the two sentences, always written**

1. The system *shall* close every feature's spec-delta with a non-goal sentence and a success-measure sentence, both always written, taking nothing deliberately left out this time as a valid non-goal and reading only a missing sentence as a hole. [INV-20, INV-21]
2. *when* a non-goal narrows what the wish asked for, the system *shall* ride it on the batched report as a stated scope decision. [INV-20, INV-4, INV-5]

**Case: the success measure carries no row**

3. The system *shall* write the success measure decided or `[default]`-tagged with a number where one exists, derive no test-matrix row from it, and keep it a written promise the human checks by eye until the reading machinery ships. [INV-21, INV-18]
4. The system *shall* bind both sentences forward from features specified after this rule, owe an adopted feature its pair at the first landing that touches it, and write neither on a prototype. [INV-20, INV-21, A-3, E-17, INV-159]

**Case: the reading machinery is promised**

5. The system *shall* keep the success-measure reading machinery promised under its own queue row. [INV-21]
   [target]

---

## Requirement 99: The door step decides a feature from a sketch

**Context:** The boundary between a feature and a sketch sits at the door step, the point where a request becomes a product feature. A wish to have something in the product is a feature and walks the pipeline; a request to merely see or try something, with no commitment, may live as a sketch inside the fence. When the door is unclear, the agent asks rather than guesses.

**User Story:** As a person voicing a request, I want the door step to sort a feature from a sketch by a fixed rule, so that a commitment gets a spec and a lane while a no-commitment try stays a free sketch.

### Acceptance Criteria

**Case: the boundary at the door**

1. *when* a wish asks to have something in the product, the system *shall* read it as a feature and route it through the build pipeline. [INV-16]
2. *when* a request asks only to see or try something with no commitment, the system *shall* let it live as a sketch inside the fence, carrying no lane through the build pipeline and no spec. [INV-16, E-17]

**Case: the unclear door asks**

3. *if* which of the two was meant is unclear, *then* the system *shall* ask one plain question and *shall* not guess. [INV-16]

---

## Requirement 100: Opening a prototype home is a repo write

**Context:** A prototype home is a folder or branch, and creating it writes to the repository like any other write. So the write-ownership law governs it, the assigned seat makes the judgment call, and a session working from outside files an inbox wish rather than opening the home itself.

**User Story:** As a maintainer of the repository, I want opening a prototype home held to the write-ownership law, so that a worker never opens a prototype home on its own brief and an outside session routes through the inbox.

### Acceptance Criteria

**Case: the write is owned**

1. *when* a prototype home is opened, the system *shall* govern that write by the write-ownership law and *shall* leave the judgment call to the assigned seat. [INV-10, ACT-2]
2. *when* a session works from outside the assigned pack session, the system *shall* have it file an inbox wish rather than open a prototype home on its own brief. [INV-10]

---

## Requirement 101: Promotion enters a sketch's earned feature at the spec step

**Context:** When a sketch earns its place, its feature enters the pipeline at the spec step like any wish, without its code being merged. The prototype serves as evidence for that spec, and its code holds no rights.

**User Story:** As a person promoting a proven sketch, I want its feature to enter at the spec step with the code left behind, so that the earned idea is specced fresh and the sketch's code claims nothing.

### Acceptance Criteria

**Case: the earned feature is specced fresh**

1. *when* a sketch earns its place, the system *shall* enter its feature at the spec step like any wish and *shall* not merge the sketch's code. [T-12, INV-16]
2. The system *shall* treat the prototype as evidence for that spec, its code holding no rights. [T-12]

---

## Requirement 102: The fence guardrail's three legs and the header's honesty

**Context:** A guardrails check enforces the one-way fence, and it has three legs. One leg runs live today; two are promised targets. When all three land, the header's honesty rule holds in both directions — the spec never claims what is not built, and the build never contains what the spec does not name.

**User Story:** As a person trusting the fence, I want a mechanical check with three named legs and one honest note of which run today, so that a prod file reaching into a prototype turns red while the promised legs are marked as still owed.

### Acceptance Criteria

**Case: the three legs**

1. *when* a prod file references anything inside a prototype home, the system *shall* turn the fence leg red. [E-6]
2. The system *shall* enforce the completeness scan over the surface registry and the behaviour-traces-to-spec check as the two remaining legs. [E-10, E-6]
   [target]

**Case: the honesty in both directions**

3. *when* all three legs land, the system *shall* hold that the spec never claims what is not built and the build never contains what the spec does not name. [S-0, INV-17]
4. *while* only the fence leg is enforced, the system *shall* keep the other two legs promised, marked, and owned by their rows. [INV-17]
   [target]

---

## Requirement 103: An approved look is frozen as the norm its clause cites

**Context:** Prose alone cannot record how a design looks and feels, so a rebuild made from prose with no artifact to check against can pass every test and still ship a look-alike. Once the human approves a sketch as the look, that prototype becomes the norm for look and feel. The clause it governs cites the frozen artifact, and approval freezes a dated copy into the project's records.

**User Story:** As a person who approved a look, I want the approving clause to cite a frozen copy of the artifact, so that a later rebuild is checked against the frozen artifact itself.

### Acceptance Criteria

**Case: the clause cites its artifact**

1. *when* a clause is governed by an approved look, the system *shall* place a norm pointer of the form `norm: <path>` at the clause's line end beside its anchors, the prose carrying the laws and the artifact keeping the look. [INV-43]
2. *when* a sketch is approved as the look, the system *shall* freeze a copy into `docs/norms/` with a dated provenance line naming what it is, when it was approved, and which sketch it came from. [INV-43]

**Case: the pointer never reaches a live sketch**

3. The system *shall* have the norm pointer cite the frozen copy and *shall* never let it reach into a live prototype home, so the one-way fence stays absolute and the sketch stays free to die. [INV-43, E-17, INV-17]

---

## Requirement 104: The build and the prover read the norm

**Context:** A norm is only as good as the reads that enforce it. When a surface's clauses carry a norm pointer, the build opens the artifact before writing code and records a plan-versus-prototype diff; the verify feel pass reads the same pointer; and the prover reads visual clauses with a norm lens. A story may also demand the human see a mockup before the build starts.

**User Story:** As a person guarding an approved look, I want the build, the verify pass, and the prover all reading the norm pointer, so that a missing line is caught at the code step and a pointerless prototype-born clause is flagged.

### Acceptance Criteria

**Case: the build reads the artifact**

1. *when* a surface whose clauses carry a norm pointer is built, the system *shall* open the artifact before the code step and *shall* record a one-line plan-versus-prototype diff in the delivery report, a missing line being a defect caught at the code step. [INV-43]
2. The system *shall* have the verify step's feel pass read the same norm pointer. [INV-43, INV-30]

**Case: the prover's norm lens**

3. *when* the prover reads a visual clause, the system *shall* flag a prototype-born clause carrying no pointer, and *shall* flag a clause whose text contradicts its own artifact. [INV-43]

**Case: the mockup-first entry condition**

4. *when* a story declares a mockup-first requirement, the system *shall* write `entry: mockup-first` on the queue row and *shall* hold it at the door step until the human cancels it by name. [INV-43]
   - a mockup-first requirement is the human needing to see a mockup before the build starts;
   - a general instruction to build moves priority without cancelling this entry.

**Case: the pointer binds forward only**

5. The system *shall* add a clause's pointer at the first landing that touches it and *shall* never apply pointers retroactively across the whole spec at once. [INV-43, INV-159]
6. The system *shall* place a pointer only for a prototype the human approved as the look, leaving an unapproved sketch as plain evidence in its fence and a text-born clause with no pointer. [INV-43, E-17]

---

## Requirement 214: An expensive decision earns an adversarial read before it lands

**Context:** A decision is expensive when unwinding it costs more than making it did, and the pack's expensive decisions are a closed, enumerable set: the birth of a new agent, a node carved or merged in the architecture, the shape of a contract once a consumer has pinned it, a project's kind, the split of a reusable product into engine and instance, and a repository going public. No machine tells an expensive decision from an ordinary one, so the duty is stated for the whole class and each member carries it at its own decision point as the pack wires it. The read is a fresh-context independent audit that closes by bringing the decision to the human with findings and a recommendation.

**User Story:** As a person owning the taste call on a costly decision, I want each expensive decision to earn a fresh adversarial read that reaches me with findings and a recommendation, so that the call rests on a case already broken and tested.

### Acceptance Criteria

**Case: the class is closed and enumerated**

1. The system *shall* treat the expensive-decision set as closed and enumerable, naming every member as either enumerated on its own row or riding inside another row's work. [INV-235, T-22, INV-113, INV-122, INV-187, INV-36, INV-85, INV-44, INV-226]
   - the set holds: an agent's birth, a node carved or merged, a contract's shape once a consumer pinned it, a project's kind, an engine-and-instance split, and a repository going public.
2. The system *shall* state the duty for the whole class and have each member carry it at its own decision point, a traceability test holding that this clause names the read and that agent birth carries it; that test *shall* ride the suite and take no push-gate letter, since no gate reads a reversal cost, the far-tier and node-growth checks the precedent. [INV-235]

**Case: the read is adversarial and closes with the human**

3. *when* an expensive decision is about to land, the system *shall* run a fresh-context independent audit at the best tier the pack's quality habit sets, set on breaking the case as the verify audit reads a delivery. [INV-235, INV-46, INV-145]
   [GAP: the read runs at the best tier the pack's quality habit sets, but the source neither defines that quality habit nor states which tier it yields for this read, so the read's out-of-box model tier is unstated.]
4. *where* the decision turns on whether members are one kind, the design review *shall* read the grouping with the two compared objects in hand. [INV-235, INV-141, INV-142]
5. The read *shall* close by bringing the decision to the human with its findings and a recommendation, the taste call staying the human's because it needs a fact only the human holds. [INV-235, INV-143, INV-152]

---

## Requirement 215: The authoring seat does not certify its own work

**Context:** The seat that authored a change drafts and accepts it but never provides its own adversarial certification, since a head marinated in the authoring context is blind to the gap it just wrote. Two carriers follow. A release's adversarial pass — the full prover re-prove at the release gate — is authored by a fresh, differently-contexted seat, and a newly added lens or rule is applied to the very document that introduces it before release. The release gate may require a dated clean-context review record naming a seat other than the release's.

**User Story:** As a person trusting a release, I want its adversarial pass run by a fresh seat and every new rule applied to its own introducing document, so that an authoring-blind gap is caught by a differently-contexted head before the release ships.

### Acceptance Criteria

**Case: the author drafts but does not certify**

1. The system *shall* let the authoring seat draft and accept a change and *shall* never let it provide the change's own adversarial certification. [INV-237]
2. The system *shall* author a release's adversarial pass — the full prover re-prove at the release gate — with a fresh, differently-contexted seat under the freshness the verify audit already defines. [INV-237, INV-116, INV-217, INV-46, INV-145]

**Case: a new rule is self-applied and the record names a fresh seat**

3. *when* a release is prepared, the system *shall* apply a newly added lens or rule to the document that introduces it and *shall* name the result in the release record. [INV-237]
4. The release gate *shall* be able to require a dated review record that exists, is dated to the release, and names a seat other than the release's. [INV-237]

---

## Requirement 258: Every stateful surface is reviewed against a floor of composition axes

**Context:** Some parts of a host project hold state — a screen, a panel, a saved file the user can change and find again later. Each is a stateful surface. Every stateful surface is reviewed against a set of composition axes, each axis one question about the surface's behaviour. A floor of axes holds for every stateful surface whatever its project's kind. The axis a reviewer skips most is the last one, the presence of every other live surface: a caption still naming the previous photo once the closing screen arrives is the classic stranding hole, because the caption's behaviour with the finale in view was never written as a sentence.

**User Story:** As a person composing a surface, I want a fixed floor of axes every stateful surface answers and one stated shape for the whole axis set, so that no kind-independent angle of its behaviour is left unreviewed and a reader knows when the surface's spec is complete.

### Acceptance Criteria

**Case: the kind-independent floor**

1. The system *shall* review every stateful surface against the floor axes: its behaviour in each view, in each mode, at each user tier, at each viewport size, when it is closed and reopened, and under two writers that can act on it at once. [C-1]
2. The system *shall* include in the floor the surface's behaviour alongside every other surface that can be present at the same time — a sibling sharing the screen, or a surface the flow reaches one step before or after it — whether or not that other surface holds state. [C-1]

**Case: the seam beside each other live surface**

3. The system *shall* state, for each other live surface present with this one, what this surface does while that one is present — whether it holds, clears, or hands off. [C-1, INV-72]

**Case: the axis set declares its own shape**

4. The system *shall* read the axis set as a hybrid whose shape it declares: the floor is an enumerated set every stateful surface answers, and the kind-owed tail is an open set whose members a kind names one at a time. [C-1, INV-226]
5. The system *shall* read a surface's spec as complete only once every floor axis and every axis its kind owes has an answer. [C-1, INV-244]

---

## Requirement 259: The prover hunts the situation the author never wrote

**Context:** The prover reads the whole axis list actively and derives each surface's reachable situations for itself, rather than trusting the author to have filled every one. A reachable situation the spec leaves blank is the exact hole a running product still reaches, and the prover reports it and leaves the sentence to the author.

**User Story:** As a person relying on a spec to cover what the product reaches, I want the prover to derive each surface's reachable situations and flag every blank one, so that a state the product can reach but the spec never wrote is caught before a user meets it.

### Acceptance Criteria

**Case: derive the reachable situations**

1. *when* the prover reads a stateful surface, the system *shall* walk every axis. [INV-72, C-1]
   - the axes are the views, modes, and tiers;
   - the viewport shapes and reopens it passes through while already shown;
   - every other surface that can be present at the same time, siblings on its screen and the surfaces one step before and after it in the flow.
2. *when* the prover reaches one situation, the system *shall* ask whether this surface's behaviour is stated there, and *shall* report a reachable situation with a blank answer as a finding of the same class as a fact no node owns. [INV-72, E-14]

**Case: the hunt rides both passes and leaves the sentence to the author**

3. The system *shall* run the hunt on both the whole-spec pass and the surface-add pass. [INV-72, M-6]
4. *when* the hunt reports a missing situation, the system *shall* leave the sentence to the author, who writes it as a composition invariant, decided or marked a default the way the standard-facet sweep marks its own, and *shall* invent no answer and ask the human for nothing. [INV-72, INV-18, INV-31]

---

## Requirement 260: A cross-surface policy is stated once at the class level

**Context:** When a decision governs a kind that recurs across sibling surfaces or elements — a gesture policy, an affordance, an input-to-action mapping, a repeated state transition, or a feature and its element shared across places — the spec states it once at the surface-class level, naming the class and enumerating the surfaces it governs. Consistency of this kind is itself an invariant. This is the preventive twin of the class hunt: the class hunt sweeps siblings once a bug is confirmed, and this holds the policy uniform before a bug is filed.

**User Story:** As a person keeping behaviour uniform across similar surfaces, I want a policy for a recurring kind stated once at the class level and checked across its siblings, so that a rule written for one surface while its siblings stand cannot ship non-uniform.

### Acceptance Criteria

**Case: the policy is homed on the class**

1. *when* a decision governs a kind that recurs across sibling surfaces or elements, the system *shall* state it once at the surface-class level, naming the class and enumerating the surfaces it governs. [INV-125]
2. The system *shall* read a policy written for one surface while siblings of the same kind exist as a spec defect. [INV-125, INV-124]

**Case: the prover and the guardrail hold it**

3. *when* the prover reads an interaction policy, the system *shall* enumerate the surfaces of that kind from the surface registry and flag any the clause does not cover, the same finding class as a reachable situation with a blank answer. [INV-125, E-10, INV-72]
4. *when* a product renders a page, the system *shall* assert a policy declared for one surface root across every registered sibling root and hold it red until all are covered, so the non-uniformity reds the day the single-surface fix lands. [INV-125, INV-97]
5. The system *shall* keep the spec-class rule as the root and leave the page-wide assertion to the products the pack serves, the pack shipping the rule and the prover lens as the ship-the-shape pole of the pack-to-host split. [INV-125, INV-163]

**Case: the same defect stated in prose**

6. *when* a sentence states a principle for a whole kind while it is homed on one surface and siblings of that kind exist, the system *shall* read it as the same defect in prose form, and *shall* demand the author lift the principle to a class clause naming the class and its members, or scope it to the one member by a decided sentence. [INV-125]

---

## Requirement 261: Both directions of a paired state change get the same craft

**Context:** When a surface has a pair of opposite state changes — open and close, enter and exit, expand and collapse, show and hide — a transition crafted for one direction is a decision about the pair, so the other direction is stated too. The default is symmetry: the exit mirrors the enter's feel unless a reason is written. A shorter exit or a deliberately instant one is a valid, stated, decided answer. Motion feel is the human's own gate, so where the author cannot judge the pair the question is surfaced to him.

**User Story:** As a person crafting a paired transition, I want the opposite direction stated whenever one direction is crafted, so that a crafted-in and instant-out pair cannot ship silently and a reader tells a decided asymmetry from an overlooked one.

### Acceptance Criteria

**Case: the continuity of the transition**

1. *when* a surface has a pair of opposite state changes and one direction's transition is crafted, the system *shall* state the other direction too, defaulting to symmetry unless a written reason parts them. [INV-126]
2. The system *shall* have the author write the pair's answer as a spec sentence — mirror, a named shorter exit, or deliberately instant — decided or marked a default on the standard-facet sweep. [INV-126, INV-18, INV-31]
3. *if* the author cannot judge the pair's feel, *then* the system *shall* surface the question to the human rather than ship a crafted-in and instant-out pair. [INV-126, INV-30]
4. *when* the prover reads a paired state change with one direction described and the opposite unstated, the system *shall* report it as a finding of the same blank-answer class as an unwritten situation. [INV-126, INV-72]

**Case: the reversibility of the means**

5. *when* a surface is opened by a continuous, reversible gesture — a pinch, a drag, a lift — the system *shall* have that same gesture reversed stand among its ways to close, or a decided sentence state why it is absent. [INV-126, INV-30]
6. *when* an opening gesture has a natural inverse, the surface offers no way to close by that inverse, and no deciding sentence stands, the system *shall* block it as a finding of the same blank-answer class. [INV-126, INV-72]

**Case: the magnitude of a reversible quantity**

7. *when* the paired open and close ride a continuous, reversible quantity, the system *shall* state whether the inverse asks the same magnitude as the forward move, symmetric or a named deliberate asymmetry. [INV-126, INV-31, INV-72]
   - the continuous, reversible quantity may be a pinch span, a drag distance, or a wheel accumulation;
   - the answer is decided or marked a default;
   - the system *shall* report a stated pair whose magnitude sentence is missing as the same blank-answer finding.

---

## Requirement 262: Each scenario states how it is entered and how it exits

**Context:** A person-facing scenario is a flow, and a flow has edges: it is entered from somewhere with something already true, and it exits to somewhere leaving something behind. The scenario states both, so a reader can check it against a known before and after. This lifts the per-operation precondition and postcondition lenses to the scenario level.

**User Story:** As a person reading a scenario, I want its entry and its exit stated, so that the prior state it assumes and the postcondition the next scenario inherits are both stated on the page for the reader.

### Acceptance Criteria

**Case: the scenario states both edges**

1. The system *shall* have each person-facing scenario state its entry — where the walk arrives from and what must already hold — and its exit — where the person lands and what it leaves true for the next scenario to inherit. [INV-127]
2. The system *shall* read this as the scenario-level lift of the per-operation precondition and postcondition lenses, kin of the entry-symmetry lens and the runtime view's flow walks. [INV-127, INV-50, INV-74]

**Case: the prover holds it, binding forward**

3. *when* the prover reads a flow whose entry or exit is unstated, the system *shall* report it as a finding of the same blank-answer class. [INV-127, INV-72]
4. The system *shall* have a new scenario state its edges from the first draft and *shall* flag an existing scenario's unstated edge as a finding rather than block the lane. [INV-127, INV-159]

**Case: a trivially-none edge is still stated**

5. *when* a scenario's entry or exit is trivially none — a top-level scenario entered from nowhere, a terminal scenario exiting to nowhere — the system *shall* state it as such in one short clause, so a reader tells a decided edge from an overlooked one. [INV-127]

---

## Requirement 263: A gated behaviour names both ends of its range, and a scoped guarantee answers for its whole domain

**Context:** When a transition is gated on a quantity that runs on a line — elapsed time, a count, a distance, a size — the spec states its behaviour at both ends of the live range: below the low end and above the high end. When a slot on screen is filled by asynchronously produced content, the spec names the three faces of the wait — pending, arrived, and failed — and a visible pending face stands wherever the slot holds a reserved place. A guarantee that holds over one named part of its domain owes the same completeness across the whole domain, the viewport its worked instance.

**User Story:** As a person crossing an unnamed edge — reloading before the lower bound, returning after the upper, landing on a viewport band a guarantee never named — I want every range end, wait face, and domain part decided, so that no edge of a range or a partial guarantee renders as a blank the spec never wrote.

### Acceptance Criteria

**Case: both ends of a gated range**

1. *when* a transition is gated on a quantity that runs on a line, the system *shall* state its behaviour below the low end and above the high end, each end standing as its own decided or default sentence, and *shall* read a phrase that names one point and leaves an unbounded interval silent as incomplete until that interval is bounded on both sides. [INV-138]

**Case: the three faces of an async slot**

2. *when* a slot on screen is filled by asynchronously produced content, the system *shall* name the pending, arrived, and failed faces of the wait and stand a visible pending face wherever the slot holds a reserved place. [INV-138]
3. The system *shall* read the pending face as that slot's loading state, sharpening the standard facets' empty, error, and loading states for a reserved slot. [INV-138, INV-18]
4. *when* the prover reads a gated range or an async slot with an out-of-range or in-between state left unspecified, the system *shall* report it as the same class as an unwritten situation. [INV-138, INV-72, INV-31, INV-30]
   - the timing is surfaced to the human, since only he can judge it.

**Case: a scoped guarantee owes its whole domain**

5. *when* a guarantee holds over one named domain part, the system *shall* draw the standing question about the remainder and give each remaining part its own decided or default sentence until the domain is covered. [INV-138]
   - a named domain part is a band of a ranged quantity, a user state, a network condition, or a locale.
6. The system *shall* read a guarantee that speaks for one part while the remainder stays silent as the same unwritten-situation class. [INV-138, INV-72]

**Case: the viewport is the worked instance**

7. The system *shall* have every layout guarantee name its viewport quantifier — holding on every viewport or naming the band it is scoped to — and *shall* leave the other bands silent until each is stated, the short-viewport band among them. [INV-138, T-13]
8. *when* the parts are a same-kind group no clause has yet declared, the system *shall* reach them through the design review's group pass and hold them in the prover once a part-uniform guarantee is declared. [INV-138, INV-141, INV-150]
9. The system *shall* read this as the range-and-lifecycle member of the composition-lens family, its member set open-ended, naming the viewport as its worked instance and leaving the remainder to the general duty. [INV-138, INV-125, INV-126, INV-136, INV-226]

---

## Requirement 264: A general law over concrete instances declares whether it enumerates them or lets them ride

**Context:** A law that states one general duty a set of concrete instances falls under makes one choice about those instances: the clause names every member, or an instance rides the general duty with no name. The member set keys the choice. A closed set names every member; an open-ended set names only its worked instances and leaves the remainder to the general duty. A law that reaches this choice by feel is the defect this rule keys.

**User Story:** As a person writing a general law over instances, I want the member set to decide whether the law enumerates or lets instances ride, so that a closed set names every member while an open-ended set names only what a real incident earned.

### Acceptance Criteria

**Case: the member set keys the choice**

1. *when* a law states a general duty a set of concrete instances falls under, the system *shall* make one choice: name every member in the clause, or let an instance ride the general duty with no name. [INV-226]
2. *when* the member set is closed and enumerable — finite and nameable, even one that grows a member at a time by a named incident — the system *shall* name every member in the clause, as the per-kind quality budgets name each project kind and the standard-facet list names each facet. [INV-226, INV-18, INV-41]
3. *when* the member set is open-ended — any sub-case of a domain, unlistable in advance — the system *shall* name only its worked instances, each earned by a real incident, and leave the remainder to the general duty carried by the rule with no list, as the scoped-guarantee law names the viewport alone. [INV-226, INV-18, INV-138]

**Case: reaching the choice by feel is the defect**

4. The system *shall* read a general law reaching enumerate-or-ride by feel as the defect this rule keys, the member set deciding, and *shall* have a law whose set is genuinely borderline state which side it took and why. [INV-226]
5. The system *shall* read this as the declaration member of the composition-lens family, and *shall* place its enforcement with the author who writes the law. The prover *shall* run no sweep of its own for it, since only the author knows whether a member set is closed. The prover *shall* catch the sibling-surface case in its cross-surface uniformity sweep. [INV-226, INV-125, INV-126, INV-136, INV-138]

---

## Requirement 265: A surface's composition axes are the set its project's kind owes

**Context:** The floor axes are the kind-independent set every stateful surface answers, and a project's kind settles which further axes a surface owes beyond it. A kind carries a standard set of composition axes the way it already carries a node-structure scaffold and a set of design principles, so the author of a surface reads its axes from the kind before composing. An axis exists because the kind renders under it, and that existence stands apart from what today's code happens to cover; the gap between an owed axis and the code's coverage is the finding.

**User Story:** As a person composing a visitor-facing surface, I want its axes read from the project's kind and every owed axis covered against each of its values, so that an axis the kind owes cannot sit uncovered until a visitor falls through it.

### Acceptance Criteria

**Case: the axis set is read from the kind**

1. The system *shall* have the author read a surface's axes from the project's kind before composing, the kind carrying its axis set the way it carries a node-structure scaffold and a set of design principles. [INV-244, INV-36, INV-135, INV-136]
2. *when* a project's kind is visual, the system *shall* owe every visitor-facing surface an open axis set whose first named member is the input-capability axis, beyond the viewport axis the floor already carries. [INV-244, INV-36, INV-136, C-1]
   - a visual kind renders a visitor-facing surface and declares a design-principles set; the `static site` and `fullstack` kinds are visual kinds.
3. The system *shall* have the sibling axes on that surface — browser engine, locale and text direction, connection reach, first-versus-returning visit, accessibility, and measurement reach — ride the per-kind duty and enter as their own increments, so the visual kind's owed set stays open. [INV-244, INV-226]

**Case: the axis set is a founding declaration**

4. The system *shall* have every project kind name the composition axes it owes beyond the floor as a founding declaration, the way it declares its concrete layers and proof kinds. [INV-244, INV-135]
5. *when* a kind owes no axis beyond the floor, the system *shall* accept the empty set only as an explicit stated decision, the case the per-kind design-principles set already legitimises for a kind with no visual surface. [INV-244, INV-136]
6. *when* a kind is recorded with no axis-set declaration at all, the system *shall* flag it the way a kind recorded with no layers or proofs is flagged. [INV-244, INV-135, A-10]
7. The system *shall* have a non-visual backend kind owe its own non-empty axis set — load, version, and tenant — so an axis set that stays empty for a non-visual kind is a defect the flag-if-absent check stops. [INV-244, INV-135]

**Case: the gap between owed and covered is the finding**

8. The system *shall* read the two layers at each surface, and *shall* report an owed axis whose value the code leaves uncovered as a finding of the same blank-answer class. [INV-244, INV-72]
   - the two layers are the axes the kind owes and the values the shipped code covers;
   - that blank-answer class also covers a reachable situation the spec never wrote.
9. *when* the gap is found, the system *shall* have the author state it as a spec sentence, decided or marked a default. [INV-244, INV-18, INV-31]
10. The system *shall* read an owed axis as covered only once the author composes and tests the surface against each elementary value of the axis, the write-the-sentence half and the cover-the-values half splitting one dimension by time. [INV-244, C-1, INV-18]

**Case: an axis carries its own value space**

11. The system *shall* read an axis's value space as a domain the same completeness reaches, and *shall* model the input-capability values as combinable capabilities a surface answers for in combination, since touch, a fine pointer, hover, and a keyboard co-occur on one machine. [INV-244, INV-138, INV-226]
12. The system *shall* owe and answer the two elementary poles — touch and a fine pointer — up front, and *shall* carry the co-occurrence answer, hover present alongside touch, in with the later step that forces the author to answer for the in-between. [INV-244]
    [GAP: the source answers the two elementary poles up front but defers the co-occurrence value — one device carrying touch and hover at once — to a later forcing step, naming no interim answer or default; a surface's behaviour when both are present is unstated today, so a test author cannot pin the tablet-with-hover-and-touch case.]
13. The system *shall* leave the refinement values past the elementary poles — a stylus, a keyboard-only reach, a device an advanced user registers — to the human's taste, entering later, decided or marked a default when they do. [INV-244, INV-30, INV-31]

**Case: the rule binds forward**

14. The system *shall* have a surface authored after this rule read its axis set from the kind from the first draft, and a surface that predates it carry the read at the first landing that touches it, staying uncovered on the axis until that landing arrives. [INV-244, INV-159]

**Case: the value-space machinery is promised**

15. The system *shall* keep the value-space in-between forcing step and the recursive axis-registry similarity sweep promised as later increments. [INV-244]
    [target]

---

## Requirement 266: A declared axis that adds runtime code names whether its artifact divides or ships whole

**Context:** The composition law reads whether a surface's behaviour divides along a cross-cutting axis its kind owes. Its dual reads whether the artifact the visitor receives divides along that same axis or arrives as one piece. When a spec declares such an axis and covering it adds runtime code, the design owes one of two decided sentences; an axis that adds runtime code and carries neither is the finding, shipping as one artifact because the choice went unexamined.

**User Story:** As a person reviewing an artifact's delivery, I want each declared axis that adds runtime code to state whether the artifact divides along it or ships whole for a named reason, so that a monolith nobody examined is caught while a monolith with a stated reason stands.

### Acceptance Criteria

**Case: the dual of the composition law**

1. The system *shall* read whether the delivered artifact divides along a declared axis its kind owes or arrives as one piece, the dual of the composition law that reads whether behaviour divides along that axis. [INV-248, INV-244]
2. *when* a spec declares such an axis and covering it adds runtime code, the system *shall* carry one of two decided sentences. [INV-248]

**Case: the two settled answers and the finding**

3. The system *shall* accept a monolith named for a stated architectural reason as a settled answer. [INV-248]
   - the reason may be one bundle behind one page that is never torn down;
   - a delivery that runs on no server;
   - a payload the design judges too small to make a split worth its cost;
   - the design judges whether the named reason holds.
   [GAP: the source names the design as the judge of a "too small to make a split worth its cost" payload but states no measure — the payload size below which a split costs more than it saves — so a maintainer cannot pin the boundary between a settled small-payload monolith and an unexamined one; the source leaves it to the design as a senior read, not a gate.]
4. The system *shall* accept an axis that names the delivery road it owes — a platform split, a lazy load, a per-value chunk — carried by its own later row. [INV-248, INV-159]
5. The system *shall* read the finding as the third case: an axis that adds runtime code and carries neither sentence, shipping as one artifact because the choice went unexamined, its byte weight the downstream symptom of the unasked separability question. [INV-248]

**Case: the lens's reach and its standing**

6. The system *shall* reach this lens past the input-capability axis to any declared axis a kind owes. [INV-248]
   - reached only where covering it ships runtime code;
   - it may be an assistant capability present or absent, a rendering engine, or the viewport;
   - a viewport answered by a media query, or a locale answered by a logical property, draws no delivery question.
7. The system *shall* keep this a senior read the prover carries and not a gate, since a monolith is lawful whenever its reason is named and only the design can say whether that reason holds. [INV-248, INV-244, INV-214]
8. The system *shall* carry a prover discovery habit stated in its skill: for a lens the prover applies, it may ask whether that lens's dual applies to the document here. The system *shall* read this as a prompt that surfaces a missing lens, and not as a rule that every lens ship paired, since one dual folds into a lens already run while another is nameable yet seldom applies. [INV-248]
9. The system *shall* read this as the delivery-separability member of the composition-lens family, binding forward. [INV-248, INV-125, INV-126, INV-136, INV-138, INV-226, INV-159]
   - the forward terms match the axis-set rule's: from the first draft for a new surface, at the first touching landing for an older one.

---

