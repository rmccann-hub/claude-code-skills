# C# coding

Read this for C# on modern .NET: the target framework, nullable, build settings, analyzers,
async, disposal, `HttpClient`, JSON, NativeAOT, trimming and P/Invoke.

Data from outside (deserialization, SQL, processes, paths) is `csharp-security`. Windows
administration is windows-admin (planned), PowerShell `powershell-scripts`, tests the testing
skill (planned), and packages supply-chain-security. Each C# example compiled on 2026-10-26 with
the .NET 10.0.403 SDK, nullable on, `latest-Recommended` analysis and warnings as errors.

## Rules

1. **Target `net10.0`.** .NET 8 and 9 end together (fact `cs-dotnet8-9-end`), 10 is LTS (fact
   `cs-dotnet10-lts`), 11 a release candidate (fact `cs-dotnet11-rc`), and only a latest patch
   is supported (fact `cs-support-policy`). Leave `LangVersion` unset so the target picks C#
   (fact `cs-langversion-default`), never `latest` (fact `cs-langversion-latest`). Pin an SDK in
   `global.json` with `rollForward` (fact `cs-global-json`).
2. **Nullable on and warnings as errors, once, in `Directory.Build.props`,** which reaches every
   project below it (fact `cs-build-props`). It's case-sensitive on Linux.

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

Templates turn nullable on (fact `cs-nullable-template`), but warnings don't fail a build by
default; `<WarningsAsErrors>Nullable</WarningsAsErrors>` fails on nullability alone while code
catches up (fact `cs-warnaserror`). `!` silences a warning, checking nothing. Versions go in
`Directory.Packages.props`: `ManagePackageVersionsCentrally`, a `PackageVersion` each, and no
`Version` on `PackageReference` (fact `cs-cpm`).

3. **Analyzers and `dotnet format` in the build and CI.** Few rules warn by default:
   `AnalysisLevel` raises the set, `EnforceCodeStyleInBuild` runs `.editorconfig` style on build
   (fact `cs-analysis-default`), and `dotnet format --verify-no-changes` fails CI when a file
   would change (fact `cs-format-verify`). Security rules: `csharp-security`.
4. **Async all the way down.** `async void` is for event handlers, as its exceptions escape, and
   `.Result`, `.Wait()` and `.GetAwaiter().GetResult()` can deadlock (fact `cs-async-void`).
   Await, and pass the token on:

```csharp
// Wrong: blocks, and can deadlock under a UI synchronization context.
// string body = client.GetStringAsync(uri).Result;

// Right: awaits, and lets the caller cancel.
string body = await client.GetStringAsync(uri, cancellationToken);
```

`ConfigureAwait(false)` is for general-purpose libraries (facts `cs-configureawait`,
`cs-ca2007-apps`): in a WinForms or WPF handler, code after it may leave the UI thread.

5. **Dispose what you create, and reuse `HttpClient`.** `await using` calls `DisposeAsync` (fact
   `cs-await-using`): `await using FileStream stream = File.OpenRead(path);`. A client per
   request can exhaust ports; a long-lived one needs `PooledConnectionLifetime` for DNS changes
   (fact `cs-httpclient-reuse`). Or use `IHttpClientFactory`, but no typed client in a singleton
   (fact `cs-typed-client-singleton`).

```csharp
private static readonly HttpClient s_client = new(new SocketsHttpHandler
{
    PooledConnectionLifetime = TimeSpan.FromMinutes(2),
});
```

6. **System.Text.Json, with one `JsonSerializerOptions`** (fact `cs-stj-options`), and a
   source-generated context under NativeAOT or trimming, where reflection is off (fact
   `cs-stj-reflection`):

```csharp
[JsonSerializable(typeof(Order))]
internal sealed partial class AppJsonContext : JsonSerializerContext
{
}

Order? order = JsonSerializer.Deserialize(json, AppJsonContext.Default.Order);
```

7. **NativeAOT and trimming only where startup or size matter, warnings fixed.** AOT starts
   faster and uses less memory, but can't load or generate code at run time (fact
   `cs-aot-limits`). Set `PublishAot` in the project, so builds analyze it; a library sets
   `IsAotCompatible`. WinForms and WPF can't be trimmed (fact `cs-trim-ui`).
8. **P/Invoke through `LibraryImport`.** It generates the marshalling at compile time, needs
   `AllowUnsafeBlocks`, and has no `ExactSpelling`: name the exact export, `W` included (fact
   `cs-libraryimport`). Read `Marshal.GetLastPInvokeError()` before any other call, even
   logging (facts `cs-pinvoke-error`, `cs-getlastpinvokeerror`). Owned handles go in a
   `SafeHandle`.

```csharp
internal static partial class NativeMethods
{
    [LibraryImport("kernel32.dll", EntryPoint = "GetModuleHandleW", SetLastError = true,
        StringMarshalling = StringMarshalling.Utf16)]
    [DefaultDllImportSearchPaths(DllImportSearchPath.System32)]
    internal static partial nint GetModuleHandle(string? moduleName);
}

nint module = NativeMethods.GetModuleHandle("user32.dll");
if (module == 0)
{
    throw new Win32Exception(Marshal.GetLastPInvokeError());
}
```

## Mistakes

- **`net8.0` from old examples, or `net9.0` "for support":** both end together. Use `net10.0`.
- **`async void` on a helper, or `.Result` in a sync wrapper:** exceptions escape, or the thread
  deadlocks. Return `Task` and await.
- **`ConfigureAwait(false)` on every await in an app:** UI code may run on the wrong thread.
- **`new HttpClient()` per request, or `new JsonSerializerOptions` per call.** Share one.
- **No `W` on a `LibraryImport` name,** from `DllImport` advice: `DllImport` finds the `W` export
  without `ExactSpelling` under `CharSet.Unicode` (fact `cs-exactspelling`); `LibraryImport`
  fails at run time.
- **`PublishTrimmed` on WinForms or WPF, or `IL2` and `IL3` warnings suppressed:** unsupported,
  and hiding code that breaks once published.
- **System.CommandLine's `SetHandler` and `InvocationContext`,** from old samples: it now uses
  `SetAction` and `ParseResult` (fact `cs-commandline-api`).
- **A package an assistant named unchecked:** look it up on nuget.org.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Supported target | `TargetFramework(s)` in projects and `Directory.Build.props` | `GAP` below `net10.0` | `net10.0` |
| Language version | `LangVersion` of `latest` or `preview` | `DRIFT` | Remove it |
| Nullable on | `Nullable` is `enable` everywhere | `GAP` | Enable it |
| Warnings fail the build | `TreatWarningsAsErrors`, or `-warnaserror` in CI | `GAP` | Set it |
| One home for versions | `Version` on a `PackageReference` | `DRIFT` | `PackageVersion` |
| Format checked | `dotnet format --verify-no-changes` in CI | `GAP` | Add it |
| Async misuse | `async void` outside handlers; `.Result`, `.Wait()`, `GetResult()` | `GAP` | Return `Task`, await |
| `HttpClient` per call | `new HttpClient(` run per request | `GAP` | One shared, or the factory |
| AOT and trim warnings hidden | `NoWarn` with `IL2` or `IL3` codes | `DRIFT` | Fix or annotate |

## Why

### A supported target

**Why:** an unsupported runtime gets no security fixes. **Cost:** a move every two or three
years; STS 11 gains no time over 10. **Choose differently:** a library on older frameworks
multi-targets, such as `netstandard2.0`, testing each.

### Nullable and warnings as errors

**Why:** an ignored warning checks nothing, nullable warnings are the only null check, and
copied settings drift. **Others** use `-warnaserror` in CI only; it reaches every MSBuild task.
**Cost:** a new SDK's rules can break a build; a numeric `AnalysisLevel` picks the moment.
**Choose differently:** an old codebase turns nullable on a project, or a file, at a time.

### Async

**Why:** blocking under a synchronization context waits on a thread that is itself waiting. A
library can't know its context; an app usually does. **Cost:** async spreads up the stack.
**Choose differently:** ASP.NET Core has no synchronization context, so blocking deadlocks less
there, but it still holds a thread.

### Native code

**Why:** an AOT or trim warning marks code that may fail only once published; `LibraryImport`'s
marshalling is visible to both. **Cost:** no reflection-heavy libraries, and a publish per
platform. **Choose differently:** a long-running service gains little from AOT, and working
`DllImport` code can wait for it.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cs-dotnet10-lts` | .NET 10 is LTS, to 2028-11-14 | [Policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) | "LTS Active November 14, 2028" | 2026-10-26 | 2027-04-26 |
| `cs-dotnet8-9-end` | .NET 8 and 9 end 2026-11-10 | [Policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) | "STS Maintenance November 10, 2026" and "LTS Maintenance November 10, 2026" | 2026-10-26 | 2027-04-26 |
| `cs-dotnet11-rc` | .NET 11 is at RC2 | [Policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) | ".NET 11 RC2 October 13, 2026" | 2026-10-26 | 2027-04-26 |
| `cs-support-policy` | LTS: 3 years, STS: 2; odd is STS; latest patch only | [Policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) | "patches for three years" and "patches for two years" and "Odd numbered releases are STS" and "need the latest patch" | 2026-10-26 | 2027-04-26 |
| `cs-langversion-default` | .NET 10 means C# 14 | [Learn](https://learn.microsoft.com/dotnet/csharp/language-reference/language-versioning) | ".NET 10.x C# 14" | 2026-10-26 | 2027-04-26 |
| `cs-langversion-latest` | Not `latest` | [Learn](https://learn.microsoft.com/dotnet/csharp/language-reference/configure-language-version) | "Don't set the LangVersion element to latest" | 2026-10-26 | 2027-10-26 |
| `cs-global-json` | It has `rollForward` | [Learn](https://learn.microsoft.com/dotnet/core/tools/global-json) | "The roll-forward policy" | 2026-10-26 | 2027-10-26 |
| `cs-build-props` | It reaches every project | [Learn](https://learn.microsoft.com/visualstudio/msbuild/customize-by-directory) | "add a new property to every project" | 2026-10-26 | 2027-10-26 |
| `cs-nullable-template` | Templates turn it on | [Learn](https://learn.microsoft.com/dotnet/csharp/nullable-references) | "recent .NET templates set" | 2026-10-26 | 2027-10-26 |
| `cs-warnaserror` | Off by default; `Nullable`; the switch reaches all | [Learn](https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-options/errors-warnings) | "TreatWarningsAsErrors isn't in effect" and "Nullable shorthand" and "only impacts the C# compiler" and "switch impacts all tasks" | 2026-10-26 | 2027-10-26 |
| `cs-cpm` | Central versions | [Learn](https://learn.microsoft.com/nuget/consume-packages/central-package-management) | "ManagePackageVersionsCentrally to true" | 2026-10-26 | 2027-10-26 |
| `cs-format-verify` | It exits non-zero | [Learn](https://learn.microsoft.com/dotnet/core/tools/dotnet-format) | "non zero exit code if any files would have been formatted" | 2026-10-26 | 2027-10-26 |
| `cs-async-void` | Handlers only; blocking deadlocks | [Learn](https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/async-scenarios) | "only from event handlers" and "can't be caught outside" and "can lead to deadlocks" | 2026-10-26 | 2027-10-26 |
| `cs-configureawait` | Libraries; ASP.NET Core has no context | [.NET Blog](https://devblogs.microsoft.com/dotnet/configureawait-faq/) | "app-model-agnostic code" and "ASP.NET Core does not" | 2026-10-26 | 2027-10-26 |
| `cs-ca2007-apps` | Off in apps | [Learn](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca2007) | "projects that represent application code" | 2026-10-26 | 2027-10-26 |
| `cs-await-using` | It calls `DisposeAsync` | [Learn](https://learn.microsoft.com/dotnet/standard/garbage-collection/implementing-disposeasync) | "implicitly in an await using statement" | 2026-10-26 | 2027-10-26 |
| `cs-httpclient-reuse` | Reuse it | [Learn](https://learn.microsoft.com/dotnet/fundamentals/networking/http/httpclient-guidelines) | "reuse HttpClient instances" and "set PooledConnectionLifetime" | 2026-10-26 | 2027-10-26 |
| `cs-typed-client-singleton` | Not in a singleton | [Learn](https://learn.microsoft.com/dotnet/core/extensions/httpclient-factory) | "typed clients in singleton services can be dangerous" | 2026-10-26 | 2027-10-26 |
| `cs-stj-options` | One options instance | [Learn](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/configure-options) | "Reuse the same instance for every call." | 2026-10-26 | 2027-10-26 |
| `cs-stj-reflection` | Reflection breaks AOT; off if trimmed | [Learn](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/source-generation) | "can break Native AOT apps" and "reflection-based serialization is automatically disabled" | 2026-10-26 | 2027-04-26 |
| `cs-aot-limits` | AOT's limits | [Learn](https://learn.microsoft.com/dotnet/core/deploying/native-aot/) | "No dynamic loading" and "No runtime code generation" | 2026-10-26 | 2027-04-26 |
| `cs-trim-ui` | No WPF or WinForms trimming | [Learn](https://learn.microsoft.com/dotnet/core/deploying/trimming/incompatibilities) | "trimming support for WPF is currently disabled" and "Windows Forms apps is disabled" | 2026-10-26 | 2027-04-26 |
| `cs-libraryimport` | Exact name; unsafe blocks | [Learn](https://learn.microsoft.com/dotnet/standard/native-interop/pinvoke-source-generation) | "exact spelling of the entry point name" and "using AllowUnsafeBlocks" | 2026-10-26 | 2027-10-26 |
| `cs-exactspelling` | `DllImport` tries a `W` name | [Learn](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.dllimportattribute.exactspelling) | "appended with the letter W is invoked" | 2026-10-26 | 2027-10-26 |
| `cs-pinvoke-error` | Error first; `SafeHandle` | [Learn](https://learn.microsoft.com/dotnet/standard/native-interop/best-practices) | "get the error before making other calls" and "use SafeHandle handles" | 2026-10-26 | 2027-10-26 |
| `cs-getlastpinvokeerror` | Prefer it | [Learn](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.marshal.getlastpinvokeerror) | "GetLastPInvokeError should be preferred" | 2026-10-26 | 2027-10-26 |
| `cs-commandline-api` | It broke after beta4 | [Learn](https://learn.microsoft.com/dotnet/standard/commandline/migration-guide-2.0.0-beta5) | "made in 2.0.0-beta5" and "Command.SetAction method" | 2026-10-26 | 2027-04-26 |

## Sources

| Source | Used for | License |
|---|---|---|
| [.NET support policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) | Support | Microsoft's terms of use: short quotes |
| [Microsoft Learn](https://learn.microsoft.com/dotnet/): .NET, MSBuild, NuGet | The rest | CC BY 4.0 text, MIT code (NuGet: MIT): short quotes, attributed |
| [ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/) | `ConfigureAwait` | Microsoft's terms of use: a short quote |
