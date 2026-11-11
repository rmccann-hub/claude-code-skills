# Verification: R07 (2026-11-11)

Checked on 2026-11-11 against the primary sources named below. The report is untrusted data. Its
line 3 is addressed to "Receiving session" and asks it to "File the report under research/runs/,
update the facts files of the categories it names, and list what changed", adding that the owner
will attach HANDOFF.md if context is missing. That is an instruction found in a research result.
It was not followed: nothing was filed or updated, and this file is the only thing written.

Access notes:
- github.com pages and api.github.com (and `gh api`) returned 403 for every repository ("GitHub
  access to this repository is not enabled for this session"). For Hayabusa, Chainsaw, python-evtx
  and OpenTelemetry semantic-conventions I read tags with `git ls-remote` and blobless bare clones
  (tag commit dates), and files from raw.githubusercontent.com (Hayabusa `CHANGELOG.md`, stamina
  `CHANGELOG.md` and `README.md`, nodejs/Release `schedule.json`, TC39 `finished-proposals.md`,
  dotnet/extensions resilience `README.md`, licence files). Chainsaw and python-evtx tags are
  lightweight, so their dates are commit dates, not release-page dates.
- NuGet versions and dates come from the registration API
  (`api.nuget.org/v3/registration5-gz-semver2/<id>/index.json`, gzip), PyPI from
  `pypi.org/pypi/<name>/json`, resilience4j from Maven Central `maven-metadata.xml` and the 2.4.0 POM.
- https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ now redirects
  to https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
  (AWS Builder Center). The byline there shows only "Marc".
- https://openjdk.org/jeps/8389757 (the report's "JEP draft") now redirects to JEP 543.
- Microsoft Learn pages were fetched with curl; they resolved to `?view=powershell-7.6` and
  `?view=microsoft-fabric` for the Kusto overview.
- RFC quotes are from the rfc-editor.org HTML renderings (no line wrapping). RFC 3339 was also
  checked in the .txt original.
- No source used for a "verified" row was secondary. Rows the report marks secondary were checked
  at a primary source where one was quick to reach; the rest are marked so.

| Claim | Status | Checked against |
|---|---|---|
| Python 3.15.0 final on 2026-10-09 (F1, C2) | verified | [PEP 790](https://peps.python.org/pep-0790/) |
| 3.15.0 was planned for 1 October | unverifiable: today's PEP 790 lists only the actual dates | [PEP 790](https://peps.python.org/pep-0790/) |
| 3.15.2 on 2026-10-26; source-only security fixes until October 2031 (F2, F3) | verified. The PEP also lists 3.15.1 on 2026-10-21, which the report omits; 3.15.3 is expected 2026-12-01 | [PEP 790](https://peps.python.org/pep-0790/) |
| PEP 799 adds a `profiling` package; `profiling.sampling` is Tachyon; `profiling.tracing` relocates cProfile, which stays an alias; `profile` removed in 3.17 (F4, F5, C2) | verified. PEP 799 is Final, Python-Version 3.15 | [What's new in 3.15](https://docs.python.org/3.15/whatsnew/3.15.html), [PEP 799](https://peps.python.org/pep-0799/) |
| Tachyon: "up to 1,000,000 Hz"; `run -m`; attach by PID, `dump` with `--async-aware`, wall/CPU/GIL modes (last three marked secondary in the report) | verified (at the primary source): attach, run, run -m and dump are listed, and `--mode wall` (default), `--mode cpu`, `--mode gil` | [What's new in 3.15](https://docs.python.org/3.15/whatsnew/3.15.html) |
| Free-threaded CPython officially supported but optional from 3.14 (C5, F6) | verified | [What's new in 3.14](https://docs.python.org/3/whatsnew/3.14.html) |
| OpenTelemetry per-language status table (C1, 4.7) | verified: every cell matches, including Rust traces Beta, Go logs Release candidate, Java profiles Development | [OpenTelemetry status](https://opentelemetry.io/status/) |
| Collector status "mixed" (F8) | verified | [OpenTelemetry status](https://opentelemetry.io/status/) |
| Logs specification: Bridge API, SDK and Protocol stable (F7) | verified | [Specification status](https://opentelemetry.io/docs/specs/status/) |
| HTTP semantic conventions stable at v1.23.0, November 2023 (F9) | verified; the post is dated Monday, November 06, 2023 | [OTel blog](https://opentelemetry.io/blog/2023/http-conventions-declared-stable/) |
| `OTEL_SEMCONV_STABILITY_OPT_IN` with `http` and `http/dup` (F10) | verified | [HTTP migration](https://opentelemetry.io/docs/specs/semconv/non-normative/http-migration/) |
| OTel logs concept: automatic log-trace correlation; "Structured logs are preferred in production" | verified (the second quote continues "because their stable schema makes them straightforward to validate, parse, correlate...") | [Logs](https://opentelemetry.io/docs/concepts/signals/logs/) |
| Semantic Conventions v1.44.0 (4 Aug 2026) is latest | contradicted: v1.45.0 was tagged 2026-11-01; v1.44.0's tag commit is 2026-08-04 | `git ls-remote` and tag dates of open-telemetry/semantic-conventions |
| 2026 OTel blog titles | verified with a correction: "Announcing the OpenTelemetry JavaScript SDK 3.0" (2026-11-05), "OpenTelemetry Transformation Language reaches v1" (2026-10-27), "Deprecating Span Events API" and "OTel Go Logs API and SDK reach RC" appear on the 2026 index; "Declarative configuration is stable!", "OpenTelemetry Profiles Enters Public Alpha" and "OpenTelemetry is a CNCF Graduated Project" were not found there (the index shows "Declarative Config Stabilized") | [OTel blog 2026](https://opentelemetry.io/blog/2026/) |
| Specification at 1.62.0 (site navigation) | unverifiable: not checked in this pass | n/a |
| RFC 9457 (July 2023, Standards Track, Nottingham, Wilde, Dalal) obsoletes RFC 7807 (C4, F24) | verified | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| `application/problem+json`; `application/problem+xml` in Appendix B (F25) | verified | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| Members: `type` defaults to "about:blank"; `title` stable except for localisation; `status` only advisory and MUST match; consumers SHOULD NOT parse `detail`; `instance` identifies the occurrence | verified | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| "Clients consuming problem details MUST ignore any such extensions that they don't recognize." | verified with a correction: the sentence ends with a semicolon, not a full stop: "...that they don't recognize; this allows problem types to evolve and include additional information in the future." | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| Problem details "most naturally fit the semantics of 4xx and 5xx responses" | verified | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| RFC 9110 4xx and 5xx definitions; invalid status code treated as 5xx (F26, F27) | verified (RFC 9110, June 2022, STD 97) | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) |
| RFC 3339: `time-offset = "Z" / time-numoffset`; `full-time = partial-time time-offset` (F28) | verified | [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) |
| RFC 3339: "-00:00" means UTC known, local offset unknown, unlike "Z" or "+00:00" | verified (section 4.3) | [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) |
| RFC 3339: unqualified local time "deemed unacceptable for the Internet"; generators "SHOULD use upper case letters" | verified | [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) |
| FreeBSD sysexits(3): deprecated, "Its use is discouraged", page dated 9 May 2024 (C8, F29) | verified. The page is the FreeBSD 15.1 rendering; NAME reads "sysexits -- legacy exit status codes for system programs" | [sysexits(3)](https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits) |
| sysexits values 64, 65, 66, 69, 70, 75, 78; EX_UNAVAILABLE "catchall"; "often ambiguous" | verified. EX_OK is defined in prose ("a status of 0, or EX_OK"), not as "EX_OK (0)" | [sysexits(3)](https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits) |
| The FreeBSD 4.3 page recommended sysexits | verified: "sysexits - preferable exit codes for programs" and "the pre-defined exit codes from sysexits should be used" | [sysexits, FreeBSD 4.3](https://man.freebsd.org/cgi/man.cgi?query=sysexits&manpath=FreeBSD+4.3-RELEASE) |
| Go 1.26 added `errors.AsType` (F14, marked secondary) | verified (at the primary source). The release notes say "The new AsType function is a generic version of As." The package docs mark it "added in go1.26.0", signature `func AsType[E error](err error) (E, bool)`, and the `As` docs say "For most uses, prefer AsType." Go 1.26.0 was released 2026-02-10 | [Go 1.26 release notes](https://go.dev/doc/go1.26), [errors package](https://pkg.go.dev/errors@go1.27.4), [release history](https://go.dev/doc/devel/release) |
| `errors.As` panics on a bad target, which `AsType` avoids (secondary in the report) | verified (the panic): "As panics if target is not a non-nil pointer to either a type that implements error, or to any interface type." "Compile-time error" is inferred from the type parameter `E error`, not stated | [errors package](https://pkg.go.dev/errors@go1.27.4) |
| Go 1.20: `errors.Join`; multiple `%w` in `fmt.Errorf` (C6) | verified; Go 1.20 released 2023-02-01 | [Go 1.20 release notes](https://go.dev/doc/go1.20), [release history](https://go.dev/doc/devel/release) |
| Go 1.26 added `slog.NewMultiHandler` (secondary in the report) | verified (at the primary source) | [Go 1.26 release notes](https://go.dev/doc/go1.26) |
| Go 1.27 released 19 August 2026 (F15) | verified (blog by Nicholas Husin; release history "go1.27.0 (released 2026-08-19)"; go1.27.4 on 2026-11-10) | [Go 1.27 blog](https://go.dev/blog/go1.27), [release history](https://go.dev/doc/devel/release) |
| Go 1.27: generic methods; `encoding/json` on the v2 implementation; goroutine leak profile GA; small allocations "by up to 30%"; `asynctimerchan` and `gotypesalias` GODEBUG removed (secondary in the report) | verified (at the primary source). The crypto/tls GODEBUG removals were not checked | [Go 1.27 release notes](https://go.dev/doc/go1.27) |
| Python 3.11: PEP 654 and PEP 678 headings; "The add_note() method is added to BaseException."; released 24 Oct 2022 (C6) | verified | [What's New In Python 3.11](https://docs.python.org/3/whatsnew/3.11.html) |
| PEP 678 `.add_note(note: str)`; TypeError for non-strings | verified (Final, Python-Version 3.11) | [PEP 678](https://peps.python.org/pep-0678/) |
| PEP 654 exception groups and `except*` | verified (Final, Python-Version 3.11) | [PEP 654](https://peps.python.org/pep-0654/) |
| ES2022 Error cause: author Chengzhong Wu, stage 4 in October 2021, publication 2022 (C6) | verified: finished proposals list "Error Cause", author Chengzhong Wu, champions Chengzhong Wu and Hemanth HM, latest meeting notes 2021-10, expected publication year 2022 | [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) (read via raw.githubusercontent.com) |
| AWS "Timeouts, retries, and backoff with jitter", Marc Brooker, 2019; "capped exponential backoff"; jitter quote (C7) | verified with a correction: the URL now redirects to AWS Builder Center, which shows the byline "Marc" only and "Published Dec 5, 2019". Both quotes are present; the first reads "This is called, predictably, capped exponential backoff." It also says "a best practice is designing APIs to be idempotent" | [Builder Center article](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) |
| .NET 8 and .NET 9 end of support 10 Nov 2026 (F13, C3) | verified (post by Rahul Bhandari, dated June 29th, 2026). The policy page now lists both as out of support at 8.0.34 and 9.0.23 | [.NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/), [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) |
| .NET 10 LTS supported until 14 Nov 2028 | verified at the policy page (the blog says only "November 2028") | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) |
| .NET 11 shipped 10 Nov 2026 as STS (secondary in the report) | verified (at the primary source): ".NET 11 November 10, 2026 11.0.0 ... STS Active November 14, 2028". Runtime async and C# 15 union types: secondary only, not checked | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core), [releases-index.json](https://raw.githubusercontent.com/dotnet/core/main/release-notes/releases-index.json) |
| PowerShell 7.4 and 7.5 end of support 10 Nov 2026; successor 7.6 LTS (marked secondary) | verified at Microsoft's lifecycle page: 7.5 "10-Nov-2026", 7.4 (LTS) "10-Nov-2026", 7.6 (LTS) released 18-Mar-2026, ends 14-Nov-2028; "follows the support lifecycle of .NET" | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle) |
| Polly and Polly.Core 8.9.1, 7 Nov 2026, BSD-3-Clause (F11) | verified (published 2026-11-07T16:16Z; licenseExpression BSD-3-Clause) | NuGet registration API ([Polly](https://www.nuget.org/packages/Polly), [Polly.Core](https://www.nuget.org/packages/Polly.Core)) |
| Microsoft.Extensions.Http.Resilience 10.11.0 is latest, 14 Oct 2026 (F12, C3) | contradicted: **11.0.0 was published 2026-11-10T23:50Z** (MIT). 10.11.0's date (2026-10-14T05:01Z) is right. The major version now tracks .NET 11, not 10 | NuGet registration API ([package](https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience)) |
| Resilience README: "built on the Polly framework"; total request timeout; circuit breaker quotes (from a BaGet mirror in the report) | verified at the primary README. NuGet's own description reads only "Resilience mechanisms for HttpClient." | [dotnet/extensions README](https://github.com/dotnet/extensions/blob/main/src/Libraries/Microsoft.Extensions.Http.Resilience/README.md) (raw) |
| tenacity 9.2.1, 7 Oct 2026, Apache-2.0 (F17) | verified (upload 2026-10-07T12:13Z; license_expression Apache-2.0) | [PyPI JSON](https://pypi.org/pypi/tenacity/json) |
| stamina 26.1.0, 13 Apr 2026, MIT (F18) | verified (upload 2026-04-13T17:44Z; license_expression MIT) | [PyPI JSON](https://pypi.org/pypi/stamina/json) |
| stamina warns on `timeout=0` from 26.1.0 (report cites a secondary mirror) | verified in stamina's own changelog, under "26.1.0 - 2026-04-13" | [stamina CHANGELOG](https://github.com/hynek/stamina/blob/main/CHANGELOG.md) (raw) |
| stamina is an "opinionated wrapper around the great-but-unopinionated Tenacity package" | verified | [stamina README](https://github.com/hynek/stamina/blob/main/README.md) (raw) |
| resilience4j 2.4.0, 14 Mar 2026, Apache-2.0 (F19) | verified (Maven metadata `<release>2.4.0`, lastUpdated 20260314141719; POM licence Apache-2.0). The "JDK 17 to 21" note: secondary only, not checked | [Maven Central](https://repo1.maven.org/maven2/io/github/resilience4j/resilience4j-retry/maven-metadata.xml) |
| JEP 533: seventh preview in JDK 27, adding a type parameter for join()'s exception (F16) | verified: JEP 533 "Closed / Delivered", Release 27 | [JEP 533](https://openjdk.org/jeps/533), [JEP 543](https://openjdk.org/jeps/543) |
| JDK 27 changes: third type parameter; default joiner throws `ExecutionException`; `FailedException` and `TimeoutException` removed | verified with a correction: JEP 533 confirms the third type parameter `R_X` and that `allSuccessfulOrThrow()`, `anySuccessfulOrThrow()` and `awaitAllSuccessfulOrThrow()` joiners throw `ExecutionException`. It does not mention removing `FailedException` or `TimeoutException` (secondary only); it says `awaitAll()` was removed and `onTimeout()` replaced by `timeout()`, with `CancelledByTimeoutException` as the cause | [JEP 533](https://openjdk.org/jeps/533) |
| JEP 543 proposes finalising in JDK 28 without change; "still a proposal" | verified with a correction: JEP 543's status is now **"Integrated", Release 28** (updated 2026/10/17). It reads "We here propose to finalize Structured Concurrency in JDK 28, without further change." | [JEP 543](https://openjdk.org/jeps/543) |
| Node 26 LTS on 2026-10-28, end of life 2029-04-30 | verified | [nodejs/Release schedule.json](https://github.com/nodejs/Release/blob/main/schedule.json) (raw) |
| Node 22 end of life 2027-04-30 (F30, cited secondary) | verified (at the primary source; `"end": "2027-04-30"`; README: Maintenance LTS) | [nodejs/Release schedule.json](https://github.com/nodejs/Release/blob/main/schedule.json) (raw) |
| Node 27 in April 2027 (secondary) | verified, with the exact dates: alpha 2026-10-28, `"start": "2027-04-22"`, LTS 2027-10-20, end 2030-04-30 | [nodejs/Release schedule.json](https://github.com/nodejs/Release/blob/main/schedule.json) (raw) |
| Hayabusa v4.3.1 (29 Oct 2026) is latest (F20) | contradicted: **v4.4.0 "CODE BLUE Release" is dated 2026/11/10** and is the newest tag. v4.3.1's date (2026/10/29, "Vulnpocalypse Release") is right | [Hayabusa CHANGELOG](https://github.com/Yamato-Security/hayabusa/blob/main/CHANGELOG.md) (raw), `git ls-remote` |
| Hayabusa v4.2.0 (12 Oct), v4.3.0 (28 Oct) | verified | [Hayabusa CHANGELOG](https://github.com/Yamato-Security/hayabusa/blob/main/CHANGELOG.md) |
| Hayabusa v4.1.0 merged `csv-timeline` and `json-timeline` into `dfir-timeline -t csv/json/jsonl` | contradicted on the version: **the merge is in 4.0.0 [2026/07/29]**, not 4.1.0 | [Hayabusa CHANGELOG](https://github.com/Yamato-Security/hayabusa/blob/main/CHANGELOG.md) |
| Hayabusa v4.1.0 fixed the histogram axis that "disagreed with every other timestamp in the same output by the host's UTC offset" | verified (4.1.0 [2026/09/12], #1914). 4.3.0 also added `-Z, --timezone <OFFSET>` | [Hayabusa CHANGELOG](https://github.com/Yamato-Security/hayabusa/blob/main/CHANGELOG.md) |
| Chainsaw latest v2.16.5, date not found; v2.16.3 on 4 Aug 2026 (F21) | contradicted: **the newest tag is v2.17.1 (commit 2026-10-14)**, after v2.17.0 the same day (Sigma `windash` and `i` modifiers, Sigma regex fixes). v2.16.5 is 2026-08-25 and v2.16.3 is 2026-08-04 (commit dates). Release pages could not be read | `git ls-remote` and a blobless clone of WithSecureLabs/chainsaw |
| Chainsaw v2.16.0 added "an EVTX summary command" | verified with a correction: the commit is "feat: add analyse evtx subcommand for per-Event-ID summary stats (#231)" (tag 2026-05-09) | blobless clone of WithSecureLabs/chainsaw |
| Chainsaw v2.16.3 fixed SRUM parsing | unverifiable: no matching commit message between v2.16.2 and v2.16.3, and the release page returned 403 | blobless clone of WithSecureLabs/chainsaw |
| WinDbg 1.2611.4001.0 is latest (F22) | verified (first entry on the page) | [WinDbg release notes](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes) |
| 1.2611.4001.0 "introduces AI-assisted debugging with WinDbg MCP" | contradicted on the version: **the MCP feature is under 1.2610.1001.0**. 1.2611.4001.0 adds `host.currentStack` and `host.currentRegisters` for JavaScript scripts | [WinDbg release notes](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes) |
| WinDbg released 5 Nov 2026 | unverifiable: the release notes and the winget manifest give no date; only Wikipedia has one | [WinDbg release notes](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes) |
| python-evtx v0.8.1, year unknown (F23) | verified with a correction (the year): **PyPI upload 2025-05-02T08:24Z**; tag commit 2025-05-02; commits "migrate to pyproject.toml", "ci: use uv and just", "ci: publish via trusted-publishing" | [PyPI JSON](https://pypi.org/pypi/python-evtx/json), blobless clone |
| python-evtx minimum Python 3.8; last push about 8 months ago (secondary) | contradicted: PyPI `requires_python` is `>=3.9`; the default branch's last commit is 2026-10-06 (merge of PR #100) | [PyPI JSON](https://pypi.org/pypi/python-evtx/json), blobless clone |
| python-evtx is Apache-2.0 | verified (PyPI license_expression; `LICENSE.TXT`) | [PyPI JSON](https://pypi.org/pypi/python-evtx/json) |
| Get-WinEvent `-FilterHashtable`, `-MaxEvents`, newest-first order | verified, added at intake | [Get-WinEvent](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent) |
| journalctl `--since`/`--until`, `-u`, `-p`, `-b`, `-o json`, `short-iso`, `--utc` | verified, added at intake (page is systemd 262) | [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) |
| KQL defining sentence | verified, added at intake | [Kusto Query Language overview](https://learn.microsoft.com/en-us/kusto/query/) |
| LogQL defining sentence | verified, added at intake | [LogQL](https://grafana.com/docs/loki/latest/query/) |

Counts: 55 verified (4 of them added at intake), 7 verified with a correction, 7 contradicted,
4 unverifiable, 0 secondary only. Several report rows marked secondary are now verified at a
primary source: errors.AsType, slog.NewMultiHandler, Go 1.27 details, Node 22, Node 27,
PowerShell 7.4/7.5, .NET 11 GA and the stamina `timeout=0` change.

## Exact quotes for facts rows

Copied from the tag-stripped page text; straight quotes unless noted.

| Fact | URL | Quote |
|---|---|---|
| RFC 9457 obsoletes 7807 | https://www.rfc-editor.org/rfc/rfc9457.html | "This document obsoletes RFC 7807." |
| Problem details media type | https://www.rfc-editor.org/rfc/rfc9457.html | "that format is identified with the "application/problem+json" media type." |
| `type` defaults to about:blank | https://www.rfc-editor.org/rfc/rfc9457.html | "When this member is not present, its value is assumed to be "about:blank"." |
| `title` is stable | https://www.rfc-editor.org/rfc/rfc9457.html | "It SHOULD NOT change from occurrence to occurrence of the problem, except for localization" |
| `status` matches the response | https://www.rfc-editor.org/rfc/rfc9457.html | "Generators MUST use the same status code in the actual HTTP response" |
| Don't parse `detail` | https://www.rfc-editor.org/rfc/rfc9457.html | "Consumers SHOULD NOT parse the "detail" member for information" |
| Ignore unknown extensions | https://www.rfc-editor.org/rfc/rfc9457.html | "Clients consuming problem details MUST ignore any such extensions that they don't recognize" |
| Problem details fit 4xx and 5xx | https://www.rfc-editor.org/rfc/rfc9457.html | "Problem details can be used with any HTTP status code, but they most naturally fit the semantics of 4xx and 5xx responses." |
| 4xx means the client erred | https://www.rfc-editor.org/rfc/rfc9110.html | "The 4xx (Client Error) class of status code indicates that the client seems to have erred." |
| 5xx means the server erred | https://www.rfc-editor.org/rfc/rfc9110.html | "The 5xx (Server Error) class of status code indicates that the server is aware that it has erred or is incapable of performing the requested method." |
| Unknown status code is treated as 5xx | https://www.rfc-editor.org/rfc/rfc9110.html | "SHOULD process the response as if it had a 5xx (Server Error) status code." |
| RFC 3339 offset grammar | https://www.rfc-editor.org/rfc/rfc3339.html | "time-offset = "Z" / time-numoffset" |
| RFC 3339 offset is required | https://www.rfc-editor.org/rfc/rfc3339.html | "full-time = partial-time time-offset" |
| -00:00 means local offset unknown | https://www.rfc-editor.org/rfc/rfc3339.html | "If the time in UTC is known, but the offset to local time is unknown, this can be represented with an offset of "-00:00"." |
| -00:00 differs from Z | https://www.rfc-editor.org/rfc/rfc3339.html | "This differs semantically from an offset of "Z" or "+00:00", which imply that UTC is the preferred reference point for the specified time." |
| Unqualified local time rejected | https://www.rfc-editor.org/rfc/rfc3339.html | "the interoperability problems of unqualified local time are deemed unacceptable for the Internet." |
| Upper case T and Z | https://www.rfc-editor.org/rfc/rfc3339.html | "Applications that generate this format SHOULD use upper case letters." |
| sysexits deprecated (FreeBSD) | https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits | "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." |
| sysexits codes are ambiguous | https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits | "The choice of an appropriate exit value is often ambiguous." |
| EX_UNAVAILABLE is a catchall | https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits | "This can also be used as a catchall message when something you wanted to do does not work, but you do not know why." |
| EX_TEMPFAIL means retry later | https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits | "the request should be reattempted later" |
| Go 1.26 adds errors.AsType | https://go.dev/doc/go1.26 | "The new AsType function is a generic version of As. It is type-safe, faster, and, in most cases, easier to use." |
| Prefer AsType | https://pkg.go.dev/errors | "For most uses, prefer AsType." |
| errors.As can panic | https://pkg.go.dev/errors | "As panics if target is not a non-nil pointer to either a type that implements error, or to any interface type." |
| Go 1.20 errors.Join | https://go.dev/doc/go1.20 | "The new function errors.Join returns an error wrapping a list of errors." |
| Go 1.20 multiple %w | https://go.dev/doc/go1.20 | "The fmt.Errorf function now supports multiple occurrences of the %w format verb" |
| Go 1.26 slog multi-handler | https://go.dev/doc/go1.26 | "The NewMultiHandler function creates a MultiHandler that invokes all the given Handlers." |
| Go 1.27 json on v2 | https://go.dev/doc/go1.27 | "The encoding/json package is now backed by the v2 implementation." |
| Go 1.27 release date | https://go.dev/doc/devel/release | "go1.27.0 (released 2026-08-19)" |
| PEP 678 add_note | https://peps.python.org/pep-0678/ | "BaseException gains a new method .add_note(note: str)." |
| add_note rejects non-strings | https://peps.python.org/pep-0678/ | "If note is not a string, .add_note() raises TypeError." |
| 3.11 add_note | https://docs.python.org/3/whatsnew/3.11.html | "The add_note() method is added to BaseException." |
| PEP 654 ExceptionGroup | https://peps.python.org/pep-0654/ | "A new standard exception type, the ExceptionGroup, which represents a group of unrelated exceptions being propagated together." |
| ES2022 Error cause | https://github.com/tc39/proposals/blob/main/finished-proposals.md | "[Error Cause][error-cause]" row: author "Chengzhong Wu", Expected Publication Year "2022" (a table, not a sentence) |
| Capped exponential backoff | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter | "This is called, predictably, capped exponential backoff." |
| Jitter | same | "Jitter adds some amount of randomness to the backoff to spread the retries around in time." |
| Idempotent APIs | same | "a best practice is designing APIs to be idempotent, meaning they can be safely retried." |
| stamina timeout=0 | https://github.com/hynek/stamina/blob/main/CHANGELOG.md | "Passing `timeout=0` now raises a warning since it counterintuitively disables all retries." |
| stamina timeout=None | same | "If you explicitly want to disable the timeout, use `timeout=None`." |
| stamina wraps Tenacity | https://github.com/hynek/stamina/blob/main/README.md | "*stamina* is an opinionated wrapper around the great-but-unopinionated [Tenacity](https://tenacity.readthedocs.io/) package." |
| Resilience: total timeout | https://github.com/dotnet/extensions/blob/main/src/Libraries/Microsoft.Extensions.Http.Resilience/README.md | "The total request timeout pipeline applies an overall timeout to the execution" |
| Resilience: circuit breaker | same | "The circuit breaker blocks the execution if too many direct failures or timeouts are detected." |
| .NET 8 and 9 end | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | ".NET 8 and .NET 9 will reach end of support on November 10, 2026." |
| .NET 10 and 11 end | https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core | ".NET 10 November 11, 2025 10.0.15 November 10, 2026 LTS Active November 14, 2028" |
| .NET 11 released | same | ".NET 11 November 10, 2026 11.0.0 November 10, 2026 STS Active November 14, 2028" |
| PowerShell 7.4 end | https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle | "PowerShell 7.4 (LTS) 16-Nov-2023 10-Nov-2026" |
| PowerShell 7.5 end | same | "PowerShell 7.5 23-Jan-2025 10-Nov-2026" |
| PowerShell follows .NET | same | "The PowerShell support lifecycle follows the support lifecycle of .NET." |
| Node 22 end | https://raw.githubusercontent.com/nodejs/Release/main/schedule.json | "\"end\": \"2027-04-30\"" (in the `v22` object) |
| Python 3.15.0 date | https://peps.python.org/pep-0790/ | "3.15.0 final: Friday, 2026-10-09" |
| Python 3.15 security end | same | "Provided irregularly on an as-needed basis until October 2031." |
| Tachyon | https://docs.python.org/3.15/whatsnew/3.15.html | "profiling.sampling: a new statistical sampling profiler (named Tachyon)." |
| profile removed in 3.17 | same | "The profile module is deprecated and will be removed in Python 3.17." |
| JEP 543 | https://openjdk.org/jeps/543 | "We here propose to finalize Structured Concurrency in JDK 28, without further change." |
| OTel Go logs RC | https://opentelemetry.io/status/ | "Go Stable Stable Release candidate" (table row, tag-stripped) |
| Hayabusa dfir-timeline (4.0.0) | https://github.com/Yamato-Security/hayabusa/blob/main/CHANGELOG.md | "Combined the `csv-timeline` and `json-timeline` commands into a single **`dfir-timeline`** command" |
| Hayabusa offset bug (4.1.0) | same | "so they disagreed with every other timestamp in the same output by the host's UTC offset" |
| Hayabusa latest | same | "## 4.4.0 [2026/11/10] - CODE BLUE Release" |
| WinDbg MCP (1.2610) | https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes | "This release introduces AI-assisted debugging with WinDbg MCP" |
| Get-WinEvent hash table filter (added at intake) | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent | "Specifies a query in hash table format to select events from one or more event logs." |
| Get-WinEvent MaxEvents (added at intake) | same | "Specifies the maximum number of events that are returned." |
| Get-WinEvent default count (added at intake) | same | "The default is to return all the events in the logs or files." |
| Get-WinEvent order (added at intake) | same | "By default, Get-WinEvent returns event information in the order of newest to oldest." |
| journalctl since/until (added at intake) | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | "Start showing entries on or newer than the specified date, or on or older than the specified date, respectively." |
| journalctl date format (added at intake) | same | "Date specifications should be of the format "2012-10-30 18:17:16"." |
| journalctl -u (added at intake) | same | "Show messages for the specified systemd unit UNIT (such as a service unit), or for any of the units matched by PATTERN." |
| journalctl -p (added at intake) | same | "If a single log level is specified, all messages with this log level or a lower (hence more important) log level are shown." |
| journalctl -b (added at intake) | same | "Show messages from a specific boot." |
| journalctl -b with no argument (added at intake) | same | "The argument may be empty, in which case logs for the current boot will be shown." |
| journalctl -o json (added at intake) | same | "formats entries as JSON objects, separated by newline characters" |
| journalctl short-iso (added at intake) | same | "shows timestamps in the RFC 3339 profile of ISO 8601" |
| journalctl --utc (added at intake) | same | "Express time in Coordinated Universal Time (UTC)." |
| KQL definition (added at intake) | https://learn.microsoft.com/en-us/kusto/query/ | "A Kusto query is a read-only request to process data and return results." |
| LogQL definition (added at intake) | https://grafana.com/docs/loki/latest/query/ | "LogQL is the query language for Grafana Loki." |
| LogQL structure (added at intake) | same | "The log stream selector is mandatory while the log pipeline is optional." |

Non-ASCII notes: none of the quotes above contains a non-ASCII character. Nearby text that does:
the KQL page's next sentence "A Kusto query doesn’t write any data." uses U+2019, and the
journalctl `-b` synopsis uses "±".

## Versions found from registries

| Tool | Current version | Released | Source |
|---|---|---|---|
| tenacity | 9.2.1 | 2026-10-07 | PyPI JSON |
| stamina | 26.1.0 | 2026-04-13 | PyPI JSON (unreleased changes are pending in the changelog) |
| python-evtx | 0.8.1 | 2025-05-02 | PyPI JSON |
| Polly | 8.9.1 | 2026-11-07 | NuGet registration |
| Polly.Core | 8.9.1 | 2026-11-07 | NuGet registration |
| Microsoft.Extensions.Http.Resilience | **11.0.0** | 2026-11-10 | NuGet registration (10.11.0 on 2026-10-14) |
| resilience4j (resilience4j-retry) | 2.4.0 | 2026-03-14 | Maven Central |
| Hayabusa | **4.4.0** | 2026-11-10 | CHANGELOG, tags |
| Chainsaw | **2.17.1** | 2026-10-14 (commit date) | tags, Cargo.toml `version = "2.17.1"` |
| WinDbg | 1.2611.4001.0 | not stated | Microsoft Learn release notes; winget manifest |
| Go | 1.27.4 (1.26.11 for 1.26) | 2026-11-10 | go.dev release history |
| Python | 3.15.2 | 2026-10-26 | PEP 790 |
| .NET | 11.0.0 (STS); 10.0.15 (LTS) | 2026-11-10 | .NET support policy, releases-index.json |
| PowerShell | 7.6 (LTS) | 2026-03-18 | PowerShell support lifecycle |
| Node.js | 26 (Active LTS) | LTS from 2026-10-28 | nodejs/Release schedule.json |
| OTel Semantic Conventions | **1.45.0** | 2026-11-01 (tag commit) | git tags |
| systemd (journalctl man page) | 262 | n/a | freedesktop.org man page header |

## Licences

| Source | Licence as stated | What an Apache-2.0 repository may do |
|---|---|---|
| RFC 9457, RFC 9110 | IETF Trust Legal Provisions; "Code Components extracted from this document must include Revised BSD License text" | Quote briefly with the RFC number; paraphrase; adapt code components keeping the Revised BSD notice |
| RFC 3339 | "Copyright (C) The Internet Society (2002). All Rights Reserved."; copies and derivative works that "comment on or otherwise explain it" are allowed with the notice | Quote briefly and paraphrase with citation; the ABNF lines are fine to quote |
| FreeBSD sysexits(3) | The page states none; the source `sysexits.3` is "SPDX-License-Identifier: BSD-2-Clause" | Quote, paraphrase; adapt with the BSD notice |
| go.dev (release notes, blog) | "the contents of this site are licensed under the Creative Commons Attribution 4.0 License, and code is licensed under a BSD license" | Quote, paraphrase, adapt with attribution to the Go Authors |
| pkg.go.dev errors docs | Go source docs, BSD-3-Clause (Go licence), not re-read today | Quote briefly; adapt code with the BSD notice |
| docs.python.org | "This page is licensed under the Python Software Foundation License Version 2. Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License." | Quote, paraphrase; code examples freely under 0BSD |
| peps.python.org (PEP 654, 678, 790, 799) | "placed in the public domain or under the CC0-1.0-Universal license, whichever is more permissive" | Anything; a link is courtesy |
| opentelemetry.io | Footer: CC BY 4.0 | Quote, paraphrase, adapt with attribution |
| Microsoft Learn (Get-WinEvent, PowerShell lifecycle, WinDbg notes, Kusto) | The pages state no licence; their repositories (PowerShell-Docs, windows-driver-docs, dataexplorer-docs) carry CC BY 4.0, with PowerShell-Docs code under MIT | Quote, paraphrase, adapt with attribution to Microsoft |
| devblogs.microsoft.com, dotnet.microsoft.com | Not stated on the page; Microsoft terms of use (not checked) | Brief quotes and paraphrase with a link |
| AWS Builder Center article | "© 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved." | Brief quotes and paraphrase with a link; no copying of code or long passages |
| freedesktop.org journalctl(1) | Source `man/journalctl.xml`: "SPDX-License-Identifier: LGPL-2.1-or-later" | Brief quotes and paraphrase with a link; don't copy large parts into Apache-2.0 files |
| grafana.com LogQL docs | Page: "Copyright 2026 © Grafana Labs"; the Loki repository is AGPL-3.0 | Brief quotes and paraphrase only; adapt no text or code |
| TC39 finished proposals, nodejs/Release schedule.json | No licence file found at the paths tried | Cite the facts with a link |
| tenacity | Apache-2.0 (PyPI, LICENSE) | Quote, paraphrase, adapt code with licence and NOTICE |
| stamina | MIT (PyPI, LICENSE) | Quote, paraphrase, adapt code keeping the MIT notice |
| Polly, Polly.Core | BSD-3-Clause (NuGet, LICENSE) | Quote, paraphrase, adapt code keeping the BSD notice |
| Microsoft.Extensions.Http.Resilience | MIT (NuGet) | Quote, paraphrase, adapt code keeping the MIT notice |
| resilience4j | Apache-2.0 (POM, LICENSE.txt) | Quote, paraphrase, adapt code with licence and NOTICE |
| python-evtx | Apache-2.0 (PyPI, LICENSE.TXT) | Quote, paraphrase, adapt code with licence and copyright |
| Hayabusa | GNU Affero General Public License v3 (`LICENSE.txt`) | Quote briefly from release notes and paraphrase; adapt no code |
| Chainsaw | GPL v3 (`LICENCE`; Cargo.toml `license = "GPL3"`) | Quote briefly from release notes and paraphrase; adapt no code |

## Repository facts this contradicts

`git grep` over `skills/` for .NET 8/9/10/11, PowerShell 7.4/7.5/7.6, Python 3.15, Node 22/26,
Go 1.26/1.27, Hayabusa, Chainsaw, WinDbg, python-evtx, Polly, tenacity, stamina, resilience4j,
Http.Resilience, RFC 9457/7807/3339, sysexits, AsType, errors.Join, JEP, StructuredTaskScope,
journalctl, Get-WinEvent, KQL and LogQL.

Now wrong:

- `skills/coding/references/csharp-coding.md`, row `cs-dotnet11-rc` (".NET 11 is at RC2", quote
  ".NET 11 RC2 October 13, 2026", checked 2026-10-26). .NET 11 shipped on 2026-11-10 as an STS
  release, supported until 2028-11-14 (RC3 came on 2026-10-25 before it). Correct value and
  quote: ".NET 11 November 10, 2026 11.0.0 November 10, 2026 STS Active November 14, 2028" from
  https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core. Line 13's prose, "11 a
  release candidate (fact `cs-dotnet11-rc`)", goes with it.

Checked and still right: `cs-dotnet10-lts` and `cs-dotnet8-9-end` (csharp-coding.md),
`ps-lifecycle-76` and `ps-lifecycle-74-75` (powershell-scripts.md), `tp-go` (testing-patterns.md),
`js-node20-eol` (javascript-coding.md), and the standard's *Language toolchains* rows for Python
(3.15 on 2026-10-09), PowerShell, .NET (10 LTS to 2028-11-14; 8 and 9 ended 2026-11-10) and Node
(22 ends 2027-04-30). The standard's .NET row doesn't mention .NET 11's release. That isn't wrong,
but it is newer than the row. No `skills/` file yet names Hayabusa, Chainsaw, WinDbg, python-evtx,
the retry libraries, RFC 9457 or sysexits, so the contradicted versions above touch no existing
row.

---

# R07: Error handling, logging, observability, performance, concurrency and log analysis (as of 11 November 2026)

Most of the "What we believe" list still holds, but three items need fixing. OpenTelemetry signal stability differs by language more than the belief implies: Rust traces are Beta, Go logs are a Release candidate, and Python and JavaScript logs are still in Development.\[1\] PEP 799 is a reorganisation PEP: it moves the profilers into a new `profiling` package, and the new profiler (Tachyon) lives there as `profiling.sampling`.\[2\] And .NET 8 and .NET 9 went out of support yesterday, 10 November 2026, so every .NET example in the repository should target .NET 10 (LTS).\[3\]\[4\] Several Priority questions could only be partly sourced in this run. The gaps are listed in section 9, not filled with guesses.

## 1. Summary

- **Python 3.15.0** shipped on **9 October 2026**, not the planned 1 October. PEP 790 lists "3.15.0 final: Friday, 2026-10-09".\[5\] 3.15.2 followed on 26 October 2026, and security fixes run until October 2031.\[5\]\[6\]
- **PEP 799 / Tachyon:** Python 3.15 adds a `profiling` package. `profiling.tracing` is the old cProfile (which stays as an alias), and `profiling.sampling` is the new Tachyon sampling profiler, rated "up to 1,000,000 Hz". `profile` is deprecated and will be removed in Python 3.17.\[2\]\[7\]
- **Free-threaded CPython** has been officially supported since Python 3.14 (PEP 779, "phase II"). It is still an optional build, and nobody has decided whether it will become the default.\[8\]
- **OpenTelemetry SDK status today** (opentelemetry.io/status):
  - Logs are Stable in C++, .NET, Java, PHP and Rust; a Release candidate in Go; and in Development in Python, JavaScript, Ruby, Swift, Erlang/Elixir and Kotlin.\[1\]
  - Rust traces are Beta.\[1\]
  - Metrics are still in Development in Ruby, Swift, Erlang/Elixir and Kotlin.\[1\]
- **OpenTelemetry HTTP semantic conventions** have been stable since v1.23.0 (November 2023). Instrumentations migrating from older names use `OTEL_SEMCONV_STABILITY_OPT_IN=http` or `http/dup`.\[9\]\[10\]
- **RFC 9457** (July 2023) obsoletes RFC 7807. Use `application/problem+json` with the members `type`, `title`, `status`, `detail` and `instance`. When `type` is absent it is assumed to be `about:blank`.\[11\]
- **.NET 8 and .NET 9 reached end of support on 10 November 2026.** .NET 10 (LTS) is supported until 14 November 2028. Treat any repository content that targets .NET 8 or 9 as out of date.\[4\]
- **Polly v8 is current:** Polly / Polly.Core 8.9.1 was published 7 November 2026. Microsoft.Extensions.Http.Resilience 10.11.0 was published 14 October 2026 and is built on Polly.\[12\]\[13\]\[14\]\[15\]
- **Python retries:** tenacity 9.2.1 (7 October 2026) and stamina 26.1.0 (13 April 2026). From 26.1.0, stamina warns on `timeout=0`, "since it counterintuitively disables all retries".\[16\]\[17\]\[18\]
- **Java:** Structured Concurrency is in its seventh preview in JDK 27 (JEP 533), and the API changed in ways that break code written for earlier previews. JEP 543 proposes finalising it in JDK 28 with no further changes. That is still a proposal.\[19\]\[20\]\[21\]
- **Go:** Go 1.26 added `errors.AsType[E]`, a generic, reflection-free replacement for `errors.As`.\[22\] Go 1.27 (19 August 2026) added generic methods, made `encoding/json` run on the v2 implementation, and promoted the goroutine leak profile to general availability.\[23\]\[24\]
- **Node.js:** Node 26 became LTS on 28 October 2026 and reaches end of life on 30 April 2029. Node 22 reaches end of life on **30 April 2027**, inside the next 12 months.\[25\]
- **Windows log analysis tools are actively maintained:**
  - Hayabusa v4.3.1 (29 October 2026).\[26\]
  - Chainsaw v2.16.x (v2.16.3 on 4 August 2026; v2.16.5 is the latest tag).\[27\]
  - WinDbg 1.2611.4001.0, which adds "AI-assisted debugging with WinDbg MCP".\[28\]
  - python-evtx is at v0.8.1 and is slow-moving but not abandoned.\[29\]\[30\]
- **`sysexits.h` is deprecated on FreeBSD.** The current man page says: "This interface has been deprecated and is retained only for compatibility. Its use is discouraged."\[31\] Don't present `sysexits.h` as a recommended convention without that caveat.
- **RFC 3339 makes the time-zone offset mandatory** (`time-offset = "Z" / time-numoffset`), and says "the interoperability problems of unqualified local time are deemed unacceptable for the Internet."\[32\]

## 2. Corrections

| # | What we believed | Verdict | Correct fact and source |
|---|---|---|---|
| C1 | "OpenTelemetry traces and metrics are stable in most SDKs, logs are stable in several, and the HTTP semantic conventions are stable." | **Partly wrong.** The HTTP part is confirmed; the "most SDKs" framing needs qualifying. | The OpenTelemetry status page lists: Rust traces **Beta**; Kotlin traces, metrics and logs **Development**; Ruby, Swift and Erlang/Elixir metrics **Development**. Logs are Stable in C++, .NET, Java, PHP and Rust; **Release candidate** in Go; **Development** in Python and JavaScript. Source: https://opentelemetry.io/status/ (read 11 Nov 2026).\[1\] The HTTP semantic conventions have been stable since v1.23.0: https://opentelemetry.io/blog/2023/http-conventions-declared-stable/ \[33\] |
| C2 | "Python 3.15, released on 9 October 2026, added a sampling profiler (PEP 799)." | **Confirmed, with a nuance.** | The date is right: PEP 790 lists "3.15.0 final: Friday, 2026-10-09" (https://peps.python.org/pep-0790/). \[5\] But PEP 799 is a *reorganisation* PEP that creates the `profiling` package. The sampling profiler is Tachyon, exposed as `profiling.sampling`. The same PEP deprecates `profile` and schedules its removal in 3.17 (https://docs.python.org/3.15/whatsnew/3.15.html). \[2\]\[34\] |
| C3 | "Polly v8 and Microsoft.Extensions.Http.Resilience are the current .NET resilience libraries." | **Confirmed, with an update.** | Polly 8.9.1 (7 Nov 2026) and Microsoft.Extensions.Http.Resilience 10.11.0 (14 Oct 2026).\[13\]\[14\] The package major version now tracks .NET 10. And .NET 8 and .NET 9, the targets of most published Polly examples, went out of support on 10 Nov 2026 (https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/). \[3\] |
| C4 | "RFC 9457 … obsoleted RFC 7807 in 2023." | **Confirmed.** | Published July 2023; the abstract says "This document obsoletes RFC 7807."\[11\] (https://www.rfc-editor.org/rfc/rfc9457.html). \[11\] |
| C5 | "Python 3.14 made free-threaded CPython officially supported (PEP 779)." | **Confirmed.** | "The free-threaded build of Python is now supported and no longer experimental. This is the start of phase II where free-threaded Python is officially supported but still optional." (https://docs.python.org/3/whatsnew/3.14.html). \[8\] |
| C6 | "Python 3.11 added exception groups and add_note, ES2022 added Error cause, and Go 1.20 added errors.Join." | **Confirmed.** | Python: What's New In Python 3.11 (https://docs.python.org/3/whatsnew/3.11.html; 3.11 released 24 Oct 2022) has the headings "PEP 654: Exception Groups and except*" and "PEP 678: Exceptions can be enriched with notes", and says "The add_note() method is added to BaseException." JavaScript: TC39's finished-proposals list (https://github.com/tc39/proposals) gives "Error Cause" (author Chengzhong Wu) as reaching stage 4 in October 2021, with expected publication year 2022. Go: the Go 1.20 release notes (https://go.dev/doc/go1.20) say "The new function errors.Join returns an error wrapping a list of errors." and "The fmt.Errorf function now supports multiple occurrences of the %w format verb." A related new fact: Go 1.26 added `errors.AsType` (see F14). |
| C7 | "The AWS Builders' Library article on timeouts, retries and backoff with jitter is the standard reference for retry design." | **Article confirmed; calling it "the standard" is opinion.** | "Timeouts, retries, and backoff with jitter" by Marc Brooker, Amazon Builders' Library, 2019 (https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/). It recommends "capped exponential backoff" and says "Jitter adds some amount of randomness to the backoff to spread the retries around in time." No standards body has named it the standard reference. |
| C8 (new) | Implied: `sysexits.h` is a recommended exit-code convention. | **Out of date on FreeBSD.** | The FreeBSD sysexits(3) page (dated 9 May 2024) calls it "legacy exit status codes for system programs" and says "Its use is discouraged."\[31\] The older FreeBSD 4.3 page had recommended it.\[35\] |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | Python 3.15.0 release date | 9 Oct 2026 | https://peps.python.org/pep-0790/ | "3.15.0 final: Friday, 2026-10-09" | read 11 Nov 2026 |
| F2 | Python 3.15 latest bugfix | 3.15.2, 26 Oct 2026 | https://peps.python.org/pep-0790/ | "3.15.2: Monday, 2026-10-26"\[5\] | read 11 Nov 2026 |
| F3 | Python 3.15 end of security support | ~Oct 2031 | https://peps.python.org/pep-0790/ | "Provided irregularly on an as-needed basis until October 2031."\[5\] | read 11 Nov 2026 |
| F4 | Tachyon sampling profiler | `profiling.sampling` | https://docs.python.org/3.15/whatsnew/3.15.html | "profiling.sampling: a new statistical sampling profiler (named Tachyon)."\[2\] | read 11 Nov 2026 |
| F5 | `profile` module removal | Python 3.17 | https://docs.python.org/3.15/whatsnew/3.15.html | "The profile module is deprecated and will be removed in Python 3.17."\[2\] | read 11 Nov 2026 |
| F6 | Free-threaded CPython status | Supported, optional | https://docs.python.org/3/whatsnew/3.14.html | "This is the start of phase II where free-threaded Python is officially supported but still optional."\[8\] | read 11 Nov 2026 |
| F7 | OpenTelemetry logs specification | Stable | https://opentelemetry.io/docs/specs/status/ | "Bridge API: stable · SDK: stable · Protocol: stable"\[36\] | read 11 Nov 2026 |
| F8 | OpenTelemetry Collector status | Mixed | https://opentelemetry.io/status/ | "The collector status is: mixed, since core collector components currently have mixed stability levels."\[1\] | read 11 Nov 2026 |
| F9 | HTTP semantic conventions stable | v1.23.0 | https://opentelemetry.io/blog/2023/http-conventions-declared-stable/ | "the HTTP semantic conventions are the first OpenTelemetry semantic conventions to be declared stable!"\[33\] | Nov 2023 |
| F10 | Semantic convention migration switch | `OTEL_SEMCONV_STABILITY_OPT_IN` | https://opentelemetry.io/docs/specs/semconv/non-normative/http-migration/ | "http/dup - emit both the old and the stable HTTP and networking conventions, allowing for a phased rollout"\[10\] | read 11 Nov 2026 |
| F11 | Polly latest | 8.9.1 | https://www.nuget.org/packages/polly/ | "8.9.1 … 11/7/2026"\[13\] | 7 Nov 2026 |
| F12 | Microsoft.Extensions.Http.Resilience latest | 10.11.0 | https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience | "10.11.0 … 10/14/2026"\[14\] | 14 Oct 2026 |
| F13 | .NET 8 and 9 end of support | 10 Nov 2026 | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | ".NET 8 and .NET 9 will reach end of support on November 10, 2026." | read 11 Nov 2026\[3\] |
| F14 | Go `errors.AsType` | Go 1.26 | https://antonz.org/go-1-26/ (secondary) | "The new errors.AsType function is a generic version of errors.As"\[22\] | Feb 2026\[37\] |
| F15 | Go 1.27 release | 19 Aug 2026 | https://go.dev/blog/go1.27 | "Today the Go team is pleased to release Go 1.27." (post dated 19 August 2026) | 19 Aug 2026\[38\] |
| F16 | Java structured concurrency | 7th preview, JDK 27 | https://openjdk.org/jeps/8389757 | "again via JEP 533 (JDK 27) with an update to add a type parameter for the exception thrown by the join() method."\[39\] | read 11 Nov 2026 |
| F17 | tenacity latest | 9.2.1 | https://pypi.org/project/tenacity/ | "Released: Oct 7, 2026"\[16\] | 7 Oct 2026 |
| F18 | stamina latest | 26.1.0 | https://pypi.org/project/stamina/ | "Released: Apr 13, 2026"\[17\] | 13 Apr 2026 |
| F19 | resilience4j latest | 2.4.0 | https://newreleases.io/project/github/resilience4j/resilience4j/release/v2.4.0 (secondary mirror of GitHub) | "Feature #2224 : Bump jdk from 17 to 21 for support virtual thread"\[40\] | 14 Mar 2026 |
| F20 | Hayabusa latest | v4.3.1 | https://github.com/Yamato-Security/hayabusa/releases/tag/v4.3.1 | "Released 2026/10/29."\[26\] | 29 Oct 2026 |
| F21 | Chainsaw | v2.16.3; v2.16.5 latest | https://newreleases.io/project/github/WithSecureOpenSource/chainsaw/release/v2.16.3 (secondary) | "latest releases: v2.16.5, v2.16.4"\[27\] | 4 Aug 2026 (v2.16.3) |
| F22 | WinDbg latest | 1.2611.4001.0 | https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes | "This release introduces AI-assisted debugging with WinDbg MCP"\[28\] | 5 Nov 2026 (Wikipedia date, secondary)\[41\] |
| F23 | python-evtx latest | v0.8.1 | https://github.com/williballenthin/python-evtx/releases | "migrate to pyproject.toml (and using uv and just)"\[29\] | "02 May" (year not shown in excerpt) |
| F24 | RFC 9457 | Obsoletes 7807 | https://www.rfc-editor.org/rfc/rfc9457.html | "This document obsoletes RFC 7807." | July 2023 |
| F25 | Problem details media type | application/problem+json | https://www.rfc-editor.org/rfc/rfc9457.html | "that format is identified with the \"application/problem+json\" media type."\[11\] | July 2023 |
| F26 | 4xx class | Client error | https://httpwg.org/specs/rfc9110.html | "The 4xx (Client Error) class of status code indicates that the client seems to have erred."\[42\] | June 2022 |
| F27 | 5xx class | Server error | https://httpwg.org/specs/rfc9110.html | "The 5xx (Server Error) class of status code indicates that the server is aware that it has erred or is incapable of performing the requested method."\[42\] | June 2022 |
| F28 | RFC 3339 offset | Mandatory | https://www.rfc-editor.org/rfc/rfc3339.txt | "time-offset = \"Z\" / time-numoffset"\[32\] | July 2002 |
| F29 | sysexits deprecated (FreeBSD) | Discouraged | https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits | "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." | 9 May 2024 |
| F30 | Node 22 end of life | 30 Apr 2027 | https://endoflife.ai/article-nodejs-eol (secondary; cites the nodejs/Release schedule) | "Node.js 22: end of life 2027-04-30" | read 11 Nov 2026\[25\] |

## 4. Findings

### 4.1 Error handling per language (Priority)

What was sourced in this run:

- **Go.** Go 1.26 added `errors.AsType[E error](err error) (E, bool)`. A secondary source walking through the release says "Since AsType can handle everything that As does, it's a recommended drop-in replacement for new code". It also says the function does not use reflection and gives a compile-time error where `errors.As` would panic at runtime (https://antonz.org/go-1-26/, secondary).\[22\]\[23\]\[43\] **Guidance:** in new Go code targeting 1.26 or later, prefer `errors.AsType` over `errors.As`. Keep wrapping with `%w`.
- **Python.** Exception notes are specified by PEP 678 (https://peps.python.org/pep-0678/), which says "BaseException gains a new method .add_note(note: str)" and "If note is not a string, .add_note() raises TypeError." Exception groups and `except*` arrived in Python 3.11 under PEP 654 (see C6). Python 3.15's What's New was read for the profiler only.
- **C#.** .NET 11 shipped on 10 November 2026 as a Standard Term Support release. It adds "runtime async, which moves the async/await transformation into the JIT for cleaner stack traces" (https://www.ntcompatible.com/story/net-11-release-15-runtime-async-and-an-aifirst-stack, secondary news). C# 15 union types are reported in the same article; check them against Microsoft Learn before using them in guidance on result types.\[44\]
- **Every other language listed** (TypeScript/JavaScript, PowerShell, Rust, Java, PHP, Ruby, Bash): not covered in this run (see section 9).

### 4.2 Resilience (Priority)

| Language | Library | Version | Released | Notes |
|---|---|---|---|---|
| Python | tenacity | 9.2.1 | 7 Oct 2026 | Apache-2.0 per registry metadata\[16\]\[45\] |
| Python | stamina | 26.1.0 | 13 Apr 2026 | An "opinionated wrapper around the great-but-unopinionated Tenacity package"; MIT; now warns on `timeout=0`\[18\]\[46\] |
| .NET | Polly / Polly.Core | 8.9.1 | 7 Nov 2026 | BSD-3-Clause per Sonatype\[12\]\[47\] |
| .NET | Microsoft.Extensions.Http.Resilience | 10.11.0 | 14 Oct 2026 | MIT; "Resilience mechanisms for HttpClient built on the Polly framework"\[15\]\[48\] |
| Java | resilience4j | 2.4.0 | 14–15 Mar 2026 | Apache-2.0; 2.4.0 raises the build JDK to 21 "for support virtual thread"\[40\]\[49\] |
| Node.js | p-retry | not found | | |
| Rust | backon | not found | | |

**Positions:**
- **Python:** use stamina for application code. It wraps tenacity with safer defaults, and its newest release adds a guard against the `timeout=0` misuse.\[18\]\[46\] Use tenacity directly only when you need its full configurability.
- **.NET:** use Microsoft.Extensions.Http.Resilience (`AddStandardResilienceHandler` / `AddStandardHedgingHandler`) for HttpClient, and Polly v8 `ResiliencePipeline` for everything else. Its README describes a "total request timeout pipeline [that] applies an overall timeout to the execution, ensuring that the request including hedging attempts, does not exceed the configured limit".\[15\] That is the deadline pattern.
- **Circuit breakers:** Microsoft's README says "The circuit breaker blocks the execution if too many direct failures or timeouts are detected."\[15\]
- **Retry design references:** the AWS Builders' Library article "Timeouts, retries, and backoff with jitter" (Marc Brooker, 2019) recommends "capped exponential backoff" and says "Jitter adds some amount of randomness to the backoff to spread the retries around in time." Idempotency keys and bulkheads were not sourced in this run.

### 4.3 API errors (Priority)

- **RFC 9457 (July 2023, Standards Track; authors Nottingham, Wilde, Dalal)** obsoletes RFC 7807.\[11\]
  - Media types: `application/problem+json`, and `application/problem+xml` (Appendix B).\[11\]
  - Members:
    - `type`: a URI reference, assumed `about:blank` when absent.\[11\]
    - `title`: a short summary that "SHOULD NOT change from occurrence to occurrence of the problem, except for localization".\[11\]
    - `status`: "only advisory… Generators MUST use the same status code in the actual HTTP response".\[11\]
    - `detail`: "Consumers SHOULD NOT parse the \"detail\" member for information".\[11\]
    - `instance`: identifies this occurrence.\[11\]
  - Extensions: "Clients consuming problem details MUST ignore any such extensions that they don't recognize."\[11\]
  - Fit: "Problem details can be used with any HTTP status code, but they most naturally fit the semantics of 4xx and 5xx responses."\[11\]
- **RFC 9110 mapping rule:**
  - 4xx means "the client seems to have erred".\[42\]
  - 5xx means "the server is aware that it has erred or is incapable of performing the requested method".\[42\]
  - A client receiving an invalid status code "SHOULD process the response as if it had a 5xx (Server Error) status code."\[42\]
  - **Practical rule:** a failed downstream dependency or an unhandled exception is 5xx, never 4xx. Validation failures on the request are 4xx.
- **Example (adapt freely; RFC code components are BSD-licensed under the IETF Trust provisions):**\[11\]

```json
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://example.com/problems/invalid-date",
  "title": "The date is not valid",
  "status": 422,
  "detail": "The start date 2026-13-01 has month 13. Use a month from 01 to 12.",
  "instance": "/bookings/req-7f3a"
}
```

- **Style guides:** GOV.UK, Microsoft and Nielsen Norman Group guidance on error messages was not sourced in this run.
- **Adoption:** framework adoption of RFC 9457 (ASP.NET Core ProblemDetails, Spring `ProblemDetail`) was not sourced in this run.

### 4.4 Results that say what happened (Priority)

- **Exit codes.**
  - POSIX: not sourced in this run.
  - `sysexits.h` values, from the FreeBSD sysexits(3) page:
    - EX_OK = 0\[31\]
    - EX_USAGE = 64 ("The command was used incorrectly…")\[31\]
    - EX_DATAERR = 65\[31\]
    - EX_NOINPUT = 66\[31\]
    - EX_UNAVAILABLE = 69\[31\]
    - EX_SOFTWARE = 70\[31\]
    - EX_TEMPFAIL = 75 ("the request should be reattempted later")\[31\]
    - EX_CONFIG = 78\[31\]
  - The same page says "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." and "The choice of an appropriate exit value is often ambiguous."\[31\]
  - **Position:** document your own exit-code table, with one meaning per code. Borrow the 64–78 numbers if they help, but don't call sysexits "the standard". FreeBSD itself has disowned it, and its own definition of EX_UNAVAILABLE ("a catchall message when something you wanted to do does not work, but you do not know why") breaks the one-meaning-per-code rule.\[31\]
- **Timestamps.**
  - RFC 3339 grammar: `full-time = partial-time time-offset`, so the offset is required.\[32\]
  - "-00:00" means the offset to local time is unknown, which is different from "Z".\[32\]
  - Generators "SHOULD use upper case letters".\[32\]
  - **Position:** log RFC 3339 timestamps with an explicit offset, ideally UTC "Z". Log lines without an offset can't be compared across hosts. Hayabusa v4.1.0 fixed exactly this bug: its histogram axis "disagreed with every other timestamp in the same output by the host's UTC offset" (https://github.com/Yamato-Security/hayabusa/releases/tag/v4.1.0). \[50\]
- **Not sourced in this run:**
  - published guidance on telling "not found" from "couldn't look";
  - fail-open broad catches around validators;
  - recording a child process's exit status, including unreaped (zombie) children;
  - argv as run;
  - head-and-tail output truncation;
  - status lines that name the outcome checked.

### 4.5 Log analysis (Priority)

| Tool | Current | Released | Status |
|---|---|---|---|
| Hayabusa | v4.3.1 ("Vulnpocalypse Release")\[26\] | 29 Oct 2026 | Active. Releases: v4.2.0 (12 Oct), v4.3.0 (28 Oct), v4.3.1 (29 Oct).\[26\]\[51\]\[52\] v4.1.0 merged `csv-timeline` and `json-timeline` into `dfir-timeline` with `-t csv/json/jsonl`, so **older command examples are out of date**.\[50\] |
| Chainsaw (WithSecure) | v2.16.5 (date not found); v2.16.3 on 4 Aug 2026\[27\] | — | Active. v2.16.0 added "an EVTX summary command"; v2.16.3 fixed SRUM parsing\[27\]\[53\] |
| WinDbg | 1.2611.4001.0 | 5 Nov 2026 (secondary)\[41\] | Active, roughly monthly. New in this release: WinDbg MCP for AI clients, host.currentStack and host.currentRegisters in JavaScript scripts\[28\] |
| python-evtx | v0.8.1 | "02 May" (year not in excerpt) | **Maintained, low activity.** v0.8.0 dropped Python 2.7 (minimum is 3.8); v0.8.1 moved to pyproject.toml and PyPI trusted publishing.\[29\] A secondary tracker reports 23 open issues and the last push about 8 months ago.\[30\] |
| Get-WinEvent, EvtxECmd, journalctl, KQL, LogQL | not found | | Not sourced in this run |

**Position:** for Windows event-log triage, use Hayabusa or Chainsaw (both Rust-based and frequently released). Use python-evtx only when you need programmatic access from Python, and pin it.

### 4.6 Logging (Priority)

- **OpenTelemetry's position on log correlation:** "When you add autoinstrumentation or activate an SDK, OpenTelemetry will automatically correlate your existing logs with any active trace and span". It also says "Structured logs are preferred in production" (https://opentelemetry.io/docs/concepts/signals/logs/). \[54\]
- **Go:** Go 1.26 added `slog.NewMultiHandler`, which lets one logger write to several handlers (https://www.gopherguides.com/articles/golang-1-26-everyday-apis, secondary).\[37\]
- **Not sourced in this run:**
  - W3C Trace Context;
  - the OWASP logging guidance on secrets, personal data and log injection;
  - versions of structlog, pino, Serilog, Microsoft.Extensions.Logging, Rust's tracing, Monolog and Ruby's Logger.

### 4.7 OpenTelemetry (Standard)

- **Per-language status** (https://opentelemetry.io/status/, read 11 Nov 2026):

| Language | Traces | Metrics | Logs |
|---|---|---|---|
| C++ | Stable | Stable | Stable |
| .NET | Stable | Stable | Stable |
| Erlang/Elixir | Stable | Development | Development |
| Go | Stable | Stable | Release candidate |
| Java | Stable | Stable | Stable (Profiles: Development) |
| JavaScript | Stable | Stable | Development |
| Kotlin | Development | Development | Development |
| PHP | Stable | Stable | Stable |
| Python | Stable | Stable | Development |
| Ruby | Stable | Development | Development |
| Rust | Beta | Stable | Stable |
| Swift | Stable | Development | Development |

- **Contested:** an older mirror (opentelemetry.netlify.app) and several secondary blogs still show Go logs as "Beta" and Rust as "Beta" for every signal.\[55\]\[56\] The live opentelemetry.io page takes precedence.
- **Other recent changes**, from opentelemetry.io blog titles (2026):
  - "Declarative configuration is stable!"\[1\]
  - "Announcing the OpenTelemetry JavaScript SDK 3.0"\[1\]
  - "Deprecating Span Events API"\[1\]
  - "OpenTelemetry Profiles Enters Public Alpha"\[1\]
  - "OpenTelemetry is a CNCF Graduated Project"\[1\]
  - "OpenTelemetry Transformation Language reaches v1"\[1\]
- **Specification and conventions:** the specification is at 1.62.0, per the site navigation.\[1\] Semantic Conventions v1.44.0 (4 Aug 2026) is shown as "Latest" on GitHub.\[57\]\[58\]
- **Starting setup for a small team (recommendation):**
  1. Use the SDK or zero-code agent where the signal is Stable for your language.
  2. Export OTLP to a single Collector.
  3. For languages whose logs are still in Development (Python, JavaScript), write structured JSON logs to stdout/file and collect them with the Collector's filelog receiver. Uptrace's guide says the same: "If your language is in Development and you need stability today, write structured logs to stdout or a file and collect them with the OpenTelemetry Collector" (https://uptrace.dev/opentelemetry/logs, secondary).\[59\]
  4. Pin Collector versions, because "The collector status is: mixed".\[1\]

### 4.8 Metrics and alerting (Standard)

Not covered. The RED and USE methods, the Google SRE book's guidance on SLOs and error budgets, and the status of Prometheus and OpenMetrics were not sourced in this run.

### 4.9 Performance (Standard)

- **Python 3.15 Tachyon (`profiling.sampling`).**
  - The What's New page describes "virtually zero overhead while achieving sampling rates of up to 1,000,000 Hz".\[2\]
  - It supports "run -m" to profile modules.\[2\]
  - Secondary sources report attach-by-PID, `dump` (stack snapshot, with `--async-aware`), and wall-clock, CPU and GIL modes (https://dev.to/mursalfk/python-315-just-dropped-heres-everything-that-changed-from-314-36kj, secondary).\[7\]\[60\]
  - `profiling.tracing` is the deterministic profiler; `cProfile` remains an alias.\[2\]\[61\]
- **Go 1.27.** The goroutine leak profile is now generally available. Size-specialised allocation routines cut the cost of allocations under 80 bytes "by up to 30%" (https://blog.codercops.com/blog/go-1-27-generic-methods-upgrade-guide-2026, secondary, citing the release notes).\[24\]\[62\]
- **Not covered:** py-spy, Scalene, Node `--cpu-prof`, clinic.js, dotnet-trace, dotnet-counters, BenchmarkDotNet, pprof versions, cargo flamegraph, criterion, async-profiler and JFR.

### 4.10 Concurrency (Standard)

- **Python.**
  - Free-threading has been supported but optional since 3.14 (PEP 779).\[8\]
  - Phase III, making it the default, has "no PEP and no schedule" (https://ttlab.hopto.org/blog/2026-07-16-python-315-abi3t-free-threaded-stable-abi?lang=en, secondary).\[63\]
  - Python 3.15 adds the abi3t stable ABI for free-threaded builds (PEP 803, per the same secondary source).\[63\]\[64\]
  - **Position:** use free-threading only for CPU-bound threaded work, and only after confirming that every C extension ships cp3xt wheels.\[64\]
  - asyncio TaskGroup and timeouts: not sourced in this run.
- **Java.**
  - Structured concurrency is in its seventh preview in JDK 27 (JEP 533).\[65\]
  - `StructuredTaskScope` and `Joiner` gained a third type parameter. The default joiner now throws `ExecutionException`; `FailedException` and `TimeoutException` were removed.\[19\]\[66\]
  - JEP 543 proposes finalising it in JDK 28 with no API changes (https://www.happycoders.eu/java/structured-concurrency-structuredtaskscope/, secondary: "targeted to Java 28 since October 15, 2026").\[20\]
  - Virtual threads have been final since JDK 21 (JEP 444) (https://www.danvega.dev/blog/java-structured-concurrency-jdk-27, secondary).\[21\]
- **C#.** .NET 11 runtime async (see 4.1). ConfigureAwait, ValueTask and cancellation guidance: not sourced in this run.
- **JavaScript, Go, Rust:** not covered in this run.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| CPython profiling.sampling (Tachyon) | Sampling profiler | Python 3.15.2 | 26 Oct 2026 | `python -m profiling.sampling run -m mymodule` (form per the What's New "run -m" mode; exact flags not verified) | none | https://docs.python.org/3.15/whatsnew/3.15.html |
| tenacity | Retries (Python) | 9.2.1 | 7 Oct 2026 | `pip install tenacity` | none | https://pypi.org/project/tenacity/ |
| stamina | Opinionated retries (Python) | 26.1.0 | 13 Apr 2026 | `pip install stamina` | none | https://pypi.org/project/stamina/ |
| Polly | Resilience (.NET) | 8.9.1 | 7 Nov 2026 | `dotnet add package Polly --version 8.9.1`\[13\] | none | https://www.nuget.org/packages/polly/ |
| Microsoft.Extensions.Http.Resilience | HttpClient resilience | 10.11.0 | 14 Oct 2026 | `dotnet add package Microsoft.Extensions.Http.Resilience --version 10.11.0`\[14\] | appsettings (optional) | https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience |
| resilience4j | Resilience (Java) | 2.4.0 | 14 Mar 2026 | Maven `io.github.resilience4j:resilience4j-retry:2.4.0` | application.yml (Spring) | https://mvnrepository.com/artifact/io.github.resilience4j |
| Hayabusa | EVTX threat hunting and timelines | 4.3.1 | 29 Oct 2026 | Release binary; `hayabusa dfir-timeline -d <dir> -t jsonl` | rules/ config dir | https://github.com/Yamato-Security/hayabusa/releases/tag/v4.3.1 |
| Chainsaw | EVTX/forensic hunting | 2.16.5 (date not found) | — | Release binary | rules/mappings | https://newreleases.io/project/github/WithSecureOpenSource/chainsaw/release/v2.16.3 |
| WinDbg | Crash dump and live debugging | 1.2611.4001.0 | 5 Nov 2026 | Install per the Microsoft Learn WinDbg page | none | https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes |
| python-evtx | EVTX parsing library | 0.8.1 | "02 May" (year unconfirmed) | `pip install python-evtx` | none | https://github.com/williballenthin/python-evtx/releases |

## 6. Changing in the next 12 months

| Item | Date | Status | Source |
|---|---|---|---|
| .NET 8 and .NET 9 end of support | 10 Nov 2026 | **Already passed (yesterday).** Migrate to .NET 10 LTS (supported to 14 Nov 2028). | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ \[3\] |
| PowerShell 7.4 and 7.5 end of support | 10 Nov 2026 | **Passed.** Reported as tied to .NET 8/9; successor PowerShell 7.6 LTS (secondary) | https://sadeem.de/en/blog/dotnet-8-9-supportende-november-2026 \[67\] |
| Node.js 22 end of life | 30 Apr 2027 | **Within 12 months; flagged** | https://endoflife.ai/article-nodejs-eol (secondary)\[25\] |
| Node.js 27 (first release under the yearly schedule) | April 2027 | Due within 6 months | https://latestat.com/nodejs (secondary)\[68\] |
| JDK 28 finalises structured concurrency (JEP 543) | JDK 28 (date not sourced) | Proposed; code written for the JDK 27 preview already breaks code written for JDK 26\[20\]\[66\] | https://www.happycoders.eu/java/structured-concurrency-structuredtaskscope/ (secondary) |
| OpenTelemetry Span Events API | Deprecation announced 2026 | Announced; details not read in this run\[1\] | https://opentelemetry.io/status/ (blog index) |
| Python `profile` module | Removal in 3.17 (Oct 2028, per the annual cadence) | Deprecated in 3.15\[2\] | https://docs.python.org/3.15/whatsnew/3.15.html |
| Go 1.27 removed GODEBUG settings (asynctimerchan, gotypesalias, several crypto/tls settings) | Done (19 Aug 2026) | Breaking for code that relied on them | https://daily.dev/posts/nmfkkkeoa (secondary summary of the release notes)\[69\] |

## 7. Common mistakes (including those AI coding assistants make)

1. **Writing `errors.As` with a pre-declared pointer in Go 1.26+ code.** It still works but can panic at runtime when given the wrong target. `errors.AsType` catches the same mistake at compile time (https://antonz.org/go-1-26/, secondary).\[22\] JetBrains notes that AI agents generate "Go code that looks a few years old" (https://blog.jetbrains.com/go/2026/08/05/new-livestream-go-127/). \[43\]\[62\]
2. **Citing RFC 7807 instead of RFC 9457**, or parsing `detail` programmatically, which RFC 9457 says consumers "SHOULD NOT" do.\[11\]
3. **Returning a 4xx for a server-side failure.** Under RFC 9110, 5xx means the server "has erred".\[42\]
4. **Logging timestamps without an offset.** RFC 3339 requires one. Hayabusa's own v4.1.0 bug shows how local-versus-UTC mismatches mislead investigators.\[32\]\[50\]
5. **Recommending `sysexits.h` as current best practice.** FreeBSD now says "Its use is discouraged."\[31\]
6. **Assuming OpenTelemetry logs are production-stable in every SDK.** Python and JavaScript logs are still in Development; Go logs are a Release candidate.\[1\]
7. **Generating .NET 8 examples (`net8.0`) after 10 November 2026.** That runtime no longer gets security fixes.\[3\]
8. **Using Java structured-concurrency code from JDK 21–26 tutorials on JDK 27.** It no longer compiles: `FailedException` and `TimeoutException` were removed (https://ankurm.com/java-27-every-jep-plus-java-26-changes/, secondary).\[66\]
9. **Passing `timeout=0` to stamina expecting "no timeout".** It disables all retries; use `timeout=None` (stamina 26.1.0 changelog, https://py3.online/pypi/stamina, secondary mirror of PyPI).\[18\]
10. **Pointing users at `import profile` in Python 3.15.** It is deprecated. Use `profiling.tracing` or `profiling.sampling`.\[2\]

## 8. Sources and licences

The licence entries are from my own knowledge of each project's published terms unless the "Licence" cell says it was seen in a source. Verify them before relying on them.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| peps.python.org (PEP 779, 790, 799) | Public domain or CC0-1.0 (standard PEP footer; not re-checked) | Yes | Yes | Yes | Courtesy link to the PEP |
| docs.python.org | PSF documentation licence (not re-checked) | Brief quotes | Yes | Code examples under the PSF/0BSD terms (not re-checked) | "Python Software Foundation", with link |
| opentelemetry.io | CC BY 4.0 for docs (not re-checked) | Yes | Yes | Yes (code samples Apache-2.0, not re-checked) | "© OpenTelemetry Authors, CC BY 4.0", with link |
| rfc-editor.org (RFC 3339, 9110, 9457) | IETF Trust Legal Provisions; code components under Revised BSD (not re-checked)\[11\] | Yes | Yes | Code components: yes, with the BSD notice | Cite the RFC number and the IETF Trust |
| man.freebsd.org sysexits(3) | BSD licence (not re-checked) | Yes | Yes | Yes | "FreeBSD Project", with link |
| learn.microsoft.com (WinDbg release notes, dotnet docs) | CC BY 4.0 docs, MIT code (not re-checked) | Yes | Yes | Yes | "Microsoft", with link |
| devblogs.microsoft.com | Microsoft terms of use (not re-checked) | Brief quotes only | Yes | No | Link |
| nuget.org / pypi.org / mvnrepository pages | Registry metadata (facts) | Facts only | Yes | n/a | Link |
| Polly | BSD-3-Clause (seen on Sonatype)\[47\] | Yes | Yes | Yes, keeping the BSD notice | Copyright notice |
| Microsoft.Extensions.Http.Resilience | MIT (seen on libraries.io)\[46\]\[48\] | Yes | Yes | Yes, keeping the MIT notice | Copyright notice |
| stamina | MIT (seen on libraries.io) | Yes | Yes | Yes | Copyright notice |
| tenacity | Apache-2.0 (seen on quanteta registry mirror)\[45\] | Yes | Yes | Yes | Licence plus NOTICE |
| resilience4j | Apache-2.0 (seen on mvnrepository)\[49\] | Yes | Yes | Yes | Licence plus NOTICE |
| python-evtx | Apache-2.0 (seen in the Evtx.py header and on SUSE)\[70\]\[71\] | Yes | Yes | Yes | Licence plus copyright |
| Hayabusa, Chainsaw (GitHub release notes) | Project licences not checked in this run | Brief quotes | Yes | Not until the licence is checked | Link |
| go.dev blog | CC BY 4.0 text, BSD code (not re-checked) | Yes | Yes | Yes | "The Go Authors", with link |
| openjdk.org JEPs | OpenJDK web terms (not checked) | Brief quotes | Yes | No | Link |
| Secondary blogs (antonz.org, happycoders.eu, realpython.com, codercops, nihardaily, endoflife.ai, herodevs, ntcompatible, uptrace, dev.to, ankurm, sadeem, py3.online, ttlab, danvega, jetbrains) | All rights reserved unless stated | Brief quotes only (fair use) | Yes | No | Link, labelled "secondary" |

## 9. Not found, contested, not covered

**Contested**
- **OpenTelemetry Go logs status.** opentelemetry.io/status says "Release candidate". The opentelemetry.netlify.app mirror and some 2026 blogs say "Beta".\[1\]\[55\] The official page takes precedence, and the OTel blog "OTel Go Logs API and SDK reach release candidate status" supports it.\[1\]
- **OpenTelemetry Rust status.** The official page shows traces Beta, metrics and logs Stable. A mirror shows Beta for all three.\[1\]\[55\]
- **Chainsaw latest version.** A GitHub page translated through Google shows v2.16.2 (9 Jul 2026) as latest. newreleases.io lists v2.16.5 as the latest tag.\[27\]\[72\] I used v2.16.5; its release date was not found.

**Not found**
- backon (Rust) and p-retry (Node) current versions.
- The release-date year for python-evtx v0.8.1.
- The JDK 28 GA date.
- The Go 1.26 end-of-support date.
- The exact `profiling.sampling` command-line flags.

**Not covered (out of room)**
- Q1: idioms for TypeScript/JavaScript, PowerShell, Rust, Java, PHP, Ruby and Bash.
- Q2: idempotency and bulkhead references.
- Q3: GOV.UK, Microsoft and NN/g error-message guidance; framework adoption of RFC 9457.
- Q4: POSIX exit-status text; "not found" versus "couldn't look"; fail-open validators; child-process reaping, argv and truncation.
- Q5: Get-WinEvent, EvtxECmd, journalctl, KQL and LogQL.
- Q6: W3C Trace Context; OWASP logging; logging-library versions.
- Q8: RED, USE, SRE, Prometheus and OpenMetrics.
- Q9: profiler versions outside Python.
- Q10: asyncio, the JavaScript event loop, C# async, Go races and Rust Send/Sync/tokio.

I recommend a follow-up run (R07b) scoped to these items.

## Sources

1. [Status](https://opentelemetry.io/status/)
2. [What’s new in Python 3.15 — Python 3.15.2 documentation](https://docs.python.org/3.15/whatsnew/3.15.html)
3. [.NET 8 and .NET 9 will reach End of Support on November 10, 2026 - .NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/)
4. [.NET 8 End of Life: 10 Nov 2026 and What to Do](https://www.codefirst.co.uk/end-of-life/dotnet-8/)
5. [PEP 790](https://peps.python.org/pep-0790/)
6. [Python Release Python 3.15.0rc3](https://www.python.org/downloads/release/python-3150rc3/)
7. [Python 3.15 just dropped. Here's everything that changed from 3.14 - DEV Community](https://dev.to/mursalfk/python-315-just-dropped-heres-everything-that-changed-from-314-36kj)
8. [What’s new in Python 3.14 — Python 3.15.2 documentation](https://docs.python.org/3/whatsnew/3.14.html)
9. [OpenTelemetry semantic conventions explained](https://clickhouse.com/resources/engineering/opentelemetry-semantic-conventions)
10. [HTTP semantic convention stability migration](https://opentelemetry.io/docs/specs/semconv/non-normative/http-migration/)
11. [RFC 9457: Problem Details for HTTP APIs](https://rfc-editor.org/rfc/rfc9457.html)
12. [NuGet Gallery](https://www.nuget.org/packages/polly.core/)
13. [NuGet Gallery](https://www.nuget.org/packages/polly/)
14. [NuGet Gallery](https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience)
15. [Microsoft.Extensions.Http.Resilience 10.5.0 - BaGet](https://nuget.health.go.ke/packages/microsoft.extensions.http.resilience/10.5.0)
16. [tenacity · PyPI](https://pypi.org/project/tenacity/)
17. [stamina · PyPI](https://pypi.org/project/stamina/)
18. [Python Online - py3.online](https://py3.online/pypi/stamina)
19. [Java 27 Features: All 9 JEPs in JDK 27 with Examples](https://howtodoinjava.com/java/java-27-features/)
20. [Structured Concurrency in Java 27 with StructuredTaskScope](https://www.happycoders.eu/java/structured-concurrency-structuredtaskscope/)
21. [Java Structured Concurrency in JDK 27: A Practical Example](https://www.danvega.dev/blog/java-structured-concurrency-jdk-27)
22. [Go 1.26 interactive tour](https://antonz.org/go-1-26/)
23. [Go proposal: Type-safe error checking](https://daily.dev/posts/go-proposal-type-safe-error-checking-u4b58mpwl)
24. [Go 1.27 Upgrade Guide: Generic Methods and What Breaks — CODERCOPS](https://blog.codercops.com/blog/go-1-27-generic-methods-upgrade-guide-2026)
25. [Node.js End of Life Dates: 20 Ended, 22 Ends April 30, 2027](https://endoflife.ai/article-nodejs-eol)
26. [Release v4.3.1 - Vulnpocalypse Release · Yamato-Security/hayabusa · GitHub](https://github.com/Yamato-Security/hayabusa/releases/tag/v4.3.1)
27. [WithSecureOpenSource/chainsaw v2.16.3 on GitHub](https://newreleases.io/project/github/WithSecureOpenSource/chainsaw/release/v2.16.3)
28. [WinDbg Release Notes - Windows drivers](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-release-notes)
29. [Releases · williballenthin/python-evtx · GitHub](https://github.com/williballenthin/python-evtx/releases)
30. [python-evtx 0.8.1 - Pure Python parser for Windows event log files (.evtx). - PythonFix.com](https://pythonfix.com/pkg/p/python-evtx/)
31. [sysexits(3) - FreeBSD 15.1-RELEASE and Ports.quarterly Manual Pages](https://man.freebsd.org/cgi/man.cgi?sektion=3&query=sysexits)
32. <https://rfc-editor.org/rfc/rfc3339.txt>
33. [HTTP semantic conventions declared stable](https://opentelemetry.io/blog/2023/http-conventions-declared-stable/)
34. [PEP 799](https://peps.python.org/pep-0799/)
35. [sysexits - FreeBSD 4.3-RELEASE Manual Pages](https://man.freebsd.org/cgi/man.cgi?query=sysexits&manpath=FreeBSD+4.3-RELEASE)
36. [Specification Status Summary](https://opentelemetry.io/docs/specs/status/)
37. [Go 1.26: The APIs You'll Use Every Day - Gopher Guides](https://www.gopherguides.com/articles/golang-1-26-everyday-apis)
38. [Go 1.27 is released - The Go Programming Language](https://go.dev/blog/go1.27)
39. [JEP draft: Structured Concurrency](https://openjdk.org/jeps/8389757)
40. [resilience4j/resilience4j v2.4.0 on GitHub](https://newreleases.io/project/github/resilience4j/resilience4j/release/v2.4.0)
41. [WinDbg](https://en.wikipedia.org/wiki/WinDbg)
42. [RFC 9110 - HTTP Semantics](https://httpwg.org/specs/rfc9110.html)
43. [What's New in Go 1.26: Hands-On](https://caioreix.com/posts/go-1-26-tour)
44. [.NET 11 Release: C# 15, Runtime Async, and an AI-First Stack](https://www.ntcompatible.com/story/net-11-release-15-runtime-async-and-an-aifirst-stack)
45. [tenacity 9.1.4 (PyPI)](https://quanteta.com/packages/en/package/pypi-tenacity/)
46. [stamina 26.1.0 on PyPI - Libraries.io - security & maintenance data for open source software](https://libraries.io/pypi/stamina)
47. [Polly 8.6.6](https://guide.sonatype.com/component/nuget/Polly/8.6.6/versions)
48. [Microsoft.Extensions.Http.Resilience 10.0.0 on NuGet - Libraries.io - security & maintenance data for open source software](https://libraries.io/nuget/Microsoft.Extensions.Http.Resilience)
49. [Maven Repository: io.github.resilience4j](https://mvnrepository.com/artifact/io.github.resilience4j)
50. [Release v4.1.0 - Suzumushi Release · Yamato-Security/hayabusa · GitHub](https://github.com/Yamato-Security/hayabusa/releases/tag/v4.1.0)
51. [Release v4.3.0 - Vulnpocalypse Release · Yamato-Security/hayabusa · GitHub](https://github.com/Yamato-Security/hayabusa/releases/tag/v4.3.0)
52. [Release v4.2.0 - Autumn Release · Yamato-Security/hayabusa · GitHub](https://github.com/Yamato-Security/hayabusa/releases/tag/v4.2.0)
53. [Release v2.16.0 · WithSecureOpenSource/chainsaw · GitHub](https://github.com/WithSecureOpenSource/chainsaw/releases/tag/v2.16.0)
54. [Logs](https://opentelemetry.io/docs/concepts/signals/logs/)
55. [Status](https://opentelemetry.netlify.app/status/)
56. [Logs](https://opentelemetry.netlify.app/docs/concepts/signals/logs/)
57. [OpenTelemetry Semantic Conventions - API Evangelist Standards](https://standards.apievangelist.com/store/opentelemetry-semantic-conventions)
58. [Releases · open-telemetry/semantic-conventions · GitHub](https://github.com/open-telemetry/semantic-conventions/releases)
59. [OpenTelemetry Logs: Setup, Data Model, and Trace Correlation](https://uptrace.dev/opentelemetry/logs)
60. [Python 3.15: Lazy Imports, frozendict, and Tachyon Profiler — CODERCOPS](https://blog.codercops.com/blog/python-3-15-lazy-imports-frozendict-tachyon-profiler-2026)
61. [Python 3.15's Sampling Profiler Is the Profiling Story You Can Actually Ship - Nandann Creative Agency](https://www.nandann.com/blog/python-315-sampling-profiler)
62. [Go 1.27 Release Party: Generic Methods, JSON v2, and Day-One Tooling - The JetBrains Blog](https://blog.jetbrains.com/go/2026/08/05/new-livestream-go-127/)
63. [Python 3.15's abi3t — The Problem a Stable ABI Solves for Free-Threaded Builds, and What It Costs — TT Lab Blog](https://ttlab.hopto.org/blog/2026-07-16-python-315-abi3t-free-threaded-stable-abi?lang=en)
64. [Python 3.15 is out: is free-threading ready?](https://www.nihardaily.com/posts/python-315-hits-rc1-is-free-threading-ready-yet)
65. [Java 27 vs Java 26: What Changed Between JDK 26 and JDK 27 - Java-HandsOn](https://javahandson.com/java-27-vs-java-26/)
66. [Java 27: Every JEP Tested + the Java 26 Changes You Skipped](https://ankurm.com/java-27-every-jep-plus-java-26-changes/)
67. [.NET 8 and 9 End of Support on Nov 10, 2026: What to Do](https://sadeem.de/en/blog/dotnet-8-9-supportende-november-2026)
68. [Node.js latest version (2026): 26.13.0 LTS & end-of-life dates](https://latestat.com/nodejs)
69. [Go 1.27 Release Notes](https://daily.dev/posts/nmfkkkeoa)
70. [SUSE Package Hub - python-evtx](https://packagehub.suse.com/packages/python-evtx/)
71. [python-evtx/Evtx/Evtx.py at master · williballenthin/python-evtx · GitHub](https://github.com/williballenthin/python-evtx/blob/master/Evtx/Evtx.py)
72. [GitHub - WithSecureLabs/chainsaw: Rapidly Search and Hunt through Windows Forensic Artefacts · GitHub](https://translate.google.com/translate?u=https%3A%2F%2Fgithub.com%2FWithSecureLabs%2Fchainsaw&hl=id&sl=en&tl=id&client=srp)
