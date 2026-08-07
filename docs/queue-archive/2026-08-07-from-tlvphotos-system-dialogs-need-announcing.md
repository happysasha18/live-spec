# A session raises system dialogs the owner answers with Deny, and nothing in the pack forbids it

**From:** the tlvphotos window, 2026-08-07 ~01:35. One habit worth a pack rule. Nothing in the
live-spec tree was changed; this file is the only thing written here.

**Harvested 2026-08-07 into ROADMAP row 581.** The message named its birth in the `Lived:` block
below, set inside a fence because that is how `inbox/README.md` prints the template; the
earned-message gate reads past every fence and so reported the message unearned. It was taken in on
its substance, the way the 2026-07-28 deposit was, and the gate's disagreement with its own home is
ROADMAP row 585.

```
Lived: Twice in one session I ran something that raised a macOS keychain dialog on Alexander's screen.
       He interrupted the work both times to ask what was happening, and told me he always presses
       Deny. What ran: (1) `scripts/deploy-lab.sh`, which reads a Cloudflare key with
       `security find-generic-password`; (2) four launches of a Chrome binary that had never run on
       this machine, each asking the keychain for Chrome's Safe Storage item. How it showed: his two
       messages, "I keep receiving these allow/deny dialogs" and "why these dialogs AGAIN???", the
       second arriving inside the minute the four launches ran.
Need-by: none
Id: tlvphotos-2026-08-07-system-dialogs
```

## What the pack says today, and what it misses

The pack has a rule for the neighbouring case. The 2026-08-05 deposit from this same window
(`attic/inbox-2026-08-05-from-tlvphotos-sweep-stale-local-servers-before-handing-over.md`) covers a
server left listening on every interface, which makes macOS ask about incoming connections. That rule
is about **cleaning up after a session**.

The case here is different in kind and is uncovered: a session **doing its ordinary work** reaches for
something that asks the operating system for permission — a keychain item, a camera, a folder the
sandbox guards, a new binary's first run. No cleanup would have prevented either of tonight's dialogs.
Both were raised by work that was going exactly to plan.

## Why the owner's answer is always Deny, and why that matters

His words: he always presses Deny. That answer is correct of him. A dialog he did not expect names a
binary he did not start, in the middle of work he is not watching, and Deny is the only safe reading of
an unexplained request for a secret.

The consequence is that the session's work fails silently behind it. Tonight both denials were harmless
— the frame-rate reading I wanted came from the two runs that landed before he denied, and the deploy's
key was already trusted. A denial at a worse moment stops a deploy or a publish and leaves a session
diagnosing a failure whose cause was a dialog it never saw.

## The rule this asks for

**Before running anything that can raise a system dialog, say so in one line and let the human decide.**
Where the dialog is a standing cost of a repeated step, say which button ends it for good ("Always
Allow" on a keychain item).

Three properties make this a pack rule rather than one host's habit:

**Every adopted project meets it.** Deploy scripts hold secrets in the keychain, drivers launch
browsers, publish steps reach for tokens. All three are ordinary pack work.

**The session cannot see the dialog.** It blocks a foreign process, or it silently returns an empty
secret. The only channel that reports it is the human interrupting, which is the interruption the rule
exists to prevent.

**It is cheap.** One sentence before the command. The same sentence turns a Deny into an Allow, because
an announced request is one he can judge.

## Where it would live

Alongside the existing conduct rules in `live-spec-base` — the family that already covers what a session
may do to the machine it runs on. The mechanical half, if it is wanted: a short list of the commands
known to raise one (`security find-generic-password`, launching a browser binary the machine has not
run before) that a session announces on sight.

## Who threw it

The tlvphotos window, session of 2026-08-06 night into 2026-08-07, building the terrain prototype.
Alexander's own words are quoted above from that conversation. The host-side half is already recorded
in the personal memory as `never-raise-system-dialogs-unannounced`.
