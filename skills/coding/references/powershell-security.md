# PowerShell security

Read this for handling credentials and untrusted input in PowerShell: `[pscredential]`
parameters and SecretManagement, plain-text passwords, `Invoke-Expression`, argument arrays and
batch files, paths from input, execution policy, and signing with App Control for Business.

Editions, functions, `-WhatIf`, errors and exit codes, prompts in jobs, PSScriptAnalyzer and
Pester are `powershell-scripts`'s. Where a secret is kept, and why never in a task's arguments,
is the project-bootstrap-and-audit standard's dimension 7 and *Wiring*. Windows Server
administration is the planned `windows-admin` module's.

## Rules

1. **Credentials arrive as a `[pscredential]`,** from `Get-Credential` at a console or a vault in
   a job.
2. **Never a password in plain text:** not in the script, a `[string]` parameter, or
   `ConvertTo-SecureString -AsPlainText` with a literal.
3. **No `Invoke-Expression` on anything built from input.** Call the command with `&` and an
   array of arguments.
4. **Don't hand input to a batch file:** an argument array doesn't protect it.
5. **Take a path from input with `-LiteralPath`.**
6. **Execution policy is a guard rail, not a security boundary.** Sign scripts where policy
   requires it.

### Credentials

- **Take a `[pscredential]` parameter.** At a console the caller passes `(Get-Credential)`. A
  job can't answer a prompt (fact `ps-noninteractive`), so it reads the credential from a vault
  through SecretManagement, which stores a `PSCredential` as it is.
- **SecretManagement is finished,** and gets security fixes only. Microsoft points to
  passwordless sign-in, such as Microsoft Entra ID, where a service accepts it (fact
  `ps-secretmanagement`).
- **Never a password in the script, a `[string]` parameter, or `ConvertTo-SecureString
  -AsPlainText` with a literal.** PSScriptAnalyzer flags all three (fact `ps-pssa-rules`).

### Input, commands and paths

- **No `Invoke-Expression` on a string built from input.** It runs the string as code, and its
  own page warns against it (fact `ps-iex`). Call the command directly, or with `&` and an array
  of arguments, with `--` before input where the program takes it, then check `$LASTEXITCODE`
  (fact `ps-native-exit`).
- **An argument array doesn't protect a batch file.** On Windows, a `.bat` or `.cmd` target, and
  `cmd.exe` itself, always get legacy argument passing: the arguments reach `cmd.exe` as a raw
  command line. 5.1 passes every native command's arguments the legacy way (fact
  `ps-legacy-args`). Don't hand input to a batch file; where you must, allow only the characters
  you expect first.
- **`-LiteralPath` for a path from input,** so `[` and `*` in a name aren't wildcards (fact
  `ps-literalpath`). Under `-Path`, a name holding `*` matches every file it fits.

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

### Execution policy and signing

- **Execution policy isn't a security boundary:** any user can bypass it, and outside Windows
  it's always `Unrestricted` (fact `ps-execpolicy`). Don't weaken it machine-wide to get one
  script running: sign the script, or review a downloaded one and run `Unblock-File` on it.
- **Sign scripts where policy requires it.** `AllSigned` and `RemoteSigned` refuse an unsigned
  script. What enforces on Windows is App Control for Business, which Microsoft services as a
  security feature; AppLocker isn't one (fact `ps-signing`).

## Mistakes

- **A password as a `[string]` parameter, or `ConvertTo-SecureString 'CHANGEME' -AsPlainText
  -Force` in the file.** It reaches the repository and the logs. Take a `[pscredential]` (fact
  `ps-pssa-rules`).
- **Building a command line as a string for `Invoke-Expression`** to get the quoting right.
  Input holding `;` or `$()` then runs as code. Pass an argument array (fact `ps-iex`).
- **Trusting an argument array to quote input for a `.cmd` wrapper.** `cmd.exe` parses it again
  (fact `ps-legacy-args`). Call the program the wrapper calls, directly.
- **`Remove-Item -Path` on a name from input,** where `*` or `[` matches other files. Use
  `-LiteralPath` (fact `ps-literalpath`).
- **"Fixing" a blocked script with `Set-ExecutionPolicy Unrestricted`,** or calling execution
  policy a security control (fact `ps-execpolicy`). Unblock or sign the one script.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A password in the code | `Invoke-ScriptAnalyzer -Recurse` for `AvoidUsingConvertToSecureStringWithPlainText`, `AvoidUsingPlainTextForPassword`, `AvoidUsingUsernameAndPasswordParams` | `BLOCKER` where the value is real, else `GAP` | Rotate a real one first, then take a `[pscredential]` (fact `ps-pssa-rules`) |
| Input reaches `Invoke-Expression` | `Select-String -Pattern 'Invoke-Expression\|\biex\b'`, and where each string comes from | `BLOCKER` where outside input reaches it, else `GAP` | `&` with an argument array (fact `ps-iex`) |
| Input reaches a batch file | Calls to `.bat`, `.cmd` or `cmd.exe` with values from input | `BLOCKER` where outside input reaches it, else `GAP` | Call the program directly, or allow only expected characters (fact `ps-legacy-args`) |
| Wildcards in paths from input | `-Path` given a value from input | `GAP` | `-LiteralPath` (fact `ps-literalpath`) |
| Execution policy weakened | `Set-ExecutionPolicy Unrestricted` or `Bypass` for the machine, in install steps or docs | `DRIFT` | Sign or unblock the one script (fact `ps-execpolicy`) |

## Why

### 1 and 2. Credentials

- **The advice:** a `[pscredential]` parameter, filled by `Get-Credential` or a vault.
- **The reason:** a password in a script reaches the repository, every copy, and every log that
  echoes the command line.
- **What others do, and why:** where the service accepts it, a managed identity or another
  passwordless sign-in removes the secret, the direction Microsoft now gives (fact
  `ps-secretmanagement`).
- **What it costs:** a vault to set up on each host that runs the job.
- **When to choose differently:** a person at a console can type the credential at the
  `Get-Credential` prompt, with no vault.

### 3 to 5. Input, commands and paths

- **The advice:** no `Invoke-Expression` on input, an argument array instead, no input to a
  batch file, and `-LiteralPath`.
- **The reason:** `Invoke-Expression` runs a string as code, so input holding `;` or `$()` runs
  commands (fact `ps-iex`). A batch file gets its arguments as one raw line that `cmd.exe` reads
  again (fact `ps-legacy-args`). A wildcard in a name widens a delete (fact `ps-literalpath`).
- **What it costs:** an array takes more lines than a string, and a batch file that must take
  input needs an allow-list or a rewrite.
- **When to choose differently:** a fixed string you wrote, with nothing from input, carries no
  injection risk, but calling the command directly is still clearer.

### 6. Execution policy and signing

- **The advice:** execution policy as a guard rail, and signing where policy requires it.
- **The reason:** any user can get around execution policy (fact `ps-execpolicy`); App Control
  for Business is what Microsoft treats as a boundary (fact `ps-signing`).
- **What it costs:** signing needs a certificate and a step in the release.
- **When to choose differently:** where an organization enforces App Control, follow its signing
  policy.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `ps-noninteractive` | Under `-NonInteractive`, a prompt is an error, not a hang | [about_Pwsh](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh) | "like Read-Host or confirmation prompts, result in statement terminating errors rather than hanging" | 2026-10-26 | 2027-10-26 |
| `ps-secretmanagement` | SecretManagement stores a `PSCredential`; it's feature complete, with security fixes only; Microsoft points to passwordless sign-in | [SecretManagement README](https://raw.githubusercontent.com/PowerShell/SecretManagement/master/README.md); [SecretManagement overview](https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/overview) | "supports the following secret data types" and "PSCredential" and "Secret modules are feature complete" and "supported for security and critical bug fixes" and "Passwordless authentication methods such as passkeys" and "Microsoft Entra ID, biometrics, and hardware security keys are the future" | 2026-10-26 | 2027-10-26 |
| `ps-pssa-rules` | PSScriptAnalyzer flags plain-text passwords and `Invoke-Expression`; its compatibility rules are off by default | [PSScriptAnalyzer rules](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/readme) | "AvoidUsingConvertToSecureStringWithPlainText Error" and "AvoidUsingPlainTextForPassword Warning" and "AvoidUsingUsernameAndPasswordParams Error" and "AvoidUsingInvokeExpression Warning" and "UseCompatibleCommands Warning Disabled" and "UseCompatibleSyntax Error Disabled" | 2026-10-26 | 2027-04-26 |
| `ps-iex` | Microsoft's page for `Invoke-Expression` cautions against it | [Invoke-Expression](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression) | "Take reasonable precautions when using the Invoke-Expression cmdlet" | 2026-10-26 | 2027-10-26 |
| `ps-native-exit` | A native command's exit code is in `$LASTEXITCODE` and doesn't reach `catch`; the preference that changes this is stable from 7.4 | [about_Error_Handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling) | "stores in the $LASTEXITCODE automatic variable" and "Does not trigger catch or trap" and "became a stable feature in 7.4" | 2026-10-26 | 2027-10-26 |
| `ps-legacy-args` | On Windows, `cmd.exe` and batch files always get legacy argument passing, as raw command lines; legacy was 5.1's behavior | [about_Parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing) | "automatically use the Legacy style argument passing" and "passed as raw command-line strings to cmd.exe" and "untrusted input should be passed another way" and "Legacy is the historic behavior" and "a breaking change from the Windows PowerShell 5.1 behavior" | 2026-10-26 | 2027-10-26 |
| `ps-literalpath` | `-LiteralPath` reads no wildcards | [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem) | "No characters are interpreted as wildcards" | 2026-10-26 | 2027-10-26 |
| `ps-execpolicy` | Execution policy isn't a security boundary, users can bypass it, and outside Windows it's always `Unrestricted` | [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) | "isn't a security boundary" and "users can easily bypass a policy" and "the default execution policy is Unrestricted and can't be changed" and "Use the Unblock-File cmdlet to unblock the scripts" | 2026-10-26 | 2027-10-26 |
| `ps-signing` | `AllSigned` and `RemoteSigned` refuse unsigned scripts; App Control for Business is serviced as a security feature, and AppLocker isn't | [about_Signing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_signing); [Security features](https://learn.microsoft.com/en-us/powershell/scripting/security/security-features) | "prevent PowerShell from running scripts that don't have a digital signature" and "App Control for Business is designed as a security feature" and "AppLocker isn't a security feature" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is in this module's own words. Sources are quoted briefly, with attribution, and
each quote is a dated fact above. No code was copied from them.

| Source | Used for | License |
|---|---|---|
| [PowerShell documentation on Microsoft Learn](https://learn.microsoft.com/en-us/powershell/), PSScriptAnalyzer's and SecretManagement's included | `-NonInteractive`, `Invoke-Expression`, exit codes, argument passing, `-LiteralPath`, execution policy, signing, security features, analyzer rules, SecretManagement's status | Docs CC BY 4.0, code MIT: short quotes, with attribution |
| [PowerShell/SecretManagement README](https://github.com/PowerShell/SecretManagement) | The secret types it stores, and passwordless sign-in | MIT: short quotes, with attribution |
