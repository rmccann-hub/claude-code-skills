# Rebasing and recovery

Read this for deleting a branch, rebasing your own branch and pushing it, resolving a conflict,
recovering a lost commit, leaving shared history alone, reading Git's output, or commit IDs
longer than 40 characters.

The branching model, protecting the default branch and the merge strategy are
`branches-and-merging`. Removing a secret or personal information from history is
`leaked-data`.

## Rules

1. **Never delete a branch until you've checked what still needs it:** its pull request,
   commits cited only there, a release line, a sibling repository. Never bulk-delete remote
   branches from `git branch -r --merged`.
2. **Never rewrite shared or cited history.** No force-push to a shared branch, and no amend of
   a pushed or cited commit. Revert, or add a commit. The one exception is removing personal
   information at the owner's request, which `leaked-data` lays out.
3. **Read Git's output whole.** Merge and rebase output lists the conflicts. Check for conflict
   markers in CI. Read Git's paths with `-z`.

### Delete a branch only after checking what needs it

Before deleting a remote branch, check each of these:

1. **Its pull request is merged or closed.** Under squash or rebase-merge, "merged" can't be
   read from the history, because the branch's commits aren't in the base. Read the pull
   request's state.
2. **No commit that exists only on it is cited anywhere.** For each cited commit, run
   `git branch -r --contains <commit>`. It answers from the refs you have, so in a shallow or
   single-branch clone, such as CI's or a cloud session's, fetch every branch first, with
   `--unshallow` if `git rev-parse --is-shallow-repository` prints `true`. If this branch is
   the only answer, keep it, or tag the commit and push the tag:
   `git tag -a archive/<branch> -m "…" <commit>`, then `git push origin refs/tags/archive/<branch>`.
   A tag unpushed is lost with the clone, and a pushed tag starts any workflow that runs
   `on: push: tags` for that name. After a squash, the commits are still fetchable from the pull
   request itself: `git fetch origin pull/<number>/head` (fact `pr-refs`).
3. **Nothing else uses it:** an open pull request based on it, a release line, a CI
   configuration, a sibling repository's records. Where you can't check a sibling repository,
   ask its owner rather than guessing.

Then:

- **Local branches:** `git fetch --prune`, then `git branch -vv` marks as `gone` each branch
  whose remote branch was deleted. Check each one's pull request before deleting it: a remote
  branch can go without being merged. Plain `git branch -d` refuses a branch that isn't merged,
  and after a squash merge it always refuses. Use `-D` only after the checks above.
- **`git branch --delete-merged`,** new in Git 2.56, the current release (fact `git-current`),
  deletes local branches whose tip is on their upstream (fact `delete-merged`). Preview with
  `git branch --dry-run --delete-merged 'origin/*'`, then drop `--dry-run`. It leaves alone a
  branch whose upstream is gone, and one whose push would update that upstream, which covers
  most branches made with `git push -u`. It suits branches that track a shared branch such as
  `origin/main`.
- **Never bulk-delete remote branches** by piping `git branch -r --merged` into
  `git push --delete`. `--merged` knows nothing of squash merges, citations or sibling
  repositories.
- **GitHub's "Automatically delete head branches" setting** (fact `auto-delete`) is safe under
  merge commits, where the branch's commits live on in the base. Under squash or rebase-merge
  it takes the branch the moment the pull request merges, and with it every commit only that
  branch held.

### Rebasing your own branch, conflicts and recovery

- **Updating a branch:** rebase a branch only you use onto the base. Merge the base into a
  branch others share, because rebasing rewrites commits they already have.
- **Push a rebased branch with `git push --force-with-lease --force-if-includes`.** The first
  refuses when the remote branch has moved since you last fetched it. The second also refuses
  when a fetch brought in commits you never looked at, which the first can't tell apart (fact
  `force-if-includes`). Plain `--force` overwrites whatever is there.
- **On a conflict,** read the whole output, then `git status` lists the files. Resolve each
  one, `git add` it, and run `git rebase --continue` or `git merge --continue`. `--abort` puts
  everything back as it was before you started.
- **During a rebase, `--ours` and `--theirs` swap meaning:** `--ours` is the branch you're
  rebasing onto, and `--theirs` is your own work (fact `rebase-ours`).
- **A conflict you resolve again and again,** such as in a long-lived branch, can be recorded
  once: `git config rerere.enabled true` replays your resolution when it recurs (fact
  `rerere`).
- **A commit lost to a reset or a rebase** is still in the reflog, which records where each
  branch pointed (fact `reflog`). `git reflog` finds it, and `git branch rescue <commit>` gets
  it back. The reflog belongs to one clone, and it expires. Uncommitted work was never in it.

### Moving off older practice

- **Towards SHA-256 repositories:** Git 3.0 will make SHA-256 the default for new repositories
  (fact `git3`). Stop treating commit IDs as 40 characters in scripts, regular expressions and
  database columns, and accept 64.

## Mistakes

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
- **Validating commit IDs as exactly 40 hex characters.** SHA-256 repositories use 64, and Git
  3.0 makes SHA-256 the default for new repositories (fact `git3`).
- **Pushing a merged branch's commits again because a tool calls them unpushed.** Once GitHub
  deletes a merged pull request's branch, the local branch's upstream is gone, and a status
  line or a session's stop hook can count its commits as unpushed. They're on the default
  branch already. `git remote prune origin` and `git branch --unset-upstream` clear it, with
  nothing pushed.
- **Trimming a merge's or rebase's output for readability.** The conflict it listed goes unseen,
  and the markers ship. Read the whole output, and check for markers in CI.
- **Comparing paths Git printed with stored paths, without `-z`.** Git quotes a path holding
  a non-ASCII character, with octal escapes (fact `quotepath`), so it matches nothing stored.
  One check reported 29 files missing from a manifest that listed every one. Read `ls-files`,
  `ls-tree`, `diff --name-only` and `diff-tree` with `-z`, and split on NUL.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Conflict markers in tracked files | The command below the table | `BLOCKER` | Resolve them, and add the CI form below |

The conflict-marker search lists every line that starts with a merge's opening, closing or
base marker. It exits 0 when it finds some, 1 when the tree is clean, and 2 or more when the
search itself failed:

```sh
git grep -n -E '^(<{7}|>{7}|[|]{7})( |$)'
```

So in CI, where a pass must mean "no markers", invert it and keep its failures:

```sh
status=0
git grep -n -E '^(<{7}|>{7}|[|]{7})( |$)' || status=$?
if [ "$status" -eq 0 ]; then echo "::error::conflict markers found"; exit 1; fi
if [ "$status" -gt 1 ]; then echo "::error::the search failed"; exit "$status"; fi
```

## Why

### Deleting branches

**The advice.** Check what still needs a branch before you delete it: its pull request, commits
cited only there, a release line, a sibling repository. Never bulk-delete from
`git branch -r --merged`.

**Why.** Deleting is the step that strands a commit. `--merged` asks whether a branch's tip is
an ancestor of the target, and after a squash or rebase-merge it never is, so it can't tell a
squashed branch from abandoned work.

**What others do.** GitHub can delete head branches automatically once their pull requests
merge (fact `auto-delete`), which keeps the branch list short. Under merge commits that loses
nothing. Under squash it strands the branch's commits the moment the pull request merges. Git
2.56 added `git branch --delete-merged`, which deletes a local branch only when its upstream
holds its tip (fact `delete-merged`). Projects with release lines, such as FFmpeg, keep those
branches indefinitely.

**What each choice costs.** Automatic deletion costs nothing until a cited commit goes. The
manual check takes minutes for each branch.

**What could be better.** A script that looks for each branch's commit IDs in pull request
bodies and the decision record before deleting it would make the check routine.

### Rewriting history

**The advice.** Never force-push a shared branch, or amend a commit that is pushed or cited.
Revert, or add a commit.

**Why.** Anyone who has the old commits now has a history that disagrees with yours, and every
citation of a rewritten commit points at nothing. The kernel says the same: history "exposed to
the world beyond your private system should usually not be changed" (fact `kernel-merges`).

**What others do.** CPython asks contributors not to squash or force-push while a pull request
is under review, because "Reviewers often want to look at individual commits" (fact
`cpython-squash`). Gerrit projects such as Go amend all the time, but only the change under
review, before it lands (fact `go-subject`). What they share is that nothing is rewritten once
someone else relies on it.

**When to choose differently.** A branch only you have used, and nothing cites, is yours to
rebase and tidy. Push it with `--force-with-lease`, which refuses when someone else has pushed
since you last fetched.

### Reading Git's output

**The advice.** Read merge and rebase output whole, check for conflict markers in CI, and never
read an exit status through a pipe.

**Why.** Git lists every conflict in its output. Trimming that output for readability hides
the one that matters, and Markdown with conflict markers still passes every test that doesn't
parse it. `cmd | tail` reports `tail`'s exit status, not the command's.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `git-current` | Git 2.56.0, released 2026-09-28, is the current source release | [git-scm.com](https://git-scm.com/) | "Latest source release 2.56.0 Release Notes (2026-09-28)" | 2026-09-30 | 2026-12-31 |
| `git3` | Git 3.0 will make SHA-256 the default hash for new repositories, and has no release date | [BreakingChanges](https://git-scm.com/docs/BreakingChanges) | "There is no planned release date for this breaking version yet." | 2026-09-30 | 2026-12-31 |
| `delete-merged` | `git branch --delete-merged <pattern>` deletes local branches only when their tip is reachable from their configured upstream, and takes `--dry-run`. It skips a branch whose upstream is gone, and one whose push would update its upstream | [git-branch](https://git-scm.com/docs/git-branch) | "Delete local branches whose configured upstream matches <pattern>, but only when their tip is reachable from that upstream" and "A branch is not deleted when: its configured upstream ref no longer exists" and "would update its upstream" | 2026-09-30 | 2027-03-31 |
| `quotepath` | Git quotes a path holding a byte above 0x80 in its output, with octal escapes, unless the command is given `-z`. `core.quotePath` is true by default | [git-config](https://git-scm.com/docs/git-config) | "Many commands can output pathnames completely verbatim using the `-z` option. The default value is true." | 2026-10-15 | 2027-04-15 |
| `force-if-includes` | `git push --force-with-lease --force-if-includes` refuses a forced push when a fetch brought in remote commits you haven't integrated | [git-push](https://git-scm.com/docs/git-push) | "will verify if updates from the remote-tracking refs that may have been implicitly updated in the background are integrated locally before allowing a forced update" | 2026-09-30 | 2027-09-30 |
| `rebase-ours` | During a rebase, `--ours` is the branch being rebased onto, and `--theirs` is your own work | [git-checkout](https://git-scm.com/docs/git-checkout) | "during git rebase and git pull --rebase, ours and theirs may appear swapped" | 2026-09-30 | 2027-09-30 |
| `rerere` | `git rerere` records how a conflict was resolved, and reuses it | [git-rerere](https://git-scm.com/docs/git-rerere) | "Reuse recorded resolution of conflicted merges" | 2026-09-30 | 2027-09-30 |
| `reflog` | The reflog records where each branch pointed, in one clone | [git-reflog](https://git-scm.com/docs/git-reflog) | "record when the tips of branches and other references were updated in the local repository" | 2026-09-30 | 2027-09-30 |
| `auto-delete` | A repository can delete head branches automatically once their pull requests merge | [Managing the automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches) | "You can have head branches automatically deleted after pull requests are merged" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-branch, git-checkout, git-config, git-push, git-reflog, git-rerere, BreakingChanges) and [git-scm.com](https://git-scm.com/) | Commands, and Git's releases | GPL-2.0: facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (automatic branch deletion, checking out pull requests) | Deleting branches, and fetching a pull request's commits | CC BY 4.0: facts in our own words, with short quotes |
| [Linux kernel](https://docs.kernel.org/) and [CPython devguide](https://devguide.python.org/) | Leaving published history alone | Not stated on the pages: short quotes only |
