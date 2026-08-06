# Guardrails — the pack's gates as git hooks

Two git hooks turn the rules the pack already lives by into things that actually stop you,
instead of things you have to remember.

## What each gate catches

**`pre-push`** — blocks a push unless every gate below holds (thirteen today — a, b, c, d, e, f,
g, h, i, j, k, l, m; this list is the one enumeration, kept current by the quantifier re-verify,
SPEC INV-170):

- **a. Fresh review.** A prover record dated today exists under `docs/prover/` and is
  committed. This is the push gate every push of live-spec must pass (SPEC anchor `M-6`):
  no push without a same-day whole-spec re-check on file.
- **b. Tests green.** `python3 -m pytest -q tests` exits clean — the SAME runner the CI mirror
  runs, so the local net and the second net can never disagree on what "the suite" is.
- **c. Every spec anchor has exactly one owner.** In this repo that's already asserted
  inside the test suite itself (`tests/test_traceability.py`), so gate (b) passing means
  gate (c) passed too — there's no separate check to run.
- **d. The matrix Reference agrees with the body.** `TEST_MATRIX.md` ends with a generated
  `## Reference` table (`scripts/build-matrix-reference.py` builds it from the rows'
  trailing anchors); `check-matrix-reference.py` reds a hand edit, a body anchor the
  table misses, or a table anchor no row carries, and states its reach on the green
  line (SPEC `INV-273`). It replaced the hand-walked coverage checklist at the matrix's
  format conversion (row 477); the per-row facts moved to the suite's row lint (`INV-274`).
- **e. The prototype fence holds.** A prototype lives in a fenced home (a `prototype/`
  folder — SPEC `INV-17`); a PROD file referencing anything inside that home is RED.
  This gate catches STRUCTURAL wiring — a prod file naming or loading a fenced file
  (a script src, an import, a link target). Narrative mentions stay clear of the gate: `docs/`, `attic/`,
  `inbox/`, `JOURNAL.md`, `ROADMAP.md`, `NEXT_STEPS.md`, any `README.md` under
  `guardrails/`, and `.live-spec/` are excluded, so a journal can talk *about* a
  prototype without tripping the gate. If no `prototype/` directory exists (or it's
  empty), the gate passes — there's nothing fenced yet. A host that names its fence
  home something else passes that name as the script's second argument
  (`check-prototype-fence.sh <repo-root> <fence-dir-name>`).

- **f. Skill loadability.** Every `skills/**/SKILL.md` parses: frontmatter, name, description,
  version (`check-skill-loadability.sh`).
- **g. Pin drift.** ARCHITECTURE.md's `file:line` pins still resolve; the named thing is
  normative, the line a cache (`check-pin-drift.sh`).
- **h. Host checks.** The four scaffold checks (completeness · tests-present ·
  traces-to-spec · conflicts) run against the base diff (`scaffold/guardrails/check_*.py`).
- **i. Shipped language.** No Cyrillic or owner-name in the shipped set (SPEC `INV-120`,
  `check-shipped-language.sh`).
- **j. No broad kill.** No tracked script name-kills a browser broadly (SPEC `INV-162`,
  `check-broad-kill.sh`).
- **k. Freeze.** Guarded docs match their compaction baseline where one is armed
  (`check-freeze.sh`).
- **l. Muted launch.** Every browser-driving script launches muted (SPEC `INV-157`,
  `check-muted-launch.sh`).
- **m. Config health.** The installed hooks match their `guardrails/` sources byte-for-byte
  (SPEC `INV-175`, `check-config-health.sh`).
- **ae. Named checks.** `scripts/check-registry.json` records what each runnable file a skill body
  names is: its kind, its handle, and which tree it judges. The record also holds whether the file
  belongs in an adopting project, what it reads on its own, and what it needs. `check-named-checks.py`
  recomputes every field from the tree and reds a disagreement. It also reds a skill body that names
  a check measuring this pack's own machinery (SPEC `INV-306`).

Each check lives in its own small script so it can be run and tested on its own, pointed at a
scratch file instead of the real repo.

**`pre-commit`** — the concurrent-edit fence. It protects against two sessions writing the
same repo at once. It is **off by default**: if no `.live-spec-fence` file exists at the
repo root, the hook does nothing. A session opts in by running `guardrails/fence-refresh.sh`,
which records the commit it started from. From then on, if the commit at the repo's tip ever
moves without that session's knowledge (another writer got there first), the next commit is
blocked with a message explaining what to review and how to re-arm the fence.

`pre-commit` also runs two content gates. It rejects a staged line stamped with a future time
(`check-future-times.sh`, SPEC `INV-24`), and it runs the **deferral-marker gate**
(`check-deferral-marker.py`, SPEC `INV-152`): a work item in `NEXT_STEPS.md` or a
`docs/decisions/*.md` page that parks for the human's word — "his to correct", "reserved for
his", "still his", "row N reserved" — must name its human-only fact (taste, policy,
irreversible, or device-feel), or drop the marker and do the item. A marker that names no
reason reds the commit with the file, line, and text. A negated mention ("NOT owner-reserved")
and a quoted narration of an old marker are both left alone. This is the mechanical net for the
same rule the chat-law hook delivers at the ask moment — the two arms of base rule 29.

## How to install

From the repo root:

```
./guardrails/install.sh
```

This copies `pre-commit` and `pre-push` into `.git/hooks/` and makes them executable.
Safe to re-run any time — it just overwrites with whatever is currently in `guardrails/`.
It does **not** create `.live-spec-fence`; the fence stays opt-in until you run
`guardrails/fence-refresh.sh` yourself.

## The runaway-child notice — a Stop-time report the owner wires by hand (SPEC INV-213)

`guardrails/check-runaway-child.py` reports a runaway descendant a finished worker left behind: a
process the run provably owns (in the run's own process group, or under its own temp tree) that is
orphaned — its owning parent no longer alive — and burning a full core. It reads no program name for
its verdict, only process group, parent liveness, and CPU share, so it can never target the human's
own copy of a program (SPEC INV-162). It is notice-first: it reports through the shared cleanup notice
and ends no process.

This is **not** installed by `install.sh`, and it takes **no** pre-push gate letter — a push gate runs
long after a runaway would have burned its cores, so the report belongs at the Stop surface. Wiring it
is left to the owner and is done **only when a session is quiet**, because a process scanner wired into
a live session's Stop hook could report against that session's own live background workers. To wire it,
add a Stop entry to `~/.claude/settings.json` that runs the check when a session stops:

```
"hooks": {
  "Stop": [
    { "hooks": [ { "type": "command",
        "command": "python3 /ABSOLUTE/PATH/live-spec/guardrails/check-runaway-child.py" } ] }
  ]
}
```

Run it against a simulated table first to see its shape without touching the real process list:

```
LIVE_SPEC_RUNAWAY_PROCS_JSON='[{"pid":1,"ppid":0,"pgid":1,"pcpu":0.0,"command":"init"},
  {"pid":777,"ppid":1,"pgid":'"$(ps -o pgid= -p $$ | tr -d ' ')"',"pcpu":98.0,"command":"python"}]' \
  LIVE_SPEC_OWNED_PGIDS="$(ps -o pgid= -p $$ | tr -d ' ')" \
  python3 guardrails/check-runaway-child.py
```

`LIVE_SPEC_OWNED_PGIDS` (space/comma-separated) and `LIVE_SPEC_OWNED_TREE` override the owned process
groups and owned temp tree; unset, the check owns its own process group and the repo's `.live-spec/`
tree. The check always exits zero, so the notice never blocks a stop.

## The worker-restore gate — a worker never restores a working tree with a git command (row 479)

`guardrails/check-worker-restore.py` reds when a worker run handed a shell one of the commands the
clause names. A worker runs no command that discards uncommitted work, in any tree: `git checkout --
<path>`, `git checkout .`, `git restore` outside `--staged`, `git stash` and its `push`, `save`,
`create` and `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and `git clean` with
`-f` or `-x`. Such a command's blast radius is a PATH, so its damage lands on files the worker never
wrote and its brief never named, and the write-set disjointness that fences concurrent edits gives
no cover against it. This rule binds a worker in every tree, including its own isolated worktree,
since a worktree shares one repository with the lanes beside it and a worker cannot read off its
brief what else that repository holds.

That list is stated in this section, in the gate's own header, and in `skills/live-spec-base/SKILL.md`,
`skills/build-pipeline/SKILL.md`, `skills/build-pipeline/references/delegation-protocol.md`,
`templates/agent.template.md` and `scripts/open-lane.sh`, in one wording, and
`tests/test_worker_restore.py` reds when two of them differ.

It opens the worker-run transcripts under the harness transcript root (`~/.claude/projects` by
default, `--root` or `LIVE_SPEC_TRANSCRIPT_ROOT` to move it): the files matching
`<project-dir>/<session-id>/subagents/agent-*.jsonl`, one per worker run. In each it reads the
records whose `type` is `assistant` and takes the `input.command` string of every `tool_use` block
named `Bash`. It reads no prose — a report that merely names a restore is left alone, and only a
segment whose first word is `git` counts, so the same text quoted inside a `grep` pattern stays
silent. The default window is the runs touched in the last 24 hours (`--since-hours`, `--all` for
every run on disk).

It is BLOCKING and rides the verify step rather than the push chain: a push gate runs long after the
bytes are gone, while verify is where the orchestrator accepts a worker's result. It is armed in two
places. `skills/build-pipeline/SKILL.md` step 8 names the command a session runs before it accepts a
worker's result, and `tests/test_worker_restore.py` runs it against the machine's real transcript
root so a red reaches a person on the next suite run. When the transcript root does not exist the
gate stands down by name and exits zero; when the root exists but holds no worker-run transcript, the
layout it reads has moved and it reds by name through `guardrails/nonempty_input.py` rather than
reporting clean over nothing (SPEC INV-218).

The gate carries a counting start, `COUNTING_FROM` in its own header (`--counting-from`,
`LIVE_SPEC_WORKER_RESTORE_FROM`), because this machine's transcripts hold 80 worker runs from before
the clause existed that carry a discarding command. A finding stamped before that date is carried as
history: every verdict line counts it and it reds nothing. A finding stamped on or after that date
reds, and so does a finding whose record carries no timestamp, since the gate cannot place it. Read
the history with `--counting-from 2000-01-01 --all`.

## How a host project adapts the pattern

**The ratchet gates (style lint · redundancy · freeze) install themselves in one pass:** run
`bash <pack>/adopt/install-ratchet.sh` from the host root (SPEC INV-172). It vendors the scripts
with a source-pin manifest, seeds the host's debt caps at the sizes measured that moment — green
at once, shrinking-only from then on — and generates the guard test. The section below covers the
structural gates, which are adapted by hand.

The gate shape (fresh review · green tests · ownership · full coverage · prototype fence ·
loadability · pin drift · host checks · shipped language · no broad kill · freeze · muted launch ·
config health) is the part worth copying as-is. What changes per host:

- **Test command.** Swap `python3 -m pytest -q tests` in `check-tests.sh` for whatever the host
  runs (`npm test`, `go test`, …) — and set the CI mirror to the SAME command, so the local net
  never under-runs what CI runs (a runner that collects fewer tests than CI false-greens locally).
- **Review cadence.** Not every host proves the whole spec before every push — a host may
  only require a full prover pass before a major version, checking something lighter
  (or nothing) in between. That cadence is a host setting; state it in
  the host's own profile and adjust `check-prover-record.sh`'s expectations (or drop gate a
  entirely) to match.
- **File names/paths.** If the host's matrix or prover folder lives somewhere else, pass
  it as the script's argument, or edit the default.
- **Fence home name.** If the host calls its prototype home something other than
  `prototype/` (say `sketches/` or `labs/`), pass that name as
  `check-prototype-fence.sh`'s second argument instead of renaming the script.

Everything else — the fence being opt-in, the plain-English failure messages, hooks
living in a version-controlled `guardrails/` folder rather than only inside `.git/hooks/`
so they travel with the repo — is meant to hold for any host.

## The gate contract (SPEC INV-47)

A gate born from a stated law scans the WHOLE tracked tree, retroactive by construction (SPEC
INV-176) — never only the diff. Pre-gate debt surfaces the day the gate lands; a backlog too
large to fold at once is absorbed by seeding the cap at the current size (SPEC INV-172).

Every gate script authored or next touched in this directory obeys three conventions (the
neighbours' CLI lesson, adopted from OpenSpec's gate contract — provenance and the full
borrowings inventory: docs/research/2026-07-10-originality-audit.md; the adopting row rests in
the queue archive):

1. **A blocking red carries one typed line.** Beside its human lines, a BLOCKING gate that fails
   emits exactly one parseable JSON object — `{"severity": "...", "code": "...", "message": "...",
   "fix": "..."}` — where `fix` is the same sentence a person reads. Agents parse the line; humans
   read the prose; both see one truth. (First gate under the contract: `check-prototype-fence.sh`.)
2. **Every check declares blocking or advisory.** A header comment names it; an advisory check
   prints its findings and never flips the exit code.
3. **All-or-nothing writes.** A script that rebuilds artifacts validates every output before writing any — no half-written artifact ever lands on disk.

Exempt by name: `check-push-reach.sh` — its exit code is a VERDICT (which checks the diff can
reach) rather than a defect; it is a decider, informational rather than a blocking gate.

## The CI mirror (SPEC M-5, ROADMAP row 14)

The gates' native home is the LOCAL pre-push hook — CI is the second net, never the first. Three
rules: **same checks, one source of truth** — CI invokes the same scripts in this directory
and never redefines a check; **the full set, always** — the reach map (SPEC INV-45) is a local latency
optimization, the second net stays conservative; **a plain workflow a host copies** — swap the test
command for your own, keep the script calls. The worked example is this repo's own
`.github/workflows/gates.yml` (note its `fetch-depth: 0` — the prover-record freshness rule reads
history — and its `TZ` pin, so "today" is measured in the author's own timezone, distinct from UTC).

## The kill-list scanner (SPEC E-26)

A host with taste-reviewed artifacts keeps a kill-list beside them (template:
`templates/KILL_LIST.template.md` — the human's cuts as dated literals, appended, never removed) and
wires a SCANNER: a test that reads the kill-list table and greps the artifact's surfaces for each
literal — a killed phrase reappearing turns the suite red. Same shape as every gate here: the list is the
declared truth, the test re-walks it every run.
