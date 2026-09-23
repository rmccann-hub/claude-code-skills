# RESEARCH RUN R02: Repository structure, documentation, Markdown, file size and splitting

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: repo-structure, documentation, markdown, code-style (file and function size).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R02 · FORM: research-result v1
Save as: R02-RESULT.md
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

- GitHub recognizes community health files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, FUNDING, CODEOWNERS, issue and pull request templates) in the root, docs/ or .github/.
- Contributor Covenant 3.0 was released in 2025.
- Diataxis (tutorials, how-to guides, reference, explanation) is the most widely cited documentation framework.
- MADR 4.0 is the current Markdown Architectural Decision Record template.
- Material for MkDocs entered maintenance mode in late 2025, and its authors moved to a new tool (Zensical).
- The current CommonMark spec is 0.31.2. GitHub Flavored Markdown adds tables, task lists, strikethrough, autolinks, footnotes and alerts (NOTE, TIP, IMPORTANT, WARNING, CAUTION).
- markdownlint (with markdownlint-cli2) is the common Markdown linter, Vale the common prose linter, and lychee a common link checker.
- (the standard, 2026-09) For always-loaded context, prune past about 150 lines; about 300 lines is the outer limit anyone recommends. A tool shim should be about 30 lines, and a scoped rule file about 50.
- Default thresholds: ESLint max-lines 300 and max-lines-per-function 50 (both off unless enabled); Pylint too-many-lines 1000, too-many-statements 50 and too-many-branches 12; ruff C901 max-complexity 10; SonarQube cognitive complexity 15; RuboCop Metrics/MethodLength 10 and ClassLength 100; golangci-lint funlen 60 lines or 40 statements; clippy too_many_lines 100; Checkstyle FileLength 2000; SwiftLint file_length warning at 400.

## Questions

### Priority

1. Standard repository layouts from official or authoritative sources for each project type: a Python package (src layout, PyPA), a Node or TypeScript package and monorepo (workspaces), a .NET solution, a Go module (go.dev's "Organizing a Go module"), a Rust crate or workspace (the Cargo book), Java or Kotlin (Maven and Gradle layouts), a PowerShell module, a documentation site, and a repository of skills or plugins. Where do tests, docs, scripts, examples, config, CI and tooling files go?
2. The files a professional repository has and what each must contain: README (sections; the status of the standard-readme spec), LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md (and security.txt, RFC 9116, for websites), SUPPORT, CODEOWNERS, CHANGELOG, CITATION.cff, .editorconfig, .gitattributes, .gitignore, issue and pull request templates. Which does GitHub surface, and where does it look?
3. File size and splitting, from evidence: what official style guides and research say about maximum file length, function length, class size and complexity. Confirm or correct each default threshold above from the linter's own documentation. Is there research linking file or function size to defects or to review quality?
4. Splitting documents so they stay readable: guidance from technical-writing authorities (Google's developer documentation style guide, the Microsoft Writing Style Guide, Diataxis, Write the Docs) on page length, one topic per page, navigation, cross-linking and tables of contents. Should a split set of documents be navigated as an index plus leaves (hub and spoke), as a sequential chain, or both? Cite.
5. Progressive disclosure for AI agents: Anthropic's guidance for skills (SKILL.md under 500 lines, references one level deep, a table of contents in long references) and for CLAUDE.md, and any published evidence on how agents read long or chained files.

### Standard

6. Markdown: the current CommonMark and GFM specifications, GitHub's alert syntax, markdownlint's current rules and configuration file names, which rules to relax for agent-oriented files (such as inline HTML for XML tags), and Vale's and lychee's current versions and CI use.
7. Docs as code: MkDocs (and Material for MkDocs' maintenance status and successor), Sphinx, Docusaurus, Starlight, mdBook and DocFX: current versions, and when each fits.
8. Decision records: ADR practice (MADR 4, Nygard's format), where to store them, and how to supersede them.
9. Diagrams as code: Mermaid (current version, GitHub support), PlantUML, Structurizr and C4, D2. Which render natively on GitHub?
10. Comments versus documentation: authoritative guidance on what belongs in code comments, docstrings, commit messages and external docs, and on writing comments for future maintainers.
