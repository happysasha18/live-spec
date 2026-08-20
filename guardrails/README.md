# Guardrails — the pack's gates as git hooks

Two git hooks turn the rules the pack already lives by into things that actually stop you,
instead of things you have to remember.

## What each gate catches

**`pre-push`** — blocks a push unless every gate below holds.

<!-- generated:count:gate-roster — scripts/gen-tree-counts.py owns the block below -->

The push hook runs 29 distinct gate letters today. The roster below is the whole set, one line per gate as `guardrails/pre-push` announces it.

Count them yourself, and list them:

```
grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push | sort -u | wc -l
grep -oE -- '-- gate [a-z]{1,2}: [^"]+' guardrails/pre-push | sort -u
```

A push of this repository is refused where either command disagrees with what stands here. The count decides how much of the tree a push protects. It also decides how long a push waits. It is read against the gate steps `.github/workflows/gates.yml` mirrors, which `guardrails/check-ci-mirror.sh` holds equal to this roster. The roster holds to no number of its own. A gate is added when a stated law earns one, and dropped when its law goes, so neither direction is better on its own. When the count rises, every push runs one more check and waits for it.

```
-- gate a: fresh prover record for today (one record per push: the re-check of the spec and the architecture, and the adversarial read of the pushed range, SPEC M-6/INV-116/INV-304) --
-- gate aa: doc findings bound (no live document above its recorded finding count; a cleared document stays at zero, SPEC INV-301) --
-- gate ad: published tree counts (every count this repository publishes about its own tree matches the tree, and the reproduction command beside it returns the published number, SPEC INV-305) --
-- gate ae: named checks (the registry says what each runnable file a skill body names is, SPEC INV-306) --
-- gate af: gate device manifest (guardrails/gates-manifest.json joins every gate's script, red proof and CI-mirror status from pre-push, gate-red-proofs.json and ci-mirror.json; it reds where a fresh build differs from the committed file, or where a gates.yml step's law sentence differs from the gate's own, SPEC INV-210/INV-212) --
-- gate b: test suite green (scoped by the diff's reach, SPEC INV-45) --
-- gate c: every spec anchor owned by exactly one architecture node --
-- gate d: TEST_MATRIX.md generated Reference agrees with the body (SPEC INV-273/INV-218) --
-- gate e: prototype fence --
-- gate f: skill loadability --
-- gate g: pin drift --
-- gate h: the four host checks (this repo attached as its own first host, SPEC INV-97) --
-- gate i: shipped-language (no owner name or stray Cyrillic in the shipped set, SPEC INV-120) --
-- gate j: no broad browser-kill (cleanup targets the test resource only, SPEC INV-162) --
-- gate k: compaction freeze (guarded docs' anchor map / markers / numbers unchanged, 2.0) --
-- gate l: muted browser launch (every browser-driving script launches muted, SPEC INV-157) --
-- gate m: config health (installed hooks match guardrails/ source, SPEC INV-175) --
-- gate n: the earned message (an agent's inbox deposit names its birth, SPEC INV-189) --
-- gate o: cleanup notice (every cleanup path that ends a process says what it ended, SPEC INV-204) --
-- gate p: touchpoint kind (a surface speaks only the kind its touchpoint affords, SPEC INV-205) --
-- gate q: waiting list (the board loses nothing — no over-cap shown set, no demotion into the void, SPEC INV-206) --
-- gate r: authority anchor (a decision recorded as the person's names its exchange, SPEC INV-207) --
-- gate s: skill review (a substantive skill change carries its skill-creator review record, SPEC INV-208) --
-- gate t: doc rotation (the pack's split-and-rotated docs lose nothing — every rotated row is findable in its archive and every archive is named in a manifest line, SPEC INV-209) --
-- gate u: CI mirror parity (every local gate is mirrored in CI or a declared carve-out, SPEC INV-210) --
-- gate v: judges listed (every wired chat judge is referenced in the installed settings.json, SPEC INV-211) --
-- gate w: every gate can fail (every gate in this chain carries a known-red proof, SPEC INV-212) --
-- gate x: generated index (the committed index equals a fresh build off the body; body and index agree; an empty body reds by name, SPEC INV-258/INV-259/INV-218) --
-- gate y: agent card (a live-spec host tree carries its .live-spec/agent.md card, SPEC INV-219) --
```

<!-- /generated:count:gate-roster -->

Each check lives in its own small script so it can be run and tested on its own, pointed at a
scratch file instead of the real repo.

### What runs locally, and what the server runs

The local chain is the fast set. Every gate above runs on a push except gate b, the pytest suite.
Measured on 2026-08-18: the local chain took 144 seconds, and the suite alone takes over twenty
minutes. The server runs that suite on every push, in the `gates.yml` step named
`test suite (gate b, full — the reach map stays local)`. A second local run bought a slower push and
no new protection. Set `LIVE_SPEC_PUSH_FULL=1` to run the old chain, gate b included and
reach-scoped. One thing the fast set gives up: `guardrails/check-suite-budget.sh` rides the suite,
so a push measures the suite's wall-time only under that flag.

Gate g, pin drift, is the chain's second cost: 56 to 63 seconds of every push. It stays local, since
pins are repaired because it stands there. It now runs only when the push can move a pin. That means
a diff touching `ARCHITECTURE.md`, `.live-spec/r5-rule-prices-2026-08-11.md`, `skills/`, the gate's
own two readers, or a file an `ARCHITECTURE.md` pin names. Anything the chain cannot read — no base,
no diff, no pin list — runs the gate. Measured on 2026-08-18: 103 seconds with gate g, 40 without.
The server runs gate g on every push, unconditionally, and so does `LIVE_SPEC_PUSH_FULL=1`.

### Notes on some of the gates

The roster above is the whole set. These notes enumerate nothing. They cover the gates whose
behaviour takes more than one line. A gate with no note here runs all the same.

- **a. Fresh review.** A prover record dated today exists under `docs/prover/` and is
  committed. This is the push gate every push of live-spec must pass (SPEC anchor `M-6`):
  no push without a same-day whole-spec re-check on file. One record carries the whole
  review a push owes (SPEC `INV-304`). On the push road the same check reads that record
  against the pushed range. The record names the base commit and every commit reviewed. It
  carries the `PUSH-REVIEW` marker and its five fields with values. No blocking finding is
  left open. Whether the review was adversarial rests on the reviewer; no script decides
  that. `docs/prover/README.md` holds the shape for a person writing one.
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
- **ad. Published tree counts.** `guardrails/tree-counts.json` declares every count this repository
  publishes about its own tree, the measurement that produces it, and the pages that state it.
  `check-tree-counts.py` re-measures each declared count against the committed tree and reds a page
  whose number disagrees (SPEC `INV-305`).
- **ae. Named checks.** `scripts/check-registry.json` records what each runnable file a skill body
  names is: its kind, its handle, and which tree it judges. The record also holds whether the file
  belongs in an adopting project, what it reads on its own, and what it needs. `check-named-checks.py`
  recomputes every field from the tree and reds a disagreement. It also reds a skill body that names
  a check measuring this pack's own machinery (SPEC `INV-306`).

**`pre-commit`** — the concurrent-edit fence. It protects against two sessions writing the
same repo at once. It is **off by default**: if no `.live-spec-fence` file exists at the
repo root, the hook does nothing. A session opts in by running `guardrails/fence-refresh.sh`.
The refresh records the starting commit on line one and the arming session's token on line
two (`$LIVE_SPEC_SESSION_ID`, else `$CLAUDE_CODE_SESSION_ID`, else empty). From then on, if
the commit at the repo's tip ever moves without that session's knowledge (another writer got
there first), the next commit is blocked with a message explaining what to review and how to
re-arm the fence. The session's own commits stay free. The `post-commit` hook re-arms the
fence to the new tip when the committing session's token matches the recorded one (ROADMAP
row 572). Only the arming session extends its own arm. A commit from another window carries a
different token and re-arms nothing. The recorded tip then goes stale, so the next commit
from anyone still blocks. With no token in the environment the fence keeps its old
manual-refresh behavior.

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

This copies `pre-commit`, `post-commit`, and `pre-push` into `.git/hooks/` and makes them executable.
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

The gate reds on this project's own sessions. The transcript root holds the owner's other projects too.
A discarding command in one of their sessions is their defect, as row 598 says in words.
The key is the session's recorded `cwd`: a session belongs to a neighbour when that directory exists
and git reads it as another repository. A session the gate cannot place elsewhere still reds. Only
where `cwd` alone answers nothing does the gate take one further look, at `effective_dir`. This is the
directory the one command actually ran in, once any `cd` inside it is walked — printed as `ran in`. An
owner's home directory (unplaceable) whose command `cd`ed into a real neighbouring checkout is that
neighbour's finding too (row 623). The look never overrides a `cwd` the key could already place. An
`effective_dir` that is itself `UNKNOWN` or unplaceable leaves the session reading as this project's
own, unchanged. The same holds when it lands back in this project's own repository — a sibling lane
worktree among them. A neighbour's finding is never dropped — it prints as a notice naming session,
directory, command and outcome, and reds nothing.

At verify, pass the exact transcript returned for the worker result being accepted:
`python3 guardrails/check-worker-restore.py --run <agent-*.jsonl>`. This mode opens one file, reads
every assistant `Bash` tool-use command, and applies no clock window, counting start, or
own-versus-neighbour downgrade. A missing or empty file reds. A red run never becomes acceptable:
recovery gives the worker a fresh brief, and the fresh run earns its own verdict.

The root form is a forensic census, not an acceptance verdict. With no `--run`, the check opens the
worker transcripts under `~/.claude/projects` by default (`--root` or
`LIVE_SPEC_TRANSCRIPT_ROOT` moves it), matching
`<project-dir>/<session-id>/subagents/agent-*.jsonl`. `--all` reads every run; otherwise it reads the
last 24 hours. It keeps old incidents visible and red without blocking unrelated later work through
a nondeterministic personal time window. Both forms read no prose: quoted examples and reports stay
silent because only a shell segment whose first word is `git` counts.

Every finding says what the shell did with the command. The `tool_use` block carries an `id`. The
shell's answer sits in the same transcript as a `tool_result` block repeating it as `tool_use_id`.
A call the harness refused is marked there by a `toolDenialKind` key. Its four values are
`automode-blocked`, `permission-rule`, `user-rejected` and `interrupted`. A call that reached a
shell carries no such key, whatever its exit status.

So a finding reads one of three ways. The command ran. The harness declined it. Or the transcript
answers nothing, and the outcome is unknown. All three red, because the rule forbids handing such a
command to a shell at all. Whether the shell obeyed lies outside the worker's reach.

What the outcome tells the reader is how much recovery it faces. The findings print ranked by that:
the executed ones first, the unanswered ones second, the declined attempts last. The unanswered ones
outrank the declined because they cannot be ruled out. The verdict line tallies the three. The typed
JSON line carries `outcome`, an `outcomes` count, and the first finding after the ranking.
tlvphotos asked for this on 2026-08-12, in
`inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md`. It had received a finding that read as
lost work, when the classifier had declined the command and nothing was lost.

The exact-run form is BLOCKING and rides verify rather than the push chain: a push runs long after
the bytes are gone, while verify is where the orchestrator accepts one worker result. The pipeline
skill names the command, and deterministic fixture tests prove both red and green. The suite no
longer scans this machine's growing transcript root. In forensic root mode, an absent root stands
down by name; a present root holding no worker transcript reds through
`guardrails/nonempty_input.py` rather than reporting clean over nothing (SPEC INV-218).

`hooks/worker-restore-guard.py` is the earlier arm. It denies the same command class at
PreToolUse(Bash), before the shell can discard bytes. `scripts/install-worker-restore-guard.sh`
supports `--dry-run`, copies the hook, wires it once, and self-tests one denied and one allowed form.
The hook does not guess whether its caller is a worker: the event carries no reliable seat/worker
identity. Instead it gives the safe rule to every caller — a worker writes only its own saved bytes;
without them it halts, and the orchestrator owns recovery from the last committed stage.

The gate carries a counting start, `COUNTING_FROM` in its own header (`--counting-from`,
`LIVE_SPEC_WORKER_RESTORE_FROM`). This machine's transcripts hold worker runs from before the clause
existed that carry a discarding command. This page states no figure for that class, and no figure
would hold. The runs live in a transcript root outside this repository, and that root grows while a
person reads it. Two readings minutes apart returned different totals on 2026-08-06. Ask the machine
that holds them instead. The command
`python3 guardrails/check-worker-restore.py --counting-from 2000-01-01 --all` lists every such run on
this machine, with the date each one carries. A finding stamped before the counting start is carried
as history: every verdict line counts it and it reds nothing. A finding stamped on or after that date
reds, and so does a finding whose record carries no timestamp, since the gate cannot place it.

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
