"""INV-178 — version is one fact: every skill inherits the pack VERSION, the stamp writes it.

Ten skills carried ten unrelated hand-rolled versions (1.0.0 through 1.1.4) while the pack was
2.0.0 — a per-skill number drifts the moment attention does, and a prover record naming the
skill version that ran the pass named a number nobody maintained. The root VERSION file is the
one home; frontmatter versions and in-text base references are stamped copies, held here.
"""
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = open(os.path.join(REPO, "VERSION"), encoding="utf-8").read().strip()


def _is_external_clone(skill_dir):
    """A skill dir holding its own .git is another project's canonical clone.

    install.sh, scripts/sync-skills.sh and the INV-243 config-health arm all carry this same
    probe. The pack VERSION is this repo's one fact about ITSELF; an external skill carries its
    own release number from its own repo (product-prover ships 1.3.0 while the pack is 5.0.0),
    and neither this law nor its stamper has any authority over that file.
    """
    return os.path.exists(os.path.join(skill_dir, ".git"))


def _skills():
    d = os.path.join(REPO, "skills")
    for name in sorted(os.listdir(d)):
        if _is_external_clone(os.path.join(d, name)):
            continue
        p = os.path.join(d, name, "SKILL.md")
        if os.path.isfile(p):
            yield name, open(p, encoding="utf-8").read()


def test_every_skill_frontmatter_version_equals_pack_version():
    for name, body in _skills():
        m = re.search(r"^  version: (\S+)$", body, flags=re.M)
        assert m, "%s: no frontmatter version line" % name
        assert m.group(1) == VERSION, "%s: version %s, pack %s" % (name, m.group(1), VERSION)


def test_every_base_reference_equals_pack_version():
    rx = re.compile(r"`live-spec-base` \(v(\d+\.\d+\.\d+)\)")
    for name, body in _skills():
        for got in rx.findall(body):
            assert got == VERSION, "%s: base reference v%s, pack %s" % (name, got, VERSION)


def test_spec_states_the_law():
    spec = open(os.path.join(REPO, "PRODUCT_SPEC.md"), encoding="utf-8").read()
    assert "version is one fact" in spec
    assert "| INV-178 |" in spec


def test_the_law_reaches_every_pack_owned_skill_and_no_external_clone():
    """The fence narrows this law to what the pack owns — and must narrow it no further.

    Read both ways: every pack-owned SKILL.md is still held (a fence that quietly emptied the
    law would leave the two assertions above with nothing to check), and any skill dir carrying
    its own .git is out of reach. On a bare checkout with no external clone the second half is
    vacuous by construction, which is the point — the stamper's own fence is proven hermetically
    below, so this pair never depends on the clone being installed to mean something.
    """
    d = os.path.join(REPO, "skills")
    held = {name for name, _ in _skills()}
    assert held, "the fence must not empty the law: no pack-owned skill left to hold"
    for name in sorted(os.listdir(d)):
        if not os.path.isfile(os.path.join(d, name, "SKILL.md")):
            continue
        if _is_external_clone(os.path.join(d, name)):
            assert name not in held, "%s carries its own .git: not this pack's fact to stamp" % name
        else:
            assert name in held, "%s is pack-owned and must stay held by the one-fact law" % name


def test_stamp_versions_cannot_rewrite_an_external_skill_clone():
    """Red-first fence: the stamper walked skills/ blind and would rewrite another repo's file.

    scripts/stamp-versions.py rewrote every skills/*/SKILL.md whose frontmatter matched, with no
    external-skill fence — so a bump ran on this machine silently restamped the installed
    product-prover clone (its own 1.3.0 overwritten with the pack's number), a write into a
    project this repo does not own and cannot release. Hermetic, in install.sh's exact idiom: a
    tmp layout with one pack-owned skill and one dir carrying a planted .git; the script finds
    its own skills dir from its own location, so the real clone is never needed and never read.
    """
    with tempfile.TemporaryDirectory() as tmp:
        scripts_dir = os.path.join(tmp, "scripts")
        os.makedirs(scripts_dir)
        script = os.path.join(scripts_dir, "stamp-versions.py")
        with open(os.path.join(REPO, "scripts", "stamp-versions.py"), "rb") as f:
            body = f.read()
        with open(script, "wb") as f:
            f.write(body)
        with open(os.path.join(tmp, "VERSION"), "w", encoding="utf-8") as f:
            f.write("9.9.9\n")

        plain = os.path.join(tmp, "skills", "plain-skill")
        os.makedirs(plain)
        plain_md = os.path.join(plain, "SKILL.md")
        with open(plain_md, "w", encoding="utf-8") as f:
            f.write("---\nmetadata:\n  version: 1.0.0\n---\nreads `live-spec-base` (v1.0.0) here\n")

        ext = os.path.join(tmp, "skills", "ext-clone")
        os.makedirs(os.path.join(ext, ".git"))
        ext_md = os.path.join(ext, "SKILL.md")
        ext_body = "---\nmetadata:\n  version: 1.3.0\n---\nreads `live-spec-base` (v1.3.0) here\n"
        with open(ext_md, "w", encoding="utf-8") as f:
            f.write(ext_body)
        with open(os.path.join(ext, ".git", "HEAD"), "w", encoding="utf-8") as f:
            f.write("ref: refs/heads/main\n")

        r = subprocess.run([sys.executable, script], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr

        assert open(ext_md, encoding="utf-8").read() == ext_body, \
            "the external clone's SKILL.md was rewritten: this repo has no authority over it"
        assert "ext-clone" not in r.stdout, "the stamper must not even report writing the clone"

        stamped = open(plain_md, encoding="utf-8").read()
        assert "  version: 9.9.9" in stamped, "the pack-owned skill must still be stamped"
        assert "`live-spec-base` (v9.9.9)" in stamped, "the in-text base reference too"
        assert "1 file(s) stamped to 9.9.9" in r.stdout, "exactly the pack-owned one"
