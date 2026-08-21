#!/usr/bin/env bash
# check-tests.sh — gate (b) of the push gate: the test suite must be fully green.
#
# This also covers gate (c), anchor ownership: tests/test_traceability.py already
# asserts every spec anchor is owned by exactly one architecture node
# (TestArchitecture::test_architecture_owns_every_anchor_once). A green suite run
# proves both gates in one pass — no separate anchor-ownership check exists here.
#
# Scoped runs (SPEC INV-45, ROADMAP row 362): when env SCOPED_TEST_FILES is non-empty
# (newline-separated test file paths), only those files run — the reach map's SCOPED verdict
# already proved this set covers the diff.
#
# Usage: check-tests.sh [tests-dir]
#   tests-dir defaults to "tests" (relative to the repo root, or an absolute path
#   for testing this gate against a scratch fixture without touching the real suite)
#   SCOPED_TEST_FILES (env, optional): newline-separated test file paths — run exactly these
#   instead of the whole tests-dir.
#
# An explicit tests-dir names its OWN repo root as its parent directory, never the ambient
# cwd's repo (tests/test_guardrails.py::TestGateB_Tests' scratch runs are the caller this
# protects): a caller that launches this script from inside the real, judged tree while
# pointing it at a scratch copy elsewhere must not have this script `cd` back into that judged
# tree and hand it, as the nested pytest process's inherited cwd, to every test the scratch
# copy runs — the same class of defect d747bcd fixed for docs/PROGRESS.md, one layer down.

set -euo pipefail

# A hook runs with git's own environment exported, and an inherited GIT_DIR outranks any
# `-C` a test passes: a fixture that builds its own little repository would commit into
# the repository being pushed instead. The suite starts from a clean git environment.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY \
      GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_QUARANTINE_PATH \
      GIT_PREFIX GIT_NAMESPACE

if [ -n "${1:-}" ]; then
  TESTS_DIR="$1"
  REPO_ROOT="$(cd "$(dirname "$TESTS_DIR")" && pwd)"
else
  REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  TESTS_DIR="tests"
fi
cd "$REPO_ROOT"

LOG="$(mktemp "${TMPDIR:-/tmp}/livespec-test-suite-log.XXXXXX")"
cleanup() { rm -f "$LOG"; }
trap cleanup EXIT

# The runner MUST match the CI mirror's (.github/workflows/gates.yml runs `python3 -m pytest -q`);
# the two nets share one runner or the local net is weaker than the second one (SPEC M-5, M-154);
# unittest discover cannot collect the plain-function pytest-style tests (fixtures like monkeypatch/
# tmp_path), so it silently under-runs and false-greens — the exact hole that let a red reach CI.
if [ -n "${SCOPED_TEST_FILES:-}" ]; then
  scoped_count=0
  scoped_list=()
  while IFS= read -r t; do
    [ -z "$t" ] && continue
    scoped_list+=("$t")
    scoped_count=$((scoped_count + 1))
  done <<< "$SCOPED_TEST_FILES"

  set +e
  python3 -m pytest -q "${scoped_list[@]}" 2>&1 | tee "$LOG"
  status="${PIPESTATUS[0]}"
  set -e

  if [ "$status" -eq 0 ]; then
    echo "OK (tests): scoped suite green ($scoped_count files, reach-scoped per SPEC INV-45)."
    exit 0
  else
    echo "FAIL (tests): scoped suite is not green ($scoped_count files)."
    echo "  Fix: run 'python3 -m pytest -q' on the scoped files and repair the failing test(s)."
    exit 1
  fi
fi

set +e
python3 -m pytest -q "$TESTS_DIR" 2>&1 | tee "$LOG"
status="${PIPESTATUS[0]}"
set -e

if [ "$status" -ne 0 ]; then
  echo "FAIL (tests): suite is not green ($TESTS_DIR)."
  echo "  Fix: run 'python3 -m pytest -q tests' and repair the failing test(s) before pushing."
  exit 1
fi

echo "OK (tests): suite green ($TESTS_DIR) — also covers anchor ownership (gate c)."

exit 0
