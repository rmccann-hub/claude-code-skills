# Action pinning

Read this for choosing, pinning and updating a workflow's third-party actions: SHA pins and how
to find one, workflow dependency lockfiles, Dependabot for actions and its cooldown, a policy that
requires pins, or moving off Node 20 actions.

It covers which code a workflow runs when it calls an action. A workflow's permissions,
untrusted input and `pull_request_target` are `actions-security`; triggers, timeouts and
required checks are `ci-workflows`.

## Rules

1. **Pin each action to a full commit SHA, with its version in a comment,** and keep the pins
   moving with Dependabot.
2. **Read what an action runs before adopting it.** It runs with the job's token and secrets.

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
- **Read zizmor's `dependabot-cooldown` finding against the platform's default.** Dependabot
  already waits three days after a release before a version update, with no `cooldown:` set,
  and security updates don't wait (fact `dependabot-cooldown`). zizmor flags an entry with no
  `cooldown:`, or one under its own seven days (fact `zizmor-cooldown`). So the finding asks for
  four more days, not a missing control. Either set `default-days: 7` and record why, or keep
  the default and ignore the finding under `rules.dependabot-cooldown.ignore` in `zizmor.yml`,
  with that reason. Never add a `cooldown:` of about three days: it repeats the default.
- **Leave "Dependabot on self-hosted runners" off** unless a runner labeled for Dependabot
  exists. Its jobs wait for one, and fail after 24 hours (fact `dependabot-runners`), so no
  update arrives.
- **Enforce pinning by policy** where you can (fact `sha-policy`), so an unpinned action fails
  instead of relying on review. The policy covers GitHub's own actions too, and lets a reusable
  workflow keep a tag (fact `sha-policy-scope`). It also fails an action that calls an unpinned
  one (fact `sha-policy-nested`), so read each action's `action.yml` for its own `uses:` lines
  before turning it on, and watch the next runs.

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

## Mistakes

- **Suggesting `actions/checkout@v4` or other old majors from training data.** Node 20 is gone
  from the runners (fact `node20`). Take the version and SHA from the action's release page, or
  from fact `checkout-sha`.
- **Assuming a SHA-pinned action gets security backports.** It doesn't (fact `checkout-v7`).
- **Taking a SHA from a fork of the action,** or from a search result. Take it from the action's
  own repository.
- **Turning on the SHA-pinning policy without reading each action's own `uses:` lines.** An
  action that calls an unpinned one fails the run (fact `sha-policy-nested`).

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Actions pinned by tag or branch | `grep -n 'uses:' .github/workflows/*.y*ml` | `GAP` where the workflow reads secrets, writes or publishes | A full SHA with the version in a comment, and Dependabot (fact `sha-pin`) |
| A `cooldown:` repeats the platform's three days | `grep -n -A3 'cooldown:' .github/dependabot.y*ml` | `OVER`, as project-bootstrap-and-audit rates it (dimension 8). An entry with none is no finding, whatever zizmor says | Remove it, or set a longer window and record why (fact `dependabot-cooldown`) |
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

### Dependabot's cooldown

**The advice.** Leave the platform's three-day wait alone, or lengthen it on purpose; never
restate it.

**Why.** A new release is where a compromised version lands before it's caught, and waiting
lets the signal surface (fact `dependabot-cooldown`). A setting that copies the default drifts
from it when GitHub moves it. zizmor asks for seven days (fact `zizmor-cooldown`), a choice
project-bootstrap-and-audit accepts when its reason is recorded. **Cost:** updates arrive four
days later.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sha-pin` | Without a lockfile, GitHub advises pinning each action to a full commit SHA from its own repository | [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) | "Pin references to actions to a commit SHA" | 2026-10-12 | 2027-04-12 |
| `actions-lockfile` | Lockfiles are in public preview: `.github/workflows/actions.lock`, made by `gh actions-lock`, records every action's commit, nested ones included. GitHub calls it stronger than SHA pins | [Lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles) | "Workflow dependency lockfiles are in public preview" | 2026-10-12 | 2027-01-12 |
| `sha-policy` | Repository and organization policy can require SHA-pinned actions | [Changelog, 2025-08-15](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/) | "enforce the use of SHA pinning" | 2026-09-30 | 2027-03-31 |
| `sha-policy-scope` | The SHA-pinning policy covers GitHub's own actions, and lets a reusable workflow keep a tag | [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | "This includes actions from your organization and actions authored by GitHub" and "Reusable workflows can still be referenced by tag" | 2026-10-05 | 2027-04-05 |
| `sha-policy-nested` | Semgrep found the policy also fails an action that calls an unpinned one, and turned it on a repository at a time | [Semgrep, 2026](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) | "pinned all the way down" and "flip the setting off and re-run the failed job" | 2026-10-05 | 2027-04-05 |
| `checkout-sha` | `actions/checkout` v7.0.1 is commit `3d3c42e5aac5ba805825da76410c181273ba90b1` | `git ls-remote --tags https://github.com/actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1 refs/tags/v7.0.1` | 2026-09-30 | 2026-12-31 |
| `node20` | Runners default to Node 24 from 2026-06-16, and Node 20 was removed on 2026-09-23 | [Changelog, 2025-09-19](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/) | "Updated the Node20 removal date to September 23rd, 2026." | 2026-09-30 | 2026-12-31 |
| `dependabot-cooldown` | Dependabot waits three days after a release before a version update, with no configuration; security updates don't wait. Since 2026-07-14 | [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference), [Changelog, 2026-07-14](https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/) | "If not specified, Dependabot applies a default cooldown of 3 days." and "Security updates still open immediately" | 2026-10-27 | 2027-04-27 |
| `zizmor-cooldown` | zizmor's `dependabot-cooldown` audit flags a missing cooldown or one under seven days, configurable; a finding can be ignored in `zizmor.yml` | [zizmor audits](https://docs.zizmor.sh/audits/), [zizmor configuration](https://docs.zizmor.sh/configuration/) | "Detects missing or insufficient" and "recommends a cooldown of seven days by default" and "Ignoring specific findings via rules.<id>.ignore" | 2026-10-27 | 2027-04-27 |
| `dependabot-runners` | Dependabot on self-hosted runners needs a runner labeled for it, and a job no runner takes fails after 24 hours | [Dependabot runners](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-on-self-hosted-runners), [Self-hosted runners](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) | "Assign the default dependabot label or a custom label" and "queued for more than 24 hours, the job will fail" | 2026-10-05 | 2027-04-05 |
| `tj-actions` | In March 2025 every tag of `tj-actions/changed-files`, v1 to v45.0.7, was moved to a commit that printed secrets (CVE-2025-30066) | [CVE-2025-30066](https://cveawg.mitre.org/api/cve/CVE-2025-30066) | "modified by a threat actor to point at commit 0e58ed8" | 2026-09-30 | 2027-09-30 |
| `starter-pins` | GitHub's starter workflows pin GitHub's own actions by tag, and require a SHA for every other | [CONTRIBUTING](https://raw.githubusercontent.com/actions/starter-workflows/main/CONTRIBUTING.md), [python-app.yml](https://raw.githubusercontent.com/actions/starter-workflows/main/ci/python-app.yml) | "outside of the `actions` organization be pinned to a specific SHA" and "uses: actions/checkout@v" | 2026-09-30 | 2027-03-31 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) (security hardening, Actions settings, lockfiles, Dependabot on self-hosted runners, Dependabot options) | Pinning, lockfiles, the pinning policy, Dependabot | CC BY 4.0: facts in our own words, with short quotes |
| [GitHub changelog](https://github.blog/changelog/) (2025-08-15, 2025-09-19, 2026-07-14) | Dated platform changes | © GitHub: short quotes only |
| [actions/checkout](https://github.com/actions/checkout) | A release tag's commit | MIT: a fact with its tag line |
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | How GitHub pins actions in its own templates | MIT: a fact with short quotes |
| [CVE-2025-30066](https://cveawg.mitre.org/api/cve/CVE-2025-30066) | The moved tags of `tj-actions/changed-files` | CVE's terms of use: a fact with a short quote |
| [zizmor's documentation](https://docs.zizmor.sh/) | Its Dependabot cooldown audit | MIT: facts with short quotes |
| [Semgrep blog, 2026](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) | Turning on the SHA-pinning policy across many repositories | Not stated on the page: short quotes only |
