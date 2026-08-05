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

WHAT IT DOES NOT SEE. It reads no prose. A worker report, a brief, or a plan that NAMES a restore is
left alone — only a command the worker actually handed to a shell counts, and only when the segment's
first word is `git`, so the same text quoted inside a `grep` pattern stays silent. It reads the
parent session's own transcript for nothing: a main-thread session that restores its own tree is the
orchestrator acting, which the rule allows. It cannot tell whether the worker ran inside its own
isolated worktree; that case reds like any other, which is the scope the clause states.

WHERE IT PLACES A FINDING. A command string is read left to right for a moving effective directory,
starting at the record's own cwd: a `cd <path>` moves it (`cd -`, `pushd` and `popd` move it to
UNKNOWN, since the gate does not track a directory stack), a plain literal assignment earlier in the
same string (`S=/some/path`) is remembered so a later `cd $S/sub` still resolves, and a `git -C <path>`
sets the directory for that one invocation only, without moving the running one. A target built from
anything the gate cannot read statically — an unassigned variable, a subshell, command substitution —
sets the effective directory to UNKNOWN. A forbidden git command reds when it ran at the record's cwd
with no `cd` in between, as it always has, or when it ran at a known directory whose enclosing git
repository still exists on disk at scan time (walking up from it for a `.git`); a known directory gone
from disk, or holding no enclosing repository, is not a finding, and an UNKNOWN effective directory
reds, since the gate can place it no better than a record with no timestamp. Each finding's report
line names the effective directory beside the session's recorded cwd.

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

THE STAND-DOWN. When the transcript root does not exist, this host keeps no transcripts where the
gate looks. The gate stands down, says so by name, and exits 0 — a stated stand-down rather than a
silent pass. When the root DOES exist but holds no worker-run transcript at all, the layout the gate
reads has moved and the check would report clean while testing nothing; that is the vacuous pass
guardrails/nonempty_input.py names, and it reds by name (SPEC INV-218). The time window is applied
after that check, and a window holding no worker run is legitimate — a session may spawn no worker —
so an empty WINDOW is declared here as a permitted empty set and reports OK naming the window.

Usage:
  check-worker-restore.py [--root PATH] [--since-hours H] [--all] [--counting-from YYYY-MM-DD]
Exit 0 when no worker run discarded working-tree changes since the counting start, 1 otherwise.
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

# The day the gate began counting. Every worker run stamped before it is history: the clause was
# written on 2026-07-27 and the machine's transcripts hold runs from before it, so a gate that red on
# them would have been switched off rather than obeyed. History is counted and named in every verdict
# line, and reds nothing. The date moves forward only with a recorded reason, and moving it forward
# hides findings — read the history first with `--counting-from 2000-01-01 --all`.
COUNTING_FROM = "2026-07-28"

# The segment separators a shell command line is cut on, so `cd x && git restore y` is read as its
# own invocation. The pipe is included: `yes | git clean -fd` is still git clean.
SEPARATORS = ("&&", "||", ";", "|", "\n")

WHOLE_TREE = "the whole working tree"


def _segments(command):
    """The command line cut into invocations. Plain string surgery, no shell."""
    out = [command]
    for sep in SEPARATORS:
        nxt = []
        for part in out:
            nxt.extend(part.split(sep))
        out = nxt
    return [p.strip() for p in out if p.strip()]


def _tokens(segment):
    """The segment's words. shlex keeps a quoted phrase as ONE token, which is what keeps a
    `grep 'git restore'` pattern from reading as a git invocation."""
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def _git_args(segment):
    """The arguments of a git invocation, or None when this segment is not one.

    A segment is a git invocation only when its first word — past leading `VAR=value` assignments —
    is exactly `git`. git's own pre-command options (`-C <path>`, `-c <k=v>`, `--git-dir=…`) are
    stepped over so the subcommand is the first thing returned.
    """
    tokens = _tokens(segment)
    while tokens and "=" in tokens[0] and not tokens[0].startswith("-"):
        head = tokens[0].split("=", 1)[0]
        if head and all(c.isalnum() or c == "_" for c in head):
            tokens = tokens[1:]
        else:
            break
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
    tokens = _tokens(segment)
    while tokens and "=" in tokens[0] and not tokens[0].startswith("-"):
        head = tokens[0].split("=", 1)[0]
        if head and all(c.isalnum() or c == "_" for c in head):
            tokens = tokens[1:]
        else:
            break
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


def classify(command, cwd):
    """The discarding invocations in one shell command line, each placed in the directory it
    really ran in.

    Walks the command's own segments in order, holding an effective directory that starts at
    `cwd` and moves with each `cd` (see `_resolve_dir`) and a running map of the plain literal
    variable assignments the command made along the way, so `S=/tmp/x` earlier in the same
    string lets a later `cd $S/sub` still resolve. A `git -C <path>` sets the directory for
    that one invocation only. A forbidden git command reds when it ran at `cwd` with no `cd`
    in between (the gate's original, unconditional read), or at a known directory whose
    enclosing git repository still exists on disk at scan time; a known directory gone from
    disk or holding no enclosing repository is not a finding, and an UNKNOWN effective
    directory reds, since the gate can place it no better than an unstamped record.

    Returns a list of {"command": <the segment>, "which": <the named form>, "paths": [...],
    "effective_dir": <the directory the command ran in, or None for UNKNOWN>}. An empty list
    means the line discards nothing this gate reds on.
    """
    found = []
    env = {}
    effective_dir = cwd
    for segment in _segments(command):
        assignment = _var_assignment(segment)
        if assignment is not None:
            env[assignment[0]] = assignment[1]
            continue

        tokens = _tokens(segment)
        if tokens and tokens[0] == "cd":
            target = tokens[1] if len(tokens) > 1 else None
            effective_dir = None if target == "-" else _resolve_dir(_substitute(target, env), effective_dir)
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
    """Every Bash command a worker run handed to a shell, with the record that names the run."""
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
                    out.append((command, rec))
    return out


def scan(paths):
    """The findings across a set of worker-run transcripts, each naming command, path, and run."""
    findings = []
    commands_read = 0
    for path in paths:
        for command, rec in _bash_commands(path):
            commands_read += 1
            cwd = rec.get("cwd")
            for hit in classify(command, cwd):
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
                })
    return findings, commands_read


def is_history(finding, counting_from):
    """True when the run's record is stamped before the counting start.

    The stamp is the harness's ISO-8601 timestamp, so its first ten characters are the date and
    compare as text. A record carrying no stamp is never history: the gate cannot place it in time,
    and an unplaceable finding is read as a new one.
    """
    at = finding.get("at") or ""
    if len(at) < 10 or not at[:4].isdigit():
        return False
    return at[:10] < counting_from


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
                        help="the day the gate starts counting; a finding stamped before it is "
                             "carried as history (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    counting_from = args.counting_from.strip()
    parts = counting_from.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts) or len(parts[0]) != 4:
        print("%s: --counting-from reads %r, and the gate reads a date written YYYY-MM-DD."
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
        for f in current:
            print("%s: %s ran `%s` — %s, discarding every uncommitted change under %s, including bytes "
                  "the run never wrote and its brief never named (ROADMAP row 479)."
                  % (CHECK, f["agent"], f["command"], f["which"], ", ".join(f["paths"])))
            print("    run     : %s" % f["run"])
            ran_in = f.get("effective_dir")
            ran_in = ran_in if ran_in is not None else "UNKNOWN (a cd target the gate could not read statically)"
            print("    session : %s   cwd: %s   ran in: %s   at: %s"
                  % (f["session"], f["cwd"], ran_in, f["at"]))
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
        print("Reach: %s under %s, %d command line%s read; %s."
              % (window, root, commands_read, "" if commands_read == 1 else "s",
                 history_phrase(len(history), counting_from)))
        first = current[0]
        print(json.dumps({
            "severity": "error",
            "code": "worker-restore",
            "message": ("a worker run discarded working-tree changes: %s ran `%s` against %s in %s "
                        "(ROADMAP row 479)"
                        % (first["agent"], first["command"], ", ".join(first["paths"]), first["run"])),
            "fix": ("a worker restores a file it mutated by writing its own saved bytes back, and halts "
                    "and reports when a file needs a git-level restore — the orchestrator owns recovery"),
        }))
        return 1

    print("OK (%s): no worker run discarded working-tree changes since %s. Read %s under %s — the files "
          "matching %s, one per worker run — taking every assistant record's Bash tool_use command "
          "field (%d command line%s) and reading each git invocation's subcommand and flags for "
          "git checkout -- and git checkout ., git restore outside --staged, git stash and its push, "
          "save, create and store forms, git reset with --hard, --merge or --keep, and git clean with "
          "-f or -x. Report prose is outside the reach: only a command handed to a shell counts. %s "
          "(ROADMAP row 479)."
          % (CHECK, counting_from, window, root, RUN_GLOB, commands_read,
             "" if commands_read == 1 else "s",
             _open_sentence(history_phrase(len(history), counting_from))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
