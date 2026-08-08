# Day 1 census — every rule in skills/live-spec-base/SKILL.md, traced

Root: Alexander's order of 2026-08-08 22:17 and the approved culling plan `.live-spec/culling-plan-2026-08-08.md`, day 1. This is a census only: one row per rule, its own plain-English restatement, its byte size inside `skills/live-spec-base/SKILL.md`, and every place it is wired, found by grepping its identifiers (its SPEC INV codes, the literal phrase "rule N", and any distinctive script name it names) across `tests/`, `guardrails/`, `scripts/`, `skills/`, `docs/`, `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`, `ROADMAP.md`. No change is proposed to any rule; no new check is added; no plan is edited. Version measured: `skills/live-spec-base/SKILL.md` v4.3.0, thirty-five rules in the body (lines 110-641).

**How a hit is classified.** A test-file hit is reported with the enclosing `def test_*` function name(s); a hit outside any function is marked module-level. A guardrail-script hit (`guardrails/*.py`, `*.sh`, `*.json`) and a pipeline-script hit (`scripts/`, `hooks/`) are reported by path. A doc hit under `docs/` is split into two kinds, both listed in full — **living docs**, the pack's own current guidance (`docs/pipeline.md`, `docs/adoption.md`, and siblings), reported with every line number; and **historical/record docs** — `docs/prover/`, `docs/design/`, `docs/research/`, `docs/audit/`, `docs/handovers/`, `docs/attic/`, `docs/queue-archive/`, `docs/reports/`, `docs/measure/`, `docs/gate-audit/`, `docs/briefs/`, `docs/push-review/`, `docs/skill-review/`, `docs/language-reads/`, `docs/evals/` — reported by path with a line-hit count, since these are dated records of a past pass (the same split `scripts/rule-census.py` already draws for its own, unrelated census, on the same reasoning: a record states what was written at the time and is never swept when a live rule changes). This split is a classification of the grep hits actually found, not a judgment about which rule to keep. The four root documents (`PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`, `ROADMAP.md`) are living and always reported with line numbers. The rule's own text in `skills/live-spec-base/SKILL.md` is excluded from its own trace count — it is the rule, not a wiring of it.

**Known measurement caveat — a code collision, found and left visible, not filtered out.** `tests/fixtures/specformat/` holds format-lint fixtures that invent small sequential codes `INV-1` through `INV-7` purely to exercise the spec-format linter's mechanics (bullet shape, readability, history, vocabulary) — they are not excerpts of this pack's real invariant registry. Base rule 1 carries `INV-4` and `INV-5`, and base rule 10 carries `INV-7`, in its own real text; where those exact numbers recur as placeholders in that fixture set, the grep still fires and the hit is still listed below, marked SYNTHETIC in place. One fixture in the same directory, `good_corpus_section.md`, is different: it is a verbatim copy of real `PRODUCT_SPEC.md` prose used to test the lint against a known-good corpus, so its INV codes (including `INV-135`, `INV-136`, `INV-139`, `INV-107`, `INV-56`, `INV-84`, and others) are real citations and are left unflagged.

## Compact table

| # | identifier | what it demands (own words) | bytes | test files | guardrail scripts | pipeline scripts | other skills | living docs | historical docs | root docs |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | base rule 1 — (no heading SPEC code — body cites INV-12, INV-121, INV-4, INV-5) | Ask the human only what only they can answer; never invent intent or offer a fork the artifacts already settle. | 929 | 19 | 4 | 3 | 7 | 4 | 87 | 4 |
| 2 | base rule 2 — (no heading SPEC code — body cites INV-8) | Human-facing text stands alone in plain product language; codes/jargon trail quietly, never open a sentence, never get loan-translated. | 947 | 4 | 0 | 0 | 4 | 0 | 20 | 3 |
| 3 | base rule 3 — (carries no SPEC INV code) | One thing keeps exactly one name everywhere, drawn from the host spec's own vocabulary. | 189 | 0 | 0 | 0 | 2 | 1 | 0 | 1 |
| 4 | base rule 4 — (carries no SPEC INV code) | Every fact has one canonical home; every other mention is a pointer, kept live when the home moves. | 300 | 1 | 1 | 0 | 3 | 1 | 27 | 3 |
| 5 | base rule 5 — SPEC INV-69 | The seat orchestrates and briefs; each unit of work routes to the cheapest tier that can pass it, logged. | 1107 | 8 | 1 | 0 | 7 | 4 | 69 | 4 |
| 6 | base rule 6 — (no heading SPEC code — body cites INV-107, INV-76, INV-95) | Long or delegated work keeps a disk checkpoint (done/in-progress/next) so a cutoff resumes cleanly; red is never committed. | 1860 | 7 | 1 | 0 | 6 | 4 | 31 | 4 |
| 7 | base rule 7 — (no heading SPEC code — body cites ACT-3, E-13, INV-10, INV-105, INV-11, INV-117, INV-214, INV-298, INV-39, INV-49, INV-76, T-18) | Before every write and commit, re-check git status/HEAD; parallel lanes, worktrees, and worker restores follow a strict collision-avoidance set. | 5477 | 17 | 7 | 3 | 10 | 14 | 145 | 4 |
| 8 | base rule 8 — (no heading SPEC code — body cites A-7, M-7) | Re-read skill/pack/profile modification times at every breakpoint; journal the old-to-new change on any version bump. | 316 | 5 | 1 | 1 | 2 | 3 | 47 | 3 |
| 9 | base rule 9 — (carries no SPEC INV code) | Dated reasons live in JOURNAL.md; SPEC/NEXT_STEPS/ROADMAP state only current truth; shipped docs update the same session. | 678 | 0 | 0 | 0 | 3 | 1 | 22 | 1 |
| 10 | base rule 10 — (no heading SPEC code — body cites A-4, A-9, INV-7) | Nothing is silently deleted; a superseded file moves to the attic with a manifest line, and only regenerable junk is dropped, with approval. | 304 | 8 | 3 | 2 | 4 | 2 | 43 | 4 |
| 11 | base rule 11 — (carries no SPEC INV code) | "Works" is said only after running it and seeing the result; synthetic data always carries the label SYNTHETIC. | 362 | 2 | 0 | 0 | 3 | 0 | 9 | 1 |
| 12 | base rule 12 — (carries no SPEC INV code) | Irreversible, authored-content, publishing, push-gated, and taste decisions go to the human; everything else proceeds and gets reported. | 310 | 2 | 0 | 0 | 3 | 0 | 9 | 0 |
| 13 | base rule 13 — (no heading SPEC code — body cites INV-205, INV-206, INV-207) | Every factual claim traces to a primary source (file:line, commit, command output); a human-attributed decision needs a dated, checkable exchange. | 2028 | 6 | 7 | 0 | 6 | 0 | 43 | 4 |
| 14 | base rule 14 — (no heading SPEC code — body cites INV-124) | A found defect is one sample of a class; name the class, sweep every look-alike in the same change. | 1929 | 2 | 0 | 0 | 6 | 1 | 37 | 4 |
| 15 | base rule 15 — (no heading SPEC code — body cites INV-16, INV-22, T-12, T-16) | Every request is classified by entry door (feature/bug/refactor/docs-only/skip) and work-kind before the first line of code. | 1371 | 5 | 0 | 0 | 10 | 3 | 71 | 4 |
| 16 | base rule 16 — (no heading SPEC code — body cites E-17, INV-17) | A prototype stays fenced and labelled in prototype/, never wired into production; promotion re-enters through the spec step. | 875 | 4 | 2 | 1 | 8 | 1 | 31 | 3 |
| 17 | base rule 17 — (carries no SPEC INV code) | Truly irreversible acts (spend, delete, unsendable send) always stop for the human's word; a repo push is not irreversible. | 570 | 3 | 3 | 0 | 5 | 0 | 19 | 1 |
| 18 | base rule 18 — (carries no SPEC INV code) | A taken filename differentiates first by its home's own semantic mark, then by a numeric ordinal; never overwrite. | 766 | 2 | 0 | 1 | 3 | 0 | 16 | 1 |
| 19 | base rule 19 — (no heading SPEC code — body cites E-24, INV-23, INV-56) | Operational noise gets a WATCHED line on first sight; a repeat gets a named owner; an owned problem never blocks unrelated work. | 1723 | 6 | 0 | 1 | 6 | 2 | 39 | 4 |
| 20 | base rule 20 — SPEC INV-65 | At setup or a repeated struggle, search installed skills and catalogs for a fit before building something new. | 838 | 1 | 0 | 0 | 1 | 2 | 18 | 4 |
| 21 | base rule 21 — SPEC INV-84 | Durable human-facing prose is drafted by a fresh, rule-free writer session from a brief, never written by the author directly. | 820 | 3 | 0 | 0 | 2 | 2 | 22 | 3 |
| 22 | base rule 22 — SPEC INV-98 | Name a concrete goal artifact up front; measure every iteration against that goal itself, never a proxy; lock gains by a mechanism. | 1219 | 2 | 0 | 0 | 1 | 2 | 21 | 3 |
| 23 | base rule 23 — SPEC INV-108 | A behavioural rule that breaks mid-turn a second time earns a live channel: a prompt hook or a mechanical red check. | 1198 | 2 | 0 | 0 | 0 | 1 | 24 | 3 |
| 24 | base rule 24 — SPEC INV-135 | The pipeline's stations are kind-abstract; each project kind fills them with its own concrete layers and proof kinds. | 2087 | 9 | 3 | 1 | 4 | 3 | 31 | 4 |
| 25 | base rule 25 — SPEC INV-137 | The lead's context holds only orchestration essentials; reads done to discover or understand are dispatched to a worker for distillation. | 1981 | 8 | 0 | 0 | 2 | 3 | 49 | 3 |
| 26 | base rule 26 — SPEC INV-136, INV-139 | Beside its layers and proofs, a project kind names checkable design principles that the verify pass runs. | 679 | 10 | 3 | 2 | 6 | 4 | 40 | 4 |
| 27 | base rule 27 — SPEC INV-143 | The seat decides mechanical steps, artifact-determined values, and sensible defaults; only genuine taste, trade-off, or correctness calls reach the human. | 710 | 19 | 4 | 3 | 5 | 5 | 98 | 4 |
| 28 | base rule 28 — SPEC INV-145 | Beyond the continuous lints, a full adversarial whole-read audit of the living documents runs every ten landings. | 1121 | 14 | 1 | 1 | 1 | 5 | 120 | 4 |
| 29 | base rule 29 — SPEC INV-152 | A parked, needs-the-human's-word item is re-tested for derivability every time it's touched; an unjustified marker defaults to the seat's own work. | 2138 | 25 | 7 | 5 | 8 | 14 | 104 | 4 |
| 30 | base rule 30 — SPEC INV-164 | Any property a machine can verify becomes a blocking gate run on every push, held by no one's attention. | 939 | 14 | 10 | 0 | 3 | 5 | 49 | 4 |
| 31 | base rule 31 — SPEC INV-183, INV-189 | Agents talk on exactly two channels, inbox and published contract; a message must name the sender's own real blocked work. | 6067 | 17 | 8 | 4 | 3 | 4 | 49 | 4 |
| 32 | base rule 32 — SPEC INV-217 | A release's patch/minor/major number is judged by what taking it costs a host, a stated call the session makes. | 2205 | 12 | 3 | 3 | 5 | 3 | 59 | 4 |
| 33 | base rule 33 — SPEC INV-237 | The seat that authored a change never supplies that change's own adversarial certification; a fresh, differently-contexted seat runs it. | 1445 | 9 | 4 | 0 | 2 | 3 | 93 | 4 |
| 34 | base rule 34 — SPEC INV-247 | Before a deferred item's work resumes, its technical premise is re-checked against the current shipped code, not the stale record. | 1084 | 5 | 2 | 0 | 2 | 1 | 18 | 4 |
| 35 | base rule 35 — SPEC INV-302 | A fresh agent, never the session that lived it, reads and writes both ends of a session's record, from a transcript extract. | 1815 | 3 | 2 | 1 | 0 | 0 | 16 | 4 |

## Per-rule traces

### Rule 1 — (no heading SPEC code — body cites INV-12, INV-121, INV-4, INV-5)

**Demands:** Ask the human only what only they can answer; never invent intent or offer a fork the artifacts already settle.

**Size:** 929 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-12, INV-121, INV-4, INV-5; literal phrase "rule 1".

**TRACES — test files (19, of which 10 are synthetic-placeholder noise, see below):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/fixtures/specformat/mini_added.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/mini_added_oversized.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/mini_budget_over.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/mini_sharpened_survives.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_bullets_clean.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_bullets_dirty.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_clean.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_dirty.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/rec_added_new.json` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/rec_sharpen_survives.json` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/test_board.py` — test_gate_reds_a_parked_question_with_no_default
- `tests/test_criterion_readability.py` — test_a_bullet_carrying_a_bracket_code_reds_the_anchor_noise_arm, test_the_shared_parser_hands_a_criterion_its_bullets_and_its_pieces
- `tests/test_delta_classifier.py` — test_appeared_undeclared_reds
- `tests/test_derive_before_fork.py` — test_formal_index_row, test_spec_clause_stands
- `tests/test_impact_analysis_entry.py` — test_spec_cites_derive_before_fork
- `tests/test_index_generated.py` — test_reds_a_body_code_the_index_misses
- `tests/test_seat_acts_by_default.py` — test_spec_invariant_143_present_and_indexed
- `tests/test_traceability.py` — test_parameter_default, test_spec_states_founding_and_designsync

**TRACES — guardrail scripts (4):**
- `guardrails/check-board.py`
- `guardrails/check-delta-record.py`
- `guardrails/route_agent_transport.py`
- `guardrails/specformat.py`

**TRACES — pipeline scripts/hooks (3):**
- `scripts/gate_common.py`
- `scripts/measurements-table.py`
- `scripts/spec-style-lint.py`

**TRACES — other skill files (7):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/excuses-table.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/writing-register.md`
- `skills/design-reviewer/SKILL.md`
- `skills/feedback-intake/SKILL.md`
- `skills/product-prover/SKILL.md`

**TRACES — root documents (4 files, 77 lines):**
- `ARCHITECTURE.md`:57, 145
- `PRODUCT_SPEC.md`:405, 451, 458, 463, 464, 480, 485, 486, 500, 501, 502, 542, 609, 715, 742, 754, 933, 984, 1084, 1147, 1199, 1219, 1234, 1291, 1415, 1443, 1677, 1678, 1738, 1789, 1805, 1853, 1854, 1901, 2070, 2092, 3465, 3628, 3663, 3706, 3895, 3901, 4550, 4897, 5081, 5086, 5087, 5101, 5109, 5264, 5757, 7908, 7909, 7916, 8025
- `ROADMAP.md`:129
- `TEST_MATRIX.md`:144, 175, 177, 282, 289, 290, 291, 324, 325, 333, 334, 335, 413, 526, 604, 874, 875, 882, 991

**TRACES — living docs (4 files, 5 lines):**
- `docs/lenses.md`:172
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:56
- `docs/plans/2026-07-29-specification-subdivision.md`:219, 287
- `docs/spec-style.md`:145

**TRACES — historical/record docs (87 files, 235 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (54 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (15 line-hits)
- `docs/audit/2026-07-05/pass1-prover-fable.md` (2 line-hits)
- `docs/audit/2026-07-05/pass2-matrix-opus.md` (1 line-hits)
- `docs/audit/2026-07-05/skill-creator-eval-opus.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (4 line-hits)
- `docs/audit/2026-07-16-batch-2p2p0.md` (1 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (1 line-hits)
- `docs/evals/2026-07-05-first-run/bare-spec-author.md` (2 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/bare-spec-author.md` (2 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (2 line-hits)
- `docs/evals/2026-07-06-push-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-06-rerun/scores-build-pipeline.md` (2 line-hits)
- `docs/evals/2026-07-06-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/measure/2026-07-29-specification-size.md` (1 line-hits)
- `docs/prover/2026-07-04-v03-push.md` (1 line-hits)
- `docs/prover/2026-07-04.md` (1 line-hits)
- `docs/prover/2026-07-05-classes.md` (1 line-hits)
- `docs/prover/2026-07-05-doors.md` (1 line-hits)
- `docs/prover/2026-07-05-facets.md` (3 line-hits)
- `docs/prover/2026-07-05-fences.md` (2 line-hits)
- `docs/prover/2026-07-05-founding-designsync.md` (7 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (5 line-hits)
- `docs/prover/2026-07-05-iterativity.md` (1 line-hits)
- `docs/prover/2026-07-05-row100.md` (2 line-hits)
- `docs/prover/2026-07-05-row86.md` (3 line-hits)
- `docs/prover/2026-07-05-row99.md` (2 line-hits)
- `docs/prover/2026-07-05-v05-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v11-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v14-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v15-push.md` (2 line-hits)
- `docs/prover/2026-07-05.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (2 line-hits)
- `docs/prover/2026-07-06-pushgate-s20.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s21-2.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s21.md` (1 line-hits)
- `docs/prover/2026-07-06-row138.md` (2 line-hits)
- `docs/prover/2026-07-06-row140.md` (1 line-hits)
- `docs/prover/2026-07-06-row142.md` (2 line-hits)
- `docs/prover/2026-07-06-row145.md` (2 line-hits)
- `docs/prover/2026-07-06-rows108-119.md` (3 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk1.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk10.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk2.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk3.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk5.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk6.md` (3 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk7.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk9.md` (4 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-11.md` (1 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (1 line-hits)
- `docs/prover/2026-07-09-row187.md` (3 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (2 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (5 line-hits)
- `docs/prover/2026-07-12-s40-inv124-class-hunt.md` (1 line-hits)
- `docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv133-critical-preempt-bound.md` (1 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (2 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (1 line-hits)
- `docs/prover/2026-07-16-prover-doc-restructure.md` (1 line-hits)
- `docs/prover/2026-07-17-lanes-and-self-declaration.md` (5 line-hits)
- `docs/prover/2026-07-18-row-396-transport-split.md` (1 line-hits)
- `docs/prover/2026-07-23-row445-4.0.0-fix-verify.md` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (10 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (10 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/skill-review/2026-07-18-product-prover.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-05-design-reviewer-readability.md` (3 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 2 — (no heading SPEC code — body cites INV-8)

**Demands:** Human-facing text stands alone in plain product language; codes/jargon trail quietly, never open a sentence, never get loan-translated.

**Size:** 947 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-8; literal phrase "rule 2".

**TRACES — test files (4):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_code_anchor_scan.py` — (module-level, no enclosing test_ function)
- `tests/test_register_judge.py` — test_flat_informative_sentence_passes_both
- `tests/test_traceability.py` — test_adopt_phases_cite_spec, test_no_calques_rule, test_outcome_leads_law, test_spec_states_bootstrap_order

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (4):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`
- `skills/publish/SKILL.md`

**TRACES — root documents (3 files, 9 lines):**
- `ARCHITECTURE.md`:244
- `PRODUCT_SPEC.md`:3824, 3829, 3830, 3834, 7912
- `TEST_MATRIX.md`:464, 646, 878

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (20 files, 42 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (5 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (1 line-hits)
- `docs/audit/2026-07-05/skill-creator-eval-opus.md` (1 line-hits)
- `docs/prover/2026-07-04.md` (2 line-hits)
- `docs/prover/2026-07-05-adopt.md` (2 line-hits)
- `docs/prover/2026-07-05-calques-push.md` (11 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (1 line-hits)
- `docs/prover/2026-07-06-row116.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (1 line-hits)
- `docs/prover/2026-07-18-2.8.1-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-05.md` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (5 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 3 — (carries no SPEC INV code)

**Demands:** One thing keeps exactly one name everywhere, drawn from the host spec's own vocabulary.

**Size:** 189 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 3".

**TRACES — test files (0):**
- none found

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (2):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (1 files, 1 lines):**
- `ROADMAP.md`:215

**TRACES — living docs (1 files, 1 lines):**
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:59

**TRACES — historical/record docs (0 files, 0 line-hits, path + count only):**
- none found

---

### Rule 4 — (carries no SPEC INV code)

**Demands:** Every fact has one canonical home; every other mention is a pointer, kept live when the home moves.

**Size:** 300 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 4".

**TRACES — test files (1):**
- `tests/test_description_field.py` — (module-level, no enclosing test_ function)

**TRACES — guardrail scripts (1):**
- `guardrails/check-description-field.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (3):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (3 files, 4 lines):**
- `ARCHITECTURE.md`:731
- `ROADMAP.md`:215
- `TEST_MATRIX.md`:194, 195

**TRACES — living docs (1 files, 1 lines):**
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:63

**TRACES — historical/record docs (27 files, 57 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (9 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (2 line-hits)
- `docs/audit/2026-07-05/skill-creator-eval-opus.md` (1 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (1 line-hits)
- `docs/briefs/2026-07-28-one-ceiling-law-brief.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (2 line-hits)
- `docs/design-review/2026-07-19.md` (2 line-hits)
- `docs/prover/2026-07-06-row142.md` (1 line-hits)
- `docs/prover/2026-07-06-row145.md` (1 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (2 line-hits)
- `docs/prover/2026-07-15-1.8.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-15-327-harness-invariants.md` (3 line-hits)
- `docs/prover/2026-07-15-332-inv163-audit.md` (2 line-hits)
- `docs/prover/2026-07-18-row407-release-tier-rule.md` (2 line-hits)
- `docs/prover/2026-07-19.md` (12 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (1 line-hits)
- `docs/prover/2026-07-20-comms.md` (2 line-hits)
- `docs/prover/2026-07-21-axes-push-recheck.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (2 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (1 line-hits)
- `docs/skill-review/2026-07-18-live-spec-base-build-pipeline.md` (2 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (1 line-hits)

---

### Rule 5 — SPEC INV-69

**Demands:** The seat orchestrates and briefs; each unit of work routes to the cheapest tier that can pass it, logged.

**Size:** 1107 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-46, INV-69; literal phrase "rule 5".

**TRACES — test files (8):**
- `tests/test_chat_law_hook.py` — test_output_carries_the_routing_law
- `tests/test_clean_context_review.py` — (module-level, no enclosing test_ function)
- `tests/test_delegation_trigger_no_size.py` — test_no_pack_skill_states_a_size_or_time_delegation_trigger, test_scan_has_teeth
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_periodic_full_audit.py` — test_audit_is_defined_adversarial_by_nature_once
- `tests/test_rendered_sweep.py` — test_publish_sweeps_the_accumulation_at_a_release
- `tests/test_review_record_class.py` — test_names_every_member
- `tests/test_traceability.py` — test_adversarial_verify_option, test_pair_leadership_law, test_routing_rule, test_rule5_drops_the_three_superseded_bars, test_rule5_states_the_settled_delegation_rule

**TRACES — guardrail scripts (1):**
- `guardrails/check-earned-message.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (7):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/delegation-protocol.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/page-lifecycle.md`
- `skills/communicator/references/words.md`
- `skills/communicator/references/writing-register.md`
- `skills/publish/SKILL.md`

**TRACES — root documents (4 files, 58 lines):**
- `ARCHITECTURE.md`:145, 152, 153, 517, 665, 715
- `PRODUCT_SPEC.md`:639, 664, 1657, 2542, 3034, 4962, 4966, 4967, 5008, 5009, 5013, 5014, 5018, 5019, 5023, 5058, 5059, 5123, 5124, 5128, 5131, 5152, 5170, 5241, 5242, 5276, 5277, 5278, 5488, 5579, 7378, 7709, 7768, 7773, 7950, 7973
- `ROADMAP.md`:85, 115
- `TEST_MATRIX.md`:151, 176, 280, 281, 314, 332, 340, 341, 342, 770, 786, 788, 916, 939

**TRACES — living docs (4 files, 6 lines):**
- `docs/lenses.md`:27
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:66
- `docs/spec-format.md`:34, 42
- `docs/worker-liveness.md`:40, 44

**TRACES — historical/record docs (69 files, 262 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (27 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (9 line-hits)
- `docs/audit/2026-07-08/milestone-audit.md` (2 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (19 line-hits)
- `docs/audit/2026-07-15-1.8.0-audit.md` (1 line-hits)
- `docs/design-review/2026-07-15.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (4 line-hits)
- `docs/language-reads/2026-07-28-read15-campaign-plan.md` (1 line-hits)
- `docs/language-reads/2026-07-28-read16-chat-law-hook.md` (1 line-hits)
- `docs/prover/2026-07-05-row93.md` (2 line-hits)
- `docs/prover/2026-07-06-pushgate-s22-5.md` (2 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (3 line-hits)
- `docs/prover/2026-07-07-row56.md` (10 line-hits)
- `docs/prover/2026-07-07-rows111-113.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (2 line-hits)
- `docs/prover/2026-07-10-row201.md` (1 line-hits)
- `docs/prover/2026-07-12-row253-routing-reminder.md` (2 line-hits)
- `docs/prover/2026-07-12-row254-delegation-check.md` (1 line-hits)
- `docs/prover/2026-07-12-row255-drafter-applier-form.md` (1 line-hits)
- `docs/prover/2026-07-12-row279-adopt-impersonal-voice.md` (2 line-hits)
- `docs/prover/2026-07-12-s40-inv46-audit-trigger-broadened.md` (7 line-hits)
- `docs/prover/2026-07-12-s41-inv134-footprint-note-enforcement.md` (1 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (11 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (7 line-hits)
- `docs/prover/2026-07-13-prover-overlap-lens.md` (1 line-hits)
- `docs/prover/2026-07-13-prover-self-review.md` (1 line-hits)
- `docs/prover/2026-07-13-row298-design-principles.md` (1 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (3 line-hits)
- `docs/prover/2026-07-14-cross-host-coordinator.md` (2 line-hits)
- `docs/prover/2026-07-14-design-review.md` (1 line-hits)
- `docs/prover/2026-07-14-monitor-schedule.md` (2 line-hits)
- `docs/prover/2026-07-14-property-routing.md` (3 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (2 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (2 line-hits)
- `docs/prover/2026-07-15-322-forward-binding-and-323-review-record-class.md` (5 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (3 line-hits)
- `docs/prover/2026-07-18-release-2.8.0.md` (3 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (4 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (4 line-hits)
- `docs/prover/2026-07-20-conduct-stories-2-3.md` (1 line-hits)
- `docs/prover/2026-07-27-row494-rendered-sweep.md` (1 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (2 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-06-budget-never-bend-recheck.md` (7 line-hits)
- `docs/prover/2026-08-06-spec-table-regeneration.md` (2 line-hits)
- `docs/prover/2026-08-06-work-board.md` (4 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (23 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (28 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (3 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (1 line-hits)
- `docs/skill-review/2026-07-18-inv237-wiring.md` (4 line-hits)
- `docs/skill-review/2026-07-23-build-pipeline-row480.md` (1 line-hits)
- `docs/skill-review/2026-07-27-communicator.md` (2 line-hits)
- `docs/skill-review/2026-07-27-publish.md` (4 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (2 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (2 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (1 line-hits)

---

### Rule 6 — (no heading SPEC code — body cites INV-107, INV-76, INV-95)

**Demands:** Long or delegated work keeps a disk checkpoint (done/in-progress/next) so a cutoff resumes cleanly; red is never committed.

**Size:** 1860 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-107, INV-76, INV-95; literal phrase "rule 6".

**TRACES — test files (7):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_checkpoint_closes.py` — test_spec_anchor_and_index, test_stale_checkpoint_is_a_defect_in_both_homes
- `tests/test_communicator_body_thinned.py` — test_relocated_examples_live_in_the_reference
- `tests/test_leave_command.py` — test_spec_anchor_and_index
- `tests/test_no_silent_drop.py` — test_build_pipeline_points_at_the_one_home
- `tests/test_reap_owned_group.py` — test_reap_source_names_no_process_by_name
- `tests/test_traceability.py` — test_no_calques_rule, test_own_architecture_carries_views_and_budgets, test_worker_liveness_protocol

**TRACES — guardrail scripts (1):**
- `guardrails/reap_owned_group.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (6):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/page-lifecycle.md`
- `skills/communicator/references/words.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (4 files, 40 lines):**
- `ARCHITECTURE.md`:59, 61, 73, 209
- `PRODUCT_SPEC.md`:805, 806, 807, 811, 812, 2849, 2850, 2896, 2940, 2941, 2945, 2946, 2947, 3030, 4243, 4992, 4994, 5638, 7980, 7999, 8011
- `ROADMAP.md`:84, 85, 101, 199
- `TEST_MATRIX.md`:164, 168, 171, 176, 432, 433, 487, 605, 946, 965, 977

**TRACES — living docs (4 files, 12 lines):**
- `docs/lenses.md`:44, 66, 105
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:71
- `docs/restyle-repoint-log.md`:103
- `docs/worker-liveness.md`:3, 11, 12, 20, 22, 34, 59

**TRACES — historical/record docs (31 files, 105 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (14 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (8 line-hits)
- `docs/audit/2026-07-05/skill-creator-eval-opus.md` (1 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (8 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (1 line-hits)
- `docs/evals/2026-07-06-rerun/scores-communicator.md` (2 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-05-calques-push.md` (6 line-hits)
- `docs/prover/2026-07-06-rows143-144.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (2 line-hits)
- `docs/prover/2026-07-09-row181.md` (2 line-hits)
- `docs/prover/2026-07-10-m1-audit.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (7 line-hits)
- `docs/prover/2026-07-10-row235.md` (5 line-hits)
- `docs/prover/2026-07-12-row226-checkpoint-closes.md` (3 line-hits)
- `docs/prover/2026-07-12-row240-layout-pass-vehicle.md` (1 line-hits)
- `docs/prover/2026-07-12-s38-batch-inv117-120.md` (8 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (3 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (2 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (1 line-hits)
- `docs/queue-archive/2026-07-05.md` (1 line-hits)
- `docs/queue-archive/2026-07-10-v1.0.0-milestone.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (9 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (4 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (4 line-hits)
- `docs/skill-review/2026-08-05-build-pipeline-readability.md` (2 line-hits)

---

### Rule 7 — (no heading SPEC code — body cites ACT-3, E-13, INV-10, INV-105, INV-11, INV-117, INV-214, INV-298, INV-39, INV-49, INV-76, T-18)

**Demands:** Before every write and commit, re-check git status/HEAD; parallel lanes, worktrees, and worker restores follow a strict collision-avoidance set.

**Size:** 5477 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** ACT-3, E-13, INV-10, INV-105, INV-11, INV-117, INV-214, INV-298, INV-39, INV-49, INV-76, T-18; script names guardrails/check-worker-restore.py, scripts/open-lane.sh; literal phrase "rule 7".

**TRACES — test files (17):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_agent_channels.py` — test_message_carries_a_stable_identifier, test_ratification_authorizes_the_founding_and_the_agent_declares_it
- `tests/test_behavioural_break_one_home.py` — (module-level, no enclosing test_ function)
- `tests/test_brief_time_disjointness.py` — test_spec_worker_contract_carries_the_imperative
- `tests/test_canonical_state_dir.py` — test_spec_anchor_and_index
- `tests/test_deferred_revisit_cadence.py` — (module-level, no enclosing test_ function)
- `tests/test_delivery_separability.py` — test_inv248_architecture_owns_the_lens
- `tests/test_drafter_applier_form.py` — test_born_live_and_cited
- `tests/test_formal_index.py` — (module-level, no enclosing test_ function)
- `tests/test_guardrails.py` — test_pre_push_calls_all_four_checks
- `tests/test_lane_branch_road.py` — test_a_rebased_lane_fast_forwards_main_with_no_merge_commit, test_architecture_owns_inv214, test_every_new_anchor_carries_an_index_row, test_inv214_carries_one_index_row, test_spec_states_the_lane_open_act, test_the_act_refuses_off_main, test_two_worktrees_share_one_ref_store_so_a_foreign_claim_needs_no_fetch
- `tests/test_pen_tiebreak_identity.py` — test_spec_anchor, test_spec_anchor_and_index, test_tiebreak_orders_on_session_identity
- `tests/test_reap_owned_group.py` — test_reap_source_names_no_process_by_name, test_worker_contract_carries_the_idle_habit
- `tests/test_redoor_independence_rebuild.py` — (module-level, no enclosing test_ function)
- `tests/test_restructure_merge_gate.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_177_lane_claim_tiebreaker, test_brief_carries_ledger_and_clock, test_host_profile_recorded_override, test_inbox_states_write_rule, test_landing_purity, test_lanes_by_graph, test_own_architecture_carries_views_and_budgets, test_parallel_lanes_law, test_roadmap_in_work_cap, test_settings_ladder_documented, test_worker_contract_stated, test_worker_liveness_protocol
- `tests/test_worker_restore.py` — test_the_brief_stub_hands_the_clause_to_the_worker, test_the_five_homes_state_one_command_list, test_the_verify_step_names_the_command

**TRACES — guardrail scripts (7):**
- `guardrails/README.md`
- `guardrails/check-handover-provenance.py`
- `guardrails/check-worker-restore.py`
- `guardrails/fence-refresh.sh`
- `guardrails/language-rules.json`
- `guardrails/reap_owned_group.py`
- `guardrails/specformat.py`

**TRACES — pipeline scripts/hooks (3):**
- `scripts/check-registry.json`
- `scripts/open-lane.sh`
- `scripts/stranger-wish-monitor.py`

**TRACES — other skill files (10):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/delegation-protocol.md`
- `skills/build-pipeline/references/drafter-applier-example.md`
- `skills/build-pipeline/references/minor-bump-gate.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`
- `skills/feedback-collector/SKILL.md`
- `skills/feedback-intake/SKILL.md`
- `skills/product-prover/SKILL.md`

**TRACES — root documents (4 files, 250 lines):**
- `ARCHITECTURE.md`:57, 58, 59, 60, 61, 62, 68, 74, 88, 91, 188, 194, 196, 219, 268, 365, 463, 470, 618, 647, 648, 650, 651, 652, 667, 731
- `PRODUCT_SPEC.md`:805, 1238, 1830, 1834, 1835, 1839, 1872, 1873, 1877, 1891, 1892, 1896, 1897, 1901, 1902, 1903, 1907, 1921, 1926, 1927, 1941, 1942, 1946, 1947, 1967, 1982, 1996, 2002, 2021, 2065, 2091, 2092, 2096, 2097, 2121, 2141, 2146, 2152, 2153, 2167, 2319, 2320, 2898, 2920, 2921, 2940, 2941, 2945, 2946, 2947, 3000, 3185, 3215, 3574, 3634, 3638, 3639, 3710, 3773, 3774, 3788, 3875, 3899, 3919, 3920, 3933, 3975, 3985, 4245, 4265, 4311, 4365, 4366, 4370, 4523, 4529, 4557, 4561, 4566, 4639, 4723, 4763, 4791, 4832, 4837, 4842, 4877, 4878, 4883, 4942, 4947, 4967, 4981, 4982, 4983, 4987, 4992, 4993, 4994, 5019, 5132, 5207, 5236, 5243, 5249, 5264, 5269, 5638, 5639, 5719, 5977, 5978, 5985, 6000, 6027, 6079, 6104, 6105, 6114, 6115, 6119, 6403, 6511, 7323, 7324, 7349, 7350, 7351, 7353, 7357, 7358, 7359, 7363, 7364, 7365, 7366, 7376, 7667, 7691, 7692, 7693, 7719, 7720, 7862, 7882, 7914, 7915, 7943, 7953, 7980, 8009, 8021, 8118, 8202, 8239
- `ROADMAP.md`:84, 85, 93, 101, 115, 124, 126, 182, 203, 223
- `TEST_MATRIX.md`:143, 146, 151, 152, 153, 154, 164, 167, 170, 171, 195, 198, 202, 242, 254, 321, 326, 330, 336, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 363, 364, 365, 366, 438, 507, 510, 514, 517, 527, 578, 605, 660, 779, 784, 794, 826, 848, 880, 881, 909, 919, 946, 975, 987, 1084, 1168, 1210

**TRACES — living docs (14 files, 32 lines):**
- `docs/adoption.md`:13, 61
- `docs/audits/2026-08-07-number-census.md`:37, 93
- `docs/audits/2026-08-07-number-rulings.md`:18
- `docs/decisions/2026-07-06-overnight-decisions.md`:93
- `docs/decisions/2026-07-07-morning-round3.md`:38
- `docs/language-rule-coverage.md`:357
- `docs/lenses.md`:44, 95, 152
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:17, 27
- `docs/onboarding-and-settings.md`:6, 12, 52, 84
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:75
- `docs/plans/2026-07-29-specification-subdivision.md`:220, 289
- `docs/spec-compaction-protocol.md`:41
- `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md`:23
- `docs/worker-liveness.md`:3, 7, 12, 20, 34, 48, 49, 50, 51, 59

**TRACES — historical/record docs (145 files, 776 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (10 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (137 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (41 line-hits)
- `docs/audit/2026-07-05-night/composition-architecture.md` (2 line-hits)
- `docs/audit/2026-07-05/pass1-prover-fable.md` (9 line-hits)
- `docs/audit/2026-07-05/pass1-prover-opus.md` (8 line-hits)
- `docs/audit/2026-07-05/pass2-matrix-opus.md` (7 line-hits)
- `docs/audit/2026-07-05/pass3-composition-opus.md` (20 line-hits)
- `docs/audit/2026-07-12-compaction-pass.md` (3 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (6 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (5 line-hits)
- `docs/audit/2026-07-12-once-read-rules-sweep.md` (2 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (2 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/bare-test-author.md` (2 line-hits)
- `docs/evals/2026-07-10-rerun/with-skill-test-author.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/measure/2026-07-28-tier-routing-experiment.md` (1 line-hits)
- `docs/prover/2026-07-04-v03-push.md` (7 line-hits)
- `docs/prover/2026-07-04.md` (1 line-hits)
- `docs/prover/2026-07-05-adopt.md` (1 line-hits)
- `docs/prover/2026-07-05-architecture.md` (1 line-hits)
- `docs/prover/2026-07-05-base-skill.md` (5 line-hits)
- `docs/prover/2026-07-05-doors.md` (1 line-hits)
- `docs/prover/2026-07-05-founding-designsync.md` (5 line-hits)
- `docs/prover/2026-07-05-lost-layers.md` (1 line-hits)
- `docs/prover/2026-07-05-row100.md` (5 line-hits)
- `docs/prover/2026-07-05-row86.md` (1 line-hits)
- `docs/prover/2026-07-05-row93.md` (1 line-hits)
- `docs/prover/2026-07-05-row94.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (2 line-hits)
- `docs/prover/2026-07-05-scopes.md` (2 line-hits)
- `docs/prover/2026-07-05-v05-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v14-push.md` (4 line-hits)
- `docs/prover/2026-07-05-v15-8-full.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-9.md` (1 line-hits)
- `docs/prover/2026-07-05-v15b-push.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (2 line-hits)
- `docs/prover/2026-07-06-push-2.md` (4 line-hits)
- `docs/prover/2026-07-06-pushgate-s20-2.md` (3 line-hits)
- `docs/prover/2026-07-06-pushgate-s20.md` (6 line-hits)
- `docs/prover/2026-07-06-pushgate-s21.md` (1 line-hits)
- `docs/prover/2026-07-06-row135.md` (14 line-hits)
- `docs/prover/2026-07-06-row136.md` (2 line-hits)
- `docs/prover/2026-07-06-row139.md` (3 line-hits)
- `docs/prover/2026-07-06-row140.md` (4 line-hits)
- `docs/prover/2026-07-06-row142.md` (4 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (6 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (5 line-hits)
- `docs/prover/2026-07-07-humanize-machines.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-one-rulebook.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-package-repo.md` (3 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-rhythm.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (10 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk10.md` (6 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk6.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk9.md` (2 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-6.md` (3 line-hits)
- `docs/prover/2026-07-07-pushgate-s23-1.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s23-5.md` (1 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-07-row54.md` (2 line-hits)
- `docs/prover/2026-07-07-row56.md` (6 line-hits)
- `docs/prover/2026-07-07-rows111-113.md` (2 line-hits)
- `docs/prover/2026-07-07-rows149-152.md` (4 line-hits)
- `docs/prover/2026-07-07-spec-humanize-prototype.md` (2 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (1 line-hits)
- `docs/prover/2026-07-09-full-reprove-session29-body.md` (3 line-hits)
- `docs/prover/2026-07-09-row181.md` (3 line-hits)
- `docs/prover/2026-07-09-small-holes.md` (5 line-hits)
- `docs/prover/2026-07-10-m1-audit.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (18 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (11 line-hits)
- `docs/prover/2026-07-10-night-postfold.md` (7 line-hits)
- `docs/prover/2026-07-10-onboarding-crosslink.md` (1 line-hits)
- `docs/prover/2026-07-10-row201.md` (1 line-hits)
- `docs/prover/2026-07-10-row221.md` (5 line-hits)
- `docs/prover/2026-07-10-row235.md` (2 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (15 line-hits)
- `docs/prover/2026-07-12-row227-canonical-state-dir.md` (3 line-hits)
- `docs/prover/2026-07-12-row255-drafter-applier-form.md` (1 line-hits)
- `docs/prover/2026-07-12-row258-restructure-merge-gate.md` (2 line-hits)
- `docs/prover/2026-07-12-s38-batch-inv117-120.md` (14 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv129-deferred-revisit-cadence.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv131-redoor-independence-rebuild.md` (6 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (11 line-hits)
- `docs/prover/2026-07-14-cross-host-coordinator.md` (3 line-hits)
- `docs/prover/2026-07-14-design-review.md` (1 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (2 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (3 line-hits)
- `docs/prover/2026-07-15-321-feedback-collector.md` (3 line-hits)
- `docs/prover/2026-07-16-2.3.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (6 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (1 line-hits)
- `docs/prover/2026-07-17-2.4.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-17-2.5.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-17-agent-communication.md` (5 line-hits)
- `docs/prover/2026-07-17-lanes-and-self-declaration.md` (8 line-hits)
- `docs/prover/2026-07-18-batch4-push-recheck.md` (3 line-hits)
- `docs/prover/2026-07-18-rows-393-405-389.md` (1 line-hits)
- `docs/prover/2026-07-18-rows386-412-414-lane-open-act.md` (10 line-hits)
- `docs/prover/2026-07-19.md` (3 line-hits)
- `docs/prover/2026-07-20-3.0.0-backdescribe.md` (1 line-hits)
- `docs/prover/2026-07-20-comms.md` (3 line-hits)
- `docs/prover/2026-07-21-integration-recheck.md` (8 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (1 line-hits)
- `docs/prover/2026-07-21-inv248-delivery-separability.md` (3 line-hits)
- `docs/prover/2026-07-23-row445-4.0.0-fix-verify.md` (3 line-hits)
- `docs/prover/2026-07-23-row477-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-23-row477.md` (1 line-hits)
- `docs/prover/2026-07-23-row480-minor-gate.md` (2 line-hits)
- `docs/prover/2026-07-23-row480.md` (2 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (20 line-hits)
- `docs/prover/2026-07-29-night-landings-push-recheck.md` (2 line-hits)
- `docs/prover/2026-07-29-ratchet-arm-and-extract-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (3 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (4 line-hits)
- `docs/prover/2026-08-06-work-board.md` (6 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (2 line-hits)
- `docs/queue-archive/2026-07-05-test-author-extraction.md` (1 line-hits)
- `docs/queue-archive/2026-07-05.md` (3 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (6 line-hits)
- `docs/queue-archive/2026-07-10-v1.0.0-milestone.md` (4 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (25 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (25 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (9 line-hits)
- `docs/research/2026-07-07-genre-migration-plan.md` (1 line-hits)
- `docs/skill-review/2026-07-18-lane-open-act.md` (4 line-hits)
- `docs/skill-review/2026-07-21-build-pipeline.md` (7 line-hits)
- `docs/skill-review/2026-07-21-live-spec-base.md` (8 line-hits)
- `docs/skill-review/2026-07-21-product-prover-delivery-separability.md` (4 line-hits)
- `docs/skill-review/2026-07-21-product-prover.md` (8 line-hits)
- `docs/skill-review/2026-07-23-build-pipeline-row480.md` (1 line-hits)
- `docs/skill-review/2026-07-28-build-pipeline.md` (10 line-hits)
- `docs/skill-review/2026-07-28-live-spec-base.md` (13 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)

---

### Rule 8 — (no heading SPEC code — body cites A-7, M-7)

**Demands:** Re-read skill/pack/profile modification times at every breakpoint; journal the old-to-new change on any version bump.

**Size:** 316 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** A-7, M-7; literal phrase "rule 8".

**TRACES — test files (5):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_derived_doc_header_policy.py` — (module-level, no enclosing test_ function)
- `tests/test_installed_copy_staleness_class.py` — test_installed_copy_class_enumerates_every_member
- `tests/test_setup_entry.py` — test_a_version_disagreement_is_said_aloud
- `tests/test_traceability.py` — test_adopt_phases_cite_spec, test_bookkeeping_never_list, test_sync_skills_script

**TRACES — guardrail scripts (1):**
- `guardrails/check-skill-loadability.sh`

**TRACES — pipeline scripts/hooks (1):**
- `scripts/sync-skills.sh`

**TRACES — other skill files (2):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (3 files, 34 lines):**
- `ARCHITECTURE.md`:61, 244
- `PRODUCT_SPEC.md`:2835, 3130, 3131, 4099, 4100, 4101, 4168, 4201, 4399, 4403, 4857, 4862, 4863, 4882, 5982, 6448, 6610, 7629, 7632, 7633, 7855, 8225
- `TEST_MATRIX.md`:18, 157, 158, 405, 471, 491, 497, 535, 819, 1191

**TRACES — living docs (3 files, 3 lines):**
- `docs/onboarding-and-settings.md`:31
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:79
- `docs/worker-liveness.md`:59

**TRACES — historical/record docs (47 files, 123 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (18 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (6 line-hits)
- `docs/audit/2026-07-05/pass1-prover-opus.md` (3 line-hits)
- `docs/audit/2026-07-05/pass2-matrix-opus.md` (2 line-hits)
- `docs/audit/2026-07-05/pass3-composition-opus.md` (4 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (2 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (2 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-rows126-128-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-rows126-128-rerun/with-skill-communicator.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (2 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-04-v04-push.md` (2 line-hits)
- `docs/prover/2026-07-04.md` (1 line-hits)
- `docs/prover/2026-07-05-architecture.md` (1 line-hits)
- `docs/prover/2026-07-05-base-skill.md` (2 line-hits)
- `docs/prover/2026-07-05-row94.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-8-full.md` (1 line-hits)
- `docs/prover/2026-07-05.md` (4 line-hits)
- `docs/prover/2026-07-06-feature-fit-retro.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (1 line-hits)
- `docs/prover/2026-07-06-row136.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (3 line-hits)
- `docs/prover/2026-07-07-humanize-rhythm.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (2 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (1 line-hits)
- `docs/prover/2026-07-10-row221.md` (3 line-hits)
- `docs/prover/2026-07-10-row237.md` (1 line-hits)
- `docs/prover/2026-07-11-row219-skill-kind-review.md` (1 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (1 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (1 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (2 line-hits)
- `docs/prover/2026-07-16-2p1p1-prepush.md` (1 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (2 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-05.md` (4 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (3 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (17 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (2 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (3 line-hits)
- `docs/skill-review/2026-07-21-live-spec-base-rule34.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (1 line-hits)

---

### Rule 9 — (carries no SPEC INV code)

**Demands:** Dated reasons live in JOURNAL.md; SPEC/NEXT_STEPS/ROADMAP state only current truth; shipped docs update the same session.

**Size:** 678 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 9".

**TRACES — test files (0):**
- none found

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (3):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (1 files, 1 lines):**
- `ARCHITECTURE.md`:217

**TRACES — living docs (1 files, 1 lines):**
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:83

**TRACES — historical/record docs (22 files, 45 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (2 line-hits)
- `docs/evals/2026-07-06-rerun/scores-communicator.md` (4 line-hits)
- `docs/evals/2026-07-06-rerun/with-skill-communicator-2.md` (1 line-hits)
- `docs/evals/2026-07-06-rows126-128-rerun/bare-communicator.md` (1 line-hits)
- `docs/evals/2026-07-06-rows126-128-rerun/scores.md` (2 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (1 line-hits)
- `docs/prover/2026-07-05-classes.md` (1 line-hits)
- `docs/prover/2026-07-05-rule9-detail.md` (3 line-hits)
- `docs/prover/2026-07-06-night.md` (1 line-hits)
- `docs/prover/2026-07-06-push-2.md` (1 line-hits)
- `docs/prover/2026-07-06-rows126-128.md` (2 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (1 line-hits)
- `docs/queue-archive/2026-07-05.md` (3 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (7 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (2 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (2 line-hits)
- `docs/skill-review/2026-08-05-communicator.md` (6 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 10 — (no heading SPEC code — body cites A-4, A-9, INV-7)

**Demands:** Nothing is silently deleted; a superseded file moves to the attic with a manifest line, and only regenerable junk is dropped, with approval.

**Size:** 304 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** A-4, A-9, INV-7; literal phrase "rule 10".

**TRACES — test files (8, of which 1 are synthetic-placeholder noise, see below):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/fixtures/specformat/readability_dirty.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/test_board.py` — (module-level, no enclosing test_ function)
- `tests/test_doc_bound.py` — (module-level, no enclosing test_ function)
- `tests/test_doc_rotation.py` — test_rotate_output_survives_the_gate
- `tests/test_rendered_sweep.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_adopt_phases_cite_spec, test_decision_card_consequences, test_default_expiry_law, test_spec_names_decision_page
- `tests/test_withdrawal_convergence.py` — (module-level, no enclosing test_ function)

**TRACES — guardrail scripts (3):**
- `guardrails/check-board.py`
- `guardrails/check-doc-rotation.py`
- `guardrails/check-rendered-sweep.py`

**TRACES — pipeline scripts/hooks (2):**
- `scripts/rotate-doc.py`
- `scripts/sweep-rendered.py`

**TRACES — other skill files (4):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/page-lifecycle.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (4 files, 38 lines):**
- `ARCHITECTURE.md`:215, 225, 244, 629
- `PRODUCT_SPEC.md`:422, 3868, 4121, 4129, 4135, 4136, 4141, 4142, 4946, 6114, 7153, 7163, 7168, 7169, 7170, 7183, 7852, 7857, 7911
- `ROADMAP.md`:30, 50, 51, 124
- `TEST_MATRIX.md`:167, 435, 437, 463, 469, 476, 592, 595, 816, 821, 877

**TRACES — living docs (2 files, 2 lines):**
- `docs/adoption.md`:35
- `docs/spec-style.md`:149

**TRACES — historical/record docs (43 files, 122 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (17 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (7 line-hits)
- `docs/audit/2026-07-05/pass1-prover-fable.md` (2 line-hits)
- `docs/audit/2026-07-05/pass2-matrix-opus.md` (1 line-hits)
- `docs/audit/2026-07-05/skill-creator-eval-opus.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (1 line-hits)
- `docs/briefs/2026-07-29-rotate-the-journal-brief.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/bare-test-author.md` (2 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (3 line-hits)
- `docs/evals/2026-07-10-rerun/with-skill-test-author.md` (4 line-hits)
- `docs/prover/2026-07-04.md` (2 line-hits)
- `docs/prover/2026-07-05-adopt.md` (6 line-hits)
- `docs/prover/2026-07-05-architecture.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (4 line-hits)
- `docs/prover/2026-07-05-v14-push.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-5-full.md` (1 line-hits)
- `docs/prover/2026-07-05.md` (1 line-hits)
- `docs/prover/2026-07-06-feature-fit-retro.md` (2 line-hits)
- `docs/prover/2026-07-06-push.md` (1 line-hits)
- `docs/prover/2026-07-06-row116.md` (1 line-hits)
- `docs/prover/2026-07-06-row135.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (3 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk1.md` (1 line-hits)
- `docs/prover/2026-07-07-rows149-152.md` (1 line-hits)
- `docs/prover/2026-07-10-row221.md` (3 line-hits)
- `docs/prover/2026-07-12-row227-canonical-state-dir.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv130-withdrawal-convergence.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-17-row408-waiting-list.md` (3 line-hits)
- `docs/prover/2026-07-18-row390-392-doc-rotation.md` (2 line-hits)
- `docs/prover/2026-07-27-evening-movement.md` (1 line-hits)
- `docs/prover/2026-07-27-row494-rendered-sweep.md` (7 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-05.md` (4 line-hits)
- `docs/queue-archive/2026-07-06-communicator-commentable-provenance.md` (3 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (3 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (10 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (7 line-hits)

---

### Rule 11 — (carries no SPEC INV code)

**Demands:** "Works" is said only after running it and seeing the result; synthetic data always carries the label SYNTHETIC.

**Size:** 362 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 11".

**TRACES — test files (2):**
- `tests/test_communicator_body_thinned.py` — test_relocated_examples_live_in_the_reference
- `tests/test_traceability.py` — test_done_claim_evidence_walk

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (3):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (1 files, 1 lines):**
- `ARCHITECTURE.md`:216

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (9 files, 13 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (2 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (2 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (3 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (1 line-hits)

---

### Rule 12 — (carries no SPEC INV code)

**Demands:** Irreversible, authored-content, publishing, push-gated, and taste decisions go to the human; everything else proceeds and gets reported.

**Size:** 310 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 12".

**TRACES — test files (2):**
- `tests/test_critical_preempt_bound.py` — (module-level, no enclosing test_ function)
- `tests/test_footprint_note.py` — test_capture_echo_carries_the_footprint_field

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (3):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/writing-register.md`

**TRACES — root documents (0 files, 0 lines):**
- none found

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (9 files, 16 line-hits, path + count only):**
- `docs/prover/2026-07-06-feature-fit-retro.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (1 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (1 line-hits)
- `docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md` (1 line-hits)
- `docs/prover/2026-07-12-s40-inv133-critical-preempt-bound.md` (1 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (3 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (3 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (3 line-hits)

---

### Rule 13 — (no heading SPEC code — body cites INV-205, INV-206, INV-207)

**Demands:** Every factual claim traces to a primary source (file:line, commit, command output); a human-attributed decision needs a dated, checkable exchange.

**Size:** 2028 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-205, INV-206, INV-207; script names guardrails/check-authority-anchor.py; literal phrase "rule 13".

**TRACES — test files (6):**
- `tests/test_authority_anchor.py` — test_architecture_owns_the_invariant, test_formal_index_row, test_gate_names_no_person_in_code, test_gate_ships, test_gate_standing_scan_hard_blocks_records_and_reaches_risky_surfaces, test_judge_mode_is_wired_and_advisory, test_matrix_row_covers_the_law, test_spec_states_the_law
- `tests/test_board.py` — test_architecture_owns_the_invariant, test_formal_index_row, test_gate_reds_a_closing_report_that_omits_an_open_item, test_gate_reds_a_demotion_with_no_matching_line, test_gate_reds_an_over_cap_shown_set, test_matrix_row_covers_the_law, test_spec_states_the_law
- `tests/test_communicator_body_thinned.py` — test_relocated_examples_live_in_the_reference
- `tests/test_release_note.py` — (module-level, no enclosing test_ function)
- `tests/test_touchpoint_kind.py` — test_architecture_owns_the_invariant, test_formal_index_row, test_gate_reds_a_teaching_line_on_a_point_the_person_did_not_open, test_gate_reds_an_interruption_from_an_asynchronous_point, test_matrix_row_covers_the_law, test_spec_states_the_law
- `tests/test_traceability.py` — test_communicator_trigger_narrowed, test_rule5_states_the_settled_delegation_rule

**TRACES — guardrail scripts (7):**
- `guardrails/README.md`
- `guardrails/authority-anchor.json`
- `guardrails/check-authority-anchor.py`
- `guardrails/check-board.py`
- `guardrails/check-release-note.py`
- `guardrails/check-touchpoint-kind.py`
- `guardrails/touchpoints.json`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (6):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`
- `skills/product-prover/SKILL.md`
- `skills/publish/SKILL.md`

**TRACES — root documents (4 files, 53 lines):**
- `ARCHITECTURE.md`:316, 317, 319, 375, 376, 377, 378, 382, 383, 384, 385, 485, 666
- `PRODUCT_SPEC.md`:2206, 5653, 5654, 5658, 5659, 5673, 5674, 5678, 5679, 5683, 5697, 5698, 5699, 5703, 5704, 5723, 5743, 5762, 7675, 7676, 7708, 8109, 8110, 8111
- `ROADMAP.md`:53, 226
- `TEST_MATRIX.md`:327, 338, 382, 411, 412, 438, 591, 592, 593, 604, 787, 1075, 1076, 1077

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (43 files, 160 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (20 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (10 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (1 line-hits)
- `docs/briefs/2026-07-28-record-the-settled-answer-brief.md` (2 line-hits)
- `docs/evals/2026-07-06-push-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/with-skill-spec-author.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (2 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-11-row248-detached-visibility.md` (1 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (2 line-hits)
- `docs/prover/2026-07-17-batch2-push-recheck.md` (3 line-hits)
- `docs/prover/2026-07-17-row408-waiting-list.md` (6 line-hits)
- `docs/prover/2026-07-17-row413-touchpoint-kind.md` (5 line-hits)
- `docs/prover/2026-07-17-row415-authority-anchor.md` (12 line-hits)
- `docs/prover/2026-07-17-row419-skill-review-gate.md` (1 line-hits)
- `docs/prover/2026-07-18-row390-392-doc-rotation.md` (2 line-hits)
- `docs/prover/2026-07-18-rows382-403-far-tier.md` (2 line-hits)
- `docs/prover/2026-07-18-rows402-409-touchpoint-instances.md` (6 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (2 line-hits)
- `docs/prover/2026-07-27-language-gate-reach.md` (2 line-hits)
- `docs/prover/2026-07-27-row494-rendered-sweep.md` (2 line-hits)
- `docs/prover/2026-08-06-work-board.md` (4 line-hits)
- `docs/prover/red-proof-2026-07-17-row408.txt` (9 line-hits)
- `docs/prover/red-proof-2026-07-17-row415.txt` (7 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (4 line-hits)
- `docs/push-review/2026-08-06-three-landings-and-the-edition-measured.md` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (5 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (13 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/research/2026-07-06-neighbours-implementation-harvest.md` (1 line-hits)
- `docs/skill-review/2026-07-17-live-spec-base-build-pipeline.md` (10 line-hits)
- `docs/skill-review/2026-07-18-publish.md` (2 line-hits)
- `docs/skill-review/2026-07-21-live-spec-base-rule34.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-rename-sweep.md` (2 line-hits)
- `docs/skill-review/2026-08-05-communicator-teeth-repin.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator.md` (4 line-hits)
- `docs/skill-review/2026-08-05-design-reviewer-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (3 line-hits)

---

### Rule 14 — (no heading SPEC code — body cites INV-124)

**Demands:** A found defect is one sample of a class; name the class, sweep every look-alike in the same change.

**Size:** 1929 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-124; literal phrase "rule 14".

**TRACES — test files (2):**
- `tests/test_class_hunt.py` — test_build_pipeline_bug_entry_drives_the_hunt, test_formal_index_row, test_matrix_row_covers_the_class_hunt, test_spec_clause_stands
- `tests/test_cross_surface_policy.py` — (module-level, no enclosing test_ function)

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (6):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/request-kind-table.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/communicator/references/writing-register.md`
- `skills/product-prover/SKILL.md`

**TRACES — root documents (4 files, 18 lines):**
- `ARCHITECTURE.md`:145
- `PRODUCT_SPEC.md`:1214, 3653, 3658, 3659, 3663, 3664, 3665, 6204, 7333, 8028
- `ROADMAP.md`:54, 136, 215
- `TEST_MATRIX.md`:251, 324, 333, 994

**TRACES — living docs (1 files, 1 lines):**
- `docs/lenses.md`:186

**TRACES — historical/record docs (37 files, 74 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (5 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (3 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (2 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (2 line-hits)
- `docs/audit/2026-07-23-tlvphotos-conduct-verdicts.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/evals/2026-07-05-first-run/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-06-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-push.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (1 line-hits)
- `docs/prover/2026-07-09-row180.md` (1 line-hits)
- `docs/prover/2026-07-10-row210.md` (1 line-hits)
- `docs/prover/2026-07-11-row246-mirror-attribution.md` (1 line-hits)
- `docs/prover/2026-07-12-s40-inv124-class-hunt.md` (5 line-hits)
- `docs/prover/2026-07-12-s40-inv125-cross-surface-uniformity.md` (1 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (1 line-hits)
- `docs/prover/2026-07-16-inv157-third-net.md` (1 line-hits)
- `docs/prover/2026-07-18-rows382-403-far-tier.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/2026-07-12-from-tlvphotos-a-caught-bug-triggers-a-class-hunt-not-a-point-fix.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (15 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (4 line-hits)
- `docs/skill-review/2026-08-05-communicator-rename-sweep.md` (2 line-hits)
- `docs/skill-review/2026-08-05-communicator.md` (2 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (2 line-hits)

---

### Rule 15 — (no heading SPEC code — body cites INV-16, INV-22, T-12, T-16)

**Demands:** Every request is classified by entry door (feature/bug/refactor/docs-only/skip) and work-kind before the first line of code.

**Size:** 1371 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-16, INV-22, T-12, T-16; literal phrase "rule 15".

**TRACES — test files (5):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_communicator_register_extracted.py` — test_reference_file_carries_the_ten_point_checklist
- `tests/test_forward_binding_and_infra_class.py` — test_forward_binding_cites_are_repointed_off_the_silent_roots
- `tests/test_redoor_independence_rebuild.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_base_rules_door_and_prototype, test_skills_carry_work_kind, test_spec_states_door_procedure, test_spec_states_work_kind

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (10):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/excuses-table.md`
- `skills/build-pipeline/references/request-kind-table.md`
- `skills/build-pipeline/references/work-kind-table.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/writing-register.md`
- `skills/feedback-intake/SKILL.md`
- `skills/product-prover/SKILL.md`
- `skills/publish/SKILL.md`
- `skills/spec-author/SKILL.md`

**TRACES — root documents (4 files, 71 lines):**
- `ARCHITECTURE.md`:145, 647
- `PRODUCT_SPEC.md`:451, 453, 454, 463, 464, 1068, 1069, 1073, 1081, 1082, 1083, 1084, 1098, 1099, 1138, 1186, 1233, 1234, 1238, 1239, 1240, 1259, 1289, 1290, 1291, 1295, 1314, 1334, 1424, 1478, 1522, 2300, 2301, 2305, 2334, 2335, 3256, 3257, 3261, 3276, 3315, 3334, 3484, 3981, 3985, 3989, 4119, 5263, 5265, 5925, 7920, 7926, 8233, 8237
- `ROADMAP.md`:52, 132
- `TEST_MATRIX.md`:265, 297, 298, 299, 302, 325, 334, 335, 354, 886, 892, 1204, 1208

**TRACES — living docs (3 files, 5 lines):**
- `docs/lenses.md`:30, 279
- `docs/onboarding-and-settings.md`:71
- `docs/pipeline.md`:20, 140

**TRACES — historical/record docs (71 files, 228 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (40 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (9 line-hits)
- `docs/audit/2026-07-05-night/composition-architecture.md` (3 line-hits)
- `docs/audit/2026-07-08/milestone-audit.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (2 line-hits)
- `docs/audit/2026-07-15-1.8.0-audit.md` (1 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/design-review/2026-07-14.md` (1 line-hits)
- `docs/design-review/2026-07-15-1.8.0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (3 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (2 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (2 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (2 line-hits)
- `docs/prover/2026-07-05-calques-push.md` (1 line-hits)
- `docs/prover/2026-07-05-doors.md` (2 line-hits)
- `docs/prover/2026-07-05-facets.md` (3 line-hits)
- `docs/prover/2026-07-05-fences.md` (1 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (2 line-hits)
- `docs/prover/2026-07-05-row86.md` (15 line-hits)
- `docs/prover/2026-07-05-row93.md` (1 line-hits)
- `docs/prover/2026-07-05-row94.md` (1 line-hits)
- `docs/prover/2026-07-05-row98.md` (2 line-hits)
- `docs/prover/2026-07-05-row99.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (1 line-hits)
- `docs/prover/2026-07-05-v10-push.md` (2 line-hits)
- `docs/prover/2026-07-05-v11-push.md` (2 line-hits)
- `docs/prover/2026-07-05-v14-push.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-push.md` (8 line-hits)
- `docs/prover/2026-07-05-v15b-push.md` (3 line-hits)
- `docs/prover/2026-07-05-v15c-push.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (2 line-hits)
- `docs/prover/2026-07-06-push-2.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s20.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s21-2.md` (3 line-hits)
- `docs/prover/2026-07-06-row109.md` (2 line-hits)
- `docs/prover/2026-07-06-row140.md` (2 line-hits)
- `docs/prover/2026-07-06-row145.md` (1 line-hits)
- `docs/prover/2026-07-06-row146.md` (2 line-hits)
- `docs/prover/2026-07-06-rows108-119.md` (2 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (5 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-machines.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-publishing.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk1.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk6.md` (5 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk7.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk8.md` (1 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-07-spec-humanize-plan.md` (1 line-hits)
- `docs/prover/2026-07-07-spec-humanize-prototype.md` (3 line-hits)
- `docs/prover/2026-07-10-row221.md` (1 line-hits)
- `docs/prover/2026-07-10-row244.md` (1 line-hits)
- `docs/prover/2026-07-11-row219-skill-kind-review.md` (2 line-hits)
- `docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md` (6 line-hits)
- `docs/prover/2026-07-12-s40-inv131-redoor-independence-rebuild.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv46-audit-trigger-broadened.md` (1 line-hits)
- `docs/prover/2026-07-12-s41-inv134-footprint-note-enforcement.md` (2 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (5 line-hits)
- `docs/prover/2026-07-15-1.8.0-minor-gate.md` (2 line-hits)
- `docs/prover/2026-07-15-322-forward-binding-and-323-review-record-class.md` (4 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (5 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (15 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (9 line-hits)
- `docs/research/2026-07-07-genre-migration-plan.md` (1 line-hits)
- `docs/research/2026-07-07-spec-humanize-plan.md` (1 line-hits)
- `docs/skill-review/2026-07-21-spec-author.md` (1 line-hits)

---

### Rule 16 — (no heading SPEC code — body cites E-17, INV-17)

**Demands:** A prototype stays fenced and labelled in prototype/, never wired into production; promotion re-enters through the spec step.

**Size:** 875 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** E-17, INV-17; literal phrase "rule 16".

**TRACES — test files (4):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_communicator_register_extracted.py` — test_reference_file_carries_the_ten_point_checklist
- `tests/test_guardrails.py` — test_retired_checkbox_gate_unwired
- `tests/test_traceability.py` — test_base_rules_door_and_prototype, test_feedback_never_lost_in_both_homes, test_spec_states_door_procedure, test_targets_owned_by_open_rows

**TRACES — guardrail scripts (2):**
- `guardrails/README.md`
- `guardrails/check-prototype-fence.sh`

**TRACES — pipeline scripts/hooks (1):**
- `scripts/check-shipped-language.py`

**TRACES — other skill files (8):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/request-kind-table.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/words.md`
- `skills/communicator/references/writing-register.md`
- `skills/product-prover/SKILL.md`
- `skills/publish/SKILL.md`
- `skills/spec-author/SKILL.md`

**TRACES — root documents (3 files, 28 lines):**
- `ARCHITECTURE.md`:61, 308
- `PRODUCT_SPEC.md`:307, 1190, 1334, 1474, 1790, 1810, 2280, 2281, 2285, 2286, 2301, 2355, 2356, 2376, 2406, 4120, 5102, 5370, 7886, 7921
- `TEST_MATRIX.md`:160, 177, 334, 566, 852, 887

**TRACES — living docs (1 files, 1 lines):**
- `docs/lenses.md`:279

**TRACES — historical/record docs (31 files, 74 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (16 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (4 line-hits)
- `docs/audit/2026-07-05-night/composition-architecture.md` (1 line-hits)
- `docs/design-review/2026-07-15-1.8.0.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-05-doors.md` (3 line-hits)
- `docs/prover/2026-07-05-facets.md` (2 line-hits)
- `docs/prover/2026-07-05-fences.md` (2 line-hits)
- `docs/prover/2026-07-05-founding-designsync.md` (1 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (2 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (1 line-hits)
- `docs/prover/2026-07-05-v11-push.md` (1 line-hits)
- `docs/prover/2026-07-06-row109.md` (3 line-hits)
- `docs/prover/2026-07-06-rows108-119.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-machines.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk7.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk8.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk9.md` (2 line-hits)
- `docs/prover/2026-07-07-rows149-152.md` (1 line-hits)
- `docs/prover/2026-07-07-spec-humanize-prototype.md` (7 line-hits)
- `docs/prover/2026-07-11-row218-convergence-rule.md` (1 line-hits)
- `docs/prover/2026-07-12-row279-adopt-impersonal-voice.md` (1 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate-addendum.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (7 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (4 line-hits)
- `docs/skill-review/2026-07-21-spec-author.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 17 — (carries no SPEC INV code)

**Demands:** Truly irreversible acts (spend, delete, unsendable send) always stop for the human's word; a repo push is not irreversible.

**Size:** 570 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 17".

**TRACES — test files (3):**
- `tests/test_broad_kill_guardrail.py` — (module-level, no enclosing test_ function)
- `tests/test_measurement_carries_method.py` — test_the_writing_register_states_the_rule
- `tests/test_traceability.py` — test_night_batch_skill_rules

**TRACES — guardrail scripts (3):**
- `guardrails/check-broad-kill.sh`
- `guardrails/check-runaway-child.py`
- `guardrails/reap_owned_group.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (5):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/words.md`
- `skills/communicator/references/writing-register.md`
- `skills/feedback-collector/SKILL.md`

**TRACES — root documents (1 files, 1 lines):**
- `ARCHITECTURE.md`:643

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (19 files, 36 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (8 line-hits)
- `docs/audit/2026-07-05-night/composition-architecture.md` (2 line-hits)
- `docs/prover/2026-07-05-row93.md` (1 line-hits)
- `docs/prover/2026-07-06-row136.md` (1 line-hits)
- `docs/prover/2026-07-06-row141.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-publishing.md` (1 line-hits)
- `docs/prover/2026-07-15-321-feedback-collector.md` (4 line-hits)
- `docs/prover/2026-07-15-334-cleanup-ownership.md` (1 line-hits)
- `docs/prover/architecture-prover-record.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (1 line-hits)
- `docs/queue-archive/2026-07-05.md` (1 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (3 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (4 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (1 line-hits)
- `docs/skill-review/2026-07-28-build-pipeline.md` (1 line-hits)
- `docs/skill-review/2026-08-05-build-pipeline-readability.md` (1 line-hits)

---

### Rule 18 — (carries no SPEC INV code)

**Demands:** A taken filename differentiates first by its home's own semantic mark, then by a numeric ordinal; never overwrite.

**Size:** 766 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** (none); literal phrase "rule 18".

**TRACES — test files (2):**
- `tests/test_rendered_sweep.py` — test_two_pages_sharing_one_basename_take_their_source_dir_first
- `tests/test_traceability.py` — test_collision_law_one_home, test_spec_names_decision_page

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (1):**
- `scripts/sweep-rendered.py`

**TRACES — other skill files (3):**
- `skills/communicator/SKILL.md`
- `skills/communicator/references/page-lifecycle.md`
- `skills/communicator/references/words.md`

**TRACES — root documents (1 files, 2 lines):**
- `TEST_MATRIX.md`:142, 437

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (16 files, 23 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (1 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (3 line-hits)
- `docs/prover/2026-07-05-v15-5-full.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-package-repo.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-10.md` (1 line-hits)
- `docs/prover/2026-07-07-spec-humanize-plan.md` (1 line-hits)
- `docs/prover/2026-07-21-inv249-inbox-deposit-protocol.md` (1 line-hits)
- `docs/prover/2026-07-27-row494-rendered-sweep.md` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/2026-07-17-from-promoter-consumer-side-input.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (2 line-hits)
- `docs/research/2026-07-07-genre-migration-plan.md` (1 line-hits)
- `docs/research/2026-07-07-spec-humanize-plan.md` (1 line-hits)

---

### Rule 19 — (no heading SPEC code — body cites E-24, INV-23, INV-56)

**Demands:** Operational noise gets a WATCHED line on first sight; a repeat gets a named owner; an owned problem never blocks unrelated work.

**Size:** 1723 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** E-24, INV-23, INV-56; literal phrase "rule 19".

**TRACES — test files (6):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_behavioural_break_one_home.py` — (module-level, no enclosing test_ function)
- `tests/test_code_compaction_station.py` — test_spec_names_second_trigger_and_gate
- `tests/test_compaction_discipline.py` — test_removal_keeps_meaning_phrase, test_spec_anchor
- `tests/test_crosscut_counter.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_base_rule_problem_ledger, test_communicator_trigger_narrowed, test_limp_never_dams_flow, test_matrix_anchor_reads_from_the_trailing_bracket

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (1):**
- `scripts/spec-style-lint.py`

**TRACES — other skill files (6):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/delegation-protocol.md`
- `skills/build-pipeline/references/minor-bump-gate.md`
- `skills/communicator/SKILL.md`
- `skills/feedback-intake/SKILL.md`
- `skills/test-author/SKILL.md`

**TRACES — root documents (4 files, 46 lines):**
- `ARCHITECTURE.md`:59, 76, 235, 237, 301, 920
- `PRODUCT_SPEC.md`:2538, 2591, 2996, 3000, 3492, 3653, 3679, 3684, 3685, 3699, 3704, 3710, 3712, 3726, 3731, 3749, 3753, 3754, 3759, 3783, 3787, 3788, 3792, 3807, 4370, 4376, 4988, 7893, 7927, 7960
- `ROADMAP.md`:217
- `TEST_MATRIX.md`:139, 155, 169, 321, 451, 545, 859, 893, 926

**TRACES — living docs (2 files, 2 lines):**
- `docs/lenses.md`:39
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:27

**TRACES — historical/record docs (39 files, 109 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (4 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (19 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (6 line-hits)
- `docs/audit/2026-07-12-compaction-pass.md` (1 line-hits)
- `docs/audit/2026-07-12-minor-gate-walk.md` (1 line-hits)
- `docs/audit/2026-07-12-once-read-rules-sweep.md` (4 line-hits)
- `docs/briefs/repairer-prompt.md` (1 line-hits)
- `docs/design-review/2026-07-15-1.7.0.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-05-row100.md` (1 line-hits)
- `docs/prover/2026-07-05-row103.md` (1 line-hits)
- `docs/prover/2026-07-06-feature-fit-retro.md` (1 line-hits)
- `docs/prover/2026-07-06-push-2.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (5 line-hits)
- `docs/prover/2026-07-07-humanize-rhythm.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-9.md` (4 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (6 line-hits)
- `docs/prover/2026-07-10-row210.md` (1 line-hits)
- `docs/prover/2026-07-10-row221.md` (1 line-hits)
- `docs/prover/2026-07-12-row256-live-channel.md` (1 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (2 line-hits)
- `docs/prover/2026-07-12-s41-crosscut-counter-architecture.md` (1 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (2 line-hits)
- `docs/prover/2026-07-15-327-harness-invariants.md` (3 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (9 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-stories-2-3.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (3 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (1 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (9 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (5 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)

---

### Rule 20 — SPEC INV-65

**Demands:** At setup or a repeated struggle, search installed skills and catalogs for a fit before building something new.

**Size:** 838 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-65; literal phrase "rule 20".

**TRACES — test files (1):**
- `tests/test_traceability.py` — test_skill_discovery

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (1):**
- `skills/communicator/SKILL.md`

**TRACES — root documents (4 files, 10 lines):**
- `ARCHITECTURE.md`:59, 77
- `PRODUCT_SPEC.md`:3806, 3807, 3811, 3812, 7969
- `ROADMAP.md`:217
- `TEST_MATRIX.md`:140, 935

**TRACES — living docs (2 files, 2 lines):**
- `docs/restyle-repoint-log.md`:11
- `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md`:24

**TRACES — historical/record docs (18 files, 30 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (2 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s23-4.md` (2 line-hits)
- `docs/prover/2026-07-07-row163.md` (1 line-hits)
- `docs/prover/2026-07-07-row165.md` (2 line-hits)
- `docs/prover/2026-07-18-row407-release-tier-rule.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (6 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (4 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (1 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/skill-review/2026-07-18-live-spec-base-build-pipeline.md` (1 line-hits)

---

### Rule 21 — SPEC INV-84

**Demands:** Durable human-facing prose is drafted by a fresh, rule-free writer session from a brief, never written by the author directly.

**Size:** 820 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-84; literal phrase "rule 21".

**TRACES — test files (3):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_readme_stance.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_clean_writer_law, test_push_to_remote_law

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (2):**
- `skills/communicator/SKILL.md`
- `skills/spec-author/SKILL.md`

**TRACES — root documents (3 files, 11 lines):**
- `ARCHITECTURE.md`:59, 78
- `PRODUCT_SPEC.md`:2961, 2962, 2966, 2968, 4332, 7988
- `TEST_MATRIX.md`:165, 434, 954

**TRACES — living docs (2 files, 3 lines):**
- `docs/lenses.md`:50, 57
- `docs/pair-adoption.md`:100

**TRACES — historical/record docs (22 files, 59 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (3 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (2 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (6 line-hits)
- `docs/prover/2026-07-10-night-postfold.md` (16 line-hits)
- `docs/prover/2026-07-10-onboarding-crosslink.md` (3 line-hits)
- `docs/prover/2026-07-10-row201.md` (1 line-hits)
- `docs/prover/2026-07-10-row213.md` (1 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (1 line-hits)
- `docs/prover/2026-07-12-row223-declared-laws.md` (1 line-hits)
- `docs/prover/2026-07-12-row242-readme-stance.md` (2 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (3 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (9 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/skill-review/2026-08-05-communicator-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-05-spec-author-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-07-live-spec-base.md` (1 line-hits)

---

### Rule 22 — SPEC INV-98

**Demands:** Name a concrete goal artifact up front; measure every iteration against that goal itself, never a proxy; lock gains by a mechanism.

**Size:** 1219 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-98; literal phrase "rule 22".

**TRACES — test files (2):**
- `tests/test_code_compaction_station.py` — (module-level, no enclosing test_ function)
- `tests/test_convergence_rule.py` — test_spec_anchor_index_and_playbook_cite

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (1):**
- `skills/communicator/SKILL.md`

**TRACES — root documents (3 files, 13 lines):**
- `ARCHITECTURE.md`:59, 79
- `PRODUCT_SPEC.md`:3048, 5290, 5291, 5295, 5296, 6456, 8002
- `TEST_MATRIX.md`:166, 321, 322, 968

**TRACES — living docs (2 files, 3 lines):**
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:10, 33
- `docs/restyle-repoint-log.md`:81

**TRACES — historical/record docs (21 files, 38 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (8 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (3 line-hits)
- `docs/audit/2026-07-12-minor-gate-walk.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-creator-walk.md` (1 line-hits)
- `docs/design/2026-07-17-node-growth-law.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-14.md` (1 line-hits)
- `docs/prover/2026-07-11-row218-convergence-rule.md` (3 line-hits)
- `docs/prover/2026-07-12-row256-live-channel.md` (1 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (2 line-hits)
- `docs/prover/2026-07-12-s41-inv135-per-kind-layers-proofs.md` (1 line-hits)
- `docs/prover/2026-07-18-row390-392-doc-rotation.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-06-suite-budget-row.md` (3 line-hits)
- `docs/prover/2026-08-07-recovery-plan-adversarial.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-06-communicator-commentable-provenance.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (3 line-hits)

---

### Rule 23 — SPEC INV-108

**Demands:** A behavioural rule that breaks mid-turn a second time earns a live channel: a prompt hook or a mechanical red check.

**Size:** 1198 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-108; literal phrase "rule 23".

**TRACES — test files (2):**
- `tests/test_behavioural_break_one_home.py` — (module-level, no enclosing test_ function)
- `tests/test_live_channel_law.py` — test_spec_anchor_and_index

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (0):**
- none found

**TRACES — root documents (3 files, 13 lines):**
- `ARCHITECTURE.md`:59, 80
- `PRODUCT_SPEC.md`:1134, 3492, 5310, 5311, 5315, 5316, 5579, 6477, 8012
- `TEST_MATRIX.md`:169, 978

**TRACES — living docs (1 files, 2 lines):**
- `docs/spec-format.md`:34, 42

**TRACES — historical/record docs (24 files, 63 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (9 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (1 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (2 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (3 line-hits)
- `docs/audit/2026-07-12-minor-gate-walk.md` (2 line-hits)
- `docs/audit/2026-07-12-once-read-rules-sweep.md` (7 line-hits)
- `docs/audit/2026-07-12-skill-creator-walk.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (2 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (5 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/language-reads/2026-07-28-read10-language-defects.md` (1 line-hits)
- `docs/prover/2026-07-12-row256-live-channel.md` (2 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (3 line-hits)
- `docs/prover/2026-07-12-s41-inv135-per-kind-layers-proofs.md` (1 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (10 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-07-recovery-plan-adversarial.md` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (2 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (2 line-hits)

---

### Rule 24 — SPEC INV-135

**Demands:** The pipeline's stations are kind-abstract; each project kind fills them with its own concrete layers and proof kinds.

**Size:** 2087 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-135, INV-36; literal phrase "rule 24".

**TRACES — test files (9):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_agent_card_gate.py` — (module-level, no enclosing test_ function)
- `tests/test_composition_axes.py` — test_spec_author_reads_declared_axes
- `tests/test_config_surface.py` — (module-level, no enclosing test_ function)
- `tests/test_design_principles.py` — (module-level, no enclosing test_ function)
- `tests/test_expensive_decision_read.py` — test_members_swept_enumerated
- `tests/test_founding_layers_proofs.py` — test_adopt_founding_prompts_layers_and_proofs, test_base_rulebook_states_layers_and_proofs, test_spec_clause_and_index
- `tests/test_founding_set_version.py` — (module-level, no enclosing test_ function)
- `tests/test_traceability.py` — test_project_kind, test_standard_vocabulary_crosswalk, test_template_carries_per_kind_node_structure

**TRACES — guardrail scripts (3):**
- `guardrails/check-agent-card.py`
- `guardrails/check-config-surface.py`
- `guardrails/check-push-reach.sh`

**TRACES — pipeline scripts/hooks (1):**
- `scripts/founding-questions.json`

**TRACES — other skill files (4):**
- `skills/build-pipeline/SKILL.md`
- `skills/product-prover/SKILL.md`
- `skills/spec-author/SKILL.md`
- `skills/test-author/SKILL.md`

**TRACES — root documents (4 files, 55 lines):**
- `ARCHITECTURE.md`:63, 244, 761, 763, 812, 831, 839, 843, 859, 867
- `PRODUCT_SPEC.md`:1634, 2736, 2768, 2788, 3969, 3975, 3976, 3977, 3993, 4001, 4007, 4008, 4012, 4017, 4018, 4034, 4309, 4571, 5146, 5237, 5396, 5830, 6335, 6336, 6342, 6344, 6345, 7262, 7275, 7277, 7940, 8039
- `ROADMAP.md`:52, 135, 215
- `TEST_MATRIX.md`:172, 173, 197, 241, 340, 478, 492, 527, 906, 1005

**TRACES — living docs (3 files, 3 lines):**
- `docs/architecture-method.md`:34
- `docs/onboarding-and-settings.md`:69
- `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md`:18

**TRACES — historical/record docs (31 files, 128 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (9 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (29 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (8 line-hits)
- `docs/design/2026-07-17-node-growth-law.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (6 line-hits)
- `docs/prover/2026-07-06-pushgate-s20-2.md` (2 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (5 line-hits)
- `docs/prover/2026-07-06-rows143-144.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-spec-to-tests.md` (2 line-hits)
- `docs/prover/2026-07-09-items45-prepush.md` (1 line-hits)
- `docs/prover/2026-07-09-row180.md` (1 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (2 line-hits)
- `docs/prover/2026-07-10-onboarding-crosslink.md` (1 line-hits)
- `docs/prover/2026-07-12-s41-inv135-per-kind-layers-proofs.md` (10 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (2 line-hits)
- `docs/prover/2026-07-13-row298-design-principles.md` (2 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (1 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (3 line-hits)
- `docs/prover/2026-07-18-rows380-388-reach-config-wrong-referral.md` (2 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (4 line-hits)
- `docs/prover/2026-07-21-axes-push-recheck.md` (5 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-17-from-track-coach-reach-classes-should-be-config.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (11 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (7 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/skill-review/2026-07-20-spec-author-axes.md` (3 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)

---

### Rule 25 — SPEC INV-137

**Demands:** The lead's context holds only orchestration essentials; reads done to discover or understand are dispatched to a worker for distillation.

**Size:** 1981 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-103, INV-137, INV-53, INV-69; literal phrase "rule 25".

**TRACES — test files (8):**
- `tests/test_chat_law_hook.py` — test_output_carries_the_routing_law
- `tests/test_delegation_line.py` — test_spec_anchor_and_index
- `tests/test_delegation_trigger_no_size.py` — test_no_pack_skill_states_a_size_or_time_delegation_trigger, test_scan_has_teeth
- `tests/test_footprint_note.py` — (module-level, no enclosing test_ function)
- `tests/test_forward_binding_and_infra_class.py` — test_every_binds_forward_clause_cites_the_law
- `tests/test_minor_gate_reconciliations.py` — test_d1_reading_discipline_composes_with_brief_read, test_d5_chat_law_hook_carries_reading_discipline
- `tests/test_orchestrator_read_discipline.py` — test_architecture_owns_137, test_base_rule_states_read_discipline, test_delegation_accounting_names_reads, test_matrix_row_for_137, test_spec_invariant_137_present_and_indexed
- `tests/test_traceability.py` — test_brief_trio_laws, test_pair_leadership_law, test_routing_rule, test_rule5_states_the_settled_delegation_rule

**TRACES — guardrail scripts (0):**
- none found

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (2):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/delegation-protocol.md`

**TRACES — root documents (3 files, 60 lines):**
- `ARCHITECTURE.md`:145, 153, 665
- `PRODUCT_SPEC.md`:639, 664, 1167, 4962, 4966, 4967, 5008, 5009, 5013, 5014, 5018, 5019, 5023, 5042, 5044, 5058, 5059, 5064, 5065, 5067, 5189, 5190, 5191, 5241, 5242, 5278, 5488, 5579, 7364, 7709, 7757, 7758, 7768, 7770, 7773, 7837, 7957, 7973, 8007, 8041
- `TEST_MATRIX.md`:151, 281, 283, 314, 315, 316, 329, 332, 342, 786, 788, 789, 797, 923, 939, 973, 1007

**TRACES — living docs (3 files, 5 lines):**
- `docs/lenses.md`:220
- `docs/restyle-repoint-log.md`:133, 136
- `docs/spec-format.md`:34, 42

**TRACES — historical/record docs (49 files, 306 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (22 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (8 line-hits)
- `docs/audit/2026-07-08/milestone-audit.md` (2 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (1 line-hits)
- `docs/audit/2026-07-12-delegation-dedup.md` (21 line-hits)
- `docs/design-review/2026-07-15-1.8.0.md` (2 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (2 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (5 line-hits)
- `docs/language-reads/2026-07-28-read16-chat-law-hook.md` (5 line-hits)
- `docs/measure/2026-07-29-specification-size.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-economy-ladder.md` (4 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (3 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-7.md` (1 line-hits)
- `docs/prover/2026-07-07-row56.md` (8 line-hits)
- `docs/prover/2026-07-07-rows111-113.md` (1 line-hits)
- `docs/prover/2026-07-10-row201.md` (1 line-hits)
- `docs/prover/2026-07-12-row253-routing-reminder.md` (2 line-hits)
- `docs/prover/2026-07-12-row254-delegation-check.md` (3 line-hits)
- `docs/prover/2026-07-12-row255-drafter-applier-form.md` (1 line-hits)
- `docs/prover/2026-07-12-s41-inv134-footprint-note-enforcement.md` (5 line-hits)
- `docs/prover/2026-07-13-gap0-read-discipline.md` (18 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (14 line-hits)
- `docs/prover/2026-07-15-1.8.0-minor-gate.md` (9 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (2 line-hits)
- `docs/prover/2026-07-15-332-inv163-audit.md` (1 line-hits)
- `docs/prover/2026-07-16-2.0-prose-batch.md` (2 line-hits)
- `docs/prover/2026-07-17-row417-cleanup-notice-and-inversions.md` (1 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (1 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-18-rows380-388-reach-config-wrong-referral.md` (1 line-hits)
- `docs/prover/2026-07-18-rows382-403-far-tier.md` (1 line-hits)
- `docs/prover/2026-07-18-rows384-387-gate-correctness.md` (1 line-hits)
- `docs/prover/2026-07-18-rows397-383-answer-first-no-dramatization.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (4 line-hits)
- `docs/prover/2026-07-23-row480.md` (3 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (1 line-hits)
- `docs/prover/2026-08-06-budget-never-bend-recheck.md` (4 line-hits)
- `docs/prover/2026-08-06-spec-table-regeneration.md` (1 line-hits)
- `docs/prover/2026-08-06-work-board.md` (8 line-hits)
- `docs/prover/2026-08-07-night-order-adversarial.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (17 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (103 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (1 line-hits)
- `docs/skill-review/2026-07-23-build-pipeline-row480.md` (4 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (2 line-hits)

---

### Rule 26 — SPEC INV-136, INV-139

**Demands:** Beside its layers and proofs, a project kind names checkable design principles that the verify pass runs.

**Size:** 679 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-135, INV-136, INV-139; literal phrase "rule 26".

**TRACES — test files (10):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_agent_card_gate.py` — (module-level, no enclosing test_ function)
- `tests/test_composition_axes.py` — test_spec_author_reads_declared_axes
- `tests/test_config_surface.py` — (module-level, no enclosing test_ function)
- `tests/test_design_principles.py` — test_adopt_founding_prompts_design_principles, test_interactive_overlap_has_one_full_home_the_spec, test_prover_carries_the_interactive_overlap_lens, test_spec_author_reads_declared_design_principles, test_spec_clause_and_index, test_verify_feel_pass_reads_design_principles
- `tests/test_founding_layers_proofs.py` — test_adopt_founding_prompts_layers_and_proofs, test_base_rulebook_states_layers_and_proofs, test_spec_clause_and_index
- `tests/test_founding_set_version.py` — (module-level, no enclosing test_ function)
- `tests/test_legibility_floor.py` — test_matrix_row, test_spec_clause_and_index
- `tests/test_minor_gate_reconciliations.py` — test_base_rule_26_homes_design_principles
- `tests/test_pack_to_host_split.py` — test_no_site_re_derives_the_split_in_its_own_words

**TRACES — guardrail scripts (3):**
- `guardrails/check-agent-card.py`
- `guardrails/check-config-surface.py`
- `guardrails/check-push-reach.sh`

**TRACES — pipeline scripts/hooks (2):**
- `scripts/founding-questions.json`
- `scripts/preshow-legibility-lint.py`

**TRACES — other skill files (6):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/work-kind-table.md`
- `skills/communicator/SKILL.md`
- `skills/product-prover/SKILL.md`
- `skills/spec-author/SKILL.md`
- `skills/test-author/SKILL.md`

**TRACES — root documents (4 files, 69 lines):**
- `ARCHITECTURE.md`:63, 83, 763, 785, 796, 802, 812, 831, 839, 841, 843, 867
- `PRODUCT_SPEC.md`:1522, 1523, 1634, 4001, 4007, 4008, 4012, 4017, 4018, 4027, 4033, 4034, 4035, 4036, 4040, 4041, 4045, 4046, 4054, 4060, 4064, 4065, 4066, 4070, 4571, 5396, 5830, 6300, 6321, 6335, 6336, 6342, 6343, 6344, 6345, 6405, 6426, 7275, 7277, 7284, 7285, 8039, 8040, 8043
- `ROADMAP.md`:111, 112, 215
- `TEST_MATRIX.md`:172, 173, 174, 197, 241, 492, 527, 1005, 1006, 1009

**TRACES — living docs (4 files, 5 lines):**
- `docs/audits/2026-08-07-number-census.md`:107
- `docs/lenses.md`:215, 231
- `docs/restyle-repoint-log.md`:83
- `docs/spec-compaction-protocol.md`:42

**TRACES — historical/record docs (40 files, 159 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (11 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (27 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (7 line-hits)
- `docs/audit/2026-07-16-prover-fable.md` (4 line-hits)
- `docs/design-review/2026-07-15-1.8.0.md` (5 line-hits)
- `docs/design-review/2026-07-16-2.3.0.md` (1 line-hits)
- `docs/design-review/2026-07-16-2p2p0.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (2 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (2 line-hits)
- `docs/design/2026-07-17-node-growth-law.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (8 line-hits)
- `docs/prover/2026-07-12-s41-inv135-per-kind-layers-proofs.md` (4 line-hits)
- `docs/prover/2026-07-13-gap1-edge-completeness.md` (1 line-hits)
- `docs/prover/2026-07-13-gap2-legibility-floor.md` (8 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (12 line-hits)
- `docs/prover/2026-07-13-prover-overlap-lens.md` (2 line-hits)
- `docs/prover/2026-07-13-prover-self-review.md` (1 line-hits)
- `docs/prover/2026-07-13-row298-design-principles.md` (6 line-hits)
- `docs/prover/2026-07-14-design-review.md` (1 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (4 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (1 line-hits)
- `docs/prover/2026-07-15-332-inv163-audit.md` (6 line-hits)
- `docs/prover/2026-07-15-minor-gate-1.5.0.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (1 line-hits)
- `docs/prover/2026-07-17-2.4.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-17-2.5.0-minor-gate.md` (2 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-18-rows380-388-reach-config-wrong-referral.md` (2 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (4 line-hits)
- `docs/prover/2026-07-21-axes-push-recheck.md` (6 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/architecture-prover-record.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-17-from-track-coach-reach-classes-should-be-config.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (4 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (9 line-hits)
- `docs/skill-review/2026-07-20-spec-author-axes.md` (5 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 27 — SPEC INV-143

**Demands:** The seat decides mechanical steps, artifact-determined values, and sensible defaults; only genuine taste, trade-off, or correctness calls reach the human.

**Size:** 710 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-121, INV-143, INV-4, INV-48, INV-70; literal phrase "rule 27".

**TRACES — test files (19, of which 8 are synthetic-placeholder noise, see below):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/fixtures/specformat/mini_added.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/mini_added_oversized.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/mini_budget_over.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_bullets_clean.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_bullets_dirty.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_clean.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/readability_dirty.md` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/fixtures/specformat/rec_added_new.json` — (module-level, no enclosing test_ function)  *(SYNTHETIC placeholder corpus — a spec-format-lint fixture using made-up sequential INV-1..7 example codes, not a reference to this rule; see the methodology note above)*
- `tests/test_board.py` — test_gate_reds_a_parked_question_with_no_default
- `tests/test_delta_classifier.py` — test_appeared_undeclared_reds
- `tests/test_derive_before_fork.py` — test_formal_index_row, test_spec_clause_stands
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_guardrails.py` — test_leading_handle_goes_red
- `tests/test_impact_analysis_entry.py` — test_spec_cites_derive_before_fork
- `tests/test_index_generated.py` — test_reds_a_body_code_the_index_misses
- `tests/test_resume_digest.py` — test_template_states_the_law
- `tests/test_seat_acts_by_default.py` — test_architecture_owns_143, test_base_rule_states_the_default_action_posture, test_matrix_row_for_143, test_spec_invariant_143_present_and_indexed
- `tests/test_traceability.py` — test_parameter_default, test_spec_states_founding_and_designsync

**TRACES — guardrail scripts (4):**
- `guardrails/check-board.py`
- `guardrails/check-delta-record.py`
- `guardrails/route_agent_transport.py`
- `guardrails/specformat.py`

**TRACES — pipeline scripts/hooks (3):**
- `scripts/gate_common.py`
- `scripts/preshow-legibility-lint.py`
- `scripts/spec-style-lint.py`

**TRACES — other skill files (5):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/excuses-table.md`
- `skills/design-reviewer/SKILL.md`
- `skills/feedback-intake/SKILL.md`
- `skills/product-prover/SKILL.md`

**TRACES — root documents (4 files, 83 lines):**
- `ARCHITECTURE.md`:63, 84, 145, 235, 875, 882
- `PRODUCT_SPEC.md`:405, 464, 485, 500, 501, 502, 715, 742, 754, 933, 984, 1147, 1199, 1219, 1415, 1443, 1677, 1678, 1732, 1734, 1738, 1739, 1805, 1853, 1901, 2070, 2092, 2864, 2865, 2866, 3029, 3180, 3465, 3559, 3663, 3706, 3895, 4550, 4764, 5081, 5082, 5086, 5087, 5101, 5109, 5155, 5520, 5554, 5579, 5757, 7908, 7952, 7974, 8025, 8047
- `ROADMAP.md`:132
- `TEST_MATRIX.md`:175, 176, 177, 282, 289, 290, 324, 325, 333, 334, 335, 340, 413, 453, 526, 604, 874, 918, 940, 991, 1013

**TRACES — living docs (5 files, 7 lines):**
- `docs/lenses.md`:172
- `docs/plans/2026-07-29-specification-subdivision.md`:219, 287
- `docs/spec-format.md`:34, 42
- `docs/spec-style.md`:145
- `docs/worker-liveness.md`:57

**TRACES — historical/record docs (98 files, 268 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (5 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (57 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (16 line-hits)
- `docs/audit/2026-07-05/pass1-prover-fable.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (3 line-hits)
- `docs/audit/2026-07-16-batch-2p2p0.md` (1 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (2 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (3 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (2 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (4 line-hits)
- `docs/evals/2026-07-05-first-run/bare-spec-author.md` (1 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/bare-spec-author.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-06-rerun/scores-build-pipeline.md` (2 line-hits)
- `docs/evals/2026-07-06-rerun/with-skill-build-pipeline.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-04.md` (1 line-hits)
- `docs/prover/2026-07-05-classes.md` (1 line-hits)
- `docs/prover/2026-07-05-facets.md` (2 line-hits)
- `docs/prover/2026-07-05-founding-designsync.md` (3 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (3 line-hits)
- `docs/prover/2026-07-05-row100.md` (2 line-hits)
- `docs/prover/2026-07-05-row86.md` (1 line-hits)
- `docs/prover/2026-07-05-row99.md` (1 line-hits)
- `docs/prover/2026-07-05-v11-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v14-push.md` (1 line-hits)
- `docs/prover/2026-07-05-v15-push.md` (1 line-hits)
- `docs/prover/2026-07-06-night.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s21-2.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s21.md` (1 line-hits)
- `docs/prover/2026-07-06-row138.md` (2 line-hits)
- `docs/prover/2026-07-06-row142.md` (2 line-hits)
- `docs/prover/2026-07-06-row145.md` (2 line-hits)
- `docs/prover/2026-07-06-rows108-119.md` (2 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-bootstrap.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-rhythm.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk1.md` (3 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk10.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk3.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk5.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk7.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk9.md` (2 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-11.md` (1 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (3 line-hits)
- `docs/prover/2026-07-09-full-reprove-session29-body.md` (1 line-hits)
- `docs/prover/2026-07-09-row181.md` (1 line-hits)
- `docs/prover/2026-07-09-row187.md` (1 line-hits)
- `docs/prover/2026-07-09-rows182-186.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (8 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (1 line-hits)
- `docs/prover/2026-07-10-night-postfold.md` (2 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (1 line-hits)
- `docs/prover/2026-07-12-row226-checkpoint-closes.md` (1 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (5 line-hits)
- `docs/prover/2026-07-12-s40-inv124-class-hunt.md` (1 line-hits)
- `docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md` (3 line-hits)
- `docs/prover/2026-07-13-gap2-legibility-floor.md` (1 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (7 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (3 line-hits)
- `docs/prover/2026-07-15-321-feedback-collector.md` (2 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (2 line-hits)
- `docs/prover/2026-07-16-2.3.0-minor-gate.md` (5 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (2 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (2 line-hits)
- `docs/prover/2026-07-16-prover-doc-restructure.md` (1 line-hits)
- `docs/prover/2026-07-17-2.4.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-17-2.5.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-17-lanes-and-self-declaration.md` (5 line-hits)
- `docs/prover/2026-07-18-row-396-transport-split.md` (1 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (2 line-hits)
- `docs/prover/2026-07-18-rows397-383-answer-first-no-dramatization.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (2 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (2 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-06-suite-budget-row.md` (3 line-hits)
- `docs/prover/2026-08-07-recovery-plan-adversarial.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/push-review/2026-08-07-the-night-order-and-the-morning-orders.md` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (1 line-hits)
- `docs/queue-archive/2026-07-10-v1.0.0-milestone.md` (1 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (14 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (15 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (1 line-hits)
- `docs/skill-review/2026-07-18-product-prover.md` (1 line-hits)
- `docs/skill-review/2026-08-05-design-reviewer-readability.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 28 — SPEC INV-145

**Demands:** Beyond the continuous lints, a full adversarial whole-read audit of the living documents runs every ten landings.

**Size:** 1121 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-145, INV-46, INV-70, M-1; literal phrase "rule 28".

**TRACES — test files (14):**
- `tests/fixtures/scaffold_guardrails/host-clean/TEST_MATRIX.md` — (module-level, no enclosing test_ function)
- `tests/test_architecture_prove_seam.py` — (module-level, no enclosing test_ function)
- `tests/test_architecture_proved_at_full_pass.py` — (module-level, no enclosing test_ function)
- `tests/test_clean_context_review.py` — (module-level, no enclosing test_ function)
- `tests/test_compaction_discipline.py` — test_removal_keeps_meaning_phrase
- `tests/test_deferred_revisit_cadence.py` — (module-level, no enclosing test_ function)
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_guardrails.py` — test_leading_handle_goes_red, test_matrix_permits_the_fixture_ledger_and_a_test_name
- `tests/test_matrix_reference.py` — test_builder_expands_ranges_and_compounds
- `tests/test_milestone_enumerates_design_review.py` — test_m1_list_names_the_design_review, test_m1_step_lands_the_dated_record
- `tests/test_minor_gate_reconciliations.py` — test_base_rule_26_homes_design_principles
- `tests/test_periodic_full_audit.py` — test_architecture_owns_145, test_audit_is_defined_adversarial_by_nature_once, test_matrix_row_for_145, test_spec_invariant_145_present_and_indexed
- `tests/test_review_record_class.py` — test_names_every_member
- `tests/test_traceability.py` — test_adversarial_verify_option, test_m1_names_loader_thin_item, test_m1_names_skill_creator_rewalk, test_parameter_default, test_rule5_states_the_settled_delegation_rule

**TRACES — guardrail scripts (1):**
- `guardrails/check-earned-message.py`

**TRACES — pipeline scripts/hooks (1):**
- `scripts/preshow-legibility-lint.py`

**TRACES — other skill files (1):**
- `skills/build-pipeline/SKILL.md`

**TRACES — root documents (4 files, 95 lines):**
- `ARCHITECTURE.md`:63, 85, 145, 152, 631, 645, 875, 900, 901
- `PRODUCT_SPEC.md`:1275, 1649, 1657, 1732, 1734, 1738, 1739, 1903, 1907, 2168, 2542, 2982, 2983, 2991, 2992, 2996, 3000, 3003, 3009, 3013, 3029, 3030, 3034, 3180, 3735, 3778, 3792, 4500, 4802, 5081, 5123, 5124, 5128, 5131, 5152, 5170, 5276, 5277, 5520, 5554, 5940, 7378, 7950, 7974, 8049, 8219
- `ROADMAP.md`:85, 94, 98, 132
- `TEST_MATRIX.md`:18, 143, 145, 147, 149, 150, 156, 159, 175, 176, 211, 216, 270, 273, 275, 276, 280, 282, 289, 295, 296, 322, 326, 330, 331, 340, 341, 390, 471, 506, 525, 770, 916, 940, 1015, 1185

**TRACES — living docs (5 files, 7 lines):**
- `docs/lenses.md`:27
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:15, 28, 34
- `docs/restyle-repoint-log.md`:44
- `docs/spec-compaction-protocol.md`:43
- `docs/worker-liveness.md`:44

**TRACES — historical/record docs (120 files, 386 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (9 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (37 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (31 line-hits)
- `docs/audit/2026-07-05-night/composition-architecture.md` (1 line-hits)
- `docs/audit/2026-07-05-night/matrix-audit.md` (2 line-hits)
- `docs/audit/2026-07-05/model-comparison.md` (2 line-hits)
- `docs/audit/2026-07-05/pass1-prover-fable.md` (5 line-hits)
- `docs/audit/2026-07-05/pass1-prover-opus.md` (4 line-hits)
- `docs/audit/2026-07-05/pass2-matrix-opus.md` (2 line-hits)
- `docs/audit/2026-07-06-skill-creator-walk.md` (3 line-hits)
- `docs/audit/2026-07-12-compaction-pass.md` (1 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (3 line-hits)
- `docs/audit/2026-07-12-deferred-trigger-rescan.md` (4 line-hits)
- `docs/audit/2026-07-12-minor-gate-walk.md` (6 line-hits)
- `docs/audit/2026-07-12-skill-creator-walk.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (1 line-hits)
- `docs/audit/2026-07-15-1.8.0-audit.md` (1 line-hits)
- `docs/audit/2026-07-16-batch-2p1p0.md` (1 line-hits)
- `docs/design-review/2026-07-14.md` (3 line-hits)
- `docs/design-review/2026-07-15.md` (2 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (3 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-04-v03-push.md` (2 line-hits)
- `docs/prover/2026-07-04-v04-push.md` (3 line-hits)
- `docs/prover/2026-07-05-architecture.md` (1 line-hits)
- `docs/prover/2026-07-05-base-skill.md` (1 line-hits)
- `docs/prover/2026-07-05-classes.md` (1 line-hits)
- `docs/prover/2026-07-05-facets.md` (1 line-hits)
- `docs/prover/2026-07-05-fences.md` (2 line-hits)
- `docs/prover/2026-07-05-founding-designsync.md` (1 line-hits)
- `docs/prover/2026-07-05-intake-trio.md` (1 line-hits)
- `docs/prover/2026-07-05-lost-layers.md` (3 line-hits)
- `docs/prover/2026-07-05-row100.md` (2 line-hits)
- `docs/prover/2026-07-05-row94.md` (2 line-hits)
- `docs/prover/2026-07-05-rows57-60.md` (4 line-hits)
- `docs/prover/2026-07-05-v15-5-full.md` (2 line-hits)
- `docs/prover/2026-07-05-v15-8-full.md` (1 line-hits)
- `docs/prover/2026-07-05-v15-9.md` (3 line-hits)
- `docs/prover/2026-07-05.md` (3 line-hits)
- `docs/prover/2026-07-06-push.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s20.md` (1 line-hits)
- `docs/prover/2026-07-06-pushgate-s22-5.md` (2 line-hits)
- `docs/prover/2026-07-06-row130.md` (2 line-hits)
- `docs/prover/2026-07-06-row135.md` (1 line-hits)
- `docs/prover/2026-07-06-row140.md` (1 line-hits)
- `docs/prover/2026-07-06-row142.md` (1 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-one-rulebook.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-problem-ledger.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-rhythm.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk10.md` (1 line-hits)
- `docs/prover/2026-07-07-row56.md` (2 line-hits)
- `docs/prover/2026-07-07-rows111-113.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (2 line-hits)
- `docs/prover/2026-07-09-full-reprove-session29-body.md` (2 line-hits)
- `docs/prover/2026-07-09-row181.md` (1 line-hits)
- `docs/prover/2026-07-09-rows182-186.md` (1 line-hits)
- `docs/prover/2026-07-09-small-holes.md` (1 line-hits)
- `docs/prover/2026-07-10-m1-audit.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (10 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (1 line-hits)
- `docs/prover/2026-07-10-night-postfold.md` (2 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (3 line-hits)
- `docs/prover/2026-07-12-release-1.1.0.md` (1 line-hits)
- `docs/prover/2026-07-12-row279-adopt-impersonal-voice.md` (2 line-hits)
- `docs/prover/2026-07-12-s38-batch-inv117-120.md` (1 line-hits)
- `docs/prover/2026-07-12-s38-inv115-inv116-and-architecture.md` (8 line-hits)
- `docs/prover/2026-07-12-s40-inv129-deferred-revisit-cadence.md` (2 line-hits)
- `docs/prover/2026-07-12-s40-inv46-audit-trigger-broadened.md` (7 line-hits)
- `docs/prover/2026-07-13-gap2-legibility-floor.md` (1 line-hits)
- `docs/prover/2026-07-13-prover-overlap-lens.md` (1 line-hits)
- `docs/prover/2026-07-13-prover-self-review.md` (1 line-hits)
- `docs/prover/2026-07-13-row298-design-principles.md` (1 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (13 line-hits)
- `docs/prover/2026-07-14-cross-host-coordinator.md` (2 line-hits)
- `docs/prover/2026-07-14-design-review.md` (1 line-hits)
- `docs/prover/2026-07-14-monitor-schedule.md` (2 line-hits)
- `docs/prover/2026-07-14-property-routing.md` (3 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (2 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (2 line-hits)
- `docs/prover/2026-07-15-322-forward-binding-and-323-review-record-class.md` (10 line-hits)
- `docs/prover/2026-07-15-inv154-fixed-point-loop.md` (3 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (8 line-hits)
- `docs/prover/2026-07-15-minor-gate-1.5.0.md` (2 line-hits)
- `docs/prover/2026-07-16-2.3.0-minor-gate.md` (4 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-18-release-2.8.0.md` (3 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (5 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-18-rows397-383-answer-first-no-dramatization.md` (1 line-hits)
- `docs/prover/2026-07-19.md` (1 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (1 line-hits)
- `docs/prover/2026-07-20-comms.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (1 line-hits)
- `docs/prover/2026-07-20-conduct-stories-2-3.md` (1 line-hits)
- `docs/prover/2026-07-23-row477-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-06-budget-never-bend-recheck.md` (6 line-hits)
- `docs/prover/2026-08-06-spec-table-regeneration.md` (2 line-hits)
- `docs/prover/2026-08-06-suite-budget-row.md` (3 line-hits)
- `docs/prover/architecture-prover-record.md` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-05.md` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/2026-07-10-v1.0.0-milestone.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (21 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07-18.md` (2 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (28 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (4 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (2 line-hits)
- `docs/skill-review/2026-07-18-inv237-wiring.md` (4 line-hits)
- `docs/skill-review/2026-07-23-build-pipeline-row456.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (2 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (1 line-hits)

---

### Rule 29 — SPEC INV-152

**Demands:** A parked, needs-the-human's-word item is re-tested for derivability every time it's touched; an unjustified marker defaults to the seat's own work.

**Size:** 2138 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-121, INV-143, INV-151, INV-152, INV-153, INV-155, INV-28, INV-59; script names guardrails/check-deferral-marker.py, hooks/chat-law-hook.sh; literal phrase "rule 29".

**TRACES — test files (25):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_agent_channels.py` — test_homeless_question_is_dropped, test_the_holding_is_itself_the_finding
- `tests/test_chat_law_hook.py` — test_output_carries_the_deferral_law
- `tests/test_code_anchor_scan.py` — test_bracketed_anchor_in_a_document_line_passes, test_naked_invariant_code_reds
- `tests/test_deferral_marker.py` — (module-level, no enclosing test_ function)
- `tests/test_derive_before_fork.py` — test_formal_index_row, test_spec_clause_stands
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_flaky_test_is_a_defect.py` — test_flaky_test_is_a_defect_build_pipeline_green_definition, test_flaky_test_is_a_defect_test_author_determinism_rule
- `tests/test_forward_binding_and_infra_class.py` — (module-level, no enclosing test_ function)
- `tests/test_guardrails.py` — test_machine_local_pins_skip_in_ci_only, test_outcome_led_and_trailing_anchor_pass
- `tests/test_harness_template.py` — test_template_probes_for_a_frame_at_launch
- `tests/test_hedge_arm.py` — (module-level, no enclosing test_ function)
- `tests/test_impact_analysis_entry.py` — test_spec_cites_derive_before_fork
- `tests/test_interface_coverage.py` — test_pack_declared_laws_each_have_a_covering_test
- `tests/test_lane_branch_road.py` — (module-level, no enclosing test_ function)
- `tests/test_minor_gate_reconciliations.py` — test_base_rule_26_homes_design_principles, test_d5_chat_law_hook_carries_reading_discipline
- `tests/test_named_reference.py` — test_spec_states_the_earned_auto_deposit_law
- `tests/test_no_retry_plugin.py` — test_no_retry_plugin
- `tests/test_progress_report.py` — test_a_file_with_no_record_entry_prints_not_measured_not_zero
- `tests/test_request_classifier.py` — test_count_word_tracks_the_control_set, test_deferral_clause_stands, test_entry_layer_criterion_stands, test_inv151_index_and_ownership, test_inv152_index_and_ownership, test_inv153_index_and_ownership, test_lives_in_the_base_rulebook, test_names_all_four_controls, test_one_plain_question_fallback, test_the_count_agrees_across_its_homes, test_unification_clause_stands
- `tests/test_seat_acts_by_default.py` — test_architecture_owns_143, test_base_rule_states_the_default_action_posture, test_matrix_row_for_143, test_spec_invariant_143_present_and_indexed
- `tests/test_setup_entry.py` — test_three_setup_rows_each_naming_entry_and_back_check
- `tests/test_traceability.py` — test_bookkeeping_never_list, test_narration_three_teeth, test_outcome_leads_law, test_promoter_harvest_trio, test_task_list_plain_words
- `tests/test_vacuous_pass.py` — (module-level, no enclosing test_ function)
- `tests/test_withdrawal_convergence.py` — test_spec_states_the_bound_and_its_kin

**TRACES — guardrail scripts (7):**
- `guardrails/README.md`
- `guardrails/check-deferral-marker.py`
- `guardrails/check-deposit-description.py`
- `guardrails/judge-hooks.json`
- `guardrails/language-rules.json`
- `guardrails/nonempty_input.py`
- `guardrails/progress-baseline.json`

**TRACES — pipeline scripts/hooks (5):**
- `scripts/preshow-lint.py`
- `scripts/progress-report.py`
- `scripts/shipped-language-allowlist.json`
- `scripts/spec-freeze.json`
- `scripts/spec-freeze.py`

**TRACES — other skill files (8):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/request-kind-table.md`
- `skills/communicator/SKILL.md`
- `skills/communicator/references/field-examples.md`
- `skills/design-reviewer/SKILL.md`
- `skills/feedback-intake/SKILL.md`
- `skills/product-prover/SKILL.md`
- `skills/test-author/SKILL.md`

**TRACES — root documents (4 files, 138 lines):**
- `ARCHITECTURE.md`:63, 84, 145, 209, 546, 669
- `PRODUCT_SPEC.md`:418, 437, 500, 501, 624, 625, 629, 630, 634, 635, 639, 644, 746, 750, 878, 964, 968, 969, 1147, 1185, 1186, 1190, 1199, 1375, 1410, 1415, 1423, 1424, 1518, 1693, 2070, 2183, 2536, 2537, 2538, 2542, 2543, 2579, 2616, 2731, 3487, 3604, 3680, 4407, 4486, 4505, 4662, 4669, 4699, 4764, 4779, 5081, 5082, 5086, 5087, 5101, 5102, 5103, 5107, 5109, 5155, 5548, 5579, 5763, 6060, 7079, 7080, 7132, 7137, 7170, 7637, 7697, 7699, 7707, 7713, 7725, 7734, 7752, 7826, 7932, 7963, 8025, 8047, 8055, 8056, 8057, 8059
- `ROADMAP.md`:57, 59, 132, 143, 215
- `TEST_MATRIX.md`:175, 177, 178, 181, 184, 186, 196, 290, 325, 334, 335, 336, 340, 357, 403, 405, 406, 407, 408, 409, 416, 423, 435, 496, 512, 601, 604, 615, 646, 714, 764, 785, 898, 929, 991, 1013, 1021, 1022, 1023, 1025

**TRACES — living docs (14 files, 24 lines):**
- `docs/MEASUREMENTS.md`:8
- `docs/PROGRESS.md`:17, 23
- `docs/audits/2026-08-07-number-census.md`:25
- `docs/language-rule-coverage.md`:198, 342, 360, 868, 900, 904
- `docs/language-rules.md`:821
- `docs/lenses.md`:17, 172
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:8, 33
- `docs/onboarding-and-settings.md`:100, 102
- `docs/plans/2026-07-28-two-goals-one-campaign.md`:97
- `docs/plans/2026-07-29-specification-subdivision.md`:414
- `docs/spec-compaction-protocol.md`:15
- `docs/spec-format.md`:34, 42
- `docs/spec-style.md`:126
- `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md`:82

**TRACES — historical/record docs (104 files, 441 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (5 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (77 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (29 line-hits)
- `docs/audit/2026-07-12-skill-evals-rerun.md` (1 line-hits)
- `docs/audit/2026-07-15-1.8.0-audit.md` (1 line-hits)
- `docs/audit/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/audit/2026-07-23-tlvphotos-conduct-evidence.md` (1 line-hits)
- `docs/audit/2026-07-23-tlvphotos-conduct-verdicts.md` (1 line-hits)
- `docs/briefs/2026-07-28-findings-ratchet-brief.md` (1 line-hits)
- `docs/briefs/2026-07-28-one-ceiling-law-brief.md` (2 line-hits)
- `docs/briefs/2026-07-28-record-the-settled-answer-brief.md` (4 line-hits)
- `docs/briefs/2026-07-28-session-reading-process-brief.md` (1 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (7 line-hits)
- `docs/design-review/2026-07-15-1.7.0.md` (6 line-hits)
- `docs/design-review/2026-07-16-2.3.0.md` (2 line-hits)
- `docs/design-review/2026-07-16-2p2p0.md` (2 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (2 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (2 line-hits)
- `docs/design-review/2026-07-19.md` (6 line-hits)
- `docs/design/2026-07-17-node-growth-law.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (2 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (4 line-hits)
- `docs/evals/2026-07-06-batch2-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-push-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-06-rows126-128-rerun/scores.md` (1 line-hits)
- `docs/evals/2026-07-10-rerun/scores.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/handovers/2026-07-28-readability-campaign-handover.md` (4 line-hits)
- `docs/handovers/2026-07-29-176e927f-4e67-4fa6-887e-86d1d6e5d1e4-handover.md` (1 line-hits)
- `docs/language-reads/2026-07-28-read16-chat-law-hook.md` (4 line-hits)
- `docs/prover/2026-07-06-feature-fit-retro.md` (1 line-hits)
- `docs/prover/2026-07-06-row116.md` (4 line-hits)
- `docs/prover/2026-07-06-row131.md` (2 line-hits)
- `docs/prover/2026-07-06-row133.md` (3 line-hits)
- `docs/prover/2026-07-06-row136.md` (2 line-hits)
- `docs/prover/2026-07-06-row138.md` (2 line-hits)
- `docs/prover/2026-07-06-row139.md` (1 line-hits)
- `docs/prover/2026-07-06-row141.md` (2 line-hits)
- `docs/prover/2026-07-06-row142.md` (1 line-hits)
- `docs/prover/2026-07-06-rows126-128.md` (7 line-hits)
- `docs/prover/2026-07-06-rows129-132.md` (1 line-hits)
- `docs/prover/2026-07-06-rows143-144.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-adoption.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-sending-feedback-in.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk1.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk10.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk2.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk3.md` (2 line-hits)
- `docs/prover/2026-07-07-humanize-wish-walk-chunk5.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-10.md` (1 line-hits)
- `docs/prover/2026-07-07-pushgate-s22-11.md` (1 line-hits)
- `docs/prover/2026-07-07-row47.md` (1 line-hits)
- `docs/prover/2026-07-07-rows149-152.md` (1 line-hits)
- `docs/prover/2026-07-08-humanize-whole-doc.md` (7 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (3 line-hits)
- `docs/prover/2026-07-10-night-pair-wave.md` (1 line-hits)
- `docs/prover/2026-07-10-night-postfold.md` (7 line-hits)
- `docs/prover/2026-07-10-row232.md` (1 line-hits)
- `docs/prover/2026-07-10-row237.md` (1 line-hits)
- `docs/prover/2026-07-11-row249-hook-no-scissors.md` (1 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (1 line-hits)
- `docs/prover/2026-07-12-row223-declared-laws.md` (1 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (5 line-hits)
- `docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md` (3 line-hits)
- `docs/prover/2026-07-12-s40-inv130-withdrawal-convergence.md` (4 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (5 line-hits)
- `docs/prover/2026-07-14-design-review.md` (2 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (16 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (5 line-hits)
- `docs/prover/2026-07-15-1.8.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (1 line-hits)
- `docs/prover/2026-07-15-327-harness-invariants.md` (21 line-hits)
- `docs/prover/2026-07-15-deferral-guard.md` (18 line-hits)
- `docs/prover/2026-07-15-inv154-fixed-point-loop.md` (2 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (16 line-hits)
- `docs/prover/2026-07-15-minor-gate-1.5.0.md` (4 line-hits)
- `docs/prover/2026-07-16-2.3.0-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-16-2p1p1-prepush.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (5 line-hits)
- `docs/prover/2026-07-17-agent-communication.md` (5 line-hits)
- `docs/prover/2026-07-17-lanes-and-self-declaration.md` (1 line-hits)
- `docs/prover/2026-07-17-row417-cleanup-notice-and-inversions.md` (2 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (4 line-hits)
- `docs/prover/2026-07-18-rows384-387-gate-correctness.md` (1 line-hits)
- `docs/prover/2026-07-18-rows402-409-touchpoint-instances.md` (1 line-hits)
- `docs/prover/2026-07-19.md` (15 line-hits)
- `docs/prover/2026-07-20-comms.md` (3 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (1 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (3 line-hits)
- `docs/prover/2026-07-27-language-gate-reach.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate-addendum.md` (2 line-hits)
- `docs/prover/2026-07-27-push-gate.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (2 line-hits)
- `docs/prover/2026-08-07-night-order-adversarial.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-16-row364.txt` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/2026-07-08-milestone-compaction.md` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (18 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (22 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (2 line-hits)
- `docs/reports/2026-07-29-session-report.md` (2 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (1 line-hits)

---

### Rule 30 — SPEC INV-164

**Demands:** Any property a machine can verify becomes a blocking gate run on every push, held by no one's attention.

**Size:** 939 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-115, INV-123, INV-164, INV-97, INV-98; literal phrase "rule 30".

**TRACES — test files (14):**
- `tests/test_agent_card_gate.py` — test_gate_passes_the_pack_own_tree, test_spec_states_the_law
- `tests/test_answer_first_arm.py` — (module-level, no enclosing test_ function)
- `tests/test_code_compaction_station.py` — test_formal_index_row, test_spec_clause_and_index
- `tests/test_compaction_discipline.py` — test_base_rulebook_carries_the_principle, test_build_pipeline_carries_compaction_every_pass, test_compaction_is_continuous, test_index_row_present, test_removal_keeps_meaning_phrase, test_spec_anchor, test_spec_anchor_and_index
- `tests/test_convergence_rule.py` — test_spec_anchor_index_and_playbook_cite
- `tests/test_deposit_description.py` — (module-level, no enclosing test_ function)
- `tests/test_design_reviewer.py` — test_inventory_never_a_rival_registry
- `tests/test_four_checks_contract.py` — test_spec_anchor_and_index
- `tests/test_node_growth.py` — test_live_architecture_within_caps
- `tests/test_readme_stance.py` — (module-level, no enclosing test_ function)
- `tests/test_scaffold_guardrails.py` — (module-level, no enclosing test_ function)
- `tests/test_scaffold_install.py` — (module-level, no enclosing test_ function)
- `tests/test_setup_entry.py` — test_registry_is_created_after_the_config_and_takes_its_name
- `tests/test_suite_budget.py` — (module-level, no enclosing test_ function)

**TRACES — guardrail scripts (10):**
- `guardrails/README.md`
- `guardrails/check-agent-card.py`
- `guardrails/check-deposit-description.py`
- `guardrails/check-description-field.py`
- `guardrails/check-earned-message.py`
- `guardrails/check-handover-provenance.py`
- `guardrails/check-rendered-sweep.py`
- `guardrails/check-suite-budget.sh`
- `guardrails/check-tests.sh`
- `guardrails/node_growth_counter.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (3):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/minor-bump-gate.md`
- `skills/design-reviewer/SKILL.md`

**TRACES — root documents (4 files, 61 lines):**
- `ARCHITECTURE.md`:59, 79, 145, 311
- `PRODUCT_SPEC.md`:2732, 2996, 3000, 3029, 3048, 3049, 3053, 3879, 4574, 4703, 5290, 5291, 5295, 5296, 5392, 5441, 5443, 5447, 5448, 5452, 5453, 5799, 5824, 6209, 6456, 6460, 6477, 6501, 6545, 8001, 8002, 8019, 8027, 8068
- `ROADMAP.md`:128
- `TEST_MATRIX.md`:166, 176, 321, 322, 330, 339, 434, 559, 560, 561, 562, 563, 571, 602, 603, 617, 618, 967, 968, 985, 993, 1034

**TRACES — living docs (5 files, 12 lines):**
- `docs/audits/2026-08-07-number-census.md`:15, 207
- `docs/language-worked-example.md`:34, 166, 179
- `docs/lenses.md`:55, 74, 143, 181
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:10, 33
- `docs/restyle-repoint-log.md`:81

**TRACES — historical/record docs (49 files, 164 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (4 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (37 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (17 line-hits)
- `docs/audit/2026-07-12-minor-gate-walk.md` (1 line-hits)
- `docs/audit/2026-07-12-skill-creator-walk.md` (1 line-hits)
- `docs/audit/2026-07-16-2.3.0.md` (2 line-hits)
- `docs/audit/2026-07-16-batch-2p2p0.md` (1 line-hits)
- `docs/briefs/2026-07-10-row241-guardrails-brief.md` (1 line-hits)
- `docs/design-review/2026-07-16-2.3.0.md` (4 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (4 line-hits)
- `docs/design-review/2026-07-16-ratchet-kit.md` (1 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (3 line-hits)
- `docs/design/2026-07-17-node-growth-law.md` (2 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (1 line-hits)
- `docs/gate-audit/2026-07-18-habits-to-gates.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/prover/2026-07-10-row241-integration.md` (1 line-hits)
- `docs/prover/2026-07-10-row241-spec.md` (1 line-hits)
- `docs/prover/2026-07-11-row218-convergence-rule.md` (2 line-hits)
- `docs/prover/2026-07-12-row242-readme-stance.md` (1 line-hits)
- `docs/prover/2026-07-12-s38-inv115-inv116-and-architecture.md` (5 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (6 line-hits)
- `docs/prover/2026-07-12-s40-inv125-cross-surface-uniformity.md` (1 line-hits)
- `docs/prover/2026-07-12-s41-inv135-per-kind-layers-proofs.md` (1 line-hits)
- `docs/prover/2026-07-14-design-review.md` (3 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (8 line-hits)
- `docs/prover/2026-07-16-2.3.0-minor-gate.md` (2 line-hits)
- `docs/prover/2026-07-16-2p1p1-prepush.md` (3 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-16-inv157-third-net.md` (4 line-hits)
- `docs/prover/2026-07-16-inv172-inv173.md` (1 line-hits)
- `docs/prover/2026-07-18-release-2.8.0.md` (1 line-hits)
- `docs/prover/2026-07-18-row390-392-doc-rotation.md` (2 line-hits)
- `docs/prover/2026-07-18-rows384-387-gate-correctness.md` (2 line-hits)
- `docs/prover/2026-07-18-rows390-392-growth-law-residual.md` (2 line-hits)
- `docs/prover/2026-07-18-rows397-383-answer-first-no-dramatization.md` (1 line-hits)
- `docs/prover/2026-07-19.md` (3 line-hits)
- `docs/prover/2026-07-20-comms.md` (1 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-06-suite-budget-row.md` (6 line-hits)
- `docs/prover/architecture-prover-record.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (3 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (12 line-hits)
- `docs/skill-review/2026-07-18-inv237-wiring.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)

---

### Rule 31 — SPEC INV-183, INV-189

**Demands:** Agents talk on exactly two channels, inbox and published contract; a message must name the sender's own real blocked work.

**Size:** 6067 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** E-31, E-32, INV-112, INV-130, INV-153, INV-182, INV-183, INV-184, INV-185, INV-188, INV-189, INV-190, INV-191, INV-193, INV-194, INV-195, INV-196, INV-197, INV-225; script names guardrails/check-earned-message.py, guardrails/check-wrong-referral.py; literal phrase "rule 31".

**TRACES — test files (17):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_agent_card_gate.py` — test_inv184_index_row_carries_no_target, test_inv184_prose_no_longer_rides_row_387_as_target
- `tests/test_agent_channels.py` — test_agent_is_a_project_window, test_agent_message_is_a_proposal_until_ratified, test_agent_recognises_a_neighbours_zone_itself, test_an_unowned_concern_goes_to_the_pack, test_capability_taken_through_one_of_the_two_channels, test_card_and_scan_law, test_cardless_tree_is_flagged_beside_its_siblings, test_checker_reds_wrong_referral_passes_correct, test_contract_default_deny, test_data_never_travels_as_a_message, test_e31_index_and_ownership, test_e32_index_and_ownership, test_e33_index_and_ownership, test_earned_message_names_its_block, test_exactly_two_channels_in_the_spec, test_gate_declines_the_real_track_coach_deposit, test_gate_help_prescribes_the_format_the_readme_prescribes, test_gate_passes_a_fault_message_naming_what_it_lived, test_gate_passes_over_a_field_inside_a_fenced_block, test_gate_reads_a_deposit_that_is_not_markdown, test_gate_reads_a_relayed_owner_wish_as_owing_nothing, test_gate_reads_an_agent_marker_split_across_lines, test_gate_reads_the_owners_own_deposit_as_owing_nothing, test_gate_reads_the_source_marks_variants, test_gate_reds_a_blocked_field_that_only_points_elsewhere, test_gate_reds_a_message_naming_neither_birth, test_gate_reds_a_message_naming_no_blocked_work, test_gate_reds_the_real_corpus_format_carrying_no_body_source_field, test_gate_reports_an_agent_message_that_states_no_need_by, test_grain_boundary_names_its_three_marks, test_homeless_question_is_dropped, test_inv182_index_and_ownership, test_inv183_index_and_ownership, test_inv184_index_and_ownership, test_inv185_index_and_ownership, test_inv187_index_and_ownership, test_inv188_index_and_ownership, test_inv189_index_and_ownership, test_inv190_index_and_ownership, test_inv191_index_and_ownership, test_inv193_index_and_ownership, test_inv194_index_and_ownership, test_inv195_index_and_ownership, test_inv196_index_and_ownership, test_inv197_index_and_ownership, test_inv225_index_and_ownership, test_no_file_outside_any_tree_describes_any_agent, test_no_third_channel_exists, test_one_question_crosses_twice_then_goes_to_the_owner, test_pack_card_exists_and_names_its_five_fields, test_readme_and_the_gate_agree_on_the_sources_one_home, test_referral_travels_back_to_the_asker, test_t22_index_and_ownership, test_the_bound_cites_the_kin_it_copies, test_the_holding_is_itself_the_finding, test_the_real_deposit_names_no_blocked_work_and_the_spec_says_so, test_work_never_stalls_on_ownership, test_wrong_referral_is_named_the_finding, test_wrong_referral_law_stands, test_zones_may_overlap
- `tests/test_config_surface.py` — (module-level, no enclosing test_ function)
- `tests/test_deposit_description.py` — test_gate_is_presence_not_a_semantic_match, test_gate_reads_only_from_agent_inbox_files, test_gate_reds_a_deposit_referencing_a_bare_code, test_spec_states_the_law
- `tests/test_design_reviewer.py` — test_unanswered_held
- `tests/test_founding_set_version.py` — test_old_host_gets_unanswered_question_named
- `tests/test_guardrails.py` — test_inbox_only_push_carve_out_needs_no_record
- `tests/test_inbox_remote_arm.py` — test_remote_arm_in_all_prose_homes, test_spec_anchor_and_index
- `tests/test_local_inbox_deposit.py` — (module-level, no enclosing test_ function)
- `tests/test_mirror_autosync.py` — test_ci_arm_is_key_gated_and_skips_gracefully
- `tests/test_named_reference.py` — test_spec_carries_the_deferred_penned_run_and_fault_birth_wording, test_spec_states_the_earned_auto_deposit_law
- `tests/test_read_grant.py` — (module-level, no enclosing test_ function)
- `tests/test_request_classifier.py` — test_count_word_tracks_the_control_set, test_inv152_index_and_ownership, test_inv153_index_and_ownership, test_names_all_four_controls, test_the_count_agrees_across_its_homes, test_unification_clause_stands
- `tests/test_traceability.py` — test_feedback_never_lost_in_both_homes, test_targets_owned_by_open_rows
- `tests/test_traffic_transport.py` — test_spec_corrects_inv183_transport_sentence
- `tests/test_withdrawal_convergence.py` — test_communicator_rule_carries_the_bound, test_formal_index_row, test_spec_clause_stands, test_spec_states_the_bound_and_its_kin

**TRACES — guardrail scripts (8):**
- `guardrails/README.md`
- `guardrails/check-agent-card.py`
- `guardrails/check-config-surface.py`
- `guardrails/check-deposit-description.py`
- `guardrails/check-earned-message.py`
- `guardrails/check-prover-record.sh`
- `guardrails/check-wrong-referral.py`
- `guardrails/route_agent_transport.py`

**TRACES — pipeline scripts/hooks (4):**
- `scripts/founding-questions.json`
- `scripts/read-grant-ask.md`
- `scripts/read-grant.py`
- `scripts/stranger-wish-monitor.py`

**TRACES — other skill files (3):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/SKILL.md`
- `skills/design-reviewer/SKILL.md`

**TRACES — root documents (4 files, 181 lines):**
- `ARCHITECTURE.md`:64, 65, 66, 87, 91, 100, 145, 209, 268, 291, 380, 677, 730, 731
- `PRODUCT_SPEC.md`:417, 418, 1410, 1415, 1423, 1424, 1679, 2223, 3106, 3221, 4415, 4427, 4428, 4432, 4436, 4437, 4451, 4452, 4453, 4457, 4470, 4485, 4497, 4505, 4525, 4548, 4549, 4550, 4554, 4555, 4556, 4557, 4561, 4562, 4566, 4567, 4571, 4590, 4594, 4595, 4596, 4607, 4615, 4616, 4620, 4635, 4639, 4643, 4644, 4645, 4649, 4653, 4657, 4661, 4662, 4670, 4674, 4693, 4694, 4695, 4699, 4703, 4705, 4709, 4712, 4716, 4718, 4719, 4737, 4738, 4742, 4743, 4759, 4765, 4770, 4775, 4779, 6004, 6005, 6019, 6020, 6021, 6035, 6119, 7900, 7901, 8016, 8034, 8057, 8086, 8087, 8088, 8089, 8092, 8093, 8094, 8095, 8097, 8098, 8099, 8100, 8101, 8129
- `ROADMAP.md`:107, 114, 116, 117, 118, 128, 132, 212, 215, 246
- `TEST_MATRIX.md`:180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 195, 196, 197, 235, 236, 238, 249, 335, 336, 337, 435, 492, 508, 509, 510, 517, 518, 526, 527, 602, 614, 618, 866, 867, 982, 1000, 1023, 1052, 1053, 1054, 1055, 1058, 1059, 1060, 1061, 1063, 1064, 1065, 1066, 1067, 1095

**TRACES — living docs (4 files, 5 lines):**
- `docs/lenses.md`:126
- `docs/migration-sample/2026-07-20-backdescribe-sample.md`:8, 33
- `docs/restyle-repoint-log.md`:84
- `docs/spec-compaction-protocol.md`:33

**TRACES — historical/record docs (49 files, 388 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (10 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (102 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (34 line-hits)
- `docs/audit/2026-07-12-composition-walk.md` (14 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (3 line-hits)
- `docs/design-review/2026-07-15-1.7.0.md` (1 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (2 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (1 line-hits)
- `docs/design-review/2026-07-19.md` (7 line-hits)
- `docs/design/2026-07-27-configuration-surface-seam.md` (1 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (2 line-hits)
- `docs/prover/2026-07-12-composition-fixes-fold.md` (2 line-hits)
- `docs/prover/2026-07-12-full-pass-pre-1.1.0.md` (18 line-hits)
- `docs/prover/2026-07-12-row247-inbox-remote-arm.md` (2 line-hits)
- `docs/prover/2026-07-12-s40-inv130-withdrawal-convergence.md` (4 line-hits)
- `docs/prover/2026-07-14-design-review.md` (3 line-hits)
- `docs/prover/2026-07-14-monitor-schedule.md` (1 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (4 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (2 line-hits)
- `docs/prover/2026-07-15-inv154-fixed-point-loop.md` (3 line-hits)
- `docs/prover/2026-07-15-minor-gate-1.5.0.md` (5 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-16-inv174-inv175.md` (3 line-hits)
- `docs/prover/2026-07-17-agent-communication.md` (27 line-hits)
- `docs/prover/2026-07-17-lanes-and-self-declaration.md` (11 line-hits)
- `docs/prover/2026-07-18-batch5-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-18-row-396-transport-split.md` (11 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (1 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (2 line-hits)
- `docs/prover/2026-07-18-rows-393-405-389.md` (3 line-hits)
- `docs/prover/2026-07-18-rows380-388-reach-config-wrong-referral.md` (8 line-hits)
- `docs/prover/2026-07-18-rows384-387-gate-correctness.md` (3 line-hits)
- `docs/prover/2026-07-18-rows397-383-answer-first-no-dramatization.md` (1 line-hits)
- `docs/prover/2026-07-19.md` (26 line-hits)
- `docs/prover/2026-07-20-3.0.0-backdescribe.md` (3 line-hits)
- `docs/prover/2026-07-20-comms.md` (11 line-hits)
- `docs/prover/2026-07-21-inv249-inbox-deposit-protocol.md` (4 line-hits)
- `docs/prover/2026-07-23-row445-4.0.0-fix-verify.md` (3 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-16-rows367-368.txt` (2 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (3 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (4 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (22 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (5 line-hits)
- `docs/research/2026-07-17-agent-routing-prior-art.md` (4 line-hits)
- `docs/skill-review/2026-07-18-live-spec-base-wrong-referral.md` (3 line-hits)
- `docs/skill-review/2026-07-21-feedback-intake-draft-sweep.md` (1 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)

---

### Rule 32 — SPEC INV-217

**Demands:** A release's patch/minor/major number is judged by what taking it costs a host, a stated call the session makes.

**Size:** 2205 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-141, INV-217, INV-91; literal phrase "rule 32".

**TRACES — test files (12):**
- `tests/fixtures/specformat/good_corpus_section.md` — (module-level, no enclosing test_ function)
- `tests/test_catchup_walk.py` — test_before_after_inventory_and_restore, test_catchup_walk
- `tests/test_description_field.py` — (module-level, no enclosing test_ function)
- `tests/test_design_reviewer.py` — test_architecture_node_and_seams, test_cross_sibling_routing_split, test_formal_index_rows, test_matrix_rows_cite_the_node, test_spec_clauses_stand
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_founding_set_version.py` — test_versionless_host_is_told_the_set_is_versioned
- `tests/test_gesture_overlay_parity.py` — (module-level, no enclosing test_ function)
- `tests/test_milestone_enumerates_design_review.py` — test_m1_list_names_the_design_review
- `tests/test_prover_doc_homes.py` — test_boundary_homed_in_when_not_to_use, test_description_carries_only_the_trigger
- `tests/test_release_tier_rule.py` — test_architecture_owns_the_invariant, test_base_rulebook_states_the_release_tier_rule, test_build_pipeline_release_step_points_to_the_rule, test_formal_index_row, test_matrix_row_covers_the_law, test_spec_states_the_law
- `tests/test_review_record_class.py` — test_names_every_member
- `tests/test_second_sibling_intake.py` — test_spec_scopes_the_stand_down

**TRACES — guardrail scripts (3):**
- `guardrails/check-description-field.py`
- `guardrails/doc-bounds.json`
- `guardrails/language-rules.json`

**TRACES — pipeline scripts/hooks (3):**
- `scripts/check-pack-update.sh`
- `scripts/spec-freeze.json`
- `scripts/spec-freeze.py`

**TRACES — other skill files (5):**
- `skills/build-pipeline/SKILL.md`
- `skills/build-pipeline/references/minor-bump-gate.md`
- `skills/design-reviewer/SKILL.md`
- `skills/product-prover/SKILL.md`
- `skills/text-audit/references/human-prose-rules.md`

**TRACES — root documents (4 files, 54 lines):**
- `ARCHITECTURE.md`:63, 86, 244, 588, 658, 902
- `PRODUCT_SPEC.md`:1396, 1512, 1513, 1517, 1518, 1522, 1523, 1538, 1559, 1649, 1673, 1678, 1698, 1703, 2606, 2983, 3029, 4157, 4158, 4159, 4414, 4491, 5154, 5170, 6299, 6579, 6580, 6581, 6582, 6587, 6588, 6589, 7995, 8045, 8121
- `ROADMAP.md`:128
- `TEST_MATRIX.md`:176, 193, 340, 341, 484, 617, 764, 767, 768, 961, 1011, 1087

**TRACES — living docs (3 files, 4 lines):**
- `docs/language-rules.md`:300, 821
- `docs/restyle-repoint-log.md`:88
- `docs/spec-compaction-protocol.md`:42

**TRACES — historical/record docs (59 files, 180 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (6 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (32 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (9 line-hits)
- `docs/audit/2026-07-16-batch-2p1p0.md` (2 line-hits)
- `docs/audit/2026-07-16-batch-2p2p0.md` (1 line-hits)
- `docs/audit/2026-07-16-prover-fable.md` (2 line-hits)
- `docs/design-review/2026-07-14-cross-host-coordinator.md` (1 line-hits)
- `docs/design-review/2026-07-14-property-routing.md` (2 line-hits)
- `docs/design-review/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/design-review/2026-07-14.md` (4 line-hits)
- `docs/design-review/2026-07-15-1.7.0.md` (2 line-hits)
- `docs/design-review/2026-07-15-1.8.0.md` (2 line-hits)
- `docs/design-review/2026-07-15.md` (8 line-hits)
- `docs/design-review/2026-07-16-full-2p1p0.md` (2 line-hits)
- `docs/design-review/2026-07-17-2.4.0.md` (3 line-hits)
- `docs/design-review/2026-07-17-2.5.0.md` (2 line-hits)
- `docs/handovers/2026-07-27-row496-document-blocks.md` (1 line-hits)
- `docs/language-reads/2026-07-29-read19-text-audit-skill.md` (1 line-hits)
- `docs/prover/2026-07-10-row221.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (1 line-hits)
- `docs/prover/2026-07-14-design-review.md` (10 line-hits)
- `docs/prover/2026-07-14-property-routing.md` (1 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (1 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (1 line-hits)
- `docs/prover/2026-07-15-1.7.0-minor-gate.md` (5 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (1 line-hits)
- `docs/prover/2026-07-15-322-forward-binding-and-323-review-record-class.md` (2 line-hits)
- `docs/prover/2026-07-15-332-inv163-audit.md` (1 line-hits)
- `docs/prover/2026-07-15-inv154-fixed-point-loop.md` (4 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (2 line-hits)
- `docs/prover/2026-07-15-minor-gate-1.5.0.md` (4 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-16-full-2p2p0.md` (2 line-hits)
- `docs/prover/2026-07-16-inv169.md` (3 line-hits)
- `docs/prover/2026-07-16-inv181-featurefit.md` (1 line-hits)
- `docs/prover/2026-07-16-prover-doc-restructure.md` (1 line-hits)
- `docs/prover/2026-07-18-2.8.1-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-18-batch4-push-recheck.md` (3 line-hits)
- `docs/prover/2026-07-18-release-2.7.0.md` (3 line-hits)
- `docs/prover/2026-07-18-release-2.8.0.md` (1 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (2 line-hits)
- `docs/prover/2026-07-18-row407-release-tier-rule.md` (12 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-19-2.8.2-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-19.md` (3 line-hits)
- `docs/prover/2026-07-20-3.0.0-backdescribe.md` (1 line-hits)
- `docs/prover/2026-07-20-comms.md` (2 line-hits)
- `docs/prover/2026-07-20.md` (1 line-hits)
- `docs/prover/2026-07-21-axes-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/architecture-prover-record.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (1 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (6 line-hits)
- `docs/skill-review/2026-07-17-live-spec-base-build-pipeline.md` (1 line-hits)
- `docs/skill-review/2026-07-18-live-spec-base-build-pipeline.md` (9 line-hits)
- `docs/skill-review/2026-07-18-product-prover.md` (1 line-hits)

---

### Rule 33 — SPEC INV-237

**Demands:** The seat that authored a change never supplies that change's own adversarial certification; a fresh, differently-contexted seat runs it.

**Size:** 1445 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-116, INV-237, INV-46; literal phrase "rule 33".

**TRACES — test files (9):**
- `tests/test_architecture_prove_seam.py` — (module-level, no enclosing test_ function)
- `tests/test_architecture_proved_at_full_pass.py` — test_spec_anchor_and_index
- `tests/test_clean_context_review.py` — test_architecture_owns_the_invariant, test_base_rule_33_states_it, test_build_pipeline_wires_verify_station, test_formal_index_row, test_matrix_row_covers_the_law, test_product_prover_wires_self_application, test_spec_states_the_law
- `tests/test_expensive_decision_read.py` — test_road_states_owned_pieces
- `tests/test_guardrails.py` — test_stale_when_architecture_changed_after_record
- `tests/test_periodic_full_audit.py` — test_audit_is_defined_adversarial_by_nature_once
- `tests/test_register_judge.py` — test_bare_code_lead_reds_under_the_judge, test_trailing_anchor_sentence_passes_the_judge
- `tests/test_review_record_class.py` — test_names_every_member
- `tests/test_traceability.py` — test_adversarial_verify_option, test_rule5_states_the_settled_delegation_rule

**TRACES — guardrail scripts (4):**
- `guardrails/check-earned-message.py`
- `guardrails/check-handover-provenance.py`
- `guardrails/check-prover-record.sh`
- `guardrails/language-rules.json`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (2):**
- `skills/build-pipeline/SKILL.md`
- `skills/product-prover/SKILL.md`

**TRACES — root documents (4 files, 42 lines):**
- `ARCHITECTURE.md`:145, 152, 181, 182, 631, 899
- `PRODUCT_SPEC.md`:1657, 2542, 2982, 3029, 3034, 3215, 5123, 5124, 5128, 5131, 5152, 5169, 5170, 5174, 5175, 5276, 5277, 5778, 7378, 7477, 7492, 7950, 8020, 8141
- `ROADMAP.md`:85
- `TEST_MATRIX.md`:176, 280, 331, 340, 341, 594, 662, 770, 916, 986, 1107

**TRACES — living docs (3 files, 4 lines):**
- `docs/language-rule-coverage.md`:357
- `docs/lenses.md`:27, 148
- `docs/worker-liveness.md`:44

**TRACES — historical/record docs (93 files, 276 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (4 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (18 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (7 line-hits)
- `docs/audit/2026-07-15-1.8.0-audit.md` (1 line-hits)
- `docs/design-review/2026-07-15.md` (1 line-hits)
- `docs/design/2026-07-18-clean-context-review-rule.md` (1 line-hits)
- `docs/design/2026-07-19-reminder-dependent-capability-audit.md` (1 line-hits)
- `docs/design/2026-07-20-conduct-audit-stories-2-3-spec-delta.md` (5 line-hits)
- `docs/prover/2026-07-06-pushgate-s22-5.md` (2 line-hits)
- `docs/prover/2026-07-06-rows110-114-115.md` (1 line-hits)
- `docs/prover/2026-07-07-humanize-who-decides.md` (1 line-hits)
- `docs/prover/2026-07-07-row56.md` (2 line-hits)
- `docs/prover/2026-07-07-rows111-113.md` (1 line-hits)
- `docs/prover/2026-07-10-night-full-reprove.md` (2 line-hits)
- `docs/prover/2026-07-12-row279-adopt-impersonal-voice.md` (2 line-hits)
- `docs/prover/2026-07-12-s38-batch-inv117-120.md` (5 line-hits)
- `docs/prover/2026-07-12-s38-inv115-inv116-and-architecture.md` (15 line-hits)
- `docs/prover/2026-07-12-s39-backlog-batch.md` (2 line-hits)
- `docs/prover/2026-07-12-s40-inv46-audit-trigger-broadened.md` (7 line-hits)
- `docs/prover/2026-07-12-s41-crosscut-counter-architecture.md` (1 line-hits)
- `docs/prover/2026-07-13-minor-gate-audit.md` (1 line-hits)
- `docs/prover/2026-07-13-prover-overlap-lens.md` (1 line-hits)
- `docs/prover/2026-07-13-prover-self-review.md` (1 line-hits)
- `docs/prover/2026-07-13-row298-design-principles.md` (1 line-hits)
- `docs/prover/2026-07-14-brief-time-disjointness.md` (2 line-hits)
- `docs/prover/2026-07-14-cleanup-movement.md` (3 line-hits)
- `docs/prover/2026-07-14-cross-host-coordinator.md` (2 line-hits)
- `docs/prover/2026-07-14-design-review.md` (1 line-hits)
- `docs/prover/2026-07-14-monitor-schedule.md` (2 line-hits)
- `docs/prover/2026-07-14-property-routing.md` (3 line-hits)
- `docs/prover/2026-07-14-request-classifier.md` (2 line-hits)
- `docs/prover/2026-07-14-stranger-door.md` (2 line-hits)
- `docs/prover/2026-07-15-2.0-movement.md` (2 line-hits)
- `docs/prover/2026-07-15-322-forward-binding-and-323-review-record-class.md` (7 line-hits)
- `docs/prover/2026-07-15-inv155-flaky-test.md` (3 line-hits)
- `docs/prover/2026-07-17-row419-skill-review-gate.md` (2 line-hits)
- `docs/prover/2026-07-18-2.8.1-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-18-release-2.8.0.md` (12 line-hits)
- `docs/prover/2026-07-18-row395-expensive-decision.md` (4 line-hits)
- `docs/prover/2026-07-18-rows-370-394.md` (1 line-hits)
- `docs/prover/2026-07-19-2.8.2-push-recheck.md` (2 line-hits)
- `docs/prover/2026-07-20-3.0.0-backdescribe.md` (2 line-hits)
- `docs/prover/2026-07-20-axes-from-kind.md` (2 line-hits)
- `docs/prover/2026-07-20-conduct-judge.md` (20 line-hits)
- `docs/prover/2026-07-20-conduct-stories-2-3.md` (2 line-hits)
- `docs/prover/2026-07-20.md` (1 line-hits)
- `docs/prover/2026-07-21-axes-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-21-integration-recheck.md` (1 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (1 line-hits)
- `docs/prover/2026-07-21-inv248-delivery-separability.md` (3 line-hits)
- `docs/prover/2026-07-21-inv249-inbox-deposit-protocol.md` (2 line-hits)
- `docs/prover/2026-07-22-row445-4.0.0-full-audit.md` (1 line-hits)
- `docs/prover/2026-07-23-row445-4.0.0-fix-verify.md` (2 line-hits)
- `docs/prover/2026-07-23-row477-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-23-row480-minor-gate.md` (1 line-hits)
- `docs/prover/2026-07-24-row456.md` (1 line-hits)
- `docs/prover/2026-07-27-evening-movement.md` (1 line-hits)
- `docs/prover/2026-07-27-language-gate-reach.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate-addendum.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate-fold.md` (1 line-hits)
- `docs/prover/2026-07-27-push-gate.md` (1 line-hits)
- `docs/prover/2026-07-27-row494-rendered-sweep.md` (1 line-hits)
- `docs/prover/2026-07-28-language-rule-home.md` (2 line-hits)
- `docs/prover/2026-07-28-requirement-302-findings-ratchet.md` (1 line-hits)
- `docs/prover/2026-07-29-night-landings-push-recheck.md` (1 line-hits)
- `docs/prover/2026-07-29-ratchet-arm-and-extract-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-night-campaign-push-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/prover/2026-08-05-public-edition-and-reader-repairs.md` (1 line-hits)
- `docs/prover/2026-08-05-readability-day-spec-recheck.md` (1 line-hits)
- `docs/prover/2026-08-06-budget-never-bend-recheck.md` (8 line-hits)
- `docs/prover/2026-08-06-spec-table-regeneration.md` (3 line-hits)
- `docs/prover/2026-08-06-suite-budget-row.md` (1 line-hits)
- `docs/prover/2026-08-06-work-board.md` (2 line-hits)
- `docs/prover/2026-08-07-night-order-adversarial.md` (1 line-hits)
- `docs/prover/architecture-prover-record.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (10 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (23 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (2 line-hits)
- `docs/research/2026-07-10-originality-audit.md` (1 line-hits)
- `docs/skill-review/2026-07-18-inv237-wiring.md` (13 line-hits)
- `docs/skill-review/2026-07-18-product-prover.md` (1 line-hits)
- `docs/skill-review/2026-07-20-spec-author-axes.md` (2 line-hits)
- `docs/skill-review/2026-07-21-live-spec-base-rule34.md` (2 line-hits)
- `docs/skill-review/2026-07-23-build-pipeline-row456.md` (1 line-hits)
- `docs/skill-review/2026-07-28-live-spec-base-rule35.md` (2 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-never-bend.md` (3 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (3 line-hits)
- `docs/skill-review/2026-08-07-live-spec-base.md` (1 line-hits)
- `docs/skill-review/2026-08-07-product-prover.md` (1 line-hits)

---

### Rule 34 — SPEC INV-247

**Demands:** Before a deferred item's work resumes, its technical premise is re-checked against the current shipped code, not the stale record.

**Size:** 1084 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-129, INV-247; literal phrase "rule 34".

**TRACES — test files (5):**
- `tests/test_deferred_revisit_cadence.py` — test_build_pipeline_carries_the_queue_take_rescan, test_formal_index_row, test_spec_clause_stands
- `tests/test_far_tier.py` — test_vocab_reds_a_deferred_row_carrying_no_trigger
- `tests/test_inbox_deposit_protocol.py` — (module-level, no enclosing test_ function)
- `tests/test_listener_tripwire.py` — test_matrix_row_covers_the_law
- `tests/test_resume_rederive.py` — test_inv247_base_rule_states_the_reread, test_inv247_distinct_from_queue_take_rescan, test_inv247_formal_index_row, test_inv247_spec_clause_stands

**TRACES — guardrail scripts (2):**
- `guardrails/check-far-tier.py`
- `guardrails/check-listener-tripwire.py`

**TRACES — pipeline scripts/hooks (0):**
- none found

**TRACES — other skill files (2):**
- `skills/build-pipeline/SKILL.md`
- `skills/communicator/references/field-examples.md`

**TRACES — root documents (4 files, 27 lines):**
- `ARCHITECTURE.md`:145, 146, 174, 175
- `PRODUCT_SPEC.md`:2167, 2168, 2182, 2183, 2187, 2201, 2222, 2227, 2916, 4466, 4679, 6941, 8033, 8151
- `ROADMAP.md`:123
- `TEST_MATRIX.md`:201, 326, 327, 338, 508, 606, 999, 1117

**TRACES — living docs (1 files, 2 lines):**
- `docs/restyle-repoint-log.md`:115, 116

**TRACES — historical/record docs (18 files, 64 line-hits, path + count only):**
- `docs/attic/2026-07-22-pre-format/ARCHITECTURE.md` (1 line-hits)
- `docs/attic/2026-07-22-pre-format/PRODUCT_SPEC.md` (12 line-hits)
- `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (5 line-hits)
- `docs/prover/2026-07-12-s40-inv129-deferred-revisit-cadence.md` (4 line-hits)
- `docs/prover/2026-07-16-full-2p1p0.md` (1 line-hits)
- `docs/prover/2026-07-18-row-396-transport-split.md` (1 line-hits)
- `docs/prover/2026-07-18-rows-393-405-389.md` (1 line-hits)
- `docs/prover/2026-07-18-rows382-403-far-tier.md` (5 line-hits)
- `docs/prover/2026-07-21-inv247-resume-rederive.md` (15 line-hits)
- `docs/prover/2026-07-21-inv249-inbox-deposit-protocol.md` (2 line-hits)
- `docs/prover/2026-07-23-row480.md` (1 line-hits)
- `docs/prover/red-proof-2026-07-18-row395.txt` (2 line-hits)
- `docs/queue-archive/JOURNAL-archive-2026-07-29.md` (2 line-hits)
- `docs/queue-archive/rotated-ROADMAP-2026-07.md` (4 line-hits)
- `docs/queue-archive/status-notes-ROADMAP-2026-07-23.md` (1 line-hits)
- `docs/skill-review/2026-07-21-build-pipeline.md` (1 line-hits)
- `docs/skill-review/2026-07-21-feedback-intake-draft-sweep.md` (1 line-hits)
- `docs/skill-review/2026-07-21-live-spec-base-rule34.md` (5 line-hits)

---

### Rule 35 — SPEC INV-302

**Demands:** A fresh agent, never the session that lived it, reads and writes both ends of a session's record, from a transcript extract.

**Size:** 1815 bytes of rule text in `skills/live-spec-base/SKILL.md`.

**Search identifiers used:** INV-302; script names guardrails/check-handover-provenance.py, scripts/session-extract.py; literal phrase "rule 35".

**TRACES — test files (3):**
- `tests/test_handover_provenance.py` — (module-level, no enclosing test_ function)
- `tests/test_opening_decision_sweep.py` — (module-level, no enclosing test_ function)
- `tests/test_session_extract.py` — (module-level, no enclosing test_ function)

**TRACES — guardrail scripts (2):**
- `guardrails/README.md`
- `guardrails/check-handover-provenance.py`

**TRACES — pipeline scripts/hooks (1):**
- `scripts/session-extract.py`

**TRACES — other skill files (0):**
- none found

**TRACES — root documents (4 files, 55 lines):**
- `ARCHITECTURE.md`:69, 89, 466, 467, 468
- `PRODUCT_SPEC.md`:2880, 2881, 2882, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2893, 2894, 2895, 2896, 2897, 2898, 2899, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 8206
- `ROADMAP.md`:198, 226, 227, 234
- `TEST_MATRIX.md`:199, 200, 201, 202, 203, 204, 1172

**TRACES — living docs (0 files, 0 lines):**
- none found

**TRACES — historical/record docs (16 files, 59 line-hits, path + count only):**
- `docs/briefs/2026-07-28-session-reading-process-brief.md` (1 line-hits)
- `docs/briefs/2026-07-29-the-extract-names-its-session-brief.md` (9 line-hits)
- `docs/briefs/2026-07-29-the-ratchet-arm-holds-on-a-real-push-brief.md` (1 line-hits)
- `docs/handovers/2026-07-29-176e927f-4e67-4fa6-887e-86d1d6e5d1e4-handover.md` (2 line-hits)
- `docs/handovers/2026-08-06-adoption-movement-handover.md` (1 line-hits)
- `docs/handovers/2026-08-06-evening-work-board-handover.md` (1 line-hits)
- `docs/prover/2026-07-28-session-record-read.md` (4 line-hits)
- `docs/prover/2026-07-29-night-landings-push-recheck.md` (17 line-hits)
- `docs/prover/2026-07-29-ratchet-arm-and-extract-recheck.md` (10 line-hits)
- `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` (1 line-hits)
- `docs/prover/2026-08-05-pin-repoint-check.md` (1 line-hits)
- `docs/push-review/2026-08-05-day-of-readability-repairs.md` (1 line-hits)
- `docs/push-review/2026-08-06-three-landings-and-the-edition-measured.md` (1 line-hits)
- `docs/skill-review/2026-07-28-live-spec-base-rule35.md` (5 line-hits)
- `docs/skill-review/2026-08-05-live-spec-base-readability.md` (2 line-hits)
- `docs/skill-review/2026-08-06-live-spec-base.md` (2 line-hits)

---

## Totals

- Rules covered: 35 (base rules 1-35, the whole body of `skills/live-spec-base/SKILL.md`).
- Total bytes of rule text: 48387 bytes (sum of the 35 per-rule byte counts above).
- Total distinct test files touched (union across all 35 rules): 123.
- Total distinct guardrail scripts touched: 39.
- Total distinct pipeline scripts/hooks touched: 21.
- Total distinct other-skill files touched: 20.
- Total distinct root-document files touched: 4 (of 4); total root-document line-hits summed across rules: 1699.
- Total distinct living-doc files touched: 24; total living-doc line-hits summed across rules: 160.
- Total distinct historical/record-doc files touched: 416; total historical-doc line-hits summed across rules: 5509.
- Total document lines touched (root + living + historical line-hits, summed across all 35 rules, a rule counted once per line it hits): 7368.

