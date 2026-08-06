# A session extract cannot recover what the owner pasted, and the opening read has no trigger

Lived: Rule 35 (SPEC INV-302) hands a fresh agent the person's own turns out of the transcript. Two faults showed up in one morning in the tlvphotos window, one in the instrument and one in the rule's opening half.

**Fault one: a paste is a placeholder in the transcript, and the body is nowhere.** On 2026-08-06 the owner's first message ended with the literal string `[Pasted text #1 +5 lines]`. He later asked me to recover those five lines from the transcript, naming rule 35 as the reason he expected them to be there.

What I ran and what happened:

- Read the session's own transcript, `~/.claude/projects/-Users-sashaabramovich/b5d847ca-ee7b-4638-8bda-d23c1a784839.jsonl`, and found the user record for that turn. Its `message.content` holds the same placeholder string `[Pasted text #1 +5 lines]` and no body. The record carries no `pastedContents` field of any kind.
- Read `~/.claude/paste-cache/`, which is where Claude Code keeps paste bodies. Thirty-four files, newest dated 2026-08-05 15:45. Nothing from 2026-08-06 at all. The five lines were never written there.

So the content is gone, and `scripts/session-extract.py` cannot recover it — the extract can only ever be as complete as the transcript, and the transcript drops short pastes. This matters because a paste is exactly where an owner puts the material he does not want to retype: a spec fragment, an error dump, another agent's report. Rule 35 promises "the person's own turns", and a pasted turn is silently a hole.

Two things this suggests, and the choice between them is live-spec's:

1. `session-extract.py` detects a `[Pasted text #N +M lines]` placeholder, looks the body up in `~/.claude/paste-cache/` by modification time against the turn's timestamp, and where it finds nothing, MARKS the hole in the extract instead of passing over it. A named hole is recoverable — the reader can ask the owner to paste it again while he still remembers. A silent hole is not.
2. A session that reads a placeholder in a LIVE turn says so at once, in that turn. I did this by hand today and it is what let him answer. Standing behaviour would be better than one session's judgement.

**Fault two: the opening half of rule 35 has no trigger, and it did not run.** The rule says a fresh agent reads the previous session's extract at the open, lists the owner's decisions with timestamps, and compares them against `DECISIONS.md` and `NEXT_STEPS.md`. The rule's own text grants this: "The opening step stays a discipline the seat holds, since a session's opening writes no committed artifact for a gate to read."

This session opened on `/clear` with a prompt naming a project and a resume file. It read `NEXT_STEPS.md` and went to work. No extract was pulled, no previous session was read. Nothing anywhere reminded it — the closing half has a gate (`check-handover-provenance.py`) and the opening half has nothing, so the opening half is the one that silently does not happen.

The cost showed up within the hour: `NEXT_STEPS.md` described eight darkroom items as still to be built, and five of them were already built and sitting unproven on a parked branch from the previous session. I found that by reading the branch, which the resume file did point at. A session that had read the previous session's extract would have known before designing anything.

The `UserPromptSubmit` hook that fires the six session laws into every prompt is one place a first-prompt-of-session trigger could live.

Need-by: none
Id: tlvphotos-2026-08-06-transcript-paste-and-opening-read

Who threw it: the tlvphotos window, session b5d847ca, 2026-08-06 morning, while working the darkroom queue. Raised because the owner asked for the five lines and then asked that this go here if the mechanism could not produce them.
