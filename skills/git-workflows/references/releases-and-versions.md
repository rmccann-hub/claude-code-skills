# Releases and versions

Read this for cutting a release, making or protecting a release tag, writing or fixing a release
workflow, writing a changelog entry, choosing a version number, or keeping a release line and
backporting to it.

It covers everything from the changelog entry to the published release. The commits it
releases are `commits-and-pull-requests`; the checks that must pass first are `ci-workflows`.

## Rules

1. **Release from an annotated tag on the release commit's SHA,** never a branch's tip, made by
   a job when there's no local clone, after the changelog entry and after CI is green on that
   commit.
2. **A tag or release a job makes with `GITHUB_TOKEN` starts no other workflow** (fact
   `token-no-trigger`). Publish in the same job, or call the publish workflow.
3. **Add the changelog entry in the same pull request as the change,** written for the people
   using the project.
4. **Keep a second release line only when users need it,** and backport to it with
   `git cherry-pick -x`, one focused pull request per fix.

### Releases

1. **Write the changelog entry,** under the version's heading, before the tag.
2. **Read CI's conclusion on the exact commit you're releasing.** A green run on another commit
   proves nothing about this one.
3. **Tag that commit by its SHA,** never a branch: a branch's tip may have moved past the
   release commit. Tag it before a later commit changes a workflow. A job's token can't push a
   tag whose commit carries a workflow file that no branch still has as it was
   (fact `workflow-scope`).
4. **Make an annotated tag.** Git's docs mean annotated tags for releases, and `git describe`
   uses nothing else by default (facts `tag-kinds`, `describe`). `gh release create` with a new
   tag name makes the tag itself, and it isn't annotated (fact `gh-release-tag`). So push the
   annotated tag first, then run `gh release create --verify-tag`, which refuses a tag that
   doesn't exist yet. With no local clone, a `workflow_dispatch` job makes the tag.
   project-bootstrap-and-audit's release gate gives the route (*How a tag gets cut when there
   is no local clone*).
5. **A tag or release the job makes with `GITHUB_TOKEN` starts no other workflow** (fact
   `token-no-trigger`). A publish workflow listening for `on: push: tags` or `on: release` never
   runs. Publish in the same job, or call the publish workflow with `workflow_call`.
6. **With immutable releases:** create the release as a draft, attach its assets, then publish.
   Once published, the tag can't move, and a deleted release's tag name can't be used again
   (fact `immutable`).

Example, tested: [assets/workflows/release.yml](../assets/workflows/release.yml) takes a version
and a commit SHA. It refuses a version that isn't Semantic Versioning, a commit that isn't on
the default branch, a commit whose `CHANGELOG.md` has no section for the version, a commit
carrying a workflow file no branch has as it is, and a commit with a check that hasn't passed,
or with no checks at all. Its own earlier attempts don't count as checks. Then it makes the
annotated tag on that commit as `github-actions[bot]` (fact `bot-identity`), and pushes it. A
run that fails after pushing can be run again: it carries on from a tag it would have made.
Only its job may write, and checkout keeps no credentials.

**Protect the release tags.**
[assets/rulesets/release-tags.json](../assets/rulesets/release-tags.json) stops a `v*` tag
being moved, deleted or force-pushed. It leaves creation open, so the release job can still
make the tag. Import it under Settings, Rules, Rulesets (fact `ruleset-import`).

**Test a release job without spending a tag.** With immutable releases, a published tag name
can never be used again (fact `immutable`). So try a release job in a fork, or in a test
repository, or with a pre-release version such as `1.4.0-rc.1`, before you trust it with a real
version.

**Signed tags.** If you sign, sign release tags with `git tag -s`, which makes an annotated
tag. A release job's tag then needs a signing key the job can reach, so decide where that key
lives before requiring signed tags.

### Changelog entries

Keep a Changelog 2.0.0 (fact `kac`) keeps the format that 1.1.0 had.

- `## [Unreleased]` sits at the top, and entries go under six headings: **Added**, **Changed**,
  **Deprecated**, **Removed**, **Fixed** and **Security**. Dates are `YYYY-MM-DD`, a pulled
  release is marked `[YANKED]`, and each version links to a compare view of its diff.
- Write for the people using the project: what changed for them, not the commit log. A commit
  and a changelog entry are written for different readers, so draft one from the other if you
  like, then rewrite it.
- A **Security** entry that has a CVE starts with it.
- Mark a breaking change, and give the upgrade steps beside it.
- Add the entry in the same pull request as the change. At release, the `Unreleased` entries
  move under the new version before the tag is made.
- Where coding agents work on the project, the changelog brief goes in their context file
  (fact `kac-agents`).
- From Keep a Changelog 1.1.0, an existing changelog stays valid. Update the link in its
  preamble, and take up the new guidance.

### Version numbers

The scheme, what counts as a major change for this project, and how to deprecate before
removing are project-bootstrap-and-audit's rules (dimension 10, *Documentation, versioning and
handoff*). It uses Semantic Versioning (fact `semver`), which works only once the project says
what its public API is. Other projects choose differently: pip numbers releases by the calendar
(fact `pip-calver`), and semantic-release derives each version from Conventional Commits (fact
`semantic-release`).

### Release lines and backports

- **Each line has a branch,** `release/X.Y`.
- **A fix lands on the default branch first,** then goes to the line with `git cherry-pick -x`,
  so the commit names its source (fact `cherry-x`). FFmpeg does this for 78 of the last 80
  commits on its `release/9.0`.
- **A fix meant for a backport stays focused,** with nothing it doesn't need, so it applies
  cleanly and is quick to review. FFmpeg's developer guide asks for exactly this.
- **Each backport is its own pull request against the release branch,** so that line's own CI
  runs on it. FFmpeg automates this: a label on the merged pull request opens the backport.
- **What a point release may take** is the standard's rule: project-bootstrap-and-audit's
  release gate.
- **Which lines need a fix:** the ones containing the commit that introduced the bug, which the
  fix's `Fixes:` trailer names where the author knew it. Then run
  `git branch -r --contains <commit>` and `git tag --contains <commit>`.

### From lightweight to annotated release tags

Make every tag from now on annotated, made on the release commit by its SHA. Don't replace tags
already published: with immutable releases you can't (fact `immutable`), and other people's
clones already have them.

## Mistakes

- **A release staged and never published.** Work committed after it, under its dated changelog
  heading, makes the heading describe something the tag won't hold, and whatever waits on the
  release waits silently. Publish it, or move the heading back to `Unreleased`.
- **A release candidate proved only in the working tree.** One candidate's suite failed a
  freshness check on a clean checkout, and its regeneration step named every derived file but
  two. Build each candidate from a clean checkout, regenerate with one command, and move the
  same artifact between channels rather than rebuilding it.
- **`gh release create` with a new tag name,** which makes a tag that isn't annotated (fact
  `gh-release-tag`). Push the annotated tag first, then run it with `--verify-tag`.
- **Tagging a branch instead of a commit.** The branch's tip may have moved past the release
  commit, and with immutable releases the mistake can't be undone. Tag the SHA.
- **Expecting a tag or release made with `GITHUB_TOKEN` to start the publish workflow.** It
  starts nothing (fact `token-no-trigger`).
- **Deleting an immutable release to redo it.** The tag name can't be used again (fact
  `immutable`).
- **Attaching assets after publishing an immutable release.** Attach them while it's a draft.
- **Tagging before the changelog entry exists,** or tagging a commit whose CI you haven't read.
- **`git push --tags`,** which pushes every local tag, including stray ones. Push the one tag:
  `git push origin refs/tags/v1.4.0`.
- **A changelog copied from the commit log.** It's written for the wrong reader. Rewrite it for
  the people using the project.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`. Whether a tag
ruleset exists needs admin access to the settings, or it's `UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Release tags are lightweight, or the release route makes them so | `git for-each-ref refs/tags --format='%(refname:short) %(objecttype)'`; `commit` means lightweight | `GAP`; rate how the next tag gets made | An annotated tag on the release commit's SHA, made by a job (facts `tag-kinds`, `gh-release-tag`) |
| A job makes a release with `GITHUB_TOKEN`, and another workflow is meant to publish it | Look for `on: release` or `on: push: tags` workflows | `BLOCKER` where the docs say releases publish | Publish in the same job, or `workflow_call` (fact `token-no-trigger`) |
| A second release line with no branch, or backports without `-x` | `git log release/X.Y --grep 'cherry picked from'` | `GAP` | A `release/X.Y` branch, and `git cherry-pick -x` for each backport (fact `cherry-x`) |
| Release tags can be moved or deleted | The same rulesets, for a tag ruleset matching the release tags | `GAP` where releases are tagged and the plan allows rulesets | Import `assets/rulesets/release-tags.json` |

## Why

### Releasing from a tag

**The advice.** Release from an annotated tag on a commit whose CI you've read, after the
changelog entry.

**Why.** Git's own documentation keeps annotated tags for releases (fact `tag-kinds`), and
`git describe` counts only annotated tags unless told otherwise (fact `describe`). An annotated
tag records who tagged, when, and why. A tag on a commit whose CI you haven't read releases
whatever that commit holds.

**What others do.** Many projects release with `gh release create` or GitHub's release page.
Given a new tag name, `gh` makes the tag itself, and to release from an annotated tag you push
that tag first (fact `gh-release-tag`). semantic-release works out the version from the commit
messages and publishes it (fact `semantic-release`). For changelogs, towncrier builds notes from
one file per change, so parallel pull requests don't conflict over one shared file (fact
`towncrier`).

**What each choice costs.** An annotated tag made by a job takes one more step than clicking
"Publish release". A generated changelog saves writing, but reads like the commit log it came
from.

### Release lines and backports

**The advice.** Keep a second release line only when users need one. Backport with
`git cherry-pick -x`, one focused pull request per fix.

**What others do.**

| Project | Practice | Its reason |
|---|---|---|
| Linux kernel | A fix goes into mainline first, then back to stable lines, at most 100 lines each (fact `kernel-stable`) | A fix that exists only on a stable line regresses at the next upgrade |
| Git | Bug fixes build up on `maint`, and `master` contains all of `maint` (fact `git-branches`) | One commit ID serves both lines, so nothing needs `-x` |
| FFmpeg | Cherry-picks with `-x` on each release branch | Each backport names its source commit |

**What each choice costs.** Merging forward keeps a single commit ID, but the fix has to be
written against the old code. Cherry-picking back is simpler when the lines have drifted apart,
and `-x` records where each copy came from (fact `cherry-x`).

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `describe` | `git describe` uses only annotated tags unless given `--tags` or `--all` | [git-describe](https://git-scm.com/docs/git-describe) | "By default (without --all or --tags) git describe only shows annotated tags." | 2026-09-30 | 2027-09-30 |
| `tag-kinds` | Git's own docs mean annotated tags for releases | [git-tag](https://git-scm.com/docs/git-tag) | "Annotated tags are meant for release while lightweight tags are meant for private or temporary object labels." | 2026-09-30 | 2027-09-30 |
| `cherry-x` | `git cherry-pick -x` records the source commit in the message | [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick) | "append a line that says \"(cherry picked from commit …)\"" | 2026-09-30 | 2027-09-30 |
| `token-no-trigger` | Events made with `GITHUB_TOKEN` start no new workflow run, except `workflow_dispatch` and `repository_dispatch`; a pull request it opens or updates gets runs that wait for approval | [Triggering a workflow](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow) | "events triggered by the GITHUB_TOKEN will not create a new workflow run, with the following exceptions" | 2026-09-30 | 2027-03-31 |
| `workflow-scope` | A token without the workflow permission can push a workflow file only where a branch already has it with the same path and contents | [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) | "Workflow files can be committed without this scope if the same file (with both the same path and contents) exists on another branch in the same repository." | 2026-10-05 | 2027-04-05 |
| `bot-identity` | Checkout's README commits as `github-actions[bot]` with the address `41898282+github-actions[bot]@users.noreply.github.com` | [checkout README](https://raw.githubusercontent.com/actions/checkout/main/README.md) | `git config user.name "github-actions[bot]"` | 2026-09-30 | 2027-03-31 |
| `immutable` | An immutable release locks its tag and assets once published. A deleted release's tag name can't be reused, and assets go on while it's a draft | [Immutable releases](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases) | "Git tags cannot be moved" | 2026-09-30 | 2027-03-31 |
| `gh-release-tag` | `gh release create` with a new tag name makes the tag itself, and it isn't annotated; `--verify-tag` refuses a tag that doesn't exist yet | [gh release create](https://cli.github.com/manual/gh_release_create) | "To create a release from an annotated git tag, first create one locally with git, push the tag to GitHub, then run this command." and "Use --verify-tag to abort the release if the tag doesn't already exist." | 2026-09-30 | 2027-03-31 |
| `kac` | Keep a Changelog 2.0.0 (2026-06-07) changed the guidance, not the format: six change types, `YYYY-MM-DD` dates, `Unreleased` and `[YANKED]` | [keepachangelog.com](https://keepachangelog.com/en/2.0.0/) | "It breaks the guidance, not the format" | 2026-09-30 | 2027-03-31 |
| `kac-agents` | Keep a Changelog 2.0.0 asks projects with coding agents to put their changelog brief in the agents' context file | [keepachangelog.com](https://keepachangelog.com/en/2.0.0/) | "record that brief where they read it, for example an AGENTS.md or CLAUDE.md file" | 2026-09-30 | 2027-03-31 |
| `semver` | Semantic Versioning 2.0.0 is current, and it requires a declared public API | [semver.org](https://semver.org/) | "Software using Semantic Versioning MUST declare a public API." | 2026-09-30 | 2027-09-30 |
| `pip-calver` | pip numbers releases by the calendar, as YY.N | [pip release process](https://pip.pypa.io/en/stable/development/release-process/) | "The version number of pip is YY.N, where YY is the year of the release and N identifies the quarter of the year" | 2026-09-30 | 2027-03-31 |
| `semantic-release` | semantic-release works out the next version from commit messages, and publishes it | [semantic-release README](https://raw.githubusercontent.com/semantic-release/semantic-release/master/README.md) | "Fully automated version management and package publishing" | 2026-09-30 | 2027-03-31 |
| `towncrier` | towncrier builds release notes from one file per change, so changes don't conflict over one shared file | [towncrier](https://towncrier.readthedocs.io/en/stable/) | "towncrier reads “news fragments” which contain information useful to end users" | 2026-09-30 | 2027-03-31 |
| `kernel-stable` | A fix reaches a kernel stable line only once it is in mainline, and is at most 100 lines | [Stable kernel rules](https://docs.kernel.org/process/stable-kernel-rules.html) | "It or an equivalent fix must already exist in Linux mainline (upstream)." and "It cannot be bigger than 100 lines" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-tag, git-describe, git-cherry-pick) | Tags and backports | GPL-2.0: facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (triggering a workflow, immutable releases, OAuth scopes) | What a job's token can start and push | CC BY 4.0: facts in our own words, with short quotes |
| [actions/checkout README](https://github.com/actions/checkout) | The bot identity | MIT: a fact with a short quote |
| [gh manual](https://cli.github.com/manual/gh_release_create) | The tag `gh release create` makes | MIT: a fact with a short quote |
| [Semantic Versioning 2.0.0](https://semver.org/) | Version numbers | CC BY 3.0: summarized, with attribution |
| [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | Changelog format and guidance | MIT: summarized |
| [Linux kernel: stable kernel rules](https://docs.kernel.org/process/stable-kernel-rules.html) | Stable backports | Not stated on the page: short quotes only |
| [towncrier](https://towncrier.readthedocs.io/en/stable/), [pip's release process](https://pip.pypa.io/en/stable/development/release-process/), [semantic-release](https://github.com/semantic-release/semantic-release) | Changelog fragments, calendar versions, versions from commits | Not stated on the pages: short quotes only |
| FFmpeg, read from its own tree and history on 2026-09-30 | Cherry-picks with `-x` on `release/9.0`, its backport automation, focused backports | Facts about the project, in our own words |
