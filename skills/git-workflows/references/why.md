# Why: the reasons behind these rules, what others do, and what each choice costs

Read this when you want to know why a rule says what it does, when a repository you respect does
it differently, or when you're deciding whether a rule fits your project. Each section gives
this skill's advice, the reason, what other projects do and why, what each choice costs, when to
choose differently, and what could still be better. The rules are numbered as in `SKILL.md`.
Facts are named by ID from `facts.md`, where each has its source and the date it was checked.

Checked 2026-09-30.

## Contents

1. The merge strategy
2. Deleting branches
3. Rewriting history
4. Going around a check
5. The commit grammar
6. Hardening workflows
7. Releasing from a tag
8. Reading Git's output
9. Release lines and backports
10. How long CI should take, and where it should run

## 1. The merge strategy

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
| Rebase-merge | A straight line that keeps each commit's content | Every commit gets a new ID, so it strands citations just as squash does |
| One reviewed commit (Gerrit) | The reviewed commit is the landed one | It needs a review tool built for it, and authors amend rather than add commits |

**When to choose differently.** If nothing outside the repository cites commits, for example
in a solo project whose records cite pull request numbers, squash is simpler and loses nothing
you use.

**What could be better.** Cite pull request numbers or tags, which survive any strategy, rather
than commit IDs. Then the strategy becomes a matter of taste. The rule stays because citations
already written can't be changed after the fact.

## 2. Deleting branches

**The advice.** Check what still needs a branch before you delete it: its pull request, commits
cited only there, a release line, a sibling repository. Never bulk-delete from
`git branch -r --merged`.

**Why.** Deleting is the step that strands a commit. `--merged` asks whether a branch's tip is
an ancestor of the target, and after a squash or rebase-merge it never is, so it can't tell a
squashed branch from abandoned work.

**What others do.** GitHub can delete head branches automatically once their pull requests
merge (fact `auto-delete`), which keeps the branch list short. Under merge commits that loses
nothing. Under squash it strands the branch's commits the moment the pull request merges. Git
2.56 added
`git branch --delete-merged`, which deletes a local branch only when its upstream holds its tip
(fact `delete-merged`). Projects with release lines, such as FFmpeg, keep those branches
indefinitely.

**What each choice costs.** Automatic deletion costs nothing until a cited commit goes. The
manual check takes minutes for each branch.

**What could be better.** A script that looks for each branch's commit IDs in pull request
bodies and the decision record before deleting it would make the check routine.

## 3. Rewriting history

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

## 4. Going around a check

**The advice.** No `--no-verify`, and no skipping or quarantining a failing test to get to
green.

**Why.** A skipped check reports nothing, and a quarantined test goes on failing where nobody
looks. An assistant under pressure to finish will take either route unless it's ruled out.

**What others do.** Large projects do take flaky tests out of the blocking path, but with
machinery behind it. Google classifies flakes by statistics across the company, so an engineer
can tell whether their change broke a test or the test is unstable (fact `google-presubmit`).
Chromium's commit queue runs some jobs as experiments, which report without blocking (fact
`chromium-cq`). In both, someone owns the test, and its failures stay visible.

**When to choose differently.** Quarantine is reasonable when a named person owns the test,
there is an open issue, and its results stay visible. The rule forbids the version with none of
these.

## 5. The commit grammar

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

## 6. Hardening workflows

**The advice.** Put `permissions:` at the top, a timeout on every job, actions pinned to a full
commit SHA, installs that fail on lockfile drift, CI on the branches where work happens, and no
path filter on a required check.

**Why, one by one.**
- **SHA pins.** A tag can be moved. In March 2025 an attacker moved every tag of
  `tj-actions/changed-files` onto a commit that printed secrets into build logs (fact
  `tj-actions`). Workflows pinned by tag ran it; workflows pinned by SHA didn't. A full SHA is
  the only immutable reference (fact `sha-pin`).
- **Permissions.** A token that can only read can't be used to write, whatever a compromised
  step tries.
- **Timeouts.** A hung job otherwise runs for six hours (fact `timeout`), and holds a runner
  that other jobs wait for.
- **Lockfile drift.** An install that quietly resolves new versions tests code nobody reviewed
  (fact `uv-locked`).
- **Path filters.** A required check that a filter skips stays pending, so the pull request
  can't merge (fact `skipped-pending`). The opposite trap: a job skipped by its own `if:`
  reports success, even when it is required (fact `job-if-success`).

**What others do.** GitHub's starter workflows pin GitHub's own actions by tag, which reads
easily and picks up fixes within a major version, but require every other action to be pinned
by SHA (fact `starter-pins`). Many projects keep tag pins for the same convenience.

**What each choice costs.** SHA pins need a bot, such as Dependabot, to raise updates, and they
get no security fix until you take that update.

**What could be better.** Require SHA pinning by policy (fact `sha-policy`), so no pull request
can bring back a tag pin.

## 7. Releasing from a tag

**The advice.** Release from an annotated tag on a commit whose CI you've read, after the
changelog entry.

**Why.** Git's own documentation keeps annotated tags for releases (fact `tag-kinds`), and
`git describe` counts only annotated tags unless told otherwise (fact `describe`). An annotated
tag records who tagged, when, and why. A tag on a commit whose CI you haven't read releases
whatever that commit holds.

**What others do.** Many projects release with `gh release create` or GitHub's release page. Given
a new tag name, `gh` makes the tag itself, and to release from an annotated tag you push that tag
first (fact `gh-release-tag`). semantic-release works out the version from the commit messages
and publishes it (fact `semantic-release`). For changelogs, towncrier builds notes from one file per
change, so parallel pull requests don't conflict over one shared file (fact `towncrier`).

**What each choice costs.** An annotated tag made by a job takes one more step than clicking
"Publish release". A generated changelog saves writing, but reads like the commit log it came
from.

## 8. Reading Git's output

**The advice.** Read merge and rebase output whole, check for conflict markers in CI, and never
read an exit status through a pipe.

**Why.** Git lists every conflict in its output. Trimming that output for readability hides
the one that matters, and Markdown with conflict markers still passes every test that doesn't
parse it. `cmd | tail` reports `tail`'s exit status, not the command's.

## 9. Release lines and backports

**The advice.** Keep a second release line only when users need one. Backport with
`git cherry-pick -x`, one focused pull request per fix.

**What others do.**

| Project | Practice | Its reason |
|---|---|---|
| Linux kernel | A fix goes into mainline first, then back to stable lines, at most 100 lines each (fact `kernel-stable`) | A fix that exists only on a stable line regresses at the next upgrade |
| Git | Bug fixes build up on `maint`, and `master` contains all of `maint` (fact `git-branches`) | One commit ID serves both lines, so nothing needs `-x` |
| FFmpeg | Cherry-picks with `-x` on each release branch | Each backport names its source commit |

**What each choice costs.** Merging forward keeps a single commit ID, but the fix has to be
written against the old code. Cherry-picking back is simpler when the lines have drifted apart,
and `-x` records where each copy came from (fact `cherry-x`).

## 10. How long CI should take, and where it should run

**The advice.** Run fast, reliable checks before merge, and make sure the full suite runs on
what lands. Weaken no test to save time: change where and how often it runs.

**The evidence.**
- Fowler: "the XP guideline of a ten minute build is perfectly within reason", with slower tests
  in later stages of the pipeline (fact `fowler-build`).
- Google: before submit, "only fast, reliable ones", catching the rest after submit and
  accepting "some number of rollbacks" (fact `google-presubmit`).
- Chromium's commit queue runs only the suites a change might affect (fact `chromium-cq`).
- Kubernetes runs presubmit, postsubmit and periodic jobs (fact `prow-jobs`).
- LLVM reviews after commit as well as before, and reverts first when a commit breaks something
  (fact `llvm-policy`).
- Rust runs a short subset on each push to a pull request (fact `rust-pr-builds`), and the full
  suite once, on the merge commit that becomes the main branch (fact `rust-queue`). Nothing runs
  it again after the push, because it is the same commit.

**How GitHub decides what was tested.**
- A `pull_request` run tests the merge of the branch into its base, not the branch's head (fact
  `pr-merge-ref`).
- With strict required checks, the default, a branch must be up to date before it merges, so
  the tree that lands is a tree that was tested (fact `strict-checks`).
- Without them, two pull requests can each pass and fail together once merged (fact
  `loose-checks`). Then the run on the default branch is what catches it.
- A merge queue gives strict's guarantee without making every author update their branch, but
  only in organization-owned repositories (fact `merge-queue`).

**Is the run on the default branch needed?** Compare its jobs with the pull request's:

| What the default branch's run does | Pull requests merge | Verdict |
|---|---|---|
| The same jobs as the pull request | Strictly, or through a queue | It tests a tree that was already tested. Keep only what differs there: deploys, publishing, tests that need secrets, filling the cache (fact `cache-scope`) |
| The same jobs as the pull request | Loosely | It catches two changes that pass alone and fail together. Keep it, or merge strictly, or use a queue |
| More suites than the pull request | Either | This is the split Google, LLVM and Kubernetes use. It's sound if a red run on the default branch gets a revert at once. Otherwise move those suites before merge, as Rust does |

**Making it faster without testing less.**
- Measure first: a job's steps are timed in its log, and queueing, setup and installs often
  cost more than the tests.
- Run independent jobs in parallel, and split a long suite across jobs.
- Cache dependencies and build outputs.
- Cancel a pull request's superseded run when a new push arrives (fact `cancel-in-progress`).
  Don't cancel on the default branch, where every commit should be tested.
- Don't run every job twice. `push` on every branch plus `pull_request` tests each pull
  request's commits once as the head and once as the merge. That doubles the minutes, and on a
  Free account the two runs share 20 concurrent jobs (fact `concurrent-jobs`).
- Put fast checks, such as lint and types, in their own job, so a failure shows in a minute.

**When to choose differently.** A repository that deploys from its default branch on every
merge needs the full suite before merge, because a red run after merge has already shipped.

**What could be better.** This skill advises `push` on every branch plus `pull_request`, so that
branches without a pull request, which agents' cloud sessions often push, still get CI. That
runs each pull request's commits twice. It costs about a minute in this skill's own repository,
but it would double a 15-minute suite. The alternative is `push` on the default branch only,
plus `pull_request`, and opening a draft pull request for every branch.
