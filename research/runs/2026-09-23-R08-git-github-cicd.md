# Verification: R08 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| Node 20 is removed from GitHub-hosted runners on 23 September 2026; runners have used Node 24 by default since 16 June 2026 | verified. This repository's CI passed on `main` after the removal | [GitHub changelog](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/), editor's note of 2026-08-25 |
| A default rule disabling `pull_request_target` on public repositories runs in evaluate mode, then is enforced on 2 November 2026 | verified. This repository doesn't use `pull_request_target` | [GitHub changelog, 2026-09-17](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/) |
| Push rulesets apply only to private and internal repositories | verified | [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): "block pushes to a private or internal repository" |
| The standard is wrong that push rulesets need an organisation plan | **overstated**: Team and Enterprise Cloud, the two plans the report cites, are both organisation plans. The plan itself is unverifiable here: its availability note isn't in the fetched page text. The standard can add that push rulesets don't apply to public repositories | About rulesets, free and Enterprise Cloud editions |
| actions/checkout v7.0.1, setup-node v7.0.0 and setup-go v7.0.0 SHAs | verified with `git ls-remote` on 2026-09-23 (see `2026-09-23-C-platform.md`); in use here | `.github/workflows/ci.yml` |
| astral-sh/setup-uv: "not verified" in the report | superseded: v10.2.0 (`c18668ad…`) was verified on 2026-09-23 and is in use here | `2026-09-23-C-platform.md` |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R08 · FORM: research-result v1
Save as: R08-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R08 — Git, GitHub, code review, and CI/CD (researched 23 September 2026)

## 1. Summary

The biggest change since the standard's facts were written is that GitHub has spent June to September 2026 closing off `pull_request_target`: checkout v7 refuses fork checkouts, and public repositories get a default rule that disables the trigger, enforced from 2 November 2026. Two of the standard's dated facts are also wrong or incomplete (push rulesets, push protection default).

**TL;DR**

- Git 2.55.0 (29 June 2026) is current; Git 3.0 will default new repositories to SHA-256, reftable and `main`, but the Git project itself says "There is no planned release date for this breaking version yet" — Phoronix (11 September 2026) says 3.0 is "potentially coming around the end of 2026", and LWN (18 September 2026) says "If the 3.0 release does not happen in 2026, it seems certain to show up shortly thereafter" (both secondary).
- GitHub Actions security moved fast in 2026: `actions/checkout` v7 (18 June 2026) blocks common "pwn request" checkouts, the Node 20 runtime is removed from runners on 23 September 2026 (today), and a default rule disabling `pull_request_target` on public repositories is enforced from 2 November 2026.
- The standard is wrong on push rulesets (they target private/internal repositories, and GitHub's own pages disagree on whether Team or Enterprise Cloud is required) and imprecise on push protection (on by default for *users* pushing to public repos; on by default at *repository* level only for public repos created by personal accounts after 11 March 2024).

Further points a professional must know today:

- The December 2025 `pull_request_target` change is confirmed: from 8 December 2025 the workflow file and checkout commit always come from the default branch.
- Workflows pinned to a commit SHA did **not** receive the checkout v7 backport (20 July 2026); they must be bumped deliberately (Dependabot or manual).
- SHA pinning can now be enforced by policy (GitHub changelog, 15 August 2025); the policy treats local composite actions as unpinned (community report, secondary).
- Current majors (verified SHAs): checkout v7.0.1, setup-python v7.0.0, setup-node v7.0.0, setup-go v7.0.0. upload-artifact is v7.0.1 and download-artifact v8.x; their full SHAs were not found.
- Merge queue is only available on organisation-owned public repositories (or GHEC private); it is not available on repositories owned by a personal account.
- Immutable releases are generally available (28 October 2025) and lock tags and assets after publication.
- DORA's trunk-based development guidance still stands: three or fewer active branches, merge to trunk at least daily, no code freezes.
- zizmor 1.30.x, actionlint 1.7.12 and Harden-Runner 2.21.1 are the current releases of the three workflow-security tools.
- Git 2.54 added config-based hooks and 2.55 runs compatible configured hooks in parallel; pre-commit already accommodates Git 2.54+ hooks, and Dependabot can now update `.pre-commit-config.yaml` (10 March 2026).
- prek reached full language parity with pre-commit in 0.4.5 (15 June 2026); latest is 0.5.1 (1 September 2026).

## 2. Corrections

| Belief | Verdict | Correct fact | Source |
|---|---|---|---|
| Git 3.0 is planned to default to SHA-256 and "main"; Git 2.5x is current. | **Confirmed, with additions.** | Also defaults to reftable and requires Rust to build. Current stable is 2.55.0 (29 June 2026); 2.56-rc0 was published 11 September 2026. The Git project gives no release date for 3.0. | https://git-scm.com/docs/BreakingChanges — "There is no planned release date for this breaking version yet." |
| (the standard, 2026-09) Rulesets free for public repos, paid (Pro enough) for private personal repos. | **Confirmed.** | Exactly as stated for branch and tag rulesets. Classic branch protection availability was not re-verified this run. | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets — "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." |
| (the standard, 2026-09) Push rulesets need an organisation plan. | **Wrong / imprecise — the standard should be corrected.** | Push rulesets apply only to private and internal repositories (and their forks), so they are irrelevant to a public repository. GitHub's pages disagree on the plan: the free-pro-team pages say Team; the Enterprise Cloud pages say Enterprise Cloud. Record as "contested". | FPT docs: "Push rulesets are available for the GitHub Team plan in internal and private repositories, and forks of repositories that have push rulesets enabled." GHEC docs (https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): "Push rulesets are available for the GitHub Enterprise Cloud plan in internal and private repositories…" |
| (the standard, 2026-09) Secret scanning and push protection are free and on by default for public repositories. | **Partly wrong — settled below.** | Two different features share the name. *Push protection for users* is on by default and blocks your pushes to any public repo. *Repository push protection* is "disabled by default" in general, but was switched on by default for **new public repositories owned by personal accounts** from 11 March 2024; older repos and org-owned repos are not affected. | See Findings §3 for all three quotes. |
| GitHub changed `pull_request_target` in late 2025 so workflows run from the default branch. | **Confirmed, and now out of date.** | Announced 7 November 2025, effective 8 December 2025. Since then: checkout v7 (18 June 2026) refuses fork PR checkouts; backport to older majors 20 July 2026; a default rule disabling `pull_request_target` on public repos is enforced 2 November 2026. | https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/ — "These changes will take effect on 12/8/2025." |
| zizmor = static security analyzer; actionlint = correctness; Harden-Runner = runner monitoring. | **Confirmed.** | Harden-Runner now describes itself as "an EDR for GitHub Actions runners" monitoring egress, file integrity and processes. | https://github.com/step-security/harden-runner |
| pre-commit 4.x is standard; prek is a faster compatible implementation; lefthook an alternative. | **Confirmed, with an update.** | prek now claims "full feature parity with pre-commit" (0.4.5, 15 June 2026). pre-commit is on 4.6.2 (released 10 August 2026, per PyPI). lefthook's current version was not found. | https://prek.j178.dev/0.5.2/changelog/ |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Git 3.0 release date | None set by Git project | https://git-scm.com/docs/BreakingChanges | "There is no planned release date for this breaking version yet." | page last updated in 2.55.0 (2026-06-29); read 2026-09-23 |
| 2 | Git 3.0 default hash | SHA-256 | https://git-scm.com/docs/BreakingChanges | "The default hash function for new repositories will be changed from \"sha1\" to \"sha256\"." | read 2026-09-23 |
| 3 | Git current stable | 2.55.0, 29 June 2026 | https://git-scm.com/docs/BreakingChanges (version list) | "2.55.0 … 2026-06-29" | read 2026-09-23 |
| 4 | Git 2.56-rc0 | 11 September 2026 (secondary) | https://dev.to/techaiwire/git-30-will-default-to-sha-256-and-require-rust-3h8n | "Git 2.56-rc0 was published on September 11, 2026" | 2026-09 |
| 5 | `pull_request_target` source ref | Default branch, from 8 Dec 2025 | https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/ | "The workflow file and checkout commit will always be taken from the repository's default branch, regardless of the pull request's base branch." | 2025-11-07 |
| 6 | checkout v7 GA | 18 June 2026 | https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/ | "Starting today, actions/checkout v7 is generally available and refuses common pwn request patterns by default." | 2026-06-18 |
| 7 | checkout backport date | 20 July 2026 (moved from 16 July) | same | "Enforcement for backported versions of actions/checkout has been moved from July 16, 2026 to Monday, July 20, 2026." | editor's note 2026-07-15 |
| 8 | SHA-pinned workflows and backport | Not covered | same | "Workflows pinned to a specific SHA, minor, or patch version aren't affected by the backport" | 2026-06-18 |
| 9 | Opt-out input | `allow-unsafe-pr-checkout` | same | "you can opt out of this protection by adding the allow-unsafe-pr-checkout input on the actions/checkout step" | 2026-06-18 |
| 10 | Default `pull_request_target` block | Enforced 2 Nov 2026, public repos | https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/ | "For public repositories that do not already have an applicable event policy, GitHub is introducing a default rule that disables pull_request_target." | 2026-09-17 |
| 11 | Enforcement date | 2 November 2026 | same | "On November 2, 2026, we'll automatically enforce the default rule for affected repositories that were using the default pull_request_target policy before general availability." | 2026-09-17 |
| 12 | SHA pinning policy | Available | https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/ | "Administrators can now enforce the use of SHA pinning through the allowed actions policy." | 2025-08-15 |
| 13 | Node 24 default on runners | 16 June 2026 | https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | "Beginning on June 16th, 2026, runners will begin using Node24 by default." | updated 2026-08-25 |
| 14 | Node 20 removal | 23 September 2026 | same | "Editor's note (August 25, 2026): Updated the Node20 removal date to September 23rd, 2026." | 2026-08-25 |
| 15 | Rulesets availability | Free public; Pro/Team/GHEC private | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets | "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." | read 2026-09-23 |
| 16 | Push protection for users | On by default | https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/push-protection-for-users | "Push protection for users is on by default for public repositories" | read 2026-09-23 |
| 17 | Repository push protection (general) | Off by default | https://docs.github.com/en/code-security/concepts/secret-security/push-protection | "Is disabled by default, and can be enabled by a repository administrator, organization owner, security manager, or enterprise owner" | read 2026-09-23 |
| 18 | Repository push protection (new personal public repos) | On by default since 11 Mar 2024 | https://github.blog/changelog/2024-03-11-secret-scanning-and-push-protection-are-enabled-by-default-on-new-public-repositories/ | "All new public repositories owned by personal accounts will now have secret scanning and push protection enabled by default." | 2024-03-11 |
| 19 | Merge queue availability | Org-owned public, or GHEC private | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue | "Pull request merge queues are available in any public repository owned by an organization, or in private repositories owned by organizations using GitHub Enterprise Cloud." | read 2026-09-23 |
| 20 | Merge queue CI trigger | `merge_group` required | https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue | "You must use the merge_group event to trigger your GitHub Actions workflow when a pull request is added to a merge queue." | read 2026-09-23 |
| 21 | Immutable releases | GA 28 Oct 2025 | https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/ | "Tag protection: Tags for new immutable releases are protected and can't be deleted or moved." | 2025-10-28 |
| 22 | DORA branch guidance | ≤3 active branches, daily merges | https://dora.dev/capabilities/trunk-based-development/ | "Have three or fewer active branches in the application's code repository." | read 2026-09-23 |
| 23 | Dependabot + pre-commit | Supported | https://github.blog/changelog/2026-03-10-dependabot-now-supports-pre-commit-hooks/ | "Dependabot will parse your .pre-commit-config.yaml, check each hook's repository for new tags or releases, and open pull requests to update the rev field." | 2026-03-10 |
| 24 | Git 2.55 parallel hooks | Yes | https://github.blog/open-source/git/highlights-from-git-2-55/ | "Git 2.55 extends that work by allowing compatible configured hooks to run in parallel." | 2026-06-29 |
| 25 | prek parity | Full parity at 0.4.5 | https://prek.j178.dev/0.5.2/changelog/ | "This is full feature parity with pre-commit." | 2026-06-15 |
| 26 | Non-zipped artifacts | upload-artifact v7 `archive: false`; download-artifact v8 needed | https://github.blog/changelog/2026-02-26-github-actions-now-supports-uploading-and-downloading-non-zipped-artifacts/ | "You will also need to update to v8 of actions/download-artifact if you use that action." | 2026-02-26 |

## 4. Findings

### 4.1 Branching and merging

- **Trunk-based development is the evidence-backed default.** DORA defines it as each developer merging small batches "into trunk at least once (and potentially several times) a day", and reports from its 2016 and 2017 data that teams perform better when they "Have three or fewer active branches", "Merge branches to trunk at least once a day" and "Don't have code freezes and don't have integration phases" (https://dora.dev/capabilities/trunk-based-development/, read 2026-09-23). DORA also names "An overly heavy code-review process" as a pitfall.
- **Recommendation for a solo maintainer:** GitHub Flow is trunk-based development with short-lived PR branches; use it. PRs give you CI on every change and a record, even with one maintainer. Git Flow's long-lived `develop`/`release` branches contradict the DORA findings above; reserve it for projects that must maintain several released versions in parallel. A current primary statement from Git Flow's author and trunkbaseddevelopment.com was not re-fetched this run (see §9).
- **Merge strategy:** for a solo or small repository, squash-merge into a linear history keeps one commit per reviewed change; this is a recommendation, not a sourced fact.
- **Merge queue:** not available to personal-account repositories (fact 19). If rmccann-hub is a personal account, a merge queue is not an option; if it is an organisation, it is free for public repos. Any workflow providing a required check must add the `merge_group` trigger (fact 20).

### 4.2 Commits and pull requests

Conventional Commits, SubmittingPatches, PR-size research, Conventional Comments, SSH signing, gitsign and vigilant mode were **not covered** in this run (search budget exhausted; see §9). One incidental primary observation: GitHub's own release pages for actions/checkout show "This commit was created on GitHub.com and signed with GitHub's verified signature" alongside "Learn about vigilant mode" (https://github.com/actions/checkout/releases, read 2026-09-23), confirming vigilant mode remains a current GitHub feature.

### 4.3 GitHub settings for a public repository

| Setting | Free on personal account? | On by default? | Menu path | Source |
|---|---|---|---|---|
| Branch/tag rulesets (required checks, block force push, restrict deletions, required reviews) | Yes (public) | No | Settings → Code and automation → Rules → Rulesets → New ruleset | about-rulesets and creating-rulesets docs (fact 15); menu path quoted: "In the left sidebar, under \"Code and automation,\" click Rulesets" |
| Push rulesets | Not applicable to public repos | — | — | fact/correction above |
| Push protection for users | Yes | **Yes** | Profile → Settings → Security → Code security → "Push protection for yourself" | fact 16 |
| Repository secret scanning + push protection | Yes (public) | Only for public repos created by personal accounts on/after 11 Mar 2024 | Repo Settings → "Security and quality" → Advanced Security → Secret Protection → Enable | facts 17–18; enabling doc: "In the \"Security and quality\" section of the sidebar, click Advanced Security." |
| Merge queue | **No** (org-owned only) | No | — | fact 19 |
| Immutable releases | Yes | No (opt-in at repo or org level) | Repository settings | fact 21: "You can enable immutable releases at the repository or organization level in your settings" |
| Private vulnerability reporting, Dependabot alerts/security updates, code scanning default setup, CODEOWNERS | not verified this run | not verified | not verified | see §9 |

**Push protection, settled.** There is no real contradiction once the two features are separated: (1) *push protection for users* is account-level, on by default, and applies whenever you push to any public repository; (2) *repository push protection* is off by default in general, but GitHub turned it on at creation for new personal-account public repositories from 11 March 2024 ("Existing public repositories are not affected, nor are new public repositories that belong to an organization"). The standard should say: "verify the repository toggle; do not assume it." The 2024 GitHub blog phrasing "we've enabled secret scanning push protection by default for all pushes to public repositories" (https://github.blog/news-insights/product-news/keeping-secrets-out-of-public-repositories/) refers to the user-level feature and is the source of the apparent disagreement.

### 4.4 GitHub Actions security hardening

- **`pull_request_target` timeline.** (a) 8 Dec 2025: always runs the default branch's workflow; `GITHUB_REF` resolves to the default branch (fact 5). (b) 18 Jun 2026: checkout v7 refuses fork PR checkouts in `pull_request_target` and `workflow_run` (the latter "only when workflow_run.event is a pull_request* event") (fact 6). (c) 20 Jul 2026: backport to supported majors except v1; floating-tag users picked it up, SHA-pinned users did not (facts 7–8). (d) 17 Sep 2026: workflow execution protections GA, with a default rule disabling `pull_request_target` on public repositories, in evaluate mode until enforcement on 2 Nov 2026 (facts 10–11).
- **Limits of checkout v7.** GitHub warns that pwn requests via `run` blocks using `git` or `gh`, and via other events "such as issue_comment", "will not be blocked by this change" (checkout changelog, 2026-06-18). Static analysis (zizmor) is still needed.
- **SHA pinning.** Enforceable via the allowed-actions policy (fact 12). A GitHub community thread reports the policy treats local composite actions as unpinned (https://github.com/orgs/community/discussions/170337 — secondary).
- **Tools.** zizmor 1.30.1 is the newest entry in its release notes (https://docs.zizmor.sh/release-notes/, read 2026-09-23) and is published on crates.io under the MIT licence (https://crates.io/crates/zizmor); its exact release date is unconfirmed, but downstream PRs adopting it merged on 14 September 2026, so it was released on or before that date; actionlint's docs pin `rev: v1.7.12` (https://github.com/rhysd/actionlint/blob/main/docs/usage.md); Harden-Runner 2.21.1 was released on or before 17 September 2026 — a Renovate PR bumping v2.21.0 → v2.21.1 merged at "2026-09-17 20:06 UTC" (https://github.com/knu/avail/pull/40 — secondary for date). OpenSSF Scorecard's current version was not found.
- Permissions/`permissions: {}`, `persist-credentials`, OIDC, artifact attestations, self-hosted runner risk and `${{ }}` script injection were **not re-verified** against the hardening guide this run (§9).

### 4.5 Action versions and SHAs

| Action | Latest tag | Released | Full commit SHA | Source |
|---|---|---|---|---|
| actions/checkout | v7.0.1 | 20 Jul 2026 | 3d3c42e5aac5ba805825da76410c181273ba90b1 | https://github.com/actions/checkout/releases/tag/v7.0.1 |
| actions/setup-python | v7.0.0 | 20 Jul 2026 | 5fda3b95a4ea91299a34e894583c3862153e4b97 | https://github.com/actions/setup-python/releases/tag/v7.0.0 |
| actions/setup-node | v7.0.0 | 14 Jul 2026 | 820762786026740c76f36085b0efc47a31fe5020 | https://github.com/actions/setup-node/releases/tag/v7.0.0 |
| actions/setup-go | v7.0.0 | 16 Jul 2026 | b7ad1dad31e06c5925ef5d2fc7ad053ef454303e | https://github.com/actions/setup-go/releases/tag/v7.0.0 |
| actions/setup-dotnet | not found | not found | not found | — |
| actions/cache | not found | not found | not found | — |
| actions/upload-artifact | v7.0.1 | 10 Apr 2026 | not found (short SHA 043fb46 only) | https://github.com/actions/upload-artifact/releases |
| actions/download-artifact | v8.0.1 (listed in releases) | not found | not found | https://github.com/actions/download-artifact/releases |
| astral-sh/setup-uv | not verified (README snippet shows v10.1.0 → bec219d24cd3e171d82865faccec33120bb574f4, **unverified**) | not found | not verified | https://github.com/astral-sh/setup-uv |
| github/codeql-action | v4.x (exact tag not found) | not found | not found | — |

Notes: the four verified SHAs are commit SHAs linked from each release page, not annotated-tag objects. checkout also released backport tags v6.1.0 (d23441a48e516b6c34aea4fa41551a30e30af803), v5.1.0, v4.4.0, v3.7.0 and v2.8.0 on 20 July 2026. **Deprecations:** Node 20 is removed from runners on 23 September 2026 (fact 14); an older schedule (Node 24 default 2 June, removal 16 September 2026) still appears in runner warning text quoted in many issues, and is superseded by the editor's notes. download-artifact v8 is required to read non-zipped artifacts (fact 26). Artifact v3 removal and cache service v2 were not re-verified this run.

### 4.6 Hooks

- pre-commit: 4.6.2, released 10 August 2026, is the latest release on PyPI (https://pypi.org/project/pre-commit/), fixing node hooks "Regressed in 4.6.1"; pre-commit also added "pre-commit hook-impl: allow --hook-dir to be missing to enable easier usage with git 2.54+ git hooks" (https://github.com/pre-commit/pre-commit/releases, read 2026-09-23).
- prek 0.5.1, released 2026-09-01 (https://github.com/j178/prek/pull/2635); full parity since 0.4.5.
- Git itself now supports config-based hooks (2.54) running in parallel (2.55) (fact 24).
- **Local vs CI:** local hooks should be fast, auto-fixing checks (formatting, whitespace, secrets); CI must re-run everything because hooks are bypassable. This is a recommendation. DORA's pitfall "Not running automated tests before committing code" supports running tests before commit.
- lefthook and Husky current versions: not found.

### 4.7 CI design

Not covered in depth. Two current primary items: a `cache-mode` control for Actions cache access (changelog "Control GitHub Actions cache access with cache-mode", 2026-09-10, title only) and "Ubuntu 26 generally available and latest migration" (2026-09-17, title only) — `ubuntu-latest` is migrating, so pin runner images where reproducibility matters.

### 4.8 Code review practice

Not covered this run apart from DORA's guidance favouring synchronous review: "they should ask somebody else on the team to review the code right then" (https://dora.dev/capabilities/trunk-based-development/).

### 4.9 Git hygiene

Not covered this run (§9).

### 4.10 Git 3.0 and recent Git features

- Git 3.0: SHA-256, reftable, `main`, Rust required (fact 2; secondary summaries at dev.to and daily.dev). Maintainer Junio Hamano's git mailing-list post of 6 September 2026, "What will come after Git 2.56?" (archived at https://ratatoskr.run/git/2026/09/17520163/t), asks what the next release should be and offers "(1) Git 3.0 … (2) Git 2.99 … (3) Git 2.98 (or 2.97)".
- Git 2.55 (29 Jun 2026): experimental `git history fixup`, built-in fsmonitor on Linux, parallel config hooks, push to remote groups, terminal-control sanitisation of sideband output (https://github.blog/open-source/git/highlights-from-git-2-55/; https://about.gitlab.com/blog/whats-new-in-git-2-55-0/).
- Git 2.56: Hamano's same 6 September 2026 post says "the current development cycle for Git 2.56 will conclude around the end of this month", and Git for Windows snapshots published 2.56.0-rc2 on 22 September 2026; features include `git refs create/delete/update/rename`, `git branch --delete-merged`, `git add --resolved`, experimental `git history drop` (daily.dev, secondary).

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Git | VCS | 2.55.0 | 2026-06-29 | OS package manager | `.gitconfig` | git-scm.com |
| zizmor | Actions security static analysis | 1.30.1 | on or before 2026-09-14 (downstream adoption PRs merged that day; exact date unconfirmed) | `pipx install zizmor` / `zizmor .` | `zizmor.yml` | https://docs.zizmor.sh/release-notes/ |
| actionlint | Workflow correctness lint | 1.7.12 | not found | `go install github.com/rhysd/actionlint/cmd/actionlint@latest` | `.github/actionlint.yaml` | https://github.com/rhysd/actionlint |
| Harden-Runner | Runner egress/process monitoring | 2.21.1 | ≤ 2026-09-17 | `uses: step-security/harden-runner@<sha>` with `egress-policy: audit` | workflow step | https://github.com/step-security/harden-runner |
| OpenSSF Scorecard | Repo security posture | not found | not found | not found | — | — |
| pre-commit | Hook framework | 4.6.2 | 2026-08-10 | `pipx install pre-commit` | `.pre-commit-config.yaml` | https://pypi.org/project/pre-commit/ |
| prek | Rust pre-commit reimplementation | 0.5.1 | 2026-09-01 | `prek install` | `.pre-commit-config.yaml` or `prek.toml` | https://github.com/j178/prek |
| lefthook | Hook manager | not found | not found | not found | `lefthook.yml` | — |
| Husky | JS hook manager | not found | not found | not found | `.husky/` | — |

## 6. Changing in the next 12 months

- **23 Sep 2026 (today):** Node 20 removed from Actions runners; actions still declaring `node20` stop having a fallback (fact 14). **Flag: reached now.**
- **~End Sep 2026:** Git 2.56 — Hamano (6 September 2026): "the current development cycle for Git 2.56 will conclude around the end of this month"; 2.56.0-rc2 Git for Windows snapshots appeared 22 September 2026.
- **2 Nov 2026:** default rule disabling `pull_request_target` enforced on public repositories that had the default policy (fact 11). **Flag: within 12 months.**
- **Git 3.0:** no official date; Phoronix (11 September 2026) says "potentially coming around the end of 2026" and LWN (18 September 2026) says "If the 3.0 release does not happen in 2026, it seems certain to show up shortly thereafter" (both secondary). New repositories will default to SHA-256, which GitHub hosting must support; tools that validate "40-character SHAs" will need to accept 64-character ones. **Flag: possibly within 12 months.**
- **Ubuntu 26 `latest` migration** (changelog 2026-09-17, title only).
- End-of-support dates for Git 2.x releases, pre-commit, prek, zizmor, actionlint and Harden-Runner: not found (these projects publish no support windows that this run located).

## 7. Common mistakes

- **Assuming a SHA pin gets security backports.** It does not; the checkout v7 protection reached only floating-tag users (fact 8). Pair SHA pins with Dependabot for `github-actions`.
- **Copying `@v4`-era examples.** AI coding assistants trained on older data commonly emit `actions/checkout@v4` or `upload-artifact@v4`; with Node 20 removed (fact 14) and v7/v8 current, check the release page before accepting a suggested version. (The observation about assistants is this report's, not a cited study.)
- **Relying on `pull_request_target` after 2 November 2026 without an explicit event policy** — runs will fail on public repositories (fact 11).
- **Opting out with `allow-unsafe-pr-checkout` casually.** GitHub: "you should treat opting out as a deliberate security decision" (checkout changelog).
- **Enabling a merge queue without `merge_group`** — required checks never report and merges fail (fact 20).
- **Planning a merge queue on a personal-account repository** — not offered (fact 19); a public issue records exactly this surprise (https://github.com/ned2/dashpot/issues/250 — secondary).
- **Assuming repository push protection is on** for older or org-owned public repositories (facts 17–18).
- **Enforcing SHA pinning by policy while using local composite actions** (community report, secondary).
- **Regex-validating commit IDs as exactly 40 hex characters** — breaks under SHA-256 repositories in Git 3.0 (secondary: byteiota).

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| GitHub Docs (docs.github.com) | CC-BY-4.0 text, MIT code (per github/docs repository; not re-verified this run) | Yes | Yes | Yes (MIT) | "GitHub Docs, CC BY 4.0" + URL |
| GitHub Blog / Changelog (github.blog) | © GitHub, Inc., all rights reserved (footer "© 2026 GitHub, Inc.") | Brief quotes only (fair use) | Yes | No | Title, date, URL |
| git-scm.com docs (Git Documentation) | GPL-2.0 per Git project (not re-verified this run) | Brief | Yes | Only under GPL-2.0 — do not copy into Apache-2.0 files | URL |
| dora.dev | not found | Brief | Yes | n/a | "DORA, dora.dev" + URL |
| zizmor docs | MIT (conda-forge listing: "License · MIT") | Yes | Yes | Yes | Copyright notice + MIT text |
| actionlint | MIT ("The source code and website content are licensed MIT") | Yes | Yes | Yes | Copyright notice + MIT text |
| Harden-Runner | Apache-2.0 (GitHub package page) | Yes | Yes | Yes | NOTICE/licence retained |
| pre-commit | MIT (PyPI) | Yes | Yes | Yes | MIT notice |
| prek | not verified | Brief | Yes | Check first | URL |
| Secondary: dev.to, daily.dev, Phoronix, GitLab blog, byteiota | Various/all rights reserved | Brief | Yes | No | Author, site, URL; label "secondary" |

## 9. Not found, contested, not covered

**Contested**
- Push rulesets plan: Team (FPT docs) vs Enterprise Cloud (GHEC docs).
- Node 20 schedule: 2 June/16 September 2026 (runner warning text) vs 16 June/23 September 2026 (changelog editor's notes, authoritative and later).

**Not found**
- Full SHAs for setup-dotnet, cache, upload-artifact, download-artifact, setup-uv, codeql-action; exact latest tags for setup-dotnet, cache, codeql-action.
- Current versions of OpenSSF Scorecard, lefthook, Husky; release date for actionlint 1.7.12; exact release date for zizmor 1.30.1 (on or before 14 September 2026).
- dora.dev licence.

**Not covered (search budget exhausted)**
- Q2 in full (Conventional Commits, SubmittingPatches, PR-size research, Conventional Comments, SSH signing, gitsign).
- Q3: private vulnerability reporting, Dependabot alerts/security updates, code scanning default setup, CODEOWNERS; classic branch protection availability.
- Q4: re-verification of the hardening guide (permissions, `persist-credentials`, OIDC, artifact attestations, self-hosted runners, script injection) and Scorecard.
- Q5: artifact v3 removal and cache service v2 dates.
- Q7 (path filters and skipped required checks, reusable workflows, environments), Q8 (Google eng-practices, Microsoft Research, Copilot code review), Q9 (gitignore, gitattributes, LFS, filter-repo, BFG, `git check-ignore -v`).
- trunkbaseddevelopment.com and a current Git Flow statement.