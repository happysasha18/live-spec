# Prover record — Requirement 300, the criterion rewrites, the widened readability gate, and the worker-restore clause, 2026-07-28

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK with the architecture lens, delta
scoped. Written by a seat that authored none of this work (SPEC INV-237).

## Scope

**What this record reviews.** The uncommitted tree at HEAD `73741a9`, read through `git diff`,
`git status`, and `git show HEAD:PRODUCT_SPEC.md`:

- `PRODUCT_SPEC.md` — Requirement 300 with its twenty criteria and INV-292 through INV-297, and the 93
  rewritten acceptance criteria across the body;
- the language-rule machinery — `guardrails/language-rules.json`, `scripts/gen-language-consumers.py`,
  `hooks/language-laws.json`, `docs/language-rules.md`, `guardrails/check-language-rules.py`,
  `tests/test_language_rules.py`, `docs/language-defects.md`, `docs/language-reads/`;
- `ARCHITECTURE.md`'s guardrails node and `TEST_MATRIX.md` rows M-468 through M-473;
- `guardrails/check-criterion-readability.py`, `guardrails/criterion-readability.json`,
  `guardrails/specformat.py`, and the two new `tests/fixtures/specformat/readability_bullets_*.md`;
- the worker-restore clause in `skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md`,
  `skills/build-pipeline/references/delegation-protocol.md`, `templates/agent.template.md`, and
  `scripts/open-lane.sh`, with `guardrails/check-worker-restore.py` and `tests/test_worker_restore.py`.

**What this record reads for collisions and does not judge.** `guardrails/check-tier-refusal.py`,
`guardrails/tier-refusal.json`, `tests/test_tier_refusal.py`, `docs/measure/tier-refusals.md`, and
`docs/measure/2026-07-28-tier-routing-experiment.md` arrived in the same tree and belong to another row.
They are named once, in F16, because they share that finding's cause.

**The tree moved while this pass ran, and the state below is what the verdict judges.** The pass opened at
01:01 and closed at 01:35. Between those two times `docs/language-defects.md` was rewritten and
`scripts/gen-language-consumers.py`'s document renderer was replaced. Two consequences are recorded in
place: F21 opened at 01:06 and was folded by another session before this record was written, and F32 names
the new renderer. Every other finding below was re-verified against the tree at 01:35, and a
`PRODUCT_SPEC.md` line number is given only where the record needs one, since sibling sessions are
writing the same file. Criteria are cited by requirement and number.

**Commands run.** `guardrails/check-language-rules.py` (green, 60 rules, 137 repository pins and 106 home
pins resolved), `guardrails/check-criterion-readability.py PRODUCT_SPEC.md` (green, 1526 criteria),
`scripts/check-shipped-language.py` (green), `guardrails/check-every-gate-can-fail.py` (green, 26 gates),
`guardrails/check-judge-listed.py` (green), `guardrails/check-doc-bound.py` (green),
`scripts/spec-style-lint.py PRODUCT_SPEC.md` (green), and
`pytest tests/test_language_rules.py tests/test_worker_restore.py tests/test_criterion_readability.py
tests/test_traceability.py tests/test_tier_refusal.py` (325 passed).

## Verdict

**The delta holds once the must-fix findings are folded.** Every gate the delta touches is green and the
targeted suite passes, so what follows is what the green misses.

The design underneath Requirement 300 is right. One home, a generator, a gate that rebuilds through the
generator rather than through a second renderer, a status vocabulary that says whether anything runs a
rule, and a stand-down for a pin under a reader's own tree — those are the pieces a rule family needs, and
the machine carries them. What holds the fold is a gap between the requirement's twenty criteria and the
machine underneath them: five criteria promise a red the check never issues, and the check does work no
criterion states. The criterion rewrites moved a shipped behaviour out of the spec in one place, moved a
normative link into a Context block in another, and turned a waiver's subject around in a third. The
worker-restore clause forbids fewer commands in every brief than its gate reds on, and its gate is armed
nowhere.

The delivery's own reading is worth naming. The readability gate widened its reach in the same pass that
93 criteria moved words into bullets, and the config records why: the three prose counts fell by 93, 56
and 26 while the same criteria ran 5247 words before and 5541 after. A measure that would have paid a
writer for moving words one line down was found and closed inside the same landing, and the fifth arm that
sums a criterion's pieces closes it for good. That is the delta's strongest piece of work.

| # | Kind / severity | Claim | Status |
|---|---|---|---|
| F1 | defect / must-fix | R300.3 calls a second statement a defect; `sources` records second statements by design and the gate reports none | OPEN |
| F2 | defect / must-fix | R300.4 says every consumer is generated; three pattern hooks hold their own lists | OPEN |
| F3 | defect / must-fix | R300.2 demands thresholds, exceptions and examples on every rule; most rules carry none of one or more | OPEN |
| F4 | defect / must-fix | R300.8, R300.9 and R300.11 promise a red for a missing catcher record; the check fires only on `status: held` | OPEN |
| F5 | defect / must-fix | R300.7 is universal; `check_sources` spares every pin under the reader's home tree | OPEN |
| F6 | defect / must-fix | R300.16 and R300.17 declare a law and name no net | OPEN |
| F7 | defect / must-fix | The shipped fifth readability arm rests on no criterion, and R297's case heading counts four | OPEN |
| F8 | defect / must-fix | The criterion sub-list is a format element no format law states | OPEN |
| F9 | defect / must-fix | R117.1's "only" now excludes what its own bullet permits | OPEN |
| F10 | defect / must-fix | R61.5's stand-down criterion carries a bullet saying the review still runs | OPEN |
| F11 | defect / must-fix | R294.1 dropped the span-stripping rule its declared sibling R232.1 kept, and the code strips | OPEN |
| F12 | defect / must-fix | R244.2 dropped the sentence that turns a nodes-per-file count into a failed fitness answer | OPEN |
| F13 | defect / must-fix | R186.4 deleted the only statement of "the show rule", a term used twice and glossed nowhere | OPEN |
| F14 | defect / must-fix | R151.2's bullet now waives a genuine offence where the original waived a legitimate fixture name | OPEN |
| F15 | defect / must-fix | `check-worker-restore.py` is BLOCKING and no step, gate, or suite run takes its verdict | OPEN |
| F16 | defect / must-fix | The worker-restore and tier-refusal machinery own no architecture node and no matrix row | OPEN |
| F17 | defect / must-fix | The gate reds five command forms; all five prose statements name four | OPEN |
| F18 | defect / must-fix | The clause's headline scopes to the shared tree; its body and its gate reach every tree | OPEN |
| F19 | defect / must-fix | The clause ends the failure branch at HALT and names no path out | OPEN |
| F20 | defect / must-fix | The clause's positive path presumes saved bytes it never tells a worker to save | OPEN |
| F21 | defect / must-fix | `docs/language-defects.md` counted 61 rules over a home holding 60 | FOLDED at 01:20 by another session, verified |
| F22 | recommendation / should-fix | R268.5 lost the installer's own red-first proof on a planted defect | OPEN |
| F23 | recommendation / should-fix | R91.2 lost the sentence saying only the human's asked word raises the lane cap | OPEN |
| F24 | recommendation / should-fix | The sub-list's normativity is undeclared: two bullets carry *shall*, 208 read descriptively | OPEN |
| F25 | recommendation / should-fix | R124.2's last bullet lost its *shall* and sits under a list introduced as what the validation confirms | OPEN |
| F26 | recommendation / should-fix | M-471 reads *todo* while the gate enforces the surface list today | OPEN |
| F27 | recommendation / should-fix | Rule `r47` reads `stated-only` while its `armed` field names `session-prompt-hook` | OPEN |
| F28 | recommendation / should-fix | Two readability arms sit exactly at their recorded counts, so the next unrelated criterion reds | OPEN |
| F29 | recommendation / should-fix | R300.13 states a duty with no way for a maintainer to tell when it applies | OPEN |
| F30 | recommendation / should-fix | `templates/agent.template.md` binds the clause to a card a worker never reads | OPEN |
| F31 | recommendation / should-fix | Two of the five clause homes name no gate | OPEN |
| F32 | recommendation / should-fix | The new renderer writes each rule in full under every surface it binds; R300.13's `*where*` guard is now dead | OPEN |

## Phase 1 — the model

**Entities.**

- **A rule** — one entry in `guardrails/language-rules.json`, carrying `id`, `name`, `rule`,
  `reader_test`, `surfaces`, `status`, `catchers`, `armed`, `sources`, `notes`, and optionally
  `examples`, `exceptions`, `thresholds`, `personal_override`. Sixty rules stand today, ids `r01` through
  `r62` with two numbers unused.
- **A catcher** — one of `pattern`, `model`, `person` under a rule, each with a `status` of `held`,
  `partial`, or `absent`, a `where`, and for the model a `law_text`.
- **A surface** — one of `spec-body`, `human-prose`, `chat`, `artifact`, `commit`, `worker-brief`, the
  tuple `SURFACES` in `scripts/gen-language-consumers.py`.
- **A consumer** — an artifact built from the home: `hooks/language-laws.json` and
  `docs/language-rules.md`.
- **A criterion** — a numbered line under a requirement's case, and, since this delta, the indented
  bullet sub-list under that line.

**States of a rule.** `held` — a catcher runs it at a named event, a gate, or a named manual step; exits
to `stated-only` when its catcher is removed. `stated-only` — nothing runs it, which covers a script that
exists and is armed nowhere; exits to `held` when a catcher is wired. `claimed-but-absent` — a home names
a catcher that does not carry the rule; no rule sits here today. No state is a dead end.

**Actors.** The writer edits the home. The generator writes both consumers. The gate reads the home and
compares the consumers against a fresh build. The register judge and the pre-show document lint read
`hooks/language-laws.json` at run time. A cold reader produces the findings that become classes. The
person who names a class and writes it into the home is the writer again.

**Composition.** The home sits under the guardrails node in `ARCHITECTURE.md`, which owns INV-292 through
INV-297 and pins all five files. `hooks/register_judge_core.py` reads the generated law bodies, so the
judge node and the guardrails node meet at `hooks/language-laws.json`, and the artifact's own `reading`
field states the key shape both sides use.

### What I assumed

- I read `sources` as a record of every place that states a rule today, kept so a reader can find the
  restatements and a sweep can retire them. The new renderer's own words — "kept so a reader can see where
  the rule used to live, and so a sweep can retire the duplicates" — confirm that reading, and F1 rests on
  it.
- I read the worker-restore clause's five statements as one rule with five homes, so a difference between
  any two of them is a finding. The brief for this pass states that reading.
- I read a bullet under a criterion as part of that criterion's rule, since `guardrails/specformat.py`
  now returns it in `crit.pieces` and four of the five readability arms measure it. F24 asks whether a
  bullet may also carry a *shall*.
- I treated `git ls-files` returning nothing for `guardrails/check-worker-restore.py` and
  `guardrails/check-tier-refusal.py` as the tree still landing rather than as a decision to leave them
  untracked.

## Phase 2 — Requirement 300 against the machinery that exists

Ten of the twenty criteria describe something the shipped files do. Five outrun the implementation. Five
state process with no mechanism. Three pieces of the implementation the requirement never states.

**Criteria the machinery carries.** R300.1 (the home exists and holds the rules), R300.5 (the two
generated artifacts are the judge's law text and the reader's rendering —
`hooks/register_judge_core.py` loads `language-laws.json` and takes its chat and human-prose bodies from
it), R300.6 (`check_drift` names the differing artifact by its relative path), R300.12 (`surfaces` is a
required field and an unlisted surface reds), R300.14 and R300.15 (rule `r10` carries
`personal_override: {"exceptions": []}` beside its shipped `exceptions` entry, and the doc renders both),
R300.18 through R300.20 (rule `r61` states the class-with-examples law and every entry carries a `rule`
sentence over its `examples`).

### F1 — R300.3 calls a second statement a defect while the home records second statements by design

> "*if* a rule is stated in a second place, *then* `guardrails/check-language-rules.py` *shall* report
> that second statement as a defect." — Requirement 300, criterion 3 / Case: one home for the rules about
> text

Fifty-two of the sixty rules carry a `sources` list, 243 pins in total. `check_sources` in
`guardrails/check-language-rules.py` opens each pin and reds only when a repository path is absent or a
line number runs past the file's end. It reports no pin as a defect, and the gate greens on the current
home. A maintainer who adds a rule, lists the four format documents that already state it, and runs the
gate is told the rule is clean, and reads R300.3 as having checked what it never looked at.

Write R300.3 as the duty the home actually carries, and open the fold-back as its own criterion:

> 3. A rule *shall* record in its `sources` field every other place that states it today, and
>    `guardrails/check-language-rules.py` *shall* red a `sources` entry naming a repository file or a
>    line that does not exist. [INV-292]
> 4. A `sources` entry *shall* stand as a debt until that place is generated from the home or points at
>    it, and the debt *shall* carry an owning queue row. [INV-292]

`defect · direct-contradiction (contradiction)`

### F2 — R300.4 says every consumer is generated; three pattern hooks hold their own copies

> "`scripts/gen-language-consumers.py` *shall* build every consumer of these rules from that home." —
> Requirement 300, criterion 4 / Case: the consumers are generated from the home

The generator writes two files, `LAWS_REL` and `DOC_REL`. `hooks/scissors-scan.py`,
`hooks/hedge-scan.py`, and `hooks/affirmation-scan.py` each declare an inline `PATTERNS` list and read
nothing from `guardrails/language-rules.json`. The home's own `_comment` names the state plainly: "a
checker that keeps its own copy of a list is drift to fold back." So the requirement claims a property the
delivery deliberately deferred, and a reader who edits a scissors pattern in the home finds the running
hook unchanged.

Scope R300.4 to the two artifacts and give the pattern hooks their own criterion with a row behind it:

> 4. `scripts/gen-language-consumers.py` *shall* build the model-judge law bodies and the human rendering
>    from that home. [INV-293]
> 5. *where* a checker holds its own copy of a rule's word list, that copy *shall* carry a dated
>    fold-back row, and the home *shall* name that checker in the rule's `catchers`. [INV-293]

`defect · unenforceable-promise (discharge)`

### F3 — R300.2 demands fields most rules do not carry

> "Each rule *shall* carry its own sentence, the test a reader applies, the surfaces it binds, its
> thresholds, its exceptions, and its examples." — Requirement 300, criterion 2

`thresholds` appears on 9 rules, `exceptions` on 17, `examples` on 19, out of 60. `REQUIRED_FIELDS` in
`scripts/gen-language-consumers.py` names `rule`, `reader_test`, `surfaces`, `status`, and `check_shape`
in both the generator and the gate demands those four. So the criterion is false of the home as it ships,
and it omits `status`, which is the field the gate does demand.

> 2. Each rule *shall* carry its own sentence, the test a reader applies, the surfaces it binds, and its
>    status, and *shall* carry its thresholds, its exceptions, and its examples *where* it has any.
>    [INV-292]

`defect · unenforceable-promise (discharge)`

### F4 — three criteria promise a red for a missing catcher record; the check reaches one case

> "*if* a rule names no catcher and states no such reason, *then* the check *shall* red and *shall* name
> that rule." — Requirement 300, criterion 11 / Case: every rule names what catches it

`check_catchers` in `guardrails/check-language-rules.py` returns immediately for a rule whose `status` is
anything other than `held`. Thirty-five rules read `stated-only`. A rule added with
`status: "stated-only"`, no `catchers` object, and empty `notes` passes the gate silently, and R300.8 and
R300.9 — which demand the catcher record and the arming point on every rule — have no arm at all, since
`catchers` and `armed` sit outside `REQUIRED_FIELDS`. R300.10's "reason" is discharged today by the status
word, and R300.10 never says that a status word is the reason.

Two roads. (a) Widen the machine: add `catchers` and `armed` to `REQUIRED_FIELDS` and let `check_catchers`
demand a note from any rule with no `held` catcher — the cost is that each of the 35 `stated-only` rules
needs a note written. (b) Write the machine's own rule into the criteria — cheaper, and it keeps the
status vocabulary as the single answer. I prefer (b):

> 8. A rule *shall* carry a `catchers` record naming the pattern, the model, and the person, each with
>    its status. [INV-294]
> 9. A rule *shall* carry an `armed` record naming the event or the gate its catchers run at, or the word
>    `nowhere`. [INV-294]
> 10. A rule whose `status` reads `held` *shall* carry a catcher reading `held`, or *shall* say in
>     `notes` what holds it. [INV-294]
> 11. *if* a rule carries no `catchers` record, no `armed` record, or claims to be held with neither a
>     held catcher nor a note, *then* the check *shall* red and *shall* name that rule. [INV-294]

`defect · missing-outcome-check (postcondition)`

### F5 — R300.7 is universal; the check spares a whole class of pins

> "*if* a rule points at a file or a line that does not exist, *then* the check *shall* red." —
> Requirement 300, criterion 7

`check_sources` treats a pin opening with `~` as unread rather than absent, so the gate gives the same
verdict on a machine with no personal layer. That is the right behaviour and the gate's docstring states
it. The criterion states something else. On this machine 106 of 243 pins resolved under the home tree; on
a machine without it, all 106 go unread and the gate still greens, while R300.7 says every one of them
owes a red.

> 7. *if* a rule points at a repository file or a line that does not exist, *then* the check *shall* red;
>    a pin under the reader's own home tree *shall* be read where that tree stands and *shall* be
>    counted unread where it does not. [INV-293]

`defect · internal-conflict (consistency)`

### F6 — R300.16 and R300.17 declare a law and name no net

> "*when* one of these rules changes, the system *shall* read it against its relatives in the same pass."
> — Requirement 300, criterion 17 / Case: the family is worked in one pass

The declared-cross-cutting-laws sweep demands every declared law name its enforcer: a mechanical gate, the
prover's own judgment station, or the design review's recommendation (SPEC INV-150). These two name none.
`TEST_MATRIX.md` carries M-472 as `*todo*` with no test file behind it, and no script reads a change to
one rule against its relatives. R300.13 sits in the same state.

The honest net here is the prover's own station, since telling one rule's relatives from its strangers is
a meaning call:

> 17. *when* one of these rules changes, the prover *shall* read it against every rule sharing a surface
>     with it in the same pass, and the pass record *shall* carry that verdict line. [INV-296, INV-150]

`defect · missing-rule (invariant)`

### What the implementation does that Requirement 300 never states

Three facts ship with no criterion over them.

- **The gate reds two rules sharing an id or a name** (`check_shape` in
  `guardrails/check-language-rules.py`), and `tests/test_language_rules.py` covers it. No criterion
  demands one rule one handle.
- **The gate reads its surface list from the generator**, so `SURFACES` has one home. No criterion states
  the six surface names or that the list has one home.
- **The gate refuses to read drift when a rule cannot render**, and `hooks/language-laws.json` is escaped
  to ASCII so a law quoting the reader's own alphabet travels through the shipped-language gate as
  program data (`laws_text` in `scripts/gen-language-consumers.py`). That second one is load-bearing: it
  is what keeps `hooks/` inside the shipped set while the home carries Russian pattern text. No criterion
  states it.

Each owes a criterion under INV-292 or INV-293.

## Phase 3 — the 93 rewrites: did meaning survive?

I read all 93 pairs through `git diff PRODUCT_SPEC.md` against `git show HEAD:PRODUCT_SPEC.md`. Most are
clean: an enumeration moved down, a gloss moved down, a participial tail turned into a bullet with its own
subject. Six changed a duty, a trigger, a scope, or an exception — F9 through F14 — and three more shifted
weight without losing a duty outright, F22, F23 and F25.

### F9 — the criterion's "only" now excludes what its own bullet permits

> "*when* a cleanup would touch a shared resource, the system *shall* act only on what this run provably
> owns, and *shall* leave a resource in current use untouched." — Requirement 117, criterion 1 / Case: the
> test is current use and provable ownership

The line before the rewrite read "act only on what this run provably owns **or a prior run whose recorded
owner is provably dead**". The disjunct moved into a bullet reading "the run may also act on a prior run's
resource whose recorded owner is provably dead". The word "only" stayed on the line, so the line and the
bullet now contradict. A session that reads the line and stops refuses to reap a dead prior run's temp
tree, its port, and its lock, and the machine accumulates them until a person clears them by hand. A
session that reads the bullet does the opposite. The pack's own reaping habit rests on the disjunct.

> 1. *when* a cleanup would touch a shared resource, the system *shall* act only on what this run provably
>    owns or on what a prior run whose recorded owner is provably dead left behind, and *shall* leave a
>    resource in current use untouched. [INV-162, INV-157]
>    - a shared resource is a process, a temp directory, a port, a file, a lock, or the display.

`defect · direct-contradiction (contradiction)`

### F10 — a stand-down criterion carries a bullet saying the thing still runs

> "*when* a kind has no element a person acts on, the system *shall* stand the design review down by name
> in the record rather than run it vacuously." — Requirement 61, criterion 5 / Case: the review runs in the
> kind's own form

Its first bullet reads "the review still runs in the project kind's own form, the way the verify walk and
the design principles do". Under the criterion's own trigger the review stands down and the bullet says it
runs. Before the rewrite the participle "running it in the project kind's own form" hung off the general
rule and reached past the trigger; a bullet is scoped to its criterion, so the rewrite pulled it inside.
A session on a kind with no acted-on element now has two answers and picks one.

Lift the two bullets to their own criterion outside the trigger:

> 6. The design review *shall* run in the project kind's own form, the way the verify walk and the design
>    principles do, and the spec's own declared-class check *shall* keep governing *where* a class is
>    already declared. [INV-141, INV-125]

`defect · direct-contradiction (contradiction)`

### F11 — R294.1 dropped a shipped behaviour its declared sibling kept

> "*when* any message the seat showed since the last human turn carries an empty-validation phrase, the
> system *shall* block the stop in the after-the-fact shape the scissors scan and the hedge gate take." —
> Requirement 294, criterion 1 / Case: the validation gate

The line before the rewrite read "carries an empty-validation phrase from the pattern list, **after a
quoted, backticked, or fenced span is stripped**, the system *shall* block the stop with a rewrite
instruction reaching the seat one message later". `hooks/affirmation-scan.py` strips quoted, backticked
and fenced spans before matching, so the code holds the rule the criterion dropped. Requirement 232,
criterion 1 — the hedge gate, which R294.1 itself names as its sibling — was rewritten in the same pass and
kept it as a bullet: "a quoted, backticked, or fenced span is stripped from the message before the pattern
list is matched."

So two criteria the spec itself declares same-kind now state one behaviour two ways. A session quoting a
banned phrase to discuss it reads as a violation under the spec as written and passes under the code, and
a host implementing the empty-validation arm from the spec alone ships a scan that fires on its own
documentation.

Give R294.1 the bullet its sibling carries, in the same words. This is the rewrite loss the suite could
not catch: no test compares a criterion against the hook it governs, and both criteria pass every
readability arm.

`defect · direct-contradiction (contradiction)`

### F12 — R244.2 dropped the sentence that turns a count into a verdict

> "*when* an architecture is re-proven, the system *shall* have each node re-answer the three fitness
> questions on its pins." — Requirement 244, criterion 2 / Case: co-residence is the counted signal

The line before the rewrite carried the three questions and then the load-bearing consequence: "two nodes
sharing one file answering the parallel-work question no." The three questions survive at Requirement 119,
criterion 1, so nothing is lost there. The consequence survives only in Requirement 244's Context block,
which is prose over the criteria rather than a criterion.

The requirement's title, its case heading, and its ratchet all rest on that link. Criterion 1 counts
nodes-per-file and rejects raw size; nothing now says what a count of two means. A person watching a file
grow to hold two nodes reads criterion 1, gets a number, and finds no criterion that turns it into a
failed fitness answer.

> 2. *when* an architecture is re-proven, the system *shall* have each node re-answer the three fitness
>    questions on its pins, and two nodes whose pins name one file *shall* answer the parallel-work
>    question no. [INV-233, INV-122]

`defect · missing-rule (invariant)`

### F13 — the only statement of "the show rule" is gone

> "*when* the card opens, the system *shall* open it by the show rule, and *shall* pass the pre-show
> register lint on the fixed copy and the rendered values before it opens." — Requirement 186, criterion 4

The line before the rewrite carried the gloss — "a new browser window on a local seat, its own channel on
a remote seat". The gloss is gone and no bullet took it. The term is used at Requirement 182, criterion 7
and here, and appears in no glossary entry, so the document now uses a term it defines nowhere. R297.2
says a criterion uses a term the glossary already defines.

Add the glossary entry and leave both criteria as they stand:

> - **show rule** — how a rendered artifact is opened: a new browser window on a local seat, its own
>   channel on a remote seat.

`defect · missing-rule (invariant)`

### F14 — a waiver's subject turned around

> "- a genuine offence is waived as counted debt through the dated allowlist." — Requirement 151,
> criterion 2 / Case: the project-name arm

The line before the rewrite read "a fixture name that ever falls beside a date redding and a genuine one
waived as counted debt through the dated allowlist." There "a genuine one" is a genuine fixture name — a
legitimate name that happens to sit beside a date. The bullet now says a genuine **offence** is waived,
which reverses the subject: the arm exists to red project names beside dates, and the criterion now tells
a maintainer that a real one gets waived. Someone reading it adds true offences to
`scripts/shipped-language-allowlist.json` and the arm stops meaning anything.

> - a fixture name that ever falls beside a date still reds;
> - a legitimate fixture name so caught is waived as counted debt through the dated allowlist.

`defect · direct-contradiction (contradiction)`

### The rewrites that held

Worth recording, so a later reader knows the sample was wide. Requirement 43, criterion 5 (three-source
disagreement) split a dash-list into three routing bullets with no change of home. Requirement 45,
criterion 3 (the closed set of entry points) turned eight welded routes into eight bullets, each naming
its entry. Requirement 130, criteria 5 through 9 (the compaction stations) split five welded criteria and
kept every duty on a *shall*. Requirement 196, criterion 12 (the message identifier) moved the identity
recipe into a bullet and left the minting duty on the line. Requirement 263, criterion 5 (a scoped
guarantee) moved the domain-part list down and gained clarity. Requirement 173, criterion 4 (the three
intake verdicts) is the cleanest of the 93: three parallel facts, three bullets, one duty on the line.

Requirement 263, criterion 1 gained words rather than losing them — "each end standing as its own decided
or default sentence" was added. That is a change of content inside a pass whose stated job was moving
overflow. It reads as right, and it is worth the author confirming it was meant.

## Phase 3b — composition

**Requirement 300 beside Requirement 297.** They govern different objects and do not collide: R297
governs how a criterion in `PRODUCT_SPEC.md` is written, R300 governs where the rules about this project's
texts live. The seam is `docs/language-rules.md`, which is a human-prose surface bound by rules the home
carries. It composes.

**Requirement 300 beside the register machinery (INV-203, INV-166, INV-173).** These now compose through
one artifact rather than by agreement: `hooks/register_judge_core.py` takes its chat body and its
human-prose body out of `hooks/language-laws.json` instead of carrying Python constants. That is the
strongest structural move in the delta. The residue is F2 — the pattern tier still holds its own lists, so
the model tier and the pattern tier of one rule are edited in two places.

**Requirement 300 beside the compaction station (R130.5, INV-115).** F32 opens here.

### F7 — the shipped fifth readability arm rests on no criterion

> "**Case: the four reading defects**" — Requirement 297

`guardrails/criterion-readability.json` now declares five arms, and
`guardrails/check-criterion-readability.py` lists `criterion-load` in `ARMS` with `max_total_words` 60 and
a recorded count of 42. R297.6 says the check reads the criteria "through one readability arm per defect".
A reader counts four defects in R297 and finds five arms in the config. The arm that reds a criterion by
summing its line and its bullets — the one that closes the loophole this delivery created — stands on no
stated rule, so nobody can fold it, argue with it, or re-derive its cap.

`docs/spec-format.md` carries the same stale count at its lint list: "the criterion-readability ratchet —
four arms over the acceptance criteria". That document is what a host reads.

> 6. A criterion's line and its bullets together *shall* state one rule within the recorded total cap.
>    [INV-287]

Renumber the case's criteria, retitle the case, and correct `docs/spec-format.md`.

`defect · missing-rule (invariant)`

### F8 — the criterion sub-list is a format element no format law states

`guardrails/specformat.py` gained `Bullet`, `crit.bullets`, and `crit.pieces`, and 93 criteria now carry
210 bullets. `docs/spec-format.md` still describes a case as "one bold line naming a situation, followed
by two to six numbered criteria", and describes a criterion as one line whose anchor "trails at the line's
end". Requirement 277, criterion 4 states the criterion form and says nothing about a sub-list. So the
pack's own spec uses a shape the pack's own format law never names, and a host adopting the format writes
criteria that the pack's parser reads one way and the host's reader reads another.

Two things to write. In `docs/spec-format.md`, under "The criterion form": a criterion may carry its
remaining pieces as an indented bullet sub-list under its own line; the sub-list ends at the next
criterion, the next case heading, the next requirement, or a blank line followed by unindented text; a
bullet carries no code anchor. In `PRODUCT_SPEC.md` under Requirement 277:

> 7. A criterion *shall* carry its remaining pieces as an indented bullet sub-list under its own line, and
>    a bullet *shall* carry no code anchor. [INV-251]

`defect · missing-rule (invariant)`

## Phase 3c — liveness and safety

**Can the home reach a state where a rule is unreachable by every catcher and nothing reports it?** Yes,
by two roads. The first is F4: a rule with `status: "stated-only"`, no `catchers` and no `notes` passes
the gate in silence. The second is quieter. A rule can read `status: "held"` while its `armed` field reads
`nowhere` — the gate never compares the two fields, and the doc renders "**Status.** held, armed at
nowhere" without complaint. No rule sits in that state today. Rule `r47` sits in its mirror image (F27):
`status: "stated-only"` while `armed` names `session-prompt-hook`. A criterion tying the two fields would
close both:

> A rule reading `held` *shall* name an arming point other than `nowhere`, and a rule naming an arming
> point *shall* read `held`. [INV-294]

**Can the generator write a consumer the gate accepts while the home says something else?** For the two
generated artifacts, no. The gate loads the generator itself (`_load_generator`) and rebuilds through the
one builder, so there is no second renderer to drift. `validate` re-parses the law artifact and asserts
every model-held rule's `law_text` appears in the body its `where` names, and asserts each rule has a doc
entry. `write` runs after both artifacts are built and validated, so a failure leaves the disk untouched.
That is the all-or-nothing convention held properly.

One gap sits at the edge of that guarantee. `model_checkers` takes the first word of each comma-separated
home in `catchers.model.where` and calls it the checker path. A `where` written with a leading article, or
with the mechanism named before the checker, silently produces a body keyed to a path no checker asks for,
and every check stays green: the gate compares the artifact against a fresh build off the same malformed
source, and `validate` looks for the law text inside the body the same parse produced. So the law reaches
nobody and every verdict reads clean. The convention lives in the source's `_comment` and nothing enforces
it.

> A `catchers.model.where` entry *shall* open with the path of the checker that runs the law, and the
> generator *shall* refuse a `where` whose opening word names no file in the repository. [INV-293]

**Atomicity of the family pass.** R300.17 asks that a change to one rule be read against its relatives in
the same pass. Nothing makes that pass atomic: a session can edit one rule, regenerate, commit, and the
relatives stay as they were with every gate green. F6 covers the missing net; the atomicity reading is
what makes it worth a net rather than a habit.

## Phase 3d — the delta's other machinery

### F15 — the worker-restore gate is BLOCKING and nothing runs it

> "It is BLOCKING and rides the verify step rather than the push chain, the same placement
> `check-runaway-child.py` takes." — `guardrails/README.md`, the worker-restore gate section

`skills/build-pipeline/SKILL.md` names the script inside a prose clause about what the brief carries. It
does not place the script in the verify step's run list. The script appears in no push-gate chain, in no
CI workflow, and in no suite test that runs it against the default transcript root:
`tests/test_worker_restore.py` passes `--root` a fixture directory in every case. So the gate reds
correctly on a planted transcript and has never once read a real worker run.

The consequence is the incident the gate was built for. A worker runs
`git checkout -- engine/assets/exhibition.js`, a sibling lane loses its uncommitted work, and the gate
that would have named the run sits on disk with nobody calling it. The orchestrator's verify step reads a
green suite and accepts the worker's result.

Two things: add the call to the verify step's own list in `skills/build-pipeline/SKILL.md`, and add one
suite test that runs the gate against the default root with `--since-hours` scoped to the session, so a
real red reaches a person and the stand-down path is exercised on a machine that has transcripts.

`defect · hard-to-monitor (observability)`

### F16 — two new machines own no architecture node and no matrix row

`ARCHITECTURE.md` carries zero occurrences of `check-worker-restore`, `check-tier-refusal`, or
`tier-refusal.json`, and `TEST_MATRIX.md` carries zero. Requirement 124, criterion 4 states that the
system lands no wish whose facts lack an owning architecture node and a matrix row at the right level. Two
BLOCKING scripts, one data file, two test files, and two `docs/measure/` records stand outside both
documents. The language-rule family landed its owns entries and its pins in the same tree, so the road is
open and these two rows did not take it.

`defect · boundary-issue (composition)`

### F21 — a human-facing page counted 61 rules over a home holding 60

At 01:06 `docs/language-defects.md` opened with "`docs/language-rules.md` carries all 61 of them, one
entry each" and repeated the number at "Of the 61 rules, 34 are armed nowhere today". The home holds 60
rules and the generated page renders 60 unique entries; the 34 was right. Another session rewrote the page
before this record was written, and both claims are gone from the tree at 01:35. Recorded so the next
reader does not re-open it, and so the class stays visible: a hand-kept count over generated contents is
the shape that produced it.

`defect · internal-conflict (consistency)` — FOLDED, verified

## Phase 3e — mandatory sweep verdicts

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| `guardrails/language-rules.json` (the home) | hit — F6, no net on R300.16, R300.17, R300.13 | hit — `status` and `armed` may disagree unbounded (F27, Phase 3c) | clean — one rule, one entry, one id | hit — a rule's move from `held` to `stated-only` has no stated trigger | hit — a malformed `where` passes every check (Phase 3c) |
| `scripts/gen-language-consumers.py` | clean — INV-293 names the gate | clean — `BuildError` before any write | hit — F32, the renderer's repetition rule sits in code alone | N/A — the generator holds no state across runs | clean |
| `hooks/language-laws.json` + `docs/language-rules.md` | clean | clean — drift reds, absence reds | hit — F2, the pattern tier is a consumer outside the generator | N/A — generated output | clean |
| `guardrails/check-language-rules.py` | clean — INV-292 and INV-294 own it | hit — F5, the home-tree pin class | clean | N/A | clean |
| The criterion sub-list | hit — F8, no format law states it | clean — the sub-list's end conditions are stated in the parser | hit — F7, R297's four-defect enumeration | N/A | hit — F24, a bullet's normativity |
| The worker-restore clause | hit — F15, the net is armed nowhere | hit — F17, five command forms against four | hit — F18, shared tree against every tree | hit — F19, HALT has no exit; F20, no save precondition | hit — the orchestrator and a sibling main-thread session are unbound |

The quantifier re-verify (SPEC INV-170) fired on four sentences. "the four reading defects" (Requirement
297's case heading) is falsified by the fifth arm — F7. "four arms over the acceptance criteria"
(`docs/spec-format.md`) — F7. "The four commands are…" in five prose homes — F17. "all 61 of them"
(`docs/language-defects.md`) — F21, folded. Two sentences re-verified clean: `SURFACES` names six surfaces
and the home binds only those; `REQUIRED_FIELDS` names four and both readers demand the same four.

CRUD and authorization tables are N/A here: the product is a method pack with no user-mutated persistent
entity and one operator. The surface-by-sweep table above stands in their place (SPEC INV-171).

## Phase 4 — the worker-restore clause

I read all five statements. They say nearly the same thing, and the differences are where the findings
sit.

**What all five carry, in the same words.** The positive act — a worker that mutated a file puts it back
by writing its own saved bytes. The banned set — `git checkout -- <path>`, `git restore`, `git stash`,
`git reset --hard`. The reason — the blast radius is a path, so the damage lands on files the worker never
wrote and its brief never named. The failure branch — a worker that believes a file needs a git-level
restore halts and reports, and the orchestrator owns recovery. The orchestrator's half — a finished build
stage is committed before the next worker touches its files.

**Where they differ.** `skills/live-spec-base/SKILL.md` and
`skills/build-pipeline/references/delegation-protocol.md` add why brief-time disjointness gives no cover.
The delegation protocol adds the incident history and the sentence that the clause rides every brief it
composes. `skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md` and the delegation protocol
name the gate; `templates/agent.template.md` and `scripts/open-lane.sh` do not (F31).
`templates/agent.template.md` binds "a worker acting under this card", and a card describes a project's
agent rather than a brief a worker reads, so the clause's reach there is narrower than in the other four
(F30).

**Is the rule stated positively?** Yes. Every statement opens on what a worker does and reaches the
prohibition second. That is the right order and it survived five copies.

**Is it complete?** Four gaps, F17 through F20.

### F17 — the gate reds five command forms; every brief names four

`guardrails/check-worker-restore.py` reds `git clean` with `-f` or `-x`, and reds `git reset --merge` and
`git reset --keep` beside `--hard`. All five prose statements name four commands and stop; none of the
five contains the string `git clean`. The gate's own red message admits it: "The four named commands —
git checkout -- <path>, git restore, git stash, git reset --hard — reach past the brief's write-set by
construction, and so does git clean." A worker briefed verbatim runs `git clean -fd` believing it obeyed,
the sibling lane's untracked file is gone, and the gate reds after the bytes are.

Add `git clean` and the two other reset modes to the enumeration in all five homes, in one wording.

`defect · internal-conflict (consistency)`

### F18 — the headline scopes to the shared tree; the body and the gate reach every tree

Three of the five statements head the clause "No worker restores the shared working tree". The body in all
five forbids any command that discards uncommitted work, with no tree qualifier.
`guardrails/check-worker-restore.py` states the position plainly: "It cannot tell whether the worker ran
inside its own isolated worktree, where no sibling's bytes were at risk; that case reds like any other."

`scripts/open-lane.sh` is the one script in the pack that gives a lane worker a private worktree, and it
is where the clause is pasted verbatim. So the parallel-lanes road hands every lane worker a rule its own
gate reds on inside a tree where nothing was at risk, and the worker has no way to tell from the clause
which reading is meant.

Decide it in the clause. Either bind it to every tree and drop "shared" from the three headlines, or bind
it to the shared tree and give the gate the worktree read — `git rev-parse --git-common-dir` off the
recorded `cwd`. I prefer the first: it is one rule a worker carries with no state to check, the positive
path stays available inside a lane worktree, and the gate needs no change.

`defect · internal-conflict (consistency)`

### F19 — the failure branch ends at HALT

All five statements close the failure branch at "HALTS and reports, and the orchestrator owns recovery".
No statement says what recovery is, what the orchestrator does with the halted row, or how long the worker
waits. A halted lane has no stated exit, and the orchestrator has no stated act. The delegation protocol
comes closest — "a worker that hits a broken file has a commit to be recovered from" — and that is the
precondition for recovery rather than the act.

`defect · stuck-state (liveness)`

### F20 — the positive path presumes bytes nobody was told to save

"Puts it back by WRITING ITS OWN SAVED BYTES" appears in all five. Nothing tells a worker to read and hold
a file's prior bytes before mutating it. The pack's own red-first method mutates a shipped artifact to
prove a row red, which is exactly the case that produced both incidents, and a worker that mutated without
saving has no path the clause offers: HALT is stated for "a worker that believes a file needs a git-level
restore", and this worker knows it needs one.

`defect · missing-prerequisite (precondition)`

### The spec criteria I would add

Requirement 301 is free, and INV-298 and INV-299 are unclaimed. Written in the document's own format, and
with the four gaps above closed:

---

## Requirement 301: A worker restores a file it mutated by writing its own saved bytes

**Context:** A worker writes the files its brief names. A git command that discards uncommitted work is a
different act: its blast radius is a path, so it lands on files the worker never wrote and its brief never
named. The brief-time write-set disjointness that fences concurrent edits holds the writes apart and says
nothing about a command that reaches past them, and the `git status` a careful worker pastes afterwards
reads clean in the safe case and the destructive one alike. So a worker keeps its own saved bytes and puts
them back itself. The pack's own red-first method mutates a shipped artifact to prove a row red, so this
act recurs in every parallel session, and the clause rides every brief. The orchestrator's half of the
rule is that a finished build stage is committed before the next worker touches its files, so a worker
that meets a broken file has a commit to be recovered from.

**User Story:** As a person whose session holds uncommitted work, I want a worker to put back only what it
wrote, so that my unsaved edits survive another lane's repair.

### Acceptance Criteria

**Case: the worker holds its own bytes**

1. *when* a worker intends to mutate a file it will put back, the worker *shall* read and hold that file's
   bytes before the mutation. [INV-298]
2. *when* a worker puts a file back, the worker *shall* write its own saved bytes. [INV-298]
3. A worker *shall* run no command that discards uncommitted work in any tree. [INV-298]
   - the commands are `git checkout -- <path>`, `git checkout .`, `git restore` outside `--staged`,
     `git stash` and its `push`, `save`, `create` and `store` forms, `git reset` with `--hard`, `--merge`
     or `--keep`, and `git clean` with `-f` or `-x`;
   - a worker inside its own isolated worktree holds the same rule, since the tree it stands in is the one
     thing it cannot read off its own brief.

**Case: a worker with no saved bytes halts**

4. *when* a worker holds no saved bytes for a file it mutated, the worker *shall* halt and *shall* report
   the file and the mutation it made. [INV-298]
5. *when* a worker believes a file needs a git-level restore, the worker *shall* halt and *shall* report
   what it read. [INV-298]
6. A halting worker *shall* write no further file and *shall* run no further command. [INV-298]

**Case: the orchestrator owns recovery**

7. *when* a worker halts under this rule, the orchestrator *shall* restore the named file from the last
   committed stage, *shall* re-brief the worker with that file's current bytes, and *shall* record the
   halt in the row's delivery report. [INV-298, INV-103]
8. The orchestrator *shall* commit a finished build stage before the next worker touches its files.
   [INV-298, INV-39]
9. A session holding the pen *shall* run no command that discards uncommitted work *while* another session
   or another worker holds uncommitted work in the same tree. [INV-298, INV-11]

**Case: the clause rides every brief**

10. Every brief a session composes for a worker *shall* carry this rule in the pack's own words.
    [INV-299, INV-173]
11. The pack *shall* state this rule in its shared rulebook, in the pipeline skill, in the delegation
    protocol, in the agent-card template, and in the lane-opening script, with one wording across all
    five. [INV-299]
12. *if* two of those homes state the rule with different words or a different command list, *then* the
    suite *shall* red and *shall* name both homes. [INV-299]

**Case: the mechanical arm**

13. `guardrails/check-worker-restore.py` *shall* read the worker runs' transcripts and *shall* red a run
    that handed a shell any command criterion 3 names. [INV-299]
14. The check *shall* read a command a worker handed to a shell and *shall* leave a report, a brief, or a
    plan that names such a command alone. [INV-299]
15. The check *shall* run at the verify step, and its verdict *shall* stand between a worker's result and
    the orchestrator's acceptance of it. [INV-299, INV-46]
16. *when* the transcript root does not exist, the check *shall* stand down by name and *shall* say what
    it read nothing of. [INV-299, INV-218]
17. *if* the transcript root exists and holds no worker-run transcript, *then* the check *shall* red by
    name. [INV-299, INV-218]
18. Each run *shall* state its reach: the transcript root, the file pattern it matched, the window it
    read, and the count of command lines it took. [INV-269]

---

Codes to open: **INV-298** (a worker restores by writing its own saved bytes, and halts where it holds
none) and **INV-299** (the clause has one wording across five homes and a mechanical arm at the verify
step). Matrix rows to open beside them: one per case, at string level over the five homes and over the
gate's own fixtures, plus the real-root run F15 names.

Two of these criteria state something the shipped clause does not say today, and I read them as intended
rather than decided. Criterion 9 binds the orchestrator and a sibling session, where the gate today reads
a main-thread restore as the orchestrator acting and allows it. Criterion 12 asks the suite to compare the
five homes' wording, where `tests/test_worker_restore.py` today asserts each home carries the clause
without comparing them. Both are questions for the author, and they sit in Phase 5.

## Phase 5 — closing

### Top three to fold before the push

1. **F1 and F4 together** — Requirement 300's criteria promise reds the gate does not issue. Whichever
   road the author picks, the criteria and `guardrails/check-language-rules.py` have to say one thing.
2. **F11** — R294.1 dropped a rule that ships, and its declared sibling kept it. That is the rewrite loss
   the suite could not catch.
3. **F15 and F16** — a BLOCKING gate nothing runs, and two machines with no owning node and no matrix row.

### Properties to state in the document

- A rule reading `held` names an arming point other than `nowhere`, and a rule naming an arming point
  reads `held`.
- A `catchers.model.where` entry opens with the path of the checker that runs the law, and the generator
  refuses a `where` whose opening word names no file in the repository.
- One rule carries one id and one name.
- The six surface names have one home, and both the generator and the gate read that home.
- A criterion carries its remaining pieces as an indented bullet sub-list under its own line, and a bullet
  carries no code anchor.
- A criterion's line and its bullets together state one rule within the recorded total cap.
- Two nodes whose pins name one file answer the parallel-work question no.

### Open questions for the author

1. Is `sources` a permanent record of where a rule is restated for a reader, or a debt ledger to be
   emptied as each place is generated from the home? The new renderer's wording — "so a sweep can retire
   the duplicates" — reads as the second, and F1's repair takes that shape unless you say otherwise.
2. Should the three pattern hooks read their lists from the home, and on which row? F2 stands until that
   is decided; the home's `_comment` already calls the copies drift to fold back.
3. Does the worker-restore rule bind the orchestrator and a sibling main-thread session, or workers alone?
   The gate today reads a main-thread restore as lawful, and the tlvphotos near miss was a sibling-lane
   collision that a main-thread restore reproduces exactly.
4. Should a lane worker inside its own worktree be free to run `git restore` there? F18 asks the pack to
   pick one reading, and `scripts/open-lane.sh` is where the answer lands.
5. May a bullet carry a *shall*? Two of the 210 do. F24 stands until the format law says.
6. Requirement 263, criterion 1 gained a clause during a pass whose job was moving overflow. Was that
   meant?

### Recommendations queued for a taste call

- **F22** — Requirement 268, criterion 5's bullet reads "follows the four project-side checks' shipping
  contract … and their red-first attachment proof" where the line before the rewrite read "prove itself
  red-first on a planted defect". The four checks' own proof is owned at Requirement 228, criterion 6, so
  the installer's block no longer owes a red-first proof of its own, under a case headed "wire the push
  gate red-first". `recommendation · now · missing-outcome-check (postcondition)`
- **F23** — Requirement 91, criterion 2 dropped "raised for the session only by the human's asked word".
  The duty survives at Requirement 80, criterion 2, so nothing is lost from the document; the criterion
  now reads as though the cap is fixed. `recommendation · later · over-general (abstraction)`
- **F24** — of the 210 bullets, two carry a *shall* (Requirement 226 criterion 2, Requirement 261
  criterion 7) and 208 read descriptively. A reader has no rule for telling a bullet that binds from a
  bullet that explains, and the count moved during this pass as a sibling session edited one of them.
  `recommendation · now · confusing-for-users (cognitive-load)`
- **F25** — Requirement 124, criterion 2's bullets are introduced as what the coverage validation
  confirms, and the last one states a separate duty about the matrix row lint and the matrix-reference
  gate, with its *shall* dropped. `recommendation · now · boundary-issue (composition)`
- **F26** — M-471 reads *todo* while `surfaces` is a required field the gate enforces and
  `tests/test_language_rules.py` covers through `check_shape`. The matrix understates what ships.
  `recommendation · now · hard-to-operate (ops-ux)`
- **F27** — rule `r47` reads `status: "stated-only"` with `armed: ["session-prompt-hook"]`. One of the two
  fields is wrong, and the counts split on it: 35 rules read `stated-only` and 34 read `armed: nowhere`.
  `recommendation · now · internal-conflict (consistency)`
- **F28** — `anchor-noise` reads 61 against a recorded 61 and `criterion-load` reads 42 against 42. The
  next criterion carrying four codes, or a sub-list summing past 60 words, reds a landing that has nothing
  to do with readability. The three prose arms carry real headroom. Worth a rebaseline run or a stated
  decision that zero headroom is the intent. `recommendation · now · stuck-state (liveness)`
- **F29** — R300.13 says a rule whose verdict differs by surface holds one entry per surface, and nothing
  tells a maintainer how to recognize a differing verdict or what to do when one appears.
  `recommendation · later · unclear-owner (actors)`
- **F30** — `templates/agent.template.md` binds the clause to "a worker acting under this card". A card
  describes a project's agent; a worker spawned by another project's session never reads it.
  `recommendation · now · boundary-issue (composition)`
- **F31** — `templates/agent.template.md` and `scripts/open-lane.sh` state the clause and name no gate, so
  a worker briefed from either cannot tell the rule is mechanically read.
  `recommendation · later · hard-to-operate (ops-ux)`
- **F32** — `scripts/gen-language-consumers.py`'s document renderer was replaced during this pass. It now
  writes each rule in full under every surface it binds: 60 rules become 184 entries and the page runs
  4338 lines. The reason is stated in the code and it is a good one — a reader told to read one section
  met pointers instead of rules. Two consequences follow. R300.13 says a rule holds one entry per surface
  *where* its verdict differs by surface, and the renderer now does it for every rule, so the `*where*`
  guard governs nothing. And the compaction station (Requirement 130, criterion 5) audits every living
  document for redundant information; this one repeats each rule up to six times by design. Generated
  output is a defensible carve-out from that station, and the carve-out is stated nowhere.
  `recommendation · now · boundary-issue (composition)`

### Acknowledged gaps

The delta carries one the author already named: the worker-restore clause has no spec criteria. Phase 4
writes them. The `[GAP: ...]` markers inside two rewritten criteria — Requirement 156, criterion 1's
strong-reaction measure and Requirement 266, criterion 3's payload-size measure — are pre-existing and
unchanged by this delta. Both survived their rewrite with the marker attached, which is the right
handling.

`acknowledged · missing-rule (invariant)`

### The `[default]` count

Three criteria in the document carry a literal `[default]` tag, all in Requirement 186: criteria 13, 14
and 16, covering the settings card's one-column reading on a narrow window, its static-page-with-no-hover
shape, and its read-only render. The delta added none and removed none. Three unratified defaults is a
short enough list to hand over whole rather than sample, and none of them is urgent: each names a shape a
person can see for himself the first time the card opens.

### Readiness

The design is sound and the machine under Requirement 300 is better than the requirement that describes
it. Needs another iteration: fold F1 through F20, then push.
