# Source findings from the readability pilot on the communicator skill

From: the context-slimdown session (readability pilot, 2026-07-30). Found while fresh readers and a rule-record check worked over the communicator skill. These are defects in the source document itself; the rewrite cannot resolve them without inventing rules. Reported for the live-spec window to fix at the source.

1. **Number-context rule conflicts with its neighbor's example.** One rule requires four pieces of context beside every number a report shows. The neighboring rule's own approved example of naming a skipped step shows a bare version number and check count with none of the four. No precedence between the two is stated anywhere.

2. **The status legend ends in an undefined slot.** The status-line legend's final entry is a "docs" slot. Neither the skill, nor its rule record, nor the shared base document says what that slot holds. A first-time reader stops there in every reading round.

3. **The away-stretch rule points at an un-numbered rule.** The rule about ending an away stretch sends the reader to "the show rule (a new window)" without a number. By title that is rule 1; by behavior (opening a window) it is rule 5. The referent is genuinely ambiguous in the source.

4. **(Added 12:14) The design-sync bullet rests on an undefined declaration.** The rule about showing visual work turns on "a landing's declared visual components". Neither the skill, nor its rule record, nor the shared base document says where or how a landing declares its visual components. A reader cannot tell when the bullet applies.

5. **(Added 13:28, from the base-skill rewrite) Two state labels are missing from the style checker's own allowlist.** `CAPS_ALLOW` in `scripts/spec-style-lint.py` blesses WATCHED, OWNED, SOLVED, ARCHIVED, PROTOTYPE — and misses RETIRED and SYNTHETIC, which are the same kind of defined label. Our draft backticks them as a local workaround; adding the two tokens to the allowlist is the root fix.

6. **(Added 13:28) The worker-restore passage can never scan clean.** The passage that SPEC INV-299 and tests/test_worker_restore.py keep word-for-word identical across worker-briefing skills carries 5 sentences over the 25-word cap and 7 emphasis-caps spans; the style scan fires on them in every carrier, including the live base skill today. Needs one policy call: rewrite the passage once across all carriers in one landing, or allow its tokens, or record a dated waiver.

7. **(Added 13:52) The `[default]` mark carries two jobs.** In the communicator skill the same bracketed mark means both "this value was set without the user's word" on a report line, and a tunable figure inside the heartbeat cadence. Twelve self-test readers held the two apart only at a cost, under every phrasing tried. The root fix is one mark per job in the source.

8. **(Added 14:15, from the text-audit chain) The repo owes itself a commit.** skills/text-audit in the repo carries uncommitted working-tree edits to both reference files (human-prose-rules.md r08 tweak; reader-prompt.md regenerated 5→38 stop classes) that are already the shipped installed state, and the repo copy of SKILL.md still carries the old 170-word description the 07-30 slimdown replaced. One sync commit settles all three.

9. **(Added 14:15) human-prose-rules.md violates its own rule r70.** Its hand-written head says two pages carry more than the sheet does, then the list beneath disagrees with that count (docs/language-worked-example.md is named beside the list yet absent from it). The fix is either adding the page to the generator's list or rewording the count — a one-line call.

10. **(Added 14:50, from the base-skill rewrite) Six source defects in live-spec-base**, detailed with record citations in ~/context-slimdown/reports/live-spec-base-read-residue.md: rule 19 cites a "two-strikes law" no clause carries as a name; rule 14's fourth move lives only in build-pipeline; rule 3 (one name per thing) is broken by the file's own four names for one role (lead, orchestrator, seat, senior); rules 28 and 30 each hold a compaction sweep without naming the other; three settings marked `[default]` in prose never reach the defaults table; rule 29's prose names three user-only facts where its gate lists four.

11. **(Added 15:00) The decision page's answer round trip has no remote path.** The page collects answers via a download button and the claiming step reads the Downloads folder — both assume a local seat. The source states remote sessions never open local windows, and never says how the round trip works remotely. Four independent cold readers hit exactly this gap. (Three smaller candidates recorded in ~/context-slimdown/reports/communicator-read-residue.md: one spec code carrying several distinct claims; a scenario written entirely as promised-not-built; the design-sync setting's own definition.)

12. **(Added 15:15) rule-census.py's register column is blind.** It reports `register 0` even when preshow-register-lint.py errors: the lint's JSON record carries no `errors` field, so the census's run_lint reads zero. Reproduced during the base-skill rewrite — a planted register leak passed the census and only the direct lint caught it. Until fixed, any census register verdict is vacuous.

13. **(Added 15:15) The census applies one sentence cap to every surface.** Rule r08 gives spec text a 35-word cap against prose's 25, and the census scores a 29-word spec criterion as over-cap anyway; a 31-word sentence lands in the cap column with zero style/register. The text-audit skill's page contradicts the script it ships. Root call needed: teach the census the spec cap, or state one cap for all surfaces.

14. **(Added 15:15) Fourteen more source-silent items** from the base and text-audit rewrites, each detailed with citations in ~/context-slimdown/reports/live-spec-base-read-residue.md and ~/context-slimdown/reports/text-audit-read-residue.md — including rule 15's unexplained `skip`, rule 23's undefined "mid-turn", rule 21's missing clean-writer mechanism, the intake line with no stated home, and text-audit's "recorded decision" with no location.

15. **(Added 18:34) Five more source-silent items in live-spec-base**, from its final reading round, detailed in ~/context-slimdown/reports/live-spec-base-read-residue.md: rule 12 conditions a push approval on a host-profile setting no settings row carries; rule 19's ledger states are scattered with no single life-cycle statement; rule 33 leans on an undefined "lens"; rule 1's carry-on-alone clause sits unreconciled with rule 12's wait-for-approval; rule 28's compaction sentence has an ambiguous subject.

16. **(Added 19:30, from the communicator audit sweep) The pre-report walk both forbids and requires a question.** Step 6 of the walk says a removal you cannot justify "becomes a question before the report closes"; the standing rule four lines below says "The walk adds no questions to the report". Both sentences are in the source word for word. The only tie-breaker the source offers is that second sentence's own justification, which is about defaults and consent (SPEC INV-31) and so does not reach step 6's case. The rewrite took that reading and named step 6 as the walk's one exception; the source should rule it outright. Three neighbouring contradictions the sweep also raised are resolvable from the source's own wording and were fixed in the rewrite without a ruling: the skill description's "not for routine narration" against rule 13 (the source settles it at "narration marks beats, never a per-command commentary"); rule 6's "never describe the mechanism" against rule 10's "mechanism only after, only if it helps" (what rule 6 bans is the internal machinery doing the talking); and rule 3's show-it-now timing against rule 17's away-stretch (rule 17 already states "this rule governs WHEN"). Each of the three would still read better stated once in the source.

## 2026-07-30, 19:34 — 38 more items the rewrite cannot settle

From the full audit sweep of the communicator skill (~/context-slimdown/reports/communicator-audit-sweep.md). Each of these is a gap in the rule content itself, not in the wording, so the rewrite left the text as it stands. The tag at the end of each line is the sweep's own row, for looking the case up. Grouped by kind.

**Two rules collide and neither is stated as winning (14).**

- Rule 7 wants four things beside every number, and the rules themselves quote roughly a dozen bare figures. Nothing says the rule binds only numbers reported to a user. (N2)
- Rule 13 keeps a NOW/NEXT line current in the chat and rule 18 makes a final line the last thing rendered. Both claim the same slot at a close. (N17)
- The closing beat, the long report and the final line cannot be put in order for one real ending. (N18)
- Rule 10 batches decisions only when more than one waits; rule 17 puts every waiting decision on the stretch page whatever the count. (N19)
- A critical bug that arrives in an inbox file is caught by "interrupts running work immediately" and by "never arrives as an interruption" at once. (N20)
- Rule 3 asks for the user's approval on finished work; rule 10 says the settled defaults ask for no confirmation because silence is consent. The scopes are never separated. (N21)
- Rule 12 says independent steps add roughly no wall-clock time, while rule 9 caps parallel lanes at three. (N22)
- A claims page and a decision page produced on the same day collide on the filename, and the ordinal rule covers only repeats of the same kind. (N23)
- The digest forbids three named things; rule 8 forbids more than three. Which set binds the digest is undefined. (N24)
- A checkpoint is defined as one file per running piece of work, and the same page speaks of checkpoints written per delegated worker. (N26)
- The glossary sends the reader to rule 10 for how to mark a settled pick, and rule 10 gives no such instruction. (N27)
- The `[default]` mark is said to appear in two places, yet rule 13's two-minute cadence is the same kind of host-tunable figure and carries no mark. (N28)
- Synthetic data is restricted to your own checks and must always carry a label, so the label has no reader unless it can reach a shown surface. (N65)
- One sentence treats the Downloads folder as belonging to a project and another as one shared folder on the machine. (N67)

**A term or a value is used as known and defined nowhere (11).**

- The legibility floor names a size threshold for normal text and none for large text, so a reader cannot tell which floor applies. (F4)
- "Decision markers" are listed among the internal handles and explained nowhere. (N31)
- A dossier and a claims page are named as known artifacts with no definition in the shipping unit. (N32)
- The three footprint values — presentation-only, single-module, cross-cutting — are offered as a choice with no definitions. (N35)
- Opus, Sonnet and Haiku each get a stated job; Fable gets only a restriction and no job. (N36)
- The timestamp leading a reply is used as an example of a convention the document never states. (N38)
- Rule 11 lists five records and says every project names them itself, so a reader cannot tell whether the five are names or roles. (N39)
- The units of work — stretch, away-stretch, repeating session, movement, lane, row, beat — never say how they nest. A reader has to invent the hierarchy. (N45)
- Rule 13 says every rule about user-facing language still applies, without naming which rules those are. (N47)
- The rule map says a few rules make sense only together and names one of them. (N48)
- How a skill fires is explained as a moment arriving, which names no actor and no test. (N52)

**A rule states a judgment with no test, measure, or consequence (13).**

- Rule 9 caps parallel lanes at three and says nothing about what happens when a fourth is wanted. (N37)
- A time estimate is drawn from "known shape or past runs", and neither a measure nor a located record of past runs exists. (N41)
- Five rules call something "a defect", and nothing says what a defect costs: a block, a log entry, or disapproval. (N43)
- Rule 3 fires on "a real before/after" and calls waiting "too late", with no test for either. (N54)
- Rule 12 asks for an honest estimate; rule 8 later checks the estimate against the actual, implying a standard rule 12 never states. (N55)
- Rule 22 says to flag inferences most prominently and gives no mechanism, where every other mechanic in the rule is specified. (N56)
- The self-check reads inverted: a question "fails" the test when you can answer it yourself, so a reader applying it literally asks instead of doing. (N58)
- Nothing separates a later genuine change of mind from the third withdrawal the previous sentence says to refuse. (N59)
- "Session memory alone is too weak" gives no standard; the real reason is that a context wipe does not carry it. (N61)
- Step 6 accounts for every removal of substance and never says what counts as substance against ordinary rewording. (N63)
- Rule 5 orders you to detect where you are running and never names the signal to read; the only implied test is the thing that fails remotely. (N64)
- Rule 18's "render that line last, after every tool call" reads both as after each call and as after the turn's last call. (N68)
- Four checkers overlap — the style lint, the pre-show lint, the register lint, the legibility lint — with no statement of which runs when, which the writer invokes, and which blocks. (N78)

Context for verification: the pilot's rule record and reader stop lists live in ~/context-slimdown/ (extractions/rules-communicator.md, reports/communicator-read-r*.md).

## text-audit — source defects found by the skill's audit of itself (added 2026-07-30, 19:45)

The rewritten text-audit body was audited with its own method (report: ~/context-slimdown/reports/text-audit-audit-sweep.md). It returned 11 blocking findings. **Every one of them is present in the source too** — the installed `skills/text-audit/SKILL.md` and, except where noted, the repo copy as well. The rewrite has been repaired and every machine check is green, but each item below still ships from the source until the live-spec window fixes it there. Line numbers refer to the installed copy at ~/.claude/skills/text-audit/SKILL.md.

17. **The self-check section names one of the three numbers the push gate reads** (lines 328-334). It tells the next editor to run `preshow-register-lint.py`, then says `check-doc-findings-bound.py` refuses a push that raises the count. That gate reads the census total — long sentences, style, register — and the register lint reports one of the three. An editor who follows the section exactly sees a clean run and still reds at push. The fix is to name `python3 scripts/rule-census.py skills/text-audit/SKILL.md` in that section and state that its total must read 0.

18. **The `references/` path does not resolve from the root the page names** (lines 21-22, 32, 82, 276, 326). The page says every path is relative to the repository root, then writes this skill's two reference files as `references/…`. There is no `references/` directory at that root — checked on disk — so a reader cannot open the reader-prompt the whole loop turns on. The files really sit at `skills/text-audit/references/`, which the same page writes in full at line 330. One form, written in full, settles it.

19. **The census is printed with no file argument** (line 191). Run as printed, `python3 scripts/rule-census.py` measures the repository's own live set (117 files, 4849 findings today) and never reads the audited file. Every other script on the page is printed with `FILE`, and gate aa's own remedy line prints the argument form. Should read `python3 scripts/rule-census.py FILE`.

20. **Two of the five lints exit red on any text that is not a spec, and the page does not say so** (lines 236, 243). `check-vocabulary.py` and `check-weak-words.py` refuse with the empty-input-set message (INV-218) on a README or an article — reproduced on the draft. The page prints both unqualified, so a reader running the audit as written sees a red they cannot interpret. Either the page says the refusal is not a finding and the grep fallback is the check for such a text, or the two scripts learn to stand down on a text with no glossary and no numbered criteria.

21. **`guardrails/weak-words.json` is missing five of the eleven words the skill names** (line 239-245). The file holds 28 words; *depends*, *related*, *handles*, *based on*, and *corresponds to* are in none of them, while the page calls the file "the fuller list". `check-weak-words.py` reads that file's `weak_words` key and nothing else, so a reader trusting the script never sees those five flagged. **This is the one item whose real fix is a source-side data change** — add the five to the JSON. The rewrite could only narrow the claim, which it did: it now says the prose names classes and the file holds the words it has learned, and names the five the grep fallback has to catch.

22. **The closing rule is stated one cycle short in the section a reader consults to stop** (line 289): "The loop closes on zero blocking findings." Lines 116 and 131 both say two consecutive clean reads, and `docs/spec-format.md` line 76 records that pattern. A stranger acting on line 289 ends the audit a full cycle early. Line 336's "one cold-reader loop" reads the same way.

23. **A design review is routed to two different skills.** Line 104 sends it to product-prover; line 344's roster says design-reviewer "judges the design the spec describes". The pack's own descriptions settle it — product-prover reviews and finds gaps in a spec, design-reviewer runs after a spec is proven to check that similar features behave consistently — and neither sentence on the page says that. The rewrite kept the source's assignment (product-prover) and restated the roster line from design-reviewer's own description.

24. **The four structure checks are printed against live-spec's own documents** (lines 184-190). All four hardcode `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md` and `TEST_MATRIX.md`, while line 229 says the audited path may lead anywhere on disk. Run as printed while auditing another project, they check live-spec and return a pass that says nothing about the audited text — and the auditor records it as a pass. The freeze check and the index check also apply only where the audited project keeps the same three guarded documents.

25. **`docs/language-defects.md` is claimed to record what each reading returned** (lines 44-45). That document opens by saying it is the record behind the rules — why a given rule says what it says. The readings themselves live under `docs/language-reads/`. As written, the auditor writes reading results into the wrong file.

26. **The file breaks its own one-name lint in six places, and `check-one-name.py` cannot see any of them.** The pairs: requirement-shape lint / requirements genre (151, 253); the mechanical lints / the mechanical layer (223, 251); a real hole / a genuine hole (173, 315); the person / the human, for one role (57, 347); cold reader / fresh reader / fresh session / fresh agent across the loop; and the three requirement-shape points printed twice word for word (153-154, 253-255). `guardrails/one-name-aliases.json` holds 5 artifacts and 13 aliases, none of these, so the gate passes on the file that defines the rule. Root fix: settle one name per thing in the source and add the settled pairs to the alias file, which is what the skill's own page instructs for a new weak word.

27. **The installed copy's slimmed description reds gate aa on install.** Item 8 above already records that the repo copy still carries the pre-slimdown description. New fact: the slimmed one-sentence description in the installed copy joins with the frontmatter's opening lines into a 26-word census sentence, so installing it into the repo returns `FAIL (doc-findings-bound): skills/text-audit/SKILL.md was repaired to zero and now carries 1 finding(s)` — reproduced against a scratch tree. Whatever description lands at the sync must be measured with `rule-census.py` first, counting the `--- name: … description: …` join.

28. **(Added 20:05) `--compaction` is printed on a `--freeze` command, where it does nothing.** Both the source (line 202) and the draft print `python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`, and the page never says what the flag does. Reading `scripts/spec-freeze.py`: `--compaction` is consumed only on the `--verify` branch (line 202 of the script, passed to `verify(...)`), where it allows an anchor-count drop when the anchor survives a removed duplicate row. The `--freeze` branch ignores it entirely. So the command the skill teaches carries a flag with no effect at that call site. Two things are owed by the script's owner: state what the flag does where the page can cite it, and settle whether the freeze command should carry it at all.

29. **(Added 20:05) The old-vs-new second reader is briefed from nothing.** After a spec section is repaired, the skill sends a second reader to put the old text and the new text side by side and report every difference in meaning. The cold reader gets a shipped artifact for its brief, `skills/text-audit/references/reader-prompt.md`; this second reader gets a one-sentence description and no artifact — checked, `skills/text-audit/references/` holds two files and neither is such a brief. Two auditors will therefore brief this reader two different ways, and the check is the one that guards against meaning loss during a rewrite. The fix is a pack deliverable: a second prompt file beside the reader-prompt, or a named section of the existing one.

## live-spec-base — defects the repair could not resolve without inventing a rule (added 2026-07-30, from the audit-sweep repair)

The rewritten live-spec-base body was audited (report: `~/context-slimdown/reports/live-spec-base-audit-sweep.md`) and then repaired: the eight changed obligations were put back to the source's force, and 59 passages the project's own tests quote were restored byte-identical (`~/context-slimdown/reports/live-spec-base-restored-passages.md`). Four items below are carried by the source itself, so the repair could only make the wording truthful about who judges. They still ship from `skills/live-spec-base/SKILL.md` until the live-spec window settles them.

30. **Rule 5's independent-checker trigger has no measure.** The source reads "A large or high-stakes landing earns an independent fresh-context checker beyond that re-check (SPEC INV-46)". Nothing says what makes a landing large or high-stakes, and the sentence decides whether the checker runs at all, so two sessions draw the line differently. The repair added one truthful sentence naming the judge — the seat's own call, made when it routes and named in the delivery report — and stated plainly that no measure sits behind the two words. A real fix is a stated trigger, or a threshold the delivery report can be held to.

31. **Rule 25's glance boundary has no measure.** The source reads "A glance is bounded: one small file, or a handful of targeted lines whose result IS the deliverable". Small relative to what, and a handful counted how, are unstated, and this is the line deciding whether the lead reads a file itself or must dispatch it. The repair named the judge (the lead, with the delegation accounting recording which side a read fell on) and said no measure sits behind the words. A real fix is a number, or a named test.

32. **Rule 31 uses "owner" for two different actors.** Inside one rule the word means the owning *agent* ("the zone's owner is presumed competent and informed") and the *person* ("a new agent the owner ratifies", "the third crossing goes to the owner"). The data-and-contracts law turns on it: "Every field in that artifact leaves the producer's tree on the owner's explicit permission". The rewrite had ruled that an owning agent is never the user, which moved a data-release approval from the person to a neighbouring agent; that ruling has been removed and the source's wording restored, with one derived sentence added — the permission rides rule 12's publishing gate, so it is the user's own word. The source should say which actor each "owner" is, once. This also breaks rule 3 (one surface, one name).

33. **Three more the repair left standing, all present in the source.** The `worker.tiering` settings row offers "fixed tier per size class (SPEC D-2)" while rule 5 says size is a weak hint and never the decider — two live sentences giving opposite instructions. The `lanes.cap` row writes a person-specific value into the file ("the user's 2026-07-06 value of three lives in the personal profile") after the file forbids exactly that. Rule 5's tier-override log names a format and no destination; the repair named the row's delivery report as its home in the draft, but the source still names none.
