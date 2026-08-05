# A session leaves listening servers behind, and the owner pays for it weeks later

**From:** the tlvphotos window, 2026-08-05. One habit worth a pack rule. Nothing in the live-spec tree
was changed; this file is the only thing written here.

## What happened

Alexander reported a dialog popping up again and again, asking him to approve something about a
browser. He assumed a test had been rigged. The cause was older than today: three
`python3 -m http.server` processes, started by earlier sessions 22, 20 and 8 days ago, were still
running and still listening on `*:8747`, `*:8973` and `*:8765`.

A server bound to every interface is reachable from the network, so macOS asks the owner to approve
incoming connections, and keeps asking. A server bound to `127.0.0.1` never raises the dialog. This
host's own `lab/serve.py` binds the local address and had been quiet all along.

Stopping the three ended it.

## Why this is a pack-level habit rather than one host's mess

Three properties make it recur anywhere the pack is adopted.

**A served page is the normal way to show work.** A prototype with WebGL, a rendered document, a
screenshot run — each wants a local server, and the quickest line anyone types is
`python3 -m http.server`, which binds every interface by default.

**The cost lands outside the session that caused it.** The process outlives the session, the terminal
and often the week. The person who meets the dialog has no way to connect it to the session that
started the server, which is exactly why he suspected today's tests.

**Nothing in the pack currently notices.** The cleanup rules cover files and browser processes. A
listening socket left behind is invisible to all of them.

## What this host adopted, offered as the rule

Two lines, both cheap:

1. **Bind the local address.** A server a session starts for its own showing binds `127.0.0.1`
   explicitly. The dialog never appears, and the page still opens.
2. **Sweep before handing over.** At the end of a session that served anything, list the listening
   sockets it owns and stop them. `lsof -nP -iTCP -sTCP:LISTEN` reads them in one line; anything older
   than the session belongs to a previous one and is a finding in itself.

A mechanical check is available if the pack wants one: a guard that reds when a listening socket bound
to `0.0.0.0` or `*` belongs to a process started from the project tree. This host has not written it.

## The related rules already in the pack

The browser-cleanup rule scopes a reap by the owning run, and the orphaned-child rule covers a worker
that leaves a process burning. This is the same family with a different resource, so it may belong
beside them rather than as its own rule.
