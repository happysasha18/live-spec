# Prover record — 2026-08-17 the slimming packet and its architecture pin renumber

PUSH-REVIEW

This record covers the integration of the three-commit slimming packet onto `origin/main`, and the
repair the review demanded of it. The packet moves reference material out of three skill bodies
without rewriting a word of it, so `ARCHITECTURE.md` had to follow the text with new line numbers.
That renumber is what obliges this record: `M-6`/`INV-116` want the prover pass to cover the
architecture, and the packet as it arrived carried none.

Range: 9efe559..113f11f (base 9efe559, the remote head; nine reviewed commits listed below; this
record's own commits follow them and touch `docs/prover/` alone, which gate a exempts because a
record cannot name the commit that first ships it. `113f11f` and `3905f7f` touch `docs/skill-review/`
alone and are exempt by the same clause, and are listed anyway because the range owes them a name.)
- 113f11f The three skills carry a second-pass skill-creator review, taken after the findings landed
- 0ab4b05 The shipped chat-law hook keeps all seven laws for every host; the owner's shortening lives
  only in his installed copy — the revert of ed7c3bf, argued at item (5) of the word below
- ed7c3bf The repo's chat-law hook is the copy this machine runs — REVERTED in 0ab4b05
- 94ae4c3 The reviews' findings land: firing conditions and the reading key return to the bodies
- 3905f7f The three slimmed skills carry their skill-creator reviews, each allowing with findings
- 2139bad The census keeps the three untouched entries as the last landing recorded them
- cb26b70 communicator: the rule histories move to references, word for word
- 88c4622 build-pipeline: five reference sections move out of the body, word for word
- 5295b06 live-spec-base: the glossary and the worked examples move to references, word for word

Files read: `ARCHITECTURE.md` in full and its diff line by line; the three bodies
`skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md`, `skills/communicator/SKILL.md`
before and after; the eight new reference files `references/glossary.md`,
`references/worked-examples.md`, `references/architecture-step-detail.md`,
`references/footprint-read.md`, `references/lanes-and-pen.md`, `references/mockup-first-entry.md`,
`references/verify-step-detail.md`, `references/rule-histories.md`, and the grown
`references/delegation-protocol.md`; `guardrails/rule-census.json` against its 9efe559 copy entry by
entry; `guardrails/node-file-cap.json`; `guardrails/check-prover-record.sh`,
`guardrails/check-config-health.sh`, `guardrails/check-tests.sh`, `guardrails/check-pin-drift.sh`;
`tests/test_guardrails.py` `TestGateA_ProverRecord` and `TestGateB_Tests`;
`tests/test_progress_report.py`; `tests/test_worker_restore.py`; `docs/prover/README.md`.

Checks run: `check-pin-drift.sh` — exit 0, 207 pins proved (65 line pins against their own line, 136
file-level, 6 unlabelled) plus 53 r5 range pins; the five architecture test files
(`test_architecture_format`, `_pins`, `_prove_seam`, `_proved_at_full_pass`,
`_redesign_owes_rework`) — 24 passed; `check-skill-loadability.sh` — exit 0, 11 skills;
`tests/test_rule_census_ratchet.py` — 8 passed; `check-doc-findings-bound.py` (gate aa) — exit 0,
137 live documents, 26 held at zero, none above its record; the focused integration set of twelve
files — 381 passed, 1 failed, 2 skipped; `python3 -m pytest -q tests/ --deselect
tests/test_guardrails.py` — **2,396 passed, 3 failed, 53 skipped, 78 deselected, 1 error** in 3
minutes 19 seconds; `tests/test_guardrails.py` alone — **76 passed, 2 failed** in 20 minutes 46
seconds; and a word-for-word audit of the move itself, described under Findings.

Findings: one blocking, closed below, and five notes. The move's central claim — that the text
travels unchanged — was tested rather than taken on trust. Every `.md` file under each of the three
skill directories was concatenated at 9efe559 and again at cb26b70 and compared as a word stream:
of 504, 501 and 461 sentences of eight words or more, the handful that did not survive a literal
match all proved to be my own splitter joining a heading across the seam where a section was cut,
and each was then found present verbatim by fragment search. No sentence of the moved material is
lost or reworded. The three bodies fall 56,083 to 52,466, 64,143 to 52,432 and 45,861 to 44,881
bytes; the eight new files hold 22,090 bytes; the code route, base plus build-pipeline, falls
120,226 to 104,898 bytes.

Blocking: two, argued in full below.
- closed: 2139bad returns the three untouched census entries to the values 9efe559 recorded.
- closed: 3905f7f commits the three skill-creator reviews gate s demanded; all three allow the change
  and all three carry findings, listed under that finding below.

1. **The census recount rewrote three entries the packet never touched.** In 5295b06 the rebuild of
   `guardrails/rule-census.json` carried three files' byte counts along with it: `PRODUCT_SPEC.md`
   702,954 to 703,125, `TEST_MATRIX.md` 484,277 to 484,267, and
   `docs/audits/2026-08-07-number-census.md` 31,991 to 32,027. None of the three is edited anywhere
   in this range. Their drift belongs to an earlier landing, and a slimming packet silently
   restating another change's numbers puts them beyond the reach of whoever owns them.
   closed: 2139bad returns exactly those three `bytes` fields to their 9efe559 values and nothing
   else — three lines, the entries then byte-identical to the base copy field by field. The ratchet
   and gate aa are green over the restored file.

2. **The three changed skills owe a skill-creator review record, and the packet brought none.** Gate s
   (SPEC INV-208) holds that a substantively changed skill carries a committed record under
   `docs/skill-review/` whose verdict is at least as new as the skill's own last change. All three
   bodies this range edits are named: `build-pipeline` last changed in 88c4622, `communicator` in
   cb26b70, `live-spec-base` in 5295b06, and no record covers any of them. Moving text out of a body
   into its references is not the version-stamp bump the gate exempts by construction.
   closed: 3905f7f commits three records written by three independent reviewer agents, one per skill,
   each reading against the skill-creator discipline installed at `~/.claude/skills/skill-creator` and
   each verifying the word-for-word claim itself rather than taking this record's word for it. All
   three return ALLOW WITH FINDINGS; none refuses. Their findings are real and are listed here rather
   than left in the records, because two of them are defects this range introduced:
   - `references/lanes-and-pen.md` carries the drafter-applier link verbatim from the body, where
     `references/drafter-applier-example.md` was the correct path. From inside `references/` it
     resolves to `references/references/…`, which does not exist, and that broken link is now the
     ONLY mention of the file anywhere in the skill. A reference file reachable in one hop before this
     range is reachable in none after it. I confirmed this independently with grep and `ls`.
   - The communicator move filed an imperative as history. "Do NOT rely on the harness's own task list
     or spinner for this: a browser-seated session never shows them…" now exists only in
     `references/rule-histories.md`; the body keeps the weaker "never the status's home" without the
     fact that makes it obeyable. Confirmed by grep across the body and all five reference files.
   - live-spec-base moved its own reading key. "The four names mean the one session" — the only
     sentence in the repository telling a reader that seat, senior, orchestrator and lead are one
     session — now sits in `references/glossary.md` behind a pointer that says to open it when a term
     is being resolved. The body goes on using the other three names eleven times. Confirmed by grep
     over the whole tree.
   The three reviews also name work that is owed rather than broken: no conservation test guards the
   build-pipeline or live-spec-base moves the way `tests/test_communicator_body_thinned.py` guards the
   communicator's; the audit's high-stakes firing condition and the node fitness test's three
   questions left the build-pipeline body while their names stayed; and the appended block in
   `references/delegation-protocol.md` restates six invariants the file already carried. Gate s is
   green over the three records. The findings above are the honest state of the range, not a reason
   the gate should have stayed red.

   reopened and closed again: `94ae4c3` landed the findings' repairs AFTER those three records were
   written, which made every one of them stale by the gate's own freshness rule — a record must be at
   or after the skill's last change, and all three now sat behind it. Gate s reddened a second time on
   all three skills. `113f11f` closes it with a second pass: three fresh reviewer agents, one per
   skill, each reading the CURRENT body against the same installed skill-creator discipline and each
   verifying `94ae4c3`'s delta itself rather than taking this record's account of it. All three again
   return ALLOW WITH FINDINGS. What they confirm: the three-question fitness test and the audit's
   high-stakes firing condition are back in the build-pipeline body byte-identical to their 9efe559
   wording, with both reference files rewritten rather than trimmed so the return introduced no new
   duplication; the drafter-applier link resolves and that reference is reachable again; the
   harness-panel imperative is back in the communicator body and exists in exactly one place; and the
   live-spec-base reading key is back beside the glossary pointer. What they refuse to call cured:
   `references/delegation-protocol.md` still states the per-block root and plan-line accounting duty
   twice within twelve lines (`:96` and `:108-110`), which predates 88c4622 and survived `94ae4c3`'s
   cleanup; the communicator's four provenance pointers still over-claim, and its rule-13 pointer now
   names the harness panel's standing as living in `references/rule-histories.md` when `94ae4c3` moved
   exactly that back into the body, so the pointer describes content its target no longer holds; and
   `guardrails/rule-census.json`'s `delegation-protocol.md` entry has its `total` updated to 53 while
   its `reason` still narrates a rise "52 to 58". None of the three reviewers judged any of these
   blocking, and none is left unnamed here.

## What the push gate said, run in full

`bash guardrails/pre-push < /dev/null` over this tree at 434f1b9: **PUSH BLOCKED**, 1,496 seconds,
29 gates. Four reds, and they are not one class:

- **gate a** reddened on THIS record, and the defect was mine. The blocking field read
  `Blocking: one, closed in 2139bad.` as a lone line, and the gate's parser reads the field only as
  far as the first blank line and wants the literal token `closed:` or `stands:` in what it finds.
  My own check had run `check-prover-record.sh` without `--push`, which never reaches that arm, so I
  certified a shape the real gate rejects. The field is now bullets directly under it, the shape the
  house already used.
- **gate s** reddened on the three missing skill reviews — blocking finding 2 above, closed in 3905f7f
  and re-run green.
- **gate b** reddened on five tests. Four are machine-local and reproduce identically at the base
  9efe559 in a second worktree: `test_config_health` twice, `test_judge_listed` once — that one reds
  because six judges declared wired to Stop and UserPromptSubmit are absent from this machine's
  `~/.claude/settings.json` — and the worker-restore transcript gate. The fifth,
  `TestGateB_Tests::test_real_content_passes`, also reds at the base, and reds there for the same
  single inner test. None of the five is this range's work.
- **gate m** reddened on the same machine state from the other side: the installed copies of the
  three slimmed skills, plus a `chat-law-hook.sh` hook drift that predates this range entirely.

One of the four machine-local reds turns out to have a repo side, and that side stops at the
specification's door. `test_judge_listed` reds because the owner unwired six judges on 2026-08-17 —
the whole Stop surface and the register judge's report arm — while `guardrails/judge-hooks.json` still
declares all eight as wired. Bringing the declaration to the fact is the honest repair, and it does not
fit in one commit: `PRODUCT_SPEC.md` R230.4 [INV-203] requires a Stop arm to dispatch and a
prompt-submit arm to report, R293 says a Stop-hook scan "now reads the turn", R294.4 has the setup walk
install the code-anchor scan, and R232's title names two Stop-hook soft signals. Ten rules in
`guardrails/language-rules.json` carry a `session-stop-hook` arming that would become false, two of
them (r12, r14) falling to `stated-only` with no catcher left, which forces a rebuild of the four
generated language pages. Editing a requirement is not this worker's to do, so the declaration stands
as it is and this record names the gap rather than closing it quietly. ROADMAP row 543 already owns
the question of what those scripts permanently become.

## The owner's word on the machine-local reds

Recorded here because a gate loosened without a recorded reason is a gate turned off. The word was
given on 2026-08-17 in the evening and relayed through the coordinator's window; it is reproduced in
the language it was given in, since a translated permission is a paraphrased one.

> Slovo vladel'tsa, 2026-08-17, vecher, iz okna koordinatora: push paketa razreshon pri mashinnykh
> krasnykh etoy mashiny — (1) config-health x2: dreyf ustanovlennykh kopiy, lechitsya
> scripts/sync-skills.sh srazu posle sliyaniya (ego razreshenie togo zhe dnya); (2) transkriptnyy
> worker-restore: sluzhebnyy git stash podgotovitelya 15:33Z, okno istekaet 2026-08-18 15:33Z;
> (3) vlozhennyy TestGateB::test_real_content_passes: predsushchestvuyushchiy, dokazan na baze
> 9efe559; (4) test_judge_listed: pryamoe sledstvie ego prikaza togo zhe dnya snyat' fonovykh sudey
> v ~/.claude nemedlenno ("voobshche vse pravki mozhesh' khot' seychas sdelat'", "na vse soglasen");
> repozitornoe prizemlenie otstavki — otdel'nym paketom po stroke 543;
> (5) gate m, chat-law-hook: ustanovlennaya kopiya namerenno koroche istochnika v repozitorii — ego
> prikaz ot 2026-08-17 o ego lichnom byudzhete konteksta. Istochnik v repozitorii khranit vse sem'
> zakonov dlya lyubogo khozyaina; repozitornyy mekhanizm deklaratsii etoy raznitsy
> (guardrails/local-overrides.json) prikhodit utrennim paketom.

In English, for a reader who does not read the original: the push is authorised over five
machine-local reds — the installed-copy drift, which `scripts/sync-skills.sh` repairs immediately
after the merge under the same day's permission; the transcript worker-restore finding, which is the
preparer's own service stash at 15:33Z and ages out of the gate's window on 2026-08-18 at 15:33Z; the
nested `TestGateB::test_real_content_passes`, pre-existing and proved so at the base;
`test_judge_listed`, which is the direct consequence of the same day's instruction to unwire the
background judges immediately, with the repository-side retirement landing as its own packet under
ROADMAP row 543; and gate m's `chat-law-hook.sh` drift, which is deliberate — the installed copy on
this machine is the owner's own shortening, ordered on 2026-08-17 against his personal context
budget, while the repository source keeps all seven laws for every other host that vendors the pack.

That fifth item is why `ed7c3bf` is reverted inside this range rather than left standing. It had
copied the owner's shortened personal hook INTO the shipped source, which would have exported one
machine's context budget to every host the pack reaches; `0ab4b05` puts the 5,866-byte source back.
The drift the gate reports is therefore the intended end state, not an oversight, and the repository
already owns the mechanism for declaring exactly this: `guardrails/local-overrides.json` pins a
fingerprint, a reason and a review date for an installed hook kept deliberately different, and
`guardrails/check-config-health.sh` stands the red down for the copy an entry names. No entry is
written here, because writing one requires the installed file's fingerprint and a review date, and
that is the morning packet's work, not this range's. Until it lands the red stands, named.

**Two further findings on the transcript gate are the preparer's own, and the owner's word above does
not name them.** They are recorded here in full rather than absorbed, because base rule 7's
worker-restore sub-rule binds a worker in every tree including its own worktree (INV-298), and
because the word above was given against a gate reading one finding.

- `a955b441e703af7f6`, 17:41Z, in this worktree: `git checkout HEAD -- guardrails/rule-census.json`,
  run while rebuilding the census. Nothing was lost. The bytes discarded were the preparer's own
  regenerated census, deterministically reproducible from `scripts/rule-census.py`, and the file was
  rebuilt by WRITING its bytes rather than by a git-level restore — the repair the rule prescribes.
- `ac85659f2aac49789`, 15:54Z, in `/private/tmp/live-spec-slimdown/wt`:
  `git checkout -- .live-spec/r5-rule-prices-2026-08-11.md`, by the same run whose 15:33Z stash the
  owner's item (2) names. Same class, same day, same preparer lineage.

The decision to carry these two into the push rather than halt on them was taken by the coordinating
session, not by the owner. He was not asked about them and has said nothing about them, and this
record claims no word from him on either. A delegation covering decisions of this class was relayed
to the integrator second-hand through the coordinator's window; it is named here as the stated basis
for the call, and it is deliberately NOT reproduced as his words, because the integrator did not
receive it from him and cannot vouch for its wording. A reader auditing this authorisation later
should weigh these two findings as a delegate's call under a relayed grant, and item (2) above as the
only place the owner himself speaks to this gate. Both findings age out of the gate's 24-hour window
on 2026-08-18, and no edit in this range can clear them before then.

**A finding from outside this repository also stands on the same gate, and nothing here covers it.**
`ab589d1157102281b` ran `git stash -q -u` at 18:03Z in
`/Users/sashaabramovich/exhibition-engine-u27-applied`, under session `7e26e515`, against the
`exhibition-engine` project — a different repository, a different session, and no part of this
packet's lineage. `check-worker-restore.py` therefore reports FOUR findings at the time of writing,
not the three this record carried when it was first drafted. It is named because the record must
state the gate's true reading. It is not argued away: it is owned by whoever answers for that run,
it is unreachable from this range, and it falls under neither the owner's word above nor the
coordinating session's decision beside it.

The remaining machine-local reds have no documented road past them. The repository's own written remedies
are repairs, not bypasses: `scripts/sync-skills.sh` and `scripts/install-session-hooks.sh` write into
the owner's `~/.claude`, and the worker-restore counting start moves only on a recorded finding and
only as far as that finding requires — which this one does not need, since it ages out of the gate's
24-hour window on its own. `docs/push-law.md` states the governing rule: loosening a gate takes a
recorded profile entry, never a silent skip. `--no-verify` appears in `NEXT_STEPS.md` as a way to
avoid paying for the same 25-minute chain twice on a green verdict, not as a road past a red one.

Notes:

- **`ARCHITECTURE.md`'s change is 33 lines and all 33 are pins.** Every changed line is a
  `skills/*/SKILL.md:NNN` pin following its text to a new line number; no prose, no node, no
  invariant moved. Gate g proves each of them lands on its own line within tolerance.
- **Two suite reds predate this range and are not its work.**
  `tests/test_worker_restore.py::TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts`
  reds on a `git stash push -u -q` and a `git checkout --` run by agent `ac85659f` in
  `/private/tmp/live-spec-slimdown/wt` at 2026-08-17T15:33Z and 15:54Z — yesterday's builder, not a
  tree this range touches. stands: it is a true finding against the machine's transcripts, owned by
  whoever answers for that run, and no edit in this range can clear it.
- **`TestGateB_Tests::test_real_content_passes` is pre-existing, and was measured to prove it.** A
  second worktree was cut at the base, `git worktree add … --detach 9efe559`, and the same node run
  there alone: 1 failed, 1 passed in 8 minutes 5 seconds, the failure identical and resting on the
  same single inner test as above. stands: the node reds at the base as it reds here. The two
  scratch runs are also the whole of the file's 20-minute cost — each copies the repository and runs
  the full 208-file suite through `check-tests.sh`; nothing hangs.
- **`tests/test_config_health.py` reds on installed-skill drift, and this range caused it.** The
  gate diffs `skills/<name>/` against `~/.claude/skills/<name>`, and this packet slims exactly the
  three skills it names. stands: the prescribed repair, `scripts/sync-skills.sh`, writes outside the
  repository into the owner's own configuration. That is the owner's word to give and it is
  escalated, not taken here.
- **The suite rewrites `docs/PROGRESS.md` where it runs.** `tests/test_progress_report.py` executes
  `scripts/progress-report.py` with the repository root as its working directory, so any full run
  leaves the generated page modified in that tree. The behaviour predates this range — the test
  stands unchanged at 9efe559 — and the file is left as the run wrote it rather than restored by a
  discarding command. The single suite error, a leaked `/tmp/livespec-test-suite-log.*`, was my own:
  two pytest sessions ran at once and the session-scoped no-trace fixture of one saw the temp file
  of the other. It is an artifact of how I ran the suite, not of the change.
