# Performance and concurrency

Read this for finding why code is slow and proving a change made it faster: profilers and their
modes, flame graphs, and benchmark harnesses and their pitfalls. It also covers concurrent code:
task lifetimes, cancellation, blocking an event loop, race detectors, free threading and Java's
structured concurrency. Caching, data structures and complexity, and the statistics for
comparing benchmark runs aren't covered yet: its research found no sources.

Each language's async style is its language module's: `python-coding`, `javascript-coding`,
`csharp-coding` (`ConfigureAwait` in apps among it), `bash-coding` and `c-coding`. Timeouts,
retries and circuit breakers are `error-handling`'s; ThreadSanitizer is `c-build`'s. A test that
flakes from a race is `flaky-tests`, and a timing test in CI `ci-speed`.

## Rules

1. **Measure before you change anything for speed.** Profile the symptom, and keep the number
   from before to compare with the one after.
2. **Profile with a sampler first:** its overhead is bounded, and it can attach to a running
   process. A tracing profiler inflates small, hot calls: use it for exact call counts.
3. **Choose wall-clock or CPU mode from the symptom.** Wall-clock counts waiting on I/O, locks
   and sleep, for slow responses; CPU mode, for a busy CPU. High in wall-clock and low in CPU
   means waiting (fact `pc-py-modes`).
4. **Read a flame graph's widths, never its order.** The x-axis is alphabetical (fact
   `pc-flamegraph`), and call counts and outliers don't show. For a timeline, use a flame chart,
   such as a browser's performance panel.
5. **Benchmark with the language's harness,** which warms up, forks fresh processes and keeps the
   compiler from deleting the work. Never time a hand-written loop.
6. **Give every concurrent task an owner that waits for it:** a task group or scope, which
   cancels the rest when one fails.
7. **Treat cancellation as cooperative:** pass the token or context down, check it in long loops,
   and never swallow the cancellation error.
8. **Never block an event loop or an async runtime's thread.** CPU work goes to a worker or
   thread pool, blocking calls to the runtime's blocking pool.
9. **Run the race detector in CI, with tests that reach the concurrent paths.**
10. **A cache gets an owner, an invalidation rule and a size bound.**

### Tools per language

| Language | Profile | Benchmark | Facts |
|---|---|---|---|
| Python | `profiling.sampling` on 3.15, else py-spy; `profiling.tracing` for counts | `timeit` | `pc-py-tachyon`, `pc-py-spy` |
| Node.js | `node --cpu-prof`, not clinic.js | Not researched | `pc-node-cpu-prof`, `pc-clinic` |
| .NET | dotnet-trace, dotnet-counters | BenchmarkDotNet | `pc-dotnet-diag` |
| Go | `go tool pprof`, with the `goroutineleak` profile | `b.Loop()` | `tp-go`, `pc-go-leak`, `pc-go-bloop` |
| Rust | `cargo flamegraph` | criterion | `pc-rust-bench` |
| JVM | async-profiler | JMH | `pc-async-profiler`, `pc-jmh` |

### Benchmarks

- **Warm-up and forks.** A JIT runs code slowly until it compiles it, and one benchmark's state
  leaks into the next in one process. Keep JMH's default forks (fact `pc-jmh`).
- **A sink for the result,** or the compiler may delete the work: Go's `b.Loop()` (fact
  `pc-go-bloop`), Rust's `std::hint::black_box` (fact `pc-rust-bench`), JMH's `Blackhole` or a
  returned value (fact `pc-jmh`).

### Concurrency per language

- **Python.** `asyncio.TaskGroup`, not `gather`; re-raise `CancelledError` (fact
  `pc-py-taskgroup`). Free threading is opt-in (fact `pc-py-free-threading`), not thread safety.
- **Node.js.** Workers are for CPU-heavy JavaScript, not I/O (fact `pc-node-workers`).
- **C#.** `ConfigureAwait(false)` in libraries (fact `cs-configureawait`). Await a `ValueTask`
  once; pass the `CancellationToken` down, with `ThrowIfCancellationRequested()` in long loops
  (fact `pc-dotnet-async`).
- **Go.** `go test -race` (fact `pc-go-race`); the `goroutineleak` profile finds goroutines
  blocked forever (fact `pc-go-leak`).
- **Rust.** Fix a `Send` or `Sync` error by changing the type, such as to `Arc<Mutex<T>>`, not
  with `unsafe impl`. In tokio, blocking goes to `spawn_blocking` (fact `pc-rust-async`).
- **Java.** Virtual threads are final (fact `pc-java-vt`). `StructuredTaskScope` is a preview
  in JDK 27, behind `--enable-preview`, to be final in JDK 28 unchanged (fact `pc-java-sc`):
  `StructuredTaskScope.open()` with a `Joiner`, catching `ExecutionException`.

## Mistakes

- **Optimizing the function that looks slow.** Profile: the time is often elsewhere.
- **Pointing Tachyon at a 3.14 process.** It needs the target's minor version: use py-spy.
- **`except asyncio.CancelledError: pass` in a coroutine.** Task groups and timeouts break.
- **`time.sleep` in `async def`, `std::thread::sleep` in a tokio task.** That thread stalls.

Assistants still write these five, from older code and articles:

- **Reading a flame graph left to right as time.** The order is alphabetical.
- **Recommending clinic.js.** It's unmaintained: use `node --cpu-prof`.
- **`for i := 0; i < b.N; i++` in a new Go benchmark.** Write `for b.Loop()`.
- **`criterion::black_box`.** Use `std::hint::black_box`.
- **`new StructuredTaskScope.ShutdownOnFailure()` with `throwIfFailed()`,** the JDK 21 to 24
  preview, or calling it final in JDK 27. Write the JDK 27 shape.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A speed change with no numbers | No profile or before and after | `GAP` | Rules 1 to 3 |
| A hand-timed benchmark | A timer around a loop; `b.N` loops in new Go | `DRIFT` | The harness |
| An unused benchmark result | No `b.Loop()`, `black_box`, `Blackhole` or return | `BLOCKER` where CI gates on it, else `DRIFT` | A sink |
| A task with no owner | A dropped `create_task` result or `Task`; a `go` nothing stops | `GAP` | A group or scope |
| Swallowed cancellation | `CancelledError` caught and not re-raised | `DRIFT` | Re-raise |
| Blocking in async code | `time.sleep`, synchronous I/O or `.Result` there | `DRIFT` | Await, or the blocking pool |
| No race detector | A Go module's CI without `-race` | `GAP` | `go test -race ./...` |
| An old preview API | `ShutdownOnFailure`, `throwIfFailed` | `DRIFT` | `open()` and a `Joiner` |
| An unbounded cache | A memo map with no limit, expiry or owner | `GAP` | Rule 10 |

## Why

### Measure first, with a sampler, in the right mode

- **The reason:** a guess optimizes code that wasn't slow. The modes tell waiting from
  computing (fact `pc-py-modes`).
- **What it costs:** a profiling run; a sampler can miss a short, rare call.
- **When to choose differently:** a tracing profiler for exact call counts.

### Benchmark with the harness

- **The reason:** without warm-up you time the interpreter, and without a sink the compiler
  deletes the work (facts `pc-go-bloop`, `pc-rust-bench`, `pc-jmh`).
- **What it costs:** at JMH's defaults, about eight minutes per benchmark.
- **When to choose differently:** fewer forks while exploring, never for a number you publish.

### Owned tasks and cooperative cancellation

- **The reason:** a task nobody waits for loses its error or never ends: Go now profiles leaked
  goroutines (fact `pc-go-leak`). Code that never checks its token never stops (fact
  `pc-dotnet-async`).
- **What others do:** Java is moving to structured concurrency (fact `pc-java-sc`).
- **What it costs:** fire-and-forget gets harder, on purpose.
- **When to choose differently:** work that outlives a request gets a long-lived owner that
  stops it at shutdown.

### Event loops, race detectors and previews

- **Event loops:** tasks share a thread, so one blocking call stalls every task on it (facts
  `pc-node-workers`, `pc-rust-async`). A worker costs startup and copying.
- **Race detectors:** a silent run says nothing about code that didn't run (fact `pc-go-race`).
- **Previews:** JDK 25 and 27 each broke the last preview's code (fact `pc-java-sc`), so
  production code waits for JDK 28.
- **Free threading:** opt-in (fact `pc-py-free-threading`); measure before relying on it.
- **`Send` and `Sync`:** our practice: never `unsafe impl` them to quiet the compiler, which
  turns off its check for data races.

### Caches

This repository's practice, not researched: a cache with no bound grows until memory runs out,
one with no invalidation rule serves stale data, and one with no owner is never fixed.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `pc-flamegraph` | A flame graph's x-axis is alphabetical, not time | [Flame graphs](https://www.brendangregg.com/flamegraphs.html) | "sorted alphabetically (it is not the passage of time)" | 2026-11-11 | 2027-05-11 |
| `pc-py-modes` | High in wall-clock and low in CPU mode means waiting | [profiling.sampling](https://docs.python.org/3/library/profiling.sampling.html) | "If a function is high in wall-clock mode but low or absent in CPU mode, it is I/O-bound or waiting." | 2026-11-11 | 2027-05-11 |
| `pc-py-tachyon` | 3.15 adds Tachyon; it profiles only its own minor version | [What's new in 3.15](https://docs.python.org/3/whatsnew/3.15.html), [profiling.sampling](https://docs.python.org/3/library/profiling.sampling.html) | "A new statistical sampling profiler (Tachyon) has been added as profiling.sampling." and "must run the same Python minor version" | 2026-11-11 | 2027-02-11 |
| `pc-py-spy` | py-spy 0.4.3 (2026-11-02) | [PyPI](https://pypi.org/pypi/py-spy/json) | "\"version\":\"0.4.3\"" | 2026-11-11 | 2027-02-11 |
| `pc-py-free-threading` | Free threading: supported but optional since 3.14 | [What's new in 3.14](https://docs.python.org/3/whatsnew/3.14.html) | "officially supported but still optional." | 2026-11-11 | 2027-02-11 |
| `pc-py-taskgroup` | TaskGroup cancels the rest, `gather` doesn't; a swallowed `CancelledError` breaks it | [asyncio](https://docs.python.org/3/library/asyncio-task.html) | "TaskGroup will, while gather will not, cancel the remaining scheduled tasks." and "might misbehave if a coroutine swallows asyncio.CancelledError." | 2026-11-11 | 2027-05-11 |
| `pc-node-cpu-prof` | `--cpu-prof` writes a V8 CPU profile | [Node CLI](https://nodejs.org/api/cli.html) | "writes the CPU profile to disk before exit." | 2026-11-11 | 2027-05-11 |
| `pc-clinic` | clinic.js is unmaintained | [README](https://raw.githubusercontent.com/clinicjs/node-clinic/main/README.md) | "Clinic.js is not being actively maintained." | 2026-11-11 | 2027-02-11 |
| `pc-node-workers` | Workers help CPU-bound JavaScript, not I/O | [Workers](https://nodejs.org/api/worker_threads.html) | "They do not help much with I/O-intensive work." | 2026-11-11 | 2027-05-11 |
| `pc-dotnet-diag` | dotnet-trace, dotnet-counters 10.0.750501 (2026-10-07); `dnx` runs counters | [Learn](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters), [NuGet](https://www.nuget.org/packages/dotnet-trace) | "you can run dotnet-counters without permanent installation using dnx" | 2026-11-11 | 2027-02-11 |
| `pc-dotnet-async` | A `ValueTask` is awaited once; cancellation is cooperative | [ValueTask](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask?view=net-10.0), [cancellation](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads) | "may only be awaited once" and "Cancellation is cooperative" | 2026-11-11 | 2027-05-11 |
| `pc-go-bloop` | Prefer `B.Loop` (Go 1.24), which keeps values alive | [testing](https://pkg.go.dev/testing) | "New benchmarks should prefer using B.Loop" and "preventing the compiler from fully optimizing away the loop body." | 2026-11-11 | 2027-05-11 |
| `pc-go-race` | `-race` finds only races in code that runs | [Race detector](https://go.dev/doc/articles/race_detector) | "it can't find races in code paths that are not executed." | 2026-11-11 | 2027-05-11 |
| `pc-go-leak` | Go 1.27 made the goroutine leak profile generally available | [Go 1.27](https://go.dev/doc/go1.27) | "is now generally available." and "named goroutineleak" | 2026-11-11 | 2027-02-11 |
| `pc-rust-bench` | criterion 0.8.2 (2026-02-04) takes std's `black_box`; cargo-flamegraph 0.6.15 (2026-11-02) | [criterion](https://raw.githubusercontent.com/criterion-rs/criterion.rs/master/CHANGELOG.md), [flamegraph](https://crates.io/api/v1/crates/flamegraph) | "should switch to `std::hint::black_box()`." and "\"max_stable_version\":\"0.6.15\"" | 2026-11-11 | 2027-02-11 |
| `pc-rust-async` | `Send`; tokio 1.54.1 (2026-10-21) tasks must not block | [marker](https://doc.rust-lang.org/std/marker/index.html), [tokio](https://docs.rs/tokio/latest/tokio/task/) | "Types that can be transferred across thread boundaries." and "could block a thread" | 2026-11-11 | 2027-02-11 |
| `pc-async-profiler` | async-profiler 4.6 (2026-10-20) removed the HTTP server; 4.5 added JDK 27 | [Changelog](https://raw.githubusercontent.com/async-profiler/async-profiler/v4.6/CHANGELOG.md) | "#1776: Remove embedded HTTP server" and "#1765: JDK 27 support" | 2026-11-11 | 2027-02-11 |
| `pc-jmh` | JMH 1.37 (2023-08-03): 5 forks of 5 warm-up and 5 measured 10 s runs; `Blackhole` | [Defaults](https://raw.githubusercontent.com/openjdk/jmh/1.37/jmh-core/src/main/java/org/openjdk/jmh/runner/Defaults.java), [Blackhole](https://raw.githubusercontent.com/openjdk/jmh/1.37/jmh-core/src/main/java/org/openjdk/jmh/infra/Blackhole.java) | "MEASUREMENT_FORKS = 5;" and "preventing JIT to eliminate dependent computations." | 2026-11-11 | 2027-02-11 |
| `pc-java-vt` | Virtual threads final in JDK 21 | [JEP 444](https://openjdk.org/jeps/444) | "finalize virtual threads in JDK 21" | 2026-11-11 | 2027-05-11 |
| `pc-java-sc` | Factories from JDK 25; `ExecutionException` in 27; final in 28, GA planned 2027-03-09 | [JEP 543](https://openjdk.org/jeps/543), [JEP 533](https://openjdk.org/jeps/533), [JDK 28](https://openjdk.org/projects/jdk/28/) | "replaced with static factory methods." and "throw an ExecutionException" and "finalize Structured Concurrency in JDK 28, without further change." | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Python](https://docs.python.org/3/), [Node.js](https://nodejs.org/api/) | Profilers, async, workers | PSF-2.0; MIT: quoted |
| [Learn](https://learn.microsoft.com/en-us/dotnet/), [Go](https://go.dev/doc/) | .NET and Go | CC BY 4.0: quoted with attribution |
| [Rust std](https://doc.rust-lang.org/std/), [tokio](https://docs.rs/tokio/) | `Send`, blocking | MIT or Apache-2.0; MIT: quoted |
| criterion, async-profiler, clinic.js | Changes | Apache-2.0 or MIT; Apache-2.0; MIT: quoted |
| [PyPI](https://pypi.org/), [crates.io](https://crates.io/), [NuGet](https://www.nuget.org/) | Versions | Facts only |
| [OpenJDK JEPs](https://openjdk.org/jeps/0), [JMH](https://github.com/openjdk/jmh) | Java | GPLv2, JMH with Classpath exception: brief quotes |
| [Brendan Gregg](https://www.brendangregg.com/flamegraphs.html) | Flame graphs | None stated: brief quotes |
