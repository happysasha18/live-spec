# R3 — how often each rule actually fires

Root: Alexander's own mechanism, recorded in the 2026-08-09 handover under the work that runs without anyone's word — "Extend the runs-and-fires law from checks to rules, under his landed row 391" (`.live-spec/handover-2026-08-09.md:107`), and his law that a rule which never fires becomes a retirement candidate with the evidence in hand (`.live-spec/handover-2026-08-09.md:80-87`). The landed device is queue row 391, `docs/queue-archive/rotated-ROADMAP-2026-07.md:195`: every net records how often it RAN and how often it FIRED, zero runs reads as a broken trigger, many runs with zero fires surfaces the net for the human's word, and retirement is always his call.

This page carries the reading only. It changes no machine, adds no hook and retires no rule. The campaign's own rule 2 — no new check, rule or hook until the campaign closes, the exception his alone (`.live-spec/culling-plan-v3-2026-08-10.md:33`) — means the recording that is missing is written here as a decision row for him, at the end.

## How a check's fires are counted today

Three separate arrangements, and only the first counts anything on its own.

**The personal Stop-hook meter.** `~/.claude/hooks/hook-meter.py` wraps a hook, passes its input and output through untouched, and appends one JSON line per invocation to `~/.claude/hooks/hook-meter.jsonl`. A line reads `{"hook": "scissors-scan.py", "event": "Stop", "fired": true, "hits": 2}`. A fire is a block decision on the hook's own stdout. The log holds 22,800 lines today and covers eight hooks; `~/.claude/settings.json` wires those eight through the meter at lines 118, 128, 132, 140, 148, 156, 164 and 172. Three more wired hooks bypass it — `midturn-chat-scan.py` (line 92), `clock-hook.sh` (line 102) and `chat-law-hook.sh` (line 110) — so their runs and fires are counted nowhere.

The reading, run today (command C1):

| hook | runs | fires | reading |
|---|---:|---:|---|
| `register-judge-report.sh` | 3,446 | 195 | off since 2026-07-30 on his word; its last recorded fire sits at log line 16,950 of 22,800 |
| `scissors-scan.py` | 3,288 | 131 | live |
| `register-judge-collect.sh` | 3,227 | 0 | off since 2026-07-30 on his word; a run of the disabled script cannot fire |
| `answer-first-scan.py` | 3,204 | 0 | live and silent — a retirement candidate under row 391's own law |
| `hedge-scan.py` | 3,023 | 4 | live |
| `affirmation-scan.py` | 2,612 | 37 | live |
| `lean-orchestrator-scan.py` | 2,396 | 26 | live |
| `code-anchor-scan.py` | 1,604 | 20 | live |

The two disabled scripts carry the line `exit 0  # TEMPORARILY DISABLED 2026-07-30` at line 2 of each file, so every run since that date is an empty pass. The meter's records carry no timestamp, so a fire can be placed in the log's order but not on a date; the window is the meter's first day, 2026-07-17, to today.

**The pack-side shape, shipped and unwired.** `guardrails/net_meter.py` landed with row 391 and offers the same two faces, `--wrap` and `--report`, plus a roster so a net that never ran can still be named. Nothing in this repository wraps a net with it: no `.live-spec/net-meter.jsonl` exists, no roster file exists, and every reference to the module outside its own file sits in `tests/test_net_meter.py` and in records. So the pack's own thirty-one push gates count nothing (command C6).

**The hand search.** A gate's fires are established by reading `git log`, `JOURNAL.md`, `docs/PROGRESS.md` and the record folders for the gate blocking real work, which is what `.live-spec/day1-census-checks.md` did on 2026-08-08. Its result: 6 of 31 gates carry a dated catch — a (2026-07-20), h (2026-07-23), m (2026-07-20), s (2026-07-20), t (2026-07-27), ac (2026-08-05) — and 25 carry none (`.live-spec/day1-census-checks.md`, the Totals section). A red-proof fixture is never counted as a fire: `guardrails/gate-red-proofs.json` holds one for all 31 gates by construction of gate w, and `guardrails/hook-red-proofs.json` does the same for the hooks, which proves each machine CAN fire and says nothing about whether it did.

## What counts as a rule firing

A rule fires when a machine that carries it catches real work. Four machine kinds carry a rule here: a push gate in `guardrails/pre-push`, a suite check that reds inside gate b, a Stop hook on the chat surface, and a pre-show lint a session runs by hand. A test that pins the rule counts as proof that the machine can fire, and it stays outside the fire count, the same standing a red-proof fixture has.

A rule with no machine and no recorded fire is the evidence row the campaign wants: nothing enforces it, and nothing shows it was ever needed. That is not a verdict. Row 391's law reserves retirement for him.

## How each column is built

- **Rule** — the 35 shared rules from `.live-spec/day1-census-rules.md` (`skills/live-spec-base/SKILL.md` v4.3.0, lines 110-641) and the 53 working-skill rules from `.live-spec/r5-rule-prices-2026-08-11.md`. 88 in all, the count `NEXT_STEPS.md:26` states.
- **Enforcing machine** — a runnable script that (a) the rule's own text names by path, (b) declares in its first 4,000 bytes a SPEC code the rule's own text carries, or (c) states as its own purpose the demand the rule makes. The basis column says which of the three applies, so any row can be rejected on its own terms. Where a code is shared but the script's purpose is a different demand, the machine is left out and the rule reads none.
- **Recorded fires** — from the hook meter for a metered hook, from the six dated gate catches for a gate, and the words none on record everywhere else.
- **Regenerate** — the commands below, by number.

## Commands

```
C1  python3 ~/.claude/hooks/hook-meter.py --report
C2  # the machines a rule names, and the codes it carries, from the rule's own text
    sed -n '<line-range>p' <skill file>
C3  sed -n '/^## Table (31 gates/,/^## Totals/p' .live-spec/day1-census-checks.md
C4  grep -n 'TRACES — guardrail scripts' -A6 .live-spec/day1-census-rules.md
C5  # every script's declared codes, the map the machine column is built from
    for f in guardrails/check-* scripts/*.py scripts/*.sh hooks/*.py hooks/*.sh; do
      printf '%s :: ' "$f"; head -c 4000 "$f" | grep -oE '\b(INV|T|E|ACT|M|A)-[0-9]+\b' | sort -u | tr '\n' ' '; echo
    done
C6  ls .live-spec/net-meter.jsonl; grep -rn net_meter --include='*.py' --include='*.sh' --include='*.json' . | grep -v '^./.git/'
```

## The 35 shared rules

| # | what the rule demands | enforcing machine | basis | recorded fires | regenerate |
|---:|---|---|---|---|---|
| 1 | Ask the human only what only they can answer; never invent intent or offer a fork the artifacts already settle. | `guardrails/check-board.py` (gate q) | code INV-4 | none on record | C3, C5 |
| 2 | Human-facing text stands alone in plain product language; codes/jargon trail quietly, never open a sentence, never get loan-translated. | `hooks/code-anchor-scan.py` (Stop hook, metered) | the hook's own text names base rule 2 | 20 fires in 1,604 runs, window 2026-07-17 to 2026-08-11 | C1 |
| 3 | One thing keeps exactly one name everywhere, drawn from the host spec's own vocabulary. | `guardrails/check-one-name.py` (rides gate b) | purpose | none on record | C4, C5 |
| 4 | Every fact has one canonical home; every other mention is a pointer, kept live when the home moves. | `guardrails/check-pin-drift.sh` (gate g) | purpose | none on record | C3, C5 |
| 5 | The seat orchestrates and briefs; each unit of work routes to the cheapest tier that can pass it, logged. | `guardrails/check-tier-refusal.py` (rides gate b); `~/.claude/hooks/chat-law-hook.sh` (wired, unmetered) | purpose; code INV-69 | none on record | C2, C4, C5 |
| 6 | Long or delegated work keeps a disk checkpoint (done/in-progress/next) so a cutoff resumes cleanly; red is never committed. | none | - | none on record | C2, C4 |
| 7 | Before every write and commit, re-check git status/HEAD; parallel lanes, worktrees, and worker restores follow a strict collision-avoidance set. | `guardrails/pre-commit`; `guardrails/check-worker-restore.py`; `scripts/open-lane.sh` | code INV-11; named by the rule; named by the rule | none on record | C2, C5 |
| 8 | Re-read skill/pack/profile modification times at every breakpoint; journal the old-to-new change on any version bump. | `guardrails/check-config-health.sh` (gate m); `guardrails/check-skill-loadability.sh` (gate f); `scripts/sync-skills.sh` | purpose; code M-7; code A-7 | 1 fire, 2026-07-20 — ten installed skills sat at 2.8.1 against pack source 3.0.0 | C3, C5 |
| 9 | Dated reasons live in JOURNAL.md; SPEC/NEXT_STEPS/ROADMAP state only current truth; shipped docs update the same session. | `guardrails/check-no-history.py` (rides gate b) | purpose | none on record | C4, C5 |
| 10 | Nothing is silently deleted; a superseded file moves to the attic with a manifest line, and only regenerable junk is dropped, with approval. | `guardrails/check-doc-rotation.py` (gate t); `guardrails/check-deletion-only-push.sh`; `guardrails/check-rendered-sweep.py` | purpose; purpose; purpose | 1 fire, 2026-07-27 — seven archived rows whose status cells never followed their delivery reports | C3, C5 |
| 11 | "Works" is said only after running it and seeing the result; synthetic data always carries the label SYNTHETIC. | none | - | none on record | C2, C4 |
| 12 | Irreversible, authored-content, publishing, push-gated, and taste decisions go to the human; everything else proceeds and gets reported. | none | - | none on record | C2, C4 |
| 13 | Every factual claim traces to a primary source (file:line, commit, command output); a human-attributed decision needs a dated, checkable exchange. | `guardrails/check-authority-anchor.py` (gate r); `guardrails/check-touchpoint-kind.py` (gate p); `guardrails/check-release-note.py` | code INV-207; code INV-205; code INV-205 | none on record | C3, C5 |
| 14 | A found defect is one sample of a class; name the class, sweep every look-alike in the same change. | none | - | none on record | C2, C4 |
| 15 | Every request is classified by entry door (feature/bug/refactor/docs-only/skip) and work-kind before the first line of code. | `guardrails/check-delta-record.py` (rides gate b) | purpose | none on record | C4, C5 |
| 16 | A prototype stays fenced and labelled in prototype/, never wired into production; promotion re-enters through the spec step. | `guardrails/check-prototype-fence.sh` (gate e); `scripts/check-shipped-language.py` | code E-17, INV-17; code INV-17 | none on record | C3, C5 |
| 17 | Truly irreversible acts (spend, delete, unsendable send) always stop for the human's word; a repo push is not irreversible. | none | - | none on record | C2, C4 |
| 18 | A taken filename differentiates first by its home's own semantic mark, then by a numeric ordinal; never overwrite. | none | - | none on record | C2, C4 |
| 19 | Operational noise gets a WATCHED line on first sight; a repeat gets a named owner; an owned problem never blocks unrelated work. | none | - | none on record | C2, C4 |
| 20 | At setup or a repeated struggle, search installed skills and catalogs for a fit before building something new. | none | - | none on record | C2, C4 |
| 21 | Durable human-facing prose is drafted by a fresh, rule-free writer session from a brief, never written by the author directly. | none | - | none on record | C2, C4 |
| 22 | Name a concrete goal artifact up front; measure every iteration against that goal itself, never a proxy; lock gains by a mechanism. | none | - | none on record | C2, C4 |
| 23 | A behavioural rule that breaks mid-turn a second time earns a live channel: a prompt hook or a mechanical red check. | none | - | none on record | C2, C4 |
| 24 | The pipeline's stations are kind-abstract; each project kind fills them with its own concrete layers and proof kinds. | `guardrails/check-agent-card.py` (gate y); `guardrails/check-config-surface.py`; `guardrails/check-push-reach.sh` | code INV-135, INV-36; code INV-135; code INV-135 | none on record | C3, C5 |
| 25 | The lead's context holds only orchestration essentials; reads done to discover or understand are dispatched to a worker for distillation. | `hooks/lean-orchestrator-scan.py` (Stop hook, metered); `~/.claude/hooks/chat-law-hook.sh` (wired, unmetered) | the hook's own text names the lean-orchestrator law; code INV-137 | 26 fires in 2,396 runs, window 2026-07-17 to 2026-08-11 | C1, C2 |
| 26 | Beside its layers and proofs, a project kind names checkable design principles that the verify pass runs. | `scripts/preshow-legibility-lint.py`; `guardrails/check-config-surface.py` | code INV-136, INV-139; code INV-136 | none on record | C2, C5 |
| 27 | The seat decides mechanical steps, artifact-determined values, and sensible defaults; only genuine taste, trade-off, or correctness calls reach the human. | `guardrails/check-board.py` (gate q), the reaching half only | code INV-4 | none on record | C3, C5 |
| 28 | Beyond the continuous lints, a full adversarial whole-read audit of the living documents runs every ten landings. | none | - | none on record | C2, C4 |
| 29 | A parked, needs-the-human's-word item is re-tested for derivability every time it's touched; an unjustified marker defaults to the seat's own work. | `guardrails/check-deferral-marker.py` (rides gate b); `hooks/hedge-scan.py` (Stop hook, metered) | code INV-152, INV-155; the hook's own text names base rule 29 | 4 fires in 3,023 runs, window 2026-07-17 to 2026-08-11 | C1, C5 |
| 30 | Any property a machine can verify becomes a blocking gate run on every push, held by no one's attention. | `guardrails/check-tests.sh` (gate b); `guardrails/check-every-gate-can-fail.py` (gate w); `guardrails/check-hooks-can-fire.py` | code INV-164; purpose; purpose | none on record for gate w; gate b keeps no per-event record | C3, C5 |
| 31 | Agents talk on exactly two channels, inbox and published contract; a message must name the sender's own real blocked work. | `guardrails/check-earned-message.py` (gate n, report-only); `guardrails/check-wrong-referral.py`; `guardrails/check-deposit-description.py` | code INV-189, INV-193; code INV-196, INV-225; code INV-183, INV-189, INV-190 | none on record | C3, C5 |
| 32 | A release's patch/minor/major number is judged by what taking it costs a host, a stated call the session makes. | `guardrails/check-release-note.py`, the note half only | purpose | none on record | C4, C5 |
| 33 | The seat that authored a change never supplies that change's own adversarial certification; a fresh, differently-contexted seat runs it. | `guardrails/check-push-review.sh` (gate ac); `guardrails/check-prover-record.sh` (gate a) | purpose; code INV-116 | 1 fire, 2026-08-05 — eleven findings across 24 unpushed commits, every one repaired the same hour; gate a's catch of 2026-07-20 is counted on build-pipeline's prove step instead | C3, C5 |
| 34 | Before a deferred item's work resumes, its technical premise is re-checked against the current shipped code, not the stale record. | `guardrails/check-far-tier.py`; `guardrails/check-listener-tripwire.py` | code INV-129; code INV-129 | none on record | C4, C5 |
| 35 | A fresh agent, never the session that lived it, reads and writes both ends of a session's record, from a transcript extract. | `guardrails/check-handover-provenance.py` (gate ab); `scripts/session-extract.py` | purpose; code INV-302 and named by the rule | none on record | C3, C5 |

## The 53 rules inside the nine working skills

Ordered by price, the order `.live-spec/r5-rule-prices-2026-08-11.md` sets, so the most expensive rule with no machine sits at the top.

| # | skill | rule | home | enforcing machine | basis | recorded fires | regenerate |
|---:|---|---|---|---|---|---|---|
| 1 | build-pipeline | 8. Verify by deed | `skills/build-pipeline/SKILL.md:404-469` | `guardrails/check-worker-restore.py` (rides gate b) | named by the rule | none on record | C4, C5 |
| 2 | build-pipeline | 3. Architecture — write or update `ARCHITECTURE.md` from the proven spec | `skills/build-pipeline/SKILL.md:286-351` | `guardrails/check-pin-drift.sh` (gate g) | purpose | none on record | C3, C5 |
| 3 | build-pipeline | 9. Commit & show | `skills/build-pipeline/SKILL.md:471-499` | `guardrails/pre-push`, the whole gate chain, gate b first | purpose | none on record beyond the six gate catches listed in this page | C3, C5 |
| 4 | spec-author | 7. Terms | `skills/spec-author/SKILL.md:241-269` | `guardrails/check-one-name.py`; `guardrails/check-vocabulary.py` | purpose; purpose | none on record | C4, C5 |
| 5 | communicator | 6. Account for every removal of substance (SPEC INV-109) | `skills/communicator/SKILL.md:470-489` | none | - | none on record | C2, C4 |
| 6 | build-pipeline | 2. Prove — invoke `product-prover` | `skills/build-pipeline/SKILL.md:263-284` | `guardrails/check-prover-record.sh` (gate a) | purpose | 1 fire, 2026-07-20 — the v3.2.0 push blocked for a prover record covering the spec change | C3, C5 |
| 7 | build-pipeline | 1. Spec — invoke `spec-author` | `skills/build-pipeline/SKILL.md:243-261` | `guardrails/check-requirement-shape.py` (rides gate b) | purpose | none on record | C4, C5 |
| 8 | build-pipeline | 5. Test spec — invoke test-author to derive TEST_MATRIX.md from the proven spec | `skills/build-pipeline/SKILL.md:364-379` | `guardrails/check-matrix-reference.py` (gate d) | purpose | none on record | C3, C5 |
| 9 | text-audit | 5. Read again, and close on two clean rounds | `skills/text-audit/SKILL.md:168-187` | none | - | none on record | C2, C4 |
| 10 | build-pipeline | 7. Code — implement until green | `skills/build-pipeline/SKILL.md:385-402` | none | - | none on record | C2, C4 |
| 11 | text-audit | 3. The auditor merges the two lists | `skills/text-audit/SKILL.md:147-164` | none | - | none on record | C2, C4 |
| 12 | communicator | 4. Run the register lint — a hard BLOCK (SPEC INV-83) | `skills/communicator/SKILL.md:460-468` | `scripts/preshow-register-lint.py` | named by the rule, code INV-83 | none on record — the lint keeps no ledger | C2, C4 |
| 13 | spec-author | 1. Author / grow the relevant requirement | `skills/spec-author/SKILL.md:587-596` | `guardrails/check-index-generated.py` (gate x); `scripts/build-index.py` | purpose; named by the rule | none on record | C3, C5 |
| 14 | build-pipeline | 4. Prove the architecture — invoke `product-prover` with the architecture lens | `skills/build-pipeline/SKILL.md:353-362` | `guardrails/check-prover-record.sh` (gate a) | code INV-116, M-6 | none on record separate from the 2026-07-20 catch above | C3, C5 |
| 15 | test-author | 8. Close by the mechanical gates, not a hand-walked list | `skills/test-author/SKILL.md:58-67` | `guardrails/check-matrix-reference.py` (gate d); `scripts/build-matrix-reference.py` | named by the rule; named by the rule | none on record | C3, C5 |
| 16 | design-reviewer | 3. Every position behaves alike | `skills/design-reviewer/SKILL.md:202-212` | none | - | none on record | C2, C4 |
| 17 | design-reviewer | 1. Enumerate | `skills/design-reviewer/SKILL.md:129-136` | none | - | none on record | C2, C4 |
| 18 | communicator | 5. Legibility floor (a BLOCK, SPEC INV-139) | `skills/communicator/SKILL.md:469-469` | `scripts/preshow-legibility-lint.py` | named by the rule, code INV-139 | none on record — the lint keeps no ledger | C2, C4 |
| 19 | test-author | 7. A norm-pointered clause owes a norm-conformance row | `skills/test-author/SKILL.md:50-57` | none | - | none on record | C2, C4 |
| 20 | communicator | 3. Run the mechanical check | `skills/communicator/SKILL.md:455-459` | `scripts/preshow-lint.py` | named by the rule, code INV-28 | none on record — the lint keeps no ledger | C2, C4 |
| 21 | text-audit | 2. Hand the text to two fresh cold readers | `skills/text-audit/SKILL.md:140-146` | none | - | none on record | C2, C4 |
| 22 | design-reviewer | 4. Check parity | `skills/design-reviewer/SKILL.md:146-151` | none | - | none on record | C2, C4 |
| 23 | design-reviewer | 5. Fire the tight ask | `skills/design-reviewer/SKILL.md:153-159` | none | - | none on record | C2, C4 |
| 24 | design-reviewer | 2. Every object type behaves alike | `skills/design-reviewer/SKILL.md:197-201` | none | - | none on record | C2, C4 |
| 25 | design-reviewer | 1. Entry mirrors exit | `skills/design-reviewer/SKILL.md:193-196` | none | - | none on record | C2, C4 |
| 26 | test-author | 6. Matrix-local row ids are legal, spec anchors stay the parent | `skills/test-author/SKILL.md:46-49` | none | - | none on record | C2, C4 |
| 27 | test-author | 5. Name the state space before filling cells | `skills/test-author/SKILL.md:42-45` | none | - | none on record | C2, C4 |
| 28 | spec-author | 5. Invariants | `skills/spec-author/SKILL.md:236-239` | none | - | none on record | C2, C4 |
| 29 | text-audit | 1. Run the mechanical lints, and fix every hit | `skills/text-audit/SKILL.md:136-139` | none | - | none on record | C2, C4 |
| 30 | build-pipeline | 6. Test — with `test-author`, write tests that assert the REAL shipped artifact | `skills/build-pipeline/SKILL.md:381-383` | `scaffold/guardrails/check_tests_present.py` (gate h) | purpose | 1 fire, 2026-07-23 — the v4.0.1 push carried eleven skill files changed to the version stamp alone | C3, C5 |
| 31 | communicator | 2. Pass the draft phrase by phrase through one question | `skills/communicator/SKILL.md:451-454` | none | - | none on record | C2, C4 |
| 32 | communicator | 1. Re-read the rules above, and the full writing register | `skills/communicator/SKILL.md:448-450` | none | - | none on record | C2, C4 |
| 33 | spec-author | 5. Then walk the two layers to the tests | `skills/spec-author/SKILL.md:604-607` | none | - | none on record | C2, C4 |
| 34 | design-reviewer | 2. Describe by role | `skills/design-reviewer/SKILL.md:138-141` | none | - | none on record | C2, C4 |
| 35 | spec-author | 4. Hand off to `product-prover` on the whole spec — the delta included | `skills/spec-author/SKILL.md:601-603` | none | - | none on record | C2, C4 |
| 36 | text-audit | 4. Write each fix from the source | `skills/text-audit/SKILL.md:165-167` | none | - | none on record | C2, C4 |
| 37 | spec-author | 2. Ask, don't silently fill | `skills/spec-author/SKILL.md:597-599` | none | - | none on record | C2, C4 |
| 38 | spec-author | 5. The two closing sentences | `skills/spec-author/SKILL.md:329-331` | none | - | none on record | C2, C4 |
| 39 | spec-author | 2. Entities | `skills/spec-author/SKILL.md:230-231` | none | - | none on record | C2, C4 |
| 40 | test-author | 1. Open with the artifact inventory | `skills/test-author/SKILL.md:35-36` | none | - | none on record | C2, C4 |
| 41 | test-author | 3. Every row states BOTH sides | `skills/test-author/SKILL.md:39-40` | none | - | none on record | C2, C4 |
| 42 | spec-author | 3. States & transitions | `skills/spec-author/SKILL.md:232-233` | none | - | none on record | C2, C4 |
| 43 | design-reviewer | 3. Propose groups | `skills/design-reviewer/SKILL.md:143-144` | none | - | none on record | C2, C4 |
| 44 | test-author | 2. Blocks per architecture node; every spec fact ≥ 1 row | `skills/test-author/SKILL.md:37-38` | none | - | none on record | C2, C4 |
| 45 | spec-author | 4. Actors | `skills/spec-author/SKILL.md:234-235` | none | - | none on record | C2, C4 |
| 46 | spec-author | 3. The standard-facet sweep | `skills/spec-author/SKILL.md:327-327` | none | - | none on record | C2, C4 |
| 47 | spec-author | 1. Regression fences | `skills/spec-author/SKILL.md:325-325` | none | - | none on record | C2, C4 |
| 48 | spec-author | 2. The new behaviour itself | `skills/spec-author/SKILL.md:326-326` | none | - | none on record | C2, C4 |
| 49 | test-author | 4. Every row pins a LEVEL | `skills/test-author/SKILL.md:41-41` | none | - | none on record | C2, C4 |
| 50 | spec-author | 4. The fit walk | `skills/spec-author/SKILL.md:328-328` | none | - | none on record | C2, C4 |
| 51 | spec-author | 6. Cross-section composition | `skills/spec-author/SKILL.md:240-240` | none | - | none on record | C2, C4 |
| 52 | spec-author | 1. Purpose | `skills/spec-author/SKILL.md:229-229` | none | - | none on record | C2, C4 |
| 53 | spec-author | 3. Run the completeness pass | `skills/spec-author/SKILL.md:600-600` | none | - | none on record | C2, C4 |

## What the two tables add up to

- **37 of the 88 rules have an enforcing machine** — 23 of the 35 shared rules, 14 of the 53 working-skill rules. The other 51 have none.
- **8 of the 88 rules have a recorded fire.** Three come from the hook meter: base rule 25 with 26 fires, base rule 2 with 20, base rule 29 with 4. Five come from the six dated gate catches: base rule 8 (2026-07-20), base rule 10 (2026-07-27), base rule 33 (2026-08-05), build-pipeline's prove step (2026-07-20) and build-pipeline's test step (2026-07-23).
- **80 of the 88 rules have no recorded fire**, and 51 of those have no machine that could produce one.
- **The most-firing machines carry no rule of the 88.** `scissors-scan.py` fired 131 times and `affirmation-scan.py` 37; both hold writing laws that live in the personal profile and in pack prose outside the numbered rules — `skills/communicator/SKILL.md:437` mentions the scissors check in passing, and that line falls outside every one of the 53 counted rules. The sixth dated gate catch, gate s on 2026-07-20, holds INV-208, which no rule of the 88 carries.
- **One machine is silent under its own law.** `answer-first-scan.py` shows 0 fires over 3,204 runs, past row 391's default 20-run window (`guardrails/net_meter.py:47`). It is a retirement candidate, and the retirement is his call.

## Where the recording stops, in order of what it costs to fix

1. A gate that fires leaves no machine-readable trace. The only record is a sentence someone wrote in `JOURNAL.md` that same day, so the six dated catches are the six a reader found by hand, and how many more happened is unknown.
2. A hook's meter record carries no timestamp, so no fire can be dated and no window can be measured except by the log's order.
3. A machine records what IT caught, never which rule it was carrying, so the rule column of this page is rebuilt by reading and judging rather than read off a file.
4. A pre-show lint — `preshow-lint.py`, `preshow-register-lint.py`, `preshow-legibility-lint.py` — blocks text on the way to him and writes nothing down, so three of the rules with a machine can never show a fire.
5. A test that reds during real work is not recorded against the rule it pins, so the largest machine of all, gate b's suite, contributes no rule fire at all.

## D10 (candidate) — the decision row this page owes him; numbered after the plan's D1-D9

**Proposal.** Record a rule's fires the way row 391 already records a check's, using the shape that landed with that row rather than a new one. Four parts, each buildable alone:

- **D10.1 — a rule roster.** One file mapping each machine to the rule it carries, seeded from the two tables above. No new machine; it turns this page's judgment into a file a script can read. Cost: small.
- **D10.2 — a timestamp in the meter record.** One field added to the line `hook-meter.py` and `net_meter.py` already write, so a fire can be dated and a window measured. This edits an existing instrument rather than adding a hook. Cost: small.
- **D10.3 — wrap the push gates.** `guardrails/pre-push` calls each gate directly; wrapping each call in `net_meter.py --wrap <gate>` makes every gate's runs and fires countable, which is the pack-side arm row 391 shipped and never wired. Cost: medium, and it touches the file every push runs.
- **D10.4 — wrap the three unmetered wired hooks.** `chat-law-hook.sh`, `clock-hook.sh` and `midturn-chat-scan.py` are wired in `~/.claude/settings.json` without the meter. Cost: small, and it lands on the personal layer rather than the pack.

**Why it waits for his word.** The campaign's rule 2 bans a new check, rule or hook before the campaign closes. D10.1 and D10.2 add no machine and only extend records that already exist; D10.3 and D10.4 change how existing machines are invoked. His word decides whether any of the four counts as new machinery.

**What it would buy.** Every later pass of this page would be read off a file instead of rebuilt by judgment, and a rule's retirement would arrive with a dated count beside it, which is the evidence his law asks for.

