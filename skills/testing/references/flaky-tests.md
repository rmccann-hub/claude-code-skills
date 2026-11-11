# Flaky tests

Read this for a test that passes and fails on the same code: whether to re-run it, how to find
which tests flake and why, when and how to quarantine one, and how to keep a fixed flake fixed.

Proving that a check can fail, a fix's test among them, is `test-gates`; what a result is
checked against is `test-oracles`. A slow test, a timing test, or a timeout that comes and goes
is `ci-speed` in `git-workflows`: read it where a timeout is the symptom. Test strategy and each
framework's retry and ordering options are the planned `testing-patterns` module.

## Rules

1. **A flaky failure is a defect to root-cause,** in the test or in the program. A test is
   flaky when it passes and fails on the same code. Until the cause is found, treat the failure
   as real, and check the program before changing the test.
2. **Re-run only to confirm, once, and keep the failure on record.** A pass on the re-run shows
   the test flakes; it clears nothing. Record the failure before the re-run. A second failure on
   the same commit is real.
3. **Find flakes two ways:** re-run the failing test on the same commit under changed
   conditions, and mine the history for a test that both passed and failed on one commit.
4. **Quarantine only as a tracked, time-limited step with an owner,** never a silent skip. A
   quarantined test still runs and reports, and stops blocking. It has an issue, an owner and
   an end date, and goes back to blocking when it's fixed or the date passes. No pull request
   quarantines a test to get its own checks green.
5. **Fix the flake where it is, then add a ratchet that refuses its class back.** Fix the race
   or shared state at its source, fix every instance of the same shape, and add a check that
   fails on the next one.

### Recording a flaky failure

Before any re-run, write down the test's name, the commit, the run's link, the host, the
failure message, and the seed or order if the runner shuffles tests. Keep one issue per flaky
test and add each new occurrence to it: the count is how much the flake costs, and the record
is what a fix is later checked against.

### Reproducing it

Change one condition at a time, on the same commit. GitHub's three retries name the usual
causes (fact `ft-github-retries`):

- **The same process, again:** run the test alone, many times. A failure points at chance or a
  race.
- **Later in time:** shift or freeze the clock. A failure points at an assumption about dates,
  month lengths or time zones.
- **Another host or order:** run it inside the full suite, in shuffled order, with CI's number
  of parallel workers, or on another machine. A failure only there points at shared state:
  a directory, a port, a global, or a test that depends on another's leftovers.

Then mine the history. `gh run list --commit <sha>` lists a commit's runs; a test with both a
pass and a fail on one commit is flaky. Keep each run's test report as an artifact, so a test's
record can be read across runs. Where a timeout is the symptom, measure
the test as `ci-speed` says before calling it a flake.

### Where the cause lives

- **In the program:** a signal, callback, thread or process that arrives at a moment the code
  doesn't expect. Users can meet the same race, so fix it in the program and keep the test
  that caught it unchanged.
- **In the test:** a shared directory or port, global state, order dependence, a `sleep` in
  place of waiting on a condition, or a hard-coded date.

A fix is shown by the reproduction that failed before: run it the same number of times again,
and record both counts in the issue.

### The ratchet

A ratchet is a check, a test or a lint rule, that scans the code for the flake's shape, such as
a directory walk over a path a parallel worker cleans up. It:

- **fails closed:** code it can't parse or place is a failure, not a pass;
- **keeps an allowlist that may only shrink:** the known instances it tolerates, with a test
  that fails when the list grows;
- **names the fix** in its message, so whoever writes the next instance learns the pattern.

## Mistakes

- **A retry setting for the whole suite,** in the runner or the CI configuration. It turns
  every flake green and records none. Remove it; re-run by hand, once, after recording.
- **Re-running until green and calling it an infrastructure flake.** A second failure on one
  commit is real. Look for the cause; the runner is a cause only when the log shows it, such as
  a job that died before any test ran.
- **Changing the test when the program races.** A `sleep` or a looser assertion hides a defect
  users can hit. Find which side is wrong first.
- **A skip marker with "flaky" as its reason,** and no issue, owner or date. Nobody returns to
  it. Quarantine with all three, or fix it now.
- **Fixing the one test and stopping.** Look for every test with the same shape, and add the
  ratchet. A third flake of one class had been written before its ratchet existed.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Automatic retries hide failures | `grep -rni -e rerun -e retry -e flaky` over the runner's configuration and CI workflows | `GAP` | Remove them, or record every retry that passed as an issue with an owner |
| A pull request skips or quarantines a test to get green | Skip markers, deleted tests or quarantine entries in the pull request's diff | `BLOCKER` | Revert that part and fix the cause |
| A skip or quarantine with no issue, owner or end date, or a quarantined test that no longer runs | Each skip marker's reason, each quarantine entry, and CI's logs for its name | `GAP` | Add all three and run it outside the blocking path, or fix the test |
| A quarantine past its end date | The entries' dates against today | `GAP` | Fix it, or the owner decides to delete the test; either way it leaves the list |
| Flaky failures go unrecorded | A commit with a pass and a fail of one test, against the issues | `GAP` | One issue per test, each occurrence added with its run's link |
| A fixed class of flake has no ratchet | Tests with the fixed one's shape | `GAP` | A ratchet that fails closed, with an allowlist that may only shrink |
| A ratchet's allowlist grew | The allowlist's history | `GAP` | Fix the new instance and take it off |
| Every flake has an issue and an owner; no quarantine is overdue | The checks above | `OK` | None |

## Why

### A flake is a defect

- **The advice:** root-cause each flaky failure, in the program as well as the test.
- **The reason:** a test that fails without a change to the code may have found a race the
  program has. In one audited repository, an intermittent failure was a signal arriving after
  the loop, and was fixed in the program, not the test (L13).
- **What others do, and why:** flakes are common at scale: Google saw about 1.5% of test runs
  flaky and almost 16% of its tests with some flakiness, and most of its pass-to-fail
  transitions involved a flaky test (fact `ft-google-rate`). It warns that quarantining one
  "could easily mask a real race condition" (fact `ft-google-quarantine`).
- **What it costs:** investigation time on failures that turn out to be in the test.
- **When to choose differently:** a test nobody needs any more can be deleted instead, by its
  owner, on the record.

### One re-run, recorded

- **The advice:** re-run once to confirm, after the failure is written down.
- **The reason:** a re-run that turns green erases the only evidence, and a suite that re-runs
  itself teaches people to stop reading failures. Google found its fail-three-times marker
  "encourages developers to ignore flakiness" (fact `ft-google-three-in-a-row`). This skill's
  own repository holds its sessions to one re-run: "A second failure on the same head is real."
- **What others do, and why:** Microsoft's CloudBuild retries a failed test once and lets the
  build continue when it passes, and its Flakes system files a bug for each flake (fact
  `ft-flakes-retry`). GitHub's CI re-runs automatically and opens an issue for whoever last
  changed the test or its code (fact `ft-github-issue`). Automation does the recording there.
- **What it costs:** a real flake blocks a merge until someone looks.
- **When to choose differently:** an automatic retry is sound where, as at Microsoft and
  GitHub, every retry that passes files or updates an issue with an owner, with no exceptions.

### Detection on the same commit and in history

- **The advice:** re-run under changed conditions, and read the record across runs.
- **The reason:** a test re-run under the same conditions misses flakes that depend on time,
  order or host. History shows flakes that nobody re-ran.
- **What others do, and why:** GitHub retries in the same process, shifted in time and on
  another host, and finds most flaky failures that way (fact `ft-github-retries`). Its flaky
  builds fell from about 9 percent of commits to less than half a percent (fact
  `ft-github-rate`).
- **What it costs:** keeping test reports, and runs spent on reproduction.
- **When to choose differently:** a suite that runs rarely has little history; rely on
  reproduction there.

### Quarantine with an owner and an end date

- **The advice:** take a flaky test out of the blocking path only with an issue, an owner and
  an end date, still running.
- **The reason:** a test skipped without those is forgotten, and the defect it found ships.
  This skill's own repository never lets a session "skip, disable or quarantine a test, or
  loosen a check, to get green."
- **What others do, and why:** Google's tool quarantines a test and files a bug (fact
  `ft-google-quarantine`). Microsoft's Flakes suppresses a failure for 30 days "to discourage
  developers from fully relying on suppressions", and lifts it when the bug closes (fact
  `ft-flakes-suppress`).
- **What it costs:** the test's failures don't block while it's out, and someone must own it.
- **When to choose differently:** with no one to own it, fix the test now or delete it on the
  record; an unowned quarantine is a skip.

### Fix where it is, then a ratchet

- **The advice:** fix at the source, fix the siblings, and add a check against the class.
- **The reason:** flakes come in classes. In one audited repository, two flakes from one
  directory walk racing a parallel worker's cleanup had the same shape, and a third had been
  written before the ratchet (L32). A ratchet that passes code it can't place lets the next one
  through, and an allowlist that can grow becomes the new way to skip.
- **What others do, and why:** the three practices above detect, quarantine and file flakes as
  they come. The ratchet comes from this repository's audits, for a class already seen twice.
- **What it costs:** writing the check, and its false alarms.
- **When to choose differently:** a one-off with no plausible sibling needs the fix alone.

## Facts

Practices and figures, each named elsewhere by its ID. Checked 2026-11-10.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `ft-google-rate` | Google saw about 1.5% of test runs flaky, almost 16% of its tests with some flakiness, and a flaky test in about 84% of pass-to-fail transitions (2016-05-27) | [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) | "a continual rate of about 1.5% of all test runs" and "Almost 16% of our tests have some level of flakiness associated with them!" and "about 84% of the transitions we observe from pass to fail involve a flaky test!" | 2026-11-10 | 2027-05-10 |
| `ft-google-quarantine` | Google's tool quarantines a test that flakes too often and files a bug, which can mask a real race | [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) | "it automatically quarantines the test" and "files a bug for developers to reduce the flakiness" and "could easily mask a real race condition" | 2026-11-10 | 2027-05-10 |
| `ft-google-three-in-a-row` | A test marked flaky at Google fails only after three failures in a row, which encourages ignoring it | [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) | "report a failure only if it fails 3 times in a row" and "encourages developers to ignore flakiness in their own tests" | 2026-11-10 | 2027-05-10 |
| `ft-flakes-retry` | Microsoft's CloudBuild retries a failed test once and continues the build if it passes; Flakes filed over 4,000 bug reports | [Lam et al., ICSE 2020](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/07/LamETAL20FaTB.pdf) | "CloudBuild automatically retries the test once" and "Flakes has created over 4,000 bug reports" | 2026-11-10 | 2027-05-10 |
| `ft-flakes-suppress` | Flakes suppresses a flaky failure for 30 days, and removes it when its bug closes | [Lam et al., ICSE 2020](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/07/LamETAL20FaTB.pdf) | "to discourage developers from fully relying on suppressions" and "Flakes automatically removes the test from the suppression file" | 2026-11-10 | 2027-05-10 |
| `ft-github-rate` | GitHub's flaky builds fell from about 9 percent of commits to under half a percent (2020-12-16) | [Reducing flaky builds by 18x](https://github.blog/engineering/engineering-principles/reducing-flaky-builds-by-18x/) | "about 9 percent of commits" and "less than half a percent, or 1 in 200 commits" | 2026-11-10 | 2027-05-10 |
| `ft-github-retries` | GitHub retries in the same process, shifted in time and on another host, finding 90 percent of flaky failures | [Reducing flaky builds by 18x](https://github.blog/engineering/engineering-principles/reducing-flaky-builds-by-18x/) | "Retry in the same process, shifted into the future." and "Retry on a different host." and "identify 90 percent of flaky failures" | 2026-11-10 | 2027-05-10 |
| `ft-github-issue` | Past an impact threshold, GitHub opens an issue for whoever last changed the test or its code | [Reducing flaky builds by 18x](https://github.blog/engineering/engineering-principles/reducing-flaky-builds-by-18x/) | "an issue is automatically opened and assigned to the people who most recently modified either the test files or associated code" | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) (Micco, 2016-05-27) | Flake rates, re-run markers, quarantine | Not stated on the page: short quotes only |
| [Lam et al., ICSE 2020](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/07/LamETAL20FaTB.pdf) | Microsoft's retry, bugs and suppression | © the authors: short quotes only |
| [Reducing flaky builds by 18x](https://github.blog/engineering/engineering-principles/reducing-flaky-builds-by-18x/) (2020-12-16) | GitHub's retries, rate and issues | © GitHub: short quotes only |
| This skill's repository: its rules for sessions driving a pull request | One re-run, and no skip or quarantine to get green | Our own: quoted |
| Audits of live repositories, unnamed here (L13, L32) | A race in the program, and a class of flake held off by a ratchet | Observed practice, in our own words |
