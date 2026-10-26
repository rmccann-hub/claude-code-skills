# Actions security

Read this for writing or reviewing a workflow's permissions, its third-party actions and how
they're pinned, untrusted input in a `run:` step, triggers that run with secrets such as
`pull_request_target`, moving off Node 20 actions, or scanning workflows.

It covers what a workflow can be made to do by someone else. Triggers, timeouts and required
checks are `ci-workflows`; a secret that already reached a commit is `leaked-data`.

## Rules

1. **Every workflow narrows its token at the top,** with `permissions: contents: read`, and a
   job that needs more asks for it by name (fact `permissions`).
2. **Pin each action to a full commit SHA, with its version in a comment,** and keep the pins
   moving with Dependabot.
3. **Never put `${{ … }}` of untrusted text inside a `run:` script.** Pass it through an
   environment variable.
4. **Prefer `pull_request` to `pull_request_target`,** and never check out or run a pull
   request's code with secrets in reach.

### Permissions and credentials

- **One workflow without the `permissions:` block is a finding,** however many others have it.
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

### Third-party actions

- **A tag can be moved to other code, and a commit can't** (fact `sha-pin`). Check that the SHA
  comes from the action's own repository, not a fork of it.
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

### Untrusted input

Pull request titles, branch names (`github.head_ref` among them), issue and comment bodies, and
commit messages are all written by whoever opened them. The shell runs whatever such text
contains, so pass it through an environment variable (fact `injection`):

```yaml
      - name: Greet the pull request
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: printf 'Checking %s\n' "$TITLE"
```

### Triggers that run with secrets

- **`pull_request_target` runs in the base repository's context, with its secrets,** for pull
  requests from forks. Since 8 December 2025 it always runs the default branch's copy of the
  workflow (fact `prt-branch`). `actions/checkout` v7 refuses the common unsafe checkouts in it,
  and `allow-unsafe-pr-checkout` opts out (fact `checkout-v7`). From 2 December 2026, public
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

### Scanning workflows

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

### Moving off older practice

- **From tag-pinned to SHA-pinned actions:**
  1. For each `uses:`, take the SHA of the version you use from the action's own repository:
     `git ls-remote --tags https://github.com/OWNER/ACTION 'refs/tags/v7.0.1*'`. For an
     annotated tag it prints two lines: the tag object's SHA, then the commit's, on the line
     ending `^{}`. Pin the commit's.
  2. Replace `@v7` with `@<full SHA> # v7.0.1`.
  3. Turn on Dependabot version updates for `github-actions`, and check its pull requests reach
     the pinned lines.
  4. Where you can, require pinning by policy (fact `sha-policy`).
- **Off actions that run on Node 20:** the runners no longer ship Node 20 (fact `node20`). Move
  each action to its current major, from its release page, and pin it by SHA.
- **Off `pull_request_target`:**
  1. Move what the workflow does to `pull_request`, which has no secrets for forks.
  2. Where it must stay, because it labels or comments, make sure it never checks out or runs
     the pull request's code.
  3. On a public repository, set an explicit event policy before 2 December 2026, or it stops
     running (fact `prt-default`).

## Mistakes

- **Suggesting `actions/checkout@v4` or other old majors from training data.** Node 20 is gone
  from the runners (fact `node20`). Take the version and SHA from the action's release page, or
  from fact `checkout-sha`.
- **Assuming a SHA-pinned action gets security backports.** It doesn't (fact `checkout-v7`).
- **`${{ github.event.pull_request.title }}` inside `run:`**, which is shell injection (fact
  `injection`).
- **Checking out the pull request's head in `pull_request_target`** to build or test it. Fork
  code then runs with your secrets.
- **Taking a SHA from a fork of the action,** or from a search result. Take it from the action's
  own repository.
- **Turning on the SHA-pinning policy without reading each action's own `uses:` lines.** An
  action that calls an unpinned one fails the run (fact `sha-policy-nested`).

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`. The checks of
the trigger policy and the token's default need admin access to the settings, or they're
`UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Every workflow narrows its token at the top | `grep -L '^permissions:' .github/workflows/*.y*ml`, then read each top-level block for `write-all` or a write grant | `GAP` per workflow | `contents: read` at the top, and any wider grant on the job that needs it (fact `permissions`) |
| Actions pinned by tag or branch | `grep -n 'uses:' .github/workflows/*.y*ml` | `GAP` where the workflow reads secrets, writes or publishes | A full SHA with the version in a comment, and Dependabot (fact `sha-pin`) |
| `pull_request_target` or `workflow_run` runs a pull request's code | Read those workflows' checkout and `run:` steps | `BLOCKER` | Move it to `pull_request`, which runs a fork's code without your secrets |
| `pull_request_target` on a public repository with no event policy | Read the workflows, and the repository's Actions policy | `GAP`: it stops from 2 December 2026 (fact `prt-default`) | Move it, or set a policy |
| Untrusted text inside a `run:` script | `grep -nE -e '[$][{][{] *github[.]event' -e '[$][{][{] *github[.]head_ref' .github/workflows/*.y*ml`, then zizmor, whose injection audit follows more contexts | `BLOCKER` where the value is user-written | An environment variable (fact `injection`) |
| The token's default is read and write | Settings, Actions, General, Workflow permissions | `GAP`, whatever the workflows declare: one that forgets its block gets write access | The read-only setting (fact `workflow-permissions`) |
| Dependabot's jobs wait for a self-hosted runner that doesn't exist | Dependabot's runs in the Actions tab: queued, or failed after 24 hours | `DRIFT`: configured, and no update arrives | Turn off "Dependabot on self-hosted runners" (fact `dependabot-runners`) |

## Why

### Pinning actions by SHA

**The advice.** Pin each action to a full commit SHA, with its version in a comment, and let
Dependabot move the pins.

**Why.** A tag can be moved. In March 2025 an attacker moved every tag of
`tj-actions/changed-files` onto a commit that printed secrets into build logs (fact
`tj-actions`). Workflows pinned by tag ran it; workflows pinned by SHA didn't. A full SHA can't
be moved (fact `sha-pin`), and a lockfile, now in preview, also pins the actions an action
calls (fact `actions-lockfile`).

**What others do.** GitHub's starter workflows pin GitHub's own actions by tag, which reads
easily and picks up fixes within a major version, but require every other action to be pinned
by SHA (fact `starter-pins`). Many projects keep tag pins for the same convenience.

**What each choice costs.** SHA pins need a bot, such as Dependabot, to raise updates, and they
get no security fix until you take that update.

**What could be better.** Require SHA pinning by policy (fact `sha-policy`), so no pull request
can bring back a tag pin.

### Narrowing the token

**The advice.** `permissions: contents: read` at the top of every workflow, wider grants only on
the job that needs them, and a read-only default for the repository.

**Why.** A token that can only read can't be used to write, whatever a compromised step tries.
The repository's default catches the workflow that forgets its block.

**What it costs.** A job that needs to write must say so, and one that forgets fails with a
permissions error the first time it runs.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `permissions` | `permissions:` narrows what the job's `GITHUB_TOKEN` can do | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "modify the default permissions granted to the GITHUB_TOKEN" | 2026-09-30 | 2027-03-31 |
| `sha-pin` | GitHub tells a repository that can't adopt a lockfile to pin each action to a full-length commit SHA, taken from the action's own repository | [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) | "Pin references to actions to a commit SHA in your workflow files." | 2026-10-12 | 2027-04-12 |
| `actions-lockfile` | Workflow dependency lockfiles are in public preview: `.github/workflows/actions.lock` records the exact commit of every action a repository's workflows use, the ones those actions call included, and is generated with the `gh actions-lock` extension. GitHub calls a lockfile stronger than SHA pins | [Workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles) | "Workflow dependency lockfiles are in public preview and subject to change." | 2026-10-12 | 2027-01-12 |
| `sha-policy` | Repository and organization policy can require SHA-pinned actions | [GitHub changelog, 2025-08-15](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/) | "Administrators can now enforce the use of SHA pinning through the allowed actions policy." | 2026-09-30 | 2027-03-31 |
| `sha-policy-scope` | The SHA-pinning policy covers GitHub's own actions too, and still lets a reusable workflow be referenced by tag | [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "This includes actions from your organization and actions authored by GitHub." and "Reusable workflows can still be referenced by tag." | 2026-10-05 | 2027-04-05 |
| `sha-policy-nested` | Semgrep, turning on the SHA-pinning policy across its repositories, found it also fails an action that calls an unpinned action, and turned it on one repository at a time | [Semgrep blog, 2026](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) | "The setting requires everything to be pinned all the way down." and "If you break something flip the setting off and re-run the failed job" | 2026-10-05 | 2027-04-05 |
| `injection` | Untrusted input in an inline script goes through an intermediate environment variable, not `${{ }}` in the script | [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) | "Use an intermediate environment variable" | 2026-09-30 | 2027-03-31 |
| `checkout-v7` | `actions/checkout` v7 refuses common "pwn request" checkouts. Workflows pinned to a SHA, minor or patch didn't get the backport, and `allow-unsafe-pr-checkout` opts out | [GitHub changelog, 2026-06-18](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/) | "refuses common pwn request patterns by default" | 2026-09-30 | 2026-12-31 |
| `checkout-sha` | `actions/checkout` v7.0.1 is commit `3d3c42e5aac5ba805825da76410c181273ba90b1` | `git ls-remote --tags https://github.com/actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1 refs/tags/v7.0.1` | 2026-09-30 | 2026-12-31 |
| `persist-creds` | `actions/checkout` keeps the token for later git commands unless `persist-credentials: false` | [checkout README](https://raw.githubusercontent.com/actions/checkout/main/README.md) | "Whether to configure the token or SSH key with the local git config" and "Default: true" | 2026-09-30 | 2026-12-31 |
| `prt-branch` | From 8 December 2025, `pull_request_target` takes its workflow file and checkout commit from the default branch | [GitHub changelog, 2025-11-07](https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/) | "The workflow file and checkout commit will always be taken from the repository’s default branch" | 2026-09-30 | 2027-03-31 |
| `prt-default` | A default rule blocks `pull_request_target` on public repositories with no event policy of their own, enforced from 2 December 2026, moved from 2 November by an editor's note of 2026-10-21 | [GitHub changelog, 2026-09-17](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/) | "On December 2nd, 2026, we'll automatically enforce the default rule" | 2026-10-26 | 2026-12-01 |
| `node20` | Runners default to Node 24 from 16 June 2026, and Node 20 was removed on 23 September 2026 | [GitHub changelog, 2025-09-19](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/) | "Updated the Node20 removal date to September 23rd, 2026." | 2026-09-30 | 2026-12-31 |
| `workflow-permissions` | Settings, Actions, General, Workflow permissions sets the token's default: read and write for everything, or read for contents and packages only. A setting in the same section decides whether the token can create and approve pull requests | [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "just read access for the contents and packages permissions (the restricted setting)" and "Allow GitHub Actions to create and approve pull requests" | 2026-10-05 | 2027-04-05 |
| `token-default` | A new repository in a personal account starts with the token read-only, and unable to create or approve pull requests | [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "By default, when you create a new repository in your personal account, GITHUB_TOKEN only has read access for the contents and packages scopes." and "workflows are not allowed to create or approve pull requests" | 2026-10-05 | 2027-04-05 |
| `fork-approval` | On a public repository, workflows on a first-time contributor's pull request wait for approval by default. A contributor with one merged change no longer waits, and the stricter setting covers every external contributor | [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "By default, all first-time contributors require approval to run workflows." and "a user that has had any commit or pull request merged into the repository will not require approval" and "Require approval for all external contributors" | 2026-10-05 | 2027-04-05 |
| `codeql-default` | Code scanning's default setup is available on every public repository, under Settings, Advanced Security, CodeQL analysis | [Configuring default setup for code scanning](https://docs.github.com/en/code-security/code-scanning/enabling-code-scanning/configuring-default-setup-for-code-scanning) | "Public repositories on GitHub.com" and "click Advanced Security" and "to the right of \"CodeQL analysis\", select Set up" | 2026-10-05 | 2027-04-05 |
| `dependabot-runners` | Dependabot on self-hosted runners sends its jobs to a runner labeled for it, and a job no runner picks up fails after 24 hours | [Configuring Dependabot on self-hosted runners](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-on-self-hosted-runners), [Self-hosted runners reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) | "Assign the default dependabot label or a custom label to each runner you want Dependabot to use." and "If the job remains queued for more than 24 hours, the job will fail." | 2026-10-05 | 2027-04-05 |
| `tj-actions` | In March 2025 an attacker moved every tag of `tj-actions/changed-files` from v1 to v45.0.7 onto a commit that printed secrets into logs (CVE-2025-30066) | [CVE-2025-30066](https://cveawg.mitre.org/api/cve/CVE-2025-30066) | "because they were modified by a threat actor to point at commit 0e58ed8" | 2026-09-30 | 2027-09-30 |
| `starter-pins` | GitHub's starter workflows pin GitHub's own actions by tag, and require every other action to be pinned by SHA | [starter-workflows CONTRIBUTING](https://raw.githubusercontent.com/actions/starter-workflows/main/CONTRIBUTING.md), [python-app.yml](https://raw.githubusercontent.com/actions/starter-workflows/main/ci/python-app.yml) | "We require that Actions outside of the `actions` organization be pinned to a specific SHA." and "uses: actions/checkout@v" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (security hardening, workflow syntax, Actions settings, lockfiles, code scanning, Dependabot on self-hosted runners) | Permissions, pinning, injection, approval, scanning | CC BY 4.0: facts in our own words, with short quotes |
| [GitHub changelog](https://github.blog/changelog/) (2025-08-15, 2025-09-19, 2025-11-07, 2026-06-18, 2026-09-17) | Dated platform changes | © GitHub: short quotes only |
| [actions/checkout README](https://github.com/actions/checkout) | Credentials left in a checkout | MIT: facts with short quotes |
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | How GitHub pins actions in its own templates | MIT: a fact with short quotes |
| [CVE-2025-30066](https://cveawg.mitre.org/api/cve/CVE-2025-30066) | The moved tags of `tj-actions/changed-files` | CVE's terms of use: a fact with a short quote |
| [Semgrep blog, 2026](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) | Turning on the SHA-pinning policy across many repositories | Not stated on the page: short quotes only |
