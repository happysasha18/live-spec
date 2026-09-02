# A person who did not build this can read the task list and understand it
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

(nothing yet)

## NEXT

(nothing yet)

## DECISION SHEET

Goal: task titles/group names in PLAN.md read in plain language a non-builder can follow, checked by an outside reader not the session. Outcome: state-probe.sh and render-board.sh print titles a reader can say what-it-gives-them and what-state-it's-in for every open row, without asking. Dimensions: board & visibility (source problem), documentation (titles live in PLAN.md prose). Known: current titles already read as plain sentences by design (PLAN.md's own titles ARE already outcome-phrased, e.g. 'A person who did not build this can read the task list...') but GROUP names (Board & visibility, Cross-project, Testing, etc.) and any residual jargon in titles are the likely gap; q-808's own text says of task LINES shown to him he could follow 1 in 3 -- audit against his literal complaint, not assumed. Unknown: exactly which lines/groups failed his read and why. Risk: none, reversible text edit. Specialist: sonnet worker in lane/q-808-plain-language-titles. Evidence: a fresh-eyes reading pass (a cold agent standing in for a non-builder reader) walks every open+recently-closed title and group name and flags any that need a builder's context to parse; those get rewritten; re-read confirms. Next: dispatch worker.
