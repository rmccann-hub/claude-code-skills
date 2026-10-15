@AGENTS.md

Sessions on this repository also load the maintainer's skills synced from claude.ai. They are
older copies of skills this repository is replacing. This repository's settings can't stop the
sync, but `skillOverrides` in `.claude/settings.json` hides a synced skill, tried on
2026-10-15. Where one disagrees with a file under `skills/`, the file here is the one being
worked on.

`.claude/settings.json` turns off both plugins' copies of this repository's own skills, and the
synced copies of `git-workflows` and `project-bootstrap-and-audit`. It also applies the owner's
exclusion list in `skills/project-bootstrap-and-audit/assets/`, which turns off the retired
`markdown-standards` (`house-style` replaces it), `skill-orchestrator`, `skill-stress-tester`
and `code-planner`, with `skill-creator` left on here, where skills are built.
