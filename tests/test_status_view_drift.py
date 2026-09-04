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


# ---------------------------------------------------------------------------------------------
# F1 — the pack's own pair, checked directly, no manifest needed: the repo being checked IS the
# pack (it carries a VERSION file at its root), so criterion 2's byte-identity is proved at every
# push from this repository even though the pack ships no ratchet-manifest.json of its own.

def _make_pack_shaped_repo(tmp_path, scaffold_contents="#!/bin/bash\necho hi\n",
                            vendored_contents=None):
    root = tmp_path / "pack-shaped"
    (root / "scaffold" / "status-view").mkdir(parents=True)
    (root / "scripts").mkdir(parents=True)
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (root / "scaffold" / "status-view" / "state-probe.sh").write_text(
        scaffold_contents, encoding="utf-8")
    (root / "scripts" / "state-probe.sh").write_text(
        vendored_contents if vendored_contents is not None else scaffold_contents,
        encoding="utf-8")
    return root


def test_the_packs_own_pair_reds_when_the_two_copies_differ(tmp_path):
    root = _make_pack_shaped_repo(tmp_path, vendored_contents="#!/bin/bash\necho DRIFTED\n")
    result = _gate(str(root))  # no manifest, no --pack-root — the repo checked IS the pack
    assert result.returncode == 1, result.stdout + result.stderr
    assert "scripts/state-probe.sh" in result.stdout
    assert "differs from the pack's own copy" in result.stdout


def test_the_packs_own_pair_passes_when_byte_identical(tmp_path):
    root = _make_pack_shaped_repo(tmp_path)
    result = _gate(str(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no drift" in result.stdout


# ---------------------------------------------------------------------------------------------
# F2 — a host reaches the pack through its own manifest's recorded pack root, with no --pack-root
# needed at its push gate.

def _make_host_with_recorded_pack_root(tmp_path, pack_root, contents="#!/bin/bash\necho hi\n"):
    host_root = tmp_path / "host-with-recorded-pack-root"
    (host_root / "scripts").mkdir(parents=True)
    (host_root / "scripts" / "state-probe.sh").write_text(contents, encoding="utf-8")
    manifest = {
        "pack_version": "1.0.0",
        "pack_root": str(pack_root),
        "vendored": {"scaffold/status-view/state-probe.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    return host_root


def test_a_hosts_recorded_pack_root_is_found_with_no_flag_and_reds_on_drift(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host_with_recorded_pack_root(tmp_path, pack_root,
                                                    contents="#!/bin/bash\necho HACKED\n")
    result = _gate(str(host_root))  # no --pack-root — read from the manifest instead
    assert result.returncode == 1, result.stdout + result.stderr
    assert "differs from the pack's own copy" in result.stdout


def test_a_hosts_recorded_pack_root_passes_when_byte_identical(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host_with_recorded_pack_root(tmp_path, pack_root)
    result = _gate(str(host_root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no drift" in result.stdout


def test_explicit_pack_root_still_wins_over_the_recorded_one(tmp_path):
    recorded_pack = _make_pack(tmp_path, contents="#!/bin/bash\necho RECORDED\n")
    real_pack = tmp_path / "real-pack"
    (real_pack / "scaffold" / "status-view").mkdir(parents=True)
    (real_pack / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (real_pack / "scaffold" / "status-view" / "state-probe.sh").write_text(
        "#!/bin/bash\necho hi\n", encoding="utf-8")
    host_root = _make_host_with_recorded_pack_root(tmp_path, recorded_pack)
    result = _gate(str(host_root), pack_root=str(real_pack))
    assert result.returncode == 0, result.stdout + result.stderr


def _make_host_with_relative_pack_root(tmp_path, pack_root, contents="#!/bin/bash\necho hi\n"):
    """R12: the manifest carries pack_root relative to the host root — the form
    adopt/install-status-view.sh writes for the ordinary sibling layout."""
    host_root = tmp_path / "host-with-relative-pack-root"
    (host_root / "scripts").mkdir(parents=True)
    (host_root / "scripts" / "state-probe.sh").write_text(contents, encoding="utf-8")
    manifest = {
        "pack_version": "1.0.0",
        "pack_root": os.path.relpath(str(pack_root), str(host_root)),
        "vendored": {"scaffold/status-view/state-probe.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    return host_root


def test_a_relative_recorded_pack_root_resolves_against_the_host_and_finds_drift(tmp_path):
    """R12: a relative pack_root is resolved against the host root, not this process's own cwd —
    the gate is invoked from ROOT (via subprocess's default cwd), a directory that shares no
    relative path with either tmp tree, so a cwd-relative resolution would miss the pack
    entirely."""
    pack_root = _make_pack(tmp_path)
    host_root = _make_host_with_relative_pack_root(
        tmp_path, pack_root, contents="#!/bin/bash\necho HACKED\n")
    result = _gate(str(host_root))  # no --pack-root — read the relative recorded one
    assert result.returncode == 1, result.stdout + result.stderr
    assert "differs from the pack's own copy" in result.stdout


def test_a_relative_recorded_pack_root_passes_when_byte_identical(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host_with_relative_pack_root(tmp_path, pack_root)
    result = _gate(str(host_root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no drift" in result.stdout


def test_a_recorded_pack_root_not_on_this_machine_stands_down_honestly(tmp_path):
    host_root = _make_host_with_recorded_pack_root(tmp_path, tmp_path / "nonexistent-pack")
    result = _gate(str(host_root))  # no --pack-root
    assert result.returncode == 0, result.stdout + result.stderr
    assert "nothing to diff against" in result.stdout


# ---------------------------------------------------------------------------------------------
# R1 — a `VERSION` file is an ordinary thing for a host project to carry too; it is not a
# property of this pack, and the pack pole must not fire for a host that happens to have one. The
# repo is the pack only when it carries the shipped source itself. A comparison that resolves
# nothing must never print as a clean pass either.

def test_a_host_carrying_a_version_file_still_reds_on_a_genuinely_drifted_copy(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = _make_host_with_recorded_pack_root(
        tmp_path, pack_root, contents="#!/bin/bash\necho HACKED\n")
    (host_root / "VERSION").write_text("2.0.0\n", encoding="utf-8")  # the host versions itself too
    result = _gate(str(host_root))  # no --pack-root — read the recorded one
    assert result.returncode == 1, result.stdout + result.stderr
    assert "scripts/state-probe.sh" in result.stdout
    assert "differs from the pack's own copy" in result.stdout


def test_a_resolved_root_that_is_not_the_pack_stands_down_rather_than_comparing(tmp_path):
    """R1's own leftover: the resolved pack_root was still validated by asking whether it carries
    a `VERSION` file, the exact question R1 threw out for the other pole. Here the recorded root
    is another HOST of the pack — it carries a VERSION file and its own vendored
    scripts/render-board.sh, coincidentally byte-identical to this host's own copy — but it is not
    the pack itself: it has no scaffold/status-view/ kit of its own. A VERSION-only check would
    treat it as the pack, compare the one entry that happens to resolve, and print a false clean
    pass; the check must stand down honestly instead of comparing against this unintended
    checkout."""
    not_the_pack = tmp_path / "another-host"
    (not_the_pack / "scripts").mkdir(parents=True)
    (not_the_pack / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (not_the_pack / "scripts" / "render-board.sh").write_text("#!/bin/bash\necho same\n",
                                                               encoding="utf-8")

    host_root = tmp_path / "host-with-wrong-recorded-root"
    (host_root / "scripts").mkdir(parents=True)
    (host_root / "scripts" / "render-board.sh").write_text("#!/bin/bash\necho same\n",
                                                             encoding="utf-8")
    manifest = {
        "pack_version": "1.0.0",
        "pack_root": str(not_the_pack),
        "vendored": {"scripts/render-board.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")

    result = _gate(str(host_root))  # no --pack-root — read the recorded, wrong root
    assert result.returncode == 0, result.stdout + result.stderr
    assert "nothing to diff against" in result.stdout
    assert "no drift" not in result.stdout


def test_a_host_pole_that_resolves_nothing_never_prints_a_clean_pass(tmp_path):
    pack_root = _make_pack(tmp_path)
    host_root = tmp_path / "host-nothing-resolves"
    (host_root / "scripts").mkdir(parents=True)
    manifest = {
        "pack_version": "1.0.0",
        "vendored": {"scaffold/status-view/does-not-exist.sh": "deadbeef" * 8},
    }
    (host_root / "scripts" / "ratchet-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    result = _gate(str(host_root), str(pack_root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no drift" not in result.stdout
    assert "0 vendored file(s) checked" not in result.stdout
