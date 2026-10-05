# Audit: checking a repository's Git and CI setup

Read this when you review how a repository branches, merges, runs CI and releases, without a
full audit. For a full audit, with tiers and a report, use project-bootstrap-and-audit: it rates
most of these checks by tier (dimensions 6, 8 and 10, and its release gate), and its rating wins
where the two differ. The status words are the standard's:

- **`BLOCKER`:** a live exposure, or a check reporting success while measuring nothing.
- **`DRIFT`:** configured, but no longer doing what it says.
- **`GAP`:** missing something the project needs.
- **`OVER`:** heavier than the project needs.
- **`MIRROR`:** the truth is outside the repository, such as a platform setting you've read
  rather than a file.
- **`UNVERIFIABLE-HERE`:** can't be established from this session, such as a settings page
  without admin access. Checks 2, 4, 13 and 23 need that access.
- **`OK`**, and **`N/A`**.

Facts are named by ID from `facts.md`. Workflows may end in `.yml` or `.yaml`, so every search
here covers both.

| # | Check | How to look | Usual status | Fix |
|---|---|---|---|---|
| 1 | The merge strategy is recorded, with its reason | The context file (`AGENTS.md` or `CLAUDE.md`) and the decision record | `GAP` from T2 if missing | Record it in the context file, with the reason: whether anything cites commits |
| 2 | The platform allows only the recorded strategy | Settings, General, Pull Requests, or `gh api repos/OWNER/REPO --jq '.allow_merge_commit, .allow_squash_merge, .allow_rebase_merge'` | `GAP` from T2 if more are on | Turn the others off |
| 3 | Squash or rebase-merge where commits are cited from outside | Search pull request bodies, the decision record and sibling repositories for commit IDs, then check each with `git merge-base --is-ancestor <commit> origin/main`, after fetching every branch | `GAP`, naming each stranded commit | Merge commits. A stranded commit is still fetchable as `pull/<number>/head` (fact `pr-refs`): tag it and push the tag |
| 4 | Head branches auto-delete under squash or rebase-merge | Settings, General (fact `auto-delete`) | `GAP` where commits are cited | Turn it off, or move to merge commits |
| 5 | Every workflow narrows its token at the top | `grep -L '^permissions:' .github/workflows/*.y*ml`, then read each top-level block for `write-all` or a write grant | `GAP` per workflow | `contents: read` at the top, and any wider grant on the job that needs it (fact `permissions`) |
| 6 | Every job sets `timeout-minutes` | Read each job | `GAP` | Set it from the job's usual time, with room (fact `timeout`) |
| 7 | Actions pinned by tag or branch | `grep -n 'uses:' .github/workflows/*.y*ml` | `GAP` where the workflow reads secrets, writes or publishes | A full SHA with the version in a comment, and Dependabot (fact `sha-pin`) |
| 8 | The install doesn't fail on lockfile drift | Look for `pip install -r`, `npm install` or `uv sync --frozen` | `GAP`; `BLOCKER` where the docs call it a lockfile gate | `npm ci`, `uv sync --locked` (fact `uv-locked`) |
| 9 | CI doesn't run where work lands | The `on:` blocks, against the branches people push | `BLOCKER` where anything counts on it | `push` and `pull_request` with no branch filter |
| 10 | A required check comes from a path-filtered workflow | The ruleset's required checks, against each workflow's `on:` | `GAP`: pull requests that skip it can't merge | Remove the filter, or stop requiring the check (fact `skipped-pending`) |
| 11 | A required check comes from a job with an `if:` | The required checks, against each job's `if:` | `BLOCKER` where the condition can skip it on a pull request that changes code: it reports success having run nothing (fact `job-if-success`) | Remove the condition, or require a final job that `needs:` the others and fails if any failed |
| 12 | `paths` and `paths-ignore` on one event | Read the `on:` blocks | `DRIFT`: the workflow is invalid | Keep one (fact `paths-both`) |
| 13 | `pull_request_target` or `workflow_run` runs a pull request's code | Read those workflows' checkout and `run:` steps | `BLOCKER` | Move it to `pull_request`, which runs a fork's code without your secrets |
| 14 | `pull_request_target` on a public repository with no event policy | Read the workflows, and the repository's Actions policy | `GAP`: it stops from 2 November 2026 (fact `prt-default`) | Move it, or set a policy |
| 15 | Untrusted text inside a `run:` script | `grep -nE -e '[$][{][{] *github[.]event' -e '[$][{][{] *github[.]head_ref' .github/workflows/*.y*ml`, then zizmor, whose injection audit follows more contexts | `BLOCKER` where the value is user-written | An environment variable (fact `injection`) |
| 16 | Release tags are lightweight, or the release route makes them so | `git for-each-ref refs/tags --format='%(refname:short) %(objecttype)'`; `commit` means lightweight | `GAP`; rate how the next tag gets made | An annotated tag on the release commit's SHA, made by a job (facts `tag-kinds`, `gh-release-tag`) |
| 17 | A job makes a release with `GITHUB_TOKEN`, and another workflow is meant to publish it | Look for `on: release` or `on: push: tags` workflows | `BLOCKER` where the docs say releases publish | Publish in the same job, or `workflow_call` (fact `token-no-trigger`) |
| 18 | Hooks are documented, but nothing installs them | `core.hooksPath`, a SessionStart hook, pre-commit config | `GAP` where the repository counts on them | Where a persistent local clone exists, commit the hooks as executable and set `core.hooksPath`; otherwise count on CI |
| 19 | Instructions say `--no-verify`, or to skip or quarantine a failing test | `grep -rn -e '--no-verify' -e quarantin .` | `DRIFT` | Remove them; fix the cause |
| 20 | Conflict markers in tracked files | The command below the table | `BLOCKER` | Resolve them, and add the CI form below |
| 21 | `.gitignore` lines that do nothing | Inline `#` comments, or `!` under an ignored directory: test with `git check-ignore -v` | `DRIFT` | Facts `gitignore-comment`, `gitignore-parent` |
| 22 | The commit grammar is unstated or unchecked | The context file; a CI check on commits, or on titles where squash titles come from the pull request (fact `squash-default`) | `GAP` from T2 | Write the grammar in the context file, and check it with the commit-subjects example |
| 23 | A second release line with no branch, or backports without `-x` | `git log release/X.Y --grep 'cherry picked from'` | `GAP` | A `release/X.Y` branch, and `git cherry-pick -x` for each backport (fact `cherry-x`) |
| 24 | A scheduled scan in a public repository last ran over 60 days ago | Its run history | `GAP`: it has stopped (fact `schedule-60`) | Re-enable it; watch the date |
| 25 | The context file has a "current state" or status section | Read it | `DRIFT`: it goes stale | Move plans to one planning file, and status to the pull request or issue |

The conflict-marker search for check 20 lists every line that starts with a merge's opening,
closing or base marker. It exits 0 when it finds some, 1 when the tree is clean, and 2 or more
when the search itself failed:

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
