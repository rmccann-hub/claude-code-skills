# CI workflows

Read this for writing or fixing a GitHub Actions workflow's triggers, timeouts, installs, path
filters and required checks, or proving that a gate, a test job or a workflow works.

It covers the jobs that run checks and how to trust them. How long CI should take, where each
suite runs, caching and slow tests are `ci-speed`; a workflow's permissions, pinned actions and
untrusted input are `actions-security`; local hooks are `git-hooks`; the release job is
`releases-and-versions`. How to design the tests themselves belongs to a testing skill.

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
  where it happens, not only after it merges. That runs a pull request's commits twice, as the
  branch and merged with its base (fact `pr-merge-ref`). `ci-speed` weighs that cost.
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

### Lint the workflows

**Lint workflows with actionlint, and scan them with zizmor** (facts `actionlint`, `zizmor`), in
CI, with both tools pinned by version. actionlint checks syntax, expressions and job wiring, and
with ShellCheck on the path it checks every `run:` script. Both run offline. Neither can tell
you the workflow ran, only that it could.

### Test jobs prove the suite ran to the end

A test run that stops early can still exit 0. A test job checks that its report exists, and
that the number of tests it counts meets a recorded baseline. The standard's starter CI file
has only the collection guard, which counts what was collected.
[assets/workflows/tests.yml](../assets/workflows/tests.yml), tested, adds the completion guard:
the test report must exist, and count at least as many tests as `.test-baseline`.

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

## Mistakes

- **Quarantining or skipping a flaky test "so it doesn't block CI".** It hides the failure from
  the only people who can fix it. Re-run it once to confirm it flakes, then instrument it and
  keep the artifacts until the cause is found.
- **Reading an exit status through a pipe:** `pytest | tail` reports `tail`'s status, not
  pytest's.
- **Running the tests and pushing in one command.** One session's single command ran the suite,
  which failed, and pushed the branch anyway. Push as its own step, after reading a green result.
- **Running only the tests you expect to matter before pushing an edit to a checked file.** One
  session edited a status line, ran a subset, and pushed a shape a test it skipped would have
  refused. Run every test that names the file, or the whole suite.
- **A path filter on a required check, or an `if:` that skips one,** or `paths` with
  `paths-ignore` on one event (facts `skipped-pending`, `job-if-success`, `paths-both`).
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

**What others do.** Large projects do take flaky tests out of the blocking path, with machinery
behind it. Google classifies flakes by statistics across the company, so an engineer can tell
whether their change broke a test or the test is unstable (fact `google-presubmit`). Chromium's
commit queue runs some jobs as experiments, which report without blocking (fact `chromium-cq`).
In both, someone owns the test, and its failures stay visible.

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

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `timeout` | A job with no `timeout-minutes` runs up to 360 minutes | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "Default: 360" | 2026-09-30 | 2027-03-31 |
| `paths-both` | One event can't use both `paths` and `paths-ignore` | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "You cannot use both the paths and paths-ignore filters for the same event" | 2026-09-30 | 2027-03-31 |
| `skipped-pending` | A workflow skipped by a path, branch or commit-message filter leaves its checks pending | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "checks associated with that workflow will remain in a \"Pending\" state" | 2026-09-30 | 2027-03-31 |
| `job-if-success` | A job skipped by its `if:` reports success, even as a required check | [Using conditions to control job execution](https://docs.github.com/en/actions/using-jobs/using-conditions-to-control-job-execution) | "It will not prevent a pull request from merging, even if it is a required check." | 2026-09-30 | 2027-03-31 |
| `job-log-redirect` | The REST endpoint for a job's log answers with a redirect whose link expires after a minute | [Workflow jobs REST API](https://docs.github.com/en/rest/actions/workflow-jobs) | "Gets a redirect URL to download a plain text file of logs for a workflow job." and "This link expires after 1 minute." | 2026-10-15 | 2027-04-15 |
| `schedule-60` | In a public repository, scheduled workflows turn off after 60 days with no activity | [Disabling and enabling a workflow](https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow) | "scheduled workflows are automatically disabled when no repository activity has occurred in 60 days" | 2026-09-30 | 2027-03-31 |
| `uv-locked` | `uv sync --locked` fails when the lockfile needs updating; `--frozen` doesn't check it | [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | "If the lockfile is missing or needs to be updated, uv will exit with an error." | 2026-09-30 | 2027-03-31 |
| `pr-merge-ref` | A `pull_request` run tests the merge commit, `refs/pull/<number>/merge`, not the head | [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) | "Last merge commit on the GITHUB_REF branch" | 2026-09-30 | 2027-03-31 |
| `cancel-in-progress` | `concurrency` with `cancel-in-progress: true` cancels the run already going in its group | [Using concurrency](https://docs.github.com/en/actions/using-jobs/using-concurrency) | "specify cancel-in-progress: true" | 2026-09-30 | 2027-03-31 |
| `merge-queue` | Merge queues need an organization-owned repository, public or on Enterprise Cloud, and the `merge_group` trigger | [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) | "available in any public repository owned by an organization" | 2026-09-30 | 2027-03-31 |
| `actionlint` | actionlint's newest tag is v1.7.12 | `git ls-remote --tags https://github.com/rhysd/actionlint` | `refs/tags/v1.7.12` | 2026-09-30 | 2026-12-31 |
| `zizmor` | zizmor 1.30.1, released 2026-09-09, MIT: static security analysis for workflows | [PyPI](https://pypi.org/project/zizmor/) | version 1.30.1, uploaded 2026-09-09 | 2026-09-30 | 2026-12-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (workflow syntax, events, conditions, concurrency, disabling workflows, merge queues, workflow jobs API) | GitHub Actions' behavior | CC BY 4.0: facts in our own words, with short quotes |
| [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | `--locked` against `--frozen` | MIT or Apache-2.0: a fact with a short quote |
| PyPI's page for [zizmor](https://pypi.org/project/zizmor/); tags of [actionlint](https://github.com/rhysd/actionlint) | Tool versions | MIT: versions only |
| [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html); [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | Flaky tests at scale | CC BY-NC-ND 4.0, and not stated: short quotes only |
| Two live repositories of this skill's owner, unnamed here | A push after a failed suite | Observed practice, in our own words |
