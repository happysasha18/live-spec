# Context audit — findings and paste-ready replacements (2026-07-30, from the Fable session in the home window)

Alexander asked for an outside audit of why sessions degrade once the project loads. Eleven skill files, the profile, the boot file, the prompt-time reminder, recent transcripts, and the last 3 days of commits were each read by a separate clean worker with no project vocabulary in its context. This note carries the verdicts and ready drafts. Alexander decided on 2026-07-30 that the global hook wiring stays in place for now, because other windows use it; every gain below comes from shrinking or replacing text, with no settings changes.

## 1. What loads, and what the readers found

Numbers: bytes from `wc -c`, tokens estimated as bytes/4, word counts from the reader reports.

| Surface | Loads when | Size now | Reader verdict | Target |
|---|---|---|---|---|
| chat-law hook text | every user prompt, every window | 8,297 B (~2,100 tok) | rewrite; ~20% operative | ~500 tok (draft in §3) |
| profile.md | session start | 20,887 B (~5,200 tok) | rewrite as a flat settings table; it reads as a changelog with rules buried in dates and quoted chat | ~1,000 tok; move history to a separate file |
| CLAUDE.md | session start | 1,844 B (~460 tok) | trim; drop archive/rollback trivia | ~300 tok |
| 11 skill descriptions | every session, every project | 1,599 words | replace; drafts in §4 | 251 words |
| live-spec-base body | every pack session | ~14,900 tok | rewrite; 35 rules survive at one imperative sentence + one example each | ~4,500 tok |
| build-pipeline body | pipeline runs | ~14,200 tok | rewrite; ~45-50 rules survive | ~6,000 tok |
| product-prover body | reviews | ~15,650 tok | rewrite | ~5,000 tok |
| spec-author body | spec work | ~14,400 tok | rewrite | ~4,500 tok |
| communicator body | reports | ~11,450 tok | trim (content is concrete) | ~4,000 tok |

Recurring defects across all bodies: coined metaphors used as load-bearing terms, internal law codes cited as if self-explanatory, dated incident stories standing in for rules, and each file breaking the plain-language rule it states. Structural clashes worth fixing during the rewrite: three separate mechanisms in build-pipeline decide how much process a change needs, with no stated precedence; the review skill's lens list gives no stopping test; the reporting skill's 2-minute progress cadence clashes with its own ban on frequent pinging.

## 2. Why the campaign stalled (evidence)

- Of 100 commits since 2026-07-26 (`git log --oneline --since=2026-07-26 | wc -l`), one file received genuine prose rewriting (skills/text-audit/SKILL.md, 6 commits). The most-touched files were queues, journals, measurement tables, and dated reading logs that record stop-counts.
- The register-judge machinery spawns its own headless sessions on every judged turn; the 5 newest transcript files in the project folder are judge calls. Each such call itself receives the full 8 KB reminder. Two of five produced a JSON offence list; it flagged single-word acknowledgements. The judge edits nothing.
- Doubled reminder: until 23:12 on 2026-07-29 every prompt in every window received the reminder twice (17,120 B of attachments per prompt; visible in home and live-spec transcripts alike). The 23:12 edit of ~/.claude/settings.json ended it. Root-cause guard still owed: scripts/install-session-hooks.sh should refuse to register a hook command that is already present, and a test should assert each hook command appears once.

Suggested definition of done for every rewrite item, replacing counter reports: the file is replaced, a cold reader with empty context retells its rules correctly, and the report to Alexander names the file and its before/after size. Reading logs that only tally findings stop counting as progress.

## 3. Draft replacement for the prompt-time reminder (~270 tok)

> Session rules (live-spec):
> 1. Open every reply with the outcome; detail follows below.
> 2. Plain product words with the human. Internal codes and project metaphors only trail in parentheses at line ends. While work runs, post a short progress line at least every 10 minutes naming the task and its step.
> 3. In chat use the standard industry word in the human's language. Run `python3 scripts/preshow-register-lint.py <path>` on any page before showing it.
> 4. Name things by what they are, in positive sentences. The frame "X, not Y" is banned everywhere.
> 5. The session plans, briefs, and accepts; workers execute. Decision-bearing units go to opus, multi-step mechanical units to sonnet, single-step ones to haiku. Workers locate their own files. A long read that ends in the session's own verdict stays with the session; other long reads go to reader workers who return summaries.
> 6. Before parking an item for Alexander or asking him a question, check whether a written source already answers it (base rules, PRODUCT_SPEC.md, ARCHITECTURE.md, an approved prototype, a past decision). Park only what needs his taste, a policy call, an irreversible act, or a real device — and name which.

## 4. Draft replacements for the 11 skill descriptions (1,599 → 251 words)

- **live-spec-base**: Load before using any live-spec pack skill (spec-author, product-prover, design-reviewer, build-pipeline, test-author, communicator, feedback-intake, feedback-collector, text-audit, publish) or to resolve shared rules and settings.
- **spec-author**: Use to start a new product spec, add a feature to an existing spec, or keep a spec in sync with behavior changes.
- **product-prover**: Use to review, critique, or find gaps in a spec or design document (PRD, HLD, LLD, architecture doc) before it ships.
- **design-reviewer**: Use after a spec is proven to check whether similar features behave consistently and flag ungrouped same-kind items the spec missed.
- **build-pipeline**: Use to run a non-trivial feature, bug fix, or behavior change through the full spec-to-ship pipeline. Not for tiny one-line edits.
- **test-author**: Use to derive a test matrix and write tests from a proven spec and architecture. Not a substitute for reviewing the spec itself.
- **communicator**: Use to show work to a human and ask for a decision, report a milestone, or answer "did we do X". Not for routine narration.
- **feedback-intake**: Use whenever feedback arrives from a person — a comment, answer, file, or reaction — and route it to where it belongs.
- **feedback-collector**: Use, only if enabled, when the user shows a rare, strong reaction (delight or frustration) to offer drafting a private note to the pack's authors.
- **text-audit**: Use to check any human-facing text — README, spec, copy, article — for places a first-time reader gets stuck, then repair them.
- **publish**: Use before work leaves the machine publicly — a public repo, README push, release, or shared skill — to check it meets publish quality.

## 5. Suggested landing order

1. Reminder text (§3) and the 11 descriptions (§4) — biggest per-prompt and per-session relief, both paste-ready.
2. profile.md → flat settings table; CLAUDE.md trim.
3. Skill bodies, one per session, in the order base → build-pipeline → product-prover → spec-author → communicator, each landing as: extract the rule list mechanically, rewrite plain, cold-read twice, replace.
4. Installer guard + single-registration test for hooks (§2).
5. Judge cost review: one judged verdict per turn end instead of per-turn headless judge sessions, and pre-show lint for pages only — proposal, Alexander's word owed.

Questions and comments to the home-window Fable session via this inbox.

## 6. Landed the same night (2026-07-30, on Alexander's answered word)

Alexander answered two questions: remove the per-turn judge temporarily and restore it later; the home window may insert the prepared replacements one time, with global wiring untouched so other windows keep working.

Done, each original at `<file>.bak-2026-07-30`:
- chat-law-hook.sh now prints the short reminder from §3 (8,297 → ~1,800 bytes per prompt).
- register-judge-collect.sh, register-judge-report.sh, midturn-chat-scan.py: disabled by an `exit 0` guard on line 2 with a dated comment. To restore any of them, delete that line.
- ~/.claude/CLAUDE.md (real file: playbook/CLAUDE.md): trimmed to current state only.
- profile.md: rewritten as a flat settings list; the full previous text moved verbatim to playbook/personal/profile-history.md.
- The 11 skill descriptions from §4: applied.

Still open for the live-spec seat: the skill-body rewrites (§5 item 3), the installer guard and single-registration test (§5 item 4), and the decision on the judge's permanent shape (§5 item 5).

## 7. Repo checks that now show red (dependency sweep, 2026-07-30 ~00:35)

Tonight's edits touched INSTALLED copies only; repo copies are unchanged, so the drift checks fire. Verified by running them:

1. `tests/test_config_health.py` (both tests) and `guardrails/check-config-health.sh` (also pre-push): red — installed vs repo drift on chat-law-hook.sh, midturn-chat-scan.py, register-judge-collect.sh, register-judge-report.sh, and all 11 skills (description frontmatter). Fix: decide direction. Adopting tonight's versions means copying the installed files into the repo (hooks/ and skills/) and committing; rejecting them means re-running scripts/install-pack-hooks.sh + scripts/sync-skills.sh from the repo. Alexander's answers of 00:23 back the adopt direction for the judge disable and the short reminder; the disable is temporary by his word.
2. `tests/test_language_rules.py::test_gate_stays_silent_on_the_real_file`: red — guardrails/language-rules.json pins line numbers into the personal profile (~/.claude/playbook/personal/profile.md), which was rewritten and is now ~74 lines. Fix: re-pin rows r01, r13, r47, r49, r50, r51 to the new lines, then `python3 scripts/gen-language-consumers.py`.
3. Same pin mechanism holds line numbers into four skill BODIES (communicator, live-spec-base, spec-author, text-audit) — still green, but any body rewrite must re-baseline those pins in the same change.
4. Fixed on our side already: scripts/open-lane.sh reads the exact key `lanes.cap:` from the personal profile; the rewrite had renamed it, the key is restored (value 3).
5. Note for later: the repo's own founding file `.live-spec/profile.md` shares a name with the personal profile — a standing confusion risk two files carry.
