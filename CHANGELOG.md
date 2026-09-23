# Changelog

Notable changes to this repository. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-23

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
- CI: the checks, Claude Code's own catalog validator, and a secret scan behind a canary. Every
  action is pinned to a full commit SHA.
- Research prompts, and the procedure for taking results in (`research/`).
- Context files, the decision record, the authoring review, the security policy.
- How to withdraw a bad skill: the README's Operations section.

### Changed

- The repository's licence is now Apache-2.0, replacing the CC0-1.0 file it was created with.
  The standard keeps its own CC0-1.0 dedication.
