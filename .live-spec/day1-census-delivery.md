# Day 1 census: what a stranger has after installing live-spec

Root: Alexander's order of 2026-08-08 22:17 and `.live-spec/culling-plan-2026-08-08.md`, day 1. Census only — no check added, no plan edited, no rule changed.

## Headline

A stranger who clones the repo and runs `./install.sh`, per the README's own walkthrough, gets the ten skill folders under `~/.claude/skills/` and nothing else — no hooks, no scripts, no guardrail checks. The README never points at `scripts/install-session-hooks.sh` or `scripts/install-pack-hooks.sh`; a stranger who separately finds and runs the session-hooks script also gets sixteen hook files under `~/.claude/hooks/`, wired into `~/.claude/settings.json`. Counting the more generous of the two — skills plus hooks, the largest set any documented or discoverable script places on a fresh machine — the ten skill files and sixteen hook files together carry **219 references that point at nothing the install placed**, spread across 33 of the 66 installed files. 123 distinct targets are named. My count does not match the audit's 183; see "Why my count differs" below.

## Method, in short

Simulated the install into a throwaway `$HOME` (never the real `~/.claude`): ran `install.sh` (copies `skills/` into `~/.claude/skills/`), then `scripts/install-session-hooks.sh` (which copies its own two hooks and chains to `scripts/install-pack-hooks.sh` for the other eight, then wires all ten into `settings.json`). Also ran `scripts/check-pack-update.sh`, which writes only a version-check stamp file — it installs nothing and is excluded from the census. `adopt/install-scaffold.sh` and `adopt/install-ratchet.sh` vendor checks into a *host project*, not into `$HOME`, so they sit outside this "fresh home" census.

Every installed file was scanned for markdown links, backtick-quoted paths, and bare mentions of `scripts/…`, `guardrails/…`, `skills/…`, `docs/…` and the pack's other top-level directories. Each reference was resolved against the installed tree only. Excluded from the count: content inside fenced code-block examples (shell commands like `cp design-reviewer/SKILL.md ~/.claude/skills/design-reviewer/`, correct relative to a different working directory, not a doc cross-reference), external URLs, glob/date-pattern placeholders (`YYYY-MM-DD`, `<name>`, `[-suffix]`), directory-only mentions with no filename, and five confirmed illustrative examples in the prose (`build_widget.py`, `docs/x.html`, `notes/x.html`, `docs/deltas/2026-07-22-row445.json`, and the `SPEC.md` example in a rename-convention table).

## By installed file carrying broken references

| Installed file | Broken references |
|---|---:|
| skills/text-audit/SKILL.md | 30 |
| skills/spec-author/SKILL.md | 29 |
| skills/live-spec-base/SKILL.md | 27 |
| skills/build-pipeline/SKILL.md | 22 |
| skills/text-audit/references/rewrite-meaning-check.md | 17 |
| skills/design-reviewer/SKILL.md | 9 |
| skills/product-prover/SKILL.md | 9 |
| skills/communicator/references/words.md | 8 |
| skills/test-author/SKILL.md | 8 |
| skills/build-pipeline/references/project-setup.md | 7 |
| skills/communicator/references/page-lifecycle.md | 6 |
| skills/text-audit/references/human-prose-rules.md | 6 |
| skills/communicator/SKILL.md | 4 |
| skills/publish/SKILL.md | 4 |
| skills/build-pipeline/references/delegation-protocol.md | 3 |
| skills/build-pipeline/references/request-kind-table.md | 3 |
| skills/communicator/references/writing-register.md | 3 |
| skills/feedback-intake/README.md | 3 |
| skills/feedback-intake/SKILL.md | 3 |
| skills/build-pipeline/README.md | 2 |
| skills/communicator/references/field-examples.md | 2 |
| skills/feedback-collector/SKILL.md | 2 |
| skills/product-prover/README.md | 2 |
| hooks/affirmation-scan.py | 1 |
| hooks/hedge-scan.py | 1 |
| hooks/scissors-scan.py | 1 |
| skills/build-pipeline/references/drafter-applier-example.md | 1 |
| skills/build-pipeline/references/minor-bump-gate.md | 1 |
| skills/build-pipeline/references/work-kind-table.md | 1 |
| skills/design-reviewer/README.md | 1 |
| skills/spec-author/README.md | 1 |
| skills/test-author/README.md | 1 |
| skills/text-audit/README.md | 1 |
| **Total** | **219** |

The other 33 installed files (LICENSE files, most README.md files, `settings.json`, the remaining hook files) carry none.

## The 123 distinct missing targets

Count is how many installed files reference that target.

**Named 6+ times**

| Target | Referenced by N installed files |
|---|---:|
| ARCHITECTURE.md | 10 |
| PRODUCT_SPEC.md | 10 |
| PRODUCT_SPEC.index.md | 8 |
| ROADMAP.md | 6 |
| TEST_MATRIX.md | 6 |

**Named 3–5 times**

.live-spec/PROBLEMS.md (5) · scripts/spec-style-lint.py (5) · MIGRATION.md (4) · .live-spec/profile.md (3) · DECISIONS.md (3) · FEEDBACK.md (3) · JOURNAL.md (3) · NEXT_STEPS.md (3) · PLAYBOOK.md (3) · adopt/ADOPT.md (3) · docs/language-rule-coverage.md (3) · docs/pipeline.md (3) · guardrails/check-index-generated.py (3) · guardrails/check-worker-restore.py (3) · guardrails/language-rules.json (3) · scripts/preshow-register-lint.py (3) · scripts/sync-mirrors.sh (3) · tests/test_traceability.py (3)

**Named twice**

PROBLEMS.md · SURFACES.md · adopt/START.md · docs/language-rules.md · guardrails.config.json · guardrails/check-matrix-reference.py · guardrails/check-requirement-shape.py · guardrails/check-vocabulary.py · guardrails/crosscut_counter.py · guardrails/node_growth_counter.py · guardrails/rule-census.json · install.sh · scripts/build-index.py · scripts/gen-language-consumers.py · scripts/open-lane.sh · scripts/spec-debt-cap.json · scripts/sweep-rendered.py · templates/profile.template.md · test_traceability.py · tests/test_interface_coverage.py

**Named once (86 targets)**

./install.sh · .claude-plugin/marketplace.json · .git/hooks/pre-push · .live-spec/agent.md · .live-spec/logs/suite.log · CHANGELOG.md · CLAUDE.md · attic/MANIFEST.md · check-requirement-shape.py · check-vocabulary.py · check-weak-words.py · docs/language-defects.md · docs/language-worked-example.md · docs/lenses.md · docs/plans/2026-07-28-top-level-readability.md · docs/prose-quality-gate-design.md · docs/prover/architecture-prover-record.md · docs/queue-archive/rotated-ROADMAP-2026-07.md · docs/reports/2026-07-28-document-state-and-plan.md · docs/roadmap-format.md · docs/skill-review/2026-08-05-audit-runs-two-readers.md · docs/skill-review/2026-08-05-audit-skill-names-its-spec-only-lints.md · docs/skill-review/2026-08-05-live-spec-base-readability.md · docs/spec-format-by-project-type.md · docs/spec-format.md · docs/spec-style.md · evals/fixtures/text-audit/rewrite-weakens-the-rule.md · gen-language-consumers.py · guardrails/check-authority-anchor.py · guardrails/check-deferral-marker.py · guardrails/check-delta-record.py · guardrails/check-doc-findings-bound.py · guardrails/check-earned-message.py · guardrails/check-far-tier.py · guardrails/check-freeze.sh · guardrails/check-handover-provenance.py · guardrails/check-language-rules.py · guardrails/check-muted-launch.sh · guardrails/check-one-name.py · guardrails/check-push-reach.sh · guardrails/check-release-note.py · guardrails/check-rendered-sweep.py · guardrails/check-shipped-language.sh · guardrails/check-size-ratchet.py · guardrails/check-weak-words.py · guardrails/check-wrong-referral.py · guardrails/node-file-cap.json · guardrails/pre-push · guardrails/spec-coinages.json · guardrails/spec-ratchet.json · guardrails/specformat.py · guardrails/weak-words.json · scripts/build-matrix-reference.py · scripts/judge-rubric.md · scripts/preshow-legibility-lint.py · scripts/preshow-lint.py · scripts/render-doc.py · scripts/rule-census.py · scripts/session-extract.py · scripts/spec-done-gate.py · scripts/spec-freeze.py · scripts/spec-judge.py · scripts/spec-redundancy-precheck.py · scripts/spec-waivers.json · templates/ARCHITECTURE.template.md · templates/PRODUCT_SPEC.template.md · templates/TEST_MATRIX.template.md · templates/agent.template.md · templates/headless_harness.py · tests/test_derived_doc_header_policy.py · tests/test_text_audit_fixtures.py · tests/test_worker_restore.py · weak-words.json · ~/.claude/CLAUDE.md · ~/.claude/hooks/affirmation-personal.json · ~/.claude/hooks/hedge-personal.json · ~/.claude/hooks/scissors-personal.json · ~/.claude/live-spec/profile.md · ~/.claude/plugins/installed_plugins.json · ~/.live-spec-pack

## What each missing target actually is (observation only — no repair proposed)

Every one of the 123 targets was checked against the live-spec repository itself. With the five illustrative examples already excluded, none of the 123 point at something that exists nowhere at all — each falls into one of three classes:

**Would be resolved by shipping it (96 of 123 targets, the large majority).** These are real files that sit in the live-spec repository right now — under `scripts/`, `guardrails/`, `docs/`, `templates/`, `tests/`, `evals/`, `adopt/ADOPT.md`, `adopt/START.md`, `attic/MANIFEST.md`, `install.sh`, `.claude-plugin/marketplace.json` — and simply never get copied by `install.sh` or `install-session-hooks.sh`, which vendor only `skills/` and `hooks/`. Every `scripts/check-*.py`, `guardrails/check-*.py`, and doc under `docs/` in the list above exists in the repository today. A person who instead used `/plugin install` may fare differently — the README says that path "puts the whole tree under `~/.claude/plugins/cache/`" — but that path was not part of this simulation (it is a Claude Code marketplace mechanism, not a shell script this census can run offline).

**Would not be resolved by shipping anything — the name only becomes real once a project attaches (19 targets).** `ARCHITECTURE.md`, `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`, `ROADMAP.md`, `TEST_MATRIX.md`, `MIGRATION.md`, `DECISIONS.md`, `FEEDBACK.md`, `JOURNAL.md`, `NEXT_STEPS.md`, `SURFACES.md`, `PROBLEMS.md`, `.live-spec/PROBLEMS.md`, `.live-spec/profile.md`, `.live-spec/agent.md`, `.live-spec/logs/suite.log`, `guardrails.config.json`, `CHANGELOG.md`, and `.git/hooks/pre-push` are the generic names of documents the setup walk writes inside whatever project a person later says "attach live-spec to this project" in. No file the pack could vendor into a bare `$HOME` would satisfy these — a fresh, project-less install has no project for them to belong to. Making the reference itself clearer that it names a future host-project file, not a pack file, is the only route available to this class — a wording change, not a shipping one.

**Neither — intentionally outside what this pack ships (8 targets).** `PLAYBOOK.md` names the owner's separate private playbook repository, explicitly said so in the text next to it. `CLAUDE.md` and `~/.claude/CLAUDE.md` name the person's own root config file, which the pack deliberately treats as a thin loader it never writes. `~/.claude/hooks/scissors-personal.json`, `~/.claude/hooks/hedge-personal.json`, and `~/.claude/hooks/affirmation-personal.json` are the personal-overlay files the hook scripts' own comments say they "never create or modify." `~/.live-spec-pack` names an alternative clone location the text offers as an instruction, not a promised artifact. `~/.claude/plugins/installed_plugins.json` is a Claude Code platform file, not something live-spec writes. These references already read correctly as written; nothing here calls for either shipping or rewording.

## Why my count differs from the audit's 183

The audit of 2026-08-08 states 183 dangling references; this census found 219 (224 raw hits, minus 5 confirmed illustrative examples in the prose). I do not have the audit's own script or file list to compare line for line, so I can't point to the exact cause of the 36-reference gap. Candidates, from building this scan by hand: which installers count as "the install" (I included both the README's documented `install.sh` and the undocumented-in-README `install-session-hooks.sh`, since the task named the latter explicitly; a narrower audit scoped to `install.sh` alone would count skill files only, but hooks referencing their own missing personal-overlay files would then also disappear from the count); whether a bare filename mention (`check-vocabulary.py`) and its directory-qualified twin (`guardrails/check-vocabulary.py`) appearing in the same document count as one broken reference or two (this census counts both, since they are two different literal strings a reader would follow differently); and whether host-project-relative doc names like `PRODUCT_SPEC.md` count at all, given they are not really broken so much as not-yet-created. Any of these scoping choices, made differently, plausibly closes most of the gap.
