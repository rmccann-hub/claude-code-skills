# Mistakes: what goes wrong, including what AI assistants get wrong

Read this before a risky Git operation, when a workflow does something you didn't expect, or
when you're checking advice an assistant gave. Facts are named by ID from `facts.md`.

## History and branches

- **Squash-merging, then deleting the branch, where commits are cited.** The cited commits leave
  the default branch, and survive only under the pull request's own refs, which a clone doesn't
  fetch (facts `rebase-merge`, `pr-refs`). Use merge commits wherever anything cites commits.
- **Bulk-deleting remote branches that `git branch -r --merged` lists.** It can't see squash
  merges, citations or sibling repositories. Check each branch's pull request, the commits
  cited only there, and whoever else uses it, one branch at a time.
- **`git push --force` after rebasing.** It overwrites whatever someone else pushed since you
  fetched. Use `--force-with-lease --force-if-includes` (fact `force-if-includes`).
- **Reading `--ours` and `--theirs` the same way in a rebase as in a merge.** They swap (fact
  `rebase-ours`).
- **Amending, rebasing or force-pushing a commit others have, or that something cites.** Add a
  new commit; revert rather than reset on a shared branch.
- **`git reset --hard` or `git checkout -- <path>` with uncommitted work in the tree.** It's gone,
  and the reflog doesn't hold it. Commit, stash or copy it first.
- **`git add .` in a tree holding unrelated changes,** or a secret file that isn't ignored yet.
  Stage by path, or with `git add -p`.
- **`git push --tags`,** which pushes every local tag, including stray ones. Push the one tag:
  `git push origin refs/tags/v1.4.0`.
- **Validating commit IDs as exactly 40 hex characters.** SHA-256 repositories use 64, and Git
  3.0 makes SHA-256 the default for new repositories (fact `git3`).
- **`git init`, then `git push -u origin main`, when the new branch is `master`.** Use
  `git init -b main`, or set `init.defaultBranch`.

## Hooks and checks

- **`git commit --no-verify` or `git push --no-verify` to get past a hook.** Fix what it caught, or
  fix the hook. CI will run the check anyway.
- **Quarantining or skipping a flaky test "so it doesn't block CI".** It hides the failure from
  the only people who can fix it. Re-run it once to confirm it flakes, then instrument it and
  keep the artifacts until the cause is found.
- **A `pre-push` hook that checks the current branch.** It passes a push of another branch
  straight to `main`. Read the refs on standard input (`assets/githooks/pre-push`).
- **A hook documented in the README and installed by nobody,** especially in cloud sessions,
  which start fresh each time.
- **`chmod +x` on a hook, committed from Windows.** Git for Windows ignores file modes by
  default, so the commit keeps the file non-executable, and Git won't run it. Use
  `git add --chmod=+x`.
- **A hook that reads the first line of the message file.** Git hands it the message before it
  strips comments, so a commit template's comment becomes "the subject". Read it through
  `git stripspace --strip-comments`.
- **Reading an exit status through a pipe:** `pytest | tail` reports `tail`'s status.
- **Trimming a merge's or rebase's output for readability.** The conflict it listed goes unseen,
  and the markers ship. Read the whole output, and check for markers in CI.

## CI

- **Suggesting `actions/checkout@v4` or other old majors from training data.** Node 20 is gone
  from the runners (fact `node20`). Take the version and SHA from the action's release page, or
  from fact `checkout-sha`.
- **Assuming a SHA-pinned action gets security backports.** It doesn't (fact `checkout-v7`).
- **`paths` and `paths-ignore` on the same event** (fact `paths-both`), or a path filter on a
  required check (fact `skipped-pending`).
- **An `if:` that skips a required job.** A skipped job reports success, so the pull request
  merges with nothing tested (fact `job-if-success`).
- **`pip install -r requirements.txt` in CI with no lockfile, or `uv sync --frozen` believed to
  check the lockfile** (fact `uv-locked`).
- **A step name containing `: ` without quotes.** The file is no longer valid YAML, and the
  workflow never runs. actionlint catches it.
- **`${{ github.event.pull_request.title }}` inside `run:`**, which is shell injection (fact
  `injection`).
- **Planning a merge queue on a personal account's repository.** It isn't offered there (fact
  `merge-queue`).

## Releases

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

## Files

- **Comments after a pattern in `.gitignore`,** which become part of the pattern (fact
  `gitignore-comment`).
- **`!` re-including a file under an ignored directory,** which keeps nothing (fact
  `gitignore-parent`).
- **Ignoring `Cargo.lock` in a library,** which was the old advice (fact `cargo-lock`).
- **`git rm --cached` on a file others have,** such as a shared config. Their next pull
  deletes it from their working tree. Warn them first.
- **A "current state" section in `CLAUDE.md`.** It goes stale within days. Plans live in one
  planning file, and status in pull requests and issues.
- **Accepting only Conventional Commits.** "area: summary" is Git's own convention (fact
  `area-prefix`). Pick one, and write it down.
