# RESEARCH RUN R07b: Logging, observability, metrics, and error handling in the remaining languages

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: logging-and-observability, error-handling (per-language idioms).

## What this run is for

A follow-up to R07 (filed 11 November 2026), which covered error handling for Python, Go and C#,
resilience libraries, RFC 9457, exit codes, timestamps and Windows log tools, and listed the rest
as not covered. This run supplies what a planned `logging-and-observability` module needs, and
the per-language error idioms the shipped `error-handling` module leaves to each language. Don't
repeat R07's findings; where one has changed since, say so.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R07b · FORM: research-result v1
Save as: R07b-RESULT.md
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

- W3C Trace Context (traceparent, tracestate) is a W3C Recommendation, and Level 2 is in progress.
- OWASP's Logging Cheat Sheet says what never to log (secrets, session IDs, personal data) and how
  to stop log injection (encode CR, LF and delimiters).
- OpenTelemetry logs are Stable in C++, .NET, Java, PHP and Rust, a release candidate in Go, and in
  development in Python and JavaScript (R07, read 11 November 2026).
- The RED method (rate, errors, duration) suits request-driven services and the USE method
  (utilization, saturation, errors) suits resources; the Google SRE books define SLOs and error
  budgets.
- Prometheus 3.x is current, and OpenMetrics' text format is being folded into Prometheus.

## Questions

### Priority

1. **Logging practice:** structured logging (JSON lines, a stable field set), log levels and what
   each is for, correlation IDs, W3C Trace Context in logs, sampling, and retention. Cite each
   source.
2. **What never to log, and log injection:** OWASP's guidance, personal-data rules that apply to
   logs (GDPR's position on logs as personal data, with sources), redaction at the source, and
   the encoding that stops forged log lines.
3. **Logging libraries per language,** each with its current version and release date, its
   structured-logging API, and how it attaches trace context: Python `logging` and structlog;
   Node.js pino and winston; .NET `Microsoft.Extensions.Logging` and Serilog; Go `log/slog`; Rust
   `tracing`; Java SLF4J with Logback or Log4j 2; PHP Monolog; Ruby `Logger` and semantic_logger;
   PowerShell's own streams and `Write-Information`.
4. **Error handling idioms for TypeScript and JavaScript, PowerShell, Rust, Java, PHP, Ruby and
   Bash,** from each language's documentation: exception or error design, wrapping and causes,
   result types, and what to catch where. For PowerShell: terminating against non-terminating
   errors, `-ErrorAction Stop`, `$ErrorActionPreference`, `try`/`catch`/`trap`. For Bash:
   `set -e` and its documented exceptions, `pipefail`, `trap ... ERR`.
5. **Metrics and alerting:** the RED and USE methods with their original sources, SLOs and error
   budgets (Google SRE books), alerting on symptoms against causes, and Prometheus and OpenMetrics
   status today, with versions.

### Standard

6. **Error messages for people:** Microsoft's and Nielsen Norman Group's guidance on error
   messages, with quotes (GOV.UK's was checked in R07's intake).
7. **RFC 9457 in frameworks:** ASP.NET Core `ProblemDetails`, Spring `ProblemDetail`, and the
   equivalents in FastAPI, Express and Go, with versions.
8. **Idempotency keys and bulkheads:** the IETF Idempotency-Key draft's status, and published
   sources for the bulkhead pattern.
9. **Common mistakes,** including those AI coding assistants make with logging and errors, with
   sources.
