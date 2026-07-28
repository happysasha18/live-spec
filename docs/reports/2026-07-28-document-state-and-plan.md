# Every document, where it stands, and the plan — 2026-07-28

## The answer first

Four documents carry no finding at all, out of 107 the measure reads. They are the two text skills and
their READMEs, cleared this afternoon. Every other live document still carries findings, and the
repository's count stands at 4827, down from 5429 this morning.

The count fell for three reasons, and only one of them is rewriting. Two checkers were reporting
defects the text never had: the person rule read explanatory prose as if it were a numbered
requirement, and the style lint read fenced code blocks as prose. Both are repaired, with a proof in
each direction.

The plan below runs the documents in the order a reader meets them, rather than in the order of their
counts, and it arms a gate so a cleared document stays cleared.

## The four that stand clean

| document | this morning | now |
|---|---:|---:|
| `skills/product-prover/SKILL.md` | 253 | 0 |
| `skills/product-prover/README.md` | 40 | 0 |
| `skills/text-audit/SKILL.md` | 53 | 0 |
| `skills/text-audit/README.md` | 14 | 0 |

Clean here means the machine bar: no sentence past the 25-word cap, no style finding, no register
finding. The reader bar stands separately, and no document has reached it yet.

## The two bars, and why both are needed

**The machine bar** is the census: sentence length, style, register. A script settles it in seconds, and
it is the bar the four documents above now meet.

**The reader bar** is two consecutive readings by a stranger with zero blocking findings. It is the bar
the audit skill states, and it is the one that decides whether an agent can build from the text. Nine
readings on one page in July never approached it.

The counts below measure the first bar. They say nothing about the second.

## What the count does not measure

The readability plan of this morning names six groups of defect. The two that stop an agent from
building are a set the text points at and never gives, and a word used before anything explains it.
No script counts either one. A probe over the spec returned 139 matches for the second and the visible
ones were mostly false.

So a document at zero on the machine bar can still stop a reader. The order below is built on who reads
a document and how often, and the reader bar is what closes each one.

## What is inside the measure, and what is outside it

The repository holds 943 markdown files. 721 of them are records of something that happened: a
journal entry, a prover record, a reading, an archived queue page. A record states what was written at
the time, so the rules bind it when it is written and never afterwards. 100 more are scaffold for a
host to copy.

107 files are live text a reader is held to, and those are the ones the census reads. Every one of them
is in the table below.

### Every live document, worst first

| document | kind | reader | findings | of which long | longest sentence | style | this morning |
|---|---|---|---:|---:|---:|---:|---:|
| `PRODUCT_SPEC.md` | spec | agent-building | 1831 | 1831 | 80 | 0 | — |
| `skills/build-pipeline/SKILL.md` | skill-body | agent-building | 262 | 139 | 198 | 123 | 273 |
| `skills/live-spec-base/SKILL.md` | skill-body | agent-building | 229 | 141 | 97 | 88 | 243 |
| `ROADMAP.md` | queue | agent-building | 215 | 8 | 242 | 207 | 220 |
| `skills/communicator/SKILL.md` | skill-body | agent-building | 182 | 87 | 105 | 95 | 202 |
| `skills/spec-author/SKILL.md` | skill-body | agent-building | 117 | 117 | 121 | 0 | — |
| `docs/prior-art-frameworks.md` | record | human | 112 | 7 | 42 | 105 | 114 |
| `docs/language-rule-coverage.md` | reader-doc | agent-building | 105 | 83 | 81 | 22 | 107 |
| `ARCHITECTURE.md` | architecture | agent-building | 88 | 88 | 870 | 0 | — |
| `docs/restyle-repoint-log.md` | record | maintainer | 83 | 20 | 78 | 63 | — |
| `docs/prior-art-longtail.md` | record | record | 78 | 15 | 53 | 63 | 83 |
| `skills/design-reviewer/SKILL.md` | skill-body | agent-building | 77 | 70 | 92 | 7 | 85 |
| `TEST_MATRIX.md` | test-matrix | agent-building | 76 | 8 | 46 | 68 | 79 |
| `skills/publish/SKILL.md` | skill-body | agent-building | 66 | 33 | 85 | 33 | 68 |
| `docs/spec-style.md` | spec | agent-building | 65 | 32 | 64 | 33 | — |
| `skills/test-author/SKILL.md` | skill-body | agent-building | 57 | 38 | 91 | 19 | 58 |
| `skills/build-pipeline/references/delegation-protocol.md` | reader-doc | agent-building | 52 | 28 | 71 | 24 | 53 |
| `guardrails/README.md` | reader-doc | maintainer | 49 | 30 | 68 | 19 | 54 |
| `adopt/ADOPT.md` | other | host-agent | 46 | 46 | 93 | 0 | — |
| `docs/language-rules.md` | spec | agent-building | 43 | 35 | 95 | 8 | 46 |
| `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | record | maintainer | 41 | 14 | 65 | 27 | — |
| `docs/lenses.md` | record | maintainer | 39 | 37 | 49 | 2 | — |
| `templates/ARCHITECTURE.template.md` | template | agent-building | 39 | 23 | 51 | 16 | 40 |
| `docs/decisions/2026-07-07-morning-round3.md` | record | human | 38 | 6 | 64 | 32 | — |
| `docs/language-defects.md` | record | maintainer | 38 | 34 | 78 | 4 | — |
| `hooks/conduct-law.md` | reader-doc | agent-building | 38 | 11 | 72 | 27 | — |
| `docs/spec-compaction-protocol.md` | spec | agent-building | 36 | 11 | 60 | 25 | — |
| `docs/roadmap-format.md` | spec | agent-building | 33 | 33 | 60 | 0 | — |
| `docs/test-matrix-format.md` | spec | agent-building | 33 | 32 | 59 | 1 | — |
| `docs/prose-quality-gate-design.md` | plan | maintainer | 32 | 9 | 65 | 23 | 34 |
| `docs/decisions/2026-07-06-overnight-decisions.md` | record | human | 31 | 8 | 51 | 23 | 38 |
| `inbox/README.md` | reader-doc | maintainer | 31 | 28 | 75 | 3 | 35 |
| `skills/feedback-intake/SKILL.md` | skill-body | agent-building | 25 | 14 | 48 | 11 | 26 |
| `skills/communicator/references/field-examples.md` | reader-doc | agent-building | 21 | 17 | 51 | 4 | 32 |
| `skills/feedback-collector/SKILL.md` | skill-body | agent-building | 21 | 4 | 41 | 17 | 23 |
| `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | record | maintainer | 19 | 9 | 60 | 10 | 20 |
| `docs/wishes/2026-07-09-prover-unwritten-seams.md` | record | maintainer | 18 | 9 | 59 | 9 | — |
| `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | record | maintainer | 18 | 6 | 36 | 12 | — |
| `docs/worker-liveness.md` | reader-doc | agent-building | 17 | 16 | 52 | 1 | — |
| `templates/agent.template.md` | template | agent-building | 17 | 10 | 47 | 7 | 19 |
| `README.md` | reader-doc | human | 16 | 16 | 88 | 0 | 29 |
| `docs/architecture-format.md` | spec | agent-building | 16 | 16 | 49 | 0 | — |
| `docs/migration-sample/2026-07-20-backdescribe-sample.md` | template | human | 16 | 8 | 76 | 8 | 22 |
| `docs/spec-format.md` | spec | agent-building | 16 | 15 | 98 | 1 | 18 |
| `skills/design-reviewer/README.md` | skill-readme | human | 16 | 16 | 55 | 0 | 21 |
| `docs/test-method.md` | reader-doc | agent-building | 15 | 15 | 52 | 0 | — |
| `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | record | maintainer | 14 | 7 | 54 | 7 | — |
| `scripts/judge-rubric.md` | template | agent-building | 13 | 0 | 25 | 13 | — |
| `skills/build-pipeline/references/work-kind-table.md` | reader-doc | agent-building | 13 | 0 | 22 | 13 | — |
| `docs/architecture-method.md` | reader-doc | agent-building | 12 | 12 | 47 | 0 | — |
| `templates/ROADMAP.template.md` | template | agent-building | 12 | 12 | 74 | 0 | — |
| `NEXT_STEPS.md` | resume-file | agent-building | 11 | 11 | 39 | 0 | 12 |
| `skills/build-pipeline/references/guardrails-catalog.md` | reader-doc | agent-building | 11 | 2 | 76 | 9 | 12 |
| `skills/communicator/references/page-lifecycle.md` | reader-doc | agent-building | 11 | 11 | 50 | 0 | — |
| `skills/spec-author/README.md` | skill-readme | human | 11 | 11 | 52 | 0 | 16 |
| `docs/onboarding-and-settings.md` | reader-doc | agent-building | 10 | 10 | 53 | 0 | — |
| `docs/plans/2026-07-28-top-level-readability.md` | plan | agent-building | 10 | 6 | 51 | 4 | — |
| `skills/build-pipeline/README.md` | skill-readme | human | 10 | 9 | 60 | 1 | 15 |
| `skills/communicator/references/writing-register.md` | reader-doc | agent-building | 10 | 8 | 45 | 2 | 15 |
| `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | record | maintainer | 9 | 5 | 35 | 4 | — |
| `OVERVIEW.md` | reader-doc | human | 8 | 8 | 67 | 0 | 9 |
| `docs/language-worked-example.md` | reader-doc | agent-building | 8 | 6 | 41 | 2 | 9 |
| `docs/pipeline.md` | reader-doc | agent-building | 8 | 8 | 44 | 0 | — |
| `docs/spec-format-by-project-type.md` | plan | maintainer | 8 | 2 | 41 | 6 | 13 |
| `skills/test-author/README.md` | skill-readme | human | 8 | 4 | 35 | 4 | 12 |
| `docs/pair-adoption.md` | reader-doc | host-agent | 7 | 7 | 47 | 0 | — |
| `scripts/read-grant-ask.md` | template | human | 7 | 3 | 28 | 4 | — |
| `skills/build-pipeline/references/drafter-applier-example.md` | reader-doc | agent-building | 7 | 3 | 67 | 4 | — |
| `templates/PRODUCT_SPEC.template.md` | template | agent-building | 7 | 6 | 32 | 1 | 8 |
| `templates/TEST_MATRIX.template.md` | template | agent-building | 7 | 5 | 95 | 2 | — |
| `docs/adoption.md` | reader-doc | host-agent | 6 | 6 | 51 | 0 | — |
| `docs/push-law.md` | reader-doc | agent-building | 6 | 5 | 53 | 1 | — |
| `skills/feedback-intake/README.md` | skill-readme | human | 6 | 6 | 35 | 0 | 8 |
| `skills/publish/README.md` | skill-readme | human | 6 | 2 | 40 | 4 | — |
| `templates/DECISIONS.template.md` | template | human | 5 | 1 | 36 | 4 | 14 |
| `templates/JOURNAL.template.md` | template | agent-building | 5 | 0 | 24 | 5 | 6 |
| `templates/NEXT_STEPS.template.md` | template | agent-building | 5 | 1 | 27 | 4 | — |
| `templates/PROBLEMS.template.md` | template | agent-building | 5 | 0 | 25 | 5 | — |
| `skills/build-pipeline/references/minor-bump-gate.md` | reader-doc | agent-building | 4 | 4 | 65 | 0 | — |
| `templates/KILL_LIST.template.md` | template | agent-building | 4 | 0 | 16 | 4 | — |
| `templates/profile.template.md` | template | human | 4 | 2 | 72 | 2 | — |
| `SURFACES.md` | other | maintainer | 3 | 1 | 26 | 2 | 4 |
| `docs/norms/onboarding-card-2026-07-10.provenance.md` | record | record | 3 | 3 | 35 | 0 | — |
| `scripts/grant-ask.md` | template | human | 3 | 0 | 19 | 3 | — |
| `skills/build-pipeline/references/request-kind-table.md` | reader-doc | agent-building | 3 | 1 | 28 | 2 | — |
| `skills/communicator/README.md` | skill-readme | human | 3 | 2 | 37 | 1 | 8 |
| `skills/feedback-collector/README.md` | skill-readme | human | 3 | 2 | 32 | 1 | 9 |
| `skills/build-pipeline/references/excuses-table.md` | reader-doc | agent-building | 2 | 0 | 18 | 2 | 4 |
| `templates/skill-review.template.md` | template | agent-building | 2 | 0 | 14 | 2 | — |
| `docs/prior-art.md` | record | human | 1 | 0 | 17 | 1 | — |
| `guardrails/release-note-fixtures/note-neither.md` | scaffold | maintainer | 1 | 1 | 28 | 0 | — |
| `guardrails/release-note-fixtures/note-offers.md` | scaffold | maintainer | 1 | 1 | 30 | 0 | 4 |
| `skills/live-spec-base/README.md` | skill-readme | human | 1 | 1 | 28 | 0 | — |
| `PRODUCT_SPEC.index.md` | generated-page | maintainer | **clean** | 0 | 0 | 0 | — |
| `guardrails/far-tier-fixtures/report-names-far-in-runnable.md` | scaffold | maintainer | **clean** | 0 | 14 | 0 | — |
| `guardrails/far-tier-fixtures/report-runnable-no-standdown.md` | scaffold | maintainer | **clean** | 0 | 9 | 0 | — |
| `guardrails/far-tier-fixtures/report-stands-far-down.md` | scaffold | maintainer | **clean** | 0 | 14 | 0 | — |
| `guardrails/far-tier-fixtures/vocab-clean.md` | scaffold | maintainer | **clean** | 0 | 15 | 0 | — |
| `guardrails/far-tier-fixtures/vocab-deferred-without-trigger.md` | scaffold | maintainer | **clean** | 0 | 10 | 0 | — |
| `guardrails/far-tier-fixtures/vocab-far-with-trigger.md` | scaffold | maintainer | **clean** | 0 | 15 | 0 | — |
| `guardrails/far-tier-fixtures/window-first-offer-after-window.md` | scaffold | maintainer | **clean** | 0 | 12 | 0 | — |
| `guardrails/far-tier-fixtures/window-second-offer-in-window.md` | scaffold | maintainer | **clean** | 0 | 12 | 0 | — |
| `guardrails/release-note-fixtures/note-no-offer.md` | scaffold | maintainer | **clean** | 0 | 21 | 0 | — |
| `skills/product-prover/README.md` | skill-readme | human | **clean** | 0 | 25 | 0 | 15 |
| `skills/product-prover/SKILL.md` | skill-body | agent-building | **clean** | 0 | 25 | 0 | 27 |
| `skills/text-audit/README.md` | skill-readme | human | **clean** | 0 | 25 | 0 | 8 |
| `skills/text-audit/SKILL.md` | skill-body | agent-building | **clean** | 0 | 25 | 0 | 36 |

### The twenty worst sections, by their own body

| section | document | lines | findings |
|---|---|---:|---:|
| # live-spec Roadmap (dated version: 2026-07-23 — updated at every edit; SPEC M-3 | `ROADMAP.md` | 180 | 220 |
| ## The shared rules | `skills/live-spec-base/SKILL.md` | 441 | 197 |
| ## Glossary | `PRODUCT_SPEC.md` | 251 | 119 |
| ## The steps | `skills/build-pipeline/SKILL.md` | 256 | 113 |
| ## Verdict table | `docs/prior-art-frameworks.md` | 27 | 72 |
| ## When to run it — and where each kind of change enters | `skills/build-pipeline/SKILL.md` | 104 | 62 |
| # Junior delegation protocol | `skills/build-pipeline/references/delegation-protocol.md` | 97 | 53 |
| ## Gates worth remembering | `skills/build-pipeline/SKILL.md` | 113 | 50 |
| ### How to show it | `skills/communicator/SKILL.md` | 87 | 41 |
| ### Whether and when to show | `skills/communicator/SKILL.md` | 122 | 39 |
| (opening) | `hooks/conduct-law.md` | 44 | 38 |
| # inbox — parallel-safe intake for wishes and feedback | `inbox/README.md` | 135 | 35 |
| ## The rules | `docs/spec-style.md` | 23 | 35 |
| # Lens & rule origins | `docs/lenses.md` | 290 | 35 |
| ## The pre-report walk — run before any movement-end or milestone report, and be | `skills/communicator/SKILL.md` | 51 | 30 |
| ### Asking for a decision | `skills/communicator/SKILL.md` | 57 | 29 |
| ## The facet sweep — run when a wish's door says feature (SPEC T-13, INV-18) | `skills/spec-author/SKILL.md` | 116 | 28 |
| # live-spec — spec-style round 3 (2026-07-07 morning, session 23) | `docs/decisions/2026-07-07-morning-round3.md` | 62 | 22 |
| ## The kind checklist — what every publication owes (one home: this table) | `skills/publish/SKILL.md` | 50 | 21 |
| ## The rules it holds a text to | `skills/text-audit/SKILL.md` | 97 | 20 |


## The plan

### Order

The order runs from the documents read every day to the ones read once:

1. **The prose inside the rule home.** `guardrails/language-rules.json` generates the writer's page,
   the maintainer's page, and the rules block inside the audit skill. A hand edit in a generated page
   is erased by the next build, so its prose is repaired in the source.
2. **The front door.** `README.md`, `OVERVIEW.md`, `adopt/ADOPT.md`. A stranger meets these first, and
   no cold reading has ever been run on them.
3. **The skill bodies loaded in every session**: `live-spec-base`, `build-pipeline`, `communicator`.
   Together they carry 673 findings, and an agent reads them before every non-trivial change.
4. **The requirements the documents above point a reader at.** These are what a host's agent meets on
   its first build.
5. **The rest of the spec**, worst first.

### The stages, per document

Each stage is one worker, and the documents are independent, so they run in parallel:

1. the mechanical lints, repaired to zero, with meaning held;
2. the check: counters at zero, the suite green, every phrase a test pins still present;
3. a cold reading by a fresh worker with no pack loaded;
4. the repair of each blocking stop, taken from the source, with a real hole recorded as a question;
5. stages 3 and 4 again, until two readings in a row return nothing that blocks;
6. the gate, so the document cannot regress.

### Three things that make the campaign possible

**The tests pin raw lines.** 79 test files read document text, 72 call a helper named `flat`, and 4 of
those helpers collapse whitespace. In the rest, a repaired sentence that re-wraps fails a test. Twelve
failed that way today. One pass over the helpers removes that failure mode.

**The counters need a gate.** Nothing refuses a document whose count rose. The census prints a report
and the push proceeds. A per-file bound in the push gate turns each cleared document into a floor.

**The build test needs a record.** The plan's own baseline, two of six requirements implemented by a
fresh agent, is stated in the plan with no record naming which six, which agent, or what it produced.
Without that record the before-and-after comparison the plan promises cannot be honoured.

### The cost, measured on today

Four documents went from 360 findings to zero in about one hour, and half of that hour repaired the two
checkers, which now serves every remaining file. The heading rename across eleven skills took one
worker eight minutes, including the push gate it would have turned red.

The cold reading has no measured cost yet, because no document has been through it end to end. The
front door is the place to measure it.

### The one decision

The machine bar over the whole live set is affordable. The reader bar is two workers per section,
repeated until two clean readings, and its cost is unmeasured.

The recommendation: run the machine bar over the whole live set, and the reader bar over the front door
and the skill bodies alone. The spec's requirements take the reader bar only where a document points a
host's agent at them.
