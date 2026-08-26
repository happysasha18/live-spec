# A rendered page's lifecycle — shown, read, cleared (SPEC INV-286)

Rule 5 puts the artifact where the person will actually see it. This page carries the other half of
that rule: what happens to the page once the seeing is done. It is normative — the walk rule 5 points
at, held out of the skill body only for length.

A page rendered for a person is built for one reading. Left alone it stands in the tree until someone
notices it, so a working directory carries several at any moment and the count only grows. This repo's
own root held four when the law was written, the oldest eighteen days old, one of them a render of a
document that no longer exists under that name.

## When a page is cleared

The clearing fires when the exchange the page served closes:

- the person has replied to the showing, or
- a decision page's answers have been read back and harvested (rule 10).

A release sweeps whatever escaped those moments — the publish walk runs the sweep as one of its own
steps, so a shipping version never carries an accumulated pile forward.

## Which kind of page it is — the renderer decides

A page the document renderer produced is **transient**: it was built for one reading and rebuilds from
its source in a second. Every other page in the tree is the artifact itself and stays — a hand-built
decision page, a frozen norm card, a test fixture, a prototype sketch, a project's built site.

The rule reads the renderer's own mark, `<meta name="generator" content="live-spec render-doc">`,
which `scripts/render-doc.py` stamps into every page it writes. A page rendered before that mark
existed is recognised by the second half of the same evidence: its source document standing beside it
under the same name, which is what makes a render a render.

The renderer carries the rule because it is the one thing that knows. A naming convention is a habit
that fails on one file. A directory allowlist has to be kept honest by hand, and it reads a project's
`dist/`, `site/`, and `node_modules/` as pages built for one reading, which is how a sweep eats a
shipped website. The mark is written by the act that creates the page, so it cannot drift from the
truth, and nothing else carries it.

A host declares its own homes outside the sweep's reach under `rendered_pages` in
`guardrails.config.json`. The same file carries a `reach_classes` key, which sorts directories for the
push-reach check `guardrails/check-push-reach.sh`. Both keys take the same road, so adopting the rule
means declaring directories and editing no script.

## Where a cleared page goes

Into the **attic** (base rule 10), which already holds every superseded file. Nothing is deleted. The
name it takes there follows the pack's one collision law in its two moves (SPEC E-9):
the source directory prefixes the basename, so `docs/x.html` and `notes/x.html` land apart on the
first move, and a numeric ordinal before the extension follows while the name is still taken. A page
cleared from the tree root carries no source directory and keeps its bare name. A second clearing
never overwrites the first. The page rests in the attic the way a file rests in the trash: it comes
back by being moved back.

The attic's bytes stay off the remote — a rendered page rebuilds from its source document, and
`.gitignore` keeps `*.html` out of history. The manifest is committed, so the record of what was
cleared is durable while the page itself waits on disk.

## What a clearing declares

One line names each page cleared and says the attic holds it. The same fact lands dated in
`attic/MANIFEST.md`, one line per file:

```
- `README.html` -> `attic/README.html` * a rendered page whose reading is over: carried the
  `live-spec render-doc` generator mark * 2026-07-27
```

The line records **why** the page moved, in the evidence the rule actually read, so a reader of the
manifest can tell one page's grounds from another's.

Each line is written as its page moves and flushed to disk. A run that halts partway therefore leaves
every page it already moved accounted for: the attic keeps only a basename, so the manifest line is
the page's provenance, and a batch write at the end would lose the provenance of everything moved
before the failure.

## The two machines

- `python3 scripts/sweep-rendered.py` performs the clearing and prints the declaration. `--dry-run`
  names what would move and moves nothing.
- `guardrails/check-rendered-sweep.py` reds while a transient page still stands, and the sweep clears
  the red. It runs inside the test suite rather than as its own push gate. Each push gate is keyed by
  one letter, the letters a to z are all assigned, and a check that arrived later rides the suite
  instead. A suite-riding check needs no letter of its own, and gate b already reds a push on a red
  suite. The check states its reach on its green line.

The check reads a page's mark and never the person's attention: a page rendered a minute ago reds
exactly like one that has stood for a week. The suite runs at verify and at landing, by which point
the exchange the page served has closed. A directory reached only through a symbolic link stands
outside the walk, since following links invites a cycle; a page there is never cleared and never
harmed.

## Where the reach stops

**Committed history first.** A page version control tracks stands outside the clearing. Removing it
is a commit with its own gate, which is a different act, and a sweep never performs it silently. A
page committed before this law existed therefore keeps standing; clearing it is a deletion commit
somebody makes deliberately.

**Then four homes**: git's own directory, the harness's worktrees, the host state directory
`.live-spec/` (the checkpoint law governs its files, base rule 6), and `attic/` itself, the
clearing's own destination. A host names its own under `rendered_pages.outside_reach`.

## What the attic does with what piles up

The attic is append-only and keeps what it holds for good, which is base rule 10's law and no
oversight here. Re-rendering one document and sweeping repeatedly leaves a numbered series in the
attic. Bounding or rotating the attic is a separate question about the attic itself, and it belongs
to whoever opens it.

---

The law comes from the owner's word, 2026-07-27:

> always clean up after yourself, write it into the skill, and clear the whole accumulated history of
> those files too, maybe when a version goes out; into the trash, so it can come back if it turns out
> to be needed.
