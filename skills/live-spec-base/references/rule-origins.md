# Rule origins

The instructions live in [../SKILL.md](../SKILL.md). This file holds only their background — a
dated citation, the history of how a rule arose, its justification, or its worked example — never
a rule restated in words of its own. Open it only to dispute or amend a rule; the body never needs
it to be followed. A rule with no background beyond its own words carries no entry here.

---

### 2. Plain words carry the meaning; the code trails, quietly

Citation (2026-07-05): a calque reads as machine-speak and degrades the product — the finding that
gave the rule its name. Worked example of the anchor convention: "no remote copy exists (INV-8)" in
chat, `[INV-8]` in a document.

### 3. One surface = one name, everywhere

Justification: the moment one thing answers to two names, every cross-check silently loses the
seam between them — the vocabulary itself comes from the host's SPEC, so a second name for the
same surface is always avoidable.

### 4. One canonical home per fact

Justification: two documents claiming authority over one fact is undefined behaviour the moment
they disagree — the reason a second home is never tolerated even briefly.

### 7. The concurrent-edit fence, before every write and every commit

History: this class of self-collision — two writers running unprotected on the same physical tree
— has cost real token spend more than once, on the owner's own account of past sessions.

Citation (2026-08-08), role-profile sub-rule: a blind A/B in tlvphotos gave the same mechanical
task to two identical-tier workers — one briefed with a short (~25-line) role profile (a craftsman
identity, the project's own design charter as sole naming source, causal chains for each rule, an
escalation interdict for taste questions) plus the charter, the other in plain engineering words.
Neither knew of the other, and a third, fresh agent judged the two patches unlabeled. The profiled
arm won on all three pre-registered criteria: vocabulary fidelity, truth of the documentation it
wrote, and integration quality. Full record: `inbox/handled/2026-08-08-profile-briefed-worker-ab-result.md` (harvested from
PLAN.md's Blockers 2026-09-03).

### 9. History lives in the journal; docs travel with the change

Citation (2026-07-05): a record is answerable later — "yesterday evening you wrote X, so I did Y"
— only when it kept the time of day beside the date, which is why entries and harvested records
carry both. A decision file's answered-at stamp and a journal entry's opening timestamp follow the
same reasoning.

### 13. A claim needs its primary source

Justification: a text gate alone cannot catch a fabrication that carries a plausible date — an
invented ranking invents its date just as easily — so the read-back on the touchpoint cadence
[INV-205, INV-206] is the load-bearing defence, turning the person's own eye into the check.
`guardrails/check-authority-anchor.py` hard-blocks an unanchored entry on a decision record, and,
outside the project's history and archive directories, a sentence crediting a person named in
`guardrails/authority-anchor.json` with a decision that names no date; its own opening lists what
it leaves out — the dated records, the journal, the archives, the fixtures, the working notes —
each of them narrating what already happened.

History (2026-07-27): a window told the person that launching workers without their ask was
forbidden. The line had come from the session's own instructions, the person had never said it,
and their standing word was the opposite — multi-agent by default. That window dropped delegation
for a whole movement, shaping its method around a rule nobody had given it. The incident is why a
line is named down to person's-word, tooling's-default, or unknown, and why a conflict between them
resolves toward the person's own standing word.

### 17. Irreversible means gone, not merely public

Citation (2026-07-05): the criterion is "can we get back to before, ourselves, losing nothing?" —
money yes, deletion yes, a push no.

### 22. Every process converges on its goal

Worked example: a reached level locks by one of four mechanisms — a norm template, a conformance
test, a lint floor that only grows, or a cap that only ratchets down.

History: the pack's own first teeth for the rule were the norm-conformance rows and the
convergence-lock tests (rows 216/217).

Citation (playbook, "Truth & sourcing", 2026-06-21 s14), the rendered-output trigger: "'What's the
point? / what a mess?' means stop coding and read the rendered data... The bug is usually the
accumulation, not the latest diff." Twice in one playbook session this turned a cosmetic rename
into the real fix — an empty-artifact card that should not fire, and a three-system label where the
headline was worse than trusting the input. Migrated from the retiring playbook document per
PLAN.md's Blockers finding (31.08, q-800; closed 03.09) — a related trigger this rule borrows for
its own convergence case, not itself part of the playbook's convergence chapter.

### 24. The process stations are kind-abstract; a project declares its concrete layers and proofs

Its worked cases live together in [worked-examples.md](worked-examples.md), the one home the
rule's own line points at.

### 25. The seat reads to decide; discovery reads go to workers

Justification: the leanness is load-bearing — a seat filling its context with source it could have
had distilled loses the room to hold the whole arc, and its judgment degrades as the context
bloats.

### 26. A project kind also declares design principles the verify pass runs

Worked example: the frontend kind's interactive-overlap rule and its legibility floor are two such
principles. Citation: this rule is the base home the design-principles invariants own; their full
statement, the per-kind table, and its starter sets live in `ARCHITECTURE.md`.

### 27. The seat decides what it can decide, and surfaces only what it cannot

Justification: this rule is where the human-only list is defined once; every other rule that needs
it points back here rather than repeating it. An act irreversible outside git still stops for the
person under rule 17, whatever this rule would otherwise allow.

### 29. A deferral must justify itself, or the item is the seat's to do

Justification: the pipeline's closed-door set is this rule's twin [INV-151], both instances of one
routing principle — a thing that pins to no home is itself the finding.

Citation: two mechanisms hold it — `guardrails/check-deferral-marker.py` reds a commit where a
parked item names none of the four grounds, and the deferral line of `hooks/chat-law-hook.sh`
re-fires the moment a marker is written or a question is opened, reminding without blocking.

### 31. Agents talk on exactly two channels, and a message earns its passage

Justification: several agents on one person's projects generate noise the moment they can talk to
each other; the two-channel design keeps that channel quiet while the one thing that must cross
still does.

Worked example: the human-decision withdrawal loop already takes the two-crossing shape [INV-196,
INV-130]. A wrong referral loops back over the same pair without the two-crossing cap absorbing it
[INV-225].

### 36. Who the person is, by default, and what changes that

History (2026-08-27): a plan file had been given executable commands nobody asked for; the cost of
that unrequested machinery then surfaced as a question put to its owner — the incident this rule's
closing clause answers, since a default the person did not choose is not theirs to be quizzed about
later.

### 37. Every plan names what it must not touch

Citation (playbook, 2026-06-20, `PLAYBOOK.md` "Plan first"): "Every plan names the components I
must not touch... This rule exists because I kept breaking working things by editing more than I
was asked to. That is the cardinal sin here." Migrated from the retiring playbook document per
PLAN.md's Blockers finding (31.08, q-800; closed 03.09) — the other piece plan-16 (31.08) left
unmoved when it gave every other rule of the pack one home.

## Rule 38 — the shape of a reply, and the order the rows are printed in

Entered 2026-09-04 on the pack's own repository, after a session opened three replies in a row with
the row list retyped and reordered to suit the sentence that followed, and after the owner read a
board where the row being edited stood last while nothing was working the rows above it. He asked
for the order to be written down rather than explained to him. The correction that followed the
first draft is part of the rule: several rows stand in hand at once whenever lanes run in parallel,
so a single "next" is a claim the list should not make. The clause allowing a cluster name before a
colon replaced a proposal to add sections to the board — sections are machinery, and a name everyone
in the project already uses is not.

## Rule 36 — who the person is

Sharpened 2026-09-04. The rule had said a session should write for a non-technical reader and deepen
the register when that reader showed depth. Three things were missing, and each had cost the owner a
complaint the same night: who the reader actually is (the one who commissioned the work, riding
rather than driving), that a project's README names who its PRODUCT is for and never who the session
is speaking to, and that a result is reported flat — the connective phrases that grade the work while
reporting it read as a person covering themselves.

## Rule 39 — nothing new is built to serve the process itself

Entered 2026-09-04, and it is the oldest of the owner's own standing rules to reach this file: he had
said it nine times across two weeks before it was written down anywhere the pack could read. The
night it entered, this tree had just answered a failing check by widening it — a spec criterion added
so a promise with no owner could pass a gate that existed to catch exactly that. The rule names that
move as the same failure as inventing a threshold: both add machinery to explain away a fact rather
than change the fact. Its "downwards only" clause comes from the same source, and from a year of
thresholds that grew every time work pressed against them.

## Rule 40 — the person is the client, and checking the work is never their job

Entered 2026-09-04, on the owner's own word the same night. It settles a habit rules 12 and 27 had
left half-settled: work would finish, be shown, and then sit waiting for him to look at it, with a
row held open on his attention and a running tally of what he had yet to read. He named that tally
for what it is — a way of asking again — and the pressure it puts on him is what the rule removes.

The rule's first half is a demand on the session rather than a relief for him: taking a piece of
work means knowing how it will be checked, so a session that cannot say how it would prove its own
result has not understood the task well enough to have taken it. The client's judgement is whether
the work was worth doing; whether it works is the pack's own job.

Two things still stop, and the rule names only those two: an act that cannot be undone outside git
waits for his word before it runs, and a fork whose answer is a taste or a policy is put to him as a
question while the rest of the work keeps moving.
