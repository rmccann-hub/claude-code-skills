# C# coding

Read this for writing, reviewing or fixing C# on modern .NET: choosing a target framework,
nullable warnings, shared build settings, analyzers, async code, disposal, `HttpClient`, JSON,
NativeAOT and trimming, P/Invoke, and the security mistakes particular to C#.

Windows Server and Active Directory administration belong to the planned windows-admin module,
and PowerShell to `powershell-scripts`. Test design belongs to the planned testing skill. Package
choice, audits and lockfiles belong to the security skill's supply-chain-security module and to
project-bootstrap-and-audit, whose *Language toolchains* table says which .NET to pin. Every C#
example here compiled on 2026-10-26 with the .NET 10.0.403 SDK, under this module's own settings:
nullable on, `latest-Recommended` analysis and warnings as errors. CI has no C# checker, so it
doesn't compile them again.

## Contents

- [Rules](#rules)
- [Mistakes](#mistakes)
- [Audit](#audit)
- [Why](#why)
- [Facts](#facts)
- [Sources](#sources)

## Rules

1. **Target a supported .NET:** `net10.0` for new work, and let the target framework choose the
   C# version.
2. **Nullable on and warnings as errors,** set once in `Directory.Build.props`, with package
   versions in `Directory.Packages.props`.
3. **Run the analyzers and `dotnet format` in the build and in CI.**
4. **Async all the way down:** no `async void` outside event handlers, no `.Result` or `.Wait()`,
   and a `CancellationToken` passed on. `ConfigureAwait(false)` belongs in library code only.
5. **Dispose what you create,** with `using` and `await using`, and reuse `HttpClient`.
6. **Serialize with System.Text.Json.** Never `BinaryFormatter`, or a Newtonsoft.Json
   `TypeNameHandling` other than `None`, on data from outside.
7. **Outside input never builds a command:** SQL takes parameters, a process takes
   `ArgumentList` without a shell, and a path is resolved and checked against its root.
8. **NativeAOT and trimming only where startup time or size matter,** with their warnings fixed.
9. **P/Invoke through `LibraryImport`,** with the exact entry point name, `SafeHandle` for owned
   handles, and the error read straight after the call.

### Project setup

- **The target framework.** .NET 8 and .NET 9 both leave support on the same day (fact
  `cs-dotnet8-9-end`), so move to 10, the LTS release (fact `cs-dotnet10-lts`). .NET 11 is a
  go-live release candidate, not a release (fact `cs-dotnet11-rc`): check the support policy
  before targeting it. Only a release's latest patch is supported (fact `cs-support-policy`).
- **The C# version follows the target framework** (fact `cs-langversion-default`). Leave
  `LangVersion` unset, and never set it to `latest` (fact `cs-langversion-latest`). Where builds
  must use one SDK, pin it in `global.json` with `rollForward` (fact `cs-global-json`).
- **Shared settings go in `Directory.Build.props`** at the repository root, which MSBuild imports
  into every project below it (fact `cs-build-props`). Its name is case-sensitive on Linux.

  ```xml
  <Project>
    <PropertyGroup>
      <Nullable>enable</Nullable>
      <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
      <AnalysisLevel>latest-Recommended</AnalysisLevel>
      <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    </PropertyGroup>
  </Project>
  ```

- **Nullable warnings.** New templates turn nullable on (fact `cs-nullable-template`), but
  warnings don't fail a build by default (fact `cs-warnaserror`). Where a codebase isn't ready,
  `<WarningsAsErrors>Nullable</WarningsAsErrors>` makes only the nullability warnings errors.
  The `!` operator silences a warning and checks nothing at run time.
- **Central package management:** `ManagePackageVersionsCentrally` set to `true`, a
  `PackageVersion` for each package in `Directory.Packages.props`, and `PackageReference` items
  with no `Version` (fact `cs-cpm`).
- **Analyzers and formatting.** Code analysis is on for .NET 5 and later, but only a few rules
  warn (fact `cs-analysis-default`). `AnalysisLevel` raises the set, `EnforceCodeStyleInBuild`
  runs the `.editorconfig` style rules on build (fact `cs-analysis-default`), and in CI
  `dotnet format --verify-no-changes` fails when a file would change (fact `cs-format-verify`).

### Async and disposal

- **`async void` only for event handlers:** an exception in one can't be caught by the caller
  (fact `cs-async-void`).
- **Never block on a task.** `.Result`, `.Wait()` and `.GetAwaiter().GetResult()` can deadlock
  (fact `cs-async-void`). Make the caller async, and pass the token on:

  ```csharp
  // Wrong: blocks a thread, and can deadlock under a UI synchronization context.
  // string body = client.GetStringAsync(uri).Result;

  // Right: awaits, and lets the caller cancel.
  string body = await client.GetStringAsync(uri, cancellationToken);
  ```

- **`ConfigureAwait(false)` in general-purpose libraries, not in apps** (facts
  `cs-configureawait`, `cs-ca2007-apps`). In a WinForms or WPF handler, code after it may run off
  the UI thread.
- **`await using` for anything `IAsyncDisposable`,** which calls `DisposeAsync` (fact
  `cs-await-using`), as in `await using FileStream stream = File.OpenRead(path);`.
- **One long-lived `HttpClient`, or clients from `IHttpClientFactory`.** Each client owns a
  connection pool, so one per request can exhaust ports, and a long-lived one needs
  `PooledConnectionLifetime` to see DNS changes (fact `cs-httpclient-reuse`). A typed client held
  by a singleton is a hazard (fact `cs-typed-client-singleton`).

  ```csharp
  private static readonly HttpClient s_client = new(new SocketsHttpHandler
  {
      PooledConnectionLifetime = TimeSpan.FromMinutes(2),
  });
  ```

### Data and outside input

- **System.Text.Json:** reuse one `JsonSerializerOptions` (fact `cs-stj-options`). Under
  NativeAOT or trimming, serialize through a source-generated context; reflection-based
  serialization is off when `PublishTrimmed` is on (fact `cs-stj-reflection`).

  ```csharp
  [JsonSerializable(typeof(Order))]
  internal sealed partial class AppJsonContext : JsonSerializerContext
  {
  }

  Order? order = JsonSerializer.Deserialize(json, AppJsonContext.Default.Order);
  ```

- **No `BinaryFormatter`:** it can't be made secure, and from .NET 9 it throws on use (fact
  `cs-binaryformatter`). Newtonsoft.Json's `TypeNameHandling` lets the data choose the type to
  create, so keep it `None` (fact `cs-typenamehandling`).
- **SQL takes parameters,** such as `@id` with `command.Parameters.Add`, never text built from
  input, interpolated strings included (fact `cs-sql-params`).
- **Processes start without a shell.** `UseShellExecute` is `false` by default on .NET, but
  `true` on .NET Framework (fact `cs-shellexecute`). Pass each value as one `ArgumentList` item,
  which escapes it (fact `cs-argumentlist`), never inside a `cmd.exe /c` or `sh -c` string. A
  value starting with `-` can still be read as an option by the program.
- **Paths from input are resolved, then checked.** `Path.Combine` drops everything before a
  rooted argument (fact `cs-path-combine`), and neither it nor `Path.Join` stops `..`:

  ```csharp
  string root = Path.GetFullPath(uploadDirectory);
  if (!Path.EndsInDirectorySeparator(root))
  {
      root += Path.DirectorySeparatorChar;
  }
  string full = Path.GetFullPath(fileName, root);
  if (!full.StartsWith(root, StringComparison.Ordinal))
  {
      throw new UnauthorizedAccessException("The path is outside the upload directory.");
  }
  ```

### Ahead-of-time compilation, trimming and interop

- **NativeAOT** starts faster and uses less memory, but allows no dynamic loading and no runtime
  code generation (fact `cs-aot-limits`). Set `PublishAot` in the project file, so its analysis
  runs on every build, and fix each warning. A library sets `IsAotCompatible`.
- **WinForms and WPF can't be trimmed:** the SDK disables it (fact `cs-trim-ui`).
- **`LibraryImport`** generates the marshalling at compile time, and needs `AllowUnsafeBlocks`.
  It has no `ExactSpelling`, so the name or `EntryPoint` is the export's exact name, with the
  `W` where a function has `A` and `W` forms (fact `cs-libraryimport`).
- **Read the error at once:** `SetLastError = true`, then `Marshal.GetLastPInvokeError()` before
  any other call, logging included (facts `cs-pinvoke-error`, `cs-getlastpinvokeerror`). A
  handle you must close goes in a `SafeHandle` (fact `cs-pinvoke-error`).

  ```csharp
  internal static partial class NativeMethods
  {
      [LibraryImport("kernel32.dll", EntryPoint = "GetModuleHandleW", SetLastError = true,
          StringMarshalling = StringMarshalling.Utf16)]
      internal static partial nint GetModuleHandle(string? moduleName);
  }

  nint module = NativeMethods.GetModuleHandle("user32.dll");
  if (module == 0)
  {
      throw new Win32Exception(Marshal.GetLastPInvokeError());
  }
  ```

## Mistakes

- **Targeting `net8.0` because older examples do,** or `net9.0` "for support": both end on the
  same day (fact `cs-dotnet8-9-end`). Target `net10.0`.
- **`async void` on a helper, or `.Result` in a sync wrapper.** Exceptions escape, or the thread
  deadlocks. Return `Task`, and await it all the way up.
- **`ConfigureAwait(false)` on every await in app code.** UI code after it may run on the wrong
  thread.
- **`new HttpClient()` per request, or `new JsonSerializerOptions` per call.** Share one instance.
- **Re-enabling `BinaryFormatter` with a compatibility switch,** which .NET 9 removed (fact
  `cs-binaryformatter`). Move to a serializer that doesn't take types from the data.
- **SQL built with `$"... WHERE Name = '{name}'"`, or `Process.Start("cmd.exe", "/c " + input)`.**
  Input then rewrites the command. Use a parameter, or `ArgumentList` with no shell.
- **`Path.Combine(root, userInput)` as a guard.** An absolute input replaces the root, and `..`
  climbs out. Resolve and check.
- **No `W` on a `LibraryImport` name,** from advice written for `DllImport`, which looks for the
  `W` export while `ExactSpelling` is false. `LibraryImport` doesn't (fact `cs-libraryimport`),
  so the call fails at run time.
- **`PublishTrimmed` on WinForms or WPF, or `IL2` and `IL3` warnings suppressed** to pass a
  build. The first isn't supported (fact `cs-trim-ui`); the second hides code that breaks after
  publishing.
- **System.CommandLine code with `SetHandler` and `InvocationContext`,** from samples older than
  its breaking changes. It now uses `SetAction` and `ParseResult` (fact `cs-commandline-api`).
- **A package an assistant named without checking it exists.** Look it up on nuget.org first; the
  supply-chain-security module has the rest.

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Supported target | `TargetFramework` and `TargetFrameworks` in each project and in `Directory.Build.props` | `GAP` for `net8.0`, `net9.0` or older (fact `cs-dotnet8-9-end`) | Move to `net10.0` |
| Language version | `LangVersion` set to `latest` or `preview` | `DRIFT` | Remove it (fact `cs-langversion-latest`) |
| Nullable on | `Nullable` is `enable` for every project | `GAP` where it's off | Enable it in `Directory.Build.props`, with `WarningsAsErrors` set to `Nullable` while migrating |
| Warnings fail the build | `TreatWarningsAsErrors`, or `-warnaserror` in CI | `GAP` | Set it in `Directory.Build.props` |
| One home for versions | `Version` on `PackageReference` while `Directory.Packages.props` exists | `DRIFT` | Move each version to a `PackageVersion` (fact `cs-cpm`) |
| Format checked | `dotnet format --verify-no-changes` in CI | `GAP` | Add it (fact `cs-format-verify`) |
| Async misuse | `async void` outside event handlers; `.Result`, `.Wait()`, `GetAwaiter().GetResult()` | `GAP` | Return `Task`, and await |
| `HttpClient` per call | `new HttpClient(` inside a method that runs per request | `GAP` | One shared client with `PooledConnectionLifetime`, or `IHttpClientFactory` |
| Unsafe deserialization | `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer`; `TypeNameHandling` other than `None` | `BLOCKER` on data from outside | System.Text.Json (facts `cs-binaryformatter`, `cs-typenamehandling`) |
| SQL from strings | `CommandText` or `FromSqlRaw` built by concatenation or interpolation | `BLOCKER` where input reaches it | Parameters (fact `cs-sql-params`) |
| Shell commands | `UseShellExecute = true`, `cmd.exe /c` or `sh -c` with input | `BLOCKER` where input reaches it | `ArgumentList`, no shell (fact `cs-argumentlist`) |
| Paths from input | `Path.Combine` or `Path.Join` with request data, no containment check | `BLOCKER` where input reaches it | Resolve and check against the root |
| Suppressed AOT and trim warnings | `NoWarn` holding `IL2` or `IL3` codes | `DRIFT` | Fix the code, or annotate it |

## Why

### A supported target, and the C# version it brings

**The advice.** Target `net10.0`, leave `LangVersion` alone, and keep patches current.

**Why.** An unsupported runtime gets no security fixes. LTS releases get three years and STS
releases two (fact `cs-support-policy`), so .NET 8 and 9 end together (fact `cs-dotnet8-9-end`).
The compiler picks the C# version the target framework's runtime supports (fact
`cs-langversion-default`).

**What it costs.** A move every two years on STS, or three on LTS. An odd-numbered release such
as 11 is STS: a year later than 10, with a year less support, it gains no time over 10.

**When to choose differently.** A library still used on older frameworks can multi-target, such
as `netstandard2.0` beside `net10.0`, if it builds and tests each.

### Nullable, warnings as errors, and one place for settings

**The advice.** Nullable on and warnings as errors in `Directory.Build.props`; versions in
`Directory.Packages.props`.

**Why.** A warning that doesn't fail a build gets ignored, and nullable warnings are the
compiler's only check on null. Settings copied into each project drift apart (facts
`cs-build-props`, `cs-cpm`).

**What others do.** Some projects pass `-warnaserror` in CI only, so a local build with a stray
warning still runs. That switch reaches every MSBuild task, where `TreatWarningsAsErrors` reaches
only the compiler (fact `cs-warnaserror`).

**What it costs.** A new SDK brings new rules, and can break a build on upgrade (fact
`cs-analysis-default`). A numeric `AnalysisLevel` chooses the moment.

**When to choose differently.** A large old codebase turns nullable on a project, or a file with
`#nullable enable`, at a time, with only `Nullable` warnings as errors meanwhile.

### Async all the way

**The advice.** No `async void` but event handlers, no blocking, tokens passed on, and
`ConfigureAwait(false)` in libraries only.

**Why.** Blocking under a synchronization context waits on a thread that is itself waiting, and
an exception in `async void` reaches no caller (fact `cs-async-void`).
Library code can't know its context, so it shouldn't depend on one; app code usually does (facts
`cs-configureawait`, `cs-ca2007-apps`).

**What it costs.** Async spreads up the call stack, and a synchronous interface that can't change
needs a careful bridge.

**When to choose differently.** ASP.NET Core has no synchronization context (fact
`cs-configureawait`), so blocking there is less prone to deadlock. It still holds a thread, so
the rule stands.

### Serialization and outside input

**The advice.** No type names from the data, SQL parameters, `ArgumentList` without a shell, and
contained paths.

**Why.** Each stops data becoming code. A serializer that lets the payload pick the type can be
made to run code (facts `cs-binaryformatter`, `cs-typenamehandling`), and concatenated SQL or
shell text lets input change the command. `Path.Combine` assumes trusted parts (fact
`cs-path-combine`).

**What others do.** Microsoft's analyzers flag several, such as CA2100 for SQL and CA2326 for
`TypeNameHandling`. The safe form costs little: it's as short as the unsafe one.

### Ahead-of-time compilation, trimming and interop

**The advice.** AOT where startup or size matter, with every warning fixed; `LibraryImport` for
new P/Invoke.

**Why.** An AOT or trim warning marks code that may fail only after publishing, while the JIT
build under the debugger works (fact `cs-stj-reflection`). `LibraryImport`'s marshalling is
generated at compile time, so trimming and AOT see it (fact `cs-libraryimport`).

**What it costs.** No reflection-heavy libraries, no runtime code generation, and a publish for
each platform (fact `cs-aot-limits`).

**When to choose differently.** A long-running service gains little from faster startup; publish
it framework-dependent. Working `DllImport` code can stay until the project moves to AOT.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cs-dotnet10-lts` | .NET 10, released 2025-11-11, is LTS and supported until 2028-11-14 | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | ".NET 10 November 11, 2025" and "LTS Active November 14, 2028" | 2026-10-26 | 2027-04-26 |
| `cs-dotnet8-9-end` | .NET 8 (LTS) and .NET 9 (STS) both end on 2026-11-10 | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | "STS Maintenance November 10, 2026" and "LTS Maintenance November 10, 2026" | 2026-10-26 | 2027-04-26 |
| `cs-dotnet11-rc` | .NET 11 is at RC2, a go-live release, and not yet released | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | ".NET 11 RC2 October 13, 2026" | 2026-10-26 | 2027-04-26 |
| `cs-support-policy` | LTS releases get three years of support, STS releases two, and odd-numbered releases are STS; support requires the latest patch | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | "LTS releases get free support and patches for three years. STS releases get free support and patches for two years." and "Odd numbered releases are STS releases" and "Customers choosing LTS need the latest patch update installed to qualify for support." | 2026-10-26 | 2027-04-26 |
| `cs-langversion-default` | The default C# version follows the target framework: C# 14 for .NET 10 | [Language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning) | ".NET 10.x C# 14" | 2026-10-26 | 2027-04-26 |
| `cs-langversion-latest` | Microsoft warns against `LangVersion` set to `latest` | [Configure language version](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version) | "Don't set the LangVersion element to latest." | 2026-10-26 | 2027-10-26 |
| `cs-global-json` | `global.json` can pin an SDK and allow later feature bands with `rollForward` | [global.json overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) | "The roll-forward policy to use when selecting an SDK version" | 2026-10-26 | 2027-10-26 |
| `cs-build-props` | `Directory.Build.props` at the root applies to every project below it | [Customize by directory](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory) | "You can add a new property to every project by defining it in a single file called Directory.Build.props in the root folder that contains your source." | 2026-10-26 | 2027-10-26 |
| `cs-nullable-template` | New .NET templates turn nullable reference types on | [Nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references) | "Projects created from recent .NET templates set" | 2026-10-26 | 2027-10-26 |
| `cs-warnaserror` | Warnings don't fail a build by default; `Nullable` names every nullability warning; `TreatWarningsAsErrors` reaches only the compiler, `-warnaserror` every task | [Errors and warnings options](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/errors-warnings) | "By default, TreatWarningsAsErrors isn't in effect" and "The set of all nullability warnings can be specified with the Nullable shorthand." and "TreatWarningsAsErrors only impacts the C# compiler, not any other MSBuild tasks in your csproj file. The warnaserror command line switch impacts all tasks." | 2026-10-26 | 2027-10-26 |
| `cs-cpm` | Central package management keeps versions in `Directory.Packages.props` | [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) | "set the MSBuild property ManagePackageVersionsCentrally to true" | 2026-10-26 | 2027-10-26 |
| `cs-analysis-default` | Code analysis is on for .NET 5 and later, with few rules as warnings; `AnalysisLevel` defaults to `latest`; `EnforceCodeStyleInBuild` runs style rules on build | [Code analysis overview](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) | "If your project targets .NET 5 or later, code analysis is enabled by default." and "The default value for the AnalysisLevel property is latest" and "Set the MSBuild property EnforceCodeStyleInBuild to true." | 2026-10-26 | 2027-10-26 |
| `cs-format-verify` | `dotnet format --verify-no-changes` exits non-zero when a file would change | [dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format) | "Terminates with a non zero exit code if any files would have been formatted." | 2026-10-26 | 2027-10-26 |
| `cs-async-void` | `async void` is for event handlers, and its exceptions can't be caught outside it; blocking on async code can deadlock | [Asynchronous programming scenarios](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios) | "Return 'async void' only from event handlers" and "Exceptions thrown in an async void method can't be caught outside of that method" and "Synchronous blocking on asynchronous operations can lead to deadlocks and should be avoided whenever possible." | 2026-10-26 | 2027-10-26 |
| `cs-configureawait` | `ConfigureAwait(false)` is for general-purpose library code; ASP.NET Core has no `SynchronizationContext` | [ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/) | "use ConfigureAwait(false) if you're writing general-purpose library / app-model-agnostic code, and otherwise don't." and "in contrast ASP.NET Core does not" | 2026-10-26 | 2027-10-26 |
| `cs-ca2007-apps` | CA2007 is meant for libraries, and is suppressed in application code | [CA2007](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2007) | "It is generally appropriate to suppress the warning entirely for projects that represent application code rather than library code" | 2026-10-26 | 2027-10-26 |
| `cs-await-using` | `await using` calls `DisposeAsync` | [Implement a DisposeAsync method](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-disposeasync) | "The public parameterless DisposeAsync() method is called implicitly in an await using statement" | 2026-10-26 | 2027-10-26 |
| `cs-httpclient-reuse` | Reuse `HttpClient`: long-lived with `PooledConnectionLifetime`, or short-lived from the factory | [HttpClient guidelines](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines) | "reuse HttpClient instances for as many HTTP requests as possible" and "use either long-lived clients and set PooledConnectionLifetime" | 2026-10-26 | 2027-10-26 |
| `cs-typed-client-singleton` | A typed client in a singleton is a known hazard | [IHttpClientFactory](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory) | "Using typed clients in singleton services can be dangerous." | 2026-10-26 | 2027-10-26 |
| `cs-stj-options` | Reuse one `JsonSerializerOptions` instance | [Configure options](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/configure-options) | "Reuse the same instance for every call." | 2026-10-26 | 2027-10-26 |
| `cs-stj-reflection` | Reflection-based System.Text.Json can break NativeAOT, and is off when `PublishTrimmed` is on | [Source generation](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation) | "Because System.Text.Json uses reflection by default, calling a basic serialization method can break Native AOT apps" and "If you don't specify this property and PublishTrimmed is enabled, reflection-based serialization is automatically disabled." | 2026-10-26 | 2027-04-26 |
| `cs-binaryformatter` | `BinaryFormatter` can't be made secure, and from .NET 9 throws on use, with its compatibility settings removed | [BinaryFormatter security guide](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide) | "BinaryFormatter is insecure and can't be made secure." and "Starting in .NET 9, the in-box BinaryFormatter implementation throws exceptions on use, even with the settings that previously enabled its use. Those settings are also removed." | 2026-10-26 | 2027-10-26 |
| `cs-typenamehandling` | CA2326 flags Newtonsoft.Json `TypeNameHandling` values other than `None` | [CA2326](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2326) | "This rule finds Newtonsoft.Json.TypeNameHandling values other than None." | 2026-10-26 | 2027-10-26 |
| `cs-sql-params` | CA2100 asks for parameterized SQL | [CA2100](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2100) | "Use a parameterized command string." | 2026-10-26 | 2027-10-26 |
| `cs-shellexecute` | `UseShellExecute` defaults to `false` on .NET, `true` on .NET Framework | [ProcessStartInfo.UseShellExecute](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.useshellexecute) | "The default is false (or true on .NET Framework apps)." | 2026-10-26 | 2027-10-26 |
| `cs-argumentlist` | `ArgumentList` escapes each argument | [ProcessStartInfo.ArgumentList](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.argumentlist) | "ArgumentList escapes the provided arguments" | 2026-10-26 | 2027-10-26 |
| `cs-path-combine` | `Path.Combine` restarts at a rooted argument, and isn't meant for user input | [Path.Combine](https://learn.microsoft.com/en-us/dotnet/api/system.io.path.combine) | "if an argument other than the first contains a rooted path, any previous path components are ignored" and "particularly if any subsequent arguments are strings input by the user, call the Join or TryJoin method instead" | 2026-10-26 | 2027-10-26 |
| `cs-aot-limits` | NativeAOT allows no dynamic loading and no runtime code generation | [Native AOT deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/) | "No dynamic loading, for example, Assembly.LoadFile. No runtime code generation, for example, System.Reflection.Emit." | 2026-10-26 | 2027-04-26 |
| `cs-trim-ui` | The SDK disables trimming for WPF and Windows Forms | [Trimming incompatibilities](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/incompatibilities) | "trimming support for WPF is currently disabled in the .NET SDK" and "trimming support for Windows Forms apps is disabled in the .NET SDK currently" | 2026-10-26 | 2027-04-26 |
| `cs-libraryimport` | `LibraryImport` has no `ExactSpelling`, and needs `AllowUnsafeBlocks` | [P/Invoke source generation](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke-source-generation) | "The method name or EntryPoint should be the exact spelling of the entry point name." and "The project must be marked unsafe using AllowUnsafeBlocks." | 2026-10-26 | 2027-10-26 |
| `cs-pinvoke-error` | Read the last error before making other calls, and use `SafeHandle` for unmanaged handles | [Native interop best practices](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/best-practices) | "get the error before making other calls to avoid inadvertently having it overwritten" and "use SafeHandle handles to manage lifetime of objects that encapsulate unmanaged resources" | 2026-10-26 | 2027-10-26 |
| `cs-getlastpinvokeerror` | `GetLastPInvokeError` is preferred over `GetLastWin32Error` | [Marshal.GetLastPInvokeError](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshal.getlastpinvokeerror) | "GetLastPInvokeError should be preferred over GetLastWin32Error." | 2026-10-26 | 2027-10-26 |
| `cs-commandline-api` | System.CommandLine's API changed after 2.0.0-beta4: `SetAction` replaced `SetHandler` | [System.CommandLine migration guide](https://learn.microsoft.com/en-us/dotnet/standard/commandline/migration-guide-2.0.0-beta5) | "This article describes the breaking changes that were made in 2.0.0-beta5 and 2.0.0-beta7" and "You can use the Command.SetAction method to set an action for a command." | 2026-10-26 | 2027-04-26 |

## Sources

Every rule here is in this module's own words. Each quote is short, and a dated fact above. No
code was copied.

| Source | Used for | License |
|---|---|---|
| [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | Release dates, support windows, the .NET 11 release candidate | Microsoft's terms of use: facts in our own words, with short quotes |
| [.NET documentation on Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/) (dotnet/docs and dotnet/dotnet-api-docs) | Language versions, nullable, warnings, analyzers, `dotnet format`, async, disposal, `HttpClient`, JSON, serialization security, process and path APIs, NativeAOT, trimming, P/Invoke | CC BY 4.0 for text, MIT for code: short quotes, with attribution |
| [MSBuild documentation](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory) (MicrosoftDocs/visualstudio-docs) | `Directory.Build.props` | CC BY 4.0 for text, MIT for code: a short quote, with attribution |
| [NuGet documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) (NuGet/docs.microsoft.com-nuget) | Central package management | MIT: a short quote |
| [ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/), .NET Blog | When to use `ConfigureAwait(false)`, and ASP.NET Core's context | Microsoft's terms of use: one short quote, for a fact |
