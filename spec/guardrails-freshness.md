## Requirement 168: The version-control gate runs before the first delivery

**Context:** Every host reaches its first delivery through the same gate, and both a fresh start and an attach run it in the same order. A gate cannot protect files older than itself, so the gate runs before anything is created or moved. The gate settles two things: that git exists, and that a remote either exists or is declined on the record.

**User Story:** As a person starting or attaching a host, I want the version-control gate settled before the first delivery, so that no work is committed somewhere it cannot be recovered or tracked.

### Acceptance Criteria

**Case: git exists first**

1. *when* founding or adoption begins, the system *shall* run the version-control gate before it creates or moves any file. [INV-8, A-0, A-5]
2. *if* the host has no git, *then* the system *shall* initialize git and make a pristine baseline commit that doubles as the diff baseline. [A-5]

**Case: the remote is settled on the record**

3. Before the first delivery, the system *shall* settle the remote as a named deliverable: a remote exists, or the human has declined one, and the host's journal records which. [INV-8]
4. A recommendation of a remote *shall* not close the gate; the gate closes only on an existing remote or the human's recorded decline. [INV-8]

**Case: never deliver into an unversioned host**

5. The system *shall* refuse to deliver into a host that lacks version control. [INV-8]

---

## Requirement 188: How the skills arrive and how a machine learns a newer pack exists

**Context:** The pack ships one installer that copies its skills onto a machine and backs up any existing copy first. A separate daily check tells a machine when the public repo has moved past what it runs. The check proposes; the human's word installs.

**User Story:** As a person running the pack on a machine, I want the installer to add skills without losing an existing setup and the daily check to tell me when a newer pack ships, so that updating stays my own step. [E-21, E-25]

### Acceptance Criteria

**Case: the installer**

1. *when* the installer runs, the system *shall* copy every pack skill into the agent's skills home (`~/.claude/skills/`). [E-21]
2. The installer *shall* be idempotent: it *shall* back up an existing copy with a timestamp before overwriting and *shall* delete nothing. [E-21]
3. The installer *shall* place the backup in an attic folder beside the skills home rather than inside it, so the agent never scans a stale copy as a live skill. [E-21]
4. The installer *shall* write to `.live-spec/` exactly what adoption's record clause writes. [E-21, A-7]

**Case: the daily update check**

5. *when* the day's first freshness point is reached, the update check *shall* run once, throttled by a dated stamp in the machine's pack home, and *shall* ask the public repo's VERSION file on main whether the pack has moved past the installed version. The update check *shall* be the outward twin of the dev-machine skill sync, which keeps the machine's copies true to the local repo. [E-25, M-7, E-23]
6. *if* the remote is newer, *then* the update check *shall* propose in the session's chat, naming both versions, pointing to what changed, and naming the install road; it *shall* install nothing. [E-25, ACT-1]
7. *if* there is no network or the answer is unreadable, *then* the update check *shall* report one honest skip line naming the address it tried, *shall* leave the stamp unwritten so the next session retries, and *shall* neither block nor guess. [E-25]
8. *if* the machine is ahead of the public repo, *then* the update check *shall* read as up to date and *shall* propose no downgrade. [E-25]
9. The update check's only surface *shall* be the proposal line, governed by the plain-language register. [INV-28]

**Case: the check reads vendored pins and never-answered questions**

10. *when* the update check sees the pack moved past the pin in the ratchet manifest, the system *shall* propose the re-install and name the vendored files whose content differs from the local pack's current copies, naming each stale key's own re-install road. [INV-177, INV-172]
11. *when* a host carries no ratchet manifest, the system *shall* give it the plain version proposal unchanged. [INV-177]
12. *when* the update check runs, its founding arm *shall* read the host's recorded `founding.set-version` against the current set and name each founding question the host has never answered, beside the vendored-file report. [INV-227]
13. *if* a host has no readable `founding.set-version`, *then* the founding arm *shall* name every founding question as potentially owed. [INV-227, INV-91]
14. The system *shall* surface a never-answered founding question for the owner to answer at catch-up, *shall* answer none on the host's behalf, since the duty binds forward, and *shall* home the recorded set version in the host profile and the agent card among the questions. [INV-227, INV-159, E-16, E-32, INV-184]

## Requirement 222: A behavioural rule that breaks twice earns a live channel

**Context:** A standing behavioural rule keeps its normative home in a once-read file — the loader, a profile, a skill's text. Prose in a once-read file loses to mid-turn momentum, and attention alone holds nothing across sessions. So a rule that breaks mid-turn a second time despite that home earns a live channel at that same moment, and the pick is recorded where the rule lives.

**User Story:** As a person whose standing rule the pack keeps breaking, I want the second mid-turn break to earn a live channel, so that a recurring failure gets a mechanism at once, before a third suffering.

### Acceptance Criteria

**Case: the second break earns a channel**

1. *when* a standing behavioural rule breaks mid-turn a second time despite its once-read home, the system *shall* give it a live channel that same moment — an every-prompt hook line reminding at the decision point, or a mechanical after-the-fact check that turns the suite red. [INV-108]
2. *when* a live channel is chosen, the system *shall* record the pick where the rule lives and *shall* keep the once-read file as the rule's normative home. [INV-108]

**Case: the break-record lives in one home**

3. The system *shall* record a rule's mid-turn breaks in one home, the problem ledger (`PROBLEMS.md`), so the sweep reads one source. [INV-108]
4. *when* a live channel lands, the system *shall* point it back to that ledger entry rather than standing it as a second break-record. [INV-108]

---

## Requirement 225: The guardrails wired to the push gate

**Context:** The guardrails are mechanical checks wired to the pre-push hook, running live for the pack's own repository. Each push must show a set of proofs before it reaches the remote. On a host these checks are offered for the human to accept, since the human may not know what a git hook is.

**User Story:** As a maintainer pushing the pack, I want each push to show its proofs mechanically before it reaches the remote, so that a structural defect turns the push red rather than landing on the remote.

### Acceptance Criteria

**Case: what each push must show**

1. *when* a push runs, the system *shall* require a prover record dated the same day, a green suite scoped to the diff's reach, every anchor owned by one node, and no unchecked matrix-coverage box. [E-6, INV-41]
2. *when* a push runs, the system *shall* require the prototype fence — no production file referencing into a prototype home — and the opt-in concurrent-edit fence on commit. [E-17, INV-17]

**Case: hosts are offered, never imposed**

3. *when* the checks reach a host, the system *shall* install the hooks only where the host uses git and only after asking the human in plain words. [E-6]

---

## Requirement 226: The push gate derives its reach from the diff

**Context:** Running every check before every push double-misses: a prose-only push pays for behavioural tests that read none of its changed lines, while the checks a prose diff can break never run. So the push gate derives its check-set from a declared reach map — which checks read which file classes — read mechanically from the diff's file list. The map is conservative: anything it cannot classify falls to the full run.

**User Story:** As a maintainer pushing a change, I want the gate to run every check the diff can reach and only those, so that a prose push stands down the behavioural suite by name while an unclassified file still pulls the whole run.

### Acceptance Criteria

**Case: the reach map decides the set**

1. *when* a push runs, the system *shall* derive its check-set from the declared reach map against the diff's file list, and *shall* run the full suite *if* any changed file is unmapped or new. [INV-45, INV-40]
2. *when* a diff is confined to the declared infra classes, the system *shall* run the test files that read its changed files plus the traceability net, and *shall* log the picked set with its reason. [INV-45, INV-212, INV-18]
   - the traceability net is the suite's own traceability tests, carrying the anchor-ownership assertion and riding every scoped run, a mechanism distinct from the feature-coverage check;
   - the system *shall* curate the infra-class list by incident and re-justify it at milestones.
3. *when* a full run completes, the system *shall* read its own wall-time against the architecture's stated number and red on an overrun naming both figures. [INV-41, INV-164]

**Case: the classes are the host's to declare**

4. The system *shall* read the reach map's directory classes from `guardrails.config.json` under a `reach_classes` key, the same layers the host's `project.layers` already carries. [INV-224, INV-135]
5. *if* the config names no classes, *then* the system *shall* leave every changed file unclassified and run the full suite on every push. [INV-224]

**Case: the cheap gates never scope**

6. The system *shall* run the prover-record, ownership, coverage, loadability, and prototype-fence checks at every push that carries content, except a deletion-only push (criterion 7); an inbox-deposit push under inbox/; a push in the owner's recordless class — docs/prover/, docs/skill-review/, docs/language-reads/; or a push whose entire diff is only a change in letter case, in whitespace, or both — the case-or-space carve-out. [INV-40]

**Case: a deletion-only push carries no content**

7. *when* every ref-update line git feeds the pre-push hook carries the all-zero local object id, the system *shall* read the push as deletion-only and *shall* stand the whole gate chain down. [INV-290]
8. *when* the chain stands down for a deletion-only push, the system *shall* print one line naming the stand-down and its reason, deriving no reach and running no suite. [INV-290]
9. *when* at least one fed line carries a real object id, the system *shall* run the push gate exactly as on any other push, never reading a mixed push as deletion-only. [INV-290]
10. *if* the hook reads no ref-update lines, *then* the system *shall* run the whole gate chain as an ordinary push, since an unreadable input names no deletion to stand down for. [INV-290]

---

## Requirement 227: A blocking gate speaks one typed language

**Context:** Today each gate script fails in its own words, so an agent parses prose and a human hunts for the fix. Every blocking gate instead emits, on red, one parseable failure object beside its human-readable lines, and every check declares itself blocking or advisory.

**User Story:** As an agent or a person reading a red gate, I want each blocking gate to emit one typed failure line carrying the fix, so that the reason and the remedy are read the same way from every gate.

### Acceptance Criteria

**Case: the typed failure line**

1. *when* a blocking gate reds, the system *shall* emit one typed failure object carrying a severity, a code, a message, and a fix field that reads as the sentence a person follows. [INV-47]
2. The system *shall* have every check declare itself blocking or advisory, an advisory check printing its finding and never flipping the exit code. [INV-47]

**Case: no half-written artifact**

3. *when* a script rebuilds artifacts, the system *shall* validate every output before it writes any, so no half-written artifact lands on disk. [INV-47]

---

## Requirement 228: The four project-side checks are attachable code

**Context:** The pack ships a generic runnable form of the four checks the pipeline names — completeness, tests-present, behaviour-traces-to-spec, and conflicts — parametrized by one host config file, attached without editing check code. A host attaches them by config, and each check proves itself red-first on one planted defect before it counts as attached.

**User Story:** As a person attaching the pack to a host, I want the four project-side checks configured rather than re-implemented, so that a host wires them by naming its own shape and each check proves it can fire.

### Acceptance Criteria

**Case: the checks attach by config**

1. The system *shall* ship the four checks — completeness, tests-present, behaviour-traces-to-spec, and conflicts — under `scaffold/guardrails/` parametrized by one host config declaring the document paths, the tests directory, the source globs, the registry path, and the render command. [INV-97]
   [GAP: the source names the conflicts check as one of the four but never states what conflict it detects; the other three carry their subject in their own names.]
2. *when* a check runs, the system *shall* read the config and the tree, exit green or red, and on red emit the typed failure line beside its human sentence. [INV-97, INV-47]

**Case: failure is honest by construction**

3. *if* the config is missing, *then* the system *shall* red with an attach-me line rather than pass silently, and *shall* red *if* the config points at a path that does not exist. [INV-97]
4. *if* a host lacks a check's precondition, *then* the system *shall* require the waiver declared in the config where a reader sees it, so an undeclared gap never passes quietly. [INV-97]

**Case: attachment proves itself**

5. *when* the attach command runs, the system *shall* vendor the four checks, seed the config where the host carries none, leave a filled config unclobbered, and *shall* write the host's source pins into the ratchet manifest so the daily update check covers this kit. [INV-97, INV-177]
6. *when* a check is attached, the system *shall* prove it red-first on one planted defect before it counts as attached, the registry's own content staying the host's authorship. [INV-97, E-10]

---

## Requirement 229: The net-liveness meter reads every net

**Context:** A net that never fires is a fact about itself with two readings: the defect is gone and the net is dead weight, or the net is broken and its trigger sits where the work never passes. Two numbers tell those apart — how often the net ran and how often it fired — and no net keeps them on its own. The meter records both against the host's declared roster of nets and reads them back.

**User Story:** As a person maintaining a set of nets, I want each net's runs and fires recorded and read against a declared roster, so that a broken trigger is named while a merely quiet net is surfaced for a human retirement call, the trust-or-retire decision left to the human.

### Acceptance Criteria

**Case: the two numbers are recorded**

1. *when* a net runs, the system *shall* record one line per invocation to `.live-spec/net-meter.jsonl`, and *shall* aggregate runs and fires against the host's declared roster of nets. [INV-202]

**Case: the three readings**

2. *when* a net's recorded run count is zero, the system *shall* red it by name as a broken trigger, since its condition sits where the work never passes. [INV-202]
3. *when* a net's runs reach its declared window with zero fires, the system *shall* surface it as a retirement candidate and *shall* leave the retirement as the human's call. [INV-202]
   [GAP: the source names a per-net declared window for the zero-fires retirement reading but does not state who declares the window or its default value.]
4. The system *shall* read every other net as live, and *shall* never auto-retire a net nor red one for staying quiet. [INV-202]

---

## Requirement 230: The register judge reads a class a word-list cannot

**Context:** A register law that names a class cannot rest on a list of literal words, since each escape earns one more pattern while the next word walks through and a human ends up working as the regular expression. So a model that reads meaning holds the class. It takes the outgoing text and the law and returns the sentences that carry no information or leak register, with the literal pattern list demoted to a first cheap filter.

**User Story:** As a person reading the pack's own words, I want a model to hold the whole register class, so that a register offence is caught in meaning while a broken judge falls back to the cheap list and keeps working.

### Acceptance Criteria

**Case: the judge holds the class**

1. *when* the register law is applied, the system *shall* hand the outgoing text and the law to the cheapest model tier the routing rule names and take back the sentences that carry no information or leak register. [INV-203, INV-69]
2. The system *shall* keep the literal pattern list as a first cheap filter that earns no new entries by duty. [INV-203, INV-83]

**Case: the universal laws the judge reads**

3. The system *shall* read the universal laws that ship in the mechanism, the set `guardrails/language-rules.json` states and `hooks/language-laws.json` carries to the judge, and *shall* leave the personal laws to an overlay the personal layer owns. [INV-203, INV-221]

**Case: two surfaces, one mechanism**

4. *when* the seat finishes a turn on the chat surface, a Stop arm *shall* dispatch every message shown since the last human turn, and a prompt-submit arm *shall* report the verdict at the person's next message. [INV-203]
5. *when* a styled file is about to be shown, the same judge *shall* stand as the ceiling of the pre-show register gate pointed at that file. [INV-83, INV-203]
6. The contrast-frame scan, the hedge scan, the code-anchor scan, and the empty-validation scan *shall* each read every message shown since the last human turn through the shared full-turn reader, the reach the register judge's Stop arm carries. [INV-281, INV-203]

**Case: the judge stands down on its own breakage**

7. *if* the judge's own machinery breaks — a missing binary, a timeout, a non-zero exit, or a shape it cannot read — *then* the system *shall* leave the literal-list verdict standing rather than red, so a guard cannot train the guarded to route around it. [INV-203]
8. A scan reading through the shared full-turn reader *shall* stand down *where* the stop hook is already active, or the event payload or the turn's record cannot be read. [INV-281]

**Case: the host wires these arms itself**

9. The two arms and four scans above *shall* each bind *where* the host wired it, since each stood down from the pack's default wiring. [INV-203, INV-211]

---

## Requirement 231: The answer-first arm reds a lead-less wall — retired

**Context:** The Stop-hook proxy this requirement specified ran against real turns with zero catches, a mechanized gate that never once fired. Its retirement is recorded in DECISIONS.md. The answer-first law itself is untouched — it stands permanently in the personal profile and is still reminded at every prompt by the chat-law hook (Requirement 230); only this requirement's own mechanized proxy is gone.

**User Story:** As a person who read the silent runs of this proxy with nothing caught, I want the dead machinery retired rather than left running unread, so that the pack carries no gate that never fires.

### Acceptance Criteria

**Case: retired**

1. The system *shall* carry no Stop-hook arm implementing this proxy; its former file stands retired at `attic/answer-first-scan.py`, never re-armed without a fresh decision. [INV-220]

---

## Requirement 232: Two Stop-hook soft signals: the hedge gate and the lean-orchestrator arm

**Context:** Two once-read behavioural laws gained a mechanical net. The first: a reply that offers to do a thing the seat could already derive and reverse, holding the offer open for a cue, is an offering-hedge. The second: a session that holds raw file content inline without dispatching a worker leaks the seat's context. Each is a Stop-hook soft signal that reads after the fact and corrects one message later; each is honest that it catches only the frames it lists.

**User Story:** As a person relying on the seat to act rather than hedge and to delegate heavy reading, I want each law backed by a cheap literal net, so that a common hedge frame and a pure context-hoard are caught while the class in any phrasing stays with the conduct judge.

### Acceptance Criteria

**Case: the hedge gate**

1. *when* any message the seat showed since the last human turn carries an offering-hedge frame from the pattern list, the system *shall* block the stop with a rewrite instruction reaching the seat one message later. [INV-238, INV-173]
   - a quoted, backticked, or fenced span is stripped from the message before the pattern list is matched;
   - the scissors scan is the literal gate for the contrast-frame law (`guardrails/language-rules.json`, rule r10); this arm is modelled on it, matching against an inline universal pattern list and an optional personal-overlay file a host tunes, as the scissors scan carries one;
   - the setup walk places the gate's file and leaves the wiring to the host.
2. The system *shall* leave clear of a genuine taste, policy, or irreversible question that names its human-only fact, since that question is an honest admission the human owns. [INV-238, INV-152]
3. The system *shall* catch only the frames it lists, so a paraphrase it does not carry stays with the conduct judge that reads the class in meaning. [INV-238, INV-241]

**Case: the lean-orchestrator arm**

4. *when* cumulative inline raw file content across the session reaches the threshold and the worker-dispatch count is zero, the system *shall* warn that the reading rode no worker dispatch. [INV-246]
5. The system *shall* read the threshold as a tunable parameter defaulting to 50 kibibytes, and *shall* count only a main-thread Read or one of six literal file-dump verbs, a read inside a worker riding a sidechain never counted. [INV-246, INV-70]
6. *when* the seat dispatches its first worker, the system *shall* clear the warning, since one dispatch shows the session is delegating. [INV-246]

**Case: both stand down on their own breakage**

7. *if* a payload or transcript is unreadable, *then* the system *shall* stand the signal down silently, and *shall* have its runs and fires read by the net-liveness meter rather than trusted. [INV-203, INV-202]

**Case: the host wires this arm itself**

8. The hedge gate *shall* block no stop on a host that has not turned it on, which is the pack's default. [INV-238, INV-211]

---

## Requirement 233: The conduct judge reads the action trace

**Context:** The register judge reads what the seat said; the orchestration laws are about what the seat did — whether it dispatched a long artifact or a deep read to a worker, whether it routed each unit of work to the cheapest sufficient tier, whether it kept pulling unblocked work. No text arm can see an act. The conduct judge generalizes the register judge from the turn's text to the turn's action trace, reading it against the standing orchestration laws.

**User Story:** As a person relying on the orchestration laws that name no mechanical net, I want a model to read each turn's action trace against them, so that a missed act is named for a forward correction the same way a register offence is.

### Acceptance Criteria

**Case: the trace is read against the laws**

1. *when* the seat finishes a turn, the system *shall* read the turn's action trace against the standing orchestration laws and red a violation after the fact. [INV-241, INV-150]
2. The system *shall* render the trace to quotable text before the model reads it, so the reused hallucination guard — the check that each span a verdict quotes is found in the judged text itself — has spans to match. [INV-241, INV-203]
3. *if* a turn's trace is empty, *then* the system *shall* skip it, since a chat-only turn carries no act to judge. [INV-241]

**Case: the law body and its evidence**

4. The system *shall* judge the orchestration laws carrying a reminder history of two or more, and *shall* leave a law with a single occurrence as a reminder until it recurs. [INV-241, INV-108, INV-69, INV-137, INV-143]
   - worker-routing: each unit of work is routed to the cheapest tier its step and kind allow;
   - lean-orchestrator: heavy reading is dispatched to a worker, and none of it is held inline;
   - pull-unblocked-work: the session keeps pulling unblocked queue work instead of idling;
   - classify-the-subtask: a subtask is the person's or the seat's by what the subtask itself needs, never by the heading it sits under;
   - each break is recorded in the problem ledger (`PROBLEMS.md`), the home the break-record law names.
5. *when* the evidence is partial — an idle or a parked step the trace cannot fully show — the system *shall* red only on a clear case and *shall* lean on the net-liveness meter and the human review window. [INV-241, INV-202]

**Case: async, and off the deterministic gate**

6. *when* the verdict is collected, a Stop arm *shall* write it to a slot distinct from the register judge's, and a prompt-submit arm *shall* surface it at the person's next message as a forward-looking correction. [INV-241, INV-203]
7. The system *shall* keep the conduct judge outside the deterministic suite and push gate, opt-in per host and off by default, since it reads the transcript and rests on a model call. [INV-241]
8. The system *shall* read the per-person strictness as a parameter it does not own, taking a built-in default a host overrides by environment until the parameters registry ships. [INV-241]
   [GAP: the source names a built-in strictness default the conduct judge reads before the parameters registry ships but never states that default's value or how hard it reds a borderline act.]

---

## Requirement 234: A cleanup says what it ended

**Context:** Every process the pack ends is reported with what it was and why the run owned it — the process identifier, the process group, or the owned path that proves ownership — so an ending nobody expected is visible the moment it happens, ahead of any unexplained loss of the person's work. This is the minimum owed on a machine shared with someone who runs the same programs the pack does.

**User Story:** As a person sharing a machine with the pack, I want every process the pack ends to announce what it was and how the run owned it, so that an unexpected ending is seen at once, before it surfaces as lost work.

### Acceptance Criteria

**Case: the notice on every ending**

1. *when* a cleanup path ends a process, the system *shall* emit through the shared notice shape one line naming the identity ended, what it was, and the owned-via proof. [INV-204]
2. *if* a tracked cleanup path ends a process while emitting no notice, *then* the system *shall* red the gate that scans for it. [INV-204]

**Case: the notice ships ahead of the strict form**

3. The system *shall* ship this notice ahead of the stricter owned-identity check, so what the strict form would refuse is shown before the strict form starts refusing. [INV-204, INV-162]
4. *when* a cleanup is built through an indirection the patterns cannot read, the system *shall* leave the announcement to the forker. The muted-launch check keeps the same bound. [INV-204, INV-157]
   - the muted-launch check holds that every browser a test launches starts muted, and it reds an unmuted launch.

---

## Requirement 235: A finished worker leaves no runaway child, and teardown reaps its own group

**Context:** When a worker the run spawned completes, a descendant it left behind can keep burning a full processor core unnoticed while a frozen status line masks it. The run owns that descendant, since it sits in the run's own process group or under the run's own temp tree. One arm reports such a runaway; a second reaps the run's own process group at teardown; and a stalled worker is caught by its idle output. Because a coarse scope does real harm in process space, a target is identified only by provable ownership, never by a program name.

**User Story:** As a person whose machine the run shares, I want a finished run to report and reap only the descendants it provably owns, so that a runaway core-burn is caught without a broad sweep ever touching a foreign process.

### Acceptance Criteria

**Case: report a runaway the run owns**

1. *when* a stopping point is reached, the system *shall* report a descendant that is owned, orphaned, and burning — its identity, its processor share, and why the run owns it — reasoning over process group, parent liveness, and processor share alone, and *shall* fire this notice at the stopping point and never at the push gate, which runs long after the cores burn. [INV-213]
   [GAP: the source gates the burning test on a host-settable processor-share threshold but names no default, so the reporter's out-of-box firing point is unstated.]
2. The system *shall* read no command or name field for that verdict, so a process whose command merely matches a known burner in a foreign group is never targeted. [INV-213, INV-162]

**Case: teardown reaps the owned group**

3. *when* a worker tears down, the system *shall* reap the process group the run itself spawned through `os.killpg` and *shall* refuse any group absent from the run's owned set. [INV-230, INV-162]
4. *when* the group is reaped, the system *shall* report what it ended through the shared cleanup-notice shape. [INV-230, INV-204]

**Case: a stall caught by idle output**

5. *when* a worker's status reads running while its output file has stopped growing, the system *shall* read the stall from that file's modification time and return the stalled worker with its owned process group for confirmation before any reap. [INV-230, INV-76]
6. The system *shall* keep the worker's brief carrying the setting lines it needs, so a worker session onboards no one. [ACT-3]

---

## Requirement 242: A skill-body change carries the review it owes

**Context:** A skill is instructions a model reads, and a change to those instructions can shift how every session that loads it behaves. So a push that changes a skill's body must carry the skill-creator review that catches a regression before it ships. A pure version stamp is the one carve-out, since it copies the version fact rather than changing instructions.

**User Story:** As a maintainer changing a skill's body, I want the push blocked until it carries a fresh skill-creator review, so that a change to instructions every session reads cannot ship unreviewed while a bare version bump passes quiet.

### Acceptance Criteria

**Case: a body change owes a fresh review**

1. *when* a push substantively changes a skill under `skills/`, the system *shall* require a committed review naming the skill, carrying a verdict, and at least as new as the skill's last change. [INV-208]
2. The system *shall* read the push range through the base ladder the prover-record gate uses — the declared base (`LIVE_SPEC_DIFF_BASE`), then `origin/main`, then the previous commit (`HEAD~1`), the first that resolves. [INV-208, INV-116]

**Case: the version-stamp carve-out**

3. *if* a skill diff's only changed lines are the machine-stamped version and base-reference lines, *then* the system *shall* pass it quiet as owing no review. [INV-208, INV-178]
4. *if* a skill diff's only changed lines differ by letter case, whitespace, or both, *then* the system *shall* pass it quiet, owing no review. [INV-208]
5. *when* a substantive body change carries no fresh review, the system *shall* red, the review's judgment staying the skill-creator's own. [INV-208]

---

## Requirement 243: Append-only documents are rotated with nothing lost

**Context:** The pack's growable working documents grow with every delivery, and a guard's scan slows as they pass roughly half a megabyte. So a fully-closed portion of a growable document is rotated out of the live file into a dated archive, and the live file keeps only live material. This is the attic law applied to a document's own closed portion, and a gate holds that nothing rotated is lost.

**User Story:** As a person whose scans slow on ever-growing documents, I want each fully-closed portion rotated into a dated archive with a manifest, so that the live file shrinks while every rotated row stays findable and nothing is lost.

### Acceptance Criteria

**Case: rotate the closed portion**

1. *when* a growable document holds enough fully-closed material, the system *shall* move the closed rows into a dated archive under `docs/queue-archive/` and leave a manifest line naming which rows moved and where. [INV-209, INV-276]
   - for the queue, the closing commit is that moment: the live-body law moves each closed row as it closes.
2. The system *shall* read a row as rotatable only when it carries a closed status and no open signal, reusing the existing signal rather than minting a marker. [INV-209, INV-164]

**Case: the gate holds nothing-lost**

3. *if* a row the manifest declares rotated is found in neither the live file nor its archive, *then* the system *shall* red as a nothing-lost violation. [INV-209]
4. *if* an archive file is pointed at by no live manifest line, or a row declared rotated still stands as a live table row, *then* the system *shall* red as ambiguous. [INV-209]
5. *if* a row inside an archive carries no terminal word in its status — landed, decided, declined, or superseded — *then* the system *shall* red it by name, since a row still open there is reachable from no answer about what is left. [INV-209, INV-276]

---

## Requirement 251: Only an assigned session writes the pack repository

**Context:** The pack runs on its own method, and its repository is a shared surface whose push gates run mechanically on installed hooks. Only a session assigned to the pack itself writes this repository; every other session is read-only here, with one exception — creating a new file in the inbox. A developer's machine keeps its installed skills fresh by a named step, since a hand-copy syncs silently and tells the next breakpoint nothing.

**User Story:** As a maintainer of the shared pack repository, I want only the assigned session to write it and the installed skills synced by a named step, so that no outside session scrambles the tree and every skill version change is reported aloud.

### Acceptance Criteria

**Case: the write test**

1. *if* a session cannot say the human asked it in this conversation, or through a standing routine the human created for the pack, to change the pack, *then* the system *shall* not write the repository. [INV-10]
2. The system *shall* keep every other session read-only on this repository, with one exception — creating a new file in the inbox. [INV-10]

**Case: the developer machine syncs by a named step**

3. *when* a session edits a skill on the developer machine, the system *shall* sync the installed copy the same session through the named tool `scripts/sync-skills.sh`, reporting every version change from old to new as the line the re-read rule fires on. [E-23, D-4, A-7]
4. The system *shall* retire a hand-copy, since it syncs silently and tells the next breakpoint nothing that moved. [E-23]
5. The system *shall* run the repository's own push gates mechanically on installed hooks — a fresh prover record, a green suite, anchor ownership, and matrix coverage. [M-4]
6. The system *shall* mint each session a stable identity at its start, so two sessions racing one act tell themselves apart. [INV-117]

---

## Requirement 267: A capability the pack can ship identically lives in one pack home

**Context:** Where a capability's body lives is placed on the pack-to-host axis by one question: can the pack ship a single identical body that every host runs? The base rulebook gives every fact one home, and this rule resolves where that home sits when the pack could hold the body or each host could. A body the pack can ship identically centralizes; a host-specific body ships as a shape each host fills.

**User Story:** As a person placing a capability's body, I want the pack-to-host question to settle whether it centralizes or ships as a shape, so that shared machinery has one source that a fix reaches everywhere while a host-specific part stays home.

### Acceptance Criteria

**Case: the placing question**

1. *when* a capability's body could live in the pack or in each host, the system *shall* place it by one question — can the pack ship a single identical body that every host runs — resolving where the fact's one home sits. [INV-163]

**Case: the two poles**

2. *when* the pack can ship one identical body, the system *shall* centralize the body to a single pack home adopted by a package update, so a fix lands once and reaches every host and no divergent copy can form, the browser test harness the centralize pole. [INV-163, INV-158]
3. *when* the body is host-specific — it names a host's own surfaces, holds a host's own data, or reads a host's own artifacts — the system *shall* ship the shape, a template and the guidance around it, and have each host own the instance it fills. [INV-163]
4. The system *shall* ship the shape for three capabilities. [INV-163, INV-125, INV-136, INV-139, E-26]
   - the cross-surface uniformity rule ships as its rule and prover lens;
   - a project kind's design principles ship as the law and starter set, with the pixel projection left to the adopting project;
   - the removal-list scanner ships as host-held greps under a pack-shipped template.

**Case: the boundary moves toward centralization, binding forward**

5. *when* a host's instance grows a generic seam, the system *shall* lift that seam to the pack and keep the host-specific remainder home, so the boundary moves toward centralization as a body proves uniform. [INV-163]
6. The system *shall* have a new host-specific capability state which pole it takes from its first landing, the bodies that predate this rule standing as they are cited. [INV-163, INV-159]

---

## Requirement 268: Adoption wires the ratchet gates in one pass, seeded at the host's current size

**Context:** The compaction and register gates a machine can run reach a host through one installable kit rather than prose the host re-implements. The pack vendors the style lint, the redundancy precheck, the freeze tool, and their shared library into the host's tree, each vendored copy carrying a source pin so a later update check can tell a current copy from a stale one. The kit seeds the host's debt caps at the host's current measured size, so the gate is green the moment it lands and every later push may only hold or shrink the debt.

**User Story:** As a person adopting the pack, I want the ratchet gates vendored, seeded, guard-tested, and wired into the push gate in one pass, so that adoption demands no re-compaction and the ratchet points down from the first landing.

### Acceptance Criteria

**Case: vendor the kit with source pins**

1. *when* adoption runs, the system *shall* vendor the style lint, the redundancy precheck, the freeze tool, and their shared library into the host's tree. [INV-172, A-7]
   - each vendored copy carries a source pin: the pack version and the content hash it came from;
   - a later update check reads that source pin.
2. The system *shall* merge the ratchet manifest across installer runs, so a prior install's keys survive a later run of the other kit. [INV-172]

**Case: seed the caps and pin them**

3. *when* the installer runs the gates over the host's declared doc set, the system *shall* write the cap file at the counts it finds, so the gate is green the moment it lands and every later push may only hold or shrink the debt, demanding no re-compaction at adoption. [INV-172]
4. The system *shall* pin the seeded caps with a generated guard test, so lowering the cap file is an ordinary edit while raising it demands editing the test. [INV-172, INV-98]

**Case: wire the push gate red-first**

5. *when* the installer wires the gates into the host's push gate, the system *shall* insert the block at a safe anchor ahead of the host's terminating exit. [INV-172, INV-97]
   - verifies the block is reachable before reporting the gate wired;
   - follows the four project-side checks' shipping contract — config-driven, standard-library only, one JSON line per red — and their red-first attachment proof.
6. *when* a re-run finds a block stranded past a terminating exit, the system *shall* repair it by moving it to the safe anchor. [INV-172]

---

## Requirement 269: The pack's hooks have one canonical home, split universal against personal

**Context:** A live-channel hook the pack relies on lives as source in the pack's `hooks/` home and reaches a machine through an installer, the same ship-and-attach contract as the gates. A hook living only in an installed location has no home to update from, and that is a defect of this law. The set splits on one question: a universal hook enforces a pack law that binds every host, and a personal hook enforces one human's own patterns.

**User Story:** As a person installing the pack's hooks, I want each hook homed as source in the pack and split into a universal set that ships and a personal set the personal layer owns, so that a fix has one home and the pack ships nobody's personal rules.

### Acceptance Criteria

**Case: the canonical home**

1. The system *shall* keep a live-channel hook the pack relies on as source in the pack's `hooks/` home reached through an installer, and *shall* read a hook living only in an installed location as a defect of this law. [INV-173, INV-108, INV-97]

**Case: universal against personal**

2. The system *shall* split the set on one question: a universal hook enforces a pack law that binds every host, such as the contrast-frame scan in the docs language, and ships with the pack; a personal hook enforces one human's own patterns, such as a chat-language rule, and lives in the personal layer. [INV-173]
3. The system *shall* have the canonical universal hook read the personal patterns as an overlay file the personal layer owns, so one installed hook serves both. [INV-173]
4. *when* adoption or the machine-setup walk runs, the system *shall* install the universal set by the agent's own hand and say it aloud in the report. [INV-173]

**Case: a scan hook skips a demonstration**

5. *when* a scan hook reads text inside quotation marks or code fences, the system *shall* skip it, since such text names a pattern rather than using it, so a demonstration is never flagged. [INV-173]

---

## Requirement 270: The installed gate is the source gate, held by a config-health check

**Context:** A gate lives twice — its source in `guardrails/` travels with the repo, its installed copy in the hooks directory runs — and the two drift the moment an install is skipped. A stale installed hook silently under-runs the source's gate list, which is how a gate believed wired stays unenforced. The config-health check reds the drift and names the one fix, and it runs inside the suite so even a stale push gate that still runs the tests surfaces the drift.

**User Story:** As a maintainer trusting a wired gate, I want a config-health check that reds a missing or drifted installed hook against its source, so that a skipped install cannot leave a gate believed wired but unenforced.

### Acceptance Criteria

**Case: the check reds the drift**

1. *when* an expected hook is missing from the hooks directory or differs from its source, the system *shall* red the config-health check and name the one fix, running it inside the suite and wiring it into the push gate itself. [INV-175, INV-164]

**Case: it reads the whole source directory**

2. The system *shall* read the whole hook source directory against the installed set, so every hook the pack ships is covered the moment it lands with no edit to the check. [INV-175]
3. *when* a file lives only in the installed set — a personal-layer overlay the pack never ships — the system *shall* leave it alone, since it has no source to drift against. [INV-175]
4. *when* a checkout carries no installed hooks by design, such as a continuous-integration runner, the system *shall* skip the check by name. [INV-175]

**Case: the commit fence's second arm**

5. *when* a file is both staged and holding unstaged modifications at commit time, the system *shall* read it as a fence stop, the signature of a second writer touching a file mid-landing. [INV-175, INV-11, INV-174]

---

## Requirement 271: The installed skill copy is the source skill

**Context:** The pack authors a skill in `skills/<skill>` and the seat installs a working copy at the agent's skills home, and the two drift the moment an install is skipped, so an out-of-date installed skill silently runs an older behaviour than the pack ships. The config-health check gains a second arm beside its hook-diff arm to catch this, holding the installed skill copy to its source.

**User Story:** As a maintainer relying on installed skills, I want the config-health check to red an installed skill that has drifted from its pack source, so that a stale installed skill cannot silently run an older behaviour than the pack ships.

### Acceptance Criteria

**Case: the skill-copy arm**

1. *when* an installed skill tree is un-synced or drifted against the pack's `skills/` source, the system *shall* red the config-health check's skill-copy arm and name the one fix, to re-run `scripts/sync-skills.sh`. [INV-243, INV-175]
2. The system *shall* read the whole skill source directory against the installed set, so every skill the pack ships is covered the moment it lands and a personal-layer skill with no pack source is left alone. [INV-243, INV-175]

**Case: a shipped skill is held byte-pristine**

3. The system *shall* hold a shipped skill's installed copy byte-pristine, the recursive tree diff counting even an extra file dropped inside a shipped skill's directory as drift. [INV-243]
4. *when* a checkout carries no installed skills, such as a continuous-integration runner, the system *shall* stand the whole check down through its single top-of-file carve-out, so the skill-copy arm needs no skip of its own. [INV-243, INV-175]

---

## Requirement 272: A law that earns a gate gets a retroactive gate over the whole tree

**Context:** When a request or a stated law is extracted into a mechanical gate, the gate's scan is retroactive by construction: it reads the entire tracked tree, or the whole gated artifact set, rather than the changed lines alone. So the debt that predates the gate is found the day the gate lands, never the day each old file happens to be touched next.

**User Story:** As a person landing a new gate, I want its scan to read the whole tree from the first landing, so that debt older than the gate is found at once, in a single sweep of the tree.

### Acceptance Criteria

**Case: the scan is retroactive by construction**

1. *when* a law is extracted into a mechanical gate, the system *shall* scan the entire tracked tree or the whole gated artifact set, reaching beyond the changed lines, so debt that predates the gate is found the day the gate lands, as the browser-mute gate reds an old script the same as a new one. [INV-176, INV-164, INV-157]

**Case: an over-big backlog and the catch-up run**

2. *when* the found backlog is too big to fold at once, the system *shall* absorb it by the seeding law, seeding the cap at the current size so it ratchets down. [INV-176, INV-172]
3. *when* adoption or a catch-up walk runs, the system *shall* run the pack's current gate set backward over the host's existing tree the same way. [INV-176, A-11]

---

## Requirement 273: The pack's version is one fact, stamped outward from one home

**Context:** The product's version lives in one place, the root VERSION file. Every skill's frontmatter version line and every in-text base-version reference is a stamped copy written by the sync script at every bump and held by a guard test, so a copy that drifts reds the guard test instead of quietly disagreeing. A per-skill number hand-rolled at edit time drifts the moment attention does.

**User Story:** As a maintainer reading a version anywhere in the pack, I want every shown version to be a stamped copy of one root home, so that no two copies can disagree and a record's version line names the pack version.

### Acceptance Criteria

**Case: one home, stamped copies**

1. The system *shall* keep the root VERSION file as the one home and *shall* write every skill's frontmatter version line and in-text base-version reference as a stamped copy, refreshed by the sync script at every bump and held by a guard test that reds a drifted copy. [INV-178, INV-14]
2. The system *shall* have a record's version line name the pack version from this law on. [INV-178]

---

## Requirement 274: A release's number reports what taking it costs a host

**Context:** A release picks a version number, and the number answers one question for a host that vendored the previous version: what taking it costs the host, in the host's own action. A patch costs nothing, a minor costs a re-run of the catch-up walk, and a major costs a change to what the host already carries. The default is a patch, raised only where the release earns the higher tier.

**User Story:** As a host reading a release's number, I want it to tell me what taking the release costs me in my own action, so that I know whether to do nothing, re-run my catch-up walk, or follow a migration.

### Acceptance Criteria

**Case: the three tiers answer one question**

1. The system *shall* have a release's number answer one question for a host that vendored the previous version: what taking it costs the host in the host's own action. [INV-217]
2. *when* a release fixes a machine to hold a law already stated, with no new capability and no changed contract, the system *shall* number it a patch, which the host takes by doing nothing. [INV-217]
3. *when* a release grows what a host may adopt — a new capability, a new law, a new gate — in a backward-compatible way, the system *shall* number it a minor, which the host takes by re-running its catch-up walk with nothing it already carries rewritten. [INV-217, INV-91]
4. *when* a release cannot be taken without the host changing what it already carries, the system *shall* number it a major and ship its dated migration chapter. [INV-217, INV-91]
   - such a change is a reworded vendored rule, a renamed or removed surface a host depends on, a changed adoption or catch-up step, or a moved law that forces host action.

**Case: the tier call is a stated judgment**

5. The system *shall* default to a patch and raise to a minor or major only where the release earns the higher tier. [INV-217]
6. The system *shall* keep the minor-versus-major call a stated guidance the releasing session applies and names, held by no gate, the same standing as a design-review finding that never blocks a lane, since the call reads meaning a machine cannot. [INV-217, INV-141]
7. The system *shall* home this rule in the base rulebook, in build-pipeline's commit-and-show step, and here, beside the version-is-one-fact home. [INV-217, INV-178]

---

## Requirement 275: The pack's authored artifacts and their installed copies are one class

**Context:** A capability the pack authors lives twice — its source in the pack, a running copy on the host — and the two drift the moment an install or a stamp is skipped. The class carries one parity: each member names the mechanical net that tells its running copy stale. The installed skills were the class's weakest member, held by discipline where its siblings held by a machine, until the config-health skill-copy arm gave them a net too.

**User Story:** As a person trusting the pack's installed copies, I want every installable artifact to name the net that catches its running copy going stale, so that no installed copy can fall silently behind the pack it came from.

### Acceptance Criteria

**Case: the class and its parity**

1. The system *shall* read the pack's authored artifacts and their installed copies as one class, each member naming the mechanical net that tells its running copy stale. [INV-180]

**Case: each member names its net**

2. The system *shall* have the vendored kit scripts name the ratchet manifest's source pin, the pack version and content hash the update check reads against the pack's current copy. [INV-180, INV-172, INV-177]
3. The system *shall* have the installed hooks and gates name the config-health check that reds a hook missing from the hooks directory or drifted from its source. [INV-180, INV-173, INV-175]
4. The system *shall* have the stamped version copies name the stamp script and the guard test that reds a copy diverged from the one home. [INV-180, INV-178]
5. The system *shall* have the installed skills name the config-health skill-copy arm, backed by the session-run version compare at the freshness points, the same-session sync through the named tool, and the daily update proposal. [INV-180, INV-243, A-7, M-7, E-23, E-25, D-4]

**Case: the class binds forward**

6. The system *shall* have a new installable artifact state its own staleness net against this parity, the members named before the class standing as they are cited. [INV-180, INV-159]

---

## Requirement 276: Adoption adds the document-provenance axis

**Context:** Adoption adds one composition axis beyond the floor: document provenance, where a spec claim came from. A claim written fresh under the pack is native and trusted from the start. A claim recovered from documents a project held before adoption is re-engineered and starts unverified, staying unverified until it is reconciled against real code or removed.

**User Story:** As a person adopting an existing project, I want each spec claim marked by where it came from, so that a claim recovered from pre-adoption documents is checked against real code before it is trusted as truth.

### Acceptance Criteria

**Case: the provenance axis and its two values**

1. *when* a project is adopted, the system *shall* add document provenance as a composition axis, marking each spec claim by where it came from. [A-3, C-1]
2. The system *shall* read a claim written fresh under the pack as native and trust it from the start. [C-1]
3. The system *shall* read a claim recovered from a project's pre-adoption documents as re-engineered, holding it unverified until it is reconciled against real code or removed. [A-3]

## Requirement 292: Every session hook carries a known-red proof

**Context:** A hook reports nothing two ways: because the turn was clean, or because it no longer fires at all. The push side settled this long ago [INV-212]; the session hooks had nothing of the kind, so a hook whose pattern list, stand-down clause, or exit path broke would go on reporting nothing and read as a clean turn. A registry gives each hook a fixture built to trigger it, and a runner executes the hook script itself against that fixture.

**User Story:** As a person relying on the session hooks to catch an offence in the seat's own words, I want every hook run against a fixture built to make it fire, so that a hook that has gone silent is named by a run of its own and the whole run fails.

### Acceptance Criteria

**Case: a fixture per hook, run for real**

1. The system *shall* classify every session hook the wired-hook declaration lists in a red-proof registry, each proof naming a fixture that makes the hook print a live decision, and *shall* execute the hook script itself against it, mocking none of its logic. [INV-282, INV-212, INV-211]
2. *when* a hook stays silent against the fixture built to trigger it, the system *shall* name it and fail the whole run. [INV-282]
3. The system *shall* resolve the pack's own copy of a hook before the installed copy, and *shall* report the fall back to the installed copy rather than taking it silently. [INV-282, INV-175]
4. *where* a hook reads a verdict file the person's live state owns, the system *shall* seed it under a temporary home directory, so no live state is touched. [INV-282]

**Case: a hook whose output can carry no verdict is declared**

5. The system *shall* let a hook whose output can never carry a verdict be declared with its recorded reason, *shall* report that entry on every run, and *shall* never count it as a failure. [INV-282, INV-212]
6. *if* a hook the wired-hook declaration lists is classified in neither map, *then* the system *shall* red it by name, holding that declaration's library files — a reader another hook invokes, an opt-in net a host turns on — outside the population. [INV-282, INV-211]

**Case: what the proof reaches, and what it does not**

7. The system *shall* prove the firing direction of the pack's own copy only, the installed copy's agreement with its source staying with the config-health check and its presence in the installed settings with the judge-listed check. [INV-282, INV-175, INV-211]

**Case: the registry names files that exist**

8. *if* an entry in either map, or a name in the wired declaration, resolves to a file found under neither the pack's own directory nor the installed one, *then* the system *shall* red it by name. [INV-282, INV-211]

---

## Requirement 295: A chat law is judged while the turn still runs — retired

**Context:** The PreToolUse arm this requirement specified stood before every tool call in the tree. It judged the seat's narration alone, and it delivered its refusal into whichever tool call happened to be in flight — a background worker's included, where it arrived as an order from nowhere to rewrite a sentence that worker never wrote, and was hunted for a night as an instruction planted from outside. No field of the event the arm reads separates the seat's call from a worker's, so it could not prove whose work it stopped, and the law that a check unable to prove that stands down governs the arm itself. Its retirement is recorded in JOURNAL.md. The two laws it carried stand: the code-anchor law keeps the Stop-side scan that reads the same text at the turn's end (Requirement 293), opt-in by Requirement 311, and the measurement law now names no machine and rests with a person.

**User Story:** As a person whose background workers were stopped 76 times by a refusal about lines they never wrote — counted off the transcripts by record shape, a tool result opening with the scan's own refusal line, the count deciding whether the arm was repairable or had to go — I want the arm retired rather than left standing, so that no check in the pack refuses work it cannot prove is the work it is judging.

### Acceptance Criteria

**Case: retired**

1. The system *shall* carry no PreToolUse arm implementing this requirement; its former files stand retired at `attic/midturn-chat-scan.py` and `attic/chat-calques.json`, never re-armed without a fresh decision. [INV-285]

---

## Requirement 296: A rendered page built for one reading is cleared once its moment passes

**Context:** A rendered page is built for one reading, and it stays in the tree until someone notices it, so a working directory carries several at any moment and the count only grows. The renderer says which kind of page it is: a page the document renderer produced is transient, and every other page in the tree is the artifact itself — a hand-built decision page, a frozen norm card, a test fixture, a prototype sketch, a project's built site. The renderer decides because it is the one thing that knows: it stamps its mark into every page it writes, so the mark cannot drift from the truth, and nothing else carries it. A naming convention is a habit a writer forgets on a single file, and a directory list has to be kept honest by hand and reads a project's own build output as pages built for one reading. A transient page is cleared once its reading is over, and the clearing moves it to the attic with a manifest line, the road base rule 10 already gives a superseded file.

**User Story:** As a person who opens the pages the agent renders for me, I want each one cleared once I have read it and kept somewhere I can reach, so that my working directory holds only pages someone will open again while anything I might still need stays recoverable.

### Acceptance Criteria

**Case: the renderer tells the two kinds apart**

1. The document renderer *shall* stamp a generator mark into every page it writes, and the system *shall* read a page carrying that mark as transient. [INV-286]
2. *where* a page was rendered before the mark existed, the system *shall* read its source document standing beside it under the same name as the same evidence. [INV-286]
3. The system *shall* read every other page inside the reach as the artifact itself and *shall* leave it standing. [INV-286, A-9]

**Case: a transient page is cleared once its reading is over**

4. The system *shall* clear a transient page *when* the exchange it was built for closes — the person has read it, or its decision is answered and harvested. [INV-286, E-22]
5. The system *shall* move a cleared page into the attic under the one collision law, *shall* delete nothing, and *shall* keep the page recoverable from there. [INV-286, INV-7, A-4, E-9]
6. The system *shall* write each page's manifest line as that page moves, so a run that halts partway leaves every page it already moved accounted for. [INV-286, A-4]
7. The system *shall* name every page it cleared, why it read that page as a render, and where it comes back from, both in the manifest line and to the person. [INV-286, INV-28, A-4]

**Case: a release sweeps what accumulated**

8. *when* a release leaves the machine, the system *shall* sweep every transient page still standing and *shall* report the outcome in one line. [INV-286, INV-44]

**Case: a page left standing reds**

9. *while* a transient rendered page stands in the tree, the system *shall* red the sweep check, and the clearing *shall* clear that red. [INV-286]
10. The check *shall* state its reach on its passing line: the count of pages read, the mark they were read for, and what stands outside the reach. [INV-286, INV-269]

**Case: the reach stops before committed history**

11. The system *shall* leave every page version control tracks outside the sweep, *because* removing tracked history is a commit with its own gate. [INV-286, INV-7]
12. The system *shall* leave the version-control directory, the harness's worktree home, the host state directory, and the attic outside the sweep. [INV-286]
13. The system *shall* let a host add its own homes outside the reach as host configuration, on top of the pack's own four, which no declaration lowers. [INV-286, INV-224]

---

## Requirement 298: The setup walk installs every session hook the pack declares

**Context:** `guardrails/judge-hooks.json` declares every wired session hook, each with the event it rides. `scripts/install-session-hooks.sh` is the one command a human runs, since the harness classifier blocks an agent's own hand in its configuration. Before this requirement it installed its own two alone; the rest reached a real machine only by hand, so a fresh machine, and any host adopting the pack, got a fifth of the conduct machinery with no sign the rest was missing. The fix generates the installer's own coverage from the declaration and chains to the existing installer that already covered the rest, so the one command reaches every declared hook with its data files.

**User Story:** As a person adopting the pack on a fresh machine, I want the one installer command to place every session hook the declaration names. Then no shipped hook is missing from my machine without a sign.

### Acceptance Criteria

**Case: generated coverage**

1. *when* the human runs the installer, the system *shall* place the file of every hook the declaration's `file` map names and wire every hook in its wired declaration, each under its declared event with its declared command form. [INV-289]
2. The system *shall* install every data file a hook's declaration names, beside that hook. [INV-289]

**Case: both directions proven mechanically**

3. *if* a declared wired hook is missing after a fresh install, *then* a check *shall* fail naming it. [INV-289]
4. *if* the installer places a file the declaration names nowhere, *then* the same check *shall* fail naming it. [INV-289]

**Case: idempotence and personal overlays**

5. *when* the installer runs a second time, the system *shall* change nothing already wired or already installed, recognizing a hook already wired under any command form. [INV-289]
6. The system *shall* never create, edit, or overwrite a personal overlay file, and *shall* name each one it finds already present. [INV-289]

**Case: the host wires the opt-in six itself**

7. The installer *shall* wire none of the six opt-in hooks, placing their files and leaving each host to add the command it wants. [INV-289, INV-211]


---

## Requirement 300: The rules about this project's own texts hold one home and move as one family

**Context:** This project states rules about how its own texts are written. They govern the spec body, the prose a person reads, the chat surface, and the published artifact. Each rule carries the sentence it states, the test a reader applies, the surfaces it binds, its status, its catcher, where that catcher is armed, the files that state it today, and its thresholds, exceptions and examples where it has any. A catcher is a pattern list, a model reading meaning, or a person. These rules are relatives of each other. A word held back on one surface, a gloss owed on another, and a register judged on a third all decide the same question about the same sentence. A rule spread over several files ends up with a different verdict in each, and a rule changed alone leaves its relatives disagreeing with it. This requirement gives them one home, generates every consumer from that home, and works them in one pass.

**User Story:** As a person reading anything this project writes, I want every rule about its language to hold one home and change together with its relatives, so that no two places state one rule with two verdicts.

### Acceptance Criteria

**Case: one home for the rules about text**

1. Every rule governing this project's own human-facing text *shall* live in `guardrails/language-rules.json`. [INV-292]
2. Each rule *shall* carry its own sentence, the test a reader applies, the surfaces it binds, and its status, and *shall* carry its thresholds, its exceptions, and its examples *where* it has any. [INV-292]
3. A rule *shall* be edited in its one home, and *shall* record in its `sources` field every other place that states it today. [INV-292]
   - a `sources` entry stands as a place the rule still appears;
   - a statement of a rule that no `sources` entry records is the defect `guardrails/check-language-rules.py` reports.

**Case: the consumers are generated from the home**

4. `scripts/gen-language-consumers.py` *shall* build every consumer of these rules from that home. [INV-293]
5. The generated consumers *shall* be the law text the model judge is handed and the human-readable rendering of the rules. [INV-293, INV-203]
6. *if* a generated consumer differs from the home, *then* the check *shall* red and *shall* name that consumer. [INV-293]
7. *if* a rule points at a file or a line that does not exist, *then* the check *shall* red. [INV-293]

**Case: every rule names what catches it**

8. A rule *shall* record its catcher. [INV-294]
9. A rule *shall* record where its catcher is armed. [INV-294]
10. A rule that no catcher runs *shall* record the reason none runs it. [INV-294]
11. *if* a rule names no catcher and states no such reason, *then* the check *shall* red and *shall* name that rule. [INV-294]

**Case: the surfaces a rule binds**

12. A rule *shall* name the surfaces it governs. [INV-295]
13. *where* a rule's verdict differs by surface, that rule *shall* hold one entry per surface. [INV-295]
14. The system *shall* let a person's own layer override a rule's exceptions. [INV-295, E-13]
15. *when* a person's layer overrides a rule's exceptions, the home *shall* keep the shipped default stated beside that override. [INV-295, E-13]

**Case: the family is worked in one pass**

16. The system *shall* treat the rules about this project's own texts as one family. [INV-296]
17. *when* one of these rules changes, the system *shall* read it against its relatives in the same pass. [INV-296]

**Case: a reader's finding enters as a class**

18. *when* a reader finds a defect in this project's text, the system *shall* enter that defect in this home as a class carrying its definition. [INV-297, INV-124]
19. The examples that produced a class *shall* sit beneath that class as its evidence. [INV-297]
20. The home *shall* hold no entry that gathers examples with no class stated over them. [INV-297]

---

## Requirement 301: A worker restores a file it mutated by writing its own saved bytes

**Context:** A worker writes the files its brief names, and the pack's own red-first method has it mutate a shipped artifact to prove a row red. A git command that discards uncommitted work is a different act: its blast radius is a path, so it lands on files the worker never wrote and its brief never named, and the `git status` a careful worker pastes afterwards reads clean in the safe case and the destructive one alike. So a worker holds the bytes it is about to overwrite and puts them back itself, and a worker holding none halts for the orchestrator. The orchestrator owns recovery, and the last committed stage is what a repair reads from. The census arm of the mechanical check reads records that stay on disk, so a finding it makes is true forever and a finished recovery used to clear nothing: every push after an incident waited for the reading window to roll past it. What counts as made good is stated once, below, and it is a question put to the repository the command ran in, answered afresh on every run, so nothing records that a finding was cleared and no reader has to trust such a record.

**User Story:** As a person whose session holds uncommitted work, I want a worker to put back only what it wrote, so that my unsaved edits survive another lane's repair.

### Acceptance Criteria

**Case: the worker holds its own bytes**

1. *when* a worker intends to mutate a file it will put back, the worker *shall* read and hold that file's bytes before the mutation. [INV-298]
2. *when* a worker puts a file back, the worker *shall* write its own saved bytes. [INV-298]
3. A worker *shall* run no command that discards uncommitted work, in any tree. [INV-298]
   - the discarding commands are `git checkout` on a path, `git restore` outside `--staged`, `git stash` in its saving forms, `git reset` with `--hard`, `--merge`, or `--keep`, and `git clean` with `-f` or `-x`.
4. A worker inside its own isolated worktree *shall* hold this same rule, since that worktree shares one repository with the lanes beside it. [INV-298]

**Case: a worker with no saved bytes halts**

5. *when* a worker holds no saved bytes for a file it mutated, the worker *shall* halt and *shall* report the file and the mutation it made. [INV-298]
6. *when* a worker believes a file needs a git-level restore, the worker *shall* halt and *shall* report what it read. [INV-298]
7. A halting worker *shall* write no further file and *shall* run no further command. [INV-298]

**Case: the orchestrator owns recovery**

8. *when* a worker halts under this rule, the orchestrator *shall* restore the named file from the last committed stage and *shall* hand the worker a fresh brief carrying that file's current bytes. [INV-298]
9. The orchestrator *shall* record the halt in the row's delivery report, and the halted work *shall* resume under that new brief. [INV-298, INV-103]
10. The orchestrator *shall* commit a finished build stage before the next worker touches its files. [INV-298, INV-39]
11. A session holding the pen *shall* hold this same rule *while* another session or another worker carries uncommitted work in the same tree. [INV-298, INV-11]

**Case: the clause rides every brief**

12. Every brief a session composes for a worker *shall* carry this rule in the pack's own words. [INV-299, INV-173]
13. The pack *shall* state this rule in its shared rulebook, in the pipeline skill, in the delegation protocol, in the agent-card template, and in the lane-opening script, with one wording across all five. [INV-299]
14. *if* two of those homes state the rule with different words or a different command list, *then* the suite *shall* red and *shall* name both homes. [INV-299]

**Case: the mechanical arm**

15. `guardrails/check-worker-restore.py` *shall* read the worker runs' transcripts and *shall* red a run that handed a shell any of the discarding commands. [INV-299]
16. The check *shall* read a command a worker handed to a shell, and *shall* leave alone a report, a brief, or a plan that names such a command. [INV-299]
17. The check *shall* run at the verify step, and its verdict *shall* stand between a worker's result and the orchestrator's acceptance of it. [INV-299, INV-46]
18. *when* the transcript root does not exist, the check *shall* stand down by name and *shall* say what it read nothing of. [INV-299, INV-218]
19. *if* the transcript root exists and holds no worker-run transcript, *then* the check *shall* red by name. [INV-299, INV-218]
20. Each run *shall* state its reach: the transcript root, the file pattern it matched, the window it read, and the count of command lines it took. [INV-269]

**Case: a finding the tree shows made good**

21. A finding *shall* count as made good *when* every file its command named carries, in the repository that command ran in, a commit dated later than the command by author date, and each such file still sits at the tip of that repository's current history — the work at those paths is saved in that repository's history again, and is there to see now. [INV-299]
22. *when* a finding counts as made good, the census arm *shall* red nothing for it and *shall* keep it named in the report beside the commit that made it good. [INV-299]
23. *if* a command's blast radius names no single file — the whole working tree, a directory, a path carrying a glob metacharacter or opening git's pathspec-magic prefix, or a path the check cannot place in a repository — *then* that finding *shall* never count as made good, since no commit can show an unbounded set of lost bytes is back. [INV-299]
   - a path is confirmed as naming exactly one file by asking git: it *shall* pass only when it names no glob and the repository's own tracked files answer with that one path and no other.
24. A finding whose record carries no timestamp *shall* never count as made good, since the check cannot say which commits came after it. [INV-299]
25. The verify arm *shall* apply none of this, and a worker run it reds *shall* stay red for acceptance however the tree moves afterwards. [INV-299, INV-46]
26. *if* a later commit only deletes a path the command named, *then* that finding *shall* never count as made good, since the path no longer stands at the tip of the repository's current history and the work it named is not there to see. [INV-299]
27. "Dated later than the command" in criterion 21 *shall* be read from the commit's author date, since `git commit --amend` and a rebase both reset the committer date to the moment they run while leaving the author date unchanged. [INV-299]
   - an author date set by hand with `git commit --date` is a bound this requirement cannot close; no fact the repository holds can tell such a date from a genuine one.


## Requirement 302: A document repaired to zero stays at zero, and every other count moves down alone

**Context:** The census measures every live document against the project's writing rules and prints a report. A report refuses nothing, so a count is free to rise between two readings. One generated page went from 107 findings to 112 in a single day, and nothing noticed until the next census was read by hand. A document repaired to zero is held at zero on every push, without exception. The record of counts is the ceiling, and the direction of every count is down.

**User Story:** As the owner, I want a repaired document held at its count on every push, so a cleared page collects no new findings.

### Acceptance Criteria

**Case: the record is the ceiling**

1. The system *shall* hold one recorded finding count per live document in `guardrails/rule-census.json`. [INV-301]
2. *when* a push runs, the system *shall* measure every live document and *shall* compare each count against its recorded count. [INV-301]
3. *if* a document's count stands above its recorded count, *then* the system *shall* refuse the push. [INV-301]
   - the refusal *shall* name the document, its recorded count, and its measured count.
4. *if* a document recorded at zero carries any finding, *then* the system *shall* refuse the push. [INV-301]
   - the refusal *shall* name that document as one already cleared.

**Case: a fall tightens the ceiling**

5. *when* a document's count falls below its recorded count, the system *shall* pass that document and *shall* print the command that records the lower count. [INV-301]

**Case: nothing ships unmeasured**

6. *if* a live document carries no entry in the record, *then* the system *shall* refuse the push and *shall* name that document. [INV-301]
7. *when* the record names no document, the system *shall* refuse rather than pass over an empty set. [INV-301, INV-218]
8. Each run *shall* state its reach: the count of live documents read, the count held at zero, and the word cap it measured against. [INV-301, INV-269]

**Case: the record moves only down**

9. No run *shall* raise a recorded count. [INV-301]
10. *when* the census writes the record and no live document stands above its recorded count, the system *shall* write each measured count back. [INV-301]
11. A raised recorded count *shall* be a hand edit to the record, stating a non-empty `reason` field for the raised entry. [INV-301]
   - the census carries a recorded reason forward, so a later write keeps it.
12. *when* the gate runs, one arm *shall* read the record against the copy the base commit holds. [INV-301]
   - the base commit is the one the remote holds, read from the stated base, then `origin/main`, then the commit before the tip;
   - the tip itself is read where a repository holds one commit and no upstream.
13. *if* an entry's recorded count rose against that copy with no reason beside it, *then* the gate *shall* red. [INV-301]
   - the refusal *shall* name the document, the count that copy holds, and the recorded count.
14. *where* no such copy is reachable, that arm *shall* stand down by name and *shall* say what it read nothing of. [INV-301, INV-218]
15. *when* no recorded count stands above that copy, that arm *shall* say nothing and *shall* leave the verdict to the document arm. [INV-301]
16. *if* any reading refuses to run, *then* the census *shall* write no record and *shall* name that reading. [INV-301]
   - a live document the census could not read *shall* stop the write the same way.

---

## Requirement 306: A count this repository publishes about its own tree is built from the tree

**Context:** A reader who meets a number decides whether to trust it. A count a person typed goes stale as the tree grows. The reader cannot tell a fresh count from a stale one. So every count this repository publishes about its own tree carries a declared measurement, a home, and a push gate.

**User Story:** As a reader, I want each count built from the tree, so that a figure I cannot check never reaches me.

### Acceptance Criteria

**Case: every published count is declared**

1. The system *shall* declare each count this repository publishes about its own tree in `guardrails/tree-counts.json`. [INV-305]
   - the entry carries the measurements producing the count and every page statement of it.
2. The system *shall* refuse to build a count whose ground leaves any part empty. [INV-305]
   - the parts are what it counts, its unit, the decision it informs, and what changes when it moves;
   - the remaining parts are its baseline, its better direction, and its target.
3. The system *shall* accept an empty baseline, direction or target that carries a written reason, and *shall* refuse one that carries none. [INV-305]

**Case: a count in a generated block is rebuilt**

4. The system *shall* build a block home's text with `scripts/gen-tree-counts.py`, and *shall* red a committed block differing from a fresh build. [INV-305, INV-258]
5. The system *shall* write no text at a sentence home, and *shall* red where the page lacks the sentence the template renders. [INV-305]
   - the red names the page and the rendered sentence.

**Case: the published command answers for the published number**

6. *when* a measurement declares a reproduction command, the system *shall* run it, and *shall* red where its output disagrees with the number a home states. [INV-305]
7. The system *shall* read a measurement claimed at-least as a floor, and *shall* red only where the tree falls below it. [INV-305]
8. The system *shall* render the reader's copy of a reproduction command from the same argument list it runs. [INV-305]

**Case: what the gate may execute**

9. The system *shall* run a reproduction command as an argument list with no shell, expanding patterns inside the repository root. [INV-305]
10. The system *shall* red a command naming a program outside the declared allowlist, and *shall* run no stage of that command. [INV-305]
11. The system *shall* red an argument that is absolute, that leaves the repository root, or that holds a newline. [INV-305]

**Case: the gate measures what the push sends**

12. The system *shall* red before either arm reads where a path a measurement reads, or a page holding a home, carries an uncommitted modification. [INV-305]
    - the red names the path.

**Case: the gate reports its reach and reds over nothing**

13. The system *shall* red a registry parsing to zero counts, and a pattern matching zero files, by name. [INV-305, INV-218]
14. The system *shall* print on its green line every count read, every page swept, every command run, and its elapsed seconds. [INV-305, INV-269]

**Case: the gate is wired and can fail**

15. The system *shall* leave gate ad (`guardrails/check-tree-counts.py`) and `scripts/gen-tree-counts.py` retired, never re-armed without a fresh decision. [INV-305, INV-210, INV-212]

**Case: honest about its reach**

16. The system *shall* judge whether a published count matches the tree, and *shall* leave to the person whether the count is worth publishing. [INV-305, INV-269]
    - whether the ground stated around a count is the right ground is the person's judgment too.

---

## Requirement 307: The pack records what each of its runnable files is

**Context:** A skill body tells an agent to run a file by path. Some of those files judge the pack's own document set and mean nothing in a host project. Nothing on the page says which is which. So the pack carries one machine-readable record of every runnable file a skill names, what each one is, and which tree each one judges.

**User Story:** As a skill's user, I want each named check to judge my own tree, so that none reads the pack's documents.

### Acceptance Criteria

**Case: the registry records what each runnable file is**

1. The system *shall* carry one registry entry for every runnable file a skill body names in command position, and for every file those entries read. [INV-306]
   - a command position is a path preceded on its line by `python3`, `bash`, `sh`, or a leading `./`;
   - every other path mention is prose and keeps its path.
2. Each entry *shall* record its kind as one of check, library, or data. [INV-306]
3. *if* an entry's recorded kind disagrees with the tree, *then* the gate *shall* red, naming the entry and the test that disagreed. [INV-306]
   - an entry point present or absent, and an import present or absent, are the disagreements this arm reads.
4. *if* an entry's path names no file in the tree, *then* the gate *shall* red, naming the entry. [INV-306]

**Case: a check carries a name, a kit, and a reach**

5. A check entry *shall* carry a name unique across the registry, and a library or data entry *shall* carry none. [INV-306]
6. A check entry's kit *shall* be derived from its reach. [INV-306]
   - an empty reach reads ships; a reach naming a path under the pack's machinery directories reads pack-only; every other reach reads host-optional.
7. *if* a check's source states a document name its reach does not declare, *then* the gate *shall* red, naming the entry and the document. [INV-306]
   - the source is read with comments and docstrings stripped, so a name inside usage text passes;
   - a reach member naming a missing path inside the pack reds on the same arm.
8. Every module a check imports from `scripts/` or `guardrails/` *shall* appear in that entry's needs, and every needs member *shall* be a registry entry. [INV-306]

**Case: a pack-only check leaves the host instructions**

9. No skill body *shall* name a check whose kit reads pack-only in command position. [INV-306]
10. *if* a skill body names a pack-only check in command position, *then* the gate *shall* red. [INV-306]
    - the red names the skill file, the line, and the check's reach.

**Case: a check declares how it learns which tree it judges**

11. Each check entry *shall* record its root as one of argument, working-directory, or own-tree. [INV-306]
12. *if* a check recorded argument or working-directory defaults its scan root from its own file's location, *then* the gate *shall* red. [INV-306]
    - the red names the entry and the line.

**Case: the gate is itself held**

13. The gate *shall* run as gate ae on `guardrails/pre-push`, *shall* carry a red-proof entry, and *shall* appear as a step in the CI workflow. [INV-306, INV-210, INV-212]
14. *when* the gate passes, it *shall* print the count of entries read, the count of skill bodies scanned, and the count of command-position paths found. [INV-306, INV-269]

---
