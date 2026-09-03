# live-spec — Product Spec (v6.1.0, 2026-07-23)

This document is the living statement of what live-spec is right now. The body is a flat list of requirements, each stating one rule of the method. A requirement carries a Context block, a one-sentence User Story, and acceptance criteria grouped into named cases; a requirement whose heading carries a `[feature: F-...]` tag is a person-facing scenario — what the reader does and what the reader sees. Edit history lives in `JOURNAL.md`; this spec states what is true today.

live-spec takes any request a person submits, of any size and at any moment, breaks it into story-sized pieces — one user story to a piece — and runs each piece through the same pipeline, one stage at a time, each stage checked by its own gate before the next, until the piece reaches a delivery and ships tested. A machine enforces the process at every step, every claim earns a test, and nothing ships until that test passes.

Bracket codes like `[E-1]` and `[INV-27]` trail a criterion and point to the rule's home in the project spec; a reader can ignore them, a maintainer follows them. The letter before the number names the kind: `E-` an entity, a numbered part of the product; `INV-` an invariant, a numbered rule that must always hold; `T-` a transition, a numbered change of state; `M-` a rhythm rule, a numbered recurring routine; `A-` an adoption step; `B-` a bootstrap step; `ACT-` an actor; `C-` a composition-axis rule; `D-` a recorded decision; `S-` a header rule; and `F-` a feature, which a scenario heading carries as a `[feature: F-...]` tag. A range such as `[T-1..T-7]` cites its whole run of codes. A `[target]` marker on a line of its own marks a feature or leg that is promised but not yet built, and a `[default]` marker names a value the agent set that the human may retune. A `[GAP: ...]` line under a criterion records a place the source states a behaviour and leaves its judge, its measure, or its scope unstated; it is the honest output for a real hole, never a filled-in guess.

The keywords *when*, *while*, *if*, *then*, *where*, and *shall* are set in lowercase italics and carry their standard requirements meaning: *shall* states a duty, *when* and *while* open a situation, *if* and *then* open a condition and its result, and *where* scopes a duty to the setting it holds in.

The foundational nouns of the method — request, pipeline, spec, architecture, invariant, guardrail, suite, session, journal, queue, movement, delivery, delivery report, footprint, profile, and resume file — carry the meanings the base method glossary gives them, at `skills/live-spec-base/references/glossary.md`. The glossary below defines, in one place, every domain noun the thirty assembled sections introduce; a term appears once, under one name, and the criteria use it with that meaning.

## Glossary

- **act** — what a person did in one message, read as one or more of the seven kinds the first read decides between.
- **action trace** — the ordered record of which tools the seat called during one turn, read from the tool-use events in the transcript.
- **activity generation** — the stranger-monitor's dedupe unit: the state of a shown work's outside comments, those not the monitor's own markers; a new outside comment advances the generation, and an item surfaces at most once per generation.
- **adoption** — attaching the pack to a project already running, run as an ordered set of phases.
- **adversarial read** — a fresh-context audit set on breaking a decision's case, run before the decision lands, that closes by bringing the decision to the owner with its findings and a recommendation.
- **agent** — one project window that carries its own tree, queue, gates, published contracts, a standing mission, and an agent card, each of which outlives any single conversation.
- **agent card** — a host's self-describing file (`.live-spec/agent.md`) stating its name, mission, zones, published contracts, and inbox address.
- **announced self-compaction** — the session's own act, said aloud at a safe breakpoint, of pruning its working context while carrying its live lines forward into the summary.
- **architecture format** — the format-family member the architecture document is written in: a preamble, then a body of node sections, then the architecture's generated tables; it inherits the family's shared laws from the spec format and adds only the architecture-particular rules, its definition at `docs/architecture-format.md`.
- **architecture node** — one named unit in the architecture document carrying one responsibility and one name, owning the spec facts it implements and pinned to its place in the code.
- **architecture Reference** — the generated section mapping each spec anchor a node owns to the node names that own it, built by script and output only.
- **architecture-reference gate** — the mechanical check that reds an architecture Reference differing from a fresh build or disagreeing with the nodes' owns fields.
- **artifact inventory** — the test matrix's opening section naming every file the reader receives, each carried by at least one row asserting it at the rendered level.
- **attic** — the host's append-only archive folder (`attic/`). A superseded file moves here with one manifest line and is kept for good.
- **attribution line** — the single `made with live-spec` line a built-with publication carries on its landing surface, naming the pack version the project runs.
- **base skill** — the pack skill that holds the shared rulebook and the default settings, stated once, so every working skill points at one home rather than restating them.
- **beat** — one narration line marking one unit of the work's progress; a stretch with no beat is beatless, and the heartbeat line covers it.
- **blocking finding** — a finding that a criterion cannot be understood or acted on as written; it stops the section from passing.
- **board row** — one line of the work board standing for one task, live while in hand and kept once it closes.
- **breakpoint** — a point where a movement ends and session memory can be wiped with no loss, its live state replaced, a dated journal entry added, and the work committed.
- **brief** — the written instruction set a worker runs from, carrying its files, its steps, its clock, and its stop conditions.
- **cadence** — the one number a producer owns, stating how often it regenerates its published artifact.
- **capability** — one thing a window can do; a capability holding durable state, a standing mission, and a zone of its own is an agent, and a capability living wholly inside one session is a skill.
- **capture echo** — the line the sweep posts back on an item's source, naming what was heard, its route, its name, and its row.
- **card** — one work board row rendered as a task: its echo-name, the line saying what the change does, its chips, and the details layer behind it.
- **card scan** — the live scan that reads the agent-card files under each of its roots and treats every card it finds as an agent.
- **carrier** — what makes a rule of this document happen, one of four: a command the machine runs, an instruction a session reads and follows, a surface drawn when somebody asks for it, or nothing yet.
- **catch-up** — the sequence that brings an already-adopted host onto the pack's current version.
- **catch-up walk** — the ordered set of steps a session walks to run catch-up on an adopted host.
- **checkpoint** — a saved point of work that can be resumed from, written under `.live-spec/`. A planned-work checkpoint is one grouped unit of planned work in the resume state, carrying a status the landing that ships its items flips to closed; a worker's checkpoint is the file a worker keeps under `.live-spec/checkpoints/`, holding its resume point and touched on a fixed interval as a heartbeat.
- **chip** — one short labelled fact standing on a card, such as its estimate, its placement tag, or its state.
- **class hunt** — the search a confirmed bug drives before it closes: name the defect abstractly, find every sibling of that kind, and fix them in one change.
- **closed vocabulary** — the rule that every domain noun in the document holds exactly one glossary entry.
- **cold reader** — a fresh reader who reads a changed section with zero project context.
- **cold-reader panel** — the set of cold readers a changed section is read by in one round.
- **Communicator** — the pack's working skill that owns the human-facing exchange; it resolves the settings ladder to the working contract before each report, showing, or question.
- **compaction pass** — the milestone routine that prunes a working skill's restatement of a base-skill rule once it lags behind the base, one skill at a time.
- **composition axis** — one angle a stateful surface's behaviour can vary along, stated as one question about the surface. A floor axis is one of the kind-independent set every stateful surface answers; a kind-owed axis is one a project's kind adds beyond the floor.
- **comprehension gate** — the two-layer check a changed section passes: the mechanical layer, then the cold-reader panel.
- **concurrent-edit fence** — the check, run before every shared write or commit, that compares the repository's `HEAD` and tree state against what the session last read at its start, blocking a commit when either has moved, and clearing again once the session re-reads and accounts for the change.
- **conduct judge** — the model call that reads a turn's action trace against the standing orchestration laws and reds a violation after the turn.
- **confidence read** — a design review finding's label of one of two values, confident or likely, saying whether the deciding fact lives in the spec text or in the person's intent.
- **config-health check** — the check that diffs each installed copy of a pack artifact against its source in the pack and reds a missing or drifted copy, naming the one fix; it runs inside the suite and the push gate.
- **content contract** — the engine's public list naming every place a concrete instance plugs in. Each entry has a handle and a test proving the engine works without that instance's value.
- **conversion delivery** — the one delivery that converts the whole spec document to the requirements format; every gate this section names arms in it.
- **coverage validation** — the checklist that closes the matrix derivation, walked to confirm every spec anchor, artifact, and node carries the rows it owes.
- **craft name** — the display name a running step's worker is shown by on the work board, standing with the craft's icon; the fixed set of craft names and icons lives in the work board's source file.
- **crafts** — the professions a project's own work already draws on, such as a product manager, an architect, a test engineer, or a senior developer, matched against the project's kind when the fit list is proposed.
- **criteria set** — the set of criteria a spec document holds at one moment, each keyed by its code and its criterion text.
- **criterion** — one numbered line stating one rule — a single situation with the duty that holds in it — with its code anchor trailing at the line's end.
- **cross-link mode** — the prover's focused pass at a surface add, scoped to the new surface's seams, carrying one mandatory whole-document step: it sweeps the document for enumerations and universal quantifiers and re-verifies each against the surface set including the newcomer.
- **decision archive** — the directory `docs/decisions/` where a decision page is filed once its answer comes back.
- **decision card** — one question on a decision page, opening with what each option changes for the person and carrying the recommended answer.
- **decision page** — one surface that carries several open questions to the person together, opening in its own window while the rest of the work continues.
- **decision sheet** — the written understanding accepted work carries before any working skill is called, held as a section of that work's own checkpoint; the requirement that owns it names the fields it holds.
- **decision-set record** — the file `DECISIONS.md` that shows the person the decisions the pack believes the person made, each naming the exchange it came from.
- **declared-laws home** — the one place the spec lists its cross-cutting laws, each carrying its per-surface clause or dated exemption and the net that enforces it.
- **defect** — a prover finding where a stated invariant is violated, a spec claim is false, or a required invariant is missing; it blocks the design until it is folded.
- **deferral test** — the intake check on whether a wish's work may be deferred, run before any row is parked.
- **delegation accounting** — the line a delivered queue row carries naming how its work was delegated, or why the seat kept it.
- **delta classifier** — the pre-push gate that reads the delta record and diffs the old criteria set against the new one.
- **delta kind** — one of the four words a delta record assigns to a touched code: *new* (a code the body did not carry before), *sharpen* (a code whose criterion text changed), *retire* (a code the body no longer carries), or *scenario-only* (a code whose criterion text is unchanged and only its placement moved — the named case it sits under or the prose around it).
- **delta record** — the per-code declaration a spec-touching delivery carries, naming each touched code as new, sharpen, retire, or scenario-only.
- **departures board** — the status-report view, read live off the queue's open rows at report time, that names every rolling train's station and the row a waiting lane sits behind; the view itself keeps no file of its own.
- **description field** — the authored home of a code's plain statement: the criterion the code trails carries the code's rule, and an entity code's definition lives in the glossary; the generated code-to-location table carries locations only.
- **design principle** — a checkable design rule that a project kind's products must hold, run by the verify pass in the medium's own form.
- **design project** — the team's own design project, an external destination where rendered cards go for human review.
- **design review** — the pass that reads a proven spec and judges its design, grouping the elements a person acts on and checking each group for behaviour parity.
- **design-sync** — the optional machine that mirrors the components a delivery declared to the team's design project for human review.
- **detached-work cadence** — the rule that a background or delegated run expected to pass about two minutes opens with a start line, lands a beat about every two minutes or at each stage, and closes with a done digest.
- **document provenance** — the composition axis adoption adds: where a spec claim came from. A claim is native when it was written fresh under the pack, and re-engineered when it was recovered from documents a project held before adoption.
- **domain noun** — a noun naming a thing the product deals in, as against a word of ordinary English.
- **done-claim** — a statement that a piece of work is finished, settled by walking its evidence rather than answered from memory.
- **Done-when** — the written acceptance a queue row or one of its legs carries, naming the observable state that closes it.
- **door** — the intake classification that places a queued wish at one entry point of the pipeline, one of feature, bug, refactor, docs-only, or skip, decided before any code is written and kept separate from the wish's size. A request that never becomes a queued wish — an ask merely to see or try a thing — takes a separate entry lane, the labelled-sketch door, held outside this five-way set.
- **earned message** — one file a sender agent deposits in a receiver agent's inbox, naming the sender's own work that earned it.
- **echo-name** — the short name the capture echo posts back on an item's source, so the person can find the row the item became; the same name is the task's own short name on the work board's card.
- **economy ladder** — the setting `budget.pressure`, whose three rungs — full, lean, and tight — name what rigor a tight budget may shed.
- **engine** — in an engine-and-instance pair, the generic reusable mechanism. It ships as its own host, public by default, tested on its own generic fixtures.
- **entity** — a numbered part of the product a code can name, as against a rule of behaviour.
- **evaluative phrase** — a phrase that passes a judgment — broken, larger than, worth, and their kind — which a criterion pairs with the judge that decides it and the inputs judged by.
- **expected-red note** — a recorded note that a check is held red for an understood, stated reason, which keeps a known owned problem parked without blocking unrelated work.
- **expensive decision** — a decision that would cost more to unwind than to make.
- **facet** — one aspect of a feature's design, ending as a written spec sentence that is decided or tagged as a default.
- **far tier** — the queue's tier for a row kept with no revisit trigger and no plan to run, held so the thought is never lost; the rows it holds are the far backlog, and the report of runnable work names the tier in one line rather than listing its rows.
- **feature map** — the product's map of features, constituted by the spec's scenario sections and the architecture's nodes together, with no separate map document.
- **feature-coverage trace** — a second traceability layer above the test matrix, keyed to the project's primary unit, that maps each unit to the node implementing it and a test exercising it.
- **feedback** — anything a person hands back to the project, at any size, any moment, through any channel. The person is usually the host's human; when a host's product has its own users, their reports travel the same road once a session receives them.
- **feedback ledger** — the append-only file `FEEDBACK.md` kept beside the queue at the host root. It holds one dated line per handed-in item whose route has no other home.
- **feedback-collector** — the skill that notices a strong reaction and offers to carry a short note up to the pack's authors.
- **feedback-intake** — the skill that receives a handed-in item and routes it to the one home its kind owns; the intake half of the exchange, where communicator carries work out and feedback-intake carries what comes back.
- **field evidence** — a person's reaction to a shipped feature, recorded as one feedback-ledger line that cites the feature's scenario.
- **finding** — one recorded item a cold reader returns on a section; a note-level finding is recorded and does not stop the section.
- **first read** — the reading of a person's message that decides which acts it carries, done before anything answers it or changes a file.
- **fit walk** — the intake interrogation of how a feature sits in the person's path, scaled to the wish's kind.
- **founding** — the start of a fresh host, where the shaping questions are answered in the new spec's opening and the templates are copied in.
- **founding-question set** — the versioned set of questions founding asks a host. It grows as the pack learns what a founding host owes; a host records which version it answered.
- **freshness check** — the check that compares each installed skill's version against the pack's and re-reads any skill whose version moved.
- **gap line** — the line that records a source hole under the criterion it touches, in the form `[GAP: ...]`.
- **gate** — a check that must pass before work proceeds; a red gate stops the work at that step.
- **generated index** — the code-to-location table a script builds from the body criteria at freeze; it is output only.
- **generation stamp** — the moment a published artifact records as the time it was generated.
- **glossary** — the block at the head of a spec document that defines every domain noun once.
- **grant** — one recorded permission a session or remote seat holds for one repository: a push grant to deposit and push into it, a read grant to clone and pull a private producer's repository.
- **green line** — the single line a gate prints when it passes.
- **ground** — the reason a message earns sending, drawn from a closed set of three.
- **harness** — the runtime that runs a session and its tools, the environment the agent executes in; it owns the machinery between sessions, among it the socket plumbing whose listener the direct channel waits on.
- **harvested row** — the queue row that an answer lands in when the session harvests it there.
- **heartbeat** — a narration line on a long beatless stretch, naming what is grinding and why the stretch runs long.
- **host** — one project the pack attaches to. Each host holds its own spec, queue, journal, and `.live-spec/` folder.
- **input-capability axis** — the composition axis for the input a surface is used through, such as touch or a fine pointer. Its values are the input capabilities a device carries, which co-occur on one machine.
- **installer** — the pack's one install script (`install.sh`). It copies the pack's skills onto a machine and backs up any existing copy first.
- **instance** — in an engine-and-instance pair, the concrete product a real person uses today. It holds the content and plugs into the engine.
- **intake** — the pipeline's first station, where a wish already captured as a queue row is classified: the classifier reads its size, priority, door, and work-kind and states them back in one line.
- **judge** — the named actor a criterion states as deciding one of its evaluative phrases.
- **landing** — the act of one piece of work reaching the repository's shared truth as one commit under the pen. The delivery is the shipped work; its landing is the commit that puts it into the shared truth.
- **lane** — one build train a session rolls through the pipeline.
- **lane branch** — a lane's isolated copy, a git worktree holding a branch named for its queue row.
- **leg** — one of the separately-accepted parts a multi-part row still carries, each with its own Done-when acceptance.
- **lens** — a named check the prover or the design review walks a document with, each testing one concern (the architecture lens, the cognitive-load lens).
- **level ladder** — the ordered set of test levels a matrix row pins to, running string, then document-text, then browser-computed, then pixel.
- **local reach map** — the file that maps a diff's file classes to the checks each class must run, read by the local pre-push hook as a scoped subset of the full check set.
- **local-only diaries** — the journal, the resume file, the queue, and the migration chapter, the host-local files that hold candid attribution and process history no publish ships.
- **loop** — an autonomous recurring run the session performs with no person present, working in iterations and sleeping between them.
- **map note** — the row field, written `map:`, that records the intake verdict of how a wish maps onto the product: changes feature X, new feature, or restructure.
- **matrix Reference** — the generated section of the test matrix mapping each spec anchor to the matrix rows that cover it, built by script and output only.
- **matrix-reference gate** — the mechanical check that reds a matrix Reference differing from a fresh build or disagreeing with the body rows.
- **matrix row** — one criterion of the test matrix: a single trigger-and-response sentence stating both what a fact does and what it must never do with its spec anchor trailing, and beside it a pinned test level, an owning test, and a status.
- **matrix row lint** — the mechanical check that reds a matrix row pinning no test level or stating no never side.
- **measurement family** — the deferred machinery, still unbuilt, that reads, scores, and aggregates feedback signals such as field evidence.
- **mechanical lint** — a free script check the comprehension gate runs before any reader: the vocabulary check, the one-name check, the weak-word check, or the style lint.
- **method version** — the pack-and-skill version set a piece of work was carried out under, read from the host's installed set.
- **migration chapter** — one dated, versioned entry in the migration guide (MIGRATION.md) stating the host-side steps a pack release requires.
- **milestone** — a rhythm point where the whole spec and architecture are re-proven, the design review runs, and the full gate list completes; periodic routines such as the skill-eval re-run and the problem-ledger compaction fold in at it.
- **milestone gate** — the whole-spec pass that re-proves the spec and the architecture, runs the design review, and completes the full gate list.
- **monitor** — the scheduled script that bridges each open issue a stranger filed into one committed inbox file under the reserved stranger source word, naming its source.
- **named case** — one bold line naming a situation, followed by the criteria that hold in it.
- **named reference** — an internal item's stable code paired with a plain one-sentence description of what the item does and the problem it solves.
- **narration** — the running account of work as it happens, said in the roadmap's terms between the capture echo and the delivery report.
- **need-by** — the moment a message states as the time by which it needs its terminal state.
- **net** — one hook or guard that watches for a stated condition and fires when it holds. A guardrail is one kind of net.
- **net-liveness meter** — the shared instrument that records how often a net ran and how often it fired, and reads the two numbers back so a silent net is caught by the numbers.
- **never side** — the half of a matrix row's sentence stating what the fact must never do, written with the literal word *never*.
- **never-bend list** — the set of protections that holds at every rung of the economy ladder and does not bend.
- **new-criteria budget** — the byte sum a spec-touching delivery declares for the criteria it adds under the *new* kind.
- **node block** — the group of matrix rows owned by one architecture node, headed by the node's name, standing as the matrix's case grouping.
- **node reader** — the one reader that reads the node shape — the node names, each node's owned-anchor set, and each node's pins — read through by every consumer of the architecture; the sibling of `guardrails/specformat.py`, the spec format's one reader.
- **node section** — the section one architecture node stands as, headed `### [node: <name>]` and carrying four fields: the responsibility, the owns list of spec anchors, the pins list of file-and-line places, and a notes line for what the other fields cannot hold.
- **non-goal** — one sentence in a spec-delta naming what the change deliberately leaves out, so a deliberate absence reads as a decision.
- **norm** — an approved prototype frozen as the binding record of a surface's look and feel, kept as a dated copy under `docs/norms/`.
- **norm pointer** — the `norm: <path>` reference a spec clause carries at its line end, pointing at the frozen norm artifact its behaviour is checked against.
- **offline window** — a narration line before a stretch that needs nothing from the person, naming that the person may step away, an honest range for how long, and what the person is needed for at its end.
- **once-read-rules sweep** — the audit walk that reads the problem ledger for a standing rule that broke mid-turn despite living in a once-read file such as a loader, a profile, or a skill's text.
- **open leg** — a leg of a multi-part queue row whose own Done-when acceptance has not yet been met.
- **orient** — adoption's opening phase, in which the system reads every existing document before touching anything and answers the founding questions about what it found; its digest and inventory land in `.live-spec/adopt/`.
- **outbox** — the gitignored per-host directory `outbox/` that holds an upstream note until the person delivers it; it never rides a push.
- **pack** — the shipped live-spec method: its skills, its document and suite templates, and its guardrail scripts. It carries a version.
- **part** — one file of a document's body, standing beside the other parts and read only because the core's parts map names it.
- **parts map** — the table in a document's core naming its part files in the order they are read; the core is that order's one home, and a document whose map is empty is the core file alone.
- **pen** — the single write-lock a repository holds, under which one delivery reaches the repository's shared truth at a time.
- **pen-stage** — one span in which a lane holds the pen for one indivisible piece of shared-truth work, from taking the pen to its landing, never cut mid-edit.
- **personal profile** — the human's own settings file on the machine, holding their languages, how to address them, what they do, and their own vocabulary. The intake glossary's *profile* is the host's own project settings; this is the machine-wide file the person owns.
- **placeholder-stub list** — the checklist of stub shapes a claimed fact's substantiveness is checked against: `TODO`, `FIXME`, placeholder, lorem, a hardcoded sample, and an empty body.
- **priority** — the wish's urgency, normal unless its row carries one of two marks, critical or quick win.
- **priority bubble** — the one way priority reorders the lane: a marked wish jumps ahead of the fresh queued wishes, visibly, straight to the queue head. The intake classification writes the mark — critical or quick win — on the wish's row; an unmarked row carries normal priority.
- **proactivity mode** — the per-person setting for how far the agent acts on its own before asking, held in the personal profile and moved only on the human's word.
- **problem ledger** — the per-host file `.live-spec/PROBLEMS.md` that records the workshop's own recurring operational noise as a signature with its dated occurrences and a status, born on its first entry.
- **prod surface** — any part of the shipped product a user meets.
- **product** — the software the project owns and ships to its user.
- **project kind** — what a host's product is, named from a curated vocabulary: book, backend service, static site, fullstack app, CLI, or skill pack. It is recorded in the host profile and seeds the host's defaults.
- **project layers** — the concrete parts a project kind decomposes into. They are the host's own footprint categories.
- **proof kinds** — the concrete checks a project kind proves its work with. They are the host's own test-ladder rungs.
- **prototype** — an exploration of an idea kept as a sketch, living fenced off in its own clearly named home such as a `prototype/` folder or branch, so nothing in the shipped product reaches into it.
- **prover** — the review pass that reads a spec for holes, reasoning in entities, states, transitions, and invariants.
- **prover record** — one dated file under `docs/prover/` recording one review pass: what was reviewed, the findings, and the verdict. A push carries exactly one, and it is the whole review the push owes. It re-checks the spec and the architecture, and reads the commits being sent for a refusal. The push gate reads that a committed record dated the push's own day exists. It must be at least as new as the documents it covers and as the newest commit in the pushed range. It must name that range, the files read, the checks run, and its findings.
- **publish checklist** — the per-kind walk the publish skill owns, run before any deposit leaves the machine.
- **publish gate** — the human's own gate over anything irreversible or outward, which the publish checklist runs ahead of.
- **published contract** — a surface in a producer agent's own spec, paired with a machine-readable artifact at the path the producer's card names, stating the version it was generated under and the moment it was generated, that another agent reads on its own clock.
- **push gate** — the ordered chain of nets that runs before a push to the pack's repository and blocks the push on any red. Each net in the chain carries a letter.
- **queue archive** — the dated directory `docs/queue-archive/` holding every roadmap row that has left the queue's body at a terminal exit, kept verbatim with its delivery report and grepable by its number; one archive file gathers one calendar month's moved rows, and a manifest line above the body points at each.
- **queue-take** — the moment a session reads the queue's runnable head to plan the next work, building its dependency graph before opening any lane.
- **ratchet manifest** — the host record that pins the pack version each vendored gate script came from.
- **reach** — what a gate read to reach its verdict: the files it opened and the rows it matched of the rows it scanned.
- **real-device walk row** — a matrix row for a behaviour living past a desktop headless browser, one the suite can never turn green, owed to the human's own hands before ship.
- **recommendation** — a prover finding where nothing stated is broken and nothing required is missing; it queues for a taste call and does not block.
- **recorded count** — the number a growth or defect ratchet is held at, written into the gate's config or record on the day it was measured; a delivery may lower it, and no delivery raises it on its own.
- **referral** — the answer that a question belongs to another agent's zone, returned to whoever asked it.
- **register judge** — the model call that reads a stretch of outgoing text against the plain-language register law and returns the sentences that carry no information or leak register.
- **register lint** — the pre-show check `scripts/preshow-register-lint.py` that reads a surface's text for machine dialect and blocks the showing on a red result.
- **regression fence** — one sentence in a spec-delta naming a neighbouring promise that must stay true through a change, citing the existing clause it guards.
- **release** — a version bump of the pack: the root version file changes and every skill's stamped frontmatter copy is refreshed to match.
- **release gate** — the point a release passes through: the full prover re-prove over the spec and the architecture, which can require a dated clean-context review record naming a seat other than the release's.
- **remote gate** — the check set a host may mirror in its continuous-integration runner, whose verdict the pushing session reads after a push.
- **remote seat** — a session that shares no filesystem with the assigned session and reaches the repository only through git — a cloud session, a scheduled routine, or another machine.
- **removal list** — the dated record of the literal phrasings a person cut from a taste-reviewed artifact, appended when a cut happens and never removed.
- **rendered page** — the readable page `scripts/render-doc.py` builds from a markdown document for a person to open in a browser; it carries the renderer's generator mark.
- **requirement** — one unit of the body, made of a Context block, a User Story line, and acceptance criteria grouped into named cases.
- **requirements format** — the genre a spec document is written in: a preamble, a glossary, then a body of requirements.
- **response** — the duty a criterion states: its *shall* clauses, read together as one duty.
- **revisit trigger** — the recorded condition on a deferred queue row that, once it fires against the current moment, returns the row to the runnable head.
- **roadmap format** — the format-family member the queue is written in: a preamble, a glossary, then a body of live wish rows in ascending id order above a manifest, held by a row lint; it inherits the family's shared laws from the spec format and adds only the roadmap-particular rules, its definition at `docs/roadmap-format.md`.
- **round cap** — the bound of three progressing rounds on the prover-and-design-review loop, past which the loop stops iterating and surfaces its unsettled groupings on the record; a host may set its own cap.
- **routing rule** — the rule that proposes the cheapest tier that can pass a brief for each unit of work before the seat may overrule it.
- **scaffold** — the runnable suite the templates ship with. It defines what a green suite means for the first delivery.
- **scenario** — a requirement whose heading carries a `[feature: F-...]` tag, telling what a person does and what the person sees for one feature; the spec's body is a list of requirements, and a shipped feature's scenario is the requirement that states its working behaviour.
- **seat** — the one acting orchestrator session that owns judgment, orchestrates the pipeline, briefs workers, judges lane independence, reads and writes and reports during a turn, and reports to the person; the source also names this actor the senior, the senior agent, and the orchestrator, and this document keeps the one name seat throughout.
- **session extract** — one compact file holding the person's own turns from one session transcript, each turn carrying its timestamp and its text.
- **session handover** — the file a closing session leaves for the next, written from the session extract by a fresh agent.
- **settings card** — the rendered page that lists every setting the pack knows, its current value where one is recorded, and one plain-speech line saying how to change it.
- **settings ladder** — the four nested scopes that resolve any setting: the session's live word, then the host profile, then the personal profile, then the pack default. A nearer scope overrides a farther one.
- **shopfront** — the public README as the reader-facing front of a repository, whose claims match the truth just pushed.
- **show rule** — how a rendered artifact is opened for the person: a new browser window on a local seat, its own channel on a remote seat.
- **signature** — one entry in the problem ledger: a short greppable plain phrase that names a recurring operational problem, carrying its dated occurrences and one status.
- **size** — the wish's extent, named by one word from a four-word vocabulary: bug, small, surface, or large. A surface-sized wish is a new surface or a multi-file behaviour change. A bug-sized wish is the bug door itself, one call stated once for both axes. The size word is what the row's class column carries, the priority mark standing on the row beside it. The word surface elsewhere stays the common noun for a screen a person sees, and the word bug elsewhere stays the common noun for a defect.
- **skill eval** — one recorded scenario per working skill: a case where a bare session errs and the skill's text corrects it, proven red without the skill.
- **skill-creator** — the skill-making skill that reviews each skill file's craft, apart from the evals that test each skill's behaviour.
- **slot** — the reference point, the measure, or the reason a weak word opens and its criterion must fill.
- **snapshot** — the saved artifact of the last accepted run of a surface — its rendered output, files, and numbers — that the next run diffs against as its baseline.
- **source hole** — a place where the spec states a behaviour and leaves its judge, its measure, or its scope unstated.
- **spec-delta** — the set of spec sentences one wish or feature adds or changes, drafted and proven against the whole spec before any test or code is written.
- **spec-touching delivery** — a delivery whose change set includes the spec document.
- **staleness bound** — the one number a consumer owns, stating how old a published artifact may be and still carry that consumer's analysis.
- **standard facet** — one dimension every visible feature has whether or not anyone names it, such as a viewport band, touch, or an empty state, swept when a feature is specified.
- **statement validation** — the check a task statement passes before its task enters work: a mechanical floor — name, description, plan and estimate present, an estimate stated, the register check clean — and a clean-context reader's judgment that the statement is understandable.
- **stateful surface** — a part of a host project that holds state: a screen, a panel, or a saved file the user can change and find again later.
- **status report** — the running account a session keeps of the work in hand, what the queue holds next, and the messages its agent channel has sent.
- **stranger** — a contributor with no push rights and no per-repository grant for a repository; a stranger's message enters through an Issue or Discussion opened on the repository's public tracker, which the monitor bridges into the inbox.
- **stranger-wish monitor** — the scheduled process that converts each open stranger Issue or Discussion into one committed inbox file.
- **success measure** — one written way, with a number where one exists, to notice a feature worked for its person, written in the feature's spec-delta.
- **success-measure feed** — the small JSON file a host's own fetch tooling writes: a generation timestamp, the fetch's own source in plain words, a list of named metrics, and, where a two-variant experiment is running, its own named block of exactly two variants. `scripts/check-success-measure-feed.py` is its one reader.
- **suite-honesty class** — the class of invariants that keep a green suite meaningful — each naming the net that enforces it — so a passing suite proves the behaviour it claims.
- **surface registry** — one host-authored list of every user-facing surface the product carries, read by a completeness net.
- **target tag** — the marker `[target]` a spec line carries on a line of its own to mark a feature or leg that is promised but not yet built.
- **task statement** — one task's frozen wording: its name, its description, its plan, and its time estimate, spoken in those words everywhere.
- **test matrix** — the document (`TEST_MATRIX.md`) whose rows pair one architecture node with one spec fact, each row pinning the test level that covers the fact.
- **test-matrix format** — the format-family member the test matrix is written in: an artifact inventory, matrix rows grouped into node blocks, and a generated Reference; it inherits the family's shared laws from the spec format and adds only the matrix-particular rules.
- **thin loader** — the personal layer's global instruction file, holding only what must be true before any pack file loads.
- **tier** — the model level a unit of work runs at: a no-decision one-shot worker, a multi-step mechanical worker, or the seat for judgment.
- **touchpoint** — one point of contact with the person, carrying a kind: synchronous when the person is present and the work waits on the person, asynchronous when the person reads on the person's own clock while the work keeps running.
- **transient page** — a page carrying the document renderer's generator mark, built for one reading and cleared to the attic once that reading is over.
- **transport** — the road a message between two agents travels: the store, where the sender deposits one file the receiver sweeps later, or the direct channel, a live back-and-forth between two running sessions.
- **trigger** — the situation or condition a criterion opens with — a *when*, a *while*, or an *if* clause; an unconditional criterion carries none.
- **tripwire** — one fixed mechanical rule in the door step that lifts a wish to a door whatever its casual label.
- **trust** — the per-person setting family recording what the agent may do on its own word (commit, push, install its own hooks), each level moving only on the human's word.
- **update check** — the once-a-day check that asks the public repo whether the pack has moved past what this machine runs.
- **upstream note** — a short, distilled, non-public account of what happened, shaped as a private request to the pack's authors and deposited for the person to deliver.
- **user story** — the unit a request is split into: one distinct thing a person does and sees, told as a short sentence naming who wants what and for which benefit; a wish carries one, and a wish carrying more is split at intake into a row apiece.
- **verify walk** — the pipeline's final step, run in the form the medium has, where the delivery is exercised end to end through the visitor's own outside eyes before the row closes.
- **version-control gate** — the check that a host has git and a settled or explicitly declined remote before its first delivery.
- **waiting board** — the file `WAITING.md` at the host root that holds every item parked for the person's eyes, so nothing waiting evaporates when chat scrolls.
- **walk** — the pipeline's own handling of one wish, its path from capture to landing; a rule that binds the walk binds the process itself rather than any one actor.
- **watch-level** — a law's status when the design review is its named net: the law is watched and recommended rather than blocked, until the author's own declaration moves it to a blocking net.
- **weak word** — a relational word — proportional, larger, sufficient, fast, and their kind — that opens a slot for a reference point, a measure, or a reason.
- **wish** — one request a person voices in plain words, of any size and at any moment, captured as a queue row and carried to a recorded terminal state.
- **work board** — the standing page of the working picture, one source file in the host's tree published at one stable link. It shows the whole queue in columns, one column per recorded state, each row rendered as a card.
- **work-kind** — the intake axis naming what a wish produces, one of product, infra, skill, or prose, which scales how much machinery each pipeline step spends.
- **worker** — a delegated agent session the seat briefs for a bounded piece of mechanical work, narrowed to the files its brief names.
- **working skill** — a pack skill that elaborates one domain of the pipeline and opens by naming the base skill and the base version it was written against; the pack's working skills are spec-author, product-prover, product-prover-pack (the pack adapter binding the external canonical product-prover; it reviews nothing itself), design-reviewer, architect (writes or updates the architecture from a proven spec), build-pipeline, test-author, communicator, publish, text-audit (the audit-and-fix loop for human-facing texts, which runs mechanical lints and then fresh zero-context cold reads and fixes each finding at its source until two reads come back clean in a row), text-audit-pack (the pack adapter binding the external canonical text-audit; it audits nothing itself), feedback-intake, feedback-collector, and director (the first reader of a human message, deciding what it is before anything decides what to do about it; for accepted work, writes a decision sheet and carries it through a checkpoint it opens and closes itself).
- **workshop** — the tooling and machinery that build, test, and run the product without shipping in it.
- **workshop noise** — a problem the workshop raises while the product stays sound: a test harness or tool that flakes, a missing dependency, a shell command that fails outside the product, a tool that times out.
- **write-ownership law** — the rule that an assigned session writes only the tree it owns, while every other window's tree stays read-only save one inbox deposit.
- **zone** — the area of ownership an agent claims, declared on its own card.

## Parts map

| Part | Requirements | Topic |
|---|---|---|
| `spec/message-first-read.md` | R313–R314 | Reading what a person just said |
| `spec/spec-extension.md` | R316–R317 | What this document may claim, and how it is written across files |
| `spec/wish-intake.md` | R4 | Taking in a wish |
| `spec/draft-sandbox.md` | R98 | Draft sandbox |
| `spec/external-publish.md` | R143 | Publishing to the outside |
| `spec/customer-feedback.md` | R152–R158 | Feedback from the customer |
| `spec/success-measure-feed.md` | R318 | A host's fetched success-measure feed |
| `spec/product-map.md` | R159 | Product map on request |
| `spec/bug-priority-queue.md` | R160–R161 | A bug jumps the queue |
| `spec/internal-failure-log.md` | R162–R167 | Log of internal failures |
| `spec/fresh-start.md` | R169 | Starting from nothing |
| `spec/adopt-existing-project.md` | R177 | Joining an existing project |
| `spec/pack-upgrade.md` | R180 | Upgrading to the current pack version |
| `spec/settings-card.md` | R186 | Settings card |
| `spec/engine-instance-pair.md` | R187 | An engine and its instance |
| `spec/agent-identity.md` | R193 | Telling agents apart |
| `spec/public-contract.md` | R194 | The public contract between the system's parts |
| `spec/agent-request.md` | R195 | A request between agents |
| `spec/agent-birth.md` | R197 | A new agent is born |
| `spec/work-board.md` | R309 | Work board |
| `spec/queue-intake-priority.md` | R5–R6, R9–R10, R12–R17, R37–R50, R92–R96, R252–R256 | Queue: intake, classification, and priority |
| `spec/owner-questions-drafts.md` | R7–R8, R31–R36, R69, R238, R241 | Questions for the owner and draft edits |
| `spec/live-status-reporting.md` | R18–R30, R129, R236–R237, R239–R240, R257, R293–R294, R310–R311 | Live status, and how the system talks to the customer |
| `spec/parallel-lanes.md` | R77–R91 | Parallel work lanes |
| `spec/design-spec-review.md` | R11, R52–R68, R70–R76, R99–R104, R214–R215, R258–R266 | Design and spec review before the build |
| `spec/test-honesty.md` | R105–R117 | Test honesty |
| `spec/doc-order-generated.md` | R1, R97, R118–R124, R223–R224, R244, R246–R250, R277–R291, R312 | Order in the project's documents |
| `spec/public-text-rules.md` | R144–R147, R149–R151 | Rules for public-facing text |
| `spec/push-gate-milestone-audit.md` | R125–R128, R130–R142, R303, R305 | Push gates, checkpoints, and full audits at milestones |
| `spec/guardrails-freshness.md` | R168, R188, R222, R225–R235, R242–R243, R251, R267–R276, R292, R295–R296, R298, R300–R302, R306–R307 | Automatic guardrails and pack freshness |
| `spec/roles-and-agents.md` | R2, R51, R189–R192, R196, R198–R199, R206–R213, R216–R221 | Roles, workers, and agents inside the system |
| `spec/settings-layers.md` | R200–R205 | Settings, and who decides what |
| `spec/project-setup-tuning.md` | R3, R170–R176, R178–R179, R181–R185, R299, R308 | Setting up and tuning a project for its own use |
