# The settings ladder

The one home for how the pack's settings resolve. It holds the four nested scopes, the
package-defaults table, and the rule that a budget moves the pace and never the standard. It sits in
the base skill's own package, beside `SKILL.md`. Open it when a setting is being resolved, proposed,
or recorded, and not before. Every rule below reads exactly as it read in the rulebook body.

How the pack behaves is a **named setting** living in one of four nested scopes, and a setting belongs to
the scope it describes. Broader values are inherited downward until a narrower scope overrides them on
the human's word. Resolution reads from the narrowest scope out — **session beats host beats personal beats
package default** (SPEC E-13):

| Scope | Home | Holds settings about |
|---|---|---|
| package defaults | the table below, in this file | the pack out of the box |
| personal profile | `~/.claude/live-spec/profile.md` | the person — follows them across every project |
| host profile | `<host>/.live-spec/profile.md` | this one project |
| session | the human's live word, held only in the conversation itself | the conversation running right now |

An override exists only as a written line in its profile file. Setting one leaves a dated journal note
in the home it governs, keeping every divergence visible (SPEC INV-14). The session scope is the one exception.
It lives only in the human's spoken word and dies with the conversation. The agent never writes it
anywhere on its own. Making it outlive the session is a promotion into the profile it describes, on
the human's word, journaled like any other override. Proactivity mode and trust are written
only on the human's word, and the agent may propose but never set them (SPEC INV-9). Profiles are re-read at the same
freshness points as skills (rule 8). A profile line the current pack does not recognize is ignored out
loud, named once in the session's next report as a visible, ordinary skip, never an error.

**The profile is found or founded at setup (SPEC B-3)**. The pack looks for the personal profile before
the founding questions resolve. It looks at founding, at adoption's orient, and at the first session on
a new machine or with a new human. Found ⇒ loaded and said aloud. Absent ⇒ an offer to create it from
`templates/profile.template.md`, which sits in the pack's own tree. The human tells about themselves and
may name sources for the pack to read and propose from. Every line lands on the human's word, and a declined proposal is dropped (INV-9
caps it: mode and trust move only on their word). A declined step runs the session on package
defaults, said aloud, and the offer returns at the next setup. A worker session never onboards
anyone, since its brief carries its setting lines (SPEC ACT-3).

The personal layer has one home, the profile. The machine-global instruction file (for example
`~/.claude/CLAUDE.md`) is a thin loader. It carries the pointer that loads the profile, plus only the
bootstrap lines that must hold before
any pack file is read. It is those bootstrap lines' one home, and the profile never restates them (SPEC E-16).

### Package defaults

| Setting | Default | A profile may say | Card |
|---|---|---|---|
| `language.docs` | English — docs, commits, code, artifacts | another docs language | visible |
| `language.chat` | mirror the human's language | pin one (e.g. Russian) | visible |
| `proactivity.mode` | ask-at-max — surface forks, wait on taste calls | max-proactive: proceed on recommendations, batch questions | visible |
| `trust` | low — human word before outward moves | raised only by the human (INV-9) | internal |
| `prover.cadence` | FULL pass before every MINOR bump; CROSS-LINK on every surface add | tighter (e.g. live-spec itself: before every push) or looser, recorded | internal |
| `worker.tiering` | router proposes the cheapest sufficient tier; senior may override, logged | fixed tier per size class (SPEC D-2) | internal |
| `checkpoints.home` | `<host>/.live-spec/checkpoints/`, gitignored | another host path | internal |
| `spec.file` | `PRODUCT_SPEC.md` — the host's product spec file; every pack guide reads "PRODUCT_SPEC.md" as this file under its recorded name | a host that adopted under its own name keeps it, recorded as one host-profile line (e.g. `spec.file: SPEC.md`); a rename may be offered together with its pointer sweep, never forced (SPEC INV-90) | internal |
| `work-kind.host-default` | none — each wish's kind is called at intake | a host with one usual kind names it as the intake default (SPEC T-16) | internal |
| `project.kind` | none — asked at founding and at adoption's orient, always the human's answer, never profile-seeded or inferred (SPEC INV-36) | the host's own kind: book · backend service · static site · fullstack app · CLI · skill pack · a custom kind through the queue; seeds project-wide defaults, never overriding an explicit line; updated on the human's word the moment the project outgrows it, journaled | visible |
| `project.layers` | none — declared at founding beside `project.kind`, naming this kind's concrete footprint categories (SPEC INV-135) | this project's own categories, one line: a codebase's frontend/backend/store, a photo site's content/rendering-engine/deployment, a campaign's message/channels/assets; the per-kind footprint-and-proof table in `ARCHITECTURE.md` is the scaffold each founding fills | internal |
| `project.proofs` | none — declared at founding beside `project.kind`, naming this kind's concrete test-ladder rungs (SPEC INV-135) | this project's own rungs, one line: tests and rendered checks, a byte-diff and an eye-walk, a register lint and the owner's review; a `project.kind` recorded with neither layers nor proofs is incomplete | internal |
| `project.design-principles` | none for a kind with no visual surface; a visual kind (e.g. frontend / fullstack app) declares its set at founding, seeded from that kind's starter table in `ARCHITECTURE.md`'s per-kind design-principles section (SPEC INV-136) | the project's own checkable design rules, one line, extended past the starter set through the queue; a visual kind recorded with none is flagged the way a kind recorded with no layers or proofs is (SPEC INV-135) | internal |
| `design-sync` | off — a host with visual components may switch it on (recorded profile line, SPEC E-18, INV-14) | on: a landing's declared components sync to the team's design project, every sync behind the human's publish gate (rule 17) | internal |
| `feedback-upstream` | off — the outbound feedback arm is silent; a host switches it on with a recorded profile line (SPEC INV-161, INV-14) | on: on a rare strong reaction the pack offers, with the human's explicit yes, to draft a private upstream note to the pack's authors into `outbox/`; never sends, delivery the human's own step | internal |
| `lanes.cap` | 3 — up to three build lanes roll at once without asking (SPEC T-18, INV-214) | a leaner plan lowers it, a richer one raises it, recorded with the plan it fits; the owner's 2026-07-06 value of three lives in his profile | internal |
| `budget.pressure` | full — every check runs at full strength; the economy ladder's rung (SPEC T-19, INV-40); a rung moves the pace and never the standard, stated under this table | lean or tight, only on the human's word (a session's word or a profile line; asked — or the default told — at a project's setup, founding or adoption, alongside `project.kind`; the agent proposes a rung when money/time pressure is named, never sets one); each rung's legal sheds and the never-bend list live in the economy-ladder section of `PRODUCT_SPEC.md` — every taken shed is named in the delivery report, and an explicit host line outlives any rung | visible |
| `far-tier.surface-cadence` | at most once every 14 days — how often the far backlog may surface itself unasked in the status report (SPEC INV-223, roadmap row 403); the report records the last surfacing in a dated marker, and a second offer inside the window is the defect the report-shape check reds | the person's own cadence, moved by his word like any default, and recorded in his profile | internal |

The Card column says what the settings card renders. A `visible` row appears on the card. An `internal` row is workshop machinery the card leaves out, reaching the reader only as a recorded host-profile line in the card's project-rules part. The card's own law lives in `PRODUCT_SPEC.md` (INV-87).

A profile file is plain markdown: one `setting: value` line per override, each with a trailing date and,
when it narrows the defaults, one line saying why. Settings not listed above may be proposed as wishes, and the
table grows through the queue like everything else.

### A budget moves the pace, and never the standard

A rung of the economy ladder sets how fast and how cheaply the work runs. The standard the work is held
to stands outside every rung. A check the method calls for runs at whatever the plan costs. A fresh
clean-context agent is raised every time the method asks for one. Four such asks are an adversarial
review, a cold reading, a release re-prove, and a deep spec-and-architecture audit. Economy is bought
from pace, from batching, and from a cheaper tier on mechanical work. It is never bought from a
dropped check. The full never-bend list this rule joins lives in the economy-ladder section of
`PRODUCT_SPEC.md` (SPEC INV-40, R220). The owner's word, 2026-08-05 at 22:52: quality never suffers,
whatever else does. At 22:12 he had named the smaller plan. He asked that a fresh worker the method
needs be raised on it all the same.

