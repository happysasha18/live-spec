"""A remote consumer of a private contract has no read grant (SPEC INV-232, ROADMAP 389, LAW arm).

The defect (the 2026-07-17 audit's finding 8): INV-187 sends a remote consumer to read the contract
"over git when remote" and cites [INV-112], whose home defines only a PUSH grant on the deposit path;
no READ grant is defined anywhere. tlvphotos is a private repo and the promoter↔site pair is the
expected first real consumer [row 385], so the first contract read across machines has no stated road.

This lands the LAW arm: the remote-seat law grows its read arm — what a consumer needs to read a
private repo over git, WHERE the grant is recorded (the host profile, beside the push grant [INV-82]),
and the honest grantless failure that NAMES the grant it lacks [INV-67]. The real cross-machine read is
field-gated (tied to rows 385/247) and not attempted here.

The tests drive fixture grant records — no repo is cloned.
"""
import importlib.util
import os

import pytest
from conftest import ROOT, read

MOD = os.path.join(ROOT, "scripts", "read-grant.py")
ASK = os.path.join(ROOT, "scripts", "read-grant-ask.md")


def _load():
    assert os.path.isfile(MOD), "scripts/read-grant.py missing"
    spec = importlib.util.spec_from_file_location("read_grant", MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- the mechanism ships, beside the push grant ask ---

def test_read_grant_ask_ships():
    # the read-direction sibling of scripts/grant-ask.md.
    assert os.path.isfile(ASK), "scripts/read-grant-ask.md missing"


# --- a consumer with the read grant recorded passes ---

def test_recorded_grant_passes_dict_shape():
    mod = _load()
    grants = {"owner/tlvphotos": {"kind": ["read"]}}
    line = mod.check_read_grant("owner/tlvphotos", grants)
    assert "owner/tlvphotos" in line


def test_recorded_grant_passes_list_shape():
    mod = _load()
    grants = [{"repo": "owner/tlvphotos", "kind": "read-and-write"}]
    line = mod.check_read_grant("owner/tlvphotos", grants)
    assert "owner/tlvphotos" in line


# --- a grantless consumer fails honestly, naming the grant it lacks ---

def test_grantless_consumer_fails_naming_the_grant():
    mod = _load()
    with pytest.raises(mod.ReadGrantMissing) as ei:
        mod.check_read_grant("owner/tlvphotos", {})
    msg = str(ei.value)
    # it names the missing grant and the one action, like the push grant ask.
    assert "owner/tlvphotos" in msg
    assert "read grant" in msg.lower()
    assert "trust.read-grant" in msg
    assert "read-grant-ask.md" in msg


def test_grant_for_another_repo_does_not_satisfy():
    mod = _load()
    grants = {"owner/other": {"kind": ["read"]}}
    with pytest.raises(mod.ReadGrantMissing):
        mod.check_read_grant("owner/tlvphotos", grants)


def test_has_read_grant_predicate():
    mod = _load()
    assert mod.has_read_grant("r", {"r": {"kind": ["read"]}}) is True
    assert mod.has_read_grant("r", {"r": {"kind": ["write"]}}) is True   # read+write can read
    assert mod.has_read_grant("r", {}) is False


# --- spec carries the LAW arm (and INV-187's read cites it) ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-232, INV-187]" in spec
    assert "| INV-232 |" in spec


def test_architecture_owns_the_invariant():
    assert "INV-232" in read("ARCHITECTURE.md")


def test_matrix_row_covers_the_law():
    assert "INV-232" in read("TEST_MATRIX.md")
