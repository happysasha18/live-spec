# q-809 — second reading of the claimed rule loss

**RESOLVED, checked 2026-09-02 ~22:35.** All four genuine-loss defects this file names (rules 6, 7,
9, 31) already carry their exact replacement sentence, verbatim, in the live
`skills/live-spec-base/SKILL.md` — landed in commit `33ee1b38` ("Four rules restored, rule 10
repaired against its own spec"), which post-dates this analysis. Verified by direct grep against
the live file, not assumed from the commit message. This file's analysis stands as the record of
why; no further action owed against it.

Date: 2026-09-02. Independent re-read of `docs/prover/2026-09-02-full-range-review.md` finding F2,
which lists fifteen sentences of the old rulebook (`411a353`) said to survive in neither the new
`skills/live-spec-base/SKILL.md` body nor `references/rule-origins.md`.

Each row below answers three questions in order: does the substance survive somewhere a session
actually reads; if not, is the absence a defect or an improvement; and, for a defect only, the
shortest correct replacement sentence.

Count: **10 substance survives · 4 genuine loss, a defect · 1 genuine removal, an improvement.**

---

## Substance survives (10)

### R5 — "A one-shot with no decision goes to haiku, multi-step mechanical work to sonnet, and anything carrying judgment or design to the seat."

Survives twice, and better placed than before.

- `spec/roles-and-agents.md:279` [INV-69] — "The system *shall* run mechanical work on tiered
  workers — a no-decision one-shot worker, a multi-step mechanical worker, and the seat for
  judgment." The same three-way mapping, stated without a vendor's model names. The rule's own
  title cites INV-69, so the code resolves to it.
- `~/.claude/live-spec/profile.md`, `worker-tier` — "Sonnet by default for every worker; a stronger
  tier is the rare exception the seat has to justify … This sharpens the package's routing rule,
  which said only that mechanical work goes to sonnet."

Separately, the removal of the model names from the package rulebook is an improvement under this
file's own scope rule: "Never write host- or person-specific values here — those live in profiles,
and this file holds only package defaults and the rules themselves." A vendor's tier names go stale
and are exactly a host value. The profile's line already overrides the package mapping, so a body
naming haiku would have been wrong on this machine the day it was written.

The review's sharper sub-claim — that the rule is "unactionable" because "the body no longer names a
single tier" — does not hold. The body names the deciding criterion ("the trigger is judgment
against mechanical", "a judgment step is never routed down"), the abstract mapping is at the cited
code, and the concrete default is in the profile a session loads.

### R5 — "The worker pastes raw output (command + exit code + failing lines) as it works."

The law survives in the body: "Only raw output is evidence, and the worker's prose is only a lead.
So a worker's green is a lead the seat ACCEPTS by re-checking it, never on trust." The load-bearing
half — the seat re-checks rather than trusting — is intact, and the seat's re-check does not depend
on the worker having pasted anything.

The stricter successor is at `spec/test-honesty.md:113` [INV-80]: "*when* a run is a background or
delegated one, the system *shall* read its verdict from the suite log's own tail line, trusting no
wrapper's exit code." `skills/director/references/delegation-protocol.md:10` names rule 5 as the
raw-output law's home and line 31 requires "a command's output … never memory of a file".

### R7 — "Every session mints a stable identity at its start … the start time joined with the worktree path and a single-use random string."

The recipe survives whole under the code the body's bullet already cites. `spec/parallel-lanes.md`
Requirement 79:

- line 54: "*when* a session starts, the system *shall* mint one identity before its first act and
  record it in the session checkpoint under `.live-spec/`, unchanged for the session's life."
  [INV-117]
- line 55: "*shall* use the harness session identity where the context carries one and otherwise
  mint the identity from the session's start moment joined with its worktree path and a nonce."
  [INV-117]

The body's bullet reads "A tied concurrent claim breaks on each session's stable identity (SPEC
INV-117)". The review's line — "Rule 7 gives a session no way to mint the identity its own tie-break
turns on" — is a string-match artifact: it grepped the body and never followed the code.

### R7 — the "No unprotected concurrency" bullet's core

The bullet's operative content is the same clause as the "Brief-time disjointness" bullet that now
carries it. Old: "Two writers run at the same time only under a stated safety measure: worktree
isolation, or a write-set disjointness check the seat states in both briefs before either is
dispatched." New: "before spawning another concurrent writer, the seat confirms its brief's
write-set is disjoint from every already-running writer's brief, or gives it an isolated worktree at
brief-time (SPEC ACT-3, INV-11)."

The spec holds them as one clause, not two — `spec/roles-and-agents.md:296` [INV-11, INV-105,
ACT-3]. The old file stated one rule under two headings; merging them is de-duplication.

Two clauses of that bullet did leave, and they are judged separately below: the push-in-flight
clause (a defect, listed under the defects) and the nested-repo example plus "Sequencing is the
default" (improvements, listed there).

### R13 — "Your memory, a worker's summary, and a document's prose are leads, each confirmed against that evidence"

Survives across two rules and the spec. Body rule 13: "Ground every asserted fact in evidence you
can point to — a file:line, a commit, a command's real output; say 'not sure' and check before
asserting" — memory is not pointable evidence, so it is excluded by the positive form. Body rule 5:
"the worker's prose is only a lead." `spec/roles-and-agents.md:427`: "A worker's report is a lead
and never counts as evidence, since the head that made the work is blind to its own gap."

The rule's own title, "A claim needs its **primary** source", carries the document-prose half: a doc
restating a behaviour is not the primary source for that behaviour.

### R16 — "screen banner · `_prototype: true` field/header · first-line CLI banner · name/header marker"

`spec/draft-sandbox.md:11` [E-17] carries the enumeration verbatim in spec voice: "*shall* mark it
with the `PROTOTYPE` label in the form its kind can show — an on-screen banner for a rendered page, a
`_prototype: true` field or header for an API or data payload, a first-line banner for a script, and
the marker in the name or header line for a bare file." The body's rule 16 cites (SPEC E-17,
INV-17). String-match artifact.

### R17 — "always stop for the human's word, whatever the proactivity mode"

The clause defended against something no setting offers. `spec/settings-layers.md:11` [ACT-1, INV-9]
states the gate flatly, independent of any mode: "The system *shall* keep taste, design, the
irreversible and publish and push gates, domain wording, and the human's working contract with the
human." The settings ladder's `proactivity.mode` row (`references/settings-ladder.md:49`) defines
max-proactive as "proceed on recommendations, batch questions" — it removes no gate. The personal
profile's own `mode` line says the same: "pause only for taste, design, or irreversible-outside-git
calls."

The body's "Stop for the human's word on any truly irreversible action" is unconditional as written,
which is what the dropped clause was there to make explicit.

### R22 — "The distance to the goal only shrinks."

The non-regression duty survives as its mechanism, in the body and in the spec. Body: "A reached
level locks by a mechanism, because attention alone holds nothing across sessions."
`spec/roles-and-agents.md:564` [INV-98]: "*when* a process reaches a level, the system *shall* lock
it by a mechanism — a norm template, a conformance test, a lint floor that only rises, or a cap that
only ratchets down." A locked level is a distance that cannot grow; the old sentence stated the
consequence, the surviving one states the thing that enforces it.

### R25 — "A read to verify a claim or settle a decision stays with the seat."

Survives at `spec/roles-and-agents.md:377` [INV-137] — "The system *shall* keep a read done to
verify a claim or settle a decision with the seat, checking the real artifact and re-reading a
primary source being its own hands" — under the code rule 25's own title cites.

**The claimed contradiction with rule 13 does not exist.** The review states the body "now says every
read past a glance is dispatched". The body does not say that. It says: "Reading a file **to
understand or design it**, past a glance, is itself work: the seat dispatches it to a reader." A read
to verify a claim is neither understanding nor designing, so it never enters the dispatch duty. The
qualifier is the carve-out, and it is the same qualifier the spec's own clause 1 uses
(`spec/roles-and-agents.md:371`, "any read done to understand or design"). The review's contradiction
is manufactured by dropping four words from the sentence it quotes.

### R31 — "a field with no recorded permission stays home"

The body states the same rule positively: "only a permitted field leaves the tree, never a
credential, and no permission ever moves one (SPEC INV-188, INV-185)." A field with no permission is
not a permitted field. String-match artifact.

### R36 — "Never infer this from a title, a repository, or the fact that they are technical elsewhere."

The body: "Deepen the register only when they show that depth themselves." The word *only* carries
the ban — a title, a repository, and being technical elsewhere are all things other than showing it
themselves. String-match artifact.

---

## Genuine loss, a defect (4)

### R6 — "Red at a pause is never committed: the failing test name and the hypothesis become the top item of `NEXT_STEPS.md`"

The body kept the conclusion and dropped both premises: "Red at a pause is itself the checkpoint."
That sentence forbids nothing and names no file.

The two surviving homes are each conditioned on a different trigger and neither states the general
rule. `spec/live-status-reporting.md:159` [INV-95] fires only on the leave-word;
`spec/bug-priority-queue.md:11` [T-9] only when a bug arrives mid-feature.
`skills/communicator/SKILL.md:120-121` states it in full but inside the leave-word walk. A pause that
is neither — a context wipe, a milestone break, a handoff — is left uncovered, and rule 7, which
governs commits, says nothing about red.

The review's phrase "reduced to a metaphor" is fair.

**Replacement:**

> Red at a pause is never committed: the failing test's name and the hypothesis top the resume file,
> and that entry is the checkpoint (SPEC INV-95, T-9).

### R7 — "A push anywhere in flight holds its whole physical tree until it lands, before the seat starts a second writer on that path."

Absent from the body, from `references/`, from `spec/`, from `skills/`, and from `scripts/` and
`guardrails/` — grepped for "in flight", "holds its whole", "until it lands"; no hit states this.

It is not covered by brief-time disjointness: a push is not another writer holding a brief, so no
write-set comparison catches it. It is the owner's own standing word, dated 2026-09-01 ("no parallel
work around a push"), and it names a physical-tree fact, not a host value — package-level, so it
belongs in the rulebook.

**Replacement:**

> A push in flight holds its whole physical tree until it lands; no second writer starts on that
> path meanwhile (SPEC INV-11, ACT-3).

### R9 — "A shipped change updates its `README.md`, `CHANGELOG.md`, and `SKILL.md` before the session ends."

Half survives, half does not.

- README: survives, and in a better home — `spec/public-text-rules.md:45` [INV-44] re-checks the
  README's claims at every version push, and `skills/publish/SKILL.md:37,57` walks it.
- `SKILL.md`: the attribution line survives at `skills/publish/SKILL.md:81`.
- CHANGELOG: no surviving duty. `skills/communicator/references/writing-register.md:52` governs how
  an entry is *written*, never that a shipped change owes one. Repo-wide grep for CHANGELOG finds no
  other rule.

The rule's title still promises "docs travel with the change" while its body now names only the
spec, next-steps and plan — the internal documents. The shipped documents, which are the ones that
travel outward, dropped out. `.live-spec/escort-inventory-R7-2026-08-11.md:133` records the CHANGELOG
duty as "DERIVED — parent is rule 9's docs-travel clause, which is his", so the parent is the
owner's word and the child was cut without it.

**Replacement:**

> A shipped change carries its own CHANGELOG entry and re-walks the README against the pushed truth
> (SPEC INV-44).

### R31 — "the sender has hit a fault in that zone and carries the evidence"

The spec recognises three grounds for a message (`spec/agent-request.md:25` [INV-189, INV-197]);
the body now carries two. Blocked work is in the first bullet, the unowned concern is in the
pack's-inbox bullet, and the lived fault is gone. The body's bullet reads as an exclusive test — "A
message names the sender's own blocked work, in the message, or is never sent" — so a session
reading rule 31 refuses to send a message the spec entitles it to send.

The spec states the missing ground at `spec/agent-request.md:21`: "a lived-fault message *shall* name
the fault and the evidence the sender lived — what it ran, what happened, and how the fault showed
itself." [INV-189]

This one has an incident already on the record, in the guardrail's own source
(`guardrails/check-earned-message.py:128-130`): "corrected 2026-07-17 when the first real deposit — a
fault message from track-coach — was refused by a gate demanding blocked work of everything." The
body has just reintroduced, in prose, the exact refusal that gate was corrected for.

**Replacement:**

> A message names the ground that earned it — the sender's own blocked work, or a fault it lived in
> that zone carried with its evidence — or is never sent (SPEC INV-189).

---

## Genuine removal, an improvement (1)

### R7 — "or by walking the same steps by hand"

The old body let a session open a lane either by `scripts/open-lane.sh` or by hand. The script is
what reads the resolved cap and refuses a lane past it (`scripts/open-lane.sh`, SPEC INV-214). The
by-hand path was therefore a documented way to walk around the cap the same bullet declares. Naming
one road makes INV-214 binding. `spec/parallel-lanes.md:325` says the system "*shall* **offer** the
act as `scripts/open-lane.sh`" — offering one road does not forbid the body from choosing it as the
only one.

### Two clauses of the "No unprotected concurrency" bullet, judged with it above

- The nested-repo passage ("A repo nested inside another repo's own directory — a skill's own git
  clone living under this tree, for instance …") is an instance of the rule it sits under, not a
  rule. The pack's own rule of thinking — "Every incoming item is a symptom, and the answer owed is a
  rule about its class" — puts a worked instance in `references/`, not in the body. Cutting it from
  the body is right; it is in neither reference module, which is a thin loss of a teaching example
  and not of a rule.
- "Sequencing is the default; parallelism is the exception that states its own proof at brief-time."
  The second half survives verbatim in substance as the Brief-time disjointness bullet. The first
  half contradicted the bullet three lines above it ("Lanes roll unasked up to the profile cap") in
  the old file already, and is now stale against the owner's own live word of 2026-09-02 raising the
  cap to ten. Cutting a half-sentence that contradicted its own rule is an improvement.

---

## The prior case, already worked (F1, rule 10)

Not on the F2 list; recorded here because it sets the standard the rows above were judged by. Both
the old sentence and the new one misstate `spec/project-setup-tuning.md:249` [A-9], which is narrow:
*when adoption offers a cruft sweep*, list the file counts and sizes of regenerable junk and delete
only on the person's explicit approval. The old sentence generalised one station's rule into a
universal ban; the new one exempts regenerable junk from approval everywhere.

**Replacement:**

> Nothing is deleted silently: a superseded file goes to the attic with a manifest line, a removed
> feature gets a tombstone, and the adoption cruft sweep lists what it would delete and deletes only
> on the person's approval (SPEC INV-7, A-4, A-9).

---

## Claims in the previous review judged to be string-match artifacts

1. **R7 session identity** — "Rule 7 gives a session no way to mint the identity its own tie-break
   turns on." The bullet cites INV-117; `spec/parallel-lanes.md:54-55` states the exact recipe the
   review quotes as lost.
2. **R16 label forms** — the enumeration is `spec/draft-sandbox.md:11` under E-17, the code the rule
   itself cites.
3. **R31 field permission** — "only a permitted field leaves the tree" is the same rule stated
   positively.
4. **R36 never-infer** — "only when they show that depth themselves" carries the ban.
5. **R25 contradicts rule 13** — the review quotes the body without its qualifier "to understand or
   design it", then reasons from the shortened sentence. No contradiction exists, and the carve-out
   is at `spec/roles-and-agents.md:377`.
6. **R7 "the whole 'No unprotected concurrency' bullet"** — its operative clause is the Brief-time
   disjointness bullet; `spec/roles-and-agents.md:296` holds them as one clause.
7. **R5 tier mapping counted as a loss** — the mapping is at `spec/roles-and-agents.md:279` in
   vendor-neutral words, and the concrete tier is in the personal profile's `worker-tier` line. The
   grep for "haiku" and "sonnet" measured the model names, not the rule.
8. **"say in the record which clauses were dropped deliberately and why"** — that record already
   exists and the review did not look for it.
   `.live-spec/checkpoints/q809-inventory-base.md` enumerates, rule by rule, what was core and what
   was "rest", naming the very clauses the review lists — rule 9's shipped-doc list at line 132, rule
   7's nested-repo case in its rule-7 entry. F2's second fix is largely already done.

The review's own count stands at four of fifteen. Its accounting method — grep the body, grep
rule-origins, stop — cannot see a rule that moved to the spec under the code the body cites, which
is where most of these went.
