# PowerShell scripts

Read this for writing, reviewing or fixing PowerShell: choosing 7 or Windows PowerShell 5.1 and
writing for both, encoding, advanced functions, `-WhatIf`, errors and exit codes, strict mode,
prompts in jobs, modules, PSScriptAnalyzer and Pester.

Credentials, untrusted input, `Invoke-Expression`, execution policy and signing are
`powershell-security`'s; Windows Server administration, the planned `windows-admin` module's;
test design, the planned `testing` skill's. Pins, CI and layout are the
project-bootstrap-and-audit standard's.

## Rules

1. **Choose the edition, and declare it with `#Requires`.**
2. **Write advanced functions that output objects.**
3. **Support `-WhatIf` wherever state changes.**
4. **Make errors stop the script,** a native command's included.
5. **Never prompt in automation.**
6. **Lint with PSScriptAnalyzer and test with Pester 6** on each edition.

### Choosing 7 or 5.1

- **7.6, the LTS line, where you control the host** (fact `ps-lifecycle-76`). 7.4 and 7.5 end
  together (fact `ps-lifecycle-74-75`): skip 7.5.
- **5.1 where the host has only Windows,** which supports it (fact `ps-windows-ps`).
- **7 installs beside 5.1:** a task picks `pwsh.exe` or `powershell.exe` (fact
  `ps-side-by-side`).

### Writing for both

- **Declare the floor:** `#Requires -Version 5.1`, or `-PSEdition Core` and `-Version 7.6`
  (fact `ps-requires`), and `CompatiblePSEditions`. Branch on `$PSVersionTable.PSEdition` (fact
  `ps-editions`).
- **No 7-only operators:** `&&`, `||`, `??`, `??=` or `a ? b : c` (fact `ps-7-operators`).
- **Pass `-Encoding` on every write.** 7 writes UTF-8 without a byte-order mark; 5.1's
  `Out-File` and `>` write UTF-16LE, `Set-Content` ANSI, and `-Encoding UTF8` adds a BOM. Save a
  non-ASCII script as UTF-8 with a BOM, or 5.1 misreads it (fact `ps-encoding`).
- **`Get-CimInstance` and `Get-WinEvent`,** not `Get-WmiObject` and `Get-EventLog`, which 7
  lacks (fact `ps-removed-cmdlets`).
- **Turn on PSScriptAnalyzer's `UseCompatibleCommands` and `UseCompatibleSyntax`** (fact
  `ps-pssa-rules`).

```powershell
# Runs on 5.1 and 7: no ?? or &&, and an explicit encoding.
$name = if ($env:REPORT_NAME) { $env:REPORT_NAME } else { 'daily' }
$report = Get-CimInstance -ClassName Win32_OperatingSystem |
    Select-Object -Property Caption, Version, LastBootUpTime
$report | ConvertTo-Csv -NoTypeInformation |
    Set-Content -LiteralPath "$PSScriptRoot/$name.csv" -Encoding utf8
```

`utf8` writes no BOM in 7 and one in 5.1; name `utf8BOM` or `utf8NoBOM` where it matters.

### Functions and output

- **`[CmdletBinding()]`,** with typed, `Mandatory` and `Validate*` parameters.
- **A verb from `Get-Verb`;** another warns on import (fact `ps-unapproved-verb`).
- **Objects out,** not `Write-Host` text (fact `ps-write-host`); progress to `Write-Verbose`.
- **`@()` for a collection:** one result isn't an array (fact `ps-array-one`).

Run this with `-WhatIf` first:

```powershell
#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Path,

    [ValidateRange(1, 3650)]
    [int]$OlderThanDays = 30
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'

$cutoff = (Get-Date).AddDays(-$OlderThanDays)
$old = @(Get-ChildItem -LiteralPath $Path -File | Where-Object LastWriteTime -lt $cutoff)
foreach ($file in $old) {
    if ($PSCmdlet.ShouldProcess($file.FullName, 'Remove')) {
        Remove-Item -LiteralPath $file.FullName
    }
}
Write-Verbose "Checked $($old.Count) files older than $cutoff"
```

### Errors

- **`catch` sees only terminating errors;** most cmdlets' aren't, and `$ErrorActionPreference`
  is `Continue` (facts `ps-nonterminating`, `ps-preferences`). Add `-ErrorAction Stop`, or set
  the preference atop a script (fact `ps-erroraction-stop`).
- **Catch by type what you can handle;** rethrow the rest with `throw`. Never leave a `catch` empty.
- **`Set-StrictMode -Version 3.0`,** not `Latest`, which moves: unset variables fail (fact
  `ps-strict`).
- **Check `$LASTEXITCODE` after every native command:** it never reaches `catch`. From 7.4,
  `$PSNativeCommandUseErrorActionPreference` makes it an error; 5.1 lacks it (fact
  `ps-native-exit`).

```powershell
try {
    $settings = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json
}
catch [System.Management.Automation.ItemNotFoundException] {
    Write-Warning "No settings file at ${Path}; using the defaults."
    $settings = $null
}
```

### Changes and prompts

- **`SupportsShouldProcess` adds `-WhatIf` and `-Confirm`;** call `$PSCmdlet.ShouldProcess()`
  per change. `ConfirmImpact` stays `Medium` unless it can't be undone: `High` meets the default
  `$ConfirmPreference` and prompts every run (facts `ps-shouldprocess`, `ps-preferences`).
- **No `Read-Host` in a job:** take a mandatory parameter, and run tasks `-NonInteractive`,
  where a prompt fails instead of hanging (fact `ps-noninteractive`).

### Modules, linting and tests

- **A module's layout is the standard's *Project shapes*:** `Public/`, `Private/`, a file per
  exported function, each in `FunctionsToExport`.
- **PSScriptAnalyzer with a settings file, and Pester 6, in CI** (fact `ps-tool-versions`),
  pinned by *Language toolchains*. Pester 6 runs on 5.1 and 7.4+ (fact `ps-pester6`).

```powershell
Invoke-ScriptAnalyzer -Path ./Widget -Recurse -Settings ./PSScriptAnalyzerSettings.psd1
Invoke-Pester -Path ./tests -Output Detailed
```

## Mistakes

- **7.4 to 7.5 for support:** both end together (fact `ps-lifecycle-74-75`). Go to 7.6.
- **`try` around a cmdlet without `-ErrorAction Stop`:** `catch` never runs (fact
  `ps-nonterminating`). AI assistants write it, reading `try` as in C#.
- **`Get-WmiObject` or `Get-EventLog` in code for 7,** instead of `Get-CimInstance` and
  `Get-WinEvent` (fact `ps-removed-cmdlets`).
- **5.1's `>` or `Out-File` output fed to a UTF-8 reader:** it's UTF-16LE; pass `-Encoding` (fact
  `ps-encoding`).
- **No `$LASTEXITCODE` check,** so a failed step reports success (fact `ps-native-exit`). Know
  the codes: `robocopy`'s non-zero ones aren't all errors (fact `ps-preferences`).
- **Detecting "interactive" by hand** to decide on `Read-Host`, not a mandatory parameter (fact
  `ps-noninteractive`).
- **`.Count` on what may be one object,** without `@()` (fact `ps-array-one`).
- **`$a += $x` in a long loop before 7.5,** copying the array each time (fact
  `ps-plus-equals`). Assign the loop: `$a = foreach ($x in $xs) { $x }`.
- **Pinning Pester 5.7, fearing 6:** most v5 suites run on it (fact `ps-pester6`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| `catch` never runs | `try` around cmdlets without `Stop` | `DRIFT` | `-ErrorAction Stop` (fact `ps-erroraction-stop`) |
| Exit codes ignored | No `$LASTEXITCODE` check | `GAP` | Check, throw (fact `ps-native-exit`) |
| No `-WhatIf` | `UseShouldProcessForStateChangingFunctions`, `ShouldProcess` | `GAP` | Add (fact `ps-shouldprocess`) |
| Edition undeclared | No `#Requires`, `CompatiblePSEditions` | `GAP` | Add (facts `ps-requires`, `ps-editions`) |
| Code its edition can't run | `&&`, `??`, `Get-WmiObject`; compatibility rules | `DRIFT` | Rewrite, or raise `#Requires` |
| Unsupported version | 7.4 or 7.5 in CI, images, installs | `DRIFT` from 2026-11-10 | 7.6 (fact `ps-lifecycle-74-75`) |
| Strict mode | Unset, or `Latest` | `GAP` if unset, `DRIFT` if `Latest` | `3.0` (fact `ps-strict`) |
| Prompts in jobs | `Read-Host`, `Get-Credential` | `GAP` | Parameter, vault (fact `ps-noninteractive`) |
| No encoding | Writes without `-Encoding` on 5.1 | `GAP` | `-Encoding` (fact `ps-encoding`) |
| No lint or tests | Neither tool in CI | `GAP` | *Language toolchains* (fact `ps-tool-versions`) |

## Why

**1. The edition.** 7.4 and 7.5 end on 2026-11-10 (fact `ps-lifecycle-74-75`); 5.1 lives with
its Windows (fact `ps-windows-ps`), so many admin scripts stay on it. Without `#Requires`, a
7-only script under 5.1 stops halfway. The cost: 7 is a runtime to patch; 5.1 gets no new
features. Linux and macOS need 7.

**2 and 3. Functions and `-WhatIf`.** Validation stops bad input before work starts; callers
filter objects, not text (fact `ps-write-host`); `-WhatIf` shows a change unmade. The cost: more
lines, an `if` per change, which a one-liner skips.

**4. Errors that stop.** The defaults carry on after a failure (facts `ps-preferences`,
`ps-nonterminating`, `ps-native-exit`), so a script acts on a failed step. Some set `Stop` per
call, letting expected per-item errors pass. The cost: an expected failure needs its own `try`.
A report of every failure collects each error instead.

**5. No prompts.** A prompt in a scheduled task waits for nobody; `-NonInteractive` fails it at
once, naming the cause (fact `ps-noninteractive`). The cost: callers pass every value.

**6. Lint and tests.** PSScriptAnalyzer catches many mistakes above and 7-only code (fact
`ps-pssa-rules`); Pester 6 runs on both editions. The cost: a CI job per edition, on Windows
for 5.1.

## Facts

Checked 2026-10-26; each is named above.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `ps-lifecycle-76` | 7.6 is LTS to 2028-11-14 | [Lifecycle](https://learn.microsoft.com/powershell/scripting/install/powershell-support-lifecycle) | "PowerShell 7.6 (LTS) 18-Mar-2026 14-Nov-2028" | 2026-10-26 | 2027-04-26 |
| `ps-lifecycle-74-75` | 7.4 and 7.5 end 2026-11-10 | [Lifecycle](https://learn.microsoft.com/powershell/scripting/install/powershell-support-lifecycle) | "7.5 23-Jan-2025 10-Nov-2026" and "7.4 (LTS) 16-Nov-2023 10-Nov-2026" | 2026-10-26 | 2027-04-26 |
| `ps-windows-ps` | 5.1 follows Windows | [Lifecycle](https://learn.microsoft.com/powershell/scripting/install/powershell-support-lifecycle) | "subject to the Windows support lifecycle" | 2026-10-26 | 2027-10-26 |
| `ps-side-by-side` | 7 sits beside 5.1 | [Migrating](https://learn.microsoft.com/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7) | "coexist with Windows PowerShell 5.1" and "named powershell.exe" and "named pwsh.exe" | 2026-10-26 | 2027-10-26 |
| `ps-requires` | Floor, edition | [Requires](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_requires) | "minimum version of PowerShell" and "Core for PowerShell and Desktop for Windows PowerShell" | 2026-10-26 | 2027-10-26 |
| `ps-editions` | `PSEdition`, manifests | [Editions](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_powershell_editions) | "PSEdition property in PowerShell 5.1 and above" and "CompatiblePSEditions field of the module manifest" | 2026-10-26 | 2027-10-26 |
| `ps-7-operators` | New in 7.0 | [7.0](https://learn.microsoft.com/powershell/scripting/whats-new/what-s-new-in-powershell-70) | "Ternary operator: a ? b : c" and "Pipeline chain operators" and "Null conditional operators: ?? and ??=" | 2026-10-26 | 2027-10-26 |
| `ps-encoding` | Encodings | [Encoding](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_character_encoding) | "defaults to utf8NoBOM for all text output" and "Out-File and the redirection operators > and >> create UTF-16LE" and "active system locale's ANSI legacy code page" and "UTF8 Uses UTF-8 (with BOM)" and "save them as UTF-8 with BOM" and "Encodes in UTF-8 format (no BOM)" | 2026-10-26 | 2027-10-26 |
| `ps-removed-cmdlets` | Not in 7 | [Differences](https://learn.microsoft.com/powershell/scripting/whats-new/differences-from-windows-powershell) | "WMI v1 cmdlets were removed" and "Get-ControlPanelItem Get-EventLog" | 2026-10-26 | 2027-10-26 |
| `ps-unapproved-verb` | Import warns | [Import-Module](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/import-module) | "command names include unapproved verbs" | 2026-10-26 | 2027-10-26 |
| `ps-write-host` | Not output | [Write-Host](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/write-host) | "Write-Host is a wrapper for Write-Information" and "use Write-Output or implicit output" | 2026-10-26 | 2027-10-26 |
| `ps-array-one` | One isn't an array | [Arrays](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_arrays) | "you need to declare the variable as an array" | 2026-10-26 | 2027-10-26 |
| `ps-nonterminating` | Skips `catch` | [Errors](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_error_handling) | "Non-terminating errors do not trigger catch or trap by default" | 2026-10-26 | 2027-10-26 |
| `ps-erroraction-stop` | `Stop` terminates | [Parameters](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_commonparameters) | "escalates the non-terminating error to a terminating error" | 2026-10-26 | 2027-10-26 |
| `ps-preferences` | Defaults; `robocopy` | [Preferences](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_preference_variables) | "$ErrorActionPreference default value, Continue" and "$ConfirmPreference High" and "robocopy use non-zero exit codes" | 2026-10-26 | 2027-10-26 |
| `ps-strict` | `Latest` moves | [Set-StrictMode](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/set-strictmode) | "Latest for Version in scripts isn't deterministic" and "reference variables that aren't initialized fail" | 2026-10-26 | 2027-10-26 |
| `ps-shouldprocess` | `-WhatIf`; `Medium` | [CmdletBinding](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute) | "adds Confirm and WhatIf parameters" and "The default value of the argument is Medium" | 2026-10-26 | 2027-10-26 |
| `ps-tool-versions` | Current releases | [PSScriptAnalyzer](https://www.powershellgallery.com/packages/PSScriptAnalyzer); [Pester](https://www.powershellgallery.com/packages/Pester) | "1.25.0 (current version)" and "6.2.0 (current version)" | 2026-10-26 | 2027-04-26 |
| `ps-pester6` | Platforms; v5 suites | [Pester](https://pester.dev/docs/migrations/v5-to-v6) | "targets Windows PowerShell 5.1 and PowerShell 7.4+" and "Most v5 suites run on v6 without changes" | 2026-10-26 | 2027-04-26 |
| `ps-plus-equals` | Faster `+=` | [7.5](https://learn.microsoft.com/powershell/scripting/whats-new/what-s-new-in-powershell-75) | "improves the performance of the += operation" | 2026-10-26 | 2027-10-26 |

## Sources

Quotes are short, attributed and dated; no code was copied.

| Source | Used for | License |
|---|---|---|
| [Microsoft Learn](https://learn.microsoft.com/powershell/) | Lifecycle and behavior | Docs CC BY 4.0, code MIT: short quotes, attributed |
| [Pester docs](https://pester.dev/) | Pester 6 | MIT (pester/docs): short quotes, attributed |
| [PowerShell Gallery](https://www.powershellgallery.com/) | Current versions | Gallery terms: version numbers only |
