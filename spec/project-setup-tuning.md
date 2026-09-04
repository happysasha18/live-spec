## Requirement 3: A project adopts live-spec and the host owns its own state

**Context:** A project can adopt live-spec at the start or partway through work already under way. Adoption brings the document templates, a procedure for joining midstream, and the guardrails the project installs, and the project that adopts it is the host. The host owns everything about its own work rather than sharing one set across several projects.

**User Story:** As a project taking on live-spec, I want to adopt it at any point and own all my own state, so that my spec, queue, journal, and settings live with me rather than in a shared pool.

### Acceptance Criteria

**Case: a project adopts and becomes the host**

1. The system *shall* let a project adopt live-spec at the start or partway through work already under way, bringing the document templates, a procedure for joining midstream, and the guardrails already built for it. [E-1]
   - the guardrails are the repo's own pre-push checks and the opt-in commit fence;
   - the opt-in commit fence blocks a commit when the repository moved under the session since its last read;
   - the host-facing guardrail checks stay a separate, planned family.
2. The system *shall* name the project that adopts live-spec the host. [E-1]

**Case: the host owns its own state**

3. The host *shall* own its own spec, test matrix, queue, journal, surface registry, inbox, and feedback ledger. [E-1]
4. The host *shall* keep a `.live-spec/` folder holding its profile, its checkpoints, and the versions of the skills it runs. [E-1]

## Requirement 170: Founding asks its shaping questions and never infers them

**Context:** Before the first request is worked, founding answers the questions that shape everything downstream, in the new spec's opening. The first of them is whether the product is a personal tool or a reusable product. Every later sentence leans on this answer, so an inferred answer is the most expensive silent choice.

**User Story:** As a person founding a host, I want the founding questions asked outright at setup, so that the answers every later decision leans on come from my own stated word. [B-2]

### Acceptance Criteria

**Case: the founding questions block the first request**

1. *when* founding begins, the system *shall* answer the founding questions in the new spec's opening before it works the first request. [B-2]
2. The system *shall* ask the personal-tool-or-reusable-product question first among them. [B-2]
3. This question *shall* block the first request until the system asks it or reads its answer from the profile; an ordinary open question rides along without stopping work, and this one *shall* not. [INV-4, INV-12, B-2]

**Case: the answer comes from the human or the profile**

4. *when* the personal-scope standing preference in the personal profile covers the answer, the system *shall* seed this host's default from it and *shall* say so aloud. [E-13, B-2]
5. *if* no standing preference covers the answer, *then* the system *shall* ask the human. [B-2]
6. The system *shall* derive no founding answer from example artifacts; naming three of the human's own artifacts *shall* not decide the product is those artifacts, since an inferred founding answer is a silent micro-decision at its most expensive. [B-2, INV-5]

**Case: adoption owes the same questions**

7. *when* adoption reaches its orient phase, the system *shall* put the founding questions again, personal-versus-reusable first. [A-1, B-2]

---

## Requirement 171: Founding learns who the human is

**Context:** Before any founding question resolves, the system learns who it is working with. It looks for the personal profile at its one home, at founding, at adoption's orient, and at the first session on a new machine or with a new human. The human tells the system about themselves, or names sources for it to read, and every line lands on the human's word.

**User Story:** As a person the system is about to work for, I want it to load or found my personal profile at setup, so that it works from what I told it and never from a silent assumption about me. [B-3]

### Acceptance Criteria

**Case: find the profile first**

1. *when* founding starts, adoption reaches orient, or a session opens on a new machine or with a new human, the system *shall* look for the personal profile at its one home first. [E-13, B-3]
2. *if* the personal profile exists, *then* the system *shall* load it, name the file, and read any unrecognized line aloud instead of skipping it silently. [E-13]
3. *if* the personal profile is absent, *then* the system *shall* offer to create it from `templates/profile.template.md`. [B-3]

**Case: every line lands on the human's word**

4. *when* the human tells the system a line about themselves, the system *shall* write that line faithfully. [INV-9, B-3]
5. *when* the human names a source — their repos, their docs, a public page — the system *shall* read it and propose lines, and *shall* accept or drop each proposed line one at a time on the human's word. A dropped proposal *shall* stay dropped. [INV-9, B-3]
6. The template *shall* mark every placeholder as a placeholder, so nothing in it can pass for the human's word. [B-3]

**Case: the human can decline, and a worker never onboards**

7. *if* the human declines the whole step, *then* the system *shall* run the session on pack defaults, say so, and raise the offer again at the next project setup rather than mid-work. [B-3]
8. *when* the personal profile already exists, the system *shall* skip the founding step and load the profile. [B-3]
9. A worker session *shall* onboard no one; its brief already carries the setting lines it needs. [ACT-3]

---

## Requirement 172: Founding proposes the engine-and-instance split

**Context:** A reusable product can still ship as one concrete thing a real person uses today — a gallery that hangs these photos, a coach that reads these tracks. The moment the reusable answer lands on a product that carries content of its own, founding asks one more shaping question: is the generic mechanism worth its own home, apart from the content it serves now. The system proposes; the human's word decides; both outcomes are recorded.

**User Story:** As a person founding a reusable, content-carrying product, I want the engine-and-instance split proposed rather than imposed, so that I decide whether the generic mechanism gets its own home. [INV-85]

### Acceptance Criteria

**Case: the split is proposed, and the human decides**

1. *when* the reusable answer lands on a product that carries content of its own, the system *shall* ask whether the generic mechanism is worth its own home. The human's word *shall* decide, and the system *shall* record both outcomes. [INV-85, B-2]
2. *when* the system proposes the split, the system *shall* name two homes and what each owns: an engine repo, public by default and tested on its own generic fixtures, carrying a content contract; and an instance home, holding the content, its corrections, and the private fragments. [INV-85, INV-79]
3. *when* the split proposal places binary content such as images or audio, the system *shall* place it by the architecture's placement prompt. [INV-75]

**Case: a declined split, and a taken split**

4. *if* the human declines the split, *then* the system *shall* record a one-line reuse note in the host profile under the key `reuse.split-declined: <date>`, and *shall* treat a single-repo host as a complete outcome. [INV-85]
5. *when* the human takes the split, the system *shall* bind the pair-leadership rules from that moment. [INV-85]
6. *when* a donor-specific constant is found while carving the engine, the system *shall* record it as a named content-contract entry with a test that proves the engine works without it. [INV-79]

**Case: the offer returns only when one home no longer holds**

7. *if* a declined product later outgrows one home — a second instance appears, or the content and the mechanism can no longer share one file — *then* the system *shall* raise the split offer again. [INV-85]
   [GAP: the spec does not name who judges that the content and the mechanism can no longer share one file, or by what measure.]
8. *when* adoption reaches orient, the system *shall* put the same split proposal alongside the other founding questions. [A-1, B-2]

---

## Requirement 173: Founding names the project kind, and the kind can change

**Context:** Beside personal-versus-reusable, founding asks what the project is — a book, a backend service, a static site, a fullstack app, a CLI, or a skill pack. The answer is recorded in one line in the host profile and seeds the host's defaults. The line stays alive: when work notices the project has outgrown its kind, the line updates on the human's word.

**User Story:** As a person founding or adopting a host, I want its project kind asked outright and recorded in one home, so that the host's defaults are seeded from a kind stated at founding. [INV-36]

### Acceptance Criteria

**Case: the kind is asked and recorded**

1. *when* founding runs, the system *shall* ask the project kind and record it in the host profile on a `project.kind` line. [INV-36, E-13]
2. *when* adoption reaches orient, the system *shall* ask the project kind again with the rest of the founding set. [A-1, INV-36]
3. The system *shall* ask the project kind of the human every time; no personal-profile line can state what a host is. [B-2, INV-36]

**Case: three intake verdicts stay separate**

4. The system *shall* keep three verdicts separate and *shall* let none collapse into another. [T-16, T-13, INV-30, INV-37]
   - the project kind says what the product is and seeds project-wide defaults;
   - the request's work type says what this request builds;
   - the placement says where the request lands on the feature map.
5. *if* the host profile already records a `work-kind.host-default` line, *then* the system *shall* keep it, and the project kind *shall* not silently override that explicit line. [T-16, E-13]

**Case: the kind vocabulary and its growth**

6. The system *shall* name the project kind from the curated vocabulary, and *shall* add a custom kind through the queue when a named project the list did not serve well appears. [T-16]

**Case: the line stays alive**

7. *when* work notices the project has outgrown its kind, the system *shall* update the `project.kind` line on the human's word and journal it at that moment rather than parking it for an audit. [INV-36]

---

## Requirement 174: Founding declares the project's concrete layers and proof kinds

**Context:** The impact read, the footprint categories, and the test ladder are stated once by the pack in kind-abstract terms, and each project kind fills them with its own concrete parts. So the founding line that records the kind carries two more: the concrete layers this project splits into, and the concrete checks it proves with. The per-kind fill is the project's own ratchet from there.

**User Story:** As a person founding a host of a given kind, I want its concrete layers and proof kinds declared beside its kind, so that the footprint read and the test levels run against this project's own declared parts. [INV-135]

### Acceptance Criteria

**Case: two more lines beside the kind**

1. *when* the system records `project.kind`, the system *shall* also record a `project.layers` line naming the project's concrete footprint categories and a `project.proofs` line naming its concrete proof kinds. [INV-135, INV-36]
2. The three footprint categories *shall* hold across every kind — a presentation-only change touches what the audience meets and nothing behind it, a single-module change stays inside one owned layer, and a cross-cutting change moves a shared law or crosses more than one layer — while the layers themselves are the project's own. [INV-128, INV-135]

**Case: an incomplete founding line is flagged**

3. *when* adoption reads a host profile that records `project.kind` with no declared layers and no declared proofs, a founding check *shall* flag the line as incomplete, the way an unbacked surface is flagged. [INV-135, A-10]
   [GAP: the spec flags the missing layers and proofs at adoption; it does not state whether a bootstrap founding that omits them is flagged.]

**Case: the checks read the declared categories**

4. The footprint check and the test-level rule *shall* read the project's own declared categories. [INV-134, INV-135]
5. The architecture document *shall* carry the per-kind footprint-and-proof table beside the node-structure-by-kind scaffold, and the spec and test roles *shall* read the declared layers and proofs rather than assuming code. [INV-135]
6. *when* live-spec itself carries no product surface, the system *shall* ship the abstract law and leave the concrete assertion to the products it serves. [INV-163]

---

## Requirement 175: A project kind's design principles and the interactive-overlap rule

**Context:** Beside its layers and proof kinds, a project kind names a set of design principles: checkable design rules its products must hold. The pack ships a starter set per kind, and a founding that records a visual kind declares them in the host profile. The verify pass runs each principle in the medium's own form.

**User Story:** As a person founding a visual host, I want its design principles declared and run at verify, so that a design rule its products must hold is checked in the medium's own form. [INV-136]

### Acceptance Criteria

**Case: the principles are declared and run**

1. *when* founding records a visual kind, the system *shall* declare its design principles in the host profile on a `project.design-principles` line — the pack's starter set plus any the project adds. [INV-136]
2. *when* a visual kind is recorded with no design principles, a founding check *shall* flag it, the way a kind recorded with no layers or proofs is flagged. [INV-136, INV-135]
3. *when* the verify pass runs, the system *shall* read the declared design principles and run each in the medium's own form, beside walking each surface as a visitor and the feel pass. [INV-136, INV-30]
4. *if* a design principle is one the suite cannot make green — motion feel, a real-device gesture — *then* the system *shall* have the human check it by eye; *if* the suite can hold it, *then* the system *shall* make it a matrix row in the adopting project's suite. [INV-30, INV-77, INV-136]

**Case: the frontend starter set and the interactive-overlap rule**

5. The frontend kind's starter set *shall* gather the pack's frontend guidance — walking each surface as a visitor, the feel pass scaled to a whole site, and motion and scroll feel as the human's own check — and *shall* add the interactive-overlap rule. [INV-30, INV-136]
6. Two interactive controls from different visual layers — a player, a close button, a zoom handle — *shall* hold separate clickable regions, so every press lands on one control alone. A non-interactive element — a plaque, a picture, a caption — may overlap anything. [INV-136]

**Case: the prover catches the blind spot on the spec**

7. *when* two interactive controls from different layers are reachable on one screen while the covering surface leaves the lower control pressable, the prover *shall* report it as a finding, the same blank-answer class as an unwritten seam. [INV-136, INV-125, INV-126, INV-72]
8. For each covering overlay a project defines, the adopting project's suite *shall* open the overlay and assert every other interactive control is either not rendered or not pressable — computed `pointer-events:none`, `opacity:0`, or off-screen — while the overlay stands. [INV-136, INV-163]

---

## Requirement 176: The frontend kind's legibility floor

**Context:** Beside the interactive-overlap rule, the frontend kind carries a legibility floor: text meets a minimum contrast ratio against its background and a minimum size, so a human can read what a surface shows. The floor is read at two moments — the verify feel pass and the pre-show gate — the same two the register lint guards.

**User Story:** As a person shown a surface's text, I want it to meet a stated contrast and size floor, so that what a surface shows can be read. [INV-139]

### Acceptance Criteria

**Case: the floor's numbers**

1. The legibility floor *shall* require normal text at a contrast ratio of at least 4.5 to 1; large text — font size at least 24 pixels, or 18.66 pixels when bold — at a contrast ratio of at least 3 to 1; and body and caption text at a font size of at least 12 pixels. A host may set its own numbers on its word. [INV-139]

**Case: the two reading moments**

2. *when* the verify feel pass runs, the system *shall* read a product surface's computed colours and sizes against the floor. [INV-139, INV-30]
3. *when* a styled file is about to be shown to a human, the pre-show legibility lint (`scripts/preshow-legibility-lint.py`) *shall* read the declared colours and sizes against the floor, beside the register lint. [INV-139, INV-83]
4. *if* the pre-show legibility lint reads a result below the floor, *then* the system *shall* block the showing until the text is lifted to the floor. [INV-139, INV-83]

**Case: the pack ships the law, the product ships the assertion**

5. The pack *shall* ship the law, the floor's default numbers, and the script; the browser-computed assertion for a product surface *shall* live in the adopting product's suite. [INV-139, INV-163]

---

## Requirement 178: Every unbacked live surface gets one verdict

**Context:** An adopted product often carries a surface that reaches the user but has no spec backing — a de-facto prototype, the most common residue in an adopted host. Adoption flags each one at orient. The human then decides, per surface, what becomes of it.

**User Story:** As a person adopting a running product, I want every unbacked live surface flagged and settled per surface, so that nothing keeps running unexplained. [A-10]

### Acceptance Criteria

**Case: flag every unbacked surface**

1. *when* an inventoried surface reaches the user but carries no spec backing, the system *shall* flag it at orient for the human's verdict. [A-10]

**Case: the three verdicts**

2. *if* the human chooses promote, *then* the system *shall* enter the surface at the spec step as a feature. [INV-16]
3. *if* the human chooses quarantine, *then* the system *shall* move the surface into a prototype home, label it, and leave a dated one-line record at the prototype home stating what, why, and the date. This *shall* be treated as a production change, since the user loses the surface or sees it relabelled. [E-17]
4. *if* the human chooses attic, *then* the system *shall* archive the surface. [A-4]

---

## Requirement 179: Attic over deletion

**Context:** No adopt or rework run deletes a host file. A superseded file moves to the attic with a manifest line, so nothing removed from active use is lost. One exception passes only through the human's explicit gate.

**User Story:** As a person whose project is being adopted or reworked, I want every superseded file kept in the attic rather than deleted, so that nothing I authored is ever lost. [INV-7]

### Acceptance Criteria

**Case: the attic keeps what is superseded**

1. *when* an adopt or rework run supersedes a host file, the system *shall* move it to `attic/` with one manifest line stating what it was, why it moved, and the date, and *shall* delete nothing. [INV-7, A-4]
2. The attic *shall* be append-only, one manifest line per file. [A-4]
3. *when* two files collide on a basename in the attic, the system *shall* prefix the name with its source directory, and *if* the name is still taken, *then* append a numeric ordinal. [E-9]

**Case: the cruft-sweep gate**

4. *when* adoption offers a cruft sweep, the system *shall* list the file counts and sizes of regenerable junk — caches, build leftovers, already-gitignored files — and *shall* delete only on the human's explicit approval. [A-9]
5. The system *shall* route authored content through the attic and *shall* never let it qualify for the cruft sweep. [A-9]
   [GAP: the layout of the adoption attic — a flat folder with a manifest against dated subfolders — is an open decision, recorded open in DECISIONS.md with its recommendation and reason. D-1]

---

## Requirement 181: Every catch-up step is safe on a half-done state

**Context:** A catch-up sequence can stop partway and be resumed or re-run. Every step reads its precondition from the tree so that a step already done is skipped and a step that finds both the old and new form present merges them. The sequence preserves the host's recorded facts, and a fact leaves its home only to move to one that holds it without loss.

**User Story:** As the owner of a host mid-catch-up, I want every step safe to resume or re-run and every recorded fact preserved, so that an interrupted sequence applies nothing twice and loses nothing. [INV-89, INV-90]

### Acceptance Criteria

**Case: read the precondition, then act**

1. *when* a catch-up step opens, the system *shall* read its precondition from the tree. [INV-89]
2. *if* a step's end state already holds, *then* the system *shall* report it done and skip it. [INV-89]
3. *if* a step finds both the old and the new form present, *then* the system *shall* merge them file by file. [INV-89]
4. *if* two files hold identical content, *then* the system *shall* drop the old copy to the attic. [INV-89]

**Case: reconcile a differing profile by the ladder**

5. *if* a profile file differs between old and new, *then* the system *shall* reconcile it by where each line's home sits under the settings ladder: a host-profile line whose home is the personal profile moves up, and a host-scoped line stays. [INV-89, E-16]
6. *when* a line moves up into a machine-shared file, the system *shall* follow the promotion law and re-read that file immediately before appending. [E-16]
7. *if* any other differing file or remaining conflict is found, *then* the system *shall* ride it on the plan to the owner's gate; the system *shall* never nest a directory inside its replacement and *shall* never overwrite the new form with the old. [INV-89]

**Case: preserve facts and re-home them**

8. The system *shall* rewrite settled prose only where the owner rejected it or the new shape cannot hold it as written, and *shall* carry each proposed rewrite on the plan for the owner's decision. [INV-90]
9. *when* a host adopted under its own document names, the system *shall* keep those names, record each as a host-profile line (`spec.file: SPEC.md`), and *shall* read the pack's canonical name as the host's file under its recorded name. [INV-90]
10. *when* an installed-set record is kept in an outdated format such as commit pins, the system *shall* retire it to the attic and read the new record from the version lines of the skills installed on disk and the pack version. The skills on disk *shall* be the authoritative set. [INV-90, M-7]
11. *when* a stray state file is found — a checkpoint at the repo root, a closed checkpoint, a look-alike state directory — the system *shall* re-home it: a root checkpoint to `.live-spec/checkpoints/`, a closed one to the attic, and a look-alike directory merged under the half-done-state rule. [INV-90, INV-89]

---

## Requirement 182: Catch-up proves itself and stays restorable

**Context:** The catch-up sequence proves that content survived by comparing the host before and after. It records a pre-sequence inventory beside the plan, records the same inventory after execute, and accounts for every difference by a plan item. The pre-sequence state stays restorable from the baseline commit.

**User Story:** As the owner of a caught-up host, I want the sequence to account for every difference against the plan and keep a one-command restore point, so that no file changes outside the plan and the pre-sequence state can be recovered. [INV-92]

### Acceptance Criteria

**Case: the before-and-after comparison**

1. *when* the sequence starts, the system *shall* record a pre-sequence inventory beside the plan: every document with a content fingerprint, the host spec's anchor multiset, and the suite's verdict and count as found. [INV-92]
2. *when* execute completes, the system *shall* record the same inventory again and compare the two. [INV-92]
3. Every difference *shall* be accounted for by a plan item — a file unchanged, re-homed to a named path, merged from named sources, or resting in the attic under its manifest line; an anchor delta *shall* match a change the plan names; and the suite *shall* read at least as green as before. [INV-92]
4. *if* a difference falls outside the plan, *then* the system *shall* block the verify phase until the owner accepts it as a plan amendment or the step is reverted. [INV-92]

**Case: the restore point**

5. The plan document *shall* name the baseline commit and state the one command that returns the host to the pre-sequence state. [INV-92, A-5]
6. The attic *shall* keep every superseded file readable without any restore. [INV-92]

**Case: the sequence's own show**

7. *when* the sequence changes only documents and records and creates no product surface, the system *shall* skip the facet sweep and open the plan document by the ordinary show rule. [INV-92]

---

## Requirement 183: A same-version docs-layout pass rides one named vehicle

**Context:** An adopted host may want its own documents restructured with no pack-version delta. That ask routes to the host's own queue, and the pass runs one named vehicle rather than ad-hoc edits. The vehicle proves content survived and reads the suite green before it lands.

**User Story:** As the owner of a host restructuring its own documents with no version delta, I want the pass to ride one named vehicle with a proven restore path, so that the layout changes safely and content survives. [INV-111]

### Acceptance Criteria

**Case: the vehicle's steps**

1. *when* an ask restructures a host's own documents with no pack-version delta, the system *shall* route it to the host's queue and run one named vehicle. [INV-111, INV-110]
2. The system *shall* lock the owner's decisions in a checkpoint before any file moves, and *shall* build on a clean pushed base so one command restores the pre-pass tree. [INV-111, INV-107]
3. The system *shall* prove content survived by a word-token multiset check and a punctuation multiset check, since word-token identity alone passes a reflow that dropped or moved punctuation. [INV-111]
4. The system *shall* read the full suite green on the restructured tree from the suite log's own line, since a reflow can break a suite-owned doc check no multiset reads. [INV-111, INV-39]
5. The system *shall* land one journal chapter naming what moved and why. [INV-111]

**Case: closing the pass**

6. *if* the pass rides a branch back to main, *then* the system *shall* close it through the restructure merge gate, where the multiset proof serves as the gate's first part; *if* the pass lands directly on main, *then* the system *shall* stand it on its own green suite. [INV-111, INV-114]
7. A host *shall* cite this vehicle and *shall* never improvise a layout pass. [INV-111]

---

## Requirement 184: A restructure or migration merge gate judges the delta

**Context:** When a restructure or a migration is gated for merging back into main, the gate judges the delta rather than re-proving the untouched whole. It has three parts and states pre-existing findings in the review record instead of blocking on them.

**User Story:** As a person merging a restructure or migration, I want the gate to judge only the delta, so that a large reorganization is verified without re-proving what it did not touch. [INV-114]

### Acceptance Criteria

**Case: the three parts**

1. *when* a restructure or migration is gated for merge, the system *shall* judge the delta in three parts: load-bearing token identity old-versus-new except the per-chunk named deltas plus the punctuation-multiset check; the full suite green on the merged tree; and a prover pass on both sides whose blocking set is scoped to the delta. [INV-114, INV-111, INV-39]
2. The system *shall* block on an unmatched token, a red suite, a new-side finding absent on the old side, or an unnamed meaning change. [INV-114]
3. *when* a finding is present and equal on both sides, the system *shall* state it in the review record of the same delivery and *shall* not block on it. [INV-114]

**Case: a deliberate redesign**

4. *if* a change is a deliberate redesign that changes content by intent, *then* the system *shall* route it by the architecture-redesign rule and stand its merge on the green suite and the delta-scoped prover pass, with no token-identity demand over text the redesign meant to change. [INV-114, INV-113]

**Case: a sharpened bar is said back**

5. *when* a session sharpens the human's spoken bar beyond the human's words, the system *shall* say the sharpened form back and mark it as its own interpretation. [INV-114]

---

## Requirement 185: The catch-up routing and its non-goals

**Context:** The catch-up sequence fires on one test: the host's recorded pack version is behind the current pack version. The owner's wording is an example, never the decider. A docs restructure with no version delta is the host's own queue row.

**User Story:** As the owner asking to bring a host up to date, I want the version delta alone to decide the routing, so that a same-version restructure is never misrouted into a migration sequence. [INV-110]

### Acceptance Criteria

**Case: the version delta decides**

1. *when* the host's recorded pack version is behind the current pack version, the system *shall* fire the catch-up sequence, whatever wording the ask used. [INV-110]
2. *if* an ask carries no version delta, *then* the system *shall* route it as the host's own queue row through its pipeline, whatever wording it used. [INV-110]
3. The system *shall* not fire catch-up on a first adoption, on a single-document edit, or on a restructure of the host's own product. [INV-110]

**Case: the non-goals**

4. The system *shall* execute catch-up as a procedure with no script automating it, *shall* force no rename, and *shall* keep no pack-side registry of hosts' catch-up states, since each host's own records carry its state. [INV-110]

---

## Requirement 299: A deployed kind declares what its owner changes without a build

**Context:** A project whose product is deployed carries a seam. On one side sits the build, holding the behaviour and the structure, everything that reaches production only by building the product again. On the other side sits the configuration: the values the shipped product already reads, which reach production by a deploy of configuration alone. The per-kind design principles named the visitor walk, the reachable flows, the register and the trigger, and said nothing about this seam, so a host could ship an experiment switch that costs a full build to turn off. The founding now names the seam once, and a check reads the host's own declaration.

**User Story:** As the owner of a deployed product, I want the switches, the copy and the thresholds I turn to live outside the build, so that a change of mine reaches production by a deploy of configuration alone.

### Acceptance Criteria

**Case: the seam is declared at founding**

1. *when* a project's product is deployed, the system *shall* record a `project.config-surface` line in the host profile naming what its owner changes without a build. [INV-291, INV-36]
2. The declaration *shall* name where those values live and how a change of them reaches production. [INV-291]
3. The system *shall* keep behaviour and structure in the code a build ships. [INV-291]
4. *when* nothing of a project is deployed, the system *shall* accept an explicit "none" as the founding's stated answer. [INV-291, INV-244]

**Case: which side of the seam a thing sits on**

5. The system *shall* place a value the shipped product already reads on the configuration side. [INV-291]
6. The system *shall* place a change that needs the code to do something it does not do today on the build side. [INV-291]
7. A value the product reads at build time *shall* sit on the build side until that reading moves to run time. [INV-291]

**Case: the check over the founding**

8. *when* a profile records `project.kind` and carries no `project.config-surface` record, a founding check *shall* red and *shall* name the missing line. [INV-291, INV-135, A-10]
9. *if* the declaration carries no words after its key, *then* the check *shall* red. [INV-291]
10. *if* a declaration answers "none" while the project's own `project.layers` line names a deployment layer, *then* the check *shall* red and *shall* quote both lines. [INV-291, INV-135]
11. The check *shall* read its keys and its word lists from `guardrails/config-surface.json`. [INV-291]
12. Each run *shall* state its reach: the two files it opens, and the three profile records it reads. [INV-269]
13. The check *shall* leave to the founding conversation and to the proof by deed whether a declared value truly reaches production with no build. [INV-291]

**Case: the per-kind table carries the principle**

14. The architecture document *shall* carry this principle in the per-kind design-principles table for every deployed kind, with both sides of the seam named. [INV-291, INV-136]
15. A kind whose product runs in no place its readers reach *shall* carry no such principle. [INV-291, INV-136]

---

## Requirement 308: A spoken sentence sets a project up on the pack

**Context:** The pack promises that a project is set up in plain words. Three sentences carry that promise: attaching an existing project, founding a new one, and bringing an adopted project onto a newer pack. Each has a walk. Reaching a walk needs a skill description a spoken sentence loads. It also needs a resolution of the pack's own tree, which lives outside the skills that install.

**User Story:** As a new installer, I want a plain sentence to run the right setup walk, so that I need no procedure file. [E-21]

### Acceptance Criteria

**Case: the sentence reaches one skill**

1. Exactly one installed skill description *shall* carry the setup entry, naming the pack in each of its trigger phrases. [A-0, E-21]
2. No second installed skill description *shall* carry those phrases. [INV-13]
   - a skill whose own vocabulary neighbours them names the setup entry as the earlier door.

**Case: the pack's tree resolves, or the run stops honestly**

3. *when* a setup run begins, the system *shall* resolve the pack tree by an ordered read list, the first hit winning. [INV-307, M-7]
   - the run says which read answered, the path it gave, and that tree's version before it moves.
4. *if* no read answers, *then* the system *shall* stop, *shall* hand the person one action that supplies the tree, and *shall* start no walk. [INV-307]
5. *when* the resolved tree's version differs from the installed skills' version, the system *shall* say both numbers aloud before the walk continues. [M-7, INV-307]
6. The system *shall* record the resolved path together with the read that produced it, so a later run can tell one install route from another. [A-7, M-7]

**Case: every setup sentence has a placed route**

7. The closed request set *shall* place all three setup sentences, each naming its entry document and its back-check. [INV-307, INV-151]

---

