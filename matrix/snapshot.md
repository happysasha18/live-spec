### [node: snapshot [target]]

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-063 | The snapshot is the last accepted baseline; it advances only at *landed* and only for declared surfaces; never an undeclared advance [E-7] | string | `tests/test_snapshot_baseline.py` | *built* |
| M-064 | Adoption saves a baseline snapshot of current artifacts as the first diff base; never a first landing diffed against nothing [A-6] | string | lands at row 55 (with the machinery) | *todo* |
| M-169 | The snapshot design is decided and stated: home `.live-spec/snapshot/` with a per-surface manifest (what · landing · hash), advance at *landed* for declared surfaces only, last-only retention with git history as the archive, heavy surfaces hash-only; never a second archive mechanism, never a baseline advanced for an undeclared surface [E-7] | string | `test_snapshot_design` (red proven against HEAD — design facts absent there) | *built* |
