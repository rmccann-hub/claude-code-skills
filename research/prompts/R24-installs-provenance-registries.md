# RESEARCH RUN R24: Installing what was locked, provenance on install, and registry defences

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 26 October 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 26 October 2026.

This run informs these categories: supply-chain-security, keeping-current, ci-cd, and the install
advice in every language skill.

## What this run is for

The supply-chain module tells an agent to install exactly what was locked, to check who built a
package or an update rather than a checksum published beside it, and to check a package name
before installing it. Run R21 didn't reach these three questions, so the module still says
"to be written" where each belongs. This run fills those gaps, one table per question, for the
ecosystems a professional meets most.

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
   PROJECT-BOOTSTRAP-AND-AUDIT v0.48.2, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.
9. **Measured over asserted.** Where a question asks what something costs or saves, give
   measurements: what was measured, on what, when, and how large the effect was. Label an
   estimate or an opinion as one.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R24 · FORM: research-result v1
Save as: R24-RESULT.md
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

- `npm ci` installs exactly what `package-lock.json` holds and fails when it disagrees with
  `package.json`; it doesn't update the lockfile.
- `uv sync --locked` fails when `uv.lock` is out of date, and `--frozen` installs from it without
  checking.
- pip checks hashes only when every requirement carries one, which `--require-hashes` makes
  mandatory; a `pip-tools` or `uv pip compile` lockfile can carry them.
- `pnpm install --frozen-lockfile` is the default in CI; Yarn Berry's is `--immutable`; Bun's is
  `--frozen-lockfile`.
- `cargo build --locked` fails when `Cargo.lock` would change, and Go checks every module against
  `go.sum` and the checksum database, sum.golang.org, by default.
- NuGet's lockfile, `packages.lock.json`, is opt-in, and `--locked-mode` refuses a restore that
  would change it.
- npm provenance links a package to the source repository and the workflow that built it, through
  Sigstore, and `npm audit signatures` checks it, but `npm install` doesn't check it by default.
- PyPI accepts PEP 740 attestations from trusted publishers, and neither pip nor uv checks them on
  install yet.
- crates.io supports trusted publishing, and NuGet.org requires author or repository signatures.
- GitHub artifact attestations, checked with `gh attestation verify --signer-workflow`, prove which
  workflow built a file; a checksum published beside the file proves nothing about who made it.
- npm, PyPI, crates.io and NuGet each block some names that look like popular packages, and none
  blocks a name an AI assistant invents before an attacker registers it.

## Questions

### Priority

1. Installing exactly what was locked, for npm, pnpm, Yarn, Bun, pip, uv, Poetry, Cargo, Go,
   NuGet, Composer and Bundler, as one table:
   - the lockfile, and whether a library should commit it;
   - the command that installs from it and fails rather than updates it when the lockfile and
     manifest disagree;
   - whether each package is checked against a hash in the lockfile by default, and how to turn
     that on where it isn't;
   - whether the install runs the package's own scripts by default, and the setting that stops it.
2. Verifying provenance when installing, for npm, PyPI, crates.io, NuGet, Go modules, RubyGems and
   Maven Central, as one table:
   - what each proves (who built it, from which source and workflow) and what it doesn't;
   - whether the installer checks it by default, on request, or not at all, and the exact command
     or setting;
   - how much of each registry carries it today, measured, with the date.
3. Verifying a downloaded update in a project's own code:
   - GitHub artifact attestations and Sigstore bundles: what `gh attestation verify` checks, which
     flags pin the signer, and whether it works offline from a bundle file;
   - libraries that verify a Sigstore bundle without `gh`: sigstore-python, sigstore-js, sigstore-go
     and sigstore-rs, with current versions and maintenance status;
   - refusing a downgrade or a replayed old release: what The Update Framework and Go's checksum
     database do, and what a small project can do without them.

### Standard

4. Registries' defences against typosquatted and invented package names:
   - what npm, PyPI, crates.io and NuGet do today, with each policy's source and date;
   - tools that check a name before it's installed, with current versions;
   - measured rates of typosquatted packages taken down, and how fast.
5. Common mistakes AI coding assistants make with installs: `npm install` where `npm ci` belongs,
   unpinned `pip install`, `curl | sh` installers, and disabling hash or signature checks to fix an
   error, with sources.
