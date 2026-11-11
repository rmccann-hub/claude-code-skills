# Acceptance runs

Read this for an acceptance run that goes unattended on real hardware, such as a drive, a board,
a phone or an instrument: checks before it starts, a device lost mid-run, a product failure told
from a rig failure, retries, run tiers and the evidence a run keeps. Read it too for fault
injection in an ordinary program: a failed read, a full disk, a dropped network or low memory.

Proving any check can fail is `test-gates`; what a result is checked against is `test-oracles`;
a test that fails only sometimes on a healthy device is `flaky-tests`; the mix of unit,
integration and end-to-end tests is `testing-patterns`. A GUI's tests are user-experience's
`gui-testing`; a shorter run scoped from a diff in review rounds is agent-engineering's
`review-loops`.

## Rules

1. **Check the rig before every run, and take a device that fails out of service.** A health
   check is a short job on a fixed, known-good input that drives the device and each peripheral
   the suite needs. A device that fails runs nothing until a person clears it (facts
   `ar-lava-health`, `ar-lava-device`).
2. **Keep three outcomes apart:** the product failed a test, the rig couldn't finish, or the job
   was set up wrong. Only the first counts against the product; neither other is a pass.
3. **A device lost mid-run aborts the run with its reason.** Stop through an abort path, not an
   assertion, and record which test was running. Results already recorded stand; every test
   after the loss is counted as not run.
4. **Retry a rig failure to a fixed limit, and report the last attempt.** Never retry a product
   failure. A device that keeps failing gets its health check run in a loop, to measure how
   often (facts `ar-kci-retry`, `ar-lava-queue`).
5. **Every result names what produced it,** read from the things themselves: the build under
   test, the test code, the reference data, and the device with its health at the start.
6. **Keep the evidence to judge a result without a re-run,** for a stated time, longer for a
   release (fact `ar-openqa-evidence`).
7. **Run in tiers, each saying what it leaves out:** the health check before every run, a smoke
   run per change, the full suite nightly, and every device before a release.
8. **Two devices of each kind, at least.** With one, a device fault looks like a product fault.
9. **Inject the faults hardware can't produce on demand,** with a shim at the operating
   system's boundary, and prove the program handled each. Run the suite without injection too
   (fact `ar-appverif`).

### Classing a result

KernelCI's classes, fed by LAVA's job health (facts `ar-kci-classes`, `ar-lava-health`):

| Class | What happened | What follows |
|---|---|---|
| `FAIL` | A test reached its verdict and the product got it wrong | A product defect: file it |
| `ERROR` | The rig: a lost device, a timeout, power, a cancellation | Retry to the limit, then a health check |
| `MISS` | The job: bad configuration, parameters or submission | Fix the job; nothing ran |
| Not run | Tests after an abort | Counted and listed |

A run is green only when every test it was meant to run passed.

### What a run keeps

- **The build under test:** its version and checksum, read from the artifact, not the request.
- **The test code and reference data,** each at its exact version.
- **The device:** its identity, its health at the start, and its environment, such as `df`,
  `mount` and the attached devices (fact `ar-lava-device`).
- **The run:** the console log, a machine-readable result per test, screenshots or video where
  there's a screen, the abort reason, and what it left out.

### Fault injection per platform

| Fault | Linux | Windows | macOS |
|---|---|---|---|
| Failed read or write, full disk | libfiu on POSIX calls (fact `ar-libfiu`) | Application Verifier, FILE class | A shim in an unsigned test build, or a seam in your code |
| Low memory | An `LD_PRELOAD` shim on `malloc` | HEAP_ALLOC, VIRTUAL_ALLOC | The same as above |
| Slow or dropped network | Toxiproxy (fact `ar-toxiproxy`); tc-netem as root (fact `ar-netem`) | Toxiproxy | Toxiproxy |
| Killed mid-write | Kill the process at a known point | The same | The same |

Application Verifier's `/faults` alone covers only OLE_ALLOC and HEAP_ALLOC, its probability is
in parts per million, and its checks report in a debugger (fact `ar-appverif`). On macOS,
`DYLD_INSERT_LIBRARIES` is ignored for binaries System Integrity Protection guards, and blocked
by the hardened runtime that notarization requires (fact `ar-macos-dyld`).

A fault test asserts the specified outcome, such as the exit code and message; the state after,
such as the original file intact and no partial output; and that a next operation works. It
counts the faults injected, and zero is a failure.

## Mistakes

- **A device check inside a test.** An assertion turns a lost device into a product failure; a
  skip turns it into a pass. Assistants write both. Abort the run with the reason.
- **Re-running the whole suite until green.** Retry rig failures only, to a limit.
- **A run that stopped at test 3 of 40 reported as "3 passed".** Count the 37 not run.
- **The version taken from the request or the configuration.** Read it from the build.
- **All acceptance on one physical device.** Add a second, and a shim for faults on demand.
- **A shim that never loaded,** such as `DYLD_INSERT_LIBRARIES` on a notarized app: every fault
  test passes. Count the faults injected.
- **`/faults` expected to fail file calls, or a probability written as a percent.** Name the
  classes; write parts per million.
- **Toxiproxy's API open on a shared network.** Set its token (fact `ar-toxiproxy`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Runs start on unchecked devices | A health check before each run; failed devices kept out | `GAP` | Add both |
| A lost device reads as a pass or a product failure | Device assertions or skips inside tests; how a stopped run is counted | `BLOCKER` | An abort path; later tests counted as not run |
| Rig and product failures share a class | The report's classes against the table above | `GAP` | Separate them |
| Retries hide product failures | A retry on every failure, or no limit | `GAP` | Rig failures only, to a limit |
| Results don't name what produced them | Build version and checksum, test and reference versions, device | `GAP` | Read each from the thing itself |
| Evidence missing or kept forever | The list above, and a retention rule | `GAP` | Keep the list, for a stated time |
| One device of a kind | The rig's inventory | `GAP` | A second device, and a shim |
| Fault tests that can't fail | No count of faults injected; injection into a signed build | `BLOCKER` | Count them; use an unsigned test build |
| Runs only with injection | The suite's configurations | `GAP` | Run both |
| All of the above hold | The checks above | `OK` | None |

## Why

### A health check before the run

- **The advice:** check the device and its peripherals before any run.
- **The reason:** a broken rig yields failures that aren't the product's.
- **What others do, and why:** LAVA checks a device of unknown health before its next job, takes
  one that fails offline until an admin clears it, holds jobs when no device is healthy, and
  boots a fixed image for constant results, by default every 24 hours (facts `ar-lava-health`,
  `ar-lava-queue`, `ar-lava-device`).
- **What it costs:** minutes per run, and remote power and serial control (fact
  `ar-lava-device`).
- **When to choose differently:** a run a person sets up and watches needs a checklist instead.

### Three outcomes, aborts and retries

- **The advice:** class each result; abort on a lost device; retry the rig only.
- **The reason:** a lost device read as a failure sends a person after a bug that isn't there,
  and read as skipped turns the run green. Retrying product failures hides them.
- **What others do, and why:** LAVA keeps job health apart from test results, and a test that
  finds the rig broken ends the job as Incomplete (fact `ar-lava-device`). KernelCI maps rig
  causes to `ERROR` and job causes to `MISS`, and reports only the final retry (facts
  `ar-kci-classes`, `ar-kci-retry`).
- **What it costs:** an abort path in the harness, and a report with more than two states.
- **When to choose differently:** a person watching a run can class it by hand.

### Provenance, tiers and devices

- **The advice:** read versions from the things themselves, keep evidence, run in tiers, and
  keep two devices of each kind.
- **The reason:** acceptance runs on real hardware tested the wrong build twice, until a version
  line in every log made it checkable (F123). An audited desktop application ran all its
  acceptance on one physical drive, so a drive fault and a product fault looked the same.
- **What others do, and why:** openQA keeps video, screenshots and JSON per run, the exact
  version of the reference images, and results for a set time (fact `ar-openqa-evidence`). No
  primary source found defines tiers for device racks; the four here are this repository's own.
- **What it costs:** storage, a second device, and a smoke tier that misses what the full suite
  finds.
- **When to choose differently:** one kind of device and rare releases can run the full suite
  each time.

### Fault injection as a stand-in

- **The advice:** inject faults at the system's boundary, and run without injection too.
- **The reason:** an `LD_PRELOAD` shim that failed reads found a hang no run on a real drive
  had, and reproduced a damaged disc on demand (L11).
- **What others do, and why:** libfiu fails POSIX calls with no source change; Toxiproxy and
  tc-netem degrade a network; Microsoft says both runs are needed, since each exercises
  different code; macOS blocks injection into protected and hardened binaries (facts
  `ar-libfiu`, `ar-toxiproxy`, `ar-netem`, `ar-appverif`, `ar-macos-dyld`).
- **What it costs:** an unhardened test build on macOS, root for tc-netem, and a shim whose
  timing differs from a real fault.
- **When to choose differently:** a fault the hardware produces on demand is tested there.

## Facts

Practices, defaults and versions, each named elsewhere by its ID. Checked 2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `ar-lava-health` | A failed health check takes a device offline, on a job failure, not a test case's | [LAVA](https://gitlab.com/lava/lava/-/raw/master/doc/v2/healthchecks.rst) | "that device will be automatically taken offline" and "this applies to a job failure, not a fail result from a single lava-test-case" | 2026-11-11 | 2027-05-11 |
| `ar-lava-queue` | A device of unknown health is checked first; with none healthy, jobs wait; looping repeats the check | [LAVA](https://gitlab.com/lava/lava/-/raw/master/doc/v2/lava-scheduler-device-help.rst) | "before starting any other submitted job" and "test jobs will be held in the Queue" and "continuously submits a health check" | 2026-11-11 | 2027-05-11 |
| `ar-lava-device` | `lava-test-raise` ends a job Incomplete; golden images; a failed device waits for an admin; every 24 hours; power and serial control; log `df` | [LAVA](https://lava.readthedocs.io/en/latest/technical-references/configuration/health-check.html); [debugging](https://gitlab.com/lava/lava/-/raw/master/doc/v2/debugging.rst) | "set the job health to Incomplete" and "only use Golden image for health-checks" and "until an admin set the health" and "frequency of 24 hours" and "remote power control" and "add the output of df or mount" | 2026-11-11 | 2027-05-11 |
| `ar-lava-version` | LAVA's newest tag is 2026.10 | `git ls-remote --tags https://gitlab.com/lava/lava.git` | `refs/tags/2026.10` | 2026-11-11 | 2027-02-11 |
| `ar-kci-classes` | KernelCI: rig causes are `ERROR`, job causes `MISS` | [KernelCI](https://docs.kernelci.org/components/kci-dev/maestro-validate/) | "ERROR if error_code ∈ {Canceled, Infrastructure, LAVATimeout" and "MISS if error_code ∈ {Bug, Configuration" | 2026-11-11 | 2027-05-11 |
| `ar-kci-retry` | KernelCI reports only an incomplete job's final retry | [KernelCI](https://docs.kernelci.org/components/maestro/pipeline/pipeline-details/) | "Only the final retry attempt is sent." | 2026-11-11 | 2027-05-11 |
| `ar-openqa-evidence` | openQA: video, screenshots, JSON, the needles' version, retention | [openQA](https://open.qa/docs/) | "generates a video, screenshots and a JSON file" and "The specific version of the needles" and "Keep important results for" | 2026-11-11 | 2027-05-11 |
| `ar-libfiu` | libfiu 1.2, 2023-10-29: POSIX faults without source changes | [libfiu](https://blitiri.com.ar/p/libfiu/) | "The current version is 1.2 (released on 2023-10-29)" and "without having to modify the application's source code" | 2026-11-11 | 2027-02-11 |
| `ar-toxiproxy` | Toxiproxy 2.13.0, 2026-10-14: an optional API token, and a warning when the API is open | [Changelog](https://raw.githubusercontent.com/Shopify/toxiproxy/main/CHANGELOG.md) | "[2.13.0] - 2026-10-14" and "Add optional bearer token auth" and "warn when the API is unauthenticated" | 2026-11-11 | 2027-02-11 |
| `ar-netem` | tc-netem delays, drops, duplicates and corrupts packets | [tc-netem(8)](https://man7.org/linux/man-pages/man8/tc-netem.8.html) | "delay, loss, duplication, and packet corruption" | 2026-11-11 | 2027-05-11 |
| `ar-appverif` | Application Verifier: `/faults` covers two classes, run with and without, parts per million, report in a debugger | [Testing](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/application-verifier-testing-applications); [FAQ](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/application-verifier-faqs) | "just for OLE_ALLOC and HEAP_ALLOC" and "both scenarios must be run" and "changed to parts per million" and "have no crashes, then they are not reporting any problems" | 2026-11-11 | 2027-05-11 |
| `ar-macos-dyld` | dyld ignores `DYLD_*` under SIP; the hardened runtime needs an exception; notarization needs it | [dyld(1)](https://raw.githubusercontent.com/apple-oss-distributions/dyld/main/doc/man/man1/dyld.1); [entitlement](https://developer.apple.com/tutorials/data/documentation/bundleresources/entitlements/com.apple.security.cs.allow-dyld-environment-variables.json); [runtime](https://developer.apple.com/tutorials/data/documentation/security/hardened-runtime.json) | "these environment variables are ignored" and "select Allow DYLD Environment Variables" and "you must enable the Hardened Runtime capability" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| LAVA's documentation and source (fact `ar-lava-version`) | Health checks, job health | © Linaro; repository GPL-2.0: short quotes |
| KernelCI's documentation | Classes, retries | CC BY 4.0: quoted with attribution |
| openQA's documentation | Evidence, retention | GPL-2.0: short quotes |
| libfiu; Toxiproxy | Fault injection | Public domain; MIT |
| tc-netem(8) | Network faults | Not stated: short quote |
| Microsoft Learn | Application Verifier | CC BY 4.0: quoted with attribution |
| dyld(1); Apple's documentation | macOS limits | Not checked; all rights reserved: short quotes |
| Audits, unnamed here (L11, F123) | Shims, one device, provenance | Our own words |
