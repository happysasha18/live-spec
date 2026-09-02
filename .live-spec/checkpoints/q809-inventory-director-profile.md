# Inventory: director/SKILL.md, profile.md, CLAUDE.md — read-only

Scope note: this file is read-only inventory, produced by grepping `/Users/sashaabramovich/live-spec/scripts`,
`/Users/sashaabramovich/live-spec/tests`, `/Users/sashaabramovich/live-spec/guardrails` (the actual gate
directory the three loaded files' own text points to), `~/.claude/settings.json`, and the hook scripts
`settings.json` wires. No file besides this one was edited.

Byte totals as loaded today: director/SKILL.md 25613 · profile.md 9680 · CLAUDE.md 4386 · sum 39679.
Director's `references/` (44314 bytes total, 13 files) are not loaded at start.

## Director — skills/director/SKILL.md

| Heading | Core | Bytes | What the rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| ## First — what did the human just do? | Classify what the person did — question, idea, observation, decision, correction, instruction, or halt — before deciding any work is needed. | 6087 | ~70% worked micro-scenarios distinguishing act pairs (idea-vs-instruction, decision-vs-correction, halt-vs-instruction); ~15% the table itself; ~15% justification for asking the question first. | No. Not restated in profile.md, CLAUDE.md, or live-spec-base/SKILL.md. Compared line-by-line against `references/request-kind-table.md` — that file answers a different question (which document a request enters) and never lists the seven acts. See special section below. | `evals/director/scenarios.json` + `evals/director/check.py`, exercised by `tests/test_director_scenarios.py` (`ACTS = {"question","idea","observation","decision","correction","instruction","halt"}`). These are apparatus tests for the eval grader, run "when the skill changes" per the file's own docstring — not a live per-turn gate. |
| ### One turn, several acts | List every act in one message before acting on any of them; a clause you can't place counts as its own act. | 3125 | ~70% worked examples of a clause getting wrongly absorbed into a neighbour; ~15% restates rule 1's "grounds carry their own act" test; ~15% the naming-cost tradeoff line. | No. | Same eval suite as above; no dedicated script for multi-act detection. |
| ### Not every message is one of the seven | Treat a greeting, thanks, or joke as conversation and record nothing, unless it carries an unreported fact. | 1461 | Worked example (a curse that is also a report) plus a cross-reference back to the competent-colleague test. | No. | None found. |
| ### When the act is unclear | Ask one short question in his own words only when a wrong guess would change the outcome; never guess to be safe. | 500 | Justification only — "creating work is the expensive direction." | Yes — live-spec-base rule 1: "A gap only the human can fill is asked... Never invent intent, and never ask what you can decide or verify yourself." Same principle, director's version is the speech-act-specific instance. | None found specific to this line; base rule 1's own gates are listed under live-spec-base below. |
| ## Then, only for work that was accepted — what does it touch? | For accepted work only, name every dimension it touches — never inventing a rule's one home. | 1753 | ~35% is the pointer to `references/request-kind-table.md`'s five-houses table; rest is the seven-dimension list plus the "naming claims something changes" rule. | The five-houses table itself lives ONLY in `references/request-kind-table.md` — this section correctly points rather than restates. No duplication. | None found keyed to "dimensions touched." |
| ## The decision sheet (+ ### A sheet at the size the work deserves) | Write the ten-line decision sheet for accepted work only, filling each line only when something is actually known. | 1459 + 1119 | The template's ten bullet definitions are ~70% of the parent section; the worked example is 100% worked example (a full sample sheet for one bug fix). | No. | `scripts/checkpoint.py` stores the sheet verbatim in the checkpoint's DECISION SHEET section; `tests/test_checkpoint_mechanism.py` and `test_checkpoint_closes.py` check the checkpoint has/lacks content, not that all ten lines are present. |
| ## Execution | Open one checkpoint per new work item, brief specialists from it, run lanes only when independent, replan on new facts, verify by evidence not self-report, close the checkpoint in the same step. | 5276 | ~55% pointers to four reference files (build-craft, class-hunt, verify-step-detail, landing-law) plus one line each restating what's in them; ~30% restated rule text (checkpoint mechanics, lane independence test); ~15% history (the retired `delegation-protocol.md`). | Partial. The checkpoint mechanics restate live-spec-base rule 6 in different words ("A file on disk... holds done/in-progress/next" vs. rule 6's identical description). The lane paragraph explicitly does NOT restate — it says "rule 7 carries the lane law in full and is not repeated here." | `scripts/checkpoint.py` (new/update/close) · `scripts/open-lane.sh` · `guardrails/check-worker-restore.py` · `tests/test_checkpoint_mechanism.py`, `test_checkpoint_closes.py`, `test_lane_open_act_convergence.py`, `test_worker_restore.py`, `test_class_hunt.py`. |
| ## The specialists | Call only the specialists a piece of work actually needs, briefing each with the goal and primary sources, never a copy of what was already read. | 2139 | ~75% is the ten-row routing table itself (name → when → where it lives). | No restatement; each named specialist's own SKILL.md carries its real content, this is a pure routing index. | None keyed to the table itself; individual specialist skills carry their own gates (e.g. skill-review). |
| ## What the human hears back | After every message, say in one plain sentence whether it was answered, remembered, changed running work, or started new work. | 706 | Justification only. | Overlaps in theme but not wording with profile.md `answer-first` and CLAUDE.md's Канон+prose format — three different framings of "tell him what happened," none identical. | None found keyed to this four-way classification. |
| ## Work that belongs elsewhere | Route spec/architecture/test/code writing to specialists, checks/push to guardrails+CI, and project setup to build-pipeline. | 813 | Pure routing pointer, no restatement. | No. | None found. |

### Special attention — the seven acts vs. `references/request-kind-table.md`

Read both, line by line. They are not the same table and do not overlap:

- The loaded body's seven acts (question/musing, idea, observation, decision, correction, instruction, halt) answer **"did this person even ask for work?"** — before any document, spec, or gate is in scope.
- `request-kind-table.md`'s "closed set" (product behaviour, technically-phrased request, defect, docs-only, tiny reversible edit, settings value, inbox wish, method/skill change, sketch, research question, feedback hand-back, three setup walks) answers **"given that work was accepted, which document does it enter, and what's the mandatory back-check?"** — a routing table for already-accepted work.

No sentence, no row, no phrase is shared between them. The reference file's own opening line ("The closed set of request kinds referenced from SKILL.md's 'When to run it' section") confirms it is a different skill's table (build-pipeline's old door set, inherited by reference) reused here for the second question ("what does it touch"), not a restatement of the first.

**Verdict: the full seven-acts table is needed in the loaded body.** Nothing in it duplicates `request-kind-table.md`. What the loaded body adds beyond that reference file is the entire first question — whether a message is work at all — which the reference file never asks; it starts from "a request" already given. If anything should shrink here, it is the worked-example prose around the table (the four flagged failure patterns run ~5KB across the four subsections), not the table's own existence.

## Profile.md — live-spec/profile.md

Grouped by `##` heading; one row per dash-key.

### ## Resolution (256 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| order | Resolve conflicts as: his live word, then host profile, then this file, then package defaults. | 93 | Cites code E-13. | Yes — live-spec-base's settings ladder states the identical order: "session beats host beats personal beats package default (SPEC E-13)." | None found; the order is documentation, not a mechanical resolver. |
| authority | Set a trust or mode level only on Alexander's own explicit word. | 63 | Cites INV-9. | Overlaps Trust.level below (same file). | None found. |
| home | Edit the canonical profile in the playbook repo; the live-spec copy is a symlink. | 83 | Pure fact. | No. | None — a filesystem fact, unchecked. |

### ## Language (2006 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| docs | Write all docs, commits, code, and artifacts in English. | 60 | none | No exact restatement in the other two files or live-spec-base. | None found — no doc-language detector. |
| chat | Speak Russian in chat, plain language, codes only in parentheses. | 175 | ~55% dated citation (2026-08-09, reversing a 2026-07-30 rule). | No. | None found. |
| native-english | Write English in short SVO sentences, common words, no poetic compression. | 96 | none | No. | None — `register_judge_core.py` exists but is unwired (see below). |
| no-calques | Never loan-translate a pack term into chat; say the mechanism in plain words. | 128 | none | Yes — live-spec-base rule 2, near-verbatim: "A term or metaphor coined in the docs language is never loan-translated into chat... That is the no calques rule." | The scanner for this (`midturn-chat-scan.py`) is retired to `~/.claude/hooks/attic-2026-08-17/`; not wired in any current `settings.json`. |
| industry-words | Narrate in standard industry terms; keep coined pack terms in docs. | 80 | none | No. | None found. |
| no-contrast-frame | Never define a thing by denying its neighbour ("X, not Y"); state what it is, give the boundary its own sentence. | 173 | none | MEMORY.md echoes this line closely (same author's own index, not an independent second source). | `hooks/scissors-scan.py` exists, tested (`tests/test_scissors_scan.py`) — a Stop hook, but **not wired into any current `settings.json`** (global, local, or project). Stood down 2026-08-17, opt-in since. |
| no-inflation | Never grade a result's size or promise a breakthrough; state what happened and the numbers, flat — binds chat, docs, and worker briefs/reports. | 271 | ~40% is the explicit scope-binding clause. | No second full copy. | Same `scissors-scan.py` — unwired. |
| no-validation | Answer his remark on its merits; never grade or praise it; never rank my own acts. | 120 | none | No. | `hooks/affirmation-scan.py` exists, tested (`tests/test_affirmation_arm.py`) — unwired, same as above. |
| answer-first | Open every reply with the answer he can stop at; reasoning and options after. | 150 | none | No. | Claimed live by the profile's own next row (chat-law-hook + answer-first-scan.py) — see finding below: half of that claim is false. |
| register | Hold human-facing text to communicator's register (14 rules, 8-point check) before any report; absent that, plain words, defined terms, positive framing. | 294 | ~45% is the fallback-rule restatement. | Overlaps native-english and no-contrast-frame above (same fallback rules repeated inside this same file). | `register_judge_core.py` + `register-judge.py` exist, tested (`tests/test_register_judge.py`) — unwired, same pattern as above. |
| enforcement | Names which scanner catches which chat law. | 345 | ~90% is itself a list of pointers (script names + ROADMAP row numbers). | No — this line is the enforcement index itself. | **Broken pointer found:** `answer-first-scan.py` does not exist anywhere under `~/.claude/hooks/`. It was retired to `/Users/sashaabramovich/live-spec/attic/answer-first-scan.py`. The profile still cites it as live. |
| undefined-term | Treat "what is X?" from him as a failed message; fix how the term is written, not just answer it. | 90 | none | No. | None found. |

**Finding:** every mechanical scanner this section names (`scissors-scan.py`, `affirmation-scan.py`, `register_judge_core.py`, `hedge-scan.py`, `code-anchor-scan.py`) exists on disk and has its own test, but **none is wired into `~/.claude/settings.json`, `~/.claude/settings.local.json`, or any project `.claude/settings.json`** — confirmed by reading all three files' `hooks` blocks directly. `scripts/install-pack-hooks.sh`'s own header states why: "all six stood down from the default wiring on the owner's word of 2026-08-17... each is opt-in and a host turns one on in its own settings.json." Only `chat-law-hook.sh` (a names-only reminder, not a scanner) is actually wired, via `UserPromptSubmit`.

### ## Proactivity (4110 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| mode | Default max-proactive: take the recommendation and act; batch questions; pause only for taste, design, or outside-git irreversibility. | 129 | none | Overlaps live-spec-base rule 27's three surfaced-decision cases (taste, trade-off, definition of correct) — same substance, different words. | None — a posture, not gated. |
| subtask | Judge each subtask on its own content, not its heading; split mechanical from taste. | 86 | none | No. | None found. |
| no-hedge | Never say "I can only do X, say the word"; if git-reversible, do it and report in one line. | 104 | none | Overlaps live-spec-base rule 17's irreversible-outside-git criterion. | None keyed to "no-hedge"; `hedge-scan.py` targets chat-text hedging, a related but distinct pattern, and is unwired regardless. |
| deferral | Re-test every "needs his word" marker for derivability at each touch; only taste/policy/outside-git-irreversible facts stay his. | 767 | ~50% worked criteria, ~20% a dated quote (27.08) carving out a machinery exception. | **Yes, directly** — live-spec-base rule 29 states the identical mechanism nearly verbatim: "A deferral must justify itself, or the item is the seat's to do... re-tested by derivability at its first writing and at every touch after... do it, cite the artifact, and drop the marker." | Real and active: `guardrails/check-deferral-marker.py` + `tests/test_deferral_marker.py` (base rule 29's own gate, INV-152/155). |
| how-to-ask | Ask only on a genuine fork; give options with a plus, a minus, a pick, never a bare yes/no. | 144 | none | Overlaps base rule 27's fork criteria. | None found. |
| plan-sweep | Walk the whole plan before running any step and surface every decision its user owes; never stall mid-build. | 278 | none | No. | None found — no "plan-sweep" named check. |
| loops | Propose a recurring check myself, state its exact command, arm it where possible. | 91 | none | No. | None found; the `loop` skill is a capability, not a check on this rule. |
| full-vs-light | Classify build-pipeline footprint, state verdict and reason, ask with a pick if unsure. | 123 | none | No. | None found. |
| lean-seat | Default STRICT: dispatch every authored artifact and every read past a glance to a worker. | 233 | ~35% defines "glance." | **Yes** — live-spec-base rule 25 states this at length, including the same "glance is bounded... one small file, or a handful of targeted lines" definition. | None as a hard gate; rule 25's own "delivery report's delegation accounting" is a reporting duty, not a blocking check. |
| lanes.cap | Cap parallel lanes at 3 without asking. | 131 | none | Restates live-spec-base rule 7's cap (T-18, INV-214); profile supplies the number. | **Real** — `scripts/open-lane.sh` reads this exact key (confirmed at lines 27 and 64: `cap reached: ... cap is $CAP (lanes.cap)`). |
| quality-first | Run the deep audit by default, strongest tier, fresh clean context; never let cost block it. | 236 | none | Overlaps cost-criterion below. | None found as a gate ensuring "strongest tier." |
| cost-criterion | Plan budget sets the pace only — slower and cheaper are fine, worse is never allowed. | 499 | ~55% is a dated quote (2026-08-05). | Overlaps quality-first; MEMORY.md echoes the same quote. | None found. |
| cost-levers | Reopen fresh at milestones, file long output to disk with inline verdict, batch calls, route mechanical work to sonnet. | 166 | none | Overlaps live-spec-base rule 5 (per-unit tiering). | `~/.claude/playbook/tools/usage-audit.py` is named as a tool (outside the grepped scope), not a gate; nothing in live-spec/scripts or tests checks this. |
| fable-tokens | Guard the top-tier seat's turns for decisions and acceptance only; send every read/draft/sweep to cheaper tiers. | 595 | ~50% is two stacked dated quotes (2026-08-11). | Overlaps lean-seat and rule 25 (same delegation principle, different tier name). | None found. |
| seat-split | The judging seat plans and accepts; a separate executor window does merge and push. | 498 | ~35% is a one-time-deviation carve-out (2026-08-14). | No. | None found — no script checks which window ran a push. |

### ## Trust (545 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| commit | Commit whenever the tree ends the same or better; never park finished work uncommitted. | 81 | none | No. | None found. |
| push | Push on my own read of the suite log's verdict, not a wrapper's exit code; a stricter host/gate wins. | 191 | none | Overlaps live-spec-base rule 5's raw-output-is-evidence principle. | `guardrails/pre-push` is the real push gate (confirmed present); it enforces suite-green mechanically, though "read the log, not the exit code" specifically is a habit no script can verify. |
| push-standing | Once a project's pushes are approved, every later green push is standing-authorized. | 106 | none | No. | None found. |
| self-install | Install hooks, skill copies, sync scripts myself, and report having done so. | 81 | none | No. | None found — install scripts exist but nothing checks this rule was followed. |
| level | Leave general trust at package default until he names one. | 72 | none | Overlaps Resolution.authority above (same file). | None found. |

### ## Chat (520 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| timestamp | Lead every reply with [HH:MM]. | 43 | none | **Yes, verbatim** — CLAUDE.md's "How a reply to him looks" opens with the identical instruction. | **Real and live** — `hooks/clock-hook.sh` (wired, `UserPromptSubmit`) injects the current wall clock plus the instruction to lead with it, every prompt. |
| no-disclaimers | Drop "честно" framing, permission-asking, cheerleader language; act, self-check, report. | 109 | none | No. | None found; `hedge-scan.py` targets a related but distinct pattern and is unwired anyway. |
| no-self-audit | Own a mistake in one line; write no self-audit paragraph. | 74 | none | No. | None found. |
| process-notes | Mark internal notes "(себе)", one idea per line, always offer a free-form answer. | 101 | none | Overlaps MEMORY.md's separate "always-offer-free-text-option" note. | None found. |
| recap-unanswered | End every reply with a recap of any of his unanswered or buried questions. | 86 | none | No. | None found. |
| narration | Narrate in the chat language, in the reports' voice, in roadmap terms. | 93 | none | Overlaps docs/chat rows above. | None found. |

### ## Owner reports (974 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| format | A message asking his word or reporting a result carries five fixed parts: user-facing change, recommendation, what becomes irreversible, external review verdict, real-world-unit numbers only. | 799 | ~80% is the five-part enumerated list itself; ~10% a dated citation (2026-08-14). | Points out to `~/.claude/playbook/CLAUDE.md`'s section "How a reply to him looks" for length/marks/Канон placement — a **different file** from the one under review, sharing a section title with (but different content from) `~/.claude/CLAUDE.md`'s own "How a reply to him looks." Naming collision, not content duplication — flagged as a real finding. | None found as a mechanical check on all five parts. |
| refusal | A message skipping this format goes unread; "попугаи" means reformat, take no action. | 156 | none | No. | None found. |

### ## Showing work (515 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| artifacts | Open rendered artifacts with a new Chrome window via `open`, never a bare path; remote seat uses its own channel. | 157 | none | No. | None found. |
| text-docs | Render prose for him through `render-doc.py` into a new window, never a code editor. | 114 | none | No. | `scripts/render-doc.py` exists — a tool, not a gate; nothing checks it was used. |
| movement-end | After every big movement, unasked, update NEXT_STEPS, report, say memory can be wiped. | 106 | none | Overlaps live-spec-base rule 6 (checkpoint closing) in spirit. | None found as a movement-boundary detector. |
| resume | An hour or less: ScheduleWakeup; longer: cloud /schedule; local files needed: a launchd one-shot. | 118 | none | No. | None found in live-spec scripts/tests — scheduling is a harness feature. |

### ## Identity and hosts (652 B)

| Key | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| address | Call him Alexander, never the short form. | 50 | none | No. | None found. |
| default-reusable | Build for reuse by default; his artifacts are examples, not the definition; ask once at founding. | 147 | none | No. | None found. |
| machine-layout | Skills under ~/.claude/skills/; pack/spec-author/product-prover public, playbook/personal private. | 142 | none | No. | None found — a layout fact, not a checked rule. |
| track-coach | Push track-coach on green without re-asking; reshoot README each push; rule lives in project memory until it moves. | 187 | none | No. | None found in live-spec (track-coach is a separate project's own tree). |
| live-spec | Run the full prover re-check before every push in the live-spec project itself. | 99 | none | No. | `guardrails/pre-push` + the prover gates it calls are the real mechanism. |

## CLAUDE.md — ~/.claude/CLAUDE.md

| Section | Core | Bytes | Rest is | Duplicated elsewhere? | Enforcement |
|---|---|---:|---|---|---|
| Standing rule: "Do not serve machinery" | Never add a new gate, hook, config, counter, threshold, or registry without an outside source or an already-happened incident. | 450 | ~35% is the count-and-date citation (9 times, 17.08→24.08) plus a second quote. | No restatement elsewhere, though live-spec-base's own 2026-08-26 cut of 14 unbacked rules is the same principle applied to itself. | **None found.** The rule cited 9+ times as highest-authority has no mechanical check — it is judged only by the human at review time. |
| Standing rule: "Argue back" | State disagreement and the reason when he is wrong; silent agreement is a failure. | 193 | Dated citation is most of the rest. | No. | None found. |
| ## How a reply to him looks | Lead every reply with [HH:MM] and the Канон — the plan's own task statuses from `state-probe.sh`, verbatim, 7-10 lines, five marks only — then a short prose note naming what moved. | 1531 | ~25% worked example block (the sample ✅/⬜ Канон); ~30% restatement/justification of why it must come from the script, not be typed. | The [HH:MM] instruction duplicates profile.md's Chat.timestamp verbatim. | **Real** — `tests/test_board_matches_the_canon.py` checks the board and `state-probe.sh` render task titles identically; `scripts/state-probe.sh` is the literal generator this section says to carry over; `hooks/clock-hook.sh` supplies the wall-clock half, live. |
| Bootstrap: one-window bullet | One window works one project only; a session writes solely inside its own project's tree. | 229 | none | Overlaps live-spec-base rule 7's fence spirit (loosely — that rule covers concurrent edits within one repo, not cross-project scope) and MEMORY.md's "windows: others AUDIT-ONLY" line. | None found as an automatic cross-repo write-blocker — a discipline, not a mechanical fence. |
| Bootstrap: load-profile bullet | Load ~/.claude/live-spec/profile.md; say out loud if a line can't be read. | 237 | none | No. | None found — nothing verifies the profile was actually read this session. |
| Bootstrap: profile-not-loaded bullet | If the profile load didn't happen or wasn't acted on, say so before doing any work on unconfirmed defaults. | 403 | ~90% is self-referential caveat: "Nothing today checks that the load happened." | No. | None — the bullet states plainly that nothing checks it. |
| Bootstrap: work-by-pack bullet | Work through the live-spec pack; director is the door for every request. | 297 | none | Restates director's own opening framing and live-spec-base's closing roster line ("director reads the human's message first"). | None found as a script checking which skill fired first. |
| Bootstrap: plan-resume bullet | In ~/live-spec, PLAN.md is the plan; open every session with `scripts/state-probe.sh` before reading prose. | 155 | none | Overlaps "How a reply to him looks" above (same script, same file). | **Real** — `scripts/state-probe.sh` exists; `test_board_matches_the_canon.py` exercises it. |

## The three UserPromptSubmit hooks

All three are wired in `~/.claude/settings.json`'s `hooks.UserPromptSubmit` and fire on every prompt in this session (confirmed by reading the file directly).

**`hooks/clock-hook.sh`** — injects: `Wall clock at this prompt: %H:%M, %d.%m.%Y. Lead the reply with a [HH:MM] read off this clock...`
Duplicates: the instruction half duplicates profile.md Chat.timestamp and CLAUDE.md's Канон-section opening line, both verbatim in substance. The clock *value* is unique to the hook — no loaded file can carry a live timestamp — so this hook is the only source of the actual data; the instruction text around it is the third copy of the same sentence.

**`hooks/chat-law-hook.sh`** — injects a one-line names-only list of seven laws (answer-first · plain words/codes trail/narrate · industry words + register lint script name · no contrast frames · routing/tiering · deferral re-test · root-naming), explicitly stating "full texts: ~/.claude/live-spec/profile.md and ~/.claude/skills/live-spec-base/SKILL.md."
Duplicates: every law it names is fully stated in profile.md (answer-first, no-contrast-frame, register under Language) or in live-spec-base (rule 5 tiering, rule 29 deferral). It is a deliberate compression of material already sitting in two of the four loaded documents, re-injected whole every single turn.

**`hooks/routing-preamble-hook.sh`** — injects the zone-referral reminder: refer a request belonging to another adopted project's zone back to whoever asked, citing INV-190/Requirement 196.
Duplicates: this law is NOT in director/SKILL.md, profile.md, or CLAUDE.md — it is live-spec-base rule 31's territory, stated there in full. It does not duplicate the three files this task scoped, but does duplicate a file loaded at every skill's own opening line.

**What this means for the cut:** text a hook injects every turn does not also need to sit in a loaded file. Concretely — the [HH:MM] instruction (in two loaded files plus one hook), the seven chat-law names (compressed in the hook, spelled out across profile.md's Language section and two live-spec-base rules), and the zone-referral law (in the hook and in live-spec-base) are each carried three times over: hook + one or two loaded documents. Cutting the loaded documents' copies down to a pointer at the hook (or vice versa) removes real, measured duplication without losing any rule.

## Byte budget

Every one of the 70 rows above, reduced to `Heading: Core sentence [Enforcement: pointer or "none found"]` and nothing else — no dated citations, no worked examples, no history, no cross-reference prose — was written out and measured directly (`scripts/budget.py` in the scratchpad, `wc`-equivalent byte count):

**10,422 bytes** for the three files combined (director 2,209 B · profile.md 6,830 B · CLAUDE.md 1,383 B), against 39,679 bytes loaded today — a cut of about **3.8x**, not the 4x the task assumed, without dropping any rule identified above. Two things hold this short of 4x: (1) most profile.md dash-keys have no mechanical enforcement at all, so their reduced row still carries the full Core sentence with nothing to shorten it further; (2) "none found" repeated 46 times is itself 46×12=552 bytes of honest overhead a denser enforcement story would remove. This number does not assume every reference-file pointer, cross-file duplicate, or hook-injected line gets deleted outright — it only assumes each section keeps one imperative sentence and one enforcement pointer, which is what the task specified.
