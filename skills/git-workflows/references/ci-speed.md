# CI speed

Read this for deciding how long CI should take and which suites run before and after a merge,
making CI faster without testing less, caching what a job builds, or a slow test, a timing test
or a timeout that comes and goes.

It covers how long checks take and where they run. Triggers, timeouts on every job, installs,
required checks and proving a gate are `ci-workflows`. How to design the tests themselves
belongs to a testing skill.

## Rules

1. **Weaken no test to save time.** Change where and how often it runs instead.
2. **Run fast, reliable checks before merge, and make sure the full suite runs on what lands.**
3. **Measure before you speed anything up.** A job's steps are timed in its log, and queueing,
   setup and installs often cost more than the tests.
4. **Pin what a job builds from source, then cache the result.**
5. **Know each slow test's headroom under its timeout,** and find the cause of a timeout before
   raising the limit.

### Builds and caching

**A job that clones its dependencies at their latest commit and builds them every run** is
slow, and isn't reproducible: CI's result and the shipped binary change with commits nobody
here made. One Windows job spent 19.5 of its 21 minutes building five libraries that way. Pin
each one to a tag or commit in one place, and cache the built output with `actions/cache`, keyed
on the pins, the build script's hash and the toolchain version.

### Making it faster without testing less

- Run independent jobs in parallel, and split a long suite across jobs.
- Cache dependencies and build outputs. A pull request restores caches from its own branch or
  the default branch, so the default branch's runs fill the cache pull requests read (fact
  `cache-scope`).
- Cancel a pull request's superseded run when a new push arrives (fact `cancel-in-progress`).
  Don't cancel on the default branch, where every commit should be tested.
- Don't run every job twice. `push` on every branch plus `pull_request` tests each pull
  request's commits once as the head and once as the merge (fact `pr-merge-ref`). That doubles
  the minutes, and on a Free account the two runs share 20 concurrent jobs (fact
  `concurrent-jobs`).
- Put fast checks, such as lint and types, in their own job, so a failure shows in a minute.

### Is the run on the default branch needed?

A `pull_request` run tests the merge of the branch into its base (fact `pr-merge-ref`). With
strict required checks, the default, a branch must be up to date before it merges, so the tree
that lands was tested (fact `strict-checks`). Without them, two pull requests can each pass and
fail together once merged (fact `loose-checks`), and the default branch's run catches it. A
merge queue gives strict's guarantee without making every author update their branch, but only
in organization-owned repositories (fact `merge-queue`). Compare the default branch's jobs with
the pull request's:

| What the default branch's run does | Pull requests merge | Verdict |
|---|---|---|
| The same jobs as the pull request | Strictly, or through a queue | It tests a tree that was already tested. Keep only what differs there: deploys, publishing, tests that need secrets, filling the cache (fact `cache-scope`) |
| The same jobs as the pull request | Loosely | It catches two changes that pass alone and fail together. Keep it, or merge strictly, or use a queue |
| More suites than the pull request | Either | This is the split Google, LLVM and Kubernetes use. It's sound if a red run on the default branch gets a revert at once. Otherwise move those suites before merge, as Rust does |

### Timing and timeouts

- **Set each job's timeout from its usual time, with room** (fact `timeout`).
- **A timing test asserts on growth, not on milliseconds.** Time the code at several input
  sizes far apart, and compare the ratios with room for noise. One test read 0.2 ms of runner
  noise as quadratic growth in a pattern measured linear.
- **Record each slow test's headroom under its timeout,** and act before it's gone. One suite's
  slowest test reached 87% of its timeout on a developer's machine, and timed out once on a CI
  runner the same week.
- **A timeout that comes and goes with no known cause is recorded, every time, with its
  numbers,** and the test is made to print where its time went, on passing runs too. One tree
  took from under half a minute to over two within an hour; the next timeout named its step.
  Raising the limit hides the cause.

## Mistakes

- **Diagnostics that print only when a test fails.** A test runner that shows output only for
  failures says nothing about a pass near its limit. One suite's new per-step timing reached
  nobody until a step read the runner's own results file after every run.
- **A build chain that goes on after a step fails.** Every earlier log of one Windows build
  carried a failed install, unseen, because the script ran each library's build whatever the
  last one returned. Stop at the first failure, and expect the first strict run to turn up old
  ones.
- **Raising a timeout that comes and goes,** with no record of its numbers. It hides the cause.
- **Canceling in-progress runs on the default branch.** A commit there goes untested.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A job builds its dependencies from unpinned source every run | `git clone` or a build script in `run:` steps, with no `actions/cache` | `GAP` | Pin each one in one place, and cache the output keyed on the pins |
| `cancel-in-progress` cancels default-branch runs | The `concurrency` block | `DRIFT` | Cancel only on `pull_request` (fact `cancel-in-progress`) |
| The default branch's run repeats the pull request's jobs, though nothing lands but through a strictly checked pull request or a queue | Both runs' jobs, the ruleset and its bypass list | `OVER` | Keep only what differs there, filling the cache among it (facts `strict-checks`, `cache-scope`) |

## Why

### How long CI should take, and where it should run

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

**When to choose differently.** A repository that deploys from its default branch on every
merge needs the full suite before merge, because a red run after merge has already shipped.

**What could be better.** git-workflows advises `push` on every branch plus `pull_request`, so
that branches without a pull request, which agents' cloud sessions often push, still get CI.
That runs each pull request's commits twice. It costs about a minute in this skill's own
repository, but it would double a 15-minute suite. The alternative is `push` on the default
branch only, plus `pull_request`, and opening a draft pull request for every branch.

### Pinned builds, timing tests and timeouts

- **Pinned, cached builds.** An unpinned build tests code nobody here reviewed, and rebuilding
  it every run spends most of the job on work that didn't change.
- **Growth, not milliseconds.** Runner noise is larger than many real costs, so a ratio across
  sizes far apart is what shows the shape.
- **Recording every timeout.** One timeout reads as noise. A record of each, with where the
  time went, shows a pattern, and raising the limit erases the evidence.

## Facts

Versions, dates and practices, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `strict-checks` | Required checks are strict by default: a branch must be up to date with its base before it merges | [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | "The branch must be up to date with the base branch before merging. This is the default behavior for required status checks." | 2026-09-30 | 2027-03-31 |
| `loose-checks` | Without that setting, two pull requests can each pass and fail together once merged | [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | "Status checks may fail after you merge your branch if there are incompatible changes with the base branch." | 2026-09-30 | 2027-03-31 |
| `cache-scope` | A run restores caches from its own branch or the default branch | [Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) | "Workflow runs can restore caches created in either the current branch or the default branch" | 2026-09-30 | 2027-03-31 |
| `concurrent-jobs` | On standard runners a Free account runs 20 jobs at once | [Actions limits](https://docs.github.com/en/actions/reference/limits) | "Standard GitHub-hosted runner Free 20" | 2026-09-30 | 2027-03-31 |
| `google-presubmit` | Google runs only fast, reliable tests before submit, accepts rollbacks, and classifies flaky tests company-wide | [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html) | "only fast, reliable ones." and "accept some number of rollbacks" and "a system for flake classification" | 2026-09-30 | 2027-09-30 |
| `chromium-cq` | Chromium's commit queue runs chosen suites before a change lands; experimental jobs don't block | [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | "It runs a curated set of test suites across a curated set of platforms for a given CL" and "the outcome of the build doesn't affect if the CL can land or not" | 2026-09-30 | 2027-03-31 |
| `prow-jobs` | Kubernetes' Prow runs presubmit, postsubmit and periodic jobs | [Prow jobs](https://docs.prow.k8s.io/docs/jobs/) | "The hook component schedules presubmit and postsubmit jobs" and "The horologium component schedules periodic jobs." | 2026-09-30 | 2027-03-31 |
| `fowler-build` | Fowler: a ten-minute build before merge is reasonable, with slower tests later | [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | "the XP guideline of a ten minute build is perfectly within reason" and "The commit build is the one that has to be done quickly" | 2026-09-30 | 2027-09-30 |
| `llvm-policy` | LLVM tags a subject's area in brackets for post-commit review, and reverts first when a commit breaks something | [Developer policy](https://llvm.org/docs/DeveloperPolicy.html) | "This helps email filters and searches for post-commit reviews." and "please revert and investigate offline" | 2026-09-30 | 2027-03-31 |
| `rust-queue` | Rust's bors runs the full suite on each approved pull request's merge commit before pushing it, and batches trivial ones into rollups | [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | "bors will create a merge commit and run the full test suite on it" and "to reduce CI costs and merge delays" | 2026-09-30 | 2027-03-31 |
| `rust-pr-builds` | Rust's build on each push to a pull request is a short subset of the full suite | [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | "relatively short (~40 minutes) and lightweight test suite" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (protected branches, caching, limits) | What GitHub tests, and its limits | CC BY 4.0: facts in our own words, with short quotes |
| [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html) | Presubmit and post-submit tests, flake classification | CC BY-NC-ND 4.0: quoted, never adapted |
| [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | What runs before a change lands | Not stated on the page: short quotes only |
| [Prow jobs](https://docs.prow.k8s.io/docs/jobs/) | Kubernetes' presubmit, postsubmit and periodic jobs | Apache-2.0: a fact with a short quote |
| [Martin Fowler, Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | The ten-minute build, and staged builds | © Martin Fowler: quoted, never adapted |
| [LLVM Developer Policy](https://llvm.org/docs/DeveloperPolicy.html) | Area tags, and reverting first | Not stated on the page: short quotes only |
| [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | The merge queue, rollups and pull request builds | MIT or Apache-2.0: facts with short quotes |
| Two live repositories of this skill's owner, unnamed here | A source build that took most of a job, a test near its timeout | Observed practice, in our own words |
