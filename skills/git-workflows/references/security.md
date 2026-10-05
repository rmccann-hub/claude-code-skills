# Security: workflows, triggers, secrets and history

Read this when you write or review a workflow's triggers, permissions or third-party actions,
or when a secret has reached a commit. Facts are named by ID from `facts.md`.

## Permissions and credentials

- **Every workflow narrows its token at the top,** with `permissions: contents: read`, and a job
  that needs more asks for it by name (fact `permissions`). One workflow without the block is a
  finding, however many others have it.
- **Set the repository's default to read-only too,** under Settings, Actions, General, Workflow
  permissions, and leave "Allow GitHub Actions to create and approve pull requests" off (fact
  `workflow-permissions`). A workflow that forgets its block then gets read access, not write.
  A new repository in a personal account starts that way (fact `token-default`). Check an older
  one, and one an organization owns.
- **`persist-credentials: false` on checkout,** unless a later step in that job pushes. Otherwise
  the token stays in the checkout for every later step, including third-party ones (fact
  `persist-creds`).
- **Secrets come only through `secrets.*`, into the steps that need them.** Never echo a secret,
  never write one to a file you upload, and never put one in a command's arguments, where
  process listings and logs can show it.

## Third-party actions

- **Pin each action to a full commit SHA, with its version in a comment.** A tag can be moved
  to other code, and a commit can't (fact `sha-pin`). Check that the SHA comes from the
  action's own repository, not a fork of it.
- **Keep the pins moving:** turn on Dependabot version updates for `github-actions`, and check
  that its pull requests reach the pinned lines. A pinned action gets no backported fix, so a
  pin nobody updates goes stale (fact `checkout-v7`).
- **Leave "Dependabot on self-hosted runners" off** unless a runner labeled for Dependabot
  exists. Its jobs wait for one, and fail after 24 hours (fact `dependabot-runners`), so no
  update arrives.
- **Enforce pinning by policy** where you can (fact `sha-policy`), so an unpinned action fails
  instead of relying on review. The policy covers GitHub's own actions too, and lets a reusable
  workflow keep a tag (fact `sha-policy-scope`). It also fails an action that calls an unpinned
  one (fact `sha-policy-nested`), so read each action's `action.yml` for its own `uses:` lines
  before turning it on, and watch the next runs.
- **Read what an action runs before adopting it.** It runs with the job's token and secrets.

## Untrusted input

Pull request titles, branch names (`github.head_ref` among them), issue and comment bodies, and
commit messages are all written by whoever opened them. Never put `${{ … }}` of any of them
inside a `run:` script, because the shell runs whatever the text contains. Pass it through an
environment variable instead (fact `injection`):

```yaml
      - name: Greet the pull request
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: printf 'Checking %s\n' "$TITLE"
```

## Triggers that run with secrets

- **`pull_request_target` runs in the base repository's context, with its secrets,** for pull
  requests from forks. Since 8 December 2025 it always runs the default branch's copy of the
  workflow (fact `prt-branch`). `actions/checkout` v7 refuses the common unsafe checkouts in it, and
  `allow-unsafe-pr-checkout` opts out (fact `checkout-v7`). From 2 November 2026, public
  repositories that set no event policy of their own have it disabled by default (fact
  `prt-default`).
- **So prefer `pull_request`,** which runs a fork's code without your secrets. Where you need
  `pull_request_target`, such as for labeling or commenting, never check out or run the pull
  request's code in it.
- **`workflow_run` carries the same risk** when it acts on the output of a pull request's run.
  Treat what that run produced as untrusted input.
- **On a public repository, require approval for all external contributors** before their pull
  requests' workflows run. The default asks only first-time contributors, and one merged
  change, however small, ends that (fact `fork-approval`).

## Scanning workflows

- **actionlint** checks that a workflow is valid, and with ShellCheck it checks the scripts in
  `run:` steps (fact `actionlint`). It catches things like an unquoted `: ` in a step name,
  which makes the file invalid YAML.
- **zizmor** looks for security problems: dangerous triggers, template injection, credentials
  left in a checkout, and over-broad permissions (fact `zizmor`). Its injection audit follows
  more contexts than a search for `${{ github.event` can.
- Run both in CI, with the tools pinned by version.
- **CodeQL's default setup** is available on every public repository, under Settings, Advanced
  Security (fact `codeql-default`). It adds a check to each pull request, and a release job that
  waits on every check then waits on it too.

## A secret in a commit

1. **Rotate it first.** Once pushed, it's compromised: forks, clones, caches and the platform's
   own views may hold it, and removing the commit doesn't take it back.
2. **Then remove it from the tree,** add the file to `.gitignore`, and commit an example file
   without the value.
3. **Rewrite history only if you must,** for example where the value is still sensitive after
   rotation. It rewrites every later commit, breaks everyone's clone and strands every citation.
   Rotation is the remedy; a rewrite is cleanup.
4. **Name the secret by where it was, never by its value,** in the issue, the commit message and
   the decision record.

project-bootstrap-and-audit rates secret handling, push protection and the secret-scan job
(dimension 7), and its facts give push protection's defaults.

## Signed tags

If you sign, sign release tags with `git tag -s`, which makes an annotated tag. A release job's
tag then needs a signing key the job can reach, so decide where that key lives before requiring
signed tags.
