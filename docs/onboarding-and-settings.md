# Onboarding and settings

Every way the pack behaves for a person or a project is a named setting. This page explains where
those settings live, how they resolve when scopes disagree, what goes into each profile, and which
session hooks enforce the standing habits. The normative home for the ladder and the default values
is the base skill (`skills/live-spec-base/SKILL.md`); this page explains and points. [E-13]

## The settings ladder

Settings live in four nested scopes. Each setting belongs to the scope it describes. Broader values
are inherited down until a narrower scope overrides them on the human's word, and resolution reads
from the narrowest scope out: session beats host beats personal beats package default. [E-13]

| Scope | Home | Holds settings about |
|---|---|---|
| package defaults | the defaults table in `skills/live-spec-base/SKILL.md` | the pack out of the box |
| personal profile | `~/.claude/live-spec/profile.md` | the human, across every project |
| host profile | `<host>/.live-spec/profile.md` | this one project |
| session | the human's live word in the conversation | right now, one conversation |

An override exists only as a written line in its profile file, and writing one leaves a dated
journal note in the home it governs, so every divergence stays visible. [INV-14]

The session scope is the one exception to the written-line rule. It lives in the human's spoken
word and dies with the conversation. The agent never writes it down on its own; making a session
line outlive the session is a promotion into the profile it describes, done on the human's word and
journaled like any other override. Proactivity mode and trust move only on the human's word — the
agent may propose a level, and the human sets it. [INV-9]

Profiles are re-read at the same freshness points as skills: re-stat at every safe breakpoint, and
re-read any file whose version changed before continuing. [A-7]

## The personal profile

The personal profile holds the lines about the human, and it follows the human across every
project. The template is `templates/profile.template.md`. Its sections cover:

- **the contract** — `language.docs` and `language.chat`, how to address the human,
  `proactivity.mode` (ask-at-max or max-proactive), and the trust level;
- **about the human** — their background and domain vocabulary, in their own dated words;
- **working habits** — one habit per line (how to show work, resume habits, reporting style),
  each with the human's word and its date.

Every line lands on the human's word: told directly, or proposed from a source the human named and
accepted one line at a time. A declined proposal is dropped.

The profile is found or founded at setup. At founding, at adoption's orient, and at the first
session on a new machine or with a new human, the pack looks for the profile before the founding
questions resolve. A found profile is loaded and said aloud. An absent one triggers an offer to
create it from the template. A declined offer runs the session on package defaults, said aloud, and
the offer returns at the next setup. A worker session never onboards anyone; its brief carries its
setting lines verbatim. [B-3, ACT-3]

The personal layer has one home, and it is this profile. The machine-global instruction file
(`~/.claude/CLAUDE.md` on this stack) stays a thin loader: a pointer to the profile plus only the
bootstrap lines that must hold before any pack file is read. [E-16]

## The host profile

The host profile at `<host>/.live-spec/profile.md` narrows the broader scopes for one project. It
is created at attach and lives git-tracked in the host repo; inside `.live-spec/`, only the
checkpoints stay gitignored. [E-8, A-8]

Typical host lines:

- `project.kind` — book, backend service, static site, fullstack app, CLI, skill pack, or a custom
  kind. It is always the human's answer at founding or at adoption's orient; a personal-profile
  line can never say what a host is. It seeds project-wide defaults and never overrides an
  explicit host line. [INV-36]
- `work-kind.host-default` — a host with one usual work-kind (product, infra, skill, prose) may
  record it as the intake default. [T-16]
- `budget.pressure` — the economy rung (full, lean, or tight), written only on the human's word. [T-19]
- `prover.cadence` — a tighter or looser prover rhythm than the package default, recorded.
- `design-sync` — off by default; a host with visual components may switch it on with a recorded
  line. [E-18]
- the push remote — discovered from the tree first; a host with no remote gets one contextual
  question at the first push moment, and the named choice is recorded here. [INV-82]

## Unknown profile lines

A profile line the current pack does not recognize is ignored aloud. The pack writes a dated note
in the host's journal and names the skip once in the session's next report, as a visible, ordinary
skip. The journal half is durable, so a session that dies before its report still leaves the
trace. This makes new lines safe to add under an older pack. [E-13]

## Session hooks

`guardrails/judge-hooks.json` declares every session hook the pack ships — eight today, each with
the event it rides, its command form, and the shipped files it reads. Two are wired live: the wall
clock and the chat laws. The other six are opt-in from 2026-08-17: the register judge's two arms and
the four literal Stop scans. The declaration records the surface each rides, for a host that turns one
on. The one installer a human runs is `scripts/install-session-hooks.sh`. It generates the two wired
hooks from that declaration, then chains to `scripts/install-pack-hooks.sh`, which places the other six
files and wires none. So the one command puts every shipped file in place. The human runs it by hand, because the harness deliberately blocks the agent from
editing its own configuration. Re-running it changes nothing — a hook already wired, in any form, is
left exactly as it stands, and a personal overlay file (`*-personal.json`/`*-personal.md`, or a host's
own `hook-meter.py` counter) already on the machine is only ever reported, never touched.

- `hooks/clock-hook.sh` injects the machine's wall clock into every prompt's context, so the
  reply's leading time stamp reads off the clock, no longer continued by hand. [INV-24]
- `hooks/chat-law-hook.sh` reminds every window of the chat laws: plain product words do the
  talking, internal codes only trail in parentheses, and long silence owes a narration line. The
  skills stay the laws' normative homes; the hook only reminds. [INV-28, INV-35]
- The other six — the register judge (its async collect/report arms and their shared mechanism) and
  the scissors/hedge/affirmation/code-anchor Stop scans — are documented in full at
  `scripts/install-pack-hooks.sh`'s own header.

## Planned

An interactive first-run onboarding flow, which shows a new project's human what they can
customize, is designed at mockup stage only and awaits the owner's verdict
(`docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md`).
