# A worker's git restore can throw away every sibling lane's night

**Birth of this message.** The tlvphotos window lived the fault and carries the evidence. Five lanes
were rolling in one pair of trees on the owner's raised lane cap when one worker restored a shared
file with `git checkout -- <path>`. Three minutes later another lane began editing the sources that
assemble into that same file. Nothing was lost by that margin alone.

## What happened

A worker was asked to prove a test row red before writing it. The honest road it picked was to mutate
the shipped client bundle, run the suite, and restore. It restored with
`git checkout -- engine/assets/exhibition.js`, which discards every uncommitted change in that file
rather than the worker's own. At that moment the file carried nothing of anyone else's, so the tree
survived. The concurrent lane that started writing `engine/client/00-prelude.js`,
`01-knobs-lang-history.js` and `10-share-toast.js` three minutes later would have had its work
silently erased on the next such restore, with no red anywhere and no line in any report.

The worker's own account of the restore reads as correct work: it names the mutation, names the
restore, and pastes `git status` showing the file clean. Clean is exactly what the discard produces,
so the evidence a careful worker pastes cannot distinguish the safe case from the destructive one.

## Why the pack's rules do not catch it today

Base rule 7 fences concurrent EDITS: re-check `git status` and HEAD before writing, keep write-sets
disjoint, give an overlapping lane its own worktree. Every clause reads as a rule about writing the
files a brief names. A restore is a different act: it is a git command whose blast radius is a path,
and its damage lands on files the worker never wrote and never named. The brief-time disjointness
clause holds the write-sets apart and says nothing about a command that reaches past them.

Red-first proof is the pack's own method, and mutating a shipped artifact to prove a row red is a
normal way to run it, so this act will recur in every parallel session.

## What the rule could say

A worker restores a file it mutated by writing its saved bytes back, and runs no git command that
discards working-tree changes while any sibling lane shares the tree. The natural home is base rule 7,
beside brief-time disjointness, and the natural arm is one line in every worker brief the pack hands
out, since the worker is the actor. A mechanical arm is available too: a guard that reds when a
session's transcript carries a discarding git command against a path outside the brief's write-set.

The stronger answer may be that a lane which needs to mutate a shared artifact earns worktree
isolation by that fact alone, the way an overlapping write-set already does. The tlvphotos window has
no standing to pick between the two.

## Who threw it

The tlvphotos window, night session of 2026-07-27, running five lanes across `~/tlvphotos` and
`~/exhibition-engine`. The near miss is recorded in that project's own session checkpoint.
