"""guardrails/check-status-view-drift.py — a host's vendored pack files must not drift from the
pack (row q-818). The check reads the two files, not a record about them: it never trusts the
sha256 the manifest carries. Every fault case is proved red before the pass case is trusted.
"""
import json
import os
import subprocess

from conftest import ROOT

GATE = os.path.join(ROOT, "guardrails", "check-status-view-drift.py")


def _gate(host_root, pack_root=None):
    args = ["python3", GATE, host_root]
    if pack_root is not None:
        args += ["--pack-root", pack_root]
    return subprocess.run(args, capture_output=True, text=True)


def _make_pack(tmp_path, contents="#!/bin/bash\necho hi\n"):
    pack_root = tmp_path / "pack"
    (pack_root / "scaffold" / "status-view").mkdir(parents=True)
    (pack_root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (pack_root / "scaffold" / "status-view" / "state-probe.sh").write_text(
        contents, encoding="utf-8")
    return pack_root


def _make_host(tmp_path, pack_root, contents="#!/bin/bash\necho hi\n"):
    host_root = tmp_path / "host"
    (host_root / "scripts").mkdir(parents=True)
    (host_root / "scripts" / "state-probe.sh").write_text(contents, encoding="utf-8")
    manifest = {
        "pack_version": "1.0.0",
        "vendored": {"scaffold/status-view/state-probe.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    return host_root


def test_red_first_one_line_changed(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host(tmp_path, pack_root, contents="#!/bin/bash\necho HACKED\n")
    result = _gate(str(host_root), str(pack_root))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "scripts/state-probe.sh" in result.stdout
    assert "differs from the pack's own copy" in result.stdout


def test_green_after_the_red_when_byte_identical(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host(tmp_path, pack_root)  # same contents as the pack
    result = _gate(str(host_root), str(pack_root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no drift" in result.stdout


def test_no_manifest_stands_down(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = tmp_path / "bare-host"
    host_root.mkdir()
    result = _gate(str(host_root), str(pack_root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "carries no scripts/ratchet-manifest.json" in result.stdout


def test_pack_not_on_this_machine_stands_down(tmp_path):
    host_root = _make_host(tmp_path, tmp_path / "nonexistent-pack")
    result = _gate(str(host_root), str(tmp_path / "nonexistent-pack"))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "nothing to diff against" in result.stdout


def test_manifest_entry_missing_from_host_faults(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = tmp_path / "partial-host"
    (host_root / "scripts").mkdir(parents=True)
    manifest = {
        "pack_version": "1.0.0",
        "vendored": {"scaffold/status-view/state-probe.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    result = _gate(str(host_root), str(pack_root))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "is missing" in result.stdout
