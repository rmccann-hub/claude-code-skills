# RESEARCH RUN R06c: Testing, what R06 and R06b didn't reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: testing, and the testing file of every language skill.

Two earlier runs answered framework versions, flaky tests, mutation testing at Google, `claude
plugin eval`, coverage guidance, fail-open runner settings, test doubles and Pact, and tests
that agents write. Don't repeat those. This run covers what both listed as not covered.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R06c · FORM: research-result v1
Save as: R06c-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, labelled to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- The test pyramid comes from Mike Cohn's *Succeeding with Agile* (2009) and Martin Fowler's
  "TestPyramid" article; Kent C. Dodds' "testing trophy" puts integration tests at the centre;
  Google's *Software Engineering at Google* sorts tests by size (small, medium, large), and its
  chapter on test sizes is free to read online.
- Kent Beck's *Test-Driven Development: By Example* is the source of "see the test fail first".
- Fault injection for ordinary programs: `LD_PRELOAD` shims and libfiu on Linux, Toxiproxy for
  network faults, `tc netem` for latency and loss, and a full disk simulated with a small
  loopback or tmpfs filesystem.
- No published practice covers unattended acceptance runs on physical devices; teams write
  their own.

## Questions

### Priority

- **E. Acceptance and hardware-in-the-loop testing:** how projects that depend on physical
  devices (optical and disk drives, printers, embedded boards, test racks) structure unattended
  acceptance runs: preconditions that stop a run before it starts, detecting a device lost
  mid-run and stopping instead of recording failures, run-size tiers (smoke, nightly, full),
  evidence bundles and what they hold, and how often to run. Look for embedded-systems and HIL
  vendors' documentation, LAVA (Linaro), Fuego, KernelCI, openQA, and published test-rack
  practice. Give sources, cost, and when it isn't worth it.
- **F. Fault injection for ordinary applications:** a full disk, an unwritable folder, a network
  that drops or stalls, a device removed mid-operation, a process killed mid-write. Tools and
  patterns per language and platform (Linux, Windows, macOS), with versions: libfiu,
  `LD_PRELOAD` and `DYLD_INSERT_LIBRARIES` shims, Toxiproxy, `tc netem`, Windows Application
  Verifier, chaos-engineering tools scaled down for a desktop program. What each catches, and
  how a test proves the program handled the fault rather than crashed later.
- **D. Finding what you don't know is missing:** published practice for inventories of features,
  commands and settings checked against the tests that exercise them; and for mining past
  test-run records for checks whose result never varies (always pass, never run, always
  skipped). Name tools that report this, if any.
- **Q1. Test strategy, from primary sources:** Fowler's "TestPyramid" and "On the Diverse And
  Fantastical Shapes of Testing", Dodds' testing trophy post, and *Software Engineering at
  Google* chapter 11 on test sizes: the exact definitions, where they disagree, and what each
  recommends for a desktop or command-line program with no network service.

### Standard

- **Q11. Test data:** factories and builders (factory_boy, Fishery, Bogus), fixture files,
  snapshot and golden-file testing and how to keep snapshots honest (review rules, approval
  tests), database test strategies (transactions rolled back per test, containers), and
  Testcontainers' current version per language with release dates.
- **Q12. Idioms per language** for Kotlin, Ruby and Bash, and for Python, TypeScript, C#,
  PowerShell, Go and Rust where R06 gave versions only: fixtures, parameterized tests, mocks or
  fakes, and async tests, each with the framework's own documentation as the source.
- **Tool versions R06b couldn't find,** each from its registry with a release date:
  coverage.py, c8, istanbul (nyc), coverlet, cargo-llvm-cov, fast-check, FsCheck, CsCheck,
  jqwik, proptest, cargo-fuzz, Jazzer, PIT, mutmut, cosmic-ray, cargo-mutants, Infection,
  mutant, Stryker.NET, Stryker4s, the Pact libraries, ShellSpec, and Rubberduck for VBA.
