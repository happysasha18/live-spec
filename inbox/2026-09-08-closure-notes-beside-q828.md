# Seven things the q-828 closure review noticed outside its reach

From: the push-review pass of 2026-09-08, over the range 5020064c..fa05011c. Each paragraph is one
thing that is true and that the closure reach did not cover. Nothing here opens a row and nothing
here asks for a repair; the intake sweep decides whether any of it is owed anything.

The spec sentence the row corrected is quoted verbatim in `docs/spec-format.md`, presented as what
the spec says today. That page walks one real criterion of this project's own spec before and after
its repair: "It now reads as follows, at 35 words with the same codes and five items in a list
below", and the block quoted under it contains the bullet the row rewrote. The bullet in the spec
now reads "pulling unblocked work off the board", the page's copy still reads "unblocked queue
work", and the word count the page states moved with it. The four other places holding the old
phrase — `guardrails/language-rules.json`, `docs/language-rules.md`, `docs/language-rule-coverage.md`
and the page's own "once read as follows" quote — are quoting a sentence the owner named as hard to
read on 2026-07-27, and each is correctly historical. This is the same class the push review of the
previous row deposited a few hours earlier, about a corrected done leaving two prose copies of the
replaced sentence standing, so it is the class's second occurrence in two consecutive pushes. Closed in this landing: the
page's current-text quote now carries the same words as the spec bullet it quotes. The word
count it states covers the sentence above the list, which this row did not touch, so it stands.

The row's recorded acceptance holds `spec/guardrails-freshness.md` with one negative arm alone,
`! grep -q 'unblocked queue work'`. A negative grep passes on a file that no longer exists and on a
file whose bullet has been deleted outright, so that arm proves the phrase is gone and nothing about
what stands in its place. The other three files each carry a positive arm beside their negative one.
The new test file carries the positive assertion for the spec — `assertIn("pulling unblocked work
off the board")` — but the test is not named in the acceptance command, so the row's recorded
acceptance and the guard that would catch a deletion are two separate reaches.

Line 26 of `hooks/conduct-law.md` now runs to 116 characters, against the 106-character longest line
the file carried before this change. The inserted words went in without a re-wrap, so one line of
the standing law is now the longest in the file by ten characters. No gate reads the width.

Three of the eleven re-aimed pins in `architecture/rules-and-settings.md` carry a label that does not
describe the line they point at, and did so before this change too. `skills/live-spec-base/SKILL.md:250`
is labelled "rule 26, INV-136/INV-139" and lands inside rule 24's worked-examples clause, with rule 26
beginning at line 263. `:157` is labelled "rule 7's worker-restore sub-rule, INV-298" and lands on the
co-location sentence. `:328` is labelled as the pointer to the settings ladder and lands in rule 36's
register text. The re-aim itself is faithful — each new line holds text byte-identical to what the old
pin pointed at — so the mismatch is inherited rather than introduced, and `check-pin-drift.sh` passes
all three.

Both skill-review records added in `fa05011c` open by saying "The reviewer is the session that made
the edit; nothing here is an independent read." The disclosure is the honest thing to write, and the
pack's own clean-context binding (SPEC INV-237) asks a differently-contexted seat only for a release
pass, so these records break nothing. It is worth a look at the intake because the two records are
the only reads standing behind two edits to the pack's shared rulebook.

The new sub-bullet names the design reviewer as "the one deliberate exception" to the lane that finds
a cause repairing it. One commit earlier in this same push chain, the prover pack's closure mode was
written to have a pass notice something true and hand it on without building the repair — the single
inbox deposit, judged later at the intake sweep. The deposit names no repair and a blocking finding
closes inside the same landing, so the prover is arguably not the banned shape at all; but the two
sentences now sit close together in the pack, and a reader who meets both may ask which one governs a
review pass.

The live-spec-base body stands at 483 lines and this edit spent ten of the seventeen the skill guide's
500-line ideal leaves. The rule's incident has no entry in `references/rule-origins.md`, which is where
each rule's citation, history and worked example live. The landing's own skill-review record names this
and says it is the fourth record to name the same gap for a different rule.
