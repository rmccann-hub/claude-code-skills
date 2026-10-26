---
name: project-bootstrap-and-audit
description: "Sets up, retrofits or audits a repository against the PROJECT-BOOTSTRAP-AND-AUDIT standard: structure, CI, agent files, secrets, dependencies, licensing, release readiness. Stops for approval before changing anything."
license: CC0-1.0
metadata:
  standard-version: "0.48.2"
---

# Project bootstrap and audit

The standard is one long reference file beside this one:
[references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.48.2.md](references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.48.2.md).
It is written to be read in ranges, never end to end.

1. Build its heading index first:
   `grep -n '^# \|^## ' references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.48.2.md`, run from this skill's
   directory.
2. Read its "How to read this file" section, then only the ranges your job needs.
3. Follow it as written, including both waits: Phase 3, and the Phase 6 approval gate. Nothing is
   written to the repository before explicit approval.
4. The run's report goes outside the repository, as the standard's Phase 6 describes, and is
   handed to the person in the same turn.

Where a repository keeps an `evidence` branch, as the standard's *Generated evidence* describes,
[scripts/verify_evidence.py](scripts/verify_evidence.py) checks the branch and its manifest in a
local copy, and its first lines say how to make one. It reads Git only and changes nothing.

[assets/skill-overrides.json](assets/skill-overrides.json) is the owner's exclusion list: the
skills synced from their claude.ai account that repository sessions don't load, each with its
reason. The standard's dimension 4 says how a run proposes it, as `skillOverrides` in the
repository's `.claude/settings.json`.

## When something here is wrong

If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
https://github.com/rmccann-hub/claude-code-skills/issues.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
