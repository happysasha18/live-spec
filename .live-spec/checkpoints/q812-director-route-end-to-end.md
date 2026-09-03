# The Director's real route is proven end to end, on the actual mechanism
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

A worker is live in this row's own lane, briefed with the decision sheet below verbatim plus
`PLAN.md` q-812's own body, `spec/message-first-read.md` R313/R314, `spec/wish-intake.md` R4,
`evals/director/README.md`, and `tests/test_status_view_install.py` as its fixture pattern.

- **Worker id (Agent-tool subagent):** `a7b13b8d7f9ca3103` — resume by sending it a message with
  this id/name if this session's own memory is wiped before it reports.
- **Briefed write-set (this lane's own worktree only):** `.claude/worktrees/lane-q-812-director-route-end-to-end/`
  — branch `lane/q-812-director-route-end-to-end`, cut from commit `09bbd39a`. The worker was told
  explicitly not to touch the primary tree or any other worktree, and not to run
  `scripts/land-lane.sh` itself (the orchestrator integrates).
- **Started:** 2026-09-03 ~11:47. Given the scope (four internal phases: product-prover pass,
  test-author derivation, the scripted mechanical harness, one new eval scenario), expect 45-90
  minutes based on tonight's comparable q-813/q-804 runtimes.
- **Liveness check for a resuming session (rule 6):** `ls -la .claude/worktrees/lane-q-812-director-route-end-to-end`
  (file mtimes moving = alive), `git -C .claude/worktrees/lane-q-812-director-route-end-to-end log --oneline -3`
  (new commits = it landed something), and a message to worker id `a7b13b8d7f9ca3103` asking for
  status — never assume it died from the process list alone, and never spawn a second worker on
  this same lane before checking.

## NEXT

(nothing yet)

## DECISION SHEET

Goal: prove, on a scripted deterministic scratch-host harness (no new production machinery), the full task lifecycle already promised by spec/message-first-read.md Requirement 313 (the seven-act first read) and Requirement 314 (decision sheet in one checkpoint) plus spec/wish-intake.md Requirement 4 (row never deleted, closed only with a named exit, reopened on a failing acceptance) -- his own verbatim brief in PLAN.md q-812's own body is the primary source, six numbered DOD clauses plus two named hard cases. Outcome: a reproducible, deterministic test proves (1) an instruction produces exactly one PLAN.md row plus one checkpoint with a real decision sheet; (2) a question/halt produces neither; (3) a task cannot STAY marked done without its DOD/check passing -- this already exists reactively via Req 4 criteria 10/13 (a false done reopens to 1F604 on the next probe run), so the proof is: mark a row done with a failing check, assert the probe reads it reopened, not truly closed; (4) a correction to work already running updates the SAME checkpoint (not a new one) -- extend/verify against existing evals/director/ correction-*.json scenarios, adding a mechanical-level assertion (same checkpoint file, not a second one) if the existing scenarios only prove the classification layer and not the checkpoint-identity guarantee; (5) an idea-shaping turn ('davay nakidyvat idei', multiple loose ideas in one turn) produces no task per idea voiced, only the real ones decided after settling -- this is classification-layer and belongs as ONE NEW scenario+trace in the EXISTING evals/director/scenarios.json harness, following its own established methodology (fresh producer per scenario, opaque label, independent grading, never shown the expected verdict) -- do not build a second harness for this; (6) a fresh session reading existing PLAN.md+checkpoint state (state-probe.sh's own NEXT line plus the checkpoint's own NEXT section) unambiguously identifies the SAME next action, never a duplicate and never an arbitrary different row -- prove this by asserting the DATA (PLAN.md mark + checkpoint NEXT field) deterministically constrains the answer to one row, which is testable without a live LLM call, rather than repeating the one-off manual live-session demo q-806 already did. Dimensions: architecture (this is proving an existing, already-specced mechanism -- likely NO new spec requirement needed, but confirm via a real product-prover pass rather than assuming), quality (test-author's own derivation discipline), method reliability (his own explicit anti-scope-creep instruction: no new hook, board server, event log, second plan, registry or status). Known: Req 313+314+wish-intake Req 4 already cover almost everything textually; the gap is PROOF, not specification -- but this must be CONFIRMED by an actual product-prover pass over these three requirements specifically checking coverage for the two named hard cases and the DOD-gated-close and resume-without-duplication guarantees, before writing any test, per his own explicit instruction ('Product-prover должен проверить сам продуктовый контракт этого маршрута'). If product-prover finds a real gap, spec-author authors the minimal delta -- if it finds none, say so plainly and cite the existing clauses rather than inventing new ones to look thorough. Unknown: exact shape of the scripted scratch-host harness (reuse the tests/test_status_view_install.py / tests/test_scaffold_install.py fixture pattern -- a temp git repo with a real PLAN.md, .live-spec/checkpoints/, and the real checkpoint.py/state-probe.sh/plan_checks.py copied in -- since that pattern already proves itself against three other installers tonight). Risk: none technical (fully reversible, additive tests only); the real risk is scope creep into building a NEW mechanism instead of proving the existing one -- his own instruction is explicit and repeated, treat any urge to add a hook/registry/status as a stop sign. Specialist: opus-tier worker, sequenced internally: (a) product-prover pass over Req 313/314/wish-intake Req 4 for this route's contract completeness, folding any real gap via spec-author before proceeding; (b) test-author derives the exact TEST_MATRIX rows this proof needs, no more; (c) build the scripted deterministic harness + the one new eval scenario; (d) full suite green. Evidence: the scripted harness's own red-then-green transcripts for each of the 6 numbered clauses; the new eval scenario's real fresh-producer run; TEST_MATRIX rows tracing to Req 313/314/Req 4's own clauses; full suite green, committed. Next: dispatch worker with this brief, PLAN.md q-812's own body verbatim, spec/message-first-read.md Requirement 313+314 whole, spec/wish-intake.md Requirement 4 whole, evals/director/README.md, and tests/test_status_view_install.py as the scratch-host fixture pattern to follow, as primary sources.
