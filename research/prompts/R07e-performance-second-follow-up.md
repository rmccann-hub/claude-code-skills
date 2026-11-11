# RESEARCH RUN R07e: Performance, what R07c didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: performance-and-concurrency.

## What this run is for

A second follow-up. R07c covered profilers, flame graphs, benchmark harnesses and concurrency
per language; it is filed and checked. This run takes what it listed as not covered: caching,
data structures, statistics for comparing benchmarks, and a few language gaps. Don't repeat
its findings; where one has changed since, say so.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R07e · FORM: research-result v1
Save as: R07e-RESULT.md
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

- Cache stampedes are prevented by request coalescing, probabilistic early expiry, or a lock
  per key.
- benchstat (Go) compares benchmark runs with a significance test, and criterion (Rust) keeps a
  saved baseline to compare against.
- BenchmarkDotNet reports error and standard deviation by default.
- NumPy and pandas publish free-threaded CPython wheels.

## Questions

### Priority

1. **Caching:** published guidance on invalidation, expiry, stampedes and negative caching
   (vendor docs such as Redis, Memcached, Cloudflare and AWS, and papers where they exist), and
   the in-process cache libraries per language with versions (Python `functools`, cachetools;
   Node lru-cache; .NET `IMemoryCache` and `HybridCache`; Go; Rust moka; Java Caffeine).
2. **Comparing benchmark runs:** published guidance on noisy machines, run counts, spread
   against means, and significance tests; how benchstat, criterion, BenchmarkDotNet, JMH and
   pytest-benchmark report and compare; and how projects catch regressions in CI (for example
   CodSpeed, Bencher, github-action-benchmark), with versions.
3. **Choosing data structures for performance:** guidance from language documentation (Python's
   time-complexity page, the .NET collections guidance, Java's collections, Rust's
   `std::collections` "when to use" section) and well-known sources on complexity in practice.
4. **Free threading in libraries:** which major Python libraries ship free-threaded wheels
   today (NumPy, pandas, Cython, PyO3, others), from their release notes or the community
   tracker.

### Standard

5. **Go `context`:** the package documentation and the Go blog on cancellation and deadlines.
6. **JFR and Chrome DevTools:** starting a JFR recording and reading it; the DevTools
   Performance panel, from their own documentation.
7. **Database performance from application code:** N+1 queries, connection pools and batching,
   from the docs of a major ORM per language.
8. **Common mistakes,** including those AI coding assistants make with caching and benchmarks.
