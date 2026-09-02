---
name: live-spec-base
description: Load before using any live-spec pack skill: director, spec-author, product-prover, design-reviewer, architect, build-pipeline, test-author, communicator, feedback-intake, feedback-collector, text-audit, publish. Load it also before briefing a worker that will write files, or to resolve shared rules and settings. It is the one home for the shared rules — twenty-two rules in the body, each stated as one instruction. It carries on-demand reference modules under `references/` — the glossary, the worked examples, the settings ladder, the worker-restore wording, the session handover, and rule-origins, which holds each rule's citation, history, justification, and worked example — each opened only when its own kind of question needs resolving.
metadata:
  version: 6.1.0
---

# live-spec-base — one rulebook, twelve working skills

The pack's shared working rules live here, once. A working skill opens by naming this base and the
version it was written against. It then references these rules and elaborates only its own domain.
The twelve working skills are named in the closing roster below. A second full statement of a shared
rule inside a working skill is drift (SPEC INV-13). It is a defect to fold at the next milestone,
never kept for convenience. One rule is carried whole instead by every skill that briefs a worker.
The worker-restore sub-rule under rule 7 rides each brief in one wording. `tests/test_worker_restore.py`
reds a home that states it in words of its own (SPEC INV-299). Communicator teaches how to speak
plainly; that we speak plainly is this file's sentence. Used standalone, outside the pack, a
working skill still stands: its pointer here reads as plain advice.

## Where the paths and the codes point

This file names paths in two trees, the pack's own machinery and a host's documents, and two code
kinds, an `INV-x` code and a roadmap row number. Where each resolves is recorded once, in
[references/glossary.md](references/glossary.md). Open that module when a path or a code needs
resolving, and not before.

## The words this file uses

Each term this file's rules deal in is defined once, in one module beside this file:
[references/glossary.md](references/glossary.md). It holds every term from *the pack* to *an agent
card*, each with the `PRODUCT_SPEC.md` entry that stands behind it. That module's entry for **the
seat** records the senior, the orchestrator, and the lead as the source's other names for the one
acting session; the rules below use the one name the glossary keeps, the seat.

Open that module when a term is being resolved, and not before.

## The rule of thinking, above all the rest

**Every incoming item is a symptom, and the answer owed is a rule about its class**. One phrase, one
file, one number, one incident — whatever arrives, it arrived as an instance of something. Name the
class, state the rule for it, and find the other live instances. The instance that was pointed at is
then repaired as a free consequence. A change that repairs only the instance has answered nothing,
because the next instance is already on its way. The rule holds at every channel an item arrives
through. There are three such channels: a person's feedback, a finding the agent makes itself, and a
message from another agent. The three are one filter.

This is a rule of thinking, and it governs every rule below it. The class-shaped answer was first
noticed inside a code change, in the bug-to-sibling-sweep discipline the director's own class-hunt
reference now carries; the thinking here generalizes it to everything.

Its own worked failure, the guard built as a list of literal patterns, is written out in
[references/worked-examples.md](references/worked-examples.md). A law naming a class is held by a
judge that reads meaning. If the answer to a class is a list, the design is wrong.

## The shared rules

Each rule's background — citation, history, justification, worked example — lives in
[references/rule-origins.md](references/rule-origins.md), opened only to dispute or amend a rule.

Rules 11, 14, 15, 18, 19, 20, 21, 23, 28, 30, 32, 33, 34 and 35 were cut whole from this rulebook; each
number is retired and stays open. Rule 30 went first, on its own decided cut. The 2026-08-26 cut carried
the rest of them: each covered by neither an eval fixture nor an executable script — a wish, not a rule,
per PLAN.md step 7 — and moved out to `attic/live-spec-base-unbacked-rules-2026-08-26.md`, whole, with
its own manifest line. Every other rule below keeps the number it already carries.

1. **Ask, never guess.** Ask, or mark `⟨DECIDE⟩` with a recommended pick, only where the artifacts
   leave a gap open (SPEC INV-4, INV-5, INV-12). Never invent intent, and never ask what you can
   decide or verify yourself. Where a proven artifact already settles it — the architecture, the
   spec, or the invariants — derive the requirement and cite the section instead, offering no fork.
   This is the read-the-doc twin of ask-never-guess: that half forbids inventing an answer, this
   half forbids offering a choice the documents have already made (SPEC INV-121). —
   `guardrails/check-deferral-marker.py`.

2. **Plain words carry the meaning; the code trails, quietly.** Write plainly; never let a code, row
   number, worker name, model name, or coined feature name carry the meaning; in chat the anchor
   trails the sentence in parentheses, in a document it sits at the line's end in square brackets,
   and it never opens a line. A term or metaphor coined in the docs language is never
   loan-translated into chat — the **no calques** rule: say what actually happens in natural
   chat-language words, the original term free to trail like any anchor. —
   `hooks/code-anchor-scan.py`.

3. **One surface = one name, everywhere.** One thing, one name; two names for it breaks every
   cross-check that assumes one. — `guardrails/check-one-name.py`.

4. **One canonical home per fact.** One canonical home per fact; repoint every reference the same
   session a doc moves or is superseded. — `check-doc-rotation.py`.

5. **The seat orchestrates; each unit routes to the cheapest tier that passes its brief (SPEC
   INV-69).** The seat — whatever tier holds it — orchestrates, briefs, and accepts the work, and
   it does not do the grunt itself. Every unit of work is routed PER UNIT: the trigger is judgment
   against mechanical, and the tier is proposed for that unit. And a judgment step is never routed
   down. Size is a weak hint only, never the decider. Only raw output is evidence, and the worker's
   prose is only a lead. So a worker's green is a lead the seat ACCEPTS by re-checking it, never on
   trust. A large or high-stakes landing earns an independent fresh-context checker beyond that
   re-check (SPEC INV-46). Every override of a proposed tier and every failed-acceptance escalation
   is logged, proposed tier → chosen tier → why (SPEC INV-69). —
   `guardrails/check-tier-refusal.py`.

6. **Every long or delegated piece of work keeps a persistent checkpoint.** Keep a live checkpoint
   file (done / in-progress / next) in `.live-spec/checkpoints/`; updated as the work runs, so a
   cut-off resumes from disk. A landing that ships a checkpoint's items flips that checkpoint to
   its closed state in the same landing, so a returning session never reopens finished work. Red at
   a pause is itself the checkpoint.

   - A checkpoint whose items all live in git history is stale by definition and reads as a resume
     defect (SPEC INV-107).
   - A note recording a live background worker records three things: the worker's id, its briefed
     write-set, and the liveness checks a resuming session runs before touching those files or
     spawning a sibling — the write-set's file times over a short window, the worker's heartbeat, and
     one message to its id.
   - The heartbeat is a fixed-interval touch on the worker's own checkpoint file, ~60 s [default],
     stale past ~2 min [default].
   - Never frame a worker's output as finished while the worker may still run (SPEC INV-76). Before a
     memory wipe, prefer halting the workers or letting them finish, so the next session starts
     single-writer; say plainly when a worker dies with a closed window or a sleeping machine.
   - The human's leave-word extends this rule to every open lane at once (SPEC INV-95; communicator
     carries the closing walk).

   — `scripts/checkpoint.py`.

7. **The concurrent-edit fence, before every write and every commit.** Re-check `git status` and
   HEAD against what you last read; stop and re-read if the tree moved. An unassigned repo is
   read-only, apart from a new wish file in its inbox — this binds every skill that writes shared
   files, adoption among them (SPEC INV-10, INV-11).

   The parallel-lanes rules sit underneath the fence.
   - Lanes roll unasked up to the profile cap (`lanes.cap`, default three [E-13]) (SPEC T-18).
     One more opens only on the human's asked word. Every write to a document the lanes share
     serializes under the single PEN, one lane at a time.
     That document is a convergence point the pen reconciles at integration, so sharing it never
     makes the lanes wait on each other.
     Co-location alone never pulls two rows into one lane (SPEC INV-49).
   - **The lane-open act.** The session opens a lane by running `scripts/open-lane.sh`.
     The script's own header states what it expects on disk. First, the row→in-work flip is
     committed to main under the pen. Second, the branch `lane/<row>-<slug>` is cut from that claim
     commit into its own worktree. Third, the lane goes to a worker whose brief names the branch.
     The act reads the profile cap [E-13] and refuses a lane past it (SPEC INV-214, INV-49).
   - **Worktree isolation on overlap.** So worktree isolation is the default when two lanes'
     write-sets overlap. A shared file one lane holds open is never written by another (SPEC
     INV-105).
   - **Brief-time disjointness** — before spawning another concurrent writer, the seat confirms its
     brief's write-set is disjoint from every already-running writer's brief, or gives it an
     isolated worktree at brief-time (SPEC ACT-3, INV-11).
   - A worker never restores a tree with git; wording in
     [references/worker-restore.md](references/worker-restore.md) (SPEC INV-298).
   - **One row per landing commit.** A landing commit carries exactly one row's delta (SPEC
     INV-39).
   - **A prior-context worker.** A background worker from a prior context is a concurrent writer
     too. It survives a memory wipe, and the process list is never proof of death. It stays a
     foreign writer until verified by rule 6's resume checks — the write-set's file times, the
     heartbeat, and one message to its id — before a second worker starts on a shared tree, or
     until the first replies that it halted (SPEC INV-76).
   - A tied concurrent claim breaks on each session's stable identity (SPEC INV-117).

   — `guardrails/check-worker-restore.py`, `scripts/open-lane.sh`.

8. **Freshness: versions are re-checked at every breakpoint.** Re-check modification times of
   installed skills, packs, and profiles at every breakpoint; re-read a changed file before
   continuing; journal old → new (SPEC A-7, M-7). — prose-only, no dedicated check.

9. **History lives in the journal; docs travel with the change.** Log every movement's dated reason
   in `JOURNAL.md` the same session; keep spec, next-steps, and plan stating only current truth,
   each entry dated and timed. — prose-only, no dedicated check.

10. **Nothing is silently deleted.** Move a superseded file to the attic with a manifest line;
    tombstone a removed feature; get human approval first except for regenerable junk (SPEC INV-7,
    A-4, A-9). — `guardrails/check-board.py`, `check-doc-rotation.py`.

12. **The human's gates are the human's.** Propose irreversible moves, authored-content moves,
    publishing, gated pushes, and taste or domain wording with a recommendation; execute only on
    the human's word (rule 27 draws the line). — plausibly `check-broad-kill.sh`, not confirmed.

13. **A claim needs its primary source.** Ground every asserted fact in evidence you can point to —
    a file:line, a commit, a command's real output; say "not sure" and check before asserting.

    - The human's word is the pack's highest authority, so a decision recorded as the human's
      needs an anchored `DECISIONS.md` entry naming its dated exchange; the seat's own reasoning
      carries no human authority (SPEC INV-207). An autonomy grant authorizes the seat to decide,
      and the seat owns that judgment as its own — never recording it as the human's word. The pack
      shows that set to the person on the asynchronous touchpoint cadence (SPEC INV-205, INV-206).
    - An instruction carries the authority of whoever gave it, and the seat names that source —
      person's, tooling's, or unknown; where a tooling line and the person's own standing word
      conflict, the person's standing word decides.

    — `guardrails/check-authority-anchor.py`.

16. **A prototype stays a sketch.** Fence every sketch in `prototype/` under a PROTOTYPE label,
    never wired into or linked from production; promotion is not a merge — the feature enters at
    the spec step, and the sketch is evidence, its code holds no rights; only the assigned senior
    opens a prototype home (SPEC E-17, INV-17). — `guardrails/check-prototype-fence.sh`.

17. **Irreversible means gone, not merely public.** Stop for the human's word on any truly
    irreversible action — money, data, an unsendable audience.
    A push to your own repository is NOT irreversible; it rides the mode and the project's own
    push gates. When unsure, treat it as irreversible. — `guardrails/check-runaway-child.py`.

22. **Every process converges on its goal (SPEC INV-98).** Name the goal up front as an artifact
    the work can be held against — a frozen norm, a failing test, a written acceptance. A
    paraphrase cannot serve as the goal. Measure every iteration against the goal itself; a proxy
    never replaces the goal. A reached level locks by a mechanism, because attention alone holds
    nothing across sessions. A deliberately divergent stretch — exploration, a labelled prototype
    (rule 16) — is legal only when named and bounded by its convergence point. The principle's
    fuller chapter lives in the owner's private playbook repository, in its `PLAYBOOK.md`. —
    `tests/test_convergence_rule.py`.

24. **The process stations are kind-abstract; a project declares its concrete layers and proofs
    (SPEC INV-135).** The entry impact read, the footprint categories, and the test ladder are
    stations the pack states once, and the stations are kind-abstract. Each project kind declares
    its concrete layers and its concrete proof kinds at founding, recorded beside `project.kind`
    (SPEC INV-36) as one `project.layers` line and one `project.proofs` line. —
    `tests/test_founding_layers_proofs.py`.

25. **The seat reads to decide; discovery reads go to workers (SPEC INV-137).** Keep the seat's
    context to orchestration only — the human's words, the decisions taken, the distilled results
    workers hand back. Reading a file to understand or design it, past a glance, is itself work:
    the seat dispatches it to a reader and reads back the distillation. A glance is one small file
    or a few targeted lines whose result is itself the deliverable. Workers locate their own
    anchors from the brief, so the seat never reads a file merely to hand a worker its anchors.
    The brief's own read of the files it will change (SPEC INV-53) composes with this rule the
    same way; the delivery report's delegation accounting names the reads dispatched beside the
    work delegated (SPEC INV-103, INV-137). — `tests/test_orchestrator_read_discipline.py`.

26. **A project kind also declares design principles the verify pass runs (SPEC INV-136, INV-139).**
    Declare each kind's checkable design principles and run each in the verify pass, in
    its own medium's form; fall to a human eye-walk only where no suite can green it. —
    `tests/test_design_principles.py`.

27. **The seat decides what it can decide, and surfaces only what it cannot (SPEC INV-143).**
    Decide mechanical steps, values a proven artifact already determines (SPEC INV-121), and
    sensible defaults it can pick and name (SPEC INV-70), on your own. Three cases qualify for the
    human instead: a taste call, a trade-off no artifact settles, or a change to the definition of
    correct — a threshold, a policy, a domain wording and the feel of a real device in the
    person's own hands each land in one of the three. It never parks derivable work on the human's queue to avoid deciding (SPEC INV-4). The posture holds on every session, including one resumed from its files after a memory wipe (SPEC INV-48). — `tests/test_seat_acts_by_default.py`.

29. **A deferral must justify itself, or the item is the seat's to do (SPEC INV-152).** Re-test
    every needs-the-human's-word marker for derivability at writing and every touch; if an artifact
    already answers it — a base rule, a spec sentence, an approved prototype, or an
    already-answered decision (SPEC INV-59) — do the work, cite it, drop the marker (SPEC INV-121,
    INV-143). An unnamed human-only fact defaults to the seat, and a thing that pins to no home is
    itself the finding, the twin of the pipeline's closed door set (SPEC INV-151, INV-153). —
    `guardrails/check-deferral-marker.py` reds a marker naming none of the four grounds (SPEC
    INV-155); `hooks/chat-law-hook.sh` re-fires the check on every marker or open question (SPEC
    INV-28).

31. **Agents talk on exactly two channels, and a message earns its passage (SPEC INV-183,
    INV-189).** An agent is a project window with its own tree, queue, and card; a skill is a
    capability any window loads and dies with the session (SPEC E-31, INV-182). Use exactly two
    channels between agents — the receiver's inbox for a one-shot request, a published contract for
    a recurring read, reached through git alone for a remote agent (SPEC INV-112) — after scanning
    for an owning agent card, the `.live-spec/agent.md` in that agent's own tree (SPEC E-32,
    INV-184). Each law below routes a thing to the home that governs it (SPEC INV-153).

    - A message names the sender's own blocked work, in the message, or is never sent (SPEC
      INV-189).
    - A referral travels back to whoever asked; forwarding to the zone's own owner is the defect
      (SPEC INV-190). A question that pins to no artifact is dropped (SPEC INV-191), and a referral
      to a zone that does not own the question is named as a wrong referral (SPEC INV-225).
    - Data never travels as a message, and a contract publishes nothing by default; read the
      neighbour's published artifact — only a permitted field leaves the tree, never a credential,
      and no permission ever moves one (SPEC INV-188, INV-185).
    - Recognise a neighbour's zone on your own and take the fitting channel; waiting to be told
      makes the owner your router (SPEC INV-195).
    - One question crosses twice; the third goes to the owner as a status-report line (SPEC
      INV-196, INV-130).
    - An unowned concern goes to the pack's inbox; the work never stalls on ownership (SPEC
      INV-197).
    - Take a capability another zone owns through one of the two channels, never a local copy of a
      neighbour's capability (SPEC INV-194). An agent-initiated message stays a proposal until the
      owner ratifies it; an owner-initiated one carries the owner's authority, and relaying changes
      only the carrier (SPEC INV-193).

    — `guardrails/check-earned-message.py`.

36. **Who the person is, by default, and what changes that.** Write by default for a non-technical
    reader: no gate letters, requirement codes, file:line pins, or script names in what they read.
    Deepen the register only when they show that depth themselves. Offer a richer view; never
    impose it. One item, one name, on every surface. — `guardrails/check-language-rules.py`.


## Work that belongs elsewhere

Reserve this file for the pack's own work: a session outside the pack uses a general style guide instead.
Never write host- or person-specific values here — those live in profiles, and this file holds only
package defaults and the rules themselves. The scope is pack-internal by the owner's decision (recorded
2026-07-16). The base serves the pack's skills and the projects that adopted the pack. It is no
general-purpose rulebook for unrelated sessions. That decided sentence closes the recurring scope
question for good.

## The settings ladder

How the pack behaves is a **named setting** in one of four nested scopes. Resolution reads from the
narrowest scope out — **session beats host beats personal beats package default** (SPEC E-13).

The ladder itself is one module in this same package:
[references/settings-ladder.md](references/settings-ladder.md), beside this file. It holds the four
scopes and their homes. It holds the package-defaults table every setting is a row of. It holds the
rule that a budget moves the pace and never the standard.

Open that module when a setting is being resolved, proposed, or recorded, and not before. Nothing in
it is optional. Nothing in it moved elsewhere: the module is the ladder's one home, read on demand
rather than carried by every session that touches no setting.

> The pack, whole: **live-spec-base** holds the shared rules and defaults ·
> **director** reads the human's message first and decides what it is, before any of the rest ·
> **spec-author** writes the spec ·
> **product-prover** reviews it · **product-prover-pack** binds the external prover to the pack ·
> **design-reviewer** judges the design behind it · **architect** writes or updates the
> architecture from the proven spec · **build-pipeline** ships the change ·
> **test-author** derives the matrix and writes the tests · **communicator** makes the human
> exchange land · **feedback-intake** brings what comes back to its home ·
> **feedback-collector** offers a rare private note up to the authors ·
> **text-audit** reads a text as a stranger and fixes where they stop ·
> **text-audit-pack** binds the external audit skill to the pack ·
> **publish** sees the work out the door, owing its kind's checklist.
