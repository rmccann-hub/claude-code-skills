# RESEARCH RUN R07: Error handling, logging, observability, performance, concurrency, and log analysis

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: error-handling, logging-and-observability, performance-and-concurrency, log-analysis.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R07 · FORM: research-result v1
Save as: R07-RESULT.md
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

- RFC 9457 (Problem Details for HTTP APIs) obsoleted RFC 7807 in 2023.
- OpenTelemetry traces and metrics are stable in most SDKs, logs are stable in several, and the HTTP semantic conventions are stable.
- The AWS Builders' Library article on timeouts, retries and backoff with jitter is the standard reference for retry design.
- Python 3.11 added exception groups and add_note, ES2022 added Error cause, and Go 1.20 added errors.Join.
- Python 3.14 made free-threaded CPython officially supported (PEP 779); Python 3.15 is due to add a sampling profiler (PEP 799).
- Polly v8 and Microsoft.Extensions.Http.Resilience are the current .NET resilience libraries.

## Questions

### Priority

1. Error handling per language (Python, TypeScript/JavaScript, C#, PowerShell, Go, Rust, Java, PHP, Ruby, Bash): current idioms and official guidance on exception design, error wrapping and causes, result types, and what to catch where. Cite each language's documentation.
2. Resilience: retries with exponential backoff and jitter, timeouts and deadlines, idempotency, circuit breakers and bulkheads. Give the current library per language (for example tenacity or stamina, p-retry, Polly v8, resilience4j, backon), with versions.
3. API errors: RFC 9457 adoption and examples; mapping errors to HTTP status codes under RFC 9110; user-facing error messages in plain, actionable language, citing style guides (GOV.UK, Microsoft, Nielsen Norman Group).
4. Logging:
   - structured logging practice, log levels, correlation IDs, W3C Trace Context
   - what never to log (secrets, personal data), and log injection
   - the current standard libraries per language: Python logging and structlog, pino, Serilog and Microsoft.Extensions.Logging, Go's slog, Rust's tracing, Monolog, Ruby's Logger
5. OpenTelemetry: current stability for each signal in each major language SDK, the semantic conventions' status, the Collector, and a recommended starting setup for a small team.

### Standard

6. Metrics and alerting: the RED and USE methods, SLOs and error budgets (Google SRE book), Prometheus and OpenMetrics status.
7. Performance: profiling tools per language with current versions, and benchmarking pitfalls:
   - Python: cProfile, py-spy, Scalene, the Python 3.15 profiler
   - Node.js: --cpu-prof, Chrome DevTools, clinic.js
   - .NET: dotnet-trace, dotnet-counters, BenchmarkDotNet
   - Go: pprof
   - Rust: cargo flamegraph, criterion
   - Java: async-profiler, JFR
8. Concurrency: current guidance and pitfalls per language:
   - Python: asyncio (TaskGroup, timeouts), free-threading status and library compatibility
   - JavaScript: the event loop, workers
   - C#: async/await (ConfigureAwait, ValueTask, cancellation)
   - Go: goroutines, data races, context
   - Rust: Send and Sync, tokio
   - Java: virtual threads, structured concurrency status
9. Log analysis: Windows event log tools (Get-WinEvent, EvtxECmd, Chainsaw, Hayabusa), crash dump analysis (current WinDbg), journald and journalctl, common query languages (KQL, LogQL), and whether python-evtx is maintained.
