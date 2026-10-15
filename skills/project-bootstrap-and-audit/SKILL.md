---
name: project-bootstrap-and-audit
description: "Sets up, retrofits or audits a repository against the PROJECT-BOOTSTRAP-AND-AUDIT standard: structure, CI, agent files, secrets, dependencies, licensing, release readiness. Stops for approval before changing anything."
license: CC0-1.0
metadata:
  standard-version: "0.44.0"
---

# Project bootstrap and audit

The standard is one long reference file beside this one:
[references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.44.0.md](references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.44.0.md).
It is written to be read in ranges, never end to end.

1. Build its heading index first:
   `grep -n '^# \|^## ' references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.44.0.md`, run from this skill's
   directory.
2. Read its "How to read this file" section, then only the ranges your job needs.
3. Follow it as written, including both waits: Phase 3, and the Phase 6 approval gate. Nothing is
   written to the repository before explicit approval.
4. The run's report goes outside the repository, as the standard's Phase 6 describes, and is
   handed to the person in the same turn.

Where a repository keeps an `evidence` branch, as the standard's *Generated evidence* describes,
[scripts/verify_evidence.py](scripts/verify_evidence.py) checks the branch and its manifest in a
local copy, and its first lines say how to make one. It reads Git only and changes nothing.
