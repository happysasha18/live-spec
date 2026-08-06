# Night plan, 2026-08-07 — the four complaints, executed while Alexander sleeps

Root: Alexander's order of 2026-08-07 01:06 — present one plan covering the four complaints
before any work, execute it without deviation, and have the result survive an adversarial
review by a fresh reader. His 01:41 word released the execution: go by the queue, use the
budget wisely, quality first. The four complaints are rows 568, 569, 570 and the field
evidence on row 166. Rows 572 and 574 ride as repairs. His three answers of ~01:10 are on
record in DECISIONS.md and bind every block below.

## Block 1 — repair: the edit-safety check learns the session's own saves (row 572)

Root: the problem ledger's second occurrence, 2026-08-07 00:29, carried by his 01:06 order.
The check that guards against two windows editing at once currently blocks this session's
own second save and demands a hand reset. The fix the ledger names: after this session's own
successful save, the check updates its reference point, and a save from another window still
blocks. Worker: a mid-tier worker, since the design is already named in the row. Proof: one
session lands two saves with no hand reset, and a foreign save still blocks; the ledger entry
flips to solved. Estimate: 30–45 minutes.

## Block 2 — repair: the test suite stops leaking a temp folder per run (row 574)

Root: found at the 00:20 run, carried by his 01:06 order. Every full test run leaves one
temporary folder behind; the leaker hides among the tests that run late in a full run and is
clean in isolation. Worker: a mid-tier worker running a narrowing search over the suite.
Proof: three consecutive full runs leave the temp folder count unchanged, and the leak check
stays armed. Estimate: 45–90 minutes, most of it test-run time.

## Block 3 — the cost audit page is finished under his answers (row 568)

Root: his 00:17 complaint that the work is slow, and his three ~01:10 answers. The page
docs/audits/2026-08-07-cost-map.md still recommends numeric size caps in its verdicts; his
answer struck caps everywhere, so the verdicts for the rule-writing and review steps are
rewritten to his one standard: no redundancy, and no work before its subject settles. The
test-plan verdict is restated as the standing rule he confirmed. The remaining
process-invented cost — the standing instruction to run every test on every working run —
becomes its own repair row: during work a session runs the tests near its change, and the
full suite still runs at every landing and every publication gate, so nothing ships with
less proof than today. Each repair gets its own queue row from 575 up. The page's prose is
redrafted by a clean writer from a plain brief, since Alexander reads it. Proof: the page
lists each fixed cost with price, demanding rule, author and verdict; the repair rows stand
in the queue; his own read happens in the morning and stays the last open box on the row.
Estimate: 45 minutes.

## Block 4 — grounded work blocks become written law (row 569)

Root: his words of 00:17, 00:42 and 00:46 — work blocks ran that he could not connect to any
request of his. The rule already rides every prompt as session-rules law 7. Tonight it gets
its durable home: one invariant in PRODUCT_SPEC.md (next free invariant number) saying a
work block opens by naming its root — his dated request, a standing instruction of his, or a
stated reason, with machinery never a root — and the delivery report accounts each block
against the plan it announced. The build-pipeline skill's report shape gains that accounting
line. This very plan page is the night's plan-home, and every block above opens with its
root, so tonight's transcript is the row's first evidence. Proof: the invariant stands in
the spec, the report shape names it, the transcript shows each block's root line. Estimate:
30 minutes.

## Block 5 — the fixed rulebook load is measured and cut (row 570)

Root: his 00:17 complaint that the context is huge. First measure: byte and token counts for
the shared rulebook and each working skill, recorded before and after. Then cut, worst
first: each file is restructured so the main file carries every rule in brief with detail
moved to reference files read at need, following the published skill-format guidance. The
one standard is his: nothing removable without losing meaning, and no rule lost. Each
rewritten file gets a fresh-context verification pass that compares the old rule inventory
against the new one and blocks the landing on any lost rule. Rewriters run on the strong
worker tier; verification runs fresh. The night takes the shared rulebook and the heaviest
working skills in measured order and goes as far as it goes; what remains stays on the row
with its measurements, and the installed copies are re-synced for whatever landed. Proof:
before and after numbers on the row, verification records per file, installed copies in
sync. Estimate: 2–4 hours, the night's largest block.

## Block 6 — the fresh-seat adversarial review

Root: his 01:06 order's third sentence. After the blocks land, a fresh reader with clean
context is briefed from the primary sources — this plan, the queue rows, the diffs — and
sets out to break the night's work: rules lost in the cut, verdicts that drift from his
recorded answers, repairs that fix an instance and miss the class. Findings get fixed the
same night where mechanical, and queued with the morning report where they need his word.
The reviewer runs on the strongest tier at hand, per the standing quality line. Estimate:
45–60 minutes.

## Close

Each block lands as its own commit, staged by name. The full suite runs at each landing.
One push at the end after the whole gate set passes, under the standing green-push
authorization. The journal gets the night's chapter, NEXT_STEPS is replaced, and the
morning report opens with what shipped, what remains, and the one thing waiting on him:
reading the finished cost page. Row 166's board work — the fresh adversarial review of the
board's specification and the stage-ladder re-map — starts only if the night still has room
after Block 6, and otherwise stands first in the morning queue, per the forward queue's
order.
