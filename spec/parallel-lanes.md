## Requirement 77: Intake is parallel, integration is serial — one landing under one pen

**Context:** While the session walks, intake is parallel and integration is serial: one landing at a time, per repo, under one pen. The pen is the right to write the shared truth — the spec, the architecture doc, the test matrix, the queue, the integration of a delta, the closing of a row. One lane holds it at a time, and claiming a lane is an atomic committed act.

**User Story:** As a person whose repo two sessions might share, I want one landing at a time under one pen with claims resolved by a total order, so that two lanes never scramble the shared tree and exactly one claimant backs off.

### Acceptance Criteria

**Case: the pen and the atomic claim**

1. The system *shall* hold the right to write the shared truth — the spec, the architecture doc, the test matrix, the queue, the integration of a delta, and the closing of a row — under one pen one lane holds at a time. [INV-2]
2. *when* a lane is claimed, the system *shall* commit the row-to-in-work flip first, then re-check under the concurrent-edit fence right before its first shared-truth write, and *shall* have the later claimant back off and re-queue *when* the re-check finds a foreign session's committed in-work row. [INV-2, INV-11]

**Case: the total order picks the winner**

3. The system *shall* read later by a total order that git ancestry defines: the claim whose commit is the ancestor in git history holds, and *when* two concurrent claims share no ancestry the claim whose session identity sorts lower holds; a wall-clock timestamp never enters the ordering. [INV-2, INV-117]
4. The system *shall* record the claiming session's identity in the flip so a peer computes the same order from either side, backing off exactly one session and never both. [INV-2, INV-117]

**Case: workers overlap, foreign hands never share the pen**

5. The system *shall* let bounded delegated workers overlap on disjoint brief-named files or an isolated tree with the concurrent-edit fence armed, and *shall* have a new wish wait its turn unless a bug preempts. [INV-2, ACT-3, T-10]

---

## Requirement 78: A pending question never stops the work, and no decision is silent

**Context:** Three more things hold while the session walks: a pending question never stops the work, no micro-decision is made silently, and every landing cites its wish row. The batched report carries the no-silent-decisions rule as its own postcondition.

**User Story:** As a person waiting on a decision, I want the lane to proceed on the recommended option while every choice not in my wish is asked or recorded and surfaced, so that a pending question never stalls the work and nothing is decided and buried.

### Acceptance Criteria

**Case: the pending question and the silent-decision ban**

1. *when* a question for the human is open, the system *shall* proceed on the recommended option and keep the question open in the row, revisitable any time. [INV-4]
2. The system *shall* make every choice not in the human's wish either asked or recorded in the spec and surfaced in the same batched report, reading a decision absent from the report as silent by definition. [INV-5]

**Case: every landing cites its wish**

3. The system *shall* have every landing name its wish row in the commit message or journal entry, so why a change exists is always answerable. [INV-3]

---

## Requirement 79: Each session carries a stable identity minted at its start

**Context:** Before its first act — before the inbox sweep — a session mints one identity and records it in its session checkpoint under `.live-spec/`, unchanged for the session's life. This identity is what the pen tie-break orders on, and it exists for every session.

**User Story:** As a person whose repo carries several sessions, I want each to mint a stable identity at its start, so that two sessions racing one claim compute the same tie-break order and the inbox source-mark reuses that one identity.

### Acceptance Criteria

**Case: the identity every session mints**

1. *when* a session starts, the system *shall* mint one identity before its first act and record it in the session checkpoint under `.live-spec/`, unchanged for the session's life. [INV-117]
2. The system *shall* use the harness session identity where the context carries one and otherwise mint the identity from the session's start moment joined with its worktree path and a nonce, carrying enough entropy to be unique. [INV-117]

**Case: one identity, reused by the source-mark**

3. The system *shall* order the pen tie-break on this identity and *shall* make the inbox source-mark's short session token a projection of that same one identity. [INV-117, T-10]

---

## Requirement 80: Trains may roll — one pen writes

**Context:** Parallelism already runs below the lane; this law lifts it to feature level where it is safe. One assigned session may hold up to the profile-declared lane cap of build lanes in-work at once, with a package default of three. The seat's independence read runs as the dependency graph over the runnable rows, and a lane opens only when that graph shows the lanes pairwise independent, the verdict narrated aloud as the lane opens. Everything that does not write the shared truth may overlap; everything that writes it takes the pen one lane at a time.

**User Story:** As a person whose session has independent work waiting, I want several lanes rolled at once up to the cap while every shared-document write and every landing passes through one pen, so that independent work proceeds together without the lanes corrupting each other's tree.

### Acceptance Criteria

**Case: the cap and the independence condition**

1. The system *shall* hold up to the profile-declared lane cap of build lanes in-work at once, a settings-ladder value with a package default of three, opening a lane only *when* the independence graph shows the lanes pairwise independent, narrating that read aloud as the lane opens. [T-18, E-13, INV-49]
2. *when* work waits past the cap, the system *shall* raise the cap only on the human's asked word, a session-scope settings-ladder value that outranks the profile's declared cap, and *shall* then open one more lane under the raised value, and *shall* never count read-only background analysis against the cap. [T-18, E-13]

**Case: what overlaps and what takes the pen**

3. The system *shall* let a later train's code and tests in its own isolated tree, read-only analysis and research, and a prover run reading committed law overlap. [T-18]
4. The system *shall* take the pen one lane at a time for edits to every shared document, the integration of a lane's delta, and the closing of a row, so two lanes' document stages never interleave mid-edit. [T-18]

**Case: the board, the bug, and the milestone**

5. The system *shall* show every rolling train on the board with its own station line, have a waiting lane name the row it waits behind, and ride the rolling trains' questions on one batched decision page. [T-18, INV-27, INV-4]
6. *when* a bug arrives, the system *shall* take the pen for it at the end of the current pen-stage, never cutting a pen-stage mid-edit and letting no lane take the pen back until the bug lands. [T-18, T-9]
7. *when* a milestone runs, the system *shall* run its whole-spec operations with one train only, holding the other lanes at a clean checkpoint and resuming them in landing order once the milestone lands. [T-18, M-1]

**Case: the held-for-milestone state**

8. *when* a milestone holds the other lanes, the system *shall* quiesce each in a distinct held-for-milestone state, named apart from bug-parked because nothing failed. [T-18, M-1]

---

## Requirement 81: A landing commit carries exactly one row's delta

**Context:** A milestone gate is one indivisible pen-stage: a bug arriving mid-gate waits for the gate to finish rather than preempting a half-run audit. While several trains roll, the landing stays pure — a landing commit carries exactly one row's delta and its gate runs on a tree holding nothing of any other lane's unfinished work.

**User Story:** As a person trusting a landing, I want each landing commit to carry exactly one row's delta gated on a clean tree, so that half of another train never rides a landing and the lane that landed first wins.

### Acceptance Criteria

**Case: the milestone gate is one pen-stage**

1. *when* a bug arrives mid-gate, the system *shall* have it wait for the milestone gate to finish, then take the pen the moment the milestone lands, ahead of the held lanes' resume. [T-18, T-9]
   - this is the one exception to a bug cutting the line at the end of the current pen-stage.

**Case: the pure landing**

2. The system *shall* have a landing commit carry exactly one row's delta and run its gate — the full suite plus the guardrails — on a tree holding nothing of any other lane's unfinished work. [INV-39]
3. *when* a lane lands, the system *shall* have every still-rolling lane re-check under the fence and re-run its gate against the tree as it now stands, landed-first winning and the later lanes re-verifying. [INV-39, INV-11]

---

## Requirement 82: Lanes are picked by a graph, never by mood

**Context:** At queue-take the session reads the runnable head and builds a dependency graph. It draws an edge between two runnable movements only on a true dependency or a same-section collision. Mere co-location in a shared living document draws no edge, since the shared living documents are a convergence point reconciled at integration, never a serializing surface.

**User Story:** As a person with independent work waiting, I want lanes picked from a dependency graph rather than by mood, so that movements that merely share a living document still parallelize and only genuinely dependent or same-section rows serialize.

### Acceptance Criteria

**Case: the edge and the non-edge**

1. *when* the session takes the queue, the system *shall* build a dependency graph over the runnable head, drawing an edge only on a true dependency — one movement needs another's landed output — or a same-section collision where two movements rewrite the same clause or behaviour rule. [INV-49]
2. The system *shall* draw no edge on co-location in a shared living document, treating the spec, the architecture, and the test matrix as a convergence point reconciled at integration. [INV-49, INV-198]

**Case: the lane set and when not to parallelize**

3. The system *shall* open lanes on a pairwise-independent set up to the cap, serialize rows joined by an edge inside one lane, and pre-roll integration-only collisions with the landing order declared at claim time, the later lane re-fencing on the new truth. [INV-49, T-18, INV-39]
4. The system *shall* ride tiny rows serial since parallel pays only *when* build stages dominate the pen work, narrate the chosen set and order at opening, and hold false-serialization to the seat's read rather than a gate. [INV-49, INV-214]
   [GAP: the source rides tiny rows serial when build stages do not dominate the pen work but states no measure of a tiny row or of when build stages dominate; the seat judges with no stated threshold.]

---

## Requirement 83: A lane's isolated copy is a branch in its own worktree

**Context:** The isolated copy where a later train writes its code and tests is a git worktree holding a branch of its own. A lane delegated to a worker takes one through the Agent tool's worktree isolation option, which carries no gate, and the worker's brief names the branch its work rides.

**User Story:** As a person rolling a worker lane, I want its isolated copy to be a git worktree holding its own branch, so that the lane builds in real isolation and its open lanes read off the machine itself.

### Acceptance Criteria

**Case: the worktree branch a worker lane takes**

1. The system *shall* make a lane's isolated copy a git worktree holding a branch of its own, carrying that lane's code and tests. [E-34]
2. *when* a lane is delegated to a worker, the system *shall* take a worktree through the Agent tool's worktree isolation option with no permission gate and name the branch in the worker's brief. [E-34, INV-201]

**Case: overlapping lanes default to isolation**

3. The system *shall* follow the overlapping-write-set isolation default stated once at the concurrent-edit fence requirement. [E-34, INV-105]

---

## Requirement 84: A lane branch is born from the claim commit, on main

**Context:** The claim's row-to-in-work flip is committed to main under the pen, and the branch is cut from that commit. The claim lands on main because two claims are ordered by git ancestry and a peer reads that ancestry from the refs the worktrees share, so a claim on a lane's own branch would sit outside the ordering.

**User Story:** As a person opening a lane, I want its branch cut from a claim commit on main, so that two sessions' claims stay ordered by git ancestry and the open lanes read off the branch names.

### Acceptance Criteria

**Case: the branch cut from the claim commit**

1. *when* a lane is claimed, the system *shall* commit the row-to-in-work flip to main under the pen and cut the branch from that commit, naming it for its row as `lane/<row>-<slug>`. [T-23]
2. The system *shall* land the claim on main so two claims order by git ancestry, since a claim committed on a lane's own branch would leave two sessions each reading itself as first. [T-23, INV-2, INV-117]

---

## Requirement 85: The pen moves main, and a lane's branch is penless

**Context:** Under branches the shared tree is main, so holding the pen is the sole right to move main. A lane commits to its own branch as often as it likes, and that traffic is penless. Git holds the same bound on its own, refusing every other worktree's attempt to check out, force, or push to a branch a tree holds checked out, though three named roads walk past even that refusal.

**User Story:** As a person integrating a lane, I want holding the pen to be the sole right to move main while a lane commits freely to its branch, so that git turns back the roads a lane walks by habit ahead of any gate the pack writes.

### Acceptance Criteria

**Case: the pen owns main, the branch is free**

1. The system *shall* make holding the pen the sole right to move main and *shall* let a lane commit to its own branch freely as penless traffic, since nothing another lane reads has moved. [INV-198, T-18]
2. The system *shall* rely on git refusing every other worktree's attempt to check out, force, or push to a branch a tree holds checked out as a strong first net, naming its three known edges — `git update-ref`, the `--ignore-other-worktrees` flag, and a changed `receive.denyCurrentBranch` — rather than a guarantee. [INV-198]

**Case: the pen still keeps the shared documents**

3. The system *shall* keep every document on the pen's list under the pen even under branches, since two lanes drafting deltas on two branches would each prove against a spec the other is about to move and no suite reads a proof. [INV-198, E-34, INV-101]
4. The system *shall* keep the shared tree clean of every lane's unfinished work, turning the one-row landing commit's precondition from a discipline into a structure. [INV-198, INV-39]

**Case: the config-health check**

5. *when* a repository holds more than one worktree, the system *shall* red a primary tree that does not hold main in the config-health check, reading the primary tree's own checked-out branch off git's shared worktree metadata rather than the invoking tree's; a single-worktree repository has no lane to protect against and is not this arm's concern. [INV-198]

---

## Requirement 86: A lane lands by fast-forward from a rebased branch

**Context:** At integration the lane takes the pen, rebases its branch onto main's tip, runs the landing gate on the rebased tree, and fast-forwards main onto it. Rebase and fast-forward are what the existing law already demands, since a merge commit's second parent would break the one-row landing commit and a linear main keeps the claim ordering total. A landed lane's branch and worktree are removed at the landing.

**User Story:** As a person landing a lane, I want it to rebase onto main's tip and fast-forward with the branch torn down, so that main stays a linear one-commit-per-row history and the gate never reads a stale tree.

### Acceptance Criteria

**Case: rebase, gate, fast-forward**

1. *when* a lane integrates, the system *shall* take the pen, rebase its branch onto main's tip, run the landing gate on the rebased tree, and advance main onto it with no merge commit. [INV-199, INV-39, INV-2]
2. The system *shall* stand one check ahead of the gate — the branch's merge-base with main equals main's tip — redding a lane that has not rebased so the gate never reads a stale tree. [INV-199, T-23]

**Case: teardown at the landing**

3. *when* a lane lands, the system *shall* remove its branch and worktree, and *shall* keep both on a parked lane with the board saying which. [INV-199, T-9, INV-27]
4. The system *shall* refuse teardown on a worktree holding uncommitted work and read that refusal as a finding, and *shall* red a lane worktree or a lane branch with no open row in the config-health gate. [INV-199, INV-150]

**Case: the merge-base check and the stale-lane check**

5. The system *shall* red, ahead of the landing gate, a lane whose branch's merge-base with main does not equal main's tip, reading either the invoking tree's own `HEAD` or a named worktree's, and *shall* run that check from the landing act itself, before the gate reads the tree. [INV-199]
6. The system *shall* red, in the config-health gate, a lane worktree or a `lane/*` branch whose row is closed or missing from the list, reading the rows off the primary tree's own list file so the answer does not depend on which tree asked, and standing down by name where the repository carries no list file for a lane to be stale against. [INV-199]

---

## Requirement 87: A textual conflict is the lane's own work, and a semantic one meets the nets that exist

**Context:** Git halts the rebase on a textual conflict and the landing cannot proceed, so the tool is that net; the lane resolves it in its own worktree and re-runs its gate from the top. A semantic conflict is the one that survives a clean textual merge, and the road holds two nets for it.

**User Story:** As a person rebasing a lane, I want a textual conflict resolved as my own work and a semantic one met by the nets that exist, so that the road claims no net it does not hold and a residual is named honestly.

### Acceptance Criteria

**Case: the textual conflict**

1. *when* git halts the rebase on a textual conflict, the system *shall* have the lane resolve it in its own worktree and re-run its gate from the top on the resolved tree. [INV-200]

**Case: the semantic conflict and its residual**

2. The system *shall* meet a semantic conflict with the two nets that exist — the pen keeping every document delta together so two lanes' documents never diverge, and the full suite on the rebased tree reading two lanes' diverging code. [INV-200, INV-198]
3. *when* a semantic conflict survives a green suite on the rebased tree, the system *shall* name it a test-matrix gap and route it to the test matrix's own home rather than invent a net here. [INV-200, INV-73, E-15]

---

## Requirement 88: The isolation default and the worktree tool agree through one vendored line

**Context:** The isolation law fires on a machine-readable condition — two lanes' write-sets overlap — while the worktree tool fires only on a human's word or a project instruction and lists feature work among the cases it declines. So today neither fires and the fallback is the shared tree the law forbids. The tool accepts a project instruction as authorization equal to a human's word, so adoption vendors one line into the host's project instructions.

**User Story:** As a person adopting the pack, I want one vendored line to make the isolation law and the worktree tool agree, so that the two fire on one condition without a second home for it and the line is scoped to the host that adopted.

### Acceptance Criteria

**Case: the vendored line cites the law's condition**

1. The system *shall* vendor one line into the host's project instructions that cites the isolation law's write-set condition rather than restating it, keeping the condition's one home. [INV-201, INV-105, INV-101]
2. The system *shall* scope the line to the host it governs and version it in that host's own tree, carrying it to an already-adopted host through the catch-up walk. [INV-201, A-11, INV-159]

**Case: the line records the host owner's word**

3. *when* the host owner's word for the host's tree is spoken, the system *shall* write the vendored line recording that word, and *shall* leave the session lane shut until the pack's own owner gives the word for the pack's line. [INV-201, INV-152, INV-4]
4. The system *shall* red a host whose project instructions carry no worktree line at the adoption gate, a mechanical gate the adoption and catch-up walks read as the closing step of their own gate-installing command rather than one wired into every push. [INV-201, INV-150]
5. The system *shall* require no vendored line for a worker lane, since the subagent's isolation option carries no gate. [INV-201, E-34]

---

## Requirement 89: The cap holds at three, and across sessions the pen's arbitration fires

**Context:** The lane cap is the profile-declared value with a package default of three. The branch road removes the tree's cost — a lane writes no tree another lane reads — but the three costs that bound the cap survive untouched, so the tree was never what bound it. The lanes law does not fire across sessions, and that sentence scopes the cap, the board, and the independence judgment; the pen's arbitration fires across sessions and always did.

**User Story:** As a person running lanes, I want the cap held at its declared value and the pen's cross-session arbitration recognized, so that removing the tree's cost is no reason to raise the number and two sessions on one repo need no new law.

### Acceptance Criteria

**Case: the three surviving costs hold the cap**

1. The system *shall* hold the cap at its declared value, three by the package default and by the profile line, since the branch road touches none of the three costs that bound it — pen-wait, the rebase-and-re-gate work every landing forces on every rolling lane, and the seat's dividing review attention. [T-18, E-13]
2. The system *shall* proceed on this recommendation while the owner's word on raising the cap stays owed, naming the measurement the pack has not taken — pen-wait time per lane and re-fences per landing. [T-18, INV-4]

**Case: the pen arbitrates across sessions**

3. The system *shall* scope the cap, the board, and the independence judgment to one session and *shall* fire the pen's arbitration across sessions, a foreign session's claim commit on main being readable with no fetch. [T-18, INV-198, INV-2]
4. *when* a second session takes a lane on one repo, the system *shall* give it its own worktree and branch under the stated road with no new law, since two worktrees share one object store and one set of refs. [T-18, INV-11, INV-117]

---

## Requirement 90: The branch road's machines, and what each one owes

**Context:** The branch road stands on machines. The road states each machine's boundary rather than hiding it, so it claims no net it does not hold.

**User Story:** As a person relying on the branch road, I want each of its machines named with what it owes, so that git's known-edged refusals and the pack's own gates together cover the roads a lane walks.

### Acceptance Criteria

**Case: git's own machines**

1. The system *shall* rely on git refusing every other worktree's checkout, branch-force, and push against a branch a tree holds checked out, and on git halting a rebase on a textual conflict, as strong nets whose edges are known. [T-23, INV-198]
2. The system *shall* carry the roads git leaves open — a moved checked-out branch, a documented override flag, a changed refusal default — in the pack's own gates below. [T-23, INV-198]

**Case: the pack's four build-half machines**

3. The system *shall* red a branch whose merge-base sits behind main's tip in the merge-base check, red a lane worktree or a lane branch carrying no open queue row and a primary tree that does not hold main in the config-health check, red a host whose project instructions carry no worktree line in the adoption gate, and red a lane opened past the cap in the board's lane-count check. [T-23, INV-150]
4. The system *shall* make all four mechanical gates under the net-routing law, since a deterministic check decides every one of these violations. [T-23, INV-150, INV-101]

**Case: what the road fences and leaves out**

5. The system *shall* leave the pen's document list unchanged. [T-23, INV-39, INV-2, INV-117, INV-105, INV-101, INV-11, INV-10]
   - keeps the one-row landing commit and its clean-tree gate;
   - keeps the claim ordering and its tie-break;
   - keeps the isolation condition's one home;
   - keeps write-ownership untouched;
   - opens no cross-session cap, no cross-session board, no automatic conflict resolution;
   - opens no long-lived or pushed branch, no merge commit on main.

---

## Requirement 91: Opening a lane is a performed act, and single-file work while lanes stand free is a recorded choice

**Context:** A grant with no performed step leaves the session on the single-file road every time. So opening a lane is a named act with a performable procedure, run when the independence graph shows two or more independent runnable rows and lanes stand free under the cap. Going single-file while lanes stand free is a recorded choice said aloud on the board.

**User Story:** As a person asking one window for parallel work, I want opening a lane to be a performed act and going single-file a recorded choice, so that the law's grant of parallel lanes actually gets used instead of items rolling one after another.

### Acceptance Criteria

**Case: the performed lane-open act**

1. *when* the independence graph shows two or more independent runnable rows and lanes stand free under the cap, the system *shall* perform the lane-open act. [INV-214, INV-49, INV-198, T-23, E-34, T-18]
   - the system reads that graph verdict as the seat's own independence judgment;
   - the lane-open act commits the row-to-in-work flip on main under the pen;
   - the lane-open act cuts the branch into its own worktree;
   - the lane-open act delegates the lane to a worker whose brief names the branch.
2. The system *shall* offer the act as `scripts/open-lane.sh`, which reads the settings-ladder-resolved cap and refuses to open a lane past that value. [INV-214, E-13, INV-11, INV-39]
   - the script runs the fence before it commits;
   - it carries the claim commit alone, so the landing keeps its one-row delta.

**Case: single-file is a recorded, ungated choice**

3. *when* the session goes single-file while the graph shows free independent lanes, the system *shall* say so on the board as the serial-by-the-graph line, naming which standing reason holds — a shared-section collision, a full cap, tiny rows, or a dependency. [INV-214, INV-49]
4. The system *shall* keep the recorded-reason duty a matter of discipline, since judging two rows independent is the independence graph itself and the lane branches that would evidence a parallel run are torn down at each landing, leaving the cap refusal as the one mechanical guard the act carries. [INV-214, T-23]

---

