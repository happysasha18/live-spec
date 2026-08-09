# The culling, recompiled against the cost of a change

Root: his order of 2026-08-09, 11:22, after reading the first night's results. He named the fault in
the old order: the cut should start where the machinery makes every change most expensive, and it
should cover everything rather than one file. Written 2026-08-09, 11:27, on commit `d80a7e0`.

The plan of 2026-08-08 stays the frozen record of what was tried. This one replaces its stage three
on his word, and it keeps his criterion untouched: a thing lives when it protects a stranger using
the pack, or the readability of his reports; twins merge.

## What the machine actually is

The first night counted one file and called it the rulebook. The full inventory:

| what | count |
|---|---:|
| shared rules in the base skill | 35 |
| rules inside the other nine skills | 53 |
| invariants in the product spec | 314 |
| all requirement codes in the product spec | 390 |
| rows in the test matrix | 551 |
| test files, and tests | 203, about 2 500 |
| checks on every push | 29 |

Eighty-eight rules and three hundred fourteen invariants. The first pass read thirty-five of them.

## The cost model, corrected

The old measure counted bytes a session reads before work. Reading is paid once per session. The tax
below is paid by every change, however small, and it compounds with the number of changes.

Measured on the night of 2026-08-09: removing one check that cost 0.06 seconds and had no recorded
catch took three hours from brief to green commit. Its own edit was minutes. The rest was tax.

| # | what the tax is | what it cost, measured | when it fires |
|---|---|---|---|
| 1 | the whole test suite runs inside one of the checks | 451 s of the 486 s all checks cost | every push |
| 2 | a fresh agent's adversarial review record, because the spec changed | ~12 min of agent time, 4 blocking findings | nearly every landing |
| 3 | a fresh agent's skill review record, because a skill body changed | ~10 min, two drafts refused | every skill-text change |
| 4 | the prose ratchets: findings may never rise, plus style, register and a 25-word cap | four blocked commits, each needing a rewrite | every document touch |
| 5 | re-freezing the spec, architecture and matrix baselines | one command, plus a red when skipped | every touch of those three |
| 6 | deletion bookkeeping: archive move, manifest line, spec tombstone, retired matrix row, queue rotation | five artifacts per removed thing | every deletion |
| 7 | one row per commit under a concurrent-edit fence | two blocked commits, one broken partial commit | every commit |

Row 6 is the trap. The paperwork that makes a deletion expensive is what stops the machine from
being cut back. It goes first, or every later cut pays it.

## The order, and why it is this order

**Phase A — make cutting cheap (first, because everything after it pays this).**
A1. Give the culling a named carve-out from row 6: during the campaign, a removal lands with its
archive move and manifest line alone, and the tombstone plus retired-row bookkeeping runs once per
batch instead of once per item.
A2. Take the nested suite run out of the push chain. This is row 1, the single largest number in the
whole machine, and it is already the first batch the old plan named.
A3. Merge rows 2 and 3 into one review per push. Both gates read the push range, so one fresh review
covering the push satisfies both. This keeps the protection and pays it once.

Declared measure for phase A: seconds per push, from 486 down, and artifacts per removed item, from
five down.

**Phase B — the prose ratchets (row 4).**
Four checks read the same documents with four different rules, and one of them forbids any document's
findings from ever rising. Keep the register check, which guards what he reads. Judge the other three
against the criterion, and state for each whether it protects a stranger or his reports.

Declared measure: blocked commits per landing, from four down.

**Phase C — the spec, which the first pass never opened.**
314 invariants against 551 matrix rows and 203 test files. The census here answers one question per
invariant: does a test hold it, and does anything outside this repository read it. An invariant no
test holds and no stranger reads is text.

Declared measure: invariants, from 314 down.

**Phase D — the rules, in groups.**
The first pass proved that ruling one rule at a time from summary tables produces wrong verdicts.
Three groups, each with one verdict pass and one review:
- D1, the nine working skills' 53 rules, which the first pass never read;
- D2, the base rules that state a prohibition, which stay whole and only lose their worked cases if a
  named step points at the page holding them;
- D3, the base rules that state a procedure, where the law stays and the cases move.

Declared measure: bytes a session reads before work, counted by the repaired command that includes
reference pages.

**Phase E — the install, and the stranger's run.**
The one breakage a person outside this project meets. The repair and its open fork stand in
`.live-spec/day3-opening-2026-08-09.md`.

## What comes back

The architecture-pointer check returns, on his word of 2026-08-09 11:22. Its queue row returns with
it: the check accepts a pointer when any matching word sits within a 51-line window, and a pass in
early August found 29 stale pointers green under it. The restore and the fix land together, so the
check proves a pointer against its own line.

## What stays his

Rule 30, which turns any machine-checkable property into a blocking check, and rule 23, which gives a
twice-broken behaviour a check of its own. They are the engine behind the 29 checks, and both carry
his own instructions.

## How a batch runs

One batch a day. Every removal is its own commit carrying its row number, so any one reverts alone.
One push a day, and one review pass over that push. The evening reports what moved, against the
measure the day declared in the morning.
