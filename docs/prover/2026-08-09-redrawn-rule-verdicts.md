# Prover record — the redrawn rule verdicts, 2026-08-09

Adversarial review of `.live-spec/rule-verdicts-redrawn-2026-08-09.md`, committed as `17429cc`.
Reviewer: a fresh seat with clean context, distinct from the seat that wrote the list (base rule 33).
Root: Alexander's order of 2026-08-08 22:17, the plan `.live-spec/culling-plan-2026-08-08.md`, and
the closing note of `.live-spec/day2-verdicts-2026-08-09.md`.

Nothing in the list has executed. No repository file was changed by this review except this record.
No commit, no push, no restoring command was run.

Verdict: this list is not fit to execute today. Five blocking findings and seven major findings
stand. The blocking ones sit in the reach column, which is the column the list exists to add.

## Method

Read the list first, then the plan's criterion, then all thirty-five rules in
`skills/live-spec-base/SKILL.md` end to end. Read each named rule's own trace section in
`.live-spec/day1-census-rules.md`. Read the day 2 verdict list, its closing note, its measured price,
and the day 3 opening.

Recomputed every byte figure from the file itself with a script over the rule boundaries. Searched
for a set of eleven rules matching the list's stated sum. Read the tests and scripts that pin rule
text, and read `install.sh` to see whether a reference page reaches a stranger's machine.

Read two earlier records for form: `docs/prover/2026-08-09-culling-day2-cuts.md` and
`docs/prover/2026-08-07-night-order-adversarial.md`.

## What was read and run

- `.live-spec/rule-verdicts-redrawn-2026-08-09.md` whole, and its commit `17429cc`.
- `.live-spec/culling-plan-2026-08-08.md` whole, `.live-spec/day1-measures-2026-08-09.md` whole.
- `.live-spec/day2-verdicts-2026-08-09.md`, `.live-spec/day2-price-2026-08-09.md`,
  `.live-spec/day3-opening-2026-08-09.md`, all whole.
- `skills/live-spec-base/SKILL.md`, all thirty-five rules and every section heading.
- `.live-spec/day1-census-rules.md`: the compact table, the totals, and the trace sections for
  rules 7, 8, 18, 19, 20, 28, 31, 35.
- `tests/test_worker_restore.py` lines 1 to 80, and the list of twenty-eight test files that read
  the rulebook.
- `install.sh` whole, and `skills/build-pipeline/SKILL.md` for its reference-page pointers.
- Byte counts taken with `wc -c` and with a script that sums each rule's own lines.
- `git log`, `git show --stat 17429cc`, and `git show fb1e9d7:skills/live-spec-base/SKILL.md | wc -c`.

## Findings

Eighteen findings follow. Five block execution, seven are major, six are minor.

### 1. Blocking — moving text to a reference page moves the measure by definition

The list names one measure at line 65: the rulebook a session reads before work, 73 503 bytes.
That number comes from one command, recorded at `.live-spec/day1-measures-2026-08-09.md:12`. The
command counts two files: `skills/live-spec-base/SKILL.md` and the personal profile.

A reference page under `skills/live-spec-base/references/` is neither of those files. Every byte
moved there leaves the count on the day it moves. A session that follows the pointer still reads
the bytes. So the measure falls whether or not the load falls.

The plan's day shape makes this consequential. It states at `.live-spec/culling-plan-2026-08-08.md:30`
that two days without moving a declared measure stop the work. A lever that moves the declared
number by relocation cannot report whether the work succeeded.

Repair: give each shortening row a target size for the law and one for its page. Then extend the
day 1 command to count the base skill's reference pages beside its body. That extension changes a
measurement command, so the freeze on new checks does not reach it.

### 2. Blocking — rule 20's reach line is contradicted by the rule's own first sentence

Line 50 of the list marks rule 20 for removal, with the reach line "no reader outside this project".

Rule 20 opens at `skills/live-spec-base/SKILL.md:345` with "At a project's setup, meaning founding or
adoption's orient beside the founding questions". Adoption is the stranger's own path onto the pack.
The rule then tells that session to scan the installed skills and hand the human a fit list.

The census records the rule at `.live-spec/day1-census-rules.md:1638-1666`. Its living-doc trace
includes `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md:24`, a page about
onboarding a project.

The reach line also repeats the withdrawn day 2 row. That row reads "Sound advice with no reader
outside the project" at `.live-spec/day2-verdicts-2026-08-09.md:21`. The list promised at line 34 to
read each rule's traces before ruling. On this row the ground did not change.

Repair: restate the reach as the adopting project's setup, and move the row to keep or to shorten.

### 3. Blocking — rule 28's reach line is contradicted by its own host clause

Line 49 marks rule 28 for removal, with the reach line "the project's own machinery".

Rule 28 reads at `skills/live-spec-base/SKILL.md:459-460` that the audit runs every ten landings.
The same sentence adds "a host may set its own count on its word, SPEC INV-70". A host is an
adopting project. A rule carrying a host-settable default is a rule that runs in a stranger's tree.

The rule also runs the whole-read in the milestone gate's form, cited as SPEC M-1 at line 461. That
gate is part of what the pack ships.

Repair: restate the reach as the host's own living documents, and re-rule the row against the
criterion with that reading.

### 4. Blocking — rule 19's reach line is contradicted by two clauses in its own text

Line 48 marks rule 19 "cut to its law, or remove", with the reach line "the project's own process".

Rule 19 reads at `skills/live-spec-base/SKILL.md:328` "Grep the host's `.live-spec/PROBLEMS.md` for
the signature". It reads at line 334 that a third unowned recurrence goes to the pack's own queue,
"from a host window: one inbox file". Both sentences describe a stranger's own window.

The rule also carries a clause at lines 330-331 that only the human may write an agreed
non-problem. That is a protection for the reader of the reports.

Repair: restate the reach as a host session meeting operational noise, and drop the removal half of
the row.

### 5. Blocking — two rows carry two verdicts, so the list cannot be executed as it promises

Lines 47 and 48 both read "cut to its law, or remove". Line 67 promises that every row lands as its
own commit.

A worker cannot land a row that names two outcomes. The plan requires a single mark per row at
`.live-spec/culling-plan-2026-08-08.md:25`: keep, merge, or remove. It also requires at line 26 that
a later session read progress by comparing the list against the git log. A two-outcome row makes
that comparison unreadable.

Repair: split each of the two rows into one decided verdict, or move both to the rows that wait on
his word.

### 6. Major — the count of twenty-six contradicts the list's own table

Lines 22 to 23 state that twenty-six of the thirty-five rules reach a stranger or his reports.

The table's own reach column credits ten of its fifteen rows with such a reach. Those are rules 7,
31, 32, 29, 24, 13, 25, 14, 6 and 8. Line 54 then states that the twenty remaining rules each
protect a stranger or his reports. Ten plus twenty is thirty. Drop rule 29 and it is twenty-nine.

Repair: name the twenty-six rules in a list, or correct the count to what the table supports.

### 7. Major — the claim that no remaining rule is a twin is contradicted by the rulebook

Line 55 states that none of the twenty untouched rules is a twin of another.

Rule 29 calls itself the twin of rule 15 at `skills/live-spec-base/SKILL.md:480-481`. The next
sentence adds that one routing principle covers both. Lines 478-479 call rule 29 rule 27's posture
applied to a backlog item. Rule 1 reads at line 116 that a fork reaches the human only where rule 27
says so.

So rules 1, 15, 27 and 29 state one law about what reaches the human. They hold 5 148 bytes today.
The criterion says twins merge. The list shortens rule 29 alone and leaves the family unnamed.

Repair: put the four rules on the list as a merge candidate, with one rule as the home.

### 8. Major — rule 18's merge ground is false as written

Line 51 gives rule 18's reach as "files, and rule 10 already guards them".

Rule 10 reads whole at `skills/live-spec-base/SKILL.md:226-228`. It forbids silent deletion and
sends a superseded file to the attic. It says nothing about a taken name, a semantic mark, or an
ordinal. Rule 18's law at lines 314-322 also covers the inbox race, where a session token joins the
mark so a collision costs a rename.

Rule 18 also has machinery behind it. Its census trace at
`.live-spec/day1-census-rules.md:1520-1528` names `scripts/sweep-rendered.py` and three files of the
communicator skill, which a stranger installs.

Repair: state which of rule 18's three clauses survive the merge, and where the inbox clause lands.

### 9. Major — the reference-page move is contested by the pack's own machinery for rule 7

Line 38 sends rule 7's cases to a reference page. The largest of those cases is the ban on a worker
restoring a tree with a git command, at `skills/live-spec-base/SKILL.md:197`. It is 1 567 bytes, or
29 per cent of the rule.

`tests/test_worker_restore.py:36-42` lists five homes that must each carry that clause, the rulebook
among them. Lines 43 to 47 give the reason: a home that drifts to its own wording reds the test. The
file's own opening records three destructions of uncommitted work behind the clause.

The list's reach line for rule 7 is a stranger's uncommitted work. The clause is a prohibition that
must be known before the act, so a session that never opens the page has lost it.

Repair: keep the prohibition sentences in the rule body, and send only the lane mechanics to the
page. Then say in the row which sentences move.

### 10. Major — the shortening rows carry no price and no target, and day 2 measured neither

Line 68 states that the batch shape "is the shape day 2 measured". Day 2 measured two gate removals,
at `.live-spec/day2-price-2026-08-09.md:10-11`. Its own text says at line 63 that both samples were
gates, and that a rule's tail may run wider.

One shortening sample does exist and points the other way. The day 2 edit to rule 35 took the
measure from 73 645 to 73 503 bytes, which is 142 bytes.
`.live-spec/day2-price-2026-08-09.md:45-48` records what that cost. It lists a worker pass and a seat
repair of five red tests. It lists two review passes and three drafts of the rule. It lists a sync
of the installed copies and a journal entry.

Every rule on the shortening rows is pinned by at least one test that reads the rulebook and asserts
its phrases. Rule 7 alone carries seventeen test files and fourteen living-doc references in the
census table at `.live-spec/day1-census-rules.md:19`.

Repair: price one shortening row before the batch, as the plan priced one removal on day 2, and give
each row a target size.

### 11. Major — the argument counts the rule text and the measure counts two whole files

Line 19 calls 48 387 bytes "the rulebook". Line 65 calls 73 503 bytes the measure to watch.

The gap is 25 256 bytes at the time of the census, and 24 778 today. It holds the rulebook's header,
its path section, its vocabulary section, its thinking section, its settings ladder, and the personal
profile. The settings ladder alone is 9 915 bytes today, larger than any single rule. The profile is
7 068 bytes and belongs to Alexander.

So a third of the measure is untouched by every verdict, and the list never says so.

Repair: state the measure's parts with their sizes, and say plainly which parts no rule verdict can
move.

### 12. Major — the list omits the batch day 2 already gave to day 4

`.live-spec/day2-price-2026-08-09.md:67-68` gives day 4's first batch to one job. That job takes the
nested suite run out of the push chain, which is 451 of the 486 seconds the checks cost together.
The plan gives the same instruction at `.live-spec/culling-plan-2026-08-08.md:15`.

The list carries fifteen rows and no such row. It also assigns no row to a day and declares no
measure per day, which the plan requires at lines 26 and 30.

Repair: split the rows into daily batches, name the measure each batch moves, and keep the nested
suite row where day 2 put it.

### 13. Minor — the byte column was taken on a superseded version of the file

Line 6 says the list was written on commit `ab8031c`. The byte figures are the census's, taken on
`fb1e9d7`. That version of `skills/live-spec-base/SKILL.md` was 66 577 bytes; the file is 66 435
bytes today.

The one rule that changed is rule 35, edited when the handover gate went. Line 47 gives it 1 815
bytes. It is 1 675 bytes today. The stated total of 48 387 bytes is 48 247 today.

Repair: re-measure the fifteen rows on the commit the list is written against.

### 14. Minor — the figure of 28 730 bytes matches no set of eleven rules

Line 19 states that the eleven largest rules hold 28 730 bytes, and line 20 calls that 59 per cent.

The eleven largest hold 29 310 bytes by the census figures, and 29 170 bytes in the file today.
Those are 60.6 and 60.5 per cent. A search over every eleven-rule combination of the census figures
returns no subset summing to 28 730.

The error understates the list's own case, so the conclusion survives.

Repair: replace the two numbers with 29 170 bytes and 60 per cent, measured today.

### 15. Minor — rule 7 carries eight cases, and twelve is the count of its citation codes

Line 27 states that rule 7 gives one law and then twelve worked cases. The rule carries eight
bullets, at `skills/live-spec-base/SKILL.md:175-210`.

Twelve is the number of SPEC codes in the census heading for rule 7, at
`.live-spec/day1-census-rules.md:19`. The row appears to be drawn from that heading rather than from
the rule.

Repair: count the bullets, and say which of the eight move.

### 16. Minor — the verdict column uses a word the plan's decision set does not carry

The plan gives three marks at `.live-spec/culling-plan-2026-08-08.md:25`: keep, merge with another,
or remove. Nine rows of the table carry "shorten" instead, which is none of the three.

Shortening surviving rules is legitimate work; the plan assigns it at line 38. It is work done to a
rule that was kept. Written as a verdict, it hides that nine rules were judged to live.

Repair: mark those rows keep, and carry the rewrite as the row's own task.

### 17. Minor — the opening names one number and the closing names another

Line 13 says the plan's third stage exists to bring down the 45 000 tokens a session reads before
work. Line 65 names the measure as 73 503 bytes, which is about 18 400 tokens.

`.live-spec/day1-measures-2026-08-09.md:19-23` explains the gap. The larger figure covers a session
that also loads a working skill. A pipeline session loads `skills/build-pipeline/SKILL.md`, which is
64 194 bytes on its own. No row touches it.

Repair: say which of the two numbers the list moves, and by how much.

### 18. Minor — two parked rules are counted among the rules said to protect

Line 54 says the twenty remaining rules each protect a stranger or his reports. Rules 30 and 23 are
among those twenty. Lines 59 to 61 of the same page say both feed the regrowth the culling exists to
undo. The same lines say both wait on his word.

Repair: hold the two parked rules out of that sentence, and say they are unjudged.

## The two questions the order asked, answered directly

**Does shortening move the measure while deleting does not?** Directionally yes, and the list
overstates its own certainty.

The three removal rows hold 1 121, 838 and 766 bytes, which is 2 725 bytes, or 3.7 per cent of
73 503. The eleven shortening rows hold 29 170 bytes today. Cut in half they save 14 585 bytes, or
19.8 per cent. Cut to a 300-byte law each they save 25 870 bytes, or 35.2 per cent. The rulebook a
session reads before work would then stand near 58 900 or near 47 600 bytes.

Two conditions hold that range up. No row states a target, so no figure above can be checked against
the list. And by finding 1, the fall lands in the count whether or not it lands in the session.
Day 2's one real sample moved the measure by 142 bytes, which is 0.19 per cent.

**Does moving the cases to a reference page keep the rule's reach?** For some rules yes, for two no.

Delivery is not the risk. `install.sh` copies each skill folder with `cp -r`, so a reference page
lands on a stranger's machine with the skill. The pack already uses the shape: rule 26 keeps its law
and sends its per-kind table to `ARCHITECTURE.md`, at `skills/live-spec-base/SKILL.md:443-444`.

The dividing line is what the moved text does. A table consulted at a named step survives the move,
because the step names the page. That covers rules 32, 24, 13, 29, 6 and 25. A prohibition that must
be known before an act does not survive, because nothing prompts the session to look.

Two rules hold such prohibitions. Rule 7 holds the ban on a worker restoring a tree, which exists
because uncommitted work was destroyed three times. Rule 31 holds the rule that credentials never
cross and that a field with no recorded permission stays home, at
`skills/live-spec-base/SKILL.md:539-543`. Five of rule 31's seven bullets have no gate behind them.

## What was checked and found sound

Named so a later reader knows this sweep's reach.

- Rule 8's keep is right, and its reversal of the day 2 row holds. Its census trace at
  `.live-spec/day1-census-rules.md:774-800` names `scripts/sync-skills.sh` and
  `guardrails/check-skill-loadability.sh`, and an installed copy serves other projects.
- The individual byte figures for the other fourteen rows match the file, rule 35 excepted.
- The sum of rules 7 and 31 is 11 544 bytes, which is 23.9 per cent of the rule text. The phrase
  "near a quarter" holds.
- The row count is right. Fifteen rows named, twenty rules untouched, thirty-five in the file.
- The batch review economy is real. Both review gates read the push range, as
  `.live-spec/day2-price-2026-08-09.md:33-38` and lines 52 to 56 record.
- Rules 30 and 23 are correctly left for his word, and the list says so plainly.
- The reach lines for rules 7, 31, 32, 24, 25, 14 and 6 hold against those rules' own text.
- The list is honest about its own root and its own commit, and it names the day 2 lesson it applies.

## Verdict

Not fit to execute today.

Five findings block execution.

- Finding 1: the chosen measure falls when text moves, so the lever cannot be judged.
- Finding 2: rule 20's removal rests on a reach its own opening sentence contradicts.
- Finding 3: rule 28's removal rests on a reach its own host clause contradicts.
- Finding 4: rule 19's removal half rests on a reach its own host clauses contradict.
- Finding 5: two rows name two outcomes each, so they cannot land as commits.

Seven findings are major: findings 6 to 12. Six are minor: findings 13 to 18.

Findings 2, 3 and 4 are one failure repeated. The list added a reach column and filled four of its
cells from the rule's summary rather than the rule's text. That is the failure the day 2 closing note
undertook to end.

## Reach

Files read whole: the redrawn list, the plan, the day 1 measures, and the day 2 verdicts. Also the
day 2 price, the day 3 opening, `install.sh`, and all thirty-five rules in the rulebook.

Files read in part: `.live-spec/day1-census-rules.md`, at its table, its totals, and eight trace
sections. `tests/test_worker_restore.py`, lines 1 to 80. `skills/build-pipeline/SKILL.md`, its
reference pointers. `PRODUCT_SPEC.md`, at its shared-rules requirement.

Commands run: byte counts over the rulebook and the skill bodies, and a script summing each rule's
own lines. A search over every eleven-rule combination of the census figures. Then `git log`,
`git show --stat 17429cc`, and `git show fb1e9d7:skills/live-spec-base/SKILL.md | wc -c`. No test
suite was run, since no code changed and nothing in the list has executed.

Not read: `~/.claude` and its installed copies, which the order placed out of bounds. The profile's
size is taken as 7 068 bytes by subtraction from the day 1 measure.

Files written by this review: this record alone.
