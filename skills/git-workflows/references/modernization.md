# Modernization: moving off older Git and CI practice

Read this when a repository still uses a practice that has been superseded, and you're moving it
on. Each move lists the steps in a safe order. Facts are named by ID from `facts.md`.

## From Git Flow to short-lived branches

1. Stop branching new work from `develop`; branch from the default branch instead.
2. Merge `develop` into the default branch through one pull request, with a merge commit.
3. Retarget the open pull requests at the default branch.
4. Delete `develop` only once no open pull request targets it, no release line needs it, and
   no commit found only on it is cited anywhere. Keep `release/X.Y` branches only for lines you
   still support.
5. Update the context file and the contributing guide, so no one recreates it.

## From tag-pinned to SHA-pinned actions

1. For each `uses:`, take the SHA of the version you use from the action's own repository:
   `git ls-remote --tags https://github.com/OWNER/ACTION 'refs/tags/v7.0.1*'`. For an annotated
   tag it prints two lines: the tag object's SHA, then the commit's, on the line ending `^{}`.
   Pin the commit's.
2. Replace `@v7` with `@<full SHA> # v7.0.1`.
3. Turn on Dependabot version updates for `github-actions`, and check its pull requests reach
   the pinned lines.
4. Where you can, require pinning by policy (fact `sha-policy`).

## Off actions that run on Node 20

The runners no longer ship Node 20 (fact `node20`). Move each action to its current major, from
its release page, and pin it by SHA.

## Off `pull_request_target`

1. Move what the workflow does to `pull_request`, which has no secrets for forks.
2. Where it must stay, because it labels or comments, make sure it never checks out or runs the
   pull request's code.
3. On a public repository, set an explicit event policy before 2 November 2026, or it stops
   running (fact `prt-default`).

## From `master` to `main`

1. Rename the branch on GitHub. It redirects the old name, and retargets open pull requests.
2. In each clone:
   `git branch -m master main`, then `git fetch origin`, then
   `git branch -u origin/main main`, then `git remote set-head origin -a`.
3. Update CI's `on:` branch filters, rulesets and scripts that name `master`.

## Towards SHA-256 repositories

Git 3.0 will make SHA-256 the default for new repositories (fact `git3`). Stop treating commit
IDs as 40 characters in scripts, regular expressions and database columns, and accept 64.

## From lightweight to annotated release tags

Make every tag from now on annotated, made on the release commit by its SHA. Don't replace tags already
published: with immutable releases you can't (fact `immutable`), and other people's clones
already have them.

## From hooks in `.git/hooks` to committed hooks

1. Move the scripts into a tracked directory, such as `.githooks/`.
2. Point Git at it: `git config core.hooksPath .githooks` (fact `hooks-path`).
3. For agents' cloud sessions, set it from a committed `SessionStart` hook.
4. Or use pre-commit, or prek, which runs the same `.pre-commit-config.yaml` faster (facts
   `pre-commit`, `prek`).

## From hand-written branch cleanup to `--delete-merged`

For local branches, from Git 2.56: `git branch --dry-run --delete-merged 'origin/*'`, then
without `--dry-run` (fact `delete-merged`). It deletes a branch only when its tip is on its
upstream, and it leaves alone a branch whose push would update that upstream, or whose upstream
is gone: most branches made with `git push -u`. Remote branches are still checked one at a
time, against their pull requests and anything that cites their commits.

## From Keep a Changelog 1.1.0 to 2.0.0

The format didn't change (fact `kac`), so an existing changelog stays valid. Update the link in
its preamble, and take up the new guidance, such as putting the changelog brief in the coding
agents' context file (fact `kac-agents`).
