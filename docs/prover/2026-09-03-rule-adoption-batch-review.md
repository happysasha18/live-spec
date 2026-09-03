# Prover record — 2026-09-03, the rule-adoption batch

Prover version: run under `product-prover-pack` 6.1.0 and its lens bindings. The external prover body
is untracked by this repository, so it does not travel into a worktree; the copy installed at
`~/.claude/skills/product-prover/` reports `metadata.version: 4.3.0` and describes itself as written
against `live-spec-base` v4.3.0. That is the body this pass had, and it is named here rather than
carried over from the version the day's earlier records state — see the closing note.

Mode: full review of a commit range, read for whether the rules it adopts hold together with the
documents that already stand.

Not a push review: this record carries no `PUSH-REVIEW` marker and no range fields. The push that
sends this work owes its own record.

Scope: the eight commits `d8d5305..fb836474` on `main` —

- `363d0a8f` q-816: widen acceptance to name R310 criterion 10; close the Blockers finding
- `12840c58` PLAN.md cleanup + role-profile brief rule adopted; pin drift fixed
- `85ddbda0` Adopt: a verdict on shown work is a movement end for its artifact
- `49611317` Enter two playbook-only rules into the pack (SKILL.md rules 22, 37)
- `1e952764` Re-record all 45 Director eval traces against tonight's follow-on commit
- `d2d57d24` docs/roadmap-format.md: fix framing to stop naming the retired ROADMAP.md
- `d9b61257` PLAN.md: close the roadmap-format naming Blockers finding
- `fb836474` adopt/install-style-gates.sh vendors scripts/preshow-register-lint.py; catch-up walk re-runs the kit

This is not a mechanical rename batch, unlike the two scoped reviews that preceded it tonight. It
enters four standing rules and closes four Blockers findings, and it was produced while a
worktree-isolation defect briefly put three writers on one physical tree. Every claim below was
re-derived from the tree rather than read off the commit messages.

Files read: `git diff d8d5305..fb836474` whole (63 files);
`skills/live-spec-base/SKILL.md` in full, both at `d8d5305` and at the tip;
`skills/live-spec-base/references/rule-origins.md` in full; `skills/director/SKILL.md` lines 300–380
and its specialist and closing-work sections; `README.md`; `~/.claude/playbook/PLAYBOOK.md` in full
(read-only, another project's tree); `docs/roadmap-format.md` in full;
`templates/PLAN.template.md` in full; `spec/doc-order-generated.md` Requirement 286;
`architecture/rules-and-settings.md` and `architecture/pipeline-and-lanes.md` pin blocks;
`PLAN.md` §Blockers in full and rows `q-816`, `q-166`, `q-584`, `q-801`;
`adopt/install-style-gates.sh` in full; `MIGRATION.md` Phase 4; `adopt/ADOPT.md`'s two install
headings; `scripts/preshow-register-lint.py` in full; `tests/test_style_gate_kit.py`,
`tests/test_catchup_walk.py`, `guardrails/check-pin-drift.sh` in full;
`evals/director/README.md`, `evals/director/closing-scenarios.json`; `docs/prover/README.md`;
`docs/prover/2026-09-03-work-board-restoration-review.md`.

Checks run:
`python3 -m pytest -q tests/test_guardrails.py -k ProverRecord` — 1 failed, 13 passed, before this
record was written; the failure is the freshness arm this record exists to satisfy.
`bash guardrails/check-pin-drift.sh` — exit 0, 184 pins checked, green. F1 below is what that green
is worth here.
`python3 evals/director/check.py --all` — 34 of 36, exactly the number `evals/director/README.md`
records.
`python3 -m pytest -q tests/test_director_scenarios.py` — 20 passed, the nine closing scenarios
among them.
`shasum -a 256 skills/director/SKILL.md` — `55806109…e2d684`, byte-for-byte the
`recorded_run.skill_sha256` the re-recorded eval pins.
`git merge-base --is-ancestor` against each commit hash cited in the range's own prose —
`b886c944`, `56611b76`, `614cc25e`, `61a77841`, `98a003b5`, `061d1294`.
`grep -cE '^[0-9]+\. \*\*' skills/live-spec-base/SKILL.md` — 23.
`grep -rn "twenty-two\|twenty-three"` over the whole tree, read by hand.

## F1 — The pin sweep fixed three of the seven pins its own insertions moved, and the gate passes the other four vacuously

> `- skills/live-spec-base/SKILL.md:231` (rule 26, INV-136/INV-139 — a project kind declares design
> principles the verify pass runs; the per-kind table lives in this doc)
> — `architecture/rules-and-settings.md:28`

Commit `12840c58` carries "pin drift fixed" in its own subject line. Three pins moved with it:
`architecture/pipeline-and-lanes.md:72` (149 → 154), and `architecture/rules-and-settings.md`
lines 24 and 25 (194 → 199, 204 → 209). Each of those three is now correct: rule 16 stands at line
199 and rule 22 at line 209.

The range inserted lines in three places in `skills/live-spec-base/SKILL.md` — five for the
role-profile sub-rule at rule 7, three for rule 22's extension, six for rule 37 — and seven pins
into that file sat below the first insertion. Four were not moved:

| pin | label names | rule head now stands at | now off by |
| --- | --- | --- | --- |
| `rules-and-settings.md:28` → `SKILL.md:231` | rule 26 | 239 | 8 |
| `rules-and-settings.md:29` → `SKILL.md:236` | rule 27 | 244 | 8 |
| `rules-and-settings.md:30` → `SKILL.md:253` | rule 31 | 261 | 8 |
| `rules-and-settings.md:26` → `SKILL.md:303` | the settings-ladder pointer | 317 | 14 |

All four were exactly right at `d8d5305`: reading `git show d8d5305:skills/live-spec-base/SKILL.md`,
rule 26 stood at 231, rule 27 at 236, rule 31 at 253, and the ladder pointer at 303. So this range
broke them, in the same commit that says it fixed the drift, and they sit three to five lines below
two pins the same commit corrected in the same bullet list.

Where each now lands: `:231` falls inside rule 25's body ("Reading a file to understand or design
it, past a glance, is itself work"); `:236` inside rule 25's closing sentence; `:253` inside rule
29's body. None of the three resolves to the rule its label names.

`guardrails/check-pin-drift.sh` reads all four and passes them. I checked the mechanism rather than
assuming one, by reading the gate's `label_words()` and its FURNITURE list and matching by hand:

- `:231` — the label's naming word **design** stands in the ±2 window, in rule 25's "understand or
  design it". The word belongs to a different rule.
- `:236` — the label's naming word **seat** stands in the window, in rule 25's "the seat dispatches
  it to a reader".
- `:253` — no ordinary label word stands in the window. The match is **named**, matching as a
  substring inside rule 29's "An **unnamed** human-only fact".
- `:303` — never checked as a line pin at all. It is prose inside the label of the file-level pin
  `skills/live-spec-base/references/settings-ladder.md:1`, and the gate reads pins, not the text of
  labels, so this one has no arm on it in either direction.

This is the gate's own documented failure mode, recorded in its header comment for rows 90, 541 and
588 — a pin proved by a furniture-ish word that recurs in every window of a rulebook — reappearing
on naming words that are not on its furniture list but recur just as freely inside a document about
seats, designs, and named things.

Who is affected and how: a session or a reviewer following the architecture map to rule 26, 27 or 31
lands in the middle of a different rule and reads the wrong law, and the gate that exists to catch
exactly this reports green over it.

Proposed action: re-point the four, the same re-point the range already made three times. Whether
the gate's naming-word rule needs narrowing is a second and separate question and is the owner's,
not this record's — this finding names the four stale pins, and reports that the gate's green does
not cover them.

Not blocking: nothing executes off these numbers; the normative pin is the named thing, and the
`:line` is a cache the pack's own SPEC E-14 already says so.

## F2 — The migrated rule-22 trigger names the wrong playbook chapter, and the playbook's own diagnosis did not travel

> "The principle's fuller chapter lives in the owner's private playbook repository, in its
> `PLAYBOOK.md`, whose own operational trigger is this: when the owner questions a change — 'what's
> the point' or 'what a mess' — a proxy has replaced the goal; stop editing and read the rendered
> output itself (playbook `PLAYBOOK.md`, 2026-06-21 s14)."
> — `skills/live-spec-base/SKILL.md` rule 22

> "Citation (playbook, 2026-06-21 s14), the rendered-output trigger … Migrated from the retiring
> playbook document per PLAN.md's Blockers finding (31.08, q-800; closed 03.09) — **the one piece of
> the convergence chapter** plan-16 (31.08) left unmoved."
> — `skills/live-spec-base/references/rule-origins.md`

I read `~/.claude/playbook/PLAYBOOK.md` and located the source. It is not in the convergence
chapter. The playbook's `## Convergence — every piece of work walks to its goal` runs lines 21–41.
The migrated bullet stands at line 93, inside `## Truth & sourcing` (lines 80–100), directly under
"When Alexander corrects me, I find and quote the primary source before I answer."

Two things follow from that, and they are separable.

**The attribution is wrong as written.** Rule 22's own sentence says the playbook chapter it points
at has this as "its own operational trigger", and `rule-origins.md` calls it "the one piece of the
convergence chapter … left unmoved". Neither is true of the document: the convergence chapter does
not contain it, and a reader who follows the pointer to check will not find it there. `PLAN.md`'s
Blockers entry closing the same finding repeats the framing — "folded into rule 22 (convergence),
which already pointed at this same playbook chapter" — and the chapter it already pointed at is not
the chapter the bullet came from.

**The playbook's stated cause did not travel.** The source reads: "that is a signal the change is
cosmetic, or that accumulated layers have become the real problem … **The bug is usually the
accumulation, not the latest diff.**" The pack renders the cause as "a proxy has replaced the goal",
which is rule 22's own vocabulary, not the playbook's, and drops the accumulation diagnosis whole.
The instruction half — stop editing, read the rendered output — travelled faithfully. The diagnosis
half was replaced by the framing of the rule that received it.

Whether the bullet belongs under rule 22 or under rule 13 (a claim needs its primary source, which
is the pack's home for the rest of the playbook's Truth & sourcing chapter) is the owner's call and
is not a finding. What is a finding is that two documents now assert a provenance the source does
not carry, and that the migration's own justification — that this was the convergence chapter's last
unmoved piece — rests on it.

Not blocking: the rule as stated is actionable and its instruction is faithful.

## F3 — `PLAN.md` cites a commit that no longer exists on any branch

> "Landed in `b886c944` (docs/roadmap-format.md, spec/doc-order-generated.md), full suite green
> after: 2738 passed, 57 skipped, 0 failed."
> — `PLAN.md`, the closed roadmap-format Blockers entry

`git merge-base --is-ancestor b886c944 HEAD` returns false, and `b886c944` appears on no branch —
it is a dangling object, readable today only because git has not yet collected it. The work it
names actually landed as `d2d57d24`, which carries the identical subject line.

I checked whether anything was lost in the reconciliation, and nothing was: `git diff b886c944
d2d57d24` touches neither `docs/roadmap-format.md` nor `spec/doc-order-generated.md`, so the two
files are byte-identical across the orphan and the landed commit. `b886c944` was simply built on the
pre-rule-commits base during the shared-tree collision and re-made on the reconciled one.

The other five hashes the range's prose cites all resolve: `56611b76`, `614cc25e`, `61a77841`,
`98a003b5` and `061d1294` are each ancestors of HEAD.

Who is affected and how: whoever goes looking for the landing this line names, after the object is
collected, finds nothing and cannot tell whether the work landed at all.

Proposed action: re-point the citation to `d2d57d24`. One hash.

Not blocking: the work is present in the tree.

## F4 — `docs/roadmap-format.md` still names the retired document in the one place a reader meets first

> `# The roadmap format — definition` — `docs/roadmap-format.md:1`

> "Fixed as a naming fix, no substance changed: `docs/roadmap-format.md` now names itself the format
> 'a project's plan/queue is written in' and speaks of 'the queue' throughout rather than 'the
> roadmap'." — `PLAN.md`, the closed Blockers entry

The body did change throughout, and correctly. The title did not. The original finding's own words
were that the page "opens by defining 'the format the roadmap is written in' and names a document
the pack stopped shipping today"; the first body sentence was repaired and the `# ` line above it,
which is the first thing any reader sees and the string a search returns, still says roadmap.

The other two surviving instances are fine and I checked each: line 71's `rotated-ROADMAP-YYYY-MM.md`
is a live filename, and line 65's "One delivery converts the whole roadmap to this format" opens the
declared-deltas block, which is a dated record of a past conversion and reads correctly as one.

The filename `docs/roadmap-format.md` is a separate question and I am not naming it as a defect:
`templates/PLAN.template.md` and `spec/doc-order-generated.md` Requirement 286 both point at that
path, so renaming the file is a change with its own reach, not a title edit.

Not blocking: nothing resolves off the title.

## F5 — The rule-origins file's new section breaks the ordering every other section in it keeps

`skills/live-spec-base/references/rule-origins.md` carries sixteen `### <n>. <rule name>` sections.
Fifteen stand in strictly ascending rule order: 2, 3, 4, 7, 9, 13, 17, 22, 24, 25, 26, 27, 29, 31,
36. The new `### 37. Every plan names what it must not touch` was inserted at line 86, between 22
and 24.

Nothing mechanical reads this order, and the section's content is correct where it sits. It is
reported because the file's own convention is unmistakable at fifteen for fifteen, and because a
reader scanning for rule 37 will scan past its home to the end of the file and conclude it has none.

Not blocking, and cheap: move the section below `### 36`.

## F6 — The role-profile sub-rule sits under the fence rule rather than the briefing rule, and no check reaches it

The new sub-rule was entered under rule 7, "The concurrent-edit fence, before every write and every
commit," whose body opens the sub-list with "The parallel-lanes rules sit underneath the fence."
Every other bullet under it is a concurrency or write-set constraint — the lane cap, the lane-open
act, worktree isolation on overlap, brief-time disjointness, the worker-restore wording, one row per
landing commit, the prior-context worker, the push in flight, the tied claim. The new bullet is
about what a brief should contain, which is rule 5's subject ("The seat orchestrates; each unit
routes to the cheapest tier that passes its brief"). Rule 7 closes by naming its two enforcement
arms, `guardrails/check-worker-restore.py` and `scripts/open-lane.sh`; neither reaches the new
sub-rule, so the rule sits under a footer that implies a check it does not have. Rule 37, entered in
the same range, states its own "prose-only, no dedicated check" plainly, which is the pack's own
convention for exactly this.

I checked the whole pack for a competing home before reporting this: `grep -rn "role profile\|role-
profile\|craftsman"` finds the rule stated in exactly one place, plus its citation in
`rule-origins.md` and its incident record in `inbox/handled/`. There is no duplicate and no
contradiction. This is a reachability question, not a duplication one: a session resolving "what
goes in a worker's brief" reads rule 5.

Not blocking.

## What else this pass looked for, and found clean

**The rule count, in all three homes.** `grep -cE '^[0-9]+\. \*\*'` over
`skills/live-spec-base/SKILL.md` returns 23. The frontmatter description reads "twenty-three rules
in the body" and `README.md:69` reads "twenty-three shared rules across the skill set". Both were
updated in this range and both are right. `PLAN.md:2675` still reads "twenty-two shared rules", and
that is correct as it stands: it sits inside a "**Checked by reading on 02.09.**" block recording
what was verified that day, the same way `q-166`'s reference to `q-811` reads as a dated record
rather than a live pointer. The whole-tree grep for "twenty-two" turns up no other live claim about
this file — every remaining hit is a `communicator` count (that skill genuinely has 22 rules), a
journal or archive entry, or a dated review record.

**The director rule against its neighbours.** The new paragraph sits directly under "A shown result
closes the work; the human's own eye is never the gate on an ordinary delivery," and the two
compose rather than collide: the earlier paragraph governs an ordinary delivery, and the new one
governs the three cases rule 12/27 reserve. Its citation resolves — rule 12 ("The human's gates are
the human's") and rule 27 ("The seat decides what it can decide") both exist and both name the
reserved set the paragraph relies on. It does not contradict the preceding paragraph's "a
disagreement afterward is a new fact, not a reopening", because that clause is scoped to an ordinary
shown result and this one is scoped to a taste call where his verdict is the gate. The pack already
carries "every movement ends at a safe breakpoint" as Requirement 125 in
`spec/push-gate-milestone-audit.md`, and the new paragraph adds a trigger to it rather than
restating it: what is new is that a verdict is one such end. No duplicate claim found.

**Rule 37 against the playbook's own wording.** Faithful. The playbook's "Every plan names the
components I must not touch. Before I act, I identify what already works and is out of scope … I
confirm with Alexander when the blast radius is unclear. Then I change only what the task needs and
nothing next to it. This rule exists because I kept breaking working things by editing more than I
was asked to" carries over clause for clause, with the conditional confirmation kept conditional.
`PLAN.md`'s closing note even corrects its own earlier paraphrase of "the cardinal sin" back to the
playbook's word, and names the correction as it lands. The playbook ranks this among its cardinal
rules and the pack's flat rule list has no way to carry a ranking; that is a property of the target
document, not a drift.

**`q-816`'s widened acceptance against finding F2 of the restoration review.** It closes it
properly, not by papering over. The old acceptance was scoped to one file
("unchanged from `spec/work-board.md` Requirement 309's own criteria"). The new one names the second
file, the requirement, the criterion number, and the switch itself in its own words: "and
`spec/live-status-reporting.md` Requirement 310 criterion 10 — once the board ships, a work block's
announcement home moves from the written plan page to the board's own per-task plan." F2's stated
harm was that closing `q-816` on its own words would leave criterion 10's switch unmade; that is no
longer possible on this wording. The row records the owner's reason for one row rather than two, and
names the record it closes.

**`docs/roadmap-format.md`'s substance against the template, checked rather than trusted.** The
fixing worker's claim holds. `templates/PLAN.template.md` carries the header
`| # | Wish (plain words) | Class | Status | Decision / acceptance |` — the same five cells the page
defines — its example rows read `*queued*` and `*in-work*` in lowercase italics, and it names
`docs/roadmap-format.md` as the one home of exactly the four things the page carries: the row shape,
the status and class vocabularies, the live-body law, and the row lint. The five status words and
the four class words on the page are the words the template's own prose and rows use. Nothing about
the row shape or the vocabularies is stale; only the framing was, and F4 above is the one piece of
the framing left.

**The eval re-record's own freshness mechanism.** This is the part of the range most exposed to the
collision, and it is sound. `closing-scenarios.json`'s `recorded_run.skill_sha256` reads
`55806109032985f9b7bb00a94242e7c6c112c67039fcfa7f58e6f9c2aee2d684`, and `shasum -a 256
skills/director/SKILL.md` at the tip returns the same digest, so the pin is against the file as it
now stands, not as it stood mid-collision. `skills/director/SKILL.md` is touched by exactly one
commit in the range (`85ddbda0`), which precedes the re-record (`1e952764`), and no commit after the
re-record touches it. Both graders reproduce the recorded numbers exactly: `check.py --all` returns
"34 of 36", and `tests/test_director_scenarios.py` passes all 20 including the nine closing runs.
The README's own reading of the 7-of-9 → 9-of-9 jump is the honest one — it says the added paragraph
does not touch the rules those two scenarios exercise and reads the change as producer variance
rather than as the paragraph fixing anything — and I agree with it on the text: the paragraph is
scoped to taste calls and the two scenarios turn on the closing rule and the disagreement rule.

**The vendoring fix, and whether it closes the finding it claims.** It does, and the second half of
the original finding is not owed. `scripts/preshow-register-lint.py` now stands in
`VENDOR_FILES` in both the shell array and the Python manifest block of
`adopt/install-style-gates.sh`, and in `tests/test_style_gate_kit.py`'s own tuple.
`MIGRATION.md` Phase 4 gained the `--force` re-run, `tests/test_catchup_walk.py` pins it present and
ordered after the status-view step, and `adopt/ADOPT.md` really does carry "Then wire the style
gate" and "Then install the status view" at the founding end, as both the step text and the test
docstring claim.

I checked the vendored script for dependencies that would not travel with it, since a half-vendored
script is the obvious sibling defect. It is self-contained: it holds its pattern list inline, and
its one external reach, `hooks/register_judge_core.py`, is behind `_judge_enabled()`, which is
opt-in on `PRESHOW_REGISTER_JUDGE` and off by default, and behind a `try/ImportError` that stands the
judge down without failing. A host with no `hooks/` directory runs the literal list cleanly. It needs
none of `guardrails/spec-coinages.json`, which is vendored for `spec-style-lint.py`'s sake.

I also checked whether "the law that names it still blocks nothing on a host" — the finding's second
clause — remains true, since the installer's gate-r block wires only
`python3 scripts/spec-style-lint.py` into the host's pre-push and never calls the register lint. It
does remain true, and it is deliberate: `PLAN.md:1826` records the pack's own decision that no push
gate forces an audit ("the loop is run by a person or a model, and no script decides whether it
ran"), citing `guardrails/language-rules.json:2871`. So shipping the file to the host is the whole
of what was owed, and no gate wiring is missing. Reported here because a reader of the closed finding
would otherwise have to re-derive it.

**Duplicate or colliding claims among the four new rules.** None found. The role-profile sub-rule
exists in one place. Rule 37 exists in one place and no other rule in the body covers scope
declaration. Rule 22's addition extends a rule rather than restating one. The director paragraph adds
a trigger to a movement-end law the spec already holds, without restating the law.
`PLAN.md`'s claim that director "already points at the base rulebook for the shape of a brief and
needed no change" checks out at `skills/director/SKILL.md:307`, "**A specialist gets a brief, not a
copy** — see 'The specialists' below for the exact shape."

**`MIGRATION.md`'s renumbering.** Steps 4 through 7 became 5 through 8 when the style-gate step was
inserted. Grepping the tree for references into Phase 4's step numbers turns up none — every citing
line names the phase or the script, never an ordinal — so nothing was left pointing at a step that
moved.

## Class lens

Two classes, and the second is the one this range's conditions predicted.

**A fact with several homes, corrected in some of them.** F1 (four of seven pins), F4 (the body
changed, the title did not) and F3 (a hash re-pointed nowhere) are all one shape: a correction that
reached the homes the corrector was looking at and stopped. I swept the range for further members
and found the sweep otherwise thorough — the rule count was updated in both of its live homes, the
`inbox/` renames took all three files, the `VENDOR_FILES` list was updated in both of the two places
`install-style-gates.sh` holds it, and `PLAN.md`'s own Blockers entries were closed one per finding
rather than in bulk. So three instances, in a range that got the same shape right five times.

**A claim about a source, checked against the source.** F2 is its own class: a migration that
restates where a rule came from, where the restatement is wrong in a way only reading the source
document exposes. It has one member here. I looked for a second by reading the whole playbook
against rule 37's citation, and rule 37's is accurate.

F5 and F6 are neither class — an ordering slip and a placement question, each reported once.

## Verdict

The four rules this range adopts are correctly stated, non-duplicating, and consistent with the
documents that receive them, and the two mechanical claims most exposed to the collision — the eval
re-record's hash pin and the roadmap-format page's substance — are both true when re-derived rather
than trusted. Nothing here undermines the range's claimed correctness: no rule contradicts a
neighbour, no count is wrong, no test claim is inflated, and no work was lost in the reconciliation.

What the collision did leave is bookkeeping that points at the wrong place: four architecture pins
this range itself moved and did not follow, one dangling commit hash, one page title, one
out-of-order section, and one provenance claim that does not survive reading the document it cites.

Findings: F1 (four stale pins the range created, gate green over them, non-blocking, no fix made —
review only), F2 (rule 22's migrated trigger attributed to the wrong playbook chapter and stripped
of its stated cause, non-blocking, no fix made), F3 (`PLAN.md` cites the unreachable `b886c944`,
non-blocking, no fix made), F4 (`docs/roadmap-format.md`'s title still names the retired document
against a closing claim of "throughout", non-blocking, no fix made), F5 (rule-origins' section 37
out of order, non-blocking, no fix made), F6 (the role-profile sub-rule under the fence rule rather
than the briefing rule, with no check reaching it, non-blocking, no fix made).

Blocking: none.

Note outside the range, on this record's own first line: the pack binding asks every record to name
the prover version that ran, and the day's earlier records name 1.6.2 at `skills/product-prover/`.
That path is untracked by this repository, so it is absent from a worktree, and the copy at
`~/.claude/skills/product-prover/` reports `metadata.version: 4.3.0` and states it is written
against `live-spec-base` v4.3.0 — five minor versions behind the base it now runs beside. Whether
the machine carries a newer copy elsewhere is not something this seat can see from here. Named so
that the version line on this record is the version that actually ran.
