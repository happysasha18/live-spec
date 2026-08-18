## Requirement 125: Every movement ends at a safe breakpoint

**Context:** Every movement ends the same way: the resume file's live state is overwritten in place, a dated journal entry is added, and the work is committed. Session memory can then be wiped with no loss, and the journal entry is the durable net where the resume file is gitignored. At a breakpoint the agent compacts its own context and says so, and on the way back it re-checks skill freshness.

**User Story:** As a person handing off a session, I want every movement to end with the resume state replaced, a journal entry added, and a commit, so that memory can be wiped with zero loss.

### Acceptance Criteria

**Case: the movement-end routine**

1. *when* a movement ends, the system *shall* replace the resume file's live state rather than stack it, add a dated journal entry, and commit, so session memory can be wiped with no loss. [M-2]
2. The system *shall* treat the journal entry as the durable net, since the resume file may be gitignored, and *shall* leave a full wipe or clear as the human's move. [M-2]

**Case: compaction and the way back**

3. *when* a breakpoint is reached, the system *shall* compact its own context and say so rather than silently, and *shall* re-check skill freshness on the way back. [M-2, A-7]

---

## Requirement 126: A landing closes the checkpoints it shipped

**Context:** A landing that ships a checkpoint's items flips that checkpoint to its closed state in the same landing. The movement that writes the work into git history also marks the checkpoint done, so a returning session never reopens finished work. The closing sweep rides beside the resume-file replacement.

**User Story:** As a returning session, I want a checkpoint whose items shipped flipped closed in the same landing, so that finished work is never reopened.

### Acceptance Criteria

**Case: the closing sweep**

1. *when* a landing ships a checkpoint's items, the system *shall* flip that checkpoint to its closed state in the same landing, the closing sweep riding beside the resume-file replacement. [INV-107]
2. The system *shall* read a checkpoint whose items all live in git history as stale by definition, and *shall* fail the landing on a checkpoint left reading as not started after its items shipped. [INV-107]

---

## Requirement 127: The resume file is a digest with no redundancy

**Context:** The resume file is read in one minute at a cold start, so growth is a design failure. The file's law is qualitative: it carries one live-state block, holding nothing a reader could lose without losing information. A suite check watches for drift, catching a bloated file with a synthetic fixture. An open leg is restated as one terse line, and its detail flows to its home.

**User Story:** As a returning session, I want the resume file held to its digest law and each open leg stated in one terse line, so that a cold start reads a short current picture.

### Acceptance Criteria

**Case: the digest law and its check**

1. The system *shall* hold the whole resume file to one live-state block and a digest with no redundancy — nothing removable without losing information. A suite check *shall* own that shape, reddening on a bloated file proven with a synthetic one. [INV-48]
2. The system *shall* restate an open leg as one terse line — its name, what stays open, and where the detail lives — and *shall* move the detail to the journal, the queue row, or the record the line points at. [INV-48, INV-26]
3. The system *shall* have compaction move prose to its home and *shall* never let it drop an open leg. [INV-48, INV-26]

---

## Requirement 303: A session's record is read at both ends by an agent that did not live it

**Context:** A session that lived the work reads its own record badly. A session writing its own handover from memory names a question as waiting for the person who already answered it. So a session's record is read at both ends by a fresh agent. That agent reads a compact extract of the person's own turns, where the raw transcript runs to megabytes.

**User Story:** As the owner, I want a fresh agent reading my own turns, so that no decision of mine returns as waiting.

### Acceptance Criteria

**Case: the extract of the person's own turns**

1. The system *shall* write the person's own turns from one session transcript into one session extract. [INV-302]
2. Each written turn *shall* carry its timestamp and its text. [INV-302]
3. The system *shall* take a transcript file *when* any line in it names the repository path. [INV-302]
4. The system *shall* read every human turn in a taken file, whatever working directory a line records. [INV-302]
5. The system *shall* count a user line as human *when* it carries no tool result, no sidechain mark, and no meta mark. [INV-302]
6. The system *shall* drop a turn whose whole text is a harness wrapper. [INV-302]
7. The system *shall* strip a harness wrapper out of a turn that also carries the person's own words. [INV-302]
8. The system *shall* write the session extract outside the repository, since a transcript holds private conversation. [INV-302]
9. Each run that writes an extract *shall* state its reach: the transcript it read, the count of human turns, and both file sizes. [INV-302, INV-269]
10. *when* a session closes, the system *shall* run the extractor over that session's transcript before the handover is written. [INV-302]

**Case: the closing step**

11. *when* a session closes, the system *shall* have a fresh agent session write the session handover from the extract. [INV-302]
12. The system *shall* keep the session that lived the work from writing its own handover. [INV-302]
13. *when* a movement ends, the system *shall* write the session handover beside the resume file's replacement. [INV-302, M-2]
14. The system *shall* spawn the handover's reader before the wind-down reaches its safe point. [INV-302, INV-95]
15. The system *shall* write a session handover under `docs/handovers/` under a file name ending in `-handover.md`. [INV-302]
16. A session handover's file name *shall* carry its date and its session identity, so two closes write two files. [INV-302, INV-117]
17. A session handover *shall* say what stays open, what resumes where, and every decision the person made with its timestamp. [INV-302]
18. The system *shall* keep the person's own words out of a handover, quoting them only as a decision entry's evidence. [INV-302]
19. A session handover *shall* name the transcript it was read from, the extract file, and the agent that wrote it. [INV-302]

**Case: the opening step**

20. *when* a session opens, the system *shall* have a fresh agent read the previous session's handover and its extract. [INV-302]
21. The system *shall* have that agent take the extract the previous handover names. [INV-302]
22. *if* no such extract stands, *then* the system *shall* re-derive one from the previous session's transcript. [INV-302]
23. That agent *shall* list every decision the person made, each with its timestamp. [INV-302]
24. The system *shall* compare that list against `DECISIONS.md` and `NEXT_STEPS.md`. [INV-302]
25. *if* a decision is missing from both, *then* the system *shall* report it to the seat before work starts. [INV-302]
26. The system *shall* keep this step a discipline the seat holds, since a session's opening writes no committed artifact. [INV-302, INV-247]

**Case: which transcript a run reads, and where the extract lands**

27. The system *shall* take a session identity from the caller and *shall* read the transcript file named for that identity. [INV-302, INV-117]
28. *when* a session closes, the system *shall* name its own session identity to the extractor, and that identity *shall* come from the session's checkpoint. [INV-302, INV-117]
29. *if* the named identity matches no transcript, or matches more than one, *then* the system *shall* write no extract and *shall* refuse the run. [INV-302, INV-218]
30. A refusal of that kind *shall* name the identity it was given and every transcript it matched. [INV-302, INV-218]
31. *while* no identity is named, the system *shall* read the most recently written transcript it takes and *shall* say how many it chose among. [INV-302]
32. The system *shall* refuse an output path that lands inside the repository, and the refusal *shall* name that path and the reason. [INV-302, INV-218]
33. The system *shall* resolve an output path before judging it, so a relative path, a link, and `..` are judged by where they land. [INV-302]

---

## Requirement 128: A background worker outlives a memory wipe

**Context:** A worker spawned in a session keeps running and keeps writing the shared tree after the chat's memory is cleared. The operating system's process list and the harness task record show nothing for it, so neither is proof of death; liveness is proven by deed. The handoff note records the worker's id, the files its brief lets it write, and three checks a resuming session runs before touching those files.

**User Story:** As a resuming session, I want a background worker proven dead or alive by three checks before I touch its files, so that a live writer is reconnected and a dead one's files are freed with nothing scrambled.

### Acceptance Criteria

**Case: the handoff note records three things**

1. The system *shall* have the handoff note record the worker's recorded id pointing at its checkpoint file, the exact files its brief lets it write, and the three liveness checks. [INV-76, ACT-3]
2. The system *shall* run the three checks before touching the write-set: watching the write-set's file times over a short window, reading the worker's heartbeat on its checkpoint file, and sending one message to the recorded id. [INV-76]

**Case: the verdict**

3. *when* any one check shows life, the system *shall* reconnect and treat the worker's files as claimed, and *shall* declare a dead verdict only when all three are quiet together — a still write-set, a stale heartbeat, and an unanswered probe — in one written line. [INV-76]
4. *while* no dead verdict stands, the system *shall* never frame the worker's output as finished and *shall* spawn no second worker onto the shared tree until the first is halted by its own reply or declared dead by all three checks. [INV-76, INV-11]
5. The system *shall* have a dead verdict free only the files the worker owned, reading whether the work is done from the worker's checkpoint finished marker or the verify walk. [INV-76]

---

## Requirement 130: The milestone gate re-proves and audits the whole

**Context:** A milestone runs the full gate over the accumulated landings before they are called a release. It re-proves the spec and the architecture, runs the design review, walks the matrix and surface-composition audits, re-runs the skill evals and the skill-creator craft review, compacts the documents and the code, and closes with a sweep of open gates, deferred rows, the formal index, the derived headers, and the thin loader.

**User Story:** As a person cutting a release, I want the milestone gate to re-prove and audit the whole as one pass, so that an accumulation of small landings is re-checked before it ships.

### Acceptance Criteria

**Case: the two re-proves and the design review**

1. *when* a milestone is reached, the system *shall* re-prove the spec in full and re-prove the architecture beside it, the prover reading the architecture the way it reads the spec and recording the architecture pass in `docs/prover/` beside the spec's. [M-1, INV-116]
2. The system *shall* run the design review on the re-proven spec in full: the whole element inventory, every proposed same-kind grouping, and behaviour parity within each. [M-1, INV-141, INV-154]
   - the review also covers the likely divergences, echoed as three asks or fewer;
   - the outcome is folded into a dated design-review record;
   - a confirmed grouping re-enters the prove step under the round cap;
   - a confirmed grouping typically rests at the gate, waiting for the human's answer.

**Case: the audits and the eval runs**

3. The system *shall* re-walk the coverage validation against the current spec and architecture, run the surface-composition check (the audit that opens each covering overlay and confirms interactive controls from different layers keep separate pressable space on one screen), and re-run the skill evals. [M-1, E-15, E-19]
4. The system *shall* walk the pack's skills through the skill-creator to review each skill file's craft, folding or rejecting each finding with a written reason in a dated record, a newly joining skill walking this at birth before it reaches the gate. [M-1]

**Case: the compaction stations**

5. The system *shall* audit every living document — spec, matrix, queue, skills, ledger, and the test suite — for redundant information and compact it. [M-1, INV-115, E-24, INV-109]
   - compaction removes only the redundancy, leaving a fact living once in one home with a pointer from everywhere else;
   - it keeps anything whose removal would change the meaning;
   - it accounts for each removal that takes substance.
6. The system *shall* widen the compaction station to code, merging duplicate logic and removing dead weight with its listing. It *shall* extract a ripened abstraction only through the three-question fitness gate. [M-1, INV-123, INV-122, INV-39, INV-56]
   - the second occurrence of one problem opens its own compaction row;
   - it lands through the ordinary pipeline at one row's delta per commit, without blocking its lane.
7. The system *shall* restructure a document only to make it read faster, and only by moving text without changing a word. It *shall* also verify that the queue's body carries no closed row. [M-1, INV-111, INV-1, INV-276]
   - the restructure is proven by comparing the document before and after: both texts carry the same words and the same punctuation marks in the same counts;
   - each closed row was archived in its own closing commit.

**Case: the closing sweep**

8. The system *shall* re-list every open human gate and every unharvested inbox file, one line each. [M-1, INV-1]
   - sweeps the deferred rows' revisit triggers once more, sending any fired row back to runnable;
   - re-checks the formal index against the prose as a derived map;
   - the formal index is the spec's closing reference table, pairing each code with its rule's one-sentence statement.
9. The system *shall* re-pin the derived docs' headers to the spec version and prove them, and *shall* re-read the thin loader line by line. [M-1, E-16]
   - it keeps only what must hold before any pack file loads, migrating any other line to its real home;
   - the audit report states the line count.

---

## Requirement 131: A periodic full audit catches the drift no lint names

**Context:** Two layers guard the living documents against rot. The continuous lints run on every push and hold each known drift class the moment it reappears. Beside them, a full audit runs on a landing-count cadence — every ten landings since the last full audit — running the milestone gate's whole-read even where no milestone falls due, so an unknown drift class caught between milestones is found by a fresh whole-read. The whole-read takes the adversarial stance the verify audit defines.

**User Story:** As a person guarding against slow rot, I want a full adversarial audit on a landing cadence, so that a drift class no lint yet names is caught before a human reads it late.

### Acceptance Criteria

**Case: the cadence and its whole-read**

1. *when* ten landings have passed since the last full audit, the system *shall* run the milestone gate's whole-read — the full spec and architecture re-prove, the design review, and the doc-compaction sweep — even where no milestone falls due, the count being a host-settable default. [INV-145, INV-70, INV-116, INV-141, INV-115]
2. The system *shall* read the count from the landing history and *shall* reset the counter at a milestone gate, since the gate already runs the whole-read. [INV-145, INV-107]

**Case: the adversarial stance**

3. The system *shall* take the audit's whole-read as a read set on breaking the work, refuting its claims and finding its holes, the same stance as the verify audit. [INV-145, INV-46]

---

## Requirement 132: Compaction is continuous, a gate on every push

**Context:** The doc- and code-compaction stations run at every push, above the milestone that once held them alone. Every push is held to the reached-clean floor by a mechanical gate, so no bloat accumulates between milestones. The general clause that once stood here — any quality a machine can verify becomes a blocking gate — is removed. A check no longer follows from the property being checkable; it is opened where a standing rule breaks a second time, or where the owner asks for it.

**User Story:** As a person guarding against bloat, I want the clean floor held by a gate on every push, so that no bloat accumulates between the milestone whole-reads.

### Acceptance Criteria

**Case: the reached-clean floor at every push**

1. *when* a push runs, the system *shall* hold it to the reached-clean floor: the register lint at zero errors, the redundancy gate at zero open pairs, and the debt cap ratcheting down only, each asserted against the live document. [INV-164, INV-83, INV-98]
2. The system *shall* run the milestone whole-read above the gate as the deep periodic audit, so the two stations layer rather than duplicate. [INV-164]

**Case: a check is not born from checkability**

3. The system *shall* mint no gate from the sole fact that a quality is machine-verifiable, and *shall* open a new check only *where* a standing rule has broken a second time or the owner has asked for it. [INV-164, INV-108]

---

## Requirement 133: The style lint has two tiers

**Context:** The style gate's rules divide by whom they bind. The universal tier states the plainness and normative-informative separation every live-spec document holds, so it binds every host's gate. The pack-register tier is the pack's own reference-documentation taste, right for the pack's docs and available to a host for its own. The lint names the tiers in one flag.

**User Story:** As a host adopting the gate, I want the universal language laws as my floor and the pack-register taste optional, so that I adopt the plainness laws while keeping an intentional voice.

### Acceptance Criteria

**Case: the two tiers**

1. The system *shall* bind the universal tier to every host's gate whatever its register: the contrast-frame ban, the negation-opener rule, the machine-jargon rule, and the provenance-narrative rule. [INV-166]
   - the contrast-frame ban bars naming a thing by denying its neighbour, the `"X, not Y"` frame;
   - the negation-opener rule bars opening a rule by saying what it is not before saying what it is;
   - the machine-jargon rule bars insider pack jargon and coined terms from spec prose;
   - the provenance-narrative rule bars a birth-story — the date and case that motivated a rule — inside the normative body, and runs as a hard error in every tier.
2. The system *shall* keep the pack-register tier — the caps-shout, second-person, reassurance, and future-narration rules — as the pack's own taste, right for the pack's docs and available to a host on its word. [INV-166]

**Case: the tiers named in one flag**

3. The system *shall* run the universal tier as the gate and leave the register tier advisory under one flag, and run the union under the other, declaring the split in `docs/spec-style.md` rather than inferring it, this being the pack-to-host split applied to language. [INV-166, INV-173, INV-163]

---

## Requirement 134: Enumerable facts earn bullet structure

**Context:** A prose paragraph that carries an enumeration of three or more distinct, parallel facts earns bullet or numbered structure, so a reader scans the members instead of parsing them out of a run-on sentence. Prose stays for the laws, their reasoning, and their boundaries. The rule earns no mechanical lint of its own, since a regex flagging every three-comma sentence would trip on a rhetorical triad; telling a list-owed enumeration from a triad is a meaning call the register judge and the prover make.

**User Story:** As a reader meeting a packed paragraph, I want three or more parallel facts rendered as a list, so that I scan the members rather than parse them out of a run-on sentence.

### Acceptance Criteria

**Case: the threshold and its home**

1. *when* a paragraph carries three or more distinct, parallel facts, the system *shall* render the enumeration as a bulleted or numbered list, keeping prose for the laws, their reasoning, and their boundaries. [INV-215]
2. The system *shall* leave the rule read by eye and by the prover's cognitive-load lens, earning no mechanical lint of its own, the register judge and the prover making the meaning call a regex cannot. [INV-215, INV-203]

---

## Requirement 135: Grading the size of a change is the reader's act

**Context:** A text states what changed and what follows from it; the size of a change is given as content or a number, and grading that size — its importance or drama, up or down — belongs to the reader. Over-dramatization to the plus and to the minus are one bias, so the law covers both poles at once. It binds every text — chat, docs, worker reports, and agent-to-agent messages.

**User Story:** As a person reading the pack's texts, I want the size of a change left for me to judge on every surface, so that a change is described plainly and at its true size.

### Acceptance Criteria

**Case: both poles, every surface**

1. The system *shall* state what changed and what follows, giving the size as content or a number, and *shall* leave grading that size — to the plus or to the minus — to the reader. [INV-221]
2. The system *shall* bind this law across every text — chat, docs, worker reports, and agent-to-agent messages — and *shall* describe a correction as a correction. [INV-221, INV-183]

**Case: the nets it rests on**

3. The system *shall* have the register judge read this class on the chat and document surfaces, and *shall* carry the law in the worker brief for the surface the judge does not read. [INV-221, INV-203, INV-173]
   - the register judge runs the regex pattern files as the cheap first pass ahead of the model judge, and those files are the universal list plus any host's own overlay;
   - the worker brief carries the law because chat and agent-to-agent text are emitted before any gate reads them.

---

## Requirement 136: Documents are versioned, and each version has one home

**Context:** The queue and the spec carry dated versions the way code does, so a reader can tell which roadmap version a decision was made under. Each version fact has one named home: the repository's `VERSION` file, a skill's `SKILL.md` frontmatter line, and a host's installed-set record. The freshness check compares version against version rather than bare file times.

**User Story:** As a reader tracking versions, I want documents versioned and each version fact homed in one place, so that the freshness check compares exact version strings and every reader knows where the current version lives.

### Acceptance Criteria

**Case: documents carry versions**

1. The system *shall* carry a dated version on the queue and the spec the way code does, so a reader can tell which roadmap version a decision was made under. [M-3]

**Case: version has named homes**

2. The system *shall* keep each version fact in one named home — the repository's `VERSION` file, each skill's `SKILL.md` frontmatter line, and a host's installed-set record written at attach and every update. [M-7]
3. The system *shall* have the freshness check compare version against version as exact strings, reading the stamped version itself. [M-7, A-7]

---

## Requirement 137: Time is read off the clock, never invented

**Context:** Every date a session writes — a file name, a journal or queue stamp, a ledger occurrence — comes from the machine's clock at write time, and git is the arbiter in doubt. The rule takes four forms, two mechanical and two about the chat surface.

**User Story:** As a person reading the records, I want every date read off the clock at write time, so that no record carries an invented or extrapolated date.

### Acceptance Criteria

**Case: the two mechanical fences**

1. *when* a repo file name, journal heading, or ledger date is written, the system *shall* keep it no later than the current clock, turning a future-dated stamp red as a real defect while a prose quote of a past incident's date stays legal. [INV-24]
2. *when* a commit adds a line pairing today's date with a clock time later than the commit moment, the system *shall* red it, reading the adjacent stamp shape against the commit clock so a legally quoted time stays green. [INV-24]

**Case: the chat surface**

3. The system *shall* read a human-facing timestamp off the clock at write time rather than continue it from an earlier stamp, this law living in the communicator skill. [INV-24]
4. The system *shall* inject the wall clock into every prompt's context through the harness hook where it is installed, the law above standing alone where the hook is not. [INV-24]

---

## Requirement 138: The push checks may be mirrored in a remote gate

**Context:** The guardrails' native home is the local pre-push hook. A host may also mirror the same checks in its continuous-integration runner as a second net. There is one source of truth: the runner runs the same scripts and never redefines them, and the second net runs the full set, wider than the local reach map's scoped subset.

**User Story:** As a host wanting a second net, I want the remote gate to run the same scripts as the local hook, so that the gates are re-run on another machine with one source of truth.

### Acceptance Criteria

**Case: one source of truth, the full set**

1. *when* a host mirrors the checks, the system *shall* run the same scripts in the remote gate and *shall* never redefine them, the local reach map staying a latency optimization and never a shortcut for the remote gate. [M-5]
2. The system *shall* have the remote gate run the full check set as the second net. [M-5]

---

## Requirement 139: Accepted work reaches the project's remote

**Context:** Where the host has a remote, work is pushed by rule, released as soon as it is same or better. Same or better means the work matches or improves on the tree before the change; the gates its diff reached hold that reading, each one green and none showing a regression against that prior tree. The remote is discovered from the tree first. The rule runs inside the human's standing push grant, stands down while another session is live in the repo, and re-walks the shopfront on every push.

**User Story:** As a person shipping accepted work, I want green work pushed by rule under the standing grant, so that sound work reaches the remote rather than sitting local and a named milestone still waits for the human's word.

### Acceptance Criteria

**Case: push by rule under the grant**

1. *when* work matches or improves on the tree before the change, and every gate its diff reached passes green with no regression against that prior tree, the system *shall* push it to the host's remote by rule under the human's standing push grant rather than park it locally. [INV-82, INV-70, INV-9]
2. The system *shall* discover the remote from the tree first rather than ask what `git remote -v` answers, and *shall* ask one contextual question at the first push moment only where the host has no remote or the profile records no push grant, one question per gap. [INV-82]

**Case: coordination and the shopfront**

3. *while* another session is known live in the repo, the system *shall* stand the by-rule push down and return push coordination to the human, the accepted work waiting local until the repo is single-session again. [INV-82, INV-11]
4. *when* a push reaches the remote, the system *shall* re-walk the README against the pushed truth and *shall* still wait for the human's word on a milestone gate he named in person. [INV-82, INV-44]

---

## Requirement 140: The push walk reads the remote gate's verdict

**Context:** A push does not end at the push. Where the host mirrors its checks in a remote gate, the push step reads the remote gate's own verdict — the run the push triggered — with one command in minutes and no human wait. A red verdict is the pushing session's own immediate bug.

**User Story:** As a person who just pushed, I want the session to read the remote gate's verdict and fix a red the same session, so that the human never meets a failed run first in a mailbox.

### Acceptance Criteria

**Case: the verdict is read**

1. *when* a push triggers a remote gate, the system *shall* read the gate's verdict with one `gh run` in minutes, watching a slow gate to its verdict on the detached-work cadence. [INV-106, INV-35]
2. *when* the remote verdict is red, the system *shall* treat it as the session's own immediate bug, preempting by the bug lane, fixing it the same session, and re-pushing before anything else, so the human never learns of the red from a mailbox. [INV-106, INV-2]

---

## Requirement 141: The push gate for the flagship runs a fresh re-check

**Context:** The pack's own repository is public and the method's flagship, so every push is preceded in the same session by the concurrent-edit fence and a fresh prover re-check over the spec and the architecture, its record landing before the push. That record is also the adversarial read of the change the push sends. A change can pass every test and still be wrong in ways no test asks about. A reviewer briefed to refuse a change reads it differently from one set on confirming it. Both readings are one pass over one change, so one record carries them. One carve-out is scoped by the diff.

**User Story:** As a maintainer pushing the flagship, I want the fence and one review record per push, so that nothing reaches the remote unreviewed.

### Acceptance Criteria

**Case: the two preceding steps**

1. *when* a push runs on the flagship repository, the system *shall* run the concurrent-edit fence and a fresh prover pass over the spec and the architecture, landing the record in `docs/prover/` before the push. [M-6, INV-11, INV-116]
   - a record predating the last architecture change is as stale as one predating the last spec change.
2. The system *shall* fold defect findings before pushing, a fold produced by the gate's own pass shipping with the same record and a fold that edits beyond the sections its own finding named re-triggering the gate, the rest becoming queue rows. [M-6]

**Case: the inbox-only carve-out**

3. *when* a push's diff is exactly one new file under `inbox/`, the system *shall* owe the fence and no re-check record, a diff carrying anything more riding the full gate. [M-6, INV-112]
4. The system *shall* name the record `YYYY-MM-DD[-suffix].md` with the suffix mandatory when the date's file exists, and *shall* treat no re-check record for the pushed state as a push that should not have happened. [M-6]

**Case: the one record is also the adversarial read of the delta**

5. The system *shall* require one review record per push and no second one. [INV-304, INV-156]
   - the reviewer is briefed to find reasons the change should be refused;
   - the reviewer holds the change defective until it has evidence otherwise;
   - a review set on confirming the change leaves this requirement unmet.
6. The delta *shall* be every commit between the remote's head and the local head, read with the work still uncommitted. [INV-304, INV-116]
   - the range resolves by the ladder INV-208 states.
7. The record *shall* name the commits it covers, the files it read, the checks it ran, and its findings. [INV-304]
   - a review that found nothing states there what it examined, so the absence rests on coverage rather than on silence.

**Case: a record covering another range covers nothing**

8. *if* a record names a range other than the pushed one, *then* the system *shall* read that record as covering nothing. [INV-304]
9. *when* the newest record stands older than the newest commit in the pushed range, the system *shall* red and name both commits. [INV-304, INV-116]
   - a commit carrying the record alone is exempt from the naming rule, since a record cannot name the commit that first ships it.

**Case: a blocking finding holds the push, and the judgment the check leaves alone**

10. *while* a blocking finding on the record stands open, the system *shall* hold the push. [INV-304]
11. *when* the finding is closed, or the record states why it stands, the system *shall* let the push through. [INV-304]
12. The check *shall* hold the record's presence, its commit, its freshness, its named range, and its fields. [INV-304]
13. The check *shall* leave to the reviewer the judgment of whether the review was adversarial. [INV-304]
    - no script decides whether a reviewer set out to refuse the change;
    - no script decides whether the files the record names were read;
    - the record's named commits, files, checks and findings are the pressure a machine can apply.

---

## Requirement 142: Process bookkeeping scales to the delta

**Context:** A tiny row pays the same fixed bookkeeping as a whole surface — its claim commit, its full-page re-check record, its journal chapter, and a resume rewrite — running a large share of its wall time. The re-check keeps its rigor always but scales its form, and the irreducible core stays fixed regardless of scale.

**User Story:** As a person landing a small change, I want the bookkeeping's form scaled to the delta while its rigor holds, so that a tiny row runs short without sacrificing the safety core.

### Acceptance Criteria

**Case: the re-check scales its form**

1. *when* a delta is a skill, prose, or infra kind with no new surface and no structure change, the system *shall* ship a short-form re-check record of three lines — previous records clean, the delta in one line, and the verdict. [INV-61, INV-45]
2. *when* a delta is surface-sized or structural, the system *shall* keep the full re-check walk. [INV-61]

**Case: the irreducible core**

3. The system *shall* batch claims per declared lane in one commit and take the journal chapter and resume rewrite once per landing batch rather than per tiny row. [INV-61]
4. The system *shall* keep the irreducible core fixed regardless of scale — the law's own text written well, the red-first test, the delta's cross-link prove, and the gates. [INV-61]

---

## Requirement 305: A push carries an adversarial review of the change it sends — merged into Requirement 141

**Context:** This requirement and the push gate's own re-check asked one push for two review records, written into two homes and read by two checks, over one and the same change. Both are one adversarial pass over one delta, so they are now one record: Requirement 141 carries the whole duty, and the record lives with every other review record under `docs/prover/`. The merge is recorded in DECISIONS.md. The adversarial read itself is untouched — only the second record and the second check are gone.

**User Story:** As a maintainer preparing a push, I want one review record instead of two, so that the read survives at half the writing.

### Acceptance Criteria

**Case: merged**

1. The system *shall* carry this requirement's duty in Requirement 141 alone, the check that once held it resting at `attic/check-push-review.sh`. [INV-304]
   - putting that check back into the push chain takes a decision of its own.

---

