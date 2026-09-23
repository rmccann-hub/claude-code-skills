---
name: project-bootstrap-and-audit
description: Set up a new repository, retrofit or audit an existing one, check configuration before a release, or plan what to fix next, against the PROJECT-BOOTSTRAP-AND-AUDIT standard (a two-axis stakes model and ten dimensions). Use when asked to bootstrap, scaffold, survey, audit or re-check a repository's structure, CI, agent configuration, secrets handling, dependencies, licensing or release readiness. It stops for approval before changing anything.
license: CC0-1.0
metadata:
  standard-version: "0.36.0"
---

# Project Bootstrap and Audit

The standard is one long reference file beside this one:
[references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.36.0.md](references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.36.0.md).
It is written to be read in ranges, never end to end.

1. Build its heading index first:
   `grep -n '^# \|^## ' references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.36.0.md`, run from this skill's
   directory.
2. Read its "How to Read This File" section, then only the ranges your job needs.
3. Follow it as written, including both waits: Phase 3, and the Phase 6 approval gate. Nothing is
   written to the repository before explicit approval.
4. The run's report goes outside the repository, as the standard's Phase 6 describes, and is
   handed to the person in the same turn.
