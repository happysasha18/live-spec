# Adopting the pack in an existing project

live-spec attaches to a codebase that already has code, documents, and habits. The project that
adopts it is called the **host**. The normative procedure is [adopt/ADOPT.md](../adopt/ADOPT.md);
this page gives the shape of the run, what the host gains, and where the supporting files live.
When this page and ADOPT.md differ, ADOPT.md wins. A project with nothing in it yet takes a
different walk, the founding at [adopt/START.md](../adopt/START.md). Two spoken sentences reach the right one of the
two: "attach live-spec to this project" and "found a new project on live-spec". The
[routing card](../skills/build-pipeline/references/project-setup.md) the build-pipeline skill
carries is what picks.

One boundary holds through the whole run: from a host session, the live-spec package repo is
read-only. A defect found during adoption goes into live-spec's `inbox/` as one new file and into
the host's own journal (SPEC INV-10). A live-spec session sweeps that folder later.
`feedback-intake` routes each deposit to its one home: a queue row, a decision archive entry, or a
feedback-ledger line. The same commit that lands the route removes the swept file
(SPEC INV-68, T-10).

## The procedure at a glance

ADOPT.md runs as ordered phases; each phase states its own done-condition. In plain terms:

1. **Version control first (Phase 0).** The host becomes a git repo with a `.gitignore`, one commit
   of the pristine tree made by `adopt/record-starting-state.sh` before any pack file lands, and a
   recorded decision about a remote. From this point the whole run is reversible, and every later
   change diffs against how the project started.
2. **Cruft sweep, offered once (Phase 0.5).** Writing the `.gitignore` surfaces regenerable junk
   such as caches and stale exports. The run lists it in groups and deletes only what the human
   approves.
3. **Orient (Phase 1).** The run loads the human's personal profile, asks the founding questions
   (personal or reusable, what kind of project this is, budget pressure), proposes matching
   skills, and reads every existing document before writing anything. The result is a per-document
   digest under `.live-spec/adopt/`, the run's audit trail.
4. **Inventory (Phase 2).** Every user-facing output, surface, and data entity gets one line with
   a real `file:line` pin. The surfaces seed the surface registry.
5. **Re-engineer existing documents (Phase 3).** What exists turns into the canonical document
   set, keeping the original claims and marking their provenance. Each live surface that lacks
   spec backing gets a human verdict: promote, quarantine, or attic.
6. **Attic over deletion (Phase 4).** Superseded files move to `attic/` with a manifest line,
   via `git mv`, after the human approves the set. Adoption never deletes a host file (INV-7).
7. **Architecture, then tests (Phase 5).** `ARCHITECTURE.md` grows from the inventory's pins;
   `TEST_MATRIX.md` is derived through it, one row per fact under its owning node, each row with
   a test level.
8. **Attach record (Phase 6).** The run records the installed skill versions in `.live-spec/`,
   seeds the host profile, writes its journal entry, and the host joins the standard pipeline.

The recommended first action after adoption is a full product-prover pass over the spec. One thing
lets a host skip it: a recent prover record covering the spec, with no drift since. That record
must come from the same prover version installed now (ADOPT.md, Phase 6).

## What the host gains

The canonical document set lives in `adopt/ADOPT.md` — one normative list; the lines below say what
each document does for the host.

- **A living spec** — `PRODUCT_SPEC.md`, use-case-first, with entities, states, transitions,
  invariants, and cross-section composition underneath.
- **An architecture doc and a test matrix** — `ARCHITECTURE.md` names the nodes and seams;
  `TEST_MATRIX.md` derives one pinned-level row per spec fact through them.
- **A journal** — `JOURNAL.md`, dated entries with the why, so history survives memory wipes.
- **A resume file** — `NEXT_STEPS.md`, the one place a cold session reads to continue the work.
- **A queue** — `ROADMAP.md`, where existing TODO items land as rows.
- **A surface registry** — `SURFACES.md` (or an equivalent gate test), so an unregistered
  rendered surface goes red.
- **Profiles** — the host profile at `.live-spec/profile.md` holds this project's overrides; the
  personal profile at `~/.claude/live-spec/profile.md` holds the human's standing preferences.
  The host file narrows the personal one per the settings ladder (SPEC E-13).

## Migrating an existing codebase

Phase 3 of ADOPT.md owns the mapping of existing documents: an existing spec becomes
`PRODUCT_SPEC.md` sections, existing tests become matrix rows cited at their real level, and an
existing roadmap becomes queue rows. Every re-engineered claim starts unverified and gets
reconciled against real code at the first landing that touches its surface. A host whose docs are
already in live-spec shape keeps them as they are; adoption then only fills what is missing,
usually the surface registry and the matrix.

The mapping is type-aware. The project kind recorded at orient (book, backend service, static
site, fullstack app, CLI, skill pack) sets the spec's primary unit: a feature for an app, a
command or endpoint for a CLI or API, a chapter for a book, a promised guarantee for a
methodology package. The decided format lives in
[docs/spec-format-by-project-type.md](spec-format-by-project-type.md).

[MIGRATION.md](../MIGRATION.md) covers the other entry: an already-adopted host catching up with
a newer pack. That guide owns the catch-up walk — orient on the delta, one plan behind the
owner's gate, execution that preserves facts, then verify and re-record — and holds the dated
per-version migration chapters the walk applies, oldest first. Each host's own session executes
the walk; nothing outside a host's session writes that host's repo.

## The scaffold and templates

`templates/` holds fourteen starter files. Six are the canonical document set:
`PRODUCT_SPEC.template.md`, `ARCHITECTURE.template.md`, `TEST_MATRIX.template.md`,
`PLAN.template.md`, `JOURNAL.template.md`, and `NEXT_STEPS.template.md`. Three land on the
project's own word: `DECISIONS.template.md`, `PROBLEMS.template.md`, and `KILL_LIST.template.md`.
The remaining five each carry their own job. `test_scaffold.template.py` is the first runnable
suite, and `agent.template.md` is the tree's agent card. `profile.template.md` is the shape of a
person's own profile, and `skill-review.template.md` the shape of a skill-review record.
`headless_harness.py` is the shared harness for browser-level tests.

A fresh project gets these through the founding walk, [adopt/START.md](../adopt/START.md). That
walk lands each one under its canonical name, and it stops by name where the pack tree lacks one.
`install.sh` installs the skills alone and reaches no template. An adopted host uses them only for
the documents it lacks, since Phase 3 re-engineers the rest.
The test scaffold lands in `tests/` and defines the minimal green for the first landing.

`scaffold/guardrails/README.md` is the authoritative description of the four mechanical checks a
host instantiates for its own surfaces: completeness (every rendered surface is registered and
non-empty), tests-present (a diff touching a user-facing module also touches `tests/`),
behaviour-traces-to-spec (every user-facing behaviour names its spec clause), and conflicts
(duplicate IDs, dead references, unmatrixed invariants). One command vendors them:
`bash <pack>/adopt/install-scaffold.sh`, run from the host root. It writes six files into the
host's `guardrails/`: the four checks, their shared library, and that README itself. It seeds
`guardrails.config.json` where the host carries none, and a filled config is never clobbered. It
also writes `scripts/ratchet-manifest.json`, creating a `scripts/` folder in the host that has none
(SPEC INV-97, INV-177).

Two installers follow it, both named by ADOPT.md at the end of Phase 5.
`bash <pack>/adopt/install-ratchet.sh [DOC...]` vendors the style, redundancy and freeze gates. It
seeds the debt caps at the host's size today and generates `tests/test_ratchet_lock.py`
(SPEC INV-172). `bash <pack>/scripts/install-pack-hooks.sh` installs the pack's canonical scan
hooks on the machine, idempotently, leaving the personal overlay files alone (SPEC INV-173). A host
that stops after the first installer carries less gate than the procedure asks for.

`install.sh` at the package root copies the pack's skills into `~/.claude/skills/`, backing up any
existing skill with a timestamp.

## What stays optional

- **The remote.** A GitHub remote either exists by the first landing or the human explicitly
  declines one; both outcomes are recorded.
- **The cruft sweep.** The run may skip offering it; deletion without an approval is the only
  forbidden path.
- **The personal profile.** The human may decline creating one; the session then runs on package
  defaults, said aloud.
- **Hooks.** Offered in plain words at attach, on the same terms as at bootstrap; never imposed.
- **The post-adoption prover pass.** Recommended, and skippable when a recent prover record from
  the same prover version covers the spec with no drift since.
