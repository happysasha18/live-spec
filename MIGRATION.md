# MIGRATION — the catch-up walk

This is the operating guide for the catch-up walk: the procedure an already-adopted host's own session runs to bring the host's documents and records onto the current package version. A package release that owes its hosts actions lands one dated chapter at the end of this file; the walk reads the chapter chain and applies it under the owner's gate, preserving every recorded fact. Nothing outside a host's own session ever writes that host's repo (INV-10).

The bracketed codes on this page — `INV-10`, `A-11`, `E-32` and the rest — name rules in `PRODUCT_SPEC.md`. `PRODUCT_SPEC.index.md` gives each code's location in that document. A feature code such as `F-catchup` carries no index row and sits on its requirement's heading.

The walk is the executable projection of Requirement 180 in `PRODUCT_SPEC.md`, "The catch-up sequence brings an adopted host onto the current pack". Its codes are F-catchup, A-11, and INV-89 through INV-92. The spec states the facts; this guide states the moves.

## When to run this

The ask arrives in any wording. It might read "re-layout the documentation" or "catch up to the current pack"; it names no procedure, so the package names one, and that procedure is this walk.

Route the ask before doing anything else. A host that never adopted the pack goes to adoption (`adopt/ADOPT.md`) for the first-adoption phases. A host that already adopted goes to this catch-up walk. A single-document edit belongs to the ordinary docs-only door, which `skills/build-pipeline/SKILL.md` states. A restructure of the host's own product is the host's own queue row through the build pipeline. This walk fires only to move an adopted host's own live-spec documents and records onto a newer package version. The catch-up walk fires only when the host's recorded package version is behind the current package VERSION. A docs restructure that carries no version delta is the host's own queue row through its pipeline, whatever wording the ask used. The trigger wordings are examples under this test. A wording never decides the routing; the version delta decides. (INV-110)

## The walk

The walk runs four phases in order (A-11). Its plan and its working artifacts live in the host's `.live-spec/adopt/` through the whole walk, tracked in git as the run's audit trail.

## Phase 1 — orient on the delta

1. Read the host's installed-set record, which sits in the host's `.live-spec/` directory (SPEC M-7), and the tree as found.
2. Read the package's current `VERSION` and journal, and the migration chapters below.
3. Build the work list: the ordered chain of migration chapters from the host's recorded package version to the current one (see "Migration chapters"), plus any drift the tree shows against what those chapters expect. A record that carries no readable package version — commit pins, or no record at all — starts the chain at the earliest chapter; every step's already-done check makes over-application harmless (INV-89).
4. Treat every precondition written in this guide as a claim to check against the tree. Where a written precondition and the tree disagree, the tree is the truth.
5. Name the founding questions this host has never answered: read the host profile at `.live-spec/profile.md` for its `founding.set-version`, against the current set in `scripts/founding-questions.json`, and list each question added after the host's recorded version — the agent card at `.live-spec/agent.md` (SPEC E-32) among them for a host that founded before it. A host with no `founding.set-version` line founded before the set was versioned and owes every question. Each gap rides the plan for the owner to answer, and the walk records the current set version once answered; a never-answered question is surfaced for the owner, answered on no one's behalf (SPEC INV-227, the duty binds forward INV-159).

## Phase 2 — plan, behind the owner's gate

Write one plan document into the host's `.live-spec/adopt/`, where it lives through the whole walk. It lists every file that moves, merges, or retires, every record that reformats, every rename offered, and every open conflict. It names the baseline commit of Phase 3 as the walk's restore point and states the one restore command that returns the host to the pre-walk state.

The owner's word on the plan comes before any file moves. A walk that finds nothing to do reports that and ends. No file is touched until the plan is approved.

## Phase 3 — execute, preserving facts

1. Open with a clean-tree baseline commit in the host (A-5). This commit is the restore point named in the plan; the whole walk stays reversible to it by the single restore command.
2. Record the pre-walk inventory beside the plan, before any file moves. "The before-and-after self-test" below states what that inventory holds.
3. Run under the checkpoint discipline. The walk's checkpoint names the plan document and the per-step state. An interrupted walk resumes from the checkpoint under the already-given gate — the owner is not asked twice.
4. Apply each step under the half-done-state law and the preserve-and-re-home law (see "Step laws"). A step reads its precondition from the tree at the moment it runs, so a walk resumed after a partial application does the right thing on what it finds.

## Phase 4 — verify and re-record

1. Run the pack's current gate set backward over the host's existing tree. That set is the chain
   the host's `.git/hooks/pre-push` runs. Every gate scans the whole tree, retroactive by
   construction (SPEC INV-176). A gate the pack gained since the host adopted finds the older debt
   now. An oversized backlog is carried as named waivers, one per finding with its own expiry,
   never absorbed into a cap seeded at the tree's current size (SPEC INV-172).
2. Run the host's own gates, including the test suite where one exists. A red gate is the walk's own open defect: the walk stays open until the gates read green, and the checkpoint carries the red state across sessions.
3. Re-record the installed-set record in the current format.
4. Land one journal chapter in the host: what moved, why, the provenance, and any finding held for the owner.
5. Run the before-and-after self-test below and clear it before the walk is called done.

The plan document and the superseded files rest in the attic and the adopt records. The walk changes documents and records only, and it creates no visible product surface. So the plan opens by the ordinary show rule (SPEC glossary): a new browser window on a local seat, its own channel on a remote seat.

### The before-and-after self-test (INV-92)

Before any file moves, in Phase 3, record a pre-walk inventory beside the plan in `.live-spec/adopt/`: every document with a content fingerprint, the host spec's anchor multiset, and the test suite's verdict and count as found.

After the execute phase, record the same inventory again and compare the two. Every difference must be accounted for by a plan item — a file is unchanged, re-homed to a named new path, merged from named sources, or resting in the attic under its manifest line; an anchor-multiset delta must match a change the plan names; and the suite reads at least as green as before. A difference outside the plan blocks the verify phase until the owner's gate accepts it as a plan amendment or the step is reverted.

The baseline commit is the walk's restore point: the plan names that commit and states the one restore command that returns the host to the pre-walk state. The attic keeps every superseded file readable without any restore.

## Step laws

### The half-done-state law (INV-89)

Every catch-up step reads its precondition from the tree before it acts. A step whose end state already holds is reported done and skipped. A step that finds both the old and the new form present merges file by file:

- A file with identical content on both sides drops the old copy to the attic.
- A profile file with differing content reconciles by the settings ladder: a line whose home sits at a machine-shared scope moves up, and a host-scoped line stays. A move up writes a machine-shared file, so it re-reads that file immediately before appending (the promotion law).
- Any other differing file, and any remaining conflict, rides the plan to the owner's gate.

Across all of this, never nest the old directory inside the new one, and never overwrite the new form with the old. The case this law was born from: `.livespec/` and `.live-spec/` both exist in a host that started the rename and stopped — the walk merges them and overwrites neither.

An installed-set record kept in an outdated format, such as commit pins, retires to the attic. The new record is read from the version lines of the skills actually installed on the machine and from the package `VERSION`. The skills on disk are the authoritative set; a stale record is corrected from them.

### The preserve-and-re-home law (INV-90)

The host's recorded facts survive the walk. Content moves into the current shapes, and a fact leaves its home only by moving to a better one. Settled prose is rewritten only where the owner rejected it or where the new shape cannot hold it as written; the plan carries each proposed rewrite and the gate decides.

A host that adopted under its own names keeps them. A product spec named `SPEC.md` stays `SPEC.md`, recorded as one host-profile line, `spec.file: SPEC.md`; the package's guides read "PRODUCT_SPEC.md" as whatever file that line names. The plan may offer the rename together with its pointer sweep, and the gate decides. The canonical document set and names live in one list in `adopt/ADOPT.md`; this guide points there and holds no second copy.

Stray state files re-home. A checkpoint file at the repo root moves to `.live-spec/checkpoints/`, a closed one to the attic, and a look-alike state directory merges under the half-done-state law.

## Pair routing

The walk covers exactly one host. When the ask arrives at one window of an engine-and-instance pair and means both halves, the window executes its own repo's walk and files one inbox wish naming the other half's catch-up debt (INV-86) — it never writes the other repo.

A pair half that carries no `.live-spec` records of its own is an under-attached host. Its walk opens with the full adoption run for that repo (`adopt/ADOPT.md`) before the catch-up items — the walk runs the full adoption for that repo first, then catches it up.

A Phase-4 gate that reads red only because the other half's own catch-up has not landed keeps the walk open exactly as any red does: the checkpoint carries the state across sessions, and the block rides the host's status reports as a dated blocked-on-the-other-half line under the pair law (INV-56, INV-27) until the other half's session lands its walk.

## Machine-level steps

Some steps touch the machine's shared homes — the installed-skills folder and the personal profile. They run once per machine, and every host on it shares the result. Each such step states its already-done check: the directory that already exists, or the record that already reads current. A step whose check passes is reported done and skipped, exactly as under the half-done-state law.

## Migration chapters

A package release that changes something hosts must act on lands one dated, versioned chapter here, stating the host-side steps. A release owing nothing adds no chapter and says so in its changelog. Orient reads the host's recorded package version, and the work list is the chain of chapters from that version to the current one, walked oldest first, one plan carrying the whole chain however far behind the host is.

### 1.0.0 — 2026-07-10

This chapter absorbs the 2026-07-05 package rename (livespec → live-spec, one name everywhere) and the same wave's matrix reshape, restated so each step is safe on a half-done tree.

1. Rename the host's pack folder `.livespec/` → `.live-spec/`. If only the old name exists, rename it preserving history. If both exist, merge file by file under the half-done-state law. Never nest the old directory inside the new one, never overwrite the new form with the old. If only the new name exists, the step is done and skipped.
2. Sweep the host's own docs for `livespec` references (spec, roadmap, and journal pointers to the pack; skill names in running text) → `live-spec`. The host's journal history entries stay as written.
3. Re-record the installed set. The base skill is now named `live-spec-base`. A commit-pin record retires to the attic; the new record is read from the version lines of the skills actually installed and the package `VERSION`.
4. Update the git remote URL at leisure (`git remote set-url … live-spec.git`). The GitHub redirect keeps old clone and remote URLs working meanwhile, so this step blocks nothing.
5. Once-per-machine moves, each with its already-done check: `~/.claude/livespec/` → `~/.claude/live-spec/` (skip if the target already exists), and `~/.claude/skills/livespec-base` → `~/.claude/skills/live-spec-base` (skip if the target already exists). Sweep the machine-global loader file (`~/.claude/CLAUDE.md`, E-16) for old-name pointers the same once — already-done check: the file reads current.
6. Matrix reshape. A host holding an old-shape flat matrix regroups its rows under the architecture nodes at its first architecture landing — rows are preserved and re-homed, never re-derived from scratch.

### 2.0.0 — 2026-07-16

**Host action: none.** The 2.0.0 major is a readability and compaction pass over the pack's own living
documents (the spec, architecture, matrix, roadmap, and skill docs read plainly and stay compact), plus
the machinery that keeps them that way. It changes no runtime behaviour, no skill interface, no file the
host writes, and no adoption or catch-up step. A host adopts it the ordinary way — pull the pack, run
`scripts/sync-skills.sh` — and owes nothing further.

The major number marks two things a host inherits automatically by adopting, and it breaks nothing:

1. **The compaction ratchet on the host's own push gate.** A host that runs the pack's guardrails now
   carries the reached-clean floor: the register lint at zero, no stale waiver left standing, the debt
   cap at zero for both (`scripts/spec-debt-cap.json`), and the compaction freeze
   (`guardrails/check-freeze.sh`, pre-push gate k, which skips itself where no local baseline exists). A
   host's documents can get cleaner from here, never worse — the recurrence-stop for document bloat.
   *(2026-09-02 note: this chapter shipped a third floor beside those, a per-document ceiling on
   near-duplicate sentence pairs seeded at whatever each document last measured. It was cut on the
   owner's word, with every gate of that shape. The near-duplicate reading itself stays, as a
   measurement a person reads. A host that carries the old `max_redundancy_open` key may delete it.)*
2. **The method rule (SPEC INV-164): a quality a machine can verify is enforced by a gate**, held by
   no pass's attention; compaction runs at every push, above the milestone whole-read. *(2026-08-13
   note: the numbered rulebook slot that once carried this rule was cut whole on 2026-08-12 and its
   number stays an open hole; the law itself is gate-held and stands. A host that still carries the
   numbered rule follows the 5.0.0 chapter.)*

No host file changes, so the catch-up walk records this chapter as done on read.

### 2.7.0 — 2026-07-18

**Host action: re-run the catch-up walk.** The 2.7.0 minor grows what a host may adopt — new laws,
new push gates, new capabilities — all backward-compatible: nothing a host already carries is reworded
in a breaking way, no surface a host depends on is renamed or removed, and no earlier adoption step
changes. A host takes the release the ordinary way: pull the pack, run `scripts/sync-skills.sh`, and
run the catch-up walk above (INV-91), which re-vendors the pack files, runs the current gate set
backward over the host's tree (INV-176), names the older debt the new gates surface so it can be fixed
or waived one finding at a time (INV-172), and rides the new founding questions to the owner. The tier is MINOR by rule 32 /
SPEC INV-217: the host re-runs its walk and rewrites nothing it holds. What the walk brings in, grouped:

1. **Register enforcement gains a model above the literal list (INV-203; INV-83 retracted its growth duty).**
   The pack's register nets — the pre-show register gate and the Stop-hook chat scan — gain a
   class-reading judge above the literal-pattern list. The list stays the free, deterministic first
   pass; the judge is opt-in (`PRESHOW_REGISTER_JUDGE`), off by default, and never makes a green run
   non-deterministic. INV-83's old "the set grows by one per caught leak" duty is retracted — a host
   that vendored it drops the duty; there is nothing to do.

2. **New push gates in the chain (each retroactive over the host's tree, absorbed by re-seeding caps).**
   Gate o cleanup-notice (INV-204), gate p touchpoint-kind (INV-205), gate q waiting-list (INV-206),
   gate r authority-anchor (INV-207), gate s skill-review (INV-208), gate t doc-rotation (INV-209),
   gate u CI-mirror parity (INV-210), gate v judges-listed (INV-211), gate w every-gate-can-fail
   (INV-212), gate x index-prose (INV-218), gate y agent-card (INV-219), and gate z doc-bound
   (INV-234). Every gate carries a known-red proof and a CI mirror (or a declared carve-out).

3. **The pack's gate-chain integrity, made self-checking (INV-210, INV-211, INV-212).** Every local
   push gate is mirrored in CI or a named carve-out (gate u); every wired chat judge is referenced in
   the installed settings (gate v); every gate in the chain carries a proof that it can actually red
   (gate w). A host inherits the same self-checks over its own chain.

4. **Working-doc rotation and size bounds (INV-209, INV-233, INV-234).** The pack's append-only working
   documents split and rotate into dated archives so the live file stays small; nothing is lost (every
   rotated row is findable in its archive, every archive named in a manifest line — gate t), and each
   growable doc stays within its declared bound or is freshly rotated (gate z). A node that grows past
   its file cap is the node-growth law's concern (INV-233).

5. **The far tier of the queue (INV-222, INV-223).** The queue gains `far` beside `deferred` — kept, no
   revisit trigger — and the what's-left report and feature map stand it down by name, with a rare
   self-surfacing line at the `far-tier.surface-cadence` default: at most one offer every fourteen days.

6. **The touchpoint frame, the waiting list, and the read-back (INV-205, INV-206, INV-207).** Every
   point of contact with the person has a kind, synchronous or asynchronous, and the kind licenses what
   may be said there (INV-205); everything waiting for the person's eyes has a home that outlives the
   scroll (INV-206); and a decision recorded as the person's names its exchange, so the pack shows the
   person what it believes they decided and they strike what they never said (INV-207).

7. **The lane-open act (INV-214).** The parallel-lane law gains the act that opens a lane — a branch in
   its own worktree cut from the claim commit, integration taking the pen — so a granted lane actually
   runs. The lane cap is re-homed from the spec text to the personal profile.

8. **Worker-teardown reap and the runaway-child notice (INV-213, INV-230).** A finished worker leaves no
   runaway child: teardown reaps the owned process group, and the cleanup names what it ended.

9. **The reach classes as host config (INV-224).** The reach map's directory classes move from the
   `check-push-reach.sh` body into `guardrails.config.json` under `reach_classes`, the pack's values
   shipped as the default. A host adopts via its own declared layers; the default reproduces every
   existing reach verdict, and a missing or empty config can only over-run scope, never false-green it.

10. **Versioned founding questions (INV-227) and the agent card (INV-219, gate y).** The founding-question
    set carries a version; the catch-up walk reads the host's `founding.set-version` and rides each
    question added since — the agent card at `.live-spec/agent.md` among them for a host that founded
    before it. A host with no `founding.set-version` owes every question, each surfaced for the owner
    and answered on no one's behalf. This is the walk's own designed mechanism; the host answers at its
    gate, nothing is auto-decided.

11. **The release-tier rule itself (INV-217, rule 32).** A release's number now reports what taking it
    costs a host — nothing (patch), re-run the walk (minor), or a migration (major) — a stated judgment
    the releasing session makes and names, held by no gate. This 2.7.0 chapter is that rule applied to
    its own release.

Smaller laws ride in the same walk: the answer-first arm and no-dramatization (INV-215 and the pack
law), the wrong-referral naming (INV-225), the release-note offers section (INV-228), the parked-question
default (INV-229), the listener tripwire and remote-read grant (INV-231, INV-232), the net-liveness meter
(INV-202), an expensive decision's adversarial read (INV-235), and the traffic-kind transport split
(INV-236). None reword a rule a host holds; all are adopted by re-running the walk.

### 2.8.0 — 2026-07-18

**Host action: re-run the catch-up walk.** The 2.8.0 minor adds one law, backward-compatible: nothing a
host holds is reworded in a breaking way, no surface is renamed or removed, no earlier adoption step
changes. A host takes it the ordinary way — pull the pack, run `scripts/sync-skills.sh`, and re-run the
catch-up walk (INV-91). The tier is MINOR by rule 32 / SPEC INV-217: the host re-runs its walk and
rewrites nothing it holds.

1. **The authoring seat does not adversarially certify its own work (INV-237; base rule 33).** A
   release's adversarial pass — the full re-prove at the release gate — is now authored by a fresh seat,
   never the seat that authored the change, and a newly added lens or rule is run against the very
   document that introduces it before release (self-application), the release record naming the result.
   This generalizes the fresh-context freshness the verify audit already demands (INV-46) to the release
   pass itself, after the 2.7.0 release ran its adversarial pass in the context that authored its new
   lenses and so missed a self-referential miscount a fresh review caught. A host adopts nothing
   mechanical: the law is a review discipline carried in the pack's own text, with an optional release
   gate that checks a dated clean-context review record exists and names a different seat. Nothing a host
   vendored is reworded.

### 3.0.0 — 2026-07-20

**Superseded by 4.0.0. A host whose chain reaches 4.0.0 skips this chapter.** The 4.0.0 conversion
retired the `Description` column and the gate below with it. `guardrails/description-field.json` reads
`armed: false` today. `PRODUCT_SPEC.index.md` carries `| Code | Location |` alone. Running this
chapter first would author descriptions the next chapter deletes. A host whose chain stops at 3.0.0
runs it as written.

**Host action: run a migration.** The 3.0.0 major back-describes the Formal index. The index table gains
a permanent `Description` column, and every registered code — `INV`, `E`, `T`, `A`, `M`, `ACT`, `B`, `C`, `D`, `S` — carries
a plain one-sentence human-clear description of what it does and the problem it solves. This is the
one-pass migration INV-239 and INV-217 named: the description field's one home, filled once for the whole
existing code set, arming the field gate that until now shipped dormant. The tier is MAJOR by rule 32 /
SPEC INV-217 because a host does real authoring work its own session must run: a host back-describes its
own registered codes, work no walk can re-run blind.

1. **The Formal index gains a `Description` column (E-35, INV-239).** The header moves from
   `| Anchor | One line | Section |` to `| Anchor | One line | Description | Section |`; the terse `One line` stays the machine handle's home,
   and the new `Description` column is the plain human-clear line a person and a second agent read. Every
   code's description says what the item does and the problem it solves; where the rule governs a class,
   it names the class and gives a representative handful of members inline, standing in for the exhaustive
   list (the owner's accepted form, 2026-07-20). The English description is canonical and translated in real
   time for another language (INV-83).

2. **The field gate arms (M-421, INV-239).** `guardrails/description-field.json` flips to `armed: true`
   in this same landing, so `guardrails/check-description-field.py` now reds any registered code whose
   description field is empty. It judges presence alone; whether a description reads well or matches its
   code is the human sampling net (INV-41), never the machine's. The gate rides the suite and takes no
   push-gate letter.

3. **The spec's byte ceiling rises (INV-234).** The permanent Description column takes the spec from
   about 642 kilobytes to about 736. So `guardrails/doc-bounds.json` raises PRODUCT_SPEC.md's ceiling
   to 840,000 bytes with a recorded reason, above the new live size with rotation headroom.

**How a host takes it.** Pull the pack, run `scripts/sync-skills.sh`, and re-run the catch-up walk
(INV-91). For this chapter the walk back-describes the host's own registered codes to the same quality
bar, adds the `Description` column to the host's Formal index, and arms the host's own description-field
gate — the host's session authoring its own descriptions, none written on its behalf, behind the owner's
gate.

### 4.0.0 — 2026-07-22

**Host action: run a migration.** The 4.0.0 major changes the product spec's own format. The spec moves
from the scenario-first prose form to a requirements genre: a short preamble, a glossary, and a body of
numbered requirements. Each requirement carries a Context block of two to four sentences, a one-sentence
User Story, and acceptance criteria grouped into named cases. The keywords *when*, *while*, *if*, *then*,
and *shall* read in lowercase italics; the code anchors trail at each line's end and point to the rule's
home; a `[GAP: ...]` line records a hole the source spec never filled, so a real gap is stated and never
invented. The format's full definition lives in `docs/spec-format.md`. The tier is MAJOR by rule 32 /
SPEC INV-217 because the spec document's shape changed and a host does real authoring work its own
session must run: a host rewrites its own spec into the new genre, work no walk can re-run blind.

What the release carries, grouped:

1. **The spec is a requirements document (`docs/spec-format.md`).** The whole spec reads as a preamble, a
   glossary of every domain noun, and a list of requirements. A stranger can read any one section on a
   first pass. The glossary holds one entry per term, and one artifact carries one name everywhere.

2. **The manual Formal index retires; a generated table replaces it.** `scripts/build-index.py` reads the
   body and writes a code-to-location table, embedded in the document's Reference section. No one edits it
   by hand. `guardrails/check-index-generated.py` keeps it honest: it reds if the committed table drifts
   from a fresh build, or if a code and its table row disagree.

3. **Spec changes carry a delta record.** Every touched code names one of four kinds — new, sharpen,
   retire, or scenario-only — and `guardrails/check-delta-record.py` reds where the record and the actual
   diff disagree (SPEC INV-260). *(2026-09-02 note: this chapter also shipped a bytes-per-criterion size
   ratchet, seeded at the value the conversion landed on. It was cut on the owner's word: a delivery that
   cut two whole requirements out of the pack's own spec raised the average and reddened the gate, because
   the criteria removed ran shorter than the rest. Nothing replaces it — the figure is still measured and
   printed, and held against nothing. A converting host installs no such gate.)*

4. **A comprehension gate guards every converted or new section.** The mechanical lints run first — the
   vocabulary check, the one-name check, the style lint, and the weak-word check. Then a panel of fresh
   cold readers reads the section with no project context, until two consecutive reads return zero
   blocking findings. Each new blocking word a reader finds joins the weak-word list.

5. **The register bar now covers the whole prose corpus that ships** — the skills, the public docs, and
   the working docs — and the style lint reaches further. `scripts/spec-style-lint.py` gained an arm that
   flags the definitional `rather than` and `instead of` frames it read past before, the same
   name-a-thing-by-denying-its-neighbour ban the dash-and-comma arm already held. The 2026-07-22 register
   census (`docs/audit/2026-07-22-register-census.md`) is the per-file starting point the bar tightens
   against.

6. **A new working skill, text-audit, packages the audit loop.** It runs the mechanical lints, then the
   fresh zero-context cold reads, with each fix made at the source, until two consecutive clean reads.
   The pack now carries ten working skills.

7. **Two terms settle under the one-name law.** The spec's vocabulary now reads *delivery report*
   (retiring `landing report`) and *harness task panel* (retiring `harness task list`), and the pack
   skills carry the new names throughout after the same 4.0.0 sweep. A host renames these two terms in
   its own documents as part of its conversion.

**How a host takes it.** A host keeps its current spec until it converts. The old format keeps working
and no gate forces the move, so a host that pulls 4.0.0 and waits breaks nothing.

The templates carried the old format for a year after that rewrite, so a project started from them
began in a genre the gates refuse. They were brought into the current format on 2026-08-05, proven by
building a specification from the starting template and running the shape gate over it. When a host does convert, the pack's conversion recipe
walks the spec unit by unit: convert each unit into the requirements genre, prove zero code drop through
the unit's mapping, run the mechanical lints, put each converted section before the cold-reader panel, and
assemble the units into one document. The 2026-07-22 conversion of the pack's own spec runs the recipe
end to end and records every edit past a plain concatenation (`prototype/2026-07-22-spec-format/`).
The host repository named tlvphotos converts first, on the owner's word; other hosts follow on the same word.

The host's own format gates — requirement-shape, vocabulary, one-name, weak-words, no-history, the
generated index, and the delta classifier — arm when the host's converted spec lands
(SPEC INV-270); until then they stand dormant and red nothing. The installed-set record reads the pack
version from the version lines the installed skills carry, so a host records 4.0.0 once its conversion
lands behind the owner's gate.

### 4.3.0 — 2026-07-23

**No forced host action.** The 4.3.0 minor makes the architecture document the format family's fourth
member, defined in `docs/architecture-format.md`: each node stands as a `### [node: <name>]` section with
its responsibility, the spec anchors it owns, its file-and-line pins, and an optional notes line, read
through the one node reader `guardrails/archformat.py`. This joins the spec (4.0.0), the test matrix
(4.1.0), and the roadmap (4.2.0) as family members a host converts. This chapter's five steps are the
current per-document recipe, and they supersede the 4.0.0 chapter's wording: convert the document's
units, prove no content dropped by the word-and-punctuation multiset check, repoint every consumer of
the old shape to the reader, run the mechanical lints, and put each converted section before the
cold-reader panel. A host keeps its old-format `ARCHITECTURE.md` until
it converts; the architecture format gates arm only when the host's converted document lands (SPEC
INV-270), staying dormant and reddening nothing until then. The pack's own conversion of its
`ARCHITECTURE.md` runs the recipe end to end and records every named delta
(`prototype/2026-07-23-architecture-format/`). The host repository tlvphotos converts on the owner's word; other hosts follow
on the same word.

### 5.0.0 — 2026-08-13

**Host action: re-run the catch-up walk.** The 5.0.0 major moves the product-prover canon to its own
repository; the pack now installs it as an external skill instead of shipping its body. Three steps,
each safe on a half-done state:

1. Install the external product-prover: run `scripts/install-external-skills.sh`, which clones the
   canon into the pack checkout's `skills/product-prover/`. Already-done check: that directory exists,
   carries its own `.git`, and its version meets the floor the adapter states in
   `skills/product-prover-pack/SKILL.md`. The step needs network; without it the walk stays open on
   this step under the checkpoint.
2. Run `./install.sh` to install or refresh the pack-owned skill directories — the
   `product-prover-pack` adapter arrives this way. The installer skips the external canonical clone.
   Earlier chapters route a skill refresh through `scripts/sync-skills.sh`; from this release the
   installer owns the step. The sync tool skips the external clone too, as of 2026-08-13.
3. Rule-30 retirement. The base rulebook's rule 30 was cut whole on 2026-08-12; its number stays an
   open hole, and the law it held is gate-held (SPEC INV-164). A host that adopted 2.0.0 and quotes
   rule 30 in its own documents re-points those lines to the gate-held law; a host that quotes nothing
   records this step done on read.

### 6.0.0 — 2026-08-26

**Host action: re-run the catch-up walk.** The 6.0.0 major moves the pipeline's entry point off
`build-pipeline` and onto a new skill, `director`; splits `architect` out as its own skill; and
retires thirteen base rules that carried no eval fixture and no executable script behind them.
Four steps, each safe on a half-done state:

1. Install the new skill roster. Run `./install.sh` (or `scripts/sync-skills.sh` for a host still on
   the older refresh path) to pull `director` and `architect` into the host's installed-skills home
   alongside the rest of the pack-owned set — the installer's loop over `skills/*/` picks up a new
   directory with no per-skill wiring needed. Already-done check: `director/SKILL.md` and
   `architect/SKILL.md` both exist in the host's installed skills and carry `version: 6.0.0`.
2. Re-point any host wiring that calls `build-pipeline` for an accepted change — a hook, a slash
   command, a documented "start here" line — to call `director` instead. `build-pipeline` itself
   still exists and still answers to "attach live-spec to this project" and the MINOR-bump gate
   procedure; it no longer runs the door, the work-kind table, the footprint scale, the request-kind
   table, or the fixed nine-step sequence, all of which now live in `director` (its own body, or
   `skills/director/references/`). A host that vendored a copy of any of those four tables re-points
   it at the new home or drops the copy in favor of reading `director/SKILL.md` live. Already-done
   check: the host's own docs name `director`, not `build-pipeline`, as the entry point for ordinary
   work.
3. Drop or re-point citations to the thirteen retired base rules. Rules 11, 14, 15, 18, 19, 20, 21,
   23, 28, 32, 33, 34, and 35 left `skills/live-spec-base/SKILL.md`'s mandatory body on 2026-08-26 —
   each was audited against the pack's one graded eval fixture (`evals/director/scenarios.json`) and
   every script under `guardrails/`, `hooks/`, and `tests/`, and none had a mechanism that would
   actually go red on a real violation, only prose-presence tests that watch a document's wording
   rather than a behavior. Their numbers are retired, not reused, and their full text — unedited —
   now lives in `attic/live-spec-base-unbacked-rules-2026-08-26.md`. A host that quotes one of these
   thirteen rule numbers in its own playbook or `CLAUDE.md` re-points the citation at the attic file
   (the judgment the rule carried is unchanged, only its standing as an enforced rule); a host that
   quotes none of them records this step done on read. The twenty-one rules that stayed each kept
   their number — no rule below 34 was renumbered — but several shifted line position inside
   `SKILL.md` as the retired rules' text left the file; a host holding its own line-number pins into
   `skills/live-spec-base/SKILL.md` re-derives them rather than trusting the old numbers.
4. Fifty-four gate files retired from `guardrails/` and `hooks/` in the same cutover — checks whose
   only subject was another check, invented numeric ceilings with no incident behind them, and a
   tool-boundary chat arm that could not prove whose work it stopped. None of these carried a rule
   that survived step 3 above. A host that named one of these scripts directly in its own CI
   configuration or pre-push chain (rather than through the pack's `guardrails/pre-push`, which
   already dropped them) removes that reference; a host that only ever invoked the pack's own
   `pre-push` entry point records this step done on read.

### 6.1.0 — 2026-08-31

**No host action.** The 6.1.0 minor changes what the pack teaches a project it is being attached to
for the first time. It rewrites nothing an adopted host already carries, so a host takes it by
re-running its catch-up walk and finding this chapter already satisfied (INV-217).

Two questions stood behind the change, and both are answered here.

**Does a project joining the pack still get a queue file of its own?** No. This repository merged its
own wish queue into `PLAN.md` on 2026-08-28 and has run on one list since: the plan, the board and
the queue are one document, and the second list stopped existing in the machinery on the day it
stopped existing in the work. A project founded after that date carries no legacy queue to preserve,
so the founding walk was still handing a fresh tree the two-file shape this repository had just left
as the worse one. `adopt/START.md` now lands `templates/PLAN.template.md` as the host's `PLAN.md`,
`adopt/ADOPT.md`'s canonical document set names that one list in place of `ROADMAP.md`, and the
skills that named a queue file as the place a wish lands — spec-author and its glossary,
design-reviewer, director, communicator's word list, live-spec-base and its glossary, and
product-prover-pack's path map — name the one list instead.

`templates/ROADMAP.template.md` retires to `attic/ROADMAP.template.md` under its manifest line. The
row shape, the class and status vocabularies, the live-body law and the acceptance cell all carry
over into `templates/PLAN.template.md` unchanged, and `docs/roadmap-format.md` stays their one home,
so nothing a host reads about how a row is written has moved.

**What does a host that already carries a separate queue file do?** Nothing. This is a change to what
the pack teaches at onboarding from this point forward, and it forces no migration on a tree that
already stands. Each adopted host runs its own version of the pack and decides its own timing, under
the standing boundary that nothing outside a host's own session writes that host's repo (INV-10). A
host running a separate queue is not asked to merge it, and a host that wants the one-list shape
takes it as its own row through its own pipeline. Both shapes are readable by the pack's skills: the
sentences repointed above name the one list, and a host whose queue lives under its own filename is
already covered by the host-profile line that records it.
