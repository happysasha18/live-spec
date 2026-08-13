# live-spec — Product Spec (v4.3.0, 2026-07-23)

This document is the living statement of what live-spec is right now. The body is a flat list of requirements, each stating one rule of the method. A requirement carries a Context block, a one-sentence User Story, and acceptance criteria grouped into named cases; a requirement whose heading carries a `[feature: F-...]` tag is a person-facing scenario — what the reader does and what the reader sees. Edit history lives in `JOURNAL.md`; this spec states what is true today.

live-spec takes any request a person submits, of any size and at any moment, breaks it into story-sized pieces — one user story to a piece — and runs each piece through the same pipeline, one stage at a time, each stage checked by its own gate before the next, until the piece reaches a delivery and ships tested. A machine enforces the process at every step, every claim earns a test, and nothing ships until that test passes.

Bracket codes like `[E-1]` and `[INV-27]` trail a criterion and point to the rule's home in the project spec; a reader can ignore them, a maintainer follows them. The letter before the number names the kind: `E-` an entity, a numbered part of the product; `INV-` an invariant, a numbered rule that must always hold; `T-` a transition, a numbered change of state; `M-` a rhythm rule, a numbered recurring routine; `A-` an adoption step; `B-` a bootstrap step; `ACT-` an actor; `C-` a composition-axis rule; `D-` a recorded decision; `S-` a header rule; and `F-` a feature, which a scenario heading carries as a `[feature: F-...]` tag. A range such as `[T-1..T-7]` cites its whole run of codes. A `[target]` marker on a line of its own marks a feature or leg that is promised but not yet built, and a `[default]` marker names a value the agent set that the human may retune. A `[GAP: ...]` line under a criterion records a place the source states a behaviour and leaves its judge, its measure, or its scope unstated; it is the honest output for a real hole, never a filled-in guess.

The keywords *when*, *while*, *if*, *then*, *where*, and *shall* are set in lowercase italics and carry their standard requirements meaning: *shall* states a duty, *when* and *while* open a situation, *if* and *then* open a condition and its result, and *where* scopes a duty to the setting it holds in.

The foundational nouns of the method — request, pipeline, spec, architecture, invariant, guardrail, suite, session, journal, queue, movement, delivery, delivery report, footprint, profile, and resume file — carry the meanings the base method glossary gives them. The glossary below defines, in one place, every domain noun the twelve assembled sections introduce; a term appears once, under one name, and the criteria use it with that meaning.

## Glossary

- **action trace** — the ordered record of which tools the seat called during one turn, read from the tool-use events in the transcript.
- **activity generation** — the stranger-monitor's dedupe unit: the state of a shown work's outside comments, those not the monitor's own markers; a new outside comment advances the generation, and an item surfaces at most once per generation.
- **adoption** — attaching the pack to a project already running, run as an ordered set of phases.
- **adversarial read** — a fresh-context audit set on breaking a decision's case, run before the decision lands, that closes by bringing the decision to the owner with its findings and a recommendation.
- **agent** — one project window that carries its own tree, queue, gates, published contracts, a standing mission, and an agent card, each of which outlives any single conversation.
- **agent card** — a host's self-describing file (`.live-spec/agent.md`) stating its name, mission, zones, published contracts, and inbox address.
- **announced self-compaction** — the session's own act, said aloud at a safe breakpoint, of pruning its working context while carrying its live lines forward into the summary.
- **architecture format** — the format-family member the architecture document is written in: a preamble, then a body of node sections, then the architecture's generated tables; it inherits the family's shared laws from the spec format and adds only the architecture-particular rules, its definition at `docs/architecture-format.md`.
- **architecture node** — one named unit in the architecture document carrying one responsibility and one name, owning the spec facts it implements and pinned to its place in the code.
- **artifact inventory** — the test matrix's opening section naming every file the reader receives, each carried by at least one row asserting it at the rendered level.
- **attic** — the host's append-only archive folder (`attic/`). A superseded file moves here with one manifest line and is kept for good.
- **attribution line** — the single `made with live-spec` line a built-with publication carries on its landing surface, naming the pack version the project runs.
- **base skill** — the pack skill that holds the shared rulebook and the default settings, stated once, so every working skill points at one home rather than restating them.
- **beat** — one narration line marking one unit of the work's progress; a stretch with no beat is beatless, and the heartbeat line covers it.
- **blocking finding** — a finding that a criterion cannot be understood or acted on as written; it stops the section from passing.
- **board row** — one line of the work board standing for one task, live while in hand and kept once it closes.
- **breakpoint** — a point where a movement ends and session memory can be wiped with no loss, its live state replaced, a dated journal entry added, and the work committed.
- **brief** — the written instruction set a worker runs from, carrying its files, its steps, its clock, and its stop conditions.
- **bytes-per-criterion** — the byte count of a document's criterion lines alone, glossary and preamble bytes excluded, divided by the count of criteria in its body.
- **cadence** — the one number a producer owns, stating how often it regenerates its published artifact.
- **capability** — one thing a window can do; a capability holding durable state, a standing mission, and a zone of its own is an agent, and a capability living wholly inside one session is a skill.
- **capture echo** — the line the sweep posts back on an item's source, naming what was heard, its route, its name, and its row.
- **card** — one work board row rendered as a task: its echo-name, the line saying what the change does, its chips, and the details layer behind it.
- **card scan** — the live scan that reads the agent-card files under each of its roots and treats every card it finds as an agent.
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
- **public edition** — a skill's copy for a reader outside this project, held at `editions/<skill>/`. Requirement 304 states what it carries.
- **publish checklist** — the per-kind walk the publish skill owns, run before any deposit leaves the machine.
- **publish gate** — the human's own gate over anything irreversible or outward, which the publish checklist runs ahead of.
- **published contract** — a surface in a producer agent's own spec, paired with a machine-readable artifact at the path the producer's card names, stating the version it was generated under and the moment it was generated, that another agent reads on its own clock.
- **push gate** — the ordered chain of nets that runs before a push to the pack's repository and blocks the push on any red. Each net in the chain carries a letter.
- **queue archive** — the dated directory `docs/queue-archive/` holding every roadmap row that has left the queue's body at a terminal exit, kept verbatim with its delivery report and grepable by its number; one archive file gathers one calendar month's moved rows, and a manifest line above the body points at each.
- **queue-take** — the moment a session reads the queue's runnable head to plan the next work, building its dependency graph before opening any lane.
- **ratchet manifest** — the host record that pins the pack version each vendored gate script came from.
- **reach** — what a gate read to reach its verdict: the files it opened and the rows it matched of the rows it scanned.
- **readability arm** — one of the four checks the criterion-readability gate runs, each holding one reading defect of the criterion form.
- **real-device walk row** — a matrix row for a behaviour living past a desktop headless browser, one the suite can never turn green, owed to the human's own hands before ship.
- **recommendation** — a prover finding where nothing stated is broken and nothing required is missing; it queues for a taste call and does not block.
- **recorded count** — the number of criteria that break one readability arm, written into the gate's config on the day it was measured; a delivery may lower it, and no delivery raises it on its own.
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
- **size ratchet** — the recorded bytes-per-criterion bound of the spec document, which a delivery may lower and never raises on its own.
- **skill eval** — one recorded scenario per working skill: a case where a bare session errs and the skill's text corrects it, proven red without the skill.
- **skill-creator** — the skill-making skill that reviews each skill file's craft, apart from the evals that test each skill's behaviour.
- **slot** — the reference point, the measure, or the reason a weak word opens and its criterion must fill.
- **snapshot** — the saved artifact of the last accepted run of a surface — its rendered output, files, and numbers — that the next run diffs against as its baseline.
- **source hole** — a place where the spec states a behaviour and leaves its judge, its measure, or its scope unstated.
- **spec-delta** — the set of spec sentences one wish or feature adds or changes, drafted and proven against the whole spec before any test or code is written.
- **spec-touching delivery** — a delivery whose change set includes the spec document.
- **staleness bound** — the one number a consumer owns, stating how old a published artifact may be and still carry that consumer's analysis.
- **standalone mirror** — a public mirror repository the sync script rebuilds at every sync, carrying its own generated banner, release history, and attribution line. Its source is the skill's public edition where one exists, and the pack's own skill folder where none does.
- **standard facet** — one dimension every visible feature has whether or not anyone names it, such as a viewport band, touch, or an empty state, swept when a feature is specified.
- **statement validation** — the check a task statement passes before its task enters work: a mechanical floor — name, description, plan and estimate present, an estimate stated, the register check clean — and a clean-context reader's judgment that the statement is understandable.
- **stateful surface** — a part of a host project that holds state: a screen, a panel, or a saved file the user can change and find again later.
- **status report** — the running account a session keeps of the work in hand, what the queue holds next, and the messages its agent channel has sent.
- **stranger** — a contributor with no push rights and no per-repository grant for a repository; a stranger's message enters through an Issue or Discussion opened on the repository's public tracker, which the monitor bridges into the inbox.
- **stranger-wish monitor** — the scheduled process that converts each open stranger Issue or Discussion into one committed inbox file.
- **success measure** — one written way, with a number where one exists, to notice a feature worked for its person, written in the feature's spec-delta.
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
- **working skill** — a pack skill that elaborates one domain of the pipeline and opens by naming the base skill and the base version it was written against; the pack's working skills are spec-author, product-prover, design-reviewer, build-pipeline, test-author, communicator, publish, text-audit (the audit-and-fix loop for human-facing texts, which runs mechanical lints and then fresh zero-context cold reads and fixes each finding at its source until two reads come back clean in a row), feedback-intake, and feedback-collector.
- **workshop** — the tooling and machinery that build, test, and run the product without shipping in it.
- **workshop noise** — a problem the workshop raises while the product stays sound: a test harness or tool that flakes, a missing dependency, a shell command that fails outside the product, a tool that times out.
- **write-ownership law** — the rule that an assigned session writes only the tree it owns, while every other window's tree stays read-only save one inbox deposit.
- **zone** — the area of ownership an agent claims, declared on its own card.

## Requirement 1: The spec keeps what is built apart from what is planned

**Context:** The spec states what is built and working today apart from what is only planned, and it keeps a reader from mistaking one for the other. A planned feature carries the target tag on a line of its own, and the tag never spreads to the section around it. The suite ties each target tag to the queue row that builds it — a row still open, awaiting its landing — so the marker is enforced by the suite.

**User Story:** As a reader of the spec, I want a planned feature marked by a target tag the suite enforces, so that I never mistake a promised surface for a working one.

### Acceptance Criteria

**Case: built and planned are marked apart**

1. The spec *shall* state what is built and working today apart from what is only planned, marking each scenario and its named promised parts apart, so a scenario that holds built parts beside planned ones states a status for the scenario and for every named promised part. [S-0]
2. The system *shall* carry the target tag on a line of its own and *shall* keep it off the section around it. [S-0]

**Case: the suite ties each tag to its building row**

3. The system *shall* tie each target tag to the queue row that builds it, that row still open and awaiting its landing, and *shall* red the suite *if* that row ships with the tag still on, *if* the tag vanishes, or *if* the tag was never named. [S-0]
4. The system *shall* mark as planned the host-facing guardrail checks, the snapshot machinery that records a project's state at adoption as its baseline, and the design-sync machine. [E-6, E-7, A-6, E-18]
   [target]

---

## Requirement 2: The pipeline runs as a set of roles carried by the working skills

**Context:** Behind the pipeline is a full set of roles. An analyst writes the spec, an architect stress-tests the design and finds the edge cases and dead ends before any code is written, a design reviewer judges the design and checks that same-kind things behave alike, a tester works out the tests and writes them, and a project manager runs the process and reports back to the person. The design reviewer proposes the groupings of same-kind things the spec never declared and checks behaviour parity inside each group. These roles are the working skills, and one base skill holds the shared rulebook and the default settings the other skills work by.

**User Story:** As a person relying on the pipeline, I want each request run by a full set of roles carried by named working skills over one base rulebook, so that every request meets an analyst, an architect, a reviewer, a tester, and a manager, five distinct roles in one pass.

### Acceptance Criteria

**Case: the roles are the working skills**

1. The system *shall* run each request through a set of roles — an analyst who writes the spec, an architect who finds the edge cases and dead ends before any code, a design reviewer who checks that same-kind things behave alike by proposing the groupings the spec never declared and checking behaviour parity inside each group, a tester who works out and writes the tests, and a project manager who runs the process and reports back. [E-12]
2. The system *shall* carry those roles as the working skills, bringing the person in where an answer needs a fact no artifact holds — a taste, a policy, or an act irreversible outside git. [E-12, INV-17]
3. The system *shall* hold the shared rulebook and the default settings the working skills run by in one base skill. [E-12]

---

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

## Requirement 4: A wish is captured as a queue row that is never lost  [feature: F-wish]

**Context:** A wish is one request a person voices in plain words, of any size, at any moment. The moment a person voices one it becomes a row in the queue (ROADMAP.md), the persistent ordered home of every wish. The row holds the person's words, the wish's class, its status, and its acceptance criterion.

**User Story:** As a person who voices a request in passing, I want it captured as a durable queue row the instant I speak it, so that a thought thrown mid-sentence is never lost between intake and its resolution.

### Acceptance Criteria

**Case: a wish becomes a row at once**

1. *when* a person voices a wish, the system *shall* record it as one row in the queue that same moment, holding the person's words, its size in the class column with the priority mark beside it, its status, and its acceptance criterion. [E-2, E-3]
2. *when* a wish is recorded, the system *shall* keep its row existing even *if* the session ends immediately after, since the row is written before anything else proceeds. [E-3]

**Case: a row is never deleted**

3. The system *shall* never delete a row, and *shall* close a row only with a named exit. [INV-1]
4. The system *shall* carry every wish to a recorded terminal state, so a request captured in passing is never dropped. [INV-1]

---

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

## Requirement 7: Open questions arrive together on one decision page

**Context:** Several open questions reach the person together on one decision page rather than one at a time in chat. The page opens in its own window while the rest of the work carries on. Each question is a card with its recommended answer marked and room to write another. Once answered, the page is filed and every answer folded into its queue row the same session.

**User Story:** As a person who owes the pipeline several decisions, I want them gathered on one page I answer on my own clock, so that questions never dribble out one at a time and no answer I give is lost.

### Acceptance Criteria

**Case: questions arrive together and are folded back**

1. *when* more than one open question stands, the system *shall* carry them to the person on one decision page that opens in its own window while the rest of the work carries on. [E-22, INV-4]
2. The system *shall* present each question as a card with its recommended answer marked and room to write a different one. [E-22]
3. *when* the decision page comes back answered, the system *shall* file it in the decision archive `docs/decisions/` and fold every answer into its queue row the same session, since an answer left unread is a decision lost. [E-22]

**Case: the person's word settles it**

4. The system *shall* treat the person's word as what settles a decision and *shall* read a click as recording only a first pick, so a pick taken back in plain speech is withdrawn, logged as answered-then-withdrawn, and asked again later in plainer terms. [INV-9]
5. The system *shall* settle nothing that needs the person's considered word on a pick made without understanding. [INV-9]
   [GAP: the at-pick signal for a without-understanding pick is unstated in the source; the stated mechanisms are the plain-speech withdrawal and the card-defect rule (a card unanswerable without its mechanism is a defect).]

**Case: a withdrawn decision converges**

6. *when* the same decision is withdrawn a second time, the system *shall* take the recommended option, surface it as a `[default]` in the delivery report, and never re-ask it, silence staying consent from there. [INV-130, INV-31]
7. The system *shall* close an answered question for good and *shall* route a later change of mind as a new wish, the closed decision staying closed. [INV-59, INV-130]

**Case: the page mechanics have one home**

8. The system *shall* keep how the page works — its filename, its ordering, its round-trip — written once in the communicator skill's rule 10. [INV-13]

---

## Requirement 8: A decision card asks in consequences

**Context:** A decision card opens with what each option changes for the person — what it gives them or what problem it removes — in the product's own words. The mechanism follows only where it aids the choice. Each option is labelled by its consequence, never by its implementation.

**User Story:** As a person answering a decision card, I want each option framed by what it changes for me, so that I can decide without first learning how the machinery works.

### Acceptance Criteria

**Case: the card asks in consequences**

1. *when* a decision card is shown, the system *shall* open it with what each option changes for the person and *shall* label every option by its consequence, bringing in the mechanism only where it aids the choice. [INV-32]
2. The system *shall* read a card that cannot be answered without understanding the mechanism as a defect of the card. [INV-32, INV-28]

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

## Requirement 11: A proven artifact settles a fork before the person hears it

**Context:** Before surfacing a design choice, a session checks whether an existing proven artifact — the architecture, the spec, the invariants — already determines the answer. When it does, the session derives the requirement and states it back with the section cited, offering no fork. A fork reaches the person only for what the artifacts leave genuinely open.

**User Story:** As a person asked only about real choices, I want a session to derive from a proven artifact whatever the artifact already settles, so that I hear a fork only for a taste call or a trade-off no document has decided.

### Acceptance Criteria

**Case: a settled fork is derived**

1. Before surfacing a design choice, the system *shall* check whether a proven artifact already determines the answer, and *when* one does *shall* derive the requirement and state it back with the section cited as its ground, offering no fork. [INV-121, INV-4]
2. The system *shall* raise a fork to the person only for what the artifacts leave genuinely open — a taste call, or a trade-off with no artifact-grounded winner. [INV-121]
3. The system *shall* apply this check as the design-fork sharpening of the pre-ask decide-or-verify gate. [INV-4, INV-81]

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

**Case: compaction preserves an open leg**

3. The system *shall* keep the resume file's live-state supersession from compressing an unfinished leg out of existence, restating in full a leg still open at announced self-compaction. [INV-26, M-2]
   - live-state supersession is the newest live-state block replacing the older one whole.

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
   - the reminder also states the routing line: the orchestrator seat routes work to the cheapest tier the routing rule names, while a worker finds for itself the files and lines its task needs, keeping the orchestrator's context lean;
   - the skills and the profile stay the laws' homes.
8. Before a human-facing artifact is shown, the system *shall* have `scripts/preshow-lint.py` flag any line opening with an internal handle so the agent rewrites it to lead with the outcome, a warning to clear that reads only the shown surface. [INV-28]

---

## Requirement 18: Anything shown to a person passes a register lint first

**Context:** Anything shown to a person passes a register lint before it is shown. The check reads the text for machine dialect — a coined internal metaphor shown raw, an English pack term calqued into another language, or a transliterated pack term. A red result blocks the showing until the text reads in the reader's own plain words.

**User Story:** As a person about to read a shown surface, I want its machine dialect caught and blocked before it reaches me, so that a coined metaphor or a calque never reaches my eyes as nonsense.

### Acceptance Criteria

**Case: the lint blocks the showing**

1. Before a human-facing surface is shown, the system *shall* have `scripts/preshow-register-lint.py` read its text and block the showing on a red result until the flagged text is rewritten into the reader's plain words. [INV-83]
2. The system *shall* treat this as a hard block, and *shall* scope its reach to the shown artifact — a rendered page, a mockup, a decision page, or a report page. [INV-83, INV-34]

**Case: the class the list cannot hold**

3. The system *shall* keep the literal pattern set as the free first pass and *shall* grow it by nobody's duty, since a growing list stays one escape behind the next word. [INV-83]
4. The system *shall* hand the residual machine-dialect class to the register judge, the model that reads meaning at the cheapest tier the routing rule names, standing as the ceiling the literal list cannot reach. [INV-83, INV-203, INV-69]
5. The system *shall* hold the chat line by the register judge's chat arm, the mechanical gate for the chat surface. [INV-203]

---

## Requirement 19: No line certifies its own sincerity

**Context:** No line certifies its own sincerity. A sentence that praises its author's honesty, directness, or diligence carries no information, since naming a quality informs only where its absence stood as a live alternative. The content carries the honesty; the label comes off.

**User Story:** As a person reading the pack's reports, I want a self-praising sincerity label stripped from every line, so that the honesty stays in the content rather than in a phrase that distinguishes nothing.

### Acceptance Criteria

**Case: the label comes off every surface**

1. The system *shall* strip a sentence that praises its author's honesty, directness, or diligence, since a report whose every line is meant to be true distinguishes nothing by saying so. [INV-94]
2. The system *shall* bind this across every surface — a shown artifact through the register lint, and the chat through the session's own read and the hook's reminder. [INV-94, INV-83]

**Case: the register judge holds the class**

3. The system *shall* have the register judge hold this class, a caught phrase informing the judge and the literal first pass while the pattern list grows by nobody's duty. [INV-94, INV-203]

---

## Requirement 20: The report law is walked as a live step

**Context:** The report law is walked as a live step each time, since chat has no suite to enforce it. Before any movement-end or milestone report reaches the person, the agent re-reads the communicator rules and passes the draft phrase by phrase through one question: does this sentence stand for a reader who does not live inside the pack?

**User Story:** As a reader outside the pack, I want every report walked phrase by phrase before it reaches me, so that a report I read lands understood rather than making me ask what a named surface is.

### Acceptance Criteria

**Case: the walk before every report**

1. Before any movement-end or milestone report reaches the person, the system *shall* re-read the communicator rules and pass the draft phrase by phrase through the outside-reader question. [INV-34]
2. The system *shall* explain any pack surface the draft names in the reader's own words or drop it, while quiet trailing anchors stay legal. [INV-34]
3. The system *shall* read a report that makes the reader ask what a thing is as the walk not walked, its acceptance belonging to the reader. [INV-34]

---

## Requirement 21: A question walks the same scan and one gate more

**Context:** A question to the person walks the same phrase-by-phrase scan a report walks, and one gate more, asked first: can I decide or verify this myself? A question that fails that gate is work, done instead of asked. A question that survives it arrives with its recommendation attached.

**User Story:** As a person asked only what I alone can settle, I want every question gated by can-the-agent-decide-this-first, so that a question the agent could answer itself becomes work done and a surviving question arrives with a recommendation.

### Acceptance Criteria

**Case: the scan and the extra gate**

1. Before any question is asked — in a report's batched tail, on a decision page, or as a lone ask in chat — the system *shall* pass it through the same phrase-by-phrase read, every term grounded in the reader's own words. [INV-81, INV-34]
2. The system *shall* ask first whether it can decide or verify the answer itself, and *shall* turn a question that fails that gate into work done rather than asked. [INV-81, INV-4, INV-5]
3. The system *shall* have a question that survives the gate arrive with its recommendation attached. [INV-81, INV-60]

---

## Requirement 22: Work is narrated while it runs

**Context:** Work is narrated while it runs, the third voice between the capture echo and the delivery report. The person leads many windows at once, so otherwise silence is all they get. While work runs, the agent says each beat worth a sentence — a stage passed, a load-bearing find, a change of direction — in the roadmap's terms and the reports' voice.

**User Story:** As a person leading many windows, I want each beat of running work narrated in plain roadmap terms, so that a silent stretch never reads to me as lost work.

### Acceptance Criteria

**Case: beats are narrated as they happen**

1. *while* work runs, the system *shall* say each beat worth a sentence in one or two plain sentences in the roadmap's terms, and *shall* keep the mechanical grind quiet. [INV-35]
2. The system *shall* name in every beat the work it belongs to — which wish is in hand and which pipeline stage it stands at, and whether it mends something broken or builds something new. [INV-35]
3. *when* a station completes, the system *shall* make its line a beat carrying a short digest of what the station produced in the work's own words. [INV-35]

**Case: the heartbeat and the detached run**

4. *when* a stretch runs long with no beat, the system *shall* say what is grinding and why the stretch runs long, owing this heartbeat past a beatless stretch of about 10 minutes as a default. [INV-35]
5. *when* an operation runs detached past about 2 minutes, the system *shall* open with a start line naming what runs, where its log lives, and an honest range, keep a beat landing about every 2 minutes or at each stage, and close with a done digest. [INV-35, INV-93]

**Case: the offline window**

6. *when* the coming stretch needs nothing from the person, the system *shall* say so before it starts — that the person may step away, an honest range for how long, and what the person is needed for at its end — stating an unknown duration as unknown. [INV-35]
7. *when* the person is needed again, the system *shall* say so plainly as a beat naming the gate or decision that waits, batching questions born inside the window to its end. [INV-35, INV-4]

**Case: narration is chat-register**

8. The system *shall* keep a narration line an informal chat message that walks no pre-report walk, asks nothing, and replaces no report, while every human-facing-line law still binds. [INV-35, INV-27, INV-28]

**Case: the delegated beat and the time accounting**

9. *when* a delegated worker closes a station, the system *shall* fold it into the trail, a station a delegated worker closed becomes the senior's beat the moment it lands, the trail the session's time accounting where token and test counts stay bookkeeping. [INV-35, INV-28]

**Case: the offline window's honest edges**

10. *when* the offline window runs, the system *shall* keep its edges honest, never a guess dressed as a promise, a window off its spoken range saying so, overrun, done sooner, or blocked on the human's word alone, the needed-again beat a chat line awaiting his return, never a summons, and no offline sentence fires when the very next beat needs the human. [INV-35, INV-4]

---

## Requirement 23: Every ask hears its price in time, and the landing settles it

**Context:** Every ask hears its price in time, and the landing settles it. The capture echo carries an honest time range read from the work's known shape or observed runs, an unknown stated as unknown. Work expected to run an hour or more is explained up front in plain steps. The delivery report states the estimate beside the actual.

**User Story:** As a person who owes time to a task, I want an honest range at capture and the estimate settled against the actual at landing, so that I know what a task costs before it starts and how the guess held afterward.

### Acceptance Criteria

**Case: the range at capture and the settling at landing**

1. The system *shall* carry in the capture echo an honest time range read from the work's known shape or observed runs, stating an unknown as unknown. [INV-93, INV-27, INV-35]
2. *when* work is expected to run an hour or more, the system *shall* explain it up front in plain steps — what has to happen and why it takes that long — and *shall* say on the heartbeat how much time remains as the stretch runs. [INV-93, INV-35]
3. *when* a wish lands, the system *shall* state the estimate beside the actual in the delivery report, saying an overrun or an under plainly. [INV-93]
4. *when* a direct command holds the session for more than a beat, the system *shall* have it hear its range even though it registers no row. [INV-93]
   [GAP: the beat's duration for a direct command's range announcement is unstated in the source.]

---

## Requirement 24: A rewrite that removes substance accounts for it

**Context:** A rewrite that removes substance accounts for it in the delivery report. A restyle or a restructure drops content as it tightens, and some of what it drops carries weight — a section, an argument, a rationale, a worked example. The rule scopes to substance and leaves line-level wording free.

**User Story:** As a person whose document a rewrite tightened, I want every removed piece of substance accounted for in the report, so that deleted content is kept and cited, killed by my own word, or raised as a question rather than cut silently.

### Acceptance Criteria

**Case: every removal is accounted for**

1. *when* a rewrite or restyle removes substance — a section, an argument, a rationale, or a worked example — the system *shall* list every removal in the delivery report with one line of judgment each: the fact was kept and where, the person killed it by name, or the rewriter proposes dropping it and asks. [INV-109]
2. The system *shall* turn a removal the rewriter cannot justify into a question before the report closes, and *shall* not cut substance silently. [INV-109]

**Case: line-level wording stays free**

3. The system *shall* scope this accounting to substance and *shall* leave a tightened sentence or a reordered clause needing no account. [INV-109]

---

## Requirement 25: One spoken leave-word winds the session down to a safe stop

**Context:** One spoken leave-word winds the session down to a shutdown-safe stop. When the person says they are leaving, the session stops taking new work and walks what is open to a safe point: background workers halt or run to their landing, every open lane reaches its checkpoint, green work is committed under its gates, and the resume file says what resumes where.

**User Story:** As a person about to close or sleep the machine, I want one leave-word to bring the session to a shutdown-safe stop, so that no worker dies mid-write, no red work is committed, and I am told plainly when it is safe to power off.

### Acceptance Criteria

**Case: the wind-down to a safe point**

1. *when* the person says they are leaving, the system *shall* stop taking new work and *shall* halt background workers or run them to their landing, recording any worker that cannot halt in time by the handoff discipline — a note carrying the worker's id, the exact files its brief lets it write, and the liveness checks a resuming session runs before touching them. [INV-95, INV-76]
2. The system *shall* bring every open lane to its checkpoint, committing green work under its standing gates and committing no red work, with the failing test name and hypothesis topping the resume file. [INV-95]
3. The system *shall* have the resume file say what resumes where. [INV-95]

**Case: the closing line and its timing**

4. The system *shall* answer in the first beat roughly how many minutes remain to the safe point, and *shall* give as its last a single closing line — safe to power off, plus what resumes where on return — said only *when* every point above holds. [INV-95, INV-93]
5. The system *shall* ride the remaining-minutes habit on long work even before any leave-word, and *shall* never guess from silence that the person is leaving. [INV-95, INV-35]

---

## Requirement 26: Anything handed to the person opens with a one-line identifier

**Context:** Anything handed to the person opens with a one-line identifier. A page that opens in the browser states two things: which project it belongs to, and whether it needs the person's attention. A page that states neither reads as noise.

**User Story:** As a person who finds a page open in my browser, I want it to name its project and say what it needs of me, so that I always know what I am looking at and what it asks.

### Acceptance Criteria

**Case: the identifier states project and need**

1. The system *shall* show the project's name in a handed page's visible content, not only in its URL. [INV-51]
2. The system *shall* state what the page needs from the person — a word, with what and by when, or that it is only an update with no action. [INV-51]
3. The system *shall* lead every handed or opened artifact — a report page, a decision page, a rendered doc, or a standing rendered surface the person opens — with that identifier, and *shall* carry the same two facts in the chat line that announces it. [INV-51]

---

## Requirement 27: During an away-stretch, artifacts accumulate on one page

**Context:** During an away-stretch, artifacts accumulate and one window opens at the end. When the person has stepped away for an overnight loop or an offline window, the agent does not open a browser window mid-stretch. Artifacts accumulate on one page.

**User Story:** As a person who stepped away, I want artifacts gathered on one page that opens once at the end, so that an overnight stretch never scatters windows across my screen.

### Acceptance Criteria

**Case: one page for the away-stretch**

1. *while* the person is away for an overnight loop or an offline window, the system *shall* not open a browser window mid-stretch and *shall* accumulate the stretch's decisions and report on one page. [INV-52, INV-35]
2. The system *shall* allow a mid-stretch re-open only as that same page refreshed in place. [INV-52]

---

## Requirement 28: The showing channel matches where the session runs

**Context:** The showing channel matches where the session runs. A session on the person's own machine shows a rendered artifact as a local page in a browser window. A remote session runs in the cloud, is read through a browser, and cannot open a local page, so it shows the same content through its own channel.

**User Story:** As a person reading a session that may run locally or in the cloud, I want it to show through the channel its seat can reach, so that a remote session never hands me a local file path that opens into nowhere.

### Acceptance Criteria

**Case: the seat picks the channel**

1. The system *shall* read where the session runs from what it can reach — the platform, the display, and whose filesystem it sees — and *shall* name the channel it picked. [INV-67]
2. The system *shall* show a local session's artifact as a local page in a browser window, and *shall* show a remote session's artifact through its own channel — an artifact page the host renders, or the chat itself — carrying the same identifier and the same round-trip. [INV-67, INV-51]
3. The system *shall* re-read the seat after any move between machines, and *shall* read handing a local file path to a remote reader as a defect of the exchange. [INV-67]

---

## Requirement 29: The current state of the work is answerable in any setting

**Context:** The current state of the work is answerable at any moment, in any setting. The harness's own task panel and activity line are a convenience of the local terminal, absent in a browser and stalling on a long run of tool calls. So the live status lives in the chat, the one surface present in every setting.

**User Story:** As a person who looks in at any moment, I want the work's state kept current in the chat, so that a glance answers what we are working on and what comes next whatever setting I read from.

### Acceptance Criteria

**Case: the status lives in the chat**

1. The system *shall* keep a short status current in the chat — a Now line naming the work in hand and its pipeline stage, and a Next line naming what the queue holds next. [INV-71, INV-67]
2. The system *shall* refresh the status at every stage change and *shall* carry a heartbeat on a long stretch. [INV-71, INV-35]

**Case: the harness panel is a courtesy view**

3. The system *shall* keep the harness task panel, where a setting shows it, in plain product words as a courtesy, and *shall* not make it the home of the status. [INV-71, INV-28]
4. The system *shall* offer a rendered status page as an optional richer view of the same Now and Next on a local session, and *shall* apply this to every project the pack runs. [INV-71, INV-67]

---

## Requirement 30: The end of a stretch is delivered so the person cannot miss it

**Context:** The end of a stretch is delivered so the person cannot miss it. A report that exists but sits above tool noise counts as undelivered. When a stretch ends, the last rendered thing is one short final line.

**User Story:** As a person who might miss a report buried above tool output, I want one short final line as the very last thing rendered, so that I can never miss where the run ended.

### Acceptance Criteria

**Case: the final line comes last**

1. *when* a stretch ends — a loop iteration going to sleep, an away-stretch closing, or a session ending — the system *shall* render as the last thing one short final line carrying what closed, what is next, what is needed from the person, and when the agent wakes. [INV-57]
2. The system *shall* place the long report above that line and *shall* render the final line last, after every tool call. [INV-57]
3. The system *shall* repeat a page deliverable's identifier in that final line. [INV-57, INV-51]

---

## Requirement 31: A review surface shows its sources and accepts the person's edits

**Context:** A review surface shows its sources and accepts the person's edits. Anything shown for review carries per-claim provenance, marking each claim by where it came from — read from the artifact, the person's own recorded word, or the agent's inference. Inferences are flagged most prominently.

**User Story:** As a person reviewing a surface the agent shows, I want each claim marked by its source and the surface open to my edits, so that no work reaches me as a read-only wall or an unmarked guess.

### Acceptance Criteria

**Case: per-claim provenance**

1. The system *shall* mark each claim on a review surface by where it came from — read from the artifact, the person's own recorded word, or the agent's inference — and *shall* flag an inference most prominently. [INV-64]

**Case: the surface is commentable**

2. The system *shall* keep the surface commentable and open, giving line-by-line room for the person's word and capturing the answers. [INV-64]
3. The system *shall* extend the decision page's saved-answers rule to a review surface as one round-trip back to the project. [INV-64, INV-32]

---

## Requirement 32: The person's word is read as meant, and the person's cuts hold

**Context:** The person's word on a shown artifact is read as meant, and the person's cuts hold. A phrasing the person removed in a review round stays removed in every later draft of that artifact. A vivid phrase from the person is adopted only as meant, since a person sometimes writes mockery of a bad draft rather than guidance.

**User Story:** As a person who cut a phrasing and wrote a colorful remark, I want the cut to hold across every later draft and the remark read for its intent, so that a cut word never reappears and a parody is never baked in as if prescribed.

### Acceptance Criteria

**Case: a cut holds across drafts**

1. The system *shall* keep a phrasing the person removed in a review round removed in every later draft of that artifact, holding the removal list where the artifact's project keeps its records rather than in session memory alone. [INV-42]
2. The system *shall* read a cut word reappearing a later round as a defect, however fresh it looks, since a memory wipe restores no cut phrasing. [INV-42]

**Case: a vivid phrase is read for intent**

3. Before a colorful phrase from the person shapes the work, the system *shall* read its intent from context or ask, rather than assuming a mockery of a bad draft is prescriptive. [INV-42, INV-4]
4. The system *shall* cross-link the two standing bans this rests on — no self-praising drama, and no approval-begging under silence-is-consent — rather than restate them. [INV-42, INV-31]

---

## Requirement 33: Approved text is frozen, and a revision applies only the named correction

**Context:** Approved text is frozen, and a revision applies only the named correction. Once the person approves a text it is settled material. A later revision applies exactly the correction the person named and does not rewrite the surrounding text.

**User Story:** As a person who approved a text, I want a later revision to apply only the correction I named, so that approved material never churns under a rewrite I did not ask for.

### Acceptance Criteria

**Case: only the named correction lands**

1. *when* the person approves a text, the system *shall* treat it as settled material. [INV-58]
2. *when* a revision is applied, the system *shall* make exactly the correction the person named — trim what they said to trim, swap what they said to swap — and *shall* leave the surrounding text untouched. [INV-58]
3. The system *shall* read churn of approved material as a defect, kin of a reappearing cut. [INV-58, INV-42]

---

## Requirement 34: No question is asked twice, and dialogues converge

**Context:** No question is asked twice, and dialogues converge. Before any ask, the agent searches the recorded word — the decision archives, the review records, the journal, and the profile. An answered question closes permanently and is recorded into its row the same session.

**User Story:** As a person whose answers are on record, I want the agent to search them before asking and to close an answered question for good, so that I am never asked a question a record already answers and a solved problem returns with evidence rather than re-described.

### Acceptance Criteria

**Case: the search before every ask**

1. Before any ask, the system *shall* search the recorded word — the decision archives, the review records, the journal, and the profile — and *shall* read asking a question a record already answers as a defect. [INV-59]

**Case: dialogues converge**

2. The system *shall* close an answered question permanently and record it into its row the same session. [INV-59]
3. The system *shall* return a problem the person named solved with evidence rather than re-described, so a later round carries only new material. [INV-59]

---

## Requirement 35: A taste ask arrives carrying the agent's own researched proposal

**Context:** A taste ask arrives carrying the agent's own researched proposal. A genuine taste question arrives with work already done — mined exemplars, precedents, and real options with citations — and a chosen recommendation with its evidence.

**User Story:** As a person asked a taste question, I want it to arrive with the agent's own research and a recommendation, so that I am never asked to supply what the agent should have mined first.

### Acceptance Criteria

**Case: research precedes the ask**

1. The system *shall* mine the material first — exemplars, precedents, and real options with citations — and *shall* then ask with a chosen recommendation and its evidence. [INV-60]
2. The system *shall* read asking the person to supply what the agent should have mined as a defect, this sharpening the recommended-option rule for a taste call. [INV-60, INV-4]

---

## Requirement 36: The removal list has a mechanical form

**Context:** The removal list has a mechanical form. For a host with taste-reviewed artifacts, the pack ships a removal-list template that holds the person's cuts as dated literals, appended the moment a cut happens and never removed. The pack also ships guardrails guidance for a scanner.

**User Story:** As a person whose cuts must hold, I want the removal list backed by a shipped template and a scanner, so that a literal I once cut turns the suite red if it reappears in the artifact's surfaces.

### Acceptance Criteria

**Case: the template and the scanner**

1. The system *shall* ship a removal-list template holding the person's cuts as dated literals, appended the moment a cut happens and never removed. [E-26]
2. The system *shall* ship guardrails guidance for a scanner that reads the table and greps the artifact's surfaces, turning the suite red *when* a removed literal reappears. [E-26, INV-42]

**Case: the scanner stays per-project**

3. The system *shall* keep the scanner per-project, the pack shipping the shape — the template and the guidance — while each host owns the greps that read its own surfaces and holds its own dated cuts. [E-26, INV-163]
4. *when* a host's scanner grows a genuinely generic seam, the system *shall* lift that seam to the pack and *shall* keep the host-specific greps at home. [E-26, INV-163]

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

## Requirement 51: Each step is worked with its craft's standards

**Context:** A single generalist working the whole pipeline produces generalist artifacts. Each step therefore names the profession the agent works it as, and each artifact is judged by that craft's standards. The craft, like the step's form, follows the kind.

**User Story:** As a person relying on each artifact, I want each step worked with its own craft's standards, so that a spec reads like a product manager's and a test matrix like a quality-assurance engineer's rather than one generalist's notes.

### Acceptance Criteria

**Case: each step names its craft**

1. The system *shall* work the spec as a strong product manager, the architecture as a software architect, the test matrix and tests as a quality-assurance automation engineer, the code as a senior developer, the two prove steps as the prover's formal-reviewer role, commit-and-show as a careful release engineer, and the verify walk as the visitor's own outside eyes. [INV-33, E-12]
2. The system *shall* judge each artifact by its craft's standards and speak the delivery report's step accounting in them. [INV-33]

**Case: the craft follows the kind**

3. The system *shall* let the wish's kind say what each craft's standards look like in its medium, working the code step as a strong writer on a prose product and as a tool builder on infra. [INV-33, INV-22, INV-30]

---

## Requirement 52: A feature is specified past what the human knows to ask

**Context:** The human says add a room where photos hang; the human does not say and decide what happens on a phone, because the human cannot know that is a question. So a feature-doored wish's spec-delta walks a fixed sweep of the standard facets — the dimensions every visible feature has whether or not anyone names them. The facet list has one home in the spec-author skill, and the inline list is its reader's echo.

**User Story:** As a person asking for a feature in plain words, I want its spec-delta to sweep the standard facets, so that the questions I did not know to ask — the phone layout, touch, the empty state — are each decided before the feature ships.

### Acceptance Criteria

**Case: the sweep runs the facet set**

1. *when* a wish's door says feature, the system *shall* walk its spec-delta through the standard facets — the viewport width and height bands, touch where the design assumed a mouse, the empty and error and loading states of each new surface, keyboard reach and readable contrast, the performance envelope, visual hierarchy, two windows at once, and a missing source. [T-13, INV-138]
2. The system *shall* end a layout-bearing feature's sweep with a decided or defaulted sentence per viewport band its layout law names or excludes, letting a law scoped to one band answer for the others. [T-13, INV-138]

**Case: the sweep's scope and the curated list**

3. The system *shall* scope the sweep to the feature's visible surfaces, satisfying a feature with none by one explicit sentence that no visible surface exists and the facets do not apply, never a silent skip. [T-13]
4. *when* a wish is re-doored to feature mid-work, the system *shall* walk the sweep before work resumes, and *shall* not sweep a fenced prototype, firing the sweep only when promotion makes it a feature. [T-13, INV-16, E-17]
5. The system *shall* keep the facet list in the spec-author skill as one closed enumerable set that grows a member only with a named real incident it would have caught, re-justified at milestones, naming every facet on its own line rather than letting any facet ride unnamed inside another's. [T-13, INV-226]

---

## Requirement 53: Every facet ends as a spec sentence

**Context:** A facet sentence is written one of two ways: decided, when the human or the walk's batched questions called it, or defaulted, when the recommended option is taken so the lane keeps moving. A defaulted sentence carries the literal tag `[default]` at its line end, and a facet with no sentence at all is a spec defect the prover flags.

**User Story:** As a person whose feature has many facets, I want each one written decided or defaulted rather than left silent, so that a later prover can tell a taken default from a hole and no facet ships as an unasked question.

### Acceptance Criteria

**Case: decided or defaulted, never silent**

1. The system *shall* write each facet as a decided sentence or a defaulted sentence tagged `[default]` at its line end, deriving the facet's test row either way. [INV-18, E-15]
2. The system *shall* never ask the human to confirm a default and never ping once per facet, since silence is consent and the human's veto becomes a new wish. [INV-18, INV-31]
3. *when* a facet has neither a decided nor a defaulted sentence, the system *shall* have the prover flag it a spec defect. [INV-18]

**Case: defaults on a live surface, and the split by time**

4. *when* a surface already lives, the system *shall* read a default from the shipped truth and reconcile it like any re-engineered claim, never inventing it against live behaviour. [INV-18, A-10, A-3]
5. The system *shall* let the facet sweep author the facet sentences when the feature is first specified and let the axis rule compose and test them across views once the surface exists. [INV-18, C-1]

---

## Requirement 54: The spec names its cross-cutting laws in one place, and every section answers them

**Context:** A product declares laws that cut across every surface — measurement, accessibility, error handling, a register of speech. The spec keeps that list in one declared-laws home, and each new surface's section states its line against each declared law before the prover reads it. Each declared law also names the net that enforces it.

**User Story:** As a person guarding a product-wide law, I want the laws listed in one home with each surface answering each and each law naming its net, so that a missing clause or a missing net ranks as a broken invariant.

### Acceptance Criteria

**Case: the declared-laws home and the per-surface answer**

1. The system *shall* keep the cross-cutting laws in one declared-laws home and *shall* have each new surface's section state its clause or a dated exemption against each declared law before the prover reads it. [INV-101]
2. The system *shall* have the prover's station enumerate every surface and transition per declared law and demand the clause or the dated exemption per item, ranking a missing clause a broken invariant. [INV-101]

**Case: this pack's declared laws and their nets**

3. The system *shall* declare this pack's three laws — the plain-language register on every human-facing surface, clock-honest stamps on every dated line, and no self-certification on any claim of done — each naming its mechanical gate. [INV-101, INV-28, INV-34, INV-83, INV-24, INV-94]
4. *when* a declared law names no net, the system *shall* rank the missing net a broken invariant, the same rank as a missing per-surface clause. [INV-101]

---

## Requirement 55: Every declared law names its enforcing net, and declaration moves a property to a blocking net

**Context:** A law that cuts across surfaces is enforced by one of three nets, and the law names which: a mechanical gate where a deterministic check can decide the violation, the prover's judgment station where the violation pins to a stated sentence, or the design review's recommendation where the deciding fact lives only in the person's intent. Declaration is the lever that moves a property between the nets.

**User Story:** As a person deciding how a law is enforced, I want each law to name one of three nets by where its violation can be decided, so that declaring a property promotes it from a soft recommendation to a blocking net with no property owned by two nets at once.

### Acceptance Criteria

**Case: the three nets and where each law belongs**

1. The system *shall* assign a law to a mechanical gate *when* a deterministic check can decide the violation, to the prover *when* the violation pins to a stated sentence, and to the design review *when* the deciding fact lives only in the person's intent. [INV-150, INV-125]
2. The system *shall* record each law's net beside it in the declared-laws home and *shall* rank a law with no named net a broken invariant. [INV-150, INV-101]
3. *when* a law is held at watch-level, the system *shall* name the design review as its net with a dated reason, so a watch-level choice reads as a deliberate decision. [INV-150]

**Case: declaration promotes and blocks**

4. *when* the author declares a grouping, a facet, or a law in the declared-laws home, the system *shall* move the property from the design review to the prover or a mechanical gate and start blocking on it, keeping the architecture's one-owner check as the backstop. [INV-150, INV-141]

---

## Requirement 56: Every incoming thing routes to the home whose declared sentence governs it

**Context:** The request classifier, the property net, the deferral test, and the earned message are one principle stated four times: every incoming thing routes to the home whose declared sentence governs it, and a thing that pins to no home is itself the finding. The four stay separate controls under the one principle because they run at different moments under different verifiers.

**User Story:** As a person handing the pack many kinds of thing, I want each routed to the home whose declared sentence governs it and a homeless thing made the finding, so that nothing is homeless by silence and declaration is the one lever across all four controls.

### Acceptance Criteria

**Case: each thing routes to its governing home**

1. The system *shall* route each thing to its own governing home. [INV-153, INV-151, INV-150, INV-152, INV-189]
   - a request, to the highest document whose sentences it changes;
   - a property, to the net that can pin its violation to a stated sentence;
   - a backlog item, to the seat, unless it names a fact only the human holds;
   - a question, to the sender's own blocked work.
2. *when* a thing pins to no home, the system *shall* make the thing itself the finding. [INV-153, INV-4, INV-101, INV-143, INV-191]
   - an unmatched request becomes a plain question;
   - a netless declared law becomes a broken invariant;
   - a held backlog item defaults to the seat;
   - a groundless question is dropped, with the holding named.

**Case: declaration is the lever, verified adjacent to each thing**

3. The system *shall* let declaration promote a property to a blockable check, a door or tripwire to a mechanical route, and named blocked work to a gate-readable message. [INV-153, INV-150]
4. The system *shall* verify each control adjacent to the thing it audits — the classifier by the landing's applied-or-stood-down contract, the property net by the declared-laws station, the deferral test by the seat's derive-before-defer posture, and the earned message by the receiving sweep's gate. [INV-153, INV-22, INV-101]

---

## Requirement 57: A feature is interrogated for how it fits the product

**Context:** The device facets ask what every visible feature owes; nobody has yet asked how this feature sits in the person's path. Path holes ship green because no clause ever promised the way out. So a feature-doored wish's spec-delta also walks the fit walk, scaled to the wish's kind, and the prover gains the matching focused mode, feature-fit.

**User Story:** As a person adding a feature, I want its spec-delta walked for how the person arrives, acts, and moves on, so that a path hole with no way out is caught at intake, before it ever ships green.

### Acceptance Criteria

**Case: the fit walk, scaled to the kind**

1. *when* a wish enters the feature door, the system *shall* walk its spec-delta through the fit walk scaled to its kind — a product wish through the visitor's journey, an infra wish through its flows, a skill wish through trigger, correction, and when not to fire. [INV-29]
2. The system *shall* interrogate the feature and not the person, deriving each answer from the existing spec and the shipped truth first. [INV-29]

**Case: holes closed, defaulted, or asked**

3. *when* a hole is trivially closable — its answer pins to an existing artifact: a base rule, a spec sentence, the architecture, or an already-answered decision — the system *shall* close it and write the closing down, writing the rest decided or `[default]`-tagged and sending only genuine taste calls out in a batch. [INV-29, INV-4, INV-18]
4. The system *shall* give the prover the feature-fit mode that walks the journey seams against the whole spec, and *shall* owe a landed feature its walk at the first landing that touches it rather than retroactively. [INV-29, INV-159]

---

## Requirement 58: A face that can be entered once owes a way back or a written one-way

**Context:** A surface's faces get entered under conditions — a first-visit door, an empty state, an onboarding screen, a one-time banner. A face whose condition can never re-arise is a dead end the state lenses miss. Trigger wording is the tell: only on first visit, only on first run, until dismissed.

**User Story:** As a person who can leave and re-enter a surface, I want every conditionally-entered face to state its re-entry path or name its one-way, so that a face reachable again always says how it is reached.

### Acceptance Criteria

**Case: the return sentence or the written one-way**

1. The system *shall* have every conditionally-entered face state its deliberate re-entry path or state the one-way as a decision by name. [INV-50]
2. *when* a face carries trigger wording such as only on first visit or until dismissed, the system *shall* owe that clause its return sentence and have the prover read for it through the entry-symmetry lens. [INV-50, INV-29]

---

## Requirement 59: Verify-by-deed walks the visit and judges the feel

**Context:** For the product kind, the verify step includes a named visitor walk: the whole journey as the person will live it. The agent walks the first visit, the return visit, entry through another door, where am I and how do I move on from any point, and the exits. The agent also runs a feel pass against the approved prototype as the bar, in the form the medium actually has.

**User Story:** As a person shipping a product feature, I want verify to walk the visit and judge the feel against the prototype, so that shipped work is checked the way a person actually lives it and findings become rows or red rather than a mental note.

### Acceptance Criteria

**Case: the visitor walk and the feel pass**

1. *when* the verify step runs on a product-kind wish, the system *shall* walk the first visit, the return visit, entry through another door, where the person is and how they move on from any point, and the exits. [INV-30]
2. *when* the feel pass runs, the system *shall* judge motion quality and each affordance's craft against the approved prototype as the bar, turning findings into rows or red. [INV-30, E-17]

**Case: the walk runs in the medium's own form**

3. The system *shall* run the walk in the form the medium has — motion and affordance for a browser, reading path and chapter flow for a book, the command round-trip for a command-line tool — reading its checklist from the build-pipeline product cell. [INV-30, E-12, INV-22]

---

## Requirement 60: The prover labels each finding a defect or a recommendation

**Context:** Every prover finding carries its kind, so the human knows at a glance what the finding asks of them. A defect blocks and the design becomes buildable only once it is folded; a recommendation does not block and queues for a taste call. The kind is derivable from the finding's own ground.

**User Story:** As a person reading prover findings, I want each labelled a defect or a recommendation, so that I sort what blocks from what queues at the point of report rather than by hand.

### Acceptance Criteria

**Case: the two kinds and their verdicts**

1. The system *shall* label a finding a defect *when* it names a violated invariant, a false spec claim, or a missing required invariant, blocking until it is folded. [INV-140]
2. The system *shall* label a finding a recommendation *when* nothing stated is broken and nothing required is missing, queuing it for a taste call with an optional now-or-later grade. [INV-140]

**Case: the gate folds and queues**

3. The system *shall* have the push gate fold every defect and queue every recommendation, deriving the kind from the finding's own ground. [INV-140, M-6]
4. *when* a delta-scoped gate meets a pre-existing defect outside the delta, the system *shall* queue it by that law rather than block the merge it did not create. [INV-140, INV-114]

---

## Requirement 61: A design review reads a proven spec and judges the design behind it

**Context:** After the prover has checked a spec, a separate pass called the design review reads the same spec and judges its design. It builds its own transient inventory of every element a person acts on, writes one plain sentence of what the person does with each, and proposes elements whose sentences match as a same-kind group. Its findings are recommendations or questions and never block a landing.

**User Story:** As a person guarding design consistency, I want a design review to group the elements a person acts on and check each group for behaviour parity, so that same-kind things behave alike and a divergence is brought to me with two concrete objects in hand.

### Acceptance Criteria

**Case: the inventory and the same-kind groups**

1. *when* the prover has checked a spec, the system *shall* have the design review read the same spec, build its own transient inventory of every element a person acts on that a spec sentence names, and write one plain sentence of what the person does with each in the person's own action words, never writing that inventory into the surface list the host authors. [INV-141, E-10]
2. The system *shall* propose elements whose sentences match as a same-kind group, check each group for the same gestures, transitions, and affordances, and stay silent where the grouping or the difference is not plain. [INV-141]

**Case: findings recommend or ask, never block**

3. The system *shall* name two concrete objects with the spec sentence each comes from on every finding, produce no blocking defects, and write a dated record with a per-finding outcome column. [INV-141, INV-140]
4. *when* the human confirms two elements are the same kind, the system *shall* have the spec author write a class sentence the existing checks then hold, and *when* the human says they differ by intent, *shall* write a decided sentence that closes the question. [INV-141, INV-125, INV-59]

**Case: the review runs in the kind's own form**

5. *when* a kind has no element a person acts on, the system *shall* stand the design review down by name in the record rather than run it vacuously. [INV-141, INV-22, INV-125, INV-30, INV-136, INV-139]
6. The design review *shall* run in the project kind's own form, the way the verify walk and the design principles do. [INV-141, INV-136]
7. The spec's own declared-class check *shall* keep governing *where* a class is already declared. [INV-125]

---

## Requirement 62: A gesture or overlay spec triggers the design review's motion-parity lens

**Context:** The bottom-up similarity lens builds its groups from matching role sentences, so it can miss a same-kind grouping the medium makes obvious. A spec that ships a gesture, a motion, or a layer that opens and closes over another carries a standing lens the design review runs by construction, naming three same-kind groups the text need not have declared.

**User Story:** As a person shipping a gesture or overlay, I want the design review's motion-parity lens run by construction, so that the way out mirrors the way in, every object type behaves alike, and every slot behaves alike before a device ever shows a divergence.

### Acceptance Criteria

**Case: the three same-kind groups**

1. *when* a spec ships a gesture, a motion, or a layer that opens and closes over another, the system *shall* run the motion-parity lens by construction, naming entry-mirrors-exit as the first group so a layer closes by the reverse of the motion that opened it. [INV-165, INV-141]
2. The system *shall* name every object type the gesture acts on as the second group, and every position as the third group. [INV-165]
   - in the second group, each kind opens and closes the same way and lands back on its own on-screen rectangle;
   - in the third group, the same gesture on the same type in a different slot behaves the same.

**Case: each finding recommends or asks**

3. The system *shall* make each motion-parity finding a recommendation or a question and never a blocker, holding it by the prover's uniformity check once the human declares the parity a class sentence. [INV-165, INV-125]

---

## Requirement 63: A feature delta adding a second member of a kind draws the scoped design review at intake

**Context:** The moment an undeclared same-kind grouping comes into existence is the intake of its second member: the first member ships alone with no class to belong to, so when a delta adds a sibling the uniformity check has no class clause to hold and the full design review is not due until the next milestone. Feature intake therefore carries one standing question the feature-fit walk asks by construction.

**User Story:** As a person adding a sibling to an existing kind, I want the scoped design review drawn at intake, so that the window where a second sibling ships and diverges before the next full pass is closed.

### Acceptance Criteria

**Case: the second-sibling question**

1. *when* a feature delta adds a second member of a kind an existing surface already has — the same gesture, overlay shape, or one-sentence role — the system *shall* draw the scoped design review over the delta's elements against the existing inventory. [INV-169, INV-141]
2. *when* a delta adds no such sibling, the system *shall* hold the intake stand-down and record the no as a lens verdict in the feature-fit record. [INV-169, INV-29]

**Case: the closed window**

3. The system *shall* close the window a second sibling entered by drawing this pass at intake, the same channel the uniformity lens and the motion-parity lens were born from. [INV-169, INV-125, INV-165]

---

## Requirement 64: A re-enterable surface triggers the prover's entry-state lens

**Context:** The prover reasons in states, transitions, and initialization, so a surface a visitor can leave and re-enter carries a standing lens the prover runs by construction. The entry-symmetry lens tests that a re-entry path exists; this lens tests the state that re-entry opens in.

**User Story:** As a person shipping a re-enterable surface, I want the prover's entry-state lens run by construction, so that a spec pinning the open, exit, and guards while leaving the entry position and reset-or-resume blank raises an open question before code.

### Acceptance Criteria

**Case: the entry state the lens demands**

1. *when* a surface can be left and re-entered, the system *shall* have the prover demand the spec declare where the surface opens focused or positioned and whether entering resets its internal state or resumes the state a prior visit left. [INV-167, INV-1]
2. *when* the spec pins the open ceremony, exit, variants, and guards while the entry position and reset-or-resume semantics stay blank, the system *shall* raise the unstated transition end-state as an open question before any code is written. [INV-167, INV-50]

**Case: the lens hands off once declared**

3. *when* the human declares the entry state a spec sentence, the system *shall* let the prover's ordinary state-coverage hold it. [INV-167, INV-125]

---

## Requirement 65: Every stated transition carries a payload lens

**Context:** The prover verifies the state graph's topology — that a way in, a way out, and a way back exist. Beside topology it reads each transition's payload: the parameters a person perceives across it. A parameter the spec leaves blank is answered by the platform's own default alone, so the payload a transition carries is the hole the topology lenses miss.

**User Story:** As a person specifying a transition, I want each one's perceived payload enumerated and demanded, so that a parameter left to the platform default becomes a finding, surfaced before it can silently become the behaviour.

### Acceptance Criteria

**Case: enumerate and demand each payload parameter**

1. *when* the prover reads a stated transition, the system *shall* enumerate the parameters a person perceives across it — where focus and selection land, what scroll or playback position holds, whether sound continues, whether a timer keeps running, whether a shown value is fresh or stale — and demand the spec name each. [INV-168, INV-72, INV-127]
2. The system *shall* raise each unstated payload parameter as an open question, the author writing it as a spec sentence or the human deciding it where the choice is theirs alone. [INV-168, INV-30]

**Case: the lens generalizes its instances**

3. The system *shall* read the motion-parity lens as this lens on the exit's animation and the entry-state lens as this lens on a re-entry's internal state, both instances this parent generalizes. [INV-168, INV-165, INV-167]

---

## Requirement 66: A surface add re-verifies the document's quantified claims

**Context:** A new surface falsifies existing document-level sentences without touching them: a class clause's member enumeration excludes the newcomer, a sentence quantified over every, only, all, or exactly one ranges over a set that just grew, and a previously terminal scenario's decided edge may no longer be terminal. A seam-scoped pass misses these, so the cross-link mode carries one mandatory whole-document step.

**User Story:** As a person adding a surface or a member, I want the document's quantified claims re-verified against the grown set, so that a sentence the newcomer falsifies is a finding at the add itself, ahead of the next full pass.

### Acceptance Criteria

**Case: the quantifier re-verify**

1. *when* a surface is added, the system *shall* have the cross-link mode sweep the document for enumerations and universal quantifiers, and re-verify each such sentence against the surface set that now includes the newcomer. [INV-170, INV-125, INV-127]
   - the quantifiers it sweeps for are every, only, all, and exactly, and the enumerations are the explicit member lists.
2. The system *shall* fire the step on every member add, and *shall* re-verify the same way in the full pass's own sweep. A surface add is one kind of member add. [INV-170, INV-169, INV-171]
   - a member add covers a new invariant joining a family, a new skill joining the pack, and a second sibling the intake question catches.

---

## Requirement 67: A full prover pass owes a coverage record

**Context:** Phase-level prose proves nothing about which lenses actually ran, and on a kind where the classic coverage tables all go not-applicable a skipped lens is indistinguishable from a lens that found nothing. The prover's stress lenses therefore split into three tiers. Each mandatory sweep owes one verdict line, and the imaginative probes owe none. The class lens is the third tier, the standing sweep that owes one record line every pass.

**User Story:** As a person trusting a full prover pass, I want each mandatory sweep to owe one verdict line rendered as a surface-by-sweep table, so that a missing verdict reads as a skipped sweep, its absence never passing for a clean one.

### Acceptance Criteria

**Case: the mandatory sweeps owe verdicts**

1. The system *shall* have each mandatory sweep — the declared-laws walk, edge-condition completeness, cross-surface uniformity, the lifecycle sweep under the transition-payload parent, and the unwritten-seams derivation — owe one verdict line in the persisted record: hit, clean, or not-applicable with its reason. [INV-171, INV-101, INV-138, INV-125, INV-168, INV-50, INV-167, INV-126, INV-127, INV-72]
2. The system *shall* render the verdicts as a surface-by-sweep table, the replacement for the coverage tables on a kind where those go not-applicable, and leave the imaginative probes — the checks the prover invents for the particular document beyond the mandatory sweeps — discretionary owing no verdict. [INV-171, INV-135, INV-156]
3. *when* a verdict line is missing, the system *shall* read it as a skipped sweep and never as a clean one. [INV-171]

**Case: the class line the record carries**

4. The system *shall* have every pass write one class line in its record, beneath the verdict table. The line *shall* read swept with the classes filed, no class, or not-applicable with its reason. [INV-171, INV-124]

---

## Requirement 68: Every review pass writes its record of one class

**Context:** A review pass — the prover's spec re-check, the design review, the periodic adversarial audit (the fresh-checker read run over a high-stakes delivery, set on refuting its claims and finding its holes; its cadence and rules live in the rules section of this document), and the verify-by-deed audit — records its outcome so a later session reads every pass the same way. Three of them write a dated file of one shared shape under the pass's own home, and the verify-by-deed audit is the one deliberate difference.

**User Story:** As a later session reading past passes, I want each review pass to write its record of one class with a per-finding disposition column, so that the prover, the design review, and the audit read the same way and the verify audit's difference is named.

### Acceptance Criteria

**Case: the shared record shape**

1. The system *shall* have the prover, the design review, and the periodic audit each write a dated file of one shared shape under its own home. [INV-156, INV-140, INV-141, INV-145]
   - the file names the skill and version that ran the pass;
   - it carries a per-finding disposition column;
   - it takes a same-day suffix so two passes never overwrite.
2. The system *shall* land a feature-fit record in the prover's own home in this shape, and give the design review alone a held-ask home since it alone carries a question across passes. [INV-156, INV-29, INV-169, INV-142]

**Case: the verify audit's difference, and forward binding**

3. The system *shall* land the verify-by-deed audit's verdict and its per-landing skill-creator review in the landing record, since verify is a per-landing gate and keeps no dated file of this class. [INV-156, INV-46, INV-99]
4. The system *shall* have a new review pass state its record against this class and *shall* leave records written before the class was declared unreshaped. [INV-156, INV-159]

---

## Requirement 69: Every design review finding carries a confidence read, and a strong likely one becomes one question

**Context:** Each design review finding carries a confidence read of confident or likely. A confident finding is written as a recommendation that queues and never blocks; a likely finding is written as one question to the human with both objects in hand, raised only when the signal is strong. At most three such questions ride per pass, strongest first, and an unanswered question is held quietly for the person.

**User Story:** As a person the design review would ask, I want a confident finding queued and a strong likely one raised as one batched question, so that the strongest genuine questions reach me without the lane ever waiting on them.

### Acceptance Criteria

**Case: confident queues, likely asks**

1. The system *shall* write a confident finding as a recommendation that queues and never blocks, a finding being confident *when* the reviewer would defend the grouping and the divergence on the spec text alone. [INV-142, INV-140]
2. The system *shall* write a likely finding as one question to the human with both objects and each object's spec sentence, raised only *when* the shared role fits one plain sentence, the difference is a whole behaviour one member lacks, and no spec sentence already decides it. [INV-142, INV-141]

**Case: the batched channel and the held question**

3. The system *shall* ride these questions on the batched report, at most three per pass strongest first, holding a signal below that bar silent. [INV-142, E-22, INV-4]
4. The system *shall* not apply the recommended default to the spec the pack's usual proceed-on-recommended way, landing the class sentence only on the human's word while the lane never blocks. [INV-142, INV-4, INV-141]
5. *while* a question stands unanswered, the system *shall* hold it on the dated record and not raise it again on its own until the human answers, each pass first reading the open questions and dropping a freshly-derived divergence already carried there. [INV-142, INV-130]

---

## Requirement 70: The prover and the design review iterate to a bounded fixed point

**Context:** The prover and the design review form a loop over repeated rounds. A round is one prover re-read of the changed part of the spec followed by one design-review re-read over the current spec. Only a human-accepted declaration advances the loop, and it is capped at three progressing rounds by default. On reaching the cap the loop surfaces the unsettled groupings without holding the landing.

**User Story:** As a person watching the design settle, I want the prover and design review to iterate to a bounded fixed point and surface non-convergence without holding the landing, so that a design converges in the ordinary case and a live cap keeps the loop from running away.

### Acceptance Criteria

**Case: what advances the loop**

1. The system *shall* advance the loop only on a human-accepted declaration — a class sentence over a grouping or a decided sentence over a difference — re-reading the changed part and the re-partitioned elements in the next round. [INV-154, INV-125, INV-59]
2. The system *shall* not advance the loop on a confident finding queued as a recommendation or a likely finding riding as a question, since neither re-reads the spec on its own. [INV-154, INV-142]

**Case: the loop rests with a named reason**

3. *when* a round produces no new class sentence and no new decided sentence, the system *shall* rest the loop and name why in the record — it converges when the design review left no open question and no new grouping, it waits when a question stands unanswered, and it stands down when no element a person acts on exists. [INV-154, INV-141, INV-142]

**Case: the cap and the surfacing**

4. The system *shall* cap the loop at three progressing rounds by default, let a host set its own cap, and count progressing rounds on the design-review pass alone, resetting when a fresh pass opens. [INV-154]
5. *when* the loop reaches the cap without convergence, the system *shall* surface the unsettled groupings on the dated record with its best reading of the cause, and *shall* let the landing proceed with the unsettled groupings recorded. [INV-154, INV-141]

---

## Requirement 71: A taste choice made without asking is told, never confirmed

**Context:** While building a feature, the walk makes small taste calls itself so the lane keeps moving — an animation's speed, a button's shape, a caption's wording. The agent writes each into the spec with its `[default]` tag, names it in the delivery report, and re-asks nothing later.

**User Story:** As a person whose feature carries small taste calls, I want each one told in plain words with an example and marked tweakable rather than confirmed, so that the lane keeps moving and every such choice stays findable.

### Acceptance Criteria

**Case: told with an example, marked tweakable**

1. *when* the walk makes a taste call without asking, the system *shall* write it into the spec with its `[default]` tag and name it in the delivery report in plain words with an example, marked tweakable. [INV-31, INV-18]
2. The system *shall* request no confirmation and re-ask nothing later, since silence is consent, and *shall* keep every such choice findable by its `[default]` tag so the person can ask when they want it changed. [INV-31]

---

## Requirement 72: A tunable parameter is set to a default and told, never asked

**Context:** Some choices are a mechanical knob with a range — an image's resolution, a batch size, a timeout, a sampling rate. The walk sets each knob itself and keeps the lane moving, writing it with its `[default]` tag and naming what it trades in the delivery report.

**User Story:** As a person whose feature carries tunable knobs, I want each set to a default and reported with what it trades rather than asked, so that the agent never stalls on a knob it can set and I tune it afterward only if I want a different point.

### Acceptance Criteria

**Case: set, tagged, and told**

1. *when* the walk meets a tunable knob, the system *shall* set it to a default value, choosing the cheaper or faster point wherever quality allows, write it with its `[default]` tag, and name in the delivery report what it trades. [INV-70, INV-31, INV-18]
   [GAP: the quality bar that permits the cheaper point is unstated in the source.]
2. The system *shall* owe no re-ask, letting the human tune the knob afterward and updating it together at most, the same idea the economy ladder applies to cost. [INV-70] [T-19]

**Case: the agent moves every task it can**

3. The system *shall* move every task it can and reserve a question for what it genuinely cannot decide. [INV-70, INV-4]
4. *where* the human has granted it, the system *shall* ship to production on its own certification once the work is sound, keeping the grant the human's to give or withdraw. [INV-70, M-6, INV-9]

---

## Requirement 73: The smallest sample is judged before the full artifact

**Context:** For a taste-heavy deliverable — voice, copy, visual style, spec prose — the build stops at the cheapest judgeable sample: one paragraph, one card, two sections. The human's word on that sample sets the bar before the full build spends anything. This is the agent's own discipline, distinct from a declared show-me-first entry condition.

**User Story:** As a person whose deliverable is taste-heavy, I want the smallest judgeable sample put before me before the full build, so that my word sets the bar before the full build spends anything.

### Acceptance Criteria

**Case: the cheapest judgeable sample first**

1. *when* a deliverable is taste-heavy, the system *shall* stop the build at the cheapest judgeable sample — one paragraph, one card, two sections — and take the human's word on that sample before the full build spends. [INV-62]
   [GAP: the boundary classifying a deliverable as taste-heavy is unstated in the source; the source names examples (voice, copy, visual style, spec prose) and no closed test.]
2. The system *shall* build smallest first as the agent's own discipline even unasked, distinct from the human's declared show-me-first entry condition. [INV-62, INV-43]

---

## Requirement 74: A rejected artifact reopens its source

**Context:** When the human rejects an artifact, the fix starts at the artifact's source — the spec clause, the card, or the brief that produced it. Patching the rejected output line-by-line against an unchanged source is the five-round trap by name, and it is banned.

**User Story:** As a person rejecting an artifact, I want the fix to reopen its source and rebuild from it, so that the correction lands at the root rather than looping the same rejection against an unchanged source.

### Acceptance Criteria

**Case: correct the source, rebuild from it**

1. *when* the human rejects an artifact, the system *shall* correct its source — the spec clause, the card, or the brief — first and rebuild the artifact from it. [INV-63]
2. The system *shall* ban patching the rejected output line-by-line against an unchanged source, the five-round trap by name. [INV-63]

---

## Requirement 75: What already works is fenced before it is touched

**Context:** When a feature-doored wish touches a surface that already lives, its spec-delta opens with regression fences before the facet sweep authors anything new. A fence is one sentence for a neighbouring promise that must stay true through the change, citing the existing clause it guards. The delta splits everything it touches in two: promises that stay are fenced and untouched, behaviour being changed is re-authored as new law.

**User Story:** As a person changing a live surface, I want its neighbouring promises fenced and cited before anything new is authored, so that fixed one thing and quietly broke the neighbour turns red before it ships.

### Acceptance Criteria

**Case: the fence and what it guards**

1. *when* a feature-doored wish touches a surface that already lives, the system *shall* open its spec-delta with regression fences before the facet sweep authors anything new, each fence one sentence for a neighbouring promise that must stay true and citing the existing spec clause it guards. [T-14]
2. The system *shall* earn no new test-matrix row for a fence, discharging it through the cited clause's own never-side and proving the fence held by the landing's full-suite run. [T-14, INV-19, INV-6]

**Case: an unwritten promise, and where fencing belongs**

3. *when* a fence finds no clause behind it, the system *shall* reconcile the discovered promise from the shipped truth like an adopted claim, write it as its own spec fact with its own row, and surface it rather than silently assume it. [T-14, A-3, INV-5]
4. The system *shall* name the wish's fences by the anchors they cite in the queue row, keep fence-authoring to the feature door, let the bug and refactor doors inherit only the catching, and fence nothing on a prototype since it promises nothing. [T-14, T-7, E-17]

---

## Requirement 76: A feature says its non-goals and its success measure

**Context:** Every feature's spec-delta closes with two short sentences, both always written: the non-goals, what is deliberately left out, and the success measure, how the feature's working would be noticed for its person. A non-goal that narrows what the wish asked for is a scope decision, and a success measure derives no test-matrix row.

**User Story:** As a person closing a feature's spec, I want its non-goals and its success measure both written rather than left silent, so that what the feature excludes is on the record and how we would notice it worked is a written promise.

### Acceptance Criteria

**Case: the two sentences, always written**

1. The system *shall* close every feature's spec-delta with a non-goal sentence and a success-measure sentence, both always written, taking nothing deliberately left out this time as a valid non-goal and reading only a missing sentence as a hole. [INV-20, INV-21]
2. *when* a non-goal narrows what the wish asked for, the system *shall* ride it on the batched report as a stated scope decision. [INV-20, INV-4, INV-5]

**Case: the success measure carries no row**

3. The system *shall* write the success measure decided or `[default]`-tagged with a number where one exists, derive no test-matrix row from it, and keep it a written promise the human checks by eye until the reading machinery ships. [INV-21, INV-18]
4. The system *shall* bind both sentences forward from features specified after this rule, owe an adopted feature its pair at the first landing that touches it, and write neither on a prototype. [INV-20, INV-21, A-3, E-17, INV-159]

**Case: the reading machinery is promised**

5. The system *shall* keep the success-measure reading machinery promised under its own queue row. [INV-21]
   [target]

---

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

**Case: the config-health net is promised**

5. The system *shall* keep the config-health check on the primary tree holding main promised, git's refusal the net until it ships. [INV-198]
   [target]

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

**Case: the pre-gate checks are promised**

5. The system *shall* keep the merge-base check ahead of the gate and the stale-lane check promised, the prover's station their net until then. [INV-199]
   [target]

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
4. The system *shall* red a host whose project instructions carry no worktree line at the adoption gate, a mechanical gate the prover's station stands as until the build lands. [INV-201, INV-150]
5. The system *shall* require no vendored line for a worker lane, since the subagent's isolation option carries no gate. [INV-201, E-34]

**Case: the adoption gate is promised**

6. The system *shall* keep the adoption gate for the host's worktree line promised, the prover's station its net until then. [INV-201]
   [target]

---

## Requirement 89: The cap holds at three, and across sessions the pen's arbitration fires

**Context:** The lane cap is the profile-declared value with a package default of three. The branch road removes the tree's cost — a lane writes no tree another lane reads — but the three costs that bound the cap survive untouched, so the tree was never what bound it. The lanes law does not fire across sessions, and that sentence scopes the cap, the board, and the independence judgment; the pen's arbitration fires across sessions and always did.

**User Story:** As a person running lanes, I want the cap held at its declared value and the pen's cross-session arbitration recognized, so that removing the tree's cost is no reason to raise the number and two sessions on one repo need no new law.

### Acceptance Criteria

**Case: the three surviving costs hold the cap**

1. The system *shall* hold the cap at its declared value, three by the package default and by the profile line, since the branch road touches none of the three costs that bound it — pen-wait, the rebase-and-re-gate work every landing forces on every rolling lane, and the orchestrator's dividing review attention. [T-18, E-13]
2. The system *shall* proceed on this recommendation while the owner's word on raising the cap stays owed, naming the measurement the pack has not taken — pen-wait time per lane and re-fences per landing. [T-18, INV-4]

**Case: the pen arbitrates across sessions**

3. The system *shall* scope the cap, the board, and the independence judgment to one session and *shall* fire the pen's arbitration across sessions, a foreign session's claim commit on main being readable with no fetch. [T-18, INV-198, INV-2]
4. *when* a second session takes a lane on one repo, the system *shall* give it its own worktree and branch under the stated road with no new law, since two worktrees share one object store and one set of refs. [T-18, INV-11, INV-117]

---

## Requirement 90: The branch road's machines, and what each one owes

**Context:** The branch road stands on machines. Two are git's own and run today, each guarding a road a session walks by habit; four are the road's build half and stand until the build lands, with the prover's station as their net meanwhile. The road states each machine's boundary rather than hiding it, so it claims no net it does not hold.

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

## Requirement 97: What the wishes grow is the spec

**Context:** What the wishes grow is the spec, the living statement of what the product is, where one surface carries one name everywhere.

**User Story:** As a person reading what the wishes built, I want them to grow one living spec with one name per surface, so that the whole team reads one current truth rather than scattered descriptions.

### Acceptance Criteria

**Case: one living statement, one name per surface**

1. The system *shall* grow the spec as the living statement of what the product is, naming each surface one way everywhere. [E-4]

---

## Requirement 98: A prototype is a fenced sketch that carries its label  [feature: F-prototype]

**Context:** Exploring an idea before committing to it is allowed, and a prototype is that exploration kept as a sketch. It lives fenced off in its own clearly named home, and the fence runs one way — influence crosses out of the prototype and never into the shipped product. Every artifact the prototype produces announces itself.

**User Story:** As a person exploring an idea, I want the sketch fenced off and labelled in whatever form its kind can show, so that a try-it-out experiment never leaks into the product a user meets.

### Acceptance Criteria

**Case: the label rides every artifact**

1. *when* a prototype produces an artifact, the system *shall* mark it with the `PROTOTYPE` label in the form its kind can show — an on-screen banner for a rendered page, a `_prototype: true` field or header for an API or data payload, a first-line banner for a script, and the marker in the name or header line for a bare file. [E-17]
2. The system *shall* keep the prototype's code sitting apart in its own named home, with nothing in the shipped product reaching into it. [E-17]

**Case: the fence runs one way**

3. The system *shall* let influence cross out of a prototype and never into a prod surface: never wiring a prototype into a prod surface, never linking to a prototype from a prod surface, and never styling a prod surface to match a prototype. [INV-17]
4. *when* a prototype is shown to the human, the system *shall* show it only under its label, and *shall* let nothing reach the human as the product until its surface has walked the full pipeline. [E-17, INV-17]

---

## Requirement 99: The door step decides a feature from a sketch

**Context:** The boundary between a feature and a sketch sits at the door step, the point where a request becomes a product feature. A wish to have something in the product is a feature and walks the pipeline; a request to merely see or try something, with no commitment, may live as a sketch inside the fence. When the door is unclear, the agent asks rather than guesses.

**User Story:** As a person voicing a request, I want the door step to sort a feature from a sketch by a fixed rule, so that a commitment gets a spec and a lane while a no-commitment try stays a free sketch.

### Acceptance Criteria

**Case: the boundary at the door**

1. *when* a wish asks to have something in the product, the system *shall* read it as a feature and route it through the build pipeline. [INV-16]
2. *when* a request asks only to see or try something with no commitment, the system *shall* let it live as a sketch inside the fence, carrying no lane through the build pipeline and no spec. [INV-16, E-17]

**Case: the unclear door asks**

3. *if* which of the two was meant is unclear, *then* the system *shall* ask one plain question and *shall* not guess. [INV-16]

---

## Requirement 100: Opening a prototype home is a repo write

**Context:** A prototype home is a folder or branch, and creating it writes to the repository like any other write. So the write-ownership law governs it, the assigned seat makes the judgment call, and a session working from outside files an inbox wish rather than opening the home itself.

**User Story:** As a maintainer of the repository, I want opening a prototype home held to the write-ownership law, so that a worker never opens a prototype home on its own brief and an outside session routes through the inbox.

### Acceptance Criteria

**Case: the write is owned**

1. *when* a prototype home is opened, the system *shall* govern that write by the write-ownership law and *shall* leave the judgment call to the assigned seat. [INV-10, ACT-2]
2. *when* a session works from outside the assigned pack session, the system *shall* have it file an inbox wish rather than open a prototype home on its own brief. [INV-10]

---

## Requirement 101: Promotion enters a sketch's earned feature at the spec step

**Context:** When a sketch earns its place, its feature enters the pipeline at the spec step like any wish, without its code being merged. The prototype serves as evidence for that spec, and its code holds no rights.

**User Story:** As a person promoting a proven sketch, I want its feature to enter at the spec step with the code left behind, so that the earned idea is specced fresh and the sketch's code claims nothing.

### Acceptance Criteria

**Case: the earned feature is specced fresh**

1. *when* a sketch earns its place, the system *shall* enter its feature at the spec step like any wish and *shall* not merge the sketch's code. [T-12, INV-16]
2. The system *shall* treat the prototype as evidence for that spec, its code holding no rights. [T-12]

---

## Requirement 102: The fence guardrail's three legs and the header's honesty

**Context:** A guardrails check enforces the one-way fence, and it has three legs. One leg runs live today; two are promised targets. When all three land, the header's honesty rule holds in both directions — the spec never claims what is not built, and the build never contains what the spec does not name.

**User Story:** As a person trusting the fence, I want a mechanical check with three named legs and one honest note of which run today, so that a prod file reaching into a prototype turns red while the promised legs are marked as still owed.

### Acceptance Criteria

**Case: the three legs**

1. *when* a prod file references anything inside a prototype home, the system *shall* turn the fence leg red. [E-6]
2. The system *shall* enforce the completeness scan over the surface registry and the behaviour-traces-to-spec check as the two remaining legs. [E-10, E-6]
   [target]

**Case: the honesty in both directions**

3. *when* all three legs land, the system *shall* hold that the spec never claims what is not built and the build never contains what the spec does not name. [S-0, INV-17]
4. *while* only the fence leg is enforced, the system *shall* keep the other two legs promised, marked, and owned by their rows. [INV-17]
   [target]

---

## Requirement 103: An approved look is frozen as the norm its clause cites

**Context:** Prose alone cannot record how a design looks and feels, so a rebuild made from prose with no artifact to check against can pass every test and still ship a look-alike. Once the human approves a sketch as the look, that prototype becomes the norm for look and feel. The clause it governs cites the frozen artifact, and approval freezes a dated copy into the project's records.

**User Story:** As a person who approved a look, I want the approving clause to cite a frozen copy of the artifact, so that a later rebuild is checked against the frozen artifact itself.

### Acceptance Criteria

**Case: the clause cites its artifact**

1. *when* a clause is governed by an approved look, the system *shall* place a norm pointer of the form `norm: <path>` at the clause's line end beside its anchors, the prose carrying the laws and the artifact keeping the look. [INV-43]
2. *when* a sketch is approved as the look, the system *shall* freeze a copy into `docs/norms/` with a dated provenance line naming what it is, when it was approved, and which sketch it came from. [INV-43]

**Case: the pointer never reaches a live sketch**

3. The system *shall* have the norm pointer cite the frozen copy and *shall* never let it reach into a live prototype home, so the one-way fence stays absolute and the sketch stays free to die. [INV-43, E-17, INV-17]

---

## Requirement 104: The build and the prover read the norm

**Context:** A norm is only as good as the reads that enforce it. When a surface's clauses carry a norm pointer, the build opens the artifact before writing code and records a plan-versus-prototype diff; the verify feel pass reads the same pointer; and the prover reads visual clauses with a norm lens. A story may also demand the human see a mockup before the build starts.

**User Story:** As a person guarding an approved look, I want the build, the verify pass, and the prover all reading the norm pointer, so that a missing line is caught at the code step and a pointerless prototype-born clause is flagged.

### Acceptance Criteria

**Case: the build reads the artifact**

1. *when* a surface whose clauses carry a norm pointer is built, the system *shall* open the artifact before the code step and *shall* record a one-line plan-versus-prototype diff in the delivery report, a missing line being a defect caught at the code step. [INV-43]
2. The system *shall* have the verify step's feel pass read the same norm pointer. [INV-43, INV-30]

**Case: the prover's norm lens**

3. *when* the prover reads a visual clause, the system *shall* flag a prototype-born clause carrying no pointer, and *shall* flag a clause whose text contradicts its own artifact. [INV-43]

**Case: the mockup-first entry condition**

4. *when* a story declares a mockup-first requirement, the system *shall* write `entry: mockup-first` on the queue row and *shall* hold it at the door step until the human cancels it by name. [INV-43]
   - a mockup-first requirement is the human needing to see a mockup before the build starts;
   - a general instruction to build moves priority without cancelling this entry.

**Case: the pointer binds forward only**

5. The system *shall* add a clause's pointer at the first landing that touches it and *shall* never apply pointers retroactively across the whole spec at once. [INV-43, INV-159]
6. The system *shall* place a pointer only for a prototype the human approved as the look, leaving an unapproved sketch as plain evidence in its fence and a text-born clause with no pointer. [INV-43, E-17]

---

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
4. The system *shall* fail the run on a surviving file through a session-scoped before-and-after diff of the temp home, the harness's own launch sweep clearing a prior run's litter that its own teardown never reached. [INV-100]

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

## Requirement 129: Human-facing prose is drafted by a clean writer

**Context:** Any text a human will read is drafted by a fresh writer session that does not have the package rules loaded — documentation pages, product-spec prose, reports, decision pages, product copy, and the package's own rule texts while being edited. The rules-loaded session writes a plain brief carrying the facts, the reader, and the register laws; the writer returns the draft; the rules-loaded session reviews and lands it. A blanket rewrite of settled text is refused.

**User Story:** As a person reading the pack's durable prose, I want it drafted by a fresh writer from a plain brief, so that human-facing writing stays clear of the insider register and settled text stays stable.

### Acceptance Criteria

**Case: the clean-writer road**

1. *when* durable human-facing prose is written or a section of it is edited, the system *shall* have a fresh writer session draft it from a plain brief carrying the facts, the intended reader, and the register laws, then review and land it in the rules-loaded session. [INV-84]
2. The system *shall* bind the road to the section the edit touches and *shall* redraft a whole page only on the human's word. [INV-84]

**Case: what rides the ordinary hand**

3. The system *shall* let a report typed live in chat stay the session's own words under the register laws, and *shall* let a mechanical correction ride the ordinary hand as no drafting. [INV-84]
   - a mechanical correction is a typo, a broken link, or a version number.
4. The system *shall* refuse a blanket rewrite of settled text, since meaning can shift during a bulk restructure. [INV-84]

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

## Requirement 143: A publish owes the reader what the artifact's kind owes  [feature: F-publish]

**Context:** Sooner or later a piece of work leaves the machine — a repo goes public, a skill enters a plugin directory, a release is cut, rendered cards go to a design project. The work-kind axis used at wish intake applies again at the door of publishing, and each kind owes its reader a different minimum.

**User Story:** As a person publishing an artifact, I want its kind to set the minimum it owes its reader, so that a skill shows its commands, a tool shows real runs, a visual product shows fresh screenshots, and prose shows its reading path.

### Acceptance Criteria

**Case: each kind owes its minimum**

1. *when* a piece of work is published, the system *shall* apply the work-kind axis at the door of publishing and owe the reader the minimum that kind owes. [T-16]
2. The system *shall* have a skill show how to install it, the commands to run, and when to use it and when not; a tool show real runs with real output; a visual product show fresh screenshots; and prose show its reading path. [T-16]

**Case: a comparison earns its place**

3. The system *shall* let a comparison or a diagram join only when it carries the argument, never as decoration. [T-16]
   [GAP: the judge of carries-the-argument versus decoration is unstated in the source.]

---

## Requirement 144: The publish skill owns the checklist, run before the gate

**Context:** The publish skill owns the per-kind checklist, and this spec sets the contract it follows. Nothing is deposited outward without passing the checklist first, and its result rides the delivery report. The checklist never bypasses the gates already standing — the human's publish gate and the host's push gates — and it runs before the gate, so by the time the human approves it is already worth approving.

**User Story:** As a person depositing outward, I want the publish checklist run before the human's gate, so that nothing leaves unchecked and the gate approves work already worth approving.

### Acceptance Criteria

**Case: the checklist is the one home**

1. The system *shall* have the publish skill own the per-kind checklist and *shall* deposit nothing outward without passing it first, the walk's result riding the delivery report like any other step. [E-20, INV-22]

**Case: the standing gates hold**

2. The system *shall* keep the human's publish gate over anything irreversible or outward and the host's push gates over the push, the checklist never bypassing them. [E-20, ACT-1, M-6]
3. The system *shall* run the checklist before the gate, so by the time the human approves it is already worth approving. [E-20]

---

## Requirement 145: Each publish target embeds its own steps

**Context:** Each publish target is a plugin that embeds its own steps into the walk. The target adds steps and never removes the kind's owed minimum.

**User Story:** As a person publishing to a named target, I want the target to add its own steps without removing the kind's minimum, so that a destination's demands ride on top of what the reader is already owed.

### Acceptance Criteria

**Case: the target adds, never removes**

1. *when* a publish target joins the walk, the system *shall* embed its own steps — a README at the door plus release notes for a code host, a manifest and forms for a plugin directory, its cards for the design project. [E-18]
2. The system *shall* have the target add steps and *shall* never let it remove the kind's owed minimum. [E-18]

---

## Requirement 146: A version push re-opens the shopfront

**Context:** Every push that ships a new version changes the truth a public reader will read tomorrow, even when the diff never touched a doc, so the shopfront rides every push. The README's claims still have to match the truth just pushed, and the kind-owed visuals ride along. A stale shopfront is a false claim, exactly like a stale screenshot.

**User Story:** As a public reader, I want every version push to re-check the README and its kind-owed visuals against the pushed truth, so that I never meet an out-of-date front.

### Acceptance Criteria

**Case: the shopfront rides every push**

1. *when* a push ships a new version, the system *shall* re-check the README's claims — behaviour, counts, commands, version homes — against the truth just pushed, even where the diff touched no doc. [INV-44]
2. The system *shall* have the kind-owed visuals ride along — a skill pack re-checking its diagrams, a visual product re-shooting what changed on screen, a tool re-running its example. [INV-44]

**Case: one home, its outcome recorded**

3. The system *shall* read this shopfront check as the publish checklist at push scale, the commit-and-show step pointing at it and the walk's outcome riding the delivery report. [INV-44, INV-22, E-20]
4. *when* a push's changes touch none of the shopfront's claims, the system *shall* say so in one line and *shall* fix a stale claim before the push, freshness resting on the claims themselves, styling aside. [INV-44]

---

## Requirement 147: Everything built with the method carries its attribution line

**Context:** Every publication of an artifact built with the pack carries one attribution line, `made with live-spec` linking to the pack repo, on the publication's landing surface. The line names the pack version the project runs, read from the host's attach record, so it doubles as the adoption tracker. The line is an offer, never a gate — the owner's taste rules his own shopfront.

**User Story:** As a person publishing built-with work, I want one attribution line offered on its landing surface naming the pack version, so that who runs the method is readable from the shopfronts while the owner keeps the final say.

### Acceptance Criteria

**Case: the line and its version**

1. *when* a built-with artifact is published, the system *shall* carry one attribution line on its landing surface — the README footer, and for a skill also its `SKILL.md` — naming the pack version read from the host's attach record at write time. [INV-96]

**Case: an offer, never a gate**

2. The system *shall* treat the line as an offer, the publish walk checking for it and proposing it once when absent, the owner's word deciding and a declined offer staying closed. [INV-96, INV-16]
3. The system *shall* apply the line to each built-with project through its own queue and *shall* stamp it onto each standalone mirror from the live `VERSION` file at every sync, since a hand-written footer on a mirror would carry an invented number and be wiped by the next sync. [INV-96]

---

## Requirement 148: Every standalone mirror shows its release history

**Context:** A standalone mirror's README carries a release-history section: one line per shipped version giving the version, its date, and a single story line. The sync script harvests those lines from the pack's git history and writes them fresh at every sync, the same way it stamps the attribution line. The full home of each release's story stays the journal.

**User Story:** As a reader of a mirror, I want a generated release-history section refreshed at every sync, so that the public mirror always shows a current history that never drifts.

### Acceptance Criteria

**Case: the generated history**

1. The system *shall* carry a release-history section on a standalone mirror's README, one line per shipped version giving the version, its date, and a single story line, harvested from the pack's git history and written fresh at every sync. [INV-181]
2. The system *shall* keep the journal as the one full home of each release's story, the mirror section pointing back to it, and *shall* keep the history on the README alone while the mirror's `SKILL.md` stays free of reader-facing blocks. [INV-181]

**Case: the generated blocks are one pinned kind**

3. The system *shall* read the mirror's generated blocks as one declared kind with three members — the read-only banner at the README's top, this release-history section, and the attribution line — each pinned by a test, and *shall* let the owner's word move the section to a generated changelog file. [INV-181, INV-96]

---

## Requirement 149: Shipped product docs state each requirement impersonally

**Context:** A product's shipped docs — the spec, the test matrix, the README, a skill card — reach everyone the project touches. Each requirement reads as three plain parts: the rule, the actor as a role, and the reason it holds. The reason stays because a reader has to know why the rule stands, while the personal attribution drops; a dated decision keeps its date as a plain anchor and drops the name.

**User Story:** As a reader of shipped docs, I want each requirement stated as rule, role, and reason with personal names dropped, so that what ships reads as neutral product truth while the reason a reader can act on survives.

### Acceptance Criteria

**Case: rule, role, and reason**

1. The system *shall* write each shipped requirement as the rule, the actor as a role — the user, the producer, the target user — and the reason it holds, the reason staying and the personal attribution dropping. [INV-118]
2. The system *shall* keep a dated decision's date as a plain anchor while dropping the name, so the provenance a reader can act on survives. [INV-118]

**Case: candid voice has one home**

3. The system *shall* home personal attribution and candid process voice in the local-only diaries that no publish ships, spec-author writing each shipped clause impersonally from the first draft and the publish floor reading the shipped docs for a stray personal name before the deposit leaves. [INV-118]

---

## Requirement 150: A machine holds the shipped tree's language line

**Context:** A shipped artifact carries no Cyrillic outside a user-language string the program deliberately emits, and no personal name in a requirement's statement. The publish gate holds this with a machine that reports each offence as file and line. The name arm reads a declared alphabet, and the specific out-of-alphabet name patterns live as data in an allowlist, so the detector's own source names no person.

**User Story:** As a person shipping an artifact, I want a machine flagging stray script and personal names as file and line, so that the fix is mechanical while candid notes stay in the diaries.

### Acceptance Criteria

**Case: the two mechanical offences**

1. The system *shall* hold that a shipped artifact carries no Cyrillic outside a deliberate program string and no personal name in a requirement's statement, reporting each offence as file and line through `guardrails/check-shipped-language.sh`. [INV-120]
2. The system *shall* read the name arm against a declared alphabet — `ASCII` English plus deliberate program strings — with the out-of-alphabet name patterns held as allowlist data, so the detector's own source names no person and covering a collaborator's name is one data line. [INV-120, INV-114]

**Case: what the shipped set holds**

3. The system *shall* read the shipped text files the delivery holds in its index, a staged file not yet committed included, a file belonging to no delivery staying outside the scan. [INV-120]

**Case: the arms stand down by declaration**

4. *if* a package declares no alphabet, *then* the system *shall* leave the name arm inert while the Cyrillic arm still stands, and *shall* spare deliberate program data and authorship bylines through the same dated allowlist. [INV-120]
   - a new offence still reds, and a listed one counts as debt.

---

## Requirement 151: A core spec names no foreign project and tells no dated incident

**Context:** A core spec — the product spec, the architecture, and the test matrix — states the rule that holds and leaves the project it was first met on and the day it was met to the local-only diaries. A sibling project's name couples the spec to a neighbour it should not know, and a dated-incident turn is history the diaries own. The shipped-language machine gains a project-name arm scoped to the three core specs.

**User Story:** As a reader of a core spec, I want it to state the rule and leave the project and the date to the diaries, so that the spec stays free of cross-project coupling and leaked history.

### Acceptance Criteria

**Case: the project-name arm**

1. The system *shall* red a bare project name in the product spec or the architecture, and *shall* red a project name standing beside a calendar date in any of the three core specs. [INV-245]
2. The system *shall* have the test matrix red a dated incident, while permitting a bare fixture-ledger kind name and a project-name substring of a test-function name. [INV-245]
   - a fixture name that ever falls beside a date still reds;
   - a legitimate fixture name caught that way is waived as counted debt through the dated allowlist.

**Case: the data-held names and the moved history**

3. The system *shall* hold the forbidden project names as data in the shipped-language allowlist so the detector's own source names no project, and *shall* leave the arm inert for a package that declares none. [INV-245, INV-120]
4. The system *shall* move the history a reworded line drops — who met the rule, when, and why — to the journal as a dated entry, the way a dated decision keeps its date while the attribution comes off, and *shall* leave a skill body and the README free to cite a real case since a teaching text names the project a lesson was drawn from. [INV-245, INV-118]

## Requirement 152: Handing feedback back to the workshop  [feature: F-feedback]

**Context:** A person looks at what shipped and something occurs to them. It might be a reaction, an answer, a screenshot with a red circle, or a log file. Feedback is anything a person hands back, at any size and through any channel. Two promises hold over all of it: nothing handed in is ever lost, and every item is answered by a route.

**User Story:** As a person handing something back to the project, I want every item captured and routed to one home, so that nothing I hand in is lost and I never have to hand the same thing in twice.

### Acceptance Criteria

**Case: every item lands in its route's home**

1. *when* a session receives a handed-in item, the system *shall* land it the same session in the home its route owns. [INV-68]
   - a wish lands in its queue row;
   - an answer lands in its decision archive and harvested row;
   - a fix lands in its commit and journal line;
   - workshop noise lands in the problem ledger.
2. *when* an item's route had no prior home — field evidence, a plain reaction, or a wordless drop — the system *shall* record it as one dated line in the feedback ledger. [INV-68, E-28]

**Case: the ledger line and its echo**

3. The system *shall* record each feedback-ledger line with when the item arrived, who handed it in and through which channel, what it concerns on the feature map, the item in plain words, and where it went. [INV-68]
4. *when* an item arrives, the system *shall* echo it back in one sentence, one echo per item, a wish-shaped item taking the wish echo and any other item taking a note stating what was heard and where it went. [INV-27]
5. *if* a person mentions an already-recorded item again, *then* the system *shall* append the new date to the existing line and change nothing else. [INV-68]
   [GAP: the matching rule that decides a new mention is the same item as an existing ledger line is unstated in the source.]

**Case: the promise is checkable**

6. The system *shall* keep every received item findable in the ledger, with its route, in the same session, so the same item never has to be handed in twice. [INV-68]

---

## Requirement 153: The three channels feedback arrives through  [feature: F-feedback]

**Context:** Feedback reaches the project through three channels, and all three meet one contract. A person speaks or types it, comments on something shown, or drops a file. An outside session reaches the project only through the inbox door.

**User Story:** As a person with something to hand back, I want any of the three channels to carry it under one contract, so that the channel I happen to use never changes whether the item is captured and answered.

### Acceptance Criteria

**Case: spoken or typed**

1. *when* a person makes a remark in the conversation or points at a note in a file, the system *shall* receive it as a feedback item on the spoken-or-typed channel. [T-20]

**Case: a comment on something shown**

2. *when* a person comments on a decision page or a review page, the system *shall* capture the answer as saved data, each saved answer being one feedback item whose home is the decision archive and its harvested row. [T-20, INV-4, INV-64]

**Case: a dropped file**

3. *when* a file arrives — a screenshot, a log, or a document — from the person in the conversation or from an outside session through the inbox, the system *shall* take it as one new committed file under the naming and collision law that wishes use, swept in by the host's own session. [T-20, E-11, T-10]
4. *if* a dropped file carries no words, *then* the system *shall* ask one plain question about what it means and *shall* record no guess in the ledger. [T-20]

---

## Requirement 154: Every item takes exactly one of five routes  [feature: F-feedback]

**Context:** Every item takes exactly one route, and each route already has its law and its home. The seam between the product and the workshop decides the last two: the product's behaviour goes to the feedback ledger, the workshop's own behaviour goes to the problem ledger, one home each. The seam turns on what ships: a fault in what the product ships is the product's own, and a fault in the tooling that builds, tests, or runs it without shipping is the workshop's own. A second seam separates the first two behavioural routes from the third: shown work is the artifact in front of the person for review before it lands — a diff, a decision page, a review page — while a shipped feature already carries a scenario in the spec and sits in use. A comment on shown work takes route 2; a reaction to a shipped feature takes route 4.

**User Story:** As a person handing in items of every kind, I want each item sorted to exactly one route with its own home, so that a wish, an answer, a fix, a field reaction, and a workshop hiccup each land where their law already governs them.

### Acceptance Criteria

**Case: the behavioural routes**

1. *when* an item asks for new behaviour, the system *shall* route it as a wish through wish intake with its own echo, door, and row, that row being its home. [T-20, T-12, INV-27]
2. *when* a fix-sized comment lands on shown work, the system *shall* fix it the same session with its commit and journal line as its home, and *shall* queue a story-sized comment as a wish instead. [T-20]
   [GAP: the source names no numeric measure for the size boundary; the glossary's user-story test decides it — a comment naming a distinct new thing a person does and sees is story-sized and queues, and any other comment is fix-sized.]
3. *when* a person answers an open question, the system *shall* harvest it the same session into the decision archive and the harvested row, closing the question for good. [T-20, INV-59]

**Case: the field and workshop routes**

4. *when* a person reacts to a shipped feature, the system *shall* land it as field evidence in the feedback ledger with the line citing the feature's scenario, and *shall* grow it into a wish only on the person's word or a tripwire verdict. [T-20, INV-21]
5. *when* the noise is the workshop's own — a flaky tool, a missing dependency — the system *shall* route it to the problem ledger, and *shall* record a standing behavioural rule's mid-turn break there as one entry the once-read-rules sweep reads. [T-20, INV-23, INV-108]

---

## Requirement 155: feedback-intake receives and never opens a row  [feature: F-feedback]

**Context:** The skill feedback-intake owns this behaviour. It fires the moment a session receives an item, and again at every inbox sweep for any file that carries feedback. It stays quiet when there is nothing to receive, and it holds no verdict of its own on what becomes a queue row.

**User Story:** As a person relying on the pack to catch what I hand in without inventing work, I want feedback-intake to fire on a real handed-in item and stay silent otherwise, so that every item is caught while my passing mentions and the agent's own output never spawn a row.

### Acceptance Criteria

**Case: when it fires**

1. *when* any session receives a handed-in item, the system *shall* run feedback-intake, and *shall* run it again at every inbox sweep for any file that carries feedback. [T-20, T-10]

**Case: when it stays quiet**

2. The system *shall* keep feedback-intake quiet on the agent's own output, on a question the agent asked, and on something a person merely mentions without handing it in. [T-20]
3. *if* it is unclear whether a remark was handed in, *then* the system *shall* ask one plain question rather than record it. [T-20]
4. The system *shall* never open a queue row on feedback-intake's own judgment, the intake door owning that verdict. [T-20]

---

## Requirement 156: A strong reaction earns an offer to note the authors  [feature: F-feedback]

**Context:** The pack carries a third arm beside carrying work out and taking feedback in: an occasional note up to the pack's own authors, so they learn what delighted or hurt real use. The skill feedback-collector owns the arm. It reads the agent's own observation, exactly the moment feedback-intake leaves alone, and the two arms do disjoint work rather than compete.

**User Story:** As a person whose strong reactions could teach the pack's authors, I want a rare one-line offer to send them a note, so that a real delight or hurt reaches the people who wrote the pack while a mild moment passes in silence.

### Acceptance Criteria

**Case: the rare offer**

1. *when* the conversation shows a genuinely strong reaction, the system *shall* offer to send an upstream note. It *shall* stay silent on a mild or routine reaction. [E-30]
   - the offer is one line, made only where the host has switched the upstream-note arm on;
   - such a reaction reads as a real delight, a real hurt, or a comparably notable moment.
   [GAP: the source defers the reading of a strong reaction to a conservative floor and a later design pass, so the measure that separates a strong reaction from a routine one is unstated.]

**Case: the two arms do disjoint work**

2. *when* a person hands in a strong moment, the system *shall* both log its field-evidence ledger line through feedback-intake and, when the moment reads as strong, offer the upstream note through feedback-collector. [E-30, T-20]
3. *when* the agent's own unhanded observation reads as a strong moment, the system *shall* let feedback-collector offer the note while feedback-intake stays silent, since that observation is the arm feedback-intake leaves alone. [E-30, T-20]

---

## Requirement 157: The upstream note is distilled, consented, and deposited  [feature: F-feedback]

**Context:** When the person gives a positive word, the pack writes an upstream note and deposits it; the person delivers it. Consent here is the deliberate opposite of the pack's usual silence-is-consent, because the move is an outbound send about a real person. The arm is off by default and honours its flag on every read.

**User Story:** As a person deciding whether a note about my use travels upstream, I want the pack to send nothing without my explicit yes and to hand me a distilled, anonymized note to deliver myself, so that no private detail leaves the machine on the pack's own and I hold the send.

### Acceptance Criteria

**Case: consent is a positive word**

1. *when* feedback-collector would send a note, the system *shall* ask the person's explicit consent every time and *shall* leave the note unwritten on a silence or an unclear answer. [INV-161, INV-31]
2. The system *shall* keep the arm off by default under its package-default flag, *shall* never fire, read for a strong moment, or ask on a host that has not switched it on, and *shall* turn it on only where a host records a profile line. [INV-161, INV-14]

**Case: what the note holds and where it goes**

3. *when* the person gives a positive word, the system *shall* write a short distilled account that carries its own context to a reader who does not know this user, holding no raw material, transcript, or private content beyond its self-containment test: the note's author strips everything a reader who does not know this user can do without while still understanding the point. [T-21, INV-161]
4. *when* the note is written, the system *shall* deposit it into the host's gitignored outbox directory named by date, *shall* open no network connection and no public request, and *shall* leave the delivery upstream as the person's own step. [T-21, INV-161]
5. The system *shall* anonymize the draft written after the person's positive word, turning the host's real entities into neutral role words while the pack's own public names stay, and *shall* let the note travel only once the person has read and approved that anonymized draft. [INV-179]

**Case: the note's own name and its record**

6. The system *shall* carry this arm's own name, the upstream note, distinct from the station-completion digest (the two or three plain sentences a finished pipeline station's beat carries) and the resume-file digest (the capped restatement of each open leg written into the resume file). [T-21, INV-35, INV-48]
7. The system *shall* record one dated ledger line that an offer was made and answered — when, an upstream-note offer, the person's answer, and the outbox filename when the answer is yes. [INV-161, INV-68]

---

## Requirement 158: Only the assigned session writes the ledger, and it never trims  [feature: F-feedback]

**Context:** The feedback ledger is a shared file. Outside sessions never edit it; they use the inbox door, and only the assigned session appends the ledger. The ledger is append-only and archives like the queue, extending the no-wish-ever-lost law rather than amending it.

**User Story:** As a person trusting the ledger to hold everything, I want only the assigned session to write it and the file never trimmed, so that concurrent work cannot scramble it and no recorded item is ever dropped.

### Acceptance Criteria

**Case: one writer, one door**

1. The system *shall* let only the assigned session append the feedback ledger, and *shall* route every outside session through the inbox door under the write-ownership and concurrent-edit fences. [INV-10, INV-11]

**Case: append-only, never trimmed**

2. The system *shall* keep the feedback ledger a file where nothing is ever deleted or trimmed — a repeat mention adds its date to its existing line — and *shall* archive it like the queue, extending the no-wish-ever-lost law rather than amending it. [INV-1]
3. The system *shall* read a feedback ledger holding only its header as a healthy empty state. [INV-68]

**Case: what this section does not add**

4. The system *shall* add no end-user feedback widget on a host's own product, a site's visitors riding the measurement family or their own wish. [E-28]
5. The system *shall* add no automatic reading, scoring, or aggregation of the ledger, and *shall* reuse the inbox as it stands with no new door mechanics. [INV-68]

---

## Requirement 159: Reading the whole product map on demand  [feature: F-feature-map]

**Context:** Three standing questions describe the product: the departures board reports in-flight status, intake places each new wish on the map, and this ask answers the third — what the product does today. It answers with one map current as of the request, read live from the living documents, kept in no separate file.

**User Story:** As a person asking what the product does today, I want one whole map read live from the spec and the queue on demand, so that I get a current answer with no third document to maintain or drift.

### Acceptance Criteria

**Case: the map is read live, with no third document**

1. *when* a person asks what the product does today, the system *shall* answer with the whole product map current as of the request, read from the spec's scenario sections, the header's current-versus-target paragraph, and the queue's open rows. [INV-38]
2. The system *shall* keep no third document for the map — no feature-list file and no cached copy — the spec's scenarios and the architecture's nodes constituting it. [INV-38, E-14]
3. The system *shall* separate shipped features from promised features at the granularity the target tag binds to — the scenario and its named promised parts, marking a scenario that holds both as shipped with named promised parts. [INV-38, S-0]

**Case: each line and how it is delivered**

4. The system *shall* give each map line its echo-name, what the feature gives its person, and the feature's status followed by its station, per the line law. [INV-38, INV-28]
5. The system *shall* deliver the map in chat by default and as a rendered page on request, *shall* keep routine reports at the departures board's in-flight scope, and *shall* return the whole map only on request. [INV-38, INV-27]

**Case: a host with nothing to read**

6. *if* a host has no spec and no scenario sections, *then* the system *shall* state that condition, direct the requester to bootstrap or adoption, and report only what currently exists. [INV-38]

**Case: the fences and the coverage measure**

7. The system *shall* hold the departures board's report scope, intake's placement rule, and the no-third-document law unchanged. [INV-27, INV-37, E-14]
8. The system *shall* yield a map whose feature set covers the spec's scenario sections one to one plus every open queue row that wish intake marked a new feature while its scenario stays unwritten, its shipped-versus-promised marks agreeing with the header and the target tags. [INV-38, INV-37]

## Requirement 160: A bug preempts the lane, and rolling features park  [feature: F-bug]

**Context:** Mid-feature, the human reports a bug in the shipped product — the card is broken on the phone. The feature in work is set aside at a checkpoint, the bug takes the lane, and once no bug waits the feature returns as the next thing to finish. When nothing is in work, the bug takes the lane directly.

**User Story:** As the product owner, I want a reported bug fixed before anything else while the mid-build feature comes back on its own afterward, so that an urgent defect is handled at once and no in-flight work is lost.

### Acceptance Criteria

**Case: the bug takes the lane, the feature parks**

1. *when* a bug report arrives mid-feature, the system *shall* move the feature to parked with a checkpoint written first — the failing test names when any are red, the current hypothesis, and the touched files — and *shall* commit no work while a test is red. [T-9]
2. *when* the bug holds the lane, the system *shall* run it to completion, and *shall* have an arriving bug join the waiting line and interrupt nothing. [T-9]
3. The system *shall* order waiting bugs critical-first, by the same three conditions the priority mark carries [INV-12], and *shall* order bugs of equal priority by arrival. [T-9, INV-12]
   - a bug is critical when the shipped product is broken for its user.

**Case: resume order and the parking bound**

4. *when* no bug waits, the system *shall* resume parked features ahead of the whole queue. A wish marked critical or quick win may bubble. It jumps only fresh queued wishes. It never jumps a resume. [T-11]
5. The system *shall* park at most one feature per lane, and *when* more than one lane was rolling *shall* park them all, each at its own checkpoint, resuming in their landing order. [T-18]

**Case: a resumed feature re-proves on the new tree**

6. *when* a parked feature resumes, the system *shall* re-fence and re-prove its spec-delta against the now-committed truth before it integrates, since the bug's fix may have moved the law the spec-delta was built against. [T-9, INV-39]
7. The system *shall* integrate no spec-delta proven only against the pre-bug truth without re-verifying it on the new tree, and *shall* leave every parked feature back in work or landed in its original order once the fix has landed, with no red work committed anywhere. [T-9, INV-39]

---

## Requirement 161: A confirmed bug drives a class hunt before it closes  [feature: F-bug]

**Context:** A confirmed bug is one sample of its class. Before the fix is called done, the method drives four moves rather than one — name the class and hunt its siblings, check the architecture, check the spec, and escalate a boundary call to the human — so a point fix that leaves the rest of the class standing is a status, never a landing.

**User Story:** As the product owner, I want a confirmed bug treated as one instance of a class and its siblings hunted before the fix closes, so that the same kind of defect is cleared everywhere it lives, hunted past the one place it happened to show.

### Acceptance Criteria

**Case: name the class and hunt its siblings**

1. *when* a bug is confirmed, the system *shall* name the defect abstractly, then search every surface where that kind could live and fix every sibling found in the same change. [INV-124, INV-56]
   - naming it abstractly means naming the kind of mistake: a scope too narrow, a missing guard, or an assumption that holds in one place and fails in its neighbour.

**Case: check the architecture and the spec**

2. *when* the bug has a structural cause — a boundary the architecture drew wrong or left silent, a node owning what it should not — the system *shall* update the architecture in the same change. [INV-124]
3. *if* the spec is silent on the broken behaviour or under-describes its composition, *then* the system *shall* fix the spec first so the prover can flag it, and *shall* land the code fix under it. [INV-124, INV-15]

**Case: escalate a boundary call, and the close condition**

4. *when* the class boundary needs the human's read — which behaviours are one class, the intended design, whether a whole area wants a rethink — the system *shall* stop and ask rather than guess the boundary. [INV-124, INV-4]
5. The system *shall* treat the four moves as the bug's close condition, and *shall* read a point fix that leaves the siblings standing as a status short of a landing. [INV-124, INV-26]
6. The system *shall* have the prover carry a class lens on a found defect — whether the same kind lives elsewhere, whether the architecture accounts for it, and whether the spec describes it. [INV-124]

---

## Requirement 162: The problem ledger holds the workshop's own noise  [feature: F-problem-ledger]

**Context:** Some noise comes from the workshop itself: a test harness or tool flakes at random, a dependency goes missing, a shell command fails for a reason outside the product, a tool times out. A session retries and moves on, and then the same noise eats the same minutes session after session. A flaky test the project itself owns is a different thing, a defect fixed at its root and never workshop noise.

**User Story:** As a person losing minutes to recurring operational noise, I want each workshop problem recorded in one ledger with a status, so that noise seen twice gets a tracked owner instead of being rediscovered and retried each session.

### Acceptance Criteria

**Case: the ledger and its home**

1. The system *shall* keep the workshop's operational noise in the problem ledger, one git-tracked file `.live-spec/PROBLEMS.md`, born on its first entry, and, within `.live-spec/`, *shall* keep only the checkpoints git-ignored. [E-24, E-8]
2. *when* a test the project itself owns flakes, the system *shall* read it as a defect fixed at its root, never workshop noise and never a retry. [INV-155]

**Case: the signature and its status**

3. The system *shall* record each entry as a signature — a short greppable plain phrase — carrying its dated occurrences and one status. [E-24]
4. The system *shall* hold the four statuses: `watched` when seen once, `owned` when a named queue row will solve it, an `agreed non-problem` dated on the human's word, and `solved` when its row landed with the date kept. [E-24]

---

## Requirement 163: The ledger walk and its two-strikes ladder  [feature: F-problem-ledger]

**Context:** The moment noise fires mid-work, the session greps the ledger for the signature, and what the grep returns decides the next move. The walk climbs a fixed ladder from a first sighting to a method defect.

**User Story:** As a person meeting operational noise mid-work, I want the ledger walk to record a first sighting, buy an owner on the second, and escalate a third unowned recurrence to the pack, so that a problem seen twice is never silently retried and a method defect reaches the pack's own queue.

### Acceptance Criteria

**Case: a first sighting**

1. *when* noise fires and its signature is not listed, the system *shall* write one `watched` line — signature, date, one line of context — and keep working, replacing the silent retry and never taking the lane. [INV-23]
2. *if* the noise is a defect of the product, *then* the system *shall* send it to the bug lane instead. [T-9]

**Case: the second occurrence buys an owner**

3. *when* a listed signature fires a second time, the system *shall* pick the branch its own read of the signature supports: a problem that needs solving gets a queue row the system opens itself, closing the duty at once; a signature that reads as noise gets a written no-problem recommendation, and that no-problem verdict stays the human's alone. [INV-23, INV-9]
   [GAP: the measure separating a problem that needs solving from noise at the second occurrence is unstated in the source; the seat's own read picks the branch and the human's dated word settles a no-problem close.]
4. *when* the branch is the no-problem recommendation, the system *shall* write it right away and let the ask ride the batched report; the recommendation is a pending owner only, so the signature stands without an owner of record until the human's dated word lands, and the lane never stalls on it. [INV-4, E-22]

**Case: a third unowned recurrence is a method defect**

5. *when* a signature's third recurrence carries no open queue row and no human word closing it, the system *shall* file the recurrence as a defect of the method that reaches past a single day. [INV-23, INV-10]
   - that is the state a pending no-problem recommendation still riding the batched report leaves the signature in.
6. *when* the recurrence is filed as a method defect, the system *shall* leave the host as one inbox file to the pack's own queue, citing the signature and its dates. [INV-23, E-11]

---

## Requirement 164: A resolved entry collects dates and archives at the milestone  [feature: F-problem-ledger]

**Context:** Once an entry has its owner, it only collects dates. A recurrence appends a date and changes nothing else, and a landing that closes the owning row flips the entry closed in the same session rather than waiting for an audit.

**User Story:** As a person tracking an owned problem, I want a recurrence to only append its date and a landing to close the entry at once, so that the ledger stays current without a recurrence reopening a settled verdict or an audit lagging the truth.

### Acceptance Criteria

**Case: an owned entry only collects dates**

1. *when* an `owned` or `agreed non-problem` entry recurs, the system *shall* append its date and change nothing else. [E-24]
2. The system *shall* leave the re-raising of an agreed non-problem to the human, who re-raises it from the growing date list. [INV-9]

**Case: a landing closes the entry in its own session**

3. *when* a landing closes an `owned` entry's queue row, the system *shall* flip that entry to `solved` the same session, the entry never waiting for an audit to learn its row landed. [E-24]

**Case: archival at the milestone**

4. *when* the milestone compaction runs, the system *shall* move `solved` and agreed entries to a dated archived tail of the same file, keeping one file as the one home so the ledger never grows without bound. [M-1]

---

## Requirement 165: A known owned problem stays parked while unrelated work rolls  [feature: F-problem-ledger]

**Context:** A known, owned problem never blocks unrelated work; it stays parked while every unrelated lane keeps rolling. It is either a recurring defect with a named mechanical owner or a check held red for an understood, recorded reason, held in place by its ledger line, its owning row, or an expected-red note.

**User Story:** As a person with one known problem parked, I want every unrelated lane to keep rolling and the problem's instances serviced in batch, so that one thing not quite working never blocks the rest and never interrupts the work with a per-instance ceremony.

### Acceptance Criteria

**Case: the parked problem lets unrelated work move**

1. The system *shall* keep a known, owned problem parked while every unrelated lane keeps rolling, held in place by its ledger line, its owning row, or an expected-red note. [INV-56]

**Case: two rules keep it parked**

2. The system *shall* cap hand-fixing loops at the two-strikes law, the second occurrence buying an owner rather than another hand-pass. [INV-56]
3. *when* a defect has a named mechanical owner, the system *shall* service its instances in batch, with no per-instance ceremony interrupting the work or the human reading it. [INV-56]
   - the fence fixes them silently wherever it catches them, then appends one ledger line at the session's end.

**Case: a real bug still preempts**

4. *when* a real new bug arrives, the system *shall* let it preempt, this parking law governing only the known, owned problem. [T-9, INV-56]

---

## Requirement 166: The ledger's seams and the scope of this landing  [feature: F-problem-ledger]

**Context:** The ledger's seams state who writes it, how two sessions share it, when two entries are one problem, and where the workshop's law ends and the product's begins. The landing opens the pack's own ledger and leaves the mechanical guard for later.

**User Story:** As a person maintaining the ledger across sessions and workers, I want its write-ownership, concurrency, and merge rules stated and this landing's scope named, so that a worker's noise reaches the ledger safely, two sessions never clobber it, and one problem under two wordings becomes one entry.

### Acceptance Criteria

**Case: who writes the ledger**

1. The system *shall* have sessions write the ledger, a worker reporting noise in its checkpoint for the session to carry over, and a worker whose brief names the ledger among its files writing it directly, the brief stating the write-ownership law. [ACT-3]
2. The system *shall* have two sessions on one host share the file under the concurrent-edit fence, like any document. [INV-11]

**Case: one problem, one entry**

3. *when* two entries are judged one problem by grep and eyes, the system *shall* merge them into a single entry at the milestone compaction, signatures staying short so the grep stays honest. [M-1]

**Case: the workshop's law ends at the product**

4. The system *shall* keep this the workshop's law while the product keeps its own, and *when* a product bug recurs *shall* re-door it to a feature under the pipeline's rule, distinct by what broke. [T-9]
5. The system *shall* carry no visible surface for the ledger, so the standard feature checks — phone behavior, touch, empty, error, and loading states, accessibility, and performance — do not apply. [E-24]

**Case: what this landing does not add**

6. The system *shall* add no mechanical guard yet, the named candidate — a pre-push check that no entry crosses a milestone unowned — earning its row after real usage. [E-24]
7. The system *shall* add no automated signature matching, and *shall* open the pack's own ledger this landing while a foreign host opens its ledger from its own window. [E-24, INV-10]

**Case: the success measure**

8. The system *shall* land the next operational hiccup in a session as a recorded ledger line, checked at the milestone audit. [INV-23, M-1]

---

## Requirement 167: Search for an existing skill before reinventing a fix  [feature: F-problem-ledger]

**Context:** Before reinventing a fix, the pack searches for an existing skill. Two moments trigger the search: a project's setup, and a struggle that keeps returning. A found skill is adopted or rejected by name, and borrowing keeps to one practice.

**User Story:** As a person about to reinvent a fix, I want the pack to search for an existing skill at setup and at every struggle, so that a returning failure class is met by something that already owns it, sparing a fresh build from scratch.

### Acceptance Criteria

**Case: the two moments that trigger a search**

1. *when* a project is set up — at founding, or adoption's orient, beside the founding questions — the system *shall* scan the installed skills and the catalogs it can reach, propose a fit list matched to the project's kind and crafts with a recommendation, and leave the pick to the human's word. [INV-65, B-2, B-3]
2. *when* a struggle keeps returning — a ledger entry reaching its second occurrence, a taste artifact rejected twice (voice, copy, visual style, or spec prose the human has sent back twice), or any failure family that recurs — the system *shall* wait for one search before the next attempt, and *shall* adopt or reject a found skill by name, recording the verdict where the struggle lives. [INV-65, INV-23, INV-62]

**Case: how a borrowed skill travels**

3. The system *shall* invoke a found skill as it ships, paraphrase a borrowed lesson into the project's own documents with the source credited by name, and carry verbatim text only under its license with the notice kept. [INV-65]
4. The system *shall* never republish unlicensed text. [INV-65]

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

## Requirement 169: Bootstrapping a fresh host  [feature: F-bootstrap]

**Context:** A fresh host starts from the templates the pack ships. The system copies the document set and the suite scaffold, then the first request enters the queue and runs through the ordinary pipeline. The scaffold's green is the starting floor the first delivery builds on.

**User Story:** As a person starting a fresh host, I want the templates and a runnable scaffold in place, so that the first request runs through the ordinary pipeline against a known starting floor. [B-1]

### Acceptance Criteria

**Case: the templates land**

1. *when* the version-control gate has closed, the system *shall* copy the document templates — spec, architecture, test matrix, roadmap, journal, and the resume file — and copy the suite scaffold (`test_scaffold.py`) into `tests/`. [B-1]
2. *when* the templates are in place, the system *shall* offer hooks in plain words, and *shall* impose none. [E-6]
3. *when* the templates are in place, the system *shall* let the first request enter the queue and run from intake through the ordinary pipeline. [B-1]

**Case: the scaffold defines the first green**

4. The scaffold suite *shall* judge the first delivery green by what the shipped scaffold runs. [B-1, INV-274]
   - the six documents stand, and none is an empty shell;
   - the spec's opening carries a version and a date;
   - the matrix carries its generated reference and its coverage teaching;
   - the queue is a table;
   - the resume file holds at most one live-state block.
5. *when* a header holds a leftover template placeholder, the scaffold suite *shall* count that header as red. [B-1]
6. The scaffold green *shall* stand as the starting floor; the first delivery *shall* ship its own first real test beside the scaffold. [B-1]
   [GAP: the spec does not state what content a live-state block must carry for the scaffold suite to count it present.]

**Case: a second founding is safe**

7. *when* a founding runs on a tree a prior founding began, the system *shall* read each phase's precondition from the tree. [INV-89, B-1]
   - a destination that already stands is reported to the person as done, and skipped.
8. The system *shall* overwrite no file it did not create in the running founding. [INV-7, B-1]
   - a destination standing with its template placeholders intact is named to the person, and replaced only where the person says so.

**Case: the host profile carries the host's own lines**

9. *when* a founding writes `.live-spec/profile.md`, the system *shall* write one line for every question in the founding-question set whose key names no path. [B-3, INV-227]
   - the economy rung and the answered set's version stand beside those lines.
10. The system *shall* write no setting about the person into the host profile, and *shall* use no personal-profile template as that file's source. [E-13, B-3]

**Case: the surface registry takes the config's name**

11. *when* a founding creates the surface registry, the system *shall* create it after `guardrails.config.json` exists, and *shall* take its filename from that config's registry path. [INV-97, E-10]

---

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

## Requirement 177: Adoption runs as an ordered set of phases  [feature: F-adoption]

**Context:** Adoption attaches the pack to a project already under way. It runs as a sequence where each phase finishes before the next starts, and it assumes no blank slate. The version-control gate runs first so the whole run stays reversible.

**User Story:** As a person attaching the pack to a running project, I want adoption to read everything first and re-engineer it into the pack's shapes without trusting or losing anything, so that the existing work is preserved and checked before it is trusted.

### Acceptance Criteria

**Case: orient and inventory**

1. *when* adoption begins, the system *shall* read every existing document — README, roadmap, spec, test suite, journals, TODO files, and repo wikis — before touching anything, and *shall* answer the founding questions about what was found. [A-1]
2. *when* orient completes, the system *shall* list the code, the user-facing surfaces, and the document set, each entry named with its owner, and surfaces named to file and line. [A-2]
3. Listing the surfaces *shall* seed the host's surface registry. [E-10]
4. The system *shall* keep adoption's working artifacts — the orient digest, the inventory, the reconcile notes — in the host's `.live-spec/adopt/`, tracked in git, and *shall* keep them out of the host's own folders. [A-8]

**Case: re-engineer the documents**

5. *when* the system re-engineers an existing spec, the system *shall* keep its claims as spec sections and mark them unverified. [A-3]
6. The system *shall* seed the architecture document's nodes from the inventory's file-and-line entries, turn existing tests into matrix rows cited at their real level, and turn an existing roadmap or TODO into queue rows. [E-14, E-15]
7. The system *shall* reconcile every unverified claim — pin it to file and line, or remove it — at the first delivery that touches its surface, or by the first milestone, whichever comes first. [A-3]

**Case: version-control gate, baseline, and incremental**

8. The system *shall* run the version-control gate before touching or moving anything. [A-5]
9. The system *shall* save a first baseline snapshot of the host's artifacts as found, git-tracked, as the diff baseline the snapshot machinery guards. [A-6, E-7]
10. *when* the earlier phases are done, the system *shall* run the host on the same request lifecycle as a bootstrapped host, and *shall* record the installed skill versions in `.live-spec/` at attach time. [A-7]
11. *when* the pack's version or an installed skill's version changes, the freshness check *shall* re-read the changed skill before continuing and write a one-line journal note naming old and new. [A-7, M-7]
12. *when* a safe breakpoint is reached, the freshness check *shall* re-stat the installed skills and the pack on disk and re-read whatever changed, and *shall* ask the public repo once a day whether the pack has moved. [A-7, M-2, E-25]

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

## Requirement 180: The catch-up sequence brings an adopted host onto the current pack  [feature: F-catchup]

**Context:** An already-adopted host falls behind the pack as the pack moves. The catch-up sequence brings the host's documents and records onto the current pack. The owner asks in any wording; the version delta decides that catch-up fires, whatever words the ask used. The sequence runs four phases in fixed order.

**User Story:** As the owner of an already-adopted host that has fallen behind, I want catch-up to bring it onto the current pack in fixed phases behind my gate, so that the host is brought current with nothing lost. [A-11]

### Acceptance Criteria

**Case: a release that owes host actions ships a chapter**

1. *when* a pack release changes something a host must act on, that release *shall* land one dated, versioned migration chapter stating the host-side steps; a release owing nothing *shall* add no chapter and *shall* say so in its changelog. [INV-91]
2. The system *shall* build the work list as the ordered chain of migration chapters from the host's recorded pack version to the current one, oldest first. [INV-91]
3. *if* the host's record carries no readable pack version, *then* the system *shall* start the chain at the earliest chapter. [INV-91, INV-89]

**Case: the four phases in order**

4. The system *shall* run catch-up in four phases in fixed order: orient on the delta, plan behind the owner's gate, execute while preserving facts, then verify and re-record. [A-11]
5. *when* orient runs, the system *shall* read the host's installed-set record and tree, read the pack's current version and journal, and build the work list as the difference; *when* preconditions in the guide disagree with the tree, the system *shall* take the tree as the truth. [A-11]
6. *when* the delta includes founding questions the host has never answered, orient *shall* read the host's recorded `founding.set-version` against the current set and name each question added since. [INV-227]
7. *when* the plan is written, the system *shall* write it into the host's `.live-spec/adopt/`, list every file that moves, merges, or retires and every open conflict, and *shall* move no file before the owner's word on the plan. A plan that finds nothing to do *shall* report that and end. [A-11, A-8]
8. *when* execute runs, the system *shall* open with a clean-tree baseline commit, run under the checkpoint discipline, and resume an interrupted run from the checkpoint under the already-given gate. [A-11, A-5]
9. *when* verify runs, the system *shall* run the host's own gates including the suite, keep the sequence open until the gates read green, re-record the installed-set record in the current format, and land one journal chapter. [A-11, M-7]

**Case: machine-level steps run once**

10. *when* a step touches the machine's shared homes — the installed-skills folder or the personal profile — the system *shall* run it once per machine and *shall* report it done and skip it when its already-done check passes. [A-11]

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

**Context:** When a restructure or a migration is gated for merging back into main, the gate judges the delta rather than re-proving the untouched whole. It has three parts and routes pre-existing findings to the queue instead of blocking on them.

**User Story:** As a person merging a restructure or migration, I want the gate to judge only the delta, so that a large reorganization is verified without re-proving what it did not touch. [INV-114]

### Acceptance Criteria

**Case: the three parts**

1. *when* a restructure or migration is gated for merge, the system *shall* judge the delta in three parts: load-bearing token identity old-versus-new except the per-chunk named deltas plus the punctuation-multiset check; the full suite green on the merged tree; and a prover pass on both sides whose blocking set is scoped to the delta. [INV-114, INV-111, INV-39]
2. The system *shall* block on an unmatched token, a red suite, a new-side finding absent on the old side, or an unnamed meaning change. [INV-114]
3. *when* a finding is present and equal on both sides, the system *shall* route it to a queue row in the same delivery and *shall* not block on it. [INV-114]

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

## Requirement 186: The settings card shows at setup and answers the standing question  [feature: F-onboarding]

**Context:** At the end of founding, and again at the end of adoption's orient, the system renders the settings card. The human reaches it twice — here at setup without asking, and any later time by asking. The card shows what the pack has set up and what is the human's to change, and asks nothing.

**User Story:** As a person new to the pack, I want the settings card shown at setup and re-rendered whenever I ask what I can customize, so that I see every setting and change any of them by speaking its change-line. [INV-87]

### Acceptance Criteria

**Case: the card shows at setup's end**

1. *when* founding ends, or adoption's orient ends and the project kind and the economy setting have settled, the system *shall* render the settings card. [INV-87, INV-36]
2. The card *shall* list every setting the pack knows, each row giving the setting's plain-words name, its current value for this host where one is recorded, and one line saying how to change it in plain speech. A recorded default *shall* be shown as told, and the card *shall* ask nothing. [INV-87, INV-31]
3. The system *shall* read each value from the settings ladder — the reader's own profiles and this host's recorded lines. [E-13, INV-87]
4. *when* the card opens, the system *shall* open it by the show rule, and *shall* pass the pre-show register lint on the fixed copy and the rendered values before it opens. [INV-67, INV-83]

**Case: the same card answers the standing question**

5. *when* the person later asks what they can customize, in any wording, the system *shall* answer with the same card re-rendered from the current truth, and *shall* let no hand-kept copy answer. [INV-87]

**Case: one catalog home**

6. The card and the standing answer *shall* derive from one source: the pack-defaults table joined with the reader's profile files and the host's recorded lines. No second hand-kept settings list *shall* exist. [INV-87]
7. Every card-visible table row *shall* appear on the card, every recorded profile line *shall* appear in the card's project-rules part, and every card row *shall* trace to a marked table row or a recorded profile line; a missing card-visible row and a card row with no source *shall* each be a defect. [INV-87]

**Case: the copy states rules, values stay the reader's own**

8. The card's fixed copy *shall* state each setting as a rule anyone can read, and *shall* show a personal value — a language, a name — only as the reader's current value, labelled as theirs to change. [INV-88]
9. The fixed copy *shall* never present one person's value as the product's prescription. [INV-88]

**Case: the render and its states**

10. A build-time script (`scripts/onboarding-card.py`) *shall* render the card from the pack-defaults table and the profile files, and *shall* fail the render loudly on a malformed table row. [INV-87]
11. *if* the personal profile is missing, *then* the script *shall* render the card on pack defaults, say plainly that no profile exists yet, and name how the founding offer creates one. [INV-87]
12. *when* the pack-defaults table grows a row, the system *shall* draft that row's card rule-copy on the clean-writer road before it first renders. [INV-84]

**Case: the card's facets**

13. *when* the viewport is a phone, or a window too narrow to hold multiple columns, the card *shall* read as one column top to bottom; on a window wide enough to hold them it *shall* keep its multi-column arrangement. [default] [INV-87]
14. The card *shall* be a static rendered page, plain structured HTML with headings and keyboard scrolling, and *shall* depend on no hover. [default] [INV-87]
15. The card's empty state *shall* be a missing personal profile, its error state a malformed catalog row, and its blocked state flagged text at the register lint. [INV-87, INV-83]
   - empty shows pack defaults, says the absence plainly, and names the founding offer;
   - error's render fails loudly;
   - blocked stops the showing until the text is fixed, and names what it flagged.
16. Rendering the card *shall* be read-only, so two sessions can render it at the same time; an open card *shall* show the truth of its render moment, and a later change *shall* not update the open page. [default] [INV-87]

---

## Requirement 187: Running an engine and its instance as a pair  [feature: F-pair]

**Context:** When founding takes the engine-and-instance split, the two repos run as a pair. Each repo is a full host with its own spec, queue, journal, and settings folder. No third document spans the pair. A lesson crosses between the two only through the inbox.

**User Story:** As the owner of an engine-and-instance pair, I want each repo to run as its own full host with the inbox as the only cross-seam channel, so that one window serves one repo and neither half writes the other's tree. [INV-86]

### Acceptance Criteria

**Case: each repo is a full host**

1. Each repo of the pair *shall* carry its own spec, queue, journal, and `.live-spec/` folder, and no third document *shall* span the pair. [INV-86, E-1, E-14]
   [GAP: whether one reading view is stitched across the pair's two queues, or strictly two are kept, is an open decision; today's practice is two plain queues, recorded open in DECISIONS.md. D-6]
2. The engine's spec *shall* state what the mechanism does for any instance and *shall* cite no instance's content; the instance's spec *shall* state what the product is for its real user and *shall* cite the engine only by its content-contract handles. [INV-79, INV-86, D-7]
   [GAP: whether the instance's spec may cite engine facts, or only the content-contract handles, is an open decision; today's practice is handles-only, recorded open in DECISIONS.md. D-7]

**Case: wishes and lessons cross the seam**

3. *when* a request is shaped for both engine and instance, the system *shall* split it at intake into one queue row in each repo, each citing the one spoken request. [T-17, INV-1, INV-37]
4. The system *shall* keep each repo's own inbox as the place outside items arrive; the instance's inbox is where the human hands in requests. [E-11, INV-37]
5. *when* a lesson travels between the two, the system *shall* carry it only through the inbox under write-ownership: the learning window files one new inbox file in the other repo and journals the hand-off in its own tree, writing no foreign tree beyond that one file. [E-11, INV-10, T-10]
6. One window *shall* serve one repo of the pair, *shall* stay read-only on the other half save for that one inbox file, and *shall* keep the concurrent-edit fence binding inside each repo. [INV-10, INV-11, INV-86]

**Case: the load-bearing crossing**

7. *when* the human throws a request at the instance window and intake finds a generic part and the instance's own part, the system *shall* route each part to its own home. [INV-37, T-17, E-11, INV-10, INV-56]
   - the generic part is filed as one engine inbox request;
   - the instance's own part is parked as a dated blocked-on-engine debt line;
   - this keeps the lane moving.
8. The dated debt line *shall* appear in the instance's every status report until the engine ships the request. [INV-27]
9. *when* the engine's session sweeps its inbox, the system *shall* land the request through the full pipeline on the engine's generic fixtures, make each new plug-in point a named content-contract entry with a works-without-it test, and ship and version on the engine's own rhythm. [T-10, INV-79, E-3]
10. *when* the engine ships, the system *shall* update the instance to that engine version, plug the real content into the new entry, verify on the real product, un-park the parked row, and close it whole. [INV-56, T-17]

**Case: the engine's spec carries its own provenance**

11. The engine's spec *shall* cite only the engine's own public commits for provenance and *shall* give each mechanism a neutral name in the engine's own vocabulary. [INV-119]
12. *where* a running instance shows a locale-specific label for a mechanism, the engine's spec *shall* note that string as instance-supplied copy and *shall* keep the neutral term as the mechanism's one name. [INV-79, E-4]
13. The publish gate *shall* check a generalized pack for two leaks: a private-instance provenance hash, and an instance's locale label standing as a mechanism name. [E-20, INV-119]

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

## Requirement 189: An agent and a skill are told apart by what outlives a conversation

**Context:** Several agents work on one person's projects, and the moment they can talk to each other they can generate noise. The layer that governs them opens by telling an agent from a skill, since only an agent holds standing work of its own that another agent can address. An agent is a project window with a tree, a queue, gates, contracts, a standing mission, and a card; a skill is a capability a window loads for one conversation.

**User Story:** As a person running several agents on one machine, I want an agent and a skill told apart by what outlives a conversation, so that only the trees holding standing work are addressed as agents.

### Acceptance Criteria

**Case: what an agent carries**

1. *when* a tree carries its own spec, queue, gates, published contracts, standing mission, and agent card, the system *shall* treat that tree as an agent, each of those outliving any one conversation. [E-31]
2. one window *shall* serve one agent, the same rule the engine-and-instance pair already holds for its two repos. [E-31, INV-86]

**Case: what a skill carries**

3. *when* a capability loads into a window, holds no tree, no standing mission, and no queue, and leaves nothing standing once the conversation closes, the system *shall* treat that capability as a skill. [E-31]

**Case: the line between the two**

4. the system *shall* count a capability as an agent *when* it holds durable state, a standing mission, and a zone of its own, and *shall* count a capability that lives wholly inside one session as a skill. [INV-182]
5. *when* a real capability sits on the line between the two, the owner's word *shall* place it. [INV-182, T-22]

---

## Requirement 190: Two channels carry everything between agents, and the traffic's kind picks the transport

**Context:** A message between two agents travels two roads and no more. One is the receiver's inbox, which carries a one-shot request to change something; the other is a published contract, a versioned read the reader takes on its own clock. Which road a given message takes is decided by whether it needs a timely answer, while who may talk and when stays the same on either road.

**User Story:** As a person whose agents pass work between them, I want exactly two channels to carry everything between two agents, so that no third improvised road grows to carry the traffic the two were meant to hold.

### Acceptance Criteria

**Case: the two channels**

1. the receiver's inbox *shall* carry a one-shot request to change something, one new file per item. [INV-183, E-11]
2. a published contract *shall* carry a recurring read, versioned, taken on the reader's own clock. [INV-183, E-33]
3. a reply *shall* ride the inbox in the other direction, so the count of channels between two agents stays at two. [INV-183, INV-192]

**Case: the traffic's kind picks the transport**

4. *when* a message needs no answer within a deadline, the system *shall* send it by the store. [INV-236, E-11, T-10, INV-112]
   - such a message is a durable record read on the neighbour's own clock, or a notification;
   - the file is reachable while the receiver is not running;
   - *when* the sender is remote, the file is committed and pushed.
5. *when* a message is a back-and-forth needing a live peer that answers in turn, the router (`guardrails/route_agent_transport.py`) *shall* route it to the direct channel. [INV-236]
6. *while* the harness has shipped no listener, the direct channel *shall* stand unavailable, and the router *shall* name the listener it waits on. [INV-236, INV-231]

**Case: the store road's watcher**

7. *when* a receiver arms a one-shot check that reads a deposit on the receiver's own rhythm, whenever it next runs, the system *shall* treat that check as the store road's watcher. [INV-236, INV-231, INV-129]

**Case: the contract holds across transports**

8. whichever transport carries a message, the system *shall* leave the two-channel contract untouched, so who talks and when stays as it stands. [INV-236, INV-183]

---

## Requirement 191: Every reference to an internal item carries its code and a plain description

**Context:** The method names its internal items with short codes, and a code alone tells a person nothing. So every reference to a named item carries a pair — the item's stable code beside a plain one-sentence description of what it does and the problem it solves. The pair travels in a cross-agent message and in a report a human reads alike, and each description lives where its code is written — the criterion the code trails, and the glossary for an entity code's definition.

**User Story:** As a reader of a report or a cross-agent message, I want every internal code carried beside a plain one-sentence description, so that a bare code never stands alone before me and a second agent reasons in the same terms.

### Acceptance Criteria

**Case: the pair travels together**

1. *when* a reference names an internal item the method carries a code for, the system *shall* carry the item's stable code beside a plain one-sentence description pinned to the item at its owning surface. [E-35, INV-239, E-4]
2. the system *shall* carry that pair in a message across the agent channel and in a human-facing report alike. [INV-239, INV-183]
3. within one report, the system *shall* carry the full pair on a code's first mention and the code alone on each later mention of that code. [INV-239, INV-28, INV-31]

**Case: one home for the description**

4. the system *shall* keep each code's plain statement in its authored home — the criterion the code trails carries the code's rule, and an entity code's definition lives in the glossary — written once and read by every reference, the generated code-to-location table carrying locations only. [INV-239, INV-271]
5. the system *shall* back-describe the whole existing code set in one pass at a major release carrying one MIGRATION.md chapter. [INV-239, INV-217]
6. *when* the project runs in another language, the system *shall* translate the English description in real time and translate it consistently, so one item reads under one translation across a session. [INV-239, INV-83]

**Case: the description's presence is checked, its quality sampled**

7. *when* the migration to the requirements format lands, the dedicated description-field gate *shall* retire with the criteria and the glossary as its stated successor, the requirement-shape gate thereafter holding that every code trails a criterion carrying its rule. [INV-239, INV-271]
8. for a code deposited on the agent channel with no description beside it, the reviewer's review *shall* stand as the net. [INV-239, INV-189, INV-150]
   - the reviewer role's review is the enforcement until the named gate ships;
   - the law declares the mechanism as the deposit-time lint over each `from-<agent>` inbox file.
9. a human *shall* sample descriptions against the quality bar at the migration's authoring and each periodic audit, and *shall* accept each that reads as clear. A description below the bar *shall* become a queue row. [INV-239, INV-41, INV-145]
   - the periodic audit's own count defaults to every ten deliveries, the host setting its own count in its profile.

**Case: the quality bar a description is written to**

10. a description *shall* say what the item does and the problem it solves, *shall* show the whole class *when* the rule governs a class, *shall* name its key term in plain words, and *shall* use the accurate actor and object. [INV-239, INV-153, INV-83]

---

## Requirement 192: A description a reader could not follow is rewritten by the agent that owns the item

**Context:** A description can be clear to its author and still leave a reader asking what one of its terms means. That re-asked question is the signal the description did not land. The agent that owns the item rewrites the description, and it does so on its next turn writing that item's home document rather than in the middle of another turn.

**User Story:** As a reader who re-asks what a term means, I want the description rewritten by the agent that owns the item, so that each description earns its clarity from real use each time it is re-asked.

### Acceptance Criteria

**Case: the re-asked question is the signal**

1. *when* a human re-asks what a term a reference carries means, the system *shall* read that question as a signal the description did not land. [INV-240, INV-83]

**Case: the owning agent writes the rewrite**

2. the system *shall* let only the window that owns the item write that item's description, its one home being the item's owning surface. [INV-240, INV-10]
3. *when* the confusion lands in the owning window, the owning agent *shall* reformulate the description to answer the question just asked and overwrite it in its one home on its next turn writing that document. [INV-240]
4. *when* the confusion lands at a window that does not own the item, that window *shall* carry the confusion to the owning agent as a lived-fault earned message, and the owning agent *shall* rewrite the description on its next turn writing that document. [INV-240, INV-189]

**Case: the rewrite waits for a written turn**

5. whichever window the confusion arrived at, the system *shall* record the re-question and defer the rewrite to the owning agent's next turn writing the document, holding clear of a rewrite in the middle of another turn. [INV-240, INV-39]
6. the deferred rewrite *shall* take the description's home document under its own pen and *shall* ride as a named intended change to the identity check the restructure procedure runs — word-token and punctuation multisets unchanged except the named changes — which expects it as a matched token. [INV-240, INV-198, INV-111]

**Case: the rewrite meets the same bar**

7. the rewrite *shall* obey the quality bar every description obeys, sampled against a real reference by the human sampling net, with the presence gate beneath it. [INV-240, INV-41]

---

## Requirement 193: An agent is found by the card it writes and a live scan  [feature: F-roster]

**Context:** An agent reaches this point the moment it meets something that might belong to another agent — a capability it lacks, data another project holds, a question about a neighbour's zone. It answers by scanning for cards, since a card is what makes a tree an agent. It comes away holding the owning agent's name, mission, zones, contracts, and inbox address, or it learns no agent owns the thing, which opens the birth scenario.

**User Story:** As an agent meeting something outside its own zone, I want to find the owning agent from a card it wrote and a live scan, so that who owns what is always a lookup.

### Acceptance Criteria

**Case: the card is the declaration**

1. the agent card *shall* live in the agent's own tree at `.live-spec/agent.md` and *shall* name the agent's name, its standing mission, the zones it owns, each contract it publishes with the path its artifact lives at, and its inbox address. [E-32]
2. the system *shall* treat a tree that carries a card as an agent, and writing the card *shall* be the one act that seats it. [E-32, INV-184]
3. *when* an agent finds no card on a thing that might not be its own, the system *shall* ask one plain question rather than guess. [INV-184, INV-4]

**Case: discovery is a live scan**

4. the system *shall* discover agents by reading two globs under each root — `<root>/*/.live-spec/agent.md` and `<root>/*/*/.live-spec/agent.md` — and *shall* treat every card it finds as an agent. [INV-184, E-32]
5. the scan's roots *shall* be the parent directory of the reader's own tree together with any root the personal profile names. [INV-184, E-16]
6. the scan *shall* descend no branch, so its whole cost is two directory listings per root and one stat per candidate. [INV-184]
7. the system *shall* run the scan live on every lookup and *shall* keep no cached index of who exists, since a scan reads the machine as it stands *while* a cached list answers from a past moment and is the shared file two windows race to edit. [INV-184, INV-10, INV-11]

**Case: no shared file describes an agent**

8. the system *shall* let no file outside any tree describe any agent, each agent owning its own description the way it owns its own tree. [INV-184, INV-10]
9. the system *shall* read the owning card before acting on anything that might not be its own, the reviewer's review standing as the net for that discipline. [INV-184, INV-150]

**Case: the card needs no permission, and its bounds**

10. the system *shall* grant the card by write-ownership, so writing it needs no permission act. [INV-184, INV-10]
11. the card *shall* hold the agent's own identity and addresses, and product data placed in a card *shall* be a contract field taking the contract's permission road. [INV-184, INV-185]

**Case: a tree with no card is flagged**

12. *when* an inventoried live-spec host tree carries no `.live-spec/agent.md`, the system *shall* flag it as an incomplete record and *shall* have the host write its card at its catch-up walk. [INV-184, A-10, A-11, INV-159, INV-36, INV-135]
   - an incomplete record ranks the same as a project kind recorded with no declared layers;
   - the duty binds forward.
13. the gate `guardrails/check-agent-card.py` *shall* read a host tree's root and fail by name *when* the root carries no `.live-spec/agent.md`, and the pack carries its own card so the gate reads the pack's tree and passes. [INV-219, INV-97]

---

## Requirement 194: A published contract is read on the reader's own clock  [feature: F-contract]

**Context:** A consumer agent arrives here from the scan holding a producer's card and the path its artifact lives at. A published contract is a surface in the producer's own spec, paired with a machine-readable artifact carrying its own version and generation stamp. The consumer reads it read-only on its own clock, and data past its staleness bound stops the analysis.

**User Story:** As a consumer agent needing another agent's numbers, I want to read its published contract on my own clock rather than ask it, so that I depend on a stated, versioned interface instead of an unstamped snapshot.

### Acceptance Criteria

**Case: the contract and its artifact**

1. a published contract *shall* be a surface in the producer's own spec, written, proven, and tested where the producer's other surfaces are and earning its feature coverage there. [E-33, INV-73]
2. each contract field *shall* name what the field means, the window it is measured over, how it is aggregated, and the source it derives from, and the reviewer *shall* read a field missing any of the four as an incomplete surface. [E-33, INV-101]
3. the published artifact *shall* live at the path the producer's card names and *shall* state the contract version it was generated under and the moment it was generated, so a reader tells its shape and its age from the artifact itself. [E-33, E-32, E-14, INV-24]

**Case: nothing publishes by default**

4. a contract *shall* publish no field until the owner records an explicit permission for it in the producer's tree with its date and author. [INV-185, INV-24]
5. a field with no recorded permission *shall* stay in the producer's tree, the way a neighbour's product is built granting no permission, and the reviewer's review *shall* read a declared contract's fields against their permission records. [INV-185, INV-150]
6. credentials *shall* cross no channel under any permission, the published artifact being the one road a producer's product data takes between two agents. [INV-185, INV-183]

**Case: the producer's cadence**

7. the producer *shall* declare one cadence — how often it regenerates the artifact — and *shall* hold to it whatever its consumers do, a deploy refreshing the artifact as a bonus and never triggering it. [INV-186]
8. the producer's own session-start check *shall* fail *when* its scheduled regeneration did not run, beside the pack-update check that runs there, and the consumer's staleness bound *shall* stand as the second, independent watcher that catches a producer gone quiet. [INV-186, INV-187, E-25]

**Case: the consumer's read**

9. the consumer *shall* declare one staleness bound — how old the artifact may be for its analysis — and its freshness check *shall* fail past that bound before any analysis runs. [INV-187, INV-41]
10. the consumer *shall* pin the contract version it was written against and *shall* carry a compatibility test that fails *when* its pinned version and the artifact's version diverge. [INV-187]
11. the consumer *shall* read the artifact read-only — over the filesystem when co-located, over git when remote under its recorded read grant — and *when* the generation stamp reads past its staleness bound it *shall* name the stale data aloud and stop. [INV-187, INV-112, INV-232, INV-67]

**Case: two numbers, set apart**

12. the cadence and the staleness bound *shall* be two numbers set independently, and neither side *shall* read the other's. [INV-186, INV-187]

**Case: data reads, it never asks**

13. a consumer wanting a producer's data *shall* read the contract rather than send a message asking for it. [INV-188]
14. *when* a consumer wants a field the contract lacks, the system *shall* treat it as a request about the contract's shape, which the earned message governs. [INV-188, INV-189]

**Case: the default-deny gate is promised**

15. the gate that reds a default-deny violation on the producer's suite *shall* stay promised until a host's first real contract. [INV-185]
    [target]

---

## Requirement 195: An agent earns a message before it deposits one  [feature: F-agent-ask]

**Context:** A sender agent reaches this point holding the receiver's card and inbox address and a piece of its own work the receiver's zone blocks. A message is one new file in the receiver's inbox, and every message names the work of the sender's own that earned it. The agent recognizes the neighbour's zone on its own and deposits the message in the course of its work, telling its user each time.

**User Story:** As an agent blocked by a neighbour's zone, I want to deposit a message only when my own work earns it, so that curiosity and tidiness generate no traffic on the channel.

### Acceptance Criteria

**Case: the transport**

1. a message *shall* be one new file in the receiver's inbox, named and shaped as every inbox item, naming its source with the `from-<agent>` form the inbox uses. [INV-189, E-11, INV-193, INV-146]
   - two source words are reserved and own no ground;
   - `from-owner` names the owner's own message;
   - `stranger-` names a stranger's bridged item, the inbox file the monitor commits from a stranger's issue.
2. the system *shall* deposit that one file by the standing arms — a co-located sender writes it and stops, a remote sender commits and pushes it under its per-repo grant, and the receiver's sweep carries it into the receiver's queue. [E-11, INV-10, INV-174, INV-112, T-10]

**Case: a message names the work that earned it**

3. a message *shall* name the sender's own work that earned it, and a message that can name no such work *shall* stay unsent. [INV-189]
4. a blocked message *shall* name the blocked work — a real row, a real failing step, a real thing the sender cannot finish *while* the receiver's zone stands as it does. [INV-189]
5. a lived-fault message *shall* name the fault and the evidence the sender lived — what it ran, what happened, and how the fault showed itself. [INV-189]

**Case: three grounds, and the set is closed**

6. the system *shall* recognize exactly three grounds for a message. [INV-189, INV-197]
   - the sender is blocked by the receiver's zone as it stands;
   - the sender has lived a fault in that zone and carries the evidence;
   - the sender holds a concern no agent's zone owns, carried to the pack as its default owner.
7. a candidate message matching no ground *shall* stay unsent, and the third ground *shall* carry only to the pack and only *while* no zone owns the thing. [INV-189, INV-197]

**Case: the owner's zone is presumed informed**

8. the system *shall* report to a zone's owner nothing that owner's own instruments already see, so a fault the owner's instruments cannot see, carried with the evidence the sender lived, is the case that earns the file. [INV-189]

**Case: the agent recognizes the zone and deposits on its own**

9. *when* an agent's own work meets a fault or a lack in something another agent's zone owns, the system *shall* scan for cards, find the owning agent, and take the channel that fits, on its own recognition. [INV-195, E-32, INV-183]
10. *when* the agent's work earns a message under a ground, the agent *shall* write the file to the neighbour's inbox in the course of its own work. [T-24, INV-189, INV-153, INV-163]
   - the trigger is any earned ground the work meets, so every occasion that earns a ground qualifies;
   - the pack states the form of a message, and the host's work states its content.
11. the deposited message *shall* name its references by the pair, so the neighbour reads a self-explaining file. [T-24, E-35]

**Case: the user is told**

12. *when* the agent deposits a message, the system *shall* tell its own user in the status report, naming the message's subject by its pair and the neighbour it reached, in a plain notice. [T-24, INV-27, INV-28, INV-31]
13. *when* the earned-message law declines a message the agent had drafted, the system *shall* tell the user in the status report with the reason it was withheld, and *shall* raise no tell for an impulse the discipline turned away before it became a draft. [T-24, INV-190, INV-191]

**Case: a capability is reached across its zone**

14. an agent needing a capability another agent's zone owns *shall* send a message or read a contract rather than keep a local copy of it. [INV-194, INV-183]

**Case: a deposit is written whole**

15. the system *shall* write a deposit into another window's inbox under a `.draft` name and make it final by an atomic rename once the content is complete. [INV-249]
16. the receiving sweep *shall* act only on a finished deposit and *shall* pass over any name still carrying the `.draft` suffix, leaving a routed deposit earned in place rather than removing it under a live writer. [INV-249, INV-247]

---

## Requirement 196: A misdirected question is referred back, and no refer-and-resend loop runs on

**Context:** A question can land on an agent that does not own it. The answer is a referral: the question lives in another agent's zone, so it goes back to whoever asked. Every message carries an identifier and a stated need-by and reaches a terminal state, and one question crosses between the same two agents at most twice before the third crossing goes to the owner.

**User Story:** As an agent handed a question from another agent's zone, I want to refer it back to whoever asked and let no refer-and-resend loop run on, so that a misdirected question reaches its owner without manufacturing traffic.

### Acceptance Criteria

**Case: a referral returns to whoever asked**

1. *when* a question belongs to another agent's zone, the system *shall* refer it back to whoever asked, and the zone's owner *shall* receive nothing from a referral. [INV-190]
2. *when* a human asks, the system *shall* answer in chat that the answer is the other agent's and to ask that agent, sending nothing. [INV-190]
3. *when* an agent asks, the system *shall* answer along the reply road as the message's terminal state, declined and naming the zone that owns the question. [INV-190, INV-192]

**Case: a question dropped for want of a home**

4. *when* a question pins to no artifact and no work of the sender's stands on it, the system *shall* drop it, the holding of it being the finding. [INV-191, INV-153]

**Case: a concern no zone owns**

5. *when* a concern is real work whose owning zone does not exist yet, the system *shall* carry it to the pack's inbox. Sweeping that inbox, the pack repo's assigned session *shall* answer who owns it. [INV-197, T-22, INV-182, INV-97, T-10]
   - the answer names an existing agent, a new agent the owner ratifies, or a skill.
6. *while* ownership is being settled, the agent *shall* do the work it can do now in whatever tree can hold it and mark that work provisional, the re-home landing later as ordinary pipeline work. [INV-197]

**Case: the crossing bound**

7. the system *shall* let one question cross between the same two agents at most twice, counted by the message identifier, and *shall* send the third crossing to the owner. [INV-196, INV-192, INV-27, INV-130]
   - the sender's status report names the third crossing as a zone question the two could not settle;
   - this is the shape the human-decision withdrawal loop already takes.
8. neither agent *shall* reopen the count by rewording the question. [INV-196]

**Case: a wrong referral is named**

9. *when* an exchange reaches the crossing bound through a referral met by a counter-referral between the same two agents, the system *shall* name the wrong referral in the sender's status report. [INV-225, INV-196, INV-27]
   - a wrong referral pointed at a zone which, by its own referring-back, does not own the target.
10. *when* a referral is answered by an acceptance, or an onward referral to a third zone answers it, the system *shall* reach no bound and name nothing. [INV-225]
11. the checker `guardrails/check-wrong-referral.py` *shall* read the shape of the exchange and ride the suite, staying clear of the push chain — the sequence of checks a push runs — *while* whether the target falls inside a zone's claim stays the receiving sweep's and the reviewer's judgment. [INV-225, INV-150, INV-222]

**Case: the message identifier**

12. the system *shall* mint a stable identifier per message from the sender's session identity plus a discriminator the sender mints for that message, so one session's two messages carry two identifiers. [INV-192, INV-117]
   - the sender's session identity is the harness session id where the context carries one, or else the session's start time joined with its worktree path and a nonce, recorded in the session checkpoint;
   - an exchange is keyed to its first message's identifier, which every reply names, so the crossing bound counts questions rather than sessions and outlives the sender's own session.
13. a reply *shall* name the message by that identifier after the file has left the inbox and become a row in the receiver's queue. [INV-192, E-11]

**Case: the reply and the terminal state**

14. a reply *shall* travel back to the sender as one new file in the sender's inbox, owing no blocked work of its own since the message it discharges already named the work. [INV-192, E-11]
15. every message *shall* state its need-by and *shall* reach one terminal state — delivered, declined, or escalated past its stated need-by. [INV-192, INV-1]
    [GAP: the spec does not name what checks that a message has passed its stated need-by, nor who sets the need-by value, so the move to the escalated state has no named watcher.]
16. *when* a message escalates, the system *shall* surface it in the sender's status report as blocked work aged past its need-by, and *shall* wake a dormant window on no occasion. [INV-192, INV-27]

**Case: authority does not travel by relay**

17. an agent-initiated message *shall* stand as a proposal in the receiver's queue until the owner ratifies it, *while* an owner-initiated message carries the owner's authority. [INV-193, INV-94]
18. relaying a message *shall* change only its carrier and leave its authority where it started. [INV-193, INV-94]

**Case: zones may overlap**

19. the system *shall* let two agents' zones overlap, each card recording what its own agent claims and two cards claiming one area both standing, and *shall* force no agent to carve a disjoint zone. [INV-197, INV-225]
20. the system *shall* build no uniqueness check over zone claims, the wrong referral alone earning a name. [INV-225]

---

## Requirement 197: A new agent is created only on the owner's word  [feature: F-agent-birth]

**Context:** An agent reaches this point when a capability pins to no agent's zone, or when a capability has outgrown the agent hosting it. Any agent may propose a new agent, and the owner alone brings a new tree into being. The founded agent then declares itself by writing its own card, so every scan finds it from that moment.

**User Story:** As the owner of the machine, I want a new agent created only on my own word and declared by its own hand, so that a new tree and its standing cost never come into being without me and every scan still finds what is really there.

### Acceptance Criteria

**Case: any agent may propose**

1. *when* a capability pins to no agent's zone, or a capability has outgrown its host, the system *shall* let any agent propose a new agent, naming the capability, the zone the new agent would own, and the contracts it would publish. [T-22]
   [GAP: the spec does not name who judges that a capability has outgrown its host, or by what measure.]
2. the proposal *shall* carry the adversarial read an expensive decision earns and *shall* stand as a proposal until the owner ratifies the creation. [T-22, INV-235, INV-193]

**Case: the owner ratifies, the agent declares itself**

3. the owner's word *shall* authorize the creation, since a new agent is a new tree, a new queue, a new set of gates, and a standing cost the owner carries. [T-22, INV-10]
4. the owner *shall* ratify on the adversarial read the proposal carries, the read reaching the owner with its findings and a recommendation and the taste call staying the owner's. [T-22, INV-235, INV-143]
5. the founded agent *shall* declare itself by writing its own card, and every scan *shall* find it from that moment, no third party seating it. [T-22, E-32]
6. creating an agent *shall* be a delivery, so the new tree's journal *shall* record it with its date and the request row it cites. [T-22, INV-3, INV-24]

**Case: a false declaration travels the same scan**

7. *when* a tree declares itself with a card the owner never authorized, the system *shall* show that card in the same scan that finds every other, so the owner reading it sees what stands on the machine. [T-22, E-32]
   [GAP: no gate today catches a card whose creation carries no ratification, and the spec records that this behaviour owes one.]

**Case: the contract survives the migration**

8. *when* a capability moves from its old host to a new agent, the system *shall* let the consumer keep reading its pinned version until it chooses to move, the new owner publishing at the address its own card names. [T-22, INV-187, E-32]

**Case: the kind is the owner's call**

9. *when* a capability sits on the line between a skill and an agent, the owner's word *shall* settle which it is, the call recorded with its date in the proposing agent's journal. [T-22, INV-182, INV-152, INV-24]

## Requirement 198: The shared rules live once in the base skill

**Context:** Open any skill in the pack and the same working rules meet the reader. The five rules every skill works by are these: ask and never guess, plain words with the code trailing quietly, one surface with one name, one canonical home per fact, and a worker resuming from a checkpoint. These rules live once in the base skill, the pack's shared rulebook, and each working skill references them rather than restating them.

**User Story:** As a reader opening any skill in the pack, I want the shared rules stated once in the base skill and only referenced elsewhere, so that every skill reads one authoritative copy and no near-copy drifts.

### Acceptance Criteria

**Case: the shared rules have one home**

1. The base skill *shall* state each shared rule normatively beside the pack's default settings, and every working skill *shall* reference the shared rules rather than restate them. [E-12, E-13]
2. *when* a working skill states a shared rule in full a second time, the system *shall* read it as drift and fold it back, since a shared rule has one normative home in the base skill. [INV-13]
3. The pack *shall* treat the package as the source and the standalone repositories as read-only mirrors of it. [D-4]

**Case: a working skill names the base and stands alone**

4. Every working skill *shall* open with one line naming the base skill and the base version it was written against, swept in the same session that bumps the base so the pin never goes stale. [E-12]
5. The system *shall* keep a working skill usable outside the pack, its opening line reading as plain advice and nothing in its own domain needing the base installed. [E-12]

**Case: restatements are pruned at milestones**

6. *when* a milestone is reached, the compaction pass *shall* prune restatements older than the base one skill at a time, so no single rewrite is needed. [M-1, INV-13]

---

## Requirement 199: Every place the pack lists its skills names the same set

**Context:** The pack lists its skills in more than one reader-facing place — the working-skills sentence, the closing lists the skills carry, and the README table. A list is the kind of fact that drifts as the pack grows. A check runs at every commit and reds a list that names fewer skills than the complete set. The check's reach is that missing-member drift; a stale extra name past the complete set is outside its net and waits for a reader's pass.

**User Story:** As a reader trusting any skill list in the pack, I want every list to name the identical complete set under a mechanical check, so that a list that has fallen behind the pack turns the suite red instead of misinforming a reader.

### Acceptance Criteria

**Case: the lists agree or the suite reds**

1. The system *shall* name the identical complete set of skills in every place the pack lists them — the working-skills sentence, the closing lists, and the README table. [INV-66]
2. *when* a commit leaves a skill list naming fewer than the complete set, the system *shall* red the suite. [INV-66]

---

## Requirement 200: The human owns the taste calls and the working contract

**Context:** The human owns taste, design, the irreversible and publish and push gates, domain wording, and the human's own working contract. The settings ladder resolves to that contract before every human-facing exchange. Mode and trust are set only on the human's word; the agent may propose a level and never raises its own.

**User Story:** As the person a project serves, I want taste and the gates and my own working contract to stay mine and my mode and trust set only on my word, so that every call that turns on taste or preference rests with me.

### Acceptance Criteria

**Case: the human owns the taste calls**

1. The system *shall* keep taste, design, the irreversible and publish and push gates, domain wording, and the human's working contract with the human. [ACT-1, INV-9]
2. Communicator *shall* resolve the whole settings ladder to the working contract before every human-facing exchange, reading the resolved contract rather than one file. [E-13]

**Case: mode and trust move only on the human's word**

3. The system *shall* set proactivity mode and trust only on the human's word, and the agent *shall* propose a level while it never raises its own. [INV-9]
4. The system *shall* hold the lines about the human — proactivity mode, trust, language, and domain vocabulary — in the human's personal profile, following the human across every project. [E-13]

**Case: the host profile lives with the host**

5. The system *shall* create the host profile at attach and keep it git-tracked in the host repository beside the adopt artifacts. [A-8, E-8]
6. The system *shall* keep only the checkpoints ignored inside `.live-spec/`, every other host-profile line staying tracked. [ACT-3, E-8]

---

## Requirement 201: A done-claim is settled by an evidence walk

**Context:** A fluent story can answer any done-claim and might even be right, yet it does not tell a verified fact from a narrated one. So no one answers a done-claim from memory: every claim pins to a checkable artifact walked fresh — an adoption record, a prover record, a suite run with its count, a git commit, a matrix row. The answer states what the walk verified apart from what it merely asserts and names the method version the work was done under.

**User Story:** As a person asking whether a piece of work is done, I want the answer walked fresh from claim to artifact to method version, so that a done-claim rests on freshly checked evidence.

### Acceptance Criteria

**Case: the claim walks its evidence**

1. *when* a done-claim is answered, the system *shall* walk it fresh from the claim to a checkable artifact to the method version, and *shall* state what the walk verified apart from what it merely asserts. [INV-25]
2. The system *shall* read the method version from the host's installed set, naming the pack and skill versions from their version homes. [INV-25, M-7]
3. The system *shall* answer no done-claim from memory, treating a claim with no walked artifact behind it as unproven. [INV-25]

**Case: the version is named or its absence is**

4. The system *shall* name the method version on the claim line, so one claim line reads claim, then artifact, then version. [INV-25, M-7]
5. *if* the host carries no installed set, *then* the system *shall* say exactly that, an absent version being an honest answer and never an invented one. [INV-25, M-7]

---

## Requirement 202: Settings climb a four-scope ladder and the narrowest word wins

**Context:** Every way the pack behaves for the human is a named setting with a home in exactly one of four nested scopes: the package defaults, the personal profile, the host profile, and the session's live word. The scopes nest, and resolution reads from the narrowest outward — the session word over the host, the host over the personal profile, the personal profile over the package default. Profiles are re-read at the same freshness points as skills.

**User Story:** As a person whose preferences live at different scopes, I want each setting resolved from the narrowest scope outward, so that a project or a single sitting can override a broader default on my word.

### Acceptance Criteria

**Case: each setting has one scope and the narrowest wins**

1. The system *shall* give every setting a home in one of four nested scopes — the package defaults in the base skill, the personal profile, the host profile, and the session's live word. [E-13, E-12, E-8]
2. The system *shall* resolve a setting from the narrowest scope outward, the session word overriding the host, the host overriding the personal profile, and the personal profile overriding the package default. [E-13]

**Case: profiles are re-read and an unreadable line is ignored aloud**

3. The system *shall* re-read profiles at the same freshness points as skills. [A-7]
4. *when* a profile line falls outside the current pack's vocabulary, the system *shall* ignore it aloud through a dated journal note and a line in the session's next status report, the journal note standing even *if* the session dies before its report. [E-13]

---

## Requirement 203: No override is ever silent

**Context:** An override exists only as a written line in the profile it governs, and setting one leaves a dated note in that home's journal — the host's journal for a host line, the package's journal for a default change. This is the no-silent-micro-decisions rule applied to settings.

**User Story:** As a person auditing how the pack was tuned, I want every override written as a profile line and journaled where it governs, so that no setting changes silently and the record stays readable.

### Acceptance Criteria

**Case: an override is written and journaled**

1. The system *shall* record every override as a written line in its profile file and *shall* leave a dated journal note in the home it governs. [INV-14, INV-5]
2. The system *shall* journal a host line in the host's journal and a default change in the package's journal. [INV-14]

**Case: a tighter host line is recorded**

3. The system *shall* let a host contract tighten a package default and *shall* record the tighter line where a reader sees it rather than assume it. [M-6, INV-14]
4. The system *shall* keep the push gate's own cadence as the worked example, the package default asking a full prover pass before a minor bump and a host contract tightening it to before every push. [M-6]

---

## Requirement 204: The session scope is never a file

**Context:** The session scope is the one scope that is never a file: a session override lives only in the human's spoken word and dies with the conversation, and the agent never writes it on its own. Should it outlive the session, that is a promotion into the profile it describes, made on the human's word and journaled. A full wipe ends the sitting and the session lines die with it by design.

**User Story:** As a person setting something for one sitting, I want the session override to live only in my spoken word and die with the conversation unless I promote it, so that a passing choice never silently becomes permanent.

### Acceptance Criteria

**Case: the session word dies with the sitting**

1. The system *shall* keep a session override only in the human's spoken word and *shall* never write it to a file on its own. [INV-14]
2. *when* a session override should outlive the session, the system *shall* promote it into the profile it describes on the human's word and journal it like any other override. [INV-14]

**Case: a wipe ends the sitting**

3. *when* an announced self-compaction runs, the system *shall* carry the live session lines forward in its summary. [M-2, INV-14]
4. *when* a full wipe ends the sitting, the system *shall* let the session lines die with it, since that loss is the human's own move. [INV-14]

---

## Requirement 205: The personal layer has one home and the loader stays thin

**Context:** Everything personal lives in one place, the personal profile, and the machine-global instruction file shrinks to a thin loader carrying only the bootstrap lines that must hold before any pack file loads. Migrating an existing rule file into this shape forks each rule to the scope it describes — a method rule stays the pack's, a personal line moves to the profile, a project line moves to that project's host profile. A rule-by-rule mapping proves the move lossless and the old file stays in the attic.

**User Story:** As a person consolidating a tangled rule file, I want each rule forked to the scope it describes with the old file kept in the attic, so that the personal layer has one home and one move rolls the whole change back.

### Acceptance Criteria

**Case: one home and a thin loader**

1. The system *shall* keep the personal layer in the personal profile and *shall* shrink the global instruction file to a thin loader carrying only the bootstrap lines that must hold before any pack file loads. [E-16, INV-13]
2. The system *shall* keep the loader the one home for those bootstrap lines and *shall* never restate them in the profile. [INV-13]

**Case: a rule file forks by scope, losing nothing**

3. *when* an existing rule file is migrated, the system *shall* fork each rule to the scope it describes. [E-16, INV-10]
   - a method rule stays the pack's;
   - a personal line moves to the profile;
   - a project line becomes a migration note for that project's own session to land.
4. The system *shall* prove the move lossless rule by rule and *shall* keep the old file in the attic, so one move rolls the change back. [E-16, INV-7]
5. *while* the promotion sits outside any repository fence, the system *shall* re-read the file immediately before appending, its git home standing as the recovery net. [INV-11, E-16]

---

## Requirement 206: The seat owns judgment and workers run the tiers

**Context:** The seat owns every judgment call — spec deltas, matrix levels, findings triage, and this document. Workers own mechanical execution, each keeping a persistent checkpoint file under the host's `.live-spec/checkpoints/`. Three tiers stand: a no-decision one-shot worker, a multi-step mechanical worker, and the seat for judgment.

**User Story:** As a person watching work split between judgment and mechanism, I want judgment held by the seat and mechanical work run by tiered workers with durable checkpoints, so that the calls that shape the work stay with the agent qualified to make them.

### Acceptance Criteria

**Case: judgment stays with the seat**

1. The seat *shall* own every judgment call — spec deltas, matrix levels, findings triage, and this document — and that judgment *shall* never route down to a worker. [ACT-2]
2. The routing rule *shall* propose which tier a unit of work runs at before the seat may overrule it. [INV-69]

**Case: workers run the mechanical tiers**

3. The system *shall* run mechanical work on tiered workers — a no-decision one-shot worker, a multi-step mechanical worker, and the seat for judgment. [INV-69]
4. Each worker *shall* keep a persistent checkpoint file under the host's `.live-spec/checkpoints/`, kept out of git and off the temporary directory so a reboot never erases a resume point. [ACT-3, INV-69]

---

## Requirement 207: The worker contract binds every delegation

**Context:** One contract binds every delegation. A worker inherits its session's write-ownership narrowed to the files its brief names, reads outside them, and never writes there. Its brief carries the clock, the live setting lines, and the problem-ledger duty, and it heartbeats its checkpoint so a busy worker is never mistaken for a dead one. At teardown the worker reaps only the process group it spawned.

**User Story:** As a person relying on delegated work, I want every worker bound by one contract — narrowed write-ownership, an inherited clock and settings, a ledger duty, a heartbeat, and a scoped teardown — so that parallel help never corrupts the tree or the record.

### Acceptance Criteria

**Case: write-ownership is narrowed to the brief**

1. A worker *shall* inherit its session's write-ownership narrowed to the files its brief names, reading outside them and never writing there. [INV-10]
2. *when* a brief names an isolated copy of the tree, the system *shall* let that copy's delta reach the shared tree only through the seat's integration under the pen. [T-18, INV-39]
3. *when* the seat means to spawn another concurrent writer, it *shall* confirm the brief's write-set is disjoint from every running writer's brief or give it an isolated worktree, since the concurrent-edit fence stays quiet between same-session siblings. [INV-11, INV-105, ACT-3]

**Case: the brief carries the clock, the settings, and the ledger**

4. The system *shall* ride the session's live setting lines into the brief verbatim, since a worker cannot resolve the ladder itself. [E-13]
5. The system *shall* carry the clock into the brief so a worker's stamps come off the brief's clock and are never invented, and *shall* carry the problem-ledger path so any noise the worker meets becomes one recorded ledger line. [INV-24, INV-23]

**Case: the heartbeat and the scoped teardown**

6. A worker *shall* touch its checkpoint file on a fixed interval near 60 seconds as a heartbeat, so a compute-bound run that writes no product file for minutes is never read as dead. [INV-76]
7. *when* a result fails its brief's acceptance, the worker *shall* escalate one tier with a logged line and *shall* never retry silently on the same tier or skip a rung. [ACT-3]
8. *when* a worker tears down, the system *shall* reap only the process group it spawned, reading a stall as the checkpoint's modification time going untouched past about 2 minutes and confirming ownership before any reap, never a kill by name. [INV-162, INV-230, INV-76]

---

## Requirement 208: The routing rule proposes the cheapest tier and the senior may overrule

**Context:** Before anyone delegates a unit of work, the routing rule proposes its tier from what the work is, its size only a coarse prior — a judgment step to the seat and never down, a no-decision one-shot to the cheapest worker, a multi-step mechanical brief to the mid worker. The economy rung moves the threshold. The proposal is advisory: the seat may overrule it per wish, and the override rides one logged line reading proposed tier, chosen tier, and why.

**User Story:** As a person paying for the right tier on each unit of work, I want the routing rule to propose the cheapest tier that can pass the brief and the senior's override always logged, so that no tier changes silently and judgment work never routes down.

### Acceptance Criteria

**Case: the proposal reads the work**

1. The routing rule *shall* propose a judgment step to the seat and never route it down, a no-decision one-shot to the cheapest worker, and a multi-step mechanical brief to the mid worker. [INV-69, ACT-2]
2. The system *shall* treat the size class as a coarse prior only, the step inside the work deciding its tier. [INV-69]

**Case: the economy rung moves the threshold**

3. *when* the economy rung is lean, the system *shall* let an airtight brief — one that leaves the worker nothing to decide — ride one tier cheaper and *shall* raise the bar for keeping a step on the seat. [T-19, INV-69]
4. *when* the economy rung is tight, the system *shall* propose the cheapest tier that can pass the brief and *shall* spend the seat's hours on judgment alone. [T-19, INV-69]

**Case: the override is advisory and logged**

5. The seat *shall* be free to overrule the proposal per wish, and the system *shall* ride one logged line — proposed tier, chosen tier, and why — on the checkpoint and the delivery report. [D-2, INV-69]
6. The system *shall* keep this assignment-time override distinct from the failed-acceptance escalation, both logged on their own lines, so a silent tier change cannot stand. [ACT-3, INV-69]

**Case: an expensive dispatch proves its own need**

7. *when* a unit of work is dispatched to the expensive tier, the system *shall* open its brief with the refusal instruction, which assumes a cheaper tier and asks the run to answer first. [INV-300, INV-69]
   - the instruction and the tier ladder live in `guardrails/tier-refusal.json`;
   - a refusing run replies with one line naming the tier that fits and the reason.
8. *when* a run refuses, the system *shall* record the refusal with its task text, the named tier, the reason, and the date, and *shall* re-run the same brief at the named tier. [INV-300]
9. The system *shall* turn a task away before any model call once three recorded refusals name one tier and share a phrase from their task texts. [INV-300]
   - the promoted phrases sit in `guardrails/tier-refusal.json`, where a person reads them.

---

## Requirement 209: A delivered row carries its delegation accounting

**Context:** Every delivered queue row records how its work was delegated: the unit that went to a worker with an estimated saving, or a stood-down line naming why the seat kept the work. The line rides the delivery report the archived row carries, and a suite check reds a delivered row that omits it, reading it from the archive for a row landed after the format conversion. The duty binds the orchestrating seat whatever tier leads it.

**User Story:** As a person auditing how work was delegated, I want every delivered row to carry its delegation accounting under a suite check, so that the account of who did each piece of work is never silently dropped.

### Acceptance Criteria

**Case: the delivered row carries the line**

1. The system *shall* record on each delivered row's delivery report how its work was delegated — the unit sent to a worker with its saving, or why the seat kept it — and *shall* red the suite *when* a row landed after the conversion omits the line, reading it from the archive. [INV-103, INV-276]
   [GAP: the delegation accounting records a saving for each delegated unit, but the source names no unit or baseline the saving is measured against — tokens, wall-time, or cost — so a correct saving figure is undefined and a test author cannot pin it.]
2. The system *shall* bind the duty to the orchestrating seat whatever tier leads it, and *shall* bind it forward from its own reach rather than over rows already delivered. [INV-103, INV-159]

---

## Requirement 210: The seat reads to decide and dispatches the discovery reads

**Context:** The seat keeps its context lean by dispatching reads rather than performing them. It holds orchestration material — the human's words, the decisions taken, the distilled results workers return, and the anchors it must cite — and dispatches any reading done to understand or design past a bounded glance to a reader worker that returns a distillation. A read done to verify a claim or settle a decision stays with the seat. The leanness is load-bearing: a context filled with raw source it could have distilled loses the room to hold the whole arc.

**User Story:** As a person relying on the seat's judgment across a long arc, I want discovery reads dispatched to reader workers and only distillations kept, so that the seat's context stays lean and its judgment does not degrade under raw source.

### Acceptance Criteria

**Case: discovery reads route to workers**

1. The seat *shall* dispatch any read done to understand or design past a bounded glance to a reader worker and *shall* keep only the distillation. [INV-137, INV-69]
2. The system *shall* bound a glance to one small file or a handful of targeted lines whose result is itself the deliverable, past which the read routes like any unit of work. [INV-137, INV-69]
   [GAP: the glance's size bound carries no number in the source; its only stated test is that the read's result is itself the deliverable.]

**Case: verify reads stay, discovery reads show**

3. The system *shall* keep a read done to verify a claim or settle a decision with the seat, checking the real artifact and re-reading a primary source being its own hands. [INV-137]
4. The system *shall* dispatch the brief-owed read of the files a change will touch to the reader worker whose distillation returns the per-file lines, or make it a bounded decide-read for a small edit. [INV-53, INV-137]
   [GAP: the source names no size or line count for a small edit here, so where a bounded decide-read ends and a dispatched read begins is undefined.]
5. The system *shall* name the reads dispatched in the delivery report's delegation accounting, so a session that slid into reading to discover shows it. [INV-103, INV-137]

---

## Requirement 211: The seat decides what it can and surfaces only what it cannot

**Context:** The seat decides what it can decide and reports the choice — a mechanical step, a value a proven artifact already determines, a sensible default it can pick and name. It surfaces a decision to the human only where the decision genuinely cannot be made without them: a taste call, a trade-off no artifact settles, or a change to the definition of correct. It never parks derivable work on the human's queue to avoid deciding, and the posture holds even on a session resumed from its files after a memory wipe.

**User Story:** As a person who should be asked only what genuinely needs me, I want the seat to decide every derivable question and report it, so that a taste call reaches me while derivable work never waits on my queue.

### Acceptance Criteria

**Case: it decides what an artifact or a default settles**

1. The seat *shall* decide a mechanical step, a value a proven artifact already determines, or a default it can pick, and *shall* report the choice with its `[default]` tag. [INV-143, INV-121, INV-70]
2. The system *shall* hold this posture on every session, including one resumed from its files after a memory wipe. [INV-143, INV-48]

**Case: it surfaces only what needs the human**

3. The seat *shall* surface a decision to the human only where it cannot be made without them — a taste call, a trade-off no artifact settles, or a change to the definition of correct. [INV-143, INV-121]
4. The system *shall* never park derivable work on the human's queue to avoid deciding. [INV-143, INV-4]

---

## Requirement 212: A deferral must justify itself or the item is the seat's to do

**Context:** A backlog item carrying a needs-the-human's-word marker is re-tested for derivability every time it is touched, not only when first written. Where the answer pins to an existing artifact — a base rule, a spec sentence, the architecture, an approved prototype, or an already-answered decision — the item is the seat's to do, cite, and drop the marker. Where it needs a fact no artifact holds — a taste, a policy, a move irreversible outside git, or the feel of a real device — it is the human's and the marker stands, but writing the marker requires naming that human-only fact.

**User Story:** As a person handed only the questions that truly need me, I want every deferral marker re-tested for derivability and made to name its human-only fact, so that a derivable item becomes the seat's own work and stays off my board.

### Acceptance Criteria

**Case: a derivable item is the seat's**

1. *when* a held backlog item is touched, the system *shall* re-test it for derivability, and *when* the answer pins to an existing artifact the seat *shall* do the item, cite the artifact, and drop the marker. [INV-152, INV-59, INV-121, INV-143]
2. *if* the item needs a fact no artifact holds — a taste, a policy, a move irreversible outside git, or the feel of a real device (a feel judged only by the human's own hand on the human's own device) — *then* the marker *shall* stand and *shall* name that human-only fact. [INV-152, INV-17]
3. The system *shall* default a marker that cannot name its human-only fact to the seat's own, the unnamed marker being the finding, the same shape as a request matching no kind in the closed door set. [INV-152, INV-151]

**Case: two arms enforce the deferral**

4. The system *shall* red a commit *when* a mechanical net finds a parked item in the resume file or a decision page naming no reason category — taste, policy, irreversible, or device-feel (a feel judged only by the human's own hand on the human's own device). [INV-152, INV-155]
5. *when* a marker is written or a question is opened to the human, a delivery arm *shall* re-fire the derivability test at that moment, reading the grammatical shape of a deferral itself. [INV-152, INV-28, INV-4]

---

## Requirement 213: A worker's green earns a second pair of eyes

**Context:** A worker's report is a lead and never counts as evidence, since the head that made the work is blind to its own gap. So the verify step carries an audit — a whole-read that sets out to break the work: a fresh-context checker briefed with the spec sentences the delivery claims and the artifact paths, never the worker's summary or the senior's plan. It walks each claimed fact up a fixed ladder — that it exists, that it is substantive, that it is wired, and that real values flow end to end — and its findings become rows or red.

**User Story:** As a person trusting a green suite, I want a high-stakes delivery whose only review is its author's checked by a fresh adversarial reader, so that a green machine that is actually hollow is caught before it is called done.

### Acceptance Criteria

**Case: the audit walks a fixed ladder from a fresh context**

1. The verify step *shall* brief a fresh-context checker with the delivery's spec sentences and artifact paths, never the worker's summary or the senior's plan, opening on the hypothesis that the tasks were done and the goal missed. [INV-46]
2. The checker *shall* walk each claimed fact up a fixed ladder — that it exists, that it is substantive against the placeholder-stub list, that it is wired, and that real values flow end to end — its findings becoming rows or red. [INV-46]

**Case: it fires mandatory on a high-stakes author-only delivery**

3. The system *shall* fire the audit mandatory *when* a delivery is high-stakes and its only review is the author's own. [INV-46]
   - a delivery is high-stakes when it is a surface-sized delta or a change to the method itself;
   - a change to the method itself means a rule whose meaning changed.
4. The system *shall* count a review independent only *when* a differently-contexted head is briefed from the primary sources on the goal-missed hypothesis, a same-context prover pass never counting and delegation alone never making it independent. [INV-46]
5. One fresh checker *shall* cover every law in a delivery batch, the checker being a worker under its own contract whose verdict rides the delivery report. [INV-61, ACT-3]

---

## Requirement 214: An expensive decision earns an adversarial read before it lands

**Context:** A decision is expensive when unwinding it costs more than making it did, and the pack's expensive decisions are a closed, enumerable set: the birth of a new agent, a node carved or merged in the architecture, the shape of a contract once a consumer has pinned it, a project's kind, the split of a reusable product into engine and instance, and a repository going public. No machine tells an expensive decision from an ordinary one, so the duty is stated for the whole class and each member carries it at its own decision point as the pack wires it. The read is a fresh-context independent audit that closes by bringing the decision to the human with findings and a recommendation.

**User Story:** As a person owning the taste call on a costly decision, I want each expensive decision to earn a fresh adversarial read that reaches me with findings and a recommendation, so that the call rests on a case already broken and tested.

### Acceptance Criteria

**Case: the class is closed and enumerated**

1. The system *shall* treat the expensive-decision set as closed and enumerable, naming every member as either enumerated on its own row or riding inside another row's work. [INV-235, T-22, INV-113, INV-122, INV-187, INV-36, INV-85, INV-44, INV-226]
   - the set holds: an agent's birth, a node carved or merged, a contract's shape once a consumer pinned it, a project's kind, an engine-and-instance split, and a repository going public.
2. The system *shall* state the duty for the whole class and have each member carry it at its own decision point, a traceability test holding that this clause names the read and that agent birth carries it; that test *shall* ride the suite and take no push-gate letter, since no gate reads a reversal cost, the far-tier and node-growth checks the precedent. [INV-235]

**Case: the read is adversarial and closes with the human**

3. *when* an expensive decision is about to land, the system *shall* run a fresh-context independent audit at the best tier the pack's quality habit sets, set on breaking the case as the verify audit reads a delivery. [INV-235, INV-46, INV-145]
   [GAP: the read runs at the best tier the pack's quality habit sets, but the source neither defines that quality habit nor states which tier it yields for this read, so the read's out-of-box model tier is unstated.]
4. *where* the decision turns on whether members are one kind, the design review *shall* read the grouping with the two compared objects in hand. [INV-235, INV-141, INV-142]
5. The read *shall* close by bringing the decision to the human with its findings and a recommendation, the taste call staying the human's because it needs a fact only the human holds. [INV-235, INV-143, INV-152]

---

## Requirement 215: The authoring seat does not certify its own work

**Context:** The seat that authored a change drafts and accepts it but never provides its own adversarial certification, since a head marinated in the authoring context is blind to the gap it just wrote. Two carriers follow. A release's adversarial pass — the full prover re-prove at the release gate — is authored by a fresh, differently-contexted seat, and a newly added lens or rule is applied to the very document that introduces it before release. The release gate may require a dated clean-context review record naming a seat other than the release's.

**User Story:** As a person trusting a release, I want its adversarial pass run by a fresh seat and every new rule applied to its own introducing document, so that an authoring-blind gap is caught by a differently-contexted head before the release ships.

### Acceptance Criteria

**Case: the author drafts but does not certify**

1. The system *shall* let the authoring seat draft and accept a change and *shall* never let it provide the change's own adversarial certification. [INV-237]
2. The system *shall* author a release's adversarial pass — the full prover re-prove at the release gate — with a fresh, differently-contexted seat under the freshness the verify audit already defines. [INV-237, INV-116, INV-217, INV-46, INV-145]

**Case: a new rule is self-applied and the record names a fresh seat**

3. *when* a release is prepared, the system *shall* apply a newly added lens or rule to the document that introduces it and *shall* name the result in the release record. [INV-237]
4. The release gate *shall* be able to require a dated review record that exists, is dated to the release, and names a seat other than the release's. [INV-237]

---

## Requirement 216: A brief is born from read files, never from memory

**Context:** Before writing a brief that edits existing files, the brief-writer reads in full every file the work will modify. The brief records three lines per file — its current state, what changes, and what must survive — and every step back-references the spec sentence it serves while every technical claim cites its source. A brief written from memory hands the worker a guess dressed up as fact.

**User Story:** As a worker handed a brief, I want it born from a full read of the files it touches with three recorded lines each, so that I am handed evidence rather than the senior's guess.

### Acceptance Criteria

**Case: the brief is read from the files**

1. The system *shall* write a brief that edits existing files only after reading in full every file the work will modify, recording three lines per file — current state, what changes, and what must survive. [INV-53]
2. The system *shall* have every step back-reference its spec sentence and every technical claim cite its source as a file-and-line reference or a command's output. [INV-53]
3. The system *shall* dispatch this read to the reader worker whose distillation returns the three per-file lines, or make it a bounded decide-read for a small edit. [INV-53, INV-137]
   [GAP: the source names no size or line count for a small edit at this second occurrence either, so a test author cannot pin the boundary case.]

---

## Requirement 217: A worker stops only on a named condition

**Context:** The brief carries a closed, short halt list: an ambiguous requirement, two consecutive unexplained failures of one command, a missing config or dependency, or an acceptance impossible as briefed. On any of these the worker stops with evidence; otherwise it runs to completion. This is sharper than an open standing instruction to ask when unsure, and it composes with the one-tier escalation.

**User Story:** As a person delegating a bounded job, I want the worker to stop only on a closed list of named conditions and otherwise run to completion, so that it neither pushes past a real blocker nor stalls on ordinary uncertainty.

### Acceptance Criteria

**Case: the closed halt list**

1. The system *shall* carry a closed halt list in the brief — an ambiguous requirement, two consecutive unexplained failures of one command, a missing config or dependency, or an acceptance impossible as briefed. [INV-54]
2. *when* a halt condition holds, the worker *shall* stop with evidence, and otherwise *shall* run to completion, composing with the one-tier escalation. [INV-54, ACT-3]

---

## Requirement 218: A brief is sized to its worker's head

**Context:** A brief targets a bounded share of its worker's context and splits above it, the default bound being the brief's own text within about 300 lines and at most about 8 files to edit. Above either limit the work splits into staged briefs. A brief passes paths and never inlined file bodies, since an inlined body goes stale the moment a sibling edits the file.

**User Story:** As a worker with a bounded head, I want a brief kept under a concrete size bound and passing paths not file bodies, so that I read my own current truth from disk and no pasted copy goes stale.

### Acceptance Criteria

**Case: the size bound and the split**

1. The system *shall* keep a brief within its default bound — about 300 lines of brief text and at most about 8 files to edit — and *shall* split the work into staged briefs above either limit. [INV-55]
2. The system *shall* pass paths in a brief and never an inlined file body, so the worker reads its own current truth from disk. [INV-55]

---

## Requirement 219: The economy ladder names what a tight budget may shed

**Context:** Rigor costs money and time, so the pack names what a tight budget may legally shed and makes it a setting the human moved deliberately. The pressure lives as one setting, `budget.pressure`, with package default full, and it moves only on the human's word. Three rungs each name their legal sheds, and every shed actually taken is said in the delivery report.

**User Story:** As a person under a money or time pressure, I want the sheds named as a rung I set rather than improvised, so that cost-cutting is a recorded choice and every shed appears in the delivery report.

### Acceptance Criteria

**Case: the rung is a setting the human moved**

1. The system *shall* hold the pressure as one setting, `budget.pressure`, defaulting to full, moved only on the human's word — a session word for today or a profile line to stand. [T-19, E-13, INV-9]
2. *when* the human names a money or time pressure, the agent *shall* propose a rung and *shall* never set one, and the pack *shall* ask the rung or state the standing default at project setup beside the project kind. [T-19, INV-36]

**Case: each rung names its legal sheds**

3. *when* the rung is full, the system *shall* run the full suite at every delivery gate, run the prover at its recorded cadence, and route tiers by the routing rule. [T-19, INV-69]
4. *when* the rung is lean, the system *shall* scope mid-work test runs to the touched architecture node's rows while running the full suite at every delivery gate and before every push, and *shall* write a deferred full pass as a dated debt line in its queue row. [T-19, INV-69]
5. *when* the rung is tight, the system *shall* batch consecutive small deliveries into one full-suite run at the batch's end, keep each commit at one row's delta, and bisect a batch-end red by delivery order before reverting to the last green base. [T-19, INV-39]
   [GAP: the source names no size or count bound for a small delivery under the tight rung, so which deliveries qualify to share one batch-end run is unstated.]
6. *when* a push runs under any rung, the system *shall* still require the batch's reach-scoped gate green at the tree's head and the host's recorded prover cadence. [INV-45, M-6]

**Case: the tight rung's batch rollback**

7. *when* a batch-end run reds under the tight rung, the system *shall* bisect by delivery order; the system reverts the batch to its last green base and re-applies the clean landings, so `HEAD` never sits red across a breakpoint. [INV-39, T-19]

---

## Requirement 220: The never-bend list holds at every rung

**Context:** A short list of protections holds at every rung of the economy ladder no matter how tight the budget, and this never-bend list does not bend. It carries the door law and its tripwires, red-before-fix, the human's gates, the delivery report with its taken defaults and named sheds, delivery purity, the push gate running every check the diff can reach, the safety net, and whole narration. An explicit host line outlives any rung. The standard the work is held to stands outside every rung as well. A rung moves the project's pace, and a check the method calls for runs at whatever the plan costs.

**User Story:** As a person cutting cost under pressure, I want a named never-bend list that no rung touches, so that a tight budget slows spend without dropping the guarantees that matter.

### Acceptance Criteria

**Case: what never bends**

1. The system *shall* hold at every rung the door law and its tripwires, red-before-fix, and the human's gates over irreversible moves, publishing, authored content, and taste. [INV-40, T-12, INV-16, INV-9]
2. The system *shall* hold at every rung the delivery report carrying its taken defaults and named sheds, delivery purity at one row's delta per commit, and whole narration. [INV-40, INV-5, INV-31, INV-39, INV-35]
3. The system *shall* hold at every rung the push gate — work leaving the machine only when every check the diff can reach is green at the tree's head, plus the host's recorded prover cadence — and the safety net no work-kind or scope cut touches. [INV-40, INV-45, M-6, T-15, T-16]

**Case: an explicit host line outlives the rung**

4. *when* a host profile pins a tighter cadence, the system *shall* keep it even under the tight rung. [E-13, INV-40]
5. The system *shall* move `budget.pressure` only by the human's word and *shall* switch no rung automatically. [T-19, INV-40]

**Case: a rung moves the pace alone**

6. The system *shall* hold at every rung the standard the work is held to, moving the project's pace alone. [INV-40, T-19]
7. The system *shall* run a check the method calls for at whatever the plan costs. [INV-40, T-19]
8. The system *shall* hold at every rung the fresh clean-context agent any ask of the method raises. [INV-40, INV-46]
9. The system *shall* count an adversarial review, a cold reading, a release re-prove, and a deep audit among those asks. [INV-46, INV-145, INV-237, INV-266]
10. The system *shall* buy economy from pace, from batching, and from a cheaper tier on mechanical work, and *shall* buy it from no check. [INV-40, T-19, INV-69]

## Requirement 221: Every process converges on a goal named as an artifact

**Context:** Every piece of work the pack runs walks toward a goal. So the work names that goal up front as a concrete artifact it can be measured against — a frozen norm, an exemplar bank, a failing test, a written acceptance. A paraphrase cannot serve as that goal. Each pass measures its distance to the goal itself, and a level once reached is locked by a mechanism so the work cannot slide back. The machines this whole section lists are that principle's hands.

**User Story:** As a person relying on the pack, I want every process to name its goal as a checkable artifact and lock each level it reaches, so that work converges toward the goal rather than drifting near a look-alike.

### Acceptance Criteria

**Case: the goal is a named artifact**

1. *when* a process begins, the system *shall* name its goal as a concrete artifact the work can be held against, and *shall* refuse a paraphrase as that goal. [INV-98]
2. *while* a process runs, the system *shall* measure each pass against the goal artifact itself, since a stand-in is where a look-alike is born. [INV-98]

**Case: a reached level locks**

3. *when* a process reaches a level, the system *shall* lock it by a mechanism — a norm template, a conformance test, a lint floor that only rises, or a cap that only ratchets down. [INV-98]
4. *if* a stretch of work is deliberately divergent, such as an exploration or a labelled prototype, *then* the system *shall* allow it only when it is named and bounded by its convergence point. [INV-98]

---

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
2. *when* the feature-coverage check runs, the system *shall* fail the push *if* a tagged unit resolves to no real implementer node or no real test, and *shall* fail it *if* a promised unit carries no tag. [INV-73]

**Case: every heading declares its status**

3. The system *shall* have a person-facing scenario carry its feature tag on the requirement heading, and *shall* leave a machinery or reference requirement's heading untagged. [INV-132]
4. *when* a promised scenario's requirement heading carries no feature tag, the system *shall* red it in the feature-coverage trace, a promised leg not yet built taking a `[target]` marker on its own line. [INV-132]

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

6. The system *shall* run the prover-record, ownership, coverage, loadability, and prototype-fence checks at every push that carries content, never scoped, except where criterion 7's deletion-only stand-down applies. [INV-40]

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

3. The system *shall* read the universal laws that ship in the mechanism — naming a thing by denying its neighbour, opening a chat sentence with a bare internal code, grading importance or quality without a concrete fact, and showing a coined term with no plain gloss — and *shall* leave the personal laws to an overlay the personal layer owns. [INV-203, INV-221]

**Case: two surfaces, one mechanism**

4. *when* the seat finishes a turn on the chat surface, a Stop arm *shall* dispatch every message shown since the last human turn, and a prompt-submit arm *shall* report the verdict at the person's next message. [INV-203]
5. *when* a styled file is about to be shown, the same judge *shall* stand as the ceiling of the pre-show register gate pointed at that file. [INV-83, INV-203]
6. The contrast-frame scan, the hedge scan, the code-anchor scan, the empty-validation scan, and the tool-boundary scan *shall* each read every message shown since the last human turn through the shared full-turn reader, the reach the register judge's Stop arm carries. [INV-281, INV-203]

**Case: the judge stands down on its own breakage**

7. *if* the judge's own machinery breaks — a missing binary, a timeout, a non-zero exit, or a shape it cannot read — *then* the system *shall* leave the literal-list verdict standing rather than red, so a guard cannot train the guarded to route around it. [INV-203]
8. A scan reading through the shared full-turn reader *shall* stand down *where* the stop hook is already active, or the event payload or the turn's record cannot be read. [INV-281]

---

## Requirement 231: The answer-first arm reds a lead-less wall — retired

**Context:** The Stop-hook proxy this requirement specified ran against real turns with zero catches, a mechanized gate that never once fired. Its retirement is recorded in DECISIONS.md. The answer-first law itself is untouched — it stands permanently in the personal profile and is still reminded at every prompt by the chat-law hook (Requirement 230); only this requirement's own mechanized proxy is gone.

**User Story:** As a person who read the silent runs of this proxy with nothing caught, I want the dead machinery retired rather than left running unread, so that the pack carries no gate that never fires.

### Acceptance Criteria

**Case: retired**

1. The system *shall* carry no Stop-hook arm implementing this proxy; its former file stands retired at `attic/answer-first-scan.py`, never re-armed without a fresh decision. [INV-220]

---

## Requirement 232: Two Stop-hook soft signals: the hedge gate and the lean-orchestrator arm

**Context:** Two once-read behavioural laws gained a mechanical net. The first: a reply that offers to do a thing the seat could already derive and reverse, holding the offer open for a cue, is an offering-hedge. The second: a session that holds raw file content inline without dispatching a worker leaks the orchestrator's context. Each is a Stop-hook soft signal that reads after the fact and corrects one message later; each is honest that it catches only the frames it lists.

**User Story:** As a person relying on the seat to act rather than hedge and to delegate heavy reading, I want each law backed by a cheap literal net, so that a common hedge frame and a pure context-hoard are caught while the class in any phrasing stays with the conduct judge.

### Acceptance Criteria

**Case: the hedge gate**

1. *when* any message the seat showed since the last human turn carries an offering-hedge frame from the pattern list, the system *shall* block the stop with a rewrite instruction reaching the seat one message later. [INV-238, INV-173]
   - a quoted, backticked, or fenced span is stripped from the message before the pattern list is matched;
   - the scissors scan is the literal gate that blocks a sentence naming a thing by denying its neighbour; this arm is modelled on it, matching against an inline universal pattern list and an optional personal-overlay file a host tunes, as the scissors scan carries one;
   - the gate is installed by the setup walk.
2. The system *shall* leave clear of a genuine taste, policy, or irreversible question that names its human-only fact, since that question is an honest admission the human owns. [INV-238, INV-152]
3. The system *shall* catch only the frames it lists, so a paraphrase it does not carry stays with the conduct judge that reads the class in meaning. [INV-238, INV-241]

**Case: the lean-orchestrator arm**

4. *when* cumulative inline raw file content across the session reaches the threshold and the worker-dispatch count is zero, the system *shall* warn that the reading rode no worker dispatch. [INV-246]
5. The system *shall* read the threshold as a tunable parameter defaulting to 50 kibibytes, and *shall* count only a main-thread Read or one of six literal file-dump verbs, a read inside a worker riding a sidechain never counted. [INV-246, INV-70]
6. *when* the seat dispatches its first worker, the system *shall* clear the warning, since one dispatch shows the session is delegating. [INV-246]

**Case: both stand down on their own breakage**

7. *if* a payload or transcript is unreadable, *then* the system *shall* stand the signal down silently, and *shall* have its runs and fires read by the net-liveness meter rather than trusted. [INV-203, INV-202]

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

## Requirement 236: Every point of contact with the person has a kind

**Context:** A moment of contact is synchronous when the person is present and the work waits on the person, and asynchronous when the person reads on the person's own clock while the work keeps running. The kind licenses the traffic: an interruption belongs on a synchronous point, a teaching line on a point the person opens, and waiting traffic on every point. Each touchpoint declares its kind in one manifest, and a gate reds a surface that speaks in a kind its touchpoint lacks.

**User Story:** As a person met by the pack at many points, I want each touchpoint's kind declared and enforced, so that an interruption never rises from a point I read on my own clock and a teaching line only reaches a point I opened.

### Acceptance Criteria

**Case: the kind licenses the traffic**

1. The system *shall* declare each touchpoint's kind in the manifest `guardrails/touchpoints.json`, holding whether the person opens it and what traffic it affords. [INV-205]
2. The system *shall* afford an interruption only on a synchronous point, a teaching line only on a point the person opens, and waiting traffic on every point. [INV-205]

**Case: the gate reds a mismatch**

3. *when* a surface speaks in a kind its touchpoint lacks — an interruption from an asynchronous point, or a teaching line on a point the person did not open — the system *shall* red it. [INV-205]
4. *when* a surface interrupts through wording the marker cannot read, the system *shall* leave the declaration to the author, the same bound the cleanup-notice and muted-launch nets keep. [INV-205, INV-204, INV-157]

---

## Requirement 237: The waiting board outlives the scroll

**Context:** Chat is a display and it scrolls, so a question parked for the person and an answer the person never saw both evaporate. One small file at the host root, the waiting board, holds them, and chat renders it on occasion. An item clears on the person's acknowledgement alone and is never auto-expired, since expiring an item the person never read is a silent loss.

**User Story:** As a person who reads on my own clock, I want everything waiting for me kept in one board that never auto-expires, so that a parked question or an unseen answer is there when I open it, held safe from the scroll.

### Acceptance Criteria

**Case: the board holds what waits**

1. The system *shall* hold every item waiting for the person in the board `WAITING.md`, and *shall* clear an item on the person's acknowledgement alone. [INV-206]
2. The system *shall* never auto-expire an item, moving a superseded one to the attic with a manifest line rather than deleting it. [INV-206]

**Case: the shown cap and its demotion**

3. The system *shall* show at most 12 items to the person at once, and *when* a new item arrives to a full shown set *shall* demote the oldest shown item into the list below, whole. [INV-206]
4. *if* a thirteenth item stands in the shown set, *then* the system *shall* read it as an over-cap defect. [INV-206]

**Case: the gate reds a silent loss**

5. *when* a closing report omits a still-open board item, or an item is demoted with no matching line, or the shown set runs over cap, the system *shall* red the board gate. [INV-206]

---

## Requirement 238: A recorded decision names the exchange it came from

**Context:** Every claim in the pack stands on an artifact a reader can check. A human's word is the one input with no artifact behind it, and so the one claim no agent, prover, or gate questions — which makes it the one slot a fabrication, once placed there, is never reached again. So a sentence carrying human authority names the exchange it came from, and a claim the pack reasoned out is written in the pack's own voice, challengeable by everything that reads it.

**User Story:** As a person whose recorded decisions the pack quotes back, I want each one to name the exchange it came from while the pack's own reasoning stays in the pack's voice, so that a fabricated decision cannot hide in the one slot nothing challenges.

### Acceptance Criteria

**Case: authority names its exchange**

1. The system *shall* have a sentence set down as the person's decision name the exchange it came from, at minimum a marker a reader can go to and check in the profile's own style. [INV-207]
2. The system *shall* write a sentence the pack reasoned out for itself in the pack's own voice with no such attribution, challengeable by every agent, prover, and gate. [INV-207]
3. The system *shall* treat an autonomy grant as room to act that the agent owns as its own judgment, and *shall* never record it as a decision of the person's for the record to quote back. [INV-207]

**Case: the read-back surface and its gate**

4. The system *shall* show the person the decision-set record (`DECISIONS.md`), each entry naming its exchange, rendered so the person reads on the person's own clock and strikes what the person never said. [INV-207, INV-205]
5. *when* a live on-record entry in a decision-record surface carries no exchange, the system *shall* red the authority-anchor gate, a struck entry being skipped. [INV-207]

---

## Requirement 239: The far backlog surfaces itself rarely and unasked

**Context:** Answering when the person asks is the far tier's floor; above it, the tier shows itself on its own once in a while, so a thought parked there is met again without the person having to remember it exists. The status report carries a rare line naming that a far backlog is kept, at a cadence that is a settings-ladder default, and records the last self-surfacing so the window is readable.

**User Story:** As a person keeping a far backlog, I want it to surface itself rarely and unasked on a report I already read, so that a parked thought returns to me without waiting on my memory and without a second offer inside its window.

### Acceptance Criteria

**Case: the rare self-surfacing**

1. The system *shall* answer the far tier when the person asks, and above that floor *shall* carry a rare status-report line naming that a far backlog is kept. [INV-222, INV-223]
2. The system *shall* propose at most one such offer per 14 days as a settings-ladder default, movable by the person's word, and *shall* record the last self-surfacing in a dated marker. [INV-223, E-13]

**Case: it rides an asynchronous point**

3. *when* the far-tier line rides the status report, the system *shall* treat it as an asynchronous touchpoint that may only wait, holding the entry `far-tier-surfacing` in the manifest. [INV-223, INV-205]
4. *when* a second offer would fall inside the last surfacing's window, the system *shall* red the report-shape check, and *shall* pass a first offer once the window has passed. [INV-223]

---

## Requirement 240: A release note may offer the reader next-step choices

**Context:** A release note is a surface the person opens on the person's own clock, and on it the pack may offer appealing things to do next, phrased as free choices. The offers section is optional, so a release with no worthwhile next step owes none; what the walk owes is a recorded decision, so the offer-or-none choice is never silently skipped.

**User Story:** As a person reading a release note, I want the pack free to offer me next steps and made to record whether it did, so that a worthwhile choice reaches me while the offer-or-none decision is never silently skipped.

### Acceptance Criteria

**Case: the recorded offer-or-none decision**

1. *when* the publish walk prepares a release note, the system *shall* record the offer-or-none decision on the note, carrying the optional offers section. [INV-228]
2. *when* a release-note record neither offers a next step nor records a no-offer marker, the system *shall* red the release-note check, and *shall* pass a record that offers a choice or records none by name. [INV-228, INV-83]

**Case: it rides an asynchronous point**

3. The system *shall* treat the release note as an asynchronous, person-opened touchpoint that affords an offer and not an interruption, holding the entry `release-note` in the manifest. [INV-228, INV-205]

---

## Requirement 241: A parked question carries a recommended default

**Context:** When a question's value is the person's own input yet the work cannot wait on the person's free minute, the pack does not stall: the question is born onto the waiting board already carrying the default the work took, so the work proceeds on the recommendation and the person's free minute picks when to read it. A parked question with no default is a stalled question in a parked question's clothes.

**User Story:** As a person the pack would enjoy asking, I want a parked question born with the default the work already took, so that the work keeps moving and I answer at my own free minute rather than blocking the lane.

### Acceptance Criteria

**Case: the default travels with the question**

1. *when* the pack parks a question whose value is the person's input, the system *shall* place it on the waiting board already carrying the default the work took, and *shall* proceed on that recommendation. [INV-229, INV-4]
2. *when* a board item marked a parked question records no default, the system *shall* red the board gate, and *shall* pass a parked question naming its default. [INV-229]

**Case: an unanswered parked question keeps standing**

3. *while* a parked question stands unanswered, the system *shall* hold its default and record that the default stood unreviewed as a fact rather than an expiry. [INV-229, INV-206]
4. *when* a parked question is answered, the system *shall* route it through intake and close it, distinct from a decision an agent may not settle without the person. [INV-229, INV-152]

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
4. *when* a substantive body change carries no fresh review, the system *shall* red, the review's judgment staying the skill-creator's own. [INV-208]

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

## Requirement 245: Everything growable declares the number that bounds it

**Context:** When a thing just grows without end — a script, a spec, a test matrix — the system cannot do nothing. Where a node's fitness asks whether a file holds one thing or several, this asks whether a thing has grown past what it may weigh, where size is the signal and needs its own declared number. Each of the four large working documents declares a byte ceiling with a recorded reason, and a watcher reds a document past its ceiling.

**User Story:** As a person watching a document grow without bound, I want each growable artifact to declare a byte ceiling with a reason and a watcher to read it, so that crossing the bound earns a rotation while a silent creep upward has no door.

### Acceptance Criteria

**Case: a ceiling with a recorded reason**

1. The system *shall* have each of the four named working documents — the spec (PRODUCT_SPEC.md), the queue (ROADMAP.md), the test matrix (TEST_MATRIX.md), and the journal (JOURNAL.md) — declare a byte ceiling with a non-empty recorded reason in `guardrails/doc-bounds.json`, and *shall* red a document past its ceiling. [INV-234, INV-41]
2. *if* a declared bound carries no reason, *then* the system *shall* red it. [INV-234]

**Case: rotation is the remedy**

3. *when* a document over its ceiling carries a manifest naming an archive dated the same day, the system *shall* pass it, since the grooming that shrinks it back under the bound has just been applied. [INV-234, INV-209]
4. The system *shall* seed the ceilings above the current file sizes with rotation headroom, and *shall* let a ceiling rise only with a recorded reason. [INV-234]

**Case: the queue archives at each closing commit**

5. The system *shall*, for the queue (ROADMAP.md), take the closing commit as its archiving cadence, hold its byte ceiling as a backstop, and grow its manifest one line per monthly archive file; the spec, the test matrix, and the journal keep their byte-ceiling rotation unchanged. [INV-234, INV-276]

---

## Requirement 246: The guards over the guards

**Context:** A gate can report green two ways: because the input was clean, or because it never fires at all. Four checks guard the gate machinery itself against that hollow class — the pushed gates must be mirrored into the remote check, every chat judge must be wired into settings, every gate must carry a proof it can fail, and every path a permission rule names must still exist.

**User Story:** As a maintainer trusting the push gate, I want the gate machinery itself checked, so that no gate silently protects nothing — mirrored into the remote, wired into settings, provably able to fail, and pointed at real paths.

### Acceptance Criteria

**Case: the remote mirror carries every local gate**

1. *when* the push gate runs a gate letter locally that the remote mirror does not run, the system *shall* red, naming the gate and the one fix, a legitimate remote-skip living in `guardrails/ci-mirror.json` with its reason. [INV-210, M-5]
2. *if* a carve-out names a letter that is no local gate, *then* the system *shall* red it as drift. [INV-210]

**Case: every chat judge is wired**

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

## Requirement 257: A delivery that closes a roadmap row refreshes the forward map

**Context:** The movement-end report law asks the seat to refresh the forward map and report after every big movement without being asked; left as once-read prose it fired only on a reminder. Its checkable face is a commit: a delivery is a commit that moves a roadmap row from the queue's body to the archive with its status naming *landed* and its date, and such a commit that does not also touch the forward map reds. A commit that closes no row is not a delivery and owes nothing.

**User Story:** As a person relying on an up-to-date forward map, I want a delivery commit made to refresh the forward map in the same breath, so that a movement that ends never leaves the map stale.

### Acceptance Criteria

**Case: a delivery commit refreshes the map**

1. *when* a commit's diff moves a roadmap row from the body to the archive with its status naming *landed*, the system *shall* require the same commit to touch `NEXT_STEPS.md`. [INV-242, INV-276]
   - the commit range is read through the same base ladder the other range checks use: the declared base, then `origin/main`, then the previous commit.
2. *if* such a delivery commit does not touch the forward map, *then* the system *shall* red and name the one fix. [INV-242]

**Case: what is not a delivery owes nothing**

3. The system *shall* leave a commit that closes no row, and a row closed to *declined*, *deferred*, or *superseded*, owing no refresh. [INV-242]
4. *when* the push-gate letters are exhausted, the system *shall* ride this check on the suite, so a red here reds the suite gate and blocks the push. [INV-242, INV-222]

**Case: a missed landing heals forward**

5. *when* a landing commit misses the refresh, the system *shall* let a later commit in the same range heal it. The healer *shall* touch `NEXT_STEPS.md` and name the missed landing by its commit id. A heal predating its landing heals nothing, and the system *shall* warn rather than red once healed, keeping the miss on record. [INV-242]

## Requirement 258: Every stateful surface is reviewed against a floor of composition axes

**Context:** Some parts of a host project hold state — a screen, a panel, a saved file the user can change and find again later. Each is a stateful surface. Every stateful surface is reviewed against a set of composition axes, each axis one question about the surface's behaviour. A floor of axes holds for every stateful surface whatever its project's kind. The axis a reviewer skips most is the last one, the presence of every other live surface: a caption still naming the previous photo once the closing screen arrives is the classic stranding hole, because the caption's behaviour with the finale in view was never written as a sentence.

**User Story:** As a person composing a surface, I want a fixed floor of axes every stateful surface answers and one stated shape for the whole axis set, so that no kind-independent angle of its behaviour is left unreviewed and a reader knows when the surface's spec is complete.

### Acceptance Criteria

**Case: the kind-independent floor**

1. The system *shall* review every stateful surface against the floor axes: its behaviour in each view, in each mode, at each user tier, at each viewport size, when it is closed and reopened, and under two writers that can act on it at once. [C-1]
2. The system *shall* include in the floor the surface's behaviour alongside every other surface that can be present at the same time — a sibling sharing the screen, or a surface the flow reaches one step before or after it — whether or not that other surface holds state. [C-1]

**Case: the seam beside each other live surface**

3. The system *shall* state, for each other live surface present with this one, what this surface does while that one is present — whether it holds, clears, or hands off. [C-1, INV-72]

**Case: the axis set declares its own shape**

4. The system *shall* read the axis set as a hybrid whose shape it declares: the floor is an enumerated set every stateful surface answers, and the kind-owed tail is an open set whose members a kind names one at a time. [C-1, INV-226]
5. The system *shall* read a surface's spec as complete only once every floor axis and every axis its kind owes has an answer. [C-1, INV-244]

---

## Requirement 259: The prover hunts the situation the author never wrote

**Context:** The prover reads the whole axis list actively and derives each surface's reachable situations for itself, rather than trusting the author to have filled every one. A reachable situation the spec leaves blank is the exact hole a running product still reaches, and the prover reports it and leaves the sentence to the author.

**User Story:** As a person relying on a spec to cover what the product reaches, I want the prover to derive each surface's reachable situations and flag every blank one, so that a state the product can reach but the spec never wrote is caught before a user meets it.

### Acceptance Criteria

**Case: derive the reachable situations**

1. *when* the prover reads a stateful surface, the system *shall* walk every axis. [INV-72, C-1]
   - the axes are the views, modes, and tiers;
   - the viewport shapes and reopens it passes through while already shown;
   - every other surface that can be present at the same time, siblings on its screen and the surfaces one step before and after it in the flow.
2. *when* the prover reaches one situation, the system *shall* ask whether this surface's behaviour is stated there, and *shall* report a reachable situation with a blank answer as a finding of the same class as a fact no node owns. [INV-72, E-14]

**Case: the hunt rides both passes and leaves the sentence to the author**

3. The system *shall* run the hunt on both the whole-spec pass and the surface-add pass. [INV-72, M-6]
4. *when* the hunt reports a missing situation, the system *shall* leave the sentence to the author, who writes it as a composition invariant, decided or marked a default the way the standard-facet sweep marks its own, and *shall* invent no answer and ask the human for nothing. [INV-72, INV-18, INV-31]

---

## Requirement 260: A cross-surface policy is stated once at the class level

**Context:** When a decision governs a kind that recurs across sibling surfaces or elements — a gesture policy, an affordance, an input-to-action mapping, a repeated state transition, or a feature and its element shared across places — the spec states it once at the surface-class level, naming the class and enumerating the surfaces it governs. Consistency of this kind is itself an invariant. This is the preventive twin of the class hunt: the class hunt sweeps siblings once a bug is confirmed, and this holds the policy uniform before a bug is filed.

**User Story:** As a person keeping behaviour uniform across similar surfaces, I want a policy for a recurring kind stated once at the class level and checked across its siblings, so that a rule written for one surface while its siblings stand cannot ship non-uniform.

### Acceptance Criteria

**Case: the policy is homed on the class**

1. *when* a decision governs a kind that recurs across sibling surfaces or elements, the system *shall* state it once at the surface-class level, naming the class and enumerating the surfaces it governs. [INV-125]
2. The system *shall* read a policy written for one surface while siblings of the same kind exist as a spec defect. [INV-125, INV-124]

**Case: the prover and the guardrail hold it**

3. *when* the prover reads an interaction policy, the system *shall* enumerate the surfaces of that kind from the surface registry and flag any the clause does not cover, the same finding class as a reachable situation with a blank answer. [INV-125, E-10, INV-72]
4. *when* a product renders a page, the system *shall* assert a policy declared for one surface root across every registered sibling root and hold it red until all are covered, so the non-uniformity reds the day the single-surface fix lands. [INV-125, INV-97]
5. The system *shall* keep the spec-class rule as the root and leave the page-wide assertion to the products the pack serves, the pack shipping the rule and the prover lens as the ship-the-shape pole of the pack-to-host split. [INV-125, INV-163]

**Case: the same defect stated in prose**

6. *when* a sentence states a principle for a whole kind while it is homed on one surface and siblings of that kind exist, the system *shall* read it as the same defect in prose form, and *shall* demand the author lift the principle to a class clause naming the class and its members, or scope it to the one member by a decided sentence. [INV-125]

---

## Requirement 261: Both directions of a paired state change get the same craft

**Context:** When a surface has a pair of opposite state changes — open and close, enter and exit, expand and collapse, show and hide — a transition crafted for one direction is a decision about the pair, so the other direction is stated too. The default is symmetry: the exit mirrors the enter's feel unless a reason is written. A shorter exit or a deliberately instant one is a valid, stated, decided answer. Motion feel is the human's own gate, so where the author cannot judge the pair the question is surfaced to him.

**User Story:** As a person crafting a paired transition, I want the opposite direction stated whenever one direction is crafted, so that a crafted-in and instant-out pair cannot ship silently and a reader tells a decided asymmetry from an overlooked one.

### Acceptance Criteria

**Case: the continuity of the transition**

1. *when* a surface has a pair of opposite state changes and one direction's transition is crafted, the system *shall* state the other direction too, defaulting to symmetry unless a written reason parts them. [INV-126]
2. The system *shall* have the author write the pair's answer as a spec sentence — mirror, a named shorter exit, or deliberately instant — decided or marked a default on the standard-facet sweep. [INV-126, INV-18, INV-31]
3. *if* the author cannot judge the pair's feel, *then* the system *shall* surface the question to the human rather than ship a crafted-in and instant-out pair. [INV-126, INV-30]
4. *when* the prover reads a paired state change with one direction described and the opposite unstated, the system *shall* report it as a finding of the same blank-answer class as an unwritten situation. [INV-126, INV-72]

**Case: the reversibility of the means**

5. *when* a surface is opened by a continuous, reversible gesture — a pinch, a drag, a lift — the system *shall* have that same gesture reversed stand among its ways to close, or a decided sentence state why it is absent. [INV-126, INV-30]
6. *when* an opening gesture has a natural inverse, the surface offers no way to close by that inverse, and no deciding sentence stands, the system *shall* block it as a finding of the same blank-answer class. [INV-126, INV-72]

**Case: the magnitude of a reversible quantity**

7. *when* the paired open and close ride a continuous, reversible quantity, the system *shall* state whether the inverse asks the same magnitude as the forward move, symmetric or a named deliberate asymmetry. [INV-126, INV-31, INV-72]
   - the continuous, reversible quantity may be a pinch span, a drag distance, or a wheel accumulation;
   - the answer is decided or marked a default;
   - the system *shall* report a stated pair whose magnitude sentence is missing as the same blank-answer finding.

---

## Requirement 262: Each scenario states how it is entered and how it exits

**Context:** A person-facing scenario is a flow, and a flow has edges: it is entered from somewhere with something already true, and it exits to somewhere leaving something behind. The scenario states both, so a reader can check it against a known before and after. This lifts the per-operation precondition and postcondition lenses to the scenario level.

**User Story:** As a person reading a scenario, I want its entry and its exit stated, so that the prior state it assumes and the postcondition the next scenario inherits are both stated on the page for the reader.

### Acceptance Criteria

**Case: the scenario states both edges**

1. The system *shall* have each person-facing scenario state its entry — where the walk arrives from and what must already hold — and its exit — where the person lands and what it leaves true for the next scenario to inherit. [INV-127]
2. The system *shall* read this as the scenario-level lift of the per-operation precondition and postcondition lenses, kin of the entry-symmetry lens and the runtime view's flow walks. [INV-127, INV-50, INV-74]

**Case: the prover holds it, binding forward**

3. *when* the prover reads a flow whose entry or exit is unstated, the system *shall* report it as a finding of the same blank-answer class. [INV-127, INV-72]
4. The system *shall* have a new scenario state its edges from the first draft and *shall* flag an existing scenario's unstated edge as a finding rather than block the lane. [INV-127, INV-159]

**Case: a trivially-none edge is still stated**

5. *when* a scenario's entry or exit is trivially none — a top-level scenario entered from nowhere, a terminal scenario exiting to nowhere — the system *shall* state it as such in one short clause, so a reader tells a decided edge from an overlooked one. [INV-127]

---

## Requirement 263: A gated behaviour names both ends of its range, and a scoped guarantee answers for its whole domain

**Context:** When a transition is gated on a quantity that runs on a line — elapsed time, a count, a distance, a size — the spec states its behaviour at both ends of the live range: below the low end and above the high end. When a slot on screen is filled by asynchronously produced content, the spec names the three faces of the wait — pending, arrived, and failed — and a visible pending face stands wherever the slot holds a reserved place. A guarantee that holds over one named part of its domain owes the same completeness across the whole domain, the viewport its worked instance.

**User Story:** As a person crossing an unnamed edge — reloading before the lower bound, returning after the upper, landing on a viewport band a guarantee never named — I want every range end, wait face, and domain part decided, so that no edge of a range or a partial guarantee renders as a blank the spec never wrote.

### Acceptance Criteria

**Case: both ends of a gated range**

1. *when* a transition is gated on a quantity that runs on a line, the system *shall* state its behaviour below the low end and above the high end, each end standing as its own decided or default sentence, and *shall* read a phrase that names one point and leaves an unbounded interval silent as incomplete until that interval is bounded on both sides. [INV-138]

**Case: the three faces of an async slot**

2. *when* a slot on screen is filled by asynchronously produced content, the system *shall* name the pending, arrived, and failed faces of the wait and stand a visible pending face wherever the slot holds a reserved place. [INV-138]
3. The system *shall* read the pending face as that slot's loading state, sharpening the standard facets' empty, error, and loading states for a reserved slot. [INV-138, INV-18]
4. *when* the prover reads a gated range or an async slot with an out-of-range or in-between state left unspecified, the system *shall* report it as the same class as an unwritten situation. [INV-138, INV-72, INV-31, INV-30]
   - the timing is surfaced to the human, since only he can judge it.

**Case: a scoped guarantee owes its whole domain**

5. *when* a guarantee holds over one named domain part, the system *shall* draw the standing question about the remainder and give each remaining part its own decided or default sentence until the domain is covered. [INV-138]
   - a named domain part is a band of a ranged quantity, a user state, a network condition, or a locale.
6. The system *shall* read a guarantee that speaks for one part while the remainder stays silent as the same unwritten-situation class. [INV-138, INV-72]

**Case: the viewport is the worked instance**

7. The system *shall* have every layout guarantee name its viewport quantifier — holding on every viewport or naming the band it is scoped to — and *shall* leave the other bands silent until each is stated, the short-viewport band among them. [INV-138, T-13]
8. *when* the parts are a same-kind group no clause has yet declared, the system *shall* reach them through the design review's group pass and hold them in the prover once a part-uniform guarantee is declared. [INV-138, INV-141, INV-150]
9. The system *shall* read this as the range-and-lifecycle member of the composition-lens family, its member set open-ended, naming the viewport as its worked instance and leaving the remainder to the general duty. [INV-138, INV-125, INV-126, INV-136, INV-226]

---

## Requirement 264: A general law over concrete instances declares whether it enumerates them or lets them ride

**Context:** A law that states one general duty a set of concrete instances falls under makes one choice about those instances: the clause names every member, or an instance rides the general duty with no name. The member set keys the choice. A closed set names every member; an open-ended set names only its worked instances and leaves the remainder to the general duty. A law that reaches this choice by feel is the defect this rule keys.

**User Story:** As a person writing a general law over instances, I want the member set to decide whether the law enumerates or lets instances ride, so that a closed set names every member while an open-ended set names only what a real incident earned.

### Acceptance Criteria

**Case: the member set keys the choice**

1. *when* a law states a general duty a set of concrete instances falls under, the system *shall* make one choice: name every member in the clause, or let an instance ride the general duty with no name. [INV-226]
2. *when* the member set is closed and enumerable — finite and nameable, even one that grows a member at a time by a named incident — the system *shall* name every member in the clause, as the per-kind quality budgets name each project kind and the standard-facet list names each facet. [INV-226, INV-18, INV-41]
3. *when* the member set is open-ended — any sub-case of a domain, unlistable in advance — the system *shall* name only its worked instances, each earned by a real incident, and leave the remainder to the general duty carried by the rule with no list, as the scoped-guarantee law names the viewport alone. [INV-226, INV-18, INV-138]

**Case: reaching the choice by feel is the defect**

4. The system *shall* read a general law reaching enumerate-or-ride by feel as the defect this rule keys, the member set deciding, and *shall* have a law whose set is genuinely borderline state which side it took and why. [INV-226]
5. The system *shall* read this as the declaration member of the composition-lens family, and *shall* place its enforcement with the author who writes the law. The prover *shall* run no sweep of its own for it, since only the author knows whether a member set is closed. The prover *shall* catch the sibling-surface case in its cross-surface uniformity sweep. [INV-226, INV-125, INV-126, INV-136, INV-138]

---

## Requirement 265: A surface's composition axes are the set its project's kind owes

**Context:** The floor axes are the kind-independent set every stateful surface answers, and a project's kind settles which further axes a surface owes beyond it. A kind carries a standard set of composition axes the way it already carries a node-structure scaffold and a set of design principles, so the author of a surface reads its axes from the kind before composing. An axis exists because the kind renders under it, and that existence stands apart from what today's code happens to cover; the gap between an owed axis and the code's coverage is the finding.

**User Story:** As a person composing a visitor-facing surface, I want its axes read from the project's kind and every owed axis covered against each of its values, so that an axis the kind owes cannot sit uncovered until a visitor falls through it.

### Acceptance Criteria

**Case: the axis set is read from the kind**

1. The system *shall* have the author read a surface's axes from the project's kind before composing, the kind carrying its axis set the way it carries a node-structure scaffold and a set of design principles. [INV-244, INV-36, INV-135, INV-136]
2. *when* a project's kind is visual, the system *shall* owe every visitor-facing surface an open axis set whose first named member is the input-capability axis, beyond the viewport axis the floor already carries. [INV-244, INV-36, INV-136, C-1]
   - a visual kind renders a visitor-facing surface and declares a design-principles set; the `static site` and `fullstack` kinds are visual kinds.
3. The system *shall* have the sibling axes on that surface — browser engine, locale and text direction, connection reach, first-versus-returning visit, accessibility, and measurement reach — ride the per-kind duty and enter as their own increments, so the visual kind's owed set stays open. [INV-244, INV-226]

**Case: the axis set is a founding declaration**

4. The system *shall* have every project kind name the composition axes it owes beyond the floor as a founding declaration, the way it declares its concrete layers and proof kinds. [INV-244, INV-135]
5. *when* a kind owes no axis beyond the floor, the system *shall* accept the empty set only as an explicit stated decision, the case the per-kind design-principles set already legitimises for a kind with no visual surface. [INV-244, INV-136]
6. *when* a kind is recorded with no axis-set declaration at all, the system *shall* flag it the way a kind recorded with no layers or proofs is flagged. [INV-244, INV-135, A-10]
7. The system *shall* have a non-visual backend kind owe its own non-empty axis set — load, version, and tenant — so an axis set that stays empty for a non-visual kind is a defect the flag-if-absent check stops. [INV-244, INV-135]

**Case: the gap between owed and covered is the finding**

8. The system *shall* read the two layers at each surface, and *shall* report an owed axis whose value the code leaves uncovered as a finding of the same blank-answer class. [INV-244, INV-72]
   - the two layers are the axes the kind owes and the values the shipped code covers;
   - that blank-answer class also covers a reachable situation the spec never wrote.
9. *when* the gap is found, the system *shall* have the author state it as a spec sentence, decided or marked a default. [INV-244, INV-18, INV-31]
10. The system *shall* read an owed axis as covered only once the author composes and tests the surface against each elementary value of the axis, the write-the-sentence half and the cover-the-values half splitting one dimension by time. [INV-244, C-1, INV-18]

**Case: an axis carries its own value space**

11. The system *shall* read an axis's value space as a domain the same completeness reaches, and *shall* model the input-capability values as combinable capabilities a surface answers for in combination, since touch, a fine pointer, hover, and a keyboard co-occur on one machine. [INV-244, INV-138, INV-226]
12. The system *shall* owe and answer the two elementary poles — touch and a fine pointer — up front, and *shall* carry the co-occurrence answer, hover present alongside touch, in with the later step that forces the author to answer for the in-between. [INV-244]
    [GAP: the source answers the two elementary poles up front but defers the co-occurrence value — one device carrying touch and hover at once — to a later forcing step, naming no interim answer or default; a surface's behaviour when both are present is unstated today, so a test author cannot pin the tablet-with-hover-and-touch case.]
13. The system *shall* leave the refinement values past the elementary poles — a stylus, a keyboard-only reach, a device an advanced user registers — to the human's taste, entering later, decided or marked a default when they do. [INV-244, INV-30, INV-31]

**Case: the rule binds forward**

14. The system *shall* have a surface authored after this rule read its axis set from the kind from the first draft, and a surface that predates it carry the read at the first landing that touches it, staying uncovered on the axis until that landing arrives. [INV-244, INV-159]

**Case: the value-space machinery is promised**

15. The system *shall* keep the value-space in-between forcing step and the recursive axis-registry similarity sweep promised as later increments. [INV-244]
    [target]

---

## Requirement 266: A declared axis that adds runtime code names whether its artifact divides or ships whole

**Context:** The composition law reads whether a surface's behaviour divides along a cross-cutting axis its kind owes. Its dual reads whether the artifact the visitor receives divides along that same axis or arrives as one piece. When a spec declares such an axis and covering it adds runtime code, the design owes one of two decided sentences; an axis that adds runtime code and carries neither is the finding, shipping as one artifact because the choice went unexamined.

**User Story:** As a person reviewing an artifact's delivery, I want each declared axis that adds runtime code to state whether the artifact divides along it or ships whole for a named reason, so that a monolith nobody examined is caught while a monolith with a stated reason stands.

### Acceptance Criteria

**Case: the dual of the composition law**

1. The system *shall* read whether the delivered artifact divides along a declared axis its kind owes or arrives as one piece, the dual of the composition law that reads whether behaviour divides along that axis. [INV-248, INV-244]
2. *when* a spec declares such an axis and covering it adds runtime code, the system *shall* carry one of two decided sentences. [INV-248]

**Case: the two settled answers and the finding**

3. The system *shall* accept a monolith named for a stated architectural reason as a settled answer. [INV-248]
   - the reason may be one bundle behind one page that is never torn down;
   - a delivery that runs on no server;
   - a payload the design judges too small to make a split worth its cost;
   - the design judges whether the named reason holds.
   [GAP: the source names the design as the judge of a "too small to make a split worth its cost" payload but states no measure — the payload size below which a split costs more than it saves — so a maintainer cannot pin the boundary between a settled small-payload monolith and an unexamined one; the source leaves it to the design as a senior read, not a gate.]
4. The system *shall* accept an axis that names the delivery road it owes — a platform split, a lazy load, a per-value chunk — carried by its own later row. [INV-248, INV-159]
5. The system *shall* read the finding as the third case: an axis that adds runtime code and carries neither sentence, shipping as one artifact because the choice went unexamined, its byte weight the downstream symptom of the unasked separability question. [INV-248]

**Case: the lens's reach and its standing**

6. The system *shall* reach this lens past the input-capability axis to any declared axis a kind owes. [INV-248]
   - reached only where covering it ships runtime code;
   - it may be an assistant capability present or absent, a rendering engine, or the viewport;
   - a viewport answered by a media query, or a locale answered by a logical property, draws no delivery question.
7. The system *shall* keep this a senior read the prover carries and not a gate, since a monolith is lawful whenever its reason is named and only the design can say whether that reason holds. [INV-248, INV-244, INV-214]
8. The system *shall* carry a prover discovery habit stated in its skill: for a lens the prover applies, it may ask whether that lens's dual applies to the document here. The system *shall* read this as a prompt that surfaces a missing lens, and not as a rule that every lens ship paired, since one dual folds into a lens already run while another is nameable yet seldom applies. [INV-248]
9. The system *shall* read this as the delivery-separability member of the composition-lens family, binding forward. [INV-248, INV-125, INV-126, INV-136, INV-138, INV-226, INV-159]
   - the forward terms match the axis-set rule's: from the first draft for a new surface, at the first touching landing for an older one.

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

## Requirement 280: A document's bytes-per-criterion may only fall

**Context:** The spec grows one delivery at a time, and prose can bloat while the rule count holds. To hold the density, the spec document records a bytes-per-criterion bound — its size ratchet — and the ratchet gate holds that bound. A delivery may push the bound down or leave it, and may not push it up; raising the bound is itself a change to this requirement and takes the same route through the pipeline. The ratchet governs the spec document alone, and the other documents keep their flat byte bound.

**User Story:** As a person who owns the spec's readability over time, I want the spec document's bytes-per-criterion bound to move only down, so that no single delivery is free to bloat the prose.

### Acceptance Criteria

**Case: the recorded bound**

1. The spec document `PRODUCT_SPEC.md` *shall* record a bytes-per-criterion bound, measured as the byte count of its criterion lines alone — glossary and preamble bytes excluded — divided by the count of criteria in its body. [INV-264]
2. The recorded bound *shall* live in the file `guardrails/spec-ratchet.json`. [INV-264]
3. The initial bound *shall* be the value measured at the migration-end freeze, recorded by the freeze actor. [INV-264]
4. The ratchet *shall* govern `PRODUCT_SPEC.md` only; `ROADMAP.md`, `TEST_MATRIX.md`, and `JOURNAL.md` *shall* keep their flat document byte bound. [INV-264]

**Case: the ratchet moves only down**

5. *when* a delivery freezes the spec document, the system *shall* compute the new bytes-per-criterion and *shall* require it to be at or below the recorded bound. [INV-264]
6. *if* a delivery's new bytes-per-criterion is above the recorded bound, *then* the ratchet gate *shall* red. [INV-264]
7. *when* a delivery's new bytes-per-criterion is below the recorded bound, the system *shall* lower the recorded bound to the new value. [INV-264]

**Case: raising the bound is a spec change**

8. The system *shall* raise the recorded bytes-per-criterion bound only through a change to this requirement, run through this same pipeline; no delivery *shall* raise the bound on its own. [INV-265]

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

**Context:** ROADMAP.md is the format family's third member, joining after the spec and the matrix. The page `docs/roadmap-format.md` defines the member — the inherited laws and the queue-particular additions — and this requirement binds that definition, putting the queue's shape under the gates that hold the family.

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

## Requirement 293: A naked internal code in live prose reds

**Context:** The plain-language law asks a human-facing sentence to stand in the product's own words, with an internal handle — a queue row number, a spec code — trailing in parentheses for a reader who wants to follow it. A sentence that leads with a bare handle gives the reader a number he has no way to resolve. The law had no machine and decayed for want of one, so a Stop-hook scan now reads the turn against it and asks for the naming in plain words one message later.

**User Story:** As a person reading the seat's replies, I want an internal code left standing outside its anchor flagged, so that the sentence comes back in plain words I can resolve on sight.

### Acceptance Criteria

**Case: a code outside its anchor reds**

1. *when* any message the seat showed since the last human turn carries an internal code — a queue row named by its number in either working language, or a bracket code the documents use — standing outside a trailing anchor, the system *shall* block the stop and ask for the naming in plain words one message later. [INV-283, INV-28]
2. The system *shall* pass a code sitting inside parentheses or square brackets, the lawful trailing anchor the plain-language law names. [INV-283, INV-28]

**Case: a code the sentence talks about**

3. The system *shall* pass a code inside a fenced block, an inline backtick span, or a quoted span, and *shall* pass a table row, whose neighbouring cell carries the plain words. [INV-283]
4. The system *shall* read a naming word and the number it carries, so a bare number with no naming word before it passes. [INV-283]

**Case: honest about its reach**

5. The system *shall* judge only whether a code was left standing outside an anchor, and *shall* leave whether the plain words that replace it are the right words to the person. [INV-283]

**Case: the code forms the scan reads**

6. The system *shall* read a document's own name run against a number as a code standing outside its anchor, a form handing the reader a location he can resolve only by opening the document. [INV-283]
7. The system *shall* read a multi-letter code spoken with a space as the equal of its dash form, and *shall* hold the multi-letter form and the single-letter dash form to the capital shape the documents write them in. [INV-283]
   - an ordinary word carrying a letter and a number in lower case passes.
8. The system *shall* pass a naming word and its number *where* the same line carries a file name or a file word, the shape a reference to a line inside a source file takes. [INV-283]

---

## Requirement 294: Empty validation aimed at the person reds

**Context:** A line telling the person he is right, praising his question or his intuition, or framing the seat's own work as superior costs the reader attention and returns nothing: the reply owes the finding or the act, and nothing else leads before them. The rule stood as a personal setting with a machine behind it on one host alone. The pack ships that machine as a Stop-hook scan in the two-tier shape the scissors scan carries, a universal list plus a host's own overlay.

**User Story:** As a person reading the seat's replies, I want an empty validation line caught, so that a reply opens with the finding and never with praise for the person who asked.

### Acceptance Criteria

**Case: the validation gate**

1. *when* any message the seat showed since the last human turn carries an empty-validation phrase, the system *shall* block the stop in the after-the-fact shape the scissors scan and the hedge gate take. [INV-284, INV-238]
   - the scan strips a quoted, backticked, or fenced span from the message before it matches the pattern list.
2. The system *shall* match against an inline universal pattern list plus an optional personal-overlay file a host tunes, as the scissors scan carries one, and *shall* stand on the universal list alone *where* the overlay is absent or unreadable. [INV-284, INV-203]
3. The system *shall* catch only the phrases it lists, so a paraphrase it does not carry stays with the register judge that reads the class in meaning. [INV-284, INV-203]

**Case: shipped as a pack hook**

4. The system *shall* install the scan by the setup walk beside the scissors scan, *shall* have it covered by the config-health check and classified in the wired-hook declaration, and *shall* have its runs and fires read by the net-liveness meter. [INV-284, INV-173, INV-175, INV-211, INV-202]


---

## Requirement 295: A chat law is judged while the turn still runs

**Context:** The chat laws are judged when the turn stops, and a narration line written between tool calls reaches the person long before that moment. The check meant for such a line then speaks into a turn already read, which is how bare row numbers and a loan-translated word reach the person under a scan that catches that exact sentence. The earliest boundary after a narration line is the moment before the next tool call, so the same laws are read there and the correction lands inside the turn that broke them.

**User Story:** As a person reading the seat's lines while it works, I want a broken chat law caught at the next tool call, so that the correction reaches me inside the same turn.

### Acceptance Criteria

**Case: judged at the tool boundary**

1. *when* a message shown since the last human turn carries an internal code standing outside its anchor or a listed loan translation, the system *shall* deny the next tool call and name each fragment with the plain words it owes. [INV-285, INV-28]
2. The system *shall* judge the code half through the code-anchor scan itself, so one law is read at both boundaries. [INV-285, INV-283]

**Case: the loan-translation list**

3. The system *shall* read the loan translations from a list holding a plain replacement for each, and *shall* name that replacement in what it reports. [INV-285, INV-28]
4. *where* a listed word is ordinary language on its own, the list *shall* carry the surrounding sense that makes it a loan translation. [INV-285]
5. The system *shall* pass a loan translation inside a fenced, backticked, or quoted span, which is a sentence about the word. [INV-285]

**Case: a fragment is reported once**

6. The system *shall* record what it reported for the session and *shall* stay silent on a fragment already reported. [INV-285]

**Case: the check never stops the work**

7. The system *shall* stand down on any failure of its own, leaving the session's tool calls running. [INV-285]

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

## Requirement 297: A criterion is written so a stranger reads it once

**Context:** The spec's readability lives in its acceptance criteria. A survey of every requirement body found five habits that lose a first-time reader. The whole rule arrives welded into one sentence, a term is defined inside the criterion that uses it, a closing clause carries no verb, the anchor competes with the prose, and the criterion's line and its bullets together carry several rules while each piece reads short. A gate holds each habit at the count measured the day it landed, so the document may improve and may not slide.

**User Story:** As a person meeting the spec for the first time, I want each criterion to carry one rule in one plain sentence, so that I read the document without an author beside me.

### Acceptance Criteria

**Case: the five reading defects**

1. A criterion *shall* state one trigger and one duty within the recorded word cap. [INV-287]
2. A criterion *shall* use a term the glossary already defines. [INV-287]
3. A criterion *shall* carry no definition of a term inside itself. [INV-287]
4. A criterion *shall* close on a clause carrying its own subject and finite verb. [INV-287]
5. A criterion's code anchor *shall* sit at the line's end and *shall* carry no more codes than the recorded cap. [INV-287]
6. A criterion's line and its bullets together *shall* state one rule within the recorded total cap. [INV-287]

**Case: the gate that holds them**

7. The check `guardrails/check-criterion-readability.py` *shall* read the acceptance criteria of the document named on its command line through one readability arm per defect. [INV-287]
8. The readability arms *shall* read a criterion as its line together with the bullets under it, and *shall* read each bullet as a sentence of its own. [INV-287]
9. Each readability arm *shall* take its threshold from the one config file `guardrails/criterion-readability.json`. [INV-287]
10. *when* a readability arm reports a criterion, the check *shall* name the file, the requirement code, the line, the offending text, and what to write instead. [INV-287]
11. Each run *shall* state its reach: the two files it opens, and the parts of the document the readability arms read. [INV-269]
12. The readability arms *shall* leave to the cold-reader panel the closing appositive that drops its participle, the aside that enumerates members, and the judgment of which code span a sentence says better in words. [INV-287]

**Case: the counts move only down**

13. The config *shall* hold one recorded count per readability arm. [INV-288]
14. *if* a readability arm's measured count stands above its recorded count, *then* the check *shall* red and *shall* name that arm. [INV-288]
15. *when* a readability arm's measured count falls below its recorded count, the check *shall* report the fall. [INV-288]
16. *when* the check runs with `--rebaseline` and no readability arm stands above its recorded count, the check *shall* write each measured count back to the config. [INV-288]
17. No run *shall* raise a recorded count. [INV-288]
18. A raised recorded count *shall* be a hand edit to the config stating its reason, run through this same pipeline. [INV-288]

---

## Requirement 298: The setup walk installs every session hook the pack declares

**Context:** `guardrails/judge-hooks.json` declares ten wired session hooks, each with the event it rides. `scripts/install-session-hooks.sh` is the one command a human runs, since the harness classifier blocks an agent's own hand in its configuration. Before this requirement it installed two of the ten; the other eight reached a real machine only by hand, so a fresh machine, and any host adopting the pack, got a fifth of the conduct machinery with no sign the rest was missing. The fix generates the installer's own coverage from the declaration and chains to the existing installer that already covered the other eight, so the one command reaches all ten with their data files.

**User Story:** As a person adopting the pack on a fresh machine, I want the one installer command to wire every session hook the declaration names, so that I get the whole conduct machinery.

### Acceptance Criteria

**Case: generated coverage**

1. *when* the human runs the installer, the system *shall* install and wire every hook named in `guardrails/judge-hooks.json`'s wired declaration, and each hook stands under its declared event with its declared command form. [INV-289]
2. The system *shall* install every data file a wired hook's declaration names, beside that hook. [INV-289]

**Case: both directions proven mechanically**

3. *if* a declared wired hook is missing after a fresh install, *then* a check *shall* fail naming it. [INV-289]
4. *if* the installer places a file the declaration names nowhere, *then* the same check *shall* fail naming it. [INV-289]

**Case: idempotence and personal overlays**

5. *when* the installer runs a second time, the system *shall* change nothing already wired or already installed, recognizing a hook already wired under any command form. [INV-289]
6. The system *shall* never create, edit, or overwrite a personal overlay file, and *shall* name each one it finds already present. [INV-289]


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

**Context:** A worker writes the files its brief names, and the pack's own red-first method has it mutate a shipped artifact to prove a row red. A git command that discards uncommitted work is a different act: its blast radius is a path, so it lands on files the worker never wrote and its brief never named, and the `git status` a careful worker pastes afterwards reads clean in the safe case and the destructive one alike. So a worker holds the bytes it is about to overwrite and puts them back itself, and a worker holding none halts for the orchestrator. The orchestrator owns recovery, and the last committed stage is what a repair reads from.

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
11. A raised recorded count *shall* be a hand edit to the record, made under the rule stated once at the criterion-readability requirement. [INV-301, INV-288]
   - the reason sits in the entry's `reason` field, the shape `guardrails/doc-bounds.json` carries;
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


## Requirement 304: A skill's public mirror carries the edition written for a stranger

**Context:** A skill's copy under `skills/` is written for a session that has already loaded this pack. It cites internal codes and points at scripts that travel with the pack. The sync script rebuilds each standalone mirror from the pack and pushes it to a public repository. A stranger reading that mirror needs the method in words that stand on their own.

**User Story:** As a stranger reading a mirror, I want it to carry a public edition, so that every rule stands in plain words.

### Acceptance Criteria

**Case: a skill ships a public edition**

1. A skill *shall* be able to ship a public edition under `editions/<skill>/`. [INV-303]
   - the edition states the same method, with every internal code resolved into the rule it stands for;
   - the edition carries whatever the method points at, so a reader needs no file from this pack.
2. *where* an edition exists, the sync script *shall* rebuild that skill's standalone mirror from it. [INV-303, INV-96]
3. *while* an edition stands, `skills/<skill>/` *shall* stay the copy a session in this project loads. [INV-303]
4. *when* the sync publishes an edition, it *shall* print that skill's name and the directory it published. [INV-303, INV-269]

**Case: a skill ships no edition**

5. *where* `editions/<skill>/` is absent, the sync script *shall* rebuild that mirror from `skills/<skill>/`. [INV-303, INV-96]
6. The pack *shall* stay the one source of both copies, so a hand edit on a mirror is overwritten. [INV-303, INV-96]

**Case: a half-made edition is refused**

7. *if* `editions/<skill>/` holds no `SKILL.md`, *then* the sync script *shall* refuse that skill by name. [INV-303]
   - the copy step deletes what it replaces, so publishing an empty edition leaves the mirror shipping nothing;
   - the refusal names the missing file and the two ways out, adding the file or removing the directory.
8. *when* a skill is refused, the sync *shall* publish no source for it and *shall* leave its mirror as it stands. [INV-303]
9. *when* a skill is refused, the sync *shall* run on to the remaining mirrors and *shall* record the skip in its summary. [INV-303]
10. The publish source of one skill *shall* be readable on its own, through a flag that reaches no repository. [INV-303]

---

## Requirement 305: A push carries an adversarial review of the change it sends — merged into Requirement 141

**Context:** This requirement and the push gate's own re-check asked one push for two review records, written into two homes and read by two checks, over one and the same change. Both are one adversarial pass over one delta, so they are now one record: Requirement 141 carries the whole duty, and the record lives with every other review record under `docs/prover/`. The merge is recorded in DECISIONS.md. The adversarial read itself is untouched — only the second record and the second check are gone.

**User Story:** As a maintainer preparing a push, I want one review record instead of two, so that the read survives at half the writing.

### Acceptance Criteria

**Case: merged**

1. The system *shall* carry this requirement's duty in Requirement 141 alone, the check that once held it resting at `attic/check-push-review.sh`. [INV-304]
   - putting that check back into the push chain takes a decision of its own.

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

15. The system *shall* run as gate ad on `guardrails/pre-push`, *shall* carry its step in the CI workflow, and *shall* carry a red-first proof. [INV-305, INV-210, INV-212]

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

## Requirement 309: The work board shows the whole queue in columns — the work in hand, the work done, and what each took  [feature: F-work-board]
   [target]

**Context:** The person leads several windows and asks at any moment what the agent is doing. The work board holds that answer on a page, open whenever the person looks. It is the rendered status page the pack already promises, grown up, so one surface keeps one name. That page is one source file in the host's tree, published at one stable link the person opens from any device. A task reaches the work board when its wish is captured, before its statement is validated: validation gates entry into work, never entry onto the page. A row stays after the task closes, so the page carries what is being done and what was done, each with its time. The chat's departures board keeps its own job. The page carries the whole queue in columns, the work in hand among them. Every row the page shows stands in one column: an open row by the state its queue row records, a closed row in the done column read from the queue archive. The far tier stays off the page under its own request law, and the queued rows standing below the runnable head collapse into a stated count. A card reads as a task at a glance — its echo-name first, then what the change does, then its chips — and the technical detail sits behind the card. Each running step names the worker on it by a craft name and an icon, so which worker runs which task reads at one glance. The work board's form follows the sketch the person already approved, frozen as a norm copy under `docs/norms/` and cited by the form clause's norm pointer. Nothing of this scenario is built yet.

**User Story:** As a person leading several windows, I want one page showing work in hand and work done, so that I need not ask.

### Acceptance Criteria

**Case: the promises this work board leaves standing**

1. The system *shall* keep the chat's departures board at its own scope and shape, taking over none of its report duty. [INV-27]
2. The system *shall* keep narration whole, no board row standing in for a beat the session owes in the chat. [INV-35]
3. The system *shall* keep the capture echo's honest range and the delivery report's estimate beside actual as they stand. [INV-93]
4. The system *shall* keep the routine report's scope and the status report's chat home unchanged, its report-shape check riding the suite. [INV-38, INV-222]
5. The system *shall* keep the chat's live status line whole once the work board ships, the work board adding a view and reducing no chat duty. [INV-71]

**Case: the work board is the rendered status page, grown up**

6. The system *shall* read the work board as the rendered status page the pack already promises, one rendered surface under one name. [INV-308, INV-71]
7. The system *shall* hold the work board as one source file in the host's tree. [INV-308]
8. The system *shall* publish that source file at one stable link, updated from it, so the person opens the work board from any device. [INV-308, INV-67]
   [target]
9. The system *shall* register the work board in the host's surface registry `SURFACES.md`, with the marker text the completeness check reads in the rendered page and the spec anchors it answers to, before it renders. [E-10]
10. The system *shall* lead the work board with the one-line identifier every opened artifact carries — its project, and what it needs of the person. [INV-51]
11. The system *shall* keep one work board per host project and *shall* name the session on every row. [INV-308]
12. *when* a session writes the work board, the system *shall* pass the concurrent-edit fence like any shared-document write, and *shall* have a blocked write re-read the work board and re-apply its own row. [INV-308, INV-11]
13. The system *shall* read both surfaces off the same work, the chat's departures board answering inside every status report and on ask. [INV-308, INV-27]
14. The system *shall* keep the work board standing whether or not anyone asks. [INV-308]

**Case: the form the work board takes**

15. The system *shall* take the work board's form from the sketch the person approved, landing that approved form as a frozen copy under `docs/norms/` and citing it by this clause's norm pointer from the approval on. `norm: docs/norms/work-board.html` [INV-308, INV-43]
16. The system *shall* show board rows in feature language, the work in hand, and a timestamped feed. [INV-308]
17. The system *shall* have the work board's waiting region render the waiting board `WAITING.md` and keep no list of its own, so one clearing rule and one gate hold every waiting item. [INV-308, INV-206]
18. *when* a board row stands blocked — on the person through the waiting board, on another task, or on something outside the project — the system *shall* mark it blocked with the time it has stood so, leaving it in the column its own state names. [INV-308, INV-206]
19. The system *shall* carry every mark the work board shows with its meaning beside it in place, the page shipping no legend block. [INV-308]

**Case: the whole queue stands in columns**

20. The system *shall* show the whole queue on the board in columns, one column per recorded state. [INV-308] [default]
   - the columns are awaiting validation, ready, in work, and done.
21. The system *shall* state on the page, under each column, the one condition a card meets to leave that column. [INV-308]
22. The system *shall* stand every row it shows in exactly one column, dropping none, an open row's column read off the status its queue row records. [INV-308, INV-277]
   - awaiting validation reads off *queued*, ready off *ready*, and in work off *in-work*.
23. The system *shall* keep the far tier off the board, standing it down by name and opening its rows only on the person's request, as the runnable report does. [INV-308, INV-222, INV-223]
24. The system *shall* collapse the *queued* rows standing below the runnable head into a stated count that opens on the person's act, and *shall* drop none in silence. [INV-308] [default]
   - the retunable value is how many *queued* rows stand visible at the head before the rest collapse.
25. The system *shall* show the *deferred* rows as a stated count alone, each row's revisit trigger standing behind an expand. [INV-308, INV-222] [default]
26. The system *shall* place a parked row in the in-work column and *shall* leave its parked mark to the preemption case below. [INV-308, T-9]
27. The system *shall* split the in-work column into lanes, one lane for each build lane the lane cap allows. [INV-308, T-18]
28. The system *shall* show a lane holding no row as free. [INV-308, T-18]
29. The system *shall* have a free lane draw the head *ready* task into it, a lane already holding a row drawing none. [INV-308, T-18]

**Case: a card reads as a task at a glance**

30. The system *shall* order a card's reading: the echo-name first as the recognition hook, then the description of the behaviour, then the chips. It *shall* hold every other detail behind the card in a details layer. [INV-308, INV-28] [default]
   - the echo-name runs three to five plain words.
31. The system *shall* expand every count and reference in a card's details into plain words an outside reader follows, a bare number standing as a defect. [INV-308, INV-28]
32. The system *shall* show a placement tag, as a chip on every board row, read from the queue row's own map and footprint notes. [INV-308, INV-37, INV-128]
   - the tag names the feature the row belongs to, or the several modules the row reaches across.
33. The system *shall* have every board row name and link the part of the product spec its task changes, read from that placement note and the spec delta's own anchors. [INV-308, INV-37]
34. The system *shall* show an in-work row's plan — the deliverables of the task's own statement — on its board row. [INV-308]
35. The system *shall* mark beside that plan the one pipeline stage of the nine the row now stands at. [INV-308, INV-27]
36. The system *shall* keep the fine-grained trail of activity off the card, in the delivery report and the journal the trail criterion below already names. [INV-308, INV-311]
37. The system *shall* lead each deliverable's line with its state mark alone, that line carrying no numbering beside the mark. [INV-308]
38. The system *shall* show a card in work with its settled deliverables and their progress, no line on such a card phrased as an option or an open choice. [INV-308, INV-28]
39. *when* a genuine fork opens mid-work, the system *shall* mark that card blocked under the rule above and *shall* put the question to the person. [INV-308, INV-206]
40. The system *shall* name an in-work row's branch and worktree in the row's details, read from the lane's own claim commit and checkpoint. [INV-308, E-34, INV-69]

**Case: a task enters work only through a validated statement**

41. The system *shall* give every task a statement carrying its echo-name, its description, its plan, and its time estimate. [INV-309, INV-28]
42. The system *shall* keep a task's statement and its validation record in the work board's own source file, keyed by the queue row's id, the queue row keeping its five cells. [INV-309, INV-277]
43. The system *shall* have the plan list the deliverables in the order they run, each a slice of the change that shows value on its own and can be tested on its own. [INV-309]
44. The system *shall* hold an activity that carries value only alongside others — writing the tests, say — outside a plan's deliverables. [INV-309]
45. The system *shall* keep a plan's deliverables to a handful. [INV-309] [default]
   - the retunable value is the most deliverables one plan holds, standing at five.
46. The system *shall* read the plan's parallel mark as the plan's expectation, the take-up lane decision deciding what actually runs together, and *shall* record a divergence plainly in the delivery report's trail. [INV-309, INV-49]
47. The system *shall* bound the deliverables running together inside one task by the same lane cap that bounds build lanes. [INV-309, T-18] [default]
48. The system *shall* read the statement's estimate as the one estimate every other surface cites — the capture echo's range, the board row, and the settling at the close. [INV-309, INV-93]
49. The system *shall* let no task enter work before its statement passes validation's mechanical floor — echo-name, description, plan and estimate each present, an estimate stated, and the register check clean. [INV-309]
50. The system *shall* put every statement before a clean-context reader that carries no project vocabulary and answers three questions from the statement alone — what is to be done, why, and how long — and a question the reader cannot answer fails the statement. [INV-309]
51. The system *shall* hold every outcome comment the board shows to the same plain reading the statement meets, judged by that same reader. [INV-309]
52. The system *shall* have that same reader pass the echo-name test — shown the echo-name alone later, it names which change the task is — a name it cannot place failing the statement. [INV-309, INV-28]
53. *when* a statement fails validation, the system *shall* have it rewritten and validated again, its task staying out of work until it passes. [INV-309]
54. The system *shall* read a passed validation as approval, since routing every statement to the person would stall the granted autonomy. [INV-309] [default]
55. *when* a task's statement passes validation, the system *shall* set its queue row's status to *ready*, dated like every other status. [INV-309, INV-277]
56. The system *shall* read that passing as the task's commitment point, the moment the pack takes the task on and stands behind delivering it. [INV-309]
57. The system *shall* hold the gate-and-reader approval as the standing road and the person's word on a single task as the exception, that standing policy recorded in `DECISIONS.md`. [INV-309] [default]

**Case: approved wording freezes**

58. *when* a statement passes, the system *shall* freeze its wording and speak the task in those words letter for letter, its echo-name standing as the task's one name in every communication that names the task — the chat, the reports, and a worker's brief. [INV-309, INV-28]
59. The system *shall* hold that wording at take-up, along the way, and at the close. [INV-309]
60. *when* the person re-words a statement, the system *shall* take the new wording and freeze it anew. [INV-309]
61. The system *shall* let a task's estimate and its plan be revised only before the task is taken up, the revision running statement validation again and freezing the statement anew. [INV-309, INV-93]
62. *when* a task has been taken up, the system *shall* hold its estimate as it stands and *shall* state any overrun plainly at the close. [INV-309, INV-93]

**Case: the row carries the time promised and the time spent**

63. *when* a task is taken up, the system *shall* write its statement's estimate on its board row. [INV-310, INV-93]
64. *when* a task closes, the system *shall* stand the actual beside that estimate on the same row. [INV-310, INV-93]
65. The system *shall* extend the landing's own settling of estimate against actual onto the work board. [INV-310, INV-93]
66. The system *shall* stand each closed task's end-to-end time beside that pair, from its statement passing validation to its close, read off the board's own stamps. [INV-310, INV-93] [default]
67. The system *shall* show how many tasks closed on the day the page is read, counted off those same stamps. [INV-310] [default]
   - the retunable value is the stretch the count covers, standing at one day.

**Case: a closed task keeps its row**

68. The system *shall* keep every closed task's row on the work board rather than clear it. [INV-311]
69. The system *shall* render each closed task in the done column as one line — state mark, echo-name, time pair — the rest behind a fold the person opens. [INV-311, INV-28] [default]
70. The system *shall* read the done column from the month's archive file under `docs/queue-archive/`, the current month standing by default and an older month opening on the person's ask. [INV-311, INV-276] [default]
71. The system *shall* show each closed row's own terminal state — landed, declined, superseded, or decided — so a declined row shows as declined. [INV-311, INV-276]
72. The system *shall* tag each closed row with its door — feature, bug, refactor, docs-only, or skip — read from the archived row's own intake note. [INV-311, INV-134] [default]
   - the door is the default axis here; the person may prefer the work-kind axis — product, infra, skill, or prose — in its place.
73. The system *shall* extend the delivery report to carry a trail over the plan's steps — each step's outcome, the worker tier or role that ran it, and the step's share of the task's time. [INV-311, INV-103]
74. The system *shall* draw a closed row's step trail from that delivery report. [INV-311, INV-103]

**Case: a preempted task keeps its row**

75. *when* a bug preempts the lane, the system *shall* keep the parked task's row on the work board marked parked, naming the row that preempted it, and *shall* return it to the work in hand once the bug clears. [INV-308, T-9]
76. The system *shall* name that preemption on the page as the board's one queue-jumping class, open to the bug door alone. [INV-308, T-9, INV-134]

**Case: the worker on each running step**

77. The system *shall* name the worker on each running step of the plan by a fixed craft name and icon. [INV-308, INV-33]
78. The system *shall* have the seat name a step's craft in the worker's brief at spawn. The movement's checkpoint record *shall* carry that craft, its icon and the logged tier while the step runs, a mid-flight tier change updating it, and the board *shall* read a running step's worker there. [INV-308, INV-69, D-2]
79. The system *shall* hold the fixed craft set and its icons in the work board's own source file as their one home. [INV-308]
80. The system *shall* read the board's craft names as display names of the pipeline's craft standards, keeping the skill names internal. [INV-308, INV-33, INV-137]
   - Reader stands for the reader worker, Drafter the product-manager craft, Reviewer the formal-reviewer role, Builder the developer craft, Checker the quality-assurance craft.
   - the board's Reviewer names the proving craft, and the design-review role keeps its name.
81. The system *shall* stand a muted note of that worker's tier beside the craft name. [INV-308, INV-69]
82. The system *shall* take the starter crafts as the Reader, the Drafter, the Reviewer, the Builder, and the Checker. [INV-308] [default]
83. The system *shall* hold a worker's identity at its craft name, its icon, and its tier note, and *shall* take a fuller personality only on the person's word. [INV-308]
84. *when* a step's record names no craft, the system *shall* show that step with its craft unnamed rather than guess one. [INV-308]
85. The system *shall* keep which worker runs which task readable at one glance across the whole in-work column. [INV-308]

**Case: the work board refreshes at every moment the person could look**

86. The system *shall* update the work board at every pipeline stage change, at take-up, and at a worker's spawn and finish. [INV-312, INV-71]
87. The system *shall* update it at a landing, and at every state that waits on the person. [INV-312, INV-71]
88. *while* a stretch runs long with no stage change, the system *shall* refresh the work board's stamp on the same heartbeat the chat's narration already carries, so a quiet stretch reads apart from a stalled one. [INV-312, INV-35, INV-71]
89. The system *shall* carry the work board file's update inside the landing's own commit. [INV-312]
90. The system *shall* complete a work board update within about five seconds of the stage change it records, and *shall* never delay that stage. [INV-312] [default]
   - the generator's own suite timing assertion watches this number once the generator ships.

**Case: the work board reads on any screen**

91. The system *shall* lay the work board out in one column on a narrow screen, the work in hand at the top. [INV-313] [default]
92. The system *shall* make every control reachable by touch and *shall* hide nothing behind a hover. [INV-313]
93. The system *shall* keep the work board reachable by keyboard and readable at the contrast the pack's pages hold. [INV-313] [default]

**Case: the empty work board and the stale work board**

94. *when* no work is in hand, the system *shall* say so and show the queue's head in its place. [INV-313]
95. The system *shall* stamp the work board with the time it last updated, so a reader judges its freshness. [INV-313]
96. The system *shall* have an open page re-read itself about every five seconds. [INV-313] [default]

**Case: what the work board is not, and how its working shows**

97. The system *shall* merge no other project's work into a host's work board. [INV-308]
98. The system *shall* write on the work board no history the journal already owns. [INV-308]
99. The system *shall* count the work board working *when* the person answers four questions from the page alone over one real working stretch. The four are what is now being done, who runs what, what was done, and how long each took against its estimate. [INV-308]

---

## Requirement 310: A work block is grounded in the person's sight before it runs

**Context:** Sessions entered long work blocks the person could not connect to any request of theirs. A block and every line reporting it open by naming their root, so the person can correct the state by eye.

**User Story:** As a person leading the work, I want every work block and report line to open by naming the request it serves. Then I can judge at a glance why the session does what it does.

### Acceptance Criteria

**Case: the root is named before work runs**

1. *when* a work block starts, the system *shall* open it by naming its root beside the pipeline stage, the demanding rule, and the estimate. [INV-314]
2. A root *shall* be the person's dated request, a standing instruction of theirs, or a reason stated plainly enough for the person to judge. [INV-314]
3. The system *shall* start no work block whose root it cannot name. [INV-314]
4. The system *shall* name no machinery — an alarm, a gate, a scheduled reminder — as a root. [INV-314]
5. The system *shall* name instead the person's instruction the machinery carries. [INV-314]

**Case: reports carry the same root**

6. The system *shall* open every report line with its block's root, and *shall* count a report line missing its root a defect. [INV-314, INV-28]

**Case: a step outside the plan**

7. *when* a running block is about to step outside its announced plan, the system *shall* stop. [INV-314]
8. The system *shall* announce the out-of-plan step and its root before taking it. [INV-314]

**Case: the plan is the account**

9. The system *shall* keep each task's plan as the home a block is announced against. [INV-314, INV-308]
10. That home *shall* be the work board's per-task plan once the board ships, and the written plan page until then. [INV-314, INV-308]
11. The system *shall* account each block against its plan line in the delivery report. [INV-314, INV-103]


## Reference




The code-to-location table below is generated output, built from the body criteria by `scripts/build-index.py`; no one edits it by hand. Feature codes (`F-...`) live on their scenario headings and carry no table row.

| Code | Location |
|---|---|
| A-0 | R168.1, R308.1 |
| A-1 | R170.7, R172.8, R173.2, R177.1 |
| A-2 | R177.2 |
| A-3 | R48.4, R53.4, R75.3, R76.4, R177.5, R177.7, R276.1, R276.3 |
| A-4 | R178.4, R179.1, R179.2, R296.5, R296.6, R296.7 |
| A-5 | R168.1, R168.2, R177.8, R180.8, R182.5 |
| A-6 | R1.4, R177.9, R247.5 |
| A-7 | R125.3, R136.3, R177.10, R177.11, R177.12, R188.4, R202.3, R251.3, R268.1, R275.5, R308.6 |
| A-8 | R177.4, R180.7, R200.5 |
| A-9 | R179.4, R179.5, R296.3 |
| A-10 | R53.4, R174.3, R178.1, R193.12, R265.6, R299.8 |
| A-11 | R88.2, R180.4, R180.5, R180.7, R180.8, R180.9, R180.10, R193.12, R272.3 |
| ACT-1 | R144.2, R188.6, R200.1, R248.2 |
| ACT-2 | R100.1, R206.1, R208.1 |
| ACT-3 | R77.5, R128.1, R166.1, R171.9, R200.6, R206.4, R207.3, R207.7, R208.6, R213.5, R217.2, R235.6 |
| B-1 | R169.1, R169.3, R169.4, R169.5, R169.6, R169.7, R169.8 |
| B-2 | R167.1, R170.1, R170.2, R170.3, R170.4, R170.5, R170.6, R170.7, R172.1, R172.8, R173.3 |
| B-3 | R167.1, R169.9, R169.10, R171.1, R171.3, R171.4, R171.5, R171.6, R171.7, R171.8 |
| C-1 | R53.5, R258.1, R258.2, R258.3, R258.4, R258.5, R259.1, R265.2, R265.10, R276.1, R276.2 |
| D-2 | R208.5, R309.78 |
| D-4 | R198.3, R251.3, R275.5 |
| D-7 | R187.2 |
| E-1 | R3.1, R3.2, R3.3, R3.4, R187.1 |
| E-2 | R4.1 |
| E-3 | R4.1, R4.2, R94.3, R187.9 |
| E-4 | R97.1, R187.12, R191.1 |
| E-5 | R124.1, R223.1 |
| E-6 | R1.4, R102.1, R102.2, R169.2, R225.1, R225.3, R247.2 |
| E-7 | R1.4, R177.9, R247.1, R247.2, R247.3, R247.4 |
| E-8 | R47.3, R162.1, R200.5, R200.6, R202.1, R247.5 |
| E-9 | R179.3, R296.5 |
| E-10 | R61.1, R102.2, R169.11, R177.3, R228.6, R250.1, R250.2, R250.3, R260.3, R309.9 |
| E-11 | R153.3, R163.6, R187.4, R187.5, R187.7, R190.1, R190.4, R195.1, R195.2, R196.13, R196.14, R252.1, R252.2, R252.3 |
| E-12 | R2.1, R2.2, R2.3, R50.2, R51.1, R59.3, R198.1, R198.4, R198.5, R202.1 |
| E-13 | R47.3, R80.1, R80.2, R89.1, R91.2, R169.10, R170.4, R171.1, R171.2, R173.1, R173.5, R186.3, R198.1, R200.2, R200.4, R202.1, R202.2, R202.4, R207.4, R219.1, R220.4, R239.2, R300.14, R300.15 |
| E-14 | R16.1, R16.2, R118.1, R118.2, R118.3, R118.4, R118.5, R118.6, R124.1, R124.4, R159.2, R159.7, R177.6, R187.1, R194.3, R223.2, R259.2 |
| E-15 | R53.1, R87.3, R124.2, R124.3, R130.3, R177.6, R223.2 |
| E-16 | R130.9, R181.5, R181.6, R188.14, R193.5, R205.1, R205.3, R205.4, R205.5 |
| E-17 | R52.4, R59.2, R75.4, R76.4, R98.1, R98.2, R98.4, R99.2, R103.3, R104.6, R178.3, R225.2 |
| E-18 | R1.4, R145.1, R145.2, R248.1, R248.2 |
| E-19 | R130.3, R249.1, R249.2, R249.3 |
| E-20 | R144.1, R144.2, R144.3, R146.3, R187.13 |
| E-21 | R188.1, R188.2, R188.3, R188.4, R308.1 |
| E-22 | R7.1, R7.2, R7.3, R69.3, R163.4, R296.4 |
| E-23 | R188.5, R251.3, R251.4, R275.5 |
| E-24 | R130.5, R162.1, R162.3, R162.4, R164.1, R164.3, R166.5, R166.6, R166.7 |
| E-25 | R177.12, R188.5, R188.6, R188.7, R188.8, R194.8, R275.5 |
| E-26 | R36.1, R36.2, R36.3, R36.4, R267.4 |
| E-27 | R105.1, R105.2 |
| E-28 | R152.2, R158.4 |
| E-29 | R122.1, R224.1 |
| E-30 | R156.1, R156.2, R156.3 |
| E-31 | R189.1, R189.2, R189.3 |
| E-32 | R188.14, R193.1, R193.2, R193.4, R194.3, R195.9, R197.5, R197.7, R197.8 |
| E-33 | R190.2, R194.1, R194.2, R194.3 |
| E-34 | R83.1, R83.2, R83.3, R85.3, R88.5, R91.1, R309.40 |
| E-35 | R191.1, R195.11 |
| INV-1 | R4.3, R4.4, R5.1, R5.2, R13.5, R64.1, R92.2, R96.2, R96.3, R130.7, R130.8, R158.2, R187.3, R196.15, R254.2 |
| INV-2 | R77.1, R77.2, R77.3, R77.4, R77.5, R84.2, R86.1, R89.3, R90.5, R140.2 |
| INV-3 | R78.3, R197.6 |
| INV-4 | R7.1, R9.6, R10.3, R11.1, R11.3, R21.2, R22.7, R22.10, R32.3, R35.2, R45.4, R46.4, R56.2, R57.3, R69.3, R69.4, R72.3, R76.2, R78.1, R80.5, R88.3, R89.2, R153.2, R161.4, R163.4, R170.3, R193.3, R211.4, R212.5, R241.1 |
| INV-5 | R10.4, R21.2, R40.7, R75.3, R76.2, R78.2, R170.6, R203.1, R220.2 |
| INV-6 | R75.2, R124.2, R223.3 |
| INV-7 | R169.8, R179.1, R205.4, R256.5, R296.5, R296.11 |
| INV-8 | R168.1, R168.3, R168.4, R168.5 |
| INV-9 | R7.4, R7.5, R46.4, R72.4, R139.1, R163.3, R164.2, R171.4, R171.5, R200.1, R200.3, R219.1, R220.1 |
| INV-10 | R90.5, R100.1, R100.2, R158.1, R163.5, R166.7, R187.5, R187.6, R187.7, R192.2, R193.7, R193.8, R193.10, R195.2, R197.3, R205.3, R207.1, R251.1, R251.2 |
| INV-11 | R77.2, R81.3, R89.4, R90.5, R91.2, R128.4, R139.3, R141.1, R158.1, R166.2, R187.6, R193.7, R205.5, R207.3, R253.5, R256.1, R256.2, R256.7, R270.5, R301.11, R309.12 |
| INV-12 | R9.1, R9.4, R9.5, R9.6, R10.2, R13.4, R16.4, R47.2, R50.3, R160.3, R170.3 |
| INV-13 | R7.8, R198.2, R198.6, R205.1, R205.2, R308.2 |
| INV-14 | R157.2, R203.1, R203.2, R203.3, R204.1, R204.2, R204.3, R204.4, R248.1, R273.1 |
| INV-15 | R48.3, R161.3 |
| INV-16 | R40.3, R40.7, R41.1, R41.2, R43.3, R45.2, R50.4, R52.4, R99.1, R99.2, R99.3, R101.1, R147.2, R178.2, R220.1 |
| INV-17 | R2.2, R45.3, R98.3, R98.4, R102.3, R102.4, R103.3, R212.2, R225.2 |
| INV-18 | R10.4, R12.3, R46.3, R53.1, R53.2, R53.3, R53.4, R53.5, R57.3, R71.1, R72.1, R76.3, R118.6, R226.2, R259.4, R261.2, R263.3, R264.2, R264.3, R265.9, R265.10 |
| INV-19 | R75.2 |
| INV-20 | R12.3, R76.1, R76.2, R76.4 |
| INV-21 | R12.3, R76.1, R76.3, R76.4, R76.5, R154.4 |
| INV-22 | R9.6, R50.1, R50.2, R50.3, R50.4, R51.3, R56.4, R59.3, R61.5, R144.1, R146.3, R248.3 |
| INV-23 | R112.3, R114.8, R154.5, R163.1, R163.3, R163.5, R163.6, R166.8, R167.2, R207.5 |
| INV-24 | R54.3, R137.1, R137.2, R137.3, R137.4, R194.3, R194.4, R197.6, R197.9, R207.5 |
| INV-25 | R17.6, R201.1, R201.2, R201.3, R201.4, R201.5 |
| INV-26 | R14.1, R14.2, R14.3, R127.2, R127.3, R161.5, R287.5 |
| INV-27 | R15.1, R15.2, R15.4, R15.5, R15.6, R22.8, R23.1, R80.5, R86.3, R152.4, R154.1, R159.5, R159.7, R187.8, R195.12, R196.7, R196.9, R196.16, R254.5, R309.1, R309.13, R309.35 |
| INV-28 | R8.2, R17.1, R17.2, R17.3, R17.4, R17.5, R17.6, R17.7, R17.8, R22.8, R22.9, R29.3, R54.3, R159.4, R188.9, R191.3, R195.12, R212.5, R293.1, R293.2, R295.1, R295.3, R296.7, R309.30, R309.31, R309.38, R309.41, R309.52, R309.58, R309.69, R310.6 |
| INV-29 | R57.1, R57.2, R57.3, R57.4, R58.2, R63.2, R68.2 |
| INV-30 | R51.3, R59.1, R59.2, R59.3, R61.5, R65.2, R104.2, R108.1, R173.4, R175.3, R175.4, R175.5, R176.2, R261.3, R261.5, R263.4, R265.13 |
| INV-31 | R7.6, R32.4, R46.3, R53.2, R71.1, R71.2, R72.1, R157.1, R186.2, R191.3, R195.12, R220.2, R259.4, R261.2, R261.7, R263.4, R265.9, R265.13 |
| INV-32 | R8.1, R8.2, R31.3 |
| INV-33 | R51.1, R51.2, R51.3, R309.77, R309.80 |
| INV-34 | R18.2, R20.1, R20.2, R20.3, R21.1, R54.3 |
| INV-35 | R17.3, R22.1, R22.2, R22.3, R22.4, R22.5, R22.6, R22.7, R22.8, R22.9, R22.10, R23.1, R23.2, R25.5, R27.1, R29.2, R140.1, R157.6, R220.2, R309.2, R309.88 |
| INV-36 | R121.3, R122.3, R123.4, R173.1, R173.2, R173.3, R173.7, R174.1, R186.1, R193.12, R214.1, R219.2, R265.1, R265.2, R299.1 |
| INV-37 | R15.6, R16.1, R16.2, R16.3, R16.4, R16.5, R43.5, R43.8, R46.1, R118.6, R120.2, R159.7, R159.8, R173.4, R187.3, R187.4, R187.7, R244.5, R309.32, R309.33 |
| INV-38 | R159.1, R159.2, R159.3, R159.4, R159.5, R159.6, R159.8, R309.4 |
| INV-39 | R81.2, R81.3, R82.3, R85.4, R86.1, R90.5, R91.2, R130.6, R160.6, R160.7, R183.4, R184.1, R192.5, R207.2, R219.5, R219.7, R220.2, R256.6, R301.10 |
| INV-40 | R220.1, R220.2, R220.3, R220.4, R220.5, R220.6, R220.7, R220.8, R220.10, R226.1, R226.6 |
| INV-41 | R48.3, R118.4, R121.1, R121.2, R121.3, R121.4, R121.5, R191.9, R192.7, R194.9, R225.1, R226.3, R244.1, R245.1, R264.2 |
| INV-42 | R32.1, R32.2, R32.3, R32.4, R33.3, R36.2 |
| INV-43 | R43.2, R73.2, R103.1, R103.2, R103.3, R104.1, R104.2, R104.3, R104.4, R104.5, R104.6, R309.15 |
| INV-44 | R139.4, R146.1, R146.2, R146.3, R146.4, R214.1, R296.8 |
| INV-45 | R142.1, R219.6, R220.3, R226.1, R226.2 |
| INV-46 | R68.3, R112.4, R131.3, R213.1, R213.2, R213.3, R213.4, R214.3, R215.2, R220.8, R220.9, R301.17 |
| INV-47 | R227.1, R227.2, R227.3, R228.2 |
| INV-48 | R127.1, R127.2, R127.3, R157.6, R211.2 |
| INV-49 | R80.1, R82.1, R82.2, R82.3, R82.4, R91.1, R91.3, R92.1, R309.46 |
| INV-50 | R58.1, R58.2, R64.2, R67.1, R262.2 |
| INV-51 | R26.1, R26.2, R26.3, R28.2, R30.3, R309.10 |
| INV-52 | R27.1, R27.2 |
| INV-53 | R210.4, R216.1, R216.2, R216.3 |
| INV-54 | R217.1, R217.2 |
| INV-55 | R218.1, R218.2 |
| INV-56 | R130.6, R161.1, R165.1, R165.2, R165.3, R165.4, R187.7, R187.10 |
| INV-57 | R30.1, R30.2, R30.3 |
| INV-58 | R33.1, R33.2, R33.3 |
| INV-59 | R7.7, R34.1, R34.2, R34.3, R61.4, R70.1, R121.1, R154.3, R212.1, R254.6 |
| INV-60 | R21.3, R35.1, R35.2 |
| INV-61 | R142.1, R142.2, R142.3, R142.4, R213.5 |
| INV-62 | R73.1, R73.2, R167.2 |
| INV-63 | R74.1, R74.2 |
| INV-64 | R31.1, R31.2, R31.3, R153.2 |
| INV-65 | R167.1, R167.2, R167.3, R167.4 |
| INV-66 | R199.1, R199.2 |
| INV-67 | R28.1, R28.2, R28.3, R29.1, R29.4, R186.4, R194.11, R253.3, R254.7, R255.6, R309.8 |
| INV-68 | R152.1, R152.2, R152.3, R152.5, R152.6, R157.7, R158.3, R158.5 |
| INV-69 | R17.7, R18.4, R206.2, R206.3, R206.4, R208.1, R208.2, R208.3, R208.4, R208.5, R208.6, R208.7, R210.1, R210.2, R219.3, R219.4, R220.10, R230.1, R233.4, R309.40, R309.78, R309.81 |
| INV-70 | R72.1, R72.2, R72.3, R72.4, R131.1, R139.1, R211.1, R232.5 |
| INV-71 | R29.1, R29.2, R29.3, R29.4, R309.5, R309.6, R309.86, R309.87, R309.88 |
| INV-72 | R65.1, R67.1, R175.7, R258.3, R259.1, R259.2, R259.3, R259.4, R260.3, R261.4, R261.6, R261.7, R262.3, R263.4, R263.6, R265.8 |
| INV-73 | R87.3, R194.1, R224.2 |
| INV-74 | R48.3, R118.4, R122.1, R122.2, R122.3, R262.2 |
| INV-75 | R48.3, R118.4, R123.1, R123.2, R123.3, R123.4, R172.3 |
| INV-76 | R25.1, R128.1, R128.2, R128.3, R128.4, R128.5, R207.6, R207.8, R235.5 |
| INV-77 | R108.1, R108.2, R175.4 |
| INV-78 | R109.1, R109.2 |
| INV-79 | R110.1, R110.2, R172.2, R172.6, R187.2, R187.9, R187.12 |
| INV-80 | R111.1, R111.2, R111.3 |
| INV-81 | R11.3, R21.1, R21.2, R21.3 |
| INV-82 | R139.1, R139.2, R139.3, R139.4, R253.1, R253.7 |
| INV-83 | R18.1, R18.2, R18.3, R18.4, R19.2, R54.3, R93.3, R94.4, R95.3, R132.1, R176.3, R176.4, R186.4, R186.15, R191.6, R191.10, R192.1, R230.2, R230.5, R240.2 |
| INV-84 | R129.1, R129.2, R129.3, R129.4, R186.12 |
| INV-85 | R172.1, R172.2, R172.4, R172.5, R172.7, R214.1 |
| INV-86 | R187.1, R187.2, R187.6, R189.2 |
| INV-87 | R186.1, R186.2, R186.3, R186.5, R186.6, R186.7, R186.10, R186.11, R186.13, R186.14, R186.15, R186.16 |
| INV-88 | R186.8, R186.9 |
| INV-89 | R169.7, R180.3, R181.1, R181.2, R181.3, R181.4, R181.5, R181.7, R181.11 |
| INV-90 | R181.8, R181.9, R181.10, R181.11 |
| INV-91 | R115.2, R180.1, R180.2, R180.3, R188.13, R274.3, R274.4 |
| INV-92 | R182.1, R182.2, R182.3, R182.4, R182.5, R182.6, R182.7 |
| INV-93 | R22.5, R23.1, R23.2, R23.3, R23.4, R25.4, R309.3, R309.48, R309.61, R309.62, R309.63, R309.64, R309.65, R309.66 |
| INV-94 | R19.1, R19.2, R19.3, R54.3, R196.17, R196.18 |
| INV-95 | R25.1, R25.2, R25.3, R25.4, R25.5, R303.14 |
| INV-96 | R147.1, R147.2, R147.3, R148.3, R304.2, R304.5, R304.6 |
| INV-97 | R169.11, R193.13, R196.5, R228.1, R228.2, R228.3, R228.4, R228.5, R228.6, R260.4, R268.5, R269.1 |
| INV-98 | R132.1, R221.1, R221.2, R221.3, R221.4, R268.4 |
| INV-99 | R49.1, R49.2, R68.3 |
| INV-100 | R106.1, R106.2, R106.3, R106.4, R114.1, R114.2 |
| INV-101 | R54.1, R54.2, R54.3, R54.4, R55.2, R56.2, R56.4, R67.1, R85.3, R88.1, R90.4, R90.5, R194.2 |
| INV-102 | R107.1, R107.2, R107.3 |
| INV-103 | R44.2, R209.1, R209.2, R210.5, R301.9, R309.73, R309.74, R310.11 |
| INV-104 | R42.1, R42.2, R45.3 |
| INV-105 | R83.3, R88.1, R90.5, R207.3, R256.5, R256.6 |
| INV-106 | R140.1, R140.2 |
| INV-107 | R126.1, R126.2, R131.2, R183.2 |
| INV-108 | R43.2, R132.3, R154.5, R222.1, R222.2, R222.3, R222.4, R233.4, R269.1 |
| INV-109 | R24.1, R24.2, R24.3, R130.5 |
| INV-110 | R115.1, R183.1, R185.1, R185.2, R185.3, R185.4 |
| INV-111 | R130.7, R183.1, R183.2, R183.3, R183.4, R183.5, R183.6, R183.7, R184.1, R192.6 |
| INV-112 | R141.3, R190.4, R194.11, R195.2, R253.1, R253.2, R253.3, R253.7, R256.7 |
| INV-113 | R120.1, R120.2, R184.4, R214.1, R244.5 |
| INV-114 | R60.4, R150.2, R183.6, R184.1, R184.2, R184.3, R184.4, R184.5 |
| INV-115 | R130.5, R131.1 |
| INV-116 | R130.1, R131.1, R141.1, R141.6, R141.9, R215.2, R242.2 |
| INV-117 | R77.3, R77.4, R79.1, R79.2, R79.3, R84.2, R89.4, R90.5, R303.16, R303.27, R303.28, R196.12, R251.6, R252.2, R255.1 |
| INV-118 | R149.1, R149.2, R149.3, R151.4 |
| INV-119 | R187.11, R187.13 |
| INV-120 | R150.1, R150.2, R150.3, R150.4, R151.3 |
| INV-121 | R11.1, R11.2, R43.6, R211.1, R211.3, R212.1 |
| INV-122 | R119.1, R119.2, R119.3, R130.6, R214.1, R244.2 |
| INV-123 | R130.6 |
| INV-124 | R46.2, R67.4, R161.1, R161.2, R161.3, R161.4, R161.5, R161.6, R260.2, R300.18 |
| INV-125 | R55.1, R61.4, R61.5, R61.7, R62.3, R63.3, R64.3, R66.1, R67.1, R70.1, R116.2, R175.7, R260.1, R260.2, R260.3, R260.4, R260.5, R260.6, R263.9, R264.5, R266.9, R267.4 |
| INV-126 | R67.1, R175.7, R261.1, R261.2, R261.3, R261.4, R261.5, R261.6, R261.7, R263.9, R264.5, R266.9 |
| INV-127 | R65.1, R66.1, R67.1, R262.1, R262.2, R262.3, R262.4, R262.5 |
| INV-128 | R43.1, R43.2, R43.3, R43.4, R43.5, R43.6, R43.7, R43.8, R44.1, R174.2, R309.32 |
| INV-129 | R92.1, R92.2, R93.1, R94.1, R95.1, R95.3, R190.7, R287.4 |
| INV-130 | R7.6, R7.7, R69.5, R196.7 |
| INV-131 | R41.3, R41.4 |
| INV-132 | R224.3, R224.4 |
| INV-133 | R38.1, R38.2, R38.3 |
| INV-134 | R44.1, R44.2, R44.3, R174.4, R309.72, R309.76 |
| INV-135 | R67.2, R174.1, R174.2, R174.3, R174.4, R174.5, R175.2, R193.12, R226.4, R244.6, R265.1, R265.4, R265.6, R265.7, R299.8, R299.10 |
| INV-136 | R61.5, R61.6, R175.1, R175.2, R175.3, R175.4, R175.5, R175.6, R175.7, R175.8, R263.9, R264.5, R265.1, R265.2, R265.5, R266.9, R267.4, R299.14, R299.15 |
| INV-137 | R17.7, R210.1, R210.2, R210.3, R210.4, R210.5, R216.3, R233.4, R309.80 |
| INV-138 | R52.1, R52.2, R67.1, R263.1, R263.2, R263.3, R263.4, R263.5, R263.6, R263.7, R263.8, R263.9, R264.3, R264.5, R265.11, R266.9 |
| INV-139 | R61.5, R176.1, R176.2, R176.3, R176.4, R176.5, R267.4 |
| INV-140 | R60.1, R60.2, R60.3, R60.4, R61.3, R68.1, R69.1 |
| INV-141 | R55.4, R61.1, R61.2, R61.3, R61.4, R61.5, R61.6, R62.1, R63.1, R68.1, R69.2, R69.4, R70.3, R70.5, R130.2, R131.1, R214.4, R263.8, R274.6 |
| INV-142 | R68.2, R69.1, R69.2, R69.3, R69.4, R69.5, R70.2, R70.3, R214.4, R244.4 |
| INV-143 | R56.2, R197.4, R211.1, R211.2, R211.3, R211.4, R212.1, R214.5, R233.4 |
| INV-144 | R46.1, R46.2, R46.3, R46.4 |
| INV-145 | R68.1, R131.1, R131.2, R131.3, R191.9, R214.3, R215.2, R220.9 |
| INV-146 | R15.3, R195.1, R254.1, R254.2, R254.3, R254.4, R255.5 |
| INV-147 | R15.3, R254.7 |
| INV-148 | R254.8 |
| INV-149 | R255.1, R255.2, R255.3, R255.4, R255.5, R255.6 |
| INV-150 | R55.1, R55.2, R55.3, R55.4, R56.1, R56.3, R86.4, R88.4, R90.3, R90.4, R114.6, R191.8, R193.9, R194.5, R196.11, R233.1, R263.8 |
| INV-151 | R45.1, R45.2, R45.3, R45.4, R56.1, R212.3, R308.7 |
| INV-152 | R45.4, R56.1, R88.3, R93.2, R197.9, R212.1, R212.2, R212.3, R212.4, R212.5, R214.5, R232.2, R241.4 |
| INV-153 | R56.1, R56.2, R56.3, R56.4, R191.10, R195.10, R196.4 |
| INV-154 | R70.1, R70.2, R70.3, R70.4, R70.5, R130.2 |
| INV-155 | R112.1, R112.2, R112.3, R112.4, R112.5, R114.3, R162.2, R212.4 |
| INV-156 | R67.2, R68.1, R68.2, R68.3, R68.4, R116.2, R141.5 |
| INV-157 | R114.1, R114.2, R114.3, R114.4, R114.5, R114.6, R114.7, R114.8, R115.3, R116.3, R117.1, R234.4, R236.4, R272.1 |
| INV-158 | R115.1, R115.2, R115.3, R116.3, R267.2 |
| INV-159 | R44.3, R47.5, R48.1, R48.2, R48.3, R48.4, R57.4, R68.4, R76.4, R88.2, R104.5, R116.3, R121.5, R122.3, R123.4, R124.4, R188.14, R193.12, R209.2, R262.4, R265.14, R266.4, R266.9, R267.6, R275.6 |
| INV-160 | R48.4, R116.1, R116.2, R116.3 |
| INV-161 | R157.1, R157.2, R157.3, R157.4, R157.7 |
| INV-162 | R117.1, R117.2, R117.3, R117.4, R117.5, R117.6, R207.8, R234.3, R235.2, R235.3 |
| INV-163 | R36.3, R36.4, R48.4, R115.3, R133.3, R174.6, R175.8, R176.5, R195.10, R260.5, R267.1, R267.2, R267.3, R267.4, R267.5, R267.6 |
| INV-164 | R121.2, R132.1, R132.2, R132.3, R226.3, R243.2, R244.3, R270.1, R272.1 |
| INV-165 | R62.1, R62.2, R62.3, R63.3, R65.3 |
| INV-166 | R133.1, R133.2, R133.3 |
| INV-167 | R64.1, R64.2, R64.3, R65.3, R67.1 |
| INV-168 | R65.1, R65.2, R65.3, R67.1 |
| INV-169 | R63.1, R63.2, R63.3, R66.2, R68.2 |
| INV-170 | R66.1, R66.2 |
| INV-171 | R66.2, R67.1, R67.2, R67.3, R67.4 |
| INV-172 | R188.10, R268.1, R268.2, R268.3, R268.4, R268.5, R268.6, R272.2, R275.2 |
| INV-173 | R133.3, R135.3, R232.1, R269.1, R269.2, R269.3, R269.4, R269.5, R275.3, R294.4, R301.12 |
| INV-174 | R195.2, R253.4, R253.5, R270.5 |
| INV-175 | R246.4, R270.1, R270.2, R270.3, R270.4, R270.5, R271.1, R271.2, R271.4, R275.3, R292.3, R292.7, R294.4 |
| INV-176 | R246.7, R272.1, R272.2, R272.3 |
| INV-177 | R188.10, R188.11, R228.5, R275.2 |
| INV-178 | R242.3, R273.1, R273.2, R274.7, R275.4 |
| INV-179 | R157.5 |
| INV-180 | R275.1, R275.2, R275.3, R275.4, R275.5, R275.6 |
| INV-181 | R148.1, R148.2, R148.3 |
| INV-182 | R189.4, R189.5, R196.5, R197.9 |
| INV-183 | R95.2, R135.2, R190.1, R190.2, R190.3, R190.8, R191.2, R194.6, R195.9, R195.14 |
| INV-184 | R188.14, R193.2, R193.3, R193.4, R193.5, R193.6, R193.7, R193.8, R193.9, R193.10, R193.11, R193.12 |
| INV-185 | R193.11, R194.4, R194.5, R194.6, R194.15 |
| INV-186 | R194.7, R194.8, R194.12 |
| INV-187 | R194.8, R194.9, R194.10, R194.11, R194.12, R197.8, R214.1, R253.6 |
| INV-188 | R194.13, R194.14 |
| INV-189 | R56.1, R191.8, R192.4, R194.14, R195.1, R195.3, R195.4, R195.5, R195.6, R195.7, R195.8, R195.10, R252.3, R252.4 |
| INV-190 | R195.13, R196.1, R196.2, R196.3 |
| INV-191 | R56.2, R195.13, R196.4 |
| INV-192 | R190.3, R196.3, R196.7, R196.12, R196.13, R196.14, R196.15, R196.16 |
| INV-193 | R195.1, R196.17, R196.18, R197.2, R252.4 |
| INV-194 | R195.14 |
| INV-195 | R195.9 |
| INV-196 | R196.7, R196.8, R196.9 |
| INV-197 | R195.6, R195.7, R196.5, R196.6, R196.19 |
| INV-198 | R82.2, R85.1, R85.2, R85.3, R85.4, R85.5, R87.2, R89.3, R90.1, R90.2, R91.1, R192.6, R279.12 |
| INV-199 | R86.1, R86.2, R86.3, R86.4, R86.5 |
| INV-200 | R87.1, R87.2, R87.3 |
| INV-201 | R83.2, R88.1, R88.2, R88.3, R88.4, R88.5, R88.6 |
| INV-202 | R229.1, R229.2, R229.3, R229.4, R232.7, R233.5, R294.4 |
| INV-203 | R18.4, R18.5, R19.3, R134.2, R135.3, R230.1, R230.2, R230.3, R230.4, R230.5, R230.6, R230.7, R232.7, R233.2, R233.6, R294.2, R294.3, R300.5 |
| INV-204 | R117.6, R234.1, R234.2, R234.3, R234.4, R235.4, R236.4 |
| INV-205 | R236.1, R236.2, R236.3, R236.4, R238.4, R239.3, R240.3 |
| INV-206 | R94.3, R237.1, R237.2, R237.3, R237.4, R237.5, R241.3, R309.17, R309.18, R309.39 |
| INV-207 | R238.1, R238.2, R238.3, R238.4, R238.5 |
| INV-208 | R242.1, R242.2, R242.3, R242.4 |
| INV-209 | R243.1, R243.2, R243.3, R243.4, R243.5, R245.3, R287.3 |
| INV-210 | R246.1, R246.2, R306.15, R307.13 |
| INV-211 | R246.3, R246.4, R292.1, R292.6, R292.7, R292.8, R294.4 |
| INV-212 | R226.2, R246.5, R246.6, R292.1, R292.5, R306.15, R307.13 |
| INV-213 | R235.1, R235.2 |
| INV-214 | R82.4, R91.1, R91.2, R91.3, R91.4, R266.7 |
| INV-215 | R134.1, R134.2 |
| INV-216 | R246.7, R246.8 |
| INV-217 | R191.5, R215.2, R274.1, R274.2, R274.3, R274.4, R274.5, R274.6, R274.7 |
| INV-218 | R113.1, R113.2, R303.29, R303.30, R303.32, R301.18, R301.19, R302.7, R302.14, R306.13 |
| INV-219 | R193.13 |
| INV-220 | R231.1 |
| INV-221 | R135.1, R135.2, R135.3, R230.3 |
| INV-222 | R5.3, R5.4, R5.5, R94.1, R94.2, R94.3, R94.4, R95.3, R196.11, R239.1, R257.4, R309.4, R309.23, R309.25 |
| INV-223 | R5.5, R94.3, R239.1, R239.2, R239.3, R239.4, R309.23 |
| INV-224 | R226.4, R226.5, R296.13 |
| INV-225 | R196.9, R196.10, R196.11, R196.19, R196.20 |
| INV-226 | R52.5, R121.3, R214.1, R258.4, R263.9, R264.1, R264.2, R264.3, R264.4, R264.5, R265.3, R265.11, R266.9 |
| INV-227 | R169.9, R180.6, R188.12, R188.13, R188.14 |
| INV-228 | R240.1, R240.2, R240.3 |
| INV-229 | R241.1, R241.2, R241.3, R241.4 |
| INV-230 | R207.8, R235.3, R235.4, R235.5 |
| INV-231 | R95.1, R95.2, R95.3, R190.6, R190.7 |
| INV-232 | R194.11, R253.6 |
| INV-233 | R244.1, R244.2, R244.3, R244.4, R244.5, R244.6, R244.7 |
| INV-234 | R245.1, R245.2, R245.3, R245.4, R245.5 |
| INV-235 | R197.2, R197.4, R214.1, R214.2, R214.3, R214.4, R214.5 |
| INV-236 | R190.4, R190.5, R190.6, R190.7, R190.8 |
| INV-237 | R215.1, R215.2, R215.3, R215.4, R220.9 |
| INV-238 | R232.1, R232.2, R232.3, R294.1 |
| INV-239 | R191.1, R191.2, R191.3, R191.4, R191.5, R191.6, R191.7, R191.8, R191.9, R191.10 |
| INV-240 | R192.1, R192.2, R192.3, R192.4, R192.5, R192.6, R192.7 |
| INV-241 | R232.3, R233.1, R233.2, R233.3, R233.4, R233.5, R233.6, R233.7, R233.8 |
| INV-242 | R257.1, R257.2, R257.3, R257.4, R257.5 |
| INV-243 | R271.1, R271.2, R271.3, R271.4, R275.5 |
| INV-244 | R258.5, R265.1, R265.2, R265.3, R265.4, R265.5, R265.6, R265.7, R265.8, R265.9, R265.10, R265.11, R265.12, R265.13, R265.14, R265.15, R266.1, R266.7, R299.4 |
| INV-245 | R151.1, R151.2, R151.3, R151.4 |
| INV-246 | R232.4, R232.5, R232.6 |
| INV-247 | R93.1, R93.2, R93.3, R303.26, R195.16 |
| INV-248 | R266.1, R266.2, R266.3, R266.4, R266.5, R266.6, R266.7, R266.8, R266.9 |
| INV-249 | R195.15, R195.16 |
| INV-250 | R277.1, R277.2, R277.3 |
| INV-251 | R277.4, R277.5, R277.6, R277.7, R277.8 |
| INV-252 | R277.9, R277.10 |
| INV-253 | R277.11, R277.12 |
| INV-254 | R277.13, R277.14 |
| INV-255 | R277.15, R277.16 |
| INV-256 | R277.17, R277.18 |
| INV-257 | R277.19, R277.20 |
| INV-258 | R278.1, R278.2, R306.4 |
| INV-259 | R278.3, R278.4 |
| INV-260 | R279.1 |
| INV-261 | R279.2, R279.3, R279.4, R279.5, R279.13 |
| INV-262 | R279.6, R279.7 |
| INV-263 | R279.8, R279.9, R279.10, R279.11 |
| INV-264 | R280.1, R280.2, R280.3, R280.4, R280.5, R280.6, R280.7 |
| INV-265 | R280.8 |
| INV-266 | R220.9, R281.1, R281.2 |
| INV-267 | R281.3, R281.4, R281.5, R281.6 |
| INV-268 | R281.7 |
| INV-269 | R303.9, R282.1, R282.2, R284.4, R285.3, R288.5, R296.10, R297.11, R299.12, R301.20, R302.8, R304.4, R306.14, R306.16, R307.14 |
| INV-270 | R277.21, R277.22, R283.7, R286.3, R289.6 |
| INV-271 | R191.4, R191.7, R278.5, R278.6, R278.7 |
| INV-272 | R283.1, R283.2, R283.3, R283.4, R283.5, R283.6, R283.7 |
| INV-273 | R284.1, R284.2, R284.3, R284.4 |
| INV-274 | R169.4, R285.1, R285.2, R285.3, R285.4 |
| INV-275 | R286.1, R286.2, R286.3, R286.4 |
| INV-276 | R5.1, R96.4, R130.7, R209.1, R243.1, R243.5, R245.5, R257.1, R286.4, R287.1, R287.2, R287.3, R287.4, R287.5, R309.70, R309.71 |
| INV-277 | R288.1, R288.2, R288.3, R288.4, R288.5, R309.22, R309.42, R309.55 |
| INV-278 | R289.1, R289.2, R289.3, R289.4, R289.5, R289.6 |
| INV-279 | R290.1, R290.2, R290.3, R290.4, R290.5 |
| INV-280 | R291.1, R291.2, R291.3 |
| INV-281 | R230.6, R230.8 |
| INV-282 | R292.1, R292.2, R292.3, R292.4, R292.5, R292.6, R292.7, R292.8 |
| INV-283 | R293.1, R293.2, R293.3, R293.4, R293.5, R293.6, R293.7, R293.8, R295.2 |
| INV-284 | R294.1, R294.2, R294.3, R294.4 |
| INV-285 | R295.1, R295.2, R295.3, R295.4, R295.5, R295.6, R295.7 |
| INV-286 | R296.1, R296.2, R296.3, R296.4, R296.5, R296.6, R296.7, R296.8, R296.9, R296.10, R296.11, R296.12, R296.13 |
| INV-287 | R297.1, R297.2, R297.3, R297.4, R297.5, R297.6, R297.7, R297.8, R297.9, R297.10, R297.12 |
| INV-288 | R297.13, R297.14, R297.15, R297.16, R297.17, R297.18, R302.11 |
| INV-289 | R298.1, R298.2, R298.3, R298.4, R298.5, R298.6 |
| INV-290 | R226.7, R226.8, R226.9, R226.10 |
| INV-291 | R299.1, R299.2, R299.3, R299.4, R299.5, R299.6, R299.7, R299.8, R299.9, R299.10, R299.11, R299.13, R299.14, R299.15 |
| INV-292 | R300.1, R300.2, R300.3 |
| INV-293 | R300.4, R300.5, R300.6, R300.7 |
| INV-294 | R300.8, R300.9, R300.10, R300.11 |
| INV-295 | R300.12, R300.13, R300.14, R300.15 |
| INV-296 | R300.16, R300.17 |
| INV-297 | R300.18, R300.19, R300.20 |
| INV-298 | R301.1, R301.2, R301.3, R301.4, R301.5, R301.6, R301.7, R301.8, R301.9, R301.10, R301.11 |
| INV-299 | R301.12, R301.13, R301.14, R301.15, R301.16, R301.17, R301.18, R301.19 |
| INV-300 | R208.7, R208.8, R208.9 |
| INV-301 | R302.1, R302.2, R302.3, R302.4, R302.5, R302.6, R302.7, R302.8, R302.9, R302.10, R302.11, R302.12, R302.13, R302.14, R302.15, R302.16 |
| INV-302 | R303.1, R303.2, R303.3, R303.4, R303.5, R303.6, R303.7, R303.8, R303.9, R303.10, R303.11, R303.12, R303.13, R303.14, R303.15, R303.16, R303.17, R303.18, R303.19, R303.20, R303.21, R303.22, R303.23, R303.24, R303.25, R303.26, R303.27, R303.28, R303.29, R303.30, R303.31, R303.32, R303.33 |
| INV-303 | R304.1, R304.2, R304.3, R304.4, R304.5, R304.6, R304.7, R304.8, R304.9, R304.10 |
| INV-304 | R141.5, R141.6, R141.7, R141.8, R141.9, R141.10, R141.11, R141.12, R141.13, R305.1 |
| INV-305 | R306.1, R306.2, R306.3, R306.4, R306.5, R306.6, R306.7, R306.8, R306.9, R306.10, R306.11, R306.12, R306.13, R306.14, R306.15, R306.16 |
| INV-306 | R307.1, R307.2, R307.3, R307.4, R307.5, R307.6, R307.7, R307.8, R307.9, R307.10, R307.11, R307.12, R307.13, R307.14 |
| INV-307 | R308.3, R308.4, R308.5, R308.7 |
| INV-308 | R309.6, R309.7, R309.8, R309.11, R309.12, R309.13, R309.14, R309.15, R309.16, R309.17, R309.18, R309.19, R309.20, R309.21, R309.22, R309.23, R309.24, R309.25, R309.26, R309.27, R309.28, R309.29, R309.30, R309.31, R309.32, R309.33, R309.34, R309.35, R309.36, R309.37, R309.38, R309.39, R309.40, R309.75, R309.76, R309.77, R309.78, R309.79, R309.80, R309.81, R309.82, R309.83, R309.84, R309.85, R309.97, R309.98, R309.99, R310.9, R310.10 |
| INV-309 | R309.41, R309.42, R309.43, R309.44, R309.45, R309.46, R309.47, R309.48, R309.49, R309.50, R309.51, R309.52, R309.53, R309.54, R309.55, R309.56, R309.57, R309.58, R309.59, R309.60, R309.61, R309.62 |
| INV-310 | R309.63, R309.64, R309.65, R309.66, R309.67 |
| INV-311 | R309.36, R309.68, R309.69, R309.70, R309.71, R309.72, R309.73, R309.74 |
| INV-312 | R309.86, R309.87, R309.88, R309.89, R309.90 |
| INV-313 | R309.91, R309.92, R309.93, R309.94, R309.95, R309.96 |
| INV-314 | R310.1, R310.2, R310.3, R310.4, R310.5, R310.6, R310.7, R310.8, R310.9, R310.10, R310.11 |
| M-1 | R49.2, R80.7, R80.8, R92.2, R130.1, R130.2, R130.3, R130.4, R130.5, R130.6, R130.7, R130.8, R130.9, R164.4, R166.3, R166.8, R198.6, R249.2 |
| M-2 | R14.3, R125.1, R125.2, R125.3, R303.13, R177.12, R204.3 |
| M-3 | R136.1 |
| M-4 | R251.5 |
| M-5 | R138.1, R138.2, R246.1 |
| M-6 | R60.3, R72.4, R141.1, R141.2, R141.3, R141.4, R144.2, R203.3, R203.4, R219.6, R220.3, R254.8, R259.3 |
| M-7 | R136.2, R136.3, R177.11, R180.9, R181.10, R188.5, R201.2, R201.4, R201.5, R275.5, R308.3, R308.5, R308.6 |
| S-0 | R1.1, R1.2, R1.3, R102.3, R159.3 |
| T-1..T-7 | R6.1, R6.2, R6.3, R6.4, R6.5 |
| T-7 | R75.4 |
| T-8 | R92.1, R95.1, R96.1, R96.2, R96.3, R96.4 |
| T-9 | R37.1, R37.2, R80.6, R81.1, R86.3, R160.1, R160.2, R160.3, R160.6, R160.7, R163.2, R165.4, R166.4, R309.26, R309.75, R309.76 |
| T-10 | R77.5, R79.3, R153.3, R155.1, R187.5, R187.9, R190.4, R195.2, R196.5, R254.5, R256.3, R256.4 |
| T-11 | R12.1, R12.2, R39.1, R39.2, R39.3, R39.4, R160.4 |
| T-12 | R40.1, R40.2, R40.3, R40.4, R40.5, R40.6, R50.1, R50.4, R101.1, R101.2, R154.1, R220.1 |
| T-13 | R52.1, R52.2, R52.3, R52.4, R52.5, R173.4, R263.7 |
| T-14 | R12.3, R16.5, R75.1, R75.2, R75.3, R75.4 |
| T-15 | R10.1, R10.2, R10.3, R12.4, R13.3, R40.1, R220.3 |
| T-16 | R9.1, R9.2, R9.3, R9.5, R9.6, R47.1, R47.2, R47.3, R47.4, R47.5, R48.3, R143.1, R143.2, R143.3, R173.4, R173.5, R173.6, R220.3, R248.3 |
| T-17 | R13.1, R13.2, R13.3, R13.5, R187.3, R187.7, R187.10 |
| T-18 | R80.1, R80.2, R80.3, R80.4, R80.5, R80.6, R80.7, R80.8, R81.1, R82.3, R85.1, R89.1, R89.2, R89.3, R89.4, R91.1, R160.5, R207.2, R256.6, R309.27, R309.28, R309.29, R309.47 |
| T-19 | R72.2, R208.3, R208.4, R219.1, R219.2, R219.3, R219.4, R219.5, R219.7, R220.5, R220.6, R220.7, R220.10 |
| T-20 | R45.3, R153.1, R153.2, R153.3, R153.4, R154.1, R154.2, R154.3, R154.4, R154.5, R155.1, R155.2, R155.3, R155.4, R156.2, R156.3, R254.6 |
| T-21 | R157.3, R157.4, R157.6 |
| T-22 | R189.5, R196.5, R197.1, R197.2, R197.3, R197.4, R197.5, R197.6, R197.7, R197.8, R197.9, R214.1 |
| T-23 | R84.1, R84.2, R86.2, R90.1, R90.2, R90.3, R90.4, R90.5, R91.1, R91.4 |
| T-24 | R195.10, R195.11, R195.12, R195.13 |
