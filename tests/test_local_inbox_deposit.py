"""INV-174 — the inbox's local co-located arm: the deposit is the file alone, never a git act.

Co-located sessions share one working tree and one git index, so a depositor's git add or
commit races whatever the assigned session holds staged mid-landing. The local deposit stops
at writing the one new file; the assigned session's sweep commits the harvest itself. The
remote arm's commit-and-push road stays (INV-112).
"""
from conftest import criterion_with_bullets, read


def test_spec_states_the_local_arm():
    spec = read("PRODUCT_SPEC.md")
    assert "local co-located arm" in spec
    assert "| INV-174 |" in spec


def test_local_deposit_never_stages():
    # read the co-located criterion in its own home, so the three refusals are asserted where
    # the law states them rather than anywhere in the document
    clause = criterion_with_bullets(
        read("PRODUCT_SPEC.md"), "*when* a session shares the assigned session's working tree")
    assert clause is not None, "SPEC lost the co-located deposit criterion (INV-174)"
    assert "no staging, no commit, and no push" in clause


def test_inbox_readme_carries_the_split():
    readme = read("inbox/README.md")
    assert "same filesystem" in readme
    assert "INV-174" in readme
