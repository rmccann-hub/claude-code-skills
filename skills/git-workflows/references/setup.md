# Setup: branching, merging, hooks, CI, releases and .gitignore

Read this when you set up or change how a repository branches, merges, deletes branches,
installs hooks, runs CI, cuts releases or keeps release lines. Facts are named by ID from
`facts.md`, and the examples are in `assets/`.

## Contents

- [Choose a branching model](#choose-a-branching-model)
- [Protect the default branch](#protect-the-default-branch)
- [Choose one merge strategy, and enforce it](#choose-one-merge-strategy-and-enforce-it)
- [Delete a branch only after checking what needs it](#delete-a-branch-only-after-checking-what-needs-it)
- [Rebasing your own branch, conflicts and recovery](#rebasing-your-own-branch-conflicts-and-recovery)
- [Hooks](#hooks)
- [CI on GitHub Actions](#ci-on-github-actions)
- [Releases](#releases)
- [Release lines and backports](#release-lines-and-backports)
- [.gitignore](#gitignore)

## Choose a branching model

- **Short-lived branches off the default branch are the default,** each merged through a pull
  request within a day or two. This is GitHub Flow (fact `github-flow`), a form of trunk-based
  development, and DORA's research favours it (fact `dora`). Why a pull request earns its place
  even with one maintainer is project-bootstrap-and-audit's *Review, with one maintainer*.
- **Add release lines only when you support more than one released version** (see *Release
  lines and backports*).
- **A long-lived `develop` branch, as in Git Flow, costs more than it buys for most projects.**
  It suits a project that must hold releases back for a separate stabilisation stage. Git
  Flow's own author now advises a simpler workflow for software delivered continuously (fact
  `gitflow-note`).

## Protect the default branch

- Require a pull request, require the CI checks, and block force pushes and deletion. Use
  rulesets or classic branch protection. Which your plan allows is in
  project-bootstrap-and-audit's *Facts with an Expiry Date*.
- **Import the rulesets rather than building them by hand.** Each imports from a JSON file,
  through the New ruleset menu under Settings, Rules, Rulesets (fact `ruleset-import`), in the
  shape GitHub's own starter rulesets use (fact `ruleset-recipes`):
  - [assets/rulesets/default-branch.json](../assets/rulesets/default-branch.json) blocks
    deletion and force pushes, and requires a pull request with no approval, which suits one
    maintainer (fact `pr-rule`). After importing it, add the CI checks under "Require status
    checks to pass", by the names their jobs report, which a template can't know. It leaves
    the merge method to the repository's Pull Requests setting (see *Choose one merge
    strategy*).
  - [assets/rulesets/release-tags.json](../assets/rulesets/release-tags.json) stops a `v*` tag
    being moved, deleted or force-pushed. It leaves creation open, so the release job below can
    still make the tag.
- **A required check must report on every pull request.** A workflow skipped by a path filter
  leaves its check pending, and the pull request can't merge (fact `skipped-pending`). So never
  put a path filter on a workflow that provides a required check. A job skipped by its `if:`
  reports success instead, even as a required check (fact `job-if-success`), so a condition
  that skips the tests passes the pull request with nothing tested. Where tests are skipped by
  path, require one final job that `needs:` the others and fails if any of them failed.
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
   `git branch -r --contains <commit>`. It answers from the refs you have, so in a shallow or
   single-branch clone, such as CI's or a cloud session's, fetch every branch first, with
   `--unshallow` if `git rev-parse --is-shallow-repository` prints `true`. If this branch is
   the only answer, keep it, or tag the commit and push the tag:
   `git tag -a archive/<branch> -m "…" <commit>`, then `git push origin refs/tags/archive/<branch>`.
   A tag unpushed is lost with the clone, and a pushed tag starts any workflow that runs
   `on: push: tags` for that name. After a squash, the commits are still fetchable from the pull
   request itself: `git fetch origin pull/<number>/head` (fact `pr-refs`).
3. **Nothing else uses it:** an open pull request based on it, a release line, a CI
   configuration, a sibling repository's records. Where you can't check a sibling repository,
   ask its owner rather than guessing.

Then:

- **Local branches:** `git fetch --prune`, then `git branch -vv` marks as `gone` each branch
  whose remote branch was deleted. Check each one's pull request before deleting it: a remote
  branch can go without being merged. Plain `git branch -d` refuses a branch that isn't merged,
  and after a squash merge it always refuses. Use `-D` only after the checks above.
- **Git 2.56's `git branch --delete-merged`** deletes local branches whose tip is on their
  upstream, with `--dry-run` to preview (fact `delete-merged`). It leaves alone a branch whose
  upstream is gone, and one whose push would update that upstream, which covers most branches
  made with `git push -u`. It suits branches that track a shared branch such as `origin/main`.
- **Never bulk-delete remote branches** by piping `git branch -r --merged` into
  `git push --delete`. `--merged` knows nothing of squash merges, citations or sibling
  repositories.
- **GitHub's "Automatically delete head branches" setting** (fact `auto-delete`) is safe under
  merge commits, where the branch's commits live on in the base. Under squash or rebase-merge
  it takes the branch the moment the pull request merges, and with it every commit only that
  branch held.

## Rebasing your own branch, conflicts and recovery

- **Push a rebased branch with `git push --force-with-lease --force-if-includes`.** The first
  refuses when the remote branch has moved since you last fetched it. The second also refuses
  when a fetch brought in commits you never looked at, which the first can't tell apart (fact
  `force-if-includes`). Plain `--force` overwrites whatever is there. Rebase only a branch
  nobody else has.
- **On a conflict,** read the whole output, then `git status` lists the files. Resolve each
  one, `git add` it, and run `git rebase --continue` or `git merge --continue`. `--abort` puts
  everything back as it was before you started.
- **During a rebase, `--ours` and `--theirs` swap meaning:** `--ours` is the branch you're
  rebasing onto, and `--theirs` is your own work (fact `rebase-ours`).
- **A conflict you resolve again and again,** such as in a long-lived branch, can be recorded
  once: `git config rerere.enabled true` replays your resolution when it recurs (fact
  `rerere`).
- **A commit lost to a reset or a rebase** is still in the reflog, which records where each
  branch pointed (fact `reflog`). `git reflog` finds it, and `git branch rescue <commit>` gets
  it back. The reflog belongs to one clone, and it expires. Uncommitted work was never in it.

## Hooks

- **Hooks don't travel with a clone,** because `.git/hooks` isn't tracked. Commit a hooks
  directory and point Git at it with `git config core.hooksPath .githooks` (fact `hooks-path`),
  or use pre-commit or prek with a committed `.pre-commit-config.yaml` (facts `pre-commit`,
  `prek`).
- **A hook runs only where someone installed it.** An agent's cloud session starts from a fresh
  clone and runs nothing a README asks a person to run. So install the hook from a committed
  `SessionStart` hook in `.claude/settings.json` that runs `git config core.hooksPath .githooks`,
  or count on CI alone.
- **Propose a client-side hook only where a persistent local clone exists.** Where the only
  clones are cloud sessions', a hook gates only the sessions that happen to install it, and
  CI is the gate. project-bootstrap-and-audit's dimension 6 sets this rule.
- **Hooks are for fast, local checks,** such as formatting, whitespace and secrets. CI re-runs
  what a commit hook checks, and branch protection does on the server what a pre-push hook does.
  Nobody passes `--no-verify` to get past one: fix what it caught, or fix the hook.
- **A `pre-push` hook reads the refs being pushed from its standard input.** Check those,
  because the checked-out branch may not be the one being pushed.

Examples, both tested:

- [assets/githooks/commit-msg](../assets/githooks/commit-msg) refuses a subject that doesn't
  read "area: summary", and notes one longer than 50 characters.
- [assets/githooks/pre-push](../assets/githooks/pre-push) refuses a push that updates `main`
  directly, from whichever branch.

Copy them into `.githooks/`, then commit them as executable:
`git add --chmod=+x .githooks/*`. Check with `git ls-files -s .githooks`, which shows `100755`
for each. `chmod +x` isn't enough on Windows, where Git for Windows ignores file modes by
default, so the change never reaches the commit and every clone gets a hook Git won't run. Add
`.githooks/* text eol=lf` to `.gitattributes`, so a Windows checkout doesn't give the scripts
CRLF line endings.

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
  where it happens, not only after it merges. That runs a pull request's commits twice, once as
  the branch and once merged with its base (fact `pr-merge-ref`). Where CI is slow, run `push`
  on the default branch only, with `pull_request`, and open a draft pull request for every
  branch.
- **`concurrency` with `cancel-in-progress` for pull request runs only** (fact
  `cancel-in-progress`). A run on the default branch should finish.
- **A merge queue runs workflows on `merge_group`,** so a required check's workflow lists it
  in `on:` (fact `merge-queue`).
- **Path filters:** use `paths` or `paths-ignore`, never both on one event (fact `paths-both`),
  and never on a required check (fact `skipped-pending`).
- **Tests prove they ran to the end.** A run that stops early can still exit 0. The standard's
  starter CI file has a collection guard, which counts the tests collected, not the tests that
  ran. [assets/workflows/tests.yml](../assets/workflows/tests.yml) adds the completion guard:
  the test report must exist, and count at least as many tests as `.test-baseline`.
- **A scheduled scan in a public repository stops after 60 days without activity** (fact
  `schedule-60`), with no failure shown. Read its last run date.
- **Lint workflows with actionlint, and scan them with zizmor** (facts `actionlint`, `zizmor`),
  in CI, with both tools pinned by version.

Examples, tested:

- [assets/workflows/commit-subjects.yml](../assets/workflows/commit-subjects.yml) checks each
  commit in a pull request against "area: summary". It lets through the subjects `git revert`
  writes, refuses `fixup!` and `squash!` commits that were never squashed, and fails when it
  finds no commits to check, so "couldn't check" never passes. Give Dependabot a prefix, such
  as `commit-message: prefix: "deps"`, and its subjects pass too (fact `dependabot-prefix`).
- [assets/workflows/tests.yml](../assets/workflows/tests.yml) runs the tests and proves they
  finished.

## Releases

1. **Write the changelog entry,** under the version's heading, before the tag.
2. **Read CI's conclusion on the exact commit you're releasing.** A green run on another commit
   proves nothing about this one.
3. **Tag that commit by its SHA,** never a branch: a branch's tip may have moved past the
   release commit. Tag it before a later commit changes a workflow. A job's token can't push a
   tag whose commit carries a workflow file that no branch still has as it was
   (fact `workflow-scope`).
4. **Make an annotated tag.** Git's docs mean annotated tags for releases, and `git describe`
   uses nothing else by default (facts `tag-kinds`, `describe`). `gh release create` with a new
   tag name makes the tag itself, and it isn't annotated (fact `gh-release-tag`). So push the
   annotated tag first, then run `gh release create --verify-tag`, which refuses a tag that
   doesn't exist yet. With no local clone, a `workflow_dispatch` job makes the tag.
   project-bootstrap-and-audit's release gate gives the route (*How a tag gets cut when there
   is no local clone*).
5. **A tag or release the job makes with `GITHUB_TOKEN` starts no other workflow** (fact
   `token-no-trigger`). A publish workflow listening for `on: push: tags` or `on: release` never
   runs. Publish in the same job, or call the publish workflow with `workflow_call`.
6. **With immutable releases:** create the release as a draft, attach its assets, then publish.
   Once published, the tag can't move, and a deleted release's tag name can't be used again
   (fact `immutable`).

Example, tested: [assets/workflows/release.yml](../assets/workflows/release.yml) takes a version
and a commit SHA. It refuses a version that isn't Semantic Versioning, a commit that isn't on
the default branch, a commit whose `CHANGELOG.md` has no section for the version, a commit
carrying a workflow file no branch has as it is, and a commit with a check that hasn't passed,
or with no checks at all. Its own earlier attempts don't count as checks. Then it makes the
annotated tag on that commit as `github-actions[bot]` (fact `bot-identity`), and pushes it. A
run that fails after pushing can be run again: it carries on from a tag it would have made.
Only its job may write, and checkout keeps no credentials.

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
- **What a point release may take** is the standard's rule: project-bootstrap-and-audit's
  release gate.
- **Which lines need a fix:** the ones containing the commit that introduced the bug, which the
  fix's `Fixes:` trailer names where the author knew it. Then run
  `git branch -r --contains <commit>` and `git tag --contains <commit>`.

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
  was already committed is rotated first: removing it from the tree doesn't take it back.
- **To find the rule that matched:** `git check-ignore -v <path>`. `git status --ignored` lists
  the ignored files. To stop tracking a file, `git rm --cached <path>`: it leaves your copy on
  disk (fact `rm-cached`), and the file stays in history. Everyone else who pulls that commit
  has the file deleted, because to their clone it's a tracked file being removed. Tell them to
  copy it first.
- **Your own editor and OS files** go in your global excludes file (`core.excludesFile`), not the
  project's `.gitignore`.
