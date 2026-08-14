# The local-code route, measured in files and bytes

Mission: move the settings ladder out of `skills/live-spec-base/SKILL.md` into an on-demand module
inside the same package. This file records what the **local-code route** loads before its first action
on a representative local code change, measured before the split and again after it, by the same
method.

Base: `green/2026-08-14-claude` @ `4e8df4c`. Branch `ladder/2026-08-14-settings-split`.

## Method

The route is resolved entry point by entry point. Each resolved file is measured with `wc -c` on its
real path. A hook's contribution is measured by **executing** the wired hook, with the working
directory set to the repo worktree, and counting the bytes it writes to stdout. Reading the hook's own
source would count text the model never sees.

Entry points, in the order the harness reaches them:

1. `~/.claude/settings.json` — read for its `UserPromptSubmit` hook array; every entry with no matcher
   fires on every prompt. Three are wired: `clock-hook.sh`, `chat-law-hook.sh`, and
   `hook-meter.py register-judge-report.sh`.
2. `~/.claude/CLAUDE.md` — a symlink to `~/.claude/playbook/CLAUDE.md`, loaded by the harness at
   session start.
3. That boot file's own **Bootstrap** section, read line by line for what it names as loading before
   any pack file: the personal profile `~/.claude/live-spec/profile.md`, and the pack
   (`live-spec-base` plus `build-pipeline` for a non-trivial change).
4. Each named skill's `SKILL.md`. That file is then grepped for any reference it instructs the reader
   to open **before** the first action, which keeps an on-demand module out of the always-loaded set.

### The gap, named

A true fresh-session runtime trace is unreachable from inside a worker. This session runs under an
existing context, and it can open no fresh top-level session whose transcript it could then read. What
is recorded below is the closest honest measurement the rule allows: the route's entry points resolved
file by file with real bytes. Two consequences, stated plainly:

- The harness's automatic load of `~/.claude/CLAUDE.md` at session start is **proven by documentation**
  here, and by no transcript this session observed. The hook stdout figures are proven by direct
  execution of the wired hooks.
- That the model, having read the bootstrap lines, then opens `profile.md` and the two skill bodies is
  **model compliance**. The repo holds no mechanism that forces a `SKILL.md` body to load. The route
  below is the route as instructed, and that is the route the split changes.

The per-file resolution above is the measurement. A static `wc -c` sweep over the whole skill tree
accompanies it in the appendix, and stands in for it nowhere.

### Which copy the route serves

`~/.claude/plugins/installed_plugins.json` names no `live-spec`, so this repo reaches a session as an
unregistered plugin. The Skill tool therefore resolves skill bodies from
`~/.claude/skills/<name>/SKILL.md`, which `install.sh` populates by copying the repo's `skills/*`. The
two locations have drifted. At `4e8df4c` the repo's `live-spec-base/SKILL.md` is 64,348 B and the
installed copy is 64,728 B, a gap of 380 bytes.

Both figures are carried below. The **repo source** column is the one the split moves, and the one the
before/after delta is taken on. The **installed** column is what a session on this machine would load
until `install.sh` runs again. This mission's boundary holds every write out of `~/.claude`, so the
installed column stands still by construction. It is recorded to keep the drift visible.

## Before the split — `4e8df4c`

| # | What loads | Path | Repo source (B) | Installed / runtime (B) | Proof |
|---|---|---|---|---|---|
| 1 | boot file | `~/.claude/playbook/CLAUDE.md` (via `~/.claude/CLAUDE.md` symlink) | — | 1,621 | `wc -c`; harness load documented |
| 2 | personal profile | `~/.claude/live-spec/profile.md` | — | 7,738 | `wc -c`; named in CLAUDE.md Bootstrap |
| 3 | clock hook stdout | `~/.claude/hooks/clock-hook.sh` | — | 172 | executed, stdout counted |
| 4 | chat-law hook stdout | `~/.claude/hooks/chat-law-hook.sh` | — | 4,484 | executed, stdout counted |
| 5 | judge-report hook stdout | `~/.claude/hooks/register-judge-report.sh` | — | 0 | guard `[ -f "$VERDICT" ] \|\| exit 0`; silent on a clean turn |
| 6 | shared rulebook | `skills/live-spec-base/SKILL.md` | 64,348 | 64,728 | `wc -c`; CLAUDE.md Bootstrap names it |
| 7 | build skill | `skills/build-pipeline/SKILL.md` | 64,143 | 64,028 | `wc -c`; CLAUDE.md Bootstrap routes a non-trivial change here |
| | **Total before first action** | | **128,491** (pack only) | **142,771** | |

Files loaded before the first action: **6** (boot file, profile, two skill bodies, plus two hook stdout
injections that are content but not files; the third hook contributes nothing on a clean turn).

Two things stayed out of the count, each for a stated reason. `build-pipeline/references/*.md` (8
files) are reached by in-body links at named steps; the earliest of them,
`references/request-kind-table.md`, opens at the door. `skills/live-spec-base/` carries **no**
`references/` directory at `4e8df4c`: the rulebook is one 64,348-byte body, and the settings ladder
sits inside it.

### The ladder's share of the rulebook, before

| Part of `skills/live-spec-base/SKILL.md` | Lines | Bytes |
|---|---|---|
| everything above the ladder | 1–627 | 54,369 |
| `## The settings ladder` through the end | 628–708 | 9,979 |
| whole file | 708 | 64,348 |

The ladder section proper runs lines 628–705; lines 706–708 are the file's closing pack roster, which
belongs to the rulebook and stays.

## After the split

Same route, same method, same machine, re-run after the move and its pointer repair.

| # | What loads | Path | Repo source (B) | Installed / runtime (B) | Proof |
|---|---|---|---|---|---|
| 1 | boot file | `~/.claude/playbook/CLAUDE.md` | — | 1,621 | `wc -c` |
| 2 | personal profile | `~/.claude/live-spec/profile.md` | — | 7,738 | `wc -c` |
| 3 | clock hook stdout | `~/.claude/hooks/clock-hook.sh` | — | 172 | executed, stdout counted |
| 4 | chat-law hook stdout | `~/.claude/hooks/chat-law-hook.sh` | — | 4,484 | executed, stdout counted |
| 5 | judge-report hook stdout | `~/.claude/hooks/register-judge-report.sh` | — | 0 | guard, silent on a clean turn |
| 6 | shared rulebook | `skills/live-spec-base/SKILL.md` | 56,083 | 64,728 (unreached) | `wc -c` |
| 7 | build skill | `skills/build-pipeline/SKILL.md` | 64,143 | 64,028 | `wc -c` |
| | **Total before first action** | | **120,226** (pack only) | — | |

One file sits outside that table, and holding it there is the point of the move:
`skills/live-spec-base/references/settings-ladder.md`, 9,680 B. It opens at the step that resolves a
setting, and stays closed otherwise.

The installed column stands still by construction. This mission's boundary holds every write out of
`~/.claude`, so no `install.sh` run carried the split to the runtime location. After such a run the
route would read as the repo-source column.

## The delta

| Measure | Before | After | Delta |
|---|---:|---:|---:|
| files loaded before the first action | 6 | 6 | 0 |
| of those, pack skill bodies | 2 | 2 | 0 |
| pack bytes loaded before the first action | 128,491 | 120,226 | **−8,265** |
| `live-spec-base/SKILL.md` bytes | 64,348 | 56,083 | **−8,265** |
| `live-spec-base/SKILL.md` lines | 708 | 645 | −63 |
| bytes reachable on demand | 0 (base skill had no `references/`) | 9,680 | +9,680 |
| markdown files under `skills/` | 37 | 38 | +1 |
| bytes under `skills/` | 491,594 | 493,009 | +1,415 |

The route's file count holds. The module is a file the route can reach, and the door leaves it closed.
What moves is the byte weight carried before the first action, down 8,265 bytes. That is 12.8% of the
rulebook body, and 6.4% of the pack bytes the local-code route loaded before the split.

The pack grew by 1,415 bytes overall, which is the split's honest cost. The module carries a short
preamble naming what it is and when to open it, and the rulebook keeps a pointer section in the
ladder's old place. Every rule of the ladder reads exactly as it read before, and every one of them
stayed mandatory.

## Appendix — accompanying static sweep

A `wc -c` sweep over `skills/` is recorded beside the trace, since it counts files the route never
loads. Before the split: **37** markdown files under `skills/`, **491,594** bytes in total. The
local-code route loads two of those 37 files.
