# Notes beside q-834, from its closure review

True things the closure review of the 6.1.4 push found outside its reach, and one thing it found
inside this pack's record that no row here repairs. One paragraph each. Nothing opens a row; the
intake sweep decides whether any of it is owed one.

**A closed row of this pack stands on an acceptance that runs nothing.** q-833 was abandoned today
because the acceptance it was admitted with drove a pytest module with `python3 -m unittest`, which
collects none of its bare `test_` functions and exits 0 with the count hidden. Reading every
`unittest`-driven key in `scripts/plan_checks.py` for the same shape — a module defining no
`TestCase` class — finds exactly two rows in the whole table, and the other one is closed: q-829,
the 6.1.1 release row, whose key drives `test_release_6_1_1`, a module of eighteen bare test
functions. Under pytest those eighteen pass, so the work q-829 shipped is sound; what is empty is
the evidence its close rests on. The acceptance a row is admitted with is anchored on its checkpoint
and nothing may move it, which is the point of that anchor, so this cannot be repaired in place:
editing the key makes the verifier and the push-time re-run gate refuse it as an acceptance that
moved. The two roads that exist are to leave it recorded as it stands, or to reopen the row against
this as its false condition, abandon it the way q-833 was abandoned, and carry it to a new row with
a key that runs. The first is what stands today. What would stop the class going forward is
admission refusing a key that collects nothing, which nothing does today.

**A recorded acceptance that pins a release literal goes red at the next release.** q-829, q-831,
q-832 and q-834 each carry an arm of the form `test "$(cat VERSION)" = "<their own version>"`. Every
one of the first three returns non-zero now that `VERSION` reads 6.1.4, and
`guardrails/check-acceptance-rerun.py` selects a done row whose key names a file the push touched —
so a push that moves `VERSION` selects exactly the rows whose keys that move breaks. The same
tension has no repair in place, for the same anchor reason. What a new row can do is leave the
release literal out of its acceptance: that every version surface agrees with `VERSION` already has
one home in `tests/test_version_is_one_fact.py`, and a claim about one particular release belongs
to that release's own chapter assertion, which stays true forever.

**With no run mode named, the contract is never consulted.** `verify` asks the run-mode contract
only where the environment names a mode. A tree whose `guardrails.config.json` is corrupt, or which
records `row.decides_verdict` as false, still writes a receipt when a run names no mode. The
direction is safe — an unnamed run is a row run by the contract's own default, and the recorded key
runs either way — and making every ordinary verify depend on a readable contract would refuse hosts
that carry none. It is recorded because the tree does say something there that nothing reads.

**`close` reads the receipt's exit codes and never that the receipt names only the recorded
command.** `verify` now guarantees it, so the only way past is a hand-forged `RECEIPT:` line, which
is the hole both `close` and `guardrails/check-close-receipt.py` already document and which the
push-time re-run gate answers by running the recorded key itself. A one-line comparison in `close`
would shut it.

**`grep -q '^### 6.1.4'` is a prefix match.** The release arm of q-834's acceptance passes against a
heading renamed `### 6.1.4-gone`; it goes red only when the heading is gone. Loose rather than
vacuous, and the same shape every release row's chapter arm has carried.
