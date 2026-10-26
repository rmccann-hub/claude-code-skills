# PowerShell scripts

Read this for writing, reviewing or fixing a PowerShell script or module: choosing between
PowerShell 7 and Windows PowerShell 5.1 and writing for both, advanced functions, `-WhatIf`,
error handling, PSScriptAnalyzer, Pester, credentials and script security.

It doesn't cover Active Directory, Group Policy or other Windows Server administration, which the
planned `windows-admin` module takes, or how to design tests, which the planned `testing` skill
takes. Pinning versions, CI, a module's layout and where secrets are kept belong to
project-bootstrap-and-audit's standard: its *Language toolchains* table, *Project shapes*,
*Wiring*, and dimension 7. A shell script is `bash-coding`'s, and C# is `csharp-coding`'s.

## Contents

- [Rules](#rules)
- [Mistakes](#mistakes)
- [Audit](#audit)
- [Why](#why)
- [Facts](#facts)
- [Sources](#sources)

## Rules

1. **Choose the edition on purpose, and declare it** with `#Requires`. PowerShell 7.6 for new
   work on a host you control; Windows PowerShell 5.1 where the host has only what Windows ships.
2. **Write advanced functions:** `[CmdletBinding()]`, typed and validated parameters, an approved
   verb, and objects out, not formatted text.
3. **Anything that changes state supports `-WhatIf` and `-Confirm`,** through
   `SupportsShouldProcess` and `$PSCmdlet.ShouldProcess`.
4. **Make errors stop the script:** strict mode, `-ErrorAction Stop` where a `catch` is meant to
   run, and `$LASTEXITCODE` checked after every native command.
5. **Never prompt in automation.** Input arrives as parameters, and a scheduled run uses
   `-NonInteractive`, so a prompt fails instead of hanging.
6. **Credentials arrive as a `[pscredential]`,** from `Get-Credential` at a console or a vault in
   a job. Never a password in plain text.
7. **No `Invoke-Expression` on anything built from input,** and execution policy is a guard rail,
   not a security boundary.
8. **Lint with PSScriptAnalyzer and test with Pester 6,** on each edition the code supports.

### Choosing PowerShell 7 or Windows PowerShell 5.1

- **PowerShell 7.6 is the LTS line** (fact `ps-lifecycle-76`). 7.4 and 7.5 leave support on the
  same day (fact `ps-lifecycle-74-75`), so moving from 7.4 to 7.5 gains nothing: go to 7.6.
- **Windows PowerShell 5.1 is part of Windows,** supported for as long as that Windows is (fact
  `ps-windows-ps`). It's what a host has when nobody installs anything.
- **7 installs beside 5.1, not over it.** `pwsh.exe` starts 7 and `powershell.exe` starts 5.1
  (fact `ps-side-by-side`), so a scheduled task picks one by name. Which edition a Windows host
  gets is the standard's *Defaults, and when to leave them*.

### Writing for both editions

- **Declare the floor.** `#Requires -Version 5.1` for code that runs on both, and
  `#Requires -PSEdition Core` with `-Version 7.6` for code that needs 7 (fact `ps-requires`). A
  module's manifest lists its editions in `CompatiblePSEditions`, and code branches on
  `$PSVersionTable.PSEdition`, `Desktop` or `Core` (fact `ps-editions`).
- **Keep 7's operators out of shared code.** `&&` and `||` between pipelines, `??`, `??=` and the
  ternary `a ? b : c` arrived in 7.0 (fact `ps-7-operators`), so 5.1 doesn't have them. Write
  `if` and `else`.
- **Pass `-Encoding` every time you write a file.** 7 writes UTF-8 without a byte-order mark by
  default. In 5.1, `Out-File`, `>` and `>>` write UTF-16LE, `Set-Content` writes a new file in
  the system's ANSI code page, and `-Encoding UTF8` adds a BOM. A script with characters outside
  ASCII is saved as UTF-8 with a BOM, or 5.1 misreads it (fact `ps-encoding`).
- **Use the cmdlets both editions have.** The WMI v1 cmdlets, such as `Get-WmiObject`, and the
  classic event log cmdlets, such as `Get-EventLog`, aren't in 7 (fact `ps-removed-cmdlets`).
  `Get-CimInstance` and `Get-WinEvent` work in both.
- **Turn on PSScriptAnalyzer's `UseCompatibleCommands` and `UseCompatibleSyntax`,** which test a
  script against the editions you name and are off by default (fact `ps-pssa-rules`).

```powershell
# Runs on 5.1 and 7: no ?? or &&, and an explicit encoding.
$name = if ($env:REPORT_NAME) { $env:REPORT_NAME } else { 'daily' }
$report = Get-CimInstance -ClassName Win32_OperatingSystem |
    Select-Object -Property Caption, Version, LastBootUpTime
$report | ConvertTo-Csv -NoTypeInformation |
    Set-Content -LiteralPath "$PSScriptRoot/$name.csv" -Encoding utf8
```

In 7, `-Encoding utf8` writes no BOM, and in 5.1 it writes one (fact `ps-encoding`), so the two
files differ by those three bytes. Where a reader needs one or the other, name `utf8BOM` or
`utf8NoBOM` in 7, and test on both.

### Functions, parameters and output

- **`[CmdletBinding()]` on every script and function,** which gives it `-Verbose` and the other
  common parameters. Mark required parameters `[Parameter(Mandatory)]`, type each one, and check
  it with `ValidateSet`, `ValidateRange`, `ValidatePattern` or `ValidateScript`.
- **Name it Verb-Noun with a verb from `Get-Verb`.** A module exporting another verb warns on
  every import (fact `ps-unapproved-verb`).
- **Return objects.** `Write-Output`, or a bare value, sends data down the pipeline. `Write-Host`
  is for the screen (fact `ps-write-host`), and progress messages go to `Write-Verbose`.
- **Take paths from input with `-LiteralPath`,** so `[` and `*` in a name aren't wildcards (fact
  `ps-literalpath`).
- **Wrap a result in `@()` when you need a collection.** One result comes back as one object, not
  a one-item array (fact `ps-array-one`).

This script deletes nothing until it's run without `-WhatIf`:

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

Run it with `-WhatIf` first, `.\Remove-OldLog.ps1 -Path 'D:\Logs' -WhatIf`, and read the list.

### Errors

- **`catch` sees only terminating errors.** Most cmdlets report a failure as a non-terminating
  error, which never reaches `catch`, and `$ErrorActionPreference` defaults to `Continue` (facts
  `ps-nonterminating`, `ps-preferences`). `-ErrorAction Stop` makes the error terminating, so
  `catch` runs (fact `ps-erroraction-stop`). In a script, `$ErrorActionPreference = 'Stop'` at
  the top does that for every command after it.
- **Catch what you can handle,** by exception type, and rethrow the rest with a bare `throw`. An
  empty `catch` hides the failure.
- **`Set-StrictMode -Version 3.0`,** not `Latest`, whose meaning grows with each release. Strict
  mode turns an unset variable into an error instead of `$null` (fact `ps-strict`).
- **A native command reports failure only in `$LASTEXITCODE`,** never to `catch`. Check it after
  every call, as the `git` example under *Credentials and security* does. From 7.4,
  `$PSNativeCommandUseErrorActionPreference = $true` turns a non-zero exit into an error; 5.1
  has no such setting (fact `ps-native-exit`).

```powershell
try {
    $settings = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json
}
catch [System.Management.Automation.ItemNotFoundException] {
    Write-Warning "No settings file at ${Path}; using the defaults."
    $settings = $null
}
```

### Changing state, and prompting

- **`SupportsShouldProcess` adds `-WhatIf` and `-Confirm`** (fact `ps-shouldprocess`). Call
  `$PSCmdlet.ShouldProcess(target, action)` before each change, as above. Leave `ConfirmImpact`
  at its default, `Medium`, unless the change can't be undone: `High` meets the default
  `$ConfirmPreference`, so it prompts on every run (facts `ps-shouldprocess`, `ps-preferences`).
- **No `Read-Host` in code a job runs.** Make the input a mandatory parameter. Under
  `-NonInteractive`, a prompt fails with an error instead of hanging (fact `ps-noninteractive`),
  which is why the standard's *Project shapes* runs a scheduled task that way.

### Credentials and security

- **Take a `[pscredential]` parameter.** At a console the caller passes `(Get-Credential)`. In a
  job it comes from a vault through SecretManagement, which stores a `PSCredential` as it is.
  SecretManagement is finished and gets security fixes only, and Microsoft points to passwordless
  sign-in, such as Microsoft Entra ID, where a service accepts it (fact `ps-secretmanagement`).
- **Never a password in the script, a `[string]` parameter, or `ConvertTo-SecureString
  -AsPlainText` with a literal.** PSScriptAnalyzer flags all three (fact `ps-pssa-rules`). Where
  a secret is kept, and why never in a task's arguments, is the standard's dimension 7 and
  *Wiring*.
- **No `Invoke-Expression` on a string built from input.** It runs the string as code, and its
  own page warns against it (fact `ps-iex`). Call the command directly, or with `&` and an array
  of arguments.
- **Execution policy isn't a security boundary,** and outside Windows it's always `Unrestricted`
  (fact `ps-execpolicy`). Don't weaken it machine-wide to get one script running: sign the
  script, or review a downloaded one and run `Unblock-File` on it.
- **Sign scripts where policy requires it.** `AllSigned` and `RemoteSigned` refuse an unsigned
  script. What enforces on Windows is App Control for Business, which Microsoft services as a
  security feature; AppLocker isn't one (fact `ps-signing`).

```powershell
function Send-Report {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [pscredential]$Credential,
        [Parameter(Mandatory)] [uri]$Uri
    )
    Invoke-RestMethod -Uri $Uri -Method Post -Credential $Credential -Body @{ report = 'daily' }
}

# A job reads the credential from a registered vault:
Send-Report -Credential (Get-Secret -Name 'ReportService') -Uri 'https://example.com/reports'

# Instead of: Invoke-Expression "git clone $Url $Target"
$arguments = @('clone', '--quiet', '--', $Url, $Target)
& git @arguments
if ($LASTEXITCODE -ne 0) { throw "git clone failed with exit code $LASTEXITCODE" }
```

### Modules, linting and tests

- **Lay a module out as the standard's *Project shapes* says:** `Public/` and `Private/`, one
  exported function per file, and a manifest listing each export in `FunctionsToExport`.
- **Lint with PSScriptAnalyzer** (fact `ps-tool-versions`), from a settings file in the
  repository, in CI and pinned as the standard's *Language toolchains* sets out.
- **Run tests with Pester 6** (fact `ps-tool-versions`). It runs on 5.1 and on 7.4 and later,
  and most Pester 5 suites run on it unchanged (fact `ps-pester6`).

```powershell
Invoke-ScriptAnalyzer -Path ./Widget -Recurse -Settings ./PSScriptAnalyzerSettings.psd1
Invoke-Pester -Path ./tests -Output Detailed
```

## Mistakes

- **Moving from 7.4 to 7.5 to stay supported.** Both end on the same day (fact
  `ps-lifecycle-74-75`). Move to 7.6.
- **A `try` around a cmdlet without `-ErrorAction Stop`.** The `catch` never runs, and the script
  carries on (fact `ps-nonterminating`). AI assistants write this often, reading `try` as C# or
  Python has it.
- **`Get-WmiObject` or `Get-EventLog` in code for 7,** copied from older scripts (fact
  `ps-removed-cmdlets`). Use `Get-CimInstance` and `Get-WinEvent`.
- **A file from `>` or `Out-File` in 5.1, handed to a tool that expects UTF-8.** It's UTF-16LE
  (fact `ps-encoding`). Pass `-Encoding`.
- **No `$LASTEXITCODE` check after `git` or another program,** so the script reports success
  after a failed step (fact `ps-native-exit`). Know the program's codes: some, such as
  `robocopy`, use non-zero codes for results that aren't errors (fact `ps-preferences`).
- **Detecting "interactive" by hand,** by the host's name or the command line, to decide whether
  to call `Read-Host`. Make the parameter mandatory, and run jobs with `-NonInteractive` (fact
  `ps-noninteractive`).
- **A password as a `[string]` parameter, or `ConvertTo-SecureString 'CHANGEME' -AsPlainText
  -Force` in the file.** It reaches the repository and the logs. Take a `[pscredential]` (fact
  `ps-pssa-rules`).
- **"Fixing" a blocked script with `Set-ExecutionPolicy Unrestricted`,** or calling execution
  policy a security control (fact `ps-execpolicy`). Unblock or sign the one script.
- **Trusting `.Count` on a result that may be one object.** Wrap it in `@()` (fact
  `ps-array-one`).
- **`$results += $item` in a long loop on 5.1 or 7.4,** which copies the array each time; 7.5 made
  it faster (fact `ps-plus-equals`). Assign the loop's output instead:
  `$results = foreach ($item in $items) { ... }`.
- **Pinning Pester 5.7 to avoid 6 as "breaking".** Most v5 suites run on 6 unchanged (fact
  `ps-pester6`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A password in the code | `Invoke-ScriptAnalyzer -Recurse` for `AvoidUsingConvertToSecureStringWithPlainText`, `AvoidUsingPlainTextForPassword`, `AvoidUsingUsernameAndPasswordParams` | `BLOCKER` where the value is real, else `GAP` | Rotate a real one first, then take a `[pscredential]` (fact `ps-pssa-rules`) |
| Input reaches `Invoke-Expression` | `Select-String -Pattern 'Invoke-Expression\|\biex\b'`, and where each string comes from | `BLOCKER` where outside input reaches it, else `GAP` | `&` with an argument array (fact `ps-iex`) |
| A `catch` that never runs | `try` blocks whose cmdlets lack `-ErrorAction Stop`, in a script without `$ErrorActionPreference = 'Stop'` | `DRIFT` | Add either (fact `ps-erroraction-stop`) |
| Native exit codes ignored | Calls to programs with no `$LASTEXITCODE` check after them | `GAP` | Check and throw (fact `ps-native-exit`) |
| State changes without `-WhatIf` | PSScriptAnalyzer's `UseShouldProcessForStateChangingFunctions` and `ShouldProcess` | `GAP` | `SupportsShouldProcess` and `$PSCmdlet.ShouldProcess` (fact `ps-shouldprocess`) |
| Edition not declared | Scripts without `#Requires -Version`; a manifest without `CompatiblePSEditions` | `GAP` | Add them (facts `ps-requires`, `ps-editions`) |
| Code that can't run on an edition it claims | `&&`, `??`, `Get-WmiObject` or `Get-EventLog` in code that claims 5.1 or 7; `UseCompatibleCommands` and `UseCompatibleSyntax` turned on | `DRIFT` | Rewrite for both, or raise the `#Requires` (fact `ps-pssa-rules`) |
| An unsupported PowerShell pinned | 7.4 or 7.5 in CI, an image or install steps | `DRIFT` from 2026-11-10 | 7.6 (fact `ps-lifecycle-74-75`) |
| Strict mode unset or `Latest` | `Set-StrictMode` missing from scripts and loaders, or set to `Latest` | `GAP` if missing, `DRIFT` if `Latest` | `Set-StrictMode -Version 3.0` (fact `ps-strict`) |
| A prompt in a job | `Read-Host` or `Get-Credential` in code a scheduled task runs | `GAP` | A mandatory parameter, and a vault (fact `ps-noninteractive`) |
| Files written without an encoding | `Out-File`, `Set-Content` or `>` without `-Encoding` in code 5.1 runs | `GAP` | Pass `-Encoding` (fact `ps-encoding`) |
| No lint or tests | No PSScriptAnalyzer or Pester run in CI | `GAP` | The standard's *Language toolchains* (fact `ps-tool-versions`) |

## Why

### 1. Choosing and declaring the edition

- **The advice:** 7.6 for new work on a host you control, 5.1 where the host has only Windows,
  and `#Requires` saying which.
- **The reason:** 7.4 and 7.5 end on 2026-11-10 (fact `ps-lifecycle-74-75`), while 5.1 lives as
  long as its Windows (fact `ps-windows-ps`). Without `#Requires`, a 7-only script started by
  `powershell.exe` can run halfway, then stop at the first cmdlet 5.1 lacks.
- **What others do, and why:** many administration scripts stay on 5.1, because every Windows
  host has it with nothing to install or patch.
- **What it costs:** 7 is one more runtime to install and patch on each host. 5.1 gets no new
  language features, and code for both gives up 7's operators.
- **When to choose differently:** code that must also run on Linux or macOS needs 7.

### 2 and 3. Advanced functions, and `-WhatIf` before every change

- **The advice:** `[CmdletBinding()]`, typed and validated parameters, approved verbs, objects
  out, and `SupportsShouldProcess` on anything that creates, changes or deletes.
- **The reason:** validation rejects bad input before work starts, with an error naming the
  parameter. A caller can filter and export objects, not `Write-Host` text (fact
  `ps-write-host`). `-WhatIf` shows what a change would do without doing it.
- **What it costs:** more lines than a bare `param()`, and an `if` around each change. A console
  one-liner needs neither.

### 4. Errors that stop

- **The advice:** strict mode 3.0, `-ErrorAction Stop` or the preference set to `Stop`, and a
  check of `$LASTEXITCODE`.
- **The reason:** PowerShell's defaults keep going after a failure (facts `ps-preferences`,
  `ps-nonterminating`, `ps-native-exit`), so a script can delete, copy or report the wrong thing
  after the step that should have stopped it.
- **What others do, and why:** some set `-ErrorAction Stop` on each call instead of the
  preference, so a cmdlet whose per-item errors are expected keeps going.
- **What it costs:** an expected failure, such as a file that may not exist, needs its own `try`
  or `-ErrorAction SilentlyContinue`.
- **When to choose differently:** a report that lists every failure handles each item's error
  and collects it, rather than stopping.

### 5. No prompts in automation

- **The advice and the reason:** mandatory parameters, and `-NonInteractive` for jobs. A prompt
  in a scheduled task waits for nobody; with `-NonInteractive` it fails at once, with an error
  naming the cause (fact `ps-noninteractive`). The cost: the caller supplies every value.

### 6. Credentials

- **The advice:** a `[pscredential]` parameter, filled by `Get-Credential` or a vault.
- **The reason:** a password in a script reaches the repository, every copy, and every log that
  echoes the command line.
- **What others do, and why:** where the service accepts it, a managed identity or another
  passwordless sign-in removes the secret, the direction Microsoft now gives (fact
  `ps-secretmanagement`).
- **What it costs:** a vault to set up on each host that runs the job.

### 7. `Invoke-Expression` and execution policy

- **The advice:** no `Invoke-Expression` on input; execution policy as a guard rail.
- **The reason:** `Invoke-Expression` runs a string as code, so input holding `;` or `$()` runs
  commands. Any user can get around execution policy (fact `ps-execpolicy`); App Control for
  Business is what Microsoft treats as a boundary (fact `ps-signing`).
- **What it costs:** signing needs a certificate and a step in the release.
- **When to choose differently:** where an organization enforces App Control, follow its signing
  policy.

### 8. Linting and tests

- **The advice:** both, in CI, on each edition the code supports.
- **The reason:** PSScriptAnalyzer finds many of the mistakes above before review, and its
  compatibility rules catch 7-only code in a 5.1 script (fact `ps-pssa-rules`). Pester runs
  tests written in PowerShell, and version 6 runs on both editions (fact `ps-pester6`).
- **What it costs:** a CI job per edition, and a Windows runner for 5.1.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `ps-lifecycle-76` | PowerShell 7.6 is LTS, released 2026-03-18, supported until 2028-11-14 | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6) | "PowerShell 7.6 (LTS) 18-Mar-2026 14-Nov-2028" | 2026-10-26 | 2027-04-26 |
| `ps-lifecycle-74-75` | PowerShell 7.4 and 7.5 both end support on 2026-11-10 | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6) | "PowerShell 7.5 23-Jan-2025 10-Nov-2026" and "PowerShell 7.4 (LTS) 16-Nov-2023 10-Nov-2026" | 2026-10-26 | 2027-04-26 |
| `ps-windows-ps` | Windows PowerShell follows the support lifecycle of its Windows | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6) | "Windows PowerShell is a component of the Windows operating system and is subject to the Windows support lifecycle." | 2026-10-26 | 2027-10-26 |
| `ps-side-by-side` | PowerShell 7 installs beside 5.1; 5.1 runs as `powershell.exe`, 6 and later as `pwsh.exe` | [Migrating from Windows PowerShell 5.1](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.6) | "PowerShell 7 is designed to coexist with Windows PowerShell 5.1." and "In Windows PowerShell, the PowerShell executable is named powershell.exe. In version 6 and above, the executable is named pwsh.exe." | 2026-10-26 | 2027-10-26 |
| `ps-requires` | `#Requires` sets a minimum version, and `-PSEdition` takes `Core` or `Desktop` | [about_Requires](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_requires?view=powershell-7.6) | "Specifies the minimum version of PowerShell that the script requires." and "Valid values are Core for PowerShell and Desktop for Windows PowerShell." | 2026-10-26 | 2027-10-26 |
| `ps-editions` | `$PSVersionTable.PSEdition` exists from 5.1, and a manifest declares editions in `CompatiblePSEditions` | [about_PowerShell_Editions](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_editions?view=powershell-7.6) | "The $PSVersionTable automatic variable also has PSEdition property in PowerShell 5.1 and above" and "PowerShell modules can declare what editions of PowerShell they are compatible with using the CompatiblePSEditions field of the module manifest." | 2026-10-26 | 2027-10-26 |
| `ps-7-operators` | `&&` and `\|\|` between pipelines, `??`, `??=` and the ternary operator arrived in PowerShell 7 | [about_Pipeline_Chain_Operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipeline_chain_operators?view=powershell-7.6); [What's new in PowerShell 7.0](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-70?view=powershell-7.6) | "Beginning in PowerShell 7, PowerShell implements the && and ... operators to conditionally chain pipelines." and "Null conditional operators: ?? and ??=" | 2026-10-26 | 2027-10-26 |
| `ps-encoding` | 7 writes UTF-8 without a BOM; 5.1's `Out-File` and `>` write UTF-16LE, `Set-Content` the ANSI code page, `-Encoding UTF8` with a BOM; a 5.1 script with non-ASCII text needs a BOM | [about_Character_Encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.6) | "PowerShell (v6 and higher) defaults to utf8NoBOM for all text output." and "Out-File and the redirection operators > and >> create UTF-16LE, which notably differs from Set-Content and Add-Content." and "Default is the encoding specified by the active system locale's ANSI legacy code page." and "UTF8 Uses UTF-8 (with BOM)." and "If you need to use non-Ascii characters in your scripts, save them as UTF-8 with BOM." and "Encodes in UTF-8 format (no BOM)." | 2026-10-26 | 2027-10-26 |
| `ps-removed-cmdlets` | The WMI v1 cmdlets and `Get-EventLog` aren't in PowerShell 7 | [Differences from Windows PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.6) | "The following WMI v1 cmdlets were removed from PowerShell: Register-WmiEvent Set-WmiInstance Invoke-WmiMethod Get-WmiObject Remove-WmiObject" and "Get-ControlPanelItem Get-EventLog Get-Transaction Get-WmiObject" | 2026-10-26 | 2027-10-26 |
| `ps-unapproved-verb` | Importing a module with unapproved verbs warns | [Import-Module](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/import-module?view=powershell-7.6) | "WARNING: Some imported command names include unapproved verbs which might make them less discoverable." | 2026-10-26 | 2027-10-26 |
| `ps-write-host` | `Write-Host` writes to the information stream; data goes out with `Write-Output` | [Write-Host](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-host?view=powershell-7.6) | "Starting in Windows PowerShell 5.0, Write-Host is a wrapper for Write-Information." and "to output data to the pipeline, use Write-Output or implicit output." | 2026-10-26 | 2027-10-26 |
| `ps-literalpath` | `-LiteralPath` reads no wildcards | [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6) | "The value of LiteralPath is used exactly as it's typed. No characters are interpreted as wildcards." | 2026-10-26 | 2027-10-26 |
| `ps-array-one` | One result is a single object; declare an array to get one | [about_Arrays](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays?view=powershell-7.6) | "If you want $result to be an array of strings, you need to declare the variable as an array." | 2026-10-26 | 2027-10-26 |
| `ps-nonterminating` | Non-terminating errors don't reach `catch` | [about_Error_Handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling?view=powershell-7.6) | "Non-terminating errors do not trigger catch or trap by default." | 2026-10-26 | 2027-10-26 |
| `ps-native-exit` | A native command's non-zero exit sets `$LASTEXITCODE` and doesn't reach `catch`; the preference that changes this is stable from 7.4 | [about_Error_Handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling?view=powershell-7.6) | "They report failure through a non-zero exit code, which PowerShell stores in the $LASTEXITCODE automatic variable." and "Does not trigger catch or trap" and "PowerShell 7.3 added the experimental preference variable $PSNativeCommandUseErrorActionPreference, which became a stable feature in 7.4." | 2026-10-26 | 2027-10-26 |
| `ps-erroraction-stop` | `-ErrorAction Stop` makes an error terminating, so `catch` runs | [about_CommonParameters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters?view=powershell-7.6) | "The Stop value escalates the non-terminating error to a terminating error by generating an ActionPreferenceStopException. The error can then be caught by a try/catch block or trap statement." | 2026-10-26 | 2027-10-26 |
| `ps-preferences` | `$ErrorActionPreference` defaults to `Continue` and `$ConfirmPreference` to `High`; some programs use non-zero exit codes for results that aren't errors | [about_Preference_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-7.6) | "This example shows the $ErrorActionPreference default value, Continue." and "$ConfirmPreference High" and "Some native commands, like robocopy use non-zero exit codes to represent information other than errors." | 2026-10-26 | 2027-10-26 |
| `ps-strict` | `Set-StrictMode -Version Latest` isn't deterministic; strict mode makes an unset variable an error | [Set-StrictMode](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-strictmode?view=powershell-7.6) | "Using Latest for Version in scripts isn't deterministic." and "With strict mode set to version 1.0, attempts to reference variables that aren't initialized fail." | 2026-10-26 | 2027-10-26 |
| `ps-shouldprocess` | `SupportsShouldProcess` adds `-Confirm` and `-WhatIf`; `ConfirmImpact` defaults to `Medium` | [about_Functions_CmdletBindingAttribute](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute?view=powershell-7.6) | "The SupportsShouldProcess argument adds Confirm and WhatIf parameters to the function." and "(The default value of the argument is Medium.)" | 2026-10-26 | 2027-10-26 |
| `ps-noninteractive` | Under `-NonInteractive`, a prompt is an error, not a hang | [about_Pwsh](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.6) | "Any attempts to use interactive features, like Read-Host or confirmation prompts, result in statement terminating errors rather than hanging." | 2026-10-26 | 2027-10-26 |
| `ps-secretmanagement` | SecretManagement stores a `PSCredential`; it and SecretStore are feature complete and get security fixes only; Microsoft points to passwordless sign-in | [SecretManagement README](https://raw.githubusercontent.com/PowerShell/SecretManagement/master/README.md); [SecretManagement overview](https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/overview?view=ps-modules) | "PowerShell SecretManagement supports the following secret data types:" and "PSCredential" and "The PowerShell team has decided that Secret modules are feature complete and will no longer be actively developed." and "The modules will continue to be supported for security and critical bug fixes." and "Passwordless authentication methods such as passkeys, single sign-on, and federated credential systems such as Microsoft Entra ID, biometrics, and hardware security keys are the future." | 2026-10-26 | 2027-10-26 |
| `ps-pssa-rules` | PSScriptAnalyzer flags plain-text passwords, `Invoke-Expression`, WMI v1 cmdlets and missing `ShouldProcess`, asks for `PSCredential`, and has compatibility rules that are off by default | [PSScriptAnalyzer rules](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/readme?view=ps-modules) | "AvoidUsingConvertToSecureStringWithPlainText Error Always enabled" and "AvoidUsingPlainTextForPassword Warning Always enabled" and "AvoidUsingUsernameAndPasswordParams Error Always enabled" and "AvoidUsingInvokeExpression Warning Always enabled" and "AvoidUsingWMICmdlet Warning Always enabled" and "UsePSCredentialType Warning Always enabled" and "UseShouldProcessForStateChangingFunctions Warning Always enabled" and "ShouldProcess Warning Always enabled" and "UseCompatibleCommands Warning Disabled Yes" and "UseCompatibleSyntax Error Disabled Yes" | 2026-10-26 | 2027-04-26 |
| `ps-iex` | Microsoft's page for `Invoke-Expression` cautions against it | [Invoke-Expression](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression?view=powershell-7.6) | "Take reasonable precautions when using the Invoke-Expression cmdlet in scripts." | 2026-10-26 | 2027-10-26 |
| `ps-execpolicy` | Execution policy isn't a security boundary, and outside Windows it's always `Unrestricted` | [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6) | "The execution policy isn't a security boundary, it's defense in depth." and "On non-Windows computers, the default execution policy is Unrestricted and can't be changed." | 2026-10-26 | 2027-10-26 |
| `ps-signing` | `AllSigned` and `RemoteSigned` refuse unsigned scripts; App Control for Business is serviced as a security feature, and AppLocker isn't | [about_Signing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_signing?view=powershell-7.6); [PowerShell security features](https://learn.microsoft.com/en-us/powershell/scripting/security/security-features?view=powershell-7.6) | "The AllSigned and RemoteSigned execution policies prevent PowerShell from running scripts that don't have a digital signature." and "App Control for Business is designed as a security feature under the servicing criteria defined by the Microsoft Security Response Center (MSRC)." and "AppLocker isn't a security feature under the servicing criteria defined by MSRC." | 2026-10-26 | 2027-10-26 |
| `ps-tool-versions` | PSScriptAnalyzer 1.25.0 and Pester 6.2.0 are current | [PowerShell Gallery: PSScriptAnalyzer](https://www.powershellgallery.com/packages/PSScriptAnalyzer); [PowerShell Gallery: Pester](https://www.powershellgallery.com/packages/Pester) | "1.25.0 (current version)" and "6.2.0 (current version)" | 2026-10-26 | 2027-04-26 |
| `ps-pester6` | Pester 6 runs on 5.1 and 7.4 and later, and most Pester 5 suites run on it unchanged | [Migrating from Pester v5 to v6](https://pester.dev/docs/migrations/v5-to-v6) | "Pester 6 targets Windows PowerShell 5.1 and PowerShell 7.4+." and "Most v5 suites run on v6 without changes." | 2026-10-26 | 2027-04-26 |
| `ps-plus-equals` | PowerShell 7.5 made `+=` on arrays faster | [What's new in PowerShell 7.5](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-75?view=powershell-7.6) | "improves the performance of the += operation for an array of objects" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is in this module's own words. Sources are quoted briefly, with attribution, and
each quote is a dated fact above. No code was copied from them.

| Source | Used for | License |
|---|---|---|
| [PowerShell documentation on Microsoft Learn](https://learn.microsoft.com/en-us/powershell/) (PowerShell-Docs) | Lifecycle, editions, operators, encoding, errors, strict mode, `ShouldProcess`, `-NonInteractive`, execution policy, signing, security features | Docs CC BY 4.0, code MIT: short quotes, with attribution |
| [PSScriptAnalyzer and SecretManagement documentation](https://learn.microsoft.com/en-us/powershell/utility-modules/) | Analyzer rules and their defaults; SecretManagement's status | CC BY 4.0, as PowerShell-Docs: short quotes, with attribution |
| [PowerShell/SecretManagement README](https://github.com/PowerShell/SecretManagement) | The secret types it stores | MIT: a fact with a short quote |
| [Pester documentation](https://pester.dev/docs/migrations/v5-to-v6) | Pester 6's platforms and compatibility | MIT, per the pester/docs repository: short quotes, with attribution |
| [PowerShell Gallery](https://www.powershellgallery.com/) | Current versions of PSScriptAnalyzer and Pester | Gallery terms: version numbers only |
