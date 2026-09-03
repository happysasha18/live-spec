# Skill review — director (the Director runs the project; no idea shelf, no second list)

SKILL-REVIEW

Skill: director

Date: 2026-09-03

Reviewer: this seat, by hand — a real content read of the diff against the rest of the file, not
the generic skill-creator eval/iterate loop (that tool is for a skill with no dedicated project
harness; this skill already has one, `evals/director/`, the stronger project-specific proof).

Verdict: no findings. The change is internally consistent and complete; nothing else in the file
still assumes the framing it replaced.

## What changed

Commit `614cc25e` ("director: the Director runs the project; no idea shelf, no second list")
rewrites how the Director treats an "idea for later." The old rule put every named-but-not-asked-for
possibility on a standing idea shelf. The new rule judges each one: real and understood becomes a
plan row with its own reason to be queued; unclear draws one live question; a passing thought is
answered and nothing gets recorded. A new framing sentence opens the "First — what did the human
just do?" section: "The Director runs the project; the person is the one who asks for things done
in it." Three sites carry the change — the outcome table's "Idea for later" row, the conditional-
request paragraph (a request with an idea-shaped branch is judged the same way), and the "answer to
the Director's own question" paragraph (the reply opens a fresh row rather than filling a shelf
slot). File: 415 → 427 lines, well under the pack's own 500-line guidance.

## Consistency check

`grep -in "shelf" skills/director/SKILL.md` finds nothing — the old vocabulary (idea shelf,
IDEA_SHELF.md) is gone everywhere, not just at the three edited sites; no leftover sentence still
tells a reader to file something on a shelf that no longer exists in the rule. The three sites read
the same rule consistently: judge real-and-understood / unclear / passing-thought, the same three
outcomes each time, in the same order.

One point worth naming, not as a defect: the commit message and `DECISIONS.md` quote his words as
"he runs the project as its client, not its manager" — a contrast-frame construction
("X, not Y") this pack's own register rule forbids in prose. The line that actually landed in the
skill reads "The Director runs the project; the person is the one who asks for things done in it,"
which states the same fact without the forbidden shape. The skill text is the one a session loads
and reads on every turn; it holds to the rule correctly.

## Findings

None against the change's own content or its consistency with the rest of the file.

Freshness note, not this record's to resolve: both eval sets pinned to this skill
(`evals/director/scenarios.json`, 35 scenarios, and `evals/director/closing-scenarios.json`, 9
scenarios) are now stale against this file's current sha256 — a real behavior change, not wording,
so the pin is doing its job. `PLAN.md`'s own q-812 closing note already recorded this staleness and
deliberately held the 44-producer re-record rather than run it twice across two same-night skill
edits (this commit and q-812's own). Re-recording both sets is real, owed work; it is not this
review's scope, which is the diff's correctness and consistency, both of which hold.
