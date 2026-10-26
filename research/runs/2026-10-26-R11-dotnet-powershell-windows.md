# Verification: R11 (2026-10-26)

Checked by the receiving session on 2026-10-26. Only the claims this intake relies on were
checked: those behind proposed corrections to the standard. The rest is checked when
`csharp-coding` and `powershell-scripts` are built.

| Claim | Status | Checked against |
|---|---|---|
| PowerShell 7.4 and 7.5 end on 2026-11-10; 7.6 LTS on 2028-11-14 | verified; the current 7.6 patch, contested in the report, is 7.6.6, and the current Stable 7.5.11, per Microsoft | [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6) |
| Pester 6.2.0 is current, and 5.9.1 the newest 5.x; Pester 6 targets Windows PowerShell 5.1 and PowerShell 7.4+, and "Most v5 suites run on v6 without changes" | verified; **the standard's "Pester 5.7.x is the safe pin" is contradicted** | [PowerShell Gallery](https://www.powershellgallery.com/packages/Pester); [Pester's migration guide](https://pester.dev/docs/migrations/v5-to-v6) |
| .NET 8 and 9 end on 2026-11-10; .NET 10 on 2028-11-14 | verified | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) |
| Source 48 | **not a source**: it names a tool, `mcp__Microsoft_Learn__microsoft_docs_fetch` | — |
| Everything else in the report | not yet checked | checked when the modules that rely on it are built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R11 · FORM: research-result v1
Save as: R11-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R11 result: C# and .NET, PowerShell, Windows Server and Active Directory (as of 26 October 2026)

Bottom line: the dates in the beliefs are mostly right. The biggest problems are pins and phases that have moved on. Pester 6 has been GA since July 2026 and the 5.x line itself has moved past 5.7, to 5.9.1.\[1\] WMIC is already removed from Windows 11, not "being removed".\[2\] Kerberos RC4 is past its enforcement phases (April and July 2026), not just planned.\[3\] On 10 November 2026, fifteen days from today, .NET 8, .NET 9, PowerShell 7.4 and PowerShell 7.5 all leave support on the same day,\[4\]\[5\] and Windows Server 2016 follows on 12 January 2027.\[6\]

Scope note: this run used its full search budget on the Priority questions about versions, lifecycle and security timelines. Some Priority sub-points (project practice details in Q2, most of Q3) and most Standard questions (Q6, Q7, Q9, Q10) were not researched and are listed under "Not covered". Nothing in those areas is asserted here.

## 1. Summary

- .NET 8 (LTS) and .NET 9 (STS) both reach end of support on **10 November 2026** (Microsoft .NET Blog, 29 June 2026). Move to .NET 10.\[5\]
- .NET 10 (LTS, released 11 November 2025) is the target for new projects today. It is supported "through November 2028" (Microsoft); secondary trackers give 14 November 2028.\[5\]\[7\]
- .NET 11 is at **RC2 (13 October 2026)** with a go-live licence. It is an STS release (24 months). GA is expected at .NET Conf 2026 in November (secondary: Visual Studio Magazine). C# 15 is its default language version.\[8\]\[9\]\[10\]\[11\]
- C# 14 shipped extension members, the `field` keyword and null-conditional assignment, plus `nameof` on unbound generics, user-defined compound assignment, and more (Microsoft Learn).\[12\]\[13\]
- System.CommandLine 2.0.0 went stable on 11 November 2025. The latest patch is 2.0.3 (10 February 2026) (NuGet).\[14\]
- The test frameworks have moved on: the **xunit.v3 package is at 4.0.2** (9 October 2026) and **MSTest is at 4.5.1** (7 October 2026) (NuGet).\[15\]\[16\]
- The .NET Upgrade Assistant is "officially deprecated" in favour of GitHub Copilot app modernization, which needs a paid Copilot plan (Microsoft Learn; secondary: DevClass, Techzine).\[17\]\[18\]\[19\]
- PowerShell **7.6 is the LTS line** (GA 18 March 2026, on .NET 10, support to 14 November 2028). **7.4 LTS and 7.5 both end on 10 November 2026**, so moving 7.4 to 7.5 buys no time.\[4\]\[20\]
- **Pester 6 is GA** (6.0.0 on 7 July 2026, 6.2.0 on 9 September 2026).\[21\] The 5.x line continued to 5.9.1 (11 August 2026). Pinning 5.7.x is out of date.\[1\]
- PSScriptAnalyzer 1.25.0 (20 March 2026) and PSResourceGet 1.2.0 (11 March 2026) are current. SecretManagement 1.1.2 is declared feature-complete.\[22\]\[23\]\[24\]
- Windows Server 2016 extended support ends **12 January 2027** (Microsoft Windows Server Blog, 25 February 2026); Windows Server 2019 ends 9 January 2029.
- Kerberos RC4: the January 2026 audit phase, the **April 2026 enforcement phase** (AES-SHA1 by default for accounts without `msDS-SupportedEncryptionTypes`) and the **July 2026** removal of the rollback switch have all happened (CVE-2026-20833). RC4 still works only where it is explicitly configured.\[3\]\[25\]
- NTLM: deprecated since June 2024. Network NTLM is to be **disabled by default in the next major Windows Server release** and its matching client releases (no date).\[26\]\[27\] Enforcement of the block on NTLMv1-derived single sign-on credentials became the default from the **October 2026** security update.
- SMB signing defaults differ by edition: Windows 11 24H2 Enterprise, Pro and Education require inbound and outbound signing, Windows Server 2025 requires **outbound only**, and Home requires neither.\[28\]\[29\]
- WMIC has been **removed** from all currently supported versions of Windows 11 (August and September 2026 preview updates). WMI itself stays. VBScript is still in Phase 1, with "disabled by default" planned for about 2026 or 2027.\[2\]\[30\]

## 2. Corrections

| # | What we believed | Verdict | Correct fact | Source |
|---|---|---|---|---|
| C1 | .NET 11 is due in November 2026 | Confirmed, but needs updating | .NET 11 shipped RC1 (go-live) in September 2026 and RC2 on 13 October 2026. GA is expected at .NET Conf starting 10 November 2026 (secondary).\[9\]\[11\] | https://devblogs.microsoft.com/dotnet/dotnet-11-rc-1/ ; https://www.infoq.com/news/2026/10/dotnet-11-rc-2/ |
| C2 | xUnit v3 is current | Out of date as phrased | The `xunit.v3` NuGet package is now at **4.0.2** (9 October 2026). 4.0.0 shipped 15 August 2026, and 3.2.2 (January 2026) is no longer the latest.\[31\] Pin by package version, not by "v3". | https://www.nuget.org/packages/xunit.v3 |
| C3 | MSTest 4 is current | Confirmed, needs a version | MSTest **4.5.1** (7 October 2026). 4.4.1 is marked "deprecated because it is no longer maintained".\[16\] | https://www.nuget.org/packages/MSTest |
| C4 | (the standard, 2026-10) PowerShell 7.6.x is current | Confirmed; the patch number is contested | 7.6 LTS, GA 18 March 2026. The latest 7.6.x patch differs between trackers (7.6.7, 7.6.8 or 7.6.9 in October 2026).\[32\]\[33\] See section 9. | Microsoft lifecycle table quoted by https://update.dsesecurity.com/updates/powershell-7-4-lts-7-5-end-of-support-november-10-2026-upgrade-7-6/ (secondary) |
| C5 | (the standard, 2026-10) Pester 5.7.x is the safe pin, since 6 exists and breaks things | **Wrong / out of date** | Pester 6.0.0 has been GA since 7 July 2026, and 6.2.0 came out on 9 September 2026. 5.7.1 (8 January 2025) is not even the newest 5.x: 5.8.0, 5.9.0 and 5.9.1 (11 August 2026) followed.\[1\]\[21\] Pester's own guide says "Most v5 suites run on v6 without changes". The breaks are narrow: PowerShell 5.1 or 7.4+ only, per-file discovery and run, legacy v4 parameters removed.\[34\] **The standard should change**: pin 5.9.1 if you must stay on 5, otherwise migrate to 6.2.x. | https://pester.dev/docs/migrations/v5-to-v6 ; PowerShell Gallery version history (subagent, from https://www.powershellgallery.com/packages/pester/5.7.1) |
| C6 | PowerShell 7.4 (LTS) ends support in November 2026 | Confirmed, and incomplete | 7.4 **and 7.5** both end on 10 November 2026.\[35\] | Lifecycle table quoted by secondary sources above; https://www.lansweeper.com/blog/eol/powershell-end-of-life/ (secondary) |
| C7 | PSScriptAnalyzer and Pester 5 are current | Partly wrong | PSScriptAnalyzer 1.25.0 (20 March 2026) is current. Pester 6.2.0 is current, not Pester 5.\[21\]\[24\] | https://www.powershellgallery.com/packages/PSScriptAnalyzer/1.25.0 |
| C8 | VBScript enabled by default until about 2027, then disabled, then removed | Broadly right; the date is softer | Microsoft's phases: Phase 1 is a FOD enabled by default; Phase 2, "approximately 2026 or 2027", disables it by default; Phase 3 removal has no date ("TBD").\[30\] | Microsoft 365 Developer Blog, "Prepare your VBA projects for VBScript deprecation in Windows" (Wenjun Gong): "Phase 2 (approximately 2026 or 2027): VBScript FODs will be disabled by default." https://devblogs.microsoft.com/microsoft365dev/how-to-prepare-vba-projects-for-vbscript-deprecation/ |
| C9 | WMIC is being removed | **Out of date** | WMIC "has now been removed from currently supported versions of Windows 11 and is no longer available as a Feature on Demand". It went out in the August 2026 preview update for 24H2 and 25H2 and the September 2026 preview update for 26H1. Windows Server 2025 was dropped from the article's "Applies to".\[2\] | https://support.microsoft.com/en-us/topic/windows-management-instrumentation-command-line-wmic-removal-from-windows-e9e83c7f-4992-477f-ba1d-96f694b8665d |
| C10 | Windows Server 2025 and Windows 11 24H2 require SMB signing by default | Partly wrong (too broad) | Windows 11 24H2 Enterprise, Pro and Education require outbound **and** inbound signing. **Windows Server 2025 requires outbound signing only.** Windows 11 24H2 Home requires neither.\[28\] | https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing |
| C11 | They removed NTLMv1 | Confirmed, plus a newer change | NTLMv1 is removed in 24H2 and Windows Server 2025. In addition, from the **October 2026** security update the block on NTLMv1-derived credentials for single sign-on (`BlockNtlmv1SSO`) is enforced by default.\[36\]\[37\]\[38\] | https://support.microsoft.com/en-us/topic/upcoming-changes-to-ntlmv1-in-windows-11-version-24h2-and-windows-server-2025-c0554217-cdbc-420f-b47c-e02b2db49b2e ; https://www.elevenforum.com/t/manage-changes-to-ntlmv1-and-prevent-network-issues-in-windows-11-and-windows-server-2025.50172/ (secondary, quotes Microsoft) |
| C12 | Microsoft plans to disable NTLM by default | Confirmed, with scope | Disabled by default (not removed) "in the next major release of Server and Client (subject to change)". Machines already in the field keep NTLM.\[26\] | https://techcommunity.microsoft.com/blog/windows-itpro-blog/retiring-ntlm-frequently-asked-questions/4550522 |
| C13 | Microsoft plans to remove RC4 from Kerberos | **Out of date / imprecise** | This is no longer a plan. It was delivered in 2026 as a change of *default*, not a removal: audit from 13 January 2026; from 14 April 2026, enforcement with AES-SHA1 (0x18) as the default for accounts without `msDS-SupportedEncryptionTypes`; from July 2026 the `RC4DefaultDisablementPhase` rollback is gone. RC4 still works where it is explicitly configured.\[25\]\[39\] Secondary sources say Microsoft has no announced plan to remove RC4 from Windows entirely.\[40\] | https://techcommunity.microsoft.com/discussions/microsoft-security/kerberos-and-the-end-of-rc4-protocol-hardening-and-preparing-for-cve%E2%80%912026%E2%80%9120833/4502262 (community post); https://www.mgworkplace.it/en/field-guides/rc4-deprecation-active-directory (secondary, cites KB5073381) |
| C14 | .NET 9 STS support extended to 24 months | Confirmed | "STS releases now get 24 months of support instead of 18."\[5\] | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ |
| C15 | System.CommandLine reached stable 2.0 in 2025 | Confirmed, needs a version | 2.0.0 on 11 November 2025; latest 2.0.3 on 10 February 2026.\[14\] | https://www.nuget.org/packages/System.CommandLine/2.0.0-beta2.21617.1 (version table) |
| C16 | SecretManagement and SecretStore (implied current) | Confirmed, with a caveat | SecretManagement 1.1.2 and SecretStore 1.0.6 (both 27 January 2022). The README says 1.1.2 "will be the last feature release".\[23\]\[41\]\[42\] | PowerShell Gallery; https://github.com/PowerShell/SecretManagement (subagent) |

Confirmed without change: C# 14 features; .NET 10 is LTS; Upgrade Assistant deprecated; Windows Server 2016 ends extended support January 2027 (12 January); legacy Microsoft LAPS blocked on recent Windows; WSUS deprecated but supported; Windows 7.x installs side by side with 5.1 (not re-verified, see section 9).

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | .NET 8 end of support | 10 Nov 2026 | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | "That support window closes on **November 10, 2026**."\[5\] | 2026-06-29 |
| 2 | .NET 9 end of support | 10 Nov 2026 | same | "That puts .NET 9 end of support on the same day: **November 10, 2026**."\[5\] | 2026-06-29 |
| 3 | .NET 10 release and support | 11 Nov 2025; LTS to Nov 2028 | same | "| .NET 10 | November 11, 2025 | LTS | November 2028 |"\[5\] | 2026-06-29 |
| 4 | Final .NET 8 and 9 patch | Possible on 10 Nov 2026 | same | ".NET 8 and .NET 9 may each receive one final update on that day if there is a known critical issue."\[5\] | 2026-06-29 |
| 5 | .NET 11 RC1 go-live | Go-live licence | https://devblogs.microsoft.com/dotnet/dotnet-11-rc-1/ | "This is our first release candidate, which comes with a go-live support license"\[43\] | Sept 2026 (read 2026-10-26) |
| 6 | .NET 11 RC2 | 13 Oct 2026 (secondary) | https://tech-insider.org/microsoft-dotnet-11-rc2-dotnetup-tool-2026/ | "Microsoft pushed out **.NET 11 Release Candidate 2** on October 13, 2026"\[11\] | 2026-10 |
| 7 | .NET 11 RC2 adds no C# features | — | https://www.infoq.com/news/2026/10/dotnet-11-rc-2/ | "with no new C# language features"\[44\] | 2026-10 |
| 8 | C# 15 is the default in .NET 11 | — | https://www.infoq.com/news/2026/09/dotnet-11-rc-1-release/ | "Release Candidate 1 makes C# 15 the default language version for projects that target .NET 11."\[10\] | 2026-09 |
| 9 | .NET 11 support length | STS, 2 years (secondary) | https://www.i-programmer.info/news/89-net/19225-net-11-release-candidate-2-updates-f.html | ".NET 11 will have two years of standard term support (STS)."\[8\] | 2026-10-19 |
| 10 | C# 14 features | List | https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14 | "Extension members … Null-conditional assignment … field backed properties … user-defined compound assignment operators"\[13\] | read 2026-10-26 |
| 11 | Null-conditional assignment | `?.`/`?[]` on the left side | https://github.com/dotnet/docs/blob/main/docs/csharp/whats-new/csharp-14.md | "The null-conditional member access operators, ?. and ?[], can now be used on the left hand side of an assignment or compound assignment." | read 2026-10-26 |
| 12 | System.CommandLine stable | 2.0.0, 11 Nov 2025; 2.0.3, 10 Feb 2026 | https://www.nuget.org/packages/System.CommandLine/2.0.0-beta2.21617.1 | "| 2.0.3 | 1,064,249 | 2/10/2026 |" / "| 2.0.0 | 1,988,217 | 11/11/2025 |" | read 2026-10-26 |
| 13 | xunit.v3 current | 4.0.2, 9 Oct 2026 | https://www.nuget.org/packages/xunit.v3 | "| 4.0.2 | 1,408,362 | 10/9/2026 |"\[15\] | read 2026-10-26 |
| 14 | MSTest current | 4.5.1, 7 Oct 2026 | https://www.nuget.org/packages/MSTest | "| 4.5.1 | 166,676 | 10/7/2026 |"\[16\] | read 2026-10-26 |
| 15 | Upgrade Assistant deprecated | Use Copilot app modernization | https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview | ".NET Upgrade Assistant is officially deprecated. Use the GitHub Copilot modernization chat agent instead, which is included with Visual Studio 2026 and Visual Studio 2022 17.14.16 or later."\[17\] | read 2026-10-26 |
| 16 | Upgrade Assistant fallback | Only without Copilot | https://learn.microsoft.com/en-us/dotnet/core/porting/ | "Use it only if you can't use the modernization agent—for example, if your environment doesn't have access to GitHub Copilot."\[45\] | read 2026-10-26 |
| 17 | PowerShell 7.6 LTS | GA 18 Mar 2026, EOS 14 Nov 2028, .NET 10 | https://update.dsesecurity.com/updates/powershell-7-4-lts-7-5-end-of-support-november-10-2026-upgrade-7-6/ (quotes Microsoft Learn lifecycle) | "PowerShell 7.6 (LTS) on .NET 10.0, released 18-Mar-2026, with end of support on 14-Nov-2028"\[4\] | 2026 |
| 18 | PowerShell 7.4 and 7.5 EOS | 10 Nov 2026 | same | "PowerShell 7.4 (LTS) on .NET 8.0 and PowerShell 7.5 on .NET 9.0 with end of support on 10-Nov-2026"\[4\] | 2026 |
| 19 | PowerShell lifecycle follows .NET | — | https://windowsforum.com/news/powershell-7-4-21-released-config-fixes-update-steps-and-7-6-lts-migration.448185/ (quotes Microsoft) | "the end-of-support dates follow the .NET Support Policy for the version of .NET that the release of PowerShell was built upon"\[46\] | 2026-10 |
| 20 | PowerShell 7.7 preview | 7.7.0-preview.5, 23 Sep 2026 (secondary) | https://en.wikipedia.org/wiki/PowerShell | "Preview release: 7.7.0-preview.5 / September 23, 2026"\[47\] | read 2026-10-26 |
| 21 | PowerShell 7.5 `+=` speed-up | PR #23901 | https://learn.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-75 | "PowerShell 7.5-rc.1 included PR#23901 from @jborean93 that improves the performance of the += operation for an array of objects."\[48\] | read 2026-10-26 |
| 22 | `+=` compared with `List<T>` | Faster in 7.5 | same | "Now, it's also faster than using the List<T>.Add(T) method."\[48\] | read 2026-10-26 |
| 23 | Pester 6 GA | 6.0.0, 7 Jul 2026; 6.2.0, 9 Sep 2026 | PowerShell Gallery version table (subagent, https://www.powershellgallery.com/packages/Pester/6.0.0-alpha4) | "| 6.2.0 | 783,123 | 9/9/2026 |" / "| 6.0.0 | 255,059 | 7/7/2026 |"\[21\] | read 2026-10-26 |
| 24 | Pester 5.x latest | 5.9.1, 11 Aug 2026 | PowerShell Gallery (subagent) | "| 5.9.1 | 51,288 | 8/11/2026 |"\[1\] | read 2026-10-26 |
| 25 | Pester 6 platforms | PowerShell 5.1 and 7.4+ | https://pester.dev/docs/migrations/v5-to-v6 | "Pester 6 targets **Windows PowerShell 5.1** and **PowerShell 7.4+**."\[34\] | read 2026-10-26 |
| 26 | Pester 6 compatibility | Most v5 suites run | same | "Most v5 suites run on v6 without changes."\[34\] | read 2026-10-26 |
| 27 | PSScriptAnalyzer current | 1.25.0, 20 Mar 2026 | https://www.powershellgallery.com/packages/PSScriptAnalyzer/1.25.0 | "| 1.25.0 (current version) | 4,460,520 | 3/20/2026 |"\[24\] | read 2026-10-26 |
| 28 | PSScriptAnalyzer 1.25 rules | New or updated rules | https://learn.microsoft.com/en-us/powershell/scripting/community/2026-updates?view=powershell-7.6 | "Updated PSScriptAnalyzer docs for v1.25 release including 6 new or updated rules"\[49\] | 2026-03 |
| 29 | PSResourceGet current | 1.2.0, 11 Mar 2026; 1.3.0-rc1, 20 Oct 2026 | PowerShell Gallery (subagent) | "| 1.2.0 | 2,827,576 | 3/11/2026 |"\[22\] | read 2026-10-26 |
| 30 | SecretManagement | 1.1.2, feature-complete | https://github.com/PowerShell/SecretManagement (subagent) | "Microsoft.PowerShell.SecretManagement is feature complete, so 1.1.2 will be the last feature release."\[23\] | read 2026-10-26 |
| 31 | SecretStore | 1.0.6, 27 Jan 2022 | PowerShell Gallery (subagent) | "| 1.0.6 | 6,625,100 | 1/27/2022 |"\[41\] | read 2026-10-26 |
| 32 | Windows Server 2016 EOS | 12 Jan 2027 | Microsoft Windows Server Blog, "Planning ahead for Windows Server 2016 end of support" | "In accordance with the Microsoft Lifecycle Policy, extended support for Windows Server 2016 will end on January 12, 2027." | 2026-02-25 |
| 33 | Windows Server 2019 EOS | 9 Jan 2029 (secondary) | https://en.wikipedia.org/wiki/Windows_Server_2019 | "extended support will end on January 9, 2029"\[50\] | read 2026-10-26 |
| 34 | SMB signing by edition | See C10 | https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing | "Windows Server 2025 requires outbound SMB signing only." | read 2026-10-26 |
| 35 | Do not disable signing to work around failures | — | https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3 | "Don't disable SMB protocol versions or SMB signing to work around these connection failures." | read 2026-10-26 |
| 36 | SMBv1 not installed | Windows 11, Server 2019+ | same | "SMBv1 isn't installed by default in any edition of Windows 11 or Windows Server 2019 and later versions." | read 2026-10-26 |
| 37 | NTLMv1 removed | Windows 11 24H2, Windows Server 2025 | https://learn.microsoft.com/en-us/windows/whats-new/whats-new-windows-11-version-24h2 | "NTLMv1 is removed starting in Windows 11, version 24H2 and Windows Server 2025." | read 2026-10-26 |
| 38 | NTLM disable target | Next major Server and Client release | https://techcommunity.microsoft.com/blog/windows-itpro-blog/retiring-ntlm-frequently-asked-questions/4550522 | "Our current target for default disablement is the next major release of Server and Client (subject to change)."\[26\] | 2026 |
| 39 | NTLM not removed from current versions | — | same | "In-market versions of Windows client and Windows Server will continue to support NTLM."\[26\] | 2026 |
| 40 | NTLM Phase 2 | H2 2026: IAKerb, Local KDC | https://m365admin.handsontek.net/advancing-windows-security-disabling-ntlm-default/ (republishes Microsoft) | "In the second half of 2026, new tools will be available to Windows Server 2025 and Windows 11, version 24H2 and later: IAKerb, Local KDC"\[27\] | 2026-01 |
| 41 | NTLM deprecated since | June 2024 | same | "NTLM has been deprecated since June 2024."\[27\] | 2026-01 |
| 42 | RC4 final enforcement | July 2026 | https://techcommunity.microsoft.com/discussions/microsoft-security/kerberos-and-the-end-of-rc4-protocol-hardening-and-preparing-for-cve%E2%80%912026%E2%80%9120833/4502262 | "Starting in July 2026, audit mode and rollback options are removed. RC4 will only function if explicitly configured"\[25\] | 2026 |
| 43 | RC4 April default | AES-SHA1 0x18 | https://www.mgworkplace.it/en/field-guides/rc4-deprecation-active-directory (secondary) | "For accounts without explicit msDS-SupportedEncryptionTypes, the KDC default becomes AES-SHA1 (DefaultDomainSupportedEncTypes = 0x18)."\[39\] | 2026 |
| 44 | Legacy LAPS | Deprecated, MSI blocked | https://www.microsoft.com/en-us/download/details.aspx?id=46899 | "The legacy Microsoft LAPS product is deprecated as of Windows 11 23 H2 and later. Installation of the legacy Microsoft LAPS MSI package is blocked on newer OS versions." | read 2026-10-26 |
| 45 | Windows LAPS availability | Server 2019+ and supported Windows 10/11 | https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview | "Windows LAPS is available on Windows Server 2019 and later, and on supported Windows 10 and Windows 11 clients." | read 2026-10-26 |
| 46 | WSUS deprecated | No new features, still supported | https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-server-update-services-wsus-deprecation/4250436 | "we are no longer investing in new capabilities, nor are we accepting new feature requests for WSUS." | 2024-09 (edited 2024-09-25) |
| 47 | WSUS replacements | Autopatch, Intune, Azure Update Manager | same | "we recommend organizations transition to cloud tools, including Windows Autopatch and Microsoft Intune for client update management and Azure Update Manager for server update management." | 2024-09 |
| 48 | WMIC removed | Windows 11 (supported versions) | https://support.microsoft.com/en-us/topic/windows-management-instrumentation-command-line-wmic-removal-from-windows-e9e83c7f-4992-477f-ba1d-96f694b8665d | "The WMIC utility has now been removed from currently supported versions of Windows 11 and is no longer available as a Feature on Demand (FoD)."\[2\] | 2026-09-29 |
| 49 | WMI stays | — | same | "No, WMI is not being removed. Only the WMIC command-line tool is being removed."\[2\] | 2026-09-29 |
| 50 | VBScript Phase 2 | ~2026 or 2027 | https://devblogs.microsoft.com/microsoft365dev/how-to-prepare-vba-projects-for-vbscript-deprecation/ (Microsoft 365 Developer Blog, Wenjun Gong) | "Phase 2 (approximately 2026 or 2027): VBScript FODs will be disabled by default." | 2025 |
| 51 | Windows App SDK current | 2.5.1, 16 Sep 2026 | https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/release-channels | "2.5.1 Released: 09/16/2026" | read 2026-10-26 |
| 52 | Windows App SDK 2.0 servicing end | 29 Apr 2027 | same | "| 2.0 | 04/29/2026 | 2.5.1 | 09/16/2026 | Current | 04/29/2027 |" | read 2026-10-26 |
| 53 | WinForms .NET 11 designer analyzers | WFO3000–WFO3002 | https://www.infoq.com/news/2026/10/dotnet-11-rc-2/ | "New analyzers WFO3000 to WFO3002 flag code that cannot round-trip through the Designer, which the release notes say is particularly useful when AI tools generate or refactor forms."\[44\] | 2026-10 |

## 4. Findings

### Q1. .NET support policy, .NET 11, C# 14 and 15, what to target

**Policy.** LTS releases get 36 months of support, and STS releases now get 24 months instead of 18 (fact 1, C14).\[5\] Because both are counted from GA, .NET 8 (LTS, November 2023) and .NET 9 (STS, November 2024) end on the same Patch Tuesday, 10 November 2026.\[51\] Microsoft may ship one final update that day (fact 4).\[5\] Only the latest patch of a supported release is supported.\[52\] A secondary source notes the latest .NET 10 patch as 10.0.13 (13 October 2026).\[53\]

| Release | Type | GA | End of support | Status 26 Oct 2026 |
|---|---|---|---|---|
| .NET 8 | LTS | 14 Nov 2023 | 10 Nov 2026 | **Ends in 15 days** |
| .NET 9 | STS (24 months) | 12 Nov 2024 | 10 Nov 2026 | **Ends in 15 days** |
| .NET 10 | LTS | 11 Nov 2025 | "November 2028" (Microsoft); 14 Nov 2028 (secondary trackers) | Active |
| .NET 11 | STS | RC2 13 Oct 2026; GA expected Nov 2026 | Expected Nov 2028 (projected, secondary) | Go-live RC |

**.NET 11.** RC1 and RC2 carry go-live licences. RC2 has no new C# features.\[43\]\[44\] Areas named in RC1 and RC2: JSON closed-type polymorphism and union support, AES Key Wrap, TLS channel binding on Unix, incremental CBOR reading, experimental composite ML-KEM and HPKE APIs, F# runtime async, MAUI C# UI, and Windows Forms `KioskModeManager` with designer analyzers.\[43\]\[54\] RC2 has one runtime breaking change: per InfoQ, file locking under `FileShare` is no longer enforced in one scenario, and `DOTNET_SYSTEM_IO_DISABLEFILELOCKING=0` restores it.\[44\] Read the dotnet/core RC2 notes before relying on this. A new `dotnetup` SDK acquisition tool was announced on 15 October 2026 (secondary).\[11\] GA is expected at .NET Conf 2026, starting 10 November (secondary: Visual Studio Magazine).\[9\] It is not yet released, so treat this as an expected date.

**C# 14** (with .NET 10): extension members (extension properties, static extension members, extension blocks), null-conditional assignment, `nameof` on unbound generic types, `field`-backed properties, user-defined compound assignment operators, preprocessor directives for file-based apps, and more partial members (Learn, facts 10 and 11).\[13\] The belief is confirmed.

**C# 15** (with .NET 11, default from RC1): union types and the `closed` modifier for closed hierarchies are reported, along with collection-expression arguments and labelled `break` and `continue` (secondary: fast-report.com, InfoQ).\[55\] The final feature list was **not verified against the Microsoft Learn "What's new in C# 15" page** in this run.

**What a new project should target today: `net10.0` (LTS).** .NET 11 is a pre-GA STS release. Its support would also end in November 2028, so it gains no lifetime over .NET 10.\[53\]\[56\] Choose it only for a specific feature, and only once it is GA.

### Q2. .NET project practice

Verified in this run:
- **System.CommandLine 2.0** went stable on 11 November 2025. Use 2.0.3 (10 February 2026), MIT licence (fact 12). The NuGet page lists "Breaking Changes" since beta7.\[57\] The 2.0 API (for example `RootCommand`, `Option<T>`, `SetAction`, `Parse(args).Invoke()`) was **not verified against the docs** in this run. Check https://learn.microsoft.com/dotnet/standard/commandline/ before writing guidance, because older beta4 samples (`SetHandler`, `InvocationContext`) are widespread online.
- Test frameworks: xunit.v3 4.0.2 and MSTest 4.5.1 (facts 13 and 14).\[15\]\[16\]

Not researched in this run (see section 9): Directory.Build.props and Central Package Management semantics, `packages.lock.json` opt-in, nullable, AnalysisLevel, EnforceCodeStyleInBuild, TreatWarningsAsErrors, `dotnet format`, NuGet Audit defaults, NativeAOT and trimming support for each app model, ILogger source generators, System.Text.Json source generation, and IHttpClientFactory with Microsoft.Extensions.Http.Resilience. The standard's 2026-09 belief about Directory.Build.props, Directory.Packages.props and opt-in lock files is therefore **not verified** by this run.

### Q3. Windows desktop

- **Windows App SDK / WinUI 3:** stable **2.5.1** (16 September 2026). Windows App SDK 2.0 GA was 29 April 2026, and its servicing ends 29 April 2027 (facts 51 and 52). 2.0 moved to SemVer; "the next side-by-side release will be 3.0.0". The latest experimental build is 2.5.4-experimental (29 September 2026).\[58\]\[59\]\[60\] Windows App SDK 2.2.0 added "a first-class ApplicationData entry point for unpackaged apps" (GitHub discussion #6554).\[61\]
- **WinForms on .NET 11:** visual-style refresh, `KioskModeManager`, and analyzers WFO3000–WFO3002 for designer round-tripping (fact 53).\[44\]\[54\]
- **MAUI:** RC2 notes mention C# UI creation and faster Android builds (secondary).\[10\]\[54\] Its support status was not separately verified.
- Not researched: WinForms and WPF dark mode and high-DPI status on .NET 10, CsWin32 version, LibraryImport guidance, MSIX tooling, and toast notifications from unpackaged apps.

### Q4. PowerShell

**Release and support status.**

| Line | Type | .NET | GA | End of support | Note |
|---|---|---|---|---|---|
| 7.4 | LTS | 8 | 16 Nov 2023 | **10 Nov 2026** | Latest patch reported as 7.4.21 (October 2026, secondary) |
| 7.5 | Stable (non-LTS) | 9 | 22 Jan 2025 | **10 Nov 2026** | Learn page now covers 7.5.11 |
| 7.6 | LTS | 10 | 18 Mar 2026 | 14 Nov 2028 | Latest patch: contested (see section 9) |
| 7.7 | Preview | (likely 11, not verified) | — | — | 7.7.0-preview.5, 23 Sep 2026 (secondary) |

The lifecycle follows the .NET release that PowerShell is built on (fact 19).\[46\] The PowerShell lifecycle also excludes modules shipped outside the package; for example, the ActiveDirectory module follows the Windows lifecycle (secondary, citing Microsoft Learn).\[20\]

**What changed.** In 7.5, `+=` on object arrays was optimised by PR #23901. Microsoft's benchmark for 10,240 elements dropped from 1668.13 ms (7.4.6) to 104.73 ms, now "faster than using the List<T>.Add(T) method" (facts 21 and 22).\[48\] In 7.6 (secondary summaries: 4sysops, powershellisfun): PSReadLine 2.4.5; PSResourceGet 1.2.0; ThreadJob becomes the built-in `Microsoft.PowerShell.ThreadJob`, and the old module warns and forwards; `PSForEach()` and `PSWhere()` aliases; `Get-Clipboard -Delimiter`; `Get-Command -ExcludeModule`; `Register-ArgumentCompleter -NativeFallback`; `New-Item -Target` treated as literal; `NO_COLOR` respected; full HTTP headers in `-Verbose` and bodies in `-Debug` for the web cmdlets; "four breaking changes".\[62\]\[63\]\[64\] 7.6.8 removed the in-product update notification (secondary).\[65\]

**Windows PowerShell 5.1 differences, and Get-WmiObject, Get-EventLog and Write-EventLog removed in 7:** not re-verified in this run (section 9).

**Module versions:** PSScriptAnalyzer 1.25.0, Pester 6.2.0 (5.x: 5.9.1), PSResourceGet 1.2.0 (1.3.0-rc1 is pre-release), SecretManagement 1.1.2, SecretStore 1.0.6 (facts 23 to 31). The new or updated rules in PSScriptAnalyzer 1.25 named on Learn are AlignAssignmentStatement, AvoidLongLines, UseConsistentParameterSetName, UseConsistentParametersKind and UseConstrainedLanguageMode (the Learn excerpt lists five of the six).\[49\]

**Pester 6 migration.** Classic `Should -Be` still works. The new `Should-*` assertions are opt-in. Discovery and run now happen per file. A parallel runner is experimental. Code coverage is profiler-based by default and supports Cobertura. Legacy v4 parameters are gone. Minimum versions are PowerShell 5.1 and 7.4+ (pester.dev).\[34\]\[66\]\[67\] A secondary source says `Assert-MockCalled` and `Assert-VerifiableMock` are removed; check this in the migration guide.\[67\]

**Practice** (approved verbs, comment-based help, ShouldProcess, error handling, detecting non-interactive runs): not researched (section 9).

### Q5. Windows Server and AD security changes, 2024–2027

- **SMB:** signing required by default as described in C10. SMBv1 is not installed by default on Windows 11 or Windows Server 2019+ (fact 36). Microsoft explicitly says not to disable signing to work around failures (fact 35).\[68\] Windows 11 24H2 adds an SMB client NTLM-blocking option with an exception list (Learn 24H2 page).\[69\]
- **NTLM timeline:** deprecated June 2024. Phase 1 (now): enhanced NTLM auditing in Windows 11 24H2 and Windows Server 2025. Phase 2 (H2 2026): IAKerb, Local KDC, and Kerberos-first negotiation in core features. Phase 3: network NTLM disabled by default in the next major Server LTSC release and its client releases, with re-enablement by policy. No date is announced (facts 38 to 41).\[27\]\[40\]\[70\]\[71\] NTLMv1 is removed, and `BlockNtlmv1SSO` enforcement is the default from the October 2026 update (C11).
- **Kerberos RC4 / AES:** see C13 and facts 42 and 43. Audit events are KDCSVC 201–209 (secondary).\[3\] Action: set `msDS-SupportedEncryptionTypes` explicitly and make sure service accounts have AES keys (reset the password if the account predates AES).
- **LDAP signing and channel binding:** not researched in this run. A secondary source claims "LDAP sealing by default on new deployments" for Windows Server 2025; this is unverified.\[29\]
- **Windows LAPS:** native on Windows Server 2019+ and supported Windows 10 and 11 (April 2023 updates). Legacy LAPS is deprecated from Windows 11 23H2 and its MSI is blocked. Legacy LAPS emulation mode exists for migration.\[72\]\[73\]\[74\] Automatic account management needs Windows 11 24H2 or Windows Server 2025 (facts 44 and 45; Learn overview).\[75\]\[76\] The cmdlet `Get-LapsADPassword` appears in secondary material.\[77\] The full cmdlet and schema list (`Update-LapsADSchema` and others) was not verified.
- **Credential Guard defaults:** Microsoft Learn's Credential Guard overview says "Starting in Windows 11, 22H2 and Windows Server 2025, Credential Guard is enabled by default on domain-joined, non-DC systems that meet hardware requirements", and this default enablement is without UEFI Lock.
- **VBScript:** see C8. **WMIC:** removed from supported Windows 11 (C9). Whether it is present on Windows Server 2025 is unclear: the support article dropped Server 2025 from "Applies to" on 26 August 2026.\[2\] Do not assume it is present.
- **End dates:** Windows Server 2016, 12 January 2027; Windows Server 2019, 9 January 2029 (facts 32 and 33).\[6\]\[50\] A secondary source says Windows Server 2016 ESU via Azure Arc is billed from 13 January 2027.\[78\]
- **WSUS:** deprecated (announced September 2024). It still works and is supported in Windows Server 2025, with no plan to remove it from in-market versions. Replacements are Windows Autopatch and Intune for clients and Azure Update Manager (with Azure Arc on-premises) for servers. Configuration Manager is unaffected (facts 46 and 47).\[79\]\[80\]\[81\]\[82\] Hotpatching was not researched.

### Q6–Q10 (Standard)

Q8: the Upgrade Assistant replacement is confirmed (facts 15 and 16).\[17\] Microsoft's .NET Framework support policy lists .NET Framework 4.6.2's end of support as 12 January 2027 ("| .NET Framework 4.6.2 | August 2, 2016 | Active | January 12, 2027"); 4.8.1's status was not verified. Everything else in Q6–Q10 was not researched; see section 9.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| .NET SDK / runtime 10 | Build and run .NET (LTS) | 10.0.13 runtime (secondary) | 13 Oct 2026\[53\] | `winget install Microsoft.DotNet.SDK.10` (not verified) | `global.json` | https://en.wikipedia.org/wiki/.NET (secondary) |
| .NET 11 | Next STS | 11.0.0-rc.2 | 13 Oct 2026\[53\] | Preview SDK from dotnet.microsoft.com | `global.json` | InfoQ, tech-insider (secondary) |
| PowerShell | Shell | 7.6.x LTS (patch contested) | GA 18 Mar 2026 | `winget install Microsoft.PowerShell` (not verified) | `powershell.config.json` | Lifecycle table (via secondary) |
| PSScriptAnalyzer | PowerShell linter | 1.25.0 | 20 Mar 2026\[24\] | `Install-PSResource PSScriptAnalyzer -Version 1.25.0` | `PSScriptAnalyzerSettings.psd1` | PowerShell Gallery |
| Pester | PowerShell tests | 6.2.0 (5.x: 5.9.1) | 9 Sep 2026\[21\] | `Install-PSResource Pester -Version 6.2.0` | `New-PesterConfiguration` object | PowerShell Gallery; pester.dev |
| PSResourceGet | Module install (replaces PowerShellGet cmdlets) | 1.2.0 (1.3.0-rc1 pre-release) | 11 Mar 2026\[22\] | Ships in 7.6 | — | PowerShell Gallery |
| SecretManagement / SecretStore | Secrets | 1.1.2 / 1.0.6 | 27 Jan 2022\[41\]\[42\] | `Install-PSResource Microsoft.PowerShell.SecretManagement` | — | PowerShell Gallery |
| System.CommandLine | CLI parsing | 2.0.3 | 10 Feb 2026 | `dotnet add package System.CommandLine --version 2.0.3` | — | NuGet |
| xunit.v3 | Unit tests | 4.0.2 | 9 Oct 2026\[15\] | `dotnet add package xunit.v3 --version 4.0.2` | `xunit.runner.json` | NuGet |
| MSTest | Unit tests | 4.5.1 | 7 Oct 2026\[16\] | `dotnet add package MSTest --version 4.5.1` | `.runsettings` / `testconfig.json` | NuGet |
| Windows App SDK | WinUI 3 and Windows APIs | 2.5.1 | 16 Sep 2026 | NuGet `Microsoft.WindowsAppSDK` | project file | Microsoft Learn |
| GitHub Copilot app modernization | .NET upgrades (replaces Upgrade Assistant) | Not found | GA September 2025 (secondary: DevClass)\[19\] | Visual Studio 2026 / Visual Studio 2022 17.14.16+ | — | Microsoft Learn |
| .NET Upgrade Assistant | Deprecated | Not found | — | VS: Tools > Options > Projects and Solutions > Modernization > "Enable legacy Upgrade Assistant" (secondary)\[19\] | — | Microsoft Learn; DevClass |

## 6. Changing in the next 12 months

Flagged items reach end of support within 12 months.

| Date | Change | Flag | Source |
|---|---|---|---|
| 10 Nov 2026 | .NET 8 and .NET 9 end of support\[5\] | ⚠ | Microsoft .NET Blog |
| 10 Nov 2026 | PowerShell 7.4 LTS and 7.5 end of support\[4\] | ⚠ | Lifecycle table (via secondary) |
| 10 Nov 2026 | Windows 11 Enterprise and Education 23H2 end of updates ("Windows 11, version 23H2 Enterprise and Education editions reach end of updates on November 10, 2026", per Microsoft's Windows message center reminder of 15 Sep 2026 as reported by Neowin and windowsforum); Microsoft recommends moving to 25H2 | ⚠ | Windows message center / release health (via secondary) |
| Nov 2026 (expected) | .NET 11 GA (STS) with C# 15\[9\]\[11\] | — | Visual Studio Magazine (secondary) |
| H2 2026 | NTLM Phase 2: IAKerb and Local KDC for Windows Server 2025 and Windows 11 24H2+\[27\] | — | Microsoft roadmap |
| Oct 2026 (done) | `BlockNtlmv1SSO` enforced by default | — | Microsoft Support |
| 12 Jan 2027 | Windows Server 2016 end of extended support (also Hyper-V Server 2016, and WSUS and IIS 10 on 2016, per secondary)\[83\] | ⚠ | Microsoft Windows Server Blog (25 Feb 2026); endoflife.ai (secondary, for the related products) |
| 12 Jan 2027 | .NET Framework 4.6.2 end of support | ⚠ | Microsoft .NET Framework support policy |
| ~2026–2027 | VBScript Phase 2: disabled by default\[30\] | ⚠ (possible) | Microsoft 365 Developer Blog |
| 29 Apr 2027 | Windows App SDK 2.0 servicing ends | ⚠ | Microsoft Learn |
| Next major Windows Server LTSC (no date) | Network NTLM disabled by default\[26\] | — | Microsoft FAQ |

Already happened in 2026 (breaking): Kerberos RC4 enforcement (April) and rollback removal (July); WMIC removed from Windows 11 (August and September); Windows Server 2022 mainstream support and Windows Server 2012/R2 ESU ended 13 October 2026 (secondary: endoflife.ai).\[2\]\[3\]\[84\]

## 7. Common mistakes (including AI coding assistants)

1. **Upgrading PowerShell 7.4 to 7.5 "for support".** Both end on 10 November 2026; go to 7.6 (facts 17 and 18).\[20\]
2. **Upgrading .NET 8 to .NET 9.** Both end on the same day; go to .NET 10 (fact 2).\[85\]
3. **Pinning Pester 5.7.x and avoiding 6 as "breaking".** Most v5 suites run unchanged on v6 (fact 26).\[34\]
4. **Generating `wmic` calls in scripts.** WMIC is removed from supported Windows 11. Use `Get-CimInstance` (fact 48).\[2\]\[86\]
5. **Disabling SMB signing or re-enabling SMBv1 to "fix" connection failures.** Microsoft says not to (fact 35).\[68\]
6. **Assuming Kerberos can silently fall back to RC4.** Since April and July 2026 it cannot, for accounts without explicit encryption types (fact 42).\[25\]
7. **Recommending the .NET Upgrade Assistant as the primary tool.** It is deprecated (fact 15). Also, developers reported that the Copilot replacement "introduced nuget packages during a migration that do not exist at all" (secondary: Techzine).\[18\] Verify every package an AI proposes against nuget.org.
8. **AI-generated WinForms code that the Designer cannot load.** Microsoft added analyzers WFO3000–WFO3002 for exactly this case (fact 53).\[44\]
9. **Writing System.CommandLine code against beta4 APIs.** 2.0 stable has breaking changes since the betas (NuGet release notes).
10. **Referring to "xUnit v3" as a version pin.** The `xunit.v3` package is now version 4.x (fact 13).\[15\]
11. **Installing legacy LAPS on new machines.** The MSI is blocked; use Windows LAPS (fact 44).\[72\]

Not sourced in this run, so not asserted: async void, DllImport compared with LibraryImport, and other generic AI C# mistakes (Q9).

## 8. Sources and licences

Licence identification is based on each publisher's published terms as generally known. **Re-check each licence before adapting code.**

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| Microsoft Learn (.NET docs, dotnet/docs repo) | CC BY 4.0 (docs); MIT (code samples) | Yes | Yes | Yes (MIT) | "Microsoft Learn, CC BY 4.0" plus URL; MIT notice for code |
| Microsoft Learn (PowerShell-Docs, Windows Server docs) | CC BY 4.0 (docs); MIT (code), to be verified per repo | Yes | Yes | Yes, if MIT confirmed | As above |
| Microsoft .NET Blog, Tech Community blogs | Microsoft Terms of Use (all rights reserved) | Brief quotes only | Yes | No (only short snippets as fair use) | Title, author, URL, date |
| support.microsoft.com, Microsoft Download Center | Microsoft Terms of Use | Brief quotes | Yes | No | URL and date |
| NuGet Gallery, PowerShell Gallery (metadata) | Gallery terms; packages have their own licences (System.CommandLine MIT) | Facts and short quotes | Yes | Per package licence | URL |
| pester.dev / pester/Pester | Apache-2.0 (Pester project)\[1\] | Yes | Yes | Yes | Keep NOTICE and attribution |
| PowerShell/SecretManagement GitHub | MIT | Yes | Yes | Yes | MIT notice |
| Wikipedia (secondary) | CC BY-SA 4.0 | Brief quotes | Yes | No (share-alike is incompatible with Apache-2.0 for adapted text) | Article and URL |
| InfoQ, Visual Studio Magazine, i-programmer, DevClass, Techzine, BleepingComputer, 4sysops, windowsforum, endoflife.ai, Lansweeper, other blogs (secondary) | Publisher copyright | Brief quotes | Yes | No | Publication, title, URL, date |

## 9. Not found, contested, not covered

**Contested**
- **Latest PowerShell 7.6.x patch:** Wikipedia gives 7.6.7 (13 October 2026); a windowsforum article says endoflife.date lists 7.6.8 (22 October 2026); windowsforum reports 7.6.9 built with .NET SDK 10.0.403.\[32\]\[47\] Check https://github.com/PowerShell/PowerShell/releases before pinning.
- **.NET 10 end date:** Microsoft's blog says "November 2028"; secondary trackers give 14 November 2028, and one secondary source says the announcement gave 10 November 2028.\[5\]\[7\]\[87\] Check the dotnet-core support policy page.
- **.NET 11 end date:** projected November 2028, with 9 November 2028 per one secondary source.\[53\]\[56\] Not yet published by Microsoft.
- **WMIC on Windows Server 2025:** removed from the article's scope; status unclear.

**Not found**
- GitHub Copilot app modernization version number.
- The Microsoft Learn primary page for KB5073381 (RC4) was not fetched; the RC4 dates rest on a Microsoft Tech Community post and consistent secondary sources.
- The PowerShell lifecycle page on Microsoft Learn could not be fetched directly; its table is quoted through secondary sources that agree with each other.

**Not covered (search budget exhausted).** These remain open for a follow-up run:
- Q2: Directory.Build.props and CPM, lock files and `RestoreLockedMode`, analyzer properties, `dotnet format`, NuGet Audit, NativeAOT and trimming per app model, logging source generators, STJ source generation, IHttpClientFactory and Http.Resilience. The 2026-09 standard belief is unverified.
- Q3: WinForms and WPF dark mode and high DPI, MAUI support status, CsWin32 and LibraryImport, MSIX and unpackaged toast notifications.
- Q4: Windows PowerShell 5.1 differences, `Get-WmiObject`, `Get-EventLog` and `Write-EventLog` absent in 7, PSResourceGet as the replacement for PowerShellGet (only indirectly supported), side-by-side install, coding practice.
- Q5: LDAP signing and channel binding, hotpatching, Windows LAPS schema and cmdlets, Windows 10 end of support and ESU.
- Q6 (AD best practice, gMSA and dMSA, AD CS ESC1–ESC16, MS16-072), Q7 (security baselines, CIS versions), Q8 (.NET Framework 4.8.1, WebForms, WCF, Remoting, VB.NET), Q9 (AI C# mistakes beyond those above), Q10 (ANSI and `$PSStyle.OutputRendering`, hidden Unicode, Authenticode, `Get-FileHash` limits, NuGet signing).

## Sources

1. [Pester 5.7.1](https://www.powershellgallery.com/packages/pester/5.7.1)
2. [Windows Management Instrumentation Command-line (WMIC) removal from Windows](https://support.microsoft.com/en-us/topic/windows-management-instrumentation-command-line-wmic-removal-from-windows-e9e83c7f-4992-477f-ba1d-96f694b8665d)
3. [Disable RC4 & Enforce AES in Active Directory (2026 Kerberos Guide)](https://forestall.io/resources/blog/disabling-rc4-enforcing-aes-step-by-step-guide)
4. [PowerShell 7.4 LTS and 7.5 reach end of support November 10, 2026: move automation to PowerShell 7.6 LTS](https://update.dsesecurity.com/updates/powershell-7-4-lts-7-5-end-of-support-november-10-2026-upgrade-7-6/)
5. [.NET 8 and .NET 9 will reach End of Support on November 10, 2026 - .NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/)
6. [Microsoft Warns Windows Server 2016 Support Ends Soon](https://windowsreport.com/microsoft-warns-windows-server-2016-support-ends-soon/)
7. [.NET 8 and 9 End of Support: 10 November 2026](https://www.osseva.io/blog/dotnet-8-end-of-support)
8. [.NET 11 Release Candidate 2 Updates F#](https://www.i-programmer.info/news/89-net/19225-net-11-release-candidate-2-updates-f.html)
9. [.NET 11 RC1 Gets Go-Live Support Ahead of November Launch -- Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/09/14/net-11-rc1-gets-go-live-support-ahead-of-november-launch.aspx)
10. [Microsoft Releases .NET 11 RC1 with Go-Live Support, C# 15 and F# 11 as Default Language Versions - InfoQ](https://www.infoq.com/news/2026/09/dotnet-11-rc-1-release/)
11. [Microsoft Ships .NET 11 RC2, C# 15, dotnetup Tool \[2026\]](https://tech-insider.org/microsoft-dotnet-11-rc2-dotnetup-tool-2026/)
12. [docs/docs/csharp/whats-new/csharp-14.md at main · dotnet/docs · GitHub](https://github.com/dotnet/docs/blob/main/docs/csharp/whats-new/csharp-14.md)
13. [What's new in C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)
14. [NuGet Gallery](https://www.nuget.org/packages/System.CommandLine/2.0.0-beta2.21617.1)
15. [NuGet Gallery](https://www.nuget.org/packages/xunit.v3)
16. [NuGet Gallery](https://www.nuget.org/packages/MSTest)
17. [.NET Upgrade Assistant Overview - .NET Core](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview)
18. [Copilot replaces .NET upgrade tool: developers complain - Techzine Global](https://www.techzine.eu/news/devops/136571/copilot-replaces-net-upgrade-tool-developers-complain/)
19. [Copilot .Net modernization tool a 'huge downgrade,' devs say](https://www.devclass.com/development/2025/11/20/copilot-net-modernization-tool-a-huge-downgrade-devs-say-and-no-longer-free/1725515)
20. [PowerShell 7.4 Support Ends November 10, 2026: Move to 7.6 LTS](https://windowsforum.com/news/powershell-7-4-support-ends-november-10-2026-move-to-7-6-lts.445667/)
21. [PowerShell Gallery](https://www.powershellgallery.com/packages/Pester/6.0.0-alpha4)
22. [PowerShell Gallery](https://www.powershellgallery.com/packages/Microsoft.PowerShell.PSResourceGet/1.0.1)
23. [GitHub - PowerShell/SecretManagement: PowerShell module to consistent usage of secrets through different extension vaults · GitHub](https://github.com/PowerShell/SecretManagement)
24. [PowerShell Gallery](https://www.powershellgallery.com/packages/PSScriptAnalyzer/1.25.0)
25. [Kerberos and the End of RC4: Protocol Hardening and Preparing for CVE‑2026‑20833](https://techcommunity.microsoft.com/discussions/microsoft-security/kerberos-and-the-end-of-rc4-protocol-hardening-and-preparing-for-cve%E2%80%912026%E2%80%9120833/4502262)
26. [Retiring NTLM: Frequently asked questions - Windows IT Pro Blog](https://techcommunity.microsoft.com/blog/windows-itpro-blog/retiring-ntlm-frequently-asked-questions/4550522)
27. [Advancing Windows security: Disabling NTLM by default - M365 Admin](https://m365admin.handsontek.net/advancing-windows-security-disabling-ntlm-default/)
28. [Control SMB signing behavior](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing)
29. [Windows Server Release History: 2016 to 2025, Security and Support](https://safeguard.sh/resources/blog/windows-server-release-history-2016-to-2025-security-changes-and-support-dates)
30. [Preparing Your VBA Projects for VBScript Deprecation in Windows](https://sumproduct.com/news/preparing-your-vba-projects-for-vbscript-deprecation-in-windows/)
31. [NuGet Gallery](https://www.nuget.org/packages/xunit.v3/4.0.0)
32. [PowerShell 7.6.9 LTS Released: .NET SDK 10.0.403 Update, Downloads and Support Deadlines](https://windowsforum.com/news/powershell-7-6-9-lts-released-net-sdk-10-0-403-update-downloads-and-support-deadlines.449975/)
33. [PowerShell 7.6: What’s New for Sysadmins in 2026](https://www.refontelearning.com/blog/powershell-7-6-cross-platform-automation)
34. [Migrating from Pester v5 to v6](https://pester.dev/docs/migrations/v5-to-v6)
35. [PowerShell End of Life - Lansweeper](https://www.lansweeper.com/blog/eol/powershell-end-of-life/)
36. [Manage NTLMv1 changes and prevent network authentication issues in Windows](https://support.microsoft.com/en-us/topic/upcoming-changes-to-ntlmv1-in-windows-11-version-24h2-and-windows-server-2025-c0554217-cdbc-420f-b47c-e02b2db49b2e)
37. [Manage changes to NTLMv1 and prevent network issues in Windows 11 and Windows Server 2025](https://www.elevenforum.com/t/manage-changes-to-ntlmv1-and-prevent-network-issues-in-windows-11-and-windows-server-2025.50172/)
38. [Retire NTLM without breaking the network: audit guide](https://hard2bit.com/en/blog/disable-ntlm-without-breaking-network-audit-kerberos-migration/)
39. [RC4 Deprecation in Active Directory: Timeline and Phases](https://www.mgworkplace.it/en/field-guides/rc4-deprecation-active-directory)
40. [RC4 Retirement and NTLM Phase Out in 2026](https://www.hbs.net/blog/rc4-ntlm-retirement)
41. [PowerShell Gallery](https://www.powershellgallery.com/packages/Microsoft.PowerShell.SecretStore/0.5.3-preview3)
42. [PowerShell Gallery](https://www.powershellgallery.com/packages/Microsoft.PowerShell.SecretManagement/0.5.2-preview3)
43. [Announcing .NET 11 Release Candidate 1 - .NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-11-rc-1/)
44. [.NET 11 Release Candidate 2: Go-Live License and Updates across Libraries, F#, MAUI, and WinForms - InfoQ](https://www.infoq.com/news/2026/10/dotnet-11-rc-2/)
45. [Upgrade .NET apps overview - .NET Core](https://learn.microsoft.com/en-us/dotnet/core/porting/)
46. [PowerShell 7.4.21 Released: Config Fixes, Update Steps and 7.6 LTS Migration](https://windowsforum.com/news/powershell-7-4-21-released-config-fixes-update-steps-and-7-6-lts-migration.448185/)
47. [PowerShell](https://en.wikipedia.org/wiki/PowerShell)
48. mcp\_\_Microsoft\_Learn\_\_microsoft\_docs\_fetch
49. [What's New in PowerShell-Docs for 2026 - PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/community/2026-updates?view=powershell-7.6)
50. [Windows Server 2019](https://en.wikipedia.org/wiki/Windows_Server_2019)
51. [.NET 8 End of Life (EOL) and End of Support: November 10, 2026](https://endoflife.ai/article-dotnet-eol-2026)
52. [.NET End-of-Life (EOL) Dates: What You Need to Know](https://www.herodevs.com/blog-posts/net-end-of-life-eol-dates-what-you-need-to-know)
53. [.NET](https://en.wikipedia.org/wiki/.NET)
54. [Announcing .NET 11 Release Candidate 2](https://daily.dev/posts/announcing-net-11-release-candidate-2-r6atsrapw)
55. [What's New in .NET 11: An Overview of C# 15, EF Core 11, ASP.NET Core, and Performance](https://www.fast-report.com/blogs/overview-net-11)
56. [.NET 11 — What's New: Features, Performance & Migration](https://redcoretechnologies.com/pages/dotnet-11.html)
57. [NuGet Gallery](https://www.nuget.org/packages/System.CommandLine/2.0.0)
58. [Windows App SDK release channels - Windows apps](https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/release-channels)
59. [Latest Windows App SDK downloads - Windows apps](https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads)
60. [Windows App SDK 2.0 (2.0.1) 🎉 · microsoft/WindowsAppSDK · Discussion #6438 · GitHub](https://github.com/microsoft/WindowsAppSDK/discussions/6438)
61. [Windows App SDK 2.2.0 · microsoft/WindowsAppSDK · Discussion #6554 · GitHub](https://github.com/microsoft/WindowsAppSDK/discussions/6554)
62. [PowerShell 7.6: LTS Upgrade Guide for Admins](https://www.starwindsoftware.com/blog/powershell-7-6-upgrade-guide/)
63. [PowerShell is fun :)PowerShell v7.6 LTS Release and why it matters](https://powershellisfun.com/2026/03/20/powershell-v7-6-lts-release-and-why-it-matters/)
64. [PowerShell 7.6: new features, install, and upgrade](https://4sysops.com/archives/powershell-76-new-features-install-and-upgrade/)
65. [PowerShell 7.6.8 Now Available: Update Notification Dropped, Crash Fixed](https://www.ntcompatible.com/story/powershell-768-now-available-update-notification-dropped-crash-fixed)
66. [Releases · pester/Pester · GitHub](https://github.com/pester/Pester/releases)
67. [Migrating from Pester 5 to 6 - I dont like AI](https://www.idontlikeai.dev/migrating-from-pester-5-to-6/)
68. [Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3)
69. [What's new in Windows 11, version 24H2 for IT pros](https://learn.microsoft.com/en-us/windows/whats-new/whats-new-windows-11-version-24h2)
70. [NTLM Deprecation: Microsoft's Phaseout Timeline, Risks & Migration Guide](https://powerdmarc.com/ntlm-deprecation-microsoft-phaseout/)
71. [Microsoft Moves Closer to Disabling NTLM - SecurityWeek](https://www.securityweek.com/microsoft-moves-closer-to-disabling-ntlm/)
72. [Download Local Administrator Password Solution (LAPS) from Official Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=46899)
73. [laps overview](https://learn.microsoft.com/windows-server/identity/laps/laps-overview)
74. [learn.microsoft.com](https://learn.microsoft.com/en-au/windows-server/identity/laps/laps)
75. [Windows LAPS Overview: Manage Admin Passwords](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview)
76. [Windows LAPS on Windows Server 2025: AD Setup](https://rafftechnologies.com/windows-server/windows-laps-windows-server-2025)
77. [Windows Server 2025 LAPS](https://blog.pdan.dev/posts/windows-server-laps/)
78. [Windows Server 2016 End of Life: Jan 2027 + ESU](https://rafftechnologies.com/windows-server/windows-server-2016-end-of-life)
79. [Windows Server Update Services (WSUS) deprecation - Windows IT Pro Blog](https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-server-update-services-wsus-deprecation/4250436)
80. [Beyond WSUS: How to Build a Modern Windows Update Management System (2026)](https://inventivehq.com/blog/beyond-wsus-how-to-build-a-modern-windows-update-management-system)
81. [What Is WSUS? Deprecation and Alternatives - Flamingo](https://www.flamingo.run/blog/what-is-wsus)
82. [WSUS Replacement with Azure Update Manager](https://o365hq.com/services/wsus-replacement-azure-update-manager)
83. [January 2027 Microsoft End of Support: Windows Server 2016 and More](https://endoflife.ai/article-january-2027-microsoft-end-of-support)
84. [Windows Server End of Life Dates: 2016 Ends January 12, 2027](https://endoflife.ai/article-windows-server-eol)
85. [.NET 8 End of Life: Support Ends 10 November 2026](https://www.osseva.io/eol/dotnet-8)
86. [PowerShell is fun :)Windows 11 25H2’s removal of WMIC and the PowerShell alternative](https://powershellisfun.com/2025/10/08/windows-11-25h2s-removal-of-wmic-and-the-powershell-alternative/)
87. [.NET Release and Support Timeline - STS and LTS Releases, the Move to Two-Year STS Support, and End-of-Support Dates](https://hidekazu-konishi.com/entry/dotnet_release_and_support_timeline.html)
