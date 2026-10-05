---
name: git-workflows
description: Sets up and runs a repository's Git and GitHub workflow, with the reasons, what other projects do, and the trade-offs. It covers commit messages and trailers, branch names, pull requests and review, the merge strategy, deleting branches safely, rebasing, conflicts and recovering lost commits, GitHub Actions CI (permissions, timeouts, SHA-pinned actions, path filters, required checks that never report, pull_request_target, slow CI), hooks, .gitignore, secrets that reached a commit, annotated release tags, changelogs, versions, release lines and backports. Use when writing a commit message, pull request, changelog entry or version number, deciding squash against merge commits, cleaning up branches, resolving a conflict, writing or fixing a workflow, speeding up CI without weakening it, adding a hook, responding to a committed secret, cutting a release or backporting a fix. For a full audit or first-time setup of a repository against the standard, use project-bootstrap-and-audit.
license: Apache-2.0
metadata:
  reviewed: "2026-10-05"
---

# Git workflows

How to run a repository's history, pull requests, CI and releases so that nothing gets lost:
no stranded commits, no gate that never ran, no release that never published. It assumes
GitHub and GitHub Actions. Other forges have the same ideas under other names. In Claude Code,
run the commands; on claude.ai, give them to the person to run.

Dated facts, such as versions, defaults and platform changes, live in
[references/facts.md](references/facts.md), and the other files name them by ID, such as fact
`node20`, rather than repeating them.

## The rules that matter most

1. **Choose the merge strategy by whether anything cites your commits.** A merge commit keeps a
   branch's commits. Squash and GitHub's rebase-merge write new ones (fact `rebase-merge`), so
   cited commits leave the default branch's history, and once the branch goes they survive only
   under the pull request's own refs, which a clone doesn't fetch (fact `pr-refs`). Record the
   choice in the context file, and allow only that strategy in the repository's settings.
2. **Never delete a branch until you've checked what still needs it:** its pull request,
   commits cited only there, a release line, a sibling repository. Never bulk-delete remote
   branches from `git branch -r --merged`.
3. **Never rewrite shared or cited history.** No force-push to a shared branch, and no amend of
   a pushed or cited commit. Revert, or add a commit.
4. **Never get to green by going around a check.** No `--no-verify`, and no skipping or
   quarantining a failing test. Fix the cause. CI re-runs what a commit hook checks, and branch
   protection does on the server what a pre-push hook does.
5. **Write down one commit grammar and check it:** Conventional Commits, or Git's own "area:
   summary". Subjects are in the imperative, 50 characters is the soft limit, and the body says
   why. Facts go in trailers, such as `Fixes:`, `Co-authored-by:` and `Signed-off-by:`.
6. **In every workflow:**
   - `permissions:` at the top;
   - `timeout-minutes` on every job;
   - actions pinned to a full commit SHA with the version in a comment;
   - installs that fail on lockfile drift;
   - runs on the branches where work happens;
   - no path filter on a required check.
7. **Release from an annotated tag on the release commit's SHA,** never a branch's tip, made by
   a job when there's no local clone, after the changelog entry and after CI is green on that
   commit. A tag or release the job makes with `GITHUB_TOKEN` starts no other workflow (fact
   `token-no-trigger`).
8. **Read Git's output whole.** Merge and rebase output lists the conflicts. Check for conflict
   markers in CI. Never read an exit status through a pipe.
9. **Keep a second release line only when users need it,** and backport to it with
   `git cherry-pick -x`, one focused pull request per fix.

## Where to go

| When you're | Read |
|---|---|
| writing a commit message, branch name, pull request, review comment, changelog entry or version number, or choosing the address commits carry | [references/style.md](references/style.md) |
| setting up or changing branching, protection, the merge strategy, branch deletion, hooks, CI, releases, release lines or `.gitignore`; rebasing your own branch, resolving a conflict, or recovering a lost commit | [references/setup.md](references/setup.md) |
| writing or reviewing workflow triggers, permissions or third-party actions, or handling a secret that reached a commit | [references/security.md](references/security.md) |
| proving that a workflow, hook or gate works | [references/testing.md](references/testing.md) |
| reviewing a repository's Git and CI setup | [references/audit.md](references/audit.md) |
| about to do something risky, or checking an assistant's advice | [references/mistakes.md](references/mistakes.md) |
| moving off Git Flow, tag pins, Node 20 actions, `master`, `pull_request_target` or lightweight tags | [references/modernization.md](references/modernization.md) |
| checking a version, date or default | [references/facts.md](references/facts.md) |
| checking where a rule comes from, or a source's license | [references/sources.md](references/sources.md) |
| asking why a rule is what it is, what other projects do instead, whether it fits your project, or how long CI should take and where it should run | [references/why.md](references/why.md) |

Tested examples to copy:
- [assets/githooks/commit-msg](assets/githooks/commit-msg) checks the "area: summary" grammar.
- [assets/githooks/pre-push](assets/githooks/pre-push) blocks direct pushes to `main`.
- [assets/workflows/commit-subjects.yml](assets/workflows/commit-subjects.yml) checks a pull
  request's commits.
- [assets/workflows/release.yml](assets/workflows/release.yml) makes an annotated release tag on
  a commit named by SHA, once its checks have passed.
- [assets/workflows/tests.yml](assets/workflows/tests.yml) runs the tests and proves they
  finished.
- [assets/rulesets/default-branch.json](assets/rulesets/default-branch.json) and
  [assets/rulesets/release-tags.json](assets/rulesets/release-tags.json) protect the default
  branch and the release tags, imported under Settings, Rules, Rulesets.

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

Before anything destructive, show what it will do, and wait for confirmation. That covers
deleting a branch or a tag, resetting, force-pushing, and rewriting history. Commit, stash or
copy uncommitted work before any command that touches the working tree.

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
