# Audit: checking a repository's Git and CI setup

Read this when you review how a repository branches, merges, runs CI and releases, without a
full audit. For a full audit, with tiers and a report, use project-bootstrap-and-audit: it rates
most of these checks by tier (dimensions 6, 8 and 10, and its release gate), and its rating wins
where the two differ. The status words are the standard's:

- **`BLOCKER`:** a live exposure, or a check reporting success while measuring nothing.
- **`DRIFT`:** configured, but no longer doing what it says.
- **`GAP`:** missing something the project needs.
- **`OVER`:** heavier than the project needs.
- **`OK`**, and **`N/A`**.

Facts are named by ID from `facts.md`.

| # | Check | How to look | Usual status | Fix |
|---|---|---|---|---|
| 1 | The merge strategy is recorded, with its reason | The context file (`AGENTS.md` or `CLAUDE.md`) and the decision record | `GAP` if missing | Record it (`setup.md`) |
| 2 | The platform allows only the recorded strategy | Settings, General, Pull Requests, or `gh api repos/OWNER/REPO --jq '.allow_merge_commit, .allow_squash_merge, .allow_rebase_merge'` | `DRIFT` if more are on | Turn the others off |
| 3 | Squash or rebase-merge where commits are cited from outside | Search pull request bodies, the decision record and sibling repositories for commit IDs, then check them with `git merge-base --is-ancestor <commit> origin/main` | `GAP`; `BLOCKER` if cited commits are already stranded | Merge commits; tag stranded commits you can still reach (fact `rebase-merge`) |
| 4 | Head branches auto-delete under squash or rebase-merge | Settings, General | `GAP` where commits are cited | Turn it off, or move to merge commits |
| 5 | Every workflow sets `permissions:` | `grep -L '^permissions:' .github/workflows/*.yml` | `GAP` per workflow | `contents: read` at the top (fact `permissions`) |
| 6 | Every job sets `timeout-minutes` | Read each job | `GAP` | Set it from the job's usual time, with room (fact `timeout`) |
| 7 | Actions pinned by tag or branch | `grep -n 'uses:' .github/workflows/*.yml` | `GAP` where the workflow reads secrets, writes or publishes | A full SHA with the version in a comment, and Dependabot (fact `sha-pin`) |
| 8 | The install doesn't fail on lockfile drift | Look for `pip install -r`, `npm install` or `uv sync --frozen` | `GAP`; `BLOCKER` where the docs call it a lockfile gate | `npm ci`, `uv sync --locked` (fact `uv-locked`) |
| 9 | CI doesn't run where work lands | The `on:` blocks, against the branches people push | `BLOCKER` where anything counts on it | `push` and `pull_request` with no branch filter |
| 10 | A required check comes from a path-filtered workflow | The ruleset's required checks, against each workflow's `on:` | `GAP`: pull requests that skip it can't merge | Remove the filter, or stop requiring the check (fact `skipped-pending`) |
| 11 | `paths` and `paths-ignore` on one event | Read the `on:` blocks | `DRIFT`: the workflow is invalid | Keep one (fact `paths-both`) |
| 12 | `pull_request_target` or `workflow_run` runs a pull request's code | Read those workflows' checkout and `run:` steps | `BLOCKER` | Move it to `pull_request` (`security.md`) |
| 13 | `pull_request_target` on a public repository with no event policy | Read the workflows, and the repository's Actions policy | `GAP`: it stops from 2 November 2026 (fact `prt-default`) | Move it, or set a policy |
| 14 | `${{ github.event.* }}` inside a `run:` script | `grep -n '\${{ github.event' .github/workflows/*.yml` | `BLOCKER` where the value is user-written | An environment variable (fact `injection`) |
| 15 | Release tags are lightweight, or the release route makes them so | `git for-each-ref refs/tags --format='%(refname:short) %(objecttype)'`; `commit` means lightweight | `GAP`; rate how the next tag gets made | An annotated tag from a job (`setup.md`, fact `tag-kinds`) |
| 16 | A job makes a release with `GITHUB_TOKEN`, and another workflow is meant to publish it | Look for `on: release` or `on: push: tags` workflows | `BLOCKER` where the docs say releases publish | Publish in the same job, or `workflow_call` (fact `token-no-trigger`) |
| 17 | Hooks are documented, but nothing installs them | `core.hooksPath`, a SessionStart hook, pre-commit config | `GAP` where the repository counts on them | `setup.md`, *Hooks* |
| 18 | Instructions say `--no-verify`, or to skip or quarantine a failing test | `grep -rn -e '--no-verify' -e quarantin .` | `DRIFT` | Remove them; fix the cause |
| 19 | Conflict markers in tracked files | The command below the table | `BLOCKER` | Resolve them, and add the check to CI |
| 20 | `.gitignore` lines that do nothing | Inline `#` comments, or `!` under an ignored directory: test with `git check-ignore -v` | `DRIFT` | Facts `gitignore-comment`, `gitignore-parent` |
| 21 | The commit grammar is unstated or unchecked | The context file; a CI check on commits or titles | `GAP` for a repository with several contributors or releases | `style.md`, and the commit-subjects example |
| 22 | A second release line with no branch, or backports without `-x` | `git log release/X.Y --grep 'cherry picked from'` | `GAP` | `setup.md`, *Release lines* |
| 23 | A scheduled scan in a public repository last ran over 60 days ago | Its run history | `GAP`: it has stopped (fact `schedule-60`) | Re-enable it; watch the date |
| 24 | The context file has a "current state" or status section | Read it | `DRIFT`: it goes stale | Move plans to one planning file, and status to the pull request or issue |

The conflict-marker search for check 19, which lists every line that starts with a merge's
opening, closing or base marker:

```sh
git grep -n -E '^(<{7}|>{7}|[|]{7})( |$)'
```
