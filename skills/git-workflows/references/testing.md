# Testing: proving a workflow, hook or gate works

Read this when you add or change a CI workflow, a hook or any check that's meant to stop
something, and need to show it works. Facts are named by ID from `facts.md`.

## A gate you've only watched pass hasn't been tested

It has only been seen agreeing with a state that was already right. Run it against the state it
exists to catch:

- **The parent commit.** A gate written in the same change as the thing it guards has never
  seen the state before that change. `git worktree add ../before HEAD~1`, then run the gate
  there, and it should fail.
- **A planted failure.** Break the thing three ways: remove it, reorder it so it runs too late,
  and disable it where it stands. The gate should fail each time.
- **The "couldn't check" case.** Make its input unavailable, with an unknown ref, an empty
  range or a missing file. It should fail, not pass having checked nothing.

project-bootstrap-and-audit's dimension 5 sets these rules for every gate. Restore what you
broke from a copy you made first, checked by its hash, not with `git checkout --`, which throws
away uncommitted work.

## Lint the workflow before it runs

- **actionlint** checks syntax, expressions and job wiring, and with ShellCheck on the path it
  checks every `run:` script (fact `actionlint`).
- **zizmor** checks for dangerous triggers, injection and over-broad permissions (fact
  `zizmor`).

Both run offline. Neither can tell you the workflow ran, only that it could.

## Check that it ran

- **Read the `on:` block first.** `on: push: branches: [main]` produces no run at all for a push
  to another branch: not a pending run, none.
- **Read the run at job and log level, not the rollup.** A skipped job or step reads as green in
  the summary. Name the step that proves the gate fired, such as a count it printed, and look
  for that line in the log.
- **Check that a required check reports on every pull request.** Open a pull request that
  touches only a path the workflow filters out. If the check sits pending, the filter has to go
  (fact `skipped-pending`).
- **Read a scheduled job's last run date,** because a public repository's schedule stops quietly
  (fact `schedule-60`).

## Test a hook in a throwaway repository

```sh
(
  set -eu
  work=$(mktemp -d)
  git init -q -b main "$work/repo"
  cp -r .githooks "$work/repo/"
  cd "$work/repo"
  git config core.hooksPath .githooks
  git config user.name test
  git config user.email test@example.com
  echo a > a
  git add a
  if git commit -q -m "fixed stuff"; then echo "hook let a bad subject through" >&2; exit 1; fi
  git commit -q -m "docs: add a"
  echo "commit-msg hook: refuses the bad subject, accepts the good one"
)
```

Run it from the repository root. The parentheses keep `set -eu`, `cd` and `exit` inside a
subshell, so pasting it into your own shell doesn't close that shell. Commit through Git, as
here, rather than calling the hook directly: Git hands the hook the message before it strips
comments, which is where a hook reading the first line goes wrong. The hooks in
`assets/githooks/` are tested both ways, by `tests/test_git_workflows_assets.py` in this skill's
repository, on every change.

## Test a release job without spending a tag

With immutable releases, a published tag name can never be used again (fact `immutable`). So
try a release job in a fork, or in a test repository, or with a pre-release version such as
`1.4.0-rc.1`, before you trust it with a real version.

## Test jobs prove the suite ran to the end

A test run that stops early can still exit 0. A test job checks that its report exists, and that
the number of tests it counts meets a recorded baseline. The standard's starter CI file
(*Starter File Contents*) has only the collection guard, which counts what was collected.
[assets/workflows/tests.yml](../assets/workflows/tests.yml) adds the completion guard. Never
read a test command's exit status through a pipe: `pytest | tail` reports `tail`'s status, not
pytest's.
