### [node: attach]

**responsibility** — attaching the pack to a host. That covers the adoption phases, the VCS gate, the attic, and the who-am-I-working-with step. It also covers the skill install, the version record, and the pack update check. The catch-up walk that brings an already-adopted host onto the current pack sits here too.

**owns** —
- E-1 · E-9 · INV-7 · INV-8 · B-2 · B-3 · INV-36 · A-0 · A-1 · A-2 · A-3 · A-4 · A-5 · A-7 · A-8 · A-9 · A-10 · A-11 · INV-89 · INV-90 · INV-91 · INV-92 · INV-110 · INV-111 · E-21 · E-25 · INV-85 · INV-86 · INV-172 · INV-177
- INV-227 (the recorded `founding.set-version` profile line is carried by host-contract as wiring, ownership stays here beside E-25 and INV-177)
- INV-178 · INV-180
- INV-307 (the spoken setup entry. One skill description carries the sentences. The routing card resolves the pack's own tree and picks the walk. `adopt/START.md` is the founding walk. The description field is carried by build-pipeline as wiring; ownership stays here beside A-0 and E-21.)

**pins** —
- `adopt/ADOPT.md:49` (VCS gate first)
- `adopt/ADOPT.md:201` (unbacked-surface verdict)
- `adopt/ADOPT.md:212` (attic)
- `adopt/ADOPT.md:321` (attach record)
- `adopt/ADOPT.md:90` (B-3 — who am I working with, first step of orient)
- `adopt/START.md:1` (B-1 — the founding walk)
- `skills/build-pipeline/references/project-setup.md:1` (INV-307 — the setup routing card)
- `MIGRATION.md:1` (A-11 — the catch-up walk's operating guide)
- `install.sh:1` (E-21 — the installer itself)
- `scripts/check-pack-update.sh:1` (E-25 — the update check + the founding arm, INV-227)
- `scripts/founding-questions.json:1` (INV-227 — the versioned founding-question set)
- `adopt/install-style-gates.sh:1` (INV-172 — the style-gate kit installer)

### [node: templates]

**responsibility** — the document shapes a host copies at bootstrap; the matrix's generated reference section

**owns** — E-3, E-5, INV-6, B-1, E-24, INV-48, E-26

**pins** — `templates/TEST_MATRIX.template.md:52` (coverage validation), `templates/PLAN.template.md:1`, `templates/PRODUCT_SPEC.template.md:126` (index), `templates/PROBLEMS.template.md:1` (E-24 — the ledger's shape)

### [node: package-docs]

**responsibility** — live-spec's own host instance (dogfood): spec, queue, journal, resume file, version, records, dev-machine skill sync, its own problem ledger

**owns** — S-0, M-3, M-4, D-1, D-2, D-4, D-6, D-7, E-23

**pins** — `PRODUCT_SPEC.md:1`, `PLAN.md:164` (the task list), `JOURNAL.md:1`, `VERSION:1`, `scripts/sync-skills.sh:1` (E-23), `.live-spec/PROBLEMS.md:1` (E-24's dogfood instance; anchor owned by templates)
