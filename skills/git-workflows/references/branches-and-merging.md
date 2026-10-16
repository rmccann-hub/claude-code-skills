# Branches and merging

Read this for choosing a branching model, protecting the default branch, choosing and enforcing
the merge strategy, deleting a branch, rebasing your own branch, resolving a conflict, recovering
a lost commit, or moving off Git Flow or `master`.

It covers the shape of history and what keeps it intact. What a commit says is
`commits-and-pull-requests`; the checks a pull request must pass are `ci-workflows`; release
lines are `releases-and-versions`.

## Rules

1. **Choose the merge strategy by whether anything cites your commits.** A merge commit keeps a
   branch's commits. Squash and GitHub's rebase-merge write new ones (fact `rebase-merge`), so
   cited commits leave the default branch's history, and once the branch goes they survive only
   under the pull request's own refs, which a clone doesn't fetch (fact `pr-refs`). Record the
   choice in the context file, and allow only that strategy in the repository's settings.
2. **Never delete a branch until you've checked what still needs it:** its pull request,
   commits cited only there, a release line, a sibling repository. Never bulk-delete remote
   branches from `git branch -r --merged`.
3. **Never rewrite shared or cited history.** No force-push to a shared branch, and no amend of
   a pushed or cited commit. Revert, or add a commit. The one exception is removing personal
   information at the owner's request, which `leaked-data` lays out.
4. **Read Git's output whole.** Merge and rebase output lists the conflicts. Check for conflict
   markers in CI. Read Git's paths with `-z`.

### Choose a branching model

- **Short-lived branches off the default branch are the default,** each merged through a pull
  request within a day or two. This is GitHub Flow (fact `github-flow`), a form of trunk-based
  development, and DORA's research favors it (fact `dora`). Why a pull request earns its place
  even with one maintainer is project-bootstrap-and-audit's *Review, with one maintainer*.
- **Add release lines only when you support more than one released version**
  (`releases-and-versions`).
- **A long-lived `develop` branch, as in Git Flow, costs more than it buys for most projects.**
  It suits a project that must hold releases back for a separate stabilization stage. Git
  Flow's own author now advises a simpler workflow for software delivered continuously (fact
  `gitflow-note`).

### Protect the default branch

- Require a pull request, require the CI checks, and block force pushes and deletion. Use
  rulesets or classic branch protection. Which your plan allows is in
  project-bootstrap-and-audit's *Facts with an expiry date*.
- **Import the ruleset rather than building it by hand.** It imports from a JSON file, through
  the New ruleset menu under Settings, Rules, Rulesets (fact `ruleset-import`), in the shape
  GitHub's own starter rulesets use (fact `ruleset-recipes`).
  [assets/rulesets/default-branch.json](../assets/rulesets/default-branch.json) blocks deletion
  and force pushes, and requires a pull request with no approval, which suits one maintainer
  (fact `pr-rule`). After importing it, add the CI checks under "Require status checks to
  pass", by the names their jobs report, which a template can't know. It allows merge commits
  only, so the strategy holds even if the repository's Pull Requests setting is changed. Where
  the context file records squash or rebase instead, change `allowed_merge_methods` before
  importing.
- **A required check must report on every pull request.** `ci-workflows` says how.

### Choose one merge strategy, and enforce it

| Strategy | What lands on the base | Are the branch's commits kept? | Choose it when |
|---|---|---|---|
| Merge commit | The branch's commits, plus a merge commit | Yes | Anything outside the repository cites commits by hash: pull request bodies, decision records, run reports, another repository. Or the branch's history matters |
| Squash | One new commit per pull request | No | Nothing outside cites the branch's commits, and you want one commit per reviewed change |
| Rebase and merge | The branch's commits, rewritten | No, they get new IDs (fact `rebase-merge`) | You want linear history, and nothing outside cites the branch's commits |

- **Where commits are cited from outside, only a merge commit keeps them.** Under squash or
  rebase-merge, the cited commits exist only on the branch, and deleting the branch strands
  them. One live repository lost its cited commits four minutes after a squash merge, when the
  branch was deleted.
- **Record the choice and its reason in the context file, then allow only that one** under
  Settings, General, Pull Requests, with the other two turned off. project-bootstrap-and-audit
  rates the choice and its enforcement (dimension 6, *Merging*).
- **Updating a branch:** rebase a branch only you use onto the base. Merge the base into a
  branch others share, because rebasing rewrites commits they already have. Locally,
  `git merge --no-ff` makes a merge commit and `git merge --ff-only` refuses anything else.

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
- **Git 2.56's `git branch --delete-merged`** deletes local branches whose tip is on their
  upstream, with `--dry-run` to preview (fact `delete-merged`). It leaves alone a branch whose
  upstream is gone, and one whose push would update that upstream, which covers most branches
  made with `git push -u`. It suits branches that track a shared branch such as `origin/main`.
- **Never bulk-delete remote branches** by piping `git branch -r --merged` into
  `git push --delete`. `--merged` knows nothing of squash merges, citations or sibling
  repositories.
- **GitHub's "Automatically delete head branches" setting** (fact `auto-delete`) is safe under
  merge commits, where the branch's commits live on in the base. Under squash or rebase-merge
  it takes the branch the moment the pull request merges, and with it every commit only that
  branch held.

### Rebasing your own branch, conflicts and recovery

- **Push a rebased branch with `git push --force-with-lease --force-if-includes`.** The first
  refuses when the remote branch has moved since you last fetched it. The second also refuses
  when a fetch brought in commits you never looked at, which the first can't tell apart (fact
  `force-if-includes`). Plain `--force` overwrites whatever is there. Rebase only a branch
  nobody else has.
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

- **From Git Flow to short-lived branches:**
  1. Stop branching new work from `develop`; branch from the default branch instead.
  2. Merge `develop` into the default branch through one pull request, with a merge commit.
  3. Retarget the open pull requests at the default branch.
  4. Delete `develop` only once no open pull request targets it, no release line needs it, and
     no commit found only on it is cited anywhere.
  5. Update the context file and the contributing guide, so no one recreates it.
- **From `master` to `main`:**
  1. Rename the branch on GitHub. It redirects the old name, and retargets open pull requests.
  2. In each clone: `git branch -m master main`, then `git fetch origin`, then
     `git branch -u origin/main main`, then `git remote set-head origin -a`.
  3. Update CI's `on:` branch filters, rulesets and scripts that name `master`.
- **Towards SHA-256 repositories:** Git 3.0 will make SHA-256 the default for new repositories
  (fact `git3`). Stop treating commit IDs as 40 characters in scripts, regular expressions and
  database columns, and accept 64.
- **From hand-written branch cleanup to `--delete-merged`:** for local branches, from Git 2.56,
  `git branch --dry-run --delete-merged 'origin/*'`, then without `--dry-run` (fact
  `delete-merged`). Remote branches are still checked one at a time, against their pull
  requests and anything that cites their commits.

## Mistakes

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
- **Validating commit IDs as exactly 40 hex characters.** SHA-256 repositories use 64, and Git
  3.0 makes SHA-256 the default for new repositories (fact `git3`).
- **`git init`, then `git push -u origin main`, when the new branch is `master`.** Use
  `git init -b main`, or set `init.defaultBranch`.
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

Severity uses the standard's status words, defined in this skill's `SKILL.md`. A check read
from the repository's settings needs admin access, or it's `UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The merge strategy is recorded, with its reason | The context file (`AGENTS.md` or `CLAUDE.md`) and the decision record | `GAP` from T2 if missing | Record it in the context file, with the reason: whether anything cites commits |
| The platform allows only the recorded strategy | Settings, General, Pull Requests, or `gh api repos/OWNER/REPO --jq '.allow_merge_commit, .allow_squash_merge, .allow_rebase_merge'` | `GAP` from T2 if more are on | Turn the others off |
| Squash or rebase-merge where commits are cited from outside | Search pull request bodies, the decision record and sibling repositories for commit IDs, then check each with `git merge-base --is-ancestor <commit> origin/main`, after fetching every branch | `GAP`, naming each stranded commit | Merge commits. A stranded commit is still fetchable as `pull/<number>/head` (fact `pr-refs`): tag it and push the tag |
| Head branches auto-delete under squash or rebase-merge | Settings, General (fact `auto-delete`) | `GAP` where commits are cited | Turn it off, or move to merge commits |
| Conflict markers in tracked files | The command below the table | `BLOCKER` | Resolve them, and add the CI form below |
| The default branch can be pushed to directly, deleted or force-pushed | `gh api repos/OWNER/REPO/rulesets`, each ruleset's rules, and `gh api repos/OWNER/REPO/branches/BRANCH/protection` for classic protection | `GAP` where the plan allows rulesets; `N/A` where it doesn't | Import `assets/rulesets/default-branch.json` (fact `ruleset-import`), then add the CI checks |

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

### The merge strategy

**The advice.** Choose by whether anything cites your commits. Where pull request bodies,
decision records, run reports or other repositories name commit IDs, merge with a merge commit.

**Why.** Squash and GitHub's rebase-merge write new commits (fact `rebase-merge`). A citation
still names the old ones, which the default branch never holds. The old commits live on only
under the pull request's own refs, and a reader who clones the repository doesn't get those.

**What others do.**

| Project | Practice | What it gets them |
|---|---|---|
| Linux kernel | Merge commits, and published history left alone (fact `kernel-merges`) | In its own words, "given the scale of the project, avoiding merges would be nearly impossible" |
| Git | Topics merge into `next`, then `master`; `master` and `maint` are never rewound, while `seen` is rebuilt (fact `git-branches`) | People can build on `master` and `maint`, and topics can still be tried out and dropped in `seen` |
| Rust | A bot tests each approved pull request's merge commit, then pushes that commit (fact `rust-queue`) | What reaches the main branch is exactly what was tested |
| CPython | Squash merges, with review on the unsquashed commits (fact `cpython-squash`) | One commit per change on the main branch, while reviewers still see each step |
| Go | One commit per change, amended through review in Gerrit and tied together by `Change-Id` (fact `go-subject`) | The commit that lands is the one that was reviewed, so no cited commit disappears |

The third column says what each practice achieves. Where a project gives its own reason, it is
quoted.

**What each choice costs.**

| Strategy | Gains | Costs |
|---|---|---|
| Merge commit | Every commit ID survives; `git bisect` can go inside a branch; attribution stays per commit | History forks and joins, and it keeps "fix typo" commits unless authors tidy their branch before review |
| Squash | One commit per pull request; a clean revert; a readable `git log --first-parent` without effort | Branch commits lose their IDs; per-step history is gone; co-authors survive only as trailers |
| Rebase-merge | A straight line that keeps each commit's content | Every commit gets a new ID, so it strands citations as squash does |
| One reviewed commit (Gerrit) | The reviewed commit is the landed one | It needs a review tool built for it, and authors amend rather than add commits |

**When to choose differently.** If nothing outside the repository cites commits, for example
in a solo project whose records cite pull request numbers, squash is simpler and loses nothing
you use.

**What could be better.** Cite pull request numbers or tags, which survive any strategy, rather
than commit IDs. Then the strategy becomes a matter of taste. The rule stays because citations
already written can't be changed after the fact.

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
| `rebase-merge` | GitHub's "Rebase and merge" writes new commits, so the branch's commit IDs don't reach the base | [About merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github) | "Always updates the committer information and creates new commit SHAs" | 2026-09-30 | 2027-03-31 |
| `auto-delete` | A repository can delete head branches automatically once their pull requests merge | [Managing the automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches) | "You can have head branches automatically deleted after pull requests are merged in your repository." | 2026-09-30 | 2027-03-31 |
| `pr-refs` | A pull request's commits stay fetchable from `pull/<number>/head`, after the branch is gone | [Checking out pull requests locally](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/checking-out-pull-requests-locally) | "git fetch origin pull/ID/head:BRANCH_NAME" | 2026-09-30 | 2027-03-31 |
| `ruleset-import` | A repository's ruleset can be imported from a JSON file, through the New ruleset menu under Settings, Rules, Rulesets | [Managing rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository) | "You can import an existing ruleset using a JSON file." and "Select the New ruleset dropdown, then click Import a ruleset" | 2026-10-05 | 2027-04-05 |
| `ruleset-recipes` | GitHub publishes starter rulesets as JSON files to import | [ruleset-recipes README](https://raw.githubusercontent.com/github/ruleset-recipes/main/README.md) | "Starter rulesets are pre-baked to make it easy to get started with" and "Select New Ruleset > Import a ruleset" | 2026-10-05 | 2027-04-05 |
| `pr-rule` | A ruleset's pull request rule requires that a pull request be opened, and needn't require an approval | [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) | "The pull request doesn't necessarily have to be approved, but it must be opened." | 2026-10-05 | 2027-04-05 |
| `github-flow` | GitHub flow: one main branch, and a short-lived branch per change | [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) | "GitHub flow is a lightweight, branch-based workflow." | 2026-09-30 | 2027-03-31 |
| `dora` | DORA's trunk-based guidance: three or fewer active branches, merged to trunk at least daily | [dora.dev](https://dora.dev/capabilities/trunk-based-development/) | "Have three or fewer active branches" | 2026-09-30 | 2027-09-30 |
| `gitflow-note` | Git Flow's author advises a simpler workflow for software that is delivered continuously | [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | "adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team" | 2026-09-30 | 2027-09-30 |
| `kernel-merges` | The Linux kernel merges maintainers' branches with merge commits, and asks that published history stay unchanged | [Rebasing and merging](https://docs.kernel.org/maintainer/rebasing-and-merging.html) | "the kernel community is not scared by seeing merge commits in its development history" and "given the scale of the project, avoiding merges would be nearly impossible" and "History that has been exposed to the world beyond your private system should usually not be changed." | 2026-09-30 | 2027-03-31 |
| `git-branches` | Git merges topics into `next` and then `master`. `master` and `maint` are never rewound, `seen` is rebuilt from `master`, and bug fixes build up on `maint`, which `master` contains | [maintain-git](https://raw.githubusercontent.com/git/git/master/Documentation/howto/maintain-git.adoc) | "The tips of 'master' and 'maint' branches will not be rewound" and "Usually 'master' contains all of 'maint' and 'next' contains all of 'master'." and "is rebuilt directly on 'master'" | 2026-09-30 | 2027-03-31 |
| `cpython-squash` | CPython squash-merges pull requests, and asks contributors not to squash or force-push during review | [Pull request lifecycle](https://devguide.python.org/getting-started/pull-request-lifecycle/) | "CPython uses squash merges, so PRs will end up as single commits when merged." and "Reviewers often want to look at individual commits." | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-branch, git-checkout, git-config, git-push, git-reflog, git-rerere, BreakingChanges), and Git's [maintainer howto](https://raw.githubusercontent.com/git/git/master/Documentation/howto/maintain-git.adoc) | Commands, and Git's own branches | GPL-2.0: facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (merge methods, automatic branch deletion, checking out pull requests, rulesets, GitHub flow) | Merging, deleting and protecting branches | CC BY 4.0: facts in our own words, with short quotes |
| [github/ruleset-recipes](https://github.com/github/ruleset-recipes) | The shape of the ruleset to import | Pointed to, not copied |
| [DORA: trunk-based development](https://dora.dev/capabilities/trunk-based-development/) | Branching evidence | Not stated: a short quote, with the link |
| [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | Git Flow's author's own advice | CC BY-SA: a short quote |
| [Linux kernel: rebasing and merging](https://docs.kernel.org/maintainer/rebasing-and-merging.html) | Merges, and leaving published history alone | Not stated on the page: short quotes only |
| [CPython devguide](https://devguide.python.org/getting-started/pull-request-lifecycle/) | Squash merges, and review without force-pushes | Not stated on the page: short quotes only |
| Two live repositories of this skill's owner, unnamed here | Squash merges that stranded cited commits, a branch deleted four minutes after a squash merge | Observed practice, in our own words |
