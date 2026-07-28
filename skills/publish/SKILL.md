---
name: publish
description: The publish-quality gate — run it whenever work is about to leave the machine: a repo going public, a push that updates a public README, a release, a plugin-directory submission, a skill deposited for others, rendered cards sent to a design project. It checks that the publication owes its reader what the artifact's KIND owes (a skill shows install + commands + when-to-use; a tool shows real runs; a visual product shows fresh screenshots; prose shows its reading path), lets each publish TARGET plug its own steps into the walk, and always finishes BEFORE the human's publish gate, standing only as its preparation. NOT for in-session showing of work (communicator owns that) or for commits that stay local.
metadata:
  version: 4.3.0
---

# publish — the work leaves the machine looking like a product

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v4.3.0), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

A deposit outward is a SURFACE: the reader meets the README, the release notes, the directory card. The commit history stays behind them. This skill is the
checklist that surface must pass, keyed by the artifact's work-kind (SPEC T-16, E-20), plus the point
where a publish target adds its own steps. It runs BEFORE
the human's publish gate (base rules 12/17) and before any push gate the host holds — what the human
approves has already earned approval. It never sends anything itself.

## When it fires

Anything crossing the machine's edge: first public push of a repo · a push that changes what a public
reader sees (README, docs, screenshots) · any push that ships a new version (the shopfront walk below)
· a release/tag · a plugin-directory or marketplace submission
· a skill shipped for someone else's machine · design-project sync cards (SPEC E-18). If no reader
outside this machine will meet the artifact, this skill stands down: showing work to your OWN human
in-session belongs to communicator's rule 5. That in-session exchange is not a publication.

**A version push always fires the shopfront walk (SPEC INV-44).** Shipping a new version changes the
truth a public reader will read tomorrow even when the diff never touched a doc — so at every such
push, walk the shopfront in one look: the README's CLAIMS (behaviour, counts, commands, version homes)
still match the pushed truth, and the kind-owed visuals ride along — a skill pack re-checks its
diagrams and flow pictures, a visual product re-shoots what changed on screen, a tool re-runs its
example. The delivery report carries the outcome in one line — "shopfront checked — current" when
nothing was touched; a stale claim found is fixed BEFORE the push, the same law as a stale screenshot.

**The same walk sweeps the rendered pages that accumulated (SPEC INV-286).** A page rendered for one
reading is cleared as its exchange closes (communicator rule 5), and a release is where whatever
escaped that moment gets swept: run `python3 scripts/sweep-rendered.py`, which moves each transient
page into the attic with its dated manifest line and prints what it moved. The delivery report carries
that line, so the release says which pages were cleared and where they come back from. A page inside a
record home is a source artifact and the sweep leaves it standing.

## The kind checklist — what every publication owes (one home: this table)

First, the floor every kind shares.

The README/landing surface answers, in its first screen, WHAT this is, WHO it serves, and HOW to start
— in the reader's language, keeping the repo's internal vocabulary out (base rule 2). Every claim on it
is TRUE of the shipped version today; a stale claim or picture is a false claim. The README carries a
Known issues section while real known problems exist: each issue stated honestly with its fix status,
the list re-read at every push and a resolved issue removed the push it ships (his word 2026-07-10). The
license/attribution state is explicit.

An artifact built with the pack carries the standard attribution line "made with live-spec" on its
landing surface, the name linking to the pack repo and trailing the pack version the project runs
(github.com/happysasha18/live-spec — in markdown:
`made with [live-spec](https://github.com/happysasha18/live-spec) v<pack-version>`, the version read
from the host's attach record at write time and refreshed at catch-ups, so adoption is trackable from
the shopfronts themselves), in the README's footer and for a skill also in its SKILL.md.
The line is an offer, never a gate: the walk says once when it is absent and proposes it, the owner's
word decides, a declined offer is closed and never re-asked (SPEC INV-96, base rule on answered questions; each
built-with project applies the line through its own queue).

NOTHING secret or unshareable leaves: the tree AND history swept for secrets, tokens, personal paths
and data, and every bundled fixture or sample checked shareable (no copyrighted material we may not
republish). (The sweep items entered from the first eval run, 2026-07-05: the no-skill baseline agent
caught them and the skill's checklist did not — an eval measures the skill against that baseline in both
directions.)

Shipped docs speak impersonally. Every requirement in the spec, matrix, README, or skill card reads as
the rule, the actor as a role (the user, the producer, the target user), and the reason. The rationale
stays, the personal name drops, and a dated decision keeps the date as a plain anchor while the name
comes off; personal attribution and candid process voice stay in the local-only diaries (JOURNAL,
NEXT_STEPS), which no publish ships (SPEC INV-118). The publish walk reads the shipped docs for a stray
personal name before the deposit leaves. The mechanical enforcement — a lint that reports each offending
file:line, red-proven on a fixture — lands with the shipped-artifact language gate (roadmap row 275),
and this floor states the duty the lint holds. The shipped tree carries no untranslated owner-language
and no personal attribution of a requirement. The machine that holds this is
`guardrails/check-shipped-language.sh`, run over the shipped set, reporting each offence as file:line,
its deliberate program-data and authorship bylines spared by a dated allowlist (SPEC INV-120).

| Kind (SPEC T-16) | The publication additionally owes |
|---|---|
| skill | install line(s) that actually run · the commands/invocations, shown as they're typed · when to USE it and when NOT (both, verbatim from the skill's own boundaries) · a one-scenario taste of it working (its eval scenario is the honest source, SPEC E-19) |
| infra / tool | at least one REAL run: the command and its real output, current version · requirements/platform stated · failure behaviour named (what the user sees when input is wrong) |
| product (visual) | FRESH screenshots of the shipped version — re-shot at every publish that changes what they show, never reused stale · a start-to-value walkthrough (open → first result) |
| prose | the reading path (what to read first, how long it takes) · who it's for stated up front |

Comparisons and diagrams JOIN when they carry the argument: a comparison table against the honest
alternatives, a diagram where structure shows what words cannot. They never ride as decoration; an
empty comparison ("we're better at everything") is worse than none.

## When the package is a generalized engine (SPEC INV-119)

An engine — a reusable core lifted out of one live product, the instance it grew inside — published as a generic package owes its reader a spec that reads generic, so the walk adds two leak checks before the package leaves the machine. The convention the walk holds the spec to is spec-author's own: a reconciliation log headed "how each behaviour landed in code", each entry citing the engine's own public commit ("landed in engine commit `<hash>`"), opened by one sentence naming the normal intake path — a feature proven first on a live instance, then generalized [SPEC INV-119]. The check fires only when the package is a generalized engine (its queue row carries the engine kind or the pair-split [INV-85]); a single-instance product owes it nothing.

- **No foreign provenance.** Every commit hash the spec cites as provenance resolves in the engine's OWN public history (`git cat-file -e <hash>` in the engine repo); a hash that fails to resolve is an instance's private commit riding along, and the fork-diff framing that carries it ("Deltas from the <instance> reference implementation") is rewritten to the reconciliation-log framing with the engine's own commit [INV-119]. This part is mechanically reliable: the hash either resolves in the engine's history or it does not, and the fork-diff heading is a fixed phrase.
- **No instance label as a mechanism name.** A mechanism is named by a neutral internal term; a locale-specific instance label appears only inside a span marked as instance-supplied copy. A non-Latin token standing in a heading or a mechanism name is a tripwire the walk flags (kin to the shipped-artifact language lint, row 275). Whether a Latin-script instance label is being used as the mechanism's name is an advisory read — the walk surfaces the candidate and the author confirms.

## Targets are plugins — each embeds its steps

The walk above is the shared base; the TARGET adds its own steps and never removes the kind's owed minimum
(SPEC E-20):

- **GitHub repo** — README current at the root · screenshots re-shot where the host's rule says so ·
  release notes for a tagged release, whose shape carries an OPTIONAL offers section — appealing next
  steps the reader may take, phrased as choices he is free to take on his own clock (the release note is
  a surface he opens himself, so an offer rides it, SPEC INV-228, INV-205). The section is optional, so
  a release with no worthwhile next step owes none; what the walk owes is a RECORDED offer-or-none
  decision, so the choice is never silently skipped: the walk offers a next step in a
  `<!-- release-note:offers -->` region or records `<!-- release-note:no-offer -->` for a release that
  has none, and `guardrails/check-release-note.py` reds a note leaving the decision unrecorded (it rides
  the suite; the note is a process artifact with no committed file for a push gate to scan). ·
  repo description + topics set · third-party dependency licenses
  compatible with the release · the name checked for collisions where it matters (GitHub/PyPI/npm) ·
  a fresh-clone check — install and run from scratch as an outside reader would; do not assume it
  "works on my machine" · the push gate of the host ALWAYS holds (a publish never turns into a push authorization).
- **Plugin directory / marketplace** — the manifest complete and validated · the directory's forms
  answered · the listing text reads as the directory's reader expects, in the directory's own register; repo prose does not fit a directory listing.
- **Design project (claude.ai/design)** — the landing's DECLARED components as rendered cards, through
  the human's gate; the in-session render stays the authority (SPEC E-18).
- A new target = a new plugin section here, added through the queue like any wish.

## How it runs

1. Name the artifact's kind (it usually already stands in the queue row, SPEC T-16) and the target(s).
2. Walk the floor, then the kind's row, then each target's steps — fixing what fails BEFORE asking the
   human anything.
3. Report the walk's result in the delivery report (a stood-down publish step is named like any other,
   SPEC INV-22), then hand the human their gate with the surface ALREADY worth approving: "the README
   is current, screenshots re-shot today, forms filled — push?"

## One worked example (a skill's README, before and after the walk)

❌ *"track-coach — a compositional analysis pipeline. See `build_widget.py` for entry points; config
in the usual place. v1.4 adds INV-50 scale wording."* — fails the floor (WHAT/WHO/HOW absent, internal
vocabulary, a version claim in prose) and the skill row (no install line, no typed commands, no
when-NOT, no taste of it working).

✅ *"track-coach — a coach for music producers: point it at a track (mp3/wav/…) and an Ableton
project, get one offline page that shows where the arrangement is alive and where it stalls. Install:
`./install.sh`. Use: say 'analyse my track' with the file — deep mode runs itself. Not for mastering
metrics or loudness compliance. Below: one real read of a real track."* — the first screen answers
what/who/how in the reader's words, the commands are shown as typed, both boundary sides are stated,
and the taste comes from a real run that shows the product working.

## Work that belongs elsewhere

Reserve it for work leaving the machine: skip it for showing work in-session (communicator rule 5), for local commits, and for a prototype —
a sketch is never published, it isn't a product (base rule 16); not as a substitute for the human's
publish gate — this skill prepares the deposit, the human releases it.
