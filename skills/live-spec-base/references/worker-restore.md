# A worker never restores a working tree with a git command (rule 7's worker-restore sub-rule, SPEC INV-298)

The verbatim clause every brief this pack composes carries, referenced from `SKILL.md` rule 7.

Before a worker mutates a file it means to put back, it reads that file and holds its bytes. A worker
puts a file back by WRITING ITS OWN SAVED BYTES. A worker runs no command that discards uncommitted
work, in any tree: `git checkout -- <path>`, `git checkout .`, `git restore` outside `--staged`,
`git stash` and its `push`, `save`, `create` and `store` forms, `git reset` with `--hard`, `--merge`
or `--keep`, and `git clean` with `-f` or `-x`. Such a command's blast radius is a PATH, so its damage
lands on files the worker never wrote and its brief never named. This rule binds a worker in every
tree, including its own isolated worktree, since a worktree shares one repository with the lanes
beside it and a worker cannot read off its brief what else that repository holds. A worker that holds
no saved bytes for a file it mutated, or that believes a file needs a git-level restore, HALTS and
reports the file and the mutation it made, and it writes no further file and runs no further command.
The orchestrator owns recovery: it restores the named file from the last committed stage, hands the
worker a fresh brief carrying that file's current bytes, and records the halt in the row's delivery
report, and the halted work resumes under that new brief. The orchestrator's own half: a finished
build stage is committed before the next worker touches its files.
`guardrails/check-worker-restore.py` reads the worker runs' transcripts for the command and runs at
the verify step.
