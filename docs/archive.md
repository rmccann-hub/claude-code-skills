# What this repository keeps, and where

The answer this repository gives to the standard's four questions on records (dimension 10, from
v0.49.0), the owner's rule of 2026-10-29: consistency across repositories, not sameness, with
each difference deliberate, recorded and obvious.

1. **Its own record:** `docs/decisions.md` (append-only), `CHANGELOG.md`, `ROADMAP.md` and the
   dated research under `research/`. All stay on `main`, because sessions read them to work.
2. **What an outside reviewer would want:** the same, plus each release's signed files and
   attestations on its GitHub release page.
3. **What partner repositories need from it:** the released skills and the standard, on `main`
   and in each release. The messages sent to them, and the audit kit, name audited
   repositories, so they live in the private `audit-reports` repository's `audit-log` branch,
   never here. That is the one deliberate difference from the model: this public repository
   can't hold another repository's records.
4. **Worth keeping, off `main`:** a split's finished work and superseded logs move to the orphan
   `archive` branch in one commit, never merged into `main`, added to and never edited. Each
   item sits in a folder named by its date, and is listed below.

## Index of the `archive` branch

| Date | Path on `archive` | What it holds | Moved from |
|---|---|---|---|
| 2026-11-03 | `README.md` | What the branch is for | Created |
