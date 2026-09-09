# Notes beside q-835, from its closure review and from the day's own pushes

True things the closure review of this landing found outside its reach, and one the pushes
themselves showed. One paragraph each. Nothing opens a row; the intake sweep decides whether any of
it is owed one.

**The push record chases commits the gates themselves demand.** Gate a asks the review record to
name every commit in the pushed range, and it exempts a commit touching only `docs/prover/`, since a
record cannot name the commit that first ships it. It exempts nothing else. So a gate that refuses a
push and names its own fix — gate s asking for a skill review, gate g asking for a moved architecture
pin — produces a commit that lands after the record, enters the reviewed set, and makes the record
stale; the record is then extended and re-committed, and the next run can meet the same thing again.
That happened three times across the two landings of 2026-09-09, and each round costs a full gate
chain. The commits in question change no behaviour and exist because a gate asked for them. The
exemption the gate already carries for a record-only commit is the shape that would cover them; what
that would cost is the review no longer covering a real change that happens to ride in such a
commit, which is why this is written down rather than repaired in passing.

**The deposit gates read `inbox/` by position and know nothing of a letter's state.**
`guardrails/check-earned-message.py` and `guardrails/check-deposit-description.py` enumerate the
folder and judge every file in it, so a letter left standing in place and marked `handled`, `noted`
or `superseded` is still gated as live traffic. No letter uses that shape today — every finished
letter so far has moved to `inbox/handled/` — so nothing is broken now. Driven with and without a
`Status:` line, both gates return byte-identical verdicts.

**`scripts/state-probe.sh` imports `plan_checks` without a guard.** The reader for a letter's state
and the reader for recorded task state are both loaded defensively, and this one is not: a tree
without `scripts/plan_checks.py` loses the whole INBOX section with no line saying why, at exit 0.
It predates this landing and the status-view installer seeds that file, so no host meets it today.

**Two mutations of the letter-to-row link survive the tests and neither is a defect shape.** One
gates the link on an index cutoff whose output is identical because the third letter in the fixture
carries no row — the same family as a gate on the `.md` suffix that every letter has. The other
moves the probe's own `shown` counter into the branch for a letter with no row, so a tree where
every open letter carried a row would print the letters and the line saying nothing is unhandled on
one screen. The counter is machinery this row inherited rather than wrote, and the link itself stays
correct in both.
