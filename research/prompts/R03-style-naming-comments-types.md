# RESEARCH RUN R03: Code style, naming, comments and docstrings, formatting, and types

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: code-style, types, and the style section of every language skill.

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

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R03 · FORM: research-result v1
Save as: R03-RESULT.md
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

- The official or de facto style guides are: PEP 8 and PEP 257 (Python); Microsoft's .NET naming guidelines and C# coding conventions; PowerShell's approved verbs (Get-Verb) and the community PowerShell Practice and Style guide; Effective Go, Go Code Review Comments and Google's Go style guide; the Rust API Guidelines and the rustfmt style guide (style edition 2024); PHP-FIG's PER Coding Style, which extends PSR-12; the community Ruby Style Guide (RuboCop); Kotlin's coding conventions; Google Java Style; the C++ Core Guidelines; Google's Shell Style Guide. TypeScript has no official style guide; typescript-eslint's recommended configurations are the de facto baseline.
- Doc comment formats: PEP 257 with the Google or NumPy docstring conventions; JSDoc and TSDoc; C# XML documentation comments; Go doc comments (syntax updated in Go 1.19); rustdoc; PHPDoc (PSR-5 is still a draft) through phpDocumentor; YARD; PowerShell comment-based help; Doxygen; Javadoc and KDoc.
- Formatters and linters in wide use: ruff (Python); ESLint with flat config and typescript-eslint, Biome, Prettier and oxlint (JS/TS); dotnet format and Roslyn analyzers (C#); PSScriptAnalyzer (PowerShell); gofmt, go vet, staticcheck and golangci-lint v2 (Go); rustfmt and clippy (Rust); PHP-CS-Fixer, PHPStan and Psalm (PHP); RuboCop and Standard (Ruby); Checkstyle, PMD, SpotBugs and Error Prone (Java); ktlint and detekt (Kotlin); clang-format and clang-tidy (C/C++); ShellCheck and shfmt (shell); SQLFluff (SQL); yamllint (YAML).
- Among Python type checkers, mypy and pyright are established, while Astral's ty and Meta's pyrefly are newer.

## Questions

### Priority

1. For each language (Python, TypeScript/JavaScript, C#, PowerShell, Go, Rust, Java, Kotlin, C, C++, PHP, Ruby, Bash, SQL, VBA): the official or most-adopted style guide, its naming rules (variables, constants, functions, types, files, modules), and its current URL. Confirm or correct the list above.
2. For each language: the doc comment format, what a public API's documentation must include, and the tool that renders or checks it.
3. For each language: the current formatter, linter and type checker (where one applies), with version, release date, recommended configuration, and whether it is still actively maintained. Confirm or correct the list above, and say which tools have been superseded.
4. Naming: evidence on identifier naming and comprehension (abbreviations, length, booleans, units in names) from peer-reviewed studies or respected sources.
5. Types: current guidance on strictness for Python (the typing spec, mypy and pyright strict modes, the status of ty and pyrefly), TypeScript (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`, `erasableSyntaxOnly`), C# (nullable reference types, warnings as errors), PHP (`declare(strict_types=1)`, PHPStan levels) and Ruby (RBS, Sorbet), and the status of the TC39 type annotations proposal.

### Standard

6. Comments for future maintainers: authoritative guidance on explaining why rather than what, TODO and FIXME conventions tied to issues, avoiding stale comments, and licence headers (SPDX short identifiers, REUSE).
7. Formatting consensus: tabs or spaces and line length under each language's official formatter; the current EditorConfig spec version and its supported properties.
8. Readability metrics: cyclomatic versus cognitive complexity, which tools report which, and recommended thresholds.
9. Style mistakes AI coding assistants make, per language, from published studies or vendor guidance.
