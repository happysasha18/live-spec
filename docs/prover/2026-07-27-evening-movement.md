# Prover record — the evening movement, seven deliveries on main since `f98a7fd`, 2026-07-27

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK with the architecture lens, delta
scoped, with the quantifier re-verify the mode owes at every add (SPEC INV-170). Written by a seat that
authored none of the work (SPEC INV-237).

## Scope

**What this record reviews.** Every commit on main in `f98a7fd..HEAD`, twenty-two commits, forty-nine
files, read through `git log`, `git diff` and the files themselves. The seven deliveries: the
rendered-page sweep (Requirement 296, row 494), the setup walk's full hook coverage (Requirement 298,
row 506), the deletion-only push stand-down (R226.7–10, row 502), the criterion-readability ratchet
(Requirement 297), the configuration-surface seam (Requirement 299, row 496), the mid-turn chat check's
pre-filter and its eight new words, and the queue intake of rows 503, 504, 505 and 507.

**What this record does not review.** `docs/language-defects.md`, untracked and held by a concurrent
lane. It was read for collisions with this delta and holds none. `ROADMAP.md`, `NEXT_STEPS.md`,
`JOURNAL.md` and `FEEDBACK.md` were read and not written.

**State read.** HEAD moved once while this pass ran: it opened on `4213cfd` and `90da5ec` landed at
roughly 21:05, refreshing `NEXT_STEPS.md`. Every claim below was re-checked against `90da5ec` and every
run reported here was made on that tree. The one untracked file is `docs/language-defects.md`.

## Verdict

**HOLD — the push does not go on this state.** Six must-fix, ten should-fix, nine notes.

The two decisive items need no argument: the suite is red on two blocking checks, and a run of the
shipped sweep against a probe tree shows it moving its own archive contents in a circle. Beyond those,
the delta is sound in shape. The configuration-surface check is built the right way round — it carries
no list of kinds and reads the host's own two declarations, which is the answer the brief asked after.
The deletion-only stand-down reads git's own ref lines and stays conservative in every direction the
input can fail. The readability ratchet borrows the format family's one parser and the size ratchet's
recorded-count shape rather than inventing a fifth. What holds the push is that four of the six
must-fix items are places where a document states one rule and the shipped code reads another.

| # | Kind / severity | Claim / evidence | Status |
|---|---|---|---|
| M1 | defect / must-fix | The suite is red: `check-landing-next-steps.py` reds on commit `453760a`, and gate a's prover-record check reds until this record is committed | OPEN |
| M2 | defect / must-fix | The attic stands inside the sweep's reach on this tree: every cleared page is swept again on the next run, and the check reds for good after the first clearing | OPEN |
| M3 | defect / must-fix | A host that declares one home of its own loses `.git/` and `.live-spec/` from the exclusion set, and the sweep moves files out of both | OPEN |
| M4 | defect / must-fix | The chat check's new pre-filter narrows its reach: two calque entries lose cases their patterns catch, and the test written to prevent that reads one example per entry | OPEN |
| M5 | defect / must-fix | `guardrails/pre-push` anchors the deletion-only stand-down on INV-286, the rendered-page law, in its comment and in the line it prints to the person | OPEN |
| M6 | defect / must-fix | R226.6 and R226.7 state opposite rules for one push, and the code holds 7 | OPEN |
| S1 | defect / should-fix | R296.7 owes the evidence to the person as well as to the manifest; the spoken line carries none, and its test asks for none | OPEN |
| S2 | defect / should-fix | R297 states five duties and ships four arms; criterion 2 has no arm and no named net | OPEN |
| S3 | defect / should-fix | R297.1 states "one trigger and one duty within the recorded word cap"; arm A reads the word count alone | OPEN |
| S4 | defect / should-fix | `_is_none_answer` reads the declaration's first word, so a complete answer opening "No build is needed…" reds and a real "none" at the line's end passes | OPEN |
| S5 | defect / should-fix | R299.14 says "every deployed kind"; its test holds a two-element literal, so a third deployed row passes green with no seam clause | OPEN |
| S6 | defect / should-fix | `judge-hooks.json` declares a `matcher` field per hook and names it a generation field; nothing reads it | OPEN |
| S7 | defect / should-fix | `skills/publish/SKILL.md` and the communicator node's `owns` entry still state the record-home rule the spec dropped | OPEN |
| S8 | defect / should-fix | Row 507's decision rule rests on a measure no record holds, and its three branches leave a gap and an overlap | OPEN |
| S9 | defect / should-fix | The installer overwrites an installed hook file whose content differs, with no attic copy and no word, where R298.5 says a re-run changes nothing already installed | OPEN |
| S10 | defect / should-fix | `check-pin-drift.sh` reports one live drift on the new INV-289 pin, and the check is non-strict, so it rides through the push | OPEN |

---

## M1 — The suite is red on two blocking checks

> `FAILED tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` — `python3 -m pytest tests/ -q`, 2 failed, 2046 passed in 288s

> "landing commit 453760a2 flips ROADMAP row(s) 502 to landed but does not touch NEXT_STEPS.md (INV-242)" — `python3 guardrails/check-landing-next-steps.py`, exit 1, re-run at HEAD `90da5ec`

Commit `453760a` closes row 502 and writes no line into `NEXT_STEPS.md`. The later commit `90da5ec`
refreshes that file, and the check reads landing commits one at a time, so a later refresh does not
answer for an earlier landing. The suite is gate b of the push chain, so this red stops the push.

The second red is gate a's prover-record check: the newest committed record under `docs/prover/`
predates the last `PRODUCT_SPEC.md` change. Committing this record answers it, and no other action is
owed there.

For the first red, two roads. (a) Amend `453760a` to carry the `NEXT_STEPS.md` line it owes, which is a
history rewrite on an unpushed range and costs one rebase. (b) Add the row-502 line to `NEXT_STEPS.md`
in a fresh commit that also touches `ROADMAP.md`'s row 502 line, so the check reads one landing commit
carrying both. I prefer (a): the range is unpushed, and (b) writes a second flip of a row that is
already landed.

`defect · missing-outcome-check (postcondition)`

---

## M2 — The attic stands inside the sweep's reach, so a cleared page is cleared again on every run

> `"outside_reach": [".git", ".claude", ".live-spec"]` — `guardrails.config.json`, the `rendered_pages` block

> "12. The system *shall* leave the version-control directory, the harness's worktree home, the host state directory, and the attic outside the sweep." — PRODUCT_SPEC.md, R296.12

`sweep-rendered.py` carries a four-name default, `OUTSIDE_REACH = (".git", ".claude", ".live-spec",
"attic")`. `_config` returns the host's declared list whole when the block carries one:
`names = OUTSIDE_REACH if declared is None else declared`. This repo's block declares three, so the
default never applies and `attic/` sits inside the reach.

I ran the shipped sweep three times over a probe tree holding one marked page:

> "cleared 1 rendered page to attic/: attic/attic-report.html … attic/attic-report.html -> attic/attic-attic-report.html" — `python3 scripts/sweep-rendered.py --root .`, third run

Three runs, three manifest lines, one page. The check reds on the page resting in the attic:

> "attic/attic-attic-report.html: a page the document renderer produced, standing past its one reading — carried the `live-spec render-doc` generator mark (SPEC INV-286)" — `python3 guardrails/check-rendered-sweep.py --root .`, exit 1

So the moment the first marked page is cleared on this repo, the sweep check reds, the printed remedy
is to run the clearing, the clearing renames the page inside the attic and writes a fresh manifest
line, and the check reds again. R296.9 states that the clearing clears that red; on this tree it does
not. The check rides the suite, so this is a permanent suite red one clearing away. Nothing catches it
today because no marked page has yet been cleared here: the ten pages in `attic/` predate the mark and
carry none, which is why `check-rendered-sweep.py` currently reads green over them.

The tests read past it in both directions. `test_gate_leaves_the_attic_alone` and
`test_gate_stays_out_of_the_state_and_harness_homes` build trees with no `guardrails.config.json`, so
they exercise the code default, which does hold the attic. `test_the_reach_is_declared_as_host_config`
reads the live config and asserts `.git`, `.claude` and `.live-spec` are present, and never asks for
the fourth name the criterion states.

Add `"attic"` to `rendered_pages.outside_reach` in `guardrails.config.json`, and extend
`test_the_reach_is_declared_as_host_config` to read its four names from `sweep-rendered.OUTSIDE_REACH`
rather than from a literal in the test, so the two lists cannot part again. Add one test that sweeps a
tree twice and asserts the second run moves nothing.

`defect · stuck-state (liveness)`

---

## M3 — A host that declares its own homes loses git's directory and the state directory

> "13. The system *shall* let a host declare its own homes outside the reach as host configuration, holding the pack's own four as the default." — PRODUCT_SPEC.md, R296.13

A declared list replaces the four; it does not extend them. I built a tree whose config declares
`["vendor/"]` alone, matching the shipped test `test_a_host_declares_its_own_homes_outside_the_reach`,
and put one marked page under `.git/` and one under `.live-spec/checkpoints/`:

> "would clear 2 rendered pages to attic/: .git/hooks-page.html, .live-spec/checkpoints/draft.html" — `python3 scripts/sweep-rendered.py --root . --dry-run`

A host adopting the pack writes one line to spare its `vendor/` directory and, with no word said, hands
the sweep its own `.git/` and its own `.live-spec/`. The pages that move are recoverable from the
attic, and the state directory the checkpoint law governs is the one place a recovery road is least
help: a checkpoint moved out from under a running session reads as a lost checkpoint.

R296.12 states the four unconditionally, with no host-config escape; R296.13 grants the host a
declaration and calls the four "the default". The two criteria cannot both hold, and the code holds 13.

Make the four a floor rather than a default: `_config` returns `tuple(OUTSIDE_REACH) + tuple(declared)`,
and R296.13 reads "shall let a host add its own homes to the pack's own four". A host that genuinely
wants `.git/` swept has no case worth serving. Then rewrite
`test_a_host_declares_its_own_homes_outside_the_reach` to assert the declared home is spared **and**
the four still are.

`defect · direct-contradiction (contradiction)`

---

## M4 — The chat check's pre-filter turns two of its own laws off

> "An entry with no keys (a missing or empty `keys` field) runs its pattern unconditionally, since a keyless entry has given the scan no cheap signal to filter on — silently skipping it would let a live law go dark." — `hooks/midturn-chat-scan.py`, `judge`

The same silence arrives by the other road: an entry whose key is narrower than its own pattern. Two of
the fifteen entries are in that state. I ran `judge()` on the shipped list and on the same list with the
keys stripped:

| Sentence | With the pre-filter | With the keys stripped |
|---|---|---|
| `шва между модулем и хранилищем не видно` | no finding | `шов` |
| `засеяли проверку вчера` | no finding | `засеяна` |

The `шов` entry's pattern is `шв?[оае]?\w*`, written to catch the inflected forms, and its key is the
single form `шов`. The `засеяна` entry's pattern carries a `засе\w+` branch and its key is `засеян`.
So the entry that exists to catch a seam named between two things no longer catches it in the form a
person most often writes.

The person affected is the seat itself: the scan denies the next tool call and names the fragment, and
these two fragments now pass. The eight words that landed tonight were bought with a pre-filter that
took two older laws off the board.

The test written for exactly this hazard reads one example per entry:

> "assert any(k.lower() in low for k in keys), \"no key of %r matches its own example %r\"" — `tests/test_midturn_chat_scan.py`, `test_every_entry_carries_a_key_that_fires_on_its_own_example`

Every key was chosen to match its own example, so the test can only pass. Do two things. Widen the two
keys — `["шв", "шов"]` and `["засе"]`, since `keys` is already read as a list under `any`. Then replace
the one-example test with one that derives the check from the pattern: for every entry, assert that
each literal alternative the pattern can start on contains one of the keys, or simplest and exact,
assert that judging a corpus with the keys stripped returns the same finding set as judging it with
them in place.

`defect · unenforceable-promise (discharge)`

---

## M5 — The push hook names the rendered-page law where the deletion law belongs

> "# -- deletion-only stand-down (SPEC INV-286, ROADMAP row 502) --" — `guardrails/pre-push`, line 16

> "PUSH ALLOWED — deletion-only push: standing the full gate chain down (reason: a deletion carries no content for any gate to judge, SPEC INV-286)" — `guardrails/pre-push`, line 38

INV-286 is the rendered-page clearing, which landed the same evening on row 494. The deletion-only law
is INV-290, and R226.7–10 anchor on it. Both occurrences of the anchor in `pre-push` are the wrong one,
and the second is the line a person reads at the moment the whole gate chain stands down. A reader
following it lands on Requirement 296 and finds a law about HTML pages where the reason for their push
passing unguarded should be.

`grep -rn "INV-286" guardrails/ scripts/ hooks/ tests/` returns exactly these two lines outside the
sweep's own files, so the class is two occurrences and both are in one file. Nothing catches it: no gate
reads an invariant anchor in shipped code against the spec, and `tests/test_deletion_only_push.py`
anchors its own docstring on INV-290 without reading the hook's text.

Replace both with INV-290. Then add one line to `tests/test_deletion_only_push.py` asserting that
`guardrails/pre-push`'s stand-down block names INV-290 and names no other invariant, which is the same
shape the other document-home tests in this delta already use.

`defect · internal-conflict (consistency)`

---

## M6 — Two criteria of Requirement 226 state opposite rules for one push

> "6. The system *shall* run the prover-record, ownership, coverage, loadability, and prototype-fence checks at every push, never scoped, so nothing the diff touches is skipped. [INV-40]" — PRODUCT_SPEC.md, R226.6

> "7. *when* every ref-update line git feeds the pre-push hook carries the all-zero local object id, the system *shall* read the push as deletion-only and *shall* stand the whole gate chain down. [INV-290]" — PRODUCT_SPEC.md, R226.7

The two sit eight lines apart under adjacent case headings, "the cheap gates never scope" and "a
deletion-only push carries no content". Criterion 6 is a universal over pushes; criterion 7 names a
push where none of those five checks runs. The code holds 7: the stand-down block sits above `fail=0`
and above the chain's first echo, so it exits before gate a.

This is what the quantifier re-verify is for. Criterion 6's "at every push, never scoped" was true when
written and the newcomer falsifies it, and nobody re-read the older sentence at the add. A reader
auditing INV-40 reads criterion 6, believes the five checks are unconditional, and is wrong for one
whole class of push.

Rewrite criterion 6 to carry its one exception by name: "at every push that carries content, never
scoped", with a pointer to the deletion-only case. The alternative, dropping the stand-down for those
five checks, costs the row its whole reason — a deletion carries nothing for any of the five to read.

`defect · direct-contradiction (contradiction)`

---

## S1 — The clearing tells the person what moved and leaves out why

> "7. The system *shall* name every page it cleared, why it read that page as a render, and where it comes back from, both in the manifest line and to the person." — PRODUCT_SPEC.md, R296.7

The manifest line carries the evidence; the spoken line does not.

> "cleared 1 rendered page to attic/: report.html. Each rests in the attic and comes back from there if it turns out to be needed (SPEC INV-286, base rule 10).\n  report.html -> attic/report.html" — `python3 scripts/sweep-rendered.py --root .`

`declaration()` builds its sentence from the page names alone, and `main` prints one `src -> dest` line
per page with no evidence field, while `sweep()` already holds `why` for every page it moved.

The test that reads the spoken line asks for two of the three facts:

> "assert \"REPORT.html\" in out … assert \"attic\" in out" — `tests/test_rendered_sweep.py`, `test_sweep_says_out_loud_what_it_moved`

The cost lands on the person deciding whether a clearing was right: the manifest is a file they have to
open, and the line they actually see says nothing about why any page was chosen. That is the same gap
F6 of the row-494 record closed for the manifest, left open on the other surface the criterion names.

Print the evidence in the per-page line — `report.html -> attic/report.html  (carried the generator
mark)` — and extend the test to assert it, reading the evidence string from `evidence()` rather than
from a literal.

`defect · hard-to-monitor (observability)`

---

## S2 — Requirement 297 states five duties and ships four arms

> "2. A criterion *shall* use a term the glossary already defines. [INV-287]" — PRODUCT_SPEC.md, R297.2

> "6. The check `guardrails/check-criterion-readability.py` *shall* read the acceptance criteria of the document named on its command line through one readability arm per defect. [INV-287]" — PRODUCT_SPEC.md, R297.6

Criteria 1 through 5 name five reading defects. The check's docstring names four arms and maps them:
A to criterion 1, B to criterion 3, C to criterion 4, D to criterion 5. Criterion 2 has no arm.
Requirement 297 also names no other holder for it, so INV-287's declared-law demand for a named net
goes unmet on that one criterion.

The fact is probably held elsewhere — `check-vocabulary` reads whether a domain noun carries a glossary
entry — but a reader of R297 cannot know that, and criterion 6's "one readability arm per defect" reads
as a promise of five.

Name criterion 2's net in the requirement, citing the vocabulary gate, or move criterion 2 into that
gate's requirement and leave R297 with the four it holds. I prefer the first: the four arms and the
vocabulary read are one reading law from a stranger's side, and the requirement is where a reader looks.

`defect · missing-rule (invariant)`

---

## S3 — Arm A holds half of what criterion 1 states

> "1. A criterion *shall* state one trigger and one duty within the recorded word cap. [INV-287]" — PRODUCT_SPEC.md, R297.1

`arm_long_criterion` counts words against `max_words` and returns. Nothing reads how many triggers or
how many duties a criterion carries. A criterion holding two triggers and three duties inside
thirty-five words passes the arm and breaks the criterion.

The gap matters because the word cap is a proxy the requirement itself explains: the Context says the
defect is "the whole rule arrives welded into one sentence", and the count is how the arm reaches it.
Stating the proxy and the target in one sentence leaves a reader unable to tell which of the two the
gate holds.

Split criterion 1 into the duty and the measure: "A criterion *shall* state one trigger and one duty",
then "A criterion's body *shall* stand within the recorded word cap, the mechanical read of that rule".
The arm then names which of the two it holds, and the other joins criterion 10's list of what the
cold-reader panel owns.

`defect · unenforceable-promise (discharge)`

---

## S4 — The configuration check reads the declaration's first word as its whole answer

> "10. *if* a declaration answers \"none\" while the project's own `project.layers` line names a deployment layer, *then* the check *shall* red and *shall* quote both lines." — PRODUCT_SPEC.md, R299.10

`_is_none_answer` takes the first alphabetic word of the declaration and tests it against
`none_answers`, which holds `none`, `nothing` and `no`. I ran the shipped check over two profiles, each
recording a static-site kind and a layers line naming a deployment layer:

| Declaration | Check | What R299.10 asks for |
|---|---|---|
| "no build is needed for the experiment switch and the hero copy; both live in config.json and reach production by a config deploy" | red, contradiction, exit 1 | pass |
| "the site is deployed and nothing at all is turnable from outside a build — none" | pass, exit 0 | red, contradiction |

The first is the one that costs. A founding writes a complete and correct declaration, opens it with
the ordinary English word "no", and the check tells them their two declarations disagree and asks them
to name what they have just named. On an adopting host this is the first thing the pack says about
their own answer.

Read the whole declaration rather than its opening word. The narrow shape: an answer counts as "none"
when its text, with punctuation stripped, is a none-word alone or a none-word followed by a dash and a
reason, which is the form the pack's own profile and the `project.axes` line beside it already use. The
config carries the reason field to record that shape. Then add both probe cases above as tests.

`defect · missing-scenario (state-space)`

---

## S5 — "Every deployed kind" is proven against a two-element literal

> "14. The architecture document *shall* carry this principle in the per-kind design-principles table for every deployed kind, with both sides of the seam named." — PRODUCT_SPEC.md, R299.14

> `DEPLOYED_ROWS = ("frontend / visual", "code / backend service")` — `tests/test_config_surface.py`, line 43

The test walks the two row labels it holds and asserts each names both sides. A third deployed kind
added to the table tomorrow carries no obligation the suite can see, which is the case the criterion
was written for. The classification itself holds today: the architecture prose names static-site,
fullstack, photo-portfolio and backend as deployed, and the table's two rows cover all four, with book,
prose campaign, CLI and skill pack off the seam and carrying no such principle, which is R299.15.

Two things stand beside it and belong in the same fix. The architecture's kind list and the spec's
closed vocabulary disagree: the glossary names book, backend service, static site, fullstack app, CLI
and skill pack, and the architecture's tables and its deployed sentence add photo portfolio and prose
campaign while giving book and CLI no row at all. And deployedness is asserted per kind while it is a
property of a delivery — a book published as a website runs where its readers reach it, and the prose
classes books off the seam by name.

Derive the test's row set from the table rather than from a literal: read every row of the
design-principles table, and for each row whose label appears in the deployed sentence's list, assert
both sides of the seam. Then state in R299.14 which enumeration is authoritative, and reconcile the
architecture's kind labels with the spec's vocabulary in one pass.

`defect · over-specific (abstraction)`

---

## S6 — The hook declaration carries a field nothing reads

> "'matcher' names the PreToolUse/Stop matcher the entry carries in settings.json today, null where none (every one of the ten today)." — `guardrails/judge-hooks.json`, `_installer_fields_comment`

The comment names `file`, `command`, `matcher`, `data` and `personal_overlay` as the fields that let the
setup walk generate its coverage from the declaration. `scripts/install-session-hooks.sh` reads
`file`, `command`, `data`, `wired` and `personal_overlay`. `matcher` is read by nothing:
`grep -rn '"matcher"' scripts/ guardrails/ tests/` returns one hit outside the declaration, in
`scripts/install-separator-fence.sh`, which is a different hook and a literal of its own.

Today the field is null on all ten, so the silence costs nothing. The moment one hook needs a matcher —
a PreToolUse entry scoped to `Bash`, the shape `install-separator-fence.sh` already writes — the
declaration will carry it, the installer will keep writing an unmatched entry, and the declaration will
read as the one home for a fact it does not govern.

Either have the wiring block pass `decl["matcher"][stem]` into the entry when it is not null, with one
test that a declared matcher lands in `settings.json`, or drop the field and the sentence that names it
until a hook needs one.

`defect · boundary-issue (composition)`

---

## S7 — The record-home rule outlived the law it came from

> "A page inside a record home is a source artifact and the sweep leaves it standing." — `skills/publish/SKILL.md`, the release-sweep paragraph

> "INV-286 (the showing walk's clearing arm, the same shape as INV-223: … and the record homes are declared as host config in the guardrails node's config file)" — `ARCHITECTURE.md`, the communicator node's `owns` entry

The record-home rule was the delta's first design and was replaced by the renderer's mark before row
494 landed. `PRODUCT_SPEC.md` carries the phrase zero times; the glossary entry is gone;
`guardrails.config.json` carries `rendered_pages.outside_reach` and no `record_homes`. These two
sentences survived. The row-494 record's F5 named the node's pin, which was repointed; its `owns` tail
was not.

A session reading the publish skill at a release learns a rule with no mechanism behind it, and looks
for a home list that does not exist. A session reading the architecture node learns the same.

Rewrite both off the mark: the publish sentence to "A page carrying no renderer mark is the artifact
itself and the sweep leaves it standing", and the `owns` tail to name the declared reach under
`rendered_pages.outside_reach`. One grep for "record home" over the tree confirms the only other hits
are the unrelated review-record home of INV-208 and the frozen prototype output.

`defect · internal-conflict (consistency)`

---

## S8 — Row 507's decision rule rests on a number no record holds

> "Decision rule stated before the run: the expensive share falls by a third or more and wrong refusals stay under one in ten, the instruction stays; the expensive share holds and refusals sit near zero, the instruction is judged inert…; wrong refusals pass one in ten, the instruction is rewritten toward caution." — ROADMAP.md, row 507

The row states four measures and calls them "all read from records that already exist". Three of them
are readable: the per-tier share of helper runs, the refusal count against the expensive-dispatch
count, and the weekly spend. The fourth is not. "The count of tasks re-run a tier down that came back
needing the expensive tier after all" needs an outcome recorded for each re-run brief, and the row's
own build records only the refusal — its task text, its named tier, its reason. Nothing writes down
what happened to the brief afterwards. That measure carries the "wrong refusals" variable, and two of
the rule's three branches turn on it, so as written the experiment cannot reach a verdict.

The branch set also leaves a case unanswered and lets two branches fire at once. A run where the
expensive share falls by a fifth with wrong refusals at one in twenty matches no branch. A run with one
refusal, that refusal wrong, matches branch two on "refusals sit near zero" and branch three on "wrong
refusals pass one in ten" at the same time. And "falls by a third" carries no unit against a fifty
percent baseline: a third of the share is 33 percent, a third off the share is 17 points.

Three edits, all in the row. Add the fourth record: a re-run brief that comes back to the expensive
tier writes one line beside its refusal, so the wrong-refusal count has a home. Order the branches so
the wrong-refusal test is read first, which removes the overlap, and give the middle branch an
explicit remainder. State the third as a share: "the expensive share stands at or below a third of
runs".

`defect · unenforceable-promise (discharge)`

---

## S9 — The installer replaces a hook file a host has edited, with no word and no copy

> "5. *when* the installer runs a second time, the system *shall* change nothing already wired or already installed, recognizing a hook already wired under any command form." — PRODUCT_SPEC.md, R298.5

`_install` compares contents and, where they differ, writes the pack's copy over the host's file and
prints "installed:". `scripts/install-pack-hooks.sh` does the same with `cp` for its twelve files. A
host that tuned `~/.claude/hooks/scissors-scan.py` on their own machine loses that edit at the next
run of the one command the pack tells them to run, with no backup and no line naming what changed.

Criterion 6 protects the personal overlay files by name and criterion 5 promises the rest are
untouched, so the requirement as written already forbids this and the code does it. The pack's own
attic law says a superseded file is kept.

The overwrite itself is right for a pack upgrade, so fix the criterion and the report together.
Rewrite criterion 5 to "shall change nothing already wired, and shall replace an installed hook only
where the pack's copy differs, naming each replacement and keeping the previous file". Then have
`_install` move the differing file to the attic before writing, and print the old and new state on one
line. `test_rerun_changes_nothing` passes today because it re-runs on identical files; add the edited-
file case beside it.

`defect · unclear-recovery (rollback)`

---

## S10 — One architecture pin drifted and the check that saw it does not block

> "DRIFT (pin drift): scripts/install-pack-hooks.sh:1 (chained by install-session-hooks.sh, INV-289) — label not found within ±25 lines" — `bash guardrails/check-pin-drift.sh`, exit 0, 138 pins checked

The guardrails node's new pin claims `install-pack-hooks.sh` is chained by `install-session-hooks.sh`,
and the pinned file's own header says nothing of the kind — it still reads as a standalone installer.
The drift check is non-strict, so it reports and exits 0, and the pin rides through the push exactly
as the row-494 record's F5 did.

Add one line to `scripts/install-pack-hooks.sh`'s header naming its caller, which makes the pin's label
true where the pin points, and is also the sentence a person opening that file needs now that it is no
longer the entry point.

`defect · hard-to-operate (ops-ux)`

---

## Notes

**N1 — Nine recommendations from the row-494 record have no home.** That record's fold table hands F9
through F17 back and says "the rest ride the queue". Row 494 is archived closed in
`docs/queue-archive/rotated-ROADMAP-2026-07.md`, and `ROADMAP.md` carries no row for the attic's bound
(F10), the manifest's line shape (F15), the cruft-sweep collision (F13), or the away-stretch page
(F12). Nine findings are recorded in a closed row's record and tracked nowhere.

**N2 — The legacy source-beside reading has no expiry.** `evidence()` reads a markdown file of the same
name beside a page as proof the page is a render, bounded only by the tracked-page guard. So a
hand-built artifact page is protected from the day it is committed, and not before. A person who writes
a decision page and its markdown source and runs the sweep before committing loses the page to the
attic. Criterion 2 is aimed at pages rendered before the mark existed, a set that stops growing; a
one-time named set, or a bound on the file's modification time against the mark's landing date, would
close it.

**N3 — `criterion-readability.json` declares `governs: PRODUCT_SPEC.md` and nothing reads it.** The
check compares whatever document is handed to it against these baselines, so pointing it at a host's
own spec would red or rebaseline against numbers measured on another document.

**N4 — The config's `reason` promises a fall that has already been absorbed.** It says the seed carries
one unit from a delivery in flight and "the first run after the tree settles reports the fall". The
delivery landed; the arm reads 61 against a recorded 61. The sentence will read as an open debt to the
next person who opens the file.

**N5 — One docstring cites the wrong criterion.** `_record` in `scripts/sweep-rendered.py` cites
"SPEC INV-286, R296.5" for writing a manifest line per page; R296.6 owns that duty and R296.5 owns the
move under the collision law.

**N6 — Two matrix rows name fewer tests than their files hold.** M-466 names nine of the ten in
`tests/test_deletion_only_push.py` (`test_script_ships_and_is_executable` is unnamed); M-467 names
nineteen of twenty-one, and its own narrative says "20 of 20 red against the pre-delta tree". Every
name the two rows carry resolves to a real test, and M-463's forty-six mentions resolve to forty-one
distinct tests, all present.

**N7 — A fall goes unreported while another arm has risen.** R297.13 states the fall report
unconditionally; `main` returns from the risen branch before reaching the line that names fallen arms,
so a delivery that improves one arm while breaking another is told about the break alone.

**N8 — A test carries the one-home claim for the hook declaration, and the code does not.**
`scripts/install-pack-hooks.sh` carries its own literal list of twelve files and eight wire calls and
never opens `judge-hooks.json`. A hook added to the declaration and not to that script is caught by
`test_every_declared_hook_ends_up_wired`, which is a real net; the requirement's Context says the fix
"generates the installer's own coverage from the declaration", and that is true of two hooks of the
ten.

**N9 — A remote branch deletion now passes with no gate at all.** The stand-down's printed line says
so plainly — "whatever would guard the deletion itself is unaffected, since no such gate exists in
this chain today" — so the consequence is stated where a person reads it. It is worth the owner's
eye: `git push --delete main` on a bad day is one line and no check.

---

## The architecture lens — seven checks over the ARCHITECTURE.md delta

**Every spec fact has an owning node.** All six new invariants have exactly one: INV-286 on
communicator, INV-287 through INV-290 on guardrails, INV-291 on base-rulebook. No fact is owned twice.
Clean.

**No node stands without spec backing.** The delta adds no node. Clean.

**Every seam names what crosses it and who owns the format.** The communicator-to-attach seam row landed
with row 494 and names the page, the manifest line and attach as the format owner. The delta adds no
other seam. Clean.

**Quality budgets with instrumentation homes and watchers.** The delta declares no budget. The attic's
growth is still unwatched, which is the row-494 record's F10 and N1 above.

**The runtime view walks every promised flow.** `F-page-clearing` and `F-release-sweep` landed with row
494. Requirements 297, 298, 299 and R226.7–10 promise no person-facing flow of their own; each is a
check or an installer riding an existing walk. Clean.

**The placement view says where every node runs.** Unchanged by the delta and correct as it stands.

**The node-growth re-ask.** `guardrails/node_growth_counter.py` reads its files and reports every one
within its ratchet. `guardrails.config.json` now carries a third block and is pinned by two nodes,
which is the state the row-494 pass already read as clean.

## The quantifier re-verify (CROSS-LINK owes it at every add)

I swept the delta's neighbourhood for universals and member lists the newcomers falsify.

- **"at every push, never scoped" (R226.6)** — falsified by R226.7. That is M6.
- **"the version-control directory, the harness's worktree home, the host state directory, and the attic" (R296.12)** — falsified by the shipped config. That is M2.
- **"every deployed kind" (R299.14)** — holds in the document; its test holds a literal. That is S5.
- **"every hook named in `guardrails/judge-hooks.json`'s wired declaration" (R298.1)** — holds. All ten
  are installed and wired, seven by the chained script, one by it on `UserPromptSubmit`, two by the
  generated block. Proven by `test_every_declared_hook_ends_up_wired` from a fresh HOME.
- **"one readability arm per defect" (R297.6)** — five defects, four arms. That is S2.
- **The project-kind vocabulary (glossary) against the architecture's kind labels** — the two
  enumerations disagree. Folded into S5.
- **"three verdicts kept separate" (R173.4), "the founding question set" (R174), "the composition axes"
  (R265.1)** — each re-read against the new `project.config-surface` line. The founding set's version
  moved to 6 in both `scripts/founding-questions.json` and the pack's own profile, and adoption's
  orient carries the question. No member list is left short.

## What is sound, checked against primary sources

**The configuration-surface check carries no list of kinds, which is the answer the brief asked for.**
`guardrails/check-config-surface.py` reads three records of the host's own profile and its own config
file, and its header states plainly why: "Which kinds are deployed is a judgment, and its home is the
per-kind design-principles table in ARCHITECTURE.md… A list of kinds in check code would be the
literal-list design the base rulebook already names as the wrong answer to a class." Its keys, its
none-words and its deploy-words all live in `guardrails/config-surface.json`, and the check reds by
name when that file is missing or short a key. The one flaw in its reading is S4.

**The deletion-only check is conservative in every direction its input can fail.** Zero lines read
returns 1 and the chain runs; a mixed push returns 1 and the chain runs; a tty stdin skips the check
entirely. `pre-push` reads stdin once, before any gate below can touch it, and says so. I read the
script and the hook and found no path where a content push stands down.

**The renderer stamps its mark from one home and the sweep reads it from there.** `scripts/render-doc.py`
defines `GENERATOR` and the page string interpolates it; `sweep-rendered.py` loads the renderer by path
and imports the constant, with a literal fallback for a standalone copy. The two files cannot part on
the wording.

**The readability gate borrows rather than re-invents.** It reads the document through
`guardrails/specformat.py`, the one parser the format family shares, and it takes the recorded-count
shape from `check-size-ratchet.py`. Its header states, at real width, the three reads it does not make
and hands them to the cold-reader panel. `--rebaseline` refuses to raise a count and returns 1 naming
each risen arm, which holds R297.15 by construction.

**Every test the five new matrix rows name exists and passes.** 138 passed over
`test_rendered_sweep.py`, `test_criterion_readability.py`, `test_deletion_only_push.py`,
`test_install_session_hooks.py`, `test_config_surface.py`, `test_midturn_chat_scan.py` and
`test_chat_law_hook.py`. I checked every test name in M-463 through M-467 against the files
mechanically; none resolves to nothing.

**The format gates are green on the spec.** `check-requirement-shape.py` reads 1506 of 1506 criteria
well-shaped across 299 requirements; `check-index-generated.py` reads the committed index equal to a
fresh build over 375 codes; `check-matrix-reference.py` reads 382 anchors agreeing; `spec-style-lint.py`
reports zero errors; `check-size-ratchet.py` reads 204.8 bytes per criterion against a bound of 207.2;
`check-prototype-fence.sh` reads 158 fenced files with no prod reference. `check-criterion-readability.py`
reads all four arms at their recorded counts.

## The answers asked for

**Does each new requirement hold together as written?** Requirement 298 does, whole. Requirement 297
holds except for the arm its criterion 2 lacks (S2) and the two facts welded into criterion 1 (S3).
Requirement 299 holds as a document; its check narrows criterion 10's trigger (S4) and its criterion 14
is proven narrower than it reads (S5). Requirement 296 carries the one internal contradiction between
criteria 12 and 13 (M3) and one criterion the code half-holds (S1). R226's new case contradicts R226.6
(M6).

**Do the new laws collide with any law already in the spec?** One collision, M6, found by the
quantifier re-verify and stated above. The second thing the brief asked after — a code taken twice —
is M5: `guardrails/pre-push` carries INV-286 in two places where INV-290 belongs, which is the row-494
law wearing the row-502 law's clothes. No duplicate requirement number, no duplicate criterion anchor
and no duplicate matrix code stands anywhere in the delta; `check-index-generated.py` and
`check-matrix-reference.py` both read the generated tables equal to fresh builds.

**Does each new check's stated reach match what its code reads?** Three do and two do not.
`check-config-surface.py` names two files and three profile records and reads exactly those.
`check-criterion-readability.py` names two files, the criteria and the glossary terms, and reads
exactly those. `check-deletion-only-push.sh` names stdin and reads stdin. `check-rendered-sweep.py`
prints its reach honestly and the reach itself is wrong (M2). The mid-turn chat scan's docstring states
that a keyless entry runs unconditionally so a live law never goes dark, and two keyed entries go dark
anyway (M4).

**Does Requirement 299's per-kind classification hold, and does the check read a host's own
declaration?** The check reads the host's own declaration and carries no list of kinds — that half is
right, and the header states the reasoning. The classification holds for the four deployed kinds and
the four kinds off the seam as the architecture prose names them, and the two table rows carry the
principle with both sides named. It does not hold cleanly against the spec's closed kind vocabulary,
which names six kinds where the architecture works with eight labels, and it treats deployedness as a
property of a kind where it is a property of a delivery. That is S5.

**Is every path the sweep can reach safe, and is the recovery real?** The recovery is real: nothing is
deleted, every move writes its manifest line and flushes it before the next move, `attic/MANIFEST.md`
is tracked while the bytes are ignored, and a halt partway leaves every moved page accounted for. The
paths are not all safe. On this repo the sweep reaches its own archive (M2). On any host that declares
a home of its own the sweep reaches `.git/` and `.live-spec/` (M3). Both are proven by run.

**Is row 507's rule falsifiable, and are its measures readable?** Three of its four measures are
readable from records that exist. The fourth, the wrong-refusal count, has no writer, and two of the
three branches turn on it. The branch set also holds a gap and an overlap. That is S8.

**What ships with no test.** The evidence in the sweep's spoken line (S1). The attic's place in the
declared reach — no test reads the live config for it (M2). The pre-filter's coverage past one example
per entry (M4). The installer's overwrite path (S9). The `matcher` field, which has no consumer to test
(S6). The stand-down block's anchor in `guardrails/pre-push` (M5).

**Where a document says one thing and the code does another.** `pre-push` versus the spec on which law
it serves (M5). R296.12 and R296.13 versus `_config` (M2, M3). R226.6 versus the stand-down (M6).
R299.10 versus `_is_none_answer` (S4). R296.7 versus `declaration()` (S1). R297.1 versus
`arm_long_criterion` (S3). R298.5 versus `_install` and `cp` (S9). The `_installer_fields_comment`
versus the installer on `matcher` (S6). `skills/publish/SKILL.md` and the communicator node versus the
spec on record homes (S7). `criterion-readability.json`'s `governs` versus the check (N3).

## What to do next

1. Clear the two suite reds: amend `453760a` to carry its `NEXT_STEPS.md` line, and commit this record
   (M1).
2. Add `"attic"` to `rendered_pages.outside_reach`, make the four homes a floor rather than a default,
   and add the sweep-twice test (M2, M3).
3. Widen the two calque keys and replace the one-example test with a keys-stripped comparison (M4).
4. Replace both INV-286 anchors in `guardrails/pre-push` with INV-290 and pin them with one test (M5).
5. Rewrite R226.6 to carry its one exception by name (M6).
6. S1 through S10 belong in this push where they are one edit each — S1, S3, S6, S7 and S10 are. S2,
   S4, S5, S8 and S9 each carry a design call and can ride the queue.
7. Open the nine unhomed recommendations from the row-494 record as one queue row (N1).

Overall readiness: needs another iteration.
