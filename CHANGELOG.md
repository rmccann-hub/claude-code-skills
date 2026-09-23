# Changelog

Notable changes to this repository. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The PROJECT-BOOTSTRAP-AND-AUDIT standard (v0.35.0) as the skill `project-bootstrap-and-audit`,
  in the plugin `standards`.
- `skillcheck`, checking:
  - spec-only frontmatter and the forms of its optional fields;
  - name and description limits;
  - `SKILL.md` under 500 lines;
  - links that resolve, and references one level deep;
  - hidden and bidirectional characters;
  - catalog consistency.
- `ROADMAP.md`: every skill, shipped or planned. `skillcheck` keeps it and the README's skill
  table in step with `skills/`.
- `skillcheck` runs the standard's own mechanical checks (its Test G) on the copy shipped here.
- CI: the checks, Claude Code's own catalog validator, and a secret scan behind a canary.
- Research prompts, and the procedure for taking results in (`research/`).
- Context files, the decision record, the authoring review, the security policy.
