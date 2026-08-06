# Setting a project up on the pack — the routing card

The routing referenced from `SKILL.md`'s "Setting a project up on the pack" section.

A person says one sentence: attach live-spec to this project, found a new project on live-spec, or
update live-spec here. This card turns that sentence into a walk. It finds the pack's own tree, says
what it found, and names which of the three walks this project takes. The phases themselves live in
the walks, and this card holds none of them.

Why the finding step exists: the two install routes put different things on the machine. The plugin
route places the whole pack tree under the plugin cache. `install.sh` copies the skill folders into
`~/.claude/skills/` and touches nothing else. A project set up that way has no `adopt/`, no
`templates/`, no `guardrails/`, and no `scripts/` anywhere in reach. The walks and the installers
all live outside `skills/`. A session holding only the installed skills resolves the tree before any
walk can run. This card ships inside the skill folder, which is what carries it to both
routes.

## Step zero — find the pack tree

Read these in order, one command each. The first one that answers wins.

1. **The current project root.** It carries `adopt/ADOPT.md`. Where that same tree also carries
   `install.sh` and `.claude-plugin/marketplace.json`, this is the pack's own repository: say so and
   ask before writing founding documents over it.
2. **`${CLAUDE_PLUGIN_ROOT}`.** The variable is set and the directory it names carries
   `adopt/ADOPT.md`. The harness sets this variable to a plugin's own root while that plugin runs.
3. **The plugin registry.** `~/.claude/plugins/installed_plugins.json` carries an entry keyed
   `live-spec@live-spec`, and one of that entry's `installPath` values names a directory carrying
   `adopt/ADOPT.md`. The registry is the authority on where an installed plugin sits.
4. **The plugin cache, scanned within bounds.** A directory matching
   `~/.claude/plugins/cache/*/*/*/adopt/ADOPT.md` — marketplace, plugin, version, three levels under
   `cache/`. The pack tree is that file's grandparent.
5. **A directory named `live-spec` beside the current project**, carrying `adopt/ADOPT.md`.
6. **Nothing answered.** The run stops here and starts no walk. Hand the person one action that
   supplies the tree: the two install lines from the pack's README, or a clone with its destination —
   `git clone https://github.com/happysasha18/live-spec ~/.live-spec-pack`. A machine behind a
   firewall reaches this read with no way forward. The exit is stated here for that reason.

**Where the clone goes, and which ref.** `~/.live-spec-pack` by default, or the path the person
names. The ref is the tag matching the installed skills' version, which every SKILL.md carries in its
frontmatter under `metadata.version`. Where no such tag exists, take the default branch and say both
version numbers aloud. Offer the chosen path for the person's own profile as a `pack.tree` line, so a
later run reuses it. That line is a note the person keeps for now. The settings ladder in
`live-spec-base` carries no `pack.tree` row yet, so nothing reads it on its own. Making it a
recognised setting is a change of its own. A clone into a temporary directory becomes a recorded path
that is gone by the next session.

**Say what was found before moving.** One line, spoken before anything else happens: which read
answered, the path it gave, and that tree's `VERSION`. The walk then carries that line into its own
record under `.live-spec/`, the read's number beside the path. A later catch-up run reads it to tell
a plugin-resolved tree from a cloned one, and resolves again. On a fresh project that directory does not
exist yet, and the walk creates it at the phase that writes the record.

**Where the versions disagree.** The resolved tree carries a `VERSION` file and the installed skills
carry their own version line. Where the two differ, say both numbers aloud and offer to re-run that
tree's `install.sh` before the walk continues.

## Which walk this project takes

Read the project tree, then take the first line that fits.

| What the tree holds | The walk | Where it lives |
|---|---|---|
| code, documents, or history a person made | attaching an existing project | `adopt/ADOPT.md` |
| nothing yet, or an empty directory | founding a new project | `adopt/START.md` |
| a `.live-spec/` record from an earlier setup | catching up with the current pack | `MIGRATION.md` |

A tree carrying a `.live-spec/` record takes the catch-up walk whatever else it holds. That project
is on the pack already, and its question is which pack version it stands at.

The setup walk finishes before any wish is worked. When it is done, the first wish enters at the
ordinary door, like every other request.
