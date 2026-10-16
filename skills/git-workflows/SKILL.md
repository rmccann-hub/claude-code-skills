---
name: git-workflows
description: "Sets up and runs Git and GitHub work: commits, branches, pull requests, merges, conflicts, GitHub Actions CI, hooks, leaked secrets, tags, changelogs, versions and releases. Use when writing, fixing or speeding up any of these."
license: Apache-2.0
metadata:
  reviewed: "2026-10-16"
---

# Git workflows

How to run a repository's history, pull requests, CI and releases so that nothing gets lost:
no stranded commits, no gate that never ran, no release that never published. It assumes
GitHub and GitHub Actions. Other forges have the same ideas under other names. In Claude Code,
run the commands; on claude.ai, give them to the person to run.

## What applies to every module

1. **Choose the merge strategy by whether anything cites your commits.** A merge commit keeps a
   branch's commits; squash and rebase-merge don't (`branches-and-merging`).
2. **Never delete a branch until you've checked what still needs it,** and never bulk-delete
   remote branches from `git branch -r --merged` (`branches-and-merging`).
3. **Never rewrite shared or cited history.** Revert, or add a commit. The one exception is
   removing personal information at the owner's request (`leaked-data`).
4. **Never get to green by going around a check.** No `--no-verify`, and no skipping or
   quarantining a failing test. Fix the cause (`ci-workflows`, `git-hooks`).
5. **Write down one commit grammar and check it** (`commits-and-pull-requests`).
6. **Harden every workflow:** `permissions:` at the top, `timeout-minutes` on every job, actions
   pinned to a full commit SHA, installs that fail on lockfile drift, runs on the branches where
   work happens, and no path filter on a required check (`actions-security`, `ci-workflows`).
7. **Release from an annotated tag on the release commit's SHA,** after the changelog entry and
   after CI is green on that commit (`releases-and-versions`).
8. **Read Git's output whole,** and never read an exit status through a pipe
   (`branches-and-merging`).
9. **Keep a second release line only when users need it** (`releases-and-versions`).

Before anything destructive, show what it will do, and wait for confirmation. That covers
deleting a branch or a tag, resetting, force-pushing, and rewriting history. Commit, stash or
copy uncommitted work before any command that touches the working tree.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources. A module names a fact by its ID, such
as fact `node20`, and the fact's row is in whichever module holds it.

| Module | Read it for |
|---|---|
| [`commits-and-pull-requests`](references/commits-and-pull-requests.md) | writing a commit message, naming a branch, opening or reviewing a pull request, choosing and checking the commit grammar, or the address commits carry |
| [`branches-and-merging`](references/branches-and-merging.md) | the branching model, protecting the default branch, the merge strategy, deleting branches, rebasing, conflicts, recovering a lost commit, or renaming `master` |
| [`ci-workflows`](references/ci-workflows.md) | a GitHub Actions workflow's triggers, timeouts, installs, path filters and required checks; how long CI should take; proving a gate or a test job works |
| [`actions-security`](references/actions-security.md) | a workflow's permissions, pinned actions, untrusted input, `pull_request_target`, Node 20 actions, or scanning workflows with zizmor |
| [`git-hooks`](references/git-hooks.md) | writing, installing or testing a commit or push hook, or a hook that didn't run |
| [`releases-and-versions`](references/releases-and-versions.md) | cutting a release or tag, a release workflow, changelog entries, version numbers, release lines and backports |
| [`leaked-data`](references/leaked-data.md) | a secret or personal information that reached a commit, and rewriting history to remove it |
| [`gitignore`](references/gitignore.md) | writing or debugging `.gitignore`, ignoring secrets, committing lockfiles, or untracking a file |

Tested examples to copy, each described in its module:

- [assets/githooks/commit-msg](assets/githooks/commit-msg) and
  [assets/githooks/pre-push](assets/githooks/pre-push), in `git-hooks`.
- [assets/workflows/commit-subjects.yml](assets/workflows/commit-subjects.yml), in
  `commits-and-pull-requests`.
- [assets/workflows/tests.yml](assets/workflows/tests.yml), in `ci-workflows`.
- [assets/workflows/release.yml](assets/workflows/release.yml) and
  [assets/rulesets/release-tags.json](assets/rulesets/release-tags.json), in
  `releases-and-versions`.
- [assets/rulesets/default-branch.json](assets/rulesets/default-branch.json), in
  `branches-and-merging`.

## Check before you act

| Question | Command |
|---|---|
| Which merge methods does the repository allow? | `gh api repos/OWNER/REPO --jq '.allow_merge_commit, .allow_squash_merge, .allow_rebase_merge'` |
| Which rulesets protect the branches and tags? | `gh api repos/OWNER/REPO/rulesets --jq '.[].id'`, then `gh api repos/OWNER/REPO/rulesets/<id>` for each one's rules |
| Is this cited commit still on the default branch? | `git merge-base --is-ancestor <commit> origin/main && echo reachable` |
| Which branches hold this commit? | `git branch -r --contains <commit>` |
| Which local branches lost their remote branch? | `git fetch --prune`, then `git for-each-ref --format='%(if:equals=[gone])%(upstream:track)%(then)%(refname:short)%(end)' refs/heads`; check each one's pull request before deleting it |
| Are the tags annotated? | `git for-each-ref refs/tags --format='%(refname:short) %(objecttype)'` (`tag` means annotated) |
| Which rule ignores this file? | `git check-ignore -v <path>` |
| Is the workflow valid? | `actionlint`, then `zizmor .` |
| Which local branches tracking a shared branch are merged into it? | `git branch --dry-run --delete-merged 'origin/*'` (Git 2.56 or later; it skips most branches made with `git push -u`) |

The first two answer from the refs you have. In a shallow or single-branch clone, such as CI's
or a cloud session's, fetch every branch first, with `--unshallow` if
`git rev-parse --is-shallow-repository` prints `true`.

## Reviewing a repository

Each module's Audit section checks its part of a repository, without a full audit. For a full
audit, with tiers and a report, use project-bootstrap-and-audit: it rates most of these checks
by tier (dimensions 6, 8 and 10, and its release gate), and its rating wins where the two
differ. The status words are the standard's:

- **`BLOCKER`:** a live exposure, or a check reporting success while measuring nothing.
- **`DRIFT`:** configured, but no longer doing what it says.
- **`GAP`:** missing something the project needs.
- **`OVER`:** heavier than the project needs.
- **`MIRROR`:** the truth is outside the repository, such as a platform setting you've read
  rather than a file.
- **`UNVERIFIABLE-HERE`:** can't be established from this session, such as a settings page
  without admin access.
- **`OK`**, and **`N/A`**.

Workflows may end in `.yml` or `.yaml`, so every search covers both.

## What this doesn't cover

- **A full audit, or a first-time setup of a repository:** use project-bootstrap-and-audit. It
  rates these practices by tier:
  - dimension 6, *Enforcement and review*: gates, merging and review;
  - dimension 10, *Documentation, versioning and handoff*;
  - its release gate;
  - its starter CI file.
- **How to design and write the tests CI runs:** that belongs to a testing skill. This one
  covers the job that runs them, and proving that job ran.
- **Git hosting administration:** servers, organizations, teams and Git LFS configuration.

## Where this came from

- The owner's earlier `git-workflows` skill, as a list of topics, checks and lessons. Nothing
  was copied from it. Where it advised against a lesson here, such as squash-merging feature
  branches, bulk-deleting merged branches, `--no-verify` or a status section in `CLAUDE.md`,
  the advice was dropped.
- Research runs R08 (Git, GitHub, CI/CD) and R05 (versioning, releases), filed in this skill's
  repository. They were leads until each claim was checked.
- A cold review by a second reader on 2026-09-30, and the split into modules on 2026-10-16,
  recorded in this skill's repository.
