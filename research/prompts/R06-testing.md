# RESEARCH RUN R06: Testing

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: testing, and the testing file of every language skill.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R06 · FORM: research-result v1
Save as: R06-RESULT.md
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

- pytest 9 is current, and Hypothesis is the standard Python property-based testing library.
- Jest 30 was released in 2025; Vitest 3 or 4 is current; Playwright is the most widely used browser end-to-end tool.
- xUnit v3, MSTest 3 or 4 and NUnit 4 are current, and TUnit is newer.
- (the standard, 2026-09) Pester 6 has been released and breaks things; 5.7.x is the safe pin.
- Go 1.24 added testing.B.Loop, and Go 1.25 made testing/synctest generally available.
- cargo-nextest is widely used for Rust.
- PHPUnit 12 (2025) is current and removed docblock annotations in favour of attributes; Pest 4 is current.
- JUnit 6 was released in 2025.
- Mutation testing tools: mutmut (Python), Stryker (JS/TS, C#, Scala), PIT (Java), cargo-mutants (Rust).

## Questions

### Priority

1. Test strategy: current authoritative guidance on the balance of unit, integration and end-to-end tests (the test pyramid, the testing trophy, others), what to test and what not to, and testing at boundaries. Cite sources, and note where they disagree.
2. For each language (Python, TypeScript/JavaScript, C#, PowerShell, Go, Rust, Java, Kotlin, PHP, Ruby, Bash): the current test framework or frameworks, version, release date, runner commands, and the idioms for fixtures, parameterized tests, mocks or fakes, and async tests. Confirm or correct the list above.
3. Test doubles: current guidance on mocks, stubs, fakes and spies; "don't mock what you don't own"; contract testing (Pact) status.
4. Coverage: meaningful targets, branch versus line coverage, why coverage should not be gamed, and the tools per language (coverage.py, c8/istanbul, coverlet, go test -cover, cargo-llvm-cov).
5. Flaky tests: detection, quarantine and fixing practices from large engineering organizations (Google, Microsoft, GitHub), with sources.

### Standard

6. Property-based testing and fuzzing: Hypothesis, fast-check, FsCheck or CsCheck, Go's native fuzzing, cargo-fuzz, Jazzer. When does each pay off?
7. Mutation testing: tools per language, current versions, costs, and when it is worth running.
8. End-to-end and UI testing: Playwright (current version), Cypress, Selenium 4, accessibility checks in tests (axe), visual regression.
9. Testing shell scripts and automation: bats-core, ShellSpec, Pester for PowerShell scripts, and what exists for testing Excel, VBA and Office automation.
10. Testing AI features and agent skills: evaluation practice (evals, LLM-as-judge with rubrics, baselines with and without the feature), including Anthropic's guidance and `claude plugin eval`.
11. Test data: factories, builders, fixture files, snapshot and golden-file testing; database test strategies (transactions, containers; Testcontainers' current version).
