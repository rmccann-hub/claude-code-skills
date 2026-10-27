# Git hooks

Read this for writing, installing or testing a `commit-msg`, `pre-commit` or `pre-push` hook,
moving hooks out of `.git/hooks`, or finding out why a hook didn't run.

It covers checks that run in a clone before anything reaches the server. The same checks in CI
are `ci-workflows`, which is the gate wherever no persistent clone installs the hook.

## Rules

1. **Hooks don't travel with a clone,** because `.git/hooks` isn't tracked. Commit a hooks
   directory and point Git at it, or use pre-commit or prek.
2. **A hook runs only where someone installed it.** Propose a client-side hook only where a
   persistent local clone exists. Otherwise CI is the gate.
3. **Nobody passes `--no-verify` to get past a hook.** Fix what it caught, or fix the hook.
4. **Hooks are for fast, local checks,** such as formatting, whitespace and secrets.

### Installing hooks

- **Commit a hooks directory and point Git at it** with `git config core.hooksPath .githooks`
  (fact `hooks-path`), or use pre-commit or prek with a committed `.pre-commit-config.yaml`
  (facts `pre-commit`, `prek`).
- **An agent's cloud session starts from a fresh clone** and runs nothing a README asks a person
  to run. So install the hook from a committed `SessionStart` hook in `.claude/settings.json`
  that runs `git config core.hooksPath .githooks`, or count on CI alone.
- **Where the only clones are cloud sessions',** a hook gates only the sessions that happen to
  install it, and CI is the gate. project-bootstrap-and-audit's dimension 6 sets this rule.
- **CI re-runs what a commit hook checks, and branch protection does on the server what a
  pre-push hook does.**

### Writing hooks

- **A `pre-push` hook reads the refs being pushed from its standard input.** Check those,
  because the checked-out branch may not be the one being pushed.
- **A `commit-msg` hook reads the message through `git stripspace --strip-comments`.** Git hands
  the hook the message before it strips comments, so a commit template's comment would
  otherwise become "the subject".

Examples, both tested:

- [assets/githooks/commit-msg](../assets/githooks/commit-msg) refuses a subject outside the
  grammar its `grammar=` line names, `area` or `conventional`, as the commit-subjects workflow
  does, and notes one longer than 50 characters.
- [assets/githooks/pre-push](../assets/githooks/pre-push) refuses a push that updates `main`
  directly, from whichever branch.

Copy them into `.githooks/`, then commit them as executable:
`git add --chmod=+x .githooks/*`. Check with `git ls-files -s .githooks`, which shows `100755`
for each. `chmod +x` isn't enough on Windows, where Git for Windows ignores file modes by
default, so the change never reaches the commit and every clone gets a hook Git won't run. Add
`.githooks/* text eol=lf` to `.gitattributes`, so a Windows checkout doesn't give the scripts
CRLF line endings.

### Testing a hook in a throwaway repository

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

### Moving hooks out of `.git/hooks`

1. Move the scripts into a tracked directory, such as `.githooks/`.
2. Point Git at it: `git config core.hooksPath .githooks` (fact `hooks-path`).
3. For agents' cloud sessions, set it from a committed `SessionStart` hook.
4. Or use pre-commit, or prek, which runs the same `.pre-commit-config.yaml` faster (facts
   `pre-commit`, `prek`).

## Mistakes

- **`git commit --no-verify` or `git push --no-verify` to get past a hook.** Fix what it caught,
  or fix the hook. CI will run the check anyway.
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
- **A slow hook,** such as the whole test suite on every commit. People learn to skip it. Keep
  the slow checks in CI.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Hooks are documented, but nothing installs them | `core.hooksPath`, a SessionStart hook, pre-commit config | `GAP` where the repository counts on them | Where a persistent local clone exists, commit the hooks as executable and set `core.hooksPath`; otherwise count on CI |
| Committed hooks aren't executable | `git ls-files -s .githooks` shows `100644` rather than `100755` | `DRIFT`: Git skips the hook | `git add --chmod=+x .githooks/*`, and commit |

## Why

### Hooks as a convenience, not the gate

**The advice.** Use hooks for fast, local checks where a persistent clone installs them, and
make CI the gate.

**Why.** A hook lives in one clone's configuration. Nothing makes a new clone install it, and
`--no-verify` skips it. A check that must hold for every change has to run where every change
goes: CI, and branch protection on the server.

**What others do.** pre-commit and prek install hooks from a committed configuration file, and
pin each hook's version there (facts `pre-commit`, `prek`). Projects that use them still run the
same configuration in CI, because a contributor may never have installed it.

**What each choice costs.** A hook catches a mistake seconds after it's made, before it costs a
CI run. It also slows every commit, and each clone must be set up. CI alone costs a round trip
for every mistake.

**When to choose differently.** Where every clone is a cloud session that starts fresh, skip
hooks unless a committed `SessionStart` hook installs them.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `hooks-path` | Git runs hooks from `core.hooksPath` when it's set, instead of `.git/hooks` | [githooks](https://git-scm.com/docs/githooks) | "$GIT_DIR/hooks/* (or `git config core.hooksPath`/*)" | 2026-09-30 | 2027-09-30 |
| `pre-commit` | pre-commit 4.6.2, released 2026-08-10, MIT | [PyPI](https://pypi.org/project/pre-commit/) | version 4.6.2, uploaded 2026-08-10 | 2026-09-30 | 2026-12-31 |
| `prek` | prek 0.5.4, released 2026-09-28, MIT: a faster runner for the same `.pre-commit-config.yaml` | [PyPI](https://pypi.org/project/prek/) | version 0.5.4, uploaded 2026-09-28 | 2026-09-30 | 2026-12-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (githooks, git-stripspace) | Where hooks run, and what they're handed | GPL-2.0: facts in our own words, with short quotes |
| PyPI pages for [pre-commit](https://pypi.org/project/pre-commit/) and [prek](https://pypi.org/project/prek/) | Tool versions | MIT: versions only |
| Two live repositories of this skill's owner, unnamed here | Hooks that never ran in cloud sessions | Observed practice, in our own words |
