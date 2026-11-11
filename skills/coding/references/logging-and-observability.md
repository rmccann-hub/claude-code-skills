# Logging and observability

Read this for deciding what a program writes to its logs and metrics: structured lines and
their fields, levels, timestamps, trace IDs, what to keep out and where to redact it, a logging
library per language, OpenTelemetry logs, SLOs and the alerts that page, and status lines and
run records that say what was checked.

Escaping text for a log line or a terminal is `input-handling`'s; what to catch, and error
messages, `error-handling`'s. Reading logs others wrote is the operations skill's
`log-analysis`, and profiling `performance-and-concurrency`'s.

## Rules

1. **Write one JSON object a line, with the same fields everywhere.** The message is fixed
   text, and the values go in fields.
2. **Give every timestamp its offset, and write UTC with `Z`** (fact `la-rfc3339`).
3. **Choose the level by who has to act.** `ERROR`: someone must. `WARN`: handled, but
   degraded. `INFO`: a line per request or business event. `DEBUG`: off in production.
4. **Put the active `trace_id` and `span_id` in every record,** from W3C Trace Context (fact
   `lo-tracecontext`). Mint no other correlation ID unless something outside needs one.
5. **Keep secrets and personal data out at the source.** Remove, mask, hash or encrypt a value
   before the record is built (fact `lo-owasp-treat`); log a salted hash of a session ID, never
   the ID (fact `lo-owasp-session`).
6. **Log through an encoder that escapes each value.** A parameterized call still passes CR and
   LF (fact `input-owasp-log`); `input-handling` holds the escaping.
7. **A status line names the outcome that was checked,** not that a step finished.
8. **Record each fact of a run once, and derive every report from that record.** Two records of
   one run agree, and an evidence bundle lists what it left out.
9. **Measure each service's rate, errors and duration, and page on symptoms:** an error budget
   burning, not a busy CPU.
10. **Take each library's version from the Facts, and give it somewhere to write.** Rust's
    `tracing` writes nothing without a subscriber (fact `lo-rust-tracing`).

### The fields

One record, wrapped here:

```json
{"timestamp": "2026-11-11T14:05:09.123Z", "level": "INFO", "event": "order.paid",
 "message": "Order paid", "service": "checkout",
 "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736", "span_id": "00f067aa0ba902b7",
 "order_id": "A-1001", "amount_cents": 4200}
```

`event` is a stable name to group on; `message` is for people. The IDs come from the active
span. A field renamed in one service breaks every query that spans them.

### What to keep out

- **Credentials:** passwords, access tokens, API keys, `Authorization` and `Cookie` headers.
- **Session IDs:** a salted hash, so one session's events still group.
- **Personal data:** OWASP asks for care, not a ban (fact `lo-owasp-treat`). Log an internal
  user ID, not a name or an email, and mask what must appear. Data protection law and retention
  periods aren't covered here.
- **Whole objects:** log named fields. A deny-list misses next month's field.

Redact in the logger's pipeline, so every sink gets the same record: a structlog processor, or
Monolog's `RedactingFormatter` (fact `lo-php-monolog`). Other libraries' redaction wasn't checked.

### Libraries

| Language | Library | Fact |
|---|---|---|
| Python | structlog | `lo-libs` |
| Node.js | pino; winston, last released 2025-12 | `lo-libs` |
| .NET | Serilog | `lo-libs` |
| Java | SLF4J with Logback, or Log4j 2 | `lo-java-libs`, `lo-log4j-cve` |
| PHP | Monolog | `lo-php-monolog` |
| Ruby | semantic_logger | `lo-libs` |
| Rust | `tracing`; a binary adds `tracing-subscriber` | `lo-rust-tracing` |

OpenTelemetry logs are stable in some SDKs only (fact `lo-otel-logs`). Where stable, bridge the
library to the SDK, which ties records to the active span (fact `lo-otel-structured`);
elsewhere, write JSON lines for the Collector to read.

### Metrics and alerts

- **Per service:** rate, errors and duration (fact `lo-red`); with saturation, the four golden
  signals (fact `lo-golden`). **Per resource:** utilization, saturation and errors (fact
  `lo-use`).
- **Set an SLO.** The error budget is 100% minus the SLO. Page at 2% of it burned in an hour or
  5% in six hours, and open a ticket for slower burns (fact `lo-slo-budget`).
- **Keep labels bounded:** a route or a status class, never a user ID or a raw URL. Each new
  value is a new series to store.
- **Prometheus:** pin the LTS on a server you don't upgrade often (fact `lo-prometheus`).
  OpenMetrics 2.0 is experimental (fact `lo-openmetrics2`): don't expose it alone.

## Mistakes

- **Values pasted into the message,** as in `f"user {uid} failed"`. Lines no longer group; keep
  the message fixed and put `uid` in a field.
- **An unkeyed hash of an email called anonymous.** Anyone can hash guesses and match them. Use
  a keyed hash, and treat the result as still personal.
- **A Rust library that installs a global subscriber,** or a binary that installs none.
- **"OK" printed because a step ran.** Print what was compared and the result.
- **Paging on CPU or memory.** Page on what users feel; put causes on a dashboard.
- **OpenTelemetry logs taken as stable in Python or JavaScript,** or Trace Context Level 2 as
  finished (facts `lo-otel-logs`, `lo-tracecontext`).

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Secrets logged | Log calls naming `password`, `Authorization`, `Cookie`, a session; objects whole | `BLOCKER` for a credential, else `GAP` | Redact in the pipeline |
| No offset | Naive `now()`, `%H:%M:%S`, local time in a log config | `DRIFT` | UTC with `Z` |
| Free text | String building in log calls; no JSON encoder | `GAP` | An encoder and fields |
| Logs apart from traces | Tracing in use, no `trace_id` in records | `GAP` | IDs from the active span |
| A status line that claims a check | "OK" after a step that compared nothing | `BLOCKER` | Name the check and result |
| One run, two stories | Two records of a run; a total computed twice | `DRIFT` | One record, the rest derived |
| Pages on causes | Pages on CPU, memory or one error | `DRIFT` | Burn-rate pages on an SLO |
| A known-bad version | Log4j below 2.26.1 or 2.25.5; Monolog below 3.12.1 | `DRIFT` | Upgrade |

## Why

### Structured lines, fields and levels

A JSON line parses without a pattern, and one field set lets a query cross services.
OpenTelemetry recommends structured logs (fact `lo-otel-structured`); the field names are our
practice. **Others:** logfmt and syslog lines are lighter. **Cost:** raw JSON is hard to read;
render it for a console in development. **Choose differently:** a command-line tool read by a
person writes plain lines to stderr, with offsets. Rule 3 is our practice: no level standard was
checked.

### Timestamps and tracing

- **Offsets (L3).** One application logged in local time and wrote its evidence bundle in UTC,
  so one event sat four hours apart in the two. RFC 3339 makes the offset part of the time
  (fact `la-rfc3339`).
- **Trace Context.** Level 1 is a Recommendation; Level 2 has been a draft since 2024 (fact
  `lo-tracecontext`), so depend on Level 1. Its IDs join logs and traces across services with
  no second scheme. **Choose differently:** keep a request ID a partner already quotes, beside
  the trace ID.

### What to keep out, and where to redact

OWASP lists data to remove, mask, hash or encrypt rather than record, and names personal data
such as names and emails as needing care (fact `lo-owasp-treat`); for sessions, a salted hash
(fact `lo-owasp-session`). Redaction at each call site is missed once; in the pipeline, it
isn't. **Cost:** a hashed ID can be matched in an incident, not read.

### Status lines and run records

- **Outcome, not completion (L49).** One audited application printed "Copy OK" and "read
  successfully" over output a checksum database showed was wrong, and readers took each as a
  verdict.
- **One record, derived reports (L19, L20).** A machine-readable record and an archival log of
  one run disagreed, and the archival one was wrong. One total was derived again, and fixed, in
  four files.
- **Say what was left out (L4).** A bundle that listed what it skipped, and each verdict's raw
  inputs, let "nothing was missing" be told from "nothing was collected".

**Cost:** a field per check, and reports rendered from data.

### Metrics and paging

The SRE book puts its effort on symptoms over causes (fact `lo-golden`): a page means users are
hurt. Burn-rate pages fire fast for an outage and later for a slow leak (fact `lo-slo-budget`).
RED fits request-driven services, USE resources. **Cost:** an SLO to agree, and enough traffic
for a rate to mean something. **Choose differently:** a batch job pages on a missed run.

### Library versions

Log4j's CVE-2026-49844 makes `MapMessage.asJson()` write invalid JSON (fact `lo-log4j-cve`);
Monolog's redaction let some secrets through before 3.12.1 (fact `lo-php-monolog`).

## Facts

Versions, dates and guidance, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `lo-otel-structured` | Structured logs recommended; an SDK ties logs to the active span | [Logs](https://opentelemetry.io/docs/concepts/signals/logs/) | "structured (recommended)" and "automatically correlate your existing logs with any active trace and span" | 2026-11-11 | 2027-05-11 |
| `lo-otel-logs` | Logs Stable in C++, .NET, Java, PHP, Rust; Go a candidate; Python, JavaScript Development | [Status](https://opentelemetry.io/status/) | "Go Stable Stable Release candidate" and "Python Stable Stable Development" and "JavaScript Stable Stable Development" | 2026-11-11 | 2027-02-11 |
| `lo-tracecontext` | Level 1 a Recommendation; Level 2 a draft | [Level 1](https://www.w3.org/TR/trace-context/), [Level 2](https://www.w3.org/TR/trace-context-2/) | "Trace Context W3C Recommendation 23 November 2021" and "Trace Context Level 2 W3C Candidate Recommendation Draft 28 March 2024" | 2026-11-11 | 2027-05-11 |
| `lo-owasp-treat` | Treat such data rather than log it; personal data needs care | [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | "should be removed, masked, sanitized, hashed, or encrypted" and "Non sensitive personal data" | 2026-11-11 | 2027-05-11 |
| `lo-owasp-session` | Log a salted hash of a session ID | [OWASP Sessions](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | "log a salted-hash of the session ID instead of the session ID itself" | 2026-11-11 | 2027-05-11 |
| `lo-libs` | structlog 26.1.0, pino 10.4.0, winston 3.19.0 (2025-12-07), Serilog 4.4.0, semantic_logger 5.2.0 | [structlog](https://pypi.org/pypi/structlog/json), [pino](https://registry.npmjs.org/pino), [winston](https://registry.npmjs.org/winston), [Serilog](https://api.nuget.org/v3-flatcontainer/serilog/index.json), [semantic_logger](https://rubygems.org/api/v1/versions/semantic_logger.json) | "26.1.0" and "10.4.0" and "3.19.0" and "4.4.0" and "5.2.0" | 2026-11-11 | 2027-02-11 |
| `lo-java-libs` | SLF4J 2.0.20; Logback 1.6.6 (2026-10-25) | [SLF4J](https://repo1.maven.org/maven2/org/slf4j/slf4j-api/maven-metadata.xml), [Logback](https://logback.qos.ch/news.html) | "2.0.20" and "2026-10-25 Release of logback version 1.6.6" | 2026-11-11 | 2027-02-11 |
| `lo-log4j-cve` | Log4j 2.26.1; CVE-2026-49844 in `log4j-api`, fixed in 2.25.5 and 2.26.1 | [Maven Central](https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/maven-metadata.xml), [Apache Logging security](https://logging.apache.org/security.html) | "2.26.1" and "non-finite floating-point values in MapMessage.asJson()" and "Versions fixed 2.25.5 and 2.26.1" | 2026-11-11 | 2027-02-11 |
| `lo-php-monolog` | Monolog 3.12.1; `RedactingFormatter`, fixed in 3.12.1 | [CHANGELOG](https://raw.githubusercontent.com/Seldaek/monolog/main/CHANGELOG.md) | "3.12.1 (2026-09-29)" and "Added `RedactingFormatter`" and "Fixed `RedactingFormatter` letting secrets containing" | 2026-11-11 | 2027-02-11 |
| `lo-rust-tracing` | tracing 0.1.44, tracing-subscriber 0.3.23; `tracing` has no subscriber | [tracing](https://docs.rs/tracing/latest/tracing/), [crates.io](https://crates.io/api/v1/crates/tracing-subscriber) | "0.1.44" and "This library does not contain any Subscriber implementations" and "0.3.23" | 2026-11-11 | 2027-02-11 |
| `lo-red` | RED: rate, errors, duration | [The RED Method](https://grafana.com/blog/the-red-method-how-to-instrument-your-services/) | "Rate (the number of requests per second)" and "Duration (the amount of time those requests take)" | 2026-11-11 | 2027-05-11 |
| `lo-use` | USE: utilization, saturation, errors | [The USE Method](https://www.brendangregg.com/usemethod.html) | "For every resource, check utilization, saturation, and errors." | 2026-11-11 | 2027-05-11 |
| `lo-golden` | Four golden signals; symptoms over causes | [SRE book, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | "The four golden signals of monitoring are latency, traffic, errors, and saturation." and "much more effort on catching symptoms than causes" | 2026-11-11 | 2027-05-11 |
| `lo-slo-budget` | Budget is 100% minus the SLO; page at 2% in 1 h or 5% in 6 h | [Implementing SLOs](https://sre.google/workbook/implementing-slos/), [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) | "the error budget is 100% minus the SLO." and "We recommend 2% budget consumption in one hour and 5% budget consumption in six hours" | 2026-11-11 | 2027-05-11 |
| `lo-prometheus` | Prometheus 3.16.0 (2026-11-04) current; 3.13 the LTS to 2027-07-31 | [Download](https://prometheus.io/download/), [Release cycle](https://prometheus.io/docs/introduction/release-cycle/) | "3.16.0 / 2026-11-04" and "Prometheus 3.13 2026-07-01 2027-07-31 Supported" | 2026-11-11 | 2027-02-11 |
| `lo-openmetrics2` | OpenMetrics 2.0 is an experimental release candidate | [OpenMetrics 2.0](https://prometheus.io/docs/specs/om/open_metrics_spec_2_0/) | "Version: 2.0.0-rc1" and "Status: Experimental" | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OpenTelemetry](https://opentelemetry.io/docs/), [W3C Trace Context](https://www.w3.org/TR/trace-context/) | Logs, SDK status, trace IDs | CC BY 4.0; W3C permissive document license: quoted |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | What to keep out | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| [Google SRE book and Workbook](https://sre.google/) | Signals, error budgets, paging | CC BY-NC-ND 4.0: brief quotes, never adapted |
| Brendan Gregg (USE), Grafana Labs (RED) | Metrics per resource and service | No license stated: brief quotes |
| [Prometheus docs](https://prometheus.io/docs/) | Releases, LTS, OpenMetrics 2.0 | Apache-2.0: facts with short quotes |
| Registries, changelogs, Apache Logging security | Versions, fixes | Facts with short quotes |
| Audited repositories of this skill's owner, unnamed | L3, L4, L19, L20, L49 | Observed practice, our own words |
