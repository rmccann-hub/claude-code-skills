# Deploying from CI

Read this for setting up a GitHub environment and its protection rules, deciding who can deploy,
keeping deploy credentials in an environment or moving a deploy off long-lived cloud keys to
OIDC, promoting one build through staging and production, deploying on a tag or on merge,
keeping two deploys from running at once, a smoke test after a deploy, or rolling one back.

The checks that run before a deploy are `ci-workflows`, and how long they take and where each
suite runs `ci-speed`. A workflow's token, untrusted input and `pull_request_target` are
`actions-security`; pinning the deploy's actions is `action-pinning`; cutting the tag or release
a deploy starts from is `releases-and-versions`. project-bootstrap-and-audit rules where secrets
live (dimension 7) and what's checked before a production deploy (*The release and deploy
currency gate*).

## Rules

1. **Every deploy job names its environment, and the environment holds the gate:** the refs
   that may deploy, the reviewers, the secrets, and the cloud's trust.
2. **Name the refs that may deploy:** "Selected branches and tags", with the default branch or
   a release tag pattern. Not "No restriction", and not "Protected branches only" (fact
   `cicd-deploy-refs`).
3. **Production waits for a person other than the one who started it,** where the plan offers
   reviewers: a named reviewer, self-review prevented, admin bypass off (fact `cicd-reviewers`).
4. **No long-lived cloud key.** Sign in with OIDC, the `id-token` permission granted on the
   deploy job alone, trusted on the environment's exact subject (facts `cicd-oidc`,
   `cicd-oidc-sub`).
5. **Build once, and deploy those bytes everywhere,** named by digest. Each environment adds
   only its configuration (fact `cicd-12factor`).
6. **One deploy at a time per environment, never canceled partway,** in one concurrency group
   that every workflow deploying there shares (fact `cicd-concurrency-env`).
7. **A deploy isn't done until a smoke test passes against what's live,** checking the version.
8. **Rollback is a deploy of the previous artifact, by the same workflow, and it's been run.**

### Who can deploy

- **Anyone with write access can edit a workflow,** so a check written in one gates nothing.
  An environment's rules are settings only admins change (fact `cicd-env-autocreate`).
- **The plan decides the gate.** On Free, Pro and Team, a private repository gets no required
  reviewers (fact `cicd-reviewers`). There the ref rule and the ruleset on that branch or tag
  are the gate; with no environment, trust the OIDC subject's branch (fact `cicd-oidc-sub`).
- **A pull request's run matches its merge ref,** not its branch (fact `cicd-deploy-refs`), so
  a rule naming `main` keeps pull requests out.

### Triggers, artifacts and queues

- **On merge,** every commit on the default branch ships, so the full suite runs before merge
  (`ci-speed`). **On tag,** the rule names a pattern such as `v*`, a ruleset protects those
  tags, and they aren't pushed with `GITHUB_TOKEN` (fact `token-no-trigger`).
- **Either way, a `workflow_dispatch` input takes the digest,** so a redeploy or a rollback
  needs no new commit.
- **Keep what you'd roll back to in a registry or a release,** not as an Actions artifact
  (fact `cicd-retention`).
- **A newer pending deploy replaces an older pending one** unless the group sets `queue: max`
  (fact `cicd-queue`). That suits the default branch, where the newest commit wins.
- **A schema change ships in steps the previous release can run against,** expand, migrate,
  contract (fact `cicd-parallel-change`), or the rollback fails when it's needed.
- **The smoke test reads the version the service reports,** such as a commit SHA, and a
  failure fails the job (fact `cicd-sre`).

Example: the gate, the queue and the credential on one job. Pin the action as `action-pinning`
sets out.

<!-- content: allowed, id-token is a permission's name, not a credential -->
```yaml
on:
  workflow_dispatch:
    inputs:
      digest:
        description: The digest to deploy
        required: true
permissions:
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment:
      name: production
      url: https://app.example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@<full commit SHA>
        with:
          persist-credentials: false
      - name: Deploy the digest, then smoke-test it
        env:
          DIGEST: ${{ inputs.digest }}
        run: |
          ./deploy/sign-in.sh
          ./deploy/release.sh "$DIGEST"
          ./deploy/smoke.sh https://app.example.com "$DIGEST"
```

## Mistakes

- **A typo in `environment:`.** It creates a new environment with no rules and no secrets (fact
  `cicd-env-autocreate`). Environment secrets and an OIDC subject naming the environment make
  the typo fail; repository secrets and a wildcard subject let it deploy ungated.
- **A trust policy matching `repo:OWNER/REPO:*`,** which gives any branch production's role.
- **The `id-token` permission at the top of the workflow,** so every job can mint a token (fact
  `cicd-oidc-sub`).
- **Renaming or moving the repository** without updating the trust policy. The subject changes,
  and the next deploy can't sign in (fact `cicd-oidc-immutable`).
- **Rebuilding for production** after testing staging's build. Dependencies and base images
  resolve again, and production runs bytes nobody tested.
- **`cancel-in-progress: true` on a deploy,** as GitHub's concurrency example shows for staging.
  It can stop a deploy halfway, with hosts on both versions.
- **Rolling back by re-running an old run.** It works for 30 days, with the first actor's
  privileges, while its artifact lasts (facts `cicd-rerun`, `cicd-retention`).
- **A smoke test that checks for HTTP 200.** The old version answers 200 too.

## Audit

Severity uses the standard's status words. Read access shows an environment, with
`gh api repos/OWNER/REPO/environments/<name>`; admin bypass and the cloud's trust policy need
more, or they're `UNVERIFIABLE-HERE`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A deploy job names no environment | Each deploy job's `environment:` | `GAP`; `BLOCKER` with production credentials in repository secrets | An environment per target, its secrets moved in |
| Any ref can deploy | `.deployment_branch_policy`: `null`, or `protected_branches: true` | `GAP` | Selected branches and tags (fact `cicd-deploy-refs`) |
| Production waits for nobody, or for whoever started it | `.protection_rules`, for `required_reviewers` and `prevent_self_review` | `GAP`; `N/A` where the plan lacks reviewers (fact `cicd-reviewers`) | A named reviewer, self-review prevented, bypass off |
| A long-lived cloud key | `gh secret list`, and with `--env <name>` | `GAP` where the provider takes OIDC | OIDC, then revoke the key (fact `cicd-oidc`) |
| The OIDC trust is wider than the environment | The role's subject condition | `BLOCKER` where a pull request's run can match | The environment's exact subject (fact `cicd-oidc-sub`) |
| Every job gets the `id-token` permission | The top-level `permissions:` | `GAP` | Grant it on the deploy job (fact `cicd-oidc-sub`) |
| Production rebuilds what staging tested | A build in the production job, or a deploy by tag | `GAP` | Deploy the tested digest |
| Deploys to one environment can overlap | Every workflow naming it, for one `concurrency.group` | `GAP`; `DRIFT` with `cancel-in-progress: true` | One group, never canceled (fact `cicd-concurrency-env`) |
| No smoke test, or no rollback ever run | The deploy job's last steps; the deploy history | `GAP` | A smoke test reading the version; a rollback drill on staging |

## Why

### The environment as the gate

- **The reason:** any writer can edit a workflow in a branch; only admins change an
  environment's rules, which run before its secrets are released (fact `cicd-env-secrets`).
- **What others do:** some teams gate in a separate deploy tool, and the workflow hands it the
  digest. That works too; record which holds the gate.
- **What it costs:** settings outside the repository, and in private repositories a plan that
  offers them.

### OIDC instead of keys

- **The reason:** a stored key works from anywhere until it's rotated. An OIDC token lasts one
  job (fact `cicd-oidc`), and a subject naming the environment makes the cloud enforce the
  environment's rules too (fact `cicd-oidc-sub`).
- **What it costs:** a trust policy at the provider, and a subject that changes when the
  repository is renamed or moved (fact `cicd-oidc-immutable`).
- **When to choose differently:** a target that can't take OIDC. Keep its key in the
  environment, scoped to deploying, and record when it was last rotated.

### Build once

- **The reason:** a rebuild resolves dependencies and base images again, so staging's tests
  speak for bytes production never runs.
- **What others do:** Twelve-Factor separates build from run (fact `cicd-12factor`).
- **What it costs:** a registry to keep artifacts, and configuration read at run time.
- **When to choose differently:** a target that must be built per environment. Pin every input,
  and test the build it ships.

### Queued, smoke-tested, reversible

- **The reason:** two deploys at once leave hosts on mixed versions, and a canceled one leaves
  them half done. A smoke test is cheap, and catches the plainly broken release. A rollback
  never run fails when needed, on a schema the old release can't read or an expired artifact.
- **What others do:** Google rolls back a change that fails validation (fact `cicd-sre`).
- **What it costs:** a deploy that waits, a version endpoint, and a drill on staging after each
  change to the deploy.
- **When to choose differently:** a host that keeps every deploy and rolls back in its own
  interface needs no rollback workflow, but still the drill.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cicd-env-secrets` | Environment secrets wait for the rules to pass | [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | "a job cannot access environment secrets until one of the required reviewers approves it" | 2026-11-11 | 2027-02-11 |
| `cicd-reviewers` | One approval suffices; self-review can be prevented; admins bypass by default; on Free, Pro and Team, public repositories only | [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | "Only one of the required reviewers needs to approve the job for it to proceed." and "users who initiate a deployment cannot approve the deployment job" and "By default, administrators can bypass the protection rules" and "required reviewers are only available for public repositories" | 2026-11-11 | 2027-02-11 |
| `cicd-deploy-refs` | "Protected branches only" lets every branch deploy where none is protected; a pull request's run matches its merge ref | [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | "then all branches can deploy" and "would also allow workflows triggered by pull_request events to deploy" | 2026-11-11 | 2027-02-11 |
| `cicd-env-autocreate` | A workflow naming a missing environment creates it bare; only admins configure one | [Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) | "the newly created environment will not have any protection rules or secrets configured" and "only repository admins can configure the environment" | 2026-11-11 | 2027-02-11 |
| `cicd-concurrency-env` | A concurrency group isn't tied to an environment | [Deploying with GitHub Actions](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments) | "Note that concurrency and environment are not connected." | 2026-11-11 | 2027-02-11 |
| `cicd-queue` | A new pending run replaces the pending one; `queue: max` holds up to 100 | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | "any existing pending job or workflow in the same concurrency group will be canceled" and "Up to 100 jobs or workflow runs can be pending" | 2026-11-11 | 2027-02-11 |
| `cicd-oidc` | An OIDC cloud token lasts one job | [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) | "only valid for a single job, and then automatically expires" | 2026-11-11 | 2027-02-11 |
| `cicd-oidc-sub` | OIDC needs the `id-token` permission, set to `write`; a trust needs a condition; the subject names the environment, or else the branch | [OIDC reference](https://docs.github.com/en/actions/reference/security/oidc) | "Without id-token... the OIDC JWT ID token cannot be requested." and "define at least one condition" and "The subject claim includes the environment name when the job references an environment." | 2026-11-11 | 2027-02-11 |
| `cicd-oidc-immutable` | A repository made, renamed or moved after 2026-07-15 gets a subject with IDs | [OIDC reference](https://docs.github.com/en/actions/reference/security/oidc) | "Repository renames and transfers after July 15, 2026 also move to the immutable subject format." | 2026-11-11 | 2027-02-11 |
| `cicd-rerun` | Re-runs last 30 days, with the first actor's privileges | [Re-running workflows](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) | "up to 30 days after its initial run" and "Re-runs use the privileges of the actor who initially triggered the workflow" | 2026-11-11 | 2027-02-11 |
| `cicd-retention` | Artifacts are kept 90 days by default | [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "retained for 90 days before they are automatically deleted" | 2026-11-11 | 2027-02-11 |
| `cicd-12factor` | Twelve-Factor separates build from run | [Build, release, run](https://12factor.net/build-release-run) | "Strictly separate build and run stages" | 2026-11-11 | 2027-05-11 |
| `cicd-sre` | Google: smoke tests every release; a change failing validation rolls back | [Testing](https://sre.google/sre-book/testing-reliability/), [Launches](https://sre.google/sre-book/reliable-product-launches/) | "create a series of smoke tests to run for every release" and "it's automatically rolled back" | 2026-11-11 | 2027-05-11 |
| `cicd-parallel-change` | Expand and contract makes a breaking change safely | [ParallelChange](https://martinfowler.com/bliki/ParallelChange.html) | "a pattern to implement backward-incompatible changes to an interface in a safe manner" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (environments, deployments, OIDC, concurrency, re-runs) | Every platform fact | CC BY 4.0: facts in our own words, short quotes |
| [The Twelve-Factor App](https://12factor.net/build-release-run) | Build once | CC BY 4.0 in its open-source repository: a short quote |
| [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) | Smoke tests, rollback | CC BY-NC-ND 4.0: quoted, never adapted |
| [Martin Fowler, ParallelChange](https://martinfowler.com/bliki/ParallelChange.html) | Expand and contract | © Martin Fowler: quoted, never adapted |
