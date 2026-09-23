# RESEARCH RUN R11: C# and .NET, PowerShell, Windows Server and Active Directory

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: csharp-dotnet, powershell, windows-server, and legacy-languages (.NET Framework, Windows PowerShell 5.1, VBScript).

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Beliefs marked "(the standard, date)"** come from this repository's own standard,
   PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R11 · FORM: research-result v1
Save as: R11-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- .NET 10 (LTS) was released in November 2025 with C# 14; .NET 11 is due in November 2026; .NET 8 (LTS) and .NET 9 (STS, whose support was extended to 24 months) both reach end of support in November 2026.
- C# 14 added extension members, the `field` keyword and null-conditional assignment.
- System.CommandLine reached a stable 2.0 release in 2025.
- xUnit v3 and MSTest 4 are current. Microsoft deprecated the .NET Upgrade Assistant in favour of GitHub Copilot app modernization.
- (the standard, 2026-09) PowerShell 7.6.x is current. PowerShell 7.4 (LTS) ends support in November 2026. Windows PowerShell 5.1 ships with Windows and gets security fixes only.
- (the standard, 2026-09) .NET 10 is LTS. Directory.Build.props holds shared properties and Directory.Packages.props central versions; packages.lock.json is opt-in.
- PSResourceGet replaces PowerShellGet; PSScriptAnalyzer and Pester 5 are current.
- Windows Server 2025 is current; Windows Server 2016 ends extended support in January 2027; Windows 10 ended support in October 2025, with paid Extended Security Updates.
- VBScript is a Feature on Demand being phased out: enabled by default until about 2027, then disabled, then removed. WMIC is being removed.
- Windows LAPS replaces legacy Microsoft LAPS, which is blocked on recent Windows versions. WSUS is deprecated (no new features) but still supported.
- Windows Server 2025 and Windows 11 24H2 require SMB signing by default and removed NTLMv1. Microsoft plans to disable NTLM by default and to remove RC4 from Kerberos.

## Questions

### Priority

1. .NET: the support policy and dates for every supported release, .NET 11's status and features, C# 14 features and C# 15 plans, and what a new project should target today.
2. .NET project practice:
   - SDK-style projects, Directory.Build.props, Central Package Management
   - nullable enabled, analyzers (AnalysisLevel, EnforceCodeStyleInBuild, TreatWarningsAsErrors), dotnet format, NuGet audit
   - NativeAOT and trimming: support for console, ASP.NET Core, WinForms, WPF
   - the System.CommandLine 2.0 API
   - logging (ILogger and its source generators), JSON (System.Text.Json source generation)
   - HttpClient guidance (IHttpClientFactory, Microsoft.Extensions.Http.Resilience)
3. Windows desktop: WinForms and WPF on .NET 10 (dark mode, high DPI), the current WinUI 3 / Windows App SDK version, MAUI's status, CsWin32 and LibraryImport for P/Invoke, and packaging (MSIX, unpackaged apps, toast notifications from unpackaged apps).
4. PowerShell:
   - release and support status of 7.4, 7.5 and 7.6, and what changed in 7.5 and 7.6 (for example array += performance)
   - Windows PowerShell 5.1 differences, and cmdlets removed in 7 (Get-WmiObject, Get-EventLog, Write-EventLog)
   - current versions: PSScriptAnalyzer (and its rules), Pester, PSResourceGet, SecretManagement and SecretStore
   - practice: approved verbs, comment-based help, ShouldProcess, error handling (-ErrorAction Stop, $ErrorActionPreference), detecting non-interactive runs
5. Windows Server and Active Directory security changes, 2024-2027:
   - SMB signing and SMB1; the NTLM deprecation timeline
   - removal of RC4 from Kerberos and AES enforcement; LDAP signing and channel binding
   - Windows LAPS (cmdlets, schema, the status of legacy LAPS); Credential Guard defaults
   - VBScript and WMIC removal phases, with dates
   - end dates for Windows Server 2016 and 2019
   - WSUS deprecation and its recommended replacements (Windows Autopatch, Azure Update Manager, Intune); hotpatching

### Standard

6. Active Directory best practice today:
   - tiered administration and the enterprise access model; delegation instead of Domain Admins; Protected Users
   - gMSA, and dMSA (delegated managed service accounts, Server 2025)
   - naming guidance (avoid .local), the time-sync hierarchy, DNS scavenging
   - AD CS hardening (ESC1-ESC16), and Group Policy security filtering since MS16-072
7. Security baselines: the current Microsoft Security Compliance Toolkit baselines (Server 2025, Windows 11 24H2 and 25H2), and the current CIS Benchmark versions.
8. .NET Framework and legacy: .NET Framework 4.8.1's support status; migrating WebForms (Blazor), WCF (CoreWCF, gRPC), Remoting and AppDomains; what replaced the Upgrade Assistant; VB.NET's status.
9. C# mistakes AI assistants make (for example async void, DllImport where LibraryImport fits, outdated package versions), from sources.
