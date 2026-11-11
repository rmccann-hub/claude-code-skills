# Error handling

Read this for deciding what to catch and where, telling "not found" from "couldn't look", exit
codes and results that say what happened, wrapping an error with its cause, retries, timeouts
and circuit breakers, an HTTP API's error responses, and error messages people read.

This module holds what every language shares; each language's syntax is in `python-coding`,
`javascript-coding`, `csharp-coding`, `powershell-scripts`, `bash-coding` and `c-coding`.
Rejecting bad input is `input-handling`'s, a setting that fails its check `configuration`'s,
and API design beyond errors the planned `api-patterns` module's. What to log is
logging-and-observability's.

## Rules

1. **Catch only what you can handle, where you can handle it:** the narrowest type, around the
   call that raises it. The rest reaches one boundary, such as `main` or a request handler,
   that reports it and fails. An error inside a validator or a check fails the check.
2. **Keep "not found" apart from "couldn't look".** A lookup has three outcomes: found, absent,
   and failed. Never infer absence from an empty result.
3. **Give each result one meaning:** one meaning per exit code, in a table the program
   documents.
4. **Record a child process's result whole:** the exit code, the signal, or "not finished" as
   its own state; the arguments as run; long output as head and tail, with a count of what was
   cut.
5. **Wrap an error with what you were doing, and keep the original as its cause.**
6. **Retry only a transient failure of idempotent work,** with capped exponential backoff and
   jitter, a deadline over all attempts, at one layer of the stack.
7. **Give every call that waits on something outside the process a timeout.**
8. **Stop calling a dependency that keeps failing:** a circuit breaker fails fast, and the
   caller degrades and says so.
9. **An HTTP API answers an error with problem details and an honest status:** 4xx when the
   request is wrong, 5xx when the server or its dependency failed.
10. **A message for a person says what happened and what to do.** The stack trace goes to the
    log, with an ID the message carries.

### Classes of failure

| Class | Example | Handled | Retry? |
|---|---|---|---|
| The caller's mistake | Bad input; a named file missing | Told to the caller | No |
| Absent | No record matches | A normal result, not an error | No |
| Transient | Timeout, reset, 503 | Close to the call | Yes, by rule 6 |
| Environment | A missing setting or permission | At startup, by `configuration` | No |
| A bug | A broken invariant | At the boundary: fail | No: fix it |

Inside a validator, catch the one parse that can fail, and make it a finding for that field.

### Results that say what happened

- **Exit codes.** POSIX `grep` is the model: 0 found, 1 nothing found, above 1 an error (fact
  `eh-posix-grep`). Shells take 126, 127 (fact `eh-posix-127`) and above 128 (fact
  `sh-signal-status`), so keep yours below 126. FreeBSD now discourages `sysexits.h` (fact
  `eh-sysexits`): borrow its numbers if they help, in your own table.
- **A child process.** Python's `returncode` is `None` until the child is reaped and negative
  for a signal (fact `eh-py-returncode`); Node gives a code or a signal, the other null (fact
  `eh-node-exit`). Store that state; never coerce it to 0 or -1.

### Wrapping and causes

- **Python:** `raise ... from err`, `add_note()`, and exception groups for several failures
  (fact `eh-py-311`).
- **JavaScript:** `new Error(message, { cause })` (fact `eh-js-cause`).
- **Go:** `%w`, several `%w` or `errors.Join` (fact `eh-go-join`); `errors.AsType` over
  `errors.As` from 1.26 (fact `eh-go-astype`).

### Retries, timeouts and circuit breakers

- **Backoff** doubles each wait up to a cap, with jitter so clients don't retry in step (fact
  `eh-aws-backoff`). Honor `Retry-After` (fact `eh-rfc9110-retry-after`).
- **Idempotent only:** a client doesn't retry a non-idempotent HTTP method on its own (fact
  `eh-rfc9110-idempotent`). A create becomes safe to retry with a key the client sends and the
  server remembers (fact `eh-aws-retry`).
- **One layer:** retries at each layer multiply (fact `eh-aws-retry`). Retry where the
  operation starts; lower layers fail fast.
- **Deadline:** a timeout per attempt and one over all, so retries can't outlast the caller.
  Node's `fetch` takes `AbortSignal.timeout` (fact `js-fetch`).
- **A library before a hand-written loop:** stamina over tenacity in Python (fact
  `eh-py-retry`), Microsoft.Extensions.Http.Resilience on Polly in .NET (fact
  `eh-dotnet-resilience`), resilience4j on the JVM.

### Problem details

RFC 9457 replaced RFC 7807 (fact `eh-rfc9457`). `status` matches the response's, and clients
don't parse `detail` (fact `eh-rfc9457-members`). A failed dependency is 5xx, never 4xx (fact
`eh-rfc9110-classes`).

```json
{
  "type": "https://example.com/problems/invalid-date",
  "title": "The date is not valid",
  "status": 422,
  "detail": "Month 13 in 2026-13-01. Use a month from 01 to 12.",
  "instance": "/bookings/7f3a"
}
```

## Mistakes

- **`except Exception: return []` around a validator.** One field of the wrong type returns no
  findings, and bad input is saved. Catch the one parse.
- **`if not rows: skip_check()`.** A failed query returns no rows too. Treat "failed" as
  unknown, never as absent.
- **`exit 1` for every failure.** The caller can't tell a stopped search from a failed read.
- **A child's missing exit code saved as 0.** A run that never finished reads as a success.
- **`raise RuntimeError(str(err))`.** The cause's type and traceback are gone. Chain it.
- **Retrying a POST, or a rejected request.** A payment goes through twice; a bad request
  fails the same way each time.
- **A stack trace in a response or a dialog.** The person can't act on it; an attacker can.
- **Citing RFC 7807, or `sysexits.h` as the standard.** Assistants still write both.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A check fails open | A broad catch in a validator or probe that returns no findings | `BLOCKER` | Catch narrowly |
| Absence from no result | An empty result read as absent, with no failure path | `BLOCKER` where it skips a check, else `DRIFT` | Three outcomes |
| Exit codes with two meanings | One code for different outcomes; no table | `DRIFT` | One meaning each, documented |
| A child's result flattened | Status defaulted to an integer; arguments or cut output lost | `GAP` | Rule 4 |
| An unsafe retry | Non-idempotent work retried; no backoff, cap or deadline | `DRIFT` | Rule 6, or a library |
| No timeout | A network or process call left to its default | `GAP` | A timeout and a deadline |
| Wrong status class | 4xx for a server failure; 200 with an error body | `DRIFT` | 5xx and problem details |
| Internals shown | A stack trace in a response or dialog | `GAP` | Message and ID; detail to the log |

## Why

### Narrow catches, and absence apart from failure

- **The advice:** catch what you can handle; keep "absent" and "failed" apart.
- **The reason:** a broad catch turns an error into the success path. In one audited
  application, a field of the wrong type made a validator return no errors, and a
  path-traversal template was saved (L16). Another skipped an extra verification pass when
  nothing matched a database. It also fired when the lookup failed, the case most in need of
  the pass (L43).
- **What it costs:** a branch per call for the failure. At the outermost boundary a broad catch
  is right: it logs and fails.

### One meaning per result

- **The advice:** document each exit code; record a child's result whole.
- **The reason:** one audited program exited 1 for both a failed read and a stopped search, and
  its consumer couldn't step its retry ladder down (L17). Another showed what a child's record
  needs, rule 4's list (L18). A default code reads "unknown" as "passed".
- **What others do:** `grep` separates none found from an error (fact `eh-posix-grep`). FreeBSD
  now discourages `sysexits.h` (fact `eh-sysexits`). The cost: a table to keep current.

### Retries under a deadline

- **The advice:** AWS's: capped exponential backoff with jitter, idempotent work only, one layer
  (facts `eh-aws-backoff`, `eh-aws-retry`), with RFC 9110 on which methods are idempotent.
- **The reason:** each retry adds load to a system that may be failing from load. Five layers
  retrying three times each put 243 times the load on the bottom one (fact `eh-aws-retry`).
- **What others do:** .NET's standard handler adds a circuit breaker and timeouts to retries,
  and can cap retries with a budget (fact `eh-dotnet-resilience`).
- **What it costs:** slower failure, and a dependency. Bulkheads and hedging weren't researched
  here: take them from the library's documentation.

### Problem details, and messages for people

- **The advice:** problem details, with 4xx and 5xx as RFC 9110 defines them; for a person,
  what went wrong and how to fix it (fact `eh-govuk`).
- **The reason:** clients decide from the class whether to retry (fact `eh-aws-retry`), and one
  shape lets one handler read every error. A person can act on "The file is over 10 MB. Choose
  a smaller one", not on `Error 0x80070057`; the ID lets support find the log entry.
- **What it costs:** a `type` URI per problem, and a message per failure a person can fix.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `eh-rfc9457` | RFC 9457 replaces RFC 7807 | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) | "This document obsoletes RFC 7807." | 2026-11-11 | 2027-05-11 |
| `eh-rfc9457-members` | `status` matches; `detail` isn't parsed | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) | "Generators MUST use the same status code in the actual HTTP response" and "Consumers SHOULD NOT parse the "detail" member for information" | 2026-11-11 | 2027-05-11 |
| `eh-rfc9110-classes` | 4xx: the client erred; 5xx: the server | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | "indicates that the client seems to have erred." and "indicates that the server is aware that it has erred" | 2026-11-11 | 2027-05-11 |
| `eh-rfc9110-idempotent` | No automatic retry of a non-idempotent method | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | "A client SHOULD NOT automatically retry a request with a non-idempotent method" | 2026-11-11 | 2027-05-11 |
| `eh-rfc9110-retry-after` | `Retry-After` says how long to wait | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | "how long the user agent ought to wait before making a follow-up request" | 2026-11-11 | 2027-05-11 |
| `eh-aws-backoff` | Capped exponential backoff, jitter | [AWS](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) | "This is called, predictably, capped exponential backoff." and "Jitter adds some amount of randomness to the backoff" | 2026-11-11 | 2027-05-11 |
| `eh-aws-retry` | Client errors aren't retried; idempotency tokens; one layer, 243x at five | [AWS](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) | "client errors should not be retried with the same request" and "explicit token-based mechanisms to provide idempotency" and "our best practice is to retry at a single point in the stack." and "increase 243x" | 2026-11-11 | 2027-05-11 |
| `eh-posix-grep` | `grep`: 0 found, 1 none, above 1 error | [POSIX grep](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html) | "No lines were selected." and "An error occurred." | 2026-11-11 | 2027-05-11 |
| `eh-posix-127` | 127 not found, 126 not executable | [POSIX shell](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) | "If the command is not found, the exit status shall be 127." and "not an executable utility, the exit status shall be 126." | 2026-11-11 | 2027-05-11 |
| `eh-sysexits` | FreeBSD discourages `sysexits.h` | [sysexits(3)](https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits) | "Its use is discouraged." and "The choice of an appropriate exit value is often ambiguous." | 2026-11-11 | 2027-05-11 |
| `eh-py-returncode` | `returncode` is `None` until the child ends | [subprocess](https://docs.python.org/3/library/subprocess.html) | "A None value indicates that the process hadn't yet terminated" | 2026-11-11 | 2027-05-11 |
| `eh-node-exit` | Node's `exit`: a code or a signal | [child_process](https://nodejs.org/api/child_process.html) | "If the process exited, code is the final exit code of the process, otherwise null." | 2026-11-11 | 2027-05-11 |
| `eh-py-311` | Python 3.11: `add_note()`, exception groups | [What's new in 3.11](https://docs.python.org/3/whatsnew/3.11.html) | "PEP 654: Exception Groups and except*" and "The add_note() method is added to BaseException." | 2026-11-11 | 2027-05-11 |
| `eh-js-cause` | `Error`'s `cause` option | [ECMA-262](https://tc39.es/ecma262/) | "It is used to create a "cause" property on obj when a "cause" property is present on options." | 2026-11-11 | 2027-05-11 |
| `eh-go-join` | Go 1.20: `errors.Join`, several `%w` | [Go 1.20](https://go.dev/doc/go1.20) | "The new function errors.Join returns an error wrapping a list of errors." | 2026-11-11 | 2027-05-11 |
| `eh-go-astype` | Go 1.26: `errors.AsType` | [Go 1.26](https://go.dev/doc/go1.26) | "The new AsType function is a generic version of As." | 2026-11-11 | 2027-02-11 |
| `eh-py-retry` | stamina 26.1.0 (2026-04-13) wraps tenacity 9.2.1 (2026-10-07) | [stamina](https://raw.githubusercontent.com/hynek/stamina/main/CHANGELOG.md), [tenacity](https://pypi.org/pypi/tenacity/json) | "Passing `timeout=0` now raises a warning since it counterintuitively disables all retries." | 2026-11-11 | 2027-02-11 |
| `eh-dotnet-resilience` | Microsoft.Extensions.Http.Resilience 11.0.0 (2026-11-10) | [README](https://raw.githubusercontent.com/dotnet/extensions/main/src/Libraries/Microsoft.Extensions.Http.Resilience/README.md), [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience) | "blocks the execution if too many direct failures or timeouts are detected" and "limits retries to a ratio of the requests sent" | 2026-11-11 | 2027-02-11 |
| `eh-govuk` | Say what went wrong and how to fix it | [GOV.UK](https://design-system.service.gov.uk/components/error-message/) | "In the error message explain what went wrong and how to fix it." | 2026-11-11 | 2027-05-11 |

## Sources

Rules are in our own words; each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| RFC 9457, RFC 9110 | Problem details, status, retries | IETF Trust: short quotes, cited |
| AWS Builder Center; POSIX.1-2024 | Retries; exit statuses | All rights reserved: short quotes |
| FreeBSD sysexits(3) | `sysexits.h` | BSD-2-Clause: quoted |
| Python, Node.js and Go docs, ECMA-262 | Causes, a child's exit | PSF 2.0; MIT; CC BY 4.0; Ecma's license: short quotes, attributed |
| stamina, tenacity, Polly, dotnet/extensions | Retry libraries | MIT, Apache-2.0, BSD-3-Clause: quoted |
| GOV.UK Design System | Messages | Open Government Licence v3.0: quoted, attributed |
| Audited repositories, unnamed (L16, L17, L18, L43) | Rules 1 to 4 | Observed practice, in our own words |
