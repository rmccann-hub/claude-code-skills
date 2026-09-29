# Changelog

Notable changes to this repository. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Research prompt R21, on running with the fewest dependencies at their newest versions. It asks
  what a dependency costs, when to add or remove one, which runtime versions to target and
  test, and how CI can check less. Its checked result goes into the standard.
- Research prompt R22, on starting the standard with one command from any repository. It asks
  which route reaches cloud sessions and how to tell which copy ran, how to draft an existing
  repository's answers for the owner to confirm, what a new project's interview asks before it
  recommends a language and shape, and where the answers are kept for the next run. Its checked
  result shapes the rebuild's first piece.
- Research result R22, in two passes, each filed in `research/runs/` with a verification table.
  A skill uploaded to the claude.ai account is the route into cloud sessions, where synced
  plugins are no longer documented to load. The files it proposes wait for the rebuild's first
  piece.

### Changed

- The standard is now v0.37.0, with twenty-two fixes: the nine the parity baseline found, the
  set-up run's open amendments, and four that its own parity runs found. Read-only phases no
  longer write `.git/index`, one routing table replaces two that disagreed, ratings are definite
  where two runs split, and the starter CI's collection guard names itself when it fails. Its
  history entry lists the rest.
- The standard is now v0.38.0, with fifteen fixes and one addition made before its first live
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
  - An install that is itself a gate counts in the tally of commands, and a proposed change
    to the standard has its own list at the gate.
  - Dimension 6 says every workflow sets `permissions:`, a rule that lived only in the starter
    template, where an audit doesn't look.
  - A run can read the standard from a link pinned to a commit and checked against its
    SHA-256, and its self-check records that hash.

  Its history entry lists the rest.
- The standard is now v0.39.0, with forty-one fixes from its first live audit and the runs
  before it:
  - Phase 3 drafts each answer the repository shows, with its evidence, for the owner to
    confirm. It offers "Not sure" on every question, and asks production, dependents and
    where it runs outright. A re-check asks "Is that still the case?" of each recorded answer.
  - A run that stops at Phase 3 hands over its report in a defined shape.
  - After the fetch, the default branch is read as `origin/<default>`. A secret-scan job is
    read by what it scanned, never by its conclusion.
  - Before each push, the apply half fetches the base and runs the full gate. Its fresh-clone
    check clones from the remote. It records each human action by what it saw, beside what
    it was told.
  - Dimensions 3 and 8 settle two splits. `CODEOWNERS` is due from a second committer, and an
    action pinned by tag is rated by what its workflow can reach.
  - Three dated facts about cloud sessions are checked again: synced plugins, synced skills
    and release assets.
  - Where the work lands on a branch other than the default, as in a fork whose default
    mirrors upstream, the run audits that branch.
  - An unattended run meets the Phase 3 wait with the answers it was given, and shows the tier
    first at the gate.

  Its history entry lists the rest.
- The standard is now v0.40.0, with ten fixes from its first live re-check and from the
  review, merge and branch check its owner asked for after the gate:
  - A scratch clone for replaying gates comes from the remote, or has its remote-tracking refs
    checked against the working copy's. A shallow clone is deepened before history is read.
  - A result caused by the run's own mistake goes in `corrections`, and a step the standard
    directs isn't counted as a deviation.
  - The address-domain command counts commits, not address lines.
  - Settings the run can't read are asked for at the Phase 3 wait, as a screenshot or a
    reading.
  - Before the pull request is offered, someone who didn't write the change reviews the diff.
  - Work the owner asks for after the gate, such as a merge, has its own block, and a branch is
    advised for deletion only after checking what still needs it.

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
