# Setup: branching, merging, hooks, CI, releases and .gitignore

Read this when you set up or change how a repository branches, merges, deletes branches,
installs hooks, runs CI, cuts releases or keeps release lines. Facts are named by ID from
`facts.md`, and the examples are in `assets/`.

## Contents

- [Choose a branching model](#choose-a-branching-model)
- [Protect the default branch](#protect-the-default-branch)
- [Choose one merge strategy, and enforce it](#choose-one-merge-strategy-and-enforce-it)
- [Delete a branch only after checking what needs it](#delete-a-branch-only-after-checking-what-needs-it)
- [Hooks](#hooks)
- [CI on GitHub Actions](#ci-on-github-actions)
- [Releases](#releases)
- [Release lines and backports](#release-lines-and-backports)
- [.gitignore](#gitignore)

## Choose a branching model

- **Short-lived branches off the default branch are the default,** each merged through a pull
  request within a day or two. This is GitHub Flow, a form of trunk-based development, and
  DORA's research favours it (fact `dora`). With one maintainer the pull request still earns
  its place: it gives CI somewhere to run before the default branch moves.
- **Add release lines only when you support more than one released version** (see *Release
  lines and backports*).
- **A long-lived `develop` branch, as in Git Flow, costs more than it buys for most projects.**
  It suits a project that must hold releases back for a separate stabilisation stage. To move
  off it, see `modernization.md`.

## Protect the default branch

- Require a pull request, require the CI checks, and block force pushes and deletion. Use
  rulesets or classic branch protection. Which your plan allows is in
  project-bootstrap-and-audit's *Facts with an Expiry Date*.
- **A required check must report on every pull request.** A workflow skipped by a path filter
  leaves its check pending, and the pull request can't merge (fact `skipped-pending`). So never
  put a path filter on a workflow that provides a required check. Filter inside the job
  instead, or don't require that check.
- **A merge queue** needs `merge_group` in the workflow's `on:`, and exists only on
  organisation-owned repositories (fact `merge-queue`).

## Choose one merge strategy, and enforce it

| Strategy | What lands on the base | Are the branch's commits kept? | Choose it when |
|---|---|---|---|
| Merge commit | The branch's commits, plus a merge commit | Yes | Anything outside the repository cites commits by hash: pull request bodies, decision records, run reports, another repository. Or the branch's history matters |
| Squash | One new commit per pull request | No | Nothing outside cites the branch's commits, and you want one commit per reviewed change |
| Rebase and merge | The branch's commits, rewritten | No, they get new IDs (fact `rebase-merge`) | You want linear history, and nothing outside cites the branch's commits |

- **Where commits are cited from outside, only a merge commit keeps them.** Under squash or
  rebase-merge, the cited commits exist only on the branch, and deleting the branch strands
  them. One live repository lost its cited commits four minutes after a squash merge, when the
  branch was deleted.
- **Record the choice and its reason in the context file, then allow only that one** under
  Settings, General, Pull Requests, with the other two turned off. project-bootstrap-and-audit
  rates the choice and its enforcement (dimension 6, *Merging*).
- **Updating a branch:** rebase a branch only you use onto the base. Merge the base into a
  branch others share, because rebasing rewrites commits they already have. Locally,
  `git merge --no-ff` makes a merge commit and `git merge --ff-only` refuses anything else.

## Delete a branch only after checking what needs it

Before deleting a remote branch, check each of these:

1. **Its pull request is merged or closed.** Under squash or rebase-merge, "merged" can't be
   read from the history, because the branch's commits aren't in the base. Read the pull
   request's state.
2. **No commit that exists only on it is cited anywhere.** For each cited commit, run
   `git branch -r --contains <commit>`. If this branch is the only answer, keep it, or first
   tag the commit with an annotated tag (`git tag -a archive/<branch> -m "…" <commit>`).
3. **Nothing else uses it:** an open pull request based on it, a release line, a CI
   configuration, a sibling repository's records. Where you can't check a sibling repository,
   ask its owner rather than guessing.

Then:

- **Local branches:** from Git 2.56, `git branch --dry-run --delete-merged 'origin/*'` shows
  which local branches would go, and without `--dry-run` it deletes only those whose tip is
  already on their upstream (fact `delete-merged`). Plain `git branch -d` also refuses an
  unmerged branch. Use `-D` only after the checks above.
- **Never bulk-delete remote branches** by piping `git branch -r --merged` into
  `git push --delete`. `--merged` knows nothing of squash merges, citations or sibling
  repositories.
- **GitHub's "Automatically delete head branches" setting** is safe under merge commits, where
  the branch's commits live on in the base. Under squash or rebase-merge it strands every
  commit someone cites.

## Hooks

- **Hooks don't travel with a clone,** because `.git/hooks` isn't tracked. Commit a hooks
  directory and point Git at it with `git config core.hooksPath .githooks` (fact `hooks-path`),
  or use pre-commit or prek with a committed `.pre-commit-config.yaml` (facts `pre-commit`,
  `prek`).
- **A hook runs only where someone installed it.** An agent's cloud session starts from a fresh
  clone and runs nothing a README asks a person to run. So install the hook from a committed
  `SessionStart` hook in `.claude/settings.json` that runs `git config core.hooksPath .githooks`,
  or count on CI alone.
- **Hooks are for fast, local checks,** such as formatting, whitespace and secrets. CI re-runs
  every check, because a hook can be skipped. Nobody passes `--no-verify` to get past one: fix
  what it caught, or fix the hook.
- **A `pre-push` hook reads the refs being pushed from its standard input.** Check those,
  because the checked-out branch may not be the one being pushed.

Examples, both tested:

- [assets/githooks/commit-msg](../assets/githooks/commit-msg) refuses a subject that doesn't
  read "area: summary", and notes one longer than 50 characters.
- [assets/githooks/pre-push](../assets/githooks/pre-push) refuses a push that updates `main`
  directly, from whichever branch.

Copy them into `.githooks/` and run `chmod +x .githooks/*`, because an archive or an upload may
drop the executable bit.

## CI on GitHub Actions

project-bootstrap-and-audit's *Starter File Contents* has the full CI template. These are the
properties that matter, each with its reason:

- **`permissions: contents: read` at the top of every workflow** (fact `permissions`). Widen it
  only on the job that needs more.
- **`timeout-minutes` on every job.** Without it, a hung job runs for 360 minutes (fact
  `timeout`).
- **Every action pinned to a full commit SHA, with its version in a comment** (fact `sha-pin`).
  Turn on Dependabot's `github-actions` updates to move the pins, because a SHA pin gets no
  backported fix (fact `checkout-v7`).
- **`persist-credentials: false` on checkout,** unless a later step pushes (fact
  `persist-creds`).
- **Install from the lockfile, in a mode that fails on drift:** `npm ci`, or `uv sync --locked`.
  `uv sync --frozen` doesn't check the lockfile at all (fact `uv-locked`).
  project-bootstrap-and-audit has the command for each ecosystem (dimension 2).
- **Run on `push` and `pull_request` with no branch filter,** so work gets checked on the branch
  where it happens, not only after it merges.
- **`concurrency` with `cancel-in-progress` for pull request runs only.** A run on the default
  branch should finish.
- **Path filters:** use `paths` or `paths-ignore`, never both on one event (fact `paths-both`),
  and never on a required check (fact `skipped-pending`).
- **Tests prove they ran to the end.** Check that the test report exists, and that the number
  of tests it counts meets a recorded baseline. The standard's starter file has both guards.
- **A scheduled scan in a public repository stops after 60 days without activity** (fact
  `schedule-60`), with no failure shown. Read its last run date.
- **Lint workflows with actionlint, and scan them with zizmor** (facts `actionlint`, `zizmor`;
  `security.md`).

Example, tested: [assets/workflows/commit-subjects.yml](../assets/workflows/commit-subjects.yml)
checks each commit in a pull request against "area: summary". It fails when it finds no commits
to check, so "couldn't check" never passes.

## Releases

1. **Write the changelog entry before the tag** (`style.md`).
2. **Read CI's conclusion on the exact commit you're releasing.** A green run on another commit
   proves nothing about this one.
3. **Make an annotated tag.** Git's docs mean annotated tags for releases, and `git describe`
   uses nothing else by default (facts `tag-kinds`, `describe`). `gh release create` with a new
   tag name makes a lightweight tag, so create the tag first. With no local clone, a
   `workflow_dispatch` job makes it. project-bootstrap-and-audit's release gate gives the route
   (*How a tag gets cut when there is no local clone*).
4. **A tag or release the job makes with `GITHUB_TOKEN` starts no other workflow** (fact
   `token-no-trigger`). A publish workflow listening for `on: push: tags` or `on: release` never
   runs. Publish in the same job, or call the publish workflow with `workflow_call`.
5. **With immutable releases:** create the release as a draft, attach its assets, then publish.
   Once published, the tag can't move, and a deleted release's tag name can't be used again
   (fact `immutable`).

Example, tested: [assets/workflows/release.yml](../assets/workflows/release.yml) makes an
annotated tag as `github-actions[bot]` (fact `bot-identity`), and pushes it. It refuses a
malformed version, and a version the changelog has no section for.

## Release lines and backports

- **Keep a second release line only when users need fixes on an older version.** Each line
  has a branch, `release/X.Y`.
- **A fix lands on the default branch first,** then goes to the line with `git cherry-pick -x`,
  so the commit names its source (fact `cherry-x`). FFmpeg does this for 78 of the last 80
  commits on its `release/9.0`.
- **A fix meant for a backport stays focused,** with nothing it doesn't need, so it applies
  cleanly and is quick to review. FFmpeg's developer guide asks for exactly this.
- **Each backport is its own pull request against the release branch,** so that line's own CI
  runs on it. FFmpeg automates this: a label on the merged pull request opens the backport.
- **A point release takes security fixes, documented bugs and documentation,** and stays
  compatible with the line's earlier releases.
- **Which lines need a fix:** the ones containing the commit that introduced the bug. Its
  `Fixes:` trailer names it (`style.md`). Then run `git branch -r --contains <commit>` and
  `git tag --contains <commit>`.

## .gitignore

- **Start from GitHub's template for your language** (github/gitignore, CC0; fact
  `gitignore-templates`), and cut what doesn't apply.
- **A comment goes on its own line.** `#` starts a comment only at the start of a line (fact
  `gitignore-comment`). `*.frx  # binary form data` is one pattern, "`*.frx  # binary form
  data`", and it matches nothing.
- **A file can't be re-included under an excluded directory** (fact `gitignore-parent`).
  `.vscode/` followed by `!.vscode/extensions.json` keeps nothing. Write `.vscode/*`, then the
  `!` line.
- **Commit the lockfile, never ignore it.** For Rust, commit `Cargo.lock` for libraries too, as
  the starting point: the Cargo team dropped its old advice against it (fact `cargo-lock`).
- **Ignore secret files** such as `.env` and `.env.*`, and commit a `.env.example`. A secret that
  was already committed is rotated, not just untracked (`security.md`).
- **To find the rule that matched:** `git check-ignore -v <path>`. `git status --ignored` lists
  the ignored files. To stop tracking a file, `git rm --cached <path>`; the file stays on disk,
  and in history.
- **Your own editor and OS files** go in your global excludes file (`core.excludesFile`), not the
  project's `.gitignore`.
