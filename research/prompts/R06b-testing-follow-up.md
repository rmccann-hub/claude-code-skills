# RESEARCH RUN R06b: Testing, the questions R06 didn't reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 10 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 10 November 2026.

This run informs these categories: testing, and the testing file of every language skill.

An earlier run, R06, answered the framework versions, flaky tests, Google's mutation testing at
code review and `claude plugin eval`. Don't repeat those. This run covers what R06 listed as not
covered.

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
7. **Depth over breadth.** Finish the Priority questions fully, in order. If you run out of room,
   list the rest under "Not covered", so a further run can pick them up.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R06b · FORM: research-result v1
Save as: R06b-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, labelled A to G and Q1 to Q12 to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- The test pyramid (Cohn, popularized by Fowler) and the testing trophy (Dodds) disagree mainly on
  how much weight integration tests get; Google sorts tests by size (small, medium, large) rather
  than by kind.
- "Don't mock what you don't own" comes from Freeman and Pryce's *Growing Object-Oriented
  Software, Guided by Tests*. Pact is maintained and its broker's `can-i-deploy` gates a release.
- Branch coverage says more than line coverage, and a coverage target that's enforced gets
  gamed. Google publishes guidance that 60% is acceptable, 75% commendable and 90% exemplary.
- Hypothesis (Python), fast-check (JS/TS), FsCheck or CsCheck (.NET), jqwik (Java), proptest
  (Rust) are the property-based testing libraries in use; Go has native fuzzing since 1.18.
- Mutation testing tools: mutmut and cosmic-ray (Python), Stryker (JS/TS, C#, Scala), PIT (Java),
  cargo-mutants (Rust), Infection (PHP), mutant (Ruby).
- Playwright is current at 1.65; Cypress and Selenium 4 are maintained; axe-core is the usual
  accessibility engine in tests.
- bats-core and ShellSpec are the maintained shell test frameworks; nothing standard exists for
  testing VBA.
- Testcontainers has libraries for Java, Go, .NET, Node, Python and Rust.
- Kotlin projects test with JUnit 5 or 6 and Kotest; Ruby with RSpec and Minitest.

## Questions

### Priority: from this repository's audits

These come from audits of repositories set up against this one, where a test suite and an
acceptance run were green while the output was wrong. For each, give the established practice,
who uses it, its cost, and when it isn't worth it, with sources.

A. **Checks that can't fail, the parts R06 didn't find.** Sources on mutating a test oracle, a
   grader or a CI gate itself (not the product) to prove it can fail. Sources on testing the
   "couldn't check" path: a missing input, an empty range, a tool that isn't installed, reported
   as a pass.
B. **Test oracles and independent authorities.** When a tool reports on its own output, what
   counts as an independent check, and how do projects avoid grading output against the same
   code or data that produced it? Include differential testing against another implementation,
   metamorphic testing, and checking a reference's own settings before trusting a match with it.
C. **Scoring the worst case.** Guidance on scoring a system by its outputs that are wrong and
   reported as fine, rather than by its pass rate (silent failures, false assurance), including
   how safety-critical and storage or backup software measure it.
D. **Finding what you don't know is missing:** coverage of a whole system or acceptance run
   compared with its unit-test coverage; inventories of features, commands and settings checked
   against the tests that exercise them; mining past run records for checks whose result never
   varies.
E. **Acceptance and hardware-in-the-loop testing:** how projects that depend on physical devices
   (drives, printers, embedded boards) structure unattended acceptance runs: preconditions that
   stop a run, a lost device mid-run, run-size tiers, evidence bundles, and how often to run.
F. **Fault injection for ordinary applications:** a full disk, an unwritable folder, a network
   that drops or stalls, a device removed mid-operation; tools and patterns per language.
G. **Tests that agents write.** Documented failure modes of AI coding assistants writing or
   fixing tests: asserting the current output, weakening a test to pass, mocking the subject,
   tests that pass for the wrong reason. Anthropic's and others' guidance on reviewing them.
   Prefer primary sources: vendors' documentation, peer-reviewed studies, issue trackers.

### Priority: foundations

- **Q1. Test strategy:** current authoritative guidance on the balance of unit, integration and
  end-to-end tests (the test pyramid, the testing trophy, Google's test sizes), what to test and
  what not to, and testing at boundaries. Note where sources disagree.
- **Q3. Test doubles:** current guidance on mocks, stubs, fakes and spies; "don't mock what you don't
  own"; contract testing, with Pact's current versions and status.
- **Q4. Coverage:** meaningful targets, branch versus line coverage, why coverage should not be
  gamed, and the tools per language (coverage.py, c8 and istanbul, coverlet, `go test -cover`,
  cargo-llvm-cov), with versions.

### Standard

- **Q6. Property-based testing and fuzzing:** Hypothesis, fast-check, FsCheck or CsCheck, Go's native
  fuzzing, cargo-fuzz, Jazzer, with versions. When does each pay off?
- **Q7. Mutation testing:** tools per language with current versions, costs, and when it is worth
  running.
- **Q8. End-to-end and UI testing:** Cypress and Selenium 4 versions, accessibility checks in tests
  (axe-core and its wrappers), visual regression.
- **Q9. Testing shell scripts and automation:** bats-core, ShellSpec, Pester for PowerShell scripts,
  and what exists for testing Excel, VBA and Office automation.
- **Q11. Test data:** factories, builders, fixture files, snapshot and golden-file testing; database
  test strategies (transactions, containers; Testcontainers' current versions).
- **Q12. The languages R06 left out:** Kotlin, Ruby and Bash: the current test framework or
  frameworks, version, release date, runner command, and the idioms for fixtures,
  parameterized tests, mocks or fakes, and async tests.
