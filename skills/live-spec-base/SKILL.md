---
name: live-spec-base
description: Load before using any live-spec pack skill (spec-author, product-prover, design-reviewer, build-pipeline, test-author, communicator, feedback-intake, feedback-collector, text-audit, publish), before briefing a worker that will write files, or to resolve shared rules and settings. It is the one home for the shared rules — thirty-four rules in the body — and for the settings ladder.
metadata:
  version: 4.3.0
---

# live-spec-base — one rulebook, ten working skills

The pack's shared working rules live here, once. A working skill opens by naming this base and the
version it was written against. It then references these rules and elaborates only its own domain.
The ten working skills are named in the closing roster below. A second full statement of a shared
rule inside a working skill is drift (SPEC INV-13). It is a defect to fold at the next milestone,
never kept for convenience. One rule is carried whole instead by every skill that briefs a worker.
The worker-restore sub-rule under rule 7 rides each brief in one wording. `tests/test_worker_restore.py`
reds a home that states it in words of its own (SPEC INV-299). Communicator teaches how to speak
plainly; that we speak plainly is this file's sentence. Used standalone, outside the pack, a
working skill still stands: its pointer here reads as plain advice.

## Where the paths and the codes in this file point

This file names paths of two kinds, resolving in two different trees.

**The pack's own machinery** sits in the live-spec repository, whose public home is
`github.com/happysasha18/live-spec`. Its directories are `guardrails/`, `scripts/`, `tests/`,
`templates/`, `hooks/`, `adopt/`, and `skills/`. Each of the ten working skills this file names sits
at `skills/<name>/SKILL.md`, beside this one.

**A host's own documents and workspace** sit at the root of whatever project the pack is attached to.
Those are `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `JOURNAL.md`, `NEXT_STEPS.md`,
`DECISIONS.md`, `attic/`, `prototype/`, `inbox/`, `outbox/`, `docs/`, and `.live-spec/`. The live-spec
repository is a host of its own, so on that one machine the two trees are the same directory.

A bracket code such as `INV-4` is a short handle for one rule of the product spec. Its home is
`PRODUCT_SPEC.md`, where the code trails the line it names. That file's preamble names every letter a
code can carry and what each stands for, so a code this page never uses decodes there. A roadmap row number, such as row 416, names a line of `ROADMAP.md`. A row that has closed
rotates to a dated file under `docs/queue-archive/`. So a row cited here may sit there instead. Two
other bracket marks read as part of the sentence they sit in, and `PRODUCT_SPEC.md` states both.
`[target]` marks a feature or leg that is promised and not yet built. `[default]` names a value the
agent set that the person may retune.

## The words this file uses

Each term is defined once. Most sit in the glossary of `PRODUCT_SPEC.md`, whose entry is the authority
behind the short read given here.

- **the pack** — the shipped live-spec method: its skills, its document and suite templates, and its
  guardrail scripts. It carries a version.
- **a host** — one project the pack attaches to. Each host holds its own spec, queue, journal, and
  `.live-spec/` folder.
- **the seat** — the one acting orchestrator session that owns judgment, orchestrates the pipeline,
  briefs workers, judges lane independence, and reports to the person. The glossary keeps the one name
  seat throughout. It records the senior and the orchestrator as the source's other names for it, and
  this file adds a fourth, the lead. The four names mean the one session.
- **a worker** — a delegated agent session the seat briefs for a bounded piece of mechanical work,
  narrowed to the files its brief names.
- **a tier** — the model level a unit of work runs at: a no-decision one-shot worker, a multi-step
  mechanical worker, or the seat for judgment. Rule 5 names haiku and sonnet as the two worker levels.
- **a brief** — the written instruction set a worker runs from, carrying its files, its steps, its
  clock, and its stop conditions.
- **a wish** — one request a person voices in plain words, captured as a queue row and carried to a
  recorded terminal state.
- **a queue row** — one live wish written as exactly five cells of `ROADMAP.md`: its id, the wish,
  its class, its status, and its acceptance. Its home is `docs/roadmap-format.md`. This file calls it
  a row.
- **a lane** — one build train a session rolls through the pipeline. A lane branch is that lane's
  isolated copy, a git worktree holding a branch named for its queue row.
- **the pen** — the single write-lock a repository holds, under which one delivery reaches the
  repository's shared truth at a time.
- **a landing** — the act of one piece of work reaching the repository's shared truth as one commit
  under the pen.
- **a gate** — a check that must pass before work proceeds, and a red gate stops the work at that
  step. Where a sentence here says a check *reds* something, it means the check fails on it.
- **a checkpoint** — a saved point of work that can be resumed from, written under `.live-spec/`.
- **the attic** — the host's append-only archive folder `attic/`. A superseded file moves here with
  one manifest line and is kept for good.
- **a breakpoint** — a point where a movement ends and session memory can be wiped with no loss, its
  live state replaced, a dated journal entry added, and the work committed.
- **a door** — the intake classification placing a queued wish at one entry point of the pipeline,
  one of feature, bug, refactor, docs-only, or skip. An ask merely to see or try a thing takes a
  separate entry lane, the labelled-sketch door, held outside that five-way set.
- **an agent** — defined where the rule that binds it stands, at rule 31.
- **an agent card** — a host's self-describing file `.live-spec/agent.md`, stating its name, mission,
  zones, published contracts, and inbox address. `templates/agent.template.md` gives its shape.

## The rule of thinking, above all the rest

**Every incoming item is a symptom, and the answer owed is a rule about its class.** One phrase, one
file, one number, one incident — whatever arrives, it arrived as an instance of something. Name the
class, state the rule for it, find the other live instances, and the instance that was pointed at is
repaired as a free consequence. A change that repairs only the instance has answered nothing, because
the next instance is already on its way. The rule holds at every channel an item arrives through, and
there are three: a person's feedback, a finding the agent makes itself, and a message from another
agent. The three are one filter.

This is a rule of thinking, and it governs every rule below it. Rule 14 is its mechanism inside a code
change. Rule 14 came first because the class-shaped answer was noticed in code, and the thinking
generalizes it to everything.

Its own worked failure: the guard holding this pack's register laws was built as a list of literal
patterns. There was one pattern per phrase someone once caught. So the guard built to enforce the
rules was itself the clearest breach of this one. Each caught escape only added one more pattern,
while the next new phrasing passed through untouched (proven by probe, 2026-07-17). The repair
shipped that day as roadmap row 416, which now sits in
`docs/queue-archive/rotated-ROADMAP-2026-07.md`. A law naming a class is held by a judge that reads
meaning. If the answer to a class is a list, the design is wrong.

## The shared rules

1. **Ask, never guess.** A gap only the human can fill — a threshold, a policy, a taste call — is asked or
   marked `⟨DECIDE⟩` with a one-line question and a recommended pick. Never invent intent, and never ask
   what you can decide or verify yourself. A pending question rides in its row while the lane keeps moving
   on the recommendation (SPEC INV-4, INV-5, INV-12). And before offering the human a fork, check whether
   a proven artifact already settles it. Where the architecture, the spec, or the invariants determine
   the answer, derive the requirement. Say it back with the section cited as its ground, offering no fork.
   A fork reaches the human only for what the artifacts leave genuinely open (rule 27 names those cases).
   This is the read-the-doc twin of ask-never-guess: that half forbids inventing an answer, this half
   forbids offering a choice the documents have already made (SPEC INV-121).

2. **Plain words carry the meaning; the code trails, quietly.** Every human-facing sentence stands on its
   own in the product's language. Internal handles never do the talking: an `INV-x` code, a row number, a
   worker name, a model name, a coined feature name, or a metaphor the reader never chose to learn.
   One convention, two faces: in **chat**, the anchor may trail the sentence in parentheses —
   "no remote copy exists (INV-8)"; in **documents**, anchors sit at line ends in square brackets — `[INV-8]`.
   Never open a line with a code. And when chat runs in one language while the docs run in another, a term
   or metaphor coined in the docs language is never loan-translated into chat. That is the **no calques**
   rule: say what actually happens in natural chat-language words. The original term is free to trail in parentheses like any
   anchor. (2026-07-05 — a calque reads as machine-speak and degrades the product.)

3. **One surface = one name, everywhere.** The moment one thing answers to two names, every cross-check
   silently loses the seam between them. The vocabulary comes from the host's SPEC.

4. **One canonical home per fact.** Everything else that mentions the fact is a pointer, and pointers are
   kept live — a doc superseded or moved gets every inbound reference repointed the same session. Two
   documents claiming authority over one fact is undefined behaviour when they disagree.

5. **The lead orchestrates; each unit routes to the cheapest tier that passes its brief (SPEC INV-69).**
   The lead — the orchestrator seat, whatever tier holds it — orchestrates, briefs, and accepts the work,
   and it does not do the grunt itself. Every unit of work is routed PER UNIT:
   the trigger is judgment against mechanical, and the tier is proposed for that unit. A one-shot with no
   decision goes to haiku, multi-step mechanical work to sonnet, and anything carrying judgment or design
   to the senior, and a judgment step is never routed down. Size is a weak hint only, never the decider.
   The worker pastes raw output (command + exit code + failing lines) as it works. Only raw output is
   evidence, and the worker's prose is only a lead. So a worker's green is a lead the lead ACCEPTS by
   re-checking it, never on trust. A
   large or high-stakes landing earns an independent fresh-context checker beyond that re-check (SPEC
   INV-46). Every override of a proposed tier and every
   failed-acceptance escalation is logged, proposed tier → chosen tier → why (SPEC INV-69).

6. **Every long or delegated piece of work keeps a persistent checkpoint.** A file on disk (host home:
   `.live-spec/checkpoints/`, gitignored and kept inside the repo tree) holds done / in-progress / next,
   updated as the work runs, so a cut-off resumes from disk. A landing that ships a checkpoint's items flips that checkpoint to its closed state in the same
   landing, so a returning session never reopens finished work. A checkpoint whose items all live in git
   history is stale by definition and reads as a resume defect (SPEC INV-107). Red at a pause is never
   committed. The failing test name and the hypothesis become the top item of `NEXT_STEPS.md`, so the
   red test is itself the checkpoint. A checkpoint or handoff note that records a live background
   worker also records three things about it. First, the worker's id, pointing at the worker's own
   checkpoint file. Second, its briefed write-set. Third, the liveness checks a resuming session runs
   before touching those files or spawning a sibling. Those checks are the write-set's file times
   watched over a short window, the worker's heartbeat, and one message to its id. The heartbeat is a
   fixed-interval touch on the worker's own checkpoint file, ~60 s [default],
   stale past ~2 min [default]. Such a note never frames the worker's output as finished while the
   worker may still run (SPEC INV-76). Before a memory wipe, prefer
   halting the workers or letting them finish, so the next session starts single-writer. Say plainly
   when a worker dies with a closed window or a sleeping machine. The human's leave-word fires this rule
   for everything open at once. Every lane goes to its checkpoint, workers are halted or landed, and green
   is committed. One closing line follows, only when the whole walk holds (SPEC INV-95; the communicator
   carries the walk).

7. **The concurrent-edit fence, before every write and every commit.** Re-check `git status` and HEAD
   against what you last read. If HEAD moved, or the tree holds changes you did not make, stop, re-read,
   then proceed surgically or back off. A repo you were not assigned to is read-only, apart from a new wish
   file in its inbox. This binds every skill that writes shared files, adoption among them (SPEC INV-10,
   INV-11).
   - **Lanes under one pen, up to the profile cap.** Within one session, build lanes roll without asking up
     to the profile-declared lane cap (SPEC T-18; `lanes.cap`, package default three [E-13]). One more
     opens only on the human's asked word. Every write to a document the lanes share serializes under the
     single PEN, one lane at a time. The pen reconciles that document at integration, so sharing it never
     makes the lanes wait on each other. Co-location alone never pulls two rows into one lane (SPEC INV-49).
   - **The lane-open act.** The session opens a lane by running `scripts/open-lane.sh`, or by walking the
     same steps by hand. First, the row→in-work flip is committed to main under the pen. Second, the branch
     `lane/<row>-<slug>` is cut from that claim commit into its own worktree. Third, the lane goes to a
     worker whose brief names the branch. The act reads the profile cap [E-13] and refuses a lane past it.
     It runs whenever the dependency graph shows two or more independent runnable rows and lanes stand free.
     Going single-file then is recorded on the departures board, the status-report view, as a "serial by the
     graph" board reason. Judging independence is a senior read no gate can settle, so this stays a
     discipline (SPEC INV-214, INV-49).
   - **Worktree isolation on overlap.** A later lane's code and tests live in its own isolated copy of the
     tree until the senior integrates them. So worktree isolation is the default when two lanes' write-sets
     overlap. A shared file one lane holds open is never written by another (SPEC INV-105).
   - **Brief-time disjointness** — before spawning another concurrent writer, the senior confirms its
     brief's write-set is disjoint from every already-running writer's brief, or gives it an isolated
     worktree at brief-time. The fence stays silent between same-session siblings and cannot catch the
     senior's own workers colliding (SPEC ACT-3, INV-11).
   - **A worker never restores a working tree with a git command (SPEC INV-298).** Before a worker mutates a file it means to put back, it reads that file and holds its bytes. A worker puts a file back by WRITING ITS OWN SAVED BYTES. A worker runs no command that discards uncommitted work, in any tree: `git checkout -- <path>`, `git checkout .`, `git restore` outside `--staged`, `git stash` and its `push`, `save`, `create` and `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and `git clean` with `-f` or `-x`. Such a command's blast radius is a PATH, so its damage lands on files the worker never wrote and its brief never named. This rule binds a worker in every tree, including its own isolated worktree, since a worktree shares one repository with the lanes beside it and a worker cannot read off its brief what else that repository holds. A worker that holds no saved bytes for a file it mutated, or that believes a file needs a git-level restore, HALTS and reports the file and the mutation it made, and it writes no further file and runs no further command. The orchestrator owns recovery: it restores the named file from the last committed stage, hands the worker a fresh brief carrying that file's current bytes, and records the halt in the row's delivery report, and the halted work resumes under that new brief. The orchestrator's own half: a finished build stage is committed before the next worker touches its files. `guardrails/check-worker-restore.py` reads the worker runs' transcripts for the command and runs at the verify step.
   - **One row per landing commit.** A landing commit carries exactly one row's delta (SPEC INV-39). Its
     gate runs on a tree clean of any other lane's unfinished work.
   - **A prior-context worker.** A background worker from a prior context is a concurrent writer too. It
     survives a memory wipe, and the process list and the harness task panel are never proof of death. It
     stays a foreign writer until verified by rule 6's three resume checks. No second worker goes onto a
     shared tree until the first replies that it halted, or all three checks declare it dead. The fence's
     silence between same-session siblings never crosses the wipe (SPEC INV-76).
   - **A stable session identity breaks the pen tie.** Every session mints a stable identity at its start
     and records it in its `.live-spec/` checkpoint, unchanged for its life. The identity is the harness
     session id where the context carries one. Otherwise it is the start time joined with the worktree path
     and a single-use random string. On a genuine concurrent claim with no git ancestry, the pen tie-break
     orders on this identity, so exactly one session backs off (SPEC INV-117).

8. **Freshness: versions are re-checked at every breakpoint.** Read the modification time of the
   installed skills, the pack, and the profiles. On any version change, re-read the changed file before
   continuing, work only from that freshly read copy, and journal one line naming old → new (SPEC A-7,
   M-7).

9. **History lives in the journal; docs travel with the change.** The dated reason behind every movement
   goes to `JOURNAL.md` the same session. The prose of `PRODUCT_SPEC.md`, `NEXT_STEPS.md`, and
   `ROADMAP.md` states only current truth. A shipped
   change updates its `README.md`, `CHANGELOG.md`, and `SKILL.md` before the session ends. **Entries and
   harvested records carry the date and the time of day**. Take a line like "yesterday evening you
   wrote X, so I did Y". It is answerable later only when the record kept the time of day beside the
   date. A decision file
   keeps its answered-at stamp, and a journal entry opens with when it happened (2026-07-05).

10. **Nothing is silently deleted.** A superseded host file moves to the attic with a manifest line. A
    removed feature leaves a dated tombstone in the spec and retired matrix rows. Only junk that can be
    regenerated may be deleted, listed and approved by the person first (SPEC INV-7, A-4, A-9).

11. **Verify by deed; show the real thing.** "Works" is said only after running it and seeing the result.
    Otherwise it is labelled an assumption. What the human sees is real data in its real render.
    Synthetic data is for your own checks alone, always carrying the literal label `SYNTHETIC`. Never
    show a bare file path in place of the thing itself.

12. **The human's gates are the human's.** Irreversible moves, authored-content moves, publishing, pushes
    where the host says so, taste and domain wording — proposed with a recommendation, executed on their
    word. And only what is genuinely theirs is asked; everything else proceeds and is reported.

13. **A claim needs its primary source.** Anything asserted as fact — what the code does, what happened,
    who decided — rests on evidence you can point to: an owning `file:line`, a commit, a command just run
    and its output. Your memory, a worker's summary, and a document's prose are leads, each confirmed
    against that evidence before you rely on it. Before attributing a decision to the human or calling a behaviour "by design", read the actual source
    line (rule 5's raw-output clause is this rule's delegation face). No source at hand ⇒ say "not sure",
    then check before asserting.

    One attribution stands apart: a decision recorded as the human's. The human's word is the pack's
    highest authority, so every gate, prover, and agent takes it on trust and
    questions it never. That is the very reason a sentence carrying it must name the exchange it came
    from, a date at minimum that a reader can go to and check (SPEC INV-207). A sentence the seat reasoned
    out for itself is written in the pack's own voice, claims no human authority, and stays challengeable
    by every reader. An autonomy grant authorizes the seat to decide, and the seat owns that judgment as
    its own. The seat never records that judgment as the human's word. Recording a decision as the person's adds
    an anchored entry to `DECISIONS.md`, the set the pack reads back to the person. The pack shows that set on the
    asynchronous touchpoint cadence [INV-205, INV-206], so the person reads what the pack believes they decided and
    strikes what they never said. The mechanical check `guardrails/check-authority-anchor.py` hard-blocks
    an unanchored entry on a decision record. It also reports the surfaces that change often, where an
    attribution first gets written. But the read-back is the load-bearing defence, turning the person's
    own eye into the check. A text gate alone cannot catch a fabrication that carries a plausible date.
    An invented ranking invents its date just as easily.

14. **A found defect is a sample of its class — go find the class, sweep the look-alikes.** A bug, a stale
    name, a jargon string, a design inconsistency: before calling the fix done, name the pattern behind the
    instance abstractly. That pattern is the kind of mistake — a scope too narrow, a missing guard, an
    assumption that holds in one place and fails in the neighbour. Then search the whole repo and every
    user-facing surface for that kind, and fix all siblings in the same change. The search goes looking
    for the siblings
    not yet seen, past the one instance already reported. One instance reported means the whole class is
    owned, and the human never finds the second instance by eye. A confirmed bug carries three more moves
    before it closes, which with the class hunt above make the four moves the pipeline names. Check the
    architecture, since a structural cause updates `ARCHITECTURE.md` and a cluster in one area reads as an
    architecture smell. Check the spec, since a spec silent on the broken behaviour is the real defect,
    fixed first so the prover can flag it, and the code then lands under it. And escalate to
    the human when the class boundary needs his read, since the agent never guesses the boundary. The
    full four-move law lives in
    `skills/build-pipeline/SKILL.md`, under its bug entry, and in the spec at INV-124. A rule superseded at a broad scope is the same class. Its restatements at narrower scopes go stale the
    instant the broad rule changes: a host's `CLAUDE.md`, a project's playbook copy, an installed skill.
    So the same change that supersedes the rule sweeps those copies. It never leaves a narrower scope
    quoting the old rule. Each working skill applies this in its own domain. The
    pipeline sweeps code and surfaces on every bugfix, and the prover sweeps the document with its class lens before writing a
    point finding.

15. **The door is named before any code.** Every request states its entry point — feature · bug ·
    refactor · docs-only · skip — in one intake line beside size and priority, before the first line of
    code. The same line names the **work-kind** — product · infra · skill · prose — which is what the
    request builds. The door picks which pipeline steps run, and the kind picks the form each running
    step takes; the per-kind table's one home is `skills/build-pipeline/SKILL.md`. At landing, every
    door-granted step has applied or been stood down by name in the report. So every skip is named and
    every kind touches the safety net (SPEC T-16, INV-22).
    Hard tripwires decide, never mood. Five of them send a request to the feature door: a new
    user-visible surface · new persistent state · a new
    interaction on an existing surface · a spec `[target]` mark on the touched surface · behaviour no spec
    clause backs ⇒ FEATURE, however casually asked. The tripwire
    verdict outranks a casual label
    (queue-cutting stays with the bug door alone). The door re-fires mid-work. The moment running work is
    about to create a surface or state its door doesn't grant, stop, reclassify, and continue by the right
    door. Casual asks are routed, never refused, and never hand-built past the pipeline. (SPEC T-12, INV-16)

16. **A prototype stays a sketch.** Exploring is legal, but a sketch lives fenced. It takes its own
    `prototype/` home and a PROTOTYPE label in the form its kind can show (screen banner · `_prototype:
    true` field/header · first-line CLI banner · name/header marker). It is never wired into or linked from a
    production surface, and it is shown to the human only under its label. A request merely to see or try a
    thing may be
    sketched; a request to have it in the product is a feature — unclear which ⇒ one plain question
    (rule 1). Promotion is not a merge: the feature enters at the spec step; the sketch is evidence, its
    code holds no rights. Opening a prototype home is a repo write that belongs to the assigned senior
    alone. A worker doesn't open one on their own, and an outsider's route is an inbox wish instead. (SPEC E-17, INV-17)
17. **Irreversible means gone, not merely public.** Truly irreversible actions — spending money,
   deleting data, sending to a person or an audience you cannot unsend from — always stop for the
   human's word, whatever the proactivity mode. A push to your own repository is NOT irreversible (it
   reverts); it rides the mode and the project's own push gates. When unsure which side an action is
   on, treat it as irreversible and ask. The criterion is "can we get back to before, ourselves,
   losing nothing?" (2026-07-05: money yes, deletion yes, a push no.)

18. **One name-collision law.** A new file whose name is taken differentiates in two moves, the same
   everywhere in the pack: first the semantic mark its home already defines — the attic prefixes the
   source directory, and a decision file already carries its project and date. Then, where the name is
   still taken, a numeric ordinal
   `-2`, `-3`, … goes before the extension. Never overwrite, never a third scheme. True concurrency can
   race one name, as the inbox does with two sessions, one slug, and one moment. There a short session
   token joins the semantic mark, so a collision may cost a rename and never a lost file. (Audit
   2026-07-05: the attic had no answer for a second collision, and the attic and the inbox each spoke
   half a law.)

19. **The problem ledger — workshop noise is owned, never re-suffered.** Operational noise is written
   down the moment it fires: a flaky
   test harness, a missing dependency, an environment error, a tool misbehaving. This is the workshop
   around the work, and the product's own defect is a bug that takes the bug lane instead.
   Grep the host's `.live-spec/PROBLEMS.md` for the signature. Not listed → one WATCHED line
   (signature, date, one line of context) and keep working. That write replaces the silent retry.
   Listed → the second occurrence gets an owner at that moment: a queue row (OWNED) or the human's dated
   AGREED NON-PROBLEM. Only the human's word can write the second of those, never the agent's. The agent
   recommends, writes the recommended
   owner now, and the ask rides the batched report. A third recurrence arriving unowned is a defect of
   the method itself, past that day's noise. It goes to the pack's own queue (from a host window: one inbox file).
   A recurrence on an owned entry appends its date and changes nothing else. The landing that closes an
   OWNED entry's row flips it to SOLVED (SPEC E-24, INV-23).
   **A known, owned problem never blocks unrelated work (SPEC INV-56)**. It is parked, held by the
   ledger line, the owning row, or an
   expected-red note. Every unrelated lane keeps rolling. Hand-fixing loops cap at the second-occurrence
   law above. A defect with
   a named mechanical owner is serviced in BATCH. Instances are fixed silently where the fence catches
   them, and one ledger append comes at the session's end, with no per-instance ceremony interrupting the
   work. A new bug still preempts, and this governs only the known, owned problem.

20. **Search for a skill before reinventing (SPEC INV-65).** At a project's setup, meaning founding or
   adoption's orient beside the founding questions, scan the installed skills and the catalogs you
   can reach for ones matching the project's kind and its crafts. Propose the fit list with a
   recommendation, and the human's word picks. At a struggle, the next attempt waits one search, since
   an existing skill or checklist may already own the failure class. A struggle is a ledger entry's
   second occurrence, a taste artifact rejected twice, or any returning failure family.
   The find is adopted or rejected
   by name, recorded where the struggle lives. Borrowing practice: invoke a found skill as it ships;
   paraphrase folded lessons and credit the source by name; verbatim text only under its license,
   notice kept.

21. **Human-facing prose is drafted by a clean writer (SPEC INV-84).** When a human will read the
   text, prepare a plain brief that states the facts, names the intended reader, and lists the
   register laws. Then hand it to a fresh writer session that has no package rules loaded. Let the
   writer produce the prose, review the returned draft against the brief, and land it, and
   do not write the prose yourself. Apply this to new text and to any page you are already editing. The
   unit is the section your edit touches, and a whole page is redrafted only on the human's word. Text you
   type live in chat stays your own words under the register laws. This rule binds the durable prose
   a human returns to, so settled text is left alone until a human rejects a specific page or
   your edit opens that page.

22. **Every process converges on its goal (SPEC INV-98).** Name the goal up front as an artifact
   the work can be held against — a frozen norm, an exemplar bank, a failing test, a written
   acceptance. A paraphrase cannot serve as the goal. Measure every iteration against the goal
   itself; a proxy never replaces the goal, and measuring against a proxy is where a look-alike
   appears. The distance to the goal only shrinks. A reached level locks by a mechanism, because attention
   alone holds nothing across sessions. Four such mechanisms are a norm template,
   a conformance test, a lint floor that only grows, and a cap that only ratchets down. A deliberately divergent stretch — exploration, a labelled
   prototype (rule 16) — is legal only when named and bounded by its convergence point. The
   principle's chapter lives in the owner's private playbook repository, in its `PLAYBOOK.md`, which
   a reader outside the project cannot open. The pack's own first
   teeth are the norm-conformance rows and the convergence-lock tests (rows 216/217). (The
   owner's word, 2026-07-10: convergence covers every process and every kind of artifact — there
   is a goal, and we walk toward it, always.)

23. **A behavioural rule that breaks mid-turn twice earns a live channel (SPEC INV-108).** A standing
   behavioural rule keeps its normative home in a once-read file — the loader, a profile, a skill's
   text. When the rule breaks mid-turn a second time despite that home, it earns a live channel that
   same moment. The channel is one of two: an every-prompt hook line that reminds at the decision point,
   or a mechanical after-the-fact check that turns the suite red. Record the pick where the rule lives. The once-read
   homes stay the normative homes; the live channel only carries the rule to the moment it is needed.
   Prose in a once-read file loses to mid-turn momentum, and attention alone holds nothing across
   sessions. This rule is the convergence principle's hand for behaviour (rule 22), kin of rule 19's
   second-occurrence law. Here is the worked proof. The routing rule lived in once-read files since June and
   broke mid-turn. It broke until the every-prompt hook line and the mechanical after-the-fact check
   landed (rows 253/254, 2026-07-12). That is the same cure that killed invented clock stamps. The 1.1.0 audit's
   once-read walk is this law's first sweep.

24. **The process stations are kind-abstract; a project declares its concrete layers and proofs (SPEC
   INV-135).** The entry impact read, the footprint categories, and the test ladder are stations the pack
   states once, and the stations are kind-abstract. Each project kind fills them with its own concrete
   layers and its own concrete proof kinds. The three footprints generalize past code. A
   presentation-only change touches what the audience meets and nothing behind it. A single-module change
   stays inside one owned layer. A cross-cutting change moves a shared law or several layers at once.
   The layers themselves are the project's own. A codebase splits frontend, backend and store; a photo
   site content, rendering engine and deployment. A promotion campaign splits message, channels and
   assets; a music project arrangement, stems and mix. The proofs follow the same shape, each kind
   naming the rungs its test ladder really has. A codebase proves with unit tests and rendered or pixel
   checks. A photo site proves with a byte-diff of the baked output and the owner's eye-walk. A
   promotion campaign proves with a register lint and the owner's review.
   Each project kind is recorded at founding as `project.kind`
   (SPEC INV-36) in the host profile. It declares its concrete layers and its concrete proof kinds there,
   as one `project.layers` line and one `project.proofs` line. Both stand as rows of the
   package-defaults table below. A profile that records a kind with neither is
   incomplete, flagged at adoption the way an unbacked surface is. The per-kind fill is then the
   project's own ratchet, since the footprint check and the test-level check read the categories the
   project declared. `ARCHITECTURE.md` carries the per-kind footprint-and-proof table. Both spec-author
   and test-author read the declared layers and proofs, never assuming a code layer. One abstract
   station each kind fills with its own layers and proofs is what makes one method fit every window.
   A method written only for code would fit a photo site badly.

25. **The orchestrator reads to decide; discovery reads go to workers (SPEC INV-137).** The lead's context holds only
   what orchestration needs — the human's words, the decisions taken, the distilled results workers hand
   back, and the few anchors the lead must cite. Reading a file to understand or design it, past a glance, is
   itself work, so it routes like any work (rule 5). The lead dispatches it to a reader — a search-and-locate
   pass or a read-and-distill brief — and reads the distillation the worker returns. The raw file bodies
   stay with the worker.
   A glance is bounded: one small file, or a handful of targeted lines whose result is itself the deliverable (a
   version string, one clause to quote). Past the glance, dispatch. The duty binds only the reads done to
   discover or understand, where a distillation is the right return. A read to verify a claim or settle a
   decision stays with the lead. Checking the real artifact and re-reading a primary source are the
   lead's own hands (rules 11, 13). A dispatched verification returns the raw evidence the lead
   re-checks (rule 5). The leanness is load-bearing: a lead filling its context with source it could
   have had distilled loses the room to hold the whole arc. Its judgment degrades as the context
   bloats. Workers locate their own anchors from the brief, so the
   lead never reads a file merely to hand a worker its anchors (rule 5, SPEC INV-69). The brief's own read of
   the files it will change (SPEC INV-53) composes with this rule. That read is
   dispatched to the reader whose distillation returns the per-file lines the brief records. For a small
   edit, it is a decide-read the lead makes directly and keeps bounded. The discipline is held by no
   one's memory but by a record. The delivery report's delegation accounting names the reads dispatched
   beside the work delegated (SPEC INV-103, INV-137). So a session that slid into reading-to-discover
   shows it.

26. **A project kind also declares design principles the verify pass runs (SPEC INV-136, INV-139).** Beside
   the concrete layers and proof kinds a project kind carries (rule 24, SPEC INV-135), a kind names a set of
   checkable design principles. The frontend kind's interactive-overlap rule and its legibility floor are
   two of them. The verify feel pass reads the
   declared principles and runs each in the medium's own form. A principle no suite can green falls to the
   human's own eye-walk. This rule is the base home the design-principles invariants own; their full
   statement, the per-kind design-principles table, and its starter sets live in `ARCHITECTURE.md`.

27. **The orchestrator decides what it can decide, and surfaces only what it cannot (SPEC INV-143).**
   It can decide and report three things. First, a mechanical step. Second, a value a
   proven artifact already determines [INV-121]. Third, a sensible default it can pick and name [INV-70]. It
   surfaces a decision to the human only where the decision genuinely cannot be made without them. Three
   cases qualify: a taste call, a trade-off no artifact settles [INV-121], or a change to the definition
   of correct.
   It never parks derivable work on the human's queue to avoid deciding [INV-4]. The posture holds on
   every session, including one resumed from its files after a memory wipe [INV-48].

28. **A periodic full audit catches the drift no lint names (SPEC INV-145).** Two layers guard the
   living documents against rot. The continuous lints — the register lint, the provenance-narrative
   check, and their kin — run on every push and hold each drift class already known, the moment it
   reappears.
   Beside them, a full audit runs on a landing-count cadence. It runs every ten landings since the last full
   audit [default; a host may set its own count on its word, SPEC INV-70]. At that point the pack reads
   the living documents whole, in the milestone gate's form (SPEC M-1). That whole-read is the full spec and
   architecture re-prove, the design review, and the doc-compaction sweep. It runs even where no
   milestone falls due, so a drift class nobody has named yet is caught
   before a human meets it late. The count is read from the landing commits in git history, and a
   milestone gate resets the counter since it already runs the whole-read. An audit is adversarial by
   nature: a whole-read that sets out to break the work, refute its claims, and find its holes (SPEC
   INV-46).

29. **A deferral must justify itself, or the item is the seat's to do (SPEC INV-152).** A backlog item
   carrying a needs-the-human's-word marker is re-tested by derivability every time it is touched, at its
   first writing and at every touch after. Three things carry such a marker: a queue row held for his
   word, a `NEXT_STEPS.md` line, and a decision a setup script leaves open. Sometimes the answer pins to an existing artifact: a base rule, a spec
   sentence, the architecture, an approved prototype, or an already-answered decision [INV-59]. The
   item is then the seat's. Do it, cite the artifact, and drop the marker [INV-121, INV-143]. Where it needs
   a fact no artifact holds — a taste, a policy, or an act irreversible outside git (rule 17) — it is
   the human's, and the marker stands. Writing such a marker requires naming that human-only fact. A
   marker that cannot name it defaults to the seat's. A marker that cannot say why the item belongs to
   the human is itself the finding. This is the no-homeless-item control — rule 27's
   decide-what-it-can-decide posture applied to a backlog item — binding the orchestrator seat whatever
   tier holds it. It is the twin of a request matching no kind in the closed door set (rule 15, SPEC
   INV-151). One routing principle covers both: every
   incoming thing routes to the home whose declared sentence governs it. A thing that pins to no
   home is itself the finding [INV-153]. Two mechanisms hold this rule.
   The mechanical one is `guardrails/check-deferral-marker.py`. It reds a commit when a parked item in the
   resume file or a decision page names no reason category — taste, policy, irreversible, or
   device-feel — the same shape as INV-155's retry-plugin grep. The delivery one is the deferral line of
   the chat-law hook at `hooks/chat-law-hook.sh`. It
   re-fires the derivability test at the moment a marker is written or the harness's own
   `AskUserQuestion` prompt is opened, so the re-test fires right at the point the leak would happen. It
   reminds and cannot block, the way the chat laws are always delivered (SPEC INV-28).

31. **Agents talk on exactly two channels, and a message earns its passage (SPEC INV-183, INV-189).**
   Several agents on one person's projects generate noise the moment they can talk to each other. This
   rule keeps the channel quiet while the necessary thing still crosses. An agent is a
   project window carrying its own tree, queue, gates, contracts, a standing mission, and a card of its
   own. A skill is a capability any window loads, and it dies with the session [E-31, INV-182]. Before
   acting on anything that might not be its own, an agent scans for cards and reads the owning agent's
   agent card, the `.live-spec/agent.md` in that agent's own tree [E-32, INV-184]. Then **exactly two channels** carry
   everything between two agents: the receiver's inbox for a one-shot request to change something, and a
   published contract for a recurring read. A reply rides the inbox in the other direction, so the count
   of two holds. Co-location changes the transport's speed and leaves the contract untouched, and a
   remote agent reaches the other through git alone [INV-112].

   The laws below hold the quiet, and each is a way of routing a thing to the home that governs it [INV-153].

   - **A message names the sender's own blocked work, in the message.** The named work is a real row, a
     real failing step, a real thing the sender cannot finish while the receiver's zone stands as it
     does. A message that cannot name such work is never sent. That rules out curiosity,
     tidiness, and the thought that a neighbour might want to know. Exactly
     two situations justify a message. Either the sender is blocked by the receiver's zone as it stands,
     or the sender has hit a fault
     in that zone and carries the evidence. The zone's owner is presumed competent and informed, so nothing
     that owner's own instruments already see earns a file [INV-189]. The mechanical check is
     `guardrails/check-earned-message.py`. It runs at the intake sweep and judges each deposit there;
     the sweep declines an unearned one at the door, so no human reads it. A deposit is recorded on
     arrival and never blocks a push (the owner's word, 2026-08-07 11:19: a request is written down,
     and nothing stands in the way).
   - **A referral travels back to whoever asked.** A question from another agent's zone is answered by
     naming that zone, and the zone's owner receives nothing from a referral. A human asker is answered
     in chat and costs one sentence. An agent asker is answered along the reply road as its message's
     terminal state. Forwarding a neighbour's question to the owner of its zone is the defect this law
     names, and the forwarder's own work stands on none of the answer [INV-190]. A question that pins to
     no artifact, and on which no work of the sender's stands, is dropped; holding it was itself the
     defect [INV-191]. A referral that points at a zone which does not own the question is named as a
     wrong referral, where the exchange loops back over the same pair. The two-crossing cap does not
     absorb it. `guardrails/check-wrong-referral.py` reds such an exchange on a fixture and rides
     the suite, staying off the push chain [INV-225, INV-196].
   - **Data never travels as a message, and a contract publishes nothing by default.** A consumer wanting
     numbers reads the neighbour's published artifact [INV-188]. Every field in that artifact leaves the
     producer's tree on the owner's explicit permission, recorded with its date and its author. How a
     neighbour's product happens to be built grants no permission, and a field with no recorded
     permission stays home. Credentials never cross under any permission [INV-185].
   - **An agent recognises a neighbour's zone on its own.** An agent may meet a fault or a lack in something
     another agent's zone owns: a rule of the method, a shape a neighbour ships, a field a contract
     lacks. It then scans for cards, finds the owner, and takes the channel that fits. The owner
     naming the road afterwards carries no fact the agent lacked, so his line is an acknowledgement of a
     thing already done. An agent that waits to be told has made the owner its router [INV-195].
   - **One question crosses between two agents twice, and the third crossing goes to the owner.** Every
     hop of a refer-and-re-send loop can pass its own law while the exchange manufactures traffic, so the
     bound is two, counted by the exchange's identifier. The third crossing is named in the sender's own
     status report as a zone question the two could not settle. The human-decision withdrawal loop
     already takes this shape [INV-196, INV-130].
   - **A concern no agent's zone owns goes to the pack, and the work never stalls on ownership.** A
     question no work stands on is dropped [INV-191]. A concern is a different thing: real work whose
     owning zone does not exist yet. It goes to the pack's inbox, and the pack answers who owns it — an
     existing agent, a new agent the owner ratifies, or a skill. Zones may overlap and no agent is
     forced to carve a disjoint one. The work never waits on the answer. An agent meeting an unowned
     concern does the reasonable thing now, in whatever tree can hold it, and marks that work
     provisional. The re-home lands later as ordinary pipeline work, cheap and retroactive, where a stall
     while ownership is settled is what this rule prevents [INV-197].
   - **A capability another agent's zone owns is taken through one of the two channels.** Building
     a local copy of a neighbour's capability is the violation the cards exist to prevent. The
     copy drifts from its original the day after it is made, and the two owners then answer one question
     two ways [INV-194]. An agent-initiated message stays a proposal until the owner ratifies it. An
     owner-initiated message is the one kind that carries the owner's authority, and relaying changes a
     message's carrier while leaving its authority where it started [INV-193].

32. **A release's number answers what taking it costs a host (SPEC INV-217).** The number reports what a
   host that vendored the previous version must do to take this one.
   A **patch** fixes a machine to hold a law already stated: no new capability, no changed contract, and the
   host takes it and does nothing. A **minor** grows what a host may adopt in a backward-compatible way: a new capability, a new law, or a
   new gate. The host takes it by re-running its catch-up walk [INV-91],
   with nothing it already carries rewritten. A **major** is a release a host cannot take without changing
   what it already carries. Four things earn it: a reworded rule the host vendored, a renamed or removed
   surface a host depends on, a changed adoption or catch-up step, a moved law that forces host action.
   A major ships its dated
   `MIGRATION.md` chapter [INV-91]. The default is a patch. It is raised to a minor
   or a major only where the release earns the higher tier. This is a judgment the releasing session makes and states,
   **held by no machine**. The minor-versus-major call reads meaning a gate cannot, so it **stays a stated
   rule the session holds**, the same standing as a design-review finding that never blocks a
   lane [INV-141]. The owner asked for this guidance on 2026-07-17 ~15:45. Every release before it
   picked its number by the session's feel, with the rule written nowhere.
   Three worked examples come from the pack's own history. The 1.0.0 migration chapter renamed the host's pack
   folder and swept
   its references, and a host cannot take it without acting, so it is a **major** by this rule. The inbox
   remote arm of roadmap row 247 added a capability a host adopts by re-running the walk with nothing
   rewritten, a **minor**. A fix that makes a gate finally hold a law already written is a **patch**.
   The 2.0.0 release is the
   boundary case. Its own migration chapter records "Host action: none", so by this rule it reads as a minor,
   and its major number marked significance by the session's feel. It keeps its published number as this
   cited boundary case. The rule is written now so the next release reads its number off the host cost.

33. **The authoring seat does not adversarially certify its own work (SPEC INV-237).** The seat that
   authored a change drafts and accepts it, and it never provides that change's own adversarial
   certification. A head marinated in the authoring context is blind to the blind spot it just wrote. Two
   carriers hold it. A release's adversarial pass — the full re-prove at the release gate [INV-116] — is
   authored by a fresh seat. That seat is a differently-contexted head briefed from the primary sources.
   It is the same freshness the verify audit already demands of its checker (SPEC INV-46).
   The 2.7.0 release ran its adversarial pass
   in the context that authored the new lenses, and so
   never turned a brand-new lens onto the skill body that introduced it. And a newly added lens or rule is
   run against the very document that introduces it before release, which is self-application, with the
   release record
   naming the result. A release gate may require a dated clean-context review record naming a seat other
   than the release's. Whether the review was truly clean-context is a process fact no gate fully sees.
   So the gate checks only that the record exists, is dated to the release, and names a different seat.
   That is the mechanical floor under a discipline the seat holds. The owner's word, 2026-07-18, after a fresh web
   review caught self-referential defects the in-context 2.7.0 prover missed.

34. **A deferred item's own state is re-derived from the code before its work resumes (SPEC INV-247).** A
   resume file and a queue row record a past moment. The technical problem statement a deferred or
   queued item carries — how the code it touches works — can go stale as that code moves on. So the first
   act of resuming such an item is a freshness check of its own subject against the shipped source. Read
   the code the item touches, confirm the problem the row describes still holds, and re-derive the item's
   real current state before designing anything on it. It is the resume-side twin of rule 13's primary
   source and of the architecture step's pin read from a command just run. Rule 8 re-reads versions at a
   breakpoint, and the queue-take re-scan re-reads a deferred row's revisit trigger [SPEC INV-129].
   This rule re-reads the item's own internals. So
   a session never designs a fix from a stale model of code that has since moved, and an item already handled
   is caught before the work restarts. The owner asked the pack to hold it, 2026-07-20.

35. **A session's record is read at both ends by an agent that did not live it (SPEC INV-302).** A session
   that lived the work reads its own record badly. Worked failure: on 2026-07-28 a session wrote its
   handover from memory. It named a question as still waiting for the owner, and the owner had answered
   it earlier that day. So each
   end of a session is read by a fresh agent. That agent works from a session extract: the person's own
   turns, each with its timestamp. `scripts/session-extract.py` pulls those turns out of one transcript,
   and its own header names where the transcripts sit and which traps a reader meets there.
   The extract goes to a scratch directory, since a transcript holds private conversation. At the close,
   the fresh agent writes the session handover from that extract. The session that lived the work writes
   no handover of its own. A handover is a file under `docs/handovers/` whose name ends in
   `-handover.md`, and it says where it was read from in three lines: transcript, extract, written by.
   At the open, a fresh agent reads the previous session's extract. It lists every decision the person
   made, each with its timestamp. It compares that list against `DECISIONS.md` and `NEXT_STEPS.md`. A
   decision missing from both goes to the seat before work starts.
   Both ends stay a discipline the seat holds. A script read the handover's three lines until
   2026-08-09, and the live-spec pack withdrew that script after finding no error the script had
   ever caught.
   A session's opening writes no committed artifact for a script to read. The owner asked for
   this reading as a standing process, 2026-07-28.


## Work that belongs elsewhere

Reserve this file for the pack's own work: a session outside the pack uses a general style guide instead.
Never write host- or person-specific values here — those live in profiles, and this file holds only
package defaults and the rules themselves. The scope is pack-internal by the owner's decision (recorded
2026-07-16). The base serves the pack's skills and the projects that adopted the pack. It is no
general-purpose rulebook for unrelated sessions. That decided sentence closes the recurring scope
question for good.

## The settings ladder

How the pack behaves is a **named setting** living in one of four nested scopes, and a setting belongs to
the scope it describes. Broader values are inherited downward until a narrower scope overrides them on
the human's word. Resolution reads from the narrowest scope out — **session beats host beats personal beats
package default** (SPEC E-13):

| Scope | Home | Holds settings about |
|---|---|---|
| package defaults | the table below, in this file | the pack out of the box |
| personal profile | `~/.claude/live-spec/profile.md` | the person — follows them across every project |
| host profile | `<host>/.live-spec/profile.md` | this one project |
| session | the human's live word, held only in the conversation itself | the conversation running right now |

An override exists only as a written line in its profile file. Setting one leaves a dated journal note
in the home it governs, keeping every divergence visible (SPEC INV-14). The session scope is the one exception.
It lives only in the human's spoken word and dies with the conversation. The agent never writes it
anywhere on its own. Making it outlive the session is a promotion into the profile it describes, on
the human's word, journaled like any other override. Proactivity mode and trust are written
only on the human's word, and the agent may propose but never set them (SPEC INV-9). Profiles are re-read at the same
freshness points as skills (rule 8). A profile line the current pack does not recognize is ignored out
loud, named once in the session's next report as a visible, ordinary skip, never an error.

**The profile is found or founded at setup (SPEC B-3)**. The pack looks for the personal profile before
the founding questions resolve. It looks at founding, at adoption's orient, and at the first session on
a new machine or with a new human. Found ⇒ loaded and said aloud. Absent ⇒ an offer to create it from
`templates/profile.template.md`, which sits in the pack's own tree. The human tells about themselves and
may name sources for the pack to read and propose from. Every line lands on the human's word, and a declined proposal is dropped (INV-9
caps it: mode and trust move only on their word). A declined step runs the session on package
defaults, said aloud, and the offer returns at the next setup. A worker session never onboards
anyone, since its brief carries its setting lines (SPEC ACT-3).

The personal layer has one home, the profile. The machine-global instruction file (for example
`~/.claude/CLAUDE.md`) is a thin loader. It carries the pointer that loads the profile, plus only the
bootstrap lines that must hold before
any pack file is read. It is those bootstrap lines' one home, and the profile never restates them (SPEC E-16).

### Package defaults

| Setting | Default | A profile may say | Card |
|---|---|---|---|
| `language.docs` | English — docs, commits, code, artifacts | another docs language | visible |
| `language.chat` | mirror the human's language | pin one (e.g. Russian) | visible |
| `proactivity.mode` | ask-at-max — surface forks, wait on taste calls | max-proactive: proceed on recommendations, batch questions | visible |
| `trust` | low — human word before outward moves | raised only by the human (INV-9) | internal |
| `prover.cadence` | FULL pass before every MINOR bump; CROSS-LINK on every surface add | tighter (e.g. live-spec itself: before every push) or looser, recorded | internal |
| `worker.tiering` | router proposes the cheapest sufficient tier; senior may override, logged | fixed tier per size class (SPEC D-2) | internal |
| `checkpoints.home` | `<host>/.live-spec/checkpoints/`, gitignored | another host path | internal |
| `spec.file` | `PRODUCT_SPEC.md` — the host's product spec file; every pack guide reads "PRODUCT_SPEC.md" as this file under its recorded name | a host that adopted under its own name keeps it, recorded as one host-profile line (e.g. `spec.file: SPEC.md`); a rename may be offered together with its pointer sweep, never forced (SPEC INV-90) | internal |
| `work-kind.host-default` | none — each wish's kind is called at intake | a host with one usual kind names it as the intake default (SPEC T-16) | internal |
| `project.kind` | none — asked at founding and at adoption's orient, always the human's answer, never profile-seeded or inferred (SPEC INV-36) | the host's own kind: book · backend service · static site · fullstack app · CLI · skill pack · a custom kind through the queue; seeds project-wide defaults, never overriding an explicit line; updated on the human's word the moment the project outgrows it, journaled | visible |
| `project.layers` | none — declared at founding beside `project.kind`, naming this kind's concrete footprint categories (SPEC INV-135) | this project's own categories, one line: a codebase's frontend/backend/store, a photo site's content/rendering-engine/deployment, a campaign's message/channels/assets; the per-kind footprint-and-proof table in `ARCHITECTURE.md` is the scaffold each founding fills | internal |
| `project.proofs` | none — declared at founding beside `project.kind`, naming this kind's concrete test-ladder rungs (SPEC INV-135) | this project's own rungs, one line: tests and rendered checks, a byte-diff and an eye-walk, a register lint and the owner's review; a `project.kind` recorded with neither layers nor proofs is incomplete | internal |
| `project.design-principles` | none for a kind with no visual surface; a visual kind (e.g. frontend / fullstack app) declares its set at founding, seeded from that kind's starter table in `ARCHITECTURE.md`'s per-kind design-principles section (SPEC INV-136) | the project's own checkable design rules, one line, extended past the starter set through the queue; a visual kind recorded with none is flagged the way a kind recorded with no layers or proofs is (SPEC INV-135) | internal |
| `design-sync` | off — a host with visual components may switch it on (recorded profile line, SPEC E-18, INV-14) | on: a landing's declared components sync to the team's design project, every sync behind the human's publish gate (rule 17) | internal |
| `feedback-upstream` | off — the outbound feedback arm is silent; a host switches it on with a recorded profile line (SPEC INV-161, INV-14) | on: on a rare strong reaction the pack offers, with the human's explicit yes, to draft a private upstream note to the pack's authors into `outbox/`; never sends, delivery the human's own step | internal |
| `lanes.cap` | 3 — up to three build lanes roll at once without asking (SPEC T-18, INV-214) | a leaner plan lowers it, a richer one raises it, recorded with the plan it fits; the owner's 2026-07-06 value of three lives in his profile | internal |
| `budget.pressure` | full — every check runs at full strength; the economy ladder's rung (SPEC T-19, INV-40); a rung moves the pace and never the standard, stated under this table | lean or tight, only on the human's word (a session's word or a profile line; asked — or the default told — at a project's setup, founding or adoption, alongside `project.kind`; the agent proposes a rung when money/time pressure is named, never sets one); each rung's legal sheds and the never-bend list live in the economy-ladder section of `PRODUCT_SPEC.md` — every taken shed is named in the delivery report, and an explicit host line outlives any rung | visible |
| `far-tier.surface-cadence` | at most once every 14 days — how often the far backlog may surface itself unasked in the status report (SPEC INV-223, roadmap row 403); the report records the last surfacing in a dated marker, and a second offer inside the window is the defect the report-shape check reds | the person's own cadence, moved by his word like any default, and recorded in his profile | internal |

The Card column says what the settings card renders. A `visible` row appears on the card. An `internal` row is workshop machinery the card leaves out, reaching the reader only as a recorded host-profile line in the card's project-rules part. The card's own law lives in `PRODUCT_SPEC.md` (INV-87).

A profile file is plain markdown: one `setting: value` line per override, each with a trailing date and,
when it narrows the defaults, one line saying why. Settings not listed above may be proposed as wishes, and the
table grows through the queue like everything else.

### A budget moves the pace, and never the standard

A rung of the economy ladder sets how fast and how cheaply the work runs. The standard the work is held
to stands outside every rung. A check the method calls for runs at whatever the plan costs. A fresh
clean-context agent is raised every time the method asks for one. Four such asks are an adversarial
review, a cold reading, a release re-prove, and a deep spec-and-architecture audit. Economy is bought
from pace, from batching, and from a cheaper tier on mechanical work. It is never bought from a
dropped check. The full never-bend list this rule joins lives in the economy-ladder section of
`PRODUCT_SPEC.md` (SPEC INV-40, R220). The owner's word, 2026-08-05 at 22:52: quality never suffers,
whatever else does. At 22:12 he had named the smaller plan. He asked that a fresh worker the method
needs be raised on it all the same.

> The pack, whole: **live-spec-base** holds the shared rules and defaults · **spec-author** writes the spec ·
> **product-prover** reviews it · **design-reviewer** judges the design behind it · **build-pipeline** ships the change · **test-author** derives the matrix and writes the tests · **communicator** makes the human
> exchange land · **feedback-intake** brings what comes back to its home · **feedback-collector** offers a rare private note up to the authors · **text-audit** reads a text as a stranger and fixes where they stop · **publish** sees the work out the door, owing its kind's checklist.
