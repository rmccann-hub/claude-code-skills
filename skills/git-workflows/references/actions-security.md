# Actions security

Read this for writing or reviewing a workflow's permissions and credentials, untrusted input in a
`run:` step, triggers that run with secrets such as `pull_request_target`, or scanning workflows.

It covers what a workflow can be made to do by someone else. Pinning third-party actions, and
moving off Node 20 actions, are `action-pinning`. Triggers, timeouts and required checks are
`ci-workflows`; a secret that already reached a commit is `leaked-data`.

## Rules

1. **Every workflow narrows its token at the top,** with `permissions: contents: read`, and a
   job that needs more asks for it by name (fact `permissions`).
2. **Never put `${{ … }}` of untrusted text inside a `run:` script.** Pass it through an
   environment variable.
3. **Prefer `pull_request` to `pull_request_target`,** and never check out or run a pull
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

### Moving off `pull_request_target`

1. Move what the workflow does to `pull_request`, which has no secrets for forks.
2. Where it must stay, because it labels or comments, make sure it never checks out or runs the
   pull request's code.
3. On a public repository, set an explicit event policy before 2 December 2026, or it stops
   running (fact `prt-default`).

## Mistakes

- **`${{ github.event.pull_request.title }}` inside `run:`**, which is shell injection (fact
  `injection`).
- **Checking out the pull request's head in `pull_request_target`** to build or test it. Fork
  code then runs with your secrets.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`. The checks of
the trigger policy and the token's default need admin access to the settings, or they're
`UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Every workflow narrows its token at the top | `grep -L '^permissions:' .github/workflows/*.y*ml`, then read each top-level block for `write-all` or a write grant | `GAP` per workflow | `contents: read` at the top, and any wider grant on the job that needs it (fact `permissions`) |
| `pull_request_target` or `workflow_run` runs a pull request's code | Read those workflows' checkout and `run:` steps | `BLOCKER` | Move it to `pull_request`, which runs a fork's code without your secrets |
| `pull_request_target` on a public repository with no event policy | Read the workflows, and the repository's Actions policy | `GAP`: it stops from 2 December 2026 (fact `prt-default`) | Move it, or set a policy |
| Untrusted text inside a `run:` script | `grep -nE -e '[$][{][{] *github[.]event' -e '[$][{][{] *github[.]head_ref' .github/workflows/*.y*ml`, then zizmor, whose injection audit follows more contexts | `BLOCKER` where the value is user-written | An environment variable (fact `injection`) |
| The token's default is read and write | Settings, Actions, General, Workflow permissions | `GAP`, whatever the workflows declare: one that forgets its block gets write access | The read-only setting (fact `workflow-permissions`) |

## Why

### Narrowing the token

**The advice.** `permissions: contents: read` at the top of every workflow, wider grants only on
the job that needs them, and a read-only default for the repository.

**Why.** A token that can only read can't be used to write, whatever a compromised step tries.
The repository's default catches the workflow that forgets its block.

**What it costs.** A job that needs to write must say so, and one that forgets fails with a
permissions error the first time it runs.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `permissions` | `permissions:` narrows the job's `GITHUB_TOKEN` | [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) | "modify the default permissions granted to the GITHUB_TOKEN" | 2026-09-30 | 2027-03-31 |
| `injection` | Untrusted input reaches an inline script through an environment variable, not `${{ }}` | [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) | "Use an intermediate environment variable" | 2026-09-30 | 2027-03-31 |
| `checkout-v7` | `actions/checkout` v7 refuses common pwn-request checkouts; SHA, minor and patch pins got no backport; `allow-unsafe-pr-checkout` opts out | [Changelog, 2026-06-18](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/) | "refuses common pwn request patterns by default" | 2026-09-30 | 2026-12-31 |
| `persist-creds` | `actions/checkout` leaves the token in the git config unless `persist-credentials: false` | [checkout README](https://raw.githubusercontent.com/actions/checkout/main/README.md) | "configure the token or SSH key with the local git config" and "Default: true" | 2026-09-30 | 2026-12-31 |
| `prt-branch` | From 2025-12-08, `pull_request_target` takes its workflow file and checkout commit from the default branch | [Changelog, 2025-11-07](https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/) | "always be taken from the repository’s default branch" | 2026-09-30 | 2027-03-31 |
| `prt-default` | A default rule blocks `pull_request_target` on public repositories with no event policy from 2026-12-02, moved from 2026-11-02 by an editor's note of 2026-10-21 | [Changelog, 2026-09-17](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/) | "On December 2nd, 2026, we'll automatically enforce the default rule" | 2026-10-26 | 2026-12-01 |
| `workflow-permissions` | Settings, Actions, General, Workflow permissions sets the token's default, read and write or read-only, and whether it can create and approve pull requests | [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "read access for the contents and packages permissions (the restricted setting)" and "Allow GitHub Actions to create and approve pull requests" | 2026-10-05 | 2027-04-05 |
| `token-default` | A new personal repository's token starts read-only, unable to create or approve pull requests | [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "in your personal account, GITHUB_TOKEN only has read access" and "not allowed to create or approve pull requests" | 2026-10-05 | 2027-04-05 |
| `fork-approval` | Public repositories hold a first-time contributor's workflows for approval; one merged change ends that, and a stricter setting covers every external contributor | [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "all first-time contributors require approval" and "any commit or pull request merged into the repository will not require approval" and "Require approval for all external contributors" | 2026-10-05 | 2027-04-05 |
| `codeql-default` | CodeQL's default setup is on every public repository, under Settings, Advanced Security | [Default setup](https://docs.github.com/en/code-security/code-scanning/enabling-code-scanning/configuring-default-setup-for-code-scanning) | "Public repositories on GitHub.com" and "click Advanced Security" | 2026-10-05 | 2027-04-05 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (security hardening, workflow syntax, Actions settings, code scanning) | Permissions, injection, approval, scanning | CC BY 4.0: facts in our own words, with short quotes |
| [GitHub changelog](https://github.blog/changelog/) (2025-11-07, 2026-06-18, 2026-09-17) | Dated platform changes | © GitHub: short quotes only |
| [actions/checkout README](https://github.com/actions/checkout) | Credentials left in a checkout | MIT: facts with short quotes |
