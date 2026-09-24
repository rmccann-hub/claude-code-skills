# Changelog

Notable changes to this repository. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Research prompt R21, on running with the fewest dependencies at their newest versions. It asks
  what a dependency costs, when to add or remove one, which runtime versions to target and
  test, and how CI can check less. Its checked result goes into the standard.

### Changed

- The standard is now v0.37.0, with twenty-two fixes: the nine the parity baseline found, the
  set-up run's open amendments, and four that its own parity runs found. Read-only phases no
  longer write `.git/index`, one routing table replaces two that disagreed, ratings are definite
  where two runs split, and the starter CI's collection guard names itself when it fails. Its
  history entry lists the rest.
- The standard is now v0.38.0, with twelve fixes and one addition made before its first live
  run:
  - Phase 1 finds a decision record by its content, including one kept inside another file,
    and no longer reads the words "blast radius" in prose as a recorded tier.
  - A repository's own agent rules, such as committing without asking, don't lift the run's
    two waits.
  - Context files are measured in bytes as well as lines, and logs and other evidence are read
    in parts.
  - On a Windows host, the PowerShell it recommends depends on what the host already has:
    Windows PowerShell 5.1 where nobody will install and patch PowerShell 7 there. A PowerShell
    scheduled job has a layout.
  - Phase 0 says what to do when a fetch can't run, and the starter CI pins its action to a
    commit SHA.
  - A run can read the standard from a link pinned to a commit and checked against its
    SHA-256, and its self-check records that hash.

  Its history entry lists the rest.

### Fixed

- CI's collection guard says why it failed. With nothing collected, it used to stop under the
  runner's `bash -e` before printing anything.
- The parity grader's check that a declined item isn't proposed reads only what each amendment
  proposes. An amendment's reasoning can name the item without failing the run.

## [0.1.1] - 2026-09-23

### Changed

- **Breaking:** the marketplace is renamed from `rmccann-skills` to `claude-code-skills`, the
  repository's name, which is what claude.ai shows for it. The plugin is now
  `standards@claude-code-skills`. If you added the marketplace under its old name, remove it
  with `/plugin marketplace remove rmccann-skills` and add it again.
- Sessions on this repository don't load an installed copy of the plugin. `.claude/settings.json`
  turns off `standards@synced` and `standards@claude-code-skills`, so an older copy can't stand
  in for the one being rebuilt.
- The standard is now v0.36.0, with nine dated facts corrected against their primary sources.
  The main change: Claude Code reads `AGENTS.md` natively, but only in some sessions, so the
  `CLAUDE.md` shim stays. Its history entry lists the rest.

### Added

- The catalog's plugin entry names its author and repository.
- Research results R01-R05 and R08, each filed in `research/runs/` with a verification table.
- `skillcheck` checks `AGENTS.md`, `CLAUDE.md`, `.claude/` and `research/` for hidden and
  bidirectional characters, as it already did for skills.
- Parity runs for `project-bootstrap-and-audit`, the first piece of its rebuild. There are three
  sample repositories with answer keys, a grader (`python -m skillcheck.parity`), and the
  current skill's results as the baseline. `docs/testing-the-skill.md` says how to run one.
- The plan for rebuilding the standard into the skill, in `ROADMAP.md`.

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
