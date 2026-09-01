# Every number in the tree, and its verdict — 2026-09-01

The owner's rule, 2026-08-07 09:16, forceful: find and root out every invented number. His standing
word states the bar plainly — a number pulled from the air is forbidden, and no gate, hook, config,
counter, or threshold stands without an outside source or an incident that already happened.

A first census ran that same day and found 144 numbers governing behavior across the tree. A sweep on
27–28.08 went through the machinery-heavy half of that list file by file: six removed, twelve grounded,
twenty-seven honestly labelled in place, four out of this session's write-scope. That sweep's own
account lived in a gitignored working note, and the page it owed — one list, every number, its home,
its verdict — was never built. This is that page, read against the tree as it stands today, three days
later.

Method: every guardrails script, every guardrails/scripts JSON config, every hook, every template, the
spec body (now `spec/*.md`), and the pack's own skill files were re-opened at the location the 2026-08-07
census named, or at its current location where the file moved. A number counts here when it is a
hard-coded threshold, cap, timeout, count, size limit, percentage, or constant that governs behavior.
Line-number citations, version numbers, dates, ids (`q-xxx`, `INV-xxx`), and fixed-enumeration counts
(three *named* questions, three *named* corroborating signals) are not numbers in this sense — a list of
three specific things is not a cap someone could have picked differently. Test fixtures, `PLAN.md`, and
`docs/queue-archive/` are excluded as instructed; they are not live behavior.

## Grounded — traces to an outside source or the owner's own word

| Number | Home | Ground |
|---|---|---|
| Two consecutive clean cold reads before a text ships (r54) | `guardrails/language-rules.json` | Owner's word, 2026-08-05 ~22:52, `DECISIONS.md` |
| Three parallel build lanes without asking | `skills/live-spec-base/references/settings-ladder.md`, `scripts/open-lane.sh`, `spec/roles-and-agents.md` | Owner's word, 2026-07-06, `DECISIONS.md` [T-18] |
| Nine task lines on the board (`TASK_LINE_BUDGET`) | `scripts/state-probe.sh:126` | Traces to the report format's own home, `~/.claude/playbook/CLAUDE.md`, "How a reply to him looks" — 9 lines + 1 summary = the ten-line cap stated there |
| Far-tier surfacing, at most once every 14 days | `skills/live-spec-base/references/settings-ladder.md:64` | Recorded as the person's own cadence, moved by his word, held in his profile — not a script-invented figure |
| `bytes_per_criterion` ratchet, 185.8 | `guardrails/spec-ratchet.json` | Measured against the live spec at every landing; moves only by that measurement, never invented |
| Redundancy-open floors, 116 (spec) / 15 (architecture) | `scripts/spec-debt-cap.json` | Re-measured 2026-08-24 after a coverage bug was fixed; each figure is the honest count of the assembled document, with the correction's reason written in the file |
| Register-lint pattern floor, 23 | `scripts/register-lint-floor.json` | Tied to INV-83 — the set only grows, one entry per caught leak; not a chosen magnitude |
| `progress-baseline.json`'s measured facts (bytes, requirement/criteria counts, findings counts, 10 min/100 findings, 25 min/round) | `guardrails/progress-baseline.json` | Every figure cites the dated report or commit it was read from; the file's own rule is "a fact absent here prints 'not stated' rather than a guess" |
| Contrast ratio / font-size floors (4.5:1, 3:1, 24px/18.66px/12px) | `scripts/preshow-legibility-lint.py` | Matches the published WCAG AA thresholds |
| ~500-line skill-file ideal | `tests/test_communicator_body_thinned.py` | Follows published skill-authoring guidance |
| Register-judge timeout, 120s | `hooks/register_judge_core.py:42` | Derived from a measured ~33s call cost (~3.6x safety margin) plus the owner's 2026-07-17 ~16:39 word choosing the async road over a synchronous wait, `ROADMAP` row 416 |
| 25-word sentence cap / 15–25 word target band (r08) | `guardrails/language-rules.json` | Follows plain-language readability practice, cited in the rule's own notes |
| Work-board update completes within ~5s; an open page re-reads itself every ~5s | `spec/work-board.md:145,158`, `architecture/quality-budgets.md:13` | Each carries the spec format's own `[default]` marker — the format's built-in way of naming a value the agent set that the human may retune |
| Full-suite wall-time budget, 1,780s | `architecture/quality-budgets.md:9` | Measured 2026-08-13 from seven real runs of the suite (1,221.81s–1,605.37s), with the spread itself reported ("swung 31% between runs, a load signal more than a code signal") — the strongest-grounded number in the whole tree. **But its gate is gone**: the file's own note says "its mechanical watcher retired... nothing reds past this budget today, and it is read by eye if at all." `guardrails/check-suite-budget.sh` and its call site in `guardrails/check-tests.sh` are confirmed removed. The number is honest; nothing enforces it. |

## Honest default, labelled — the file admits it is unproven

| Number | Home | Label |
|---|---|---|
| Board's shown-item cap, 12 | `guardrails/check-board.py:60` | "No incident or source behind the 12 — an engineering default, not a policy decision." |
| Pin-drift line tolerance, ±2 lines | `guardrails/check-pin-drift.sh:58` | "No incident or source behind it… an engineering default, not a policy decision." |
| Pin-drift furniture-word floor, 4 chars | `guardrails/check-pin-drift.sh:84` | "No source behind the exact 4 (2026-08-07 census, row 10); an engineering default." |
| Relocation-vs-fresh-landing day-lag, 2 days | `guardrails/check-landing-next-steps.py:330` | "No incident or source behind the 2 — an engineering default… (the 2026-08-07 census, row 7, found no trace)." |
| Reasonless-rule ratchet cap, 4 | `guardrails/check-language-rules.py:64` | Self-documented ratchet: seeded from a measured count, may only fall |
| Runaway-child CPU threshold, 50% | `guardrails/check-runaway-child.py:52` | "50% kept — NOT ruled… this is a FIXED default today." |
| Skill-frontmatter parse window, 40 lines | `guardrails/check-skill-loadability.sh:23` | "No source behind the exact 40; an engineering default with wide measured margin." |
| Tier-refusal thresholds (3 refusals; 2–8 word phrase) | `guardrails/tier-refusal.json` | Explained in the file's own comments as the experiment's working numbers, not a ruled bar |
| Worker-restore scan window, 24.0 hours | `guardrails/check-worker-restore.py:298` | "24h kept — NOT ruled… No incident traces this window either way." |
| Cross-cut boundary-candidate threshold, 3 | `guardrails/crosscut_counter.py:28` | "No incident or source behind the 3… It gates nothing: a flagged pair is a candidate surfaced for a person to judge." |
| Net retirement-candidate window, 20 runs | `guardrails/net_meter.py:47` | "No incident or source behind the 20… It judges no work and retires nothing." |
| Idle-output threshold, 120s | `guardrails/reap_owned_group.py:39` | "120s matches the shipped two-minute window… This is a FIXED default today." |
| Deposit-description floor, 2 words | `guardrails/check-deposit-description.py:77` | "The one recorded reason for the 2 is alignment, not measurement" — journal 2026-07-17, and admits its aligned partner file is gone |
| Register-judge quote-hallucination floor, 12 chars | `hooks/register_judge_core.py:57` | "The two magnitudes have no incident or source behind them — engineering defaults, not policy decisions." |
| Negation-opener scan window, 12 words | `scripts/spec-style-lint.py:112` | "No incident or source behind the 12… An engineering default." |
| VERSION-fetch curl timeout, 10s | `scripts/check-pack-update.sh:48` | "No incident or source behind the 10; it is an ordinary engineering default for a one-line fetch." |
| Check-phrase floor, 8 chars | `scripts/needle-extract.py:56` | "No incident or source behind the 8 (the 2026-08-07 census, row 67)." |
| Card-value truncation, 160 chars | `scripts/onboarding-card.py:226` | "No source behind the 160 (2026-08-07 census, row 68)." |
| Stranger-monitor lock staleness, 3600s | `scripts/stranger-wish-monitor.py:61` | "No incident or source behind the figure: an engineering default of one hour." |
| Rendered-page head-read bound, 4096 bytes | `scripts/sweep-rendered.py:95` | "No incident or source behind the figure itself; it is one filesystem block." |
| Lean-orchestrator inline-read ceiling, ~50KB | `hooks/lean-orchestrator-scan.py:53` | "The MAGNITUDE has no source — INV-70 says only that this is 'a tunable parameter, not a law'." |
| Empty-shell byte floor, 100 bytes | `templates/test_scaffold.template.py:32` | "A smell test… not a size standard." |
| Every timeout, retry cap, and settle delay in the browser harness (profile-dir staleness 3600s, glut warning at 50, 60s command timeout, 2.0s frame probe, and the rest) | `templates/headless_harness.py:172-182` | One blanket note covers the whole file: "No incident or source stands behind any of the magnitudes… This note is that mark for all of them, so nothing here reads as grounded policy." |
| Duplicate-fact detector thresholds (Jaccard 0.60, containment 0.85, 6-token floor) | `guardrails/language-rules.json` (r56) | "kept — NOT ruled… The values match the design doc's own worked reasoning (`docs/prose-quality-gate-design.md`); no incident traces either value." |
| Quote-span cap, 80 chars | `hooks/register_judge_core.py:49` | Same sentence as the 12-char floor above: "The two magnitudes have no incident or source behind them — engineering defaults" (2026-08-07 census, rows 39 and 85) |
| Node-per-file default, 2 | `skills/design-reviewer/SKILL.md:171-172` | "Two nodes per file is the default to watch for" — explicitly named a default in the prose. The enforcement machinery behind it (`guardrails/node-file-cap.json`, `guardrails/node_growth_counter.py`) is gone (see Removed); the number survives on its own as unenforced, labelled prose. |

## Removed — the census caught these and they are gone

| Number | Former home | What happened |
|---|---|---|
| Four byte ceilings on the big documents (840,000 / 700,000 / 530,000 / 640,000) | `guardrails/doc-bounds.json` | Retired whole 2026-08-18 "as an unrequested bound" — the census had flagged this as squarely the size-cap class the owner's 2026-08-07 ruling struck |
| Whole criterion-readability word/char/anchor family (r08's spec-body cap, r11's anchor thresholds, r35, r36) | `guardrails/criterion-readability.json`, `guardrails/check-criterion-readability.py` | Cut whole 2026-08-19; confirmed carried no live CI catcher before removal |
| Rule-census script and its floor mirrors | `guardrails/rule-census.json`, `scripts/rule-census.py` | Gone with the family above |
| Tree-count expected-seconds figure | `guardrails/tree-counts.json`, `scripts/gen-tree-counts.py` | File and script both gone |
| Answer-first lead-signal char floors (220 / 450 / 550) | `hooks/answer-first-scan.json` | Retired 2026-08-11 on the owner's word after 3,095 runs and zero catches |
| Register-judge's 120-char minimum-reply floor | `hooks/register-judge.py` | "Had no stated source anywhere and was removed 2026-08-26" |
| Tier-refusal's invented 1–99 phrase-width fallback | `guardrails/check-tier-refusal.py` | Removed in the 28.08 push range; an undeclared width is now reported as a config defect instead of silently passing |
| Node-per-file cap seeds (config + counter script) | `guardrails/node-file-cap.json`, `guardrails/node_growth_counter.py` | Both gone from the tree; the "2 per file" figure itself survives as labelled, unenforced prose — see Honest default, above |
| Waiver expiry ceiling, 30 days | `scripts/gate_common.py:145-152` | Removed 2026-08-26: "no waiver has ever expired and blocked a push… no single recommended replacement, so [the ceiling is gone]." The mechanism it sat on doesn't need a magnitude — every waiver already carries an `expiry` field and an expired one already hard-errors. The owner's own standing rule against a number pulled from the air, applied to itself. |
| Far-tier report-shape script | `guardrails/check-far-tier.py` | Gone; the 14-day cadence it enforced now lives as an owned setting in the settings ladder instead (see Grounded) |
| Criterion-defects display cap | `scripts/rank-criterion-defects.py` | Confirmed dead code, removed 2026-08-19 |
| Resume-digest hard line cap, 100 | `templates/NEXT_STEPS.template.md`, `tests/test_resume_digest.py` | Number gone from both; the file now carries only the qualitative law — one live-state block, no redundancy — matching the 2026-08-07 ruling's own §5 ("its qualitative law takes over") |

## Invented, ungrounded — still sitting there with nothing behind them

| Number | Home | What it governs |
|---|---|---|
| Significant-word floor, 3 characters | `guardrails/check-vocabulary.py:64` | Decides which words of a glossary term must appear in a document's body for the term to count as used. No comment near it says why 3, and none admits it's a guess. Present since the 2026-08-07 census (row 15, "no trace found") and never touched by the labelling pass that reached its siblings. |
| Negator look-back window, 4 words | `guardrails/check-deferral-marker.py:132` | How far back a negator ("not", "never", "no") is searched for before a deferral signal is silenced. The docstring explains what the window is *for* ("an incidental negator far away cannot silence a real park") but never says the number 4 itself has no source — unlike the near-identical windows in `check-pin-drift.sh` and `spec-style-lint.py`, which got that exact sentence. Same census row (4) as the two, same "no trace found" origin, but this one was skipped. |
| `SIGNAL_WAIT_SECONDS = 5.0`, `SIGNAL_POLL_INTERVAL = 0.2` | `scripts/wind-down.py:65-66` | How long the wind-down command waits for a signalled worker process to exit, and how often it polls while waiting, before reporting the worker as "still running." **New since the 28.08 sweep** — this file landed 2026-08-31. No comment anywhere in the file says where 5.0s or 0.2s came from; every other timing constant this session checked in files written after the sweep carries a source or an admission, and this one does not. |
| "At most three asks" at the design-review station | `skills/build-pipeline/references/minor-bump-gate.md:8` | Caps how many divergence questions a design review echoes per pass. Distinct from the enumerated "3 named questions" of the node-fitness test — this is a genuine arbitrary cap, and no reason is written for 3 over any other number. |
| "One question crosses the same two agents at most twice" | `spec/roles-and-agents.md:159,183` | Caps how many times a question may bounce between two agents before it escalates to the owner. The Context explains why escalation exists, not why the number is two. |
| "The second occurrence buys an owner" (two-strikes ladder) | `spec/internal-failure-log.md:21,85` | Caps how many times the same defect gets hand-fixed before it must get a named mechanical owner. Same shape: the mechanism is well-reasoned, the magnitude is not. |
| "A behavioral rule that breaks twice earns a live channel" | `spec/guardrails-freshness.md:56` (Requirement 222) | Same family — two breaks, not one or three, trigger a live enforcement channel. No stated reason for the count. |
| "Two or more no answers make the carve premature" | `skills/architect/SKILL.md:118` | The node-fitness test asks three specifically named questions (an enumeration, not a number in this audit's sense), but the cutoff for how many "no" answers reject a carve — 2, not 1 — is a separate, genuine threshold with no reason written for it. |
| "Two consecutive unexplained failures" halts a worker | `skills/director/references/delegation-protocol.md:32` | Caps how many unexplained command failures a delegated worker gets before the brief calls a HALT. No citation. |
| "Two-three plain sentences" step-completion digest | `skills/communicator/SKILL.md:91` | Caps how long a step-completion beat runs. Sits three lines above two other cadence numbers in the same rule (`~10 minutes`, `~2 minutes`) that both carry an explicit `[default]` tag — this one does not. |
| "In two or three sentences," the spec preamble's coverage statement | `skills/spec-author/references/how-it-reads.md:81` | Caps the preamble's bracket-code explainer length. No citation. |
| "A 3-5 line 'how the layers stack' map" | `skills/spec-author/references/how-it-reads.md:96` | Caps a structural overview's length. No citation. |
| Recurring-bug re-door window, ~30 days | `skills/director/references/request-kind-table.md:18` | Decides whether a second bug in the same area re-doors to a feature rather than another patch. No citation. |

Lower stakes, noted for completeness: `scripts/progress-report.py:58` shows the 15 worst-scoring
documents in a summary table; its own comment says "nothing reds if it changes," which makes it cosmetic
rather than a governing bar — closer to a display width than an invented standard, but it carries no
label calling it that.

One drift worth naming on its own: `guardrails/language-rules.json`'s r14 entry still claims "no prose
home states" the 12-character quote-hallucination floor. That sentence is now false — `hooks/register_judge_core.py:57`
does state it, in the same "engineering default, no source" language used everywhere else in the tree.
The number itself is fine (see Honest default, above); the registry's own notes field is stale and
should be refreshed the next time r14 is touched.

## What changed since the 28.08 sweep, and what it means

The 27–28.08 pass worked a self-described list of 45 ungrounded findings plus 9 unsure ones, drawn from
the 2026-08-07 census of 144. That list was the machinery half of the census — guardrails scripts,
JSON configs, hooks, templates, and a handful of scripts — and it got the label treatment this page
found consistently: almost every timeout, cap, and window in that class now carries an in-place
sentence admitting it has no source. The other half of the census, the arbitrary caps sitting inside
skill bodies and the spec's own requirements (design-review question limits, escalation strike counts,
crossing caps, digest and preamble length caps), was mostly left as it stood on 2026-08-07 — a little of
it has since been rewritten into the spec format's `[default]` marker (the two five-second work-board
figures), most of it has not (the twelve survivors listed in the table above).

Five files from the original census are confirmed gone from the tree entirely since 28.08:
`guardrails/criterion-readability.json`, `guardrails/doc-bounds.json`, `guardrails/rule-census.json`,
`guardrails/tree-counts.json`, and `hooks/answer-first-scan.json` — each removed with a dated reason
recorded either in a commit or in the surviving code that used to read them.

One number is new since the sweep closed: `scripts/wind-down.py`'s two timing constants, in a file that
did not exist on 28.08 and landed 2026-08-31. It is the one item on this page that is a genuinely fresh
find, not a survivor. Every other item in the ungrounded tail traces back to a row in the 2026-08-07
census tagged "no trace found" — most of them in the skill-body half of that census, which moved homes
as `build-pipeline`'s SKILL.md was cut down to a 67-line adapter on 2026-08-25 and its content spread
into `architect`, `director`, `spec-author`, and `communicator`'s own reference files. The relocation is
real; the number never got grounded or labelled at either address.

This page also owes a correction to its own working method: a supplementary agent re-read every row of
the 2026-08-07 census file by file, independent of the reading above, and it surfaced six more survivors
this session's first pass missed entirely — a cutoff buried inside the node-fitness test's prose
(`skills/architect/SKILL.md:118`), a worker-HALT trigger, a digest-length cap sitting three lines from
two labelled siblings, two spec-author sentence/line caps, and a recurring-bug re-door window. All six
are folded into the table above. It also caught one removal this session's own reading missed: the
30-day waiver-expiry ceiling, gone from `scripts/gate_common.py` since 2026-08-26 with the owner's own
standing rule named as the reason. And it found the strongest-grounded number in the whole tree — the
suite's 1,780-second wall-time budget, measured from seven real runs — sitting behind a gate that no
longer exists.

Two skills are out of write-scope, same as the 27.08 pass found: `skills/product-prover/` and
`skills/text-audit/` are external clones, gitignored, installed on this machine but not owned by this
repository — their own numeric content is a different project's to ground or label. `skills/text-audit/`
has no numbers of its own left in this tree (the in-tree remnant, `skills/text-audit-pack/SKILL.md`,
carries only pack bindings). `skills/product-prover/SKILL.md` does carry its own numbers, and most of
them are still exactly as ungrounded as this project's own once were — nine separate figures (a 2-header
depth cap, a 30-second scan target, a 5-minute read target, a 10–15-second per-finding target, a "3 of 4
elements," entity/state diagram triggers, observation/question count bands, a sentence-count cap on the
opening assessment, and a "top 3 things to fix" cap) with no citation anywhere in that file. None of it
is counted in this page's tally below, on the same out-of-scope basis the 27.08 pass used — but it is
the same defect this row exists to catch, sitting one repository over.

## Count

**14 grounded · 26 honest-default-labelled · 12 removed since the original census · 13 invented and
still ungrounded** — twelve survived from the 2026-08-07 census unlabelled (several relocated when
`build-pipeline`'s SKILL.md was cut down), and one, `scripts/wind-down.py`'s two timing constants,
is new since the 28.08 sweep closed. A further nine ungrounded figures sit in `skills/product-prover/SKILL.md`,
an external clone out of this project's write-scope, named above but not counted in this tally.
