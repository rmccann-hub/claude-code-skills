# Branches and merging

Read this for choosing a branching model, protecting the default branch, choosing and enforcing
the merge strategy, or moving off Git Flow or `master`.

Deleting a branch, rebasing, conflicts and recovering a lost commit are
`rebasing-and-recovery`. What a commit says is `commits-and-pull-requests`, a pull request's
checks are `ci-workflows`, and release lines are `releases-and-versions`.

## Rules

1. **Choose the merge strategy by whether anything cites your commits.** A merge commit keeps a
   branch's commits. Squash and GitHub's rebase-merge write new ones (fact `rebase-merge`), so
   cited commits leave the default branch's history, and once the branch goes they survive only
   under the pull request's own refs, which a clone doesn't fetch (fact `pr-refs`). Record the
   choice and its reason in the context file, and allow only that strategy.

### Choose a branching model

- **Short-lived branches off the default branch are the default,** each merged through a pull
  request within a day or two. This is GitHub Flow (fact `github-flow`), a form of trunk-based
  development, and DORA's research favors it (fact `dora`). Why a pull request earns its place
  with one maintainer is project-bootstrap-and-audit's *Review, with one maintainer*.
- **Add release lines only when you support more than one released version**
  (`releases-and-versions`).
- **A long-lived `develop` branch, as in Git Flow, costs more than it buys for most projects.**
  It suits a project that must hold releases back for a separate stabilization stage. Git
  Flow's own author now advises a simpler workflow for software delivered continuously (fact
  `gitflow-note`).

### Protect the default branch

- Require a pull request, require the CI checks, and block force pushes and deletion. Use
  rulesets or classic branch protection, whichever your plan allows
  (project-bootstrap-and-audit's *Facts with an expiry date*).
- **Import the ruleset rather than building it by hand,** from a JSON file under Settings,
  Rules, Rulesets (fact `ruleset-import`), in the shape of GitHub's starter rulesets (fact
  `ruleset-recipes`). [assets/rulesets/default-branch.json](../assets/rulesets/default-branch.json)
  blocks deletion and force pushes, and requires a pull request with no approval, which suits
  one maintainer (fact `pr-rule`). Then add the CI checks under "Require status checks to
  pass", by the names their jobs report. It allows merge commits only, so the strategy holds
  whatever the Pull Requests setting says. Where the context file records squash or rebase,
  change `allowed_merge_methods` before importing.
- **A required check must report on every pull request.** `ci-workflows` says how.

### Choose one merge strategy, and enforce it

| Strategy | What lands on the base | Are the branch's commits kept? | Choose it when |
|---|---|---|---|
| Merge commit | The branch's commits, plus a merge commit | Yes | Anything outside the repository cites commits by hash: pull request bodies, decision records, run reports, another repository. Or the branch's history matters |
| Squash | One new commit per pull request | No | Nothing outside cites the branch's commits, and you want one commit per reviewed change |
| Rebase and merge | The branch's commits, rewritten | No, they get new IDs (fact `rebase-merge`) | You want linear history, and nothing outside cites the branch's commits |

- **Allow only the recorded one** under Settings, General, Pull Requests, turning the other two
  off. project-bootstrap-and-audit rates the choice and its enforcement (dimension 6,
  *Merging*). Locally, `git merge --no-ff` makes a merge commit, and `git merge --ff-only`
  refuses anything else.

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

## Mistakes

- **Squash-merging, then deleting the branch, where commits are cited.** The cited commits leave
  the default branch (facts `rebase-merge`, `pr-refs`). One live repository lost its cited
  commits four minutes after a squash merge, when the branch was deleted. Use merge commits
  there.
- **`git init`, then `git push -u origin main`, when the new branch is `master`.** Use
  `git init -b main`, or set `init.defaultBranch`.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`. A public
repository's rulesets read without a token; its merge settings need write access (fact
`rest-public`). A check you can't read is `UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The merge strategy is recorded, with its reason | The context file (`AGENTS.md` or `CLAUDE.md`) and the decision record | `GAP` from T2 if missing | Record it, with the reason: whether anything cites commits |
| The platform allows only the recorded strategy | Settings, General, Pull Requests, or `gh api repos/OWNER/REPO --jq '.allow_merge_commit, .allow_squash_merge, .allow_rebase_merge'` | `GAP` from T2 if more are on | Turn the others off |
| Squash or rebase-merge where commits are cited from outside | Commit IDs in pull request bodies, the decision record and sibling repositories, each checked with `git merge-base --is-ancestor <commit> origin/main` after fetching every branch | `GAP`, naming each stranded commit | Merge commits. A stranded commit is still fetchable as `pull/<number>/head` (fact `pr-refs`): tag it and push the tag |
| Head branches auto-delete under squash or rebase-merge | Settings, General (fact `auto-delete`) | `GAP` where commits are cited | Turn it off, or move to merge commits |
| The default branch can be pushed to directly, deleted or force-pushed | `gh api repos/OWNER/REPO/rulesets` and each one's rules, or `gh api repos/OWNER/REPO/branches/BRANCH/protection` | `GAP` where the plan allows rulesets; `N/A` where it doesn't | Import `assets/rulesets/default-branch.json` (fact `ruleset-import`), then add the CI checks |

## Why

### The merge strategy

**The advice.** Where anything outside the repository names commit IDs, merge with a merge
commit.

**Why.** Squash and rebase-merge write new commits (fact `rebase-merge`). A citation still
names the old ones, which the default branch never holds.

**What others do.** Where a project gives its own reason, it is quoted.

| Project | Practice | What it gets them |
|---|---|---|
| Linux kernel | Merge commits, and published history left alone (fact `kernel-merges`) | "given the scale of the project, avoiding merges would be nearly impossible" |
| Git | Topics merge into `next`, then `master`; `master` and `maint` are never rewound, while `seen` is rebuilt (fact `git-branches`) | People build on `master` and `maint`, and try out and drop topics in `seen` |
| Rust | A bot tests each approved pull request's merge commit, then pushes that commit (fact `rust-queue`) | What reaches the main branch is exactly what was tested |
| CPython | Squash merges, with review on the unsquashed commits (fact `cpython-squash`) | One commit per change on the main branch, while reviewers still see each step |
| Go | One commit per change, amended through review in Gerrit and tied together by `Change-Id` (fact `go-subject`) | The reviewed commit lands, so no cited commit disappears |

**What each choice costs.**

| Strategy | Gains | Costs |
|---|---|---|
| Merge commit | Every commit ID survives; `git bisect` can go inside a branch; attribution stays per commit | History forks and joins, and it keeps "fix typo" commits unless authors tidy their branch first |
| Squash | One commit per pull request; a clean revert; a readable `git log --first-parent` without effort | Branch commits lose their IDs; per-step history is gone; co-authors survive only as trailers |
| Rebase-merge | A straight line that keeps each commit's content | Every commit gets a new ID, so it strands citations as squash does |
| One reviewed commit (Gerrit) | The reviewed commit is the landed one | It needs a review tool built for it, and authors amend rather than add commits |

**When to choose differently.** If nothing outside the repository cites commits, for example
a solo project whose records cite pull request numbers, squash is simpler and loses nothing
you use.

**What could be better.** Cite pull request numbers or tags, which survive any strategy, rather
than commit IDs, and the strategy becomes a matter of taste. The rule stays because written
citations can't change.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `rebase-merge` | GitHub's "Rebase and merge" gives each of the branch's commits a new ID | [About merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github) | "Always updates the committer information and creates new commit SHAs" | 2026-09-30 | 2027-03-31 |
| `pr-refs` | A pull request's commits stay fetchable from `pull/<number>/head`, after the branch is gone | [Checking out pull requests locally](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/checking-out-pull-requests-locally) | "git fetch origin pull/ID/head:BRANCH_NAME" | 2026-09-30 | 2027-03-31 |
| `ruleset-import` | A ruleset can be imported from a JSON file, under Settings, Rules, Rulesets | [Managing rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository) | "You can import an existing ruleset using a JSON file." and "Select the New ruleset dropdown, then click Import a ruleset" | 2026-10-05 | 2027-04-05 |
| `ruleset-recipes` | GitHub publishes starter rulesets as JSON files to import | [ruleset-recipes README](https://raw.githubusercontent.com/github/ruleset-recipes/main/README.md) | "Starter rulesets are pre-baked to make it easy to get started with" | 2026-10-05 | 2027-04-05 |
| `pr-rule` | A ruleset's pull request rule needn't require an approval | [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) | "The pull request doesn't necessarily have to be approved, but it must be opened." | 2026-10-05 | 2027-04-05 |
| `rest-public` | A public repository's repository, rulesets and branch-rules endpoints need no token; merge settings need contents write, a ruleset's bypass list write access | [Repositories API](https://docs.github.com/en/rest/repos/repos), [Rules API](https://docs.github.com/en/rest/repos/rules) | "can be used without authentication or the aforementioned permissions if only public resources are requested" and "To view merge-related settings, you must have the contents:read and contents:write permissions." and "the bypass_actors property is only returned if the user" | 2026-10-27 | 2027-04-27 |
| `github-flow` | GitHub flow: one main branch, and a short-lived branch per change | [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) | "GitHub flow is a lightweight, branch-based workflow." | 2026-09-30 | 2027-03-31 |
| `dora` | DORA's trunk-based guidance: three or fewer active branches, merged to trunk at least daily | [dora.dev](https://dora.dev/capabilities/trunk-based-development/) | "Have three or fewer active branches" | 2026-09-30 | 2027-09-30 |
| `gitflow-note` | Git Flow's author advises a simpler workflow for software delivered continuously | [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | "adopt a much simpler workflow (like GitHub flow)" | 2026-09-30 | 2027-09-30 |
| `kernel-merges` | The Linux kernel merges with merge commits, and asks that published history stay unchanged | [Rebasing and merging](https://docs.kernel.org/maintainer/rebasing-and-merging.html) | "given the scale of the project, avoiding merges would be nearly impossible" and "History that has been exposed to the world beyond your private system should usually not be changed." | 2026-09-30 | 2027-03-31 |
| `git-branches` | Git merges topics into `next`, then `master`. `master` and `maint` are never rewound, `seen` is rebuilt, and fixes build up on `maint`, which `master` contains | [maintain-git](https://raw.githubusercontent.com/git/git/master/Documentation/howto/maintain-git.adoc) | "The tips of 'master' and 'maint' branches will not be rewound" and "Usually 'master' contains all of 'maint' and 'next' contains all of 'master'." and "is rebuilt directly on 'master'" | 2026-09-30 | 2027-03-31 |
| `cpython-squash` | CPython squash-merges pull requests, and asks contributors not to squash or force-push during review | [Pull request lifecycle](https://devguide.python.org/getting-started/pull-request-lifecycle/) | "CPython uses squash merges, so PRs will end up as single commits when merged." and "Reviewers often want to look at individual commits." | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (merge methods, branch deletion, pull request refs, rulesets, REST API, GitHub flow) and [github/ruleset-recipes](https://github.com/github/ruleset-recipes) | Merging and protecting branches, and the ruleset's shape | Docs CC BY 4.0: our own words, short quotes. Recipes: pointed to, not copied |
| [Git's maintainer howto](https://github.com/git/git/tree/master/Documentation/howto) | Git's own branches | GPL-2.0: our own words, short quotes |
| [DORA](https://dora.dev/) and [Git Flow's author](https://nvie.com/posts/a-successful-git-branching-model/) | Branching evidence, and Git Flow's author's advice | DORA not stated; the post CC BY-SA: short quotes, with the link |
| [Linux kernel](https://docs.kernel.org/) and [CPython devguide](https://devguide.python.org/) | How large projects merge | Not stated on the pages: short quotes only |
| Two live repositories of this skill's owner, unnamed here | Squash merges that stranded cited commits | Observed practice, in our own words |
