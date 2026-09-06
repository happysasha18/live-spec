## Requirement 5: A row rests in the home its exit names

**Context:** A row's exit decides where it lives next. A row closed with a terminal exit — *landed*, *declined*, or *superseded* — moves to the queue archive in the commit that closes it and stays there unedited. A deferred row stays in the queue's body carrying its revisit trigger. A far row stays too, but carries no revisit trigger and no plan to run.

**User Story:** As a person whose queue holds live work beside parked thoughts, I want each row to rest in the home its exit names, so that a closed wish is archived, a deferred one returns on its trigger, and a far one is kept out of that same what's-left answer.

### Acceptance Criteria

**Case: a terminal exit is archived**

1. *when* a row closes with a terminal exit — *landed*, *declined*, or *superseded* — the system *shall* move it to the queue archive in the same commit that closes it, carrying it verbatim, and *shall* keep it there unedited and grepable by its number. [INV-1, INV-276]
2. The system *shall* keep in the archive only wishes no longer due back. [INV-1]

**Case: a deferred row waits on its trigger**

3. The system *shall* keep a deferred row in the queue's body, carrying its revisit trigger, until the trigger fires or the row resolves to a terminal exit. [INV-222]

**Case: a far row is kept and stood down**

4. The system *shall* keep a far row in the queue's body with no revisit trigger and no plan to run, so a thought worth keeping is not discarded. [INV-222]
5. *when* the runnable report — the what's-left answer naming the rows a session could take next, spoken at queue-take or on the person's ask — is produced, the system *shall* stand the far tier down by name and *shall* show it only on the person's request. [INV-222, INV-223]

---

## Requirement 6: From its row, a wish follows one fixed path

**Context:** From its row, a wish follows one path through the pipeline. The classifier reads and states its attributes, a spec-delta is drafted and validated, the wish is queued and worked, and it lands when its proofs pass. Each step is one transition in a fixed sequence.

**User Story:** As a person tracking a wish from capture to landing, I want it to travel one fixed path of stated steps, so that at any point I can see which step it sits at and what remains.

### Acceptance Criteria

**Case: the wish travels a fixed path**

1. *when* a wish is recorded as a row, the system *shall* read its size, priority, door, and work-kind and state them back to the person in one intake line. [T-1..T-7]
2. The system *shall* draft a spec-delta and *shall* validate it against the whole spec, sending only genuinely human questions to the person in a batch while everything else proceeds on the recommended option marked in the row. [T-1..T-7]
3. The system *shall* move the wish's status to queued and then to in-work. [T-1..T-7]
4. The system *shall* land the wish *when* the suite is green, the guardrails pass, the commit goes in, and the row closes with its acceptance met. [T-1..T-7]
5. *when* the wish lands, the system *shall* report to the person in one plain-language line naming the position on the feature map, what landed, and what remains. [T-1..T-7]

---

## Requirement 9: A wish is classified by size, priority, and work-kind

**Context:** A wish is classified by size, priority, and work-kind, three separate axes. Size uses one four-word vocabulary everywhere. The door — where the wish enters the pipeline — is a separate axis, and size is a separate question. Priority is normal unless a row carries a mark.

**User Story:** As a person whose wish enters a disciplined pipeline, I want its size, priority, and work-kind pinned at intake by the person when unclear, so that each attribute is set by a considered, explicit call.

### Acceptance Criteria

**Case: the three axes and their vocabularies**

1. The system *shall* classify each wish by one size word from the four-word measure — bug, small, surface, or large — and *shall* carry the same four words in the queue row's class column with no second size scale. [INV-12, T-16]
   [GAP: the boundary separating a small wish from a large one is unstated in the source; only the surface and bug sizes carry stated readings.]
2. The system *shall* keep the door a separate axis from size, naming where the wish enters the pipeline. [T-16]
3. The system *shall* name one work-kind per wish from the curated vocabulary — product, infra, skill, or prose — taking the host's recorded default where the person names none. [T-16]

**Case: priority and its two marks**

4. The system *shall* carry a wish at normal priority unless its row states otherwise, marking it critical *when* the shipped product is broken for its user — an unusable surface, lost data, or a violated safety gate — and quick win *when* the work is low in effort, of immediate value, and holds no design decision. [INV-12]
   [GAP: the source gives critical three concrete conditions but gives quick win only the qualitative phrases "low effort" and "immediate value", naming no measure or threshold separating a quick win from a normal wish; the classifier and the person judge it at intake with nothing pinned.]

**Case: an unclear attribute is asked, never guessed**

5. *when* the classifier cannot call a size, a priority, or a work-kind, the system *shall* ask the person at intake and *shall* not guess. [INV-12, T-16]
6. *while* an unclear attribute stays open, the system *shall* carry the wish at normal priority with the host's default work-kind or none, and *shall* scale nothing down for a work-kind not yet named. [INV-22, INV-12, INV-4, T-16]
   - the open question stays in the row while the lane keeps moving.

---

## Requirement 10: A large wish negotiates scope, never time

**Context:** The walk never asks how long a wish will take and never accepts an estimate in hours or days as an input. When a wish is worth less than the work it demands, the walk answers in scope terms and proposes cutting the scope or splitting into stages. Every cut is reported.

**User Story:** As a person whose wish may cost more than it returns, I want the walk to renegotiate its scope while holding its schedule, so that an oversized wish is trimmed or staged and every trim reaches me in the report.

### Acceptance Criteria

**Case: scope is the axis, never time**

1. The system *shall* refuse to ask how long a wish will take and *shall* refuse an estimate in hours or days as an input. [T-15]
2. *when* the work a wish demands is larger than the wish is worth, the system *shall* answer in scope terms and *shall* propose one of two moves — cut the scope to fewer surfaces with plainer defaults, or split into stages that each land through the full pipeline. [T-15, INV-12]
   [GAP: the source triggers the scope negotiation on a wish being "larger than its worth" but names no measure of a wish's worth and no judge of the comparison, so when the negotiation opens is unpinned.]

**Case: the proposal proceeds and every cut is reported**

3. The system *shall* proceed on the recommended option and *shall* not park the lane on the proposal. [T-15, INV-4]
4. The system *shall* report every cut in the batched delivery report alongside every taken default, and *shall* not cut silently. [INV-18, INV-5]

---

## Requirement 12: A scope cut moves scope alone and spares the mandatory sentences

**Context:** A scope cut changes scope only, never order. A cut surface returned later is a new wish. No cut touches the delta's mandatory sentences — the regression fences, a kept surface's facets, the non-goals, and the success measure. Scope adjusts richness.

**User Story:** As a person whose wish was trimmed, I want the cut to move scope alone and to leave the mandatory sentences intact, so that trimming never reorders the lane and never drops a fence, a facet, a non-goal, or the success measure.

### Acceptance Criteria

**Case: a cut moves scope alone**

1. The system *shall* treat a cut surface returned later as a new wish. [T-11]
2. The system *shall* let a scope cut change scope only, reading it as no quick-win mark, since only priority moves the lane order. [T-11]

**Case: the mandatory sentences are uncuttable**

3. The system *shall* keep every cut clear of the delta's mandatory sentences — the regression fences, a kept surface's facets, the non-goals, and the success measure. [T-14, INV-18, INV-20, INV-21]
4. The system *shall* adjust richness through a cut and *shall* leave the mandatory sentences standing whole. [T-15]

---

## Requirement 13: One wish is one user story, and a row closes only whole

**Context:** One wish is one user story — one distinct thing a person will do and see. A wish carrying more than one story is split at intake, each story its own row through the full pipeline. Sub-behaviours of one story — its hover face, its phone face, a backpointer — are that story's acceptance, folded into that same row.

**User Story:** As a person who voices a wish that hides two stories, I want it split at intake into a row per story, so that each row traces to one clear thing I wanted and no two behaviours are fused into one close.

### Acceptance Criteria

**Case: a multi-story wish is split**

1. The system *shall* split a wish carrying more than one user story at intake, giving each story its own row through the full pipeline. [T-17]
2. The system *shall* fold the sub-behaviours of one story — its hover face, its phone face, a backpointer — into that story's own row as its acceptance. [T-17]
3. The system *shall* keep separate stories in separate rows and *shall* not fuse them, distinct from a stage split that slices one story's depth. [T-17, T-15]

**Case: the split is asked and loses nothing**

4. *when* the story count is unclear, the system *shall* ask the person at intake and *shall* not guess. [INV-12]
5. The system *shall* have every row a split produces cite the one spoken wish it came from. [T-17, INV-1]

---

## Requirement 14: A multi-leg row enumerates per-leg acceptance

**Context:** Some rows still carry more than one leg — a legacy fusion or a harvested batch. Such a row states acceptance for each leg in its Done-when and closes only when every leg is met. Half-done is a status, never a landing.

**User Story:** As a person whose row carries several legs, I want per-leg acceptance enumerated and the row held open until every leg is met, so that a half-finished row stays visibly open rather than closing on an unmet leg.

### Acceptance Criteria

**Case: per-leg acceptance and no partial close**

1. *where* a row carries more than one leg, the system *shall* enumerate per-leg acceptance in its Done-when and *shall* not close the row with an unmet leg. [INV-26]
2. The system *shall* read half-done as a status and never as a landing. [INV-26]

**Case: compaction preserves an open leg in its one home**

3. The system *shall* keep an unfinished leg on its task's board row and working checkpoint at announced self-compaction, and *shall* never copy that leg into the resume file as a second task statement. [INV-26, INV-48, M-2]

---

## Requirement 15: The system echoes every wish back and reports each feature's stage

**Context:** The system speaks every captured wish back to the person in one immediate sentence. The echo opens with what was heard, which door the wish entered, the name the work goes by, and its row number; further law in this section adds the wish's feature-map position, and a long-running direct command adds an honest time range. Every status report then names each in-flight feature and the pipeline stage it sits at.

**User Story:** As a person who threw a wish and leads several windows, I want an immediate one-sentence echo and a status report that names each feature's stage, so that I always see a request was captured and exactly where it stands.

### Acceptance Criteria

**Case: the immediate echo**

1. *when* a wish is captured, the system *shall* echo it back in one plain sentence stating what was heard, which door it entered, the name the work goes by, and its row number. [INV-27]
2. *when* a wish arrives silently — dropped into an inbox as a file, or pulled from a batch — the system *shall* carry its echo in the next status report rather than as an interruption. [INV-27]
3. *when* a wish is bridged in from a stranger's Issue, the system *shall* also post its echo on that Issue, since the stranger reads no status report of the host's. [INV-146, INV-147]

**Case: the status report names each stage**

4. The system *shall* have every status report name each in-flight feature and the one pipeline stage it sits at, drawn from the nine steps in fixed order — spec, prove, architecture, prove architecture, matrix, test, code, verify, and commit-and-show. [INV-27]
5. The system *shall* report a paused feature under its stage's name and *shall* read landed as a terminal state that is not itself a pipeline step. [INV-27]
6. The system *shall* have the echo also state where the wish sits on the product's feature map. [INV-27, INV-37]

---

## Requirement 16: Every wish is placed on the feature map by one of three verdicts

**Context:** Every wish is placed on the product's feature map, and the placement is stated by default. The feature map is the spec's scenario sections and the architecture's nodes together, so no separate map document exists. Each placement is one of three verdicts: it changes an existing feature, it is a new feature, or it is a restructure.

**User Story:** As a person tracking where a wish lands in the product, I want its placement stated and recorded as one of three verdicts, so that the map stays the spec plus the architecture and a restructure opens its own row rather than re-dividing on the spot.

### Acceptance Criteria

**Case: the three placement verdicts**

1. *when* a wish is captured, the system *shall* place it on the feature map as one of three verdicts. [INV-37, E-14]
   - it changes an existing feature and names that scenario;
   - it is a new feature with its own scenario section and architecture node;
   - it is a restructure.
2. *when* the verdict is restructure, the system *shall* open its own row, and *shall* carry the re-division through the architecture stage and its re-proof rather than re-dividing on the spot. [INV-37, E-14]
   - the row opens at the refactor door when only structure moves, or at the feature door when behaviour moves with it.

**Case: placement reports, records, and defers the structure change**

3. The system *shall* let a placement report that the structure no longer fits, yet *shall* alter the structure only through a completed change. [INV-37]
4. The system *shall* place a bug on the feature it repairs, and *when* the classifier cannot determine a wish's feature *shall* ask the person. [INV-37, INV-12]
5. The system *shall* record the verdict in the wish's row as a note — a named changed feature, new, or restructure — so the placement stays searchable after the report scrolls away. [INV-37, T-14]

---

## Requirement 17: The outcome does the talking, and every handle trails

**Context:** The outcome does the talking: names are plain and every handle trails. A feature's echo-name is a short descriptive phrase in the product's own words that a reader who missed its birth can parse cold. A human-facing report or board line opens with what changed for the reader, and every internal handle trails in parentheses. Bookkeeping numbers are handles too.

**User Story:** As a reader who did not watch the work, I want every line to lead with what changed for me while codes and counts only trail, so that I get the outcome in plain words without decoding an internal handle.

### Acceptance Criteria

**Case: names are plain**

1. The system *shall* give a feature a short descriptive echo-name in the product's own words that a reader who missed its birth can parse cold, and *shall* not use a private metaphor. [INV-28]
2. The system *shall* read a name that needs its story told first as a bare handle. [INV-28]

**Case: the line leads with the outcome**

3. The system *shall* open a human-facing report or board line — a chat report, a narration line, a report page, a decision page, or the capture echo — with what the reader can now do, see, or stop fearing, and *shall* keep every internal handle, a spec code, a row or session number, or a coined name, trailing in parentheses. [INV-28, INV-35]
4. The system *shall* give one fact one standalone sentence and *shall* read a compression that needs the writer's own context to parse as a defect of the line. [INV-28]

**Case: bookkeeping numbers are handles**

5. The system *shall* keep a bookkeeping number — a test count, a suite size, a version string, or a check tally — out of the message content, stating what the number means for the reader while the number only trails or stays in the records. [INV-28]
6. *when* the number is the asked substance — a direct question about it, or the done-claim evidence walk that pins its artifact and method version — the system *shall* let the number itself be the content. [INV-28, INV-25]

**Case: the laws have a mechanical voice**

7. The system *shall* inject through the prompt hook `hooks/chat-law-hook.sh` a reminder of the chat laws into every prompt. [INV-28, INV-69, INV-137]
   - the reminder states the laws in plain words with codes trailing, the narration beats, the say-what-it-is line, and the banned contrast frame;
   - the say-what-it-is line names a thing by its own positive sentence;
   - the reminder also states the routing line: the orchestrator seat routes work to the cheapest tier the routing rule names, while a worker finds for itself the files and lines its task needs, keeping the seat's context lean;
   - the skills and the profile stay the laws' homes.
8. Before a human-facing artifact is shown, the system *shall* have `scripts/preshow-lint.py` flag any line opening with an internal handle so the agent rewrites it to lead with the outcome, a warning to clear that reads only the shown surface. [INV-28]

---

## Requirement 37: A critical bug heads the queue, and priority is recorded

**Context:** Priority changes the queue order, and the change is written into the row. A critical bug lands before everything, heading even the waiting-bug line. Preemption of an in-work lane belongs to the bug door alone.

**User Story:** As a person with an urgent defect, I want a critical bug to head the queue and the reordering recorded, so that the most urgent work runs first and the reason is answerable from the row.

### Acceptance Criteria

**Case: critical priority heads the queue**

1. *when* a bug is marked critical, the system *shall* place it at the head of the queue ahead of the waiting-bug line, and *shall* let only the bug door preempt the in-work lane. [T-9]
2. *when* a critical mark raises a wish's priority, the system *shall* record the change in the wish's row, so the reordering is answerable from the record. [T-9]

---

## Requirement 38: A critical mark on a non-bug heads the queue but never stops the rolling lane

**Context:** Critical priority on a non-bug door sends the wish to the head of the queue while the rolling lane keeps running. A live break that must stop the work now is a bug, which takes the pen at the end of the current pen-stage. The two are different promises, so the bound is echoed back at intake and the human can re-door the wish a bug.

**User Story:** As a person who marks a non-bug critical, I want the wish to head the queue while the lane keeps running and the bound spoken back at intake, so that I hear the difference and can re-door it a bug if I meant a live break.

### Acceptance Criteria

**Case: the bound the non-bug critical buys**

1. *when* a wish is marked critical on a non-bug door, the system *shall* head the queue with it and *shall* admit it at the pen-holder's next pen-stage boundary without interrupting the rolling lane, since preemption belongs to the bug door alone. [INV-133]
2. *when* a wish is marked critical on a non-bug door, the system *shall* say in the capture echo that it heads the queue, does not stop the lane, and that only the bug door preempts, so the person can re-door it a bug. [INV-133]
3. The system *shall* keep priority the human's own to set, stating what critical buys on each door and never refusing the mark. [INV-133]

---

## Requirement 39: A small wish may be promoted, and arrivals order by registration

**Context:** Priority is the one thing that reorders the lane, and it does so visibly. A small queued wish may be taken ahead of larger ones when the lane frees, with the promotion marked in its row. A wish is registered at the moment it arrives, and that registration order settles ties.

**User Story:** As a person throwing wishes of many sizes, I want a small wish promotable with the promotion recorded and arrivals ordered by registration, so that quick work can jump ahead visibly while a stream of small wishes cannot starve a big one.

### Acceptance Criteria

**Case: the recorded promotion**

1. *when* the lane frees, the system *shall* let the agent take a small queued wish ahead of a larger queued wish, marking the promotion in the row rather than making it in silence. [T-11]
   [GAP: the source lets a small wish be promoted ahead of larger queued wishes but names no size boundary or measure separating a promotable wish from a larger one; the agent judges with no stated threshold.]
2. *when* one promoted wish lands, the system *shall* run the queue head next, so a stream of small wishes cannot starve a big wish. [T-11]

**Case: registration order settles arrivals**

3. *when* an inbox wish arrives, the system *shall* register it at the moment of arrival and *shall* let no file's own date compete with a spoken timestamp. [T-11]
4. *when* two arrivals tie, the system *shall* resolve the tie by queue row order top to bottom, and *shall* register an inbox batch swept in one pass in filename-sorted order. [T-11]

---

## Requirement 40: Every wish is classified into one door before any code

**Context:** The door says where a wish enters the pipeline: feature, bug, refactor, docs-only, or skip. Classification is an explicit step with fixed rules, decided before any code is written, and personal judgment does not settle it. A row carries three axes stated together in one intake line: size, priority, and door. A wish too big for its worth is renegotiated in scope, never in time.

**User Story:** As a person throwing a wish however casually, I want it sorted into one door by a fixed ordered procedure, so that what counts as a feature is decided by the rule, whatever words the request used.

### Acceptance Criteria

**Case: the intake line and the door set**

1. *when* a wish is captured, the system *shall* state its size, priority, and door together in one intake line, and *shall* renegotiate a wish too big for its worth by the scope rule stated once at the scope-negotiation requirement. [T-12, T-15]
2. The system *shall* draw the door from the closed set of five — feature, bug, refactor, docs-only, and skip — naming it before any code is written. [T-12]

**Case: the ordered procedure**

3. *when* the door step runs, the system *shall* call a wish a feature *if* any tripwire holds. [T-12, INV-16]
   - a new user-visible surface appears;
   - new persistent state appears;
   - a new interaction lands on an existing surface;
   - the touched surface is marked a later surface in the spec;
   - the wish carries the `[target]` planned-feature mark on its own line;
   - the wish's building row still stands open;
   - the change adds behaviour no spec clause backs.
4. *if* no tripwire fired but shipped behaviour is wrong against what the spec or product already promises, *then* the system *shall* call the wish a bug. [T-12]
5. *if* behaviour stays identical while structure moves, *then* the system *shall* call the wish a refactor, and *if* only prose outside the normative spec changes, *then* the system *shall* call it docs-only, routing a reworded spec rule as feature or bug instead. [T-12]
6. *if* a single file changes with no new state, element, or visible behaviour and an existing test level already covers the touched fact, *then* the system *shall* call the wish a skip. [T-12]
7. *when* a casual label conflicts with a fired tripwire, the system *shall* let the tripwire verdict outrank the label, re-door the wish, and record the re-door in the intake line. [INV-16, INV-5]

---

## Requirement 41: A re-doored wish gets no preemption, and the door is re-checked mid-work

**Context:** Queue-cutting belongs only to the bug door, so a wish re-doored to feature gets no preemption. The door is also re-checked mid-work: the moment running work is about to create a surface or state its current door does not grant, the work stops and the door step fires again. A mid-work re-door that creates a surface or state re-runs the independence edges between the parallel lanes.

**User Story:** As a person whose wish turns out to be a feature mid-work, I want it re-doored in place without preemption and the lane independence re-checked, so that a change that grows a surface is caught and the departures board never asserts a stale independence.

### Acceptance Criteria

**Case: no preemption, re-entry in place**

1. The system *shall* give a re-doored wish no queue-cutting, letting the human raise its priority while no word lets a feature skip the spec step. [INV-16]
2. *when* running work is about to create a user-visible surface or persistent state its current door does not grant, the system *shall* stop the work, fire the door step again, keep the lane, and re-enter the pipeline in place with no re-queue and no parking. [INV-16]

**Case: the re-door rebuilds the independence graph**

3. *when* a mid-work re-door creates a surface or state that did not exist when the lanes were opened, the system *shall* re-run the independence edges against every rolling lane. [INV-131]
4. *when* a new edge appears, the system *shall* pull the re-doored lane back to serial behind the lane it now shares a surface with and *shall* say so on the departures board, so the board never asserts a stale independence after the ground moved. [INV-131]

---

## Requirement 42: A fix touching a spec-backed literal owes its docs and test the same session

**Context:** The bug door and the skip door carry one added tripwire, fired by the door step before any code: does this edit touch a spec-backed literal or clause — a version string, a pinned count, a named vocabulary, a promised wording? The tripwire reads the edit's content, so a one-word change to a spec-cited literal owes the same duty as a full feature.

**User Story:** As a person making a one-line fix to a spec-backed literal, I want its docs and test to land in the same session, so that the size of the diff grants no exemption from the duty a full feature owes.

### Acceptance Criteria

**Case: the literal tripwire binds the same-session duty**

1. *when* the door step reads that an edit touches a spec-backed literal or clause, the system *shall* land the documentation update and the red-first test in the same session as the fix. [INV-104]
2. The system *shall* read the edit's content for the tripwire, so a one-word change to a spec-cited literal owes the same duty as a full feature whatever the size of the diff. [INV-104]

---

## Requirement 43: Every request enters through a three-source impact read, and the footprint decides the route

**Context:** Beside the door and the work-kind, a third dimension is read at the same intake moment: the footprint, read from three sources at once. The spec says what behaviour changes, the architecture says which module owns it, and the code says what actually gets touched. The read produces one named footprint that sizes how far each step reaches, and it re-classifies mid-work when an edit reaches past its named layer.

**User Story:** As a person handing over a request, I want its footprint read from spec, architecture, and code and written in the row, so that a wrong route is catchable after the fact and the change spends effort matched to its reach.

### Acceptance Criteria

**Case: the read names one footprint**

1. *when* a request is captured, the system *shall* read its footprint from the spec, the architecture, and the code at one intake moment and *shall* name one footprint — presentation-only, single-module, or cross-cutting. [INV-128]
2. *when* the footprint is named, the system *shall* speak it in the capture echo and write it in the row's footprint note beside the door, kind, and map notes. [INV-128, INV-43, INV-108]

**Case: the footprint composes with the door**

3. The system *shall* let the door decide which steps run and the footprint decide how far each step reaches, and *shall* never let the footprint promote a feature past the spec step nor demote the door's verdict. [INV-128, INV-16]
4. *when* the footprint is cross-cutting, the system *shall* open the full pipeline from the spec step across every layer the change moves; *when* it is single-module, the system *shall* scope the steps the door grants to the one owned module; *when* it is presentation-only, the system *shall* take the lightest road the door already grants. [INV-128]

**Case: disagreement is routed to its owning home**

5. *when* the three sources disagree, the system *shall* name the disagreement, *shall* route it to the home that owns it, and *shall* pick no winner in silence. [INV-128, INV-37]
   - code past spec routes to a bug row;
   - a moved pin routes to a spec fix;
   - a missing node routes to a restructure row.
6. The system *shall* let the three-source read tell whether a proven artifact already settles a question, so the only fork the human hears is what the three sources leave open. [INV-128, INV-121]

**Case: the footprint re-classifies mid-work**

7. *when* an edit reaches past its named layer, the system *shall* stop the work, read the footprint again, and record in the delivery report the footprint held or re-classified to a named footprint at a named step. [INV-128]
8. The system *shall* read repeated cross-cuts on the same module pair as the signal to move a boundary, moving it only through the architecture step and its re-prove on the recorded-footprint evidence. [INV-128, INV-37]

---

## Requirement 44: A landed feature-or-refactor row carries its footprint note, held by a suite check

**Context:** The footprint the intake read named is written in the landing row's footprint note. A suite check reads the queue and reddens a landed feature-or-refactor row that carries no footprint note, the mechanical floor under the footprint read.

**User Story:** As a person trusting the routing record, I want a landed feature-or-refactor row's footprint note held by a suite check, so that a landed row never silently drops the note.

### Acceptance Criteria

**Case: the note and its check**

1. The system *shall* write the intake read's footprint — presentation-only, single-module, or cross-cutting — in the landing row's footprint note beside the door, kind, and map notes. [INV-134, INV-128]
2. *when* the suite check reads the queue, the system *shall* red a landed feature-or-refactor row that carries no footprint note, the same shape the delegation-accounting check gives the routing rule. [INV-134, INV-103]

**Case: the duty binds forward**

3. The system *shall* require the footprint note only on a feature-or-refactor row landed once the impact-analysis station was law, leaving rows that landed before it as they landed. [INV-134, INV-159]

---

## Requirement 45: A request enters at the highest document it reaches, and the door set is closed

**Context:** A request enters the pipeline at the highest document in the derivation chain — spec, then architecture, then test matrix, then code, then docs — whose sentences must change for the request to be satisfied. The set of entry points is closed on purpose, so a request that matches no kind becomes one plain question, its route named by the human.

**User Story:** As a person handing over a request of any shape, I want it entered at the highest document its change reaches with the door set closed, so that no gap opens between the layers and an unmatched request becomes a plain question.

### Acceptance Criteria

**Case: the entry test**

1. *when* a request is captured, the system *shall* enter it at the highest document whose sentences must change to satisfy it, testing each document from the top by whether any sentence would read differently once the request is done. [INV-151]
2. *when* a technically-phrased request trips a surface, state, or unbacked-behaviour tripwire, the system *shall* lift it to the spec at the door rather than after the architecture work is built on an unlifted premise. [INV-151, INV-16]

**Case: the closed set of entry points**

3. The system *shall* route each request-kind to its own entry. [INV-151, INV-104, INV-17, T-20]
   - a product-behaviour request goes to the spec;
   - a defect goes to the test matrix with a red-on-bug test;
   - a docs-only change goes to its light path;
   - a tiny reversible edit goes to the skip shortcut, still owing the spec-backed-literal tripwire;
   - a settings value goes to the settings ladder;
   - an outside request goes through the inbox as one wish;
   - an ask to see or try a thing goes through the labelled-sketch door;
   - a thing handed back goes through feedback-intake.
4. *if* a request matches no kind in the closed set, *then* the system *shall* make it one plain question to the human, its route settled by the answer, and *shall* treat a held backlog item that cannot say why it belongs to the human as the same shape of finding. [INV-151, INV-4, INV-152]

---

## Requirement 46: When the product and the spec diverge, the spec is the definition of correct

**Context:** A divergence between the product and the spec defaults to a possible error in the product, checked against the spec. The divergence is first named and routed to the home that owns it. Changing a spec that is confirmed the error is a decision the human's word settles, and the spec is never silently rewritten to match the product.

**User Story:** As a person whose product and spec have drifted apart, I want the spec held as the definition of correct and any change to it made a decision, so that a wrong product is fixed while the spec is never quietly rewritten.

### Acceptance Criteria

**Case: the divergence is named and routed**

1. *when* the product and the spec diverge, the system *shall* first name what the spec states, what the product does, and why they differ, and route the divergence to the home that owns it. [INV-144, INV-37]
2. *when* the product is wrong against the spec, the system *shall* fix the product to the spec. [INV-144, INV-124]

**Case: completing a silent spec, changing a confirmed-wrong spec**

3. *when* the spec is silent where the product is correct, the system *shall* complete the spec to state the guarantee, pin it with a test, and report the completion as a default on the ordinary spec-delta road, and *when* what counts as correct is itself genuinely open, the question goes to the person, whose word alone settles it. [INV-144, INV-18, INV-31]
4. *when* the spec conflicts with a correct product, the system *shall* change the spec only *when* the spec is confirmed the error and the human has understood the divergence and confirmed the change, and *shall* never silently rewrite the spec to match the product. [INV-144, INV-9, INV-4]

---

## Requirement 47: The intake line names the work-kind

**Context:** The intake line also names what is being built. The work-kind says what kind of thing the work produces and which pipeline machinery is warranted, drawn from four kinds: product, infra, skill, and prose. The classifier calls the kind from what the wish produces, one kind per wish.

**User Story:** As a person throwing a wish, I want its work-kind named at intake, so that each pipeline step spends machinery matched to what the work produces.

### Acceptance Criteria

**Case: one kind per wish**

1. *when* a wish is captured, the system *shall* name its work-kind — product, infra, skill, or prose — from what the wish produces, one kind per wish. [T-16]
2. *when* a wish genuinely produces two kinds, the system *shall* split it into two wishes at intake, and *when* the classifier cannot call the kind, *shall* ask the human the same as an uncallable size. [T-16, INV-12]

**Case: the host default and the curated vocabulary**

3. *when* a host has one usual kind, the system *shall* let the host record it as a host-profile default the intake line starts from, and *when* a host's wishes span kinds, *shall* record no default and call each wish on its own. [T-16, E-8, E-13]
4. The system *shall* curate the kind vocabulary by real routed work, admitting a fifth kind only with a named wish the four failed to serve and re-justifying the set at milestones. [T-16]
5. The system *shall* require no retroactive kind on a row queued before the kind axis existed, letting it name its kind the moment it next moves. [T-16, INV-159]

---

## Requirement 48: A duty binds forward from the first landing after its clause exists

**Context:** A rule this project adopts governs from the first landing that touches its surface once the rule is law, and what already landed stays as it landed. A backlog item queued before the clause carries the rule the moment it next moves, and a project that predates the clause brings the rule up as an owned landing. This is the one statement of the forward-binding convention every such duty cites.

**User Story:** As a person adopting a new rule, I want it to bind forward from the first landing that touches its surface and never reach back over what already landed, so that existing work is not retroactively judged and every binds-forward citation has one home.

### Acceptance Criteria

**Case: the forward-binding convention**

1. *when* a rule becomes law, the system *shall* govern from the first landing that touches its surface and *shall* leave what already landed as it landed. [INV-159]
2. *when* a backlog item was queued before the clause, the system *shall* owe no retroactive backfill, letting the item carry the rule the moment it next moves, and *shall* bring the rule up as an owned landing on a project that predates the clause. [INV-159]

**Case: the citation net**

3. The system *shall* have each duty that binds forward — the work-kind axis, the success-measure and lens-sweep duties, the spec-and-architecture pair and its quality budgets, the runtime and placement views, and each self-enforcing landing rule — cite this one law rather than restate it. [INV-159, T-16, INV-15, INV-41, INV-74, INV-75]
4. *when* a clause states that a duty binds forward and cites no root, the system *shall* make the bare citation the finding a standing net catches, the same enforced membership the suite-honesty class carries. [INV-159, INV-160, INV-163, A-3]

---

## Requirement 49: A skill-kind wish's verify walks the skill-creator review

**Context:** When the classifier names the work-kind skill — a pack skill created or edited — the verify step additionally runs the installed skill-creator's review of the touched skill: its craft and its evals where applicable. The classifier is the trigger, and the walk fires on every skill-kind landing.

**User Story:** As a person shipping a skill change, I want its verify to walk the skill-creator review, so that a regression in a skill every session reads is caught before it lands.

### Acceptance Criteria

**Case: the walk fires on every skill-kind landing**

1. *when* the classifier names the work-kind skill, the system *shall* run the installed skill-creator's review of the touched skill at the verify step, folding or rejecting each finding by name in the landing record. [INV-99]
2. The system *shall* fire the walk on every skill-kind landing from the classifier alone, and *shall* leave skills that landed before this law to the milestone gate's whole-pack walk. [INV-99, M-1]

---

## Requirement 50: The kind scales the steps and never silently skips one

**Context:** The door picks which steps run; the kind picks the form each running step takes, never whether the pipeline runs at all. At landing, every pipeline step has either applied in the form the kind's table states or stood down by name in the delivery report, so a skipped step is a written fact.

**User Story:** As a person shipping a change of any kind, I want the kind to scale each step's form while every step applies or stands down by name, so that a small change spends proportionate effort and no mandatory check is silently dropped.

### Acceptance Criteria

**Case: the kind adjusts form, never presence**

1. The system *shall* let the door pick which steps run and the kind pick the form each running step takes, never letting the kind decide whether the pipeline runs. [INV-22, T-12]
2. *when* a wish lands, the system *shall* have every pipeline step either applied in the form the kind's table states or stood down by name in the delivery report. [INV-22, E-12]
3. *while* the kind question stays open on a row, the system *shall* apply every step in full, since standing a step down requires a named kind to account for it. [INV-22, INV-12]

**Case: the checks no kind may change**

4. The system *shall* let no kind change the door law and its tripwires, the delta's mandatory sentences the scope-cut law names (the law, stated in the intake stretch of this build loop, that a scope cut spares the regression fences, a kept surface's facets, the non-goals, and the success measure), or ask-at-intake. [INV-22, T-12, INV-16]

---

## Requirement 92: Deferred rows are revisited at every queue-take

**Context:** A deferred row carries a revisit trigger, and a time-bound one can come true and lapse in the gap between two milestone gates. So the milestone re-scan is not the trigger's only reader: at every queue-take the session also re-scans each deferred row's revisit trigger against the current moment, and a fired trigger returns its row to the runnable head right then.

**User Story:** As a person with a time-bound deferral, I want its revisit trigger read at every queue-take and not only at milestones, so that a window that opens and closes between gates is caught by whichever cadence comes first.

### Acceptance Criteria

**Case: the two cadences read the same triggers**

1. *when* the session takes the queue, the system *shall* re-scan each deferred row's revisit trigger against the current moment and *shall* return a fired trigger's row to the runnable head. [INV-129, T-8, INV-49]
2. The system *shall* read the same triggers by the same rule at queue-take and at the milestone gate, so a deferred wish never waits on a trigger nobody reads, and *shall* keep the trigger vocabulary free-form since a reader now runs at queue cadence. [INV-129, M-1, INV-1]

---

## Requirement 93: A deferred item's own state is re-derived from the code before its work resumes

**Context:** A resume file and a queue row record a past moment, and the technical problem statement one item carries can go stale as the code it touches moves on. So a session resuming a deferred or queued item, before it designs anything, reads the code the item touches, confirms the problem still holds, and re-derives the item's real current state.

**User Story:** As a session resuming a deferred item, I want its own state re-derived from the shipped code before I design anything, so that I never build a fix from a stale model of code that has since moved and catch an item already handled.

### Acceptance Criteria

**Case: the resume-side re-read**

1. *when* a session resumes a deferred or queued item, the system *shall* read the code the item touches, confirm the problem the row describes still holds, and re-derive the item's real current state before it designs anything on the item. [INV-247, INV-129]
2. The system *shall* fire this read at the same resume moment as the deferral re-test that re-asks whether the item is still the seat's or the human's, owing both reads. [INV-247, INV-152]

**Case: no push gate holds it**

3. The system *shall* keep this a discipline the seat holds, since a resume is an in-session act at chat cadence with no committed artifact for a gate to scan, carried by the base rulebook's resume habit. [INV-247, INV-83]

---

## Requirement 94: The queue has a far tier the runnable report stands down by name

**Context:** A wish can be worth keeping while carrying no plan to run and no event that would bring it back. Such a row takes the far status, and a far row is not a deferred one: a deferred row carries a revisit trigger the queue-take re-scans, while a far row carries no trigger and returns only when the person asks or the rare self-surfacing line offers it.

**User Story:** As a person keeping a far backlog, I want far rows told apart from deferred ones and left out of the runnable report, so that the what's-left report notes the far tier in one line rather than naming its rows among runnable work.

### Acceptance Criteria

**Case: far and deferred told apart**

1. The system *shall* give a row worth keeping with no plan to run and no event that would bring it back the far status, distinct from a deferred row whose revisit trigger the queue-take re-scans. [INV-222, INV-129]
2. The system *shall* read the boundary both ways — a far row carrying a revisit trigger is a deferred row wearing the wrong token, and a deferred row carrying no trigger leaves the re-scan nothing to read. [INV-222]

**Case: the runnable report stands the tier down**

3. *when* the what's-left report or the feature-map answer reads the runnable queue, the system *shall* stand the far tier down by name, rather than name its rows among runnable work. [INV-222, INV-223, INV-206, E-3]
   - that one line states that a far backlog exists, its count, and that the whole tier prints on request.
4. *when* a report names a far-tier row among the runnable what's-left, the system *shall* red the report-shape check, which rides the suite and not the push chain since the status report is a chat surface with no committed file to gate. [INV-222, INV-83]

---

## Requirement 95: A deferred row can carry a mechanical revisit trigger

**Context:** A deferred row's revisit trigger is usually prose a reader judges at the queue-take. Where the awaited event is mechanically observable, the trigger is a check the queue-take runs. The worked instance is the day the harness gains a listener, a component that lets one session push a message directly to another running session in place of the inbox's file drop. The row deferred on that day carries a mechanical trigger the queue-take reads.

**User Story:** As a person deferring work on a mechanically observable event, I want its revisit trigger to become a one-shot check the queue-take runs, so that the row returns the moment the event fires and stays silent until a real record carries the field.

### Acceptance Criteria

**Case: the mechanical trigger and its check**

1. *when* a deferred row's awaited event is mechanically observable, the system *shall* make its revisit trigger a check the queue-take runs rather than prose a reader judges. [INV-231, T-8, INV-129]
2. The system *shall* fire the listener-tripwire check only on a session record carrying a non-empty socket field — the record's field naming the address a listener would serve — and stay silent on an empty or absent one, so a listenerless harness leaves it quiet. [INV-231, INV-183]

**Case: it rides the queue-take scan**

3. *when* the check fires, the system *shall* return the row to the runnable head, and *shall* ride the queue-take scan and the suite with no push-gate letter. [INV-231, INV-129, INV-222, INV-83]
   - the far-tier check likewise takes no push-gate letter;
   - a queue-cadence read is no committed file for a push gate to scan.

---

## Requirement 96: A wish can end without landing in one of three end-states

**Context:** A wish can end without landing, and its row stays in the table in one of three end-states: *declined* when the human said no, *deferred* when parked with a named revisit trigger, or *superseded* when absorbed by another wish so the row points to the absorbing one. A superseded wish never dies by pointer. The far status is a resting state: a far row stays kept in the queue with no exit event and returns on the person's ask, so the end-state list stays at three.

**User Story:** As a person whose wish ends without landing, I want it settled into one recorded end-state with what it absorbed preserved, so that a declined or superseded wish still reaches a named terminal state and nothing it held is lost.

### Acceptance Criteria

**Case: the three end-states**

1. *when* a wish ends without landing, the system *shall* keep its row in the table as declined, deferred, or superseded, a superseded row pointing to the absorbing wish. [T-8]
2. *when* a wish that other rows were superseded into is declined, the system *shall* list those rows at its decline, preserving what the declined wish had absorbed. [T-8, INV-1]

**Case: each absorbed row is settled by name**

3. *when* a wish is declined, the system *shall* either decline each listed row by name where the human's no covered it or return it to the queue as its own row where the no was about the absorber's shape, never letting a superseded wish die by pointer. [T-8, INV-1]

**Case: the terminal-exit vocabulary**

4. The terminal exits — the words a row leaving the queue's body is named by — *shall* be the closed lowercase set *landed*, *declined*, and *superseded*, and *deferred* *shall* stay a live status that keeps its row in the body. [T-8, INV-276]

---

## Requirement 252: The inbox is the parallel-safe door: one committed file per outside item

**Context:** The inbox is the parallel-safe intake door for wishes and feedback born outside a pack session. Each item arrives as exactly one new file, named by date, source, and slug, since creating a fresh file cannot collide while a shared file can. An agent's own deposit names its source in the filename, and two source words are reserved.

**User Story:** As a person or agent handing an item to the pack from outside, I want each item to land as one new committed file naming its source, so that the deposit races nothing and the receiving gate reads who sent it.

### Acceptance Criteria

**Case: one new file per item**

1. *when* an outside item arrives, the system *shall* place it as one new file named `YYYY-MM-DD-<source>-<slug>.md`, and *shall* never edit an existing file, since a fresh file cannot collide. [E-11]
2. *if* the name is taken, *then* the system *shall* append a numeric ordinal, and *when* two sessions race one slug *shall* add a short session token to the existing source mark, keeping one identity scheme. [E-11, INV-117]

**Case: the deposit names its source**

3. The system *shall* have an agent's deposit name its source in the filename in the `from-<agent>` form the receiving gate reads. [E-11, INV-189]
4. The system *shall* reserve two source words — the owner's own wish and a stranger's bridged item — both owing no birth record, and *shall* treat an agent-initiated message as a proposal until the owner ratifies it. [INV-189, INV-193]

---

## Requirement 253: The inbox's remote and local arms

**Context:** The inbox opens to seats that share no filesystem and to sessions that share one. A remote seat reaches the repository only through git and deposits one new file committed touching the inbox alone, then pushes under a recorded grant. A co-located session shares one git index, so it writes its one file and stops there, never staging or committing. Each arm fails honestly when it lacks the grant or reach it needs.

**User Story:** As a person depositing from a remote seat or a co-located session, I want each arm to add exactly one new inbox file under its own safe path, so that the deposit races nothing and a missing grant fails by naming the one action that supplies it.

### Acceptance Criteria

**Case: the remote arm**

1. *when* a remote seat deposits, the system *shall* commit one new inbox file touching the inbox alone with the source named, and *shall* push it under a per-repository grant recorded in the host profile. [INV-112, INV-82]
2. *if* a remote push is rejected, *then* the system *shall* retry after a pull, and *shall* never edit an existing file. [INV-112]
3. *if* a remote seat holds no grant, *then* the system *shall* fail honestly, naming the grant it lacks and the one action that supplies it, and *shall* never guess a workaround. [INV-112, INV-67]

**Case: the local co-located arm**

4. *when* a session shares the assigned session's working tree, the system *shall* deposit by writing its one new inbox file and stopping there, with no staging, no commit, and no push. [INV-174]
   - the assigned session's sweep commits the harvest.
5. The system *shall* read a fresh untracked inbox file as the fence's expected benign case, and a co-located neighbour's stage or commit as a fence stop. [INV-174, INV-11]

**Case: the remote read arm**

6. *when* a remote consumer reads a private producer repository, the system *shall* require a read grant, recorded beside the push grant as the profile field `trust.read-grant`, and *shall* fail honestly naming the read grant it lacks rather than guess. [INV-232, INV-187]

**Case: the stand-down holds no bar over the deposit**

7. The system *shall* hold that the live-session stand-down holds no bar over the deposit, the one additive inbox file racing nothing. [INV-112, INV-82]

---

## Requirement 254: The inbox's stranger arm and its monitor

**Context:** A stranger holds no grant but can open an Issue or Discussion. The git deposit is closed to them, so the stranger's door is a templated Issue or Discussion that requests a source, and one scheduled monitor converts each open un-surfaced item into one committed inbox file. From that file on, the item is an ordinary inbox wish. The monitor surfaces an item once per activity generation and answers the stranger on the source.

**User Story:** As a stranger with no write path, I want my Issue bridged into one inbox file and answered on its source, so that my wish reaches the queue exactly once and I learn it was heard and where it went.

### Acceptance Criteria

**Case: the monitor bridges the item**

1. *when* the monitor sees an open un-surfaced stranger item, the system *shall* convert it into one new inbox file naming the source Issue and its source field and commit it, touching the inbox alone. [INV-146]
2. The system *shall* keep a stranger's wish off the queue and the repository, the monitor and the sweeping sessions owning every write so no wish is lost. [INV-146, INV-1]

**Case: surfaced once per generation**

3. The system *shall* surface an item at most once per activity generation, reading the generation from comments that are not its own markers, so its own claim and confirm never read back as fresh activity. [INV-146]
4. *when* a swept item's activity generation is newer than the one last recorded, the system *shall* surface it afresh as a new inbox file. [INV-146]

**Case: the item is answered on its source**

5. *when* the sweep judges a surfaced item a wish, the system *shall* harvest it into a queue row and post the capture echo — what was heard, its door, its name, its row — as a comment on the source Issue. [T-10, INV-27]
6. *when* the row reaches a terminal exit, the system *shall* close the source Issue as the convergence an answered question reaches, a surfaced item judged no wish being closed with a recorded note. [T-20, INV-59]

**Case: the monitor's own single-instance law**

7. The system *shall* run the monitor as a single instance per host under a lock stolen by age near 1 hour, and *shall* fail a run that cannot reach the repository honestly, dropping no wish. [INV-147, INV-67]
8. *when* the pack repository runs its monitor, the system *shall* run it as a scheduled action pushing inbox commits only under a single-instance concurrency group, riding the inbox-only carve-out the push gate already grants. [INV-148, M-6]

---

## Requirement 255: Two hosts watching one repository converge on a single surfacing

**Context:** The single-instance lock holds inside one host. Where two hosts' monitors watch one repository, both can read a stranger item as owing a surfacing in the same window, and with no coordination each deposits its own file. The hosts already share the source item, so it carries the claim: a host posts a claim comment, re-reads the claims, and deposits only when its own claim is the winning one.

**User Story:** As a maintainer whose repository two monitors watch, I want the shared source item to carry a claim that picks one winner, so that two hosts converge on one surfacing and a dead winner delays rather than swallows the wish.

### Acceptance Criteria

**Case: the claim picks one winner**

1. *when* a host means to surface an item, the system *shall* post a claim comment carrying its host identity under a hidden marker, re-read the claims, and deposit only when its own claim wins. [INV-149, INV-117]
2. The system *shall* compute the winner identically on every host as the earliest claim by comment creation time, the lower host identity breaking a tie. [INV-149]

**Case: a dead winner is stolen by age**

3. *if* a claim is older than the stale bound the lock uses, *then* the system *shall* read it as abandoned so the next surviving host surfaces the wish. [INV-149]
4. The system *shall* keep a losing host standing down for the round and retrying on its next run, so one wish reaches the shared inbox once. [INV-149]

**Case: the claim rides the writes already held**

5. The system *shall* ride the claim on the comment writes the monitor already holds, asking no new grant, the claim marker staying distinct from the surfaced-generation record. [INV-149, INV-146]
6. *if* a run cannot reach the item to claim it, *then* the system *shall* fail honestly and retry, dropping no wish. [INV-149, INV-67]

---

## Requirement 256: The concurrent-edit fence, the harvest, and one canonical state directory

**Context:** Before writing to a repository, and again before every commit, the agent re-checks the repository's head and tree against what it last read; a moved head or an unexpected change stops it. A pack session sweeps the inbox first, harvesting each file into the home its route owns in one commit that both lands the route and removes the file. The host keeps one canonical state directory, and overlapping lanes default to worktree isolation.

**User Story:** As a person whose repository two sessions might share, I want the fence checked before every write and the harvest atomic, so that concurrent work cannot scramble the tree and every inbox item is harvested exactly once with nothing lost.

### Acceptance Criteria

**Case: the fence before every write**

1. *when* the repository head has moved or the tree holds changes the agent did not make, the system *shall* stop, re-read the changed files, and proceed surgically or back off to the inbox. [INV-11]
2. The system *shall* read a new inbox file as the expected benign case, and *shall* never push while another session is known live in the repository. [INV-11]

**Case: the atomic harvest**

3. *when* a pack session opens, the system *shall* sweep the inbox first and harvest each file into the home its route owns in one commit that both lands the route and removes the file. [T-10]
4. *if* a harvest is interrupted, *then* the system *shall* commit nothing and leave the file for the next sweep, which harvests it once. [T-10]

**Case: one canonical state directory**

5. The system *shall* keep one canonical state directory named `.live-spec`, and *shall* retire a near-miss look-alike to the attic under a manifest line naming the path, the reason, and the canonical directory. [INV-105, INV-7]
6. *when* two lanes' write-sets overlap, the system *shall* default the later lane to worktree isolation, its copy reaching the shared tree only through integration under the pen. [INV-105, INV-39, T-18]

**Case: the one-file diff carve-out**

7. *when* a push's diff is exactly one new inbox file, the system *shall* have it owe the fence and no re-check record, more riding the full gate. [INV-11, INV-112]

---
