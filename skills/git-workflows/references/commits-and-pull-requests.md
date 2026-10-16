# Commits and pull requests

Read this for writing a commit message, naming a branch, opening or reviewing a pull request,
choosing and checking the commit grammar, or setting the address commits carry.

It covers what a commit and a pull request say. How they merge, and which branches to keep, is
`branches-and-merging`. The changelog entry and the version number are `releases-and-versions`.

## Rules

1. **Write down one commit grammar and check it:** Conventional Commits, or Git's own "area:
   summary". The context file names it, and CI checks each pull request's commits.
2. **The subject is in the imperative, 50 characters is the soft limit, and the body says
   why.**
3. **Facts that tools read go in trailers,** such as `Fixes:`, `Co-authored-by:` and
   `Signed-off-by:`.
4. **One change per commit,** and the build passes at each one.
5. **Commit with the account's noreply address** in a public repository.
6. **Never amend, squash or rebase a commit once it's pushed to a shared branch or cited
   anywhere,** such as a pull request body, a decision record or a report. Add a new commit
   instead. Never invent a commit ID, an author or an issue number.

### The grammar

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
installs it (`git-hooks`).

[assets/workflows/commit-subjects.yml](../assets/workflows/commit-subjects.yml), tested,
checks each commit in a pull request against "area: summary". It lets through the subjects
`git revert` writes, refuses `fixup!` and `squash!` commits that were never squashed, and fails
when it finds no commits to check, so "couldn't check" never passes. Give Dependabot a prefix,
such as `commit-message: prefix: "deps"`, and its subjects pass too (fact `dependabot-prefix`).

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

### The author's address

- **A commit's author address is public** once the commit is in a public repository, and it
  stays with the commit. So commit with the account's noreply address, set in each clone's
  `git config user.email`, and turn on the account's "Keep my email addresses private" for
  merges and edits made on GitHub (fact `commit-email`).
- **Then turn on "Block command line pushes that expose my email".** It refuses a push whose
  newest commit carries the private address (fact `email-push-block`), which catches a clone
  still set to it.
- **An address already in published history stays there.** Changing it means rewriting every
  commit after it, which strands every clone and every citation. Fix the settings, and leave the
  history. Only the owner can ask for the rewrite, and `leaked-data` says what it costs.

### One change per commit

- A commit does one thing, and the build passes at each one, so `git bisect` can land on it.
- A formatter run, a mass rename or regenerated files get a commit of their own. Then a later
  regeneration never has to rewrite a commit someone else cites.
- Stage deliberately, with `git add -p` or named paths, when the tree holds unrelated changes.
  `git add .` sweeps them all in.

### Branch names

`<kind>/<topic>`: short, lowercase, hyphenated, one topic per branch. Kinds such as `fix/`,
`feat/`, `docs/` and `chore/` read well. A release line's branch is `release/X.Y`. Branch from
the current default branch, fetched first.

### Pull requests

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
- **Status lives in the pull request and its issues,** not in the context file. Plans live in
  one planning file.

### Review comments

- Label each comment: **blocking**, **suggestion**, **question** or **nit**, so the author knows
  what has to change before merging.
- Review in this order: correctness, security, design, edge cases, performance, readability,
  style.
- Review by the agent that wrote a change is the least independent reading there is.
  project-bootstrap-and-audit's *Review, with one maintainer* says what to do instead.

## Mistakes

- **Accepting only Conventional Commits.** "area: summary" is Git's own convention (fact
  `area-prefix`). Pick one, and write it down.
- **A grammar written down and never checked.** It drifts within weeks. Check it in CI.
- **Checking commit subjects where pull requests are squashed.** The squash commit's subject
  comes from GitHub's default unless the repository sets it to the title (fact
  `squash-default`). Check the title.
- **`git add .` in a tree holding unrelated changes,** or a secret file that isn't ignored yet.
  Stage by path, or with `git add -p`.
- **Amending or rebasing a pushed commit to tidy its message.** Anyone who has it, and every
  citation, now points at a commit the branch no longer holds. Add a commit.
- **Inventing a commit ID, an author or an issue number** in a message, a description or a
  report. Read it from Git or the platform, or leave it out.
- **Expecting `Fixes: <commit>` to close an issue.** Only a closing keyword with an issue
  number does, and only on a merge into the default branch (fact `close-keywords`).
- **A "current state" section in `CLAUDE.md`.** It goes stale within days. Plans live in one
  planning file, and status in pull requests and issues.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The commit grammar is unstated or unchecked | The context file; a CI check on commits, or on titles where squash titles come from the pull request (fact `squash-default`) | `GAP` from T2 | Write the grammar in the context file, and check it with the commit-subjects example |
| The context file has a "current state" or status section | Read it | `DRIFT`: it goes stale | Move plans to one planning file, and status to the pull request or issue |
| A public repository's commits carry an address meant to stay private | `git log --format='%ae' \| sort \| uniq -c`, or the commits API's author logins, for the people who keep their address private | `GAP` for the commits still to come; the published ones stay | The noreply address in each clone's Git configuration, and the account's two email settings (facts `commit-email`, `email-push-block`). Never rewrite published history to remove it |

## Why

### The commit grammar

**The advice.** Write down one grammar, Conventional Commits or Git's "area: summary", and check
it.

**Why.** A subject is read far more often than it's written: in `git log --oneline`, in
`git bisect`, in release notes. A grammar that is checked stays consistent. One that is only
written down drifts within weeks.

**What others do.**

| Project | Grammar | Its reason |
|---|---|---|
| Git | "area: " prefix, imperative mood (facts `area-prefix`, `subject-50`) | Readers scan by area |
| Linux kernel | "subsystem: summary phrase", imperative (fact `kernel-subject`) | Mail is filtered and routed by subsystem |
| Go | The package it changes, then a colon (fact `go-subject`) | Say where before what |
| LLVM | An area tag in brackets, such as `[SCEV]` (fact `llvm-policy`) | "This helps email filters and searches for post-commit reviews." |
| Projects using semantic-release | Conventional Commits types (fact `cc`) | A tool works out the next version from them (fact `semantic-release`) |

**What each choice costs.** Conventional Commits can drive tools, but its types are coarse, and
the subject spends characters on `feat:` rather than on where the change is. An area prefix
tells a reviewer where to look, but drives no tool unless you write one.

**When to choose differently.** Pick Conventional Commits when a tool should derive versions or
release notes from commits. Pick an area prefix when people read the history more than tools
do.

### One change per commit

**The advice.** One change per commit, with the build passing at each, and mechanical changes
in commits of their own.

**Why.** `git bisect` lands on a commit, and a commit that mixes a reformat with a fix makes the
fix hard to find and hard to revert alone. A commit that doesn't build stops the bisect there.

**What it costs.** Staging by hunk takes longer than `git add .`, and a branch has more commits.
Under squash merging the split survives only in review.

### The author's address

**The advice.** Commit with the noreply address, and turn on both email settings.

**Why.** An address in a public commit is published for good: changing it means rewriting
history, which costs every clone and every citation (`leaked-data`). Preventing it costs two
settings and one line of Git configuration.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cc` | Conventional Commits 1.0.0: `feat` for a feature, `fix` for a bug fix, and a breaking change marked by `!` before the colon or a `BREAKING CHANGE:` footer | [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/) | "breaking changes MUST be indicated by a ! immediately before the :" | 2026-09-30 | 2027-09-30 |
| `area-prefix` | Git's own guidance: prefix the subject with "area: " and describe the change in the imperative mood | [SubmittingPatches](https://git-scm.com/docs/SubmittingPatches) | "It is also conventional in most cases to prefix the first line with \"area: \"" | 2026-09-30 | 2027-09-30 |
| `subject-50` | Git's own guidance: a subject line of 50 characters or fewer, then a blank line, with no full stop | [SubmittingPatches](https://git-scm.com/docs/SubmittingPatches), [git-commit](https://git-scm.com/docs/git-commit) | "50 characters is the soft limit" | 2026-09-30 | 2027-09-30 |
| `trailers` | Trailers are `key: value` lines at the end of a commit message, and `git interpret-trailers` reads and writes them | [git-interpret-trailers](https://git-scm.com/docs/git-interpret-trailers) | "Add or parse trailer metadata at the end of the otherwise free-form part of a commit message" | 2026-09-30 | 2027-09-30 |
| `squash-default` | GitHub's default squash message takes a one-commit pull request's own commit, and the pull request's title only for two or more; the repository can change the default | [Configuring commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests) | "the commit title and message if the pull request contains only 1 commit, or the pull request title and list of commits if the pull request contains 2 or more commits" | 2026-09-30 | 2027-03-31 |
| `co-authored` | GitHub credits each author named in a `Co-authored-by:` trailer whose address is tied to their GitHub account | [Creating a commit with multiple authors](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors) | "Add one or more Co-authored-by trailers to a commit message" and "For the commit to count as a contribution, use an email address associated with their account on GitHub.com." | 2026-09-30 | 2027-09-30 |
| `close-keywords` | A closing keyword in a pull request's description or a commit message closes the issue when the pull request merges into the default branch, and does nothing when it targets another branch | [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | "close closes closed fix fixes fixed resolve resolves resolved" | 2026-09-30 | 2027-09-30 |
| `commit-email` | "Keep my email addresses private" gives operations made on GitHub, such as a merge, the account's noreply address. A clone's commits take the address its Git configuration names, and commits made before a change keep the old one | [Setting your commit email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) | "To keep your email address private when performing web-based Git operations, select Keep my email addresses private" and "Any commits you made prior to changing your commit email address are still associated with your previous email address." | 2026-10-05 | 2027-04-05 |
| `email-push-block` | With "Block command line pushes that expose my email" on, GitHub refuses a push whose newest commit's author address is a private one on the account | [Blocking command line pushes that expose your personal email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address) | "If the author email on that commit is a private email on your GitHub account, we will block the push" | 2026-10-05 | 2027-04-05 |
| `dependabot-prefix` | Dependabot's `commit-message.prefix` adds a colon and a space after a prefix that ends in a letter or a number | [Dependabot options](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) | "Dependabot inserts a colon after the prefix before adding the main commit message when the value ends with a letter, number, closing parenthesis, or closing bracket." | 2026-09-30 | 2027-03-31 |
| `kernel-subject` | The kernel's subject line is "subsystem: summary phrase", in the imperative | [Submitting patches](https://docs.kernel.org/process/submitting-patches.html) | "subsystem: summary phrase" and "Describe your changes in imperative mood" | 2026-09-30 | 2027-03-31 |
| `go-subject` | Go prefixes a subject with the package it changes, and Gerrit's `Change-Id` trailer ties a change's uploads together | [Contribution guide](https://go.dev/doc/contribute) | "prefixed by the primary affected package" and "That line is used by Gerrit to match successive uploads" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-commit, git-interpret-trailers, SubmittingPatches) | Subjects, bodies and trailers | GPL-2.0: facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (squashing, linking issues, co-authors, commit email, Dependabot options) | Squash titles, closing keywords, credit, addresses | CC BY 4.0: facts in our own words, with short quotes |
| [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | One commit grammar | CC BY 3.0: summarized, with attribution |
| [Linux kernel: submitting patches](https://docs.kernel.org/process/submitting-patches.html) | The kernel's subject lines | Not stated on the page: short quotes only |
| [Go contribution guide](https://go.dev/doc/contribute) | Package-prefixed subjects, Gerrit's `Change-Id` | Not stated on the page: short quotes only |
| FFmpeg, read from its own tree and history on 2026-09-30 | Its "area: summary" grammar and the check that enforces it, `Fixes:` and `Found-by:` trailers | Facts about the project, in our own words |
