#!/usr/bin/env python3
"""wind-down.py — one command that safely winds down all the work before you leave (PLAN q-235).

Source: owner 2026-07-10 ~13:30, from a cafe. "One command halts every running worker, writes
each one's checkpoint to disk, gets what is unpushed off the machine, and prints a single closing
line saying what is safe and what is still open."

WHAT COUNTS AS A "RUNNING WORKER" HERE. This project already has one on-disk signal for "a
process is actively using this tree": `git worktree lock`, which every agent worktree under
`.claude/worktrees/` carries with a reason string of the shape
`claude agent <name> (pid <PID> start <timestamp>)` (see `git worktree list --porcelain` on this
repo). Rather than inventing a second registry of live processes, this command reads that one:
every LOCKED worktree `git worktree list --porcelain` reports is a worker to wind down. A worktree
with no lock (the tree a person is standing in) is left alone.

SAFETY GUARD — never signal your own controlling process. The lock reason's pid is not
necessarily a distinct child process: several worktrees in this repo share one pid, the harness
process that is itself running whichever session invokes this command. Sending that process
SIGTERM would end the very session running wind-down, mid-command — the opposite of "safely".
Before signaling anything, this script reads its own ancestor chain (`ps -eo pid=,ppid=`, walked
from `os.getpid()`) and refuses to signal any pid found there. Such a worktree is reported as
still OPEN ("could not be safely signaled — it is this session's own controlling process"), never
silently skipped and never force-killed.

WHAT "CHECKPOINT" MEANS HERE. This project already has one mechanical checkpoint format,
`scripts/checkpoint.py` (`.live-spec/checkpoints/*.md`, DONE / IN PROGRESS / NEXT sections). This
command reuses it rather than writing a second free-form format: for every locked worktree it
writes (or, on a second run, updates in place) `.live-spec/checkpoints/wind-down-<branch>.md`
recording the worktree's path, branch, HEAD, uncommitted-file count, and the outcome of the
signal attempt — enough for a later session to see what was in flight there without re-deriving
it from `git worktree list`.

WHAT "GETS WHAT IS UNPUSHED OFF THE MACHINE" MEANS HERE. It never bypasses the push gate. If the
current branch has unpushed commits (`@{u}..HEAD`), this command runs `guardrails/pre-push` (if
the target tree has one) and pushes ONLY if that gate exits 0. No gate script present is treated
the same as a red gate — withheld, not pushed — because absence of a check is not evidence of
safety. A branch with no upstream configured is reported openly; this command does not guess
what "unpushed" would mean for it.

SCOPE, DELIBERATELY NARROW. This command does not delete, prune, or unlock any worktree (removing
a lock or a tree is a separate, more destructive operation the acceptance never asked for) and it
is never wired into a hook or gate — it is a standalone command a person or session runs
deliberately, the first time Alexander says he is leaving (see PLAN.md q-235's own words).
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))
import checkpoint as checkpoint_lib  # scripts/checkpoint.py — the one checkpoint format

SIGNAL_WAIT_SECONDS = 5.0
SIGNAL_POLL_INTERVAL = 0.2

_PID_RE = re.compile(r"\(pid (\d+)")


# ---------------------------------------------------------------- small process/git helpers

def _run(cmd, cwd=None, input_text=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, input=input_text)


def _git(repo, *args):
    return _run(["git", "-C", str(repo)] + list(args))


def pid_alive(pid) -> bool:
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError, PermissionError):
        return False
    # kill(pid, 0) succeeds for a zombie too -- a child that has already exited but whose
    # real parent has not reaped it yet. This command is rarely that real parent, so it
    # would otherwise have no way to ever observe such a worker as stopped. A zombie has
    # already exited; treat it as stopped, not alive.
    stat = _run(["ps", "-o", "stat=", "-p", str(pid)]).stdout.strip()
    if stat.startswith("Z"):
        return False
    return True


def build_ancestor_set(pid: int) -> set:
    """This process's own ancestor pids, read once from `ps -eo pid=,ppid=`.

    Used only for the self-guard above: a pid found here is never signaled, whatever its
    worktree lock claims about it.
    """
    ancestors = set()
    try:
        out = _run(["ps", "-eo", "pid=,ppid="]).stdout
    except Exception:
        return ancestors
    table = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        try:
            p, pp = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        table[p] = pp
    cur = pid
    seen = set()
    while cur in table and cur not in seen and cur not in (0, 1):
        seen.add(cur)
        parent = table[cur]
        ancestors.add(parent)
        cur = parent
    return ancestors


# ---------------------------------------------------------------- worktree discovery

def parse_worktrees(repo) -> list:
    """Every worktree `git worktree list --porcelain` reports, each as a dict with
    path/head/branch/locked/lock_reason/detached."""
    result = _git(repo, "worktree", "list", "--porcelain")
    entries = []
    current = None
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            if current is not None:
                entries.append(current)
            current = {
                "path": line[len("worktree "):],
                "head": None,
                "branch": None,
                "locked": False,
                "lock_reason": "",
                "detached": False,
            }
        elif current is None:
            continue
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD "):]
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):]
        elif line == "detached":
            current["detached"] = True
        elif line == "locked" or line.startswith("locked "):
            current["locked"] = True
            current["lock_reason"] = line[len("locked"):].strip()
    if current is not None:
        entries.append(current)
    return entries


def extract_pid(lock_reason: str):
    m = _PID_RE.search(lock_reason or "")
    return int(m.group(1)) if m else None


def signal_worker(pid, ancestor_pids: set):
    """Best-effort, safe stop of one worker pid. Returns (outcome, detail).

    outcome is one of: already-stopped, self-guard, stopped, still-running, signal-failed,
    unknown-pid. Only "already-stopped" and "stopped" count as safely closed.
    """
    if pid is None:
        return "unknown-pid", "lock reason carried no '(pid N)' — nothing this command could signal"
    if not pid_alive(pid):
        return "already-stopped", "pid %d is not running" % pid
    if pid in ancestor_pids:
        return (
            "self-guard",
            "pid %d is this session's own controlling process — signaling it would end the "
            "session running this command, so it was left running on purpose" % pid,
        )
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as exc:
        return "signal-failed", "SIGTERM to pid %d failed: %s" % (pid, exc)
    deadline = time.time() + SIGNAL_WAIT_SECONDS
    while time.time() < deadline:
        if not pid_alive(pid):
            return "stopped", "pid %d signaled with SIGTERM and exited" % pid
        time.sleep(SIGNAL_POLL_INTERVAL)
    return "still-running", "pid %d did not exit within %.0fs of SIGTERM" % (pid, SIGNAL_WAIT_SECONDS)


# ---------------------------------------------------------------- checkpointing

def _sanitize(label: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", label).strip("-")
    return cleaned or "worktree"


def checkpoint_path_for(repo, worktree: dict) -> Path:
    label = (worktree.get("branch") or worktree.get("head") or worktree["path"]).replace(
        "refs/heads/", ""
    )
    return Path(repo) / ".live-spec" / "checkpoints" / ("wind-down-%s.md" % _sanitize(label))


def write_checkpoint(repo, worktree: dict, outcome: str, detail: str, timestamp: str) -> Path:
    path = checkpoint_path_for(repo, worktree)
    branch = (worktree.get("branch") or "").replace("refs/heads/", "") or "(detached)"

    status = _git(worktree["path"], "status", "--porcelain")
    dirty = None
    if status.returncode == 0:
        dirty = len([line for line in status.stdout.splitlines() if line.strip()])

    in_progress_lines = [
        "- worktree: %s" % worktree["path"],
        "- branch: %s" % branch,
        "- HEAD: %s" % (worktree.get("head") or "?"),
    ]
    if dirty is not None:
        in_progress_lines.append("- uncommitted files at wind-down: %d" % dirty)
    in_progress = "\n".join(in_progress_lines)

    next_body = (
        "wind-down %s: %s (%s). If this branch still carries unmerged work, resume with "
        "`cd %s`." % (timestamp, outcome, detail, worktree["path"])
    )

    if not path.exists():
        checkpoint_lib.new_checkpoint(
            path, title="wind-down record -- %s" % branch, owner="wind-down (automated)"
        )
    checkpoint_lib.update_checkpoint(path, in_progress=in_progress, next=next_body)
    return path


# ---------------------------------------------------------------- push

def unpushed_count(repo):
    r = _git(repo, "rev-list", "--count", "@{u}..HEAD")
    if r.returncode != 0:
        return None  # no upstream configured — nothing this command can verify
    try:
        return int(r.stdout.strip())
    except ValueError:
        return None


def run_push_gate(repo):
    gate = Path(repo) / "guardrails" / "pre-push"
    if not gate.exists():
        return None, "no guardrails/pre-push in this tree"
    r = _run(["bash", str(gate)], cwd=str(repo), input_text="")
    return r.returncode, (r.stdout + r.stderr)


def do_push(repo) -> dict:
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    n = unpushed_count(repo)
    if n is None:
        return {
            "status": "no-upstream",
            "count": None,
            "detail": "branch %s has no upstream configured — nothing this command can verify "
            "as pushed" % branch,
        }
    if n == 0:
        return {"status": "clean", "count": 0, "detail": "branch %s already matches its upstream" % branch}

    gate_code, gate_output = run_push_gate(repo)
    if gate_code is None:
        return {
            "status": "no-gate",
            "count": n,
            "detail": "no guardrails/pre-push found to verify push-readiness — %d commit(s) "
            "left unpushed rather than bypassing the gate" % n,
        }
    if gate_code != 0:
        return {
            "status": "gate-red",
            "count": n,
            "detail": "guardrails/pre-push exited %d — %d commit(s) left unpushed, gate not "
            "bypassed" % (gate_code, n),
        }

    push_r = _git(repo, "push")
    if push_r.returncode != 0:
        return {
            "status": "push-failed",
            "count": n,
            "detail": "git push failed: %s" % (push_r.stderr.strip() or push_r.stdout.strip()),
        }
    return {"status": "pushed", "count": n, "detail": "%d commit(s) pushed from branch %s" % (n, branch)}


# ---------------------------------------------------------------- orchestration

def wind_down(repo) -> tuple:
    """Runs the whole wind-down over `repo`. Returns (exit_code, summary_line, full_output)."""
    lines = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ancestor_pids = build_ancestor_set(os.getpid())

    worktrees = parse_worktrees(repo)
    locked = [w for w in worktrees if w["locked"]]

    worker_results = []
    for w in locked:
        pid = extract_pid(w["lock_reason"])
        outcome, detail = signal_worker(pid, ancestor_pids)
        cpath = write_checkpoint(repo, w, outcome, detail, timestamp)
        worker_results.append({"worktree": w, "pid": pid, "outcome": outcome, "detail": detail, "checkpoint": cpath})
        lines.append("worker %s: %s (%s) -- checkpoint: %s" % (w["path"], outcome, detail, cpath))

    push_result = do_push(repo)
    lines.append("push: %s -- %s" % (push_result["status"], push_result["detail"]))

    closed_outcomes = ("stopped", "already-stopped")
    open_workers = [r for r in worker_results if r["outcome"] not in closed_outcomes]
    closed_workers = [r for r in worker_results if r["outcome"] in closed_outcomes]

    safe_bits = []
    open_bits = []

    if not worker_results:
        safe_bits.append("workers: none locked")
    else:
        if closed_workers:
            safe_bits.append("workers: %d halted & checkpointed" % len(closed_workers))
        if open_workers:
            open_bits.append(
                "workers: %d still open (%s)"
                % (
                    len(open_workers),
                    "; ".join("%s: %s" % (r["worktree"]["path"], r["detail"]) for r in open_workers),
                )
            )

    if push_result["status"] in ("pushed", "clean"):
        safe_bits.append("push: %s" % push_result["detail"])
    else:
        open_bits.append("push: %s" % push_result["detail"])

    ok = not open_bits
    if ok:
        summary = "WIND-DOWN: SAFE -- %s. OPEN -- none." % "; ".join(safe_bits)
    else:
        safe_part = "; ".join(safe_bits) if safe_bits else "nothing yet"
        summary = "WIND-DOWN: SAFE -- %s. OPEN -- %s." % (safe_part, "; ".join(open_bits))

    lines.append(summary)
    return (0 if ok else 1), summary, "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Halt every locked worktree, checkpoint it, push what's safe, and print "
        "one closing line saying what is safe and what is still open (PLAN q-235)."
    )
    parser.add_argument("--repo", default=None, help="repo root to act on (default: current repo)")
    args = parser.parse_args(argv)

    repo = args.repo
    if repo is None:
        r = _git(".", "rev-parse", "--show-toplevel")
        if r.returncode != 0:
            print("WIND-DOWN: ERROR -- not inside a git repository and no --repo given", file=sys.stderr)
            return 2
        repo = r.stdout.strip()
    repo = str(Path(repo).resolve())

    exit_code, _summary, full_output = wind_down(repo)
    print(full_output)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
