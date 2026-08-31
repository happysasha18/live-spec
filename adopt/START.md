# Start — founding a new project on live-spec

How to set a project up on live-spec when the project is new. A new project is an empty directory,
or one holding nothing a person has written yet. This walk is the executable projection of
PRODUCT_SPEC.md's founding requirements (B-1, B-2, B-3), and of Requirement 308 for the spoken
sentence that reaches it. Follow the phases in order; each states when it is done.

**Routing.** This walk is for a fresh tree. A project that already carries code, documents, or a
history someone wrote goes to [adopt/ADOPT.md](ADOPT.md), the attach walk. A project already on the
pack, coming up to a newer version, goes to [MIGRATION.md](../MIGRATION.md), the catch-up walk. The
routing card at `skills/build-pipeline/references/project-setup.md` reads the tree and picks among
the three. It resolves the pack's own tree first, which every command below needs.

**A second run is safe.** Every phase reads its precondition from the tree. What the tree already
holds is reported done and skipped. No phase of this walk overwrites a file it did not create in
this run. A document standing with its template placeholders still in it is named to the person, and
replaced only on their word.

**Where `<pack>` appears below,** it means the pack tree the routing card resolved. That is the
directory holding `adopt/`, `templates/`, and `scripts/`. Every command runs from the new project's
own root.

---

## Phase 0 — version control first

Phase 0 of [adopt/ADOPT.md](ADOPT.md) states the version-control gate. It covers the repository, the
ignore file, the files-as-found commit that `<pack>/adopt/record-starting-state.sh` makes, and the
remote settled or declined on the record. A founding runs it as written there, in the same order and
for the same reason: a gate cannot protect files older than itself. A fresh tree has nothing to
preserve yet, so that commit stands for the empty start, which the script writes on its own.

Record what this run has closed at `.live-spec/adopt/found.md`, one line per phase with the date, so
a second run resumes where this one stopped.

Done when the tree is a git repository with one commit of its files as found, and the remote outcome
is on the record.

---

## Phase 1 — who is being worked for, and the founding questions

Phase 1 of [adopt/ADOPT.md](ADOPT.md) states this phase whole. The personal profile is read or
offered first. Then the founding questions are asked or read from that profile, then the skill
search, then the economy rung. A founding runs it as written there. One thing differs: a fresh tree
carries no document to read, so the digest that phase produces closes empty.

Done when every question in `<pack>/scripts/founding-questions.json` is answered or read from the
personal profile, and the economy rung is settled.

---

## Phase 2 — the templates land

The table below is the one statement of what lands where. A destination that already stands is
reported done and skipped.

| Template | Lands as | When |
|---|---|---|
| `PRODUCT_SPEC.template.md` | `PRODUCT_SPEC.md` | always |
| `ARCHITECTURE.template.md` | `ARCHITECTURE.md` | always |
| `TEST_MATRIX.template.md` | `TEST_MATRIX.md` | always |
| `ROADMAP.template.md` | `ROADMAP.md` | always |
| `JOURNAL.template.md` | `JOURNAL.md` | always |
| `NEXT_STEPS.template.md` | `NEXT_STEPS.md` | always |
| `test_scaffold.template.py` | `tests/test_scaffold.py` | always |
| `agent.template.md` | `.live-spec/agent.md` | always |
| `DECISIONS.template.md` | `DECISIONS.md` | on the founding's word |
| `PROBLEMS.template.md` | `PROBLEMS.md` | on the founding's word |
| `KILL_LIST.template.md` | `KILL_LIST.md` | on the founding's word |

Eleven rows in all: eight land on every founding, and three wait on the person's word. Each source
file stands under `<pack>/templates/`. A source the resolved tree does not carry stops the phase,
named by its filename, before anything is written.

**What gets filled, and what stays.** Each landed document's first line takes this project's name
and the day the founding runs. Those replace the template's name placeholder and its date
placeholder. Every other placeholder stays exactly as the template wrote it. A founding fills what
it knows and guesses nothing. The rest is answered later, at the step that owns the answer.

**The host profile is written here, and no template is its source.** `.live-spec/profile.md` carries
this project's own lines alone. Every setting about the person lives in their personal profile, and
none of them is written into this file. Those are the language they read, how they are addressed,
how much the session proposes on its own, and the trust they have granted.

The host lines come from `<pack>/scripts/founding-questions.json`. Each question whose `key` names
no path becomes one line. A question whose `key` names a path is answered by that file standing on
disk. Two further lines land beside them, both named by Phase 1 of [adopt/ADOPT.md](ADOPT.md). They
are `budget.pressure`, the economy rung, and `founding.set-version`, the version of the question set
this founding answered. Where the kind of project makes a question inapplicable, its line reads
`none` with the reason beside it, so every key is accounted for.

Done when every unconditional row stands on disk and the host profile carries one line for every key.

---

## Phase 3 — the first green

Run `python3 -m unittest discover tests` from the project root. `tests/test_scaffold.py`, which
landed in Phase 2, is the judge. That file states in its own words what it holds the founding to.
This walk names no check of its own. The scaffold is the shipped artifact, and a list written here
would go stale the next time that file moves.

Done when the scaffold suite exits zero. That green is the starting floor the first delivery builds
on, and the first delivery ships its own first real test beside it.

---

## Phase 4 — the gates, then the surface registry

Run the three installers from the resolved pack tree, in the order the section "Installing the
gates" in [adopt/ADOPT.md](ADOPT.md) gives. Follow the manual steps that section lists. They put the
project-side checks, the ratchet gates, and the machine's own hooks in place.

The first of those installers, `<pack>/adopt/install-scaffold.sh`, seeds `guardrails.config.json`
where the project carries none. Once that config exists, create the surface registry at the path the
config gives as its `registry_path` value. The registry starts as an empty document under its own
header. This order matters: the config names the file, so a registry made before the config exists
is made under a name nothing has stated yet. This walk states no filename for it.

Done when each installer has run, its manual steps are followed, and the registry stands at the path
the config names.

---

## Phase 5 — the record, and the first wish

Phase 6 of [adopt/ADOPT.md](ADOPT.md) states the record and the journal entry. That record holds the
installed skill versions under `.live-spec/`, the host profile, and the run's own dated entry. A
founding writes them as that phase says, and the record names the pack version that founded this
project.

Then seed `NEXT_STEPS.md` with the first wish, or with one sentence saying that none is queued yet.
Render the settings card with `<pack>/scripts/onboarding-card.py` for the person to read. It is one
page showing what is set up and what is theirs to change.

Done when the record names the pack version that founded this project, and the first wish enters at
the ordinary door.
