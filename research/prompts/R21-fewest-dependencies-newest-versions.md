# RESEARCH RUN R21: Fewest dependencies, newest versions, and less for CI to check

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 24 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 24 September 2026.

This run informs these categories: project-bootstrap-and-audit (dimensions 2, 6 and 8, and what a new project starts with), keeping-current, supply-chain-security, ci-cd, and the dependency advice in every language skill.

## What this run is for

The owner wants every repository this standard sets up or audits to run on as few dependencies
as possible, each at its newest version. The reasoning: less to keep current, and less for CI
and dependency tools to check, so runs are shorter and the attack surface is smaller.

This run tests that aim against the evidence before it becomes a rule. Where the evidence
supports it, say how strongly. Where it says the aim is wrong, needs a limit, or trades one risk
for another, say so plainly: that is the most useful thing this run can find. Two trades to look
at: a release adopted the day it's published, and hand-written code replacing a mature package.

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Beliefs marked "(the standard, date)"** come from this repository's own standard,
   PROJECT-BOOTSTRAP-AND-AUDIT v0.37.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.
9. **Measured over asserted.** Where a question asks what something costs or saves, give
   measurements: what was measured, on what, when, and how large the effect was. Label an
   estimate or an opinion as one.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R21 · FORM: research-result v1
Save as: R21-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- Each direct dependency brings dependencies of its own. Installing an average npm package means trusting about 79 other packages and 39 maintainers (Zimmermann et al., USENIX Security 2019), and the npm graph has grown since.
- A large share of declared dependencies are never used. A study of Maven Central (Soto-Valero et al., 2021) called them "bloated dependencies".
- Fewer dependencies mean fewer advisories to triage, fewer update pull requests, faster installs and CI runs, and a smaller attack surface.
- "A little copying is better than a little dependency" (Go Proverbs, Rob Pike, 2015). Russ Cox's "Our Software Dependency Problem" (2019) sets out how to evaluate a dependency before adding it, and the OpenSSF publishes a "Concise Guide for Evaluating Open Source Software" for the same job.
- Running the newest stable release is the safest choice, because fixes land there first and older release lines stop getting them. A brand-new release is safest taken after a short wait, because malicious versions are usually found and removed within days.
- Release cooldowns: Dependabot waits three days by default; pnpm 11 waits one day by default; npm has `min-release-age`; Renovate has `minimumReleaseAge`; Yarn and Bun have similar settings; uv's `exclude-newer` accepts a relative duration.
- (the standard, 2026-09) Pester 5.7.x is the safe pin: Pester 6 exists and breaks things.
- An application should run and test on one runtime version: the newest stable one its deployment target can run. A library should test the oldest version it declares and the newest.
- Scientific Python's SPEC 0 recommends supporting each Python version for three years after its release, and core packages for two. It replaced NEP 29.
- Unused dependencies are found by deptry (Python), knip (JavaScript and TypeScript), cargo-machete and cargo-udeps (Rust), and `go mod tidy` (Go). depcheck is no longer maintained.
- The e18e project's module-replacements lists npm packages that built-in platform features now replace.
- Ruff replaces flake8, isort, black and pyupgrade. uv replaces pip, pip-tools, virtualenv and pipx. Biome replaces ESLint and Prettier for most projects.
- (the standard, 2026-09) A new JavaScript or TypeScript project starts with Biome 2.x for lint and format, and Vitest for tests.
- Node.js now has a stable built-in test runner, `fetch`, `--env-file`, `util.parseArgs`, a glob function and TypeScript type stripping, so a small project may need no package for any of them. Python 3.11 added `tomllib` and 3.9 added `zoneinfo`, so `tomli` and `backports.zoneinfo` are needed only below those versions.
- AI coding assistants recommend packages that don't exist at a measurable rate (Spracklen et al., "We Have a Package for You!", USENIX Security 2025), and attackers register those names ("slopsquatting"). Assistants also suggest the versions in their training data rather than the current ones.
- (the standard, 2026-09) Current toolchains: Python 3.14.x; PowerShell 7.6.x; .NET 10 LTS; Node.js 22 and 24, both LTS; Go 1.27; Rust 1.98.x, edition 2024.

## Questions

### Priority

1. What a dependency costs, measured:
   - what each direct dependency brings with it: transitive dependencies, maintainers trusted, vulnerabilities and advisories, update pull requests, install and CI time, and size;
   - the numbers, what was measured, in which ecosystem and when, and newer replications (npm, PyPI, Maven, Cargo, NuGet, Go);
   - where the evidence is weak, old or mixed, and whether "fewer dependencies is safer" holds up;
   - the counter-case: where writing your own code is riskier than a well-maintained package, for example cryptography, parsing, and dates and time zones.
2. Deciding whether to add one:
   - current published guidance: the OpenSSF Concise Guide for Evaluating Open Source Software, OpenSSF Scorecard and deps.dev as inputs, Russ Cox's "Our Software Dependency Problem", and the third-party policies of large projects such as Chromium and Kubernetes;
   - a short checklist a single maintainer can apply in minutes;
   - when copying a few lines beats adding a package, and when it doesn't.
3. Newest versions, safely:
   - do runtime and package maintainers recommend running the newest stable release, and what do they say about older supported lines?
   - how that combines with a release cooldown, and the current cooldown settings and defaults in Dependabot, Renovate, npm, pnpm, Yarn, Bun, uv and pip, with each setting's exact name;
   - for the 2025-2026 registry incidents (for example the chalk and debug compromise and Shai-Hulud on npm, and the nx "s1ngularity" attack), how long each malicious version was available before it was removed, and what that says about how long a cooldown should be;
   - when staying a major version behind is the right call, and how respected projects record that choice.
4. Which runtime versions to target and test:
   - published support policies for applications and for libraries: Scientific Python's SPEC 0, .NET's target-framework guidance, Go's release policy, Rust's MSRV conventions and Cargo's MSRV-aware resolver, and Node.js's guidance for package authors;
   - how many versions CI should test (one, the oldest and the newest, or every supported one), and any evidence of how often a version in the middle fails when both ends pass;
   - where the deployment target fixes the runtime (for example Windows PowerShell 5.1 on Windows Server, or a Linux distribution's system Python), what maintainers advise;
   - the current support windows and end-of-life dates for Python, Node.js, .NET, PowerShell, Go and Rust.
5. Finding what to remove, for Python, JavaScript and TypeScript, .NET, PowerShell, Go and Rust:
   - tools that find unused, duplicate or outdated dependencies, with current versions and maintenance status;
   - each tool's known false positives: plugins, command-line tools, type stubs, optional extras, dynamic imports;
   - the command that lists outdated dependencies in each ecosystem, for example `uv tree --outdated`, `npm outdated`, `go list -m -u all` and `dotnet list package --outdated`.

### Standard

6. What the platform now provides:
   - lists of packages that built-in features replace, such as e18e's module-replacements for npm;
   - Python backports and helpers made redundant by 3.9 to 3.14, for example `tomli`, `backports.zoneinfo`, `importlib-metadata`, `typing_extensions`, `mock` and `six`;
   - Node.js built-ins added from version 18 to 26, Go standard-library additions from 1.21 to 1.27, and .NET built-ins that replace common packages, for example System.Text.Json;
   - for each, the version that added it and the version where it became stable.
7. One tool per job:
   - what Ruff, uv, Biome and oxlint replace, and what they don't, type checking for example;
   - the toolchains' own tools: `go vet`, `gofmt`, `cargo fmt`, `clippy`, `dotnet format`, `node --test`, and whether `node --test` is enough for a new project in place of Vitest;
   - where consolidating removes a CI step, and where it only moves one.
8. CI that checks less and still catches what matters:
   - measurements of how dependency count affects install and CI time;
   - the current caching behaviour of setup-uv, setup-python, setup-node and actions/cache;
   - how GitHub Actions bills matrix legs and rounds minutes, and the free minutes on each plan;
   - path filters, and cancelling superseded runs;
   - which checks overlap in practice, for example two linters with the same rules, or two advisory scanners reading the same database.
9. AI coding assistants and dependencies:
   - evidence that assistants add dependencies a task doesn't need, suggest outdated versions from their training data, or name packages that don't exist;
   - the studies and their rates;
   - mitigations shown to work, such as instructions in context files, lockfile review, and checking that a package exists before installing it.
10. Measuring leaner and newer over time:
    - metrics a repository can track: direct and transitive dependency counts, libyear, versions behind, the share on the newest major version, open update pull requests, CI minutes per run;
    - tools that compute them;
    - whether any of these metrics has published evidence linking it to fewer incidents.
