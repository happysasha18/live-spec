# Skill review — live-spec-base (rule 35 after the handover gate was withdrawn)

`SKILL-REVIEW`

Skill: live-spec-base
Date: 2026-08-09
Reviewer: a fresh reviewer raised for this review alone, with clean context. It did not author the
day 2 cut or the repairs, and it wrote no file but this record. Base rule 33 asks for that freshness.

Verdict: the edited rule is fit to ship, with one wording repair owed on the actor's name. Two
blocking findings from this reviewer's first read were repaired before the verdict, and the text
judged below is the text that ships. The rule reads as one complete instruction, nothing under
`skills/` still points at the withdrawn script, and both ends of the rule now carry their own reason
for resting on the seat.

## What changed

One hunk in `skills/live-spec-base/SKILL.md`, rule 35, the session-record rule. The two sentences
naming `guardrails/check-handover-provenance.py` and its shape-only reading came out, because day 2
row 2.2 retired that script to `attic/check-handover-provenance.py`. In their place the rule states
that both ends stay a discipline the seat holds, and gives a reason for each end: the script that
read the handover's three lines was withdrawn after it caught no error in its life, and a session's
opening writes no committed artifact for a script to read. The rule count is unchanged, and the
frontmatter still reads thirty-five.

## Findings

1. **The pointer to rule 33 lost the thing it pointed at.** Repaired, and the repair is right. The
   2026-07-28 review folded that sentence in to name a shared arrangement: a machine reads the shape,
   and the seat holds what no machine sees. Rule 33 still runs that way, with
   `guardrails/check-push-review.sh` live on the push chain. Rule 35 now has no machine at either end,
   so the two rules no longer share a line. Deleting the sentence is the honest reading, since rule 35
   names no kin because it has none on this point.

2. **A machine-checkable quality left to attention, with no reason stated.** Repaired. The closing end
   now says the script was withdrawn after it caught no error, and the opening end keeps its own
   reason. That is the standard the pack holds its own rule home to, since
   `guardrails/check-language-rules.py` reds a rule that nothing holds when nothing says why. One
   residual stands, and it belongs to the owner's own row. Rule 30 states that a quality left to
   attention is a defect of the method and admits no exception, so the file now carries a stated
   exception against a rule with no clause for one. The day 2 verdict list already puts rule 30 to the
   owner with a recommendation, so this change ships a tension it did not create.

3. **The actor's name collides with the file's own use of those words.** Owed. The sentence reads
   "this project withdrew that script". Two rows of the settings table use "this project" for the
   reader's own project, and rule 30 says "the project" the same way. The base is installed into other
   projects, so a stranger reads a sentence saying their own project withdrew a script it never had.
   Name the pack as the actor instead. While that clause is open, "after finding no error it had ever
   caught" leans on a pronoun three nouns from its referent, and naming the script again reads
   straight.

4. **The in-house word and the event standing as actor.** Repaired. "The culling" is gone, and a
   named actor now carries the verb.

5. **One ragged line wrap stands where the first sentence was cut.** Minor, and this edit made it. The
   handover definition still ends on a two-word line. The orphaned "Rule 33" line is gone with its
   sentence.

6. **Nothing else points at the withdrawn script.** Reviewed and clear. Across `skills/` the word
   handover appears only inside rule 35, and the script's filename appears nowhere. Repository-wide
   the surviving mentions are dated records of past runs, the attic manifest, the day 1 and day 2
   culling notes, and two rows already marked retired or declined in `TEST_MATRIX.md` and the rotated
   roadmap. The push chain, the gate proof list, the continuous-integration mirror and the rule census
   carry no reference to it.

## The measures this review was held to

The census reads `skills/live-spec-base/SKILL.md` at 74 findings after the repairs, level with the 74
the 2026-08-07 record set against a ceiling of 92: 60 sentences past the word cap, 14 style findings,
no register findings. Every style finding sits elsewhere in the file and predates this change. The
three new sentences hold under the word cap, add no capitals, and use no cutting frame. The anchor,
named-check and loadability gates pass, and the findings-bound gate reports no document above its
record.
