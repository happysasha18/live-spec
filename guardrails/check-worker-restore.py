#!/usr/bin/env python3
"""check-worker-restore.py — a worker never restores a working tree with a git command (row 479).

BLOCKING. A red flips the exit code to 1 and carries one parseable JSON object beside its human
lines, the gate contract's typed line (guardrails/README.md). It rebuilds no artifact and writes
nothing to disk, so the all-or-nothing write convention has nothing to hold here; it reads and
reports only.

THE LAW, in the words the five prose homes carry. Before a worker mutates a file it means to put
back, it reads that file and holds its bytes. A worker puts a file back by WRITING ITS OWN SAVED
BYTES. A worker runs no command that discards uncommitted work, in any tree: `git checkout --
<path>`, `git checkout .`, `git restore` outside `--staged`, `git stash` and its `push`, `save`,
`create` and `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and `git clean` with
`-f` or `-x`. Such a command's blast radius is a PATH, so its damage lands on files the worker never
wrote and its brief never named. This rule binds a worker in every tree, including its own isolated
worktree, since a worktree shares one repository with the lanes beside it and a worker cannot read
off its brief what else that repository holds. A worker that holds no saved bytes for a file it
mutated, or that believes a file needs a git-level restore, HALTS and reports the file and the
mutation it made, and it writes no further file and runs no further command. The orchestrator owns
recovery: it restores the named file from the last committed stage, hands the worker a fresh brief
carrying that file's current bytes, and records the halt in the row's delivery report, and the
halted work resumes under that new brief. The command list above is the one this gate reds on, word
for word — `guardrails/check-worker-restore.py`, skills/live-spec-base/SKILL.md,
skills/build-pipeline/SKILL.md, skills/build-pipeline/references/delegation-protocol.md,
templates/agent.template.md and scripts/open-lane.sh state one list, and tests/test_worker_restore.py
reds when two of them differ.

WHAT PAID FOR IT. 2026-07-23 in this repo: a caps-sweep worker ran `git checkout -- TEST_MATRIX.md`
and discarded an uncommitted format conversion, recovered only because the converter was
deterministic. 2026-07-27 in the tlvphotos tree: a worker mutated a shipped client bundle to prove a
test row red, restored it with `git checkout -- engine/assets/exhibition.js`, and three minutes
later a sibling lane began writing the sources that assemble into that same file
(inbox/2026-07-27-from-tlvphotos-worker-git-restore-discards-sibling-lanes.md). Both accounts read
as correct work, because the `git status` a careful worker pastes afterwards says "clean" in the
safe case and the destructive one alike. Prose cannot separate them; the command can.

WHAT IT OPENS. The worker-run transcripts under the harness transcript root (default
`~/.claude/projects`, overridable with `--root` or `LIVE_SPEC_TRANSCRIPT_ROOT`): every file matching
`<project-dir>/<session-id>/subagents/agent-*.jsonl`, one file per worker run. Each line is one JSON
record; the gate reads the records whose `type` is `assistant`, walks their `message.content` blocks,
and takes the `input.command` string of every block whose `type` is `tool_use` and whose `name` is
`Bash`. It reads `cwd`, `sessionId`, `agentId` and `timestamp` off the same record to name the run.

WHAT THE SHELL ANSWERED. Every `tool_use` block carries an `id`, and the shell's answer to that call
sits in the same file: a later record holding a `tool_result` block whose `tool_use_id` repeats it. A
call the harness REFUSED is marked on that answering record by a `toolDenialKind` key —
`automode-blocked`, `permission-rule`, `user-rejected` or `interrupted` — and the block carries
`is_error` true with the refusal notice as its text. Nothing reached a shell. A call that RAN carries
no such key whatever its exit status: a success comes back with the shell's stdout, and a command
that exited 1 comes back as an error carrying the shell's own complaint. Across the 2,200 worker runs
on this machine every refusal carries the key and no ordinary answer does, so the key is the whole
signal and the refusal's own text is never read for meaning. A call whose id finds no answering block
— a run cut off mid-call, a transcript still being written — has an UNKNOWN outcome. The answers are
read only from a run that already produced a finding, so a clean run costs the one pass it always
did.

WHAT A FINDING SAYS ABOUT ITS OUTCOME. Every finding names one of the three: the command RAN, the
harness DECLINED it, or the transcript gives no answer and the outcome is UNKNOWN. All three red. The
rule forbids handing such a command to a shell at all, and whether the shell obeyed lies outside the
worker's reach — the same brief and the same momentum land the destructive case on a machine whose
permissions are set one notch looser. What the outcome changes is the RECOVERY, so the findings print
ranked by the work they leave a reader: the executed ones first, then the ones with no recorded
answer, then the declined attempts. Unknown sits second because it cannot be ruled out, and a reader
who must go and check whether bytes are gone faces the same errand as one who knows they are, while a
declined attempt costs nothing to recover and leaves only a brief to tighten. The verdict line tallies
the three, and the typed JSON line carries the first finding after the ranking, so a machine reading
one object reads the most urgent one.

WHAT IT DOES NOT SEE. It reads no prose. A worker report, a brief, or a plan that NAMES a restore is
left alone — only a command the worker actually handed to a shell counts, and only when the segment's
first word is `git`, so the same text quoted inside a `grep` pattern stays silent. Text a command
carries as DATA rather than as commands of its own is outside the reach the same way: the body of a
heredoc (`<<WORD`, `<<'WORD'`, `<<-WORD`, up to its closing delimiter line) is dropped before the
line is cut into segments, and the cutting itself steps over quoted spans, so the forbidden list
written inside `python3 -c "…"` or a quoted brief is one segment whose first word is `python3`, not a
git invocation. A reviewer's read-only probe reds this gate on 2026-08-05 for want of exactly that.
The cost of reading quotes is that a command hidden inside them is unreachable too — `sh -c "git
checkout -- ."` and `echo . | xargs git checkout --` pass, as does a wrapper carrying options
(`sudo -u someone git …`); a bare `command`, `sudo` or `env` prefix is stripped and does not pass. It
reads the parent session's own transcript for nothing: a main-thread session that restores its own
tree is the orchestrator acting, which the rule allows. It cannot tell whether the worker ran inside
its own isolated worktree; that case reds like any other, which is the scope the clause states.

WHERE IT PLACES A FINDING. A command string is read left to right for a moving effective directory,
starting at the record's own cwd: a `cd <path>` moves it (`cd -`, `pushd` and `popd` move it to
UNKNOWN, since the gate does not track a directory stack), a plain literal assignment earlier in the
same string (`S=/some/path`) is remembered so a later `cd $S/sub` still resolves, and a `git -C <path>`
sets the directory for that one invocation only, without moving the running one. A target built from
anything the gate cannot read statically — an unassigned variable, a subshell, command substitution —
sets the effective directory to UNKNOWN. Where a `cd` lands depends on the SEPARATOR that joined the
next command to it, because a cd can fail. After `cd X &&` the next command ran only if the cd
succeeded, so it is placed at X. After `cd X ;` or `cd X ||` the next command ran either way, so when
X is gone from disk at scan time the cd may well have failed and left the shell where it was: the
command is placed at the PRE-CD directory, the conservative read of the two. That is the escape
`cd /nonexistent ; git checkout -- .` walked through until 2026-08-05, running git in the record's own
cwd while the gate filed it under a directory that never existed. `set -e` changes the reading of `;`
and of a newline, and only of those: under errexit a failed cd ends the script, so a command that ran
at all proves the cd succeeded and is placed at X. That is the shape the fixture scripts in this repo
carry (`set -e`, then `mkdir -p X && cd X`, then the next line), and the gate follows `set +e` back
off again. A forbidden git command reds when it
ran at the record's cwd with no `cd` in between, as it always has, or when it ran at a known directory
whose enclosing git repository still exists on disk at scan time (walking up from it for a `.git`); a
known directory gone from disk, or holding no enclosing repository, is not a finding, and an UNKNOWN
effective directory reds, since the gate can place it no better than a record with no timestamp. Each
finding's report line names the effective directory beside the session's recorded cwd.

WHERE IT RUNS. At the verify step of skills/build-pipeline/SKILL.md, between a worker's result and
the orchestrator's acceptance of it, and once more in the suite as tests/test_worker_restore.py's
real-root case. A push gate would run long after the bytes are gone.

THE COUNTING START. This machine's transcripts hold worker runs from before the gate existed, and 81
of them carry a discarding command. A gate that reds on that history would be turned off on its first
run, so the gate carries a start date (COUNTING_FROM below, `--counting-from`, or
LIVE_SPEC_WORKER_RESTORE_FROM). A finding whose record is stamped before the start date is carried as
history: it is counted in every verdict line and reds nothing. A finding stamped on or after the start
date reds. A finding whose record carries no timestamp reds, since the gate cannot place it. Move the
date back to read the history: `--counting-from 2000-01-01 --all` lists every finding on disk.

The start carries a date, or an ISO timestamp that adds a time of day
(`2026-08-12T06:06:00Z`); a plain date still means midnight at the start of that day, so nothing
already written changes meaning.

The start moved twice on 2026-08-12. First from 2026-07-28 to 2026-08-13, to carry one recorded
finding as history — session `af22b716-c9d7-48b2-b3fd-2be1820a1a14` handed a shell `git checkout --
lab/data/step3-grid-derivation.json` in `/Users/sashaabramovich/tlvphotos` at 2026-08-12T06:05:40Z. A
whole-day step also carried every discarding command run for the rest of that day past the gate
unnoticed, with several workers running in this repository the same day. The start now reads
`2026-08-12T06:06:00Z`, one minute after the finding: the finding still stands as history, recorded
in `DECISIONS.md` (2026-08-12) and `ROADMAP.md` row 598, and every discarding command stamped
2026-08-12T06:06:00Z or later reds again. A red that can never clear blocks every future run, so the
date moves forward on a recorded finding, never in silence — and never further than the finding
requires.

What that finding cost was read wrong when it was written, and the tlvphotos reply of the same day
corrected it (`inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md`, 2026-08-12): the harness
classifier declined the call, the command never ran, and the file's one uncommitted line — a
regenerated timestamp — survived. The gate now says as much in the finding itself. The start stays
where it stands all the same, and it was tested back at `2026-07-28` on 2026-08-12 with the outcome
visible to see. Two findings red at that value: the declined tlvphotos attempt, and one that RAN —
session `176e927f-4e67-4fa6-887e-86d1d6e5d1e4` at 2026-07-28T21:12:39Z, `git checkout --
guardrails/rule-census.json` in this repository's own tree. A declined attempt reds like any other,
so either one turns a finished incident into a red no future run can clear, which is the one thing
the counting start exists to prevent.

THE STAND-DOWN. When the transcript root does not exist, this host keeps no transcripts where the
gate looks. The gate stands down, says so by name, and exits 0 — a stated stand-down rather than a
silent pass. When the root DOES exist but holds no worker-run transcript at all, the layout the gate
reads has moved and the check would report clean while testing nothing; that is the vacuous pass
guardrails/nonempty_input.py names, and it reds by name (SPEC INV-218). The time window is applied
after that check, and a window holding no worker run is legitimate — a session may spawn no worker —
so an empty WINDOW is declared here as a permitted empty set and reports OK naming the window.

Usage:
  check-worker-restore.py [--root PATH] [--since-hours H] [--all]
                           [--counting-from YYYY-MM-DD | YYYY-MM-DDTHH:MM:SSZ]
Exit 0 when no worker run handed a shell a discarding command since the counting start, 1 otherwise,
whether the shell ran that command or declined it.
Stdlib only.
"""
import argparse
import glob
import json
import os
import re
import shlex
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-worker-restore"
DEFAULT_ROOT = os.path.join(os.path.expanduser("~"), ".claude", "projects")
DEFAULT_SINCE_HOURS = 24.0
RUN_GLOB = os.path.join("*", "*", "subagents", "agent-*.jsonl")

# The moment the gate began counting. Every worker run stamped before it is history: the clause was
# written on 2026-07-27 and the machine's transcripts hold runs from before it, so a gate that red on
# them would have been switched off rather than obeyed. History is counted and named in every verdict
# line, and reds nothing. The value moves forward only with a recorded reason, never further than
# that reason requires, and moving it forward hides findings — read the history first with
# `--counting-from 2000-01-01 --all`. It reads a plain date (meaning midnight at the start of that
# day) or a full ISO timestamp with a time of day.
#
# Moved from 2026-07-28 to 2026-08-13 on 2026-08-12, to carry one finding as history: session
# af22b716-c9d7-48b2-b3fd-2be1820a1a14 handed a shell `git checkout --
# lab/data/step3-grid-derivation.json` in /Users/sashaabramovich/tlvphotos at 2026-08-12T06:05:40Z.
# That whole-day step also carried every discarding command run for the rest of 2026-08-12 past the
# gate unnoticed. Narrowed the same day to 2026-08-12T06:06:00Z, one minute after the finding: the
# finding still stands as history, recorded in DECISIONS.md (2026-08-12) and ROADMAP.md row 598, and
# every discarding command from 06:06 onward that day reds again.
#
# The value was re-tested at 2026-07-28 on 2026-08-12, once the outcome of that command became
# visible in the finding: the tlvphotos reply established that the classifier declined the call and
# nothing was lost (inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md). Two findings red at
# 2026-07-28 — that declined attempt, and one that ran in this repo's own tree on 2026-07-28T21:12:39Z
# — and a declined attempt reds like any other, so the earlier value turns two finished incidents into
# a permanent red and the 06:06 start stays.
COUNTING_FROM = "2026-08-12T06:06:00Z"

# What the shell did with a command the gate found. All three red; they differ in the recovery they
# leave, and the findings print in this order — the executed ones first, the ones the transcript
# never answered second because they cannot be ruled out, the declined attempts last.
OUTCOME_RAN = "ran"
OUTCOME_DECLINED = "declined"
OUTCOME_UNKNOWN = "unknown"
OUTCOME_ORDER = {OUTCOME_RAN: 0, OUTCOME_UNKNOWN: 1, OUTCOME_DECLINED: 2}

# The reason a run's transcript can answer nothing about a call it recorded.
NO_ANSWER = "the run's transcript carries no tool_result for this call"

# The segment separators a shell command line is cut on, so `cd x && git restore y` is read as its
# own invocation. The pipe is included: `yes | git clean -fd` is still git clean. Each separator is
# kept beside the segment it follows, because `cd x && git …` and `cd x ; git …` place that git
# invocation in different directories when x is gone at scan time (see `_dir_after_cd`).
SEPARATORS = ("&&", "||", ";", "|", "\n")

# Wrappers that stand in front of a command and hand it straight on, so the act is the wrapped
# command's: `command git checkout -- .` and `sudo git checkout -- .` discard exactly what the bare
# form discards.
WRAPPERS = ("command", "sudo", "env")

# A heredoc opener: `<<WORD`, `<<'WORD'`, `<<"WORD"` or `<<-WORD`. The `<<<` herestring is not one.
_HEREDOC_OPENER = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")

WHOLE_TREE = "the whole working tree"

# A counting-start value: a plain date, or an ISO timestamp that adds a time of day.
_COUNTING_FROM_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_COUNTING_FROM_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def _without_heredoc_bodies(command):
    """`command` with every heredoc BODY dropped and its opener line kept.

    A heredoc body is data handed to a command, not lines the shell reads for commands of its own, so
    a brief or a probe written `python3 - <<'PY' … PY` that quotes the forbidden list is not a run of
    it. The closing delimiter line goes with the body; a heredoc left unclosed swallows the rest of
    the string, which is what the shell does with it too. The delimiter is matched on the line's
    stripped text for `<<` and `<<-` alike — a body line that is exactly the delimiter word and
    nothing else is the terminator in practice.
    """
    lines = command.split("\n")
    kept = []
    i = 0
    while i < len(lines):
        line = lines[i]
        kept.append(line)
        i += 1
        for match in _HEREDOC_OPENER.finditer(line):
            word = match.group(2)
            while i < len(lines) and lines[i].strip() != word:
                i += 1
            if i < len(lines):
                i += 1  # step past the closing delimiter line itself
    return "\n".join(kept)


def _cut_on_separators(text):
    """`text` cut into (span, separator-after) pairs on the separators that stand OUTSIDE quotes.

    A separator inside `'…'` or `"…"` belongs to the quoted text, not to the shell: without this,
    `python3 -c "…git checkout -- .…"` was cut at the newlines inside the script and each line of the
    quoted script was read as a command of its own. The last pair carries the empty separator. Plain
    character walking, no shell.
    """
    out = []
    buf = []
    quote = None
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if quote == "'":
            buf.append(ch)
            if ch == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if ch == "\\" and i + 1 < n:
                buf.append(ch)
                buf.append(text[i + 1])
                i += 2
                continue
            buf.append(ch)
            if ch == '"':
                quote = None
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            buf.append(ch)
            buf.append(text[i + 1])
            i += 2
            continue
        if ch in "'\"":
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if text[i:i + 2] in ("&&", "||"):
            out.append(("".join(buf), text[i:i + 2]))
            buf = []
            i += 2
            continue
        if ch in (";", "|", "\n"):
            out.append(("".join(buf), ch))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    out.append(("".join(buf), ""))
    return out


def _segments(command):
    """The command line cut into invocations, each with the separator that joined the NEXT one to it.

    Heredoc bodies are dropped first and quoted spans are stepped over, so only text the shell would
    have read as commands is cut. An empty span drops out with its own separator, which leaves each
    invocation holding the first separator that follows it.
    """
    return [(span.strip(), sep)
            for span, sep in _cut_on_separators(_without_heredoc_bodies(command))
            if span.strip()]


def _tokens(segment):
    """The segment's words. shlex keeps a quoted phrase as ONE token, which is what keeps a
    `grep 'git restore'` pattern from reading as a git invocation."""
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def _is_assignment(token):
    """True when the token is a plain `NAME=value` prefix rather than a word of the command."""
    if token.startswith("-") or "=" not in token:
        return False
    head = token.split("=", 1)[0]
    return bool(head) and all(c.isalnum() or c == "_" for c in head)


def _command_tokens(segment):
    """The segment's words with leading `VAR=value` assignments and pass-through wrappers stripped,
    so the first word left is the program that really ran.

    `command git checkout -- .` and `sudo git checkout -- .` are the bare command's act, and they
    walked past this gate until 2026-08-05 for want of the strip. A wrapper carrying OPTIONS
    (`sudo -u someone git …`) is left alone, since stepping over an option that takes a value cannot
    be done without knowing the wrapper's own grammar, and a wrapper that takes the command as a
    STRING (`sh -c "git …"`, `xargs git …`) stays out of reach — both are named in the module
    docstring.
    """
    tokens = _tokens(segment)
    while tokens:
        if _is_assignment(tokens[0]) or os.path.basename(tokens[0]) in WRAPPERS:
            tokens = tokens[1:]
            continue
        break
    return tokens


def _git_args(segment):
    """The arguments of a git invocation, or None when this segment is not one.

    A segment is a git invocation only when its first word — past leading `VAR=value` assignments and
    a `command`, `sudo` or `env` wrapper — is exactly `git`. git's own pre-command options
    (`-C <path>`, `-c <k=v>`, `--git-dir=…`) are stepped over so the subcommand is the first thing
    returned.
    """
    tokens = _command_tokens(segment)
    if not tokens or os.path.basename(tokens[0]) != "git":
        return None
    args = tokens[1:]
    while args:
        if args[0] in ("-C", "-c", "--namespace", "--work-tree", "--git-dir") and len(args) > 1:
            args = args[2:]
        elif args[0].startswith("--git-dir=") or args[0].startswith("--work-tree=") \
                or args[0].startswith("-c") and len(args[0]) > 2:
            args = args[1:]
        else:
            break
    return args


def _is_redirection(token):
    """A shell redirection word (`>out`, `2>&1`, `<in`, `>>log`), which names no path git touches."""
    stripped = token.lstrip("0123456789&")
    return stripped.startswith(">") or stripped.startswith("<")


def _paths_after_double_dash(args):
    """The paths a checkout/restore names: everything after `--`, else the non-flag words.

    Shell redirections are dropped — `git stash push -- SPEC.md >/dev/null` names one path, and a
    finding that listed `>/dev/null` beside it would misname the blast radius.
    """
    if "--" in args:
        paths = args[args.index("--") + 1:]
    else:
        paths = [a for a in args if not a.startswith("-")]
    out = []
    skip_next = False
    for p in paths:
        if skip_next:
            skip_next = False
            continue
        if not p:
            continue
        if p in (">", ">>", "<", "2>", "&>"):
            skip_next = True
            continue
        if _is_redirection(p):
            continue
        out.append(p)
    return out


def _var_assignment(segment):
    """(name, value) when `segment` is a standalone literal variable assignment — one token of
    the form `NAME=value`, its value carrying no shell construct the gate cannot read
    statically. `S=/tmp/x` is one; `S=$(pwd)`, `` S=`pwd` `` and `export S=/tmp/x` are not,
    since the first hides a command and the other two are not a bare assignment."""
    tokens = _tokens(segment)
    if len(tokens) != 1:
        return None
    token = tokens[0]
    if "=" not in token:
        return None
    name, value = token.split("=", 1)
    if not name or not (name[0].isalpha() or name[0] == "_") \
            or not all(c.isalnum() or c == "_" for c in name):
        return None
    if "$" in value or "`" in value:
        return None
    return name, value


_VAR_REF = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?")


def _substitute(raw, env):
    """`raw` with every `$VAR`/`${VAR}` reference resolved against `env`. None — the gate's
    UNKNOWN — when a reference is not in `env`, or `raw` carries a construct static reading
    cannot chase (command substitution, backticks)."""
    if raw is None or "`" in raw or "$(" in raw:
        return None
    missing = []

    def repl(m):
        name = m.group(1)
        if name not in env:
            missing.append(name)
            return ""
        return env[name]

    out = _VAR_REF.sub(repl, raw)
    return None if missing else out


def _resolve_dir(target, base):
    """`target` (already variable-substituted) resolved against effective directory `base`.
    None — UNKNOWN — when `target` itself is None, or `target` is relative and `base` is
    UNKNOWN, since a relative path has nothing to resolve against."""
    if target is None:
        return None
    if os.path.isabs(target):
        return os.path.normpath(target)
    if base is None:
        return None
    return os.path.normpath(os.path.join(base, target))


def _git_dash_c_dir(segment, base, env):
    """(has_c, directory) for a `git -C <path>` on this segment, chaining several `-C` options
    the way git itself does — each resolved against the one before. `has_c` is False when the
    segment carries no `-C`, in which case `directory` is meaningless and the caller keeps
    using the running effective directory instead.
    """
    tokens = _command_tokens(segment)
    if not tokens or os.path.basename(tokens[0]) != "git":
        return False, None
    args = tokens[1:]
    cur = base
    has_c = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-C" and i + 1 < len(args):
            has_c = True
            cur = _resolve_dir(_substitute(args[i + 1], env), cur)
            i += 2
            continue
        if a.startswith("-C") and len(a) > 2:
            has_c = True
            cur = _resolve_dir(_substitute(a[2:], env), cur)
            i += 1
            continue
        if a in ("-c", "--namespace", "--work-tree", "--git-dir") and i + 1 < len(args):
            i += 2
            continue
        if a.startswith("--git-dir=") or a.startswith("--work-tree=") \
                or (a.startswith("-c") and len(a) > 2):
            i += 1
            continue
        break
    return has_c, cur


def _repo_exists_at_or_above(path):
    """True when `path` exists on disk right now and it, or an ancestor, holds a `.git`."""
    if not path or not os.path.isdir(path):
        return False
    cur = os.path.normpath(path)
    while True:
        if os.path.exists(os.path.join(cur, ".git")):
            return True
        parent = os.path.dirname(cur)
        if parent == cur:
            return False
        cur = parent


def _errexit_after(tokens, errexit):
    """`errexit` as this `set` line leaves it. `set -e`, `set -eu` and `set -o errexit` turn it on;
    `set +e` and `set +o errexit` turn it off, which a script does around a step it expects to fail."""
    i = 1
    while i < len(tokens):
        a = tokens[i]
        if a in ("-o", "+o") and i + 1 < len(tokens):
            if tokens[i + 1] == "errexit":
                errexit = a == "-o"
            i += 2
            continue
        if a.startswith("-") and "e" in a[1:]:
            errexit = True
        elif a.startswith("+") and "e" in a[1:]:
            errexit = False
        i += 1
    return errexit


def _dir_after_cd(before, target, separator, errexit):
    """The effective directory the command AFTER this `cd` really ran in.

    A cd can fail, and what the next command did about it decides where that command ran. `&&` runs
    it only when the cd succeeded, so the target stands — and a target gone from disk at scan time
    then drops the finding, which is the throwaway-fixture case. Under `set -e` a `;` and a newline
    say the same thing, because a failed cd ends the script and nothing after it runs at all: the
    fixture scripts this repo's own workers write are exactly that shape
    (`set -e` … `mkdir -p X && cd X` … newline … `git checkout -q -- .`), and reading their newline
    as ambiguous would file a throwaway repo's command against the session's real tree.

    With errexit off, `;`, `||`, a pipe and a newline run the next command whether the cd succeeded or
    not, so a target gone at scan time leaves the run ambiguous between the target and the directory
    the shell never left; the PRE-CD directory is the conservative read of the two, and it reds when
    it is the record's own cwd in a real repository. `||` keeps that read even under errexit, since a
    command followed by `||` is exempt from errexit and the branch runs precisely when the cd failed.
    """
    if target is None:
        return None
    if separator == "&&":
        return target
    if errexit and separator in (";", "\n"):
        return target
    if os.path.isdir(target):
        return target
    return before


def classify(command, cwd):
    """The discarding invocations in one shell command line, each placed in the directory it
    really ran in.

    Walks the command's own segments in order, holding an effective directory that starts at
    `cwd` and moves with each `cd` (see `_resolve_dir` and `_dir_after_cd`, which reads the
    separator after the `cd`, and whether `set -e` is standing, so a FAILED cd does not carry the
    next command out of the record's cwd) and a running map of the plain literal variable assignments the command made along the
    way, so `S=/tmp/x` earlier in the same string lets a later `cd $S/sub` still resolve. A
    `git -C <path>` sets the directory for that one invocation only. A forbidden git command
    reds when it ran at `cwd` with no `cd` in between (the gate's original, unconditional read),
    or at a known directory whose enclosing git repository still exists on disk at scan time; a
    known directory gone from disk or holding no enclosing repository is not a finding, and an
    UNKNOWN effective directory reds, since the gate can place it no better than an unstamped
    record.

    Returns a list of {"command": <the segment>, "which": <the named form>, "paths": [...],
    "effective_dir": <the directory the command ran in, or None for UNKNOWN>}. An empty list
    means the line discards nothing this gate reds on.
    """
    found = []
    env = {}
    effective_dir = cwd
    errexit = False
    for segment, separator in _segments(command):
        assignment = _var_assignment(segment)
        if assignment is not None:
            env[assignment[0]] = assignment[1]
            continue

        tokens = _tokens(segment)
        if tokens and tokens[0] == "set":
            errexit = _errexit_after(tokens, errexit)
            continue
        if tokens and tokens[0] == "cd":
            target = tokens[1] if len(tokens) > 1 else None
            if target == "-":
                effective_dir = None
            else:
                effective_dir = _dir_after_cd(
                    effective_dir, _resolve_dir(_substitute(target, env), effective_dir),
                    separator, errexit)
            continue
        if tokens and tokens[0] in ("pushd", "popd"):
            effective_dir = None  # no directory stack is tracked, so a pop cannot be placed either.
            continue

        has_c, c_dir = _git_dash_c_dir(segment, effective_dir, env)
        command_dir = c_dir if has_c else effective_dir

        args = _git_args(segment)
        if args is None or not args:
            continue
        sub, rest = args[0], args[1:]
        hit = None
        if sub == "checkout":
            # `git checkout -- <paths>` and `git checkout .` overwrite the working tree from the
            # index. `git checkout <branch>` moves HEAD and keeps uncommitted work, so it is silent.
            if "--" in rest or rest[:1] == ["."]:
                hit = {"which": "git checkout --", "paths": _paths_after_double_dash(rest)}
        elif sub == "restore":
            # `git restore --staged <path>` only unstages and leaves the working tree alone; every
            # other form of restore writes over it.
            if not ("--staged" in rest and "--worktree" not in rest and "-W" not in rest):
                hit = {"which": "git restore", "paths": _paths_after_double_dash(rest)}
        elif sub == "stash":
            # Bare `git stash`, `push` and `save` take the working tree away. `list`, `show`, `pop`,
            # `apply`, `branch`, `drop` and `clear` do not remove uncommitted work from the tree.
            verb = next((a for a in rest if not a.startswith("-")), "")
            if verb in ("", "push", "save", "create", "store") or not rest:
                paths = _paths_after_double_dash(rest[1:] if verb in ("push", "save") else rest)
                hit = {"which": "git stash", "paths": paths or [WHOLE_TREE]}
        elif sub == "reset":
            # `git reset <paths>` and `--soft`/`--mixed` leave the working tree; `--hard`, `--merge`
            # and `--keep` write over it.
            if any(a in ("--hard", "--merge", "--keep") for a in rest):
                hit = {"which": "git reset --hard", "paths": [WHOLE_TREE]}
        elif sub == "clean":
            # The same act against untracked files: a sibling lane's new file is uncommitted work too.
            if any(a.startswith("-") and ("f" in a or "x" in a) for a in rest):
                hit = {"which": "git clean", "paths": _paths_after_double_dash(rest) or [WHOLE_TREE]}

        if hit is None:
            continue

        if command_dir is None:
            reds = True  # UNKNOWN: as conservative a read as a record with no timestamp.
        elif cwd is not None and os.path.normpath(command_dir) == os.path.normpath(cwd):
            reds = True  # the record's cwd, no intervening cd — the gate's original read.
        else:
            reds = _repo_exists_at_or_above(command_dir)
        if not reds:
            continue

        hit["command"] = segment
        hit["effective_dir"] = command_dir
        found.append(hit)
    return found


def worker_runs(root):
    """Every worker-run transcript under the harness transcript root, sorted."""
    return sorted(glob.glob(os.path.join(root, RUN_GLOB)))


def _bash_commands(path):
    """Every Bash command a worker run handed to a shell, with the record that names the run and the
    `tool_use` id the shell's answer will repeat."""
    out = []
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return out
    with fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") != "assistant":
                continue
            blocks = rec.get("message", {}).get("content", []) or []
            if not isinstance(blocks, list):
                continue
            for b in blocks:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                if b.get("name") != "Bash":
                    continue
                command = (b.get("input") or {}).get("command")
                if isinstance(command, str) and command.strip():
                    out.append((command, rec, b.get("id")))
    return out


def _outcome_of(record, block):
    """(outcome, detail) for one `tool_result`: what the shell did with the call it answers.

    `toolDenialKind` is the harness's own word for a call it refused, and it stands on a refusal
    alone. The refusal notice beside it is text the gate never reads for meaning — the key is the
    whole signal. Every other answer came back from a shell that RAN the command, whatever its exit
    status, so a command that exited non-zero still ran and still discarded whatever it reached
    before it stopped.
    """
    kind = record.get("toolDenialKind")
    if kind:
        return OUTCOME_DECLINED, str(kind)
    if block.get("is_error"):
        return OUTCOME_RAN, "the shell answered with an error"
    return OUTCOME_RAN, ""


def _answers(path, tool_use_ids):
    """The shell's answer to each of `tool_use_ids`, read out of the same run transcript.

    A `tool_use` id missing from the returned map had no `tool_result` in the file, which is the
    UNKNOWN outcome. Called only for a run that already produced a finding, so the ordinary clean
    run never pays for this second pass.
    """
    out = {}
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return out
    with fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("{") or '"tool_result"' not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            blocks = rec.get("message", {}).get("content", []) or []
            if not isinstance(blocks, list):
                continue
            for b in blocks:
                if not isinstance(b, dict) or b.get("type") != "tool_result":
                    continue
                tool_id = b.get("tool_use_id")
                if tool_id in tool_use_ids:
                    out[tool_id] = _outcome_of(rec, b)
    return out


def scan(paths):
    """The findings across a set of worker-run transcripts, each naming command, path, run, and what
    the shell did with the command."""
    findings = []
    commands_read = 0
    for path in paths:
        hits_here = []
        wanted = set()
        for command, rec, tool_id in _bash_commands(path):
            commands_read += 1
            cwd = rec.get("cwd")
            for hit in classify(command, cwd):
                hits_here.append((hit, rec, tool_id))
                wanted.add(tool_id)
        if not hits_here:
            continue
        answers = _answers(path, wanted)
        for hit, rec, tool_id in hits_here:
            outcome, detail = answers.get(tool_id, (OUTCOME_UNKNOWN, NO_ANSWER))
            cwd = rec.get("cwd")
            findings.append({
                "run": path,
                "agent": rec.get("agentId") or "(unnamed run)",
                "session": rec.get("sessionId") or "(unnamed session)",
                "cwd": cwd or "(unrecorded cwd)",
                "at": rec.get("timestamp") or "(unstamped)",
                "which": hit["which"],
                "command": hit["command"],
                "paths": hit["paths"] or [WHOLE_TREE],
                "effective_dir": hit.get("effective_dir"),
                "outcome": outcome,
                "outcome_detail": detail,
            })
    return findings, commands_read


def _normalize_stamp(value):
    """`value`'s first 19 characters as `YYYY-MM-DDTHH:MM:SS`, comparable as plain text against
    another normalized stamp.

    A bare date (`YYYY-MM-DD`, 10 characters) is padded with `T00:00:00` — midnight at the start of
    that day, which is what a date-only value has always meant here, so nothing already written
    changes meaning. A fuller timestamp is read only to the second; a trailing `Z`, a fractional
    part, or a numeric offset falls past the 19th character and is dropped.
    """
    if len(value) == 10:
        return value + "T00:00:00"
    return value[:19]


def is_history(finding, counting_from):
    """True when the run's record is stamped before the counting start.

    The stamp is the harness's ISO-8601 timestamp. Both it and the counting start are normalized to
    `YYYY-MM-DDTHH:MM:SS` (see `_normalize_stamp`) and compared as text, which reads a start carrying
    a time of day exactly as finely as it reads one that doesn't. A record carrying no stamp is never
    history: the gate cannot place it in time, and an unplaceable finding is read as a new one.
    """
    at = finding.get("at") or ""
    if len(at) < 10 or not at[:4].isdigit():
        return False
    return _normalize_stamp(at) < _normalize_stamp(counting_from)


def finding_line(f):
    """The finding's own sentence, saying what the command was and what the shell did with it.

    All three outcomes are findings — the rule forbids handing the command to a shell — and each
    sentence names the recovery its outcome leaves behind, so a reader learns from the first line
    whether bytes are gone, may be gone, or were never at risk.
    """
    paths = ", ".join(f["paths"])
    outcome = f.get("outcome", OUTCOME_UNKNOWN)
    if outcome == OUTCOME_RAN:
        return ("%s ran `%s` — %s, discarding every uncommitted change under %s, including bytes "
                "the run never wrote and its brief never named (ROADMAP row 479)."
                % (f["agent"], f["command"], f["which"], paths))
    if outcome == OUTCOME_DECLINED:
        return ("%s handed a shell `%s`, a %s that would have discarded every uncommitted change "
                "under %s, and the harness declined the call (%s), so nothing was discarded and the "
                "finding stands on the attempt (ROADMAP row 479)."
                % (f["agent"], f["command"], f["which"], paths,
                   f.get("outcome_detail") or "declined"))
    return ("%s handed a shell `%s`, a %s whose blast radius is every uncommitted change under %s, "
            "and %s, so whether those bytes were discarded is unknown and wants checking by hand "
            "(ROADMAP row 479)."
            % (f["agent"], f["command"], f["which"], paths, f.get("outcome_detail") or NO_ANSWER))


def outcome_phrase(f):
    """The finding's outcome in one field, for the indented detail block."""
    outcome = f.get("outcome", OUTCOME_UNKNOWN)
    detail = f.get("outcome_detail") or ""
    if outcome == OUTCOME_RAN:
        return "RAN%s" % (" (%s)" % detail if detail else "")
    if outcome == OUTCOME_DECLINED:
        return "DECLINED by the harness (%s) — it never reached a shell" % (detail or "declined")
    return "UNKNOWN — %s" % (detail or NO_ANSWER)


def outcome_tally(findings):
    """The sentence that counts the outcomes across a set of findings."""
    counts = outcome_counts(findings)
    return ("%d ran, %d declined by the harness before reaching a shell, %d with no recorded "
            "answer; the executed ones print first"
            % (counts[OUTCOME_RAN], counts[OUTCOME_DECLINED], counts[OUTCOME_UNKNOWN]))


def outcome_counts(findings):
    """How many findings carry each outcome."""
    counts = {OUTCOME_RAN: 0, OUTCOME_DECLINED: 0, OUTCOME_UNKNOWN: 0}
    for f in findings:
        counts[f.get("outcome", OUTCOME_UNKNOWN)] = counts.get(f.get("outcome", OUTCOME_UNKNOWN), 0) + 1
    return counts


def typed_message(f):
    """The typed line's message, which names the outcome as plainly as the human line does."""
    outcome = f.get("outcome", OUTCOME_UNKNOWN)
    if outcome == OUTCOME_RAN:
        head, verb = "a worker run discarded working-tree changes", "ran"
    elif outcome == OUTCOME_DECLINED:
        head, verb = ("a worker run handed a shell a command that discards working-tree changes and "
                      "the harness declined it", "handed")
    else:
        head, verb = ("a worker run handed a shell a command that discards working-tree changes, "
                      "with no answer recorded", "handed")
    return ("%s: %s %s `%s` against %s in %s (ROADMAP row 479)"
            % (head, f["agent"], verb, f["command"], ", ".join(f["paths"]), f["run"]))


def _open_sentence(text):
    """The phrase opened as its own sentence, with the rest of it left as written."""
    return text[:1].upper() + text[1:]


def history_phrase(count, counting_from):
    """The sentence every verdict carries about the history it read past."""
    if not count:
        return ("no finding on this root is stamped before the counting start %s" % counting_from)
    return ("%d finding%s stamped before the counting start %s %s as history and red%s nothing; "
            "read %s with `--counting-from 2000-01-01 --all`"
            % (count, "" if count == 1 else "s", counting_from,
               "stands" if count == 1 else "stand", "s" if count == 1 else "",
               "it" if count == 1 else "them"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="red when a worker run discarded working-tree changes")
    parser.add_argument("--root", default=os.environ.get("LIVE_SPEC_TRANSCRIPT_ROOT", DEFAULT_ROOT))
    parser.add_argument("--since-hours", type=float,
                        default=float(os.environ.get("LIVE_SPEC_WORKER_RESTORE_SINCE_HOURS",
                                                     DEFAULT_SINCE_HOURS)))
    parser.add_argument("--all", action="store_true",
                        help="read every worker run on disk rather than the recent window")
    parser.add_argument("--counting-from",
                        default=os.environ.get("LIVE_SPEC_WORKER_RESTORE_FROM", COUNTING_FROM),
                        help="the moment the gate starts counting; a finding stamped before it is "
                             "carried as history (YYYY-MM-DD, or YYYY-MM-DDTHH:MM:SSZ for a time "
                             "of day)")
    args = parser.parse_args(argv)

    counting_from = args.counting_from.strip()
    if not (_COUNTING_FROM_DATE_RE.match(counting_from)
             or _COUNTING_FROM_TIMESTAMP_RE.match(counting_from)):
        print("%s: --counting-from reads %r, and the gate reads a date written YYYY-MM-DD or an "
              "ISO timestamp written YYYY-MM-DDTHH:MM:SSZ."
              % (CHECK, args.counting_from))
        return 1

    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        print("%s: STAND-DOWN — the transcript root %s does not exist, so this host keeps no worker-run "
              "transcripts where the gate looks. The check ran nothing and claims nothing; point it at a "
              "real root with --root or LIVE_SPEC_TRANSCRIPT_ROOT (ROADMAP row 479)." % (CHECK, root))
        return 0

    runs = worker_runs(root)
    try:
        runs = require_nonempty(CHECK, "the worker-run transcripts under %s" % root, runs)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        print("%s: the layout it reads is %s under the transcript root; a root holding none of them "
              "means the harness moved them, and a clean verdict over zero runs would protect "
              "nothing." % (CHECK, RUN_GLOB))
        return 1

    window = "every worker run on disk"
    if not args.all:
        cutoff = time.time() - args.since_hours * 3600.0
        kept = []
        for p in runs:
            try:
                if os.path.getmtime(p) >= cutoff:
                    kept.append(p)
            except OSError:
                continue
        runs = kept  # a window holding no worker run is permitted: a session may spawn no worker.
        window = "the worker runs touched in the last %g hours" % args.since_hours

    findings, commands_read = scan(runs)
    history, current = [], []
    for f in findings:
        (history if is_history(f, counting_from) else current).append(f)

    if current:
        # Most urgent first: executed, then unanswered, then declined. Python's sort is stable, so
        # findings sharing an outcome keep the order the transcripts were read in.
        current.sort(key=lambda f: OUTCOME_ORDER.get(f.get("outcome"), OUTCOME_ORDER[OUTCOME_UNKNOWN]))
        for f in current:
            print("%s: %s" % (CHECK, finding_line(f)))
            print("    run     : %s" % f["run"])
            ran_in = f.get("effective_dir")
            ran_in = ran_in if ran_in is not None else "UNKNOWN (a cd target the gate could not read statically)"
            print("    session : %s   cwd: %s   ran in: %s   at: %s"
                  % (f["session"], f["cwd"], ran_in, f["at"]))
            print("    outcome : %s" % outcome_phrase(f))
        print()
        print("Before a worker mutates a file it means to put back, it reads that file and holds its")
        print("bytes, and it puts the file back by WRITING ITS OWN SAVED BYTES. A worker runs no")
        print("command that discards uncommitted work, in any tree: git checkout -- <path>,")
        print("git checkout ., git restore outside --staged, git stash and its push, save, create and")
        print("store forms, git reset with --hard, --merge or --keep, and git clean with -f or -x.")
        print("This rule binds a worker in every tree, including its own isolated worktree, since a")
        print("worktree shares one repository with the lanes beside it. A worker that holds no saved")
        print("bytes for a file it mutated HALTS and reports the file and the mutation it made. The")
        print("orchestrator owns recovery: it restores the named file from the last committed stage,")
        print("hands the worker a fresh brief carrying that file's current bytes, and records the halt")
        print("in the row's delivery report.")
        print("Handing such a command to a shell breaks the rule whether the shell obeyed or refused,")
        print("so every outcome above is a finding; what the outcome tells a reader is how much")
        print("recovery it faces. Outcomes: %s." % outcome_tally(current))
        print("Reach: %s under %s, %d command line%s read; %s."
              % (window, root, commands_read, "" if commands_read == 1 else "s",
                 history_phrase(len(history), counting_from)))
        first = current[0]
        counts = outcome_counts(current)
        print(json.dumps({
            "severity": "error",
            "code": "worker-restore",
            "outcome": first.get("outcome", OUTCOME_UNKNOWN),
            "outcomes": {"ran": counts[OUTCOME_RAN], "declined": counts[OUTCOME_DECLINED],
                         "unknown": counts[OUTCOME_UNKNOWN]},
            "message": typed_message(first),
            "fix": ("a worker restores a file it mutated by writing its own saved bytes back, and halts "
                    "and reports when a file needs a git-level restore — the orchestrator owns recovery"),
        }))
        return 1

    print("OK (%s): no worker run handed a shell a discarding command since %s. Read %s under %s — the "
          "files matching %s, one per worker run — taking every assistant record's Bash tool_use command "
          "field (%d command line%s) and reading each git invocation's subcommand and flags for "
          "git checkout -- and git checkout ., git restore outside --staged, git stash and its push, "
          "save, create and store forms, git reset with --hard, --merge or --keep, and git clean with "
          "-f or -x. Report prose is outside the reach: only a command handed to a shell counts, and a "
          "command that reached one is a finding whether the shell ran it or the harness declined it — "
          "each finding says which, read from the tool_result that repeats the call's tool_use id. %s "
          "(ROADMAP row 479)."
          % (CHECK, counting_from, window, root, RUN_GLOB, commands_read,
             "" if commands_read == 1 else "s",
             _open_sentence(history_phrase(len(history), counting_from))))
    if history:
        print("Outcomes across the history: %s." % outcome_tally(history))
    return 0


if __name__ == "__main__":
    sys.exit(main())
