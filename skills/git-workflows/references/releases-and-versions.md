# Releases and versions

Read this for cutting a release, making or protecting a release tag, writing or fixing a release
workflow, writing a changelog entry, choosing a version number, or keeping and backporting to a
release line.

The commits it releases are `commits-and-pull-requests`; the checks that must pass first are
`ci-workflows`.

## Rules

1. **Release from an annotated tag on the release commit's SHA,** after the changelog entry and
   after CI is green on that commit. A tag is optional where the project's records make a
   release a commit that a committed manifest names and consumers pin.
2. **A tag or release a job makes with `GITHUB_TOKEN` starts no other workflow** (fact
   `token-no-trigger`), so one listening for `on: push: tags` or `on: release` never runs.
   Publish in the same job, or call the publish workflow with `workflow_call`.
3. **Add the changelog entry in the same pull request as the change,** written for its users.
4. **Keep a second release line only when users need it,** and backport to it with
   `git cherry-pick -x`, one focused pull request per fix.

### Releases

1. **Write the changelog entry,** under the version's heading, before the tag.
2. **Read CI's conclusion on the exact commit you're releasing.** A green run on another commit
   proves nothing about this one.
3. **Tag that commit by its SHA,** never a branch, whose tip may have moved on, and before a
   later commit changes a workflow: a job's token can't push a tag whose commit carries a
   workflow file no branch still has as it was (fact `workflow-scope`).
4. **Make an annotated tag** (facts `tag-kinds`, `describe`), and push it before
   `gh release create --verify-tag` (fact `gh-release-tag`). With no local clone, a
   `workflow_dispatch` job makes it (project-bootstrap-and-audit's release gate).
5. **Publish in the release job, or call the publish workflow** (rule 2).
6. **With immutable releases,** create the release as a draft, attach its assets, then publish.
   Then the tag can't move, and a deleted release's tag name can't be reused (fact `immutable`).

Example, tested: [assets/workflows/release.yml](../assets/workflows/release.yml) takes a version
and a commit SHA. It refuses a version that isn't Semantic Versioning, and a commit off the
default branch, with no `CHANGELOG.md` section for it, carrying a workflow file no branch has
as it is, or with a check not passed or none at all (its own earlier runs don't count). Then
it makes and pushes the annotated tag as `github-actions[bot]` (fact `bot-identity`). Rerun
after failing past the push, it goes on from that tag. Only its job may write, and checkout
keeps no credentials.

**Protect the release tags.**
[assets/rulesets/release-tags.json](../assets/rulesets/release-tags.json) stops a `v*` tag
being moved, deleted or force-pushed, and leaves creation open for the release job. Import it
under Settings, Rules, Rulesets (fact `ruleset-import`).

**Test a release job without spending a tag,** which immutable releases never give back: in a
fork, a test repository, or with a pre-release such as `1.4.0-rc.1`.

**Moving from lightweight tags:** make every new tag annotated, and leave published ones. With
immutable releases you can't replace them (fact `immutable`), and others' clones have them.

**Signed tags.** If you sign, sign release tags with `git tag -s`, which makes an annotated
tag. A release job then needs a key it can reach: decide where it lives first.

### Changelog entries

Keep a Changelog 2.0.0 (fact `kac`) keeps 1.1.0's format, so a 1.1.0 changelog stays valid:
update its preamble's link, and take up the new guidance.

- `## [Unreleased]` sits at the top, and entries go under six headings: Added, Changed,
  Deprecated, Removed, Fixed and Security. Dates are `YYYY-MM-DD`, a pulled release is marked
  `[YANKED]`, and each version links to a compare view of its diff.
- Write what changed for the people using the project, not the commit log. A commit has a
  different reader: draft one from the other, then rewrite it.
- A Security entry that has a CVE starts with it.
- Mark a breaking change, with its upgrade steps beside it.
- At release, the `Unreleased` entries move under the new version, before the tag.
- Where coding agents work on the project, the changelog brief goes in their context file
  (fact `kac-agents`).

### Version numbers

The scheme, what counts as a major change, and deprecating before removing are
project-bootstrap-and-audit's rules (dimension 10). It uses Semantic Versioning (fact
`semver`), which works only once the project declares its public API. pip numbers releases by
the calendar instead (fact `pip-calver`), and semantic-release derives each version from
Conventional Commits (fact `semantic-release`).

### Release lines and backports

- **Each line has a branch,** `release/X.Y`.
- **A fix lands on the default branch first,** then goes to the line with `git cherry-pick -x`,
  so the commit names its source (fact `cherry-x`), as FFmpeg does.
- **A fix meant for a backport stays focused,** so it applies cleanly and is quick to review,
  as FFmpeg's developer guide asks.
- **Each backport is its own pull request against the release branch,** so that line's CI runs
  on it. At FFmpeg, a label on the merged pull request opens the backport.
- **What a point release may take** is project-bootstrap-and-audit's release gate.
- **Which lines need a fix:** those holding the commit that brought the bug, which the fix's
  `Fixes:` trailer names where known. Run `git branch -r --contains <commit>` and
  `git tag --contains <commit>`.

## Mistakes

- **A release staged and never published.** Work committed after it, under its dated changelog
  heading, makes the heading describe what the tag won't hold, and whatever waits on it waits
  silently. Publish it, or move the heading back to `Unreleased`.
- **A release candidate proved only in the working tree.** One candidate's suite failed a
  freshness check on a clean checkout, and its regeneration step named every derived file but
  two. Build each candidate from a clean checkout, regenerate with one command, and move the
  same artifact between channels, never a rebuild.
- **`gh release create` with a new tag name,** which makes a lightweight tag (fact
  `gh-release-tag`). Push the annotated tag first, then use `--verify-tag`.
- **Tagging a branch instead of a commit.** With immutable releases it can't be undone. Tag the
  SHA.
- **Expecting a tag or release made with `GITHUB_TOKEN` to start the publish workflow** (fact
  `token-no-trigger`).
- **Deleting an immutable release to redo it,** which loses the tag name, or **attaching assets
  after publishing one:** attach them while it's a draft.
- **Tagging before the changelog entry exists,** or tagging a commit whose CI you haven't read.
- **`git push --tags`,** which pushes every local tag, including stray ones. Push the one tag:
  `git push origin refs/tags/v1.4.0`.
- **A changelog copied from the commit log,** written for the wrong reader.

## Audit

Severity uses the status words in this skill's `SKILL.md`. A public repository's rulesets read
without authentication (fact `rest-public`); a private one's need access, or it's
`UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Release tags are lightweight, or the release route makes them so | `git for-each-ref refs/tags --format='%(refname:short) %(objecttype)'`; `commit` is lightweight | `GAP` where the project's records say releases are tagged, rating how the next tag is made; else `N/A` | An annotated tag on the release commit's SHA, made by a job (fact `gh-release-tag`) |
| A release made with `GITHUB_TOKEN` that another workflow is meant to publish | Look for `on: release` or `on: push: tags` workflows | `BLOCKER` where the docs say releases publish | Publish in the same job, or `workflow_call` (fact `token-no-trigger`) |
| A second release line with no branch, or backports without `-x` | `git log release/X.Y --grep 'cherry picked from'` | `GAP` | A `release/X.Y` branch, and `git cherry-pick -x` for each backport (fact `cherry-x`) |
| Release tags can be moved or deleted | A tag ruleset matching the release tags | `GAP` where releases are tagged and the plan allows rulesets | Import `assets/rulesets/release-tags.json` |

## Why

### Releasing from a tag

**The advice.** Release from an annotated tag on a commit whose CI you've read, after the
changelog entry.

**Why.** Git's documentation keeps annotated tags for releases (fact `tag-kinds`), and
`git describe` counts only them by default (fact `describe`). An annotated tag records who
tagged, when, and why. A tag on a commit whose CI you haven't read releases whatever
that commit holds.

**What others do.** Many projects release from GitHub's release page or `gh release create`,
which makes a lightweight tag (fact `gh-release-tag`). semantic-release versions and publishes
from the commit messages. towncrier builds notes from one file per change, so parallel pull
requests don't conflict over one changelog (fact `towncrier`).

**What each choice costs.** A job's annotated tag takes one more step than clicking "Publish
release". A generated changelog saves writing, but reads like the commit log it came from.

**When to choose differently.** Where consumers pin a commit SHA a committed manifest names,
the SHA can't move, as a protected tag can't. The manifest is the record; a tag adds a name.

### Release lines and backports

**The advice.** Keep a second release line only when users need one. Backport with
`git cherry-pick -x`, one focused pull request per fix.

**What others do.**

| Project | Practice | Its reason |
|---|---|---|
| Linux kernel | A fix goes into mainline, then back to stable lines, at most 100 lines (fact `kernel-stable`) | A fix only on a stable line regresses at the next upgrade |
| Git | Bug fixes build up on `maint`, and `master` contains all of `maint` (fact `git-branches`) | One commit ID serves both lines, so nothing needs `-x` |
| FFmpeg | Cherry-picks with `-x`: 78 of the last 80 commits on its `release/9.0` | Each backport names its source commit |

**What each choice costs.** Merging forward keeps one commit ID, but the fix is written against
the old code. Cherry-picking back is simpler when the lines have drifted, and `-x` records where
each copy came from.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `describe` | `git describe` uses only annotated tags by default | [git-describe](https://git-scm.com/docs/git-describe) | "git describe only shows annotated tags." | 2026-09-30 | 2027-09-30 |
| `tag-kinds` | Git's docs mean annotated tags for releases | [git-tag](https://git-scm.com/docs/git-tag) | "Annotated tags are meant for release" | 2026-09-30 | 2027-09-30 |
| `cherry-x` | `git cherry-pick -x` names the source commit | [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick) | "append a line that says \"(cherry picked from commit …)\"" | 2026-09-30 | 2027-09-30 |
| `token-no-trigger` | Events made with `GITHUB_TOKEN` start no workflow run, but for `workflow_dispatch` and `repository_dispatch` | [Triggering a workflow](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow) | "events triggered by the GITHUB_TOKEN will not create a new workflow run" | 2026-09-30 | 2027-03-31 |
| `workflow-scope` | A token without the workflow permission pushes a workflow file only if another branch has it as is | [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) | "(with both the same path and contents) exists on another branch" | 2026-10-05 | 2027-04-05 |
| `bot-identity` | Checkout's README commits as `github-actions[bot]` | [checkout README](https://raw.githubusercontent.com/actions/checkout/main/README.md) | `git config user.name "github-actions[bot]"` | 2026-09-30 | 2027-03-31 |
| `immutable` | A published immutable release locks its tag and assets; a deleted one's tag name can't be reused, and assets go on while it's a draft | [Immutable releases](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases) | "Git tags cannot be moved" | 2026-09-30 | 2027-03-31 |
| `gh-release-tag` | `gh release create` with a new tag name makes a lightweight tag; `--verify-tag` needs an existing one | [gh release create](https://cli.github.com/manual/gh_release_create) | "To create a release from an annotated git tag, first create one locally" and "Use --verify-tag to abort the release if the tag doesn't already exist" | 2026-09-30 | 2027-03-31 |
| `kac` | Keep a Changelog 2.0.0 (2026-06-07) kept the format | [keepachangelog.com](https://keepachangelog.com/en/2.0.0/) | "It breaks the guidance, not the format" | 2026-09-30 | 2027-03-31 |
| `kac-agents` | Keep a Changelog 2.0.0 puts the brief in agents' context file | [keepachangelog.com](https://keepachangelog.com/en/2.0.0/) | "for example an AGENTS.md or CLAUDE.md file" | 2026-09-30 | 2027-03-31 |
| `semver` | Semantic Versioning 2.0.0 requires a declared public API | [semver.org](https://semver.org/) | "MUST declare a public API" | 2026-09-30 | 2027-09-30 |
| `pip-calver` | pip numbers releases by the calendar, as YY.N | [pip release process](https://pip.pypa.io/en/stable/development/release-process/) | "The version number of pip is YY.N" | 2026-09-30 | 2027-03-31 |
| `semantic-release` | semantic-release versions and publishes from commit messages | [semantic-release README](https://raw.githubusercontent.com/semantic-release/semantic-release/master/README.md) | "Fully automated version management" | 2026-09-30 | 2027-03-31 |
| `towncrier` | towncrier builds release notes from one file per change | [towncrier](https://towncrier.readthedocs.io/en/stable/) | "towncrier reads “news fragments”" | 2026-09-30 | 2027-03-31 |
| `kernel-stable` | A stable kernel fix is in mainline first, at most 100 lines | [Stable kernel rules](https://docs.kernel.org/process/stable-kernel-rules.html) | "must already exist in Linux mainline" and "It cannot be bigger than 100 lines" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) | Tags and backports | GPL-2.0: our own words, short quotes |
| [GitHub Docs](https://docs.github.com/) | Tokens and immutable releases | CC BY 4.0: our own words, short quotes |
| actions/checkout and the gh manual, linked in Facts | The bot identity, `gh release create` | MIT: short quotes |
| [Semantic Versioning 2.0.0](https://semver.org/) | Version numbers | CC BY 3.0: summarized, attributed |
| [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | Changelogs | MIT: summarized |
| Other projects, linked in Facts | What other projects do | Not stated: short quotes only |
| FFmpeg's tree and history, read 2026-09-30 | Its backports | Facts, in our own words |
