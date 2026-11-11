# RESEARCH RUN R07c: Performance and concurrency

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: performance-and-concurrency.

## What this run is for

A follow-up to R07 (filed 11 November 2026), which covered Python 3.15's profiler, free
threading's status, Go 1.27 and Java's structured concurrency only in passing. This run supplies
what a planned `performance-and-concurrency` module needs: measuring before optimizing, the
profilers per language, benchmarking without fooling yourself, and concurrency per language.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R07c · FORM: research-result v1
Save as: R07c-RESULT.md
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

- Python 3.15's `profiling.sampling` (Tachyon) is the new sampling profiler, and free-threaded
  CPython is supported but optional since 3.14 (R07).
- py-spy, Scalene, BenchmarkDotNet, pprof, cargo flamegraph, criterion, async-profiler and JFR are
  the common profilers and benchmark tools in their languages.
- Java structured concurrency is to be final in JDK 28 (JEP 543), and virtual threads have been
  final since JDK 21 (JEP 444).
- Python's `asyncio.TaskGroup` and `asyncio.timeout` (3.11) are the current way to run and bound
  concurrent tasks.

## Questions

### Priority

1. **Measuring first:** published guidance on profiling before optimizing, sampling against
   instrumenting profilers, and what a flame graph shows and hides.
2. **Profilers and benchmark tools per language,** each with its current version, release date
   and run command: Python (py-spy, Scalene, `profiling.sampling`, `profiling.tracing`), Node.js
   (`--cpu-prof`, Chrome DevTools, clinic.js status), .NET (dotnet-trace, dotnet-counters,
   BenchmarkDotNet), Go (pprof), Rust (cargo flamegraph, criterion), Java (async-profiler, JFR,
   JMH).
3. **Benchmarking pitfalls,** from published sources: warm-up, dead-code elimination, noisy
   machines, too few runs, comparing means without spread, and how CI benchmarks catch
   regressions.
4. **Concurrency per language,** with current guidance and pitfalls from the official docs:
   Python asyncio (TaskGroup, timeouts, cancellation) and free threading's state and library
   support; JavaScript's event loop and workers; C# async and await (ConfigureAwait, ValueTask,
   cancellation tokens); Go goroutines, the race detector and context; Rust Send, Sync and tokio;
   Java virtual threads and structured concurrency.

### Standard

5. **Caching:** cache invalidation, stampedes, and the libraries per language, with versions.
6. **Complexity and data structures:** published guidance on choosing them for performance.
7. **Common mistakes,** including those AI coding assistants make, with sources.
