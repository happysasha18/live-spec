# Rules cut from live-spec-base/SKILL.md — 2026-08-26

PLAN.md step 7 ("Срезать обязательный контекст"): a rule not covered by an eval fixture AND not
enforced by an executable script is a wish, not a rule — its place is `attic/`. Each rule below was
checked against `evals/director/scenarios.json` (the pack's one graded eval fixture) and against
every file under `guardrails/`, `hooks/`, and `tests/` for a mechanism that would actually go red on
a real violation, as opposed to a test that only asserts the rule's own wording is still present in a
document. None of the fourteen rules below cleared that bar. Each kept its number, and its number is
retired in `skills/live-spec-base/SKILL.md` rather than reused.

This is a whole-text move, not a summary: every word below is what stood under that number before the
cut. Nothing here is judged false or unwanted — only unenforced, by this pass's own narrow test.

---

11. **Verify by deed; show the real thing.** "Works" is said only after running it and seeing the result.
    Otherwise it is labelled an assumption. What the human sees is real data in its real render.
    Synthetic data is for your own checks alone, always carrying the literal label `SYNTHETIC`. Never
    show a bare file path in place of the thing itself.

14. **A found defect is a sample of its class — go find the class, sweep the look-alikes.** A bug, a stale
    name, a jargon string, a design inconsistency: before calling the fix done, name the pattern behind
    the instance abstractly — a scope too narrow, a missing guard, or an assumption that holds in one
    place and fails in the neighbour. Then search the whole repo and every user-facing surface for that
    kind, and fix all siblings in the same change: the search goes looking for the siblings not yet
    seen, past the one instance already reported, since one instance reported means the whole class is
    owned and the human never finds the second instance by eye. A confirmed bug carries three more moves
    before it closes, which with the class hunt above make the four moves the pipeline names: check the
    architecture, since a structural cause updates `ARCHITECTURE.md` and a cluster in one area reads as
    an architecture smell; check the spec, since a spec silent on the broken behaviour is the real
    defect, fixed first so the prover can flag it and the code then lands under it; and escalate to the
    human when the class boundary needs his read, since the agent never guesses the boundary. The full
    four-move law's homes are `skills/director/references/class-hunt.md` and the spec at INV-124.

    A rule superseded at a broad scope is the same class: its restatements at narrower scopes — a host's
    `CLAUDE.md`, a project's playbook copy, an installed skill — go stale the instant the broad rule
    changes, so the same change that supersedes the rule sweeps those copies and never leaves a
    narrower scope quoting the old rule. The pipeline sweeps code and surfaces on every bugfix, and the
    prover sweeps the document with its class lens before writing a point finding.

15. **The door is named before any code.** Every request states its entry point — feature · bug ·
    refactor · docs-only · skip — in one intake line beside size and priority, before the first line of
    code. The same line names the **work-kind** — product · infra · skill · prose — which is what the
    request builds. The door picks which pipeline steps run, and the kind picks the form each running
    step takes; the per-kind table's one home is `skills/director/references/work-kind-table.md`. At landing, every
    door-granted step has applied or been stood down by name in the report. So every skip is named and
    every kind touches the safety net (SPEC T-16, INV-22).
    Hard tripwires decide, never mood. Five of them send a request to the feature door. The first is a
    new user-visible surface. The second is new persistent state. The third is a new interaction on an
    existing surface. The fourth is a spec `[target]` mark on the touched surface. The fifth is
    behaviour no spec clause backs. Any of the five ⇒ FEATURE, however casually asked. The tripwire
    verdict outranks a casual label
    (queue-cutting stays with the bug door alone). The door re-fires mid-work. The moment running work is
    about to create a surface or state its door doesn't grant, stop, reclassify, and continue by the right
    door. Casual asks are routed, never refused, and never hand-built past the pipeline. (SPEC T-12, INV-16)

18. **One name-collision law.** A new file whose name is taken differentiates in two moves, the same
   everywhere in the pack: first the semantic mark its home already defines. The attic prefixes the
   source directory, and a decision file already carries its project and date. Then, where the name is
   still taken, a numeric ordinal
   `-2`, `-3`, … goes before the extension. Never overwrite, never a third scheme. True concurrency can
   race one name, as the inbox does with two sessions, one slug, and one moment. There a short session
   token joins the semantic mark, so a collision may cost a rename and never a lost file. (Audit
   2026-07-05: the attic had no answer for a second collision, and the attic and the inbox each spoke
   half a law.)

19. **The problem ledger — workshop noise is owned, never re-suffered.** Operational noise is written
   down the moment it fires: a flaky test harness, a missing dependency, an environment error, a tool
   misbehaving — this is the workshop around the work, and the product's own defect is a bug that takes
   the bug lane instead. Grep the host's `.live-spec/PROBLEMS.md` for the signature. Not listed → one
   WATCHED line (signature, date, one line of context) and keep working; that write replaces the silent
   retry. Listed → the second occurrence gets an owner at that moment: a queue row (OWNED) or the
   human's dated AGREED NON-PROBLEM — only the human's word can write the second of those, never the
   agent's, so the agent recommends, writes the recommended owner now, and the ask rides the batched
   report. A third recurrence arriving unowned is a defect of the method itself, past that day's noise,
   and goes to the pack's own queue (from a host window: one inbox file). A recurrence on an owned
   entry appends its date and changes nothing else; the landing that closes an OWNED entry's row flips
   it to SOLVED (SPEC E-24, INV-23).
   **A known, owned problem never blocks unrelated work (SPEC INV-56)**. It is parked, held by the
   ledger line, the owning row, or an expected-red note, and every unrelated lane keeps rolling.
   Hand-fixing loops cap at the second-occurrence law above. A defect with a named mechanical owner is
   serviced in BATCH: instances are fixed silently where the fence catches them, and one ledger append
   comes at the session's end, with no per-instance ceremony interrupting the work. A new bug still
   preempts, and this governs only the known, owned problem.

20. **Search for a skill before reinventing (SPEC INV-65).** At a project's setup, meaning founding or
   adoption's orient beside the founding questions, scan the installed skills and the catalogs you
   can reach for ones matching the project's kind and its crafts. Propose the fit list with a
   recommendation, and the human's word picks. At a struggle, the next attempt waits one search, since
   an existing skill or checklist may already own the failure class. A struggle is a ledger entry's
   second occurrence, a taste artifact rejected twice, or any returning failure family.
   The find is adopted or rejected
   by name, recorded where the struggle lives. Borrowing practice has three parts. Invoke a found skill
   as it ships. Paraphrase folded lessons and credit the source by name. Use verbatim text only under
   its license, notice kept.

21. **Human-facing prose is drafted by a clean writer (SPEC INV-84).** When a human will read the
   text, prepare a plain brief that states the facts, names the intended reader, and lists the
   register laws. Then hand it to a fresh writer session that has no package rules loaded. Let the
   writer produce the prose, review the returned draft against the brief, and land it, and
   do not write the prose yourself. Apply this to new text and to any page you are already editing. The
   unit is the section your edit touches, and a whole page is redrafted only on the human's word. Text you
   type live in chat stays your own words under the register laws. This rule binds the durable prose
   a human returns to. Settled text is left alone until a human rejects a specific page, or until
   your edit opens that page.

23. **A behavioural rule that breaks mid-turn twice earns a live channel (SPEC INV-108).** A standing
   behavioural rule keeps its normative home in a once-read file — the loader, a profile, a skill's
   text. When the rule breaks mid-turn a second time despite that home, it earns a live channel that
   same moment. The channel is one of two. It is an every-prompt hook line that reminds at the decision
   point, or a mechanical after-the-fact check that turns the suite red. Record the pick where the rule
   lives. The once-read
   homes stay the normative homes; the live channel only carries the rule to the moment it is needed.
   Prose in a once-read file loses to mid-turn momentum, and attention alone holds nothing across
   sessions. This rule is the convergence principle's application to behaviour (rule 22), kin of rule 19's
   second-occurrence law. The routing rule's worked proof — a once-read home that broke mid-turn since
   June, closed only when the every-prompt hook line and the mechanical after-the-fact check landed —
   is written out under rule 23 in [references/worked-examples.md](../skills/live-spec-base/references/worked-examples.md).
   That is the same cure that killed invented clock stamps. Open the reference when this rule's
   mechanism needs the concrete story.

28. **A periodic full audit catches the drift no lint names (SPEC INV-145).** Two layers guard the
   living documents against rot. The continuous lints are the register lint, the provenance-narrative
   check, and their kin. They run on every push. They hold each drift class already known, the moment it
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

32. **A release's number answers what taking it costs a host (SPEC INV-217).** The number reports what a
   host that vendored the previous version must do to take this one. A **patch** fixes a machine to hold a
   law already stated: no new capability, no changed contract, and the host takes it and does nothing. A
   **minor** grows what a host may adopt in a backward-compatible way: a new capability, a new law, or a
   new gate. The host takes it by re-running its catch-up walk [INV-91], with nothing it already carries
   rewritten. A **major** is a release a host cannot take without changing what it already carries. Four
   things earn it. A reworded rule the host vendored earns it. So does a renamed or removed surface a
   host depends on. So does a changed adoption or catch-up step. So does a moved law that forces host
   action. A major ships its dated
   `MIGRATION.md` chapter [INV-91]. The default is a patch. It is raised to a minor or a major only where
   the release earns the higher tier. This is a judgment the releasing session makes and states, **held by
   no machine**. The minor-versus-major call reads meaning a gate cannot. So it **stays a stated rule
   the session holds**. That is the same standing as a design-review finding that never blocks a lane
   [INV-141]. The 2.0.0
   release is this rule's cited boundary case, written out in
   [references/worked-examples.md](../skills/live-spec-base/references/worked-examples.md).

33. **The authoring seat does not adversarially certify its own work (SPEC INV-237).** The seat that
   authored a change drafts and accepts it, and it never provides that change's own adversarial
   certification. A head marinated in the authoring context is blind to the blind spot it just wrote. Two
   carriers hold it. A release's adversarial pass — the full re-prove at the release gate [INV-116] — is
   authored by a fresh seat. That seat is a differently-contexted head briefed from the primary sources.
   It is the same freshness the verify audit already demands of its checker (SPEC INV-46).
   The 2.7.0 release's own breach of this rule — an adversarial pass run in the context that had
   authored the new lenses, and so never turned onto the skill body that introduced them — is written
   out under rule 33 in [references/worked-examples.md](../skills/live-spec-base/references/worked-examples.md); open it when
   this rule's failure mode needs a concrete case. And a newly added lens or rule
   is run against the very document that introduces it before release. That is self-application, and
   the release record names the result.
   A release gate may require a dated clean-context review record naming a seat other
   than the release's. Whether the review was truly clean-context is a process fact no gate fully sees.
   So the gate checks only that the record exists, is dated to the release, and names a different seat.
   That is the mechanical floor under a discipline the seat holds.

34. **A deferred item's own state is re-derived from the code before its work resumes (SPEC INV-247).** A
   resume file and a queue row record a past moment. The technical problem statement a deferred or
   queued item carries says how the code it touches works. That statement can go stale as that code
   moves on. So the first
   act of resuming such an item is a freshness check of its own subject against the shipped source. Read
   the code the item touches. Confirm the problem the row describes still holds. Re-derive the item's
   real current state before designing anything on it. It is the resume-side twin of rule 13's primary
   source and of the architecture step's pin read from a command just run. Rule 8 re-reads versions at a
   breakpoint, and the queue-take re-scan re-reads a deferred row's revisit trigger [SPEC INV-129].
   This rule re-reads the item's own internals. So
   a session never designs a fix from a stale model of code that has since moved. And an item already
   handled is caught before the work restarts.

35. **A session's record is read at both ends by an agent that did not live it (SPEC INV-302).** A session
   that lived the work reads its own record badly. This rule's worked failure — a handover written
   from memory that named a question as still open when the owner had already answered it that day —
   and the note on the script once used to check a handover's three lines are both written out under
   rule 35 in [references/worked-examples.md](../skills/live-spec-base/references/worked-examples.md). Open it when either
   case needs the concrete story. So each end of a session is read by a fresh agent, never the session
   that lived the work. The mechanism — the session extract, the session handover file's shape, and
   the open-end's decision cross-check — lives in
   [references/session-handover.md](../skills/live-spec-base/references/session-handover.md), read when spawning that fresh
   agent at either end. Both ends stay a discipline the seat holds.
