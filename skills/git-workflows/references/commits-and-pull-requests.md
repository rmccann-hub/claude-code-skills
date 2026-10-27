# Commits and pull requests

Read this for writing a commit message, naming a branch, opening or reviewing a pull request,
choosing and checking the commit grammar, or setting the address commits carry.

It covers what a commit and a pull request say. Merging is `branches-and-merging`; which
branches to keep, `rebasing-and-recovery`; changelogs and versions, `releases-and-versions`.

## Rules

1. **Write down one commit grammar and check it:** Conventional Commits, or Git's own "area:
   summary". The context file names it, and CI checks each pull request's commits.
2. **The subject is in the imperative, 50 characters is the soft limit, and the body says
   why.**
3. **Facts that tools read go in trailers.**
4. **One change per commit,** and the build passes at each one.
5. **Commit with the account's noreply address** in a public repository.
6. **Never amend, squash or rebase a commit once it's pushed to a shared branch or cited
   anywhere,** such as a pull request body, a decision record or a report. Add a new commit
   instead. Never invent a commit ID, an author or an issue number.

### The grammar

Two families work:

- **Conventional Commits** (fact `cc`): `type(scope)!: summary`. The spec fixes `feat`, `fix`
  and the breaking-change marks. Other types, such as `docs`, `refactor`, `test`, `build`, `ci`,
  `chore`, `perf` and `revert`, are convention.
- **"area: summary"**, the area being the directory, component or module touched, such as
  `avformat/hls: fix subtitle playlist IO buffer leaks`. Git's own guidance asks for it (fact
  `area-prefix`). FFmpeg uses it for nearly all its commits, and its commit-message check
  rejects Conventional Commits.

Where pull requests are squashed, set the default squash title to the pull request's title,
and check that: otherwise GitHub takes a one-commit pull request's own message (fact
`squash-default`), and whoever merges can edit it. A `commit-msg` hook helps only where a
persistent local clone installs it (`git-hooks`).

[assets/workflows/commit-subjects.yml](../assets/workflows/commit-subjects.yml), tested, checks
a pull request's commits against the grammar its `GRAMMAR` line names, `area` or
`conventional`. It passes `git revert`'s subjects, refuses unsquashed `fixup!` and `squash!`
commits, and fails on finding none or on an unknown grammar, so "couldn't check" never passes.
Give Dependabot a prefix, such as `commit-message: prefix: "deps"`, and its subjects pass too
(fact `dependabot-prefix`).

### The subject and the body

- The subject is in the imperative, saying what the change does: "fix crash on an empty
  playlist", not "fixed stuff" (fact `area-prefix`).
- 50 characters or fewer is git's soft limit, with no full stop (fact `subject-50`). Tools that
  show one line per commit cut a long subject.
- A blank line follows the subject. Wrap the body near 72 columns, for a terminal.
- The body says **why**: the cause, the effect on users, and what a reviewer or a later
  `git bisect` needs. The diff shows what changed.

### Trailers

Trailers are `Key: value` lines at the end of the message, one per line (fact `trailers`).

| Trailer | Use it for |
|---|---|
| `Fixes: <commit> ("<subject>")` | The commit that introduced the defect, where known, so each release line can tell whether it needs the fix. FFmpeg names the reproducer or report the same way |
| `Co-authored-by: Name <address>` | Everyone else who wrote it. GitHub credits each one (fact `co-authored`) |
| `Signed-off-by: Name <address>` | Only where the project asks for a Developer Certificate of Origin |
| `Reviewed-by:`, `Found-by:` | Credit for review, and for whoever found the bug |

### The author's address

- **A public repository's commits publish their author address.** Set the noreply address in
  each clone's `git config user.email`, and turn on "Keep my email addresses private" for merges
  and edits made on GitHub (fact `commit-email`).
- **Then turn on "Block command line pushes that expose my email".** It catches a clone still set
  to the private address (fact `email-push-block`).
- **An address already published stays.** Fix the settings, and leave the history. Only the
  owner can ask for a rewrite, and `leaked-data` says what it costs.

### One change per commit

- Formatter runs, mass renames, lockfiles and other regenerated files get commits of their own,
  so a later regeneration never rewrites a cited commit.
- Stage with `git add -p` or named paths when the tree holds unrelated changes.

### Branch names

`<kind>/<topic>`: short, lowercase, hyphenated, one topic per branch. Kinds such as `fix/`,
`feat/`, `docs/` and `chore/` read well. A release line's branch is `release/X.Y`. Branch from
the current default branch, fetched first.

### Pull requests

- **Title:** in the commit grammar, since under squash merging it can become the commit's
  subject (fact `squash-default`).
- **Description:** what changes and why; how it was tested, with the commands and their
  output; what's left out on purpose; breaking changes and upgrade steps; linked issues; which
  files or commits to read first.
- **Size:** reviewable in one sitting. Why is project-bootstrap-and-audit's *Review, with one
  maintainer*.
- **Before asking for review,** read your own diff whole, for debug output, commented-out code,
  a TODO with no issue, a secret, and files you didn't mean to change.

### Review comments

- Label each comment **blocking**, **suggestion**, **question** or **nit**, so the author knows
  what must change before merging.
- Review in this order: correctness, security, design, edge cases, performance, readability,
  style.
- An agent reviewing its own change is the least independent reader. project-bootstrap-and-audit's
  *Review, with one maintainer* says what to do instead.

## Mistakes

- **Accepting only Conventional Commits.** "area: summary" is Git's own (fact `area-prefix`).
  Pick one, and write it down.
- **A grammar written down and never checked.** It drifts within weeks. Check it in CI.
- **Checking commit subjects where pull requests are squashed.** Check the title (fact
  `squash-default`).
- **`git add .` in a tree holding unrelated changes,** or a secret file not yet ignored.
- **Amending or rebasing a pushed commit to tidy its message.** Every copy and citation now
  points at a commit the branch no longer holds. Add a commit.
- **Inventing a commit ID, an author or an issue number.** Read it from Git or the platform, or
  leave it out.
- **Expecting `Fixes: <commit>` to close an issue.** Only a closing keyword and issue
  number, such as `Fixes #42` in the message or description, closes one, and only on a merge
  into the default branch (fact `close-keywords`).
- **Fixing code inherited from upstream in a commit that doesn't say so.** One went unreported
  for two months, until a search for upstream's code found it. Say whose code it is. Before
  reporting it, reproduce it on a build of upstream's head, and point each file and line there.
- **A "current state" section in `CLAUDE.md`,** or any context file. It goes stale within days.
  Status lives in the pull request and its issues; plans, in one planning file.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The commit grammar is unstated or unchecked | The context file, and CI checking commits, or titles under squash merging (fact `squash-default`) | `GAP` from T2 | Name it in the context file; check it with the commit-subjects example, set to that grammar |
| The context file has a status section | Read it | `DRIFT`: it goes stale | Plans to one planning file, status to the pull request or issue |
| Public commits carry an address meant to stay private | `git log --format='%ae' \| sort \| uniq -c`, or the commits API's author logins | `GAP` for commits to come | The noreply address in each clone, and both email settings (facts `commit-email`, `email-push-block`). Never rewrite published history for it |

## Why

### The commit grammar

**The advice.** Write down one commit grammar, and check it.

**Why.** A subject is read far more often than it's written: in `git log --oneline`,
`git bisect` and release notes. A checked grammar stays consistent; an unchecked one drifts.

**What others do.**

| Project | Grammar | Its reason |
|---|---|---|
| Git | "area: " prefix, imperative (facts `area-prefix`, `subject-50`) | Readers scan by area |
| Linux kernel | "subsystem: summary phrase", imperative (fact `kernel-subject`) | Mail is filtered and routed by subsystem |
| Go | The package it changes, then a colon (fact `go-subject`) | Say where before what |
| LLVM | An area tag in brackets, such as `[SCEV]` (fact `llvm-policy`) | "This helps email filters and searches for post-commit reviews." |
| semantic-release users | Conventional Commits types (fact `cc`) | A tool works out the next version (fact `semantic-release`) |

**What each choice costs.** Conventional Commits drives tools, but its types are coarse, and
`feat:` spends characters that could say where. An area prefix tells a reviewer where to look,
but drives no tool unless you write one.

**When to choose differently.** Conventional Commits when a tool should derive versions or
release notes from commits; an area prefix when people read the history more than tools do.

### One change per commit

**The advice.** One change per commit, each building, and mechanical changes on their own.

**Why.** `git bisect` lands on a commit. One that mixes a reformat with a fix makes the fix hard
to find and to revert alone, and one that doesn't build stops the bisect there.

**What it costs.** Staging by hunk takes longer than `git add .`, and a branch has more commits.
Under squash merging the split survives only in review.

### The author's address

**The advice.** Commit with the noreply address, and turn on both email settings.

**Why.** A public commit's address is published for good, and changing it rewrites history,
costing every clone and citation (`leaked-data`). Preventing it costs two settings and a line of
configuration.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cc` | Conventional Commits 1.0.0: `feat`, `fix`, and `!` or a `BREAKING CHANGE:` footer for a breaking change | [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/) | "indicated by a ! immediately before the :" | 2026-09-30 | 2027-09-30 |
| `area-prefix` | Git: prefix the subject with "area: ", in the imperative mood | [SubmittingPatches](https://git-scm.com/docs/SubmittingPatches) | "prefix the first line with \"area: \"" | 2026-09-30 | 2027-09-30 |
| `subject-50` | Git: a subject of 50 characters or fewer, a blank line after, no full stop | [SubmittingPatches](https://git-scm.com/docs/SubmittingPatches), [git-commit](https://git-scm.com/docs/git-commit) | "50 characters is the soft limit" | 2026-09-30 | 2027-09-30 |
| `trailers` | Trailers are `key: value` lines ending a commit message; `git interpret-trailers` handles them | [git-interpret-trailers](https://git-scm.com/docs/git-interpret-trailers) | "trailer metadata at the end of the otherwise free-form part" | 2026-09-30 | 2027-09-30 |
| `squash-default` | GitHub's default squash message for a one-commit pull request is that commit's; a repository can change it | [Commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests) | "the commit title and message if the pull request contains only 1 commit" | 2026-09-30 | 2027-03-31 |
| `co-authored` | GitHub credits each `Co-authored-by:` author whose address is tied to their account | [Multiple authors](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors) | "Co-authored-by trailers" and "associated with their account on GitHub.com" | 2026-09-30 | 2027-09-30 |
| `close-keywords` | A closing keyword in a description or a commit message closes the issue only on a merge into the default branch | [Linking issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | "fix fixes fixed" | 2026-09-30 | 2027-09-30 |
| `commit-email` | "Keep my email addresses private" covers GitHub's own operations; a clone's commits use its Git configuration, and earlier ones keep their address | [Commit email](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) | "select Keep my email addresses private" and "still associated with your previous email address" | 2026-10-05 | 2027-04-05 |
| `email-push-block` | The push-blocking setting refuses a push whose newest commit's author address is private on the account | [Blocking pushes](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address) | "a private email on your GitHub account, we will block the push" | 2026-10-05 | 2027-04-05 |
| `dependabot-prefix` | Dependabot adds a colon after a `commit-message.prefix` ending in a letter or number | [Dependabot options](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) | "Dependabot inserts a colon after the prefix" and "when the value ends with a letter, number" | 2026-09-30 | 2027-03-31 |
| `kernel-subject` | The kernel's subject is "subsystem: summary phrase", in the imperative | [Submitting patches](https://docs.kernel.org/process/submitting-patches.html) | "subsystem: summary phrase" and "in imperative mood" | 2026-09-30 | 2027-03-31 |
| `go-subject` | Go prefixes the subject with the package changed; Gerrit's `Change-Id` trailer ties a change's uploads together | [Contribution guide](https://go.dev/doc/contribute) | "prefixed by the primary affected package" and "used by Gerrit to match successive uploads" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) | Subjects, bodies and trailers | GPL-2.0: our own words, short quotes |
| [GitHub Docs](https://docs.github.com/) | Squash titles, closing keywords, credit, addresses, Dependabot | CC BY 4.0: short quotes |
| [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | One commit grammar | CC BY 3.0: summarized, attributed |
| [Linux kernel docs](https://docs.kernel.org/process/submitting-patches.html) | The kernel's subjects | Not stated: short quotes only |
| [Go contribution guide](https://go.dev/doc/contribute) | Package prefixes, Gerrit's `Change-Id` | Not stated: short quotes only |
| FFmpeg's tree and history, read 2026-09-30 | Its "area: summary" grammar and check, `Fixes:` and `Found-by:` | Facts about the project, in our own words |
