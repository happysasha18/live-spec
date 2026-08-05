# Prover record — the readability day's spec re-check, 2026-08-05

Prover skill: product-prover, live-spec pack v4.3.0. Mode: full re-read of `PRODUCT_SPEC.md` and
`ARCHITECTURE.md` against the five commits that changed them since the last record (SPEC M-6,
INV-116). Written by a seat that authored none of the work under review (SPEC INV-237).

## Scope

**What this record reviews.** The tree at `52aa815`, with the two working-tree edits to
`PRODUCT_SPEC.md` standing beside it. The last committed prover record is `b4e1425`. Five commits
have touched a guarded document since:

- `1d10642` — Requirement 304, two glossary entries, one architecture inventory line, three matrix
  rows;
- `6167a6e` — `ARCHITECTURE.md` rewritten, 537 lines added and 175 removed;
- `cefd11d` — Requirement 305, `INV-304`, `guardrails/check-push-review.sh` as gate ac, three matrix
  rows, seventeen tests;
- `a97f95b` and `52aa815` — one architecture line each.

Two edits stand uncommitted in `PRODUCT_SPEC.md`. The glossary entry for a public edition now points
at Requirement 304. Criterion 3 of Requirement 305 now points at the ladder `INV-208` states. Both
were made to bring the redundancy count back to its floor.

**Commands run.** Every number below comes from one of these.

- `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md` — 123 candidates, 119 open. The same
  script over the committed copy — 125 candidates, 121 open.
- `python3 scripts/spec-redundancy-precheck.py ARCHITECTURE.md` — 1 candidate, 0 open.
- `python3 scripts/spec-style-lint.py --gate` over both documents — 0 errors, 0 warnings, 0 stale
  waivers.
- `python3 scripts/rule-census.py` — `ARCHITECTURE.md` at 0 findings, longest sentence 25 words.
- `python3 guardrails/archformat.py` — exit 0, over the document's 22 nodes.
- `bash guardrails/check-pin-drift.sh` — 205 pins checked, five reported.
- `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` — 1631 of 1631 criteria well
  shaped across 305 requirements.
- `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — the
  committed index equals a fresh build, 388 codes agree.
- `python3 guardrails/check-vocabulary.py`, `check-weak-words.py`, `check-one-name.py`,
  `check-no-history.py` over `PRODUCT_SPEC.md` — each OK.
- `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md`, run over the working tree and
  over the committed copy — identical counts.
- `python3 guardrails/check-doc-findings-bound.py` — 127 live documents, none above its record.
- A word-token comparison of `ARCHITECTURE.md` across `6167a6e`, counting every rule code and every
  node heading on each side.
- A path comparison of the same two copies, with each path tested for a file on disk.
- Reading of `scripts/sync-mirrors.sh`, `guardrails/check-push-review.sh`,
  `guardrails/check-prover-record.sh`, `editions/product-prover/`, and the record home
  `docs/push-review/README.md` as `HEAD` holds it.
- `/private/tmp/.../scratchpad/suite-run-7.log` — 3 failed, 2358 passed.

**The record this pass stands on.** `docs/prover/2026-08-05-public-edition-and-reader-repairs.md`
holds eight findings. Requirement 304 folds three of them. Three stand open, and one of those three
is the strongest hole this pass carries forward. The section "The previous record, re-read" walks
each row.

## Verdict

**The specification holds. Ten holes stand, and each has a written fix. None of them blocks these
commits from going out.**

Requirement 304 and Requirement 305 are well formed, indexed, and claimed by matrix rows. The shape
gate reads all 1631 criteria as well shaped. The index equals a fresh build. The architecture rewrite
lost no rule code and no node. The old side carries 373 distinct codes and the new side 374. The one
addition is `INV-304`, and every node heading survives.

The holes fall in three groups. Requirement 304 describes a publish selection and leaves the two
copies free to drift apart. Requirement 305 defines the reviewed delta wider than any record can
name it, and leaves the word "blocking" to the reviewer with no bar. The architecture map carries
three pointers that name no file on disk and one pin that names text which moved.

The two redundancy repairs both still instruct. Neither lost a fact. The section "The two redundancy
repairs, judged" gives the evidence.

| # | Kind | Claim | Status |
|---|---|---|---|
| F1 | defect | An edition can fall behind the skill it was written from, and Requirement 304 states no tie | open |
| F2 | defect | The sync run ends green after refusing a skill, so a half-published set reads as a finished one | open |
| F3 | defect | Requirement 304 criterion 6 speaks of both copies from inside the case where one exists, and conflicts with criterion 8 | open |
| F4 | defect | A push review record cannot name the commit it rides in unless it rides alone, and no criterion says so | open |
| F5 | defect | Requirement 305 puts uncommitted work in the delta, and the record carries no field for it | open |
| F6 | defect | Nothing states what makes a finding blocking, and one free sentence reopens the push | open |
| F7 | defect | The base ladder's third rung narrows the reviewed range to one commit in silence, on two gates | open |
| F8 | defect | One architecture pin names a line where its labelled text no longer stands | open |
| F9 | defect | Three architecture pointers name a bare filename, and one of them names a file the pack does not ship | open |
| F10 | recommendation | The two redundancy repairs point in two different forms, a requirement number and a rule code | open |

## Phase 1 — the model, as the delta leaves it

**The publish selection.** Some skills in this pack also stand as public repositories. One script
rebuilds each of them from the pack. For each folder under `skills/`, the script resolves a publish
source and copies it over the mirror's contents. It then writes a banner, a release history and an
attribution line, scans the assembled README, and pushes. Requirement 304 states the selection. Where
`editions/<skill>/` exists, that directory is the source. Where it is absent, `skills/<skill>/` is.
Where it exists and holds no `SKILL.md`, the skill is refused by name and the run continues.

States of a skill at sync time:

1. **No edition** — entered when `editions/<skill>/` is absent; the mirror takes the skill folder.
2. **Edition published** — entered when the directory exists and holds `SKILL.md`; the mirror takes
   the edition, and a line names the skill and the directory.
3. **Refused** — entered when the directory exists and holds no `SKILL.md`. The mirror is left as it
   stands, the skip is recorded, and the run moves to the next skill.

**The push review.** Requirement 305 puts an adversarial review in front of every push. The reviewer
is briefed to find reasons to refuse the change. The review leaves a dated record under
`docs/push-review/`, committed before the push. Gate ac reads that the record exists, is committed,
and is fresh against the newest reviewed commit. It also reads that the record names the base commit
and every reviewed commit, and that five fields carry values. A blocking finding holds the push until
it is closed or explained.

States of a push:

1. **No record** — gate ac reds and prints the fix line.
2. **Record covering another range** — read as covering nothing; gate ac reds.
3. **Record fresh and covering** — gate ac reads the `Blocking:` field.
4. **Blocking item open** — the push is held.
5. **Blocking item closed or explained** — the push goes through.

**The architecture map.** `ARCHITECTURE.md` names 22 nodes. Each node states what it is for, which
rule codes it owns, and where its responsibility sits on disk as `file:line` pins. The rewrite at
`6167a6e` brought every sentence under the 25-word cap, corrected 59 line numbers, and wrote 40
shorthand pointers out in full. The guardrails node gained `INV-304`, the gate script's pin, and the
record home's pin.

**Actors.** The owner runs the sync from this machine. A stranger reads a public mirror. A session in
this project loads the copy under `skills/`. A maintainer preparing a push writes the review record
and runs the gate chain. A later session reads the architecture map to find the code behind a rule.

### What I assumed

- I read the case headings of Requirement 304 as scoping the criteria under them. F3 rests on that
  reading. Under the other reading, criterion 6 is a general rule, and it conflicts with criterion 8
  head on.
- I read `editions/product-prover/` as the only edition, from a listing of `editions/`. F1 rests on
  one edition existing today and more following.
- I treated the edition's own accuracy as outside this pass. Reading 42 kilobytes of rewritten method
  against its source is a pass of its own.
- I read the record home `docs/push-review/README.md` as `HEAD` holds it, because another session is
  writing that directory now. Findings F4 to F6 rest on the committed text.
- I found no queue row naming an edition, and no queue row naming the push review. Searches of
  `ROADMAP.md` for "edition" and for "adversarial" return the two rows quoted in the previous
  record's own area and nothing else. F1 rests on that search.
- The 25-word cap and the redundancy floor apply to the specification and the architecture. I applied
  them to this record as well.

## Phase 2 — the changed text, read against the machines

**What holds in Requirement 304.** The three cases match the script. `publish_source_for` at
`scripts/sync-mirrors.sh:77` returns the edition over the skill folder. The copy step at `:411` calls
it once and continues past a refusal. The print flag at `:95-101` exits above every clone. Ten
criteria carry `INV-303`, and matrix rows M-491, M-492 and M-493 claim all ten tests in
`tests/test_mirror_editions.py`. The language scan on the assembled README still runs after the copy.
So the declared language law reaches an edition's text the way it reached a skill folder's.

**What holds in Requirement 305.** The twelve criteria match the gate script's header line for line.
The script resolves the base through the same three rungs. It takes the commits in the range that
touch a file outside the review directory. It exempts a commit carrying the record alone. Criterion
12 and the script's own header both state what no script can decide. Matrix rows M-494, M-495 and
M-496 claim the seventeen tests, and M-496 names the known-red proof in
`guardrails/gate-red-proofs.json`.

**What holds in the architecture rewrite.** The rewrite is large, so I compared the two sides rather
than reading for a lost fact. Every rule code on the old side stands on the new side. Every node
heading stands. The census reads the document at zero findings with its longest sentence at 25 words,
against 88 sentences over the cap before. My path comparison caught nine bare filenames that gained
the directory which finds them, and each of the nine now resolves. F9 names the residue.

**What the two guarded documents say about each other.** Gate a compares the newest commit touching
`docs/prover/` against the newest commit touching each guarded document. Gate ac compares a record
under `docs/push-review/` against the commits in the pushed range. I checked the two for a cycle. A
lawful order exists. Land the specification edits and this record together, or the edits first. Then
land the push review record in a commit of its own. No order deadlocks. F4 names what happens to a
maintainer who lands the review record beside anything else.

## Phase 3 — findings

F1 — An edition can fall behind the skill it was written from, and Requirement 304 states no tie

> "the edition states the same method, with every internal code resolved into the rule it stands
> for" — PRODUCT_SPEC.md, Requirement 304, criterion 1

Requirement 304 states where an edition lives, when it publishes, and when it is refused. No
criterion binds its content to the skill it was written from. `skills/product-prover/SKILL.md` stamps
version 4.3.0. `editions/product-prover/SKILL.md` stamps `1.0.0-standalone` and says it follows no
pack version. `editions/product-prover/PROVENANCE.md` records the code-to-rule mapping and records no
source version. Nothing on disk says which skill text the edition was resolved from.

The person affected is a stranger reading the mirror after the next lens lands in the prover skill.
They run a method that is one release behind, and they never learn it. The owner sees the sync print
`product-prover: up to date`, because the edition itself has not changed. Nothing reds. This is the
previous record's F4, and Requirement 304 was written without folding it.

Add one criterion to Requirement 304. An edition *shall* record the skill version it was resolved
from, and the pack *shall* red where that version stands behind the skill's own. `PROVENANCE.md` is
the home for the stamp, since it already carries the mapping. Two options for the net. a) A guardrail
script comparing the two stamps, blocking and cheap. b) A test row reading both files, riding the
suite and off the push chain. I prefer (a), because the drift reaches the public.

`defect · stuck-state (liveness)`

F2 — The sync run ends green after refusing a skill

> "*when* a skill is refused, the sync *shall* run on to the remaining mirrors and *shall* record the
> skip in its summary." — PRODUCT_SPEC.md, Requirement 304, criterion 9

The criterion states the summary line and states nothing about the run's own result. The script
matches it. `scripts/sync-mirrors.sh:411-414` records the skip and continues, and the script ends by
printing the summary. The run exits zero with one public repository left unpublished.

The person affected is the owner running the sync from another script or from a scheduled job. That
caller reads the exit code, sees success, and reports every mirror published. The one refused mirror
keeps serving whatever it served before, and the summary line that names it scrolls past unread.

Add one criterion: *when* any skill is refused, the sync *shall* exit non-zero after printing the
summary. Two options for the wording. a) A non-zero exit for any skip, which also catches a mirror
with no reachable repository. b) A non-zero exit for a refusal alone. I prefer (b), because an
unreachable repository is a normal state for a skill that has no mirror yet.

`defect · partial-success-risk (atomicity)`

F3 — Criterion 6 speaks of both copies from inside the case where one exists

> "The pack *shall* stay the one source of both copies, so a hand edit on a mirror is overwritten."
> — PRODUCT_SPEC.md, Requirement 304, criterion 6, under "Case: a skill ships no edition"

The criterion sits in the case where `editions/<skill>/` is absent. In that case one copy exists, so
the phrase "both copies" reads against its own heading. Read as a general rule instead, it conflicts
with criterion 8 of the same requirement:

> "*when* a skill is refused, the sync *shall* publish no source for it and *shall* leave its mirror
> as it stands." — PRODUCT_SPEC.md, Requirement 304, criterion 8

Under a refusal, a hand edit on that mirror survives every sync. One criterion says a hand edit is
overwritten and another says the mirror is left as it stands. The person affected is a maintainer
reading Requirement 304 to answer whether a mirror can hold text no commit carries. The requirement
gives two answers.

Move criterion 6 out of the no-edition case into a case of its own, and scope it. The pack *shall*
stay the one source of every published copy. A hand edit on a mirror *shall* be overwritten at the
next sync that publishes to it. That wording leaves the refusal case alone and states which mirrors
the rule reaches.

`defect · direct-contradiction (contradiction)`

F4 — A push review record cannot name the commit it rides in unless it rides alone

> "a commit carrying the record alone is exempt from the naming rule, since a record cannot name the
> commit that first ships it." — PRODUCT_SPEC.md, Requirement 305, criterion 8

The exemption is written for one commit shape. Criterion 4 requires the record to be committed before
the push, and says nothing about the commit's contents. Criterion 5 requires the record to name the
commits it covers. A maintainer who commits the record beside the landing it reviews produces a
commit that touches a file outside `docs/push-review/`. That commit is a reviewed commit, and the
record inside it cannot name it. Gate ac reds.

The person affected is a maintainer following the normal landing habit of one commit per movement.
They write the review, commit the movement, run the push, and read a red naming a commit they cannot
add to a file already committed. The way out is an amend or a second commit, and no written source
names it.

Rewrite criterion 4 to state the shape: the record *shall* be one dated file under
`docs/push-review/`, committed on its own, after the commits it reviews. Add the reason as a
sub-bullet, so the reader learns why the commit stands alone. `docs/push-review/README.md` owes the
same sentence, since that page is what a person writing a record opens.

`defect · missing-prerequisite (precondition)`

F5 — The delta includes uncommitted work that the record carries no field for

> "The delta *shall* be every commit between the remote's head and the local head, read together with
> the work still uncommitted." — PRODUCT_SPEC.md, Requirement 305, criterion 2

> "The check *shall* hold the record's presence, its commit, its freshness, its named range, and its
> fields." — PRODUCT_SPEC.md, Requirement 305, criterion 11

The two cannot both hold. Criterion 2 defines a delta with two parts. The record's `Range:` field
names commits, and no field names uncommitted work. So criterion 11 holds a range that is narrower
than the delta criterion 2 defines. Criterion 12 lists three things the check leaves to the reviewer,
and uncommitted work is absent from that list.

The person affected is the maintainer at the next push. They stage half a movement, review the
committed half, and pass gate ac green. The uncommitted half reaches the remote in the next commit,
reviewed by nobody, and the green line reads as coverage of the whole change.

Two options. a) Add a sixth field, `Working tree:`, naming the uncommitted paths the review read, or
the word `clean`. The check then holds one more fact, and the record states its own coverage. b) Drop
the second half of criterion 2. The delta is then the committed range alone, and uncommitted work is
reviewed at the commit that carries it. I prefer (a). The wish behind criterion 2 is real, since work
standing in the tree at push time does reach the remote soon after.

`defect · unenforceable-promise (discharge)`

F6 — Nothing states what makes a finding blocking, and one free sentence reopens the push

> "*when* a blocking finding is closed, or the record states why it stands, the system *shall* let
> the push through." — PRODUCT_SPEC.md, Requirement 305, criterion 10

The reviewer writes the findings and marks which are blocking. No criterion states the test. The
record home states the two forms an item takes, `closed:` and `stands:`, and states no bar for the
second. So a reviewer who finds a defect can write one sentence under `stands:` and the push goes
through, with no queue row and no owner.

The person affected is the next session that inherits the defect. They read a green gate ac, a
committed record naming the defect, and no queue row holding it. The defect has a written home that
nobody sweeps. Requirement 305's own promise, that a missed defect is caught, then rests on a
sentence with no reader.

Two options. a) Require a `stands:` reason to cite a queue row number. A standing blocking finding
then becomes a parked item with an owner. b) State the test for "blocking" in the requirement. A
finding is blocking where it names a broken rule, a false claim, or a missing answer the
specification owes. Both are cheap, and I would land them together. Option (a) is the one a script
can hold.

`defect · missing-rule (invariant)`

F7 — The base ladder's third rung narrows the reviewed range to one commit in silence

> "the third rung is the previous commit, and the first rung that resolves gives the base." —
> PRODUCT_SPEC.md, Requirement 305, criterion 3

Where the caller declares no base and no `origin/main` resolves, the base is `HEAD~1`. A local branch
five commits ahead then presents a range of one. Gate ac requires the record to name that one commit,
finds it named, and passes. Four commits reach the remote reviewed by nobody, and the green line
reads as coverage.

The same ladder rides `guardrails/check-prover-record.sh`, where it decides the inbox carve-out. A
narrowed range there can read a multi-file push as the single-file deposit shape. So this is one hole
on two gates, and a repair in one place leaves the other open.

The person affected is anyone pushing from a clone whose remote carries another name, or from a tree
where `origin/main` has not been fetched. They see green from both gates on a range neither gate
actually read.

State the ladder once, in the requirement that owns it, and add one rung condition. *if* the third
rung supplies the base *and* the branch stands more than one commit ahead, *then* the gate *shall*
red and name the base. Both scripts then read one home. The ladder's own home today is
Requirement 242 criterion 2, and F10 below covers the pointer.

`defect · missing-scenario (state-space)`

F8 — One architecture pin names a line where its labelled text no longer stands

> "- `skills/spec-author/SKILL.md:203` (axes composition)" — ARCHITECTURE.md, line 105

Line 203 of that file holds the prose-quality gate's five parts. The composition-axis material stands
at line 271, under the heading "The move most specs miss: compose every stateful surface across every
axis". The pin is off by about seventy lines, and its label matches nothing within the drift check's
window.

`bash guardrails/check-pin-drift.sh` reports this pin, together with four pins ending in line one
that the landing's own message names as file-wide by design. So one real drift stands among four
declared ones. The check reports and exits zero, which is what "non-strict" means here. The landing
message for `6167a6e` says the pins all resolve, and this pin is the exception.

Repoint the pin to `skills/spec-author/SKILL.md:271`. Then decide the class question: a check that
reports drift and exits zero lets a wrong pin ride every push. Two options: a) red on any drift
outside a declared file-wide list; b) ratchet the drift count downward the way the finding counters
ratchet. I prefer (a), because the file-wide list is four entries long.

`defect · hard-to-operate (ops-ux)`

F9 — Three architecture pointers name a bare filename, and one names a file the pack does not ship

> "`judge-hooks.json` classifies it as a library entry [INV-211], and the pack's default
> `settings.json` leaves it unwired." — ARCHITECTURE.md, line 331

The landing at `6167a6e` wrote fourteen bare filenames out in full. Three stand unqualified after it.
`judge-hooks.json` appears bare at lines 323 and 331, while lines 392, 481 and 489 write
`guardrails/judge-hooks.json`. So one file carries two spellings in one document.

`settings.json` is worse. No file of that name exists anywhere in this repository. The file the
sentence means is the host's own `~/.claude/settings.json`, which
`scripts/install-pack-hooks.sh:32` names in full. A reader who opens the architecture to find the
pack's default settings file finds nothing, and the sentence gives no other place to look.

Write both out. Line 323 and line 331 take `guardrails/judge-hooks.json`. Line 331 also names the
host file and says the pack's installer leaves this hook unwired. Then run the landing's own sweep
again. A class swept once and left at three residues meets the next reader again.

`defect · hard-to-operate (ops-ux)`

F10 — The two redundancy repairs point in two different forms

> "**public edition** — a skill's copy for a reader outside this project, held at `editions/<skill>/`.
> Requirement 304 states what it carries." — PRODUCT_SPEC.md, glossary

> "The system *shall* resolve the push range by the ladder INV-208 states." — PRODUCT_SPEC.md,
> Requirement 305, criterion 3

Both edits replace a restated fact with a pointer. One points by requirement number and one by rule
code. A requirement number is a heading a reader finds by search. A rule code is an index entry: the
reader opens `PRODUCT_SPEC.index.md`, reads that `INV-208` maps to R242.1 through R242.4, then finds
Requirement 242. That is one hop longer for no gain.

The reader affected is anyone resolving either pointer for the first time. They learn two conventions
from two sentences landed minutes apart, and neither sentence says which is the house form.

Pick one form and use it in both places. I prefer the requirement number, because it names a heading
the reader can search for directly. Criterion 3 then reads: the ladder Requirement 242 states.

`recommendation · confusing-for-users (cognitive-load)`

## The two redundancy repairs, judged

The question is whether a criterion that points at another requirement still tells a reader what to
do. I read each repair for the fact it dropped and for where that fact now lives.

**The glossary entry for a public edition.** The sentence removed was "It states the same method,
with every internal code resolved into the rule it stands for." That exact sentence stands as the
first sub-bullet of Requirement 304 criterion 1. So the fact moved to one home from two, which is
what the repair was for.

What the entry still carries on its own: the term, what it is, who it is for, and where it lives on
disk. A reader meeting "public edition" for the first time learns that it is a skill's copy for a
reader outside this project, held at `editions/<skill>/`. That is a definition, and it acts. A reader
who needs the content rule follows one named heading.

**Verdict: it still instructs.** A glossary entry's job is to name the thing and place it. This one
does both, and it points at a heading a reader can search for.

**Criterion 3 of Requirement 305.** The sentence removed was "The system *shall* read the push range
through the base ladder the prover-record gate uses." The replacement points at `INV-208`. The three
rungs stayed in place beneath it, unchanged:

> "- the first rung is the base the caller declares;
> - the second rung is the remote's main branch;
> - the third rung is the previous commit, and the first rung that resolves gives the base." —
> PRODUCT_SPEC.md, Requirement 305, criterion 3

So the criterion still states its own rule in full. A reader holding that page alone can build the
ladder and pass the code over. The pointer replaced the sourcing phrase and nothing else.

**Verdict: it still instructs.** One reservation, and it predates the repair. Neither wording names
the concrete identifiers. Requirement 242 criterion 2 states the same ladder and names
`LIVE_SPEC_DIFF_BASE`, `origin/main` and `HEAD~1`. A reader of Requirement 305 alone cannot set the
declared base, because they never learn the variable's name. The repair neither caused that nor fixed
it. F10 covers the pointer's form.

**What the numbers say.** The redundancy check reads 121 open pairs on the committed copy and 119 on
the working tree. The floor is 119. So the two repairs closed exactly two pairs and reached the
floor. The criterion-readability check reports identical counts on both copies:
long-criterion 378, inline-gloss 65, absolute-tail 123, anchor-noise 61, criterion-load 31. So
neither repair traded a redundancy pair for a readability finding. The anchor-noise counter sits at
its recorded ceiling of 61, which means the next in-prose code reds.

## The previous record, re-read

`docs/prover/2026-08-05-public-edition-and-reader-repairs.md` filed eight rows. This pass read each
against the tree.

| Row | Claim | State now |
|---|---|---|
| F1 | The public edition has no requirement, no matrix row, and a stale glossary entry | folded — Requirement 304, rows M-491 to M-493, both glossary entries rewritten |
| F2 | `editions/` stands in no part of the architecture | folded — `ARCHITECTURE.md:37` carries the inventory line, and the publish node's pin label leads with the selection |
| F3 | An edition missing `SKILL.md` publishes a repository holding no skill | folded — Requirement 304 criteria 7 to 9, and `publish_source_for` refuses by name |
| F4 | Nothing binds an edition to its skill, and the sync reports a stale mirror as up to date | open — carried forward as F1 above, with no queue row holding it |
| F5 | The sync publishes from the working tree while its commit message names a commit | open — `scripts/sync-mirrors.sh:105` still reads `HEAD` for the stamp and `:418` still copies the working tree; no queue row |
| F6 | `DECISIONS.md` states three reading rounds and cites a file recording six | folded — `DECISIONS.md:254` now reads "the first three of six rounds" |
| F7 | A commit message states nine tests and the file holds six | closed by history — the message is a landed commit and cannot be edited |
| F8 | One English phrase is pinned in four documents with no criterion behind it | open — recommendation, awaiting a taste call |

Three rows stand open, and two of them carry no queue row. F4 and F5 both name a way a public mirror
can hold text that no source in this repository matches. That is one class with two members, and it
now has a third pass behind it with no owner.

## The suite, 3 failed and 2358 passed

I read `suite-run-7.log` in this session's scratch directory. Its last line reads
`3 failed, 2358 passed in 442.54s`. The three:

1. `tests/test_convergence_locks.py::TestConvergenceLocks::test_live_spec_sits_at_the_clean_floor` —
   the redundancy floor. The log's assertion reads "121 not less than or equal to 119 :
   PRODUCT_SPEC.md re-grew redundancy: 121 open pairs (floor 119)". The two working-tree repairs
   close it. Re-running the same check over the working tree returns 119 open pairs.
2. `tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes` — the missing record.
   The log's message reads "the newest committed prover record predates the last PRODUCT_SPEC.md
   change", naming `cefd11d` against record commit `b4e1425`. This document supplies the record, and
   the commit that lands it closes the failure.
3. `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes` — the third mirrors the
   first. This test copies the tree into a scratch directory and runs the whole suite there. Its
   nested run reports `1 failed, 2348 passed, 12 skipped`, and that one failure is
   `test_live_spec_sits_at_the_clean_floor` with the same 121-against-119 assertion. So it carries no
   defect of its own, and it goes green when the first does.

Confirmed against the log. No other failure stands in it.

## The mandatory sweeps

Three surfaces carry this delta. Each sweep takes one verdict per surface.

| Surface | Declared laws | Edge conditions | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The mirror sync (Requirement 304) | clean — the language scan runs on the assembled README after the copy, so an edition's text meets the same law | hit — F2, the run's end state after a refusal | clean — one selection reaches every skill under `skills/` | hit — F1, the re-publish after a skill changes | hit — F3, the case a criterion sits outside |
| The push review gate (Requirement 305) | clean — gate ac carries its known-red proof, and M-496 pins it | hit — F7, the ladder's third rung | hit — F7 again, the ladder rides two gates and each states it separately | hit — F4, the record's own commit | hit — F5 and F6, the uncommitted half and the word "blocking" |
| The architecture map | clean — the census reads the document at zero findings against its cap | clean — every node states its pins and its owned codes | N/A — one document, with no sibling surface to hold uniform | N/A — the document holds no runtime state | hit — F8 and F9, pointers that resolve to nothing |

Create-read-update-delete and authorization each read N/A across every row here. This pack holds no
user-mutated persistent entity and no role model. A table of N/A cells would train the reader to
skim, so this line stands in its place.

Invariants per state, for the sync's three states:

| State | Invariants stated | Invariants missing |
|---|---|---|
| No edition | the mirror takes the skill folder; the pack stays the source | none found |
| Edition published | the mirror takes the edition; `skills/` stays what a session loads; the run prints the skill and the directory | the edition matches the skill version (F1) |
| Refused | no source is published; the mirror is left as it stands; the skip is recorded; the run continues | the run's own result (F2); whether a hand edit survives (F3) |

## Phase 3.5 — acknowledged gaps

Requirement 304 and Requirement 305 carry no open item, no marker for pending work, and no unanswered
question in their bodies. The architecture rewrite carries none either. The one written
acknowledgement of a limit is Requirement 305 criterion 12, and it stands as a decided answer. The
requirement states which judgments no script makes, and gives the reason.

## Phase 4 — human and operational factors

**What an operator can see.** The sync prints one line per skill and a summary at the end. F2 names
what that summary cannot carry, which is the run's own result. Gate ac prints a fix line naming the
directory and the date form, which is the shape a person needs at a red.

**The words a reader meets.** Requirement 304 and Requirement 305 speak in the product's own words.
"Public edition", "standalone mirror", "push review record" and "push gate" each carry a glossary
entry. The vocabulary gate reads every glossary term as used in the body, and reads no banned
coinage.

**Reading load.** The architecture map fell from 88 sentences over the cap to zero, and its longest
sentence now runs to 25 words. The specification stands at 1830 sentences over the cap, against a
recorded ceiling in `guardrails/rule-census.json`. That is the specification's own ratchet, and this
delta moved it in neither direction.

**Scale.** `PRODUCT_SPEC.md` stands at 667 kilobytes and `ARCHITECTURE.md` at 95. The rotation law
covers a growable document past roughly half a megabyte. The specification is past that number today,
and the rotation law reaches append-only documents alone. Naming the ceiling here: a session that
loads the whole specification pays for 667 kilobytes on every read.

**Security and privacy.** Out of scope for this delta, and named rather than passed over. The two
requirements move text between directories on one machine and push to public repositories the owner
controls. The mirror language scan is the one privacy net in the path, and it runs.

## Phase 5 — closing

**Top three to fix before the next push.** F1, because a stale edition reaches the public and reports
itself up to date. F5, because gate ac's green line claims coverage the record cannot carry. F7,
because the same narrow range rides two gates.

**Properties to state, ready to paste.**

- An edition records the skill version it was resolved from, and a sync reds where that version
  stands behind the skill's own.
- A sync run that refused any skill exits non-zero after printing its summary.
- A push review record is committed on its own, after the commits it reviews.
- A blocking finding left standing cites the queue row that now holds it.
- Where the base resolves from the third rung and the branch stands more than one commit ahead, the
  gate reds and names the unresolved base.

**Open questions for the author.** One. Is `editions/` meant to grow past the one skill it holds
today? F1's fix is cheap for one edition and worth a script for ten. The answer decides whether the
net is a guardrail or a test row.

**Recommendations queued for a taste call.** F10, the pointer form. One question of taste sits under
it. May a criterion point at another requirement at all? The other road has every criterion restate
its own rule, with the redundancy floor absorbing the cost.

**Default-tagged sentences.** `PRODUCT_SPEC.md` carries three sentences marked as a value the person
may retune. All three sit in Requirement 186, the settings card: its viewport rule, its static-page
rule, and its read-only render rule. `ARCHITECTURE.md` carries two, both in the quality-budget table:
the full-suite wall-time budget and the settings-card render budget. That is the whole list, and this
delta added none and touched none.

Readiness: the specification holds, and the ten findings are all fixable in place.

## The gates, run before this record was handed over

**`sh guardrails/check-prover-record.sh`** — exit 1.

```
OK (prover record): committed record(s) for 2026-08-05 found:
  docs/prover/2026-08-05-night-campaign-push-recheck.md
  docs/prover/2026-08-05-public-edition-and-reader-repairs.md
FAIL (prover record): the newest committed prover record predates the last PRODUCT_SPEC.md change.
  PRODUCT_SPEC.md last changed in commit cefd11d58fa2f082384999a2b38515036d6df347; newest docs/prover/ commit is b4e14255370af9c55f88c0e1bb6c2f86ab0e8a8f.
```

The gate reads this file as uncommitted, because committing is the owner's step. It lists the two
records already committed today and reds on the freshness rule. The red closes when this record and
the two working-tree edits to `PRODUCT_SPEC.md` land, in one commit or with the edits first.

**`python3 scripts/preshow-register-lint.py docs/prover/2026-08-05-readability-day-spec-recheck.md`**
— exit 0.

## Verdict line

**The specification is sound enough for these commits to be pushed.** Ten findings stand, and every
one of them is a missing sentence or a wrong pointer inside behaviour that already works. None
contradicts a shipped guarantee, and none blocks the landing.
