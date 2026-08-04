# live-spec-base — leftovers from the readability rewrite that need a ruling at the source

From: the context-slimdown session (readability pilot, 2026-07-30, 21:10). Born of the sender's own
blocked work: the rewritten `skills/live-spec-base/SKILL.md` body was audited and repaired
(`~/context-slimdown/reports/live-spec-base-audit-sweep.md`,
`~/context-slimdown/reports/live-spec-base-restored-passages.md`,
`~/context-slimdown/reports/live-spec-base-leftovers-triage.md`). Sixteen findings were left standing
after that repair. Seven of them cannot be closed in the rewrite: each needs a rule the source does not
state, or a change to shipped identifiers and headings. They ship from the source today.

Numbering continues `2026-07-30-communicator-source-findings.md`, whose last item is 33. Two leftovers
are already filed there and are not repeated here: the `worker.tiering` size-class row, the `lanes.cap`
person-specific clause and the unnamed tier-override destination are item 33; the seat's four names
(lead · orchestrator · seat · senior) are item 10.

34. **Rule 24 sends the reader to two settings the defaults table has no rows for.** The rule tells a
    project to declare "one `project.layers` line and one `project.proofs` line" in its host profile.
    Neither name appears in the Package defaults table, which carries a row for every other setting the
    rules name, including `project.kind` and `project.design-principles` beside them. A reader told to
    write the two lines has no default, no scope, and no settings-card verdict to write them against.
    Either add the two rows, or say in the table's lead that a kind's own declarations ride
    `project.kind` rather than standing as rows of their own. The rewrite could do neither without
    inventing the defaults.

35. **Rule 29 breaks the pack's own one-name lint, twice.** `python3 guardrails/check-one-name.py
    skills/live-spec-base/SKILL.md` exits 1 today: "line 337 references `backlog item` as `work item`"
    and the same at line 348 (INV-255). The canonical name in `guardrails/one-name-aliases.json` is
    `backlog item` and `work item` is a listed alias. The rewrite wrote `backlog item` in both places
    and now exits 0; the source still reds, and rule 3 is the rule it breaks.

36. **Two rules name two homes for one fact, after rule 4 makes one home the law.** Rule 14: "the full
    four-move law lives in build-pipeline's bug entry and the spec's bug scenario (SPEC INV-124)". Rule
    26: "This rule is the base home the design-principles invariants own. Their full statement and
    per-kind starter sets live in ARCHITECTURE.md." Rule 4 says every mention past the one canonical home
    is a pointer. As written, a reader cannot tell which document to edit when the rule changes, or which
    wins when the two disagree. Naming the canonical home is a ruling only the pack can make, so the
    rewrite kept the source's wording.

37. **Rule 33's release-gate requirement is hedged, so a reader cannot tell whether it binds.** "A
    release gate may require a dated clean-context review record naming a seat other than the release's."
    The next sentence then describes that gate's three checks as though the requirement is live. A
    reader cannot tell whether a release with no such record can ship, or who decides. Say it in the
    active voice: the gate requires the record, or a host's gate may be configured to.

38. **Rule 30 claims an enforcement the file's own text takes back three times.** Rule 30 says every
    machine-verifiable quality runs as a blocking gate "held by no attention". Rule 32 calls its own
    release-number judgment "held by no machine"; rule 33 says whether a review was truly clean-context
    "is a process fact no gate fully sees"; rule 35 says whether the writing agent was fresh "is a fact
    no machine sees". A reader cannot tell how much of the method a machine holds and how much is
    remembered. The repair is one sentence in rule 30 stating its own exception — some rules the pack
    states have no machine behind them yet — with the three passages pointing at it instead of each
    conceding on its own. That is new rule text, so the rewrite left all four as they stand.

39. **The settings table keeps a dotted scope prefix for thirteen rows and drops it for three.**
    `trust`, `design-sync` and `feedback-upstream` carry no prefix; every other setting does
    (`language.docs`, `proactivity.mode`, `worker.tiering`, and the rest). A reader reads the split as a
    grouping and cannot resolve it. Either give the three a prefix — a rename of shipped identifiers that
    profiles and guardrails read, so a pack change — or say in the table's lead that the prefix carries no
    scheme.

40. **The heading "Work that belongs elsewhere" promises destinations the section does not give.** The
    section says what does not belong in the file and names only profiles and an unnamed general style
    guide as homes. Either the heading becomes what the section does — "What this file does not hold" —
    or the section names the destinations, starting with the style guide. The heading is shared with the
    rewrite and the readability project's structure gate compares headings between the two, so the
    rewrite cannot change it alone.

41. **The text-audit skill and `docs/language-defects.md` name two different jobs for the same file.**
    The skill's rewritten line reads: "written to a dated reading record under `docs/language-reads/`,
    and `docs/language-defects.md` records what each one returned" — naming it a log of what every
    reading turned up. The file on disk opens instead as "the record behind the rules this project
    states about its own writing... it answers one question: why does a given rule say what it says."
    One page cannot be both a running log of reading results and a record of a rule's origin without
    saying how the two relate; a reader following the skill's line to the file meets a purpose the file
    does not state. The sentence stood in the source before the rewrite touched this skill, and the
    rewrite kept its meaning under the repair rule, so the conflict is the source's to resolve: name
    which job the file holds, or split the two.

Context for verification: the rewrite, its per-finding triage, and the byte-identical passage list live
in ~/context-slimdown/ (drafts/live-spec-base-full.md, reports/live-spec-base-leftovers-triage.md,
reports/live-spec-base-restored-passages.md).

42. **guardrails/language-rules.json has no write coordination.** Two sessions wrote the file within
    eleven seconds of each other (2026-07-30, ~21:55) — the live-spec window running a line-pin sweep
    over the personal profile, and the context slim-down campaign re-pointing twenty-four pins for the
    text-audit install. The campaign's write used a hash compare-and-swap and verified all twenty-four
    targets against the other session's new content first, so nothing was lost this time. The finding is
    that the file has no write coordination: the next collision can silently drop one side's pins, and
    the pins' own checker stays green on stale pins, so the loss would not surface. A coordination rule
    or a lock is needed.

    `docs/language-rule-coverage.md` is generated output holding the same pins and currently shows
    pre-install numbers; its checker exits 1. That red predates the install and clears itself on the
    next generator run — no hand-work is owed, recorded here so nobody re-diagnoses it.

Items 43-46 come from the same campaign's build-pipeline rewrite (2026-07-30, 22:30), filed at the
question triage of `~/context-slimdown/drafts/build-pipeline-full.md`. Each is a defect in
`skills/build-pipeline/SKILL.md` as it ships today; the rewrite kept the source's meaning and changed
nothing the source does not already say.

43. **The footprint rule says what does not size the reach without naming it.** The intake section
    reads: "the footprint sizes the reach, and the size does not". Nothing on the page says which size
    is meant, and the intake line above carries a field literally called size, so a reader lands on the
    wrong antecedent. The repo answers it elsewhere: `docs/restyle-repoint-log.md` records the same law
    as "the footprint sizes the reach, and the change's raw size does not". Say that in the skill.

44. **The skill sends the reader to a cadence it never defines.** The commit-and-show step ends "a slow
    gate is watched to its verdict on the detached-work cadence (SPEC INV-106, INV-35)". The cadence is
    defined only in `PRODUCT_SPEC.md`'s glossary — a start line, a beat about every two minutes or at
    each stage, a closing digest. A skill is read on its own, so the rule as written is unrunnable
    without the spec beside it. Either gloss the cadence in the skill or cite the glossary entry.

45. **A promise rides an unnamed follow-on row.** The footprint parenthetical says the
    declared-module-interface and interface-level test machinery "rides its own follow-on row". No row
    number stands beside it, so nobody can check whether it landed or died. Name the row.

46. **A spec-backed literal sits in the skill's prose with nothing marking it.** `test_request_classifier.py`
    reads build-pipeline's own INV-153 sentence and requires a count word before "times" equal to the
    control set, which is four. The sentence carries no sign that the number is load-bearing, and the
    rewrite drafted "All three are stated together as SPEC INV-153" in good faith — that phrasing reds
    the suite. Mark the literal, or have the guard name the sentence's home in its failure message.

Items 47-51 come from the third repair pass over the live-spec-base rewrite (2026-07-30, ~22:30),
answering the second audit sweep (`~/context-slimdown/reports/live-spec-base-audit-2.md`). Each is a
defect in `skills/live-spec-base/SKILL.md` as it ships today. The rewrite's own additions around them
have been removed, so what is left is the source's to rule on.

47. **The rule of thinking cites a repair that landed, as though it were still owed.** The paragraph
    closes "(proven by probe, 2026-07-17; the repair is ROADMAP row 416)". Row 416 no longer sits in
    `ROADMAP.md`: `docs/queue-archive/rotated-ROADMAP-2026-07.md` carries it as "landed 2026-07-17,
    folded into one landing with row 418", and its body records the meaning-reading judge shipping
    beside the literal list. A reader of the top rule of the file is told the pack's own class-judging
    guard is a plan. Say what shipped, or cite the archived row as landed.

48. **Six of the eight roadmap rows the file cites have rotated out of the roadmap.** Rows 217 and 247
    are live in `ROADMAP.md`. Rows 216, 253, 254, 403, 414 and 416 are not — every one of them sits in
    `docs/queue-archive/rotated-ROADMAP-2026-07.md`. All six citations ship in the source today (rule
    22's "rows 216/217", rule 23's "rows 253/254", the `far-tier.surface-cadence` row's ROADMAP 403 and
    ROADMAP 414, and the rule of thinking's row 416), so a reader who follows any of the six finds
    nothing at the name the file gives. Either repoint the six at the archive, or state once that a
    landed row rotates there. The rewrite now states the rotation in its own words and left the six
    citations untouched, because repointing them is a change to what the source claims.

    Row 414 is a second defect underneath the first. The `far-tier.surface-cadence` row cites it for the
    person's own cadence; the archived row 414 reads "The pack asks what the person's plan affords, and
    the lane count reads off the answer" — the lane-cap row. Row 403, cited in the same cell, is the one
    that carries the far-backlog surfacing law.

49. **The rename to one name for the person cannot finish inside a rewrite, because two passages are
    pinned by tests.** Rule 3 asks for one name per surface. The file calls the person "the human" in
    rule 14 ("escalate to the human when the class boundary needs his read"), in rule 29 (the
    "needs-the-human's-word marker") and in rule 31 ("A human asker is answered in chat in one
    sentence"), and "the person" elsewhere. `test_class_hunt.py` and `test_request_classifier.py` pin the
    first two strings literally, so settling the name means re-pinning tests, which is a pack change. The
    rewrite says plainly that a few rules still read "the human" and mean the same person. Settle the
    name once and move the pins with it.

50. **Rule 2 bans two handle kinds from the talking role that the file's own rules then use.** Rule 2
    lists "INV-x, row numbers, worker names, model names, coined feature names or metaphors" as handles
    that never do the talking. Rule 5 routes "a one-shot with no decision to haiku, multi-step mechanical
    work to sonnet" — model names in the talking role. Rule 32 writes "the row-247 inbox arm", and the
    rule of thinking writes "the repair is ROADMAP row 416" — row numbers in the talking role. A reader
    cannot tell whether rule 2 binds the pack's own rulebook. The honest repair is one clause in rule 2
    saying the rulebook is read by the agents it routes and by its maintainers, so it names the tiers and
    the rows it works in; the alternative is rewording rules 5 and 32. The rewrite had added both an
    anti-exemption clause in rule 2 and a concession in rule 5; both were its own inventions and both
    have been removed, leaving the source's silence.

51. **Update to item 32 of `2026-07-30-communicator-source-findings.md` — rule 31's two owners.** That
    item recorded the rewrite carrying one derived sentence: the permission to release a field rides
    rule 12's publishing gate, so it is the user's own word. The sentence has now been removed. It
    defined "the owner" as the person inside the data-and-contracts law, while three later passages need
    the word to mean the agent that owns the zone — "a new agent the owner ratifies", "stays a proposal
    until the owner ratifies it", "an owner-initiated message is the one kind that carries the owner's
    authority". Whether releasing a neighbour's data needs the person's word or the owning agent's is now
    unanswered in both the source and the rewrite, and it is the heaviest act in the rule. The pack owes
    the ruling; item 32 stands as filed, minus the derived sentence.

52. **URGENT: sync-skills.sh will silently replace text-audit rewrite with stale repository copy.** The
    rewritten text-audit skill was installed tonight into `~/.claude/skills/text-audit/SKILL.md`
    (25,969 bytes), while the repository source `~/live-spec/skills/text-audit/SKILL.md` still holds
    the old 22,785-byte text. `sync-skills.sh` copies repository → home, so one run of it silently
    replaces the rewrite with the old text. The same hazard already applies to the chat hook, whose
    installed copy diverged from its source in the pack earlier in this campaign. Nothing is lost if it
    happens — the campaign holds byte-identical copies of every installed rewrite in
    `~/context-slimdown/drafts/` — but the overwrite would be silent and nobody would notice until the
    old wording surfaced in behaviour.

    Two fixes are needed: (1) bring the repository sources into line with the installed rewrites (the
    campaign will hand over the exact files on request), and (2) add a check that compares installed
    against repository copies and turns red when they diverge, so the next divergence announces itself.

53. **The text-audit skill has no check for consistency across a document, so contradictions and redefinitions pass every gate.** The skill's method is a cold-reader pass: a stranger reads the document straight through and marks stops. That finds single-spot readability breaks but cannot compare two distant passages against each other. Evidence (`~/context-slimdown/reports/consistency-check-coverage.md`): name drift is caught by rule r04's alias-list script, but only for known pairs; an unlisted drift, a contradiction between two rules, a term redefined with a different meaning partway through the document, and a stale pointer (a reference whose target no longer backs the claim) have no rule among the 63. Tonight's proof: the rewritten live-spec-base carried two sentences giving opposite instructions on a single topic, and a term redefined to mean two different things in two places; both passed all gates. They broke only when an adversarial audit was commissioned by hand. The pack's method says every mistake gets a rule; this class gets none. Ask for a rule class and a checking script. Meanwhile the context slim-down campaign is running its own consistency pass across the edited document — a registry of every term whose definition an edit changes, swept across the whole file; a record of every pointer with targets verified; and a contradiction check over the edited units — which the window is welcome to take as a starting shape if useful.
