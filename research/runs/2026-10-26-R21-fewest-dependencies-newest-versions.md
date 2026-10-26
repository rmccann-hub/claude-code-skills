# Verification: R21 (2026-10-26)

Checked by the receiving session on 2026-10-26. Only the claims this intake relies on were
checked: those going into `supply-chain-security`, those behind proposed corrections to the
standard, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| 75.1% of Maven dependency relationships are bloated: 2.7% bloated direct, 15.4% inherited, 57% transitive (Soto-Valero et al.) | verified | [arXiv 2001.07808](https://ar5iv.labs.arxiv.org/html/2001.07808) |
| 55.88% of the CI build time tied to npm dependency updates is triggered only by unused dependencies (Weeraddana, Alfadel and McIntosh, FSE 2024) | verified; **"3,427 build hours" not found** at the source read | [The authors' lab page](https://rebels.cs.uwaterloo.ca/confpaper/2024/07/16/dependency-induced-waste-in-continuous-integration.html); the ACM page answered HTTP 403 |
| nx's malicious packages were live for 4 hours | verified | [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem) |
| chalk and debug's malicious versions were available for about 2 hours | verified; **the quote differs**: "during the short 2-hour timeframe in which the versions were available for download" | [Wiz](https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk) |
| A 2026 replication measured package hallucination at 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini) | verified (Churilov, v3 of 2026-08-09) | [arXiv 2605.17062](https://arxiv.org/abs/2605.17062) |
| npm's `min-release-age` is in days and off by default | verified; that it "cannot be combined with `--before`" is **not confirmed**: the docs call it a complement to `before` | [npm config](https://docs.npmjs.com/cli/v11/using-npm/config) |
| uv's `exclude-newer` takes a duration, such as `1 week`, as a cooldown | verified | [uv resolution](https://docs.astral.sh/uv/concepts/resolution/) |
| pnpm's `minimumReleaseAge` defaults to 1440 minutes | verified; the default dating from pnpm 11.0 not checked | [pnpm supply chain security](https://pnpm.io/supply-chain-security) |
| Pester 6.2.0 (2026-09-09) is current; 5.9.1 (2026-08-11) is the newest 5.x | verified | [PowerShell Gallery](https://www.powershellgallery.com/packages/Pester) |
| Rust's stable is 1.99.1, 2026-10-15 | verified; **the standard's 1.98.x is contradicted** | [Rust blog](https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/) |
| Node 26 becomes LTS on 2026-10-28; Node 22 ends 2027-04-30 | verified; **Node 24 entered maintenance on 2026-10-20**, not 28 October as the report's secondary source has it | [nodejs/Release schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json) |
| PowerShell 7.4 and 7.5 end on 2026-11-10; 7.6 LTS on 2028-11-14 | verified; the current 7.6 patch, contested in the report, is 7.6.6 per Microsoft | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6) |
| .NET 8 and 9 end on 2026-11-10; .NET 10 on 2028-11-14 | verified | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) |
| Python 3.10 reached end of life on 2026-10-01 | verified | [Status of Python versions](https://devguide.python.org/versions/) |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R21 · FORM: research-result v1
Save as: R21-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R21: Fewest dependencies, newest versions, and less for CI to check

The evidence supports the aim, but only as two bounded rules: choose direct dependencies by the size of the tree they pull in (pruning declared-but-unused direct dependencies saves little), and take the newest supported release after a short release-age gate of 1–3 days, with security fixes exempt — not on the day it is published.

## TL;DR

- **Fewer dependencies: supported, but the payoff is in transitive trees, not in pruning direct declarations.** An average npm package implicitly trusts 79 packages and 39 maintainers (2019 data), and 75.1% of Maven dependency relationships are bloated — yet only 2.7% of those relationships are bloated *direct* dependencies; most bloat is transitive. No published study found here links lower dependency counts to fewer incidents.
- **Newest versions: supported, with a cooldown.** The 2025 npm compromises (chalk/debug, nx, duckdb) were live for roughly 2 to 9 hours before removal, so a 1-day install gate (pnpm 11's default) and a 3-day update-PR gate (Dependabot's default, Renovate's `config:best-practices` for npm) would have blocked them; security updates are exempt in Dependabot and Renovate.
- **Three items in the standard are out of date:** Rust is 1.99.1 (not 1.98.x); Pester 6 has shipped and reached 6.2.0, and the 5.x line moved on to 5.9.1, so "5.7.x" is no longer the right pin; Node.js 26 becomes Active LTS on 2026-10-28, and PowerShell 7.4/7.5 and .NET 8/9 all lose support on 2026-11-10.

## 1. Summary

- Node.js 26 enters Active LTS on 28 October 2026, two days after this report; Node.js 24 moves to Maintenance LTS and Node.js 22 is in its last months. A new project should start on Node.js 26 from 28 October.\[1\]
- From Node.js 27, the project ships one major release per year (April), every release becomes LTS, and a six-month Alpha phase replaces odd-numbered releases.\[1\]\[2\]
- PowerShell 7.4 (LTS) and 7.5, and .NET 8 (LTS) and .NET 9, all reach end of support on 10 November 2026. PowerShell 7.6 LTS and .NET 10 LTS are supported until 14 November 2028.\[3\]\[4\]\[5\]
- Python 3.15.0 shipped 2026-10-09 (one week late, after an extra release candidate); the current patch is 3.15.2 (2026-10-25). Python 3.10 reached end of life on 2026-10-01, per the Python Developer Guide's "Status of Python versions" table; its final release was 3.10.22 that day.
- Rust's current stable is 1.99.1 (2026-10-15), not 1.98.x. Go's is 1.27.3; Go 1.25 lost support on 2026-08-19.\[6\]\[7\]
- Pester 6.0.0 shipped 2026-07-07 and 6.2.0 on 2026-09-09; the 5.x line continued to 5.9.1 (2026-08-11). Pinning 5.7.x leaves two newer 5.x releases unused.\[8\]
- Dependabot applies a 3-day cooldown to version updates by default, never to security updates; the setting is `cooldown.default-days` (1–90).\[9\]\[10\]
- pnpm's `minimumReleaseAge` defaults to 1440 minutes since pnpm 11.0 (not pnpm 10); it was introduced in 10.16.\[11\]\[12\]
- npm's `min-release-age` (days, npm 11.10.0+) is opt-in; Yarn uses `npmMinimalAgeGate`; Bun uses `install.minimumReleaseAge` (seconds); uv uses `exclude-newer` with relative durations; pip uses `--uploaded-prior-to` (relative durations from 26.1).\[13\]\[14\]
- The units differ between tools (days, minutes, seconds, duration strings), and older tool versions silently ignore the settings — the most common way a cooldown fails.\[13\]\[15\]
- Renovate's `config:best-practices` adds a 3-day `minimumReleaseAge` for npm, which overrides a longer top-level value unless you add your own npm package rule.\[16\]
- depcheck is archived (16 June 2025) and its README recommends knip.\[17\]
- Package hallucination by code models is measured: 5.2% (commercial) vs 21.7% (open-source) in the USENIX Security 2025 study. A 2026 replication (Churilov, arXiv 2605.17062; 5 models, 199,845 prompts) measured 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini).
- The SPEC 0 window (Python 3 years, core packages 2 years) is confirmed; NumPy states NEP 29 is superseded.\[18\] Under SPEC 0 the floor is now Python 3.13.
- There is a measured CI cost of unused dependencies for npm. Weeraddana, Alfadel and McIntosh ("Dependency-Induced Waste in Continuous Integration", FSE 2024) attribute 55.88% of the CI build time spent on npm dependency-specification updates (3,427 build hours) to unused dependencies. No study found measures incidents against dependency count.

## 2. Corrections

| Belief | Verdict | Correct fact | Source |
|---|---|---|---|
| "Installing an average npm package means trusting about 79 other packages and 39 maintainers … and the npm graph has grown since" | Confirmed (first half); second half not quantified | The 79/39 figures are from data up to 2018. No newer replication with numbers was read in this run. | https://www.usenix.org/system/files/sec19-zimmermann.pdf |
| "A large share of declared dependencies are never used" (Soto-Valero 2021) | Needs correction | 75.1% of 723,444 dependency *relationships* across 9,639 Maven artifacts were bloated, but most were transitive (57%) or inherited from parent POMs (15.4%); bloated *direct* dependencies were only 2.7%. "Declared" overstates it. | https://ar5iv.labs.arxiv.org/html/2001.07808 ; https://d-nb.info/1235316149/34 |
| pnpm's `minimumReleaseAge` defaults to 1440 | Needs correction | The default of 1440 applies from pnpm 11.0; the setting was added in 10.16 with no default. | https://pnpm.io/blog/releases/11.0 \[11\]\[12\] |
| pnpm 10 stopped running dependencies' `postinstall` scripts by default | Not re-verified | Not found in this run. pnpm 11's notes confirm `strictDepBuilds` now defaults to `true`. | https://pnpm.io/blog/releases/11.0 \[11\] |
| Renovate has `minimumReleaseAge` | Confirmed, with a default to note | Renovate's `config:best-practices` sets 3 days for npm since Renovate 42 (November 2025).\[19\] | https://github.com/renovatebot/renovate/discussions/39133 |
| uv's `exclude-newer` accepts a relative duration | Confirmed, with a version floor | Relative durations were added in uv 0.9.17 (December 2025, secondary); older uv ignores them with only a warning.\[20\]\[21\] | https://docs.astral.sh/uv/concepts/resolution/ ; https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html |
| (the standard) Pester 5.7.x is the safe pin; Pester 6 exists and breaks things | Out of date | Pester 6.0.0 (2026-07-07) carries the milestone's breaking changes and runs on Windows PowerShell 5.1 and PowerShell 7.4+. Current: 6.2.0 (2026-09-09). The 5.x line reached 5.9.1 (2026-08-11). The safe 5.x pin is now 5.9.x. | https://github.com/pester/Pester/releases ; https://www.powershellgallery.com/packages/pester/6.0.0 \[8\]\[22\]\[23\] |
| (the standard) Python 3.15.x, released 2026-10-09 | Confirmed, patch moved | 3.15.0 on 2026-10-09; 3.15.1 on 2026-10-21; 3.15.2 on 2026-10-25. | https://www.python.org/downloads/source/ \[24\] |
| (the standard) PowerShell 7.6.x | Confirmed | 7.6 LTS released 2026-03-18, supported to 2028-11-14. The latest patch number is contested (7.6.6, 7.6.8 and 7.6.9 all appear in sources). | https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6 \[25\]\[26\]\[27\]\[28\] |
| (the standard) .NET 10 LTS | Confirmed | Released 2025-11-11; end of support 2028-11-14. | https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core \[4\] |
| (the standard) Node.js 22 and 24, both LTS | Out of date within days | Node.js 26 becomes Active LTS on 2026-10-28; 24 moves to Maintenance; 22 is in Maintenance with about six months left (secondary). | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule \[1\] |
| (the standard) Go 1.27 | Confirmed | Released 2026-08-19; latest patch 1.27.3. | https://go.dev/blog/go1.27 ; https://endoflife.date/go \[7\]\[29\] |
| (the standard) Rust 1.98.x, edition 2024 | Wrong | Current stable is 1.99.1 (2026-10-15); 1.99.0 shipped 2026-10-01. Edition not re-verified. | https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/ \[6\]\[30\] |
| SPEC 0: Python 3 years, core packages 2; replaced NEP 29 | Confirmed | NumPy's NEP 29 page states it is superseded by SPEC 0. | https://scientific-python.org/specs/spec-0000/ ; https://numpy.org/neps/nep-0029-deprecation_policy.html |
| depcheck is no longer maintained | Confirmed | README says so; repository archived 2025-06-16; recommends knip. | https://github.com/depcheck/depcheck \[17\] |
| Spracklen et al.: 5.2% / 21.7%, 205,474 unique names | Confirmed, with a sample-size conflict | The USENIX abstract says 576,000 code samples; a Cloud Security Alliance note says 2.23 million. Use the USENIX figure. | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen |
| "Malicious versions are usually found and removed within days" | Correct, and conservative | The 2025 npm cases were removed within hours (about 2 to 9 h), not days. | See Q3\[31\]\[32\] |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Average npm package implicit trust | 79 packages, 39 maintainers | https://www.usenix.org/system/files/sec19-zimmermann.pdf | "Installing an average npm package introduces an implicit trust on 79 third-party packages and 39 maintainers" | 2019 (USENIX Security '19) |
| 2 | Bloated Maven dependency relationships | 75.1% of 723,444 | https://ar5iv.labs.arxiv.org/html/2001.07808 | "Our key result is that 75.1% of the analyzed dependency relationships are bloated." | 2020 preprint; EMSE 2021 |
| 3 | Share that are bloated direct dependencies | 2.7% (15.4% inherited, rest transitive) | https://d-nb.info/1235316149/34 | paraphrase | 2021 |
| 4 | CI time tied to unused dependencies (npm, Weeraddana, Alfadel & McIntosh) | 55.88% (3,427 build hours) of CI build time on npm dependency-spec updates; median project 56.09% | https://dl.acm.org/doi/10.1145/3660823 | "55.88% (3,427 build hours) of the overall CI build time" | Proc. ACM SE 1(FSE), 2024 |
| 5 | Dependabot default cooldown | 3 days, version updates only | https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference | "If not specified, Dependabot applies a default cooldown of 3 days." | read 2026-10-26\[9\] |
| 6 | Dependabot cooldown range | 1–90 days; include/exclude max 150 each | https://docs.github.com/en/enterprise-cloud@latest/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates | paraphrase | read 2026-10-26\[10\] |
| 7 | pnpm 11 defaults | `minimumReleaseAge` 1440, `blockExoticSubdeps` true, `strictDepBuilds` true | https://pnpm.io/blog/releases/11.0 | "minimumReleaseAge defaults to 1440 (1 day) and blockExoticSubdeps defaults to true." | pnpm 11.0 release\[11\] |
| 8 | npm `min-release-age` | days; npm CLI 11.10.0 (February 2026); opt-in | https://craigory.dev/blog/2026-05-29/package-manager-release-cooldown/ | paraphrase (secondary) | 2026-05-29\[12\] |
| 9 | Yarn setting | `npmMinimalAgeGate` | https://yarnpkg.com/configuration/yarnrc | "Minimum age of a package version according to the publish date on the npm registry" | read 2026-10-26\[14\] |
| 10 | Bun setting | `install.minimumReleaseAge`, seconds; Bun 1.3 | https://bun.com/docs/runtime/bunfig | paraphrase | read 2026-10-26\[13\]\[33\] |
| 11 | uv cooldown | `exclude-newer = "1 week"`; per-package `exclude-newer-package` | https://docs.astral.sh/uv/concepts/resolution/ | "uv also supports dependency \"cooldowns\" in which resolution will ignore packages newer than a duration." | read 2026-10-26 |
| 12 | pip cooldown | `--uploaded-prior-to` in 26.0 (absolute); relative from 26.1 | https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html | paraphrase (secondary) | 2026-03-04 |
| 13 | Renovate npm age | 3 days in `config:best-practices` since v42 | https://github.com/renovatebot/renovate/discussions/39133 | "minimumReleaseAge: 3 days will now be set by default for npm in config:best-practices" | 2025-11-06 |
| 14 | npm unpublish window | 72 hours | https://docs.renovatebot.com/configuration-options/ | "npm packages less than 72 hours (3 days) old can be unpublished from the npm registry" | read 2026-10-26 |
| 15 | chalk/debug exposure | about 2 hours | https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk | "during the short 2-hour timeframe in which the malicious versions were available on npm" | 2025-09-09\[31\] |
| 16 | chalk/debug full removal | 13:16 → 19:59 UTC on 2025-09-08; residue removed 2025-09-09 | https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/ | paraphrase | 2025-09-11\[34\]\[35\] |
| 17 | duckdb (same actor) exposure | 7–9 hours | https://semgrep.dev/blog/2025/chalk-debug-and-color-on-npm-compromised-in-new-supply-chain-attack/ | "these packages were available for 7-9 hours before being deprecated." | 2025-09-09\[32\] |
| 18 | Builds that pulled chalk/debug in 2 h | 76 projects, 70 teams (Vercel) | https://vercel.com/blog/critical-npm-supply-chain-attack-response-september-8-2025 | "Analysis identified 70 Vercel teams with builds containing the compromised package versions across 76 unique projects." | 2025-09-08\[31\] |
| 19 | nx exposure (maintainer) | 4 hours | https://nx.dev/blog/s1ngularity-postmortem | "The malicious packages were active for 4 hours before being completely removed from the registry." | 2025-09-05 |
| 20 | nx exposure (third party) | about 5 h 20 min | https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware | "The entire attack window lasted approximately 5 hours and 20 minutes" | 2025-08 |
| 21 | nx removal per advisory | nx removed 10:44 PM EDT 2025-08-26; @nx/key and @nx/enterprise-cloud 6:20 AM EDT next day | https://github.com/advisories/GHSA-cxm3-wv7p-598c | "These versions have since been removed from NPM as of 10:44 PM EDT" | 2025-08-27 |
| 22 | Shai-Hulud scale | over 500 packages | https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem | "A self-replicating worm—publicly known as “Shai-Hulud”—has compromised over 500 packages." | 2025-09-23 |
| 23 | Package hallucination rates | 5.2% commercial, 21.7% open-source | https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf | "hallucination rate of 5.2% compared to 21.7%." | USENIX Security 2025 |
| 24 | Spracklen sample size | 576,000 samples, 16 models | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | "we generate 576,000 code samples in two programming languages" | 2025 |
| 25 | 2026 replication (Churilov) | 5 models, 199,845 prompts: 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini); 127 names hallucinated by all five, 53 still registrable | https://arxiv.org/pdf/2605.17062 | "overall hallucination rates between 4.62% (Claude Haiku 4.5) and 6.10% (GPT-5.4-mini)" | 2026 |
| 26 | SPEC 0 Python window | 3 years | https://scientific-python.org/specs/spec-0000/ | "Support for Python versions be dropped 3 years after their initial release." | read 2026-10-26 |
| 27 | NEP 29 status | superseded by SPEC 0 | https://numpy.org/neps/nep-0029-deprecation_policy.html | "This NEP is superseded by the scientific python ecosystem coordination guideline SPEC 0" | read 2026-10-26 |
| 28 | Python 3.15.0 | 2026-10-09 | https://www.python.org/downloads/release/python-3150/ | "Release date: Oct. 9, 2026" | 2026-10-09\[36\] |
| 29 | Python latest patches | 3.15.2, 3.14.10 (2026-10-25); 3.13.17 (2026-10-21); 3.11.17 (2026-10-01) | https://www.python.org/downloads/source/ | paraphrase | read 2026-10-26\[24\] |
| 30 | Python 3.15 bugfix window | about 2 years | https://peps.python.org/pep-0790/ | "Python 3.15 will receive bugfix updates approximately every second month for two years." | read 2026-10-26\[37\] |
| 31 | Python 3.10 end of life | 2026-10-01 (final release 3.10.22 the same day); 3.11 end of life 2027-10 | https://devguide.python.org/versions/ | paraphrase (status "end-of-life", end-of-life date 2026-10-01) | read 2026-10-26 |
| 32 | Rust stable | 1.99.1, 2026-10-15 | https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/ | "The Rust team has published a new point release of Rust, 1.99.1." | 2026-10-15\[6\] |
| 33 | Go 1.27 | released 2026-08-19 | https://go.dev/blog/go1.27 | "Today the Go team is pleased to release Go 1.27." | 2026-08-19\[29\] |
| 34 | Go support policy | two newest majors; 1.25 ended 2026-08-19; 1.27.3 latest | https://endoflife.date/go | "Each major Go release is supported until there are two newer major releases." | read 2026-10-26\[7\] |
| 35 | Go 1.27 stdlib additions | `uuid` package, `encoding/json/v2` without GOEXPERIMENT, `crypto/mldsa` | https://go.dev/doc/go1.27 | paraphrase | 2026-08\[38\]\[39\]\[40\] |
| 36 | Node.js schedule change | one major per year from 27; LTS 30 months; 36 months total | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule | "Starting with 27.x, Node.js will move from two major releases per year to one." | 2026\[2\] |
| 37 | Node.js 26 dates | released 2026-05-05; Active LTS 2026-10-28; Maintenance 2027-10-20; EOL 2029-04-30 | https://hidekazu-konishi.com/entry/nodejs_release_and_eol_timeline.html | paraphrase (secondary) | 2026-07-24\[41\] |
| 38 | PowerShell 7.4/7.5 end of support | 10 November 2026 | https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6 | "The previous LTS release, PowerShell 7.4.20, is still supported until 10-Nov-2026." | read 2026-10-26\[25\] |
| 39 | .NET 10 / .NET 8 end of support | 2028-11-14 / 2026-11-10 | https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core | ".NET 10 \| November 11, 2025 \| 10.0.14 … LTS \| Active \| November 14, 2028" | page updated 2026-10-25\[4\] |
| 40 | .NET 8 and 9 end of support | 10 November 2026 | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | ".NET 8 and .NET 9 will reach end of support on November 10, 2026." | read 2026-10-26\[3\] |
| 41 | Pester 6 platforms | Windows PowerShell 5.1 and PowerShell 7.4+ | https://github.com/pester/Pester/releases | "Pester 6 runs on Windows PowerShell 5.1 and PowerShell 7.4+." | read 2026-10-26\[23\] |
| 42 | Pester 6 breaking changes | 6.0.0 milestone holds them | https://github.com/pester/Pester/milestone/29 | "should have all the breaking changes for this release." | closed 2026-07-09\[22\] |
| 43 | Pester versions | 6.2.0 (2026-09-09), 6.1.0 (2026-08-11), 5.9.1 (2026-08-11), 5.7.1 (2025-01-08) | https://www.powershellgallery.com/packages/pester/6.0.0 | paraphrase | read 2026-10-26\[8\] |
| 44 | depcheck status | unmaintained; archived 2025-06-16 | https://github.com/depcheck/depcheck | "Depcheck is no longer actively maintained" | read 2026-10-26\[17\] |

## 4. Findings

### Q1. What a dependency costs, measured

**Transitive trust (npm).** Zimmermann et al. measured the npm graph up to 2018: an average package implicitly trusts 79 third-party packages and 39 maintainers.\[42\] The same paper found that a small rise in direct dependencies produces a super-linear rise in indirect ones, and that the number of implicitly trusted maintainers almost doubled over three years.\[42\]\[43\] This is the strongest primary evidence that each *direct* dependency is a decision about a whole tree. It is also old (2018 data). A newer cross-ecosystem study (Arafat, arXiv 2512.14739, 2025-12-12) measured 500 projects across 10 ecosystems. It found mean dependency amplification of 24.70× for Maven, 4.48× for Go Modules and 4.32× for npm, and 28% of Maven projects exceeded 10×.

**Bloat (Maven).** Soto-Valero et al. measured 723,444 dependency relationships across 9,639 Maven Central artifacts. 75.1% were bloated: not needed to compile or run the code.\[44\] The breakdown matters for this standard. Only 2.7% were bloated *direct* dependencies; 15.4% were inherited from parent POMs; most of the rest were transitive.\[45\] When they sent pull requests removing bloated dependencies, developers accepted most of them.\[46\] **What it means:** a tool that lists unused declared dependencies attacks a small slice. The bigger win is picking direct dependencies whose own trees are small.

**CI cost (npm).** Weeraddana, Alfadel and McIntosh ("Dependency-Induced Waste in Continuous Integration", Proc. ACM SE 1(FSE), 2024) studied 20K+ commits in 1,487 npm projects. They found that 55.88% of the CI build time consumed by npm dependency-specification updates (3,427 build hours) is attributable to unused dependencies; the median project figure was 56.09%. This is the only measured link to CI minutes found in this run.

**Advisories, update PRs, install time and size per dependency:** no per-dependency measurement was found in this run (not found).

**Does "fewer is safer" hold?** It holds as an attack-surface argument: fewer maintainers can publish into your build. The 2025 incidents all entered through compromised maintainer accounts or tokens. But no study was found that links a lower dependency count to fewer incidents in a project (not found). Treat the claim as well-reasoned, not measured.

**Counter-case (writing your own).** No primary source on hand-rolled cryptography, parsers or time-zone code was gathered in this run (not covered). One relevant platform trend was found: Go 1.27 added a standard `uuid` package and `crypto/mldsa`.\[38\]\[39\] The safe direction is standard library first, a mature package second, hand-written code last for anything security-sensitive (opinion).

### Q2. Deciding whether to add one

Not covered in this run: OpenSSF Concise Guide, Scorecard, deps.dev, Russ Cox's essay, and the Chromium and Kubernetes third-party policies were not fetched. The belief items about them remain unverified.

Checklist a single maintainer can apply in minutes (opinion, built from the evidence above):

1. Does the standard library of the runtime you target already do it? (For example, Go 1.27 `uuid`.)
2. How many transitive packages and maintainers does it add? Count from the lockfile diff, not the README.
3. Does the package exist under exactly this name, and was the version published more than your cooldown ago? (Q9.)
4. Does it run install scripts? (pnpm 11 blocks dependency builds by default via `strictDepBuilds`.)\[11\]
5. Is it security-sensitive code (crypto, parsing untrusted input, time zones)? If so, prefer the mature package over copying.

### Q3. Newest versions, safely

**Runtime maintainers' position.** Runtime projects support only a few lines: Go supports the two newest majors; Python gives about two years of bugfixes per line (PEP 790); Node.js LTS is 30 months; PowerShell and .NET LTS lines get about three years.\[2\]\[4\]\[7\]\[37\] "Newest stable" therefore means newest *supported line*, updated to its newest patch. The Microsoft lifecycle page notes only the latest update of a release is supported (secondary report of it).\[26\]

**Cooldown settings (exact names):**

| Tool | Setting | Unit | Default | Since |
|---|---|---|---|---|
| Dependabot | `cooldown.default-days` (+ `semver-major-days`, `semver-minor-days`, `semver-patch-days`, `include`, `exclude`) | days, 1–90 | 3 days for version updates; never security updates | —\[9\]\[10\] |
| Renovate | `minimumReleaseAge` | duration | none, except 3 days for npm under `config:best-practices` | Renovate 42 (2025-11) for the preset |
| npm | `min-release-age` | days | off | 11.10.0 (2026-02)\[12\]\[47\] |
| pnpm | `minimumReleaseAge` (+ `minimumReleaseAgeExclude`, `minimumReleaseAgeStrict`) | minutes | 1440 | added 10.16; default from 11.0\[11\]\[12\]\[48\] |
| Yarn | `npmMinimalAgeGate` (+ `npmPreapprovedPackages`) | minutes (per Nesbitt, 2026-03-04, secondary); docs show duration strings | contested: reported as 1 day from 4.15 (Verdaccio docs, secondary); official docs give none | 4.10.0, September 2025 (Nesbitt, secondary) |
| Bun | `install.minimumReleaseAge` (+ `minimumReleaseAgeExcludes`) | seconds (unit strings accepted in current docs) | not stated; appears off | 1.3\[49\]\[50\] |
| uv | `exclude-newer` (+ `exclude-newer-package`) | timestamp or duration | off | relative durations in 0.9.17 (secondary) |
| pip | `--uploaded-prior-to` | timestamp; ISO 8601 duration from 26.1 | off | 26.0 (2026-01) (secondary) |

**How long malicious versions were live:**

| Incident | Date | Time available | Source |
|---|---|---|---|
| chalk/debug (18 packages) | 2025-09-08 | about 2 h for the bulk;\[51\] full removal by 19:59 UTC (about 6.7 h after 13:16); residue on 2025-09-09 | Wiz; Sygnia\[31\]\[35\] |
| duckdb (same actor) | 2025-09-08/09 | 7–9 h before deprecation | Semgrep\[32\] |
| nx "s1ngularity" | 2025-08-26/27 | 4 h (Nx), about 5 h 20 min (StepSecurity); some plugin versions until 6:20 AM EDT next day\[52\]\[53\]\[54\] | Nx; StepSecurity; GHSA |
| Shai-Hulud | 2025-09-14/15 to about 09-23 | per-version removal times not found; campaign kept publishing new infected versions for about a week\[55\]\[56\] | CISA; secondary timelines |

**What it says about cooldown length.** For single-publish compromises, the measured windows were hours, so a 1-day install gate covers them. A 3-day gate also covers npm's 72-hour unpublish window, which is the reason Renovate gives.\[57\] A worm differs: it keeps publishing *new* versions for days, and each new version restarts the clock. A cooldown still blocks each fresh version, as long as you never install anything younger than the gate. Exposure only arises if a version stays undetected longer than the gate. William Woodruff ("dependency cooldowns", blog.yossarian.net, November 2025, quoted by Andrew Nesbitt on 2026-03-04) found that 8 of the 10 supply-chain attacks he examined had windows of opportunity under a week; his sample covers supply-chain attacks generally, not only npm. **Recommendation:** 3 days for update PRs (Dependabot default; set Renovate explicitly) plus at least 1 day at install time, with security updates exempt. Use 7 days only where a team can't review lockfile diffs. The extra days add delay but no measured protection for the incidents above.

**Staying a major behind.** No respected project's written policy was gathered (not covered). The Pester case shows the pattern: 5.x kept getting releases (5.9.1) after 6.0 shipped.\[8\] Staying on 5.9.x is defensible while you migrate, but it should be recorded with a review date (opinion).

### Q4. Which runtime versions to target and test

- **SPEC 0:** drop Python versions 3 years after release and core packages 2 years after.\[58\] Python 3.12 (released 2023-10-02) passed that line on 2026-10-02, so the SPEC 0 floor is now 3.13 (derived; fonttools issue #4183 states the same date).\[59\]
- **Go:** each major is supported until two newer majors exist.\[7\] Go 1.26 therefore loses support when Go 1.28 ships; by the six-month cadence that is expected around February 2027 (estimate, not announced).
- **Node.js:** the new model applies from 27 (Alpha October 2026 → 27.0.0 April 2027 → LTS October 2027).\[2\]\[60\]
- **.NET target-framework guidance, Rust MSRV and Cargo's MSRV-aware resolver, the evidence on middle-version failures, and Windows PowerShell 5.1 and distro Python advice:** not covered in this run.
- The belief "an application tests on one runtime (newest its target runs); a library tests oldest declared and newest" was not found in a primary source. It is consistent with the support windows above, but treat it as the owner's policy (opinion), not a sourced rule.

**Support windows (current):**

| Runtime | Current | Released | End of support | Within 12 months? |
|---|---|---|---|---|
| Python 3.15 | 3.15.2 | 3.15.0 on 2026-10-09 | bugfixes about 2 years (PEP 790); security end not re-verified | —\[24\]\[37\] |
| Python 3.10 | 3.10.22 (final) | 2021-10-04 | 2026-10-01 (Python Developer Guide) | **Yes, already ended** |
| Python 3.11 | 3.11.17 | 2022-10-24 | 2027-10 (Python Developer Guide) | **Yes** |
| Node.js 26 | 26.x (26.12.0 reported) | 2026-05-05 | 2029-04-30 | No\[1\] |
| Node.js 24 | — | — | Maintenance from 2026-10-20 (secondary); EOL April 2028 (secondary) | No\[61\] |
| Node.js 22 | — | — | about April 2027 (secondary: "six months left") | **Yes**\[1\] |
| .NET 10 LTS | 10.0.14 | 2025-11-11 | 2028-11-14 | No\[4\] |
| .NET 8 LTS / .NET 9 | 8.0.33 | 2023-11-14 / — | 2026-11-10 | **Yes, in 15 days**\[3\]\[4\] |
| PowerShell 7.6 LTS | 7.6.x (patch contested) | 2026-03-18 | 2028-11-14 | No\[5\]\[26\] |
| PowerShell 7.4 LTS / 7.5 | — | 2023-11-16 / 2025-01-22 | 2026-11-10 | **Yes, in 15 days**\[5\]\[62\] |
| Go 1.27 | 1.27.3 | 2026-08-19 | when Go 1.29 ships (about August 2027, estimate) | **Probably**\[7\] |
| Go 1.26 | 1.26.10 | 2026-02-10 | when Go 1.28 ships (about February 2027, estimate) | **Yes**\[7\] |
| Rust | 1.99.1 | 2026-10-15 | superseded every 6 weeks; next (1.100) expected about 2026-11-12 (estimate from cadence) | **Yes**\[6\] |

### Q5. Finding what to remove

| Ecosystem | Tool | Version (date) | Status |
|---|---|---|---|
| JS/TS | knip | 6.40.0 (2026-10-06, from a search snippet; unconfirmed) | active\[63\] |
| JS/TS | depcheck | 1.4.7 (2023-10-17) | archived 2025-06-16; README recommends knip\[17\]\[64\] |
| Python | deptry | 0.25.1 (2026-03-18); 0.25.0 yanked; repository moved to osprey-oss/deptry | active\[65\] |
| Rust | cargo-machete | 0.9.2 (2026-04-15) | active\[66\] |
| Rust | cargo-udeps | 0.1.61 (2026-04-29) | active\[67\] |
| Go | `go mod tidy` | Go 1.27 now also consolidates require blocks | toolchain\[29\] |
| .NET, PowerShell | not found | — | — |

Known false positives (plugins, CLIs, type stubs, extras, dynamic imports) and the exact outdated-listing commands were not verified this run (not covered).

### Q6. What the platform now provides

- **Go 1.27** adds a standard `uuid` package, makes `encoding/json/v2` and `encoding/json/jsontext` available without `GOEXPERIMENT=jsonv2`, and adds `crypto/mldsa` (FIPS 204).\[38\]\[39\]\[40\] For new Go code, an external UUID library is no longer needed on 1.27+ (inference from the release notes).
- **Python 3.15** adds built-in `frozendict` (PEP 814), a sentinel type (PEP 661), explicit lazy imports (PEP 810), and UTF-8 as the default encoding (PEP 686).\[68\]
- The e18e module-replacements list, the Node.js 18–26 built-ins (stable versions), the Python 3.9–3.14 backports, and the .NET replacements were not covered this run. The beliefs about `tomllib` (3.11) and `zoneinfo` (3.9) stand unverified.

### Q7. One tool per job

Not covered this run (Ruff, uv, Biome, oxlint scope; toolchain tools; `node --test` vs Vitest). Biome's current version is contested: 2.5.13 (fetched page, likely stale) or 2.6.2/2.6.3 (search snippet and dependency-bot issues dated 2026-10-21).\[69\]\[70\]\[71\] The standard's "Biome 2.x" holds either way.

### Q8. CI that checks less

Measured: in one npm study, 55.88% of the CI build time spent on dependency-specification updates was attributable to unused dependencies (Weeraddana, Alfadel and McIntosh, FSE 2024; see Q1). GitHub Actions caching, billing, rounding, free minutes, path filters and concurrency were not covered this run.

### Q9. AI coding assistants and dependencies

- **Hallucinated names (measured):** 16 models; 576,000 Python and JavaScript samples (USENIX abstract); 205,474 unique hallucinated names; average rates 5.2% (commercial) vs 21.7% (open-source). The paper also tested mitigations and reports they "significantly reduce" hallucinations while keeping code quality (paraphrase of the USENIX abstract).\[72\]\[73\]
- **2026 replication** (Churilov, arXiv 2605.17062): 5 models on 199,845 prompts gave overall hallucination rates from 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini). 127 names were hallucinated by all five models, and 53 of those can still be registered. The floor has not fallen to zero, so existence checks stay necessary.
- **Unneeded dependencies and stale versions:** no measurement found this run (not found).
- **Mitigations with evidence:** registry cooldowns (Q3) also blunt slopsquatting, because a freshly registered hallucinated name is younger than the gate. This is an inference, not a measured result.

### Q10–Q13

Not covered this run: libyear and other metrics, lockfile enforcement commands and hashes, provenance verification (npm, PEP 740, crates.io, NuGet, Go checksum DB), and registry typosquat defences. One related fact was found: the npm changes GitHub announced after Shai-Hulud included automatic provenance attestations (secondary: versprite.com).\[56\]

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Dependabot | update PRs with cooldown | service | — | enable in repository | `.github/dependabot.yml` | GitHub Docs |
| Renovate | update PRs with cooldown | 42+ (44.121.3 seen in a PR) | 42: 2025-11 | `npx renovate` / app | `renovate.json` | Renovate docs |
| pnpm | package manager with default cooldown | 11.x (11.22 referenced) | 11.0: 2026 | `corepack enable` (not verified) | `pnpm-workspace.yaml` | pnpm blog\[11\]\[74\] |
| npm | `min-release-age` | 11.10.0+ needed | 2026-02 | `npm config set min-release-age 3 --location=user` | `.npmrc` | secondary guides\[13\] |
| uv | `exclude-newer` cooldown | ≥0.9.17 needed for durations | 2025-12 | — | `pyproject.toml [tool.uv]`, `uv.toml` | uv docs |
| pip | `--uploaded-prior-to` | ≥26.1 for durations | 2026 | `pip install --uploaded-prior-to P3D …` | `pip.conf` | secondary |
| knip | unused deps/files (JS/TS) | 6.40.0 (unconfirmed) | 2026-10-06 | `npx knip` (not verified) | `knip.json` | GitHub releases\[63\] |
| deptry | unused/missing deps (Python) | 0.25.1 | 2026-03-18 | `uvx deptry .` (not verified) | `pyproject.toml` | GitHub releases\[65\] |
| cargo-machete | unused deps (Rust) | 0.9.2 | 2026-04-15 | `cargo install cargo-machete` (not verified) | `Cargo.toml` metadata | GitHub, crates.io\[66\] |
| cargo-udeps | unused deps (Rust, nightly) | 0.1.61 | 2026-04-29 | `cargo install cargo-udeps` (not verified) | — | GitHub, crates.io\[67\]\[75\] |
| Pester | PowerShell tests | 6.2.0 (5.x: 5.9.1) | 2026-09-09 | `Install-PSResource -Name Pester -Version 6.2.0` | `PesterConfiguration` | PowerShell Gallery\[8\] |

## 6. Changing in the next 12 months

- **2026-10-28:** Node.js 26 → Active LTS; Node.js 27 Alpha opens.\[61\]
- **2026-10-01 (already passed):** Python 3.10 end of life per the Python Developer Guide; final release 3.10.22. Projects still on 3.10 are unsupported now.
- **2026-11-10:** .NET 8, .NET 9, PowerShell 7.4 LTS and PowerShell 7.5 end of support.\[3\]\[5\]
- **about 2026-11-12:** Rust 1.100 (estimate; 6-week cadence from 2026-10-01).
- **2026-12-01:** Python 3.15 next scheduled bugfix per PEP 790. Expedited releases already moved 3.15 to .2, so check before relying on it.\[24\]\[37\]
- **about 2027-02:** Go 1.28; Go 1.26 then loses support (estimate).
- **2027-04:** Node.js 27.0.0 (first under the new model); Node.js 22 end of life about then (secondary).\[60\]
- **2027-10:** Python 3.11 end of life (Python Developer Guide); Node.js 26 → Maintenance 2027-10-20.
- **Announced but unconfirmed:** npm CLI v12 "is expected" to enable `min-release-age` by default (a GitHub gist; speculation). pnpm is "preparing" version 12 with a Rust installer, Pacquet (secondary news; speculation).\[47\]\[76\]

## 7. Common mistakes

1. **Unit mix-ups when copying cooldowns:** npm uses days, pnpm minutes, Bun seconds, Yarn durations. Writing `1440` in `.npmrc` means 1440 days. (Source: charpeni.com, secondary.)\[77\]
2. **Older tools silently ignore the setting:** npm older than 11.10 ignores `min-release-age`; older uv warns and carries on without `exclude-newer`, re-resolving the lockfile to newer packages (GitHub issue gira0/cyberark-async#7).\[15\] Fix: pin the tool version (`required-version` in uv; `packageManager` / `engines` for npm and pnpm).\[21\]
3. **Renovate top-level `minimumReleaseAge` overridden for npm:** `config:best-practices` injects a 3-day npm rule, so a top-level "7 days" doesn't apply to npm (renovatebot/renovate discussion #40101).\[16\]
4. **Expecting Renovate's age check to stop branch creation:** Renovate can still create a PR with a pending `renovate/stability-days` check unless `internalChecksFilter: "strict"` is set (Renovate docs; discussion #38324).\[57\]\[78\]
5. **Name-only exclusions:** a name-only `minimumReleaseAgeExclude` entry is a permanent hole; pin a version (dev.to, secondary).\[74\]
6. **Dependabot cooldown blocking security fixes:** it doesn't; cooldown applies only to version updates (GitHub Docs).\[9\]\[10\] The mistake is disabling cooldown to "get fixes faster".
7. **AI assistants:** naming packages that don't exist: 5.2–21.7% in 2025, and 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini) for five 2026 models (Churilov, arXiv 2605.17062). Assistants also state runtime versions from their training data. This run itself found three stale toolchain entries in the standard (Rust, Pester, Node LTS), which is the same failure mode.
8. **Citing Soto-Valero as "75% of declared dependencies unused":** the 75.1% is of all relationships, mostly transitive (Q1).

## 8. Sources and licences

Licences were not verified in this run unless marked; where not verified, assume all rights reserved. Quote briefly with attribution and a link, paraphrase freely with attribution, and do not copy code examples into the Apache-2.0 repository until the licence is confirmed.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| GitHub Docs (Dependabot) | not verified (believed CC BY 4.0 for docs text) | brief | yes | only after confirming | title + URL |
| pnpm blog/docs | not verified | brief | yes | after confirming | title + URL |
| uv docs (Astral) | not verified (uv project believed MIT/Apache-2.0) | brief | yes | after confirming | title + URL |
| Renovate docs/discussions | not verified | brief | yes | after confirming | title + URL |
| Python.org release pages, PEP 790 | PEPs: not verified this run | brief | yes | n/a | title + URL |
| nodejs.org blog | not verified | brief | yes | n/a | title + URL |
| go.dev blog and release notes | not verified | brief | yes | after confirming | title + URL |
| blog.rust-lang.org | not verified | brief | yes | n/a | title + URL |
| Microsoft Learn, dotnet.microsoft.com, .NET blog | not verified | brief | yes | after confirming | title + URL |
| Pester GitHub, PowerShell Gallery | not verified | brief | yes | after confirming | title + URL |
| USENIX papers (Zimmermann 2019; Spracklen 2025) | not verified (USENIX open access; author copyright) | brief | yes | n/a | authors, title, venue, year |
| Soto-Valero et al. (arXiv/EMSE) | not verified | brief | yes | n/a | authors, title, EMSE 2021 |
| arXiv 2409.18884, 2605.17062 | not verified | brief | yes | n/a | authors, title, arXiv ID |
| SPEC 0, NEP 29 | not verified | brief | yes | n/a | title + URL |
| CISA alert | US government work, generally public domain (not verified) | yes | yes | n/a | CISA + URL |
| Wiz, Sygnia, Semgrep, Vercel, StepSecurity, Nx blog, GitHub Advisory | not verified | brief | yes | no | vendor + title + URL |
| Secondary blogs (craigory.dev, nesbitt.io, charpeni.com, herodevs, hidekazu-konishi, LogRocket) | not verified | brief | yes | no | author + URL; label "secondary" |

## 9. Not found, contested, not covered

**Not found**
- Any study linking dependency count, libyear or freshness to fewer incidents.
- Per-dependency measurements of advisories, update PRs, install time or size.
- Per-version removal times for Shai-Hulud.
- Evidence on how often a middle runtime version fails when both ends pass.
- The pnpm 10 postinstall default (not re-verified).
- Yarn's default age gate in the official docs.

**Contested**
- **nx exposure:** 4 h (Nx) vs about 5 h 20 min (StepSecurity) vs plugin versions until the next morning (GHSA).
- **chalk/debug:** about 2 h (Wiz) vs final removal about 6.7 h after the first publish (Sygnia).\[31\]\[35\]
- **Spracklen sample count:** 576,000 (USENIX) vs 2.23 million (CSA).\[73\]\[79\]
- **PowerShell 7.6 latest patch:** 7.6.6, 7.6.8 or 7.6.9.\[26\]\[27\]\[28\]
- **Biome latest:** 2.5.13, 2.6.2 or 2.6.3.\[69\]\[70\]\[71\]
- **Go 1.27.3 date:** 2026-10-19 (endoflife.date) vs 2026-10-20 (versio.io).\[7\]\[80\]
- **Yarn age-gate default and version:** 1 day from 4.15 (Verdaccio docs) vs other claims.\[81\]\[82\]

**Not covered (budget)**
- Q2 published guidance (OpenSSF Concise Guide, Scorecard, deps.dev, Russ Cox, Chromium, Kubernetes).
- Q4 .NET target frameworks, Rust MSRV and Cargo resolver, fixed deployment targets.
- Q5 false positives and outdated-listing commands.
- Q6 e18e and Node.js/Python/.NET built-ins.
- Q7 entirely.
- Q8 caching, billing, path filters, concurrency.
- Q10 metrics tools.
- Q11 lockfiles and hash checking.
- Q12 provenance.
- Q13 registry defences.
- The Go Proverbs belief.
- The PROJECT-BOOTSTRAP-AND-AUDIT v0.48.1 file itself was not fetched; the standard's beliefs were checked against product sources only.

## Sources

1. [Node.js 26 Becomes LTS on 28 October 2026: Which Node Version to Use Now, and How the New Yearly Release Schedule Works](https://www.vilvaathiban.com/blog/nodejs-26-lts-october-2026-which-node-version-to-use-new-release-schedule)
2. [Node.js — Evolving the Node.js Release Schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule)
3. [.NET 8 and .NET 9 will reach End of Support on November 10, 2026 - .NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/)
4. [.NET and .NET Core official support policy | .NET](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
5. [PowerShell End of Life - Lansweeper](https://www.lansweeper.com/blog/eol/powershell-end-of-life/)
6. [Announcing Rust 1.99.1](https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/)
7. [Go](https://endoflife.date/go)
8. [PowerShell Gallery](https://www.powershellgallery.com/packages/pester/6.0.0)
9. [Dependabot options reference - GitHub Docs](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
10. [Optimizing the creation of pull requests for Dependabot version updates - GitHub Enterprise Cloud Docs](https://docs.github.com/en/enterprise-cloud@latest/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates)
11. [pnpm 11.0](https://pnpm.io/blog/releases/11.0)
12. [Locking down dependency installs across npm, pnpm, yarn, and bun](https://craigory.dev/blog/2026-05-29/package-manager-release-cooldown/)
13. [Minimum Release Age: npm, pnpm, Yarn, Bun and Deno Settings](https://www.devanshuverma.in/blog/minimum-release-age-package-managers-complete-guide)
14. [Settings (.yarnrc.yml) | Yarn](https://yarnpkg.com/configuration/yarnrc)
15. [NPM 11.10.0 adds \`min-release-age\`](https://www.brandonpugh.com/til/node/package-version-cooldown/)
16. [NPM dependencies seem to not respect \`minimumReleaseAge\` · renovatebot/renovate · Discussion #40101 · GitHub](https://github.com/renovatebot/renovate/discussions/40101)
17. [depcheck/README.md at main · depcheck/depcheck · GitHub](https://github.com/depcheck/depcheck/blob/main/README.md)
18. [NEP 29 — Recommend Python and NumPy version support as a community policy standard — NumPy Enhancement Proposals](https://numpy.org/neps/nep-0029-deprecation_policy.html)
19. [Renovate 42 is out · renovatebot/renovate · Discussion #39133 · GitHub](https://github.com/renovatebot/renovate/discussions/39133)
20. [Package Managers Need to Cool Down](https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html)
21. [Older uv silently ignores exclude-newer = "1 week" and re-resolves uv.lock · Issue #7 · gira0/cyberark-async · GitHub](https://github.com/gira0/cyberark-async/issues/7)
22. [GitHub · Where software is built](https://github.com/pester/Pester/milestone/29)
23. [Releases · pester/Pester · GitHub](https://github.com/pester/Pester/releases)
24. [Python Source Releases for Source release](https://www.python.org/downloads/source/)
25. [PowerShell Support Lifecycle - PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6)
26. [PowerShell 7.6.9 LTS Released: .NET SDK 10.0.403 Update, Downloads and Support Deadlines](https://windowsforum.com/news/powershell-7-6-9-lts-released-net-sdk-10-0-403-update-downloads-and-support-deadlines.449975/)
27. [Microsoft PowerShell](https://endoflife.date/powershell)
28. [Microsoft PowerShell End of Life (EOL) Dates and End of Support (EOS) Dates](https://eosl.date/eol/product/powershell/)
29. [Go 1.27 is released - The Go Programming Language](https://go.dev/blog/go1.27)
30. [Announcing Rust 1.99.0](https://blog.rust-lang.org/2026/10/01/Rust-1.99.0/)
31. [Exposure management starts at the registry pull](https://www.chainguard.dev/supply-chain-security-101/exposure-management)
32. [Security Alert](https://semgrep.dev/blog/2025/chalk-debug-and-color-on-npm-compromised-in-new-supply-chain-attack/)
33. [bunfig.toml](https://bun.com/docs/runtime/bunfig)
34. [NPM debug and chalk is compromised](https://www.cybersierra.co/blog/npm-chalk-debug-compromised)
35. [16 Minutes to Impact: npm Supply Chain Abuse Deploys crypto-draining malware - Sygnia](https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/)
36. [Python Release Python 3.15.0](https://www.python.org/downloads/release/python-3150/)
37. [PEP 790](https://peps.python.org/pep-0790/)
38. [Go 1.27 Released with Generic Methods, JSON v2, and Faster Memory Allocation](https://linuxiac.com/go-1-27-released-with-generic-methods-json-v2-and-faster-memory-allocation/)
39. [Go 1.27 is becoming shockingly good](https://asacrew.medium.com/go-1-27-is-becoming-shockingly-good-da67d67b636c)
40. [Go 1.27 interactive tour](https://victoriametrics.com/blog/go-1-27/)
41. [Node.js Release and EOL Timeline - LTS Schedule, Active LTS and Maintenance, and End-of-Life Dates](https://hidekazu-konishi.com/entry/nodejs_release_and_eol_timeline.html)
42. [A Study of Security Threats in the npm Ecosystem](https://www.usenix.org/system/files/sec19-zimmermann.pdf)
43. [Small world with high risks: a study of security threats in the npm ecosystem](https://blog.acolyer.org/2019/09/30/small-world-with-high-risks/)
44. [\[2001.07808\] A Comprehensive Study of Bloated Dependencies inthe Maven Ecosystem](https://ar5iv.labs.arxiv.org/html/2001.07808)
45. [https://doi.org/10.1007/s10664-020-09914-8](https://d-nb.info/1235316149/34)
46. [Debloating Java Dependencies César Soto Valero Supervised by](https://www.diva-portal.org/smash/get/diva2:1755964/FULLTEXT03.pdf)
47. [Configuring minimum release age across npm, pnpm, and yarn · GitHub](https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104)
48. [Setting minimum age on package manager configs to prevent supply chain attacks · GitHub](https://gist.github.com/altryne/233ea8c8446c1ed0aead7561aeeca213)
49. [bun install](https://bun.com/docs/pm/cli/install)
50. [Bun 1.3](https://bun.com/blog/bun-v1.3)
51. [Widespread npm Supply Chain Attack: Breaking Down Impact & Scope Across Debug, Chalk, and Beyond](https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk)
52. [s1ngularity: Popular Nx Build System Package Compromised with Data-Stealing Malware - StepSecurity](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware)
53. [S1ngularity - What Happened, How We Responded, What We Learned](https://nx.dev/blog/s1ngularity-postmortem)
54. [Malicious versions of Nx were published · CVE-2025-10894 · GitHub Advisory Database · GitHub](https://github.com/advisories/GHSA-cxm3-wv7p-598c)
55. [Shai-Hulud Worm Attack Compromises npm Registry: Over 46,000 Malicious Packages and Widespread Credential Theft](https://www.rescana.com/post/shai-hulud-worm-attack-compromises-npm-registry-over-46-000-malicious-packages-and-widespread-crede)
56. [NPM Supply Chain Attack: Shai-Hulud Worm Compromises ...](https://versprite.com/resources/security/npm-supply-chain-attack-shai-hulud-worm-compromises-500-packages/)
57. [Configuration Options - Renovate Docs](https://docs.renovatebot.com/configuration-options/)
58. [Scientific Python - SPEC 0 — Minimum Supported Dependencies](https://scientific-python.org/specs/spec-0000/)
59. [About minimum Python version · Issue #4183 · fonttools/fonttools · GitHub](https://github.com/fonttools/fonttools/issues/4183)
60. [Node.js 26 becomes LTS this month, and Node.js changes how it releases](https://www.syntior.com/updates/nodejs-26-lts-new-release-schedule)
61. [Node 26: What Breaks When You Upgrade, and When the Jump Is Worth It (LTS Guide) - DEV Community](https://dev.to/marco_odev/node-26-what-breaks-when-you-upgrade-and-when-the-jump-is-worth-it-lts-guide-4go2)
62. [PowerShell 7.4 Support Ends Nov. 10, 2026: Move to 7.6 LTS](https://windowsforum.com/threads/powershell-7-4-support-ends-nov-10-2026-move-to-7-6-lts.439248/)
63. [Releases · webpro-nl/knip · GitHub](https://github.com/webpro-nl/knip/releases)
64. [depcheck 1.4.7 on npm - Libraries.io - security & maintenance data for open source software](https://libraries.io/npm/depcheck)
65. [Releases · osprey-oss/deptry](https://github.com/fpgmaas/deptry/releases)
66. [cargo-machete 0.9.2 on Cargo - Libraries.io - security & maintenance data for open source software](https://libraries.io/cargo/cargo-machete)
67. [cargo-udeps — Cargo add-on // Lib.rs](https://lib.rs/crates/cargo-udeps)
68. [Python 3.15.0 (final) is here!](https://blog.python.org/2026/10/python-3150-final-is-here/)
69. [\[deps\] @biomejs/biome 2.5.15 → 2.6.2 · Issue #1045 · nocoo/zhe · GitHub](https://github.com/nocoo/zhe/issues/1045)
70. [Releases · biomejs/biome · GitHub](https://github.com/biomejs/biome/releases)
71. [biome](https://mise-versions.jdx.dev/tools/biome)
72. [Slopsquatting in Python: What 205,474 Hallucinated Package Names Mean for Your Supply Chain - DEV Community](https://dev.to/duriantaco/slopsquatting-in-python-what-205474-hallucinated-package-names-mean-for-your-supply-chain-12oi)
73. [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen)
74. [pnpm 11 holds every new release for 24 hours, and our exclude list is nine pinned Expo versions - DEV Community](https://dev.to/daniel_pertu/pnpm-11-holds-every-new-release-for-24-hours-and-our-exclude-list-is-nine-pinned-expo-versions-14lc)
75. [GitHub - est31/cargo-udeps: Find unused dependencies in Cargo.toml · GitHub](https://github.com/est31/cargo-udeps)
76. [pnpm 11 Enables Default Release-Age Guard to Curb npm Supply Chain Attacks](https://gbhackers.com/pnpm-11-enables-default-release-age-guard/)
77. [Protecting Against Compromised Packages with Minimum Release Age](https://charpeni.com/blog/protecting-against-compromised-packages-with-minimum-release-age)
78. [minimumReleaseAge is still creating PRs before the configured age threshold leading to potential vulnerabilities · renovatebot/renovate · Discussion #38324 · GitHub](https://github.com/renovatebot/renovate/discussions/38324)
79. [Slopsquatting: AI Code Hallucinations Fuel Supply Chain Attacks](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419-csa/)
80. [Go releases, versions & end-of-life (EOL) dates](https://www.versio.io/en/product-release-end-of-life-eol-google-go.html)
81. [Yarn 4 can automate this](https://news.ycombinator.com/item?id=48357088)
82. [yarn](https://www.verdaccio.org/docs/setup-yarn/)
