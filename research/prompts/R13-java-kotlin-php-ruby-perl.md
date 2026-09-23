# RESEARCH RUN R13: Java, Kotlin, PHP, Ruby and Perl

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: java, kotlin, php, ruby, and legacy-languages (Perl, PHP 5-7, Java 8).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R13 · FORM: research-result v1
Save as: R13-RESULT.md
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

- Java 25 (LTS) was released in September 2025 and Java 26 in March 2026; Java 27 is due in September 2026. Java 21 and 17 are earlier LTS releases.
- Java 25 finalized compact source files and instance main methods, module import declarations, flexible constructor bodies and scoped values.
- Spring Boot 4 and Spring Framework 7 were released in November 2025, Gradle 9 in 2025, and JUnit 6 in 2025. Maven 4's status is to be confirmed.
- Kotlin 2.x uses the K2 compiler by default.
- PHP 8.5 was released in November 2025, with the pipe operator and a URI extension. PHP 8.1 reached end of life at the end of 2025; PHP 8.2 gets security fixes until the end of 2026.
- PHP-FIG's PER Coding Style (version 2 or 3) supersedes PSR-12. PHPStan 2, Rector 2, PHPUnit 12 and Pest 4 are current.
- Ruby 3.4 (December 2024) made Prism the default parser; Ruby 4.0 was released in December 2025; Rails 8.1 is current.
- Perl 5.42 is current.

## Questions

### Priority

1. Java:
   - release and support status (LTS and non-LTS, vendor support), and what a new project should target
   - features finalized in 21-27 that change idiomatic code
   - build tools: Maven 3.9 or 4.x, Gradle 9, with current versions
   - static analysis (Checkstyle, PMD, SpotBugs, Error Prone, NullAway) and formatting (google-java-format, Palantir)
   - the status of JUnit 6 and JUnit 5, and migration tooling (OpenRewrite)
2. Kotlin: the current version, K2, recommended tooling (ktlint, detekt, Kover), coroutines guidance, and Kotlin Multiplatform's status.
3. PHP:
   - supported versions and their dates; 8.4 and 8.5 features (property hooks, asymmetric visibility, the pipe operator)
   - the PER Coding Style version, and current PHPStan, Psalm, Rector and PHP-CS-Fixer versions
   - PHPUnit 12 and Pest 4; Composer's current version and security features (audit, blocking insecure packages)
   - PDO driver subclasses (8.4); Laravel and Symfony versions; WordPress coding standards
4. Ruby:
   - Ruby 3.4 and 4.0 features and support dates; the frozen string literal plan (chilled strings); YJIT and ZJIT
   - current RuboCop and Standard versions; RBS and Sorbet status
   - Rails 8.x (Solid Queue, Kamal, the authentication generator)
   - current RSpec and Minitest versions and conventions
5. Security in each language: the common vulnerability classes and the official security guidance (Java deserialization and XXE; PHP injection, file inclusion and `password_hash`; Ruby mass assignment and YAML or Marshal loading; the Rails security guide).

### Standard

6. Perl: the current release, Perl 7's status, perlcritic and perltidy, and when to modernize versus rewrite.
7. Legacy upgrades: Java 8 to 21 or 25 (common breakages, the jakarta namespace), PHP 5 or 7 to 8.x (Rector sets), Ruby 2.x to 3.x or 4.0, Rails upgrades.
8. Mistakes AI assistants make in these languages.
