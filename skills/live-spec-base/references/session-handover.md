# Session handover — read at both ends by an agent that did not live it (rule 35, SPEC INV-302)

Read this when spawning the fresh agent that reads either end of a session. The rule's worked
failure and its withdrawn-script note live in
[worked-examples.md](worked-examples.md) instead.

That agent works from a session extract: the person's own turns, each with its timestamp.
`scripts/session-extract.py` pulls those turns out of one transcript, and its own header names where
the transcripts sit and which traps a reader meets there. The extract goes to a scratch directory,
since a transcript holds private conversation. At the close, the fresh agent writes the session
handover from that extract. The session that lived the work writes no handover of its own. A handover
is a file under `docs/handovers/` whose name ends in `-handover.md`. It says where it was read from in
three lines: transcript, extract, written by.

At the open, a fresh agent reads the previous session's extract. It lists every decision the person
made, each with its timestamp. It compares that list against `DECISIONS.md` and `NEXT_STEPS.md`. A
decision missing from both goes to the seat before work starts.

A session's opening writes no committed artifact for a script to read.
