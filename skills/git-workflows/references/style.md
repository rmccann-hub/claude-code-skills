# Style: commits, branches, pull requests, changelogs and versions

Read this when you write a commit message, name a branch, open or review a pull request, add a
changelog entry or choose a version number. Facts are named by ID from `facts.md`.

## Commit messages

### One grammar, written down and checked

Two families work, and neither is the only right one:

- **Conventional Commits** (fact `cc`): `type(scope)!: summary`. The spec fixes the meaning of
  `feat` and `fix`, and marks a breaking change with `!` or a `BREAKING CHANGE:` footer. Other
  types, such as `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf` and `revert`, are
  convention. It suits a project whose tools derive versions or changelogs from commits.
- **"area: summary"**, where the area is the directory, component or module the change
  touches, such as `avformat/hls: fix subtitle playlist IO buffer leaks`. Git's own guidance
  asks for it (fact `area-prefix`), and it suits a tree with clear components. FFmpeg uses it
  for nearly all its commits, and its commit-message check rejects Conventional Commits.

Whichever it is, the repository's context file names it, and CI checks it on each pull
request's commits. Where pull requests are squashed, set the repository's default squash
commit title to the pull request's title, and check the title. GitHub's default otherwise
takes a one-commit pull request's own commit message (fact `squash-default`), and whoever
merges can still edit it. A `commit-msg` hook helps only where a persistent local clone
installs it.

### The subject line

- In the imperative, as if instructing the code: "fix crash on an empty playlist", not "fixed
  stuff" (fact `area-prefix`).
- 50 characters or fewer is git's soft limit, with no full stop (fact `subject-50`). Tools that
  show one line per commit cut a long subject.
- It says what the change does, not what you did.

### The body

- A blank line after the subject. Wrap the lines so they read in a terminal, conventionally
  near 72 columns.
- Say **why**: the cause, the effect on users, and what a reviewer or a later `git bisect`
  needs. The diff already shows what changed.

### Trailers

Facts that tools read go in trailers: `Key: value` lines at the end of the message (fact
`trailers`), one per line.

| Trailer | Use it for |
|---|---|
| `Fixes: <commit> ("<subject>")` | The commit that introduced the defect, where it's known, so each release line can tell whether it needs the fix. FFmpeg names the reproducer or the report the same way. |
| `Co-authored-by: Name <address>` | Everyone else who wrote it. GitHub credits each one (fact `co-authored`). |
| `Signed-off-by: Name <address>` | Only where the project asks for a Developer Certificate of Origin. |
| `Reviewed-by:`, `Found-by:` | Credit for review, and for whoever found the bug. |

A closing keyword such as `Fixes #42`, in the message or the pull request's description, closes
the issue only when the pull request merges into the default branch (fact `close-keywords`). A
trailer naming a commit closes nothing.

### One change per commit

- A commit does one thing, and the build passes at each one, so `git bisect` can land on it.
- A formatter run, a mass rename or regenerated files get a commit of their own. Then a later
  regeneration never has to rewrite a commit someone else cites.
- Stage deliberately, with `git add -p` or named paths, when the tree holds unrelated changes.
  `git add .` sweeps them all in.

### Never

- Never amend, squash or rebase a commit once it's pushed to a shared branch or cited anywhere,
  such as a pull request body, a decision record or a report. Add a new commit instead.
- Never invent a commit ID, an author or an issue number, in a message or anywhere else.

## Branch names

`<kind>/<topic>`: short, lowercase, hyphenated, one topic per branch. Kinds such as `fix/`,
`feat/`, `docs/` and `chore/` read well. A release line's branch is `release/X.Y`. Branch from
the current default branch, fetched first.

## Pull requests

- **Title:** in the repository's commit grammar. Under squash merging it becomes the commit's
  subject once the repository's default squash title is the pull request's title (fact
  `squash-default`).
- **Description:** what changes and why; how it was tested, with the commands and what they
  showed; what's deliberately left out; breaking changes and the upgrade steps; linked issues.
  Say which files or commits to read first.
- **Size:** small enough to review in one sitting, with a mechanical change, such as a
  reformat, a rename or a lockfile regeneration, in a commit of its own. Why is
  project-bootstrap-and-audit's *Review, with one maintainer*.
- **Before asking for review,** read your own diff whole. Look for debug output, commented-out
  code, a TODO with no issue behind it, a secret, and files you didn't mean to change.

### Review comments

- Label each comment: **blocking**, **suggestion**, **question** or **nit**, so the author knows
  what has to change before merging.
- Review in this order: correctness, security, design, edge cases, performance, readability,
  style.
- Review by the agent that wrote a change is the least independent reading there is.
  project-bootstrap-and-audit's *Review, with one maintainer* says what to do instead.

## Changelog entries

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

## Version numbers

The scheme, what counts as a major change for this project, and how to deprecate before
removing are project-bootstrap-and-audit's rules (dimension 10, *Documentation, versioning and
handoff*). It uses Semantic Versioning (fact `semver`), which works only once the project says
what its public API is. Other projects choose differently: pip numbers releases by the calendar
(fact `pip-calver`), and semantic-release derives each version from Conventional Commits (fact
`semantic-release`).
