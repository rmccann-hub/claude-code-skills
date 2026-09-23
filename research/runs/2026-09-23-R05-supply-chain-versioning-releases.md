# Verification: R05 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| Dependabot waits 3 days before version updates, with no configuration; security updates are exempt | verified | [GitHub changelog, 2026-07-14](https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/); [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) |
| The cooldown keys are `default-days`, `semver-major-days`, `semver-minor-days`, `semver-patch-days`, `include` and `exclude` | verified; **the standard's bare `cooldown: 0` is not a documented form** | Dependabot options reference |
| Setting the cooldown to 0 removes it | unverifiable here: the discussion it cites answered HTTP 403 | [dependabot-core discussion #15582](https://github.com/dependabot/dependabot-core/discussions/15582) |
| Dependabot supports uv | verified in practice: its first uv, npm and github-actions runs on this repository succeeded on 2026-09-23 and opened no pull requests | Actions runs 35866855736, 35866852864, 35866852511 |
| .NET 8 and 9 end of support on 10 November 2026; Python 3.10 end of life in October 2026 | verified | see R03's table |
| Scorecard's checks (the report cites "the existing 19 Scorecard Checks") | verified: 19 checks run by default. **The standard's "Eighteen" is contradicted** | [Scorecard README](https://github.com/ossf/scorecard#scorecard-checks), read 2026-09-23 |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R05 · FORM: research-result v1
Save as: R05-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R05: Supply chain, dependencies, versioning, releases, deprecation and keeping current (as of 23 September 2026)

The standard's two dated beliefs hold up: Dependabot's three-day default cooldown (July 2026) and immutable releases as an opt-in setting (September 2026) are both confirmed by GitHub's own changelog. Three other beliefs are out of date. SLSA 1.1 has been replaced by SLSA 1.2 (November 2025). SPDX's current version is 3.0.1 (December 2024). CycloneDX 1.7 is the last 1.x release, and CycloneDX 2.0 is expected in autumn 2026. Two deadlines inside 12 months need action now: .NET 8 and .NET 9 both end support on 10 November 2026, and Python 3.10 reaches end of life on 31 October 2026. Since 11 September 2026, the EU Cyber Resilience Act's 24-hour reporting obligation has applied to manufacturers.

Read dates: every source below was read on 2026-09-23 unless it carries its own date.

## TL;DR

- **Standard confirmed, with one precision fix:** Dependabot waits three days before opening version-update pull requests, with no configuration; security updates are exempt. Opting out is done through the `cooldown` block (the numeric key documented by secondary sources is `default-days`). Immutable releases are an opt-in setting at repository or organisation level, and assets must be attached while the release is a draft.
- **Corrections:** SLSA 1.2 (November 2025, adds the Source Track) replaces 1.1. SPDX is at 3.0.1. CycloneDX 1.7 (21 October 2025, ECMA-424 2nd edition) is current and 2.0 is due in autumn 2026. npm revoked all classic tokens on 9 December 2025. pnpm 11 now enables a one-day `minimumReleaseAge` by default. Node.js moves to one major release a year from Node 27 (alpha October 2026).
- **Act within 12 months:** migrate off .NET 8 and 9 before 10 November 2026 and off Python 3.10 before 31 October 2026. Rework any parser of the NVD, which since April 2026 no longer enriches most CVEs. Any product you place on the EU market commercially has fallen under CRA reporting (24 hours, 72 hours, then a final report) since 11 September 2026.

## 1. Summary

1. Dependabot version updates now wait at least three days after a release before opening a pull request. This is the default, needs no configuration, and does not apply to security updates (GitHub changelog, 2026-07-14).
2. Dependabot's cooldown can be tuned per semver level (`default-days`, `semver-major-days`, `semver-minor-days`, `semver-patch-days`, plus `include` and `exclude`). Setting it to 0 removes it (dependabot-core discussion #15582; field list from a secondary source).
3. Renovate's `config:best-practices` preset includes `security:minimumReleaseAgeNpm`, which waits three days for npm packages only. Renovate's docs recommend `minimumReleaseAge: "14 days"` if you automerge third-party dependencies.
4. pnpm 11 defaults `minimumReleaseAge` to 1440 minutes (one day). npm has a `min-release-age` setting, measured in days.
5. npm permanently revoked all classic tokens on 9 December 2025. `npm login` now issues two-hour session tokens, and granular write tokens are capped at 90 days. Trusted publishing (OIDC) is the recommended route.
6. crates.io launched Trusted Publishing on 11 July 2025, for GitHub Actions only. PyPI finalised PEP 740 attestations on 14 November 2024; they are generated by default when the PyPA publish action runs under Trusted Publishing.
7. SLSA 1.2 is the current approved specification (November 2025). It adds a Source Track and is backwards compatible with 1.1.
8. CycloneDX 1.7 (21 October 2025) is ECMA-424 2nd edition and "the final version in the 1.x series". CycloneDX 2.0 is expected in autumn 2026, with Ecma ratification in December. SPDX's latest version is 3.0.1 (December 2024).
9. OpenSSF Scorecard is on v5 (v5.5.0, April 2026). A v6 proposal built on OSPS Baseline conformance is on the 2026 roadmap.
10. Cosign v3 makes the Sigstore bundle format the default, and `--bundle` is now required when signing. The latest release found is v3.1.3, which fixes a verification bypass (GHSA-fx35-mq7g-6g98).
11. GitHub immutable releases became generally available on 28 October 2025. Since 15 August 2025, organisations and repositories can enforce full-SHA pinning of actions through the allowed-actions policy.
12. .NET 8 (LTS) and .NET 9 (STS) both end support on 10 November 2026. .NET 10 LTS is supported until November 2028.
13. Python 3.10 reaches end of life on 31 October 2026. Python 3.14 is supported until about October 2030, and Python 3.15 final is expected in October 2026.
14. Since 15 April 2026, NIST has left most CVEs "not scheduled" for enrichment. Its priorities are KEV entries (target: one business day), software used by the federal government, and EO 14028 critical software.
15. CRA: manufacturers' reporting obligations have applied since 11 September 2026, through ENISA's Single Reporting Platform. Everything else applies from 11 December 2027. According to the Commission, open-source stewards' reporting starts on 11 December 2027.

## 2. Corrections

| Belief | Verdict | Correct fact | Source |
|---|---|---|---|
| SLSA 1.1 (2025) is current | **Wrong / out of date** | SLSA v1.2 is the latest version. It adds the Source Track and is "backwards compatible with SLSA v1.1". | https://slsa.dev/blog/2025/11/announce-slsa-v1.2 |
| SPDX 3.0 is current | **Imprecise** | The latest version is 3.0.1 (December 2024), a patch release. | https://spdx.github.io/spdx-spec/v3.0.1/ ; https://lists.spdx.org/g/Spdx-tech/topic/release_3_0_1_of_the_spdx/110308825 |
| CycloneDX 1.6 or 1.7 | **Narrow to 1.7** | 1.7 was released on 21 October 2025 as "the final version in the 1.x series" and was ratified as ECMA-424 2nd edition in December 2025. 2.0 is expected in autumn 2026. | https://cyclonedx.org/news/ ; https://ecma-international.org/publications-and-standards/standards/ecma-424/ |
| Scorecard v5 is current | **Confirmed, with an addition** | v5.5.0 is the latest v5 release. A v6 "OSPS Baseline conformance proposal and 2026 roadmap" has been merged as a document. | https://newreleases.io/project/github/ossf/scorecard/release/v5.5.0 |
| npm moved to OIDC and shorter-lived tokens | **Confirmed; stronger than stated** | All classic tokens were revoked on 9 December 2025. Logins get two-hour session tokens and write tokens are limited to 90 days. | https://github.blog/changelog/2025-12-09-npm-classic-tokens-revoked-session-based-auth-and-cli-token-management-now-available/ |
| pnpm added a minimum release age | **Out of date** | Since pnpm 11 it is on by default at 1440 minutes (one day). | https://pnpm.io/supply-chain-security |
| (the standard, 2026-07) three-day wait, no configuration, security exempt, `cooldown: 0` opts out | **Correct except the opt-out syntax** | The default, the exemption and the three days are confirmed. The primary source says only "set it to 0". The documented numeric key is `cooldown.default-days`, so write `default-days: 0` under `cooldown:`; no source shows a bare `cooldown: 0`. The default also reaches GHES in 3.23. | https://github.com/dependabot/dependabot-core/discussions/15582 ; https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/ |
| (the standard, 2026-09) immutable releases are a setting, not a default; upload assets while in draft | **Correct** | "You can enable immutable releases at the repository or organization level." Once published, assets "can't be added, modified, or deleted." Existing releases stay mutable unless republished. | https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/ ; https://github.blog/changelog/2025-08-26-releases-now-support-immutability-in-public-preview/ |
| endoflife.date publishes an API | **Confirmed, with a caveat** | The v1 API is "in Beta, and breaking changes can happen". v0 is deprecated. | https://github.com/endoflife-date/endoflife.date ; https://endoflife.date/docs/api |
| PEP 751 defined pylock.toml | **Confirmed** | Status Final, accepted on 31 March 2025. | https://peps.python.org/pep-0751/ |
| SemVer 2.0.0, Keep a Changelog 1.1.0, Conventional Commits 1.0.0 | **SemVer and Keep a Changelog confirmed; Conventional Commits not verified** | semver.org still serves 2.0.0 and no newer draft was found. Keep a Changelog's spec is 1.1.0; the site repository's 1.1.1 and 1.1.2 releases are translations and fixes only. | https://semver.org/ ; https://keepachangelog.com/en/1.1.0/ |
| GitHub artifact attestations are GA | **Confirmed** | Generally available since 25 June 2024. GitHub Changelog: "We're thrilled to announce the general availability of GitHub Artifact Attestations! … Powered by Sigstore." Immutable releases also generate "signed attestations". | https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/ ; https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/ |
| Dependabot supports uv | **Confirmed** | Version updates for uv became generally available on 13 March 2025: "For projects that use uv as a package manager, Dependabot version updates can now ensure dependencies stay current." Security updates followed on 16 December 2025: "Dependabot now supports security alerts and updates for uv." | https://github.blog/changelog/2025-03-13-dependabot-version-updates-now-support-uv-in-general-availability/ ; https://github.blog/changelog/2025-12-16-dependabot-security-updates-now-support-uv/ |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Dependabot default cooldown | 3 days; version updates only | https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/ | "This cooldown is now the default and requires no configuration." | 2026-07-14 |
| 2 | Security updates exempt | Open immediately | same | "Security updates still open immediately, so critical fixes are never delayed." | 2026-07-14 |
| 3 | Cooldown opt-out | Set to 0 | https://github.com/dependabot/dependabot-core/discussions/15582 | "set it to 0 to remove it entirely" | 2026-07 |
| 4 | GHES rollout | GHES 3.23 | changelog as #1 | "will take effect in GitHub Enterprise Server (GHES) 3.23" | 2026-07-14 |
| 5 | Immutable releases GA | 28 Oct 2025 | https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/ | "You can enable immutable releases at the repository or organization level in your settings" | 2025-10-28 |
| 6 | Existing releases unaffected | Stay mutable | https://github.blog/changelog/2025-08-26-releases-now-support-immutability-in-public-preview/ | "Existing releases remain mutable unless you republish them." | 2025-08-26 |
| 7 | SHA-pinning policy | Enforceable | https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/ | "any workflow that attempts to use an action that isn't pinned will fail." | 2025-08-15 |
| 8 | npm classic tokens | Revoked | https://github.blog/changelog/2025-12-09-npm-classic-tokens-revoked-session-based-auth-and-cli-token-management-now-available/ | "We've permanently revoked all existing npm classic tokens." | 2025-12-09 |
| 9 | npm session tokens | 2 hours | same | "when you use npm login you'll receive a two-hour session token" | 2025-12-09 |
| 10 | npm write tokens | ≤90 days | same | "write tokens limited to 90 days maximum" | 2025-12-09 |
| 11 | crates.io trusted publishing | Launched | https://blog.rust-lang.org/2025/07/11/crates-io-development-update-2025-07 | "We are excited to announce that we have implemented \"Trusted Publishing\" support on crates.io" | 2025-07-11 |
| 12 | PyPI PEP 740 | Final | https://blog.pypi.org/posts/2024-11-14-pypi-now-supports-digital-attestations/ | "This finalizes PyPI's support for PEP 740" | 2024-11-14 |
| 13 | PEP 751 | Final | https://peps.python.org/pep-0751/ | "Resolution: 31-Mar-2025" | 2025-03-31 |
| 14 | SLSA current | v1.2 | https://slsa.dev/blog/2025/11/announce-slsa-v1.2 | "SLSA v1.2 is backwards compatible with SLSA v1.1." | 2025-11 |
| 15 | CycloneDX 1.7 | Last 1.x | https://cyclonedx.org/news/ | "the final version in the 1.x series" | 2025-10-21 |
| 16 | CycloneDX 2.0 | Autumn 2026 | https://cyclonedx.org/news/ | "Release is expected in fall 2026, with Ecma ratification in December." | 2026-08-05 |
| 17 | ECMA-424 2nd ed. | CycloneDX 1.7 | https://ecma-international.org/publications-and-standards/standards/ecma-424/ | "This Standard defines the CycloneDX v1.7 Bill of materials specification" | 2025-12 |
| 18 | SPDX latest | 3.0.1 | https://spdx.dev/wp-content/uploads/sites/31/2024/12/SPDX-3.0.1-1.pdf | "Official SPDX® Specification 3.0.1" | 2024-12 |
| 19 | Scorecard latest | v5.5.0 | https://newreleases.io/project/github/ossf/scorecard/release/v5.5.0 | "The official Scorecard docker images are hosted on GitHub Container Registry starting with v5.5.0." | 2026-04-23 (date from secondary rywalker.com) |
| 20 | Cosign v3 bundle | Required | https://github.com/sigstore/cosign/releases/tag/v3.0.2 | "the --bundle flag … has moved from optional to required in v3." | 2025-10-10 |
| 21 | Cosign v3.1.3 | Security fix | https://github.com/sigstore/cosign/releases/tag/v3.1.3 | "This release resolves GHSA-fx35-mq7g-6g98, a verification bypass using an unexpected public key in a legacy bundle." | 2026-08-06 |
| 22 | pnpm default | 1 day | https://pnpm.io/supply-chain-security | "This defaults to 1440 (1 day)" | read 2026-09-23 |
| 23 | Renovate best-practices | npm 3 days | https://docs.renovatebot.com/presets-config/ | "security:minimumReleaseAgeNpm: Wait until the npm package is three days old before raising the update." | read 2026-09-23 |
| 24 | Renovate automerge advice | 14 days | https://docs.renovatebot.com/upgrade-best-practices/ | "If you automerge third-party dependencies, we recommend setting minimumReleaseAge to \"14 days\"." | read 2026-09-23 |
| 25 | .NET 8/9 EOS | 2026-11-10 | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | ".NET 8 and .NET 9 will reach end of support on November 10, 2026." | 2026-06-29 |
| 26 | .NET 10 | LTS to Nov 2028 | same | ".NET 10, which is an LTS release supported through November 2028" | 2026-06-29 |
| 27 | .NET STS length | 24 months | same | "STS releases now get 24 months of support instead of 18." | 2026-06-29 |
| 28 | Python 3.14 EOL | ~Oct 2030 | https://peps.python.org/pep-0745/ | "security updates (source only) will be released until five years after the release of 3.14.0 final, so until approximately October 2030." | read 2026-09-23 |
| 29 | Python policy | 2 + 3 years | https://endoflife.date/python | "2 years of planned releases with bugfixes. 3 years of only security fixes" | 2026-08-14 |
| 30 | Node.js new cadence | 1 major/year | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule | "One major release per year (April), with LTS promotion in October. Every release becomes LTS." | 2026 |
| 31 | Node.js support length | 36 months | same | "Total support: 36 months from first Current release to End of Life (EOL)." | 2026 |
| 32 | NVD Deferred | pre-2018 CVEs | https://www.nist.gov/itl/nvd | "All CVEs with a published date prior to 01/01/2018 that are awaiting further enrichment will be marked as Deferred" | 2025-04-02 / 2025-04-10 |
| 33 | NVD backlog | Not scheduled | same | "we will move all backlogged CVEs with an NVD publish date earlier than March 1, 2026, into the 'Not Scheduled' category." | 2026-04-15 |
| 34 | CVE contract | Extended | https://www.theregister.com/2025/04/16/cve_program_funding_save/ | "Last night, CISA executed the option period on the contract to ensure there will be no lapse in critical CVE services." | 2025-04-16 |
| 35 | CRA reporting start | 2026-09-11 | https://digital-strategy.ec.europa.eu/en/policies/cra-reporting | "As of 11 September 2026, manufacturers are required to report actively exploited vulnerabilities and severe incidents" | read 2026-09-23 |
| 36 | CRA steward reporting | 2027-12-11 | same | "open-source software stewards are subject to reporting obligations (Article 24(3)) from 11 December 2027." | read 2026-09-23 |
| 37 | CRA deadlines | 24 h / 72 h | same | "They need to submit an early warning within 24 hours of becoming aware, and a full notification within 72 hours." | read 2026-09-23 |
| 38 | endoflife.date API | v1 Beta | https://github.com/endoflife-date/endoflife.date | "The API is currently in Beta, and breaking changes can happen." | read 2026-09-23 |
| 39 | tj-actions | Secrets exposed | https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction | "This has been patched in v46.0.1." | 2025-03-18 |
| 40 | Keep a Changelog | 1.1.0 | https://keepachangelog.com/en/1.1.0/ | "[1.1.0] - 2019-02-15" | 2019-02-15 |

## 4. Findings

### 4.1 Versioning

**SemVer.** semver.org still presents "Semantic Versioning 2.0.0". No newer version or public draft was found on semver.org or in the semver/semver repository's description. The rule the repository depends on is: "Software using Semantic Versioning MUST declare a public API" (https://semver.org/spec/v2.0.0-rc.1.html, echoed in 2.0.0).

**CalVer.** Python's Steering Council rejected PEP 2026, which proposed calendar numbering such as "3.26", on 2025-02-06. This comes from a secondary source (https://hidekazu-konishi.com/entry/python_version_support_and_eol_timeline.html): "PEP 2026 proposed a calendar-based numbering scheme … but the Steering Council rejected it on 2025-02-06." Node.js, by contrast, has adopted year-aligned majors: "Version numbers align with the calendar year of their initial Current release: 27.0.0 in 2027, 28.0.0 in 2028" (nodejs.org).

**How major projects version and support releases:**

| Product | Current stable (release date) | End of support | Due within 6 months | 12-month flag |
|---|---|---|---|---|
| Python | 3.14 (3.14.0 on 2025-10-07; patch 3.14.6 per secondary dev.to/endoflifeai) | about October 2030 (PEP 745) | 3.15.0 final "expected in October" 2026; 3.15.0rc2 shipped on 2026-09-01 (secondary, HeroDevs) | **Python 3.10 EOL 2026-10-31** |
| Node.js | 26 (released 2026-05-05; nodejs.org release post "2026-05-05, Version 26.0.0 (Current), @RafaelGSS", https://nodejs.org/en/blog/release/v26.0.0) | not found for 26 | Node 26 becomes LTS in October 2026 ("Node.js 26 will enter long-term support (LTS) in October", nodejs.org); 27.0.0-alpha.1 in October 2026 | not found |
| .NET | 10 LTS (November 2025) | November 2028 (14 November 2028 per secondary endoflife.ai) | .NET 11 (STS) in November 2026 (secondary cyber-solutions.at) | **.NET 8 and 9 EOS 2026-11-10** |
| Kubernetes | not found this run | not found | not found | — |
| Rust | not found this run | not found | not found | — |

Python policy: releases arrive yearly (PEP 602), with about two years of bugfix releases followed by security-only fixes until five years after release (endoflife.date/python). .NET policy: LTS gets 36 months and STS now gets 24 months, so an LTS and the STS that follows it end on the same November Patch Tuesday (devblogs.microsoft.com). Node.js policy: from Node 27, "Every release becomes LTS", with 36 months of total support. The project's own advice to library authors is: "Please integrate Alpha releases to your CI as early as possible" (nodejs.org).

**SemVer for a library of instructions or configuration (recommendation; this is analysis, not a sourced standard).** SemVer requires a declared public API, so declare it. For this repository, the public API should be: skill names and paths, the frontmatter fields other tools read, the names and flags of scripts and their exit codes, the names and IDs of checks, and any documented rule a consumer audit relies on. Then:
- **Major:** removing or renaming a skill, a check ID or a script flag; making a rule stricter so that a previously passing repository now fails; changing an exit code or output format that other tools parse.
- **Minor:** adding a skill, a check that is advisory or off by default, or a new optional field; loosening a rule.
- **Patch:** fixing wording, typos or links, and refreshing a dated fact where the prescribed behaviour is unchanged.
- **Grey zone:** refreshing a dated fact that changes a recommendation, for example "use SLSA 1.2" instead of "use 1.1". Treat it as minor, and as major only if a check starts failing on it.

### 4.2 Changelogs and release notes

Keep a Changelog 1.1.0 (2019-02-15) is current (https://keepachangelog.com/en/1.1.0/). The site's repository has shipped "[1.1.1] - 2023-03-05" and "[1.1.2] - 2024-09-27", which are translations and fixes, not a new spec (subagent finding from the same site). The current version of Conventional Commits was **not verified** this run. Current versions of release-please, semantic-release, changesets and git-cliff, and details of GitHub's generated release notes, were **not found** this run (see section 9).

Trade-off for a single maintainer (analysis, unsourced): the repository must attach assets while releases are drafts (see 4.4 and 6). That makes a "create draft → upload assets → publish" flow mandatory, whatever the generator. Choose a tool that can create a draft release, or write the notes from a committed CHANGELOG.md and publish the release in a single workflow, as one maintainer does for this reason: "I'm probably going to put the release notes in a file in the repo so that the workflow can publish the release too" (secondary, https://aarol.dev/posts/immutable-releases-github/).

### 4.3 Deprecation policy

The primary texts of Python's PEP 387, the Kubernetes deprecation policy and .NET's breaking-change policy were **not retrieved** this run, so none of their rules are quoted here. What was sourced shows how respected projects signal ahead of time. Microsoft announced .NET 8/9 end of support on 29 June 2026, more than four months before the date, and said "Starting with a future servicing update for Visual Studio 2022, the .NET 8 and .NET 9 components will be marked as out of support" (devblogs.microsoft.com). Cosign deprecates in one line and removes in the next major: "Soon we'll start work on Cosign v4 where we will remove things that are currently deprecated" (https://github.com/sigstore/cosign/releases). Renovate's addition of a default `minimumReleaseAge` was tagged "breaking… requires major version bump" (https://github.com/renovatebot/renovate/issues/38478).

**Template for a small project (recommendation, modelled on the Cosign pattern above):**
1. Announce: add a `Deprecated` entry in CHANGELOG.md (a Keep a Changelog section) that states the replacement and the earliest removal version.
2. Warn: have checks or scripts emit a warning, not a failure, for at least one minor release and at least 90 days.
3. Remove: only in the next major version, listed under `Removed` with a migration note.
4. Exception: security fixes may remove behaviour in a patch release, with the reason stated.

### 4.4 Dependency updates and avoiding fresh malicious versions

**Dependabot.** Since 2026-07-14 the three-day cooldown is on by default for version updates "across all supported ecosystems on github.com". Security updates are exempt. Cooldown first became generally available on 1 July 2025 (secondary, classmethod.jp) and was extended to NuGet and Helm on 29 July 2025 (secondary, iuriio.com). The fields, per the secondary source iuriio.com, are `default-days`, `semver-major-days`, `semver-minor-days`, `semver-patch-days`, `include` ("max 150 entries; supports * wildcards") and `exclude`. GitHub's rationale post is linked from the changelog (https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/, not fetched). A secondary summary of that post says the GitHub Advisory Database "published more than 6,500 npm malware advisories in the year up to May 2026" (ehrensperger.dev). uv is supported: version updates became generally available on 13 March 2025 and security updates on 16 December 2025, when "Dependabot now supports security alerts and updates for uv" (GitHub Changelog). The full current ecosystem list and grouping syntax were **not verified** against GitHub Docs this run.

**Renovate.** `config:best-practices` extends `security:minimumReleaseAgeNpm`, a three-day wait for npm only. The docs recommend 14 days when automerging (docs.renovatebot.com). A request to extend the preset to other datasources such as PyPI is still open (https://github.com/renovatebot/renovate/discussions/42610, 2026-04-14). Because the preset is a `packageRule`, it overrides a root-level `minimumReleaseAge` for npm; use `ignorePresets: ["security:minimumReleaseAgeNpm"]` or your own `packageRules` (https://github.com/renovatebot/renovate/discussions/39963).

**Install-time gates.** pnpm 11 applies a one-day gate by default (pnpm.io). npm has `min-release-age`, in days, which cannot be combined with `--before`; uv has `--exclude-newer` (secondary: Matteo Collina's gist, https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104; HN item 47513932). The gist makes the key point: "The cooldown is enforced at install time, not at update-suggestion time. If you're using Renovate or Dependabot, configure their minimumReleaseAge / cooldown independently."

**How teams avoid a freshly published malicious version.** Layer the defences: an update-bot cooldown, an install-time minimum age, lockfiles with CI installing from the lockfile, SHA-pinned actions, and trusted publishing on the publishing side. Detection and takedown are fast, but not always fast enough. Renovate's 14-day advice exists "to give the upstream registries time to pull malicious dependencies". A vendor replay claims a 10–14% miss rate for slow-disclosure cases even at 14 days (secondary, vendor marketing, treat with caution: https://safeguard.sh/resources/blog/renovate-2026-security-mode-field-test).

### 4.5 Keeping current at scale

- **endoflife.date:** the v1 API (https://endoflife.date/docs/api/v1/) is unauthenticated and "currently in Beta, and breaking changes can happen". v0 is deprecated. Each product page links to its JSON, for example "/api/v1/products/api-platform/". The site is MIT-licensed.
- **Renovate `endoflife-date` datasource:** it lets Renovate raise pull requests for runtime versions recorded in arbitrary files through regex managers (https://docs.renovatebot.com/modules/datasource/endoflife-date/).
- **Fleet scoring:** Scorecard v5.4.0 "Added CLI flags to scan multiple repositories --repos, or an entire GitHub organization --org" (https://github.com/ossf/scorecard/releases/tag/v5.4.0, 14 Nov 2025).
- **Organisation policy as a currency control:** one organisation measured "every workflow in all 35 repositories" for SHA pinning before enabling `sha_pinning_required` (https://github.com/BitcreditProtocol/.github/issues/61, 2026-09-22). That is a real-world example of a fleet audit that ends in a policy change.
- **OSV, deps.dev, release feeds:** not researched this run.

### 4.6 Supply-chain security

- **SLSA 1.2:** it adds the Source Track, and the final release "Reorganized the Source Track levels. Level 2 now focuses on history and provenance while Level 3 focuses on continuous enforcement of technical controls" (https://slsa.dev/spec/v1.2/whats-new). The Build Track levels are unchanged. Build L2 is "Hosted build platform" and Build L3 is "Hardened builds" (secondary, cloudsmith.com).
- **SBOM formats:** SPDX 3.0.1 is published under Community Specification License 1.0 (SPDX PDF). CycloneDX 1.7 is ECMA-424 2nd edition, and 2.0 is expected in autumn 2026. Generators (syft, cdxgen, GitHub's dependency-graph SBOM export): **not found** this run.
- **Cosign:** v3 is the current major. "Cosign v3 defaults to signatures stored in bundles" (https://docs.sigstore.dev/cosign/system_config/installation/). The project "actively supports the most recent release as well as the last release in the v2 series" (https://github.com/sigstore/cosign). v3.1.3 fixes GHSA-fx35-mq7g-6g98. Upgrade if you verify legacy bundles.
- **Provenance:** PyPI attestations are generated by default through `pypa/gh-action-pypi-publish` ≥ v1.11.0 under Trusted Publishing (subagent, Trail of Bits/PyPI). GitHub immutable releases add "signed attestations" that can be checked with `gh release verify` and `gh release verify-asset` (secondary, sureshjoshi.com). GitHub Artifact Attestations, "Powered by Sigstore", have been generally available since 25 June 2024 (GitHub Changelog). npm provenance mechanics were **not verified**.
- **Scorecard:** v5 introduced "Structured Results… breaking the existing 19 Scorecard Checks into individual heuristics" (probes) (https://github.com/ossf/scorecard/releases). The OpenSSF Best Practices badge was **not researched**. Scorecard v5.5.0 supports a custom Best Practices URL.

### 4.7 Registry and CI incidents, 2025–2026

| Incident | What happened | Controls that would have stopped or limited it |
|---|---|---|
| tj-actions/changed-files (CVE-2025-30066), March 2025 | The attacker used a bot's personal access token and retroactively pointed tags v1 to v45.0.7 at a malicious commit that dumped runner secrets into logs. The GitHub Advisory Database (GHSA-mrrh-fwg8-r2c3) says the attack was "impacting over 23,000 repositories" and "The vulnerability existed between March 14 and March 15, 2025". CISA's audit window was 2025-03-12 00:00 to 2025-03-15 12:00 UTC. It was probably enabled by the reviewdog/action-setup@v1 compromise (CVE-2025-30154). Fixed in v46.0.1 (CISA; Wiz, secondary). | Full-SHA pinning ("the only way to use an action as an immutable release", GitHub Docs), now enforceable by policy. Immutable releases on the action's side (tags "can't be deleted or moved"). |
| Shai-Hulud wave 1, September 2025 | A self-propagating npm worm found on 2025-09-15, with @ctrl/tinycolor as the anchor. CISA's alert of 2025-09-23, "Widespread Supply Chain Compromise Impacting npm Ecosystem", states: "A self-replicating worm—publicly known as 'Shai-Hulud'—has compromised over 500 packages" (sourced by CISA to StepSecurity). It stole tokens and republished the victims' own packages. | Trusted publishing instead of long-lived tokens (npm's response), install cooldowns, and not running lifecycle scripts. |
| Shai-Hulud 2.0, 21–24 November 2025 | Ran in `preinstall` and leaked secrets to attacker-created repositories: Unit 42 counted "over 25,000 malicious repositories across about 350 unique users". It registered self-hosted runners for persistence and had a destructive fallback (Unit 42; Check Point). | The same as wave 1, plus disabling install scripts and rotating credentials after removal. Removing the package alone is not enough. |
| "Shai-Hulud: Here We Go Again", 2026 | Keyv, cacheable, flat-cache, file-entry-cache and related packages (Singapore CSA AD-2026-009; date not captured). | As above. |
| PyPI, crates.io, NuGet, RubyGems, VS Code extensions | Not researched this run. Wave 2 reportedly spread to OpenVSX (secondary, harekrishnarai repository). | — |

### 4.8 Lockfiles and pinning

PEP 751's `pylock.toml` is Final (accepted 2025-03-31). Its early adopters were pip 25.1, PDM 2.24.0 and uv 0.6.15, per the PyPA spec page as relayed by the subagent. The ecosystem details of uv.lock, package-lock.json, pnpm-lock.yaml, packages.lock.json, go.sum, Cargo.lock, composer.lock and Gemfile.lock were **not researched**. One adjacent fact: Scorecard now credits NuGet "Pinned Dependency with RestoreLockedMode" (Scorecard v5.1.0).

**Action SHA pins.** GitHub offers "policies at the repository and organization level to require actions to be pinned to a full-length commit SHA" (https://docs.github.com/en/actions/reference/security/secure-use). Two pitfalls follow. First, the policy checks the whole dependency tree, so composite actions that reference sub-actions by tag block downstream adopters (secondary, romainlespinasse.dev). Second, local `./.github/actions/...` references were reported as being flagged (community discussion #170337, **unresolved in the sources found**). Keep the pins current with Dependabot's `github-actions` ecosystem, which "understands SHA pins with version comments and updates both" (secondary, GitHub issue agigante80/Actual-sync#249), or with Renovate's `helpers:pinGitHubActionDigests`, which is part of `config:best-practices`.

### 4.9 Vulnerability data

- **NVD** (all from https://www.nist.gov/itl/nvd): the backlog was "still growing" in March 2025. CVEs published before 2018 and still awaiting enrichment became "Deferred" in April 2025. The legacy 1.1 feeds were removed in August 2025. On 15 April 2026 NIST moved to risk-based enrichment. It enriches KEV entries within about one business day, federal-use software and EO 14028 critical software; everything else is "Lowest Priority - not scheduled for immediate enrichment". Backlogged CVEs published before 1 March 2026 moved to "Not Scheduled", and NIST "will no longer routinely provide a separate severity score" where the CNA supplied one. In June 2026 NIST added CISA-ADP SSVC data and CVE "affected" data to its feeds. Consequence: do not rely on NVD CPE or CVSS enrichment for coverage. Use OSV or the GitHub Advisory Database for package-level matching, and the CNA's own scores.
- **CVE program funding:** MITRE's letter warned that the contract would expire on 16 April 2025. CISA exercised the option period on 15–16 April, an 11-month extension of a $57.8M contract to 16 March 2026 (The Record, citing contract documents). CVE Board members launched the CVE Foundation. CISA's September 2025 vision declared a "Quality Era" and kept government sponsorship. In 2026, the CVE Board minutes of 21 January record "no funding cliff in March", and CISA's acting director said the programme "is fully funded" (CSO Online, 2026-03-09, secondary). The contract value in 2026 is **not found**.
- **CISA KEV:** it added CVE-2025-30066 with a federal deadline of 4 April 2025 (secondary). NVD prioritises KEV entries "regardless of status".
- **Audit commands** (pip-audit, npm audit, dotnet list package --vulnerable, govulncheck, cargo audit, composer audit, bundler-audit): current versions **not researched**.

### 4.10 EU Cyber Resilience Act

- **Timeline:** in force since 11 December 2024. Reporting obligations apply from **11 September 2026** and full application from **11 December 2027** (https://orcwg.org/cra/; European Commission).
- **Reporting:** an early warning within 24 hours of becoming aware, a full notification within 72 hours, and a final report within 14 days of a corrective measure (for exploited vulnerabilities) or within one month (for severe incidents). All reports go through ENISA's Single Reporting Platform, "operational as of 11 September 2026" (Commission). A vulnerability known to be exploited before 11 September 2026 need not be notified (secondary, cyberresilienceact.eu).
- **Open-source stewards:** a "lighter-touch regime": no CE marking and no conformity assessment, but a cybersecurity policy and cooperation with market-surveillance authorities are required (secondary, Goodwin/Mondaq and Greenbone). **Contested:** the Commission says stewards' reporting applies "from 11 December 2027". Greenbone (secondary) says 11 September 2026. Rely on the Commission.
- **Non-commercial projects:** the regulation "distinguishes non-commercial open-source activity from commercial activity" (secondary, aegister.com). The exact recital text was **not retrieved**. On this evidence, a personal, non-monetised repository such as this one is likely outside the manufacturer obligations. That is an inference, not legal advice. Anyone who ships its content inside a commercial product becomes the manufacturer.
- **Guidance:** the Commission published draft CRA guidance on 3 March 2026, with feedback open until 31 March (secondary, HeroDevs).

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Dependabot | Update and security pull requests | Hosted service (no version) | Default cooldown 2026-07-14 | Built into GitHub | `.github/dependabot.yml` | github.blog changelog 2026-07-14 |
| Renovate | Update pull requests | 42.x (from secondary gist; exact version not found) | not found | `npx renovate` or the GitHub app | `renovate.json` | docs.renovatebot.com |
| pnpm | Package manager with release-age gate | 11.x (exact version not found) | not found | `npm i -g pnpm` | `pnpm-workspace.yaml` (`minimumReleaseAge`) | pnpm.io/supply-chain-security |
| OpenSSF Scorecard | Repository security scoring | v5.5.0 | 2026-04-23 (secondary) | `scorecard --repo github.com/ORG/REPO`; `--org` since v5.4.0 | `.github/workflows/scorecard.yml` (Action) | github.com/ossf/scorecard |
| Cosign | Signing and verification | v3.1.3 | 2026-08-06 | `go install github.com/sigstore/cosign/v3/cmd/cosign@latest` | none | github.com/sigstore/cosign |
| gh CLI | Release verification | not found | not found | `gh release verify` / `gh release verify-asset` | none | sureshjoshi.com (secondary) |
| endoflife.date API | EOL data | v1 (Beta) | not found | `curl https://endoflife.date/api/v1/products/python/` (path pattern from product pages) | none | endoflife.date |
| release-please, semantic-release, changesets, git-cliff, syft, cdxgen, pip-audit, govulncheck, cargo-audit, bundler-audit | — | not found this run | — | — | — | — |

## 6. Changing in the next 12 months

| Date | Change | Source |
|---|---|---|
| October 2026 | Node.js 26 promoted to LTS; Node.js 27.0.0-alpha.1 opens the new annual cycle | nodejs.org; InfoQ |
| October 2026 (expected) | Python 3.15.0 final | HeroDevs (secondary); Wikipedia |
| **31 October 2026** | **Python 3.10 end of life** | endoflife.ai / HeroDevs (secondary); PEP 619 per Ned Batchelder |
| **10 November 2026** | **.NET 8 and .NET 9 end of support** | devblogs.microsoft.com |
| November 2026 (expected) | .NET 11 (STS) | cyber-solutions.at (secondary) |
| Autumn 2026, Ecma ratification December (expected) | CycloneDX 2.0 | cyclonedx.org/news |
| Unscheduled | Cosign v4 removes deprecated features; v3 stays supported | github.com/sigstore/cosign/releases |
| Unscheduled | Scorecard v6 (OSPS Baseline conformance) proposal | Scorecard v5.5.0 notes |
| Unscheduled (forecast) | npm CLI v12 makes install scripts and non-registry sources opt-in; a default release-age gate is "expected" | craigory.dev; Collina gist (secondary, forecasts) |
| 12 January 2027 | .NET Framework 4.6.2 end of support | endoflife.ai (secondary) |
| 11 December 2027 (outside the window; plan now) | CRA full application and steward reporting | European Commission |

## 7. Common mistakes (including those AI coding assistants make)

1. **Assuming no cooldown exists.** Adding `cooldown` "to be safe" and not realising three days is already the default, or writing a bare `cooldown: 0`. The numeric key is `default-days` (dependabot-core #15582; secondary iuriio.com).
2. **Configuring the bot but not the installer, or the reverse.** A bot cooldown does not stop `npm install` pulling a two-hour-old transitive version. An install gate makes bot pull requests fail to install (Collina gist, secondary).
3. **Renovate's global `minimumReleaseAge` being silently overridden** for npm by `config:best-practices` (Renovate discussion #39963).
4. **Publishing an immutable release and then trying to attach assets.** Assets must be uploaded while the release is a draft (GitHub changelog; community discussion #178351).
5. **Pinning actions by tag or short SHA, or pinning only top-level actions.** The policy needs a full commit SHA throughout the dependency tree (GitHub Docs; romainlespinasse.dev, secondary). Assistants often emit `@v4`. Copilot-generated pull requests in the wild show assistants editing Dependabot cooldowns and pins (navikt/soknadsmottaker#225). Review those edits against the documentation.
6. **Citing outdated standards from training data:** "SLSA 1.0/1.1", "CycloneDX 1.5/1.6", "SPDX 2.3", "npm classic automation tokens", "Node odd/even releases", ".NET STS is 18 months". All are superseded (sources in section 2 and facts #14–#31).
7. **Treating NVD as the complete source of CVSS and CPE data** after April 2026 (nist.gov/itl/nvd).
8. **Assuming LTS means a long runway:** .NET 8 LTS ends on the same day as .NET 9 STS (devblogs.microsoft.com).
9. **Removing a compromised npm package without rotating credentials and checking for rogue self-hosted runners** (Panther and Check Point, secondary).

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| GitHub Blog / Changelog | Not stated on pages read; treat as all rights reserved | Brief, with attribution | Yes | Only trivial config snippets | "GitHub Changelog, <date>, <URL>" |
| GitHub Docs | Not verified this run (reported as CC BY 4.0, unconfirmed) | Brief | Yes | Check the licence before adapting | Title and URL |
| semver.org | Not verified this run | Brief | Yes | n/a | URL |
| keepachangelog.com | Not verified this run | Brief | Yes | Template reuse: verify the licence first | URL |
| SLSA (slsa.dev) | Not verified this run (Community Specification lifecycle mentioned) | Brief | Yes | n/a | URL |
| SPDX 3.0.1 | Community Specification License 1.0 (quoted in the spec PDF) | Yes | Yes | Examples: follow the CSL 1.0 terms | Include the required copyright line "Copyright © 2010–2024 Linux Foundation and its Contributors" |
| CycloneDX / ECMA-424 | Not verified this run | Brief | Yes | Verify first | URL |
| endoflife.date | MIT (quoted: "Licensed under the MIT License") | Yes | Yes | Yes, keeping the MIT notice | MIT copyright notice |
| Renovate docs | Not verified this run | Brief | Yes | Config snippets: verify first | URL |
| pnpm.io | Not verified this run | Brief | Yes | Trivial config | URL |
| nodejs.org, devblogs.microsoft.com, peps.python.org, nist.gov, digital-strategy.ec.europa.eu, cisa.gov | Not verified this run (US government works are generally public domain; not confirmed for these pages) | Brief | Yes | n/a | URL and date |
| sigstore/cosign, ossf/scorecard release notes | Not verified this run (repository licence may differ from release-note text) | Brief | Yes | Commands: yes | URL |
| Secondary blogs, vendors and press (InfoQ, The Register, CSO, Goodwin, Mondaq, Greenbone, HeroDevs, endoflife.ai, dev.to, safeguard.sh, Unit 42, Check Point, classmethod, iuriio, Collina gist, craigory.dev) | Not stated; assume all rights reserved | Short quotes only | Yes | No | Author or outlet, date, URL; label "secondary" |

## 9. Not found, contested, not covered

**Contested**
- Node.js 26 release date: resolved. The primary nodejs.org release post gives 2026-05-05, so InfoQ's "April 2026" is superseded.
- CRA steward reporting start: 11 December 2027 (European Commission) against 11 September 2026 (Greenbone). The Commission is preferred.
- npm classic token revocation date: 19 November 2025 (bybowu, secondary) against 9 December 2025 (GitHub changelog, primary). The deadline moved, and the primary source is preferred.
- CVE Foundation launch date: 16 April 2025 (URL slug, Forbes) against 17 April 2025 (HPCwire dateline).

**Not found / not verified**
- Conventional Commits' current version.
- Dependabot's full ecosystem list (uv support is confirmed).
- Kubernetes and Rust release and support policy.
- Current versions of release-please, semantic-release, changesets and git-cliff; GitHub generated release notes.
- The text of PEP 387, the Kubernetes deprecation policy and .NET's breaking-change policy.
- syft, cdxgen and GitHub dependency-graph SBOM export.
- npm provenance mechanics; the OpenSSF Best Practices badge.
- OSV and deps.dev APIs and release feeds.
- Current versions of the per-ecosystem audit commands.
- The CVE contract value in 2026.
- Licences for most sources.

**Not covered (out of room)**
- The per-ecosystem lockfile question (uv.lock, package-lock.json, pnpm-lock.yaml, packages.lock.json, go.sum, Cargo.lock, composer.lock, Gemfile.lock).
- Incidents on PyPI, crates.io, NuGet, RubyGems and VS Code extensions.
- The full CRA treatment of non-commercial projects (recitals).