# RESEARCH RUN R05: Supply chain, dependencies, versioning, changelogs, releases, deprecation, and keeping current

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: supply-chain-security, versioning-and-releases, keeping-current, ci-cd.

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
   PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R05 · FORM: research-result v1
Save as: R05-RESULT.md
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

- Semantic Versioning 2.0.0, Keep a Changelog 1.1.0 and Conventional Commits 1.0.0 are the current versions.
- SLSA 1.1 (2025) is current; SPDX 3.0 and CycloneDX 1.6 or 1.7 are the current SBOM formats; OpenSSF Scorecard v5 is current.
- GitHub artifact attestations are generally available; GitHub added immutable releases in 2025, and a policy to require actions pinned to a full commit SHA.
- After the 2025 npm supply-chain attacks, including the "Shai-Hulud" worm, npm moved toward trusted publishing (OIDC) and shorter-lived tokens. PyPI supports trusted publishers and attestations (PEP 740); crates.io added trusted publishing in 2025.
- Dependabot supports the uv ecosystem and a `cooldown` option; Renovate supports `minimumReleaseAge`; pnpm added a minimum release age setting.
- (the standard, 2026-07) Dependency-update pull requests wait three days after a release by default, with no configuration. Security updates are exempt, and `cooldown: 0` opts out.
- (the standard, 2026-09) Immutable releases are a repository or organisation setting, not a default. When on, assets must be uploaded while the release is still a draft.
- endoflife.date publishes an API of support dates.
- PEP 751 defined a standard Python lock file (pylock.toml).

## Questions

### Priority

1. Versioning: SemVer 2.0.0 (is there a newer version or draft?), CalVer, and how major projects (Python, Node.js, .NET, Kubernetes, Rust) version and support their releases. How should a library of instructions or configuration, rather than code, apply SemVer: what counts as a breaking change?
2. Changelogs and release notes: Keep a Changelog's current version and rules; Conventional Commits; tools that generate changelogs and releases (release-please, semantic-release, changesets, git-cliff, GitHub's generated release notes), with current versions and the trade-offs for a single-maintainer repository.
3. Deprecation policy: how respected projects announce, time and remove deprecations (for example Python's PEP 387, Kubernetes' deprecation policy, .NET's breaking-change policy), and a template a small project can adopt.
4. Dependency updates: Dependabot (current ecosystems including uv, npm and GitHub Actions; version versus security updates; grouping; cooldown defaults and fields) versus Renovate (current features, minimumReleaseAge). How do teams avoid pulling a freshly published malicious version?
5. Keeping current at scale: how to track end-of-life dates and new releases automatically (the endoflife.date API, release feeds, OSV, deps.dev), and how professional platform teams run currency or freshness audits across many repositories.

### Standard

6. Supply-chain security:
   - SLSA 1.x levels
   - SBOM formats (SPDX 3.0.x, CycloneDX 1.6 or 1.7) and generators (syft, cdxgen, GitHub's dependency graph export)
   - provenance and signing: Sigstore/cosign current major version, GitHub artifact attestations, npm provenance, PyPI attestations
   - OpenSSF Scorecard's checks and the OpenSSF Best Practices badge
7. Registry and CI incidents of 2025-2026 (npm, PyPI, crates.io, NuGet, RubyGems, VS Code extensions, GitHub Actions, for example tj-actions/changed-files): what happened, and which controls would have stopped each.
8. Lockfiles and pinning per ecosystem: uv.lock and pylock.toml, package-lock.json and pnpm-lock.yaml, packages.lock.json (NuGet), go.sum, Cargo.lock, composer.lock, Gemfile.lock. Pinning GitHub Actions by SHA, and keeping the pins updated.
9. Vulnerability data:
   - sources: OSV, the GitHub Advisory Database, the NVD backlog's status, the CVE program's funding situation in 2025, CISA KEV
   - the audit command for each ecosystem: pip-audit, npm audit, dotnet list package --vulnerable, govulncheck, cargo audit, composer audit, bundler-audit
10. Obligations for software publishers: the EU Cyber Resilience Act timeline (reporting obligations, full application), and how it treats open-source stewards and non-commercial projects.
