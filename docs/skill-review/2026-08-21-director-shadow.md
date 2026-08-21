# SKILL-REVIEW — director, first release in shadow mode

Skill: director
Date: 2026-08-21
New skill. No prior version, so nothing to diff against; the whole file was read cold.

## Who reviewed it

An agent that did not write the file, given the file, the package's requirements and its
prohibitions, and told to break it rather than approve it. It ran two rounds, the second
after the fixes from the first, and was asked to say which fixes were real and which were
rearrangements. It was also asked to argue back on one finding the author declined to fix.

## Round one — twelve findings

The reviewer was asked for four passes: break it by construction, check whether it is a
fixed pipeline under a new name, check whether it decides by keywords, and read the
English cold as someone meeting the project for the first time.

Two findings were the file contradicting itself, and both were correct:

1. The file forbids deciding by wording, and then defined **Halt** as the word list
   "stop, cancel, park, leave it" — the one row of seven described by lexicon instead of
   intent. A builder reading that row is being told to grep.
2. The file says the idea/instruction difference "is not politeness or grammar" and then
   illustrated it with a grammatical pair — subjunctive against imperative. The example
   taught the thing the sentence above it denied.

The other ten: no fallback for a message that is none of the seven acts; no rule for an
answer to a question the Director itself asked; no rule for a message with no words; a
contradiction between "a question touches nothing" and needing to read in order to answer
one; an urgent report classed as a plain observation; no stated home for the decision
sheet while promising a "later reader"; a specialist table whose order reproduced a
waterfall; one prescribed action for two different things in the question/musing row; no
worked example for the decision sheet, where the stakes are highest; unexplained jargon.

Fifteen changes were made. On the twelfth — a clause that is a question and a decision at
once, inseparably — the author declined and said so. The reviewer disagreed with the
reasoning and agreed with the outcome: the gap is closed, but by the "do not decide by
wording" rule rather than by "one turn, several acts", which handles acts that are
sequential, not fused. The reasoning is corrected here rather than in the file.

## Round two — two new holes, both from the fixes

The reviewer confirmed thirteen of fifteen fixes as real by reading the changed lines, and
found two holes the fixes had opened:

1. The new "not every message is one of the seven" section listed a greeting, a thank-you,
   a joke, a thumbs-up and a curse. Only the thumbs-up was qualified — "on something
   already agreed". So a real report delivered in a swear could be called conversation and
   dropped, citing the file. The other elements are now qualified the same way, and the
   priority against the repair test is stated.
2. The specialist table called for the spec author when "user-visible behaviour changes",
   while the worked example correctly declined the spec author because the spec was
   already right and the code disagreed with it. Two criteria for one decision. The table
   row now matches the rule.

## What the scenario runs then found, which no reading had

Three runs of thirty-five messages, described in `docs/prover/2026-08-21-director-shadow.md`.
The runs found a defect neither review round saw: the file's own "belongs elsewhere"
pointer to the communicator was being read as *requests about reporting are not work*, and
three separate agents cited that line to answer a plain request for a plan by creating
nothing. That line is now narrowed. A reader looking for holes did not find it; agents
using the file walked into it.

## Cold read

Read cold after the last change. The jargon flagged in round one is gone. The worked
example is the only place the file spends lines on illustration, and it earns them: it is
the section where a reader has to see the size of the thing rather than be told about it.
The file is 16 KB against the 56 KB of the `build-pipeline` it is meant to replace.

Verdict: ALLOW — a new skill, reviewed adversarially twice by an agent that did not write
it, with every finding either fixed or declined in writing, and with a run-found defect
that no reading caught recorded above rather than quietly patched.
