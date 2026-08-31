# The playbook repository — what it holds, and where each part belongs

Written 31.08.2026, from the live-spec window, in answer to the owner's question of 27.08 23:47:
does this repository earn a second home for something that could live in one place.

The repository is `happysasha18/playbook`, private, cloned at `~/.claude/playbook`. Every claim
below was read off disk on 31.08. The repository was read-only for this pass, and nothing in it was
changed.

## The short answer

The repository does one job today that nothing else on this machine does: it gives version history
and an off-machine copy to the two files every session reads — the boot file and the personal
profile. `~/.claude` is a plain folder with no version control, so without this repository those two
files exist as single copies on one disk. That job is worth keeping.

Everything else the repository holds is either a duplicate of something live elsewhere, or a record
of work that finished in July. Twenty-one files are tracked; twenty-one more sit on disk untracked,
so the backup this repository is kept for does not reach half of what is in the folder.

The recommendation is to keep the repository and narrow it to the personal layer. That is a smaller
change than folding it away, and it answers the owner's question directly: the second home earns its
place for two files and for nothing else in there today.

## What has happened since this page was written

All eight steps below ran on 31.08 from the window that owns `~/.claude/playbook`, and everything
was pushed. That repository now tracks eleven files, reports nothing ahead of its remote, and the
personal profile's report-format line points at the boot file rather than restating it. The two
sections below describe the state as it stood when this page was written, and they are kept as
written so the reasoning behind the answer can still be read. What is left for the owner is the
answer itself — keep the repository, narrowed to the personal layer — and the two things "What stays
open" names, neither of which the eight steps touched.

## One thing to fix first

The last commit, made 27.08, has never been pushed. The copy on GitHub still stands at 05.08. The
single reason to keep this repository is the off-machine copy, and that copy is currently 26 days
behind the profile a session reads today. The first act of the window that owns the repository is
`git push`.

## What reads the repository

Four live readers, and no others:

- `~/.claude/CLAUDE.md` is a symlink to `playbook/CLAUDE.md`. The harness loads it at the start of
  every session.
- `~/.claude/live-spec/profile.md` is a symlink to `playbook/personal/profile.md`. The boot file
  instructs every session to read it.
- `guardrails/language-rules.json` in this project pins about twenty language rules to numbered
  lines in `personal/profile.md`, recording where the owner's own wording lives.
- Two pointers in `skills/` cite `PLAYBOOK.md` — the base rulebook at line 237 for the convergence
  chapter, and the director's delegation reference at line 36 for how a brief is sized.
  `tests/test_convergence_rule.py` checks that the base rulebook still names the file.

The boot file's own last line points at `row52/migration-map.md`, and the profile's third line points
at `personal/profile-history.md`.

Nothing reads anything else in the repository.

## Every file, beside the home it belongs in

### Stays in the repository — this is its home

| File | Last changed | What reads it | Why it stays |
|---|---|---|---|
| `CLAUDE.md` | 27.08 | Loaded every session through the `~/.claude/CLAUDE.md` symlink | The only version history and the only off-machine copy it has |
| `personal/profile.md` | 27.08 | Loaded every session; about twenty rules in this project pin to its lines | Same |
| `personal/profile-history.md` | 30.07 | The profile's own third line points here | The readable account of how each setting arrived, which a diff does not give |
| `row52/migration-map.md` | 05.07 | The boot file's last line points here | It answers "where did my rules go" before the pack loads |
| `README.md` | 20.06 | A person opening the repository | It describes the repository, and it needs rewriting once the rest moves |
| `.gitignore` | 07.07 | git | Machinery of the repository itself |
| `tools/usage-audit.py` | 22.07 | The profile names it under `cost-levers` | The one script here, it reads the machine's own transcripts, and it has no other versioned home |

The profile names the script by filename alone, so the pointer does not resolve for a session that
has never seen this folder. The fix is one line in the profile giving the full path.

### Leaves the working tree and stays in the repository's git history

Nothing reads any of these. Each records work that closed in July, and dropping a file from a git
repository keeps every version of it in the history. None of them is lost by this.

| File | Last changed | Why it goes |
|---|---|---|
| `PIPELINE_UPGRADE_ROADMAP.md` | 12.07 | A plan from 03.07 with three items. All three shipped: the architecture document and the `architect` skill, the per-surface diff check, and the footprint classification |
| `claudemd_mining_s51.md` | 10.07 | A gap map that closed itself with a banner on 07.07 when the last of its eleven items landed |
| `row52/CLAUDE.draft.md` | 05.07 | A draft of a change that landed 05.07 |
| `row52/CLAUDE.final.md` | 05.07 | The text that became the boot file that day |
| `row52/profile.draft.md` | 05.07 | A draft of the profile that landed the same day |
| `row52/attic/CLAUDE.md.2026-07-05` | 05.07 | The pre-change original. The same rollback copy also sits at `~/.claude/CLAUDE.md.bak-*` |
| `row52/attic/profile.md.2026-07-05` | 05.07 | Same |
| `migration/2026-07-10-fleet-survey.md` | 10.07 | A snapshot of four repositories as they stood on 10.07; three have moved since |
| `personal/profile.md.bak-pre-langsweep` | 30.07 | A second copy of text that `profile-history.md` already holds |
| `inbox/2026-08-05-from-live-spec-readability-audit.md` | 05.08 | A reading pass over four documents here. Two of the four leave the working tree by this page, and the findings on the remaining two are worth one walk before the file goes |

### Most of it is already stated in the pack, and the file waits on another lane

`PLAYBOOK.md`, 36 kilobytes, last changed 12.07.

This is the old working agreement, and it is the file the owner's question was really about. Almost
every chapter in it points at its own successor in the pack, in its own words: the delegation
chapter at base rule 5, the pipeline chapter at base rules 15 and 16, the convergence chapter at base
rule 22, sourcing at base rule 13, showing work at the communicator's rules. Its own maintenance rule
says to commit and push it the same session a principle changes, and it has stood unchanged for seven
weeks while the pack moved almost daily. A handful of lines in it are about track-coach —
re-rendering every deposited widget, the version printed in the widget footer, the sample set the
visual check walks — and those belong to that project.

Three lines were checked against the whole pack and found nowhere else, so they need a home before
the file goes:

- **Every plan names what it must not touch.** The chapter calls breaking a working thing the
  cardinal mistake here, and asks that the parts already working be stated back as out of scope
  before any edit. The 07.07 mapping pass recorded this one as still unplaced, and it is still
  unplaced. Its home is the pack.
- **"What's the point" and "what a mess" mean stop editing and read the rendered output.** The
  owner's own signal, from 21.06, that a change has gone cosmetic or that stacked layers have become
  the real problem. Its home is the pack.
- **The template for a cold restart** lives at `~/.track-coach/resume_autopilot.sh`. The profile
  names the mechanism and leaves out the path. Its home is that one profile line.

Everything else in the file is a second statement of something live, which base rule 4 calls a
defect. Removing it also takes three edits in files this window does not own — the two citations in
`skills/` and the assertion in `tests/test_convergence_rule.py`. Those belong to the lane working on
giving every rule one home. Until that lane takes them, the file stays where it is.

### Belongs at `~/.claude/hooks/`, where the scanners read it

`hooks/affirmation-personal.json` and `hooks/scissors-personal.json`, both 22.07.

The two scanners read `~/.claude/hooks/affirmation-personal.json` and
`~/.claude/hooks/scissors-personal.json`. The copies here are byte-identical to those, and they are
kept in step by hand. The mirror reaches two of the four personal overlays: `hedge-personal.json` and
`register-judge-personal.md` sit at `~/.claude/hooks/` alone, with no history and no off-machine copy
at all.

The clean form is the one the profile already uses: the four overlays live in this repository and
`~/.claude/hooks/` holds symlinks to them. That touches armed hooks, and this plan's first law of
execution forbids editing a hook while the plan runs. So the copies stay for now, and the gap is
written into the plan's blockers.

### Its home is a project that does not exist yet

`inbox/2026-07-06-spend-monitor-agent.md`, 06.07, 726 bytes.

A wish the owner spoke in another window: an agent that watches everything he pays for. It was parked
here so a memory wipe would not lose it, and it has sat eight weeks. No project owns it, and this
folder is the only cross-project shelf on the machine, so it stays until a project does.

### Goes to the trash

Both are untracked and covered by `.gitignore`, so the repository never backed them up.

- `PLAYBOOK.html`, 07.07 — a rendered page of a document that is retiring.
- `row52/attic/skills-bak/`, twenty files, 05.07 — copies of five pack skills as they stood on
  05.07. This project's own git history holds all five from 04.07 onward.

## What folding the repository away would cost

Per part, if the folder were removed and the two symlinks replaced by real files:

- **The boot file and the personal profile** would lose their version history and their only copy off
  this machine. That is the defect this arrangement was built to close on 05.07, and a working tree
  has already been lost once on this machine.
- **The record of how the personal layer arrived** — the migration map, the drafts, the pre-change
  originals, `profile-history.md` — would need a new home somewhere, and the two pointers into it
  from the boot file and the profile would break.
- **The two hook overlays** would lose the only versioned copy any personal overlay has.
- **`usage-audit.py`** would lose its only versioned home.
- **The parked wish** would need an owner or would be dropped.
- **`PLAYBOOK.md`** would cost the three lines that live nowhere else, and nothing beyond them, once
  those three have a home and the citations pointing at the file are repointed.

## What the window that owns `~/.claude/playbook` runs

In order. Every path is relative to `~/.claude/playbook`.

1. `git push` — the 27.08 commit has never left the machine.
2. Move `personal/profile.md.bak-pre-langsweep` to the trash, and `git rm` it.
3. `git rm` these nine, which stay recoverable from the history: `PIPELINE_UPGRADE_ROADMAP.md`,
   `claudemd_mining_s51.md`, `row52/CLAUDE.draft.md`, `row52/CLAUDE.final.md`,
   `row52/profile.draft.md`, `row52/attic/CLAUDE.md.2026-07-05`,
   `row52/attic/profile.md.2026-07-05`, `migration/2026-07-10-fleet-survey.md`, and — after one walk
   of its findings on `CLAUDE.md` and `README.md` — `inbox/2026-08-05-from-live-spec-readability-audit.md`.
4. Move `PLAYBOOK.html` and the whole `row52/attic/skills-bak/` folder to the trash. Both are
   untracked, so git has nothing to do here.
5. Rewrite `README.md` so it says what the repository holds afterwards: the boot file, the personal
   profile and its history, the migration map, the usage script, the hook overlays, and one parked
   wish. The present text names `PLAYBOOK.md` as the agreement's home and will be wrong.
6. In `personal/profile.md`, give the `cost-levers` line the script's full path,
   `~/.claude/playbook/tools/usage-audit.py`.
7. Leave `PLAYBOOK.md`, `CLAUDE.md`, `personal/profile.md`, `personal/profile-history.md`,
   `row52/migration-map.md`, `hooks/`, `tools/`, `.gitignore`, and
   `inbox/2026-07-06-spend-monitor-agent.md` where they are.
8. Commit and push.

`row52/` ends holding `migration-map.md` alone. `migration/` ends empty, and `inbox/` keeps the one
parked wish.

## What stays open

- `PLAYBOOK.md` waits on the lane that is giving every rule one home, on two counts. Three edits
  release the pointers: the citation in `skills/live-spec-base/SKILL.md` around line 237, the one in
  `skills/director/references/delegation-protocol.md` around line 36, and the assertion in
  `tests/test_convergence_rule.py` that the base rulebook names the file. Two rules in it belong in
  the pack and are in no skill today — naming what a plan must not touch, and reading "what's the
  point" as a signal to stop and look at the rendered output. Its track-coach lines want one read by
  that project's window before the file goes.
- The four personal hook overlays want a single arrangement covering all four. The move touches armed
  hooks, which this plan forbids while it runs.
