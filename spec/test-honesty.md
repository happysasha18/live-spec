## Requirement 105: The test method lives in the test-author skill

**Context:** The test-author skill owns the test method, and the build pipeline calls it at the pipeline's matrix and test steps, the same way earlier steps call the spec-author and the prover. The method — the level ladder, real-artifact assertions, the red-first proof, the pinned skip-set, and traceability as a standing test — lives in the skill, and the pipeline keeps order and gates.

**User Story:** As a person deriving tests, I want the method held in one skill the pipeline calls, so that how to test lives in one place while the pipeline keeps the order and the gates.

### Acceptance Criteria

**Case: the pipeline calls the method**

1. *when* the pipeline reaches its matrix and test steps, the system *shall* run the test-author skill for the matrix derivation and the test writing, keeping order and gates in the pipeline. [E-27]
2. The system *shall* have the test-author skill hold the level ladder, real-artifact assertions, the red-first proof, the pinned skip-set, and traceability as a standing test. [E-27]

---

## Requirement 106: A test cleans up after itself and is born in a temp home

**Context:** Every test removes what it creates — temp files, fixtures on disk, spawned processes, mutated shared state — and a suite run leaves the machine as it found it. A test's files are born in the system temp home or the host's gitignored state directory and erased at the run's end; a user-visible folder is never a test's workspace, and a headless browser's download directory is pointed at the temp home. A leak is a defect of the test.

**User Story:** As a person whose machine runs the suite, I want each test to erase what it creates and write only into a temp home, so that a run leaves no residue in a folder the person can see.

### Acceptance Criteria

**Case: a test erases what it creates**

1. The system *shall* have every test remove what it creates and *shall* have a suite run leave the machine as it found it, a surviving artifact being a defect of the test. [INV-100]
2. The system *shall* birth a test's files in the system temp home or the gitignored state directory and erase them at the run's end, and *shall* point a headless browser's download directory at the temp home. [INV-100]

**Case: a user-visible folder is never a workspace**

3. The system *shall* never use a user-visible folder — Downloads, Desktop, Documents — as a test's workspace. [INV-100]
4. The system *shall* give each run a temp home of its own, *shall* fail the run on an artifact of that run's own surviving in it at session end, and *shall not* judge a run by what any other run left on the machine. The harness's own launch sweep clears a prior run's litter that its own teardown never reached. [INV-100]

---

## Requirement 107: A test's expected value is independent of the code under test

**Context:** A test compares the code's output against an expected value, and that expected value comes from a source other than the code under test. Recomputing the code's own formula and asserting the result is a mirror that can never catch the formula being wrong. Three sources of an expected value are legal, and one boundary keeps property tests in.

**User Story:** As a person trusting a passing test, I want its expected value drawn from an independent source, so that the check proves the behaviour rather than asserting the code equal to itself.

### Acceptance Criteria

**Case: the expected value comes from elsewhere**

1. The system *shall* draw a test's expected value from a source other than the code under test — a hand-computed constant, an independent derivation, or a recorded real output reviewed by a human. [INV-102]
2. The system *shall* refuse an assertion whose expected value is produced by the same formula the code runs. [INV-102]

**Case: the boundary keeps property tests in**

3. The system *shall* allow a round-trip or property test over the outputs, since it asserts an invariant over the outputs. [INV-102]

---

## Requirement 108: The ladder tops out below the real device

**Context:** Touch physics, scroll snapping, and background throttling live past a desktop headless browser's reach. A behaviour living there gets a real-device walk row, a matrix row the suite can never turn green, owed to the human's own hands before ship, kin of the feel pass. The suite says what it cannot see.

**User Story:** As a person trusting a green suite, I want a behaviour past the headless browser's reach to carry a walk row the suite can never green, so that a passing run claims nothing about a fact only a real device shows.

### Acceptance Criteria

**Case: the boundary is named honestly**

1. *when* a behaviour lives past a desktop headless browser — a momentum swipe on a real phone, a tab throttled in the background — the system *shall* give it a real-device walk row the suite can never turn green, owed to the human's hands before ship. [INV-77, INV-30]
2. The system *shall* let a green run over such a fact claim nothing about it, the suite stating what it cannot see. [INV-77]

---

## Requirement 109: A geometry fact is asserted relative, wide, and long

**Context:** A centering or positioning fact asserts relative geometry, at two or more viewport sizes, and after several consecutive steps of the interaction, so cumulative drift shows. An absolute-pixel assertion at one viewport after one step passes forever while each next step lands further off, and the drift hides from it by construction.

**User Story:** As a person guarding against drift, I want a geometry fact asserted relatively across at least two viewport sizes and after consecutive steps, so that cumulative drift a single absolute check would hide is made to show.

### Acceptance Criteria

**Case: relative, at more than one size, after more than one step**

1. The system *shall* assert a geometry fact as relative geometry — the distance between an element's center and the viewport's center staying within a small bound — at two or more viewport sizes. [INV-78]
   [GAP: the source asserts the center-to-center distance stays within a bound over a run of consecutive steps but names neither the tolerance, the step count, nor who sets them or their defaults, so a test author cannot pin the pass-or-fail boundary of the assertion.]
2. The system *shall* assert it after two or more consecutive interaction steps, so cumulative drift shows, and *shall* refuse an absolute-pixel assertion at one viewport after one step as one that hides the drift by construction. [INV-78]

---

## Requirement 110: An extracted engine tests on its own generic fixtures

**Context:** When a generic engine is carved out of a working project, the donor's data keeps the donor's shape, and a suite running only on it proves the donor and leaves the engine untested. So the engine's suite runs on engine-shaped fixtures, and every donor-specific constant the extraction finds becomes a named content-contract entry with a test that the engine works without it.

**User Story:** As a person carving an engine from an instance, I want its suite run on engine-shaped fixtures and each donor constant named in the content contract, so that the engine is proven independent of its first user.

### Acceptance Criteria

**Case: engine-shaped fixtures**

1. The system *shall* run an extracted engine's suite on engine-shaped fixtures carrying the engine's own ids and content model, letting the donor's data stay as an extra real-data suite and never as the only one. [INV-79]
2. *when* the extraction finds a donor-specific constant — an id format, a hardcoded wordmark, a path — the system *shall* record it as a named entry in the engine's content contract with a test that the engine works without it. [INV-79]

---

## Requirement 111: The suite's own plumbing must not lie

**Context:** Three legs of one class each cover a way the harness could lie about its own verdict. A skip path must execute even when never taken, a shim owes a re-export completeness test, and a background or delegated run's verdict is read from the suite log's own tail line, which a wrapper's exit code cannot fake.

**User Story:** As a person reading a suite's verdict, I want the plumbing that reports results held honest, so that a skip that cannot run reds, a missing re-export is caught, and a background run's verdict is read from its own log.

### Acceptance Criteria

**Case: the three plumbing legs**

1. The system *shall* import the skip helper at module load, so a skip path that cannot run reds instead of passing silently on the machine that needed it. [INV-80]
2. The system *shall* require an engine-or-instance shim to carry a re-export completeness test, a missing re-export otherwise keeping a whole suite silently red. [INV-80]
3. *when* a run is a background or delegated one, the system *shall* read its verdict from the suite log's own tail line, trusting no wrapper's exit code, a foreground gate reading its own child's exit staying legal. [INV-80]

---

## Requirement 112: A test is green only when it passes deterministically

**Context:** A test is green only when it passes for the same reason on every run. A test that passes on some runs and fails on others is flaky, and one question routes the flake: is the source of the nondeterminism removable in code the project owns. When it is, the flake is a defect fixed at that root, masked by no retry and no raised timeout; when it is not, it is workshop noise on the problem ledger.

**User Story:** As a person trusting a green run, I want a flake rooted in owned code fixed at that root and an external flake routed to the ledger, so that green means deterministic and no mask hides a real race.

### Acceptance Criteria

**Case: the seam question routes the flake**

1. *when* a test's nondeterminism is removable in owned code — a dependence on wall-clock time, on test ordering, on shared or leaked state, on an unseeded random draw, on a timing assumption, or a missing wait on an external tool — the system *shall* fix it at that root so the test passes every run for the same reason. [INV-155]
2. The system *shall* mask a flake with nothing: no retry, no rerun-until-green, no raised timeout that hides the race, and no single pass accepted as a pass. [INV-155]
3. *when* the nondeterminism is not removable in owned code, the system *shall* route it to the problem ledger as workshop noise, a home apart from the owned defect. [INV-155, INV-23]

**Case: the enforcing nets**

4. The system *shall* grep the test configuration for a retry or rerun-until-green plugin and red the run when one appears, leaving the rest to the verify walk's discipline, kin of the fresh-eyes audit. [INV-155, INV-46]
5. *when* a flake's root is understood but not removable in one landing, the system *shall* quarantine it by name in the pinned skip-set with a dated reason and an owning queue row. [INV-155]
   - an open quarantine holds no landing and stands as a debt the milestone audit reads.

---

## Requirement 113: A check earns its pass only over a non-empty set

**Context:** A check whose input set is empty reports clean while testing nothing — a uniqueness scan over zero items finds zero collisions, and the green says only that nothing was looked at. An empty input set is nearly always the defect: the parse broke or the source moved. So a check declares the input set it expects to be non-empty, and an empty set reds by name in place of passing silently.

**User Story:** As a person trusting a clean check, I want an empty input set to red by name, so that a broken parse or a moved source cannot pass as a check that examined nothing.

### Acceptance Criteria

**Case: an empty set reds by name**

1. The system *shall* have a check declare the input set it expects to be non-empty and *shall* red by name when that set is empty, the way an unexpected skip is a failure outright. [INV-218]
2. *where* a check may legitimately read an empty set, the system *shall* have that call site name its own reason, the default being that empty is a finding. [INV-218]

---

## Requirement 114: The browser harness launches muted and reaps what it spawned

**Context:** A harness that drives a real browser starts it muted through the browser's own mute flag, so a run makes no sound on the machine it runs on. On teardown it reaps the whole process group it launched; on launch it sweeps any stale process group and temp litter a prior run left, found by its own profile marker, since the system temp is not self-purging. It bounds each command with a real per-command deadline, prefers the dedicated headless build, and runs a launch probe before any suite is trusted.

**User Story:** As a person whose machine runs the suite, I want the harness muted, self-reaping, deadline-bounded, and probed at launch, so that a run leaves the machine as it found it and a faulty browser fails loudly by name rather than bleeding false reds.

### Acceptance Criteria

**Case: muted, reaping, and self-sweeping**

1. *when* the harness launches a browser, the system *shall* pass the browser's own mute flag so the run makes no sound, and *shall* reap the whole process group on teardown so no orphan survives the run. [INV-157, INV-100]
2. *when* the harness launches, the system *shall* sweep any stale process group and temp litter a prior run left, found by the harness's own profile marker, leaving a young ownerless directory alone as a live sibling mid-launch. [INV-157, INV-100]
   [GAP: the sweep reaps an old ownerless profile directory and leaves a young one, but the source names no age boundary between young and old, nor its owner or default, so a test author cannot pin when the sweep reaps an ownerless directory.]

**Case: the bounded deadline**

3. The system *shall* bound each command it sends the browser with a real per-command deadline, so a slow machine waits while a genuine hang fails with a bounded error, and *shall* never inflate a timeout that would bury a real race. [INV-157, INV-155]

**Case: the right binary and the launch probe**

4. The system *shall* prefer `chrome-headless-shell` as the binary, newest install first, falling back to Chrome for Testing then a system Chrome, and *shall* drop the extra headless flag when the shell is the pick. [INV-157]
5. *when* a suite is about to be trusted, the system *shall* run a launch probe, and *shall* fail a stalling or frame-dead browser loudly under the probe's own name. [INV-157]
   - the launch probe is one page served from the loopback address, loaded and then awaited for a single compositor frame, each leg under its own bounded window.

**Case: the nets and the owned-fault boundary**

6. The system *shall* assert in the pack's own suite that the shipped template carries the mute flag, the launch sweep, the process-group reap, and the bounded deadline, and *shall* assert by deed in a consuming product's suite through a post-run process-group check that reds on a surviving orphan. [INV-157, INV-150]
7. *when* a script both launches a real headless Chrome and carries the mute flag nowhere in its comment-stripped code, the system *shall* red the run through a guardrail that reads every tracked script whole, catching a hand-rolled harness's unmuted launch across the existing tree the same run the gate is added. [INV-157]
8. *when* a harness fault is caused by its own run hygiene, the system *shall* root-fix it here and *shall* route only a fault with nothing to correct in owned code to the problem ledger. [INV-157, INV-23]

---

## Requirement 115: The browser harness has one canonical home

**Context:** The harness that drives a real browser is one artifact, shipped once by the pack as a template rather than copied into each project. A consumer adopts it by updating the pack, layering its own project-specific driving methods on the shared core, so a fix to the core lands once and reaches every consumer.

**User Story:** As a person maintaining the harness, I want its core shipped once and adopted by an update, so that a hardening lands in one place and no divergent private copy can drift.

### Acceptance Criteria

**Case: one home, adopted by update**

1. The system *shall* ship the harness core once as a pack template and *shall* have a consumer adopt it by updating the pack through the catch-up walk, layering its own driving methods on the shared core. [INV-158, INV-110]
2. The system *shall* land a fix to the core — the launch flags, the teardown, the deadline — once and reach every consumer through the update, the migration path a package update carries. [INV-158, INV-91]

**Case: a fork owns its divergence**

3. *when* a project forks a private copy of the harness, the system *shall* have that project own the divergence it creates, the third mute-launch net still catching a forked unmuted launch in any tracked tree, this being the centralize pole of the pack-to-host split. [INV-158, INV-157, INV-163]

---

## Requirement 116: The suite-honesty invariants are one class, each naming its net

**Context:** The test-infrastructure family — INV-77, INV-78, INV-79, INV-80, INV-100, INV-102, INV-155, INV-157, INV-158 — shares one role: each member closes a way the suite could pass green while the fact it claims is false, or leaves the machine worse than it found it. The class carries one parity — each member names its net past merely naming the fix. For most members the net is a mechanical check; for a few the assertion shape itself is the net, among them the real-device walk row the suite can never green. The class binds forward [INV-159], a new suite-honesty invariant stating its net against this parity while members declared before the class stand unreshaped.

**User Story:** As a person relying on the suite-honesty class, I want every member to name the net that reds a run on its violation, so that a member naming no net is caught as a class defect.

### Acceptance Criteria

**Case: every member names its net**

1. The system *shall* have each suite-honesty member name the net that reds a run on a regression, the assertion shape itself being the net for the real-device walk row, the relative-wide-long geometry, and the engine-shaped fixtures. [INV-160]
2. *when* a member names no such net, the system *shall* read it as a class defect the prover blocks, the same standing an under-enumerated review-record member has. [INV-160, INV-125, INV-156]

**Case: the class binds forward**

3. *when* a new suite-honesty invariant is stated, the system *shall* have it state its net against this parity and *shall* leave members declared before the class unreshaped. [INV-160, INV-157, INV-158, INV-159]

---

## Requirement 117: A cleanup touches only what it owns

**Context:** A cleanup — a teardown, a stray-process sweep, a temp purge — acts only on what this run provably created and owns, or a prior run of the same harness whose recorded owner is provably dead, and never on a shared resource another party is using. The guard denies every ending that names a name, because a name cannot tell this run's copy of a program from the person's own copy.

**User Story:** As a person sharing a machine with the pack, I want a cleanup scoped to what the run provably owns and every name-based kill refused, so that the person's own program is never reaped.

### Acceptance Criteria

**Case: the test is current use and provable ownership**

1. *when* a cleanup would touch a shared resource, the system *shall* act only on what this run provably owns, and *shall* leave a resource in current use untouched. [INV-162, INV-157]
   - a shared resource is a process, temp directory, port, file, lock, or the display;
   - this run's provable ownership reaches a prior run's resource whose recorded owner is provably dead.
2. The system *shall* target a kill by a recorded process identifier, a process group the run holds, or an install path under the run's own tree, and *shall* read the recorded process group as the sole safe target on a machine shared with other sessions. [INV-162]

**Case: the guard refuses a name**

3. The system *shall* refuse a command that ends a process by a bare name — a name pattern, or a lookup that resolves a name to an identifier — since it reaches whatever on the machine answers to that name. [INV-162]
4. The system *shall* hold this class over every process the pack runs a copy of — the browser, the language runtime and its separation tool, the bundler, the media tool — and *shall* leave a program the pack never launches beside the point. [INV-162]

**Case: the nets and the notice**

5. *when* a tracked script ends a process by name with no identifier, process-group, or owned-path proof, the system *shall* red it through a guardrail carrying a committed probe corpus, so a later widening cannot silently narrow the check. [INV-162]
6. *when* the pack ends any process, the system *shall* announce what it ended and why the run owned it, so an ending nobody expected is visible the moment it happens. [INV-162, INV-204]

---

