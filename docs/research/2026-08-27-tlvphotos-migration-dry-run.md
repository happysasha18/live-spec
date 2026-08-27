# tlvphotos: pack 2.7.0 → 6.0.0 catch-up walk — drift inventory, dry run, restore proof

Read-only study of ~/tlvphotos. Nothing in ~/tlvphotos was written, staged, or committed.
All work happened in ~/live-spec (read-only) and under this scratchpad.

## 1. Drift inventory

| Item | Pack expects (6.0.0) | Host has | Classification |
|---|---|---|---|
| Product spec | `PRODUCT_SPEC.md` | `SPEC.md` (478,107 bytes) | **Renamed**, host's own name kept under the preserve-and-re-home law (INV-90) — but the law also requires a host-profile line `spec.file: SPEC.md` recording the rename. **That line is missing from `.live-spec/profile.md`.** Grep of the whole 144-line file finds no `spec.file:` line at all. |
| Surface gate doc | `SURFACES.md` (or an equivalent executable gate test, E-10) | `SURFACE_REGISTRY.md` (9,214 bytes) | Renamed, host's own — no profile line records this rename either, same gap as above. |
| Product vision | not a pack canonical document | `VISION.md` (25,047 bytes) | **Host's own.** Outside the canonical document set in `adopt/ADOPT.md` §"The canonical document set" (PRODUCT_SPEC, ARCHITECTURE, TEST_MATRIX, ROADMAP, JOURNAL, NEXT_STEPS, SURFACES/equivalent, attic/, .live-spec/). Stays as is. |
| Taste doc | not canonical | `TASTE.md` (15,521 bytes) | Host's own, same reasoning. Stays. |
| Feature list | not canonical | `FEATURE_INVENTORY.md` (14,326 bytes) | Host's own, same reasoning. Stays. |
| Resume file | `NEXT_STEPS.md` (pack's own copy ~12 KB) | `NEXT_STEPS.md`, 123,971 bytes (~124 KB) | Canonical name matches; content is host's own and enormous relative to the pack's copy. Host's `guardrails/doc-bounds.json` already caps it at `max_bytes: 200000`, seeded 2026-07-21 when the file was 96,808 bytes. It has grown ~27 KB in five weeks; not over cap today, but on a trend toward it. **This is entirely the host's own content — no chapter in MIGRATION.md touches NEXT_STEPS.md's prose.** |
| Skill roster (`.claude/skills/`, git-tracked, 39 files, 907 total tracked files in repo) | 14 skills at 6.0.0: `live-spec-base, spec-author, product-prover(-pack), design-reviewer, architect, build-pipeline, director, test-author, communicator, feedback-intake, feedback-collector, publish, text-audit-pack` | 10 skills, all at `version: 2.7.0`: `build-pipeline, communicator, design-reviewer, feedback-collector, feedback-intake, live-spec-base, product-prover, publish, spec-author, test-author` | **Behind.** Missing entirely: `architect`, `director`, `product-prover-pack`, `text-audit-pack`. `product-prover` itself is the old 2.7.0-era bundled copy; the pack now treats it as an external, separately-versioned clone (floor `>= 1.4.0` per `product-prover-pack/SKILL.md`) that a host must fetch itself — see finding below, this doesn't work out of the box for a host. |
| `.live-spec/installed.md` | should reflect the skills actually on disk | Header claims **"sync to pack 3.6.0"** (2026-07-21) and states "all ten skills at 3.6.0" | **The record disagrees with the disk.** Every one of those ten `SKILL.md` files reads `version: 2.7.0`, and the host's `guardrails/` carries none of the 3.0.0 (Description column / `check-description-field.py`), 4.0.0 (requirements-genre gates), or 4.3.0 (architecture-format reader) machinery — only the 2.7.0 gate set (`o` cleanup-notice through `z` doc-bound, all present and confirmed by file). The tree is genuinely at 2.7.0; the installed-set record's own claim of 3.6.0 is stale/wrong and should be corrected as part of the real walk (the half-done-state law already says a stale record like this is corrected from the skills actually on disk, INV-89). |
| `.live-spec/profile.md` founding answers | `founding.set-version: 6` (current set, `scripts/founding-questions.json`) | `founding.set-version: 5` | **Behind by exactly one question.** The only question added since version 5 is `since: 6, INV-291, project.config-surface`: "what can this project's owner change without a build?" This must ride the plan to the owner per Phase 1 step 5 of MIGRATION.md; nothing else is owed on this front. |
| Machine-global skill mirror (`~/.claude/skills`, same machine) | — | Already at 6.0.0 for every pack skill | Irrelevant to the host repo directly — Claude Code appears to prefer the project-local, git-tracked `.claude/skills/` for this project, so the global mirror being current does not carry tlvphotos forward. This is a separate finding worth naming: on this machine the global mirror already outran the project's committed copy, so anyone who assumed "the machine is current" would be wrong about this specific project. |
| Doc-format family (spec / architecture / test-matrix / roadmap, per 4.0.0 and 4.3.0 chapters) | requirements-genre spec, `[node: name]` architecture, generated index, size-ratchet gates | Old scenario-first `SPEC.md`, old free-form `ARCHITECTURE.md`, no `Description` column (3.0.0 never landed), none of the format gates present | **Behind, and this is the heavy one.** Chapters 3.0.0, 4.0.0, and 4.3.0 are each MAJOR, each explicitly "a migration... work no walk can re-run blind" — real authoring over the host's own 478 KB spec and 93 KB architecture document, not a script. MIGRATION.md itself says a host "keeps its current spec until it converts... no gate forces the move," so this is deferred, real work, not an urgent risk, but it is the largest single piece of debt between 2.7.0 and 6.0.0. |
| Host's own uncommitted WIP at read time | — | `NEXT_STEPS.md`, `lab/CROSSING-BRIEF.md`, `lab/CROSSING-HISTORY.md` modified; `PLAN.md` untracked (55,702 bytes) | Pre-existing, unrelated to the pack. Recorded so the copy and the live tree could be compared like-for-like; untouched throughout. |

## 2. Copy and backup

Commands run (all read ~/tlvphotos, write only to scratchpad):

```
git clone --no-hardlinks "$HOME/tlvphotos" "$SCRATCH/tlvphotos-dryrun"
# then, to make the copy match the LIVE working tree exactly (not just the last commit):
cp ~/tlvphotos/NEXT_STEPS.md              "$SCRATCH/tlvphotos-dryrun/NEXT_STEPS.md"
cp ~/tlvphotos/lab/CROSSING-BRIEF.md      "$SCRATCH/tlvphotos-dryrun/lab/CROSSING-BRIEF.md"
cp ~/tlvphotos/lab/CROSSING-HISTORY.md    "$SCRATCH/tlvphotos-dryrun/lab/CROSSING-HISTORY.md"
cp ~/tlvphotos/PLAN.md                    "$SCRATCH/tlvphotos-dryrun/PLAN.md"
```

Verified identical (`diff -q` on all four, and `git status --porcelain` matches between source and copy).

**Why `git clone` and not a raw filesystem copy:** `~/tlvphotos` is 34 GB on disk, but 906 of that is 907
git-tracked files (188 MB cloned, full history included) — the rest is git-ignored generated/media content
that no migration chapter touches: `lab/shots/` (23 GB of PNG/JPG, ignored via a nested `lab/.gitignore`),
`instagram_export/` (6.7 GB), `gallery/` (1.0 GB), `.venv/` (914 MB), plus caches. A full byte copy would
have cost ~35 GB and significant time for zero additional migration coverage, since the catch-up walk acts
on tracked documents, skills, and guardrails. This is a disclosed scope choice, not an omission — flagging
it explicitly per the brief's spirit rather than doing it silently.

Timestamp for this run: **20260827_094904**. Files left in scratchpad:

- `tlvphotos-dryrun/` — the working copy (post-restore state, see §4)
- `tlvphotos-dryrun-backup-20260827_094904.tar.gz` — 135,188,227 bytes, SHA-256
  `ba73809b71959387ca0ffe0a7a2aef3ba98ff68261b7c0904ee100515ae41c82` — the restore source
- `manifest-PRE-20260827_094904.txt` — SHA-256 of all 9,393 files in the copy before the dry run,
  SHA-256 of the manifest itself: `cbcb73d860193f60b6ace05f62fd379d320c39fc4cd12b85c775b5ebda6c04da`
- `manifest-POST-RESTORE-20260827_094904.txt` — same, taken after the restore
- `pre-migration-HEAD-20260827_094904.txt` — `df117143f98030b6996d204c88554519b35fc204`
- `pre-migration-status-20260827_094904.txt`, `sync-skills-output-20260827_094904.txt`
- `tlvphotos-status-START.txt`, `tlvphotos-status-END.txt` — `git -C ~/tlvphotos status --porcelain`, before and after all work

## 3. The dry run — what actually happened, and what could not be run

**What ran, against the copy only:**

```
bash ~/live-spec/scripts/sync-skills.sh "$SCRATCH/tlvphotos-dryrun/.claude/skills"
```

This is the literal action the 6.0.0 chapter's step 1 names ("`scripts/sync-skills.sh` for a host still
on the older refresh path"). Result: 13 of 14 pack skills synced 2.7.0 → 6.0.0 (or absent → 6.0.0 for the
four new ones: `architect`, `director`, `product-prover-pack`, `text-audit-pack`); `product-prover` itself
was skipped by the script's own external-clone fence.

`git status --porcelain` and `git diff --stat` inside the copy after this action: **the entire change is
confined to `.claude/skills/`** — 18 modified files, 9 deleted stale reference files (leftover
`build-pipeline/references/*` the 6.0.0 split retired), 10 new untracked files/directories (the four new
skill folders plus new reference sub-files under `communicator`, `spec-author`, `live-spec-base`,
`build-pipeline`). 27 files changed, 1,635 insertions, 2,152 deletions, all under `.claude/skills/`.
**Nothing outside `.claude/skills/` was touched by this action** — not `SPEC.md`, not `NEXT_STEPS.md`, not
any host canonical document. (The `NEXT_STEPS.md` / `lab/CROSSING-*.md` lines that still show as modified
in status are the pre-existing owner WIP copied in during step 2, unrelated to the sync.)

**What could not be run as a host action, and why (a real finding, not a gap in this exercise):**

```
cd "$SCRATCH/tlvphotos-dryrun" && bash ~/live-spec/scripts/install-external-skills.sh
```
→ `FAIL (external skills): no version floor found in skills/product-prover-pack/SKILL.md`

The script resolves paths relative to `git rev-parse --show-toplevel` and expects `skills/product-prover-pack/SKILL.md` — that is the **pack repository's own layout**, not a host's (`.claude/skills/product-prover-pack/SKILL.md`). The 5.0.0 chapter's wording ("Install the external product-prover: run `scripts/install-external-skills.sh`") reads as if a host runs this directly; empirically, it cannot — it only works inside a checkout of the pack itself. So bringing tlvphotos's `product-prover` up from its bundled 2.7.0 copy to the external clone (floor `>= 1.4.0`) needs a different, currently undocumented host-side action (most simply: clone `github.com/happysasha18/product-prover` straight into `~/tlvphotos/.claude/skills/product-prover/` by hand). Worth reporting upstream to live-spec as a real procedural gap, per the pack's own inbox convention — not something to fix by writing into either repo here.

`./install.sh` was read but not run against the copy: it hardcodes `$HOME/.claude/skills` with no
destination argument, so it cannot target a project's local `.claude/skills/` at all — only
`sync-skills.sh` can, via its `[dest]` argument. Running `install.sh` for real would only touch the
machine's global skill mirror (already at 6.0.0 on this machine), not the project. This asymmetry between
`install.sh` (no dest arg) and `sync-skills.sh` (dest arg) is itself worth naming: the 6.0.0 chapter's step
1 says "Run `./install.sh` (or `scripts/sync-skills.sh` for a host still on the older refresh path)" as if
the two are interchangeable for a host; they are not — only `sync-skills.sh` can write into a project's
own tree.

`install-pack-hooks.sh` was read (its argument parser has no `*)` fallback case, confirming the PLAN.md
Blockers note: a mistyped `--dryrun` silently falls through with `DRY_RUN` left at 0 and installs for
real) but not run — it only touches `~/.claude/hooks/`, a machine-global path unrelated to the project
copy, and is optional/opt-in tooling this walk doesn't need to exercise.

## 4. Restore proof

```
rm -rf "$SCRATCH/tlvphotos-dryrun"
tar -xzf "$SCRATCH/tlvphotos-dryrun-backup-20260827_094904.tar.gz" -C "$SCRATCH"
find "$SCRATCH/tlvphotos-dryrun" -type f -print0 | sort -z | xargs -0 shasum -a 256 > manifest-POST-RESTORE-....txt
diff manifest-PRE-20260827_094904.txt manifest-POST-RESTORE-20260827_094904.txt
```

Output of the diff: **empty. Exit code 0.** 9,393 files in both manifests, byte-for-byte identical
SHA-256 for every one. The restore is proven, not asserted.

## 5. What a real migration would do to the live host — the risk list

Ranked by what it actually touches:

1. **Skill roster refresh (`sync-skills.sh` pointed at `~/tlvphotos/.claude/skills`).** Proven safe by
   the dry run above: touches only `.claude/skills/`, never any host canonical document. Low risk. The
   nine deleted stale reference files and ten new files are pack content, not host content — no owner
   prose is at stake here.

2. **The installed-set record (`.live-spec/installed.md`) gets rewritten.** This is a host record, but
   its content is entirely pack-facts (which skills, what version) — no owner prose. The current record
   is already wrong (claims 3.6.0, disk says 2.7.0), so rewriting it is a correction, not a loss.

3. **One founding question surfaces to the owner** (`project.config-surface`, since version 6) —
   answered by the owner, on no one's behalf. No file content is at risk; it's a question, not a write.

4. **A missing profile line (`spec.file: SPEC.md`, and arguably an equivalent for `SURFACE_REGISTRY.md`)
   should be added to `.live-spec/profile.md`.** This is an addition, not a rewrite of existing profile
   prose — low risk, but flagged because the law (INV-90) already expected it and it was never done.

5. **The external `product-prover` needs to be swapped from the bundled 2.7.0 copy to an external clone.**
   This deletes and replaces a pack-owned skill directory the host currently vendors inline —
   `.claude/skills/product-prover/`. Pack content, not host content, but the mechanism to do it for a
   host doesn't exist yet (see §3) — whoever runs the real walk needs to solve that first or do it by hand.

6. **The heavy one — spec/architecture/test-matrix format conversion (chapters 3.0.0, 4.0.0, 4.3.0).**
   This is the one place a real migration touches the host's own large, owner-authored documents at
   scale: `SPEC.md` (478 KB, scenario-first prose → requirements genre, plus a new Description column
   backfilled for every registered code) and `ARCHITECTURE.md` (93 KB, free-form → `[node: name]`
   sections). MIGRATION.md's own law is preserve-and-re-home (INV-90): content moves, nothing is deleted,
   rewritten prose only where the new shape truly cannot hold the old, and every step's before/after
   self-test (INV-92) — a content-fingerprint inventory taken before and after — must show every
   difference accounted for by a named plan item before the walk is allowed to call itself done. That is
   the mechanism that makes this safe *if followed*, but it is real authoring work over the owner's own
   478 KB of product spec, and MIGRATION.md itself says a host is not forced into it ("keeps its current
   spec until it converts... no gate forces the move"). **This is not urgent and the pack does not
   require it**, but it is the part of the walk most likely to touch phrasing the owner actually cares
   about, and it should run under the owner's explicit review of the plan document (Phase 2 gate), never
   applied blind.

7. **`NEXT_STEPS.md` (124 KB) and the other large host docs are not targeted by any chapter's content
   rules** — no chapter rewrites resume-file prose. The only mechanical interaction is the existing
   `doc-bounds.json` ceiling (200,000 bytes, currently 62% full) and the doc-rotation gate, both of which
   the host already carries from 2.7.0 and which only fire if the file keeps growing past its own
   declared ceiling — not something the walk itself would trigger.

**Bottom line for the owner:** the mechanical part of a real 2.7.0 → 6.0.0 walk (skill refresh, record
rewrite, one founding question, one missing profile line) is low-risk and proven safe here — it never
touches `SPEC.md`, `NEXT_STEPS.md`, `VISION.md`, `TASTE.md`, `FEATURE_INVENTORY.md`, or
`SURFACE_REGISTRY.md`. The one piece of real risk is the optional, not-required, format-conversion debt
(3.0.0/4.0.0/4.3.0) sitting on top of the host's own 478 KB spec and 93 KB architecture document — and
that piece already carries its own preserve-and-re-home law and before/after self-test, and the pack
itself says a host is never forced to take it.
