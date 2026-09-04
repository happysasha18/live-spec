# Host profile — live-spec itself

Overrides for this repo only; they beat the personal profile and the package defaults (settings ladder,
SPEC E-13). Every line here is a recorded override, never a silent divergence (SPEC INV-14).

- `show.default: the reply itself — no browser window opens unless the person asks for one` — his
  word, 2026-09-04 02:01: the status list in the reply replaced what he used to open a page to read,
  and a window opening on its own now interrupts him. A rendered page is made when he asks for it by
  name, and never as the default way to answer a long question. This overrides the personal profile's
  own show line for this repo.

- `prover.cadence: a re-check before EVERY push, record in docs/prover/ — rigor whole, FORM scaled by the delta (SPEC INV-61): small deltas ride the three-line short form, surface/structural deltas the full walk` — this repo is
  public and the method's own flagship; tightened from the package default (before MINOR bumps) on
  Alexander's explicit word, 2026-07-04. This line and the push gate [M-6] are one fact; M-6 is its
  normative home, and M-6 names the one carve-out: a push whose diff is exactly one new inbox/ file
  (the remote deposit, SPEC INV-112) owes the fence and no re-check record.

- `project.kind: skill pack — the live-spec method itself; this repo doubles as the flagship host
  instance` — recorded 2026-07-06 at the INV-36 landing, the law's own founding-ask applied to its
  birthplace; updated on Alexander's word if the pack outgrows it (SPEC INV-36).

- `founding.set-version: 6` — the version of the founding-question set this tree answered; the pack is
  its own first host and is current on the set, carrying every question that applies to it:
  personal-versus-reusable and the kind (INV-36), the layers and proofs (INV-135), the agent card
  at `.live-spec/agent.md` (E-32), and the composition-axes question (INV-244, answered "none beyond
  the C-1 floor" on the `project.axes` line below), and the configuration-surface question (INV-291,
  answered "none — nothing of this project is deployed" on the `project.config-surface` line below);
  the design-principles question (INV-136) enters the
  set but binds a visual kind, which a skill pack is not, so it applies to no answer here. The set's
  machine home is `scripts/founding-questions.json`, and the update check's founding arm names any
  question added past this version (SPEC INV-227, recorded 2026-07-18 at the INV-227 landing).

- `project.layers: the rulebook and spec · the working skills · the guardrails, templates, and suite` —
  the concrete fill of the three abstract footprint categories for a skill pack: a presentation-only
  change touches one shipped doc or skill surface, a single-module change stays inside one skill or one
  guardrail, a cross-cutting change moves a shared rule or law across skills (SPEC INV-135, recorded at
  the INV-135 landing 2026-07-12).

- `project.proofs: the pytest suite (string and render assertions against the shipped files) · deed
  proofs driving the real engine a law names · the docs/prover records · the owner's read` — the
  concrete fill of the test ladder's rungs for a text product. The pack's rendered level is a string
  assertion against the shipped file (SPEC INV-135, recorded 2026-07-12). **Grown 2026-07-17, the lanes
  landing:** the engine rung is occupied. That day the pack stated its first laws whose truth lives in
  an external engine's runtime behaviour rather than in its own text — what git refuses to a second
  worktree, what a rebase does on a conflict, what a teardown does to a dirty tree — and no string
  assertion against a shipped file can see any of it. Such a law is proven by deed, driving a real
  process in a temp tree under the suite's own prefix (INV-100) with the machine's own git config
  switched off (INV-155), and the deed's red-proof is a mutation removing the subject it observes.
  The rung's own boundary is a fact too: the deed proves what the engine does at the version and
  defaults it ran under, and a law reading wider than its engine is the finding (the lanes landing pinned
  both the guarantee and its boundary for exactly that reason).

- `project.axes: none beyond the C-1 floor` — the composition axes this kind owes every surface
  past the kind-independent floor, an explicit stated decision that a skill pack owes none, the empty
  case the design-principles set already legitimises for a kind with no visitor-facing surface (SPEC
  INV-244, recorded at the INV-244 landing). The founding check reds a kind recorded with no such
  line at all and passes on this explicit "none"; the per-kind axis-set table in ARCHITECTURE.md is
  the scaffold each founding fills.

- `project.config-surface: none — nothing of this project is deployed` — the seam a deployed kind
  declares between what ships inside a build and what its owner turns from outside one (SPEC INV-291,
  recorded at the INV-291 landing 2026-07-27). This product is the text a session reads: it runs in
  no place the pack's authors deploy to, so no value of it reaches a reader except through a release
  the reader takes. The explicit "none" is the stated decision the check passes on, the same shape as
  the `project.axes` answer above; a kind recorded with no such line at all reds, and a "none" written
  beside a `project.layers` line that names a deployment layer reds as two declarations that disagree.
  The per-kind design-principles table in ARCHITECTURE.md is the scaffold a founding fills from.

- `other-projects: audit-only — when Alexander speaks about another project in this window, it is a
  case study for improving the pack, never a task in that project; this window never intervenes
  actively there — no fixes, no managing, not even an inbox wish (narrower than the pack-wide inbox
  exception, base rule 7); reading for audit is legal, the response is always a pack improvement` —
  Alexander's explicit word 2026-07-06 ~21:50, after this window filed an inbox wish to the gallery
  project that its own session was already handling ("тлвфото сам справится, не надо его тут
  менеджить… это только аудит").


- `trust.push-grant: standing — accepted work pushes to origin main by rule on the agent's own
  certification (every gate the diff reaches ran and passed, the verdict read from the suite log's own
  line; the prover re-check before every push stays; version-milestone releases he reserved by name
  still wait for his word)` — recorded 2026-07-10 ~09:16, Alexander's explicit word this morning
  («сам пуши! не надо меня ждать»); this answers the push-law grant question (SPEC INV-82) for this host.

- `trust.github-grant: standing — the Claude environment is linked to Alexander's GitHub account (his
  one-time click), and this repo is granted to the app, so a remote seat's inbox deposit may push here
  under the remote arm (SPEC INV-112)` — recorded 2026-07-10, the account link and repo grant done that
  day; a seat that ever finds this line absent for a repo runs the grant ask (scripts/grant-ask.md) rather
  than failing silently.

- Amendment to `other-projects` (named, dated): for the tlvphoto pair migration Alexander set on
  2026-07-10 ~02:09, this window teaches and supervises — prepares briefs he hands over, reviews
  artifacts, directs — and still never writes their trees; the audit-only line above keeps standing
  for everything else. Recorded 2026-07-10 ~09:19 from his word of that night.

- `hosts.watch: ~/tlvphotos ~/exhibition-engine ~/promoter ~/promoter-alexander ~/tc-cloud-validate` —
  the projects this repository's own probe checks for a stale copy of the pack (the drift warning in
  `scripts/state-probe.sh`'s ALARM section). The five paths stood written into that script until
  2026-09-03, when plan-14 made the status view installable and the script had to stop carrying one
  machine's list of neighbours. They are recorded here because the watch is this repository's own job
  as the pack's home: a project that merely installs the status view watches nobody and needs no such
  line. A path this machine does not carry is passed over in silence.
