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
- **Workflow dependency lockfiles go further, and are in public preview** (fact
  `actions-lockfile`). One file records the exact commit of every action, including the
  actions those actions call, and GitHub checks the source repository at run time. Try one
  where a preview feature is acceptable. Until it's generally available, SHA pins stay the
  rule.
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

## Personal information in history

An email address in commit metadata, or a home folder in a committed log, can't be rotated.
Removing it means rewriting history. That's the one exception to rule 3, and only when the
owner asks for it, knowing what it costs.

1. **Count before choosing.** Read-only, count each item in every place it can be:
   - commit metadata, messages and files;
   - release notes and release files, and published packages;
   - tags, branches and pull request refs.

   Then let the owner choose the scope with the numbers in front of them. Some copies can't be
   changed at all: a published package, an immutable release, a transparency log. A username
   that also starts the owner's public handle hides almost nothing when it's removed. In one
   live repository, narrowing the job to the email address alone made it about fifty times
   smaller, and left the other repository it shared a review loop with untouched.
2. **Change only what you must.** For an address in metadata only, use
   `git filter-repo --mailmap` (fact `filter-repo-mailmap`) with `--sensitive-data-removal`,
   version 2.47 or later (fact `sdr-version`). Add `--preserve-commit-hashes` to keep commit
   messages byte for byte (fact `filter-repo-hashes`). Every commit ID still changes, from the
   first rewritten commit on.
3. **Keep cited IDs resolvable.** Commit the tool's old-to-new map, and have every reader of
   commit IDs look an old ID up in it before asking Git, since an older clone still holds the
   old objects. Leave sent records as written. Keep the map file out of any citation scan:
   otherwise it meets the scan's floor on its own. Where another repository cites yours, agree
   the change with it word for word first, then run each side's checker on the other's tree.
4. **Rehearse on a scratch mirror,** and run the full test suite there. In that live rewrite,
   the suite found all 32 places that read commit IDs in one pass. The rewrite is
   deterministic, so the rehearsal's map has the same digest as the real run's, unless a
   branch moved in between.
5. **Hand the owner one script** that:
   - works in a new folder it names at the start and the end;
   - installs the pinned tool there, checked with `--require-hashes`;
   - before it pushes, checks for zero matches, the same commit count and the same refs, and
     that the trees, names, dates and messages are unchanged;
   - asks the owner to type `YES`, and pushes only then;
   - pushes with `--atomic` and `--force-with-lease=<ref>:<old>` on every ref, under
     `-c credential.helper=`, so the token isn't saved;
   - compares `git ls-remote` with what it pushed, and prints a summary to paste back.

   Rehearse the script itself against a local bare repository, including someone typing "no"
   and a stale lease. A fine-grained token needs Workflows write access as well as Contents,
   since the push rewrites commits that carry workflow files (fact `workflow-scope`).
6. **Warn the owner in advance:**
   - every signed commit loses its Verified badge (fact `rewrite-signatures`);
   - the first CI run after the force push can go red, where a gate compares against a commit
     that no longer exists;
   - rulesets that block force pushes must be off for the push, and on again after;
   - old commits stay viewable through `refs/pull/*` until GitHub Support removes them (fact
     `pr-refs-readonly`). On 2026-10-12, GitHub's support form had no "sensitive data"
     category: the route that worked was Repositories, then Repository features, then
     Branches. Its "Deletes" choice leads to deleting the whole repository, so avoid it;
   - a shipped app that checks out a fixed commit from the rewritten repository can't install
     afterward. Check every consumer of the repository first.
7. **Afterward, refresh every clone, the agent's own included.** A stale local branch still
   points at old history: one checker read the map from one and reported 13 false refusals.
   Run `git fetch --force --tags`, reset each local branch to its remote, or check from a
   fresh clone.

## Signed tags

If you sign, sign release tags with `git tag -s`, which makes an annotated tag. A release job's
tag then needs a signing key the job can reach, so decide where that key lives before requiring
signed tags.
