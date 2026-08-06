# Prover record — the spoken setup entry, 2026-08-06

The design under review: `scratchpad/design-A-attach.md`, the two spoken setup entries. The review is
`scratchpad/prove-A-attach.md`. The reworked design that landed is `scratchpad/design-A2-attach.md`.
The landed requirement is Requirement 308 (INV-307), matrix rows M-512 through M-518, and queue row
557.

## The verdict

Rework, then build. Ten must-fix findings, five should-fix. The review's two load-bearing arguments
held under verification — the skill count and the install route — so the home stayed the same home
and every repair sat inside the frame the first design drew. The first design was wrong twice
because it reasoned from documents; the reworked design states the file that settled each fact.

## The ten must-fix findings and their fate

| Finding | Fate |
|---|---|
| F1 — the plugin route reads one level too shallow | Answered. The resolution list is rewritten against this machine's real layout: `installed_plugins.json` is the authority, `CLAUDE_PLUGIN_ROOT` comes first, and a bounded cache scan is the fallback. |
| F2 — the trigger case asserts characters and calls it a load | Answered. The case splits into a presence floor in the suite and a triggering arm in the eval, scoring the load per named phrase. |
| F3 — one phrase contests with spec-author | Answered. The arm leads on the setup act and carries "found a new project on live-spec"; spec-author's description gains a hand-off clause with its own criterion. |
| F4 — a second run overwrites documents already being filled | Answered. Every phase reads its precondition from the tree, a destination that stands is reported done and skipped, and the fixture run proves it by deed. |
| F5 — the host profile is seeded from the personal-profile template | Answered. No template is copied. The host profile is written from `scripts/founding-questions.json`, one line per key that names no path. |
| F6 — a retired four-checks fact would be copied into new artifacts | Answered. The walk names no check list of its own and points at the shipped scaffold, and the stale spec sentence is repaired in this landing. |
| F7 — the surface registry is named two ways and created too early | Answered in part. Registry creation moves after the config exists and takes that config's registry path. The two-name drift is parked as queue row 560, on the owner's word. |
| F8 — three phases restate homes that live in `adopt/ADOPT.md` | Answered. Those phases become one-line pointers naming ADOPT.md's headings, and the one-home sweep grows to cover them. |
| F9 — the card names three walks and the closed set gains two rows | Answered. The request-kind table gains three rows, and the catch-up phrasings join the arm and the scored phrase list. |
| F10 — nothing in the acceptance set proves either walk runs | Answered. Case F is a founding executed on a throwaway tree, built and run before the reworked design was written, with three reds proven. |

## The five should-fix findings and their fate

- **F12 — the installer paragraphs have no addressable target.** Answered. `adopt/ADOPT.md` gains an
  "Installing the gates" heading above those paragraphs, and both new documents cite it by text. The
  knock-on is the pin move recorded below.
- **F13 — three criteria carried clauses no test can assert.** Answered. Each now states a measurable
  rule: a forty-character proximity over six named words, a heading pattern with a list-length bound,
  and two heading strings that must be absent beside a path that must be present.
- **F14 — one criterion's negative was anchored on a single wording.** Answered. The criterion now
  asserts the positive, the negative, and the survival of the existing pinned string.
- **F15 — the rationale claimed a banner no skill carries.** Answered. The sentence names the two real
  homes, confirmed by a read of all eleven skill banners. The argument's conclusion is unchanged.
- **F16 — the founding's stalls were silent.** Answered. Step zero says one line before it moves, and
  the record carries the read's number beside the path.

## Two things recorded, with their reasons

- The build-pipeline description field becomes the longest in the pack at 477 characters, against a
  shipped range of 122 to 383 over eleven fields. No gate caps the field. The eval is where the cost
  would show, and it re-scores after any later growth.
- `tests/fixtures/specformat/good_corpus_section.md` carries a copy of the spec sentence this landing
  repairs. It is a format fixture whose job is the shape of a well-formed section, and the format
  tests compare against its own bytes, so the live spec's wording never reaches it. It is left
  standing, and this paragraph is its record.

## The pin correction this record owes

The design predicted that the attach record pin in `ARCHITECTURE.md` would move from line 283 to line
285. The builder measured the landed file and reported 289. Four other pins into `adopt/ADOPT.md`
moved as well, which the design said would stand: the version-control gate from 44 to 47, the orient
phase from 85 to 88, the unbacked surface from 196 to 199, and the attic from 207 to 210. All five
were read off the landed `adopt/ADOPT.md` before the architecture was written, and all five match.

## Reach

Read directly: `scratchpad/design-A-attach.md`, `scratchpad/prove-A-attach.md`,
`scratchpad/design-A2-attach.md` sections 0 through 10, `adopt/ADOPT.md` at the five pinned lines,
`adopt/START.md`, `skills/build-pipeline/references/project-setup.md`, `tests/test_setup_entry.py`,
and `docs/skill-review/2026-08-06-setup-entry.md`.
