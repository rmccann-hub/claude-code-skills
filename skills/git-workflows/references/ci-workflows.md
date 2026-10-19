# CI workflows

Read this for writing or fixing a GitHub Actions workflow's triggers, timeouts, installs, path
filters and required checks; deciding how long CI should take and where each suite runs; or
proving that a gate, a test job or a workflow works.

It covers the jobs that run checks and how to trust them. A workflow's permissions, pinned
actions and untrusted input are `actions-security`; local hooks are `git-hooks`; the release
job is `releases-and-versions`. How to design the tests themselves belongs to a testing skill.

## Rules

1. **Never get to green by going around a check.** No skipping or quarantining a failing test,
   and no `--no-verify`. Fix the cause.
2. **`timeout-minutes` on every job.** Without it, a hung job runs for 360 minutes (fact
   `timeout`).
3. **Install from the lockfile, in a mode that fails on drift:** `npm ci`, or `uv sync --locked`.
   `uv sync --frozen` doesn't check the lockfile at all (fact `uv-locked`).
   project-bootstrap-and-audit has the command for each ecosystem (dimension 2).
4. **Run where work happens,** and make every required check report on every pull request.
5. **A gate you've only watched pass hasn't been tested.** Run it against the state it exists
   to catch.

project-bootstrap-and-audit's *Starter file contents* has the full CI template. These are the
properties that matter, each with its reason.

### Triggers

- **Run on `push` and `pull_request` with no branch filter,** so work gets checked on the branch
  where it happens, not only after it merges. That runs a pull request's commits twice, once as
  the branch and once merged with its base (fact `pr-merge-ref`). Where CI is slow, run `push`
  on the default branch only, with `pull_request`, and open a draft pull request for every
  branch.
- **`concurrency` with `cancel-in-progress` for pull request runs only** (fact
  `cancel-in-progress`). A run on the default branch should finish.
- **A merge queue runs workflows on `merge_group`,** so a required check's workflow lists it
  in `on:`. Merge queues exist only on organization-owned repositories (fact `merge-queue`).
- **A scheduled scan in a public repository stops after 60 days without activity** (fact
  `schedule-60`), with no failure shown. Read its last run date.

### Required checks

- **A required check must report on every pull request.** A workflow skipped by a path filter
  leaves its check pending, and the pull request can't merge (fact `skipped-pending`). So never
  put a path filter on a workflow that provides a required check.
- **A job skipped by its `if:` reports success instead,** even as a required check (fact
  `job-if-success`), so a condition that skips the tests passes the pull request with nothing
  tested. Where tests are skipped by path, require one final job that `needs:` the others and
  fails if any of them failed.
- **Path filters:** use `paths` or `paths-ignore`, never both on one event (fact `paths-both`).

### Builds and installs

- **Pin what a job builds from source, then cache the result.** A job that clones its
  dependencies at their latest commit and builds them every run is slow, and isn't
  reproducible: CI's result and the shipped binary change with commits nobody here made. One
  Windows job spent 19.5 of its 21 minutes building five libraries that way. Pin each one to a
  tag or commit in one place, and cache the built output with `actions/cache`, keyed on the
  pins, the build script's hash and the toolchain version.
- **Lint workflows with actionlint, and scan them with zizmor** (facts `actionlint`, `zizmor`),
  in CI, with both tools pinned by version. actionlint checks syntax, expressions and job
  wiring, and with ShellCheck on the path it checks every `run:` script. Both run offline.
  Neither can tell you the workflow ran, only that it could.

### Test jobs prove the suite ran to the end

A test run that stops early can still exit 0. A test job checks that its report exists, and
that the number of tests it counts meets a recorded baseline. The standard's starter CI file
has only the collection guard, which counts what was collected.
[assets/workflows/tests.yml](../assets/workflows/tests.yml), tested, adds the completion guard:
the test report must exist, and count at least as many tests as `.test-baseline`. Never read a
test command's exit status through a pipe: `pytest | tail` reports `tail`'s status, not
pytest's.

### Prove a gate works

A gate you've only watched pass has only been seen agreeing with a state that was already
right. Run it against the state it exists to catch:

- **The parent commit.** A gate written in the same change as the thing it guards has never
  seen the state before that change. `git worktree add ../before HEAD~1`, then run the gate
  there, and it should fail.
- **A planted failure.** Break the thing three ways: remove it, reorder it so it runs too late,
  and disable it where it stands. The gate should fail each time.
- **The "couldn't check" case.** Make its input unavailable, with an unknown ref, an empty
  range or a missing file. It should fail, not pass having checked nothing.
- **Every value its input states.** Change each value the checked record states, one at a
  time, by one character. A checker that compared a cited file with its manifest row, but never
  read the hash written beside the citation, passed a record with a wrong hash.

project-bootstrap-and-audit's dimension 5 sets these rules for every gate. Restore what you
broke from a copy you made first, checked by its hash, not with `git checkout --`, which throws
away uncommitted work.

### Check that it ran

- **Read the `on:` block first.** `on: push: branches: [main]` produces no run at all for a push
  to another branch: not a pending run, none.
- **Read the run at job and log level, not the rollup.** A skipped job or step reads as green in
  the summary. Name the step that proves the gate fired, such as a count it printed, and look
  for that line in the log.
- **Check that a required check reports on every pull request.** Open a pull request that
  touches only a path the workflow filters out. If the check sits pending, the filter has to go
  (fact `skipped-pending`).
- **Fetch a job's log with a client that follows redirects.** The REST endpoint answers with a
  short-lived redirect, not the log (fact `job-log-redirect`).

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
  took 28, 93 and over 120 seconds within an hour; the next timeout then named its slow step.
  Raising the limit hides the cause.

## Mistakes

- **Diagnostics that print only when a test fails.** A test runner that shows output only for
  failures says nothing about a pass near its limit. One suite's new per-step timing reached
  nobody until a step read the runner's own results file after every run.
- **A build chain that goes on after a step fails.** Every earlier log of one Windows build
  carried a failed install, unseen, because the script ran each library's build whatever the
  last one returned. Stop at the first failure, and expect the first strict run to turn up old
  ones.
- **Quarantining or skipping a flaky test "so it doesn't block CI".** It hides the failure from
  the only people who can fix it. Re-run it once to confirm it flakes, then instrument it and
  keep the artifacts until the cause is found.
- **Reading an exit status through a pipe:** `pytest | tail` reports `tail`'s status.
- **Running the tests and pushing in one command.** One session's single command ran the suite,
  which failed, and pushed the branch anyway. Push as its own step, after reading a green result.
- **Running only the tests you expect to matter before pushing an edit to a checked file.** One
  session edited a status line, ran a subset, and pushed a shape a test it skipped would have
  refused. Run every test that names the file, or the whole suite.
- **`paths` and `paths-ignore` on the same event** (fact `paths-both`), or a path filter on a
  required check (fact `skipped-pending`).
- **An `if:` that skips a required job.** A skipped job reports success, so the pull request
  merges with nothing tested (fact `job-if-success`).
- **`pip install -r requirements.txt` in CI with no lockfile, or `uv sync --frozen` believed to
  check the lockfile** (fact `uv-locked`).
- **A step name containing `: ` without quotes.** The file is no longer valid YAML, and the
  workflow never runs. actionlint catches it.
- **Planning a merge queue on a personal account's repository.** It isn't offered there (fact
  `merge-queue`).
- **Fetching a job's log from the REST API with a client that doesn't follow redirects.** The
  endpoint answers with a short-lived redirect, not the log (fact `job-log-redirect`), so the
  client reports an error or an empty file. Follow the redirect at once, or use a tool that
  does.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Every job sets `timeout-minutes` | Read each job | `GAP` | Set it from the job's usual time, with room (fact `timeout`) |
| The install doesn't fail on lockfile drift | Look for `pip install -r`, `npm install` or `uv sync --frozen` | `GAP`; `BLOCKER` where the docs call it a lockfile gate | `npm ci`, `uv sync --locked` (fact `uv-locked`) |
| CI doesn't run where work lands | The `on:` blocks, against the branches people push | `BLOCKER` where anything counts on it | `push` and `pull_request` with no branch filter |
| A required check comes from a path-filtered workflow | The ruleset's required checks, against each workflow's `on:` | `GAP`: pull requests that skip it can't merge | Remove the filter, or stop requiring the check (fact `skipped-pending`) |
| A required check comes from a job with an `if:` | The required checks, against each job's `if:` | `BLOCKER` where the condition can skip it on a pull request that changes code: it reports success having run nothing (fact `job-if-success`) | Remove the condition, or require a final job that `needs:` the others and fails if any failed |
| `paths` and `paths-ignore` on one event | Read the `on:` blocks | `DRIFT`: the workflow is invalid | Keep one (fact `paths-both`) |
| Instructions say `--no-verify`, or to skip or quarantine a failing test | `grep -rn -e '--no-verify' -e quarantin .` | `DRIFT` | Remove them; fix the cause |
| A scheduled scan in a public repository last ran over 60 days ago | Its run history | `GAP`: it has stopped (fact `schedule-60`) | Re-enable it; watch the date |

## Why

### Going around a check

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

### Timeouts, lockfiles and path filters

- **Timeouts.** A hung job otherwise runs for six hours (fact `timeout`), and holds a runner
  that other jobs wait for.
- **Lockfile drift.** An install that quietly resolves new versions tests code nobody reviewed
  (fact `uv-locked`).
- **Path filters.** A required check that a filter skips stays pending, so the pull request
  can't merge (fact `skipped-pending`). The opposite trap: a job skipped by its own `if:`
  reports success, even when it is required (fact `job-if-success`).

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

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `timeout` | A job with no `timeout-minutes` runs up to 360 minutes | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "Default: 360" | 2026-09-30 | 2027-03-31 |
| `paths-both` | One event can't use both `paths` and `paths-ignore` | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "You cannot use both the paths and paths-ignore filters for the same event in a workflow." | 2026-09-30 | 2027-03-31 |
| `skipped-pending` | A workflow skipped by a path, branch or commit-message filter leaves its checks pending, and a pull request that requires them can't merge | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "checks associated with that workflow will remain in a \"Pending\" state" | 2026-09-30 | 2027-03-31 |
| `job-if-success` | A job skipped by its `if:` reports success, and counts as passing even where it is a required check | [Using conditions to control job execution](https://docs.github.com/en/actions/using-jobs/using-conditions-to-control-job-execution) | "A job that is skipped will report its status as \"Success\". It will not prevent a pull request from merging, even if it is a required check." | 2026-09-30 | 2027-03-31 |
| `job-log-redirect` | The REST endpoint for a job's log answers with a redirect, not the log, and the link it gives expires after a minute | [Workflow jobs REST API](https://docs.github.com/en/rest/actions/workflow-jobs) | "Gets a redirect URL to download a plain text file of logs for a workflow job." and "This link expires after 1 minute." | 2026-10-15 | 2027-04-15 |
| `schedule-60` | In a public repository, scheduled workflows turn off after 60 days with no repository activity | [Disabling and enabling a workflow](https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow) | "scheduled workflows are automatically disabled when no repository activity has occurred in 60 days" | 2026-09-30 | 2027-03-31 |
| `uv-locked` | `uv sync --locked` fails when the lockfile needs updating. `--frozen` installs from the lockfile without checking it, so drift passes | [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | "If the lockfile is missing or needs to be updated, uv will exit with an error." | 2026-09-30 | 2027-03-31 |
| `pr-merge-ref` | A `pull_request` run tests the pull request's merge commit, `refs/pull/<number>/merge`, not its head | [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) | "Last merge commit on the GITHUB_REF branch" | 2026-09-30 | 2027-03-31 |
| `strict-checks` | Required checks are strict by default: a branch must be up to date with its base before it merges, so the tree that lands is a tree that was tested | [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | "The branch must be up to date with the base branch before merging. This is the default behavior for required status checks." | 2026-09-30 | 2027-03-31 |
| `loose-checks` | Without that setting, two pull requests can each pass and still fail together once merged | [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | "Status checks may fail after you merge your branch if there are incompatible changes with the base branch." | 2026-09-30 | 2027-03-31 |
| `cache-scope` | A run restores caches made on its own branch or on the default branch, so main's runs are what fill the cache pull requests read | [Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) | "Workflow runs can restore caches created in either the current branch or the default branch (usually main)." | 2026-09-30 | 2027-03-31 |
| `concurrent-jobs` | On standard runners a Free account runs 20 jobs at once, Pro 40 and Team 60 | [Actions limits](https://docs.github.com/en/actions/reference/limits) | "Standard GitHub-hosted runner Free 20" | 2026-09-30 | 2027-03-31 |
| `cancel-in-progress` | `concurrency` with `cancel-in-progress: true` cancels the run already going in the same group | [Using concurrency](https://docs.github.com/en/actions/using-jobs/using-concurrency) | "specify cancel-in-progress: true" | 2026-09-30 | 2027-03-31 |
| `merge-queue` | Merge queues exist only on organization-owned public repositories, or organization-owned private ones on Enterprise Cloud, and need the `merge_group` trigger | [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) | "available in any public repository owned by an organization" | 2026-09-30 | 2027-03-31 |
| `actionlint` | actionlint's newest tag is v1.7.12 | `git ls-remote --tags https://github.com/rhysd/actionlint` | `refs/tags/v1.7.12` | 2026-09-30 | 2026-12-31 |
| `zizmor` | zizmor 1.30.1, released 2026-09-09, MIT: static security analysis for workflows | [PyPI](https://pypi.org/project/zizmor/) | version 1.30.1, uploaded 2026-09-09 | 2026-09-30 | 2026-12-31 |
| `google-presubmit` | Google runs only fast, reliable tests before submit, catches the rest after, accepting rollbacks, and classifies flaky tests company-wide | [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html) | "Our general rule of thumb is: only fast, reliable ones." and "accept some number of rollbacks" and "a system for flake classification" | 2026-09-30 | 2027-09-30 |
| `chromium-cq` | Chromium's commit queue runs the suites a change might affect, on a chosen set of platforms, before it lands; experimental jobs report without blocking | [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | "It runs a curated set of test suites across a curated set of platforms for a given CL" and "the outcome of the build doesn't affect if the CL can land or not" | 2026-09-30 | 2027-03-31 |
| `prow-jobs` | Kubernetes' Prow runs presubmit, postsubmit and periodic jobs | [Prow jobs](https://docs.prow.k8s.io/docs/jobs/) | "The hook component schedules presubmit and postsubmit jobs" and "The horologium component schedules periodic jobs." | 2026-09-30 | 2027-03-31 |
| `fowler-build` | Fowler: a ten-minute build before merge is reasonable, with slower tests in later stages | [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | "the XP guideline of a ten minute build is perfectly within reason" and "The commit build is the one that has to be done quickly" | 2026-09-30 | 2027-09-30 |
| `llvm-policy` | LLVM tags a subject with its area in brackets for post-commit review, and reverts first when a commit breaks something | [Developer policy](https://llvm.org/docs/DeveloperPolicy.html) | "This helps email filters and searches for post-commit reviews." and "please revert and investigate offline" | 2026-09-30 | 2027-03-31 |
| `rust-queue` | Rust's bors tests each approved pull request's merge commit with the full suite before it pushes that commit to the main branch, and batches trivial ones into rollups | [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | "bors will create a merge commit and run the full test suite on it" and "to reduce CI costs and merge delays" | 2026-09-30 | 2027-03-31 |
| `rust-pr-builds` | Rust's build on each push to a pull request is a short subset of the full suite | [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | "relatively short (~40 minutes) and lightweight test suite" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (workflow syntax, events, conditions, concurrency, caching, limits, disabling workflows, protected branches, merge queues, workflow jobs API) | GitHub Actions' behavior | CC BY 4.0: facts in our own words, with short quotes |
| [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | `--locked` against `--frozen` | MIT or Apache-2.0: a fact with a short quote |
| PyPI's page for [zizmor](https://pypi.org/project/zizmor/); tags of [actionlint](https://github.com/rhysd/actionlint) | Tool versions | MIT: versions only |
| [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html) | Presubmit and post-submit tests, flake classification | CC BY-NC-ND 4.0: quoted, never adapted |
| [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | What runs before a change lands | Not stated on the page: short quotes only |
| [Prow jobs](https://docs.prow.k8s.io/docs/jobs/) | Kubernetes' presubmit, postsubmit and periodic jobs | Apache-2.0: a fact with a short quote |
| [Martin Fowler, Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | The ten-minute build, and staged builds | © Martin Fowler: quoted, never adapted |
| [LLVM Developer Policy](https://llvm.org/docs/DeveloperPolicy.html) | Area tags, and reverting first | Not stated on the page: short quotes only |
| [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | The merge queue, rollups and pull request builds | MIT or Apache-2.0: facts with short quotes |
| Two live repositories of this skill's owner, unnamed here | A source build that took most of a job, a test near its timeout, a push after a failed suite | Observed practice, in our own words |
