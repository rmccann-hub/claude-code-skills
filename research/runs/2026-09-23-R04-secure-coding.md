# Verification: R04 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| OWASP Top 10:2025 is current; A10 is Mishandling of Exceptional Conditions | verified | [OWASP Top 10:2025](https://owasp.org/Top10/2025/) |
| NIST SP 800-63B-4: single-factor passwords at least 15 characters; composition rules "SHALL NOT be imposed"; no periodic change | verified | [SP 800-63B-4, authenticators](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R04 · FORM: research-result v1
Save as: R04-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R04: Secure coding, input handling, threat modelling, authentication and cryptography

Most of the "What we believe" items are right in substance, but four need correcting before they go into the facts files:

1. The 1 January 2026 memory-safety roadmap date comes from the first version of CISA/FBI "Product Security Bad Practices", not from the Secure by Design pledge, and version 2 changed it to "by the end of 2025".
2. NIST IR 8547 is still an initial public draft.
3. RFC 8725 is about to be obsoleted by rfc8725bis, which is past IETF Last Call.
4. Hybrid ML-KEM TLS is now the default in Java too (JDK 27), not only in OpenSSL 3.5 and Go. On Windows it is available but not switched on automatically.

Read date for every source without its own date: 23 September 2026.

## TL;DR

- **Standards baseline for today:**
  - OWASP Top 10:2025 (A01 Broken Access Control to A10 Mishandling of Exceptional Conditions).
  - OWASP ASVS 5.0.0 (May 2025; 17 chapters, levels L1 to L3).
  - 2025 CWE Top 25 (released 11 December 2025; XSS, SQL injection and CSRF are the top three).
  - NIST SP 800-63B-4 (final July 2025).
- **Authentication and passwords:**
  - Passwords: at least 15 characters when the password is the only factor, 8 when it is part of MFA. No composition rules, no periodic rotation, and screen new passwords against a blocklist.
  - Hash with Argon2id at m=19 MiB, t=2, p=1 or stronger. Fall back to scrypt, bcrypt or PBKDF2 only for the reasons OWASP gives.
  - OAuth: follow RFC 9700 and the OAuth 2.1 draft (now -16): PKCE, exact redirect matching, no implicit or password grants.
- **Cryptography:** turn on hybrid X25519MLKEM768 TLS through your platform's defaults, meaning OpenSSL 3.5+, Go 1.24+, JDK 27, or Windows Schannel after the July 2026 patches (opt-in). Start a cryptographic inventory now, planning to the proposed 2030 (deprecate) and 2035 (disallow) dates in draft NIST IR 8547.

## 1. Summary

- OWASP Top 10:2025 is the current edition. In order: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions.
- Changes from the 2021 list:
  - SSRF was folded into A01.
  - "Vulnerable and Outdated Components" widened into A03 Software Supply Chain Failures.
  - A10 is a new category.
  - Security Misconfiguration moved up from #5 to #2.
- OWASP ASVS 5.0.0 (May 2025) has 345 requirements in 17 chapters (V1 to V17) and three levels (L1 to L3); OWASP's own ASVS repository says 70 of the 345 are L1, compared with 128 L1 out of 278 in 4.0.3. Its first dedicated chapters for OAuth/OIDC (V10) and self-contained tokens (V9) matter for any authentication skill.
- The 2025 CWE Top 25 was drawn from 39,080 CVEs. XSS (CWE-79) is #1 at score 60.38. Missing Authorization (CWE-862) rose five places to #4. Six entries are new, including three buffer-overflow CWEs (120, 121, 122).
- NIST SP 800-63B-4 was finalized in July 2025 (CSRC history: 07/31/25) and fully replaced SP 800-63B on 1 August 2025. Its rules are shall-level: minimum 15 characters when a password is the only factor, minimum 8 inside MFA, and no other composition requirements.
- OWASP password storage settings: Argon2id m=19456 (19 MiB), t=2, p=1 as a minimum. Fallbacks: scrypt N=2^17, r=8, p=1; bcrypt cost ≥10 with a 72-byte input limit; PBKDF2-HMAC-SHA-256 with ≥600,000 iterations if FIPS-140 is required. A pepper is optional defence in depth.
- RFC 9700 (BCP 240, January 2025) is the OAuth 2.0 security BCP. OAuth 2.1 is still an Internet-Draft; the latest is draft-ietf-oauth-v2-1-16, dated 3 September 2026. It requires PKCE for every authorization-code client and drops the implicit and password grants.
- The JWT BCP is changing. draft-ietf-oauth-rfc8725bis went to IETF Last Call on 22 June 2026 (-06), and -07 is dated 19 July 2026. Once approved it will obsolete RFC 8725.
- Post-quantum standards:
  - FIPS 203/204/205 were published on 13 August 2024.
  - HQC was selected on 11 March 2025 as a backup to ML-KEM that uses different mathematics. It is not a replacement.
  - FALCON will become FIPS 206, which is still in development.
- NIST IR 8547 is still an initial public draft (12 November 2024). It proposes that quantum-vulnerable public-key algorithms be deprecated after 2030 and disallowed after 2035.
- Hybrid X25519MLKEM768 is on by default in OpenSSL 3.5, Go 1.24+ and JDK 27 (JEP 527). On Windows, Schannel supports it after the July 2026 update, but it does not switch on automatically.
- The HTML Sanitizer API (`Element.setHTML()`) shipped in Firefox 148 (24 February 2026) and Chrome 146, but it is not Baseline. Feature-detect it and fall back to DOMPurify. Researchers have already published two bypasses for Chrome's implementation.
- Memory safety:
  - CISA/FBI Bad Practices v2 (January 2025) asks manufacturers to publish a memory-safety roadmap "by the end of 2025". It is explicitly non-binding.
  - The June 2025 CISA/NSA guide recommends writing new code in memory-safe languages and migrating the rest step by step.
- AI-generated code:
  - Veracode's 2025 study found security flaws in 45% of AI-generated code samples.
  - Spracklen et al. (USENIX Security 2025) found that at least 5.2% of packages suggested by commercial models, and 21.7% by open-source models, did not exist. That is 205,474 unique hallucinated names, which attackers can register ("slopsquatting").

## 2. Corrections

| # | What we believed | Status | Correct fact | Source |
|---|---|---|---|---|
| C1 | OWASP Top 10:2025 published in late 2025, replacing 2021 | Confirmed, with nuance | The release candidate was announced on 6 November 2025 at Global AppSec (secondary: Fastly). The owasp.org project page now calls 2025 "the most current released version". I did not find the exact date of the final release. | https://owasp.org/projects/top-ten ; https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know |
| C2 | ASVS 5.0 released May 2025 | Confirmed | 5.0.0 is "dated May 2025" and was released at Global AppSec EU Barcelona. The next target is patch release 5.0.1. | https://github.com/OWASP/ASVS |
| C3 | MITRE and CISA published a 2025 CWE Top 25 | Confirmed, with detail | It was released on 11 December 2025 by CISA together with HSSEDI, which MITRE operates. | https://www.cisa.gov/news-events/alerts/2025/12/11/2025-cwe-top-25-most-dangerous-software-weaknesses |
| C4 | SP 800-63B-4 finalized in 2025 | Confirmed, more precise | It is dated July 2025 (CSRC history "07/31/25: SP 800-63B-4 (Final)"). SP 800-63B was withdrawn on 1 August 2025. | https://csrc.nist.gov/pubs/sp/800/63/b/4/final |
| C5 | OWASP recommends Argon2id first, with minimum parameters | Confirmed | Argon2id: 19 MiB, 2 iterations, parallelism 1. The scrypt minimum is now N=2^17; older copies of the cheat sheet say 2^16. The PBKDF2 minimum is now 600,000; older copies say 310,000. | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| C6 | RFC 9700 published January 2025 | Confirmed | BCP 240; it updates RFCs 6749, 6750 and 6819. | https://datatracker.ietf.org/doc/rfc9700/ |
| C7 | OAuth 2.1 still an Internet-Draft; requires PKCE for all clients | Confirmed, but reword | The latest is -16 (3 September 2026, expires 7 March 2027). Precise wording: PKCE is required for "all OAuth clients using the authorization code flow". | https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ ; https://oauth.net/2.1/ |
| C8 | RFC 8725 is the JWT BCP | Out of date soon | RFC 8725 is still the BCP, but draft-ietf-oauth-rfc8725bis (-07, 19 July 2026) "obsoletes" it if approved. IETF Last Call on -06 was announced on 22 June 2026. | https://mailarchive.ietf.org/arch/msg/ietf-announce/fnzXydH3VUrw53AJsypi0W_XfFM/ ; https://nic.funet.fi/pub/netinfo/internet-drafts/draft-ietf-oauth-rfc8725bis-07.html |
| C9 | FIPS 203/204/205 August 2024; HQC March 2025 | Confirmed | The FIPS were published on 13 August 2024. HQC was selected on 11 March 2025. | https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization |
| C10 | IR 8547 proposes deprecating by 2030 and disallowing by 2035 | Confirmed, with nuance | The wording is "deprecated after 2030" and "disallowed after 2035", and it is still only an initial public draft (12 November 2024). A secondary source reports it was not finalized as of mid-2026. NIST has said the 2035 disallowance was not meant to cover well-designed hybrids. | https://csrc.nist.gov/pubs/ir/8547/ipd ; https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf ; https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/uHMw8RNGkC8 |
| C11 | Hybrid X25519MLKEM768 on by default in major browsers and in OpenSSL 3.5 | OpenSSL confirmed; browsers not verified here; list is incomplete | OpenSSL 3.5 offers X25519MLKEM768 and X25519 as default keyshares. The same is true of Go 1.24+ and JDK 27. Windows Schannel is opt-in. I did not fetch browser release notes in this run. JEP 527 says X25519MLKEM768 is "what most TLS clients are currently enabling by default". | https://openssl-library.org/news/openssl-3.5-notes/ ; https://go.dev/doc/go1.24 ; https://openjdk.org/jeps/527 |
| C12 | Secure by Design pledge and CISA/NSA guidance asked for memory-safety roadmaps by 1 January 2026 | Wrong in two ways | (a) The date "January 1, 2026" appears in CISA/FBI Product Security Bad Practices **v1** (October 2024), not in the pledge. (b) **v2** (January 2025) changed it to "by the end of 2025" and states it is non-binding. The pledge gives no date; it lists a roadmap only as an example of showing progress "within one year of signing". The June 2025 CISA/NSA guide sets no deadline. | https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-product-security-bad-practices-508c_0.pdf ; https://www.cisa.gov/securebydesign/pledge |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | OWASP Top 10 current edition | 2025 | https://owasp.org/projects/top-ten | "The most current released version is the OWASP Top 10 2025." | read 2026-09-23 |
| F2 | Top 10:2025 list | A01 to A10 as in the Summary | https://owasp.org/Top10/2025/ | "A10:2025 - Mishandling of Exceptional Conditions" | read 2026-09-23 |
| F3 | Top 10:2025 licence | CC BY 3.0 | https://owasp.org/Top10/2025/ | "licensed under a Creative Commons Attribution 3.0 Unported License" | read 2026-09-23 |
| F4 | Top 10:2025 release candidate announced | 6 Nov 2025 (secondary) | https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know | "announced Thursday, November 6, 2025, at the Global Ap[pSec]" | 2025-11 |
| F5 | ASVS latest stable | 5.0.0, May 2025 | https://github.com/OWASP/ASVS | "The latest stable version is version 5.0.0 (dated May 2025)" | read 2026-09-23 |
| F6 | ASVS next release | 5.0.1 patch | https://github.com/OWASP/ASVS | "The next release target will be a patch release, version 5.0.1." | read 2026-09-23 |
| F7 | ASVS 5.0 chapters | V1 Encoding and Sanitization … V17 WebRTC (17) (secondary) | https://cybersigmacs.com/knowledge-center/owasp-asvs/ | "reorganises its requirements into 17 chapters (V1-V17)" | verified 2026-08-11 by source |
| F8 | CWE Top 25 2025 release | 11 Dec 2025, CISA with HSSEDI/MITRE | https://www.cisa.gov/news-events/alerts/2025/12/11/2025-cwe-top-25-most-dangerous-software-weaknesses | "has released the 2025 Common Weakness Enumeration (CWE) Top 25" | 2025-12-11 |
| F9 | CWE Top 25 #1 | CWE-79, score 60.38 | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | "CWE-79 … 60.38" (table row) | read 2026-09-23 |
| F10 | CWE Top 25 dataset | 39,080 CVEs (secondary) | https://www.infosecurity-magazine.com/news/top-25-dangerous-software/ | "compiled from the weaknesses (CWEs) behind 39,080 CVEs" | 2025-12 |
| F11 | SP 800-63B-4 final | July 2025 | https://csrc.nist.gov/pubs/sp/800/63/b/4/final | "07/31/25: SP 800-63B-4 (Final)" | 2025-07-31 |
| F12 | Old SP 800-63B withdrawn | 1 Aug 2025 | https://csrc.nist.gov/pubs/sp/800/63/b/upd2/final | "Withdrawn on August 01, 2025. Superseded by SP 800-63B-4" | 2025-08-01 |
| F13 | Password minimum, single-factor | 15 characters | https://pages.nist.gov/800-63-4/sp800-63b/authenticators | "SHALL require passwords that are used as a single-factor authentication mechanism to be a minimum of 15 characters" | 2025-07 |
| F14 | Password minimum within MFA | 8 characters | same | "SHALL require them to be a minimum of eight characters in length" | 2025-07 |
| F15 | Maximum length to permit | ≥64 | same | "SHOULD permit a maximum password length of at least 64 characters" | 2025-07 |
| F16 | Composition rules | Prohibited | same | "Other composition requirements for passwords SHALL NOT be imposed." | 2025-07 |
| F17 | Blocklist | Required; reason must be given | same | "SHALL require the subscriber to select a different secret and SHALL provide the reason" | 2025-07 |
| F18 | Argon2id minimum | 19 MiB, t=2, p=1 | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | "minimum configuration of 19 MiB of memory, an iteration count of 2" | read 2026-09-23 |
| F19 | scrypt minimum | N=2^17, r=8, p=1 | same | "minimum CPU/memory cost parameter of (2^17), a minimum block size of 8" | read 2026-09-23 |
| F20 | bcrypt | cost ≥10, 72-byte limit | same | "use a work factor of 10 or more and with a password limit of 72 bytes" | read 2026-09-23 |
| F21 | PBKDF2 | ≥600,000, HMAC-SHA-256 | same | "use PBKDF2 with a work factor of 600,000 or more" | read 2026-09-23 |
| F22 | RFC 9700 | BCP 240, Jan 2025 | https://datatracker.ietf.org/doc/rfc9700/ | "it deprecates some modes of operation that are deemed less secure or even insecure" | 2025-01 |
| F23 | OAuth 2.1 latest draft | -16, 3 Sep 2026 | https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ | "Expires: 7 March 2027 … 3 September 2026" | 2026-09-03 |
| F24 | OAuth 2.1 PKCE | Required for auth-code clients | https://oauth.net/2.1/ | "PKCE is required for all OAuth clients using the authorization code flow" | read 2026-09-23 |
| F25 | OAuth 2.1 refresh tokens | Public clients: sender-constrained or rotated | same | "Refresh tokens for public clients must either be sender-constrained or rotated" | read 2026-09-23 |
| F26 | OAuth browser-based apps | RFC 10017 (per oauth.net) | same | "OAuth for Browser-Based Apps (RFC 10017)" | read 2026-09-23 |
| F27 | JWT BCP revision | rfc8725bis-07, 19 Jul 2026 | https://nic.funet.fi/pub/netinfo/internet-drafts/draft-ietf-oauth-rfc8725bis-07.html | "obsoletes the existing JWT BCP specification RFC 8725" | 2026-07-19 |
| F28 | rfc8725bis IETF Last Call | 22 Jun 2026 | https://mailarchive.ietf.org/arch/msg/ietf-announce/fnzXydH3VUrw53AJsypi0W_XfFM/ | "Last Call: <draft-ietf-oauth-rfc8725bis-06.txt>" | 2026-06-22 |
| F29 | FIPS 203/204/205 published | 13 Aug 2024 | https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization | "were published August 13, 2024" | read 2026-09-23 |
| F30 | HQC selected | 11 Mar 2025 | same | "HQC was selected for standardization on March 11, 2025." | 2025-03-11 |
| F31 | FALCON | FIPS 206 in development | same | "will be published in FIPS 206 (in development)" | read 2026-09-23 |
| F32 | IR 8547 status | Initial public draft, 12 Nov 2024 | https://csrc.nist.gov/pubs/ir/8547/ipd | "Date Published: November 12, 2024" | 2024-11-12 |
| F33 | IR 8547 timeline | Deprecated after 2030; disallowed after 2035 | https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf | "Deprecated after 2030 · Disallowed after 2035" | 2024-11 |
| F34 | Hybrids after 2035 | Not intended to be disallowed (NIST on pqc-forum) | https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/uHMw8RNGkC8 | "not intended to apply to hybrid modes that incorporate an approved PQC algorithm" | 2025 |
| F35 | OpenSSL 3.5 default keyshares | X25519MLKEM768 + X25519 | https://openssl-library.org/news/openssl-3.5-notes/ | "The default TLS keyshares have been changed to offer X25519MLKEM768 and and X25519." | 2025-04 |
| F36 | OpenSSL 3.5 release and LTS end | 8 Apr 2025; supported to 8 Apr 2030 (secondary) | https://postquantum.com/security-pqc/openssl-3-5-pqc-default/ | "an LTS (Long Term Stable) release, supported until April 8, 2030" | 2025-04-10 |
| F37 | Go hybrid default | Go 1.24 | https://go.dev/doc/go1.24 | "enabled by default when Config.CurvePreferences is nil" | 2025-02 |
| F38 | Java hybrid default | JDK 27, JEP 527 | https://jdk.java.net/27/release-notes | "only X25519MLKEM768 is placed at the front of the default named groups list" | 2026 |
| F39 | Hybrid TLS groups RFC | RFC 10024, Proposed Standard, Aug 2026 (secondary) | https://www.jvm-weekly.com/p/jdk-27-is-here-jvm-weekly-vol-192 | "the three mechanisms became RFC 10024, a Proposed Standard, in August" | 2026-09 |
| F40 | Windows Schannel hybrid TLS | GA; Server 2025 via KB5099536 (14 Jul 2026) | https://techcommunity.microsoft.com/blog/post-quantum-crypto-tech-blog/windows-tls-1-3-and-post-quantum-crypto-faq/4556389 | "For Windows Server 2025 use the patch from July 14, 2026-KB5099536" | 2026 |
| F41 | Schannel hybrid not automatic (secondary) | Opt-in | https://www.msn.com/en-us/technology/cybersecurity/post-quantum-cryptography-comes-to-windows-tls-three-ml-kem-groups-now-configurable/ar-AA27YDnL | "none of this activates automatically" | 2026-07-15 |
| F42 | Sanitizer API status | Not Baseline | https://developer.mozilla.org/en-US/docs/Web/API/HTML_Sanitizer_API | "This feature is not Baseline because it does not work in some of the most widely-used browsers." | read 2026-09-23 |
| F43 | Sanitizer API shipping (secondary) | Chrome 146, Firefox 148 | https://slcyber.io/research-center/two-bypasses-for-chromes-sanitizer-api/ | "arrived with much fanfare in both Chrome 146 and Firefox 148" | 2026-05-22 |
| F44 | Bad Practices v2 roadmap ask | By end of 2025, non-binding | https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-product-security-bad-practices-508c_0.pdf | "should publish a memory safety roadmap by the end of 2025" | 2025-01-17 |
| F45 | Bad Practices v1 date | 1 Jan 2026 | https://www.cisa.gov/sites/default/files/2024-10/joint-guidance-product-security-bad-practices-508c.pdf | "should publish a memory safety roadmap by January 1, 2026" | 2024-10 |
| F46 | CISA/NSA MSL guide | June 2025 | https://www.cisa.gov/resources-tools/resources/memory-safe-languages-reducing-vulnerabilities-modern-software-development | "Write new components and features in MSLs." | 2025-06-24 |
| F47 | Package hallucination rate | ≥5.2% commercial; 21.7% open-source | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | "at least 5.2% for commercial models and 21.7% for open-source models" | 2025-08 |
| F48 | Unique hallucinated names | 205,474 | same | "205,474 unique examples of hallucinated package names" | 2025-08 |
| F49 | Veracode AI code flaw rate | 45% | https://www.businesswire.com/news/home/20250730694951/en/AI-Generated-Code-Poses-Major-Security-Risks-in-Nearly-Half-of-All-Development-Tasks-Veracode-Research-Reveals | "introduces security vulnerabilities in 45 percent of cases" | 2025-07-30 |

## 4. Findings

### 4.1 OWASP Top 10:2025, ASVS 5.0, CWE Top 25

**Top 10:2025.** The ten categories are listed in the Summary (source: owasp.org/Top10/2025). Mapping from 2021, taken from secondary vendor analyses (Fastly, Orca, Reflectiz):

- A01 Broken Access Control stays #1 and now includes SSRF, which was A10:2021.
- Security Misconfiguration rises from #5 to #2.
- A03 Software Supply Chain Failures is new. It widens 2021's "Vulnerable and Outdated Components".
- Cryptographic Failures falls to #4.
- Injection falls to #5.
- Insecure Design moves from #4 to #6.
- "Identification and Authentication Failures" is renamed Authentication Failures and stays at #7.
- A09 is renamed to add "Alerting".
- A10 Mishandling of Exceptional Conditions is new.

Prevention guidance for each category is on the individual pages (for example owasp.org/Top10/2025/A01_2025-Broken_Access_Control/). I did not fetch those pages in this run, so category-by-category prevention text is **not covered**. The receiving session should pull it from the linked pages rather than rely on vendor blogs. For the skills, the interpretation is:

- The two new categories (supply chain, exceptional conditions) are the gaps most existing secure-coding checklists miss.
- The SSRF merge means access-control reviews must now include outbound requests the server makes.

**ASVS 5.0.0.** Released May 2025 at Global AppSec EU Barcelona (GitHub README). It has three levels (L1 to L3) and 345 requirements. OWASP's own ASVS repository (5.0/en/0x05-For-Users-Of-4.0.md) says 70 of them are L1 ("70 L1 requirements out of a total of 345 requirements, representing 20%"), against 128 L1 out of 278 in 4.0.3. It has 17 chapters (secondary: CyberSigma):

- V1 Encoding and Sanitization
- V2 Validation and Business Logic
- V3 Web Frontend Security
- V4 API and Web Service
- V5 File Handling
- V6 Authentication
- V7 Session Management
- V8 Authorization
- V9 Self-contained Tokens
- V10 OAuth and OIDC
- V11 Cryptography
- V12 Secure Communication
- V13 Configuration
- V14 Data Protection
- V15 Secure Coding and Architecture
- V16 Security Logging and Error Handling
- V17 WebRTC

Some secondary guides (securecodinghub.com) say "14 chapters". That contradicts the others and should be treated as wrong: the official ASVS repository is the authority, and the 17-chapter list above matches the repository's structure. Requirement IDs look like v5.0.0-1.2.3. When citing a requirement, pin the version prefix, because IDs were renumbered from 4.0.3.

**CWE Top 25 (2025).** Rank, CWE, then name:

1. CWE-79 XSS
2. CWE-89 SQL injection
3. CWE-352 CSRF
4. CWE-862 Missing Authorization
5. CWE-787 Out-of-bounds Write
6. CWE-22 Path Traversal
7. CWE-416 Use After Free
8. CWE-125 Out-of-bounds Read
9. CWE-78 OS Command Injection
10. CWE-94 Code Injection
11. CWE-120 Classic Buffer Overflow
12. CWE-434 Unrestricted Upload
13. CWE-476 NULL Pointer Dereference
14. CWE-121 Stack-based Buffer Overflow
15. CWE-502 Deserialization of Untrusted Data
16. CWE-122 Heap-based Buffer Overflow
17. CWE-863 Incorrect Authorization
18. CWE-20 Improper Input Validation
19. CWE-284 Improper Access Control
20. CWE-200 Exposure of Sensitive Information
21. CWE-306 Missing Authentication for Critical Function
22. CWE-918 SSRF
23. CWE-77 Command Injection
24. CWE-639 Authorization Bypass Through User-Controlled Key
25. CWE-770 Allocation of Resources Without Limits

Source: cwe.mitre.org 2025 list. Four of the top ten are memory-safety weaknesses, and seven entries are authorization or access control. That supports making access control and memory safety first-class skill topics, not footnotes. MITRE's CWE catalogue itself is at version 4.20 (April 2026, per secondary CloudSEK; the MITRE page title also shows "(4.20)").

### 4.2 Input handling

**Primary facts verified in this run:**
- ASVS 5.0 separates V1 "Encoding and Sanitization" from V2 "Validation and Business Logic". This is the current authoritative framing: validation enforces what input must be (business rules, allow-lists), while encoding and sanitization make output safe for the place it is used. Skills should keep these as separate steps and not use "sanitize" as a catch-all.
- Improper Input Validation (CWE-20) fell six places to #18 in the 2025 Top 25, while the specific injection sinks (79, 89, 78, 94, 77, 22, 502) rank higher. CWE's mapping guidance encourages mapping to the specific root cause, which the ranking reflects. Guidance should name the specific sink.
- **HTML Sanitizer API:** `setHTML()` always enforces an XSS-safe baseline. That baseline removes `<embed>`, `<frame>`, `<iframe>`, `<object>`, `<script>`, `<use>` and all event-handler attributes, and does so even if a custom configuration allows them (MDN). It shipped in Firefox 148 (24 February 2026) and Chrome 146 but is "not Baseline" (MDN). Searchlight Cyber published two bypasses of Chrome's implementation on 22 May 2026. `setHTMLUnsafe()` is Baseline 2025 but is an injection sink; pair it with Trusted Types. **Recommendation:** use `setHTML()` where `'setHTML' in Element.prototype`, otherwise DOMPurify. Sanitize on the server too, because client-side sanitization is not a trust boundary.

**Per-context techniques.** These are the long-standing OWASP Cheat Sheet positions, but I did not re-fetch the individual cheat sheets in this run. Each needs checking against the named sheet before it goes into a facts file:

| Context | Technique | Cheat sheet to verify against |
|---|---|---|
| SQL | Parameterized queries or prepared statements; allow-list identifiers such as table and column names, which cannot be bound | Query Parameterization; SQL Injection Prevention |
| HTML body/attributes | Contextual output encoding by the template engine; avoid raw-HTML escape hatches; Trusted Types to lock DOM sinks | Cross Site Scripting Prevention; DOM-based XSS Prevention |
| JavaScript/CSS/URL contexts | Avoid putting untrusted data in script or style blocks; if unavoidable use context-specific encoders; for URLs, validate the scheme against an allow-list (https) and then percent-encode components | XSS Prevention |
| Shell/process | Do not invoke a shell; call the program directly with an argument array; allow-list the arguments | OS Command Injection Defense |
| File paths | Canonicalize the path, then check it is inside an allow-listed base directory; prefer server-generated names | Input Validation; File Upload |
| File uploads | Allow-list extensions, validate content type and magic bytes, rename, store outside the webroot, enforce size limits | File Upload |
| XML | Disable DTDs and external entities in the parser | XML External Entity Prevention |
| Deserialization | Do not deserialize untrusted data with native formats; use data-only formats with schema validation | Deserialization |
| Regex (ReDoS) | Avoid nested quantifiers; set timeouts or use linear-time engines (e.g. RE2) | (OWASP ReDoS community page; not verified) |
| LDAP | Escape distinguished names and filters with a framework encoder | LDAP Injection Prevention |
| Templates (SSTI) | Never build templates from user input; pass user data only as template variables; sandbox | (not verified) |
| Logs | Encode or strip CR/LF and use structured logging | Logging |

### 4.3 Authentication and sessions

**Passwords (SP 800-63B-4, §3.1.1.2).** The rules are:

- Minimum length is 15 when the password is the only factor, 8 when it is part of MFA.
- Allow at least 64 characters (SHOULD).
- Accept all printing ASCII characters and the space (SHOULD).
- Composition rules SHALL NOT be imposed.
- Check the whole password against a blocklist, not substrings, and give the reason when rejecting one.
- The blocklist only needs to stop passwords likely to be guessed before throttling kicks in. NIST notes that very large blocklists add little.

The Wikipedia summary says the no-composition rule was tightened from "should not" to "shall not" in revision 4. I have not checked that change against revision 3's text, so treat the "tightened" claim as secondary. The same §3.1.1.2 of SP 800-63B-4 (pages.nist.gov/800-63-4/sp800-63b/authenticators) also sets these rules:

- Periodic change is banned: verifiers "SHALL NOT require subscribers to change passwords periodically", but "SHALL force a change if there is evidence that the authenticator has been compromised".
- Password managers and autofill SHALL be allowed. Paste is only a SHOULD ("SHOULD permit claimants to use the 'paste' function"), not a SHALL as some secondary summaries say.
- Password hints and knowledge-based questions are both SHALL NOT.

Secondary sources (Netwrix, Threatcop) also report that SMS OTP no longer meets AAL2. The receiving session should confirm that point from pages.nist.gov/800-63-4/sp800-63b before filing.

**Passkeys/WebAuthn Level 3, session management, account recovery:** not covered in this run (no primary source fetched). NIST also published SP 800-63Bsup1, "Incorporating Syncable Authenticators", which the CSRC page notes as a supplement. Whether it has since been folded into revision 4 was not checked.

**OAuth.**

- RFC 9700 is the current security BCP.
- OAuth 2.1 (-16) consolidates it: PKCE for every authorization-code client, exact redirect-URI string matching, no implicit grant, no password grant, no bearer tokens in query strings, and refresh tokens for public clients must be sender-constrained or rotated (oauth.net).
- Sender-constraining is done with DPoP or mTLS; oauth.net lists both as security extensions. Their RFC numbers were not re-verified in this run.
- oauth.net states that OAuth for Browser-Based Apps is now RFC 10017.

**Recommendation:** write skills against RFC 9700 with 2.1 semantics; do not wait for 2.1 to become an RFC.

**JWT.** RFC 8725 remains the BCP until rfc8725bis is published. The bis draft adds new threat sections, for example "Check JWT Format Type" and "Limit JWE Decompression Size" in -02, and it mitigates JWT serialization-format confusion. Skill guidance should already include:

- pin the allowed algorithms
- require `exp`
- check `iss` and `aud`
- check `typ` explicitly
- limit decompressed JWE size

### 4.4 Password storage

- **OWASP preference order:** Argon2id, then scrypt, then bcrypt (legacy only), then PBKDF2 (only where FIPS-140 is required). Parameters are in F18 to F21.
- **Alternative Argon2id settings:** the cheat sheet also lists equal-strength alternatives such as m=47104 (46 MiB), t=1, p=1 (secondary: Snyk quoting the cheat sheet).
- **Pepper:** a shared secret stored separately from the database, for example in a vault or HSM. One approach is to HMAC or encrypt the password hash with it. It is defence in depth and "alone, it provides no additional secure characteristics".
- **Legacy migration:** wrap the old hash inside the new algorithm, or re-hash when the user next logs in. The cheat sheet covers this; details not re-fetched.
- **NIST view:** SP 800-63B-4 §3.1.1.2 requires that "The salt SHALL be at least 32 bits in length". The hashing scheme SHOULD be an approved one from the latest revision of SP 800-132, and a separately stored secret key SHOULD be used for an extra keyed-hash iteration, ideally inside an HSM or TEE. NIST does not require a memory-hard KDF, so OWASP's Argon2id preference is stricter than NIST.

### 4.5 Cryptography and post-quantum migration

**Verified in this run:**
- FIPS 203 (ML-KEM), 204 (ML-DSA) and 205 (SLH-DSA) were published on 13 August 2024.
- HQC was selected on 11 March 2025 as a code-based backup KEM. NIST's Dustin Moody: organizations "should continue to migrate their encryption systems to the standards NIST finalized in 2024" (via SecurityWeek, secondary). The draft HQC standard was expected roughly a year after selection, with a final version in 2027 (secondary: Encryption Consulting). Current status not found.
- IR 8547 is still an initial public draft. It covers RSA, ECDSA, EdDSA, DH and ECDH. At 112-bit strength they are deprecated after 2030; everything quantum-vulnerable is disallowed after 2035.
- US policy (secondary, unverified): postquantum.com reports that Executive Order 14412 and OMB M-26-15 (June 2026) direct agencies to align with IR 8547. I did not verify this against a primary source, so treat it as unconfirmed.

**Hybrid key exchange status (September 2026):**

| Platform | Status | Source |
|---|---|---|
| OpenSSL 3.5 (LTS) | X25519MLKEM768 + X25519 sent by default; hybrid groups preferred | openssl-library.org 3.5 notes |
| Go | Default since 1.24 when `CurvePreferences` is nil; turn off with `GODEBUG=tlsmlkem=0` | go.dev/doc/go1.24 |
| Java | JDK 27 (JEP 527): X25519MLKEM768 first in the default named groups; SecP256r1MLKEM768 and SecP384r1MLKEM1024 available but not enabled by default. ML-KEM itself has been in the JDK since 24 (JEP 496) | openjdk.org/jeps/527; jdk.java.net/27 |
| .NET / Windows | Schannel hybrid ML-KEM groups GA on Windows 11 and Server 2025 (July 2026 updates). Not automatic; needs TLS 1.3. .NET on Windows uses Schannel. ML-KEM/ML-DSA APIs have been in Windows CNG since November 2025 | Microsoft Tech Community FAQ |
| Browsers | Not verified in this run; JEP 527 says X25519MLKEM768 is what most TLS clients currently enable | openjdk.org/jeps/527 |

Classical guidance (TLS 1.3 cipher suites, AEAD choice, CSPRNG APIs, key sizes): not covered by primary sources in this run.

**What application developers should do now:**
1. Rely on platform TLS defaults and don't hard-code named groups or cipher lists. Code that sets `CurvePreferences` (Go) or `jdk.tls.namedGroups` (Java) turns hybrid off.
2. Move to TLS 1.3 everywhere, because post-quantum key exchange does not exist for TLS 1.2 (Microsoft FAQ).
3. Upgrade to OpenSSL 3.5+, Go 1.24+ and JDK 27; on Windows, opt in to Schannel hybrid groups.
4. Build a cryptographic inventory and design for crypto-agility; ASVS 5.0 V11 covers this.
5. Post-quantum signatures and certificates are not ready for general web PKI. Hybrid key exchange first addresses harvest-now-decrypt-later, while authentication can wait (Microsoft).

### 4.6 Threat modelling
Not covered: no primary sources fetched in this run. See §9.

### 4.7 Secrets
Not covered: no primary sources fetched in this run. See §9.

### 4.8 Security tooling
Not covered: no versions verified in this run. See §5 and §9.

### 4.9 Secure HTTP configuration
Not covered: only the Sanitizer API and Trusted Types notes in §4.2 are sourced. See §9.

### 4.10 Security of AI-generated code

- **Veracode 2025 GenAI Code Security Report** (30 July 2025; vendor study, possible bias; static-analysis method):
  - 80 coding tasks across more than 100 LLMs, in Java, JavaScript, Python and C#.
  - AI "introduces security vulnerabilities in 45 percent of cases".
  - Java failed 72% of the time, and XSS (CWE-80) tasks failed 86% of the time.
  - Security did not improve with newer or larger models.
  - No C/C++ was tested.
- **Spracklen et al., USENIX Security 2025:**
  - 16 LLMs, 576,000 Python and JavaScript samples.
  - Hallucinated packages averaged at least 5.2% for commercial models and 21.7% for open-source models, with 205,474 unique names.
  - The paper does not use the word "slopsquatting"; that term came later.
  - The paper itself reports that "43% of hallucinated packages were repeated in all 10 queries" and 39% never repeated, and that a hallucinated package came back more than once in 10 runs 58% of the time. That repeatability is what makes the names worth registering.
- **Mitigations**, implied by these findings and by OWASP A03:2025:
  - Verify that every dependency an assistant suggests exists and is the intended one before installing it.
  - Pin versions with lockfiles.
  - Use an internal registry proxy or allow-list.
  - Run SAST on AI output as on human code.
  - Do not let agents run `npm install` or `pip install` without review.

### 4.11 Memory safety

- **CISA/FBI Product Security Bad Practices v2** (17 January 2025; non-binding):
  - Manufacturers should publish a memory-safety roadmap "by the end of 2025". Version 1 (October 2024) said 1 January 2026.
  - Products whose end of support falls before 1 January 2030 are exempt.
  - Starting new product lines for critical infrastructure in C/C++ is "dangerous" where memory-safe alternatives are readily available.
  - Recommended approach: short-term mitigations (hardware and compiler controls), new code in memory-safe languages, and gradual rewrites of high-risk components.
- **Secure by Design pledge** (May 2024): voluntary. A memory-safety roadmap is one example of reducing whole classes of vulnerability, with progress expected within a year of signing. It sets no fixed date.
- **CISA/NSA "Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development"** (June 2025):
  - Memory-safe languages are the most complete mitigation.
  - Full rewrites are often impractical, so adopt them step by step.
  - Write new components in memory-safe languages and put robust APIs at the boundary between memory-safe and other code.
  - The guide (CSI U/OO/172709-25, June 2025) says Android chose memory-safe languages, "specifically Rust and Java, for all new development", and that by 2024 "memory safety vulnerabilities had plummeted to 24% of the total", down from 76% in 2019. These quotes come via SecurityOnline because the PDF blocked fetching. Secondary coverage lists Ada, C#, Delphi/Object Pascal, Go, Java, Python, Ruby, Rust and Swift as the memory-safe languages it names.
- **What C/C++ teams should do:**
  - Publish a roadmap. The dates have passed, so this is now overdue under CISA's framing.
  - Write new modules in a memory-safe language.
  - Harden the existing C/C++ with compiler and hardware mitigations in the meantime.

## 5. Tools

Only items verified in this run are filled in. Everything else is marked "not verified" and must be re-checked in a later run.

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| OpenSSL | TLS/crypto library | 3.5 LTS series (latest patch not verified; secondary VersionLog says 3.5.6) | 3.5.0: 8 Apr 2025 | system package | openssl.cnf (`default_groups`) | openssl-library.org 3.5 notes |
| Go crypto/tls | TLS | Go 1.24+ has hybrid default; latest Go not verified | 1.24: Feb 2025 | `go` toolchain | `GODEBUG=tlsmlkem=0` to disable | go.dev/doc/go1.24 |
| JDK SunJSSE | TLS | JDK 27 (JEP 527) | Sept 2026 (secondary: JVM Weekly "JDK 27 is here") | JDK | `jdk.tls.namedGroups` | openjdk.org/jeps/527 |
| Windows Schannel | TLS | KB5099536 (Server 2025) | 14 Jul 2026 | Windows Update | OS TLS policy | Microsoft Tech Community FAQ |
| DOMPurify / Sanitizer API | HTML sanitization | Sanitizer API: Chrome 146, Firefox 148; DOMPurify version not verified | Firefox 148: 24 Feb 2026 | — | — | MDN; slcyber.io |
| CodeQL, Semgrep, ruff (S), bandit, eslint-plugin-security, Roslyn analyzers, PSScriptAnalyzer, gosec, cargo-deny, cargo-audit, Brakeman, PHPStan, Psalm, SpotBugs+FindSecBugs, OWASP ZAP, gitleaks, TruffleHog, Threat Dragon, MS Threat Modeling Tool | SAST, linting, DAST, secret scanning, threat modelling | not verified | not verified | not verified | not verified | — |

## 6. Changing in the next 12 months

- **OpenSSL 3.5 LTS:** support runs to 8 April 2030 (secondary), so it does not reach end of support in the next 12 months. The support end dates of other OpenSSL branches were not checked.
- **RFC 8725 → rfc8725bis:** past IETF Last Call (June 2026). Publication as a BCP that obsoletes RFC 8725 is likely within 12 months, but no date has been announced (my inference).
- **OAuth 2.1:** -16 expires on 7 March 2027. No RFC date has been announced.
- **ASVS 5.0.1:** announced as the next release; no date found.
- **NIST IR 8547 final:** no date found. HQC draft FIPS: no date confirmed in this run. FIPS 206 (FN-DSA): in development.
- **Go 1.25:** 1.25.14 was released on 19 August 2026 (go.dev release history). Go supports its two newest major releases, so 1.25 will lose support when the next major version ships after 1.26 (policy not re-verified; no date found).
- **CISA memory-safety roadmap:** the "end of 2025" date has passed. Publishing a roadmap is now overdue under CISA's (non-binding) framing.
- **Hybrid key exchange:** now an RFC (RFC 10024, August 2026, secondary). Expect more libraries to turn it on by default.
- **Federal PQC policy:** EO 14412 and OMB M-26-15 (June 2026) are reported but unverified; see §4.5.

## 7. Common mistakes (including AI assistants)

- **Installing packages an assistant names without checking they exist.** 5.2% to 21.7% of suggested packages are hallucinated (Spracklen et al.).
- **Accepting AI code without SAST.** 45% of samples had flaws, and bigger models were no better (Veracode).
- **Hard-coding TLS groups or cipher lists.** This silently turns hybrid post-quantum key exchange off (JEP 527; Go 1.24 notes).
- **Citing out-of-date password-hash parameters,** for example PBKDF2 310,000 or scrypt 2^16. These still circulate in mirrors of the OWASP cheat sheet (see the rdwz and Web-Development-Tutorials mirrors), while the current sheet says 600,000 and 2^17.
- **bcrypt without a 72-byte input limit.** Longer passwords are silently truncated (OWASP).
- **Password composition rules or an 8-character minimum for single-factor logins.** Both contradict SP 800-63B-4.
- **Using `setHTMLUnsafe()` or `innerHTML` with untrusted data,** or assuming `setHTML()` exists without feature detection (MDN).
- **Implicit or password grants, or PKCE only for public clients.** Both contradict OAuth 2.1 and RFC 9700.
- **Treating the Secure by Design pledge as setting a 1 January 2026 deadline.** It does not; see C12.
- **Citing OWASP Top 10:2021 category numbers,** such as A06 for vulnerable components or A10 for SSRF. They are out of date.

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| OWASP Top 10:2025 | CC BY 3.0 (stated on page) | Yes | Yes | Yes | "OWASP Top 10:2025, OWASP Top 10 Team, CC BY 3.0", with link |
| OWASP ASVS 5.0 | CC BY-SA 4.0 (secondary: arc42, CyberSigma; check the repo LICENSE) | Yes, briefly | Yes | Adapted text is share-alike, so keep adapted ASVS text in separately licensed CC BY-SA files and do not relicense it as Apache-2.0 | Credit OWASP ASVS and give the licence |
| OWASP Cheat Sheet Series | Believed CC BY-SA 4.0; not verified in this run | Yes, briefly | Yes | Treat code snippets as CC BY-SA until checked | Credit and link |
| MITRE CWE | MITRE CWE Terms of Use (linked from cwe.mitre.org; not read in this run) | Yes | Yes | n/a | Credit "MITRE CWE" |
| NIST SPs/IRs, FIPS | US Government work; not read in this run | Yes | Yes | n/a | Cite NIST |
| IETF RFCs/drafts | BCP 78 / IETF Trust Legal Provisions (stated in the documents) | Yes, briefly | Yes | Code components under the Trust's Revised BSD terms (not re-read) | Cite the RFC number |
| CISA/NSA publications | US Government work; not verified in this run | Yes | Yes | n/a | Cite the agency |
| OpenSSL release notes | Apache-2.0 for code (not verified for docs) | Yes, briefly | Yes | — | Link |
| Go release notes / pkg docs | BSD-3-Clause (pkg.go.dev shows it for crypto/tls) | Yes | Yes | Yes, with the BSD notice | Credit The Go Authors |
| OpenJDK JEP 527 / release notes | not found | Short quote only | Yes | No | Link |
| Microsoft Tech Community | Microsoft terms; not found | Short quote only | Yes | No | Link |
| MDN | not verified in this run (MDN states its terms on each page) | Short quote only | Yes | Check before adapting | Credit MDN contributors |
| USENIX paper (Spracklen et al.) | not found (USENIX open access) | Short quote only | Yes | n/a | Full citation |
| Veracode, Fastly, Orca, Qualys, Reflectiz, Encryption Consulting, postquantum.com, JVM Weekly, Searchlight Cyber, CyberSigma, Snyk (secondary) | All rights reserved (assumed) | Short quote only | Yes | No | Link and label as secondary |

## 9. Not found, contested, not covered

**Not found**
- The exact release date of the final OWASP Top 10:2025 (only the release candidate date of 6 November 2025 was found).
- The release date for ASVS 5.0.1.
- The finalization date for NIST IR 8547.
- The HQC draft FIPS number and date.
- The licences of the OpenJDK, Microsoft and USENIX pages.
- A primary source for the browsers' defaults for X25519MLKEM768.

**Contested**
- **ASVS 5.0 chapter count:** 17 (OWASP-derived sources, CyberSigma, arc42) against 14 (securecodinghub.com). Use 17.
- **Password rotation and paste rules in 800-63B-4:** now confirmed at primary level (§3.1.1.2). Periodic rotation is SHALL NOT, and a change is forced only on evidence of compromise. Paste is SHOULD, not SHALL, so secondary sources that call paste mandatory overstate it.
- **Package-hallucination totals:** a CSA note gives "2.23 million" and "440,445 (19.7%)", while the paper's abstract gives 576,000 samples. The CSA figures probably count package references rather than samples. Use the abstract figures.

**Not covered (search budget exhausted; carry into the next run)**
- Q1: per-category prevention guidance for the Top 10:2025.
- Q2: re-verifying each OWASP cheat sheet named in §4.2, plus Trusted Types browser status.
- Q3: WebAuthn Level 3 status, passkeys, session management, MFA and recovery rules in 800-63B-4, DPoP (RFC 9449) and mTLS (RFC 8705) numbers, and OpenID Connect.
- Q4: the legacy-hash migration procedure in detail. NIST's own storage parameters are now covered in §4.4.
- Q5: classical algorithm and key-size guidance, TLS 1.3 settings, CSPRNG and AEAD guidance.
- Q6: threat modelling (STRIDE, Threat Modeling Manifesto, OWASP cheat sheet, Threat Dragon, MS Threat Modeling Tool).
- Q7: secrets (vaults, OIDC workload identity, gitleaks, TruffleHog, GitHub secret scanning, leak response).
- Q8: all tool versions and whether they are free for public repositories.
- Q9: security headers, cookies (including CHIPS), CORS and rate limiting.