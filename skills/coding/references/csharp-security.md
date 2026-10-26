# C# security

Read this for C# that handles data from outside: deserializing it, building SQL with it, starting
processes or batch files with it, opening paths it names, loading native libraries, and the
analyzers that catch each.

The rest of C#, from the target framework to async code, `HttpClient`, System.Text.Json, NativeAOT
and P/Invoke, is `csharp-coding`. Package audits and lockfiles belong to the security skill's
supply-chain-security module, and test design to the planned testing skill. Each C# example
compiled on 2026-10-26 with the .NET 10.0.403 SDK, nullable on, `latest-Recommended` analysis and
warnings as errors, and again with the security rules on. CI has no C# checker, so it doesn't
compile them again.

## Rules

1. **No serializer that takes types from the data:** never `BinaryFormatter`, and Newtonsoft.Json
   `TypeNameHandling` only `None`, on data from outside. System.Text.Json into a declared type,
   as `csharp-coding` shows, is the default.
2. **SQL takes parameters,** never text built from input, interpolated strings included.
3. **Processes start without a shell,** each value one `ArgumentList` item, and no input reaches
   a batch file unchecked.
4. **Paths from input are resolved, then checked against their root.**
5. **Turn the security analyzers on,** as neither the default nor `latest-Recommended` does, and
   fix what they find, such as a P/Invoke with no DLL search path.

### Deserialization

- **No `BinaryFormatter`:** it can't be made secure, and from .NET 9 it throws on use, with the
  switches that re-enabled it removed. Avoid `SoapFormatter`, `NetDataContractSerializer`,
  `LosFormatter` and `ObjectStateFormatter` too (fact `cs-binaryformatter`).
- **Newtonsoft.Json's `TypeNameHandling`** lets the data choose the type to create, so keep it
  `None` (fact `cs-typenamehandling`).

### Database queries

- **A parameter for every value,** such as `@id` on SQL Server, added through
  `command.Parameters.Add` (fact `cs-sql-params`). `$"... WHERE Id = {id}"` is concatenation.

  ```csharp
  using DbCommand command = connection.CreateCommand();
  command.CommandText = "SELECT Name FROM Customers WHERE Id = @id";
  DbParameter id = command.CreateParameter();
  id.ParameterName = "@id";
  id.Value = customerId;
  command.Parameters.Add(id);
  ```

- **Entity Framework's `FromSqlRaw`** takes the same care: parameters, never built text.

### Processes and shells

- **`UseShellExecute` is `false` by default on .NET, but `true` on .NET Framework** (fact
  `cs-shellexecute`), so set it. Pass each value as one `ArgumentList` item, which escapes it
  (fact `cs-argumentlist`), never inside a `cmd.exe /c` or `sh -c` string.
- **A value starting with `-` can still be read as an option** by the program: put `--` before
  it where the program takes one.

  ```csharp
  ProcessStartInfo startInfo = new("git")
  {
      UseShellExecute = false,
      ArgumentList = { "log", "--", fileName },
  };
  using Process process = Process.Start(startInfo)
      ?? throw new InvalidOperationException("git didn't start.");
  await process.WaitForExitAsync(cancellationToken);
  ```

- **On Windows, a `.bat` or `.cmd` file runs through `cmd.exe`** whatever you pass (fact
  `py-subprocess-shell`), so input never goes to a batch file unchecked.

### Paths from input

- **`Path.Combine` drops everything before a rooted argument** (fact `cs-path-combine`), and
  neither it nor `Path.Join` stops `..`. Resolve the path, then check it against the root:

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

### Analyzers

- **CA2100 flags SQL text built from strings, and CA2326 `TypeNameHandling`,** but neither is on
  by default (facts `cs-sql-params`, `cs-typenamehandling`), and code analysis warns on few rules
  (fact `cs-analysis-default`). `latest-Recommended` leaves them off too (fact
  `cs-recommended-rules`). Turn the security category on alone (fact `cs-analysis-category`):

  ```xml
  <AnalysisLevelSecurity>latest-All</AnalysisLevelSecurity>
  ```

- **CA5392 asks each P/Invoke for `DefaultDllImportSearchPaths`,** since by default a library is
  also looked for in the current directory, where a planted DLL of the same name gets loaded
  (fact `cs-dll-search-path`). `csharp-coding`'s `LibraryImport` example sets `System32` for
  this reason.

## Mistakes

- **Re-enabling `BinaryFormatter` with a compatibility switch,** which .NET 9 removed (fact
  `cs-binaryformatter`). Move to a serializer that doesn't take types from the data.
- **SQL built with `$"... WHERE Name = '{name}'"`, or `Process.Start("cmd.exe", "/c " + input)`.**
  Input then rewrites the command. Use a parameter, or `ArgumentList` with no shell.
- **`Path.Combine(root, userInput)` as a guard.** An absolute input replaces the root, and `..`
  climbs out. Resolve and check.
- **Trusting `latest-Recommended` to catch SQL injection.** It leaves CA2100 off; set
  `AnalysisLevelSecurity`.
- **A P/Invoke with no search path.** The loader may then take a planted DLL from the current
  directory. Name the directories, such as `System32` for a Windows DLL.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Unsafe deserialization | `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer`; `TypeNameHandling` other than `None` | `BLOCKER` on data from outside | System.Text.Json (facts `cs-binaryformatter`, `cs-typenamehandling`) |
| SQL from strings | `CommandText` or `FromSqlRaw` built by concatenation or interpolation | `BLOCKER` where input reaches it | Parameters (fact `cs-sql-params`) |
| Shell commands | `UseShellExecute = true`, `cmd.exe /c` or `sh -c` with input; input to a `.bat` or `.cmd` file | `BLOCKER` where input reaches it | `ArgumentList`, no shell (fact `cs-argumentlist`) |
| Paths from input | `Path.Combine` or `Path.Join` with request data, no containment check | `BLOCKER` where input reaches it | Resolve and check against the root |
| Security analyzers | Neither `AnalysisLevel` nor `AnalysisLevelSecurity` at an `-All` level | `GAP` | Set `AnalysisLevelSecurity` (fact `cs-analysis-category`) |
| DLL search path | `DllImport` or `LibraryImport` with no `DefaultDllImportSearchPaths` on it or its assembly | `GAP` | Name the directories (fact `cs-dll-search-path`) |

## Why

### No types from the data

**The advice.** Deserialize outside data only with a serializer that builds the types the code
declares. **Why.** A serializer that lets the payload pick the type can be made to run code
(facts `cs-binaryformatter`, `cs-typenamehandling`). **What it costs.** Polymorphic data needs
its allowed types listed in code. **When to choose differently.** Not for data from outside; on
.NET 9 and later, `BinaryFormatter` throws even on your own data.

### Parameters, argument lists and contained paths

**The advice.** Keep input as data: a SQL parameter, one argument, a path checked against its
root. **Why.** Concatenated SQL or shell text lets input change the command, and `Path.Combine`
assumes trusted parts (fact `cs-path-combine`). **What it costs.** Little: the safe form is as
short as the unsafe one. `ArgumentList` gives up a shell's pipes and redirection, so do those in
C#. `GetFullPath` works on the text, so a symbolic link inside the root can still lead out of it.
**When to choose differently.** A shell only for fixed text that no input reaches.

### Security analyzers on

**The advice.** Set `AnalysisLevelSecurity` to `latest-All`. **Why.** A rule that's off catches
nothing, and these are off under the default and recommended settings. **What it costs.** CA2100
can't always tell a constant built at run time from input, so it raises false positives (fact
`cs-sql-params`); suppress each with a reason. **When to choose differently.** A project already
running a security scanner in CI that covers these rules can leave them off.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cs-binaryformatter` | `BinaryFormatter` can't be made secure, and from .NET 9 throws on use, its compatibility settings removed; `SoapFormatter`, `LosFormatter`, `NetDataContractSerializer` and `ObjectStateFormatter` are to be avoided too | [Learn](https://learn.microsoft.com/dotnet/standard/serialization/binaryformatter-security-guide) | "BinaryFormatter is insecure and can't be made secure." and "Starting in .NET 9, the in-box BinaryFormatter implementation throws exceptions on use" and "Those settings are also removed." and "Avoid the following serializers" | 2026-10-26 | 2027-10-26 |
| `cs-typenamehandling` | CA2326 flags `TypeNameHandling` other than `None`, and is off by default in .NET 10 | [Learn](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca2326) | "This rule finds Newtonsoft.Json.TypeNameHandling values other than None." and "Enabled by default in .NET 10 No" | 2026-10-26 | 2027-04-26 |
| `cs-sql-params` | CA2100 asks for parameterized SQL, is off by default in .NET 10, and can raise false positives | [Learn](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca2100) | "Use a parameterized command string." and "Enabled by default in .NET 10 No" and "this rule produces false positives" | 2026-10-26 | 2027-04-26 |
| `cs-analysis-default` | Code analysis is on for .NET 5 and later, with few rules as warnings; `AnalysisLevel` defaults to `latest`; `EnforceCodeStyleInBuild` runs style rules on build | [Learn](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview) | "If your project targets .NET 5 or later, code analysis is enabled by default." and "The default value for the AnalysisLevel property is latest" and "Set the MSBuild property EnforceCodeStyleInBuild to true." | 2026-10-26 | 2027-10-26 |
| `cs-recommended-rules` | The SDK's configuration files list each mode's rules; .NET 10.0.403's `Recommended` files leave CA2100 and CA2326 off | [Learn](https://learn.microsoft.com/dotnet/core/project-sdk/msbuild-props) | "More aggressive mode than Minimum mode, where more rules are enabled as build warnings. To see which rules this includes, inspect" | 2026-10-26 | 2027-04-26 |
| `cs-analysis-category` | `AnalysisLevel<Category>`, such as `AnalysisLevelSecurity`, sets one category's level, and `All` enables every rule as a warning | [Learn](https://learn.microsoft.com/dotnet/core/project-sdk/msbuild-props) | "it only applies to a specific category of code-analysis rules" and "if you want to enable all rules as build warnings, set the value to All" | 2026-10-26 | 2027-10-26 |
| `cs-dll-search-path` | CA5392 flags a P/Invoke without `DefaultDllImportSearchPaths`, as the default search includes the current directory; it is off by default in .NET 10 | [Learn](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca5392) | "including the current working directory for the library to load" and "Use DefaultDllImportSearchPathsAttribute to specify the DLL search path explicitly" and "Enabled by default in .NET 10 No" | 2026-10-26 | 2027-04-26 |
| `cs-shellexecute` | `UseShellExecute` defaults to `false` on .NET, `true` on .NET Framework | [Learn](https://learn.microsoft.com/dotnet/api/system.diagnostics.processstartinfo.useshellexecute) | "The default is false (or true on .NET Framework apps)." | 2026-10-26 | 2027-10-26 |
| `cs-argumentlist` | `ArgumentList` escapes each argument | [Learn](https://learn.microsoft.com/dotnet/api/system.diagnostics.processstartinfo.argumentlist) | "ArgumentList escapes the provided arguments" | 2026-10-26 | 2027-10-26 |
| `cs-path-combine` | `Path.Combine` restarts at a rooted argument, and isn't meant for user input | [Learn](https://learn.microsoft.com/dotnet/api/system.io.path.combine) | "if an argument other than the first contains a rooted path, any previous path components are ignored" and "particularly if any subsequent arguments are strings input by the user, call the Join or TryJoin method instead" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is in this module's own words. Each quote is short, and a dated fact above. No
code was copied.

| Source | Used for | License |
|---|---|---|
| [.NET documentation on Microsoft Learn](https://learn.microsoft.com/dotnet/) (dotnet/docs and dotnet/dotnet-api-docs) | Serialization security, analyzer rules and settings, process and path APIs | CC BY 4.0 for text, MIT for code: short quotes, with attribution |
| .NET 10.0.403 SDK, its analyzer configuration files | Which rules `latest-Recommended` turns on, checked by building a sample | MIT: no text taken |
