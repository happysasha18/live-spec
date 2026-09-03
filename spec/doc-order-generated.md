## Requirement 1: The spec keeps what is built apart from what is planned

**Context:** The spec states what is built and working today apart from what is only planned, and it keeps a reader from mistaking one for the other. A planned feature carries the target tag on a line of its own, and the tag never spreads to the section around it. The suite ties each target tag to the queue row that builds it — a row still open, awaiting its landing — so the marker is enforced by the suite.

**User Story:** As a reader of the spec, I want a planned feature marked by a target tag the suite enforces, so that I never mistake a promised surface for a working one.

### Acceptance Criteria

**Case: built and planned are marked apart**

1. The spec *shall* state what is built and working today apart from what is only planned, marking each scenario and its named promised parts apart, so a scenario that holds built parts beside planned ones states a status for the scenario and for every named promised part. [S-0]
2. The system *shall* carry the target tag on a line of its own and *shall* keep it off the section around it. [S-0]

**Case: the suite ties each tag to its building row**

3. The system *shall* tie each target tag to the queue row that builds it, that row still open and awaiting its landing, and *shall* red the suite *if* that row ships with the tag still on, *if* the tag vanishes, or *if* the tag was never named. [S-0]
4. The system *shall* mark as planned the design-sync machine. [E-18]
   [target]

---

## Requirement 97: What the wishes grow is the spec

**Context:** What the wishes grow is the spec, the living statement of what the product is, where one surface carries one name everywhere.

**User Story:** As a person reading what the wishes built, I want them to grow one living spec with one name per surface, so that the whole team reads one current truth rather than scattered descriptions.

### Acceptance Criteria

**Case: one living statement, one name per surface**

1. The system *shall* grow the spec as the living statement of what the product is, naming each surface one way everywhere. [E-4]

---

## Requirement 118: The architecture document names the nodes that own the spec's facts

**Context:** The spec says what the product is, and tests prove facts about the shipped artifact; two documents sit between them, and if they stay implicit they get skipped. The architecture document describes how the product is built as a list of named nodes — pipeline stages, modules, surface owners. Each node carries one responsibility and one name, every spec fact belongs to exactly one node, and every pin comes from a command that was run. It is written from the proven spec and proved with the architecture lens before anything derives from it.

**User Story:** As a person bridging the spec to the tests, I want the architecture written as named nodes each owning its facts and pinned from a real command, so that the layer between spec and tests is written out in full.

### Acceptance Criteria

**Case: named nodes, one fact one owner**

1. The system *shall* have each architecture node carry one responsibility and one name, and *shall* have every spec fact belong to exactly one node. [E-14]
2. The system *shall* pin every node to its owning place by a named thing, and *shall* draw every pin from a command that was actually run. [E-14]
   - the named thing is a function, a marker comment, a selector, or a heading;
   - a drift check resolves the name and re-greps it fresh, catching a moved line.

**Case: the architecture lens proves it**

3. *when* the architecture is written, the system *shall* prove it with the architecture lens at the project's kind scale, checking that every spec fact has an owning node, that no node stands without spec backing, and that every seam between nodes is named. [E-14]
4. The system *shall* have the lens check that the quality budgets are stated with their instrumentation homes and watchers, that the runtime view walks every promised flow, and that the placement view says where every node runs. [E-14, INV-41, INV-74, INV-75]

**Case: keeping the doc current**

5. *when* a surface-class wish lands, the system *shall* update the doc before the matrix is touched, a bug or small wish citing the node it lands in, and a fact with no owner being assigned to the nearest fitting node with no re-prove triggered by the assignment alone. [E-14]
6. *when* the structure is re-carved, the system *shall* carry the re-carve as its own row under a restructure placement and re-prove it, the doc mapping the product as it stands plus the landing in flight and never a speculative node built milestones ahead. [E-14, INV-37, INV-18]

---

## Requirement 119: Every new or carved node passes a three-question fitness test

**Context:** Before an extraction or a new node stands, it answers three questions: can it be tested alone, does a real second place need it, and can it and its neighbour be worked in parallel without queuing on shared files. Three yes answers make the node right; a single no is a flag to answer before the carve stands; two or more no make it premature. The prover's speculative-node flag is this flag raised on the second question.

**User Story:** As a person growing the architecture, I want each new node to answer three fitness questions at its birth, so that the architecture only grows a part that earns its place.

### Acceptance Criteria

**Case: three questions at birth**

1. *when* a node is born or carved, the system *shall* have it answer whether it can be tested alone, whether a real second place needs it, and whether it and its neighbour can be worked in parallel without queuing on shared files. [INV-122]
2. *if* one answer is no, *then* the system *shall* raise a flag to answer before the carve stands — naming the plan that turns it to a yes or folding the carve back — and *if* two or more answers are no *then* the system *shall* read the node as premature. [INV-122]

**Case: the prover shares the flag**

3. The system *shall* have the prover flag a node with one caller and no promised second on the second question, never auto-rejecting it, so the birth gate and the prover agree. [INV-122]

---

## Requirement 120: A deliberate redesign re-shapes the architecture document

**Context:** When structure is deliberately redesigned — layers restacked, a surface's ownership moved, nodes merged or split — the architecture document is re-shaped to the new form and re-proven in the same movement. Updating the pins alone is scoped to a boundary shift that leaves the document's shape standing; after a real redesign the old shape itself lies.

**User Story:** As a person redesigning structure, I want the document re-shaped and re-proven in the same movement, so that fresh pins never sit on a stale shape.

### Acceptance Criteria

**Case: re-shape, do not just re-pin**

1. *when* structure is deliberately redesigned, the system *shall* re-shape the architecture document to the new form and re-prove it with the architecture lens in the same movement. [INV-113]
2. The system *shall* scope the pins-only path to a boundary shift that leaves the document's shape standing, treating fresh pins on a stale shape after a redesign as a defect, the re-carve routing carrying such a redesign as its own row. [INV-113, INV-37]

---

## Requirement 121: The architecture owes numbers, not just names

**Context:** The document states measurable quality budgets for what it builds, each with its instrumentation home — where the number is measured and where a human reads it — and each budget names its watcher, the mechanical check that reds past the stated number. What is measurable depends on the project's kind, so the author asks what quality means here in numbers before writing any. The numbers are the host's taste, proposed by the architecture and set on the human's word.

**User Story:** As a person guarding quality, I want each budget stated with its instrumentation home and a watcher, so that a budget cannot silently rot and a quality with no honest number is said by name and its gap owned.

### Acceptance Criteria

**Case: a budget, its home, and its watcher**

1. The system *shall* state each measurable quality budget with its instrumentation home and *shall* have each budget name its watcher, the mechanical check that reds past the stated number, or a decided sentence naming why it is read by eye. [INV-41, INV-59]
2. *when* a budget carries neither a named watcher nor that decided sentence, the system *shall* read it as a derivation defect, flagged like an unowned fact, the watcher holding it the way the suite wall-time budget was held once it earned its gate. [INV-41, INV-164]

**Case: what is measurable follows the kind**

3. *when* the architecture writes a budget, the system *shall* read the measurable dimensions from the project's kind. [INV-41, INV-36, INV-226]
   - a user-facing product is measured by paint and interaction times;
   - a backend service is measured by latency, throughput, and error rate;
   - a pipeline is measured by run time and per-unit cost;
   - a skill pack is measured by eval pass rate and suite wall-time;
   - prose is measured by an honest number;
   - these kinds form a closed set, and each is named in this criterion.
4. *where* a quality has no honest number, the system *shall* say so by name rather than invent a vanity metric, and *shall* count a budget only once a matrix row at the right level can see it. [INV-41]

**Case: the numbers are the host's taste**

5. The system *shall* have the architecture propose the numbers with a recommendation and *shall* set them on the human's word at the surface's first budget landing, the duty binding forward from that landing. [INV-41, INV-159]

---

## Requirement 122: The architecture walks each flow at runtime

**Context:** The spec's person-facing scenarios are flows. The feature-coverage table names which nodes implement a feature; the runtime view shows how. For every flow the spec promises, the document walks the running product — which node serves each step, what data crosses at each hop, where the flow can fail, and what happens then. Every named failure point carries its fallback.

**User Story:** As a person tracing a promised flow, I want the architecture to walk it hop by hop with a fallback at each failure point, so that a flow it cannot walk end to end surfaces as a finding.

### Acceptance Criteria

**Case: one walk per flow**

1. *when* the spec promises a flow, the system *shall* walk the running product for it, in one short walk per flow. [INV-74, E-29]
   - the walk names which node serves each step, what data crosses at each hop, and where the flow can fail;
   - the walk is written as a table row or a numbered line per hop.
2. The system *shall* have every named failure point carry its fallback — a degrade, a retry, a guard — so that a failure point with no fallback sentence reads as an unfinished walk. [INV-74]

**Case: a flow that cannot be walked is a finding**

3. *when* the document cannot walk a flow end to end, the system *shall* read it as a finding — a missing node or an unnamed seam — the view scaling by kind so a book's one sentence per flow satisfies the duty. [INV-74, INV-36, INV-159]

---

## Requirement 123: The architecture says where everything runs

**Context:** Every node states its place — build-time on the author's machine, a static file on a content-delivery host, the client browser, an edge worker, an external service. Where a load-bearing technology choice exists, the place names it, and the same table says where secrets live and which tier holds each verdict that must not be decided on the client. The document reads tiers-first, opening with the shape at a glance.

**User Story:** As a person asking where a node runs, I want every node's place first-class and the document opening tiers-first, so that a reader answers where-does-this-run at a glance and a secret's tier sits in the architecture itself.

### Acceptance Criteria

**Case: every node states its place**

1. The system *shall* have every node state its place and name the load-bearing technology choice where one exists, and *shall* say in the same table where secrets live and which tier holds each verdict that must not be decided on the client. [INV-75]
2. The system *shall* make the placement first-class in its own table, the placement view, so a reader answers where a node runs at a glance. [INV-75]

**Case: tiers-first reading, scaled by kind**

3. The system *shall* open the document with the tiers named in a few lines, then the nodes, then the flows walking those tiers, then budgets, so a reader lands oriented before any table detail. [INV-75]
4. The system *shall* scale both views by the project's kind, and the duty *shall* bind forward from the first landing that touches the architecture. [INV-75, INV-36, INV-159]
   - a book project satisfies each view with one sentence;
   - a fullstack or data project owes both views in full.

---

## Requirement 124: The matrix is derived, and no wish jumps the bridge

**Context:** The matrix organizes rows by architecture node and spec fact, a structured grid where every fact gets at least one row and every row pins a test level. Derivation closes with the coverage validation, a checklist walked to confirm the rows are complete. While both layers live, no wish lands whose facts lack an owning node and a matrix row at the right level.

**User Story:** As a person crossing from spec to tests, I want the matrix derived and the coverage validation walked, so that no fact ships without a row at the right level and no wish jumps the bridge.

### Acceptance Criteria

**Case: the matrix is derived by node and fact**

1. The system *shall* organize the matrix by architecture node paired with spec fact, giving every fact at least one row and pinning each row to a test level. [E-5, E-14]
2. The system *shall* close the derivation with the coverage validation. [E-15, INV-6]
   - it confirms every spec anchor owns at least one row;
   - it confirms every artifact-inventory entry owns at least one row at a rendered tier of the level ladder, browser-computed or pixel;
   - it confirms every visibility, layout, colour, or interaction fact sits at browser-computed level or above;
   - it confirms every node carries its negative-side rows;
   - when the test-matrix conversion delivery lands, the matrix row lint and the matrix-reference gate stand as the derivation's mechanical close, and the hand-walked checklist retires with its section.
3. The system *shall* retire a stale row that cites an anchor or node no longer present rather than let it vanish, and *shall* read a fact with no row, or a row at too weak a level, as a derivation defect the prover catches before any user hits it. [E-15]

**Case: no wish jumps the bridge**

4. The system *shall* land no wish whose facts lack an owning architecture node and a matrix row at the right level. A project predating these layers *shall* bring them up as an owned landing. [E-14, INV-159]
   - the invariant binds from the landing that creates the architecture document and matrix.

---

## Requirement 223: The test matrix covers every fact both ways

**Context:** The test matrix is where "it works" is made accountable. Its rows are keyed by architecture node and spec fact, and coverage is total: no fact stands without a row, and no row stands without a pinned test level. Each row states both what the fact does and what it must never do, and that negative side is the regression fence.

**User Story:** As a person trusting a green suite, I want every fact to carry a matrix row pinned to a level and a stated negative side, so that a passing suite proves the facts were checked at the right depth and guarded against regression.

### Acceptance Criteria

**Case: total coverage, keyed by node and fact**

1. The system *shall* give every spec fact at least one matrix row, and *shall* leave no row without a pinned test level. [E-5]
2. The system *shall* key each row by one architecture node paired with one spec fact, derived from the proven architecture. [E-14, E-15]

**Case: each row states both sides**

3. The system *shall* state on each row both what the fact does and what it must never do, the negative side standing as the regression fence. [INV-6]

---

## Requirement 224: The feature-coverage trace and its heading convention

**Context:** Above the test matrix sits a second traceability layer keyed to the project's primary unit. Each project declares its type once, and the type names the unit — a web product counts features, a command-line tool its commands, a package its guarantees, a book its arguments. One table in the architecture maps each unit to the nodes that implement it and a test that exercises it, and a heading convention gives the reverse check teeth.

**User Story:** As a person asking whether every promised unit is covered, I want a two-way trace keyed to the project's own unit, so that a unit without an implementer or a test, and a promised unit that forgot its tag, both go red.

### Acceptance Criteria

**Case: the trace maps each unit both ways**

1. The system *shall* map each declared unit to the node that implements it and a test that exercises it in one coverage table in the architecture. [E-29]
2. *when* the feature-coverage check runs, the system *shall* fail the push *if* a tagged unit resolves to no real implementer node or no real test, and *shall* fail it *if* a tagged unit carries a `[target]` marker. [INV-73]

**Case: every heading declares its status**

3. The system *shall* have a person-facing scenario the product performs today carry its feature tag on the requirement heading, and *shall* leave a machinery requirement's heading and a promised scenario's heading untagged. [INV-132]
4. *while* a scenario stands promised, the system *shall* keep it out of the coverage table and *shall* mark it with a `[target]` marker on its own line, and *shall* give it its feature tag in the same change that lands its build. [INV-132]

---

## Requirement 244: A node re-answers its fitness as it grows

**Context:** The three-question fitness test governs a node's birth, but a node born right and then grown carries a standing yes nobody re-reads. So each node re-answers the three questions at every architecture re-prove, and two nodes whose pins share one file answer the parallel-work question no by construction — which makes co-residence in one file the mechanical face of a failed growth answer. Raw size is rejected as the vanity metric: a large file owning one responsibility is healthy.

**User Story:** As a person watching an engine file swell, I want node co-residence counted and re-asked at re-prove, so that a file that has grown to hold several nodes is caught and a split is proposed before a standing yes passes forever.

### Acceptance Criteria

**Case: co-residence is the counted signal**

1. The system *shall* count nodes-per-file from the architecture's own pin column as the number of distinct nodes whose pins name a file, and *shall* reject raw size as the signal. [INV-233, INV-41]
2. *when* an architecture is re-proven, the system *shall* have each node re-answer the three fitness questions on its pins, and two nodes whose pins name one file *shall* answer the parallel-work question no. [INV-233, INV-122]

**Case: the ratchet and the proposal**

3. The system *shall* hold a ratcheted per-file node cap seeded at the tree's current count, and *shall* red any increase while the cap ratchets down only. [INV-233, INV-164]
4. *when* a file's node count sits at its cap, the design review *shall* carry the split proposal in its two-objects shape — one question brought to the person with both compared objects in hand — naming the over-grown file and the split it offers. [INV-233, INV-142]

**Case: a split is a structure change**

5. *when* a split is taken, the system *shall* carve it by the architecture step alone and re-prove it there. [INV-233, INV-37, INV-113]
6. The system *shall* read what counts as a code file from the project's declared layers. [INV-233, INV-135]
7. The node-growth check *shall* ride the suite as `tests/test_node_growth.py` and take no push-gate letter, the far-tier check the precedent. [INV-233]

---

## Requirement 246: The guards over the guards

**Context:** A gate can report green two ways: because the input was clean, or because it never fires at all. Four checks guard the gate machinery itself against that hollow class — the pushed gates must be mirrored into the remote check, every chat judge the pack declares wired must be wired into settings, every gate must carry a proof it can fail, and every path a permission rule names must still exist.

**User Story:** As a maintainer trusting the push gate, I want the gate machinery itself checked, so that no gate silently protects nothing — mirrored into the remote, wired into settings where the declaration says wired, provably able to fail, and pointed at real paths.

### Acceptance Criteria

**Case: the remote mirror carries every local gate**

1. *when* the push gate runs a gate letter locally that the remote mirror does not run, the system *shall* red, naming the gate and the one fix, a legitimate remote-skip living in `guardrails/ci-mirror.json` with its reason. [INV-210, M-5]
2. *if* a carve-out names a letter that is no local gate, *then* the system *shall* red it as drift. [INV-210]

**Case: every chat judge the declaration wires is wired**

3. *when* a hook under `hooks/` is not classified in the wired-hook declaration, or a wired hook is missing from its array in the installed settings, the system *shall* red, naming the hook, the surface, and the fix. [INV-211]
4. *where* the personal-layer settings cannot be read, the system *shall* stand the wiring check down by name rather than falsely pass. [INV-211, INV-175]

**Case: every gate carries a known-red proof**

5. The system *shall* require each pushed gate letter to be classified with a red-first proof driving its check to a non-zero exit, or a covered entry naming the gate it rides and the reason. [INV-212]
6. *if* a gate marker is classified nowhere, or a gate can by construction never be made to fail, *then* the system *shall* red it loudly. [INV-212]

**Case: a permission rule points at a real path**

7. *when* a filesystem path named inside a permission rule is absent, the system *shall* red the rule, reading absolute and home-rooted paths across the personal settings and the host's project settings, stripping a trailing glob to its literal ancestor, keeping a spaced path whole, and reporting the count of rules it resolved. [INV-216, INV-176]
8. *where* a settings file cannot be read, the perms arm *shall* stand down by name, and *shall* red a present-but-unreadable settings file rather than pass it falsely. [INV-216]

---

## Requirement 247: The snapshot baseline advances only at delivery

**Context:** The snapshot is the saved artifact of the last accepted run of a surface, and the next run diffs against it as the baseline. The baseline advances only at a delivery, and only for the surfaces the change declared; an undeclared surface keeps its old baseline. That asymmetry catches the unasked change.

**User Story:** As a person guarding against an unasked change, I want the baseline to advance only at delivery and only for declared surfaces, so that a rendered surface that differs but was never declared turns the scope check red.

### Acceptance Criteria

**Case: the baseline advances by declaration**

1. The system *shall* advance a surface's baseline only at a delivery and only for the surfaces the change declared, an undeclared surface keeping its old baseline. [E-7]
2. *when* a rendered surface differs from its baseline while the delivery never declared it, the system *shall* red the declared-scope check. [E-7, E-6]

**Case: the snapshot is tracked and recoverable**

3. The system *shall* keep the snapshot folder `.live-spec/snapshot/` git-tracked with one manifest line per surface, so any older baseline can be checked out, and *shall* keep only the last baseline in the working tree. [E-7]
4. *if* a surface's rendered bytes are too heavy to hold in git, *then* the system *shall* keep only its manifest line and content hash under git, hold the bytes outside git, and diff the next run against the hash alone. [E-7]
5. *when* adoption begins, the system *shall* save the first baseline from the artifacts as found, and *shall* narrow the pack's shared settings for one project only where the host profile records it. [A-6, E-8]

---

## Requirement 248: Design-sync mirrors declared components for team review

**Context:** Design-sync [target: the machine; the wiring is live] is an optional machine for hosts with visual components. It mirrors the components a delivery declared — the same declared scope the snapshot diffs by [E-7] — to the team's design project, where the human reviews rendered cards, supplementing the in-session render — which stays the authority for the delivery gate. Every sync is gated by the human, since a sync publishes outside the machine, and the pack itself never syncs.

**User Story:** As a person reviewing a visual host's components, I want the declared components mirrored to the team design project under a human gate, so that the team reviews rendered cards while the in-session render stays the authority for the gate.

### Acceptance Criteria

**Case: the optional, off-by-default machine**

1. The system *shall* keep design-sync off by default in the base defaults table, and *shall* turn it on only where a host records a profile line. [E-18, INV-14]
2. *when* design-sync runs, the system *shall* sync the components a delivery declared and *shall* gate every sync by the human, since a sync publishes outside the machine. [E-18, ACT-1]

**Case: the work-kind axis stands it down**

3. The system *shall* apply design-sync to product-kind work on a visual host, and *shall* stand every other kind down by name. [T-16, INV-22]

---

## Requirement 249: The skill evals prove each skill at its behaviour

**Context:** The skill evals test the pack's own skills at the level that matters for a skill: behaviour. Each working skill owns at least one recorded eval — a scenario where a bare session errs and the skill's text fixes it, proven red at authoring. Evals re-run at milestones and at any delivery that changes a skill's behaviour.

**User Story:** As a person trusting the pack's skills, I want each working skill to own a behaviour eval proven red without it, so that a skill's own instructions are proven to change what a session does.

### Acceptance Criteria

**Case: one eval per working skill**

1. The system *shall* have each working skill own at least one recorded eval — a scenario proven red without the skill and corrected by it — living in `evals/`, one file per skill. [E-19]
2. *if* a working skill carries no eval, *then* the system *shall* flag it a defect at the milestone audit. [E-19, M-1]

**Case: when the evals re-run**

3. *when* a milestone is reached or a delivery changes a skill's behaviour, the system *shall* re-run that skill's eval, a bump sweeping only a pin or version line owing no re-run. [E-19]

---

## Requirement 250: The surface registry is one self-closing list

**Context:** The surface registry is one host-authored list of every user-facing surface. Its preferred form is executable: the list lives as a declared map inside a completeness-gate test, so a mismatch is a failing test in both directions. A completeness check scans the real rendered artifact against the list, so a surface that renders but is not registered goes red — the registry is self-closing.

**User Story:** As a person guarding surface coverage, I want the registry read as an executable map both ways, so that a rendered-but-unregistered surface and a registered-but-empty one each fail a test.

### Acceptance Criteria

**Case: the executable list, both directions**

1. The system *shall* keep the registry as a declared map inside a completeness-gate test, a mismatch failing in both directions — rendered-but-unregistered and registered-but-empty. [E-10]
2. *when* the completeness check runs, the system *shall* scan the real rendered artifact against the list and red a surface that renders but is not registered. [E-10]

**Case: the honest fallback**

3. The system *shall* keep the list as a document for a host with no test harness, and *when* a host arrives with the executable form already working *shall* recognize it rather than ask it back into a document. [E-10]

---

## Requirement 277: The spec is a glossary and requirements a stranger can read

**Context:** The spec is the document that states what the product does for its user. It opens with a preamble, then a glossary, then a body of requirements, each requirement carrying a Context block, a User Story, and acceptance criteria grouped into named cases. A stranger follows one requirement on first pass without asking what a word means or where a rule lives. Two further laws hold the genre honest: a source hole is recorded and never filled by invention, and every domain noun carries one glossary entry under one name.

**User Story:** As a person reading the spec for the first time, I want it written as a glossary plus named-case requirements in plain words, so that I can follow any one requirement on first pass without project context.

### Acceptance Criteria

**Case: the document shape**

1. The spec *shall* open with a preamble, then a glossary, then a body of requirements, in that order. [INV-250]
2. Each requirement *shall* carry three parts in order: a Context block of two to four sentences, a one-sentence User Story, and acceptance criteria grouped into named cases. [INV-250]
3. *when* a criterion is written, the system *shall* place it in exactly one named case, and *shall* number the criteria continuously through the requirement. [INV-250]

**Case: the criterion form**

4. Each criterion *shall* state one rule, and its code anchor *shall* trail at the line's end. [INV-251]
   - a rule is a single situation with its response, the response's *shall* clauses joined in one sentence where the duty has parts;
   - whether a line packs two rules is the cold reader's judgment, never a keyword count.
5. The keywords *when*, *while*, *if*, *then*, and *shall* *shall* be set in lowercase italics, and no word in the document *shall* be written in all capitals outside a code anchor, a `[GAP: ...]` marker, or a filename. [INV-251]
6. *if* a line breaks the criterion form or the capitals rule, *then* the style lint *shall* red. [INV-251]
7. A criterion *shall* hold the pieces of its rule its own line leaves as an indented bullet sub-list under that line. [INV-251]
   - such a piece is an enumeration of members, a scope note, or a permitted exception.
8. Each bullet *shall* carry one complete clause with its own subject and finite verb, and *shall* carry no code anchor. [INV-251]

**Case: a source hole is recorded, never filled by invention**

9. *when* a criterion names a behaviour whose judge, measure, or scope the source does not state, the system *shall* name the plainest honest actor and *shall* write a `[GAP: ...]` line under the criterion. [INV-252]
10. *if* the source does not answer a behaviour, *then* the system *shall* write the gap line and *shall* invent no answer. [INV-252]

**Case: history lives in the journal**

11. The spec *shall* state today's behaviour only; dates, provenance, and the reasons behind past choices *shall* live in `JOURNAL.md`. [INV-253]
12. *if* a dated note or a provenance sentence appears in the spec body, *then* the system *shall* count it a defect and move it to `JOURNAL.md`. [INV-253]

**Case: closed vocabulary**

13. Every domain noun used anywhere in the document *shall* hold exactly one glossary entry; a word of ordinary English *shall* hold none. [INV-254]
14. *if* a domain noun appears in the body with no glossary entry, *then* the vocabulary check *shall* red. [INV-254]

**Case: one name per thing**

15. One thing *shall* carry one name everywhere in the document. [INV-255]
16. *if* one thing is referenced under two names, *then* the one-name check *shall* red. [INV-255]

**Case: every relational word fills its slots**

17. *when* a criterion uses a weak word — proportional, larger, sufficient, fast, and their kind — the sentence *shall* fill every slot the word opens: the reference point, the measure, or the reason, stated where the word stands. [INV-256]
18. *if* a weak word stands with an unfilled slot and no gap line, *then* the weak-word check *shall* red. [INV-256]

**Case: every judgment names its judge and inputs**

19. *when* a criterion carries an evaluative phrase — broken, larger than, worth — the criterion *shall* name the actor that judges it and the inputs the actor judges by. [INV-257]
20. *if* an evaluative phrase names no judge and no inputs and carries no gap line, *then* the comprehension gate *shall* treat it as a blocking finding. [INV-257]

**Case: when the gates arm**

21. *when* the migration converts the spec to this format, the system *shall* convert the whole document in one delivery. [INV-270]
22. Every gate this section names *shall* arm in that same conversion delivery, and no gate *shall* arm before it. [INV-270]

---

## Requirement 278: The generated index is built from the criteria, never hand-written

**Context:** A maintainer follows a code from a criterion to its home and back, and the map from a code to its location is the generated index — a code-to-location table. A script builds it from the body criteria at freeze, so the generated index is output the build owns and no one edits. A code the body carries and the build misses, or the build carries and the body misses, stops the index gate — the gate that checks the body and the build agree. The criteria and the glossary are the authored home of every code's plain statement, and the generated index carries locations only.

**User Story:** As a maintainer following codes through the spec, I want the code-to-location table built from the criteria at freeze, so that the table never drifts from the body it describes.

### Acceptance Criteria

**Case: the index is generated output**

1. *when* the spec is frozen, the system *shall* build the generated index from the criteria in the body. [INV-258]
2. The generated index *shall* be output only; *if* the generated index is edited by hand, *then* the system *shall* count the edit a defect. [INV-258]

**Case: the body and the build must agree**

3. *if* a code appears on a criterion in the body and not in the generated index, *then* the index gate *shall* red. [INV-259]
4. *if* a code appears in the generated index and not on any criterion in the body, *then* the index gate *shall* red. [INV-259]

**Case: the authored home of a rule's statement**

5. The criteria and the glossary *shall* be the authored home of every code's plain statement: a criterion carries its code's rule, and a code that names an entity — a numbered part of the product — has its definition in the glossary. [INV-271]
6. The generated index *shall* carry locations only. [INV-271]
7. *when* the conversion delivery lands, the description-field gate — `check-description-field.py`, the check behind INV-239 — *shall* retire, with the criteria and the glossary as its stated successor. [INV-271]

---

## Requirement 279: Every spec-touching delivery declares its delta per code

**Context:** A delivery that changes the spec adds, sharpens, or retires rules, and an undeclared change lets a rule vanish or change wording with no notice. So every spec-touching delivery carries a delta record: for each touched code it states one of four kinds — new, sharpen, retire, or scenario-only. Before the push, the delta classifier diffs the old criteria set against the new one and reds where the record and the diff disagree.

**User Story:** As a person reviewing a delivery that changes the spec, I want each touched code declared as new, sharpen, retire, or scenario-only and checked against the diff, so that no rule appears, changes, or disappears unannounced.

### Acceptance Criteria

**Case: the delivery declares a delta record**

1. *when* a delivery changes the spec, the system *shall* carry a delta record that names each touched code with one delta kind: new, sharpen, retire, or scenario-only. [INV-260]

**Case: the diff must match the record**

2. The delta classifier *shall* diff criterion text under normalization: whitespace collapsed, italic markers stripped, and letters case-folded outside code anchors; a difference that survives normalization is a text change, and any other difference is none. [INV-261]
3. *if* a code is present in the old criteria set and absent from the new one with no *retire* declared for it, *then* the delta classifier *shall* red. [INV-261]
4. *if* a code is present in the new criteria set and absent from the old one with no *new* declared for it, *then* the delta classifier *shall* red. [INV-261]
5. *if* a code's criterion text differs under normalization between the old and the new criteria set with no *sharpen* declared for it, *then* the delta classifier *shall* red. [INV-261]

**Case: a sharpen replaces its old sentence**

6. *when* a code is declared *sharpen*, the delta classifier *shall* check survival by a normalized full-sentence match, and *shall* verify that the sharpened code's own criterion line no longer equals its old text. [INV-262]
7. *if* a *sharpen* code's old sentence survives that match anywhere in the document, *then* the delta classifier *shall* red. [INV-262]

**Case: growth stays inside the declared budget**

8. *when* a delivery declares its *new* criteria, the system *shall* sum their bytes into the delivery's new-criteria budget. [INV-263]
9. A declared new criterion *shall* carry no redundancy, and its form *shall* be governed by the readability arms. [INV-263]
10. *when* the delta classifier measures the document's byte growth over the delivery, it *shall* exclude declared sharpen bytes and glossary-addition bytes from the growth. [INV-263]
11. *if* the measured growth exceeds the declared new-criteria budget, *then* the delta classifier *shall* red. [INV-263]

**Case: one pen on the shared document**

12. The delta record *shall* ride the pen — the one-writer-at-a-time serialization the shared spec document already carries. [INV-198]
13. *when* a delivery merges after another delivery has frozen the spec, the delta classifier *shall* re-diff against the criteria set of the freeze taken after that merge. [INV-261]

---

## Requirement 281: A changed section passes the mechanical lints, then the cold readers

**Context:** A section ships once it survives two layers, an author's own read of it settling nothing. First the mechanical lints run — free scripts a machine runs on every push. Then a panel of cold readers, each reading with zero project context, reads the changed section; a blocking finding is fixed as it is found, and the section passes only after two reads in a row return zero blocking findings. A reader finding that names a source hole becomes a queue row, so the hole is tracked and not lost.

**User Story:** As a person shipping a changed section, I want it to clear the mechanical lints and then a cold-reader panel, so that a stranger can read it and every source hole a reader names is tracked.

### Acceptance Criteria

**Case: the mechanical layer runs first and free**

1. *when* a section changes, the system *shall* run the mechanical lints — the vocabulary check, the one-name check, the weak-word check, and the style lint — before any reader, on every push. [INV-266]
2. *if* any mechanical lint reds, *then* the system *shall* stop the section at the mechanical layer and *shall* send no reader. [INV-266]

**Case: the cold-reader panel**

3. *when* the mechanical layer passes, the system *shall* give the changed section to a cold-reader panel, each reader reading with zero project context. [INV-267]
   [GAP: the number of cold readers that form one panel, and the actor that supplies them, are unstated.]
4. *when* a cold reader returns a blocking finding, the system *shall* fix the finding before the next read. [INV-267]
5. The system *shall* pass a changed section only *when* two consecutive reads return zero blocking findings. [INV-267]

**Case: a section that will not converge**

6. *when* four rounds of reads have run on one section and new blocking findings still arrive, the system *shall* escalate to the human as a named question stating which terms keep failing, and *shall* pause the panel until the human answers. [INV-267]

**Case: a source hole a reader names becomes a queue row**

7. *when* a cold reader's finding names a source hole, the system *shall* open a queue row for the hole and *shall* record the criterion it sits under. [INV-268]

---

## Requirement 282: Every gate in this family states its reach on the green line

**Context:** A gate that prints green proves nothing until a reader knows how much it read. The gates in this family — the index gate, the delta classifier, the ratchet gate, the mechanical lints, the matrix-reference gate, and the matrix row lint — each read files and match rows. So each states its reach on the line it prints when it passes: the files it opened, and the rows it matched of the rows it scanned. A reader of the green line then knows the verdict and its reach together.

**User Story:** As a person reading a gate's green line, I want it to state what the gate read, so that I can tell a real pass from a pass that read nothing.

### Acceptance Criteria

**Case: the green line carries the reach**

1. *when* a gate in this family passes, the system *shall* print a green line that names the files it opened and the count of rows it matched of the rows it scanned. [INV-269]
2. *if* a gate passes while its scanned-row count is zero, *then* the gate *shall* print a line naming that it scanned nothing, and *shall* not print a bare green line. [INV-269]

---

## Requirement 283: The test matrix is a family member written as node-grouped criteria

**Context:** The spec format proved the requirements genre on the spec document itself, and the test matrix is the format family's second member, written in that same genre. The matrix's own definition — what it inherits from the family and what it adds — lives in `docs/test-matrix-format.md`. This requirement carries that definition into the spec, so the matrix's shape stands as a proven fact the spec's own gates hold.

**User Story:** As a maintainer reading the matrix, I want one format family across the spec and the matrix, so that one set of laws and one set of gates covers every family document.

### Acceptance Criteria

**Case: inherits the family, adds its own structure**

1. The test matrix *shall* be written in the requirements format the spec format defines, inheriting the closed vocabulary, the criterion form, the trailing anchor, the no-history law, the generated-section gating, and the comprehension gate from `docs/spec-format.md`, and *shall* restate none of them. [INV-272]
2. The matrix *shall* open with an artifact inventory naming every file the reader receives with at least one row asserting it at the rendered level, then the matrix rows grouped into node blocks, then the generated Reference. [INV-272]

**Case: a row is one criterion with the matrix's own fields**

3. Each matrix row *shall* state one trigger and one response in a single sentence carrying both what the fact does and what it must never do, its spec anchor trailing at the line's end. [INV-272]
4. Each row *shall* carry a pinned test level drawn from the project's declared level ladder, an owning test, and a status of *built*, *todo*, or *retired*. [INV-272]

**Case: node blocks are the case grouping, and Context and the User Story stand down**

5. Matrix rows *shall* group into node blocks, one per architecture node headed "### [node: <name>]", the heading standing as the matrix's case grouping. [INV-272]
6. A matrix row *shall* carry no Context block and no User Story; the fact's Context and User Story live once at the spec, and the row inherits them through its trailing anchor. [INV-272]

**Case: when the gates arm**

7. The matrix's conversion *shall* follow the family's one-delivery arming rule: the entire document moves at once, and this member's gates arm inside that same delivery. [INV-272] [INV-270]

---

## Requirement 284: The matrix Reference is generated from the rows, never hand-written

**Context:** A hand-kept coverage view drifts from the rows it claims to summarize. The matrix Reference is instead built from the body the way the spec's own code-to-location table is: a script reads the committed rows and produces the map, and no one edits the map by hand.

**User Story:** As a maintainer following a spec anchor into its coverage, I want the Reference built from the rows at freeze, so that it never drifts from the body it maps.

### Acceptance Criteria

**Case: generated output**

1. *when* the matrix is frozen, the system *shall* build the Reference from the body rows, mapping each row's trailing spec anchors to the row ids that cover them. [INV-273]
2. The Reference *shall* be output only; *if* it is edited by hand, *then* the matrix-reference gate *shall* red. [INV-273]

**Case: body and Reference must agree**

3. *if* the body and the committed Reference disagree in either direction — a body anchor absent from the table, or a table anchor carried by no body row — *then* the matrix-reference gate *shall* red. [INV-273]

**Case: reach and arming**

4. The matrix-reference gate *shall* stay unarmed until the conversion delivery, *shall* arm in it, and *shall* state its reach on the green line. [INV-273] [INV-269]

---

## Requirement 285: A matrix row pins a level and states its never side, or the row lint reds

**Context:** The matrix once closed its derivation with a coverage checklist walked by hand. The two facts a machine can read off each row — a pinned test level, a stated never side — become a mechanical lint instead, run at every push rather than walked once.

**User Story:** As a maintainer trusting the matrix, I want a row lint to catch a missing level or a bare happy-path row, so that the coverage a hand-walked checklist once caught is never lost to drift.

### Acceptance Criteria

**Case: the row lint holds the two per-row facts**

1. *if* a body row pins no test level from the declared ladder, *then* the row lint *shall* red, naming the row. [INV-274]
2. *if* a body row states no never side, *then* the row lint *shall* red, naming the row. [INV-274]
3. *when* every body row pins its level and states its never side, the row lint *shall* pass green and state its reach on the green line. [INV-274] [INV-269]

**Case: the hand-walked checklist retires**

4. *when* the conversion delivery lands, the checkbox gate that read the coverage-validation checklist *shall* retire, the row lint and the matrix-reference gate standing as its successors. [INV-274]

---

## Requirement 286: The queue is a family member written as live wish rows

**Context:** The queue — the plan/wish-list `templates/PLAN.template.md` hands a project at founding — is the format family's third member, joining after the spec and the matrix. The page `docs/roadmap-format.md` defines the member — the inherited laws and the queue-particular additions — and this requirement binds that definition, putting the queue's shape under the gates that hold the family.

**User Story:** As a maintainer working the queue, I want its format governed by the family's laws and gates, so that reading and holding it costs what the other family documents cost.

### Acceptance Criteria

**Case: the member definition and its inheritance**

1. The queue *shall* follow the family genre by reference to `docs/spec-format.md` — closed vocabulary, keyword form, trailing anchors, no-history, generated-section gating, the comprehension gate — restating none of them. [INV-275]
2. The queue *shall* open with a preamble and a glossary, then one table of live wish rows in ascending id order, a manifest line per archive file above the body. [INV-275]

**Case: when the gates arm**

3. The queue's conversion *shall* follow the family's one-delivery arming rule: the whole document moves at once, every consumer of the old shape is repointed in that delivery, and the row lint arms inside it. [INV-275] [INV-270]

**Case: how the no-history law is enforced here**

4. The queue's no-history net *shall* be the live-body law and the doc-rotation gate; the family's no-history gate *shall* not scan the queue, a live row carrying its status and provenance dates by design, the status cell standing as the sole authority on a row's state. [INV-275, INV-276]

---

## Requirement 287: The queue's body holds live rows, and a closed row moves to the archive at its closing commit

**Context:** The queue's body is its live table, and the record of finished work lives in the archive. When a wish reaches a terminal exit, its row leaves the body for the archive in the same commit that closes it, so the body a reader scans is always the live queue. A parked wish still awaits its turn, so a *deferred* or a *far* row stays live in the body.

**User Story:** As a person reading the queue for the live work state, I want a closed row to leave the body for the archive the moment its commit closes it, so that the body I scan holds only live wishes and nothing closed is lost.

### Acceptance Criteria

**Case: a terminal exit moves to the archive at its closing commit**

1. *when* a row reaches a terminal exit — *landed*, *declined*, or *superseded* — the system *shall* move it verbatim, its delivery report riding with it, from the body to the queue archive in the same commit that closes it. [INV-276]
2. The system *shall* gather a calendar month's moved rows in one archive file and *shall* record one manifest line per file above the body. [INV-276]
3. The system *shall* cross-check the manifest against the archive under the nothing-lost gate, a moved row found in neither the body nor its archive reading as a violation. [INV-276, INV-209]

**Case: a parked row stays live in the body**

4. The system *shall* keep a *deferred* or a *far* row in the body, its revisit trigger re-read at queue-take and at the milestone review by the existing re-scan law. [INV-276, INV-129]

**Case: a row with several legs closes only whole**

5. A row with more than one leg *shall* reach a terminal exit only *when* every leg is closed; an open leg *shall* keep the row live and named — *in-work* under a driving session, *deferred* on a named trigger *when* it waits on an outside event. [INV-276, INV-26]

---

## Requirement 288: A queue row carries five cells in the closed vocabularies, or the row lint reds

**Context:** One queue row is one live wish. The header fixes its shape at five cells, and two closed vocabularies fix what its status and class cells may say. A row lint reads every body row at every suite run and reds a row that breaks the shape or the vocabulary, so a malformed row is caught the moment it lands, before any reader meets it.

**User Story:** As a maintainer trusting the queue, I want a row lint to hold every body row to five cells and the closed vocabularies, so that a drifted or mislabelled row is caught at every suite run, before it can mislead a reader.

### Acceptance Criteria

**Case: the row form**

1. Each body row *shall* carry exactly five cells matching the header — the id, the wish, the class, the status, and the acceptance — and the body rows *shall* stand in ascending id order. [INV-277]
2. A row's status cell *shall* carry one word of the closed status vocabulary — *queued*, *ready*, *in-work*, *deferred*, or *far* — each set in lowercase italics and carrying its date, a *deferred* row naming its trigger. [INV-277]
3. A row's class cell *shall* carry one word of the closed size vocabulary — *bug*, *small*, *surface*, or *large* — the size measure the glossary's size entry defines. [INV-277]

**Case: the row lint holds the shape and the vocabularies**

4. *if* a body row carries other than five cells, breaks ascending id order, carries a status or class outside its vocabulary, or reads *deferred* with no trigger, *then* the row lint *shall* red, naming the row. [INV-277]
5. *when* every body row holds its shape and its vocabularies, the row lint *shall* pass green and state its reach on the green line, its home the suite's traceability tests, extended, with no new standalone script. [INV-277, INV-269]

## Requirement 289: The architecture is a family member written as node sections

**Context:** ARCHITECTURE.md is the format family's fourth member, joining the spec, the matrix, and the queue. The page `docs/architecture-format.md` defines the member — the laws it inherits from the family and the parts particular to the architecture — and this requirement binds that definition, putting the architecture's shape under the gates that hold the family. The architecture's reading job is a component inventory: a reader opens it to learn what parts exist, what each is for, which spec facts each owns, and where the part sits on disk. Each part is one node, and each node is one section headed `### [node: <name>]`, carrying its responsibility, the spec anchors it owns, the file-and-line pins where it lives, and a short notes line for what the other fields cannot hold.

**User Story:** As a maintainer reading the architecture, I want its format governed by the family's laws and gates, so that reading and holding it costs what the other family documents cost.

### Acceptance Criteria

**Case: the member definition and its inheritance**

1. The architecture *shall* follow the family genre by reference to `docs/spec-format.md` — closed vocabulary, keyword form, trailing anchors, no-history, generated-section gating, the comprehension gate — and *shall* restate none of them, its own definition living at `docs/architecture-format.md`. [INV-278]
2. The architecture *shall* open with a preamble, then its body of node sections, then the generated tables the member-definition page fixes in order. [INV-278]

**Case: a node is a section with four fields**

3. Each node *shall* stand as one section headed `### [node: <name>]`, and a node promised under an open queue row with its machinery still ahead *shall* carry the target tag in that heading, the matrix's block heading for the node reading the same. [INV-278]
4. A node section *shall* carry four fields. [INV-278]
   - the responsibility is one sentence naming what the node is for;
   - the owns list names the spec anchors the node owns;
   - the pins list names the file-and-line places where its responsibility is carried on disk;
   - the notes line appears only *when* the other three fields cannot hold something.

**Case: every anchor lives under exactly one node**

5. Every spec anchor *shall* be owned by exactly one node, and the suite *shall* hold that bond both ways — each anchor to its node and each node to its anchors. [INV-278]

**Case: when the gates arm**

6. The architecture's conversion *shall* follow the family's one-delivery arming rule: the whole document moves at once, every consumer of the old shape is repointed in that delivery, and this member's gates arm inside it. [INV-278] [INV-270]

## Requirement 290: An owns anchor cites its rule and carries no history

**Context:** The rule an owns anchor names lives once at the spec. So an owns entry cites that home and adds at most one parenthetical sentence saying where the anchor sits or why the node keeps it; a law copied back into the owns cell is a second home and a defect. *when* the spec turns out to lack a sentence the owns cell was carrying, that sentence moves into the spec clause in the same delivery, so the words survive at their one home. The architecture states today's structure alone: the dated prover-record table leaves for its own dated home under the prover records, and a pin carries no date and no provenance, the journal already telling when and why the node landed.

**User Story:** As a maintainer following an owns anchor, I want it to cite one home and carry no history, so that the rule lives once and the architecture reads as today's map.

### Acceptance Criteria

**Case: the owns anchor cites, and a restated law is a defect**

1. An owns entry *shall* cite the rule's home at the spec by its anchor and *shall* trail at most one parenthetical sentence saying where the anchor sits or why the node keeps it. [INV-279]
2. *if* an owns cell restates the rule its anchor names, *then* the suite *shall* red, the restated law standing as a second home. [INV-279]

**Case: content the spec lacks moves to the spec**

3. *when* an owns cell carries a sentence the cited spec clause lacks, the system *shall* move that sentence into the spec clause in the same delivery, so the content lives once at the spec. [INV-279]

**Case: the architecture carries no history**

4. The dated prover-record table *shall* relocate verbatim to its own dated home under the prover records, and the family's no-history law *shall* thereafter reach this document. [INV-279]
5. A pin *shall* carry no date and no provenance, the journal holding when and why the node landed. [INV-279]

## Requirement 291: One node reader serves every consumer of the node shape

**Context:** The node sections are read by many checks — the traceability suite's tests, the node-growth counter, the pin-drift check, and every test asking which node owns an anchor. One reader reads the node shape for all of them: the node names, each node's owned-anchor set, and each node's pins. It is the sibling of `guardrails/specformat.py`, the spec format's one reader. A consumer that reads the raw node shape on its own reads a shape that can drift under it, so such a consumer is a defect the conversion retires. The node-growth counter's hardcoded node-name list retires the same way — it re-derives the list from the reader, so a renamed node stays in step across every consumer.

**User Story:** As a maintainer changing a node, I want every check to read the node shape through one reader, so that a rename or a moved anchor reaches every consumer at once and none reads a stale shape.

### Acceptance Criteria

**Case: one reader, every consumer through it**

1. One reader — the node reader — *shall* read the node shape, the node names, each node's owned-anchor set, and each node's pins, and every consumer *shall* read through it: the traceability tests, the node-growth counter, the pin-drift check, and every test asking which node owns an anchor. [INV-280]
2. *if* a consumer reads the raw node shape on its own, *then* the suite *shall* red, that consumer standing as a defect the conversion retires. [INV-280]

**Case: the hardcoded node list re-derives**

3. The node-growth counter's node-name list *shall* re-derive from the node reader, so a renamed node *shall* stay in step across every consumer. [INV-280]

---

## Requirement 312: The architecture Reference is generated from the nodes, never hand-written

**Context:** A hand-kept ownership view drifts from the nodes it claims to summarize. The architecture Reference is instead built from the nodes the way the matrix's own Reference is: a script reads the committed node sections and produces the map, and no one edits the map by hand.

**User Story:** As a maintainer following a spec anchor into the node that owns it, I want the Reference built from the nodes at freeze, so that it never drifts from the owns fields it maps.

### Acceptance Criteria

**Case: generated output**

1. *when* the architecture is frozen, the system *shall* build the Reference from the node sections, mapping each node's owns field's anchors to the node names that own them. [INV-315]
2. The Reference *shall* be output only; *if* it is edited by hand, *then* the architecture-reference gate *shall* red. [INV-315]

**Case: body and Reference must agree**

3. *if* the nodes and the committed Reference disagree in either direction — an owns anchor absent from the table, or a table anchor owned by no node — *then* the architecture-reference gate *shall* red. [INV-315]

**Case: reach and arming**

4. The architecture-reference gate *shall* stay unarmed until this delivery, *shall* arm in it, and *shall* state its reach on the green line. [INV-315] [INV-269]

---
