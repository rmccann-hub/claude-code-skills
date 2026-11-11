# Windows Server administration

Read this for running or auditing Windows Server 2016 to 2025: supported versions, Active
Directory admin tiers, LAPS, Group Policy changes, DNS and DHCP, AD CS, shares and SMB, patching
after WSUS, hotpatching, baselines, Credential Guard, the firewall, Remoting and JEA.

Writing the scripts is `coding`'s `powershell-scripts`, and credentials and input in them
`powershell-security`. Network firewalls and segmentation are `networking-security`. Event logs
and crash dumps belong to the planned `log-analysis`.

## Rules

1. **Run only supported versions, and plan each exit a year ahead.** Windows Server 2016 gets
   no updates after 2027-01-12 (fact `win-server-support`).
2. **Give each admin a separate account per tier, and keep tier 0 credentials off lower
   tiers.** Domain admins sign in only to domain controllers and their own admin hosts (fact
   `win-access-model`).
3. **Put admin accounts in Protected Users after testing; never service or computer accounts**
   (fact `win-protected-users`).
4. **Manage every local Administrator password with Windows LAPS,** not the legacy MSI (fact
   `win-laps`).
5. **Change Group Policy like code:** back up, make a new GPO, link it to a pilot OU, read the
   result with `gpresult`, then widen the link.
6. **Run DNS on at least two domain controllers and DHCP as a failover pair,** and point domain
   members at internal DNS only.
7. **Treat AD CS as tier 0, and audit its templates and web enrollment** (fact `win-adcs`).
8. **Grant file access to groups through both share and NTFS permissions;** keep SMB signing on
   and SMBv1 off (facts `win-share-ntfs`, `win-smb`).
9. **Choose and record a supported update path for servers** (facts `win-wsus`,
   `win-update-policies`, `win-hotpatch`).
10. **Harden from Microsoft's baseline,** with Credential Guard, the firewall on in every
    profile, and nothing left depending on RC4 or NTLMv1 (facts `win-baselines`,
    `win-credential-guard`, `win-kerberos-rc4`, `win-ntlmv1`).
11. **Administer with PowerShell Remoting, and delegate with JEA** rather than adding people to
    Administrators (fact `win-jea`).

### Group Policy changes

- Back up every GPO first (`Backup-GPO -All -Path <share>`), to a share off the domain
  controllers. Put each change in a new GPO, never the two default policies.
- Link it to a pilot OU holding each role. There, run `gpupdate /force`, then
  `gpresult /scope computer /h <file>`, and confirm the GPO applied and nothing else moved.
- Widen the link in stages; keep the old GPO, unlinked, until a full cycle has passed.

### Read-only checks

<!-- example: unchecked, pwsh isn't installed where this was written; each cmdlet and parameter was checked on its Microsoft Learn page -->
```powershell
Get-SmbServerConfiguration | Format-List EnableSMB1Protocol, RequireSecuritySignature
Get-SmbClientConfiguration | Format-List RequireSecuritySignature
Get-NetFirewallProfile | Format-Table Name, Enabled
gpresult /scope computer /h "$env:TEMP\rsop.html" /f
```

A fix they lead to runs first with `-WhatIf`, or after a backup where a cmdlet lacks it.

## Mistakes

- **Turning off SMB signing, or SMBv1 back on, to reach an old NAS.** Microsoft says not to
  (fact `win-smb`). Enable signing on the device, or replace it.
- **Turning RC4 back on for the domain because one service fails.** Since July 2026 enforcement
  is the only mode (fact `win-kerberos-rc4`). Set that account's encryption types explicitly,
  then move it to AES.
- **Adding a service account or computer to Protected Users,** or every admin at once. It locks
  them out (fact `win-protected-users`). Add one admin, test, then the rest.
- **Recommending Windows Update for Business for servers.** It's now Windows Update client
  policies, for Windows 10 and 11 (fact `win-update-policies`).
- **Installing the legacy LAPS MSI on a new server.** Use Windows LAPS; its emulation mode reads
  the old policy during migration (fact `win-laps`).
- **A template with "Supply in the request", client authentication and enrollment for Domain
  Users.** Any user can then sign in as a domain admin (fact `win-adcs`).
- **Linking an untested GPO at the domain root,** or editing the Default Domain Policy in place.

## Audit

Severity uses the standard's status words.

| Check | Look for | Severity | Fix |
|---|---|---|---|
| Out-of-support servers | `Get-ADComputer -Filter * -Properties OperatingSystem` against the dates | `BLOCKER` past the date, `GAP` within a year | Upgrade or replace, with a dated plan |
| Domain admins on lower tiers | Domain Admins sign-ins on member servers and workstations | `BLOCKER` | An account per tier; deny lower-tier sign-in by Group Policy |
| Unmanaged local Administrator passwords | Computers with no Windows LAPS password in AD | `GAP` | A Windows LAPS policy per OU |
| Service accounts in Protected Users | Members with an SPN, or computer objects | `DRIFT` | Remove them; use a group managed service account |
| Dangerous certificate templates | Defender for Identity's AD CS assessments, or each template's EKUs, subject and ACL | `BLOCKER` for ESC1 or ESC4 | Turn off "Supply in the request", narrow the ACL, or unpublish |
| SMB signing off or SMBv1 on | The checks above, on every server | `DRIFT` | Signing on; SMBv1 removed |
| No recorded update path, or WSUS on WID | Each server's update source; the WSUS database | `GAP` | Record the path; plan off WID (fact `win-wsus`) |
| No baseline, or drift from it | Policy Analyzer, or OSConfig on 2025 | `GAP` | The baseline for each role (fact `win-baselines`) |
| Firewall off in a profile | `Get-NetFirewallProfile` | `DRIFT` | On by Group Policy, with rules per role |
| One DNS server, or DHCP without failover | DNS servers in scope options; `Get-DhcpServerv4Failover` | `GAP` | A second DNS server; a failover partner |

## Why

### Supported versions and updates

An unsupported server gets no security fixes, and upgrades take months, hence a year's notice. WSUS
works but gets no new features, and the database it often runs on is deprecated too (fact
`win-wsus`); Microsoft points servers to Azure Update Manager, and Configuration Manager is
unaffected. Hotpatching on 2025 outside Azure needs Azure Arc, and the quarterly baseline still
restarts (fact `win-hotpatch`). **Cost:** cloud tools need outbound access and a subscription.
**Choose differently** on an air-gapped site, where WSUS or Configuration Manager fits; record why,
and revisit yearly.

### Tiers, Protected Users and LAPS

An attacker on a machine can take the credentials used there, so a domain admin who signs in to
a workstation hands over the domain. Tiers break that path. Protected Users stops NTLM, RC4 and
delegation for its members, which is why a service account breaks there. LAPS gives each
machine its own password, so one stolen hash doesn't open them all. **Cost:** more accounts and
friction. **Choose differently:** a small site with no domain keeps LAPS and separate accounts,
without tiers.

### Group Policy, DNS and DHCP

A GPO at the domain root reaches every machine at its next refresh, so a mistake there is an
outage everywhere; a backup makes it reversible, and a pilot shows what applied. An urgent
security setting goes wide at once, still with a backup and a record. Active Directory finds
domain controllers through DNS, so one DNS server is one point of failure for every sign-in.
Both are this repository's practice.

### AD CS and SMB

A certificate that authenticates is as good as a password, and AD CS issues one to whoever a
template allows (fact `win-adcs`). SMB signing stops relay and tampering. **Cost:** old NAS
devices and printers may stop working; isolate and replace them, never turn signing off.

### Baselines, Credential Guard and JEA

A baseline's settings come tested and with reasons; a hand-made list drifts. Credential Guard is on
by default on supported 2025 members, not domain controllers (fact `win-credential-guard`). The host
firewall limits what a compromised neighbor reaches. JEA lets a help desk restart a service without
being an administrator, and Remoting avoids an interactive sign-in on the server. **Cost:** a
baseline breaks some legacy apps, so test per role, and JEA's role files need upkeep. **Choose
differently:** CIS benchmarks where an auditor requires them.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `win-server-support` | Mainstream and extended ends: 2025, 2029-11-13 and 2034-11-14; 2022, past and 2031-10-14; extended ends: 2019, 2029-01-09; 2016, 2027-01-12 | [Release information](https://learn.microsoft.com/en-us/windows-server/get-started/windows-server-release-info) | "Standard 2024-11-01 2029-11-13 2034-11-14" and "Standard 2021-08-18 End of updates 2031-10-14" and "Standard 2018-11-13 End of updates 2029-01-09" and "Standard 2016-08-02 End of updates 2027-01-12" | 2026-11-11 | 2027-02-11 |
| `win-wsus` | WSUS is deprecated but in 2025; servers go to Azure Update Manager; WID is deprecated | [WSUS deprecation](https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-server-update-services-wsus-deprecation/4250436); [Deprecated features](https://learn.microsoft.com/en-us/windows-server/get-started/removed-deprecated-features-windows-server) | "we are no longer investing in new capabilities" and "the WSUS role remains available in Windows Server 2025" and "Azure Update Manager for server update management" and "WID will be removed from Windows in a future release." | 2026-11-11 | 2027-02-11 |
| `win-update-policies` | Windows Update for Business is now client policies, for Windows 10 and 11 | [Client policies](https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb) | "formerly known as Windows Update for Business" and "editions of Windows 10 and" | 2026-11-11 | 2027-02-11 |
| `win-hotpatch` | Hotpatch for 2025 via Azure Arc at no extra cost; quarterly baselines restart | [Hotpatch](https://learn.microsoft.com/en-us/windows-server/get-started/hotpatch); [Release information](https://learn.microsoft.com/en-us/windows-server/get-started/windows-server-release-info) | "Azure Arc-enabled Hotpatch for Windows Server 2025 is now available at no extra cost." and "A restart is required to install that baseline update." | 2026-11-11 | 2027-02-11 |
| `win-smb` | 2025 requires outbound signing only; never disable signing to fix failures; no SMBv1 on 2019+ | [SMB signing](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing); [SMBv1](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3) | "Windows Server 2025 requires outbound SMB signing only." and "Don't disable SMB protocol versions or SMB signing to work around these connection failures." and "isn't installed by default in any edition of Windows 11 or Windows Server 2019 and later" | 2026-11-11 | 2027-05-11 |
| `win-share-ntfs` | Share and NTFS permissions must both allow access | [SMB Access Denied](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/access-denied-access-smb-file-share) | "Verify both Share and NTFS (Security) permissions grant the user the required access" | 2026-11-11 | 2027-05-11 |
| `win-laps` | Windows LAPS on 2019 from its April 2023 update; emulates legacy LAPS | [Windows LAPS](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview) | "Windows Server 2019 - April 11 2023 Update and later." and "legacy Microsoft LAPS emulation mode" | 2026-11-11 | 2027-05-11 |
| `win-protected-users` | No service or computer accounts; test first, or admins get locked out | [Protected Users](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group) | "Never add accounts for services and computers to the Protected Users group." and "accidentally lock out their accounts" | 2026-11-11 | 2027-05-11 |
| `win-access-model` | The enterprise access model extends the AD tier model | [Access model](https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model) | "The enterprise access model builds on the AD tier model" | 2026-11-11 | 2027-05-11 |
| `win-adcs` | ESC1, ESC4 and ESC8 | [AD CS assessments](https://learn.microsoft.com/en-us/defender-for-identity/security-posture-assessments/certificates) | "setting is one of the most common misconfigurations" and "an adversary can introduce a template misconfiguration" and "vulnerable to NTLM relay attacks (ESC8)" | 2026-11-11 | 2027-05-11 |
| `win-credential-guard` | On by default on 2025 members, not DCs | [Credential Guard](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/) | "enabled by default on domain-joined, non-DC systems that meet hardware requirements" | 2026-11-11 | 2027-05-11 |
| `win-kerberos-rc4` | Kerberos RC4 is deprecated; since July 2026 enforcement is the only mode | [Deprecated features](https://learn.microsoft.com/en-us/windows-server/get-started/removed-deprecated-features-windows-server); [Message center](https://learn.microsoft.com/en-us/windows/release-health/windows-message-center) | "RC4 usage in the Kerberos authentication protocol is deprecated." and "Enforcement mode is the only supported configuration" | 2026-11-11 | 2027-02-11 |
| `win-ntlmv1` | NTLMv1 is removed in 2025 | [Windows 11 24H2](https://learn.microsoft.com/en-us/windows/whats-new/whats-new-windows-11-version-24h2) | "NTLMv1 is removed starting in Windows 11, version 24H2 and Windows Server 2025." | 2026-11-11 | 2027-05-11 |
| `win-baselines` | Baselines ship in the Security Compliance Toolkit; on 2025 OSConfig holds them | [Baselines](https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines); [OSConfig](https://learn.microsoft.com/en-us/windows-server/security/osconfig/osconfig-how-to-configure-security-baselines) | "Security Compliance Toolkit (SCT)" and "OSConfig automatically protects your security baseline settings from drift" | 2026-11-11 | 2027-05-11 |
| `win-jea` | JEA runs as a virtual account or gMSA, with transcripts | [JEA](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/overview) | "using virtual accounts or group-managed service accounts" and "transcripts and logs" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Windows Server docs](https://learn.microsoft.com/en-us/windows-server/) | Dates, updates, SMB, LAPS, Protected Users, OSConfig | CC BY 4.0: short quotes, attributed |
| [PowerShell docs](https://learn.microsoft.com/en-us/powershell/) | JEA, and the cmdlets in the checks | Docs CC BY 4.0, code MIT: short quotes, attributed |
| Other Microsoft Learn pages | Client policies, Credential Guard, baselines, access model, AD CS, shares, RC4 | License not confirmed: our own words, short quotes |
| [Windows IT Pro Blog](https://techcommunity.microsoft.com/blog/windows-itpro-blog/windows-server-update-services-wsus-deprecation/4250436) | WSUS deprecation | All rights reserved: our own words, short quotes |
