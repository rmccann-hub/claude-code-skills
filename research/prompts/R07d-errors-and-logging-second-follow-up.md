# RESEARCH RUN R07d: Errors and logging, what R07 and R07b didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: error-handling, logging-and-observability, and the error sections of each language module.

## What this run is for

A second follow-up. R07 covered error handling for Python, Go and C#; R07b covered logging
practice, OWASP, logging-library versions, metrics, and PowerShell and Bash errors. Both are
filed and checked. This run takes what R07b listed as not covered. Don't repeat their
findings; where one has changed since, say so.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R07d · FORM: research-result v1
Save as: R07d-RESULT.md
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

- JavaScript's `Error` takes a `cause` option (ES2022), and Rust separates recoverable errors
  (`Result`, `?`) from `panic!`.
- Java distinguishes checked from unchecked exceptions, and `Throwable(String, Throwable)` keeps
  a cause; PHP's `Exception` takes `$previous`; Ruby sets `cause` automatically when raising
  inside `rescue`.
- GDPR treats an IP address as personal data in some circumstances (CJEU C-582/14, *Breyer*),
  and Article 5(1)(e) limits how long personal data is kept.
- The OpenTelemetry Logs Data Model defines numeric severities from 1 to 24.
- ASP.NET Core and Spring both produce RFC 9457 problem details out of the box.

## Questions

### Priority

1. **Error idioms for TypeScript and JavaScript, Rust, Java, PHP and Ruby,** from each
   language's own documentation: the error or exception hierarchy, keeping a cause, result
   types, what to catch and where, and the mistakes each language's docs warn against. For
   Rust, also `thiserror` and `anyhow` (versions, and when each fits).
2. **Personal data in logs:** the GDPR articles that apply (Article 4(1), 5(1)(c) and (e), 32),
   *Breyer* on IP addresses, and published regulator guidance on logging (EDPB, ICO, CNIL),
   each quoted from EUR-Lex, curia.europa.eu or the regulator.
3. **Retention and sampling:** published guidance on how long to keep application and security
   logs (OWASP's "Disposal of logs", NIST SP 800-92 and its revision, PCI DSS), and on sampling
   logs without losing errors.
4. **The OpenTelemetry Logs Data Model:** severity numbers and names, and how each listed
   library maps its levels onto them.
5. **Trace context and redaction per library:** how structlog, pino, Serilog, Logback, Log4j 2,
   Monolog and semantic_logger attach the active trace and span IDs, and each one's built-in
   redaction (pino `redact`, Serilog destructuring, Logback masking), with versions.

### Standard

6. **Error messages for people:** Microsoft's and Nielsen Norman Group's guidance, quoted.
7. **RFC 9457 in frameworks:** ASP.NET Core `ProblemDetails`, Spring `ProblemDetail`, FastAPI,
   Express and Go, with versions and defaults.
8. **Bulkheads:** primary or well-known sources (Azure Architecture Center, Nygard's *Release
   It!*), and the libraries that implement them per language.
9. **PowerShell `trap` and the information stream** (`Write-Information`, stream 6), from
   Microsoft Learn.
