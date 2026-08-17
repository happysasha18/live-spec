# Adopt — Mid-flight adoption procedure

How to attach live-spec to an existing codebase — at the start or in the middle. This is the executable
projection of PRODUCT_SPEC.md "Entry mode 2: adopting a live project" (A-0…A-9). Follow the phases in order; each
has a clear done-state. Adoption never assumes a blank slate, and it **never deletes a host file** (INV-7).

**Routing:** this guide is the first adoption. A host that already adopted and needs to come up to a
newer pack goes to the catch-up walk instead — [MIGRATION.md](../MIGRATION.md) at the package root.
A tree with no code and no documents of its own is a founding, and it goes to
[START.md](START.md). The routing card at `skills/build-pipeline/references/project-setup.md` reads
the tree and picks among the three walks.

First proven on a real project (tlvphoto, 2026-07-04); the practical notes below are from that run.

## The canonical document set

The one normative list of the documents a live-spec host carries; every other guide points here
(SPEC INV-90). Adoption's Phase 3 produces this set; the catch-up walk re-homes facts into it.

- `PRODUCT_SPEC.md` — the living product spec, use-case-first, invariants underneath. A host that
  adopted under its own name (say `SPEC.md`) keeps it, recorded as one host-profile line
  (`spec.file: SPEC.md`); every pack guide reads "PRODUCT_SPEC.md" as that file.
- `ARCHITECTURE.md` — the named nodes and seams; every spec fact has an owning node.
- `TEST_MATRIX.md` — derived through the architecture, one pinned-level row per spec fact.
- `ROADMAP.md` — the queue; one wish, one row.
- `JOURNAL.md` — dated history with the why.
- `NEXT_STEPS.md` — the one resume file a cold session reads.
- `SURFACES.md` — or an equivalent executable gate test (E-10); doc form is the fallback.
- `attic/` with its manifest — superseded host files rest here, never deleted (INV-7).
- `.live-spec/` — the host's records: `profile.md` (host overrides), the installed-set record (M-7),
  `adopt/` (run artifacts and plans), `checkpoints/` (gitignored), and `agent.md` — the host's agent
  card, its self-description read by any neighbour agent's live scan: the host's name, mission, the
  zones it owns, the contracts it publishes with their paths, and its inbox address (SPEC E-32, INV-184).
  Writing the card is the declaration that this tree is an agent; a host adopting before this law writes
  its card at its catch-up walk, and the gate `guardrails/check-agent-card.py` reds a host tree carrying
  none (SPEC INV-219).

**One canonical state directory (SPEC INV-105).** Here the canonical state directory is named `.live-spec`, once, and no second directory competes for that role. A near-miss directory found at attach or resume is a red finding: `.livespec`, `.live_spec`, a bare `livespec/`, any look-alike carrying a rival profile. The sweep records it in `.live-spec/adopt/inventory.md`, then it is retired to the attic under a manifest line naming the path, the reason, and the canonical directory that absorbs it (INV-7, A-4). Never a look-alike left standing beside `.live-spec`.

**The package repo is read-only from a host session (SPEC INV-10).** An adopt run that discovers a live-spec
defect (a stale phase here, a template gap) does not edit the live-spec repo — it drops one new file into
live-spec's `inbox/` (see `inbox/README.md`) and records the finding in the host's own journal. Learned the
hard way: the pilot run edited live-spec directly while another session was mid-flight in the same repo.

---

## Phase 0 — Version-control gate first (SPEC A-5, done early for reversibility)

The spec requires version control before the first *landing* (INV-8). In practice, this happens **before
anything else is touched** — then the whole adopt run is reversible.

1. If the host has no git: `git init`.
2. Write a `.gitignore` that keeps source + structured data and excludes the virtualenv, caches, and heavy
   generated/media artifacts. (On the pilot this was ~7.6 GB of media out of a 7.7 GB tree — commit the
   ~source and exclude the exports.)
3. Make one **baseline commit** of the pristine original — this is the restore point and the diff baseline
   (SPEC A-6 / E-7).
4. **Settle the remote — a named deliverable (SPEC A-5).** By the first landing a
   remote (GitHub) either exists or the human has explicitly declined one; record the outcome in the run's
   journal entry. Creating/pushing the remote is the human's gate — offer and follow through, don't do it
   silently and don't let "recommended" quietly become "never happened" (the pilot ended local-only that way).
   Where a remote seat will reach this repo — a cloud session, a scheduled routine, another machine — the
   remote arm of the inbox door applies (SPEC INV-112). A remote seat reaches a repo only through git, so
   its deposit stays one new file in inbox/, committed touching inbox/ only with the source named, and then
   pushed under a per-repo grant: the owner links the Claude environment to the GitHub account once, and
   grants each repo to the app once, and the grant is recorded in the host profile like the push grant. A
   seat with no grant fails honestly — it names the grant it lacks and hands the owner the one action that
   supplies it. Script that ask with its exact settings path (see the grant-ask template, scripts/grant-ask.md).

Done when: the host is a git repo with a clean baseline commit, heavy artifacts are gitignored, and the
remote outcome (exists / declined) is recorded.

---

## Phase 0.5 — Optional cruft sweep (human-gated; SPEC A-9)

Writing the `.gitignore` usually surfaces pre-existing regenerable junk (caches, build leftovers, stale
exports). Offer one sweep: list what qualifies per group with its file count and total size, get the human's
explicit OK, delete only the approved regenerable junk. Never silent, never authored content — anything a human wrote
goes through the attic (INV-7) instead of this sweep. Skipping the offer is fine; deleting without the OK is not.

Done when: the sweep was offered and either declined or executed exactly as approved.

---

## Phase 1 — Orient: read everything first (SPEC A-1)

**Who am I working with (SPEC B-3) — the first breath of orient:** before any founding question
resolves, look for the human's personal profile (`~/.claude/live-spec/profile.md`). Found ⇒ load it
and say so — the file, plus any line ignored aloud (SPEC E-13). Absent ⇒ offer to create it from
`templates/profile.template.md`: the human tells about themselves and may name sources to read; every
line lands on their word, and a declined proposal is dropped. Declining the whole step runs the
session on package defaults, said aloud. A worker session never runs this step (SPEC ACT-3).

**Founding questions ride the orient (SPEC B-2 via A-1):** before the digest closes, the run asks —
or reads from the human's profile — the answers that shape everything downstream, personal-vs-reusable
first, and **what kind of project this is** — book · backend service · static site · fullstack app ·
CLI · skill pack · a custom kind — recorded as the host profile's `project.kind` line; that one is
always asked, never profile-read: no personal line can say what a host is (SPEC INV-36); an answer
inferred from examples is a defect. **With the kind, the founding declares this project's concrete
layers and its concrete proof kinds (SPEC INV-135):** the same host profile gains a `project.layers`
line (this kind's concrete footprint categories — a codebase's frontend/backend/store, a photo site's
content/rendering-engine/deployment, a campaign's message/channels/assets) and a `project.proofs` line
(this kind's concrete test-ladder rungs — tests and rendered checks, a byte-diff and an eye-walk, a
register lint and the owner's review). The stations are kind-abstract; these two lines are the project's
own fill, and a `project.kind` recorded with neither is incomplete, flagged the way an unbacked surface
is. The per-kind footprint-and-proof table in ARCHITECTURE.md is the scaffold each founding fills.
**A visual kind declares its design principles too (SPEC INV-136):** a founding that records a
frontend/visual kind gains a `project.design-principles` line — the pack's per-kind starter set from
the ARCHITECTURE per-kind design-principles table (the visitor walk, the feel pass scaled to a whole
site, motion/scroll feel, and the interactive-overlap rule) plus any the project adds — and a visual
`project.kind` recorded with none is flagged the way a kind with no layers or proofs is; the verify
feel pass runs these principles, the interactive-overlap rule's pixel/DOM row living in this project's
own suite. **With the kind, the founding also declares its composition axes (SPEC INV-244):** beyond
the kind-independent C-1 floor, the founding records the further axis set this project's kind owes
every surface — a visual kind's input-capability, say — as a `project.axes` line in the host profile,
filled from the per-kind axis table in ARCHITECTURE.md; a kind may declare **none beyond the floor** as
an explicit stated decision, and a `project.kind` recorded with no axis-set line at all is flagged the
way a kind with no layers or proofs is. **A deployed kind declares what its owner changes without a
build (SPEC INV-291):** a founding whose product runs somewhere its readers reach it records a
`project.config-surface` line naming the values the owner turns from outside a build — an experiment
switch, a piece of copy, a threshold or budget, a feature toggle — where those values live, and how a
change reaches production; behaviour and structure stay in the code the build ships. A project that
deploys nothing writes an explicit "none", and a `project.kind` recorded with no such line at all is
flagged the way a kind with no layers or proofs is. `guardrails/check-config-surface.py` reads the
host profile and reports both the silence and a "none" written beside a `project.layers` line that
names a deployment layer. **The founding records which version of the question set it answered (SPEC INV-227):** the
founding questions above are a set that grows as the pack learns what a founding host owes, its newest
member the agent card at `.live-spec/agent.md` (SPEC E-32). The host profile gains a `founding.set-version`
line carrying the current set version from `scripts/founding-questions.json`, so a later update check can
name any question added to the set after this host founded. A host that founded before the set was
versioned carries no such line, and the update check's founding arm reads that as owing every question.
The same breath asks — or tells the standing
default of — the economy rung (`budget.pressure`: full · lean · tight, SPEC T-19): the human hears the
choice at setup, before any crisis; the rung moves only on their word.

**Skill search rides the setup (SPEC INV-65):** with the founding questions answered, scan the
installed skills and the catalogs the run can reach for ones matching the project's kind and its crafts;
propose the fit list with a recommendation — the human's word picks. Later, any struggle (a ledger
entry seen twice, a taste artifact rejected twice) buys one search before the next attempt.

**The settings card closes the setup (SPEC INV-87):** when setup finishes, once the project's kind
and the working pace have been settled, the session renders the settings card with
`scripts/onboarding-card.py` and opens it for the human. It is one page showing what is set up and
what is theirs to change, and it asks nothing.

Read every existing document before writing or moving anything: README, any roadmap, any spec, any test
suite, journals, TODO/notes files, changelogs, in-repo wikis. **A well-run host may already keep most of
these in live-spec shape** — then adoption is light and adoption rewrites nothing.

Produce a **document digest** (`.live-spec/adopt/orient_digest.md` — all adopt working artifacts live in
`.live-spec/adopt/`, tracked in git as the run's audit trail, never in the host's own folders; SPEC A-8):
per doc — kind (spec/roadmap/journal/notes/report/…) · one-paragraph what-it-says · current or stale (and
why) · what it overlaps/duplicates.

> Delegate this read to a worker — it is fan-out fact-gathering. Judgment stays with the senior, who reads the digest.

Done when: every existing document has a digest entry.

---

## Phase 2 — Inventory the code & surfaces (SPEC A-2)

**Registry form (E-10):** when the host has a test harness, lift the surface inventory into an
executable completeness gate (or recognise an existing one — a declared surface map inside a gate test
satisfies E-10 outright); the `SURFACES.md` document is the fallback for doc-only hosts.

1. List every **user-facing output** (HTML, CLI output, API responses, rendered widgets, emails, consumed
   JSON).
2. List every **surface** (a page, panel, form, chart) and pin it to its owning `file:line` — this seeds the
   **surface registry** (`SURFACES.md`, SPEC E-10), which is self-closing: a surface that renders but
   isn't registered is red.
3. List every significant **data entity** (from filenames, JSON keys, class names, tables, config).

Record in `.live-spec/adopt/inventory.md` (one line per item; A-8 home), then lift the surfaces into
`SURFACES.md`.

Done when: the inventory exists and every surface in the registry has a real `file:line` (or is marked
`⟨DECIDE⟩`).

---

## Phase 3 — Re-engineer existing documents into live-spec shapes (SPEC A-3)

Turn what exists into the canonical set — **keeping original claims, marking them unverified**:
- an existing spec → `PRODUCT_SPEC.md` sections (entities / states & transitions / actors / invariants /
  cross-section composition / glossary); if the host's spec is already in this shape, **do not rewrite it** —
  just confirm structure and fill the two things hosts usually lack: the **surface registry** (Phase 2) and
  the **test matrix** (Phase 5).
- existing tests → matrix rows citing them at their real level.
- an existing roadmap/TODO → queue rows in `ROADMAP.md`.

**Provenance (SPEC C-1).** Mark each document `native-live-spec` (authored in the method) or
`re-engineered-from-existing`. A re-engineered claim is **unverified until reconciled** — pinned to
`file:line` or removed at the first landing that touches its surface, and all remaining ones at the first
milestone. A host authored entirely in the method (like the pilot) has no reconcile backlog beyond its own
`⟨DECIDE⟩` / `[planned]` markings.

**Unbacked live surfaces get a verdict (SPEC A-10).** Anything the inventory found that reaches the user
but has no spec backing — a de-facto prototype, the adopted host's most common residue — is flagged here,
and the human decides per surface: **promote** (it enters at the spec step as a feature, SPEC INV-16) ·
**quarantine** (moved into a prototype home and labelled, SPEC E-17) · **attic** (A-4). No unbacked
surface is silently registered as product.

Done when: the canonical doc set exists (SPEC/ROADMAP/JOURNAL/NEXT_STEPS + registry + matrix), every claim
is marked native or unverified, and every unbacked live surface carries its verdict.

---

## Phase 4 — Attic over deletion (SPEC A-4, INV-7)

Any document Phase 3 supersedes (an old spec, a stale resume, a folded notes file, a completed process
checkpoint) **moves to `attic/`** with a one-line manifest entry (original path · why · absorbing doc ·
date). Flat layout; on a basename collision the source dir prefixes the name; still taken → a numeric ordinal `-2`, `-3` (the pack's one collision law, base rule 18).

**The selection is a human gate.** These are the human's authored files in a live project — propose the attic
set with reasons and get an OK before moving. Moving is done with `git mv` (history preserved).

**Sweep the coupling.** After moving, fix any **live current-state pointer** in the kept docs that named a
moved file as canonical (e.g. a JOURNAL header "canonical state lives in X") — repoint it, or it becomes a
dead backpointer. Leave pure historical citations in dated entries (they resolve via the manifest).

Done when: superseded files are under `attic/` with a manifest, and no live pointer is dead.

---

## Phase 5 — Architecture, then the test matrix (SPEC A-3 tail, E-14/E-15)

**Pins are names first (E-14):** pin nodes to a named thing (function, marker, selector); the `:line`
is a cache. Wire the drift check (`guardrails/check-pin-drift.sh`) so a stale pin is reported, never
trusted.

**First the architecture.** Seed `ARCHITECTURE.md` from Phase 2's inventory: the surfaces' `file:line`
pins become named nodes (one responsibility, one name each — template: `ARCHITECTURE.template.md`), every
spec fact is assigned an owning node, seams are named. The pins are the reconciliation of re-engineered
claims (A-3) — they come from commands run in Phase 2, independent of the old docs' prose. Run a
product-prover pass with the architecture lens before deriving anything from it.

**Then derive `TEST_MATRIX.md` through it**: rows organized node × fact, at least one row per invariant /
transition / cross-section / surface, each pinned to a test **level** (string / DOM / browser / pixel —
extend with `data` for a data pipeline). Every row states both sides — what the fact does and what it must
never do (the negative is the regression fence). Visibility/layout facts get level ≥ browser. The
derivation closes with the mechanical row lint and the matrix's generated reference section, which
replaced the hand-walked checklist at queue row 477 (SPEC INV-274). If the host has no
suite yet, all rows are `TODO` — the data/invariant rows become the acceptance criteria for the next
build sprint.

Done when: `ARCHITECTURE.md` exists with every spec fact owned (prover-lensed), and `TEST_MATRIX.md` has
≥ 1 row per spec invariant under its owning node, each with a level, all `TODO` (or better).

---

## Installing the gates (SPEC INV-97, INV-172, INV-173)

**First attach the four project-side checks, in one command (SPEC INV-97).** From the host root:
`bash <pack>/adopt/install-scaffold.sh`. The four checks are the pipeline's mechanical teeth as code a
host runs, never prose it re-implements — **completeness** (a registered surface is absent, empty,
or rendered-but-unregistered), **tests-present** (a user-facing change with no test beside it),
**behaviour-traces-to-spec** (a registry row citing no anchor or a dead one), and **conflicts**
(duplicate anchors, an indexed invariant no matrix row cites, a resolved line still marked to decide).
The installer vendors the four checks and their shared library into the host's `guardrails/`, seeds
`guardrails.config.json` from the example where the host carries none (a filled config is never
clobbered), and writes or merges the host's source pins into `scripts/ratchet-manifest.json` — pack
version plus content hash per check — so the daily update check reads this kit too (SPEC INV-177). The
remaining manual steps the installer prints: fill the real paths in the config, run each check once,
prove one red-first (plant a fake registry row, watch `check_completeness.py` red, remove it), and add
the four check lines to the host's pre-push hook. Config-only attach runs about fifteen minutes.

**Then wire the ratchet gates, seeded at the host's current size (SPEC INV-172).** One pass, from the
host root: `bash <pack>/adopt/install-ratchet.sh [--tier universal] [DOC...]`. It vendors the style
lint, the redundancy precheck, the freeze tool, and their shared library into the host's tree (each
copy pinned in `scripts/ratchet-manifest.json` — pack version + content hash, so the update check can
tell current from stale), measures the host's gated docs as they stand today, writes the debt caps at
those counts, and generates `tests/test_ratchet_lock.py`. The gate is green the moment it lands — no
re-compaction is demanded — and from then on the debt may only hold or shrink; raising a cap demands
editing the guard test, deliberate and visible. Wire the printed gate line into the host's pre-push.
Prove it red-first the way the four project-side checks are proven: plant one register defect in a
gated doc, watch the lock test red, remove it. The universal tier binds every host; the full
pack-register tier is the host's own opt-in (SPEC INV-166). The same pass runs the pack's current gate
set backward over the host's existing tree — every gate scans the whole tree, retroactive by
construction (SPEC INV-176), so debt older than the gate surfaces now, at adoption, well before the next touch.

**And install the universal hooks (SPEC INV-173):** `bash <pack>/scripts/install-pack-hooks.sh` puts
the pack's canonical scan hook onto the machine and wires it; personal patterns stay in the personal
layer's own overlay file, which the installer never touches.

---

## Phase 6 — Attach record & incremental from here (SPEC A-7)

1. Record installed skill versions in `.live-spec/` (every pack SKILL.md carries a version line under
   `metadata:` in its frontmatter and the package a root `VERSION` file — SPEC M-7) and seed
   `.live-spec/profile.md` — the host's overrides
   only; settings about the human (language, proactivity) belong in their personal profile
   (`~/.claude/live-spec/profile.md`), which this host file overrides per the settings ladder (SPEC E-13).
   Mode/trust set only on the human's word (INV-9).
2. Write the run's JOURNAL entry (what landed · why · provenance · the remote outcome (exists/declined) ·
   any findings held for the human).
3. The host is now on the standard pipeline: every new wish enters at intake and flows
   `spec → prove → architecture → prove architecture → matrix → test → code → verify → commit & show`.

**First recommended action after adoption:** run `product-prover` on the whole spec to catch what the
reverse-spec pass missed — unless the spec was prover-proven recently, with no drift since, and by the
same prover version as the one installed now (the record names the version that ran). A prover that grew
a lens since that record re-arms the full pass: a spec proven under the old lens set has not met the new
lens — that is exactly how a whole class of composition holes once kept a stale green (2026-07-09).
