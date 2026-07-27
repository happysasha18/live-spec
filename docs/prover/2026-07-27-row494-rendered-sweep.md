# Prover record — ROADMAP row 494, the rendered-page clearing (INV-286), 2026-07-27

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK with the architecture lens, delta
scoped. Written by a seat that authored none of the work (SPEC INV-237).

## Scope

**What this record reviews.** Everything uncommitted in the working tree at HEAD `556d0c9` that belongs to
ROADMAP row 494, read through `git diff` and `git status`: `PRODUCT_SPEC.md` (Requirement 296, INV-286,
and its glossary entries), `PRODUCT_SPEC.index.md`, `ARCHITECTURE.md` (the communicator node),
`TEST_MATRIX.md` (M-463), `skills/communicator/SKILL.md`,
`skills/communicator/references/page-lifecycle.md`, `skills/communicator/references/field-examples.md`,
`skills/publish/SKILL.md`, `scripts/sweep-rendered.py`, `guardrails/check-rendered-sweep.py`,
`guardrails.config.json`, `.gitignore`, `tests/test_rendered_sweep.py`, `attic/`, and the two
`docs/skill-review/2026-07-27-*.md` records.

**What this record skips, by the brief.** A concurrent lane owns `docs/spec-format.md`,
`guardrails/check-criterion-readability.py`, `guardrails/criterion-readability.json`,
`tests/fixtures/specformat/readability_clean.md`, `tests/fixtures/specformat/readability_dirty.md`, and
`tests/test_criterion_readability.py`. Those files were read for collisions with row 494 and hold none.
They touch no clause, no machine, and no test this row writes.

**The design was replaced while this pass ran, and the state below is what the verdict judges.** The pass
opened at 19:05 on a delta whose rule was the home a page is written into: three declared record homes in
`guardrails.config.json`, a `record home` glossary entry, and a sweep that read a page's directory. Between
19:20 and 19:28 that rule was replaced by a second one: the renderer stamps
`<meta name="generator" content="live-spec render-doc">` into every page it writes, the sweep reads the
mark, and a page with no mark is the artifact itself. Requirement 296 grew from nine criteria to twelve.
The `record home` glossary entry is gone. `guardrails.config.json` no longer carries `record_homes`.
`.gitignore` was rewritten twice. A sweep was run against the real tree at 19:27 and moved eleven further
pages into the attic.

**Every claim below is pinned to the tree as of 19:30.** Two findings that stood at 19:14 were folded
before this record was written and are recorded under "What folded while the pass ran", so the fold is
visible and the next reader does not re-open them. The concurrent-edit fence exists for this case: a review
record is worth what the state it read is worth, so the timestamp carries weight here.

## Verdict

**HOLD — the push does not go on the reviewed state.** Four defects must fold, four should fold, and nine
recommendations queue. Three of the four must-fix items are decisive on their own, and each is mechanical:
a blocking push gate is red, eight of the row's own thirty-one tests fail, and a sweep run against the
real tree moved five committed files into the attic, so the delta as it stands carries their deletion.

The law itself is sound and the second design is better than the first. Reading the renderer's own mark
puts the decision where the knowledge is, and the docstring states the rule's three blind spots at their
real width, which is the shape a reader can trust. The recovery road is real: nothing is deleted, the
attic holds every page, and the manifest is committed while the bytes rest on disk. What holds the push is
that the documents, the machines, and the tests now describe two different rules, and that a run of the
new machine against the live tree produced a deletion nobody reviewed.

| # | Kind / severity | Claim / evidence | Status |
|---|---|---|---|
| F1 | defect / must-fix | The sweep moved five git-tracked committed pages into the attic; the delta carries their deletion | OPEN — handed back |
| F2 | defect / must-fix | Gate e, the prototype fence, reds on the delta's own `.gitignore` line | OPEN — handed back |
| F3 | defect / must-fix | Eight of the row's thirty-one tests fail, gate x reds, and M-463 names thirteen tests that do not exist | FOLDED at 19:33 by the authoring session, verified |
| F4 | defect / must-fix | Criteria 2 and 3 of R296 disagree, and criterion 2 is what took the decision-page archive | OPEN — handed back |
| F5 | defect / should-fix | The communicator node pins a rule the config no longer carries; `check-pin-drift.sh` names it | OPEN — handed back |
| F6 | defect / should-fix | The manifest's reason is one constant string, so INV-7's "why it moved" is discharged with a sentence false for eleven of fifteen lines | OPEN — handed back |
| F7 | defect / should-fix | The attic stands outside the sweep and is named in no criterion and on no green line | OPEN — handed back |
| F8 | defect / should-fix | The clearing flow rides no runtime-view walk, and the communicator-to-attic seam has no row | OPEN — handed back |
| F9 | recommendation / should-fix | `.gitignore` states the two-kind split a second time and cannot read the renderer's mark | OPEN — handed back |
| F10 | recommendation / should-fix | The attic has no bound and no exit; every release sweep only adds to it | OPEN — handed back, needs the owner's word |
| F11 | recommendation / should-fix | E-9 prefixes the source directory on a collision; the sweep prefixes on every move | OPEN — handed back |
| F12 | recommendation / should-fix | A rendered page waiting for the person reds the check while it stands (INV-51, INV-52) | OPEN — handed back |
| F13 | recommendation / should-fix | The adoption cruft sweep may delete what R296.5 says is never deleted | OPEN — handed back |
| F14 | recommendation / should-fix | The config falls back to the pack defaults with no word said, where INV-224's road fails the other way | OPEN — handed back |
| F15 | recommendation / later | The attic manifest has three writers and no stated line shape | OPEN — handed back |
| F16 | recommendation / later | The attic's stated population is narrower than what it now holds | OPEN — handed back |
| F17 | recommendation / later | The release sweep is anchored on the shopfront walk, which reads claims | OPEN — handed back |

Nothing in this record was folded by the seat that wrote it. Every row is handed back to the authoring
session.

---

## F1 — The sweep took five committed files, and the delta carries their deletion

> "docs/decisions/2026-07-06-overnight-decisions.html -> attic/docs-decisions-2026-07-06-overnight-decisions.html * a rendered page whose reading is over * 2026-07-27" — `attic/MANIFEST.md`

`git status` at 19:30 shows five deletions of git-tracked files:
`docs/decisions/2026-07-06-overnight-decisions.html`, `docs/decisions/2026-07-07-morning-round3.html`,
`docs/reports/2026-07-06-morning.html`, `docs/research/2026-07-06-bmad-kiro-livespec-comparison.html`, and
`docs/research/2026-07-06-neighbours-implementation-harvest.html`. Each was committed on purpose in an
earlier movement. Each was taken by the 19:27 sweep run because a markdown document of the same name
stands beside it, which is criterion 2's legacy evidence.

The person who committed a decision-page archive under rule 10's own archive step gets it removed from the
repository by a push that claims to clear rendered pages. On a fresh clone the file is gone. A JOURNAL or
ROADMAP line pointing at a decision archive lands on nothing. The attic copy is on the author's disk alone,
because `*.html` keeps the attic's bytes out of git, so the recovery road the law promises does not reach
anyone who clones the repository.

Add one clause to R296 and one line to the sweep: a git-tracked file is never moved. A tracked file is by
construction an artifact somebody committed, so the test is exact, cheap, and structural, and it makes
criterion 3's promise enforceable. Then restore the five files from the attic before the push and re-run
the sweep to confirm it takes nothing.

`defect · partial-success-risk (atomicity)`

## F2 — The prototype fence reds on the delta's own `.gitignore` line

> "FAIL (prototype fence): .gitignore references prototype/work-board-sketch.html" — `bash guardrails/check-prototype-fence.sh`, run at 19:29

`.gitignore` line 19 reads `!prototype/work-board-sketch.html`. `check-prototype-fence.sh` greps every
git-tracked file outside its exclusion list for the literal path of every file under the fence home.
`.gitignore` is tracked and stands on no exclusion list, so the un-ignore line is read as a production
file naming a fenced path. The gate is gate e of the push chain and blocks under INV-47. It exits 1 today.

A session that pushes this delta is stopped at gate e with a message about wiring a sketch into a
production surface, and the actual cause is a line written to keep that sketch tracked. The gate is correct
about what it saw; the delta handed it a literal path it was built to find.

Two roads. Either add `.gitignore` to the fence's exclusion list beside `docs/` and `attic/`, with a
sentence saying an ignore rule is a tracking declaration and carries no wiring, or drop the un-ignore line
and let the sketch stay untracked. I prefer the first: the fence's exclusion list already exists for
exactly this class of narrative-or-declarative mention, and `prototype/work-board-sketch.html` was tracked
before this delta, so dropping the line loses a committed file.

`defect · internal-conflict (consistency)`

## F3 — The row's own tests, its matrix row, and gate x describe the rule that was replaced

> "8 failed, 23 passed" — `python3 -m pytest tests/test_rendered_sweep.py -q`, run at 19:29

The eight are `test_gate_passes_a_page_in_a_record_home`, `test_gate_passes_a_swept_tree`,
`test_a_record_home_declared_with_a_trailing_slash_still_holds`,
`test_a_malformed_config_falls_back_to_the_defaults`, `test_gate_states_its_reach_on_the_green_line`,
`test_sweep_leaves_a_record_page_standing`, `test_communicator_tells_the_two_kinds_apart_by_the_home`, and
`test_record_homes_are_declared_as_host_config`. Every one holds the record-home rule. The file also holds
nineteen tests of the mark rule that the matrix names nowhere.

M-463 names thirty-two test functions. Thirteen of them do not exist:
`test_a_home_that_merely_starts_with_a_record_name_is_transient`, `test_gate_passes_a_page_in_a_record_home`,
`test_gate_reds_a_transient_page_left_standing`, `test_record_homes_are_declared_as_host_config`, and nine
more. The row's fact cell still states the home rule with `docs/`, `prototype/`, and `tests/fixtures/`
named as record homes declared under `rendered_pages.record_homes`, which `guardrails.config.json` no
longer carries. Gate x reds beside it: `check-index-generated.py` reports the committed
`PRODUCT_SPEC.index.md` differs from a fresh build off the current body, because the requirement grew from
nine criteria to twelve after the index was last generated.

The traceability map is the pack's promise that a stated fact is held by a named test. Here it points a
reader at thirteen names that resolve to nothing, and it states a rule the spec has dropped. A reader
auditing INV-286 reads the matrix, opens the file, and finds a different law.

Rewrite the eight tests to the mark rule or delete them, rewrite M-463's fact cell and its evidence cell
off the twelve criteria and the nineteen tests that exist, and rebuild the index with
`python3 scripts/build-index.py`. Then run the three format gates and the row's test file together and read
the log.

`defect · internal-conflict (consistency)`

## F4 — Two criteria of one requirement disagree, and the losing one took the decision archive

> "2. *where* a page was rendered before the mark existed, the system *shall* read its source document standing beside it under the same name as the same evidence." — PRODUCT_SPEC.md, R296.2

> "3. The system *shall* read every other page in the tree as the artifact itself and *shall* leave it standing." — PRODUCT_SPEC.md, R296.3

The requirement's own Context names a hand-built decision page as the first example of the artifact kind
criterion 3 protects. A decision page is built from a markdown document and archived beside it under the
same name, which is exactly criterion 2's evidence. So criterion 2 classifies as a render what criterion 3
promises to leave standing, and criterion 2 runs first. F1 is that disagreement realized.

The legacy fallback is aimed at pages rendered before the mark existed. As written it also reaches every
hand-built page whose author kept a markdown source beside it, which is the pack's own habit for decision
pages, reports, and research notes. The evidence is a coincidence of naming, and the requirement treats it
as proof.

Scope criterion 2 so it cannot reach a committed artifact. Two options. (a) Bound it to untracked files,
which composes with F1's one line and needs no list. (b) Replace it with a one-time named set of the
pre-mark pages, swept once and then dropped from the requirement. I prefer (a): it is one predicate, it
never goes stale, and it states the real distinction — a page nobody committed is a page nobody chose to
keep.

`defect · direct-contradiction (contradiction)`

## F5 — The architecture pins a rule the config no longer carries

> "DRIFT (pin drift): guardrails.config.json:1 (INV-286 — the declared record homes under `rendered_pages`) — label not found within ±25 lines" — `bash guardrails/check-pin-drift.sh`, run at 19:29

The communicator node's pin list cites `guardrails.config.json:1` as the home of the declared record homes.
The file now carries `rendered_pages.outside_reach` alone. The pin drift check is non-strict, so it reports
and exits 0, and the stale pin survives the push.

A pin is the architecture's claim about shipped code. A reader following this one to learn where the record
homes live finds a block that holds a different fact, and the node's `owns` entry beside it still says the
record homes are declared as host config in the guardrails node's config file.

Rewrite the pin to name what the block holds — the declared reach, `rendered_pages.outside_reach` — and
rewrite the `owns` entry's tail off the mark rule. While that entry is open, the pin list also owes
`scripts/render-doc.py` a line, since the renderer's stamp is now the rule's first mechanism and the
architecture names it nowhere.

`defect · hard-to-operate (ops-ux)`

## F6 — The manifest states one reason for every page, and it is false for eleven of the fifteen

> "- `docs/research/2026-07-06-bmad-kiro-livespec-comparison.html` -> `attic/docs-research-2026-07-06-bmad-kiro-livespec-comparison.html` * a rendered page whose reading is over * 2026-07-27" — `attic/MANIFEST.md`

R179.1 requires a manifest line stating what the file was, why it moved, and the date. The sweep writes a
constant string for the reason. For the four root pages the string is true. For the eleven taken at 19:27
it says a reading is over for pages committed three weeks ago that nobody was reading, and it hides the
evidence the sweep actually used, which differs per page: some carried the mark and some were taken by
their neighbouring markdown.

A person opening the manifest to decide what to restore reads fifteen identical reasons and learns nothing
about why any page was chosen. That is the clause discharged in form with no information carried, and it
is the one record that survives once the bytes are gone.

Write the evidence into the line: the page carried the renderer's mark, or a source document stood beside
it under the same name. One field, read from the classifier that already made the call.

`defect · hard-to-monitor (observability)`

## F7 — The attic stands outside the sweep and no criterion says so

> "11. The system *shall* leave the version-control directory, the harness's worktree home, and the host state directory outside the sweep" — PRODUCT_SPEC.md, R296.11

`classify` prunes `outside_reach + (ATTIC,)`, so four directories stand outside the walk. The criterion
names three. The green line names three. R296.10 requires the check to state the homes standing outside its
reach, and the attic is missing from every statement of the reach.

The exclusion is right and its absence from the record costs two things. A person auditing why a page in
`attic/` never reds finds no sentence that says it. And a host that renames its attic, which the config
block does not allow, gets its own archive re-swept on the next run, each page taking a fresh prefix and a
fresh manifest line.

Name the attic in criterion 11 as the fourth home, with its reason — a page resting there has already been
cleared — and print it on the green line beside the other three. Read its name from the same config block
so a rename cannot break it.

`defect · missing-rule (invariant)`

## F8 — The clearing flow rides no runtime walk, and the seam it crosses has no row

> "How each promised flow runs through the nodes [INV-74]." — ARCHITECTURE.md, Runtime view

The delta changed two lines of `ARCHITECTURE.md`: the communicator node's `owns` list and its `pins` list.
R296 promises two flows — a page cleared as its exchange closes, and a release sweeping what accumulated —
and neither appears in the Runtime view. F-wish's row ends at "communicator (landing report, show)" with
no clearing tail. F-publish's row walks "publish (kind checklist) → guardrails (pre-push, reach map) → the
human's gate" with no sweep step.

The Seams table has no row for the crossing either. The attic and its manifest belong to the attach node,
which owns E-9, INV-7, A-4, and A-9. Communicator's sweep now writes into that node's surface, and the
architecture's own rule is that each seam states what crosses it and which side owns the format. Nothing
says who owns the manifest line's shape, which is F15 read from the architecture side.

Add one Runtime view row for the clearing flow and one sweep step to F-publish's walk. Add one Seams row:
between communicator and attach, what crosses is a page and one manifest line, and the format owner is
attach.

`defect · boundary-issue (composition)`

## F9 — `.gitignore` states the two-kind split a second time, and it cannot read the mark

> "# A page nothing regenerates is the artifact itself and is tracked: a frozen norm card, a hand-built decision page, a test fixture, a prototype sketch." — `.gitignore`

The requirement's rule is the renderer's mark. `.gitignore` decides the same split by four hardcoded path
patterns: `!docs/norms/*.html`, `!docs/decisions/*.html`, `!tests/fixtures/**/*.html`, and
`!prototype/work-board-sketch.html`. A pattern list cannot read a `<meta>` tag, so the two statements of one
fact will drift the first time an artifact page is written anywhere else.

The concrete case: a hand-built page under `docs/reports/`. Criterion 3 leaves it standing, so it lives in
the tree for good, and `*.html` keeps it out of every commit. Nobody sees it go missing, because the check
is green and the file is on the author's disk.

State in R296 that an artifact page is tracked, and give the tracking one keeper. The cheapest shape: a
test that walks the tree, finds every page with no renderer mark, and reds when one is ignored by git.
`git check-ignore` answers that in one call per file, and it closes the drift at the only place both facts
can be read together.

`recommendation · internal-conflict (consistency)`

## F10 — The attic grows and nothing empties it

The owner's word, quoted at the foot of `skills/communicator/references/page-lifecycle.md`, names two
stages: clear the pages, and clear the accumulated history of those files too when a version goes out. The
delta builds the first stage. The release sweep moves more pages in; nothing ever takes one out. The attic
held one page this morning and holds fifteen now, with a manifest line each, and the population rises with
every release.

Gate z, the growable-doc bound, watches four named documents and no directory, so the attic has no watcher
and no declared budget. The quality budgets table names five budgets and none of them is this one. The row
that was opened to end an accumulation has moved the accumulation one directory over.

Decide the attic's second stage. My recommendation for this push: have the release sweep's one line report
the attic's page count and total size, so the growth is visible before anybody sets a policy. The policy
itself — a page count, an age, or a deliberate no-bound — is a taste call and is the owner's.

`recommendation · stuck-state (liveness)`

## F11 — The collision law prefixes on a collision; the sweep prefixes on every move

> "3. *when* two files collide on a basename in the attic, the system *shall* prefix the name with its source directory, and *if* the name is still taken, *then* append a numeric ordinal." — PRODUCT_SPEC.md, R179.3

`attic_name` builds the prefix from the source directory on every move that has one, with no collision in
sight. Fifteen manifest lines show it: `docs/research/x.html` landed as `docs-research-x.html` on an
uncontested first move.

The eager form is the better rule. The conditional form loses the mark on the second clearing, because the
first page has already taken the bare name and the second gets an ordinal with no source in it. So the
code is right and the law is written narrower than the code. A reader who implements a second sweep off
R179.3 writes the conditional form and reintroduces the loss.

Rewrite R179.3 and base rule 18 to state the mark unconditionally: the attic name carries its source
directory, and a numeric ordinal follows while the name is still taken. Note also that the ordinal is
proven only where the mark is absent — `test_a_second_clearing_of_one_page_takes_the_ordinal` uses a root
page — so a case for one source directory swept twice is owed.

`recommendation · over-specific (abstraction)`

## F12 — A page waiting for the person reds the check while it stands

> "9. *while* a transient rendered page stands in the tree, the system *shall* red the sweep check, and the clearing *shall* clear that red." — PRODUCT_SPEC.md, R296.9

> "2. The system *shall* allow a mid-stretch re-open only as that same page refreshed in place." — PRODUCT_SPEC.md, R181.2 (INV-52)

Criterion 4 clears a page when its exchange closes. Criterion 9 reds while any marked page stands. During
an overnight away-stretch the one accumulating page is rendered, marked, and standing by design, and INV-52
requires that same file to survive so a re-open refreshes it in place. A landing inside that stretch runs
the suite, the check reds, and the printed fix is to run the sweep. The session follows it. The person
returns to a page that has moved to the attic under a new name, and the next refresh writes a second file
at the old path.

The check's blind spot is stated honestly in its own docstring — it reads a page's mark and never the
person's attention — and the away-stretch page is where that bound bites a stated law.

Name the case. The narrowest fix that fits the existing design: the away-stretch page is written once with
a marker the sweep honours, or `.live-spec/` becomes its home, which already stands outside the reach.
Whichever road is taken, R296 owes a sentence and INV-52's requirement owes a pointer to it.

`recommendation · internal-conflict (consistency)`

## F13 — The adoption cruft sweep may delete what the clearing says is never deleted

> "4. *when* adoption offers a cruft sweep, the system *shall* list the file counts and sizes of regenerable junk — caches, build leftovers, already-gitignored files — and *shall* delete only on the human's explicit approval." — PRODUCT_SPEC.md, R178.4 (A-9)

A transient page is gitignored by the delta's own `*.html` rule, so the adoption cruft sweep lists it as
regenerable junk and offers the human a deletion, while R296.5 says the same file moves to the attic and
nothing is deleted. Two paths over one file class, opposite outcomes, and the human is asked to approve the
one the newer law forbids.

The two laws the brief asked about are otherwise clean. A-9's other clause, R178.5, routes authored content
through the attic and keeps it out of the cruft sweep; a rendered page is generated, so INV-286 is stricter
than A-9 asks and contradicts nothing. Base rule 10 reads the same way: its permission to delete clearly
regenerable junk is a ceiling, and INV-286 declines to use it. That is a narrowing.

Add one clause to R178 naming the rendered page as a class the cruft sweep never lists, citing INV-286.

`recommendation · direct-contradiction (contradiction)`

## F14 — The config falls back silently, where the road it rides fails the other way

> "5. *if* the config names no classes, *then* the system *shall* leave every changed file unclassified and run the full suite on every push." — PRODUCT_SPEC.md, R226.5 (INV-224)

INV-224's road fails toward doing more work: an unreadable reach map runs everything. The rendered-page
block fails toward the pack's own defaults — `_config` catches `OSError` and `ValueError` and returns an
empty block — and `test_a_malformed_config_falls_back_to_the_pack_defaults` pins the silence as intended.
A host with a typo in `guardrails.config.json` has its own declared reach dropped and its pages swept under
the pack's three, with no word said.

The pages are recoverable, so the cost is a confusing morning. The two blocks living in one file with
opposite failure behaviour is the part worth closing while both are young.

Print one line from the sweep and from the check when the block cannot be read, naming the fallback, and
assert that line in the test that pins the behaviour. R296.12 owes the same sentence.

`recommendation · unclear-recovery (rollback)`

## F15 — The attic manifest has three writers and no stated line shape

> "2. The attic *shall* be append-only, one manifest line per file." — PRODUCT_SPEC.md, R179.2 (A-4)

Three laws now write to `attic/MANIFEST.md`: the adopt-and-rework move (R179.1), the waiting board's
superseded item (R205.2, INV-206), and this row's clearing (R296.5). R179.1 states the fields — what it
was, why it moved, the date — and no law states the line's shape, so each writer picks its own. The sweep
uses `*` as a field separator. Nothing says the other two do.

A person greps the manifest to find where a file went and gets a list in mixed shapes. No check reads it,
so a writer that drops the date is caught by nobody.

State the line's shape once in R179 — source path, attic path, reason, date — and have the other two laws
cite it. One test that parses every line in `attic/MANIFEST.md` under that shape closes all three writers
at once.

`recommendation · boundary-issue (composition)`

## F16 — The attic's stated population is narrower than what it holds

> "**attic** — the host's append-only archive folder (`attic/`). A superseded file moves here with one manifest line and is kept for good." — PRODUCT_SPEC.md, glossary

> "As a person whose project is being adopted or reworked, I want every superseded file kept in the attic rather than deleted, so that nothing I authored is ever lost." — PRODUCT_SPEC.md, R179 User Story

A cleared rendered page is neither superseded nor authored. Both sentences describe an attic that holds one
population, and the attic now holds two. This is the quantifier re-verify the CROSS-LINK mode owes at every
add: the newcomer widens a set two older sentences enumerate, and neither was re-read.

The rest of the quantifier sweep is clean. The spec's four "rides the suite" sentences each name their own
check and none of them claims to enumerate the family. The attic's other clauses — append-only, one line
per file, readable without a restore — hold for the new population as written.

Widen the glossary entry to a file that leaves active use, and add the second population to R179's Context
in one clause.

`recommendation · over-specific (abstraction)`

## F17 — The release sweep is anchored on the shopfront walk, which reads claims

> "8. *when* a release leaves the machine, the system *shall* sweep every transient page still standing and *shall* report the outcome in one line. [INV-286, INV-44]" — PRODUCT_SPEC.md, R296.8

INV-44's own criteria re-check the README's claims against the truth just pushed. The publish skill puts
the sweep paragraph inside that block, where every neighbouring step re-reads a claim. R146.4 lets the
shopfront walk stand down in one line when a push touches none of its claims, and a session taking that
stand-down skips the sweep with it.

Move the paragraph out of the shopfront block into the publish walk's own steps, or state in R296.8 that
the sweep runs whether or not the shopfront walk has a claim to re-check. The anchor on INV-44 can stay
either way; the placement is what carries the risk.

`recommendation · missing-prerequisite (precondition)`

---

## The architecture lens — six checks over the ARCHITECTURE.md delta

**Every spec fact has an owning node.** INV-286 sits on the communicator node and on no other. Clean.

**No node stands without spec backing.** The delta adds no node. Clean.

**Every seam names what crosses it and who owns the format.** F8. The communicator-to-attic crossing has no
Seams row, so the manifest line's format owner is unnamed.

**Quality budgets with instrumentation homes and watchers.** The delta declares no budget. F10 is the
budget the attic's growth now needs and does not have.

**The runtime view walks every promised flow.** F8. R296 promises two flows and the Runtime view carries
neither.

**The placement view says where every node runs.** Unchanged by the delta, and correct as it stands.

**The node-growth re-ask.** `node_growth_counter.py` reads 121 files and reports every file within its
ratchet, including `guardrails.config.json`, which two nodes now pin. Clean.

### Where INV-286 belongs — communicator or guardrails

**It belongs on communicator, and the delta places it there correctly.** The brief's two comparisons settle
it. INV-206 sits on guardrails because its surface, `WAITING.md`, is a guardrails-owned file with a
blocking gate reading it. INV-223 sits on communicator because its subject is the human-facing report and
its check rides the suite with no gate letter. INV-286's subject is the page the showing walk produces, its
home is communicator's rule 5, and `check-rendered-sweep.py` rides the suite and takes no gate letter. It
matches INV-223 on every reading, and the `owns` entry says so.

Two of its pins name guardrails-shaped files, which is the same shape INV-223 already has — communicator
pins `guardrails/check-far-tier.py --window` today. That is consistent and needs no change. The pin that is
wrong is the config one, and that is F5.

## Re-check at 19:34, while this record was being written

The tree moved again between 19:29 and 19:33. F3 folded whole and I verified each arm: the row's test file
reads 37 passed, `check-index-generated.py` exits 0 on a rebuilt index, and M-463 now names 37 tests that
all exist with none missing and none unnamed, its fact cell rewritten off the mark rule. The finding stands
in this record because the state it judged was real, and this line says it no longer holds.

Six findings were re-checked at 19:34 and all six still hold: five deletions in `git status` (F1), gate e
exiting 1 (F2), criteria 2 and 3 of R296 unchanged (F4), one drift line from `check-pin-drift.sh` and the
node's `owns` tail still naming record homes (F5), fifteen identical manifest reasons (F6), and criterion
11 still naming three homes (F7).

## What folded while the pass ran

Two findings stood at 19:14 and were folded by the authoring session before this record was written. They
are recorded so the fold is visible and nobody re-opens them.

**The attic name dropped its source-directory mark.** `sweep(...)` called `attic_name` with
`os.path.basename(rel)`, so the source directory was stripped before the namer could use it, and E-9's
first move never ran. Folded at 19:20: `attic_name` now takes the repo-relative path and builds the prefix
itself, with `test_a_nested_source_dir_flattens_into_the_mark` holding it. F11 is what remains — the law's
own wording.

**The lifecycle reference stated a one-move collision law.**
`skills/communicator/references/page-lifecycle.md` said a taken name gains a numeric ordinal and said
nothing about the source-directory prefix, where base rule 18 states two moves. Folded in the same window;
the page now states both moves in order.

## Open decision markers

No `⟨DECIDE⟩` marker stands on any surface this delta touches. The three occurrences in
`skills/communicator/SKILL.md` and `TEST_MATRIX.md` are the marker's own definition and its gate's
description, and neither is an open question.

## What is sound, verified against primary sources

Each item was checked against the file, the run, or the machine.

**The renderer stamps its mark and the sweep reads it from one home.** `scripts/render-doc.py:171` writes
`<meta name='generator' content='live-spec render-doc'>`, and `scripts/sweep-rendered.py` imports
`GENERATOR` from the renderer with a literal fallback, so the two files cannot disagree on the wording.

**The check imports its rule from the sweep.** `check-rendered-sweep.py` loads `sweep-rendered.py` by path
and calls its `classify` and `_config`, so the gate and the clearing read one classifier. Nothing is
restated.

**The blind spots are stated at their real width.** The sweep's docstring names three: it never reads the
person's attention, a directory reached through a symbolic link stands outside the walk, and a hand-built
page re-saved through the renderer reads as a render. A reader knows what the machine does not see.

**The recovery road exists and works.** Fifteen pages rest in `attic/` with fifteen manifest lines, and
`attic/MANIFEST.md` is tracked while the bytes are ignored, so the record of what was cleared survives a
clone. F1 is the case where that road does not reach far enough, and the road itself is real.

**The format gates are green on the spec.** `check-requirement-shape.py` reads 1464 criteria well-shaped
across 296 requirements, `check-no-history.py` finds no date marker in the body, `check-size-ratchet.py`
sits at 207.0 bytes per criterion against a recorded bound of 207.2, and `scripts/spec-style-lint.py`
reports zero errors. Gate x is the exception and is F3.

**The skill-side review records exist.** `docs/skill-review/2026-07-27-communicator.md` and
`docs/skill-review/2026-07-27-publish.md` both carry the `SKILL-REVIEW` marker, a verdict, and a findings
section. The skill-review gate stands down on the uncommitted diff, so the records are the evidence, and
they read as real reviews with one folded change each.

**The concurrent lane holds no collision.** The six files the brief named as a separate lane touch the
criterion-readability check and its fixtures. They write no clause, no machine, and no test row that row
494 also writes.

## What to do next

1. Restore the five committed pages from the attic and add the tracked-file predicate, so the delta stops
   carrying a deletion (F1, F4).
2. Clear gate e by excluding `.gitignore` from the fence scan (F2).
3. Rewrite the eight record-home tests, M-463's two cells, and the generated index; then run the row's test
   file and the three format gates and read the log (F3).
4. Fix the config pin and add the renderer to the node's pins (F5).
5. F6 through F8 are three small edits — an evidence field in the manifest line, the attic named in the
   reach, and three architecture rows. They belong in this push, since each states a fact the push is
   already making.
6. F9 through F17 queue for a taste call. F10 needs the owner's word on whether the attic gets a bound.

Overall readiness: needs another iteration.

---

## The fold, 2026-07-27 evening

The authoring session folded this record's must-fix set and re-ran the suite. Recorded here so the
next prover run opens on a settled file.

| Finding | State | What landed |
|---|---|---|
| F1 tracked pages moved | folded | The reach now stops before committed history: `tracked_pages()` reads `git ls-files` and a tracked page is never classified or moved. The five pages the earlier run took were restored from the attic and their manifest lines dropped. `R296.11` states the law; `test_a_committed_page_stands_outside_the_reach` and `test_an_uncommitted_page_beside_a_committed_one_is_still_cleared` hold it, both reproduced by mutation. |
| F2 prototype fence red | folded | The `.gitignore` line naming a fenced path came out. The pages it would have admitted are already tracked, so nothing changed for them. Gate e reads green over 158 fenced files. |
| F3 tests and index | folded | Confirmed by this record. |
| F4 criteria 2 and 3 contradict | folded | The contradiction dissolves under F1: the hand-built decision pages criterion 3 protects are tracked, so criterion 2 never reaches them. Criterion 2 also narrowed on its own terms — the source-beside reading is a heuristic and runs only where the tracked-page guard can stand behind it, held by `test_the_legacy_reading_stands_down_where_no_git_covers_the_tree`. |
| F5 pin drift | folded | The communicator node's config pin repoints at `rendered_pages.outside_reach`, and `scripts/render-doc.py` joined the pins as the rule's first mechanism. `check-pin-drift.sh` reads 134 pins green. |
| F6 one constant manifest reason | folded | `evidence()` returns the words the rule actually read, and each manifest line carries them. Held by `test_the_manifest_records_each_pages_own_evidence`. |
| F7 a fourth excluded home | folded | `attic/` is named in the default reach, in `R296.12`, and on the green line, and it is read from the config so a rename cannot break it. |
| F8 runtime and seam rows | folded | Two runtime rows, `F-page-clearing` and `F-release-sweep`, and one seam row for the communicator-to-attach crossing naming the manifest line and its format owner. |
| F9–F17 | handed back | Recommendations. The attic's own bound (F10) is the owner's call and is reported as such; the rest ride the queue. |

Suite after the fold: 2012 passed, 0 failed.
